# 03. DevOps Fundamentals

## 개요
DevOps의 기초 개념을 처음부터 쌓아가는 학습 프로젝트입니다. 앱 배포, IaC, 오케스트레이션, CI/CD 구축, 네트워킹, 보안, 스토리지, 모니터링까지 DevOps 엔지니어가 알아야 할 핵심 영역을 실습 중심으로 다룹니다.

## 챕터 목록

| # | 제목 | 핵심 질문 |
|---|------|----------|
| 01 | [앱 배포의 기초](./learning/01-app-deployment-basics/) | 앱을 프로덕션에 배포하려면 최소한 무엇이 필요한가? |
| 02 | [Infrastructure as Code](./learning/02-infrastructure-as-code/) | ClickOps의 문제를 IaC로 어떻게 해결하는가? |
| 03 | [오케스트레이션과 앱 관리](./learning/03-orchestration-app-management/) | 배포/스케일링/복구 자동화에 어떤 도구를 선택하는가? |
| 04 | [버전 관리, 빌드, 테스트](./learning/04-version-build-test/) | 팀이 협업하려면 코드를 어떻게 관리하고 검증하는가? |
| 05 | [멀티 도구 CI/CD 구축](./learning/05-multi-tool-cicd/) | GitHub Actions로 파이프라인을 처음부터 어떻게 구축하는가? |
| 06 | [멀티 팀과 환경 관리](./learning/06-multi-team-environments/) | 팀이 늘어나면 배포와 코드를 어떻게 분리하는가? |
| 07 | [네트워킹 기초](./learning/07-networking-fundamentals/) | 서버 간 통신을 안전하고 신뢰성 있게 구성하려면? |
| 08 | [보안: 통신과 저장소](./learning/08-security-communication-storage/) | 데이터를 전송하고 저장할 때 어떻게 보호하는가? |
| 09 | [데이터 저장소 선택과 관리](./learning/09-data-storage-management/) | 어떤 데이터에 어떤 저장소를 선택하는가? |
| 10 | [모니터링, 관측성, 미래](./learning/10-monitoring-observability-future/) | 시스템 장애를 사전 감지하고 미래 트렌드에 어떻게 대비하는가? |

## 교차참조
- Ch01 → [Docker PoC](../../03_CloudNative/01-docker/)
- Ch03 → [Kubernetes PoC](../../03_CloudNative/02-kubernetes/)
- Ch05 → [Jenkins PoC](../01-jenkins/)
- Ch07 → [Service Mesh PoC](../../03_CloudNative/03-service-mesh/)

## 각 챕터 구성
- `LEARN.md`: 본문 (500-700줄) — 문단 서술 + 동작하는 코드 예시 + Mermaid 다이어그램
- `INVESTIGATE.md`: 면접 수준 점검 질문 (100-140줄) — 질문만, 답 없음
