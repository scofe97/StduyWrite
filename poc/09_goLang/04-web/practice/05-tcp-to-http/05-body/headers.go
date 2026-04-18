package main

import (
	"bytes"
	"errors"
	"strings"
)

// Headers는 HTTP 헤더를 저장합니다
type Headers struct {
	headers map[string]string
}

// NewHeaders는 새 Headers 인스턴스를 생성합니다
func NewHeaders() *Headers {
	return &Headers{
		headers: make(map[string]string),
	}
}

// Get은 헤더 값을 대소문자 무시하여 가져옵니다
func (h *Headers) Get(name string) (string, bool) {
	name = strings.ToLower(name)
	value, exists := h.headers[name]
	return value, exists
}

// Set은 헤더 값을 설정합니다
func (h *Headers) Set(name, value string) {
	name = strings.ToLower(name)
	if existing, exists := h.headers[name]; exists {
		h.headers[name] = existing + ", " + value
	} else {
		h.headers[name] = value
	}
}

// Parse는 바이트 데이터에서 헤더를 파싱합니다
func (h *Headers) Parse(data []byte) (int, bool, error) {
	read := 0

	for {
		idx := bytes.Index(data[read:], CRLF)
		if idx == -1 {
			return read, false, nil
		}

		if idx == 0 {
			read += len(CRLF)
			return read, true, nil
		}

		line := data[read : read+idx]
		parts := bytes.SplitN(line, []byte(":"), 2)
		if len(parts) != 2 {
			return read, false, errors.New("malformed field line")
		}

		name := parts[0]
		value := bytes.TrimSpace(parts[1])

		if bytes.HasSuffix(name, []byte(" ")) {
			return read, false, errors.New("malformed field line")
		}

		h.Set(string(name), string(value))
		read += idx + len(CRLF)
	}
}
