# [Spring Study] xx. 웹 서버와 서블릿 컨테이너(WAR 배포방식)

주제: Spring Study

- 참고
    
    [스프링 부트 - 핵심 원리와 활용 - 스프링 부트와 내장 톰캣](https://soono-991.tistory.com/34)
    

# 웹 서버와 스프링 부트 소개

---

<aside>
💡 **NOTE**

> ***스프링 부트는 어떤 원리로 내장 톰캣을 사용해서 실행할 수 있는것인가?***
> 

![최근버전인 JAR 대신, WAR을 어떻게 하는지 알아보자](%5BSpring%20Study%5D%20xx%20%EC%9B%B9%20%EC%84%9C%EB%B2%84%EC%99%80%20%EC%84%9C%EB%B8%94%EB%A6%BF%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88(WAR%20%EB%B0%B0%ED%8F%AC%EB%B0%A9%EC%8B%9D)/Untitled.png)

최근버전인 JAR 대신, WAR을 어떻게 하는지 알아보자

</aside>

## WAR vs JAR

<aside>
✍️ **NOTE**

### WAR(Web Application Archive)

![기본 구조](%5BSpring%20Study%5D%20xx%20%EC%9B%B9%20%EC%84%9C%EB%B2%84%EC%99%80%20%EC%84%9C%EB%B8%94%EB%A6%BF%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88(WAR%20%EB%B0%B0%ED%8F%AC%EB%B0%A9%EC%8B%9D)/Untitled%201.png)

기본 구조

- **서버에 배포할 떄 사용하는 파일이다.**
- jar파일이 JVM위에서 실행되면 WAR는 웹 애플리케이션 서버 위에서 실행된다.
- 서버위에서 실행되고, HTML과 같은 정적리소스 클래스 파일을 모두 포함하기에 구조가 JAR에 비해 복잡하다.

### JAR(Java Archive)

- **여러 클래스와 리소스를 압축파일로 만드는 방식이다.**
- 이 파일은 JVM위에서 직접 실행되거나 다른 곳에서 사용하는 라이브러리로 제공된다.
- 직접 실행하는 경우 main()이 필요하고, MANIFEST.MF 파일에 실행할 메인 메서드가 있는 클래스를 지정한다.
- 실행 예) `java -jar [.jar 파일이름]`
</aside>

## 톰캣 설치하고 사용하기

<aside>
✍️ **NOTE**

[Apache Tomcat® - Apache Tomcat 10 Software Downloads](https://tomcat.apache.org/download-10.cgi)

설치 링크

```bash
# 톰캣 다운로드 이후 /bin경로로 이동
chmode 755 *

./startup.bat # 톰캣실행
./shutdown.bat # 톰캣종료

netstat -ano | findstr :포트번호 # 8080포트 찾기
taskkill /f /pid 프로세스번호 # 8080 포트 프로세스 죽이기
```

```java
@WebServlet(urlPatterns = "/test")
public class TestServlet extends HttpServlet {

    @Override
    protected void service(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        System.out.println("TestServlet.service");
        resp.getWriter().println("test");
    }
}
```

```bash
# war 파일생성
./gradlew build

cd ./build/libs
ls

# 압축해제
jar -xvf server-0.0.1-SNAPSHOT.war
```

![war 파일생성](%5BSpring%20Study%5D%20xx%20%EC%9B%B9%20%EC%84%9C%EB%B2%84%EC%99%80%20%EC%84%9C%EB%B8%94%EB%A6%BF%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88(WAR%20%EB%B0%B0%ED%8F%AC%EB%B0%A9%EC%8B%9D)/Untitled%202.png)

war 파일생성

![압축해제 (우리가 생성한 Servlet과 index.html이 들어감)](%5BSpring%20Study%5D%20xx%20%EC%9B%B9%20%EC%84%9C%EB%B2%84%EC%99%80%20%EC%84%9C%EB%B8%94%EB%A6%BF%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88(WAR%20%EB%B0%B0%ED%8F%AC%EB%B0%A9%EC%8B%9D)/Untitled%203.png)

압축해제 (우리가 생성한 Servlet과 index.html이 들어감)

### 톰캣 사용(war 파일 배포)

![war파일을 /webapp 경로에 넣은이후 톰캣실행](%5BSpring%20Study%5D%20xx%20%EC%9B%B9%20%EC%84%9C%EB%B2%84%EC%99%80%20%EC%84%9C%EB%B8%94%EB%A6%BF%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88(WAR%20%EB%B0%B0%ED%8F%AC%EB%B0%A9%EC%8B%9D)/Untitled%204.png)

war파일을 /webapp 경로에 넣은이후 톰캣실행

![실행하면 자동으로 압축해제 함](%5BSpring%20Study%5D%20xx%20%EC%9B%B9%20%EC%84%9C%EB%B2%84%EC%99%80%20%EC%84%9C%EB%B8%94%EB%A6%BF%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88(WAR%20%EB%B0%B0%ED%8F%AC%EB%B0%A9%EC%8B%9D)/Untitled%205.png)

실행하면 자동으로 압축해제 함

![살행결과](%5BSpring%20Study%5D%20xx%20%EC%9B%B9%20%EC%84%9C%EB%B2%84%EC%99%80%20%EC%84%9C%EB%B8%94%EB%A6%BF%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88(WAR%20%EB%B0%B0%ED%8F%AC%EB%B0%A9%EC%8B%9D)/Untitled%206.png)

살행결과

![인텔리제이에 톰캣 연결(톰캣을 인텔리제이에서 실행함)](%5BSpring%20Study%5D%20xx%20%EC%9B%B9%20%EC%84%9C%EB%B2%84%EC%99%80%20%EC%84%9C%EB%B8%94%EB%A6%BF%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88(WAR%20%EB%B0%B0%ED%8F%AC%EB%B0%A9%EC%8B%9D)/Untitled%207.png)

인텔리제이에 톰캣 연결(톰캣을 인텔리제이에서 실행함)

</aside>

## ServletContainerInitializer, @HandlesTypes()

<aside>
✍️ **NOTE**

> ***WAS는 실행하는 시점에 필요한 초기화 작업이 존재한다!***
> 

![대표적으로 서블릿 컨테이너 초기화, 애플리케이션 초기화가 존재한다.](%5BSpring%20Study%5D%20xx%20%EC%9B%B9%20%EC%84%9C%EB%B2%84%EC%99%80%20%EC%84%9C%EB%B8%94%EB%A6%BF%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88(WAR%20%EB%B0%B0%ED%8F%AC%EB%B0%A9%EC%8B%9D)/Untitled%208.png)

대표적으로 서블릿 컨테이너 초기화, 애플리케이션 초기화가 존재한다.

### 서블릿 컨테이너 초기화

```java
public class MyContainerInitV1 implements ServletContainerInitializer {

    @Override
    public void onStartup(Set<Class<?>> c, ServletContext ctx) throws ServletException {
        System.out.println("MyContainerInitV1.onStartup");
        System.out.println("c = " + c);
        System.out.println("ctx = " + ctx);
    }
}
```

```java
hello.container.MyContainerInitV1
hello.container.MyContainerInitV2
```

### 애플리케이션 초기화

```java
@HandlesTypes(AppInit.class)
public class MyContainerInitV2 implements ServletContainerInitializer {

    @Override
    public void onStartup(Set<Class<?>> c, ServletContext ctx) throws ServletException {
        System.out.println("MyContainerInitV2.onStartup");
        System.out.println("c = " + c);
        System.out.println("ctx = " + ctx);

        for (Class<?> appInitClass : c) {
            try {

                // new AppInitV1Servlet()과 동일한 코드
                AppInit appInit = (AppInit) appInitClass.getDeclaredConstructor().newInstance();
                appInit.onStartUp(ctx);
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        }
    }
}
```

```java
public class AppInitV1Servlet implements AppInit {

    @Override
    public void onStartUp(ServletContext servletContext) {

        // 순수 서블릿 코드 등록
        ServletRegistration.Dynamic helloServlet = servletContext.addServlet("helloServlet", new HelloServlet());
        helloServlet.addMapping("/heelo-servlet");
    }
}
```

1. @HandlersTypes 애노테이션에 애플리케이션 초기화 인터페이스 지정
2. 서블릿 컨테이너 초기화는 파라미터로 넘어오는 c에 초기화 인터페이스 구현체들을 모두 찾아서 전달한다.
3. appInitClass.getDeclaredConstructor().newInstance()
    - 리플렉션을 통해 객체를 생성한다.
4. appInit.onStartUp(ctx)
    - 애플리케이션 초기화 코드를 직접 실행하면서 서블릿 컨테이너 정보가 담긴 ctx도 전달
</aside>

## 스프링 컨테이너 등록

<aside>
✍️ **NOTE**

> ***앞서 사용한 서블릿 컨테이너/애플리케이션 초기화를 응용해 WAS와 스프링을 통합한다!***
> 

```java
// Spring MVC 추가
implementation 'org.springframework:spring-webmvc:6.0.4'
```

![다음 과정이 필요하다
1. 스프링 컨테이너 만들기
2. 스프링 MVC컨트롤러 빈 등록
3. 디스패쳐 서블릿 서블릿컨테이너에 등록](%5BSpring%20Study%5D%20xx%20%EC%9B%B9%20%EC%84%9C%EB%B2%84%EC%99%80%20%EC%84%9C%EB%B8%94%EB%A6%BF%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88(WAR%20%EB%B0%B0%ED%8F%AC%EB%B0%A9%EC%8B%9D)/Untitled%209.png)

다음 과정이 필요하다
1. 스프링 컨테이너 만들기
2. 스프링 MVC컨트롤러 빈 등록
3. 디스패쳐 서블릿 서블릿컨테이너에 등록

```java
public class AppInitV2Spring implements AppInit {

    @Override
    public void onStartUp(ServletContext servletContext) {
        System.out.println("AppInitV2Spring.onStartUp");

        // 스프링 컨테이너 생성
        AnnotationConfigWebApplicationContext appContext = new AnnotationConfigWebApplicationContext();
        appContext.register(HelloConfig.class);

        // 스프링 MVC 디스패쳐 서블릿 생성,  스프링 컨테이너 연결
        DispatcherServlet dispatcher = new DispatcherServlet(appContext);

        // 디스패쳐 서블릿을 서블릿 컨테이너에 등록 
        ServletRegistration.Dynamic servlet = servletContext.addServlet("dispatcherV2", dispatcher);

        // /spring/* 요청이 디스패쳐 서블릿을 통함
        servlet.addMapping("/spring/*");
    }
}
```

![최종 그림](%5BSpring%20Study%5D%20xx%20%EC%9B%B9%20%EC%84%9C%EB%B2%84%EC%99%80%20%EC%84%9C%EB%B8%94%EB%A6%BF%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88(WAR%20%EB%B0%B0%ED%8F%AC%EB%B0%A9%EC%8B%9D)/Untitled%2010.png)

최종 그림

![디스패쳐 서블릿이 정상적으로 동작함!](%5BSpring%20Study%5D%20xx%20%EC%9B%B9%20%EC%84%9C%EB%B2%84%EC%99%80%20%EC%84%9C%EB%B8%94%EB%A6%BF%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88(WAR%20%EB%B0%B0%ED%8F%AC%EB%B0%A9%EC%8B%9D)/Untitled%2011.png)

디스패쳐 서블릿이 정상적으로 동작함!

</aside>

## WebApplicationInitializer

<aside>
✍️ **NOTE**

> ***기존의 초기화 방식을 직접 구현하지 않고 간단한 인터페이스 구현만으로 스프링이 지원한다!***
> 

```java
public class AppInitV3Spring implements WebApplicationInitializer {

    @Override
    public void onStartup(ServletContext servletContext) throws ServletException {
        System.out.println("AppInitV3Spring.onStartUp");

        // 스프링 컨테이너 생성
        AnnotationConfigWebApplicationContext appContext = new AnnotationConfigWebApplicationContext();
        appContext.register(HelloConfig.class);

        // 스프링 MVC 디스패쳐 서블릿 생성,  스프링 컨테이너 연결
        DispatcherServlet dispatcher = new DispatcherServlet(appContext);

        // 디스패쳐 서블릿을 서블릿 컨테이너에 등록
        ServletRegistration.Dynamic servlet = servletContext.addServlet("dispatcherV3", dispatcher);

        // 모든 요청이 디스패쳐 서블릿을 통함
        servlet.addMapping("/");
    }
}
```

![초록색 영역은 이미 스프링이 만들어서 제공하는 영역](%5BSpring%20Study%5D%20xx%20%EC%9B%B9%20%EC%84%9C%EB%B2%84%EC%99%80%20%EC%84%9C%EB%B8%94%EB%A6%BF%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88(WAR%20%EB%B0%B0%ED%8F%AC%EB%B0%A9%EC%8B%9D)/Untitled%2012.png)

초록색 영역은 이미 스프링이 만들어서 제공하는 영역

![경로의 우선순위는 구체적인 것이 먼저 실행된다.](%5BSpring%20Study%5D%20xx%20%EC%9B%B9%20%EC%84%9C%EB%B2%84%EC%99%80%20%EC%84%9C%EB%B8%94%EB%A6%BF%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88(WAR%20%EB%B0%B0%ED%8F%AC%EB%B0%A9%EC%8B%9D)/Untitled%2013.png)

경로의 우선순위는 구체적인 것이 먼저 실행된다.

- 일반적으로는 스프링 컨테이너 하나, 디스패쳐 서블릿도 하나만 만든다.
- 디스패쳐 서블릿의 경로 매핑도 /로 해서 하나로 진행한다.

</aside>