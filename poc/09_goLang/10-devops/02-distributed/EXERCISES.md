# 21. 분산 시스템 실습 과제

## 필수 시청

시작 전 반드시 시청하세요:
- [Go로 배우는 분산 시스템 (GopherCon Korea 2024)](https://www.youtube.com/watch?v=4awGzz9IhyQ) - 김수빈(당근)

---

## 1단계: 노드 간 통신

### 과제 1-1: 간단한 RPC 서버/클라이언트
- [ ] net/rpc로 서버 구현
- [ ] Ping/Pong 메서드 구현
- [ ] 클라이언트에서 호출 테스트

```go
// 힌트: RPC 서비스 정의
type Node struct{}

type PingArgs struct {
    Message string
}

type PingReply struct {
    Message string
}

func (n *Node) Ping(args *PingArgs, reply *PingReply) error {
    reply.Message = "Pong: " + args.Message
    return nil
}
```

### 과제 1-2: 여러 노드 실행
- [ ] 3개 노드 실행 (포트 8001, 8002, 8003)
- [ ] 각 노드가 서로 통신 가능하도록 구성
- [ ] 노드 목록 설정 파일로 관리

---

## 2단계: Heartbeat 구현

### 과제 2-1: 리더의 Heartbeat 전송
- [ ] 리더가 100ms마다 Heartbeat 전송
- [ ] 팔로워가 Heartbeat 수신 확인
- [ ] 수신 시 로그 출력

### 과제 2-2: 타임아웃 감지
- [ ] 팔로워가 300ms 내 Heartbeat 없으면 감지
- [ ] 랜덤 타임아웃 (150~300ms) 구현
- [ ] 타임아웃 시 로그 출력

```go
// 힌트: 랜덤 타임아웃
func electionTimeout() time.Duration {
    return time.Duration(150+rand.Intn(150)) * time.Millisecond
}
```

---

## 3단계: Leader Election

### 과제 3-1: 상태 전이 구현
- [ ] Follower → Candidate 전이 (타임아웃 시)
- [ ] Candidate → Leader 전이 (과반수 득표 시)
- [ ] Candidate → Follower 전이 (더 높은 term 발견 시)

### 과제 3-2: 투표 요청/응답
- [ ] RequestVote RPC 구현
- [ ] 한 term에 한 번만 투표
- [ ] 투표 결과 집계

```go
// 힌트: 투표 요청
type RequestVoteArgs struct {
    Term        int
    CandidateID string
}

type RequestVoteReply struct {
    Term        int
    VoteGranted bool
}
```

### 과제 3-3: 전체 선거 흐름 테스트
- [ ] 3개 노드 시작 (모두 Follower)
- [ ] 타임아웃 후 선거 시작
- [ ] 1개 노드가 Leader 됨
- [ ] Leader 강제 종료 시 새 선거

---

## 4단계: 분산 락

### 과제 4-1: 단일 노드 락
- [ ] TryLock(owner, ttl) 구현
- [ ] Unlock(owner) 구현
- [ ] TTL 만료 시 자동 해제

### 과제 4-2: 분산 환경 락
- [ ] Leader만 락 관리
- [ ] 락 요청 → Leader로 전달
- [ ] 락 획득/실패 응답

```go
// 힌트: 락 요청
type LockRequest struct {
    Key   string
    Owner string
    TTL   time.Duration
}
```

---

## 5단계: 분산 Key-Value 저장소 (도전)

### 과제 5-1: 기본 KV 연산
- [ ] Put(key, value) 구현
- [ ] Get(key) 구현
- [ ] Delete(key) 구현

### 과제 5-2: 로그 복제
- [ ] Leader가 쓰기 요청 받음
- [ ] 로그 엔트리 생성
- [ ] Follower에게 복제
- [ ] 과반수 복제 후 커밋

### 과제 5-3: 일관성 테스트
- [ ] 클라이언트 A: Put("x", "1")
- [ ] 클라이언트 B: Get("x") → "1"
- [ ] Leader 변경 후에도 값 유지

---

## 검증 체크리스트

### Leader Election
```bash
# 터미널 1, 2, 3에서 각각 실행
go run main.go -id=node1 -port=8001
go run main.go -id=node2 -port=8002
go run main.go -id=node3 -port=8003

# 예상 출력 (노드 중 하나):
# [node2] state: Follower → Candidate
# [node2] requesting votes for term 1
# [node2] received vote from node1
# [node2] received vote from node3
# [node2] state: Candidate → Leader
# [node2] sending heartbeat...
```

### 분산 락
```bash
# 터미널 1
curl http://localhost:8001/lock?key=resource1&owner=client1&ttl=10s
# {"success": true}

# 터미널 2 (즉시)
curl http://localhost:8001/lock?key=resource1&owner=client2&ttl=10s
# {"success": false, "holder": "client1"}

# 10초 후 터미널 2
curl http://localhost:8001/lock?key=resource1&owner=client2&ttl=10s
# {"success": true}
```

---

## 학습 완료 후

`LEARNED.md`에 다음을 기록하세요:
- CAP 정리에서 왜 P는 필수인가?
- 랜덤 타임아웃이 왜 필요한가?
- Split Vote란 무엇이고 어떻게 해결하는가?
- Leader가 죽으면 어떤 일이 발생하는가?
- 로그 복제가 왜 필요한가?
