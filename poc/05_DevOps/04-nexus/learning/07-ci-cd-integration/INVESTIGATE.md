# Ch07: CI/CD 파이프라인 연동 — 심화 탐구

## Q1: mvn deploy와 nexusArtifactUploader의 차이는 정확히 무엇인가?

`mvn deploy`는 Maven 빌드 라이프사이클의 마지막 단계로, POM 메타데이터(의존성 정보, 부모 POM 관계, 플러그인 설정)를 아티팩트와 함께 업로드한다. Nexus는 이 메타데이터를 인덱싱해서 의존성 해석에 활용한다.

반면 `nexusArtifactUploader`는 Jenkins 플러그인이 Nexus REST API를 직접 호출해서 파일을 업로드하는 방식이다. Maven 프로젝트가 아닌 Go, Rust, Python 등의 빌드 결과물을 raw 리포지토리에 올릴 때 적합하다.

POM 없이도 동작하지만, Maven 의존성 해석에 필요한 메타데이터가 빠지므로 다른 Maven 프로젝트에서 참조하기 어렵다는 한계가 존재한다.

실무적 판단 기준은 간단하다. "이 아티팩트를 다른 Maven 프로젝트에서 의존성으로 쓸 것인가?" 그렇다면 `mvn deploy`, 그렇지 않다면 `nexusArtifactUploader`를 쓰면 된다.

한 가지 주의할 점은 `mvn deploy`가 빌드 라이프사이클 전체를 실행한다는 것이다. 이미 빌드와 테스트를 마친 뒤 배포만 하고 싶다면 `mvn deploy -DskipTests`로 테스트를 건너뛰는 게 맞다.

`maven-deploy-plugin`의 `deployAtEnd` 옵션도 알아두면 유용하다. 멀티 모듈 빌드에서 모든 모듈이 성공한 후에만 한꺼번에 업로드하도록 설정하는 것인데, 중간에 한 모듈이 실패했는데 이미 다른 모듈이 배포된 불완전한 릴리즈를 방지할 수 있다.

---

## Q2: Jenkins Credentials를 환경변수로 노출할 때 보안 위험은?

Jenkins의 `credentials()` 헬퍼는 파이프라인 로그에서 값을 마스킹(****)해주지만, 이것만으로 안전하다고 볼 수 없다.

`sh 'env | sort'`나 `sh 'cat /proc/self/environ'` 같은 명령을 실행하면 환경변수가 평문으로 출력될 가능성이 있다. Jenkins 에이전트의 `/tmp` 디렉토리에 임시 파일로 남을 수도 있다.

마스킹은 Jenkins 콘솔 로그에서만 적용되는 것이지, 프로세스 메모리나 파일시스템에서는 평문 그대로 존재한다는 점을 잊으면 안 된다.

더 위험한 시나리오는 악의적인 PR이다. 공개 리포지토리에서 누군가 Jenkinsfile을 수정하는 PR을 보내고, 그 안에서 환경변수를 외부 서버로 전송하는 코드를 넣으면 시크릿이 유출된다.

이를 방지하려면 Multibranch Pipeline에서 "Trust" 설정을 엄격하게 관리하고, PR 빌드에는 프로덕션 시크릿을 주입하지 않아야 한다. Jenkins의 "Properties Strategy"에서 "Only allow trusted members to modify Jenkinsfile"을 설정하면 외부 기여자의 Jenkinsfile 변경이 차단된다.

HashiCorp Vault 같은 외부 시크릿 매니저를 쓰면 시크릿의 수명을 제한(TTL)하고 감사 로그를 남길 수 있다. Vault의 동적 시크릿을 활용하면 빌드마다 일회용 Nexus 토큰을 생성하고, 빌드 종료 후 자동 폐기하는 것도 가능하다.

---

## Q3: 멀티 모듈 Maven 프로젝트에서 일부 모듈만 deploy하려면?

기본적으로 `mvn deploy`는 모든 모듈을 배포한다. 특정 모듈만 배포하려면 해당 모듈의 `pom.xml`에 `<maven.deploy.skip>true</maven.deploy.skip>`을 설정하면 된다.

또는 `-pl` 플래그로 모듈을 지정할 수 있다.

```bash
mvn deploy -pl module-a,module-b -am
```

`-am`(also-make)은 지정된 모듈의 의존 모듈까지 빌드하되, deploy는 `-pl`에 명시된 모듈만 수행한다. 테스트용 모듈이나 내부 도구 모듈처럼 외부에 공개할 필요 없는 모듈은 이 방식으로 제외하는 것이 일반적이다.

`-pl`과 `<maven.deploy.skip>` 중 어느 쪽이 나을까? 프로젝트 구조가 안정적이고 "이 모듈은 절대 배포하지 않는다"가 확정적이라면 `pom.xml`에 skip을 박아두는 게 실수를 방지한다. 상황에 따라 배포 대상이 바뀐다면 CI 파이프라인에서 `-pl`로 제어하는 편이 유연하다.

주의할 점이 하나 더 있다. CI 환경에서 클린 빌드를 하면서 `-pl`만 지정하면 의존 모듈을 찾지 못해 빌드가 실패할 수 있으니, `-am` 플래그를 반드시 함께 써야 한다.

---

## Q4: Docker push 시 Nexus와 직접 통신 vs nginx proxy 경유의 차이는?

Docker 클라이언트가 Nexus에 직접 통신하면 구성이 단순하지만, TLS 종료를 Nexus가 직접 처리해야 한다. Java keystore(.jks)에 인증서를 넣고 Jetty 설정을 수정해야 하며, 갱신 시마다 Nexus를 재시작해야 한다.

nginx를 앞에 두면 TLS 종료를 nginx가 담당하고, Nexus는 HTTP로만 동작하면 되어 설정이 간결해진다. Let's Encrypt + certbot의 자동 갱신도 nginx 환경에서 자연스럽게 동작한다.

nginx proxy 경유 시 반드시 설정해야 하는 항목이 세 가지 있다.

첫째, `client_max_body_size`를 충분히 크게 잡아야 한다. 기본 1MB는 Docker 이미지에 터무니없이 작으므로 최소 1GB 이상으로 설정한다.

둘째, `proxy_read_timeout`도 대용량 이미지 push 시 60초 기본값으로는 부족할 수 있다. 300~600초로 늘리는 것이 안전하다.

셋째, `chunked_transfer_encoding on` 설정이 필요하다. Docker 클라이언트가 레이어를 chunk 방식으로 전송하기 때문이다. 이 설정이 빠지면 push가 중간에 끊기는 증상이 나타난다.

subdomain 라우팅(`docker-hosted.company.com` → 8082 포트, `docker-group.company.com` → 8083 포트)을 nginx에서 처리하면 Docker 클라이언트가 표준 443 포트만 사용하게 되어 방화벽 설정이 간단해진다.

---

## Q5: SNAPSHOT 자동 정리와 CI 빌드 주기의 관계는?

CI가 매 커밋마다 SNAPSHOT을 배포하면 하루에 수십 개의 아티팩트가 쌓인다. 일주일이면 수백 개, 한 달이면 수천 개다. 이걸 방치하면 디스크가 순식간에 차고, Blob Store compact 작업도 오래 걸리게 된다.

Nexus의 Cleanup Policy에서 "Last Published before 7 days" 같은 규칙을 걸면, 일주일 넘은 SNAPSHOT은 자동 삭제 대상이 된다.

문제는 빌드 주기와 정리 주기가 맞지 않을 때 발생한다. 어떤 모듈은 한 달에 한 번만 빌드되는데, 정리 정책이 7일이면 해당 모듈의 SNAPSHOT이 삭제되어 다른 모듈의 빌드가 깨질 수 있다.

"Last Downloaded" 기준으로 정리하면 이런 문제를 피할 수 있다. 누군가 빌드에서 참조하고 있다면 다운로드 기록이 갱신되므로 삭제 대상에서 제외된다.

권장 전략은 "Last Downloaded 30일 + Last Published 90일" 두 조건을 AND로 결합하는 것이다.

추가로, "Keep latest N versions" 정책도 유용하다. 같은 버전의 이전 빌드만 정리하고 최신 빌드는 남기는 방식이다. Nexus의 Cleanup Policy는 리포지토리별로 다르게 설정할 수 있으니, 빌드 주기가 다른 리포지토리에는 각각 다른 정책을 적용해야 한다.

---

## Q6: GitLab CI에서 .npmrc를 안전하게 관리하는 방법은?

GitLab CI에서는 `.npmrc`를 커밋하지 않고, CI 변수로 인증 토큰을 주입하는 패턴이 표준이다.

```yaml
before_script:
  - echo "//nexus.company.com/repository/npm-hosted/:_auth=${NPM_AUTH}" >> .npmrc
```

`${NPM_AUTH}`는 GitLab의 CI/CD Variables에서 "Protected + Masked" 옵션으로 등록한다.

"Protected"로 설정하면 protected 브랜치(main, release)에서만 접근 가능하므로, feature 브랜치의 악의적인 코드가 토큰을 탈취하는 것을 방지할 수 있다.

"Masked"는 CI 로그에서 해당 값이 `[MASKED]`로 치환된다. 다만 base64 인코딩된 값에서만 제대로 동작하는 제약이 있으므로 토큰 형식을 확인해야 한다.

`.npmrc`를 리포지토리에 커밋하되 인증 부분만 환경변수로 참조하는 방식도 있다. npm은 `.npmrc`에서 `${NPM_AUTH}`처럼 환경변수 참조를 지원한다.

하지만 `.npmrc`에 `_auth`가 직접 들어가 있는 걸 실수로 커밋하는 사고가 반복적으로 발생하므로, CI에서 동적으로 생성하는 편이 더 안전하다. `.gitignore`에 `.npmrc`를 추가하는 것도 방어 수단이 되지만, 이미 tracking 중인 파일에는 `.gitignore`가 적용되지 않는다.

npm 7+ 환경이라면 `npm config set`을 CI 스크립트에서 호출하는 방식도 깔끔하다. `npm config set //nexus.company.com/repository/npm-hosted/:_auth "$NPM_AUTH" --location=project`는 프로젝트 레벨 `.npmrc`를 생성하되, 값은 환경변수에서 가져온다.

---

## 심화 질문

> 모노레포에서 여러 포맷(Maven + npm + Docker)을 하나의 파이프라인으로 관리하는 패턴은?

핵심은 "변경 감지 + 선택적 배포"다. 모노레포에서 모든 커밋마다 전체를 빌드하고 배포하면 시간 낭비이자 불필요한 아티팩트가 쌓인다.

`git diff --name-only HEAD~1`로 변경된 경로를 감지해서, backend/ 변경 시 Maven deploy, frontend/ 변경 시 npm publish, infra/ 변경 시 Docker push를 선택적으로 실행하는 것이 기본 전략이다.

Jenkins의 `changeset` 조건이나 GitHub Actions의 `paths` 필터가 이 용도로 쓰인다. 하지만 공통 라이브러리 변경 시 의존하는 모든 모듈을 빌드해야 하므로 의존성 그래프를 파이프라인에 반영하는 추가 작업이 필요하다.

Nx, Turborepo, Bazel 같은 모노레포 빌드 도구가 이 의존성 추적을 자동으로 해주므로, 규모가 커지면 이런 도구 도입을 검토해야 한다.

인증 관리 측면에서는 Maven, npm, Docker 각각의 인증 정보를 별도 시크릿으로 분리하되, 서비스 계정은 하나로 통합하는 것이 관리 부담을 줄여준다. Nexus에서 "nx-deploy" 같은 전용 역할을 만들고 필요한 리포지토리에만 쓰기 권한을 부여하면 된다.

버전 관리도 도전적인 부분이다. Maven은 `pom.xml`에, npm은 `package.json`에, Docker는 태그에 버전이 있다. Git 태그를 단일 버전 소스(single source of truth)로 삼고, CI에서 태그를 파싱하여 각 포맷의 버전에 주입하는 패턴이 일반적이다.
