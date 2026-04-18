# HTTP 서버 구현

---

> HTTP 서버를 소켓으로 직접 구현하면 Spring MVC가 내부에서 하는 일을 이해할 수 있다. 요청 파싱, 라우팅, 응답 생성, 그리고 리플렉션과 애노테이션을 활용한 자동 매핑이 프레임워크의 핵심 원리다.

## 1. HTTP 프로토콜 기초

HTTP는 텍스트 기반 프로토콜이다. 요청과 응답 모두 헤더와 바디로 나뉘며, `\r\n`으로 줄바꿈하고 빈 줄(`\r\n\r\n`)로 헤더와 바디를 구분한다.

HTTP 요청 구조:

```
GET /search?q=hello HTTP/1.1\r\n
Host: localhost:12345\r\n
Connection: keep-alive\r\n
\r\n
```

HTTP 응답 구조:

```
HTTP/1.1 200 OK\r\n
Content-Type: text/html; charset=utf-8\r\n
Content-Length: 20\r\n
\r\n
<h1>Hello World</h1>
```

## 2. 소켓으로 HTTP 서버 구현

`ServerSocket`으로 TCP 연결을 받고, 소켓의 `InputStream`에서 HTTP 요청 텍스트를 읽은 뒤 `OutputStream`에 HTTP 응답 텍스트를 쓰면 된다. 브라우저는 이 텍스트 규약에 따라 응답을 해석한다.

가장 단순한 Hello World 서버:

```java
public class HttpServerV1 {
    private final int port;

    public HttpServerV1(int port) { this.port = port; }

    public void start() throws IOException {
        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("서버 시작 port: " + port);
            while (true) {
                Socket socket = serverSocket.accept();
                process(socket);
            }
        }
    }

    private void process(Socket socket) throws IOException {
        try (socket;
             BufferedReader reader = new BufferedReader(
                 new InputStreamReader(socket.getInputStream(), StandardCharsets.UTF_8));
             PrintWriter writer = new PrintWriter(socket.getOutputStream(), false, StandardCharsets.UTF_8)) {

            // 요청 읽기 (헤더만, 빈 줄까지)
            StringBuilder request = new StringBuilder();
            String line;
            while (!(line = reader.readLine()).isEmpty()) {
                request.append(line).append("\n");
            }

            if (request.toString().contains("/favicon.ico")) return;

            // 응답 생성
            String body = "<h1>Hello World</h1>";
            int length = body.getBytes(StandardCharsets.UTF_8).length;

            writer.print("HTTP/1.1 200 OK\r\n");
            writer.print("Content-Type: text/html; charset=utf-8\r\n");
            writer.print("Content-Length: " + length + "\r\n");
            writer.print("\r\n");
            writer.print(body);
            writer.flush();
        }
    }
}
```

## 3. 요청 파싱: HttpRequest 객체

요청 문자열을 직접 파싱하는 것은 오류가 많다. HTTP 요청을 파싱해 메서드, 경로, 쿼리 파라미터, 헤더를 담는 `HttpRequest` 객체로 구조화하면 처리 코드가 훨씬 명확해진다.

```java
public class HttpRequest {
    private String method;
    private String path;
    private final Map<String, String> queryParameters = new HashMap<>();
    private final Map<String, String> headers = new HashMap<>();

    public HttpRequest(BufferedReader reader) throws IOException {
        parseRequestLine(reader);
        parseHeaders(reader);
    }

    // "GET /search?q=hello HTTP/1.1" 파싱
    private void parseRequestLine(BufferedReader reader) throws IOException {
        String requestLine = reader.readLine();
        if (requestLine == null) throw new IOException("빈 요청");

        String[] parts = requestLine.split(" ");
        method = parts[0];

        String[] pathParts = parts[1].split("\\?");
        path = pathParts[0];

        if (pathParts.length > 1) {
            parseQueryParameters(pathParts[1]);
        }
    }

    private void parseQueryParameters(String queryString) {
        for (String param : queryString.split("&")) {
            String[] kv = param.split("=");
            String key = URLDecoder.decode(kv[0], StandardCharsets.UTF_8);
            String value = kv.length > 1
                ? URLDecoder.decode(kv[1], StandardCharsets.UTF_8)
                : "";
            queryParameters.put(key, value);
        }
    }

    private void parseHeaders(BufferedReader reader) throws IOException {
        String line;
        while (!(line = reader.readLine()).isEmpty()) {
            int colonIdx = line.indexOf(':');
            if (colonIdx > 0) {
                headers.put(
                    line.substring(0, colonIdx).trim()
                    , line.substring(colonIdx + 1).trim()
                );
            }
        }
    }

    public String getMethod() { return method; }
    public String getPath() { return path; }
    public String getParameter(String name) { return queryParameters.get(name); }
    public String getHeader(String name) { return headers.get(name); }
}
```

## 4. 응답 생성: HttpResponse 객체

마찬가지로 응답도 객체로 추상화한다. `HttpResponse`는 상태 코드와 바디를 담고, `flush()` 호출 시 HTTP 응답 텍스트를 소켓에 쓴다.

```java
public class HttpResponse {
    private final PrintWriter writer;
    private int statusCode = 200;
    private String contentType = "text/html; charset=utf-8";
    private final StringBuilder body = new StringBuilder();

    public HttpResponse(PrintWriter writer) { this.writer = writer; }

    public void setStatusCode(int statusCode) { this.statusCode = statusCode; }
    public void writeBody(String content) { body.append(content); }

    public void flush() {
        String bodyStr = body.toString();
        int contentLength = bodyStr.getBytes(StandardCharsets.UTF_8).length;

        writer.print("HTTP/1.1 " + statusCode + " " + phrase(statusCode) + "\r\n");
        writer.print("Content-Type: " + contentType + "\r\n");
        writer.print("Content-Length: " + contentLength + "\r\n");
        writer.print("\r\n");
        writer.print(bodyStr);
        writer.flush();
    }

    private String phrase(int code) {
        return switch (code) {
            case 200 -> "OK";
            case 404 -> "Not Found";
            case 500 -> "Internal Server Error";
            default -> "Unknown";
        };
    }
}
```

## 5. 리플렉션으로 라우팅 자동화

if-else로 경로를 매핑하면 라우트가 늘어날 때마다 핸들러 코드를 수정해야 한다. **리플렉션**을 사용하면 컨트롤러 메서드 이름과 URL 경로를 자동으로 매핑할 수 있다.

```java
// 리플렉션 기반 서블릿: 메서드 이름 = URL 경로
public class ReflectionServlet implements HttpServlet {
    private final List<Object> controllers;

    public ReflectionServlet(List<Object> controllers) {
        this.controllers = controllers;
    }

    @Override
    public void service(HttpRequest request, HttpResponse response) throws IOException {
        String path = request.getPath(); // "/site1"

        for (Object controller : controllers) {
            for (Method method : controller.getClass().getDeclaredMethods()) {
                // 메서드명 "site1" → 경로 "/site1"
                if (path.equals("/" + method.getName())) {
                    invoke(controller, method, request, response);
                    return;
                }
            }
        }
        response.setStatusCode(404);
        response.writeBody("<h1>Not Found</h1>");
    }

    private void invoke(Object controller, Method method
            , HttpRequest request, HttpResponse response) {
        try {
            method.invoke(controller, request, response);
        } catch (IllegalAccessException | InvocationTargetException e) {
            throw new RuntimeException(e);
        }
    }
}
```

이 방식은 메서드 이름과 URL이 항상 일치해야 한다는 제약이 있다. `/` 같은 특수 경로도 처리하지 못한다.

## 6. 애노테이션으로 라우팅 고도화

`@Mapping` 같은 커스텀 애노테이션을 사용하면 메서드 이름과 URL을 분리할 수 있다. 이것이 Spring의 `@RequestMapping`이 동작하는 원리다.

커스텀 애노테이션 정의:

```java
@Retention(RetentionPolicy.RUNTIME) // 런타임에 리플렉션으로 읽을 수 있어야 함
@Target(ElementType.METHOD)
public @interface Mapping {
    String value();
}
```

애노테이션을 사용한 컨트롤러:

```java
public class SiteController {

    @Mapping("/")
    public void home(HttpRequest request, HttpResponse response) {
        response.writeBody("<h1>홈</h1>");
    }

    @Mapping("/site1")
    public void page1(HttpRequest request, HttpResponse response) {
        response.writeBody("<h1>Site 1</h1>");
    }

    @Mapping("/search")
    public void search(HttpRequest request, HttpResponse response) {
        String query = request.getParameter("q");
        response.writeBody("<p>검색어: " + query + "</p>");
    }
}
```

초기화 시 `@Mapping` 애노테이션을 스캔해 경로 → 메서드 맵을 구축한다:

```java
public class AnnotationServlet implements HttpServlet {
    private final Map<String, ControllerMethod> pathMap = new HashMap<>();

    public AnnotationServlet(List<Object> controllers) {
        for (Object controller : controllers) {
            for (Method method : controller.getClass().getDeclaredMethods()) {
                if (method.isAnnotationPresent(Mapping.class)) {
                    String path = method.getAnnotation(Mapping.class).value();
                    pathMap.put(path, new ControllerMethod(controller, method));
                }
            }
        }
    }

    @Override
    public void service(HttpRequest request, HttpResponse response) throws IOException {
        ControllerMethod cm = pathMap.get(request.getPath());
        if (cm == null) {
            response.setStatusCode(404);
            response.writeBody("<h1>Not Found</h1>");
            return;
        }
        cm.invoke(request, response);
    }

    record ControllerMethod(Object controller, Method method) {
        void invoke(HttpRequest request, HttpResponse response) {
            try {
                method.invoke(controller, request, response);
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        }
    }
}
```

이 구조가 Spring MVC의 `DispatcherServlet`이 `@RequestMapping`을 처리하는 방식의 핵심이다. Spring은 여기에 파라미터 바인딩, 인터셉터, 뷰 리졸버 등을 더해 완전한 웹 프레임워크로 발전시킨 것이다.

## 7. WAS와 서블릿 표준

각 회사가 독자적인 HTTP 서버를 만들면서 호환성 문제가 생겼고, Java 진영은 1990년대에 **Servlet** 표준(`jakarta.servlet`)을 도입했다. `HttpServlet`을 상속해 `doGet()`, `doPost()`를 구현하면 Tomcat, Jetty, Undertow 어느 WAS에서도 동일하게 동작한다. 위에서 직접 만든 `HttpServlet` 인터페이스와 `ServletManager`가 이 표준의 최소 모형이다.
