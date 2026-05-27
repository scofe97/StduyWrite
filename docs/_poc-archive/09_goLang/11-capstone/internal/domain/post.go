package domain

import (
	"fmt"
	"time"

	"github.com/looplab/fsm"
)

// 상태 상수
const (
	StatusDraft     = "draft"
	StatusPublished = "published"
	StatusArchived  = "archived"
)

// 이벤트 상수
const (
	EventPublish   = "publish"
	EventArchive   = "archive"
	EventRepublish = "republish"
)

// Post는 게시글 도메인 엔티티입니다.
type Post struct {
	ID        int64
	Title     string
	Content   string
	Status    string
	Author    string
	CreatedAt time.Time
	UpdatedAt time.Time
	fsm       *fsm.FSM
}

// NewPost는 새 게시글을 생성합니다.
func NewPost(title, content, author string) *Post {
	p := &Post{
		Title:     title,
		Content:   content,
		Status:    StatusDraft,
		Author:    author,
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}
	p.initFSM()
	return p
}

// FromRepository는 저장소에서 로드한 데이터로 Post를 생성합니다.
func FromRepository(id int64, title, content, status, author string, createdAt, updatedAt time.Time) *Post {
	p := &Post{
		ID:        id,
		Title:     title,
		Content:   content,
		Status:    status,
		Author:    author,
		CreatedAt: createdAt,
		UpdatedAt: updatedAt,
	}
	p.initFSM()
	p.fsm.SetState(status)
	return p
}

// initFSM은 FSM을 초기화합니다.
func (p *Post) initFSM() {
	p.fsm = fsm.NewFSM(
		StatusDraft,
		fsm.Events{
			{Name: EventPublish, Src: []string{StatusDraft}, Dst: StatusPublished},
			{Name: EventArchive, Src: []string{StatusPublished}, Dst: StatusArchived},
			{Name: EventRepublish, Src: []string{StatusArchived}, Dst: StatusPublished},
		},
		fsm.Callbacks{
			"after_event": func(e *fsm.Event) {
				p.Status = e.Dst
				p.UpdatedAt = time.Now()
			},
		},
	)
}

// Publish는 게시글을 발행합니다.
func (p *Post) Publish() error {
	if err := p.fsm.Event(EventPublish); err != nil {
		return fmt.Errorf("cannot publish: %w", err)
	}
	return nil
}

// Archive는 게시글을 보관합니다.
func (p *Post) Archive() error {
	if err := p.fsm.Event(EventArchive); err != nil {
		return fmt.Errorf("cannot archive: %w", err)
	}
	return nil
}

// Republish는 보관된 게시글을 재발행합니다.
func (p *Post) Republish() error {
	if err := p.fsm.Event(EventRepublish); err != nil {
		return fmt.Errorf("cannot republish: %w", err)
	}
	return nil
}

// CanPublish는 발행 가능 여부를 반환합니다.
func (p *Post) CanPublish() bool {
	return p.fsm.Can(EventPublish)
}

// CanArchive는 보관 가능 여부를 반환합니다.
func (p *Post) CanArchive() bool {
	return p.fsm.Can(EventArchive)
}

// CanRepublish는 재발행 가능 여부를 반환합니다.
func (p *Post) CanRepublish() bool {
	return p.fsm.Can(EventRepublish)
}
