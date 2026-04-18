---
title: 01-jenkins-analysis
tags: []
status: draft
related: []
updated: 2026-04-19
---

# Jenkins 사용 분석

TPS 플랫폼에서 Jenkins는 CI/CD 파이프라인의 핵심 실행 엔진이다. pipeline-api가 파이프라인의 생명주기(생성/수정/삭제/실행)를 관리하고, ppln-logging-api가 실행 결과의 상태 추적과 로그 수집을 담당한다. 두 모듈이 동일한 Jenkins 서버를 바라보되 역할을 분리함으로써, 파이프라인 관리와 모니터링이 독립적으로 확장 가능한 구조를 갖추고 있다.

---

## 1. 프로젝트간 역할 분담

pipeline-api는 Jenkins에게 "무엇을 실행할지"를 지시하는 컨트롤 플레인이고, ppln-logging-api는 "실행 결과가 어떻게 되었는지"를 수집하는 데이터 플레인이다. 이 분리가 중요한 이유는 파이프라인 실행 요청과 로그 폴링의 트래픽 패턴이 근본적으로 다르기 때문이다. 실행 요청은 사용자 액션에 의한 간헐적 호출이지만, 로그 수집은 빌드 진행 중 지속적인 폴링이 필요하다.

| 책임 | pipeline-api | ppln-logging-api |
|------|-------------|-----------------|
| 파이프라인 CRUD | O | - |
| 파이프라인 실행/중지 | O | - |
| Jenkinsfile 검증 | O | - |
| 크레덴셜 관리 | O | - |
| 노드/에이전트 모니터링 | O | - |
| 빌드 상태 조회 | - | O |
| 로그 수집 (전체/스테이지별) | - | O |
| Blue Ocean 시각화 데이터 | - | O |
| 배포 승인 처리 | - | O |
| Jenkins 상태 → TPS 상태 매핑 | - | O |

```mermaid
graph TB
    subgraph TPS["TPS 플랫폼"]
        UI["TPS Frontend"]
        PA["pipeline-api<br/><i>파이프라인 관리</i>"]
        PL["ppln-logging-api<br/><i>로그/상태 수집</i>"]
        WA["workflow-api<br/><i>워크플로우 오케스트레이션</i>"]
        DB[("MariaDB<br/>TPS DB")]
    end

    subgraph External["외부 도구"]
        JK["Jenkins Server"]
    end

    UI -->|"CRUD, 실행 요청"| PA
    UI -->|"로그/상태 조회"| PL
    WA -->|"파이프라인 실행 위임"| PA
    WA -->|"상태 폴링"| PL

    PA -->|"REST API<br/>생성/수정/삭제/실행"| JK
    PL -->|"REST + Blue Ocean API<br/>상태/로그 조회"| JK

    PA --> DB
    PL --> DB

    style TPS fill:#f0f4ff,stroke:#4a6fa5,color:#333
    style External fill:#fff8f0,stroke:#d4a574,color:#333
    style UI fill:#e8f5e9,stroke:#4caf50,color:#333
    style PA fill:#e3f2fd,stroke:#1976d2,color:#333
    style PL fill:#e3f2fd,stroke:#1976d2,color:#333
    style WA fill:#e3f2fd,stroke:#1976d2,color:#333
    style DB fill:#fce4ec,stroke:#e91e63,color:#333
    style JK fill:#fff3e0,stroke:#ff9800,color:#333
```

---

## 2. 인증 방식

Jenkins 연동은 3단계 인증 체인을 사용한다. 단순 Basic Auth만으로는 CSRF 공격에 취약하므로, Jenkins의 Crumb 메커니즘을 함께 활용한다.

**인증 흐름:**
1. Basic Auth 생성: `Base64(username:apiToken)`
2. Crumb + 세션 쿠키 조회: `GET /crumbIssuer/api/json` (Basic Auth 헤더 포함)
3. 이후 쓰기 요청에 3개 헤더 포함: `Authorization`, `Cookie(JSESSIONID)`, `Jenkins-Crumb`

읽기 요청(GET)은 Basic Auth만으로 충분하지만, 쓰기 요청(POST)은 반드시 Crumb + 세션 쿠키가 필요하다. JenkinsService에서 `getJenkinsAuth()` 메서드가 이 3단계를 캡슐화하여 JenkinsAuthVo를 반환한다.

```
GET /crumbIssuer/api/json
Authorization: Basic YWRtaW46Y2xvdWQxMjM0
→ Response: { crumb: "abc123", crumbRequestField: "Jenkins-Crumb" }
→ Set-Cookie: JSESSIONID=xyz789

POST /job/{taskCd}/job/{envrnCd}/job/{bizNm}/build
Authorization: Basic YWRtaW46Y2xvdWQxMjM0
Cookie: JSESSIONID=xyz789
Jenkins-Crumb: abc123
```

---

## 3. 파이프라인 폴더 구조

Jenkins 내 파이프라인은 3단계 폴더 계층으로 조직된다. 이 구조를 통해 업무(task) → 환경(environment) → 업무명(business name) 순서로 자연스러운 네비게이션이 가능하다. 트리거 파이프라인은 개별 bizNm 없이 환경 단위로 묶이므로 2단계만 사용한다.

**일반 파이프라인:** `/job/{taskCd}/job/{envrnCd}/job/{bizNm}`
**트리거 파이프라인:** `/job/{taskCd}/job/{taskCd}-{envrnCd}`

트리거 파이프라인의 두 번째 폴더가 `{taskCd}-{envrnCd}` 형태인 이유는, 환경별 트리거를 구분하면서도 일반 파이프라인의 envrnCd 폴더와 충돌을 피하기 위해서다.

```mermaid
graph TD
    ROOT["Jenkins Root"]
    T1["job/ACME-001<br/><i>업무 코드</i>"]
    E1["job/DEV<br/><i>개발 환경</i>"]
    E2["job/STG<br/><i>스테이징</i>"]
    E3["job/PRD<br/><i>프로덕션</i>"]
    B1["job/acme-api-build<br/><i>빌드 파이프라인</i>"]
    B2["job/acme-api-deploy<br/><i>배포 파이프라인</i>"]
    B3["job/acme-api-build"]
    TR["job/ACME-001-DEV<br/><i>트리거 파이프라인</i>"]

    ROOT --> T1
    T1 --> E1
    T1 --> E2
    T1 --> E3
    T1 --> TR
    E1 --> B1
    E1 --> B2
    E2 --> B3

    style ROOT fill:#f5f5f5,stroke:#9e9e9e,color:#333
    style T1 fill:#e8eaf6,stroke:#3f51b5,color:#333
    style E1 fill:#e8f5e9,stroke:#4caf50,color:#333
    style E2 fill:#fff8e1,stroke:#ffc107,color:#333
    style E3 fill:#fce4ec,stroke:#e91e63,color:#333
    style B1 fill:#f3e5f5,stroke:#9c27b0,color:#333
    style B2 fill:#f3e5f5,stroke:#9c27b0,color:#333
    style B3 fill:#f3e5f5,stroke:#9c27b0,color:#333
    style TR fill:#fff3e0,stroke:#ff9800,color:#333
```

**폴더 자동 생성 로직 (`autoCreateFolder`):**

PipelineProcessorImpl은 파이프라인 생성 전에 폴더 존재 여부를 확인하고, 없으면 자동 생성한다. 폴더 생성 시 `mode=com.cloudbees.hudson.plugins.folder.Folder` 파라미터를 사용한다.

1. taskCd 폴더 존재 확인 → 없으면 생성
2. envrnCd 폴더 존재 확인 → 없으면 생성 (트리거는 이 단계 스킵)
3. 파이프라인 생성 (XML 설정 기반)

---

## 4. 파이프라인 생성 흐름

사용자가 파이프라인을 생성하면, TPS 내부에서 VO 변환 → 폴더 확인 → XML 생성 → Jenkins API 호출 순서로 진행된다. PipelineUpsertVo(TPS 도메인)를 JenkinsJobVo(Jenkins 도메인)로 변환하는 과정에서 Jenkinsfile 스크립트와 파라미터를 매핑한다.

```mermaid
sequenceDiagram
    actor User
    participant UI as TPS Frontend
    participant PA as pipeline-api
    participant Proc as PipelineProcessorImpl
    participant JS as JenkinsService
    participant JK as Jenkins Server
    participant DB as MariaDB

    User->>UI: 파이프라인 생성 요청
    UI->>PA: POST /jenkins/v3/create/pipeline

    Note over PA,Proc: VO 변환 단계
    PA->>Proc: createJenkinsPipeline()
    Proc->>Proc: convertToJenkinsJobVo()<br/>PipelineUpsertVo → JenkinsJobVo

    Note over Proc,JK: 폴더 자동 생성
    Proc->>JS: createPipeline(tool, job)
    JS->>JK: GET /{taskCd}/api/json
    JK-->>JS: 404 Not Found
    JS->>JK: POST /{taskCd}/createItem<br/>mode=Folder
    JK-->>JS: 200 OK
    JS->>JK: GET /{taskCd}/{envrnCd}/api/json
    JK-->>JS: 404 Not Found
    JS->>JK: POST /{taskCd}/{envrnCd}/createItem<br/>mode=Folder

    Note over JS,JK: 파이프라인 생성
    JS->>JS: XML 설정 생성<br/>(Jenkinsfile + 파라미터)
    JS->>JK: POST /{taskCd}/{envrnCd}/createItem<br/>Content-Type: application/xml
    JK-->>JS: 200 OK

    JS-->>Proc: true
    Proc->>DB: 파이프라인 정보 저장
    Proc-->>PA: 성공 응답
    PA-->>UI: ApiResponse(success)
```

---

## 5. 파이프라인 실행 → 로그 수집 흐름

파이프라인 실행은 pipeline-api가 시작하고, 이후 상태 추적과 로그 수집은 ppln-logging-api가 담당한다. ppln-logging-api는 Jenkins의 두 가지 API를 활용한다. 전체 로그는 `progressiveText` API로, 스테이지별 상세 로그는 Blue Ocean API로 가져온다. Blue Ocean은 `/blue/rest/organizations/jenkins/` 경로 아래에서 파이프라인을 `/pipelines/{taskCd}/pipelines/{envrnCd}/pipelines/{bizNm}` 형태로 접근하는데, 이는 일반 Jenkins API의 `/job/` 경로와 다른 구조라는 점에 유의해야 한다.

```mermaid
sequenceDiagram
    actor User
    participant UI as TPS Frontend
    participant PA as pipeline-api
    participant JK as Jenkins Server
    participant PL as ppln-logging-api
    participant DB as MariaDB

    User->>UI: 파이프라인 실행
    UI->>PA: POST /jenkins/v3/execute/pipeline
    PA->>JK: POST /{struct}/buildWithParameters
    JK-->>PA: 201 Created (Queue Item)
    PA->>PA: nextBuildNumber 계산
    PA->>DB: 실행 정보 저장 (buildNo)
    PA-->>UI: buildNo 반환

    Note over UI,PL: 로그 수집 단계 (폴링)

    loop 빌드 진행 중
        UI->>PL: 상태 조회 요청
        PL->>JK: GET /{struct}/{buildNo}/wfapi/describe
        JK-->>PL: WfApiResponseVo (status, stages)
        PL->>PL: sttsCdConverter()<br/>Jenkins → TPS 상태 변환
        PL-->>UI: 상태 응답 (EXCN/CMPTN/FAIL)
    end

    Note over UI,PL: 전체 로그 조회
    UI->>PL: 전체 로그 요청
    PL->>JK: GET /{struct}/{buildNo}/logText/progressiveText?start=0
    JK-->>PL: 평문 텍스트 로그
    PL-->>UI: 로그 텍스트

    Note over UI,PL: 스테이지별 로그 (Blue Ocean)
    UI->>PL: 스테이지 목록 요청
    PL->>JK: GET /blue/rest/.../runs/{buildNo}/nodes/?limit=10000
    JK-->>PL: 노드(스테이지) 목록
    PL-->>UI: 스테이지 목록

    UI->>PL: 특정 스테이지 로그
    PL->>JK: GET /blue/rest/.../nodes/{nodeId}/log/?start=0
    JK-->>PL: 스테이지 로그
    PL-->>UI: 스테이지 로그
```

---

## 6. 배포 승인 흐름

배포 승인은 Jenkins의 `input` step을 활용한다. Jenkinsfile에 `input` 블록이 포함된 파이프라인은 해당 스테이지에 도달하면 `PAUSED_PENDING_INPUT` 상태가 되고, TPS에서는 이를 `EXCN`(실행 중)으로 매핑한다. ppln-logging-api가 승인 대기 상태를 감지하면 UI에 승인 버튼을 노출하고, 사용자의 승인/거부 응답을 Jenkins에 전달한다.

승인 ID는 `APPROVE_{bizNm}` 형태로, 각 파이프라인별로 고유하다. 승인 시 `proceedEmpty`(빈 파라미터로 진행), 거부 시 `abort`를 Jenkins에 POST한다.

```mermaid
sequenceDiagram
    actor User
    participant UI as TPS Frontend
    participant PL as ppln-logging-api
    participant JK as Jenkins Server

    Note over JK: Jenkinsfile의 input 스테이지 도달
    JK->>JK: PAUSED_PENDING_INPUT 상태

    UI->>PL: 상태 폴링
    PL->>JK: GET /{struct}/{buildNo}/wfapi/describe
    JK-->>PL: status=PAUSED_PENDING_INPUT
    PL-->>UI: 승인 대기 상태 표시

    Note over PL,JK: 승인 대기 확인
    UI->>PL: 승인 대기 확인 요청
    PL->>JK: GET /{triggerStruct}/{buildNo}/input/APPROVE_{bizNm}
    JK-->>PL: 200 OK (대기 중)
    PL-->>UI: 승인 버튼 활성화

    alt 승인
        User->>UI: 승인 클릭
        UI->>PL: 승인 요청 (proceedAt=true)
        PL->>JK: POST /{triggerStruct}/{buildNo}/input/APPROVE_{bizNm}/proceedEmpty
        JK-->>PL: 200 OK
        JK->>JK: 파이프라인 계속 실행
        PL-->>UI: 승인 완료
    else 거부
        User->>UI: 거부 클릭
        UI->>PL: 거부 요청 (proceedAt=false)
        PL->>JK: POST /{triggerStruct}/{buildNo}/input/APPROVE_{bizNm}/abort
        JK-->>PL: 200 OK
        JK->>JK: 파이프라인 중단 (ABORTED)
        PL-->>UI: 거부 완료
    end
```

---

## 7. Jenkins 상태 → TPS 상태 매핑

JenkinsConstant의 `sttsCdConverter()` 메서드가 Jenkins의 다양한 상태를 TPS의 5가지 상태로 단순화한다. 이 매핑에서 주목할 점은 `PAUSED_PENDING_INPUT`(승인 대기)이 `EXCN`(실행 중)으로 매핑된다는 것이다. TPS 관점에서 승인 대기는 "아직 끝나지 않은 실행"이므로, 별도 상태를 만들지 않고 실행 중에 포함시켰다. 승인 대기 여부는 별도 API(`checkJenkinsWaitForApprove`)로 확인한다.

```mermaid
stateDiagram-v2
    state "Jenkins 상태" as JS {
        IN_PROGRESS: IN_PROGRESS
        PAUSED: PAUSED_PENDING_INPUT
        SUCCESS: SUCCESS
        FAILED: FAILED
        UNSTABLE: UNSTABLE
        FAILURE: FAILURE
        ABORTED: ABORTED
        NOT_EXEC: NOT_EXECUTED
        NOT_BUILT: NOT_BUILT
    }

    state "TPS 상태" as TPS {
        EXCN: EXCN (실행 중)
        CMPTN: CMPTN (완성)
        FAIL: FAIL (실패)
        RJCT: RJCT (거부)
        WAIT: WAIT (대기)
    }

    IN_PROGRESS --> EXCN
    PAUSED --> EXCN
    SUCCESS --> CMPTN
    FAILED --> FAIL
    UNSTABLE --> FAIL
    FAILURE --> FAIL
    NOT_EXEC --> FAIL
    NOT_BUILT --> FAIL
    ABORTED --> RJCT
    [*] --> WAIT : 기타 상태
```

**매핑 요약:**

| Jenkins 상태 | TPS 상태 | 의미 |
|-------------|---------|------|
| IN_PROGRESS | EXCN | 빌드 실행 중 |
| PAUSED_PENDING_INPUT | EXCN | 승인 대기 (실행 중으로 간주) |
| SUCCESS | CMPTN | 성공 완료 |
| FAILED, UNSTABLE, FAILURE | FAIL | 빌드 실패 |
| NOT_EXECUTED, NOT_BUILT | FAIL | 미실행 (스테이지 스킵 등) |
| ABORTED | RJCT | 사용자가 수동 중지 |
| 기타 | WAIT | 대기 (큐 대기 등) |

---

## 8. 주요 API 엔드포인트 정리

### 8.1 pipeline-api (TPS REST API)

| HTTP | 엔드포인트 | 설명 |
|------|-----------|------|
| POST | `/jenkins/v3/create/pipeline` | 파이프라인 생성 |
| PUT | `/jenkins/v3/update/pipeline` | 파이프라인 수정 |
| DELETE | `/jenkins/v3/delete/pipeline` | 파이프라인 삭제 |
| POST | `/jenkins/v3/execute/pipeline` | 파이프라인 실행 |
| POST | `/jenkins/v3/stop/pipeline` | 파이프라인 중지 |
| POST | `/jenkins/v3/validate/pipeline` | Jenkinsfile 검증 |
| POST | `/jenkins/v3/upsert/trigger` | 트리거 파이프라인 생성/수정 |
| POST | `/jenkins/v3/execute/trigger` | 트리거 파이프라인 실행 |
| POST | `/jenkins/v3/get/pipeline/last/status` | 최근 빌드 상태 조회 |

### 8.2 Jenkins REST API (Feign Client 호출)

| 용도 | HTTP | Jenkins 경로 |
|------|------|-------------|
| CSRF 토큰 | GET | `/crumbIssuer/api/json` |
| 존재 확인 | GET | `/{struct}/api/json` |
| 폴더 생성 | POST | `/{parent}/createItem` (mode=Folder) |
| 파이프라인 생성 | POST | `/{parent}/createItem` (XML body) |
| 파이프라인 수정 | POST | `/{struct}/config.xml` |
| 파이프라인 삭제 | POST | `/{struct}/doDelete` |
| 실행 (파라미터 없음) | POST | `/{struct}/build` |
| 실행 (파라미터) | POST | `/{struct}/buildWithParameters` |
| 중지 | POST | `/{struct}/{buildNo}/stop` |
| Jenkinsfile 검증 | POST | `/{struct}/descriptorByName/.../checkScriptCompile` |
| 설정 조회 | GET | `/{struct}/config.xml` |
| 빌드 정보 | GET | `/{struct}/{buildNo}/api/json` |
| 전체 로그 | GET | `/{struct}/{buildNo}/logText/progressiveText?start=0` |
| Blue Ocean 노드 | GET | `/blue/rest/.../runs/{buildNo}/nodes/?limit=10000` |
| Blue Ocean 스텝 로그 | GET | `/blue/rest/.../nodes/{nodeId}/steps/{stepId}/log` |
| 크레덴셜 조회 | GET | `/credentials/store/system/domain/{domain}/api/json` |
| 크레덴셜 생성 | POST | `/credentials/store/system/domain/{domain}/createCredentials` |
| 노드 목록 | GET | `/computer/api/json` |

---

## 9. 크레덴셜 관리

pipeline-api는 Jenkins 크레덴셜을 TPS 도메인별로 관리한다. 기본 도메인은 `_`(언더스코어)이며, 업무코드별 도메인을 추가로 생성할 수 있다. 지원하는 크레덴셜 타입은 3가지다.

| 타입 | 용도 | 동기화 메서드 |
|------|------|-------------|
| Username/Password | Git 저장소 인증 | `syncUnPwCredential()` |
| SSH Private Key | SSH 기반 접근 | `syncUnPkCredential()` |
| Secret Text | API 토큰 등 | `syncScTxCredential()` |

`sync*` 메서드는 크레덴셜이 존재하면 업데이트, 없으면 생성하는 upsert 패턴이다.

---

## 10. 주요 VO 구조

**JenkinsToolVo** (도구 접속 정보): TPS DB의 개발지원도구 테이블(TbTpsCm150)에서 조회한 Jenkins 서버 정보를 담는다. `convertJenkinsToolVo()` 메서드가 DB 모델을 이 VO로 변환한다.

```
JenkinsToolVo { url, id, password, basicAuth }
    ↑ convertJenkinsToolVo()
TbTpsCm150 { TL_URL, TL_CNTN_ID, TL_SGNL }
```

**PipelineStructVo** (폴더 경로): taskCd, envrnCd, bizNm 3개 필드로 Jenkins 폴더 경로를 구성한다. bizNm이 비어있으면 트리거 파이프라인으로 판단한다.

**JenkinsJobVo** (파이프라인 작업): PipelineStructVo + Jenkinsfile 스크립트 + 파라미터 목록을 묶은 통합 VO다. `convertToJenkinsJobVo()`가 TPS 도메인의 PipelineUpsertVo를 이 VO로 변환한다.

```
PipelineUpsertVo (TPS 도메인)
  ├ taskCd, envrnCd, bizNm
  ├ pplnScrpt (Jenkinsfile)
  └ intrmdVriabl (JSON 파라미터)
        ↓ convertToJenkinsJobVo()
JenkinsJobVo (Jenkins 도메인)
  ├ pipelineStructVo
  ├ jenkinsFile
  └ jenkinsJobParamVoList
```
