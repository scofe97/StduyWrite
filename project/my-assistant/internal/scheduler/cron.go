package scheduler

import (
	"fmt"
	"log"

	"github.com/robfig/cron/v3"

	"my-assistant/internal/store"
)

// Scheduler manages cron-based reminders and fires notifications.
type Scheduler struct {
	cron     *cron.Cron
	store    *store.Store
	notifyFn func(chatID int64, message string)
}

// New creates a new Scheduler. notifyFn is called when a reminder fires.
func New(s *store.Store, notifyFn func(int64, string)) *Scheduler {
	c := cron.New(cron.WithSeconds()) // Support 6-field cron with seconds
	return &Scheduler{
		cron:     c,
		store:    s,
		notifyFn: notifyFn,
	}
}

// Start loads all active reminders from the store and begins scheduling.
func (s *Scheduler) Start() error {
	reminders, err := s.store.GetActiveReminders()
	if err != nil {
		return fmt.Errorf("활성 알림 로드 실패: %w", err)
	}

	for _, r := range reminders {
		s.Register(r.ID, r.CronExpr)
	}

	s.cron.Start()
	log.Printf("scheduler: started with %d active reminder(s)", len(reminders))
	return nil
}

// Register adds a cron job for the given reminder ID and cron expression.
// It is safe to call while the scheduler is running.
func (s *Scheduler) Register(reminderID int64, cronExpr string) {
	_, err := s.cron.AddFunc(cronExpr, s.buildJob(reminderID))
	if err != nil {
		log.Printf("scheduler: failed to register reminder %d with expr %q: %v", reminderID, cronExpr, err)
		return
	}
	log.Printf("scheduler: registered reminder %d (%s)", reminderID, cronExpr)
}

// Stop gracefully stops the cron scheduler.
func (s *Scheduler) Stop() {
	ctx := s.cron.Stop()
	<-ctx.Done()
	log.Println("scheduler: stopped")
}

// buildJob returns a cron job function for the given reminder ID.
func (s *Scheduler) buildJob(reminderID int64) func() {
	return func() {
		reminders, err := s.store.GetActiveReminders()
		if err != nil {
			log.Printf("scheduler: error fetching reminders for job %d: %v", reminderID, err)
			return
		}

		var target *store.Reminder
		for i := range reminders {
			if reminders[i].ID == reminderID {
				target = &reminders[i]
				break
			}
		}

		if target == nil {
			// Reminder was deactivated; nothing to do.
			return
		}

		// Fire the notification.
		if s.notifyFn != nil {
			s.notifyFn(target.ChatID, target.Message)
		}

		// Handle one-shot: deactivate after firing.
		if target.OneShot {
			if err := s.store.DeactivateReminder(reminderID); err != nil {
				log.Printf("scheduler: failed to deactivate one-shot reminder %d: %v", reminderID, err)
			} else {
				log.Printf("scheduler: one-shot reminder %d fired and deactivated", reminderID)
			}
			return
		}

		log.Printf("scheduler: reminder %d fired for chat %d", reminderID, target.ChatID)
	}
}
