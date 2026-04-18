# Ch07. Multi-container Apps with Compose - 심화 탐구

> LEARN.md를 학습한 뒤, 더 깊이 파고들어야 할 질문들

---

## Q1. Compose v2와 v1의 차이점은 무엇이며, 왜 마이그레이션해야 하는가?

### 왜 이 질문이 중요한가
기존 프로젝트에서는 `docker-compose` (v1)를 사용하지만, 최신 Docker는 `docker compose` (v2, 서브커맨드)를 권장한다. 두 버전 간 차이를 이해하지 못하면 스크립트가 깨지거나 신기능을 활용하지 못한다.

### 답변
**아키텍처 차이**:

| 특성 | Compose v1 | Compose v2 |
|------|------------|------------|
| **구현** | Python 독립 실행 파일 | Go로 재작성, Docker CLI 플러그인 |
| **명령어** | `docker-compose up` | `docker compose up` (하이픈 없음) |
| **성능** | 느림 | 빠름 (Go의 동시성 활용) |
| **설치** | pip install 또는 별도 바이너리 | Docker Desktop에 내장 |
| **유지보수** | 2023년 EOL (End of Life) | 활발히 개발 중 |

**주요 개선 사항**:
1. **더 빠른 빌드/배포**: 병렬 처리 개선
2. **Docker CLI와 통합**: `docker` 명령어와 일관된 플래그 사용
3. **BuildKit 네이티브 지원**: Multi-stage, cache mount 등
4. **Compose Watch**: 파일 변경 감지 및 자동 재시작
5. **GPU 지원 개선**: NVIDIA GPU 리소스 관리

**파일 포맷 호환성**:
- Compose v2는 v1의 YAML 파일을 대부분 호환
- `version: "3.8"` 같은 버전 선언은 선택적 (무시됨)
- Compose Specification이 표준이 됨 (버전 번호 대신)

**마이그레이션 체크리스트**:
```bash
# v1 제거 확인
docker-compose --version  # command not found가 나와야 함

# v2 확인
docker compose version  # Docker Compose version v2.x.x

# 기존 스크립트 업데이트
sed -i 's/docker-compose/docker compose/g' *.sh

# 문제 발생 시 v1 호환 모드
alias docker-compose='docker compose'
```

### 실무 적용
CI/CD 스크립트에서 `docker-compose`를 `docker compose`로 변경해야 한다. GitHub Actions에서는 `docker/setup-buildx-action`을 사용하면 자동으로 v2가 활성화된다. GitLab CI는 Docker Executor에서 기본적으로 v2를 사용한다.

---

## Q2. Compose Profiles을 활용하여 환경별 서비스를 어떻게 관리하는가?

### 왜 이 질문이 중요한가
개발 환경에서는 디버깅 도구, 테스트 DB를 사용하고, 프로덕션에서는 실제 서비스만 실행해야 한다. 모든 서비스를 항상 실행하면 리소스가 낭비되고 혼란스럽다.

### 답변
Profiles을 사용하면 서비스 그룹을 정의하고 선택적으로 활성화할 수 있다.

**예시**:
```yaml
services:
  web:
    image: myapp:latest
    # 프로파일 지정 없음 = 항상 실행

  db:
    image: postgres:15
    # 프로파일 지정 없음 = 항상 실행

  adminer:
    image: adminer
    profiles: ["dev"]  # dev 프로파일에서만 실행

  prometheus:
    image: prom/prometheus
    profiles: ["monitoring"]

  grafana:
    image: grafana/grafana
    profiles: ["monitoring"]

  debug-tool:
    image: nicolaka/netshoot
    profiles: ["debug"]
    stdin_open: true
    tty: true
```

**사용 방법**:
```bash
# 기본 서비스만 실행 (web, db)
docker compose up

# dev 프로파일 활성화 (web, db, adminer)
docker compose --profile dev up

# 여러 프로파일 동시 활성화
docker compose --profile dev --profile monitoring up

# 환경변수로 설정
COMPOSE_PROFILES=dev,monitoring docker compose up
```

**고급 패턴**:
```yaml
services:
  app:
    image: myapp:latest
    profiles: ["app"]

  app-debug:
    extends: app
    profiles: ["debug"]
    command: ["node", "--inspect=0.0.0.0:9229", "server.js"]
    ports:
      - "9229:9229"
```

**환경별 전략**:
- **로컬 개발**: `dev`, `debug` 프로파일
- **CI 테스트**: `test` 프로파일 (테스트 DB, Mock 서비스)
- **스테이징**: 기본 서비스만
- **프로덕션**: Compose 대신 Swarm/Kubernetes 사용

### 실무 적용
`.env` 파일에 `COMPOSE_PROFILES=dev`를 설정하여 팀원마다 다른 프로파일을 활성화할 수 있다. Makefile이나 스크립트로 `make dev`, `make prod` 같은 단축 명령을 만들어 프로파일을 자동 설정한다.

---

## Q3. depends_on의 한계는 무엇이며, 헬스체크와 어떻게 조합해야 하는가?

### 왜 이 질문이 중요한가
`depends_on`으로 서비스 시작 순서를 제어하지만, DB가 실제로 준비되기 전에 앱이 시작하여 연결 실패하는 경우가 빈번하다.

### 답변
`depends_on`은 컨테이너의 **시작 순서**만 제어하며, 서비스의 **준비 상태**를 기다리지 않는다.

**문제 시나리오**:
```yaml
services:
  web:
    depends_on:
      - db
  db:
    image: postgres:15
```

```
┌─────────────────────────────────────────────────────┐
│ 타임라인:                                            │
├─────────────────────────────────────────────────────┤
│ T0: db 컨테이너 시작 (postgres 초기화 중...)         │
│ T1: depends_on 만족 → web 컨테이너 시작             │
│ T2: web이 DB 연결 시도 → 실패! (postgres 아직 준비 안 됨) │
│ T3: postgres 초기화 완료                             │
└─────────────────────────────────────────────────────┘
```

**해결책 1: 헬스체크 + depends_on 조합 (Compose v2.20+)**
```yaml
services:
  web:
    depends_on:
      db:
        condition: service_healthy  # 헬스체크 통과할 때까지 대기
  db:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 5
      start_period: 10s
```

**해결책 2: 앱 레벨 재시도 로직**
```javascript
// Node.js 예시
const connectWithRetry = async () => {
  const maxRetries = 10;
  for (let i = 0; i < maxRetries; i++) {
    try {
      await db.connect();
      console.log('DB 연결 성공');
      return;
    } catch (err) {
      console.log(`DB 연결 실패 (${i + 1}/${maxRetries}), 5초 후 재시도...`);
      await new Promise(resolve => setTimeout(resolve, 5000));
    }
  }
  throw new Error('DB 연결 실패');
};
```

**해결책 3: 초기화 스크립트 (wait-for-it, dockerize)**
```yaml
services:
  web:
    depends_on:
      - db
    command: >
      sh -c "
        /wait-for-it.sh db:5432 --timeout=30 --strict --
        node server.js
      "
```

**헬스체크 베스트 프랙티스**:
```yaml
services:
  redis:
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 3s
      timeout: 1s

  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $POSTGRES_USER -d $POSTGRES_DB"]
      interval: 5s

  rabbitmq:
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 10s
```

### 실무 적용
Kubernetes로 마이그레이션하면 `initContainers`가 `depends_on`의 역할을 하고, `readinessProbe`가 헬스체크를 대체한다. Compose에서 헬스체크를 미리 설정해두면 K8s 매니페스트로 전환이 수월하다.

---

## Q4. Compose Watch는 무엇이며, 핫 리로드 개발 환경에 어떻게 활용하는가?

### 왜 이 질문이 중요한가
전통적으로는 코드 변경 시 `docker compose restart`나 볼륨 마운트를 사용했다. Compose Watch (v2.22+)는 파일 변경을 감지하여 자동으로 동기화하거나 재빌드한다.

### 답변
Compose Watch는 파일 시스템 변경을 감지하고 세 가지 액션을 수행한다:

**1. sync: 파일 동기화 (가장 빠름)**
```yaml
services:
  web:
    build: .
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
          ignore:
            - node_modules/
```
- 로컬 `./src` 변경 → 컨테이너 `/app/src`에 즉시 복사
- 노드 모듈, 파이썬 패키지 등 핫 리로드 환경에 적합

**2. rebuild: 이미지 재빌드 + 재시작**
```yaml
services:
  web:
    build: .
    develop:
      watch:
        - action: rebuild
          path: ./package.json
```
- 의존성 파일 변경 시 전체 재빌드 필요
- `package.json`, `requirements.txt`, `go.mod` 등

**3. sync+restart: 동기화 + 컨테이너 재시작**
```yaml
services:
  web:
    develop:
      watch:
        - action: sync+restart
          path: ./config
          target: /app/config
```
- 설정 파일 변경 시 재시작 필요
- 환경변수, 설정 YAML 등

**실용적 예시 (Node.js + React)**:
```yaml
services:
  backend:
    build: ./backend
    command: npm run dev  # nodemon 사용
    develop:
      watch:
        - action: sync
          path: ./backend/src
          target: /app/src
        - action: rebuild
          path: ./backend/package.json

  frontend:
    build: ./frontend
    command: npm start  # React 개발 서버
    develop:
      watch:
        - action: sync
          path: ./frontend/src
          target: /app/src
        - action: rebuild
          path: ./frontend/package.json
    environment:
      - WATCHPACK_POLLING=true  # 컨테이너 내 파일 감지 활성화
```

**사용 방법**:
```bash
# Watch 모드로 실행
docker compose watch

# 또는 up과 동시에
docker compose up --watch
```

**기존 볼륨 마운트와 비교**:
```yaml
# 전통적 방식 (여전히 유효)
services:
  web:
    volumes:
      - ./src:/app/src  # 항상 동기화, 성능 이슈 있을 수 있음

# Watch 방식 (선택적 동기화)
services:
  web:
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
```

### 실무 적용
대규모 Monorepo에서는 `sync` 액션이 특정 패키지만 감시하도록 설정하여 불필요한 동기화를 방지한다. Frontend는 `sync`, Backend는 `sync+restart`, 인프라 설정은 `rebuild`로 구분하여 최적의 개발 경험을 제공한다.

---

## Q5. 환경별 Compose 파일 오버라이드 전략은 무엇인가?

### 왜 이 질문이 중요한가
개발, 테스트, 프로덕션 환경마다 다른 설정이 필요하다. 파일을 복제하면 유지보수가 어려우므로 오버라이드 패턴을 사용한다.

### 답변
Compose는 여러 YAML 파일을 병합하여 최종 설정을 생성한다.

**파일 병합 순서**:
```bash
docker compose \
  -f compose.yaml \              # Base
  -f compose.override.yaml \     # 기본 오버라이드 (자동 로드)
  -f compose.dev.yaml \          # 환경별 오버라이드
  up
```

**권장 구조**:
```
project/
├── compose.yaml              # Base (공통 설정)
├── compose.override.yaml     # 로컬 개발 (Git 제외 가능)
├── compose.dev.yaml          # 개발 환경
├── compose.test.yaml         # CI 테스트
├── compose.prod.yaml         # 프로덕션 (참고용, 실제로는 K8s 사용)
```

**compose.yaml (Base)**:
```yaml
services:
  web:
    image: myapp:${TAG:-latest}
    environment:
      - NODE_ENV=${NODE_ENV:-production}

  db:
    image: postgres:15
```

**compose.dev.yaml**:
```yaml
services:
  web:
    build: .  # 이미지 대신 빌드
    volumes:
      - ./src:/app/src  # 소스 마운트
    environment:
      - NODE_ENV=development
      - DEBUG=*  # 디버그 로그 활성화
    ports:
      - "9229:9229"  # 디버거 포트

  db:
    ports:
      - "5432:5432"  # 로컬 접근 허용
    volumes:
      - ./db-data:/var/lib/postgresql/data  # 로컬 볼륨

  adminer:  # 개발 전용 서비스
    image: adminer
    ports:
      - "8080:8080"
```

**compose.test.yaml**:
```yaml
services:
  web:
    build:
      context: .
      target: test  # Multi-stage 테스트 스테이지
    command: npm test

  db:
    tmpfs:
      - /var/lib/postgresql/data  # 메모리 DB (빠름)
```

**compose.prod.yaml** (참고용):
```yaml
services:
  web:
    image: myregistry.io/myapp:${TAG}
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
    environment:
      - NODE_ENV=production
    # 볼륨 마운트 없음, 포트 노출 없음 (Ingress 사용)

  db:
    # 외부 DB 사용, 컨테이너로 실행 안 함
    image: placeholder
    entrypoint: /bin/true  # no-op
```

**사용 패턴**:
```bash
# 로컬 개발 (compose.yaml + compose.override.yaml 자동 병합)
docker compose up

# 명시적 개발 환경
docker compose -f compose.yaml -f compose.dev.yaml up

# CI 테스트
docker compose -f compose.yaml -f compose.test.yaml run --rm web npm test

# 환경변수로 파일 지정
COMPOSE_FILE=compose.yaml:compose.prod.yaml docker compose config
```

**병합 규칙**:
- **스칼라 값**: 나중 파일이 덮어씀
- **리스트**: 병합 또는 교체 (항목에 따라 다름)
- **딕셔너리**: 재귀적 병합

### 실무 적용
GitLab CI에서는 `.gitlab-ci.yml`에서 `COMPOSE_FILE` 환경변수로 테스트 파일을 지정한다. GitHub Actions에서는 `docker compose -f compose.yaml -f compose.test.yaml up --abort-on-container-exit`로 테스트를 실행한다.

---

## Q6. Compose에서 네트워크 격리와 서비스 간 통신을 어떻게 제어하는가?

### 왜 이 질문이 중요한가
기본적으로 같은 Compose 프로젝트의 모든 서비스는 하나의 네트워크에 연결되어 서로 통신할 수 있다. 보안상 특정 서비스만 통신을 허용하고 싶을 때가 있다.

### 답변
Compose는 프로젝트마다 기본 네트워크를 생성하지만, 커스텀 네트워크로 격리할 수 있다.

**기본 동작**:
```yaml
services:
  web:
  api:
  db:
# 모든 서비스가 {project}_default 네트워크에 연결됨
# web ↔ api ↔ db 모두 통신 가능
```

**네트워크 격리 패턴**:
```yaml
services:
  frontend:
    networks:
      - public

  api:
    networks:
      - public    # frontend와 통신
      - backend   # db와 통신

  db:
    networks:
      - backend   # api하고만 통신, frontend는 직접 접근 불가

  cache:
    networks:
      - backend

networks:
  public:
  backend:
```

```
┌─────────────────────────────────────────────────────┐
│                    public 네트워크                   │
│  ┌──────────┐              ┌──────────┐             │
│  │ frontend │◄────────────►│   api    │             │
│  └──────────┘              └──────────┘             │
│                                  │                   │
└──────────────────────────────────┼───────────────────┘
                                   │
┌──────────────────────────────────┼───────────────────┐
│                    backend 네트워크                   │
│                             ┌────┴────┐              │
│                             │   api   │              │
│                             └────┬────┘              │
│                    ┌─────────────┼─────────────┐     │
│                    ▼             ▼             ▼     │
│              ┌─────────┐   ┌─────────┐   ┌────────┐ │
│              │   db    │   │  cache  │   │ worker │ │
│              └─────────┘   └─────────┘   └────────┘ │
└─────────────────────────────────────────────────────┘
```

**네트워크 별칭**:
```yaml
services:
  api:
    networks:
      public:
        aliases:
          - api.myapp.local
      backend:
        aliases:
          - api-internal

  db:
    networks:
      backend:
        aliases:
          - postgres.myapp.internal
```

**외부 네트워크 연결**:
```yaml
services:
  web:
    networks:
      - myapp-network
      - shared-proxy-network  # 다른 Compose 프로젝트와 공유

networks:
  myapp-network:
  shared-proxy-network:
    external: true  # 외부에서 생성된 네트워크
```

**네트워크 드라이버 설정**:
```yaml
networks:
  frontend:
    driver: bridge
    driver_opts:
      com.docker.network.bridge.name: br-frontend
  backend:
    driver: bridge
    internal: true  # 외부 인터넷 접근 차단
```

### 실무 적용
마이크로서비스 환경에서 public 네트워크는 Nginx/Traefik 같은 프록시만 연결하고, backend 네트워크는 내부 서비스만 연결한다. DB는 절대 public 네트워크에 노출하지 않는다.

---

## Q7. Compose를 프로덕션에서 사용해야 하는가, 아니면 Swarm/Kubernetes로 전환해야 하는가?

### 왜 이 질문이 중요한가
Compose는 개발 환경에서 탁월하지만, 프로덕션 사용은 논란이 있다. 언제 Swarm이나 Kubernetes로 전환해야 하는지 판단 기준이 필요하다.

### 답변
**Compose의 프로덕션 한계**:
1. **단일 호스트 제약**: Compose는 기본적으로 하나의 Docker 호스트에서만 작동
2. **자동 복구 없음**: 컨테이너가 죽으면 수동으로 재시작해야 함
3. **롤링 업데이트 미지원**: 무중단 배포 불가
4. **자동 확장 없음**: CPU/메모리 기반 스케일링 불가
5. **헬스체크 기반 재시작 제한**: 헬스체크 실패 시 자동 재배포 없음

**Compose 적합 시나리오**:
- 소규모 사이드 프로젝트 (단일 서버로 충분)
- 스테이징 환경 (프로덕션과 유사한 구성 테스트)
- 개발자 로컬 환경
- CI/CD 테스트 환경
- 내부 도구 (Jenkins, GitLab, Nexus 등)

**Swarm 적합 시나리오**:
- 멀티 호스트 필요하지만 복잡도는 낮춤
- Compose 파일을 거의 그대로 재사용 (deploy 섹션만 추가)
- 소규모 클러스터 (3-10 노드)
- Kubernetes까지 필요 없는 경우

**Kubernetes 적합 시나리오**:
- 대규모 클러스터 (수십~수백 노드)
- 고급 스케줄링 정책 필요
- 다양한 워크로드 (Stateful, Job, CronJob 등)
- 클라우드 네이티브 생태계 활용 (Helm, Istio, ArgoCD 등)
- 멀티 클러스터, 멀티 클라우드

**마이그레이션 경로**:

```
로컬 개발 (Compose)
     │
     ├─→ 소규모 프로덕션 (Compose on single host)
     │
     ├─→ 멀티 호스트 필요 (Swarm)
     │        │
     │        └─→ 규모 증가 (Kubernetes)
     │
     └─→ 처음부터 K8s (클라우드 네이티브 목표)
```

**Compose → Swarm 전환**:
```yaml
# compose.yaml (Compose와 Swarm 모두 호환)
services:
  web:
    image: myapp:latest
    deploy:  # Swarm 전용 섹션 (Compose는 무시)
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
    ports:
      - "80:8080"

# Compose로 실행
docker compose up

# Swarm 스택으로 배포
docker stack deploy -c compose.yaml myapp
```

**Compose → Kubernetes 전환 (Kompose)**:
```bash
# Compose 파일을 K8s 매니페스트로 변환
kompose convert -f compose.yaml

# 생성된 파일:
# - deployment.yaml
# - service.yaml
# - persistentvolumeclaim.yaml
```

### 실무 적용
많은 스타트업은 초기에 Compose로 시작하여 단일 EC2/Droplet에서 운영한다. 트래픽 증가 시 Swarm으로 전환하고, 팀 규모와 요구사항이 커지면 Kubernetes로 마이그레이션한다. 중요한 것은 Compose 단계에서도 12-Factor App 원칙을 따라 환경변수, 헬스체크, 무상태 설계를 하면 전환이 수월하다는 점이다.
