# [Spring TDD] 01-2. 테스트 더블

주제: Spring TDD

- 참고
    
    [테스트 더블 (Test Double)](https://hudi.blog/test-double/)
    
    [Test Double을 알아보자](https://tecoble.techcourse.co.kr/post/2020-09-19-what-is-test-double/)
    
    [[Effective unit Testing] Chap3. 테스트 더블](https://aroundck.tistory.com/6109)
    

# **테스트 더블 (Test Double)**

---

<aside>
💡 **NOTE**

> ***테스트를 진행하기 어려운 경우 이를 대신해 테스트를 진행할 수 있도록 만들어주는 객체를 말한다!***
> 

![ex) 데이터베이스와 같이 공유자원을 사용하는 경우, 순서에따라 다른 결과를 유발한다.
⇒ 이런 연관된 객체를 사용하기 어려울때 사용하는게 **테스트 더블!**](%5BSpring%20TDD%5D%2001-2%20%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EB%8D%94%EB%B8%94/Untitled.png)

ex) 데이터베이스와 같이 공유자원을 사용하는 경우, 순서에따라 다른 결과를 유발한다.
⇒ 이런 연관된 객체를 사용하기 어려울때 사용하는게 **테스트 더블!**

- **테스트 더블의 종류**
    - Dummy
    - Fake
    - Stub
    - Spy
    - Mock
</aside>

## 1. Dummy

<aside>
✍️ **NOTE**

> ***가장 기본적인 테스트 더블, 인스턴스화된 객체가 필요하지만 기능이 필요하지 않은경우 사용한다!***
> 

```java
// 실제 인터페이스
public interface PringWarning{ void print(); }

// Dummy 구현
public class PrintWarningDummy implments PrintWarning {
		@Override
    public void print() {
        // 아무런 동작을 하지 않는다.
    }
}
```

</aside>

## 2. Fake

<aside>
✍️ **NOTE**

> ***동작은 하지만 실제 사용되는 객체처럼 정교하게 동작하지 않는 객체이다!***
> 

![그냥 객체참고용](%5BSpring%20TDD%5D%2001-2%20%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EB%8D%94%EB%B8%94/Untitled%201.png)

그냥 객체참고용

```java
public interface UserRepository {
    void save(User user);
    User findById(long id);
}

public class FakeUserRepository implements UserRepository {
    private Collection<User> users = new ArrayList<>();
    
    @Override
    public void save(User user) {
        if (findById(user.getId()) == null) {
            user.add(user);
        }
    }
    
    @Override
    public User findById(long id) {
        for (User user : users) {
            if (user.getId() == id) {
                return user;
            }
        }
        return null;
    }
}
```

</aside>

## 3. Stub

<aside>
✍️ **NOTE**

> ***Dummy 객체가 실제로 동작하는 것 처럼 보이게 만들어 놓은 객체이다!***
> 

![실제 DB를 사용하지 않고 사용한것처럼 응답해줌](%5BSpring%20TDD%5D%2001-2%20%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EB%8D%94%EB%B8%94/Untitled%202.png)

실제 DB를 사용하지 않고 사용한것처럼 응답해줌

```java
public class StubUserRepository implements UserRepository {
    // ...
    @Override
    public User findById(long id) {
        return new User(id, "Test User");
    }
}
```

- 테스트에서 자주 사용되는 Mockito 프레임워크도 Stub와 같은 역할을 해준다!
- 테스트를 위해 의도한 결과만 반환되도록 하기 위한 객체 ⇒ Stub
</aside>

## 4. Spy

<aside>
✍️ **NOTE**

> ***Stub의 역할을 가지면서 호출된 내용에 대해 약간의 정보를 기록한다!***
> 

```java
public class MailingService {
    private int sendMailCount = 0;
    private Collection<Mail> mails = new ArrayList<>();

    public void sendMail(Mail mail) {
        sendMailCount++;
        mails.add(mail);
    }

    public long getSendMailCount() {
        return sendMailCount;
    }
}
```

- 자기 자신이 호출된 상황을 확인할 수 있는 객체 ⇒ Spy
- Mockito 프레임워크의 `verify()` 메서드가 같은 역할을 해준다.
</aside>

## 5. Mock

<aside>
✍️ **NOTE**

> ***호출에 대한 기대를 명세하고 내용에 따라 동작하도록 프로그래밍 된 객체이다.***
> 

![명세에 따라 동작하도록한다.](%5BSpring%20TDD%5D%2001-2%20%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EB%8D%94%EB%B8%94/Untitled%203.png)

명세에 따라 동작하도록한다.

```java
@ExtendWith(MockitoExtension.class)
public class UserServiceTest {
    @Mock
    private UserRepository userRepository;
    
    @Test
    void test() {
        when(userRepository.findById(anyLong())).thenReturn(new User(1, "Test User"));
        
        User actual = userService.findById(1);
        assertThat(actual.getId()).isEqualTo(1);
        assertThat(actual.getName()).isEqualTo("Test User");
    }
}
```

</aside>