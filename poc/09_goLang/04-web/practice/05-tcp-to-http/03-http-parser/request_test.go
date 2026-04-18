package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestParseRequestLine(t *testing.T) {
	tests := []struct {
		name           string
		input          string
		expectedMethod string
		expectedTarget string
		expectedVer    string
		expectError    bool
	}{
		{
			name:           "Valid GET request",
			input:          "GET /coffee HTTP/1.1\r\n",
			expectedMethod: "GET",
			expectedTarget: "/coffee",
			expectedVer:    "1.1",
			expectError:    false,
		},
		{
			name:           "Valid POST request",
			input:          "POST /api/users HTTP/1.1\r\n",
			expectedMethod: "POST",
			expectedTarget: "/api/users",
			expectedVer:    "1.1",
			expectError:    false,
		},
		{
			name:        "Incomplete line",
			input:       "GET /coffee",
			expectError: false, // nil 반환, 에러 아님
		},
		{
			name:        "Malformed - missing parts",
			input:       "GET /coffee\r\n",
			expectError: true,
		},
		{
			name:        "Unsupported HTTP version",
			input:       "GET /coffee HTTP/2.0\r\n",
			expectError: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			rl, n, err := parseRequestLine([]byte(tt.input))

			if tt.expectError {
				require.Error(t, err)
				return
			}

			if tt.input == "GET /coffee" {
				// 불완전한 입력
				assert.Nil(t, rl)
				assert.Equal(t, 0, n)
				return
			}

			require.NoError(t, err)
			assert.Equal(t, tt.expectedMethod, rl.Method)
			assert.Equal(t, tt.expectedTarget, rl.RequestTarget)
			assert.Equal(t, tt.expectedVer, rl.HttpVersion)
			assert.Equal(t, len(tt.input), n)
		})
	}
}
