---
title: network-fundamentals-lab — 실습 인덱스
tags: [moc, study-index, lab, networking, containerlab, troubleshooting, os]
status: draft
source:
  - https://github.com/gnu-gnu/network-fundamentals-lab  # 저장소 (2026-09-13 조회)
  - ~/study/network-fundamentals-lab@c096dad  # 로컬 clone — 18편 + 체크포인트 2
related:
  - ./01-01.%EC%A3%BC%EC%86%8C%EB%A5%BC%20%EC%9D%BD%EA%B3%A0%20%EB%8F%84%EA%B5%AC%20%EC%85%8B%EC%9D%84%20%EB%93%A0%EB%8B%A4.md
  - ./02-01.%EA%B0%99%EC%9D%80%20%EC%84%B8%EA%B7%B8%EB%A8%BC%ED%8A%B8%20%EC%95%88%EC%97%90%EC%84%9C%EB%A7%8C%20%ED%86%B5%ED%95%9C%EB%8B%A4.md
  - ./03-01.%EC%84%B8%EA%B7%B8%EB%A8%BC%ED%8A%B8%EB%A5%BC%20%EB%84%98%EC%9C%BC%EB%A9%B4%20%ED%85%8C%EC%9D%B4%EB%B8%94%EC%9D%B4%20%EC%A0%84%EB%B6%80%EB%8B%A4.md
  - ./03-02.%EB%9D%BC%EC%9A%B0%ED%8A%B8%EA%B0%80%20%EC%8A%A4%EC%8A%A4%EB%A1%9C%20%EA%B1%B8%EC%96%B4%EC%98%A4%EA%B2%8C%20%ED%95%9C%EB%8B%A4.md
  - ./04-01.%EB%9D%BC%EC%9A%B0%ED%84%B0%20%EB%84%88%EB%A8%B8%EC%97%90%20%EA%B0%99%EC%9D%80%20L2%EB%A5%BC%20%EB%A7%8C%EB%93%A0%EB%8B%A4.md
  - ./05-01.%EC%97%B0%EA%B2%B0%EC%9D%80%20%EC%96%91%20%EB%81%9D%EB%A7%8C%EC%9D%98%20%EC%9D%BC%EC%9D%B4%20%EC%95%84%EB%8B%88%EB%8B%A4.md
  - ./06-01.%EC%9E%91%EC%9D%80%20%EA%B2%83%EC%9D%80%20%EB%90%98%EA%B3%A0%20%ED%81%B0%20%EA%B2%83%EB%A7%8C%20%EB%A9%8E%EB%8A%94%EB%8B%A4.md
  - ./07-01.%EA%B8%B8%EC%9D%80%20%EB%A9%80%EC%A9%A1%ED%95%9C%EB%8D%B0%20%EC%95%88%20%ED%86%B5%ED%95%A0%20%EB%95%8C.md
  - ../../README.md
  - ../../networking/README.md
  - ../cntd_computer-networking-top-down/README.md
  - ../paw_packet-analysis-wireshark/README.md
  - ../../../troubleshooting/README.md
  - ../../../roadmap/network-roadmap.md
learning:
  topic: network-fundamentals-lab
  scope: durable
  level: 기본
  last_verified:            # Phase 4 자답·_review 회차 미실시 — 작성일로 대신 채우지 않습니다
  blocked_count: 0
  next_lesson: "01-01 온램프 Phase 1 — 읽기 전 예측"
updated: 2026-09-13
---

# network-fundamentals-lab — 실습 인덱스

---

> 이 폴더는 [`gnu-gnu/network-fundamentals-lab`](https://github.com/gnu-gnu/network-fundamentals-lab) 저장소를 블록 단위로 정독하며 정리하는 **랩 저장소 기반 학습노트**입니다. 다른 `book/` 폴더가 책을 장별로 따라가는 것과 달리, 이쪽 원자료는 **고장이 장전된 채로 뜨는 containerlab 토폴로지** 18편입니다.

## 이 폴더를 여기 두는 이유

> `02_os` 안에서 `networking/` 이 패킷이 지나가는 길을 맡는다면, 이 폴더는 그 길을 **고장 내서 확인하는 쪽**을 맡습니다.

`02_os` 는 언어가 아닌 실행 환경, 곧 커널과 그 위의 자원·네트워크 메커니즘을 모으는 카테고리입니다. 그 안에서 [`networking/`](../../networking/README.md) 이 커널이 패킷을 *어떻게 나르는가*(netns·veth·netfilter·conntrack)의 SSOT 이고, 이 폴더는 같은 메커니즘을 **깨진 상태에서 출발해** 증상으로 되짚습니다. 원리 자체는 `networking/` 을 교차참조하고 여기서 다시 정의하지 않습니다.

같은 카테고리의 두 책과도 축이 갈립니다. [`cntd_computer-networking-top-down/`](../cntd_computer-networking-top-down/README.md) 은 프로토콜을 규격으로 배우는 자리입니다. [`paw_packet-analysis-wireshark/`](../paw_packet-analysis-wireshark/README.md) 는 그것을 캡처로 읽는 법을 맡습니다. 셋 다 TCP·IP·DNS·NAT 를 다룹니다. 다른 것은 출발점입니다 — **이 폴더만 "이미 망가진 상태"에서 시작합니다.** 규격을 알아도 증상에서 계층을 좁히는 일은 따로 훈련해야 하기 때문입니다.

`book/` 에 두면서도 이름을 바꾸지 않은 이유가 있습니다. 원자료가 책은 아니지만 **장별로 이어가는 외부 정본 자료**라는 점에서 운영 방식이 같습니다. 편 번호·MOC·학습 상태 채널·진도 관리가 그대로 맞아떨어져, 별도 폴더 체계를 새로 열 이유가 없었습니다. `02_os/README` 의 하위 폴더 표에서는 이 폴더만 `(랩 저장소 기반)` 으로 적어 다른 아홉 줄의 `(책 기반)` 과 갈라 둡니다.



## 저장소가 돌아가는 방식

> 배포하면 이미 깨진 상태로 뜨고, 그것을 진단해 한 줄로 고치는 구조입니다. "고장이 기본값"이라는 말이 이 저장소의 설계 전체를 요약합니다.

편 하나는 폴더 하나이고 그 안에 파일이 넷 있습니다.

- `NN-topic.clab.yml`: containerlab 토폴로지. 고장이 미리 장전돼 있습니다
- `README.md`: 실습 지시서. 개념 한 장 → 토폴로지 → 재현 → 관찰 → 원인 → 한 줄 수정 → 교훈 일곱 단계
- `fix.sh`: 한 줄 수정 스크립트
- `WALKTHROUGH.md`: 모범 답안. 저자가 실제로 실행한 기록을 의도 → 실측 결과 → 해석 세 단으로 적었습니다

저자가 권하는 순서는 **README 만 보고 스스로 해보다가, 막히거나 끝낸 뒤에 WALKTHROUGH 와 대조**하는 것입니다. 처음부터 답안을 펴면 진단 근육이 안 붙는다고 저장소가 직접 못 박아 두었습니다.

손은 이렇게 움직입니다.

```bash
./clab.sh deploy 09-conntrack/09-conntrack.clab.yml     # 고장난 채로 뜹니다
docker exec clab-09-conntrack-nat conntrack -L          # 노드 안에서 진단
docker exec clab-09-conntrack-nat sysctl -w net.netfilter.nf_conntrack_tcp_timeout_established=3600
./clab.sh destroy 09-conntrack/09-conntrack.clab.yml
```

체크포인트 둘은 README 를 주지 않습니다. `MISSION.md` 의 증상만 보고 풀고, 다 푼 뒤 `SOLUTION.md` 로 대조합니다. CP-1 은 04·05 를 섞은 이중 고장입니다. CP-2 는 08~11 을 섞어 타임아웃·RST·소스 불일치를 가르게 합니다.



## 블록 구조 — 저자의 18편과 노트 8편

> 저자가 이미 일곱 블록으로 묶어 두었고, 노트는 그 묶음을 그대로 따릅니다. 편을 1:1 로 옮기지 않은 이유는 한 블록의 편들이 같은 원리의 다른 얼굴이기 때문입니다.

저자는 18편을 L2 → L3 → 오버레이 → Transport·상태 → MTU → 이름·진단면 → 심화 순으로 쌓아 두었고, `[코어]` 10편과 `[확장]` 8편으로 트랙도 갈라 놓았습니다. 코어 트랙만 따르면 `01 → 02 → 04 → 05 → 08 → 09 → 10 → 11 → 12 → 14` 입니다.

노트가 블록을 단위로 삼는 이유는 편 사이의 의존이 블록 안에서 닫히기 때문입니다. 11편은 08·09·10 을 합성한다고 저자가 명시했고, 13편은 07 과 12 를 이어받습니다. 이 관계를 편마다 끊으면 같은 설명을 세 번 반복하게 됩니다.

| 노트 | 원자료 | 블록 |
|---|---|---|
| `01-01` | 00 | 온램프 |
| `02-01` | 01·02·03 | L2 — 같은 세그먼트 |
| `03-01` | 04·05·06 | L3 — 세그먼트를 넘어 |
| `03-02` | 17 | 심화 — 동적 라우팅 |
| `04-01` | 07 | 오버레이 — L3 위의 L2 |
| `05-01` | 08·09·10·11 | Transport·상태 |
| `06-01` | 12·13 | 경로와 MTU |
| `07-01` | 14·15·16 | 이름과 진단면 |

17장(동적 라우팅)만 블록에서 떼어 `03-02` 로 옮겼습니다. 저자는 심화 블록에 따로 두었지만 내용은 04·05 의 라우팅 테이블을 정적에서 동적으로 확장한 것이라, L3 장 아래 두어야 "라우트가 어떻게 생기는가"라는 한 질문으로 읽힙니다. 저자 자신도 17장 정리에서 "04장의 원리는 죽지 않는다"고 적었습니다.



## 장별 목표 (18장)

> 저자가 각 편 `## 0. 학습 목표` 절에 적어 둔 문구를 옮긴 것입니다. 추측으로 채운 칸은 없습니다.

`01~17` 은 각 편 README 의 학습 목표 절이 원문입니다. `00-onramp` 만 그 절이 없어 저장소 루트 README 의 목차 항목과 편 도입부에서 가져왔고, 이 표에서 유일하게 출처가 다른 행입니다.

| 장 | 제목 | 트랙 | 이 장이 가르치는 것 | 장전된 고장 |
|---|---|:---:|---|---|
| 00 | 온램프 | 선택 | CIDR 표기를 읽고, L2/L3 계층 감각을 잡고, `ip`·`ping`·`tcpdump` 세 도구에 손을 익힙니다 | 없음 — 이 시리즈의 유일한 고장 없는 장 |
| 01 | L2 인접성과 ARP | 코어 | MAC과 IP가 왜 둘 다 필요한지, "같은 네트워크"가 무엇을 뜻하는지, 서브넷 마스크가 직접 통신과 라우터 경유를 어떻게 가르는지 | 서브넷 불일치 · 중복 IP(ARP 충돌) |
| 02 | 브로드캐스트 도메인과 L2 루프 | 코어 | 스위치의 MAC 학습(FDB/CAM), unknown unicast 플러딩, 루프가 브로드캐스트 한 발을 스톰으로 키우는 과정, STP가 끊는 자리 | 브리지 둘을 링크 둘로 연결 |
| 03 | VLAN과 트렁크 | 확장 | VLAN이 논리적 브로드캐스트 도메인이라는 것, 액세스(untagged)와 트렁크(tagged)의 차이, 802.1Q 태그를 눈으로 보기 | 트렁크 VID 허용 누락 (양단 비대칭) |
| 04 | L3 라우팅과 기본 게이트웨이 | 코어 | 목적지 기반 포워딩, `ip route get`·`traceroute`로 어디서 멎는지 찾기, ICMP echo와 destination unreachable | 리턴 라우트 누락 · `ip_forward=0` · 기본 게이트웨이 누락 |
| 05 | LPM과 블랙홀 | 코어 | `/32 > /24 > /16 > default` 우선순위, blackhole(조용한 소실)과 unreachable(즉시 에러)의 증상 차이 | `h2/32`를 블랙홀로 |
| 06 | TTL과 라우팅 루프 | 확장 | 홉마다 −1과 ICMP time-exceeded, 상호 디폴트가 만드는 루프, traceroute가 사실 TTL을 이용한 장치라는 것 | r1↔r2 상호 디폴트 |
| 07 | VXLAN 기초 | 확장 | 이더넷 프레임이 UDP/IP(4789)에 실려 라우팅되는 것, VTEP와 VNI(24bit), 오버레이의 50바이트 세금 | VNI 불일치 · VTEP `remote`/FDB 누락 |
| 08 | TCP 3-way 실패 유형 | 코어 | 정상 핸드셰이크 읽기, 타임아웃·refused·중간자 RST 세 지문, RST의 TTL로 발신자 가리기 | 세 상황을 하나씩 주입 |
| 09 | conntrack과 포트·idle timeout | 코어 | 상태 테이블의 원방향·응답방향 튜플과 남은 수명, idle timeout, SNAT 포트 고갈, `conntrack -L`/`-S` | established timeout 30초 · SNAT 포트 2개 · INVALID DROP |
| 10 | NAT 기본 | 코어 | 인터넷이 사설 대역으로 돌아올 길을 모른다는 것, SNAT(egress)와 DNAT(포트 공개)의 방향, 왕복 역번역 | DNAT만 하고 리턴 라우트 없음 |
| 11 | 대칭성과 NAT 소스 재작성 | 코어 | 경로 비대칭이 헤더 재작성·상태 장비와 만날 때, "SYN-ACK가 내가 붙은 IP가 아닌 곳에서 온다"는 지문, 다지점 캡처 | 리턴 경로가 NAT를 경유하도록 라우팅 |
| 12 | MTU·MSS·PMTUD | 코어 | MSS 협상이 양 끝 MTU만 반영한다는 것, PMTUD가 중간 협곡을 ICMP로 찾는 방식, ICMP 허용(근본)과 MSS clamp(응급)의 차이 | 중간 링크 MTU 축소 + ICMP frag-needed 차단 |
| 13 | 터널·오버레이 MTU | 확장 | 커널이 로컬 underlay −50을 자동 계산하고 초과 설정을 EINVAL로 거부한다는 것, 그 방어가 경로 중간까지는 못 미친다는 것 | 경로 중간의 더 좁은 underlay |
| 14 | DNS 기본 | 코어 | `/etc/resolv.conf` → 리졸버 → 권한 서버 경로, TTL이 곧 페일오버 소요 시간이라는 것, `dig`로 계층을 분리해 질의하기 | 캐시·TTL로 페일오버 안 먹음 · 다중 A에 죽은 주소 |
| 15 | ICMP 차단의 대가 | 확장 | ping 실패가 서비스 다운이 아니라는 것, 전면 차단이 생존 확인·traceroute·PMTUD를 함께 부순다는 것 | ICMP 전면 차단 |
| 16 | NAT 헤어핀 | 확장 | 내부에서 자기 공인 IP로 꺾이는 경로, DNAT만으로 부족한 이유, "SYN-ACK가 주소도 포트도 다른 곳에서" | 헤어핀 실패 (내부에서 자기 공인 IP만 타임아웃) |
| 17 | 동적 라우팅 (OSPF/BGP) | 확장 | 이웃 → 광고 → 수신 → 설치 사다리, OSPF 인접의 조건부 성립, BGP에서 Established가 성공 지표가 아니라는 것 | OSPF area 불일치 · BGP `network` 문 누락 |



## 작성된 정독 노트

> 블록 하나가 노트 한 편입니다. 상태 칸은 Phase 2 를 마친 시점에 갱신합니다.

| 노트 | 원자료 | 다루는 것 | 상태 |
|---|---|---|---|
| [주소를 읽고 도구 셋을 든다](./01-01.%EC%A3%BC%EC%86%8C%EB%A5%BC%20%EC%9D%BD%EA%B3%A0%20%EB%8F%84%EA%B5%AC%20%EC%85%8B%EC%9D%84%20%EB%93%A0%EB%8B%A4.md) | `00` | CIDR 표기·L2/L3 계층 감각·`ip`/`ping`/`tcpdump` | 초안 |
| [같은 세그먼트 안에서만 통한다](./02-01.%EA%B0%99%EC%9D%80%20%EC%84%B8%EA%B7%B8%EB%A8%BC%ED%8A%B8%20%EC%95%88%EC%97%90%EC%84%9C%EB%A7%8C%20%ED%86%B5%ED%95%9C%EB%8B%A4.md) | `01·02·03` | ARP·MAC 학습과 루프 스톰·VLAN 트렁크 | 초안 |
| [세그먼트를 넘으면 테이블이 전부다](./03-01.%EC%84%B8%EA%B7%B8%EB%A8%BC%ED%8A%B8%EB%A5%BC%20%EB%84%98%EC%9C%BC%EB%A9%B4%20%ED%85%8C%EC%9D%B4%EB%B8%94%EC%9D%B4%20%EC%A0%84%EB%B6%80%EB%8B%A4.md) | `04·05·06` | 라우팅 테이블과 왕복·LPM 블랙홀·TTL | 초안 |
| [라우트가 스스로 걸어오게 한다](./03-02.%EB%9D%BC%EC%9A%B0%ED%8A%B8%EA%B0%80%20%EC%8A%A4%EC%8A%A4%EB%A1%9C%20%EA%B1%B8%EC%96%B4%EC%98%A4%EA%B2%8C%20%ED%95%9C%EB%8B%A4.md) | `17` | OSPF 인접·BGP 광고·추적 사다리 | 초안 |
| [라우터 너머에 같은 L2를 만든다](./04-01.%EB%9D%BC%EC%9A%B0%ED%84%B0%20%EB%84%88%EB%A8%B8%EC%97%90%20%EA%B0%99%EC%9D%80%20L2%EB%A5%BC%20%EB%A7%8C%EB%93%A0%EB%8B%A4.md) | `07` | VXLAN 캡슐화·VTEP·VNI | 초안 |
| [연결은 양 끝만의 일이 아니다](./05-01.%EC%97%B0%EA%B2%B0%EC%9D%80%20%EC%96%91%20%EB%81%9D%EB%A7%8C%EC%9D%98%20%EC%9D%BC%EC%9D%B4%20%EC%95%84%EB%8B%88%EB%8B%A4.md) | `08·09·10·11` | 3-way 실패 지문·conntrack·NAT·경로 비대칭 | 초안 |
| [작은 것은 되고 큰 것만 멎는다](./06-01.%EC%9E%91%EC%9D%80%20%EA%B2%83%EC%9D%80%20%EB%90%98%EA%B3%A0%20%ED%81%B0%20%EA%B2%83%EB%A7%8C%20%EB%A9%8E%EB%8A%94%EB%8B%A4.md) | `12·13` | MTU·MSS·PMTUD·터널 50바이트 | 초안 |
| [길은 멀쩡한데 안 통할 때](./07-01.%EA%B8%B8%EC%9D%80%20%EB%A9%80%EC%A9%A1%ED%95%9C%EB%8D%B0%20%EC%95%88%20%ED%86%B5%ED%95%A0%20%EB%95%8C.md) | `14·15·16` | DNS TTL·ICMP 차단·NAT 헤어핀 | 초안 |



## 학습 상태

> 부팅 의례가 읽는 칸입니다. 프론트매터 `learning:` 이 값을 갖고, 이 표가 그 값의 근거를 갖습니다.

| 항목 | 값 | 근거 |
|---|---|---|
| 난이도 레벨 | 기본 | `02_os/networking/` 4편과 `cntd` 정독으로 L2~L4 어휘는 이미 있습니다. 처음 보는 것은 개념이 아니라 containerlab 조작과 증상 판별입니다 |
| 막힌 지점 | 없음 | Phase 1 미실시. 노트 8편은 자료 추출로 먼저 세웠습니다 |
| 최근 검증 결과 | 없음 | Phase 4 자답 회차 미실시. `last_verified` 를 작성일로 대신 채우지 않았습니다 |
| 복습 회차 | 없음 | `_review/_queue.md` 등록은 Phase 4 이후입니다 |
| 다음 레슨 후보 | `01-01` 온램프 Phase 1 | 블록 순서가 곧 의존 순서입니다. 온램프는 고장편이 아니라 예측할 것이 적어 형식을 잡는 데 적합합니다 |



## 이 맥에서의 제약

> 저장소가 전제한 실행 환경과 이 맥이 다릅니다. 아직 한 편도 돌려 보지 않았으므로, 아래는 **확인한 사실**이고 해법은 첫 실습에서 검증합니다.

`clab.sh` 는 containerlab 을 컨테이너로 띄워 `--privileged --network host --pid host` 로 호스트 네임스페이스를 빌리는 래퍼입니다. 저장소는 macOS + Docker Desktop 에서 검증했다고 적어 두었는데, 이 맥은 Docker Desktop 을 제거하고 OrbStack 만 남긴 상태입니다.

- **소켓 경로**: `clab.sh` 가 `/var/run/docker.sock` 을 마운트하는데 이 맥에는 그 경로가 없습니다. OrbStack 소켓은 `~/.orbstack/run/docker.sock` 입니다. 저장소를 고치는 대신 링크를 걸지, 마운트 경로를 바꿀지는 첫 배포 때 정합니다
- **arm64**: 17장 FRR 공식 이미지가 amd64 전용이라 저장소 스스로 "qemu 에뮬레이션으로 돌며 수렴이 느릴 수 있다"고 경고합니다. 수십 초 대기 후 재확인하는 습관이 필요합니다
- **호스트당 랩 하나**: 컨테이너 이름과 관리망이 고정이라 동시 실습이 안 됩니다. 한 편을 `destroy` 한 뒤 다음 편을 띄웁니다
- **02장 안전 수칙**: 브로드캐스트 스톰은 컨테이너 안에 갇히지만 CPU 를 폭식합니다. 탈출 명령을 미리 띄워 놓고 관찰은 수 초 안에 끝냅니다



## 이 폴더가 맡지 않는 것

> 겹치는 주제가 많아 경계를 적어 둡니다. 이것이 없으면 같은 내용이 네 곳에 흩어집니다.

- **메커니즘의 원리**: netns·veth·netfilter·conntrack 자체는 [`02_os/networking/`](../../networking/README.md) 이 SSOT 입니다. 이 폴더는 그 메커니즘이 깨졌을 때의 증상을 맡습니다
- **프로토콜 규격**: TCP 혼잡 제어, DNS 레코드 종류 같은 규격은 [`cntd`](../cntd_computer-networking-top-down/README.md) 가, 캡처 필터와 프로토콜 해독은 [`paw`](../paw_packet-analysis-wireshark/README.md) 가 맡습니다
- **체크포인트 CP-1·CP-2**: 노트로 만들지 않습니다. 증상만 보고 푸는 것이라 답을 적는 순간 문항이 죽습니다. 풀고 나면 [`troubleshooting/`](../../../troubleshooting/README.md) 의 드릴 규약대로 `{계층}/YYYY-MM-DD_증상.md` 로 승격합니다
- **실습 절차의 전재**: 저장소 README 가 지시서이고 이 노트는 개념 축입니다. 명령은 관전 포인트에 필요한 것만 옮깁니다



## 이 폴더의 작성 규약

> 다른 `book/` 폴더와 한 가지가 다릅니다. 도식 밀도를 낮춰 잡았고, 그 이유를 남겨 둡니다.

정독 노트는 흐름이 있는 `###` 마다 도식 한 장을 두는 것이 기준이고 최근 폴더들은 편당 여섯 장 안팎입니다. 이 폴더는 **편당 한두 장**으로 낮춥니다. 원자료가 실습 지시서라 노트의 무게중심이 설명이 아니라 "무엇을 보고 무엇을 판단하는가"에 있고, 토폴로지와 패킷 경로처럼 그릴 형태가 분명한 자리에만 두는 편이 맞기 때문입니다. 형태가 없는 절은 비워 둡니다.

각 편 끝에는 `## 실습 메모` 절을 둡니다. 배포 명령, 봐야 할 지점, 실측을 채울 자리, 막힌 지점이 들어갑니다. **저자의 실측값은 옮기지 않았습니다.** 저자는 2026-07-12 에 macOS + Docker Desktop 에서 쟀고 이 맥은 OrbStack + arm64 라, 포트 번호나 타임라인이 달라질 수 있습니다. 남의 측정을 내 실측처럼 적지 않으려는 것이고, 그 칸은 Phase 3 에서 직접 재서 채웁니다.



## 출처와 톤

> 원자료는 저장소이고, 노트는 합니다체입니다.

원자료는 `gnu-gnu/network-fundamentals-lab` 저장소이며 로컬 clone 의 기준 커밋은 `c096dad` 입니다. 편마다 `README.md` 를 1차 자료로 삼고, `WALKTHROUGH.md` 는 관찰 지점을 확인하는 용도로만 참조합니다. 저장소 밖에서 보강한 내용은 그 자리에 보강임을 밝히고 공식 1차 링크를 각주로 답니다.

원문의 오류를 조용히 고치지 않습니다. 오탈자나 모순 서술을 발견하면 `> **원문 정오**: …` 인용 블록으로 병기해, 저장소를 다시 열었을 때 혼동하지 않게 합니다.
