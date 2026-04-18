# Phase 1: Engage - Vitest 기초

## 준비 질문

### 질문 1: 테스트의 종류
```
유닛 테스트: 개별 함수/컴포넌트
통합 테스트: 여러 컴포넌트 상호작용
E2E 테스트: 실제 브라우저에서 전체 플로우
```

**Q1**: React 컴포넌트는 어떤 종류의 테스트가 적합한가요?

### 질문 2: Vitest vs Jest
```tsx
// Vitest
import { describe, it, expect, vi } from "vitest"

// Jest
import { describe, it, expect, jest } from "@jest/globals"
```

**Q2**: Vitest가 Jest보다 빠른 이유는?

### 질문 3: Testing Library 철학
```tsx
// 구현 세부사항 테스트 (나쁜 예)
expect(component.state.isOpen).toBe(true)

// 사용자 관점 테스트 (좋은 예)
expect(screen.getByRole("dialog")).toBeVisible()
```

**Q3**: "구현이 아닌 동작을 테스트하라"의 의미는?

### 질문 4: Mock의 사용
```tsx
// API 모킹
vi.mock("@/api/repositories", () => ({
  fetchRepositories: vi.fn(() => Promise.resolve([]))
}))

// 시간 모킹
vi.useFakeTimers()
vi.advanceTimersByTime(1000)
```

**Q4**: 테스트에서 Mock을 사용하는 이유는?

---

## 답변 작성

### A1:

### A2:

### A3:

### A4:
