# [Spring Study] 05-3. Converter, Formatter

주제: Spring Study

- 참고
    
    [[Spring MVC] [2] 10. 스프링 타입 컨버터](https://velog.io/@dbsrud11/Spring-MVC-2-10)
    
    [Java Enum 활용하기2 - ConverterFactory](https://wildeveloperetrain.tistory.com/189)
    

# **스프링 타입 컨버터**

---

<aside>
💡 **NOTE**

> *스프링에서는 API를 통해 전달받은 문자열을 숫자로 변환하거나, 숫자를 문자열로 변환해야할 때가 많습니다. 스프링은 이러한 타입변환을 위해 다양한 Converter 구현체를 제공합니다.*
> 

![대표적인 Converter 구현체 (@ResponseBody)](%5BSpring%20Study%5D%2005-3%20Converter,%20Formatter/Untitled.png)

대표적인 Converter 구현체 (@ResponseBody)

```java
@Controller
public class MyController {

    @InitBinder
    public void initBinder(WebDataBinder binder) {
        binder.registerCustomEditor(IpPort.class, new PropertyEditorSupport() {
            @Override
            public void setAsText(String text) throws IllegalArgumentException {
                setValue(new IpPort(text)); // IpPort는 String을 인자로 받는 생성자 필요
            }
        });
    }

    @RequestMapping("/custom")
    public String handleCustomObject(IpPort ipPort) {
        return "viewPage";
    }
}
```

```java
public interface Converter<S, T> {
    T convert(S source);
}
```

```java
@Getter
@EqualsAndHashCode
public class IpPort {
    private String ip;
    private int port;
    
    public IpPort(String ip, int port) {
        this.ip = ip;
        this.port = port;
    }
}
```

```java
public class StringToIpPortConverter implements Converter<String, IpPort> {

    @Override
    public IpPort convert(String source) {
        String[] split = source.split(":");
        String ip = split[0];
        int port = Integer.parseInt(split[1]);

        return new IpPort(ip, port);
    }
}
```

스프링의 Converter구현체의 종류는 다양하지만 대표적인 Converter는 다음과 같습니다.

- 기본 문자처리: `StringHttpMessageConverter`
- 기본 객체처리: `MappingJackson2HttpMessageConverter`
- `@RequestMapping`, `@PathVariable`, `@ModelAttribute`와 같은 어노테이션도 대표적

스프링은 용도에 따라 다양한 방식의 타입 컨버터를 제공합니다.

- `Converter`: 기본 타입 컨버터
- `ConverterFactory`: 전체 클래스 계층 구조가 필요할 때
- `GenericConverter`: 정교한 구현, 대상 필드의 애노테이션 정보 사용 가능
- `ConditionalGenerictConverter`: 특정 조건이 참인 경우에만 실행
</aside>

## ConversionService 활용

<aside>
✍️ **NOTE**

> *스프링의 `ConversionService`는 타입 변환을 체계적으로 관리할 수 있도록 돕는 인터페이스입니다. 이 서비스를 사용해 개별 컨버터들을 효율적으로 관리하고, 쉽게 호출할 수 있습니다.*
> 

`DefaultConversionService`는 2개의 인터페이스를 구현해 컨버터 사용과 등록이 가능하다.

- `ConversionService`: 컨버터 사용에 초점
- `ConversionRegistry`: 컨버터 등록에 초점

```java
@Test
void conversionService() {
		// 1. ConversioService 생성
    DefaultConversionService conversionService = new DefaultConversionService();
    
    // 2. Converter 등록
    conversionService.addConverter(new StringToIpPortConverter());
    conversionService.addConverter(new IpPortToStringConverter());
    
    // 3. 변환 가능여부 확인
    assertThat(conversionService.canConvert(String.class, IpPort.class)).isTrue();
    assertThat(conversionService.canConvert(IpPort.class, String.class)).isTrue();
    
    // 4. 사용
    IpPort ipPort = conversionService.convert("127.0.0.1:8080", IpPort.class);
    assertThat(ipPort).isEqualTo(new IpPort("127.0.0.1", 8080));
    String ipPortString = conversionService.convert(ipPort, String.class);
    assertThat(ipPortString).isEqualTo("127.0.0.1:8080");
}
```

</aside>

## 스프링 컨버터 적용

<aside>
✍️ **NOTE**

> *스프링에서는 `@RequestParam`, `@PathVariable`, `@ModelAttribute`와 같은 애노테이션과 함께 타입변환 기능을 자주 사용합니다.*
> 

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

		// 컨버터 등록
    @Override
    public void addFormatters(FormatterRegistry registry) {
        registry.addConverter(new IpPortToStringConverter());
        registry.addConverter(new StringToIpPortConverter());
    }
}
```

```java
@RestController
public class TestController {

		// String -> IpPort로 자동변환됨!
		// ip-port?ipPort=127.0.0.1:8080
    @GetMapping("/ip-port")
    public String ipPort(@RequestParam("ipPort") IpPort ipPort) {
        System.out.println("ipPort IP = " + ipPort.getIp());
        System.out.println("ipPort PORT = " + ipPort.getPort());
        return "ok";
    }
}
```

</aside>

# **스프링 타입 포맷터**

---

<aside>
💡 **NOTE**

> *스프링 `Formatter` 인터페이스는 `Converter`와 비슷하지만 문자에 특화되어 있고 Local을 활용한 국제화가 가능하다는 차이점이 있습니다.*
> 

```java
public interface Formatter<T> extends Printer<T>, Parser<T> {
		// 객체 -> 문자
    String print(T object, Locale locale);
    
    // 문자 -> 객체
    T parse(String text, Locale locale) throws ParseException;
}
```

```java
public class MyNumberFormatter implements Formatter<Number> {

		// 숫자 -> 문자 변환
    @Override
    public String print(Number object, Locale locale) {
        return NumberFormat.getInstance(locale).format(object);
    }

		// 문자 -> 숫자 변환
    @Override
    public Number parse(String text, Locale locale) throws ParseException {
        return NumberFormat.getInstance(locale).parse(text);
    }
}
```

```java
@Test
void parse() throws ParseException {
    Number result = formatter.parse("1,000", Locale.KOREA);
    assertThat(result).isEqualTo(1000L);
}

@Test
void print() {
    String result = formatter.print(1000, Locale.KOREA);
    assertThat(result).isEqualTo("1,000");
}
```

스프링은 애노테이션 기반으로 원하는 형식을 지정해서 사용할 수 있는 유용한 포맷터를 제공합니다. 

- `@NumberFormat`: 숫자 관련 형식 지정 포맷터 사용
- `@DateTimeFormat`: 날짜 관련 형식 지정 포맷터 사용
</aside>

## ConversionService 활용

<aside>
✍️ **NOTE**

> `*Converter`와 동일하게 `DefaultFormattingConversionService`를 통해 등록하여 사용할 수 있습니다.*
> 

```java
@Test
void conversionServiceWithFormatter() {
    // 1. FormattingConversionService 생성
    DefaultFormattingConversionService conversionService = new DefaultFormattingConversionService();

    // 2. 포맷터 등록(컨버터 등록도 가능)
    conversionService.addFormatter(new MyNumberFormatter());

    // 3. 포맷터 사용
    Number number = conversionService.convert("1,000", Number.class);
    assertThat(number).isEqualTo(1000);
    String formattedNumber = conversionService.convert(1000, String.class);
    assertThat(formattedNumber).isEqualTo("1,000");
}
```

</aside>

## Formatter와 Jackson

<aside>
✍️ **NOTE**

> `*Formatter`는 JSON 직렬화 과정에 영향을 미치지 않습니다. 스프링의 데이터 바인딩 혹은 웹 form 제출에는 유효하지만 REST API응답에서 제대로 사용하기 위해선 Jackson 라이브러리가 제공하는 어노테이션을 사용해야 합니다.*
> 

### @JsonFormat 사용

`@JsonFormat`은 Jackson 라이브러리가 제공하는 어노테이션으로 JSON 직렬화/역직렬화 시 날짜 및 숫자 형식을 지정하는데 사용할 수 있습니다.

```java
@Data
static class Form {
    @NumberFormat(pattern = "###,###")
    private Integer number;
    
    // 수정!
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime localDateTime;
}
```

- `@NumberFormat`의 경우 `@JsonFormat`이 적용되지 않으므로 다른 방법을 고려해야 합니다.

### Jackson 사용자 정의 직렬화

Jackson의 사용자 정의 직렬화를 만들어서 사용할 수 있습니다.

```java
public class CustomNumberSerializer extends JsonSerializer<Integer> {

		// 직렬화 구현
    @Override
    public void serialize(Integer value, JsonGenerator gen, SerializerProvider serializers) throws IOException {
        NumberFormat formatter = NumberFormat.getInstance();
        formatter.setGroupingUsed(true);
        formatter.setMinimumFractionDigits(0);
        formatter.setMaximumFractionDigits(0);
        String formattedNumber = formatter.format(value);
        gen.writeString(formattedNumber);
    }
}
```

```java
@Data
static class Form {
		// 커스텀 직렬화 설정
    @JsonSerialize(using = CustomNumberSerializer.class)
    private Integer number;
    
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime localDateTime;
}
```

</aside>

# 덤프

```java
package org.okestro.tps.api.infrastructure.config;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.okestro.tps.api.application.ticket.enums.TableEnum;
import org.springframework.core.convert.converter.Converter;
import org.springframework.core.convert.converter.ConverterFactory;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class StringToTableEnumConverterFactory implements ConverterFactory<String, TableEnum> {

    @Override
    public <T extends TableEnum> Converter<String, T> getConverter(Class<T> targetType) {
        if (!targetType.isEnum()) {
            throw new IllegalArgumentException("TableEnum 구현체는 Enum이어야 합니다.");
        }
        return new StringToTableEnumConverter<>(targetType);
    }

    // TableEnum => 구현 Enum 변환
    @RequiredArgsConstructor
    private static class StringToTableEnumConverter<T extends TableEnum> implements Converter<String, T> {

        private final Class<T> enumType;

        @Override
        public T convert(String source) {
            if (source.isEmpty()) {
                return null;
            }

            for (T enumConstant : enumType.getEnumConstants()) {
                if (enumConstant.getCode().equals(source)) {
                    log.debug("변환성공");
                    return enumConstant;
                }
            }

            String errmsg = String.format("Enum 상수에 '%s' 코드가 없습니다. enumType= %s", source, enumType.getSimpleName());
            throw new IllegalArgumentException(String.format(errmsg));
        }
    }
}
```

```java

```