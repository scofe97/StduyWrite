package bot

import (
	"context"
	"log/slog"
	"strings"

	"github.com/go-telegram/bot"
	"github.com/go-telegram/bot/models"

	"my-assistant/internal/agent"
)

type TelegramBot struct {
	bot       *bot.Bot
	agent     *agent.Agent
	allowedID int64 // 0 = allow all, otherwise restrict to this chat ID
}

func New(token string, ag *agent.Agent, allowedID int64) (*TelegramBot, error) {
	tb := &TelegramBot{
		agent:     ag,
		allowedID: allowedID,
	}

	opts := []bot.Option{
		bot.WithDefaultHandler(tb.handleMessage),
	}

	b, err := bot.New(token, opts...)
	if err != nil {
		return nil, err
	}

	b.RegisterHandler(bot.HandlerTypeMessageText, "/start", bot.MatchTypeExact, tb.handleStart)
	b.RegisterHandler(bot.HandlerTypeMessageText, "/clear", bot.MatchTypeExact, tb.handleClear)
	b.RegisterHandler(bot.HandlerTypeMessageText, "/help", bot.MatchTypeExact, tb.handleHelp)

	tb.bot = b
	return tb, nil
}

// Start begins polling for Telegram updates. Blocks until ctx is cancelled.
func (tb *TelegramBot) Start(ctx context.Context) {
	slog.Info("telegram bot started")
	tb.bot.Start(ctx)
}

// SendMessage sends a text message to a chat. Used by the scheduler for reminders.
func (tb *TelegramBot) SendMessage(ctx context.Context, chatID int64, text string) {
	_, err := tb.bot.SendMessage(ctx, &bot.SendMessageParams{
		ChatID: chatID,
		Text:   text,
	})
	if err != nil {
		slog.Error("failed to send message", "chat_id", chatID, "error", err)
	}
}

func (tb *TelegramBot) handleStart(ctx context.Context, b *bot.Bot, update *models.Update) {
	b.SendMessage(ctx, &bot.SendMessageParams{
		ChatID: update.Message.Chat.ID,
		Text:   "안녕하세요! 개인 AI 비서입니다.\n\n사용 가능한 명령어:\n/clear - 대화 초기화\n/help - 도움말\n\n자유롭게 대화해보세요!",
	})
}

func (tb *TelegramBot) handleClear(ctx context.Context, b *bot.Bot, update *models.Update) {
	chatID := update.Message.Chat.ID
	tb.agent.ClearHistory(chatID)
	b.SendMessage(ctx, &bot.SendMessageParams{
		ChatID: chatID,
		Text:   "대화 이력이 초기화되었습니다.",
	})
}

func (tb *TelegramBot) handleHelp(ctx context.Context, b *bot.Bot, update *models.Update) {
	help := strings.Join([]string{
		"사용 가능한 기능:",
		"",
		"- 메모 저장/검색/삭제",
		"- 리마인더 설정/관리",
		"- 웹 검색",
		"- 날씨 조회",
		"",
		"자연어로 요청하세요. 예:",
		"\"내일 오전 9시에 회의 알려줘\"",
		"\"서울 날씨 알려줘\"",
		"\"Go 동시성 패턴 검색해줘\"",
		"\"오늘 회의 내용 메모해줘\"",
	}, "\n")

	b.SendMessage(ctx, &bot.SendMessageParams{
		ChatID: update.Message.Chat.ID,
		Text:   help,
	})
}

func (tb *TelegramBot) handleMessage(ctx context.Context, b *bot.Bot, update *models.Update) {
	if update.Message == nil || update.Message.Text == "" {
		return
	}

	chatID := update.Message.Chat.ID

	// Access control
	if tb.allowedID != 0 && chatID != tb.allowedID {
		b.SendMessage(ctx, &bot.SendMessageParams{
			ChatID: chatID,
			Text:   "접근이 제한되어 있습니다.",
		})
		return
	}

	// Skip command messages (handled by registered handlers)
	if strings.HasPrefix(update.Message.Text, "/") {
		return
	}

	slog.Info("message received", "chat_id", chatID, "text_len", len(update.Message.Text))

	// Run agent
	response, err := tb.agent.Run(ctx, chatID, update.Message.Text)
	if err != nil {
		slog.Error("agent error", "chat_id", chatID, "error", err)
		b.SendMessage(ctx, &bot.SendMessageParams{
			ChatID: chatID,
			Text:   "처리 중 오류가 발생했습니다: " + err.Error(),
		})
		return
	}

	if response == "" {
		response = "(응답 없음)"
	}

	// Telegram has a 4096 character limit per message
	for len(response) > 0 {
		chunk := response
		if len(chunk) > 4000 {
			chunk = response[:4000]
			response = response[4000:]
		} else {
			response = ""
		}

		b.SendMessage(ctx, &bot.SendMessageParams{
			ChatID: chatID,
			Text:   chunk,
		})
	}
}
