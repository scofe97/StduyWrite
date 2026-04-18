/**
 * Modal 컴포넌트 - Compound Component 패턴 실습
 *
 * ===== 학습할 패턴 =====
 *
 * 1. Compound Component 패턴
 *    - 부모-자식 컴포넌트가 암묵적으로 상태 공유
 *    - JSX 구조가 UI 구조를 반영
 *    - 각 부분을 독립적으로 커스터마이징 가능
 *
 * 2. Context API 패턴
 *    - createContext로 상태 컨텍스트 생성
 *    - Provider로 상태 전달
 *    - useContext로 상태 소비
 *
 * 3. Static Property 패턴
 *    - Modal.Header, Modal.Content 형태로 접근
 *    - 관련 컴포넌트를 네임스페이스로 그룹화
 *
 * 사용 예시:
 * <Modal open={isOpen} onOpenChange={setIsOpen}>
 *   <Modal.Trigger>
 *     <Button>Open Modal</Button>
 *   </Modal.Trigger>
 *   <Modal.Content>
 *     <Modal.Header>
 *       <Modal.Title>제목</Modal.Title>
 *     </Modal.Header>
 *     <Modal.Body>내용</Modal.Body>
 *     <Modal.Footer>
 *       <Button>확인</Button>
 *     </Modal.Footer>
 *   </Modal.Content>
 * </Modal>
 *
 * 참고: 01-core-patterns.md (Composition 패턴)
 */

import * as React from "react"
import { createContext, useContext, useState } from "react"
import { cn } from "@/lib/utils"

// ===== 패턴 1: Context 정의 =====
type ModalContextType = {
  open: boolean
  onOpenChange: (open: boolean) => void
}

const ModalContext = createContext<ModalContextType | null>(null)

// Context 사용 Hook
function useModalContext() {
  const context = useContext(ModalContext)
  if (!context) {
    throw new Error("Modal 컴포넌트 내부에서만 사용할 수 있습니다.")
  }
  return context
}

// ===== 패턴 2: Root 컴포넌트 (Provider) =====
interface ModalProps {
  children: React.ReactNode
  open?: boolean
  onOpenChange?: (open: boolean) => void
  defaultOpen?: boolean
}

function ModalRoot({
  children,
  open: controlledOpen,
  onOpenChange: controlledOnOpenChange,
  defaultOpen = false,
}: ModalProps) {
  // Controlled vs Uncontrolled 패턴
  const [uncontrolledOpen, setUncontrolledOpen] = useState(defaultOpen)

  const isControlled = controlledOpen !== undefined
  const open = isControlled ? controlledOpen : uncontrolledOpen
  const onOpenChange = isControlled
    ? controlledOnOpenChange!
    : setUncontrolledOpen

  return (
    <ModalContext.Provider value={{ open, onOpenChange }}>
      {children}
    </ModalContext.Provider>
  )
}

// ===== 패턴 3: Trigger 컴포넌트 =====
interface ModalTriggerProps {
  children: React.ReactNode
  className?: string
}

function ModalTrigger({ children, className }: ModalTriggerProps) {
  const { onOpenChange } = useModalContext()

  return (
    <div
      className={cn("inline-block cursor-pointer", className)}
      onClick={() => onOpenChange(true)}
    >
      {children}
    </div>
  )
}

// ===== 패턴 4: Content 컴포넌트 (Portal + Overlay) =====
interface ModalContentProps {
  children: React.ReactNode
  className?: string
}

function ModalContent({ children, className }: ModalContentProps) {
  const { open, onOpenChange } = useModalContext()

  if (!open) return null

  return (
    // Overlay
    <div
      className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center"
      onClick={() => onOpenChange(false)}
    >
      {/* Content */}
      <div
        className={cn(
          "relative bg-background rounded-lg shadow-lg",
          "w-full max-w-md mx-4 p-6",
          "animate-in fade-in-0 zoom-in-95",
          className
        )}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <button
          className="absolute right-4 top-4 opacity-70 hover:opacity-100"
          onClick={() => onOpenChange(false)}
        >
          ✕
        </button>
        {children}
      </div>
    </div>
  )
}

// ===== 패턴 5: 하위 컴포넌트들 =====
interface ModalPartProps {
  children: React.ReactNode
  className?: string
}

function ModalHeader({ children, className }: ModalPartProps) {
  return (
    <div className={cn("mb-4", className)}>
      {children}
    </div>
  )
}

function ModalTitle({ children, className }: ModalPartProps) {
  return (
    <h2 className={cn("text-lg font-semibold", className)}>
      {children}
    </h2>
  )
}

function ModalDescription({ children, className }: ModalPartProps) {
  return (
    <p className={cn("text-sm text-muted-foreground", className)}>
      {children}
    </p>
  )
}

function ModalBody({ children, className }: ModalPartProps) {
  return (
    <div className={cn("py-4", className)}>
      {children}
    </div>
  )
}

function ModalFooter({ children, className }: ModalPartProps) {
  return (
    <div className={cn("mt-4 flex justify-end gap-2", className)}>
      {children}
    </div>
  )
}

// ===== 패턴 6: Static Property로 Export =====
const Modal = Object.assign(ModalRoot, {
  Trigger: ModalTrigger,
  Content: ModalContent,
  Header: ModalHeader,
  Title: ModalTitle,
  Description: ModalDescription,
  Body: ModalBody,
  Footer: ModalFooter,
})

export { Modal, useModalContext }
