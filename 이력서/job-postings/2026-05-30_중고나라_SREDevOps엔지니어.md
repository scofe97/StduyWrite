# 중고나라 — SRE(DevOps) 엔지니어

## Meta
- 회사: 중고나라 (중고거래 커머스 플랫폼)
- 포지션: SRE(DevOps) 엔지니어
- URL: https://www.wanted.co.kr/wd/343038
- 접수일: 상시채용
- 출처: 원티드
- 기록일: 2026-05-30

## 기술 스택
**필수**: AWS, Docker, Kubernetes, Bitbucket, ArgoCD, Argo Rollout, Datadog, Prometheus, Grafana, Loki, Sentry, Shell Script, Golang, Node.js, MySQL, Redis, MongoDB
**우대**: 본문 정보 부족 — 본인 확인 필요 (공고에 별도 우대사항 섹션 없음)

## 주요 업무
- AWS 기반 전사 인프라 운영
- 대규모 트래픽 환경에서 장애 대응 및 사후 분석
- CI/CD 파이프라인 구축 및 운영
- 성능 및 비용 최적화

## 자격 요건·우대사항
**자격 요건**
- 1~3년의 SRE, DevOps, 시스템 엔지니어 경력 (공고 표기, 채용 밴드 1~5년)
- Linux/Unix 운영체제 이해 및 경험
- AWS, GCP, Azure 등 클라우드 인프라 구축 및 운영 경험
- Shell 등 스크립트 언어 자동화 경험
- 컨테이너 및 Kubernetes 기본 지식

**우대사항**
- 본문 정보 부족 — 본인 확인 필요

## 매칭 분석 (vs 지원자)
**강점 (어필 가능한 마일스톤)**
- **경력 밴드 정확 일치 (1~3년)**: 본인 3년차가 요구 밴드에 정확히 안착 → 5건 중 가장 좋은 경력 적합도
- **Kubernetes + CKA**: 개인 GCP 3노드 자가호스팅 + CKA → "컨테이너·K8s" 요건을 기본 지식 이상으로 초과 충족
- **ArgoCD + Argo Rollout**: 트럼본 ArgoCD/GitOps + 개인 ArgoCD 자가호스팅 → 필수 직접 매칭. Argo Rollout(카나리/블루그린)은 동시성·점진배포 사고와 정합
- **관찰성 스택(Prometheus·Grafana·Loki)**: 개인 GCP에 동일 OSS 스택 자가 구성 → 정확 매칭(드문 OSS 도구 일치)
- **Shell·자동화**: Jenkins·인프라 자동화 스크립팅 경험 → "스크립트 자동화" 매칭
- **커머스 대규모 트래픽·장애 대응**: 분산 트랜잭션·동시성 직렬화(비관적 락) 경험 → "대규모 트래픽 장애 대응·사후 분석" 사고 회로 정합

**공백**
- **AWS 상용 운영 경험 부재** (자격증만) — 전사 인프라가 AWS. GCP 운영을 AWS로 매핑하는 답변 준비
- **Golang·Node.js 자동화 경험 부족** — 자동화 언어가 Go/Node 중심. 본인 주력은 Java/Python. Shell·Python으로 우선 어필, Go 보강
- **Datadog·Sentry 직접 운영 경험 없음** — OSS(Prometheus/Grafana/Loki)는 매칭되나 상용 APM/에러트래킹은 학습 필요
- **Redis·MongoDB 운영 경험 부족** (Redis는 알려진 공백) — MySQL은 강하나 Redis/MongoDB 운영 보강 필요
- **대용량 트래픽 정량 메트릭 부족** (알려진 공백) — 중고거래 트래픽 규모 대비 정량 SRE 경험 보강 필요

**매칭 신뢰도**: 상 — 경력 밴드(1~3년)가 정확히 맞고 ArgoCD·Argo Rollout·OSS 관찰성 스택·K8s가 다중 직접 매칭. 핵심 공백은 AWS 상용운영과 Go/상용 APM으로 한정되어 5건 중 적합도 최상위권

## 도메인 한 줄 + 예상 기술부채
**도메인**: 국내 최대 중고거래 커머스 플랫폼. 대규모 트래픽과 다수 데이터 스토어(MySQL·Redis·MongoDB) 위에서 SRE 신뢰성 운영이 핵심.
**예상 기술부채 2~3개**
1. **대규모 트래픽 장애의 사후 분석 표준 부재** — "장애 대응·사후 분석"이 명시 = 포스트모템·SLO 체계가 진행형일 가능성. Datadog/Grafana SLO + 표준 포스트모템 템플릿으로 회로화 가능 (관찰성 스택 운영 경험 전이)
2. **점진 배포(Argo Rollout) 도입기 카나리 안정성** — Argo Rollout 카나리/블루그린은 트래픽 분기·롤백 기준 설계가 까다로움. 동시성·멱등 사고로 안전한 롤아웃 게이트 설계 가능
3. **멀티 데이터스토어(Redis/MongoDB/MySQL) 일관성·비용** — 스토어가 셋이면 캐시 무효화·정합성·비용이 누적. 본인 비관적 락·일관성 사고로 캐시·정합 패턴 점검 가능 (단 Redis 운영은 학습 병행)

## 90일 가설
입사 후 첫 30일은 전사 AWS 인프라의 관찰성 커버리지와 Argo Rollout 점진 배포의 롤백 기준, 그리고 장애 사후 분석 표준의 일관성을 점검합니다. 다음 30일은 CI/CD·배포 흐름 1개를 골라 카나리 롤아웃 기준 미비나 SLO 미정의 구간을 1건 이상 찾아 게이트·대시보드 PoC를 제안합니다. 마지막 30일은 대규모 트래픽 장애 1종에 대한 자동 탐지·알람·포스트모템 흐름을 검증하고 점진 배포 롤백 정책을 표준화합니다.

## 원문 (참고)
> 1~3년의 SRE, DevOps, 시스템 엔지니어
> 대규모 트래픽 환경에서 장애 대응 및 사후 분석
> CI/CD: Bitbucket, ArgoCD, Argo Rollout
> 모니터링: Datadog, Prometheus, Grafana, Loki, Sentry
