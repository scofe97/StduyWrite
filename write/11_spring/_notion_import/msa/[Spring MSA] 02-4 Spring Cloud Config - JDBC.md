# [Spring MSA] 02-4. Spring Cloud Config - JDBC

주제: Spring MSA

- 참고
    
    

# Spring Cloud Config

---

<aside>
💡 **NOTE**

> 
> 

```yaml
spring:
	# jdbc 백엔드 활성화
  profiles:
    active: jdbc
  # 데이터 소스 설정  
  datasource:
    url: jdbc:mysql://localhost:3306/configdb
    username: root
    password: root
    driver-class-name: com.mysql.cj.jdbc.Driver

	# Spring Cloud ConfigServer가 데이터베이스 설정 값 조사
	# Application(요청 애플리케이션 이름), Profile(요청 서버 프로파일 이름), Label(요청 레이블)
  cloud:
    config:
      server:
        jdbc:
          sql: SELECT KEY, VALUE from PROPERTIES where APPLICATION=? and PROFILE=? and LABEL=?
```

```sql
# 스키마 지정(변경 가능)
USE configdb;

# 테이블 이름 지정(변경 가능)
CREATE TABLE PROPERTIES (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    APPLICATION VARCHAR(50),
    PROFILE VARCHAR(50),
    LABEL VARCHAR(50) DEFAULT 'master',
    KEY VARCHAR(100),
    VALUE VARCHAR(1000)
);

# 조회 쿼리
SELECT KEY, VALUE
	FROM PROPERTIES
 WHERE APPLICATION=?
	 AND PROFILE=?
	 AND LABEL=?
```

```yaml

```

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