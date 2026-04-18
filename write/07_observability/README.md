---
title: 07_observability MOC
tags: [moc, observability, grafana, tempo, loki]
status: final
related: []
updated: 2026-04-19
---

# 07_observability
---
> 로깅·메트릭·트레이싱 세 축과 Grafana LGTM 스택 운영 문서를 모은다.

## 경계 기준

Alert 룰 설계와 SLO는 여기에 속한다. 반면 이를 CI/CD 파이프라인에서 배포·검증하는 절차는 `08_devops/`로 간다.

## 주요 문서 (초기 이관분)

- `01-1.모니터링.md`, `01.관측 기술스택.md`
- Grafana 시리즈: `02-01.Grafana Core`, `02-02.Alloy`, `02-03.Loki`, `02-04.Tempo`, `02-05.Mimir`, `02-06.Beyla`, `02-07.LGTM K8s 통합 배포`
- `03-01~06` 실전 프로젝트 시리즈 (LGTM 통합·Outbox E2E 트레이스)
- `05-01.Tempo 분산 트레이싱 시각화.md`
