package server

import (
	"context"
	"strconv"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"

	pb "github.com/runners-high/git-provider/pkg/pb/v1"
)

// GitServer는 GitService gRPC 서버 구현체입니다.
type GitServer struct {
	pb.UnimplementedGitServiceServer
}

// NewGitServer는 새 GitServer를 생성합니다.
func NewGitServer() *GitServer {
	return &GitServer{}
}

// =============================================================================
// 저장소 관련 RPC 메서드
// =============================================================================

// ListRepositories는 프로바이더의 저장소 목록을 반환합니다.
func (s *GitServer) ListRepositories(ctx context.Context, req *pb.ListRepositoriesRequest) (*pb.ListRepositoriesResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}

	var repos []*pb.Repository
	var err error

	switch config := req.Provider.Config.(type) {
	case *pb.ProviderConfig_Github:
		ghClient, clientErr := createGitHubClient(ctx, config.Github)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create github client: %v", clientErr)
		}
		repos, err = ghClient.ListRepositories(ctx)

	case *pb.ProviderConfig_Gitlab:
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		repos, err = glClient.ListRepositories(ctx)

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		repos, err = bbClient.ListRepositories(ctx)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to list repositories: %v", err)
	}

	return &pb.ListRepositoriesResponse{Repositories: repos}, nil
}

// GetRepository는 특정 저장소의 상세 정보를 반환합니다.
func (s *GitServer) GetRepository(ctx context.Context, req *pb.GetRepositoryRequest) (*pb.GetRepositoryResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}

	var repo *pb.Repository
	var err error

	switch config := req.Provider.Config.(type) {
	case *pb.ProviderConfig_Github:
		if req.Namespace == "" {
			return nil, status.Error(codes.InvalidArgument, "namespace (owner) is required for github")
		}
		ghClient, clientErr := createGitHubClient(ctx, config.Github)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create github client: %v", clientErr)
		}
		repo, err = ghClient.GetRepository(ctx, req.Namespace, req.Repository)

	case *pb.ProviderConfig_Gitlab:
		// GitLab은 namespace/repo 형태로 조회
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		repo, err = glClient.GetRepository(ctx, projectPath)

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		repo, err = bbClient.GetRepository(ctx, req.Repository)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to get repository: %v", err)
	}

	return &pb.GetRepositoryResponse{Repository: repo}, nil
}

// CreateRepository는 새 저장소를 생성합니다.
func (s *GitServer) CreateRepository(ctx context.Context, req *pb.CreateRepositoryRequest) (*pb.CreateRepositoryResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Name == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}

	var repo *pb.Repository
	var err error

	switch config := req.Provider.Config.(type) {
	case *pb.ProviderConfig_Github:
		ghClient, clientErr := createGitHubClient(ctx, config.Github)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create github client: %v", clientErr)
		}
		repo, err = ghClient.CreateRepository(ctx, req.Name, req.Description, req.Private, req.Namespace)

	case *pb.ProviderConfig_Gitlab:
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		namespaceID := 0
		if req.Namespace != "" {
			namespaceID, _ = strconv.Atoi(req.Namespace)
		}
		repo, err = glClient.CreateRepository(ctx, req.Name, req.Description, req.Private, namespaceID)

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		repo, err = bbClient.CreateRepository(ctx, req.Name, req.Description, req.Private)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to create repository: %v", err)
	}

	return &pb.CreateRepositoryResponse{Repository: repo}, nil
}

// DeleteRepository는 저장소를 삭제합니다.
func (s *GitServer) DeleteRepository(ctx context.Context, req *pb.DeleteRepositoryRequest) (*pb.DeleteRepositoryResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}

	var err error

	switch config := req.Provider.Config.(type) {
	case *pb.ProviderConfig_Github:
		if req.Namespace == "" {
			return nil, status.Error(codes.InvalidArgument, "namespace (owner) is required for github")
		}
		ghClient, clientErr := createGitHubClient(ctx, config.Github)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create github client: %v", clientErr)
		}
		err = ghClient.DeleteRepository(ctx, req.Namespace, req.Repository)

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		err = glClient.DeleteRepository(ctx, projectPath)

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		err = bbClient.DeleteRepository(ctx, req.Repository)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to delete repository: %v", err)
	}

	return &pb.DeleteRepositoryResponse{Success: true}, nil
}

// =============================================================================
// 브랜치 관련 RPC 메서드
// =============================================================================

// ListBranches는 저장소의 브랜치 목록을 반환합니다.
func (s *GitServer) ListBranches(ctx context.Context, req *pb.ListBranchesRequest) (*pb.ListBranchesResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}

	var branches []*pb.Branch
	var err error

	switch config := req.Provider.Config.(type) {
	case *pb.ProviderConfig_Github:
		if req.Namespace == "" {
			return nil, status.Error(codes.InvalidArgument, "namespace (owner) is required for github")
		}
		ghClient, clientErr := createGitHubClient(ctx, config.Github)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create github client: %v", clientErr)
		}
		branches, err = ghClient.ListBranches(ctx, req.Namespace, req.Repository)

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		branches, err = glClient.ListBranches(ctx, projectPath)

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		branches, err = bbClient.ListBranches(ctx, req.Repository)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to list branches: %v", err)
	}

	return &pb.ListBranchesResponse{Branches: branches}, nil
}

// GetBranch는 특정 브랜치의 상세 정보를 반환합니다.
func (s *GitServer) GetBranch(ctx context.Context, req *pb.GetBranchRequest) (*pb.GetBranchResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}
	if req.Branch == "" {
		return nil, status.Error(codes.InvalidArgument, "branch name is required")
	}

	var branch *pb.Branch
	var err error

	switch config := req.Provider.Config.(type) {
	case *pb.ProviderConfig_Github:
		if req.Namespace == "" {
			return nil, status.Error(codes.InvalidArgument, "namespace (owner) is required for github")
		}
		ghClient, clientErr := createGitHubClient(ctx, config.Github)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create github client: %v", clientErr)
		}
		branch, err = ghClient.GetBranch(ctx, req.Namespace, req.Repository, req.Branch)

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		branch, err = glClient.GetBranch(ctx, projectPath, req.Branch)

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		branch, err = bbClient.GetBranch(ctx, req.Repository, req.Branch)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to get branch: %v", err)
	}

	return &pb.GetBranchResponse{Branch: branch}, nil
}

// CreateBranch는 새 브랜치를 생성합니다.
func (s *GitServer) CreateBranch(ctx context.Context, req *pb.CreateBranchRequest) (*pb.CreateBranchResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}
	if req.Branch == "" {
		return nil, status.Error(codes.InvalidArgument, "branch name is required")
	}
	if req.Ref == "" {
		return nil, status.Error(codes.InvalidArgument, "ref (source branch or commit) is required")
	}

	var branch *pb.Branch
	var err error

	switch config := req.Provider.Config.(type) {
	case *pb.ProviderConfig_Github:
		if req.Namespace == "" {
			return nil, status.Error(codes.InvalidArgument, "namespace (owner) is required for github")
		}
		ghClient, clientErr := createGitHubClient(ctx, config.Github)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create github client: %v", clientErr)
		}
		branch, err = ghClient.CreateBranch(ctx, req.Namespace, req.Repository, req.Branch, req.Ref)

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		branch, err = glClient.CreateBranch(ctx, projectPath, req.Branch, req.Ref)

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		branch, err = bbClient.CreateBranch(ctx, req.Repository, req.Branch, req.Ref)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to create branch: %v", err)
	}

	return &pb.CreateBranchResponse{Branch: branch}, nil
}

// DeleteBranch는 브랜치를 삭제합니다.
func (s *GitServer) DeleteBranch(ctx context.Context, req *pb.DeleteBranchRequest) (*pb.DeleteBranchResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}
	if req.Branch == "" {
		return nil, status.Error(codes.InvalidArgument, "branch name is required")
	}

	var err error

	switch config := req.Provider.Config.(type) {
	case *pb.ProviderConfig_Github:
		if req.Namespace == "" {
			return nil, status.Error(codes.InvalidArgument, "namespace (owner) is required for github")
		}
		ghClient, clientErr := createGitHubClient(ctx, config.Github)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create github client: %v", clientErr)
		}
		err = ghClient.DeleteBranch(ctx, req.Namespace, req.Repository, req.Branch)

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		err = glClient.DeleteBranch(ctx, projectPath, req.Branch)

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		err = bbClient.DeleteBranch(ctx, req.Repository, req.Branch)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to delete branch: %v", err)
	}

	return &pb.DeleteBranchResponse{Success: true}, nil
}
