package main

import (
	"crypto/sha256"
	"fmt"
	"io"
)

// WriteChunkedBody는 청크 형식으로 데이터를 작성합니다
func WriteChunkedBody(w io.Writer, data []byte) error {
	if len(data) == 0 {
		return nil
	}

	// 1. 청크 크기 (16진수) + CRLF
	size := fmt.Sprintf("%x\r\n", len(data))
	if _, err := w.Write([]byte(size)); err != nil {
		return err
	}

	// 2. 데이터
	if _, err := w.Write(data); err != nil {
		return err
	}

	// 3. CRLF
	_, err := w.Write([]byte("\r\n"))
	return err
}

// WriteChunkedEnd는 청크 전송 종료를 작성합니다
func WriteChunkedEnd(w io.Writer) error {
	// 크기 0 청크 + 빈 줄
	_, err := w.Write([]byte("0\r\n\r\n"))
	return err
}

// WriteTrailers는 트레일러 헤더를 작성합니다
func WriteTrailers(w io.Writer, trailers *Headers) error {
	trailers.ForEach(func(name, value string) {
		fmt.Fprintf(w, "%s: %s\r\n", name, value)
	})
	_, err := w.Write([]byte("\r\n"))
	return err
}

// CalculateSHA256은 데이터의 SHA-256 해시를 계산합니다
func CalculateSHA256(data []byte) string {
	hash := sha256.Sum256(data)
	return fmt.Sprintf("%x", hash)
}

// StreamWithChunks는 Reader에서 데이터를 읽어 청크로 전송합니다
func StreamWithChunks(w io.Writer, r io.Reader, bufferSize int) ([]byte, error) {
	var fullBody []byte
	buf := make([]byte, bufferSize)

	for {
		n, err := r.Read(buf)
		if err != nil && err != io.EOF {
			return fullBody, err
		}

		if n > 0 {
			fullBody = append(fullBody, buf[:n]...)
			if err := WriteChunkedBody(w, buf[:n]); err != nil {
				return fullBody, err
			}
		}

		if err == io.EOF {
			break
		}
	}

	return fullBody, WriteChunkedEnd(w)
}

// StreamWithTrailers는 청크 전송 후 트레일러를 추가합니다
func StreamWithTrailers(w io.Writer, r io.Reader, bufferSize int) error {
	// 1. 청크로 스트리밍하며 전체 본문 수집
	fullBody, err := StreamWithChunksNoEnd(w, r, bufferSize)
	if err != nil {
		return err
	}

	// 2. 종료 청크 작성
	if _, err := w.Write([]byte("0\r\n")); err != nil {
		return err
	}

	// 3. 트레일러 작성
	trailers := NewHeaders()
	trailers.Set("X-Checksum", CalculateSHA256(fullBody))
	trailers.Set("X-Content-Length", fmt.Sprintf("%d", len(fullBody)))

	return WriteTrailers(w, trailers)
}

// StreamWithChunksNoEnd는 종료 청크 없이 스트리밍합니다
func StreamWithChunksNoEnd(w io.Writer, r io.Reader, bufferSize int) ([]byte, error) {
	var fullBody []byte
	buf := make([]byte, bufferSize)

	for {
		n, err := r.Read(buf)
		if err != nil && err != io.EOF {
			return fullBody, err
		}

		if n > 0 {
			fullBody = append(fullBody, buf[:n]...)
			if err := WriteChunkedBody(w, buf[:n]); err != nil {
				return fullBody, err
			}
		}

		if err == io.EOF {
			break
		}
	}

	return fullBody, nil
}
