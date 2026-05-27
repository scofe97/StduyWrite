# 21. 분산 시스템 힌트

막힐 때만 참고하세요.

---

## RPC 서버 설정

```go
import (
    "net"
    "net/rpc"
)

type Node struct {
    id    string
    peers []string
}

func (n *Node) StartServer(port string) error {
    rpc.Register(n)

    listener, err := net.Listen("tcp", ":"+port)
    if err != nil {
        return err
    }

    go func() {
        for {
            conn, _ := listener.Accept()
            go rpc.ServeConn(conn)
        }
    }()

    return nil
}
```

---

## RPC 클라이언트 호출

```go
func (n *Node) callPeer(peer string, method string, args, reply interface{}) error {
    client, err := rpc.Dial("tcp", peer)
    if err != nil {
        return err
    }
    defer client.Close()

    return client.Call(method, args, reply)
}

// 사용
var reply PingReply
err := n.callPeer("localhost:8002", "Node.Ping", &PingArgs{Message: "hello"}, &reply)
```

---

## 상태 전이 구조

```go
type State int

const (
    Follower State = iota
    Candidate
    Leader
)

type Node struct {
    mu       sync.Mutex
    state    State
    term     int
    votedFor string

    // 채널
    heartbeatCh chan struct{}
    voteCh      chan struct{}

    // 설정
    id    string
    peers []string
}

func (n *Node) Run(ctx context.Context) {
    for {
        select {
        case <-ctx.Done():
            return
        default:
        }

        n.mu.Lock()
        state := n.state
        n.mu.Unlock()

        switch state {
        case Follower:
            n.runFollower(ctx)
        case Candidate:
            n.runCandidate(ctx)
        case Leader:
            n.runLeader(ctx)
        }
    }
}
```

---

## Follower 로직

```go
func (n *Node) runFollower(ctx context.Context) {
    timeout := electionTimeout()
    timer := time.NewTimer(timeout)
    defer timer.Stop()

    for {
        select {
        case <-ctx.Done():
            return

        case <-n.heartbeatCh:
            // Heartbeat 받음, 타이머 리셋
            timer.Reset(electionTimeout())

        case <-n.voteCh:
            // 투표함, 타이머 리셋
            timer.Reset(electionTimeout())

        case <-timer.C:
            // 타임아웃! Candidate로 전환
            n.mu.Lock()
            n.state = Candidate
            n.mu.Unlock()
            return
        }
    }
}

func electionTimeout() time.Duration {
    return time.Duration(150+rand.Intn(150)) * time.Millisecond
}
```

---

## Candidate 로직

```go
func (n *Node) runCandidate(ctx context.Context) {
    n.mu.Lock()
    n.term++
    n.votedFor = n.id
    currentTerm := n.term
    n.mu.Unlock()

    votes := 1 // 자기 자신에게 투표
    voteCh := make(chan bool, len(n.peers))

    // 모든 피어에게 투표 요청
    for _, peer := range n.peers {
        go func(peer string) {
            args := &RequestVoteArgs{
                Term:        currentTerm,
                CandidateID: n.id,
            }
            var reply RequestVoteReply

            if err := n.callPeer(peer, "Node.RequestVote", args, &reply); err != nil {
                voteCh <- false
                return
            }

            if reply.Term > currentTerm {
                // 더 높은 term 발견, Follower로
                n.mu.Lock()
                n.state = Follower
                n.term = reply.Term
                n.mu.Unlock()
            }

            voteCh <- reply.VoteGranted
        }(peer)
    }

    // 결과 집계
    timeout := electionTimeout()
    timer := time.NewTimer(timeout)

    for {
        select {
        case <-ctx.Done():
            return

        case granted := <-voteCh:
            if granted {
                votes++
            }
            // 과반수 득표
            if votes > (len(n.peers)+1)/2 {
                n.mu.Lock()
                n.state = Leader
                n.mu.Unlock()
                return
            }

        case <-timer.C:
            // 타임아웃, 새 선거
            return

        case <-n.heartbeatCh:
            // 다른 Leader 발견, Follower로
            n.mu.Lock()
            n.state = Follower
            n.mu.Unlock()
            return
        }
    }
}
```

---

## Leader 로직

```go
func (n *Node) runLeader(ctx context.Context) {
    ticker := time.NewTicker(50 * time.Millisecond) // Heartbeat 간격
    defer ticker.Stop()

    for {
        select {
        case <-ctx.Done():
            return

        case <-ticker.C:
            n.sendHeartbeats()

        default:
            n.mu.Lock()
            if n.state != Leader {
                n.mu.Unlock()
                return
            }
            n.mu.Unlock()
        }
    }
}

func (n *Node) sendHeartbeats() {
    n.mu.Lock()
    currentTerm := n.term
    n.mu.Unlock()

    for _, peer := range n.peers {
        go func(peer string) {
            args := &AppendEntriesArgs{
                Term:     currentTerm,
                LeaderID: n.id,
            }
            var reply AppendEntriesReply

            if err := n.callPeer(peer, "Node.AppendEntries", args, &reply); err != nil {
                return
            }

            if reply.Term > currentTerm {
                n.mu.Lock()
                n.state = Follower
                n.term = reply.Term
                n.mu.Unlock()
            }
        }(peer)
    }
}
```

---

## RPC 핸들러

```go
// RequestVote RPC 핸들러
func (n *Node) RequestVote(args *RequestVoteArgs, reply *RequestVoteReply) error {
    n.mu.Lock()
    defer n.mu.Unlock()

    reply.Term = n.term
    reply.VoteGranted = false

    if args.Term < n.term {
        return nil
    }

    if args.Term > n.term {
        n.term = args.Term
        n.state = Follower
        n.votedFor = ""
    }

    if n.votedFor == "" || n.votedFor == args.CandidateID {
        n.votedFor = args.CandidateID
        reply.VoteGranted = true

        // voteCh에 신호
        select {
        case n.voteCh <- struct{}{}:
        default:
        }
    }

    return nil
}

// AppendEntries RPC 핸들러 (Heartbeat)
func (n *Node) AppendEntries(args *AppendEntriesArgs, reply *AppendEntriesReply) error {
    n.mu.Lock()
    defer n.mu.Unlock()

    reply.Term = n.term
    reply.Success = false

    if args.Term < n.term {
        return nil
    }

    if args.Term > n.term {
        n.term = args.Term
        n.votedFor = ""
    }

    n.state = Follower
    reply.Success = true

    // heartbeatCh에 신호
    select {
    case n.heartbeatCh <- struct{}{}:
    default:
    }

    return nil
}
```

---

## 디버깅 팁

```go
import "log"

func (n *Node) log(format string, args ...interface{}) {
    prefix := fmt.Sprintf("[%s term=%d state=%v] ", n.id, n.term, n.state)
    log.Printf(prefix+format, args...)
}

// 사용
n.log("received vote from %s", candidateID)
n.log("state changed: %v → %v", oldState, newState)
```
