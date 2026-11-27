---
title: 사이드카 트래픽 가로채기·iptables 체인 — 인바운드 15006·아웃바운드 15001·예외 규칙
tags: [istio, sidecar, iptables, traffic-interception, envoy, cni]
status: draft
source:
  - https://istio.io/v1.32/docs/ops/deployment/application-requirements/
  - https://istio.io/v1.32/docs/ops/configuration/traffic-management/traffic-routing/
  - https://istio.io/v1.32/docs/setup/additional-setup/cni/
  - https://istio.io/v1.32/docs/setup/install/virtual-machine/
  - https://github.com/istio/istio/blob/1.32.0/tools/istio-iptables/pkg/capture/run.go
  - https://github.com/istio/istio/blob/1.32.0/tools/istio-iptables/pkg/constants/constants.go
  - https://github.com/istio/istio/blob/1.32.0/manifests/charts/istio-control/istio-discovery/files/injection-template.yaml
related:
  - ./README.md
  - ./사이드카 시동·종료 순서.md
  - ../../book/istio-in-action/a0-02.부록 — 사이드카를 이루는 넷과 VM 이 받는 다섯 파일.md
  - ../../book/istio-in-action/a0-04.부록 — 포트 열넷과 디버그 엔드포인트 지도.md
  - ../../book/networking-and-kubernetes/02-03.iptables·IPVS·eBPF — kube-proxy를 이해하는 세 기술.md
updated: "2026-11-27"
---

# 사이드카 트래픽 가로채기·iptables 체인 — 인바운드 15006·아웃바운드 15001·예외 규칙

---

> Istio 사이드카는 파드 네트워크 네임스페이스 안에 `nat` 테이블 `iptables` 규칙을 세워 인바운드 트래픽을 `15006`, 아웃바운드 트래픽을 `15001` Envoy 리스너로 투명하게 돌립니다. 동시에 UID 1337, 루프백, `127.0.0.6`, 관리 포트를 먼저 `RETURN` 으로 빼야 무한 루프와 헬스 체크 차단을 막습니다.

근거는 Istio 1.32 공식 문서와 `1.32.0` 태그의 `tools/istio-iptables` 및 주입 템플릿 소스입니다. 규칙과 순서는 Go 소스와 골든 테스트 출력을 대조해 정리했으며, 실제 클러스터에서 실행해 검증하지는 않았습니다.

`iptables` 테이블과 훅의 기초는 [02-03 노트](../../book/networking-and-kubernetes/02-03.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md)가 다룹니다. `istio-init` 의 특권 요구와 Istio CNI 전환 배경은 [부록 B §4](../../book/istio-in-action/a0-02.부록%20%E2%80%94%20%EC%82%AC%EC%9D%B4%EB%93%9C%EC%B9%B4%EB%A5%BC%20%EC%9D%B4%EB%A3%A8%EB%8A%94%20%EB%84%B7%EA%B3%BC%20VM%20%EC%9D%B4%20%EB%B0%9B%EB%8A%94%20%EB%8B%A4%EC%84%AF%20%ED%8C%8C%EC%9D%BC.md#4-istio-init-특권과-cni-플러그인)가, 사이드카 포트 열넷의 역할은 [부록 D](../../book/istio-in-action/a0-04.부록%20%E2%80%94%20%ED%8F%AC%ED%8A%B8%20%EC%97%B4%EB%84%B7%EA%B3%BC%20%EB%94%94%EB%B2%84%EA%B7%B8%20%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8%20%EC%A7%80%EB%8F%84.md)가 맡습니다.

## 1. 앱 수정 없는 투명 가로채기

> 앱 코드는 서비스 이름과 애플리케이션 포트만 호출하는데도, 파드 안의 모든 TCP 트래픽이 Envoy 프록시를 거치지 않으면 mTLS 와 L7 라우팅이 동작하지 않습니다.

애플리케이션 컨테이너는 `http://api-service:8080` 같은 서비스 DNS 이름이나 포트 `8080` 으로만 요청을 주고받습니다. 앱에 프록시 주소를 하드코딩하지 않고도 트래픽을 모두 프록시로 보내지 못하면, 상호 TLS(mTLS) 암호화와 라우팅 정책을 인프라 계층에 둘 수 없습니다. 반대로 모든 패킷을 무조건 Envoy 로 돌리면, Envoy 자신이 내보낸 패킷까지 다시 Envoy 로 빨려 들어가 무한 루프에 빠집니다.

Istio 는 파드의 네트워크 네임스페이스 안에 **투명 가로채기**(transparent interception) 규칙을 세워 이 문제를 풉니다. 네트워크 네임스페이스는 리눅스 커널이 네트워크 인터페이스와 라우팅 표를 격리하는 단위입니다. 커널의 `iptables` 가 목적지 포트를 프록시 리스너로 바꿔치기하므로 앱은 프록시 존재를 알 필요가 없습니다.[^run-go]

### 규칙을 심는 두 주체와 공통 코드

파드가 뜰 때 `iptables` 규칙을 세우는 주체는 `istio-init` 초기화 컨테이너 또는 노드 수준 데몬셋인 Istio CNI 플러그인입니다. 어느 쪽을 쓰든 `sidecar_iptables_linux.go` 가 `ProgramIptables` 를 호출하므로 생성되는 체인과 규칙 구조는 같습니다.[^cni-ipt][^app-req] 권한 분리와 CNI 도입 배경은 [부록 B §4](../../book/istio-in-action/a0-02.부록%20%E2%80%94%20%EC%82%AC%EC%9D%B4%EB%93%9C%EC%B9%B4%EB%A5%BC%20%EC%9D%B4%EB%A3%A8%EB%8A%94%20%EB%84%B7%EA%B3%BC%20VM%20%EC%9D%B4%20%EB%B0%9B%EB%8A%94%20%EB%8B%A4%EC%84%AF%20%ED%8C%8C%EC%9D%BC.md#4-istio-init-특권과-cni-플러그인)에서 다룹니다.



## 2. 인바운드 경로와 제외 포트

> 파드로 들어오는 모든 TCP 연결을 가로채되, HBONE 터널과 헬스 체크·메트릭 포트는 제외하지 않으면 상태 점검과 프로메테우스 수집이 막힙니다.

외부에서 파드의 애플리케이션 포트로 들어오는 패킷이 앱 소켓에 바로 닿으면, Envoy 가 mTLS 를 종단하거나 인가 정책을 검사할 수 없습니다. 반대로 파드의 준비 상태를 확인하는 kubelet 프로브나 메트릭 스크랩 요청까지 Envoy 인바운드 리스너로 돌리면 관리 트래픽이 꼬입니다.

기본 `REDIRECT` 모드에서는 `nat` 테이블의 `PREROUTING` 훅이 이 분기를 맡습니다. `istio-iptables` 는 사용자 체인 두 개를 만들어 들어오는 TCP 패킷을 포트 `15006` 으로 넘깁니다.[^run-go][^config-go]

```markdown
PREROUTING (nat)
  └─ -p tcp -j ISTIO_INBOUND
       ├─ --dport 15008 -j RETURN        (HBONE 터널 포트 제외)
       ├─ --dport 15090 -j RETURN        (Envoy 메트릭 포트 제외)
       ├─ --dport 15021 -j RETURN        (헬스 체크 포트 제외)
       ├─ --dport 15020 -j RETURN        (병합 메트릭·상태 포트 제외)
       └─ -p tcp -j ISTIO_IN_REDIRECT
            └─ -p tcp -j REDIRECT --to-ports 15006
```

### 인바운드 체인의 포트 제외 기준

`PREROUTING` 은 모든 TCP 패킷을 `ISTIO_INBOUND` 체인으로 보냅니다. 여기서 **제외 포트**가 먼저 `RETURN` 으로 빠져나갑니다.

- `15008` 포트: HBONE 터널 전용 포트라서 `Run()` 함수가 항상 `RETURN` 규칙을 맨 앞에 넣습니다.[^run-go] HBONE 은 HTTP-Based Overlay Network Environment 의 약자입니다.
- `15090`·`15021`·`15020` 포트: 사이드카 주입 템플릿이 기본 `InboundPortsExclude` 인자로 넘기는 관리 포트들입니다.[^inj-tmpl]
- 내부 전용 포트: `15000`(관리)과 `15002`(장애 감지), `15004`(디버그), `15053`(로컬 DNS) 은 파드 내부 전용 포트로 지정되어 있습니다.[^app-req]
- VM SSH `22` 포트: VM 환경에서는 SSH 접속이 끊기지 않도록 `22` 번 포트가 인바운드 제외 목록에 자동으로 들어갑니다. VM 설정 도구는 이 값을 `cluster.env` 의 `ISTIO_LOCAL_EXCLUDE_PORTS` 에 적습니다.[^vm-workload]

제외 목록에 걸리지 않은 나머지 TCP 트래픽은 `ISTIO_IN_REDIRECT` 체인으로 넘어갑니다. 이 체인의 `REDIRECT` 타깃이 패킷 목적지 포트를 `15006` 으로 바꾸어 Envoy 인바운드 리스너가 받게 합니다.

### REDIRECT 와 TPROXY 가로채기 방식 비교

Istio 는 인바운드 가로채기 모드로 기본값인 `REDIRECT` 외에 `TPROXY` 모드를 함께 지원합니다. 두 모드는 사용하는 커널 테이블과 원본 출발지 IP 보존 방식에서 차이가 납니다.[^run-go][^config-go]

| 비교 기준 | REDIRECT (기본값) | TPROXY |
|---|---|---|
| 사용 테이블 | `nat` (`PREROUTING` → `ISTIO_INBOUND` → `ISTIO_IN_REDIRECT`) | `mangle` (`PREROUTING` → `ISTIO_INBOUND` → `ISTIO_TPROXY`) |
| 패킷 전달 방식 | 목적지 주소·포트를 로컬 `15006` 으로 NAT 변환 | 패킷 헤더를 바꾸지 않고 `TPROXY` 로 로컬 소켓에 전달 |
| 권한 요구 | 파드별 `istio-init` 은 `NET_ADMIN`·`NET_RAW` 필요 | 프록시 컨테이너에도 `NET_ADMIN` 및 정책 라우팅 설정 필요 |

실무에서는 별도 설정이 없으면 `REDIRECT` 가 기본으로 동작합니다. 파드 안 앱이 원본 클라이언트 IP 를 커널 소켓 수준에서 그대로 봐야 할 때만 `TPROXY` 를 검토합니다.



## 3. 아웃바운드 경로와 예외 규칙

> 아웃바운드 체인은 평가 순서가 곧 동작입니다. Envoy 가 보낸 패킷이나 루프백 패스스루를 위에서 먼저 `RETURN` 시키지 않으면 트래픽이 프록시 안에서 무한히 맴돕니다.

애플리케이션이 내보내는 패킷은 모두 Envoy 를 거쳐야 하지만, Envoy 자신이 내보내는 패킷까지 다시 가로채면 자기 자신에게 연결하는 무한 루프가 생깁니다. 커널의 `nat` 테이블 `OUTPUT` 체인은 패킷을 `ISTIO_OUTPUT` 체인으로 넘겨 이 문제를 순서로 풉니다. `ISTIO_OUTPUT` 은 예외 조건을 위에서 아래로 먼저 거른 뒤, 남은 트래픽만 `ISTIO_REDIRECT` 로 보내 `15001` 포트에 넘깁니다.[^run-go]

```markdown
OUTPUT (nat) → ISTIO_OUTPUT
  1. [옵션] OutboundPortsExclude (--dport)         → RETURN
  2. -o lo -s 127.0.0.6/32                         → RETURN  (인바운드 패스스루)
  3. -o lo ! -d 127.0.0.1/32 --uid-owner 1337      → ISTIO_IN_REDIRECT (:15006)
  4. -o lo -m owner ! --uid-owner 1337             → RETURN  (앱 루프백 직접 통과)
  5. -m owner --uid-owner 1337                     → RETURN  (Envoy·pilot-agent 외부 송신)
  6. --gid-owner 1337 에 대한 3~5번 동일 규칙
  7. [옵션] DNS 캡처 활성 시 ISTIO_OUTPUT_DNS      → REDIRECT --to-ports 15053
  8. -d 127.0.0.1/32                               → RETURN  (localhost 목적지 제외)
  9. [기본 *] OutboundIPRangesInclude              → ISTIO_REDIRECT (:15001)
```

### UID 1337 과 GID 1337 의 무한 루프 방지

사이드카 컨테이너 `istio-proxy` 안의 Envoy 와 `pilot-agent` 프로세스는 기본 UID `1337` 및 GID `1337` 로 실행됩니다.[^inj-tmpl][^app-req] Envoy 가 앱 대신 외부 서비스로 TCP 패킷을 내보낼 때도 커널의 `OUTPUT` → `ISTIO_OUTPUT` 체인은 다시 실행됩니다.

이때 5번 규칙(`-m owner --uid-owner 1337 -j RETURN`)이 맨 아래 `ISTIO_REDIRECT` 보다 위에 놓여 있습니다. 소스 주석에 명시되어 있듯, 프로토콜에 관계없이 프록시 UID 가 만든 외부 패킷은 전부 `RETURN` 으로 체인을 빠져나가 `15001` 로 되돌아가지 않습니다.[^run-go]

컨트롤 플레인 통신도 이 규칙을 그대로 탑니다. `pilot-agent` 역시 같은 `istio-proxy` 컨테이너에서 UID `1337` 로 동작합니다. 따라서 `istiod` 의 `15012` 포트로 나가는 xDS 연결도 `--uid-owner 1337 -j RETURN` 에 먼저 걸려 `15001` 을 거치지 않고 바로 나갑니다.[^run-go][^inj-tmpl] 애플리케이션 컨테이너가 UID `1337` 을 쓰면 안 되는 이유도 이 규칙에 걸려 사이드카를 완전히 우회하기 때문입니다.[^app-req]

VM 에 `istio-sidecar` 패키지를 설치할 때는 `postinst.sh` 가 호스트에 `istio-proxy` 시스템 계정과 그룹을 만듭니다.[^vm-install][^vm-postinst] `istio-iptables` 는 실행 시 이 계정을 조회하므로, 컨테이너의 고정 `1337` 대신 설치 때 정해진 호스트 UID·GID 로 owner `RETURN` 규칙을 세웁니다.[^config-go]

### 루프백과 127.0.0.6 바인드 주소의 역할

루프백 인터페이스(`lo`) 규칙 셋은 자기 자신에게 보내는 호출과 인바운드 전달 경로가 엉키지 않게 가릅니다.

- `127.0.0.6/32` 송신 제외: 로컬 앱으로 요청을 넘기는 인바운드 클러스터(`InboundPassthroughCluster` 포함)는 출발지를 `127.0.0.6`(IPv6 는 `::6`)으로 바인드합니다.[^cb-go] 이 트래픽이 아래 3번 규칙(`ISTIO_IN_REDIRECT`)에 걸리면 `15006` 으로 되돌아갑니다. 그래서 2번 규칙(`-o lo -s 127.0.0.6/32 -j RETURN`)을 3번 규칙보다 앞에 둡니다.[^run-go]
- Envoy 자기 루프백 재유입: 3번 규칙은 Envoy(UID `1337`)가 `127.0.0.1` 이 아닌 파드 IP 를 향해 `lo` 로 보낸 패킷만 `15006` 으로 보냅니다. 앱이 자기 자신의 Kubernetes Service VIP 를 호출해 Envoy 아웃바운드를 거쳐 다시 자기 파드로 들어오는 경우를 처리하기 위함입니다.[^run-go]
- 앱 직접 루프백 제외: 4번과 8번 규칙은 같은 파드 안 컨테이너끼리 `127.0.0.1` 이나 `lo` 로 직접 통신할 때 Envoy 를 거치지 않게 합니다. DNS 캡처가 켜져 있을 때는 TCP 포트 `53` 만 예외로 빼서 `ISTIO_OUTPUT_DNS`(`15053`)로 넘깁니다.[^run-go]



## 4. 파드 간 East-West 전 경로

> 같은 클러스터 안의 파드끼리 통신할 때는 Ingress Gateway 없이 양쪽 사이드카 프록시만 거치는 2-hop 경로로 mTLS 와 정책이 적용됩니다.

앱이 상대 파드의 위치나 인증서 유무를 모른 채 서비스 DNS 만 부르면, 어느 지점에서 트래픽이 꺾이고 어디서 암호화가 붙는지 한눈에 잡기 어렵습니다. 아래 시퀀스 도식은 Pod A 앱에서 Pod B 앱까지 포트, 체인 이름, UID 조건이 단계마다 어떻게 맞물리는지 보여 줍니다.
![Pod A 에서 Pod B 로 가는 트래픽 가로채기와 사이드카 2-hop 흐름](./_assets/%EC%82%AC%EC%9D%B4%EB%93%9C%EC%B9%B4%20%ED%8A%B8%EB%9E%98%ED%94%BD%20%EA%B0%80%EB%A1%9C%EC%B1%84%EA%B8%B0%C2%B7iptables%20%EC%B2%B4%EC%9D%B8.east-west-flow.svg)

도식의 왼쪽에서 오른쪽으로 따라가면 각 홉의 역할이 갈립니다.

1. Pod A 앱 아웃바운드 가로채기: 앱(UID `!= 1337`)이 `api-service:8080` 으로 TCP 연결을 엽니다. 이 패킷은 `OUTPUT` 과 `ISTIO_OUTPUT`, `ISTIO_REDIRECT` 를 거쳐 로컬 Envoy A 의 `15001` 포트로 넘어갑니다.[^run-go]
2. Envoy A 라우팅과 mTLS 송신: Envoy A 는 `istiod` 에서 받은 xDS(EDS·CDS·SDS) 설정으로 목적지 Pod B IP 를 고르고 mTLS 연결을 엽니다. 이때 Envoy A 는 UID `1337` 이므로 `ISTIO_OUTPUT` 의 `RETURN` 규칙을 타고 `15001` 재진입 없이 나갑니다.[^run-go]
3. Pod B 인바운드 가로채기: 패킷이 Pod B 에 도착하면 `PREROUTING` → `ISTIO_INBOUND` → `ISTIO_IN_REDIRECT` 가 실행됩니다. 이 규칙이 목적지 포트를 `15006` 으로 바꾸어 Envoy B 로 넘깁니다.[^run-go]
4. Envoy B 종단과 앱 전달: Envoy B 는 mTLS 세션을 복호화하고 인가 정책을 확인한 뒤 출발지를 `127.0.0.6` 으로 바인드해 `8080` 으로 보냅니다. 이 패킷은 Pod B 의 `ISTIO_OUTPUT` 2번 규칙(`127.0.0.6/32 RETURN`)을 통과해 Pod B 앱에 닿습니다.[^run-go][^cb-go]

클러스터 내부 파드 간 통신(East-West)은 이처럼 호출 측 Envoy 와 수신 측 Envoy 두 홉만 거칩니다. 앱 코드는 서비스 메시 존재나 mTLS 인증서를 모른 채 기존 서비스 DNS 호출을 그대로 유지합니다.[^traffic-routing]



## 5. 한계와 예외 조건

> `iptables` 가로채기는 TCP 와 비-1337 UID 를 전제로 동작하므로, 조건이 어긋나면 프록시를 우회하거나 프로토콜 감지가 깨집니다.

실제 워크로드에 사이드카를 붙일 때는 규칙이 적용되지 않거나 예상과 다르게 라우팅되는 네 가지 경계를 확인해야 합니다.

- 애플리케이션 UID `1337` 충돌: 앱 컨테이너의 `runAsUser` 를 `1337` 로 두면 `ISTIO_OUTPUT` 의 `--uid-owner 1337 -j RETURN` 규칙에 걸립니다. 그 결과 루프백을 뺀 아웃바운드 트래픽이 전부 Envoy 를 우회합니다.[^app-req][^run-go]
- HTTP `Host` 헤더와 Pod IP 직접 호출: HTTP 트래픽은 목적지 IP 가 아니라 `Host` 헤더로 라우팅됩니다. Pod IP 를 직접 호출하면 서비스 리스너와 맞지 않아 `passthrough` 트래픽으로 분류되어 그대로(as-is) 전달됩니다. 서비스 기준 라우팅 규칙은 이 경로에 적용되지 않습니다.[^traffic-routing]
- Server-First 프로토콜: MySQL(`3306`)이나 SMTP(`25`)처럼 서버가 먼저 바이트를 보내는 프로토콜은 자동 프로토콜 감지 및 `PERMISSIVE` mTLS 와 충돌합니다. 이 경우 포트 이름을 `tcp` 로 명시하거나 `STRICT`·`DISABLE` 모드로 맞추어야 합니다.[^app-req]
- UDP 및 비-TCP 트래픽: 기본 `PREROUTING` 과 `ISTIO_REDIRECT` 는 `-p tcp` 만 가로챕니다. DNS 캡처를 켰을 때의 UDP `53`(`15053` 리다이렉트) 외 일반 UDP 트래픽은 사이드카를 거치지 않습니다.[^run-go]



## 관련 문서

> 이 문서가 이어지는 이웃 노트와 공식 문서 정독 지도입니다.

- [Istio 공식문서 정독 인덱스](./README.md) — 이 폴더의 문서 목록과 규칙
- [사이드카 시동·종료 순서](./%EC%82%AC%EC%9D%B4%EB%93%9C%EC%B9%B4%20%EC%8B%9C%EB%8F%99%C2%B7%EC%A2%85%EB%A3%8C%20%EC%88%9C%EC%84%9C.md) — `iptables` 준비 후 앱과 프록시의 기동 순서 맞추기
- [부록 B — 사이드카를 이루는 넷과 VM 이 받는 다섯 파일](../../book/istio-in-action/a0-02.부록%20—%20사이드카를%20이루는%20넷과%20VM%20이%20받는%20다섯%20파일.md) — `istio-init` 특권과 Istio CNI 전환 배경
- [부록 D — 포트 열넷과 디버그 엔드포인트 지도](../../book/istio-in-action/a0-04.부록%20—%20포트%20열넷과%20디버그%20엔드포인트%20지도.md) — `15001`·`15006`·`15020`·`15021`·`15090` 포트 용도
- [iptables·IPVS·eBPF — kube-proxy를 이해하는 세 기술](../../book/networking-and-kubernetes/02-03.iptables·IPVS·eBPF%20—%20kube-proxy를%20이해하는%20세%20기술.md) — `nat` 테이블, 훅 실행 순서, `RETURN` 타깃 기초



## 참고 자료

> 본문에서 인용한 Istio 1.32 공식 문서와 `1.32.0` 소스 파일입니다.

- [Istio 1.32 — Application Requirements](https://istio.io/v1.32/docs/ops/deployment/application-requirements/) — UID 1337 예약, 사이드카·컨트롤 플레인 포트 표, Server-First 프로토콜, 아웃바운드 라우팅 규칙
- [Istio 1.32 — Understanding Traffic Routing](https://istio.io/v1.32/docs/ops/configuration/traffic-management/traffic-routing/) — 프론트엔드/백엔드 매칭, HTTP `Host` 헤더 라우팅, Passthrough 동작
- [Istio 1.32 — Install the Istio CNI node agent](https://istio.io/v1.32/docs/setup/additional-setup/cni/) — `istio-init` 대체 및 Chained CNI 플러그인 동작
- [Istio 1.32 — Virtual Machine Installation](https://istio.io/v1.32/docs/setup/install/virtual-machine/) — VM 용 `istio-sidecar` 패키지 설치와 `cluster.env` 배치
- [Istio 1.32.0 소스 — `tools/istio-iptables/pkg/capture/run.go`](https://github.com/istio/istio/blob/1.32.0/tools/istio-iptables/pkg/capture/run.go) — `PREROUTING`/`ISTIO_INBOUND`·`OUTPUT`/`ISTIO_OUTPUT` 규칙 생성 순서

[^app-req]: Istio 1.32 Official Docs — Application Requirements (Pod requirements, Ports used by Istio, Server First Protocols, Outbound traffic), 2026-11-27 확인. <https://istio.io/v1.32/docs/ops/deployment/application-requirements/>
[^traffic-routing]: Istio 1.32 Official Docs — Understanding Traffic Routing (Protocols, Unmatched traffic), 2026-11-27 확인. <https://istio.io/v1.32/docs/ops/configuration/traffic-management/traffic-routing/>
[^run-go]: Istio 1.32.0 소스 — `tools/istio-iptables/pkg/capture/run.go` (`Run()` L222–464, `handleInboundPortsInclude()` L89–172, `127.0.0.6/32` L307–308 및 주석 L306 "bind connect from inbound passthrough cluster", `--uid-owner` `ISTIO_IN_REDIRECT` L319–333, `--uid-owner` `RETURN` L357–358), 2026-11-27 확인. <https://github.com/istio/istio/blob/1.32.0/tools/istio-iptables/pkg/capture/run.go>
[^config-go]: Istio 1.32.0 소스 — `tools/common/config/config.go` (`DefaultConfig()` L35–48, `FillConfigFromEnvironment()` L165–188: `ENVOY_USER` 기본값 `istio-proxy` 를 `user.Lookup` 으로 조회해 UID·GID 설정 후 미존재 시 `1337` 폴백), 2026-11-27 확인. <https://github.com/istio/istio/blob/1.32.0/tools/common/config/config.go>
[^inj-tmpl]: Istio 1.32.0 소스 — `manifests/charts/istio-control/istio-discovery/files/injection-template.yaml` (L92–113 `15090,15021`, L411–414 `runAsUser`/`runAsGroup` 1337), 2026-11-27 확인. <https://github.com/istio/istio/blob/1.32.0/manifests/charts/istio-control/istio-discovery/files/injection-template.yaml>
[^cni-ipt]: Istio 1.32.0 소스 — `cni/pkg/plugin/sidecar_iptables_linux.go` (`Program()` L36–73: 파드 `netns` 에서 `cmd.ProgramIptables(cfg)` 호출), 2026-11-27 확인. <https://github.com/istio/istio/blob/1.32.0/cni/pkg/plugin/sidecar_iptables_linux.go>
[^cb-go]: Istio 1.32.0 소스 — `pilot/pkg/networking/core/cluster_builder.go` (L725–735: 로컬 인바운드 클러스터의 `UpstreamBindConfig` 가 `passThroughBindIPs[0]` 으로 바인드, L764–793 `buildInboundPassthroughCluster()`: `InboundPassthroughBindIpv4` 바인드), 2026-11-27 확인. <https://github.com/istio/istio/blob/1.32.0/pilot/pkg/networking/core/cluster_builder.go>
[^vm-install]: Istio 1.32 Official Docs — Virtual Machine Installation (`istio-sidecar.deb`·`istio-sidecar.rpm` 설치 및 `cluster.env` 배치), 2026-11-27 확인. <https://istio.io/v1.32/docs/setup/install/virtual-machine/>
[^vm-postinst]: Istio 1.32.0 소스 — `tools/packaging/postinst.sh` (L22–30: `useradd --system` / `adduser --system` 로 `istio-proxy` 계정·그룹 생성), 2026-11-27 확인. <https://github.com/istio/istio/blob/1.32.0/tools/packaging/postinst.sh>
[^vm-workload]: Istio 1.32.0 소스 — `istioctl/pkg/workload/workload.go` (L350–370: `excludePorts := "22,15090,15021"` 을 `ISTIO_LOCAL_EXCLUDE_PORTS` 에 설정) 및 `tools/packaging/common/sidecar.env` (L41–42: 인바운드 제외 목록 설명 아래 `Port 22 is automatically excluded`), 2026-11-27 확인. <https://github.com/istio/istio/blob/1.32.0/istioctl/pkg/workload/workload.go>
