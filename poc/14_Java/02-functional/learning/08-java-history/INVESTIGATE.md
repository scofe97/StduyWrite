# Java 역사와 버전 전략: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. LTS 전략이 기업의 Java 버전 선택에 미치는 영향은 무엇인가

### 왜 이 질문이 중요한가
Java 11 이후 6개월 릴리즈 주기와 LTS 정책은 기업의 기술 부채와 업그레이드 전략에 직접 영향을 미친다. 버전 선택의 근거를 설명할 수 있어야 아키텍처 논의에 참여할 수 있다.

### 답변
Oracle은 2017년(Java 9)부터 6개월 릴리즈 주기를 도입했다. 매년 3월과 9월에 새 버전이 나오고, 그 중 일부가 LTS(Long-Term Support) 버전이다. LTS 버전은 최소 8년간 보안 패치와 버그 수정을 받는다(Oracle의 경우 Extended Support 포함).

LTS 버전 목록: 8(2014), 11(2018), 17(2021), 21(2023), 25(2025년 9월 예정). Java 17부터 3년 주기 LTS가 확정되었다.

기업 영향은 크게 세 가지로 나타난다.

첫째, 보수적 기업은 LTS만 사용한다. 금융, 공공, 레거시 시스템을 운영하는 기업들은 비LTS 버전의 짧은 지원 기간(6개월)을 감수하지 않는다. Java 8에서 11로, 11에서 17로, 이제 17에서 21로 이동하는 것이 일반적인 엔터프라이즈 패턴이다.

둘째, 업그레이드 주기가 길어진다. Java 8은 무려 10년 가까이 많은 기업의 표준이었다. 이는 신규 언어 기능(Stream, var, record, sealed class)의 채택이 느렸다는 의미다. Java 17이나 21의 기능(Virtual Thread, Pattern Matching, Record)을 실무에서 사용하려면 조직의 LTS 업그레이드 결정이 선행되어야 한다.

셋째, 컨테이너/클라우드 환경에서는 업그레이드가 더 쉬워졌다. Docker 이미지로 Java 버전을 격리하면 조직 전체 업그레이드 없이 서비스별 독립 업그레이드가 가능해져 LTS 제약이 다소 완화된다.

---

## Q2. Java 8에서 21로의 마이그레이션 핵심 포인트는 무엇인가

### 왜 이 질문이 중요한가
많은 레거시 코드베이스가 여전히 Java 8 기반이다. 마이그레이션의 주요 장애물과 얻을 수 있는 것을 알아야 비용-편익 분석을 할 수 있다.

### 답변
Java 8 → 21 마이그레이션의 주요 장애물과 대응 방법을 단계별로 살펴본다.

첫 번째 장애물은 모듈 시스템(JPMS, Java 9)이다. Java 9에서 도입된 모듈 시스템은 `sun.*`, `com.sun.*` 같은 내부 API 접근을 차단한다. 많은 레거시 라이브러리가 이런 내부 API를 사용하므로 `IllegalAccessException`이 발생한다. 단기 해결책은 `--add-opens`, `--add-exports` JVM 옵션이고, 장기 해결책은 최신 버전의 라이브러리로 업그레이드하는 것이다.

```bash
# 임시 해결책 — 내부 API 접근 허용
java --add-opens java.base/java.lang=ALL-UNNAMED \
     --add-opens java.base/java.util=ALL-UNNAMED \
     -jar app.jar
```

두 번째 장애물은 제거된 API다. Java 11에서 `javax.*` 패키지(JAXB, JAX-WS, Corba, Java EE 관련)가 JDK에서 제거되었다. 이를 사용하는 코드는 별도 의존성을 추가해야 한다.

```xml
<!-- Java 11+ JAXB 별도 의존성 -->
<dependency>
    <groupId>jakarta.xml.bind</groupId>
    <artifactId>jakarta.xml.bind-api</artifactId>
    <version>3.0.1</version>
</dependency>
```

세 번째는 GC 변경이다. Java 11에서 G1GC가 기본 GC가 되었고, Java 15에서 ZGC, Java 16에서 Shenandoah가 프로덕션 Ready가 되었다. 기존 CMS GC는 Java 14에서 제거되었다. GC 튜닝 파라미터를 재검토해야 한다.

반대로 얻을 수 있는 것도 크다. `var`(Java 10), `record`(Java 16), `sealed class`(Java 17), `pattern matching`(Java 16~21)으로 보일러플레이트가 줄어들고, `String` 개선(`strip`, `isBlank`, `lines`, `formatted`), `Map.of`, `List.of` 불변 컬렉션, `HttpClient`(Java 11) 내장, Virtual Thread(Java 21)가 IO 성능을 크게 향상시킨다.

마이그레이션 전략으로는 Spring Boot 3.x(Java 17+), Quarkus, Micronaut 같은 프레임워크 업그레이드를 트리거로 삼는 것이 효과적이다. 프레임워크가 최신 Java의 이점을 최대로 활용하도록 설계되어 있어 마이그레이션 동기가 명확해진다.
