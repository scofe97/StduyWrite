# [Spring Study] 09-99. AOP 세부내용

주제: Spring Study

- 참고
    
    [14. 스프링부트 MVC - Spring AOP 설정](https://linked2ev.github.io/gitlog/2019/09/22/springboot-mvc-14-%EC%8A%A4%ED%94%84%EB%A7%81%EB%B6%80%ED%8A%B8-MVC-Spring-AOP-%EC%84%A4%EC%A0%95/)
    
    [Spring AOP](https://kha0213.github.io/spring/spring-aop/)
    
    [https://www.youtube.com/watch?v=ax4PfMaaFdY](https://www.youtube.com/watch?v=ax4PfMaaFdY)
    
    [Spring AOP 스프링이 해줄건데 너가 왜 어려워 해? Spring boot에서 aop logging 사용법 제일 쉽게 알려드립니다!](https://jeong-pro.tistory.com/171)
    

# 내용

---

## **AOP(Aspect Oriented Programming)**

---

<aside>
✍️ **NOTE**

> ***관점 지향 프로그래밍 ( Aspect Oriented Programming )***
> 

![KakaoTalk_20221018_180318895.png](%5BSpring%20Study%5D%2009-99%20AOP%20%EC%84%B8%EB%B6%80%EB%82%B4%EC%9A%A9/KakaoTalk_20221018_180318895.png)

- 어떤 로직을 기준으로 **핵심적인 관점**, **부가적인 관점**으로 나눠보고 그 관점을 기준으로 각각
모듈화 하겠다는 의미
    - **핵심적인 관점** : 개발자가 적용하고자 하는 핵심 비즈니스 로직
    - **부가적인 관점** : 핵심 로직을 수행하기 위해 필요한 DB연결(JDBC), 로깅, 파일 입출력 등
- **AOP는 프록시 패턴을 통해 구현된다**
    - 프록시(Proxy) : Target을 감싸서 요청을 대신 받아주는 Wrapping 오브젝트이다
    - Advice가 적용되었을 때 만들어짐
- 대표적으로 **Spring AOP**와 **AspectJ**가 존재한다.
</aside>

### AOP - Apsect(관점)

<aside>
✍️ **NOTE**

![하나의 회사가 있다고 가정하자, 회사에는 부서가 존재하고 각 부서에는 팀장과 팀원이 존재한다](%5BSpring%20Study%5D%2009-99%20AOP%20%EC%84%B8%EB%B6%80%EB%82%B4%EC%9A%A9/Untitled.png)

하나의 회사가 있다고 가정하자, 회사에는 부서가 존재하고 각 부서에는 팀장과 팀원이 존재한다

![Untitled](%5BSpring%20Study%5D%2009-99%20AOP%20%EC%84%B8%EB%B6%80%EB%82%B4%EC%9A%A9/Untitled%201.png)

- 일할 때 모든 직원이 필요하지는 않다
    - 부서장 회의, 신규 사업회의 등 주제와 같은 인원들만 필요함
- 이와 같은 주제를 **프로그래밍에서는 관점(Aspect)**라고 부른다.
</aside>

### AOP - Container , Bean

<aside>
✍️ **NOTE**

![Group 37.png](%5BSpring%20Study%5D%2009-99%20AOP%20%EC%84%B8%EB%B6%80%EB%82%B4%EC%9A%A9/Group_37.png)

- **Container**
    - 관점에 따라 필요한 직원들이 존재하는 회사
- **Bean**
    - 회사에 다니는 직원들은 **객체(Objct), Beans**라고 한다
</aside>

### AOP - 적용 예시, 용어

<aside>
✍️ **NOTE**

![어느날 부터 개발팀 사람들의 지각이 많아졌고, 개발팀 전원은 출퇴근시 지문인증을하고 급여에 반영하기로 했다](%5BSpring%20Study%5D%2009-99%20AOP%20%EC%84%B8%EB%B6%80%EB%82%B4%EC%9A%A9/Untitled%202.png)

어느날 부터 개발팀 사람들의 지각이 많아졌고, 개발팀 전원은 출퇴근시 지문인증을하고 급여에 반영하기로 했다

![야근하는 특정 인원들에게 택시비를 지급하는 경우](%5BSpring%20Study%5D%2009-99%20AOP%20%EC%84%B8%EB%B6%80%EB%82%B4%EC%9A%A9/Untitled%203.png)

야근하는 특정 인원들에게 택시비를 지급하는 경우

- **이렇게 적용된 추가 작업은 언제든지 해제할 수 있으며, 해제하면 원래대로 돌아간다.**
- **AOP 용어**
    - `Aspect`
        - `Advice`를 가진 클래스
    - `Advice`
        - 간섭에 사용할 코드를 가진 메소드
        - `Aspect`가 **무엇을 언제 할 지를 정의한다** (Before, After 등.. )
    - `Target`
        - `Advice`를 받을 대상 (핵심이 기능이 담긴 클래스)
    - `Joinpoint`
        - `Advice`를 적용할 수 있는 곳을 `JoinPoint`라고 한다
        - 즉 애플리케이션 실행에 `Aspect`를 끼워 넣을 수 있는 지점을 말한다
            - **메서드**, 필드, 객체, 생성자 등등…
    - `Pointcut`
        - **`T**arget`과 `JoinPoint`를 특정하기 위한 식 (실제 `Advice`가 적용될 시점)
        - `Aspect`가 어디서 `JoinPoint`를 할 지를 말한다.
    - `Weaving`
        - `Target`객체에 `Asepct`를 실제로 적용하는 절차
        - `Advice`와 `Target`이 결합되어서 프록시 객체를 만드는 과정

---

- **[참고]**
    - `Pointcut` 실제 적용
        
        ![Untitled](%5BSpring%20Study%5D%2009-99%20AOP%20%EC%84%B8%EB%B6%80%EB%82%B4%EC%9A%A9/Untitled%204.png)
        
        ```java
        // pointCut 적용 식
        @Before(value = "execution(* com.ssafy.board.model..Board*.*(..))")
        	// execution(실행) *(접근 제한자, *이므로 모두에 적용)
        	// [패키지 명] ..(앞의 패키지명을 포함한 모든 패키지를 선택한다)
        	// Board*.*(Board~.~ 로 시작하는 파일(클래스)을 모두 찾는다) 
        	// (..) 파라미터도 제한이 없음  
        ```
        
</aside>

### AOP - 시점에 따른 Advice 구분

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20Study%5D%2009-99%20AOP%20%EC%84%B8%EB%B6%80%EB%82%B4%EC%9A%A9/Untitled%205.png)

![Untitled](%5BSpring%20Study%5D%2009-99%20AOP%20%EC%84%B8%EB%B6%80%EB%82%B4%EC%9A%A9/Untitled%206.png)

![Untitled](%5BSpring%20Study%5D%2009-99%20AOP%20%EC%84%B8%EB%B6%80%EB%82%B4%EC%9A%A9/Untitled%207.png)

- **AOP 시점에 따른 코드**
    
    ```java
    @Component // Bean 등록
    @Aspect // 공통 관심 코드가 들어있는 클래스라는 의미로 spring에게 알려줌
    public class LogginAspect {
    	
    	// logger 생성
    	private Logger logger = LoggerFactory.getLogger(LogginAspect.class);
    	
    	
    	@**Before**(value = "execution(* com.ssafy.board.model..Board*.*(..))")
    	public void login(JoinPoint joinPoint) {
    		logger.debug("before 호출 메서드 : {} ", joinPoint.getSignature());
    		logger.debug("메서드 선언부 : {} 전달 파라미터 : {}", joinPoint.getSignature(), Arrays.toString(joinPoint.getArgs()));
    	}
    	
    	
    	@**Around**(value = "execution(* com.ssafy.board.model..Board*.*(..))")
    	public Object executionTime(ProceedingJoinPoint joinPoint) throws Throwable {
    		logger.debug("around 호출 메서드 : {}", joinPoint.getSignature());
    		
    		StopWatch stopWatch = new StopWatch();
    		stopWatch.start();
    		
    		Object proceed = joinPoint.proceed(); // 각 원래의 메서드 실행
    		stopWatch.stop();
    		
    		logger.debug("요약 : {}", stopWatch.shortSummary());
    		logger.debug("수행시간: {}", stopWatch.getTotalTimeMillis());
    		logger.debug("예쁘게 출력 : {}", stopWatch.prettyPrint());
    		
    		return proceed;
    	}
    	
    	// returning 이름 무조건 일치시켜야함
    	@**AfterReturning**(value ="execution(* com.ssafy.board.list..Board*.*(..))", returning = "obj")
    	public void afterReturningMethod(JoinPoint joinPoint, Object obj) {
    		logger.debug("afterReturning 호출 메서드: {}", joinPoint.getSignature());
    		logger.debug("return 값: {}",obj );
    	}
    	
    	
    	@**AfterThrowing**(value ="execution(* com.ssafy.board.model..Board*.list*(..))", throwing = "exception")
    	public void afterThrowingMethod(JoinPoint joinPoint, Exception exception) {
    		logger.debug("afterThrowing 호출 메서드 : {}", joinPoint.getSignature());
    		logger.debug("exception : {}",exception);
    	}
    	
    	@**After**(value = "execution(* com.ssafy.board.model..Board*.list*(..))")
    	public void afterMethod(JoinPoint joinPoint) {
    		logger.debug("after 호출 메서드 : {}", joinPoint.getSignature());
    	}
    }
    ```
    
</aside>