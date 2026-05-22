# [Spring Study] 04. 스프링 MVC 흐름

주제: Spring Study
연관 노트: [Spring Study] 08-2. 필터와 인터셉터 (https://www.notion.so/Spring-Study-08-2-df2108b46b1c429e83a9c668b85a925f?pvs=21)

- 참고
    
    [Spring Framework 실행순서](https://javannspring.tistory.com/231)
    
    [[Spring] Spring Framework 구동순서 완벽정리](https://yoo-hyeok.tistory.com/139)
    
    [Spring Framework 실행순서](https://seongeun-it.tistory.com/238)
    
    [Sori](https://gowoonsori.com/spring/architecture/)
    

# Spring 실행순서

---

<aside>
💡 **NOTE**

![Untitled](%5BSpring%20Study%5D%2004%20%EC%8A%A4%ED%94%84%EB%A7%81%20MVC%20%ED%9D%90%EB%A6%84/Untitled.png)

![Untitled](%5BSpring%20Study%5D%2004%20%EC%8A%A4%ED%94%84%EB%A7%81%20MVC%20%ED%9D%90%EB%A6%84/Untitled%201.png)

![Untitled](%5BSpring%20Study%5D%2004%20%EC%8A%A4%ED%94%84%EB%A7%81%20MVC%20%ED%9D%90%EB%A6%84/Untitled%202.png)

- 처음 설정로딩 (1~4)
- 요청 들어와서 DispatcherServlet생성됨 (5)
- 이후는 우리가 아는 MVC 동작
</aside>

## 1. Loading - 웹 어플리케이션이 실행되면 Tomcat(WAS)에 의해 web.xml 로딩

<aside>
✍️ **NOTE**

- `ServeltContainer` (ex : 톰캣서버 ) → URL 확인 → 요청을 처리할 `Setvlet`을 찾아 실행
- web.xml : 각종 설정을 위한 파일
</aside>

## 2. Create - web.xml에 등록되어 있는 ContextLoadaerListener 생성.

<aside>
✍️ **NOTE**

- **Servlet Container가 파일을 읽어서 구동될 때, `ContextLoaderLIstener`가 자동으로 메모리에 생성된다 (Pre-Loading)**
- `ContextLoaderListener 클래스`는 `ApplicationContext (root-context)`를 생성하는 역할을 수행한다
- `ContextLoaderListener 클래스`는 `Servlet`의 생명주기를 관리해줌
    - Servlet을 사용하는 시점에 `ServletContext`에 `ApllicationContext` **등록**
    - `Servlet`이 종됼되는 시점에 `ApplicationContext`를 **삭제**
    
- **web.xml 코드**
    
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <web-app version="2.5" xmlns="http://java.sun.com/xml/ns/javaee"
    	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    	xsi:schemaLocation="http://java.sun.com/xml/ns/javaee https://java.sun.com/xml/ns/javaee/web-app_2_5.xsd">
    
    	<!-- The definition of the Root Spring Container shared by all Servlets and Filters -->
    	<context-param>
    		<param-name>contextConfigLocation</param-name>
    		<param-value>/WEB-INF/spring/root-context.xml</param-value>
    	</context-param>
    	
    	<!-- Creates the Spring Container shared by all Servlets and Filters -->
    	<listener>
    		**<listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>**
    	</listener>
    
    	<!-- 여기부터는 요청들어올 떄 실행됨 -->
    	<!-- POST 방식의 한글 처리 -->
        <filter>
            <filter-name>encodingFilter</filter-name>
            <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
            <init-param>
                <param-name>encoding</param-name>
                <param-value>UTF-8</param-value>
            </init-param>
        </filter>
        
        <filter-mapping>
            <filter-name>encodingFilter</filter-name>
            <url-pattern>/*</url-pattern>
        </filter-mapping>
    	
    	
    	<servlet>
    		<servlet-name>appServlet</servlet-name>
    		<servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    		<init-param>
    			<param-name>contextConfigLocation</param-name>
    			<param-value>/WEB-INF/spring/appServlet/servlet-context.xml</param-value>
    		</init-param>
    		<init-param>
    			<param-name>throwExceptionIfNoHandlerFound</param-name>
    			<param-value>true</param-value>
    		</init-param>
    		<load-on-startup>1</load-on-startup>
    	</servlet>
    		
    	<servlet-mapping>
    		<servlet-name>appServlet</servlet-name>
    		<url-pattern>/</url-pattern>
    	</servlet-mapping>
    
    </web-app>
    ```
    
</aside>

## 3. ContextLoaderListener가 ApplicationContext(root-context.xml)을 로딩

<aside>
✍️ **NOTE**

- `ContextLoaderListener` 객체는 `applicationContext.xml (root-context.xml)` 파일을 로딩하여 스프링 컨테이너를 구동하는데 이를 **Root 컨테이너라고 한다.**
</aside>

## 4. root-context.xml에 등록되어 있는 Spring Container를 구동

<aside>
✍️ **NOTE**

- **root-context.xml에는 주로 view 지원을 제외한 공통 bean을 설정**
    - web과 관련된 bean들은 등록해주지 않음 (ex `Controller`)
    - `service`, `dao`

- **root-context.xml 코드 ( web에 관련된걸 모두 설정, `DispathcerServlet`에 전달됨 )**
    
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
    	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    	xmlns:context="http://www.springframework.org/schema/context"
    	xmlns:aop="http://www.springframework.org/schema/aop"
    	xsi:schemaLocation="http://www.springframework.org/schema/beans https://www.springframework.org/schema/beans/spring-beans.xsd
    		http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-4.3.xsd
    		http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop-4.3.xsd">
    	
    	<!-- Annotation 사용할 수 있는 범위 설정 -->
    	<context:component-scan base-package="com.ssafy.ws"></context:component-scan>
    	
    	<!-- Spring AOP의 ProxyFactoryBean을 자동으로 생성하는 태그 -->
    	<aop:aspectj-autoproxy></aop:aspectj-autoproxy>
    	
    	<!-- 톰켓(WAS)이 가지고 있는 Connection Pool에 접근하기 위한 설정 -->
    	<!-- META-INF의 context에 jdbc/ssafy 존재 -->
    	<bean id="ds" class="org.springframework.jndi.JndiObjectFactoryBean">
    		<property name="jndiName" value="java:comp/env/jdbc/ssafy"></property>
    	</bean>
    </beans>
    ```
    
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <Context>
    	<Resource name="jdbc/ssafy" auth="Container"
    		type="javax.sql.DataSource" maxTotal="100" maxIdle="30"
    		maxWaitMillis="10000" username="ssafy" password="ssafy"
    		driverClassName="com.mysql.cj.jdbc.Driver"
    		url="jdbc:mysql://localhost:3306/ssafyweb?serverTimezone=UTC&amp;useUniCode=yes&amp;characterEncoding=UTF-8" />
    	<WatchedResource>WEB-INF/web.xml</WatchedResource>
    </Context>
    ```
    
</aside>

## 5. 클라이언트로부터 웹 어플리케이션 요청이 오고 Servlet-context 로딩

<aside>
✍️ **NOTE**

- **최초의 클라이언트 요청에 의해 `DispathcerServlet`이 생성됨**
- **DispatcherServlet가 servlet-context.xml 로딩**
    - WEB-INF/confing 폴더의 `s**ervlet-context.xml` 파일을 로딩하여 두번째 스프링 컨테이너를 구동**한다
- **servlet-context.xml**
    - 주로 웹과 관련된것을 로드함 → Controller, VIewResolver ..

- **servlet-context.xml 코드**
    
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <beans:beans xmlns="http://www.springframework.org/schema/mvc"
    	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    	xmlns:beans="http://www.springframework.org/schema/beans"
    	xmlns:context="http://www.springframework.org/schema/context"
    	xsi:schemaLocation="http://www.springframework.org/schema/mvc https://www.springframework.org/schema/mvc/spring-mvc.xsd
    		http://www.springframework.org/schema/beans https://www.springframework.org/schema/beans/spring-beans.xsd
    		http://www.springframework.org/schema/context https://www.springframework.org/schema/context/spring-context.xsd">
    
    	<!-- DispatcherServlet Context: defines this servlet's request-processing infrastructure -->
    	
    	<!-- 어노테이션을 사용한다 -->
    	<annotation-driven />
    
    	<!-- 리소스 사용을 위한 경로자동 변경 -->
    	<resources mapping="/resources/**" location="/resources/" />
    
    	<!-- Resolves views selected for rendering by @Controllers to .jsp resources in the /WEB-INF/views directory -->
    	<beans:bean class="org.springframework.web.servlet.view.InternalResourceViewResolver">
    		<beans:property name="prefix" value="/WEB-INF/views/" />
    		<beans:property name="suffix" value=".jsp" />
    	</beans:bean>
    	
    	<context:component-scan base-package="com.ssafy.ws" />
    
    	
    </beans:beans>
    ```
    
</aside>

## 6. 두번째 Spring Container 구동되며 응답에 맞는 Controller들이 동작

<aside>
✍️ **NOTE**

- FrontController의 MVC동작이 진행됨 → [[Spring Study] 04-4. FrontController V5(Adapter 추가)](https://www.notion.so/Spring-Study-04-4-FrontController-V5-Adapter-1896133bc96a452e90e9a84a6b406594?pvs=21)
</aside>