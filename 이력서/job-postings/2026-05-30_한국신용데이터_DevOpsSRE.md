# 한국신용데이터(KCD) — DevOps Engineer (SRE팀)

## Meta
- 회사: 한국신용데이터 (KCD, 소상공인 핀테크, 2022 유니콘)
- 포지션: DevOps Engineer (SRE팀)
- URL: https://www.wanted.co.kr/wd/132623
- 접수일: 상시채용
- 출처: 원티드
- 기록일: 2026-05-30

## 기술 스택
**필수**: AWS ECS/EKS, Kubernetes, GitHub Enterprise·Actions, Jenkins, ArgoCD, Terraform·Ansible(IaC), Datadog, ElasticSearch, CloudWatch
**우대**: 본문 정보 부족 — 본인 확인 필요 (공고에 별도 우대사항 섹션 없음)

## 주요 업무
- AWS ECS/EKS 기반 인프라 구축 및 운영
- CI/CD 환경 구축 및 운영 (GitHub Enterprise, Actions, Jenkins, ArgoCD)
- 모니터링 시스템 구축 및 운영 (Datadog, ElasticSearch, CloudWatch)
- Site 관리·개선, 자동화, 프로세스 정의, 장애 관리, 비용 최적화

## 자격 요건·우대사항
**자격 요건**
- AWS EKS 기반 컨테이너 서비스 및 CI/CD 운영 경험 (전체 경력 5~18년)
- 애플리케이션 모니터링 시스템 구축/운영 경험
- IaC 도구 사용 경험 (Terraform, Ansible 등)
- 프로그래밍 언어 경험 (Java, Go, Python 등)
- Unix/Linux 및 네트워크 구조 이해
- 문제 해결 능력 및 지속적 학습 역량

**우대사항**
- 본문 정보 부족 — 본인 확인 필요

## 매칭 분석 (vs 지원자)
**강점 (어필 가능한 마일스톤)**
- **EKS + CI/CD(ArgoCD/Jenkins)**: K8s 운영 + 트럼본 ArgoCD/Jenkins 파이프라인 실행엔진 → 필수 직접 매칭(도구 정확 일치)
- **Kubernetes + CKA**: 개인 GCP 3노드 자가호스팅 + CKA → 필수 매칭
- **모니터링 시스템 구축**: 개인 GCP에 Grafana·Loki·Tempo·Prometheus 관찰성 자가 구성 → "모니터링 구축/운영" 매칭(Datadog은 상용 갭)
- **Java/Python 언어**: Java 17/21 주력 + Python 자동화 → "Java, Go, Python 등" 직접 매칭
- **GitHub Actions·Jenkins CI/CD**: Jenkins 멀티 인스턴스 표준화 + Job 이관 자동화 → 필수 매칭
- **핀테크 변경관리 도메인**: 본인 결재(변경관리) 도메인 = 소상공인 금융 서비스의 감사·추적 요구와 정합

**공백**
- **경력 밴드 미달 (5~18년 vs 3년차)** — 가장 큰 갭. SRE팀 시니어 포지션 성격. 본인은 3년차로 하단보다 2년 부족. 깊이로 보완 필요하거나 포지션 레벨 재확인 필요
- **Terraform 직접 작성 경험 부족** (IaC 최우선 공백) — Ansible/Terraform 실무 학습 필요
- **AWS 상용 운영 경험 부재** (자격증만) — ECS/EKS/CloudWatch는 AWS 고유. GCP→AWS 매핑 답변 준비
- **Datadog 직접 운영 경험 없음** — OSS 관찰성(Grafana/Loki/Tempo)만 운영. 상용 APM 학습 또는 "관찰성 사고 회로" 일반화 답변
- **대용량 트래픽 정량 메트릭 부족** (알려진 공백) — 약 200만 사업장 트래픽 규모 대비 정량 운영 경험 보강 필요

**매칭 신뢰도**: 중 — 도구 스택(EKS·ArgoCD·Jenkins·모니터링)은 다중 정확 매칭이고 핀테크 변경관리 도메인이 정합하나, 요구 경력 5~18년이 3년차와 갭이 커서 포지션 레벨 적합성이 신뢰도를 끌어내림

## 도메인 한 줄 + 예상 기술부채
**도메인**: 소상공인 대상 핀테크(캐시노트 등). 약 200만 사업장에 서비스하는 유니콘으로, 대규모 트래픽 SRE 운영이 핵심.
**예상 기술부채 2~3개**
1. **ECS와 EKS 이중 런타임 운영 부담** — ECS/EKS 병행은 배포·관찰성 표준이 갈라지기 쉬움. ArgoCD GitOps로 EKS 측 표준화 후 점진 수렴 가능
2. **대규모 사업장 트래픽의 비용·장애 트레이드오프** — 200만 사업장 = 비용 최적화와 장애 격리가 상시 과제. Datadog SLO + 비용 추적 대시보드로 정량화 가능 (관찰성 스택 운영 경험 전이)
3. **금융 데이터 변경관리·감사 추적 요구** — 핀테크는 모든 인프라 변경이 감사 대상. GitOps git 이력을 변경관리 증적으로 연결하는 설계 가능 (결재·변경관리 도메인 직접 경험)

## 90일 가설
입사 후 첫 30일은 ECS/EKS 이중 런타임의 배포·관찰성 표준 일관성과 Datadog 기반 SLO·알람 커버리지, 그리고 변경관리 증적 경로를 점검합니다. 다음 30일은 CI/CD 흐름 1개를 골라 Terraform 미적용 구간이나 ArgoCD 표준 미준수를 1건 이상 찾아 코드화 PoC를 제안합니다. 마지막 30일은 대규모 트래픽 서비스 1종의 장애 패턴을 분석해 자동 회복·비용 최적화 정책 1건을 검증하고 장애 대응 런북을 표준화합니다.

## 원문 (참고)
> CI/CD 환경 구축 및 운영 (Github Enterprise, Actions, Jenkins, ArgoCD)
> AWS ECS/EKS 기반 인프라 구축 및 운영
> IaC 도구 사용 경험 (Terraform, Ansible 등)
> 모니터링 시스템 구축 및 운영 (Datadog, ElasticSearch, CloudWatch)
