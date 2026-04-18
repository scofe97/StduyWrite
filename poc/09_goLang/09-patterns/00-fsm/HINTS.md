# FSM 힌트

막힐 때만 참고하세요! 스스로 해결하는 것이 학습에 더 효과적입니다.

---

## Phase 1: FSM 기본 설정

<details>
<summary>Task 1.2: NewPost 함수 구현</summary>

```go
func NewPost(id int64, title string) *Post {
    p := &Post{
        ID:        id,
        Title:     title,
        UpdatedAt: time.Now(),
    }

    p.FSM = fsm.NewFSM(
        StateDraft,  // 초기 상태
        fsm.Events{
            {Name: EventPublish, Src: []string{StateDraft}, Dst: StatePublished},
            {Name: EventArchive, Src: []string{StatePublished}, Dst: StateArchived},
            {Name: EventRepublish, Src: []string{StateArchived}, Dst: StatePublished},
        },
        fsm.Callbacks{
            "before_event":    p.beforeEvent,
            "after_event":     p.afterEvent,
            "enter_published": p.onEnterPublished,
            "leave_published": p.onLeavePublished,
        },
    )

    return p
}
```
</details>

<details>
<summary>Task 1.3: 상태 확인 메서드</summary>

```go
func (p *Post) State() string {
    return p.FSM.Current()
}

func (p *Post) Can(event string) bool {
    return p.FSM.Can(event)
}

func (p *Post) AvailableTransitions() []string {
    return p.FSM.AvailableTransitions()
}
```
</details>

---

## Phase 2: 상태 전이

<details>
<summary>Task 2.1: 전이 메서드 구현</summary>

```go
func (p *Post) Publish() error {
    return p.FSM.Event(EventPublish)
}

func (p *Post) Archive() error {
    return p.FSM.Event(EventArchive)
}

func (p *Post) Republish() error {
    return p.FSM.Event(EventRepublish)
}
```

**main.go에서 테스트**:
```go
post := workflow.NewPost(1, "Hello World")

fmt.Printf("Initial state: %s\n", post.State())

err := post.Publish()
if err != nil {
    log.Fatal(err)
}
fmt.Printf("After publish: %s\n", post.State())

err = post.Archive()
fmt.Printf("After archive: %s\n", post.State())

err = post.Republish()
fmt.Printf("After republish: %s\n", post.State())
```
</details>

<details>
<summary>Task 2.2: 에러 처리</summary>

```go
post := workflow.NewPost(1, "Test")

// draft 상태에서 archive 시도 (불가능)
err := post.Archive()
if err != nil {
    fmt.Printf("Error: %v\n", err)
    // Error: event archive inappropriate in current state draft
}

// 상태는 여전히 draft
fmt.Printf("State: %s\n", post.State())

// 에러 타입 확인
var invalidEvent *fsm.InvalidEventError
if errors.As(err, &invalidEvent) {
    fmt.Printf("Invalid event: %s in state %s\n",
        invalidEvent.Event, invalidEvent.State)
}
```
</details>

---

## Phase 3: 콜백 기본

<details>
<summary>Task 3.1: before/after 콜백</summary>

```go
p.FSM = fsm.NewFSM(
    StateDraft,
    fsm.Events{...},
    fsm.Callbacks{
        // 모든 이벤트 전
        "before_event": func(e *fsm.Event) {
            fmt.Printf("[Before] %s: %s → %s\n", e.Event, e.Src, e.Dst)
        },
        // 모든 이벤트 후
        "after_event": func(e *fsm.Event) {
            fmt.Printf("[After] %s: now %s\n", e.Event, e.Dst)
        },
    },
)
```

**콜백 실행 순서**:
1. `before_<event>` (특정 이벤트)
2. `before_event` (모든 이벤트)
3. `leave_<state>` (출발 상태)
4. `enter_<state>` (도착 상태)
5. `after_<event>` (특정 이벤트)
6. `after_event` (모든 이벤트)
</details>

<details>
<summary>Task 3.2: enter/leave 콜백</summary>

```go
fsm.Callbacks{
    "enter_published": func(e *fsm.Event) {
        // p는 클로저로 캡처하거나 e.Args로 전달
        fmt.Printf("[Enter Published] State entered!\n")
    },
    "leave_published": func(e *fsm.Event) {
        fmt.Printf("[Leave Published] State left!\n")
    },
}

// 또는 메서드로 정의
func (p *Post) onEnterPublished(e *fsm.Event) {
    fmt.Printf("[Enter Published] Post '%s' is now public!\n", p.Title)
}
```
</details>

<details>
<summary>Task 3.3: 이벤트별 콜백</summary>

```go
fsm.Callbacks{
    // 특정 이벤트 전
    "before_publish": func(e *fsm.Event) {
        fmt.Println("[BeforePublish] Validating...")
    },
    // 특정 이벤트 후
    "after_publish": func(e *fsm.Event) {
        fmt.Println("[AfterPublish] Published!")
    },
    "before_archive": func(e *fsm.Event) {
        fmt.Println("[BeforeArchive] Archiving...")
    },
}
```
</details>

---

## Phase 4: 콜백 고급

<details>
<summary>Task 4.1: 전이 취소</summary>

```go
func (p *Post) validationCallback(e *fsm.Event) {
    // 발행 전 콘텐츠 검증
    if e.Event == "publish" && p.Content == "" {
        e.Cancel(fmt.Errorf("cannot publish empty post"))
        return
    }

    // 또는 e.Err에 에러 설정
    // e.Err = fmt.Errorf("validation failed")
}

// FSM에 등록
fsm.Callbacks{
    "before_publish": p.validationCallback,
}

// 테스트
post := workflow.NewPost(1, "Test")
post.Content = ""

err := post.Publish()
if err != nil {
    fmt.Printf("Error: %v\n", err)  // cannot publish empty post
}
fmt.Printf("State: %s\n", post.State())  // draft (전이 취소됨)
```
</details>

<details>
<summary>Task 4.2: 콜백에서 데이터 전달</summary>

```go
// 이벤트 호출 시 인자 전달
err := post.FSM.Event("publish", "admin", "urgent")

// 콜백에서 인자 읽기
func (p *Post) afterPublishWithArgs(e *fsm.Event) {
    if len(e.Args) >= 2 {
        publisher := e.Args[0].(string)
        priority := e.Args[1].(string)
        fmt.Printf("Published by %s with %s priority\n", publisher, priority)
    }
}

// 래퍼 메서드 만들기
func (p *Post) PublishBy(user string) error {
    return p.FSM.Event("publish", user)
}
```
</details>

<details>
<summary>Task 4.3: UpdatedAt 자동 갱신</summary>

```go
func (p *Post) afterEvent(e *fsm.Event) {
    p.UpdatedAt = time.Now()
    fmt.Printf("[After] UpdatedAt: %s\n", p.UpdatedAt.Format(time.RFC3339))
}

// FSM에 등록
fsm.Callbacks{
    "after_event": p.afterEvent,
}
```
</details>

---

## Phase 5: 상태 영속화

<details>
<summary>Task 5.1: SetState 구현</summary>

```go
func (p *Post) SetState(state string) error {
    // 유효한 상태인지 확인
    validStates := map[string]bool{
        StateDraft:     true,
        StatePublished: true,
        StateArchived:  true,
    }

    if !validStates[state] {
        return fmt.Errorf("invalid state: %s", state)
    }

    p.FSM.SetState(state)
    return nil
}

// 사용 예 (DB에서 로드)
func LoadPostFromDB(id int64) (*Post, error) {
    // DB에서 데이터 로드
    row := db.QueryRow("SELECT id, title, status FROM posts WHERE id = ?", id)

    var post Post
    var status string
    row.Scan(&post.ID, &post.Title, &status)

    // FSM 생성 후 상태 설정
    post.FSM = fsm.NewFSM(...)
    post.SetState(status)

    return &post, nil
}
```
</details>

<details>
<summary>Task 5.3: DB 연동 패턴</summary>

```go
// 패턴 1: 콜백에서 DB 업데이트
func (p *Post) afterEvent(e *fsm.Event) {
    // 주의: 콜백에서 DB 에러 발생 시 처리 어려움
    db.Exec("UPDATE posts SET status = ? WHERE id = ?", e.Dst, p.ID)
}

// 패턴 2: 별도 메서드에서 트랜잭션 관리 (권장)
func (s *PostService) PublishPost(ctx context.Context, id int64) error {
    return s.db.WithTx(func(tx *sql.Tx) error {
        // 1. 게시글 로드 (잠금)
        post, err := s.repo.GetForUpdate(tx, id)
        if err != nil {
            return err
        }

        // 2. FSM 전이
        if err := post.Publish(); err != nil {
            return err  // 잘못된 전이 → 롤백
        }

        // 3. DB 업데이트
        return s.repo.UpdateStatus(tx, id, post.State())
    })
}

// 패턴 3: 낙관적 락
func (s *PostService) PublishPost(ctx context.Context, post *Post) error {
    // 1. FSM 전이 (메모리)
    oldState := post.State()
    if err := post.Publish(); err != nil {
        return err
    }

    // 2. DB 업데이트 (조건부)
    result, err := s.db.Exec(
        "UPDATE posts SET status = ? WHERE id = ? AND status = ?",
        post.State(), post.ID, oldState)

    // 3. 충돌 확인
    rows, _ := result.RowsAffected()
    if rows == 0 {
        // 다른 프로세스가 이미 변경함
        post.SetState(oldState)  // 롤백
        return ErrConcurrentModification
    }

    return nil
}
```
</details>

---

## 일반적인 문제 해결

<details>
<summary>콜백에서 Post에 접근할 수 없어요</summary>

**방법 1: 메서드로 정의 (권장)**
```go
func (p *Post) myCallback(e *fsm.Event) {
    // p에 직접 접근 가능
    fmt.Printf("Post title: %s\n", p.Title)
}

// FSM에 등록
fsm.Callbacks{
    "after_event": p.myCallback,  // 메서드 참조
}
```

**방법 2: 클로저 사용**
```go
p := &Post{...}

p.FSM = fsm.NewFSM(
    StateDraft,
    fsm.Events{...},
    fsm.Callbacks{
        "after_event": func(e *fsm.Event) {
            // 클로저로 p 캡처
            fmt.Printf("Post: %s\n", p.Title)
        },
    },
)
```

**방법 3: Args로 전달**
```go
err := p.FSM.Event("publish", p)

func callback(e *fsm.Event) {
    post := e.Args[0].(*Post)
    fmt.Printf("Post: %s\n", post.Title)
}
```
</details>

<details>
<summary>전이 취소가 안 돼요</summary>

**e.Cancel() 사용**:
```go
func (p *Post) beforePublish(e *fsm.Event) {
    if p.Content == "" {
        e.Cancel(fmt.Errorf("content is empty"))
        // 또는
        // e.Err = fmt.Errorf("content is empty")
        return
    }
}
```

**주의**: `before_<event>`나 `before_event`에서만 취소 가능.
`after_*`나 `enter_*`에서는 이미 전이 완료됨.
</details>

<details>
<summary>여러 Src 상태에서 같은 Dst로 전이</summary>

```go
fsm.Events{
    // 여러 출발 상태 가능
    {
        Name: "cancel",
        Src:  []string{"pending", "confirmed", "processing"},
        Dst:  "cancelled",
    },
}
```
</details>

<details>
<summary>콜백 실행 순서 확인</summary>

**전체 순서**:
1. `before_<event>`
2. `before_event`
3. `leave_<old_state>`
4. `leave_state` (모든 상태 퇴장)
5. `enter_<new_state>`
6. `enter_state` (모든 상태 진입)
7. `after_<event>`
8. `after_event`

**디버깅**:
```go
fsm.Callbacks{
    "before_event": func(e *fsm.Event) { fmt.Println("1. before_event") },
    "after_event":  func(e *fsm.Event) { fmt.Println("6. after_event") },
    "before_publish": func(e *fsm.Event) { fmt.Println("0. before_publish") },
    "leave_draft": func(e *fsm.Event) { fmt.Println("2. leave_draft") },
    "enter_published": func(e *fsm.Event) { fmt.Println("3. enter_published") },
    "after_publish": func(e *fsm.Event) { fmt.Println("5. after_publish") },
}
```
</details>

---

## 추가 리소스

**상태 다이어그램 생성**:
```go
func (p *Post) Diagram() string {
    return `
stateDiagram-v2
    [*] --> draft
    draft --> published : publish
    published --> archived : archive
    archived --> published : republish
`
}
```

**참고 프로젝트**:
- [looplab/fsm examples](https://github.com/looplab/fsm/tree/master/examples)
- [State Pattern](https://refactoring.guru/design-patterns/state/go/example)

---

**힌트를 너무 많이 봤다면**: 파일을 삭제하고 처음부터 다시 도전해보세요!
