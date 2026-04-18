import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

/**
 * cn() - shadcn/ui 핵심 유틸리티
 *
 * clsx: 조건부 클래스 문자열 생성
 * tailwind-merge: Tailwind 클래스 충돌 해결
 *
 * @example
 * cn("px-4 py-2", "bg-blue-500")
 * // → "px-4 py-2 bg-blue-500"
 *
 * cn("px-4", isActive && "bg-primary")
 * // isActive가 true면 → "px-4 bg-primary"
 *
 * cn("px-4", "px-6")
 * // → "px-6" (나중 값이 우선)
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
