---
title: 305 Jenkins 로그 BlueOcean Crumb Credential API
tags: [305p, jenkins, log, blueocean, credential]
status: final
source:
  - /Users/simbohyeon/okestro/tps-gitlab2/pipeline-api/src/main/java/org/okestro/tps/pipeline/v3/infrastructure/external/client/JenkinsFeignClient.java
  - /Users/simbohyeon/okestro/tps-gitlab2/ppln-logging-api/src/main/java/org/okestro/tps/api/v3/infrastructure/external/client/JenkinsFeignClient.java
related:
  - ./01_Jenkins_Job_생성_수정_실행_API.md
  - ./05_ppln_logging_로그수집_callback_유스케이스.md
updated: 2026-04-23
---

# 305 Jenkins 로그 BlueOcean Crumb Credential API
---
> Jenkins 연동은 Job 생성/실행 외에도 crumb, credential, agent monitoring, progressive log, Blue Ocean, approval input API를 사용한다. 특히 로그 수집은 `ppln-logging-api`의 핵심 책임이다.



## 조사 기준

> 이 문서는 Jenkins 보조 API를 기능 단위로 정리한다.

`pipeline-api`의 Jenkins FeignClient에는 credential과 agent monitoring API가 포함되어 있다. `ppln-logging-api`의 Jenkins FeignClient에는 build 상태, full log, Blue Ocean node/step log, Jenkins input approval API가 포함되어 있다.



## API 사용 표

> 같은 Jenkins라도 모듈별로 쓰는 API 성격이 다르다.

| 기능 | 모듈 | 외부 API | 사용 목적 |
|---|---|---|---|
| crumb 발급 | pipeline-api, ppln-logging-api | `GET /crumbIssuer/api/json` | POST 요청에 필요한 crumb과 cookie 확보 |
| credential domain 조회 | pipeline-api | `GET /credentials/store/system/domain/{domainName}/api/json` | Jenkins credential domain 존재 확인 |
| credential 조회 | pipeline-api | `GET /credentials/store/system/domain/{domainName}/credential/{credentialId}` | credential id 존재 확인 |
| domain 생성 | pipeline-api | `POST /manage/credentials/store/system/createDomain` | credential domain 신규 생성 |
| credential 생성 | pipeline-api | `POST /credentials/store/system/domain/{domainName}/createCredentials` | Git/토큰/비밀번호 계열 credential 생성 |
| credential 수정 | pipeline-api | `POST /credentials/store/system/domain/{domainName}/credential/{credentialId}/updateSubmit` | 기존 credential 갱신 |
| credential 삭제 | pipeline-api | `POST /credentials/store/system/domain/{domainName}/credential/{credentialName}/doDelete` | credential 삭제 |
| agent 목록 | pipeline-api | `GET /computer/api/json` | Jenkins node 상태 조회 |
| agent 상세 | pipeline-api | `GET /computer/{agentId}/api/json` | 특정 node 상태 조회 |
| full log | ppln-logging-api | `GET /{pipelineStruct}/{buildNumber}/logText/progressiveText?start=0` | build 전체 로그 수집 |
| wfapi 상태 | ppln-logging-api | `GET /{pipelineStruct}/{buildNumber}/wfapi/describe` | workflow stage 상태 조회 |
| Blue Ocean node | ppln-logging-api | `GET /blue/rest/organizations/jenkins/{blueStruct}/runs/{buildNumber}/nodes/?limit=10000` | stage/node 목록 조회 |
| Blue Ocean step | ppln-logging-api | `GET /blue/rest/organizations/jenkins/{blueStruct}/runs/{buildNumber}/nodes/{nodeId}/steps/` | step 목록 조회 |
| Blue Ocean log | ppln-logging-api | `GET /blue/rest/organizations/jenkins/{blueStruct}/runs/{buildNumber}/nodes/{nodeId}/steps/{stepId}/log` | step 로그 조회 |
| approval 대기 확인 | ppln-logging-api | `GET /{pipelineStruct}/{buildNumber}/input/{inputId}` | 배포 승인 input 대기 여부 확인 |
| approval 응답 | ppln-logging-api | `POST /{pipelineStruct}/{buildNumber}/input/{inputId}/{syncResult}` | `proceedEmpty` 또는 `abort` 처리 |



## 현재 코드에서 실제로 쓰는 정책

> logging-api는 full log를 한 번에 가져온 뒤 환경 코드에 따라 pipeline-api callback을 호출한다.

`getPipelineFullLogText`는 progressive endpoint를 사용하지만 `start=0`만 지정한다. Jenkins progressive log API의 chunk 반복 수집은 구현되어 있지 않다. Blue Ocean node/step API는 유틸 메서드로 존재하지만, `LogWriterImpl.collectPipelineLog`의 기본 흐름은 full log 조회를 사용한다.

Credential API는 Jenkins Job을 Git SCM 기반으로 구성할 때 필요한 credential을 맞추기 위한 기반이다. Git credential, secret text, SSH private key, username/password 계열 VO가 존재하며, JSON form payload로 Jenkins credential API를 호출한다.



## 개선점

> Jenkins 보조 API는 대용량 로그, 민감정보, 권한 오류 처리 관점에서 보강할 부분이 많다.

- progressive log는 `X-Text-Size`와 `X-More-Data`를 따라 chunk 반복 수집하도록 개선해야 한다.
- full log를 application log로 그대로 남기는 코드는 secret masking 없이 위험하다.
- credential payload는 민감정보를 다루므로 debug log, 예외 메시지, 문서 복사 범위를 엄격히 제한해야 한다.
- crumb 응답에서 cookie/body가 없을 때의 null 방어가 부족하면 Jenkins 장애가 NPE로 보일 수 있다.
- agent monitoring 조회는 있지만 실행 제한 로직은 주석 처리되어 있어 Jenkins executor 포화 시 queue 지연이 커질 수 있다.



## 확인한 로컬 코드 위치

> 아래 파일에서 Jenkins 로그, Blue Ocean, credential API를 확인했다.

- `pipeline-api/.../JenkinsFeignClient.java`
- `pipeline-api/.../JenkinsService.java`
- `ppln-logging-api/.../JenkinsFeignClient.java`
- `ppln-logging-api/.../JenkinsService.java`
- `LogWriterImpl.java`
