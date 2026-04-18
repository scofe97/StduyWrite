# Phase 2: Investigate - React Hook Form 실험

## 실험 과제

아래 코드를 직접 실행하며 동작을 관찰합니다.

### 실험 1: register 반환값 확인

```tsx
// src/experiments/register-test.tsx
import { useForm } from "react-hook-form"

export function RegisterTest() {
  const { register } = useForm()

  // TODO: register가 무엇을 반환하는지 console.log로 확인
  const nameRegister = register("name")
  console.log("register result:", nameRegister)

  return (
    <div>
      <input {...nameRegister} />
      {/* nameRegister의 각 속성이 어떻게 사용되는지 관찰 */}
    </div>
  )
}
```

**관찰할 것**:
- [ ] register가 반환하는 객체의 속성들
- [ ] onChange, onBlur, ref, name 각각의 역할

### 실험 2: Re-render 추적

```tsx
// src/experiments/rerender-test.tsx
import { useForm } from "react-hook-form"

let renderCount = 0

export function RerenderTest() {
  renderCount++
  console.log("Form rendered:", renderCount)

  const { register, handleSubmit, watch } = useForm()

  // watch를 사용하면 어떻게 될까?
  // const watchedName = watch("name")

  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      <input {...register("name")} placeholder="Name" />
      <input {...register("email")} placeholder="Email" />
      <button type="submit">Submit</button>
    </form>
  )
}
```

**관찰할 것**:
- [ ] 입력할 때마다 renderCount가 증가하는가?
- [ ] watch를 활성화하면 어떻게 변하는가?
- [ ] 특정 필드만 watch할 때 vs 전체 watch할 때 차이

### 실험 3: Validation 타이밍

```tsx
// src/experiments/validation-test.tsx
import { useForm } from "react-hook-form"

export function ValidationTest() {
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm({
    mode: "onSubmit"  // 이 옵션을 변경해보세요: onBlur, onChange, all
  })

  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      <input
        {...register("email", {
          required: "필수 입력",
          pattern: {
            value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
            message: "이메일 형식이 아닙니다"
          }
        })}
      />
      {errors.email && <span>{errors.email.message}</span>}
      <button type="submit">Submit</button>
    </form>
  )
}
```

**관찰할 것**:
- [ ] mode가 onSubmit일 때 에러 표시 시점
- [ ] mode가 onChange일 때 에러 표시 시점
- [ ] mode가 onBlur일 때 에러 표시 시점

### 실험 4: Zod와 함께 사용

```tsx
// src/experiments/zod-test.tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

const schema = z.object({
  name: z.string().min(2, "최소 2글자"),
  email: z.string().email("이메일 형식 오류"),
  age: z.number().min(18, "18세 이상만")
})

type FormData = z.infer<typeof schema>

export function ZodTest() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema)
  })

  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      <input {...register("name")} />
      {errors.name && <span>{errors.name.message}</span>}

      <input {...register("email")} />
      {errors.email && <span>{errors.email.message}</span>}

      <input type="number" {...register("age", { valueAsNumber: true })} />
      {errors.age && <span>{errors.age.message}</span>}

      <button type="submit">Submit</button>
    </form>
  )
}
```

**관찰할 것**:
- [ ] Zod 스키마와 TypeScript 타입의 연결
- [ ] valueAsNumber의 역할
- [ ] 복잡한 validation이 어디서 정의되는지

---

## 실험 결과 기록

### 실험 1 결과:

### 실험 2 결과:

### 실험 3 결과:

### 실험 4 결과:
