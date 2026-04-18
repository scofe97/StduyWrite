# Phase 2: Investigate - Zustand 실험

## 실험 과제

### 실험 1: 리렌더링 추적

```tsx
// src/experiments/zustand-rerender.tsx
import { create } from "zustand"

const useStore = create((set) => ({
  user: { name: "Kim", email: "kim@test.com" },
  settings: { theme: "dark", lang: "ko" },
  updateName: (name: string) =>
    set((state) => ({ user: { ...state.user, name } })),
  updateTheme: (theme: string) =>
    set((state) => ({ settings: { ...state.settings, theme } })),
}))

let userRenders = 0
let settingsRenders = 0

function UserInfo() {
  userRenders++
  console.log("UserInfo rendered:", userRenders)
  const user = useStore((state) => state.user)
  return <div>User: {user.name}</div>
}

function Settings() {
  settingsRenders++
  console.log("Settings rendered:", settingsRenders)
  const settings = useStore((state) => state.settings)
  return <div>Theme: {settings.theme}</div>
}

export function ZustandRerenderTest() {
  const updateName = useStore((state) => state.updateName)
  const updateTheme = useStore((state) => state.updateTheme)

  return (
    <div>
      <UserInfo />
      <Settings />
      <button onClick={() => updateName("Lee")}>Change Name</button>
      <button onClick={() => updateTheme("light")}>Change Theme</button>
    </div>
  )
}
```

**관찰할 것**:
- [ ] Name 변경 시 어떤 컴포넌트가 리렌더링?
- [ ] Theme 변경 시 어떤 컴포넌트가 리렌더링?
- [ ] 셀렉터 없이 전체 state를 구독하면?

### 실험 2: shallow equality

```tsx
// src/experiments/zustand-shallow.tsx
import { create } from "zustand"
import { useShallow } from "zustand/react/shallow"

const useStore = create((set) => ({
  todos: [
    { id: 1, text: "Learn Zustand", done: false },
    { id: 2, text: "Build App", done: false },
  ],
  addTodo: (text: string) =>
    set((state) => ({
      todos: [...state.todos, { id: Date.now(), text, done: false }],
    })),
  toggleTodo: (id: number) =>
    set((state) => ({
      todos: state.todos.map((t) =>
        t.id === id ? { ...t, done: !t.done } : t
      ),
    })),
}))

let normalRenders = 0
let shallowRenders = 0

function NormalSelect() {
  normalRenders++
  // 새 배열 참조가 매번 생성됨
  const doneTodos = useStore((state) => state.todos.filter((t) => t.done))
  console.log("NormalSelect:", normalRenders)
  return <div>Done (normal): {doneTodos.length}</div>
}

function ShallowSelect() {
  shallowRenders++
  // shallow 비교로 불필요한 리렌더링 방지
  const doneTodos = useStore(
    useShallow((state) => state.todos.filter((t) => t.done))
  )
  console.log("ShallowSelect:", shallowRenders)
  return <div>Done (shallow): {doneTodos.length}</div>
}

export function ShallowTest() {
  const addTodo = useStore((state) => state.addTodo)
  const toggleTodo = useStore((state) => state.toggleTodo)

  return (
    <div>
      <NormalSelect />
      <ShallowSelect />
      <button onClick={() => addTodo("New Todo")}>Add</button>
      <button onClick={() => toggleTodo(1)}>Toggle #1</button>
    </div>
  )
}
```

**관찰할 것**:
- [ ] Add 버튼 클릭 시 두 컴포넌트의 렌더 횟수
- [ ] Toggle 버튼 클릭 시 차이
- [ ] useShallow의 효과

### 실험 3: Persist Middleware

```tsx
// src/experiments/zustand-persist.tsx
import { create } from "zustand"
import { persist, createJSONStorage } from "zustand/middleware"

interface SettingsState {
  theme: "light" | "dark"
  fontSize: number
  setTheme: (theme: "light" | "dark") => void
  setFontSize: (size: number) => void
}

const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      theme: "light",
      fontSize: 14,
      setTheme: (theme) => set({ theme }),
      setFontSize: (fontSize) => set({ fontSize }),
    }),
    {
      name: "settings-storage",
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({ theme: state.theme }),  // fontSize는 저장 안함
    }
  )
)

export function PersistTest() {
  const { theme, fontSize, setTheme, setFontSize } = useSettingsStore()

  return (
    <div>
      <p>Theme: {theme}</p>
      <p>Font Size: {fontSize}</p>
      <button onClick={() => setTheme(theme === "light" ? "dark" : "light")}>
        Toggle Theme
      </button>
      <button onClick={() => setFontSize(fontSize + 2)}>
        Increase Font
      </button>
      <p>Now refresh the page and check values!</p>
    </div>
  )
}
```

**관찰할 것**:
- [ ] 설정 변경 후 DevTools > Application > Local Storage 확인
- [ ] 페이지 새로고침 후 theme 값
- [ ] 페이지 새로고침 후 fontSize 값 (partialize로 제외됨)

---

## 실험 결과 기록

### 실험 1 결과:

### 실험 2 결과:

### 실험 3 결과:
