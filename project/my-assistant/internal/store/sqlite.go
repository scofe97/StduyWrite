package store

import (
	"database/sql"
	"fmt"
	"time"

	_ "modernc.org/sqlite"
)

type Store struct {
	db *sql.DB
}

func New(dbPath string) (*Store, error) {
	db, err := sql.Open("sqlite", dbPath)
	if err != nil {
		return nil, fmt.Errorf("open db: %w", err)
	}

	// Enable WAL mode for better concurrent access
	if _, err := db.Exec("PRAGMA journal_mode=WAL"); err != nil {
		return nil, fmt.Errorf("set WAL mode: %w", err)
	}

	s := &Store{db: db}
	if err := s.migrate(); err != nil {
		return nil, fmt.Errorf("migrate: %w", err)
	}
	return s, nil
}

func (s *Store) Close() error {
	return s.db.Close()
}

func (s *Store) migrate() error {
	queries := []string{
		`CREATE TABLE IF NOT EXISTS conversations (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			chat_id INTEGER NOT NULL,
			role TEXT NOT NULL,
			content TEXT NOT NULL,
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP
		)`,
		`CREATE TABLE IF NOT EXISTS memos (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			chat_id INTEGER NOT NULL,
			title TEXT NOT NULL,
			content TEXT NOT NULL,
			tags TEXT DEFAULT '',
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
		)`,
		`CREATE TABLE IF NOT EXISTS reminders (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			chat_id INTEGER NOT NULL,
			message TEXT NOT NULL,
			cron_expr TEXT NOT NULL,
			one_shot INTEGER DEFAULT 0,
			active INTEGER DEFAULT 1,
			next_run DATETIME,
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP
		)`,
		`CREATE TABLE IF NOT EXISTS tool_logs (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			chat_id INTEGER NOT NULL,
			tool_name TEXT NOT NULL,
			input TEXT,
			output TEXT,
			error TEXT,
			duration_ms INTEGER,
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP
		)`,
		`CREATE INDEX IF NOT EXISTS idx_conversations_chat ON conversations(chat_id)`,
		`CREATE INDEX IF NOT EXISTS idx_memos_chat ON memos(chat_id)`,
		`CREATE INDEX IF NOT EXISTS idx_reminders_active ON reminders(active, next_run)`,
	}

	for _, q := range queries {
		if _, err := s.db.Exec(q); err != nil {
			return fmt.Errorf("exec %q: %w", q[:40], err)
		}
	}
	return nil
}

// --- Conversation ---

func (s *Store) SaveMessage(chatID int64, role, content string) error {
	_, err := s.db.Exec(
		"INSERT INTO conversations (chat_id, role, content) VALUES (?, ?, ?)",
		chatID, role, content,
	)
	return err
}

type Message struct {
	Role      string
	Content   string
	CreatedAt time.Time
}

func (s *Store) GetMessages(chatID int64, limit int) ([]Message, error) {
	rows, err := s.db.Query(
		`SELECT role, content, created_at FROM conversations
		 WHERE chat_id = ? ORDER BY id DESC LIMIT ?`,
		chatID, limit,
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var msgs []Message
	for rows.Next() {
		var m Message
		if err := rows.Scan(&m.Role, &m.Content, &m.CreatedAt); err != nil {
			return nil, err
		}
		msgs = append(msgs, m)
	}
	// Reverse to chronological order
	for i, j := 0, len(msgs)-1; i < j; i, j = i+1, j-1 {
		msgs[i], msgs[j] = msgs[j], msgs[i]
	}
	return msgs, nil
}

func (s *Store) ClearMessages(chatID int64) error {
	_, err := s.db.Exec("DELETE FROM conversations WHERE chat_id = ?", chatID)
	return err
}

// --- Memos ---

type Memo struct {
	ID        int64
	Title     string
	Content   string
	Tags      string
	CreatedAt time.Time
}

func (s *Store) SaveMemo(chatID int64, title, content, tags string) (int64, error) {
	res, err := s.db.Exec(
		"INSERT INTO memos (chat_id, title, content, tags) VALUES (?, ?, ?, ?)",
		chatID, title, content, tags,
	)
	if err != nil {
		return 0, err
	}
	return res.LastInsertId()
}

func (s *Store) SearchMemos(chatID int64, query string) ([]Memo, error) {
	rows, err := s.db.Query(
		`SELECT id, title, content, tags, created_at FROM memos
		 WHERE chat_id = ? AND (title LIKE ? OR content LIKE ? OR tags LIKE ?)
		 ORDER BY updated_at DESC LIMIT 20`,
		chatID, "%"+query+"%", "%"+query+"%", "%"+query+"%",
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var memos []Memo
	for rows.Next() {
		var m Memo
		if err := rows.Scan(&m.ID, &m.Title, &m.Content, &m.Tags, &m.CreatedAt); err != nil {
			return nil, err
		}
		memos = append(memos, m)
	}
	return memos, nil
}

func (s *Store) DeleteMemo(chatID, memoID int64) error {
	_, err := s.db.Exec("DELETE FROM memos WHERE id = ? AND chat_id = ?", memoID, chatID)
	return err
}

// --- Reminders ---

type Reminder struct {
	ID       int64
	ChatID   int64
	Message  string
	CronExpr string
	OneShot  bool
	Active   bool
	NextRun  time.Time
}

func (s *Store) SaveReminder(chatID int64, message, cronExpr string, oneShot bool, nextRun time.Time) (int64, error) {
	oneShotInt := 0
	if oneShot {
		oneShotInt = 1
	}
	res, err := s.db.Exec(
		"INSERT INTO reminders (chat_id, message, cron_expr, one_shot, next_run) VALUES (?, ?, ?, ?, ?)",
		chatID, message, cronExpr, oneShotInt, nextRun,
	)
	if err != nil {
		return 0, err
	}
	return res.LastInsertId()
}

func (s *Store) GetActiveReminders() ([]Reminder, error) {
	rows, err := s.db.Query(
		"SELECT id, chat_id, message, cron_expr, one_shot, next_run FROM reminders WHERE active = 1",
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var reminders []Reminder
	for rows.Next() {
		var r Reminder
		if err := rows.Scan(&r.ID, &r.ChatID, &r.Message, &r.CronExpr, &r.OneShot, &r.NextRun); err != nil {
			return nil, err
		}
		r.Active = true
		reminders = append(reminders, r)
	}
	return reminders, nil
}

func (s *Store) DeactivateReminder(id int64) error {
	_, err := s.db.Exec("UPDATE reminders SET active = 0 WHERE id = ?", id)
	return err
}

func (s *Store) UpdateNextRun(id int64, nextRun time.Time) error {
	_, err := s.db.Exec("UPDATE reminders SET next_run = ? WHERE id = ?", nextRun, id)
	return err
}

// --- Tool Logs ---

func (s *Store) LogToolCall(chatID int64, toolName, input, output, errStr string, durationMs int64) error {
	_, err := s.db.Exec(
		"INSERT INTO tool_logs (chat_id, tool_name, input, output, error, duration_ms) VALUES (?, ?, ?, ?, ?, ?)",
		chatID, toolName, input, output, errStr, durationMs,
	)
	return err
}
