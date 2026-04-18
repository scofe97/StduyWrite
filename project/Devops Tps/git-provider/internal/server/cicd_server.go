package server

import (
	"context"
	"log"
	"time"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"

	"github.com/runners-high/git-provider/internal/cicd"
	"github.com/runners-high/git-provider/internal/jenkins"
	"github.com/runners-high/git-provider/internal/kafka"
	"github.com/runners-high/git-provider/internal/pipeline"
	pb "github.com/runners-high/git-provider/pkg/pb/v1"
)

type CICDServer struct {
	pb.UnimplementedCICDServiceServer
	store    *pipeline.Store
	producer *kafka.EventProducer
}

func NewCICDServer(store *pipeline.Store, producer *kafka.EventProducer) *CICDServer {
	return &CICDServer{
		store:    store,
		producer: producer,
	}
}

// =============================================================================
// Pipeline CRUD
// =============================================================================

func (s *CICDServer) CreatePipeline(ctx context.Context, req *pb.CreatePipelineRequest) (*pb.CreatePipelineResponse, error) {
	if req.Name == "" {
		return nil, status.Error(codes.InvalidArgument, "name is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository is required")
	}
	if req.CiConfig == nil {
		return nil, status.Error(codes.InvalidArgument, "ci_config is required")
	}

	p := s.store.CreatePipeline(req.Name, req.Repository, req.BranchPattern, req.JenkinsJobName, req.Stages, req.CiConfig)
	return &pb.CreatePipelineResponse{Pipeline: p}, nil
}

func (s *CICDServer) GetPipeline(ctx context.Context, req *pb.GetPipelineRequest) (*pb.GetPipelineResponse, error) {
	if req.Id == "" {
		return nil, status.Error(codes.InvalidArgument, "id is required")
	}

	p, err := s.store.GetPipeline(req.Id)
	if err != nil {
		return nil, status.Errorf(codes.NotFound, "pipeline not found: %v", err)
	}
	return &pb.GetPipelineResponse{Pipeline: p}, nil
}

func (s *CICDServer) ListPipelines(ctx context.Context, req *pb.ListPipelinesRequest) (*pb.ListPipelinesResponse, error) {
	pipelines := s.store.ListPipelines(req.Repository)
	return &pb.ListPipelinesResponse{Pipelines: pipelines}, nil
}

func (s *CICDServer) DeletePipeline(ctx context.Context, req *pb.DeletePipelineRequest) (*pb.DeletePipelineResponse, error) {
	if req.Id == "" {
		return nil, status.Error(codes.InvalidArgument, "id is required")
	}

	if err := s.store.DeletePipeline(req.Id); err != nil {
		return nil, status.Errorf(codes.NotFound, "pipeline not found: %v", err)
	}
	return &pb.DeletePipelineResponse{Success: true}, nil
}

// =============================================================================
// Build 관리
// =============================================================================

func (s *CICDServer) TriggerBuild(ctx context.Context, req *pb.TriggerBuildRequest) (*pb.TriggerBuildResponse, error) {
	if req.PipelineId == "" {
		return nil, status.Error(codes.InvalidArgument, "pipeline_id is required")
	}

	p, err := s.store.GetPipeline(req.PipelineId)
	if err != nil {
		return nil, status.Errorf(codes.NotFound, "pipeline not found: %v", err)
	}

	branch := req.Branch
	if branch == "" {
		branch = p.BranchPattern
	}

	// Build 레코드 생성
	build, err := s.store.AddBuild(p.Id, "manual", branch, req.CommitSha)
	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to create build: %v", err)
	}

	// Jenkins 빌드 트리거
	jenkinsClient, err := cicd.CreateJenkinsClient(p.CiConfig)
	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to create jenkins client: %v", err)
	}

	params := map[string]string{
		"BRANCH": branch,
	}
	if req.CommitSha != "" {
		params["COMMIT_SHA"] = req.CommitSha
	}

	queueID, err := jenkinsClient.TriggerBuild(ctx, p.JenkinsJobName, params)
	if err != nil {
		log.Printf("jenkins trigger failed (build will stay QUEUED): %v", err)
		// 빌드 레코드는 이미 생성됨 — Jenkins 연결 실패해도 레코드 유지
	} else {
		// 빌드 번호 확인을 위한 비동기 폴링
		go s.pollBuildNumber(context.Background(), jenkinsClient, p, build, queueID)
	}

	return &pb.TriggerBuildResponse{Build: build}, nil
}

func (s *CICDServer) GetBuild(ctx context.Context, req *pb.GetBuildRequest) (*pb.GetBuildResponse, error) {
	if req.PipelineId == "" {
		return nil, status.Error(codes.InvalidArgument, "pipeline_id is required")
	}

	build, err := s.store.GetBuild(req.PipelineId, req.BuildNumber)
	if err != nil {
		return nil, status.Errorf(codes.NotFound, "build not found: %v", err)
	}
	return &pb.GetBuildResponse{Build: build}, nil
}

func (s *CICDServer) ListBuilds(ctx context.Context, req *pb.ListBuildsRequest) (*pb.ListBuildsResponse, error) {
	if req.PipelineId == "" {
		return nil, status.Error(codes.InvalidArgument, "pipeline_id is required")
	}

	builds := s.store.ListBuilds(req.PipelineId, req.Limit)
	return &pb.ListBuildsResponse{Builds: builds}, nil
}

func (s *CICDServer) GetBuildLog(ctx context.Context, req *pb.GetBuildLogRequest) (*pb.GetBuildLogResponse, error) {
	if req.PipelineId == "" {
		return nil, status.Error(codes.InvalidArgument, "pipeline_id is required")
	}

	build, err := s.store.GetBuild(req.PipelineId, req.BuildNumber)
	if err != nil {
		return nil, status.Errorf(codes.NotFound, "build not found: %v", err)
	}

	p, err := s.store.GetPipeline(req.PipelineId)
	if err != nil {
		return nil, status.Errorf(codes.NotFound, "pipeline not found: %v", err)
	}

	jenkinsClient, err := cicd.CreateJenkinsClient(p.CiConfig)
	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to create jenkins client: %v", err)
	}

	logText, err := jenkinsClient.GetBuildLog(ctx, p.JenkinsJobName, int(build.BuildNumber))
	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to get build log: %v", err)
	}

	return &pb.GetBuildLogResponse{Log: logText}, nil
}

// =============================================================================
// Helper
// =============================================================================

// pollBuildNumber polls Jenkins queue until build number is assigned, then polls build status.
func (s *CICDServer) pollBuildNumber(ctx context.Context, client *jenkins.JenkinsClient, p *pb.Pipeline, build *pb.Build, queueID int64) {
	// 큐에서 빌드 번호 확인 (최대 60초)
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
	// 빌드 상태를 RUNNING으로 업데이트
	_ = s.store.UpdateBuildStatus(p.Id, build.BuildNumber, pb.BuildStatus_BUILD_STATUS_RUNNING, "", 0)

	// 빌드 완료 폴링 (최대 30분)
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

			// 빌드 완료
			finalStatus := mapJenkinsResult(info.Result)
			duration := int32(info.Duration / 1000) // ms → seconds
			_ = s.store.UpdateBuildStatus(p.Id, build.BuildNumber, finalStatus, info.URL, duration)

			// cicd-results 이벤트 발행
			if s.producer != nil {
				event := kafka.BuildResultEvent{
					PipelineID:      p.Id,
					BuildNumber:     int(build.BuildNumber),
					Status:          info.Result,
					DurationSeconds: int(duration),
					URL:             info.URL,
					Timestamp:       time.Now().UTC().Format(time.RFC3339),
				}
				if err := s.producer.Publish(ctx, kafka.TopicCICDResults, p.Id, event); err != nil {
					log.Printf("failed to publish build result: %v", err)
				}
			}
			return
		}
	}
}

func mapJenkinsResult(result string) pb.BuildStatus {
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
