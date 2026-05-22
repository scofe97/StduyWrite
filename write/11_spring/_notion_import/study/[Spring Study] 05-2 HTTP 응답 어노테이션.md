# [Spring Study] 05-2. HTTP 응답 어노테이션

주제: Spring Study

- 참고
    
    [spring-mvc-1/10 HTTP 응답 - 정적 리소스, 뷰 템플릿.md at main · backend-sprout/spring-mvc-1](https://github.com/backend-sprout/spring-mvc-1/blob/main/06%20%EC%8A%A4%ED%94%84%EB%A7%81%20MVC%20-%20%EA%B8%B0%EB%B3%B8%EA%B8%B0%EB%8A%A5/10%20HTTP%20%EC%9D%91%EB%8B%B5%20-%20%EC%A0%95%EC%A0%81%20%EB%A6%AC%EC%86%8C%EC%8A%A4%2C%20%EB%B7%B0%20%ED%85%9C%ED%94%8C%EB%A6%BF.md)
    
    [spring-mvc-1/11 HTTP 응답 - HTTP API, 메시지 바디에 직접 입력.md at main · backend-sprout/spring-mvc-1](https://github.com/backend-sprout/spring-mvc-1/blob/main/06%20%EC%8A%A4%ED%94%84%EB%A7%81%20MVC%20-%20%EA%B8%B0%EB%B3%B8%EA%B8%B0%EB%8A%A5/11%20HTTP%20%EC%9D%91%EB%8B%B5%20-%20HTTP%20API%2C%20%EB%A9%94%EC%8B%9C%EC%A7%80%20%EB%B0%94%EB%94%94%EC%97%90%20%EC%A7%81%EC%A0%91%20%EC%9E%85%EB%A0%A5.md)
    
    [ResponseEntity란 - 개념, 구조, 사용법, 사용하는 이유](https://thalals.tistory.com/268)
    

# **HTTP 응답 - 정적 리소스, 뷰 템플릿**

---

<aside>
💡 **NOTE**

> ***스프링(서버)에서 응답 데이터를 만드는 방법은 크게 3가지입니다.***
> 

### **정적 리소스 제공**

정적 리소스는 변경 없이 그대로 제공되는 파일들, 예를 들어 HTML, CSS, JavaScript 파일 등을 말합니다. 스프링 부트는 이러한 정적 파일들을 자동으로 처리할 수 있는 기능을 내장하고 있습니다.

- 스프링 부투는 기본적으로 `src/main/resources` 아래의 `static`, `public` 폴더에 정적 리소스를 서비스합니다.
- **정적 리소스 반환**
    - `src/main/resources/static` 경로에 파일이 있다면, 해당 파일은 정적 리소스로 반환됩니다. 예를 들어, `src/main/resources/static/basic/hello-form.html`을 입력하면 `hello-form.html`가 바로 반환됩니다.
    - 위에서 사용한 경로는 컨트롤러를 거치지 않고 직접 파일을 반환합니다.

### **뷰 템플릿 사용**

동적 웹 페이지를 생성할 때는 뷰 템플릿 엔진을 사용합니다. 스프링 부트는 Thymeleaf, Freemarker, JSP 등 여러 종류의 템플릿 엔진을 지원합니다.

- **HTTP 메시지 사용**
    - HTTP API를 제공하는 경우에는 HTML이 아니라 데이터를 전달해야 하므로
    HTTP 메시지 바디에 JSON 같은 형식으로 데이터를 실어 보낸다.

```xml
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <p th:text="${data}">empty</p>
</body>
</html>
```

```java
@Controller
public class ResponseViewController {

    @RequestMapping("/response-view-v1")
    public ModelAndView responseViewV1(){
        ModelAndView mav = new ModelAndView("response/hello")
                .addObject("data", "hello!");

        return mav;
    }
    
    @RequestMapping("/response-view-v2")
    public String responseViewV2(Model model){
        model.addAttribute("data", "hello");
        return "response/hello";
    }

    @RequestMapping("/response/hello")
    public void responseViewV3(Model model){
        model.addAttribute("data", "hello");
    }
}
```

### **HTTP 메시지 사용**

REST API와 같은 HTTP API를 구현할 때는 HTML이 아닌 JSON,XML을 반환해야 하며 HTTP 메시지 바디에 직접 응답 데이터를 출력할 수 있습니다.

![반환 흐름도](%5BSpring%20Study%5D%2005-2%20HTTP%20%EC%9D%91%EB%8B%B5%20%EC%96%B4%EB%85%B8%ED%85%8C%EC%9D%B4%EC%85%98/Untitled.png)

반환 흐름도

- HTTP 메시지를 사용하는 반환에는 아래에서 좀 더 구체적으로 다뤄보겠습니다.
</aside>

## **HttpServletResponse**

<aside>
✍️ **NOTE**

> `*HttpServletResponse` 객체를 사용하여 HTTP 메시지 바디에 'ok' 응답 메시지를 전달합니다.*
> 

```java
@Slf4j
@RestController
public class ResponseBodyController {
 
     @GetMapping("/response-body-string-v1")
     public void responseBodyV1(HttpServletResponse response) throws IOException {
         response.getWriter().write("ok");
     }
}
```

</aside>

## **@ResponseBody**

<aside>
✍️ **NOTE**

> `*@ResponseBody`를 사용하여 HTTP 메시지 컨버터를 통해 HTTP 메시지를 직접 입력할 수 있습니다.*
> 

```java
@Slf4j
@RestController
public class ResponseBodyController {
 
     **@ResponseBody**
     @GetMapping("/response-body-string-v3")
     public String responseBodyV3() {
         return "ok";
     }
}
```

</aside>

## **ResponseEntity**

<aside>
✍️ **NOTE**

> `*ResponseEntity`는 HTTP 응답의 상태 코드, 헤더 및 바디를 포함할 수 있습니다*
> 

```java
@Slf4j
@RestController
public class ResponseBodyController {

    // 1. 직접 객체 생성
    @GetMapping("/response-body-json-v1")
    public ResponseEntity<HelloData> responseBodyJsonV1() {
        HelloData helloData = new HelloData();
        helloData.setUsername("userA");
        helloData.setAge(20);
        return new ResponseEntity<>(helloData, HttpStatus.OK);
    }

    // 2. 응답코드 어노테이션 사용해서 반환
    @ResponseStatus(HttpStatus.OK)
    @ResponseBody
    @GetMapping("/response-body-json-v2")
    public HelloData responseBodyJsonV2() {
        HelloData helloData = new HelloData();
        helloData.setUsername("userA");
        helloData.setAge(20);
        return helloData;
    }

		// 3. builder 사용
    @GetMapping("/api/users")
    public ResponseEntity<HelloData> getUser() {
        HelloData helloData = new HelloData();
        helloData.setUsername("userB");
        helloData.setAge(25);

        // ResponseEntity 빌더를 사용하여 객체를 구성
        return ResponseEntity.ok()
                .header("Custom-Header", "value")
                .body(helloData);
    }
}
```

</aside>