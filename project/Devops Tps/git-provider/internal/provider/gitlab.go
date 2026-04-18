package provider

// GitLabConfig는 GitLab 프로바이더 설정입니다.
type GitLabConfig struct {
	// Token은 GitLab Personal Access Token입니다. (필수)
	// 발급: GitLab → Settings → Access Tokens
	Token string

	// BaseURL은 Self-hosted GitLab 서버 URL입니다. (선택)
	// 공개 GitLab 사용 시 빈 문자열로 두면 됩니다.
	// 예: "https://gitlab.mycompany.com"
	BaseURL string
}

// GetType은 프로바이더 종류를 반환합니다.
func (c *GitLabConfig) GetType() ProviderType {
	return GitLab
}

// GetCredentials는 인증 정보를 반환합니다.
// GitLab은 Bearer Token 방식을 사용합니다.
func (c *GitLabConfig) GetCredentials() Credentials {
	return &TokenCredentials{
		Token: c.Token,
	}
}

// GetBaseURL은 API 기본 URL을 반환합니다.
func (c *GitLabConfig) GetBaseURL() string {
	return c.BaseURL
}

// Validate는 설정이 유효한지 검증합니다.
func (c *GitLabConfig) Validate() error {
	if c.Token == "" {
		return ErrEmptyToken
	}
	return nil
}

// 컴파일 타임에 인터페이스 구현 확인
var _ ProviderConfig = (*GitLabConfig)(nil)
