# Phase 4: Extend - Repository 생성 폼 구현

## 구현 과제

학습한 내용을 바탕으로 Repository 생성 폼을 구현합니다.

### 요구사항

1. **필드 목록**:
   - `name`: 필수, 2-100자, 영문/숫자/하이픈만
   - `description`: 선택, 최대 500자
   - `provider`: 필수, github | gitlab | bitbucket
   - `visibility`: 필수, public | private

2. **UX 요구사항**:
   - 실시간 validation (onChange)
   - Submit 버튼은 유효한 상태에서만 활성화
   - 에러 메시지는 필드 아래에 표시

3. **기술 요구사항**:
   - Zod resolver 사용
   - shadcn/ui 컴포넌트 사용
   - TypeScript strict 모드

### 구현 템플릿

```tsx
// src/features/repository/components/RepositoryForm.tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
// TODO: Select, Textarea 등 추가

// TODO: Zod 스키마 정의
const repositorySchema = z.object({
  // ...
})

type RepositoryFormData = z.infer<typeof repositorySchema>

interface RepositoryFormProps {
  onSubmit: (data: RepositoryFormData) => void
  defaultValues?: Partial<RepositoryFormData>
}

export function RepositoryForm({ onSubmit, defaultValues }: RepositoryFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors, isValid }
  } = useForm<RepositoryFormData>({
    resolver: zodResolver(repositorySchema),
    mode: "onChange",
    defaultValues
  })

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* TODO: 폼 필드 구현 */}
    </form>
  )
}
```

### 체크리스트

- [ ] Zod 스키마 정의 완료
- [ ] 모든 필드 구현
- [ ] validation 에러 표시
- [ ] Submit 버튼 비활성화 로직
- [ ] 기본값 지원 (수정 모드용)
- [ ] 타입 안정성 확인

---

## 구현 결과

### 완성된 코드:

### 어려웠던 점:

### 추가 학습이 필요한 부분:
