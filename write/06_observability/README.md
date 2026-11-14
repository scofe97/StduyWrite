---
title: 06_observability MOC
tags: [moc, observability, grafana, tempo, loki, opentelemetry, 305p]
status: published
related: []
updated: 2026-11-14
---

# 06_observability

> 로깅·메트릭·트레이싱 세 축과 Grafana LGTM 스택 운영 문서, 그리고 305P 실 운영기록을 모읍니다.



## 경계 기준

Alert 룰 설계와 SLO는 본 디렉토리에 속합니다. 같은 룰을 CI/CD 파이프라인에서 배포·검증하는 절차는 `07_devops/`로 갑니다.

신호 4단계 모델·PromQL·LogQL 기본은 [`01_Foundations/`](01_Foundations/)와 [`02_LGTMStack/`](02_LGTMStack/)에 둡니다. OpenTelemetry 자체 규격과 Tempo·Loki·Prometheus 설정은 `02_LGTMStack/`에 속합니다. 오브젝트 스토리지 자체는 [`../05_data/`](../05_data/README.md)로 갑니다.



## 키워드

### observability-keywords.md

키워드 파일: [observability-keywords.md](../landscape/observability-keywords.md)

| 묶음 | 다룬 문서 | 빈 필수 키워드 |
|---|---|---|
| 1단계 · 관측 가능성의 자리 | 4편 | 구조화 이벤트가 기본 단위 |
| 2단계 · 계측 | 4편 | exposition · exporter · 클라이언트 라이브러리 |
| 3단계 · 지표와 PromQL | 7편 | 집계 연산자 · 이항 연산자 · 함수 |
| 4단계 · 로그와 트레이스 | 8편 | 트레이싱 배포 · 오버헤드 · 샘플링 |
| 5단계 · 알림과 SLO | 4편 | SLI · SLO · 에러 버짓 |
| 6단계 · 확장과 운영 | 7편 | — |
| 7단계 · 플랫폼 | 8편 | — |



## 하위 폴더·문서 목록

### 01_Foundations — 기초: 시그널과 SLO

- [01-01.모니터링.md](01_Foundations/01-01.모니터링.md) — 관측 스택 입문
- [01-02.관측 기술스택.md](01_Foundations/01-02.관측%20기술스택.md) — 신호 생산·수집·저장·시각화 4단계 모델
- [01-03.시그널 모델 — Golden Signals, RED, USE.md](01_Foundations/01-03.시그널%20모델%20—%20Golden%20Signals,%20RED,%20USE.md)
- [01-04.SLO와 알림 — Error Budget, Burn Rate.md](01_Foundations/01-04.SLO와%20알림%20—%20Error%20Budget,%20Burn%20Rate.md) — burn rate 이론과 알림 룰 SSOT를 정리합니다. 요청·윈도우 기반 SLO와 Sloth·Pyrra 자동 생성은 정독 노트 [13-01](book/mastering_prometheus/13-01.SLO%20를%20Prometheus%20로%20정의하고%20알림하기%20—%20요청·윈도우%20기반과%20Sloth·Pyrra.md)에서 다룹니다.
- [01-05.Logback 기초.md](01_Foundations/01-05.Logback%20기초.md) — SLF4J 관계·4대 구성요소·패턴·root=OFF·EvaluatorFilter·MDC (로그 신호 생산 계층)

### 02_LGTMStack — LGTM 컴포넌트

- [02-01.Grafana Core.md](02_LGTMStack/02-01.Grafana%20Core.md) — 시각화 계층, datasource 모델
- [02-02.Grafana Alloy.md](02_LGTMStack/02-02.Grafana%20Alloy.md) — OTel Collector 기반 통합 수집기
- [02-03.Grafana Loki.md](02_LGTMStack/02-03.Grafana%20Loki.md) — 라벨 기반 로그 저장소
- [02-04.Grafana Tempo.md](02_LGTMStack/02-04.Grafana%20Tempo.md) — 분산 trace 백엔드
- [02-05.Grafana Mimir.md](02_LGTMStack/02-05.Grafana%20Mimir.md) — 분산 메트릭 스토리지
- [02-06.Grafana Beyla.md](02_LGTMStack/02-06.Grafana%20Beyla.md) — eBPF 기반 자동 계측
- [02-07.LGTM K8s 통합 배포.md](02_LGTMStack/02-07.LGTM%20K8s%20통합%20배포.md)

### 단행본 정독·기타 폴더

- [book/mastering_prometheus/](book/mastering_prometheus/README.md) — *Mastering Prometheus*(Packt) 단행본 정독 노트 20편(15개 장)입니다. Prometheus를 운영·확장(extend) 관점에서 훑습니다. Thanos·VictoriaMetrics 저장 계층, promtool·Pint CI 검증, Sloth·Pyrra SLO 도구, OTel 통합을 다룹니다. 각 편은 책 사실 대조와 실측 및 정오표 검증을 거쳤습니다. MOC는 [book/mastering_prometheus/README.md](book/mastering_prometheus/README.md)입니다.
- `LGTM/` — LGTM 스택 추가 자료 (TBD)
- `_practice/` — 코드 실습 자산 (LGTM lab PoC)



## 예정 주제 — 관측 저장소 심화 (TBD)

> LGTM 스택(Mimir·Loki)이 메트릭·로그를 저장하는 한 가지 답이라면, 같은 문제를 다른 방식으로 푸는 저장 계층이 현장에 흔합니다. Prometheus 원본 생태계의 장기저장(Thanos)과 역색인 기반 로그 검색(OpenSearch)을 LGTM 대비 관점으로 익힙니다.

- **Thanos** — ✅ *작성됨.* 단일 노드 보존과 수평 확장 부재를 메우는 장기보존·글로벌 쿼리·다운샘플링 계층입니다. Mimir([02-05](02_LGTMStack/02-05.Grafana%20Mimir.md))와 같은 문제를 푸는 다른 해법이라 나란히 비교하면 좋습니다. 장기 데이터의 저장 백엔드로 오브젝트 스토리지(→ `05_data`의 MinIO편)를 씁니다. (실환경 예시: CMP 3.0.4 dataplatform이 Prometheus→Thanos→MinIO 구성)
  - 정독 노트: 저장 경로 [10-01](book/mastering_prometheus/10-01.Thanos%20저장%20경로%20—%20Sidecar·Compactor·Store.md) · 쿼리 경로 [10-02](book/mastering_prometheus/10-02.Thanos%20쿼리%20경로%20—%20Query·Query%20Frontend·Ruler·Receiver.md) · Mimir·VictoriaMetrics 대조 [09-02](book/mastering_prometheus/09-02.VictoriaMetrics%20와%20Grafana%20Mimir.md)
- **OpenSearch** — 역색인 기반 로그·검색 분석 엔진(Elasticsearch 포크)입니다. Loki([02-03](02_LGTMStack/02-03.Grafana%20Loki.md))가 라벨 기반 최소 인덱싱이라면 OpenSearch는 전문(full-text) 역색인입니다. 저장 비용과 쿼리 표현력의 트레이드오프가 정반대라는 점이 대비 포인트입니다.

경계: 신호 4단계 모델·PromQL·LogQL 기본은 [`01_Foundations/`](01_Foundations/)와 [`02_LGTMStack/`](02_LGTMStack/)에 있습니다. 여기 예정 범위는 비-LGTM 저장 계층(Thanos·OpenSearch)의 구조와 LGTM 대비만 다룹니다. 오브젝트 스토리지 자체는 [`../05_data/`](../05_data/README.md)로 갑니다.
