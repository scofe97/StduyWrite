---
title: 08_cloud/openstack — 오픈스택 IaaS 개요
tags: [moc, openstack, iaas, cloud]
status: final
source:
  - https://www.openstack.org/software/
  - 사업수행2본부 5차 세미나 "OpenStack 서비스 소개"(오케스트로 박인 수석, 2026-03)
related:
  - ../README.md
  - ../kubernetes/README.md
updated: 2026-07-01
---

# 08_cloud/openstack

---

> 오픈스택은 사내 서버에 AWS 를 세우는 오픈소스 IaaS 플랫폼입니다. 이 카테고리는 그 IaaS 층이 무엇이고, 회사 CMP·Kubernetes 가 그 위에서 어떻게 도는지를 개발자 관점에서 조망합니다.

`08_cloud` 의 다른 서브카테고리(kubernetes·argocd·service-mesh)가 "클러스터 *내부* 구조" 를 다룬다면, openstack 은 그 **아래층인 IaaS(인프라를 만드는 층)** 를 다룹니다. 오픈스택이 만든 VM 위에서 Kubernetes 가 돌고, 그 위에서 컨테이너·CMP 가 실행됩니다.

현재는 참고용 개요 한 편으로 시작합니다. 서비스별 딥다이브(Nova·Neutron·Placement·Octavia 등)는 필요해질 때 편을 늘려 확장할 여지를 둡니다.

## 구성

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 00-01 | [오픈스택 개요](00-01.%EC%98%A4%ED%94%88%EC%8A%A4%ED%83%9D%20%EA%B0%9C%EC%9A%94.md) | IaaS 란 무엇이고, AWS·Kubernetes 와 어떤 층 관계인가? |

각 본문에는 같은 번호의 점검 문서가 짝을 이룹니다(`00-01.오픈스택 개요 점검.md`).

## 관련 문서

> 위층(컨테이너)과 옆 카테고리(모니터링)로 이어집니다.

- [08_cloud MOC](../README.md) — 상위 클라우드 카테고리
- [kubernetes MOC](../kubernetes/README.md) — 오픈스택 VM 위에서 도는 컨테이너 층
- [06_observability](../../06_observability/README.md) — 세미나가 함께 다룬 Prometheus 상세
