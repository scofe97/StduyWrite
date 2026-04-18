# HTTP 서버 구현: Deep Investigation
> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. 미니 HTTP 서버 구현이 Spring MVC 이해에 도움이 되는 이유는 무엇인가?

### 왜 이 질문이 중요한가
Spring MVC를 사용하면서 `@RequestMapping`, `DispatcherServlet`, `HandlerMapping`, `HandlerAdapter`의 관계를 추상적으로만 이해하는 경우가 많다. 소켓 위에서 직접 HTTP를 파싱하고 라우팅을 구현해보면 Spring이 해결하는 문제가 무엇인지 구체적으로 보인다. 면접에서 "Spring MVC의 동작 원리"를 물을 때 소켓 레벨부터 설명할 수 있으면 깊이가 달라진다.

### 답변

미니 HTTP 서버를 직접 구현하면 Spring MVC의 각 컴포넌트가 왜 존재하는지 필요에서부터 이해하게 된다.

**Step 1: 소켓에서 HTTP 요청 파싱**

```java
// HTTP/1.1 요청 형식
// GET /users/123 HTTP/1.1\r\n
// Host: localhost:8080\r\n
// \r\n

BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
String requestLine = reader.readLine();  // "GET /users/123 HTTP/1.1"
String[] parts = requestLine.split(" ");
String method = parts[0];   // GET
String path = parts[1];     // /users/123
String version = parts[2];  // HTTP/1.1

// 헤더 파싱
Map<String, String> headers = new HashMap<>();
String line;
while (!(line = reader.readLine()).isEmpty()) {
    int colon = line.indexOf(':');
    headers.put(line.substring(0, colon).trim(), line.substring(colon + 1).trim());
}
```

이 파싱 코드를 직접 작성하면 Spring의 `HttpServletRequest`가 왜 `getMethod()`, `getRequestURI()`, `getHeader()`를 제공하는지, 그리고 Servlet 컨테이너(Tomcat)가 이 파싱을 대신 해준다는 것을 체감한다.

**Step 2: 라우팅 구현**

```java
// 직접 구현한 라우터
Map<String, Map<String, Handler>> routes = new HashMap<>();
routes.computeIfAbsent("GET", k -> new HashMap<>())
      .put("/users/{id}", (req, res) -> getUserById(req, res));

// Spring의 HandlerMapping이 정확히 이 역할
// PathVariableMethodArgumentResolver가 {id} → @PathVariable 매핑을 처리
```

직접 라우팅 테이블을 구현하면서 느끼는 불편함(경로 패턴 매칭, 와일드카드, 우선순위)이 Spring의 `AntPathMatcher`, `PathPatternParser`가 존재하는 이유다.

**Spring MVC와의 대응 관계**:

| 미니 서버 코드 | Spring MVC 컴포넌트 | 역할 |
|--------------|-------------------|------|
| 소켓 accept | Tomcat Connector | TCP 연결 수락 |
| HTTP 파싱 | Tomcat Http11Processor | 요청 파싱 |
| 라우팅 테이블 | HandlerMapping | URL → 핸들러 매핑 |
| Handler 호출 | HandlerAdapter | 메서드 호출 규약 통일 |
| 응답 직렬화 | MessageConverter | 객체 → HTTP 응답 변환 |

---

## Q2. 리플렉션 기반 라우팅의 성능 비용과 Spring의 최적화 방식은?

### 왜 이 질문이 중요한가
Spring MVC는 `@RequestMapping` 메서드를 리플렉션으로 호출한다. "리플렉션은 느리다"는 말을 들어봤지만 실제로 얼마나 느리고, Spring은 이를 어떻게 완화하는지 알아야 한다. 성능 병목을 분석할 때 리플렉션 호출이 원인인지 판단할 수 있어야 하고, Java 21+ MethodHandle 기반 최적화의 의미도 이해할 수 있다.

### 답변

**리플렉션 비용의 실체**: `Method.invoke()`는 내부적으로 접근 검사, 인자 박싱/언박싱, 네이티브 메서드 호출 등을 수반한다. JMH 측정 기준으로 직접 메서드 호출 대비 10~50배 느릴 수 있다. 단, 절대 시간은 수십 나노초 수준이므로 요청당 1회 호출이라면 전체 레이턴시에서 차지하는 비율은 무시할 수준이다.

```java
// 리플렉션 기반 라우팅 (미니 서버)
Method handler = controller.getClass().getMethod("getUser", HttpRequest.class);
handler.setAccessible(true);  // 접근 제어 우회
Object result = handler.invoke(controller, request);

// 성능 개선: MethodHandle (Java 7+)
MethodHandles.Lookup lookup = MethodHandles.lookup();
MethodHandle mh = lookup.findVirtual(Controller.class, "getUser",
    MethodType.methodType(Response.class, HttpRequest.class));
// MethodHandle은 JIT가 직접 호출로 최적화 가능
```

**Spring의 최적화 방식**: Spring은 시작 시 `@RequestMapping` 메서드를 분석해 `HandlerMethod` 객체로 캐싱한다. 요청마다 리플렉션으로 메서드를 찾는 것이 아니라, 이미 캐싱된 `Method` 객체를 재사용한다. `Method.setAccessible(true)`를 한 번만 호출하면 이후 호출에서 접근 검사가 생략된다.

```
Spring MVC 요청 처리에서 리플렉션 비용 비율 (일반적 REST API 기준):
- DB 쿼리/네트워크 I/O: 70~90%
- JSON 직렬화/역직렬화: 5~15%
- 리플렉션 호출: < 1%
```

Spring 6.x(Spring Boot 3.x)에서는 GraalVM Native Image 지원을 위해 AOT 처리로 리플렉션을 사전 생성된 코드로 대체하는 방향으로 발전하고 있다. `spring-aot-maven-plugin`이 컴파일 타임에 리플렉션 코드를 직접 호출 코드로 치환해, 네이티브 이미지에서 리플렉션 비용이 완전히 제거된다.
