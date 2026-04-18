# A2UI 프로토콜 스펙 (Specification v0.8)

> **학습 목표**: A2UI v0.8 프로토콜의 메시지 구조, 스키마, 규칙을 정확히 이해한다.

---

## 1. 설계 원칙

A2UI 프로토콜은 다음 원칙을 따릅니다:

| 원칙 | 설명 |
|------|------|
| **LLM 친화적** | 선언적이고 단순한 구조로 LLM이 쉽게 생성 |
| **점진적 렌더링** | JSONL/SSE 스트림으로 실시간 응답성 |
| **플랫폼 독립성** | 클라이언트 정의 카탈로그 사용 |
| **효율적 상태 관리** | UI 구조와 데이터 분리 |
| **확장 가능한 통신** | 단방향 UI 스트림 + 이벤트 처리 |

---

## 2. 아키텍처 구성요소

### 2.1 Surface (표면)

**정의**: 화면의 연속된 영역을 나타내는 고유 식별자

```json
{
  "surfaceId": "main-content"
}
```

**특징**:
- 단일 스트림이 여러 Surface를 동시에 제어 가능
- 각 Surface는 독립적인 컴포넌트 트리와 데이터 모델을 가짐

### 2.2 Component Tree (인접 리스트 모델)

컴포넌트는 평탄 목록으로 전송되며, ID 참조로 트리 구조를 형성합니다.

```json
{
  "components": [
    {"id": "root", "component": {"Column": {"children": {"explicitList": ["header", "content"]}}}},
    {"id": "header", "component": {"Text": {"text": {"literalString": "제목"}}}},
    {"id": "content", "component": {"Text": {"text": {"path": "/data/content"}}}}
  ]
}
```

### 2.3 데이터 분리

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  surfaceUpdate  │     │ dataModelUpdate │     │ beginRendering  │
│   (UI 구조)     │     │   (동적 데이터) │     │   (렌더 신호)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## 3. 메시지 타입 상세

### 3.1 surfaceUpdate (Server → Client)

UI 컴포넌트를 정의하거나 업데이트합니다.

**구조**:
```json
{
  "surfaceUpdate": {
    "surfaceId": "unique-surface-id",
    "components": [
      {
        "id": "component-id",
        "component": {
          "ComponentType": {
            "property1": {"literalString": "value"},
            "property2": {"path": "/data/path"}
          }
        }
      }
    ]
  }
}
```

**규칙**:
- 각 컴포넌트는 **정확히 하나의 타입 키**를 가짐
- 기존 ID를 재전송하면 해당 컴포넌트를 **업데이트**
- 새 ID는 **추가**

### 3.2 dataModelUpdate (Server → Client)

컴포넌트가 바인딩하는 데이터 모델을 갱신합니다.

**구조**:
```json
{
  "dataModelUpdate": {
    "surfaceId": "unique-surface-id",
    "path": "/user",
    "contents": [
      {"key": "name", "valueString": "Alice"},
      {"key": "age", "valueNumber": 25},
      {"key": "verified", "valueBoolean": true}
    ]
  }
}
```

**값 타입**:

| 필드 | 타입 | 예시 |
|------|------|------|
| `valueString` | 문자열 | `"Alice"` |
| `valueNumber` | 숫자 | `25` |
| `valueBoolean` | 불리언 | `true` |
| `valueMap` | 중첩 객체 | `[{"key": "city", "valueString": "Seoul"}]` |

**경로 규칙**:
- `path`를 지정하면 특정 위치만 업데이트
- `path`를 생략하면 전체 모델을 교체

### 3.3 beginRendering (Server → Client)

클라이언트에 렌더링 시작 신호를 전달합니다.

**구조**:
```json
{
  "beginRendering": {
    "surfaceId": "unique-surface-id",
    "root": "root-component-id",
    "catalogId": "https://github.com/google/A2UI/...",
    "styles": {}
  }
}
```

**필드 설명**:

| 필드 | 필수 | 설명 |
|------|------|------|
| `surfaceId` | ✅ | 고유 식별자 |
| `root` | ✅ | 루트 컴포넌트 ID |
| `catalogId` | ⬜ | 사용할 컴포넌트 카탈로그 URL |
| `styles` | ⬜ | 스타일 오버라이드 |

### 3.4 deleteSurface (Server → Client)

특정 Surface와 관련된 모든 컴포넌트 및 데이터를 제거합니다.

**구조**:
```json
{
  "deleteSurface": {
    "surfaceId": "unique-surface-id"
  }
}
```

**참고**: 존재하지 않는 Surface 삭제는 안전합니다 (무작동).

### 3.5 userAction (Client → Server)

사용자 상호작용을 에이전트에 전송합니다.

**구조**:
```json
{
  "userAction": {
    "name": "submit_form",
    "surfaceId": "main-content",
    "sourceComponentId": "submit-button",
    "timestamp": "2025-12-25T10:30:00Z",
    "context": {
      "/form/name": "Alice",
      "/form/email": "alice@example.com"
    }
  }
}
```

**필드 설명**:

| 필드 | 필수 | 설명 |
|------|------|------|
| `name` | ✅ | 액션 이름 (Button의 action.name과 매칭) |
| `surfaceId` | ✅ | 이벤트 발생 Surface |
| `sourceComponentId` | ✅ | 이벤트 발생 컴포넌트 ID |
| `timestamp` | ✅ | ISO 8601 형식 타임스탬프 |
| `context` | ⬜ | 해결된 데이터 값들 |

### 3.6 error (Client → Server)

클라이언트 렌더링/바인딩 오류를 서버에 보고합니다.

**구조**:
```json
{
  "error": {
    "surfaceId": "main-content",
    "componentId": "broken-component",
    "errorType": "INVALID_BINDING",
    "message": "Path /user/name not found in data model"
  }
}
```

---

## 4. BoundValue (데이터 바인딩)

컴포넌트 속성에 값을 할당하는 두 가지 방식:

### 4.1 리터럴 값 (고정)

```json
{
  "text": {"literalString": "환영합니다!"}
}
```

### 4.2 데이터 바인딩 (반응형)

```json
{
  "text": {"path": "/user/name"}
}
```

### 4.3 혼합 (초기값 + 바인딩)

```json
{
  "text": {
    "literalString": "Guest",
    "path": "/user/name"
  }
}
```

**동작**: `path`에 데이터가 없으면 `literalString`을 사용, 있으면 `path` 값 사용

---

## 5. 컨테이너 자식 정의

### 5.1 explicitList (정적 자식)

고정된 ID 리스트:

```json
{
  "children": {
    "explicitList": ["header", "content", "footer"]
  }
}
```

### 5.2 template (동적 자식)

데이터 배열에서 생성:

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

**작동 원리**:
1. `/items` 배열의 각 항목에 대해
2. `item-template` 컴포넌트를 복제
3. 복제된 컴포넌트의 경로는 해당 항목으로 범위 지정

**예시**:
- 데이터: `/items` = `[{name: "A"}, {name: "B"}]`
- 템플릿 내 `/name` → `/items/0/name`, `/items/1/name`으로 해석

---

## 6. 메시지 순서 규칙

### 권장 순서

```
1. surfaceUpdate (컴포넌트 정의)
2. dataModelUpdate (데이터 채우기)
3. beginRendering (렌더링 시작)
4. [추가 surfaceUpdate/dataModelUpdate] (업데이트)
5. deleteSurface (정리)
```

### 규칙

| 규칙 | 설명 |
|------|------|
| `beginRendering`은 초기 `surfaceUpdate` 이후 | 컴포넌트가 정의된 후에만 렌더링 시작 |
| `surfaceUpdate`와 `dataModelUpdate`는 순서 무관 | 독립적으로 처리 가능 |
| 여러 `surfaceUpdate`는 병합됨 | 같은 ID는 최신 값으로 덮어쓰기 |

---

## 7. 카탈로그 협상

### 흐름

```
┌─────────┐                    ┌─────────┐
│  서버   │                    │ 클라이언트│
├─────────┤                    ├─────────┤
│ Agent   │ ←───────────────── │ 지원    │
│ Card에  │  a2uiClient        │ 카탈로그 │
│ 카탈로그 │  Capabilities      │ 명시    │
│ 명시    │                    │         │
│         │ ─────────────────→ │         │
│         │  beginRendering    │ 카탈로그 │
│         │  (catalogId 선택)  │ 적용    │
└─────────┘                    └─────────┘
```

### 표준 카탈로그 ID

```
v0.8: https://github.com/google/A2UI/blob/main/specification/0.8/json/standard_catalog_definition.json
```

---

## 8. 클라이언트 구현 요소

### 필수 구성요소

| 구성요소 | 역할 |
|----------|------|
| **JSONL 파서** | 스트림에서 JSON 객체 추출 |
| **메시지 디스패처** | 메시지 타입별 처리기 라우팅 |
| **컴포넌트 버퍼** | ID → 컴포넌트 Map 관리 |
| **데이터 모델 스토어** | JSON Pointer 경로로 데이터 저장/조회 |
| **위젯 레지스트리** | 컴포넌트 타입 → 네이티브 위젯 매핑 |
| **바인딩 리졸버** | 경로 해석 및 반응형 업데이트 |
| **Surface 관리자** | 다중 Surface 라이프사이클 관리 |
| **이벤트 핸들러** | 사용자 상호작용 → userAction 변환 |

---

## 9. 데이터 흐름 요약

```
1. SSE 스트림 시작
         ↓
2. surfaceUpdate 수신 → 컴포넌트 버퍼에 저장
         ↓
3. dataModelUpdate 수신 → 데이터 모델 구축
         ↓
4. beginRendering 수신 → 렌더링 시작
         ↓
5. 사용자 상호작용 → userAction 전송
         ↓
6. 서버 응답 → 새로운 surfaceUpdate/dataModelUpdate
         ↓
7. UI 자동 업데이트
```

---

## 📝 실습: 스펙 이해도 체크

### 퀴즈

1. `beginRendering` 메시지는 언제 전송해야 하나요?
   - [ ] 스트림 시작 시 가장 먼저
   - [x] 초기 `surfaceUpdate` 이후
   - [ ] 사용자 상호작용 후

2. 다음 중 `dataModelUpdate`의 값 타입이 아닌 것은?
   - [ ] `valueString`
   - [ ] `valueNumber`
   - [x] `valueArray`

3. `template` 방식의 자식 정의에서 범위 지정(scoping)이란?
   - [ ] 스타일을 제한하는 것
   - [x] 경로가 배열 항목으로 해석되는 것
   - [ ] 컴포넌트를 숨기는 것

### 실습 과제

1. 다음 UI를 A2UI 메시지로 작성하세요:
   - 제목: "할 일 목록"
   - 동적 리스트: 각 항목에 체크박스와 텍스트
   - 추가 버튼

2. `userAction` 메시지를 작성하여 "항목 추가" 액션을 전송하세요.

---

## 🔗 다음 단계

- [05. 컴포넌트 레퍼런스](./05-components.md) → 모든 컴포넌트 상세 사용법
- [06. 실제 사용 시나리오](./06-practical-scenarios.md) → 프로덕션 적용 가이드

---

## 📚 참고 자료

- [A2UI Specification v0.8](https://a2ui.org/specification/v0.8-a2ui/)
- [A2A Extension](https://a2ui.org/specification/v0.8-a2a-extension/)
- [Message Reference](https://a2ui.org/reference/messages/)
- [Standard Catalog Definition](https://github.com/google/A2UI/blob/main/specification/0.8/json/standard_catalog_definition.json)
