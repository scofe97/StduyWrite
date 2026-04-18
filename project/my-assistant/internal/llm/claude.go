package llm

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/option"

	"my-assistant/internal/tools"
)

type Client struct {
	inner     anthropic.Client
	model     anthropic.Model
	maxTokens int64
}

func New(apiKey, model string, maxTokens int64) *Client {
	return &Client{
		inner:     anthropic.NewClient(option.WithAPIKey(apiKey)),
		model:     anthropic.Model(model),
		maxTokens: maxTokens,
	}
}

func (c *Client) SendMessage(
	ctx context.Context,
	systemPrompt string,
	messages []anthropic.MessageParam,
	registry *tools.Registry,
) (*anthropic.Message, error) {
	params := anthropic.MessageNewParams{
		Model:     c.model,
		MaxTokens: c.maxTokens,
		Messages:  messages,
	}

	if systemPrompt != "" {
		params.System = []anthropic.TextBlockParam{
			{Text: systemPrompt},
		}
	}

	if registry != nil {
		params.Tools = convertTools(registry)
	}

	resp, err := c.inner.Messages.New(ctx, params)
	if err != nil {
		return nil, fmt.Errorf("claude api: %w", err)
	}
	return resp, nil
}

// convertTools converts our tool registry to Anthropic SDK tool params.
func convertTools(registry *tools.Registry) []anthropic.ToolUnionParam {
	allTools := registry.All()
	result := make([]anthropic.ToolUnionParam, 0, len(allTools))

	for _, t := range allTools {
		var schema anthropic.ToolInputSchemaParam
		if err := json.Unmarshal(t.InputSchema(), &schema); err != nil {
			continue
		}

		toolParam := anthropic.ToolParam{
			Name:        t.Name(),
			Description: anthropic.String(t.Description()),
			InputSchema: schema,
		}
		result = append(result, anthropic.ToolUnionParam{OfTool: &toolParam})
	}
	return result
}

// ExtractText extracts all text content from a message response.
func ExtractText(msg *anthropic.Message) string {
	var text string
	for _, block := range msg.Content {
		if tb, ok := block.AsAny().(anthropic.TextBlock); ok {
			text += tb.Text
		}
	}
	return text
}

// ExtractToolCalls extracts tool use blocks from a message response.
type ToolCall struct {
	ID    string
	Name  string
	Input json.RawMessage
}

func ExtractToolCalls(msg *anthropic.Message) []ToolCall {
	var calls []ToolCall
	for _, block := range msg.Content {
		if tc, ok := block.AsAny().(anthropic.ToolUseBlock); ok {
			calls = append(calls, ToolCall{
				ID:    tc.ID,
				Name:  tc.Name,
				Input: json.RawMessage(tc.Input),
			})
		}
	}
	return calls
}
