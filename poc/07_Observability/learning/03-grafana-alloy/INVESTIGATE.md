# Ch03. Grafana Alloy - 점검 질문

## Q1. 통합 수집기가 없던 시절에 어떤 운영 문제가 있었는가?

**핵심 포인트**:
- 신호별 별도 에이전트(Promtail, OTel Collector, exporter) → 노드당 리소스 소모, 설정 파편화
- 설정 형식이 다르므로 운영 지식이 분산됨
- 장애 시 어느 수집기에서 막혔는지 추적이 어려움

## Q2. Alloy와 OTel Collector의 공통점과 차이점을 설명하라.

**핵심 포인트**:
- 공통: receive → process → export 파이프라인 아키텍처
- 차이: 설정 문법(YAML vs 컴포넌트 그래프), 생태계 통합(범용 vs Grafana 스택 특화)
- OTel Collector = 백엔드 무관 범용, Alloy = Grafana 스택 최적화

## Q3. 컴포넌트 그래프 모델이 OTel Collector의 YAML 설정보다 나은 점은?

**핵심 포인트**:
- 컴포넌트 간 `.output`/`.receiver` 참조로 데이터 흐름이 명시적
- OTel Collector는 `service.pipelines`에서 이름으로 연결 → 흐름 파악이 간접적
- 설정 파일만 읽으면 "이 데이터가 어디로 가는가"를 바로 알 수 있음

## Q4. 로그 파이프라인과 트레이스 파이프라인의 4단계(Discover→Process→Route→Export)를 실제 컴포넌트로 설명하라.

**핵심 포인트**:
- 로그: discovery.docker → discovery.relabel → loki.process → loki.write
- 트레이스: otelcol.receiver.otlp → otelcol.processor.batch/filter → otelcol.exporter.otlphttp
- 하나의 Alloy 프로세스 안에서 두 파이프라인이 나란히 존재, 각각 다른 백엔드로 라우팅

## Q5. Promtail에서 Alloy로의 전환이 "이름 변경"이 아닌 이유를 설명하라.

**핵심 포인트**:
- Promtail = 로그 전용 에이전트, Alloy = 로그+메트릭+트레이스 통합 수집기
- 수집 계층의 아키텍처가 전용→통합으로 전환된 것
- Promtail은 유지보수 모드, Alloy가 현재 표준

## Q6. Alloy 운영에서 백프레셔가 왜 가장 중요한 모니터링 포인트인가?

**핵심 포인트**:
- 백엔드가 느려지면 Alloy에 데이터가 쌓여 메모리 압박 → 최악의 경우 데이터 유실
- 핵심 지표: 입력량, 드롭 비율, exporter 큐 크기, 재시도 횟수
- 내장 UI(localhost:12345)에서 컴포넌트별 상태 실시간 확인 가능

## Q7. Alloy가 적합한 환경과 부적합한 환경을 구체적으로 구분하라.

**핵심 포인트**:
- 적합: Grafana 스택 사용자, K8s DaemonSet 배포, Promtail 마이그레이션
- 부적합: 비-Grafana 백엔드(Datadog, Elastic), 극도로 커스텀한 처리 로직(OTel Collector 확장성이 유리)
- 판단 기준: "백엔드가 Grafana 스택인가?"
