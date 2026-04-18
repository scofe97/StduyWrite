package event

import (
	"encoding/json"
	"time"
)

// EventType defines the type of git operation event
type EventType string

const (
	// Command Events (tps-api → git-api)
	BranchCreateRequested      EventType = "BRANCH_CREATE_REQUESTED"
	BranchDeleteRequested      EventType = "BRANCH_DELETE_REQUESTED"
	RepositorySyncRequested    EventType = "REPOSITORY_SYNC_REQUESTED"
	PullRequestCreateRequested EventType = "PR_CREATE_REQUESTED"

	// Result Events (git-api → tps-api)
	BranchCreated      EventType = "BRANCH_CREATED"
	BranchDeleted      EventType = "BRANCH_DELETED"
	RepositorySynced   EventType = "REPOSITORY_SYNCED"
	PullRequestCreated EventType = "PR_CREATED"
	OperationFailed    EventType = "OPERATION_FAILED"
)

// ConnectionType defines the git provider type
type ConnectionType string

const (
	GitHub ConnectionType = "GITHUB"
	GitLab ConnectionType = "GITLAB"
)

// BaseEvent contains common event fields
type BaseEvent struct {
	EventID       string    `json:"eventId"`
	EventType     EventType `json:"eventType"`
	Timestamp     time.Time `json:"timestamp"`
	CorrelationID string    `json:"correlationId"`
}

// BranchCommand represents a branch operation command
type BranchCommand struct {
	BaseEvent
	Payload BranchCommandPayload `json:"payload"`
}

type BranchCommandPayload struct {
	ConnectionID   string         `json:"connectionId"`
	ConnectionType ConnectionType `json:"connectionType"`
	RepositoryURL  string         `json:"repositoryUrl"`
	RepositoryID   string         `json:"repositoryId"`
	BranchName     string         `json:"branchName"`
	BaseBranch     string         `json:"baseBranch,omitempty"`
	AccessToken    string         `json:"accessToken"`
}

// BranchResult represents a branch operation result
type BranchResult struct {
	BaseEvent
	Payload BranchResultPayload `json:"payload"`
}

type BranchResultPayload struct {
	RepositoryID string `json:"repositoryId"`
	BranchName   string `json:"branchName"`
	BranchID     string `json:"branchId,omitempty"`
	CommitSHA    string `json:"commitSha,omitempty"`
	Success      bool   `json:"success"`
	ErrorMessage string `json:"errorMessage,omitempty"`
}

// RepositorySyncCommand represents a repository sync command
type RepositorySyncCommand struct {
	BaseEvent
	Payload RepositorySyncPayload `json:"payload"`
}

type RepositorySyncPayload struct {
	ConnectionID   string         `json:"connectionId"`
	ConnectionType ConnectionType `json:"connectionType"`
	RepositoryURL  string         `json:"repositoryUrl"`
	RepositoryID   string         `json:"repositoryId"`
	AccessToken    string         `json:"accessToken"`
}

// RepositorySyncResult represents a repository sync result
type RepositorySyncResult struct {
	BaseEvent
	Payload RepositorySyncResultPayload `json:"payload"`
}

type RepositorySyncResultPayload struct {
	RepositoryID  string   `json:"repositoryId"`
	DefaultBranch string   `json:"defaultBranch"`
	Branches      []string `json:"branches"`
	LastCommitSHA string   `json:"lastCommitSha"`
	Success       bool     `json:"success"`
	ErrorMessage  string   `json:"errorMessage,omitempty"`
}

// PullRequestCommand represents a PR/MR creation command
type PullRequestCommand struct {
	BaseEvent
	Payload PullRequestPayload `json:"payload"`
}

type PullRequestPayload struct {
	ConnectionID   string         `json:"connectionId"`
	ConnectionType ConnectionType `json:"connectionType"`
	RepositoryURL  string         `json:"repositoryUrl"`
	RepositoryID   string         `json:"repositoryId"`
	SourceBranch   string         `json:"sourceBranch"`
	TargetBranch   string         `json:"targetBranch"`
	Title          string         `json:"title"`
	Description    string         `json:"description"`
	AccessToken    string         `json:"accessToken"`
}

// PullRequestResult represents a PR/MR creation result
type PullRequestResult struct {
	BaseEvent
	Payload PullRequestResultPayload `json:"payload"`
}

type PullRequestResultPayload struct {
	RepositoryID   string `json:"repositoryId"`
	PullRequestID  string `json:"pullRequestId"`
	PullRequestURL string `json:"pullRequestUrl"`
	Success        bool   `json:"success"`
	ErrorMessage   string `json:"errorMessage,omitempty"`
}

// OperationError represents a failed operation event
type OperationError struct {
	BaseEvent
	Payload OperationErrorPayload `json:"payload"`
}

type OperationErrorPayload struct {
	OriginalEventID   string `json:"originalEventId"`
	OriginalEventType string `json:"originalEventType"`
	ErrorCode         string `json:"errorCode"`
	ErrorMessage      string `json:"errorMessage"`
}

// ParseEvent parses a JSON message into the appropriate event type
func ParseEvent(data []byte) (interface{}, error) {
	var base BaseEvent
	if err := json.Unmarshal(data, &base); err != nil {
		return nil, err
	}

	switch base.EventType {
	case BranchCreateRequested, BranchDeleteRequested:
		var cmd BranchCommand
		if err := json.Unmarshal(data, &cmd); err != nil {
			return nil, err
		}
		return &cmd, nil

	case RepositorySyncRequested:
		var cmd RepositorySyncCommand
		if err := json.Unmarshal(data, &cmd); err != nil {
			return nil, err
		}
		return &cmd, nil

	case PullRequestCreateRequested:
		var cmd PullRequestCommand
		if err := json.Unmarshal(data, &cmd); err != nil {
			return nil, err
		}
		return &cmd, nil

	default:
		return &base, nil
	}
}
