---
title: 06_architecture — 클러스터 내부 구조
tags: [moc, kubernetes, control-plane, etcd, pki, upgrade]
status: final
related:
  - ../README.md
updated: 2026-07-10
---

# 06_architecture — 클러스터 내부 구조

> Control Plane과 노드가 어떻게 맞물려 돌아가는지, 그 상태를 어떻게 지키고 복구하는지를 봅니다.



## 문서 목록
> 공식 concepts의 Cluster Architecture에 대응합니다. 파일 번호(`06-MM`)가 읽기 순서입니다. 각 본문 끝에는 `## N. 점검 질문` 절이 있어, 개념 설명과 심화 Q&A를 한 문서에서 이어 읽습니다(일부 입문 편 제외).

| 번호 | 제목 | 한 줄 소개 |
|------|------|-----------|
| 06-01 | [클러스터 업그레이드와 ETCD 백업·복구](06-01.%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%97%85%EA%B7%B8%EB%A0%88%EC%9D%B4%EB%93%9C%EC%99%80%20ETCD%20%EB%B0%B1%EC%97%85%C2%B7%EB%B3%B5%EA%B5%AC.md) | kubeadm 업그레이드와 etcd 재해 복구를 어떤 절차로 다루는지, etcd Raft 합의가 일관성을 어떻게 지키는지 봅니다. |
| 06-02 | [TLS와 API 접근 보안](06-02.TLS%EC%99%80%20API%20%EC%A0%91%EA%B7%BC%20%EB%B3%B4%EC%95%88.md) | 컨트롤 플레인 PKI(API 서버·etcd·kubelet 인증서)가 어떻게 연결되는지 봅니다. |



## 관련 문서
> 이 폴더가 딛고 서거나 이어지는 이웃 대주제입니다.

- [kubernetes MOC](../README.md) — 전체 대주제 지도와 딥다이브 로드맵 연결
