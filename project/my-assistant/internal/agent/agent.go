package agent

import (
	"context"
	"errors"
	"log/slog"
	"time"

	"github.com/anthropics/anthropic-sdk-go"

	"my-assistant/internal/llm"
	"my-assistant/internal/store"
	"my-assistant/internal/tools"
)

type Agent struct {
	llm          *llm.Client
	registry     *tools.Registry
	conversation *Conversation
	store        *store.Store
	systemPrompt string
	maxIter      int
}

type Config struct {
	LLM          *llm.Client
	Registry     *tools.Registry
	Store        *store.Store
	SystemPrompt string
	MaxIter      int
	ConvLimit    int
}

func New(cfg Config) *Agent {
	if cfg.MaxIter <= 0 {
		cfg.MaxIter = 10
	}
	if cfg.ConvLimit <= 0 {
		cfg.ConvLimit = 50
	}
	return &Agent{
		llm:          cfg.LLM,
		registry:     cfg.Registry,
		conversation: NewConversation(cfg.Store, cfg.ConvLimit),
		store:        cfg.Store,
		systemPrompt: cfg.SystemPrompt,
		maxIter:      cfg.MaxIter,
	}
}

// Run executes the ReAct loop for a user message and returns the final text response.
func (a *Agent) Run(ctx context.Context, chatID int64, userMsg string) (string, error) {
	a.conversation.AddUserMessage(chatID, userMsg)

	for i := 0; i < a.maxIter; i++ {
		messages := a.conversation.GetHistory(chatID)

		// 1. Call Claude
		resp, err := a.llm.SendMessage(ctx, a.systemPrompt, messages, a.registry)
		if err != nil {
			return "", err
		}

		// 2. Save assistant response to conversation
		a.conversation.AddAssistantMessage(chatID, resp)

		// 3. Check stop reason
		if resp.StopReason == anthropic.StopReasonEndTurn {
			return llm.ExtractText(resp), nil
		}

		// 4. Handle tool calls
		if resp.StopReason == anthropic.StopReasonToolUse {
			toolCalls := llm.ExtractToolCalls(resp)
			if len(toolCalls) == 0 {
				return llm.ExtractText(resp), nil
			}

			results := make([]anthropic.ContentBlockParamUnion, 0, len(toolCalls))
			for _, tc := range toolCalls {
				start := time.Now()
				output, execErr := a.registry.Execute(ctx, tc.Name, tc.Input)
				duration := time.Since(start)

				isError := execErr != nil
				content := output
				if isError {
					content = execErr.Error()
				}

				slog.Info("tool executed",
					"tool", tc.Name,
					"duration", duration,
					"error", isError,
				)

				// Log to DB
				errStr := ""
				if execErr != nil {
					errStr = execErr.Error()
				}
				_ = a.store.LogToolCall(chatID, tc.Name, string(tc.Input), output, errStr, duration.Milliseconds())

				results = append(results, anthropic.NewToolResultBlock(tc.ID, content, isError))
			}

			a.conversation.AddToolResults(chatID, results)
		}
	}

	return "", errors.New("max iterations reached")
}

// ClearHistory clears conversation history for a chat.
func (a *Agent) ClearHistory(chatID int64) {
	a.conversation.Clear(chatID)
}
