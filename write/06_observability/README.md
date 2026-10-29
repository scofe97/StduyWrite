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

처음에는 [관측 가능성 학습 로드맵](../roadmap/observability-roadmap.md)을 읽습니다. 계측에서 SLO·확장·플랫폼까지 무엇을 어떤 순서로 볼지 정합니다.

## 경계 기준

Alert 룰 설계와 SLO는 본 디렉토리에 속한다. 같은 룰을 CI/CD 파이프라인에서 배포·검증하는 절차는 `07_devops/`로 간다.

## 01. 기초 — 시그널과 SLO (`01_Foundations/`)

- [01-01.모니터링.md](01_Foundations/01-01.모니터링.md) — 관측 스택 입문
- [01-02.관측 기술스택.md](01_Foundations/01-02.관측%20기술스택.md) — 신호 생산·수집·저장·시각화 4단계 모델
- [01-03.시그널 모델 — Golden Signals, RED, USE.md](01_Foundations/01-03.시그널%20모델%20—%20Golden%20Signals,%20RED,%20USE.md)
- [01-04.SLO와 알림 — Error Budget, Burn Rate.md](01_Foundations/01-04.SLO와%20알림%20—%20Error%20Budget,%20Burn%20Rate.md) — burn rate 이론·알림 룰 SSOT. 요청 vs 윈도우 기반 SLO·Sloth/Pyrra 자동 생성은 정독 노트 [13-01](book/mastering_prometheus/13-01.SLO%20를%20Prometheus%20로%20정의하고%20알림하기%20—%20요청·윈도우%20기반과%20Sloth·Pyrra.md)
- [01-05.Logback 기초.md](01_Foundations/01-05.Logback%20기초.md) — SLF4J 관계·4대 구성요소·패턴·root=OFF·EvaluatorFilter·MDC (로그 신호 생산 계층)

## 02. LGTM 컴포넌트 (`02_LGTMStack/`)

- [02-01.Grafana Core.md](02_LGTMStack/02-01.Grafana%20Core.md) — 시각화 계층, datasource 모델
- [02-02.Grafana Alloy.md](02_LGTMStack/02-02.Grafana%20Alloy.md) — OTel Collector 기반 통합 수집기
- [02-03.Grafana Loki.md](02_LGTMStack/02-03.Grafana%20Loki.md) — 라벨 기반 로그 저장소
- [02-04.Grafana Tempo.md](02_LGTMStack/02-04.Grafana%20Tempo.md) — 분산 trace 백엔드
- [02-05.Grafana Mimir.md](02_LGTMStack/02-05.Grafana%20Mimir.md) — 분산 메트릭 스토리지
- [02-06.Grafana Beyla.md](02_LGTMStack/02-06.Grafana%20Beyla.md) — eBPF 기반 자동 계측
- [02-07.LGTM K8s 통합 배포.md](02_LGTMStack/02-07.LGTM%20K8s%20통합%20배포.md)

## 예정 주제 — 관측 저장소 심화 (TBD)

> LGTM 스택(Mimir·Loki)이 메트릭·로그를 저장하는 한 가지 답이라면, 같은 문제를 다른 방식으로 푸는 저장 계층이 현장에 흔하다. Prometheus 원본 생태계의 장기저장(Thanos)과, 역색인 기반 로그 검색(OpenSearch)을 LGTM 대비 관점으로 익힌다.

- **Thanos** — ✅ *작성됨.* Prometheus의 한계(단일 노드 보존·수평 확장 부재)를 메우는 장기보존·다중 클러스터 글로벌 쿼리·다운샘플링 계층. Mimir([02-05](02_LGTMStack/02-05.Grafana%20Mimir.md))와 *같은 문제를 푸는 다른 해법*이라 나란히 비교하면 좋다. 장기 데이터의 저장 백엔드로 오브젝트 스토리지(→ `05_data`의 MinIO편)를 쓴다. (실환경 예시: CMP 3.0.4 dataplatform이 Prometheus→Thanos→MinIO 구성.)
  → 정독 노트: 저장 경로 [10-01](book/mastering_prometheus/10-01.Thanos%20저장%20경로%20—%20Sidecar·Compactor·Store.md) · 쿼리 경로 [10-02](book/mastering_prometheus/10-02.Thanos%20쿼리%20경로%20—%20Query·Query%20Frontend·Ruler·Receiver.md). Mimir·VictoriaMetrics와의 직접 대조는 [09-02](book/mastering_prometheus/09-02.VictoriaMetrics%20와%20Grafana%20Mimir.md).
- **OpenSearch** — 역색인 기반 로그·검색 분석 엔진(Elasticsearch 포크). Loki([02-03](02_LGTMStack/02-03.Grafana%20Loki.md))가 *라벨 기반 최소 인덱싱*이라면 OpenSearch는 *전문(full-text) 역색인*이라, 저장 비용·쿼리 표현력의 트레이드오프가 정반대다. 이 대비가 학습 포인트.

경계: 신호 4단계 모델·PromQL·LogQL 기본은 [`01_Foundations/`](01_Foundations/)·[`02_LGTMStack/`](02_LGTMStack/)에 있다. 여기 예정 범위는 **비-LGTM 저장 계층**(Thanos·OpenSearch)의 구조와 LGTM 대비만. 오브젝트 스토리지 자체는 [`../05_data/`](../05_data/README.md).

## 서브 디렉토리

- `01_Foundations/` · `02_LGTMStack/` — 주제 폴더 (2026-05-24 평면 → 폴더 재구성, 2026-05-25 05 추가, 2026-08-05 04_Troubleshooting 정리)
- `book/mastering_prometheus/` — *Mastering Prometheus*(Packt) 단행본 정독 노트 20편(15개 장). Prometheus를 *운영·확장·확장(extend)* 관점에서 훑는다. LGTM과 대비되는 저장 계층(Thanos·VictoriaMetrics), CI 검증(promtool·Pint), SLO 도구(Sloth·Pyrra), OTel 통합까지 다룬다. 각 편은 책 사실 대조 + 실측(도구 빌드·실행) + 정오표 검증을 거쳤다. MOC는 [book/mastering_prometheus/README.md](book/mastering_prometheus/README.md).
- `LGTM/` — LGTM 스택 추가 자료 (TBD)
- `_practice/` — 코드 실습 자산 (LGTM lab PoC)

> **2026-05-24 재구성**: 24개 평면 파일을 4개 주제 폴더로 이동. 옛 `05. 심화`(Tempo 시각화)와 `06. 305P 운영기록`은 모두 실전 성격이라 `03_Project/`로 흡수(03-08~03-11 재넘버링).

경계: OpenTelemetry 자체 규격·Tempo·Loki·Prometheus 설정은 `02_LGTMStack/`에 속한다.
