# Docker PoC Practice

Docker 학습 프로젝트의 실습 파일 모음입니다.

## 디렉토리 구조

```
practice/
├── README.md                    # 이 파일
├── Makefile                     # 실습 명령어 모음
├── sample-apps/                 # 샘플 애플리케이션
│   ├── go-api/                  # Go HTTP API
│   └── nginx-static/            # 정적 웹페이지
├── dockerfile/                  # Dockerfile 예제
│   ├── basic/                   # 기본 빌드 (Node.js)
│   ├── multistage/              # Multi-stage build (Go)
│   └── optimization/            # 최적화 비교
├── compose/                     # Docker Compose 예제
│   ├── basic/                   # 기본 스택 (nginx + redis)
│   ├── fullstack/               # 전체 스택 (frontend + backend + db)
│   └── profiles/                # 환경별 구성
├── networking/                  # 네트워킹 데모
│   └── network-demo.sh
├── volumes/                     # 볼륨 데모
│   └── volume-demo.sh
└── security/                    # 보안 데모
    └── scan-demo.sh
```

## 실행 순서

### 1. 기본 환경 확인
```bash
docker --version
docker compose version
```

### 2. Docker CLI 기초 (Ch02, Ch05)
```bash
make cli-basics
# http://localhost:8080 접속 확인
make cli-cleanup
```

### 3. Dockerfile 빌드 (Ch06)
```bash
# 기본 빌드
make build-basic
docker images | grep docker-poc

# Multi-stage 빌드
make build-multistage
docker images | grep docker-poc
```

### 4. Docker Compose (Ch07)
```bash
# 기본 스택
make compose-up
docker compose -f practice/compose/basic/docker-compose.yml ps
make compose-down

# 전체 스택
cd practice/compose/fullstack
docker compose up -d
docker compose ps
docker compose down

# 환경별 구성 (Profiles)
cd practice/compose/profiles
docker compose --profile dev up -d
docker compose --profile debug up -d
docker compose down
```

### 5. 네트워킹 (Ch08)
```bash
make net-demo
```

### 6. 볼륨 (Ch09)
```bash
make vol-demo
```

### 7. 보안 (Ch10)
```bash
make sec-scan
bash practice/security/scan-demo.sh
```

### 8. 전체 정리
```bash
make clean-all
```

## 샘플 애플리케이션

### go-api
- 경로: `sample-apps/go-api/`
- 포트: 8080
- Endpoints:
  - GET /health → {"status": "ok"}
  - GET /hello → {"message": "Hello Docker!"}
- 빌드: Multi-stage (golang:alpine → scratch)

### nginx-static
- 경로: `sample-apps/nginx-static/`
- 포트: 80
- 정적 HTML 페이지 제공

## Dockerfile 예제

### basic/
Node.js 애플리케이션 기본 빌드 예제
- FROM node:alpine
- npm install 캐시 최적화

### multistage/
Go 애플리케이션 Multi-stage build
- Stage 1: golang:alpine (빌드)
- Stage 2: scratch (실행)
- 이미지 크기 10MB 이하

### optimization/
Dockerfile 최적화 비교
- Dockerfile.bad: 캐시 비효율적
- Dockerfile.good: 레이어 캐싱 최적화

## Compose 예제

### basic/
nginx + redis 기본 스택
- 서비스 간 네트워크 연결
- 환경 변수 사용

### fullstack/
실전 풀스택 구성
- frontend: nginx (port 80)
- backend: go-api (port 8080)
- db: postgres (port 5432)
- cache: redis (port 6379)
- 의존성 관리 (depends_on)
- 헬스체크 설정

### profiles/
환경별 구성 분리
- dev: 기본 서비스
- debug: 추가 디버깅 도구 포함

## 네트워킹 데모

`networking/network-demo.sh`:
1. 커스텀 bridge 네트워크 생성
2. 컨테이너 2개 연결
3. DNS 이름으로 통신 확인
4. 정리

## 볼륨 데모

`volumes/volume-demo.sh`:
1. Named volume 생성
2. 컨테이너에 마운트
3. 데이터 쓰기
4. 컨테이너 삭제 후 데이터 영속성 확인
5. 정리

## 보안 데모

`security/scan-demo.sh`:
1. Docker Scout로 이미지 스캔
2. CVE 확인
3. 베이스 이미지 버전별 비교

## 주요 명령어 요약

```bash
# 빌드
docker build -t name:tag .

# 실행
docker run -d -p 8080:80 --name container-name image:tag

# 로그 확인
docker logs container-name

# 실행 중인 컨테이너
docker ps

# 정리
docker rm -f container-name
docker rmi image:tag

# Compose
docker compose up -d
docker compose ps
docker compose logs -f
docker compose down

# 네트워크
docker network ls
docker network inspect network-name

# 볼륨
docker volume ls
docker volume inspect volume-name

# 보안
docker scout quickview image:tag
```

## 문제 해결

### 포트 충돌
```bash
# 포트 사용 중인 프로세스 확인 (macOS)
lsof -i :8080

# 컨테이너 강제 종료
docker rm -f $(docker ps -aq)
```

### 디스크 공간
```bash
# 사용하지 않는 리소스 정리
docker system prune -a --volumes
```

### 네트워크 연결 실패
```bash
# 네트워크 재생성
docker network prune -f
```

## 참고 자료
- learning/ 디렉토리의 각 챕터별 LEARN.md
- Docker 공식 문서: https://docs.docker.com
