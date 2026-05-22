# [Spring Study] 05-1. HTTP 요청 어노테이션

주제: Spring Study

- 참고
    
    [spring-mvc-1/05 HTTP 요청 파라미터 - 쿼리 파라미터, HTML Form.md at main · backend-sprout/spring-mvc-1](https://github.com/backend-sprout/spring-mvc-1/blob/main/06%20%EC%8A%A4%ED%94%84%EB%A7%81%20MVC%20-%20%EA%B8%B0%EB%B3%B8%EA%B8%B0%EB%8A%A5/05%20HTTP%20%EC%9A%94%EC%B2%AD%20%ED%8C%8C%EB%9D%BC%EB%AF%B8%ED%84%B0%20-%20%EC%BF%BC%EB%A6%AC%20%ED%8C%8C%EB%9D%BC%EB%AF%B8%ED%84%B0%2C%20HTML%20Form.md)
    
    [spring-mvc-1/08 HTTP 요청 메시지 - 단순 텍스트.md at main · backend-sprout/spring-mvc-1](https://github.com/backend-sprout/spring-mvc-1/blob/main/06%20%EC%8A%A4%ED%94%84%EB%A7%81%20MVC%20-%20%EA%B8%B0%EB%B3%B8%EA%B8%B0%EB%8A%A5/08%20%20HTTP%20%EC%9A%94%EC%B2%AD%20%EB%A9%94%EC%8B%9C%EC%A7%80%20-%20%EB%8B%A8%EC%88%9C%20%ED%85%8D%EC%8A%A4%ED%8A%B8.md)
    
    [spring-mvc-1/09 HTTP 요청 메시지 - JSON.md at main · backend-sprout/spring-mvc-1](https://github.com/backend-sprout/spring-mvc-1/blob/main/06%20%EC%8A%A4%ED%94%84%EB%A7%81%20MVC%20-%20%EA%B8%B0%EB%B3%B8%EA%B8%B0%EB%8A%A5/09%20HTTP%20%EC%9A%94%EC%B2%AD%20%EB%A9%94%EC%8B%9C%EC%A7%80%20-%20JSON.md)
    

# **HTTP 요청 메소드 어노테이션**

---

## **@Controller, @RestController**

<aside>
✍️ **NOTE**

> ***스프링이 자동으로 스프링 Bean으로 등록해주며, Controllr의 기능을한다!***
> 

```java
@Controller // Controller 동작
public class MemberController {}

@RestController // 반환값으로 View가 아닌, HTTP 메시지바디에 입력
								// @ResponseBody + @Controller
public class MemberController {}
```

</aside>

## **@RequestMapping**

<aside>
✍️ **NOTE**

> ***클라이언트 요청에 정보를 어떤 Controller가 처리할지를 맵핑하기 위한 어노테이션이다!***
> 

```java
@RequestMapping("/members")
public class MemberController {}
```

- 대부분의 속성들은 배열[] 형태로 제공되며, 이를 통해 다중 설정이 가능합니다 `{"/hello-basic", "/hello-go"}`
- URL의 끝에 /가 붙어도, /를 생략한 URL로 매핑해줍니다. `/hello-basic == /hello-basic/`
</aside>

## **PathVariable(경로 변수) 사용**

<aside>
✍️ **NOTE**

> *PathVariable은 경로의 일부를 변수로 사용할 수 있습니다.*
> 

```java
@GetMapping("/mapping/{userId}")
public String mappingPath(@PathVariable("userId") String data) {
    log.info("mappingPath userId={}", data);
    return "ok";
}

// 경로 변수와 변수가 이름이 동일하면 생략가능
@GetMapping("/mapping/{userId}")
public String mappingPath(@PathVariable String userId) {
    log.info("mappingPath userId={}", data);
    return "ok";
}

// 다중으로 사용 가능
@GetMapping("/mapping/users/{userId}/orders/{orderId}")
public String mappingPath(@PathVariable String userId, @PathVariable Long orderId) {
    log.info("mappingPath userId={}, orderId={}", userId, orderId);
    return "ok";
}
```

</aside>

## **HTTP 메서드(Get, Post, Put, Delete, Patch)**

<aside>
✍️ **NOTE**

```java
@RestController
@RequestMapping("/mapping/users")
public class MappingClassController {

     /**
     * GET /mapping/users - 유저 리스트 조회
     */
     @GetMapping
     public String users() {
         return "get users";
     }
     
     /**
     * POST /mapping/users - 유저 생성
     */
     @PostMapping
     public String addUser() {
         return "post user";
     }
     
     /**
     * GET /mapping/users/{userId} - 유저 세부조회
     */
     @GetMapping("/{userId}")
     public String findUser(@PathVariable String userId) {
         return "get userId=" + userId;
     }
     
     /**
     * PATCH /mapping/users/{userId} - 유저 수정
     */
     @PatchMapping("/{userId}")
     public String updateUser(@PathVariable String userId) {
         return "update userId=" + userId;
     }
     /**
     * DELETE /mapping/users/{userId} - 유저 삭제
     */
     @DeleteMapping("/{userId}")
     public String deleteUser(@PathVariable String userId) {
        return "delete userId=" + userId;
    }
}
```

</aside>

## **특정 조건 매핑(params, headers, consumes, produces)**

<aside>
✍️ **NOTE**

```java
// params에 mode=debug가 있어야 호출된다.
@GetMapping(value = "/mapping-header", params = "mode=debug")
public String mappingHeader() {
    log.info("mappingHeader");
    return "ok";
}

// header에 mode=debug가 있어야 호출된다.
@GetMapping(value = "/mapping-header", headers = "mode=debug")
public String mappingHeader() {
    log.info("mappingHeader");
    return "ok";
}
```

```java
// consumes = Content-Type 헤더을 제한합니다.
// 충족되지 않으면 415 코드를 반환한다.
@PostMapping(value = "/mapping-consume", consumes = "application/json")
public String mappingConsumes() {
    log.info("mappingConsumes");
    return "ok";
}

// produce = Accept을 제한합니다.
// Accept헤더가 이를 수용하지 않으면 406 에러를 반환합니다.
@GetMapping(value = "/mapping-produce", produces = "text/html")
public String mappingHeader() {
    log.info("mappingHeader");
    return "ok";
}
```

</aside>

# **HTTP 요청 파라미터 어노테이션**

---

## **@RequestParam**

<aside>
✍️ **Note**

> `*@RequestParam`은 요청 파라미터를 전달할 때 사용됩니다.*
> 

```java
// http://localhost:8080/request-param-v2?username=hello&age=20
@ResponseBody
@RequestMapping("/request-param-v2")
public String requestParamV2(
        @RequestParam("username") String username,
        @RequestParam("age") int age) {

    log.info("username={}, age={}", username, age);
    return "ok";
}

// 변수명이 돌일하면 (name="xxx") 이름 생략이 가능하다.
@ResponseBody
@RequestMapping("/request-param-v3")
public String requestParamV3(
        @RequestParam String username,
        @RequestParam int age) {

    log.info("username={}, age={}", username, age);
    return "ok";
}

// 변수명이 동일하고 기본타입이면 @RequestParam도 생략이 가능하다. (기본 컨버터 지원)
@ResponseBody
@RequestMapping("/request-param-v4")
public String requestParamV4(String username, int age) {
    log.info("username={}, age={}", username, age);
    return "ok";
}
```

```java
// required: 필수값을 설정할 수 있다. (없을시 400에러)
@ResponseBody
@RequestMapping("/request-param-required")
public String requestParamRequired(
        @RequestParam(required = true) String username,
        @RequestParam(required = false) int age) {

    log.info("username={}, age={}", username, age);
    return "ok";
}

// defaultValue: 파라미터에 값이 없는 경우 기본 값을 적용한다.
@ResponseBody
@RequestMapping("/request-param-default")
public String requestParamDefault(
        @RequestParam(required = true, defaultValue = "guest") String username,
        @RequestParam(required = false, defaultValue = "-1") int age) {

    log.info("username={}, age={}", username, age);
    return "ok";
}

// Map 조회: 파라미터의 값이 여러개인 경우 map으로 받을 수 있다.
@ResponseBody
@RequestMapping("/request-param-map")
public String requestParamMap(
        @RequestParam Map<String, Object> paramMap){

    log.info("username={}, age={}", paramMap.get("username"), paramMap.get("age"));
    return "ok";
}
```

</aside>

## **@ModelAttribute**

<aside>
✍️ **NOTE**

> `*@ModelAttribute`는 HTTP 요청 파라미터를 객체에 바인딩 하는데 사용할 수 있습니다.*
> 

```java
// @ModelAttribute: 스프링MVC가 자동으로 요청 파라미터에 알맞게 객체생성
// 단 주입을 기반으로 하기에 생성자와 setter가 필수이다.
@ResponseBody
@RequestMapping("/model-attribute-v1")
public String modelAttributeV1(@ModelAttribute HelloData helloData) {
    log.info("username={}, age={}", helloData.getUsername(),
    helloData.getAge());
    return "ok";
}
```

- 작동 과정
    - 요청 파라미터의 이름으로 HelloData 객체의 프로퍼티를 찾습니다.
    - 해당 프로퍼티의 **생성자 또는 setter를 호출하여 파라미터의 값을 입력(바인딩)합니다.**
- 바인딩 오류
    - `age=abc`와 같이 숫자가 들어가야 하는 곳에 문자를 입력하면 `BindException`이 발생합니다.
    - 이런 **바인딩 오류**를 처리하는 방법은 검증 부분에서 다룹니다.
    - 요청 파라미터와 다르게 HTTP 메시지 바디를 통해 데이터가 직접 넘어오는 경우 `@RequestParam`, `@ModelAttribute`를 사용할 수 없다.
</aside>

# **HTTP 요청 파라미터 지원타입**

---

## HttpServletRequest

<aside>
✍️ **NOTE**

> `*HttpServletRequest`의 입력 스트림으로부터 JSON 데이터를 직접 읽어 사용할 수 있습니다.*
> 

```java
@PostMapping("/request-body-json-v1")
public void requestBodyJsonV1(HttpServletRequest request, 
															HttpServletResponse response) throws IOException {
		
		// 객체 변환							
    ServletInputStream inputStream = request.getInputStream();
    String messageBody = StreamUtils.copyToString(inputStream, StandardCharsets.UTF_8);

    log.info("messageBody={}", messageBody);

		// Jackson의 ObjetMapper를 사용해 역직렬화
    HelloData helloData = objectMapper.readValue(messageBody, HelloData.class);
    log.info("username={}, age={}", helloData.getUsername(), helloData.getAge());

    response.getWriter().write("ok");
}
```

</aside>

## **HttpEntity**

<aside>
✍️ **NOTE**

> `*HttpEntity`를 사용하면 HTTP 요청의 헤더와 본문을 래핑해서 받을 수 있습니다.*
> 

```java
@ResponseBody
@PostMapping("/request-body-json-v4")
public String requestBodyJsonV4(HttpEntity<HelloData> data) throws IOException {
    HelloData helloData = data.getBody();
    log.info("messageBody={}", helloData);
    log.info("username={}, age={}", helloData.getUsername(), helloData.getAge());

    return  "ok";
}
```

</aside>

## **@RequestBody 객체 변환**

<aside>
✍️ **NOTE**

> `*@RequestBody`을 사용하면 HTTP 요청 본문을 객체로 변환할 수 있습니다. 이 때 스프링은 `httpMessageConverter`중 `MappingJackson2HttpMessageConvertes`를 사용하여 자동으로 JSON데이터를 자바 객체로 변환합니다.*
> 

```java
@ResponseBody
@PostMapping("/request-body-json-v3")
public String requestBodyJsonV3(@RequestBody HelloData helloData) throws IOException {
    log.info("messageBody={}", helloData);
    log.info("username={}, age={}", helloData.getUsername(), helloData.getAge());
    return  "ok";
}
```

- 여기서 HelloData객체에는 일반적으로 생성자 or setter함수로 객체가 생성되어야 하지만, 2개의 요소가 모두 없더라도 Jackson라이브러리가 리플렉션을 통해 값을 초기화해줍니다.
</aside>