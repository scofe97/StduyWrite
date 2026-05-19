---
title: 305 Jenkins 연동 인덱스
tags: [305p, jenkins, pipeline]
status: final
source:
  - /Users/simbohyeon/okestro/tps-gitlab2/pipeline-api/src/main/java/org/okestro/tps/pipeline/v3/infrastructure/external/client/JenkinsFeignClient.java
  - /Users/simbohyeon/okestro/tps-gitlab2/ppln-logging-api/src/main/java/org/okestro/tps/api/v3/infrastructure/external/client/JenkinsFeignClient.java
related:
  - ../305_SONARQUBE/00_SonarQube_연동_인덱스.md
  - ../305_ARGOCD/00_ArgoCD_연동_인덱스.md
updated: 2026-04-23
---

# 305 Jenkins 연동 인덱스
---
> Jenkins 연동은 TPS Pipeline 실행의 중심이다. 별도 `305_PIPELINE` 폴더를 두면 책임이 모호해지므로, 일반 파이프라인, 트리거 파이프라인, logging callback 문서를 모두 Jenkins 폴더로 통합한다.



## 문서 맵

> Jenkins는 Pipeline 문서와 분리해서 외부 API 사용 방식 중심으로 읽는다.

| 문서 | 범위 | 핵심 내용 |
|---|---|---|
| [01_Jenkins_Job_생성_수정_실행_API.md](01_Jenkins_Job_생성_수정_실행_API.md) | Jenkins API 단위 | Job folder, `config.xml`, build, stop, script validation, agent 조회 |
| [02_Jenkins_로그_BlueOcean_Crumb_Credential_API.md](02_Jenkins_로그_BlueOcean_Crumb_Credential_API.md) | Jenkins 보조 API 단위 | crumb, credential, progressiveText, Blue Ocean, approval input |
| [03_일반_파이프라인_CRUD_실행_유스케이스.md](03_일반_파이프라인_CRUD_실행_유스케이스.md) | 일반 파이프라인 유스케이스 | pipeline-api 내부 API가 Jenkins API와 DB 이력을 어떻게 조합하는지 |
| [04_트리거_파이프라인_상세_유스케이스.md](04_트리거_파이프라인_상세_유스케이스.md) | 트리거 파이프라인 유스케이스 | 생성, 실행 전 검증, Jenkins trigger Job upsert, 실행, scheduler 동기화 |
| [05_ppln_logging_로그수집_callback_유스케이스.md](05_ppln_logging_로그수집_callback_유스케이스.md) | logging-api 유스케이스 | Jenkins 로그 수집 결과가 JUnit, SonarQube, ArgoCD callback으로 분기되는 방식 |



## 공통 경로 규칙

> Job 경로는 업무 파이프라인과 트리거 파이프라인을 구분한다.

일반 파이프라인은 `/job/{taskCd}/job/{envrnCd}/job/{bizNm}` 형태로 생성된다. 트리거 파이프라인은 업무명이 없고 `/job/{taskCd}/job/{taskCd}-{envrnCd}` 형태로 생성된다. 이 차이 때문에 일반 파이프라인은 "하나의 업무 Job"이고, 트리거 파이프라인은 "여러 업무 Job을 순서대로 호출하는 orchestrator Job"으로 보는 편이 정확하다.

Blue Ocean 조회 경로는 logging-api에서 별도로 만든다. 일반 파이프라인 기준으로 `/pipelines/{taskCd}/pipelines/{envrnCd}/pipelines/{bizNm}` 형태를 사용한다.



## 공통 인증 규칙

> Jenkins 쓰기 API는 Basic Auth, crumb, cookie를 함께 사용한다.

`pipeline-api`의 `JenkinsService.getJenkinsAuth`는 Jenkins crumb을 먼저 조회하고, 응답 header의 cookie와 body의 crumb field를 다음 쓰기 요청에 넣는다. `ppln-logging-api`는 조회 계열에서 Basic Auth만 사용하는 메서드가 많지만, approval input 응답처럼 POST가 필요한 경우 crumb과 cookie를 함께 만든다.

문서에는 실제 계정과 비밀번호를 적재하지 않는다. 모든 인증 정보는 `tool id/password`, `Basic Auth`, `Jenkins-Crumb`, `Cookie` 수준으로만 표현한다.



## 확인한 로컬 코드 위치

> Jenkins 문서는 아래 파일을 기준으로 나누어 작성했다.

- `pipeline-api/.../infrastructure/util/jenkins/service/JenkinsService.java`
- `pipeline-api/.../infrastructure/external/client/JenkinsFeignClient.java`
- `pipeline-api/.../infrastructure/util/freemarker/service/FreemarkerService.java`
- `pipeline-api/.../application/trigger/TriggerService.java`
- `ppln-logging-api/.../infrastructure/util/jenkins/service/JenkinsService.java`
- `ppln-logging-api/.../infrastructure/external/client/JenkinsFeignClient.java`
