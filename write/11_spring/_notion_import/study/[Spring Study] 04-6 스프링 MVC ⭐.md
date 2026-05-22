# [Spring Study] 04-6. 스프링 MVC ⭐

주제: Spring Study
연관 노트: 아키텍쳐 & 대규모 시스템 설계] 06. 소프트웨어 아키텍쳐 패턴 (https://www.notion.so/06-a8475f529f8c403383558ea8b1068718?pvs=21)

- 참고
    
    [spring-mvc-1/04 스프링 MVC.md at main · backend-sprout/spring-mvc-1](https://github.com/backend-sprout/spring-mvc-1/blob/main/05%20%EC%8A%A4%ED%94%84%EB%A7%81%20MVC%20-%20%EA%B5%AC%EC%A1%B0%20%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0/04%20%EC%8A%A4%ED%94%84%EB%A7%81%20MVC.md)
    

# **스프링 MVC - 시작하기**

---

## **@RequestMapping**

<aside>
✍️ **NOTE**

> ***스프링 MVC에서 가장 높은 `HandlerMapping`과 `HandlerAdapter` 방식
(실무에서 가장 많이 사용하는 방식이다)***
> 
> - `RequestMappingHandlerMapping`
> - `RequestMappingHandlerAdapter`
- **@Controller**
    - 스프링이 자동으로 스프링 빈으로 등록한다
    (내부에 @Component 어노테이션이 있어서 컴포넌트 스캔의 대상이됨)
- **@RequestMapping**
    - 요청 정보를 매핑한다
    - 해당 URL이 호출되면 이 메서드가 호출된다
    - 어노테이션을 기반으로 동작하기 때문에, 메서드의 이름은 임의로 지어도됨
- **ModelAndView**
    - 모델과 뷰 정보를 담아서 반환한다.

- **클래스**에 `@Controller`를 붙이고 **메서드/클래스 레벨**에 `@RequestMapping`을 선언하면 된다. 
( 이 과정에서 더 이상 `FrontController`는 생성하지 않아도 됨 )
</aside>

## **RequestMappingHandlerMapping**

<aside>
✍️ **NOTE**

```java
@Override
protected boolean isHandler(Class<?> beanType) {
    return (AnnotatedElementUtils.hasAnnotation(beanType, **Controller.class**) || 
            AnnotatedElementUtils.hasAnnotation(beanType, **RequestMapping.class**));
}
```

- `RequestMappiongHandleMapping`의 `isHander()`를 보면 재밌는점을 알 수 있는데 스프링 빈 중에서 `@RequestMapping` 또는 `@Controller`가 붙은 클래스의 매핑 정보를 인식한다.

- **방법1 ( 일반적인 방법 )**
    
    ```java
    @Component   
    @RequestMapping
    public class SpringMemberFormControllerV1 {  
    
        @RequestMapping("/springmvc/v1/members/new-form")
        public ModelAndView process() {
            return new ModelAndView("new-form");
        }
        
    }
    ```
    
- **방법2 (Component안쓰고 Bean에 직접 등록)**
    
    ```java
    @RequestMapping
    public class SpringMemberFormControllerV1 {  
    
        @RequestMapping("/springmvc/v1/members/new-form")
        public ModelAndView process() {
            return new ModelAndView("new-form");
        }
        
    }
    ```
    
    ```java
    @Configuration
    public class TestConfiguration {
        
        @Bean
        TestController testController() {
            return new TestController();
        }
        
    }
    ```
    
- **Best Pratice ( @Controller로 편-안하게 사용하기)**
    
    ```java
    @Controller
    public class SpringMemberFormControllerV1 {   
    
        @RequestMapping("/springmvc/v1/members/new-form")
        public ModelAndView process() {
            return new ModelAndView("new-form");
        }
        
    }
    ```
    
    ```java
    @Controller
    public class SpringMemberSaveControllerV1 {
        
        private MemberRepository memberRepository = MemberRepository.getInstance();
        
        @RequestMapping("/springmvc/v1/members/save")
        public ModelAndView process(HttpServletRequest request, HttpServletResponse response) {
            String username = request.getParameter("username");
            int age = Integer.parseInt(request.getParameter("age"));
            Member member = new Member(username, age);
            
            memberRepository.save(member);
            
            ModelAndView mv = new ModelAndView("save-result");
            mv.addObject("member", member);
            return mv;
        }
    }
    ```
    
    - 스프링이 제공하는 ModelAndView를 사용하면 쉽게 데이터 추가가능
</aside>

# **스프링 MVC - 컨트롤러 통합**

---

<aside>
💡 **NOTE**

- `RequestHandlingMapping`은 `@RequestMapping`을 기준으로만 동작을 한다
- `@RequestMapping`은 주로 메서드 단위에 적용되는데 이를 **하나의 컨트롤러 클래스에서 여러 `@RequestMapping` 메서드를 가질 수 있다.**
- **코드 (Class레벨에서 RequestMapping을 해서 메서드에 공통으로 적용시킴)**
    
    ```java
    @Controller
    @RequestMapping("/springmvc/v2/members")
    public class SpringMemberControllerV2 {
        private MemberRepository memberRepository = MemberRepository.getInstance();
    
        @RequestMapping("/new-form")
        public ModelAndView newForm() {
            return new ModelAndView("new-form");
        }
    
        @RequestMapping("/save")
        public ModelAndView save(HttpServletRequest request, HttpServletResponse
                response) {
            String username = request.getParameter("username");
            int age = Integer.parseInt(request.getParameter("age"));
            Member member = new Member(username, age);
            memberRepository.save(member);
            ModelAndView mav = new ModelAndView("save-result");
            mav.addObject("member", member);
            return mav;
        }
    
        @RequestMapping
        public ModelAndView members() {
            List<Member> members = memberRepository.findAll();
            ModelAndView mav = new ModelAndView("members");
            mav.addObject("members", members);
            return mav;
        }
    }
    ```
    

**조합 결과**

- 클래스 레벨 `@RequestMapping("/springmvc/v2/members")`
    - `@RequestMapping("/new-form")` → `/springmvc/v2/members/new-form`
    - `@RequestMapping("/save")` → `/springmvc/v2/members/save`
    - `@RequestMapping` → `/springmvc/v2/members`
</aside>

# **스프링 MVC - 실용적인 방식**

---

<aside>
💡 **NOTE**

> ***스프링 MVC는 개발자가 편리하게 개발할 수 있도록 많은 편의 기능을 제공한다
특히 핸들러에 정의된 메서드 파라미터 및 반환값을 유연하게 설정할 수 있도록 해준다***
> 
> - 참고로 스프링 MVC의 핸들러란 `@RequestMapping`이 정의된 메서드를 의미한다 (Servlet에서는 Controller 그자체)
</aside>

## 실용적인 방식 코드적용

<aside>
✍️ **NOTE**

```java
@Controller
@RequestMapping("/springmvc/v2/members")
public class SpringMemberControllerV2 {
    private MemberRepository memberRepository = MemberRepository.getInstance();

    @RequestMapping("/new-form")
    public ModelAndView newForm() {
        return new ModelAndView("new-form");
    }

    @RequestMapping("/save")
    public ModelAndView save(HttpServletRequest request, HttpServletResponse
            response) {
        String username = request.getParameter("username");
        int age = Integer.parseInt(request.getParameter("age"));
        Member member = new Member(username, age);
        memberRepository.save(member);
        ModelAndView mav = new ModelAndView("save-result");
        mav.addObject("member", member);
        return mav;
    }

    @RequestMapping
    public ModelAndView members() {
        List<Member> members = memberRepository.findAll();
        ModelAndView mav = new ModelAndView("members");
        mav.addObject("members", members);
        return mav;
    }
}
```

```java
@Controller
@RequestMapping("/springmvc/v3/members")
public class SpringMemberControllerV3 {
    
    private MemberRepository memberRepository = MemberRepository.getInstance();
    
    @GetMapping("/new-form")
    public String newForm() {
        return "new-form";
    }
    
    @PostMapping("/save")
    public String save(
            @RequestParam("username") String username,
            @RequestParam("age") int age, Model model) {
    
       Member member = new Member(username, age);
       memberRepository.save(member);
       model.addAttribute("member", member);
       return "save-result";
    }
    
    @GetMapping
    public String members(Model model) {
        List<Member> members = memberRepository.findAll();
        model.addAttribute("members", members);
        return "members";
    }
}
```

- **ModelAndView**
    - 스프링이 제공해주는 `ModelAndView` 객체를 파라미터로 받거나 반환값으로 설정할 수 있다.
- **Model**
    - 스프링이 제공해주는 Model 객체를 파라미터로 받을 수 있다.
    - 주로 `addAttribute("key", value);`를 통해 값을 request 범위로 저장한다.
- **View**
    - 뷰 인터페이스를 구현한 구현체를 파라미터로 받거나 반환값으로 설정할 수 있다.
- **View 이름을 String 타입으로 직접 반환**
    - 뷰의 논리 이름을 String 타입으로 직접 반환할 수 있다.**`@RequestParam` 사용**
    - HTTP 요청 파라미터를 **`@RequestParam`**으로 받을 수 있다.
    - `@RequestParam("username")`은 `request.getParameter("username")`와 거의 같은 코드다.
    - 물론, **GET 쿼리 파라미터**, **POST Form 방식**을 모두 지원한다.
- **@RequestMapping -> @GetMapping, @PostMapping**
    - **@RequestMapping은 URL만 매칭하는 것이 아니라, HTTP Method도 함께 구분할 수 있다.**
        - `@RequestMapping(value = "/new-form", method = RequestMethod.GET)`
    - 스프링 4.3부터 `@GetMapping` , `@PostMapping`으로 더 편리하게 사용할 수 있다( `Get`, `Post`, `Put`, `Delete`, `Patch` 모두 애노테이션이 준비되어 있다 )
</aside>