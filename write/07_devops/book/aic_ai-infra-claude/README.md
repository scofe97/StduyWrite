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

"Claude로 만든다"는 *주제*가 아니라 *방법*입니다. 각 장은 인프라를 한 조각 쌓을 때마다 그 작업을 Claude Code와 어떻게 협업했는지를 마무리 절에 정리합니다(`CLAUDE.md` 행동규칙 → 메모리 컨텍스트 → 아키텍처 결정 기록 → `claude-context/` → `settings.local.json` 권한 분리 → `command-guardrails/`). 모델 자체의 특성·LLM 일반론은 `12_AI/` <!-- 링크 끊김(2026-08): ../../../../12_AI/README.md -->, 순수 K8s 네트워킹·오브젝트 이론은 `08_cloud/kubernetes/` <!-- 링크 끊김(2026-08): ../../../../08_cloud/kubernetes/README.md -->가 맡습니다. 이 책은 그 둘을 *배포 인프라를 만드는 워크플로우*로 엮는 자리입니다.

## 장 구성

원본은 단행본을 주차별로 캡처한 스크린샷이며 총 **9개 장**입니다(§1.4.1 전체 흐름표로 확정). 1~9장 전체 섹션을 판독해 확인했습니다(week1~4, 총 ~233장). 모든 장은 끝에서 두 절이 "마무리(그 장의 Claude 협업 산출물)" + "N장 가드레일 살펴보기"로 닫힙니다(9장은 회고 장이라 마무리 대신 §9.5 다음 단계로 닫힘).

| 장 | 제목 | 핵심 | 섹션 확인 |
|----|------|------|:---:|
| 1 | 개발자에게 인프라가 다가온 시대 | DevOps·클라우드 네이티브·풀스택 확장 / 쿠버네티스=공통 언어 / GitOps→**GitAIOps** / Notiflex 시나리오 / 가드레일 | 전체 |
| 2 | 환경 구성 | GCP 계정·클로드 코드·gcloud·깃허브 저장소·GKE 클러스터 / 첫 배포(빌드·매니페스트·커밋) / /update-docs 스킬 | 전체 |
| 3 | 첫 번째 배포 파이프라인 | 푸시 배포의 한계 → ArgoCD·GitOps → 롤링 업데이트 → GitHub Actions CI → CI+CD 연결 | 전체 |
| 4 | 관측 가능성 한 번에 구축하기 | Prometheus+Grafana 메트릭, Loki+Fluent Bit 로그, PrometheusRule 알림 | 전체 |
| 5 | 무중단 배포 | Rolling Update의 한계, Gateway API 트래픽, Blue/Green(Argo Rollouts) | 전체 |
| 6 | 엔터프라이즈를 위한 기반 정비 | Valkey 상태 공유, Google Secret Manager, 점진적 배포 Canary | 전체 |
| 7 | 규모 확장 | SMB 구조의 한계, 멀티 노드풀, App of Apps+Sync Wave, 멀티테넌시 네임스페이스 | 전체 |
| 8 | 고도화 | Kafka(Strimzi KRaft) 이벤트 드리븐, Tempo 분산 트레이싱, CronJob 배치, `command-guardrails/` | 전체 |
| 9 | GitAIOps: 살아있는 운영 표준 | 저장소 분석(코드:매니페스트 4.7배)·의사결정 종합·살아있는 문서·GitAIOps 루프(회고) | 전체 |

> 배포 전략이 장을 거치며 발전합니다 — 3장 Rolling Update → 5장 Blue/Green → 6장 Canary. 동시에 Claude 협업 산출물도 발전합니다 — 2장 `/update-docs` → 3장 `CLAUDE.md` → 4장 메모리 컨텍스트 → 5장 아키텍처 결정 기록 → 6장 `claude-context/` → 7장 `settings.local.json` → 8장 `command-guardrails/`. 9장이 이 모두를 "살아있는 운영 표준"으로 회고합니다.

## 작성된 정독 노트

| 노트 | 범위 |
|------|------|
| [01-01 개발자에게 인프라가 다가온 시대](./01-01.개발자에게%20인프라가%20다가온%20시대.md) | §1.1 인프라가 개발자에게 온 배경 + §1.2 쿠버네티스=공통 언어·AI 동료 |
| [01-02 GitOps에서 GitAIOps로](./01-02.GitOps에서%20GitAIOps로.md) | §1.3 책의 핵심 개념 — GitOps 선언적 관리 → 빈자리 → AI가 채움 |
| [01-03 이 책의 지도](./01-03.이%20책의%20지도%20—%20구성·Notiflex%20시나리오·가드레일.md) | §1.4 구성·저장소 + §1.5 Notiflex 시나리오 + §1.6 가드레일 |
| [02-01 환경 구성](./02-01.환경%20구성%20—%20GCP·클로드%20코드·GKE%20클러스터.md) | §2.1~§2.5 GCP·클로드 코드·gcloud·깃허브·GKE |
| [02-02 첫 배포와 마무리](./02-02.첫%20배포와%20마무리%20—%20빌드·매니페스트·커밋·스킬.md) | §2.6~§2.9 빌드·매니페스트·커밋·/update-docs |
| [03-01 푸시 배포의 한계와 ArgoCD GitOps](./03-01.푸시%20배포의%20한계와%20ArgoCD%20GitOps%20—%20설치·연결·롤링·롤백.md) | §3.1~§3.3 드리프트 사례·ArgoCD 설치·Application 연결·롤링 업데이트·git revert 롤백 |
| [03-02 깃허브 액션 CI와 ArgoCD 연결](./03-02.깃허브%20액션%20CI와%20ArgoCD%20연결%20—%20빌드부터%20배포까지.md) | §3.4~§3.7 CI 구축·CI-ArgoCD 연결·무한 루프 방어·CLAUDE.md 행동 규칙·가드레일 |
| [04-01 관측 가능성과 메트릭](./04-01.관측%20가능성과%20메트릭%20—%20프로메테우스·그라파나.md) | §4.1~§4.2 3요소 개념·Prometheus Pull·kube-prometheus-stack 설치·PromQL |
| [04-02 로그와 알림](./04-02.로그와%20알림%20—%20Loki·Fluent%20Bit·PrometheusRule.md) | §4.3~§4.6 Loki 라벨 인덱싱·Fluent Bit·PrometheusRule·메모리 마무리·가드레일 |
| [05-01 Rolling Update의 한계와 Gateway API](./05-01.Rolling%20Update의%20한계와%20Gateway%20API.md) | §5.1~§5.2 Rolling Update 두 빈틈·Gateway API 역할 분리·HealthCheckPolicy |
| [05-02 Blue/Green 무중단 전환과 아키텍처 결정 기록](./05-02.Blue-Green%20무중단%20전환과%20아키텍처%20결정%20기록.md) | §5.3~§5.5 Blue/Green·Argo Rollouts·activeService/previewService·ADR 마무리·가드레일 |
| [06-01 Valkey 캐시와 Google Secret Manager](./06-01.Valkey%20캐시와%20Google%20Secret%20Manager.md) | §6.1~§6.2 Pod 간 상태 공유·Valkey INCR·Secret Manager CSI·Workload Identity |
| [06-02 점진적 배포 Canary와 claude-context](./06-02.점진적%20배포%20Canary와%20claude-context.md) | §6.3~§6.5 Canary setWeight/pause·claude-context 3층 지식 구조·가드레일 |
| [07-01 SMB 구조의 한계와 멀티 노드풀](./07-01.SMB%20구조의%20한계와%20멀티%20노드풀.md) | §7.1~§7.2 리소스 경합·격리 불가·nodeSelector 4방식·Spot VM·노드풀 생성 |
| [07-02 App of Apps와 멀티테넌시](./07-02.App%20of%20Apps와%20멀티테넌시.md) | §7.3~§7.6 App of Apps·Sync Wave·네임스페이스 격리·cross-namespace DNS·settings.local.json |
| [08-01 Kafka 이벤트 드리븐과 Tempo 분산 트레이싱](./08-01.Kafka%20이벤트%20드리븐과%20Tempo%20분산%20트레이싱.md) | §8.1~§8.2 Kafka Strimzi KRaft·Consumer offset·관측 3요소·Tempo·OpenTelemetry |
| [08-02 CronJob 배치 자동화와 command-guardrails](./08-02.CronJob%20배치%20자동화와%20command-guardrails.md) | §8.3~§8.5 CronJob concurrencyPolicy·command-guardrails 3단 절차·가드레일 |
| [09-01 GitAIOps — 살아있는 운영 표준의 탄생](./09-01.GitAIOps%20—%20살아있는%20운영%20표준의%20탄생.md) | §9.1~§9.6 저장소 분석·의사결정 종합·살아있는 문서·GitAIOps 루프·다음 단계 |

## 출처·캡처 메모

- 원본: Drive `book/ai-infra-claude-week1~4/` 스크린샷 (week1 53장 / week2 61장 / week3 53장 / week4 66장, 총 ~233장). 캡처 해상도는 1254×1259로 충분 — 작은 본문은 ImageMagick 상/하단 크롭(`-crop -resize`)으로 확대해 판독함
- week1=Ch1+Ch2 · week2=Ch3+Ch4 · week3=Ch5+Ch6 · week4=Ch7+Ch8(+Ch9). 각 주차 2개 장, 마지막 주차에 9장 회고 포함
- 가이드 저장소 `_Book_GitAIOps`(CLAUDE.md·가드레일) + 완성본 `notiflex-platform` (github.com/sysnet4admin). 서비스 `notiflex`는 Go 표준 라이브러리 API 서버, GKE `notiflex-cluster` 위에서 동작하며 장을 거치며 Kafka·Valkey·Tempo/Loki/Prometheus 등이 더해짐

## 톤·시각화 (정독 노트 작성 시)

상위 [`04_cicd/README.md`](../../README.md)의 톤 규약을 상속합니다. 정독 노트는 합니다체로 쓰고, 형제 폴더와 동일하게 07-04 책 요약 템플릿 구조(핵심 요약 → 학습 목표 → 본문 정리 → 심화 학습 → 실무 적용 → 체크리스트 → 면접 관점 정리 → 참고 자료)를 따릅니다. 각 편에 Mermaid 1장 이상을 두고, 심화 학습(책 밖 조사분)은 본문 정리와 섹션으로 분리해 출처 링크를 남깁니다. roadmap은 원문 키워드 기록이므로 `status: reference`로 두고 사실·섹션 제목을 보존합니다.

> 1장·2장 정독 노트 5편 완료(2026-06-30), 07-04 구조로 재구성 + 심화·예제 코드 보강(2026-07-04). 3장·4장(week2) 4편, 5장·6장(week3) 4편, 7·8·9장(week4) 5편 완료(2026-07-04) — **9개 장 전편 정독 노트 18편 완성**. 도입부 요약 SVG(`_assets/`)는 추후 보강합니다.
