package main

// AzureDevOpsConfig는 Azure DevOps 프로바이더 설정
type AzureDevOpsConfig struct {
	Organization string
	Project      string
	PAT          string
}

func (g *AzureDevOpsConfig) GetType() ProviderType {
	return Azure
}
func (g *AzureDevOpsConfig) GetBaseURL() string {
	if g.Organization == "" {
		return "https://dev.azure.com"
	}
	return "https://dev.azure.com/" + g.Organization
}

// TODO: init() 함수에서 Register 호출
func init() {
	Register(Azure, func(option map[string]string) ProviderConfig {
		return &AzureDevOpsConfig{
			Organization: option["Organization"],
			Project:      option["Project"],
			PAT:          option["PAT"],
		}
	})
}
