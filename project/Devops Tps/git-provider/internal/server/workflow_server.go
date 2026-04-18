package server

import (
	"context"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"

	"github.com/runners-high/git-provider/internal/workflow"
	pb "github.com/runners-high/git-provider/pkg/pb/v1"
)

type WorkflowServer struct {
	pb.UnimplementedWorkflowServiceServer
	store *workflow.Store
}

func NewWorkflowServer(store *workflow.Store) *WorkflowServer {
	return &WorkflowServer{store: store}
}

// =============================================================================
// Workflow CRUD
// =============================================================================

func (s *WorkflowServer) CreateWorkflow(ctx context.Context, req *pb.CreateWorkflowRequest) (*pb.CreateWorkflowResponse, error) {
	if req.Name == "" {
		return nil, status.Error(codes.InvalidArgument, "name is required")
	}
	if req.TriggerEvent == "" {
		return nil, status.Error(codes.InvalidArgument, "trigger_event is required")
	}
	if len(req.Steps) == 0 {
		return nil, status.Error(codes.InvalidArgument, "at least one step is required")
	}

	wf := s.store.CreateWorkflow(req.Name, req.TriggerEvent, req.Filter, req.Steps)
	return &pb.CreateWorkflowResponse{Workflow: wf}, nil
}

func (s *WorkflowServer) GetWorkflow(ctx context.Context, req *pb.GetWorkflowRequest) (*pb.GetWorkflowResponse, error) {
	if req.Id == "" {
		return nil, status.Error(codes.InvalidArgument, "id is required")
	}

	wf, err := s.store.GetWorkflow(req.Id)
	if err != nil {
		return nil, status.Errorf(codes.NotFound, "workflow not found: %v", err)
	}
	return &pb.GetWorkflowResponse{Workflow: wf}, nil
}

func (s *WorkflowServer) ListWorkflows(ctx context.Context, req *pb.ListWorkflowsRequest) (*pb.ListWorkflowsResponse, error) {
	workflows := s.store.ListWorkflows(req.Repository)
	return &pb.ListWorkflowsResponse{Workflows: workflows}, nil
}

func (s *WorkflowServer) DeleteWorkflow(ctx context.Context, req *pb.DeleteWorkflowRequest) (*pb.DeleteWorkflowResponse, error) {
	if req.Id == "" {
		return nil, status.Error(codes.InvalidArgument, "id is required")
	}

	if err := s.store.DeleteWorkflow(req.Id); err != nil {
		return nil, status.Errorf(codes.NotFound, "workflow not found: %v", err)
	}
	return &pb.DeleteWorkflowResponse{Success: true}, nil
}

// =============================================================================
// Execution 조회
// =============================================================================

func (s *WorkflowServer) GetExecution(ctx context.Context, req *pb.GetExecutionRequest) (*pb.GetExecutionResponse, error) {
	if req.ExecutionId == "" {
		return nil, status.Error(codes.InvalidArgument, "execution_id is required")
	}

	exec, err := s.store.GetExecution(req.ExecutionId)
	if err != nil {
		return nil, status.Errorf(codes.NotFound, "execution not found: %v", err)
	}
	return &pb.GetExecutionResponse{Execution: exec}, nil
}

func (s *WorkflowServer) ListExecutions(ctx context.Context, req *pb.ListExecutionsRequest) (*pb.ListExecutionsResponse, error) {
	executions := s.store.ListExecutions(req.WorkflowId, req.Limit)
	return &pb.ListExecutionsResponse{Executions: executions}, nil
}
