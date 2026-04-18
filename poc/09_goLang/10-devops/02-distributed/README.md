# 21. Go로 배우는 분산 시스템

분산 시스템의 핵심 개념을 Go로 직접 구현하며 학습합니다.

---

## 참조 영상

| 자료 | 설명 |
|------|------|
| [Go로 배우는 분산 시스템 (GopherCon Korea 2024)](https://www.youtube.com/watch?v=4awGzz9IhyQ) | 김수빈(당근) - 핵심 참조 |

---

## 학습 목표

- [ ] 분산 시스템의 핵심 문제 이해 (CAP, 합의)
- [ ] Leader Election 구현
- [ ] 분산 락(Distributed Lock) 구현
- [ ] 간단한 Raft 합의 알고리즘 이해
- [ ] Go의 동시성을 활용한 분산 패턴

---

## 왜 Go로 분산 시스템인가?

| 특징 | 설명 |
|------|------|
| **동시성** | 고루틴, 채널로 네트워크 통신 자연스럽게 표현 |
| **단일 바이너리** | 배포 용이, 컨테이너 친화적 |
| **성능** | C/C++ 수준 성능, GC 부담 적음 |
| **실제 사례** | etcd, Kubernetes, CockroachDB, TiDB |

---

## 핵심 개념

### 1. CAP 정리

분산 시스템은 세 가지를 동시에 만족할 수 없음:

| 속성 | 설명 | 예시 |
|------|------|------|
| **C**onsistency | 모든 노드가 같은 데이터 | 은행 잔고 |
| **A**vailability | 항상 응답 가능 | 웹 서비스 |
| **P**artition Tolerance | 네트워크 분리에도 동작 | 필수 |

**선택**:
- CP: 일관성 우선 (etcd, ZooKeeper)
- AP: 가용성 우선 (Cassandra, DynamoDB)

### 2. 합의 알고리즘 (Consensus)

여러 노드가 하나의 값에 동의하는 방법

```
Node A: "값은 X다"
Node B: "값은 X다"  → 합의 완료!
Node C: "값은 X다"
```

**대표 알고리즘**:
- Paxos: 이론적 기초 (복잡)
- **Raft**: 이해하기 쉬움 (etcd, Consul 사용)

### 3. Leader Election

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Node A  │     │ Node B  │     │ Node C  │
│ Follower│     │ LEADER  │     │ Follower│
└────┬────┘     └────┬────┘     └────┬────┘
     │               │               │
     │◄──Heartbeat───│───Heartbeat──►│
     │               │               │
```

리더가 죽으면 → 새 선거 → 새 리더 선출

---

## 프로젝트 구조

```
21-distributed-systems/
├── README.md
├── EXERCISES.md
├── HINTS.md
├── LEARNED.md
├── go.mod
├── main.go
├── leader/
│   └── election.go      # Leader Election 구현
├── lock/
│   └── distributed.go   # 분산 락 구현
├── raft/
│   ├── node.go          # Raft 노드
│   ├── log.go           # 로그 복제
│   └── state.go         # 상태 머신
└── examples/
    ├── kv_store/        # 분산 Key-Value 저장소
    └── counter/         # 분산 카운터
```

---

## 코드 패턴

### 1. 노드 간 통신 (gRPC)

```go
// proto 정의
service Raft {
    rpc RequestVote(VoteRequest) returns (VoteResponse);
    rpc AppendEntries(AppendRequest) returns (AppendResponse);
}
```

### 2. Leader Election 기본 구조

```go
type Node struct {
    id       string
    state    State  // Follower, Candidate, Leader
    term     int    // 현재 임기
    votedFor string // 투표한 후보

    heartbeat chan struct{}
    mu        sync.Mutex
}

type State int

const (
    Follower State = iota
    Candidate
    Leader
)

func (n *Node) Run(ctx context.Context) {
    for {
        select {
        case <-ctx.Done():
            return
        default:
            switch n.state {
            case Follower:
                n.runFollower(ctx)
            case Candidate:
                n.runCandidate(ctx)
            case Leader:
                n.runLeader(ctx)
            }
        }
    }
}
```

### 3. 선거 타이머

```go
func (n *Node) runFollower(ctx context.Context) {
    timeout := randomTimeout(150, 300) // 150~300ms
    timer := time.NewTimer(timeout)

    for {
        select {
        case <-n.heartbeat:
            // 리더로부터 heartbeat 받음, 타이머 리셋
            timer.Reset(randomTimeout(150, 300))

        case <-timer.C:
            // 타임아웃! 선거 시작
            n.state = Candidate
            return

        case <-ctx.Done():
            return
        }
    }
}

func randomTimeout(min, max int) time.Duration {
    return time.Duration(min+rand.Intn(max-min)) * time.Millisecond
}
```

### 4. 분산 락

```go
type DistributedLock struct {
    key     string
    owner   string
    expires time.Time
    mu      sync.Mutex
}

func (l *DistributedLock) TryLock(owner string, ttl time.Duration) bool {
    l.mu.Lock()
    defer l.mu.Unlock()

    now := time.Now()

    // 락이 만료되었거나 없으면 획득
    if l.owner == "" || now.After(l.expires) {
        l.owner = owner
        l.expires = now.Add(ttl)
        return true
    }

    // 이미 내가 가진 락이면 갱신
    if l.owner == owner {
        l.expires = now.Add(ttl)
        return true
    }

    return false
}

func (l *DistributedLock) Unlock(owner string) bool {
    l.mu.Lock()
    defer l.mu.Unlock()

    if l.owner == owner {
        l.owner = ""
        return true
    }
    return false
}
```

---

## 학습 순서

### 1단계: 기초
- 노드 간 통신 (net/rpc 또는 gRPC)
- Heartbeat 구현
- 타임아웃 처리

### 2단계: Leader Election
- Follower → Candidate → Leader 상태 전이
- 투표 요청/응답
- Split Vote 처리

### 3단계: 로그 복제
- Leader가 로그 전파
- Follower가 로그 수신/적용
- 커밋 인덱스 관리

### 4단계: 실전 적용
- 분산 Key-Value 저장소
- 분산 락 서비스
- 설정 관리 시스템

---

## 참조 자료

### 영상
- [Go로 배우는 분산 시스템 (GopherCon Korea 2024)](https://www.youtube.com/watch?v=4awGzz9IhyQ) ⭐ 핵심

### 문서
- [Raft 논문 (한글 번역)](https://github.com/OnurGumus/raft-paper-korean)
- [Raft 시각화](https://raft.github.io/)
- [etcd Raft 구현](https://github.com/etcd-io/raft)

### 📚 Learning Go, 2nd Edition 참조
- **12_Concurrency_in_Go.md**: 고루틴, 채널, select (필수!)
- **14_The_Context.md**: 취소 전파, 타임아웃
- **13_The_Standard_Library.md**: net/rpc, time 패키지

---

## 관련 학습 모듈

| 모듈 | 관련 개념 |
|------|----------|
| **16-context** | 타임아웃, 취소 전파 |
| **18-worker-pool** | 동시성 패턴 |
| **19-websocket** | 실시간 통신 |
| **06-grpc** | 노드 간 RPC |

---

## 다음 단계

분산 시스템을 더 깊이 학습하려면:
- [MIT 6.824 분산 시스템](https://pdos.csail.mit.edu/6.824/) - 유명 강의
- [Designing Data-Intensive Applications](https://dataintensive.net/) - 필독서
- etcd, Consul 소스 코드 분석
