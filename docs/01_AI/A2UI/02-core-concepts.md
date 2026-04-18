# A2UI 핵심 개념 (Core Concepts)

> **학습 목표**: A2UI의 세 가지 핵심 원칙(스트리밍, 선언적 컴포넌트, 데이터 바인딩)을 이해한다.

---

## 1. 아키텍처 개요

A2UI는 **세 가지 핵심 원칙** 위에 구축되었습니다:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  스트리밍    │ → │ 선언적      │ → │ 데이터      │
│  메시지     │    │ 컴포넌트    │    │ 바인딩      │
└─────────────┘    └─────────────┘    └─────────────┘
```

| 원칙 | 설명 |
|------|------|
| **스트리밍 메시지** | UI 업데이트가 JSON 메시지 시퀀스로 전달됨 |
| **선언적 컴포넌트** | UI가 코드가 아닌 데이터로 표현됨 |
| **데이터 바인딩** | UI 구조와 애플리케이션 상태가 분리됨 |

---

## 2. 데이터 흐름 (Data Flow)

### 2.1 전체 아키텍처

```
┌──────────┐    ┌──────────┐    ┌───────────┐    ┌──────────┐    ┌──────────┐
│  Agent   │ → │ A2UI     │ → │ Transport │ → │ Client   │ → │ Native   │
│  (LLM)   │    │ Generator│    │ (SSE/WS)  │    │ Renderer │    │ UI       │
└──────────┘    └──────────┘    └───────────┘    └──────────┘    └──────────┘
```

### 2.2 메시지 포맷: JSON Lines (JSONL)

A2UI는 **JSONL 형식**을 사용합니다. 각 라인이 완전한 JSON 객체입니다.

```jsonl
{"surfaceUpdate": {"surfaceId": "main", "components": [...]}}
{"dataModelUpdate": {"surfaceId": "main", "path": "/user", "contents": [...]}}
{"beginRendering": {"surfaceId": "main", "root": "root-component"}}
```

**장점**:
- ✅ 스트리밍 친화적 (한 줄씩 파싱 가능)
- ✅ LLM이 점진적으로 생성하기 용이
- ✅ 실시간 UI 업데이트 가능

### 2.3 메시지 타입

| 메시지 타입 | 목적 | 방향 |
|-------------|------|------|
| `surfaceUpdate` | UI 컴포넌트 정의/업데이트 | Server → Client |
| `dataModelUpdate` | 애플리케이션 상태 업데이트 | Server → Client |
| `beginRendering` | 렌더링 시작 신호 | Server → Client |
| `deleteSurface` | UI 표면 제거 | Server → Client |
| `userAction` | 사용자 상호작용 전송 | Client → Server |
| `error` | 오류 보고 | Client → Server |

---

## 3. 실습: 레스토랑 예약 라이프사이클

### Step 1: UI 구조 정의 (`surfaceUpdate`)

```json
{
  "surfaceUpdate": {
    "surfaceId": "reservation",
    "components": [
      {
        "id": "header",
        "component": {
          "Text": {
            "text": {"literalString": "레스토랑 예약"},
            "usageHint": "h1"
          }
        }
      },
      {
        "id": "date-picker",
        "component": {
          "DateTimeInput": {
            "label": {"literalString": "예약 날짜"},
            "value": {"path": "/reservation/date"}
          }
        }
      },
      {
        "id": "guest-input",
        "component": {
          "TextField": {
            "label": {"literalString": "인원 수"},
            "text": {"path": "/reservation/guests"},
            "textFieldType": "number"
          }
        }
      },
      {
        "id": "submit-btn",
        "component": {
          "Button": {
            "child": "btn-text",
            "primary": true,
            "action": {"name": "submit_reservation"}
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

### Step 2: 데이터 채우기 (`dataModelUpdate`)

```json
{
  "dataModelUpdate": {
    "surfaceId": "reservation",
    "path": "/reservation",
    "contents": [
      {"key": "date", "valueString": "2025-12-25T19:00:00Z"},
      {"key": "guests", "valueString": "2"}
    ]
  }
}
```

### Step 3: 렌더링 시작 (`beginRendering`)

```json
{
  "beginRendering": {
    "surfaceId": "reservation",
    "root": "header"
  }
}
```

### Step 4: 사용자 상호작용 (`userAction`)

사용자가 인원을 "3"으로 변경하고 버튼 클릭:

```json
{
  "userAction": {
    "name": "submit_reservation",
    "surfaceId": "reservation",
    "sourceComponentId": "submit-btn",
    "timestamp": "2025-12-25T10:30:00Z",
    "context": {
      "/reservation/date": "2025-12-25T19:00:00Z",
      "/reservation/guests": "3"
    }
  }
}
```

### Step 5: 에이전트 응답

에이전트가 새로운 확인 UI를 생성하거나 기존 UI를 업데이트합니다.

---

## 4. 컴포넌트 구조 (Components)

### 4.1 Adjacency List 모델

A2UI는 중첩된 JSON 트리 대신 **플랫 리스트 구조**를 사용합니다.

**❌ 중첩 트리 방식 (사용하지 않음)**
```json
{
  "Card": {
    "children": [
      {"Text": {"text": "Hello"}},
      {"Button": {"label": "Click"}}
    ]
  }
}
```

**✅ Adjacency List 방식 (A2UI 방식)**
```json
{
  "components": [
    {"id": "card-1", "component": {"Card": {"child": "text-1"}}},
    {"id": "text-1", "component": {"Text": {"text": {"literalString": "Hello"}}}},
    {"id": "btn-1", "component": {"Button": {"child": "btn-text"}}}
  ]
}
```

**장점**:
- ✅ LLM이 한 번에 완벽한 중첩을 생성할 필요 없음
- ✅ 깊게 중첩된 컴포넌트 업데이트 용이
- ✅ 증분 스트리밍 지원
- ✅ 구조와 데이터 분리

### 4.2 컴포넌트 기본 구조

```json
{
  "id": "unique-id",        // 고유 식별자 (필수)
  "component": {
    "ComponentType": {       // 정확히 하나의 타입
      "property1": {...},
      "property2": {...}
    }
  }
}
```

### 4.3 자식 컴포넌트 처리

**정적 자식 (고정된 ID 리스트)**
```json
{
  "children": {
    "explicitList": ["header", "content", "footer"]
  }
}
```

**동적 자식 (데이터 배열에서 생성)**
```json
{
  "children": {
    "template": {
      "dataBinding": "/items",
      "componentId": "item-template"
    }
  }
}
```

---

## 5. 데이터 바인딩 (Data Binding)

### 5.1 핵심 개념

A2UI는 **UI 구조(컴포넌트)** 와 **애플리케이션 상태(데이터)** 를 분리합니다.

```
┌─────────────────┐          ┌─────────────────┐
│   surfaceUpdate │          │ dataModelUpdate │
│   (UI 구조)     │    ↔     │ (데이터 상태)   │
└─────────────────┘          └─────────────────┘
         │                            │
         └────────┬───────────────────┘
                  ↓
         ┌─────────────────┐
         │   렌더링된 UI   │
         └─────────────────┘
```

### 5.2 JSON Pointer 경로

RFC 6901 표준을 따르는 경로 구문:

| 데이터 | 경로 | 결과 |
|--------|------|------|
| `{"user": {"name": "Alice"}}` | `/user/name` | `"Alice"` |
| `{"items": ["Apple", "Banana"]}` | `/items/0` | `"Apple"` |
| `{"cart": {"items": [{"price": 100}]}}` | `/cart/items/0/price` | `100` |

### 5.3 리터럴 vs. 데이터 바인딩

**리터럴 (고정값)**
```json
{"text": {"literalString": "환영합니다!"}}
```

**데이터 바인딩 (반응형)**
```json
{"text": {"path": "/user/name"}}
```

**혼합 (초기값 + 바인딩)**
```json
{"text": {"literalString": "Guest", "path": "/user/name"}}
```

### 5.4 반응형 업데이트

데이터가 변경되면 UI가 **자동으로 업데이트**됩니다:

```json
// 데이터 업데이트
{"dataModelUpdate": {"path": "/user/name", "contents": [{"valueString": "Bob"}]}}

// → Text 컴포넌트가 자동으로 "Bob"으로 변경
```

### 5.5 입력 바인딩 (양방향)

| 컴포넌트 | 사용자 작업 | 데이터 업데이트 |
|---------|-----------|----------------|
| TextField | "Alice" 입력 | `/form/name` = "Alice" |
| CheckBox | 박스 체크 | `/form/agreed` = true |
| DateTimeInput | 날짜 선택 | `/form/date` = "2025-12-25" |

---

## 6. 실습: 데이터 바인딩 예제

### 예제: 쇼핑 카트

**Step 1: 컴포넌트 정의**
```json
{
  "surfaceUpdate": {
    "surfaceId": "cart",
    "components": [
      {
        "id": "cart-list",
        "component": {
          "List": {
            "children": {
              "template": {
                "dataBinding": "/cart/items",
                "componentId": "item-template"
              }
            }
          }
        }
      },
      {
        "id": "item-template",
        "component": {
          "Row": {
            "children": {"explicitList": ["item-name", "item-price"]}
          }
        }
      },
      {
        "id": "item-name",
        "component": {
          "Text": {"text": {"path": "/name"}}
        }
      },
      {
        "id": "item-price",
        "component": {
          "Text": {"text": {"path": "/price"}}
        }
      },
      {
        "id": "total",
        "component": {
          "Text": {
            "text": {"path": "/cart/total"},
            "usageHint": "h2"
          }
        }
      }
    ]
  }
}
```

**Step 2: 데이터 제공**
```json
{
  "dataModelUpdate": {
    "surfaceId": "cart",
    "path": "/cart",
    "contents": [
      {
        "key": "items",
        "valueMap": [
          {"key": "0", "valueMap": [
            {"key": "name", "valueString": "커피"},
            {"key": "price", "valueString": "$5.00"}
          ]},
          {"key": "1", "valueMap": [
            {"key": "name", "valueString": "케이크"},
            {"key": "price", "valueString": "$8.00"}
          ]}
        ]
      },
      {"key": "total", "valueString": "$13.00"}
    ]
  }
}
```

---

## 7. 모범 사례

### 컴포넌트 ID 네이밍

```
✅ 좋은 예: "user-profile-card", "submit-button", "date-picker"
❌ 나쁜 예: "c1", "comp", "x"
```

### 데이터 구조 설계

```
✅ 좋은 예: 도메인별 그룹화
{
  "user": {"name": "...", "email": "..."},
  "cart": {"items": [...], "total": "..."}
}

❌ 나쁜 예: 평탄한 구조
{
  "userName": "...",
  "userEmail": "...",
  "cartItems": [...],
  "cartTotal": "..."
}
```

### 업데이트 전략

```
✅ 세밀한 업데이트: 변경된 경로만 업데이트
{"dataModelUpdate": {"path": "/user/name", ...}}

❌ 전체 교체: 모든 데이터 재전송
{"dataModelUpdate": {"path": "/", ...}}
```

---

## 📝 실습: 핵심 개념 이해도 체크

### 퀴즈

1. A2UI가 JSONL 형식을 사용하는 이유는?
   - [ ] JSON보다 작기 때문
   - [x] 스트리밍과 점진적 생성에 적합하기 때문
   - [ ] 더 빠르기 때문

2. Adjacency List 모델의 장점이 아닌 것은?
   - [ ] LLM이 임의 순서로 생성 가능
   - [ ] 증분 스트리밍 지원
   - [x] 코드 실행 가능

3. `/cart/items/0/price` 경로가 참조하는 데이터는?
   - [ ] 카트의 첫 번째 가격
   - [x] 카트 아이템 배열의 첫 번째 항목의 가격
   - [ ] 모든 아이템의 가격

### 실습 과제

1. 사용자 프로필 카드 UI를 A2UI JSON으로 작성해보세요:
   - 프로필 이미지
   - 이름 (데이터 바인딩)
   - 이메일 (데이터 바인딩)
   - 편집 버튼

2. 데이터 모델을 설계하고 `dataModelUpdate` 메시지를 작성해보세요.

---

## 🔗 다음 단계

- [03. 빠른 시작](./03-quickstart.md) → 5분 만에 첫 A2UI 앱 실행
- [04. 스펙 정리](./04-specification.md) → v0.8 프로토콜 상세 학습

---

## 📚 참고 자료

- [A2UI Concepts - Data Flow](https://a2ui.org/concepts/data-flow/)
- [A2UI Concepts - Components](https://a2ui.org/concepts/components/)
- [A2UI Concepts - Data Binding](https://a2ui.org/concepts/data-binding/)
- [RFC 6901 - JSON Pointer](https://datatracker.ietf.org/doc/html/rfc6901)
