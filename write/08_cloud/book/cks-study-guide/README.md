---
title: CKS Study Guide — 정독 인덱스
tags: [moc, study-index, book, cks, kubernetes-security, cluster-hardening, certification]
status: draft
source:
  - 《Certified Kubernetes Security Specialist (CKS) Study Guide》(Benjamin Muschko, O'Reilly, 2023, ISBN 978-1098132972) — 1판 (2판 존재는 확인 안 됨)
  - 챕터 PDF 폴더 — GoogleDrive/내 드라이브/book/Certified Kubernetes Security Specialist (CKS) Study Guide/ (7개 장 + 부록)
  - https://lovereading.co.uk/book/9781098132972/isbn/Certified-Kubernetes-Security-Specialist-CKS-Study-Guide-by-Benjamin-Muschko.html  # 저자·출판사·ISBN·출판일 2023-06-23 확인 (2026-11-05 조회)
  - https://www.cncf.io/blog/2023/02/01/kubernetes-and-cloud-security-associate-kcsa-certification-coming-in-q3-2023/  # KCSA 발표 2023-02-01, 정식 출시는 2023 3분기 예고 (2026-11-05 조회)
  - https://training.linuxfoundation.org/blog/kubernetes-and-cloud-native-security-associate-kcsa-launches/  # KCSA 출시 보도자료 2024-02-27 (2026-11-05 조회)
related:
  - ../container-security/README.md
  - ../kubernetes-in-action/README.md
  - ../kubernetes-up-and-running/README.md
  - ../../../roadmap/k8s-roadmap.md
  - ../../README.md
learning:
  topic: cks-study-guide
  scope: durable
  level: 기본
  last_verified:
  blocked_count:
  next_lesson: "1장 01-01 정독 노트 작성"
updated: 2026-11-05
---

# CKS Study Guide — 정독 인덱스
---
> 이 폴더는 《Certified Kubernetes Security Specialist (CKS) Study Guide》(Benjamin Muschko, O'Reilly, 2023)를 장 단위로 정독하며 정리하는 책-종속 학습노트입니다. 챕터 PDF를 하나씩 읽은 뒤 한 편씩 채워 넣습니다.

## 이 책을 여기 두는 이유

> 이 책은 클러스터 운영자가 하드닝 절차를 직접 치는 시험 실기 관점을 맡습니다. 격리·공급망·탐지의 원리는 형제 노트에 맡기고, 이 폴더에는 CKS 고유 내용만 남깁니다.

### 하드닝 절차 중심의 책

`08_cloud`는 "클러스터 내부에서 어떻게 돌아가는가"를 다루는 카테고리입니다. 이 책은 그 질문을 **클러스터 하드닝**(hardening, 기본 설정이 열어 둔 공격 표면을 하나씩 닫는 일) 축으로 파고듭니다.

저자는 CKS 시험 커리큘럼 여섯 도메인의 순서를 그대로 따라 장을 구성했다고 밝힙니다. 장마다 공격 시나리오를 먼저 보인 뒤 막는 설정과 도구를 붙입니다.

독자는 CKA(Certified Kubernetes Administrator) 수준의 운영 지식을 갖췄다고 전제하고, 겹치는 기초는 반복하지 않는다고 1장에서 밝힙니다.[^author] 그래서 이 책은 시험 실기 관점에서 "이 설정을 어디서 어떻게 바꾸는가"를 중심에 둡니다.

### 형제 책과 보는 층의 차이

[『Container Security』](../container-security/README.md)는 커널이 세우는 격리 경계를 파고듭니다. 무엇이 무엇을 못 보게 막는가가 질문입니다.

[『Kubernetes in Action』](../kubernetes-in-action/README.md)은 오브젝트를 다룹니다. 무엇을 배포하는가가 질문입니다. 이 책은 운영자가 직접 치는 **하드닝 절차**를 다룹니다.

### 위임 대상과 CKS 고유 내용

겹치는 주제의 기초 설명은 형제 노트로 링크를 걸어 위임합니다. 위임 대상은 다음과 같습니다.

- 격리 경계와 샌드박싱(seccomp·AppArmor·gVisor·Kata)의 원리는 [컨테이너 격리 강화](../container-security/08-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC%20%EA%B0%95%ED%99%94%20%E2%80%94%20%EC%83%8C%EB%93%9C%EB%B0%95%EC%8B%B1%EC%9D%98%20%EC%84%B8%20%EA%B0%88%EB%9E%98.md)와 [컨테이너 격리 깨뜨리기](../container-security/09-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC%20%EA%B9%A8%EB%9C%A8%EB%A6%AC%EA%B8%B0%20%E2%80%94%20%EC%84%A4%EC%A0%95%20%ED%95%98%EB%82%98%EB%A1%9C%20%EB%AC%B4%EB%84%88%EC%A7%80%EB%8A%94%20%EA%B2%BD%EA%B3%84.md)가 맡습니다.
- 이미지 공급망의 원리는 [이미지 공급망 보안](../container-security/06-02.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EA%B3%B5%EA%B8%89%EB%A7%9D%20%EB%B3%B4%EC%95%88%20%E2%80%94%20%EB%B9%8C%EB%93%9C%EB%B6%80%ED%84%B0%20%EB%B0%B0%ED%8F%AC%EA%B9%8C%EC%A7%80.md)가, 런타임 탐지의 원리는 [컨테이너 런타임 보호](../container-security/13-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%9F%B0%ED%83%80%EC%9E%84%20%EB%B3%B4%ED%98%B8%20%E2%80%94%20%EC%A0%95%EC%83%81%EC%9D%84%20%EC%A0%95%EC%9D%98%ED%95%B4%20%EC%9D%B4%EC%83%81%EC%9D%84%20%EC%9E%A1%EB%8B%A4.md)가 맡습니다.
- NetworkPolicy의 일반 동작은 [NetworkPolicy와 DNS](../networking-and-kubernetes/04-03.NetworkPolicy%EC%99%80%20DNS%20%E2%80%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%95%88%EC%9D%98%20%EB%B0%A9%ED%99%94%EB%B2%BD%EA%B3%BC%20%EC%9D%B4%EB%A6%84.md)가 맡습니다.
- RBAC의 설계와 운영은 [RBAC 노트](../kubernetes-up-and-running/14-01.RBAC%20%E2%80%94%20%EC%9D%B8%EA%B0%80%EB%A5%BC%20%EC%84%A4%EA%B3%84%ED%95%98%EA%B3%A0%20%EC%9A%B4%EC%98%81%ED%95%98%EB%8A%94%20%EB%B2%95.md)가, 어드미션 정책(Gatekeeper)은 [Policy and Governance](../kubernetes-up-and-running/20-01.Policy%20and%20Governance%20%E2%80%94%20Gatekeeper%20%EB%A1%9C%20%EB%A7%8C%EB%93%A4%EA%B8%B0%20%EC%A0%84%EC%97%90%20%EB%A7%89%EA%B3%A0%20%EB%A7%8C%EB%93%A0%20%EB%92%A4%EC%97%90%20%EC%84%B8%EB%8A%94%20%EB%B2%95.md)가 맡습니다.

이 폴더에 남는 CKS 고유 내용은 PDF 목차에서 확인한 것만 듭니다.

- 2장: kube-bench로 CIS 벤치마크를 돌려 나온 위반 고치기, Ingress의 TLS 종단 설정, 노드 메타데이터 서버 접근 차단, 쿠버네티스 Dashboard 접근 제한, 플랫폼 바이너리 체크섬 검증
- 3장: CertificateSigningRequest로 사용자 만들기, ServiceAccount 토큰 자동 마운트 끄기
- 4장: 호스트 OS의 서비스·패키지·포트 줄이기와 방화벽 규칙
- 5장: etcd 저장 암호화, RuntimeClass 지정
- 6장: ImagePolicyWebhook, Hadolint·Kubesec·Trivy
- 7장: Falco 규칙 작성, audit policy

### 로드맵 속 자리

[쿠버네티스 로드맵](../../../roadmap/k8s-roadmap.md)에서는 자료 표에 우선순위 추천, 읽을 범위 2~7장, 자리 6단계로 올라 있습니다. 6단계 「보안과 확장」의 개념 표에서는 API 접근 하드닝(3장), 감사 로그(7장)처럼 형제 책에 대응 노트가 없는 행의 출처 칸이 이 책을 가리킵니다.



## 장별 목표

> 각 장 PDF 앞머리의 저자 선언을 `pdftotext`로 추출해 근거로 삼았습니다. 원문에 없는 목표를 추측해 넣지 않습니다.

| 장 | 제목 | 저자가 선언한 목표 | 주요 토픽 |
|----|------|------------------|----------|
| 1 | Exam Details and Resources | CKS 응시자가 가장 먼저 묻는 질문에 답함 — 자격증의 대상 독자, 커리큘럼, 시험 환경, 팁과 추가 학습 자료 | 쿠버네티스 자격증 학습 경로(KCNA·KCSA·CKAD·CKA·CKS), 시험 목표와 여섯 도메인, 시험에 걸린 쿠버네티스 프리미티브와 외부 도구, 허용 문서, 연습 환경 |
| 2 | Cluster Setup | 시험 첫 도메인인 클러스터 설정·구성의 보안 측면만 다룸 — 일반 관리자 책임은 제외 | NetworkPolicy, CIS 벤치마크(kube-bench), Ingress TLS, 노드 포트·API 엔드포인트·GUI 보호, 바이너리 체크섬 |
| 3 | Cluster Hardening | 클러스터를 처음 설정한 뒤 가능한 한 안전하게 유지하는 주제를 다룸 | API 서버 요청 처리, API 접근 제한, RBAC, ServiceAccount, 쿠버네티스 업그레이드 |
| 4 | System Hardening | 클러스터 노드를 돌리는 호스트 시스템의 보안을 다룸 — 근본적으로 Linux 핵심 기능이며, 컨테이너 안 프로세스가 호스트에서 할 수 있는 일을 제한하는 도구로 마무리 | 호스트 OS 최소화, IAM 역할(사용자·그룹·파일 권한), 외부 네트워크 접근 최소화, AppArmor, seccomp |
| 5 | Minimizing Microservice Vulnerabilities | Pod 수준 보안 설정의 거버넌스와 강제를 다룸 — 쿠버네티스 핵심 기능과 외부 도구, 그리고 Pod 사이 암호화 통신 | securityContext, Pod Security Admission, OPA Gatekeeper, Secret, etcd 암호화, 컨테이너 런타임 샌드박스(gVisor·Kata), mTLS |
| 6 | Supply Chain Security | 컨테이너 이미지를 설계·빌드·최적화하는 과정과 모범 사례를 다룸 — 다른 팀이 만든 이미지를 가져다 쓸 때의 취약점 스캔 포함 | 베이스 이미지 축소, 이미지 서명·다이제스트, 허용 레지스트리 제한(OPA Gatekeeper·ImagePolicyWebhook), Hadolint·Kubesec 정적 분석, Trivy |
| 7 | Monitoring, Logging, and Runtime Security | 커리큘럼의 마지막 도메인으로, 주로 호스트·컨테이너 수준의 의심스러운 활동을 탐지하는 일을 다룸 — 시작된 컨테이너를 바꾸지 못하게 하는 불변성과 클러스터 이벤트 로그 수집 포함 | 행위 분석, Falco, 컨테이너 불변성, audit log |
| 부록 | Answers to Review Questions | 2~7장 끝의 샘플 연습 문제에 대한 답 | 장별 풀이(명령과 매니페스트), 1장은 해당 없음 |

### 시험 도메인과 장의 대응

1장 본문이 밝힌 CKS 도메인 비중입니다. 저자는 책의 장 구성이 커리큘럼을 그대로 따른다고 적었으므로 도메인 하나가 장 하나에 대응합니다.

| 도메인 | 비중 | 장 |
|--------|-----:|----|
| Cluster Setup | 10% | 2 |
| Cluster Hardening | 15% | 3 |
| System Hardening | 15% | 4 |
| Minimize Microservice Vulnerabilities | 20% | 5 |
| Supply Chain Security | 20% | 6 |
| Monitoring, Logging, and Runtime Security | 20% | 7 |



## 작성된 정독 노트

> 편을 작성하는 대로 채우며, 아직 쓰지 않은 편은 상태만 "작성 예정"으로 둡니다. 제목 칸은 장 제목을 옮긴 가제입니다.

| 편 | 제목 | 상태 |
|----|------|------|
| 01-01 | Exam Details and Resources (Ch1 전체, 가제) | 작성 예정 |
| 02-01 | Cluster Setup 전반부 (Ch2 전반부, 가제) | 작성 예정 |
| 02-02 | Cluster Setup 후반부 (Ch2 후반부, 가제) | 작성 예정 |
| 03-01 | Cluster Hardening (Ch3 전체, 가제) | 작성 예정 |
| 04-01 | System Hardening (Ch4 전체, 가제) | 작성 예정 |
| 05-01 | Minimizing Microservice Vulnerabilities 전반부 (Ch5 전반부, 가제) | 작성 예정 |
| 05-02 | Minimizing Microservice Vulnerabilities 후반부 (Ch5 후반부, 가제) | 작성 예정 |
| 06-01 | Supply Chain Security (Ch6 전체, 가제) | 작성 예정 |
| 07-01 | Monitoring, Logging, and Runtime Security (Ch7 전체, 가제) | 작성 예정 |

### 편 나누기 계획

한 편은 원문 4,000~5,000단어를 기준으로 하고, 경계는 그 근처의 원문 절 경계에 맞춥니다(`learning-method` 스킬의 정독 노트 세션 규약). 장별 단어 수는 `pdftotext`로 쟀습니다.

| 장 | 단어 수 | 계획 |
|----|-------:|------|
| 1 | 2,453 | 한 편 |
| 2 | 8,002 | 두 편 후보. Ingress TLS 절이 끝나고 노드 메타데이터·포트 절이 시작되는 지점에서 나눕니다. 앞 약 4,400단어(NetworkPolicy·CIS 벤치마크·Ingress TLS), 뒤 약 3,600단어(노드 메타데이터와 포트·Dashboard·바이너리 체크섬·연습 문제) |
| 3 | 5,718 | 한 편 |
| 4 | 5,600 | 한 편 |
| 5 | 8,460 | 두 편 후보. 보안 컨텍스트·PSA·OPA 절이 끝나고 Secret 절이 시작되는 지점에서 나눕니다. 앞 약 3,800단어, 뒤 약 4,700단어(Secret과 etcd 암호화·런타임 샌드박스·mTLS·연습 문제) |
| 6 | 7,431 | 한 편으로 두되, 기준 상한을 넘으므로 01 편을 쓰기 전에 다시 잽니다. 나눈다면 공급망 절과 정적 분석 절의 경계가 후보이며 앞 약 4,600단어, 뒤 약 2,800단어입니다 |
| 7 | 5,880 | 한 편 |
| 부록 | 5,409 | 별도 편을 두지 않습니다. 부록은 2~7장 연습 문제의 답이므로 각 장 노트의 복습 절로 흡수하는 것을 추천값으로 둡니다 |



## 학습 상태

> 세션을 새로 열 때 이 표부터 읽습니다. 정독본의 STATE.md 대용입니다.

| 항목 | 현재 값 |
|------|--------|
| 진행률 | 0/7 장 (부록은 각 장 복습 절로 흡수 예정). 정독 노트 0편 |
| 난이도 레벨 | 미정 |
| 막힌 지점 | 없음 |
| 다음 레슨 후보 | 01-01 (1장 Exam Details and Resources) |
| 최근 검증 결과 | 이 README의 `verify-gate.sh --type=learning --style=jondae` 결과는 작성 보고서에 있습니다 (2026-11-05) |
| 원문 정오 누적 | 0 |
| 버전 차이 기록 | 0 |
| 복습 회차 | 0 |



## 번호 체계와 작성 규약

> 파일명은 `NN-MM.제목.md`이고, 버전에 따라 바뀌는 값은 쿠버네티스 버전과 함께 적습니다.

`NN`은 책의 장 번호이고 `MM`은 그 장을 여러 편으로 나눌 때의 편 순번입니다. 정밀 도식은 `_assets/`에 SVG로 두고, 흐름·관계 중 자동 배치가 나은 것은 Mermaid로 본문에 직접 그립니다.

이 책은 쿠버네티스 1.26 기준으로 쓰였다고 1장이 밝힙니다. 보안 기능은 버전에 따라 기본값과 필드가 바뀌므로, 노트에 적는 값은 반드시 쿠버네티스 버전과 함께 적습니다. 특히 PodSecurityPolicy 제거와 Pod Security Admission, AppArmor 지정 방식, seccomp 기본값, 시험이 기준으로 삼는 쿠버네티스 버전이 그렇습니다. 원문과 현재 값이 다르면 원문 정오 누적과 버전 차이 기록에 나누어 적습니다.

작성 규약은 writing 스킬의 책 요약 템플릿과 정독 노트 세션 규약을 따르되, "Spring 앱 개발 관점" 절은 접점이 자연스러운 장에만 둡니다. 이 책은 클러스터 운영자의 하드닝 절차가 본체이므로, 순수 호스트·클러스터 설정 장에 Spring을 붙이면 연결이 억지스러워집니다. 접점이 생길 수 있는 후보는 Secret 소비와 컨테이너 불변성이 나오는 5·7장 정도이며, 실제 적용 여부는 해당 편을 쓸 때 정합니다.



## 관련 문서

- [『Container Security』 정독본](../container-security/README.md) — 같은 `book/` 영역, 격리 경계 중심 관점의 짝이자 샌드박싱·공급망·런타임 탐지 원리의 위임 대상
- [『Kubernetes in Action, 2판』 정독본](../kubernetes-in-action/README.md) — 오브젝트 중심 관점, Secret·SecurityContext 사용법의 짝
- [『Kubernetes: Up and Running』 정독본](../kubernetes-up-and-running/README.md) — RBAC와 Gatekeeper 정책 운영의 위임 대상
- [쿠버네티스 로드맵](../../../roadmap/k8s-roadmap.md) — 6단계 보안 개념 표에서 이 책이 출처로 걸린 행
- [08_cloud MOC](../../README.md) — 상위 카테고리 경계

[^author]: 저자 Benjamin Muschko가 쓴 『Certified Kubernetes Administrator (CKA) Study Guide』를 1장이 선행 학습 자료로 가리킵니다. 저자 서지와 출판일은 위 `source`의 서점 목록 페이지에서 확인했고, 출판사 O'Reilly의 제품 페이지는 접근이 막혀(HTTP 403) 직접 읽지 못했습니다.
