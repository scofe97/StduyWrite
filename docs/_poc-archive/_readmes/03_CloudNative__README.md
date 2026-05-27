# 03_CloudNative POC

## 개요
클라우드 네이티브 기술 스택(Docker, Kubernetes)의 핵심 개념과 실전 활용 실습 공간입니다.

## 디렉토리 구조
```
03_CloudNative/
├── README.md
├── 01-docker/          # Docker 핵심 개념과 실전 활용 (13챕터)
│   ├── learning/       # Ch01~Ch13 LEARN.md + INVESTIGATE.md
│   └── practice/       # 실습 프로젝트
├── 02-kubernetes/      # 쿠버네티스 실전 운영 실습 (20챕터)
│   ├── learning/       # Ch01~Ch20 LEARN.md + INVESTIGATE.md
│   └── practice/       # 실습 프로젝트
├── 03-service-mesh/    # Service Mesh (Linkerd + Istio + Cilium) (20챕터)
│   ├── learning/       # Ch01~Ch20 LEARN.md + INVESTIGATE.md
│   └── practice/       # Kind 클러스터 기반 실습
└── 04-oracle-cloud/    # Oracle Cloud Always Free Tier 구축 (3챕터)
    ├── learning/       # Ch01~Ch03 LEARN.md
    └── practice/       # Terraform 프로젝트
```

## 프로젝트 목록

| # | 프로젝트 | 챕터 수 | 예상 시간 | 설명 |
|---|---------|---------|----------|------|
| 01 | [Docker](01-docker/) | 13 | ~9h | Docker 핵심 개념과 실전 활용 (이미지, 컨테이너, 네트워킹, 볼륨, 멀티스테이지 빌드, 보안 등) |
| 02 | [Kubernetes](02-kubernetes/) | 20 | ~15h | 쿠버네티스 실전 운영 실습 (Pod, Service, ConfigMap, StatefulSet, Helm, Operator 등) |
| 03 | [Service Mesh](03-service-mesh/) | 20 | ~14h | Service Mesh 핵심 (Linkerd 2.19 + Istio 1.29 + Cilium, Gateway API, mTLS, Ambient Mesh) |
| 04 | [Oracle Cloud](04-oracle-cloud/) | 3 | ~2h | Oracle Cloud Always Free Tier 구축 (ARM VM, Terraform, 운영 관리) |

**총 56챕터, 예상 학습 시간: ~40시간**

## 학습 순서
1. **01-docker** (선행): Docker 기초 및 실전 활용
2. **02-kubernetes**: Kubernetes 운영 및 배포 자동화
3. **03-service-mesh**: Service Mesh (Linkerd, Istio, Cilium)
4. **04-oracle-cloud** (독립): Oracle Cloud Free Tier 인프라 구축

> Docker → Kubernetes → Service Mesh 순서로 학습 권장 (각 단계가 다음 단계의 기반)
> 04-oracle-cloud는 독립 주제로 순서 무관

## 관련 이론 문서

### docs 매핑
- **01-docker** → [docs/03_CloudNative/01_Docker/](../../docs/03_CloudNative/01_Docker/) (17개 문서)
  - Docker 아키텍처, 이미지 빌드, 네트워킹, 볼륨, 보안, 성능 최적화 등
- **02-kubernetes** → [docs/03_CloudNative/02_Kubernetes/](../../docs/03_CloudNative/02_Kubernetes/) (23개 문서)
  - K8s 아키텍처, 워크로드, 네트워킹, 스토리지, 배포 전략, Helm, Operator 등
- **03-service-mesh** → [docs/03_CloudNative/04_Linkerd/](../../docs/03_CloudNative/04_Linkerd/) (8개 문서)
  - Service Mesh 기초, Linkerd 배포/CLI/mTLS/정책 (Istio는 PoC 챕터에서 직접 다룸)

### 전체 이론 문서
- [docs/03_CloudNative](../../docs/03_CloudNative/)

## 상태
- [x] 01-docker (13챕터 구조 완성, Ch01 작성 중)
- [ ] 02-kubernetes (20챕터 구조 완성, 작성 예정)
- [x] 03-service-mesh (20챕터 구조 완성, 전체 작성 완료)
- [x] 04-oracle-cloud (3챕터 작성 완료)
