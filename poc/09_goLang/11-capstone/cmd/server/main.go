package main

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	// TODO: 내부 패키지 import
	// "blog-api/internal/api"
	// "blog-api/internal/config"
	// "blog-api/internal/repository"
)

func main() {
	// TODO: 1. 설정 로드
	// cfg, err := config.Load("configs/config.yaml")
	// if err != nil {
	//     log.Fatalf("Failed to load config: %v", err)
	// }

	// TODO: 2. 로거 초기화
	// logger := setupLogger(cfg.Log.Level, cfg.Log.Format)
	// logger.Info().Msg("Starting Blog API server")

	// TODO: 3. 데이터베이스 연결
	// db, err := repository.NewDB(cfg.Database.Path)
	// if err != nil {
	//     logger.Fatal().Err(err).Msg("Failed to connect database")
	// }
	// defer db.Close()

	// TODO: 4. 라우터 설정
	// router := api.NewRouter(db, logger)

	// TODO: 5. 서버 시작 (그레이스풀 셧다운)
	// startServer(cfg.Server.Host, cfg.Server.Port, router, logger)

	fmt.Println("Blog API Capstone - Run 'sqlc generate' first!")
	fmt.Println("Server would start on :8080")

	// 임시 서버
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte(`{"message": "Blog API - Work in progress"}`))
	})
	http.ListenAndServe(":8080", nil)
}

// startServer는 그레이스풀 셧다운을 지원하는 서버를 시작합니다.
func startServer(host string, port int, handler http.Handler) {
	addr := fmt.Sprintf("%s:%d", host, port)

	srv := &http.Server{
		Addr:         addr,
		Handler:      handler,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	// 서버 시작 (고루틴)
	go func() {
		fmt.Printf("Server starting on %s\n", addr)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			fmt.Printf("Server error: %v\n", err)
			os.Exit(1)
		}
	}()

	// 시그널 대기
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	fmt.Println("\nShutting down server...")

	// 그레이스풀 셧다운 (5초 타임아웃)
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		fmt.Printf("Server forced to shutdown: %v\n", err)
	}

	fmt.Println("Server exited properly")
}
