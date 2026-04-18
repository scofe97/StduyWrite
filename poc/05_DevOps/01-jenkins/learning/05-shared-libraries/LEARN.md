# 05. Shared Libraries - 학습 (LEARN)

## 학습 목표

이 문서를 학습하면 다음 질문에 답할 수 있습니다:
- 100개 마이크로서비스의 Jenkinsfile 중복을 어떻게 제거하는가?
- Shared Library의 vars/, src/, resources/ 디렉토리는 각각 어떤 역할을 하는가?
- Pipeline에서 Shared Library를 로딩하는 4가지 방식과 각각의 장단점은?

---

## 1. 왜 Shared Library가 필요한가

> **한 문장 정의**: Jenkins Shared Library는 **여러 Pipeline에서 공유하는 Groovy 코드를 별도 Git 저장소로 분리**하여, CI/CD 로직의 중복을 제거하고 조직 표준을 강제하는 메커니즘입니다.

---

### 문제: Jenkinsfile 복붙의 악순환

마이크로서비스 아키텍처를 채택한 조직에서는 수십~수백 개의 서비스가 존재합니다. 각 서비스의 빌드-테스트-배포 파이프라인은 대부분 동일한 패턴을 따릅니다. 문제는 이 동일한 패턴이 **각 저장소의 Jenkinsfile에 복사-붙여넣기**로 존재한다는 점입니다.

```groovy
// service-A/Jenkinsfile — 100개 서비스 모두 거의 동일
pipeline {
    agent any
    stages {
        stage('Build') {
            steps { sh 'docker build -t service-a .' }
        }
        stage('Test') {
            steps { sh './gradlew test' }
        }
        stage('Security Scan') {
            steps { sh 'trivy image service-a' }
        }
        stage('Deploy') {
            steps { sh 'kubectl apply -f k8s/' }
        }
    }
}
```

이 구조에서 보안 스캔 도구를 Trivy에서 Grype로 교체하려면, **100개 저장소의 Jenkinsfile을 모두 수정**해야 합니다. 하나라도 누락하면 일부 서비스만 새 도구를 사용하는 불일치가 발생합니다.

### 복붙 방식의 구체적 문제

| 문제 | 설명 | 실제 영향 |
|------|------|----------|
| **변경 증폭** | 하나의 로직 변경이 N번의 수정을 요구 | 100개 서비스 = 100개 PR |
| **드리프트(Drift)** | 시간이 지나면 서비스마다 Jenkinsfile이 미묘하게 달라짐 | "왜 service-B만 보안 스캔이 없지?" |
| **거버넌스 부재** | CI/CD 표준을 강제할 수 없음 | 신규 서비스가 보안 스캔 단계를 빼먹어도 알 수 없음 |
| **온보딩 비용** | 새 개발자가 "올바른" Jenkinsfile을 어디서 복사해야 하는지 모름 | 오래된 템플릿을 복사하여 안티패턴 전파 |

### 해결: DRY 원칙과 중앙화

Shared Library는 이 문제를 **공통 로직을 별도 Git 저장소로 추출**하여 해결합니다. 각 Jenkinsfile은 라이브러리의 함수를 호출하기만 하므로, 변경이 필요하면 **라이브러리 저장소 한 곳만 수정**하면 됩니다.

```groovy
// service-A/Jenkinsfile — Shared Library 적용 후
@Library('my-pipeline-lib') _

standardPipeline(
    serviceName: 'service-a',
    deployTarget: 'production'
)
```

100줄이던 Jenkinsfile이 5줄로 줄었습니다. 보안 스캔 도구를 교체하려면 라이브러리의 `standardPipeline.groovy` 한 파일만 수정하면 100개 서비스에 동시에 반영됩니다.

### 거버넌스 관점

Shared Library는 단순한 코드 재사용을 넘어 **조직의 CI/CD 정책을 코드로 강제**하는 도구입니다. 라이브러리에 보안 스캔 단계를 포함시키면, 이 라이브러리를 사용하는 모든 Pipeline이 자동으로 보안 스캔을 수행합니다. 개별 팀이 "빌드 속도를 위해 보안 스캔을 생략"하는 것을 구조적으로 방지할 수 있기 때문에, 플랫폼 엔지니어링 팀이 조직 전체의 CI/CD 품질을 관리하는 핵심 수단이 됩니다.

```mermaid
graph LR
    subgraph "Before: 복붙 방식"
        A1[service-A<br/>Jenkinsfile] --- C1[빌드-테스트-배포<br/>로직 직접 포함]
        A2[service-B<br/>Jenkinsfile] --- C2[빌드-테스트-배포<br/>로직 직접 포함]
        A3[service-C<br/>Jenkinsfile] --- C3[빌드-테스트-배포<br/>로직 직접 포함]
    end

    subgraph "After: Shared Library"
        B1[service-A<br/>Jenkinsfile] --> L[Shared Library<br/>Git 저장소]
        B2[service-B<br/>Jenkinsfile] --> L
        B3[service-C<br/>Jenkinsfile] --> L
        L --- D["standardPipeline()<br/>buildDocker()<br/>deployTo()"]
    end

    style L fill:#4CAF50,color:#fff
```

> 위 다이어그램은 Shared Library 도입 전후를 비교합니다. **Before**에서는 각 서비스가 동일한 로직을 각자 갖고 있어서 변경 시 N번 수정해야 하지만, **After**에서는 공통 로직이 라이브러리 한 곳에 집중되어 변경이 1번만 필요합니다.

---

## 2. Shared Library 구조

Jenkins Shared Library는 특정 디렉토리 구조를 따르는 Git 저장소입니다. 이 구조를 지켜야 Jenkins가 라이브러리를 올바르게 로딩하고, Pipeline에서 호출할 수 있습니다.

```
my-pipeline-lib/          # Git 저장소 루트
├── vars/                  # 전역 변수/함수 — Pipeline에서 직접 호출
│   ├── buildDocker.groovy       # buildDocker() 로 호출
│   ├── deployTo.groovy          # deployTo() 로 호출
│   ├── notifySlack.groovy       # notifySlack() 로 호출
│   └── standardPipeline.groovy  # standardPipeline() 로 호출
├── src/                   # Groovy 클래스 — import로 사용
│   └── com/
│       └── example/
│           ├── PipelineHelper.groovy
│           └── DockerConfig.groovy
└── resources/             # 설정 파일, 템플릿
    ├── deploy-template.yaml
    └── sonar-config.properties
```

### 디렉토리별 역할

| 디렉토리 | 역할 | 접근 방식 | 사용 시점 |
|----------|------|----------|----------|
| **vars/** | Pipeline에서 **함수처럼** 호출되는 전역 변수 | 파일명이 곧 함수명: `buildDocker.groovy` → `buildDocker()` | 단순한 빌드 단계, 알림, 배포 등 **Pipeline DSL 수준의 동작** |
| **src/** | 일반 Groovy 클래스 (OOP 패턴) | `import com.example.PipelineHelper` | 복잡한 비즈니스 로직, 설정 객체, 유틸리티 클래스 |
| **resources/** | 정적 파일 (YAML, JSON, 템플릿 등) | `libraryResource('deploy-template.yaml')` | 배포 매니페스트 템플릿, 설정 파일 |

### vars/ 디렉토리 상세

vars/의 핵심 규칙은 **파일명 = 함수명**이라는 점입니다. `buildDocker.groovy` 파일을 만들면 Pipeline에서 `buildDocker()`로 호출할 수 있습니다. 이것이 가능한 이유는 Jenkins가 vars/ 디렉토리의 각 `.groovy` 파일을 **전역 스코프에 바인딩**하기 때문입니다.

각 파일은 `call()` 메서드를 정의해야 합니다. Pipeline에서 `buildDocker(imageName: 'my-app')`을 호출하면 실제로는 `buildDocker.groovy`의 `call(imageName: 'my-app')`이 실행됩니다.

### src/ 디렉토리 상세

src/는 일반 Groovy 소스 코드를 담습니다. Java와 동일한 패키지 구조를 따르며, 클래스를 정의하고 import하여 사용합니다. vars/의 함수들이 복잡해질 때 로직을 분리하는 용도로 사용합니다. 단, src/ 클래스에서는 Pipeline DSL(`sh`, `stage` 등)을 직접 사용할 수 없습니다. Pipeline 컨텍스트가 필요하면 vars/에서 컨텍스트를 전달받아야 합니다.

### resources/ 디렉토리 상세

resources/는 `libraryResource()` 함수로 로드할 수 있는 정적 파일을 담습니다. 배포 매니페스트 템플릿, SonarQube 설정 파일 등을 여기에 두면 라이브러리와 함께 버전 관리됩니다.

```groovy
// vars/deployTo.groovy 에서 resources/ 파일 로드
def template = libraryResource('deploy-template.yaml')
def rendered = template.replace('{{SERVICE_NAME}}', config.serviceName)
writeFile file: 'deploy.yaml', text: rendered
```

```mermaid
graph TB
    subgraph "Shared Library 저장소"
        V["vars/<br/>buildDocker.groovy<br/>deployTo.groovy<br/>notifySlack.groovy"]
        S["src/<br/>com.example.<br/>PipelineHelper"]
        R["resources/<br/>deploy-template.yaml"]
    end

    subgraph "Jenkinsfile"
        J["@Library('my-lib') _<br/>buildDocker(imageName: 'app')<br/>deployTo(env: 'prod')"]
    end

    J -- "함수 호출" --> V
    V -- "import" --> S
    V -- "libraryResource()" --> R

    style V fill:#2196F3,color:#fff
    style S fill:#FF9800,color:#fff
    style R fill:#9C27B0,color:#fff
```

> 위 다이어그램은 Jenkinsfile에서 Shared Library의 각 디렉토리가 어떻게 연결되는지를 보여줍니다. Pipeline은 **vars/ 함수를 직접 호출**하고, vars/ 함수는 필요에 따라 **src/ 클래스를 import**하거나 **resources/ 파일을 로드**합니다. Pipeline이 src/나 resources/에 직접 접근하는 것이 아니라, 항상 vars/를 통해 간접적으로 사용한다는 점이 핵심입니다.

---

## 3. 로딩 메커니즘

Shared Library를 Pipeline에서 사용하려면 먼저 **로딩**해야 합니다. Jenkins는 4가지 로딩 방식을 제공하며, 각각의 적합한 상황이 다릅니다.

### 3-1. Explicit Loading (@Library 어노테이션)

```groovy
@Library('my-pipeline-lib') _
// 또는
@Library('my-pipeline-lib@main') _

pipeline {
    agent any
    stages {
        stage('Build') {
            steps { buildDocker(imageName: 'my-app') }
        }
    }
}
```

`@Library` 어노테이션을 Jenkinsfile 최상단에 선언합니다. 뒤의 `_`(언더스코어)는 Groovy 문법상 어노테이션이 적용될 대상이 필요하기 때문에 사용하는 더미 심볼입니다. 어떤 라이브러리를 사용하는지 Jenkinsfile에 명시적으로 드러나므로 가독성이 좋습니다.

### 3-2. Implicit Loading (전역 설정)

Jenkins 관리 화면(Manage Jenkins > System > Global Pipeline Libraries)에서 라이브러리를 등록하고 "Load implicitly" 옵션을 활성화하면, **모든 Pipeline에 자동으로 로딩**됩니다. Jenkinsfile에 `@Library` 선언 없이도 vars/ 함수를 바로 사용할 수 있습니다.

이 방식은 조직 전체에 CI/CD 표준 라이브러리를 강제할 때 유용합니다. 다만 Jenkinsfile만 보면 어떤 라이브러리가 로딩되는지 알 수 없어서 **디버깅이 어려워질 수 있습니다**.

### 3-3. Version Pinning (버전 고정)

```groovy
// 특정 브랜치
@Library('my-pipeline-lib@main') _

// 특정 태그
@Library('my-pipeline-lib@v1.2.0') _

// 특정 커밋
@Library('my-pipeline-lib@a1b2c3d') _
```

`@` 뒤에 Git 브랜치, 태그, 또는 커밋 해시를 지정하여 **특정 버전의 라이브러리를 고정**합니다. 버전을 고정하지 않으면 Jenkins 전역 설정에서 지정한 기본 브랜치(보통 main)를 사용합니다.

버전 고정이 중요한 이유는, 라이브러리에 breaking change가 발생했을 때 **모든 Pipeline이 동시에 깨지는 것을 방지**하기 때문입니다. 프로덕션 Pipeline은 안정적인 태그 버전을 사용하고, 개발 Pipeline은 최신 브랜치를 사용하는 식으로 분리할 수 있습니다.

### 3-4. Dynamic Loading (런타임 로딩)

```groovy
// Pipeline 실행 중에 동적으로 라이브러리 로딩
def lib = library('my-pipeline-lib@feature-branch')

pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                script {
                    lib.com.example.PipelineHelper.build()
                }
            }
        }
    }
}
```

`library()` 함수를 사용하면 Pipeline 실행 중에 동적으로 라이브러리를 로딩할 수 있습니다. 조건에 따라 다른 버전의 라이브러리를 로딩하거나, 특정 단계에서만 라이브러리가 필요한 경우에 사용합니다. 단, vars/ 함수는 전역 스코프에 바인딩되지 않으므로 접근 방식이 달라진다는 점에 주의해야 합니다.

### 로딩 방식 비교

| 방식 | 선언 위치 | 적합한 상황 | 주의사항 |
|------|----------|------------|---------|
| **Explicit** | Jenkinsfile | 대부분의 경우 (권장) | 명시적이라 추적 용이 |
| **Implicit** | Jenkins 전역 설정 | 조직 표준 라이브러리 강제 | Jenkinsfile에 안 보여서 디버깅 어려움 |
| **Version Pinning** | Jenkinsfile | 프로덕션 안정성 확보 | 라이브러리 업데이트를 수동으로 반영해야 함 |
| **Dynamic** | Pipeline 스크립트 내부 | 조건부 로딩, 실험 | vars/ 전역 바인딩 안 됨 |

```mermaid
sequenceDiagram
    participant JF as Jenkinsfile
    participant JM as Jenkins Master
    participant Git as Library Git 저장소
    participant Exec as Pipeline 실행

    JF->>JM: Pipeline 시작
    JM->>JM: @Library 어노테이션 파싱<br/>또는 Implicit Library 확인

    JM->>Git: 지정 버전(브랜치/태그) checkout
    Git-->>JM: vars/, src/, resources/ 반환

    JM->>JM: vars/*.groovy를<br/>전역 스코프에 바인딩
    JM->>JM: src/ 클래스패스에 추가

    JM->>Exec: Pipeline 실행 시작
    Exec->>Exec: buildDocker() 호출
    Note over Exec: vars/buildDocker.groovy<br/>의 call() 메서드 실행
    Exec->>Exec: deployTo() 호출
    Note over Exec: vars/deployTo.groovy<br/>의 call() 메서드 실행
```

> 위 시퀀스 다이어그램은 Pipeline이 시작되었을 때 Shared Library가 로딩되는 과정을 보여줍니다. Jenkins Master가 라이브러리 Git 저장소에서 코드를 가져온 뒤, vars/ 파일들을 전역 스코프에 바인딩하여 Pipeline에서 함수처럼 호출할 수 있게 합니다. 이 과정은 Pipeline의 실제 단계(stage)가 실행되기 **전에** 완료됩니다.

---

## 4. 실전 패턴: vars/ 함수 구현

### 4-1. 기본 패턴: call() 메서드와 Map config

```groovy
// vars/buildDocker.groovy
def call(Map config = [:]) {
    def imageName = config.imageName ?: error("imageName is required")
    def tag = config.tag ?: env.BUILD_NUMBER
    def dockerfile = config.dockerfile ?: 'Dockerfile'

    stage('Docker Build') {
        sh "docker build -t ${imageName}:${tag} -f ${dockerfile} ."
    }
    stage('Docker Push') {
        docker.withRegistry('https://registry.example.com', 'registry-cred') {
            sh "docker push ${imageName}:${tag}"
            sh "docker push ${imageName}:latest"
        }
    }

    return "${imageName}:${tag}"
}
```

**왜 Map config 패턴을 사용하는가?** 일반적인 위치 기반 파라미터(`def call(String imageName, String tag)`)는 파라미터가 늘어날수록 호출부가 읽기 어려워집니다. Map을 사용하면 `buildDocker(imageName: 'my-app', tag: 'v1.0')`처럼 **이름 기반으로 호출**할 수 있어 가독성이 높아집니다. 또한 기본값을 `?:` 연산자로 쉽게 지정할 수 있고, 새 파라미터를 추가해도 기존 호출부가 깨지지 않습니다.

**필수 파라미터 검증**: `config.imageName ?: error("imageName is required")`는 imageName이 null이면 Pipeline을 즉시 실패시킵니다. 파라미터 누락을 빌드 실행 초기에 잡아내어, 30분 뒤에 배포 단계에서 실패하는 것보다 빠른 피드백을 줍니다.

### 4-2. 표준 Pipeline 패턴

```groovy
// vars/standardPipeline.groovy
def call(Map config = [:]) {
    def serviceName = config.serviceName ?: error("serviceName is required")
    def deployTarget = config.deployTarget ?: 'staging'
    def skipTests = config.skipTests ?: false

    pipeline {
        agent any

        stages {
            stage('Checkout') {
                steps { checkout scm }
            }
            stage('Build') {
                steps { buildDocker(imageName: serviceName) }
            }
            stage('Test') {
                when { expression { !skipTests } }
                steps { sh './gradlew test' }
            }
            stage('Security Scan') {
                steps { sh "trivy image ${serviceName}:${env.BUILD_NUMBER}" }
            }
            stage('Deploy') {
                steps { deployTo(service: serviceName, env: deployTarget) }
            }
        }

        post {
            success { notifySlack(channel: '#deploys', status: 'SUCCESS') }
            failure { notifySlack(channel: '#deploys', status: 'FAILURE') }
        }
    }
}
```

이 패턴에서 `standardPipeline`은 **전체 Pipeline을 캡슐화**합니다. 개별 서비스의 Jenkinsfile은 단 몇 줄만으로 조직의 전체 CI/CD 표준을 따르게 됩니다. 보안 스캔 단계가 라이브러리에 포함되어 있으므로, 개별 팀이 이 단계를 생략할 수 없습니다.

### 4-3. src/ 클래스 활용

```groovy
// src/com/example/DockerConfig.groovy
package com.example

class DockerConfig implements Serializable {
    String registry = 'registry.example.com'
    String credentialsId = 'registry-cred'

    String fullImageName(String name, String tag) {
        return "${registry}/${name}:${tag}"
    }

    boolean shouldPush(String branch) {
        return branch in ['main', 'release']
    }
}
```

```groovy
// vars/buildDocker.groovy 에서 src/ 클래스 사용
import com.example.DockerConfig

def call(Map config = [:]) {
    def dockerConfig = new DockerConfig()
    def imageName = config.imageName ?: error("imageName required")
    def tag = config.tag ?: env.BUILD_NUMBER
    def fullName = dockerConfig.fullImageName(imageName, tag)

    stage('Docker Build') {
        sh "docker build -t ${fullName} ."
    }

    if (dockerConfig.shouldPush(env.BRANCH_NAME)) {
        stage('Docker Push') {
            docker.withRegistry("https://${dockerConfig.registry}", dockerConfig.credentialsId) {
                sh "docker push ${fullName}"
            }
        }
    }
}
```

**왜 src/ 클래스를 분리하는가?** vars/ 함수가 복잡해지면 로직을 테스트하기 어려워집니다. 순수 로직(이미지 이름 생성, 조건 판단 등)을 src/ 클래스로 분리하면 Jenkins 환경 없이도 **단위 테스트가 가능**합니다. `Serializable`을 구현하는 이유는 Jenkins Pipeline이 실행 중간에 직렬화/역직렬화를 수행하기 때문입니다(Pipeline CPS 변환).

---

## 5. 테스트 전략

Shared Library는 조직 전체의 CI/CD를 담당하므로, 라이브러리의 버그가 모든 서비스의 배포를 중단시킬 수 있습니다. 따라서 **라이브러리 자체의 테스트**가 매우 중요합니다.

### 5-1. Jenkins Pipeline Unit 프레임워크

[Jenkins Pipeline Unit](https://github.com/jenkinsci/JenkinsPipelineUnit)은 Jenkins 없이 Pipeline 코드를 테스트할 수 있는 프레임워크입니다. Pipeline DSL(`sh`, `stage`, `docker` 등)을 모킹하여 vars/ 함수의 로직을 검증합니다.

```groovy
// test/BuildDockerTest.groovy
import com.lesfurets.jenkins.unit.BasePipelineTest
import org.junit.Before
import org.junit.Test

class BuildDockerTest extends BasePipelineTest {

    @Before
    void setUp() {
        super.setUp()
        binding.setVariable('env', [BUILD_NUMBER: '42'])
    }

    @Test
    void 'imageName_필수_파라미터_누락시_에러'() {
        def script = loadScript('vars/buildDocker.groovy')
        try {
            script.call([:])
            fail('에러가 발생해야 함')
        } catch (Exception e) {
            assert e.message.contains('imageName is required')
        }
    }

    @Test
    void '기본_태그는_BUILD_NUMBER를_사용'() {
        def script = loadScript('vars/buildDocker.groovy')
        script.call(imageName: 'my-app')

        // docker build 명령어에 BUILD_NUMBER가 포함되었는지 검증
        assertJobStatusSuccess()
    }
}
```

### 5-2. src/ 클래스 단위 테스트

src/ 클래스는 Jenkins 의존성이 없으므로 일반 Groovy/Spock 테스트로 검증합니다.

```groovy
// test/DockerConfigTest.groovy
import com.example.DockerConfig
import spock.lang.Specification

class DockerConfigTest extends Specification {

    def 'fullImageName이_레지스트리를_포함해야_함'() {
        given:
        def config = new DockerConfig()

        when:
        def result = config.fullImageName('my-app', 'v1.0')

        then:
        result == 'registry.example.com/my-app:v1.0'
    }

    def 'main과_release_브랜치만_push_허용'() {
        given:
        def config = new DockerConfig()

        expect:
        config.shouldPush('main') == true
        config.shouldPush('release') == true
        config.shouldPush('feature-x') == false
    }
}
```

### 5-3. 라이브러리 개발 워크플로우

```mermaid
graph LR
    A["feature 브랜치<br/>생성"] --> B["코드 작성<br/>+ 단위 테스트"]
    B --> C["PR 생성<br/>코드 리뷰"]
    C --> D["테스트 Pipeline에서<br/>@Library('lib@feature-branch')<br/>로 검증"]
    D --> E{"통과?"}
    E -- "Yes" --> F["main 머지"]
    E -- "No" --> B
    F --> G["태그 생성<br/>v1.3.0"]
    G --> H["프로덕션 Pipeline<br/>@Library('lib@v1.3.0')"]

    style D fill:#FF9800,color:#fff
    style G fill:#4CAF50,color:#fff
    style H fill:#2196F3,color:#fff
```

> 위 다이어그램은 Shared Library의 개발부터 프로덕션 적용까지의 워크플로우를 보여줍니다. 핵심은 **테스트 Pipeline에서 feature 브랜치를 직접 로딩하여 검증**하는 단계(주황색)입니다. 이 단계에서 실제 Jenkins 환경에서 라이브러리가 제대로 동작하는지 확인한 후에야 main에 머지합니다. 프로덕션 Pipeline은 **태그 버전을 고정**하여 안정성을 보장합니다.

### 5-4. 버전 관리 전략

| 브랜치/태그 | 용도 | 사용 대상 |
|------------|------|----------|
| `main` | 최신 안정 버전 | 스테이징 Pipeline |
| `develop` | 실험적 기능 | 개발자 로컬 테스트 |
| `v1.x.x` 태그 | 프로덕션 고정 버전 | 프로덕션 Pipeline |
| `feature/*` | 신규 기능 개발 | 테스트 Pipeline |

Semantic Versioning을 따르되, **breaking change가 있으면 반드시 메이저 버전을 올려야** 합니다. 그렇지 않으면 `@Library('lib@v1')` 형태의 와일드카드 버전을 사용하는 Pipeline이 예상치 못하게 깨질 수 있습니다.

---

## 핵심 정리

| 개념 | 핵심 | 왜 중요한가 |
|------|------|------------|
| **Shared Library** | 공통 CI/CD 로직을 별도 Git 저장소로 분리 | 중복 제거 + 거버넌스 강제 |
| **vars/** | 파일명 = 함수명, call() 메서드 | Pipeline에서 직접 호출하는 진입점 |
| **src/** | 일반 Groovy 클래스 | 복잡한 로직 분리 + 단위 테스트 가능 |
| **resources/** | 정적 파일 | 설정/템플릿의 버전 관리 |
| **Version Pinning** | @Library('lib@v1.2.0') | 프로덕션 안정성 보장 |
| **Implicit Loading** | 전역 자동 로딩 | 조직 표준 강제 |
| **테스트** | Jenkins Pipeline Unit + Spock | 라이브러리 버그 = 전사 장애 방지 |
