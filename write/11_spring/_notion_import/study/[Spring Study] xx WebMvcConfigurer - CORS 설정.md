# [Spring Study] xx. WebMvcConfigurer - CORS 설정

주제: Spring Study
연관 노트: [AWS - SAA] 09-3. S3 보안 (https://www.notion.so/AWS-SAA-09-3-S3-af313943a4734295b3de0974827bffea?pvs=21)

- 참고
    
    [[Spring] 설정 자동화와 설정의 변경, @EnableWebMvc와 WebMvcConfigurer](https://mangkyu.tistory.com/176)
    
    [](https://goodteacher.tistory.com/258)
    

# **Spring에서 제공하는 설정의 자동화와 변경**

---

<aside>
💡 **NOTE**

> `*@Enable`**~ 을 이용한 설정 자동화***
> 

```java
@Configuration
**@EnableWebMvc**
public class WebMvcConfig {

}
```

- Spring 기반의 프로젝트를 구축하려면 `message converter`나 `view resolver`등 설정등을 매번해주어야 했고 이는 상당히 귀찮은 일이다.
- 스프링은 이런 부분들에 대해 최신 전략들을 기반으로 설정을 자동화하는 기능 제공
- 대표적으로 @EnableWebMvc가 대표적인데, 이를 붙이면 웹과 관련된 최신 전략 bean들이 등록된다.
</aside>

## **SpringBoot의 AutoConfiguration(자동 설정)**

<aside>
✍️ **NOTE**

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan(excludeFilters = { @Filter(type = FilterType.CUSTOM, classes = TypeExcludeFilter.class),
		@Filter(type = FilterType.CUSTOM, classes = AutoConfigurationExcludeFilter.class) })
public @interface SpringBootApplication {

    ...

}
```

- 이 어노테이션은 내부에 `@EnableAutoConfiguration`이라는 어노테이션을 갖고 있다.
    - `@EnableAutoConfiguration`은 내부적으로 **`@EnableWebMvc`와 동일한 기능을 사용**하기 때문에 **메시지 컨버터, 뷰 리졸버, 인터셉터 등을 따로 설정해주지 않아도 된다**
    - 스프링 프로젝트만 생성하면 이러한 부분을 자동으로 해줌
</aside>

## **~Configurer 인터페이스을 통한 설정의 변경**

<aside>
✍️ **NOTE**

> *스프링에서는 `@Enable`로 적용되는 인프라 빈에 대해 추가적인 설정을 할 수 있도록 **~Configure로 끝나는 인터페이스(빈 설정자)를 제공**하고 있다*
> 
- 이를 구현할 클래스를 만들어 빈으로 등록하면 `@Enable`전용 어노테이션을 처리하는 단계에서 설정용 빈을 활용해 설정을 마무리한다
- 대표적으로 @**EnableWebMvc의 빈 설정자는 WebMvcConfigure**이며, 이를 구현할 클래스를 만들고 `@Configuration`을 붙여 빈으로 등록해주면 된다.
</aside>

# **@EnableWebMvc와 WebMvcConfigurer**

---

<aside>
💡 **NOTE**

```java
@Configuration
**@EnableAspectJAutoProxy**
@MapperScan(basePackages = { "com.ssafy.**.mapper" })
public class WebMvcConfiguration implements **WebMvcConfigurer** {

	private final List<String> patterns = Arrays.asList("/board/*", "/admin", "/user/list");

	// 인터셉터 생성
	@Autowired
	private ConfirmInterceptor confirmInterceptor;

	private final String uploadFilePath;

	public WebMvcConfiguration(@Value("${file.path.upload-files}") String uploadFilePath) {
		this.uploadFilePath = uploadFilePath;
	}

	@Override
	public void **addCorsMappings**(CorsRegistry registry) {
		registry.addMapping("/**").allowedOrigins("*")
//			.allowedOrigins("http://localhost:8080", "http://localhost:8081")
				.allowedMethods(HttpMethod.GET.name(), HttpMethod.POST.name(), HttpMethod.PUT.name(),
						HttpMethod.DELETE.name(), HttpMethod.HEAD.name(), HttpMethod.OPTIONS.name(),
						HttpMethod.PATCH.name())
//				.allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD")
				.maxAge(1800);
	}

	@Override
	public void **addInterceptors**(InterceptorRegistry registry) {
		registry.addInterceptor(confirmInterceptor).addPathPatterns(patterns);
	}

	@Override
	public void **addResourceHandlers**(ResourceHandlerRegistry registry) {
		registry.addResourceHandler("/upload/file/**").addResourceLocations("file:///" + uploadFilePath + "/")
				.setCachePeriod(3600).resourceChain(true).addResolver(new PathResourceResolver());
	}

}
```

- `WebMvcConfigure`는 다음과 같은 구조를 가지고 있으며, 메소드의 이름은 대부분 add나 configure로 시작하는데, 다음의 의미를 가지고 있다
    - `add~` : 기본 설정이 없는 빈들에 대하여 **새로운 빈 추가**
    - `configure~` : 수정자를 통해 **기존의 설정을 대신하여 등록**
    - `extend~` : **기존의 설정을 이용하여 확장**
- **WebMvcConfigure 구조코드**
    
    ```java
    public interface WebMvcConfigurer {
    
    	default void configurePathMatch(PathMatchConfigurer configurer) {
    	}
    
    	default void configureContentNegotiation(ContentNegotiationConfigurer configurer) {
    	}
    
    	default void configureAsyncSupport(AsyncSupportConfigurer configurer) {
    	}
    
    	default void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer) {
    	}
    
    	default void addFormatters(FormatterRegistry registry) {
    	}
    
    	default void addInterceptors(InterceptorRegistry registry) {
    	}
    
    	default void addResourceHandlers(ResourceHandlerRegistry registry) {
    	}
    
    	default void addCorsMappings(CorsRegistry registry) {
    	}
    
    	default void addViewControllers(ViewControllerRegistry registry) {
    	}
    
    	default void configureViewResolvers(ViewResolverRegistry registry) {
    	}
    
    	default void addArgumentResolvers(List<HandlerMethodArgumentResolver> resolvers) {
    	}
    
    	default void addReturnValueHandlers(List<HandlerMethodReturnValueHandler> handlers) {
    	}
    
    	default void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
    	}
    
    	default void extendMessageConverters(List<HttpMessageConverter<?>> converters) {
    	}
    
    	default void configureHandlerExceptionResolvers(List<HandlerExceptionResolver> resolvers) {
    	}
    
    	default void extendHandlerExceptionResolvers(List<HandlerExceptionResolver> resolvers) {
    	}
    
    	@Nullable
    	default Validator getValidator() {
    		return null;
    	}
    
    	@Nullable
    	default MessageCodesResolver getMessageCodesResolver() {
    		return null;
    	}
    
    }
    ```
    
</aside>

## **WebMvcConfigurer를 통한 설정의 변경 예시**

<aside>
✍️ **NOTE**

```java
@Configuration
public class WebMvcConfig implements WebMvcConfigurer {

    @Override
    public void **extendMessageConverters**(List<HttpMessageConverter<?>> messageConverters) {
        **messageConverters.add(createXmlHttpMessageConverter());**
    }

    private HttpMessageConverter<Object> createXmlHttpMessageConverter() {
        MarshallingHttpMessageConverter xmlConverter = new MarshallingHttpMessageConverter();

        XStreamMarshaller xstreamMarshaller = new XStreamMarshaller();
        xmlConverter.setMarshaller(xstreamMarshaller);
        xmlConverter.setUnmarshaller(xstreamMarshaller);

        return xmlConverter;
    }
    
}
```

- **기존의 메시지 컨버터 확장**
    - `extendMessageConverter` 오버라이딩
- **기존의 메시지 컨버터 모두 비활성하고 새로운 컨버터 추가**
    - `configureMessageConverters` 오버라이딩

---

- **[📌 [참고](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#web.servlet.spring-mvc.auto-configuration)]**
    - `@EnableWebMvc`를 빼주어야 동작이됨!
    - 기본적으로 스프링에서 제공해주는 웹 기능들에 대해 커스터마이징이 필요한 경우, 
    `@EnableWebMvc`**없이** `WebMvcConfigure`**를 구현한 설정 파일만 등록**
</aside>

## **view controller**

<aside>
✍️ **NOTE**

```java
// Controller에 개별적인 handler method로 구현하는 형태
@GetMapping("/login")
public String loginForm(Model model) {
    return "login";
}
    

// MVCConfig에서 View Controller로 처리하는 형태    
public class MVCConfig implements WebMvcConfigurer {
  @Override
  public void addViewControllers(ViewControllerRegistry registry) {
    // /login이라고 요청이 들어오면 login을 viewResolver에게 넘겨줌
    **registry.addViewController("/login").setViewName("login");**
  }
}
```

- 웹 어플리케이션을 만들다 보면 **Controller을 거치지 않고 단순히 페이지만 보여줘도 되는 경우**가 존재한다. 
ex) `get /login`의 경우 단순히 form만 보여주면됨
</aside>

# CORS란?

---

<aside>
💡 **NOTE**

> ***Cross-Origin Resource Sharing, CORS 란 다른 출처의 자원을 공유할 수 있도록 설정하는 권한 체제를 말한다.***
> 

![CORS를 설정하지 않으면, 제대로 리소스 공유를 하지못하고 위와같이 에러 발생](%5BSpring%20Study%5D%20xx%20WebMvcConfigurer%20-%20CORS%20%EC%84%A4%EC%A0%95/Untitled.png)

CORS를 설정하지 않으면, 제대로 리소스 공유를 하지못하고 위와같이 에러 발생

</aside>

## Configuration으로 해결 (**WebMvcConfigurer)**

<aside>
✍️ **NOTE**

```java
@Configuration
public class WebConfig implements **WebMvcConfigurer** {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedOrigins("*")
                .allowedMethods("GET", "POST")
                .maxAge(3000);
	}
}
```

- `addCorsMapping`
    - CORS를 적용할 URL패턴을 정의
- `allowedOrigins`
    - 자원 공유를 허락할 Origin 지정
- `allowedMethods`
    - 허용할 HTTP method를 지정
- `maxAge`
    - 원하는 시간만큼 pre-flight 리퀘스르 캐싱
</aside>

## Annotation 사용하기

<aside>
✍️ **NOTE**

```java
@RestController
@RequestMapping("/somePath")
public class SomeController {

    @CrossOrigin(origins="*")
    @RequestMapping(value = "/{something}",method = RequestMethod.DELETE)
    public ResponseEntity<String> delete(@PathVariable Long reservationNo) throws Exception{
    }

}
```

</aside>