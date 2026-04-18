package tools

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strings"
	"time"
)

// WebSearchTool searches the web using DuckDuckGo's HTML endpoint.
type WebSearchTool struct {
	httpClient *http.Client
}

func NewWebSearchTool() *WebSearchTool {
	return &WebSearchTool{
		httpClient: &http.Client{Timeout: 10 * time.Second},
	}
}

func (t *WebSearchTool) Name() string { return "web_search" }

func (t *WebSearchTool) Description() string {
	return "웹에서 정보를 검색합니다. 최신 뉴스, 사실 확인, 일반적인 질문에 답하는 데 사용합니다."
}

func (t *WebSearchTool) InputSchema() json.RawMessage {
	return json.RawMessage(`{
		"type": "object",
		"properties": {
			"query": {
				"type": "string",
				"description": "검색할 키워드나 질문"
			}
		},
		"required": ["query"]
	}`)
}

type webSearchInput struct {
	Query string `json:"query"`
}

func (t *WebSearchTool) Execute(ctx context.Context, input json.RawMessage) (string, error) {
	var in webSearchInput
	if err := json.Unmarshal(input, &in); err != nil {
		return "", fmt.Errorf("입력 파싱 오류: %w", err)
	}
	if in.Query == "" {
		return "", fmt.Errorf("query가 비어 있습니다")
	}

	searchURL := "https://html.duckduckgo.com/html/?q=" + url.QueryEscape(in.Query)
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, searchURL, nil)
	if err != nil {
		return "", fmt.Errorf("요청 생성 실패: %w", err)
	}
	req.Header.Set("User-Agent", "Mozilla/5.0 (compatible; MyAssistant/1.0)")
	req.Header.Set("Accept-Language", "ko-KR,ko;q=0.9,en;q=0.8")

	resp, err := t.httpClient.Do(req)
	if err != nil {
		return fmt.Sprintf("웹 검색 중 오류가 발생했습니다: %v", err), nil
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(io.LimitReader(resp.Body, 512*1024)) // 512KB limit
	if err != nil {
		return fmt.Sprintf("응답 읽기 실패: %v", err), nil
	}

	results := parseDuckDuckGoResults(string(body))
	if len(results) == 0 {
		return fmt.Sprintf("%q에 대한 검색 결과를 찾을 수 없습니다.", in.Query), nil
	}

	var sb strings.Builder
	fmt.Fprintf(&sb, "검색어: %q\n\n", in.Query)
	for i, r := range results {
		fmt.Fprintf(&sb, "%d. %s\n", i+1, r.title)
		if r.snippet != "" {
			fmt.Fprintf(&sb, "   %s\n", r.snippet)
		}
		if r.url != "" {
			fmt.Fprintf(&sb, "   URL: %s\n", r.url)
		}
		fmt.Fprintln(&sb)
	}
	return sb.String(), nil
}

type searchResult struct {
	title   string
	snippet string
	url     string
}

// parseDuckDuckGoResults extracts search results from DuckDuckGo's HTML response.
// DuckDuckGo HTML results use class="result__title", "result__snippet", "result__url".
func parseDuckDuckGoResults(html string) []searchResult {
	const maxResults = 5
	var results []searchResult

	// Each result block starts with class="result__body"
	// We extract title, snippet, and URL using simple string parsing.
	blocks := splitByMarker(html, `class="result__body"`)

	for _, block := range blocks {
		if len(results) >= maxResults {
			break
		}

		title := extractBetween(block, `class="result__a"`, `</a>`)
		title = stripTags(title)
		title = strings.TrimSpace(title)

		snippet := extractBetween(block, `class="result__snippet"`, `</a>`)
		if snippet == "" {
			snippet = extractBetween(block, `class="result__snippet"`, `</span>`)
		}
		snippet = stripTags(snippet)
		snippet = strings.TrimSpace(snippet)

		rawURL := extractBetween(block, `class="result__url"`, `</a>`)
		if rawURL == "" {
			rawURL = extractBetween(block, `class="result__url"`, `</span>`)
		}
		rawURL = stripTags(rawURL)
		rawURL = strings.TrimSpace(rawURL)

		if title == "" {
			continue
		}
		results = append(results, searchResult{title: title, snippet: snippet, url: rawURL})
	}
	return results
}

// splitByMarker splits s into segments that start after each occurrence of marker.
func splitByMarker(s, marker string) []string {
	var parts []string
	for {
		idx := strings.Index(s, marker)
		if idx < 0 {
			break
		}
		s = s[idx+len(marker):]
		// Take up to next result block or a large chunk
		end := strings.Index(s, `class="result__body"`)
		if end < 0 {
			parts = append(parts, s)
			break
		}
		parts = append(parts, s[:end])
	}
	return parts
}

// extractBetween finds the content after the first occurrence of startMarker
// and before the next occurrence of endMarker.
func extractBetween(s, startMarker, endMarker string) string {
	start := strings.Index(s, startMarker)
	if start < 0 {
		return ""
	}
	s = s[start+len(startMarker):]
	// Skip to end of the opening tag
	tagEnd := strings.Index(s, ">")
	if tagEnd >= 0 {
		s = s[tagEnd+1:]
	}
	end := strings.Index(s, endMarker)
	if end < 0 {
		return s
	}
	return s[:end]
}

// stripTags removes all HTML tags from s.
func stripTags(s string) string {
	var sb strings.Builder
	inTag := false
	for _, ch := range s {
		switch {
		case ch == '<':
			inTag = true
		case ch == '>':
			inTag = false
		case !inTag:
			sb.WriteRune(ch)
		}
	}
	// Collapse whitespace
	result := strings.Join(strings.Fields(sb.String()), " ")
	return result
}
