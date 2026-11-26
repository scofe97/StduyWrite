---
title: 07_devops/docs/jenkins — Jenkins 의 구조와 동작 원리
tags: [moc, devops, jenkins, ci, pipeline]
status: draft
related:
  - ../../README.md
  - ../artifact/README.md
  - ../iac/README.md
  - ../sonarqube/README.md
updated: 2026-11-21
---

# 07_devops/docs/jenkins — Jenkins 의 구조와 동작 원리

---

> Jenkins 가 빌드 요청을 받아 실행하고 상태를 남기는 과정을 원리 중심으로 다루는 자리입니다. 설정 화면을 따라 하는 절차나 API 호출 예제 모음은 두지 않고, 왜 그렇게 동작하는지와 어디서 깨지는지를 남겼습니다.

## 읽는 순서

> 장 번호 순서로 읽습니다. 1장과 2장이 뒤 편들의 전제이고, 3장부터는 필요한 장만 골라 읽어도 됩니다.

「언제」 열은 그 문서를 펼칠 상황입니다.

### 1장 구조

Jenkins 를 이루는 부품과 상태가 놓이는 자리입니다. 뒤의 모든 편이 이 그림을 전제로 합니다.

| 문서 | 언제 |
|------|------|
| [01-01 Controller·Agent·Executor 와 JENKINS_HOME](01-01.Controller%C2%B7Agent%C2%B7Executor%20%EC%99%80%20JENKINS_HOME.md) | Controller 와 Agent 가 왜 나뉘는지, `JENKINS_HOME` 의 어떤 파일을 잃으면 안 되는지 알고 싶을 때 |
| [01-02 정적 Agent 와 동적 Agent](01-02.%EC%A0%95%EC%A0%81%20Agent%20%EC%99%80%20%EB%8F%99%EC%A0%81%20Agent.md) | Launch method·Availability, SSH 기동 순서와 JVM 두 겹, 상시 노드와 동적 Agent 의 맞교환, Label 배정 기준을 볼 때 |
| [01-03 Executor 와 Agent JVM 의 일 나누기](01-03.Executor%20%EC%99%80%20Agent%20JVM%20%EC%9D%98%20%EC%9D%BC%20%EB%82%98%EB%88%84%EA%B8%B0.md) | executor 슬롯이 어느 JVM 에 있는지, step 이 채널을 거쳐 에이전트에서 실행되는 흐름, 재연결 때 돌던 빌드가 어떻게 되는지 볼 때 |


### 2장 엔진

요청 하나가 URL 에서 Executor 까지 가는 길을 소스로 따라갑니다.

| 문서 | 언제 |
|------|------|
| [02-01 Stapler 와 URL 이 doBuild 에 닿는 길](02-01.Stapler%20%EC%99%80%20URL%20%EC%9D%B4%20doBuild%20%EC%97%90%20%EB%8B%BF%EB%8A%94%20%EA%B8%B8.md) | `/job/이름/build` 같은 URL 이 어떤 객체의 어떤 메서드에 닿는지 추적할 때 |
| [02-02 Queue 상태 전이와 Executor 로 가는 길](02-02.Queue%20%EC%83%81%ED%83%9C%20%EC%A0%84%EC%9D%B4%EC%99%80%20Executor%20%EB%A1%9C%20%EA%B0%80%EB%8A%94%20%EA%B8%B8.md) | 빌드가 큐에서 멈춰 있는 이유를 큐 상태로 읽어야 할 때 |
| [02-03 Executor 배정과 동적 Pod](02-03.Executor%20%EB%B0%B0%EC%A0%95%EA%B3%BC%20%EB%8F%99%EC%A0%81%20Pod.md) | 빈 Executor 가 있는데도 빌드가 배정되지 않거나, Pod Agent 가 언제 만들어지는지 궁금할 때 |
| [02-04 podRetention·Garbage Collection](02-04.podRetention%C2%B7Garbage%20Collection.md) | 빌드가 끝난 Pod 가 남아 있거나 고아 Pod 가 쌓일 때 |


### 3장 Pipeline

Jenkinsfile 이 평가되는 규칙과, 제어 블록이 실행기를 얼마나 오래 쥐는지를 다룹니다.

| 문서 | 언제 |
|------|------|
| [03-01 Pipeline as Code 와 Declarative 평가 규칙](03-01.Pipeline%20as%20Code%20%EC%99%80%20Declarative%20%ED%8F%89%EA%B0%80%20%EA%B7%9C%EC%B9%99.md) | Declarative 와 Scripted 의 차이, 블록 우선순위, CI 스테이지를 어떤 순서로 둘지 정할 때 |
| [03-02 병렬·승인·재시도와 실행기 점유](03-02.%EB%B3%91%EB%A0%AC%C2%B7%EC%8A%B9%EC%9D%B8%C2%B7%EC%9E%AC%EC%8B%9C%EB%8F%84%EC%99%80%20%EC%8B%A4%ED%96%89%EA%B8%B0%20%EC%A0%90%EC%9C%A0.md) | `retry`·`timeout`·`input`·`parallel`·`when` 이 겹칠 때 실행기가 묶이는 시간을 줄이고 싶을 때 |
| [03-03 sh step 이 실패를 삼키는 이유](03-03.sh%20step%20%EC%9D%B4%20%EC%8B%A4%ED%8C%A8%EB%A5%BC%20%EC%82%BC%ED%82%A4%EB%8A%94%20%EC%9D%B4%EC%9C%A0.md) | `sh` step 의 실패가 빌드 성공으로 묻히거나, 시크릿을 문자열에 넣는 방식이 안전한지 따질 때 |


### 4장 내구성

Controller 가 재기동해도 Pipeline 이 이어지는 원리입니다.

| 문서 | 언제 |
|------|------|
| [04-01 재기동을 견디는 Pipeline](04-01.%EC%9E%AC%EA%B8%B0%EB%8F%99%EC%9D%84%20%EA%B2%AC%EB%94%94%EB%8A%94%20Pipeline.md) | 재기동 뒤 어떤 빌드는 이어지고 어떤 빌드는 죽는지, durability 설정을 무엇으로 둘지 정할 때 |


### 5장 Groovy 확장

Groovy 가 도는 자리와 권한, 공통 로직을 나누는 방법입니다.

| 문서 | 언제 |
|------|------|
| [05-01 Groovy 는 Jenkins 어디서 도는가](05-01.Groovy%20%EB%8A%94%20Jenkins%20%EC%96%B4%EB%94%94%EC%84%9C%20%EB%8F%84%EB%8A%94%EA%B0%80.md) | Pipeline 의 Groovy 가 어디서 어떤 권한으로 도는지, Script Console 을 열어도 되는지 판단할 때 |
| [05-02 Shared Library](05-02.Shared%20Library.md) | 여러 저장소의 Jenkinsfile 에 같은 코드가 복사돼 있어 한 곳으로 모으려 할 때 |
| [05-03 전역 Hook·Listener 와 Extension Point](05-03.%EC%A0%84%EC%97%AD%20Hook%C2%B7Listener%20%EC%99%80%20Extension%20Point.md) | 모든 빌드에 공통 규칙을 걸어야 하는데 Jenkinsfile 을 일일이 고칠 수 없을 때 |


### 6장 보안

누가 무엇을 할 수 있는지와, 빌드가 시스템을 해치지 못하게 막는 경계입니다.

| 문서 | 언제 |
|------|------|
| [06-01 인증·인가와 시크릿](06-01.%EC%9D%B8%EC%A6%9D%C2%B7%EC%9D%B8%EA%B0%80%EC%99%80%20%EC%8B%9C%ED%81%AC%EB%A6%BF.md) | 권한 모델을 고르거나, 시크릿의 노출 범위와 로그 마스킹의 한계를 따질 때 |
| [06-02 빌드 격리와 공격 표면](06-02.%EB%B9%8C%EB%93%9C%20%EA%B2%A9%EB%A6%AC%EC%99%80%20%EA%B3%B5%EA%B2%A9%20%ED%91%9C%EB%A9%B4.md) | 외부 PR 빌드가 자격증명을 읽을 수 있는지, 웹 계층과 포트를 어디까지 열지 정할 때 |


### 7장 운영

Jenkins 를 올리는 방법과 설정을 재현하는 방법, 크기를 정하는 기준입니다.

| 문서 | 언제 |
|------|------|
| [07-01 Kubernetes 에 Jenkins 를 올리는 이유와 방법](07-01.Kubernetes%20%EC%97%90%20Jenkins%20%EB%A5%BC%20%EC%98%AC%EB%A6%AC%EB%8A%94%20%EC%9D%B4%EC%9C%A0%EC%99%80%20%EB%B0%A9%EB%B2%95.md) | VM 의 Jenkins 를 Kubernetes 로 옮길지, Helm 차트와 JCasC 가 각각 무엇을 맡는지 볼 때 |
| [07-02 설정을 코드로 관리하는 JCasC](07-02.%EC%84%A4%EC%A0%95%EC%9D%84%20%EC%BD%94%EB%93%9C%EB%A1%9C%20%EA%B4%80%EB%A6%AC%ED%95%98%EB%8A%94%20JCasC.md) | UI 로 바꾼 설정을 다른 서버에 똑같이 재현할 수 없을 때 |
| [07-03 용량 산정과 성능 모니터링](07-03.%EC%9A%A9%EB%9F%89%20%EC%82%B0%EC%A0%95%EA%B3%BC%20%EC%84%B1%EB%8A%A5%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81.md) | Controller 의 CPU·힙을 얼마로 잡을지, 느려진 원인을 어떤 지표로 찾을지 정할 때 |


### 8장 REST API

외부 서비스가 Jenkins 를 부르고 결과를 받아 가는 방법입니다.

| 문서 | 언제 |
|------|------|
| [08-01 REST API 로 빌드를 부르고 추적하기](08-01.REST%20API%20%EB%A1%9C%20%EB%B9%8C%EB%93%9C%EB%A5%BC%20%EB%B6%80%EB%A5%B4%EA%B3%A0%20%EC%B6%94%EC%A0%81%ED%95%98%EA%B8%B0.md) | 다른 서비스에서 빌드를 시작하고 끝났는지 추적해야 할 때 |
| [08-02 stage 상태와 로그를 가져오는 wfapi](08-02.stage%20%EC%83%81%ED%83%9C%EC%99%80%20%EB%A1%9C%EA%B7%B8%EB%A5%BC%20%EA%B0%80%EC%A0%B8%EC%98%A4%EB%8A%94%20wfapi.md) | stage 단위 진행 상태와 로그를 가져오거나, 연동 방식을 정할 때 |



## 다른 폴더가 맡는 것

> 같은 주제를 다른 폴더가 이미 다루면 여기서 다시 쓰지 않고 링크만 둡니다.

- 컨테이너 이미지 빌드(데몬 없는 빌드, rootless, 빌더 선택): [artifact](../artifact/README.md)
- Helm 차트 작성과 릴리스 운영: [iac](../iac/README.md)
- 정적 분석과 Quality Gate 를 CI 에 붙이는 과정: [sonarqube](../sonarqube/README.md)
- GitOps 와 Argo CD 로 하는 배포: [Argo CD 정독 노트](../../book/argocd-up-and-running/README.md)



## 관련 문서

- [07_devops](../../README.md) — DevOps 카테고리 지도
