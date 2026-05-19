---
title: 305 SonarQube 연동 인덱스
tags: [305p, sonarqube, static-analysis, jenkins]
status: final
source:
  - /Users/simbohyeon/okestro/tps-gitlab2/pipeline-api/src/main/java/org/okestro/tps/pipeline/v3/presentation/sonarqube/api
  - /Users/simbohyeon/okestro/tps-gitlab2/pipeline-api/src/main/java/org/okestro/tps/pipeline/v3/infrastructure/external/client/SonarQubeFeignClient.java
related:
  - ../305_JENKINS/00_Jenkins_연동_인덱스.md
updated: 2026-04-23
---

# 305 SonarQube 연동 인덱스
---
> SonarQube 연동 문서는 API 목록이 아니라 유스케이스별 조합을 기준으로 읽는다. 실제 분석 실행은 SonarQube API 단독 호출이 아니라 TPS 관리 API, Jenkins 분석 Job, ppln-logging callback, SonarQube quality gate API가 결합된 흐름이다.



## 문서 맵

> SonarQube 문서는 생성부터 결과 조회까지 시간 순서로 읽는다.

| 문서 | 범위 | 핵심 내용 |
|---|---|---|
| [01_프로젝트_생명주기와_Jenkins_분석_파이프라인.md](01_프로젝트_생명주기와_Jenkins_분석_파이프라인.md) | 관리 API | SonarQube 프로젝트 등록, 수정, 삭제와 Jenkins 분석 Job 동기화 |
| [02_분석_실행_종료_callback_품질게이트.md](02_분석_실행_종료_callback_품질게이트.md) | 실행 API | 티켓 분석, 수동 분석, logging callback, quality gate 반영 |
| [03_결과_조회_이슈_관리_API.md](03_결과_조회_이슈_관리_API.md) | 조회/이슈 API | measures, branches, issues, sources, rules, issue update |



## 공통 구조

> SonarQube 자체 project 생성 API는 FeignClient에 있지만, v3 관리 흐름의 중심은 TPS DB와 Jenkins 분석 Job이다.

`AnalysisManagementService.createSonarQubeProject`는 project key를 생성하고, Git/Harbor 정보를 조회하고, FreeMarker로 SonarQube용 Jenkins script를 만든다. 이후 통합관리 정보를 만들고 Jenkins 테스트 파이프라인을 `SQA`, `ETC` 환경으로 동기화한 뒤 SonarQube 프로젝트 메타데이터를 TPS DB에 저장한다.

분석 결과 종료 처리는 `ppln-logging-api`가 Jenkins 로그 수집 후 pipeline-api의 hidden callback을 호출하는 구조다. callback에서는 SonarQube quality gate를 조회하고 TPS 분석 실행 상태를 갱신한다.



## 유스케이스 읽기 순서

> SonarQube는 등록, 실행, 종료, 조회/관리 순서로 API가 조합된다.

| 순서 | 유스케이스 | 조합되는 시스템 |
|---|---|---|
| 1 | SonarQube 분석 대상 등록 | pipeline-api 관리 API, 통합관리, Jenkins Job 생성, TPS DB |
| 2 | 티켓 자동화 분석 실행 | Analysis API, Trigger API, Jenkins trigger Job, 하위 SQA Job |
| 3 | 수동 분석 실행 | Analysis management API, Jenkins SQA/ETC Job, TPS 실행 이력 |
| 4 | 분석 종료 callback | ppln-logging-api, pipeline-api hidden callback, SonarQube quality gate API |
| 5 | 분석 결과와 이슈 관리 | pipeline-api 조회 API, SonarQube measures/issues/sources/rules API |



## 공통 인증 규칙

> SonarQube API 호출은 지원 도구 테이블의 접속 정보로 Basic Auth를 만든다.

SonarQube FeignClient 메서드는 `URI baseUrl`과 `Authorization` header를 인자로 받는다. `AnalysisReader`와 `AnalysisWriter` 계열 구현체는 task, env, project key, ticket 정보를 기준으로 SonarQube tool id를 찾고, 해당 tool의 접속 ID와 시그널을 Basic Auth로 변환한다.



## 확인한 로컬 코드 위치

> 아래 파일을 기준으로 SonarQube 문서를 나누었다.

- `AnalysisManagementV3Controller.java`
- `AnalysisV3Controller.java`
- `AnalysisManagementService.java`
- `AnalysisService.java`
- `AnalysisReaderImpl.java`
- `AnalysisWriterImpl.java`
- `SonarQubeFeignClient.java`
- `SonarQubeService.java`
