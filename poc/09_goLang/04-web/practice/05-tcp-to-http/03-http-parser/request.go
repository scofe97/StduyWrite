package main

import (
	"bytes"
	"errors"
	"strings"
)

var CRLF = []byte("\r\n")

// RequestLine은 HTTP 요청의 첫 번째 줄을 나타냅니다
type RequestLine struct {
	Method        string // GET, POST, PUT, DELETE 등
	RequestTarget string // /path/to/resource
	HttpVersion   string // 1.1
}

// Request는 HTTP 요청 전체를 나타냅니다
type Request struct {
	RequestLine RequestLine
}

// parseRequestLine은 바이트 데이터에서 요청 라인을 파싱합니다
// 반환값: RequestLine, 읽은 바이트 수, 에러
func parseRequestLine(data []byte) (*RequestLine, int, error) {
	// 1. CRLF 위치 찾기
	idx := bytes.Index(data, CRLF)
	if idx == -1 {
		// 아직 완전한 줄이 없음 - 더 많은 데이터 필요
		return nil, 0, nil
	}

	// 2. 첫 번째 줄 추출
	startLine := data[:idx]

	// 3. 공백으로 분리 (정확히 3개 부분이어야 함)
	parts := bytes.Split(startLine, []byte(" "))
	if len(parts) != 3 {
		return nil, 0, errors.New("malformed request line")
	}

	// 4. HTTP 버전 검증
	httpParts := strings.Split(string(parts[2]), "/")
	if len(httpParts) != 2 || httpParts[0] != "HTTP" {
		return nil, 0, errors.New("malformed request line")
	}
	if httpParts[1] != "1.1" {
		return nil, 0, errors.New("unsupported HTTP version")
	}

	// 5. RequestLine 생성
	rl := &RequestLine{
		Method:        string(parts[0]),
		RequestTarget: string(parts[1]),
		HttpVersion:   httpParts[1],
	}

	// 6. 읽은 바이트 수 = 줄 길이 + CRLF 길이
	return rl, idx + len(CRLF), nil
}
