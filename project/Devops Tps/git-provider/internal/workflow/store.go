package workflow

import (
	"fmt"
	"sync"
	"time"

	pb "github.com/runners-high/git-provider/pkg/pb/v1"
)

// Store is an in-memory store for workflow definitions and executions.
type Store struct {
	mu         sync.RWMutex
	workflows  map[string]*pb.Workflow   // id -> Workflow
	executions map[string]*pb.Execution  // id -> Execution
	nextWfID   int
	nextExecID int
}

func NewStore() *Store {
	return &Store{
		workflows:  make(map[string]*pb.Workflow),
		executions: make(map[string]*pb.Execution),
	}
}

// =============================================================================
// Workflow CRUD
// =============================================================================

func (s *Store) CreateWorkflow(name, triggerEvent string, filter *pb.WorkflowFilter, steps []*pb.WorkflowStep) *pb.Workflow {
	s.mu.Lock()
	defer s.mu.Unlock()

	s.nextWfID++
	id := fmt.Sprintf("wf-%d", s.nextWfID)
	now := time.Now().UTC().Format(time.RFC3339)

	wf := &pb.Workflow{
		Id:           id,
		Name:         name,
		TriggerEvent: triggerEvent,
		Filter:       filter,
		Steps:        steps,
		CreatedAt:    now,
		UpdatedAt:    now,
	}
	s.workflows[id] = wf
	return wf
}

func (s *Store) GetWorkflow(id string) (*pb.Workflow, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	wf, ok := s.workflows[id]
	if !ok {
		return nil, fmt.Errorf("workflow %q not found", id)
	}
	return wf, nil
}

func (s *Store) ListWorkflows(repository string) []*pb.Workflow {
	s.mu.RLock()
	defer s.mu.RUnlock()

	result := make([]*pb.Workflow, 0, len(s.workflows))
	for _, wf := range s.workflows {
		if repository == "" || (wf.Filter != nil && wf.Filter.Repository == repository) {
			result = append(result, wf)
		}
	}
	return result
}

func (s *Store) DeleteWorkflow(id string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	if _, ok := s.workflows[id]; !ok {
		return fmt.Errorf("workflow %q not found", id)
	}
	delete(s.workflows, id)
	return nil
}

// =============================================================================
// Execution management
// =============================================================================

func (s *Store) CreateExecution(workflowID string, wf *pb.Workflow, repository, branch, commitSHA string) *pb.Execution {
	s.mu.Lock()
	defer s.mu.Unlock()

	s.nextExecID++
	id := fmt.Sprintf("exec-%d", s.nextExecID)
	now := time.Now().UTC().Format(time.RFC3339)

	steps := make([]*pb.StepExecution, len(wf.Steps))
	for i, st := range wf.Steps {
		steps[i] = &pb.StepExecution{
			Name:       st.Name,
			Type:       st.Type,
			PipelineId: st.PipelineId,
			Status:     "pending",
		}
	}

	exec := &pb.Execution{
		Id:           id,
		WorkflowId:   workflowID,
		Status:       pb.ExecutionStatus_EXECUTION_STATUS_RUNNING,
		CurrentStep:  0,
		Steps:        steps,
		TriggerEvent: wf.TriggerEvent,
		Repository:   repository,
		Branch:       branch,
		CommitSha:    commitSHA,
		StartedAt:    now,
	}
	s.executions[id] = exec
	return exec
}

func (s *Store) GetExecution(id string) (*pb.Execution, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	exec, ok := s.executions[id]
	if !ok {
		return nil, fmt.Errorf("execution %q not found", id)
	}
	return exec, nil
}

func (s *Store) ListExecutions(workflowID string, limit int32) []*pb.Execution {
	s.mu.RLock()
	defer s.mu.RUnlock()

	if limit <= 0 {
		limit = 20
	}

	var result []*pb.Execution
	for _, exec := range s.executions {
		if workflowID == "" || exec.WorkflowId == workflowID {
			result = append(result, exec)
		}
	}

	if int32(len(result)) > limit {
		result = result[len(result)-int(limit):]
	}
	return result
}

// FindExecutionByPipelineID finds a RUNNING/WAITING execution whose current step references
// the given pipeline. Used to correlate build results back to workflow executions.
func (s *Store) FindExecutionByPipelineID(pipelineID string) *pb.Execution {
	s.mu.RLock()
	defer s.mu.RUnlock()

	for _, exec := range s.executions {
		if exec.Status != pb.ExecutionStatus_EXECUTION_STATUS_RUNNING &&
			exec.Status != pb.ExecutionStatus_EXECUTION_STATUS_WAITING_FOR_STEP {
			continue
		}
		idx := int(exec.CurrentStep)
		if idx < len(exec.Steps) && exec.Steps[idx].PipelineId == pipelineID {
			return exec
		}
	}
	return nil
}

// MatchWorkflows returns all workflows that match the given event type, repository, and branch.
func (s *Store) MatchWorkflows(eventType, repository, branch string) []*pb.Workflow {
	s.mu.RLock()
	defer s.mu.RUnlock()

	var result []*pb.Workflow
	for _, wf := range s.workflows {
		if wf.TriggerEvent != eventType {
			continue
		}
		if wf.Filter == nil {
			result = append(result, wf)
			continue
		}
		if wf.Filter.Repository != "" && wf.Filter.Repository != repository {
			continue
		}
		if wf.Filter.Branch != "" && wf.Filter.Branch != branch {
			continue
		}
		result = append(result, wf)
	}
	return result
}
