---
title: Learning CoreDNS — 정독 인덱스
tags: [moc, study-index, book, coredns, dns, kubernetes, cncf, service-discovery]
status: draft
source:
  - 《Learning CoreDNS: Configuring DNS for Cloud Native Environments》(John Belamaric·Cricket Liu, O'Reilly, 2019, ISBN 978-1492047964)
  - 챕터 PDF 폴더 — GoogleDrive/내 드라이브/book/Learning CoreDNS/ (9개 장)
  - https://coredns.io/plugins/
related:
  - ../networking-and-kubernetes/README.md
  - ../kubernetes-in-action/README.md
  - ../../project/learning-coredns-lab/README.md
  - ../../README.md
  - ../../../02_os/network-keywords.md
learning:
  topic: learning-coredns
  scope: durable
  level: 기본
  last_verified:            # Phase 4 자답·_review 회차 미실시 — 원문 대조일로 대신 채우지 않는다
  blocked_count:
  next_lesson: "7장 07-01 Phase 2(핵심 질문 점검) 대기 — Phase 1 완료 2026-11-10(_workspace/07-01-phase1-predictions.md). 1~6장 Phase 1~2·1~4장 실습(S1~S7) 완료, 5~9장 Phase 1~2 후 통합 실습·Phase 4 자답 진행(_review/_queue.md 참조)."
updated: 2026-11-29
---

# Learning CoreDNS — 정독 인덱스

---

> 《Learning CoreDNS: Configuring DNS for Cloud Native Environments》(John Belamaric·Cricket Liu, O'Reilly, 2019)를 장 단위로 정독한 책-종속 학습노트입니다. 클러스터 이름 해석의 서버 편에서 DNS 기초·Corefile·존 데이터·서비스 디스커버리·쿠버네티스 연동·질의 조작·관측·커스텀 빌드까지 다룹니다.

## 작성 현황

> 1~9장 정독 노트 15편과 보조 문서 3편(총 18편)의 목록입니다.

| 편 | 제목과 한 줄 요약 | 상태 |
|----|------------------|------|
| [00-01](./00-01.%EC%9A%A9%EC%96%B4%EC%A7%91.md) | 용어집 — 정독 노트 15편의 핵심 용어를 장 순서로 정리 (99개) | 완료 (draft) |
| [00-02](./00-02.%EA%B2%B0%EC%A0%95%20%EC%B9%98%ED%8A%B8%EC%8B%9C%ED%8A%B8.md) | 결정 치트시트 — 15편의 판단 표를 결정 축 16개로 통합 (126행) | 완료 (draft) |
| [00-03](./00-03.1~3%EC%9E%A5%20%ED%86%B5%ED%95%A9%20%EC%9A%94%EC%95%BD.md) | 1~3장 통합 요약 — 덜어낸 서버에서 Corefile 한 장까지 | 완료 (draft) |
| [01-01](./01-01.CoreDNS%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9D%84%20%ED%8F%AC%EA%B8%B0%ED%95%98%EA%B3%A0%20%EB%AC%B4%EC%97%87%EC%9D%84%20%EC%96%BB%EC%97%88%EB%8A%94%EA%B0%80.md) | CoreDNS는 무엇을 포기하고 무엇을 얻었는가 — Caddy 포크·플러그인·Go 메모리 안전성·완전 재귀 미지원 (Ch1) | 완료 (draft · Phase 1~2) |
| [02-01](./02-01.%EC%9C%84%EC%9E%84%EC%9D%B4%20%EA%B7%B8%EC%9D%80%20%EA%B2%BD%EA%B3%84%EA%B0%80%20%EC%A7%88%EC%9D%98%20%EA%B2%BD%EB%A1%9C%EB%A5%BC%20%EC%A0%95%ED%95%9C%EB%8B%A4.md) | 위임이 그은 경계가 질의 경로를 정한다 — 이름공간·도메인 대 존·리졸버 분담·재귀·캐싱 (Ch2 전반) | 완료 (draft · Phase 1~2) |
| [02-02](./02-02.%EB%A0%88%EC%BD%94%EB%93%9C%20%ED%95%9C%20%EC%A4%84%EC%9D%84%20%EC%9D%BD%EC%9C%BC%EB%A9%B4%20%EC%A1%B4%20%ED%8C%8C%EC%9D%BC%EC%9D%B4%20%EC%9D%BD%ED%9E%8C%EB%8B%A4.md) | 레코드 한 줄을 읽으면 존 파일이 읽힌다 — RR 다섯 칸·생략 상속·주요 레코드·SOA 타이머 (Ch2 후반) | 완료 (draft · Phase 1~2) |
| [03-01](./03-01.Corefile%EC%9D%80%20%EB%9D%BC%EB%B2%A8%EB%A1%9C%20%EC%84%9C%EB%B2%84%EB%A5%BC%20%EA%B0%80%EB%A5%B8%EB%8B%A4.md) | Corefile은 라벨로 서버를 가른다 — 프로토콜·이름·포트 라벨, 최장 일치, 스니펫·import, 실행 옵션 (Ch3 전반) | 완료 (draft · Phase 1~2) |
| [03-02](./03-02.%ED%94%8C%EB%9F%AC%EA%B7%B8%EC%9D%B8%20%EC%9D%BC%EA%B3%B1%EC%9D%B4%EB%A9%B4%20%EC%84%9C%EB%B2%84%20%ED%95%98%EB%82%98%EA%B0%80%20%EC%84%A0%EB%8B%A4.md) | 플러그인 일곱이면 서버 하나가 선다 — 고정 처리 순서, file·secondary·forward·cache·errors·log (Ch3 후반) | 완료 (draft · Phase 1~2) |
| [04-01](./04-01.%EC%A1%B4%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%A5%BC%20%EC%96%B4%EB%94%94%EC%97%90%20%EB%91%98%EC%A7%80%EA%B0%80%20%EA%B4%80%EB%A6%AC%20%EB%B0%A9%EC%8B%9D%EC%9D%84%20%EC%A0%95%ED%95%9C%EB%8B%A4.md) | 존 데이터를 어디에 둘지가 관리 방식을 정한다 — file·auto·git-sync·hosts·route53 비교 (Ch4) | 완료 (draft · Phase 1~2) |
| [05-01](./05-01.%EC%83%81%ED%83%9C%EB%A5%BC%20%EB%B0%96%EC%97%90%20%EB%91%90%EC%96%B4%EC%95%BC%20%EC%9D%B4%EB%A6%84%EC%9D%B4%20%EC%B4%88%20%EB%8B%A8%EC%9C%84%EB%A1%9C%20%EB%B0%94%EB%80%90%EB%8B%A4.md) | 상태를 밖에 두어야 이름이 초 단위로 바뀐다 — 서비스 디스커버리 사다리, etcd 쿼럼·역순 키·리스 TTL (Ch5) | 완료 (draft · Phase 1~2) |
| [06-01](./06-01.%EB%AC%B4%EC%97%87%EC%9D%84%20%EC%84%A0%EC%96%B8%ED%96%88%EB%8A%90%EB%83%90%EA%B0%80%20%EB%A0%88%EC%BD%94%EB%93%9C%20%EB%AA%A8%EC%96%91%EC%9D%84%20%EC%A0%95%ED%95%9C%EB%8B%A4.md) | 무엇을 선언했느냐가 레코드 모양을 정한다 — ClusterIP 대 헤드리스, DNS 명세·SRV·StatefulSet·파드 레코드 폐기 (Ch6 1/4) | 완료 (draft · Phase 1~2) |
| [06-02](./06-02.%EA%B8%B0%EB%B3%B8%20Corefile%EC%9D%98%20%EC%A4%84%EB%A7%88%EB%8B%A4%20%EC%9D%B4%EC%9C%A0%EA%B0%80%20%EC%9E%88%EB%8B%A4.md) | 기본 Corefile의 줄마다 이유가 있다 — 읽기 전용 컨트롤러·두 캐시·Endpoints 비용·기본 Corefile·스텁 도메인 (Ch6 2/4) | 완료 (draft · Phase 1~2) |
| [06-03](./06-03.%EB%B3%B5%EC%A0%9C%EB%B3%B8%20%EB%91%98%EA%B3%BC%20170Mi%EB%8A%94%20%EC%96%B4%EB%94%94%EC%84%9C%20%EC%98%A8%20%EA%B0%92%EC%9D%B8%EA%B0%80.md) | 복제본 둘과 170Mi는 어디서 온 값인가 — RBAC·kube-dns Service·Deployment·오토스케일링·Corefile 개선 (Ch6 3/4) | 완료 (draft · Phase 1~2) |
| [06-04](./06-04.%EB%AA%85%EC%84%B8%20%EB%B0%96%EC%9C%BC%EB%A1%9C%20%EB%82%98%EA%B0%80%EB%A9%B4%20%EC%9D%B4%EC%8B%9D%EC%84%B1%EC%9D%84%20%EB%82%B4%EC%A4%80%EB%8B%A4.md) | 명세 밖으로 나가면 이식성을 내준다 — pods 모드·와일드카드·ndots:5·autopath·AXFR·k8s_external (Ch6 4/4) | 완료 (draft · Phase 1~2) |
| [07-01](./07-01.%EC%A7%88%EB%AC%B8%EA%B3%BC%20%EB%8B%B5%EC%9D%B4%20%EC%96%B4%EA%B8%8B%EB%82%98%EB%A9%B4%20%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8%EA%B0%80%20%EB%B2%84%EB%A6%B0%EB%8B%A4.md) | 질문과 답이 어긋나면 클라이언트가 버린다 — template·rewrite·EDNS0·metadata·DNSSEC·필터링 사례 (Ch7) | 완료 (draft · Phase 1) |
| [08-01](./08-01.%EB%AC%B4%EC%97%87%EC%9D%84%20%EB%B3%BC%EC%A7%80%20%EC%A2%81%ED%9E%88%EB%8A%94%20%EC%86%90%EC%9E%A1%EC%9D%B4%EA%B0%80%20%EB%8F%84%EA%B5%AC%EB%A7%88%EB%8B%A4%20%EB%8B%A4%EB%A5%B4%EB%8B%A4.md) | 무엇을 볼지 좁히는 손잡이가 도구마다 다르다 — prometheus·log·dnstap·errors·trace·debug (Ch8) | 완료 (draft) |
| [09-01](./09-01.%ED%95%9C%20%EC%A4%84%EC%9D%84%20%EC%98%AE%EA%B8%B0%EB%A9%B4%20%EA%B7%B8%20%ED%94%8C%EB%9F%AC%EA%B7%B8%EC%9D%B8%EC%9D%B4%20%EC%93%B8%EB%AA%A8%EC%97%86%EC%96%B4%EC%A7%84%EB%8B%A4.md) | 한 줄을 옮기면 그 플러그인이 쓸모없어진다 — Docker·로컬 빌드, plugin.cfg 순서, 라이브러리 임베딩 (Ch9 1/2) | 완료 (draft) |
| [09-02](./09-02.%EB%84%A4%20%ED%95%A8%EC%88%98%EB%A5%BC%20%EA%B5%AC%ED%98%84%ED%95%98%EB%A9%B4%20%EC%B2%B4%EC%9D%B8%EC%9D%98%20%ED%95%9C%20%EC%B9%B8%EC%9D%B4%20%EB%90%9C%EB%8B%A4.md) | 네 함수를 구현하면 체인의 한 칸이 된다 — init·setup·Name·ServeDNS, 생명주기 훅, nonwriter·ClientWrite (Ch9 2/2) | 완료 (draft) |



## 학습 상태

> 세션을 열 때 현재 진행 위치만 빠르게 확인하는 요약입니다. 장별 상세 진행과 약한 축 정본은 복습 대기 큐에 있습니다.

| 항목 | 현재 값 |
|------|--------|
| 진행률 | 9/9장 작성 완료 — 정독 노트 15편 + 보조 문서 3편(용어집 · 결정 치트시트 · 1~3장 통합 요약) |
| 현재 상태 | 난이도 `기본`. 1~6장 Phase 1~2 완료, 1~4장 실습 S1~S7 완료, 7장 07-01 Phase 1 완료(Phase 2 대기), 8~9장 Phase 1~2 및 전 장 Phase 4 미실시 |
| 실습 코드·기록 | `~/study/runners-lab/net/learning-coredns/` · [learning-coredns-lab](../../project/learning-coredns-lab/README.md) (1~4장 S1~S7 완료) |
| 복습·작업 메모 | [복습 대기 큐](../../../_review/_queue.md) (`coredns` ch00~ch09) · `_workspace/reinforce-candidates.md` |



## 관련 문서

> 같은 book/ 영역의 형제 정독본, 연계 실습, 상위 인덱스입니다.

- [Kubernetes in Action 정독 인덱스](../kubernetes-in-action/README.md) — 쿠버네티스 오브젝트 중심 관점
- [Networking and Kubernetes 정독 인덱스](../networking-and-kubernetes/README.md) — 패킷·커널·CNI 중심 관점
- [learning-coredns-lab 프로젝트 인덱스](../../project/learning-coredns-lab/README.md) — 1~4장 장애 재현 실습 S1~S7 기록
- [08_cloud MOC](../../README.md) — 상위 카테고리 경계
- [네트워크 개발 키워드](../../../02_os/network-keywords.md) — DNS·네트워크 전체 키워드 표. 질의를 보내는 쪽(resolv.conf·ndots·search domain)은 거기서, 받는 쪽(Corefile·플러그인·존 데이터)은 이 폴더에서 봅니다.
