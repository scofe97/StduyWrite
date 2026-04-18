package client

import (
	"context"
	"fmt"
	"net/url"
	"strings"

	"github.com/xanzy/go-gitlab"
)

// GitLabClient wraps GitLab API operations
type GitLabClient struct {
	client *gitlab.Client
}

// NewGitLabClient creates a new GitLab client with the given access token
func NewGitLabClient(accessToken string) (*GitLabClient, error) {
	client, err := gitlab.NewClient(accessToken)
	if err != nil {
		return nil, err
	}
	return &GitLabClient{client: client}, nil
}

// NewGitLabClientWithBaseURL creates a client for self-hosted GitLab
func NewGitLabClientWithBaseURL(accessToken, baseURL string) (*GitLabClient, error) {
	client, err := gitlab.NewClient(accessToken, gitlab.WithBaseURL(baseURL))
	if err != nil {
		return nil, err
	}
	return &GitLabClient{client: client}, nil
}

// parseGitLabRepoURL extracts project path from GitLab URL
func parseGitLabRepoURL(repoURL string) (string, error) {
	// Handle formats:
	// https://gitlab.com/group/project
	// https://gitlab.com/group/subgroup/project
	// https://gitlab.com/group/project.git

	repoURL = strings.TrimSuffix(repoURL, ".git")

	parsed, err := url.Parse(repoURL)
	if err != nil {
		return "", err
	}

	// Remove leading slash
	path := strings.TrimPrefix(parsed.Path, "/")
	if path == "" {
		return "", fmt.Errorf("invalid GitLab URL: %s", repoURL)
	}

	return path, nil
}

// CreateBranch creates a new branch from the base branch
func (c *GitLabClient) CreateBranch(ctx context.Context, repoURL, branchName, baseBranch string) (string, error) {
	projectPath, err := parseGitLabRepoURL(repoURL)
	if err != nil {
		return "", err
	}

	branch, _, err := c.client.Branches.CreateBranch(projectPath, &gitlab.CreateBranchOptions{
		Branch: gitlab.Ptr(branchName),
		Ref:    gitlab.Ptr(baseBranch),
	})
	if err != nil {
		return "", fmt.Errorf("failed to create branch %s: %w", branchName, err)
	}

	return branch.Commit.ID, nil
}

// DeleteBranch deletes a branch
func (c *GitLabClient) DeleteBranch(ctx context.Context, repoURL, branchName string) error {
	projectPath, err := parseGitLabRepoURL(repoURL)
	if err != nil {
		return err
	}

	_, err = c.client.Branches.DeleteBranch(projectPath, branchName)
	if err != nil {
		return fmt.Errorf("failed to delete branch %s: %w", branchName, err)
	}

	return nil
}

// GetBranches returns list of branch names
func (c *GitLabClient) GetBranches(ctx context.Context, repoURL string) ([]string, error) {
	projectPath, err := parseGitLabRepoURL(repoURL)
	if err != nil {
		return nil, err
	}

	branches, _, err := c.client.Branches.ListBranches(projectPath, nil)
	if err != nil {
		return nil, err
	}

	result := make([]string, len(branches))
	for i, b := range branches {
		result[i] = b.Name
	}
	return result, nil
}

// GetRepository returns repository information
func (c *GitLabClient) GetRepository(ctx context.Context, repoURL string) (*RepositoryInfo, error) {
	projectPath, err := parseGitLabRepoURL(repoURL)
	if err != nil {
		return nil, err
	}

	project, _, err := c.client.Projects.GetProject(projectPath, nil)
	if err != nil {
		return nil, err
	}

	return &RepositoryInfo{
		Name:          project.Name,
		DefaultBranch: project.DefaultBranch,
		CloneURL:      project.HTTPURLToRepo,
		HTMLURL:       project.WebURL,
	}, nil
}

// CreateMergeRequest creates a new merge request
func (c *GitLabClient) CreateMergeRequest(ctx context.Context, repoURL, title, description, sourceBranch, targetBranch string) (*PullRequestInfo, error) {
	projectPath, err := parseGitLabRepoURL(repoURL)
	if err != nil {
		return nil, err
	}

	mr, _, err := c.client.MergeRequests.CreateMergeRequest(projectPath, &gitlab.CreateMergeRequestOptions{
		Title:        gitlab.Ptr(title),
		Description:  gitlab.Ptr(description),
		SourceBranch: gitlab.Ptr(sourceBranch),
		TargetBranch: gitlab.Ptr(targetBranch),
	})
	if err != nil {
		return nil, fmt.Errorf("failed to create merge request: %w", err)
	}

	return &PullRequestInfo{
		ID:     fmt.Sprintf("%d", mr.IID),
		Number: mr.IID,
		URL:    mr.WebURL,
		State:  mr.State,
	}, nil
}
