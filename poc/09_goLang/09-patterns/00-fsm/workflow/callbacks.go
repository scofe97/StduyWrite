package workflow

import (
	"fmt"
	"time"

	"github.com/looplab/fsm"
)

// --- 고급 콜백 패턴 ---

// ValidationCallback은 전이 전 유효성 검사를 수행합니다.
// TODO: 유효성 검사 콜백 구현
func ValidationCallback(e *fsm.Event) {
	// 힌트: e.Cancel()로 전이 취소 가능
	// e.Err에 에러 설정 가능

	// 예: 특정 조건에서만 전이 허용
	// post := e.FSM.Metadata("post").(*Post)
	// if post.Content == "" {
	//     e.Cancel(fmt.Errorf("cannot publish empty post"))
	// }
}

// LoggingCallback은 상태 변경을 로깅합니다.
// TODO: 로깅 콜백 구현
func LoggingCallback(e *fsm.Event) {
	timestamp := time.Now().Format(time.RFC3339)
	fmt.Printf("[%s] State transition: %s → %s (event: %s)\n",
		timestamp, e.Src, e.Dst, e.Event)
}

// MetricsCallback은 상태 변경 메트릭을 수집합니다.
// TODO: 메트릭 수집 콜백 구현
func MetricsCallback(e *fsm.Event) {
	// 힌트: 프로메테우스, statsd 등에 메트릭 전송
	// metrics.Counter("state_transition_total").Inc()
	// metrics.Histogram("state_transition_duration").Observe(duration)
}

// --- 이벤트별 콜백 ---

// BeforePublish는 발행 전에 호출됩니다.
func BeforePublish(e *fsm.Event) {
	fmt.Println("[BeforePublish] Validating content...")

	// 콘텐츠 검증 로직
	// post := e.Args[0].(*Post)
	// if len(post.Content) < 10 {
	//     e.Cancel(fmt.Errorf("content too short"))
	// }
}

// AfterPublish는 발행 후에 호출됩니다.
func AfterPublish(e *fsm.Event) {
	fmt.Println("[AfterPublish] Publishing complete!")

	// 후처리 로직
	// - 검색 인덱스 업데이트
	// - 캐시 갱신
	// - 알림 발송
}

// BeforeArchive는 보관 전에 호출됩니다.
func BeforeArchive(e *fsm.Event) {
	fmt.Println("[BeforeArchive] Preparing to archive...")
}

// AfterArchive는 보관 후에 호출됩니다.
func AfterArchive(e *fsm.Event) {
	fmt.Println("[AfterArchive] Post archived!")

	// 후처리 로직
	// - 검색 인덱스에서 제거
	// - 캐시 무효화
}

// --- 상태 진입/퇴장 콜백 ---

// EnterState는 특정 상태에 진입할 때 호출됩니다.
func EnterState(state string) fsm.Callback {
	return func(e *fsm.Event) {
		fmt.Printf("[Enter %s] Entering state\n", state)
	}
}

// LeaveState는 특정 상태를 떠날 때 호출됩니다.
func LeaveState(state string) fsm.Callback {
	return func(e *fsm.Event) {
		fmt.Printf("[Leave %s] Leaving state\n", state)
	}
}

// --- 조건부 콜백 ---

// ConditionalCallback은 조건에 따라 다른 동작을 수행합니다.
func ConditionalCallback(condition func(*fsm.Event) bool, action func(*fsm.Event)) fsm.Callback {
	return func(e *fsm.Event) {
		if condition(e) {
			action(e)
		}
	}
}

// --- 콜백 체인 ---

// ChainCallbacks는 여러 콜백을 순서대로 실행합니다.
func ChainCallbacks(callbacks ...fsm.Callback) fsm.Callback {
	return func(e *fsm.Event) {
		for _, cb := range callbacks {
			cb(e)
			// 에러 발생 시 중단
			if e.Err != nil {
				return
			}
		}
	}
}

// --- 비동기 콜백 (주의: FSM은 동기 처리 권장) ---

// AsyncCallback은 비동기 작업을 시작합니다 (완료 대기 안 함).
func AsyncCallback(action func(*fsm.Event)) fsm.Callback {
	return func(e *fsm.Event) {
		go func() {
			// 주의: 에러 처리 필요
			defer func() {
				if r := recover(); r != nil {
					fmt.Printf("Async callback panic: %v\n", r)
				}
			}()
			action(e)
		}()
	}
}

// --- 재시도 콜백 ---

// RetryCallback은 실패 시 재시도합니다.
func RetryCallback(maxRetries int, delay time.Duration, action func(*fsm.Event) error) fsm.Callback {
	return func(e *fsm.Event) {
		var lastErr error
		for i := 0; i < maxRetries; i++ {
			if err := action(e); err == nil {
				return
			} else {
				lastErr = err
				time.Sleep(delay)
			}
		}
		e.Err = fmt.Errorf("failed after %d retries: %w", maxRetries, lastErr)
	}
}
