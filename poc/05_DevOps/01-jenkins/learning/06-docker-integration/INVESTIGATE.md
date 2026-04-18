# Ch06. Docker Integration - 면접 대비 질문

> 각 질문은 실제 면접에서 나올 수 있는 수준으로, 개념 이해뿐 아니라 실무 경험과 트레이드오프 판단 능력을 검증한다.

---

## Q1. DinD와 DooD의 차이를 설명하고, 각각의 보안/성능 트레이드오프를 설명하시오.

### 핵심 포인트

- **DinD(Docker-in-Docker)** 는 Jenkins 컨테이너 내부에 별도의 Docker daemon을 실행하는 방식이다. `--privileged` 플래그가 필수이며, 이는 컨테이너에 호스트 커널의 거의 모든 기능에 대한 접근 권한을 부여한다. 보안 관점에서 컨테이너 탈출(container escape) 공격에 취약하지만, 빌드 환경이 호스트와 완전히 격리된다는 장점이 있다.
- **DooD(Docker-outside-of-Docker)** 는 호스트의 `/var/run/docker.sock`을 Jenkins 컨테이너에 마운트하는 방식이다. `--privileged`가 필요 없지만, Docker socket 접근 자체가 사실상 호스트의 root 접근과 동등하다. `docker run -v /:/host`로 호스트 파일시스템 전체를 읽을 수 있기 때문이다. 대신 호스트의 이미지 레이어 캐시를 공유하므로 빌드 성능이 DinD보다 우수하다.
- **보안 트레이드오프**: DinD는 격리는 좋지만 `--privileged`가 더 넓은 공격 표면을 제공한다. DooD는 `--privileged` 없이 동작하지만 socket을 통해 호스트를 직접 제어할 수 있어 다른 종류의 위험이 존재한다. 결론적으로 두 방식 모두 프로덕션 보안 요구사항을 완전히 만족시키기 어렵다.
- **성능 트레이드오프**: DinD는 내부 Docker daemon이 자체 스토리지 드라이버를 사용하므로 레이어 캐시가 분리되어 이미지 pull/build가 느리다. DooD는 호스트 캐시를 그대로 사용하므로 반복 빌드가 빠르다.
- **실무 선택 기준**: 보안이 최우선이고 Kubernetes 환경이라면 DinD/DooD 대신 Kaniko나 Buildah 같은 daemonless 도구를 사용한다. 개발/테스트 환경에서 편의성이 중요하면 DooD를, 격리가 필요하면 DinD를 선택한다.

### 심화 질문

- Kubernetes Pod Security Standards에서 DinD와 DooD가 각각 어떤 수준(privileged, baseline, restricted)에서 허용되는가?
- DinD에서 `--privileged` 대신 `--cap-add`로 필요한 capability만 부여하는 것이 가능한가? 가능하다면 어떤 capability가 필요한가?

---

## Q2. Docker Agent를 사용하는 이유와 호스트에서 직접 빌드하는 것과의 차이를 설명하시오.

### 핵심 포인트

- **호스트 직접 빌드의 문제점**: Jenkins 에이전트에 설치된 도구 버전에 의존하므로, 에이전트 간 환경 차이로 "이 에이전트에서만 실패"하는 비결정적 빌드가 발생한다. 또한 여러 파이프라인이 같은 에이전트에서 동시에 실행될 때 글로벌 패키지, 포트, 임시 파일 등에서 충돌이 발생할 수 있다.
- **Docker Agent의 세 가지 이점**: (1) 환경 일관성 -- 이미지 태그로 도구 버전을 고정하므로 어디서 실행해도 동일한 결과를 보장한다. (2) 격리성 -- 각 빌드가 독립된 컨테이너에서 실행되므로 빌드 간 간섭이 원천 차단된다. (3) 재현성 -- 6개월 전 빌드를 동일한 이미지로 다시 실행할 수 있다.
- **스테이지별 이미지 지정**: `agent none`을 파이프라인 레벨에서 선언하고, 각 스테이지에서 다른 Docker 이미지를 사용할 수 있다. 빌드는 `node:18-alpine`, 보안 스캔은 `aquasec/trivy`, 배포는 `amazon/aws-cli`처럼 목적에 맞는 이미지를 선택하면 된다.
- **동작 원리**: Jenkins는 지정된 이미지로 컨테이너를 생성하면서 워크스페이스 디렉토리를 볼륨 마운트한다. 스텝들은 컨테이너 내부에서 실행되고, 완료 후 컨테이너는 삭제된다. 소스 코드와 빌드 아티팩트는 마운트된 워크스페이스를 통해 보존된다.
- **주의할 점**: Docker Agent는 빌드 "환경"을 컨테이너화하는 것이지, Docker 이미지를 빌드하는 것과는 다르다. Docker Agent 안에서 `docker build`를 실행하려면 DinD/DooD/Kaniko 같은 별도의 전략이 필요하다.

### 심화 질문

- Docker Agent에서 npm 캐시나 Maven 로컬 리포지토리를 빌드 간에 공유하려면 어떻게 해야 하는가?
- Docker Agent 실행 시 네트워크 모드(`--network`)를 지정해야 하는 상황은 어떤 경우인가?

---

## Q3. 컨테이너 이미지 태깅 전략에서 latest 태그를 프로덕션에서 사용하면 안 되는 이유를 설명하시오.

### 핵심 포인트

- **비결정성(Non-determinism)**: `latest`는 "가장 최근에 빌드된 이미지"를 가리키지만, 여러 브랜치에서 동시에 빌드가 발생하면 어떤 커밋의 이미지가 `latest`인지 보장할 수 없다. main 브랜치의 빌드 직후에 feature 브랜치의 빌드가 `latest`를 덮어쓸 수 있다.
- **롤백 불가능**: 배포 후 문제가 발견되어 롤백해야 할 때, "이전 latest"라는 개념이 존재하지 않는다. 이전 버전의 이미지 태그를 별도로 기록해두지 않았다면 어떤 이미지로 돌아가야 하는지 알 수 없다.
- **Kubernetes 캐싱 문제**: Kubernetes에서 `imagePullPolicy`가 `IfNotPresent`(기본값)일 때, 노드에 이미 `latest` 이미지가 캐시되어 있으면 새 버전을 pull하지 않는다. 결과적으로 노드마다 다른 버전의 `latest`가 실행될 수 있으며, 이는 디버깅이 극도로 어려운 불일치를 만든다.
- **감사 추적(Audit Trail) 부재**: 프로덕션에서 어떤 코드가 실행 중인지 추적하려면 이미지 태그에서 Git 커밋이나 버전을 역추적할 수 있어야 한다. `latest`는 이 정보를 제공하지 않는다.
- **권장 전략**: Git SHA 기반(`myapp:a1b2c3d`)이나 SemVer + Git SHA 조합(`myapp:2.1.0-a1b2c3d`)을 사용한다. 이렇게 하면 실행 중인 이미지에서 정확한 소스 코드 버전을 즉시 확인할 수 있고, 특정 버전으로의 롤백이 명확해진다.

### 심화 질문

- `latest` 태그를 개발 환경에서 편의상 사용하는 것은 괜찮은가? 괜찮다면 어떤 조건에서인가?
- 이미지 태그의 불변성(immutability)을 레지스트리 수준에서 강제하는 방법은 무엇인가? (예: Harbor의 tag immutability 정책)

---

## Q4. Kaniko나 Buildah가 필요한 이유를 Docker socket 마운트의 보안 관점에서 설명하시오.

### 핵심 포인트

- **Docker socket의 위험성**: `/var/run/docker.sock`에 접근할 수 있는 프로세스는 Docker API를 통해 호스트에서 임의의 컨테이너를 실행할 수 있다. `docker run -v /:/host alpine chroot /host`를 실행하면 호스트의 root 쉘을 얻는 것과 동일한 효과를 가진다. 이는 CI/CD 파이프라인에서 실행되는 코드(빌드 스크립트, 테스트 등)가 악의적이거나 취약할 경우 호스트 전체가 위험에 노출된다는 의미이다.
- **Kubernetes 환경의 제약**: Kubernetes의 Pod Security Standards(PSS)는 `restricted` 프로파일에서 호스트 path 마운트와 privileged 컨테이너를 금지한다. 보안 정책을 준수하면서 이미지를 빌드하려면 Docker daemon에 의존하지 않는 도구가 필요하다.
- **Kaniko의 접근 방식**: Kaniko는 컨테이너 내부에서 Dockerfile의 각 명령을 사용자 공간에서 실행하여 파일시스템 스냅샷을 기반으로 레이어를 생성한다. Docker daemon이 필요 없으므로 `--privileged`도, socket 마운트도 필요하지 않다. 일반 컨테이너 권한으로 동작하며, Kubernetes의 `restricted` PSS를 준수할 수 있다.
- **Buildah의 접근 방식**: Buildah는 rootless 모드를 지원하여 일반 사용자 권한으로 이미지를 빌드할 수 있다. Dockerfile뿐 아니라 스크립트 기반 빌드도 지원하여 더 유연한 이미지 생성이 가능하다.
- **트레이드오프**: Kaniko는 레이어 캐싱이 Docker만큼 효율적이지 않아(원격 레지스트리를 캐시 소스로 사용해야 함) 빌드 속도가 느릴 수 있다. Buildah는 Linux 전용이며 macOS/Windows에서 네이티브로 실행할 수 없다. 그러나 보안 요구사항이 엄격한 프로덕션 CI/CD 환경에서는 이러한 성능 트레이드오프가 보안 이점보다 크지 않다.

### 심화 질문

- Kaniko에서 레이어 캐시 효율을 높이려면 어떤 전략을 사용해야 하는가? (`--cache=true --cache-repo` 옵션의 동작 원리)
- rootless Docker(Docker Engine의 rootless mode)가 Kaniko/Buildah의 대안이 될 수 있는가? 차이점은 무엇인가?

---

## Q5. Multi-stage Dockerfile이 CI/CD에서 중요한 이유를 설명하시오.

### 핵심 포인트

- **이미지 크기 최적화**: Single-stage 빌드에서는 빌드 도구(컴파일러, 패키지 매니저, 개발 의존성)가 최종 이미지에 모두 포함된다. 예를 들어 Node.js 프로젝트에서 `node_modules`와 소스 코드가 포함된 이미지는 1GB를 넘을 수 있지만, Multi-stage로 빌드된 정적 파일 + nginx 이미지는 30~50MB 수준이다. 이미지가 작을수록 레지스트리 전송 시간이 줄고, 네트워크 비용이 감소하며, 컨테이너 시작 시간이 빨라진다.
- **보안 강화 (공격 표면 축소)**: 최종 이미지에 컴파일러, 패키지 매니저, 개발 도구가 없으면 공격자가 이용할 수 있는 도구가 줄어든다. 취약점 스캔(Trivy, Grype) 결과에서도 탐지되는 CVE 수가 극적으로 감소한다. 빌드 의존성에 존재하는 취약점이 런타임 이미지에 영향을 주지 않는다.
- **빌드 캐시 효율**: Docker는 레이어 단위로 캐시를 관리한다. Multi-stage에서 `COPY package*.json ./` + `RUN npm ci`를 소스 코드 복사보다 먼저 실행하면, `package.json`이 변경되지 않는 한 의존성 설치 레이어가 캐시에서 재사용된다. CI/CD에서 빌드 속도는 개발자 생산성에 직결되므로 이 캐시 전략은 중요하다.
- **관심사의 분리**: 빌드 환경과 런타임 환경을 명확히 분리함으로써, 각 스테이지를 독립적으로 최적화할 수 있다. 빌드 스테이지에서는 캐시 효율에 집중하고, 런타임 스테이지에서는 최소 이미지(Alpine, Distroless)를 사용하여 보안과 크기를 최적화한다.
- **CI/CD 파이프라인 단순화**: Dockerfile 하나에 빌드와 패키징 로직이 모두 포함되므로, Jenkins 파이프라인에서는 `docker build`와 `docker push`만 실행하면 된다. 빌드 도구 설치, 아티팩트 복사 등의 단계를 파이프라인에서 관리할 필요가 없어진다.

### 심화 질문

- Multi-stage 빌드에서 중간 스테이지의 결과물을 디버깅하거나 테스트하려면 어떻게 하는가? (`--target` 플래그의 활용)
- Google의 Distroless 이미지를 런타임 스테이지에 사용하면 어떤 추가적인 보안 이점이 있는가?

---

## Q6. Jenkins 파이프라인에서 docker.withRegistry()를 사용하는 이유와 Credential 관리의 중요성을 설명하시오.

### 핵심 포인트

- **Credential 노출 방지**: `docker login -u user -p password`를 파이프라인 스크립트에 직접 작성하면, Jenkins 빌드 로그에 비밀번호가 평문으로 노출된다. `docker.withRegistry()`는 Jenkins Credentials Store에 저장된 인증 정보를 안전하게 사용하며, 로그에서 자동으로 마스킹 처리한다.
- **동작 원리**: `docker.withRegistry()` 블록이 시작되면 Jenkins는 지정된 credential ID로 Credentials Store에서 인증 정보를 조회하고, `docker login`을 수행한다. 블록 내의 `push()`/`pull()` 호출은 인증된 상태에서 실행되며, 블록이 종료되면 `docker logout`이 자동 실행된다. 이 패턴은 credential의 생명주기를 명확하게 관리한다.
- **중앙 집중식 관리의 이점**: credential이 Jenkins Credentials Store에 저장되므로, credential 교체(rotation) 시 파이프라인 코드를 변경할 필요가 없다. 관리자가 Credentials Store에서만 업데이트하면 모든 파이프라인에 즉시 반영된다. 또한 RBAC을 통해 어떤 파이프라인이 어떤 credential에 접근할 수 있는지 제어할 수 있다.
- **실수 방지**: 환경변수로 credential을 전달하는 `withCredentials` 블록과 달리, `docker.withRegistry()`는 Docker 인증에 특화된 래퍼이므로 실수로 credential을 echo하거나 파일에 기록하는 위험이 줄어든다.
- **멀티 레지스트리 지원**: 하나의 파이프라인에서 여러 레지스트리(Docker Hub에서 pull, Private Registry에 push)를 사용할 때, 각 `withRegistry()` 블록에서 다른 credential을 사용할 수 있다.

### 심화 질문

- Jenkins Credentials Store에 저장된 credential은 디스크에 어떻게 암호화되어 저장되는가? Master 키가 유출되면 어떤 위험이 있는가?
- HashiCorp Vault와 같은 외부 시크릿 관리 도구와 Jenkins를 연동하면 어떤 추가적인 보안 이점이 있는가?
