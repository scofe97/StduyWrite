# 05. Shared Libraries - 조사 (INVESTIGATE)

> Jenkins Shared Library를 통해 조직의 CI/CD 파이프라인을 표준화하고 중복을 제거하는 방법을 탐구합니다.

---

## 면접 질문

### 1. **Jenkins Shared Library가 필요한 이유를 마이크로서비스 환경에서의 CI/CD 관점으로 설명하시오.**

**핵심 포인트**:
- 마이크로서비스 환경에서는 수십~수백 개의 서비스가 동일한 빌드-테스트-배포 패턴을 따르는데, 각 서비스의 Jenkinsfile에 같은 로직을 복사하면 **하나의 변경이 N번의 수정을 요구**하는 변경 증폭 문제가 발생한다.
- 시간이 지나면 서비스마다 Jenkinsfile이 미묘하게 달라지는 **드리프트(Drift) 현상**이 발생하여, 어떤 서비스는 보안 스캔이 있고 어떤 서비스는 없는 불일치가 생긴다.
- Shared Library는 공통 CI/CD 로직을 **별도 Git 저장소로 추출**하여, 한 곳에서 수정하면 모든 Pipeline에 반영되도록 한다. 이는 코드의 DRY 원칙을 CI/CD 영역에 적용한 것이다.
- 거버넌스 관점에서, 라이브러리에 보안 스캔 단계를 포함시키면 이 라이브러리를 사용하는 모든 Pipeline이 **자동으로 보안 스캔을 수행**하므로, 개별 팀이 보안 단계를 생략하는 것을 구조적으로 방지할 수 있다.
- 결과적으로 Shared Library는 단순한 코드 재사용이 아니라, **조직의 CI/CD 정책을 코드로 강제하는 플랫폼 엔지니어링 도구**이다.

**심화 질문**:
- Shared Library 없이 Jenkinsfile 중복을 줄이는 다른 방법(예: Jenkinsfile 템플릿 생성기)과 비교했을 때, Shared Library의 장단점은 무엇인가?
- Shared Library가 단일 장애점(Single Point of Failure)이 될 수 있는데, 이를 어떻게 완화하는가?

---

### 2. **vars/와 src/ 디렉토리의 차이를 설명하고, 각각 어떤 코드를 넣어야 하는지 가이드를 제시하시오.**

**핵심 포인트**:
- **vars/ 디렉토리**는 Pipeline에서 **함수처럼 직접 호출**되는 전역 변수를 담는다. 파일명이 곧 함수명이 되어(`buildDocker.groovy` → `buildDocker()`), `call()` 메서드를 통해 실행된다. Pipeline DSL(`sh`, `stage`, `docker` 등)을 자유롭게 사용할 수 있다.
- **src/ 디렉토리**는 일반 Groovy 클래스를 담으며, Java와 동일한 패키지 구조를 따른다. `import`문으로 사용하고, Pipeline DSL에 직접 접근할 수 없다. Pipeline 컨텍스트가 필요하면 vars/에서 `this`를 전달받아야 한다.
- **가이드**: vars/에는 **Pipeline 흐름을 정의하는 코드**(stage 정의, sh 호출, 알림 등)를 넣고, src/에는 **순수 비즈니스 로직**(설정 객체, 조건 판단, 문자열 변환 등)을 넣는다. 이렇게 분리하면 src/ 클래스는 Jenkins 없이도 단위 테스트가 가능하다.
- src/ 클래스는 반드시 `Serializable` 인터페이스를 구현해야 한다. Jenkins Pipeline은 CPS(Continuation Passing Style) 변환을 통해 실행 중간에 직렬화/역직렬화를 수행하기 때문이다.

**심화 질문**:
- src/ 클래스에서 Pipeline DSL을 사용하려면 어떻게 해야 하는가? (steps 객체 주입 패턴)
- vars/에 모든 로직을 넣고 src/를 아예 사용하지 않는 팀이 있다면, 어떤 문제가 생기겠는가?

---

### 3. **@Library 어노테이션의 버전 고정(Version Pinning)이 왜 중요한지, 고정하지 않으면 어떤 문제가 발생하는지 설명하시오.**

**핵심 포인트**:
- 버전을 고정하지 않으면 Jenkins 전역 설정에서 지정한 기본 브랜치(보통 main)의 **최신 코드**를 항상 사용하게 된다. 라이브러리에 breaking change가 머지되면, 이 라이브러리를 사용하는 **모든 Pipeline이 동시에 깨질 수 있다**.
- `@Library('my-lib@v1.2.0')`처럼 태그를 고정하면, 라이브러리가 아무리 변경되어도 해당 Pipeline은 항상 동일한 코드를 사용하므로 **재현 가능한 빌드(Reproducible Build)**가 보장된다.
- 프로덕션 Pipeline은 반드시 **태그 또는 커밋 해시로 고정**해야 하고, 스테이징이나 개발 Pipeline은 `@main`이나 `@develop`으로 최신 변경을 빠르게 검증할 수 있다.
- 버전 고정은 **롤백**도 쉽게 만든다. 라이브러리 v1.3.0에 버그가 있으면 Jenkinsfile에서 `@v1.2.0`으로 되돌리기만 하면 되기 때문이다.
- Semantic Versioning을 따르면 breaking change는 메이저 버전으로, backward-compatible 변경은 마이너/패치 버전으로 관리하여 업그레이드의 위험도를 판단할 수 있다.

**심화 질문**:
- 100개 서비스가 모두 `@Library('lib@v1.2.0')`을 사용 중인데 v1.3.0으로 업그레이드해야 한다면, 점진적으로 마이그레이션하는 전략은?
- Dynamic Loading(`library()` 함수)을 사용하여 Pipeline 파라미터로 라이브러리 버전을 선택하게 하면 어떤 장단점이 있는가?

---

### 4. **Shared Library를 테스트하는 전략을 설명하시오.**

**핵심 포인트**:
- Shared Library는 조직 전체의 CI/CD를 담당하므로, 라이브러리의 버그가 **모든 서비스의 배포를 중단**시킬 수 있다. 따라서 라이브러리 자체의 테스트가 필수적이다.
- **단위 테스트 (vars/)**: Jenkins Pipeline Unit 프레임워크를 사용하여 vars/ 함수를 테스트한다. 이 프레임워크는 `sh`, `stage`, `docker` 등의 Pipeline DSL을 모킹하여 Jenkins 없이도 vars/ 함수의 로직을 검증할 수 있다.
- **단위 테스트 (src/)**: src/ 클래스는 Jenkins 의존성이 없으므로, Groovy의 Spock 프레임워크나 JUnit으로 일반적인 단위 테스트를 작성한다. 이것이 src/로 순수 로직을 분리하는 가장 큰 이유이다.
- **통합 테스트**: 실제 Jenkins 환경에서 테스트 Pipeline을 만들어 `@Library('lib@feature-branch')`로 feature 브랜치의 라이브러리를 로딩하여 실행한다. 단위 테스트로는 검증할 수 없는 **Jenkins 환경 의존적인 동작**(credential 접근, Docker 빌드 등)을 여기서 확인한다.
- **워크플로우**: feature 브랜치에서 개발 → 단위 테스트 통과 → PR + 코드 리뷰 → 테스트 Pipeline에서 통합 테스트 → main 머지 → 태그 생성 → 프로덕션 Pipeline에서 태그 버전 사용.

**심화 질문**:
- Jenkins Pipeline Unit의 한계는 무엇이며, 이를 보완하는 방법은?
- Shared Library의 CI/CD Pipeline(라이브러리를 위한 파이프라인)은 어떻게 구성해야 하는가?

---

### 5. **Implicit Loading과 Explicit Loading의 차이를 설명하고, 조직에서 어떤 방식을 권장해야 하는지 설명하시오.**

**핵심 포인트**:
- **Explicit Loading**: Jenkinsfile에 `@Library('my-lib') _`을 명시적으로 선언한다. 어떤 라이브러리를 사용하는지 Jenkinsfile만 보면 알 수 있으므로 **추적성과 가독성이 높다**. 버전 고정도 Jenkinsfile에서 직접 제어할 수 있다.
- **Implicit Loading**: Jenkins 관리 화면에서 "Load implicitly"를 활성화하면 모든 Pipeline에 자동 로딩된다. Jenkinsfile에 선언 없이도 vars/ 함수를 사용할 수 있다. 조직의 **CI/CD 표준을 강제**할 때 유용하지만, Jenkinsfile만 봐서는 어떤 라이브러리가 로딩되는지 알 수 없어 **디버깅이 어려워진다**.
- **권장 방식**: 두 가지를 **계층적으로 조합**하는 것이 좋다. 조직 공통 라이브러리(보안 스캔, 알림 등)는 Implicit으로 강제하고, 팀별 도메인 라이브러리는 Explicit으로 선언하게 한다. 이렇게 하면 보안/거버넌스는 중앙에서 관리하면서도, 팀별 자율성을 허용할 수 있다.
- Implicit Loading의 위험: 라이브러리의 함수명이 Pipeline의 기존 함수와 충돌할 수 있다. 예를 들어 vars/에 `build.groovy`를 만들면 Jenkins의 기본 `build` 함수와 충돌한다.

**심화 질문**:
- Implicit으로 로딩된 라이브러리와 Explicit으로 로딩된 라이브러리가 동일한 vars/ 함수명을 가지면 어떤 것이 우선하는가?
- Jenkins Configuration as Code(JCasC)를 사용할 때, Implicit Library 설정은 어떻게 관리하는가?

---

### 6. **Shared Library를 도입한 후 발생할 수 있는 문제점과 해결 방법을 설명하시오.**

**핵심 포인트**:
- **단일 장애점(SPOF)**: 라이브러리에 버그가 있으면 모든 Pipeline이 영향을 받는다. 해결책은 **버전 고정**과 **철저한 테스트**이다. 프로덕션 Pipeline은 검증된 태그 버전을 사용하고, 라이브러리 자체의 CI/CD를 통해 머지 전에 충분히 테스트해야 한다.
- **추상화 누수**: 라이브러리가 너무 많은 것을 추상화하면, 개별 서비스의 특수한 요구사항을 수용하기 어려워진다. 해결책은 **확장 포인트(Extension Point)**를 제공하는 것이다. 예를 들어 `standardPipeline(beforeDeploy: { sh './custom-check.sh' })`처럼 클로저를 받아 커스텀 단계를 삽입할 수 있게 한다.
- **디버깅 어려움**: Pipeline 실패 시 에러가 라이브러리 코드에서 발생하면 호출 스택이 복잡해진다. 해결책은 **명확한 에러 메시지**와 **로그 수준 관리**이다.
- **학습 곡선**: Groovy의 CPS 변환, 직렬화 제약 등 Jenkins Pipeline 고유의 제약사항을 이해해야 라이브러리를 올바르게 작성할 수 있다. `@NonCPS` 어노테이션, `Serializable` 인터페이스 등의 개념을 팀 전체가 이해해야 한다.
- **버전 파편화**: 서비스마다 다른 라이브러리 버전을 사용하면 관리가 복잡해진다. 해결책은 **정기적인 업그레이드 캠페인**과 **최소 지원 버전 정책**이다.

**심화 질문**:
- Groovy의 CPS 변환이 Shared Library 코드에 미치는 영향은 무엇이며, @NonCPS는 언제 사용해야 하는가?
- Shared Library가 10개 이상으로 늘어났을 때, 라이브러리 간 의존성을 어떻게 관리하는가?

---

### 7. **Shared Library 디자인 시 vars/ 함수의 인터페이스를 어떻게 설계해야 하는지 설명하시오.**

**핵심 포인트**:
- **Map config 패턴**을 사용하여 이름 기반 파라미터를 받는 것이 권장된다. `buildDocker(imageName: 'app', tag: 'v1')`처럼 호출하면 가독성이 높고, 새 파라미터를 추가해도 기존 호출부가 깨지지 않는다.
- **필수 파라미터는 즉시 검증**해야 한다. `config.imageName ?: error("imageName is required")`처럼 함수 진입 시 바로 검증하면, 파이프라인 후반부에서 모호한 에러가 발생하는 것을 방지한다.
- **합리적인 기본값**을 제공하여 호출부의 부담을 줄인다. `config.tag ?: env.BUILD_NUMBER`처럼 대부분의 경우 적절한 기본값을 사용하되, 필요할 때는 오버라이드할 수 있게 한다.
- **반환값을 활용**한다. 예를 들어 `buildDocker()`가 빌드된 이미지 이름을 반환하면, 후속 단계에서 `def image = buildDocker(...)` 형태로 사용할 수 있다.
- **클로저를 통한 확장**: `standardPipeline(beforeDeploy: { sh './check.sh' })`처럼 클로저 파라미터를 받으면, 고정된 표준 위에 팀별 커스텀 로직을 유연하게 삽입할 수 있다.

**심화 질문**:
- vars/ 함수가 20개 이상으로 늘어났을 때, 네이밍 컨벤션과 문서화는 어떻게 관리하는가?
- vars/ 함수 내부에서 다른 vars/ 함수를 호출하는 것은 괜찮은가? 순환 의존성은 어떻게 방지하는가?
