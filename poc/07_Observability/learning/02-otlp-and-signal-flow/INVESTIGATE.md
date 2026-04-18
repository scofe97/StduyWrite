# Ch02. OTLP and Signal Flow - 점검 질문

## Q1. 왜 OTLP를 "전송 포맷"보다 "수집 계층 계약"으로 이해하는 편이 더 정확한가?

**핵심 포인트**:
- signal, data model, transport를 함께 규정함
- collector가 이해할 수 있는 공통 ingress를 제공함
- backend와 애플리케이션 사이의 결합을 낮춤

## Q2. OTLP/gRPC와 OTLP/HTTP는 무엇이 다르고, 어떤 환경에서 각각 더 현실적인가?

**핵심 포인트**:
- 기본 관례 포트는 `4317`, `4318`
- 서버 간 통신과 프록시/HTTP 친화 환경의 차이
- 성능만이 아니라 네트워크 제약까지 함께 봐야 함

## Q3. Resource가 없으면 로그와 트레이스 상관분석이 왜 어려워지는가?

**핵심 포인트**:
- `service.name`, `deployment.environment` 같은 구분 기준이 사라짐
- 본문만으로는 출처를 식별하기 어려움
- 공통 문맥이 약해져 분석 비용이 커짐

## Q4. Span은 "로그 한 줄"과 무엇이 다른가?

**핵심 포인트**:
- 작업 단위와 시간 범위를 표현함
- 부모/자식 관계를 가질 수 있음
- 병목과 호출 구조를 드러냄

## Q5. "앱 -> collector -> backend" 구조에서 collector가 담당하는 책임은 무엇인가?

**핵심 포인트**:
- receive, process, export
- filter, batch, sampling, transform 적용
- backend 변경 시 애플리케이션 설정 흔들림을 줄임

## Q6. 현재 PoC의 `receiver -> tail sampling -> exporter -> Jaeger` 흐름은 왜 OTLP 학습에 중요한가?

**핵심 포인트**:
- collector 중심 사고방식을 이미 경험하고 있음
- backend보다 ingress와 processing 계층 이해가 더 중요함
- 이후 Alloy + Tempo 구조로 자연스럽게 확장 가능함

## Q7. OTLP가 저장소도 아니고 시각화 도구도 아니라면, 정확히 무엇인가?

**핵심 포인트**:
- telemetry를 전달하는 표준 프로토콜
- 데이터 모델과 전송 규약의 조합
- 저장과 조회 책임은 backend가 가짐
