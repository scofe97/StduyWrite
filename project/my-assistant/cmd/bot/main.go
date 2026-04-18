package main

import (
	"context"
	"log/slog"
	"os"
	"os/signal"
	"strconv"
	"syscall"

	"my-assistant/internal/agent"
	"my-assistant/internal/bot"
	"my-assistant/internal/llm"
	"my-assistant/internal/scheduler"
	"my-assistant/internal/store"
	"my-assistant/internal/tools"
)

func main() {
	// --- Config from environment variables ---
	telegramToken := mustEnv("TELEGRAM_BOT_TOKEN")
	anthropicKey := mustEnv("ANTHROPIC_API_KEY")
	model := getEnv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
	maxTokens := getEnvInt("ANTHROPIC_MAX_TOKENS", 4096)
	dbPath := getEnv("DB_PATH", "data/assistant.db")
	weatherKey := getEnv("OPENWEATHER_API_KEY", "")
	allowedChatID := getEnvInt("ALLOWED_CHAT_ID", 0)
	maxIter := getEnvInt("MAX_ITERATIONS", 10)
	convLimit := getEnvInt("CONVERSATION_LIMIT", 50)

	systemPrompt := getEnv("SYSTEM_PROMPT",
		"당신은 개인 AI 비서입니다. 사용자의 일상을 도와주세요.\n"+
			"메모 저장, 리마인더 설정, 웹 검색, 날씨 조회 등의 도구를 사용할 수 있습니다.\n"+
			"한국어로 자연스럽게 대화하세요.")

	// --- Initialize components ---
	slog.Info("starting my-assistant",
		"model", model,
		"db", dbPath,
	)

	// Ensure data directory exists
	if err := os.MkdirAll("data", 0755); err != nil {
		slog.Error("failed to create data dir", "error", err)
		os.Exit(1)
	}

	// Store
	db, err := store.New(dbPath)
	if err != nil {
		slog.Error("failed to open database", "error", err)
		os.Exit(1)
	}
	defer db.Close()

	// LLM client
	llmClient := llm.New(anthropicKey, model, int64(maxTokens))

	// Tool registry
	registry := tools.NewRegistry()
	// Note: memo and reminder tools use chatID=0 as placeholder.
	// The agent sets the correct chatID per request via tool input.
	registry.Register(tools.NewMemoTool(db, 0))
	registry.Register(tools.NewWebSearchTool())
	registry.Register(tools.NewWeatherTool(weatherKey))

	// Scheduler (needs bot reference for notifications, set up after bot creation)
	var sched *scheduler.Scheduler

	// Reminder tool needs a register function that adds cron jobs
	reminderRegisterFn := func(id int64, cronExpr string) {
		if sched != nil {
			sched.Register(id, cronExpr)
		}
	}
	registry.Register(tools.NewReminderTool(db, 0, reminderRegisterFn))

	// Agent
	ag := agent.New(agent.Config{
		LLM:          llmClient,
		Registry:     registry,
		Store:        db,
		SystemPrompt: systemPrompt,
		MaxIter:       maxIter,
		ConvLimit:     convLimit,
	})

	// Telegram bot
	telegramBot, err := bot.New(telegramToken, ag, int64(allowedChatID))
	if err != nil {
		slog.Error("failed to create telegram bot", "error", err)
		os.Exit(1)
	}

	// Scheduler with notification via Telegram
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	sched = scheduler.New(db, func(chatID int64, message string) {
		telegramBot.SendMessage(ctx, chatID, "⏰ 리마인더: "+message)
	})
	if err := sched.Start(); err != nil {
		slog.Error("failed to start scheduler", "error", err)
		os.Exit(1)
	}
	defer sched.Stop()

	// --- Start ---
	slog.Info("all components initialized, starting bot...")

	// Graceful shutdown
	go func() {
		sigCh := make(chan os.Signal, 1)
		signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)
		sig := <-sigCh
		slog.Info("shutdown signal received", "signal", sig)
		cancel()
	}()

	telegramBot.Start(ctx)
}

func mustEnv(key string) string {
	v := os.Getenv(key)
	if v == "" {
		slog.Error("required environment variable not set", "key", key)
		os.Exit(1)
	}
	return v
}

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func getEnvInt(key string, fallback int) int {
	v := os.Getenv(key)
	if v == "" {
		return fallback
	}
	n, err := strconv.Atoi(v)
	if err != nil {
		return fallback
	}
	return n
}
