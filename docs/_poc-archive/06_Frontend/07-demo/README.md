# React Demo - 디자인 패턴 실습 프로젝트

> **레퍼런스 프로젝트** (학습 모듈 아님) — shadcn/ui 패턴을 실제 동작하는 코드로 확인하는 용도

shadcn/ui의 네이티브 코드에서 추출한 **디자인 패턴**과 **컴포넌트 설계 규칙**을 학습하기 위한 프로젝트입니다.

## 관련 이론

- [reference/06-ui-development/shadcn-ui/](../reference/06-ui-development/shadcn-ui/): shadcn/ui 컴포넌트 가이드

## 설치 및 실행

```bash
# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

---

## 학습할 디자인 패턴

> 총 **14개**의 핵심 패턴을 다룹니다.

| 구분 | 패턴 |
|------|------|
| **기초 패턴** | 1. cn() 유틸리티, 2. cva() Variants, 3. forwardRef, 6. Props 확장 |
| **합성 패턴** | 4. Compound Component, 5. Polymorphic, 7. asChild/Slot |
| **스타일링 패턴** | 8. Data Attributes, 12. Animation, 14. CSS Variables Theme |
| **상태 관리 패턴** | 10. Responsive Component, 11. Controlled/Uncontrolled |
| **고급 패턴** | 9. Portal, 13. Accessibility |

---

### 1. cn() 유틸리티 패턴
**파일**: `src/lib/utils.ts`

```tsx
// clsx + tailwind-merge 조합
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

**핵심 개념**:
- 조건부 클래스 병합
- Tailwind 클래스 충돌 해결 (px-4 + px-6 → px-6)
- 외부 className을 마지막에 배치하여 우선 적용

---

### 2. cva() Variants 패턴
**파일**: `src/components/ui/button.tsx`

```tsx
const buttonVariants = cva(
  "기본 스타일",
  {
    variants: {
      variant: { default: "...", destructive: "..." },
      size: { sm: "...", md: "...", lg: "..." },
    },
    defaultVariants: { variant: "default", size: "md" },
  }
)
```

**핵심 개념**:
- 타입 안전한 스타일 변형 관리
- `VariantProps<typeof buttonVariants>`로 타입 자동 추출
- `defaultVariants`로 기본값 설정

---

### 3. forwardRef 패턴
**파일**: `src/components/ui/input.tsx`

```tsx
const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, ...props }, ref) => {
    return <input ref={ref} {...props} />
  }
)
Input.displayName = "Input"
```

**핵심 개념**:
- 부모에서 자식 DOM 요소에 접근 가능
- React Hook Form 등 외부 라이브러리와 호환
- `displayName` 설정으로 DevTools 디버깅 지원

---

### 4. Compound Component 패턴
**파일**: `src/components/patterns/modal.tsx`

```tsx
<Modal open={isOpen} onOpenChange={setIsOpen}>
  <Modal.Trigger>
    <Button>Open</Button>
  </Modal.Trigger>
  <Modal.Content>
    <Modal.Header>
      <Modal.Title>제목</Modal.Title>
    </Modal.Header>
    <Modal.Body>내용</Modal.Body>
    <Modal.Footer>
      <Button>확인</Button>
    </Modal.Footer>
  </Modal.Content>
</Modal>
```

**핵심 개념**:
- Context API로 부모-자식 간 암묵적 상태 공유
- JSX 구조가 UI 구조를 반영 (가독성)
- Static Property 패턴 (`Modal.Header`, `Modal.Content`)
- Controlled vs Uncontrolled 컴포넌트 지원

---

### 5. Polymorphic Component 패턴
**파일**: `src/components/ui/button.tsx`

```tsx
interface ButtonProps {
  as?: React.ElementType  // 렌더링할 요소 타입
}

const Button = forwardRef(({ as: Component = "button", ...props }, ref) => {
  return <Component ref={ref} {...props} />
})
```

**핵심 개념**:
- `as` prop으로 렌더링 요소 변경 가능
- shadcn의 `asChild` 패턴을 라이브러리 없이 구현
- Link, a 태그 등으로 유연하게 변경

---

### 6. Props 확장 패턴
**파일**: `src/components/ui/input.tsx`

```tsx
interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  // 추가 props만 정의
}
```

**핵심 개념**:
- HTML 네이티브 속성 그대로 상속
- 추가 props만 명시적으로 정의
- 스프레드 연산자로 모든 속성 전달

---

### 7. asChild / Slot 패턴
**파일**: `src/components/ui/button.tsx`

Radix UI의 핵심 패턴으로, 컴포넌트의 스타일을 유지하면서 렌더링 요소를 완전히 교체합니다.

```tsx
import { Slot } from "@radix-ui/react-slot"

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return <Comp ref={ref} {...props} />
  }
)

// 사용 예시: Button 스타일을 유지하면서 Link로 렌더링
<Button asChild>
  <Link href="/login">Login</Link>
</Button>
```

**핵심 개념**:
- 자식 컴포넌트가 부모의 props와 스타일을 상속
- Polymorphic보다 더 유연한 컴포넌트 합성
- `@radix-ui/react-slot` 기반

---

### 8. Data Attributes 스타일링 패턴
**파일**: `src/components/ui/sheet.tsx`

`data-state`, `data-selected` 등 데이터 속성으로 상태 기반 스타일링

```tsx
<SheetPrimitive.Overlay
  className={cn(
    "data-[state=open]:animate-in data-[state=closed]:animate-out",
    "data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0"
  )}
/>

// Calendar 예시
<Button
  data-selected-single={modifiers.selected}
  data-range-start={modifiers.range_start}
  className="data-[selected-single=true]:bg-primary"
/>
```

**핵심 개념**:
- CSS에서 `data-[state=open]:` 선택자 사용
- JavaScript 상태와 CSS 스타일 분리
- Tailwind의 arbitrary variants와 조합

---

### 9. Portal 패턴
**파일**: `src/components/ui/dialog.tsx`, `src/components/ui/sheet.tsx`

모달, 드롭다운 등을 DOM 계층 밖에 렌더링

```tsx
import * as DialogPrimitive from "@radix-ui/react-dialog"

const DialogPortal = DialogPrimitive.Portal

const DialogContent = forwardRef((props, ref) => (
  <DialogPortal>
    <DialogOverlay />
    <DialogPrimitive.Content ref={ref} {...props}>
      {children}
    </DialogPrimitive.Content>
  </DialogPortal>
))
```

**핵심 개념**:
- z-index 충돌 방지
- 부모의 `overflow: hidden` 영향 회피
- 접근성 포커스 트래핑

---

### 10. Responsive Component 패턴
**파일**: `src/components/patterns/responsive-modal.tsx`

화면 크기에 따라 다른 컴포넌트 렌더링

```tsx
import { useMediaQuery } from "@/hooks/use-media-query"

export function ResponsiveModal({ open, onOpenChange, children }) {
  const isDesktop = useMediaQuery("(min-width: 768px)")

  if (isDesktop) {
    return (
      <Dialog open={open} onOpenChange={onOpenChange}>
        <DialogContent>{children}</DialogContent>
      </Dialog>
    )
  }

  return (
    <Drawer open={open} onOpenChange={onOpenChange}>
      <DrawerContent>{children}</DrawerContent>
    </Drawer>
  )
}
```

**핵심 개념**:
- `useMediaQuery` 커스텀 훅
- Desktop: Dialog, Mobile: Drawer 전환
- 동일 API로 반응형 UX 제공

---

### 11. Controlled/Uncontrolled 패턴
**파일**: `src/components/ui/dialog.tsx`

외부 상태 관리 vs 내부 상태 관리 선택권

```tsx
// Controlled: 외부에서 상태 관리
const [open, setOpen] = useState(false)
<Dialog open={open} onOpenChange={setOpen}>
  <DialogTrigger>Open</DialogTrigger>
  <DialogContent>...</DialogContent>
</Dialog>

// Uncontrolled: 내부에서 상태 관리 (open prop 생략)
<Dialog>
  <DialogTrigger>Open</DialogTrigger>
  <DialogContent>...</DialogContent>
</Dialog>
```

**핵심 개념**:
- `open`, `onOpenChange` props 조합
- 두 방식 모두 지원하는 유연한 API
- React Hook Form과 통합 용이

---

### 12. Animation with data-state 패턴
**파일**: `src/components/ui/sheet.tsx`

CSS 애니메이션과 상태 속성 조합

```tsx
const sheetVariants = cva(
  "fixed z-50 transition ease-in-out",
  {
    variants: {
      side: {
        right: cn(
          "inset-y-0 right-0 h-full w-3/4 border-l",
          "data-[state=open]:animate-in data-[state=open]:slide-in-from-right",
          "data-[state=closed]:animate-out data-[state=closed]:slide-out-to-right",
          "data-[state=open]:duration-500 data-[state=closed]:duration-300"
        ),
        // left, top, bottom 등...
      },
    },
  }
)
```

**핵심 개념**:
- `tailwindcss-animate` 플러그인 활용
- 열림/닫힘 각각 다른 애니메이션 시간
- 방향별 슬라이드 효과

---

### 13. Accessibility (a11y) 패턴
**파일**: `src/components/ui/combobox.tsx`

접근성 속성 및 키보드 네비게이션

```tsx
<Button
  role="combobox"
  aria-expanded={open}
  aria-haspopup="listbox"
  className="w-[200px] justify-between"
>
  {value ? selectedLabel : "Select..."}
  <ChevronsUpDown className="opacity-50" />
</Button>

// 스크린 리더 전용 텍스트
<SheetPrimitive.Close>
  <X className="h-4 w-4" />
  <span className="sr-only">Close</span>
</SheetPrimitive.Close>
```

**핵심 개념**:
- ARIA 속성 (`role`, `aria-expanded`, `aria-selected`)
- 키보드 네비게이션 (Tab, Enter, Escape)
- 포커스 관리 및 포커스 트래핑
- `sr-only` 클래스로 스크린 리더 지원

---

### 14. CSS Variables Theme 패턴
**파일**: `src/styles/globals.css`

CSS 변수 기반 테마 시스템

```css
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;
  --muted: 210 40% 96.1%;
  --muted-foreground: 215.4 16.3% 46.9%;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  --primary: 210 40% 98%;
  --primary-foreground: 222.2 47.4% 11.2%;
}
```

```tsx
// Tailwind에서 CSS 변수 사용
<div className="bg-background text-foreground">
  <Button className="bg-primary text-primary-foreground">
    Click me
  </Button>
</div>
```

**핵심 개념**:
- HSL 색상 값으로 유연한 테마
- `bg-background`, `text-foreground` 시맨틱 클래스
- 다크모드 자동 전환
- `tailwind.config.js`에서 CSS 변수 매핑

---

## 프로젝트 구조

```
src/
├── components/
│   ├── ui/              # 기본 UI 컴포넌트
│   │   ├── button.tsx   # cva, asChild, forwardRef
│   │   ├── input.tsx    # Props 확장, forwardRef
│   │   ├── dialog.tsx   # Portal, Controlled/Uncontrolled
│   │   ├── sheet.tsx    # Data Attributes, Animation
│   │   └── combobox.tsx # Accessibility
│   ├── patterns/        # 디자인 패턴 예제
│   │   ├── modal.tsx           # Compound Component
│   │   └── responsive-modal.tsx # Responsive Component
│   └── theme-provider.tsx
├── hooks/               # 커스텀 훅
│   └── use-media-query.ts  # Responsive 패턴용
├── lib/
│   └── utils.ts         # cn() 유틸리티
├── pages/               # 페이지 컴포넌트 (실습용)
├── styles/
│   └── globals.css      # CSS Variables Theme
├── types/               # TypeScript 타입 정의
└── utils/               # 유틸리티 함수
```

---

## TPS 프로젝트 참고 포인트

| shadcn/ui 패턴 | 난이도 | TPS 적용 가능성 | 우선순위 |
|---------------|--------|----------------|----------|
| cn() 유틸리티 | ⭐ | ✅ 즉시 적용 가능 | 1순위 |
| cva() variants | ⭐⭐ | ✅ 신규 컴포넌트에 적용 | 1순위 |
| forwardRef | ⭐ | ✅ 기존 컴포넌트 점검 | 1순위 |
| Props 확장 패턴 | ⭐ | ✅ 즉시 적용 가능 | 1순위 |
| asChild/Slot | ⭐⭐ | ✅ Button + Link 조합 | 1순위 |
| Data Attributes 스타일링 | ⭐ | ✅ 상태 기반 스타일링 | 1순위 |
| Controlled/Uncontrolled | ⭐ | ✅ Form 컴포넌트 필수 | 1순위 |
| CSS Variables Theme | ⭐⭐ | ✅ 테마 시스템 구축 | 2순위 |
| Animation 패턴 | ⭐⭐ | ⚠️ 선택적 적용 | 2순위 |
| Compound Component | ⭐⭐⭐ | ⚠️ Modal, Dropdown 리팩토링 시 | 2순위 |
| Polymorphic Component | ⭐⭐ | ⚠️ 복잡한 조합 필요 시 | 3순위 |
| Portal 패턴 | ⭐⭐⭐ | ⚠️ Modal 리팩토링 시 | 3순위 |
| Responsive Component | ⭐⭐ | ⚠️ 반응형 UI 필요 시 | 3순위 |
| Accessibility | ⭐⭐⭐ | ✅ 점진적 적용 | 3순위 |

---

## 실습 순서

1. **Phase 1**: Button, Input 컴포넌트 직접 구현 (cn, cva, forwardRef)
2. **Phase 2**: asChild/Slot 패턴과 Data Attributes 스타일링
3. **Phase 3**: Modal Compound Component 이해
4. **Phase 4**: Controlled/Uncontrolled 패턴 적용
5. **Phase 5**: CSS Variables Theme 시스템 구축
6. **Phase 6**: Animation 패턴 및 접근성 개선
7. **Phase 7**: TPS 패턴과 비교 분석

---

## 참고 문서

- `docs/shadcn document/01-core-patterns.md` - 핵심 패턴
- `docs/shadcn document/02-button-input.md` - Button/Input 분석
- `docs/shadcn document/08-tps-application.md` - TPS 적용 전략
