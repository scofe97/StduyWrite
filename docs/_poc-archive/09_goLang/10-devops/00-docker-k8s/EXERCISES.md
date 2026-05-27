# 20. Docker & Kubernetes 실습 과제

## 1단계: Dockerfile 작성

### 과제 1-1: 기본 Dockerfile
- [ ] `app/main.go`에 간단한 HTTP 서버 작성
- [ ] 단일 스테이지 Dockerfile 작성
- [ ] 이미지 빌드 및 실행 확인

### 과제 1-2: 멀티스테이지 빌드
- [ ] 빌드 스테이지와 실행 스테이지 분리
- [ ] `scratch` 또는 `distroless` 베이스 이미지 사용
- [ ] 이미지 크기 비교 (단일 vs 멀티스테이지)

```bash
# 힌트: 이미지 크기 확인
docker images | grep myapp
```

### 과제 1-3: 최적화
- [ ] `.dockerignore` 작성
- [ ] 빌드 캐시 최적화 (의존성 먼저, 소스 나중)
- [ ] CGO_ENABLED=0 설정 이해

---

## 2단계: docker-compose

### 과제 2-1: 로컬 개발 환경
- [ ] Go 앱 + PostgreSQL 구성
- [ ] 볼륨 마운트로 코드 핫 리로드
- [ ] 네트워크 연결 확인

### 과제 2-2: 환경 변수 관리
- [ ] `.env` 파일 사용
- [ ] 개발/운영 환경 분리

---

## 3단계: Kubernetes 매니페스트

### 과제 3-1: 기본 리소스
- [ ] Deployment 작성 (replicas: 3)
- [ ] Service 작성 (ClusterIP)
- [ ] ConfigMap으로 설정 주입

### 과제 3-2: 헬스체크
- [ ] `/health` 엔드포인트 구현
- [ ] `/ready` 엔드포인트 구현
- [ ] livenessProbe, readinessProbe 설정

---

## 검증 체크리스트

### Docker
```bash
# 이미지 빌드
docker build -t myapp:v1 .

# 컨테이너 실행
docker run -d -p 8080:8080 myapp:v1

# 헬스체크
curl http://localhost:8080/health
```

### Kubernetes (minikube 또는 kind)
```bash
# 적용
kubectl apply -f k8s/

# 확인
kubectl get pods
kubectl get svc

# 로그
kubectl logs -f deployment/myapp
```

---

## 심화 학습

컨테이너 내부 원리(Namespace, CGroups, chroot)를 직접 구현하며 학습하려면:

➡️ **22-container-from-scratch** 모듈로 이동하세요.

---

## 학습 완료 후

`LEARNED.md`에 다음을 기록하세요:
- 멀티스테이지 빌드의 장점
- scratch vs distroless 차이
- CGO_ENABLED=0이 필요한 이유
- 헬스체크 엔드포인트의 목적
