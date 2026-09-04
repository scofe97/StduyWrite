---
title: 08_cloud/troubleshooting — 쿠버네티스 트러블슈팅 사례집
tags: [moc, troubleshooting, kubernetes, incident, observability]
status: final
related:
  - ../README.md
  - ../kubernetes/README.md
  - ../../02_os/troubleshooting/README.md
updated: 2026-09-05
---

# 08_cloud/troubleshooting
---
> 클러스터 위에서 마주치는 장애를 증상에서 원인으로 역추적하는 사례집입니다. `kubernetes/`가 리소스의 동작을 설명한다면 여기는 그 동작이 어긋났을 때 어떤 명령을 어떤 순서로 치는지를 다룹니다.

문서 하나가 하나의 주제를 맡고, 그 안의 `## 사례`가 개별 장애 하나에 해당합니다. 사례마다 증상과 주어진 출력, 원인, 조치, 재발 방지가 같은 순서로 들어 있습니다.

사례 38건은 [Infratice](https://github.com/kiku99/Infratice)의 `content/problems/` 에서 가져와 재구성했습니다. 원문은 정답을 가린 문제 형식이고 이 문서들은 해설을 이어 붙인 형태라, 먼저 사이트에서 풀어 본 뒤 여기서 대조하는 순서를 권합니다.



## 문서

> 장 번호가 장애의 국면을 나눕니다. 01 기동, 02 자원과 스케줄링, 03 설정과 워크로드, 04 네트워크, 05 스토리지와 권한, 06 확장과 관측입니다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 01-01 | [이미지를 못 가져올 때 — ImagePullBackOff·시크릿·롤백](01-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%EB%A5%BC%20%EB%AA%BB%20%EA%B0%80%EC%A0%B8%EC%98%AC%20%EB%95%8C%20%E2%80%94%20ImagePullBackOff%C2%B7%EC%8B%9C%ED%81%AC%EB%A6%BF%C2%B7%EB%A1%A4%EB%B0%B1.md) | 같은 `ImagePullBackOff` 뒤에 선 세 가지 원인을 무엇으로 가르는가? |
| 01-02 | [컨테이너가 죽거나 준비되지 않을 때 — CrashLoop·Init·사이드카·readiness](01-02.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EA%B0%80%20%EC%A3%BD%EA%B1%B0%EB%82%98%20%EC%A4%80%EB%B9%84%EB%90%98%EC%A7%80%20%EC%95%8A%EC%9D%84%20%EB%95%8C%20%E2%80%94%20CrashLoop%C2%B7Init%C2%B7%EC%82%AC%EC%9D%B4%EB%93%9C%EC%B9%B4%C2%B7readiness.md) | Pod 기동의 네 관문 중 어디에서 멈췄는지를 어떻게 아는가? |
| 02-01 | [자원 한계 — requests·limits와 OOMKilled](02-01.%EC%9E%90%EC%9B%90%20%ED%95%9C%EA%B3%84%20%E2%80%94%20requests%C2%B7limits%EC%99%80%20OOMKilled.md) | `requests` 가 없을 때와 `limits` 가 작을 때는 각각 무엇이 다른가? |
| 02-02 | [Pending 의 원인들 — affinity·taint·HPA 메트릭](02-02.Pending%20%EC%9D%98%20%EC%9B%90%EC%9D%B8%EB%93%A4%20%E2%80%94%20affinity%C2%B7taint%C2%B7HPA%20%EB%A9%94%ED%8A%B8%EB%A6%AD.md) | `Pending` 의 사유를 `FailedScheduling` 이벤트에서 어떻게 읽는가? |
| 03-01 | [설정 주입 — ConfigMap 마운트·subPath·리로드](03-01.%EC%84%A4%EC%A0%95%20%EC%A3%BC%EC%9E%85%20%E2%80%94%20ConfigMap%20%EB%A7%88%EC%9A%B4%ED%8A%B8%C2%B7subPath%C2%B7%EB%A6%AC%EB%A1%9C%EB%93%9C.md) | ConfigMap 을 붙였는데 왜 원래 파일이 사라지는가? |
| 03-02 | [배치 워크로드 — Job·CronJob·네임스페이스](03-02.%EB%B0%B0%EC%B9%98%20%EC%9B%8C%ED%81%AC%EB%A1%9C%EB%93%9C%20%E2%80%94%20Job%C2%B7CronJob%C2%B7%EB%84%A4%EC%9E%84%EC%8A%A4%ED%8E%98%EC%9D%B4%EC%8A%A4.md) | 배치 작업의 실패는 왜 며칠 뒤에야 발견되는가? |
| 04-01 | [서비스 디스커버리 — Service·EndpointSlice·DNS](04-01.%EC%84%9C%EB%B9%84%EC%8A%A4%20%EB%94%94%EC%8A%A4%EC%BB%A4%EB%B2%84%EB%A6%AC%20%E2%80%94%20Service%C2%B7EndpointSlice%C2%B7DNS.md) | Service 이름으로 접속이 안 될 때 가장 먼저 볼 것은 무엇인가? |
| 04-02 | [외부 진입과 트래픽 분할 — Ingress·가중치·컨테이너 네트워크](04-02.%EC%99%B8%EB%B6%80%20%EC%A7%84%EC%9E%85%EA%B3%BC%20%ED%8A%B8%EB%9E%98%ED%94%BD%20%EB%B6%84%ED%95%A0%20%E2%80%94%20Ingress%C2%B7%EA%B0%80%EC%A4%91%EC%B9%98%C2%B7%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC.md) | 404 와 연결 거부와 이름 해석 실패는 각각 어느 계층인가? |
| 05-01 | [볼륨 — PVC 확장·StorageClass·권한](05-01.%EB%B3%BC%EB%A5%A8%20%E2%80%94%20PVC%20%ED%99%95%EC%9E%A5%C2%B7StorageClass%C2%B7%EA%B6%8C%ED%95%9C.md) | PVC 만 봐서는 왜 스토리지 문제가 안 풀리는가? |
| 05-02 | [권한과 격리 — RBAC·NetworkPolicy·TLS·nonroot](05-02.%EA%B6%8C%ED%95%9C%EA%B3%BC%20%EA%B2%A9%EB%A6%AC%20%E2%80%94%20RBAC%C2%B7NetworkPolicy%C2%B7TLS%C2%B7nonroot.md) | 무엇이 막았는지를 에러의 형태로 어떻게 가르는가? |
| 06-01 | [CRD 로 API 넓히기 — 등록과 스키마 검증](06-01.CRD%20%EB%A1%9C%20API%20%EB%84%93%ED%9E%88%EA%B8%B0%20%E2%80%94%20%EB%93%B1%EB%A1%9D%EA%B3%BC%20%EC%8A%A4%ED%82%A4%EB%A7%88%20%EA%B2%80%EC%A6%9D.md) | CRD 는 API 를 늘리는 대신 무엇을 함께 떠맡는가? |
| 06-02 | [클러스터 관측 — 스크레이프·알림·대시보드·TSDB](06-02.%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EA%B4%80%EC%B8%A1%20%E2%80%94%20%EC%8A%A4%ED%81%AC%EB%A0%88%EC%9D%B4%ED%94%84%C2%B7%EC%95%8C%EB%A6%BC%C2%B7%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C%C2%B7TSDB.md) | 대시보드가 비었을 때 어느 단계가 끊겼는지 어떻게 좁히는가? |



## 어디부터 읽나

> 장애 대응 중이라면 Pod 상태에 맞는 장으로 바로 갑니다. 학습이 목적이면 01장부터 기동 순서를 따라가는 편이 낫습니다.

증상으로 찾을 때는 `kubectl get pods`의 두 열이 안내가 됩니다. `ImagePullBackOff` 는 01-01, `CrashLoopBackOff` 와 `Init:0/1` 은 01-02, `Pending` 은 02-02, `Evicted` 는 02-01 입니다. 접속이 안 되면 04장, 볼륨이면 05-01, 권한 거절이면 05-02 입니다.

학습이 목적이면 번호가 곧 순서입니다. 01장이 Pod 가 뜨기까지, 02장이 놓일 자리와 자원, 03장이 설정과 배치 작업, 04장이 트래픽, 05장이 상태와 권한, 06장이 확장과 그 전체를 지켜보는 층을 다룹니다.

여러 문서에 걸쳐 반복되는 명령이 셋 있습니다.

- `kubectl describe`: 상태와 이벤트를 읽습니다
- `kubectl logs --previous`: 죽기 직전 인스턴스의 마지막 말을 봅니다
- `kubectl get endpoints`: Service 와 Pod 가 실제로 연결됐는지 확인합니다



## 트러블슈팅 연습 사이트

> 아래 목록은 각 사이트를 직접 열어 제목과 소개 문구를 확인한 것입니다(2026-09-05 기준). 유료 여부와 무료 범위는 자주 바뀌므로 링크에서 직접 확인합니다.

| 사이트 | 방식 | 다루는 범위 |
|--------|------|------------|
| [Infratice](https://infratice.co.kr/) | 정적 문제 — 로그·설정만 보고 원인을 추론하고 AI로 풀이를 검토 | Linux · Kubernetes · Network · CI/CD · Monitoring (한국어) |
| [SadServers](https://sadservers.com/scenarios) | 브라우저 안 실서버에 붙어 제한 시간 안에 복구 | Linux 트러블슈팅 랩, 면접·채용 평가 겸용 |
| [iximiuz Labs](https://labs.iximiuz.com/) | 브라우저나 SSH로 실서버 실습, 학습 경로 제공 | Linux · Docker · Kubernetes · Networking |
| [Killercoda](https://killercoda.com/) | 브라우저 터미널 시나리오, 직접 시나리오 작성 가능 | DevOps · Linux · Kubernetes · CKA/CKS/CKAD |
| [Killer Shell](https://killer.sh/) | 자격 시험 시뮬레이터 | CKA · CKS · CKAD · LFCS · CNPE |
| [KodeKloud](https://kodekloud.com/) | 핸즈온 랩과 가이드 영상 | DevOps · Cloud · AI 전반 |
| [Deadnodes](https://deadnodes.com/) | 실습·팀 챌린지·면접 워크플로를 묶은 플랫폼 | 시스템 엔지니어링 실습 |
| [DevOpsEngine Labs](https://devopsengine.cloud/labs/) | 핸즈온 랩 | Kubernetes · Linux · CI/CD · 트러블슈팅 |
| [Kubernetes Troubleshooting (LFWS313)](https://training.linuxfoundation.org/training/kubernetes-troubleshooting-lfws313/) | Linux Foundation 공식 과정, 랩과 실사례 중심 | Kubernetes |
| [DevOps-Learn-By-Doing](https://github.com/deepakkumar-platform/DevOps-Learn-By-Doing) | 무료 랩·챌린지 큐레이션 저장소 | Linux 부터 Kubernetes 까지 |

성격으로 나누면 셋입니다.

- 정적 문제: Infratice — 환경 없이 로그와 설정만 읽습니다
- 대화형 셸: SadServers · iximiuz Labs · Killercoda · Killer Shell — 실제 서버를 줍니다
- 학습 과정: LFWS313 · DevOps-Learn-By-Doing — 커리큘럼과 큐레이션입니다

쿠버네티스만 놓고 보면 Killercoda 와 Killer Shell 이 가장 밀도가 높습니다. 자격 시험 문제가 곧 트러블슈팅 문제이기 때문입니다.



## 참고 읽을거리

> 사례를 다 풀고 나서 같은 증상을 더 넓게 훑고 싶을 때 읽습니다.

- [쿠버네티스 공식 — 클러스터 디버깅](https://kubernetes.io/ko/docs/tasks/debug/debug-cluster/)
- [50 Common Errors in Kubernetes](https://www.linkedin.com/pulse/50-common-errors-kubernetes-avinash-tietler-ocoqc/)
- [Common Kubernetes Errors and How to Troubleshoot Them](https://www.linkedin.com/pulse/common-kubernetes-errors-how-troubleshoot-them-pramod-medi-mjkgc/)



## 상위·이웃

> 이 폴더가 어느 문서들 사이에 놓이는지를 정리합니다.

- 상위: [08_cloud MOC](../README.md)
- 이웃: [08_cloud/kubernetes/](../kubernetes/README.md) — 여기 사례들이 다루는 리소스의 개념과 운영
- 짝: [02_os/troubleshooting/](../../02_os/troubleshooting/README.md) — 같은 사례집의 리눅스 호스트 편
- 관측: [06_observability/](../../06_observability/README.md) — 06-02 가 다루는 스택의 설계와 운영

> 사례 원문은 [Infratice](https://github.com/kiku99/Infratice)(MIT, `0aba7df`)의 `content/problems/` 에서 가져와 재구성했습니다.
