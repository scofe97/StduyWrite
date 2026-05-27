# React 패턴 (HOC, Render Props, Compound)

## 개요

**정의**: React 패턴은 컴포넌트 간 로직 재사용과 관심사 분리를 위한 설계 기법이다.

**목적**: 코드 중복을 줄이고 컴포넌트의 재사용성과 유지보수성을 향상시킨다.

---

## 핵심 개념

### 패턴 선택 가이드

```
로직 재사용 필요
    │
    ├─ 상태나 로직을 여러 컴포넌트에서 공유?
    │       └─ Yes → Custom Hooks (권장)
    │
    ├─ 렌더링 결과를 동적으로 결정?
    │       └─ Yes → Render Props 패턴
    │
    ├─ 컴포넌트에 기능을 투명하게 추가?
    │       └─ Yes → HOC 패턴
    │
    └─ 관련 컴포넌트를 하나의 API로 묶기?
            └─ Yes → Compound Components
```

### 패턴 비교

| 패턴 | 로직 공유 방식 | Props 전달 | 타입 안전성 | 현재 권장도 |
|------|--------------|-----------|------------|------------|
| HOC | 컴포넌트 래핑 | 암시적 | 어려움 | 레거시 |
| Render Props | 함수 prop | 명시적 | 중간 | 특정 케이스 |
| Custom Hooks | 함수 호출 | 명시적 | 높음 | **권장** |

---

## 구현 패턴

### 1. Higher-Order Component (HOC)

**정의**: 컴포넌트를 받아 새로운 컴포넌트를 반환하는 함수

```
┌──────────────────────────────────────────────────────────┐
│                    HOC 동작 원리                          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   Component ──→ HOC(Component) ──→ Enhanced Component   │
│                                                          │
│   예시:                                                  │
│   Button ──→ withStyles(Button) ──→ StyledButton        │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

#### 기본 HOC 구현

```javascript
// withStyles HOC - 스타일 추가
function withStyles(WrappedComponent) {
    return function EnhancedComponent(props) {
        const style = { padding: '0.2rem', margin: '1rem' };
        return <WrappedComponent style={style} {...props} />;
    };
}

// 사용
const Button = () => <button>Click me!</button>;
const StyledButton = withStyles(Button);
```

#### withLoader HOC 예제

```javascript
// 로딩 상태를 처리하는 HOC
function withLoader(WrappedComponent, url) {
    return function WithLoaderComponent(props) {
        const [data, setData] = useState(null);
        const [loading, setLoading] = useState(true);

        useEffect(() => {
            async function fetchData() {
                const response = await fetch(url);
                const result = await response.json();
                setData(result);
                setLoading(false);
            }
            fetchData();
        }, []);

        if (loading) {
            return <div>Loading...</div>;
        }

        return <WrappedComponent {...props} data={data} />;
    };
}

// 사용
function DogImages({ data }) {
    return data.message.map((dog, index) => (
        <img src={dog} alt="Dog" key={index} />
    ));
}

export default withLoader(
    DogImages,
    "https://dog.ceo/api/breed/labrador/images/random/6"
);
```

#### HOC 합성

```javascript
// 여러 HOC 조합
function withHover(Component) {
    return function WithHoverComponent(props) {
        const [hovering, setHovering] = useState(false);

        return (
            <div
                onMouseEnter={() => setHovering(true)}
                onMouseLeave={() => setHovering(false)}
            >
                <Component {...props} hovering={hovering} />
            </div>
        );
    };
}

// HOC 체이닝
export default withHover(withLoader(DogImages, url));
```

#### HOC 장단점

| 장점 | 단점 |
|------|------|
| 로직 재사용 | Props 이름 충돌 가능 |
| 관심사 분리 | Wrapper Hell (깊은 중첩) |
| DRY 원칙 준수 | 디버깅 어려움 |
| 조합 가능 | 암시적 props 주입 |

#### Props 충돌 해결

```javascript
// 문제: style prop 덮어씌움
function withStyles(Component) {
    return props => {
        const style = { padding: '0.2rem', margin: '1rem' };
        return <Component style={style} {...props} />;
        // 기존 props.style이 손실됨
    };
}

// 해결: Props 병합
function withStyles(Component) {
    return props => {
        const style = {
            padding: '0.2rem',
            margin: '1rem',
            ...props.style  // 기존 스타일 병합
        };
        return <Component {...props} style={style} />;
    };
}
```

---

### 2. Render Props 패턴

**정의**: JSX를 반환하는 함수를 prop으로 전달하여 렌더링 권한을 위임

```
┌──────────────────────────────────────────────────────────┐
│                 Render Props 구조                         │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   <DataProvider render={(data) => <Display data={data} />} />
│                                                          │
│   1. DataProvider가 데이터 로직 처리                      │
│   2. render 함수에 데이터 전달                            │
│   3. 소비자가 렌더링 방식 결정                            │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

#### 기본 구현

```javascript
// 데이터를 render prop으로 전달
function DataProvider({ render }) {
    const [data, setData] = useState(null);

    useEffect(() => {
        fetch('/api/data')
            .then(res => res.json())
            .then(setData);
    }, []);

    return render(data);
}

// 사용
<DataProvider
    render={data => (
        <div>
            {data ? <DisplayData data={data} /> : <Loading />}
        </div>
    )}
/>
```

#### 온도 변환기 예제

```javascript
// Input이 render prop을 받아 처리
function Input({ render }) {
    const [value, setValue] = useState("");

    return (
        <>
            <input
                type="text"
                value={value}
                onChange={e => setValue(e.target.value)}
                placeholder="온도 (°C)"
            />
            {render(value)}
        </>
    );
}

function Kelvin({ value }) {
    return <div>{(parseFloat(value) || 0) + 273.15}K</div>;
}

function Fahrenheit({ value }) {
    return <div>{((parseFloat(value) || 0) * 9) / 5 + 32}°F</div>;
}

// 사용
function App() {
    return (
        <Input
            render={value => (
                <>
                    <Kelvin value={value} />
                    <Fahrenheit value={value} />
                </>
            )}
        />
    );
}
```

#### Children as Function

```javascript
// render prop 대신 children 사용
function Input({ children }) {
    const [value, setValue] = useState("");

    return (
        <>
            <input
                value={value}
                onChange={e => setValue(e.target.value)}
            />
            {children(value)}  {/* children을 함수로 호출 */}
        </>
    );
}

// 더 깔끔한 문법
function App() {
    return (
        <Input>
            {value => (
                <>
                    <Kelvin value={value} />
                    <Fahrenheit value={value} />
                </>
            )}
        </Input>
    );
}
```

#### Render Props 장단점

| 장점 | 단점 |
|------|------|
| 명시적 Props 전달 | 대부분 Hooks로 대체 가능 |
| 이름 충돌 없음 | 중첩 시 콜백 지옥 |
| 유연한 렌더링 제어 | 클래스 라이프사이클 사용 불가 |

---

### 3. HOC vs Render Props

| 특성 | HOC | Render Props |
|------|-----|--------------|
| Props 전달 | 암시적 (자동 주입) | 명시적 (함수 인자) |
| 이름 충돌 | 가능 | 없음 |
| 디버깅 | 어려움 | 상대적 용이 |
| 타입 추론 | 복잡 | 중간 |
| 조합성 | HOC 체이닝 | 중첩 함수 |

```javascript
// HOC 방식 - 암시적 props 주입
const EnhancedComponent = withData(withHover(MyComponent));
// MyComponent는 data, hovering props를 받음 (어디서 오는지 불명확)

// Render Props 방식 - 명시적 props 전달
<DataProvider render={data => (
    <HoverProvider render={hovering => (
        <MyComponent data={data} hovering={hovering} />
    )} />
)} />
// 각 prop의 출처가 명확
```

---

### 4. 현대적 대안: Custom Hooks

**권장 접근법**: 대부분의 경우 HOC와 Render Props는 Custom Hooks로 대체 가능

```javascript
// HOC/Render Props 방식
const EnhancedComponent = withLoader(withHover(MyComponent), url);

// Hooks 방식 (권장)
function MyComponent() {
    const { data, loading, error } = useLoader(url);
    const { hovering, hoverProps } = useHover();

    if (loading) return <Loading />;
    if (error) return <Error error={error} />;

    return (
        <div {...hoverProps}>
            {hovering && <Tooltip />}
            <DataDisplay data={data} />
        </div>
    );
}
```

#### Custom Hook 예제

```javascript
// useLoader Hook
function useLoader(url) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        setLoading(true);
        fetch(url)
            .then(res => res.json())
            .then(setData)
            .catch(setError)
            .finally(() => setLoading(false));
    }, [url]);

    return { data, loading, error };
}

// useHover Hook
function useHover() {
    const [hovering, setHovering] = useState(false);

    const hoverProps = {
        onMouseEnter: () => setHovering(true),
        onMouseLeave: () => setHovering(false)
    };

    return { hovering, hoverProps };
}
```

---

## 트레이드오프

### 패턴 선택 체크리스트

```yaml
hoc_pattern:
  use_when:
    - 레거시 코드와의 호환
    - 인증/권한 체크 래핑
    - 서드파티 라이브러리 통합
    - 로깅/분석 기능 주입
  avoid_when:
    - 신규 프로젝트 (Hooks 권장)
    - Props 충돌 위험
    - 타입 안전성 중요

render_props_pattern:
  use_when:
    - 렌더링 제어권 위임 필요
    - 상태를 공유하는 형제 컴포넌트
    - 동적 렌더링 결정
  avoid_when:
    - 단순한 상태 공유 (useState)
    - Hooks로 충분한 경우

custom_hooks:
  use_when:
    - 대부분의 로직 재사용 상황
    - 상태 로직 추출
    - 사이드 이펙트 캡슐화
  avoid_when:
    - 렌더링 자체를 제어해야 할 때
    - 클래스 컴포넌트 환경
```

---

## 면접 포인트

**Q**: HOC와 Render Props의 차이점은?

**A**: HOC는 컴포넌트를 받아 새 컴포넌트를 반환하며 props를 암시적으로 주입한다. Render Props는 함수를 prop으로 전달하여 명시적으로 데이터를 전달한다. HOC는 props 충돌 위험이 있고 Render Props는 충돌이 없지만 중첩 시 복잡해진다. 현대 React에서는 둘 다 Custom Hooks로 대체하는 것이 권장된다.

**Q**: 왜 Hooks가 HOC/Render Props보다 권장되는가?

**A**: Hooks는 함수 호출로 로직을 재사용하여 Wrapper Hell을 방지하고, 반환값이 명시적이라 타입 추론이 쉽다. 조합도 단순한 함수 호출로 가능하며, 컴포넌트 계층 구조를 변경하지 않아 디버깅이 용이하다.

**Q**: HOC를 사용해야 하는 경우는?

**A**: 레거시 클래스 컴포넌트와의 호환, 서드파티 라이브러리 통합(예: Redux connect), 또는 인증/권한 검사 같은 횡단 관심사를 투명하게 적용할 때 여전히 유용하다.

---

## 참고 자료

- [React Higher-Order Components](https://legacy.reactjs.org/docs/higher-order-components.html)
- [React Render Props](https://legacy.reactjs.org/docs/render-props.html)
- [React Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks)
- Dan Abramov, "Use a Render Prop!"
