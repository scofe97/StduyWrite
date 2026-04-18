package handler

import (
	"context"

	"github.com/runners-high/git-api/internal/service"
	"github.com/runners-high/git-api/pkg/event"
	"go.uber.org/zap"
)

// KafkaHandler handles incoming Kafka messages
type KafkaHandler struct {
	gitService *service.GitService
	logger     *zap.Logger
}

// NewKafkaHandler creates a new Kafka handler
func NewKafkaHandler(gitService *service.GitService, logger *zap.Logger) *KafkaHandler {
	return &KafkaHandler{
		gitService: gitService,
		logger:     logger,
	}
}

// Handle processes incoming Kafka messages
func (h *KafkaHandler) Handle(message []byte) error {
	ctx := context.Background()

	// Parse the event
	parsedEvent, err := event.ParseEvent(message)
	if err != nil {
		h.logger.Error("Failed to parse event",
			zap.Error(err),
			zap.ByteString("message", message))
		return err
	}

	// Route to appropriate handler based on event type
	switch e := parsedEvent.(type) {
	case *event.BranchCommand:
		return h.handleBranchCommand(ctx, e)

	case *event.RepositorySyncCommand:
		return h.gitService.HandleRepositorySync(ctx, e)

	case *event.PullRequestCommand:
		return h.gitService.HandlePullRequestCreate(ctx, e)

	case *event.BaseEvent:
		h.logger.Warn("Received unhandled event type",
			zap.String("eventType", string(e.EventType)))
		return nil

	default:
		h.logger.Warn("Received unknown event type")
		return nil
	}
}

// handleBranchCommand routes branch commands
func (h *KafkaHandler) handleBranchCommand(ctx context.Context, cmd *event.BranchCommand) error {
	switch cmd.EventType {
	case event.BranchCreateRequested:
		return h.gitService.HandleBranchCreate(ctx, cmd)

	case event.BranchDeleteRequested:
		return h.gitService.HandleBranchDelete(ctx, cmd)

	default:
		h.logger.Warn("Unknown branch command type",
			zap.String("eventType", string(cmd.EventType)))
		return nil
	}
}
