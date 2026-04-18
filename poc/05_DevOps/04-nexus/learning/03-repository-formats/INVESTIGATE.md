# Ch03: 리포지토리 포맷과 구성 — 심화 탐구

> LEARN.md의 개념을 더 깊이 파고드는 Q&A

---

## Q1: RELEASE와 SNAPSHOT의 writePolicy가 다른 이유는?

RELEASE 리포지토리의 writePolicy는 `ALLOW_ONCE`다. 같은 GAV 좌표로 두 번 배포하면 거부된다. 이것은 단순한 규칙이 아니라 **아티팩트 불변성(immutability)의 기술적 강제**에 해당한다.

프로덕션에 `payment-service:1.2.3`이 배포되어 있다고 하자. 누군가 같은 좌표로 내용이 다른 JAR를 덮어쓰면 무슨 일이 생길까? 다른 서비스가 이 라이브러리를 의존하고 있을 때, 동일한 버전 선언에 대해 어제와 오늘 내려오는 바이너리가 다르다. 장애 원인 추적이 불가능해지고, 재현 가능한 빌드라는 개념 자체가 무너진다. 6개월 후 감사팀이 "1.2.3 버전의 바이너리를 제출하세요"라고 하면 어떤 걸 줘야 할지 알 수 없게 된다.

반면 SNAPSHOT은 `ALLOW`로 반복 덮어쓰기를 허용한다. 개발 중에는 같은 버전을 수십 번 빌드하기 때문이다. Nexus는 SNAPSHOT 업로드 시 `1.2.3-20240301.143052-1` 같은 타임스탬프 버전을 내부적으로 생성해서 이전 스냅샷도 보존하되, 클라이언트에게는 항상 최신을 반환한다. 불변성을 포기하는 대신 개발 편의성을 취하는 트레이드오프인 셈이다.

한 가지 추가로 알아둘 것이 있다. `ALLOW`라는 세 번째 Write Policy도 존재한다. 이건 RELEASE든 SNAPSHOT이든 무조건 덮어쓰기를 허용하는 설정인데, 특수한 상황(레거시 마이그레이션 등)에서만 임시로 사용하고 즉시 ALLOW_ONCE로 되돌려야 한다.

---

## Q2: npm scoped package를 Nexus에서 관리할 때 주의할 점은?

핵심은 **install 경로와 publish 경로를 분리**하는 것이다. 여기서 자주 발생하는 실수와 해결법을 정리하자.

**실수 1: publish 경로를 group으로 설정.** group은 읽기 전용이므로 `npm publish`가 `403 Forbidden`으로 실패한다. publish 경로는 반드시 hosted를 직접 가리켜야 한다.

**실수 2: `_auth` 토큰의 URL 경로 불일치.** npm은 URL prefix 매칭으로 인증 정보를 찾는다. `//nexus.example.com/repository/npm-hosted/:_auth=...`에서 경로가 한 글자라도 다르면 인증이 누락된다. 슬래시 하나 차이로 30분을 헤매기도 한다.

**실수 3: `_authToken`과 `_auth`의 혼동.** npm은 두 가지 인증 방식을 지원한다. `_auth`는 `username:password`의 Base64 인코딩이고, `_authToken`은 npm token 기반이다. Nexus는 둘 다 지원하지만, 팀 내에서 하나로 통일하는 것이 관리가 편하다.

CI 환경에서는 `.npmrc`에 비밀번호를 하드코딩하는 대신 환경변수로 주입하는 것이 안전하다:

```bash
# .npmrc (CI용)
//nexus.example.com/repository/npm-hosted/:_auth=${NPM_AUTH_TOKEN}
```

scope가 아닌 일반 패키지(`lodash`, `express`)는 `registry` 설정을 따라 group에서 내려받고, group 안의 proxy가 npmjs.org에서 캐싱한다.

---

## Q3: Docker layer가 이미 존재할 때 push 동작은 어떻게 되나?

Docker는 **content-addressable storage** 구조를 사용한다. 각 layer는 내용의 SHA256 해시가 식별자다. 같은 내용이면 같은 해시, 즉 같은 layer로 인식한다.

`docker push` 과정에서 CLI는 각 layer를 올리기 전에 `HEAD /v2/<name>/blobs/<digest>` 요청으로 해당 layer가 이미 존재하는지 확인한다. 존재하면 업로드를 건너뛴다(skip). 이것이 Docker push가 빠른 이유다.

실무에서 이 메커니즘이 빛나는 순간: `openjdk:17-slim` 기반 이미지를 10개 서비스가 사용한다고 하자. 첫 번째 서비스가 push할 때 base image layer가 올라가고, 나머지 9개는 해당 layer를 전부 skip한다. 실제 전송되는 건 각 서비스의 애플리케이션 코드 layer(보통 수 MB)뿐이다. Blob Store 공간도 절약되고 네트워크 전송량도 줄어든다.

이 구조가 의미하는 중요한 점이 하나 더 있다. Dockerfile에서 **자주 변경되는 명령을 아래로** 배치해야 layer 재사용률이 높아진다. `COPY . /app` 같은 소스 복사가 위에 있으면 소스가 바뀔 때마다 그 아래의 모든 layer가 무효화된다. 의존성 설치(`RUN npm install`) layer를 소스 복사 전에 두면, 의존성이 바뀌지 않는 한 해당 layer는 캐시에서 재사용된다.

---

## Q4: Raw 리포지토리와 S3의 역할 차이는?

겉보기에는 둘 다 "파일을 저장하는 곳"이라 헷갈릴 수 있다. 하지만 설계 목적이 다르다.

**Raw 리포지토리**는 빌드 파이프라인의 일부로서 아티팩트를 관리한다. 버전 관리가 필요하고, Nexus의 보안 모델(Realm, Role, Privilege)로 접근 제어가 되며, proxy/group과 조합할 수 있다. 예를 들어 팀이 사용하는 protoc 바이너리를 Raw hosted에 올려두고, CI에서 `curl`로 다운받아 사용하는 식이다. Cleanup Policy로 오래된 파일을 자동 정리할 수도 있고, Nexus의 감사 로그에 누가 언제 다운로드했는지 기록된다.

**S3(오브젝트 스토리지)**는 범용 데이터 저장소다. 로그, 백업, 미디어 파일, 데이터셋 같은 대용량 비정형 데이터를 저장한다. 라이프사이클 정책으로 자동 삭제하거나 Glacier로 아카이빙하는 것도 S3의 역할이다. 단일 파일 5TB까지 저장 가능하고, 11 nines(99.999999999%)의 내구성을 제공한다.

판단 기준은 간단하다. "이 파일이 빌드/배포 파이프라인에서 사용되는가?" 그렇다면 Raw, 아니라면 S3. Raw에 로그 파일이나 DB 덤프를 넣으면 Blob Store가 급격히 커져서 Nexus 전체 성능에 영향을 준다.

---

## Q5: Content Selector로 특정 groupId만 접근 허용하는 시나리오는?

결제 팀의 내부 라이브러리(`com.mycompany.payment.*`)에 다른 팀이 직접 접근하면 안 되는 상황을 가정하자. API 게이트웨이 라이브러리(`com.mycompany.gateway.*`)만 외부 팀이 사용해야 한다.

Content Selector를 이렇게 만든다:

```
format == "maven2" and path =^ "/com/mycompany/payment/"
```

이 Selector를 `payment-team-access`라는 Privilege에 연결하고, 결제 팀 Role에만 이 Privilege를 부여한다. 다른 팀의 Role에는 이 Privilege가 없으므로 해당 경로에 접근하면 `403`이 반환된다.

역방향도 가능하다. "결제 팀 라이브러리를 제외한 모든 것"에 접근 가능한 Privilege를 만들려면 Content Selector를 부정(negation)으로 쓸 수는 없지만, 허용할 경로를 명시적으로 나열하는 방식으로 우회할 수 있다. 현실적으로는 팀별 리포지토리 분리와 Content Selector를 조합하는 것이 관리하기 편한 접근이다.

주의할 점: Content Selector는 **리포지토리 레벨이 아니라 경로 레벨**의 제어다. 같은 리포지토리 안에서도 경로별로 다른 권한을 적용할 수 있다는 뜻인데, 지나치게 세분화하면 관리가 복잡해진다.

---

## Q6: Routing Rule로 dependency confusion 공격을 방어하는 방법은?

Routing Rule은 proxy 리포지토리에 적용된다. `BLOCK` 모드로 설정하면 매칭되는 경로의 요청을 외부로 보내지 않는다.

dependency confusion 공격의 시나리오는 이렇다. 내부 라이브러리의 groupId가 `com.mycompany`인데, 공격자가 Maven Central에 같은 groupId로 악성 패키지를 올린다. group에서 proxy가 hosted보다 먼저 탐색되거나, hosted에 해당 버전이 아직 없는 시간차가 있으면 공격자의 패키지가 다운로드될 수 있다.

방어는 두 겹으로 한다. 첫째, group 멤버 순서에서 hosted를 proxy보다 앞에 둔다. 둘째, Routing Rule로 proxy에서 `com/mycompany/.*`를 BLOCK한다. 이렇게 하면 설령 hosted에 해당 버전이 없더라도, proxy가 외부에서 해당 네임스페이스의 아티팩트를 가져오지 않는다.

npm에서는 scope(`@mycompany/*`)를 사용하면 dependency confusion 위험이 낮아진다. 공격자가 같은 scope의 패키지를 npmjs.org에 올리려면 해당 scope의 소유권이 필요하기 때문이다. Maven은 groupId에 이런 소유권 검증이 없으므로 Routing Rule이 더 중요하다.

---

## Q7: 포맷별 메타데이터 구조의 차이가 실무에서 왜 중요한가?

빌드 도구는 메타데이터를 기반으로 의존성을 해결한다. 메타데이터 구조를 이해하면 "왜 이 버전이 안 보이지?"라는 문제를 빠르게 진단할 수 있다.

Maven의 `maven-metadata.xml`은 버전 목록과 최신 버전 정보를 담는다. proxy에서 이 파일이 캐시되어 있으면 새로 릴리스된 버전이 안 보일 수 있고, 이때 메타데이터 캐시 무효화가 필요하다.

npm의 메타데이터는 패키지의 전체 버전 히스토리를 담은 JSON 문서다. `https://registry.npmjs.org/lodash` 같은 URL로 조회하면 모든 버전의 `dist-tags`, `versions`, `time` 정보가 반환된다. Nexus proxy가 이 JSON을 캐시하므로, 캐시 유효기간 동안 새 버전이 안 보이는 현상이 Maven과 동일하게 발생한다.

Docker의 메타데이터는 manifest와 tag list다. `GET /v2/<name>/tags/list`로 태그 목록을 조회하고, 특정 태그의 manifest를 가져와서 layer 목록을 확인한다. Docker proxy에서는 태그 목록 캐싱이 이슈가 되는데, `latest` 같은 mutable 태그가 가리키는 digest가 바뀌어도 캐시에 이전 값이 남아 있을 수 있기 때문이다.

---

## 심화: PyPI, NuGet, Go 등 새 포맷을 추가해야 할 때 고려할 점은?

새 포맷을 추가하는 작업 자체는 Nexus UI에서 리포지토리 세 개(hosted + proxy + group)를 만들면 끝이다. 하지만 운영 관점의 고려사항이 있다.

**Blob Store 분리 여부.** 포맷별로 Blob Store를 분리하면 디스크 사용량 모니터링과 백업 정책을 개별 적용할 수 있다. Docker 이미지는 수 GB 단위로 빠르게 쌓이는데, Maven JAR와 같은 Blob Store에 넣으면 디스크 풀 예측이 어렵다. 최소한 Docker는 별도 Blob Store를 사용하는 것을 권장한다.

**Cleanup Policy.** 포맷마다 아티팩트 생명주기가 다르다. SNAPSHOT은 30일 후 삭제, Docker 태그는 최신 N개만 유지, npm prerelease는 7일 후 삭제 같은 정책을 포맷별로 설정해야 Blob Store가 무한히 커지는 것을 방지할 수 있다.

**클라이언트 설정 배포.** 새 포맷의 리포지토리를 만들어도 개발자가 모르면 소용없다. `.npmrc`, `pip.conf`, `settings.xml` 같은 클라이언트 설정 템플릿을 팀 위키나 온보딩 문서에 즉시 반영해야 한다. 이 부분이 누락되면 "Nexus 만들어놨는데 아무도 안 쓴다"는 상황이 반복된다.

**인증 방식 차이.** 포맷마다 인증 메커니즘이 다르다. Maven은 `settings.xml`의 `server` 블록, npm은 `.npmrc`의 `_auth` 토큰, Docker는 Bearer Token Realm, pip는 URL에 인증 정보 포함. 새 포맷을 추가하면 해당 클라이언트의 인증 방식을 파악하고, 필요한 Realm을 활성화해야 한다.
