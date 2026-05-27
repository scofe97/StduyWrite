package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
)

// 과제 2: Graceful Shutdown 서버
// SIGTERM 신호를 받으면 진행 중인 요청을 완료한 후 종료하는 HTTP 서버를 구현하세요.

// 느린 핸들러 (실제 처리 시간을 시뮬레이션)
func slowHandler(w http.ResponseWriter, r *http.Request) {
	log.Println("요청 처리 시작...")

	// 5초간 처리 (긴 작업 시뮬레이션)
	select {
	case <-time.After(5 * time.Second):
		log.Println("요청 처리 완료")
		fmt.Fprintln(w, "처리 완료!")
	case <-r.Context().Done():
		// 클라이언트가 연결을 끊거나 서버가 종료 중
		log.Println("요청 취소됨:", r.Context().Err())
		return
	}
}

// 빠른 핸들러
func fastHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "Hello, World!")
}

// 상태 확인 핸들러
func healthHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "OK")
}

func main() {
	fmt.Println("=== Graceful Shutdown 서버 ===\n")

	// TODO 1: HTTP 서버 설정
	mux := http.NewServeMux()
	mux.HandleFunc("/slow", slowHandler)
	mux.HandleFunc("/fast", fastHandler)
	mux.HandleFunc("/health", healthHandler)

	server := &http.Server{
		Addr:    ":8080",
		Handler: mux,
	}

	// TODO 2: 서버를 고루틴에서 시작
	// go func() {
	//     log.Println("서버 시작: http://localhost:8080")
	//     if err := server.ListenAndServe(); err != http.ErrServerClosed {
	//         log.Fatal("서버 에러:", err)
	//     }
	// }()

	// TODO 3: 종료 신호 대기 (SIGINT, SIGTERM)
	// quit := make(chan os.Signal, 1)
	// signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	// <-quit
	// log.Println("종료 신호 수신, 서버 종료 중...")

	// TODO 4: Graceful Shutdown 실행
	// - 30초 타임아웃 설정
	// - server.Shutdown(ctx) 호출
	// - 진행 중인 요청이 완료될 때까지 대기
	// ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	// defer cancel()
	//
	// if err := server.Shutdown(ctx); err != nil {
	//     log.Fatal("강제 종료:", err)
	// }
	// log.Println("서버 종료 완료")

	fmt.Println("TODO: Graceful Shutdown 서버 구현")
	fmt.Println("\n테스트 방법:")
	fmt.Println("1. 서버 시작 후 curl http://localhost:8080/slow 실행")
	fmt.Println("2. 요청 처리 중에 Ctrl+C로 서버 종료 시도")
	fmt.Println("3. 진행 중인 요청이 완료된 후 서버가 종료되는지 확인")
}

// 힌트:
// 1. server.Shutdown(ctx)는 새 연결을 거부하고 기존 연결이 완료될 때까지 대기
// 2. ctx가 취소되면 강제 종료 (기존 연결도 끊김)
// 3. 클라이언트 연결이 끊기면 r.Context().Done()이 닫힘

// 추가 참고: Shutdown 동작
// - 새 연결 수락 중지
// - 활성 연결의 요청 완료 대기
// - ctx 타임아웃 시 즉시 종료

var _ = os.Interrupt
var _ = signal.Notify
var _ = syscall.SIGTERM
var _ = context.Background
