# Ch06. Containerizing Applications - 심화 탐구

> LEARN.md를 학습한 뒤, 더 깊이 파고들어야 할 질문들

---

## Q1. Multi-stage 빌드에서 레이어 캐싱은 어떻게 동작하며, 어떻게 최적화할 수 있는가?

### 왜 이 질문이 중요한가
Multi-stage 빌드는 이미지 크기를 줄이는 강력한 도구이지만, 빌드 속도도 중요하다. 레이어 캐싱을 제대로 활용하지 못하면 매번 전체 빌드를 다시 실행하게 되어 개발 생산성이 떨어진다.

### 답변
각 스테이지는 독립적인 캐시 체인을 가진다. `FROM base AS build` 형태로 이전 스테이지를 참조하면 해당 스테이지의 레이어를 재사용할 수 있다. 최적화 전략은 다음과 같다:

1. **의존성 레이어 분리**: `COPY package.json .` → `RUN npm install` → `COPY . .` 순서로 작성하여 소스 코드 변경 시 의존성 설치를 건너뛸 수 있다.
2. **BuildKit의 캐시 마운트 활용**: `RUN --mount=type=cache,target=/root/.npm npm install`로 패키지 매니저 캐시를 호스트에 유지한다.
3. **병렬 스테이지 활용**: 의존성 없는 스테이지는 자동으로 병렬 실행되므로, 클라이언트/서버 빌드를 분리하면 빌드 시간이 거의 절반으로 줄어든다.
4. **캐시 무효화 최소화**: ARG를 사용하여 빌드 타임 변수를 전달할 때, ARG 위치에 따라 이후 레이어가 모두 재빌드되므로 가능한 늦게 선언한다.

### 실무 적용
CI/CD 파이프라인에서 `--cache-from` 플래그로 이전 빌드의 레이어를 캐시로 사용할 수 있다. Docker Build Cloud나 BuildKit의 registry cache를 활용하면 분산 빌드 환경에서도 캐시를 공유할 수 있다.

---

## Q2. .dockerignore는 정확히 어떤 영향을 미치며, 어떤 전략으로 작성해야 하는가?

### 왜 이 질문이 중요한가
.dockerignore를 작성하지 않으면 빌드 컨텍스트에 불필요한 파일(node_modules, .git 등)이 포함되어 빌드가 느려지고 이미지 크기가 커진다. 또한 민감한 정보(.env, 키 파일)가 이미지에 포함될 수 있다.

### 답변
.dockerignore는 빌드 컨텍스트로 전송되는 파일을 제외한다. `docker build .` 실행 시 Docker 데몬은 현재 디렉토리의 모든 파일을 먼저 전송하는데, .dockerignore가 있으면 제외 패턴에 맞는 파일은 전송하지 않는다.

**전략적 작성 방법**:
1. **허용 목록 방식**: `*`로 모든 파일 제외 후 `!src`, `!package.json` 등 필요한 것만 포함
2. **거부 목록 방식**: `node_modules`, `.git`, `*.log` 등 불필요한 것만 나열
3. **보안 우선**: `.env`, `*.key`, `*.pem`, `.aws` 등 시크릿 파일은 반드시 제외
4. **빌드 결과물 제외**: `dist/`, `build/`, `target/` 등은 컨테이너 내에서 빌드되므로 제외
5. **문서 및 메타파일 제외**: `README.md`, `.git`, `.github`, `docs/`는 런타임에 불필요

### 실무 적용
.dockerignore는 .gitignore와 유사하지만 목적이 다르다. .gitignore는 버전 관리 대상을 결정하고, .dockerignore는 빌드 컨텍스트를 최적화한다. 개발 환경에서만 필요한 파일(test/, .vscode/ 등)은 .dockerignore에 추가해야 한다.

---

## Q3. scratch 이미지를 Base로 사용할 때의 장단점과 실용적인 사용 시나리오는?

### 왜 이 질문이 중요한가
Multi-stage 빌드 예제에서 `FROM scratch`를 사용하여 극도로 작은 이미지(27MB)를 만들었다. 하지만 scratch는 아무것도 포함하지 않기 때문에 디버깅이나 일부 기능에 제약이 있다.

### 답변
`scratch`는 Docker의 가장 작은 Base 이미지로, 실제로는 빈 레이어이다. Go와 같이 정적 바이너리를 생성하는 언어에 적합하다.

**장점**:
- **최소 공격 표면**: 쉘, 패키지 매니저, 유틸리티가 없어 공격자가 악용할 도구가 없다
- **최소 크기**: 바이너리만 포함하므로 이미지가 수 MB에 불과
- **최소 취약점**: 설치된 패키지가 없으므로 CVE가 거의 발생하지 않음

**단점**:
- **디버깅 불가**: `docker exec`로 쉘 접속 불가, `ls`, `cat`, `curl` 등 도구 없음
- **CA 인증서 없음**: HTTPS 요청 시 인증서 검증 실패 (수동으로 COPY 필요)
- **DNS 해석 제약**: 일부 언어는 `/etc/resolv.conf` 등이 필요
- **타임존 없음**: `/usr/share/zoneinfo` 없음, 시간 처리가 UTC로 제한될 수 있음

**실용적 사용 시나리오**:
1. Go 정적 바이너리: `CGO_ENABLED=0 go build`로 완전히 독립적인 실행 파일
2. Rust 정적 바이너리: `musl` 타겟으로 빌드
3. C/C++ 정적 링크: `glibc` 의존성 제거 후
4. 보안 최우선 마이크로서비스: 공격 표면을 최소화해야 하는 경우

**대안**: `alpine` (5MB), `distroless` (Google 제공, 런타임만 포함)

### 실무 적용
프로덕션에서는 `scratch` 대신 `distroless`를 권장한다. distroless는 CA 인증서, 타임존, 사용자 관리 등 최소한의 런타임 요소를 포함하면서도 쉘은 제공하지 않아 보안과 실용성의 균형을 맞춘다.

---

## Q4. BuildKit의 고급 기능(RUN --mount, 병렬 빌드 등)은 어떻게 동작하며 언제 사용해야 하는가?

### 왜 이 질문이 중요한가
`docker init`이 생성한 Dockerfile에는 `RUN --mount=type=bind`, `--mount=type=cache` 같은 BuildKit 전용 문법이 사용된다. 이를 이해하지 못하면 빌드 최적화 기회를 놓친다.

### 답변
BuildKit은 Docker의 차세대 빌드 엔진으로, Docker 18.09부터 기본 활성화되었다. 전통적인 빌드보다 빠르고 효율적이다.

**주요 기능**:

1. **Bind Mount (`--mount=type=bind`)**:
   - 빌드 컨텍스트의 파일을 임시로 마운트하여 COPY 레이어 생성을 피한다
   - `package.json`만 마운트하여 의존성을 설치하면 레이어가 더 작아진다
   - 예: `RUN --mount=type=bind,source=package.json,target=package.json npm install`

2. **Cache Mount (`--mount=type=cache`)**:
   - 빌드 간 지속되는 캐시 디렉토리를 마운트
   - 패키지 매니저 캐시(`/root/.npm`, `/root/.cache/pip` 등)를 호스트에 유지
   - 의존성 재다운로드 시간 대폭 감소
   - 예: `RUN --mount=type=cache,target=/root/.npm npm install`

3. **Secret Mount (`--mount=type=secret`)**:
   - 빌드 시 필요한 시크릿(API 키 등)을 레이어에 포함시키지 않고 임시 마운트
   - 예: `RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm install`

4. **병렬 빌드**:
   - 의존성 없는 스테이지를 자동으로 병렬 실행
   - DAG(Directed Acyclic Graph) 기반 최적화

5. **Lazy Pull**:
   - Base 이미지를 전체 다운로드하지 않고 필요한 레이어만 먼저 가져온다

### 실무 적용
Node.js 프로젝트에서 `--mount=type=cache,target=/root/.npm`을 사용하면 초기 빌드는 느리지만 이후 빌드는 수십 초로 단축된다. Monorepo에서 여러 패키지를 빌드할 때 병렬 스테이지를 활용하면 빌드 시간이 크게 줄어든다.

---

## Q5. 프로덕션 이미지에서 비root 사용자로 실행하는 것이 왜 중요하며, 어떻게 구현하는가?

### 왜 이 질문이 중요한가
`docker init`이 생성한 Dockerfile에는 `USER node`가 포함되어 있다. 컨테이너를 root로 실행하면 보안 위험이 크게 증가한다.

### 답변
컨테이너 내 root 사용자는 UID 0으로, 호스트의 root와 동일한 UID이다. 만약 컨테이너가 탈출하거나 호스트 디렉토리를 바인드 마운트한 경우, root 권한으로 호스트 파일시스템을 조작할 수 있다.

**위험 시나리오**:
1. 컨테이너에서 `/etc/passwd`를 마운트하면 호스트 사용자를 추가/삭제 가능
2. 커널 취약점을 통해 컨테이너 탈출 시 호스트를 완전히 장악
3. 불필요한 Capabilities가 부여되어 네트워크 설정 변경 가능

**구현 방법**:

**패턴 1: 기존 사용자 활용**
```dockerfile
FROM node:20-alpine
USER node  # node 이미지는 기본적으로 'node' 사용자 제공
WORKDIR /home/node/app
COPY --chown=node:node . .
```

**패턴 2: 사용자 생성**
```dockerfile
FROM alpine
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser
USER appuser
WORKDIR /home/appuser
```

**패턴 3: 숫자 UID 사용 (distroless)**
```dockerfile
FROM gcr.io/distroless/static
COPY --chown=65532:65532 /bin/app /app
USER 65532
ENTRYPOINT ["/app"]
```

**주의사항**:
- COPY 시 `--chown` 플래그로 파일 소유권 설정
- 비root 사용자는 1024 이하 포트 바인딩 불가 (CAP_NET_BIND_SERVICE 필요)
- 로그 디렉토리, 캐시 디렉토리 등에 쓰기 권한 필요

### 실무 적용
Kubernetes에서는 SecurityContext로 `runAsNonRoot: true`를 설정하여 root 컨테이너 실행을 차단할 수 있다. 이미지에 USER 지시자가 없으면 Pod 생성이 실패하므로, 모든 프로덕션 이미지는 비root 사용자를 명시해야 한다.

---

## Q6. 12-Factor App 원칙을 Dockerfile에 어떻게 적용하는가?

### 왜 이 질문이 중요한가
12-Factor App은 클라우드 네이티브 애플리케이션의 설계 원칙이다. Dockerfile을 작성할 때 이 원칙을 따르면 이식성, 확장성, 운영성이 향상된다.

### 답변
12가지 원칙 중 컨테이너화와 관련된 핵심 요소:

**III. Config (환경 변수로 설정 관리)**
```dockerfile
# ✗ 잘못된 예: 하드코딩
ENV DATABASE_URL=postgres://prod-db:5432/myapp

# ✓ 올바른 예: 런타임에 주입
ENV DATABASE_URL=""
# docker run -e DATABASE_URL=postgres://... 으로 주입
```

**IV. Backing Services (외부 서비스를 연결된 리소스로 취급)**
```dockerfile
# 데이터베이스, 캐시, 메시지 큐를 ENV로 설정
ENV REDIS_URL=""
ENV POSTGRES_URL=""
ENV RABBITMQ_URL=""
```

**VI. Processes (무상태 프로세스)**
```dockerfile
# 세션 상태를 컨테이너에 저장하지 않음
# 파일 업로드는 S3 등 외부 스토리지로
# sticky session 대신 Redis 등 외부 세션 스토어 사용
```

**VII. Port Binding (포트를 통한 서비스 노출)**
```dockerfile
EXPOSE 8080
# 외부 웹서버(Apache, Nginx)에 의존하지 않고 자체 HTTP 서버 실행
CMD ["node", "server.js"]
```

**VIII. Concurrency (프로세스 모델로 확장)**
```dockerfile
# 하나의 컨테이너 = 하나의 프로세스
# 수평 확장은 컨테이너 복제로
# Swarm replicas나 Kubernetes ReplicaSet으로 관리
```

**X. Dev/Prod Parity (개발/프로덕션 환경 일치)**
```dockerfile
# 동일한 Base 이미지 사용
FROM node:20-alpine  # 개발, 스테이징, 프로덕션 모두 동일
```

**XI. Logs (로그를 이벤트 스트림으로)**
```dockerfile
# stdout/stderr로 로그 출력
# 파일에 쓰지 않음 (docker logs로 수집)
CMD ["node", "app.js"]  # console.log() 사용
```

### 실무 적용
CI/CD 파이프라인에서 환경별로 다른 설정을 주입한다. 개발 환경에서는 `docker-compose.override.yml`로 로컬 DB를 연결하고, 프로덕션에서는 Kubernetes Secret/ConfigMap으로 실제 서비스를 연결한다. 이미지는 환경과 무관하게 한 번만 빌드한다.

---

## Q7. CI/CD 파이프라인에서 Docker 빌드를 어떻게 최적화하는가?

### 왜 이 질문이 중요한가
로컬에서는 빌드가 빠르지만, CI/CD에서는 캐시가 없어 매번 전체 빌드를 실행하게 된다. 이는 배포 시간을 증가시키고 리소스를 낭비한다.

### 답변
CI/CD 환경에서는 각 빌드가 클린 상태에서 시작되므로 레이어 캐시가 없다. 다음 전략으로 최적화할 수 있다:

**1. 캐시 재사용 (--cache-from)**
```bash
# 이전 이미지를 캐시로 사용
docker pull myapp:latest || true
docker build --cache-from myapp:latest -t myapp:${CI_COMMIT_SHA} .
docker push myapp:${CI_COMMIT_SHA}
```

**2. BuildKit Inline Cache**
```bash
# 빌드 시 캐시 메타데이터를 이미지에 포함
docker buildx build \
  --cache-to type=inline \
  --cache-from type=registry,ref=myapp:latest \
  -t myapp:latest \
  --push .
```

**3. Registry Cache**
```bash
# 원격 레지스트리에 캐시 저장
docker buildx build \
  --cache-to type=registry,ref=myapp:buildcache \
  --cache-from type=registry,ref=myapp:buildcache \
  -t myapp:latest .
```

**4. Docker Build Cloud**
```bash
# 빌드를 클라우드로 오프로드, 캐시 자동 관리
docker buildx build --builder cloud-myorg-mybuilder -t myapp:latest .
```

**5. Layer Caching 서비스 (GitHub Actions, GitLab CI)**
```yaml
# GitHub Actions 예시
- uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

**6. Dockerfile 최적화**
```dockerfile
# 자주 변경되지 않는 레이어를 앞에 배치
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./     # 의존성 먼저
RUN npm ci --only=production
COPY . .                  # 소스는 마지막
```

**7. Multi-stage 병렬 빌드**
```dockerfile
# 의존성 없는 스테이지는 병렬 실행됨
FROM base AS build-frontend
RUN npm run build:frontend

FROM base AS build-backend
RUN npm run build:backend

FROM nginx
COPY --from=build-frontend /app/dist /usr/share/nginx/html
COPY --from=build-backend /app/server /app/server
```

### 실무 적용
GitHub Actions에서는 `docker/build-push-action`이 자동으로 GitHub Cache를 활용한다. GitLab CI에서는 `DOCKER_BUILDKIT=1`과 `--cache-from`을 조합하여 레지스트리 캐시를 사용한다. Jenkins에서는 Docker-in-Docker 대신 DinD (Docker-outside-of-Docker)를 사용하여 호스트의 레이어 캐시를 활용할 수 있다.
