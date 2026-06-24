---
title: Jenkins Agent·컨테이너·K8s 학습 MOC
tags: [moc, jenkins, agent, docker, kubernetes, kaniko]
status: draft
related:
  - ../../README.md
  - ../01_core/README.md
  - ../02_security/README.md
  - ../05_operations/README.md
updated: 2026-05-28
---

# Jenkins Agent·컨테이너·K8s 학습 MOC

---

> Jenkins 빌드가 "어디서 도는가" 를 결정하는 실행 환경 두 갈래 — VM/도커 Agent 와 Kubernetes Agent — 를 한 폴더로 모았습니다. 본 묶음을 끝내면 "내 빌드가 어떤 호스트의 어떤 격리 경계 안에서 도는지, 그리고 그 경계를 컨테이너 이미지로 어떻게 박제하는지" 를 한 흐름으로 답할 수 있습니다.

## 왜 한 폴더로 묶었는가

Agent(구 04) 와 Kubernetes Jenkins(구 08) 는 의외로 같은 질문에 답합니다. "이 빌드를 누가, 어떤 격리로, 어떤 빌드 도구로 돌리는가" — Agent 절은 그 격리를 VM·Docker 컨테이너로 풀고, K8s 절은 같은 격리를 Pod 로 풉니다. 두 답을 인접한 장 번호로 두면 "VM 도커 에이전트 → 쿠버네티스 동적 Pod" 라는 운영 진화 경로가 자연스럽게 잡힙니다.

01장이 *실행 단위* 와 *컨테이너 이미지 빌드* 의 기초를 세우고, 02장이 그 단위를 *K8s Pod 로 동적 프로비저닝* 하는 방식으로 확장합니다.

## 학습 순서

| 장 | # | 문서 | 다루는 핵심 |
|----|---|------|-----------|
| 01 Agent·컨테이너 | 01-00 | [점검 — 핵심 질문과 답 (Agent)](01-00.점검.핵심%20질문과%20답%20%28Agent%29.md) | 01장 진입 전 자가 점검 |
| 01 Agent·컨테이너 | 01-01 | [실행환경으로서의 Agent](01-01.실행환경으로서의%20Agent.md) | Built-in node 한계, SSH/JNLP Agent, Label 매칭, Executor |
| 01 Agent·컨테이너 | 01-02 | [Docker with Pipeline](01-02.Docker%20with%20Pipeline.md) | `agent { docker { ... } }`, args, reuseNode, 이미지 풀 정책 |
| 01 Agent·컨테이너 | 01-03 | [빌드 도구 비교와 선택](01-03.빌드%20도구%20비교와%20선택.md) | Docker, Buildah, Kaniko, BuildKit — 권한·캐시·속도 트레이드오프 |
| 01 Agent·컨테이너 | 01-04 | [컨테이너 이미지 빌드](01-04.컨테이너%20이미지%20빌드.md) | Dockerfile, multi-stage, 캐시 전략, 레지스트리 푸시 |
| 01 Agent·컨테이너 | 01-05 | [VM Jenkins에서의 Docker 보안 모델](01-05.VM%20Jenkins에서의%20Docker%20보안%20모델.md) | docker.sock 노출 위험, rootless, DinD vs DooD |
| 02 K8s | 02-00 | [점검 — 핵심 질문과 답 (K8s)](02-00.점검.핵심%20질문과%20답%20%28K8s%29.md) | 02장 진입 전 자가 점검 |
| 02 K8s | 02-01 | [Kubernetes Jenkins 구축](02-01.Kubernetes%20Jenkins%20구축.md) | kubernetes-plugin, Pod Template, ServiceAccount, PVC |
| 02 K8s | 02-02 | [Kubernetes Jenkins 운영](02-02.Kubernetes%20Jenkins%20운영.md) | 자원 할당, GC, 로그 수집, 노드 친화도 |

처음 진입자는 01-01 부터 순서대로 따라가면 됩니다. 이미 VM 위 Docker Agent 를 쓰고 있다면 01-05 의 보안 모델로 자기 환경의 노출 지점을 점검합니다. K8s 환경이라면 02-01·02-02 로 직진한 뒤, 막히면 01-03 의 빌드 도구 비교로 돌아옵니다.

## 환경과 버전

> 본 묶음 예제는 다음 조합 기준입니다.

| 항목 | 값 | 비고 |
|------|-----|------|
| Jenkins | LTS 2.426.x 이상 | docker-workflow, kubernetes 플러그인 동봉 |
| Docker | 24.x 이상 | rootless 모드 지원 |
| Kubernetes | 1.28 이상 | PodSecurity 표준 적용 |
| Kaniko | gcr.io/kaniko-project/executor 최신 | rootless 이미지 빌드 |

## 사전 지식

> 이 묶음은 다음을 안다고 가정합니다.

1. [`../01_core/`](../01_core/README.md) 의 Pipeline 기본 구조(agent/stages/steps) 를 알고 있습니다.
2. Docker `build`/`run` 명령을 셸에서 실행해 본 적이 있습니다.
3. Kubernetes 의 Pod·Service·Namespace 개념을 한 줄로 설명할 수 있습니다.

위 항목 중 막히는 부분이 있으면 [`../01_core/`](../01_core/README.md) 또는 Docker·K8s 입문 자료를 먼저 보고 돌아오는 편이 빠릅니다.

## 면접 대비 체크리스트

> 두 장을 다 읽은 뒤 다음 질문에 답할 수 있어야 합니다.

1. Built-in node 에서 빌드를 돌리지 말라는 권고가 있는 이유는? Agent 분리가 격리하는 것은 정확히 무엇입니까?
2. `agent { docker { ... } }` 의 `reuseNode` 옵션은 어떤 차이를 만듭니까? 옵션을 끄면 무엇이 새로 생기나요?
3. docker.sock 호스트 마운트가 위험한 이유는? DooD 와 DinD 의 트레이드오프는?
4. Kaniko 가 Docker 데몬 없이 이미지를 빌드할 수 있는 메커니즘은? 캐시 전략에서 Kaniko 의 약점은?
5. kubernetes-plugin 의 Pod Template 에서 ServiceAccount 를 분리하는 이유는?

각 질문에 막히면 해당 절로 돌아갑니다.
