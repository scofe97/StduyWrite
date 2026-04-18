# Ch10. Sampling Strategies - 점검 질문

## Q1. 샘플링과 필터링의 차이는 무엇인가?

**핵심 포인트**:
- 샘플링은 대표성 유지, 필터링은 대표성 손실
- 샘플링은 전체를 대표하도록 선택
- 필터링은 특정 조건만 남김

## Q2. Head Sampling으로 에러 trace 100% 캡처가 불가능한 이유는 무엇인가?

**핵심 포인트**:
- 결정 시점에 trace 내용을 알 수 없음
- Trace ID 해시 기반 확률 결정
- 에러 발생 여부는 trace 완료 후에야 확정

## Q3. Tail Sampling의 decision_wait를 너무 짧게 설정하면 어떤 문제가 생기는가?

**핵심 포인트**:
- 불완전한 trace로 잘못된 결정
- 늦게 도착한 span 누락
- 에러 span이 decision_wait 이후 도착하면 정상으로 판정

## Q4. 고볼륨 환경에서 Head + Tail 조합을 쓰는 이유는 무엇인가?

**핵심 포인트**:
- Tail Sampler의 메모리/리소스 부담 감소
- Head로 1차 필터 후 Tail로 정교한 판단
- Tail Sampler 병목 방지

## Q5. 현재 PoC의 tail_sampling 정책 세 개가 어떤 순서로 평가되는가?

**핵심 포인트**:
- errors → latency → probabilistic 순서
- 하나라도 만족하면 기록
- "에러는 전부, 느린 건 전부, 나머지는 10%" 전략
