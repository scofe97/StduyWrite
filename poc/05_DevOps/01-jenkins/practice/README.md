# Jenkins 실습 Quick Reference

## 환경 구성

```bash
# 환경 시작
docker compose up -d

# 상태 확인
docker compose ps

# 로그 확인
docker compose logs -f jenkins-controller

# 환경 종료
docker compose down

# 데이터 포함 완전 초기화
docker compose down -v
```

## 초기 설정: SSH 키 생성

Agent 연결을 위해 SSH 키 쌍을 생성해야 합니다. 최초 1회만 실행하면 됩니다.

```bash
# 1. SSH 키 쌍 생성 (practice/ 디렉토리에서 실행)
ssh-keygen -t rsa -b 4096 -f jenkins-agent-key -N "" -C "jenkins-agent"

# 2. 공개키를 환경변수로 설정
export AGENT_SSH_PUBKEY=$(cat jenkins-agent-key.pub)

# 3. 환경 시작
docker compose up -d

# 4. 개인키를 Jenkins Credentials에 등록
#    Jenkins UI > Manage Jenkins > Credentials > System > Global
#    Kind: SSH Username with private key
#    ID: agent-ssh-key
#    Username: jenkins
#    Private Key: jenkins-agent-key 파일 내용 붙여넣기
```

> 생성된 `jenkins-agent-key`, `jenkins-agent-key.pub` 파일은 `.gitignore`에 추가하세요.

## 접속 정보

| 서비스 | URL | 계정 |
|--------|-----|------|
| Jenkins UI | http://localhost:8080 | admin / admin |
| Jenkins API | http://localhost:8080/api/json | admin / admin |
| Docker Registry | http://localhost:5000 | (인증 없음) |
| Registry Catalog | http://localhost:5000/v2/_catalog | (인증 없음) |

## 주요 실습 시나리오

| # | 시나리오 | 챕터 | 설명 |
|---|---------|------|------|
| 1 | Freestyle Job 생성 | Ch02 | UI에서 직접 Job을 만들어 Jenkins 기본 동작을 이해한다 |
| 2 | 첫 번째 Jenkinsfile | Ch03 | Declarative Pipeline으로 Hello World 파이프라인을 작성한다 |
| 3 | Docker 빌드 파이프라인 | Ch04 | sample-app을 Docker 이미지로 빌드하고 Registry에 push한다 |
| 4 | Shared Library 적용 | Ch05 | 공통 빌드/배포 로직을 라이브러리로 추출한다 |
| 5 | Multi-branch Pipeline | Ch06 | 브랜치별 자동 파이프라인 트리거를 구성한다 |
| 6 | CasC 설정 변경 | Ch07 | casc.yaml 수정 후 Jenkins에 반영하는 흐름을 실습한다 |
| 7 | Prometheus 메트릭 수집 | Ch08 | Jenkins 메트릭을 Prometheus로 수집하고 확인한다 |

## 유용한 Jenkins CLI 명령어

```bash
# Jenkins CLI jar 다운로드
curl -O http://localhost:8080/jnlpJars/jenkins-cli.jar

# Job 목록 조회
java -jar jenkins-cli.jar -s http://localhost:8080/ -auth admin:admin list-jobs

# 빌드 트리거
java -jar jenkins-cli.jar -s http://localhost:8080/ -auth admin:admin build sample-app

# 플러그인 목록
java -jar jenkins-cli.jar -s http://localhost:8080/ -auth admin:admin list-plugins

# Jenkins 재시작
java -jar jenkins-cli.jar -s http://localhost:8080/ -auth admin:admin safe-restart
```

## 트러블슈팅 FAQ

### Q1: Jenkins가 시작되지 않음
```bash
# 로그 확인
docker compose logs jenkins-controller

# 원인: 메모리 부족인 경우가 많음
# 해결: Docker Desktop에서 메모리를 4GB 이상으로 설정
```

### Q2: "Setup Wizard" 화면이 나타남
```bash
# 원인: JAVA_OPTS에 runSetupWizard=false가 적용되지 않음
# 확인
docker exec jenkins-controller env | grep JAVA_OPTS

# 해결: docker-compose.yml의 environment 설정 확인 후 재시작
docker compose down && docker compose up -d
```

### Q3: Docker 명령어가 Agent에서 실행되지 않음
```bash
# 원인: Docker socket 마운트 또는 권한 문제
# 확인
docker exec jenkins-agent docker version

# 해결: docker.sock 권한 수정
docker exec -u root jenkins-agent chmod 666 /var/run/docker.sock
```

### Q4: Registry push 실패 (insecure registry)
```bash
# 원인: Docker가 HTTP registry를 신뢰하지 않음
# 해결: Docker Desktop > Settings > Docker Engine에 추가
{
  "insecure-registries": ["localhost:5000"]
}
# 이후 Docker Desktop 재시작
```

### Q5: 플러그인 설치 실패
```bash
# 원인: 네트워크 문제 또는 플러그인 의존성 충돌
# 수동 설치
docker exec jenkins-controller jenkins-plugin-cli --plugins workflow-aggregator

# 또는 Jenkins UI > Manage Jenkins > Plugins에서 수동 설치
```

### Q6: CasC 변경이 반영되지 않음
```bash
# Jenkins UI에서 수동 반영
# Manage Jenkins > Configuration as Code > Reload existing configuration

# 또는 컨테이너 재시작
docker compose restart jenkins-controller
```

## 데이터 관리

```bash
# Jenkins 데이터 백업 (볼륨 내용)
docker run --rm -v jenkins-data:/data -v $(pwd):/backup alpine \
  tar czf /backup/jenkins-backup.tar.gz -C /data .

# Jenkins 데이터 복원
docker run --rm -v jenkins-data:/data -v $(pwd):/backup alpine \
  tar xzf /backup/jenkins-backup.tar.gz -C /data
```
