# [Spring Study] 06-1. Validation 처리 - BindingResult

주제: Spring Study

- 참고
    
    [[Spring MVC] [2] 4. 검증1 - Validation](https://velog.io/@dbsrud11/Spring-MVC-2-4)
    
    [[Spring] @Valid, @Validated 사용법](https://developer-rooney.tistory.com/229)
    
    [[Spring] 스프링의 다양한 예외 처리 방법(ExceptionHandler, ControllerAdvice 등) 완벽하게 이해하기 - (1/2)](https://mangkyu.tistory.com/204)
    

# Validation **처리**

---

<aside>
💡 **NOTE**

> *스프링 부트에서는 데이터 `Validation`을 위해 여러 접근 방식을 제공합니다. `Validation` 처리는 주로 데이터의 유효성을 확인하고, 타입 불일치 등의 입력 오류를 사용자에게 알려주는데 사용됩니다.*
> 

**검증** 처리에는 `@ModelAttribute(form data)`와 `@RequestBody(JSON)` 두 가지 타입이 있습니다. 이 두 요청 모두 `@Valid`, `@Validated` 어노테이션을 통해 처리 가능하지만 처리 방식에 차이가 있습니다.

- `@ModelAttribute`: `BindingResult`를 사용하여 메서드 내에서 바로 오류를 처리할 수 있습니다.
- `@RequestBody`: 검증 실패 시 `MethodArgumentNotValidException` 예외를 발생시켜 별도의 예외 처리기에서 관리합니다.
</aside>

## **BindingResult**

<aside>
✍️ **NOTE**

> `*BindingResult`는 스프링이 제공하는 검증 오류를 보관하는 객체입니다.*
> 

```java
@PostMapping("/add")
public String addItemV1(@ModelAttribute Item item, BindingResult bindingResult) {
    if (!StringUtils.hasText(item.getItemName())) {
        bindingResult.addError(new FieldError("item", "itemName", "상품 이름은 필수입니다."));
    }
    
    if (item.getPrice() == null || item.getPrice() < 1000 || item.getPrice() > 1000000) {
        bindingResult.addError(new FieldError("item", "price", "가격은 1,000 ~ 1,000,000 까지 허용합니다."));
    }
    
    if (item.getQuantity() == null || item.getQuantity() >= 10000) {
        bindingResult.addError(new FieldError("item", "quantity", "수량은 최대 9,999 까지 허용합니다."));
    }
    
    if (item.getPrice() != null && item.getQuantity() != null) {
        int resultPrice = item.getPrice() * item.getQuantity();
        if (resultPrice < 10000) {
            bindingResult.addError(new ObjectError("item", "가격 * 수량의 합은 10,000원 이상이어야 합니다. 현재 값 = " + resultPrice));
        }
    }
    
    if (bindingResult.hasErrors()) {
        return "validation/v2/addForm";
    }
    
    // ...
}
```

- `BindingResult`는 인터페이스이며 `Errors`를 상속받고 있습니다. `Errors`를 사용해도 되지만, `BindingResult`가 더 사용하기 쉽게 되어있습니다.
- `BindingResult` 객체는 `FiledError`와 `ObjectError`를 통해 발생한 오류들을 관리합니다. 만약 JSP, Thymeleaf를 사용하는 경우 오류 정보에 접근이 가능합니다.
    - `FiledError`: 특정 필드에 대한 검증 실패 정보
    - `ObjectError`: 객체 레벨의 오류(필드 에러가 아닌 객체검증)
</aside>

## 오류 메시지 파일

<aside>
✍️ **NOTE**

> `*MessageSource`는 스프링 프레임워크의 국제화 기능을 지원하는 인터페이스이며, 이를 통해 에러 메시지를 외부에서 관리할 수 있게됩니다.*
> 

```yaml
spring:
  messages:
    basename: messages,errors
```

- `errors.properteis`, `errors_[언어].properteis`의 파일들을 사용할 수 있게됩니다.

```java
required.item.itemName=상품 이름은 필수입니다.
range.item.price=가격은 {0} ~ {1} 까지 허용합니다.
max.item.quantity=수량은 최대 {0} 까지 허용합니다.
totalPriceMin=가격 * 수량의 합은 {0}원 이상이어야 합니다. 현재 값 = {1}
```

- 에러 메시지 등록

```java
public class MessageService {

    @Autowired
    private MessageSource messageSource;

    public String getRequiredItemNameMessage(Locale locale) {
        return messageSource.getMessage("required.item.itemName", null, locale);
    }

    public String getRangeItemPriceMessage(int min, int max, Locale locale) {
        Object[] args = {min, max};
        return messageSource.getMessage("range.item.price", args, locale);
    }

    public String getMaxItemQuantityMessage(int max, Locale locale) {
        Object[] args = {max};
        return messageSource.getMessage("max.item.quantity", args, locale);
    }

    public String getTotalPriceMinMessage(int min, int current, Locale locale) {
        Object[] args = {min, current};
        return messageSource.getMessage("totalPriceMin", args, locale);
    }
}
```

</aside>

## **rejectValue, reject**

<aside>
✍️ **NOTE**

> `*rejectValue`와 `reject`는 BindingResult에서 제공하는 메서드로, 데이터 검증 과정에서 발생한 오류를 특정 필드나 전역적으로 등록하는데 사용됩니다.*
> 

```java
// FieldError => rejectValue()
// rejectValue(
if (!StringUtils.hasText(item.getItemName())) {
    bindingResult.rejectValue("itemName", "required");
}
if (item.getPrice() == null || item.getPrice() < 1000 || item.getPrice() > 1000000) {
    bindingResult.rejectValue("price", "range", new Object[]{1000,1000000}, null);
}
if (item.getQuantity() == null || item.getQuantity() >= 9999) {
    bindingResult.rejectValue("quantity", "max", new Object[]{9999}, null);
}

// ObjectError => reject()
if (item.getPrice() != null && item.getQuantity() != null) {
    int resultPrice = item.getPrice() * item.getQuantity();
    if (resultPrice < 10000) {
        bindingResult.reject("totalPriceMin", new Object[]{10000, resultPrice}, null);
    }
}
```

```java
void rejectValue(String field,           // 오류 발생 필드이름
								 String errorCode,       // 오류 코드, 화면에서 오류 메시지 찾기위한 키 값
								 Object[] errorArgs,     // 메시지 인자값
								 String defaultMessage); // 메시지가 없는 경우 기본 메시지
								 
								 
void reject(String errorCode,            // 전역 오류 코드, 화면에서 오류 메시지 찾기 위한 키 값
            Object[] errorArgs,          // 메시지 인자값, 메시지 포맷팅에 사용
            String defaultMessage);      // 메시지가 없는 경우 기본으로 사용될 메시지
```

</aside>

## **MessageCodesResolver,** DefaultMessageCodeResolver

<aside>
✍️ **NOTE**

> `*MessageCodesResolver`와 구현체인 `DefaultMessageCodeResolver`는 스프링에서 유효성 검사를 할 때 어떤 오류 메시지를 찾을지 결정하는 역할을 진행합니다.*
> 

```java
typeMismatch.item.name=상품 이름에는 문자열이어야 합니다.
typeMismatch.item.price=상품 가격에는 숫자를 입력해야 합니다.
```

```java
private final MessageCodesResolver messageCodesResolver = new DefaultMessageCodesResolver();

@PostMapping("/items")
public String addItem(@RequestBody Item item, BindingResult bindingResult) {
    // MessageCodesResolver를 사용하여 메시지 코드 생성
    String[] errorCodes = messageCodesResolver.resolveMessageCodes("typeMismatch", "item.name");

    // 생성된 메시지 코드를 이용하여 오류 메시지를 BindingResult에 추가
    bindingResult.rejectValue("name", errorCodes[0]);

    // 오류가 있으면 폼 페이지로 다시 이동
    if (bindingResult.hasErrors()) {
        return "itemForm";
    }

    // 유효성 검사 통과 시, 비즈니스 로직 수행
    // ...

    // 성공 시 다음 페이지로 리다이렉트 또는 응답
    return "redirect:/success";
}
```

</aside>

## **Validator 분리(Validator 구현, WebDataBinder)**

<aside>
✍️ **NOTE**

> `*BindingResult`의 복잡한 검증 로직을 별도로 분리하여 컨트롤러에서 간결하게 유지하기 위해서는 `Validator` 인터페이스를 구현하고, `WebDataBinder`에 등록하면 됩니다.*
> 

```java
public interface Validator {
    boolean supports(Class<?> clazz);
    void validate(Object target, Errors errors);
}
```

```java
@Component
public class ItemValidator implements Validator {
    
    @Override
    public boolean supports(Class<?> clazz) {
        return Item.class.isAssignableFrom(clazz); // 검증 하겠다는 의미
    }

    @Override
    public void validate(Object target, Errors errors) {
        Item item = (Item) target;
        
        ValidationUtils.rejectIfEmptyOrWhitespace(errors, "itemName", "required");
        
        if (item.getPrice() == null || item.getPrice() < 1000 || item.getPrice() > 1000000) {
            errors.rejectValue("price", "range", new Object[]{1000, 1000000}, null);
        }
        
        if (item.getQuantity() == null || item.getQuantity() > 10000) {
            errors.rejectValue("quantity", "max", new Object[]{9999}, null);
        }
        
        if (item.getPrice() != null && item.getQuantity() != null) {
            int resultPrice = item.getPrice() * item.getQuantity();
            if (resultPrice < 10000) {
                errors.reject("totalPriceMin", new Object[]{10000, resultPrice}, null);
            }
        }
    }
}
```

- `supports()` : 해당 검증기를 지원하는지 여부
- `validate(Object target, Errors errors)` : 검증 대상 객체와 `BindingResult`

```java
private final ItemValidator itemValidator;

@PostMapping("/add")
public String addItemV5(@ModelAttribute Item item, BindingResult bindingResult) {
		// 검증 로직 단순화
    itemValidator.validate(item, bindingResult);

    if (bindingResult.hasErrors()) {
        return "validation/v2/addForm";
    }

    // 성공 로직
    return "redirect:/validation/v2/items";
}
```

`WebDataBinder`를 사용하여 `Validator`를 등록하면 해당 컨트롤러에서 자동으로 검증이 수행됩니다.

```java
private final ItemValidator itemValidator;

@InitBinder
public void init(WebDataBinder dataBinder){
    dataBinder.addValidators(itemValidator);
}

// @Validated 어노테이션으로 자동으로 Validation 진행
@PostMapping("/add")
public String addItemV6(@Validated @ModelAttribute Item item, BindingResult bindingResult) {
    if (bindingResult.hasErrors()) {
        return "validation/v2/addForm";
    }

    // 성공 로직
    return "redirect:/validation/v2/items";
}
```

- 위 코드에서 `@Validated` 대신 `@Valid`를 사용해도 정상적으로 동작합니다.
    - `@Valid`: 자바 표준 어노테이션
    - `@Validated`: 스프링 특화 어노테이션
</aside>