package tools

import (
	"context"
	"encoding/json"
	"fmt"
	"strings"
	"time"

	"my-assistant/internal/store"
)

// ReminderTool allows the agent to set, list, and cancel reminders.
type ReminderTool struct {
	store      *store.Store
	chatID     int64
	registerFn func(id int64, cronExpr string)
}

func NewReminderTool(s *store.Store, chatID int64, registerFn func(int64, string)) *ReminderTool {
	return &ReminderTool{store: s, chatID: chatID, registerFn: registerFn}
}

func (t *ReminderTool) Name() string { return "reminder" }

func (t *ReminderTool) Description() string {
	return "알림을 설정, 조회, 취소합니다. cron 표현식을 사용하여 반복 알림이나 일회성 알림을 만들 수 있습니다."
}

func (t *ReminderTool) InputSchema() json.RawMessage {
	return json.RawMessage(`{
		"type": "object",
		"properties": {
			"action": {
				"type": "string",
				"enum": ["set", "list", "cancel"],
				"description": "수행할 작업: set(설정), list(조회), cancel(취소)"
			},
			"message": {
				"type": "string",
				"description": "알림 메시지 (set 액션에 필요)"
			},
			"cron_expr": {
				"type": "string",
				"description": "cron 표현식 (예: '0 9 * * *' = 매일 오전 9시, set 액션에 필요)"
			},
			"one_shot": {
				"type": "boolean",
				"description": "true이면 한 번만 실행되는 일회성 알림 (기본값: false)"
			},
			"reminder_id": {
				"type": "integer",
				"description": "알림 ID (cancel 액션에 필요)"
			}
		},
		"required": ["action"]
	}`)
}

type reminderInput struct {
	Action     string `json:"action"`
	Message    string `json:"message"`
	CronExpr   string `json:"cron_expr"`
	OneShot    bool   `json:"one_shot"`
	ReminderID int64  `json:"reminder_id"`
}

func (t *ReminderTool) Execute(_ context.Context, input json.RawMessage) (string, error) {
	var in reminderInput
	if err := json.Unmarshal(input, &in); err != nil {
		return "", fmt.Errorf("입력 파싱 오류: %w", err)
	}

	switch in.Action {
	case "set":
		return t.set(in)
	case "list":
		return t.list()
	case "cancel":
		return t.cancel(in)
	default:
		return "", fmt.Errorf("알 수 없는 액션: %q (set/list/cancel 중 하나여야 합니다)", in.Action)
	}
}

func (t *ReminderTool) set(in reminderInput) (string, error) {
	if in.Message == "" {
		return "", fmt.Errorf("set 액션에는 message가 필요합니다")
	}
	if in.CronExpr == "" {
		return "", fmt.Errorf("set 액션에는 cron_expr이 필요합니다")
	}

	id, err := t.store.SaveReminder(t.chatID, in.Message, in.CronExpr, in.OneShot, time.Now())
	if err != nil {
		return "", fmt.Errorf("알림 저장 실패: %w", err)
	}

	if t.registerFn != nil {
		t.registerFn(id, in.CronExpr)
	}

	kind := "반복"
	if in.OneShot {
		kind = "일회성"
	}
	return fmt.Sprintf("%s 알림이 설정되었습니다. (ID: %d, 스케줄: %q, 메시지: %q)", kind, id, in.CronExpr, in.Message), nil
}

func (t *ReminderTool) list() (string, error) {
	reminders, err := t.store.GetActiveReminders()
	if err != nil {
		return "", fmt.Errorf("알림 조회 실패: %w", err)
	}

	// Filter to current chat
	var mine []store.Reminder
	for _, r := range reminders {
		if r.ChatID == t.chatID {
			mine = append(mine, r)
		}
	}

	if len(mine) == 0 {
		return "활성화된 알림이 없습니다.", nil
	}

	var sb strings.Builder
	fmt.Fprintf(&sb, "활성 알림: %d개\n\n", len(mine))
	for _, r := range mine {
		kind := "반복"
		if r.OneShot {
			kind = "일회성"
		}
		fmt.Fprintf(&sb, "ID: %d\n", r.ID)
		fmt.Fprintf(&sb, "메시지: %s\n", r.Message)
		fmt.Fprintf(&sb, "스케줄: %s (%s)\n", r.CronExpr, kind)
		fmt.Fprintf(&sb, "다음 실행: %s\n", r.NextRun.Format("2006-01-02 15:04:05"))
		fmt.Fprintln(&sb, "---")
	}
	return sb.String(), nil
}

func (t *ReminderTool) cancel(in reminderInput) (string, error) {
	if in.ReminderID == 0 {
		return "", fmt.Errorf("cancel 액션에는 reminder_id가 필요합니다")
	}
	if err := t.store.DeactivateReminder(in.ReminderID); err != nil {
		return "", fmt.Errorf("알림 취소 실패: %w", err)
	}
	return fmt.Sprintf("알림 (ID: %d)이 취소되었습니다.", in.ReminderID), nil
}
