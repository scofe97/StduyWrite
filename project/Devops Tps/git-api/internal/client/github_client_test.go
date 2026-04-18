package client

import (
	"testing"
)

func TestParseRepoURL_GitHub(t *testing.T) {
	tests := []struct {
		name          string
		url           string
		expectedOwner string
		expectedRepo  string
		expectError   bool
	}{
		{
			name:          "HTTPS URL",
			url:           "https://github.com/owner/repo",
			expectedOwner: "owner",
			expectedRepo:  "repo",
			expectError:   false,
		},
		{
			name:          "HTTPS URL with .git",
			url:           "https://github.com/owner/repo.git",
			expectedOwner: "owner",
			expectedRepo:  "repo",
			expectError:   false,
		},
		{
			name:          "SSH URL",
			url:           "git@github.com:owner/repo.git",
			expectedOwner: "owner",
			expectedRepo:  "repo",
			expectError:   false,
		},
		{
			name:          "URL with trailing slash",
			url:           "https://github.com/owner/repo/",
			expectedOwner: "owner",
			expectedRepo:  "repo",
			expectError:   false,
		},
		{
			name:          "Complex repo name",
			url:           "https://github.com/my-org/my-complex-repo-name",
			expectedOwner: "my-org",
			expectedRepo:  "my-complex-repo-name",
			expectError:   false,
		},
		{
			name:        "Invalid URL - too short",
			url:         "https://github.com/owner",
			expectError: true,
		},
		{
			name:        "Invalid URL - empty",
			url:         "",
			expectError: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			owner, repo, err := parseRepoURL(tt.url)

			if tt.expectError {
				if err == nil {
					t.Errorf("expected error, got nil")
				}
				return
			}

			if err != nil {
				t.Errorf("unexpected error: %v", err)
				return
			}

			if owner != tt.expectedOwner {
				t.Errorf("expected owner %s, got %s", tt.expectedOwner, owner)
			}
			if repo != tt.expectedRepo {
				t.Errorf("expected repo %s, got %s", tt.expectedRepo, repo)
			}
		})
	}
}

func TestRepositoryInfo(t *testing.T) {
	info := RepositoryInfo{
		ID:            "123",
		Name:          "test-repo",
		FullName:      "owner/test-repo",
		Description:   "Test repository",
		DefaultBranch: "main",
		Private:       false,
		CloneURL:      "https://github.com/owner/test-repo.git",
		SSHURL:        "git@github.com:owner/test-repo.git",
	}

	if info.Name != "test-repo" {
		t.Errorf("expected Name test-repo, got %s", info.Name)
	}
	if info.DefaultBranch != "main" {
		t.Errorf("expected DefaultBranch main, got %s", info.DefaultBranch)
	}
}

func TestPullRequestInfo(t *testing.T) {
	info := PullRequestInfo{
		ID:     "456",
		Number: 42,
		Title:  "Test PR",
		URL:    "https://github.com/owner/repo/pull/42",
		State:  "open",
	}

	if info.Number != 42 {
		t.Errorf("expected Number 42, got %d", info.Number)
	}
	if info.State != "open" {
		t.Errorf("expected State open, got %s", info.State)
	}
}

// GitHubClient Integration Test (Skip without token)
// Run with: GITHUB_TEST_TOKEN=xxx go test -v -run TestGitHubClient_Integration
func TestGitHubClient_Integration(t *testing.T) {
	// Skip if no token provided
	// token := os.Getenv("GITHUB_TEST_TOKEN")
	// if token == "" {
	// 	t.Skip("GITHUB_TEST_TOKEN not set, skipping integration test")
	// }

	t.Skip("Integration test - requires GITHUB_TEST_TOKEN")

	// Example integration test structure:
	// ctx := context.Background()
	// client := NewGitHubClient(ctx, token)
	//
	// // Test GetRepository
	// repo, err := client.GetRepository(ctx, "https://github.com/owner/repo")
	// if err != nil {
	//     t.Errorf("GetRepository failed: %v", err)
	// }
	// t.Logf("Repository: %+v", repo)
	//
	// // Test GetBranches
	// branches, err := client.GetBranches(ctx, "https://github.com/owner/repo")
	// if err != nil {
	//     t.Errorf("GetBranches failed: %v", err)
	// }
	// t.Logf("Branches: %v", branches)
}

// Benchmark for URL parsing
func BenchmarkParseRepoURL(b *testing.B) {
	url := "https://github.com/owner/repository-name.git"

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _, _ = parseRepoURL(url)
	}
}
