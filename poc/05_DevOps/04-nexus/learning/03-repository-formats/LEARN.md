# Ch03: 리포지토리 포맷과 구성

> **핵심 질문**: 20개 넘는 포맷 중 실무에서 꼭 알아야 할 것은?

---

## 1. Nexus가 지원하는 포맷 전체 목록

Nexus 3은 20개 이상의 포맷을 지원한다. 전부 알 필요는 없고, 자기 팀이 쓰는 포맷만 깊이 이해하면 된다. 하지만 전체 그림을 보는 건 의미가 있다.

| 분류 | 포맷 | 용도 |
|------|------|------|
| **JVM** | Maven, Gradle (maven 포맷) | JAR, WAR, POM |
| **JavaScript** | npm | node_modules |
| **Python** | PyPI | wheel, sdist |
| **Container** | Docker | OCI/Docker 이미지 |
| **.NET** | NuGet | .NET 패키지 |
| **Go** | Go | Go 모듈 |
| **Ruby** | RubyGems | gem |
| **Linux** | yum (RPM), apt (DEB) | OS 패키지 |
| **Helm** | Helm | K8s chart |
| **범용** | Raw | 아무 파일 (바이너리, 설정, 문서) |
| **기타** | Conan (C++), R, Conda, Bower, GitLFS 등 | 특화 생태계 |

이 중 실무에서 80% 이상의 팀이 사용하는 건 **Maven, npm, Docker, Raw** 네 가지다. 이 네 포맷을 제대로 구성할 줄 알면 대부분의 요구사항을 커버할 수 있다.

## 2. Maven: JVM 생태계의 표준

### 2.1 GAV 좌표 체계

Maven의 핵심은 **GAV(GroupId, ArtifactId, Version)** 좌표다. 이 세 가지로 지구상의 모든 Java 아티팩트를 유일하게 식별한다.

```
com.example:payment-service:1.2.3
     G              A          V
```

여기에 추가로 **classifier**와 **packaging**이 붙기도 한다. `com.example:payment-service:1.2.3:sources:jar`처럼. classifier는 같은 GAV에서 변형본(sources, javadoc, tests)을 구분하고, packaging은 파일 형식(jar, war, pom)을 나타낸다. 실무에서 흔히 보는 패턴은 이렇다:

```
payment-service-1.2.3.jar           → 메인 아티팩트
payment-service-1.2.3-sources.jar   → 소스 코드 (디버깅용)
payment-service-1.2.3-javadoc.jar   → API 문서
payment-service-1.2.3.pom           → 의존성 선언 (POM)
payment-service-1.2.3.jar.sha1      → 체크섬
```

Nexus는 이 좌표를 디렉토리 구조로 변환해서 저장한다. groupId의 `.`이 `/`로 바뀌고, artifactId가 디렉토리, version이 하위 디렉토리가 되는 규칙이다:

```
# GAV: com.example:payment-service:1.2.3
# 실제 저장 경로:
com/example/payment-service/1.2.3/payment-service-1.2.3.jar
com/example/payment-service/1.2.3/payment-service-1.2.3.pom
com/example/payment-service/1.2.3/payment-service-1.2.3.jar.sha1
com/example/payment-service/1.2.3/payment-service-1.2.3.jar.md5

# 멀티모듈 프로젝트 예시:
# com.example:payment-api:1.2.3
com/example/payment-api/1.2.3/payment-api-1.2.3.jar

# com.example:payment-domain:1.2.3
com/example/payment-domain/1.2.3/payment-domain-1.2.3.jar

# 메타데이터 (버전 목록)
com/example/payment-service/maven-metadata.xml
```

이 경로 매핑 규칙을 아는 것이 왜 중요할까? 트러블슈팅 때문이다. "빌드에서 아티팩트를 못 찾겠다"는 문제가 생기면, GAV를 경로로 변환해서 Nexus에 직접 조회할 수 있다. 브라우저에서 `https://nexus.example.com/repository/maven-public/com/example/payment-service/1.2.3/`을 열면 해당 버전의 파일 목록이 보인다.

```mermaid
graph LR
    GAV["com.example<br/>:payment-service<br/>:1.2.3"] --> PATH["com/example/<br/>payment-service/<br/>1.2.3/"]
    PATH --> JAR["payment-service<br/>-1.2.3.jar"]
    PATH --> POM["payment-service<br/>-1.2.3.pom"]
    PATH --> SHA["*.sha1, *.md5"]

    style GAV fill:#e3f2fd,stroke:#1565C0,color:#333
    style PATH fill:#fff9c4,stroke:#F9A825,color:#333
    style JAR fill:#c8e6c9,stroke:#2E7D32,color:#333
    style POM fill:#c8e6c9,stroke:#2E7D32,color:#333
    style SHA fill:#f3e5f5,stroke:#7B1FA2,color:#333
```

`maven-metadata.xml`은 해당 아티팩트의 모든 버전 목록을 담고 있다. 빌드 도구가 "최신 버전이 뭐지?"를 판단할 때 이 파일을 참조한다. SNAPSHOT의 경우 타임스탬프 정보도 여기 들어간다.

### 2.2 RELEASE vs SNAPSHOT

이 구분을 제대로 이해하지 않으면 배포에서 사고가 난다.

**RELEASE**는 불변(immutable)이다. `1.2.3` 버전을 한번 올리면 같은 좌표로 다시 올릴 수 없다. 왜 이런 제약을 둘까? 프로덕션에 배포된 `1.2.3`이 내일 달라지면 아무도 믿을 수 없기 때문이다. "어제 빌드한 1.2.3이랑 오늘 빌드한 1.2.3이 다르다"는 상황은 재현 불가능한 빌드를 의미한다.

**SNAPSHOT**은 가변(mutable)이다. `1.2.3-SNAPSHOT`은 개발 중인 버전이며, 같은 좌표로 몇 번이든 덮어쓸 수 있다. Nexus는 SNAPSHOT 업로드 시 타임스탬프를 붙여서 이전 버전도 보존하는데, 클라이언트는 항상 최신 SNAPSHOT을 가져간다. 예를 들어 `1.2.3-SNAPSHOT`을 세 번 deploy하면 내부적으로는 이런 파일이 생긴다:

```
payment-service-1.2.3-20240301.091200-1.jar   # 첫 번째
payment-service-1.2.3-20240301.143052-2.jar   # 두 번째
payment-service-1.2.3-20240302.083015-3.jar   # 세 번째 (최신)
```

클라이언트가 `1.2.3-SNAPSHOT`을 요청하면 `maven-metadata.xml`에서 가장 최근 타임스탬프를 찾아 세 번째 파일을 반환한다.

이것이 Nexus 리포지토리 설정에서 **Version Policy**와 **Write Policy**로 반영된다:

| 리포지토리 | Version Policy | Write Policy | 용도 |
|-----------|---------------|-------------|------|
| maven-releases | Release | ALLOW_ONCE | 릴리스 아티팩트 |
| maven-snapshots | Snapshot | ALLOW | 개발 중 아티팩트 |
| maven-central (proxy) | Release | — | 외부 캐싱 |

**Layout Policy**도 있다. `Strict`으로 설정하면 GAV 좌표와 저장 경로가 일치하지 않는 아티팩트를 거부한다. `Permissive`는 불일치를 허용하지만, 잘못된 경로에 아티팩트가 올라가면 빌드 도구가 찾지 못하므로 Strict이 기본이자 권장이다.

### 2.3 settings.xml 설정

개발자 머신과 CI 서버에서 Nexus를 바라보게 하려면 `~/.m2/settings.xml`을 설정해야 한다:

```xml
<settings>
  <mirrors>
    <mirror>
      <id>nexus</id>
      <mirrorOf>*</mirrorOf>
      <url>https://nexus.example.com/repository/maven-public/</url>
    </mirror>
  </mirrors>
  <servers>
    <server>
      <id>nexus-releases</id>
      <username>deploy-user</username>
      <password>deploy-pass</password>
    </server>
    <server>
      <id>nexus-snapshots</id>
      <username>deploy-user</username>
      <password>deploy-pass</password>
    </server>
  </servers>
  <profiles>
    <profile>
      <id>nexus</id>
      <repositories>
        <repository>
          <id>central</id>
          <url>https://nexus.example.com/repository/maven-public/</url>
          <releases><enabled>true</enabled></releases>
          <snapshots><enabled>true</enabled></snapshots>
        </repository>
      </repositories>
    </profile>
  </profiles>
  <activeProfiles>
    <activeProfile>nexus</activeProfile>
  </activeProfiles>
</settings>
```

`mirrorOf: *`는 "모든 원격 저장소 요청을 이 미러로 보내라"는 뜻이다. Maven Central 뿐 아니라 POM에 선언된 모든 저장소가 Nexus를 거치게 된다. `server` 블록의 `id`는 `pom.xml`의 `distributionManagement`에 선언된 리포지토리 `id`와 일치해야 인증이 적용된다.

Gradle을 쓰는 팀이라면 `build.gradle.kts`에서 설정한다:

```kotlin
repositories {
    maven {
        url = uri("https://nexus.example.com/repository/maven-public/")
        credentials {
            username = project.findProperty("nexusUser") as String? ?: "anonymous"
            password = project.findProperty("nexusPass") as String? ?: ""
        }
    }
}

publishing {
    repositories {
        maven {
            name = "nexus"
            val releasesUrl = uri("https://nexus.example.com/repository/maven-releases/")
            val snapshotsUrl = uri("https://nexus.example.com/repository/maven-snapshots/")
            url = if (version.toString().endsWith("SNAPSHOT")) snapshotsUrl else releasesUrl
            credentials {
                username = project.findProperty("nexusUser") as String?
                password = project.findProperty("nexusPass") as String?
            }
        }
    }
}
```

## 3. npm: JavaScript 생태계

### 3.1 Scoped Package

npm에는 **scope**라는 개념이 있다. `@mycompany/utils` 같은 패키지명에서 `@mycompany`가 scope다. 내부 라이브러리를 관리할 때 scope를 사용하면 공개 패키지와 이름이 충돌할 일이 없다.

Nexus에서 scope 패키지를 관리하려면 `.npmrc` 설정이 필요하다. 이 파일의 구성이 직관적이지 않아서 실수가 잦으므로, 단계별로 설명한다.

```bash
# === .npmrc 완전한 예제 ===

# 1) 기본 레지스트리: 모든 패키지의 install 경로 → group
registry=https://nexus.example.com/repository/npm-group/

# 2) @mycompany scope의 publish 경로 → hosted
#    group에는 publish 불가(읽기 전용), 반드시 hosted 직접 지정
@mycompany:registry=https://nexus.example.com/repository/npm-hosted/

# 3) hosted에 대한 인증 (Base64 인코딩된 user:pass)
//nexus.example.com/repository/npm-hosted/:_auth=ZGVwbG95LXVzZXI6ZGVwbG95LXBhc3M=

# 4) group에서 다운로드할 때도 인증이 필요한 경우 (private hosted 포함)
//nexus.example.com/repository/npm-group/:_auth=ZGVwbG95LXVzZXI6ZGVwbG95LXBhc3M=

# 5) SSL 인증서 검증 (사설 CA 사용 시)
# strict-ssl=false  ← 프로덕션에서는 사용 금지, 테스트용만
# cafile=/path/to/ca-cert.pem  ← 사설 CA 사용 시 이 방식 권장

# 6) npm audit 설정 (proxy에서 audit API 프록시가 안 되면)
# audit=false  ← 보안 관점에서 비추, 가급적 audit 동작하게 구성
```

`_auth` 토큰 생성 방법:

```bash
echo -n 'deploy-user:deploy-pass' | base64
# 출력: ZGVwbG95LXVzZXI6ZGVwbG95LXBhc3M=
```

여기서 주의할 점이 있다. `registry` 설정은 **install(다운로드)** 경로이고, `@mycompany:registry`는 **publish(업로드)** 경로다. group에는 publish할 수 없으니(group은 읽기 전용), publish 경로는 반드시 hosted를 직접 가리켜야 한다.

흔한 실수 두 가지가 있다. 첫째, `_auth` 토큰의 URL 경로가 registry와 정확히 일치하지 않는 것. npm은 URL prefix 매칭으로 인증 정보를 찾으므로, 경로가 한 글자라도 다르면 인증이 누락된다. 둘째, 프로젝트 루트의 `.npmrc`와 홈 디렉토리의 `~/.npmrc`가 충돌하는 것. npm은 두 파일을 병합하는데, 같은 키가 있으면 프로젝트 루트가 우선한다.

### 3.2 npm audit과 Nexus

`npm audit`은 취약점 데이터베이스를 조회하는데, 이 요청도 Nexus proxy를 거친다. Nexus가 npmjs.org의 `/-/npm/v1/security/advisories` 엔드포인트를 프록시하지 못하면 audit이 실패할 수 있다. npm audit 전용 proxy를 별도로 구성하거나, `audit=false`로 비활성화하는 팀도 있지만, 보안 관점에서는 audit이 동작하도록 만드는 것이 맞다.

### 3.3 npm과 yarn/pnpm의 차이

yarn과 pnpm도 `.npmrc`를 읽지만, 자체 설정 파일도 있다. yarn은 `.yarnrc.yml`(yarn berry)에서 `npmRegistryServer`를, pnpm은 `.npmrc`를 그대로 사용한다. Nexus 입장에서는 어떤 클라이언트든 npm Registry API를 구현하므로 동일하게 동작하지만, lockfile 형식이 다르기 때문에 팀 내에서 패키지 매니저를 통일하는 것이 중요하다.

## 4. Docker: 컨테이너 이미지

### 4.1 Docker Registry HTTP API V2

Nexus의 Docker 리포지토리는 Docker Registry HTTP API V2를 구현한다. `docker push`/`docker pull` 명령이 이 API를 호출하는 것이다.

Docker 이미지는 단일 파일이 아니라 **manifest + layer**의 조합이다. manifest는 이미지의 메타데이터(어떤 layer가 필요한지)를 담고, layer는 실제 파일시스템 차분(diff)이다. 각 layer는 SHA256 해시로 식별되는 **content-addressable storage** 구조다.

API V2의 핵심 엔드포인트를 정리하면 이렇다:

| 메서드 | 엔드포인트 | 용도 |
|--------|-----------|------|
| `GET` | `/v2/` | API 버전 확인, 인증 체크 |
| `HEAD` | `/v2/<name>/blobs/<digest>` | layer 존재 여부 확인 |
| `POST` | `/v2/<name>/blobs/uploads/` | layer 업로드 시작 |
| `PATCH` | `/v2/<name>/blobs/uploads/<uuid>` | layer 데이터 전송 |
| `PUT` | `/v2/<name>/blobs/uploads/<uuid>?digest=<digest>` | layer 업로드 완료 |
| `PUT` | `/v2/<name>/manifests/<reference>` | manifest 업로드 (push 완료) |
| `GET` | `/v2/<name>/manifests/<reference>` | manifest 조회 (pull 시작) |
| `GET` | `/v2/<name>/blobs/<digest>` | layer 다운로드 |
| `GET` | `/v2/_catalog` | 리포지토리 목록 조회 |
| `GET` | `/v2/<name>/tags/list` | 태그 목록 조회 |

```mermaid
sequenceDiagram
    participant CLI as docker CLI
    participant NEXUS as Nexus Docker Hosted
    participant BLOB as Blob Store

    Note over CLI,BLOB: docker push myimage:1.0
    CLI->>NEXUS: HEAD /v2/myimage/blobs/sha256:abc123
    alt layer 이미 존재
        NEXUS-->>CLI: 200 OK (skip upload)
    else layer 없음
        NEXUS-->>CLI: 404 Not Found
        CLI->>NEXUS: POST /v2/myimage/blobs/uploads/
        NEXUS-->>CLI: 202 Accepted (upload URL)
        CLI->>NEXUS: PATCH (layer data)
        CLI->>NEXUS: PUT (complete upload)
        NEXUS->>BLOB: layer 저장
    end
    CLI->>NEXUS: PUT /v2/myimage/manifests/1.0
    NEXUS->>BLOB: manifest 저장
    NEXUS-->>CLI: 201 Created
```

layer가 이미 존재하면 업로드를 건너뛰는 것이 핵심이다. 기본 이미지(예: `openjdk:17`)의 layer는 대부분 이미 있으므로, 실제로 전송하는 건 애플리케이션 코드 layer 뿐이다. 이 덕분에 Docker push가 빠른 것이다.

`docker pull`은 이 과정의 역순이다. 먼저 manifest를 가져와서 필요한 layer 목록을 확인하고, 각 layer를 병렬로 다운로드한다. 이미 로컬에 있는 layer는 다운로드를 건너뛴다. 같은 base image를 쓰는 이미지를 여러 개 pull하면 base layer는 한 번만 전송된다.

### 4.2 Docker 리포지토리의 포트 문제

Nexus에서 Docker 리포지토리를 만들면 **별도 포트**를 할당해야 한다. Docker CLI는 Registry URL에 경로를 포함할 수 없기 때문이다. `docker push nexus.example.com/myimage:1.0`은 되지만, `docker push nexus.example.com/repository/docker-hosted/myimage:1.0`은 안 된다.

그래서 hosted에 8082, proxy에 8083, group에 8084 같은 식으로 포트를 나눈다. Reverse proxy를 쓰면 서브도메인으로 라우팅할 수도 있다:

```
docker-hosted.nexus.example.com → 8082
docker-proxy.nexus.example.com  → 8083
docker.nexus.example.com        → 8084 (group)
```

nginx reverse proxy 설정 예시:

```nginx
server {
    listen 443 ssl;
    server_name docker.nexus.example.com;
    client_max_body_size 0;  # Docker layer 크기 제한 해제

    location / {
        proxy_pass http://localhost:8084;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

`client_max_body_size 0`이 핵심이다. Docker layer는 수백 MB가 될 수 있는데, nginx 기본값(1MB)이면 push가 실패한다. 이걸 빠뜨려서 한 시간을 헤매는 사람이 많다.

### 4.3 Docker Bearer Token

Docker Registry는 인증에 Bearer Token을 사용한다. Nexus에서 Docker 리포지토리를 사용하려면 **Docker Bearer Token Realm**을 활성화해야 한다. `Administration → Security → Realms`에서 추가하지 않으면 `docker login` 자체가 실패한다. 이걸 빠뜨리고 30분을 헤매는 사람이 생각보다 많다.

## 5. Raw: 범용 파일 저장소

Maven이나 npm 같은 포맷에 맞지 않는 파일은 Raw 리포지토리에 넣는다. 바이너리, 설정 파일, 문서, 스크립트 등이 대상이다.

Raw는 별도의 좌표 체계가 없다. URL 경로가 곧 파일 경로다:

```
PUT /repository/raw-hosted/tools/terraform/1.5.0/terraform-linux-amd64
GET /repository/raw-hosted/tools/terraform/1.5.0/terraform-linux-amd64
```

실무에서 Raw가 유용한 경우를 좀 더 구체적으로 살펴보자.

**빌드 도구 캐싱.** protoc, grpc 플러그인, SonarQube Scanner 같은 빌드에 필요한 바이너리를 Raw hosted에 올려두고 CI에서 `curl`로 다운받아 사용한다. GitHub Releases에서 직접 받으면 rate limit에 걸리거나 네트워크 지연이 발생하는데, 내부 Raw 리포지토리에서 받으면 안정적이다.

**설정 파일 버전 관리.** Ansible playbook, Terraform plan 결과, K8s manifest 같은 설정 파일을 아티팩트로 보관한다. 특정 시점의 설정 상태를 재현할 수 있어서 롤백에 유용하다.

**팀 간 공유 바이너리.** 데이터팀이 만든 ML 모델 바이너리, QA팀의 테스트 데이터셋 등을 버전 관리하며 공유한다.

**Raw proxy의 활용.** 외부 다운로드 URL을 Raw proxy로 캐싱할 수 있다. 예를 들어 `https://releases.hashicorp.com/`을 proxy하면 Terraform, Vault 등의 바이너리를 한번만 외부에서 받고 이후로는 캐시에서 가져온다.

Raw에 뭐든지 넣을 수 있다고 해서 S3 대용으로 쓰면 안 된다. 로그 파일이나 백업 데이터는 Raw가 아니라 오브젝트 스토리지에 넣어야 한다. Nexus의 Blob Store가 감당할 용량이 아니기 때문이다.

## 6. 포맷별 리포지토리 구성 패턴

모든 포맷에서 hosted + proxy + group의 3종 세트는 동일하다. 표준 구성은 이렇다:

| 포맷 | Hosted | Proxy | Group |
|------|--------|-------|-------|
| Maven | maven-releases, maven-snapshots | maven-central | maven-public |
| npm | npm-hosted | npm-proxy (npmjs.org) | npm-group |
| Docker | docker-hosted (8082) | docker-proxy (8083) | docker-group (8084) |
| Raw | raw-hosted | (필요 시) | raw-group |
| PyPI | pypi-hosted | pypi-proxy (pypi.org) | pypi-group |

group의 멤버 순서는 **hosted → proxy**가 원칙이다. 내부 아티팩트가 외부 아티팩트보다 우선되어야 하기 때문이다.

Maven은 hosted를 두 개(releases, snapshots)로 나누는 것이 관례인데, Docker는 보통 하나의 hosted로 충분하다. Docker 이미지 태그에 SNAPSHOT이라는 개념이 없고, `latest` 태그를 덮어쓰는 것이 일반적이기 때문이다. 다만 프로덕션용과 개발용 이미지를 분리하고 싶으면 `docker-releases`, `docker-snapshots` 두 개를 만들기도 한다.

## 7. Content Selector와 Routing Rule

리포지토리가 많아지면 "특정 아티팩트에 대한 접근을 제한하고 싶다"는 요구가 나온다. 이때 사용하는 도구가 Content Selector와 Routing Rule이다.

### 7.1 Content Selector

CSEL(Content Selector Expression Language)로 아티팩트를 필터링한다. CSEL 문법은 단순하지만 강력하다. 사용 가능한 속성과 연산자를 정리하면:

| 속성 | 설명 | 예시 값 |
|------|------|--------|
| `format` | 리포지토리 포맷 | `"maven2"`, `"npm"`, `"docker"` |
| `path` | 아티팩트 경로 | `"/com/mycompany/"` |

| 연산자 | 의미 | 예시 |
|--------|------|------|
| `==` | 같음 | `format == "maven2"` |
| `=^` | 시작 문자열 | `path =^ "/com/mycompany/"` |
| `=~` | 정규식 매칭 | `path =~ ".*-SNAPSHOT.*"` |
| `and` | 논리 AND | `format == "maven2" and path =^ "/com/"` |
| `or` | 논리 OR | `path =^ "/com/team-a/" or path =^ "/com/team-b/"` |

실제 사용 예시:

```
# 특정 groupId만 선택
format == "maven2" and path =^ "/com/mycompany/"

# SNAPSHOT만 선택 (Cleanup 등에 활용)
format == "maven2" and path =~ ".*-SNAPSHOT.*"

# npm 특정 scope만 선택
format == "npm" and path =^ "/@mycompany/"

# Docker 특정 이미지 prefix만 선택
format == "docker" and path =^ "/production/"
```

이 표현식을 Privilege에 연결하면 특정 팀만 특정 groupId에 접근하도록 제한할 수 있다.

### 7.2 Routing Rule

proxy 리포지토리에서 특정 경로의 요청을 차단하거나 허용하는 규칙이다. Content Selector가 "누가 접근할 수 있는가"를 제어한다면, Routing Rule은 "proxy가 무엇을 외부에서 가져올 수 있는가"를 제어한다.

두 가지 모드가 있다:

**BLOCK 모드**: 매칭되는 경로를 차단한다.

```
# dependency confusion 방어: 내부 네임스페이스를 외부에서 가져오지 못하게
BLOCK:
  - com/mycompany/.*
  - com/example/internal/.*

# 보안 취약 라이브러리 긴급 차단 (Log4Shell 대응 등)
BLOCK:
  - .*log4j.*
```

**ALLOW 모드**: 매칭되는 경로만 허용한다 (화이트리스트).

```
# 승인된 라이브러리만 외부에서 가져오기
ALLOW:
  - org/springframework/.*
  - org/apache/commons/.*
  - com/google/guava/.*
```

ALLOW 모드가 보안은 강하지만, 새 외부 라이브러리를 추가할 때마다 규칙을 업데이트해야 하는 운영 부담이 있다. 대부분의 환경에서는 BLOCK 모드로 내부 namespace만 차단하는 것이 현실적이다.

```mermaid
sequenceDiagram
    participant DEV as 개발자
    participant GROUP as maven-public (Group)
    participant HOSTED as maven-releases (Hosted)
    participant PROXY as maven-central (Proxy)
    participant EXT as Maven Central

    DEV->>GROUP: GET com.example:my-lib:1.0
    GROUP->>HOSTED: 탐색 (1순위)
    HOSTED-->>GROUP: 200 OK (found)
    GROUP-->>DEV: 아티팩트 반환

    DEV->>GROUP: GET org.apache:commons-lang3:3.14
    GROUP->>HOSTED: 탐색 (1순위)
    HOSTED-->>GROUP: 404
    GROUP->>PROXY: 탐색 (2순위)
    Note over PROXY: Routing Rule 체크
    alt 차단 규칙 매칭
        PROXY-->>GROUP: 403 Blocked
    else 통과
        PROXY->>EXT: fetch
        EXT-->>PROXY: 아티팩트
        PROXY-->>GROUP: 200 OK
    end
    GROUP-->>DEV: 결과 반환
```

## 8. 클라이언트 설정 요약

각 포맷별 클라이언트 설정을 한눈에 정리해두면 신규 팀원 온보딩이 빨라진다.

### Maven (`~/.m2/settings.xml`)
```xml
<mirror>
  <id>nexus</id>
  <mirrorOf>*</mirrorOf>
  <url>https://nexus.example.com/repository/maven-public/</url>
</mirror>
```

### npm (`~/.npmrc`)
```bash
registry=https://nexus.example.com/repository/npm-group/
@mycompany:registry=https://nexus.example.com/repository/npm-hosted/
//nexus.example.com/repository/npm-hosted/:_auth=BASE64_ENCODED
//nexus.example.com/repository/npm-group/:_auth=BASE64_ENCODED
```

### Docker (`docker login`)
```bash
docker login docker.nexus.example.com
# 또는 CI에서:
echo "$NEXUS_PASS" | docker login docker.nexus.example.com -u "$NEXUS_USER" --password-stdin
```

### pip (`~/.pip/pip.conf`)
```ini
[global]
index-url = https://deploy-user:deploy-pass@nexus.example.com/repository/pypi-group/simple
trusted-host = nexus.example.com
```

### Gradle (`build.gradle.kts`)
```kotlin
repositories {
    maven {
        url = uri("https://nexus.example.com/repository/maven-public/")
        credentials {
            username = project.findProperty("nexusUser") as String?
            password = project.findProperty("nexusPass") as String?
        }
    }
}
```

### Go (`go env`)
```bash
export GONOSUMCHECK="mycompany.com/*"
export GONOSUMDB="mycompany.com/*"
export GOPROXY="https://nexus.example.com/repository/go-group/,direct"
```

## 9. 정리

| 개념 | 핵심 |
|------|------|
| GAV 좌표 | groupId:artifactId:version으로 유일 식별. 경로로 변환되어 저장 |
| RELEASE vs SNAPSHOT | RELEASE는 불변(ALLOW_ONCE), SNAPSHOT은 타임스탬프 기반 반복 업로드 |
| Docker 포트 | Docker CLI 제약으로 리포지토리별 별도 포트 필요. reverse proxy로 우회 |
| Raw | 포맷에 맞지 않는 범용 파일 저장. 빌드 도구, 설정 파일, 공유 바이너리 |
| Content Selector | CSEL로 아티팩트 필터링 → Privilege 연결로 경로 레벨 접근 제어 |
| Routing Rule | proxy에서 특정 패턴 차단(BLOCK)/허용(ALLOW). dependency confusion 방어 |
| 구성 원칙 | hosted + proxy + group 3종 세트, group 순서는 hosted 먼저 |

포맷을 이해하는 것은 결국 "빌드 도구가 아티팩트를 어떻게 찾고, 어떤 규칙으로 해석하는가"를 이해하는 것과 같다. 각 포맷의 좌표 체계와 메타데이터 구조를 알면 문제가 생겼을 때 어디를 봐야 하는지 감이 온다. 다음 장에서는 proxy 리포지토리의 캐싱 메커니즘을 깊이 다룬다.

---

> **이전**: [Ch02 - 설치와 배포 환경](../02-installation-deployment/LEARN.md)
> **다음**: [Ch04 - 프록시와 캐싱 전략](../04-proxy-and-caching/LEARN.md)
