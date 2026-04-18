# 학습 일지 - 2026-02-09 (일요일)

## 오늘의 목표
- [x] SSE 프로젝트 Ch04~Ch06 TODO 실습 완료
- [x] SSE 프로젝트 Ch08 TODO 실습 완료
- [x] 통합 React 앱 정리 (TODO 마커 제거, 배지 업데이트)

---

## 학습 내용

### SSE Ch04: Reconnection (useSSEWithRecovery)
- **경로**: `poc/06_Frontend/09-sse/practice/react-app/src/hooks/ch04/`
- **핵심 배움**:
  - EventSourcePolyfill로 커스텀 헤더(Authorization) + heartbeatTimeout 설정
  - Last-Event-ID를 useRef로 관리하여 재연결 시 서버에 전달 → 이벤트 유실 방지
  - onerror에서 수동 재연결: maxRetries 제한 + exponential backoff
  - onopen에서 reconnectCount 리셋하여 성공 시 카운터 초기화

### SSE Ch05: Error Handling (useSSEWithErrorHandling)
- **경로**: `poc/06_Frontend/09-sse/practice/react-app/src/hooks/ch05/`
- **핵심 배움**:
  - 연결 상태 머신: connecting → connected → error → disconnected → fallback-polling
  - readyState 기반 에러 판단 (CONNECTING=일시적, CLOSED=치명적)
  - heartbeat 타임아웃 감지: setInterval로 마지막 이벤트 시간 체크
  - SSE 실패 시 polling fallback 자동 전환

### SSE Ch06: React Integration (useSSEWithCleanup)
- **경로**: `poc/06_Frontend/09-sse/practice/react-app/src/hooks/ch06/`
- **핵심 배움**:
  - AbortController + useRef로 연결 생명주기 관리
  - isMountedRef로 언마운트 후 setState 방지
  - React 18 Strict Mode 대응: mount → unmount → remount 시뮬레이션에서 안전하게 동작
  - useCallback으로 connect/disconnect 메모이제이션, 의존성 배열 최적화

### SSE Ch08: 대규모 아키텍처 (useAdaptivePolling)
- **경로**: `poc/06_Frontend/09-sse/practice/react-app/src/hooks/ch08/`
- **핵심 배움**:
  - Full Jitter (AWS 권장): `random(0, min(ceiling, base * 2^attempt))` — 0부터 균등 분포로 요청 분산
  - 기본 지수 백오프 vs Full Jitter: base만큼 항상 대기 vs 0부터 분산 (thundering herd 방지)
  - 서버 TTL ± 20% Jitter: 동일 TTL 받은 클라이언트들의 동시 요청 방지
  - 어댑티브 폴링: 서버가 position 기반 TTL로 클라이언트 폴링 주기를 제어

### LEARN.md 문서 보강
- **경로**: `poc/06_Frontend/09-sse/learning/08-large-scale-architecture/LEARN.md`
- **추가 내용**:
  - WebSocket vs SSE 연결 비용 비교 (핸드셰이크, 버퍼, heartbeat, 로드밸런서, 프록시)
  - 재연결 시 같은 서버 필요 여부 분석 (상태 저장 위치에 따른 Sticky Session 결정)

---

## 복습 완료
- [ ] (아직 복습 항목 없음)

---

## 내일 계획
- SSE 프로젝트 LEARNED.md 기반 면접 대비 복습
- 다음 학습 토픽 선정

---

## 회고

SSE 학습 프로젝트의 실습 파트를 모두 완료했습니다. Ch02~Ch06, Ch08까지 통합 React 앱에서 실습 훅을 직접 구현하고, 각 챕터의 핵심 패턴을 체험했습니다.

가장 인상 깊었던 것은 **Full Jitter**입니다. 단순 지수 백오프는 base만큼 항상 대기하기 때문에 같은 시점에 실패한 클라이언트들이 여전히 몰리지만, Full Jitter는 0부터 ceiling까지 균등 분포하여 시간축에 골고루 분산시킵니다. AWS가 권장하는 이유를 코드로 직접 구현하며 이해했습니다.

또한 React 18 Strict Mode에서 isMountedRef 패턴의 중요성을 체감했습니다. mount → unmount → remount 시뮬레이션에서 AbortController + isMountedRef 없이는 좀비 연결과 메모리 누수가 발생합니다.
