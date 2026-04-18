package kafka

const (
	TopicGitEvents   = "git-events"
	TopicCICDResults = "cicd-results"

	// Workflow topics
	TopicCICDCommands  = "cicd.commands"
	TopicCICDEvents    = "cicd.events"
	TopicWorkflowEvents = "workflow.events"
)

type GitEvent struct {
	EventType  string `json:"event_type"`  // "push", "branch_created", "mr_merged"
	Repository string `json:"repository"`  // namespace/repo
	Branch     string `json:"branch"`
	CommitSHA  string `json:"commit_sha"`
	Author     string `json:"author"`
	Timestamp  string `json:"timestamp"` // ISO 8601
}

type BuildResultEvent struct {
	PipelineID      string `json:"pipeline_id"`
	BuildNumber     int    `json:"build_number"`
	Status          string `json:"status"`           // "SUCCESS", "FAILURE", "ABORTED"
	DurationSeconds int    `json:"duration_seconds"`
	URL             string `json:"url"`
	Timestamp       string `json:"timestamp"`
}

// =============================================================================
// Workflow Command/Event types
// =============================================================================

// TriggerBuildCommand is published to cicd.commands by the workflow engine.
type TriggerBuildCommand struct {
	Type        string `json:"type"`         // "trigger_build"
	PipelineID  string `json:"pipeline_id"`
	Branch      string `json:"branch"`
	CommitSHA   string `json:"commit_sha"`
	ExecutionID string `json:"execution_id"` // workflow execution reference
	Timestamp   string `json:"timestamp"`
}

// BuildCompletedEvent is published to cicd.events after Jenkins build completes.
type BuildCompletedEvent struct {
	Type            string `json:"type"`         // "build_completed"
	PipelineID      string `json:"pipeline_id"`
	BuildNumber     int    `json:"build_number"`
	Status          string `json:"status"`       // "SUCCESS", "FAILURE", "ABORTED"
	ExecutionID     string `json:"execution_id"`
	DurationSeconds int    `json:"duration_seconds"`
	URL             string `json:"url"`
	Timestamp       string `json:"timestamp"`
}

// WorkflowEvent is published to workflow.events on workflow state changes.
type WorkflowEvent struct {
	Type        string `json:"type"`         // "workflow_completed", "workflow_failed"
	ExecutionID string `json:"execution_id"`
	WorkflowID  string `json:"workflow_id"`
	Status      string `json:"status"`
	Timestamp   string `json:"timestamp"`
}
