-- 게시글 쿼리

-- name: GetPost :one
SELECT * FROM posts WHERE id = ?;

-- name: ListPosts :many
SELECT * FROM posts ORDER BY created_at DESC;

-- name: ListPostsByStatus :many
SELECT * FROM posts WHERE status = ? ORDER BY created_at DESC;

-- name: CreatePost :one
INSERT INTO posts (title, content, status, author)
VALUES (?, ?, ?, ?)
RETURNING *;

-- name: UpdatePost :one
UPDATE posts
SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP
WHERE id = ?
RETURNING *;

-- name: UpdatePostStatus :one
UPDATE posts
SET status = ?, updated_at = CURRENT_TIMESTAMP
WHERE id = ?
RETURNING *;

-- name: DeletePost :exec
DELETE FROM posts WHERE id = ?;
