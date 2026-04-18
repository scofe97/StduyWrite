package main

import (
	"fmt"
	"io"
	"log"
	"net"
)

// Server는 HTTP 서버를 나타냅니다
type Server struct {
	port     int
	listener net.Listener
	closed   bool
}

// Serve는 지정된 포트에서 HTTP 서버를 시작합니다
func Serve(port int) (*Server, error) {
	listener, err := net.Listen("tcp", fmt.Sprintf(":%d", port))
	if err != nil {
		return nil, err
	}

	server := &Server{
		port:     port,
		listener: listener,
	}

	// 백그라운드에서 연결 수락
	go server.acceptLoop()

	return server, nil
}

// acceptLoop은 연결을 계속 수락합니다
func (s *Server) acceptLoop() {
	for !s.closed {
		conn, err := s.listener.Accept()
		if err != nil {
			if !s.closed {
				log.Println("Accept error:", err)
			}
			continue
		}

		// 각 연결을 고루틴으로 처리
		go handleConnection(conn)
	}
}

// Close는 서버를 종료합니다
func (s *Server) Close() error {
	s.closed = true
	return s.listener.Close()
}

// handleConnection은 단일 HTTP 연결을 처리합니다
func handleConnection(conn net.Conn) {
	defer conn.Close()

	// 1. 요청 파싱
	request, err := RequestFromReader(conn)
	if err != nil {
		log.Println("Parse error:", err)
		WriteStatusLine(conn, 400)
		return
	}

	// 2. 요청 정보 로깅
	log.Printf("%s %s HTTP/%s",
		request.RequestLine.Method,
		request.RequestLine.RequestTarget,
		request.RequestLine.HttpVersion)

	// 3. 응답 작성
	body := "Hello, World!"

	WriteStatusLine(conn, 200)
	headers := GetDefaultHeaders(len(body))
	WriteHeaders(conn, headers)
	conn.Write([]byte(body))
}

// WriteStatusLine은 HTTP 상태 라인을 작성합니다
func WriteStatusLine(w io.Writer, statusCode int) error {
	var statusLine string
	switch statusCode {
	case 200:
		statusLine = "HTTP/1.1 200 OK\r\n"
	case 400:
		statusLine = "HTTP/1.1 400 Bad Request\r\n"
	case 404:
		statusLine = "HTTP/1.1 404 Not Found\r\n"
	case 500:
		statusLine = "HTTP/1.1 500 Internal Server Error\r\n"
	default:
		return fmt.Errorf("unrecognized status code: %d", statusCode)
	}
	_, err := w.Write([]byte(statusLine))
	return err
}

// GetDefaultHeaders는 기본 응답 헤더를 생성합니다
func GetDefaultHeaders(contentLength int) *Headers {
	headers := NewHeaders()
	headers.Set("Content-Length", fmt.Sprintf("%d", contentLength))
	headers.Set("Content-Type", "text/plain")
	headers.Set("Connection", "close")
	return headers
}

// WriteHeaders는 헤더를 작성합니다
func WriteHeaders(w io.Writer, h *Headers) error {
	h.ForEach(func(name, value string) {
		fmt.Fprintf(w, "%s: %s\r\n", name, value)
	})
	_, err := w.Write([]byte("\r\n"))
	return err
}
