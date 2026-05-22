# [Spring Study] 06-2. Bean Validation(@Validated)

주제: Spring Study

- 참고
    
    [[Spring] 스프링의 다양한 예외 처리 방법(ExceptionHandler, ControllerAdvice 등) 완벽하게 이해하기 - (1/2)](https://mangkyu.tistory.com/204)
    
    [[Spring MVC] [2] 5. 검증2 - Bean Validation](https://velog.io/@dbsrud11/Spring-MVC-2-5.-%EA%B2%80%EC%A6%9D2-Bean-Validation#1-bean-validation---%EC%86%8C%EA%B0%9C)
    
    [Validation 어디까지 해봤니? : NHN Cloud Meetup](https://meetup.nhncloud.com/posts/223)
    
    [Cross-Parameter Validation with Spring](https://focusedlabs.io/blog/cross-parameter-validation-with-spring)
    

# **Bean Validation**

---

<aside>
💡 **NOTE**

> *Bean Validation은 특정 구현체가 아니라 Bean Validation 2.0 (JSR-380)을 기반으로 한 기술 표준입니다. 이 표준은 다양한 어노테이션과 인터페이스로 구성되어 있습니다.*
> 

```java
implementation 'org.springframework.boot:spring-boot-starter-validation'
```

Validation의 구현체로 Hibernate 구현체가 있는데 이는 ORM과 직접적인 연관은 없으며 Bean Validatior의 여러 구현체 중 하나로 보면 됩니다.

</aside>

## **Bean Validation - 사용/테스트**

<aside>
✍️ **NOTE**

> *스프링에서는 여러 validation의 어노테이션을 제공하여 객체의 필드에 적용함으로써, 해당 필드가 특정 조건을 충족하는지 쉽게 검증할 수 있습니다.*
> 

```java
@NotNull    // 필드 값이 null이 아니어야 합니다.
@NotEmpty   // 필드 값이 null이 아니며, 빈 문자열("")이 아니어야 합니다.
@NotBlank   // 필드 값이 null이 아니며, 공백을 포함한 빈 문자열이 아니어야 합니다.
@AssertTrue // 필드 값이 true여야 합니다.
@Size       // 문자열, 컬렉션, 맵, 배열 등의 크기가 지정된 범위 안에 있어야 합니다.
@Min, @Max  // 숫자가 지정된 최소값 이상, 최대값 이하이어야 합니다.
@Pattern    // 문자열이 정규 표현식과 일치해야 합니다.
```

스프링은 다음과 같은 순서로 입력 데이터의 처리 및 검증을 진행합니다.

1. **데이터 바인딩과 타입 변환**
    - `@ModelAttribute` 사용시, 각 필드에 대한 타입 변환 시도가 이루어집니다.
        - 변환 성공: `Validator` 적용
        - 변환 실패: 타입 불일치로 `FiledError`가 생성되고, `typeMismatch` 오류로 분류된다.
2. **Bean Validation 적용**
    - 바인딩에 성공한 필드만이 Bean Validation 검증 대상이 됩니다.
    - 검증 과정에서 오류가 발견되면 FiledError or ObjectError가 BindingResult 객체에 저장됩니다.
- **검증하는 방법 2가지**
    1. BeanValidation의 `groups`기능
    2. item을 직접 사용하지 않고, `ItemSaveForm`, `ItemUpdateFomr` 같은 폼 전송을 위한 별도의 모델 객체 사용

```java
@Data
public class Item {
    private Long id;
    
    @NotBlank
    private String itemName;
    
    @NotNull
    @Range(min = 1000, max = 1000000)
    private Integer price;
    
    @NotNull
    @Max(9999)
    private Integer quantity;

    public Item() {}
    public Item(String itemName, Integer price, Integer quantity) {
        this.itemName = itemName;
        this.price = price;
        this.quantity = quantity;
    }
}
```

```java
public class BeanValidationTest {
    @Test
    void beanValidation() {
        // ValidatorFactory를 생성합니다. 이 팩토리는 Bean Validation의 기본 구현을 제공합니다.
        ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
        
        // Validator 인스턴스를 가져옵니다. 이 인스턴스를 사용하여 데이터 모델을 검증할 수 있습니다.
        Validator validator = factory.getValidator();
        
        // 검증할 Item 객체를 생성합니다. 이 객체는 공백 이름, 0 가격, 10000 수량으로 초기화됩니다.
        Item item = new Item(" ", 0, 10000);
        
        // Item 객체를 검증하고, 위반된 제약 조건들의 집합을 반환합니다.
        Set<ConstraintViolation<Item>> violations = validator.validate(item);
        
        // 검증 결과의 각 ConstraintViolation을 순회하면서, 위반 사항과 해당 메시지를 출력합니다.
        for (ConstraintViolation<Item> violation : violations) {
            System.out.println("violation=" + violation); // 위반된 제약 조건의 상세 정보를 출력합니다.
            System.out.println("violation.message=" + violation.getMessage()); // 위반 사항에 대한 메시지를 출력합니다.
        }
    }
}

```

```java
@PostMapping("/items/new")
public String addItem(@ModelAttribute @Valid Item item, BindingResult bindingResult) {
    if (bindingResult.hasErrors()) {
        return "itemForm"; // 오류가 있으면 폼 페이지로 반환
    }
    // 비즈니스 로직 실행
    return "redirect:/items";
}
```

</aside>

## **Bean Validation 한계**

<aside>
✍️ **NOTE**

> `*Bean Validation`을 통해 데이터 검증을 효율적으로 할 수 있지만, 하나의 DTO로 등록/수정에 대하여 다른 검증 요구사항이 발생할 수 있습니다.*
> 

만약 Item 도메인의 경우 등록과 수정에 대하여 다른 검증 요구사항이 있다고 가정해봅시다.

- **등록**: id값 필수 x, 수량 9999 제한
- **수정**: id값 필수 O, 수량 제한 없음

`Bean Validation`에서는 이러한 문제를 해결하기 위해 groups라는 기능을 제공합니다. 하지만 실제적으로 등록/수정에서 동일한 DTO를 사용하는 경우가 드물어 일반적으로는 분리해서 사용하게 됩니다.

```java
// 등록 그룹
public interface SaveCheck {}

// 수정 그룹
public interface UpdateCheck {}
```

```java
@Data
public class Item {
    @NotNull(groups = UpdateCheck.class)  // 수정 시에만 적용
    private Long id;
    
    @NotBlank(groups = {SaveCheck.class, UpdateCheck.class})
    private String itemName;
    
    @NotNull(groups = {SaveCheck.class, UpdateCheck.class})
    @Range(min = 1000, max = 1000000, groups = {SaveCheck.class, UpdateCheck.class})
    private Integer price;
    
    @NotNull(groups = {SaveCheck.class, UpdateCheck.class})
    @Max(value = 9999, groups = SaveCheck.class)  // 등록 시에만 적용
    private Integer quantity;
}
```

```java
// 등록 그룹
@PostMapping("/add")
public String addItemV2(@Validated(SaveCheck.class) 
												@ModelAttribute Item item,
BindingResult bindingResult, RedirectAttributes redirectAttributes) {}

// 수정 그룹
@PostMapping("/{itemId}/edit")
public String editV2(@PathVariable Long itemId, 
										 @Validated(UpdateCheck.class)
										 @ModelAttribute Item item, 
										 BindingResult bindingResult) {}
```

</aside>

## **Form 전송 객체 분리**

<aside>
✍️ **NOTE**

```java
@Data
public class ItemSaveForm {
    @NotBlank
    private String itemName;
    
    @NotNull
    @Range(min = 1000, max = 1000000)
    private Integer price;
    
    @NotNull
    @Max(value = 9999)
    private Integer quantity;
}

```

```java
@Data
public class ItemUpdateForm {
    @NotNull
    private Long id;
    
    @NotBlank
    private String itemName;
    
    @NotNull
    @Range(min = 1000, max = 1000000)
    private Integer price;
    
    // 수정에서는 수량 제한 없음
    private Integer quantity;
}

```

</aside>

## **HTTP 메시지 컨버터**

<aside>
✍️ **NOTE**

> `*Bean Validation`과 **HTTP 메시지 컨버터**와의 통합을 통해 JSON과 같은 HTTP Body 데이터를 처리할 때 유효성 검증을 자동으로 적용할 수 있습니다.*
> 

`@Valid`, `@Validate`, `@RequestBody`를 같이 사용하는 경우로 예시를 들어보겠습니다.

```java
@RestController
public class MemberController {

    @PostMapping("/member")
    public ResponseEntity<?> createMember(@Valid @RequestBody MemberDto memberDto, BindingResult result) {
        if (result.hasErrors()) {
            FieldError error = result.getFieldError();
            ErrorResponse errorResponse = new ErrorResponse(error.getDefaultMessage());
            return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
        }

        SuccessResponse successResponse = new SuccessResponse("Member created successfully");
        return new ResponseEntity<>(successResponse, HttpStatus.CREATED);
    }
}
```

- 성공 요청
    - ex) `{"itemName":"hello", "price":1000, "quantity": 10}`
    - 성공적으로 데이터 가 바인딩되고, 검증이 통과됩니다.
- 타입 불일치로 인한 실패요청
    - ex) `{"itemName":"hello", "price":"A", "quantity": 10}`
    - HttpMessageNotReadableException 예외가 발생하며 HttpMessageConverter 단계에서 실패하므로 검증 로직이 실행되지 않습니다.
- 검증 오류 요청
    - ex) `{"itemName":"hello", "price":1000, "quantity": 10000}`
    - quantity의 최대 허용범위를 넘어서

### @ModelAttribute vs @RequestBody

- `@ModelAttribute`
    - URL 쿼리 스트링, Post 폼 데이터 객체 바인딩에 주로 쓰입니다.
    - 각 필드 단위로 데이터가 바인딩되며, 특정 필드에서 타입 불일치가 발생해도 다른 필드는 정상적으로 처리됩니다.
- `@RequestBody`
    - HTTP body을 사용하여 객체를 생성할 때 쓰입니다.
    - 만약 데이터 변환에 실패하면, 컨트롤러 메서드 자체가 호출되지 않기 때문에 검증 절차 또한 진행되지 않습니다.

### BindingResult vs ControllerAdvice

스프링 부트에서 데이터 유효성을 검증할 때 BindingResult를 통해서 직접 사용하는 방법과 ControllerAdvice를 활용하는 방식 2가지가 있습니다.

</aside>

## BindingResult vs ControllerAdvice

<aside>
✍️ **NOTE**

> *스프링 부트에서 데이터 유효성을 검증할 때 `BindingResult`를 통해서 직접 사용하는 방법과 `ControllerAdvice`를 활용하는 방식 2가지가 있습니다.*
> 

### BindingResult

- BindingResult는 컨트롤러 내에서 유효성 검사를 직접 제어하고 처리할 수 있습니다.
- 여러 필드에서 오류가 발생한 경우, 각 필드 별로 오류 메시지를 제공하여 사용자에게 더 자세한 피드백을 제공할 수 있습니다.
- 하지만 컨트롤러의 코드길이가 늘어나고, 중복되는 코드가 늘어날 수 있습니다.

### ControllerAdvice

- 모든 예외 처리 로직을 중앙에서 관리해 코드의 일관성과 오류 응답 형식을 통일 할 수 있습니다.
- 표준화된 처리 제공이 가능하지만 경우에 따라 맞춤 응답을 제공하기가 어렵습니다.
</aside>