-- 게시글 쿼리

-- name: GetPost :one
-- 단일 게시글 조회
SELECT * FROM posts
WHERE id = ?;

-- name: ListPosts :many
-- 모든 게시글 조회 (최신순)
SELECT * FROM posts
ORDER BY created_at DESC;

-- name: ListPostsByStatus :many
-- 상태별 게시글 조회
SELECT * FROM posts
WHERE status = ?
ORDER BY created_at DESC;

-- name: ListPostsByAuthor :many
-- 작성자별 게시글 조회
SELECT * FROM posts
WHERE author = ?
ORDER BY created_at DESC;

-- name: CreatePost :one
-- 게시글 생성
INSERT INTO posts (title, content, status, author)
VALUES (?, ?, ?, ?)
RETURNING *;

-- name: UpdatePost :one
-- 게시글 수정
UPDATE posts
SET title = ?,
    content = ?,
    updated_at = CURRENT_TIMESTAMP
WHERE id = ?
RETURNING *;

-- name: UpdatePostStatus :one
-- 게시글 상태 변경
UPDATE posts
SET status = ?,
    updated_at = CURRENT_TIMESTAMP
WHERE id = ?
RETURNING *;

-- name: DeletePost :exec
-- 게시글 삭제
DELETE FROM posts
WHERE id = ?;

-- name: CountPostsByStatus :one
-- 상태별 게시글 수
SELECT COUNT(*) FROM posts
WHERE status = ?;

-- name: SearchPosts :many
-- 제목/내용 검색
SELECT * FROM posts
WHERE title LIKE ? OR content LIKE ?
ORDER BY created_at DESC;
