# Phase 2: Investigate - shadcn/ui 패턴 실험

## 실험 과제

### 실험 1: cn() 유틸리티 동작

```tsx
// src/experiments/cn-test.tsx
import { cn } from "@/lib/utils"

export function CnTest() {
  const isActive = true
  const isDisabled = false

  // 각각의 결과를 console.log로 확인
  console.log("Test 1:", cn("px-4", "py-2"))
  console.log("Test 2:", cn("px-4", false && "hidden"))
  console.log("Test 3:", cn("px-4 text-red-500", "px-8"))  // tailwind-merge 효과
  console.log("Test 4:", cn("px-4", isActive && "bg-blue-500", isDisabled && "opacity-50"))

  return (
    <div>
      <div className={cn("px-4", "py-2", "bg-gray-100")}>Test 1</div>
      <div className={cn("px-4 bg-red-500", "bg-blue-500")}>
        Test 2: Which background wins?
      </div>
    </div>
  )
}
```

**관찰할 것**:
- [ ] clsx가 조건부 클래스를 어떻게 처리하는지
- [ ] tailwind-merge가 충돌을 어떻게 해결하는지
- [ ] bg-red-500과 bg-blue-500 중 어떤 것이 적용되는지

### 실험 2: cva 변형 만들기

```tsx
// src/experiments/cva-test.tsx
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const badgeVariants = cva(
  // 기본 스타일
  "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground",
        secondary: "bg-secondary text-secondary-foreground",
        success: "bg-green-500 text-white",
        warning: "bg-yellow-500 text-black",
        error: "bg-red-500 text-white",
      },
      size: {
        sm: "text-xs px-2 py-0.5",
        md: "text-sm px-2.5 py-0.5",
        lg: "text-base px-3 py-1",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "md",
    },
  }
)

interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, size, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant, size }), className)} {...props} />
  )
}

export function CvaTest() {
  return (
    <div className="flex gap-2 flex-wrap">
      <Badge>Default</Badge>
      <Badge variant="success">Success</Badge>
      <Badge variant="error" size="lg">Large Error</Badge>
      <Badge variant="warning" className="animate-pulse">Custom Class</Badge>
    </div>
  )
}
```

**관찰할 것**:
- [ ] 각 variant 조합의 결과 클래스
- [ ] VariantProps 타입이 어떻게 자동 생성되는지
- [ ] className prop이 기존 스타일을 덮어쓰는지

### 실험 3: Compound Components 구현

```tsx
// src/experiments/compound-test.tsx
import * as React from "react"
import { cn } from "@/lib/utils"

// Context for sharing state
const AlertContext = React.createContext<{
  variant: "default" | "destructive"
}>({ variant: "default" })

// Root component
function Alert({
  children,
  variant = "default",
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement> & { variant?: "default" | "destructive" }) {
  return (
    <AlertContext.Provider value={{ variant }}>
      <div
        role="alert"
        className={cn(
          "relative w-full rounded-lg border p-4",
          variant === "destructive" && "border-destructive/50 text-destructive",
          className
        )}
        {...props}
      >
        {children}
      </div>
    </AlertContext.Provider>
  )
}

function AlertTitle({
  className,
  ...props
}: React.HTMLAttributes<HTMLHeadingElement>) {
  return (
    <h5
      className={cn("mb-1 font-medium leading-none tracking-tight", className)}
      {...props}
    />
  )
}

function AlertDescription({
  className,
  ...props
}: React.HTMLAttributes<HTMLParagraphElement>) {
  return (
    <div className={cn("text-sm [&_p]:leading-relaxed", className)} {...props} />
  )
}

export function CompoundTest() {
  return (
    <div className="space-y-4">
      <Alert>
        <AlertTitle>Default Alert</AlertTitle>
        <AlertDescription>This is a default alert message.</AlertDescription>
      </Alert>

      <Alert variant="destructive">
        <AlertTitle>Error!</AlertTitle>
        <AlertDescription>Something went wrong.</AlertDescription>
      </Alert>
    </div>
  )
}
```

**관찰할 것**:
- [ ] Context를 통한 부모-자식 상태 공유
- [ ] 각 하위 컴포넌트의 독립성
- [ ] 유연한 조합 가능성

### 실험 4: asChild 패턴

```tsx
// src/experiments/as-child-test.tsx
import { Slot } from "@radix-ui/react-slot"
import { cn } from "@/lib/utils"

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  asChild?: boolean
  variant?: "default" | "link"
}

function Button({ className, asChild, variant = "default", ...props }: ButtonProps) {
  const Comp = asChild ? Slot : "button"

  return (
    <Comp
      className={cn(
        "inline-flex items-center justify-center rounded-md px-4 py-2",
        variant === "default" && "bg-primary text-primary-foreground",
        variant === "link" && "text-primary underline-offset-4 hover:underline",
        className
      )}
      {...props}
    />
  )
}

export function AsChildTest() {
  return (
    <div className="space-y-4">
      {/* 일반 버튼 */}
      <Button onClick={() => alert("clicked!")}>Regular Button</Button>

      {/* asChild로 Link 컴포넌트처럼 사용 */}
      <Button asChild>
        <a href="https://google.com" target="_blank">
          Link styled as Button
        </a>
      </Button>

      {/* asChild로 다른 컴포넌트 래핑 */}
      <Button asChild variant="link">
        <span>Span styled as Button</span>
      </Button>
    </div>
  )
}
```

**관찰할 것**:
- [ ] asChild가 true일 때 렌더링되는 요소
- [ ] Slot이 props를 자식에게 어떻게 전달하는지
- [ ] 접근성과 시맨틱 HTML 유지

---

## 실험 결과 기록

### 실험 1 결과:

### 실험 2 결과:

### 실험 3 결과:

### 실험 4 결과:
