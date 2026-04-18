# Java 모듈 시스템(JPMS): Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. JPMS를 채택하지 않는 프로젝트가 대부분인 이유는 무엇인가

### 왜 이 질문이 중요한가
Java 9에서 도입된 JPMS는 거대한 기능이지만 실제 채택률은 낮다. 이유를 설명할 수 없으면 기술 평가나 아키텍처 논의에서 피상적인 답변에 그친다.

### 답변
JPMS(Java Platform Module System)가 대부분의 애플리케이션 프로젝트에서 채택되지 않는 이유는 크게 네 가지다.

첫째, 마이그레이션 비용 대비 이득이 불분명하다. JPMS는 모든 의존성이 모듈화되어야 완전한 이점을 얻는다. 그런데 Maven Central의 라이브러리 대다수는 아직도 "자동 모듈(automatic module)"이나 "이름 없는 모듈(unnamed module)" 상태다. 부분 모듈화는 캡슐화 이점을 제공하지 못하면서 복잡성만 추가한다.

둘째, 기존 리플렉션 기반 프레임워크와 충돌한다. Spring, Hibernate, Jackson 같은 주요 프레임워크는 리플렉션을 광범위하게 사용한다. JPMS는 기본적으로 모듈 경계를 넘는 리플렉션을 차단하므로 `--add-opens` 옵션이 넘쳐나게 된다. 이는 JPMS의 캡슐화 목적을 무력화한다.

```
# 현실의 module-info.java를 제대로 쓰려면
# 수십 개의 --add-opens가 필요할 수 있음
--add-opens java.base/java.lang=ALL-UNNAMED
--add-opens java.base/java.util=ALL-UNNAMED
--add-opens java.base/java.lang.reflect=ALL-UNNAMED
# ... 수십 줄
```

셋째, 클래스패스 기반 개발 방식의 관성이 크다. 25년간의 클래스패스 기반 개발 패러다임, 빌드 도구(Maven, Gradle), IDE 지원이 JPMS보다 훨씬 성숙하다. JPMS 전환은 빌드 스크립트 수정, `module-info.java` 작성, 테스트 설정 변경을 수반한다.

넷째, 컨테이너가 대체 격리 수단을 제공한다. JPMS의 주요 이점 중 하나인 배포 크기 감소(jlink로 필요한 모듈만 포함)는 Docker 멀티스테이지 빌드와 GraalVM Native Image로도 달성할 수 있다. 애플리케이션 간 격리는 컨테이너나 마이크로서비스 아키텍처가 제공한다.

JPMS가 잘 맞는 경우는 JDK 자체나 라이브러리를 개발하는 경우, 또는 jlink로 최소화된 JRE를 생성해 임베디드 환경에 배포하는 경우다.

---

## Q2. --add-opens 남용의 위험은 무엇인가

### 왜 이 질문이 중요한가
레거시 애플리케이션을 Java 9+로 마이그레이션할 때 `--add-opens`를 무분별하게 추가하는 경우가 많다. 이 관행의 위험을 알아야 단기 해결책과 장기 전략을 구분할 수 있다.

### 답변
`--add-opens module/package=target`은 지정된 모듈의 패키지를 타겟 모듈(또는 모든 코드)에 깊은 리플렉션(deep reflection)으로 접근 가능하게 연다. JPMS가 닫은 문을 다시 여는 것이다.

위험은 네 가지 차원에서 발생한다.

첫째, 보안 캡슐화 훼손이다. JPMS의 핵심 목적은 내부 API(`sun.*`, `com.sun.*`, `java.lang` 내부)를 외부에서 접근하지 못하게 하는 것이다. `--add-opens`로 이를 열면 공격자가 JVM 내부 구조를 조작할 수 있는 취약점이 생긴다. 특히 `java.lang.reflect.Field`에 대한 접근을 열면 `final` 필드도 수정 가능해진다.

둘째, 미래 JDK 버전에서의 깨짐이다. 내부 API는 공식 계약이 아니어서 언제든 변경되거나 제거될 수 있다. `--add-opens`로 접근하는 코드는 JDK 업그레이드마다 깨질 위험이 있다. Java 17에서 `sun.misc.Unsafe`의 일부 메서드가 제거되었고, 이후 버전에서도 유사한 변경이 계속된다.

셋째, 모니터링과 감사 어려움이다. JVM 옵션에 넣어둔 `--add-opens`는 코드 리뷰에서 보이지 않아 조직의 보안 정책을 우회하는 경로가 될 수 있다.

```bash
# 잘못된 관행 — ALL-UNNAMED로 모두 열기
java --add-opens java.base/java.lang=ALL-UNNAMED \
     --add-opens java.base/java.lang.reflect=ALL-UNNAMED \
     --add-opens java.base/java.util=ALL-UNNAMED \
     # ... 계속 추가
     -jar app.jar

# 올바른 접근
# 1. 어떤 라이브러리가 이 옵션을 요구하는지 파악
# 2. 해당 라이브러리의 최신 버전(모듈 지원)으로 업그레이드
# 3. 업그레이드 불가능하면 해당 라이브러리만 명시적 모듈로 한정
```

올바른 대응 전략은 `--add-opens`를 임시 해결책으로 명시적으로 문서화하고, 라이브러리 의존성을 최신 버전으로 업그레이드하는 계획을 세우며, 매 JDK 버전 업그레이드 시 `--add-opens` 목록을 검토해 제거 가능한 것을 제거하는 것이다.
