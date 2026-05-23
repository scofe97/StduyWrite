# Nexus Repository Manager - Practice

## Quick Start

### 1. Nexus 시작
```bash
docker compose up -d
```

### 2. 초기 비밀번호 확인
```bash
docker exec nexus cat /nexus-data/admin.password
```

### 3. 리포지토리 자동 생성
```bash
# 초기 비밀번호로 로그인 후 admin123으로 변경한 뒤 실행
chmod +x nexus-config/setup-repos.sh
./nexus-config/setup-repos.sh
```

### 4. 모니터링 (선택)
```bash
docker compose --profile monitoring up -d
```

## 서비스 접속 정보

| 서비스 | URL | 비고 |
|--------|-----|------|
| Nexus UI | http://localhost:8081 | admin / admin123 |
| Docker Push | localhost:8082 | docker-hosted |
| Docker Pull | localhost:8083 | docker-group |
| Prometheus | http://localhost:9090 | monitoring 프로필 |
| Grafana | http://localhost:3000 | admin / admin |
| Jenkins | http://localhost:8080 | ci 프로필 |

## 파일 구조

| 디렉토리 | 설명 | 관련 챕터 |
|----------|------|-----------|
| nexus-config/ | Nexus 설정, 초기화 스크립트 | Ch02, Ch03 |
| nginx/ | Reverse proxy 설정 | Ch02, Ch08 |
| monitoring/ | Prometheus + Grafana | Ch11 |
| web-file-manager/ | REST API 기반 파일 관리 UI | Ch05 |
| sample-projects/ | Maven/npm/Docker 샘플 | Ch03, Ch07 |
| scripts/ | 백업/복구/정리 스크립트 | Ch09, Ch10 |
| http/ | REST API 테스트 (.http 파일) | Ch05 |

## Jenkins 연동
```bash
docker compose -f docker-compose.yml -f docker-compose.ci.yml up -d
```
