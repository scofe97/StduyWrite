---
title: 03_Nexus MOC
tags: [moc, nexus, devops, artifact]
status: draft
related:
  - ../README.md
updated: 2026-05-07
---

# 03_Nexus

---

> Sonatype Nexus Repository Manager 3 운영·확장 문서를 모은다. 아티팩트 관리 개념, 리포지토리 모델, 운영 인터페이스, 통합, 운영 신뢰성을 5개 장으로 묶는다.



## 경계 기준

이 카테고리는 아티팩트 저장소로서의 Nexus 자체를 다룬다. CI/CD 파이프라인 그루비 작성법은 `02_Jenkins/`로, Nexus가 만들어내는 메트릭의 대시보드 구성은 `06_observability/`로 분담한다. Docker Registry 일반 개념(Registry HTTP API V2 등)은 본 카테고리에 두되, 컨테이너 이미지 빌드 자체는 `02_Jenkins/04-03.컨테이너 이미지 빌드`를 우선 참고한다.



## 1장 입문과 설치

Nexus의 설계 모델과 배치 환경을 먼저 잡는다. 이 두 문서로 모델·운영 어휘를 정착한 뒤 2장 이후로 넘어간다.

- [01-01.아티팩트 관리의 기초](01-01.아티팩트 관리의 기초.md) — Hosted/Proxy/Group, 아티팩트 생명주기, Nexus 3 아키텍처(Karaf/OSGi/H2/Blob Store)
- [01-02.설치와 배포 환경](01-02.설치와 배포 환경.md) — VM/Docker/K8s 선택, JVM·Direct Memory 산정, Reverse Proxy, 업그레이드 전략
- [01-점검.핵심 질문과 답](01-점검.핵심 질문과 답.md) — 1장 핵심 통찰 7문항 Q&A



## 2장 리포지토리 모델

리포지토리 포맷과 캐싱 전략을 모델 차원에서 다룬다.

- [02-01.리포지토리 포맷과 구성](02-01.리포지토리 포맷과 구성.md) — Maven GAV, npm scope, Docker Registry V2, Raw, Content Selector, Routing Rule
- [02-02.프록시와 캐싱 전략](02-02.프록시와 캐싱 전략.md) — Content/Metadata Max Age, Negative Cache, Auto-blocking, Air-gapped
- [02-점검.핵심 질문과 답](02-점검.핵심 질문과 답.md) — Write Policy·Max Age·Routing Rule 점검



## 3장 운영 인터페이스

외부에서 Nexus를 다루는 주요 진입점을 정리한다.

- [03-01.REST API와 웹 통합](03-01.REST API와 웹 통합.md) — `/service/rest/v1` 구조, continuationToken, multipart 업로드, CORS
- [03-02.접근 제어와 인증](03-02.접근 제어와 인증.md) — Realm/User/Role/Privilege, Content Selector, LDAP, Anonymous
- [03-점검.핵심 질문과 답](03-점검.핵심 질문과 답.md) — Realm 순서·LDAP 캐시·CORS 우회 점검



## 4장 통합 활용

CI/CD 파이프라인과 컨테이너 생태계에서 Nexus를 활용하는 패턴을 묶는다.

- [04-01.CI/CD 파이프라인 연동](04-01.CI-CD 파이프라인 연동.md) — Jenkins·Gradle·npm·Docker 배포, 시크릿 관리, SNAPSHOT→RELEASE 프로모션
- [04-02.Docker Registry로서의 Nexus](04-02.Docker Registry로서의 Nexus.md) — hosted/proxy/group 포트 분리, nginx 라우팅, Bearer Token Realm
- [04-점검.핵심 질문과 답](04-점검.핵심 질문과 답.md) — 포트 분리 근거·rate limit·Realm 누락 증상 점검



## 5장 운영 신뢰성

장기 운영에서 무너지지 않게 만드는 정책·복구·관찰 가능성·운영 모델을 모은다.

- [05-01.정리 정책과 스토리지 관리](05-01.정리 정책과 스토리지 관리.md) — Cleanup→Compact 2단계, Blob Store 분리, S3 전환
- [05-02.백업 복구 업그레이드](05-02.백업 복구 업그레이드.md) — DB+Blob Store 일관 백업, 롤백 절차, RPO/RTO 설계
- [05-03.모니터링과 트러블슈팅](05-03.모니터링과 트러블슈팅.md) — Prometheus/Grafana, 5분 타임박스 진단, JVM·디스크 진단
- [05-04.프로덕션 운영 패턴](05-04.프로덕션 운영 패턴.md) — 규모별 아키텍처, OSS vs Pro, IaC, Promotion·Firewall, 마이그레이션
- [05-점검.핵심 질문과 답](05-점검.핵심 질문과 답.md) — 2단계 삭제·hot backup·HA·drift 점검



## 진행 현황

| 장 | 상태 | 구성 |
|----|------|------|
| 01 입문과 설치 | draft | 본문 2 + 점검 1 |
| 02 리포지토리 모델 | draft | 본문 2 + 점검 1 |
| 03 운영 인터페이스 | draft | 본문 2 + 점검 1 |
| 04 통합 활용 | draft | 본문 2 + 점검 1 |
| 05 운영 신뢰성 | draft | 본문 4 + 점검 1 |
