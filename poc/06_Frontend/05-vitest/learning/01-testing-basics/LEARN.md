# Phase 2: Investigate - Vitest 실험

## 실험 과제

### 실험 1: 기본 테스트 작성

```tsx
// src/__tests__/utils.test.ts
import { describe, it, expect } from "vitest"

// 테스트할 유틸리티 함수
function formatRepositoryName(name: string): string {
  return name.toLowerCase().replace(/\s+/g, "-")
}

function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

describe("formatRepositoryName", () => {
  it("should convert to lowercase", () => {
    expect(formatRepositoryName("MyRepo")).toBe("myrepo")
  })

  it("should replace spaces with hyphens", () => {
    expect(formatRepositoryName("my cool repo")).toBe("my-cool-repo")
  })

  it("should handle multiple spaces", () => {
    expect(formatRepositoryName("my   repo")).toBe("my-repo")
  })
})

describe("isValidEmail", () => {
  it.each([
    ["test@example.com", true],
    ["invalid-email", false],
    ["test@", false],
    ["@example.com", false],
  ])("should validate %s as %s", (email, expected) => {
    expect(isValidEmail(email)).toBe(expected)
  })
})
```

**관찰할 것**:
- [ ] describe로 테스트 그룹화
- [ ] it.each로 파라미터화된 테스트
- [ ] expect의 다양한 매처

### 실험 2: React 컴포넌트 테스트

```tsx
// src/__tests__/Button.test.tsx
import { describe, it, expect, vi } from "vitest"
import { render, screen, fireEvent } from "@testing-library/react"
import { Button } from "@/components/ui/button"

describe("Button", () => {
  it("renders with text", () => {
    render(<Button>Click me</Button>)
    expect(screen.getByRole("button", { name: "Click me" })).toBeInTheDocument()
  })

  it("calls onClick when clicked", () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click</Button>)

    fireEvent.click(screen.getByRole("button"))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it("is disabled when disabled prop is true", () => {
    render(<Button disabled>Disabled</Button>)
    expect(screen.getByRole("button")).toBeDisabled()
  })

  it("applies variant classes", () => {
    render(<Button variant="destructive">Delete</Button>)
    const button = screen.getByRole("button")
    // 클래스 이름 확인 또는 스타일 확인
    expect(button).toHaveClass("bg-destructive")
  })
})
```

**관찰할 것**:
- [ ] render와 screen의 역할
- [ ] getByRole vs getByText vs getByTestId
- [ ] vi.fn()으로 함수 모킹

### 실험 3: 비동기 테스트

```tsx
// src/__tests__/async.test.tsx
import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen, waitFor } from "@testing-library/react"
import { QueryClient, QueryClientProvider, useQuery } from "@tanstack/react-query"

// 테스트할 컴포넌트
function UserProfile({ userId }: { userId: string }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ["user", userId],
    queryFn: () => fetchUser(userId),
  })

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  return <div>Hello, {data?.name}</div>
}

// API 함수 (모킹 대상)
async function fetchUser(id: string) {
  const res = await fetch(`/api/users/${id}`)
  return res.json()
}

// 테스트 래퍼
function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  })
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  )
}

describe("UserProfile", () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it("shows loading state initially", () => {
    vi.spyOn(global, "fetch").mockImplementation(() =>
      new Promise(() => {})  // 영원히 pending
    )

    render(<UserProfile userId="1" />, { wrapper: createWrapper() })
    expect(screen.getByText("Loading...")).toBeInTheDocument()
  })

  it("shows user data after loading", async () => {
    vi.spyOn(global, "fetch").mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ id: "1", name: "Kim" }),
    } as Response)

    render(<UserProfile userId="1" />, { wrapper: createWrapper() })

    await waitFor(() => {
      expect(screen.getByText("Hello, Kim")).toBeInTheDocument()
    })
  })

  it("shows error when fetch fails", async () => {
    vi.spyOn(global, "fetch").mockRejectedValue(new Error("Network error"))

    render(<UserProfile userId="1" />, { wrapper: createWrapper() })

    await waitFor(() => {
      expect(screen.getByText(/Error:/)).toBeInTheDocument()
    })
  })
})
```

**관찰할 것**:
- [ ] waitFor로 비동기 상태 변화 대기
- [ ] vi.spyOn으로 전역 함수 모킹
- [ ] QueryClient 래퍼 설정

### 실험 4: 스냅샷 테스트

```tsx
// src/__tests__/snapshot.test.tsx
import { describe, it, expect } from "vitest"
import { render } from "@testing-library/react"
import { Badge } from "@/components/ui/badge"

describe("Badge snapshots", () => {
  it("renders default badge", () => {
    const { container } = render(<Badge>Default</Badge>)
    expect(container).toMatchSnapshot()
  })

  it("renders github variant", () => {
    const { container } = render(<Badge variant="github">GitHub</Badge>)
    expect(container).toMatchSnapshot()
  })
})
```

**관찰할 것**:
- [ ] __snapshots__ 폴더 생성
- [ ] 스냅샷 파일 내용
- [ ] 스냅샷 업데이트 방법 (vitest -u)

---

## 실험 결과 기록

### 실험 1 결과:

### 실험 2 결과:

### 실험 3 결과:

### 실험 4 결과:
