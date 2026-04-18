# Ch10. Groovy 커스터마이징과 Init Hook

**핵심 질문**: "Jenkins를 Groovy로 커스터마이징하는 것은 어디까지 가능하고, 어디부터 위험한가?"

---

## 1. Jenkins와 Groovy의 관계

### 왜 Groovy인가

Jenkins는 Java로 작성된 애플리케이션이지만, 설정과 확장의 핵심 언어로 Groovy를 사용합니다. 이 선택은 우연이 아닙니다. Groovy는 JVM 위에서 동작하므로 Jenkins의 모든 Java 클래스에 직접 접근할 수 있고, Java와 거의 동일한 문법을 가지면서도 스크립팅에 적합한 동적 타이핑을 지원합니다. 즉, Jenkins 내부 API를 호출하면서도 별도의 컴파일 과정 없이 즉시 실행할 수 있는 언어가 필요했고, Groovy가 그 조건을 완벽하게 충족했습니다.

구체적으로 Groovy가 Jenkins에 적합한 이유는 세 가지입니다. 첫째, **JVM 호환성**입니다. Groovy 코드는 JVM 바이트코드로 컴파일되므로 Jenkins의 Java 클래스를 `import`하여 직접 호출할 수 있습니다. 별도의 브릿지나 FFI(Foreign Function Interface)가 필요 없습니다. 둘째, **문법적 간결함**입니다. Java에서 10줄이 필요한 코드를 Groovy에서는 3줄로 작성할 수 있습니다. 세미콜론 생략, 클로저, GString 같은 편의 기능이 관리 스크립트 작성에 생산성을 높여줍니다. 셋째, **동적 타이핑**입니다. 런타임에 타입을 결정하므로 탐색적 스크립팅, 즉 "이 API가 무엇을 반환하는지 실행해보면서 확인하는" 작업에 유리합니다.

### Groovy가 사용되는 3가지 영역

Jenkins에서 Groovy는 명확히 구분되는 세 가지 영역에서 사용되며, 각 영역의 보안 수준과 실행 컨텍스트가 다릅니다.

```mermaid
flowchart TB
    subgraph jenkins["Jenkins 내부"]
        direction TB

        subgraph area1["1. Pipeline DSL<br/>(Jenkinsfile)"]
            P1["Sandbox 환경에서 실행"]
            P2["제한된 API 접근"]
            P3["개발자가 작성"]
        end

        subgraph area2["2. Script Console<br/>(Manage Jenkins)"]
            S1["Sandbox 없음"]
            S2["모든 Internal API 접근"]
            S3["관리자만 접근"]
        end

        subgraph area3["3. Init Hook<br/>(init.groovy.d/)"]
            I1["Jenkins 시작 시 실행"]
            I2["모든 Internal API 접근"]
            I3["파일 시스템 접근 필요"]
        end
    end

    area1 -. "보안 수준: 높음<br/>(Sandbox)" .-> area2
    area2 -. "보안 수준: 없음<br/>(무제한)" .-> area3
    area3 -. "보안 수준: 없음<br/>(무제한, 시작 시점)" .-> area1

    style area1 fill:#d4edda,stroke:#28a745,color:#333
    style area2 fill:#f8d7da,stroke:#dc3545,color:#333
    style area3 fill:#fff3cd,stroke:#ffc107,color:#333
```

**영역 1: Pipeline DSL (Jenkinsfile)**은 가장 일상적인 Groovy 사용처입니다. 개발자가 `Jenkinsfile`에 `pipeline { ... }` 블록을 작성하면, Jenkins는 이것을 Groovy 코드로 해석하고 실행합니다. 이 영역에서는 **Script Security Plugin**이 Sandbox를 적용하여 위험한 API 호출을 차단합니다. 개발자가 `System.exit(0)`을 Pipeline에 넣어도 실행되지 않고 관리자 승인을 요구합니다.

**영역 2: Script Console (Manage Jenkins > Script Console)**은 Jenkins 관리자가 Groovy 코드를 직접 입력하여 실행하는 인터페이스입니다. 이 콘솔은 Sandbox가 적용되지 않으므로 Jenkins의 모든 Internal API에 무제한으로 접근할 수 있습니다. 크레덴셜을 평문으로 읽을 수도 있고, 모든 Job을 삭제할 수도 있습니다. 강력하지만 그만큼 위험한 영역입니다.

**영역 3: Init Hook (JENKINS_HOME/init.groovy.d/)**은 Jenkins가 시작될 때 자동으로 실행되는 Groovy 스크립트입니다. Script Console과 동일한 권한을 가지지만, 사용자가 직접 실행하는 것이 아니라 Jenkins 프로세스가 시작 시점에 자동으로 실행합니다. 주로 초기 설정 자동화에 사용됩니다.

이 세 영역의 핵심적인 차이는 **누가 실행하느냐**와 **어떤 보안 경계 안에서 실행되느냐**입니다. Pipeline DSL은 개발자가 작성하고 Sandbox에서 실행되며, Script Console은 관리자가 직접 실행하고 보안 경계가 없으며, Init Hook은 시스템이 자동 실행하고 보안 경계가 없습니다.

---

## 2. Init Groovy Hook (전역 초기화 스크립트)

### 실행 시점과 메커니즘

`JENKINS_HOME/init.groovy.d/` 디렉토리는 Jenkins의 "부팅 스크립트" 폴더입니다. Jenkins 프로세스가 시작되면 이 디렉토리 안의 모든 `.groovy` 파일을 알파벳 순서로 실행합니다. 실행 시점은 플러그인 로딩 이후, 웹 UI가 준비되기 전입니다. 이 타이밍이 중요한데, 플러그인이 로딩된 상태이므로 플러그인 API를 호출할 수 있지만, 아직 사용자 요청을 받기 전이므로 초기 설정을 안전하게 적용할 수 있기 때문입니다.

```mermaid
sequenceDiagram
    participant JVM as JVM 프로세스
    participant Core as Jenkins Core
    participant Plugin as 플러그인 매니저
    participant Init as init.groovy.d/
    participant UI as 웹 UI

    JVM->>Core: Jenkins 시작
    Core->>Core: 기본 설정 로딩<br/>(JENKINS_HOME/config.xml)
    Core->>Plugin: 플러그인 로딩 시작
    Plugin->>Plugin: 모든 플러그인 초기화<br/>(HPI/JPI 파일)
    Plugin-->>Core: 플러그인 로딩 완료

    rect rgb(255, 243, 205)
        Note over Init: init.groovy.d/ 실행 구간
        Core->>Init: *.groovy 파일 탐색<br/>(알파벳 순서)
        Init->>Init: 01-security.groovy 실행
        Init->>Init: 02-credentials.groovy 실행
        Init->>Init: 03-tools.groovy 실행
        Init-->>Core: 모든 스크립트 실행 완료
    end

    Core->>UI: 웹 UI 초기화
    UI-->>Core: Jenkins 준비 완료<br/>(포트 리스닝 시작)
```

왜 이 순서가 중요할까요? 만약 init.groovy.d가 플러그인 로딩 전에 실행된다면, 특정 플러그인의 API를 호출하는 스크립트가 `ClassNotFoundException`으로 실패할 것입니다. 반대로 UI가 준비된 후에 실행된다면, 보안 설정이 적용되기 전에 사용자가 접근할 수 있는 시간 창이 열립니다. 플러그인 로딩 직후, UI 준비 직전이라는 타이밍은 이 두 가지 문제를 모두 피하는 최적의 시점입니다.

### 파일 네이밍 컨벤션

init.groovy.d 안의 스크립트는 알파벳 순서로 실행되므로, 숫자 접두사를 붙여 실행 순서를 명시적으로 제어하는 것이 관례입니다.

```
JENKINS_HOME/init.groovy.d/
├── 01-security-realm.groovy      # 보안 설정 (가장 먼저)
├── 02-authorization.groovy       # 인가 전략
├── 03-csrf-protection.groovy     # CSRF 보호
├── 04-credentials.groovy         # 크레덴셜 등록
├── 05-global-tools.groovy        # 전역 도구 설정 (JDK, Maven)
└── 99-final-save.groovy          # 최종 저장
```

### 활용 사례와 코드 예시

**사례 1: 관리자 계정 자동 생성**

Docker 기반 Jenkins를 처음 시작할 때 관리자 계정을 자동으로 설정하는 가장 일반적인 사례입니다. 초기 설정 마법사를 건너뛰고 바로 사용 가능한 상태로 만들 수 있습니다.

```groovy
import jenkins.model.*
import hudson.security.*

def instance = Jenkins.getInstance()

// HudsonPrivateSecurityRealm: Jenkins 내장 사용자 DB를 사용하는 인증 방식
// false 파라미터는 "사용자 자가 등록 비허용"을 의미
def hudsonRealm = new HudsonPrivateSecurityRealm(false)
hudsonRealm.createAccount("admin", "admin-password")
instance.setSecurityRealm(hudsonRealm)

// FullControlOnceLoggedInAuthorizationStrategy:
// 로그인한 사용자에게 전체 권한, 비인증 사용자는 접근 불가
def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
strategy.setAllowAnonymousRead(false)
instance.setAuthorizationStrategy(strategy)

instance.save()
println "[init] Admin account created and security configured."
```

왜 이것이 필요할까요? Jenkins Docker 이미지를 CI/CD 파이프라인으로 자동 배포할 때, 초기 설정 마법사를 수동으로 진행할 수 없기 때문입니다. 특히 Kubernetes 환경에서 Pod이 재시작될 때마다 일관된 초기 상태를 보장해야 합니다.

**사례 2: CSRF 보호 및 Agent 프로토콜 설정**

```groovy
import jenkins.model.*
import hudson.security.csrf.DefaultCrumbIssuer
import jenkins.security.s2m.AdminWhitelistRule

def instance = Jenkins.getInstance()

// CSRF Protection 활성화 — 웹 UI에서의 CSRF 공격 방지
instance.setCrumbIssuer(new DefaultCrumbIssuer(true))

// Agent → Master 접근 제한 — Agent가 Master의 파일시스템에 접근하는 것을 차단
// 왜 중요한가: 악의적인 Agent가 Master의 크레덴셜이나 설정을 읽을 수 있기 때문
instance.getInjector().getInstance(AdminWhitelistRule.class)
    .setMasterKillSwitch(false)

instance.save()
println "[init] CSRF protection enabled, Agent protocol secured."
```

**사례 3: 크레덴셜 자동 등록 (환경변수 기반)**

```groovy
import jenkins.model.*
import com.cloudbees.plugins.credentials.*
import com.cloudbees.plugins.credentials.domains.*
import com.cloudbees.plugins.credentials.impl.*
import org.jenkinsci.plugins.plaincredentials.impl.*
import hudson.util.Secret

def env = System.getenv()

// 환경변수에서 크레덴셜 값을 읽어 Jenkins Credentials Store에 등록
// 왜 환경변수인가: Docker/K8s에서 Secret을 환경변수로 주입하는 것이 표준 패턴
def store = Jenkins.getInstance()
    .getExtensionList('com.cloudbees.plugins.credentials.SystemCredentialsProvider')[0]
    .getStore()

def domain = Domain.global()

// Git 접근용 Username/Password
if (env.containsKey('GIT_USER') && env.containsKey('GIT_TOKEN')) {
    def gitCred = new UsernamePasswordCredentialsImpl(
        CredentialsScope.GLOBAL,
        "git-credentials",           // credentials ID
        "Git Access Token",          // description
        env['GIT_USER'],             // username
        env['GIT_TOKEN']             // password
    )
    store.addCredentials(domain, gitCred)
    println "[init] Git credentials registered."
}

// Docker Registry 접근용 Secret Text
if (env.containsKey('DOCKER_REGISTRY_TOKEN')) {
    def dockerCred = new StringCredentialsImpl(
        CredentialsScope.GLOBAL,
        "docker-registry-token",
        "Docker Registry Token",
        Secret.fromString(env['DOCKER_REGISTRY_TOKEN'])
    )
    store.addCredentials(domain, dockerCred)
    println "[init] Docker registry credentials registered."
}
```

이 패턴이 권장되는가? **조건부로 권장**됩니다. JCasC(Configuration as Code)가 크레덴셜 등록을 지원하지만, 복잡한 조건부 로직(환경변수 존재 여부에 따른 분기)이 필요할 때는 init.groovy.d가 더 유연합니다. 다만 환경변수에 비밀값을 넣는 것 자체의 보안 고려가 필요합니다. Kubernetes라면 Secret 리소스를, Docker라면 Docker Secret을 사용해야 합니다.

---

## 3. Script Console로 할 수 있는 것들

### Script Console의 본질

Jenkins Script Console (Manage Jenkins > Script Console)은 Jenkins 프로세스 내부에서 Groovy 코드를 직접 실행하는 REPL(Read-Eval-Print Loop)입니다. 이것이 의미하는 바는, Jenkins의 모든 Java 객체에 접근할 수 있다는 것입니다. Jenkins 인스턴스, 모든 Job, 모든 빌드, 모든 크레덴셜, 모든 에이전트, 플러그인 설정까지 읽고 수정할 수 있습니다.

```mermaid
flowchart TB
    SC["Script Console<br/>(Groovy REPL)"]

    SC --> JI["Jenkins.getInstance()"]

    JI --> Jobs["모든 Job<br/>생성/수정/삭제"]
    JI --> Builds["모든 빌드 기록<br/>조회/삭제"]
    JI --> Creds["Credentials Store<br/>조회/추가/⚠️복호화"]
    JI --> Agents["모든 Agent<br/>상태 관리/삭제"]
    JI --> Plugins["플러그인 정보<br/>조회/활성화/비활성화"]
    JI --> Security["보안 설정<br/>인증/인가 변경"]
    JI --> System["시스템 프로퍼티<br/>JVM 설정 변경"]

    style SC fill:#dc3545,color:#fff
    style Creds fill:#f8d7da,stroke:#dc3545,color:#333
    style Security fill:#f8d7da,stroke:#dc3545,color:#333
    style System fill:#f8d7da,stroke:#dc3545,color:#333
```

### 실용적 스크립트 예시

**빌드 기록 정리**: 디스크 공간이 부족할 때 오래된 빌드 기록을 대량 삭제합니다.

```groovy
import jenkins.model.*

def daysToKeep = 30

Jenkins.getInstance().getAllItems(hudson.model.Job.class).each { job ->
    job.getBuilds().each { build ->
        def buildDate = new Date(build.getTimeInMillis())
        def cutoffDate = new Date() - daysToKeep

        if (buildDate.before(cutoffDate)) {
            println "Deleting: ${job.fullName} #${build.number} (${buildDate})"
            build.delete()
        }
    }
}
println "Cleanup complete."
```

**Agent 상태 조회**: 모든 Agent의 온/오프라인 상태와 실행 중인 빌드를 확인합니다.

```groovy
import jenkins.model.*
import hudson.model.*

Jenkins.getInstance().getNodes().each { node ->
    def computer = node.toComputer()
    def status = computer?.isOnline() ? "ONLINE" : "OFFLINE"
    def executors = computer?.countBusy() ?: 0
    def total = computer?.countExecutors() ?: 0

    println "${node.displayName}: ${status} (${executors}/${total} executors busy)"

    if (!computer?.isOnline()) {
        println "  Offline cause: ${computer?.getOfflineCause()}"
    }
}
```

**플러그인 정보 조회**: 설치된 모든 플러그인의 버전과 업데이트 가능 여부를 확인합니다.

```groovy
import jenkins.model.*

Jenkins.getInstance().getPluginManager().getPlugins().sort { it.getShortName() }.each { plugin ->
    def update = plugin.hasUpdate() ? " [UPDATE AVAILABLE]" : ""
    println "${plugin.getShortName()} (${plugin.getVersion()})${update}"
}
```

### Script Console의 보안 위험

Script Console의 가장 심각한 보안 문제는 **크레덴셜 평문 노출**입니다. 다음 코드는 Jenkins에 저장된 모든 크레덴셜의 비밀값을 평문으로 출력할 수 있습니다.

```groovy
// ⚠️ 위험: 크레덴셜을 평문으로 노출하는 스크립트
// 이것이 가능하다는 사실 자체가 Script Console 접근 제한의 이유
import com.cloudbees.plugins.credentials.*
import com.cloudbees.plugins.credentials.impl.*

def creds = CredentialsProvider.lookupCredentials(
    com.cloudbees.plugins.credentials.common.StandardCredentials.class,
    Jenkins.getInstance(), null, null
)

creds.each { c ->
    println "ID: ${c.id}"
    if (c instanceof UsernamePasswordCredentialsImpl) {
        println "  Username: ${c.username}"
        println "  Password: ${c.password.plainText}"  // 평문 노출!
    }
}
```

왜 이것이 가능할까요? Jenkins는 크레덴셜을 암호화하여 저장하지만, 복호화 키가 Jenkins 프로세스 메모리에 있습니다. Script Console은 그 프로세스 안에서 실행되므로 복호화 API를 직접 호출할 수 있습니다. 이것은 설계 결함이 아니라, Jenkins가 빌드 중에 크레덴셜을 사용해야 하므로 프로세스가 복호화 능력을 갖추어야 하기 때문입니다. 문제는 그 능력이 Script Console을 통해 관리자에게 노출된다는 것입니다.

따라서 Script Console 접근 권한은 **Jenkins 시스템 관리자 중에서도 극소수**에게만 부여해야 합니다. Matrix-based Security에서 "Administer" 권한과 "Run Scripts" 권한을 분리하여 관리하는 것이 권장됩니다.

---

## 4. Groovy 커스터마이징의 범위와 한계

### 할 수 있는 것

Groovy를 통한 Jenkins 커스터마이징은 사실상 무한에 가깝습니다. Jenkins의 모든 Java API에 접근할 수 있으므로, UI에서 할 수 있는 모든 것과 UI에서 할 수 없는 것까지 Groovy로 가능합니다.

| 영역 | 가능한 작업 | 예시 |
|------|------------|------|
| **Pipeline 확장** | 커스텀 DSL step 정의 | `deployToK8s()` 같은 도메인 전용 step |
| **전역 Hook** | 모든 빌드에 전/후 동작 삽입 | 빌드 시작/완료 시 Slack 알림 |
| **동적 설정** | 런타임에 설정 변경 | 특정 시간대에 Agent 수 조절 |
| **모니터링** | 시스템 상태 수집 | 빌드 큐 길이, Agent 활용률 |
| **보안 자동화** | 보안 정책 프로그래매틱 적용 | 사용자 권한 일괄 변경, 감사 로그 |

### 위험한 것

"할 수 있다"와 "해야 한다"는 다릅니다. Groovy의 무제한 접근 권한이 오히려 보안 사고와 운영 장애의 원인이 될 수 있습니다.

**크레덴셜 평문 노출**: 앞서 설명한 것처럼 Script Console에서 모든 비밀값을 읽을 수 있습니다. 누군가 악의적으로 또는 실수로 크레덴셜을 로그에 출력하면, 그 로그가 빌드 아티팩트나 모니터링 시스템으로 전파될 수 있습니다.

**init.groovy에서 외부 URL 호출**: init.groovy.d 스크립트에서 외부 URL의 코드를 다운로드하여 실행하는 패턴이 있습니다. 이것은 **공급망 공격(Supply Chain Attack)의 벡터**입니다. 외부 서버가 해킹당하면 Jenkins 시작 시마다 악성 코드가 실행됩니다.

```groovy
// ⚠️ 절대 하지 말아야 할 패턴
new GroovyShell().evaluate(
    new URL("https://example.com/init-script.groovy").text
)
```

**시스템 프로퍼티 무분별 변경**: `System.setProperty()`로 JVM 레벨의 설정을 변경하면 Jenkins의 동작이 예측 불가능해질 수 있습니다. 예를 들어 HTTP 프록시 설정을 잘못 변경하면 플러그인 업데이트나 Git clone이 모두 실패합니다.

**Groovy Sandbox 우회 시도**: Pipeline에서 Sandbox를 우회하려는 시도는 Script Security Plugin이 차단하지만, 우회 방법이 발견될 때마다 보안 취약점으로 보고됩니다. Jenkins 보안 어드바이저리에서 가장 빈번하게 등장하는 유형 중 하나가 Sandbox 우회입니다.

---

## 5. Groovy 커스터마이징 권장 여부 -- 현실적 가이드

### 권장 판단 매트릭스

| 용도 | 대안 | 결론 |
|------|------|------|
| 초기 설정 자동화 | JCasC (Configuration as Code) | **JCasC 우선**, 불가능할 때만 init.groovy.d |
| Pipeline 공통 로직 | Shared Library | **Shared Library 사용** |
| 일회성 관리 작업 | Script Console | **주의하여 사용**, 감사 로그 필수 |
| 빌드 전/후 전역 동작 | Global Pipeline Libraries | **Library 우선**, 불가능하면 init hook |
| 크레덴셜 등록 | JCasC + 외부 Secret Manager | **JCasC + Vault/K8s Secret**, 불가능하면 init.groovy.d |
| 플러그인 설정 초기화 | JCasC | **JCasC가 거의 모든 경우 가능** |

핵심 원칙은 명확합니다. **"선언적 방법이 있으면 선언적 방법을 쓰고, 없을 때만 명령적 방법을 쓴다."** JCasC는 선언적이고, init.groovy.d는 명령적입니다.

### JCasC vs init.groovy.d 비교

**JCasC (Jenkins Configuration as Code)**는 Jenkins 설정을 YAML 파일로 선언하는 플러그인입니다. `jenkins.yaml` 파일 하나로 보안, 크레덴셜, 도구, 에이전트 설정을 모두 정의할 수 있습니다.

```yaml
# JCasC 예시: jenkins.yaml
jenkins:
  securityRealm:
    local:
      allowsSignup: false
      users:
        - id: "admin"
          password: "${JENKINS_ADMIN_PASSWORD}"
  authorizationStrategy:
    loggedInUsersCanDoAnything:
      allowAnonymousRead: false

credentials:
  system:
    domainCredentials:
      - credentials:
          - usernamePassword:
              id: "git-credentials"
              username: "${GIT_USER}"
              password: "${GIT_TOKEN}"

tool:
  jdk:
    installations:
      - name: "JDK17"
        home: "/usr/lib/jvm/java-17-openjdk"
```

**init.groovy.d**는 동일한 설정을 Groovy 코드로 명령적으로 작성합니다.

| 비교 항목 | JCasC | init.groovy.d |
|-----------|-------|---------------|
| **패러다임** | 선언적 (YAML) | 명령적 (Groovy 코드) |
| **버전 관리** | 쉬움 (YAML diff가 명확) | 어려움 (코드 diff는 의도 파악이 힘듦) |
| **디버깅** | 명확한 에러 메시지 | println 디버깅, 스택 트레이스 해석 필요 |
| **재현성** | 동일 YAML = 동일 결과 | 실행 순서, 타이밍에 따라 결과 다를 수 있음 |
| **유연성** | 플러그인 지원 범위 내에서만 | 무제한 (Jenkins 전체 API 접근) |
| **조건부 로직** | 제한적 (환경변수 치환 정도) | 완전한 프로그래밍 가능 |
| **학습 곡선** | 낮음 (YAML 작성) | 높음 (Jenkins Internal API 이해 필요) |

결론은 분명합니다. **JCasC로 할 수 있으면 JCasC를 쓰고, JCasC로 불가능한 경우에만 init.groovy.d를 사용하며, Script Console은 긴급 상황이나 일회성 조사에만 사용합니다.** 이 우선순위를 어기면 유지보수 부채가 빠르게 쌓입니다.

### Script Security Plugin

Script Security Plugin은 Pipeline에서 실행되는 Groovy 코드에 보안 경계를 설정하는 핵심 플러그인입니다. 이 플러그인이 없으면, 개발자가 Jenkinsfile에서 `System.exit(0)`을 실행하여 Jenkins를 종료하거나, 크레덴셜을 평문으로 읽어서 외부로 전송할 수 있습니다.

```mermaid
flowchart TB
    Dev["개발자가 Pipeline<br/>Groovy 코드 작성"]
    Dev --> Sandbox{"Sandbox<br/>Check"}

    Sandbox -->|"허용된 API<br/>(sh, echo, stage)"| Execute["즉시 실행"]
    Sandbox -->|"비허용 API<br/>(System.exit, Runtime.exec)"| Block["실행 차단"]
    Block --> Approval{"관리자<br/>Script Approval"}
    Approval -->|"승인"| AllowList["허용 목록에 추가"]
    AllowList --> Execute
    Approval -->|"거부"| Reject["실행 거부<br/>Pipeline 실패"]

    Execute --> Result["빌드 결과"]
    Reject --> Fail["빌드 실패"]

    subgraph legend["보안 계층"]
        L1["1차: Sandbox 자동 검사"]
        L2["2차: 관리자 수동 승인"]
        L3["3차: 허용 목록 관리"]
    end

    style Sandbox fill:#ffc107,color:#000
    style Block fill:#dc3545,color:#fff
    style Execute fill:#28a745,color:#fff
    style Reject fill:#dc3545,color:#fff
```

**Sandbox 모드의 동작 원리**: Pipeline의 Groovy 코드는 기본적으로 Sandbox 안에서 실행됩니다. Sandbox는 허용된 API 목록(whitelist)을 유지하고, 코드가 목록에 없는 API를 호출하면 실행을 차단합니다. `sh`, `echo`, `stage`, `parallel` 같은 Pipeline DSL 기본 기능은 허용되지만, `java.lang.Runtime.exec()`, `System.exit()`, `jenkins.model.Jenkins.getInstance()` 같은 시스템 레벨 API는 차단됩니다.

**Script Approval 프로세스**: 차단된 API가 정당한 용도로 필요한 경우, 관리자가 "Manage Jenkins > In-process Script Approval"에서 해당 메서드 시그니처를 승인할 수 있습니다. 승인된 메서드는 허용 목록에 추가되어 이후 모든 Pipeline에서 사용 가능해집니다. 이것이 왜 위험할 수 있느냐면, 한 번 승인된 메서드는 모든 Pipeline에서 사용 가능하므로, 특정 팀만을 위해 승인한 메서드가 다른 팀에 의해 악용될 수 있기 때문입니다.

**Sandbox가 없다면 어떤 일이 벌어지는가**: 개발자가 Jenkinsfile에 악의적인 코드를 넣으면 즉시 실행됩니다. Jenkins Master의 파일 시스템에 접근하여 크레덴셜 파일을 외부로 전송하거나, 내부 네트워크를 스캔하거나, 암호화폐 채굴 프로세스를 실행할 수 있습니다. Multibranch Pipeline에서 외부 기여자의 Pull Request를 자동 빌드하는 경우 이 위험은 더욱 커집니다.

---

## 6. 전역 파이프라인 Hook: 모든 빌드에 로직 주입하기

"모든 파이프라인의 빌드 시작 시 Slack 알림을 보내고, 완료 시 결과를 기록하고 싶다"는 요구사항이 있을 때, 각 Jenkinsfile을 수정하는 것은 비현실적이다. 프로젝트가 100개가 넘으면 더더욱 그렇다. Jenkins는 이런 전역 Hook을 구현하는 여러 메커니즘을 제공하며, 각각 적용 범위와 강제성이 다르다.

### 전역 Hook 접근법 비교

| 접근법 | 강제성 | 적용 대상 | Jenkinsfile 수정 | 권장도 |
|--------|--------|----------|-----------------|--------|
| Shared Library Wrapper | Opt-in | Pipeline | 필요 (`@Library`) | 가장 권장 |
| Implicit Global Library | Opt-in | Pipeline | 불필요 (자동 로드) | 권장 |
| RunListener (init.groovy.d) | 강제 | 모든 빌드 | 불필요 | 조건부 권장 |
| FlowExecutionListener | 강제 | Pipeline만 | 불필요 | 조건부 권장 |
| Organization Default Jenkinsfile | 강제 | Multibranch | 불필요 | 특수 상황 |

### 접근법 1: Shared Library Wrapper (가장 권장)

각 팀이 자발적으로 사용하는 방식이다. Shared Library에 래퍼 함수를 만들고, 각 Jenkinsfile에서 호출한다. 팀별로 opt-in이므로 부작용 제어가 쉽다.

```groovy
// vars/standardPipeline.groovy (Shared Library)
def call(Map config = [:], Closure body) {
    // --- 전역 Pre-Hook ---
    slackSend(channel: '#ci-notifications',
              message: "Build started: ${env.JOB_NAME} #${env.BUILD_NUMBER}")

    def startTime = System.currentTimeMillis()

    try {
        // 실제 Pipeline 로직 실행
        body()

        // --- 전역 Post-Hook (성공) ---
        def duration = (System.currentTimeMillis() - startTime) / 1000
        slackSend(channel: '#ci-notifications', color: 'good',
                  message: "Build SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER} (${duration}s)")
    } catch (Exception e) {
        // --- 전역 Post-Hook (실패) ---
        slackSend(channel: '#ci-notifications', color: 'danger',
                  message: "Build FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}\n${e.message}")
        throw e
    }
}
```

```groovy
// Jenkinsfile (사용 측) — @Library로 명시적 로드
@Library('my-shared-lib') _

standardPipeline {
    pipeline {
        agent any
        stages {
            stage('Build') {
                steps {
                    sh 'mvn clean package'
                }
            }
        }
    }
}
```

이 방식의 장점은 **버전 관리**가 된다는 것이다. `@Library('my-shared-lib@v2.1.0') _`처럼 특정 버전을 고정할 수 있고, 라이브러리 변경이 모든 프로젝트에 즉시 영향을 주지 않는다. 단점은 각 Jenkinsfile이 래퍼를 호출해야 한다는 것이다.

### 접근법 2: Implicitly Loaded Global Library

Jenkins 관리 > Configure System > Global Pipeline Libraries에서 **"Load implicitly"**를 체크하면, 모든 Pipeline에서 `@Library` 선언 없이 Shared Library의 `vars/` 함수를 사용할 수 있다.

```yaml
# CasC로 Implicit Global Library 설정
unclassified:
  globalLibraries:
    libraries:
      - name: "global-hooks"
        defaultVersion: "main"
        implicit: true              # 핵심: 모든 Pipeline에 자동 로드
        allowVersionOverride: false  # 버전 오버라이드 금지 (일관성 보장)
        retriever:
          modernSCM:
            scm:
              git:
                remote: "https://github.com/company/jenkins-global-hooks.git"
                credentialsId: "git-credentials"
```

```groovy
// vars/globalHooks.groovy (Implicit Global Library)
// 모든 Pipeline에서 globalHooks.xxx()로 호출 가능

class globalHooks implements Serializable {

    static void notifyBuildStart(script) {
        script.echo "[Global Hook] Build started: ${script.env.JOB_NAME}"
        // Slack, Teams, 메트릭 수집 등
    }

    static void notifyBuildEnd(script, String result) {
        script.echo "[Global Hook] Build ${result}: ${script.env.JOB_NAME}"
    }

    static void enforceBuildTimeout(script, int minutes = 60) {
        // 전역 타임아웃 정책 강제
        script.timeout(time: minutes, unit: 'MINUTES') {
            script.echo "Build timeout set to ${minutes} minutes"
        }
    }
}
```

Implicit Loading은 함수를 "사용 가능"하게 만들 뿐이지, 자동으로 실행하지는 않는다. 각 Jenkinsfile이 `globalHooks.notifyBuildStart(this)`를 호출해야 한다. 진짜 "Jenkinsfile 수정 없이 모든 빌드에 강제 적용"하려면 다음 접근법이 필요하다.

### 접근법 3: RunListener — 진짜 전역 Hook (init.groovy.d)

`RunListener`는 Jenkins의 내부 이벤트 리스너로, **모든 빌드의 시작/완료/삭제** 이벤트에 반응한다. Jenkinsfile을 전혀 수정하지 않아도 모든 빌드에 강제 적용된다. 이것이 질문한 "전역 로직을 넣는" 방법의 핵심이다.

```groovy
// init.groovy.d/10-global-build-listener.groovy
import hudson.model.listeners.RunListener
import hudson.model.Run
import hudson.model.TaskListener

// RunListener를 상속한 커스텀 리스너 정의
class GlobalBuildListener extends RunListener<Run> {

    // --- 빌드 시작 시 호출 ---
    @Override
    void onStarted(Run run, TaskListener listener) {
        def jobName = run.getParent().getFullName()
        def buildNumber = run.getNumber()
        def startedBy = run.getCause(hudson.model.Cause.UserIdCause)?.getUserId() ?: 'system'

        listener.getLogger().println("[Global Hook] Build #${buildNumber} started by ${startedBy}")

        // 예시: 빌드 시작 메트릭 수집
        // pushMetric("jenkins.build.started", jobName, buildNumber)

        // 예시: 특정 시간대 빌드 차단 (배포 동결 기간)
        // def hour = new Date().getHours()
        // if (hour >= 22 || hour < 6) {
        //     listener.getLogger().println("WARNING: Building during maintenance window")
        // }
    }

    // --- 빌드 완료 시 호출 ---
    @Override
    void onCompleted(Run run, TaskListener listener) {
        def jobName = run.getParent().getFullName()
        def buildNumber = run.getNumber()
        def result = run.getResult()?.toString() ?: 'UNKNOWN'
        def duration = run.getDuration()

        listener.getLogger().println("[Global Hook] Build #${buildNumber} completed: ${result} (${duration}ms)")

        // 예시: 빌드 실패 시 Slack 알림
        if (result == 'FAILURE') {
            // sendSlackNotification("#alerts", "FAILED: ${jobName} #${buildNumber}")
        }

        // 예시: 빌드 시간 메트릭 기록
        // pushMetric("jenkins.build.duration", jobName, duration)

        // 예시: 빌드 결과를 외부 대시보드에 전송
        // postToApi("https://metrics.company.com/builds", [
        //     job: jobName, build: buildNumber, result: result, duration: duration
        // ])
    }

    // --- 빌드 삭제 시 호출 ---
    @Override
    void onDeleted(Run run) {
        def jobName = run.getParent().getFullName()
        println "[Global Hook] Build #${run.getNumber()} deleted from ${jobName}"
    }

    // --- 빌드 최종 완료 시 호출 (모든 post 액션 이후) ---
    @Override
    void onFinalized(Run run) {
        // onCompleted 이후, post { always { } } 블록까지 모두 실행된 후 호출
        // 최종 정리 작업에 적합
    }
}

// 리스너 등록
RunListener.all().add(new GlobalBuildListener())
println "[init] Global build listener registered."
```

```mermaid
sequenceDiagram
    participant J as Jenkins Core
    participant RL as RunListener<br/>(GlobalBuildListener)
    participant P as Pipeline 실행
    participant Ext as 외부 서비스<br/>(Slack, Metrics)

    Note over J: 사용자가 빌드 트리거
    J->>RL: onStarted(run, listener)
    RL->>Ext: 빌드 시작 알림/메트릭
    RL-->>J: return

    J->>P: Pipeline 실행 시작
    P->>P: stage('Build')
    P->>P: stage('Test')
    P->>P: stage('Deploy')
    P-->>J: Pipeline 실행 완료

    J->>RL: onCompleted(run, listener)
    RL->>Ext: 빌드 결과 알림/메트릭
    RL-->>J: return

    J->>P: post { always { } } 실행
    P-->>J: post 블록 완료

    J->>RL: onFinalized(run)
    RL->>Ext: 최종 정리
    RL-->>J: return
```

**RunListener의 4가지 이벤트**:

| 이벤트 | 호출 시점 | 용도 |
|--------|----------|------|
| `onStarted` | 빌드 시작 직후 | 시작 알림, 메트릭 기록, 배포 동결 검사 |
| `onCompleted` | 빌드 결과 확정 직후 | 결과 알림, 실패 분석, 성공/실패 메트릭 |
| `onFinalized` | post 블록까지 모두 실행 후 | 최종 정리, 리소스 해제 |
| `onDeleted` | 빌드 기록 삭제 시 | 외부 시스템의 빌드 기록 정리 |

**주의사항**: RunListener는 Jenkins의 모든 빌드(Freestyle, Pipeline, Multibranch 등)에 적용된다. 특정 Job만 대상으로 하려면 `onStarted` 내부에서 Job 이름이나 타입으로 필터링해야 한다.

```groovy
// 특정 폴더의 Job만 Hook 적용
@Override
void onStarted(Run run, TaskListener listener) {
    def jobName = run.getParent().getFullName()

    // "production/" 폴더 하위의 Job만 대상
    if (!jobName.startsWith("production/")) {
        return
    }

    // Hook 로직 실행
    listener.getLogger().println("[Prod Hook] Production build started: ${jobName}")
}
```

### 접근법 4: FlowExecutionListener — Pipeline 전용 Hook

`FlowExecutionListener`는 Pipeline(Declarative/Scripted) 빌드만 대상으로 하는 리스너이다. Freestyle Job에는 적용되지 않으므로, Pipeline 환경에서 더 정밀한 Hook이 가능하다.

```groovy
// init.groovy.d/11-pipeline-listener.groovy
import org.jenkinsci.plugins.workflow.flow.FlowExecutionListener
import org.jenkinsci.plugins.workflow.flow.FlowExecution
import org.jenkinsci.plugins.workflow.flow.FlowExecutionOwner

class GlobalPipelineListener extends FlowExecutionListener {

    // Pipeline 시작 시
    @Override
    void onRunning(FlowExecution execution) {
        def owner = execution.getOwner()
        def run = owner.getExecutable()
        println "[Pipeline Hook] Pipeline started: ${run.getParent().getFullName()} #${run.getNumber()}"
    }

    // Pipeline 완료 시
    @Override
    void onCompleted(FlowExecution execution) {
        def owner = execution.getOwner()
        def run = owner.getExecutable()
        def result = run.getResult()?.toString() ?: 'SUCCESS'
        println "[Pipeline Hook] Pipeline completed: ${run.getParent().getFullName()} → ${result}"

        // Pipeline에서만 사용 가능한 정보 수집
        // 예: 어떤 stage에서 실패했는지, 총 stage 수 등
    }

    // Pipeline 재개 시 (Jenkins 재시작 후 중단된 Pipeline 재개)
    @Override
    void onResumed(FlowExecution execution) {
        println "[Pipeline Hook] Pipeline resumed after Jenkins restart"
    }
}

FlowExecutionListener.all().add(new GlobalPipelineListener())
println "[init] Pipeline execution listener registered."
```

RunListener와 FlowExecutionListener의 차이: RunListener는 **모든 빌드 타입**에 적용되고 빌드의 시작/완료를 감지한다. FlowExecutionListener는 **Pipeline만** 대상이며, Pipeline의 시작/완료 외에 **재개(resume)** 이벤트도 감지할 수 있다. Jenkins가 재시작된 후 이전에 실행 중이던 Pipeline이 재개될 때 `onResumed`가 호출된다.

### 접근법 5: 실전 조합 — 전역 보안 정책 + 감사 로그

실무에서는 여러 접근법을 조합하여 사용한다. 다음은 "모든 빌드의 시작/결과를 감사 로그로 남기고, 프로덕션 배포는 근무시간에만 허용"하는 전역 정책 예시이다.

```groovy
// init.groovy.d/10-audit-and-policy.groovy
import hudson.model.listeners.RunListener
import hudson.model.Run
import hudson.model.TaskListener
import java.time.LocalTime
import java.time.DayOfWeek
import java.time.LocalDate

class AuditAndPolicyListener extends RunListener<Run> {

    // 감사 로그 파일 경로
    static final String AUDIT_LOG = "${System.getenv('JENKINS_HOME')}/audit/build-audit.log"

    @Override
    void onStarted(Run run, TaskListener listener) {
        def jobName = run.getParent().getFullName()
        def buildNumber = run.getNumber()
        def user = run.getCause(hudson.model.Cause.UserIdCause)?.getUserId() ?: 'trigger/system'

        // 1. 감사 로그 기록
        writeAuditLog("STARTED", jobName, buildNumber, user)

        // 2. 프로덕션 배포 시간대 정책
        if (jobName.contains("deploy") && jobName.contains("prod")) {
            def now = LocalTime.now()
            def today = LocalDate.now().getDayOfWeek()

            // 평일 09:00~18:00만 허용
            boolean isWorkHours = (today != DayOfWeek.SATURDAY
                                  && today != DayOfWeek.SUNDAY
                                  && now.isAfter(LocalTime.of(9, 0))
                                  && now.isBefore(LocalTime.of(18, 0)))

            if (!isWorkHours) {
                listener.getLogger().println(
                    "WARNING: Production deployment outside work hours. " +
                    "Current time: ${now}, Day: ${today}")
                // 경고만 하고 차단하지는 않음 (차단하려면 run.setResult(Result.ABORTED))
            }
        }
    }

    @Override
    void onCompleted(Run run, TaskListener listener) {
        def jobName = run.getParent().getFullName()
        def result = run.getResult()?.toString() ?: 'UNKNOWN'
        writeAuditLog(result, jobName, run.getNumber(), "-")
    }

    private void writeAuditLog(String event, String job, int build, String user) {
        def logFile = new File(AUDIT_LOG)
        logFile.parentFile.mkdirs()
        def timestamp = new Date().format("yyyy-MM-dd HH:mm:ss")
        logFile.append("${timestamp} | ${event} | ${job} #${build} | ${user}\n")
    }
}

RunListener.all().add(new AuditAndPolicyListener())
println "[init] Audit and policy listener registered."
```

감사 로그 출력 예시:
```
2026-03-06 10:23:45 | STARTED  | backend/api-service #142 | admin
2026-03-06 10:25:12 | SUCCESS  | backend/api-service #142 | -
2026-03-06 14:30:01 | STARTED  | deploy/prod-rollout #28  | deploy-bot
2026-03-06 14:35:44 | FAILURE  | deploy/prod-rollout #28  | -
```

### 전역 Hook 선택 가이드

```mermaid
flowchart TD
    Q1{"Jenkinsfile 수정이<br/>가능한가?"}
    Q1 -->|"가능"| Q2{"팀별 Opt-in<br/>가능한가?"}
    Q1 -->|"불가능<br/>(레거시, 외부팀)"| Q3{"Pipeline만<br/>대상인가?"}

    Q2 -->|"가능"| A1["Shared Library<br/>Wrapper 패턴"]
    Q2 -->|"모든 팀 강제"| A2["Implicit Global<br/>Library + Wrapper"]

    Q3 -->|"Pipeline만"| A4["FlowExecution<br/>Listener"]
    Q3 -->|"Freestyle 포함<br/>모든 빌드"| A3["RunListener<br/>(init.groovy.d)"]

    style A1 fill:#d4edda,stroke:#28a745,color:#333
    style A2 fill:#d4edda,stroke:#28a745,color:#333
    style A3 fill:#fff3cd,stroke:#ffc107,color:#333
    style A4 fill:#fff3cd,stroke:#ffc107,color:#333
```

---

## 7. Groovy 커스터마이징 전체 카탈로그

Groovy로 Jenkins의 어디까지 커스터마이징할 수 있는지를 영역별로 정리한다. 모든 예시는 Script Console 또는 init.groovy.d에서 실행할 수 있다.

### 7-1. Job/Pipeline 관리

```groovy
import jenkins.model.*

def jenkins = Jenkins.getInstance()

// Job 목록 조회
jenkins.getAllItems(hudson.model.Job.class).each { job ->
    println "${job.fullName} [${job.getClass().simpleName}]"
}

// Job 비활성화/활성화
def job = jenkins.getItemByFullName("my-folder/my-job")
job.setDisabled(true)   // 비활성화
job.setDisabled(false)  // 활성화
job.save()

// Job 설명 변경
job.setDescription("Updated by Groovy script on ${new Date()}")
job.save()

// Freestyle Job 프로그래밍 생성
import hudson.model.FreeStyleProject
def project = jenkins.createProject(FreeStyleProject.class, "auto-generated-job")
project.setDescription("Groovy로 자동 생성된 Job")
project.save()

// Pipeline Job 프로그래밍 생성
import org.jenkinsci.plugins.workflow.job.WorkflowJob
import org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition
def pipelineJob = jenkins.createProject(WorkflowJob.class, "auto-pipeline")
pipelineJob.setDefinition(new CpsFlowDefinition('''
    pipeline {
        agent any
        stages {
            stage('Hello') {
                steps { echo 'Generated by Groovy' }
            }
        }
    }
''', true))  // true = sandbox 모드
pipelineJob.save()
```

### 7-2. Node/Agent 관리

```groovy
import jenkins.model.*
import hudson.model.*
import hudson.slaves.*

def jenkins = Jenkins.getInstance()

// 모든 노드 상태 조회
jenkins.getNodes().each { node ->
    def comp = node.toComputer()
    println "${node.displayName}: ${comp?.isOnline() ? 'ONLINE' : 'OFFLINE'}" +
            " | Labels: ${node.getLabelString()}" +
            " | Executors: ${comp?.countBusy()}/${node.getNumExecutors()}"
}

// Agent 라벨 동적 변경
def agent = jenkins.getNode("docker-agent")
if (agent) {
    agent.setLabelString("docker linux amd64")  // 라벨 변경
    agent.save()
}

// Agent Executor 수 변경
agent.setNumExecutors(4)
agent.save()

// Agent를 일시적으로 오프라인으로 전환
def computer = agent.toComputer()
computer.setTemporarilyOffline(true,
    new hudson.slaves.OfflineCause.ByCLI("Maintenance window"))

// Agent를 다시 온라인으로
computer.setTemporarilyOffline(false, null)

// 새 SSH Agent 프로그래밍 추가
import hudson.plugins.sshslaves.SSHLauncher
import hudson.plugins.sshslaves.verifiers.ManuallyTrustedKeyVerificationStrategy

def launcher = new SSHLauncher(
    "agent-host.company.com",  // 호스트
    22,                         // 포트
    "agent-ssh-key",           // credentials ID
    null, null, null, null,
    30, 3, 15,
    new ManuallyTrustedKeyVerificationStrategy(false)
)

def newAgent = new DumbSlave(
    "new-agent",               // 이름
    "/home/jenkins",           // 원격 디렉토리
    launcher
)
newAgent.setNumExecutors(2)
newAgent.setLabelString("linux docker")
newAgent.setMode(Node.Mode.NORMAL)
jenkins.addNode(newAgent)
```

### 7-3. Credentials 관리

```groovy
import jenkins.model.*
import com.cloudbees.plugins.credentials.*
import com.cloudbees.plugins.credentials.domains.*
import com.cloudbees.plugins.credentials.impl.*
import org.jenkinsci.plugins.plaincredentials.impl.*
import hudson.util.Secret

def store = Jenkins.getInstance()
    .getExtensionList('com.cloudbees.plugins.credentials.SystemCredentialsProvider')[0]
    .getStore()
def domain = Domain.global()

// Username/Password 등록
store.addCredentials(domain, new UsernamePasswordCredentialsImpl(
    CredentialsScope.GLOBAL,
    "nexus-credentials",
    "Nexus Repository Access",
    "deploy-user",
    "deploy-password"
))

// Secret Text 등록
store.addCredentials(domain, new StringCredentialsImpl(
    CredentialsScope.GLOBAL,
    "slack-webhook-token",
    "Slack Webhook Token",
    Secret.fromString("xoxb-xxxx-xxxx")
))

// SSH Key 등록
import com.cloudbees.jenkins.plugins.sshcredentials.impl.*
import com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey.DirectEntryPrivateKeySource

store.addCredentials(domain, new BasicSSHUserPrivateKey(
    CredentialsScope.GLOBAL,
    "deploy-ssh-key",
    "deploy",
    new DirectEntryPrivateKeySource("-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----"),
    "",  // passphrase
    "SSH Key for deployment"
))

// 기존 Credential 삭제
def creds = CredentialsProvider.lookupCredentials(
    com.cloudbees.plugins.credentials.common.StandardCredentials.class,
    Jenkins.getInstance(), null, null
)
creds.findAll { it.id == "old-credential" }.each { c ->
    store.removeCredentials(domain, c)
}
```

### 7-4. 전역 환경변수 관리

```groovy
import jenkins.model.*
import hudson.slaves.EnvironmentVariablesNodeProperty

def jenkins = Jenkins.getInstance()

// 기존 전역 환경변수 조회
def globalProps = jenkins.getGlobalNodeProperties()
    .getAll(EnvironmentVariablesNodeProperty.class)

globalProps.each { prop ->
    prop.getEnvVars().each { k, v ->
        println "${k} = ${v}"
    }
}

// 전역 환경변수 추가/수정
def envVarsNodeProperty = globalProps[0]
if (envVarsNodeProperty == null) {
    envVarsNodeProperty = new EnvironmentVariablesNodeProperty()
    jenkins.getGlobalNodeProperties().add(envVarsNodeProperty)
}

envVarsNodeProperty.getEnvVars().put("COMPANY_NAME", "MyCompany")
envVarsNodeProperty.getEnvVars().put("DEFAULT_DOCKER_REGISTRY", "registry.company.com:5000")
envVarsNodeProperty.getEnvVars().put("DEPLOY_ENVIRONMENT", "staging")

jenkins.save()
```

### 7-5. 보안 설정

```groovy
import jenkins.model.*
import hudson.security.*
import jenkins.security.s2m.AdminWhitelistRule

def jenkins = Jenkins.getInstance()

// LDAP 인증 설정
import hudson.security.LDAPSecurityRealm
def ldap = new LDAPSecurityRealm(
    "ldap://ldap.company.com:389",      // server
    "dc=company,dc=com",                 // rootDN
    "ou=People",                          // userSearchBase
    "uid={0}",                            // userSearch
    "ou=Groups",                          // groupSearchBase
    "cn={0}",                             // groupSearchFilter
    null,                                 // groupMembershipFilter
    "cn=admin,dc=company,dc=com",        // managerDN
    Secret.fromString("manager-password"), // managerPassword
    false, false, null, null, null, null, null
)
jenkins.setSecurityRealm(ldap)

// Matrix 기반 인가 설정
import hudson.security.GlobalMatrixAuthorizationStrategy
def authStrategy = new GlobalMatrixAuthorizationStrategy()
authStrategy.add(Jenkins.ADMINISTER, "admin")
authStrategy.add(Jenkins.READ, "authenticated")
authStrategy.add(hudson.model.Item.BUILD, "developers")
authStrategy.add(hudson.model.Item.READ, "developers")
authStrategy.add(hudson.model.Item.CONFIGURE, "leads")
jenkins.setAuthorizationStrategy(authStrategy)

// Markup Formatter (HTML 허용/차단)
jenkins.setMarkupFormatter(new hudson.markup.RawHtmlMarkupFormatter(false))

jenkins.save()
```

### 7-6. 빌드 큐 관리

```groovy
import jenkins.model.*
import hudson.model.*

def queue = Jenkins.getInstance().getQueue()

// 큐에 대기 중인 빌드 조회
queue.getItems().each { item ->
    println "Waiting: ${item.task.getName()} | Why: ${item.getWhy()}"
    println "  In queue since: ${new Date(item.getInQueueSince())}"
}

// 특정 Job의 대기 빌드 취소
queue.getItems().findAll { it.task.getName() == "slow-job" }.each { item ->
    queue.cancel(item)
    println "Cancelled: ${item.task.getName()}"
}

// 모든 대기 빌드 취소 (긴급 시)
queue.getItems().each { queue.cancel(it) }

// 실행 중인 빌드 조회
Jenkins.getInstance().getAllItems(Job.class).each { job ->
    if (job.isBuilding()) {
        println "Building: ${job.fullName} #${job.getLastBuild().getNumber()}"
    }
}

// 특정 빌드 강제 중단
def runningBuild = Jenkins.getInstance()
    .getItemByFullName("my-job")?.getLastBuild()
if (runningBuild?.isBuilding()) {
    def executor = runningBuild.getExecutor()
    executor?.interrupt()
    println "Interrupted: ${runningBuild}"
}
```

### 7-7. View/Dashboard 관리

```groovy
import jenkins.model.*
import hudson.model.*

def jenkins = Jenkins.getInstance()

// ListView 생성
def view = new ListView("Backend Services")
view.setDescription("백엔드 서비스 빌드 현황")
view.setIncludeRegex("backend/.*")  // 정규식으로 Job 필터링
jenkins.addView(view)

// 기존 View에 Job 추가
def existingView = jenkins.getView("My View")
if (existingView instanceof ListView) {
    existingView.add(jenkins.getItemByFullName("my-new-job"))
}

jenkins.save()
```

### 7-8. 플러그인 관리

```groovy
import jenkins.model.*

def pm = Jenkins.getInstance().getPluginManager()
def uc = Jenkins.getInstance().getUpdateCenter()

// 설치된 플러그인 목록 + 업데이트 확인
pm.getPlugins().sort { it.getShortName() }.each { plugin ->
    def hasUpdate = plugin.hasUpdate() ? " → ${plugin.getUpdateInfo()?.version}" : ""
    println "${plugin.getShortName()}:${plugin.getVersion()}${hasUpdate}"
}

// 업데이트 사이트 갱신
uc.updateAllSites()

// 플러그인 설치 (재시작 필요)
def plugin = uc.getPlugin("docker-workflow")
if (plugin) {
    plugin.deploy()
    println "Installing: docker-workflow"
}

// 비활성 플러그인 조회
pm.getPlugins().findAll { !it.isActive() }.each {
    println "Inactive: ${it.getShortName()}"
}
```

### 7-9. 시스템 정보 및 프로퍼티

```groovy
import jenkins.model.*

// Jenkins 버전 및 시스템 정보
println "Jenkins version: ${Jenkins.VERSION}"
println "Java version: ${System.getProperty('java.version')}"
println "OS: ${System.getProperty('os.name')} ${System.getProperty('os.arch')}"
println "JENKINS_HOME: ${Jenkins.getInstance().getRootDir()}"
println "Uptime: ${Jenkins.getInstance().toComputer().getConnectTime()}"

// JVM 메모리 상태
def runtime = Runtime.getRuntime()
def mb = 1024 * 1024
println "Heap Max: ${runtime.maxMemory() / mb}MB"
println "Heap Used: ${(runtime.totalMemory() - runtime.freeMemory()) / mb}MB"
println "Heap Free: ${runtime.freeMemory() / mb}MB"

// 시스템 프로퍼티 변경 (주의: 사이드 이펙트 큼)
// HTTP 프록시 설정
System.setProperty("http.proxyHost", "proxy.company.com")
System.setProperty("http.proxyPort", "8080")
System.setProperty("http.nonProxyHosts", "localhost|*.company.com")
// ⚠️ 프록시 설정 변경 시 플러그인 업데이트, Git clone 등 모든 HTTP 통신에 영향
```

### 7-10. 메일/알림 설정

```groovy
import jenkins.model.*

// SMTP 설정 변경
def mailer = Jenkins.getInstance().getDescriptorByType(
    hudson.tasks.Mailer.DescriptorImpl.class
)
mailer.setSmtpHost("smtp.company.com")
mailer.setSmtpPort("587")
mailer.setUseSsl(true)
mailer.setSmtpAuth("noreply@company.com", "smtp-password")
mailer.setReplyToAddress("ci-team@company.com")
mailer.setDefaultSuffix("@company.com")
mailer.save()

// 시스템 관리자 이메일 주소 변경
def location = jenkins.model.JenkinsLocationConfiguration.get()
location.setAdminAddress("Jenkins CI <ci-admin@company.com>")
location.setUrl("https://jenkins.company.com/")
location.save()
```

### 7-11. Folder 및 조직 관리

```groovy
import jenkins.model.*
import com.cloudbees.hudson.plugins.folder.Folder

def jenkins = Jenkins.getInstance()

// Folder 생성
def folder = jenkins.createProject(Folder.class, "backend")
folder.setDescription("Backend Service Pipelines")
folder.save()

// 중첩 Folder
def subFolder = folder.createProject(Folder.class, "api")
subFolder.save()

// Folder 안에 Pipeline Job 생성
import org.jenkinsci.plugins.workflow.job.WorkflowJob
import org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition

def job = subFolder.createProject(WorkflowJob.class, "user-service")
job.setDefinition(new CpsFlowDefinition("pipeline { agent any; stages { stage('Build') { steps { echo 'Hello' } } } }", true))
job.save()
// 결과: backend/api/user-service 경로의 Job 생성
```

### 커스터마이징 권장도 요약

| 영역 | Script Console | init.groovy.d | JCasC 대안 | 권장 |
|------|:---:|:---:|:---:|------|
| Job 생성/수정 | O | O | Job DSL Plugin | JCasC + Job DSL |
| Agent 관리 | O | O | CasC nodes | JCasC |
| Credentials | O | O | CasC credentials | JCasC |
| 전역 환경변수 | O | O | CasC globalNodeProperties | JCasC |
| 보안 설정 | O | O | CasC securityRealm | JCasC |
| 빌드 큐 관리 | O | △ | 없음 | Script Console |
| View 관리 | O | O | CasC views | JCasC |
| 플러그인 관리 | O | △ | plugins.txt | plugins.txt |
| 시스템 프로퍼티 | O | O | JAVA_OPTS | 환경변수 |
| 메일 설정 | O | O | CasC unclassified | JCasC |
| Folder 관리 | O | O | Job DSL | Job DSL |
| **전역 Hook** | △ | **O** | Shared Library | **상황에 따라** |

원칙은 변하지 않는다: **JCasC로 가능하면 JCasC, 불가능할 때만 Groovy**. 전역 Hook(RunListener, FlowExecutionListener)은 JCasC로 구현할 수 없는 대표적인 영역이므로, init.groovy.d가 정당한 선택이다.

---

## 8. 실전 레시피: 자주 사용하는 Groovy 스크립트

### 레시피 1: 오프라인 Agent 자동 정리

장기간 오프라인 상태인 Agent를 자동으로 정리하는 스크립트입니다. 이 스크립트는 Script Console에서 일회성으로 실행하거나, 주기적 Pipeline Job으로 스케줄링할 수 있습니다.

```groovy
import jenkins.model.*
import hudson.model.*

def offlineDaysThreshold = 7
def now = new Date()
def removedCount = 0

Jenkins.getInstance().getNodes().each { node ->
    def computer = node.toComputer()

    if (computer != null && !computer.isOnline()) {
        def offlineCause = computer.getOfflineCause()

        // 오프라인 원인에 타임스탬프가 있는 경우 기간 계산
        if (offlineCause != null && offlineCause.hasProperty('timestamp')) {
            def offlineSince = new Date(offlineCause.timestamp)
            def daysDiff = (now.time - offlineSince.time) / (1000 * 60 * 60 * 24)

            if (daysDiff > offlineDaysThreshold) {
                println "Removing: ${node.displayName} (offline for ${daysDiff.intValue()} days)"
                Jenkins.getInstance().removeNode(node)
                removedCount++
            }
        }
    }
}

println "Removed ${removedCount} offline agents."
```

**이것이 권장되는가?** 조건부로 권장됩니다. 클라우드 기반 동적 에이전트(EC2, Kubernetes Pod)를 사용하는 환경에서는 해당 플러그인이 자동 정리를 담당하므로 이 스크립트가 불필요합니다. 정적 에이전트(물리 서버, 고정 VM)를 사용하는 환경에서 유용하지만, 자동 삭제 전에 관리자에게 알림을 보내는 것이 안전합니다.

### 레시피 2: Job 설정 대량 변경

모든 Pipeline Job의 빌드 보관 정책을 일괄 변경해야 하는 상황입니다. UI에서 수백 개의 Job을 하나씩 수정하는 것은 비현실적입니다.

```groovy
import jenkins.model.*
import hudson.tasks.LogRotator

def daysToKeep = 30
def numToKeep = 50
def changedCount = 0

Jenkins.getInstance().getAllItems(hudson.model.Job.class).each { job ->
    def currentRotator = job.getBuildDiscarder()

    // 빌드 보관 정책이 없거나 기존 정책보다 느슨한 경우 업데이트
    if (currentRotator == null) {
        job.setBuildDiscarder(new LogRotator(daysToKeep, numToKeep, -1, -1))
        job.save()
        println "Updated: ${job.fullName} (was: no policy)"
        changedCount++
    }
}

println "Updated ${changedCount} jobs."
```

**이것이 권장되는가?** 일회성 마이그레이션 작업으로는 적절합니다. 하지만 이런 정책을 지속적으로 강제하려면 JCasC의 Job DSL이나 Organization Folder의 기본 설정을 사용하는 것이 더 바람직합니다. Script Console로 일괄 변경한 후에도 누군가 UI에서 개별 Job의 설정을 다시 바꿀 수 있기 때문입니다.

---

## 9. 핵심 요약

| 영역 | 보안 수준 | 주요 용도 | 권장 대안 |
|------|----------|----------|----------|
| Pipeline DSL | Sandbox (높음) | 빌드/배포 파이프라인 | - (표준 사용법) |
| Script Console | 없음 (위험) | 일회성 관리 작업, 디버깅 | 가능하면 JCasC/CLI |
| init.groovy.d | 없음 (위험) | 초기 설정 자동화, 전역 Hook | JCasC 우선, Hook은 init.groovy.d |

Jenkins Groovy 커스터마이징의 핵심 판단 기준은 **"이것을 JCasC로 할 수 있는가?"**이다. 할 수 있으면 JCasC를 사용하고, 할 수 없으면 init.groovy.d를 사용하되 가능한 한 간결하게 작성한다. Script Console은 운영 중 긴급 상황이나 일회성 조사에만 사용하고, 실행 내용은 반드시 기록으로 남긴다.

전역 파이프라인 Hook은 JCasC로 구현할 수 없는 대표적인 영역이다. Shared Library Wrapper(opt-in)를 기본으로 하되, Jenkinsfile 수정이 불가능한 환경에서는 `RunListener`(init.groovy.d)로 모든 빌드에 강제 적용할 수 있다. "Groovy로 할 수 있다"와 "Groovy로 해야 한다"는 전혀 다른 질문이며, 이 구분을 아는 것이 Jenkins 운영 성숙도의 지표이다.
