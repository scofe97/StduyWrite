package _7_strings_regex

import "errors"

// 검증 에러들
var (
	ErrEmptyOrganization = errors.New("organization is required")
	ErrEmptyProject      = errors.New("project is required")
	ErrEmptyPAT          = errors.New("pat is required")
)

type AzureDevopsConfig struct {
	Organization string
	Project      string
	PAT          string
}

func (c *AzureDevopsConfig) Validate() error {
	if c.Organization == "" {
		return ErrEmptyOrganization
	}
	if c.Project == "" {
		return ErrEmptyProject
	}
	if c.PAT == "" {
		return ErrEmptyPAT
	}

	return nil
}

type Validatable interface {
	Validate() error
}

var _ Validatable = (*AzureDevopsConfig)(nil)
