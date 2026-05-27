# Phase 1: Engage - TanStack Query 기초
## 준비 질문

### 질문 1: 서버 상태 vs 클라이언트 상태
```tsx
// 클라이언트 상태 (UI 상태)
const [isModalOpen, setIsModalOpen] = useState(false)
const [selectedTab, setSelectedTab] = useState("home")

// 서버 상태 (원격 데이터)
const [repositories, setRepositories] = useState([])
const [isLoading, setIsLoading] = useState(false)
const [error, setError] = useState(null)

useEffect(() => {
  setIsLoading(true)
  fetchRepositories()
    .then(data => setRepositories(data))
    .catch(err => setError(err))
    .finally(() => setIsLoading(false))
}, [])
```

**Q1**: 서버 상태를 useState로 관리할 때 어떤 문제가 생기나요?
- 캐싱? 중복 요청? 동기화? 재시도?

### 질문 2: useQuery의 기본 동작
```tsx
const { data, isLoading, error } = useQuery({
  queryKey: ["repositories"],
  queryFn: fetchRepositories,
})
```

**Q2**: queryKey의 역할은 무엇인가요? 왜 배열로 정의하나요?

### 질문 3: staleTime vs gcTime
```tsx
const { data } = useQuery({
  queryKey: ["repositories"],
  queryFn: fetchRepositories,
  staleTime: 1000 * 60 * 5,  // 5분
  gcTime: 1000 * 60 * 30,    // 30분
})
```

**Q3**: staleTime과 gcTime(구 cacheTime)의 차이는?
- 데이터가 "stale"하다는 것은 무슨 의미?
- 언제 refetch가 발생하나요?

### 질문 4: useMutation의 역할
```tsx
const mutation = useMutation({
  mutationFn: createRepository,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ["repositories"] })
  },
})

// 사용
mutation.mutate({ name: "new-repo", visibility: "public" })
```

**Q4**: mutation 후 invalidateQueries는 왜 필요한가요?

---

## 답변 작성

### A1:

### A2:

### A3:

### A4:
