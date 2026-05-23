---
title: 06_observability MOC
tags: [moc, observability, grafana, tempo, loki, opentelemetry, 305p]
status: published
related: []
updated: 2026-05-17
---

# 06_observability
---
> 로깅·메트릭·트레이싱 세 축과 Grafana LGTM 스택 운영 문서, 그리고 305P 실 운영기록을 모은다.

## 경계 기준

Alert 룰 설계와 SLO는 본 디렉토리에 속한다. 같은 룰을 CI/CD 파이프라인에서 배포·검증하는 절차는 `07_devops/`로 간다.

## 01. 기초 — 시그널과 SLO (`01_Foundations/`)

- [01-01.모니터링.md](01_Foundations/01-01.모니터링.md) — 관측 스택 입문
- [01-02.관측 기술스택.md](01_Foundations/01-02.관측%20기술스택.md) — 신호 생산·수집·저장·시각화 4단계 모델
- [01-03.시그널 모델 — Golden Signals, RED, USE.md](01_Foundations/01-03.시그널%20모델%20—%20Golden%20Signals,%20RED,%20USE.md)
- [01-04.SLO와 알림 — Error Budget, Burn Rate.md](01_Foundations/01-04.SLO와%20알림%20—%20Error%20Budget,%20Burn%20Rate.md)

## 02. LGTM 컴포넌트 (`02_LGTMStack/`)

- [02-01.Grafana Core.md](02_LGTMStack/02-01.Grafana%20Core.md) — 시각화 계층, datasource 모델
- [02-02.Grafana Alloy.md](02_LGTMStack/02-02.Grafana%20Alloy.md) — OTel Collector 기반 통합 수집기
- [02-03.Grafana Loki.md](02_LGTMStack/02-03.Grafana%20Loki.md) — 라벨 기반 로그 저장소
- [02-04.Grafana Tempo.md](02_LGTMStack/02-04.Grafana%20Tempo.md) — 분산 trace 백엔드
- [02-05.Grafana Mimir.md](02_LGTMStack/02-05.Grafana%20Mimir.md) — 분산 메트릭 스토리지
- [02-06.Grafana Beyla.md](02_LGTMStack/02-06.Grafana%20Beyla.md) — eBPF 기반 자동 계측
- [02-07.LGTM K8s 통합 배포.md](02_LGTMStack/02-07.LGTM%20K8s%20통합%20배포.md)

## 03. 실전 프로젝트 + 305P 운영 (`03_Project/`)

> LGTM+Spring Boot+Outbox 실전 구축(03-01~07), Tempo 활용 시각화(03-08), 그리고 305P(`dev.trombone-v2.okestro.cloud`) 환경의 실 운영기록·OTel 도입 고려(03-09~11)를 하나의 실전 흐름으로 모은다.

- [03-01.LGTM 통합.md](03_Project/03-01.LGTM%20통합.md)
- [03-02.Application 적용.md](03_Project/03-02.Application%20적용.md)
- [03-03.실전 프로젝트 1.md](03_Project/03-03.실전%20프로젝트%201.md)
- [03-04.실전 프로젝트 2(스프링 상세 설정).md](03_Project/03-04.실전%20프로젝트%202(스프링%20상세%20설정).md)
- [03-05.실전 프로젝트 3(커넥터 상세 설정).md](03_Project/03-05.실전%20프로젝트%203(커넥터%20상세%20설정).md)
- [03-06.실전 프로젝트 4(alloy 상세 설정).md](03_Project/03-06.실전%20프로젝트%204(alloy%20상세%20설정).md)
- [03-07.실전 프로젝트 5(Outbox E2E 트레이스 연결).md](03_Project/03-07.실전%20프로젝트%205(Outbox%20E2E%20트레이스%20연결).md)
- [03-08.Tempo 분산 트레이싱 시각화.md](03_Project/03-08.Tempo%20분산%20트레이싱%20시각화.md) — Tempo trace를 Grafana에서 시각화·병목 분석 (개념은 02-04 참조)
- [03-09.305P 관측 운영기록.md](03_Project/03-09.305P%20관측%20운영기록.md) — 클러스터 현황·라벨 카탈로그·LogQL 결정·대시보드 chart·잔여 작업·의사결정 박제
- [03-10.LGTM·Loki 운영 관점.md](03_Project/03-10.LGTM·Loki%20운영%20관점.md) — label explosion·7일 보존·k8s-sidecar·datasource UID·Alloy 파이프라인·알람 인프라 선택지
- [03-11.305P OpenTelemetry 도입 고려사항.md](03_Project/03-11.305P%20OpenTelemetry%20도입%20고려사항.md) — 15장 교육 문서, Tail Sampling/Reactor/Retry-Trace 포함

## 04. 트러블슈팅 (`04_Troubleshooting/`)

- [04-01.관측 트러블슈팅.md](04_Troubleshooting/04-01.관측%20트러블슈팅.md)
- [04-02.트러블 슈팅.md](04_Troubleshooting/04-02.트러블%20슈팅.md)

## 서브 디렉토리

- `01_Foundations/` · `02_LGTMStack/` · `03_Project/` · `04_Troubleshooting/` — 위 4개 주제 폴더 (2026-05-24 평면 → 폴더 재구성)
- `LGTM/` — LGTM 스택 추가 자료 (TBD)
- `_practice/` — 코드 실습 자산 (LGTM lab PoC)

> **2026-05-24 재구성**: 24개 평면 파일을 4개 주제 폴더로 이동. 옛 `05. 심화`(Tempo 시각화)와 `06. 305P 운영기록`은 모두 실전 성격이라 `03_Project/`로 흡수(03-08~03-11 재넘버링).

## 예정 주제 — Spring 관측성 (TBD)

> 옛 `spring/` 서브폴더 placeholder를 본 README로 흡수 (2026-05-23). 작성 시점에는 본 README의 새 절 (예: `07. Spring 관측성`)로 직접 추가하거나, 분량이 커지면 그 시점에 별도 `spring/` 서브폴더 신설.

- Actuator 엔드포인트 커스터마이즈·보안
- Micrometer와 Prometheus 연결
- Spring Boot 3.x의 자동 트레이싱 (Brave → OpenTelemetry 전환)
- `/actuator/health` 그룹·프로브 설계

경계: OpenTelemetry 자체 규격·Tempo·Loki·Prometheus 설정은 `02_LGTMStack/`·`03_Project/`에 속한다. Spring Boot가 이들과 *자동 통합*되는 지점만 위의 예정 주제 범위.
