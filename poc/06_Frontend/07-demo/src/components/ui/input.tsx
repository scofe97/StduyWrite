/**
 * Input 컴포넌트 - 디자인 패턴 실습
 *
 * ===== 학습할 패턴 =====
 *
 * 1. forwardRef 패턴
 *    - Form 라이브러리(React Hook Form 등)와 호환
 *    - 부모에서 focus, value 접근 가능
 *
 * 2. cn() 유틸리티 패턴
 *    - 기본 스타일 + 외부 className 병합
 *    - 외부에서 스타일 오버라이드 가능
 *
 * 3. Props 확장 패턴
 *    - HTML 네이티브 속성 그대로 상속
 *    - 추가 props만 정의
 *
 * 참고: 02-button-input.md
 */

import * as React from "react"
import { cn } from "@/lib/utils"

// ===== 패턴: Props 확장 =====
// InputHTMLAttributes를 상속받아 모든 input 속성 사용 가능
export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  // 필요시 추가 props 정의
  // error?: boolean
  // leftIcon?: React.ReactNode
}

// ===== 패턴: forwardRef 컴포넌트 =====
const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          // 레이아웃
          "flex h-9 w-full",
          // 모양
          "rounded-md border border-input bg-transparent",
          // 패딩
          "px-3 py-1",
          // 텍스트 (모바일: 16px 확대방지, 데스크탑: 14px)
          "text-base md:text-sm",
          // 그림자 & 트랜지션
          "shadow-sm transition-colors",
          // placeholder
          "placeholder:text-muted-foreground",
          // 포커스 상태
          "focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring",
          // 비활성화 상태
          "disabled:cursor-not-allowed disabled:opacity-50",
          // 파일 입력 스타일
          "file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground",
          // 외부 className (우선 적용)
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Input.displayName = "Input"

export { Input }
