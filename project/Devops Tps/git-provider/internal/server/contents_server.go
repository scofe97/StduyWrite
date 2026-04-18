package server

import (
	"context"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"

	pb "github.com/runners-high/git-provider/pkg/pb/v1"
)

// ContentsServer는 ContentsService gRPC 서버 구현체입니다.
type ContentsServer struct {
	pb.UnimplementedContentsServiceServer
}

// NewContentsServer는 새 ContentsServer를 생성합니다.
func NewContentsServer() *ContentsServer {
	return &ContentsServer{}
}

// =============================================================================
// 트리 관련 RPC 메서드
// =============================================================================

// GetTree는 저장소의 파일 트리를 반환합니다.
func (s *ContentsServer) GetTree(ctx context.Context, req *pb.GetTreeRequest) (*pb.GetTreeResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}

	var entries []*pb.TreeEntry
	var truncated string
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
		entries, truncated, err = ghClient.GetTree(ctx, req.Namespace, req.Repository, req.Ref, req.Recursive)

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		entries, err = glClient.GetTree(ctx, projectPath, req.Ref, req.Recursive)

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		entries, err = bbClient.GetTree(ctx, req.Repository, req.Ref, req.Recursive)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to get tree: %v", err)
	}

	return &pb.GetTreeResponse{
		Entries:   entries,
		Truncated: truncated,
	}, nil
}

// =============================================================================
// 콘텐츠 관련 RPC 메서드
// =============================================================================

// GetContents는 특정 경로의 파일/디렉토리 내용을 반환합니다.
func (s *ContentsServer) GetContents(ctx context.Context, req *pb.GetContentsRequest) (*pb.GetContentsResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}

	var content *pb.ContentEntry
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
		content, err = ghClient.GetContents(ctx, req.Namespace, req.Repository, req.Path, req.Ref)

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		content, err = glClient.GetContents(ctx, projectPath, req.Path, req.Ref)

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		content, err = bbClient.GetContents(ctx, req.Repository, req.Path, req.Ref)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to get contents: %v", err)
	}

	return &pb.GetContentsResponse{Content: content}, nil
}

// =============================================================================
// README 관련 RPC 메서드
// =============================================================================

// GetReadme는 저장소의 README 파일을 반환합니다.
func (s *ContentsServer) GetReadme(ctx context.Context, req *pb.GetReadmeRequest) (*pb.GetReadmeResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}

	var content *pb.ContentEntry
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
		content, err = ghClient.GetReadme(ctx, req.Namespace, req.Repository, req.Ref)

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		content, err = glClient.GetReadme(ctx, projectPath, req.Ref)

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		content, err = bbClient.GetReadme(ctx, req.Repository, req.Ref)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.NotFound, "failed to get readme: %v", err)
	}

	return &pb.GetReadmeResponse{
		Name:    content.Name,
		Path:    content.Path,
		Content: content.Content,
	}, nil
}
