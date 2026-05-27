# Phase 1: Engage - React Hook Form 기초

## 준비 질문

아래 질문에 답변하면서 React Hook Form의 핵심 개념을 탐구합니다.

### 질문 1: 폼 상태 관리의 문제점
```tsx
// 전통적인 React 폼 관리
function TraditionalForm() {
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [errors, setErrors] = useState({})

  return (
    <form>
      <input value={name} onChange={(e) => setName(e.target.value)} />
      <input value={email} onChange={(e) => setEmail(e.target.value)} />
      <input value={password} onChange={(e) => setPassword(e.target.value)} />
    </form>
  )
}
```

**Q1**: 이 방식의 문제점은 무엇인가요? 필드가 10개, 100개로 늘어나면?

### 질문 2: Controlled vs Uncontrolled
```tsx
// Controlled
<input value={value} onChange={(e) => setValue(e.target.value)} />

// Uncontrolled
<input ref={inputRef} defaultValue="initial" />
```

**Q2**: React Hook Form은 어떤 방식을 사용할까요? 왜 그런 선택을 했을까요?

### 질문 3: Re-render 최소화
```tsx
// React Hook Form 기본 사용
const { register, handleSubmit, watch } = useForm()

const onSubmit = (data) => console.log(data)

return (
  <form onSubmit={handleSubmit(onSubmit)}>
    <input {...register("name")} />
    <input {...register("email")} />
    <button type="submit">Submit</button>
  </form>
)
```

**Q3**: `register`가 반환하는 것은 무엇인가요? input에 어떻게 연결되나요?

### 질문 4: Validation
```tsx
<input
  {...register("email", {
    required: "이메일은 필수입니다",
    pattern: {
      value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
      message: "유효하지 않은 이메일입니다"
    }
  })}
/>
```

**Q4**: validation이 언제 실행되나요? submit 시점? 입력 시점? 둘 다?

---

## 답변 작성

위 질문들에 대한 답변을 여기에 작성하세요:

### A1:


### A2:


### A3:


### A4:

