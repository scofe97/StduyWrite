# React Hooks 심화

## 개요

**정의**: React Hooks는 함수 컴포넌트에서 상태(state)와 라이프사이클(lifecycle)을 사용할 수 있게 해주는 특별한 함수이다.

**목적**: 클래스 컴포넌트의 복잡성을 줄이고, HOC/Render Props의 wrapper hell 문제를 해결하며, 상태 로직을 재사용 가능한 단위로 추출한다.

---

## 핵심 개념

### Hook의 규칙 (Rules of Hooks)

| 규칙 | 설명 | 위반 시 문제 |
|------|------|-------------|
| **최상위 호출** | 함수 컴포넌트의 최상위에서만 호출 | 조건부 Hook 호출 시 순서 불일치 |
| **조건부 호출 금지** | if문, 반복문, 중첩 함수 안에서 호출 불가 | React 내부 상태 추적 실패 |
| **함수 컴포넌트 전용** | 클래스 컴포넌트에서는 사용 불가 | 문법 오류 |

```javascript
// 잘못된 예: 조건문 안에서 호출
function Component() {
  if (condition) {
    const [count, setCount] = useState(0);  // 규칙 위반
  }
}

// 올바른 예: 최상위에서 호출 후 조건부 로직
function Component() {
  const [clicked, setClicked] = useState(false);

  useEffect(() => {
    if (clicked) {
      console.log("Clicked!");
    }
  }, [clicked]);
}
```

---

## 구현 패턴

### 1. useState: 상태 관리

**기본 사용법**:

```javascript
const [state, setState] = useState(initialValue);

// 원시값
const [count, setCount] = useState(0);
const [name, setName] = useState("");
const [loading, setLoading] = useState(true);

// 상태 업데이트
setCount(count + 1);                    // 직접 값 설정
setCount(prevCount => prevCount + 1);   // 함수형 업데이트 (권장)
```

**여러 상태 관리**:

```javascript
function Form() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [age, setAge] = useState(0);

  return (
    <form>
      <input value={name} onChange={e => setName(e.target.value)} />
      <input value={email} onChange={e => setEmail(e.target.value)} />
      <input type="number" value={age} onChange={e => setAge(Number(e.target.value))} />
    </form>
  );
}
```

---

### 2. useReducer: 복잡한 상태 로직

**useState vs useReducer 선택 기준**:

| 상황 | 권장 Hook |
|------|-----------|
| 단순한 원시값 (숫자, 문자열, 불린) | useState |
| 복잡한 객체 상태 | useReducer |
| 여러 상태 값이 연관되어 함께 변경 | useReducer |
| 다음 상태가 이전 상태에 의존 | useReducer |
| 상태 변경 로직이 복잡함 | useReducer |

**Discriminated Union으로 타입 안전하게 구현**:

```typescript
// 1. State 타입 정의
type State = {
  name: string | undefined;
  score: number;
  loading: boolean;
};

// 2. Action 타입 정의 (Discriminated Union)
type Action =
  | { type: 'initialize'; name: string }
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'reset' };

// 3. Reducer 함수
function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'initialize':
      return { name: action.name, score: 0, loading: false };
    case 'increment':
      return { ...state, score: state.score + 1 };
    case 'decrement':
      return { ...state, score: state.score - 1 };
    case 'reset':
      return { ...state, score: 0 };
    default:
      return state;
  }
}

// 4. 컴포넌트에서 사용
function Counter() {
  const [{ name, score, loading }, dispatch] = useReducer(reducer, {
    name: undefined,
    score: 0,
    loading: true,
  });

  return (
    <div>
      <h3>{name}: {score}</h3>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <button onClick={() => dispatch({ type: 'reset' })}>Reset</button>
    </div>
  );
}
```

---

### 3. useEffect: 사이드 이펙트

**의존성 배열에 따른 실행 시점**:

| 의존성 배열 | 실행 시점 | 사용 사례 |
|------------|----------|----------|
| 생략 | 매 렌더링마다 | 거의 사용 안 함 |
| `[]` | 초기 렌더링 시 1회 | 초기 데이터 페칭, 이벤트 등록 |
| `[a, b]` | a 또는 b 변경 시 | 값 변경에 따른 부수효과 |

**데이터 페칭 패턴**:

```javascript
// async/await 올바른 사용법
useEffect(() => {
  async function fetchData() {
    const response = await fetch('/api/data');
    const result = await response.json();
    setData(result);
  }
  fetchData();
}, []);

// 잘못된 예: effect 함수에 async 직접 사용
useEffect(async () => {
  const data = await fetch('/api/data');  // 오류!
}, []);
```

**Cleanup 함수**:

```javascript
useEffect(() => {
  const handleClick = () => onClickAnywhere();
  document.addEventListener("click", handleClick);

  // 정리 함수 반환
  return () => {
    document.removeEventListener("click", handleClick);
  };
}, [onClickAnywhere]);
```

---

### 4. useRef: DOM 접근 및 값 보존

**특징**:
- 값이 변경되어도 리렌더링 발생 안 함
- 컴포넌트 생애주기 동안 값 유지
- `.current` 속성으로 값 접근/변경

**DOM 요소 접근**:

```typescript
function FocusInput() {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  return <input ref={inputRef} type="text" />;
}
```

**일반적인 HTML 요소 타입**:

| 요소 | TypeScript 타입 |
|------|-----------------|
| `<button>` | `HTMLButtonElement` |
| `<input>` | `HTMLInputElement` |
| `<div>` | `HTMLDivElement` |
| `<form>` | `HTMLFormElement` |

---

### 5. useMemo와 useCallback: 성능 최적화

**useMemo: 값 메모이제이션**:

```javascript
const memoizedValue = useMemo(
  () => expensiveCalculation(a, b),
  [a, b]
);
```

**useCallback: 함수 메모이제이션**:

```javascript
const memoizedCallback = useCallback(
  () => handleClick(id),
  [id]
);
```

**비교**:

| Hook | 메모이제이션 대상 | 반환값 |
|------|------------------|--------|
| useMemo | **값** | 계산된 값 |
| useCallback | **함수** | 함수 자체 |

**React.memo와 조합**:

```javascript
// 자식 컴포넌트
const ResetButton = memo(({ onClick }: { onClick: () => void }) => {
  console.log("render ResetButton");
  return <button onClick={onClick}>Reset</button>;
});

// 부모 컴포넌트
function Parent() {
  const [state, dispatch] = useReducer(reducer, initialState);

  // useCallback으로 함수 메모이제이션
  const handleReset = useCallback(
    () => dispatch({ type: 'reset' }),
    []
  );

  return <ResetButton onClick={handleReset} />;
}
```

---

### 6. 커스텀 Hook: 로직 재사용

**규칙**: Hook 이름은 반드시 `use`로 시작해야 한다.

**useKeyPress 예제**:

```javascript
function useKeyPress(targetKey) {
  const [keyPressed, setKeyPressed] = useState(false);

  useEffect(() => {
    const handleDown = ({ key }) => {
      if (key === targetKey) setKeyPressed(true);
    };
    const handleUp = ({ key }) => {
      if (key === targetKey) setKeyPressed(false);
    };

    window.addEventListener("keydown", handleDown);
    window.addEventListener("keyup", handleUp);

    return () => {
      window.removeEventListener("keydown", handleDown);
      window.removeEventListener("keyup", handleUp);
    };
  }, [targetKey]);

  return keyPressed;
}

// 사용
function App() {
  const isQPressed = useKeyPress("q");
  return <div>{isQPressed && "Q is pressed!"}</div>;
}
```

**useLocalStorage 예제**:

```javascript
function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      return initialValue;
    }
  });

  const setValue = value => {
    try {
      const valueToStore = value instanceof Function
        ? value(storedValue)
        : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(error);
    }
  };

  return [storedValue, setValue];
}
```

---

### 7. 기타 Hooks

**useContext**: Context 값 접근

```javascript
const ThemeContext = React.createContext("light");

function ThemedButton() {
  const theme = useContext(ThemeContext);
  return <button className={theme}>Themed Button</button>;
}
```

**useId**: 고유 ID 생성 (접근성)

```javascript
function Field({ label, name }) {
  const id = useId();
  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <input id={id} name={name} type="text" />
    </div>
  );
}
```

**useTransition**: UI 블로킹 없이 상태 전환

```javascript
function SearchList() {
  const [query, setQuery] = useState("");
  const [list, setList] = useState(names);
  const [isPending, startTransition] = useTransition();

  return (
    <div>
      <input
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);  // 높은 우선순위
          startTransition(() => {     // 낮은 우선순위
            setList(names.filter(/* ... */));
          });
        }}
      />
      {isPending && <p>Loading...</p>}
    </div>
  );
}
```

---

## 트레이드오프

### Hooks vs 클래스 컴포넌트

| 항목 | 클래스 | Hooks |
|------|--------|-------|
| 코드량 | 많음 (보일러플레이트) | 적음 |
| this 바인딩 | 필요 | 불필요 |
| 상태 접근 | this.state.x | x |
| 상태 업데이트 | this.setState() | setX() |
| 라이프사이클 | 메서드 분리 | useEffect 통합 |
| 로직 재사용 | HOC/Render Props | 커스텀 Hook |

### 메모이제이션 사용 주의사항

```javascript
// 잘못된 예: 의존성 배열 비어있음
const handleClick = useCallback(() => {
  setCount(count + 1);  // count는 항상 0
}, []);

// 올바른 예 1: 의존성 포함
const handleClick = useCallback(() => {
  setCount(count + 1);
}, [count]);

// 올바른 예 2: 함수형 업데이트
const handleClick = useCallback(() => {
  setCount(prev => prev + 1);
}, []);
```

---

## 실무 적용

### 커스텀 Hook 라이브러리

| 라이브러리 | 특징 |
|-----------|------|
| react-use | 다양한 유틸리티 Hooks |
| useHooks | 실용적인 Hooks 모음 |
| ahooks | Alibaba의 Hooks 라이브러리 |

### 자주 사용되는 커스텀 Hooks

- `useDebounce`: 디바운싱
- `useThrottle`: 쓰로틀링
- `useWindowSize`: 윈도우 크기
- `useOnClickOutside`: 외부 클릭 감지
- `usePrevious`: 이전 값 기억
- `useAsync`: 비동기 상태 관리

### 사용 가이드라인

```yaml
performance_optimization:
  use_when:
    - 실제 성능 문제가 있을 때
    - 렌더링 비용이 높은 컴포넌트
    - 자식에게 콜백을 props로 전달할 때
  avoid_when:
    - 단순한 컴포넌트
    - 의존성이 자주 변경되는 경우
    - 조기 최적화

custom_hooks:
  use_when:
    - 상태 로직이 여러 컴포넌트에서 반복
    - 복잡한 로직을 캡슐화
    - 테스트 용이성 필요
  naming:
    - 반드시 use로 시작
    - 목적을 명확히 표현
```

---

## 면접 포인트

**Q**: useState와 useReducer의 차이점과 선택 기준은?

**A**: useState는 단순한 원시값 상태에 적합하고, useReducer는 복잡한 객체 상태나 여러 값이 연관되어 변경될 때 적합하다. useReducer는 상태 변경 로직을 reducer 함수로 분리하여 테스트하기 쉽고, 복잡한 상태 전환을 명시적으로 관리할 수 있다.

**Q**: useCallback과 useMemo의 차이는?

**A**: useMemo는 계산된 값을 메모이제이션하고, useCallback은 함수 자체를 메모이제이션한다. useCallback은 사실상 `useMemo(() => fn, deps)`의 축약형이다. 둘 다 의존성이 변경될 때만 재계산/재생성된다.

**Q**: Hook의 규칙과 그 이유는?

**A**: Hook은 컴포넌트 최상위에서만 호출해야 하며, 조건문이나 반복문 안에서 호출할 수 없다. 이는 React가 Hook 호출 순서로 상태를 추적하기 때문이다. 순서가 바뀌면 React가 어떤 상태가 어떤 Hook에 해당하는지 알 수 없게 된다.

---

## 참고 자료

- [React Hooks Reference](https://react.dev/reference/react)
- [Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks)
- [useHooks](https://usehooks.com/)
- [React Use](https://github.com/streamich/react-use)
