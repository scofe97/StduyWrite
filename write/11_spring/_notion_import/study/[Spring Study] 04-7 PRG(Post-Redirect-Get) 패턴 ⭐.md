# [Spring Study] 04-7. PRG(Post-Redirect-Get) 패턴 ⭐

주제: Spring Study

- 참고
    
    [스프링 MVC 기본 기능 - 웹 페이지 만들기 :: 개발자 한선우](https://yadon079.github.io/2022/spring/spring-mvc-11)
    

# **PRG(Post-Redirect-Get) 패턴**

---

<aside>
💡 **NOTE**

> ***PRG 패턴은 웹 개발시 자주 사용되는 디자인 패턴이다!***
> 

![새로고침 할 때 마다 POST 요청이 수행된다 ( 중복 수행 )](%5BSpring%20Study%5D%2004-7%20PRG(Post-Redirect-Get)%20%ED%8C%A8%ED%84%B4%20%E2%AD%90/Untitled.png)

새로고침 할 때 마다 POST 요청이 수행된다 ( 중복 수행 )

- POST 요청에 대한 응답이 또 다른 URL로의 GET 요청을 위한 리다이렉트여야 한다는 것
- 만약 POST요청에 대한 응답이 리다이렉트가 아닌 **단순 페이지 이동이면 문제가 발생한다.**
</aside>

## **PRG(Post-Redirect-Get) 패턴 적용**

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20Study%5D%2004-7%20PRG(Post-Redirect-Get)%20%ED%8C%A8%ED%84%B4%20%E2%AD%90/Untitled%201.png)

```java
@PostMapping("/add")
public String addItemV5(Item item) {

  itemRepository.save(item);
  
  /* Path Variable로 추가되는 item의 id와 같은 변수를 추가적으로 인코딩 되지 않음 */
  return **"redirect:/basic/items/" + item.getId();**
}
```

- **Redirect를 이용해서 GET을 호출하도록 설계**
- 이제 브라우저 새로고침이 있어도 해당되는 GET만 다시 요청된다.
- **POST 요청 후 redirect 수행시 주의사항**
    - 특정 값을 추가해서 redirec할 때, 서블렛에서는 데이터를 전달할 방법이 없었다.
    → **`RedirectAttributes`를 사용해서 해결이 가능**해짐
</aside>

# **RedirectAttributes**

---

<aside>
💡 **NOTE**

> **Redirect를 할 때 URL 인코딩, Path Variable / Query Parameter를 처리해준다
특정 VIew에서 Redirect의 여부를 확인하기 위해 변수를 전달에 사용**
> 

```java
@PostMapping("/add")
public String addItemV6(Item item, RedirectAttributes redirectAttributes) {
  
  Item savedItem = itemRepository.save(item);
  
  redirectAttributes.addAttribute("itemId", savedItem.getId()); // 3
  redirectAttributes.addAttribute("status", true);
  
  **return "redirect:/basic/items/{itemId}";**
}
```

- RedirectAttributes 객체 사용
- .addAttribute로 값을 추가할 수 있음
- url 경로에 변수가 존재하면 넣어주며, 없으면 자동으로 Query Parameter로 처리됨
</aside>