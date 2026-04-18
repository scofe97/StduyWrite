package workflow

import (
	"fmt"
	"time"

	"github.com/looplab/fsm"
)

// 상태 상수
const (
	StateDraft     = "draft"
	StatePublished = "published"
	StateArchived  = "archived"
)

// 이벤트 상수
const (
	EventPublish   = "publish"
	EventArchive   = "archive"
	EventRepublish = "republish"
)

// Post는 게시글 엔티티입니다.
type Post struct {
	ID        int64
	Title     string
	Content   string
	Author    string
	FSM       *fsm.FSM
	UpdatedAt time.Time
}

// NewPost는 새 게시글 상태 기계를 생성합니다.
// TODO: FSM 초기화 구현
func NewPost(id int64, title string) *Post {
	p := &Post{
		ID:        id,
		Title:     title,
		UpdatedAt: time.Now(),
	}

	// TODO: FSM 생성
	// p.FSM = fsm.NewFSM(
	//     StateDraft,  // 초기 상태
	//     fsm.Events{
	//         // 이벤트 정의: {Name, Src, Dst}
	//         {Name: EventPublish, Src: []string{StateDraft}, Dst: StatePublished},
	//         {Name: EventArchive, Src: []string{StatePublished}, Dst: StateArchived},
	//         {Name: EventRepublish, Src: []string{StateArchived}, Dst: StatePublished},
	//     },
	//     fsm.Callbacks{
	//         // 콜백 등록
	//         "before_event":        p.beforeEvent,
	//         "after_event":         p.afterEvent,
	//         "enter_published":     p.onEnterPublished,
	//         "leave_published":     p.onLeavePublished,
	//     },
	// )

	return p
}

// State는 현재 상태를 반환합니다.
func (p *Post) State() string {
	if p.FSM == nil {
		return StateDraft
	}
	return p.FSM.Current()
}

// Can은 특정 전이가 가능한지 확인합니다.
func (p *Post) Can(event string) bool {
	if p.FSM == nil {
		return false
	}
	return p.FSM.Can(event)
}

// AvailableTransitions는 현재 상태에서 가능한 전이 목록을 반환합니다.
func (p *Post) AvailableTransitions() []string {
	if p.FSM == nil {
		return nil
	}
	return p.FSM.AvailableTransitions()
}

// Publish는 게시글을 발행합니다.
// TODO: 발행 메서드 구현
func (p *Post) Publish() error {
	if p.FSM == nil {
		return fmt.Errorf("FSM not initialized")
	}
	// 힌트: p.FSM.Event(EventPublish)
	return nil
}

// Archive는 게시글을 보관합니다.
// TODO: 보관 메서드 구현
func (p *Post) Archive() error {
	if p.FSM == nil {
		return fmt.Errorf("FSM not initialized")
	}
	// 힌트: p.FSM.Event(EventArchive)
	return nil
}

// Republish는 보관된 게시글을 재발행합니다.
// TODO: 재발행 메서드 구현
func (p *Post) Republish() error {
	if p.FSM == nil {
		return fmt.Errorf("FSM not initialized")
	}
	// 힌트: p.FSM.Event(EventRepublish)
	return nil
}

// SetState는 상태를 직접 설정합니다 (DB에서 로드 시 사용).
// TODO: 외부 상태 설정 구현
func (p *Post) SetState(state string) error {
	if p.FSM == nil {
		return fmt.Errorf("FSM not initialized")
	}
	// 힌트: p.FSM.SetState(state)
	return nil
}

// --- 콜백 함수들 ---

// beforeEvent는 모든 이벤트 전에 호출됩니다.
func (p *Post) beforeEvent(e *fsm.Event) {
	fmt.Printf("[Before] %s: %s → %s\n", e.Event, e.Src, e.Dst)
}

// afterEvent는 모든 이벤트 후에 호출됩니다.
func (p *Post) afterEvent(e *fsm.Event) {
	p.UpdatedAt = time.Now()
	fmt.Printf("[After] %s: now %s\n", e.Event, e.Dst)
}

// onEnterPublished는 published 상태 진입 시 호출됩니다.
func (p *Post) onEnterPublished(e *fsm.Event) {
	fmt.Printf("[Enter Published] Post '%s' is now public!\n", p.Title)
	// TODO: 알림 발송, 캐시 갱신 등
}

// onLeavePublished는 published 상태를 떠날 때 호출됩니다.
func (p *Post) onLeavePublished(e *fsm.Event) {
	fmt.Printf("[Leave Published] Post '%s' is no longer public\n", p.Title)
}
