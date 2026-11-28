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
  - ../../k8s-keywords.md
  - ../../README.md
learning:
  topic: cks-study-guide
  scope: durable
  level: 기본
  last_verified:
  blocked_count:
  next_lesson: "모든 장 정독 완료. 각 편의 연습 문제로 장별 복습"
updated: 2026-11-29
---

# CKS Study Guide — 정독 인덱스

《Certified Kubernetes Security Specialist (CKS) Study Guide》(Benjamin Muschko, O'Reilly, 2023)를 장 단위로 정독한 노트입니다.

클러스터 운영자가 시험 실기처럼 하드닝 절차를 직접 치는 관점을 다룹니다. 독자는 CKA 수준의 운영 지식을 갖췄다고 보고, 겹치는 기초는 반복하지 않습니다.[^author]

이 폴더에는 CKS 고유 내용만 둡니다. 격리·공급망·탐지의 원리는 아래 형제 노트에 맡깁니다.

## 작성된 정독 노트

10편 모두 작성했습니다. 편 번호는 장 번호(NN)와 장 안의 순서(MM)입니다.

| 편 | 노트 | 다루는 내용 |
|----|------|------------|
| 01-01 | [01-01.CKS 시험의 범위와 준비 — 자격증 경로·출제 도메인·시험 환경](./01-01.CKS%20%EC%8B%9C%ED%97%98%EC%9D%98%20%EB%B2%94%EC%9C%84%EC%99%80%20%EC%A4%80%EB%B9%84%20%E2%80%94%20%EC%9E%90%EA%B2%A9%EC%A6%9D%20%EA%B2%BD%EB%A1%9C%C2%B7%EC%B6%9C%EC%A0%9C%20%EB%8F%84%EB%A9%94%EC%9D%B8%C2%B7%EC%8B%9C%ED%97%98%20%ED%99%98%EA%B2%BD.md) | 자격증 경로, 출제 도메인과 비중, 시험 환경 |
| 02-01 | [02-01.클러스터 경계 세우기 — NetworkPolicy·CIS 벤치마크·TLS Ingress](./02-01.%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EA%B2%BD%EA%B3%84%20%EC%84%B8%EC%9A%B0%EA%B8%B0%20%E2%80%94%20NetworkPolicy%C2%B7CIS%20%EB%B2%A4%EC%B9%98%EB%A7%88%ED%81%AC%C2%B7TLS%20Ingress.md) | NetworkPolicy, kube-bench로 CIS 벤치마크 점검, Ingress TLS |
| 02-02 | [02-02.노드와 접근 지점 지키기 — 메타데이터·Dashboard·설정 인자·바이너리 검증](./02-02.%EB%85%B8%EB%93%9C%EC%99%80%20%EC%A0%91%EA%B7%BC%20%EC%A7%80%EC%A0%90%20%EC%A7%80%ED%82%A4%EA%B8%B0%20%E2%80%94%20%EB%A9%94%ED%83%80%EB%8D%B0%EC%9D%B4%ED%84%B0%C2%B7Dashboard%C2%B7%EC%84%A4%EC%A0%95%20%EC%9D%B8%EC%9E%90%C2%B7%EB%B0%94%EC%9D%B4%EB%84%88%EB%A6%AC%20%EA%B2%80%EC%A6%9D.md) | 노드 메타데이터 차단, Dashboard 접근 제한, 위험한 설정 인자, 바이너리 체크섬 |
| 03-01 | [03-01.클러스터 굳히기 — API 접근·RBAC·ServiceAccount·업그레이드](./03-01.%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EA%B5%B3%ED%9E%88%EA%B8%B0%20%E2%80%94%20API%20%EC%A0%91%EA%B7%BC%C2%B7RBAC%C2%B7ServiceAccount%C2%B7%EC%97%85%EA%B7%B8%EB%A0%88%EC%9D%B4%EB%93%9C.md) | API 요청 처리 순서, CSR로 사용자 만들기, RBAC, ServiceAccount 토큰, 업그레이드 |
| 04-01 | [04-01.노드 호스트 굳히기 — 패키지·계정·포트·AppArmor·seccomp](./04-01.%EB%85%B8%EB%93%9C%20%ED%98%B8%EC%8A%A4%ED%8A%B8%20%EA%B5%B3%ED%9E%88%EA%B8%B0%20%E2%80%94%20%ED%8C%A8%ED%82%A4%EC%A7%80%C2%B7%EA%B3%84%EC%A0%95%C2%B7%ED%8F%AC%ED%8A%B8%C2%B7AppArmor%C2%B7seccomp.md) | 호스트 OS 줄이기, 계정과 파일 권한, 외부 네트워크 줄이기, AppArmor·seccomp |
| 05-01 | [05-01.파드 보안 설정 강제하기 — securityContext·Pod Security Admission·Gatekeeper](./05-01.%ED%8C%8C%EB%93%9C%20%EB%B3%B4%EC%95%88%20%EC%84%A4%EC%A0%95%20%EA%B0%95%EC%A0%9C%ED%95%98%EA%B8%B0%20%E2%80%94%20securityContext%C2%B7Pod%20Security%20Admission%C2%B7Gatekeeper.md) | securityContext, Pod Security Admission, OPA Gatekeeper |
| 05-02 | [05-02.데이터와 실행 경계 지키기 — etcd 암호화·런타임 샌드박스·mTLS](./05-02.%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%99%80%20%EC%8B%A4%ED%96%89%20%EA%B2%BD%EA%B3%84%20%EC%A7%80%ED%82%A4%EA%B8%B0%20%E2%80%94%20etcd%20%EC%95%94%ED%98%B8%ED%99%94%C2%B7%EB%9F%B0%ED%83%80%EC%9E%84%20%EC%83%8C%EB%93%9C%EB%B0%95%EC%8A%A4%C2%B7mTLS.md) | etcd 암호화, RuntimeClass 샌드박스(gVisor·Kata), mTLS |
| 06-01 | [06-01.이미지 작게 만들고 미리 검사하기 — 베이스 이미지·멀티 스테이지·Hadolint·Kubesec](./06-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%9E%91%EA%B2%8C%20%EB%A7%8C%EB%93%A4%EA%B3%A0%20%EB%AF%B8%EB%A6%AC%20%EA%B2%80%EC%82%AC%ED%95%98%EA%B8%B0%20%E2%80%94%20%EB%B2%A0%EC%9D%B4%EC%8A%A4%20%EC%9D%B4%EB%AF%B8%EC%A7%80%C2%B7%EB%A9%80%ED%8B%B0%20%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80%C2%B7Hadolint%C2%B7Kubesec.md) | 작은 베이스 이미지, 멀티 스테이지 빌드, Hadolint·Kubesec 검사 |
| 06-02 | [06-02.믿을 수 있는 이미지만 들이기 — 서명·digest·레지스트리 허용 목록·Trivy](./06-02.%EB%AF%BF%EC%9D%84%20%EC%88%98%20%EC%9E%88%EB%8A%94%20%EC%9D%B4%EB%AF%B8%EC%A7%80%EB%A7%8C%20%EB%93%A4%EC%9D%B4%EA%B8%B0%20%E2%80%94%20%EC%84%9C%EB%AA%85%C2%B7digest%C2%B7%EB%A0%88%EC%A7%80%EC%8A%A4%ED%8A%B8%EB%A6%AC%20%ED%97%88%EC%9A%A9%20%EB%AA%A9%EB%A1%9D%C2%B7Trivy.md) | 이미지 서명과 digest, 허용 레지스트리(ImagePolicyWebhook), Trivy 스캔 |
| 07-01 | [07-01.실행 중인 클러스터 지켜보기 — Falco·불변 컨테이너·감사 로그](./07-01.%EC%8B%A4%ED%96%89%20%EC%A4%91%EC%9D%B8%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%A7%80%EC%BC%9C%EB%B3%B4%EA%B8%B0%20%E2%80%94%20Falco%C2%B7%EB%B6%88%EB%B3%80%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%C2%B7%EA%B0%90%EC%82%AC%20%EB%A1%9C%EA%B7%B8.md) | Falco 규칙, 불변 컨테이너, audit policy |

2·5·6장은 두 편으로 나눴습니다. 6장은 원문 순서 대신 이미지를 만드는 쪽(06-01)과 들이는 쪽(06-02)으로 나눴습니다. 부록은 별도 편이 없습니다. 답은 2~7편의 「정답」 절에 들어 있습니다.

편 나눔의 근거가 된 장별 단어 수는 `pdftotext`로 쟀습니다. 1장 2,453, 2장 8,002, 3장 5,718, 4장 5,600, 5장 8,460, 6장 7,431, 7장 5,880, 부록 5,409단어입니다.



## 장과 시험 도메인

책의 장 순서가 시험 도메인 순서를 따르므로, 도메인 하나가 장 하나에 대응합니다. 비중은 CNCF CKS 커리큘럼 v1.37 기준이며 2026-11-27에 조회했습니다.

| 장 | 책의 주제 | 시험 도메인 | 비중 |
|----|----------|------------|-----:|
| 1 | 자격증 경로와 시험 안내 | — | — |
| 2 | 클러스터 설정 | Cluster Setup | 15% |
| 3 | 클러스터 하드닝 | Cluster Hardening | 15% |
| 4 | 노드 호스트 하드닝 | System Hardening | 10% |
| 5 | 마이크로서비스 취약점 줄이기 | Minimize Microservice Vulnerabilities | 20% |
| 6 | 공급망 보안 | Supply Chain Security | 20% |
| 7 | 모니터링·로깅·런타임 보안 | Monitoring, Logging and Runtime Security | 20% |



## 위임 대상

이 책과 겹치는 주제는 형제 책 노트에 맡기고 링크만 겁니다. 『Container Security』는 커널이 세우는 격리 경계를, 『Kubernetes in Action』은 오브젝트를 다루므로 이 책과 층이 다릅니다.

- 샌드박싱(seccomp·AppArmor·gVisor·Kata): [컨테이너 격리 강화](../container-security/08-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC%20%EA%B0%95%ED%99%94%20%E2%80%94%20%EC%83%8C%EB%93%9C%EB%B0%95%EC%8B%B1%EC%9D%98%20%EC%84%B8%20%EA%B0%88%EB%9E%98.md), [컨테이너 격리 깨뜨리기](../container-security/09-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC%20%EA%B9%A8%EB%9C%A8%EB%A6%AC%EA%B8%B0%20%E2%80%94%20%EC%84%A4%EC%A0%95%20%ED%95%98%EB%82%98%EB%A1%9C%20%EB%AC%B4%EB%84%88%EC%A7%80%EB%8A%94%20%EA%B2%BD%EA%B3%84.md)
- 이미지 공급망: [이미지 공급망 보안](../container-security/06-02.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EA%B3%B5%EA%B8%89%EB%A7%9D%20%EB%B3%B4%EC%95%88%20%E2%80%94%20%EB%B9%8C%EB%93%9C%EB%B6%80%ED%84%B0%20%EB%B0%B0%ED%8F%AC%EA%B9%8C%EC%A7%80.md)
- 런타임 탐지: [컨테이너 런타임 보호](../container-security/13-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%9F%B0%ED%83%80%EC%9E%84%20%EB%B3%B4%ED%98%B8%20%E2%80%94%20%EC%A0%95%EC%83%81%EC%9D%84%20%EC%A0%95%EC%9D%98%ED%95%B4%20%EC%9D%B4%EC%83%81%EC%9D%84%20%EC%9E%A1%EB%8B%A4.md)
- NetworkPolicy 일반 동작: [NetworkPolicy와 DNS](../networking-and-kubernetes/04-03.NetworkPolicy%EC%99%80%20DNS%20%E2%80%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%95%88%EC%9D%98%20%EB%B0%A9%ED%99%94%EB%B2%BD%EA%B3%BC%20%EC%9D%B4%EB%A6%84.md)
- RBAC 설계와 운영: [RBAC 노트](../kubernetes-up-and-running/14-01.RBAC%20%E2%80%94%20%EC%9D%B8%EA%B0%80%EB%A5%BC%20%EC%84%A4%EA%B3%84%ED%95%98%EA%B3%A0%20%EC%9A%B4%EC%98%81%ED%95%98%EB%8A%94%20%EB%B2%95.md)
- 어드미션 정책(Gatekeeper): [Policy and Governance](../kubernetes-up-and-running/20-01.Policy%20and%20Governance%20%E2%80%94%20Gatekeeper%20%EB%A1%9C%20%EB%A7%8C%EB%93%A4%EA%B8%B0%20%EC%A0%84%EC%97%90%20%EB%A7%89%EA%B3%A0%20%EB%A7%8C%EB%93%A0%20%EB%92%A4%EC%97%90%20%EC%84%B8%EB%8A%94%20%EB%B2%95.md)



## 로드맵 속 자리

[쿠버네티스 로드맵](../../k8s-keywords.md)의 6단계 「보안과 확장」 개념 표는 API 접근 하드닝(3장)과 감사 로그(7장) 행을 이 책으로 잇습니다. 두 행은 형제 책 노트가 없어서 책 칸이 이 책을 가리킵니다.



## 장별 메모

- 버전: 책은 쿠버네티스 1.26 기준입니다. 보안 기본값과 필드는 버전마다 바뀌므로, 노트에는 현재 값을 버전과 함께 적습니다.
- 번호와 도식: 파일명은 `NN-MM.제목.md`입니다. 도식은 `_assets/`의 SVG이고 생성 스크립트는 `_assets/_gen/`에 있습니다.
- 작성 규약: `writing-method` 스킬의 정독 노트 규약을 따릅니다.
- Spring 절: 접점이 자연스러운 5장(Secret 소비)과 7장(컨테이너 불변성)만 후보입니다. 지금 노트에는 없습니다.



## 학습 상태

> 세션을 새로 열 때 이 표부터 읽습니다.

| 항목 | 현재 값 |
|------|--------|
| 진행률 | 7/7 장, 정독 노트 10편. 부록 답은 각 편의 「정답」 절에 있음 |
| 난이도 레벨 | 미정 |
| 막힌 지점 | 없음 |
| 다음 레슨 후보 | 각 편의 「연습 문제」로 장별 복습 |
| 최근 검증 결과 | 02-01~07-01은 2026-11-05·11-06에 게이트 실패 0과 적대적 내용 검증을 마쳤습니다. 01-01은 2026-11-27에 공식 페이지 기준으로 다시 대조했습니다(KCSA 설명 수정, 도식 세 장 추가). 수정 곳 수는 git 이력에 있습니다 |
| 버전 차이 기록 | 4 (시험 기준 쿠버네티스 버전, Cluster Setup 비중, System Hardening 비중, Pod 보안 항목 표기) |
| 복습 회차 | 0 |



## 관련 문서

- [『Container Security』 정독본](../container-security/README.md) — 같은 `book/` 영역, 격리 경계 중심의 짝
- [『Kubernetes in Action, 2판』 정독본](../kubernetes-in-action/README.md) — 오브젝트 중심의 짝, Secret·SecurityContext 사용법
- [『Kubernetes: Up and Running』 정독본](../kubernetes-up-and-running/README.md) — RBAC와 Gatekeeper 정책 운영
- [쿠버네티스 로드맵](../../k8s-keywords.md) — 6단계 보안 개념 표
- [08_cloud MOC](../../README.md) — 상위 카테고리 경계

[^author]: 저자 Benjamin Muschko가 쓴 『Certified Kubernetes Administrator (CKA) Study Guide』를 1장이 선행 학습 자료로 가리킵니다. 저자 서지와 출판일은 위 `source`의 서점 목록 페이지에서 확인했고, 출판사 O'Reilly의 제품 페이지는 접근이 막혀(HTTP 403) 직접 읽지 못했습니다.
