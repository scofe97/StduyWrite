package client

import (
	"context"
	"fmt"
	"strings"

	"github.com/google/go-github/v57/github"
	"golang.org/x/oauth2"
)

// GitHubClient wraps GitHub API operations
// 깃허브 API 작업을 래핑하는 도구
type GitHubClient struct {
	client *github.Client
}

// NewGitHubClient creates a new GitHub client with the given access token
// 주어진 액세스 토큰으로 표준 Github 클라이언트를 생성한다.
func NewGitHubClient(ctx context.Context, accessToken string) *GitHubClient {
	ts := oauth2.StaticTokenSource(
		&oauth2.Token{AccessToken: accessToken},
	)
	tc := oauth2.NewClient(ctx, ts)
	client := github.NewClient(tc)

	return &GitHubClient{client: client}
}

// NewGitHubClientWithBaseURL creates a client for GitHub Enterprise
func NewGitHubClientWithBaseURL(ctx context.Context, accessToken, baseURL string) (*GitHubClient, error) {
	ts := oauth2.StaticTokenSource(
		&oauth2.Token{AccessToken: accessToken},
	)
	tc := oauth2.NewClient(ctx, ts)
	client, err := github.NewClient(tc).WithEnterpriseURLs(baseURL, baseURL)
	if err != nil {
		return nil, err
	}

	return &GitHubClient{client: client}, nil
}

// parseRepoURL extracts owner and repo from GitHub URL
func parseRepoURL(url string) (owner, repo string, err error) {
	// Handle formats:
	// https://github.com/owner/repo
	// https://github.com/owner/repo.git
	// git@github.com:owner/repo.git

	url = strings.TrimSuffix(url, ".git")

	if strings.HasPrefix(url, "git@") {
		// git@github.com:owner/repo
		parts := strings.Split(url, ":")
		if len(parts) != 2 {
			return "", "", fmt.Errorf("invalid git URL format: %s", url)
		}
		pathParts := strings.Split(parts[1], "/")
		if len(pathParts) != 2 {
			return "", "", fmt.Errorf("invalid git URL format: %s", url)
		}
		return pathParts[0], pathParts[1], nil
	}

	// https://github.com/owner/repo
	parts := strings.Split(url, "/")
	if len(parts) < 2 {
		return "", "", fmt.Errorf("invalid repository URL: %s", url)
	}
	return parts[len(parts)-2], parts[len(parts)-1], nil
}

// CreateBranch creates a new branch from the base branch
func (c *GitHubClient) CreateBranch(ctx context.Context, repoURL, branchName, baseBranch string) (string, error) {
	owner, repo, err := parseRepoURL(repoURL)
	if err != nil {
		return "", err
	}

	// Get the SHA of the base branch
	baseRef, _, err := c.client.Git.GetRef(ctx, owner, repo, "refs/heads/"+baseBranch)
	if err != nil {
		return "", fmt.Errorf("failed to get base branch %s: %w", baseBranch, err)
	}

	// Create new branch reference
	newRef := &github.Reference{
		Ref:    github.String("refs/heads/" + branchName),
		Object: &github.GitObject{SHA: baseRef.Object.SHA},
	}

	ref, _, err := c.client.Git.CreateRef(ctx, owner, repo, newRef)
	if err != nil {
		return "", fmt.Errorf("failed to create branch %s: %w", branchName, err)
	}

	return ref.GetObject().GetSHA(), nil
}

// DeleteBranch deletes a branch
func (c *GitHubClient) DeleteBranch(ctx context.Context, repoURL, branchName string) error {
	owner, repo, err := parseRepoURL(repoURL)
	if err != nil {
		return err
	}

	_, err = c.client.Git.DeleteRef(ctx, owner, repo, "refs/heads/"+branchName)
	if err != nil {
		return fmt.Errorf("failed to delete branch %s: %w", branchName, err)
	}

	return nil
}

// GetBranches returns list of branch names
func (c *GitHubClient) GetBranches(ctx context.Context, repoURL string) ([]string, error) {
	owner, repo, err := parseRepoURL(repoURL)
	if err != nil {
		return nil, err
	}

	branches, _, err := c.client.Repositories.ListBranches(ctx, owner, repo, nil)
	if err != nil {
		return nil, err
	}

	result := make([]string, len(branches))
	for i, b := range branches {
		result[i] = b.GetName()
	}
	return result, nil
}

// GetRepository returns repository information
func (c *GitHubClient) GetRepository(ctx context.Context, repoURL string) (*RepositoryInfo, error) {
	owner, repo, err := parseRepoURL(repoURL)
	if err != nil {
		return nil, err
	}

	repository, _, err := c.client.Repositories.Get(ctx, owner, repo)
	if err != nil {
		return nil, err
	}

	return &RepositoryInfo{
		Name:          repository.GetName(),
		DefaultBranch: repository.GetDefaultBranch(),
		CloneURL:      repository.GetCloneURL(),
		HTMLURL:       repository.GetHTMLURL(),
	}, nil
}

// CreatePullRequest creates a new pull request
func (c *GitHubClient) CreatePullRequest(ctx context.Context, repoURL, title, body, head, base string) (*PullRequestInfo, error) {
	owner, repo, err := parseRepoURL(repoURL)
	if err != nil {
		return nil, err
	}

	newPR := &github.NewPullRequest{
		Title: github.String(title),
		Body:  github.String(body),
		Head:  github.String(head),
		Base:  github.String(base),
	}

	pr, _, err := c.client.PullRequests.Create(ctx, owner, repo, newPR)
	if err != nil {
		return nil, fmt.Errorf("failed to create pull request: %w", err)
	}

	return &PullRequestInfo{
		ID:     fmt.Sprintf("%d", pr.GetNumber()),
		Number: pr.GetNumber(),
		URL:    pr.GetHTMLURL(),
		State:  pr.GetState(),
	}, nil
}

// RepositoryInfo contains repository information
type RepositoryInfo struct {
	Name          string
	DefaultBranch string
	CloneURL      string
	HTMLURL       string
}

// PullRequestInfo contains pull request information
type PullRequestInfo struct {
	ID     string
	Number int
	URL    string
	State  string
}
