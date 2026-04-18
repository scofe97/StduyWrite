/**
 * Button 컴포넌트 - 디자인 패턴 실습
 *
 * ===== 학습할 패턴 =====
 *
 * 1. cva() Variants 패턴
 *    - 타입 안전한 스타일 변형 관리
 *    - defaultVariants로 기본값 설정
 *    - VariantProps로 타입 추출
 *
 * 2. forwardRef 패턴
 *    - 부모에서 자식 DOM에 접근 가능
 *    - ref를 props로 전달
 *    - displayName 설정
 *
 * 3. cn() 유틸리티 패턴
 *    - 조건부 클래스 병합
 *    - Tailwind 클래스 충돌 해결
 *    - 외부 className 우선 적용
 *
 * 4. Polymorphic Component 패턴 (asChild 대체)
 *    - 렌더링 요소를 유연하게 변경
 *    - Link, a 태그 등으로 대체 가능
 *
 * 참고: 02-button-input.md
 */

import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

// ===== 패턴 1: cva() Variants 정의 =====
// TODO: 아래 스타일을 직접 채워보세요
const buttonVariants = cva(
  // 기본 스타일 (모든 버튼에 공통)
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        // TODO: 각 variant별 스타일 정의
        default: "bg-primary text-primary-foreground shadow hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
        outline: "border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        // TODO: 각 size별 스타일 정의
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 rounded-md px-8",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

// ===== 패턴 2: Props 타입 정의 =====
// VariantProps로 cva의 variant 타입을 자동 추출
export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  // Polymorphic 패턴용 (선택적)
  as?: React.ElementType
}

// ===== 패턴 3: forwardRef 컴포넌트 =====
const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, as: Component = "button", ...props }, ref) => {
    return (
      <Component
        // cn()으로 variants + 외부 className 병합
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
// DevTools에서 컴포넌트 이름 표시
Button.displayName = "Button"

export { Button, buttonVariants }
