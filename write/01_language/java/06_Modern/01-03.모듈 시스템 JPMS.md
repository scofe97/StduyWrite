# 모듈 시스템 JPMS

---

> JPMS는 classpath hell과 내부 API 오남용 문제를 해결하기 위해 Java 9에서 도입되었지만, 실무 채택은 여전히 제한적이며 대부분의 프로젝트가 unnamed module로 동작한다.

## 등장 배경

Java가 엔터프라이즈 환경에서 수십 년간 사용되면서 두 가지 고질적인 문제가 누적되었다. 첫째는 *classpath hell*로, 동일한 라이브러리의 여러 버전이 classpath에 공존할 때 어느 버전이 로드될지 보장할 수 없는 상황이다. 둘째는 캡슐화 부재로, `sun.misc.Unsafe` 같은 JDK 내부 API를 외부 라이브러리가 직접 사용하여 JDK 업그레이드가 어려워졌다.

**JPMS(Java Platform Module System)**는 이 문제를 해결하기 위해 Project Jigsaw로 개발되어 Java 9(JEP 261)에서 도입되었다. 모듈은 패키지의 상위 단위로, 어떤 패키지를 외부에 공개하고 어떤 모듈에 의존하는지를 명시적으로 선언한다. JDK 자체도 `java.base`, `java.sql`, `java.desktop` 등 수십 개의 모듈로 분리되었다.

## module-info.java

모듈은 소스 루트에 위치한 `module-info.java` 파일로 정의한다. 이 파일이 없으면 해당 JAR는 unnamed module로 취급된다.

```java
// module-info.java
module com.example.payment {
    // 의존 모듈 선언
    requires java.sql;
    requires transitive com.example.common;  // 전이 의존성

    // 공개 패키지
    exports com.example.payment.api;
    exports com.example.payment.model to com.example.web;  // 한정 공개

    // 리플렉션 허용 (프레임워크용)
    opens com.example.payment.entity to org.hibernate.orm;
    opens com.example.payment.dto;  // 모든 모듈에 리플렉션 허용

    // SPI 선언
    provides com.example.spi.PaymentProcessor
            with com.example.payment.impl.CreditCardProcessor;
    uses com.example.spi.Logger;
}
```

주요 키워드의 의미는 다음과 같다.

- `requires`: 컴파일·런타임에 필요한 모듈 의존성
- `requires transitive`: 이 모듈을 사용하는 모듈도 해당 의존성을 자동으로 가짐
- `exports`: 패키지를 다른 모듈에 공개 (리플렉션 불허)
- `opens`: 리플렉션 접근까지 허용 (프레임워크 어노테이션 처리 등)
- `provides ... with`: SPI 구현체 등록
- `uses`: SPI 인터페이스 사용 선언

## 모듈 유형

Java 런타임은 세 가지 모듈 유형을 구분한다.

| 유형 | 설명 | module-info.java |
|------|------|-----------------|
| Named module | 명시적 모듈 선언이 있는 JAR | 있음 |
| Automatic module | module-info 없이 module path에 추가된 JAR | 없음 (JAR 이름에서 자동 생성) |
| Unnamed module | classpath에 추가된 모든 JAR와 클래스 | 없음 |

*Automatic module*은 기존 라이브러리를 모듈 시스템과 점진적으로 통합하기 위한 다리 역할이다. classpath의 모든 패키지에 접근할 수 있고, `exports`된 모든 패키지를 자동으로 공개한다. **Unnamed module**은 전통적인 classpath 방식으로 동작하며, named module에서는 unnamed module을 `requires`할 수 없다.

## JDK 내부 API 캡슐화

JPMS 도입의 핵심 목적 중 하나는 `sun.misc.*`, `com.sun.*` 같은 JDK 내부 API의 접근을 차단하는 것이다. 이전에는 이 API들이 사실상 공개 API처럼 광범위하게 사용되었기 때문에, JDK는 하위 호환성을 위해 이를 변경하기 어려웠다.

Java 9부터는 이 API들이 모듈로 캡슐화되어 기본적으로 접근이 차단된다. 기존 라이브러리와의 호환성 문제가 발생하면 JVM 옵션으로 임시 우회할 수 있다.

```bash
# 컴파일 시 내부 API 접근 허용
javac --add-exports java.base/sun.nio.ch=ALL-UNNAMED MyClass.java

# 런타임에 리플렉션 접근 허용
java --add-opens java.base/java.lang=ALL-UNNAMED \
     --add-opens java.base/sun.nio.ch=ALL-UNNAMED \
     -jar myapp.jar
```

`ALL-UNNAMED`는 unnamed module(classpath의 모든 코드)에 접근을 허용한다는 의미다. 이는 임시 해결책으로, 장기적으로는 내부 API에 의존하는 라이브러리를 업그레이드하거나 대안 API로 교체해야 한다.

## 모듈 그래프와 의존성 해결

JVM 시작 시 모듈 시스템은 의존성 그래프를 구성하고 검증한다. 순환 의존성이 있으면 시작 자체가 실패한다. `java --list-modules`로 현재 JVM의 모든 시스템 모듈을 확인할 수 있고, `java --describe-module java.sql`로 특정 모듈의 의존성을 조회할 수 있다.

```bash
# 모듈 그래프 분석 도구
# 의존성 확인
java --describe-module java.sql

# 모듈 해결 과정 출력
java --show-module-resolution -m com.example.app/com.example.Main

# jdeps로 미선언 내부 API 의존성 탐지
jdeps --jdk-internals myapp.jar
```

**jlink**를 사용하면 애플리케이션에 필요한 모듈만 포함한 최소화된 커스텀 JRE를 생성할 수 있다. 컨테이너 환경에서 이미지 크기를 크게 줄이는 데 활용된다.

## 실무 JPMS 채택 현황

솔직히 말하면, 대부분의 실무 프로젝트는 JPMS를 적극 활용하지 않는다. Spring Boot, Hibernate, Jackson 같은 주요 프레임워크들이 내부적으로 리플렉션을 대량 사용하기 때문에, 완전한 named module로 전환하면 `opens` 선언을 모두 수동으로 관리해야 한다.

결과적으로 대부분의 Spring Boot 애플리케이션은 unnamed module로 동작하며, JDK 내부 API 차단 경고만 `--add-opens`로 억제하는 수준에 머물고 있다. JPMS가 실질적으로 효과를 발휘하는 영역은 SDK나 라이브러리 개발, 그리고 jlink를 통한 커스텀 런타임 구성이다.

## Spring Boot와 JPMS 호환성

Spring Boot 3.x는 Java 17을 최소 요구 버전으로 하지만, 완전한 JPMS 모듈로 동작하지는 않는다. Spring Framework 자체가 `Automatic module`로 동작하며, AOT(Ahead-of-Time) 처리와 GraalVM Native Image 빌드 시에는 리플렉션 힌트를 별도로 등록해야 한다.

```java
// Spring Boot에서 JPMS 관련 VM 옵션 (build.gradle 또는 pom.xml 설정)
// Gradle
tasks.withType(JavaCompile).configureEach {
    options.compilerArgs += [
            '--add-opens', 'java.base/java.lang=ALL-UNNAMED'
    ]
}

// Maven Surefire (테스트 실행 시)
// <argLine>--add-opens java.base/java.lang=ALL-UNNAMED</argLine>
```

JPMS를 실무에 도입하려면 사용 중인 모든 라이브러리의 모듈 지원 여부를 먼저 확인해야 한다. 단계적 접근으로 먼저 unnamed module로 Java 버전을 올린 후, 필요한 경우에만 named module 전환을 검토하는 것이 현실적이다.
