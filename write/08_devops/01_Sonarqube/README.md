---
title: 01_Sonarqube MOC
tags: [moc, sonarqube, devops, static-analysis, quality-gate]
status: draft
related:
  - ../README.md
updated: 2026-05-07
---

# 01_Sonarqube

---

> SonarQube Server 운영·확장 문서를 모은다. 정적 분석 모델, 분석 리소스 구조, 운영 인터페이스, 통합, 운영 신뢰성을 5개 장으로 묶는다.



## 경계 기준

이 카테고리는 정적 분석 도구로서의 SonarQube 자체를 다룬다. CI/CD 파이프라인 그루비 작성법은 `02_Jenkins/`로, 아티팩트 저장소 운영은 `03_Nexus/`로 분담한다. SonarQube 분석 결과를 노출하는 대시보드 운영은 SonarQube 내장 UI를 기준으로 본 카테고리에서 다루지만, Prometheus/Grafana로 SonarQube 자체 메트릭을 적재하는 경우는 `07_observability/`로 넘긴다.

분석 결과를 외부 시스템(예: TPS Operator, ppln-logging-api)이 어떻게 받아들이는지는 4장 "통합 활용"에 둔다. 도구 자체의 모델과 운영은 1~3장과 5장에 둔다.



## 1장 입문과 모델

SonarQube가 어떤 결함을 잡고, 내부 컴포넌트와 리소스 모델이 어떻게 짜여 있는지를 잡는다. 이 두 본문으로 어휘를 정착한 뒤 2장 이후로 넘어간다.

- [01-01.정적 분석과 SonarQube 모델](01-01.정적 분석과 SonarQube 모델.md) — 정적 분석이 푸는 결함, 3-tier 아키텍처(Web/Compute Engine/Search), Issue·Rule·Quality Profile 관계, Quality Gate, Clean as You Code, MQR 모드
- [01-02.운영 환경과 분석 흐름](01-02.운영 환경과 분석 흐름.md) — 배포 모델 선택, 메모리·Elasticsearch 산정, Scanner 종류, 분석 한 번의 흐름, 인증·토큰, 업그레이드 트랙
- [01-점검.핵심 질문과 답](01-점검.핵심 질문과 답.md) — 1장 핵심 통찰 7문항 Q&A



## 2장 분석 모델

분석 결과를 구성하는 리소스를 모델 차원에서 다룬다.

- [02-01.Rule과 Quality Profile](02-01.Rule과 Quality Profile.md) — 내장 규칙 세트, Sonar way profile, 커스텀 profile (복제·상속), MQR 모드에서의 Profile 운영
- [02-02.Issue와 Security Hotspot](02-02.Issue와 Security Hotspot.md) — Issue 라이프사이클(OPEN/CONFIRMED/RESOLVED/CLOSED/REOPENED), 추적 알고리즘, Hotspot 리뷰 워크플로우, severity 모델 (Standard vs MQR)
- [02-03.Coverage와 Duplication](02-03.Coverage와 Duplication.md) — 외부 커버리지 리포트(JaCoCo, Cobertura) 흡수, Duplication 토큰 기반 탐지, 측정값과 Rating
- [02-점검.핵심 질문과 답](02-점검.핵심 질문과 답.md) — 2장 핵심 통찰 8문항 Q&A



## 3장 운영 인터페이스

외부에서 SonarQube를 다루는 주요 진입점을 정리한다.

- [03-01.Web API 구조](03-01.Web API 구조.md) — `/api/*` 네임스페이스, 응답 모델(paging+데이터+참조), 페이지네이션 한계, form-urlencoded 본문
- [03-02.인증과 토큰](03-02.인증과 토큰.md) — User/Project Analysis/Global Analysis Token, 권한 모델, Permission Template, LDAP/SAML/OAuth, 토큰 회전
- [03-03.Webhook과 이벤트](03-03.Webhook과 이벤트.md) — 페이로드 구조, 등록 범위, URL 거부 정책, HMAC-SHA256 시그니처, best-effort 전달
- [03-점검.핵심 질문과 답](03-점검.핵심 질문과 답.md) — 3장 핵심 통찰 8문항 Q&A



## 4장 통합 활용

CI/CD 파이프라인과 외부 시스템에서 SonarQube를 활용하는 패턴을 묶는다. TPS-GitLab2의 실사용 사례 3종을 본 장에서 본격 분석한다.

- [04-01.SonarScanner for Gradle 적용 패턴](04-01.SonarScanner for Gradle 적용 패턴.md) — `org.sonarqube` 플러그인, Gradle Tooling API 의존성, CI 환경에서의 토큰 주입 (TPS `pipeline-api` 사례)
- [04-02.SonarQube Web API·Webhook 통합](04-02.SonarQube Web API·Webhook 통합.md) — Feign 기반 13개 엔드포인트 래핑, ConfigurationProperties로 webhook 자동 등록, admin tool 단일 진입 (TPS `operator/cicd` 사례)
- [04-03.분석 실행 로그 수집](04-03.분석 실행 로그 수집.md) — 환경 코드 분기, SonarQube webhook 페이로드를 자체 로그 모델로 변환 (TPS `ppln-logging-api` 사례)
- [04-04.Jenkins 파이프라인 통합](04-04.Jenkins 파이프라인 통합.md) — `withSonarQubeEnv`, `waitForQualityGate`, `sonar.qualitygate.wait=true`
- [04-점검.핵심 질문과 답](04-점검.핵심 질문과 답.md) — 4장 핵심 통찰 8문항 Q&A



## 5장 운영 신뢰성

장기 운영에서 무너지지 않게 만드는 정책·복구·관찰 가능성을 모은다.

- [05-01.DB와 Elasticsearch 백업](05-01.DB와 Elasticsearch 백업.md) — DB 1순위/ES 옵션, PostgreSQL 논리·물리 백업, K8s persistence 트레이드오프, 복구 시연
- [05-02.업그레이드와 LTS 정책](05-02.업그레이드와 LTS 정책.md) — LTS Active/Previous/Latest 트랙, DB 마이그레이션 절차, 호환성 절벽(Java/DB/Scanner), Plugin 호환성
- [05-03.모니터링과 트러블슈팅](05-03.모니터링과 트러블슈팅.md) — `/api/system/status·health`, 4개 로그 파일 분리, CE 큐 적체·OOM·ES RED, Prometheus 통합 한계
- [05-점검.핵심 질문과 답](05-점검.핵심 질문과 답.md) — 5장 핵심 통찰 8문항 Q&A



## 진행 현황

| 장 | 상태 | 비고 |
|----|------|------|
| 01 입문과 모델 | draft | 본문 2 + 점검 1 |
| 02 분석 모델 | draft | 본문 3 + 점검 1 |
| 03 운영 인터페이스 | draft | 본문 3 + 점검 1 |
| 04 통합 활용 | draft | 본문 4 + 점검 1, TPS 3종 + Jenkins |
| 05 운영 신뢰성 | draft | 본문 3 + 점검 1 |
