---
title: 07_devops/docs/artifact — 빌드 산출물
tags: [moc, devops, build, artifact, container-image]
status: draft
related:
  - ../../README.md
  - ../jenkins/01-01.Controller·Agent·Executor 와 JENKINS_HOME.md
updated: 2026-11-15
---

# 07_devops/docs/artifact — 빌드 산출물

---

> CI 가 소스를 받아 무엇을 만들어 내는지, 그 산출물을 어디서 어떤 도구로 굽는지를 다루는 자리입니다. 언어별 빌드 설정의 깊은 내용은 언어 폴더가 맡고, 여기서는 CI 파이프라인에서 보이는 모습만 봅니다.

## 폴더 규칙

> 산출물 종류마다 폴더를 하나 두고, 그 안에서 개념 편은 번호로, 도구 시트는 도구 이름으로 둡니다.

| 폴더 | 산출물 | 지금 상태 |
|------|--------|-----------|
| `container/` | 컨테이너 이미지 | 개념 편 셋과 도구 시트 하나 |
| `package/` | JAR·바이너리 같은 실행 패키지 | 아직 없음. 정본은 아래 「다른 폴더가 맡는 것」 |
| `vm/` | VM 이미지 | 폴더를 만들지 않았습니다. 아래 「다른 폴더가 맡는 것」 의 fdsd 두 절이 지금의 자리입니다 |

개념 편은 `{장}-{절}.{제목}.md` 로 번호를 받습니다. 여러 도구에 걸친 질문(왜 컨테이너 안 빌드가 어려운가, rootless 는 무엇을 요구하는가)을 차례로 쌓아 가기 때문입니다. 도구 시트는 `buildkit.md` 처럼 번호 없는 이름 파일로 둡니다. 개념 편과 읽는 순서를 다투지 않고, 도구 이름이 곧 찾는 단서이기 때문입니다. 도식은 개념 편에만 둡니다.



## 문서 목록

> 「언제」 열은 그 문서를 펼칠 상황입니다.

| 문서 | 산출물 | 언제 |
|------|--------|------|
| [01-01 컨테이너 안 빌드가 문제가 되는 이유](container/01-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EC%95%88%20%EB%B9%8C%EB%93%9C%EA%B0%80%20%EB%AC%B8%EC%A0%9C%EA%B0%80%20%EB%90%98%EB%8A%94%20%EC%9D%B4%EC%9C%A0.md) | 컨테이너 이미지 | CI 에이전트를 VM 에서 Pod 로 옮겼더니 `docker build` 가 데몬을 못 찾을 때 |
| [01-02 rootless 빌드의 조건](container/01-02.rootless%20%EB%B9%8C%EB%93%9C%EC%9D%98%20%EC%A1%B0%EA%B1%B4.md) | 컨테이너 이미지 | 특권 없이 빌드하려는데 RUN 단계가 권한 오류로 멈출 때 |
| [01-03 이미지 빌더 종류와 선택](container/01-03.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EB%B9%8C%EB%8D%94%20%EC%A2%85%EB%A5%98%EC%99%80%20%EC%84%A0%ED%83%9D.md) | 컨테이너 이미지 | BuildKit·Buildah·Jib·Buildpacks 가운데 무엇을 쓸지 정할 때 |
| [buildkit](container/buildkit.md) | 컨테이너 이미지 | `buildctl` 로 빌드하고 결과를 registry·tar 로 내보내거나 캐시를 주고받을 때 |



## 아직 안 쓴 것

> 쓸 순서대로 적었습니다. 이름이 정해진 파일은 그 이름으로 만듭니다.

- `container/` 도구 시트: `kaniko.md`(저장소가 2025-06-03 보관된 상태와 옮겨 갈 곳 포함), `jib.md`, `buildpacks.md`, `buildah.md`
- `container/02-01.레이어 캐시와 multi-stage.md`
- `container/02-02.멀티 플랫폼 이미지 빌드.md`
- `package/01-01.빌드 산출물과 CI 빌드의 조건.md`



## 다른 폴더가 맡는 것

> 같은 주제를 다른 폴더가 이미 깊게 다루면 여기서 다시 쓰지 않고 링크만 둡니다.

- Java 빌드와 패키징: [패키징·배포·CI](../../../01_language/java/06_Build/05-01.%ED%8C%A8%ED%82%A4%EC%A7%95%C2%B7%EB%B0%B0%ED%8F%AC%C2%B7CI.md) — 산출물 종류, Wrapper 로 맞추는 재현성, Jenkinsfile·GitHub Actions 예시
- Go 빌드: [Go 바이너리의 빌드 정보와 GOOS·GOARCH](../../../01_language/book/lgo_learning-go/11-04.Go%20%EB%B0%94%EC%9D%B4%EB%84%88%EB%A6%AC%EB%8A%94%20%EB%B9%8C%EB%93%9C%20%EC%A0%95%EB%B3%B4%EB%A5%BC%20%ED%92%88%EA%B3%A0%20GOOS%C2%B7GOARCH%20%EC%99%80%20%EB%B9%8C%EB%93%9C%20%ED%83%9C%EA%B7%B8%EB%A1%9C%20%EB%8C%80%EC%83%81%EC%9D%84%20%EA%B0%80%EB%A6%BD%EB%8B%88%EB%8B%A4.md)
- VM 이미지: [Server Templating Tools](../../book/fdsd_fundamentals-devops/02-01.How%20to%20Manage%20Your%20Infrastructure%20as%20Code.md#28-server-templating-tools)(Packer 로 굽는 이미지)와 [VM 오케스트레이션](../../book/fdsd_fundamentals-devops/03-01.How%20to%20Manage%20Your%20Apps.md#34-vm-오케스트레이션-vm-orchestration)
- 이미지 보안(베이스 이미지 고르기, 공급망): `08_cloud/book/` 의 cks-study-guide 06-01, container-security 06-01·06-02
- 산출물이 저장되는 곳: 레지스트리 문서는 artifact 아래에 두지 않고 `07_devops/docs/harbor/`·`07_devops/docs/nexus/` 에 둘 예정입니다. 지금은 [03_Nexus](../../03_Nexus/) 에 있습니다



## 관련 문서

- [07_devops MOC](../../README.md) — 대분류 지도
- [docs/jenkins](../jenkins/01-01.Controller%C2%B7Agent%C2%B7Executor%20%EC%99%80%20JENKINS_HOME.md) — 빌드를 돌리는 쪽. Agent 가 VM 인지 Pod 인지가 01-01 의 출발점입니다
