# A2UI 실제 사용 시나리오 (Practical Scenarios)

> **학습 목표**: A2UI를 실제 프로젝트에 적용하는 방법과 추천 시나리오를 이해한다.

---

## 1. A2UI 적용 추천 시나리오

### ✅ 적합한 사용 사례

| 시나리오 | 설명 | 활용 포인트 |
|---------|------|------------|
| **AI 어시스턴트 앱** | 사용자 질문에 동적 UI로 응답 | 폼, 선택지, 결과 표시 |
| **다중 에이전트 시스템** | 여러 에이전트가 UI 생성 | 신뢰 경계 넘어 안전한 UI 전송 |
| **크로스플랫폼 앱** | 웹/모바일/데스크톱 동시 지원 | 단일 JSON으로 모든 플랫폼 |
| **기업 워크플로우** | 승인, 데이터 입력 자동화 | 단계별 인터페이스 |
| **프로토타이핑** | 빠른 UI 테스트 | LLM으로 즉시 UI 생성 |

### ❌ 적합하지 않은 사용 사례

| 시나리오 | 이유 | 대안 |
|---------|------|------|
| 정적 웹사이트 | 동적 UI 불필요 | HTML/CSS |
| 순수 텍스트 채팅 | UI 요소 불필요 | 일반 채팅 API |
| 복잡한 그래픽 편집기 | 세밀한 제어 필요 | 네이티브 개발 |
| 게임 UI | 고성능 렌더링 필요 | 게임 엔진 |

---

## 2. 시나리오 1: 레스토랑 예약 에이전트

### 개요

사용자가 자연어로 레스토랑을 검색하고 예약하는 AI 에이전트입니다.

### 아키텍처

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   사용자    │ ←→ │  AI 에이전트 │ ←→ │  레스토랑   │
│   (앱)     │     │  (Gemini)   │     │  API       │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 구현 단계

#### Step 1: 검색 UI 생성

사용자: "강남에서 이탈리안 레스토랑 찾아줘"

**에이전트 응답 (A2UI JSON)**:
```json
{
  "surfaceUpdate": {
    "surfaceId": "restaurant-search",
    "components": [
      {
        "id": "search-header",
        "component": {
          "Text": {
            "text": {"literalString": "🍝 강남 이탈리안 레스토랑"},
            "usageHint": "h1"
          }
        }
      },
      {
        "id": "results-list",
        "component": {
          "List": {
            "children": {
              "template": {
                "dataBinding": "/restaurants",
                "componentId": "restaurant-card"
              }
            }
          }
        }
      },
      {
        "id": "restaurant-card",
        "component": {
          "Card": {"child": "card-content"}
        }
      },
      {
        "id": "card-content",
        "component": {
          "Column": {
            "children": {"explicitList": ["rest-name", "rest-rating", "rest-price", "reserve-btn"]}
          }
        }
      },
      {
        "id": "rest-name",
        "component": {
          "Text": {"text": {"path": "/name"}, "usageHint": "h3"}
        }
      },
      {
        "id": "rest-rating",
        "component": {
          "Text": {"text": {"path": "/rating"}, "usageHint": "caption"}
        }
      },
      {
        "id": "rest-price",
        "component": {
          "Text": {"text": {"path": "/priceRange"}}
        }
      },
      {
        "id": "reserve-btn",
        "component": {
          "Button": {
            "child": "btn-text",
            "action": {"name": "start_reservation"}
          }
        }
      },
      {
        "id": "btn-text",
        "component": {
          "Text": {"text": {"literalString": "예약하기"}}
        }
      }
    ]
  }
}
```

**데이터 모델**:
```json
{
  "dataModelUpdate": {
    "surfaceId": "restaurant-search",
    "path": "/restaurants",
    "contents": [
      {"key": "0", "valueMap": [
        {"key": "name", "valueString": "Pasta Paradise"},
        {"key": "rating", "valueString": "⭐ 4.5"},
        {"key": "priceRange", "valueString": "₩₩₩"}
      ]},
      {"key": "1", "valueMap": [
        {"key": "name", "valueString": "Little Italy"},
        {"key": "rating", "valueString": "⭐ 4.2"},
        {"key": "priceRange", "valueString": "₩₩"}
      ]}
    ]
  }
}
```

#### Step 2: 예약 폼 표시

사용자가 "예약하기" 버튼 클릭 → `userAction` 전송:
```json
{
  "userAction": {
    "name": "start_reservation",
    "surfaceId": "restaurant-search",
    "sourceComponentId": "reserve-btn",
    "context": {"/name": "Pasta Paradise"}
  }
}
```

**에이전트 응답 (예약 폼)**:
```json
{
  "surfaceUpdate": {
    "surfaceId": "reservation-form",
    "components": [
      {
        "id": "form-container",
        "component": {
          "Card": {"child": "form-content"}
        }
      },
      {
        "id": "form-content",
        "component": {
          "Column": {
            "children": {"explicitList": ["form-title", "date-input", "time-input", "guests-input", "confirm-btn"]}
          }
        }
      },
      {
        "id": "form-title",
        "component": {
          "Text": {
            "text": {"literalString": "Pasta Paradise 예약"},
            "usageHint": "h2"
          }
        }
      },
      {
        "id": "date-input",
        "component": {
          "DateTimeInput": {
            "label": {"literalString": "예약 날짜"},
            "value": {"path": "/reservation/date"}
          }
        }
      },
      {
        "id": "time-input",
        "component": {
          "TextField": {
            "label": {"literalString": "예약 시간"},
            "text": {"path": "/reservation/time"}
          }
        }
      },
      {
        "id": "guests-input",
        "component": {
          "TextField": {
            "label": {"literalString": "인원 수"},
            "text": {"path": "/reservation/guests"},
            "textFieldType": "number"
          }
        }
      },
      {
        "id": "confirm-btn",
        "component": {
          "Button": {
            "child": "confirm-text",
            "primary": true,
            "action": {"name": "confirm_reservation"}
          }
        }
      },
      {
        "id": "confirm-text",
        "component": {
          "Text": {"text": {"literalString": "예약 확정"}}
        }
      }
    ]
  }
}
```

#### Step 3: 예약 확인

예약 완료 후 확인 메시지:
```json
{
  "surfaceUpdate": {
    "surfaceId": "confirmation",
    "components": [
      {
        "id": "success-card",
        "component": {
          "Card": {"child": "success-content"}
        }
      },
      {
        "id": "success-content",
        "component": {
          "Column": {
            "children": {"explicitList": ["check-icon", "success-title", "reservation-details"]}
          }
        }
      },
      {
        "id": "check-icon",
        "component": {
          "Icon": {"name": {"literalString": "check_circle"}}
        }
      },
      {
        "id": "success-title",
        "component": {
          "Text": {
            "text": {"literalString": "예약이 완료되었습니다!"},
            "usageHint": "h2"
          }
        }
      },
      {
        "id": "reservation-details",
        "component": {
          "Text": {
            "text": {"path": "/confirmation/summary"}
          }
        }
      }
    ]
  }
}
```

---

## 3. 시나리오 2: 기업 승인 워크플로우

### 개요

휴가 신청, 경비 청구 등 승인이 필요한 기업 워크플로우를 AI가 처리합니다.

### 흐름

```
1. 직원이 요청 작성
2. AI가 적절한 양식 UI 생성
3. 관리자에게 승인 UI 전송
4. 승인/거부 결과 처리
```

### 휴가 신청 폼

```json
{
  "surfaceUpdate": {
    "surfaceId": "leave-request",
    "components": [
      {
        "id": "form",
        "component": {
          "Column": {
            "children": {"explicitList": ["title", "type-select", "start-date", "end-date", "reason", "submit"]}
          }
        }
      },
      {
        "id": "title",
        "component": {
          "Text": {"text": {"literalString": "휴가 신청"}, "usageHint": "h1"}
        }
      },
      {
        "id": "start-date",
        "component": {
          "DateTimeInput": {
            "label": {"literalString": "시작일"},
            "value": {"path": "/leave/startDate"}
          }
        }
      },
      {
        "id": "end-date",
        "component": {
          "DateTimeInput": {
            "label": {"literalString": "종료일"},
            "value": {"path": "/leave/endDate"}
          }
        }
      },
      {
        "id": "reason",
        "component": {
          "TextField": {
            "label": {"literalString": "사유"},
            "text": {"path": "/leave/reason"},
            "textFieldType": "longText"
          }
        }
      },
      {
        "id": "submit",
        "component": {
          "Button": {
            "child": "submit-text",
            "primary": true,
            "action": {"name": "submit_leave_request"}
          }
        }
      },
      {
        "id": "submit-text",
        "component": {
          "Text": {"text": {"literalString": "신청하기"}}
        }
      }
    ]
  }
}
```

### 관리자 승인 UI

```json
{
  "surfaceUpdate": {
    "surfaceId": "approval-panel",
    "components": [
      {
        "id": "panel",
        "component": {
          "Card": {"child": "panel-content"}
        }
      },
      {
        "id": "panel-content",
        "component": {
          "Column": {
            "children": {"explicitList": ["request-info", "action-buttons"]}
          }
        }
      },
      {
        "id": "request-info",
        "component": {
          "Column": {
            "children": {"explicitList": ["requester", "dates", "reason-display"]}
          }
        }
      },
      {
        "id": "requester",
        "component": {
          "Text": {"text": {"path": "/request/requesterName"}, "usageHint": "h3"}
        }
      },
      {
        "id": "dates",
        "component": {
          "Text": {"text": {"path": "/request/dateRange"}}
        }
      },
      {
        "id": "reason-display",
        "component": {
          "Text": {"text": {"path": "/request/reason"}, "usageHint": "caption"}
        }
      },
      {
        "id": "action-buttons",
        "component": {
          "Row": {
            "children": {"explicitList": ["approve-btn", "reject-btn"]},
            "distribution": "spaceEvenly"
          }
        }
      },
      {
        "id": "approve-btn",
        "component": {
          "Button": {
            "child": "approve-text",
            "primary": true,
            "action": {"name": "approve_request"}
          }
        }
      },
      {
        "id": "approve-text",
        "component": {
          "Text": {"text": {"literalString": "승인"}}
        }
      },
      {
        "id": "reject-btn",
        "component": {
          "Button": {
            "child": "reject-text",
            "action": {"name": "reject_request"}
          }
        }
      },
      {
        "id": "reject-text",
        "component": {
          "Text": {"text": {"literalString": "거부"}}
        }
      }
    ]
  }
}
```

---

## 4. 시나리오 3: 데이터 대시보드

### 개요

실시간 데이터를 시각화하는 대시보드를 AI가 생성합니다.

### 대시보드 UI

```json
{
  "surfaceUpdate": {
    "surfaceId": "dashboard",
    "components": [
      {
        "id": "dashboard-container",
        "component": {
          "Column": {
            "children": {"explicitList": ["header", "metrics-row", "chart-section"]}
          }
        }
      },
      {
        "id": "header",
        "component": {
          "Row": {
            "children": {"explicitList": ["title", "refresh-btn"]},
            "distribution": "spaceBetween"
          }
        }
      },
      {
        "id": "title",
        "component": {
          "Text": {"text": {"literalString": "매출 대시보드"}, "usageHint": "h1"}
        }
      },
      {
        "id": "refresh-btn",
        "component": {
          "Button": {
            "child": "refresh-text",
            "action": {"name": "refresh_data"}
          }
        }
      },
      {
        "id": "refresh-text",
        "component": {
          "Text": {"text": {"literalString": "새로고침"}}
        }
      },
      {
        "id": "metrics-row",
        "component": {
          "Row": {
            "children": {"explicitList": ["metric-1", "metric-2", "metric-3"]},
            "distribution": "spaceEvenly"
          }
        }
      },
      {
        "id": "metric-1",
        "component": {
          "Card": {"child": "metric-1-content"}
        }
      },
      {
        "id": "metric-1-content",
        "component": {
          "Column": {
            "children": {"explicitList": ["metric-1-label", "metric-1-value"]}
          }
        }
      },
      {
        "id": "metric-1-label",
        "component": {
          "Text": {"text": {"literalString": "오늘 매출"}, "usageHint": "caption"}
        }
      },
      {
        "id": "metric-1-value",
        "component": {
          "Text": {"text": {"path": "/metrics/todaySales"}, "usageHint": "h2"}
        }
      }
    ]
  }
}
```

**데이터 업데이트** (실시간):
```json
{
  "dataModelUpdate": {
    "surfaceId": "dashboard",
    "path": "/metrics",
    "contents": [
      {"key": "todaySales", "valueString": "₩12,500,000"},
      {"key": "monthlyGrowth", "valueString": "+15.3%"},
      {"key": "activeUsers", "valueString": "1,234"}
    ]
  }
}
```

---

## 5. 에이전트 개발 가이드

### 5.1 기본 구조 (Python + Google ADK)

```python
from google.adk.agents.llm_agent import Agent

# 도구 정의
def get_restaurants(location: str, cuisine: str):
    """레스토랑 검색"""
    return [
        {"name": "Pasta Paradise", "rating": 4.5},
        {"name": "Little Italy", "rating": 4.2}
    ]

# 에이전트 초기화
root_agent = Agent(
    model='gemini-2.5-flash',
    name="restaurant_agent",
    instruction="""
    당신은 레스토랑 찾기 어시스턴트입니다.
    사용자 요청에 따라 레스토랑을 검색하고,
    A2UI JSON 형식으로 UI를 생성합니다.

    출력 형식:
    ---대화---
    [사용자에게 보여줄 텍스트]
    ---a2ui_JSON---
    [A2UI JSON 메시지 리스트]
    """,
    tools=[get_restaurants]
)
```

### 5.2 프롬프트 엔지니어링 팁

**템플릿 규칙 정의**:
```
- 5개 이하 결과: 단일 열 레이아웃
- 5개 초과 결과: 2열 레이아웃
- 예약 요청: 예약 양식 표시
- 확인: 확인 메시지 사용
```

**JSON 스키마 포함**:
```python
instruction = f"""
A2UI 컴포넌트 스키마:
{a2ui_schema_json}

이 스키마를 따라 UI를 생성하세요.
"""
```

### 5.3 출력 검증

```python
import jsonschema

def validate_a2ui_output(json_data):
    try:
        jsonschema.validate(
            instance=json_data,
            schema=a2ui_schema_object
        )
        return True
    except jsonschema.ValidationError as e:
        print(f"Validation error: {e.message}")
        return False
```

---

## 6. 클라이언트 통합 가이드

### 6.1 Lit (Web Components)

```javascript
import { A2UIProcessor, A2UISurface } from '@a2ui/lit';

// 메시지 프로세서 초기화
const processor = new A2UIProcessor();

// SSE 스트림 연결
const eventSource = new EventSource('/api/agent-stream');
eventSource.onmessage = (event) => {
    const message = JSON.parse(event.data);
    processor.processMessage(message);
};

// HTML
// <a2ui-surface processor="${processor}" surfaceId="main"></a2ui-surface>
```

### 6.2 Angular

```typescript
// app.config.ts
import { provideA2UI } from '@a2ui/angular';

export const appConfig = {
  providers: [provideA2UI()]
};

// component.ts
import { A2UIMessageProcessor } from '@a2ui/angular';

@Component({...})
export class AppComponent {
  constructor(private processor: A2UIMessageProcessor) {
    this.connectToAgent();
  }

  connectToAgent() {
    // SSE 연결 및 메시지 처리
  }
}
```

### 6.3 Flutter

```dart
import 'package:flutter_genui/flutter_genui.dart';

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return GenUIApp(
      agentUrl: 'https://my-agent.example.com/stream',
      child: GenUISurface(surfaceId: 'main'),
    );
  }
}
```

---

## 7. 모범 사례

### 7.1 성능 최적화

| 전략 | 설명 |
|------|------|
| **세밀한 업데이트** | 변경된 경로만 `dataModelUpdate` 전송 |
| **배치 처리** | 여러 컴포넌트를 하나의 `surfaceUpdate`에 포함 |
| **템플릿 활용** | 반복 UI는 동적 자식으로 처리 |
| **스트리밍** | `beginRendering` 전에 점진적 컴포넌트 전송 |

### 7.2 사용자 경험

| 전략 | 설명 |
|------|------|
| **로딩 상태** | 에이전트 응답 대기 중 로딩 UI 표시 |
| **에러 처리** | 명확한 에러 메시지와 재시도 옵션 |
| **접근성** | 스크린 리더 지원, 키보드 네비게이션 |
| **반응형** | 다양한 화면 크기 지원 |

### 7.3 보안

| 전략 | 설명 |
|------|------|
| **입력 검증** | 사용자 입력 검증 후 에이전트 전송 |
| **카탈로그 제한** | 신뢰된 컴포넌트 카탈로그만 사용 |
| **인증** | 에이전트 통신 시 인증 토큰 사용 |
| **Rate Limiting** | 과도한 요청 방지 |

---

## 📝 실습 프로젝트 제안

### 초급

1. **To-Do 앱**: 할 일 추가/삭제/완료 표시
2. **계산기**: 기본 사칙연산 UI

### 중급

3. **설문조사 폼**: 다양한 입력 타입 활용
4. **상품 카탈로그**: 검색 + 필터 + 상세보기

### 고급

5. **예약 시스템**: 전체 예약 워크플로우
6. **관리자 대시보드**: 실시간 데이터 + 승인 UI

---

## 🔗 참고 자료

- [A2UI 공식 문서](https://a2ui.org/)
- [Google ADK (Agent Development Kit)](https://developers.google.com/agent-development-kit)
- [A2UI GitHub](https://github.com/google/A2UI)
- [Flutter GenUI SDK](https://pub.dev/packages/flutter_genui)
- [AG UI / CopilotKit](https://copilotkit.ai/)

---

## 📚 학습 로드맵

```
1주차: 소개 + 핵심 개념 (01, 02)
       ↓
2주차: Quickstart + 데모 실행 (03)
       ↓
3주차: 스펙 + 컴포넌트 심화 (04, 05)
       ↓
4주차: 실습 프로젝트 구현 (06)
       ↓
5주차: 에이전트 개발 + 클라이언트 통합
       ↓
6주차: 프로덕션 배포 + 최적화
```

---

**축하합니다! 🎉**

A2UI 학습 문서를 모두 완료했습니다. 이제 AI 에이전트가 안전하고 풍부한 UI를 생성하는 시스템을 구축할 수 있습니다.
