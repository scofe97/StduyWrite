# [Spring Study] xx.  스프링 부트와 내장 톰캣

주제: Spring Study

- 참고
    
    [스프링 부트 - 핵심 원리와 활용 - 스프링 부트와 내장 톰캣](https://soono-991.tistory.com/34)
    

# WAR 배포 방식의 단점

---

<aside>
💡 **NOTE**

> ***WAR배포 방식은 너무나 복잡했다 단순히 main()을 실행하면 서버가 실행되는 방식은 없는가?***
> 

![JAR은 main()을 통해 동작한다 (톰캣을 라이브러리(내장 톰캣)로 사용함!)](%5BSpring%20Study%5D%20xx%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EB%B6%80%ED%8A%B8%EC%99%80%20%EB%82%B4%EC%9E%A5%20%ED%86%B0%EC%BA%A3/Untitled.png)

JAR은 main()을 통해 동작한다 (톰캣을 라이브러리(내장 톰캣)로 사용함!)

```java
//내장 톰켓 추가
implementation 'org.apache.tomcat.embed:tomcat-embed-core:10.1.5'
```

</aside>

## 내장 톰캣 실제로 사용해보기

<aside>
✍️ **NOTE**

```java
public class EmbedTomcatServletMain {

    public static void main(String[] args) throws LifecycleException {
        System.out.println("EmbedTomcatServletMain.main");

        // tomcat setting
        Tomcat tomcat = new Tomcat();
        Connector connector = new Connector();
        connector.setPort(8080);
        tomcat.setConnector(connector);

        // Servlet add
        Context context = tomcat.addContext("", "/");

				// 예와발생시 코드추가
        File docBaseFile = new File(context.getDocBase());
        if (!docBaseFile.isAbsolute()) {
            docBaseFile = new File(((org.apache.catalina.Host) context.getParent()).getAppBaseFile(), docBaseFile.getPath());
        }
        docBaseFile.mkdirs();
				// 코드추가 끝 

        tomcat.addServlet("", "helloServlet", new HelloServlet());
        context.addServletMappingDecoded("/hello-servlet", "helloServlet");
        tomcat.start();

    }
}
```

![Untitled](%5BSpring%20Study%5D%20xx%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EB%B6%80%ED%8A%B8%EC%99%80%20%EB%82%B4%EC%9E%A5%20%ED%86%B0%EC%BA%A3/Untitled%201.png)

```java
public class EmbedTomcatSpringMain {

    public static void main(String[] args) throws LifecycleException {
        System.out.println("EmbedTomcatServletMain.main");

        // tomcat setting
        Tomcat tomcat = new Tomcat();
        Connector connector = new Connector();
        connector.setPort(8080);
        tomcat.setConnector(connector);

				// 스프링 컨테이너 생성
        AnnotationConfigWebApplicationContext appContext = new
                AnnotationConfigWebApplicationContext();
        appContext.register(HelloConfig.class);

				// 스프링 MVC 디스패쳐 서블릿 생성, 스프링 컨테이너 연결
        DispatcherServlet dispatcher = new DispatcherServlet(appContext);
        
				// 디스패쳐 서블릿 등록
        Context context = tomcat.addContext("", "/");
        tomcat.addServlet("", "dispatcher", dispatcher);
        context.addServletMappingDecoded("/", "dispatcher");
        tomcat.start();
    }
}
```

![Untitled](%5BSpring%20Study%5D%20xx%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EB%B6%80%ED%8A%B8%EC%99%80%20%EB%82%B4%EC%9E%A5%20%ED%86%B0%EC%BA%A3/Untitled%202.png)

</aside>

## 빌드와 배포 (jar, fat-jar)

<aside>
✍️ **NOTE**

> ***내장 톰캣은 어떻게 빌드하고 배포하는가?***
> 

```groovy
Manifest-Version: 1.0
Main-Class: hello.embed.EmbedTomcatSpringMain
```

### 일반 JAR

```groovy
//일반 Jar 생성
task buildJar(type: Jar) {
    manifest {
        attributes 'Main-Class': 'hello.embed.EmbedTomcatSpringMain'
    }
    with jar
}
```

```bash
# 압축해제 코드 (./build/libs로 먼저 이동)
jar -xvf embed-0.0.1-SNAPSHOT.jar
```

![파일 생성됨](%5BSpring%20Study%5D%20xx%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EB%B6%80%ED%8A%B8%EC%99%80%20%EB%82%B4%EC%9E%A5%20%ED%86%B0%EC%BA%A3/Untitled%203.png)

파일 생성됨

![압축파일 내용 (WAR과 비교해서 **lib폴더**가 없다)](%5BSpring%20Study%5D%20xx%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EB%B6%80%ED%8A%B8%EC%99%80%20%EB%82%B4%EC%9E%A5%20%ED%86%B0%EC%BA%A3/Untitled%204.png)

압축파일 내용 (WAR과 비교해서 **lib폴더**가 없다)

- `./gradlew clean buildJar` 를 입력하면 위의 코드가 실행된다. (에러발생)
- **lib 폴더**가 없기 떄문에 스프링 라이브러리나, 톰캣 내장 라이브러리가 없으므로 에러가 발생한다.
- JAR은 WAR과 다르게 내부에 라이브러리 역할을 하는 파일을 포함할 수 없다.

### Fat JAR

```groovy
//Fat Jar 생성
task buildFatJar(type: Jar) {
    manifest {
        attributes 'Main-Class': 'hello.embed.EmbedTomcatSpringMain'
    }
    duplicatesStrategy = DuplicatesStrategy.WARN
    from { configurations.runtimeClasspath.collect { it.isDirectory() ? it : zipTree(it) } }
    with jar
}
```

```bash
# 압축해제 코드 (./build/libs로 먼저 이동)
jar -xvf embed-0.0.1-SNAPSHOT.jar
```

![폴더를 열면 수많은 파일들이 나온다.](%5BSpring%20Study%5D%20xx%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EB%B6%80%ED%8A%B8%EC%99%80%20%EB%82%B4%EC%9E%A5%20%ED%86%B0%EC%BA%A3/Untitled%205.png)

폴더를 열면 수많은 파일들이 나온다.

- 이제 build는 되는데, 아직 단점들이 많다.
- 모든 클래스를 압축해제해서 어떤 라이브러리를 쓰는지 알기 힘들며, 파일명 중복을 해결할 수 없다.
</aside>

## 편리한 스프링부트 클래스 만들기

<aside>
✍️ **NOTE**

```java
@MySpringBootApplication
public class MySpringBootMain {

    public static void main(String[] args) {
        MySpringApplication.run(MySpringBootMain.class, args);
    }
}
```

```java
public class MySpringApplication {

    public static void run(Class ConfigClass, String[] args) {
        System.out.println("MySpringApplication.main args=" + List.of(args));

        // tomcat setting
        Tomcat tomcat = new Tomcat();
        Connector connector = new Connector();
        connector.setPort(8080);
        tomcat.setConnector(connector);

        // 스프링 컨테이너 생성
        AnnotationConfigWebApplicationContext appContext = new
                AnnotationConfigWebApplicationContext();
        appContext.register(HelloConfig.class);

				// 스프링 MVC 디스패쳐 서블릿 생성, 스프링 컨테이너 연결
        DispatcherServlet dispatcher = new DispatcherServlet(appContext);
        
				// 디스패쳐 서블릿 등록
        Context context = tomcat.addContext("", "/");
        tomcat.addServlet("", "dispatcher", dispatcher);
        context.addServletMappingDecoded("/", "dispatcher");
        try {
            tomcat.start();
        } catch (LifecycleException e) {
            throw new RuntimeException(e);
        }
    }
}
```

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@ComponentScan
public @interface MySpringBootApplication {
}
```

</aside>

## 스프링 부트와 웹 서버

<aside>
✍️ **NOTE**

```java
@SpringBootApplication
public class BootApplication {

	public static void main(String[] args) {
		SpringApplication.run(BootApplication.class, args);
	}
}
```

- 단순해 보이는 저 코드 한줄에는 수 많은 일들이 발생하지만 핵심은 2가지다.
    1. 스프링 컨테이너를 생성한다.
    2. WAS(내장 톰캣)을 생성한다.

### 빌드와 배포, executable jar(실행가능한 jar)

```bash
# 빌드
./gradlew clean build

# 실행 (Fat JAR보다 압도적으로 용량이 가벼움)
java -jar boot-0.0.1-SNAPSHOT.jar

# 압축해제
jar -xvf boot-0.0.1-SNAPSHOT.jar
```

![plain은 신경쓰지 않아도된다.](%5BSpring%20Study%5D%20xx%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EB%B6%80%ED%8A%B8%EC%99%80%20%EB%82%B4%EC%9E%A5%20%ED%86%B0%EC%BA%A3/Untitled%206.png)

plain은 신경쓰지 않아도된다.

![압축해제 - lib가 존재한다 (왜?)
Fat-Jar가 아니라 새로운 구조로 만들어짐.](%5BSpring%20Study%5D%20xx%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EB%B6%80%ED%8A%B8%EC%99%80%20%EB%82%B4%EC%9E%A5%20%ED%86%B0%EC%BA%A3/Untitled%207.png)

압축해제 - lib가 존재한다 (왜?)
Fat-Jar가 아니라 새로운 구조로 만들어짐.

- 스프링부트가 Fat-jar 문제를 해결하기 위해 특별한 구조의 jar을 만들었으며 이 구조를 **실행 가능한 Jar**이라고 한다.
- 동시에 이러한 jar를 내부 jar를 포함해서 실행할 수 있게한다.
- 여러 설명이 있었는데 그냥 참고하는 정도로만 기억하자.
</aside>