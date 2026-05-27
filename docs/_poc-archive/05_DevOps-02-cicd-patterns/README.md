# 02. CI/CD Design Patterns

## 개요
GoF 디자인 패턴의 렌즈로 CI/CD 파이프라인 설계를 분석하는 심화 학습 프로젝트입니다. Pipeline as Code, 테스트 자동화, 배포 전략, 행동/생성/구조 패턴, 규제 준수, 성숙도 모델까지 엔터프라이즈 수준의 CI/CD 아키텍처를 다룹니다.

## 선행 학습
- [01-jenkins](../01-jenkins/) — CI/CD 기초와 Jenkins 파이프라인
- [03-devops-fundamentals](../03-devops-fundamentals/) — DevOps 기초 개념

## 챕터 목록

| # | 제목 | 핵심 질문 |
|---|------|----------|
| 01 | [CI/CD 디자인 패턴 기초](./learning/01-cicd-design-pattern-foundations/) | GoF 패턴을 CI/CD에 어떻게 적용하는가? |
| 02 | [Pipeline as Code와 실행 모델](./learning/02-pipeline-as-code/) | 파이프라인을 코드로 정의하면 왜 수동 설정보다 나은가? |
| 03 | [테스트 자동화 패턴과 브랜칭](./learning/03-test-automation-patterns/) | CI/CD에서 테스트 자동화를 어떤 패턴으로 설계하는가? |
| 04 | [구조적 CI/CD 패턴](./learning/04-structural-cicd-patterns/) | Monorepo와 Polyrepo에서 파이프라인을 어떻게 다르게 설계하는가? |
| 05 | [배포 전략 심화](./learning/05-advanced-deployment-strategies/) | Feature Toggle/A/B/Dark Launch는 언제 사용하는가? |
| 06 | [행동 디자인 패턴](./learning/06-behavioral-patterns/) | Observer/Strategy/Command가 파이프라인 설계에 왜 필요한가? |
| 07 | [도메인 주도 CI/CD와 규제 준수](./learning/07-ddd-regulated-compliance/) | 규제 산업에서 파이프라인에 컴플라이언스를 어떻게 통합하는가? |
| 08 | [생성 패턴과 클라우드 네이티브](./learning/08-creational-patterns-cloud-native/) | Factory/Builder로 클라우드 파이프라인을 어떻게 구성하는가? |
| 09 | [측정, 감사, 성숙도 모델](./learning/09-measurement-audit-maturity/) | CI/CD 성과를 어떻게 측정하고 조직 성숙도를 평가하는가? |
| 10 | [안티패턴과 케이스 스터디](./learning/10-antipatterns-casestudies/) | CI/CD에서 가장 흔한 안티패턴과 극복 사례는? |

## Jenkins 교차참조
- Ch02 → Jenkins Ch03/04 (Pipeline as Code 기본은 Jenkins에서, 여기서는 멀티 도구 비교)
- Ch04 → Jenkins Ch05 (Shared Libraries 기본은 Jenkins에서, 여기서는 구조 패턴 관점)
- Ch05 → Jenkins Ch07 (기본 배포 전략은 Jenkins에서, 여기서는 Feature Toggle/A/B 심화)

## 각 챕터 구성
- `LEARN.md`: 본문 (500-700줄) — 문단 서술 + 동작하는 코드 예시 + Mermaid 다이어그램
- `INVESTIGATE.md`: 면접 수준 점검 질문 (100-140줄) — 질문만, 답 없음
