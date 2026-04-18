package tools

import (
	"context"
	"encoding/json"
	"fmt"
	"strings"

	"my-assistant/internal/store"
)

// MemoTool allows the agent to save, search, and delete memos.
type MemoTool struct {
	store  *store.Store
	chatID int64
}

func NewMemoTool(s *store.Store, chatID int64) *MemoTool {
	return &MemoTool{store: s, chatID: chatID}
}

func (t *MemoTool) Name() string { return "memo" }

func (t *MemoTool) Description() string {
	return "메모를 저장, 검색, 삭제합니다. 중요한 정보나 나중에 참조할 내용을 기억하는 데 사용합니다."
}

func (t *MemoTool) InputSchema() json.RawMessage {
	return json.RawMessage(`{
		"type": "object",
		"properties": {
			"action": {
				"type": "string",
				"enum": ["save", "search", "delete"],
				"description": "수행할 작업: save(저장), search(검색), delete(삭제)"
			},
			"title": {
				"type": "string",
				"description": "메모 제목 (save 액션에 필요)"
			},
			"content": {
				"type": "string",
				"description": "메모 내용 (save 액션에 필요)"
			},
			"tags": {
				"type": "string",
				"description": "쉼표로 구분된 태그 목록 (save 액션에 선택적)"
			},
			"query": {
				"type": "string",
				"description": "검색어 (search 액션에 필요)"
			},
			"memo_id": {
				"type": "integer",
				"description": "메모 ID (delete 액션에 필요)"
			}
		},
		"required": ["action"]
	}`)
}

type memoInput struct {
	Action  string `json:"action"`
	Title   string `json:"title"`
	Content string `json:"content"`
	Tags    string `json:"tags"`
	Query   string `json:"query"`
	MemoID  int64  `json:"memo_id"`
}

func (t *MemoTool) Execute(_ context.Context, input json.RawMessage) (string, error) {
	var in memoInput
	if err := json.Unmarshal(input, &in); err != nil {
		return "", fmt.Errorf("입력 파싱 오류: %w", err)
	}

	switch in.Action {
	case "save":
		return t.save(in)
	case "search":
		return t.search(in)
	case "delete":
		return t.delete(in)
	default:
		return "", fmt.Errorf("알 수 없는 액션: %q (save/search/delete 중 하나여야 합니다)", in.Action)
	}
}

func (t *MemoTool) save(in memoInput) (string, error) {
	if in.Title == "" {
		return "", fmt.Errorf("save 액션에는 title이 필요합니다")
	}
	if in.Content == "" {
		return "", fmt.Errorf("save 액션에는 content가 필요합니다")
	}
	id, err := t.store.SaveMemo(t.chatID, in.Title, in.Content, in.Tags)
	if err != nil {
		return "", fmt.Errorf("메모 저장 실패: %w", err)
	}
	return fmt.Sprintf("메모가 저장되었습니다. (ID: %d, 제목: %q)", id, in.Title), nil
}

func (t *MemoTool) search(in memoInput) (string, error) {
	if in.Query == "" {
		return "", fmt.Errorf("search 액션에는 query가 필요합니다")
	}
	memos, err := t.store.SearchMemos(t.chatID, in.Query)
	if err != nil {
		return "", fmt.Errorf("메모 검색 실패: %w", err)
	}
	if len(memos) == 0 {
		return fmt.Sprintf("%q에 대한 검색 결과가 없습니다.", in.Query), nil
	}

	var sb strings.Builder
	fmt.Fprintf(&sb, "검색 결과: %d개의 메모\n\n", len(memos))
	for _, m := range memos {
		fmt.Fprintf(&sb, "ID: %d\n", m.ID)
		fmt.Fprintf(&sb, "제목: %s\n", m.Title)
		fmt.Fprintf(&sb, "내용: %s\n", m.Content)
		if m.Tags != "" {
			fmt.Fprintf(&sb, "태그: %s\n", m.Tags)
		}
		fmt.Fprintf(&sb, "생성일: %s\n", m.CreatedAt.Format("2006-01-02 15:04"))
		fmt.Fprintln(&sb, "---")
	}
	return sb.String(), nil
}

func (t *MemoTool) delete(in memoInput) (string, error) {
	if in.MemoID == 0 {
		return "", fmt.Errorf("delete 액션에는 memo_id가 필요합니다")
	}
	if err := t.store.DeleteMemo(t.chatID, in.MemoID); err != nil {
		return "", fmt.Errorf("메모 삭제 실패: %w", err)
	}
	return fmt.Sprintf("메모 (ID: %d)가 삭제되었습니다.", in.MemoID), nil
}
