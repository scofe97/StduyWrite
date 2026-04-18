package client

import (
	"context"
	"fmt"
	"time"

	"github.com/xanzy/go-gitlab"

	pb "github.com/runners-high/git-provider/pkg/pb/v1"
)

// GitLabClient는 GitLab API 클라이언트입니다.
type GitLabClient struct {
	client *gitlab.Client
}

// NewGitLabClient는 새 GitLab 클라이언트를 생성합니다.
func NewGitLabClient(token, baseURL string) (*GitLabClient, error) {
	var client *gitlab.Client
	var err error

	if baseURL != "" {
		// Self-hosted GitLab
		client, err = gitlab.NewClient(token, gitlab.WithBaseURL(baseURL))
	} else {
		// Public GitLab
		client, err = gitlab.NewClient(token)
	}

	if err != nil {
		return nil, fmt.Errorf("failed to create GitLab client: %w", err)
	}

	return &GitLabClient{client: client}, nil
}

// =============================================================================
// 저장소(프로젝트) 관련 메서드
// =============================================================================

// ListRepositories는 사용자의 프로젝트 목록을 반환합니다.
func (c *GitLabClient) ListRepositories(ctx context.Context) ([]*pb.Repository, error) {
	// 인증된 사용자의 프로젝트 조회
	owned := true
	projects, _, err := c.client.Projects.ListProjects(&gitlab.ListProjectsOptions{
		Owned:       &owned,
		ListOptions: gitlab.ListOptions{PerPage: 100},
	})
	if err != nil {
		return nil, fmt.Errorf("failed to list projects: %w", err)
	}

	result := make([]*pb.Repository, len(projects))
	for i, proj := range projects {
		result[i] = c.convertProject(proj)
	}

	return result, nil
}

// GetRepository는 특정 프로젝트의 상세 정보를 반환합니다.
func (c *GitLabClient) GetRepository(ctx context.Context, projectPath string) (*pb.Repository, error) {
	project, _, err := c.client.Projects.GetProject(projectPath, &gitlab.GetProjectOptions{})
	if err != nil {
		return nil, fmt.Errorf("failed to get project: %w", err)
	}

	return c.convertProject(project), nil
}

// CreateRepository는 새 프로젝트를 생성합니다.
func (c *GitLabClient) CreateRepository(ctx context.Context, name, description string, private bool, namespaceID int) (*pb.Repository, error) {
	visibility := gitlab.PublicVisibility
	if private {
		visibility = gitlab.PrivateVisibility
	}

	opts := &gitlab.CreateProjectOptions{
		Name:                 gitlab.Ptr(name),
		Description:          gitlab.Ptr(description),
		Visibility:           gitlab.Ptr(visibility),
		InitializeWithReadme: gitlab.Ptr(true),
	}

	if namespaceID > 0 {
		opts.NamespaceID = gitlab.Ptr(namespaceID)
	}

	project, _, err := c.client.Projects.CreateProject(opts)
	if err != nil {
		return nil, fmt.Errorf("failed to create project: %w", err)
	}

	return c.convertProject(project), nil
}

// DeleteRepository는 프로젝트를 삭제합니다.
func (c *GitLabClient) DeleteRepository(ctx context.Context, projectPath string) error {
	_, err := c.client.Projects.DeleteProject(projectPath, nil)
	if err != nil {
		return fmt.Errorf("failed to delete project: %w", err)
	}
	return nil
}

// =============================================================================
// 브랜치 관련 메서드
// =============================================================================

// ListBranches는 프로젝트의 브랜치 목록을 반환합니다.
func (c *GitLabClient) ListBranches(ctx context.Context, projectPath string) ([]*pb.Branch, error) {
	branches, _, err := c.client.Branches.ListBranches(projectPath, &gitlab.ListBranchesOptions{
		ListOptions: gitlab.ListOptions{PerPage: 100},
	})
	if err != nil {
		return nil, fmt.Errorf("failed to list branches: %w", err)
	}

	result := make([]*pb.Branch, len(branches))
	for i, branch := range branches {
		result[i] = c.convertBranch(branch)
	}

	return result, nil
}

// GetBranch는 특정 브랜치의 상세 정보를 반환합니다.
func (c *GitLabClient) GetBranch(ctx context.Context, projectPath, branchName string) (*pb.Branch, error) {
	branch, _, err := c.client.Branches.GetBranch(projectPath, branchName)
	if err != nil {
		return nil, fmt.Errorf("failed to get branch: %w", err)
	}

	return c.convertBranch(branch), nil
}

// CreateBranch는 새 브랜치를 생성합니다.
func (c *GitLabClient) CreateBranch(ctx context.Context, projectPath, branchName, ref string) (*pb.Branch, error) {
	branch, _, err := c.client.Branches.CreateBranch(projectPath, &gitlab.CreateBranchOptions{
		Branch: gitlab.Ptr(branchName),
		Ref:    gitlab.Ptr(ref),
	})
	if err != nil {
		return nil, fmt.Errorf("failed to create branch: %w", err)
	}

	return c.convertBranch(branch), nil
}

// DeleteBranch는 브랜치를 삭제합니다.
func (c *GitLabClient) DeleteBranch(ctx context.Context, projectPath, branchName string) error {
	_, err := c.client.Branches.DeleteBranch(projectPath, branchName)
	if err != nil {
		return fmt.Errorf("failed to delete branch: %w", err)
	}
	return nil
}

// =============================================================================
// 헬퍼 메서드
// =============================================================================

// convertProject는 GitLab Project를 통합 모델로 변환합니다.
func (c *GitLabClient) convertProject(proj *gitlab.Project) *pb.Repository {
	return &pb.Repository{
		Id:            fmt.Sprintf("%d", proj.ID),
		Name:          proj.Name,
		FullName:      proj.PathWithNamespace,
		Description:   proj.Description,
		Url:           proj.WebURL,
		CloneUrl:      proj.HTTPURLToRepo,
		SshUrl:        proj.SSHURLToRepo,
		DefaultBranch: proj.DefaultBranch,
		Private:       proj.Visibility != gitlab.PublicVisibility,
		CreatedAt:     proj.CreatedAt.String(),
		UpdatedAt:     proj.LastActivityAt.String(),
		Provider:      pb.ProviderType_PROVIDER_TYPE_GITLAB,
		Namespace:     c.convertNamespace(proj.Namespace),
	}
}

// convertNamespace는 GitLab Namespace를 통합 모델로 변환합니다.
func (c *GitLabClient) convertNamespace(ns *gitlab.ProjectNamespace) *pb.Namespace {
	if ns == nil {
		return nil
	}

	nsType := pb.NamespaceType_NAMESPACE_TYPE_UNSPECIFIED
	switch ns.Kind {
	case "user":
		nsType = pb.NamespaceType_NAMESPACE_TYPE_USER
	case "group":
		nsType = pb.NamespaceType_NAMESPACE_TYPE_GROUP
	}

	return &pb.Namespace{
		Id:        fmt.Sprintf("%d", ns.ID),
		Name:      ns.Name,
		FullPath:  ns.FullPath,
		Type:      nsType,
		AvatarUrl: ns.AvatarURL,
		Url:       ns.WebURL,
	}
}

// convertBranch는 GitLab Branch를 통합 모델로 변환합니다.
func (c *GitLabClient) convertBranch(branch *gitlab.Branch) *pb.Branch {
	result := &pb.Branch{
		Name:      branch.Name,
		Sha:       branch.Commit.ID,
		Protected: branch.Protected,
		IsDefault: branch.Default,
	}

	// 커밋 정보 추가
	if branch.Commit != nil {
		result.LastCommit = &pb.Commit{
			Sha:         branch.Commit.ID,
			Message:     branch.Commit.Title,
			AuthorName:  branch.Commit.AuthorName,
			AuthorEmail: branch.Commit.AuthorEmail,
			Date:        branch.Commit.AuthoredDate.String(),
		}
	}

	return result
}

// =============================================================================
// 콘텐츠 관련 메서드 (Phase 1.1)
// =============================================================================

// GetTree는 저장소의 파일 트리를 반환합니다.
func (c *GitLabClient) GetTree(ctx context.Context, projectPath, ref string, recursive bool) ([]*pb.TreeEntry, error) {
	// ref가 비어있으면 기본 브랜치 사용
	if ref == "" {
		project, _, err := c.client.Projects.GetProject(projectPath, &gitlab.GetProjectOptions{})
		if err != nil {
			return nil, fmt.Errorf("failed to get project: %w", err)
		}
		ref = project.DefaultBranch
	}

	opts := &gitlab.ListTreeOptions{
		Ref:         gitlab.Ptr(ref),
		Recursive:   gitlab.Ptr(recursive),
		ListOptions: gitlab.ListOptions{PerPage: 100},
	}

	var allEntries []*pb.TreeEntry
	for {
		treeNodes, resp, err := c.client.Repositories.ListTree(projectPath, opts)
		if err != nil {
			return nil, fmt.Errorf("failed to list tree: %w", err)
		}

		for _, node := range treeNodes {
			entries := &pb.TreeEntry{
				Path: node.Path,
				Type: node.Type,
				Sha:  node.ID,
				Mode: node.Mode,
			}
			allEntries = append(allEntries, entries)
		}

		if resp.NextPage == 0 {
			break
		}
		opts.Page = resp.NextPage
	}

	return allEntries, nil
}

// GetContents는 특정 경로의 파일/디렉토리 내용을 반환합니다.
func (c *GitLabClient) GetContents(ctx context.Context, projectPath, path, ref string) (*pb.ContentEntry, error) {
	opts := &gitlab.GetFileOptions{}
	if ref != "" {
		opts.Ref = gitlab.Ptr(ref)
	}

	// 먼저 파일로 시도
	file, resp, err := c.client.RepositoryFiles.GetFile(projectPath, path, opts)
	if err == nil && file != nil {
		return &pb.ContentEntry{
			Type:     pb.ContentType_CONTENT_TYPE_FILE,
			Name:     file.FileName,
			Path:     file.FilePath,
			Size:     int64(file.Size),
			Sha:      file.BlobID,
			Content:  file.Content,
			Encoding: file.Encoding,
		}, nil
	}

	// 파일이 아니면 디렉토리로 시도
	if resp != nil && resp.StatusCode == 404 {
		// 트리 조회로 디렉토리 내용 가져오기
		treeOpts := &gitlab.ListTreeOptions{
			Path:        gitlab.Ptr(path),
			ListOptions: gitlab.ListOptions{PerPage: 100},
		}
		if ref != "" {
			treeOpts.Ref = gitlab.Ptr(ref)
		}

		treeNodes, _, err := c.client.Repositories.ListTree(projectPath, treeOpts)
		if err != nil {
			return nil, fmt.Errorf("failed to get contents: %w", err)
		}

		entries := make([]*pb.ContentEntry, len(treeNodes))
		for i, node := range treeNodes {
			contentType := pb.ContentType_CONTENT_TYPE_FILE
			if node.Type == "tree" {
				contentType = pb.ContentType_CONTENT_TYPE_DIRECTORY
			}
			entries[i] = &pb.ContentEntry{
				Type: contentType,
				Name: node.Name,
				Path: node.Path,
				Sha:  node.ID,
			}
		}

		return &pb.ContentEntry{
			Type:    pb.ContentType_CONTENT_TYPE_DIRECTORY,
			Name:    getLastSegment(path),
			Path:    path,
			Entries: entries,
		}, nil
	}

	return nil, fmt.Errorf("failed to get contents: %w", err)
}

// GetReadme는 저장소의 README 파일을 반환합니다.
func (c *GitLabClient) GetReadme(ctx context.Context, projectPath, ref string) (*pb.ContentEntry, error) {
	// README 파일명 후보
	readmeNames := []string{"README.md", "README.MD", "readme.md", "README", "README.txt"}

	for _, name := range readmeNames {
		content, err := c.GetContents(ctx, projectPath, name, ref)
		if err == nil {
			return content, nil
		}
	}

	return nil, fmt.Errorf("README not found")
}

// getLastSegment는 경로의 마지막 세그먼트를 반환합니다.
func getLastSegment(path string) string {
	if path == "" {
		return ""
	}
	// 끝의 / 제거
	for len(path) > 0 && path[len(path)-1] == '/' {
		path = path[:len(path)-1]
	}
	// 마지막 / 이후 부분 반환
	for i := len(path) - 1; i >= 0; i-- {
		if path[i] == '/' {
			return path[i+1:]
		}
	}
	return path
}

// =============================================================================
// 브랜치 비교 메서드 (Phase 1.2)
// =============================================================================

// CompareBranches는 두 브랜치를 비교합니다.
func (c *GitLabClient) CompareBranches(ctx context.Context, projectPath, base, compare string) (*BranchComparison, error) {
	comparison, _, err := c.client.Repositories.Compare(projectPath, &gitlab.CompareOptions{
		From: gitlab.Ptr(base),
		To:   gitlab.Ptr(compare),
	})
	if err != nil {
		return nil, fmt.Errorf("failed to compare branches: %w", err)
	}

	result := &BranchComparison{
		BaseBranch:    base,
		CompareBranch: compare,
		MergeBaseSha:  comparison.Commit.ID, // GitLab의 Compare는 merge base를 직접 제공하지 않음
	}

	// 커밋 수로 ahead/behind 계산
	result.AheadBy = len(comparison.Commits)

	// behind_by 계산을 위해 역방향 비교
	reverseComparison, _, err := c.client.Repositories.Compare(projectPath, &gitlab.CompareOptions{
		From: gitlab.Ptr(compare),
		To:   gitlab.Ptr(base),
	})
	if err == nil {
		result.BehindBy = len(reverseComparison.Commits)
	}

	// base와 compare의 SHA 조회
	baseBranch, _, err := c.client.Branches.GetBranch(projectPath, base)
	if err == nil {
		result.BaseSha = baseBranch.Commit.ID
	}

	compareBranch, _, err := c.client.Branches.GetBranch(projectPath, compare)
	if err == nil {
		result.CompareSha = compareBranch.Commit.ID
	}

	// 파일 변경 통계
	if comparison.Diffs != nil {
		result.FilesChanged = len(comparison.Diffs)
		for _, diff := range comparison.Diffs {
			// GitLab diff는 additions/deletions를 직접 제공하지 않음
			// 대신 diff 문자열을 분석해야 함 (간략화)
			_ = diff
		}
	}

	// 머지 가능 여부 판단
	result.Mergeable = "unknown"
	result.MergeStatus = determineMergeStatus(result.AheadBy, result.BehindBy)
	result.SuggestedAction = determineSuggestedAction(result.AheadBy, result.BehindBy, result.MergeStatus)

	return result, nil
}

// ListCommitsDiff는 두 브랜치 간 커밋 차이를 조회합니다.
func (c *GitLabClient) ListCommitsDiff(ctx context.Context, projectPath, base, compare string, page, perPage int) ([]*CommitInfo, int, error) {
	if perPage == 0 {
		perPage = 30
	}
	if page == 0 {
		page = 1
	}

	comparison, _, err := c.client.Repositories.Compare(projectPath, &gitlab.CompareOptions{
		From: gitlab.Ptr(base),
		To:   gitlab.Ptr(compare),
	})
	if err != nil {
		return nil, 0, fmt.Errorf("failed to compare commits: %w", err)
	}

	totalCount := len(comparison.Commits)

	// 페이징 적용
	start := (page - 1) * perPage
	end := start + perPage
	if start >= totalCount {
		return []*CommitInfo{}, totalCount, nil
	}
	if end > totalCount {
		end = totalCount
	}

	commits := make([]*CommitInfo, 0, end-start)
	for i := start; i < end; i++ {
		commit := comparison.Commits[i]
		commits = append(commits, &CommitInfo{
			SHA:         commit.ID,
			Message:     commit.Title,
			AuthorName:  commit.AuthorName,
			AuthorEmail: commit.AuthorEmail,
			Date:        commit.AuthoredDate.String(),
		})
	}

	return commits, totalCount, nil
}

// ListMergedBranches는 기준 브랜치에 머지된 브랜치 목록을 반환합니다.
func (c *GitLabClient) ListMergedBranches(ctx context.Context, projectPath, base string) ([]*MergedBranchInfo, error) {
	// 머지된 MR 목록을 통해 머지된 브랜치 확인
	state := "merged"
	mrs, _, err := c.client.MergeRequests.ListProjectMergeRequests(projectPath, &gitlab.ListProjectMergeRequestsOptions{
		State:        gitlab.Ptr(state),
		TargetBranch: gitlab.Ptr(base),
		ListOptions: gitlab.ListOptions{
			PerPage: 100,
		},
	})
	if err != nil {
		return nil, fmt.Errorf("failed to list merged MRs: %w", err)
	}

	merged := make([]*MergedBranchInfo, 0, len(mrs))
	seenBranches := make(map[string]bool)

	for _, mr := range mrs {
		if seenBranches[mr.SourceBranch] {
			continue
		}
		seenBranches[mr.SourceBranch] = true

		mergedAt := ""
		if mr.MergedAt != nil {
			mergedAt = mr.MergedAt.String()
		}

		mergedBy := ""
		if mr.MergedBy != nil {
			mergedBy = mr.MergedBy.Username
		}

		merged = append(merged, &MergedBranchInfo{
			Name:          mr.SourceBranch,
			MergedAt:      mergedAt,
			MergedBy:      mergedBy,
			LastCommitSHA: mr.SHA,
			MergedInto:    mr.TargetBranch,
		})
	}

	return merged, nil
}

// ListStaleBranches는 오래된 브랜치 목록을 반환합니다.
func (c *GitLabClient) ListStaleBranches(ctx context.Context, projectPath string, staleDays int) ([]*StaleBranchInfo, error) {
	if staleDays == 0 {
		staleDays = 30
	}

	branches, _, err := c.client.Branches.ListBranches(projectPath, &gitlab.ListBranchesOptions{
		ListOptions: gitlab.ListOptions{PerPage: 100},
	})
	if err != nil {
		return nil, fmt.Errorf("failed to list branches: %w", err)
	}

	var stale []*StaleBranchInfo
	now := time.Now()

	for _, branch := range branches {
		if branch.Commit == nil || branch.Commit.AuthoredDate == nil {
			continue
		}

		commitDate := time.Time(*branch.Commit.AuthoredDate)
		daysSince := int(now.Sub(commitDate).Hours() / 24)

		if daysSince >= staleDays {
			stale = append(stale, &StaleBranchInfo{
				Name:           branch.Name,
				LastCommitSHA:  branch.Commit.ID,
				LastCommitDate: commitDate.String(),
				DaysInactive:   daysSince,
			})
		}
	}

	return stale, nil
}

// determineMergeStatus는 머지 상태를 결정합니다.
func determineMergeStatus(aheadBy, behindBy int) string {
	if aheadBy == 0 && behindBy == 0 {
		return "identical"
	}
	if aheadBy > 0 && behindBy > 0 {
		return "diverged"
	}
	if aheadBy > 0 {
		return "ahead"
	}
	return "behind"
}

// =============================================================================
// Merge Request 메서드 (Phase 1.4)
// =============================================================================

// ListMergeRequests는 MR 목록을 반환합니다.
func (c *GitLabClient) ListMergeRequests(ctx context.Context, projectPath string, state string, page, perPage int) ([]*MergeRequestInfo, int, error) {
	if perPage == 0 {
		perPage = 30
	}
	if page == 0 {
		page = 1
	}

	opts := &gitlab.ListProjectMergeRequestsOptions{
		ListOptions: gitlab.ListOptions{
			Page:    page,
			PerPage: perPage,
		},
	}

	// state 변환
	if state != "" && state != "all" {
		opts.State = gitlab.Ptr(state)
	}

	mrs, resp, err := c.client.MergeRequests.ListProjectMergeRequests(projectPath, opts)
	if err != nil {
		return nil, 0, fmt.Errorf("failed to list merge requests: %w", err)
	}

	result := make([]*MergeRequestInfo, len(mrs))
	for i, mr := range mrs {
		result[i] = c.convertMergeRequest(mr)
	}

	totalCount := resp.TotalItems
	if totalCount == 0 {
		totalCount = len(mrs)
	}

	return result, totalCount, nil
}

// GetMergeRequest는 MR 상세 정보를 반환합니다.
func (c *GitLabClient) GetMergeRequest(ctx context.Context, projectPath string, mrIID int) (*MergeRequestInfo, error) {
	mr, _, err := c.client.MergeRequests.GetMergeRequest(projectPath, mrIID, &gitlab.GetMergeRequestsOptions{})
	if err != nil {
		return nil, fmt.Errorf("failed to get merge request: %w", err)
	}

	return c.convertMergeRequest(mr), nil
}

// CreateMergeRequest는 새 MR을 생성합니다.
func (c *GitLabClient) CreateMergeRequest(ctx context.Context, projectPath string, title, description, sourceBranch, targetBranch string, draft bool) (*MergeRequestInfo, error) {
	opts := &gitlab.CreateMergeRequestOptions{
		Title:        gitlab.Ptr(title),
		Description:  gitlab.Ptr(description),
		SourceBranch: gitlab.Ptr(sourceBranch),
		TargetBranch: gitlab.Ptr(targetBranch),
	}

	// Draft MR 생성 (GitLab 14.0+)
	if draft {
		opts.Title = gitlab.Ptr("Draft: " + title)
	}

	mr, _, err := c.client.MergeRequests.CreateMergeRequest(projectPath, opts)
	if err != nil {
		return nil, fmt.Errorf("failed to create merge request: %w", err)
	}

	return c.convertMergeRequest(mr), nil
}

// UpdateMergeRequest는 MR을 수정합니다.
func (c *GitLabClient) UpdateMergeRequest(ctx context.Context, projectPath string, mrIID int, title, description, state, targetBranch string) (*MergeRequestInfo, error) {
	opts := &gitlab.UpdateMergeRequestOptions{}

	if title != "" {
		opts.Title = gitlab.Ptr(title)
	}
	if description != "" {
		opts.Description = gitlab.Ptr(description)
	}
	if state != "" {
		opts.StateEvent = gitlab.Ptr(state) // "close" or "reopen"
	}
	if targetBranch != "" {
		opts.TargetBranch = gitlab.Ptr(targetBranch)
	}

	mr, _, err := c.client.MergeRequests.UpdateMergeRequest(projectPath, mrIID, opts)
	if err != nil {
		return nil, fmt.Errorf("failed to update merge request: %w", err)
	}

	return c.convertMergeRequest(mr), nil
}

// MergeMergeRequest는 MR을 머지합니다.
func (c *GitLabClient) MergeMergeRequest(ctx context.Context, projectPath string, mrIID int, commitMessage string, squash, deleteSourceBranch bool) (*MergeRequestInfo, string, error) {
	opts := &gitlab.AcceptMergeRequestOptions{
		Squash:                      gitlab.Ptr(squash),
		ShouldRemoveSourceBranch:    gitlab.Ptr(deleteSourceBranch),
	}

	if commitMessage != "" {
		opts.MergeCommitMessage = gitlab.Ptr(commitMessage)
	}

	mr, _, err := c.client.MergeRequests.AcceptMergeRequest(projectPath, mrIID, opts)
	if err != nil {
		return nil, "", fmt.Errorf("failed to merge merge request: %w", err)
	}

	return c.convertMergeRequest(mr), mr.MergeCommitSHA, nil
}

// GetMergeRequestDiff는 MR의 변경사항을 반환합니다.
func (c *GitLabClient) GetMergeRequestDiff(ctx context.Context, projectPath string, mrIID int) (*MergeRequestDiffInfo, error) {
	changes, _, err := c.client.MergeRequests.GetMergeRequestChanges(projectPath, mrIID, &gitlab.GetMergeRequestChangesOptions{})
	if err != nil {
		return nil, fmt.Errorf("failed to get merge request changes: %w", err)
	}

	diff := &MergeRequestDiffInfo{
		Files:        make([]*FileDiffInfo, len(changes.Changes)),
		ChangedFiles: len(changes.Changes),
	}

	for i, change := range changes.Changes {
		status := "modified"
		if change.NewFile {
			status = "added"
		} else if change.DeletedFile {
			status = "removed"
		} else if change.RenamedFile {
			status = "renamed"
		}

		diff.Files[i] = &FileDiffInfo{
			Filename:         change.NewPath,
			Status:           status,
			Patch:            change.Diff,
			PreviousFilename: change.OldPath,
		}
	}

	return diff, nil
}

// ListReviews는 MR 승인자 목록을 반환합니다.
func (c *GitLabClient) ListReviews(ctx context.Context, projectPath string, mrIID int) ([]*ReviewInfo, error) {
	approvals, _, err := c.client.MergeRequestApprovals.GetConfiguration(projectPath, mrIID)
	if err != nil {
		return nil, fmt.Errorf("failed to get merge request approvals: %w", err)
	}

	var reviews []*ReviewInfo
	for _, approver := range approvals.ApprovedBy {
		reviews = append(reviews, &ReviewInfo{
			ID:    fmt.Sprintf("%d", approver.User.ID),
			User:  c.convertGitLabBasicUser(approver.User),
			State: "APPROVED",
		})
	}

	return reviews, nil
}

// SubmitReview는 MR 승인/거부를 제출합니다.
func (c *GitLabClient) SubmitReview(ctx context.Context, projectPath string, mrIID int, state, body string) (*ReviewInfo, error) {
	switch state {
	case "APPROVED":
		_, _, err := c.client.MergeRequestApprovals.ApproveMergeRequest(projectPath, mrIID, &gitlab.ApproveMergeRequestOptions{})
		if err != nil {
			return nil, fmt.Errorf("failed to approve merge request: %w", err)
		}
	case "CHANGES_REQUESTED":
		// GitLab은 명시적인 "변경 요청" 기능이 없음. 코멘트로 대체
		if body != "" {
			_, _, err := c.client.Notes.CreateMergeRequestNote(projectPath, mrIID, &gitlab.CreateMergeRequestNoteOptions{
				Body: gitlab.Ptr(body),
			})
			if err != nil {
				return nil, fmt.Errorf("failed to add review comment: %w", err)
			}
		}
	}

	return &ReviewInfo{
		State: state,
		Body:  body,
	}, nil
}

// ListComments는 MR 댓글 목록을 반환합니다.
func (c *GitLabClient) ListComments(ctx context.Context, projectPath string, mrIID int) ([]*CommentInfo, error) {
	notes, _, err := c.client.Notes.ListMergeRequestNotes(projectPath, mrIID, &gitlab.ListMergeRequestNotesOptions{
		ListOptions: gitlab.ListOptions{PerPage: 100},
	})
	if err != nil {
		return nil, fmt.Errorf("failed to list merge request notes: %w", err)
	}

	result := make([]*CommentInfo, len(notes))
	for i, note := range notes {
		result[i] = &CommentInfo{
			ID:        fmt.Sprintf("%d", note.ID),
			User:      c.convertNoteAuthor(note.Author),
			Body:      note.Body,
			CreatedAt: note.CreatedAt.String(),
			UpdatedAt: note.UpdatedAt.String(),
		}
	}

	return result, nil
}

// CreateComment는 MR 댓글을 생성합니다.
func (c *GitLabClient) CreateComment(ctx context.Context, projectPath string, mrIID int, body, path string, line int) (*CommentInfo, error) {
	note, _, err := c.client.Notes.CreateMergeRequestNote(projectPath, mrIID, &gitlab.CreateMergeRequestNoteOptions{
		Body: gitlab.Ptr(body),
	})
	if err != nil {
		return nil, fmt.Errorf("failed to create merge request note: %w", err)
	}

	return &CommentInfo{
		ID:        fmt.Sprintf("%d", note.ID),
		User:      c.convertNoteAuthor(note.Author),
		Body:      note.Body,
		CreatedAt: note.CreatedAt.String(),
		UpdatedAt: note.UpdatedAt.String(),
	}, nil
}

// UpdateComment는 MR 댓글을 수정합니다.
func (c *GitLabClient) UpdateComment(ctx context.Context, projectPath string, mrIID, noteID int, body string) (*CommentInfo, error) {
	note, _, err := c.client.Notes.UpdateMergeRequestNote(projectPath, mrIID, noteID, &gitlab.UpdateMergeRequestNoteOptions{
		Body: gitlab.Ptr(body),
	})
	if err != nil {
		return nil, fmt.Errorf("failed to update merge request note: %w", err)
	}

	return &CommentInfo{
		ID:        fmt.Sprintf("%d", note.ID),
		User:      c.convertNoteAuthor(note.Author),
		Body:      note.Body,
		CreatedAt: note.CreatedAt.String(),
		UpdatedAt: note.UpdatedAt.String(),
	}, nil
}

// DeleteComment는 MR 댓글을 삭제합니다.
func (c *GitLabClient) DeleteComment(ctx context.Context, projectPath string, mrIID, noteID int) error {
	_, err := c.client.Notes.DeleteMergeRequestNote(projectPath, mrIID, noteID)
	if err != nil {
		return fmt.Errorf("failed to delete merge request note: %w", err)
	}
	return nil
}

// convertMergeRequest는 GitLab MR을 MergeRequestInfo로 변환합니다.
func (c *GitLabClient) convertMergeRequest(mr *gitlab.MergeRequest) *MergeRequestInfo {
	if mr == nil {
		return nil
	}

	state := "open"
	if mr.State == "merged" {
		state = "merged"
	} else if mr.State == "closed" {
		state = "closed"
	}

	result := &MergeRequestInfo{
		ID:           fmt.Sprintf("%d", mr.ID),
		Number:       mr.IID,
		Title:        mr.Title,
		Description:  mr.Description,
		State:        state,
		SourceBranch: mr.SourceBranch,
		TargetBranch: mr.TargetBranch,
		URL:          mr.WebURL,
		Draft:        mr.Draft,
		Mergeable:    mr.MergeStatus == "can_be_merged",
		CreatedAt:    mr.CreatedAt.String(),
		UpdatedAt:    mr.UpdatedAt.String(),
		HeadSHA:      mr.SHA,
	}

	if mr.Author != nil {
		result.Author = c.convertGitLabBasicUser(mr.Author)
	}

	if mr.MergedAt != nil {
		result.MergedAt = mr.MergedAt.String()
	}
	if mr.ClosedAt != nil {
		result.ClosedAt = mr.ClosedAt.String()
	}
	if mr.MergedBy != nil {
		result.MergedBy = c.convertGitLabBasicUser(mr.MergedBy)
	}

	// 담당자
	if mr.Assignees != nil {
		result.Assignees = make([]*UserInfo, len(mr.Assignees))
		for i, a := range mr.Assignees {
			result.Assignees[i] = c.convertGitLabBasicUser(a)
		}
	}

	// 리뷰어
	if mr.Reviewers != nil {
		result.Reviewers = make([]*UserInfo, len(mr.Reviewers))
		for i, r := range mr.Reviewers {
			result.Reviewers[i] = c.convertGitLabBasicUser(r)
		}
	}

	// 라벨
	if mr.Labels != nil {
		result.Labels = mr.Labels
	}

	return result
}

// convertGitLabUser는 GitLab User를 UserInfo로 변환합니다.
func (c *GitLabClient) convertGitLabUser(user *gitlab.User) *UserInfo {
	if user == nil {
		return nil
	}
	return &UserInfo{
		ID:        fmt.Sprintf("%d", user.ID),
		Login:     user.Username,
		Name:      user.Name,
		Email:     user.Email,
		AvatarURL: user.AvatarURL,
	}
}

// convertGitLabBasicUser는 GitLab BasicUser를 UserInfo로 변환합니다.
func (c *GitLabClient) convertGitLabBasicUser(user *gitlab.BasicUser) *UserInfo {
	if user == nil {
		return nil
	}
	return &UserInfo{
		ID:        fmt.Sprintf("%d", user.ID),
		Login:     user.Username,
		Name:      user.Name,
		AvatarURL: user.AvatarURL,
	}
}

// NoteAuthor는 GitLab Note의 Author 타입입니다.
type NoteAuthor struct {
	ID        int    `json:"id"`
	Username  string `json:"username"`
	Email     string `json:"email"`
	Name      string `json:"name"`
	State     string `json:"state"`
	AvatarURL string `json:"avatar_url"`
	WebURL    string `json:"web_url"`
}

// convertNoteAuthor는 GitLab Note Author를 UserInfo로 변환합니다.
func (c *GitLabClient) convertNoteAuthor(author struct {
	ID        int    `json:"id"`
	Username  string `json:"username"`
	Email     string `json:"email"`
	Name      string `json:"name"`
	State     string `json:"state"`
	AvatarURL string `json:"avatar_url"`
	WebURL    string `json:"web_url"`
}) *UserInfo {
	return &UserInfo{
		ID:        fmt.Sprintf("%d", author.ID),
		Login:     author.Username,
		Name:      author.Name,
		AvatarURL: author.AvatarURL,
	}
}
