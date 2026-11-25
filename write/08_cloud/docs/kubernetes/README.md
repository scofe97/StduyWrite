---
title: 08_cloud/docs/kubernetes — 쿠버네티스 공식문서 정독
tags: [moc, kubernetes, official-docs]
status: final
related:
  - ../README.md
  - ../../README.md
  - ../../../_archive/08_cloud/kubernetes/README.md
updated: 2026-11-15
---

# 08_cloud/docs/kubernetes — 쿠버네티스 공식문서 정독

---

> k8s.io 공식문서를 1차 자료로 삼아 궁금한 주제만 한 편씩 파고드는 자리입니다. 전체 개념을 순서대로 훑는 일은 [book/](../../book/)의 정독 노트와 [kubernetes/](../../../_archive/08_cloud/kubernetes/README.md)의 주제별 노트가 맡습니다.

## 폴더 규칙

> 문서는 묶음 폴더 넷(`architecture/`·`scheduling/`·`operations/`·`api/`) 중 하나에 두고, 파일명에는 번호를 붙이지 않습니다.

이 폴더의 문서는 처음부터 차례로 읽는 연재가 아닙니다. 궁금한 주제를 한 편씩 골라 읽으므로 파일명은 한글 문서 이름만으로 짓습니다. 이름은 명사구 하나로 쓰고, 다루는 대상이 둘 이상이면 `와/과` 대신 `·` 로 잇습니다(예: `노드 추가·제거.md`, `이미지 pull·폐쇄망 반입.md`). 제목에 ` — ` 로 붙은 부제는 파일명에서 뺍니다. 그래서 파일명과 H1 제목은 다를 수 있습니다(파일 `노드·클러스터 소속.md`, 제목 「노드와 클러스터의 소속 — …」). 사례 편은 어느 사례인지 가려야 해서 부제까지 둡니다(`OOMKilled 사례 — Endowus Rebalance 서비스.md`).

| 폴더 | 묶음 | 다루는 것 |
|------|------|-----------|
| `architecture/` | 아키텍처 | 노드·컨트롤러·런타임·이미지처럼 클러스터가 어떻게 짜여 있는지 |
| `scheduling/` | 스케줄링·축출 | 파드를 어디에 놓고 언제 내보낼지 |
| `operations/` | 클러스터 운영 | 관측·로깅·etcd·업그레이드·노드 추가처럼 클러스터를 굴리고 손대는 일 |
| `api/` | API | 헬스 엔드포인트·인증서·kubeconfig·조회 문법처럼 API 서버와 대화하는 규칙 |

새 문서는 묶음 하나를 골라 그 폴더에 두고 아래 「문서 목록」 의 그 묶음 표에 한 줄을 더합니다. 어느 묶음에도 들지 않으면 폴더와 표를 하나씩 더합니다. 묶음 폴더 이름은 번호 없는 영어 kebab 입니다(`02_os/docs/cmd/shell/` 과 같은 방식). 도식과 생성기는 문서가 있는 묶음 폴더의 `_assets/` 에 `{문서 이름}.{주제}.svg` 로 두고, 생성기는 `_assets/_gen/` 에서 그 폴더의 `_assets/dd.py` 를 씁니다. 도식 센서(`dd-verify-all.sh`)가 문서 옆의 `_assets/` 만 보기 때문입니다.

공식 문서의 어느 페이지를 읽었는지는 프론트매터 `source` 가 맡습니다. 첫 줄에 1차 근거 페이지를 두면 URL 의 `concepts`·`tasks`·`reference` 갈래로 원리를 읽었는지 절차를 읽었는지가 드러납니다.

> 2026-11-12 이전에는 k8s.io 섹션 슬러그와 같은 이름의 폴더 다섯 개에 한 편씩 두었습니다. 「자원 모니터링 파이프라인」 은 출처가 모두 `tasks/debug` 와 `reference` 여서 폴더 이름과 어긋났고, 폴더마다 한 편뿐이라 평탄하게 바꿨습니다. 2026-11-15 에 묶음 폴더 넷으로 다시 나눈 것은 그때와 두 가지가 다르기 때문입니다. 폴더 기준이 URL 섹션이 아니라 이 README 의 묶음이고, 묶음마다 이미 쓴 편과 「아직 안 쓴 주제」 가 쌓여 있습니다. 그 사이에는 "한 묶음이 5편이면 폴더로 올린다" 는 규칙으로 운영 묶음만 `03_operations/` 로 올라가 있었는데, 그 폴더의 문서는 도식이 상위 `_assets/` 에 있어 도식 센서가 보지 못했습니다.



## 문서 목록

> 묶음마다 표 하나입니다. 묶음의 뜻은 위 「폴더 규칙」 표에 있습니다.

### 아키텍처 (`architecture/`)

| 제목 | 한 줄 소개 |
|------|-----------|
| [노드와 클러스터의 소속 — 겹쳐 보이는 클러스터는 어느 층에서 겹치는가](architecture/%EB%85%B8%EB%93%9C%C2%B7%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%86%8C%EC%86%8D.md) | 노드가 클러스터에 소속되는 경로를 kubelet 자가등록으로 따라가고, 여러 클러스터가 노드를 겹쳐 쓴다는 말이 어느 층의 이야기인지 가릅니다. |
| [컨테이너 런타임 인터페이스·crictl](architecture/%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%9F%B0%ED%83%80%EC%9E%84%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4%C2%B7crictl.md) | kubelet 이 CRI 소켓으로 containerd 를 부르는 경로를 따라가고, `crictl`·`ctr`·`nerdctl` 이 각각 무엇을 보는지와 cgroup 드라이버를 맞춰야 하는 이유를 봅니다. |
| [이미지 pull과 폐쇄망 반입 — 노드는 이미지를 어디서 누구의 자격으로 받는가](architecture/%EC%9D%B4%EB%AF%B8%EC%A7%80%20pull%C2%B7%ED%8F%90%EC%87%84%EB%A7%9D%20%EB%B0%98%EC%9E%85.md) | kubelet 에서 레지스트리까지의 pull 경로와 `imagePullPolicy`, `imagePullSecrets` 와 노드 containerd 설정이라는 자격 두 자리를 가르고, 사설 CA·미러와 폐쇄망 반입, 이벤트 메시지별 진단 순서를 봅니다. |

### 스케줄링·축출 (`scheduling/`)

| 제목 | 한 줄 소개 |
|------|-----------|
| [노드 압박 축출과 디스크 관리 — DiskPressure는 무엇을 보고 켜지는가](scheduling/%EB%85%B8%EB%93%9C%20%EC%95%95%EB%B0%95%20%EC%B6%95%EC%B6%9C%C2%B7%EB%94%94%EC%8A%A4%ED%81%AC%20%EA%B4%80%EB%A6%AC.md) | kubelet 이 자원 신호를 재고 노드 컨디션을 달고 자원을 회수한 뒤 파드를 고르는 다섯 단을 따라갑니다. 디스크 관리가 여기 붙습니다. |

### 클러스터 운영 (`operations/`)

| 제목 | 한 줄 소개 |
|------|-----------|
| [자원 모니터링 파이프라인 — kubelet이 재는 것과 kubectl top이 읽는 것](operations/%EC%9E%90%EC%9B%90%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8.md) | `kubectl top` 의 숫자가 cAdvisor 에서 metrics-server 를 거쳐 오는 경로를 따라가고, 이 내장 파이프라인의 경계를 긋습니다. kubelet 통계 API(`/stats/summary`) 경로와 `nodes/stats`·`nodes/proxy` 권한도 함께 봅니다. |
| [etcd 헬스와 유지보수 — 상태 판독과 compaction·defrag·quota](operations/etcd%20%ED%97%AC%EC%8A%A4%C2%B7%EC%9C%A0%EC%A7%80%EB%B3%B4%EC%88%98.md) | `etcdctl` 세 명령으로 멤버 상태를 읽고, compaction·defrag·quota 가 맞물려 NOSPACE 로 쓰기가 멈추는 과정과 복구 순서, snapshot 확인을 봅니다. |
| [클러스터 업그레이드와 ETCD 백업·복구](operations/%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%97%85%EA%B7%B8%EB%A0%88%EC%9D%B4%EB%93%9C%C2%B7ETCD%20%EB%B0%B1%EC%97%85%C2%B7%EB%B3%B5%EA%B5%AC.md) | `kubeadm upgrade` 단계별 절차와 장애 롤백, 그리고 etcdctl snapshot 을 통한 백업 및 복구 검증을 다룹니다. |
| [모니터링 개요와 트러블슈팅 루틴 — 관찰의 세 기둥과 장애 진단 순서](operations/%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EA%B0%9C%EC%9A%94%C2%B7%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85%20%EB%A3%A8%ED%8B%B4.md) | 메트릭·로그·트레이스 관측 3요소와 kubectl 진단 명령, Pod·Node 장애 트러블슈팅 루틴을 다룹니다. |
| [노드 추가와 제거](operations/%EB%85%B8%EB%93%9C%20%EC%B6%94%EA%B0%80%C2%B7%EC%A0%9C%EA%B1%B0.md) | 부트스트랩 토큰·CA 해시·TLS 부트스트래핑으로 노드가 합류하는 과정과, drain → reset → delete 로 노드를 빼고 etcd 멤버를 정리하는 순서를 봅니다. |
| [OOMKilled 사례 — Endowus Rebalance 서비스](operations/OOMKilled%20%EC%82%AC%EB%A1%80%20%E2%80%94%20Endowus%20Rebalance%20%EC%84%9C%EB%B9%84%EC%8A%A4.md) | cgroup v1/v2 메모리 계층과 JVM 힙 밖 영역 누수로 발생한 Pod Exit Code 137 장애 사례와 원인을 분석합니다. |

### API (`api/`)

| 제목 | 한 줄 소개 |
|------|-----------|
| [API 서버 헬스 엔드포인트 — livez와 readyz는 무엇을 나눠 묻는가](api/API%20%EC%84%9C%EB%B2%84%20%ED%97%AC%EC%8A%A4%20%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8.md) | 재시작 여부와 트래픽 수용 여부를 `/livez`·`/readyz` 로 나눠 읽고, `verbose` 로 실패한 검사를 좁히며, `componentstatuses` 를 쓰지 않는 이유를 봅니다. |
| [TLS와 API 접근 보안](api/TLS%C2%B7API%20%EC%A0%91%EA%B7%BC%20%EB%B3%B4%EC%95%88.md) | 쿠버네티스 PKI 인증서 구조와 kubeconfig 인증, API 서버 접근 제어 체계를 정리하고, kubeadm 인증서의 만료 점검·갱신과 kubelet 인증서 로테이션을 봅니다. |
| [JSONPath와 kubectl 고급 조회](api/JSONPath%C2%B7kubectl%20%EA%B3%A0%EA%B8%89%20%EC%A1%B0%ED%9A%8C.md) | kubectl JSONPath 표현식과 필터 문법, 실무 조회 예시를 정리합니다. |
| [kubeconfig·여러 클러스터 접근](api/kubeconfig%C2%B7%EC%97%AC%EB%9F%AC%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%A0%91%EA%B7%BC.md) | cluster·user·context 세 블록의 참조 구조와 `--kubeconfig` → `KUBECONFIG` → `~/.kube/config` 우선순위, 여러 파일을 합칠 때 먼저 나온 값이 이기는 규칙, kubectx·kubens 가 직전 값을 남기는 자리를 실측으로 봅니다. |
| [kubectl 출력 형식 — 표는 서버가 그리고 객체는 kubectl 이 가공한다](api/kubectl%20%EC%B6%9C%EB%A0%A5%20%ED%98%95%EC%8B%9D.md) | 기본 출력과 `-o wide` 는 서버가 만든 Table 을 열 우선순위로 거른 것이고, `yaml`·`json`·`name`·`custom-columns`·`jsonpath` 는 객체를 받아 kubectl 이 가공한다는 차이를 Accept 헤더 실측으로 봅니다. |



## 아직 안 쓴 주제

> 앞으로 받을 공식 페이지입니다. 쓰는 순서는 정해 두지 않고 그때 궁금한 것부터 씁니다.

클러스터를 직접 세우면 kubernetes.io 에 없는 부품도 함께 씁니다. 그래서 하위 프로젝트(kubernetes-sigs·kubernetes-csi)도 이 목록에 둡니다. 그런 항목은 괄호에 저장소를 적었습니다.

### 아키텍처

- `Controllers`
- `Leases`
- `About cgroup v2`
- `Garbage Collection`
- `Kubernetes Self-Healing`
- `Cloud Controller Manager`

### 스케줄링·축출

- `Kubernetes Scheduler`
- `Assigning Pods to Nodes`
- `Taints and Tolerations`
- `Pod Topology Spread Constraints`
- `Pod Priority and Preemption`
- `API-initiated Eviction`

### 클러스터 운영

- `Observability`
- `Metrics For Kubernetes System Components`
- `Logging Architecture`
- `System Logs`
- `Node Shutdowns`
- `Node Autoscaling`
- `Horizontal Pod Autoscaling` — CPU 사용률로 Pod 수를 늘리고 줄이는 규칙
- `metrics-server` (kubernetes-sigs/metrics-server) — HPA·`kubectl top` 이 읽는 지표
- `Installing Kubernetes with Kubespray` (kubernetes-sigs/kubespray) — Ansible 로 설치 자동화

### 스토리지

스토리지 묶음 폴더는 아직 없습니다. 첫 편을 쓸 때 `storage/` 폴더와 「문서 목록」 표를 함께 만듭니다.

- `Container Storage Interface (CSI)` — 외부 스토리지 드라이버가 kubelet 에 붙는 규격
- `csi-driver-nfs` (kubernetes-csi/csi-driver-nfs) — NFS 서버를 StorageClass 로 동적 프로비저닝하는 드라이버

### API

- `Kubernetes API Concepts`
- `Server-Side Apply`
- `Client Libraries`
- `Kubernetes Deprecation Policy`



## 관련 문서

> 이 폴더가 딛고 서거나 이어지는 이웃입니다.

- [docs MOC](../README.md) — 제품별 폴더 규칙과 전체 문서 목록
- [08_cloud MOC](../../README.md) — 대분류 지도
- [kubernetes/](../../../_archive/08_cloud/kubernetes/README.md) — 주제별 학습 노트. 공식문서 정독과 겹치는 주제는 서로 링크로 잇습니다
- [book/](../../book/) — 책 정독 노트. 전체 개념의 뼈대는 이쪽에서 잡습니다
