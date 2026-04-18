# React 테스트

## 개요

**정의**: React 테스트는 Vitest(테스트 러너)와 React Testing Library(테스트 유틸리티)를 조합하여 컴포넌트의 동작을 사용자 관점에서 검증하는 자동화된 품질 보증 과정이다.

**목적**: 회귀 버그 방지, 리팩토링 안전성 확보, 컴포넌트 동작 문서화, 개발 생산성 향상을 달성한다.

---

## 핵심 개념

### 테스트 라이브러리 생태계

| 라이브러리 | 역할 | 설명 |
|-----------|------|------|
| **Vitest** | 테스트 러너 | 테스트 실행, 어서션, 모킹 |
| **@testing-library/react** | 컴포넌트 렌더링 | render, screen 제공 |
| **@testing-library/dom** | DOM 쿼리 | getBy, queryBy, findBy 등 |
| **@testing-library/jest-dom** | 커스텀 매처 | toBeInTheDocument 등 |
| **@testing-library/user-event** | 이벤트 시뮬레이션 | 실제 사용자처럼 상호작용 |

### Vitest vs Jest

| 항목 | Jest | Vitest |
|------|------|--------|
| 번들러 통합 | Webpack/Babel | Vite (네이티브 ESM) |
| 설정 | 별도 설정 필요 | Vite 설정 재사용 |
| 속도 | 상대적 느림 | HMR 기반 빠른 실행 |
| TypeScript | ts-jest 필요 | 기본 지원 |
| API 호환성 | - | Jest API 호환 |

### Testing Library 철학

> "The more your tests resemble the way your software is used, the more confidence they can give you."

```typescript
// 나쁜 예: 구현 세부사항 테스트
expect(component.state.isOpen).toBe(true);

// 좋은 예: 사용자 동작 테스트
await user.click(screen.getByRole('button', { name: '메뉴 열기' }));
expect(screen.getByRole('menu')).toBeVisible();
```

---

## 구현 패턴

### 1. Vitest 설정

```typescript
// vite.config.ts
import { defineConfig, mergeConfig } from 'vite';
import { defineConfig as defineVitestConfig } from 'vitest/config';

const viteConfig = defineConfig({
  plugins: [react()],
});

const vitestConfig = defineVitestConfig({
  test: {
    globals: true,           // describe, it, expect 전역 사용
    environment: 'jsdom',    // DOM 시뮬레이션
    setupFiles: './vitest.setup.ts',
    include: ['src/**/*.{test,spec}.{ts,tsx}'],
    coverage: {
      exclude: ['**/types.ts', '**/index.ts'],
    },
  },
});

export default mergeConfig(viteConfig, vitestConfig);
```

```typescript
// vitest.setup.ts
import '@testing-library/jest-dom/vitest';
```

```json
// package.json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage"
  }
}
```

---

### 2. 순수 함수 테스트

```typescript
import { describe, it, expect } from 'vitest';

// 기본 테스트 구조
test('should return true when in checkedIds', () => {
  const result = isChecked([1, 2, 3], 2);
  expect(result).toBe(true);
});

// 주요 Matcher
expect(value).toBe(3);                    // 원시값 비교 (===)
expect(obj).toStrictEqual({ a: 1 });      // 객체 깊은 비교
expect(result).not.toBe(null);            // 반대 조건
expect(arr).toContain(99);                // 배열 포함
expect(str).toMatch(/error/);             // 정규식

// 예외 테스트 - 함수로 감싸기
expect(() => {
  assertValueCanBeRendered(true);
}).toThrow('value is not a string or a number');
```

---

### 3. 컴포넌트 테스트

```typescript
import { render, screen } from '@testing-library/react';
import { Checklist } from './Checklist';

test('should render correct list items', () => {
  render(
    <Checklist
      data={[{ id: 1, name: 'Lucy', role: 'Manager' }]}
      id="id"
      primary="name"
      secondary="role"
    />
  );

  expect(screen.getByText('Lucy')).toBeInTheDocument();
  expect(screen.getByText('Manager')).toBeInTheDocument();
});
```

### 쿼리 타입

| 쿼리 타입 | 요소 없을 때 | 용도 |
|-----------|-------------|------|
| `getBy*` | 에러 발생 | 요소가 있어야 할 때 |
| `queryBy*` | null 반환 | 요소 부재 확인 |
| `findBy*` | 에러 (재시도 후) | 비동기 요소 |
| `getAllBy*` | 에러 발생 | 다수 요소 |
| `queryAllBy*` | 빈 배열 | 다수 요소 부재 확인 |

### 쿼리 우선순위 (권장 순서)

```typescript
// 1순위: 접근성 쿼리
screen.getByRole('button', { name: '저장' });
screen.getByLabelText('이메일');
screen.getByPlaceholderText('Enter name');
screen.getByText('Submit');

// 2순위: 시맨틱 쿼리
screen.getByAltText('Logo');
screen.getByTitle('Close');

// 3순위: 테스트 ID (최후의 수단)
screen.getByTestId('submit-btn');
```

---

### 4. user-event로 상호작용 테스트

```typescript
import userEvent from '@testing-library/user-event';

test('should check and uncheck when clicked', async () => {
  const user = userEvent.setup();  // 항상 setup() 호출

  render(<Checklist data={[{ id: 1, name: 'Lucy' }]} />);

  const checkbox = screen.getByTestId('Checklist__input__1');

  expect(checkbox).not.toBeChecked();
  await user.click(checkbox);
  expect(checkbox).toBeChecked();
});

// 다양한 상호작용
await user.type(screen.getByRole('textbox'), 'Hello');
await user.clear(screen.getByRole('textbox'));
await user.tab();
await user.keyboard('{Enter}');
await user.selectOptions(screen.getByRole('combobox'), 'option1');
await user.hover(screen.getByRole('button'));
```

---

### 5. 모킹 (Mocking)

#### 함수 모킹

```typescript
import { vi } from 'vitest';

test('콜백 함수 호출 확인', async () => {
  const handleChange = vi.fn();

  render(<Input onChange={handleChange} />);
  await user.type(screen.getByRole('textbox'), 'test');

  expect(handleChange).toHaveBeenCalled();
  expect(handleChange).toHaveBeenCalledWith('test');
  expect(handleChange).toHaveBeenCalledTimes(4);  // 각 글자마다
});

// 반환값 지정
const mockFn = vi.fn()
  .mockReturnValue('기본값')
  .mockReturnValueOnce('첫번째 호출');

// 구현 지정
const mockFn = vi.fn().mockImplementation((a, b) => a + b);
```

#### 모듈 모킹

```typescript
vi.mock('./api', () => ({
  fetchUser: vi.fn().mockResolvedValue({ id: 1, name: 'Test' }),
}));

test('API 호출을 모킹한다', async () => {
  const user = await fetchUser(1);
  expect(user).toEqual({ id: 1, name: 'Test' });
});
```

#### 타이머 모킹

```typescript
beforeEach(() => {
  vi.useFakeTimers();
});

afterEach(() => {
  vi.useRealTimers();
});

test('setTimeout을 테스트한다', () => {
  const callback = vi.fn();
  setTimeout(callback, 1000);

  expect(callback).not.toHaveBeenCalled();
  vi.advanceTimersByTime(1000);
  expect(callback).toHaveBeenCalled();
});
```

---

### 6. 비동기 테스트

```typescript
import { waitFor, waitForElementToBeRemoved } from '@testing-library/react';

test('데이터 로딩 후 표시', async () => {
  render(<AsyncComponent />);

  // 로딩 상태 확인
  expect(screen.getByText('로딩 중...')).toBeInTheDocument();

  // findBy로 비동기 요소 대기 (기본 1초)
  expect(await screen.findByText('로딩 완료')).toBeInTheDocument();

  // 로딩 요소가 사라졌는지 확인
  expect(screen.queryByText('로딩 중...')).not.toBeInTheDocument();
});

test('waitFor로 조건 대기', async () => {
  render(<Counter />);
  await user.click(screen.getByRole('button'));

  await waitFor(() => {
    expect(screen.getByText('카운트: 1')).toBeInTheDocument();
  });
});

test('요소 제거 대기', async () => {
  render(<Modal />);
  await user.click(screen.getByRole('button', { name: '닫기' }));

  await waitForElementToBeRemoved(() => screen.queryByRole('dialog'));
});
```

---

### 7. 커스텀 훅 테스트

```typescript
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

test('초기값을 설정할 수 있다', () => {
  const { result } = renderHook(() => useCounter(10));
  expect(result.current.count).toBe(10);
});

test('증가/감소가 동작한다', () => {
  const { result } = renderHook(() => useCounter(0));

  act(() => {
    result.current.increment();
  });
  expect(result.current.count).toBe(1);

  act(() => {
    result.current.decrement();
  });
  expect(result.current.count).toBe(0);
});
```

---

### 8. Provider 래핑 (customRender)

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';

const customRender = (ui: React.ReactElement, options = {}) => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });

  const Wrapper = ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>{children}</BrowserRouter>
    </QueryClientProvider>
  );

  return render(ui, { wrapper: Wrapper, ...options });
};

// 사용
test('Provider가 필요한 컴포넌트', () => {
  customRender(<MyComponent />);
});
```

---

### 9. 스냅샷 테스트

```typescript
test('기본 버튼과 일치한다', () => {
  const { container } = render(<Button>Click me</Button>);
  expect(container).toMatchSnapshot();
});

test('인라인 스냅샷', () => {
  const result = formatDate(new Date('2024-01-01'));
  expect(result).toMatchInlineSnapshot(`"2024-01-01"`);
});
```

---

### 10. Props 변경 테스트 (rerender)

```typescript
test('variant에 따라 스타일이 달라진다', () => {
  const { rerender } = render(<Button variant="primary">버튼</Button>);
  expect(screen.getByRole('button')).toHaveClass('btn-primary');

  rerender(<Button variant="secondary">버튼</Button>);
  expect(screen.getByRole('button')).toHaveClass('btn-secondary');
});
```

---

## jest-dom 주요 Matcher

| Matcher | 용도 |
|---------|------|
| `toBeInTheDocument()` | DOM에 존재 확인 |
| `toBeVisible()` | 화면에 보이는지 |
| `toBeChecked()` | 체크박스 체크 상태 |
| `toBeDisabled()` | 비활성화 상태 |
| `toHaveTextContent()` | 텍스트 내용 |
| `toHaveAttribute()` | 속성 값 |
| `toHaveClass()` | CSS 클래스 |
| `toHaveValue()` | 입력 필드 값 |
| `toHaveFocus()` | 포커스 상태 |

---

## 트레이드오프

### 테스트 피라미드

| 테스트 종류 | 범위 | 속도 | 신뢰도 | 비용 |
|------------|------|------|--------|------|
| **단위 테스트** | 함수, 훅 | 빠름 | 낮음 | 저렴 |
| **컴포넌트 테스트** | 단일 컴포넌트 | 중간 | 중간 | 중간 |
| **통합 테스트** | 여러 컴포넌트 | 중간 | 높음 | 높음 |
| **E2E 테스트** | 전체 앱 | 느림 | 매우 높음 | 비쌈 |

### fireEvent vs user-event

| 특성 | fireEvent | user-event |
|------|-----------|------------|
| 이벤트 발생 | 단일 이벤트 | 실제 사용자처럼 여러 이벤트 |
| 결합도 | 높음 | 낮음 |
| 권장도 | 비권장 | **권장** |

---

## 실무 체크리스트

```yaml
test_priority:
  - 유틸리티 함수: 순수 함수 단위 테스트
  - 커스텀 훅: renderHook으로 훅 동작 테스트
  - 핵심 컴포넌트: 비즈니스 로직이 있는 컴포넌트
  - 사용자 플로우: 주요 시나리오 통합 테스트

common_mistakes:
  - toBe로 객체 비교 → toStrictEqual 사용
  - findBy에 await 누락 → async/await 필수
  - getBy로 부재 확인 → queryBy 사용
  - fireEvent 사용 → user-event 사용
  - 구현 세부사항 테스트 → 사용자 동작 테스트
```

---

## 면접 포인트

**Q**: getBy, findBy, queryBy의 차이점은?

**A**: getBy는 동기적으로 요소를 찾고 없으면 에러를 던진다. queryBy는 없으면 null을 반환하여 요소 부재를 확인할 때 사용한다. findBy는 비동기로 최대 1초까지 재시도하며 없으면 에러를 던진다. 비동기로 나타나는 요소에 사용한다.

**Q**: user-event가 fireEvent보다 나은 이유는?

**A**: fireEvent는 단일 이벤트만 발생시키지만 user-event는 실제 사용자처럼 mouseDown, click, mouseUp 등 여러 이벤트를 순서대로 발생시킨다. 이로 인해 구현에 덜 결합되고 실제 브라우저 동작에 더 가깝게 테스트할 수 있다.

**Q**: 코드 커버리지 100%가 좋은 테스트를 의미하나요?

**A**: 아니다. 커버리지는 실행된 코드만 측정하고, 테스트의 품질(올바른 검증)은 측정하지 않는다. 80% 커버리지의 의미 있는 테스트가 100% 커버리지의 얕은 테스트보다 낫다. 핵심 비즈니스 로직과 사용자 시나리오에 집중해야 한다.

---

## 참고 자료

- [Vitest 공식 문서](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Testing Library 쿼리 우선순위](https://testing-library.com/docs/queries/about/#priority)
- [jest-dom Matchers](https://github.com/testing-library/jest-dom)
- [Common Mistakes with RTL](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
