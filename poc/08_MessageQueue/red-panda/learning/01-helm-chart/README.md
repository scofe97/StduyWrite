# 01. 설치 및 배포 (Docker + Helm)

Redpanda를 Docker와 Helm 두 가지 방식으로 설치하고 배포하는 방법을 다룹니다.
Docker는 로컬 개발/테스트 환경에 적합하고, Helm은 Kubernetes 기반 스테이징/프로덕션 배포에 사용합니다.

## 참조 차트

```
/Users/simbohyeon/okestro/tps_manifest/helm-charts/redpanda/ (v25.3.1)
```

## 챕터 구성

| # | 주제 | 설명 |
|---|------|------|
| 01 | [docker-quickstart](01-docker-quickstart.md) | Docker/Docker Compose 로컬 설치 및 실행 |
| 02 | [chart-overview](02-chart-overview.md) | Helm 차트 구조, Chart.yaml, 의존성 |
| 03 | [values-configuration](03-values-configuration.md) | values.yaml 상세 설정 분석 |
| 04 | [templates-analysis](04-templates-analysis.md) | 템플릿 파일 분석, Go 템플릿 문법 |
| 05 | [deployment](05-deployment.md) | Helm 배포 실습, 검증, 트러블슈팅 |
| 06 | [customization](06-customization.md) | 환경별 오버라이드, 프로덕션 설정 |

## 학습 순서

```
01-docker-quickstart (Docker로 빠르게 체험)
       ↓
02-chart-overview (Helm 구조 이해)
       ↓
03-values-configuration (설정 분석)
       ↓
04-templates-analysis (템플릿 동작 원리)
       ↓
05-deployment (Helm 배포 실습)
       ↓
06-customization (프로덕션 적용)
```

## Docker vs Helm 선택 기준

| 항목 | Docker Compose | Helm (K8s) |
|------|---------------|------------|
| 적합 환경 | 로컬 개발/테스트 | 스테이징/프로덕션 |
| 복잡도 | 낮음 | 중간-높음 |
| 스케일링 | 수동 | 자동 (HPA) |
| 장애 복구 | 수동 재시작 | 자동 (StatefulSet) |
