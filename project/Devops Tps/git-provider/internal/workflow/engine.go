package workflow

import (
	"context"
	"log"
	"sync"
	"time"

	"github.com/runners-high/git-provider/internal/kafka"
	pb "github.com/runners-high/git-provider/pkg/pb/v1"
)

// Engine consumes git.events and cicd.events to orchestrate workflows.
type Engine struct {
	mu       sync.Mutex
	store    *Store
	producer *kafka.EventProducer
}

func NewEngine(store *Store, producer *kafka.EventProducer) *Engine {
	return &Engine{
		store:    store,
		producer: producer,
	}
}

// MakeGitEventHandler returns a handler for git.events (or git-events) topic.
// When a git event arrives, it matches against registered workflows and starts executions.
func (e *Engine) MakeGitEventHandler() kafka.MessageHandler {
	return func(ctx context.Context, topic string, key, value []byte) error {
		event, err := kafka.ParseEvent[kafka.GitEvent](value)
		if err != nil {
			return err
		}

		workflows := e.store.MatchWorkflows(event.EventType, event.Repository, event.Branch)
		if len(workflows) == 0 {
			return nil
		}

		for _, wf := range workflows {
			log.Printf("workflow matched: %s (%s) for event %s repo=%s branch=%s",
				wf.Name, wf.Id, event.EventType, event.Repository, event.Branch)

			exec := e.store.CreateExecution(wf.Id, wf, event.Repository, event.Branch, event.CommitSHA)
			log.Printf("execution started: %s for workflow %s", exec.Id, wf.Id)

			e.executeNextStep(ctx, exec)
		}

		return nil
	}
}

// MakeCICDEventHandler returns a handler for cicd.events topic.
// When a build completes, it advances the workflow execution to the next step.
func (e *Engine) MakeCICDEventHandler() kafka.MessageHandler {
	return func(ctx context.Context, topic string, key, value []byte) error {
		event, err := kafka.ParseEvent[kafka.BuildCompletedEvent](value)
		if err != nil {
			return err
		}

		if event.Type != "build_completed" {
			return nil
		}

		// Find execution by execution_id (if provided) or by pipeline_id
		var exec *pb.Execution
		if event.ExecutionID != "" {
			exec, _ = e.store.GetExecution(event.ExecutionID)
		}
		if exec == nil {
			exec = e.store.FindExecutionByPipelineID(event.PipelineID)
		}
		if exec == nil {
			return nil // not a workflow-triggered build
		}

		log.Printf("build result for execution %s: pipeline=%s status=%s",
			exec.Id, event.PipelineID, event.Status)

		e.handleBuildResult(ctx, exec, event)
		return nil
	}
}

func (e *Engine) executeNextStep(ctx context.Context, exec *pb.Execution) {
	e.mu.Lock()
	defer e.mu.Unlock()

	e.executeNextStepLocked(ctx, exec)
}

// executeNextStepLocked advances the execution to the next step.
// Must be called with e.mu held.
func (e *Engine) executeNextStepLocked(ctx context.Context, exec *pb.Execution) {
	idx := int(exec.CurrentStep)
	if idx >= len(exec.Steps) {
		e.completeExecutionLocked(ctx, exec)
		return
	}

	step := exec.Steps[idx]
	step.Status = "running"
	step.StartedAt = time.Now().UTC().Format(time.RFC3339)

	switch step.Type {
	case "cicd_build":
		exec.Status = pb.ExecutionStatus_EXECUTION_STATUS_WAITING_FOR_STEP

		cmd := kafka.TriggerBuildCommand{
			Type:        "trigger_build",
			PipelineID:  step.PipelineId,
			Branch:      exec.Branch,
			CommitSHA:   exec.CommitSha,
			ExecutionID: exec.Id,
			Timestamp:   time.Now().UTC().Format(time.RFC3339),
		}
		if err := e.producer.Publish(ctx, kafka.TopicCICDCommands, step.PipelineId, cmd); err != nil {
			log.Printf("failed to publish cicd command: %v", err)
			step.Status = "failure"
			e.failExecutionLocked(ctx, exec)
		}

	default:
		log.Printf("unknown step type %q in execution %s", step.Type, exec.Id)
		step.Status = "failure"
		e.failExecutionLocked(ctx, exec)
	}
}

func (e *Engine) handleBuildResult(ctx context.Context, exec *pb.Execution, event kafka.BuildCompletedEvent) {
	e.mu.Lock()
	defer e.mu.Unlock()

	idx := int(exec.CurrentStep)
	if idx >= len(exec.Steps) {
		return
	}

	step := exec.Steps[idx]
	step.FinishedAt = time.Now().UTC().Format(time.RFC3339)

	if event.Status == "SUCCESS" {
		step.Status = "success"
		exec.CurrentStep++
		e.executeNextStepLocked(ctx, exec)
	} else {
		step.Status = "failure"
		e.failExecutionLocked(ctx, exec)
	}
}

func (e *Engine) completeExecution(ctx context.Context, exec *pb.Execution) {
	e.mu.Lock()
	defer e.mu.Unlock()

	e.completeExecutionLocked(ctx, exec)
}

// completeExecutionLocked marks the execution as completed and publishes an event.
// Must be called with e.mu held.
func (e *Engine) completeExecutionLocked(ctx context.Context, exec *pb.Execution) {
	exec.Status = pb.ExecutionStatus_EXECUTION_STATUS_COMPLETED
	exec.FinishedAt = time.Now().UTC().Format(time.RFC3339)

	log.Printf("workflow execution completed: %s", exec.Id)

	wfEvent := kafka.WorkflowEvent{
		Type:        "workflow_completed",
		ExecutionID: exec.Id,
		WorkflowID:  exec.WorkflowId,
		Status:      "COMPLETED",
		Timestamp:   time.Now().UTC().Format(time.RFC3339),
	}
	if err := e.producer.Publish(ctx, kafka.TopicWorkflowEvents, exec.WorkflowId, wfEvent); err != nil {
		log.Printf("failed to publish workflow completed event: %v", err)
	}
}

func (e *Engine) failExecution(ctx context.Context, exec *pb.Execution) {
	e.mu.Lock()
	defer e.mu.Unlock()

	e.failExecutionLocked(ctx, exec)
}

// failExecutionLocked marks the execution as failed and publishes an event.
// Must be called with e.mu held.
func (e *Engine) failExecutionLocked(ctx context.Context, exec *pb.Execution) {
	exec.Status = pb.ExecutionStatus_EXECUTION_STATUS_FAILED
	exec.FinishedAt = time.Now().UTC().Format(time.RFC3339)

	log.Printf("workflow execution failed: %s", exec.Id)

	wfEvent := kafka.WorkflowEvent{
		Type:        "workflow_failed",
		ExecutionID: exec.Id,
		WorkflowID:  exec.WorkflowId,
		Status:      "FAILED",
		Timestamp:   time.Now().UTC().Format(time.RFC3339),
	}
	if err := e.producer.Publish(ctx, kafka.TopicWorkflowEvents, exec.WorkflowId, wfEvent); err != nil {
		log.Printf("failed to publish workflow failed event: %v", err)
	}
}
