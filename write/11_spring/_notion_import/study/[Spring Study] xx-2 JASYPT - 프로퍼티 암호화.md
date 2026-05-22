# [Spring Study] xx-2. JASYPT - 프로퍼티 암호화

주제: Spring Study

- 참고
    
    [Spring Boot 프로젝트 properties 암복호화 처리 구현하기](https://luvstudy.tistory.com/251#article-2--spring-security-crypto-소개)
    
    [[Spring] JASYPT를 사용한 프로퍼티 암호화](https://emgc.tistory.com/137)
    

# **JASYPT란?**

---

<aside>
💡 **NOTE**

> ***개발자가 암호화 작동 방식에 대한 깊은 지식 없이도 프로젝트에 기본 암호화 기능을 추가할 수 있도록 해준다!***
> 

```groovy
implementation 'com.github.ulisesbocchio:jasypt-spring-boot-starter:3.0.5'
```

</aside>

## **기본설정**

<aside>
✍️ **NOTE**

```java
@Configuration
public class JasyptConfig {

    @Value("${jasypt.encryptor.password}")
    private String password;

    @Bean(name = "jasyptEncryptorAES")
    public StringEncryptor stringEncryptor(){

        PooledPBEStringEncryptor encryptor = new PooledPBEStringEncryptor();
        SimpleStringPBEConfig config = new SimpleStringPBEConfig();

        config.setPassword(password);
        config.setAlgorithm("PBEWithMD5AndDES");
        config.setKeyObtentionIterations("1000");
        config.setPoolSize("1");
        config.setProviderName("SunJCE");
        config.setSaltGeneratorClassName("org.jasypt.salt.RandomSaltGenerator");
        config.setIvGeneratorClassName("org.jasypt.iv.NoIvGenerator");
        config.setStringOutputType("base64");
        encryptor.setConfig(config);
        return encryptor;
    }
}
```

```yaml
jasypt:
  encryptor:
    bean: jasyptEncryptorAES
```

</aside>

## 패스워드 외부주입

<aside>
✍️ **NOTE**

```groovy
./gradlew build -Djasypt.encryptor.password=testkey
```

```groovy
java -Djasypt.encryptor.password=testkey -jar your-app.jar
```

```groovy
tasks.named('test') {
	useJUnitPlatform()
	systemProperty 'jasypt.encryptor.password', System.getProperty("jasypt.encryptor.password")
}
```

</aside>