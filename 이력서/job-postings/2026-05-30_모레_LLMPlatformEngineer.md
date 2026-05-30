# 모레 — LLM Platform Engineer

## Meta
- 회사: 모레 (Moreh, AI 인프라/LLM 플랫폼)
- 포지션: LLM Platform Engineer
- URL: https://www.wanted.co.kr/wd/328144
- 접수일: 상시채용
- 출처: 원티드
- 기록일: 2026-05-30

## 기술 스택
**필수**: Kubernetes(커스텀 오퍼레이터 개발), Go / Python / Rust, OpenTelemetry
**우대**: 본문 정보 부족 — 본인 확인 필요 (공고에 별도 우대사항 섹션 없음)

## 주요 업무
- Performance Gateway 개발 — 사용자 요청과 클러스터 상태를 실시간 분석해 disaggregated inference·prefix-cache 라우팅하는 지능형 게이트웨이 구축
- Inference Autopilot 개발 — 프리셋 기반으로 추론 서비스를 관리하고 트래픽·클러스터 상태에 따라 스케일하는 오퍼레이터 제작
- High-Fidelity Observability — OpenTelemetry로 분산 환경 오류 탐지 모니터링 파이프라인 구축
- AI-Native 개발 — 설계부터 검증까지 개발 프로세스에 AI 에이전트 통합

## 자격 요건·우대사항
**자격 요건**
- 컴퓨터공학 혹은 관련 전공 학부 졸업 (또는 동등 경험)
- Cloud Native: Kubernetes 운영 및 커스텀 오퍼레이터 개발 2년 이상
- Go, Python, 또는 Rust 프로그래밍 역량
- 테스트·CI/CD 자동화를 포함한 강한 엔지니어링 오너십
- 팀 협업 역량 (전체 경력 2~10년)

**우대사항**
- 본문 정보 부족 — 본인 확인 필요

## 매칭 분석 (vs 지원자)
**강점 (어필 가능한 마일스톤)**
- **Kubernetes 운영 + CKA**: 개인 GCP 3노드 K8s 자가호스팅 + CKA → "Kubernetes 운영 2년 이상" 직접 매칭
- **관찰성(OpenTelemetry)**: 개인 GCP에 Grafana·Loki·Tempo OpenTelemetry 자가 구성 → "High-Fidelity Observability" 정확 매칭(드문 직접 일치)
- **Python**: 운영 자동화·스크립팅에 사용 → Go/Python 중 Python 측 매칭
- **CI/CD 자동화 오너십**: Jenkins 파이프라인 실행엔진 + GitOps 자동화 경험 → "테스트·CI/CD 자동화 오너십" 정합
- **AI-Native 개발 정합**: 본인 Claude Code·OMC 멀티에이전트 운영 경험 = "AI 에이전트를 개발 프로세스에 통합" 우대 보강 가능
- **이벤트드리븐·동시성 사고**: Performance Gateway의 실시간 라우팅·스케일링은 이벤트드리븐·동시성 직렬화 사고와 정합

**공백**
- **커스텀 K8s 오퍼레이터 개발 경험 부재** (핵심 요건) — 본인은 K8s 운영자(operator로서의 사용)이지 controller-runtime 기반 Operator 개발 경험은 없음. 이게 가장 큰 갭
- **Go 실무 경험 부족** — 오퍼레이터/게이트웨이는 사실상 Go 중심. 본인 주력은 Java/Spring. Go 학습 필요 (JVM외 언어 공백, 단 본인 우선순위는 하향)
- **LLM 추론 인프라 도메인 생소** — disaggregated inference·prefix-cache는 LLM 서빙 특화 개념. 도메인 학습 필요
- **Rust 무경험** — 선택지 중 하나라 필수는 아님

**매칭 신뢰도**: 중 — K8s 운영·OpenTelemetry는 강한 직접 매칭이고 AI-Native 정합이 차별점이나, 핵심인 "커스텀 오퍼레이터 개발 2년"과 Go 실무가 본인 이력에 비어 있어 어필 각도가 운영·관찰성·AI에 한정됨

## 도메인 한 줄 + 예상 기술부채
**도메인**: LLM 추론 인프라/플랫폼. 클러스터 상태 기반 지능형 라우팅과 추론 오토스케일을 자체 개발하는 AI 인프라 조직.
**예상 기술부채 2~3개**
1. **분산 추론 환경의 오류 가시성 부족** — disaggregated inference는 노드 간 의존이 복잡해 장애 원인 추적이 어려움. OpenTelemetry 트레이스 표준화로 분산 추적 회로 구축 가능 (개인 Tempo 운영 경험 직접 전이)
2. **오퍼레이터 기반 스케일링의 동시성·경합** — Inference Autopilot이 트래픽 따라 스케일하면 스케일 결정의 경합·중복 실행 위험. 본인 동시성 직렬화(비관적 락)·멱등 사고로 스케일 게이트 설계 가능
3. **AI 에이전트 통합 개발 프로세스의 신뢰성** — AI-Native 개발은 검증 게이트 부재 시 회귀 위험. 본인 OMC verifier·적대적 검증 운영 경험으로 검증 레인 설계 기여 가능

## 90일 가설
입사 후 첫 30일은 분산 추론 클러스터의 OpenTelemetry 트레이스 커버리지와 오퍼레이터 스케일 결정의 관측 가능성을 점검하며 Go·오퍼레이터 코드베이스를 학습합니다. 다음 30일은 Inference Autopilot의 스케일 경로 1개를 골라 동시성 경합이나 멱등성 결함을 1건 이상 찾아 격리 PoC를 제안합니다. 마지막 30일은 분산 추론 장애 1종에 대한 OpenTelemetry 기반 자동 탐지·알람 파이프라인을 검증하고 AI-Native 개발 검증 게이트 한 가지를 표준화합니다.

## 원문 (참고)
> Kubernetes 운영 및 커스텀 오퍼레이터 개발 2년 이상
> Go, Python, 또는 Rust 프로그래밍 역량
> OpenTelemetry로 분산 환경 오류 탐지 모니터링 파이프라인 구축
> 설계부터 검증까지 개발 프로세스에 AI 에이전트 통합
