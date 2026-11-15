---
title: 08_cloud/docs/kubernetes — 쿠버네티스 공식문서 정독
tags: [moc, kubernetes, official-docs]
status: final
related:
  - ../README.md
  - ../../README.md
  - ../../kubernetes/README.md
updated: 2026-11-15
---

# 08_cloud/docs/kubernetes — 쿠버네티스 공식문서 정독

---

> k8s.io 공식문서를 1차 자료로 삼아 궁금한 주제만 한 편씩 파고드는 자리입니다. 전체 개념을 순서대로 훑는 일은 [book/](../../book/)의 정독 노트와 [kubernetes/](../../kubernetes/README.md)의 주제별 노트가 맡습니다.

## 폴더 규칙

> 문서는 이 폴더 바로 아래에 두고, 묶음은 파일 번호의 장 자리로 나눕니다. 공식 문서의 목차를 폴더로 옮기지 않는 까닭은 문서 한 편이 여러 섹션을 가로질러, 폴더를 고를 때마다 고민이 생겼기 때문입니다.

| 장 | 묶음 | 다루는 것 |
|----|------|-----------|
| 01 | 아키텍처 | 노드·컨트롤러·리스처럼 클러스터가 어떻게 짜여 있는지 |
| 02 | 스케줄링·축출 | 파드를 어디에 놓고 언제 내보낼지 |
| 03 | 클러스터 운영 | 관측·로깅·etcd·인증서·업그레이드처럼 클러스터를 굴리고 손대는 일 |
| 04 | API | 헬스 엔드포인트·API 버전처럼 API 서버와 대화하는 규칙 |

파일명은 `05-file-placement.md` §5.1 의 `{장}-{절}.{제목}.md` 를 따릅니다. 같은 묶음의 새 문서는 절 번호를 올리고, 어느 묶음에도 들지 않으면 다음 장 번호를 열어 이 표에 한 줄을 더합니다.

공식 문서를 읽고 정리한 공통 개념은 이 번호를 받고, 그 개념이 실제로 드러난 사례는 `OOMKilled 사례 — Endowus Rebalance 서비스.md` 처럼 번호 없는 이름 파일로 둡니다. 사례는 개념 편과 순서를 다투지 않고, 원 글의 이름이 곧 찾는 단서이기 때문입니다.

한 묶음이 5편이 되면 그 묶음만 `03_operations/` 처럼 `NN_이름/` 폴더로 올립니다. 그 전에는 폴더를 만들지 않습니다. 5편은 `05-file-placement.md` §4.4 의 신설 기준과 같은 숫자입니다. 03 클러스터 운영 묶음은 5편(03-01~03-05)이 채워져 `03_operations/` 폴더로 승격되었고, 사례 파일도 같은 폴더에 둡니다.

공식 문서의 어느 페이지를 읽었는지는 프론트매터 `source` 가 맡습니다. 첫 줄에 1차 근거 페이지를 두면 URL 의 `concepts`·`tasks`·`reference` 갈래로 원리를 읽었는지 절차를 읽었는지가 드러납니다.

> 2026-11-12 이전에는 k8s.io 섹션 슬러그와 같은 이름의 폴더 다섯 개에 한 편씩 두었습니다. 「자원 모니터링 파이프라인」 은 출처가 모두 `tasks/debug` 와 `reference` 여서 폴더 이름과 어긋났고, 폴더마다 한 편뿐이라 평탄하게 바꿨습니다.



## 문서 목록

> 번호의 앞 두 자리가 묶음입니다. 묶음의 뜻은 위 「폴더 규칙」 표에 있습니다.

| 번호 | 제목 | 한 줄 소개 |
|------|------|-----------|
| 01-01 | [노드와 클러스터의 소속 — 겹쳐 보이는 클러스터는 어느 층에서 겹치는가](01-01.%EB%85%B8%EB%93%9C%EC%99%80%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%EC%9D%98%20%EC%86%8C%EC%86%8D%20%E2%80%94%20%EA%B2%B9%EC%B3%90%20%EB%B3%B4%EC%9D%B4%EB%8A%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%EB%8A%94%20%EC%96%B4%EB%8A%90%20%EC%B8%B5%EC%97%90%EC%84%9C%20%EA%B2%B9%EC%B9%98%EB%8A%94%EA%B0%80.md) | 노드가 클러스터에 소속되는 경로를 kubelet 자가등록으로 따라가고, 여러 클러스터가 노드를 겹쳐 쓴다는 말이 어느 층의 이야기인지 가릅니다. |
| 01-02 | [컨테이너 런타임 인터페이스·crictl](01-02.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%9F%B0%ED%83%80%EC%9E%84%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4%C2%B7crictl.md) | kubelet 이 CRI 소켓으로 containerd 를 부르는 경로를 따라가고, `crictl`·`ctr`·`nerdctl` 이 각각 무엇을 보는지와 cgroup 드라이버를 맞춰야 하는 이유를 봅니다. |
| 02-01 | [노드 압박 축출과 디스크 관리 — DiskPressure는 무엇을 보고 켜지는가](02-01.%EB%85%B8%EB%93%9C%20%EC%95%95%EB%B0%95%20%EC%B6%95%EC%B6%9C%EA%B3%BC%20%EB%94%94%EC%8A%A4%ED%81%AC%20%EA%B4%80%EB%A6%AC%20%E2%80%94%20DiskPressure%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9D%84%20%EB%B3%B4%EA%B3%A0%20%EC%BC%9C%EC%A7%80%EB%8A%94%EA%B0%80.md) | kubelet 이 자원 신호를 재고 노드 컨디션을 달고 자원을 회수한 뒤 파드를 고르는 다섯 단을 따라갑니다. 디스크 관리가 여기 붙습니다. |
| 03-01 | [자원 모니터링 파이프라인 — kubelet이 재는 것과 kubectl top이 읽는 것](03_operations/03-01.%EC%9E%90%EC%9B%90%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%20%E2%80%94%20kubelet%EC%9D%B4%20%EC%9E%AC%EB%8A%94%20%EA%B2%83%EA%B3%BC%20kubectl%20top%EC%9D%B4%20%EC%9D%BD%EB%8A%94%20%EA%B2%83.md) | `kubectl top` 의 숫자가 cAdvisor 에서 metrics-server 를 거쳐 오는 경로를 따라가고, 이 내장 파이프라인의 경계를 긋습니다. |
| 03-02 | [etcd 헬스와 유지보수 — 상태 판독과 compaction·defrag·quota](03_operations/03-02.etcd%20%ED%97%AC%EC%8A%A4%EC%99%80%20%EC%9C%A0%EC%A7%80%EB%B3%B4%EC%88%98%20%E2%80%94%20%EC%83%81%ED%83%9C%20%ED%8C%90%EB%8F%85%EA%B3%BC%20compaction%C2%B7defrag%C2%B7quota.md) | `etcdctl` 세 명령으로 멤버 상태를 읽고, compaction·defrag·quota 가 맞물려 NOSPACE 로 쓰기가 멈추는 과정과 복구 순서, snapshot 확인을 봅니다. |
| 03-03 | [클러스터 업그레이드와 ETCD 백업·복구](03_operations/03-03.%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%97%85%EA%B7%B8%EB%A0%88%EC%9D%B4%EB%93%9C%EC%99%80%20ETCD%20%EB%B0%B1%EC%97%85%C2%B7%EB%B3%B5%EA%B5%AC.md) | `kubeadm upgrade` 단계별 절차와 장애 롤백, 그리고 etcdctl snapshot 을 통한 백업 및 복구 검증을 다룹니다. |
| 03-04 | [모니터링 개요와 트러블슈팅 루틴 — 관찰의 세 기둥과 장애 진단 순서](03_operations/03-04.%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EA%B0%9C%EC%9A%94%EC%99%80%20%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85%20%EB%A3%A8%ED%8B%B4.md) | 메트릭·로그·트레이스 관측 3요소와 kubectl 진단 명령, Pod·Node 장애 트러블슈팅 루틴을 다룹니다. |
| 03-05 | [노드 추가와 제거](03_operations/03-05.%EB%85%B8%EB%93%9C%20%EC%B6%94%EA%B0%80%EC%99%80%20%EC%A0%9C%EA%B1%B0.md) | 부트스트랩 토큰·CA 해시·TLS 부트스트래핑으로 노드가 합류하는 과정과, drain → reset → delete 로 노드를 빼고 etcd 멤버를 정리하는 순서를 봅니다. |
| 사례 | [OOMKilled 사례 — Endowus Rebalance 서비스](03_operations/OOMKilled%20%EC%82%AC%EB%A1%80%20%E2%80%94%20Endowus%20Rebalance%20%EC%84%9C%EB%B9%84%EC%8A%A4.md) | cgroup v1/v2 메모리 계층과 JVM 힙 밖 영역 누수로 발생한 Pod Exit Code 137 장애 사례와 원인을 분석합니다. |
| 04-01 | [API 서버 헬스 엔드포인트 — livez와 readyz는 무엇을 나눠 묻는가](04-01.API%20%EC%84%9C%EB%B2%84%20%ED%97%AC%EC%8A%A4%20%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8%20%E2%80%94%20livez%EC%99%80%20readyz%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9D%84%20%EB%82%98%EB%88%A0%20%EB%AC%BB%EB%8A%94%EA%B0%80.md) | 재시작 여부와 트래픽 수용 여부를 `/livez`·`/readyz` 로 나눠 읽고, `verbose` 로 실패한 검사를 좁히며, `componentstatuses` 를 쓰지 않는 이유를 봅니다. |
| 04-02 | [TLS와 API 접근 보안](04-02.TLS%EC%99%80%20API%20%EC%A0%91%EA%B7%BC%20%EB%B3%B4%EC%95%88.md) | 쿠버네티스 PKI 인증서 구조와 kubeconfig 인증, API 서버 접근 제어 체계를 정리하고, kubeadm 인증서의 만료 점검·갱신과 kubelet 인증서 로테이션을 봅니다. |
| 04-03 | [JSONPath와 kubectl 고급 조회](04-03.JSONPath%EC%99%80%20kubectl%20%EA%B3%A0%EA%B8%89%20%EC%A1%B0%ED%9A%8C.md) | kubectl JSONPath 표현식과 필터 문법, 실무 조회 예시를 정리합니다. |
| 04-04 | [kubeconfig·여러 클러스터 접근](04-04.kubeconfig%C2%B7%EC%97%AC%EB%9F%AC%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%A0%91%EA%B7%BC.md) | cluster·user·context 세 블록의 참조 구조와 `--kubeconfig` → `KUBECONFIG` → `~/.kube/config` 우선순위, 여러 파일을 합칠 때 먼저 나온 값이 이기는 규칙을 실측으로 봅니다. |



## 아직 안 쓴 주제

> 앞으로 받을 공식 페이지입니다. 쓰는 순서는 정해 두지 않고 그때 궁금한 것부터 씁니다.

### 01 아키텍처

- `Controllers`
- `Leases`
- `About cgroup v2`
- `Garbage Collection`
- `Kubernetes Self-Healing`
- `Cloud Controller Manager`

### 02 스케줄링·축출

- `Kubernetes Scheduler`
- `Assigning Pods to Nodes`
- `Taints and Tolerations`
- `Pod Topology Spread Constraints`
- `Pod Priority and Preemption`
- `API-initiated Eviction`

### 03 클러스터 운영

- `Observability`
- `Metrics For Kubernetes System Components`
- `Logging Architecture`
- `System Logs`
- `Node Shutdowns`
- `Node Autoscaling`

### 04 API

- `Kubernetes API Concepts`
- `Server-Side Apply`
- `Client Libraries`
- `Kubernetes Deprecation Policy`



## 관련 문서

> 이 폴더가 딛고 서거나 이어지는 이웃입니다.

- [docs MOC](../README.md) — 제품별 폴더 규칙과 전체 문서 목록
- [08_cloud MOC](../../README.md) — 대분류 지도
- [kubernetes/](../../kubernetes/README.md) — 주제별 학습 노트. 공식문서 정독과 겹치는 주제는 서로 링크로 잇습니다
- [book/](../../book/) — 책 정독 노트. 전체 개념의 뼈대는 이쪽에서 잡습니다
