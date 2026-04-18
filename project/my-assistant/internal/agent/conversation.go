package agent

import (
	"sync"

	"github.com/anthropics/anthropic-sdk-go"

	"my-assistant/internal/store"
)

// Conversation manages per-chat message history for the ReAct loop.
type Conversation struct {
	mu       sync.Mutex
	store    *store.Store
	limit    int
	// In-memory cache of current conversation messages per chat.
	// Claude API needs the full message list each call, so we keep it in memory
	// and persist to DB for durability.
	sessions map[int64][]anthropic.MessageParam
}

func NewConversation(s *store.Store, limit int) *Conversation {
	return &Conversation{
		store:    s,
		limit:    limit,
		sessions: make(map[int64][]anthropic.MessageParam),
	}
}

// GetHistory returns the current message history for a chat.
func (c *Conversation) GetHistory(chatID int64) []anthropic.MessageParam {
	c.mu.Lock()
	defer c.mu.Unlock()

	msgs, ok := c.sessions[chatID]
	if !ok {
		return nil
	}
	// Return a copy
	result := make([]anthropic.MessageParam, len(msgs))
	copy(result, msgs)
	return result
}

// AddUserMessage appends a user message to the conversation.
func (c *Conversation) AddUserMessage(chatID int64, text string) {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.sessions[chatID] = append(c.sessions[chatID], anthropic.NewUserMessage(
		anthropic.NewTextBlock(text),
	))
	c.trimLocked(chatID)

	// Persist asynchronously (best-effort)
	go func() { _ = c.store.SaveMessage(chatID, "user", text) }()
}

// AddAssistantMessage appends the full assistant response to the conversation.
func (c *Conversation) AddAssistantMessage(chatID int64, msg *anthropic.Message) {
	c.mu.Lock()
	defer c.mu.Unlock()

	// Convert response content blocks to param blocks
	blocks := make([]anthropic.ContentBlockParamUnion, 0, len(msg.Content))
	for _, block := range msg.Content {
		switch v := block.AsAny().(type) {
		case anthropic.TextBlock:
			blocks = append(blocks, anthropic.NewTextBlock(v.Text))
		case anthropic.ToolUseBlock:
			blocks = append(blocks, anthropic.NewToolUseBlock(v.ID, v.Input, v.Name))
		}
	}

	c.sessions[chatID] = append(c.sessions[chatID], anthropic.MessageParam{
		Role:    anthropic.MessageParamRoleAssistant,
		Content: blocks,
	})

	// Persist text portion
	var text string
	for _, block := range msg.Content {
		if tb, ok := block.AsAny().(anthropic.TextBlock); ok {
			text += tb.Text
		}
	}
	if text != "" {
		go func() { _ = c.store.SaveMessage(chatID, "assistant", text) }()
	}
}

// AddToolResults appends tool results as a user message.
func (c *Conversation) AddToolResults(chatID int64, results []anthropic.ContentBlockParamUnion) {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.sessions[chatID] = append(c.sessions[chatID], anthropic.NewUserMessage(results...))
}

// Clear removes all conversation history for a chat.
func (c *Conversation) Clear(chatID int64) {
	c.mu.Lock()
	defer c.mu.Unlock()

	delete(c.sessions, chatID)
	go func() { _ = c.store.ClearMessages(chatID) }()
}

// trimLocked trims old messages to stay within the limit.
// Must be called with mu held.
func (c *Conversation) trimLocked(chatID int64) {
	msgs := c.sessions[chatID]
	if len(msgs) > c.limit {
		c.sessions[chatID] = msgs[len(msgs)-c.limit:]
	}
}
