# INVESTIGATE: 실제 코드 분석

## 학습 목표
TPS 프로젝트의 실제 WebSocket 구현 코드를 분석하고, 프로덕션 환경에서의 고려사항을 이해합니다.

---

## 소크라테스 질문

### Q1. connectionTrigger 패턴

> PipelineRealTimeLogger에서 `connectionTrigger` 상태를 사용하는 이유는 무엇인가?

**생각해볼 점:**
- `shouldConnect` 옵션 대신 상태 값으로 연결을 제어하는 이유는?
- 특정 이벤트(예: 모달 열기)에서 연결을 시작해야 할 때 어떻게 구현하는가?
- 컴포넌트 생명주기와 WebSocket 연결의 관계는?

```typescript
// TPS 코드 예시
const [connectionTrigger, setConnectionTrigger] = useState(false);

// 모달 열릴 때
useEffect(() => {
  if (isOpen) {
    setConnectionTrigger(true);
  }
}, [isOpen]);

useWebSocket(connectionTrigger ? WS_URL : null);
```

---

### Q2. 구독 관리

> 실제 애플리케이션에서 다중 구독은 어떻게 관리하는가?

**생각해볼 점:**
- 여러 컴포넌트가 동시에 다른 토픽을 구독하면?
- 컴포넌트 언마운트 시 구독 해제는 어떻게?
- 전역 WebSocket 연결 vs 컴포넌트별 연결?

---

### Q3. 메모리 누수 방지

> WebSocket 관련 메모리 누수를 방지하려면 무엇을 신경 써야 하는가?

**생각해볼 점:**
- 컴포넌트 언마운트 시 정리해야 할 것들은?
- `useEffect` cleanup 함수에서 해야 할 작업은?
- 타이머, 이벤트 리스너 정리는?

---

### Q4. 테스트 전략

> WebSocket을 사용하는 컴포넌트는 어떻게 테스트하는가?

**생각해볼 점:**
- Mock WebSocket 서버를 어떻게 설정하는가?
- 연결 상태 변화에 따른 UI 테스트는?
- 메시지 수신/전송 테스트는?

---

### Q5. 프로덕션 고려사항

> 실제 서비스에서 WebSocket을 사용할 때 추가로 고려해야 할 점은?

**생각해볼 점:**
- 인증/인가 처리 (토큰 만료 시)
- 로드밸런서 sticky session
- 서버 배포 시 기존 연결 처리
- 모니터링 및 로깅

---

## 실제 코드 분석 대상

### 1. PipelineRealTimeLogger
파일 위치: `~/okestro/tps-gitlab/react-app/src/components/.../PipelineRealTimeLogger.tsx`

**분석 포인트:**
- 연결 트리거 조건
- 메시지 처리 로직
- 에러 처리 방식

### 2. 공통 WebSocket 훅 (있다면)
**분석 포인트:**
- 재사용 가능한 패턴
- 옵션 설계

---

## 다음 단계
위 질문들을 바탕으로 실제 코드를 분석하고, `LEARN.md`에 발견한 패턴과 인사이트를 정리합니다.
