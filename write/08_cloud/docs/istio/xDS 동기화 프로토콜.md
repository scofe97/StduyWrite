---
title: "xDS 동기화 프로토콜 — Istio 리소스 매핑·Delta xDS·ACK/NACK"
tags: [istio, envoy, xds, delta-xds, ads, ack-nack, proxy-status]
status: draft
source:
  - https://www.envoyproxy.io/docs/envoy/v1.36.0/api-docs/xds_protocol
  - https://www.envoyproxy.io/docs/envoy/v1.36.0/intro/arch_overview/operations/dynamic_configuration
  - https://istio.io/v1.32/docs/ops/diagnostic-tools/proxy-cmd/
  - https://istio.io/v1.32/docs/reference/commands/pilot-discovery/
  - https://istio.io/v1.32/docs/reference/commands/pilot-agent/
  - https://istio.io/v1.32/docs/ops/deployment/architecture/
  - https://istio.io/v1.32/docs/concepts/security/
related:
  - ./README.md
  - ../../book/istio-in-action/03-01.Envoy가 맡는 일과 Istio가 보태는 일.md
  - ../../book/istio-in-action/10-01.프록시는 다 알고 있고 사람은 못 읽는다.md
  - ../../book/istio-in-action/11-01.컨트롤 플레인의 성능은 낡은 설정의 수명이다.md
updated: "2026-11-27"
---

# xDS 동기화 프로토콜 — Istio 리소스 매핑·Delta xDS·ACK/NACK

---

> `istiod` 는 Istio 리소스를 Envoy 의 xDS v3 타입으로 번역해 Delta gRPC 스트림으로 밀어냅니다. Envoy 는 수신한 설정을 검증한 뒤 `nonce` 와 `version_info` 로 승인하거나 거부하며, 이 응답이 `istioctl proxy-status` 의 상태를 만듭니다.

이 문서는 Envoy v1.36.0 의 xDS 프로토콜 명세와 Istio 1.32 공식 문서·소스를 근거로 썼습니다. 클러스터에서 패킷이나 스트림을 직접 잡아 확인하지는 않았습니다.

xDS 여섯 API 의 개요와 `ADS` 순서 경쟁, `istiod` 부트스트랩 구조는 [03-01 노트](../../book/istio-in-action/03-01.Envoy가%20맡는%20일과%20Istio가%20보태는%20일.md#5-정적-설정과-xds)가 다룹니다. 이 문서는 그 뒤를 이어 리소스 매핑, 전송 변종, 검증 회신, 상태 진단의 연결을 봅니다.

## 1. Istio 리소스와 xDS 타입 URL 매핑

> Envoy 는 Kubernetes 나 Istio 의 CRD 를 직접 읽지 못합니다. `istiod` 가 각 설정을 xDS v3 리소스로 번역해 Type URL 로 구분해 내려보냅니다.

`VirtualService` 나 `DestinationRule` 을 고쳤는데도 요청이 503 오류로 실패할 때가 있습니다. 이럴 때는 `istiod` 가 어느 xDS 단계까지 내려보냈는지부터 갈라야 원인을 찾습니다.

**xDS**(Extensible Discovery Service)는 Envoy 가 동적 설정을 받아 오는 API 묶음입니다. **CRD**(Custom Resource Definition)는 사용자가 Kubernetes 에 추가하는 리소스 정의입니다.[^istio-arch]

`istiod` 의 `pilot-discovery` 가 클러스터의 Istio 리소스와 서비스 상태를 감시합니다. 이 정보를 Envoy 가 읽는 다섯 가지 핵심 xDS 리소스로 바꿉니다.[^istio-arch] 각 리소스는 `type.googleapis.com/<리소스 타입>` 꼴의 **Type URL** 로 구분합니다.[^envoy-xds-types]

| Istio · Kubernetes 입력 | xDS API | Envoy 역할 | v3 Type URL |
|---|---|---|---|
| `Gateway` 와 `PeerAuthentication` | `LDS` | 리스너와 인바운드 필터 체인 | `type.googleapis.com/envoy.config.listener.v3.Listener` |
| `VirtualService` | `RDS` | 가상 호스트와 경로 라우팅 규칙 | `type.googleapis.com/envoy.config.route.v3.RouteConfiguration` |
| `DestinationRule` | `CDS` | 로드밸런싱·연결 풀·서킷 브레이커 | `type.googleapis.com/envoy.config.cluster.v3.Cluster` |
| 서비스 엔드포인트(`Service` 등) | `EDS` | 실제 파드 IP·포트·로컬리티 목록 | `type.googleapis.com/envoy.config.endpoint.v3.ClusterLoadAssignment` |
| 워크로드 mTLS 인증서·개인 키 | `SDS` | 디스크 마운트 없이 메모리로 인증서 주입 | `type.googleapis.com/envoy.extensions.transport_sockets.tls.v3.Secret` |

표의 다섯 약어는 다음과 같습니다.

- LDS(Listener Discovery Service): Envoy 가 어느 IP 와 포트에서 트래픽을 받을지 정합니다.
- RDS(Route Discovery Service): 들어온 요청의 호스트와 경로를 어느 백엔드 묶음으로 보낼지 정합니다.
- CDS(Cluster Discovery Service): 백엔드 서비스 묶음의 연결 정책과 로드밸런싱 방식을 정합니다.
- EDS(Endpoint Discovery Service): 클러스터에 속한 실제 파드의 IP 와 포트를 채웁니다.
- SDS(Secret Discovery Service): 상호 TLS 인증에 쓰는 X.509 인증서와 개인 키를 전달합니다.

`Gateway` 는 수신 포트와 호스트 진입점을 여는 리스너를 만듭니다. `PeerAuthentication` 은 인바운드 리스너의 인증 설정에 반영됩니다.[^istio-lds]

인증서 배포인 `SDS` 는 파드 안의 `istio-agent` 가 맡습니다. 에이전트는 `istiod` CA 에서 받은 인증서를 로컬 유닉스 소켓으로 Envoy 에 넘깁니다.[^istio-sds]

### 확장 xDS API 세 가지

다섯 핵심 API 외에 거대한 라우트 테이블이나 런타임 플래그를 다루는 확장 API 가 셋 더 있습니다.[^envoy-xds-types]

- SRDS(Scoped Route Discovery Service): 라우트 테이블이 클 때 스코프별 조각으로 나눠 조회합니다.
- VHDS(Virtual Host Discovery Service): `VirtualHost` 를 필요 시점에 따로 요청하는 Delta 전용 API 입니다.
- RTDS(Runtime Discovery Service): 프로세스 재시작 없이 Envoy 피처 플래그와 런타임 설정을 바꿉니다.



## 2. SotW 와 Delta xDS 의 전송 차이

> SotW 는 변경 없는 리소스까지 목록 전체를 다시 보냅니다. Delta xDS 는 바뀐 리소스와 삭제된 이름만 보내 대역폭과 메모리 부담을 줄입니다.

클러스터의 서비스가 수천 개로 불어나면 엔드포인트 하나만 바뀌어도 설정 전체가 무거워집니다. `istiod` 의 푸시 크기와 대역폭 병목은 [11-01 노트](../../book/istio-in-action/11-01.컨트롤%20플레인의%20성능은%20낡은%20설정의%20수명이다.md#6-기본값은-모두가-모두를-알게-한다)가 다룹니다. 전송 계층에서 이 낭비를 줄이려고 나온 방식이 Delta xDS 입니다.

**SotW**(State of the World)는 초기 xDS 가 쓰던 전체 상태 동기화 방식입니다. 클라이언트는 매 `DiscoveryRequest` 의 `resource_names` 에 구독 중인 이름 전체를 싣습니다.[^envoy-sotw] 특히 `LDS` 와 `CDS` 는 100개 중 1개만 바뀌어도 서버가 100개 전체를 다시 보냅니다.[^envoy-sotw]

**Delta xDS**(Incremental xDS)는 직전 상태 대비 변경분만 주고받는 방식입니다. 메시지는 `DeltaDiscoveryRequest` 와 `DeltaDiscoveryResponse` 를 씁니다.[^envoy-delta] 클라이언트는 추가·해제할 이름만 알리고, 서버는 변경분과 삭제 이름만 보냅니다.[^envoy-delta]

| 구분 | SotW | Delta xDS |
|---|---|---|
| 요청 메시지 | `DiscoveryRequest` (`resource_names` 전체) | `DeltaDiscoveryRequest` (`subscribe`·`unsubscribe`) |
| `LDS`·`CDS` 응답 | 변경 없어도 구독 목록 전체 전송 | 변경·추가된 리소스만 전송 |
| 삭제 전달 | 목록 누락(`LDS`·`CDS`) 또는 참조 해제(`RDS`·`EDS`) | `removed_resources` 필드로 명시 |
| 지연 로딩 | 미지원 | 요청 도착 시 필요한 리소스만 온디맨드 요청 |
| 지원 전송 | gRPC 스트리밍 · REST-JSON 폴링 | 양방향 gRPC 스트리밍 전용 |

Delta xDS 는 요청이 들어온 뒤에야 필요한 클러스터를 요청하는 지연 로딩(lazy loading)을 지원합니다.[^envoy-delta] 또한 요청한 리소스가 없을 때도 `removed_resources` 에 이름을 실어 보냅니다. 클라이언트는 15초 타임아웃을 기다리지 않고 부재를 바로 판별합니다.[^envoy-delta]

다만 모든 xDS 변종은 이름이 붙은 리소스 전체 단위로만 동작합니다.[^envoy-sotw] `EDS` 응답 하나 안의 개별 파드 IP 몇 개만 쪼개 보내는 필드는 없습니다. 파드 IP 하나가 바뀌어도 해당 `ClusterLoadAssignment` 리소스 전체를 새로 보냅니다.[^envoy-sotw]

### Istio 1.32 의 기본 전송 방식

Istio 1.32 는 Delta xDS 를 기본값으로 씁니다. `pilot-discovery` 와 `pilot-agent` 에서 `ISTIO_DELTA_XDS` 의 기본값이 `true` 입니다.[^istio-delta-flag] 부트스트랩 생성 코드도 `DeltaXds` 가 켜져 있으면 연결 타입을 `DELTA_GRPC` 로 지정합니다.[^istio-bootstrap]

그래도 Delta xDS 가 언제나 변경된 조각만 보내는 것은 아닙니다. Istio 레퍼런스는 이 API 를 써도 경우에 따라 변경 없는 설정을 보낼 수 있다고 적습니다.[^istio-delta-flag] 모든 리소스를 한 스트림에 싣는 **ADS**(Aggregated Discovery Service)에서는 `DeltaAggregatedResources` RPC 를 씁니다.[^envoy-delta]



## 3. ACK 와 NACK 검증 흐름

> Envoy 는 `DiscoveryResponse` 를 받으면 검증 결과와 `nonce` 를 `DiscoveryRequest` 에 담아 회신합니다. 오류가 나도 gRPC 스트림을 끊지 않고 직전 유효 설정을 유지합니다.

잘못된 설정이 내려왔을 때 프록시가 그냥 죽으면 서비스 트래픽이 끊깁니다. 반대로 오류를 숨기면 컨트롤 플레인은 새 설정이 적용됐다고 잘못 알게 됩니다. Envoy 는 `version_info` 와 `nonce`, `error_detail` 세 필드로 이 문제를 풉니다.

아래 그림은 `istiod` 와 `Envoy` 가 `DiscoveryResponse` 와 `DiscoveryRequest` 를 주고받는 흐름입니다. `version_info` 는 리소스 타입의 버전을, `nonce` 는 서버가 응답마다 붙이는 식별자를 뜻합니다.

![istiod와 Envoy 사이의 ACK와 NACK 흐름](./_assets/xDS%20동기화%20프로토콜.ack-nack.svg)

위쪽 `[검증 통과]` 분기에서는 `Envoy` 가 응답과 같은 `v2` 와 `n2` 를 돌려보내 승인을 알립니다. 아래쪽 `[검증 실패]` 분기에서는 `error_detail` 을 채우고 직전 버전 `v1` 을 돌려보낸 뒤 `v1` 설정을 그대로 유지합니다.

### version_info 와 nonce 의 역할

**version_info** 는 각 xDS 리소스 타입이 따로 갖는 문자열 버전입니다.[^envoy-ack] `ADS` 로 단일 스트림을 공유해도 `LDS`·`RDS`·`CDS`·`EDS` 는 각자 독립된 `version_info` 를 가집니다.[^envoy-ack] 서버가 `v2` 를 보낸 뒤 클라이언트가 `v2` 를 돌려주면 그 리소스 타입의 최신 버전이 맞았다는 뜻입니다.

**nonce** 는 서버가 `DiscoveryResponse` 마다 발급하는 짝짓기 토큰입니다.[^envoy-ack] 비동기 스트림에서는 클라이언트가 `v1` 상태에서 새 리소스를 요청하자마자 서버가 `v2` 를 보내 버리는 경쟁 상태가 생깁니다.[^envoy-ack] 이때 `v1` 이 적힌 뒤늦은 요청이 `v2` 를 거부한 것으로 오인되지 않으려면 어느 응답에 대한 회신인지 구분해야 합니다.

Envoy 는 모든 후속 요청의 `response_nonce` 에 가장 최근 `nonce` 를 적습니다.[^envoy-ack] ADS 에서는 `nonce` 도 리소스 타입마다 따로 추적합니다.[^envoy-ack] SotW 에서 서버는 오래된 `nonce` 요청에 응답을 보내지 않으므로, 늦은 힌트 요청을 `NACK` 으로 착각하지 않습니다.[^envoy-ack] Delta xDS 에서는 오래된 `nonce` 라도 구독 변경은 반영해야 합니다.[^envoy-delta] 단 `nonce` 는 해당 gRPC 스트림 안에서만 유효하므로 스트림이 새로 열리면 효력이 사라집니다.[^envoy-ack]

Delta xDS 에서는 `DeltaDiscoveryResponse` 의 `nonce` 가 필수 필드입니다.[^envoy-delta] `system_version_info` 필드는 디버깅 용도로만 쓰이며 승인 판정에는 쓰지 않습니다.[^envoy-delta] 클라이언트는 `response_nonce` 와 `error_detail` 유무로 승인 여부를 전합니다.[^envoy-delta]

### PGV 검증과 ACK·NACK 의 뜻

Envoy 는 리소스를 받으면 **PGV**(protoc-gen-validate) 어노테이션으로 시맨틱 제약을 검사합니다.[^envoy-pgv] 명세는 이 검사를 클라이언트의 필수 절차로 정하지 않습니다. 명세가 드는 예로 Envoy 는 이 검사를 하고 gRPC 는 하지 않습니다.[^envoy-pgv] 예를 들어 포트 번호 범위나 필수 필드 누락을 이 단계에서 걸러냅니다. 다만 PGV 가 모든 검사를 대신하지는 않으므로 Envoy 는 PGV 와 무관한 이유로도 리소스를 거부할 수 있습니다.[^envoy-pgv]

**ACK**(Acknowledgement)는 응답에 담긴 개별 리소스를 단독으로 검사했을 때 유효하고 적용할 의도가 있다는 회신입니다.[^envoy-ack] Envoy 공식 명세는 ACK 가 실제 적용 성공을 뜻하지 않는다고 못 박습니다.[^envoy-ack] 클라이언트가 ACK 를 보낸 뒤에도 리스너 바인딩 실패 등 실제 적용 단계에서 실패할 수 있기 때문입니다.[^envoy-ack]

**NACK**(Negative Acknowledgement)은 하나 이상의 리소스가 유효하지 않을 때 보내는 거부 회신입니다.[^envoy-ack] Envoy 는 `error_detail` 에 오류를 채우고 마지막 유효 `version_info` 와 `response_nonce` 를 보냅니다.[^envoy-ack] 명세는 버전 추론보다 `error_detail` 필드 존재 여부로 NACK 을 판정하는 방식을 선호한다고 적습니다.[^envoy-ack]

NACK 을 보내더라도 `istiod` 와 Envoy 사이의 **gRPC**(gRPC Remote Procedure Call) 스트림은 유지됩니다.[^envoy-ack] Envoy 는 직전까지 유효했던 마지막 설정으로 계속 트래픽을 처리합니다. 이어서 `istiod` 가 오류를 고친 새 응답을 같은 스트림으로 보내면 Envoy 가 정상 `ACK` 로 넘어갑니다.[^envoy-ack]



## 4. proxy-status 상태 판정

> `istioctl proxy-status` 의 세 상태는 xDS 스트림에서 마지막 응답이 전송됐는지와 `ACK` 가 돌아왔는지로 갈립니다.

설정이 반영되지 않을 때 `istiod` 가 아직 안 보낸 것인지, 보냈는데 Envoy 가 `ACK` 를 안 보낸 것인지 가려야 원인을 좁힙니다. `istioctl proxy-status` 명령의 사용법과 실전 진단 순서는 [10-01 노트](../../book/istio-in-action/10-01.프록시는%20다%20알고%20있고%20사람은%20못%20읽는다.md#2-컨트롤-플레인을-먼저-지운다)가 다룹니다. 여기서는 그 출력의 세 상태가 앞 절의 xDS 회신과 어떻게 맞물리는지만 짚습니다.

Istio 1.32 공식 진단 문서는 `istioctl proxy-status` 의 세 상태를 다음과 같이 정의합니다.[^istio-proxy-status]

- SYNCED: `istiod` 가 마지막으로 보낸 설정을 Envoy 가 받고 `ACK` 를 돌려보낸 상태입니다.
- STALE: `istiod` 가 설정을 보냈지만 Envoy 의 `ACK` 를 받지 못한 상태입니다.
- NOT SENT: `istiod` 가 해당 xDS 타입의 설정을 아직 아무것도 보내지 않은 상태입니다.

`STALE` 은 두 가지 경로로 생깁니다. 첫째는 네트워크 문제나 Istio 버그로 응답이 오가지 못하는 경우입니다.[^istio-proxy-status] 둘째는 Envoy 가 잘못된 설정을 받아 `NACK` 을 보낸 뒤 아직 새 유효 버전으로 `ACK` 를 못 끝낸 경우입니다. 이 둘째 경로는 페이지 정의의 「ACK 를 받지 못함」을 따른 해석입니다.

`NOT SENT` 는 오류가 아닌 경우가 많습니다. 해당 프록시가 그 xDS 타입에서 받아 갈 설정이 없으면 `istiod` 가 응답을 보내지 않기 때문입니다.[^istio-proxy-status] 반면 프록시 자체가 목록에서 빠졌다면 현재 어느 `istiod` 인스턴스와도 xDS 스트림을 맺지 못한 상태입니다.[^istio-proxy-status]



## 관련 문서

> 이 문서의 배경과 실전 진단·튜닝으로 이어지는 이웃 문서입니다.

- [Istio 공식문서 정독 인덱스](./README.md) — 같은 폴더의 Istio 공식 문서 편 목록
- [Envoy가 맡는 일과 Istio가 보태는 일](../../book/istio-in-action/03-01.Envoy가%20맡는%20일과%20Istio가%20보태는%20일.md#5-정적-설정과-xds) — xDS 여섯 API 개요, `ADS` 순서 경쟁, `istiod` 부트스트랩 구조
- [프록시는 다 알고 있고 사람은 못 읽는다](../../book/istio-in-action/10-01.프록시는%20다%20알고%20있고%20사람은%20못%20읽는다.md#2-컨트롤-플레인을-먼저-지운다) — `istioctl proxy-status` 와 `config_dump` 진단 절차
- [컨트롤 플레인의 성능은 낡은 설정의 수명이다](../../book/istio-in-action/11-01.컨트롤%20플레인의%20성능은%20낡은%20설정의%20수명이다.md) — `istiod` 푸시 큐, 디바운싱, `Sidecar` 리소스로 설정 크기 줄이기



## 참고 자료

> 본문에서 인용한 Envoy 및 Istio 1.32 1차 자료입니다.

- [Envoy v1.36 — xDS REST and gRPC protocol](https://www.envoyproxy.io/docs/envoy/v1.36.0/api-docs/xds_protocol) — v3 Type URL, PGV 검증, SotW·Incremental 차이, ACK/NACK 규격
- [Envoy v1.36 — xDS configuration API overview](https://www.envoyproxy.io/docs/envoy/v1.36.0/intro/arch_overview/operations/dynamic_configuration) — LDS·RDS·CDS·EDS·SRDS·VHDS 개요
- [Istio 1.32 — Architecture](https://istio.io/v1.32/docs/ops/deployment/architecture/) — `istiod` 의 Envoy 설정 번역과 배포 역할
- [Istio 1.32 — Security Concepts](https://istio.io/v1.32/docs/concepts/security/) — `istio-agent` 의 `SDS` 기반 인증서·개인 키 전달
- [Istio 1.32 — pilot-discovery](https://istio.io/v1.32/docs/reference/commands/pilot-discovery/) · [pilot-agent](https://istio.io/v1.32/docs/reference/commands/pilot-agent/) — `ISTIO_DELTA_XDS` 기본값 `true`
- [Istio 1.32 — Debugging Envoy and Istiod](https://istio.io/v1.32/docs/ops/diagnostic-tools/proxy-cmd/) — `istioctl proxy-status` 의 `SYNCED`·`STALE`·`NOT SENT` 정의

[^istio-arch]: Istio 1.32 — Architecture. "Istiod converts high level routing rules that control traffic behavior into Envoy-specific configurations, and propagates them to the sidecars at runtime." <https://istio.io/v1.32/docs/ops/deployment/architecture/> (2026-11-27 조회)
[^envoy-xds-types]: Envoy v1.36.0 — xDS REST and gRPC protocol, Resource Types 및 RPC Services and Methods. `envoy.config.listener.v3.Listener`, `RouteConfiguration`, `ScopedRouteConfiguration`, `VirtualHost`, `Cluster`, `ClusterLoadAssignment`, `Secret`, `Runtime` 과 `type.googleapis.com/<resource type>` 형식을 정의합니다. <https://www.envoyproxy.io/docs/envoy/v1.36.0/api-docs/xds_protocol#resource-types> (2026-11-27 조회)
[^istio-lds]: Istio 1.32 소스(`release-1.32`) — `pilot/pkg/networking/core/listener_builder.go` 와 `pilot/pkg/networking/core/cluster.go`. `listener_builder.go` 는 `TLSInspector` 플래그를 두고 `authnBuilder.BuildHTTP` 로 인증 HTTP 필터를 붙입니다. `cluster.go` 는 `PeerAuthentication`·`DestinationRule` 변경을 클러스터 갱신 경로에서 다룹니다. <https://github.com/istio/istio/blob/release-1.32/pilot/pkg/networking/core/listener_builder.go> (2026-11-27 조회)
[^istio-sds]: Istio 1.32 — Security Concepts, Istio identity and certificate management. "When a workload is started, Envoy requests the certificate and key from the Istio agent in the same container via the Envoy secret discovery service (SDS) API." <https://istio.io/v1.32/docs/concepts/security/> (2026-11-27 조회)
[^envoy-sotw]: Envoy v1.36.0 — xDS REST and gRPC protocol, Variants of the xDS Transport Protocol 및 Grouping Resources into Responses. SotW 는 `resource_names` 전체와 `LDS`·`CDS` 전체 집합 재전송을 요구하며, 모든 변종이 이름 있는 리소스 전체 단위로 동작합니다. <https://www.envoyproxy.io/docs/envoy/v1.36.0/api-docs/xds_protocol#variants-of-the-xds-transport-protocol> (2026-11-27 조회)
[^envoy-delta]: Envoy v1.36.0 — xDS REST and gRPC protocol, Incremental xDS. "Allows the protocol to communicate on the wire in terms of resource/resource name deltas ("Delta xDS")." "Allows the Envoy to on-demand / lazily request additional resources." "There is no REST version of Incremental xDS yet." 존재하지 않는 리소스에는 `removed_resources` 로 응답합니다. <https://www.envoyproxy.io/docs/envoy/v1.36.0/api-docs/xds_protocol#incremental-xds> (2026-11-27 조회)
[^istio-delta-flag]: Istio 1.32 — `pilot-discovery` 및 `pilot-agent` 레퍼런스, `ISTIO_DELTA_XDS`. `Boolean`, 기본값 `true`. "If enabled, pilot will only send the delta configs as opposed to the state of the world configuration on a Resource Request. While this feature uses the delta xds api, it may still occasionally send unchanged configurations instead of just the actual deltas." <https://istio.io/v1.32/docs/reference/commands/pilot-discovery/> (2026-11-27 조회)
[^istio-bootstrap]: Istio 1.32 소스(`release-1.32`) — `pkg/bootstrap/config.go` (`if features.DeltaXds { xdsType = "DELTA_GRPC" }`) 및 `pilot/pkg/features/experimental.go` (`ISTIO_DELTA_XDS` 기본값 `true`). <https://github.com/istio/istio/blob/release-1.32/pkg/bootstrap/config.go> (2026-11-27 조회)
[^envoy-ack]: Envoy v1.36.0 — xDS REST and gRPC protocol, ACK/NACK and resource type instance version 및 ACK and NACK semantics summary. "ACKing simply means that the client considered each of the resources in the response to be valid when evaluated in isolation." "After the client sends ACK, it can still fail to apply the resources." "After a NACK, an API update may succeed at a new version Y:" <https://www.envoyproxy.io/docs/envoy/v1.36.0/api-docs/xds_protocol#ack-nack-and-resource-type-instance-version> (2026-11-27 조회)
[^envoy-pgv]: Envoy v1.36.0 — xDS REST and gRPC protocol, Protoc-Gen-Validate Annotations. "The protobuf messages for the individual xDS resource types have annotations using protoc-gen-validate (PGV), which indicate semantic constraints to be used to validate the contents of a resource when it is received by a client." "clients may reject a resource for reasons unrelated to the PGV annotations." <https://www.envoyproxy.io/docs/envoy/v1.36.0/api-docs/xds_protocol#protoc-gen-validate-annotations> (2026-11-27 조회)
[^istio-proxy-status]: Istio 1.32 — Debugging Envoy and Istiod. `SYNCED`, `NOT SENT`, `STALE` 의 정의와 프록시 누락 시 의미. <https://istio.io/v1.32/docs/ops/diagnostic-tools/proxy-cmd/> (2026-11-27 조회)
