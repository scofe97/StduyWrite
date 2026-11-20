---
title: DevOps 명령어 시트
tags: [moc, devops, cli, cheatsheet, reference]
status: draft
related:
  - ../../README.md
  - ../../../02_os/docs/cmd/README.md
  - ../iac/README.md
  - ../artifact/README.md
  - ../../../08_cloud/docs/cmd/README.md
updated: 2026-11-21
---

# DevOps 명령어 시트

---

> 빌드·배포 도구의 사용법을 도구별로 모으는 조회용 시트 자리입니다. 개념 노트는 원리를 설명하고, 명령 옵션과 실행 예는 여기에 둔 뒤 링크로 가져다 씁니다.

## 이 폴더를 쓰는 법

> 도구 하나를 한 시트에 두고, 하는 일에 따라 아래 분류의 하위 폴더에 둡니다.

지금은 분류와 후보 명령만 정해 두었고, 이 폴더 안에 쓴 시트는 아직 없습니다. 시트를 쓰면 해당 분류의 표에 한 행을 더합니다.

- [image: 이미지 빌드와 레지스트리](#image--이미지-빌드와-레지스트리)
- [manifest: 매니페스트 패키징과 렌더](#manifest--매니페스트-패키징과-렌더)
- [gitops: 배포와 동기화](#gitops--배포와-동기화)
- [vcs: 소스 저장소](#vcs--소스-저장소)
- [ci: 빌드와 품질 검사](#ci--빌드와-품질-검사)
- [data: 설정 파일과 API 응답 가공](#data--설정-파일과-api-응답-가공)
- [infra: 인프라 프로비저닝](#infra--인프라-프로비저닝)

시트의 절 순서와 코드 블록 안 `#` 줄의 뜻은 [리눅스 명령어 시트](../../../02_os/docs/cmd/README.md)의 「이 폴더를 쓰는 법」을 그대로 따릅니다. 개요, 핵심 문법, 종료 코드, 유스케이스, 주의사항과 동작 원리, 관련 문서 순서입니다. 실측한 환경과 도구 버전은 시트마다 개요에 적습니다.

다른 명령어 시트와 겹치는 도구는 한쪽에만 둡니다. 운영체제 기능을 직접 보는 명령(`ps`·`ss`·`systemctl`)은 리눅스 명령어 시트에, 컨테이너 실행과 클러스터 조작 명령(`docker`·`crictl`·`kubectl`)은 [클라우드 명령어 시트](../../../08_cloud/docs/cmd/README.md)에, 빌드와 배포 흐름에서 쓰는 도구는 이쪽에 둡니다. 이미 다른 폴더에 있는 시트는 옮기지 않고 아래 표에서 링크로 가리킵니다.



## image — 이미지 빌드와 레지스트리

> 이미지를 만들고, 레지스트리 사이로 옮기고, 내용과 취약점을 확인하는 도구입니다. 후보는 `docker build`·`docker buildx`·`skopeo`·`crane`·`trivy` 입니다.

빌더를 고르는 기준과 rootless 빌드의 조건은 [artifact](../artifact/README.md)의 개념 편이 맡습니다. `buildctl` 시트는 그 폴더에 이미 있어서 링크만 둡니다. `docker` 로 컨테이너를 실행하고 조회하는 명령은 클라우드 명령어 시트가 맡고, 여기는 빌드와 레지스트리 전송만 다룹니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|
| [buildkit](../artifact/container/buildkit.md) | `buildctl` · `buildkitd` | `buildctl` 로 빌드하고 결과를 registry·tar 로 내보내거나 캐시를 주고받을 때 |



## manifest — 매니페스트 패키징과 렌더

> 매니페스트를 템플릿이나 patch 로 만들어 내고, 적용하기 전에 결과를 비교하는 도구입니다. 후보는 `helm`·`helmfile`·`kustomize` 입니다.

차트 구조와 base·overlay 의 원리는 [iac](../iac/README.md)의 [Helm 기초](../iac/Helm%20%EA%B8%B0%EC%B4%88.md)·[Helm 고급](../iac/Helm%20%EA%B3%A0%EA%B8%89.md)·[Kustomize](../iac/Kustomize.md)가 맡습니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|



## gitops — 배포와 동기화

> Git 에 적힌 상태를 클러스터에 맞추고, 새 버전을 조금씩 내보내는 도구입니다. 후보는 `argocd`·`kubectl argo rollouts` 입니다.

Argo CD 의 원리는 [Argo CD 정독 노트](../../book/argocd-up-and-running/README.md)가, 배포 전략은 [deployment](../deployment/README.md)가 맡습니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|



## vcs — 소스 저장소

> 변경 이력을 남기고, 되돌리고, 원격 저장소와 주고받는 도구입니다. 후보는 `git`·`gh`·`glab` 입니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|



## ci — 빌드와 품질 검사

> 파이프라인 안에서 소스를 빌드하고 분석 서버로 결과를 보내는 도구입니다. 후보는 `mvn`·`gradle`·`jenkins-cli`·`sonar-scanner` 입니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|



## data — 설정 파일과 API 응답 가공

> YAML·JSON 에서 값을 뽑거나 바꾸고, 도구의 HTTP API 를 직접 부르는 도구입니다. 후보는 `jq`·`yq`·`envsubst`·`curl` 입니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|



## infra — 인프라 프로비저닝

> 서버와 클라우드 자원을 코드로 만들고 설정을 맞추는 도구입니다. 후보는 `terraform`·`ansible` 입니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|



## 관련 문서

- [07_devops](../../README.md) — DevOps 카테고리 지도
- [리눅스 명령어 시트](../../../02_os/docs/cmd/README.md) — 운영체제 명령의 시트와 시트 작성 형식
- [iac](../iac/README.md) — Helm·Kustomize 의 원리
- [artifact](../artifact/README.md) — 이미지 빌드의 원리와 `buildctl` 시트
- [클라우드 명령어 시트](../../../08_cloud/docs/cmd/README.md) — `docker`·`crictl`·`kubectl` 처럼 컨테이너와 클러스터를 다루는 명령의 시트
