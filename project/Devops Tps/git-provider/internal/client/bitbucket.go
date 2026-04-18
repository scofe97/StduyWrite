package client

import (
	"context"
	"encoding/base64"
	"fmt"
	"regexp"
	"strings"
	"time"

	"github.com/ktrysmt/go-bitbucket"

	pb "github.com/runners-high/git-provider/pkg/pb/v1"
)

// BitbucketClient는 Bitbucket API 클라이언트입니다.
type BitbucketClient struct {
	client    *bitbucket.Client
	workspace string
}

// NewBitbucketClient는 API Token을 사용하여 새 Bitbucket 클라이언트를 생성합니다.
// Bitbucket API Token은 Basic Auth로 사용: email (username), api_token (password)
func NewBitbucketClient(email, apiToken, workspace string) (*BitbucketClient, error) {
	client, err := bitbucket.NewBasicAuth(email, apiToken)
	if err != nil {
		return nil, fmt.Errorf("failed to create bitbucket client: %w", err)
	}

	return &BitbucketClient{
		client:    client,
		workspace: workspace,
	}, nil
}

// =============================================================================
// 저장소 관련 메서드
// =============================================================================

// ListRepositories는 사용자의 저장소 목록을 반환합니다.
func (c *BitbucketClient) ListRepositories(ctx context.Context) ([]*pb.Repository, error) {
	if c.workspace == "" {
		return nil, fmt.Errorf("workspace is required for listing repositories")
	}

	repos, err := c.client.Repositories.ListForAccount(&bitbucket.RepositoriesOptions{
		Owner: c.workspace,
	})
	if err != nil {
		return nil, fmt.Errorf("failed to list repositories: %w", err)
	}

	result := make([]*pb.Repository, 0)
	for _, repo := range repos.Items {
		result = append(result, c.convertRepository(&repo))
	}

	return result, nil
}

// GetRepository는 특정 저장소의 상세 정보를 반환합니다.
func (c *BitbucketClient) GetRepository(ctx context.Context, repoSlug string) (*pb.Repository, error) {
	repo, err := c.client.Repositories.Repository.Get(&bitbucket.RepositoryOptions{
		Owner:    c.workspace,
		RepoSlug: repoSlug,
	})
	if err != nil {
		return nil, fmt.Errorf("failed to get repository: %w", err)
	}

	return c.convertRepositoryFromGet(repo), nil
}

// CreateRepository는 새 저장소를 생성합니다.
func (c *BitbucketClient) CreateRepository(ctx context.Context, name, description string, private bool) (*pb.Repository, error) {
	isPrivate := "false"
	if private {
		isPrivate = "true"
	}

	repo, err := c.client.Repositories.Repository.Create(&bitbucket.RepositoryOptions{
		Owner:       c.workspace,
		RepoSlug:    name,
		Description: description,
		IsPrivate:   isPrivate,
	})
	if err != nil {
		return nil, fmt.Errorf("failed to create repository: %w", err)
	}

	return c.convertRepositoryFromGet(repo), nil
}

// DeleteRepository는 저장소를 삭제합니다.
func (c *BitbucketClient) DeleteRepository(ctx context.Context, repoSlug string) error {
	_, err := c.client.Repositories.Repository.Delete(&bitbucket.RepositoryOptions{
		Owner:    c.workspace,
		RepoSlug: repoSlug,
	})
	if err != nil {
		return fmt.Errorf("failed to delete repository: %w", err)
	}
	return nil
}

// =============================================================================
// 브랜치 관련 메서드
// =============================================================================

// ListBranches는 저장소의 브랜치 목록을 반환합니다.
func (c *BitbucketClient) ListBranches(ctx context.Context, repoSlug string) ([]*pb.Branch, error) {
	// 기본 브랜치 확인을 위해 저장소 정보 조회
	repo, err := c.client.Repositories.Repository.Get(&bitbucket.RepositoryOptions{
		Owner:    c.workspace,
		RepoSlug: repoSlug,
	})
	if err != nil {
		return nil, fmt.Errorf("failed to get repository for default branch: %w", err)
	}
	defaultBranch := getMainbranchName(repo)

	branches, err := c.client.Repositories.Repository.ListBranches(&bitbucket.RepositoryBranchOptions{
		Owner:    c.workspace,
		RepoSlug: repoSlug,
	})
	if err != nil {
		return nil, fmt.Errorf("failed to list branches: %w", err)
	}

	result := make([]*pb.Branch, 0, len(branches.Branches))
	for _, branch := range branches.Branches {
		result = append(result, c.convertBranch(&branch, defaultBranch))
	}

	return result, nil
}

// GetBranch는 특정 브랜치의 상세 정보를 반환합니다.
func (c *BitbucketClient) GetBranch(ctx context.Context, repoSlug, branchName string) (*pb.Branch, error) {
	// 기본 브랜치 확인
	repo, err := c.client.Repositories.Repository.Get(&bitbucket.RepositoryOptions{
		Owner:    c.workspace,
		RepoSlug: repoSlug,
	})
	if err != nil {
		return nil, fmt.Errorf("failed to get repository for default branch: %w", err)
	}
	defaultBranch := getMainbranchName(repo)

	branch, err := c.client.Repositories.Repository.GetBranch(&bitbucket.RepositoryBranchOptions{
		Owner:      c.workspace,
		RepoSlug:   repoSlug,
		BranchName: branchName,
	})
	if err != nil {
		return nil, fmt.Errorf("failed to get branch: %w", err)
	}

	return c.convertBranch(branch, defaultBranch), nil
}

// CreateBranch는 새 브랜치를 생성합니다.
func (c *BitbucketClient) CreateBranch(ctx context.Context, repoSlug, branchName, ref string) (*pb.Branch, error) {
	// ref가 브랜치명인 경우 SHA를 조회
	var sha string
	if len(ref) != 40 {
		// 브랜치에서 SHA 조회
		branch, err := c.client.Repositories.Repository.GetBranch(&bitbucket.RepositoryBranchOptions{
			Owner:      c.workspace,
			RepoSlug:   repoSlug,
			BranchName: ref,
		})
		if err != nil {
			return nil, fmt.Errorf("failed to get ref branch: %w", err)
		}
		// Target에서 hash 추출
		if target := branch.Target; target != nil {
			if hash, ok := target["hash"].(string); ok {
				sha = hash
			}
		}
		if sha == "" {
			return nil, fmt.Errorf("failed to get SHA from ref branch")
		}
	} else {
		sha = ref
	}

	_, err := c.client.Repositories.Repository.CreateBranch(&bitbucket.RepositoryBranchCreationOptions{
		Owner:    c.workspace,
		RepoSlug: repoSlug,
		Name:     branchName,
		Target: bitbucket.RepositoryBranchTarget{
			Hash: sha,
		},
	})
	if err != nil {
		return nil, fmt.Errorf("failed to create branch: %w", err)
	}

	return c.GetBranch(ctx, repoSlug, branchName)
}

// DeleteBranch는 브랜치를 삭제합니다.
func (c *BitbucketClient) DeleteBranch(ctx context.Context, repoSlug, branchName string) error {
	err := c.client.Repositories.Repository.DeleteBranch(&bitbucket.RepositoryBranchDeleteOptions{
		Owner:    c.workspace,
		RepoSlug: repoSlug,
		RefName:  branchName,
	})
	if err != nil {
		return fmt.Errorf("failed to delete branch: %w", err)
	}
	return nil
}

// =============================================================================
// 헬퍼 메서드
// =============================================================================

// convertRepository는 Bitbucket Repository를 통합 모델로 변환합니다.
func (c *BitbucketClient) convertRepository(repo *bitbucket.Repository) *pb.Repository {
	defaultBranch := ""
	if repo.Mainbranch.Name != "" {
		defaultBranch = repo.Mainbranch.Name
	}

	cloneURL := extractCloneURL(repo.Links, "https")
	sshURL := extractCloneURL(repo.Links, "ssh")
	htmlURL := extractLinkHref(repo.Links, "html")

	return &pb.Repository{
		Id:            repo.Uuid,
		Name:          repo.Name,
		FullName:      repo.Full_name,
		Description:   repo.Description,
		Url:           htmlURL,
		CloneUrl:      cloneURL,
		SshUrl:        sshURL,
		DefaultBranch: defaultBranch,
		Private:       repo.Is_private,
		CreatedAt:     repo.CreatedOn,
		UpdatedAt:     repo.UpdatedOn,
		Provider:      pb.ProviderType_PROVIDER_TYPE_BITBUCKET,
		Namespace:     c.createWorkspaceNamespace(),
	}
}

// convertRepositoryFromGet는 Get 응답을 통합 모델로 변환합니다.
func (c *BitbucketClient) convertRepositoryFromGet(repo *bitbucket.Repository) *pb.Repository {
	return c.convertRepository(repo)
}

// createWorkspaceNamespace는 현재 workspace 정보로 Namespace를 생성합니다.
func (c *BitbucketClient) createWorkspaceNamespace() *pb.Namespace {
	return &pb.Namespace{
		Id:       c.workspace,
		Name:     c.workspace,
		FullPath: c.workspace,
		Type:     pb.NamespaceType_NAMESPACE_TYPE_WORKSPACE,
		// AvatarUrl과 Url은 별도 API 호출 필요
	}
}

// convertBranch는 Bitbucket RepositoryBranch를 통합 모델로 변환합니다.
func (c *BitbucketClient) convertBranch(branch *bitbucket.RepositoryBranch, defaultBranch string) *pb.Branch {
	var sha string
	var lastCommit *pb.Commit

	if target := branch.Target; target != nil {
		sha, _ = target["hash"].(string)
		message, _ := target["message"].(string)
		date, _ := target["date"].(string)

		var authorName, authorEmail string
		if author, ok := target["author"].(map[string]interface{}); ok {
			raw, _ := author["raw"].(string)
			authorName, authorEmail = parseAuthor(raw)
		}

		lastCommit = &pb.Commit{
			Sha:         sha,
			Message:     message,
			AuthorName:  authorName,
			AuthorEmail: authorEmail,
			Date:        date,
		}
	}

	return &pb.Branch{
		Name:       branch.Name,
		Sha:        sha,
		Protected:  false, // Bitbucket은 별도 API로 확인 필요
		IsDefault:  branch.Name == defaultBranch,
		LastCommit: lastCommit,
	}
}

// extractCloneURL은 links에서 clone URL을 추출합니다.
func extractCloneURL(links map[string]interface{}, protocol string) string {
	if cloneLinks, ok := links["clone"].([]interface{}); ok {
		for _, link := range cloneLinks {
			if linkMap, ok := link.(map[string]interface{}); ok {
				if name, _ := linkMap["name"].(string); name == protocol {
					href, _ := linkMap["href"].(string)
					return href
				}
			}
		}
	}
	return ""
}

// extractLinkHref는 links에서 특정 키의 href를 추출합니다.
func extractLinkHref(links map[string]interface{}, key string) string {
	if linkObj, ok := links[key].(map[string]interface{}); ok {
		href, _ := linkObj["href"].(string)
		return href
	}
	return ""
}

// getMainbranchName는 저장소에서 기본 브랜치명을 추출합니다.
func getMainbranchName(repo *bitbucket.Repository) string {
	if repo != nil && repo.Mainbranch.Name != "" {
		return repo.Mainbranch.Name
	}
	return "main"
}

// parseAuthor는 "Name <email>" 형태의 문자열을 파싱합니다.
var authorRegex = regexp.MustCompile(`^(.+?)\s*<(.+?)>$`)

func parseAuthor(raw string) (name, email string) {
	matches := authorRegex.FindStringSubmatch(raw)
	if len(matches) == 3 {
		return strings.TrimSpace(matches[1]), matches[2]
	}
	return raw, ""
}

// =============================================================================
// 콘텐츠 관련 메서드 (Phase 1.1)
// =============================================================================

// GetTree는 저장소의 파일 트리를 반환합니다.
func (c *BitbucketClient) GetTree(ctx context.Context, repoSlug, ref string, recursive bool) ([]*pb.TreeEntry, error) {
	// ref가 비어있으면 기본 브랜치 사용
	if ref == "" {
		repo, err := c.client.Repositories.Repository.Get(&bitbucket.RepositoryOptions{
			Owner:    c.workspace,
			RepoSlug: repoSlug,
		})
		if err != nil {
			return nil, fmt.Errorf("failed to get repository: %w", err)
		}
		ref = getMainbranchName(repo)
	}

	// Bitbucket은 src endpoint로 디렉토리 내용 조회
	// 재귀적으로 전체 트리를 가져오려면 반복 호출 필요
	return c.getTreeRecursive(ctx, repoSlug, ref, "", recursive)
}

// getTreeRecursive는 재귀적으로 트리를 조회합니다.
func (c *BitbucketClient) getTreeRecursive(ctx context.Context, repoSlug, ref, path string, recursive bool) ([]*pb.TreeEntry, error) {
	srcPath := ref
	if path != "" {
		srcPath = ref + "/" + path
	}

	contents, err := c.client.Repositories.Repository.ListFiles(&bitbucket.RepositoryFilesOptions{
		Owner:    c.workspace,
		RepoSlug: repoSlug,
		Ref:      srcPath,
	})
	if err != nil {
		return nil, fmt.Errorf("failed to list files: %w", err)
	}

	var entries []*pb.TreeEntry

	// contents는 []RepositoryFile 타입
	for _, item := range contents {
		entryType := "blob"
		if item.Type == "commit_directory" {
			entryType = "tree"
		}

		entry := &pb.TreeEntry{
			Path: item.Path,
			Type: entryType,
			Size: int64(item.Size),
		}
		entries = append(entries, entry)

		// 재귀 옵션이고 디렉토리인 경우
		if recursive && entryType == "tree" {
			subEntries, err := c.getTreeRecursive(ctx, repoSlug, ref, item.Path, true)
			if err == nil {
				entries = append(entries, subEntries...)
			}
		}
	}

	return entries, nil
}

// GetContents는 특정 경로의 파일/디렉토리 내용을 반환합니다.
func (c *BitbucketClient) GetContents(ctx context.Context, repoSlug, path, ref string) (*pb.ContentEntry, error) {
	// ref가 비어있으면 기본 브랜치 사용
	if ref == "" {
		repo, err := c.client.Repositories.Repository.Get(&bitbucket.RepositoryOptions{
			Owner:    c.workspace,
			RepoSlug: repoSlug,
		})
		if err != nil {
			return nil, fmt.Errorf("failed to get repository: %w", err)
		}
		ref = getMainbranchName(repo)
	}

	srcPath := ref
	if path != "" {
		srcPath = ref + "/" + path
	}

	// 먼저 파일 내용 조회 시도
	fileContent, err := c.client.Repositories.Repository.GetFileContent(&bitbucket.RepositoryFilesOptions{
		Owner:    c.workspace,
		RepoSlug: repoSlug,
		Ref:      srcPath,
	})
	if err == nil && fileContent != nil {
		// fileContent는 []byte 타입
		content := base64.StdEncoding.EncodeToString(fileContent)
		return &pb.ContentEntry{
			Type:     pb.ContentType_CONTENT_TYPE_FILE,
			Name:     extractFileName(path),
			Path:     path,
			Content:  content,
			Encoding: "base64",
		}, nil
	}

	// 디렉토리로 시도
	dirContents, err := c.client.Repositories.Repository.ListFiles(&bitbucket.RepositoryFilesOptions{
		Owner:    c.workspace,
		RepoSlug: repoSlug,
		Ref:      srcPath,
	})
	if err != nil {
		return nil, fmt.Errorf("failed to get contents: %w", err)
	}

	var entries []*pb.ContentEntry
	// dirContents는 []RepositoryFile 타입
	for _, item := range dirContents {
		contentType := pb.ContentType_CONTENT_TYPE_FILE
		if item.Type == "commit_directory" {
			contentType = pb.ContentType_CONTENT_TYPE_DIRECTORY
		}

		entries = append(entries, &pb.ContentEntry{
			Type: contentType,
			Name: extractFileName(item.Path),
			Path: item.Path,
			Size: int64(item.Size),
		})
	}

	return &pb.ContentEntry{
		Type:    pb.ContentType_CONTENT_TYPE_DIRECTORY,
		Name:    extractFileName(path),
		Path:    path,
		Entries: entries,
	}, nil
}

// GetReadme는 저장소의 README 파일을 반환합니다.
func (c *BitbucketClient) GetReadme(ctx context.Context, repoSlug, ref string) (*pb.ContentEntry, error) {
	// README 파일명 후보
	readmeNames := []string{"README.md", "README.MD", "readme.md", "README", "README.txt"}

	for _, name := range readmeNames {
		content, err := c.GetContents(ctx, repoSlug, name, ref)
		if err == nil && content.Type == pb.ContentType_CONTENT_TYPE_FILE {
			return content, nil
		}
	}

	return nil, fmt.Errorf("README not found")
}

// extractFileName는 경로에서 파일명을 추출합니다.
func extractFileName(path string) string {
	if path == "" {
		return ""
	}
	// 끝의 / 제거
	path = strings.TrimSuffix(path, "/")
	// 마지막 / 이후 부분
	idx := strings.LastIndex(path, "/")
	if idx >= 0 {
		return path[idx+1:]
	}
	return path
}

// =============================================================================
// 브랜치 비교 메서드 (Phase 1.2)
// =============================================================================

// CompareBranches는 두 브랜치를 비교합니다.
func (c *BitbucketClient) CompareBranches(ctx context.Context, repoSlug, base, compare string) (*BranchComparison, error) {
	// Bitbucket API로 커밋 비교
	// spec 형식: base..compare
	spec := base + ".." + compare

	diffstat, err := c.client.Repositories.Diff.GetDiffStat(&bitbucket.DiffStatOptions{
		Owner:    c.workspace,
		RepoSlug: repoSlug,
		Spec:     spec,
	})
	if err != nil {
		return nil, fmt.Errorf("failed to get diffstat: %w", err)
	}

	result := &BranchComparison{
		BaseBranch:    base,
		CompareBranch: compare,
	}

	// diffstat에서 파일 변경 정보 추출
	if diffstat != nil && diffstat.DiffStats != nil {
		result.FilesChanged = len(diffstat.DiffStats)
		for _, item := range diffstat.DiffStats {
			result.Additions += item.LinedAdded
			result.Deletions += item.LinesRemoved
		}
	}

	// 브랜치 SHA 조회
	baseBranch, err := c.client.Repositories.Repository.GetBranch(&bitbucket.RepositoryBranchOptions{
		Owner:      c.workspace,
		RepoSlug:   repoSlug,
		BranchName: base,
	})
	if err == nil && baseBranch.Target != nil {
		if hash, ok := baseBranch.Target["hash"].(string); ok {
			result.BaseSha = hash
		}
	}

	compareBranch, err := c.client.Repositories.Repository.GetBranch(&bitbucket.RepositoryBranchOptions{
		Owner:      c.workspace,
		RepoSlug:   repoSlug,
		BranchName: compare,
	})
	if err == nil && compareBranch.Target != nil {
		if hash, ok := compareBranch.Target["hash"].(string); ok {
			result.CompareSha = hash
		}
	}

	// ahead/behind 계산을 위해 커밋 조회
	commits, err := c.getCommitsBetween(ctx, repoSlug, base, compare)
	if err == nil {
		result.AheadBy = len(commits)
	}

	reverseCommits, err := c.getCommitsBetween(ctx, repoSlug, compare, base)
	if err == nil {
		result.BehindBy = len(reverseCommits)
	}

	// 머지 상태 판단
	result.Mergeable = "unknown"
	result.MergeStatus = determineMergeStatus(result.AheadBy, result.BehindBy)
	result.SuggestedAction = determineSuggestedAction(result.AheadBy, result.BehindBy, result.MergeStatus)

	return result, nil
}

// getCommitsBetween은 두 브랜치 사이의 커밋을 조회합니다.
func (c *BitbucketClient) getCommitsBetween(ctx context.Context, repoSlug, base, compare string) ([]map[string]interface{}, error) {
	commits, err := c.client.Repositories.Commits.GetCommits(&bitbucket.CommitsOptions{
		Owner:       c.workspace,
		RepoSlug:    repoSlug,
		Branchortag: compare,
		Exclude:     base,
	})
	if err != nil {
		return nil, err
	}

	var result []map[string]interface{}
	if values, ok := commits.(map[string]interface{})["values"].([]interface{}); ok {
		for _, v := range values {
			if commit, ok := v.(map[string]interface{}); ok {
				result = append(result, commit)
			}
		}
	}
	return result, nil
}

// ListCommitsDiff는 두 브랜치 간 커밋 차이를 조회합니다.
func (c *BitbucketClient) ListCommitsDiff(ctx context.Context, repoSlug, base, compare string, page, perPage int) ([]*CommitInfo, int, error) {
	if perPage == 0 {
		perPage = 30
	}
	if page == 0 {
		page = 1
	}

	commits, err := c.getCommitsBetween(ctx, repoSlug, base, compare)
	if err != nil {
		return nil, 0, fmt.Errorf("failed to get commits: %w", err)
	}

	totalCount := len(commits)

	// 페이징 적용
	start := (page - 1) * perPage
	end := start + perPage
	if start >= totalCount {
		return []*CommitInfo{}, totalCount, nil
	}
	if end > totalCount {
		end = totalCount
	}

	result := make([]*CommitInfo, 0, end-start)
	for i := start; i < end; i++ {
		commit := commits[i]
		hash, _ := commit["hash"].(string)
		message, _ := commit["message"].(string)
		date, _ := commit["date"].(string)

		var authorName, authorEmail string
		if author, ok := commit["author"].(map[string]interface{}); ok {
			raw, _ := author["raw"].(string)
			authorName, authorEmail = parseAuthor(raw)
		}

		result = append(result, &CommitInfo{
			SHA:         hash,
			Message:     message,
			AuthorName:  authorName,
			AuthorEmail: authorEmail,
			Date:        date,
		})
	}

	return result, totalCount, nil
}

// ListMergedBranches는 기준 브랜치에 머지된 브랜치 목록을 반환합니다.
func (c *BitbucketClient) ListMergedBranches(ctx context.Context, repoSlug, base string) ([]*MergedBranchInfo, error) {
	// Bitbucket에서 머지된 PR 목록을 통해 머지된 브랜치 확인
	prs, err := c.client.Repositories.PullRequests.Gets(&bitbucket.PullRequestsOptions{
		Owner:    c.workspace,
		RepoSlug: repoSlug,
		States:   []string{"MERGED"},
	})
	if err != nil {
		return nil, fmt.Errorf("failed to list pull requests: %w", err)
	}

	merged := make([]*MergedBranchInfo, 0)
	seenBranches := make(map[string]bool)

	if values, ok := prs.(map[string]interface{})["values"].([]interface{}); ok {
		for _, v := range values {
			pr, ok := v.(map[string]interface{})
			if !ok {
				continue
			}

			// destination (target) 브랜치 확인
			destBranch := ""
			if dest, ok := pr["destination"].(map[string]interface{}); ok {
				if branch, ok := dest["branch"].(map[string]interface{}); ok {
					destBranch, _ = branch["name"].(string)
				}
			}

			// base 브랜치가 아니면 스킵
			if destBranch != base {
				continue
			}

			// source 브랜치 정보
			sourceBranch := ""
			if source, ok := pr["source"].(map[string]interface{}); ok {
				if branch, ok := source["branch"].(map[string]interface{}); ok {
					sourceBranch, _ = branch["name"].(string)
				}
			}

			if seenBranches[sourceBranch] {
				continue
			}
			seenBranches[sourceBranch] = true

			mergedAt := ""
			if updatedOn, ok := pr["updated_on"].(string); ok {
				mergedAt = updatedOn
			}

			mergedBy := ""
			if author, ok := pr["author"].(map[string]interface{}); ok {
				if nickname, ok := author["nickname"].(string); ok {
					mergedBy = nickname
				}
			}

			commitSha := ""
			if mergeCommit, ok := pr["merge_commit"].(map[string]interface{}); ok {
				if hash, ok := mergeCommit["hash"].(string); ok {
					commitSha = hash
				}
			}

			merged = append(merged, &MergedBranchInfo{
				Name:          sourceBranch,
				MergedAt:      mergedAt,
				MergedBy:      mergedBy,
				LastCommitSHA: commitSha,
				MergedInto:    destBranch,
			})
		}
	}

	return merged, nil
}

// ListStaleBranches는 오래된 브랜치 목록을 반환합니다.
func (c *BitbucketClient) ListStaleBranches(ctx context.Context, repoSlug string, staleDays int) ([]*StaleBranchInfo, error) {
	if staleDays == 0 {
		staleDays = 30
	}

	branches, err := c.client.Repositories.Repository.ListBranches(&bitbucket.RepositoryBranchOptions{
		Owner:    c.workspace,
		RepoSlug: repoSlug,
	})
	if err != nil {
		return nil, fmt.Errorf("failed to list branches: %w", err)
	}

	var stale []*StaleBranchInfo

	for _, branch := range branches.Branches {
		if branch.Target == nil {
			continue
		}

		date, _ := branch.Target["date"].(string)
		hash, _ := branch.Target["hash"].(string)

		// 날짜 파싱 및 일수 계산
		daysSince := calculateDaysSince(date)

		if daysSince >= staleDays {
			stale = append(stale, &StaleBranchInfo{
				Name:           branch.Name,
				LastCommitSHA:  hash,
				LastCommitDate: date,
				DaysInactive:   daysSince,
			})
		}
	}

	return stale, nil
}

// calculateDaysSince는 날짜 문자열로부터 경과 일수를 계산합니다.
func calculateDaysSince(dateStr string) int {
	if dateStr == "" {
		return 0
	}
	t, err := time.Parse(time.RFC3339, dateStr)
	if err != nil {
		return 0
	}
	return int(time.Since(t).Hours() / 24)
}

// =============================================================================
// Pull Request 메서드 (Phase 1.4)
// =============================================================================

// ListMergeRequests는 PR 목록을 반환합니다.
func (c *BitbucketClient) ListMergeRequests(ctx context.Context, repoSlug string, state string, page, perPage int) ([]*MergeRequestInfo, int, error) {
	states := []string{}
	if state != "" && state != "all" {
		// Bitbucket states: OPEN, MERGED, DECLINED, SUPERSEDED
		states = append(states, strings.ToUpper(state))
	}

	prs, err := c.client.Repositories.PullRequests.Gets(&bitbucket.PullRequestsOptions{
		Owner:    c.workspace,
		RepoSlug: repoSlug,
		States:   states,
	})
	if err != nil {
		return nil, 0, fmt.Errorf("failed to list pull requests: %w", err)
	}

	var result []*MergeRequestInfo
	totalCount := 0

	if prMap, ok := prs.(map[string]interface{}); ok {
		if size, ok := prMap["size"].(float64); ok {
			totalCount = int(size)
		}

		if values, ok := prMap["values"].([]interface{}); ok {
			for _, v := range values {
				if pr, ok := v.(map[string]interface{}); ok {
					result = append(result, c.convertPullRequest(pr))
				}
			}
		}
	}

	return result, totalCount, nil
}

// GetMergeRequest는 PR 상세 정보를 반환합니다.
func (c *BitbucketClient) GetMergeRequest(ctx context.Context, repoSlug string, prID int) (*MergeRequestInfo, error) {
	pr, err := c.client.Repositories.PullRequests.Get(&bitbucket.PullRequestsOptions{
		Owner:    c.workspace,
		RepoSlug: repoSlug,
		ID:       fmt.Sprintf("%d", prID),
	})
	if err != nil {
		return nil, fmt.Errorf("failed to get pull request: %w", err)
	}

	if prMap, ok := pr.(map[string]interface{}); ok {
		return c.convertPullRequest(prMap), nil
	}

	return nil, fmt.Errorf("invalid pull request response")
}

// CreateMergeRequest는 새 PR을 생성합니다.
func (c *BitbucketClient) CreateMergeRequest(ctx context.Context, repoSlug string, title, description, sourceBranch, targetBranch string, closeSourceBranch bool) (*MergeRequestInfo, error) {
	pr, err := c.client.Repositories.PullRequests.Create(&bitbucket.PullRequestsOptions{
		Owner:             c.workspace,
		RepoSlug:          repoSlug,
		Title:             title,
		Description:       description,
		SourceBranch:      sourceBranch,
		DestinationBranch: targetBranch,
		CloseSourceBranch: closeSourceBranch,
	})
	if err != nil {
		return nil, fmt.Errorf("failed to create pull request: %w", err)
	}

	if prMap, ok := pr.(map[string]interface{}); ok {
		return c.convertPullRequest(prMap), nil
	}

	return nil, fmt.Errorf("invalid pull request response")
}

// UpdateMergeRequest는 PR을 수정합니다.
func (c *BitbucketClient) UpdateMergeRequest(ctx context.Context, repoSlug string, prID int, title, description string) (*MergeRequestInfo, error) {
	pr, err := c.client.Repositories.PullRequests.Update(&bitbucket.PullRequestsOptions{
		Owner:       c.workspace,
		RepoSlug:    repoSlug,
		ID:          fmt.Sprintf("%d", prID),
		Title:       title,
		Description: description,
	})
	if err != nil {
		return nil, fmt.Errorf("failed to update pull request: %w", err)
	}

	if prMap, ok := pr.(map[string]interface{}); ok {
		return c.convertPullRequest(prMap), nil
	}

	return nil, fmt.Errorf("invalid pull request response")
}

// MergeMergeRequest는 PR을 머지합니다.
func (c *BitbucketClient) MergeMergeRequest(ctx context.Context, repoSlug string, prID int, commitMessage string, closeSourceBranch bool) (*MergeRequestInfo, string, error) {
	opts := &bitbucket.PullRequestsOptions{
		Owner:             c.workspace,
		RepoSlug:          repoSlug,
		ID:                fmt.Sprintf("%d", prID),
		Message:           commitMessage,
		CloseSourceBranch: closeSourceBranch,
	}

	pr, err := c.client.Repositories.PullRequests.Merge(opts)
	if err != nil {
		return nil, "", fmt.Errorf("failed to merge pull request: %w", err)
	}

	var mergeCommitSHA string
	if prMap, ok := pr.(map[string]interface{}); ok {
		if mergeCommit, ok := prMap["merge_commit"].(map[string]interface{}); ok {
			if hash, ok := mergeCommit["hash"].(string); ok {
				mergeCommitSHA = hash
			}
		}
		return c.convertPullRequest(prMap), mergeCommitSHA, nil
	}

	return nil, "", fmt.Errorf("invalid pull request response")
}

// DeclineMergeRequest는 PR을 거절합니다.
func (c *BitbucketClient) DeclineMergeRequest(ctx context.Context, repoSlug string, prID int) (*MergeRequestInfo, error) {
	pr, err := c.client.Repositories.PullRequests.Decline(&bitbucket.PullRequestsOptions{
		Owner:    c.workspace,
		RepoSlug: repoSlug,
		ID:       fmt.Sprintf("%d", prID),
	})
	if err != nil {
		return nil, fmt.Errorf("failed to decline pull request: %w", err)
	}

	if prMap, ok := pr.(map[string]interface{}); ok {
		return c.convertPullRequest(prMap), nil
	}

	return nil, fmt.Errorf("invalid pull request response")
}

// GetMergeRequestDiff는 PR의 변경사항을 반환합니다.
func (c *BitbucketClient) GetMergeRequestDiff(ctx context.Context, repoSlug string, prID int) (*MergeRequestDiffInfo, error) {
	diffstat, err := c.client.Repositories.Diff.GetDiffStat(&bitbucket.DiffStatOptions{
		Owner:             c.workspace,
		RepoSlug:          repoSlug,
		FromPullRequestID: prID,
	})
	if err != nil {
		return nil, fmt.Errorf("failed to get pull request diffstat: %w", err)
	}

	diff := &MergeRequestDiffInfo{
		Files: make([]*FileDiffInfo, 0),
	}

	if diffstat != nil && diffstat.DiffStats != nil {
		diff.ChangedFiles = len(diffstat.DiffStats)
		for _, item := range diffstat.DiffStats {
			fileDiff := &FileDiffInfo{}

			if item.New != nil {
				if path, ok := item.New["path"].(string); ok {
					fileDiff.Filename = path
				}
			}
			if item.Old != nil {
				if path, ok := item.Old["path"].(string); ok {
					fileDiff.PreviousFilename = path
				}
			}

			fileDiff.Status = strings.ToLower(item.Status)
			fileDiff.Additions = item.LinedAdded
			fileDiff.Deletions = item.LinesRemoved
			diff.Additions += fileDiff.Additions
			diff.Deletions += fileDiff.Deletions

			diff.Files = append(diff.Files, fileDiff)
		}
	}

	return diff, nil
}

// ListComments는 PR 댓글 목록을 반환합니다.
func (c *BitbucketClient) ListComments(ctx context.Context, repoSlug string, prID int) ([]*CommentInfo, error) {
	comments, err := c.client.Repositories.PullRequests.GetComments(&bitbucket.PullRequestsOptions{
		Owner:    c.workspace,
		RepoSlug: repoSlug,
		ID:       fmt.Sprintf("%d", prID),
	})
	if err != nil {
		return nil, fmt.Errorf("failed to get pull request comments: %w", err)
	}

	var result []*CommentInfo

	if commentsMap, ok := comments.(map[string]interface{}); ok {
		if values, ok := commentsMap["values"].([]interface{}); ok {
			for _, v := range values {
				if comment, ok := v.(map[string]interface{}); ok {
					result = append(result, c.convertComment(comment))
				}
			}
		}
	}

	return result, nil
}

// CreateComment는 PR 댓글을 생성합니다.
func (c *BitbucketClient) CreateComment(ctx context.Context, repoSlug string, prID int, body string) (*CommentInfo, error) {
	comment, err := c.client.Repositories.PullRequests.AddComment(&bitbucket.PullRequestCommentOptions{
		Owner:         c.workspace,
		RepoSlug:      repoSlug,
		PullRequestID: fmt.Sprintf("%d", prID),
		Content:       body,
	})
	if err != nil {
		return nil, fmt.Errorf("failed to add pull request comment: %w", err)
	}

	if commentMap, ok := comment.(map[string]interface{}); ok {
		return c.convertComment(commentMap), nil
	}

	return nil, fmt.Errorf("invalid comment response")
}

// UpdateComment는 PR 댓글을 수정합니다.
// Bitbucket API는 댓글 수정 시 PR ID와 Comment ID가 필요합니다.
func (c *BitbucketClient) UpdateComment(ctx context.Context, repoSlug string, prID int, commentID int64, body string) (*CommentInfo, error) {
	comment, err := c.client.Repositories.PullRequests.UpdateComment(&bitbucket.PullRequestCommentOptions{
		Owner:         c.workspace,
		RepoSlug:      repoSlug,
		PullRequestID: fmt.Sprintf("%d", prID),
		CommentId:     fmt.Sprintf("%d", commentID),
		Content:       body,
	})
	if err != nil {
		return nil, fmt.Errorf("failed to update pull request comment: %w", err)
	}

	if commentMap, ok := comment.(map[string]interface{}); ok {
		return c.convertComment(commentMap), nil
	}

	return nil, fmt.Errorf("invalid comment response")
}

// DeleteComment는 PR 댓글을 삭제합니다.
// Bitbucket API는 댓글 삭제 시 PR ID와 Comment ID가 필요합니다.
func (c *BitbucketClient) DeleteComment(ctx context.Context, repoSlug string, prID int, commentID int64) error {
	_, err := c.client.Repositories.PullRequests.DeleteComment(&bitbucket.PullRequestCommentOptions{
		Owner:         c.workspace,
		RepoSlug:      repoSlug,
		PullRequestID: fmt.Sprintf("%d", prID),
		CommentId:     fmt.Sprintf("%d", commentID),
	})
	if err != nil {
		return fmt.Errorf("failed to delete pull request comment: %w", err)
	}
	return nil
}

// Approve는 PR을 승인합니다.
func (c *BitbucketClient) Approve(ctx context.Context, repoSlug string, prID int) error {
	_, err := c.client.Repositories.PullRequests.Approve(&bitbucket.PullRequestsOptions{
		Owner:    c.workspace,
		RepoSlug: repoSlug,
		ID:       fmt.Sprintf("%d", prID),
	})
	if err != nil {
		return fmt.Errorf("failed to approve pull request: %w", err)
	}
	return nil
}

// Unapprove는 PR 승인을 취소합니다.
func (c *BitbucketClient) Unapprove(ctx context.Context, repoSlug string, prID int) error {
	_, err := c.client.Repositories.PullRequests.UnApprove(&bitbucket.PullRequestsOptions{
		Owner:    c.workspace,
		RepoSlug: repoSlug,
		ID:       fmt.Sprintf("%d", prID),
	})
	if err != nil {
		return fmt.Errorf("failed to unapprove pull request: %w", err)
	}
	return nil
}

// convertPullRequest는 Bitbucket PR을 MergeRequestInfo로 변환합니다.
func (c *BitbucketClient) convertPullRequest(pr map[string]interface{}) *MergeRequestInfo {
	if pr == nil {
		return nil
	}

	result := &MergeRequestInfo{}

	// ID
	if id, ok := pr["id"].(float64); ok {
		result.ID = fmt.Sprintf("%.0f", id)
		result.Number = int(id)
	}

	// Title, Description
	result.Title, _ = pr["title"].(string)
	result.Description, _ = pr["description"].(string)

	// State
	if state, ok := pr["state"].(string); ok {
		switch strings.ToUpper(state) {
		case "OPEN":
			result.State = "open"
		case "MERGED":
			result.State = "merged"
		case "DECLINED", "SUPERSEDED":
			result.State = "closed"
		default:
			result.State = strings.ToLower(state)
		}
	}

	// Source/Target Branch
	if source, ok := pr["source"].(map[string]interface{}); ok {
		if branch, ok := source["branch"].(map[string]interface{}); ok {
			result.SourceBranch, _ = branch["name"].(string)
		}
		if commit, ok := source["commit"].(map[string]interface{}); ok {
			result.HeadSHA, _ = commit["hash"].(string)
		}
	}
	if destination, ok := pr["destination"].(map[string]interface{}); ok {
		if branch, ok := destination["branch"].(map[string]interface{}); ok {
			result.TargetBranch, _ = branch["name"].(string)
		}
		if commit, ok := destination["commit"].(map[string]interface{}); ok {
			result.BaseSHA, _ = commit["hash"].(string)
		}
	}

	// Author
	if author, ok := pr["author"].(map[string]interface{}); ok {
		result.Author = c.convertBitbucketUser(author)
	}

	// URL
	if links, ok := pr["links"].(map[string]interface{}); ok {
		if html, ok := links["html"].(map[string]interface{}); ok {
			result.URL, _ = html["href"].(string)
		}
	}

	// Dates
	result.CreatedAt, _ = pr["created_on"].(string)
	result.UpdatedAt, _ = pr["updated_on"].(string)

	// Merged info
	if mergeCommit, ok := pr["merge_commit"].(map[string]interface{}); ok {
		if _, ok := mergeCommit["hash"]; ok {
			result.MergedAt = result.UpdatedAt
		}
	}
	if closedBy, ok := pr["closed_by"].(map[string]interface{}); ok {
		result.MergedBy = c.convertBitbucketUser(closedBy)
	}

	// Reviewers
	if reviewers, ok := pr["reviewers"].([]interface{}); ok {
		result.Reviewers = make([]*UserInfo, len(reviewers))
		for i, r := range reviewers {
			if reviewer, ok := r.(map[string]interface{}); ok {
				result.Reviewers[i] = c.convertBitbucketUser(reviewer)
			}
		}
	}

	// Participants (assignees 대신)
	if participants, ok := pr["participants"].([]interface{}); ok {
		var assignees []*UserInfo
		for _, p := range participants {
			if participant, ok := p.(map[string]interface{}); ok {
				if role, ok := participant["role"].(string); ok && role == "REVIEWER" {
					if user, ok := participant["user"].(map[string]interface{}); ok {
						assignees = append(assignees, c.convertBitbucketUser(user))
					}
				}
			}
		}
		result.Assignees = assignees
	}

	return result
}

// convertBitbucketUser는 Bitbucket User를 UserInfo로 변환합니다.
func (c *BitbucketClient) convertBitbucketUser(user map[string]interface{}) *UserInfo {
	if user == nil {
		return nil
	}

	result := &UserInfo{}
	result.ID, _ = user["uuid"].(string)
	result.Login, _ = user["nickname"].(string)
	if result.Login == "" {
		result.Login, _ = user["username"].(string)
	}
	result.Name, _ = user["display_name"].(string)

	if links, ok := user["links"].(map[string]interface{}); ok {
		if avatar, ok := links["avatar"].(map[string]interface{}); ok {
			result.AvatarURL, _ = avatar["href"].(string)
		}
	}

	return result
}

// convertComment는 Bitbucket Comment를 CommentInfo로 변환합니다.
func (c *BitbucketClient) convertComment(comment map[string]interface{}) *CommentInfo {
	if comment == nil {
		return nil
	}

	result := &CommentInfo{}

	if id, ok := comment["id"].(float64); ok {
		result.ID = fmt.Sprintf("%.0f", id)
	}

	if content, ok := comment["content"].(map[string]interface{}); ok {
		result.Body, _ = content["raw"].(string)
	}

	if user, ok := comment["user"].(map[string]interface{}); ok {
		result.User = c.convertBitbucketUser(user)
	}

	result.CreatedAt, _ = comment["created_on"].(string)
	result.UpdatedAt, _ = comment["updated_on"].(string)

	// Inline comment info
	if inline, ok := comment["inline"].(map[string]interface{}); ok {
		result.Path, _ = inline["path"].(string)
		if to, ok := inline["to"].(float64); ok {
			result.Line = int(to)
		}
	}

	return result
}
