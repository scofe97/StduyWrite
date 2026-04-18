package main

import (
	"bytes"
	"errors"
	"io"
	"strconv"
	"strings"
)

var CRLF = []byte("\r\n")

// ParserState는 파서의 현재 상태를 나타냅니다
type ParserState string

const (
	StateInit    ParserState = "init"
	StateHeaders ParserState = "headers"
	StateBody    ParserState = "body"
	StateDone    ParserState = "done"
	StateError   ParserState = "error"
)

// RequestLine은 HTTP 요청의 첫 번째 줄입니다
type RequestLine struct {
	Method        string
	RequestTarget string
	HttpVersion   string
}

// Request는 HTTP 요청 전체를 나타냅니다
type Request struct {
	RequestLine RequestLine
	Headers     *Headers
	Body        string
	state       ParserState
}

// NewRequest는 새 Request 인스턴스를 생성합니다
func NewRequest() *Request {
	return &Request{
		Headers: NewHeaders(),
		state:   StateInit,
	}
}

// Done은 파싱이 완료되었는지 확인합니다
func (r *Request) Done() bool {
	return r.state == StateDone
}

// Parse는 데이터를 점진적으로 파싱합니다
// 반환값: 소비한 바이트 수, 에러
func (r *Request) Parse(data []byte) (int, error) {
	read := 0

outer:
	for {
		currentData := data[read:]

		switch r.state {
		case StateInit:
			rl, n, err := parseRequestLine(currentData)
			if err != nil {
				r.state = StateError
				return read, err
			}
			if n == 0 {
				// 불완전한 데이터
				break outer
			}
			r.RequestLine = *rl
			r.state = StateHeaders
			read += n

		case StateHeaders:
			n, done, err := r.Headers.Parse(currentData)
			if err != nil {
				r.state = StateError
				return read, err
			}
			read += n
			if done {
				if r.hasBody() {
					r.state = StateBody
				} else {
					r.state = StateDone
				}
			}
			if n == 0 {
				break outer
			}

		case StateBody:
			n, err := r.parseBody(currentData)
			if err != nil {
				r.state = StateError
				return read, err
			}
			read += n
			if len(currentData) == 0 {
				break outer
			}

		case StateDone:
			break outer

		case StateError:
			return read, errors.New("request in error state")
		}
	}

	return read, nil
}

// hasBody는 요청에 본문이 있는지 확인합니다
func (r *Request) hasBody() bool {
	length := getContentLength(r.Headers)
	return length > 0
}

// parseBody는 본문을 파싱합니다
func (r *Request) parseBody(data []byte) (int, error) {
	length := getContentLength(r.Headers)
	if length == 0 {
		r.state = StateDone
		return 0, nil
	}

	remaining := length - len(r.Body)
	toRead := min(remaining, len(data))
	r.Body += string(data[:toRead])

	if len(r.Body) == length {
		r.state = StateDone
	}

	return toRead, nil
}

// getContentLength는 Content-Length 헤더 값을 가져옵니다
func getContentLength(h *Headers) int {
	value, exists := h.Get("Content-Length")
	if !exists {
		return 0
	}
	length, err := strconv.Atoi(value)
	if err != nil {
		return 0
	}
	return length
}

// parseRequestLine은 요청 라인을 파싱합니다
func parseRequestLine(data []byte) (*RequestLine, int, error) {
	idx := bytes.Index(data, CRLF)
	if idx == -1 {
		return nil, 0, nil
	}

	startLine := data[:idx]
	parts := bytes.Split(startLine, []byte(" "))
	if len(parts) != 3 {
		return nil, 0, errors.New("malformed request line")
	}

	httpParts := strings.Split(string(parts[2]), "/")
	if len(httpParts) != 2 || httpParts[0] != "HTTP" {
		return nil, 0, errors.New("malformed request line")
	}
	if httpParts[1] != "1.1" {
		return nil, 0, errors.New("unsupported HTTP version")
	}

	rl := &RequestLine{
		Method:        string(parts[0]),
		RequestTarget: string(parts[1]),
		HttpVersion:   httpParts[1],
	}

	return rl, idx + len(CRLF), nil
}

// RequestFromReader는 io.Reader에서 요청을 파싱합니다
func RequestFromReader(reader io.Reader) (*Request, error) {
	request := NewRequest()
	buf := make([]byte, 1024)
	bufLen := 0

	for !request.Done() {
		n, err := reader.Read(buf[bufLen:])
		if err != nil && err != io.EOF {
			return nil, err
		}
		if n == 0 && err == io.EOF {
			if !request.Done() {
				return nil, errors.New("unexpected EOF")
			}
			break
		}

		bufLen += n

		readN, err := request.Parse(buf[:bufLen])
		if err != nil {
			return nil, err
		}

		// 읽은 데이터 제거
		copy(buf, buf[readN:bufLen])
		bufLen -= readN
	}

	return request, nil
}

// min은 두 정수 중 작은 값을 반환합니다
func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
