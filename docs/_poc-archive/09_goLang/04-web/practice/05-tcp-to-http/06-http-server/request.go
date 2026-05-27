package main

import (
	"bytes"
	"errors"
	"io"
	"strconv"
	"strings"
)

var CRLF = []byte("\r\n")

type ParserState string

const (
	StateInit    ParserState = "init"
	StateHeaders ParserState = "headers"
	StateBody    ParserState = "body"
	StateDone    ParserState = "done"
	StateError   ParserState = "error"
)

type RequestLine struct {
	Method        string
	RequestTarget string
	HttpVersion   string
}

type Request struct {
	RequestLine RequestLine
	Headers     *Headers
	Body        string
	state       ParserState
}

func NewRequest() *Request {
	return &Request{
		Headers: NewHeaders(),
		state:   StateInit,
	}
}

func (r *Request) Done() bool {
	return r.state == StateDone
}

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

func (r *Request) hasBody() bool {
	length := getContentLength(r.Headers)
	return length > 0
}

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

		copy(buf, buf[readN:bufLen])
		bufLen -= readN
	}

	return request, nil
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
