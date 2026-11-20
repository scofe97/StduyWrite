---
title: 클라우드 명령어 시트
tags: [moc, cloud, kubernetes, container, cli, cheatsheet, reference]
status: draft
related:
  - ../README.md
  - ../kubernetes/README.md
  - ../../../07_devops/docs/cmd/README.md
  - ../../../02_os/docs/cmd/README.md
updated: 2026-11-21
---

# 클라우드 명령어 시트

---

> 컨테이너와 쿠버네티스 클러스터를 다루는 도구의 사용법을 도구별로 모으는 조회용 시트 자리입니다. 개념 노트는 원리를 설명하고, 명령 옵션과 실행 예는 여기에 둔 뒤 링크로 가져다 씁니다.

## 이 폴더를 쓰는 법

> 도구 하나를 한 시트에 두고, 하는 일에 따라 아래 분류의 하위 폴더에 둡니다.

이 폴더 안에 쓴 시트는 [docker](container/docker.md) 한 편이고, 나머지는 분류와 후보 명령만 정해 두었습니다. 시트를 쓰면 해당 분류의 표에 한 행을 더합니다.

- [container: 컨테이너 실행과 조회](#container--컨테이너-실행과-조회)
- [k8s: 클러스터 조작](#k8s--클러스터-조작)

시트의 절 순서와 코드 블록 안 `#` 줄의 뜻은 [리눅스 명령어 시트](../../../02_os/docs/cmd/README.md)의 「이 폴더를 쓰는 법」을 그대로 따릅니다. 개요, 핵심 문법, 종료 코드, 유스케이스, 주의사항과 동작 원리, 관련 문서 순서입니다. 실측한 환경과 도구 버전은 시트마다 개요에 적습니다.

다른 명령어 시트와 겹치는 도구는 한쪽에만 둡니다.

- [DevOps 명령어 시트](../../../07_devops/docs/cmd/README.md): 빌드와 배포 흐름에서 쓰는 도구(`helm`·`argocd`·`git`·`mvn`)
- DevOps 명령어 시트: 이미지 빌드와 레지스트리 전송 도구(`docker build`·`skopeo`·`trivy`)
- 리눅스 명령어 시트: 운영체제 기능을 직접 보는 명령(`ps`·`ss`·`systemctl`)

이미 다른 폴더에 있는 문서는 옮기지 않고 아래 표에서 링크로 가리킵니다.



## container — 컨테이너 실행과 조회

> 컨테이너를 띄우고, 안을 들여다보고, 로그와 상태를 읽는 도구입니다. 후보는 `docker`·`docker compose`·`podman`·`ctr`·`crictl` 입니다.

`nerdctl` 시트는 리눅스 명령어 시트의 isolate 분류에 이미 있습니다. `crictl` 은 시트가 아니라 공식 문서 정독 노트가 명령과 진단 순서를 함께 담고 있어서 그 노트를 가리킵니다.

| 문서 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|
| [docker](container/docker.md) | `docker save` · `docker load` · `docker export` · `docker import` | 이미지를 tar 로 내보내 다른 호스트에 들이고, 태그를 되살려 저장소에 올릴 때. 실행·조회 명령은 아직 없습니다 |
| [nerdctl](../../../02_os/docs/cmd/isolate/nerdctl.md) | `nerdctl` | containerd 위의 컨테이너·이미지를 docker 문법으로 보고 실행하고, namespace 를 가르고, tar 로 반입한 이미지를 저장소에 올릴 때 |
| [컨테이너 런타임 인터페이스·crictl](../kubernetes/architecture/%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%9F%B0%ED%83%80%EC%9E%84%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4%C2%B7crictl.md) | `crictl` | 워커 노드에서 `docker ps` 로 보이지 않는 Pod 컨테이너와 샌드박스를 CRI 소켓으로 볼 때 |



## k8s — 클러스터 조작

> 클러스터의 리소스를 보고, 고치고, 파드 안에서 원인을 찾는 도구입니다. 후보는 `kubectl`·`kubectl debug`·`oc`·`kubectx`·`kubens`·`stern` 입니다.

리소스가 어떻게 동작하는지는 [docs/kubernetes](../kubernetes/README.md)의 노트와 책 정독 노트가 맡습니다. 아래 세 편은 시트 형식은 아니지만 `kubectl` 사용법을 주제로 삼은 노트라서 함께 가리킵니다.

| 문서 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|
| [kubectl 출력 형식](../kubernetes/api/kubectl%20%EC%B6%9C%EB%A0%A5%20%ED%98%95%EC%8B%9D.md) | `kubectl get -o` | 기본 표·`-o wide`·`-o yaml`·`-o json` 가운데 목적에 맞는 출력 형식을 고를 때 |
| [JSONPath·kubectl 고급 조회](../kubernetes/api/JSONPath%C2%B7kubectl%20%EA%B3%A0%EA%B8%89%20%EC%A1%B0%ED%9A%8C.md) | `kubectl get -o jsonpath` | 필요한 필드만 뽑아 점검 루틴이나 스크립트에 넣을 때 |
| [kubeconfig·여러 클러스터 접근](../kubernetes/api/kubeconfig%C2%B7%EC%97%AC%EB%9F%AC%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%A0%91%EA%B7%BC.md) | `kubectl config` | context 를 바꾸거나 kubeconfig 파일 여럿을 합쳐 쓸 때. `kubectx`·`kubens` 도 여기서 다룹니다 |



## 관련 문서

- [08_cloud/docs](../README.md) — 공식 문서 정독 노트의 지도
- [DevOps 명령어 시트](../../../07_devops/docs/cmd/README.md) — 이미지 빌드, 매니페스트, GitOps, CI 도구의 시트
- [리눅스 명령어 시트](../../../02_os/docs/cmd/README.md) — 운영체제 명령의 시트와 시트 작성 형식
- [쿠버네티스 로드맵](../../k8s-keywords.md) — kubectl 기본 조회·고급 조회·`kubectl debug` 가 놓인 단계
