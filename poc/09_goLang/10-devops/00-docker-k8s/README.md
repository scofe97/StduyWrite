# 20. Docker 및 Kubernetes

Go 애플리케이션의 컨테이너화 및 배포를 학습합니다.

## 학습 목표

- 멀티스테이지 Dockerfile 작성
- docker-compose로 로컬 개발 환경 구성
- Kubernetes 매니페스트 작성
- 컨테이너 최적화

> **심화 학습**: 컨테이너 내부 원리(Namespace, CGroups)는 **22-container-from-scratch** 모듈에서 다룹니다.

---

## 핵심 개념

### 멀티스테이지 빌드

```dockerfile
# 빌드 스테이지
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -o main .

# 실행 스테이지
FROM scratch
COPY --from=builder /app/main /main
ENTRYPOINT ["/main"]
```

### 베이스 이미지 비교

| 이미지 | 크기 | 특징 |
|--------|------|------|
| golang:1.21 | ~800MB | 빌드용 |
| alpine | ~5MB | 경량, musl libc |
| scratch | 0MB | 비어있음, 정적 바이너리 필요 |
| distroless | ~2MB | 최소 런타임, Google 제공 |

---

## 프로젝트 구조

```
20-docker-k8s/
├── README.md
├── EXERCISES.md
├── HINTS.md
├── LEARNED.md
├── Dockerfile            # 멀티스테이지 빌드
├── docker-compose.yml    # 로컬 개발 환경
├── .dockerignore
├── app/
│   ├── main.go          # 샘플 애플리케이션
│   └── go.mod
└── k8s/
    ├── deployment.yaml
    ├── service.yaml
    └── configmap.yaml
```

---

## 참조 자료

### Learning Go, 2nd Edition
- **01_Setting_Up_Your_Go_Environment.md**: Go 빌드 환경 이해
- **11_Go_Tooling.md**: 빌드 옵션, 크로스 컴파일 → Docker 이미지 최적화
- **10_Modules_Packages_and_Imports.md**: 의존성 관리 → 컨테이너 빌드 최적화

### 추가 참조
- [Docker Best Practices for Go](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Kubernetes for Go Developers](https://kubernetes.io/docs/tutorials/)
- [Distroless Images](https://github.com/GoogleContainerTools/distroless)

---

## 관련 모듈

| 모듈 | 주제 |
|------|------|
| **21-distributed-systems** | 분산 시스템 (Raft, Leader Election) |
| **22-container-from-scratch** | Go로 컨테이너 내부 구현 (Namespace, CGroups) |
