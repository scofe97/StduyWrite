package main

import "errors"

// ProviderType은 Git 프로바이더 종류를 나타냅니다.
type ProviderType string

const (
	GitHub    ProviderType = "github"
	GitLab    ProviderType = "gitlab"
	Bitbucket ProviderType = "bitbucket"
	Azure     ProviderType = "azure"
)

// 검증 에러들
var (
	ErrEmptyToken    = errors.New("token is required")
	ErrEmptyUsername = errors.New("username is required")
	ErrInvalidType   = errors.New("invalid provider type")
)

type ProviderConfig interface {
	GetType() ProviderType
	GetCredentials() Credentials
	GetBaseURL() string
	Validate() error
}
