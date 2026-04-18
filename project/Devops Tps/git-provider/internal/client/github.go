package client

import (
	"context"
	"fmt"
	"time"

	"github.com/google/go-github/v57/github"
	"golang.org/x/oauth2"

	pb "github.com/runners-high/git-provider/pkg/pb/v1"
)

// GitHubClient는 GitHub API 클라이언트입니다.
type GitHubClient struct {
	client *github.Client
}

// NewGitHubClient는 새 GitHub 클라이언트를 생성합니다.
func NewGitHubClient(ctx context.Context, token, baseURL string) (*GitHubClient, error) {
	ts := oauth2.StaticTokenSource(
		&oauth2.Token{AccessToken: token},
	)
	tc := oauth2.NewClient(ctx, ts)

	var client *github.Client
	var err error

	if baseURL != "" {
		// GitHub Enterprise
		client, err = github.NewClient(tc).WithEnterpriseURLs(baseURL, baseURL)
		if err != nil {
			return nil, fmt.Errorf("failed to create GitHub Enterprise client: %w", err)
		}
	} else {
		// Public GitHub
		client = github.NewClient(tc)
	}

	return &GitHubClient{client: client}, nil
}

// =============================================================================
// 저장소 관련 메서드
// =============================================================================

// ListRepositories는 사용자의 저장소 목록을 반환합니다.
func (c *GitHubClient) ListRepositories(ctx context.Context) ([]*pb.Repository, error) {
	// 인증된 사용자의 모든 저장소 조회
	repos, _, err := c.client.Repositories.List(ctx, "", &github.RepositoryListOptions{
		ListOptions: github.ListOptions{PerPage: 100},
	})
	if err != nil {
		return nil, fmt.Errorf("failed to list repositories: %w", err)
	}

	result := make([]*pb.Repository, len(repos))
	for i, repo := range repos {
		result[i] = c.convertRepository(repo)
	}

	return result, nil
}

// GetRepository는 특정 저장소의 상세 정보를 반환합니다.
func (c *GitHubClient) GetRepository(ctx context.Context, owner, repoName string) (*pb.Repository, error) {
	repo, _, err := c.client.Repositories.Get(ctx, owner, repoName)
	if err != nil {
		return nil, fmt.Errorf("failed to get repository: %w", err)
	}

	return c.convertRepository(repo), nil
}

// CreateRepository는 새 저장소를 생성합니다.
func (c *GitHubClient) CreateRepository(ctx context.Context, name, description string, private bool, org string) (*pb.Repository, error) {
	repoReq := &github.Repository{
		Name:        github.String(name),
		Description: github.String(description),
		Private:     github.Bool(private),
		AutoInit:    github.Bool(true),
	}

	var repo *github.Repository
	var err error

	if org != "" {
		// 조직에 저장소 생성
		repo, _, err = c.client.Repositories.Create(ctx, org, repoReq)
	} else {
		// 개인 저장소 생성
		repo, _, err = c.client.Repositories.Create(ctx, "", repoReq)
	}

	if err != nil {
		return nil, fmt.Errorf("failed to create repository: %w", err)
	}

	return c.convertRepository(repo), nil
}

// DeleteRepository는 저장소를 삭제합니다.
func (c *GitHubClient) DeleteRepository(ctx context.Context, owner, repoName string) error {
	_, err := c.client.Repositories.Delete(ctx, owner, repoName)
	if err != nil {
		return fmt.Errorf("failed to delete repository: %w", err)
	}
	return nil
}

// =============================================================================
// 브랜치 관련 메서드
// =============================================================================

// ListBranches는 저장소의 브랜치 목록을 반환합니다.
func (c *GitHubClient) ListBranches(ctx context.Context, owner, repoName string) ([]*pb.Branch, error) {
	branches, _, err := c.client.Repositories.ListBranches(ctx, owner, repoName, &github.BranchListOptions{
		ListOptions: github.ListOptions{PerPage: 100},
	})
	if err != nil {
		return nil, fmt.Errorf("failed to list branches: %w", err)
	}

	// 기본 브랜치 확인을 위해 저장소 정보 조회
	repo, _, err := c.client.Repositories.Get(ctx, owner, repoName)
	if err != nil {
		return nil, fmt.Errorf("failed to get repository for default branch: %w", err)
	}
	defaultBranch := repo.GetDefaultBranch()

	result := make([]*pb.Branch, len(branches))
	for i, branch := range branches {
		result[i] = &pb.Branch{
			Name:      branch.GetName(),
			Sha:       branch.GetCommit().GetSHA(),
			Protected: branch.GetProtected(),
			IsDefault: branch.GetName() == defaultBranch,
		}
	}

	return result, nil
}

// GetBranch는 특정 브랜치의 상세 정보를 반환합니다.
func (c *GitHubClient) GetBranch(ctx context.Context, owner, repoName, branchName string) (*pb.Branch, error) {
	branch, _, err := c.client.Repositories.GetBranch(ctx, owner, repoName, branchName, 0)
	if err != nil {
		return nil, fmt.Errorf("failed to get branch: %w", err)
	}

	// 기본 브랜치 확인
	repo, _, err := c.client.Repositories.Get(ctx, owner, repoName)
	if err != nil {
		return nil, fmt.Errorf("failed to get repository for default branch: %w", err)
	}

	// 커밋 상세 정보 조회
	commit, _, err := c.client.Repositories.GetCommit(ctx, owner, repoName, branch.GetCommit().GetSHA(), nil)
	if err != nil {
		// 커밋 정보 조회 실패해도 브랜치 정보는 반환
		return &pb.Branch{
			Name:      branch.GetName(),
			Sha:       branch.GetCommit().GetSHA(),
			Protected: branch.GetProtected(),
			IsDefault: branch.GetName() == repo.GetDefaultBranch(),
		}, nil
	}

	return &pb.Branch{
		Name:      branch.GetName(),
		Sha:       branch.GetCommit().GetSHA(),
		Protected: branch.GetProtected(),
		IsDefault: branch.GetName() == repo.GetDefaultBranch(),
		LastCommit: &pb.Commit{
			Sha:         commit.GetSHA(),
			Message:     commit.GetCommit().GetMessage(),
			AuthorName:  commit.GetCommit().GetAuthor().GetName(),
			AuthorEmail: commit.GetCommit().GetAuthor().GetEmail(),
			Date:        commit.GetCommit().GetAuthor().GetDate().String(),
		},
	}, nil
}

// CreateBranch는 새 브랜치를 생성합니다.
func (c *GitHubClient) CreateBranch(ctx context.Context, owner, repoName, branchName, ref string) (*pb.Branch, error) {
	// ref가 브랜치명인 경우 SHA를 조회
	var sha string
	if len(ref) != 40 {
		// 브랜치명으로 간주하고 SHA 조회
		branch, _, err := c.client.Repositories.GetBranch(ctx, owner, repoName, ref, 0)
		if err != nil {
			return nil, fmt.Errorf("failed to get ref branch: %w", err)
		}
		sha = branch.GetCommit().GetSHA()
	} else {
		sha = ref
	}

	// Git Reference 생성
	refPath := fmt.Sprintf("refs/heads/%s", branchName)
	gitRef := &github.Reference{
		Ref: github.String(refPath),
		Object: &github.GitObject{
			SHA: github.String(sha),
		},
	}

	_, _, err := c.client.Git.CreateRef(ctx, owner, repoName, gitRef)
	if err != nil {
		return nil, fmt.Errorf("failed to create branch: %w", err)
	}

	// 생성된 브랜치 정보 반환
	return c.GetBranch(ctx, owner, repoName, branchName)
}

// DeleteBranch는 브랜치를 삭제합니다.
func (c *GitHubClient) DeleteBranch(ctx context.Context, owner, repoName, branchName string) error {
	refPath := fmt.Sprintf("refs/heads/%s", branchName)
	_, err := c.client.Git.DeleteRef(ctx, owner, repoName, refPath)
	if err != nil {
		return fmt.Errorf("failed to delete branch: %w", err)
	}
	return nil
}

// =============================================================================
// 헬퍼 메서드
// =============================================================================

// convertRepository는 GitHub Repository를 통합 모델로 변환합니다.
func (c *GitHubClient) convertRepository(repo *github.Repository) *pb.Repository {
	return &pb.Repository{
		Id:            fmt.Sprintf("%d", repo.GetID()),
		Name:          repo.GetName(),
		FullName:      repo.GetFullName(),
		Description:   repo.GetDescription(),
		Url:           repo.GetHTMLURL(),
		CloneUrl:      repo.GetCloneURL(),
		SshUrl:        repo.GetSSHURL(),
		DefaultBranch: repo.GetDefaultBranch(),
		Private:       repo.GetPrivate(),
		CreatedAt:     repo.GetCreatedAt().String(),
		UpdatedAt:     repo.GetUpdatedAt().String(),
		Provider:      pb.ProviderType_PROVIDER_TYPE_GITHUB,
		Namespace:     c.convertOwnerToNamespace(repo.GetOwner()),
	}
}

// convertOwnerToNamespace는 GitHub Owner를 Namespace로 변환합니다.
func (c *GitHubClient) convertOwnerToNamespace(owner *github.User) *pb.Namespace {
	if owner == nil {
		return nil
	}

	nsType := pb.NamespaceType_NAMESPACE_TYPE_UNSPECIFIED
	switch owner.GetType() {
	case "User":
		nsType = pb.NamespaceType_NAMESPACE_TYPE_USER
	case "Organization":
		nsType = pb.NamespaceType_NAMESPACE_TYPE_ORGANIZATION
	}

	return &pb.Namespace{
		Id:        fmt.Sprintf("%d", owner.GetID()),
		Name:      owner.GetLogin(),
		FullPath:  owner.GetLogin(),
		Type:      nsType,
		AvatarUrl: owner.GetAvatarURL(),
		Url:       owner.GetHTMLURL(),
	}
}

// =============================================================================
// 콘텐츠 관련 메서드 (Phase 1.1)
// =============================================================================

// GetTree는 저장소의 파일 트리를 반환합니다.
func (c *GitHubClient) GetTree(ctx context.Context, owner, repoName, ref string, recursive bool) ([]*pb.TreeEntry, string, error) {
	// ref가 비어있으면 기본 브랜치 사용
	if ref == "" {
		repo, _, err := c.client.Repositories.Get(ctx, owner, repoName)
		if err != nil {
			return nil, "", fmt.Errorf("failed to get repository: %w", err)
		}
		ref = repo.GetDefaultBranch()
	}

	// ref에서 SHA 조회 (브랜치명/태그명인 경우)
	sha := ref
	if len(ref) != 40 {
		branch, _, err := c.client.Repositories.GetBranch(ctx, owner, repoName, ref, 0)
		if err != nil {
			return nil, "", fmt.Errorf("failed to get branch: %w", err)
		}
		sha = branch.GetCommit().GetSHA()
	}

	// 트리 조회
	tree, _, err := c.client.Git.GetTree(ctx, owner, repoName, sha, recursive)
	if err != nil {
		return nil, "", fmt.Errorf("failed to get tree: %w", err)
	}

	entries := make([]*pb.TreeEntry, len(tree.Entries))
	for i, entry := range tree.Entries {
		entries[i] = &pb.TreeEntry{
			Path: entry.GetPath(),
			Type: entry.GetType(),
			Sha:  entry.GetSHA(),
			Size: int64(entry.GetSize()),
			Mode: entry.GetMode(),
		}
	}

	truncated := ""
	if tree.GetTruncated() {
		truncated = "true"
	}

	return entries, truncated, nil
}

// GetContents는 특정 경로의 파일/디렉토리 내용을 반환합니다.
func (c *GitHubClient) GetContents(ctx context.Context, owner, repoName, path, ref string) (*pb.ContentEntry, error) {
	opts := &github.RepositoryContentGetOptions{}
	if ref != "" {
		opts.Ref = ref
	}

	fileContent, dirContents, _, err := c.client.Repositories.GetContents(ctx, owner, repoName, path, opts)
	if err != nil {
		return nil, fmt.Errorf("failed to get contents: %w", err)
	}

	// 디렉토리인 경우
	if dirContents != nil {
		entries := make([]*pb.ContentEntry, len(dirContents))
		for i, item := range dirContents {
			entries[i] = c.convertContentItem(item)
		}
		return &pb.ContentEntry{
			Type:    pb.ContentType_CONTENT_TYPE_DIRECTORY,
			Name:    getLastPathSegment(path),
			Path:    path,
			Entries: entries,
		}, nil
	}

	// 파일인 경우
	return c.convertContent(fileContent), nil
}

// GetReadme는 저장소의 README 파일을 반환합니다.
func (c *GitHubClient) GetReadme(ctx context.Context, owner, repoName, ref string) (*pb.ContentEntry, error) {
	opts := &github.RepositoryContentGetOptions{}
	if ref != "" {
		opts.Ref = ref
	}

	readme, _, err := c.client.Repositories.GetReadme(ctx, owner, repoName, opts)
	if err != nil {
		return nil, fmt.Errorf("failed to get readme: %w", err)
	}

	return c.convertContent(readme), nil
}

// convertContent는 GitHub RepositoryContent를 ContentEntry로 변환합니다.
func (c *GitHubClient) convertContent(content *github.RepositoryContent) *pb.ContentEntry {
	contentType := pb.ContentType_CONTENT_TYPE_FILE
	switch content.GetType() {
	case "dir":
		contentType = pb.ContentType_CONTENT_TYPE_DIRECTORY
	case "symlink":
		contentType = pb.ContentType_CONTENT_TYPE_SYMLINK
	case "submodule":
		contentType = pb.ContentType_CONTENT_TYPE_SUBMODULE
	}

	contentStr, _ := content.GetContent()
	return &pb.ContentEntry{
		Type:        contentType,
		Name:        content.GetName(),
		Path:        content.GetPath(),
		Size:        int64(content.GetSize()),
		Sha:         content.GetSHA(),
		Content:     contentStr,
		Encoding:    content.GetEncoding(),
		Url:         content.GetURL(),
		DownloadUrl: content.GetDownloadURL(),
	}
}

// convertContentItem는 디렉토리 내 항목을 변환합니다.
func (c *GitHubClient) convertContentItem(item *github.RepositoryContent) *pb.ContentEntry {
	contentType := pb.ContentType_CONTENT_TYPE_FILE
	switch item.GetType() {
	case "dir":
		contentType = pb.ContentType_CONTENT_TYPE_DIRECTORY
	case "symlink":
		contentType = pb.ContentType_CONTENT_TYPE_SYMLINK
	case "submodule":
		contentType = pb.ContentType_CONTENT_TYPE_SUBMODULE
	}

	return &pb.ContentEntry{
		Type:        contentType,
		Name:        item.GetName(),
		Path:        item.GetPath(),
		Size:        int64(item.GetSize()),
		Sha:         item.GetSHA(),
		Url:         item.GetURL(),
		DownloadUrl: item.GetDownloadURL(),
	}
}

// getLastPathSegment는 경로의 마지막 세그먼트를 반환합니다.
func getLastPathSegment(path string) string {
	if path == "" {
		return ""
	}
	parts := splitPath(path)
	if len(parts) == 0 {
		return ""
	}
	return parts[len(parts)-1]
}

// splitPath는 경로를 분리합니다.
func splitPath(path string) []string {
	var parts []string
	for _, p := range splitString(path, "/") {
		if p != "" {
			parts = append(parts, p)
		}
	}
	return parts
}

// splitString은 문자열을 분리합니다.
func splitString(s, sep string) []string {
	if s == "" {
		return nil
	}
	var result []string
	start := 0
	for i := 0; i < len(s); i++ {
		if string(s[i]) == sep {
			if i > start {
				result = append(result, s[start:i])
			}
			start = i + 1
		}
	}
	if start < len(s) {
		result = append(result, s[start:])
	}
	return result
}

// =============================================================================
// 브랜치 비교 메서드 (Phase 1.2)
// =============================================================================

// BranchComparison은 브랜치 비교 결과입니다.
type BranchComparison struct {
	BaseBranch      string
	CompareBranch   string
	AheadBy         int
	BehindBy        int
	Mergeable       string // "mergeable", "conflicting", "unknown"
	MergeStatus     string
	SuggestedAction string
	BaseSha         string
	CompareSha      string
	MergeBaseSha    string
	FilesChanged    int
	Additions       int
	Deletions       int
}

// CompareBranches는 두 브랜치를 비교합니다.
func (c *GitHubClient) CompareBranches(ctx context.Context, owner, repoName, base, compare string) (*BranchComparison, error) {
	comparison, _, err := c.client.Repositories.CompareCommits(ctx, owner, repoName, base, compare, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to compare branches: %w", err)
	}

	result := &BranchComparison{
		BaseBranch:    base,
		CompareBranch: compare,
		AheadBy:       comparison.GetAheadBy(),
		BehindBy:      comparison.GetBehindBy(),
		MergeStatus:   comparison.GetStatus(),
		MergeBaseSha:  comparison.GetMergeBaseCommit().GetSHA(),
	}

	// base와 compare의 SHA 조회
	baseBranch, _, err := c.client.Repositories.GetBranch(ctx, owner, repoName, base, 0)
	if err == nil {
		result.BaseSha = baseBranch.GetCommit().GetSHA()
	}

	compareBranch, _, err := c.client.Repositories.GetBranch(ctx, owner, repoName, compare, 0)
	if err == nil {
		result.CompareSha = compareBranch.GetCommit().GetSHA()
	}

	// 파일 변경 통계
	if comparison.Files != nil {
		result.FilesChanged = len(comparison.Files)
		for _, file := range comparison.Files {
			result.Additions += file.GetAdditions()
			result.Deletions += file.GetDeletions()
		}
	}

	// 머지 가능 여부 판단
	result.Mergeable = "unknown"
	result.SuggestedAction = determineSuggestedAction(result.AheadBy, result.BehindBy, result.MergeStatus)

	return result, nil
}

// CommitInfo는 커밋 정보입니다.
type CommitInfo struct {
	SHA         string
	Message     string
	AuthorName  string
	AuthorEmail string
	Date        string
}

// ListCommitsDiff는 두 브랜치 간 커밋 차이를 조회합니다.
func (c *GitHubClient) ListCommitsDiff(ctx context.Context, owner, repoName, base, compare string, page, perPage int) ([]*CommitInfo, int, error) {
	if perPage == 0 {
		perPage = 30
	}
	if page == 0 {
		page = 1
	}

	comparison, _, err := c.client.Repositories.CompareCommits(ctx, owner, repoName, base, compare, &github.ListOptions{
		Page:    page,
		PerPage: perPage,
	})
	if err != nil {
		return nil, 0, fmt.Errorf("failed to compare commits: %w", err)
	}

	commits := make([]*CommitInfo, len(comparison.Commits))
	for i, commit := range comparison.Commits {
		commits[i] = &CommitInfo{
			SHA:         commit.GetSHA(),
			Message:     commit.GetCommit().GetMessage(),
			AuthorName:  commit.GetCommit().GetAuthor().GetName(),
			AuthorEmail: commit.GetCommit().GetAuthor().GetEmail(),
			Date:        commit.GetCommit().GetAuthor().GetDate().String(),
		}
	}

	return commits, comparison.GetTotalCommits(), nil
}

// MergedBranchInfo는 머지된 브랜치 정보입니다.
type MergedBranchInfo struct {
	Name          string
	MergedAt      string
	MergedBy      string
	LastCommitSHA string
	MergedInto    string
}

// ListMergedBranches는 기준 브랜치에 머지된 브랜치 목록을 반환합니다.
func (c *GitHubClient) ListMergedBranches(ctx context.Context, owner, repoName, base string) ([]*MergedBranchInfo, error) {
	// GitHub API는 직접 머지된 브랜치 목록을 제공하지 않음
	// 모든 브랜치를 조회하고 base에 머지 가능한지 확인
	branches, _, err := c.client.Repositories.ListBranches(ctx, owner, repoName, &github.BranchListOptions{
		ListOptions: github.ListOptions{PerPage: 100},
	})
	if err != nil {
		return nil, fmt.Errorf("failed to list branches: %w", err)
	}

	var merged []*MergedBranchInfo
	for _, branch := range branches {
		if branch.GetName() == base {
			continue
		}

		// 브랜치가 base에 머지되었는지 확인 (behind_by == 0 && ahead_by == 0)
		comparison, _, err := c.client.Repositories.CompareCommits(ctx, owner, repoName, base, branch.GetName(), nil)
		if err != nil {
			continue
		}

		// 브랜치가 base보다 뒤처지지 않고 앞서지 않으면 머지된 것으로 간주
		// (실제로는 PR 히스토리를 확인해야 정확함)
		if comparison.GetAheadBy() == 0 {
			merged = append(merged, &MergedBranchInfo{
				Name:          branch.GetName(),
				LastCommitSHA: branch.GetCommit().GetSHA(),
				MergedInto:    base,
			})
		}
	}

	return merged, nil
}

// StaleBranchInfo는 오래된 브랜치 정보입니다.
type StaleBranchInfo struct {
	Name           string
	LastCommitSHA  string
	LastCommitDate string
	DaysInactive   int
}

// ListStaleBranches는 오래된 브랜치 목록을 반환합니다.
func (c *GitHubClient) ListStaleBranches(ctx context.Context, owner, repoName string, staleDays int) ([]*StaleBranchInfo, error) {
	if staleDays == 0 {
		staleDays = 30
	}

	branches, _, err := c.client.Repositories.ListBranches(ctx, owner, repoName, &github.BranchListOptions{
		ListOptions: github.ListOptions{PerPage: 100},
	})
	if err != nil {
		return nil, fmt.Errorf("failed to list branches: %w", err)
	}

	var stale []*StaleBranchInfo
	now := time.Now()

	for _, branch := range branches {
		// 커밋 상세 정보 조회
		commit, _, err := c.client.Repositories.GetCommit(ctx, owner, repoName, branch.GetCommit().GetSHA(), nil)
		if err != nil {
			continue
		}

		commitDate := commit.GetCommit().GetAuthor().GetDate()
		daysSince := int(now.Sub(commitDate.Time).Hours() / 24)

		if daysSince >= staleDays {
			stale = append(stale, &StaleBranchInfo{
				Name:           branch.GetName(),
				LastCommitSHA:  branch.GetCommit().GetSHA(),
				LastCommitDate: commitDate.String(),
				DaysInactive:   daysSince,
			})
		}
	}

	return stale, nil
}

// determineSuggestedAction은 권장 작업을 결정합니다.
func determineSuggestedAction(aheadBy, behindBy int, status string) string {
	if aheadBy == 0 && behindBy == 0 {
		return "UP_TO_DATE"
	}
	if status == "diverged" {
		if behindBy > 10 {
			return "REBASE"
		}
		return "MERGE_BASE"
	}
	if aheadBy > 0 && behindBy == 0 {
		return "CREATE_MR"
	}
	if status == "behind" {
		return "MERGE_BASE"
	}
	return "CREATE_MR"
}

// =============================================================================
// Pull Request 메서드 (Phase 1.4)
// =============================================================================

// MergeRequestInfo는 PR 정보입니다.
type MergeRequestInfo struct {
	ID           string
	Number       int
	Title        string
	Description  string
	State        string // "open", "closed", "merged"
	SourceBranch string
	TargetBranch string
	Author       *UserInfo
	Assignees    []*UserInfo
	Reviewers    []*UserInfo
	Labels       []string
	URL          string
	Draft        bool
	Mergeable    bool
	CreatedAt    string
	UpdatedAt    string
	MergedAt     string
	ClosedAt     string
	MergedBy     *UserInfo
	HeadSHA      string
	BaseSHA      string
}

// UserInfo는 사용자 정보입니다.
type UserInfo struct {
	ID        string
	Login     string
	Name      string
	Email     string
	AvatarURL string
}

// ReviewInfo는 리뷰 정보입니다.
type ReviewInfo struct {
	ID          string
	User        *UserInfo
	State       string // "APPROVED", "CHANGES_REQUESTED", "COMMENTED", "PENDING"
	Body        string
	SubmittedAt string
}

// CommentInfo는 댓글 정보입니다.
type CommentInfo struct {
	ID          string
	User        *UserInfo
	Body        string
	Path        string
	Line        int
	CreatedAt   string
	UpdatedAt   string
	InReplyToID string
}

// FileDiffInfo는 파일 변경 정보입니다.
type FileDiffInfo struct {
	Filename         string
	Status           string // "added", "removed", "modified", "renamed"
	Additions        int
	Deletions        int
	Patch            string
	PreviousFilename string
}

// MergeRequestDiffInfo는 MR diff 정보입니다.
type MergeRequestDiffInfo struct {
	Files        []*FileDiffInfo
	Additions    int
	Deletions    int
	ChangedFiles int
}

// ListMergeRequests는 PR 목록을 반환합니다.
func (c *GitHubClient) ListMergeRequests(ctx context.Context, owner, repoName string, state string, page, perPage int) ([]*MergeRequestInfo, int, error) {
	if perPage == 0 {
		perPage = 30
	}
	if page == 0 {
		page = 1
	}

	ghState := "all"
	if state != "" && state != "all" {
		ghState = state
	}

	prs, resp, err := c.client.PullRequests.List(ctx, owner, repoName, &github.PullRequestListOptions{
		State: ghState,
		ListOptions: github.ListOptions{
			Page:    page,
			PerPage: perPage,
		},
	})
	if err != nil {
		return nil, 0, fmt.Errorf("failed to list pull requests: %w", err)
	}

	result := make([]*MergeRequestInfo, len(prs))
	for i, pr := range prs {
		result[i] = c.convertPullRequest(pr)
	}

	totalCount := resp.LastPage * perPage
	if totalCount == 0 {
		totalCount = len(prs)
	}

	return result, totalCount, nil
}

// GetMergeRequest는 PR 상세 정보를 반환합니다.
func (c *GitHubClient) GetMergeRequest(ctx context.Context, owner, repoName string, number int) (*MergeRequestInfo, error) {
	pr, _, err := c.client.PullRequests.Get(ctx, owner, repoName, number)
	if err != nil {
		return nil, fmt.Errorf("failed to get pull request: %w", err)
	}

	return c.convertPullRequest(pr), nil
}

// CreateMergeRequest는 새 PR을 생성합니다.
func (c *GitHubClient) CreateMergeRequest(ctx context.Context, owner, repoName string, title, body, sourceBranch, targetBranch string, draft bool) (*MergeRequestInfo, error) {
	newPR := &github.NewPullRequest{
		Title:               github.String(title),
		Body:                github.String(body),
		Head:                github.String(sourceBranch),
		Base:                github.String(targetBranch),
		MaintainerCanModify: github.Bool(true),
		Draft:               github.Bool(draft),
	}

	pr, _, err := c.client.PullRequests.Create(ctx, owner, repoName, newPR)
	if err != nil {
		return nil, fmt.Errorf("failed to create pull request: %w", err)
	}

	return c.convertPullRequest(pr), nil
}

// UpdateMergeRequest는 PR을 수정합니다.
func (c *GitHubClient) UpdateMergeRequest(ctx context.Context, owner, repoName string, number int, title, body, state, targetBranch string) (*MergeRequestInfo, error) {
	update := &github.PullRequest{}

	if title != "" {
		update.Title = github.String(title)
	}
	if body != "" {
		update.Body = github.String(body)
	}
	if state != "" {
		update.State = github.String(state)
	}
	if targetBranch != "" {
		update.Base = &github.PullRequestBranch{Ref: github.String(targetBranch)}
	}

	pr, _, err := c.client.PullRequests.Edit(ctx, owner, repoName, number, update)
	if err != nil {
		return nil, fmt.Errorf("failed to update pull request: %w", err)
	}

	return c.convertPullRequest(pr), nil
}

// MergeMergeRequest는 PR을 머지합니다.
func (c *GitHubClient) MergeMergeRequest(ctx context.Context, owner, repoName string, number int, commitTitle, commitMessage, mergeMethod string, deleteSourceBranch bool) (*MergeRequestInfo, string, error) {
	opts := &github.PullRequestOptions{}

	switch mergeMethod {
	case "squash":
		opts.MergeMethod = "squash"
	case "rebase":
		opts.MergeMethod = "rebase"
	default:
		opts.MergeMethod = "merge"
	}

	if commitTitle != "" {
		opts.CommitTitle = commitTitle
	}

	result, _, err := c.client.PullRequests.Merge(ctx, owner, repoName, number, commitMessage, opts)
	if err != nil {
		return nil, "", fmt.Errorf("failed to merge pull request: %w", err)
	}

	// 소스 브랜치 삭제
	if deleteSourceBranch && result.GetMerged() {
		pr, _, _ := c.client.PullRequests.Get(ctx, owner, repoName, number)
		if pr != nil && pr.Head != nil {
			refPath := fmt.Sprintf("refs/heads/%s", pr.Head.GetRef())
			c.client.Git.DeleteRef(ctx, owner, repoName, refPath)
		}
	}

	// 머지된 PR 정보 반환
	pr, _, _ := c.client.PullRequests.Get(ctx, owner, repoName, number)
	return c.convertPullRequest(pr), result.GetSHA(), nil
}

// GetMergeRequestDiff는 PR의 변경사항을 반환합니다.
func (c *GitHubClient) GetMergeRequestDiff(ctx context.Context, owner, repoName string, number int) (*MergeRequestDiffInfo, error) {
	files, _, err := c.client.PullRequests.ListFiles(ctx, owner, repoName, number, &github.ListOptions{PerPage: 100})
	if err != nil {
		return nil, fmt.Errorf("failed to get pull request files: %w", err)
	}

	diff := &MergeRequestDiffInfo{
		Files:        make([]*FileDiffInfo, len(files)),
		ChangedFiles: len(files),
	}

	for i, file := range files {
		diff.Files[i] = &FileDiffInfo{
			Filename:         file.GetFilename(),
			Status:           file.GetStatus(),
			Additions:        file.GetAdditions(),
			Deletions:        file.GetDeletions(),
			Patch:            file.GetPatch(),
			PreviousFilename: file.GetPreviousFilename(),
		}
		diff.Additions += file.GetAdditions()
		diff.Deletions += file.GetDeletions()
	}

	return diff, nil
}

// ListReviews는 PR 리뷰 목록을 반환합니다.
func (c *GitHubClient) ListReviews(ctx context.Context, owner, repoName string, number int) ([]*ReviewInfo, error) {
	reviews, _, err := c.client.PullRequests.ListReviews(ctx, owner, repoName, number, &github.ListOptions{PerPage: 100})
	if err != nil {
		return nil, fmt.Errorf("failed to list reviews: %w", err)
	}

	result := make([]*ReviewInfo, len(reviews))
	for i, review := range reviews {
		result[i] = &ReviewInfo{
			ID:          fmt.Sprintf("%d", review.GetID()),
			User:        c.convertUser(review.GetUser()),
			State:       review.GetState(),
			Body:        review.GetBody(),
			SubmittedAt: review.GetSubmittedAt().String(),
		}
	}

	return result, nil
}

// SubmitReview는 PR 리뷰를 제출합니다.
func (c *GitHubClient) SubmitReview(ctx context.Context, owner, repoName string, number int, state, body string) (*ReviewInfo, error) {
	event := "COMMENT"
	switch state {
	case "APPROVED":
		event = "APPROVE"
	case "CHANGES_REQUESTED":
		event = "REQUEST_CHANGES"
	}

	review, _, err := c.client.PullRequests.CreateReview(ctx, owner, repoName, number, &github.PullRequestReviewRequest{
		Body:  github.String(body),
		Event: github.String(event),
	})
	if err != nil {
		return nil, fmt.Errorf("failed to submit review: %w", err)
	}

	return &ReviewInfo{
		ID:          fmt.Sprintf("%d", review.GetID()),
		User:        c.convertUser(review.GetUser()),
		State:       review.GetState(),
		Body:        review.GetBody(),
		SubmittedAt: review.GetSubmittedAt().String(),
	}, nil
}

// ListComments는 PR 댓글 목록을 반환합니다.
func (c *GitHubClient) ListComments(ctx context.Context, owner, repoName string, number int) ([]*CommentInfo, error) {
	comments, _, err := c.client.PullRequests.ListComments(ctx, owner, repoName, number, &github.PullRequestListCommentsOptions{
		ListOptions: github.ListOptions{PerPage: 100},
	})
	if err != nil {
		return nil, fmt.Errorf("failed to list comments: %w", err)
	}

	result := make([]*CommentInfo, len(comments))
	for i, comment := range comments {
		result[i] = &CommentInfo{
			ID:          fmt.Sprintf("%d", comment.GetID()),
			User:        c.convertUser(comment.GetUser()),
			Body:        comment.GetBody(),
			Path:        comment.GetPath(),
			Line:        comment.GetLine(),
			CreatedAt:   comment.GetCreatedAt().String(),
			UpdatedAt:   comment.GetUpdatedAt().String(),
			InReplyToID: fmt.Sprintf("%d", comment.GetInReplyTo()),
		}
	}

	return result, nil
}

// CreateComment는 PR 댓글을 생성합니다.
func (c *GitHubClient) CreateComment(ctx context.Context, owner, repoName string, number int, body, path string, line int, commitID string) (*CommentInfo, error) {
	var comment *github.PullRequestComment
	var err error

	if path != "" && line > 0 {
		// 라인 코멘트
		comment, _, err = c.client.PullRequests.CreateComment(ctx, owner, repoName, number, &github.PullRequestComment{
			Body:     github.String(body),
			Path:     github.String(path),
			Line:     github.Int(line),
			CommitID: github.String(commitID),
		})
	} else {
		// 일반 코멘트 (Issue Comment)
		issueComment, _, err := c.client.Issues.CreateComment(ctx, owner, repoName, number, &github.IssueComment{
			Body: github.String(body),
		})
		if err != nil {
			return nil, fmt.Errorf("failed to create comment: %w", err)
		}
		return &CommentInfo{
			ID:        fmt.Sprintf("%d", issueComment.GetID()),
			User:      c.convertUser(issueComment.GetUser()),
			Body:      issueComment.GetBody(),
			CreatedAt: issueComment.GetCreatedAt().String(),
			UpdatedAt: issueComment.GetUpdatedAt().String(),
		}, nil
	}

	if err != nil {
		return nil, fmt.Errorf("failed to create review comment: %w", err)
	}

	return &CommentInfo{
		ID:        fmt.Sprintf("%d", comment.GetID()),
		User:      c.convertUser(comment.GetUser()),
		Body:      comment.GetBody(),
		Path:      comment.GetPath(),
		Line:      comment.GetLine(),
		CreatedAt: comment.GetCreatedAt().String(),
		UpdatedAt: comment.GetUpdatedAt().String(),
	}, nil
}

// UpdateComment는 PR 댓글을 수정합니다.
func (c *GitHubClient) UpdateComment(ctx context.Context, owner, repoName string, commentID int64, body string) (*CommentInfo, error) {
	comment, _, err := c.client.PullRequests.EditComment(ctx, owner, repoName, commentID, &github.PullRequestComment{
		Body: github.String(body),
	})
	if err != nil {
		return nil, fmt.Errorf("failed to update comment: %w", err)
	}

	return &CommentInfo{
		ID:        fmt.Sprintf("%d", comment.GetID()),
		User:      c.convertUser(comment.GetUser()),
		Body:      comment.GetBody(),
		Path:      comment.GetPath(),
		Line:      comment.GetLine(),
		CreatedAt: comment.GetCreatedAt().String(),
		UpdatedAt: comment.GetUpdatedAt().String(),
	}, nil
}

// DeleteComment는 PR 댓글을 삭제합니다.
func (c *GitHubClient) DeleteComment(ctx context.Context, owner, repoName string, commentID int64) error {
	_, err := c.client.PullRequests.DeleteComment(ctx, owner, repoName, commentID)
	if err != nil {
		return fmt.Errorf("failed to delete comment: %w", err)
	}
	return nil
}

// convertPullRequest는 GitHub PR을 MergeRequestInfo로 변환합니다.
func (c *GitHubClient) convertPullRequest(pr *github.PullRequest) *MergeRequestInfo {
	if pr == nil {
		return nil
	}

	state := "open"
	if pr.GetMerged() {
		state = "merged"
	} else if pr.GetState() == "closed" {
		state = "closed"
	}

	mr := &MergeRequestInfo{
		ID:           fmt.Sprintf("%d", pr.GetID()),
		Number:       pr.GetNumber(),
		Title:        pr.GetTitle(),
		Description:  pr.GetBody(),
		State:        state,
		SourceBranch: pr.GetHead().GetRef(),
		TargetBranch: pr.GetBase().GetRef(),
		Author:       c.convertUser(pr.GetUser()),
		URL:          pr.GetHTMLURL(),
		Draft:        pr.GetDraft(),
		Mergeable:    pr.GetMergeable(),
		CreatedAt:    pr.GetCreatedAt().String(),
		UpdatedAt:    pr.GetUpdatedAt().String(),
		HeadSHA:      pr.GetHead().GetSHA(),
		BaseSHA:      pr.GetBase().GetSHA(),
	}

	if !pr.GetMergedAt().IsZero() {
		mr.MergedAt = pr.GetMergedAt().String()
	}
	if !pr.GetClosedAt().IsZero() {
		mr.ClosedAt = pr.GetClosedAt().String()
	}
	if pr.GetMergedBy() != nil {
		mr.MergedBy = c.convertUser(pr.GetMergedBy())
	}

	// 담당자
	if pr.Assignees != nil {
		mr.Assignees = make([]*UserInfo, len(pr.Assignees))
		for i, a := range pr.Assignees {
			mr.Assignees[i] = c.convertUser(a)
		}
	}

	// 리뷰어
	if pr.RequestedReviewers != nil {
		mr.Reviewers = make([]*UserInfo, len(pr.RequestedReviewers))
		for i, r := range pr.RequestedReviewers {
			mr.Reviewers[i] = c.convertUser(r)
		}
	}

	// 라벨
	if pr.Labels != nil {
		mr.Labels = make([]string, len(pr.Labels))
		for i, l := range pr.Labels {
			mr.Labels[i] = l.GetName()
		}
	}

	return mr
}

// convertUser는 GitHub User를 UserInfo로 변환합니다.
func (c *GitHubClient) convertUser(user *github.User) *UserInfo {
	if user == nil {
		return nil
	}
	return &UserInfo{
		ID:        fmt.Sprintf("%d", user.GetID()),
		Login:     user.GetLogin(),
		Name:      user.GetName(),
		Email:     user.GetEmail(),
		AvatarURL: user.GetAvatarURL(),
	}
}
