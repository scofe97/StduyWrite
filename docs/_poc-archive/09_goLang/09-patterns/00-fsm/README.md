# FSM (Finite State Machine) 학습

## 학습 목표

looplab/fsm을 사용하여 상태 기계를 구현하고 복잡한 워크플로우를 관리하는 방법을 익힙니다.

## FSM이란?

유한 상태 기계(FSM)는 시스템이 가질 수 있는 상태와 상태 간 전이를 정의하는 모델입니다.

**사용 사례**:
- 주문 처리: created → paid → shipped → delivered
- 게시글 관리: draft → published → archived
- 사용자 계정: pending → active → suspended → deleted
- 결제 상태: initiated → processing → completed/failed

**장점**:
- 명시적인 상태 관리
- 잘못된 전이 방지
- 전이 로직 중앙화
- 테스트 용이성

## 핵심 개념

### 1. 상태 (State)

시스템이 가질 수 있는 상태:
```go
const (
    StateDraft     = "draft"
    StatePublished = "published"
    StateArchived  = "archived"
)
```

### 2. 이벤트 (Event)

상태 전이를 트리거하는 이벤트:
```go
const (
    EventPublish   = "publish"
    EventArchive   = "archive"
    EventRepublish = "republish"
)
```

### 3. 전이 (Transition)

```
[draft] --publish--> [published] --archive--> [archived]
                          ^                       |
                          +-----republish---------+
```

### 4. 콜백 (Callback)

전이 전/후에 실행되는 함수:
- `before_<event>`: 이벤트 전에 실행
- `after_<event>`: 이벤트 후에 실행
- `enter_<state>`: 상태 진입 시 실행
- `leave_<state>`: 상태 퇴장 시 실행

## 프로젝트 구조

```
27-fsm/
├── main.go              # 엔트리 포인트
├── workflow/
│   ├── post.go          # 게시글 상태 기계
│   └── callbacks.go     # 콜백 함수들
├── go.mod
├── README.md            # 이 파일
├── EXERCISES.md         # 실습 과제
├── HINTS.md             # 힌트
└── LEARNED.md           # 학습 회고
```

## 학습 흐름

### 1단계: FSM 기본
- 상태와 이벤트 정의
- FSM 인스턴스 생성
- 전이 규칙 정의

### 2단계: 전이 실행
- Event() 메서드로 전이
- Can() 메서드로 전이 가능 여부 확인
- 에러 처리

### 3단계: 콜백
- before/after 콜백
- enter/leave 콜백
- 전이 취소 (Cancel)

### 4단계: 고급 패턴
- DB 연동 (상태 영속화)
- 비동기 콜백
- 콜백 체인

## 주요 API

### FSM 생성

```go
import "github.com/looplab/fsm"

f := fsm.NewFSM(
    "initial_state",
    fsm.Events{
        {Name: "event1", Src: []string{"state1"}, Dst: "state2"},
        {Name: "event2", Src: []string{"state2"}, Dst: "state3"},
    },
    fsm.Callbacks{
        "before_event1": func(e *fsm.Event) { /* ... */ },
        "after_event1":  func(e *fsm.Event) { /* ... */ },
        "enter_state2":  func(e *fsm.Event) { /* ... */ },
    },
)
```

### 상태 확인

```go
f.Current()                    // 현재 상태
f.Is("state1")                 // 특정 상태인지
f.Can("event1")                // 전이 가능한지
f.AvailableTransitions()       // 가능한 전이 목록
```

### 전이 실행

```go
err := f.Event("event1")       // 전이 실행
if err != nil {
    // 에러 처리
}
```

### 콜백 시그니처

```go
func callback(e *fsm.Event) {
    e.Event  // 이벤트 이름
    e.Src    // 출발 상태
    e.Dst    // 목적 상태
    e.Err    // 에러 설정
    e.Args   // 추가 인자
    e.Cancel(err) // 전이 취소
}
```

## 실행 예시

```bash
# 의존성 설치
go get -u github.com/looplab/fsm

# 실행
go run main.go
```

## 참고 자료

- [looplab/fsm GitHub](https://github.com/looplab/fsm)
- [State Pattern (GoF)](https://refactoring.guru/design-patterns/state)
- [Finite State Machine](https://en.wikipedia.org/wiki/Finite-state_machine)

### 연관 모듈
- **26-sqlc**: 상태 변경을 DB에 저장
- **28-capstone**: Blog API에서 게시글 상태 관리

## 다음 단계

1. `EXERCISES.md`에서 TODO 체크박스 확인
2. 각 파일의 TODO 주석을 채우며 구현
3. `HINTS.md`는 막힐 때만 참고
4. 완료 후 `LEARNED.md`에 회고 작성

## 디버깅 팁

```bash
# 상태 전이 로그
# 콜백에서 fmt.Printf로 출력

# 현재 상태 확인
fmt.Printf("Current: %s\n", post.State())

# 가능한 전이 확인
fmt.Printf("Can publish: %v\n", post.Can("publish"))
fmt.Printf("Available: %v\n", post.AvailableTransitions())
```

## 성공 기준

- [ ] FSM 생성 및 초기화
- [ ] 상태 전이 동작
- [ ] 잘못된 전이 시 에러 발생
- [ ] 콜백 동작
- [ ] 상태 영속화 가능

---

**시작하기**: `EXERCISES.md`를 열고 첫 번째 TODO부터 시작하세요!
