# Phase 2: Investigate - TanStack Query 실험

## 실험 과제

### 실험 1: queryKey와 캐싱

```tsx
// src/experiments/query-key-test.tsx
import { useQuery, useQueryClient } from "@tanstack/react-query"

// 가짜 API (네트워크 탭에서 확인용)
const fetchRepo = async (id: string) => {
  console.log(`Fetching repo ${id}...`)
  await new Promise(resolve => setTimeout(resolve, 1000))
  return { id, name: `repo-${id}`, stars: Math.floor(Math.random() * 100) }
}

export function QueryKeyTest() {
  const queryClient = useQueryClient()

  // 같은 queryKey로 여러 번 호출
  const query1 = useQuery({
    queryKey: ["repo", "1"],
    queryFn: () => fetchRepo("1"),
  })

  const query2 = useQuery({
    queryKey: ["repo", "1"],  // 동일한 key
    queryFn: () => fetchRepo("1"),
  })

  const query3 = useQuery({
    queryKey: ["repo", "2"],  // 다른 key
    queryFn: () => fetchRepo("2"),
  })

  return (
    <div>
      <p>Query1: {JSON.stringify(query1.data)}</p>
      <p>Query2: {JSON.stringify(query2.data)}</p>
      <p>Query3: {JSON.stringify(query3.data)}</p>
      <button onClick={() => queryClient.invalidateQueries({ queryKey: ["repo"] })}>
        Invalidate All
      </button>
    </div>
  )
}
```

**관찰할 것**:
- [ ] console.log가 몇 번 찍히는가?
- [ ] query1과 query2는 같은 데이터를 공유하는가?
- [ ] invalidateQueries 후 동작

### 실험 2: staleTime과 refetch

```tsx
// src/experiments/stale-time-test.tsx
import { useQuery } from "@tanstack/react-query"

const fetchData = async () => {
  console.log("Fetching at", new Date().toLocaleTimeString())
  return { time: new Date().toISOString() }
}

export function StaleTimeTest() {
  const { data, isFetching, isStale } = useQuery({
    queryKey: ["time"],
    queryFn: fetchData,
    staleTime: 5000,  // 5초 후 stale
  })

  return (
    <div>
      <p>Data: {data?.time}</p>
      <p>Is Fetching: {String(isFetching)}</p>
      <p>Is Stale: {String(isStale)}</p>
      <p>현재 시간: {new Date().toLocaleTimeString()}</p>
    </div>
  )
}
```

**관찰할 것**:
- [ ] 페이지 로드 후 5초 이내에 다른 탭 갔다 오면?
- [ ] 5초 이후에 다른 탭 갔다 오면?
- [ ] isStale이 true가 되는 시점

### 실험 3: Optimistic Updates

```tsx
// src/experiments/optimistic-test.tsx
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"

const fetchTodos = async () => {
  await new Promise(r => setTimeout(r, 500))
  return [{ id: 1, text: "Learn React Query", done: false }]
}

const updateTodo = async (todo: { id: number; done: boolean }) => {
  await new Promise(r => setTimeout(r, 2000))  // 느린 API
  return todo
}

export function OptimisticTest() {
  const queryClient = useQueryClient()
  const { data: todos } = useQuery({
    queryKey: ["todos"],
    queryFn: fetchTodos,
  })

  const mutation = useMutation({
    mutationFn: updateTodo,
    // Optimistic update
    onMutate: async (newTodo) => {
      await queryClient.cancelQueries({ queryKey: ["todos"] })
      const previous = queryClient.getQueryData(["todos"])
      queryClient.setQueryData(["todos"], (old: any) =>
        old?.map((t: any) => t.id === newTodo.id ? { ...t, done: newTodo.done } : t)
      )
      return { previous }
    },
    onError: (err, variables, context) => {
      queryClient.setQueryData(["todos"], context?.previous)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] })
    },
  })

  return (
    <div>
      {todos?.map(todo => (
        <div key={todo.id}>
          <input
            type="checkbox"
            checked={todo.done}
            onChange={() => mutation.mutate({ id: todo.id, done: !todo.done })}
          />
          {todo.text}
        </div>
      ))}
    </div>
  )
}
```

**관찰할 것**:
- [ ] 체크박스 클릭 즉시 UI가 변경되는가?
- [ ] 2초 후 API 응답이 오면 어떻게 되는가?
- [ ] 에러 발생 시 롤백되는가? (updateTodo에서 throw 해보기)

---

## 실험 결과 기록

### 실험 1 결과:

### 실험 2 결과:

### 실험 3 결과:
