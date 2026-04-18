package main

import (
	"fmt"
	"log"
	"os"
	"os/signal"
	"syscall"
)

func main() {
	// 서버 시작
	server, err := Serve(42069)
	if err != nil {
		log.Fatal("Failed to start server:", err)
	}
	defer server.Close()

	log.Println("HTTP Server listening on :42069")

	// Graceful shutdown 대기
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
	<-sigChan

	fmt.Println("\nServer shutting down...")
}
