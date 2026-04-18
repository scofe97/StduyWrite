package handlers

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"strconv"

	"blog-api/internal/domain"

	"github.com/go-chi/chi/v5"
	"github.com/rs/zerolog"
)

// Handler는 HTTP 핸들러입니다.
type Handler struct {
	db     *sql.DB
	logger zerolog.Logger
	// queries *repository.Queries  // sqlc 생성 후 추가
}

// NewHandler는 새 핸들러를 생성합니다.
func NewHandler(db *sql.DB, logger zerolog.Logger) *Handler {
	return &Handler{
		db:     db,
		logger: logger,
		// queries: repository.New(db),
	}
}

// Response는 API 응답 구조체입니다.
type Response struct {
	Success bool        `json:"success"`
	Data    interface{} `json:"data,omitempty"`
	Error   string      `json:"error,omitempty"`
}

// CreatePostRequest는 게시글 생성 요청입니다.
type CreatePostRequest struct {
	Title   string `json:"title"`
	Content string `json:"content"`
	Author  string `json:"author"`
}

// UpdatePostRequest는 게시글 수정 요청입니다.
type UpdatePostRequest struct {
	Title   string `json:"title"`
	Content string `json:"content"`
}

// ListPosts는 게시글 목록을 반환합니다.
// TODO: sqlc 생성 후 구현
func (h *Handler) ListPosts(w http.ResponseWriter, r *http.Request) {
	// posts, err := h.queries.ListPosts(r.Context())
	// if err != nil {
	//     respondError(w, http.StatusInternalServerError, "Failed to list posts")
	//     return
	// }
	// respondJSON(w, http.StatusOK, posts)

	respondJSON(w, http.StatusOK, []interface{}{})
}

// GetPost는 특정 게시글을 반환합니다.
// TODO: sqlc 생성 후 구현
func (h *Handler) GetPost(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil {
		respondError(w, http.StatusBadRequest, "Invalid ID")
		return
	}

	// post, err := h.queries.GetPost(r.Context(), id)
	// if err == sql.ErrNoRows {
	//     respondError(w, http.StatusNotFound, "Post not found")
	//     return
	// }
	// if err != nil {
	//     respondError(w, http.StatusInternalServerError, "Failed to get post")
	//     return
	// }
	// respondJSON(w, http.StatusOK, post)

	respondJSON(w, http.StatusOK, map[string]int64{"id": id})
}

// CreatePost는 새 게시글을 생성합니다.
// TODO: sqlc 생성 후 구현
func (h *Handler) CreatePost(w http.ResponseWriter, r *http.Request) {
	var req CreatePostRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		respondError(w, http.StatusBadRequest, "Invalid request body")
		return
	}

	if req.Title == "" || req.Author == "" {
		respondError(w, http.StatusBadRequest, "Title and author are required")
		return
	}

	// 도메인 객체 생성
	post := domain.NewPost(req.Title, req.Content, req.Author)

	h.logger.Info().
		Str("title", post.Title).
		Str("author", post.Author).
		Msg("Creating new post")

	// post, err := h.queries.CreatePost(r.Context(), repository.CreatePostParams{
	//     Title:   req.Title,
	//     Content: req.Content,
	//     Status:  post.Status,
	//     Author:  req.Author,
	// })
	// if err != nil {
	//     respondError(w, http.StatusInternalServerError, "Failed to create post")
	//     return
	// }
	// respondJSON(w, http.StatusCreated, post)

	respondJSON(w, http.StatusCreated, post)
}

// UpdatePost는 게시글을 수정합니다.
// TODO: sqlc 생성 후 구현
func (h *Handler) UpdatePost(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil {
		respondError(w, http.StatusBadRequest, "Invalid ID")
		return
	}

	var req UpdatePostRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		respondError(w, http.StatusBadRequest, "Invalid request body")
		return
	}

	// post, err := h.queries.UpdatePost(r.Context(), repository.UpdatePostParams{
	//     Title:   req.Title,
	//     Content: req.Content,
	//     ID:      id,
	// })
	// respondJSON(w, http.StatusOK, post)

	respondJSON(w, http.StatusOK, map[string]interface{}{"id": id, "title": req.Title})
}

// DeletePost는 게시글을 삭제합니다.
// TODO: sqlc 생성 후 구현
func (h *Handler) DeletePost(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil {
		respondError(w, http.StatusBadRequest, "Invalid ID")
		return
	}

	// err = h.queries.DeletePost(r.Context(), id)
	// if err != nil {
	//     respondError(w, http.StatusInternalServerError, "Failed to delete post")
	//     return
	// }

	h.logger.Info().Int64("id", id).Msg("Post deleted")
	w.WriteHeader(http.StatusNoContent)
}

// PublishPost는 게시글을 발행합니다.
// TODO: FSM 통합 구현
func (h *Handler) PublishPost(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil {
		respondError(w, http.StatusBadRequest, "Invalid ID")
		return
	}

	// 1. DB에서 게시글 로드
	// dbPost, err := h.queries.GetPost(r.Context(), id)

	// 2. 도메인 객체로 변환
	// post := domain.FromRepository(dbPost.ID, dbPost.Title, ...)

	// 3. FSM 상태 전이
	// if err := post.Publish(); err != nil {
	//     respondError(w, http.StatusBadRequest, err.Error())
	//     return
	// }

	// 4. DB 업데이트
	// updated, err := h.queries.UpdatePostStatus(r.Context(), repository.UpdatePostStatusParams{
	//     Status: post.Status,
	//     ID:     id,
	// })

	h.logger.Info().Int64("id", id).Msg("Post published")
	respondJSON(w, http.StatusOK, map[string]interface{}{"id": id, "status": "published"})
}

// ArchivePost는 게시글을 보관합니다.
// TODO: FSM 통합 구현
func (h *Handler) ArchivePost(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil {
		respondError(w, http.StatusBadRequest, "Invalid ID")
		return
	}

	// 동일한 패턴으로 구현
	// post.Archive() 호출 후 DB 업데이트

	h.logger.Info().Int64("id", id).Msg("Post archived")
	respondJSON(w, http.StatusOK, map[string]interface{}{"id": id, "status": "archived"})
}

// --- 유틸리티 함수 ---

func respondJSON(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(Response{Success: true, Data: data})
}

func respondError(w http.ResponseWriter, status int, message string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(Response{Success: false, Error: message})
}
