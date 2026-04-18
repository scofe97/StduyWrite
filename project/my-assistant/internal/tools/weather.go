package tools

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"time"
)

// WeatherTool fetches current weather using OpenWeatherMap API.
type WeatherTool struct {
	apiKey     string
	httpClient *http.Client
}

func NewWeatherTool(apiKey string) *WeatherTool {
	return &WeatherTool{
		apiKey:     apiKey,
		httpClient: &http.Client{Timeout: 10 * time.Second},
	}
}

func (t *WeatherTool) Name() string { return "weather" }

func (t *WeatherTool) Description() string {
	return "특정 도시의 현재 날씨 정보를 조회합니다. 기온, 날씨 상태, 습도, 풍속을 제공합니다."
}

func (t *WeatherTool) InputSchema() json.RawMessage {
	return json.RawMessage(`{
		"type": "object",
		"properties": {
			"city": {
				"type": "string",
				"description": "날씨를 조회할 도시 이름 (영문 또는 한글, 예: Seoul, 서울, Tokyo)"
			}
		},
		"required": ["city"]
	}`)
}

type weatherInput struct {
	City string `json:"city"`
}

// openWeatherResponse maps the relevant fields from OpenWeatherMap API response.
type openWeatherResponse struct {
	Name string `json:"name"`
	Main struct {
		Temp      float64 `json:"temp"`
		FeelsLike float64 `json:"feels_like"`
		TempMin   float64 `json:"temp_min"`
		TempMax   float64 `json:"temp_max"`
		Humidity  int     `json:"humidity"`
	} `json:"main"`
	Weather []struct {
		Description string `json:"description"`
		Icon        string `json:"icon"`
	} `json:"weather"`
	Wind struct {
		Speed float64 `json:"speed"`
		Deg   int     `json:"deg"`
	} `json:"wind"`
	Clouds struct {
		All int `json:"all"`
	} `json:"clouds"`
	Visibility int `json:"visibility"`
	Sys        struct {
		Country string `json:"country"`
	} `json:"sys"`
	Cod     interface{} `json:"cod"`
	Message string      `json:"message"`
}

func (t *WeatherTool) Execute(ctx context.Context, input json.RawMessage) (string, error) {
	if t.apiKey == "" {
		return "날씨 API 키가 설정되지 않았습니다. WEATHER_API_KEY 환경변수를 설정해주세요.", nil
	}

	var in weatherInput
	if err := json.Unmarshal(input, &in); err != nil {
		return "", fmt.Errorf("입력 파싱 오류: %w", err)
	}
	if in.City == "" {
		return "", fmt.Errorf("city가 비어 있습니다")
	}

	apiURL := fmt.Sprintf(
		"https://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s&units=metric&lang=kr",
		url.QueryEscape(in.City),
		t.apiKey,
	)

	req, err := http.NewRequestWithContext(ctx, http.MethodGet, apiURL, nil)
	if err != nil {
		return "", fmt.Errorf("요청 생성 실패: %w", err)
	}

	resp, err := t.httpClient.Do(req)
	if err != nil {
		return fmt.Sprintf("날씨 API 요청 실패: %v", err), nil
	}
	defer resp.Body.Close()

	var data openWeatherResponse
	if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
		return "", fmt.Errorf("응답 파싱 실패: %w", err)
	}

	// Handle API errors (cod can be int 200 or string "404")
	if resp.StatusCode != http.StatusOK {
		msg := data.Message
		if msg == "" {
			msg = fmt.Sprintf("HTTP %d", resp.StatusCode)
		}
		return fmt.Sprintf("날씨 정보를 가져올 수 없습니다: %s", msg), nil
	}

	description := "정보 없음"
	if len(data.Weather) > 0 {
		description = data.Weather[0].Description
	}

	result := fmt.Sprintf(
		"[%s, %s] 현재 날씨\n"+
			"날씨 상태: %s\n"+
			"기온: %.1f°C (최저 %.1f°C / 최고 %.1f°C)\n"+
			"체감 온도: %.1f°C\n"+
			"습도: %d%%\n"+
			"풍속: %.1f m/s\n"+
			"구름: %d%%\n"+
			"가시거리: %d m",
		data.Name,
		data.Sys.Country,
		description,
		data.Main.Temp,
		data.Main.TempMin,
		data.Main.TempMax,
		data.Main.FeelsLike,
		data.Main.Humidity,
		data.Wind.Speed,
		data.Clouds.All,
		data.Visibility,
	)
	return result, nil
}
