package main

import (
	"bytes"
	"errors"
	"strings"
)

var CRLF = []byte("\r\n")

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

	// 중복 헤더 처리: 콤마로 연결
	if existing, exists := h.headers[name]; exists {
		h.headers[name] = existing + ", " + value
	} else {
		h.headers[name] = value
	}
}

// Parse는 바이트 데이터에서 헤더를 파싱합니다
// 반환값: 소비한 바이트 수, 헤더 종료 여부, 에러
func (h *Headers) Parse(data []byte) (int, bool, error) {
	read := 0

	for {
		// 1. CRLF 위치 찾기
		idx := bytes.Index(data[read:], CRLF)
		if idx == -1 {
			// 완전한 줄이 없음 - 더 많은 데이터 필요
			return read, false, nil
		}

		// 2. 빈 줄 확인 (헤더 종료)
		if idx == 0 {
			read += len(CRLF)
			return read, true, nil
		}

		// 3. 헤더 라인 파싱
		line := data[read : read+idx]
		name, value, err := parseFieldLine(line)
		if err != nil {
			return read, false, err
		}

		// 4. 헤더 저장
		h.Set(name, value)

		// 5. 읽은 위치 업데이트
		read += idx + len(CRLF)
	}
}

// parseFieldLine은 단일 헤더 라인을 파싱합니다
func parseFieldLine(line []byte) (string, string, error) {
	// 콜론으로 분리 (최대 2개)
	parts := bytes.SplitN(line, []byte(":"), 2)
	if len(parts) != 2 {
		return "", "", errors.New("malformed field line")
	}

	name := parts[0]
	value := parts[1]

	// 필드 이름에 공백이 있으면 에러
	if bytes.HasSuffix(name, []byte(" ")) {
		return "", "", errors.New("malformed field line: space before colon")
	}

	// 값 앞뒤 공백 제거
	value = bytes.TrimSpace(value)

	return string(name), string(value), nil
}

// ForEach는 모든 헤더를 순회합니다
func (h *Headers) ForEach(cb func(name, value string)) {
	for name, value := range h.headers {
		cb(name, value)
	}
}
