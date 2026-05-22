# [Spring Study] 08-1. 횡단 관심사

주제: Spring Study

- 참고
    
    [10 Frequently Occurring Cross-Cutting Concerns](https://peterbeukema.medium.com/top-10-cross-cutting-concerns-4cf30f7ab7fa)
    
    [횡단 관심사 (Cross-cutting-concerns)](https://taak-e.tistory.com/entry/횡단-관심사-Cross-cutting-concerns#google_vignette)
    
    [횡단관심사, 그게 뭔데요](https://hellomooneekim.netlify.app/횡단관심사/)
    

# 1. 목차

---

<aside>
💡 **NOTE**

> 
> 
- 
- 

</aside>

## 목차

<aside>
✍️ **NOTE**

- 
- 

</aside>

# 1. 목차

---

<aside>
💡 **NOTE**

> 
> 
- 
- 

</aside>

## 목차

<aside>
✍️ **NOTE**

- 
- 
</aside>

# 필터 vs 인터셉터 vs AOP

---

<aside>
💡 **NOTE**

> `*Filter`, `Interceptor`, `AOP`는 모두 실제 비즈니스 로직이 호출되기 이전, 이후에 공통적으로 처리해야 하는 기능들인 Logging, 인증, 인코딩 변환등의 공통로직(횡단 관심)을 처리하기 위한 계층입니다.*
> 

아래의 이미지를 보면 `Filter`, `Interceptor`, `AOP`모두 각 메서드가 실행되는 범위가 다릅니다. 이러한 실행되는 시점의 차이에 따라서 어떠한 곳에 공통로직을 사용할지가 결정됩니다.

![Filter - Interceptor - Aop](%5BSpring%20Study%5D%2008-1%20%ED%9A%A1%EB%8B%A8%20%EA%B4%80%EC%8B%AC%EC%82%AC/Untitled.png)

Filter - Interceptor - Aop

- AOP에 대해서는 이후 자세히 다룹니다. 지금은 횡단 관심사를 구현하는 기술정도로만 알아주세요

![횡단 관심사](%5BSpring%20Study%5D%2008-1%20%ED%9A%A1%EB%8B%A8%20%EA%B4%80%EC%8B%AC%EC%82%AC/Untitled%201.png)

횡단 관심사

</aside>

## 필터 vs 인터셉터

<aside>
✍️ **NOTE**

> *Filter와 Interceptor모두 HttpServletRequest/Response의 속성을 조작할 수 있는 기능을 제공하지만, 조작의 범위가 조금 다릅니다.*
> 

![Untitled](%5BSpring%20Study%5D%2008-1%20%ED%9A%A1%EB%8B%A8%20%EA%B4%80%EC%8B%AC%EC%82%AC/Untitled%202.png)

[Spring Filter에서 Response 수정하기](https://medium.com/sjk5766/spring-filter에서-response-수정하기-7de6da9836f5)

실무에서는 큰 의미가 없을 수 있지만 Filter는 반환되는 데이터를 직접 수정하는 로직을 작성할 수 있습니다. 하지만 Interceptor의 경우에는 불가능합니다.

- `Filter`: Servlet API의 일부로, HTTP 요청/응답의 전처리 및 후처리를 담당합니다. 요청/응답에 대한 직접적인 접근을 제공하며, Header나 Body를 읽고 수정할 수 있습니다.
- `Interceptor`: `HttpServletRequest/Response`에 접근이 가능하지만, 주로 요청 처리 전후의 추가 작업에 초점을 맞춥니다. 실제 Body를 조작하는 기능은 제공하지 않습니다.
</aside>