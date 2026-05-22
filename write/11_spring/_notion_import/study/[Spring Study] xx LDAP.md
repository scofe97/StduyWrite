# [Spring Study] xx. LDAP

주제: Spring Study

[알아두면 쓸데있는 LDAP | 인사이트리포트 | 삼성SDS](https://www.samsungsds.com/kr/insights/ldap.html)

[LDAP 간단소개](https://hmdev.vercel.app/LDAP-간단소개)

[[ LDAP ] LDAP(Lightweight Directory Access Protocol)](https://velog.io/@duck-ach/LDAP-LDAPLightweight-Directory-Access-Protocol에-대하)

# LDAP(Lightweight Directory Access Protocol)

---

<aside>
💡 **NOTE**

> *네트워크 상에서 조직이나 개인정보 혹은 파일이나 디바이스 정보 등을 찾아보는 것을 가능하게 하는 프로토콜*
> 

LDAP는 네트워크 상의 디렉토리 서비스 표준인 X.500의 DAP(Directory Access Protocol)을 기반으로 경량화된 버전이다.

- DAP는 OSI전체 프로토콜 스택을 지원하며 운영에 많은 컴퓨팅 자원을 필요로하는 아주 무거운 프로토콜
- LDAP는 DAP의 복잡성을 줄이고 TCP/IP 레이어에서 더 적은 비용으로 DAP의 많은 기능적인 부분을 조작할 수 있도록 설계

### 특징

**디렉토리 서비스**

- 이름을 기준으로 대상을 조회하거나 편집할 수 있는 서비스
- DNS도 일종의 디렉토리 서비스의 일종
- 디렉토리 안에는 연락처, 사용자, 파일 code 등 무엇이든 넣을 수 있고, insert, update 보다는 검색 요청에 특화되어 있다.

**Lightweight**

- 사용하기 간편하다는 의미보다는 통신 네트워크 대역폭 상의 가벼움을 의미한다.
- 데이터를 조금만 주고 받아도 되게끔 설계되어 있다.

**검색에 특화**

- LDAP의 요청 99%는 검색에 대한 요청을 한다.
- 검색에 특화되다 보니, Transaction이나 Rollback이 없고, 복잡한 관계 등을 설정할 수 없다.

Binary Protocol

- ANS.1 이라는 언어로 메시지를 표현
- 메시지를 BER라는 포멧으로 Incoding하여 주고받음
- Binary Protocol은 Compact하지만 해석하기 쉽고, 내부적으로 처리되는 것이므로 상세하게 몰라도된다.
</aside>

## LDAP의 구조

<aside>
✍️ **NOTE**

> *LDAP는 디렉토리, 엔트리, 속성, 스키마라는 주요 구성요소를 가집니다!*
> 

![LDAP 구조](%5BSpring%20Study%5D%20xx%20LDAP/Untitled.png)

LDAP 구조

```yaml
dn: cn=John Doe,dc=example,dc=com
cn: John Doe
givenName: John
sn: Doe
telephoneNumber: +1 888 555 6789
telephoneNumber: +1 888 555 1232
mail: john@example.com
manager: cn=Barbara Doe,dc=example,dc=com
objectClass: inetOrgPerson
objectClass: organizationalPerson
objectClass: person
objectClass: top
```

- **DC(Domain Component): 도메인 구성요소**
- **DN(Distinguished Name): 모인 Entry를 바탕으로 사용자를 구분할 수 있는 고유의 트리 이름**
- **CN(Common Name): 일반이름**
- SN(Sir Name): (이름의) 성
- C(Country Name): 국가명
- ST(State Province Name): 주(도) 명
- L(Locality Name): 도시, 특정 지역 단위명
- O(Organization): 조직 명
- **OU(Organization Unit Name): 조직 부서 명**
- UID(User ID): 유저 아이디
</aside>

## Information 모델

<aside>
✍️ **NOTE**

> *LDAP의 정보 모델은 디렉터리 내에 저장된 데이터 형식과 구성을 정의합니다.*
> 

![Untitled](%5BSpring%20Study%5D%20xx%20LDAP/Untitled%201.png)

### 엔트리(entry)

- 디렉토리의 기본 정보 단위이다.
- ex) 사용자, 그룹, 리소스 등을 나타내며 각 엔트리는 여러 개의 속성을 가질 수 있다.

### 속성(attribute)

- 엔트리에 대한 구체적인 정보를 나타낸다.
- 각 속성은 속성 타입과, 하나 이상의 속성 값을 가진다.
- ex) `cn`, `mail`, `telephoneNumber`

### ObjectClass

- LDAP 엔트리의 유형을 정의합니다.
- ex) `inetOrgPerson`(`organizationPerson`, `person` - `ObjectClasses` 확장)
- 엔트리는 하나 이상의 ObjectClass 속성을 가질 수 있습니다.

### Schema

- 디렉토리 서비스에서 사용할 수 있는 모든 ObjectClass와 Attributes의 타입을 정의합니다.
- ex) Arrtibutes 정의 - cn, mail
- ex) ObjectClass 정의
- 규칙과 매칭 규칙: 데이터의 형식과 속성 값들이 어떻게 비교되어야 하는지에 대한 규칙을 정의한다.
</aside>

## Naming 모델

<aside>
✍️ **NOTE**

> *LDAP의 명명 모델은 디렉토리 내의 엔트리들을 식별하고 구조화하는 방법을 정의합니다. 디렉토리 내의 모든 엔트리에 고유한 이름을 부여하는 매커니즘을 제공합니다.*
> 

### RDN

- DN의 일부로, 특정 부모 엔트리 내에서 엔트리를 고유하게 식별하는 이름입니다.
- ex) `cn=John Doe`는 해당 엔트리의 RDN으로,. 자신이 속한 조직 내에서 고유합니다.

### DN

- 디렉토리 내에서 엔트리를 고유하게 식별하는 전체 이름입니다.
- **RDN값들을 이어 붙여 생성된 고유한 문자를 DN이라 부릅니다.**
- DN은 LDAP 디렉터리 계층적 구조를 반영하여, 엔트리가 속한 경로를 포함합니다.
- ex) `cn=John Doe, ou=People, dc=example.dc=com`은 [example.com](http://example.com) 도메인 내의 People조직에 속한 Job Doe 사용자를 가리킵니다.
</aside>

## Functinoal 모델

<aside>
✍️ **NOTE**

> *LDAP는 다양한 종류의 연산과 행동을 설명합니다.*
> 

### 질문 작업

- Search: 주어진 조건에 맞는 Entry 도출
- Compare: 특정 Entry의 속성 값 비교

### 갱신 작업

- Add: 디렉토리에 신규 Entry 추가
- Delete: 디렉토리에 기존 Entry 삭제
- Modify: 디렉토리에 기존 Entry 수정 및 Entry DN값 변경

### 인증 밎 제어 작업

- Bind: 디렉토리 서버 연결 시 사용자 인증
- Unbind: 디렉토리 서버와의 연결 해제
- Abandon: 이전 요청 명령을 취소
</aside>

## Security 모델

<aside>
✍️ **NOTE**

> LDAP 디렉토리 서비스의 보안 측면을 다루며, 데이터의 무결성과 기밀성, 접근제어를 보장하는 매커니즘을 포함합니다.
> 
- 인증: 클라이언트가 자신의 정체성을 설명하며 익명인증, 패스워드, SASL 매커니즘을 지원합니다.
- 암호화: 데이터의 기밀성을 위해 TLS를 사용해 데이터를 암호화합니다.
- 접근 제어: 특정 그룹이나 사용자에 접근하는 권한을 제어합니다.
</aside>

# LDAP와 관계형 데이터베이스

LDAP을 이용한 디렉토리 서버도 데이터를 저장하는 DB의 유형이지만 RDB와는 구조와 용도에 많은 차이가 있습니다.

RDB

- 행과 열의 형태로 구성된 테이블에 데이터를 저장하고 서로 다른 테이블들과의 관계를 통해 결과를 도출합니다
- 여러 데이터, 테이블들의 관계를 통해 필요한 데이터를 종합적으로 가져오는 복합적 처리

LADP

- 데이터가 트리 구조로 이루어진 계층형 데이터베이스이다.
- 각 Entry, Attribue로 이루어진 데이터들과 함께 하위에 여러 자식 Entry를 가지는 그룹 형태를 반복해 트리와 같은 계층 형태의 데이터로 표현할 수 있다.
- 데이터를 신속하게 조회/ 단순 쿼리용 작업에 특화되며 수정작업에 대해서는 RDB 보다 안정성이 떨어진다.
- 트랜잭션, 유효성 검사가 제한적이라 읽기 작업에 많이 쓰인다.

계층 구조를 통해 검색/읽기 작업에 특화된다. 데이터가 위치한 계층에 접근해 필요한 데이터를 바로 꺼내고, 같은 계층의 같은 성격을 가진 데이터의 속성과 스키마 설정을 통해 보다 상세히 비교할 수 있다.

# LDAP + Springboot

---

## 1. docker-compose를 통해 로컬에 ldap 세팅

```yaml
version: "3.8"

services:
  openldap:
    image: osixia/openldap:latest
    container_name: openldap
    ports:
      - "389:389"
      - "636:636"
    volumes:
      - ./data/certificates:/container/service/slapd/assets/certs
      - ./data/slapd/database:/var/lib/ldap
      - ./data/slapd/config:/etc/ldap/slapd.d
    environment:
      LDAP_LOG_LEVEL: "256"
      LDAP_ORGANISATION:
      
      LDAP_DOMAIN: "tps.com"
      LDAP_ADMIN_USERNAME: "admin"
      LDAP_ADMIN_PASSWORD: "admin"
      LDAP_CONFIG_PASSWORD: "config"
      
      LDAP_BASE_DN: "dc=tps,dc=com"
      
      LDAP_TLS_CRT_FILENAME: "ldap.crt"
      LDAP_TLS_KEY_FILENAME: "ldap.key"
      LDAP_TLS_CA_CRT_FILENAME: "example.com.ca.crt"
      LDAP_READONLY_USER: "true"
      LDAP_READONLY_USER_USERNAME: "readonly"
      LDAP_READONLY_USER_PASSWORD: "readonly"
    networks:
      - openldap

  phpldapadmin:
    image: osixia/phpldapadmin:latest
    container_name: phpldapadmin
    hostname: phpldapadmin
    ports:
      - "8080:80"
    environment:
      PHPLDAPADMIN_LDAP_HOSTS: "openldap"
      PHPLDAPADMIN_HTTPS: "false"
    depends_on:
      - openldap
    networks:
      - openldap

networks:
  openldap:
    driver: bridge
```

![스크린샷 2024-03-21 오전 10.03.02.png](%5BSpring%20Study%5D%20xx%20LDAP/%25E1%2584%2589%25E1%2585%25B3%25E1%2584%258F%25E1%2585%25B3%25E1%2584%2585%25E1%2585%25B5%25E1%2586%25AB%25E1%2584%2589%25E1%2585%25A3%25E1%2586%25BA_2024-03-21_%25E1%2584%258B%25E1%2585%25A9%25E1%2584%258C%25E1%2585%25A5%25E1%2586%25AB_10.03.02.png)

## 2. 자바 설정

### 의존성 설치

```yaml
implementation 'org.springframework.boot:spring-boot-starter-data-ldap'
```

### 연결 서버 세팅

```java
import javax.naming.directory.Attributes;
import org.springframework.ldap.core.AttributesMapper;
import org.springframework.ldap.core.LdapTemplate;
import org.springframework.ldap.core.support.LdapContextSource;

import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class LDAPService {

		public List<String> getAllGroups() {
				// 접근 하려하는 서버 정보 
		    LdapContextSource contextSource = new LdapContextSource();
		    contextSource.setUrl("ldap://localhost:389");
		    contextSource.setUserDn("cn=admin,dc=tps,dc=com");
		    contextSource.setPassword("admin");
		    contextSource.setBase("dc=tps,dc=com");
		    contextSource.afterPropertiesSet();
		
		    LdapTemplate ldapTemplate = new LdapTemplate(contextSource);
		
		
		    return ldapTemplate.search("ou=group",
							  // 전체 조회
		            "cn=*",
		            new GroupAttributesMapper());
		}
		
		// 그룹 정보를 매핑하는 Mapper 클래스
		private static class GroupAttributesMapper implements AttributesMapper<String> {
		    @Override
		    public String mapFromAttributes(Attributes attributes) throws javax.naming.NamingException {
		        // 그룹 이름을 가져와서 리턴
		        return (String) attributes.get("cn").get();
		    }
		}
}
```

## **LdapQueryBuilder & LdapTemplate**

<aside>
✍️ **NOTE**

> ***LdapQueryBuilder**는 LDAP 검색을 위한 쿼리를 구성하는데 사용되며, 검색 필터를 작성할 수 있게 해주는 빌더 패턴을 제공합니다. **LdapTemplate**는 Spring LDAP의 핵심 클래스로 LDAP 연산을 수행하기 위한 메소드를 제공합니다.*
> 

```java
// "cn" 속성이 "John Doe"인 엔트리 검색
LdapQuery query1 = LdapQueryBuilder.query()
    .where("cn").is("John Doe");

// "cn" 속성이 "John"으로 시작하는 엔트리 검색
LdapQuery query2 = LdapQueryBuilder.query()
    .where("cn").startsWith("John");

// "mail" 속성이 NULL이 아닌 엔트리 검색
LdapQuery query3 = LdapQueryBuilder.query()
    .where("mail").isNotNull();

// "objectclass"가 "person"이고 "cn" 속성이 "John Doe" 또는 "Jane Doe"인 엔트리 검색
LdapQuery query4 = LdapQueryBuilder.query()
    .where("objectclass").is("person")
    .and("cn").is("John Doe")
    .or("cn").is("Jane Doe");

// "objectclass"가 "person"이고 "cn" 속성이 "John Doe"이 아닌 엔트리 검색
LdapQuery query5 = LdapQueryBuilder.query()
    .where("objectclass").is("person")
    .not("cn").is("John Doe");

// "cn" 속성이 "John*" 패턴과 일치하는 엔트리 검색
LdapQuery query6 = LdapQueryBuilder.query()
    .where("cn").like("John*");

// "age" 속성 값이 30보다 큰 엔트리 검색
LdapQuery query7 = LdapQueryBuilder.query()
    .where("age").greaterThan(30);

// "dateOfBirth" 속성 값이 1990년부터 2000년 사이인 엔트리 검색
LdapQuery query8 = LdapQueryBuilder.query()
    .where("dateOfBirth").within(1990, 2000);
```

```java
public void searchExample() {
    LdapQuery query = query()
        .where("objectclass").is("person")
        .and("cn").is("John Doe");

    List<Person> result = ldapTemplate
	    .search(query, new PersonAttributesMapper());
}
```

```java
// 엔트리 추가
DirContextOperations context = new DirContextAdapter(
    LdapNameBuilder.newInstance()
        .add("ou", "users")
        .add("cn", "John Doe")
        .build());

context.setAttributeValues(
    "objectclass",
    new String[] {"top", "person", "organizationalPerson", "inetOrgPerson"});
context.setAttributeValue("cn", "John Doe");
context.setAttributeValue("sn", "Doe");
context.setAttributeValue("mail", "johndoe@example.com");

ldapTemplate.bind(context);
```

```java
// cn이 John Doe인 엔트리의 메일 주소 변경
ContextModifications modifications = new ContextModifications();
modifications.modifyAttributes(
    "cn=John Doe,ou=users",
    new ModificationItem[] {
        new ModificationItem(DirContext.REPLACE_ATTRIBUTE, new BasicAttribute("mail", "newemail@example.com"))
    });

ldapTemplate.modifyAttributes(modifications);
```

```java
// cn이 John Doe인 엔트리 삭제
ldapTemplate.unbind("cn=John Doe,ou=users");
```

</aside>