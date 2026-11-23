---
title: 07_devops/docs/artifact — 빌드 산출물
tags: [moc, devops, build, artifact, container-image]
status: draft
related:
  - ../../README.md
  - ../jenkins/01-01.Controller·Agent·Executor 와 JENKINS_HOME.md
updated: 2026-11-23
---

# 07_devops/docs/artifact — 빌드 산출물

---

> CI 가 소스를 받아 무엇을 만들어 내는지, 그 산출물을 어디서 어떤 도구로 굽는지를 다루는 자리입니다. 언어별 빌드 설정의 깊은 내용은 언어 폴더가 맡고, 여기서는 CI 파이프라인에서 보이는 모습만 봅니다.

## 폴더 규칙

> 산출물 종류마다 폴더를 하나 두고, 그 안에서 개념 편은 번호로, 도구 시트는 도구 이름으로 둡니다.

| 폴더 | 산출물 | 지금 상태 |
|------|--------|-----------|
| `container/` | 컨테이너 이미지 | 개념 편 여덟과 도구 시트 하나 |
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
| [02-01 JDK 이미지가 서로 다른 이유](container/02-01.JDK%20%EC%9D%B4%EB%AF%B8%EC%A7%80%EA%B0%80%20%EC%84%9C%EB%A1%9C%20%EB%8B%A4%EB%A5%B8%20%EC%9D%B4%EC%9C%A0.md) | 컨테이너 이미지 | 보안 패치로 이미지의 JDK 만 바꾸려는데, 이미지마다 JDK 가 들어 있는 모양이 달라 어디를 봐야 할지 모를 때 |
| [02-02 JDK 배포판이 여럿인 이유](container/02-02.JDK%20%EB%B0%B0%ED%8F%AC%ED%8C%90%EC%9D%B4%20%EC%97%AC%EB%9F%BF%EC%9D%B8%20%EC%9D%B4%EC%9C%A0.md) | 컨테이너 이미지 | JDK 를 바꾸면 TLS 같은 동작이 달라질 수 있다는데, 배포판 차이인지 업데이트 판 차이인지 가려야 할 때 |
| [03-01 이미지 구조와 digest](container/03-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EA%B5%AC%EC%A1%B0%EC%99%80%20digest.md) | 컨테이너 이미지 | 같은 이미지인데 머신마다 이미지 ID 가 다르거나, 레지스트리를 옮긴 뒤 digest 가 달라져 같은 이미지인지 가려야 할 때 |
| [03-02 레지스트리 통신과 오프라인 반입](container/03-02.%EB%A0%88%EC%A7%80%EC%8A%A4%ED%8A%B8%EB%A6%AC%20%ED%86%B5%EC%8B%A0%EA%B3%BC%20%EC%98%A4%ED%94%84%EB%9D%BC%EC%9D%B8%20%EB%B0%98%EC%9E%85.md) | 컨테이너 이미지 | HTTP 사내 레지스트리에서 이미지를 받아 폐쇄망으로 옮겨 올리는데 로그인·pull·push 가 막힐 때 |
| [03-03 layer 변경분과 whiteout](container/03-03.layer%20%EB%B3%80%EA%B2%BD%EB%B6%84%EA%B3%BC%20whiteout.md) | 컨테이너 이미지 | Dockerfile 뒤 단계에서 지운 파일 때문에 이미지 크기가 줄지 않거나, 지운 줄 알았던 파일이 tar 에서 꺼내질 때 |
| [buildkit](container/buildkit.md) | 컨테이너 이미지 | `buildctl` 로 빌드하고 결과를 registry·tar 로 내보내거나 캐시를 주고받을 때 |



## 아직 안 쓴 것

> 쓸 순서대로 적었습니다. 이름이 정해진 파일은 그 이름으로 만듭니다.

- `container/` 도구 시트: `kaniko.md`(저장소가 2025-06-03 보관된 상태와 옮겨 갈 곳 포함), `jib.md`, `buildpacks.md` (`buildah` 는 [명령어 시트](../cmd/image/buildah.md)로 썼습니다)
- `container/02-01.레이어 캐시와 multi-stage.md`
- `container/02-03.멀티 플랫폼 이미지 빌드.md`
- `package/01-01.빌드 산출물과 CI 빌드의 조건.md`
- `container/03-01` 보강(학습 세션이 끝난 뒤): index 가 선택 항목이라는 단서와 digest 의 `알고리즘:값` 꼴을 더합니다. 명세의 `ImageID` 정의(config 의 sha256)와 `platform.variant` 규칙도 넣습니다. 여럿이 맞을 때 첫 항목을 쓰는 규칙, `oci-layout` 파일, `org.opencontainers.image.ref.name` 도 함께 적습니다.



## OCI 명세와 문서 후보 뽑기

> 컨테이너 표준 명세 세 편과, 원문에서 새 문서 후보를 고르는 기준을 둡니다.

OCI(Open Container Initiative)는 컨테이너 이미지 형식과 실행 규격을 정하는 표준 기구입니다. 명세는 이미지·배포·실행 세 편으로 나뉩니다. 이 폴더의 `container/` 문서는 그중 이미지 형식과 레지스트리 통신 두 편에 기대고 있습니다.

| 명세 | 정하는 것 | 원문 | 먼저 읽을 파일 | 지금 닿아 있는 문서 |
|------|-----------|------|----------------|---------------------|
| image-spec | 이미지를 이루는 파일(index·manifest·config·layer)의 형식과 digest | [v1.1.1 (2025-03-03)](https://github.com/opencontainers/image-spec/tree/v1.1.1) | `spec.md` 에서 시작해 `manifest.md`·`image-index.md`·`descriptor.md`·`config.md`·`layer.md`·`image-layout.md` | [03-01 이미지 구조와 digest](container/03-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EA%B5%AC%EC%A1%B0%EC%99%80%20digest.md), [03-03 layer 변경분과 whiteout](container/03-03.layer%20%EB%B3%80%EA%B2%BD%EB%B6%84%EA%B3%BC%20whiteout.md) |
| distribution-spec | 레지스트리와 이미지를 주고받는 HTTP API | [v1.1.1 (2025-01-29)](https://github.com/opencontainers/distribution-spec/blob/v1.1.1/spec.md) | `spec.md` 한 편. 「Workflow Categories」 의 Pull·Push·Content Discovery·Content Management 네 갈래와 「Endpoints」·「Error Codes」 | [03-02 레지스트리 통신과 오프라인 반입](container/03-02.%EB%A0%88%EC%A7%80%EC%8A%A4%ED%8A%B8%EB%A6%AC%20%ED%86%B5%EC%8B%A0%EA%B3%BC%20%EC%98%A4%ED%94%84%EB%9D%BC%EC%9D%B8%20%EB%B0%98%EC%9E%85.md) |
| runtime-spec | 풀어 놓은 이미지를 컨테이너로 실행하는 설정과 생명주기 | [v1.3.0 (2025-11-04)](https://github.com/opencontainers/runtime-spec/tree/v1.3.0) | `spec.md` 에서 시작해 `bundle.md`·`runtime.md`·`config.md`·`config-linux.md` | 이 폴더에는 없음. 가장 가까운 문서는 [컨테이너 런타임 인터페이스·crictl](../../../08_cloud/docs/kubernetes/architecture/%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%9F%B0%ED%83%80%EC%9E%84%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4%C2%B7crictl.md) |

runtime-spec 은 빌드 산출물이 아니라 실행 영역이므로, 후보가 나오면 다른 폴더에 두고 어느 폴더인지는 그때 정합니다. 원문 링크를 `main` 브랜치 대신 릴리스 태그로 건 까닭은 판마다 문장이 바뀌어 인용이 어긋나기 때문입니다.

1. 가장 새 릴리스 태그를 확인하고 원문을 그 태그로 받습니다.
2. 명세 파일마다 사실을 한 줄씩 뽑습니다. 사실은 독자가 알면 판단이 달라지는 규칙·구조·값입니다. 거버넌스·릴리스 절차·Go 타입 정의는 뽑지 않습니다.
3. 사실마다 이 폴더와 다른 폴더 문서에서 같은 말을 찾아 다섯으로 가릅니다. 분류는 다룸, 다른 문서가 다룸, 빈 곳, 어긋남, 일부러 뺌입니다. 절 제목만 보고 「다뤘다」고 하지 않습니다.
4. 어긋남은 후보보다 먼저 고칩니다.
5. 빈 곳 가운데 「모르면 실무에서 무엇을 틀리는가」를 한 문장으로 쓸 수 있는 것만 후보로 남깁니다.
6. 후보마다 있는 편에 몇 문단 더하기, 새 편, 링크만 중 둘 자리를 정합니다. 다른 폴더가 이미 다뤘으면 링크만 둡니다.
7. 맥북의 `docker`·`crane`·`jq`·`tar` 로 직접 확인할 수 있는 후보를 먼저 씁니다. 정해진 후보는 「아직 안 쓴 것」에 파일 이름으로 올립니다.



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
