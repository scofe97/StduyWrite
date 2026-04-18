# 일반·트리거 파이프라인 차이와 FTL 설명
---
> 이 문서는 일반 파이프라인과 트리거 파이프라인의 차이를 Jenkins Job 관점에서 설명하고, `ftl` 템플릿 파일이 이 구조에서 어떤 역할을 하는지 정리한 문서다.

## 1. 한 줄 요약
가장 단순하게 요약하면 일반 파이프라인은 Jenkins Job 하나가 자기 스크립트로 직접 작업을 수행하는 구조다. 트리거 파이프라인은 Jenkins Job 하나가 상위 오케스트레이터가 되어 여러 일반 파이프라인 Job을 순서대로 호출하는 구조다.

다만 트리거도 Jenkins Job "하나"라는 점은 같다. 차이는 그 Job이 직접 빌드·배포를 하느냐, 아니면 다른 Job들을 호출하느냐에 있다.

## 2. 일반 파이프라인과 트리거 파이프라인의 차이
일반 파이프라인과 트리거 파이프라인은 둘 다 Jenkins build를 호출하지만, Job의 책임이 다르다.

| 비교 항목 | 일반 파이프라인 | 트리거 파이프라인 |
| :--- | :--- | :--- |
| 기본 역할 | 자기 스크립트를 직접 수행 | 하위 파이프라인들을 호출 |
| Jenkins Job 의미 | 실행 주체 | 실행 지시자 |
| 대표 API | `/pipeline/v3/execute` | `/pipeline/v3/execute/trigrPpln` |
| 실행 전 반영 방식 | 기존 Job을 `updatePipeline()`으로 갱신 | Trigger Job을 `upsertTriggerPipeline()`으로 새로 반영 |
| 스크립트 내용 | 빌드·배포 단계 자체 | `build job:` 호출 로직 |
| 실행 대상 | 일반 Pipeline Job 1건 | Trigger Job 1건 + 하위 일반 Job 여러 건 |
| 후속 동기화 | 파이프라인 실행 이력 중심 | 트리거 상태와 하위 파이프라인 상태까지 포함 |

운영 관점에서 보면 일반 파이프라인은 "이 Job을 실행하면 실제 작업이 일어난다"에 가깝다. 반대로 트리거 파이프라인은 "이 Job을 실행하면 연결된 여러 일반 파이프라인이 순서대로 시작된다"에 가깝다.

## 3. 일반 파이프라인 예시
일반 파이프라인은 Jenkinsfile 또는 그에 준하는 Groovy 스크립트를 자기 Job 안에 직접 가진다. 개념적으로는 아래처럼 이해하면 된다.

```groovy
pipeline {
    agent any

    parameters {
        string(name: 'IMAGE_TAG', defaultValue: 'latest')
    }

    stages {
        stage('Build') {
            steps {
                sh 'gradle clean build'
            }
        }

        stage('Deploy') {
            steps {
                sh './deploy.sh'
            }
        }
    }
}
```

이 경우 Job 자체가 `Build`, `Deploy` 같은 실제 작업 단계를 수행한다. 따라서 일반 파이프라인은 "실행하면 곧바로 실작업이 수행되는 Job"이다.

## 4. 트리거 파이프라인 예시
트리거 파이프라인은 직접 빌드·배포를 하지 않고 하위 Job을 호출한다. `TriggerGroovyScript.ftl`에서 생성되는 핵심 구조는 아래와 비슷하다.

```groovy
def buildTrigger(bizNm) {
    def separateId = "${wrkflwExcnNo}-${wrkflwInptNo}-${trigrSn}"

    bizBuild = build job: "${envrnCd}/${bizNm}",
        propagate: false,
        wait: true,
        quietPeriod: 5,
        parameters: [
            string(name: 'SEPARATE_ID', value: "${separateId}"),
            string(name: 'IMAGE_TAG', value: "${separateId}")
        ]
}
```

하위 파이프라인 목록이 `biz-a`, `biz-b`라면 Trigger Job은 개념적으로 아래처럼 동작한다.

```groovy
pipeline {
    agent any

    stages {
        stage('TASK/DEV/biz-a') {
            steps {
                script {
                    buildTrigger('biz-a')
                }
            }
        }

        stage('TASK/DEV/biz-b') {
            steps {
                script {
                    buildTrigger('biz-b')
                }
            }
        }
    }
}
```

이 스크립트의 핵심은 `sh`나 배포 명령을 직접 수행하는 것이 아니라 `build job:`으로 다른 Jenkins Job을 호출한다는 점이다. 그래서 트리거 파이프라인은 오케스트레이터라고 보는 편이 정확하다.

## 5. 더 쉬운 설명
가장 쉽게 비유하면 일반 파이프라인은 "작업자"이고, 트리거 파이프라인은 "작업 지시자"다.

일반 파이프라인은 자기 안에 실제 작업 명령이 있다. 예를 들어 `gradle build`, `docker build`, `kubectl apply` 같은 명령을 자기 스크립트에서 직접 실행한다.

반면 트리거 파이프라인은 그런 명령을 직접 수행하지 않는다. 대신 "먼저 `biz-a` Job 실행", "그다음 `biz-b` Job 실행"처럼 다른 Jenkins Job을 호출하는 순서표를 들고 있는 Job이라고 보면 된다.

즉 아래처럼 이해하면 된다:

- 일반 파이프라인: 내가 직접 빌드하고 배포한다.
- 트리거 파이프라인: 다른 파이프라인들에게 빌드와 배포를 시킨다.

## 6. 실제 Jenkins 경로로 보면
코드 기준으로 일반 파이프라인과 트리거 파이프라인의 Jenkins 경로 구조도 다르다.

- 일반 파이프라인 경로:
  `/job/{taskCd}/job/{envrnCd}/job/{bizNm}`
- 트리거 파이프라인 경로:
  `/job/{taskCd}/job/{taskCd}-{envrnCd}`

예를 들어 업무코드가 `TASK`, 환경코드가 `DEV`라고 가정하면 아래처럼 된다:

- 트리거 Job:
  `/job/TASK/job/TASK-DEV`
- 일반 Job 1:
  `/job/TASK/job/DEV/job/biz-a`
- 일반 Job 2:
  `/job/TASK/job/DEV/job/biz-b`

이때 사용자가 트리거 실행을 누르면 Jenkins는 먼저 `/job/TASK/job/TASK-DEV`를 실행한다. 그런데 이 Job 안에는 실제 빌드 명령이 있는 것이 아니라, 내부적으로 `/job/TASK/job/DEV/job/biz-a`, `/job/TASK/job/DEV/job/biz-b` 같은 일반 Job을 차례대로 호출하는 코드가 들어 있다.

즉 사용자는 트리거 Job 하나를 실행하지만, 실제 작업은 그 아래 일반 Job 여러 개가 수행한다.

## 7. 아주 단순한 예시
배포 대상이 두 개라고 가정해 보자.

- 고객관리 서비스 `biz-a`
- 주문관리 서비스 `biz-b`

일반 파이프라인 방식이면 사용자가 각각 따로 실행해야 한다.

1. `biz-a` 파이프라인 실행
2. `biz-b` 파이프라인 실행

트리거 파이프라인 방식이면 사용자는 트리거 Job 하나만 실행한다.

1. `TASK-DEV` 트리거 실행
2. 트리거 Job이 내부에서 `biz-a` 실행
3. 트리거 Job이 내부에서 `biz-b` 실행

그래서 트리거는 "여러 파이프라인을 묶어 실행하는 상위 시나리오"라고 이해하면 된다.

## 8. 실제 실행 흐름을 단계로 보면
일반 파이프라인은 다음 순서로 이해하면 된다.

1. DB 또는 통합 정보에서 현재 파이프라인 스크립트를 가져온다.
2. 그 스크립트로 Jenkins 일반 Job의 `config.xml`을 갱신한다.
3. 그 일반 Job을 직접 실행한다.

트리거 파이프라인은 다음 순서로 이해하면 된다.

1. 트리거에 연결된 하위 파이프라인 목록을 읽는다.
2. 그 목록으로 Trigger Job용 Groovy를 새로 생성한다.
3. 그 Groovy로 Jenkins Trigger Job의 `config.xml`을 갱신한다.
4. 그 Trigger Job을 실행한다.
5. Trigger Job 내부에서 하위 일반 파이프라인들을 `build job:`으로 호출한다.

즉 차이는 "몇 개를 실행하느냐"보다 "실행 전에 어떤 스크립트를 Jenkins Job에 넣느냐"에 더 가깝다.

## 9. `ftl` 파일이란 무엇인가
`ftl`은 FreeMarker Template Language의 확장자다. FreeMarker는 서버에서 문자열을 생성할 때 쓰는 템플릿 엔진이며, 이 프로젝트에서는 Jenkins Groovy 스크립트와 Jenkins `config.xml` 문자열을 동적으로 만드는 데 사용한다.

쉽게 말하면 `ftl` 파일은 "완성본이 아니라 틀"이다. 자바 코드가 변수 값을 넣어 최종 텍스트를 만들면, 그 결과가 Jenkins에 전달된다.

예를 들어 아래와 같은 값이 있다고 가정하면:

- 업무코드: `TASK`
- 환경코드: `DEV`
- 하위 파이프라인: `biz-a`, `biz-b`

`TriggerGroovyScript.ftl`은 이 값을 받아 최종 Groovy 스크립트를 만든다. 따라서 `ftl`은 직접 실행되는 파일이 아니라, 실행될 Groovy나 XML을 만들어 내는 원본 템플릿이다.

## 10. 이 프로젝트에서 `ftl`이 쓰이는 위치
이 프로젝트의 `FreemarkerService`는 템플릿을 읽어 Jenkins용 문자열을 만든다. 대표적인 파일은 다음과 같다.

- `TriggerGroovyScript.ftl`
- `JenkinsJobConfigXml.ftl`
- `JenkinsJobConfigXmlWithTicket.ftl`
- `GitBaseJobConfigXml.ftl`
- `GitBaseJobConfigXmlWithTicket.ftl`

역할은 다음처럼 나뉜다:

- `TriggerGroovyScript.ftl`: 트리거 실행용 Groovy 스크립트 생성
- `JenkinsJobConfigXml.ftl`: 일반 Jenkins Job의 `config.xml` 생성
- `JenkinsJobConfigXmlWithTicket.ftl`: 티켓 기반 파라미터가 포함된 Job XML 생성
- `GitBaseJobConfigXml.ftl`: 스크립트를 Git 저장소에서 읽는 Jenkins Job XML 생성

즉 `ftl`은 파이프라인을 "정의하는 텍스트"를 자동 생성하는 도구다.

## 11. 코드와 연결해서 보면
코드 흐름은 아래처럼 이어진다.

- 일반 파이프라인 실행:
  `PipelineProcessorImpl.executeJenkinsPipeline()` -> `JenkinsService.executePipeline()` -> `updatePipeline()`
- 트리거 파이프라인 실행:
  `PipelineProcessorImpl.executeTriggerPipeline()` -> `JenkinsService.executeTriggerPipeline()` -> `upsertTriggerPipeline()` -> `FreemarkerService.processTriggerScript()`

이 흐름 때문에 일반 파이프라인은 기존 스크립트를 다시 싣는 구조가 되고, 트리거 파이프라인은 실행 직전에 새 스크립트를 합성하는 구조가 된다.

## 12. 읽는 순서 가이드
질문 목적에 따라 보면 좋은 순서는 다음과 같다:

- 실행 전체 흐름이 궁금하면 `04_실행_관련_전체_로직.md`
- 일반과 트리거의 차이가 궁금하면 이 문서
- 트리거 실행 시 Jenkins 수정 여부만 보고 싶으면 `01_트리거_실행시_Jenkins_수정_여부.md`

## 13. 변경 이력
| 날짜 | 작성자 | 내용 | 비고 |
| :--- | :--- | :--- | :--- |
| 2026-04-12 | Codex | 일반/트리거 차이와 FTL 설명 문서 신규 작성 | - |
| 2026-04-12 | Codex | 트리거 파이프라인 예시를 쉬운 설명과 실제 Job 경로 예시로 보강 | - |
