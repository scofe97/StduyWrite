# Phase 1: Engage - shadcn/ui 패턴 기초

## 준비 질문

### 질문 1: cn() 유틸리티
```tsx
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// 사용 예
<div className={cn(
  "px-4 py-2",
  isActive && "bg-blue-500",
  className
)} />
```

**Q1**: clsx와 tailwind-merge 각각의 역할은?
- `clsx("px-4", false && "hidden")` → ?
- `twMerge("px-4", "px-8")` → ?

### 질문 2: cva (class-variance-authority)
```tsx
import { cva, type VariantProps } from "class-variance-authority"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md font-medium",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground",
        destructive: "bg-destructive text-destructive-foreground",
        outline: "border border-input bg-background",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 px-3",
        lg: "h-11 px-8",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)
```

**Q2**: cva의 장점은 무엇인가요? 일반 조건문 대비?

### 질문 3: Compound Components
```tsx
// Card 컴포넌트
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>Content here</CardContent>
  <CardFooter>Footer</CardFooter>
</Card>
```

**Q3**: 왜 하나의 `<Card title="..." description="...">` 대신
여러 하위 컴포넌트로 분리했을까요?

### 질문 4: asChild 패턴
```tsx
// Slot 사용
<Button asChild>
  <Link href="/dashboard">Dashboard</Link>
</Button>
```

**Q4**: asChild는 어떻게 동작하나요? 왜 필요한가요?

---

## 답변 작성

### A1:

### A2:

### A3:

### A4:
