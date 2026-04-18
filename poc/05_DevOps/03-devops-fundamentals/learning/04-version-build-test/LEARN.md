# Ch04. 버전 관리, 빌드, 테스트

**핵심 질문**: "팀이 협업하려면 코드를 어떻게 관리하고 검증하는가?"

---

## 🎯 학습 목표

1. Git 브랜칭 전략(Trunk-based, GitFlow, GitHub Flow)의 차이를 설명하고 팀 규모에 맞는 전략을 선택할 수 있다.
2. 시맨틱 버저닝(SemVer) 규칙을 적용해 버전 번호를 결정하고 CHANGELOG를 관리할 수 있다.
3. Makefile로 lint, test, build, docker 타겟을 구성해 반복 작업을 자동화할 수 있다.
4. Jest로 단위 테스트를 작성하고 모킹(mocking) 전략을 적절히 활용할 수 있다.
5. pytest 픽스처(fixture)와 teardown을 활용해 통합 테스트를 안전하게 구성할 수 있다.
6. 테스트 피라미드 원칙에 따라 각 레이어의 비율과 범위를 설계할 수 있다.

---

## 1. Git 워크플로와 브랜칭 전략

소스 코드를 혼자 작성할 때는 단순한 커밋 이력만으로 충분하다. 그러나 팀이 늘어나면 "누가 어떤 코드를 언제 변경했는가"를 추적하고, 기능 개발과 릴리스가 서로 방해하지 않도록 격리하는 구조가 필요해진다. 브랜칭 전략이 그 해답이다.

### Trunk-based Development

Trunk-based Development(TBD)는 모든 개발자가 `main`(trunk) 브랜치 하나에 자주, 짧게 커밋하는 전략이다. 기능이 미완성 상태라면 Feature Flag로 코드를 비활성화한 채 머지한다. 결과적으로 항상 배포 가능한 상태를 유지한다.

```
main ──●──●──●──●──●──●──●──   (모든 커밋이 CI를 통과)
       │        │
    feature  hotfix  (수명: 1일 미만)
```

TBD가 빛을 발하는 조건은 CI 파이프라인이 빠르고(< 10분), 팀 전체가 테스트를 작성하는 문화가 정착됐을 때다. 구글, 메타 같은 대형 조직도 이 전략을 사용한다. 반면 브랜치 수명이 길어질수록 머지 충돌이 누적되므로 "며칠짜리 피처 브랜치"는 TBD의 정신에 어긋난다.

### GitHub Flow

GitHub Flow는 TBD보다 약간 구조적이다. `main` 외에 피처 브랜치만 두며, PR(Pull Request) 리뷰를 거쳐 머지한다. 브랜치 수명은 수일에서 1~2주 이내를 권장한다. SaaS처럼 단일 프로덕션 환경에 지속 배포하는 팀에 적합하다.

```
main ──●──────────────────●──
        \                /
         feature/login──●  (PR → 리뷰 → 머지)
```

### GitFlow

GitFlow는 `main`, `develop`, `feature/*`, `release/*`, `hotfix/*` 다섯 종류의 브랜치를 정의한다. 릴리스 주기가 명확하고 여러 버전을 동시에 지원해야 하는 패키지 라이브러리나 모바일 앱에 어울린다. 브랜치가 많고 규칙이 복잡해서 CI/CD 자동화 없이는 유지 비용이 높다.

```
main    ──●──────────────────────●──
           \                    /
develop ──●──●──●──●──●──●──●──
                \      /  \
              feature  \  release/1.2
                        hotfix/bug
```

세 전략 중 어느 것이 "정답"이라는 기준은 없다. 배포 빈도, 팀 규모, 제품 특성에 따라 달라진다. 스타트업 초기라면 GitHub Flow로 시작하고, 릴리스 관리가 복잡해지면 GitFlow 요소를 선택적으로 도입하는 방식이 실용적이다.

---

## 2. 시맨틱 버저닝과 릴리스 관리

라이브러리나 API를 외부에 공개할 때 버전 번호는 "이 변경이 얼마나 영향을 미치는가"를 전달하는 약속이다. 시맨틱 버저닝(SemVer)은 `MAJOR.MINOR.PATCH` 세 숫자로 그 약속을 표준화한다.

| 변경 유형 | 버전 증가 | 예 |
|-----------|-----------|-----|
| 하위 호환 버그 수정 | PATCH | 1.2.3 → 1.2.4 |
| 하위 호환 기능 추가 | MINOR | 1.2.3 → 1.3.0 |
| 하위 호환 불가 변경 | MAJOR | 1.2.3 → 2.0.0 |

MAJOR가 0인 경우(`0.y.z`)는 초기 개발 단계로, 언제든 API가 바뀔 수 있다는 의미다. 릴리스 후보에는 `-rc.1`, `-beta.2` 같은 프리릴리스 식별자를 붙인다.

CHANGELOG는 개발자가 "무엇이 바뀌었나"를 파악하는 첫 번째 창구다. [Keep a Changelog](https://keepachangelog.com) 형식을 따르면 `Added`, `Changed`, `Fixed`, `Removed`, `Security` 섹션으로 구조화할 수 있다.

```markdown
## [1.3.0] - 2025-09-01
### Added
- 사용자 프로필 이미지 업로드 API (`POST /users/:id/avatar`)

### Fixed
- 로그아웃 후 세션 쿠키가 남아있던 버그 (#234)

## [1.2.1] - 2025-08-15
### Security
- JWT 서명 알고리즘을 HS256에서 RS256으로 교체
```

Git 태그로 버전을 추적하면 특정 릴리스 코드로 즉시 되돌아갈 수 있다.

```bash
git tag -a v1.3.0 -m "Release 1.3.0: 프로필 이미지 업로드"
git push origin v1.3.0
```

---

## 3. 빌드 자동화 — Makefile

빌드 자동화의 목적은 "개발자가 명령어 순서를 외우지 않아도 동일한 결과를 얻게 하는 것"이다. Makefile은 그 도구 중 가장 범용적이다. Node.js, Go, Python 어느 언어든 `make build` 하나로 프로세스를 통일할 수 있다.

아래 Makefile은 Node.js 백엔드 서비스를 가정한 완성된 예시다. `.PHONY`를 선언하는 이유는 같은 이름의 파일이 존재할 때 Make가 파일을 빌드 대상으로 오해하는 것을 막기 위해서다.

```makefile
# Makefile — Node.js 백엔드 서비스 빌드 자동화
# 변수 선언: 환경 변수 우선, 없으면 기본값 사용
APP_NAME    := my-api
VERSION     ?= $(shell git describe --tags --always --dirty 2>/dev/null || echo "dev")
DOCKER_REPO ?= registry.example.com/$(APP_NAME)
NODE_ENV    ?= development
PORT        ?= 3000

# .PHONY: 파일명과 충돌 방지 — 항상 레시피를 실행하도록 강제
.PHONY: all install lint test test-unit test-integration build \
        docker-build docker-push docker-run clean help

# 기본 타겟: make만 입력했을 때 실행
all: install lint test build

## 의존성 설치
install:
	@echo "==> Installing dependencies..."
	npm ci --prefer-offline

## 코드 품질 검사 (ESLint + Prettier)
lint:
	@echo "==> Running lint..."
	npm run lint
	npm run format:check

## 전체 테스트 (단위 + 통합)
test: test-unit test-integration

## 단위 테스트만 실행 (빠른 피드백)
test-unit:
	@echo "==> Running unit tests..."
	npm run test:unit -- --coverage --coverageThreshold='{"global":{"lines":80}}'

## 통합 테스트 (DB, 외부 서비스 필요)
test-integration:
	@echo "==> Running integration tests..."
	NODE_ENV=test npm run test:integration

## 프로덕션 빌드 (TypeScript 컴파일)
build:
	@echo "==> Building $(APP_NAME) $(VERSION)..."
	npm run build
	@echo "Build complete: dist/"

## Docker 이미지 빌드
docker-build:
	@echo "==> Building Docker image $(DOCKER_REPO):$(VERSION)..."
	docker build \
		--build-arg VERSION=$(VERSION) \
		--build-arg BUILD_DATE=$(shell date -u +"%Y-%m-%dT%H:%M:%SZ") \
		-t $(DOCKER_REPO):$(VERSION) \
		-t $(DOCKER_REPO):latest \
		.

## Docker 이미지를 레지스트리에 푸시
docker-push: docker-build
	@echo "==> Pushing $(DOCKER_REPO):$(VERSION)..."
	docker push $(DOCKER_REPO):$(VERSION)
	docker push $(DOCKER_REPO):latest

## 로컬 개발 서버 실행
docker-run:
	docker run --rm -p $(PORT):$(PORT) \
		-e NODE_ENV=$(NODE_ENV) \
		$(DOCKER_REPO):latest

## 빌드 산출물 및 캐시 삭제
clean:
	@echo "==> Cleaning..."
	rm -rf dist/ coverage/ node_modules/.cache

## 도움말 출력
help:
	@grep -E '^## ' Makefile | sed 's/## /  /'
```

`VERSION ?= $(shell git describe ...)` 패턴은 태그가 있으면 `v1.3.0`, 없으면 커밋 해시(`abc1234-dirty`)를 자동으로 사용한다. Docker 이미지에 이 값을 태그로 붙이면 "어느 커밋에서 빌드된 이미지인가"를 코드 없이 추적할 수 있다.

---

## 4. 단위 테스트 — Jest

단위 테스트는 함수 하나, 클래스 하나를 격리해서 검증한다. "격리"가 핵심이다. 외부 DB나 HTTP 서버 없이 실행되어야 한다. 그래서 모킹(mocking)이 중요해진다.

아래는 Express REST API 핸들러를 테스트하는 완성된 Jest 테스트 모음이다.

```javascript
// src/handlers/__tests__/userHandler.test.js
// 목적: userHandler의 비즈니스 로직만 검증 (DB, HTTP는 모킹)

const { getUserById, createUser } = require('../userHandler');
const userRepository = require('../../repositories/userRepository');
const emailService = require('../../services/emailService');

// 모듈 전체를 모킹 — 실제 DB 연결 없이 반환값을 제어
jest.mock('../../repositories/userRepository');
jest.mock('../../services/emailService');

describe('userHandler', () => {
  // 각 테스트 전 모든 모킹 상태를 초기화 (테스트 간 독립성 보장)
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getUserById', () => {
    it('존재하는 사용자 ID로 요청 시 200과 사용자 정보를 반환한다', async () => {
      // Arrange: 모킹된 저장소가 반환할 값을 설정
      const mockUser = { id: 1, name: '홍길동', email: 'hong@example.com' };
      userRepository.findById.mockResolvedValue(mockUser);

      const req = { params: { id: '1' } };
      const res = {
        status: jest.fn().mockReturnThis(), // 메서드 체이닝을 위해 this 반환
        json: jest.fn(),
      };

      // Act
      await getUserById(req, res);

      // Assert
      expect(res.status).toHaveBeenCalledWith(200);
      expect(res.json).toHaveBeenCalledWith({ data: mockUser });
      expect(userRepository.findById).toHaveBeenCalledWith(1); // 정수로 변환됐는지 확인
    });

    it('존재하지 않는 사용자 ID로 요청 시 404를 반환한다', async () => {
      // Arrange: null 반환 → 사용자 없음
      userRepository.findById.mockResolvedValue(null);

      const req = { params: { id: '999' } };
      const res = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn(),
      };

      // Act
      await getUserById(req, res);

      // Assert
      expect(res.status).toHaveBeenCalledWith(404);
      expect(res.json).toHaveBeenCalledWith({
        error: { code: 'USER_NOT_FOUND', message: expect.any(String) },
      });
    });

    it('저장소에서 예외 발생 시 500을 반환하고 에러를 로깅한다', async () => {
      // Arrange: DB 연결 실패 시뮬레이션
      const dbError = new Error('Connection refused');
      userRepository.findById.mockRejectedValue(dbError);

      const req = { params: { id: '1' } };
      const res = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn(),
      };

      // Act
      await getUserById(req, res);

      // Assert: 에러 세부 내용은 클라이언트에 노출하지 않음
      expect(res.status).toHaveBeenCalledWith(500);
      expect(res.json).toHaveBeenCalledWith({
        error: { code: 'INTERNAL_ERROR', message: 'Internal server error' },
      });
    });
  });

  describe('createUser', () => {
    it('유효한 입력으로 사용자 생성 시 201과 생성된 사용자를 반환하고 환영 이메일을 보낸다', async () => {
      // Arrange
      const input = { name: '이순신', email: 'lee@example.com', password: 'secure123' };
      const savedUser = { id: 42, name: input.name, email: input.email };

      userRepository.create.mockResolvedValue(savedUser);
      emailService.sendWelcome.mockResolvedValue(true);

      const req = { body: input };
      const res = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn(),
      };

      // Act
      await createUser(req, res);

      // Assert: 저장 + 이메일 발송 둘 다 호출됐는지 확인
      expect(userRepository.create).toHaveBeenCalledTimes(1);
      expect(emailService.sendWelcome).toHaveBeenCalledWith(savedUser.email);
      expect(res.status).toHaveBeenCalledWith(201);
    });

    it('이메일 형식이 잘못된 경우 422를 반환하고 저장소를 호출하지 않는다', async () => {
      const req = { body: { name: '테스트', email: 'not-an-email', password: '123' } };
      const res = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn(),
      };

      await createUser(req, res);

      // Assert: 유효성 검사에서 걸려 저장소까지 도달하지 않아야 함
      expect(res.status).toHaveBeenCalledWith(422);
      expect(userRepository.create).not.toHaveBeenCalled();
    });
  });
});
```

테스트 구조의 핵심은 `describe → it → Arrange/Act/Assert` 흐름이다. `beforeEach`에서 `clearAllMocks()`를 호출하는 이유는 앞선 테스트의 호출 횟수나 반환값이 다음 테스트에 영향을 주는 것을 막기 위해서다.

---

## 5. 통합 테스트 — pytest

통합 테스트는 여러 컴포넌트가 실제로 함께 동작하는지 검증한다. DB에 실제로 데이터를 넣고, API를 실제로 호출하며, 응답을 확인한다. 그래서 테스트 후 상태를 반드시 원복(teardown)해야 한다.

```python
# tests/integration/test_user_api.py
# 목적: 실제 PostgreSQL + FastAPI 스택이 올바르게 연동되는지 검증

import pytest
import httpx
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import User

# 테스트 전용 DB URL — 프로덕션 DB를 절대 오염시키지 않음
TEST_DATABASE_URL = "postgresql://testuser:testpass@localhost:5433/testdb"

@pytest.fixture(scope="session")
def db_engine():
    """세션 전체에서 한 번만 엔진 생성 (비용 절약)"""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)  # 테이블 생성
    yield engine
    Base.metadata.drop_all(bind=engine)   # 세션 종료 시 테이블 삭제


@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    각 테스트마다 독립된 트랜잭션을 제공한다.
    테스트 종료 시 rollback으로 DB 상태를 원복 — DELETE 없이도 깨끗하게 유지.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()

    yield session

    # Teardown: 테스트가 성공하든 실패하든 반드시 rollback
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """
    FastAPI 테스트 클라이언트 생성.
    get_db 의존성을 테스트 세션으로 교체해 실제 DB 대신 트랜잭션 내 세션 사용.
    """
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with httpx.Client(app=app, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def existing_user(db_session):
    """테스트에 필요한 기본 사용자 데이터를 미리 삽입"""
    user = User(name="기존 사용자", email="existing@example.com")
    db_session.add(user)
    db_session.flush()  # ID 생성을 위해 flush (commit은 안 함)
    return user


class TestUserAPI:
    def test_get_user_returns_200_for_existing_user(self, client, existing_user):
        """존재하는 사용자 조회 시 200과 사용자 정보를 반환해야 한다"""
        response = client.get(f"/api/users/{existing_user.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == existing_user.id
        assert data["email"] == "existing@example.com"

    def test_get_user_returns_404_for_missing_user(self, client):
        """존재하지 않는 ID 조회 시 404를 반환해야 한다"""
        response = client.get("/api/users/99999")

        assert response.status_code == 404
        assert response.json()["error"]["code"] == "USER_NOT_FOUND"

    def test_create_user_persists_to_db(self, client, db_session):
        """사용자 생성 후 DB에서 조회가 가능해야 한다"""
        payload = {"name": "신규 사용자", "email": "new@example.com"}

        response = client.post("/api/users", json=payload)

        assert response.status_code == 201
        user_id = response.json()["id"]

        # DB에서 직접 확인 (API를 신뢰하는 게 아니라 실제 저장을 확인)
        saved = db_session.query(User).filter_by(id=user_id).first()
        assert saved is not None
        assert saved.email == "new@example.com"

    def test_create_duplicate_email_returns_409(self, client, existing_user):
        """이미 존재하는 이메일로 생성 시도 시 409를 반환해야 한다"""
        payload = {"name": "중복 이메일", "email": existing_user.email}

        response = client.post("/api/users", json=payload)

        assert response.status_code == 409
```

`scope="function"` 픽스처의 rollback 패턴이 핵심이다. `DELETE FROM users WHERE ...` 쿼리를 직접 작성하는 방식은 테스트 순서에 따라 간섭이 생길 수 있다. 반면 트랜잭션을 시작하고 테스트 후 무조건 rollback하면 어떤 순서로 실행해도 DB 상태가 항상 깨끗하게 유지된다.

---

## 6. npm scripts 구성

`package.json`의 `scripts`는 팀이 공유하는 명령어 계약이다. 개발자가 "이 프로젝트 어떻게 실행해요?"라고 묻지 않아도 되게 만드는 것이 목적이다.

```json
{
  "name": "my-api",
  "version": "1.3.0",
  "scripts": {
    "start": "node dist/server.js",
    "dev": "ts-node-dev --respawn --transpile-only src/server.ts",
    "build": "tsc --project tsconfig.build.json",
    "build:watch": "tsc --project tsconfig.build.json --watch",

    "test": "jest --runInBand",
    "test:unit": "jest --testPathPattern='__tests__' --runInBand",
    "test:integration": "jest --testPathPattern='integration' --runInBand --forceExit",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",

    "lint": "eslint 'src/**/*.{ts,js}' --max-warnings 0",
    "lint:fix": "eslint 'src/**/*.{ts,js}' --fix",
    "format": "prettier --write 'src/**/*.{ts,js,json}'",
    "format:check": "prettier --check 'src/**/*.{ts,js,json}'",

    "typecheck": "tsc --noEmit",
    "validate": "npm run typecheck && npm run lint && npm run test:unit",

    "db:migrate": "npx prisma migrate deploy",
    "db:seed": "ts-node prisma/seed.ts",
    "db:reset": "npx prisma migrate reset --force"
  }
}
```

`validate` 스크립트는 "이 코드가 커밋 전 조건을 만족하는가"를 한 번에 확인하는 게이트다. PR 전에 `npm run validate`를 실행하는 습관을 들이면 CI에서 실패하는 빈도가 눈에 띄게 줄어든다.

---

## 7. .gitignore — Node.js 프로젝트

```gitignore
# 의존성 (버전 관리 불필요 — npm ci로 재현 가능)
node_modules/
.pnp
.pnp.js

# 빌드 산출물
dist/
build/
*.tsbuildinfo

# 테스트 커버리지 리포트
coverage/
.nyc_output/

# 환경 변수 (절대 커밋 금지 — .env.example은 커밋 허용)
.env
.env.local
.env.*.local

# 로그
*.log
npm-debug.log*

# 에디터 설정 (팀 통일 시 .editorconfig는 커밋 가능)
.vscode/settings.json
.idea/
*.swp

# OS 파일
.DS_Store
Thumbs.db

# Docker
*.env.docker
```

---

## 8. 테스트 피라미드와 전략

테스트 피라미드는 "어떤 테스트를 얼마나 작성해야 하는가"에 대한 시각적 가이드다. 아래로 갈수록 빠르고 저렴하며, 위로 갈수록 현실에 가깝지만 느리고 관리 비용이 높다.

```mermaid
graph TB
    subgraph pyramid["테스트 피라미드"]
        E2E["🔺 E2E / UI 테스트<br/>10% · 느림 · 비용 높음<br/>Cypress, Playwright"]
        INT["🔶 통합 테스트<br/>20% · 보통 · 실제 인프라 필요<br/>pytest, Testcontainers"]
        UNIT["🟩 단위 테스트<br/>70% · 빠름 · 격리됨<br/>Jest, JUnit, pytest"]
    end

    E2E --> INT --> UNIT

    style E2E fill:#ffcccc,stroke:#cc0000,color:#333
    style INT fill:#ffe4b5,stroke:#cc7700,color:#333
    style UNIT fill:#ccffcc,stroke:#007700,color:#333
```

단위 테스트가 70%를 차지하는 이유는 비용 대비 효과 때문이다. 함수 하나를 테스트하는 데 드는 시간은 수십 밀리초지만, E2E 테스트 하나는 수십 초에서 수 분이 걸린다. 피라미드가 뒤집히면(아이스크림 콘 안티패턴) CI 시간이 길어지고, 테스트가 왜 실패했는지 찾는 시간이 늘어난다.

### Bad: 테스트 게이트 없는 빌드

```bash
# 테스트 없이 바로 배포 — 프로덕션이 테스트 환경
npm run build
docker build -t my-api .
docker push registry/my-api:latest
# 결과: 런타임에 버그 발견, 롤백 비용 발생
```

### Good: 테스트 게이트가 있는 빌드

```bash
# 각 단계가 게이트 역할 — 앞 단계 실패 시 이후 단계 실행 안 됨
npm run lint          # 코드 품질 게이트
npm run test:unit     # 단위 테스트 게이트 (커버리지 80% 이하면 실패)
npm run test:integration  # 통합 테스트 게이트
npm run build         # 컴파일 게이트
docker build -t my-api:$(git rev-parse --short HEAD) .
docker push registry/my-api:$(git rev-parse --short HEAD)
# 결과: 문제가 배포 전에 발견됨, 어느 커밋이 원인인지 이미지 태그로 추적 가능
```

---

## 9. 핵심 정리

- **브랜칭 전략**은 배포 빈도와 팀 규모에 맞게 선택한다. 자주 배포한다면 TBD, 릴리스 주기가 있다면 GitFlow.
- **시맨틱 버저닝**은 번호가 아니라 변경의 영향 범위를 전달한다. MAJOR는 파괴적 변경, MINOR는 하위 호환 추가, PATCH는 버그 수정.
- **Makefile**은 언어에 무관하게 빌드 프로세스를 통일하는 가장 이식성 높은 도구다.
- **단위 테스트**는 모킹으로 격리하고, **통합 테스트**는 트랜잭션 rollback으로 부작용을 제거한다.
- **테스트 피라미드**는 단위 70 : 통합 20 : E2E 10 비율을 목표로 한다. 피라미드가 뒤집히면 CI가 느려지고 피드백 루프가 길어진다.

---

## 📚 다음 챕터

Ch05에서는 Jenkins, GitHub Actions, GitLab CI를 사용해 이번 챕터에서 구성한 빌드/테스트 파이프라인을 실제 CI/CD 워크플로에 연결하는 방법을 다룬다.
