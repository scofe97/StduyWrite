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

이 폴더 안에 쓴 시트는 image 분류의 [buildah](image/buildah.md)·[crane](image/crane.md)·[trivy](image/trivy.md)·[cosign](image/cosign.md) 네 편이고, 나머지는 분류와 후보 명령만 정해 두었습니다. 시트를 쓰면 해당 분류의 표에 한 행을 더합니다.

- [image: 이미지 빌드와 레지스트리](#image--이미지-빌드와-레지스트리)
- [gitops: 배포와 동기화](#gitops--배포와-동기화)
- [vcs: 소스 저장소](#vcs--소스-저장소)
- [ci: 빌드와 품질 검사](#ci--빌드와-품질-검사)
- [data: 설정 파일과 API 응답 가공](#data--설정-파일과-api-응답-가공)
- [infra: 인프라 프로비저닝](#infra--인프라-프로비저닝)

시트의 절 순서와 코드 블록 안 `#` 줄의 뜻은 [리눅스 명령어 시트](../../../02_os/docs/cmd/README.md)의 「이 폴더를 쓰는 법」을 그대로 따릅니다. 개요, 핵심 문법, 종료 코드, 유스케이스, 주의사항과 동작 원리, 관련 문서 순서입니다. 실측한 환경과 도구 버전은 시트마다 개요에 적습니다.

다른 명령어 시트와 겹치는 도구는 한쪽에만 둡니다. 운영체제 기능을 직접 보는 명령(`ps`·`ss`·`systemctl`)은 리눅스 명령어 시트에, 컨테이너 실행과 클러스터 조작 명령(`docker`·`crictl`·`kubectl`)은 [클라우드 명령어 시트](../../../08_cloud/docs/cmd/README.md)에, 빌드와 배포 흐름에서 쓰는 도구는 이쪽에 둡니다. 이미 다른 폴더에 있는 시트는 옮기지 않고 아래 표에서 링크로 가리킵니다. `helm`·`kustomize` 는 시트를 따로 두지 않습니다. 명령과 실행 예까지 [iac](../iac/README.md) 문서가 주제별로 다룹니다.



## image — 이미지 빌드와 레지스트리

> 이미지를 만들고, 레지스트리 사이로 옮기고, 내용과 취약점을 확인하는 도구입니다. 후보는 `docker build`·`docker buildx`·`skopeo`·`crane`·`trivy` 입니다.

빌더를 고르는 기준과 rootless 빌드의 조건은 [artifact](../artifact/README.md)의 개념 편이 맡습니다. `buildctl` 시트는 그 폴더에 이미 있어서 링크만 둡니다. `docker` 로 컨테이너를 실행하고 조회하는 명령은 클라우드 명령어 시트가 맡고, 여기는 빌드와 레지스트리 전송만 다룹니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|
| [buildkit](../artifact/container/buildkit.md) | `buildctl` · `buildkitd` | `buildctl` 로 빌드하고 결과를 registry·tar 로 내보내거나 캐시를 주고받을 때 |
| [buildah](image/buildah.md) | `buildah` | 데몬 없이 Dockerfile 이나 셸 명령으로 OCI 이미지를 빌드하고, 셸 없는 이미지를 만들고, 저장소·tar 로 내보내고, 캐시·격리 방식을 고를 때 |
| [crane](image/crane.md) | `crane` | 데몬 없이 원격 저장소의 digest·manifest·config 를 읽거나, 저장소 사이 복사·태그·pull/push·mutate/append·삭제를 할 때 |
| [trivy](image/trivy.md) | `trivy` | 이미지·디렉터리·설정 파일·SBOM 의 알려진 취약점과 설정 오류를 찾고, CI 에서 종료 코드로 빌드를 막거나 폐쇄망에서 DB 갱신 없이 스캔할 때 |
| [cosign](image/cosign.md) | `cosign` | 이미지·파일에 서명하고 받는 쪽에서 확인하거나, 검증이 실패한 이유(서명 없음·다른 키·바뀐 이미지)를 가를 때 |



## gitops — 배포와 동기화

> Git 에 적힌 상태를 클러스터에 맞추고, 새 버전을 조금씩 내보내는 도구입니다. 후보는 `argocd`·`kubectl argo rollouts` 입니다.

Argo CD 의 원리는 [Argo CD 정독 노트](../../book/argocd-up-and-running/README.md)가, 배포 전략은 [Blue/Green 무중단 전환과 아키텍처 결정 기록](../../book/aic_ai-infra-claude/05-02.Blue-Green%20%EB%AC%B4%EC%A4%91%EB%8B%A8%20%EC%A0%84%ED%99%98%EA%B3%BC%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98%20%EA%B2%B0%EC%A0%95%20%EA%B8%B0%EB%A1%9D.md)과 [점진적 배포 Canary와 claude-context](../../book/aic_ai-infra-claude/06-02.%EC%A0%90%EC%A7%84%EC%A0%81%20%EB%B0%B0%ED%8F%AC%20Canary%EC%99%80%20claude-context.md) 정독 노트가 맡습니다.

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
- [iac](../iac/README.md) — Helm·Kustomize 의 원리와 명령
- [artifact](../artifact/README.md) — 이미지 빌드의 원리와 `buildctl` 시트
- [클라우드 명령어 시트](../../../08_cloud/docs/cmd/README.md) — `docker`·`crictl`·`kubectl` 처럼 컨테이너와 클러스터를 다루는 명령의 시트
