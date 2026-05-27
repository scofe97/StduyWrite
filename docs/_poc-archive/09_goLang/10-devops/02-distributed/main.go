// 21-distributed-systems: Go로 배우는 분산 시스템
//
// 학습 목표:
// 1. 분산 시스템 핵심 개념 (CAP, 합의)
// 2. Leader Election 구현
// 3. Heartbeat 및 타임아웃 처리
// 4. 간단한 Raft 알고리즘 이해
//
// 참조:
// - https://www.youtube.com/watch?v=4awGzz9IhyQ (김수빈, 당근)
// - https://raft.github.io/

package main

import (
	"flag"
	"fmt"
	"log"
	"math/rand"
	"net"
	"net/rpc"
	"sync"
	"time"
)

// ============================================
// 1. 상태 정의
// ============================================

type State int

const (
	Follower State = iota
	Candidate
	Leader
)

func (s State) String() string {
	switch s {
	case Follower:
		return "Follower"
	case Candidate:
		return "Candidate"
	case Leader:
		return "Leader"
	default:
		return "Unknown"
	}
}

// ============================================
// 2. RPC 메시지 구조체
// ============================================

// RequestVoteArgs 투표 요청
type RequestVoteArgs struct {
	Term        int
	CandidateID string
}

// RequestVoteReply 투표 응답
type RequestVoteReply struct {
	Term        int
	VoteGranted bool
}

// AppendEntriesArgs Heartbeat / 로그 복제 요청
type AppendEntriesArgs struct {
	Term     int
	LeaderID string
	// TODO: 로그 복제용 필드 추가
}

// AppendEntriesReply Heartbeat / 로그 복제 응답
type AppendEntriesReply struct {
	Term    int
	Success bool
}

// ============================================
// 3. 노드 구조체
// ============================================

type Node struct {
	mu sync.Mutex

	// 기본 정보
	id    string
	port  string
	peers []string

	// Raft 상태
	state    State
	term     int
	votedFor string

	// 채널
	heartbeatCh chan struct{}
	voteCh      chan struct{}
}

// NewNode 새 노드 생성
func NewNode(id, port string, peers []string) *Node {
	return &Node{
		id:          id,
		port:        port,
		peers:       peers,
		state:       Follower,
		term:        0,
		votedFor:    "",
		heartbeatCh: make(chan struct{}, 10),
		voteCh:      make(chan struct{}, 10),
	}
}

// ============================================
// 4. RPC 서버/클라이언트
// ============================================

// StartServer RPC 서버 시작
func (n *Node) StartServer() error {
	// TODO: RPC 서버 등록 및 리스닝
	// 힌트:
	// rpc.Register(n)
	// listener, _ := net.Listen("tcp", ":"+n.port)
	// go rpc.Accept(listener)

	_ = rpc.Register  // 사용할 함수
	_ = net.Listen    // 사용할 함수

	log.Printf("[%s] RPC 서버 시작: :%s\n", n.id, n.port)
	return nil
}

// callPeer 피어에게 RPC 호출
func (n *Node) callPeer(peer, method string, args, reply interface{}) error {
	// TODO: RPC 클라이언트로 호출
	// 힌트:
	// client, _ := rpc.Dial("tcp", peer)
	// return client.Call(method, args, reply)

	_ = rpc.Dial // 사용할 함수
	_ = peer
	_ = method
	return nil
}

// ============================================
// 5. RPC 핸들러
// ============================================

// RequestVote 투표 요청 핸들러
func (n *Node) RequestVote(args *RequestVoteArgs, reply *RequestVoteReply) error {
	n.mu.Lock()
	defer n.mu.Unlock()

	// TODO: 투표 로직 구현
	// 1. args.Term < n.term 이면 거부
	// 2. args.Term > n.term 이면 term 업데이트, Follower로
	// 3. 아직 투표 안 했거나 같은 후보면 투표

	reply.Term = n.term
	reply.VoteGranted = false

	log.Printf("[%s] RequestVote from %s (term=%d)\n", n.id, args.CandidateID, args.Term)

	return nil
}

// AppendEntries Heartbeat/로그복제 핸들러
func (n *Node) AppendEntries(args *AppendEntriesArgs, reply *AppendEntriesReply) error {
	n.mu.Lock()
	defer n.mu.Unlock()

	// TODO: Heartbeat 처리
	// 1. args.Term < n.term 이면 거부
	// 2. 유효한 Leader로부터 받으면 Follower로 전환
	// 3. heartbeatCh에 신호 보내기

	reply.Term = n.term
	reply.Success = false

	log.Printf("[%s] AppendEntries from %s (term=%d)\n", n.id, args.LeaderID, args.Term)

	return nil
}

// ============================================
// 6. 상태별 로직
// ============================================

// electionTimeout 랜덤 선거 타임아웃 (150~300ms)
func electionTimeout() time.Duration {
	return time.Duration(150+rand.Intn(150)) * time.Millisecond
}

// runFollower Follower 상태 실행
func (n *Node) runFollower() {
	log.Printf("[%s] 상태: Follower\n", n.id)

	// TODO: Follower 로직
	// 1. 타이머 설정 (electionTimeout)
	// 2. heartbeatCh 받으면 타이머 리셋
	// 3. 타임아웃 시 Candidate로 전환

	timeout := electionTimeout()
	timer := time.NewTimer(timeout)
	defer timer.Stop()

	for {
		select {
		case <-n.heartbeatCh:
			// TODO: 타이머 리셋
			_ = timer

		case <-n.voteCh:
			// TODO: 타이머 리셋

		case <-timer.C:
			// TODO: Candidate로 전환
			log.Printf("[%s] 타임아웃! 선거 시작\n", n.id)
			return
		}
	}
}

// runCandidate Candidate 상태 실행
func (n *Node) runCandidate() {
	log.Printf("[%s] 상태: Candidate\n", n.id)

	// TODO: Candidate 로직
	// 1. term 증가
	// 2. 자신에게 투표
	// 3. 모든 피어에게 RequestVote 전송
	// 4. 과반수 득표 시 Leader로
	// 5. 타임아웃 시 새 선거

	n.mu.Lock()
	n.term++
	n.votedFor = n.id
	currentTerm := n.term
	n.mu.Unlock()

	votes := 1 // 자기 자신
	_ = votes
	_ = currentTerm

	log.Printf("[%s] term %d로 선거 시작\n", n.id, currentTerm)

	// TODO: 피어들에게 투표 요청
	// for _, peer := range n.peers { ... }
}

// runLeader Leader 상태 실행
func (n *Node) runLeader() {
	log.Printf("[%s] 상태: Leader ★\n", n.id)

	// TODO: Leader 로직
	// 1. 주기적으로 Heartbeat 전송 (50ms)
	// 2. 클라이언트 요청 처리
	// 3. 더 높은 term 발견 시 Follower로

	ticker := time.NewTicker(50 * time.Millisecond)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			// TODO: sendHeartbeats() 호출
			log.Printf("[%s] Heartbeat 전송\n", n.id)
		}
	}
}

// sendHeartbeats 모든 피어에게 Heartbeat 전송
func (n *Node) sendHeartbeats() {
	// TODO: 모든 피어에게 AppendEntries 전송
	// for _, peer := range n.peers { ... }
}

// ============================================
// 7. 메인 루프
// ============================================

// Run 노드 실행
func (n *Node) Run() {
	for {
		n.mu.Lock()
		state := n.state
		n.mu.Unlock()

		switch state {
		case Follower:
			n.runFollower()
		case Candidate:
			n.runCandidate()
		case Leader:
			n.runLeader()
		}
	}
}

// ============================================
// Main
// ============================================

func main() {
	id := flag.String("id", "node1", "노드 ID")
	port := flag.String("port", "8001", "RPC 포트")
	peersStr := flag.String("peers", "localhost:8002,localhost:8003", "피어 목록 (쉼표 구분)")
	flag.Parse()

	// 피어 목록 파싱
	var peers []string
	if *peersStr != "" {
		for _, p := range splitPeers(*peersStr) {
			peers = append(peers, p)
		}
	}

	fmt.Println("=== 21. Go로 배우는 분산 시스템 ===\n")
	fmt.Printf("노드 ID: %s\n", *id)
	fmt.Printf("포트: %s\n", *port)
	fmt.Printf("피어: %v\n\n", peers)

	// 노드 생성 및 실행
	node := NewNode(*id, *port, peers)

	if err := node.StartServer(); err != nil {
		log.Fatalf("서버 시작 실패: %v", err)
	}

	fmt.Println("📌 TODO 주석을 채워서 분산 시스템을 완성하세요!")
	fmt.Println("📺 참조: https://www.youtube.com/watch?v=4awGzz9IhyQ\n")

	// 메인 루프 시작
	node.Run()
}

func splitPeers(s string) []string {
	var result []string
	current := ""
	for _, c := range s {
		if c == ',' {
			if current != "" {
				result = append(result, current)
			}
			current = ""
		} else {
			current += string(c)
		}
	}
	if current != "" {
		result = append(result, current)
	}
	return result
}
