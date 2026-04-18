package main

import (
	"context"
	"database/sql"
	"fmt"
	"log"

	// TODO: SQLite 드라이버 import
	// _ "modernc.org/sqlite"

	// TODO: 생성된 db 패키지 import
	// "sqlc-learning/internal/db"
)

func main() {
	// TODO: 데이터베이스 연결
	// conn, err := sql.Open("sqlite", "blog.db")
	// if err != nil {
	//     log.Fatal(err)
	// }
	// defer conn.Close()

	// TODO: 스키마 초기화
	// if err := initSchema(conn); err != nil {
	//     log.Fatal(err)
	// }

	// TODO: sqlc Queries 객체 생성
	// queries := db.New(conn)

	// TODO: CRUD 테스트
	ctx := context.Background()

	// 게시글 생성
	// post, err := queries.CreatePost(ctx, db.CreatePostParams{
	//     Title:   "Hello World",
	//     Content: "My first post content",
	//     Status:  "draft",
	//     Author:  "john",
	// })

	// 게시글 조회
	// posts, err := queries.ListPosts(ctx)
	// for _, p := range posts {
	//     fmt.Printf("[%s] %s by %s\n", p.Status, p.Title, p.Author)
	// }

	// 게시글 상태 변경
	// updated, err := queries.UpdatePostStatus(ctx, db.UpdatePostStatusParams{
	//     Status: "published",
	//     ID:     post.ID,
	// })

	// 트랜잭션 예시
	// tx, _ := conn.BeginTx(ctx, nil)
	// qtx := queries.WithTx(tx)
	// // ... 작업 ...
	// tx.Commit() // 또는 tx.Rollback()

	fmt.Println("sqlc learning module")
	_ = ctx
}

// initSchema는 데이터베이스 스키마를 초기화합니다.
func initSchema(conn *sql.DB) error {
	schema := `
	CREATE TABLE IF NOT EXISTS posts (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		title TEXT NOT NULL,
		content TEXT NOT NULL,
		status TEXT NOT NULL DEFAULT 'draft',
		author TEXT NOT NULL,
		created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
		updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
	);

	CREATE INDEX IF NOT EXISTS idx_posts_status ON posts(status);
	CREATE INDEX IF NOT EXISTS idx_posts_author ON posts(author);
	`

	_, err := conn.Exec(schema)
	return err
}

// runWithTransaction은 트랜잭션 내에서 작업을 실행합니다.
// TODO: 트랜잭션 헬퍼 함수 구현
func runWithTransaction(ctx context.Context, conn *sql.DB, fn func(*sql.Tx) error) error {
	tx, err := conn.BeginTx(ctx, nil)
	if err != nil {
		return err
	}

	if err := fn(tx); err != nil {
		tx.Rollback()
		return err
	}

	return tx.Commit()
}
