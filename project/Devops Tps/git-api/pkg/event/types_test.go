package event

import (
	"encoding/json"
	"testing"
	"time"
)

func TestEventTypeParsing(t *testing.T) {
	tests := []struct {
		name      string
		eventType EventType
		expected  string
	}{
		{"BranchCreateRequested", BranchCreateRequested, "BRANCH_CREATE_REQUESTED"},
		{"BranchCreated", BranchCreated, "BRANCH_CREATED"},
		{"RepositorySyncRequested", RepositorySyncRequested, "REPOSITORY_SYNC_REQUESTED"},
		{"PRCreateRequested", PRCreateRequested, "PR_CREATE_REQUESTED"},
		{"OperationFailed", OperationFailed, "OPERATION_FAILED"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if string(tt.eventType) != tt.expected {
				t.Errorf("expected %s, got %s", tt.expected, tt.eventType)
			}
		})
	}
}

func TestConnectionTypeParsing(t *testing.T) {
	tests := []struct {
		name     string
		connType ConnectionType
		expected string
	}{
		{"GitHub", GitHub, "GITHUB"},
		{"GitLab", GitLab, "GITLAB"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if string(tt.connType) != tt.expected {
				t.Errorf("expected %s, got %s", tt.expected, tt.connType)
			}
		})
	}
}

func TestParseEvent_BranchCommand(t *testing.T) {
	// Create test event
	cmd := BranchCommand{
		BaseEvent: BaseEvent{
			EventID:   "test-123",
			EventType: BranchCreateRequested,
			Timestamp: time.Now(),
		},
		Payload: BranchPayload{
			RepositoryID:   "repo-1",
			RepositoryURL:  "https://github.com/test/repo",
			BranchName:     "feature/test",
			BaseBranch:     "main",
			ConnectionType: GitHub,
			AccessToken:    "test-token",
		},
	}

	// Serialize
	data, err := json.Marshal(cmd)
	if err != nil {
		t.Fatalf("failed to marshal: %v", err)
	}

	// Parse
	parsed, err := ParseEvent(data)
	if err != nil {
		t.Fatalf("failed to parse: %v", err)
	}

	// Verify type
	branchCmd, ok := parsed.(*BranchCommand)
	if !ok {
		t.Fatalf("expected *BranchCommand, got %T", parsed)
	}

	// Verify values
	if branchCmd.EventID != "test-123" {
		t.Errorf("expected EventID test-123, got %s", branchCmd.EventID)
	}
	if branchCmd.Payload.BranchName != "feature/test" {
		t.Errorf("expected BranchName feature/test, got %s", branchCmd.Payload.BranchName)
	}
	if branchCmd.Payload.ConnectionType != GitHub {
		t.Errorf("expected ConnectionType GITHUB, got %s", branchCmd.Payload.ConnectionType)
	}
}

func TestParseEvent_RepositorySyncCommand(t *testing.T) {
	cmd := RepositorySyncCommand{
		BaseEvent: BaseEvent{
			EventID:   "sync-456",
			EventType: RepositorySyncRequested,
			Timestamp: time.Now(),
		},
		Payload: RepositorySyncPayload{
			RepositoryID:   "repo-2",
			RepositoryURL:  "https://gitlab.com/test/repo",
			ConnectionType: GitLab,
			AccessToken:    "gitlab-token",
		},
	}

	data, err := json.Marshal(cmd)
	if err != nil {
		t.Fatalf("failed to marshal: %v", err)
	}

	parsed, err := ParseEvent(data)
	if err != nil {
		t.Fatalf("failed to parse: %v", err)
	}

	syncCmd, ok := parsed.(*RepositorySyncCommand)
	if !ok {
		t.Fatalf("expected *RepositorySyncCommand, got %T", parsed)
	}

	if syncCmd.EventID != "sync-456" {
		t.Errorf("expected EventID sync-456, got %s", syncCmd.EventID)
	}
	if syncCmd.Payload.ConnectionType != GitLab {
		t.Errorf("expected ConnectionType GITLAB, got %s", syncCmd.Payload.ConnectionType)
	}
}

func TestParseEvent_PRCommand(t *testing.T) {
	cmd := PullRequestCommand{
		BaseEvent: BaseEvent{
			EventID:   "pr-789",
			EventType: PRCreateRequested,
			Timestamp: time.Now(),
		},
		Payload: PullRequestPayload{
			RepositoryID:   "repo-3",
			RepositoryURL:  "https://github.com/test/repo",
			Title:          "Test PR",
			Description:    "Test description",
			SourceBranch:   "feature/test",
			TargetBranch:   "main",
			ConnectionType: GitHub,
			AccessToken:    "gh-token",
		},
	}

	data, err := json.Marshal(cmd)
	if err != nil {
		t.Fatalf("failed to marshal: %v", err)
	}

	parsed, err := ParseEvent(data)
	if err != nil {
		t.Fatalf("failed to parse: %v", err)
	}

	prCmd, ok := parsed.(*PullRequestCommand)
	if !ok {
		t.Fatalf("expected *PullRequestCommand, got %T", parsed)
	}

	if prCmd.EventID != "pr-789" {
		t.Errorf("expected EventID pr-789, got %s", prCmd.EventID)
	}
	if prCmd.Payload.Title != "Test PR" {
		t.Errorf("expected Title 'Test PR', got %s", prCmd.Payload.Title)
	}
}

func TestParseEvent_InvalidJSON(t *testing.T) {
	invalidJSON := []byte(`{invalid json}`)

	_, err := ParseEvent(invalidJSON)
	if err == nil {
		t.Error("expected error for invalid JSON, got nil")
	}
}

func TestParseEvent_UnknownEventType(t *testing.T) {
	unknownEvent := BaseEvent{
		EventID:   "unknown-1",
		EventType: "UNKNOWN_EVENT_TYPE",
		Timestamp: time.Now(),
	}

	data, _ := json.Marshal(unknownEvent)

	parsed, err := ParseEvent(data)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	// Should return BaseEvent for unknown types
	baseEvent, ok := parsed.(*BaseEvent)
	if !ok {
		t.Fatalf("expected *BaseEvent for unknown type, got %T", parsed)
	}

	if baseEvent.EventType != "UNKNOWN_EVENT_TYPE" {
		t.Errorf("expected UNKNOWN_EVENT_TYPE, got %s", baseEvent.EventType)
	}
}

func TestBranchResult_Serialization(t *testing.T) {
	result := BranchResult{
		BaseEvent: BaseEvent{
			EventID:       "result-1",
			EventType:     BranchCreated,
			Timestamp:     time.Now(),
			CorrelationID: "cmd-1",
		},
		Payload: BranchResultPayload{
			RepositoryID: "repo-1",
			BranchName:   "feature/test",
			CommitSHA:    "abc123",
			Success:      true,
			ErrorMessage: "",
		},
	}

	data, err := json.Marshal(result)
	if err != nil {
		t.Fatalf("failed to marshal: %v", err)
	}

	var decoded BranchResult
	if err := json.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("failed to unmarshal: %v", err)
	}

	if decoded.EventID != "result-1" {
		t.Errorf("expected EventID result-1, got %s", decoded.EventID)
	}
	if decoded.CorrelationID != "cmd-1" {
		t.Errorf("expected CorrelationID cmd-1, got %s", decoded.CorrelationID)
	}
	if !decoded.Payload.Success {
		t.Error("expected Success true, got false")
	}
}
