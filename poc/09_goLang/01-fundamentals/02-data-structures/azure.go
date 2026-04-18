package main

type AzureDevOpsConfig struct {
	Organization string
	Project      string
	PAT          string
}

// GetType은 프로바이더 종류를 반환합니다.
func (c *AzureDevOpsConfig) GetType() ProviderType {
	return GitHub
}

// GetCredentials는 인증 정보를 반환합니다.
// GitHub는 Bearer Token 방식을 사용합니다.
func (c *AzureDevOpsConfig) GetCredentials() Credentials {
	return &BasicCredentials{
		Username: "",
		Password: c.PAT,
	}
}

// GetBaseURL은 API 기본 URL을 반환합니다.
func (c *AzureDevOpsConfig) GetBaseURL() string {
	return c.Organization
}

// Validate는 설정이 유효한지 검증합니다.
func (c *AzureDevOpsConfig) Validate() error {
	if c.PAT == "" {
		return ErrEmptyToken
	}
	return nil
}

// 컴파일 타임에 인터페이스 구현 확인
var _ ProviderConfig = (*AzureDevOpsConfig)(nil)
