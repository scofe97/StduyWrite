---
title: AI 인프라 — Claude로 (정독 노트 MOC)
tags: [moc, devops, cicd, gitops, kubernetes, ai, claude, book]
status: draft
related:
  - ../../README.md
  - ../../roadmap.md
  - ../fdsd_fundamentals-devops/README.md
  - ../cicd_cicd-patterns/README.md
updated: 2026-06-30
---

# AI 인프라 — Claude로
---
> Claude Code를 도구 삼아 GCP·Kubernetes(GKE `notiflex-cluster`) 위에 배포 인프라를 직접 구축해 나가는 실습형 단행본입니다(저자 sysnet4admin). 환경 구성에서 시작해 GitOps·관측 가능성·무중단 배포·규모 확장·위험 작업 통제까지, 가상 스타트업 서비스 **Notiflex**(B2B 알림 SaaS, Go 표준 라이브러리)를 **9개 장**에 걸쳐 점진적으로 엔터프라이즈 수준으로 키웁니다. 책의 핵심 개념은 GitOps에 AI를 더한 **GitAIOps** — 인프라를 클로드 코드와 대화하며 선언하고, 그 결과를 깃에 커밋하는 흐름입니다.

## 이 책을 여기 두는 이유

책의 무게중심은 **CI/CD·GitOps·배포 전략**입니다. ArgoCD로 깃 푸시만으로 배포하고, Rolling Update → Blue/Green → Canary로 배포 전략을 한 단계씩 발전시키며, 멀티 노드풀·멀티테넌시로 규모를 키우는 흐름이 본문의 뼈대입니다. 이는 `04_cicd`가 모으는 "도구를 관통하는 배포 이론·전략"의 경계 안에 들어옵니다. 그래서 형제 단행본인 [`fdsd_fundamentals-devops`](../fdsd_fundamentals-devops/README.md)·[`cicd_cicd-patterns`](../cicd_cicd-patterns/README.md)와 같은 `book/{슬러그}/` 자리에 둡니다.

"Claude로 만든다"는 *주제*가 아니라 *방법*입니다. 각 장은 인프라를 한 조각 쌓을 때마다 그 작업을 Claude Code와 어떻게 협업했는지를 마무리 절에 정리합니다(`CLAUDE.md` 행동규칙 → 메모리 컨텍스트 → 아키텍처 결정 기록 → `claude-context/` → `settings.local.json` 권한 분리 → `command-guardrails/`). 모델 자체의 특성·LLM 일반론은 [`12_AI/`](../../../../12_AI/README.md), 순수 K8s 네트워킹·오브젝트 이론은 [`08_cloud/kubernetes/`](../../../../08_cloud/kubernetes/README.md)가 맡습니다. 이 책은 그 둘을 *배포 인프라를 만드는 워크플로우*로 엮는 자리입니다.

## 장 구성

원본은 단행본을 주차별로 캡처한 스크린샷이며 총 **9개 장**입니다(§1.4.1 전체 흐름표로 확정). 1~7장은 전체 섹션을 판독해 확인했고, 8장 일부 절과 9장은 아직 미판독입니다(아래 표와 [roadmap.md](roadmap.md)에 표기). 모든 장은 끝에서 두 절이 "마무리(그 장의 Claude 협업 산출물)" + "N장 가드레일 살펴보기"로 닫힙니다.

| 장 | 제목 | 핵심 | 섹션 확인 |
|----|------|------|:---:|
| 1 | 개발자에게 인프라가 다가온 시대 | DevOps·클라우드 네이티브·풀스택 확장 / 쿠버네티스=공통 언어 / GitOps→**GitAIOps** / Notiflex 시나리오 / 가드레일 | 전체 |
| 2 | 환경 구성 | GCP 계정·클로드 코드·gcloud·깃허브 저장소·GKE 클러스터 / 첫 배포(빌드·매니페스트·커밋) / /update-docs 스킬 | 전체 |
| 3 | 첫 번째 배포 파이프라인 | 푸시 배포의 한계 → ArgoCD·GitOps → 롤링 업데이트 → GitHub Actions CI → CI+CD 연결 | 전체 |
| 4 | 관측 가능성 한 번에 구축하기 | Prometheus+Grafana 메트릭, Loki+Fluent Bit 로그, PrometheusRule 알림 | 전체 |
| 5 | 무중단 배포 | Rolling Update의 한계, Gateway API 트래픽, Blue/Green(Argo Rollouts) | 전체 |
| 6 | 엔터프라이즈를 위한 기반 정비 | Valkey 상태 공유, Google Secret Manager, 점진적 배포 Canary | 전체 |
| 7 | 규모 확장 | SMB 구조의 한계, 멀티 노드풀, App of Apps+Sync Wave, 멀티테넌시 네임스페이스 | 전체 |
| 8 | 위험 작업의 안전한 실행 | `command-guardrails/`로 위험 작업 절차 통제 (§8.4 마무리 확인) | 일부 |
| 9 | GitAIOps: 살아있는 운영 표준 | 그동안 쌓인 코드·설정·문서를 AI로 분석해 운영 표준으로 정리(회고) | 미판독 |

> 배포 전략이 장을 거치며 발전합니다 — 3장 Rolling Update → 5장 Blue/Green → 6장 Canary. 동시에 Claude 협업 산출물도 발전합니다 — 2장 `/update-docs` → 3장 `CLAUDE.md` → 4장 메모리 컨텍스트 → 5장 아키텍처 결정 기록 → 6장 `claude-context/` → 7장 `settings.local.json` → 8장 `command-guardrails/`. 9장이 이 모두를 "살아있는 운영 표준"으로 회고합니다.

## 작성된 정독 노트

| 노트 | 범위 |
|------|------|
| [01-01 개발자에게 인프라가 다가온 시대](./01-01.개발자에게%20인프라가%20다가온%20시대.md) | §1.1 인프라가 개발자에게 온 배경 + §1.2 쿠버네티스=공통 언어·AI 동료 |
| [01-02 GitOps에서 GitAIOps로](./01-02.GitOps에서%20GitAIOps로.md) | §1.3 책의 핵심 개념 — GitOps 선언적 관리 → 빈자리 → AI가 채움 |
| [01-03 이 책의 지도](./01-03.이%20책의%20지도%20—%20구성·Notiflex%20시나리오·가드레일.md) | §1.4 구성·저장소 + §1.5 Notiflex 시나리오 + §1.6 가드레일 |
| [02-01 환경 구성](./02-01.환경%20구성%20—%20GCP·클로드%20코드·GKE%20클러스터.md) | §2.1~§2.5 GCP·클로드 코드·gcloud·깃허브·GKE |
| [02-02 첫 배포와 마무리](./02-02.첫%20배포와%20마무리%20—%20빌드·매니페스트·커밋·스킬.md) | §2.6~§2.9 빌드·매니페스트·커밋·/update-docs |

## 출처·캡처 메모

- 원본: Drive `book/ai-infra-claude-week1~4/` 스크린샷 (week1 53장 / week2 61장 / week3 53장 / week4 66장, 총 ~233장). 캡처 해상도는 1254×1259로 충분 — 작은 본문은 ImageMagick 상/하단 크롭(`-crop -resize`)으로 확대해 판독함
- week1=Ch1+Ch2 · week2=Ch3+Ch4 · week3=Ch5+Ch6 · week4=Ch7+Ch8(+Ch9). 각 주차 2개 장, 마지막 주차에 9장 회고 포함
- 가이드 저장소 `_Book_GitAIOps`(CLAUDE.md·가드레일) + 완성본 `notiflex-platform` (github.com/sysnet4admin). 서비스 `notiflex`는 Go 표준 라이브러리 API 서버, GKE `notiflex-cluster` 위에서 동작하며 장을 거치며 Kafka·Valkey·Tempo/Loki/Prometheus 등이 더해짐

## 톤·시각화 (정독 노트 작성 시)

상위 [`04_cicd/README.md`](../../README.md)의 톤 규약을 상속합니다. 정독 노트는 합니다체로 쓰고, 각 편 도입부에 요약 SVG 1장(`_assets/`)을 임베드하며 배포 흐름·상태 전이에 Mermaid를 더합니다. roadmap은 원문 키워드 기록이므로 `status: reference`로 두고 사실·섹션 제목을 보존합니다.

> 1장·2장 정독 노트 5편 완료(2026-06-30). 3장(week2)부터 이어서 작성하며, 도입부 요약 SVG(`_assets/`)는 추후 보강합니다.
