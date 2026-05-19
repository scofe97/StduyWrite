---
title: 305 Jenkins Job 생성 수정 실행 API
tags: [305p, jenkins, job, config-xml]
status: final
source:
  - /Users/simbohyeon/okestro/tps-gitlab2/pipeline-api/src/main/java/org/okestro/tps/pipeline/v3/infrastructure/util/jenkins/service/JenkinsService.java
  - /Users/simbohyeon/okestro/tps-gitlab2/pipeline-api/src/main/java/org/okestro/tps/pipeline/v3/infrastructure/external/client/JenkinsFeignClient.java
related:
  - ./03_일반_파이프라인_CRUD_실행_유스케이스.md
  - ./04_트리거_파이프라인_상세_유스케이스.md
  - ./02_Jenkins_로그_BlueOcean_Crumb_Credential_API.md
updated: 2026-04-23
---

# 305 Jenkins Job 생성 수정 실행 API
---
> `pipeline-api`는 Jenkins Job을 직접 만들고 수정한다. FreeMarker 템플릿으로 Jenkins `config.xml`을 생성한 뒤 Jenkins Remote API에 XML을 전송하는 방식이다.



## 조사 기준

> 이 문서는 `pipeline-api` v3의 Jenkins 쓰기 작업을 기준으로 한다.

핵심 클래스는 `JenkinsService`와 `JenkinsFeignClient`이다. `PipelineService`와 `PipelineProcessorImpl`은 어떤 시점에 JenkinsService를 호출하는지 보여 주며, 실제 외부 API 경로는 FeignClient에 선언되어 있다.



## 현재 코드에서 실제로 쓰는 흐름

> Job 생성은 folder 자동 생성, Job 존재 확인, `config.xml` 생성, `createItem` 호출 순서로 진행된다.

| 유스케이스 | 내부 메서드 | Jenkins 처리 | 템플릿 기준 |
|---|---|---|---|
| 일반 Job 생성 | `createPipeline` | folder가 없으면 만들고, Job이 없으면 `createItem`을 호출한다 | `JenkinsJobConfigXml.ftl` 또는 `GitBaseJobConfigXml.ftl` |
| 일반 Job 수정 | `updatePipeline` | Job이 있으면 `config.xml`을 갱신하고, 없으면 생성으로 전환한다 | 생성과 동일한 XML 템플릿 |
| Job 삭제 | `deletePipeline` | Job이 있으면 `doDelete`를 호출한다 | 현재 일반 파이프라인 삭제 서비스에서는 호출이 주석 처리되어 있다 |
| 일반 Job 실행 | `executePipeline` | Job update 후 queue/inProgress 확인을 거쳐 build API를 호출한다 | 중간변수 유무에 따라 build API가 달라진다 |
| trigger Job 실행 | `executeTriggerPipeline` | trigger Job을 upsert하고 `/build`를 호출한다 | `TriggerGroovyScript.ftl` 기반 |

FreeMarker 템플릿은 `.ftl`이지만 최종 산출물은 Jenkins Pipeline Groovy 또는 Jenkins Job `config.xml`이다. 기존 문서의 결론처럼 Jenkins 파이프라인 템플릿은 `.ftl`로 관리하고, Jenkins에 전달되는 Job 정의는 XML이다.



## 외부 API 사용 방식

> `JenkinsFeignClient`에는 Job 관리와 실행에 필요한 Jenkins API가 직접 선언되어 있다.

| 목적 | HTTP | 외부 API | 사용 위치 |
|---|---|---|---|
| crumb 조회 | GET | `/crumbIssuer/api/json` | 모든 쓰기 요청의 사전 인증 |
| Job 존재 확인 | GET | `{pipelineStruct}/api/json` | 생성/수정/삭제/실행 전 확인 |
| 마지막 build 번호 | GET | `{pipelineStruct}/lastBuild/buildNumber` | 실행 이력 번호 산정 |
| build 상세 조회 | GET | `{pipelineStruct}/{lastBuildNo}/api/json` | inProgress 확인 |
| folder 생성 | POST | `{pipelineStruct}/createItem` | Job 경로 자동 생성 |
| Job 생성 | POST | `{pipelineStruct}/createItem` | XML Job 정의 등록 |
| Job 수정 | POST | `{pipelineStruct}/config.xml` | 기존 Job 설정 교체 |
| Job 삭제 | POST | `{pipelineStruct}/doDelete` | Job 삭제 |
| 실행 | POST | `{pipelineStruct}/build` | 파라미터 없는 실행 |
| 파라미터 실행 | POST | `{pipelineStruct}/buildWithParameters` | 중간변수 포함 실행 |
| 중지 | POST | `{pipelineStruct}/{lastBuildNo}/stop` | 실행 중인 build 중지 |
| 스크립트 검증 | POST | `{pipelineStruct}/descriptorByName/org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition/checkScriptCompile` | 현재 화면 API는 사실상 미사용 |



## 개선점

> Jenkins Job 관리는 현재 동작하지만, 운영 안정성을 위해 추적성과 실패 복구를 보강해야 한다.

- Job 생성과 수정이 자동 전환되므로 API 의도와 실제 Jenkins 작업이 다를 수 있다.
- 일반 파이프라인 삭제에서 Jenkins 삭제가 빠져 있어 orphan Job이 남을 수 있다.
- build number 예측은 Jenkins queue item id 추적으로 대체하는 편이 안전하다.
- script validation API는 선언되어 있지만 `/pipeline/v3/validate/script`는 현재 `null`을 반환하므로 지원 여부를 명확히 표시해야 한다.
- Jenkins 설정 XML 생성은 문자열 템플릿 기반이므로 XML escaping, credential id 누락, branch/path 오타 검증이 필요하다.



## 확인한 로컬 코드 위치

> 아래 파일에서 Jenkins Job 생성, 수정, 실행 API를 확인했다.

- `JenkinsService.java`
- `JenkinsFeignClient.java`
- `FreemarkerService.java`
- `PipelineProcessorImpl.java`
- `PipelineService.java`
