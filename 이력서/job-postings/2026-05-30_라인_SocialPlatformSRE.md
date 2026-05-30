# LINE — Social Platform SRE & Service Operations Engineer

## Meta
- 회사: LINE (LY Corporation, 글로벌 메신저·소셜 플랫폼)
- 포지션: Social Platform SRE & Service Operations Engineer
- URL: https://careers.linecorp.com/ko/jobs/2527
- 접수일: 상시채용
- 출처: LINE CAREERS (careers.linecorp.com)
- 기록일: 2026-05-30

## 기술 스택
**필수**: Ansible, Grafana, Prometheus, Github Actions, ArgoCD, Helm, Java 기반 서비스 운영, DevOps/SRE(3년 이상)

**우대**: 글로벌 서비스 인프라·데이터 스토리지 구축·대규모 트래픽 처리, 애플리케이션·시스템 성능 튜닝, SLI/SLO 정의 및 모니터링 최적화, 외국어(영어 또는 일본어)

## 주요 업무
- 소셜 플랫폼(Java 기반) 서비스의 신뢰성·성능 유지 및 운영
- Ansible·Grafana·Prometheus·Github Actions·ArgoCD·Helm 기반 인프라 운영·자동화
- 모니터링·알림·옵저버빌리티 환경 운영 및 장애 대응
- (검색 기준 본문 일부 — 상세 책무 원문 전체는 본인 확인 필요)

> 주요업무 일부 항목: 본문 정보 부족 — 본인 확인 필요 (LINE careers 페이지가 WebFetch 차단, 검색 스니펫 기반 정리)

## 자격 요건·우대사항
**자격 요건**
- DevOps 또는 SRE 경력 3년 이상
- Java 기반 서비스 운영 전문성
- Ansible, Grafana, Prometheus, Github Actions, ArgoCD, Helm 등 다양한 도구 활용 경험
- 논리적·체계적 문제해결 및 분석 역량
- 여러 팀과 원활히 협업하는 커뮤니케이션 역량
- 해외 출장·파견 결격 사유 없음

**우대사항**
- 글로벌 서비스용 인프라·데이터 스토리지 구축·운영 및 대규모 트래픽 처리 경험
- 성능 개선을 위한 애플리케이션·시스템 튜닝 및 분석 기반 솔루션 제안 경험
- 서비스·인프라 SLI/SLO 지표 정의 및 이를 기반으로 한 모니터링·운영 환경 최적화 경험
- 외국어(영어 또는 일본어)로 업무 수행 가능

**전형 절차**
- 서류 전형 → 1차 면접 → 2차 면접 → 평판조회·처우 협의 → 최종 합격

## 매칭 분석 (vs 지원자)
**강점 (어필 가능한 마일스톤)**
- **Grafana·Prometheus 운영**: 개인 GCP 클러스터에 Grafana·Loki·Tempo·Prometheus 자가 관찰성 구성 → 필수 도구 직접 매칭
- **ArgoCD·Helm·Github Actions**: Helm 차트 K8s 배포 + ArgoCD GitOps + CI/CD 자동화 → 필수 3종 정확 매칭
- **Java 서비스 운영**: Java 17/21·Spring Boot 3.x로 TROMBONE 운영 → 필수 "Java 기반 서비스 운영" 직접 매칭
- **DevOps/SRE 3년+**: 3년차 백엔드 풀스택 + DevOps 플랫폼 담당 → "3년 이상" 자격선 충족
- **SLI/SLO·성능 튜닝(우대)**: 동시성 직렬화·이벤트드리븐 + 관찰성 스택 → SLI/SLO·튜닝 우대 부분 매칭

**공백**
- **Ansible 직접 운영 경험 부족** — 본인은 Helm·kubeadm 중심, 구성관리는 Ansible보다 선언적 K8s 위주. 학습 필요
- **대규모 글로벌 트래픽 정량 경험 부재** (알려진 공백) — LINE급 글로벌 트래픽 미경험. 개인 클러스터 규모로 우회
- **외국어 업무(영어·일본어)** — 우대이자 해외 출장 전제. 영어 readiness는 본인 확인 필요
- **데이터 스토리지 대규모 운영 경험 제한** — Kafka/Redpanda는 있으나 글로벌 스토리지 인프라 규모는 미경험

**매칭 신뢰도**: 상 — 필수 도구셋(Grafana·Prometheus·ArgoCD·Helm·Github Actions·Java)이 본인 스택과 거의 1:1. Ansible·외국어만 보완하면 강한 후보. 경력 3년 자격선도 충족.

## 도메인 한 줄 + 예상 기술부채
**도메인**: 글로벌 메신저 LINE의 소셜 플랫폼(Java 기반) 신뢰성을 SRE·서비스 운영으로 보장.

**예상 기술부채 2~3개**
1. **글로벌 멀티리전 트래픽·지연 편차** — 지역별 트래픽·레이턴시 불균형이 SLO 위반으로 누적. 본인 관찰성 + SLI/SLO 정의 경험으로 리전별 모니터링 표준화 기여 가능
2. **Java 서비스 성능·GC 튜닝 부채** — 대규모 Java 서비스의 JVM·GC 미튜닝이 지연·장애 원인. 본인 Spring Boot·JVM 경험으로 튜닝 PoC 가능
3. **구성관리(Ansible)·배포(ArgoCD) 혼재** — 명령형 Ansible과 선언형 ArgoCD가 섞이면 드리프트 발생. GitOps 일원화 방향 제안 가능(본인 ArgoCD 경험)

## 90일 가설
입사 후 첫 30일은 소셜 플랫폼 Java 서비스군의 SLI/SLO·Grafana 대시보드·알림 커버리지와 Ansible·ArgoCD 운영 흐름을 점검합니다. 다음 30일은 서비스 1개를 골라 SLO 위반 패턴 또는 JVM 성능 병목을 1건 이상 찾아 튜닝·모니터링 개선 PoC를 제안합니다. 마지막 30일은 ArgoCD·Helm 배포 표준 또는 알림 노이즈 정리 1개를 운영에 적용해 회복·알람 일관성을 검증합니다.

## 원문 (참고)
> Experience with various tools such as Ansible, Grafana, Prometheus, Github Actions, ArgoCD, and Helm.
>
> 3+ years of DevOps or SRE experience, Java-based service operations expertise.
>
> Experience defining SLI/SLO metrics and optimizing monitoring and operational environments.
>
> Ability to conduct business in a foreign language (English or Japanese).
>
> No disqualifying reasons for overseas business trips and assignments.
