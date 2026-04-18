package main

// ProviderType은 Git 프로바이더 종류를 나타냅니다.
type ProviderType string

const (
	GitHub    ProviderType = "github"
	GitLab    ProviderType = "gitlab"
	Bitbucket ProviderType = "bitbucket"
	Azure     ProviderType = "azure"
)

// ProviderConfig 인터페이스 - 모든 프로바이더가 구현해야 함
type ProviderConfig interface {
	GetType() ProviderType
	GetBaseURL() string
}
