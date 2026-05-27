package main

// GitHubConfig는 GitHub 프로바이더 설정
type GitHubConfig struct {
	Token   string
	BaseURL string
}

// GetType은 프로바이더 타입 반환
func (g *GitHubConfig) GetType() ProviderType {
	return GitHub
}

// GetBaseURL은 API 기본 URL 반환
func (g *GitHubConfig) GetBaseURL() string {
	if g.BaseURL == "" {
		return "https://api.github.com"
	}
	return g.BaseURL
}

// init은 패키지 로드 시 자동 실행 - GitHub 프로바이더 등록
func init() {
	Register(GitHub, func(option map[string]string) ProviderConfig {
		return &GitHubConfig{
			Token:   option["Token"],
			BaseURL: option["BaseURL"],
		}
	})
}
