package service

import (
	"context"
	"fmt"
	"time"

	"github.com/google/uuid"
	"github.com/runners-high/git-api/internal/client"
	"github.com/runners-high/git-api/pkg/event"
	"github.com/runners-high/git-api/pkg/kafka"
	"go.uber.org/zap"
)

// GitService handles git operations
type GitService struct {
	producer *kafka.Producer
	logger   *zap.Logger
}

// NewGitService creates a new git service
func NewGitService(producer *kafka.Producer, logger *zap.Logger) *GitService {
	return &GitService{
		producer: producer,
		logger:   logger,
	}
}

// HandleBranchCreate handles branch creation command
func (s *GitService) HandleBranchCreate(ctx context.Context, cmd *event.BranchCommand) error {
	s.logger.Info("Processing branch create command",
		zap.String("eventId", cmd.EventID),
		zap.String("repositoryId", cmd.Payload.RepositoryID),
		zap.String("branchName", cmd.Payload.BranchName))

	var commitSHA string
	var err error

	switch cmd.Payload.ConnectionType {
	case event.GitHub:
		ghClient := client.NewGitHubClient(ctx, cmd.Payload.AccessToken)
		baseBranch := cmd.Payload.BaseBranch
		if baseBranch == "" {
			baseBranch = "main"
		}
		commitSHA, err = ghClient.CreateBranch(ctx, cmd.Payload.RepositoryURL, cmd.Payload.BranchName, baseBranch)

	case event.GitLab:
		glClient, clientErr := client.NewGitLabClient(cmd.Payload.AccessToken)
		if clientErr != nil {
			err = clientErr
		} else {
			baseBranch := cmd.Payload.BaseBranch
			if baseBranch == "" {
				baseBranch = "main"
			}
			commitSHA, err = glClient.CreateBranch(ctx, cmd.Payload.RepositoryURL, cmd.Payload.BranchName, baseBranch)
		}

	default:
		err = fmt.Errorf("unsupported connection type: %s", cmd.Payload.ConnectionType)
	}

	// Publish result event
	result := s.createBranchResult(cmd, commitSHA, err)
	if pubErr := s.producer.Publish(result); pubErr != nil {
		s.logger.Error("Failed to publish result event", zap.Error(pubErr))
		return pubErr
	}

	if err != nil {
		s.logger.Error("Branch creation failed",
			zap.String("branchName", cmd.Payload.BranchName),
			zap.Error(err))
	} else {
		s.logger.Info("Branch created successfully",
			zap.String("branchName", cmd.Payload.BranchName),
			zap.String("commitSHA", commitSHA))
	}

	return nil
}

// HandleBranchDelete handles branch deletion command
func (s *GitService) HandleBranchDelete(ctx context.Context, cmd *event.BranchCommand) error {
	s.logger.Info("Processing branch delete command",
		zap.String("eventId", cmd.EventID),
		zap.String("repositoryId", cmd.Payload.RepositoryID),
		zap.String("branchName", cmd.Payload.BranchName))

	var err error

	switch cmd.Payload.ConnectionType {
	case event.GitHub:
		ghClient := client.NewGitHubClient(ctx, cmd.Payload.AccessToken)
		err = ghClient.DeleteBranch(ctx, cmd.Payload.RepositoryURL, cmd.Payload.BranchName)

	case event.GitLab:
		glClient, clientErr := client.NewGitLabClient(cmd.Payload.AccessToken)
		if clientErr != nil {
			err = clientErr
		} else {
			err = glClient.DeleteBranch(ctx, cmd.Payload.RepositoryURL, cmd.Payload.BranchName)
		}

	default:
		err = fmt.Errorf("unsupported connection type: %s", cmd.Payload.ConnectionType)
	}

	// Publish result event
	result := s.createBranchDeleteResult(cmd, err)
	if pubErr := s.producer.Publish(result); pubErr != nil {
		s.logger.Error("Failed to publish result event", zap.Error(pubErr))
		return pubErr
	}

	if err != nil {
		s.logger.Error("Branch deletion failed",
			zap.String("branchName", cmd.Payload.BranchName),
			zap.Error(err))
	} else {
		s.logger.Info("Branch deleted successfully",
			zap.String("branchName", cmd.Payload.BranchName))
	}

	return nil
}

// HandleRepositorySync handles repository sync command
func (s *GitService) HandleRepositorySync(ctx context.Context, cmd *event.RepositorySyncCommand) error {
	s.logger.Info("Processing repository sync command",
		zap.String("eventId", cmd.EventID),
		zap.String("repositoryId", cmd.Payload.RepositoryID))

	var repoInfo *client.RepositoryInfo
	var branches []string
	var err error

	switch cmd.Payload.ConnectionType {
	case event.GitHub:
		ghClient := client.NewGitHubClient(ctx, cmd.Payload.AccessToken)
		repoInfo, err = ghClient.GetRepository(ctx, cmd.Payload.RepositoryURL)
		if err == nil {
			branches, err = ghClient.GetBranches(ctx, cmd.Payload.RepositoryURL)
		}

	case event.GitLab:
		glClient, clientErr := client.NewGitLabClient(cmd.Payload.AccessToken)
		if clientErr != nil {
			err = clientErr
		} else {
			repoInfo, err = glClient.GetRepository(ctx, cmd.Payload.RepositoryURL)
			if err == nil {
				branches, err = glClient.GetBranches(ctx, cmd.Payload.RepositoryURL)
			}
		}

	default:
		err = fmt.Errorf("unsupported connection type: %s", cmd.Payload.ConnectionType)
	}

	// Publish result event
	result := s.createSyncResult(cmd, repoInfo, branches, err)
	if pubErr := s.producer.Publish(result); pubErr != nil {
		s.logger.Error("Failed to publish result event", zap.Error(pubErr))
		return pubErr
	}

	if err != nil {
		s.logger.Error("Repository sync failed",
			zap.String("repositoryId", cmd.Payload.RepositoryID),
			zap.Error(err))
	} else {
		s.logger.Info("Repository synced successfully",
			zap.String("repositoryId", cmd.Payload.RepositoryID),
			zap.Int("branchCount", len(branches)))
	}

	return nil
}

// HandlePullRequestCreate handles PR/MR creation command
func (s *GitService) HandlePullRequestCreate(ctx context.Context, cmd *event.PullRequestCommand) error {
	s.logger.Info("Processing pull request create command",
		zap.String("eventId", cmd.EventID),
		zap.String("repositoryId", cmd.Payload.RepositoryID))

	var prInfo *client.PullRequestInfo
	var err error

	switch cmd.Payload.ConnectionType {
	case event.GitHub:
		ghClient := client.NewGitHubClient(ctx, cmd.Payload.AccessToken)
		prInfo, err = ghClient.CreatePullRequest(ctx,
			cmd.Payload.RepositoryURL,
			cmd.Payload.Title,
			cmd.Payload.Description,
			cmd.Payload.SourceBranch,
			cmd.Payload.TargetBranch)

	case event.GitLab:
		glClient, clientErr := client.NewGitLabClient(cmd.Payload.AccessToken)
		if clientErr != nil {
			err = clientErr
		} else {
			prInfo, err = glClient.CreateMergeRequest(ctx,
				cmd.Payload.RepositoryURL,
				cmd.Payload.Title,
				cmd.Payload.Description,
				cmd.Payload.SourceBranch,
				cmd.Payload.TargetBranch)
		}

	default:
		err = fmt.Errorf("unsupported connection type: %s", cmd.Payload.ConnectionType)
	}

	// Publish result event
	result := s.createPRResult(cmd, prInfo, err)
	if pubErr := s.producer.Publish(result); pubErr != nil {
		s.logger.Error("Failed to publish result event", zap.Error(pubErr))
		return pubErr
	}

	if err != nil {
		s.logger.Error("Pull request creation failed",
			zap.String("repositoryId", cmd.Payload.RepositoryID),
			zap.Error(err))
	} else {
		s.logger.Info("Pull request created successfully",
			zap.String("repositoryId", cmd.Payload.RepositoryID),
			zap.String("prUrl", prInfo.URL))
	}

	return nil
}

// Helper methods for creating result events

func (s *GitService) createBranchResult(cmd *event.BranchCommand, commitSHA string, err error) *event.BranchResult {
	eventType := event.BranchCreated
	success := true
	errorMsg := ""

	if err != nil {
		eventType = event.OperationFailed
		success = false
		errorMsg = err.Error()
	}

	return &event.BranchResult{
		BaseEvent: event.BaseEvent{
			EventID:       uuid.New().String(),
			EventType:     eventType,
			Timestamp:     time.Now(),
			CorrelationID: cmd.EventID,
		},
		Payload: event.BranchResultPayload{
			RepositoryID: cmd.Payload.RepositoryID,
			BranchName:   cmd.Payload.BranchName,
			CommitSHA:    commitSHA,
			Success:      success,
			ErrorMessage: errorMsg,
		},
	}
}

func (s *GitService) createBranchDeleteResult(cmd *event.BranchCommand, err error) *event.BranchResult {
	eventType := event.BranchDeleted
	success := true
	errorMsg := ""

	if err != nil {
		eventType = event.OperationFailed
		success = false
		errorMsg = err.Error()
	}

	return &event.BranchResult{
		BaseEvent: event.BaseEvent{
			EventID:       uuid.New().String(),
			EventType:     eventType,
			Timestamp:     time.Now(),
			CorrelationID: cmd.EventID,
		},
		Payload: event.BranchResultPayload{
			RepositoryID: cmd.Payload.RepositoryID,
			BranchName:   cmd.Payload.BranchName,
			Success:      success,
			ErrorMessage: errorMsg,
		},
	}
}

func (s *GitService) createSyncResult(cmd *event.RepositorySyncCommand, repoInfo *client.RepositoryInfo, branches []string, err error) *event.RepositorySyncResult {
	eventType := event.RepositorySynced
	success := true
	errorMsg := ""
	defaultBranch := ""

	if err != nil {
		eventType = event.OperationFailed
		success = false
		errorMsg = err.Error()
	} else if repoInfo != nil {
		defaultBranch = repoInfo.DefaultBranch
	}

	return &event.RepositorySyncResult{
		BaseEvent: event.BaseEvent{
			EventID:       uuid.New().String(),
			EventType:     eventType,
			Timestamp:     time.Now(),
			CorrelationID: cmd.EventID,
		},
		Payload: event.RepositorySyncResultPayload{
			RepositoryID:  cmd.Payload.RepositoryID,
			DefaultBranch: defaultBranch,
			Branches:      branches,
			Success:       success,
			ErrorMessage:  errorMsg,
		},
	}
}

func (s *GitService) createPRResult(cmd *event.PullRequestCommand, prInfo *client.PullRequestInfo, err error) *event.PullRequestResult {
	eventType := event.PullRequestCreated
	success := true
	errorMsg := ""
	prID := ""
	prURL := ""

	if err != nil {
		eventType = event.OperationFailed
		success = false
		errorMsg = err.Error()
	} else if prInfo != nil {
		prID = prInfo.ID
		prURL = prInfo.URL
	}

	return &event.PullRequestResult{
		BaseEvent: event.BaseEvent{
			EventID:       uuid.New().String(),
			EventType:     eventType,
			Timestamp:     time.Now(),
			CorrelationID: cmd.EventID,
		},
		Payload: event.PullRequestResultPayload{
			RepositoryID:   cmd.Payload.RepositoryID,
			PullRequestID:  prID,
			PullRequestURL: prURL,
			Success:        success,
			ErrorMessage:   errorMsg,
		},
	}
}
