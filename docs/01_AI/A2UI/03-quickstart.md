# A2UI 빠른 시작 (Quickstart)

> **학습 목표**: 5분 만에 A2UI 데모를 실행하고 동작 원리를 이해한다.

---

## 1. 사전 요구사항

### 필수 환경

| 요구사항 | 버전 | 확인 명령어 |
|---------|------|------------|
| Node.js | 18+ | `node --version` |
| npm | 8+ | `npm --version` |
| Python | 3.10+ | `python3 --version` |
| Git | - | `git --version` |

### Gemini API 키 발급

1. [Google AI Studio](https://aistudio.google.com/apikey) 접속
2. **Create API Key** 클릭
3. 발급된 키 복사 (무료)

---

## 2. 레스토랑 예약 데모 실행

### Step 1: 저장소 복제

```bash
git clone https://github.com/google/a2ui.git
cd a2ui
```

### Step 2: API 키 설정

```bash
# Linux/macOS
export GEMINI_API_KEY="your_gemini_api_key_here"

# Windows (PowerShell)
$env:GEMINI_API_KEY="your_gemini_api_key_here"

# 확인
echo $GEMINI_API_KEY
```

### Step 3: Lit 클라이언트로 이동

```bash
cd samples/client/lit
```

### Step 4: 설치 및 실행

```bash
npm install
npm run demo:all
```

**실행되는 작업**:
1. ✅ 모든 의존성 설치
2. ✅ A2UI 렌더러 빌드
3. ✅ A2A 레스토랑 파인더 에이전트 시작
4. ✅ 개발 서버 시작
5. ✅ 브라우저에서 `http://localhost:5173` 자동 오픈

---

## 3. 데모 작동 흐름 이해

### 전체 흐름

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   웹 UI     │ → │  A2A Agent  │ → │   Gemini    │ → │  A2UI JSON  │
│  메시지 전송 │     │  메시지 수신 │     │  UI 생성    │     │  클라이언트  │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### 실습: 메시지 보내보기

1. 브라우저에서 입력창에 메시지 입력:
   ```
   "12월 25일 저녁에 2명 예약할 수 있는 이탈리안 레스토랑 찾아줘"
   ```

2. Gemini가 A2UI JSON 메시지를 생성

3. 클라이언트가 네이티브 UI로 렌더링

---

## 4. A2UI 메시지 구조 분석

### 4.1 UI 정의 (`surfaceUpdate`)

에이전트가 생성하는 UI 구조:

```json
{
  "surfaceUpdate": {
    "surfaceId": "restaurant-finder",
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
        "id": "guest-count",
        "component": {
          "TextField": {
            "label": {"literalString": "인원"},
            "text": {"path": "/reservation/guests"},
            "textFieldType": "number"
          }
        }
      },
      {
        "id": "confirm-btn",
        "component": {
          "Button": {
            "child": "btn-label",
            "primary": true,
            "action": {"name": "confirm_reservation"}
          }
        }
      },
      {
        "id": "btn-label",
        "component": {
          "Text": {"text": {"literalString": "예약 확인"}}
        }
      }
    ]
  }
}
```

### 4.2 데이터 채우기 (`dataModelUpdate`)

```json
{
  "dataModelUpdate": {
    "surfaceId": "restaurant-finder",
    "path": "/reservation",
    "contents": [
      {"key": "date", "valueString": "2025-12-25T19:00:00Z"},
      {"key": "guests", "valueString": "2"},
      {"key": "restaurant", "valueString": "Pasta Paradise"}
    ]
  }
}
```

### 4.3 렌더링 시작 (`beginRendering`)

```json
{
  "beginRendering": {
    "surfaceId": "restaurant-finder",
    "root": "header"
  }
}
```

---

## 5. 다른 데모 실행하기

### 컴포넌트 갤러리

모든 A2UI 컴포넌트를 한눈에 볼 수 있습니다:

```bash
npm start -- gallery
```

**포함된 컴포넌트**:
- 레이아웃: Row, Column, List
- 표시: Text, Image, Icon, Divider
- 입력: TextField, Button, Checkbox, DateTimeInput
- 컨테이너: Card, Modal, Tabs

### 연락처 조회 데모

데이터 바인딩과 검색 인터페이스를 시연합니다:

```bash
npm run demo:contact
```

---

## 6. 트러블슈팅

### 문제: 포트 5173이 사용 중

```bash
# 다른 포트로 실행
npm start -- --port 3000
```

또는 자동으로 다음 가용 포트를 시도합니다.

### 문제: API 키 오류

```bash
# 환경변수 확인
echo $GEMINI_API_KEY

# 키가 비어있으면 다시 설정
export GEMINI_API_KEY="your_key_here"
```

### 문제: Python 의존성 오류

```bash
# Python 버전 확인
python3 --version  # 3.10+ 필요

# 가상환경 사용 권장
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 문제: npm install 실패

```bash
# 캐시 클리어 후 재시도
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

---

## 7. 직접 만들어보기: 간단한 폼

### 실습: 회원가입 폼 JSON 작성

**목표**: 이름, 이메일, 비밀번호 입력 폼 만들기

```json
{
  "surfaceUpdate": {
    "surfaceId": "signup-form",
    "components": [
      {
        "id": "form-container",
        "component": {
          "Column": {
            "children": {"explicitList": ["title", "name-input", "email-input", "password-input", "submit-btn"]}
          }
        }
      },
      {
        "id": "title",
        "component": {
          "Text": {
            "text": {"literalString": "회원가입"},
            "usageHint": "h1"
          }
        }
      },
      {
        "id": "name-input",
        "component": {
          "TextField": {
            "label": {"literalString": "이름"},
            "text": {"path": "/form/name"},
            "textFieldType": "shortText"
          }
        }
      },
      {
        "id": "email-input",
        "component": {
          "TextField": {
            "label": {"literalString": "이메일"},
            "text": {"path": "/form/email"},
            "textFieldType": "shortText"
          }
        }
      },
      {
        "id": "password-input",
        "component": {
          "TextField": {
            "label": {"literalString": "비밀번호"},
            "text": {"path": "/form/password"},
            "textFieldType": "obscured"
          }
        }
      },
      {
        "id": "submit-btn",
        "component": {
          "Button": {
            "child": "btn-text",
            "primary": true,
            "action": {"name": "submit_signup"}
          }
        }
      },
      {
        "id": "btn-text",
        "component": {
          "Text": {"text": {"literalString": "가입하기"}}
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
    "surfaceId": "signup-form",
    "path": "/form",
    "contents": [
      {"key": "name", "valueString": ""},
      {"key": "email", "valueString": ""},
      {"key": "password", "valueString": ""}
    ]
  }
}
```

---

## 8. 렌더러 옵션

### 사용 가능한 렌더러

| 렌더러 | 플랫폼 | 상태 | 설치 |
|--------|--------|------|------|
| **Lit** | 웹 (Web Components) | ✅ 안정 | `npm install @a2ui/lit` |
| **Angular** | 웹 | ✅ 안정 | `npm install @a2ui/angular` |
| **Flutter** | 모바일/데스크톱/웹 | ✅ 안정 | `flutter pub add flutter_genui` |
| **React** | 웹 | 🚧 2026 Q1 | - |

### Lit 렌더러 구성요소

```
┌─────────────────────────────────────────┐
│  Lit Renderer                           │
├─────────────────────────────────────────┤
│  • 메시지 프로세서: A2UI 상태 관리      │
│  • <a2ui-surface>: 서피스 렌더링        │
│  • Lit Signals: 반응형 상태 관리        │
└─────────────────────────────────────────┘
```

### Angular 렌더러 구성요소

```typescript
// app.config.ts
import { provideA2UI } from '@a2ui/angular';

export const appConfig = {
  providers: [
    provideA2UI()
  ]
};
```

---

## 📝 실습 체크리스트

### 필수 과제

- [ ] 저장소 클론 및 데모 실행
- [ ] 레스토랑 예약 데모에서 메시지 보내기
- [ ] 컴포넌트 갤러리 확인
- [ ] 연락처 조회 데모 실행

### 도전 과제

- [ ] 회원가입 폼 JSON 직접 작성
- [ ] 데이터 바인딩 테스트
- [ ] 커스텀 UI 디자인

---

## 🔗 다음 단계

- [04. 스펙 정리](./04-specification.md) → v0.8 프로토콜 상세 학습
- [05. 컴포넌트 레퍼런스](./05-components.md) → 모든 컴포넌트 사용법
- [06. 실제 사용 시나리오](./06-practical-scenarios.md) → 프로덕션 적용 가이드

---

## 📚 참고 자료

- [A2UI Quickstart](https://a2ui.org/quickstart/)
- [A2UI Composer](https://a2ui.org/composer/)
- [GitHub - Samples](https://github.com/google/A2UI/tree/main/samples)
- [Google AI Studio - API Key](https://aistudio.google.com/apikey)
