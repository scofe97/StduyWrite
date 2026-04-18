package main

import (
	"fmt"
	"io"
	"net"
)

func main() {
	// 1. TCP 리스너 생성 (포트 42069)
	listener, err := net.Listen("tcp", ":42069")
	if err != nil {
		fmt.Println("Error creating listener:", err)
		return
	}
	defer listener.Close()

	fmt.Println("TCP Server listening on :42069")

	// 무한 루프로 연결 수락
	for {
		// 2. 연결 수락 (블로킹 호출)
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("Error accepting connection:", err)
			continue
		}

		// 3. 연결 처리 (고루틴으로 동시 처리)
		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()

	fmt.Println("New connection from:", conn.RemoteAddr())

	// 버퍼 생성
	buf := make([]byte, 1024)

	for {
		// 데이터 읽기
		n, err := conn.Read(buf)
		if err == io.EOF {
			fmt.Println("Connection closed by client")
			break
		}
		if err != nil {
			fmt.Println("Error reading:", err)
			break
		}

		// 수신 데이터 출력
		fmt.Printf("Received %d bytes: %s", n, buf[:n])
	}
}
