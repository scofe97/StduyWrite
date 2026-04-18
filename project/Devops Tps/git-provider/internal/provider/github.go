package provider

// GitHubConfig는 GitHub 프로바이더 설정입니다.
type GitHubConfig struct {
	// Token은 GitHub Personal Access Token입니다. (필수)
	// 발급: GitHub → Settings → Developer settings → Personal access tokens
	Token string

	// BaseURL은 GitHub Enterprise 서버 URL입니다. (선택)
	// 공개 GitHub 사용 시 빈 문자열로 두면 됩니다.
	// 예: "https://github.mycompany.com"
	BaseURL string
}

// GetType은 프로바이더 종류를 반환합니다.
func (c *GitHubConfig) GetType() ProviderType {
	return GitHub
}

// GetCredentials는 인증 정보를 반환합니다.
// GitHub는 Bearer Token 방식을 사용합니다.
func (c *GitHubConfig) GetCredentials() Credentials {
	return &TokenCredentials{
		Token: c.Token,
	}
}

// GetBaseURL은 API 기본 URL을 반환합니다.
func (c *GitHubConfig) GetBaseURL() string {
	return c.BaseURL
}

// Validate는 설정이 유효한지 검증합니다.
func (c *GitHubConfig) Validate() error {
	if c.Token == "" {
		return ErrEmptyToken
	}
	return nil
}

// 컴파일 타임에 인터페이스 구현 확인
var _ ProviderConfig = (*GitHubConfig)(nil)
