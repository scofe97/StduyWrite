# [Spring MSA] xx. 멀티모듈 아키텍쳐

주제: Spring MSA

- 참고
    
    [[Server] 멀티 모듈을 설계하는 관점과 고려사항 with Spring & Gradle](https://mangkyu.tistory.com/304)
    
    [스프링 부트 단일 모듈 코드에 멀티 모듈을 적용하여 프로젝트 구조 개선하기](https://velog.io/@jonghyun3668/스프링-부트-단일-모듈-코드에-멀티-모듈을-적용하여-프로젝트-구조-개선하기)
    
    [[Spring] 멀티 모듈 프로젝트 만들기](https://velog.io/@soyeon207/스프링-부트-멀티-모듈-프로젝트-만들기)
    
    [스프링부트 그레이들 멀티 모듈 프로젝트 (SpringBoot Gradle Multi Module)](https://devfoxstar.github.io/spring/gradle-multi-module/)
    
    [멀티모듈은 무엇이고 왜 사용할까 ?](https://jie0025.tistory.com/534)
    
    [[Spring] 멀티 모듈 프로젝트 적용](https://www.devjoon.com/60)
    

# 멀티 모듈 프로젝트를 만드는 이유

---

<aside>
💡 **NOTE**

> ***모듈은 패키지의 한 단계 위의 집합이며 자바에서는 독립적으로 배포될 수 있는 코드의 단위이다!***
> 

**MSA 서비스를 개발하다보면 각 서버에서 동작할 프로젝트가 필요하게되고 이를 하나의 단일 프로젝트로 개발하게 되면 다음과 같은 문제가 생긴다.**

- 공통적으로 처리해야하는 코드의 처리
    - 각 프로젝트의 공통되는 코드들은 각 프로젝트에 복붙해서 사용할 수 밖에 없다
    - 한 파일의 코드가 수정된다면 다른 프로젝트의 코드도 수정해야 한다.
- 접근성 문제
    - 프로젝트 수에 따라 IDE를 실행시켜야한다.

**멀티 모듈로 개발하면 위에서 발생하는 문제들을 해결해줄 수 있다!**

- 코드 재사용성
    - 공통 기능을 하나의 모듈에 구축하고, 여러 모듈에서 활용한다.
- 기능 분리
    - 모듈별로 기능을 분리해서 직관적인 프로젝트 관리가 가능하다.
- 빌드 유연성
    - 루트 프로젝트에서 전체를 빌드할 수도 있고, 개별 모듈 별로 빌드할 수도 있다.
- 의존성 분리
    - 전체 프로젝트에 의존성을 추가할 필요 없이, 개별 모듈에 필요한 의존성을 지정할 수 있다.
</aside>

## 멀티 모듈 프로젝트 구성 1

<aside>
✍️ **NOTE**

![다음의 구성으로 멀티 모듈을 작성한다.](%5BSpring%20MSA%5D%20xx%20%EB%A9%80%ED%8B%B0%EB%AA%A8%EB%93%88%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90/Untitled.png)

다음의 구성으로 멀티 모듈을 작성한다.

```kotlin
rootProject.name = "ordering-project"

include(
    "order-service:order-application",
    "order-service:order-container",
    "order-service:order-dataaccess",
    "order-service:order-domain:order-application-service",
    "order-service:order-domain:order-domain-core",
    "order-service:order-messaging",
)
```

![모듈 패키지](%5BSpring%20MSA%5D%20xx%20%EB%A9%80%ED%8B%B0%EB%AA%A8%EB%93%88%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90/Untitled%201.png)

모듈 패키지

[Groovy에서 KTS로 빌드 구성 이전  |  Android 개발자  |  Android Developers](https://developer.android.com/studio/build/migrate-to-kts?hl=ko)

```kotlin
import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

// 플러그인 선언
// Kotlin, Spring 관련 플러그인과, Springboot, 의존성 관련 플러그인
plugins {
	kotlin("jvm") version "1.9.20"
	kotlin("plugin.spring") version "1.9.20" apply false
	id("org.springframework.boot") version "3.2.0" apply false
	id("io.spring.dependency-management") version "1.1.4" apply false
}

// 자바 버전 설정
java {
	sourceCompatibility = JavaVersion.VERSION_17
}

// 모든 프로젝트(루트 - 서브 모듈)에 공통적으로 적용
// 루트 프로젝트 포함
allprojects{

	// 프로젝트 그룹 & 버전 설정
	group = "com.example"
	version = "0.0.1-SNAPSHOT"

	// Maven 중앙 저장소 사용
	repositories {
		mavenCentral()
	}
}

// 서브 프로젝트에만 적용될 설정
// root 프로젝트에 영향이 가지 않음
subprojects{

	// 서브 프로젝트에 Kotlin 및 Spring Boot 관련 플러그인 적용
	// 프로젝트의 빌드에 사용된다. (위에서 사용한 플러그인을 적용시킨것)
	apply(plugin = "org.jetbrains.kotlin.jvm")
	apply(plugin = "org.jetbrains.kotlin.plugin.spring")
	apply(plugin = "org.springframework.boot")
	apply(plugin = "io.spring.dependency-management")

	// bootJar 태스크 비활성화, jar 태스크 활성화
	// 기본적으로 Spring Boot는 bootJar를 사용하지만, 일반 Jar 파일을 생성하려면 이렇게 설정
	// 일반적인 서브모듈은 스프링이 없는 일반 빌드 Jar을 사용하도록 한다.
	tasks.getByName("bootJar"){
		enabled = false
	}

	tasks.getByName("jar"){
		enabled = true
	}

	// 공통 의존성
	// 컴파일, 테스트 등에서 사용하는 외부 라이브러리나 모듈을 의미한다.
	dependencies {
		//implementation("org.springframework.boot:spring-boot-starter-web")
		implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
		implementation("org.jetbrains.kotlin:kotlin-reflect")
		testImplementation("org.springframework.boot:spring-boot-starter-test")
	}

	// Kotlin 컴파일 옵션
	tasks.withType<KotlinCompile> {
		kotlinOptions {
			freeCompilerArgs += "-Xjsr305=strict"
			jvmTarget = "17"
		}
	}

	// 테스트 태스크 섲렁
	tasks.withType<Test> {
		useJUnitPlatform()
	}

}
```

**allproject**, **subproject**, **project**(모듈 이름)으로 원하는 범위만큼의 모듈에 원하는 설정을 할 수 있다.

```kotlin
// bootJar 태스크 활성화, jar 태스크 비활성화
// 이 설정은 서브 모듈에서 Spring Boot 실행 가능 Jar를 생성할 때 필요
tasks.getByName("bootJar"){
	enabled = true
}

tasks.getByName("jar"){
	enabled = false
}

// order-application-service 모듈의존
dependencies {
	implementation("org.springframework.boot:spring-boot-starter-web")
	implementation(":order-service:order-domain:order-application-service")
}
```

여기서 bootJar의 경우 실행가능한 jar을 만들어야 하기 때문에, main()이 필요하다. 때문에 main()이 없는 경우는 flase로 설정해줘야 한다.

</aside>

## 멀티 모듈 프로젝트의 구성 2

<aside>
✍️ **NOTE**

![다른 사람이 모듈을 설계한 이미지](%5BSpring%20MSA%5D%20xx%20%EB%A9%80%ED%8B%B0%EB%AA%A8%EB%93%88%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90/Untitled%202.png)

다른 사람이 모듈을 설계한 이미지

- api (프로젝트 루트)
    - api-core (api 공통)
        - 공통 유틸을 비롯한 프로젝트 공통 기능 모듈
    - api-domain (api 데이터)
        - Service, Repositroy, Entity 등 데이터 모듈
    - api-web
        - 컨트롤러를 비롯한 통신 모듈

```kotlin
dependencies {
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

tasks.bootJar {
    enabled = false
}

tasks.jar {
    enabled = true
}
```

```kotlin
dependencies {
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

tasks.bootJar {
    enabled = false
}

tasks.jar {
    enabled = true
}
```

```kotlin
dependencies {

    api("io.springfox:springfox-boot-starter:3.0.0")

    implementation(project(":api-core"))
    implementation(project(":api-domain"))

    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.jetbrains.kotlin:kotlin-reflect")
    implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}
```

- **api**
    - 해당 모듈을 의존하는 다른 모듈에도 노출된다.
- **implementation**
    - 현재 내 모듈내에서만 사용한다. (다른 모듈이 접근하지 못한다)
    
</aside>

## 멀티 모듈 프로젝트의 구성 3

<aside>
✍️ **NOTE**

```kotlin
@SpringBootApplication(
	scanBasePackages = {패키지 이름 작성})
public class ApiApplication {

	public static void main(String[] args) {
		SpringApplication.run(ApiApplication.class, args);
	}
}
```

별도의 설정을 하지 않는다면 Spring은 다른 모듈에 있는 클래스들을 Bean으로 등록하지 않는다. 

- 위와 같이 scanBasePackage에 패키지 이름을 입력해야 정상적으로 Bean으로 등록된다!
</aside>