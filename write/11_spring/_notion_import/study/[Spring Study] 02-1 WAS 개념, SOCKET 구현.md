# [Spring Study] 02-1. WAS 개념, SOCKET 구현

주제: Spring Study

- 참고
    
    [[Web] Web Server와 WAS의 차이와 웹 서비스 구조 - Heee's Development Blog](https://gmlwjd9405.github.io/2018/10/27/webserver-vs-was.html)
    
    [[소켓과 웹소켓] 한 번에 정리 (1) | 소켓이란?, 소켓 API의 실행 흐름, 클라이언트 소켓과 서버 소켓](https://velog.io/@rhdmstj17/%EC%86%8C%EC%BC%93%EA%B3%BC-%EC%9B%B9%EC%86%8C%EC%BC%93-%ED%95%9C-%EB%B2%88%EC%97%90-%EC%A0%95%EB%A6%AC-1)
    
    [[JAVA Networking] 소켓(socket) 통신의 기본구조 및 기본개념](https://mainpower4309.tistory.com/25)
    
    [스프링 MVC 1편 - 백엔드 웹 개발 핵심 기술](https://velog.io/@wrjang96/스프링-웹-MVC-1)
    

# WAS **(Web Application Server)**

---

<aside>
💡 **NOTE**

> ***DB 조회나 다양한 로직 처리를 요구하는 동적인 컨텐츠를 제공하기 위해 만들어진 Application Server***
> 

![Web Server → 정적 컨텐츠 담당
Web Container → 동적인 컨텐츠 담당](%5BSpring%20Study%5D%2002-1%20WAS%20%EA%B0%9C%EB%85%90,%20SOCKET%20%EA%B5%AC%ED%98%84/Untitled.png)

Web Server → 정적 컨텐츠 담당
Web Container → 동적인 컨텐츠 담당

- HTTP를 통해 컴퓨터나 장치에 Application을 수행해주는 **미들웨어(소프트웨어 엔진) 이다**
- **웹 컨테이너(Web Container)** 혹은 **서블릿 컨테이너(Servlet Container)**라고 부른다.
- **Application Server**
    - `Servlet`을 통해서 요청메시지를 처리함 ( Request, Response )
        1. **Data get**
        2. **Logic**
        3. **response page** 

### **Web Server vs WAS**

- ***WebServer***
    - 웹 브라우저 클라이언트로부터 **HTTP 요청**을 받아 **정적인 컨텐츠(html, css, Js, 이미지, 영상 등등..)** 등을 제공함
    - WAS를 거치지 않고 바로 데이터 제공, 동적인 컨텐츠 제공을 위한 요청을WAS에게 전달해줌
- ***WAS***
    - Web Server의 기능을 구조적으로 분리하여 처리하고자 만들어짐
    - 주로 DB서버와 같이 수행됨
    - ex) 서블릿, JSP, 스프링 MVC

---

### 📌 참조

- ***구분하는 이유***
    
    ![WAS가 장애가 발생하면 아무것도 못행..](%5BSpring%20Study%5D%2002-1%20WAS%20%EA%B0%9C%EB%85%90,%20SOCKET%20%EA%B5%AC%ED%98%84/Untitled%201.png)
    
    WAS가 장애가 발생하면 아무것도 못행..
    
    - `WAS`가 `WebServer`의 기능도 모두 수행은 가능하지만 단점이 존재한다
    - `WAS`에 장애가 발생했을 시 가용 서버 자체가 없기에 오류 화면 노출도 불가능하며`WAS`에 너무 많은 역할을 담당하게 되기에 서버 과부하가 생긴다.
    - 이러한 이유로 관심사 분리 **웹 애플리케이션 서버 앞에 일반 웹 서버 (프록시 서버)를 놓는 방식을 권장**한다.

- **프록시 서버(관심사의 분리)**
    
    ![Web Server(프록시)를 두어 부하를 줄인다!](%5BSpring%20Study%5D%2002-1%20WAS%20%EA%B0%9C%EB%85%90,%20SOCKET%20%EA%B5%AC%ED%98%84/Untitled%202.png)
    
    Web Server(프록시)를 두어 부하를 줄인다!
    
    - **프록시(웹 서버)**가  정적 리소스를 처리해서 WAS의 부담을 줄여준다!
    
    ![확장면에서도 구분해서 할 수 있다](%5BSpring%20Study%5D%2002-1%20WAS%20%EA%B0%9C%EB%85%90,%20SOCKET%20%EA%B5%AC%ED%98%84/Untitled%203.png)
    
    확장면에서도 구분해서 할 수 있다
    
    - **리소스 관리가 효율적으로 이루어짐**
        - 정적 리소스가 많아진다 → 웹 서버 증설
        - 애플리케이션 리소스가 많아진다 → WAS를 증설
    - **참고로 API만 제공한다면 굳이 웹 서버를 사용할 필요는 없음**
</aside>

# WAS 실습 - SOCKET

---

<aside>
💡 **NOTE**

![서버에서 처리해야 할 작업(순수 서버구현)](%5BSpring%20Study%5D%2002-1%20WAS%20%EA%B0%9C%EB%85%90,%20SOCKET%20%EA%B5%AC%ED%98%84/Untitled%204.png)

서버에서 처리해야 할 작업(순수 서버구현)

- **SOCKET** 이란?
    
    ![Untitled](%5BSpring%20Study%5D%2002-1%20WAS%20%EA%B0%9C%EB%85%90,%20SOCKET%20%EA%B5%AC%ED%98%84/Untitled%205.png)
    
    - 프로세스가 네트워크 세계로 데이터를 내보내거나 혹은 그 세계로부터 데이터를 받기
    위한 실제 창구 역할을 한다
    - 프로토콜, IP 주소, 포트 넘버로 정의된다.
    
    ![Untitled](%5BSpring%20Study%5D%2002-1%20WAS%20%EA%B0%9C%EB%85%90,%20SOCKET%20%EA%B5%AC%ED%98%84/Untitled%206.png)
    
    1. `Client class`를 생성한다
    2. 해당 클래스에 서버의 `ip주소`와 `port번호`를 넣고 출력 스트림으로 넘어간 후 
    `Server Socket`에 접근한다
    3. `Server Socket class`는 `clinet`가 접속을 했는지 확인하는 용도
    4. 접근이 인식되면 서버는 클래스는 `Socket.accpet()`를 실행한다.

![Socket으로 하는거라서 .java 파일 실행하고 주소로 직접 들어가야함](%5BSpring%20Study%5D%2002-1%20WAS%20%EA%B0%9C%EB%85%90,%20SOCKET%20%EA%B5%AC%ED%98%84/Untitled%207.png)

Socket으로 하는거라서 .java 파일 실행하고 주소로 직접 들어가야함

- **Socket 코드**
    
    ```java
    // PORT
    private static final int PORT = 8080;
    
    // 서버 소켓
    ServerSocket serverSocket = null;
    
    // 클라이언트 소켓
    Socket clientSocket= null;
    
    // 소켓 통신에 활용할 노드 스트림
    InputStream is = null;
    OutputStream os = null;
    
    // 소켓 통신에 활용할 보조 스트림
    InputStreamReader isr = null;
    OutputStreamWriter osw = null;
    BufferedReader br = null;
    BufferedWriter bw = null;
    
    // 1. 요청을 받으면 request 객체와 response 객체를 생성
    SsafyRequest request = new SsafyRequest();
    SsafyResponse response = new SsafyResponse();
    ```
    
    ```java
    while (true) {
    			try {
    				// 클라이언트 요청을 받을 서버 소켓 생성
    				**serverSocket = new ServerSocket(PORT);**
    				System.out.println("SSAFY Web Server is running ... " + PORT);
    
    				// 클라이언트 요청 대기
    				**clientSocket = serverSocket.accept();**
    				System.out.println("Client is accepted ...");
    
    				// 데이터 주고받기 위해 노드 스트림과 보조 스트림 객체 생성
    				// 최종적으로 br, bw를 사용
    				is = **clientSocket**.getInputStream();
    				os = **clientSocket**.getOutputStream();
    				isr = new InputStreamReader(is);
    				osw = new OutputStreamWriter(os);
    				br = new BufferedReader(isr);
    				bw = new BufferedWriter(osw);
    
    				// 클라이언트로부터 요청 받기
    				String line = br.readLine();
    				if (line != null) {
    					// 요청받은 내용 분석
    					System.out.println(line);
    
    					// 헤더 정보를 저장할 자료구조
    					Map<String, String> headers = new HashMap<>();
    					
    					// 첫 줄을 제외한 나머지 요청 헤더 정보 받아오기
    					String headerLine = null;
    					System.out.println("=== Header ===");
    					while ((headerLine = br.readLine()).length() != 0) {
    						System.out.println(headerLine);
    						String[] splitHeaderLine = headerLine.split(":");
    						String name = splitHeaderLine[0].trim();
    						String value = splitHeaderLine[1].trim();
    						
    						headers.put(name, value);
    					}
    					
    					// 헤더 정보를 request 객체에 담기
    					request.setHeaders(headers);
    					if ("GET".equals(method)) {
    							// ...
    					}
    					else if ("POST".equals(method)) {
    							// ...
    			}
    			catch (IOException e) {
    				e.printStackTrace();
    
    			}
    			finally {
    				try {
    					if (bw != null) {
    						bw.flush();
    						bw.close();
    					}
    					if (br != null) {
    						br.close();
    					}
    					if (clientSocket != null) {
    						clientSocket.close();
    					}
    					if (serverSocket != null) {
    						serverSocket.close();
    					}
    				}
    				catch (IOException e) {
    					e.printStackTrace();
    				}
    			}
    		}
    	}
    }
    ```
    
- **Response , Request 코드**
    
    ```java
    public class SsafyResponse {
    	
    	private String msg;
    	
    	public void print(String msg) {
    		this.msg = msg;
    	}
    	
    	public String getMsg() {
    		return msg;
    	}
    }
    ```
    
    ```java
    public class SsafyRequest {
    	
    	private Map<String, String> headers;
    	private Map<String, String> parameters;
    
    	public Map<String, String> getParameters() {
    		return parameters;
    	}
    
    	public void setParameters(Map<String, String> parameters) {
    		this.parameters = parameters;
    	}
    	
    	public String getParameter(String parameterName) {
    		return parameters.get(parameterName);
    	}
    
    	public void setHeaders(Map<String, String> headers) {
    		this.headers = headers;
    	}
    	
    	public Map<String, String> getHeaders() {
    		return headers;
    	}
    	
    	public String getHeaders(String name) {
    		return headers.get(name);
    	}
    }
    ```
    
- **Clinet 요청받기 코드**
    
    ```java
    // 클라이언트로부터 요청 받기
    String line = br.readLine();
    if (line != null) {
    	// 요청받은 내용 분석
    
    	// GET /index.html HTTP/1.1
    	System.out.println(line);
    
    	String[] split = line.split(" ");
    	String method = split[0];
    	String uri = split[1];
    	String protocol = split[2];
    ```
    
- **QueryString 파싱 코드**
    
    ```java
    String[] uriSplit = uri.split("\\?");
    Map<String, String> parameters = new HashMap<>();
    if (uriSplit != null && uriSplit.length > 1 && uriSplit[1] != null) {
    	String[] keyValues = uriSplit[1].split("\\&");
    	for (String keyValue : keyValues) {
    		String[] item = keyValue.split("=");
    		parameters.put(URLDecoder.decode(item[0]), URLDecoder.decode(item[1]));
    	}
    }
    // 2. 서블릿으로 넘길 요청 정보들을 request 객체에 저장
    request.setParameters(parameters);
    ```
    
</aside>

## SOCKET - GET

<aside>
✍️ **NOTE**

![Header](%5BSpring%20Study%5D%2002-1%20WAS%20%EA%B0%9C%EB%85%90,%20SOCKET%20%EA%B5%AC%ED%98%84/Untitled%208.png)

Header

![Response](%5BSpring%20Study%5D%2002-1%20WAS%20%EA%B0%9C%EB%85%90,%20SOCKET%20%EA%B5%AC%ED%98%84/Untitled%209.png)

Response

- **GET - (처음 index.html 불러옴) 코드**
    
    ```java
    if ("GET".equals(method)) { 
    			// ...
    	
    			// 서버에 있는 정적파일을 클라이언트로 응답	보내기
    			// index.html으로 들어감
    			// 서버에 있는 정적파일을 클라이언트로 응답	보내기
    			File file = new File("static" + URLDecoder.decode(uri));
    			if (file.exists()) {
    				// 응답 헤더 작성
    				// 파일은 byte로 동작해야하므로 os로 진행
    				os.write("HTTP/1.1 200 OK\r\n".getBytes());
    				os.write("Server:SSAFY Web Server\r\n".getBytes());
    				
    				// 확장자 얻어내기
    				int dot = uri.lastIndexOf(".");
    				String ext = uri.substring(dot+1);
    				
    				switch (ext) {
    				case "html":
    					os.write("Content-Type:text/html; charset=UTF-8\r\n".getBytes()); 
    					break;
    				case "jpg":
    				case "jpeg":
    					os.write("Content-Type:image/jpeg\r\n".getBytes());
    					break;
    				}
    				
    				os.write("\r\n".getBytes()); // 헤더 영역과 Payload 영역을 구분하기 위한 한줄공백
    				
    				FileInputStream fis = new FileInputStream(file);
    				byte[] buffer = new byte[2048];
    				while(fis.available() > 0) {
    					int length = fis.read(buffer);
    					os.write(buffer, 0, length);
    				}
    				fis.close();
    		
    			}
    			else {
    				bw.write("HTTP/1.1 404 Not Found\r\n");
    				bw.write("Content-Type:text/html; charset=UTF-8\r\n");
    				bw.write("\r\n");  // 헤더와 Payload 구분하기 위한 줄바꿈
    				bw.write("<h1>" + uri + "는 존재하지 않습니다.</h1>");
    			}
    		}
    	}
    ```
    

![Untitled](%5BSpring%20Study%5D%2002-1%20WAS%20%EA%B0%9C%EB%85%90,%20SOCKET%20%EA%B5%AC%ED%98%84/Untitled%2010.png)

![Header](%5BSpring%20Study%5D%2002-1%20WAS%20%EA%B0%9C%EB%85%90,%20SOCKET%20%EA%B5%AC%ED%98%84/Untitled%2011.png)

Header

![Untitled](%5BSpring%20Study%5D%2002-1%20WAS%20%EA%B0%9C%EB%85%90,%20SOCKET%20%EA%B5%AC%ED%98%84/Untitled%2012.png)

- **GET - (/list 게시판 목록 가져오기) 코드**
    
    ```java
    if ("GET".equals(method)) {
    			// Application 서버에서 처리하는 부분이지만 편의상 여기서 처리
    			case "/list":
    					BoardServlet boardServlet = new BoardServlet();
    					boardServlet.doGet(request, response);
    
    					// 1. 응답 헤더 작성
    					bw.write("HTTP/1.1 200 OK\r\n");
    					bw.write("Server:SSAFY Web Server\r\n");
    					bw.write("Content-Type:text/html; charset=UTF-8\r\n");
    					bw.write("\r\n");
    
    					// 2. 응답 내용(Payload) 작성
    					bw.write(response.getMsg());
    					break;
    		}
    }
    else {
    				bw.write("HTTP/1.1 404 Not Found\r\n");
    				bw.write("Content-Type:text/html; charset=UTF-8\r\n");
    				bw.write("\r\n");  // 헤더와 Payload 구분하기 위한 줄바꿈
    				bw.write("<h1>" + uri + "는 존재하지 않습니다.</h1>");
    			}
    		}
    	}
    ```
    
</aside>

## SOCKET - POST

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20Study%5D%2002-1%20WAS%20%EA%B0%9C%EB%85%90,%20SOCKET%20%EA%B5%AC%ED%98%84/Untitled%2013.png)

![header](%5BSpring%20Study%5D%2002-1%20WAS%20%EA%B0%9C%EB%85%90,%20SOCKET%20%EA%B5%AC%ED%98%84/Untitled%2014.png)

header

![payload](%5BSpring%20Study%5D%2002-1%20WAS%20%EA%B0%9C%EB%85%90,%20SOCKET%20%EA%B5%AC%ED%98%84/Untitled%2015.png)

payload

![payload](%5BSpring%20Study%5D%2002-1%20WAS%20%EA%B0%9C%EB%85%90,%20SOCKET%20%EA%B5%AC%ED%98%84/Untitled%2016.png)

payload

- **POST - (글 생성) 코드**
    - **index.html에서 글 등록 이벤트 발생**
    
    ```java
    else if ("POST".equals(method)) {
    		// 헤더 다음 줄부터 나오는 Payload 내용 가져오기
    		StringBuilder payload = new StringBuilder();
    
    		// payload의 내용을 읽어옴
    		while (br.ready()) {
    			payload.append((char) br.read());
    		}
    
    		// payload의 속성값을 담을 MAP
    		Map<String, String> parameters = new HashMap<>();
    
    		String[] keyValues = payload.toString().split("\\&");
    		for (String keyValue : keyValues) {
    			String[] item = keyValue.split("=");
    			parameters.put(URLDecoder.decode(item[0]), URLDecoder.decode(item[1]));
    		}
    		
    		request.setParameters(parameters);
    
    		switch (uri) {
    		case "/regist":
    			BoardRegistServlet servlet = new BoardRegistServlet();
    			servlet.doPost(request, response);
    
    			// 1. 응답 헤더 작성
    			bw.write("HTTP/1.1 200 OK\r\n");
    			bw.write("Server:SSAFY Web Server\r\n");
    			bw.write("Content-Type:text/html; charset=UTF-8\r\n");
    			bw.write("\r\n");
    
    			// 2. 응답 내용(Payload) 작성
    			bw.write(response.getMsg());
    			break;
    		}
    
    ```
    
</aside>