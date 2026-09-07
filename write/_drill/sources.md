---
title: 트러블슈팅 드릴 출제 소스
tags: [drill, troubleshooting, sources, network]
status: draft
source:
  - experience
related:
  - ./README.md
  - ../02_os/troubleshooting/README.md
  - ../08_cloud/troubleshooting/README.md
updated: 2026-09-07
---

# 트러블슈팅 드릴 출제 소스

---

> 문항을 미리 적어 두지 않습니다. 매 회차마다 여기 적힌 소스에서 그날 것을 새로 뽑습니다.

## 왜 문제 목록을 두지 않는가

> 문항 41개를 표로 만들어 봤다가 걷어냈습니다. 세 가지가 걸렸습니다.

목록의 증상 한 줄이 이미 그날 문제를 알려줍니다. 진행 상태를 확인하러 표를 여는 순간 다음에 나올 것이 눈에 들어오고, 능동 회상은 그 지점에서 무너집니다.

미리 채운 근거는 확인 없이 굳습니다. 실제로 그랬습니다. 41행의 근거를 문서 제목만 보고 채웠는데, 두 건이 어긋나 있었습니다. `nk/01-02` 는 keepalive 를 다루지 않았고 `single-request` 는 `write/` 전체에 0건이었습니다. 매 회차에 뽑으면 그때 근거를 확인하므로 틀린 매핑이 쌓이지 않습니다.

소스만 두면 자료가 자동으로 따라옵니다. 노트를 새로 쓰면 그 주제가 바로 출제 범위에 들어오고, 외부 사이트에 새 시나리오가 올라오면 그것도 후보가 됩니다. 목록을 두면 목록을 갱신해야 합니다.



## 출제 순서

> 아래 순서로 후보를 찾고, 앞 단계에서 뽑히면 뒷 단계로 가지 않습니다.

1. **내 노트**: 아래 커버리지 맵에서 계층을 고르고, 그 폴더의 노트를 열어 장애로 드러날 지점을 찾습니다. 근거가 확실하므로 1순위입니다.
2. **사례집 예비 풀**: 리눅스 41건과 쿠버네티스 38건입니다. 이미 해설을 읽은 사례라 회상 난이도는 낮지만 복습 효과가 있습니다.
3. **외부 사이트**: 아래 목록에서 주제만 가져오고 증상은 내 어휘로 다시 씁니다. 문제 본문을 복제하지 않습니다.

뽑을 때 지키는 것이 셋 있습니다.

- 한 회차의 문항을 한 계층에 몰지 않습니다.
- 출제 전에 그 노트에 내용이 실제로 있는지 확인합니다. 제목이 맞아 보여도 본문이 다른 것을 다루는 경우가 있었습니다.
- 이미 낸 것은 아래 출제 이력에서 확인해 거릅니다. 점수 2 이하로 재출제 대기인 것은 예외입니다.



## 커버리지 맵

> 무엇을 배웠는지를 주제 단위로 적습니다. 증상이 아니라 주제라 미리 읽어도 문제가 새지 않습니다.

### A. 리눅스 호스트

| 배운 주제 | 근거 폴더 | 편수 |
|----------|----------|------|
| 라우팅, DNS 해석, 서브네팅, netfilter 와 conntrack | [02_os/networking/](../02_os/networking/) | 4 |
| namespace, cgroup, OverlayFS, 컨테이너 격리 | [02_os/kernel/](../02_os/kernel/) | 7 |
| 디스크, 프로세스, 서비스 기동, 로그, 포트와 소켓 | [02_os/troubleshooting/](../02_os/troubleshooting/) | 13 |
| 셸, 파일 추상화, systemd, 관측, 네트워킹 기초 | [02_os/book/learning-modern-linux/](../02_os/book/learning-modern-linux/) | 17 |
| TCP 와 TLS, IP 와 라우팅, 커널 패킷 처리, 진단 도구 | [08_cloud/book/networking-and-kubernetes/](../08_cloud/book/networking-and-kubernetes/) 1~2장 | 9 |
| 전송 계층 이론, 큐잉, 이름 해석 | [02_os/book/cntd_computer-networking-top-down/](../02_os/book/cntd_computer-networking-top-down/) | 다수 |

### B. 쿠버네티스 클러스터 내부

| 배운 주제 | 근거 폴더 | 편수 |
|----------|----------|------|
| Pod 네트워크, 오버레이, Service, DNS, Ingress, NetworkPolicy, 이중 스택, 토폴로지 라우팅 | [08_cloud/kubernetes/04_networking/](../08_cloud/kubernetes/04_networking/) | 10 |
| 이미지 풀, 자원 한계, 설정 주입, 배치, 볼륨, 권한, CRD, 관측 | [08_cloud/troubleshooting/](../08_cloud/troubleshooting/) | 12 |
| 컨테이너 네트워킹, CNI, kube-proxy, EndpointSlice, Service 5유형 | [08_cloud/book/networking-and-kubernetes/](../08_cloud/book/networking-and-kubernetes/) 3~5장 | 11 |
| 워크로드와 운영 전반 | [08_cloud/book/kubernetes-in-action/](../08_cloud/book/kubernetes-in-action/) | 진행 중 |

### C. 서비스 메시

| 배운 주제 | 근거 폴더 | 편수 |
|----------|----------|------|
| Envoy, 게이트웨이와 라우팅, 트래픽 제어, 복원력, 관측, mTLS, 인증과 인가, 컨트롤 플레인 성능, 확장 | [08_cloud/book/istio-in-action/](../08_cloud/book/istio-in-action/) | 14 |
| 설치 프로파일, 사이드카 구성, 신원 규격, 포트와 디버그 엔드포인트 | 같은 폴더 부록 | 4 |

### D. 클라우드 네트워킹

| 배운 주제 | 근거 폴더 | 편수 |
|----------|----------|------|
| VPC 부품, 보안 그룹과 NACL, NAT 와 IGW 와 ELB, EKS 두 VPC, 노드당 Pod 수와 ENI 한도, VPC CNI, ALB ingress | [08_cloud/book/networking-and-kubernetes/](../08_cloud/book/networking-and-kubernetes/) 06-01 | 1 |
| GCP 글로벌 네트워크, GKE 와 NEG, Azure 라우트, AKS, 3사 비교 | 같은 폴더 06-02 | 1 |
| 존 간 트래픽과 토폴로지 인지 라우팅 | [08_cloud/kubernetes/04_networking/](../08_cloud/kubernetes/04_networking/) 04-09 | 1 |

D 계층은 근거가 셋뿐입니다. 여기서 뽑을 때는 위 세 편이 실제로 덮는 범위 안인지 먼저 확인하고, 벗어나면 다른 계층으로 돌립니다. 노트에 없는 주제로는 출제하지 않습니다.

덮이지 않는 것을 알아 두면 헛출제를 줄일 수 있습니다. NAT 게이트웨이 포트 고갈, PrivateLink 와 프라이빗 DNS, Direct Connect 의 BGP 플랩, 로드밸런서 뒤의 클라이언트 주소 보존, 멀티 클라우드 자격 증명 연합, 게이트웨이 로드밸런서의 비대칭 경로가 그렇습니다. 이 주제로 문제를 풀고 싶으면 노트를 먼저 씁니다.



## 출제 이력

> 중복을 거르고 진행을 추적합니다. 이미 낸 것이므로 여기 적힌 내용은 스포일러가 아닙니다.

| 날짜 | 문항 | 계층 | 점수 | 재출제 |
|------|------|------|------|--------|
| 2026-09-07 | 실패율 0.3%가 사라지지 않는 서버 | A | 2 | 2026-09-10 |
| 2026-09-07 | Pod 로는 되고 이름으로는 안 되는 호출 | B | 3 | |
| 2026-09-07 | 트래픽이 늘 때만 섞여 나오는 503 | C | 3 | |



## 약한 영역

> [오답 노트](./_mistakes.md) 에서 같은 원인이 두 번 이상 나온 주제입니다. 다음 출제에서 가중치를 둡니다.

**확인 방법**. 2026-09-07 세 문항 모두 가설과 처방은 세웠으나 "어디를 보면 갈리는지"에서 멈췄습니다. 다음 회차는 계층별 진단 명령을 요구하는 문항에 가중치를 둡니다.



## 외부 사이트

> 사이트 목록의 정본은 [OS 사례집 README](../02_os/troubleshooting/README.md) 의 연습 사이트 절입니다. 성격이 셋으로 갈립니다.

- **정적 문제**: Infratice — 환경 없이 로그와 설정만 읽습니다. 사례집이 41건을 편입했고 나머지가 바로 후보입니다
- **대화형 셸**: SadServers, iximiuz Labs, Killercoda, Killer Shell — 실제 서버를 주므로 주말 실습을 대체할 수 있습니다
- **학습 과정**: LFWS313, DevOps-Learn-By-Doing — 커리큘럼과 큐레이션입니다

외부에서 가져올 때는 주제와 링크만 옮깁니다. 증상 서술은 제 노트의 어휘로 다시 쓰고, 출처는 그 회차 파일의 `source` 에 남깁니다.



## 관련 문서

- [드릴 진입점](./README.md) — 루틴, 문항 포맷, 채점 규약
- [오답 노트](./_mistakes.md) — 막힌 지점의 누적 기록
- [OS 트러블슈팅 사례집](../02_os/troubleshooting/README.md) — A 계층 예비 풀과 연습 사이트 목록의 출처
- [Kubernetes 트러블슈팅 사례집](../08_cloud/troubleshooting/README.md) — B 계층 예비 풀
