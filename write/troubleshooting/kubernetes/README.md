---
title: troubleshooting/kubernetes — 계층 B
tags: [moc, troubleshooting, kubernetes]
status: draft
related:
  - ../README.md
  - ../_drill/sources.md
updated: 2026-09-07
---

# troubleshooting/kubernetes

---

> 클러스터 안에서 생기는 일입니다. Pod 네트워크·Service·CoreDNS·CNI·NetworkPolicy 가 여기 속합니다.

파일명이 증상입니다. 날짜순으로 쌓이니 훑으면 됩니다.

## 어디부터 보나

> 걷어낸 사례집 38건에서 반복되던 진입 축입니다.

`kubectl get pods` 의 두 열이 안내가 됩니다. `ImagePullBackOff` 는 이미지를 가져오는 단계, `CrashLoopBackOff` 와 `Init:0/1` 은 컨테이너가 뜨는 단계, `Pending` 은 놓일 자리를 찾는 단계, `Evicted` 는 자원 한계입니다. 접속이 안 되면 네트워크, 볼륨이면 스토리지, 권한 거절이면 RBAC 쪽입니다.

문서에 걸쳐 반복되는 명령이 셋 있습니다.

- `kubectl describe`: 상태와 이벤트를 읽습니다
- `kubectl logs --previous`: 죽기 직전 인스턴스의 마지막 말을 봅니다
- `kubectl get endpoints`: Service 와 Pod 가 실제로 연결됐는지 확인합니다

## 참고 읽을거리

> 같은 증상을 더 넓게 훑고 싶을 때 읽습니다.

- [쿠버네티스 공식 — 클러스터 디버깅](https://kubernetes.io/ko/docs/tasks/debug/debug-cluster/)
- [50 Common Errors in Kubernetes](https://www.linkedin.com/pulse/50-common-errors-kubernetes-avinash-tietler-ocoqc/)
- [Common Kubernetes Errors and How to Troubleshoot Them](https://www.linkedin.com/pulse/common-kubernetes-errors-how-troubleshoot-them-pramod-medi-mjkgc/)

## 관련 문서

- [troubleshooting 지도](../README.md) — 계층 표와 여는 절차
- [출제 소스](../_drill/sources.md) — 이 계층의 근거 노트
