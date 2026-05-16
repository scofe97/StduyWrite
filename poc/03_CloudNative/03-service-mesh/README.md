# Service Mesh 학습 프로젝트

> 이 카테고리는 write/09_cloud/service-mesh/로 이관 완료. 삭제 예정 (2026-05-19). 최종본과 실습은 `write/09_cloud/service-mesh/`를 기준으로 참조한다.

Service Mesh 핵심 개념(Linkerd + Istio + Cilium)을 학습하고 Kind 클러스터에서 실습하는 프로젝트.

## 구조

| 디렉토리 | 설명 |
|----------|------|
| `learning/` | 20챕터 이론 (LEARN.md + INVESTIGATE.md) |
| `practice/` | Kind 클러스터 기반 실습 |

## 챕터 목록

### Part 1: Service Mesh Foundations (Ch01-04)
| Ch | 제목 | 시간 |
|----|------|------|
| 01 | Service Mesh 기초와 2026 지형도 | 40m |
| 02 | 프록시 아키텍처 비교 | 35m |
| 03 | Gateway API와 트래픽 관리 | 40m |
| 04 | mTLS와 제로 트러스트 | 35m |

### Part 2: Linkerd Deep Dive (Ch05-09)
| Ch | 제목 | 시간 |
|----|------|------|
| 05 | Linkerd 아키텍처 (2.19) | 40m |
| 06 | Linkerd 설치와 메시 구성 | 45m |
| 07 | Linkerd 트래픽 관리 | 40m |
| 08 | Linkerd 보안과 정책 | 45m |
| 09 | Linkerd 관측성 | 40m |

### Part 3: Istio Deep Dive (Ch10-15)
| Ch | 제목 | 시간 |
|----|------|------|
| 10 | Istio 아키텍처 (1.29) | 45m |
| 11 | Istio Ambient Mesh | 50m |
| 12 | Istio 설치와 메시 구성 | 45m |
| 13 | Istio 트래픽 관리 | 50m |
| 14 | Istio 보안 | 45m |
| 15 | Istio 관측성 | 40m |

### Part 4: Advanced & Decision (Ch16-20)
| Ch | 제목 | 시간 |
|----|------|------|
| 16 | 멀티클러스터 서비스 메시 | 45m |
| 17 | Linkerd vs Istio vs Cilium 비교 | 40m |
| 18 | eBPF와 Cilium Service Mesh | 40m |
| 19 | 프로덕션 패턴 | 45m |
| 20 | 도입 전략과 의사결정 | 40m |

**총 학습 시간**: ~14시간

## 참조

- 이론: `docs/03_CloudNative/04_Linkerd/` (기존 8챕터)
- Docker: `poc/03_CloudNative/01-docker/`
- Kubernetes: `poc/03_CloudNative/02-kubernetes/`
