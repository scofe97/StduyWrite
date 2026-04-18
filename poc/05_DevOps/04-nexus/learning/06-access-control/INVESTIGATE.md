# Ch06. 접근 제어와 인증 - 심화 탐구

---

## Q1. nx-anonymous 기본 권한은 어디까지이고, 보안 위험은 뭘까?

nx-anonymous 역할에는 기본적으로 `nx-healthcheck-read`, `nx-search-read`, 그리고 일부 리포지토리의 `browse`/`read` 권한이 포함되어 있다. 설치 직후 상태에서 Anonymous Access를 켜면, 인증 없이도 리포지토리 목록을 조회하고 컴포넌트를 검색할 수 있다는 뜻이다.

보안 위험은 환경에 따라 달라진다. 사내 네트워크에서만 접근 가능하다면 프록시 리포지토리(Maven Central 캐시 등)에 대한 익명 읽기는 합리적인 선택이다. 개발자가 `settings.xml`에 인증 정보를 넣지 않아도 빌드가 돌아가니 온보딩 비용이 줄어들기 때문이다. 하지만 인터넷에 노출된 인스턴스라면 사내 라이브러리의 바이너리가 외부에 유출될 수 있으므로, Anonymous Access를 비활성화하거나 nx-anonymous에서 hosted 리포지토리 관련 권한을 모두 제거해야 한다.

흔한 실수는 group 리포지토리에 대한 익명 읽기를 허용하는 것인데, group이 hosted를 포함하고 있으면 간접적으로 사내 코드에 접근 가능해진다. 반드시 group의 구성원 리포지토리를 확인하고, 프록시만 포함된 별도 group을 만들어 익명 접근용으로 분리하는 게 안전하다. 예를 들어 `maven-public-anonymous`(proxy만 포함)와 `maven-public`(proxy + hosted) 두 개의 group을 운영하면서, 익명 읽기는 전자에만 허용하는 패턴이다.

---

## Q2. Role 상속이 깊게 중첩되면 어떤 문제가 생길까?

Nexus Pro의 Contained Roles는 역할 안에 역할을 포함할 수 있어서 계층 구조를 만들 수 있다. `base-role` → `team-role` → `lead-role` 같은 2단계 중첩은 관리하기 수월하다.

문제는 3단계 이상부터 시작된다. "이 사용자가 실제로 어떤 권한을 갖는가?"를 파악하려면 역할 트리를 재귀적으로 탐색해야 하는데, UI에서 이를 한눈에 보여주지 않는다. 디버깅이 어려워지는 거다. "왜 이 사용자가 이 리포지토리에 접근 가능하지?"라는 질문에 답하려면 여러 역할을 추적해야 한다.

또 하나의 함정은 순환 참조다. A가 B를 포함하고 B가 A를 포함하면 무한 루프가 발생할 수 있는데, Nexus가 이를 방지하는지 문서상 명확하지 않다. 실무에서는 2단계까지만 중첩하고, 역할 이름에 계층을 명시하는 컨벤션(예: `L1-base-read`, `L2-dev-team`, `L3-dev-lead`)을 쓰면 관리가 수월해진다. 이 컨벤션의 장점은 역할 목록만 봐도 계층 구조가 한눈에 파악된다는 것이다. L1이 가장 기본적인 권한이고 번호가 올라갈수록 추가 권한이 붙는 구조라는 걸 이름만으로 알 수 있다.

역할 상속 디버깅이 필요하다면 API를 활용할 수 있다. `GET /service/rest/v1/security/roles/{roleId}` 응답에 포함된 `roles` 필드가 Contained Roles 목록인데, 이를 재귀적으로 조회하는 스크립트를 만들면 역할 트리를 평탄화(flatten)할 수 있다. 다만 이런 스크립트가 필요하다는 것 자체가 구조가 과하게 복잡하다는 신호이니, 단순화를 먼저 고려하는 게 바람직하다.

---

## Q3. Content Selector로 특정 groupId의 SNAPSHOT만 제한할 수 있을까?

가능하다. CSEL 표현식으로 경로 패턴을 지정하면 된다. Maven에서 groupId는 경로로 변환되므로(예: `com.mycompany` → `/com/mycompany/`), 다음과 같이 작성한다.

```
format == "maven2" and path =^ "/com/mycompany/" and path =~ ".*-SNAPSHOT.*"
```

이 Content Selector를 기반으로 Privilege를 만들고 역할에 할당하면, 해당 역할의 사용자는 `com.mycompany` 그룹의 SNAPSHOT 아티팩트에만 접근할 수 있다. 나머지 groupId의 SNAPSHOT이나 릴리스 버전에는 접근이 차단된다.

주의점이 있는데, Content Selector는 "허용" 방식으로만 동작한다. "이 경로를 차단하고 나머지는 허용"이 아니라 "이 경로만 허용"이다. 따라서 "대부분은 접근 가능하되 특정 경로만 차단"하고 싶다면, 차단 대상을 제외한 모든 경로를 허용하는 식으로 구성해야 하는데 이게 꽤 번거롭다. CSEL에는 NOT 연산자가 없기 때문이다. 이런 경우에는 리포지토리를 분리하는 편이 더 실용적이다.

```
# 부정 조건이 필요한 경우 — 정규식으로 우회
# "/com/secret/"을 제외한 모든 경로 (비권장: 유지보수 어려움)
format == "maven2" and path =~ "^/(?!com/secret/).*"
```

---

## Q4. LDAP 그룹 변경이 Nexus에 즉시 반영되지 않는 이유는?

Nexus는 LDAP 조회 결과를 내부적으로 캐시한다. 매 요청마다 LDAP 서버에 쿼리하면 성능이 떨어지고 LDAP 서버에 부하를 줄 수 있기 때문이다. 기본 캐시 만료 시간은 설정에 따라 다르지만, 보통 수 분에서 수십 분 사이다.

이로 인해 LDAP에서 사용자를 그룹에 추가/제거해도 Nexus에 즉시 반영되지 않는 상황이 발생한다. 퇴사자의 LDAP 계정을 비활성화했는데 캐시 만료 전까지 Nexus에 접근 가능한 보안 위험이 생길 수도 있다.

대응 방법은 세 가지다. 첫째, `Administration → Security → LDAP`에서 캐시 TTL을 짧게 설정(예: 5분)하되 LDAP 서버 부하를 모니터링한다. LDAP 서버의 쿼리 로그를 보면서 부하가 허용 범위 내인지 확인해야 한다. 둘째, Nexus 관리 UI에서 해당 사용자의 캐시를 수동으로 무효화한다. `Administration → Support → System Information`에서 캐시 관련 정보를 확인할 수 있다. 셋째, 긴급 상황에서는 Nexus에서 해당 사용자를 직접 비활성화(Status: Disabled)하여 LDAP 캐시와 무관하게 즉시 차단한다. REST API로도 즉시 비활성화가 가능하다.

```bash
# 사용자 즉시 비활성화
curl -u admin:admin123 -X PUT \
  "http://localhost:8081/service/rest/v1/security/users/target-user" \
  -H "Content-Type: application/json" \
  -d '{"userId":"target-user","status":"disabled","roles":[]}'
```

이 방법이 가장 확실하며, 퇴사 프로세스에 "Nexus 계정 비활성화" 단계를 반드시 포함시켜야 하는 이유이기도 하다.

---

## Q5. Docker Token Realm과 Basic Auth Realm은 어떻게 다를까?

Docker 클라이언트는 레지스트리 인증 시 토큰 기반 프로토콜을 사용한다. `docker login`을 하면 먼저 레지스트리에 접근하고, 401 응답과 함께 `WWW-Authenticate` 헤더에서 토큰 엔드포인트 정보를 받고, 해당 엔드포인트에서 Bearer Token을 발급받아 이후 요청에 사용하는 흐름이다. Docker Token Realm은 이 토큰 발급/검증을 처리한다.

```
흐름: Client → Registry(401) → Token Endpoint(Basic Auth) → Bearer Token 발급 → Registry(Token)
```

Basic Auth Realm은 단순히 매 요청의 Authorization 헤더에서 사용자/비밀번호를 추출하여 검증하는 방식이다. curl이나 REST 클라이언트에서 Nexus API를 호출할 때 주로 사용된다.

Docker 리포지토리를 운영한다면 Docker Token Realm을 반드시 활성화해야 하고, Realm 순서에서 Local Authenticating Realm보다 뒤에 놓는 게 일반적이다. 단, 일부 환경에서는 Docker Token Realm이 Local보다 앞에 있어야 docker login이 정상 동작하는 경우도 보고되니, 동작하지 않으면 순서를 바꿔보는 것도 방법이다. Docker Token Realm이 비활성화된 상태에서의 증상은 독특한데, `docker login`은 성공하지만 `docker push`에서 `unauthorized` 에러가 나는 경우가 대표적이다. 이 에러를 만나면 먼저 `Administration → Security → Realms`에서 Docker Bearer Token Realm이 Active 목록에 있는지 확인하는 것이 가장 빠른 해결책이다.

두 Realm의 인증 흐름을 비교하면 이렇다.

```
Basic Auth:    요청마다 ID/PW → 서버 검증 → 응답
Docker Token:  최초 접근(401) → Token 요청(Basic Auth) → Token 발급 → Token으로 접근
```

Docker Token 방식은 한 번 토큰을 받으면 토큰 만료까지 재인증 없이 사용할 수 있어 효율적이다. 반면 Basic Auth는 매 요청마다 인증 정보를 전송하므로, 네트워크 스니핑에 더 취약한 구조이기도 하다.

---

## Q6. API Token의 생명주기는 어떻게 관리해야 할까?

Nexus Pro의 User Token은 사용자별로 nameCode/passCode 쌍을 생성하며, Basic Auth 대신 이 토큰 쌍을 사용하여 인증한다. 토큰의 생명주기 관리에서 주의할 점이 몇 가지 있다.

토큰은 생성 시점에만 passCode를 확인할 수 있고, 이후에는 조회할 수 없다. 따라서 생성 즉시 안전한 곳(CI 시크릿, Vault 등)에 저장해야 한다. 분실하면 토큰을 폐기하고 새로 발급받아야 하며, 이때 해당 토큰을 사용하던 모든 시스템의 설정도 업데이트해야 한다.

정기 교체(rotation) 정책을 세워야 한다. 90일마다 토큰을 재발급하는 것이 일반적인 관행이다. 자동화하려면 Nexus API로 토큰 재생성을 호출하고, 결과를 시크릿 매니저에 업데이트하는 스크립트를 만들 수 있다. Vault의 dynamic secrets 기능과 연동하면 토큰 교체를 완전 자동화하는 것도 가능하다.

OSS 버전에서는 User Token이 없으므로, 서비스 계정의 비밀번호를 정기적으로 변경하고 CI 시크릿도 함께 업데이트하는 수동 프로세스가 필요하다. 비밀번호 변경 시 CI 파이프라인이 일시적으로 실패할 수 있으니, 변경 절차를 문서화하고 모든 사용처를 목록으로 관리하는 것이 운영 안정성을 위해 필수적이다.

---

## 심화 질문: SAML SSO와 LDAP을 동시에 사용하는 하이브리드 인증은 어떻게 구성할까?

대규모 조직에서는 SSO(SAML/OIDC)로 웹 로그인을 처리하면서도, CLI 도구(Maven, npm, Docker)에서는 LDAP 인증이나 토큰 인증을 사용해야 하는 경우가 흔하다. SAML은 브라우저 리다이렉트 기반이라 CLI에서 직접 사용할 수 없기 때문이다.

하이브리드 구성은 Realm 순서로 해결한다. Local Authenticating → Docker Token → SAML → LDAP 순으로 배치하면, 브라우저 접근은 SAML IdP를 통한 SSO로, CLI 접근은 LDAP 비밀번호나 User Token으로 처리된다. SAML로 인증된 사용자에게 Nexus 역할을 매핑하려면, IdP가 보내는 SAML Assertion의 그룹 속성을 Nexus 역할에 매핑하는 설정이 필요하다.

실제 설정 시에는 IdP 측에서 Nexus를 Service Provider(SP)로 등록해야 한다. Nexus의 SAML 메타데이터 엔드포인트(`/saml/metadata`)에서 SP 설정 XML을 다운받아 IdP에 등록하고, IdP에서 발급하는 Assertion에 그룹 Claim을 포함하도록 구성한다. 이 그룹 Claim의 값이 Nexus 역할 이름과 일치하면 자동 매핑되는 식이다.

이 구성의 복잡도는 상당히 높아서, IdP 설정(속성 매핑, 그룹 Claim), Nexus SAML 설정, LDAP 동기화 세 가지를 동시에 관리해야 한다. 장애 시 원인 파악도 까다로운데, "SAML 인증 실패인가, LDAP 연결 끊김인가, Realm 순서 문제인가"를 구분해야 하기 때문이다. 로그 레벨을 DEBUG로 올려서 Realm별 인증 시도 결과를 확인할 수 있으니, 문제가 발생하면 `${NEXUS_DATA}/log/nexus.log`에서 "realm" 키워드로 검색하는 것이 첫 번째 디버깅 단계다.

도입 전에 "SSO가 정말 필요한가, LDAP만으로 충분하지 않은가"를 먼저 판단하는 게 중요하다. 50명 이하 조직이라면 LDAP 단독 운영이 더 실용적인 경우가 많다. SSO 도입이 정당화되는 시나리오는 "여러 도구(Nexus, Jenkins, SonarQube, GitLab)에 걸쳐 통합 인증이 필요한 경우"이므로, Nexus 단독으로 SSO를 위해 SAML을 도입하는 것은 비용 대비 효과가 낮다.
