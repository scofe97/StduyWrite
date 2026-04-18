package main

import (
	"encoding/base64"
	"net/http"
)

type Credentials interface {
	ApplyAuth(req *http.Request)

	GetAuthType() string
}

type TokenCredentials struct {
	Token string
}

func (c *TokenCredentials) ApplyAuth(req *http.Request) {
	req.Header.Set("Authorization", "Bearer "+c.Token)
}

func (c *TokenCredentials) GetAuthType() string {
	return "bearer_token"
}

var _ Credentials = (*TokenCredentials)(nil)

type BasicCredentials struct {
	Username string
	Password string // Bitbucket의 경우 App Password
}

func (c *BasicCredentials) ApplyAuth(req *http.Request) {
	auth := c.Username + ":" + c.Password
	encoded := base64.StdEncoding.EncodeToString([]byte(auth))
	req.Header.Set("Authorization", "Basic "+encoded)
}

func (c *BasicCredentials) GetAuthType() string {
	return "basic_auth"
}

var _ Credentials = (*BasicCredentials)(nil)
