# INVESTIGATE: SNAPSHOT/DELTA 메시지 패턴

## 학습 목표
효율적인 실시간 데이터 동기화를 위한 SNAPSHOT/DELTA 패턴을 이해합니다.

---

## 소크라테스 질문

### Q1. SNAPSHOT vs DELTA

> SNAPSHOT과 DELTA를 분리하는 이유는 무엇인가?

**생각해볼 점:**
- 모든 메시지를 SNAPSHOT으로 보내면 어떤 문제가 생기는가?
- 모든 메시지를 DELTA로만 보내면 어떤 문제가 생기는가?
- 언제 SNAPSHOT이 필요하고 언제 DELTA가 필요한가?

```typescript
// SNAPSHOT: 전체 상태
{ type: 'SNAPSHOT', data: [item1, item2, item3, ...] }

// DELTA: 변경된 부분만
{ type: 'DELTA', data: { id: 1, changes: { status: 'completed' } } }
```

---

### Q2. 상태 동기화 전략

> DELTA로 기존 상태를 업데이트할 때 주의해야 할 점은 무엇인가?

**생각해볼 점:**
- DELTA가 순서대로 도착하지 않으면?
- DELTA를 적용하려는데 해당 항목이 없으면?
- 네트워크 지연으로 DELTA가 누락되면?

---

### Q3. 메시지 타입 설계

> 실시간 애플리케이션에서 어떤 메시지 타입이 필요한가?

**생각해볼 점:**
- CRUD(Create, Read, Update, Delete) 각각에 대응하는 메시지는?
- ACK(확인응답) 메시지가 필요한 경우는?
- 에러 메시지는 어떻게 처리해야 하는가?

---

### Q4. 낙관적 업데이트

> DELTA 전송 시 낙관적 업데이트(Optimistic Update)를 적용해야 하는가?

**생각해볼 점:**
- 서버 응답을 기다리는 동안 UI를 어떻게 처리해야 하는가?
- 낙관적 업데이트 후 서버에서 실패 응답이 오면?
- WebSocket과 낙관적 업데이트의 조합은 HTTP와 다른가?

---

## 다음 단계
질문에 대한 답을 찾았다면 `LEARN.md`에 정리하고, `practice/` 폴더에서 실습합니다.
