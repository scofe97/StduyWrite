# 05_DevOps POC

## 개요
DevOps 도구와 프랙티스를 직접 구축하며 학습하는 실습 프로젝트 공간입니다.

## 프로젝트 목록

| # | 프로젝트 | 핵심 주제 | 챕터 | 상태 |
|---|---------|----------|------|------|
| 01 | [Jenkins](./01-jenkins/) | CI/CD 파이프라인, Pipeline as Code, Docker 통합 | 11ch | 🟢 진행중 |
| 02 | [CI/CD Patterns](./02-cicd-patterns/) | GoF 패턴 기반 CI/CD 설계, 배포 전략 심화, 성숙도 모델 | 10ch | 🟢 완성 |
| 03 | [DevOps Fundamentals](./03-devops-fundamentals/) | 앱 배포, IaC, 오케스트레이션, 네트워킹, 보안, 모니터링 | 10ch | 🟢 완성 |
| 04 | [Nexus Repository](./04-nexus/) | 아티팩트 관리, Docker Registry, REST API, CI/CD 연동 | 12ch | 🟢 완성 |

## 학습 순서 (권장)
1. **03-devops-fundamentals** — DevOps 기초 개념 (배포, IaC, 네트워킹, 보안, 모니터링)
2. **01-jenkins** — Jenkins 기반 CI/CD 파이프라인 실습
3. **02-cicd-patterns** — 디자인 패턴 관점의 CI/CD 설계 심화
4. **04-nexus** — Nexus Repository Manager를 활용한 아티팩트 관리 및 Docker Registry 운영

## 관련 이론 문서
- [docs/05_DevOps](../../docs/05_DevOps/)

## 연관 카테고리
- [03_CloudNative](../03_CloudNative/) — Docker, Kubernetes, Service Mesh
- [08_MessageQueue](../08_MessageQueue/) — 메시지 큐 연동 파이프라인
