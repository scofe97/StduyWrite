package provider

// BitbucketConfig는 Bitbucket 프로바이더 설정입니다.
//
// GitHub/GitLab과 다른 점:
// - Username이 필수입니다!
// - Token 대신 App Password를 사용합니다.
// - Basic Auth 방식으로 인증합니다.
type BitbucketConfig struct {
	// Username은 Bitbucket 계정 이름입니다. (필수)
	Username string

	// AppPassword는 Bitbucket App Password입니다. (필수)
	// 발급: Bitbucket → Settings → App passwords
	AppPassword string

	// Workspace는 Bitbucket Workspace 이름입니다. (선택)
	// 조직/팀 저장소에 접근할 때 사용합니다.
	Workspace string
}

// GetType은 프로바이더 종류를 반환합니다.
func (c *BitbucketConfig) GetType() ProviderType {
	return Bitbucket
}

// GetCredentials는 인증 정보를 반환합니다.
// Bitbucket은 Basic Auth 방식을 사용합니다.
func (c *BitbucketConfig) GetCredentials() Credentials {
	return &BasicCredentials{
		Username: c.Username,
		Password: c.AppPassword,
	}
}

// GetBaseURL은 API 기본 URL을 반환합니다.
// Bitbucket Cloud는 고정 URL을 사용합니다.
func (c *BitbucketConfig) GetBaseURL() string {
	return "" // Bitbucket Cloud는 항상 api.bitbucket.org 사용
}

// GetWorkspace는 Workspace 이름을 반환합니다.
// Bitbucket 전용 메서드입니다.
func (c *BitbucketConfig) GetWorkspace() string {
	return c.Workspace
}

// Validate는 설정이 유효한지 검증합니다.
func (c *BitbucketConfig) Validate() error {
	if c.Username == "" {
		return ErrEmptyUsername
	}
	if c.AppPassword == "" {
		return ErrEmptyToken
	}
	return nil
}

// 컴파일 타임에 인터페이스 구현 확인
var _ ProviderConfig = (*BitbucketConfig)(nil)
