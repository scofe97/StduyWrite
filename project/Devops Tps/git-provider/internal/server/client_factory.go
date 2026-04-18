package server

import (
	"context"
	"fmt"

	"github.com/runners-high/git-provider/internal/client"
	pb "github.com/runners-high/git-provider/pkg/pb/v1"
)

// =============================================================================
// 공통 클라이언트 생성 함수
// 4개 서버(git, branch, contents, mr)에서 공유합니다.
// =============================================================================

func createGitHubClient(ctx context.Context, config *pb.GitHubConfig) (*client.GitHubClient, error) {
	if config.Token == "" {
		return nil, fmt.Errorf("github token is required")
	}
	return client.NewGitHubClient(ctx, config.Token, config.BaseUrl)
}

func createGitLabClient(config *pb.GitLabConfig) (*client.GitLabClient, error) {
	if config.Token == "" {
		return nil, fmt.Errorf("gitlab token is required")
	}
	return client.NewGitLabClient(config.Token, config.BaseUrl)
}

func createBitbucketClient(config *pb.BitbucketConfig) (*client.BitbucketClient, error) {
	if config.Email == "" {
		return nil, fmt.Errorf("bitbucket email is required")
	}
	if config.ApiToken == "" {
		return nil, fmt.Errorf("bitbucket api_token is required")
	}
	if config.Workspace == "" {
		return nil, fmt.Errorf("bitbucket workspace is required")
	}
	return client.NewBitbucketClient(config.Email, config.ApiToken, config.Workspace)
}
