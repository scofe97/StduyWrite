---
title: docs/sonarqube MOC
tags: [moc, sonarqube, devops, static-analysis, quality-gate, jenkins, web-api]
status: draft
source:
  - https://docs.sonarsource.com/sonarqube-server/2026.1/
  - https://docs.sonarsource.com/sonarqube-community-build/feature-comparison-table
related:
  - ../../README.md
updated: 2026-08-22
---

# docs/sonarqube

> SonarQube Server 2026.1 LTA 공식 문서를 1차 자료로 삼아 정적 분석 모델부터 Jenkins 연계와 Web API 까지 6개 장으로 정리합니다. 본문에 적는 동작은 로컬 실습 인스턴스에서 실제로 확인한 것만 씁니다.

## 이 폴더의 자리

> `book/` 이 단행본 정독 노트라면 여기는 공식 문서 기반 노트입니다. 둘을 폴더로 갈라 근거의 성격을 드러냅니다.

SonarQube 에는 볼 만한 전용 단행본이 없습니다. 전용서는 둘뿐입니다.

- *SonarQube in Action* (Manning, 2013)
- *Sonar Code Quality Testing Essentials* (Packt, 2012)

둘 다 Quality Gate 의 현행 모델보다 앞섭니다. Clean as You Code 와 MQR 모드, Security Hotspot 이 등장하기 전에 쓰인 책입니다. O'Reilly 에도 챕터 단위 언급만 있습니다. 그래서 이 카테고리는 공식 문서를 정본으로 삼아 `07_devops/book/` 과 분리해 둡니다.

Jenkins 파이프라인 문법 자체는 `../../02_Jenkins/` 가 담당합니다. 다만 4장은 SonarQube 를 CI 에 붙이는 과정을 처음부터 끝까지 자족적으로 다룹니다. 학습 중 폴더를 왕복하지 않게 하려는 의도이며, 그만큼 `02_Jenkins/06_infra/` 와 겹치는 부분이 있습니다.



## 기준 버전

> 문서는 2026.1 LTA, 실습은 같은 세대의 Community Build 26.1 입니다. 둘을 굳이 나눈 이유가 이 표에 있습니다.

| 대상 | 값 | 이유 |
|------|-----|------|
| 문서 기준 | SonarQube Server **2026.1 LTA** | 현행 Long-Term Active |
| 실습 서버 | Community Build **26.1.0.118079** | 2026.1 과 같은 세대. 26.1 에서 들어간 JDK 요구와 Quality Gate fudge factor 변경이 본문과 맞습니다 |
| branch plugin | **26.1.0** | 서드파티. SonarQube 와 major.minor 를 맞춥니다 |
| Jenkins JDK | **17** | TPS 의 Corretto 17 환경과 맞추려고 골랐습니다. JRE 자동 프로비저닝이 켜져 있으면 빌드 JDK 와 스캐너 런타임이 분리되는데, 4장 실행 로그가 이를 확인했습니다 |

2026.1 LTA 이미지는 Developer 에디션 이상이라 로컬에 띄울 수 없습니다. 무료로 쓸 수 있는 것은 Community Build 뿐이고, 여기서는 branch 와 PR 분석이 빠집니다. 그 빈자리를 서드파티 플러그인으로 메우는데, **학습 한정 구성이지 실무 권장 구성이 아닙니다.** 에디션 경계 자체는 6장에서 다룹니다.

각 편에는 Community Build 로 재현할 수 있는지를 표시합니다. PR 분석과 Advanced SAST, Portfolio 처럼 재현할 수 없는 항목은 문서 근거만으로 서술했음을 밝힙니다.

실습 환경은 `~/sonarqube-practice/` 에 있습니다.



## 장 구성

> 모델을 먼저 세우고, 분석이 도는 경로를 따라간 뒤, 결과를 읽고, CI 에 붙이고, 운영으로 마무리합니다. 6장은 에디션 경계를 다룹니다.

본문 19편입니다. 회상 문항은 각 편 안의 §면접에서 받을 만한 질문과 §정답 절에 둡니다.

### 1장 입문과 모델

| 편 | 다룰 내용 | 상태 |
|----|----------|------|
| [01-01 정적 분석이 푸는 결함](01-01.정적 분석이 푸는 결함.md) | 실행 없이 잡아내는 결함, 규칙과 이슈, 품질 분포 실측 | draft |
| [01-02 서버 구성 요소와 분석 흐름](01-02.서버 구성 요소와 분석 흐름.md) | 프로세스 넷, 데이터 위치, CI 호스트와 서버의 분업 | draft |
| [01-03 Clean as You Code와 MQR](01-03.Clean as You Code와 MQR.md) | New Code 정의 네 가지, MQR 과 Standard 의 분류 차이 | draft |

### 2장 분석 파이프라인

| 편 | 다룰 내용 | 상태 |
|----|----------|------|
| [02-01 Scanner 종류와 선택](02-01.Scanner 종류와 선택.md) | 빌드 시스템별 선택, 최소 버전, JRE 자동 프로비저닝 | draft |
| [02-02 분석 한 번의 흐름](02-02.분석 한 번의 흐름.md) | 스캐너와 Compute Engine 의 비동기 경계, 파라미터 우선순위 | draft |
| [02-03 Rule과 Quality Profile](02-03.Rule과 Quality Profile.md) | 내장 프로파일, 상속과 재정의 실측 | draft |
| [02-04 Quality Gate](02-04.Quality Gate.md) | Sonar way 네 조건, 브랜치와 PR 차이, fudge factor | draft |

### 3장 결과 모델

| 편 | 다룰 내용 | 상태 |
|----|----------|------|
| [03-01 Issue 라이프사이클과 추적](03-01.Issue%20라이프사이클과%20추적.md) | 두 상태 축, 줄 해시 매칭, 백데이팅, Sandbox | draft |
| [03-02 Security Hotspot](03-02.Security%20Hotspot.md) | 이슈와의 차이, 네 상태, OWASP·CWE 우선순위 | draft |
| [03-03 Coverage와 Duplication](03-03.Coverage와%20Duplication.md) | 커버리지 세 지표와 공식, 언어별 중복 임계 | draft |

### 4장 CI 통합

| 편 | 다룰 내용 | 상태 |
|----|----------|------|
| [04-01 Jenkins 연계](04-01.Jenkins%20연계.md) | 등록 셋, 두 스테이지, 웹훅 필수 조건, 첫 분석의 함정 | draft |
| [04-02 Web API 구조](04-02.Web%20API%20구조.md) | 실측 카탈로그 39·229, Bearer 인증, v2 이행 | draft |
| [04-03 인증과 토큰](04-03.인증과%20토큰.md) | 세 종류 접두어, 최소 권한, 만료와 회전 | draft |
| [04-04 Webhook](04-04.Webhook.md) | 두 개의 상태, 최선 노력 전달, HMAC 서명 | draft |

### 5장 운영

| 편 | 다룰 내용 | 상태 |
|----|----------|------|
| [05-01 설치와 용량 산정](05-01.설치와%20용량%20산정.md) | 기동 순서 실측, Elasticsearch 가 정하는 요구사항, 빈 인스턴스의 바닥 비용 | draft |
| [05-02 업그레이드와 LTA 정책](05-02.업그레이드와%20LTA%20정책.md) | 두 제품의 릴리스 주기, active version, LTA 경유 규칙, 폐기 달력 | draft |
| [05-03 모니터링과 트러블슈팅](05-03.모니터링과%20트러블슈팅.md) | 로그 여섯 갈래, 상태 엔드포인트 셋, 지표 두 경로, 적체 판정 | draft |

### 6장 에디션과 확장

| 편 | 다룰 내용 | 상태 |
|----|----------|------|
| [06-01 에디션 경계와 branch plugin](06-01.에디션%20경계와%20branch%20plugin.md) | 경계가 부재로 구현되는 방식, 플러그인이 메우는 자리와 그 대가 | draft |
| [06-02 Advanced Security와 AI 기능](06-02.Advanced%20Security와%20AI%20기능.md) | Enterprise 위의 별도 제품, AI 기능 네 갈래, 문서 간 불일치 | draft |



## 진행 현황

> 19편 전부 완료이고 구본 제거까지 끝났습니다.

| 장 | 본문 | 상태 |
|----|-----:|------|
| 1 입문과 모델 | 3 / 3 | **draft 완료** |
| 2 분석 파이프라인 | 4 / 4 | **draft 완료** |
| 3 결과 모델 | 3 / 3 | **draft 완료** |
| 4 CI 통합 | 4 / 4 | **draft 완료** |
| 5 운영 | 3 / 3 | **draft 완료** |
| 6 에디션과 확장 | 2 / 2 | **draft 완료** |

이 카테고리는 2026년 5월에 조사 기반으로 쓴 구본 21편을 대체하며, 구본은 제거했습니다. 사내 실사례를 다루던 3편만 공개 저장소 밖으로 옮겨 보존했습니다.
