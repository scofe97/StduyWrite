package server

import (
	"context"
	"strconv"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"

	"github.com/runners-high/git-provider/internal/client"
	pb "github.com/runners-high/git-provider/pkg/pb/v1"
)

// MergeRequestServer는 MergeRequestService gRPC 서버 구현체입니다.
type MergeRequestServer struct {
	pb.UnimplementedMergeRequestServiceServer
}

// NewMergeRequestServer는 새 MergeRequestServer를 생성합니다.
func NewMergeRequestServer() *MergeRequestServer {
	return &MergeRequestServer{}
}

// =============================================================================
// MergeRequest CRUD RPC 메서드
// =============================================================================

// ListMergeRequests는 MR 목록을 반환합니다.
func (s *MergeRequestServer) ListMergeRequests(ctx context.Context, req *pb.ListMergeRequestsRequest) (*pb.ListMergeRequestsResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}

	var mergeRequests []*client.MergeRequestInfo
	var totalCount int
	var err error

	state := convertMRStateToString(req.State)
	page := int(req.Page)
	perPage := int(req.PerPage)

	switch config := req.Provider.Config.(type) {
	case *pb.ProviderConfig_Github:
		if req.Namespace == "" {
			return nil, status.Error(codes.InvalidArgument, "namespace (owner) is required for github")
		}
		ghClient, clientErr := createGitHubClient(ctx, config.Github)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create github client: %v", clientErr)
		}
		mergeRequests, totalCount, err = ghClient.ListMergeRequests(ctx, req.Namespace, req.Repository, state, page, perPage)

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		mergeRequests, totalCount, err = glClient.ListMergeRequests(ctx, projectPath, state, page, perPage)

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		mergeRequests, totalCount, err = bbClient.ListMergeRequests(ctx, req.Repository, state, page, perPage)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to list merge requests: %v", err)
	}

	return &pb.ListMergeRequestsResponse{
		MergeRequests: convertMergeRequestInfoList(mergeRequests),
		TotalCount:    int32(totalCount),
	}, nil
}

// GetMergeRequest는 MR 상세 정보를 반환합니다.
func (s *MergeRequestServer) GetMergeRequest(ctx context.Context, req *pb.GetMergeRequestRequest) (*pb.GetMergeRequestResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}
	if req.Number == 0 {
		return nil, status.Error(codes.InvalidArgument, "merge request number is required")
	}

	var mergeRequest *client.MergeRequestInfo
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
		mergeRequest, err = ghClient.GetMergeRequest(ctx, req.Namespace, req.Repository, int(req.Number))

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		mergeRequest, err = glClient.GetMergeRequest(ctx, projectPath, int(req.Number))

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		mergeRequest, err = bbClient.GetMergeRequest(ctx, req.Repository, int(req.Number))

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to get merge request: %v", err)
	}

	return &pb.GetMergeRequestResponse{
		MergeRequest: convertMergeRequestInfo(mergeRequest),
	}, nil
}

// CreateMergeRequest는 새 MR을 생성합니다.
func (s *MergeRequestServer) CreateMergeRequest(ctx context.Context, req *pb.CreateMergeRequestRequest) (*pb.CreateMergeRequestResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}
	if req.Title == "" {
		return nil, status.Error(codes.InvalidArgument, "title is required")
	}
	if req.SourceBranch == "" {
		return nil, status.Error(codes.InvalidArgument, "source branch is required")
	}
	if req.TargetBranch == "" {
		return nil, status.Error(codes.InvalidArgument, "target branch is required")
	}

	var mergeRequest *client.MergeRequestInfo
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
		mergeRequest, err = ghClient.CreateMergeRequest(ctx, req.Namespace, req.Repository, req.Title, req.Description, req.SourceBranch, req.TargetBranch, req.Draft)

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		mergeRequest, err = glClient.CreateMergeRequest(ctx, projectPath, req.Title, req.Description, req.SourceBranch, req.TargetBranch, req.Draft)

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		mergeRequest, err = bbClient.CreateMergeRequest(ctx, req.Repository, req.Title, req.Description, req.SourceBranch, req.TargetBranch, req.Draft)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to create merge request: %v", err)
	}

	return &pb.CreateMergeRequestResponse{
		MergeRequest: convertMergeRequestInfo(mergeRequest),
	}, nil
}

// UpdateMergeRequest는 MR을 수정합니다.
func (s *MergeRequestServer) UpdateMergeRequest(ctx context.Context, req *pb.UpdateMergeRequestRequest) (*pb.UpdateMergeRequestResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}
	if req.Number == 0 {
		return nil, status.Error(codes.InvalidArgument, "merge request number is required")
	}

	var mergeRequest *client.MergeRequestInfo
	var err error

	state := convertMRStateToString(req.State)

	switch config := req.Provider.Config.(type) {
	case *pb.ProviderConfig_Github:
		if req.Namespace == "" {
			return nil, status.Error(codes.InvalidArgument, "namespace (owner) is required for github")
		}
		ghClient, clientErr := createGitHubClient(ctx, config.Github)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create github client: %v", clientErr)
		}
		mergeRequest, err = ghClient.UpdateMergeRequest(ctx, req.Namespace, req.Repository, int(req.Number), req.Title, req.Description, state, req.TargetBranch)

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		mergeRequest, err = glClient.UpdateMergeRequest(ctx, projectPath, int(req.Number), req.Title, req.Description, state, req.TargetBranch)

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		// Bitbucket UpdateMergeRequest only supports title and description
		mergeRequest, err = bbClient.UpdateMergeRequest(ctx, req.Repository, int(req.Number), req.Title, req.Description)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to update merge request: %v", err)
	}

	return &pb.UpdateMergeRequestResponse{
		MergeRequest: convertMergeRequestInfo(mergeRequest),
	}, nil
}

// MergeMergeRequest는 MR을 머지합니다.
func (s *MergeRequestServer) MergeMergeRequest(ctx context.Context, req *pb.MergeMergeRequestRequest) (*pb.MergeMergeRequestResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}
	if req.Number == 0 {
		return nil, status.Error(codes.InvalidArgument, "merge request number is required")
	}

	var mergeRequest *client.MergeRequestInfo
	var mergeSHA string
	var err error

	mergeMethod := convertMergeMethodToString(req.MergeMethod)

	switch config := req.Provider.Config.(type) {
	case *pb.ProviderConfig_Github:
		if req.Namespace == "" {
			return nil, status.Error(codes.InvalidArgument, "namespace (owner) is required for github")
		}
		ghClient, clientErr := createGitHubClient(ctx, config.Github)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create github client: %v", clientErr)
		}
		mergeRequest, mergeSHA, err = ghClient.MergeMergeRequest(ctx, req.Namespace, req.Repository, int(req.Number), req.CommitTitle, req.CommitMessage, mergeMethod, req.DeleteSourceBranch)

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		// GitLab: commitTitle + commitMessage 합치기, squash 여부 결정
		commitMsg := req.CommitMessage
		if req.CommitTitle != "" {
			commitMsg = req.CommitTitle + "\n\n" + req.CommitMessage
		}
		squash := mergeMethod == "squash"
		mergeRequest, mergeSHA, err = glClient.MergeMergeRequest(ctx, projectPath, int(req.Number), commitMsg, squash, req.DeleteSourceBranch)

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		// Bitbucket: commitTitle + commitMessage 합치기
		commitMsg := req.CommitMessage
		if req.CommitTitle != "" {
			commitMsg = req.CommitTitle + "\n\n" + req.CommitMessage
		}
		mergeRequest, mergeSHA, err = bbClient.MergeMergeRequest(ctx, req.Repository, int(req.Number), commitMsg, req.DeleteSourceBranch)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to merge merge request: %v", err)
	}

	return &pb.MergeMergeRequestResponse{
		MergeRequest: convertMergeRequestInfo(mergeRequest),
		Sha:          mergeSHA,
	}, nil
}

// GetMergeRequestDiff는 MR의 변경사항을 반환합니다.
func (s *MergeRequestServer) GetMergeRequestDiff(ctx context.Context, req *pb.GetMergeRequestDiffRequest) (*pb.GetMergeRequestDiffResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}
	if req.Number == 0 {
		return nil, status.Error(codes.InvalidArgument, "merge request number is required")
	}

	var diff *client.MergeRequestDiffInfo
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
		diff, err = ghClient.GetMergeRequestDiff(ctx, req.Namespace, req.Repository, int(req.Number))

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		diff, err = glClient.GetMergeRequestDiff(ctx, projectPath, int(req.Number))

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		diff, err = bbClient.GetMergeRequestDiff(ctx, req.Repository, int(req.Number))

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to get merge request diff: %v", err)
	}

	return &pb.GetMergeRequestDiffResponse{
		Diff: convertMergeRequestDiffInfo(diff),
	}, nil
}

// =============================================================================
// Review RPC 메서드
// =============================================================================

// ListReviews는 MR 리뷰 목록을 반환합니다.
func (s *MergeRequestServer) ListReviews(ctx context.Context, req *pb.ListReviewsRequest) (*pb.ListReviewsResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}
	if req.Number == 0 {
		return nil, status.Error(codes.InvalidArgument, "merge request number is required")
	}

	var reviews []*client.ReviewInfo
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
		reviews, err = ghClient.ListReviews(ctx, req.Namespace, req.Repository, int(req.Number))

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		reviews, err = glClient.ListReviews(ctx, projectPath, int(req.Number))

	case *pb.ProviderConfig_Bitbucket:
		// Bitbucket does not have a formal review API
		// Return empty list - approvals are tracked differently in Bitbucket
		reviews = []*client.ReviewInfo{}

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to list reviews: %v", err)
	}

	return &pb.ListReviewsResponse{
		Reviews: convertReviewInfoList(reviews),
	}, nil
}

// SubmitReview는 MR 리뷰를 제출합니다.
func (s *MergeRequestServer) SubmitReview(ctx context.Context, req *pb.SubmitReviewRequest) (*pb.SubmitReviewResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}
	if req.Number == 0 {
		return nil, status.Error(codes.InvalidArgument, "merge request number is required")
	}

	var review *client.ReviewInfo
	var err error

	state := convertReviewStateToString(req.State)

	switch config := req.Provider.Config.(type) {
	case *pb.ProviderConfig_Github:
		if req.Namespace == "" {
			return nil, status.Error(codes.InvalidArgument, "namespace (owner) is required for github")
		}
		ghClient, clientErr := createGitHubClient(ctx, config.Github)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create github client: %v", clientErr)
		}
		review, err = ghClient.SubmitReview(ctx, req.Namespace, req.Repository, int(req.Number), state, req.Body)

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		review, err = glClient.SubmitReview(ctx, projectPath, int(req.Number), state, req.Body)

	case *pb.ProviderConfig_Bitbucket:
		// Bitbucket uses Approve/Unapprove instead of reviews
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		if state == "APPROVED" {
			err = bbClient.Approve(ctx, req.Repository, int(req.Number))
		} else {
			// For other states, add a comment instead
			if req.Body != "" {
				_, err = bbClient.CreateComment(ctx, req.Repository, int(req.Number), req.Body)
			}
		}
		if err == nil {
			review = &client.ReviewInfo{State: state, Body: req.Body}
		}

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to submit review: %v", err)
	}

	return &pb.SubmitReviewResponse{
		Review: convertReviewInfo(review),
	}, nil
}

// =============================================================================
// Comment RPC 메서드
// =============================================================================

// ListComments는 MR 댓글 목록을 반환합니다.
func (s *MergeRequestServer) ListComments(ctx context.Context, req *pb.ListCommentsRequest) (*pb.ListCommentsResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}
	if req.Number == 0 {
		return nil, status.Error(codes.InvalidArgument, "merge request number is required")
	}

	var comments []*client.CommentInfo
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
		comments, err = ghClient.ListComments(ctx, req.Namespace, req.Repository, int(req.Number))

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		comments, err = glClient.ListComments(ctx, projectPath, int(req.Number))

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		comments, err = bbClient.ListComments(ctx, req.Repository, int(req.Number))

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to list comments: %v", err)
	}

	return &pb.ListCommentsResponse{
		Comments: convertCommentInfoList(comments),
	}, nil
}

// CreateComment는 MR 댓글을 생성합니다.
func (s *MergeRequestServer) CreateComment(ctx context.Context, req *pb.CreateCommentRequest) (*pb.CreateCommentResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}
	if req.Number == 0 {
		return nil, status.Error(codes.InvalidArgument, "merge request number is required")
	}
	if req.Body == "" {
		return nil, status.Error(codes.InvalidArgument, "comment body is required")
	}

	var comment *client.CommentInfo
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
		comment, err = ghClient.CreateComment(ctx, req.Namespace, req.Repository, int(req.Number), req.Body, req.Path, int(req.Line), req.CommitId)

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		// GitLab CreateComment: (ctx, projectPath, mrIID, body, path, line)
		comment, err = glClient.CreateComment(ctx, projectPath, int(req.Number), req.Body, req.Path, int(req.Line))

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		// Bitbucket CreateComment: (ctx, repoSlug, prID, body) - 인라인 댓글 미지원
		comment, err = bbClient.CreateComment(ctx, req.Repository, int(req.Number), req.Body)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to create comment: %v", err)
	}

	return &pb.CreateCommentResponse{
		Comment: convertCommentInfo(comment),
	}, nil
}

// UpdateComment는 MR 댓글을 수정합니다.
func (s *MergeRequestServer) UpdateComment(ctx context.Context, req *pb.UpdateCommentRequest) (*pb.UpdateCommentResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}
	if req.CommentId == "" {
		return nil, status.Error(codes.InvalidArgument, "comment id is required")
	}
	if req.Body == "" {
		return nil, status.Error(codes.InvalidArgument, "comment body is required")
	}

	var comment *client.CommentInfo
	var err error

	commentID, parseErr := strconv.ParseInt(req.CommentId, 10, 64)
	if parseErr != nil {
		return nil, status.Error(codes.InvalidArgument, "invalid comment id")
	}

	switch config := req.Provider.Config.(type) {
	case *pb.ProviderConfig_Github:
		if req.Namespace == "" {
			return nil, status.Error(codes.InvalidArgument, "namespace (owner) is required for github")
		}
		ghClient, clientErr := createGitHubClient(ctx, config.Github)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create github client: %v", clientErr)
		}
		comment, err = ghClient.UpdateComment(ctx, req.Namespace, req.Repository, commentID, req.Body)

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		// GitLab UpdateComment: (ctx, projectPath, mrIID, noteID, body)
		comment, err = glClient.UpdateComment(ctx, projectPath, int(req.Number), int(commentID), req.Body)

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		// Bitbucket UpdateComment: (ctx, repoSlug, prID, commentID, body)
		comment, err = bbClient.UpdateComment(ctx, req.Repository, int(req.Number), commentID, req.Body)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to update comment: %v", err)
	}

	return &pb.UpdateCommentResponse{
		Comment: convertCommentInfo(comment),
	}, nil
}

// DeleteComment는 MR 댓글을 삭제합니다.
func (s *MergeRequestServer) DeleteComment(ctx context.Context, req *pb.DeleteCommentRequest) (*pb.DeleteCommentResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}
	if req.CommentId == "" {
		return nil, status.Error(codes.InvalidArgument, "comment id is required")
	}

	var err error

	commentID, parseErr := strconv.ParseInt(req.CommentId, 10, 64)
	if parseErr != nil {
		return nil, status.Error(codes.InvalidArgument, "invalid comment id")
	}

	switch config := req.Provider.Config.(type) {
	case *pb.ProviderConfig_Github:
		if req.Namespace == "" {
			return nil, status.Error(codes.InvalidArgument, "namespace (owner) is required for github")
		}
		ghClient, clientErr := createGitHubClient(ctx, config.Github)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create github client: %v", clientErr)
		}
		err = ghClient.DeleteComment(ctx, req.Namespace, req.Repository, commentID)

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		// GitLab DeleteComment: (ctx, projectPath, mrIID, noteID)
		err = glClient.DeleteComment(ctx, projectPath, int(req.Number), int(commentID))

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		// Bitbucket DeleteComment: (ctx, repoSlug, prID, commentID)
		err = bbClient.DeleteComment(ctx, req.Repository, int(req.Number), commentID)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to delete comment: %v", err)
	}

	return &pb.DeleteCommentResponse{
		Success: true,
	}, nil
}

// =============================================================================
// 변환 헬퍼 함수
// =============================================================================

// convertMRStateToString은 MergeRequestState enum을 문자열로 변환합니다.
func convertMRStateToString(state pb.MergeRequestState) string {
	switch state {
	case pb.MergeRequestState_MERGE_REQUEST_STATE_OPEN:
		return "open"
	case pb.MergeRequestState_MERGE_REQUEST_STATE_CLOSED:
		return "closed"
	case pb.MergeRequestState_MERGE_REQUEST_STATE_MERGED:
		return "merged"
	case pb.MergeRequestState_MERGE_REQUEST_STATE_DRAFT:
		return "draft"
	default:
		return ""
	}
}

// convertStringToMRState는 문자열을 MergeRequestState enum으로 변환합니다.
func convertStringToMRState(state string) pb.MergeRequestState {
	switch state {
	case "open":
		return pb.MergeRequestState_MERGE_REQUEST_STATE_OPEN
	case "closed":
		return pb.MergeRequestState_MERGE_REQUEST_STATE_CLOSED
	case "merged":
		return pb.MergeRequestState_MERGE_REQUEST_STATE_MERGED
	case "draft":
		return pb.MergeRequestState_MERGE_REQUEST_STATE_DRAFT
	default:
		return pb.MergeRequestState_MERGE_REQUEST_STATE_UNSPECIFIED
	}
}

// convertMergeMethodToString은 MergeMethod enum을 문자열로 변환합니다.
func convertMergeMethodToString(method pb.MergeMethod) string {
	switch method {
	case pb.MergeMethod_MERGE_METHOD_MERGE:
		return "merge"
	case pb.MergeMethod_MERGE_METHOD_SQUASH:
		return "squash"
	case pb.MergeMethod_MERGE_METHOD_REBASE:
		return "rebase"
	default:
		return "merge"
	}
}

// convertReviewStateToString은 ReviewState enum을 문자열로 변환합니다.
func convertReviewStateToString(state pb.ReviewState) string {
	switch state {
	case pb.ReviewState_REVIEW_STATE_APPROVED:
		return "APPROVED"
	case pb.ReviewState_REVIEW_STATE_CHANGES_REQUESTED:
		return "CHANGES_REQUESTED"
	case pb.ReviewState_REVIEW_STATE_COMMENTED:
		return "COMMENTED"
	case pb.ReviewState_REVIEW_STATE_PENDING:
		return "PENDING"
	case pb.ReviewState_REVIEW_STATE_DISMISSED:
		return "DISMISSED"
	default:
		return "COMMENTED"
	}
}

// convertStringToReviewState는 문자열을 ReviewState enum으로 변환합니다.
func convertStringToReviewState(state string) pb.ReviewState {
	switch state {
	case "APPROVED", "approved":
		return pb.ReviewState_REVIEW_STATE_APPROVED
	case "CHANGES_REQUESTED", "changes_requested":
		return pb.ReviewState_REVIEW_STATE_CHANGES_REQUESTED
	case "COMMENTED", "commented":
		return pb.ReviewState_REVIEW_STATE_COMMENTED
	case "PENDING", "pending":
		return pb.ReviewState_REVIEW_STATE_PENDING
	case "DISMISSED", "dismissed":
		return pb.ReviewState_REVIEW_STATE_DISMISSED
	default:
		return pb.ReviewState_REVIEW_STATE_UNSPECIFIED
	}
}

// convertMergeRequestInfo는 client.MergeRequestInfo를 pb.MergeRequest로 변환합니다.
func convertMergeRequestInfo(mr *client.MergeRequestInfo) *pb.MergeRequest {
	if mr == nil {
		return nil
	}

	return &pb.MergeRequest{
		Id:           mr.ID,
		Number:       int32(mr.Number),
		Title:        mr.Title,
		Description:  mr.Description,
		State:        convertStringToMRState(mr.State),
		SourceBranch: mr.SourceBranch,
		TargetBranch: mr.TargetBranch,
		Author:       convertUserInfo(mr.Author),
		Assignees:    convertUserInfoList(mr.Assignees),
		Reviewers:    convertUserInfoList(mr.Reviewers),
		Labels:       mr.Labels,
		Url:          mr.URL,
		Draft:        mr.Draft,
		Mergeable:    mr.Mergeable,
		CreatedAt:    mr.CreatedAt,
		UpdatedAt:    mr.UpdatedAt,
		MergedAt:     mr.MergedAt,
		ClosedAt:     mr.ClosedAt,
		MergedBy:     convertUserInfo(mr.MergedBy),
		HeadSha:      mr.HeadSHA,
		BaseSha:      mr.BaseSHA,
	}
}

// convertMergeRequestInfoList는 client.MergeRequestInfo 슬라이스를 pb.MergeRequest 슬라이스로 변환합니다.
func convertMergeRequestInfoList(mrs []*client.MergeRequestInfo) []*pb.MergeRequest {
	result := make([]*pb.MergeRequest, len(mrs))
	for i, mr := range mrs {
		result[i] = convertMergeRequestInfo(mr)
	}
	return result
}

// convertUserInfo는 client.UserInfo를 pb.User로 변환합니다.
func convertUserInfo(user *client.UserInfo) *pb.User {
	if user == nil {
		return nil
	}
	return &pb.User{
		Id:        user.ID,
		Login:     user.Login,
		Name:      user.Name,
		Email:     user.Email,
		AvatarUrl: user.AvatarURL,
	}
}

// convertUserInfoList는 client.UserInfo 슬라이스를 pb.User 슬라이스로 변환합니다.
func convertUserInfoList(users []*client.UserInfo) []*pb.User {
	if users == nil {
		return nil
	}
	result := make([]*pb.User, len(users))
	for i, user := range users {
		result[i] = convertUserInfo(user)
	}
	return result
}

// convertReviewInfo는 client.ReviewInfo를 pb.Review로 변환합니다.
func convertReviewInfo(review *client.ReviewInfo) *pb.Review {
	if review == nil {
		return nil
	}
	return &pb.Review{
		Id:          review.ID,
		User:        convertUserInfo(review.User),
		State:       convertStringToReviewState(review.State),
		Body:        review.Body,
		SubmittedAt: review.SubmittedAt,
	}
}

// convertReviewInfoList는 client.ReviewInfo 슬라이스를 pb.Review 슬라이스로 변환합니다.
func convertReviewInfoList(reviews []*client.ReviewInfo) []*pb.Review {
	result := make([]*pb.Review, len(reviews))
	for i, review := range reviews {
		result[i] = convertReviewInfo(review)
	}
	return result
}

// convertCommentInfo는 client.CommentInfo를 pb.Comment로 변환합니다.
func convertCommentInfo(comment *client.CommentInfo) *pb.Comment {
	if comment == nil {
		return nil
	}
	return &pb.Comment{
		Id:          comment.ID,
		User:        convertUserInfo(comment.User),
		Body:        comment.Body,
		Path:        comment.Path,
		Line:        int32(comment.Line),
		CreatedAt:   comment.CreatedAt,
		UpdatedAt:   comment.UpdatedAt,
		InReplyToId: comment.InReplyToID,
	}
}

// convertCommentInfoList는 client.CommentInfo 슬라이스를 pb.Comment 슬라이스로 변환합니다.
func convertCommentInfoList(comments []*client.CommentInfo) []*pb.Comment {
	result := make([]*pb.Comment, len(comments))
	for i, comment := range comments {
		result[i] = convertCommentInfo(comment)
	}
	return result
}

// convertMergeRequestDiffInfo는 client.MergeRequestDiffInfo를 pb.MergeRequestDiff로 변환합니다.
func convertMergeRequestDiffInfo(diff *client.MergeRequestDiffInfo) *pb.MergeRequestDiff {
	if diff == nil {
		return nil
	}
	return &pb.MergeRequestDiff{
		Files:        convertFileDiffInfoList(diff.Files),
		Additions:    int32(diff.Additions),
		Deletions:    int32(diff.Deletions),
		ChangedFiles: int32(diff.ChangedFiles),
	}
}

// convertFileDiffInfoList는 client.FileDiffInfo 슬라이스를 pb.FileDiff 슬라이스로 변환합니다.
func convertFileDiffInfoList(files []*client.FileDiffInfo) []*pb.FileDiff {
	result := make([]*pb.FileDiff, len(files))
	for i, file := range files {
		result[i] = &pb.FileDiff{
			Filename:         file.Filename,
			Status:           file.Status,
			Additions:        int32(file.Additions),
			Deletions:        int32(file.Deletions),
			Patch:            file.Patch,
			PreviousFilename: file.PreviousFilename,
		}
	}
	return result
}
