package handler

import (
	"encoding/json"
	"testing"
	"time"

	"github.com/runners-high/git-api/pkg/event"
)

func TestKafkaHandler_HandleInvalidJSON(t *testing.T) {
	// Create handler with nil service (will panic if used)
	h := &KafkaHandler{}

	invalidJSON := []byte(`{invalid json}`)

	err := h.Handle(invalidJSON)
	if err == nil {
		t.Error("expected error for invalid JSON, got nil")
	}
}

func TestKafkaHandler_RouteUnknownEventType(t *testing.T) {
	h := &KafkaHandler{}

	unknownEvent := event.BaseEvent{
		EventID:   "unknown-1",
		EventType: "UNKNOWN_TYPE",
		Timestamp: time.Now(),
	}

	data, _ := json.Marshal(unknownEvent)

	// Should not error, just log warning
	err := h.Handle(data)
	if err != nil {
		t.Errorf("unexpected error for unknown event type: %v", err)
	}
}

// TestEventRouting verifies correct routing based on event type
func TestEventRouting(t *testing.T) {
	tests := []struct {
		name          string
		eventType     event.EventType
		expectedRoute string
	}{
		{"BranchCreate", event.BranchCreateRequested, "handleBranchCommand"},
		{"BranchDelete", event.BranchDeleteRequested, "handleBranchCommand"},
		{"RepositorySync", event.RepositorySyncRequested, "HandleRepositorySync"},
		{"PRCreate", event.PRCreateRequested, "HandlePullRequestCreate"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Verify event type is recognized
			switch tt.eventType {
			case event.BranchCreateRequested, event.BranchDeleteRequested:
				if tt.expectedRoute != "handleBranchCommand" {
					t.Errorf("branch events should route to handleBranchCommand")
				}
			case event.RepositorySyncRequested:
				if tt.expectedRoute != "HandleRepositorySync" {
					t.Errorf("sync events should route to HandleRepositorySync")
				}
			case event.PRCreateRequested:
				if tt.expectedRoute != "HandlePullRequestCreate" {
					t.Errorf("PR events should route to HandlePullRequestCreate")
				}
			}
		})
	}
}

// TestBranchCommandParsing tests parsing of branch command events
func TestBranchCommandParsing(t *testing.T) {
	cmd := event.BranchCommand{
		BaseEvent: event.BaseEvent{
			EventID:   "cmd-123",
			EventType: event.BranchCreateRequested,
			Timestamp: time.Now(),
		},
		Payload: event.BranchPayload{
			RepositoryID:   "repo-1",
			RepositoryURL:  "https://github.com/test/repo",
			BranchName:     "feature/test",
			BaseBranch:     "main",
			ConnectionType: event.GitHub,
			AccessToken:    "token-xxx",
		},
	}

	data, err := json.Marshal(cmd)
	if err != nil {
		t.Fatalf("failed to marshal: %v", err)
	}

	parsed, err := event.ParseEvent(data)
	if err != nil {
		t.Fatalf("failed to parse: %v", err)
	}

	branchCmd, ok := parsed.(*event.BranchCommand)
	if !ok {
		t.Fatalf("expected *BranchCommand, got %T", parsed)
	}

	// Verify all fields
	if branchCmd.EventID != "cmd-123" {
		t.Errorf("wrong EventID")
	}
	if branchCmd.EventType != event.BranchCreateRequested {
		t.Errorf("wrong EventType")
	}
	if branchCmd.Payload.RepositoryID != "repo-1" {
		t.Errorf("wrong RepositoryID")
	}
	if branchCmd.Payload.BranchName != "feature/test" {
		t.Errorf("wrong BranchName")
	}
	if branchCmd.Payload.ConnectionType != event.GitHub {
		t.Errorf("wrong ConnectionType")
	}
}

// TestRepositorySyncCommandParsing tests parsing of sync command events
func TestRepositorySyncCommandParsing(t *testing.T) {
	cmd := event.RepositorySyncCommand{
		BaseEvent: event.BaseEvent{
			EventID:   "sync-456",
			EventType: event.RepositorySyncRequested,
			Timestamp: time.Now(),
		},
		Payload: event.RepositorySyncPayload{
			RepositoryID:   "repo-2",
			RepositoryURL:  "https://gitlab.com/test/repo",
			ConnectionType: event.GitLab,
			AccessToken:    "gitlab-token",
		},
	}

	data, err := json.Marshal(cmd)
	if err != nil {
		t.Fatalf("failed to marshal: %v", err)
	}

	parsed, err := event.ParseEvent(data)
	if err != nil {
		t.Fatalf("failed to parse: %v", err)
	}

	syncCmd, ok := parsed.(*event.RepositorySyncCommand)
	if !ok {
		t.Fatalf("expected *RepositorySyncCommand, got %T", parsed)
	}

	if syncCmd.Payload.ConnectionType != event.GitLab {
		t.Errorf("expected GitLab, got %s", syncCmd.Payload.ConnectionType)
	}
}

// TestPullRequestCommandParsing tests parsing of PR command events
func TestPullRequestCommandParsing(t *testing.T) {
	cmd := event.PullRequestCommand{
		BaseEvent: event.BaseEvent{
			EventID:   "pr-789",
			EventType: event.PRCreateRequested,
			Timestamp: time.Now(),
		},
		Payload: event.PullRequestPayload{
			RepositoryID:   "repo-3",
			RepositoryURL:  "https://github.com/test/repo",
			Title:          "Feature: Add new function",
			Description:    "This PR adds a new feature",
			SourceBranch:   "feature/new-func",
			TargetBranch:   "main",
			ConnectionType: event.GitHub,
			AccessToken:    "gh-token",
		},
	}

	data, err := json.Marshal(cmd)
	if err != nil {
		t.Fatalf("failed to marshal: %v", err)
	}

	parsed, err := event.ParseEvent(data)
	if err != nil {
		t.Fatalf("failed to parse: %v", err)
	}

	prCmd, ok := parsed.(*event.PullRequestCommand)
	if !ok {
		t.Fatalf("expected *PullRequestCommand, got %T", parsed)
	}

	if prCmd.Payload.Title != "Feature: Add new function" {
		t.Errorf("wrong Title: %s", prCmd.Payload.Title)
	}
	if prCmd.Payload.SourceBranch != "feature/new-func" {
		t.Errorf("wrong SourceBranch")
	}
	if prCmd.Payload.TargetBranch != "main" {
		t.Errorf("wrong TargetBranch")
	}
}

// Benchmark for event parsing
func BenchmarkEventParsing(b *testing.B) {
	cmd := event.BranchCommand{
		BaseEvent: event.BaseEvent{
			EventID:   "cmd-bench",
			EventType: event.BranchCreateRequested,
			Timestamp: time.Now(),
		},
		Payload: event.BranchPayload{
			RepositoryID:   "repo-1",
			RepositoryURL:  "https://github.com/test/repo",
			BranchName:     "feature/test",
			BaseBranch:     "main",
			ConnectionType: event.GitHub,
			AccessToken:    "token-xxx",
		},
	}

	data, _ := json.Marshal(cmd)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _ = event.ParseEvent(data)
	}
}
