# Ch01. Observability Stack Overview - 점검 질문

## Q1. 수집기와 저장소를 왜 분리해서 이해해야 하는가?

**핵심 포인트**:
- 수집기는 ingress 계층이고 저장소는 persistence 계층이라는 점
- "데이터가 안 보인다"는 문제의 원인이 여러 층에 걸쳐 있다는 점
- 운영에서 병목과 장애 지점을 좁히려면 책임 분리가 필요하다는 점

## Q2. Alloy, Loki, Tempo의 역할을 각각 1분 안에 설명할 수 있는가?

**핵심 포인트**:
- Alloy는 수집, 처리, 라우팅
- Loki는 로그 저장 및 쿼리
- Tempo는 trace 저장 및 쿼리
- 셋을 혼동하지 않아야 함

## Q3. Monitoring과 Observability는 어떻게 다른가?

**핵심 포인트**:
- Monitoring은 미리 정의한 상태 감시
- Observability는 새로운 질문에 답할 수 있는 능력
- 실무에서는 둘이 함께 필요함

## Q4. Grafana는 저장소인가, UI인가?

**핵심 포인트**:
- Grafana는 기본적으로 visualization and exploration 계층
- Loki나 Tempo가 실제 저장 책임을 가짐
- 이 구분을 못 하면 장애 지점을 잘못 추적하게 됨

## Q5. 현재 PoC 자산에서 "수집기 역할"과 "저장소 역할"을 하는 것은 무엇인가?

**핵심 포인트**:
- `otel-collector-config.yaml`은 수집기/처리기 계층
- `jaeger`는 현재 trace backend
- 문서 학습의 목표는 이를 Alloy/Loki/Tempo 관점으로 재해석하는 것

## Q6. 왜 LGTM 조합이 운영 대화에서 자주 등장하는가?

**핵심 포인트**:
- Logs, Grafana, Traces, Metrics를 축약한 표현
- 저장소와 UI를 조합으로 사고하기 쉬움
- 팀 공통 언어가 되기 좋음
