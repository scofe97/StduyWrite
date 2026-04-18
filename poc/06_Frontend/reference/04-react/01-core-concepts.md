# Chapter 1. Getting Started with React

---

### 📌 핵심 요약
> React는 Meta가 만든 **컴포넌트 기반 프론트엔드 라이브러리**로, Virtual DOM을 통해 성능을 최적화한다. React 컴포넌트는 **JSX**로 UI를 선언하며, **Props**로 구성 가능하고 **State**로 상호작용을 구현한다. **Vite**를 사용하면 React 프로젝트를 빠르게 설정할 수 있으며, ESLint와 Prettier로 코드 품질을 관리한다. 이벤트 핸들러와 커스텀 이벤트를 통해 사용자 상호작용을 처리하고, React Developer Tools로 컴포넌트를 디버깅한다.

---

### 🎯 학습 목표
- React의 장점과 Virtual DOM 개념을 이해한다
- Vite로 React 프로젝트를 생성하고 설정할 수 있다
- React 컴포넌트를 생성하고 JSX 문법을 사용할 수 있다
- Props를 사용해 컴포넌트를 구성 가능하게 만들 수 있다
- useState Hook으로 상태를 관리할 수 있다
- 이벤트 핸들러와 커스텀 이벤트를 구현할 수 있다
- React Developer Tools를 사용해 컴포넌트를 디버깅할 수 있다

---

### 📖 본문 정리

#### 1. React의 장점

```
┌─────────────────────────────────────────────────────────────┐
│                    Why React?                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Virtual DOM   │  │  Component-based │                  │
│  │   (성능 최적화)  │  │   (재사용 가능)   │                  │
│  └─────────────────┘  └─────────────────┘                  │
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │  Narrow Focus   │  │   Meta Backing   │                  │
│  │ (기존 앱에 통합) │  │  (높은 품질 보장) │                  │
│  └─────────────────┘  └─────────────────┘                  │
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │ Server Comp.    │  │  React Native   │                  │
│  │ (성능 + 생산성) │  │ (크로스 플랫폼)  │                  │
│  └─────────────────┘  └─────────────────┘                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

##### Virtual DOM 동작 원리

```
┌─────────────────────────────────────────────────────────────┐
│                  Virtual DOM Process                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [State Change]                                            │
│        │                                                    │
│        ▼                                                    │
│   ┌──────────────┐                                          │
│   │ New Virtual  │                                          │
│   │     DOM      │                                          │
│   └──────┬───────┘                                          │
│          │                                                  │
│          ▼                                                  │
│   ┌──────────────┐    ┌──────────────┐                     │
│   │ New Virtual  │ vs │ Old Virtual  │  ← Diffing          │
│   │     DOM      │    │     DOM      │                     │
│   └──────┬───────┘    └──────────────┘                     │
│          │                                                  │
│          ▼                                                  │
│   [Minimum Changes Calculated]                              │
│          │                                                  │
│          ▼                                                  │
│   ┌──────────────┐                                          │
│   │   Real DOM   │  ← 최소한의 변경만 적용                   │
│   └──────────────┘                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| 장점 | 설명 |
|------|------|
| **Virtual DOM** | 최소한의 DOM 변경으로 성능 최적화 |
| **컴포넌트 기반** | 재사용 가능한 UI 조각 |
| **좁은 초점** | 기존 앱에 부분적으로 통합 가능 |
| **Server Components** | 성능 향상 + 생산성 증가 |
| **React Native** | iOS/Android 크로스 플랫폼 개발 |
| **Meta 지원** | Facebook이 사용 → 높은 품질 보장 |

---

#### 2. Vite로 프로젝트 생성

##### 프로젝트 생성 명령어

```bash
# 1. Vite 프로젝트 생성
npm create vite@latest

# 2. 프롬프트 응답
# - Project name: [원하는 이름]
# - Framework: React
# - Variant: JavaScript (또는 TypeScript)

# 3. 의존성 설치 및 실행
cd <your-project-name>
npm install
npm run dev
```

##### 프로젝트 구조

```
my-react-app/
├── node_modules/          # npm 패키지들
├── public/                # 정적 파일 (이미지 등)
├── src/
│   ├── main.jsx          # React 앱 진입점
│   ├── App.jsx           # 최상위 컴포넌트
│   ├── App.css           # App 컴포넌트 스타일
│   └── index.css         # 전역 스타일
├── .gitignore
├── eslint.config.js      # ESLint 설정
├── index.html            # 루트 HTML 페이지
├── package.json          # 프로젝트 메타데이터
├── package-lock.json     # 의존성 버전 고정
└── vite.config.js        # Vite 설정
```

##### ESLint + Prettier 설정

```bash
# Prettier 설치
npm i -D prettier eslint-config-prettier
```

```javascript
// eslint.config.js
import prettier from "eslint-config-prettier";
export default [
  ...,
  prettier,
  {
    rules: {
      'react/prop-types': 'off',  // TypeScript 사용 시 불필요
    }
  }
];
```

```json
// .prettierrc.json
{
  "printWidth": 100,
  "singleQuote": true,
  "semi": true,
  "tabWidth": 2,
  "trailingComma": "all",
  "endOfLine": "auto"
}
```

##### npm 스크립트

| 명령어 | 설명 |
|--------|------|
| `npm run dev` | 개발 서버 실행 (핫 리로드) |
| `npm run build` | 프로덕션 빌드 (dist/ 폴더) |

---

#### 3. React 앱 구조 이해

##### 진입점 (main.jsx)

```jsx
import { createRoot } from 'react-dom/client';
import { StrictMode } from 'react';
import App from './App';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
```

| 요소 | 설명 |
|------|------|
| `createRoot` | React 컴포넌트를 렌더링할 DOM 루트 생성 |
| `render` | JSX로 표현된 컴포넌트를 DOM에 렌더링 |
| `StrictMode` | 개발 모드에서 잠재적 문제 감지 및 경고 |

##### 컴포넌트 트리

```
┌─────────────────────────────────────────────────────────────┐
│                    Component Tree                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    ┌────────────┐                           │
│                    │ StrictMode │  ← 루트 컴포넌트          │
│                    └─────┬──────┘                           │
│                          │                                  │
│                    ┌─────▼──────┐                           │
│                    │    App     │                           │
│                    └─────┬──────┘                           │
│           ┌──────────────┼──────────────┐                   │
│           │              │              │                   │
│     ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐            │
│     │  Header   │  │   Main    │  │  Footer   │            │
│     └───────────┘  └───────────┘  └───────────┘            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

#### 4. 컴포넌트 생성

##### 기본 컴포넌트 문법

```jsx
// Alert.jsx
export function Alert() {
  return (
    <div>
      <div>
        <span role="img" aria-label="Warning">⚠️</span>
        <span>Oh no!</span>
      </div>
      <div>Something went wrong</div>
    </div>
  );
}
```

##### 컴포넌트 규칙

| 규칙 | 설명 |
|------|------|
| **대문자 시작** | 컴포넌트 이름은 대문자로 시작 (소문자는 DOM 요소로 처리) |
| **파일 확장자** | `.js` 또는 `.jsx` |
| **단일 파일** | 일반적으로 컴포넌트당 하나의 파일 |
| **export** | 다른 파일에서 사용하려면 export 필요 |

##### Arrow Function 문법

```jsx
const Alert = () => {
  return (
    <div>
      {/* ... */}
    </div>
  );
};
```

##### 컴포넌트 사용

```jsx
// App.jsx
import { Alert } from './Alert';

function App() {
  return <Alert />;
}
```

---

#### 5. Props 사용

Props는 부모 컴포넌트가 자식 컴포넌트에 데이터를 전달하는 방법이다.

##### Props 전달 (부모)

```jsx
<Alert
  type="information"
  heading="Success"
  closable
>
  Everything is really good!
</Alert>
```

##### Props 수신 (자식)

```jsx
// 방법 1: props 객체
export function Alert(props) {
  return (
    <div>
      <span>{props.heading}</span>
      <div>{props.children}</div>
    </div>
  );
}

// 방법 2: 구조 분해 할당 (권장)
export function Alert({ type, heading, children }) {
  return (
    <div>
      <span>{heading}</span>
      <div>{children}</div>
    </div>
  );
}
```

##### Props 기본값

```jsx
export function Alert({
  type = 'information',  // 기본값 설정
  heading,
  children
}) {
  // ...
}
```

##### children Prop

```jsx
// children은 컴포넌트 태그 사이의 내용
<Alert>
  This is the children content!
</Alert>

// Alert 컴포넌트에서
function Alert({ children }) {
  return <div>{children}</div>;
}
```

---

#### 6. State 사용

State는 컴포넌트의 동적 데이터로, 변경 시 컴포넌트가 **re-render**된다.

##### useState Hook

```jsx
import { useState } from 'react';

function Alert({ closable }) {
  // [상태값, 상태변경함수] = useState(초기값)
  const [visible, setVisible] = useState(true);

  if (!visible) {
    return null;  // 조건부 렌더링
  }

  return (
    <div>
      {/* ... */}
    </div>
  );
}
```

##### 여러 개의 State

```jsx
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);
const [data, setData] = useState([]);
```

##### 조건부 렌더링 패턴

```jsx
// 1. if 문
if (!visible) {
  return null;
}

// 2. 논리 AND (&&)
{closable && (
  <button>Close</button>
)}

// 3. 삼항 연산자
{type === 'warning' ? '⚠️' : 'ℹ️'}
```

---

#### 7. Events 사용

##### 이벤트 핸들러 등록

```jsx
// 방법 1: 별도 함수
function Alert() {
  function handleCloseClick() {
    console.log('Close button clicked');
  }

  return (
    <button onClick={handleCloseClick}>Close</button>
  );
}

// 방법 2: 인라인 함수
<button onClick={() => console.log('clicked')}>Close</button>
```

##### State와 이벤트 결합

```jsx
function Alert({ closable }) {
  const [visible, setVisible] = useState(true);

  function handleCloseClick() {
    setVisible(false);  // 상태 변경 → re-render
  }

  if (!visible) {
    return null;
  }

  return (
    <div>
      {closable && (
        <button onClick={handleCloseClick}>
          <span role="img" aria-label="Close">❌</span>
        </button>
      )}
    </div>
  );
}
```

##### 커스텀 이벤트 (Props로 구현)

```jsx
// Alert.jsx - 커스텀 이벤트 정의
export function Alert({ onClose, closable }) {
  const [visible, setVisible] = useState(true);

  function handleCloseClick() {
    setVisible(false);
    if (onClose) {  // 선택적 호출
      onClose();
    }
  }

  // ...
}

// App.jsx - 커스텀 이벤트 핸들링
<Alert
  closable
  onClose={() => console.log('Alert closed!')}
>
  Content here
</Alert>
```

---

#### 8. React Developer Tools

Chrome, Firefox, Edge에서 사용 가능한 브라우저 확장 프로그램.

##### Components 패널

```
┌─────────────────────────────────────────────────────────────┐
│                   Components Panel                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Component Tree          │  Selected Component Info        │
│  ────────────────        │  ─────────────────────────       │
│  ▼ StrictMode           │                                  │
│    ▼ App                │  props:                          │
│      ▼ Alert            │    type: "information"           │
│                         │    heading: "Success"            │
│                         │    closable: true                │
│                         │                                  │
│                         │  hooks:                          │
│                         │    State(visible): true          │
│                         │                                  │
└─────────────────────────────────────────────────────────────┘
```

| 기능 | 설명 |
|------|------|
| **Props 검사** | 현재 prop 값 확인 및 수정 가능 |
| **State 검사** | 현재 state 값 확인 및 수정 가능 |
| **실시간 테스트** | 값 변경 시 즉시 UI 업데이트 |

##### Profiler 패널

```
┌─────────────────────────────────────────────────────────────┐
│                    Profiler Panel                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Start] ─── [User Interaction] ─── [Stop]                  │
│                                                             │
│  Timeline:                                                  │
│  ┌────────────────────────────────────────────┐            │
│  │ Alert re-rendered                          │            │
│  │ Duration: 0.7ms                            │            │
│  │ Reason: State changed (visible)            │            │
│  └────────────────────────────────────────────┘            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| 기능 | 설명 |
|------|------|
| **렌더링 시간 측정** | 컴포넌트별 렌더링 소요 시간 |
| **렌더링 원인 추적** | 왜 re-render 되었는지 확인 |
| **성능 병목 탐지** | 느린 컴포넌트 식별 |

---

### 🔍 심화 학습

#### 함수 컴포넌트 vs 클래스 컴포넌트

| 구분 | 함수 컴포넌트 | 클래스 컴포넌트 |
|------|--------------|----------------|
| **문법** | 일반 함수 | ES6 클래스 |
| **State** | useState Hook | this.state |
| **Lifecycle** | useEffect Hook | componentDidMount 등 |
| **코드량** | 적음 | 많음 |
| **Hooks 사용** | 가능 | 불가능 |
| **현재 추세** | 권장 | 레거시 |

#### JSX 규칙

```jsx
// 1. 단일 루트 요소 필수
// ❌ 잘못됨
return (
  <div>First</div>
  <div>Second</div>
);

// ✅ 올바름 - Fragment 사용
return (
  <>
    <div>First</div>
    <div>Second</div>
  </>
);

// 2. className (class 아님)
<div className="container">...</div>

// 3. JavaScript 표현식은 중괄호
<div>{variable}</div>
<div>{1 + 2}</div>
<div>{condition ? 'Yes' : 'No'}</div>

// 4. Self-closing 태그
<img src="..." />
<Alert />
```

---

### 💡 실무 적용 포인트

1. **Vite 사용**: CRA 대신 Vite로 빠른 개발 환경 구축
2. **ESLint + Prettier**: 코드 품질과 일관성 유지
3. **컴포넌트 분리**: 재사용 가능한 단위로 분리
4. **Props 구조 분해**: `props.xxx` 대신 구조 분해 할당 사용
5. **조건부 렌더링**: `&&` 연산자와 삼항 연산자 활용
6. **커스텀 이벤트**: `onXxx` 패턴으로 명명
7. **선택적 이벤트**: `if (onEvent) onEvent()` 패턴
8. **Developer Tools**: 개발 중 상시 활용

---

### ✅ 정리 체크리스트

- [ ] React의 Virtual DOM 개념과 장점을 설명할 수 있다
- [ ] Vite로 React 프로젝트를 생성할 수 있다
- [ ] ESLint와 Prettier를 설정할 수 있다
- [ ] 개발 서버 실행(`npm run dev`)과 프로덕션 빌드(`npm run build`)를 수행할 수 있다
- [ ] React 앱의 진입점(main.jsx)과 컴포넌트 트리 구조를 이해한다
- [ ] JSX 문법을 사용해 컴포넌트를 작성할 수 있다
- [ ] Props로 컴포넌트를 구성 가능하게 만들 수 있다
- [ ] children prop의 용도를 안다
- [ ] useState Hook으로 상태를 관리할 수 있다
- [ ] 조건부 렌더링 패턴(&&, 삼항 연산자)을 사용할 수 있다
- [ ] 이벤트 핸들러를 등록하고 상태를 업데이트할 수 있다
- [ ] 커스텀 이벤트를 function prop으로 구현할 수 있다
- [ ] React Developer Tools의 Components와 Profiler 패널을 사용할 수 있다

---

### 🔗 참고 자료

- [React 공식 문서](https://react.dev/)
- [Vite 공식 문서](https://vitejs.dev/)
- [ESLint 공식 문서](https://eslint.org/)
- [Prettier 공식 문서](https://prettier.io/)
- [React Developer Tools (Chrome)](https://chromewebstore.google.com/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi)
- [JSX 소개 - React 공식](https://react.dev/learn/writing-markup-with-jsx)
- [MDN - JavaScript 구조 분해 할당](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment)
