---
title: 05-spring-boot-gradle-version-compatibility
tags: []
status: draft
related: []
updated: 2026-04-19
---

# Spring Boot 버전 업그레이드와 Gradle/라이브러리 호환성
---
> 멀티모듈 프로젝트에서 새 모듈에만 Spring Boot 3.5.x를 적용하고, 기존 모듈은 3.2.x에 유지할 때 Gradle과 라이브러리 호환성 이슈를 정리한다.

## 배경

Spring Boot 3.5.x는 Gradle 최소 버전을 올려야 사용할 수 있다. Spring Boot 3.2.x는 Gradle 7.6.1 이상이면 충분하지만, 3.5.x는 Gradle 8.x 이상을 요구한다. 문제는 Gradle wrapper가 프로젝트 전체에 하나이기 때문에, 새 모듈을 위해 Gradle을 올리면 기존 모듈도 올라간 Gradle로 빌드된다는 점이다.

여기서 질문이 생긴다. 기존 모듈이 의존하는 라이브러리(Spring Boot 3.2.x 기반)도 함께 올려야 하는가?

## 결론

**대부분의 경우 기존 라이브러리를 올리지 않아도 된다.** Spring Boot 라이브러리는 하위 호환을 유지하므로, 3.2.x용 라이브러리가 3.5.x 모듈과 같은 프로젝트에 공존해도 빌드와 런타임 모두 정상 동작한다. Gradle 상위 버전도 하위 호환을 보장하기 때문에, 기존 3.2.x 모듈의 빌드가 깨질 가능성은 낮다.

다만 이 결론은 모듈 간 의존 관계와 배포 방식에 따라 달라진다. 아래 조건별 판단 기준을 확인해야 한다.

## 조건별 판단 기준

| 조건 | 이슈 여부 | 이유 |
|------|-----------|------|
| 각 모듈이 독립 배포 (마이크로서비스) | 없음 | 런타임이 분리되어 클래스패스 충돌 불가 |
| 모노리스인데 공통 모듈 의존 없음 | 거의 없음 | 전이 의존성이 섞이지 않음 |
| 공통 모듈을 양쪽에서 공유 | 충돌 가능 | 전이 의존성 버전 차이로 클래스패스 문제 |
| Gradle wrapper 버전 업그레이드 | 전체 영향 | wrapper는 프로젝트당 하나 |

독립 배포 구조라면 신경 쓸 것이 거의 없다. 반면 모노리스에서 공통 모듈을 공유하는 구조라면 아래 주의사항을 반드시 확인해야 한다.

## 주의할 점

### 1. Spring Boot BOM 충돌

멀티모듈 프로젝트에서 루트 `build.gradle`에 Spring Boot 플러그인을 선언하면, 해당 버전이 전체 모듈에 적용된다:

```groovy
// 루트 build.gradle — 이렇게 하면 전 모듈에 3.5.x가 적용된다
plugins {
    id 'org.springframework.boot' version '3.5.0'
}
```

새 모듈만 3.5.x를 쓰려면, **루트가 아닌 모듈 레벨에서 BOM을 관리**해야 한다:

```groovy
// new-module/build.gradle
plugins {
    id 'org.springframework.boot' version '3.5.0'
}

// legacy-module/build.gradle
plugins {
    id 'org.springframework.boot' version '3.2.12'
}
```

또는 루트에서 `apply false`로 선언하고 각 모듈에서 개별 적용하는 방식도 가능하다:

```groovy
// 루트 build.gradle
plugins {
    id 'org.springframework.boot' version '3.5.0' apply false
}

// 각 모듈에서 필요한 버전을 직접 선언
```

### 2. 공유 모듈 의존 방향

3.2.x 모듈이 만든 공통 모듈을 3.5.x 모듈이 의존하면 문제가 없다. 상위 버전은 하위 버전의 API를 포함하기 때문이다. 반대 방향은 위험하다. 3.5.x 모듈이 만든 공통 모듈을 3.2.x 모듈이 의존하면, 3.5.x에서 추가된 API를 호출하는 순간 `NoSuchMethodError`가 발생한다.

정리하면 의존 방향은 **낮은 버전 → 높은 버전**만 안전하다:

```
3.2.x 공통 모듈 ← 3.5.x 모듈이 의존   ✅ 안전
3.5.x 공통 모듈 ← 3.2.x 모듈이 의존   ❌ 위험
```

### 3. 전이 의존성 버전 차이

Spring Boot가 관리하는 전이 의존성(Jackson, Hibernate 등)의 버전이 3.2.x와 3.5.x에서 다르다:

```
Spring Boot 3.2.x → Jackson 2.15.x, Hibernate 6.2.x
Spring Boot 3.5.x → Jackson 2.18.x+, Hibernate 6.6.x+
```

같은 런타임(같은 JVM)에서 두 버전이 섞이면 클래스패스 충돌이 발생할 수 있다. 모듈이 독립 배포(별도 JAR/서비스)라면 런타임이 분리되므로 문제없지만, 하나의 WAR/JAR로 패키징하는 모노리스에서는 주의가 필요하다.

Gradle의 의존성 해결 전략은 기본적으로 **가장 높은 버전을 채택**하므로, 3.5.x 모듈이 있으면 Jackson 2.18.x가 전체에 적용된다. 대부분의 경우 상위 호환이 되지만, 간혹 deprecated API 제거나 동작 변경으로 기존 모듈이 깨질 수 있다.

### 4. Gradle Wrapper는 프로젝트 전체에 하나

Gradle wrapper(`gradle/wrapper/gradle-wrapper.properties`)는 프로젝트당 하나다. 새 모듈을 위해 Gradle 8.x로 올리면 기존 모듈도 8.x로 빌드된다.

Gradle은 상위 버전에서 하위 호환을 보장하므로 빌드가 깨질 가능성은 낮다. 다만 deprecated 경고가 늘어날 수 있고, Gradle 플러그인 중 특정 Gradle 버전에 종속된 것이 있다면 호환성을 확인해야 한다.

```bash
# Gradle 업그레이드 후 deprecated 경고 확인
./gradlew build --warning-mode all
```

## 실무 판단 플로우

업그레이드 결정 시 다음 순서로 판단한다:

```
1. 모듈 배포 방식 확인
   ├── 독립 배포 (마이크로서비스) → 이슈 없음, 바로 진행
   └── 모노리스 / 공유 모듈 있음 → 2번으로

2. 공통 모듈 의존 방향 확인
   ├── 3.2.x 공통 ← 3.5.x 모듈 의존 → 안전
   └── 3.5.x 공통 ← 3.2.x 모듈 의존 → 위험, 공통 모듈 버전 조정 필요

3. Gradle wrapper 업그레이드
   └── ./gradlew build --warning-mode all 실행
       ├── 빌드 성공 → 진행
       └── 빌드 실패 → 실패한 플러그인/의존성만 업그레이드

4. 전이 의존성 충돌 확인
   └── ./gradlew dependencies --configuration runtimeClasspath
       ├── 버전 충돌 없음 → 완료
       └── 충돌 있음 → 해당 라이브러리만 버전 고정
```

전이 의존성 충돌이 발견되면 `build.gradle`에서 특정 버전을 강제 지정할 수 있다:

```groovy
// 특정 라이브러리 버전 강제 지정
configurations.all {
    resolutionStrategy {
        force 'com.fasterxml.jackson.core:jackson-databind:2.15.4'
    }
}
```

다만 이 방식은 임시 조치에 가깝다. 장기적으로는 전체 모듈을 동일 Spring Boot 버전으로 통일하는 것이 유지보수 비용을 줄인다.

## Spring Boot 3.2 → 3.5 주요 변경점

버전을 올릴 때 알아야 할 주요 변경 사항을 정리한다. 이 목록은 호환성에 영향을 줄 수 있는 항목 위주로 선별한 것이다:

- **Gradle 최소 버전**: 7.6.1 → 8.x 이상 필요
- **Java 최소 버전**: 17 유지 (3.2.x와 동일), 21 권장
- **Jakarta EE**: 3.2.x에서 이미 Jakarta 전환 완료, 3.5.x에서 추가 변경 없음
- **Spring Framework**: 6.1.x → 6.2.x로 업그레이드 (내부 API 일부 변경)
- **Hibernate**: 6.2.x → 6.6.x (HQL 파서 변경, 일부 쿼리 동작 차이)
- **Jackson**: 2.15.x → 2.18.x (새 직렬화 옵션, deprecated API 제거)
- **Virtual Thread 지원 강화**: 3.5.x에서 `spring.threads.virtual.enabled` 공식 지원

이 중 Hibernate와 Jackson의 메이저 업데이트가 기존 코드에 영향을 줄 가능성이 가장 높다. 업그레이드 후 반드시 기존 테스트를 전수 실행해야 한다.

## 정리

새 모듈에만 Spring Boot 3.5.x를 적용하고 기존 모듈은 3.2.x에 유지하는 것은 기술적으로 가능하다. Gradle wrapper 업그레이드는 전체에 영향을 주지만, Gradle의 하위 호환성 덕분에 기존 빌드가 깨질 확률은 낮다. 핵심은 모듈 간 의존 방향과 전이 의존성 충돌을 확인하는 것이다.

다만 하나의 프로젝트에 두 가지 Spring Boot 버전이 공존하는 상태는 유지보수 부담을 만든다. 가능하다면 전체 모듈을 3.5.x로 통일하는 마이그레이션 계획을 함께 세우는 것이 바람직하다.
