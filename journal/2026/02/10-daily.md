# 학습 일지 - 2026-02-10 (월요일)

## 오늘의 목표
- [x] SSE + tmux 복습 퀴즈 15문제 진행

---

## 학습 내용

### SSE + tmux 복습 퀴즈 (15문제)
- **범위**: SSE Ch00~Ch08, tmux Ch01~Ch05
- **방식**: 1문제씩 깊이 파고들기 + 후속 질문

### 퀴즈 결과 요약

| 영역 | 결과 | 비고 |
|---|---|---|
| tmux 기본 (SIGHUP, 계층, detach) | △ | SIGHUP 시그널 새로 학습, Window/Pane 논리적·물리적 구분 혼동 |
| tmux + Claude Code 통합 | △ | Ctrl+B 충돌이 핵심 이유 (Vim만 기억) |
| SSE 기초/정의 | O | 단방향 + HTTP 기반 |
| EventSource API/인증 | O | polyfill 이름 약간 부정확 |
| 커스텀 이벤트 | △ | onmessage vs addEventListener 구분 혼동 후 교정 |
| 재연결 (Last-Event-ID) | △ | id:는 스트림 필드, Last-Event-ID는 HTTP 헤더 구분 필요 |
| 에러 처리 (readyState) | △ | CLOSED(2)를 정상 종료로 오해 → 치명적 에러임 |
| React 통합 | △ | isMountedRef 패턴 기억 못함 |
| **대규모 아키텍처** | **X** | Full Jitter, Sticky Session, TTL Jitter 전반 약함 |
| SSE vs WebSocket 선택 | O | 단방향이면 SSE, 양방향이면 WebSocket |

### 핵심 교정 사항
1. **SIGHUP**: SSH 끊기면 원격 셸에 SIGHUP 전달 → 자식 프로세스 연쇄 종료. tmux는 프로세스 트리 루트를 SSH에서 tmux server로 변경하여 해결
2. **Window vs Pane**: Window = 논리적 분리(탭), Pane = 물리적 분리(화면 분할)
3. **onmessage vs addEventListener**: event: 필드 없음 → onmessage, event: 필드 있음 → addEventListener
4. **Last-Event-ID**: 서버는 스트림에 `id:` 필드 포함, 클라이언트는 재연결 시 HTTP 헤더로 전달
5. **CLOSED(2)**: 정상 종료가 아니라 치명적 에러 → 수동 재연결 또는 polling fallback 필요
6. **isMountedRef**: 언마운트 후 setState 방지 가드 (AbortController와 역할 다름)
7. **Full Jitter**: 기본 백오프는 동시 재시도 폭주, Full Jitter는 0~ceiling 균등 분포로 분산
8. **Sticky Session**: 상태 저장 위치가 로컬 메모리면 필요, Redis면 불필요

---

## 복습 우선순위
- [ ] LEARNED.md 8번 섹션 (대규모 아키텍처) 재학습 - Full Jitter, 어댑티브 폴링, Sticky Session
- [ ] LEARNED.md 6번 섹션 (React 통합) 재학습 - isMountedRef + AbortController
- [ ] LEARNED.md 5번 섹션 (에러 처리) 재학습 - readyState CONNECTING vs CLOSED

---

## 내일 계획
- 복습 우선순위 항목 재학습
- 다음 학습 토픽 선정

---

## 회고

어제 실습으로 완료한 SSE 전체와 tmux를 복습 퀴즈로 점검했다. 기초 개념(SSE 정의, 단방향, HTTP 기반)은 잘 기억하고 있었지만, 대규모 아키텍처 패턴(Full Jitter, Sticky Session, TTL Jitter)은 거의 기억나지 않았다. 어제 직접 구현까지 했는데도 약한 것은, 코드를 짠 것과 개념을 설명할 수 있는 것이 다른 레벨의 이해라는 뜻이다. 해당 섹션을 다시 읽고 면접처럼 설명하는 연습이 필요하다.
