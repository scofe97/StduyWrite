package service

import (
	"testing"
	"time"

	"github.com/runners-high/git-api/internal/client"
	"github.com/runners-high/git-api/pkg/event"
)

func TestCreateBranchResult_Success(t *testing.T) {
	s := &GitService{}

	cmd := &event.BranchCommand{
		BaseEvent: event.BaseEvent{
			EventID:   "cmd-123",
			EventType: event.BranchCreateRequested,
			Timestamp: time.Now(),
		},
		Payload: event.BranchPayload{
			RepositoryID: "repo-1",
			BranchName:   "feature/test",
		},
	}

	result := s.createBranchResult(cmd, "abc123def", nil)

	if result.EventType != event.BranchCreated {
		t.Errorf("expected EventType BRANCH_CREATED, got %s", result.EventType)
	}
	if result.CorrelationID != "cmd-123" {
		t.Errorf("expected CorrelationID cmd-123, got %s", result.CorrelationID)
	}
	if !result.Payload.Success {
		t.Error("expected Success true")
	}
	if result.Payload.CommitSHA != "abc123def" {
		t.Errorf("expected CommitSHA abc123def, got %s", result.Payload.CommitSHA)
	}
	if result.Payload.ErrorMessage != "" {
		t.Errorf("expected empty ErrorMessage, got %s", result.Payload.ErrorMessage)
	}
}

func TestCreateBranchResult_Failure(t *testing.T) {
	s := &GitService{}

	cmd := &event.BranchCommand{
		BaseEvent: event.BaseEvent{
			EventID:   "cmd-456",
			EventType: event.BranchCreateRequested,
			Timestamp: time.Now(),
		},
		Payload: event.BranchPayload{
			RepositoryID: "repo-1",
			BranchName:   "feature/test",
		},
	}

	testError := &testErr{msg: "branch already exists"}
	result := s.createBranchResult(cmd, "", testError)

	if result.EventType != event.OperationFailed {
		t.Errorf("expected EventType OPERATION_FAILED, got %s", result.EventType)
	}
	if result.Payload.Success {
		t.Error("expected Success false")
	}
	if result.Payload.ErrorMessage != "branch already exists" {
		t.Errorf("expected ErrorMessage 'branch already exists', got %s", result.Payload.ErrorMessage)
	}
}

func TestCreateBranchDeleteResult_Success(t *testing.T) {
	s := &GitService{}

	cmd := &event.BranchCommand{
		BaseEvent: event.BaseEvent{
			EventID:   "cmd-789",
			EventType: event.BranchDeleteRequested,
			Timestamp: time.Now(),
		},
		Payload: event.BranchPayload{
			RepositoryID: "repo-1",
			BranchName:   "feature/old",
		},
	}

	result := s.createBranchDeleteResult(cmd, nil)

	if result.EventType != event.BranchDeleted {
		t.Errorf("expected EventType BRANCH_DELETED, got %s", result.EventType)
	}
	if !result.Payload.Success {
		t.Error("expected Success true")
	}
}

func TestCreateSyncResult_Success(t *testing.T) {
	s := &GitService{}

	cmd := &event.RepositorySyncCommand{
		BaseEvent: event.BaseEvent{
			EventID:   "sync-001",
			EventType: event.RepositorySyncRequested,
			Timestamp: time.Now(),
		},
		Payload: event.RepositorySyncPayload{
			RepositoryID: "repo-1",
		},
	}

	repoInfo := &client.RepositoryInfo{
		DefaultBranch: "main",
	}
	branches := []string{"main", "develop", "feature/test"}

	result := s.createSyncResult(cmd, repoInfo, branches, nil)

	if result.EventType != event.RepositorySynced {
		t.Errorf("expected EventType REPOSITORY_SYNCED, got %s", result.EventType)
	}
	if !result.Payload.Success {
		t.Error("expected Success true")
	}
	if result.Payload.DefaultBranch != "main" {
		t.Errorf("expected DefaultBranch main, got %s", result.Payload.DefaultBranch)
	}
	if len(result.Payload.Branches) != 3 {
		t.Errorf("expected 3 branches, got %d", len(result.Payload.Branches))
	}
}

func TestCreateSyncResult_Failure(t *testing.T) {
	s := &GitService{}

	cmd := &event.RepositorySyncCommand{
		BaseEvent: event.BaseEvent{
			EventID:   "sync-002",
			EventType: event.RepositorySyncRequested,
			Timestamp: time.Now(),
		},
		Payload: event.RepositorySyncPayload{
			RepositoryID: "repo-1",
		},
	}

	testError := &testErr{msg: "repository not found"}
	result := s.createSyncResult(cmd, nil, nil, testError)

	if result.EventType != event.OperationFailed {
		t.Errorf("expected EventType OPERATION_FAILED, got %s", result.EventType)
	}
	if result.Payload.Success {
		t.Error("expected Success false")
	}
	if result.Payload.ErrorMessage != "repository not found" {
		t.Errorf("expected ErrorMessage 'repository not found', got %s", result.Payload.ErrorMessage)
	}
}

func TestCreatePRResult_Success(t *testing.T) {
	s := &GitService{}

	cmd := &event.PullRequestCommand{
		BaseEvent: event.BaseEvent{
			EventID:   "pr-001",
			EventType: event.PRCreateRequested,
			Timestamp: time.Now(),
		},
		Payload: event.PullRequestPayload{
			RepositoryID: "repo-1",
			Title:        "Test PR",
		},
	}

	prInfo := &client.PullRequestInfo{
		ID:  "pr-123",
		URL: "https://github.com/owner/repo/pull/42",
	}

	result := s.createPRResult(cmd, prInfo, nil)

	if result.EventType != event.PullRequestCreated {
		t.Errorf("expected EventType PR_CREATED, got %s", result.EventType)
	}
	if !result.Payload.Success {
		t.Error("expected Success true")
	}
	if result.Payload.PullRequestID != "pr-123" {
		t.Errorf("expected PullRequestID pr-123, got %s", result.Payload.PullRequestID)
	}
	if result.Payload.PullRequestURL != "https://github.com/owner/repo/pull/42" {
		t.Errorf("unexpected PullRequestURL: %s", result.Payload.PullRequestURL)
	}
}

func TestCreatePRResult_Failure(t *testing.T) {
	s := &GitService{}

	cmd := &event.PullRequestCommand{
		BaseEvent: event.BaseEvent{
			EventID:   "pr-002",
			EventType: event.PRCreateRequested,
			Timestamp: time.Now(),
		},
		Payload: event.PullRequestPayload{
			RepositoryID: "repo-1",
		},
	}

	testError := &testErr{msg: "no commits between branches"}
	result := s.createPRResult(cmd, nil, testError)

	if result.EventType != event.OperationFailed {
		t.Errorf("expected EventType OPERATION_FAILED, got %s", result.EventType)
	}
	if result.Payload.Success {
		t.Error("expected Success false")
	}
}

// Helper error type for testing
type testErr struct {
	msg string
}

func (e *testErr) Error() string {
	return e.msg
}

// Table-driven test example
func TestConnectionTypeHandling(t *testing.T) {
	tests := []struct {
		name           string
		connectionType event.ConnectionType
		isValid        bool
	}{
		{"GitHub", event.GitHub, true},
		{"GitLab", event.GitLab, true},
		{"Unknown", event.ConnectionType("BITBUCKET"), false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			isSupported := tt.connectionType == event.GitHub || tt.connectionType == event.GitLab
			if isSupported != tt.isValid {
				t.Errorf("expected isValid %v for %s, got %v", tt.isValid, tt.connectionType, isSupported)
			}
		})
	}
}
