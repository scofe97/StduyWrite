# FSM 실습 과제

## 목표

looplab/fsm을 활용하여 게시글 워크플로우 상태 기계를 구현합니다.

---

## Phase 1: FSM 기본 설정

### Task 1.1: 프로젝트 초기화
- [ ] `go get -u github.com/looplab/fsm` 실행
- [ ] go.mod 파일에 의존성 추가 확인

### Task 1.2: NewPost 함수 구현 (workflow/post.go)
- [ ] FSM 인스턴스 생성 (`fsm.NewFSM`)
- [ ] 초기 상태: `draft`
- [ ] 이벤트 정의:
  - `publish`: draft → published
  - `archive`: published → archived
  - `republish`: archived → published
- [ ] 테스트: `go run main.go` 에러 없이 실행

### Task 1.3: 상태 확인 메서드
- [ ] `State()` 메서드가 현재 상태 반환 확인
- [ ] `Can(event)` 메서드가 전이 가능 여부 반환 확인
- [ ] `AvailableTransitions()` 메서드 확인
- [ ] 테스트:
  ```go
  post := workflow.NewPost(1, "Test")
  fmt.Println(post.State())  // "draft"
  fmt.Println(post.Can("publish"))  // true
  fmt.Println(post.Can("archive"))  // false
  ```

---

## Phase 2: 상태 전이

### Task 2.1: 전이 메서드 구현
- [ ] `Publish()` 메서드 구현 (`Event("publish")`)
- [ ] `Archive()` 메서드 구현 (`Event("archive")`)
- [ ] `Republish()` 메서드 구현 (`Event("republish")`)
- [ ] 테스트:
  ```go
  post.Publish()   // draft → published
  post.Archive()   // published → archived
  post.Republish() // archived → published
  ```

### Task 2.2: 에러 처리
- [ ] 잘못된 전이 시 에러 반환 확인
- [ ] 에러 메시지에 현재 상태와 시도한 전이 포함
- [ ] 테스트:
  ```go
  post := workflow.NewPost(1, "Test")
  err := post.Archive()  // draft 상태에서 archive 시도
  // err: "event archive inappropriate in current state draft"
  ```

### Task 2.3: 전이 체인
- [ ] 연속 전이 테스트:
  ```
  draft → publish → published → archive → archived → republish → published
  ```
- [ ] 중간에 에러 발생 시 이전 상태 유지 확인

---

## Phase 3: 콜백 기본

### Task 3.1: before/after 콜백
- [ ] `before_event` 콜백 등록 (모든 이벤트 전)
- [ ] `after_event` 콜백 등록 (모든 이벤트 후)
- [ ] 콜백에서 이벤트 정보 출력
- [ ] 테스트: 전이 시 로그 출력 확인

### Task 3.2: enter/leave 콜백
- [ ] `enter_published` 콜백 등록
- [ ] `leave_published` 콜백 등록
- [ ] 콜백에서 상태 정보 출력
- [ ] 테스트:
  ```
  [Enter Published] Post 'Test' is now public!
  [Leave Published] Post 'Test' is no longer public
  ```

### Task 3.3: 이벤트별 콜백
- [ ] `before_publish` 콜백 등록
- [ ] `after_publish` 콜백 등록
- [ ] `before_archive` 콜백 등록
- [ ] 테스트: 특정 이벤트에만 콜백 실행 확인

---

## Phase 4: 콜백 고급

### Task 4.1: 전이 취소
- [ ] `e.Cancel(err)` 로 전이 취소 구현
- [ ] 조건부 취소 로직 추가
- [ ] 테스트:
  ```go
  // 콘텐츠가 비어있으면 발행 불가
  post.Content = ""
  err := post.Publish()
  // err: "cannot publish empty post"
  // 상태: 여전히 draft
  ```

### Task 4.2: 콜백에서 데이터 전달
- [ ] `e.Args` 로 추가 데이터 전달
- [ ] 콜백에서 Args 읽기
- [ ] 테스트:
  ```go
  // Event에 인자 전달
  post.FSM.Event("publish", "admin", "urgent")
  // 콜백에서 Args[0], Args[1] 접근
  ```

### Task 4.3: UpdatedAt 자동 갱신
- [ ] `after_event` 콜백에서 UpdatedAt 갱신
- [ ] 전이 성공 시에만 갱신
- [ ] 테스트: 전이 후 UpdatedAt 변경 확인

---

## Phase 5: 상태 영속화

### Task 5.1: 외부 상태 설정
- [ ] `SetState(state)` 메서드 구현
- [ ] DB에서 로드한 상태로 FSM 설정
- [ ] 테스트:
  ```go
  post := workflow.NewPost(1, "Test")
  post.SetState("published")  // DB에서 로드한 상태
  fmt.Println(post.State())   // "published"
  ```

### Task 5.2: 상태 검증
- [ ] SetState에서 유효한 상태인지 검증
- [ ] 잘못된 상태 설정 시 에러 반환
- [ ] 테스트:
  ```go
  err := post.SetState("invalid")
  // err: "invalid state: invalid"
  ```

### Task 5.3: DB 연동 시나리오 (개념)
- [ ] 트랜잭션 내에서 상태 변경 + DB 업데이트 패턴 이해
- [ ] 콜백에서 DB 업데이트 vs 별도 로직
- [ ] 실패 시 롤백 전략

---

## Phase 6: 고급 패턴 (선택)

### Task 6.1: 콜백 체인
- [ ] 여러 콜백을 순서대로 실행
- [ ] 중간 실패 시 중단
- [ ] 테스트:
  ```go
  callbacks := ChainCallbacks(
      LoggingCallback,
      ValidationCallback,
      MetricsCallback,
  )
  ```

### Task 6.2: 조건부 콜백
- [ ] 조건에 따라 다른 동작
- [ ] 상태/이벤트에 따른 분기
- [ ] 테스트:
  ```go
  callback := ConditionalCallback(
      func(e *fsm.Event) bool { return e.Dst == "published" },
      func(e *fsm.Event) { sendNotification(e) },
  )
  ```

### Task 6.3: 주문 상태 기계 (추가 연습)
- [ ] 새 파일 `workflow/order.go` 생성
- [ ] 상태: pending → confirmed → shipped → delivered / cancelled
- [ ] 이벤트: confirm, ship, deliver, cancel
- [ ] 특별 규칙: shipped 후에는 cancel 불가

---

## Bonus Tasks

### Bonus 1: 상태 히스토리
- [ ] 상태 변경 히스토리 저장
- [ ] 히스토리 조회 메서드
- [ ] 테스트: 전체 상태 변경 이력 출력

### Bonus 2: 상태 다이어그램 생성
- [ ] Mermaid 또는 Graphviz 형식으로 다이어그램 출력
- [ ] 현재 상태 하이라이트
- [ ] 테스트: 다이어그램 문자열 생성

### Bonus 3: 동시성 안전
- [ ] Mutex를 사용한 동시성 보호
- [ ] 여러 고루틴에서 동시 전이 테스트
- [ ] 데이터 레이스 없이 동작 확인

---

## 학습 체크리스트

### 기본 개념
- [ ] FSM 생성 (fsm.NewFSM)
- [ ] 상태와 이벤트 정의
- [ ] 전이 규칙 이해 (Src → Dst)
- [ ] Current(), Can(), Event() 사용

### 콜백
- [ ] before/after 콜백
- [ ] enter/leave 콜백
- [ ] 이벤트별 콜백 (before_<event>)
- [ ] e.Cancel()로 전이 취소

### 고급 기능
- [ ] SetState()로 외부 상태 설정
- [ ] Args로 데이터 전달
- [ ] 콜백 체인
- [ ] DB 연동 패턴

---

## 성공 기준

모든 Task를 완료하면:

```bash
$ go run main.go

# 초기 상태
Initial state: draft
Can publish: true
Can archive: false

# 발행
--- Publishing post ---
[Before] publish: draft → published
[Enter Published] Post 'Hello World' is now public!
[After] publish: now published
Current state: published

# 잘못된 전이
--- Trying invalid transition ---
Expected error: event publish inappropriate in current state published

# 보관
--- Archiving post ---
[Before] archive: published → archived
[Leave Published] Post 'Hello World' is no longer public
[After] archive: now archived
Current state: archived

# 재발행
--- Republishing post ---
[Before] republish: archived → published
[Enter Published] Post 'Hello World' is now public!
[After] republish: now published
Current state: published

# 가능한 전이
--- Available transitions ---
Can archive? true
Can publish? false
```

---

**진행 방법**:
1. Phase 1부터 순서대로 진행
2. 각 Task의 체크박스를 완료하면 체크
3. 막히면 `HINTS.md` 참고 (스포일러 주의!)
4. 모든 Phase 완료 후 Bonus 도전
5. `LEARNED.md`에 학습 내용 정리

**예상 소요 시간**: 1.5-2시간
