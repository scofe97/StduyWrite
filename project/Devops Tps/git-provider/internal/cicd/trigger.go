package cicd

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/runners-high/git-provider/internal/jenkins"
	"github.com/runners-high/git-provider/internal/kafka"
	pb "github.com/runners-high/git-provider/pkg/pb/v1"
)

// TriggerRequest contains the parameters for triggering a Jenkins build.
type TriggerRequest struct {
	Pipeline    *pb.Pipeline
	Branch      string
	CommitSHA   string
	ExecutionID string // optional: workflow execution reference
}

// CreateJenkinsClient creates a JenkinsClient from a pipeline's CIConfig.
func CreateJenkinsClient(ciConfig *pb.CIConfig) (*jenkins.JenkinsClient, error) {
	if ciConfig == nil {
		return nil, fmt.Errorf("ci_config is required")
	}

	switch config := ciConfig.Config.(type) {
	case *pb.CIConfig_Jenkins:
		return jenkins.NewJenkinsClient(config.Jenkins.Url, config.Jenkins.Username, config.Jenkins.ApiToken), nil
	default:
		return nil, fmt.Errorf("unsupported CI provider type")
	}
}

// TriggerAndPoll triggers a Jenkins build and polls for completion in the background.
// On completion, it updates the build store and publishes events.
func TriggerAndPoll(ctx context.Context, req TriggerRequest, store BuildStore, producer *kafka.EventProducer) (*pb.Build, error) {
	p := req.Pipeline
	branch := req.Branch
	if branch == "" {
		branch = p.BranchPattern
	}

	build, err := store.AddBuild(p.Id, "event", branch, req.CommitSHA)
	if err != nil {
		return nil, fmt.Errorf("create build: %w", err)
	}

	client, err := CreateJenkinsClient(p.CiConfig)
	if err != nil {
		return nil, fmt.Errorf("create jenkins client: %w", err)
	}

	params := map[string]string{"BRANCH": branch}
	if req.CommitSHA != "" {
		params["COMMIT_SHA"] = req.CommitSHA
	}

	queueID, err := client.TriggerBuild(ctx, p.JenkinsJobName, params)
	if err != nil {
		log.Printf("jenkins trigger failed: pipeline=%s err=%v", p.Id, err)
		// Publish failure event so workflow engine can mark execution as FAILED
		if producer != nil && req.ExecutionID != "" {
			failEvent := kafka.BuildCompletedEvent{
				Type:        "build_completed",
				PipelineID:  p.Id,
				BuildNumber: int(build.BuildNumber),
				Status:      "FAILURE",
				ExecutionID: req.ExecutionID,
				Timestamp:   time.Now().UTC().Format(time.RFC3339),
			}
			if pubErr := producer.Publish(ctx, kafka.TopicCICDEvents, p.Id, failEvent); pubErr != nil {
				log.Printf("failed to publish trigger failure event: %v", pubErr)
			}
		}
		_ = store.UpdateBuildStatus(p.Id, build.BuildNumber, pb.BuildStatus_BUILD_STATUS_FAILURE, "", 0)
		return build, fmt.Errorf("trigger build: %w", err)
	}

	go pollBuildNumber(context.Background(), client, p, build, queueID, req.ExecutionID, store, producer)
	return build, nil
}

// BuildStore is the subset of pipeline.Store needed by trigger logic.
type BuildStore interface {
	AddBuild(pipelineID, trigger, branch, commitSHA string) (*pb.Build, error)
	UpdateBuildStatus(pipelineID string, buildNumber int32, status pb.BuildStatus, url string, durationSeconds int32) error
	GetPipeline(id string) (*pb.Pipeline, error)
}

func pollBuildNumber(ctx context.Context, client *jenkins.JenkinsClient, p *pb.Pipeline, build *pb.Build, queueID int64, executionID string, store BuildStore, producer *kafka.EventProducer) {
	// Poll queue for build number (max 60s)
	ticker := time.NewTicker(2 * time.Second)
	defer ticker.Stop()
	timeout := time.After(60 * time.Second)

	var jenkinsBuildNumber int
	for {
		select {
		case <-timeout:
			log.Printf("timeout waiting for build number from queue %d", queueID)
			return
		case <-ticker.C:
			item, err := client.GetQueueItem(ctx, queueID)
			if err != nil {
				continue
			}
			if item.Executable != nil && item.Executable.Number > 0 {
				jenkinsBuildNumber = item.Executable.Number
				goto pollStatus
			}
		}
	}

pollStatus:
	_ = store.UpdateBuildStatus(p.Id, build.BuildNumber, pb.BuildStatus_BUILD_STATUS_RUNNING, "", 0)

	// Poll build status (max 30min)
	statusTicker := time.NewTicker(5 * time.Second)
	defer statusTicker.Stop()
	statusTimeout := time.After(30 * time.Minute)

	for {
		select {
		case <-statusTimeout:
			log.Printf("timeout waiting for build completion: job=%s build=%d", p.JenkinsJobName, jenkinsBuildNumber)
			return
		case <-statusTicker.C:
			info, err := client.GetBuild(ctx, p.JenkinsJobName, jenkinsBuildNumber)
			if err != nil {
				continue
			}
			if info.Building {
				continue
			}

			finalStatus := MapJenkinsResult(info.Result)
			duration := int32(info.Duration / 1000)
			_ = store.UpdateBuildStatus(p.Id, build.BuildNumber, finalStatus, info.URL, duration)

			// Publish to cicd-results (legacy)
			if producer != nil {
				legacyEvent := kafka.BuildResultEvent{
					PipelineID:      p.Id,
					BuildNumber:     int(build.BuildNumber),
					Status:          info.Result,
					DurationSeconds: int(duration),
					URL:             info.URL,
					Timestamp:       time.Now().UTC().Format(time.RFC3339),
				}
				if err := producer.Publish(ctx, kafka.TopicCICDResults, p.Id, legacyEvent); err != nil {
					log.Printf("failed to publish build result (legacy): %v", err)
				}

				// Publish to cicd.events (workflow-aware)
				wfEvent := kafka.BuildCompletedEvent{
					Type:            "build_completed",
					PipelineID:      p.Id,
					BuildNumber:     int(build.BuildNumber),
					Status:          info.Result,
					ExecutionID:     executionID,
					DurationSeconds: int(duration),
					URL:             info.URL,
					Timestamp:       time.Now().UTC().Format(time.RFC3339),
				}
				if err := producer.Publish(ctx, kafka.TopicCICDEvents, p.Id, wfEvent); err != nil {
					log.Printf("failed to publish build completed event: %v", err)
				}
			}
			return
		}
	}
}

// MapJenkinsResult converts Jenkins result string to BuildStatus proto enum.
func MapJenkinsResult(result string) pb.BuildStatus {
	switch result {
	case "SUCCESS":
		return pb.BuildStatus_BUILD_STATUS_SUCCESS
	case "FAILURE":
		return pb.BuildStatus_BUILD_STATUS_FAILURE
	case "ABORTED":
		return pb.BuildStatus_BUILD_STATUS_ABORTED
	default:
		return pb.BuildStatus_BUILD_STATUS_FAILURE
	}
}
