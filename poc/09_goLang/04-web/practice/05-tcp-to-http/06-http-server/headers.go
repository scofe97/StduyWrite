package main

import (
	"bytes"
	"errors"
	"strings"
)

type Headers struct {
	headers map[string]string
}

func NewHeaders() *Headers {
	return &Headers{
		headers: make(map[string]string),
	}
}

func (h *Headers) Get(name string) (string, bool) {
	name = strings.ToLower(name)
	value, exists := h.headers[name]
	return value, exists
}

func (h *Headers) Set(name, value string) {
	name = strings.ToLower(name)
	if existing, exists := h.headers[name]; exists {
		h.headers[name] = existing + ", " + value
	} else {
		h.headers[name] = value
	}
}

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

func (h *Headers) ForEach(cb func(name, value string)) {
	for name, value := range h.headers {
		cb(name, value)
	}
}
