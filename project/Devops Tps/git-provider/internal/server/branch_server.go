package server

import (
	"context"
	"fmt"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"

	"github.com/runners-high/git-provider/internal/client"
	pb "github.com/runners-high/git-provider/pkg/pb/v1"
)

// BranchServer는 BranchService gRPC 서버 구현체입니다.
type BranchServer struct {
	pb.UnimplementedBranchServiceServer
}

// NewBranchServer는 새 BranchServer를 생성합니다.
func NewBranchServer() *BranchServer {
	return &BranchServer{}
}

// =============================================================================
// 브랜치 비교 RPC 메서드
// =============================================================================

// CompareBranches는 두 브랜치를 비교합니다.
func (s *BranchServer) CompareBranches(ctx context.Context, req *pb.CompareBranchesRequest) (*pb.CompareBranchesResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}
	if req.Base == "" {
		return nil, status.Error(codes.InvalidArgument, "base branch is required")
	}
	if req.Compare == "" {
		return nil, status.Error(codes.InvalidArgument, "compare branch is required")
	}

	var comparison *client.BranchComparison
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
		comparison, err = ghClient.CompareBranches(ctx, req.Namespace, req.Repository, req.Base, req.Compare)

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		comparison, err = glClient.CompareBranches(ctx, projectPath, req.Base, req.Compare)

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		comparison, err = bbClient.CompareBranches(ctx, req.Repository, req.Base, req.Compare)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to compare branches: %v", err)
	}

	return &pb.CompareBranchesResponse{
		Comparison: convertBranchComparison(comparison),
		DiffStat: &pb.DiffStat{
			FilesChanged: int32(comparison.FilesChanged),
			Additions:    int32(comparison.Additions),
			Deletions:    int32(comparison.Deletions),
		},
	}, nil
}

// ListCommitsDiff는 두 브랜치 간 커밋 차이를 조회합니다.
func (s *BranchServer) ListCommitsDiff(ctx context.Context, req *pb.ListCommitsDiffRequest) (*pb.ListCommitsDiffResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}
	if req.Base == "" {
		return nil, status.Error(codes.InvalidArgument, "base branch is required")
	}
	if req.Compare == "" {
		return nil, status.Error(codes.InvalidArgument, "compare branch is required")
	}

	var commits []*client.CommitInfo
	var totalCount int
	var err error

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
		commits, totalCount, err = ghClient.ListCommitsDiff(ctx, req.Namespace, req.Repository, req.Base, req.Compare, page, perPage)

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		commits, totalCount, err = glClient.ListCommitsDiff(ctx, projectPath, req.Base, req.Compare, page, perPage)

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		commits, totalCount, err = bbClient.ListCommitsDiff(ctx, req.Repository, req.Base, req.Compare, page, perPage)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to list commits diff: %v", err)
	}

	return &pb.ListCommitsDiffResponse{
		Commits:    convertCommitInfoList(commits),
		TotalCount: int32(totalCount),
	}, nil
}

// =============================================================================
// 머지된 브랜치 관련 RPC 메서드
// =============================================================================

// ListMergedBranches는 기준 브랜치에 머지된 브랜치 목록을 반환합니다.
func (s *BranchServer) ListMergedBranches(ctx context.Context, req *pb.ListMergedBranchesRequest) (*pb.ListMergedBranchesResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}

	base := req.Base
	if base == "" {
		base = "main"
	}

	var branches []*client.MergedBranchInfo
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
		branches, err = ghClient.ListMergedBranches(ctx, req.Namespace, req.Repository, base)

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		branches, err = glClient.ListMergedBranches(ctx, projectPath, base)

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		branches, err = bbClient.ListMergedBranches(ctx, req.Repository, base)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to list merged branches: %v", err)
	}

	return &pb.ListMergedBranchesResponse{
		Branches: convertMergedBranchInfoList(branches),
	}, nil
}

// =============================================================================
// Stale 브랜치 관련 RPC 메서드
// =============================================================================

// ListStaleBranches는 오래된 브랜치 목록을 반환합니다.
func (s *BranchServer) ListStaleBranches(ctx context.Context, req *pb.ListStaleBranchesRequest) (*pb.ListStaleBranchesResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}

	staleDays := int(req.StaleDays)
	if staleDays == 0 {
		staleDays = 30
	}

	var branches []*client.StaleBranchInfo
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
		branches, err = ghClient.ListStaleBranches(ctx, req.Namespace, req.Repository, staleDays)

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}
		branches, err = glClient.ListStaleBranches(ctx, projectPath, staleDays)

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}
		branches, err = bbClient.ListStaleBranches(ctx, req.Repository, staleDays)

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to list stale branches: %v", err)
	}

	return &pb.ListStaleBranchesResponse{
		Branches: convertStaleBranchInfoList(branches),
	}, nil
}

// =============================================================================
// 브랜치 정리 RPC 메서드
// =============================================================================

// CleanupBranches는 머지된 브랜치와 오래된 브랜치를 정리합니다.
func (s *BranchServer) CleanupBranches(ctx context.Context, req *pb.CleanupBranchesRequest) (*pb.CleanupBranchesResponse, error) {
	if req.Provider == nil {
		return nil, status.Error(codes.InvalidArgument, "provider config is required")
	}
	if req.Repository == "" {
		return nil, status.Error(codes.InvalidArgument, "repository name is required")
	}

	result := &pb.CleanupResult{
		DryRun:  req.DryRun,
		Deleted: []string{},
		Skipped: []string{},
		Failed:  []string{},
	}

	staleDays := int(req.StaleDays)
	if staleDays == 0 {
		staleDays = 30
	}

	// 정리 대상 브랜치 수집
	var branchesToDelete []string

	switch config := req.Provider.Config.(type) {
	case *pb.ProviderConfig_Github:
		if req.Namespace == "" {
			return nil, status.Error(codes.InvalidArgument, "namespace (owner) is required for github")
		}
		ghClient, clientErr := createGitHubClient(ctx, config.Github)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create github client: %v", clientErr)
		}

		// 머지된 브랜치 수집
		if req.IncludeMerged {
			mergedBranches, err := ghClient.ListMergedBranches(ctx, req.Namespace, req.Repository, "main")
			if err == nil {
				for _, b := range mergedBranches {
					if !isExcluded(b.Name, req.ExcludePatterns) {
						branchesToDelete = append(branchesToDelete, b.Name)
					}
				}
			}
		}

		// Stale 브랜치 수집
		if req.IncludeStale {
			staleBranches, err := ghClient.ListStaleBranches(ctx, req.Namespace, req.Repository, staleDays)
			if err == nil {
				for _, b := range staleBranches {
					if !isExcluded(b.Name, req.ExcludePatterns) && !contains(branchesToDelete, b.Name) {
						branchesToDelete = append(branchesToDelete, b.Name)
					}
				}
			}
		}

		// 브랜치 삭제 (dry_run이 아닌 경우)
		for _, branchName := range branchesToDelete {
			if req.DryRun {
				result.Deleted = append(result.Deleted, branchName+" (dry run)")
			} else {
				err := ghClient.DeleteBranch(ctx, req.Namespace, req.Repository, branchName)
				if err != nil {
					result.Failed = append(result.Failed, fmt.Sprintf("%s (%v)", branchName, err))
				} else {
					result.Deleted = append(result.Deleted, branchName)
				}
			}
		}

	case *pb.ProviderConfig_Gitlab:
		projectPath := req.Repository
		if req.Namespace != "" {
			projectPath = req.Namespace + "/" + req.Repository
		}
		glClient, clientErr := createGitLabClient(config.Gitlab)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
		}

		// 머지된 브랜치 수집
		if req.IncludeMerged {
			mergedBranches, err := glClient.ListMergedBranches(ctx, projectPath, "main")
			if err == nil {
				for _, b := range mergedBranches {
					if !isExcluded(b.Name, req.ExcludePatterns) {
						branchesToDelete = append(branchesToDelete, b.Name)
					}
				}
			}
		}

		// Stale 브랜치 수집
		if req.IncludeStale {
			staleBranches, err := glClient.ListStaleBranches(ctx, projectPath, staleDays)
			if err == nil {
				for _, b := range staleBranches {
					if !isExcluded(b.Name, req.ExcludePatterns) && !contains(branchesToDelete, b.Name) {
						branchesToDelete = append(branchesToDelete, b.Name)
					}
				}
			}
		}

		// 브랜치 삭제 (dry_run이 아닌 경우)
		for _, branchName := range branchesToDelete {
			if req.DryRun {
				result.Deleted = append(result.Deleted, branchName+" (dry run)")
			} else {
				err := glClient.DeleteBranch(ctx, projectPath, branchName)
				if err != nil {
					result.Failed = append(result.Failed, fmt.Sprintf("%s (%v)", branchName, err))
				} else {
					result.Deleted = append(result.Deleted, branchName)
				}
			}
		}

	case *pb.ProviderConfig_Bitbucket:
		bbClient, clientErr := createBitbucketClient(config.Bitbucket)
		if clientErr != nil {
			return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
		}

		// 머지된 브랜치 수집
		if req.IncludeMerged {
			mergedBranches, err := bbClient.ListMergedBranches(ctx, req.Repository, "main")
			if err == nil {
				for _, b := range mergedBranches {
					if !isExcluded(b.Name, req.ExcludePatterns) {
						branchesToDelete = append(branchesToDelete, b.Name)
					}
				}
			}
		}

		// Stale 브랜치 수집
		if req.IncludeStale {
			staleBranches, err := bbClient.ListStaleBranches(ctx, req.Repository, staleDays)
			if err == nil {
				for _, b := range staleBranches {
					if !isExcluded(b.Name, req.ExcludePatterns) && !contains(branchesToDelete, b.Name) {
						branchesToDelete = append(branchesToDelete, b.Name)
					}
				}
			}
		}

		// 브랜치 삭제 (dry_run이 아닌 경우)
		for _, branchName := range branchesToDelete {
			if req.DryRun {
				result.Deleted = append(result.Deleted, branchName+" (dry run)")
			} else {
				err := bbClient.DeleteBranch(ctx, req.Repository, branchName)
				if err != nil {
					result.Failed = append(result.Failed, fmt.Sprintf("%s (%v)", branchName, err))
				} else {
					result.Deleted = append(result.Deleted, branchName)
				}
			}
		}

	default:
		return nil, status.Error(codes.InvalidArgument, "unknown provider type")
	}

	return &pb.CleanupBranchesResponse{Result: result}, nil
}

// =============================================================================
// 변환 헬퍼 함수
// =============================================================================

func convertBranchComparison(c *client.BranchComparison) *pb.BranchComparison {
	if c == nil {
		return nil
	}

	mergeable := pb.MergeableState_MERGEABLE_STATE_UNKNOWN
	switch c.Mergeable {
	case "mergeable":
		mergeable = pb.MergeableState_MERGEABLE_STATE_MERGEABLE
	case "conflicting":
		mergeable = pb.MergeableState_MERGEABLE_STATE_CONFLICTING
	}

	suggestedAction := pb.SuggestedAction_SUGGESTED_ACTION_UNSPECIFIED
	switch c.SuggestedAction {
	case "CREATE_MR":
		suggestedAction = pb.SuggestedAction_SUGGESTED_ACTION_CREATE_MR
	case "REBASE":
		suggestedAction = pb.SuggestedAction_SUGGESTED_ACTION_REBASE
	case "MERGE_BASE":
		suggestedAction = pb.SuggestedAction_SUGGESTED_ACTION_MERGE_BASE
	case "RESOLVE_CONFLICTS":
		suggestedAction = pb.SuggestedAction_SUGGESTED_ACTION_RESOLVE_CONFLICTS
	case "UP_TO_DATE":
		suggestedAction = pb.SuggestedAction_SUGGESTED_ACTION_UP_TO_DATE
	}

	return &pb.BranchComparison{
		BaseBranch:      c.BaseBranch,
		CompareBranch:   c.CompareBranch,
		AheadBy:         int32(c.AheadBy),
		BehindBy:        int32(c.BehindBy),
		Mergeable:       mergeable,
		MergeStatus:     c.MergeStatus,
		SuggestedAction: suggestedAction,
		BaseSha:         c.BaseSha,
		CompareSha:      c.CompareSha,
		MergeBaseSha:    c.MergeBaseSha,
	}
}

func convertCommitInfoList(commits []*client.CommitInfo) []*pb.CommitInfo {
	result := make([]*pb.CommitInfo, len(commits))
	for i, c := range commits {
		result[i] = &pb.CommitInfo{
			Sha:         c.SHA,
			Message:     c.Message,
			AuthorName:  c.AuthorName,
			AuthorEmail: c.AuthorEmail,
			Date:        c.Date,
		}
	}
	return result
}

func convertMergedBranchInfoList(branches []*client.MergedBranchInfo) []*pb.MergedBranchInfo {
	result := make([]*pb.MergedBranchInfo, len(branches))
	for i, b := range branches {
		result[i] = &pb.MergedBranchInfo{
			Name:          b.Name,
			MergedAt:      b.MergedAt,
			MergedBy:      b.MergedBy,
			LastCommitSha: b.LastCommitSHA,
			MergedInto:    b.MergedInto,
		}
	}
	return result
}

func convertStaleBranchInfoList(branches []*client.StaleBranchInfo) []*pb.StaleBranchInfo {
	result := make([]*pb.StaleBranchInfo, len(branches))
	for i, b := range branches {
		result[i] = &pb.StaleBranchInfo{
			Name:           b.Name,
			LastCommitSha:  b.LastCommitSHA,
			LastCommitDate: b.LastCommitDate,
			DaysInactive:   int32(b.DaysInactive),
		}
	}
	return result
}

// =============================================================================
// 유틸리티 함수
// =============================================================================

// isExcluded는 브랜치 이름이 제외 패턴에 해당하는지 확인합니다.
func isExcluded(branchName string, patterns []string) bool {
	for _, pattern := range patterns {
		// 간단한 패턴 매칭 (release/*, hotfix/* 등)
		if len(pattern) > 0 && pattern[len(pattern)-1] == '*' {
			prefix := pattern[:len(pattern)-1]
			if len(branchName) >= len(prefix) && branchName[:len(prefix)] == prefix {
				return true
			}
		} else if branchName == pattern {
			return true
		}
	}
	return false
}

// contains는 슬라이스에 문자열이 포함되어 있는지 확인합니다.
func contains(slice []string, item string) bool {
	for _, s := range slice {
		if s == item {
			return true
		}
	}
	return false
}
