---
title: Istio in Action — 정독 인덱스
tags: [moc, study-index, book, istio, service-mesh, envoy, sidecar]
status: draft
source:
  - 《Istio in Action》(Christian E. Posta·Rinor Maloku, Manning) — 챕터 PDF 14편 + 부록 5편
  - 챕터 PDF 폴더 — GoogleDrive/내 드라이브/book/Istio in Action/
related:
  - ../networking-and-kubernetes/README.md
  - ../kubernetes-in-action/README.md
  - ../kubernetes-up-and-running/README.md
  - ../container-security/README.md
  - ../../docs/istio/README.md
  - ../../README.md
  - ../../../troubleshooting/mesh/README.md
learning:
  topic: istio-in-action
  scope: durable
  level: 기본
  last_verified:            # Phase 4 자답·_review 회차 미실시 — 원문 대조일로 대신 채우지 않음
  blocked_count:
  next_lesson: "본편 14장 + 부록 A~E 완주(18편). 다음은 Phase 4 자답 회차 — 18편의 면접 질문 139개에 자답하고 last_verified를 채운다(_review/_queue.md 참조)."
updated: 2026-11-29
---

# Istio in Action — 정독 인덱스

---

> 『Istio in Action』(Christian E. Posta·Rinor Maloku, Manning)을 장 단위로 정독한 책-종속 학습노트입니다. 서비스 메시와 Envoy 데이터 플레인에서 출발해 트래픽 제어·레질리언스·관측·보안·튜닝·멀티 클러스터·VM·Wasm 확장까지 다룹니다.

## 작성 현황

> 본편 14장과 부록 A~E를 정리한 정독 노트 18편(본편 14편 · 부록 4편)의 목록입니다.

| 편 | 제목과 한 줄 요약 | 상태 |
|----|------------------|------|
| [01-01](./01-01.%EC%84%9C%EB%B9%84%EC%8A%A4%20%EB%A9%94%EC%8B%9C%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9D%84%20%EC%9D%B8%ED%94%84%EB%9D%BC%EB%A1%9C%20%EB%B0%80%EC%96%B4%EB%83%88%EB%8A%94%EA%B0%80.md) | 서비스 메시는 무엇을 인프라로 밀어냈는가 — 라이브러리에서 프록시로 옮긴 결정과 대가 | 완료 (draft) |
| [02-01](./02-01.%EB%B0%B0%ED%8F%AC%EC%99%80%20%EB%A6%B4%EB%A6%AC%EC%8A%A4%EB%A5%BC%20%EA%B0%80%EB%A5%B4%EB%8A%94%20%EC%B2%AB%20%EC%8B%A4%EC%8A%B5.md) | 배포와 릴리스를 가르는 첫 실습 — 코드 배포와 트래픽 릴리스의 분리 | 완료 (draft) |
| [03-01](./03-01.Envoy%EA%B0%80%20%EB%A7%A1%EB%8A%94%20%EC%9D%BC%EA%B3%BC%20Istio%EA%B0%80%20%EB%B3%B4%ED%83%9C%EB%8A%94%20%EC%9D%BC.md) | Envoy가 맡는 일과 Istio가 보태는 일 — Envoy 데이터 플레인과 xDS 컨트롤 플레인 | 완료 (draft) |
| [04-01](./04-01.%EB%AC%B8%EC%9D%84%20%EC%97%AC%EB%8A%94%20%EC%9D%BC%EA%B3%BC%20%EA%B8%B8%EC%9D%84%20%EB%82%B4%EB%8A%94%20%EC%9D%BC%EC%9D%84%20%EA%B0%80%EB%A5%B8%EB%8B%A4.md) | 문을 여는 일과 길을 내는 일을 가른다 — Gateway(L4·L5)와 VirtualService(L7) 분리·TLS·SNI | 완료 (draft) |
| [05-01](./05-01.%EC%9C%84%ED%97%98%EC%97%90%20%EB%85%B8%EC%B6%9C%EB%90%98%EB%8A%94%20%ED%8A%B8%EB%9E%98%ED%94%BD%EC%9D%84%20%EC%A4%84%EC%97%AC%20%EA%B0%80%EB%8A%94%20%EC%88%9C%EC%84%9C.md) | 위험에 노출되는 트래픽을 줄여 가는 순서 — 다크 런치·가중치·미러링·ServiceEntry egress 제어 | 완료 (draft) |
| [06-01](./06-01.%EC%8B%A4%ED%8C%A8%EB%A5%BC%20%EA%B2%AC%EB%94%94%EB%8A%94%20%EC%9D%BC%EC%9D%84%20%ED%94%84%EB%A1%9D%EC%8B%9C%EB%A1%9C%20%EC%98%AE%EA%B2%BC%EC%9D%84%20%EB%95%8C.md) | 실패를 견디는 일을 프록시로 옮겼을 때 — 로드밸런싱·타임아웃·재시도·커넥션 풀·이상치 감지 | 완료 (draft) |
| [07-01](./07-01.%EB%AF%B8%EB%A6%AC%20%EC%A0%95%ED%95%98%EC%A7%80%20%EC%95%8A%EC%95%98%EB%8D%98%20%EA%B2%83%EC%9D%84%20%EB%82%98%EC%A4%91%EC%97%90%20%EC%84%B8%EB%A0%A4%EB%A9%B4.md) | 미리 정하지 않았던 것을 나중에 세려면 — 프록시·istiod 메트릭·Prometheus 스크랩·차원 확장 | 완료 (draft) |
| [08-01](./08-01.%EB%A9%94%EC%8B%9C%EA%B0%80%20%EC%A0%88%EB%B0%98%EA%B9%8C%EC%A7%80%EB%A7%8C%20%ED%95%B4%20%EC%A3%BC%EB%8A%94%20%EC%9D%BC.md) | 메시가 절반까지만 해 주는 일 — Grafana·Jaeger 헤더 전파 경계·Kiali 콜 그래프 | 완료 (draft) |
| [09-01](./09-01.%EA%B1%B0%EC%9D%98%20%EC%95%88%EC%A0%84%ED%95%9C%20%EA%B8%B0%EB%B3%B8%EA%B0%92%EC%9D%84%20%EB%8B%AB%EC%95%84%20%EA%B0%80%EB%8A%94%20%EC%88%9C%EC%84%9C.md) | 거의 안전한 기본값을 닫아 가는 순서 — SPIFFE mTLS·PeerAuthentication·인가 정책·ExtAuthz | 완료 (draft) |
| [10-01](./10-01.%ED%94%84%EB%A1%9D%EC%8B%9C%EB%8A%94%20%EB%8B%A4%20%EC%95%8C%EA%B3%A0%20%EC%9E%88%EA%B3%A0%20%EC%82%AC%EB%9E%8C%EC%9D%80%20%EB%AA%BB%20%EC%9D%BD%EB%8A%94%EB%8B%A4.md) | 프록시는 다 알고 있고 사람은 못 읽는다 — istioctl analyze·proxy-config·Envoy 로그 진단 순서 | 완료 (draft) |
| [11-01](./11-01.%EC%BB%A8%ED%8A%B8%EB%A1%A4%20%ED%94%8C%EB%A0%88%EC%9D%B8%EC%9D%98%20%EC%84%B1%EB%8A%A5%EC%9D%80%20%EB%82%A1%EC%9D%80%20%EC%84%A4%EC%A0%95%EC%9D%98%20%EC%88%98%EB%AA%85%EC%9D%B4%EB%8B%A4.md) | 컨트롤 플레인의 성능은 낡은 설정의 수명이다 — xDS 푸시 지연·Sidecar 스코프·배칭·자원 확장 순서 | 완료 (draft) |
| [12-01](./12-01.%EA%B2%BD%EA%B3%84%EB%A5%BC%20%EC%A7%80%EC%9A%B0%EB%8A%94%20%EC%A0%84%EC%A0%9C%20%EC%85%8B%EA%B3%BC%20%EB%82%A8%EB%8A%94%20%ED%95%9C%20%EC%9E%90%EB%A6%AC.md) | 경계를 지우는 전제 셋과 남는 한 자리 — 멀티 클러스터 발견·연결·공통 신뢰·동서 게이트웨이 | 완료 (draft) |
| [13-01](./13-01.%EC%9E%90%EB%8F%99%EC%9C%BC%EB%A1%9C%20%EB%90%98%EB%8D%98%20%EC%9D%BC%EC%9D%B4%20%EB%AA%A9%EB%A1%9D%EC%9D%B4%20%EB%90%98%EC%96%B4%20%EB%82%98%ED%83%80%EB%82%9C%EB%8B%A4.md) | 자동으로 되던 일이 목록이 되어 나타난다 — VM 편입 6요소·WorkloadGroup·로컬 DNS 프록시 | 완료 (draft) |
| [14-01](./14-01.Envoy%EB%A5%BC%20%EC%83%88%EB%A1%9C%20%EB%B9%8C%EB%93%9C%ED%95%98%EC%A7%80%20%EC%95%8A%EC%9C%BC%EB%A0%A4%EA%B3%A0%20%EB%82%B8%20%EB%84%A4%20%EA%B0%9C%EC%9D%98%20%EB%AC%B8.md) | Envoy를 새로 빌드하지 않으려고 낸 네 개의 문 — EnvoyFilter·외부 호출·Lua·WasmPlugin 확장 | 완료 (draft) |
| [a0-01](./a0-01.%EB%B6%80%EB%A1%9D%20%E2%80%94%20%EC%84%A4%EC%B9%98%EB%A5%BC%20%EA%B3%A0%EB%A5%B4%EB%8A%94%20API%20%EC%99%80%20%ED%94%84%EB%A1%9C%ED%8C%8C%EC%9D%BC%20%EC%97%AC%EB%8D%9F.md) | 부록 — 설치를 고르는 API 와 프로파일 여덟 (부록 A: istioctl·Helm·Operator·배포 프로파일) | 완료 (draft) |
| [a0-02](./a0-02.%EB%B6%80%EB%A1%9D%20%E2%80%94%20%EC%82%AC%EC%9D%B4%EB%93%9C%EC%B9%B4%EB%A5%BC%20%EC%9D%B4%EB%A3%A8%EB%8A%94%20%EB%84%B7%EA%B3%BC%20VM%20%EC%9D%B4%20%EB%B0%9B%EB%8A%94%20%EB%8B%A4%EC%84%AF%20%ED%8C%8C%EC%9D%BC.md) | 부록 — 사이드카를 이루는 넷과 VM 이 받는 다섯 파일 (부록 B·E: 파드 주입·CNI·VM 설정 파일) | 완료 (draft) |
| [a0-03](./a0-03.%EB%B6%80%EB%A1%9D%20%E2%80%94%20%EC%8B%A0%EC%9B%90%EC%9D%84%20%EB%AC%B8%EC%84%9C%EB%A1%9C%20%EB%A7%8C%EB%93%9C%EB%8A%94%20%EB%84%A4%20%EA%B7%9C%EA%B2%A9.md) | 부록 — 신원을 문서로 만드는 네 규격 (부록 C: SPIFFE ID·SVID·부트스트랩·filter metadata) | 완료 (draft) |
| [a0-04](./a0-04.%EB%B6%80%EB%A1%9D%20%E2%80%94%20%ED%8F%AC%ED%8A%B8%20%EC%97%B4%EB%84%B7%EA%B3%BC%20%EB%94%94%EB%B2%84%EA%B7%B8%20%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8%20%EC%A7%80%EB%8F%84.md) | 부록 — 포트 열넷과 디버그 엔드포인트 지도 (부록 D: 사이드카 8·Pilot 6·ControlZ) | 완료 (draft) |

- 메시와 무관한 기초(관측·보안·K8s 네트워킹)는 각 편의 `## 이 문서가 다루지 않는 것`에서 인접 폴더에 위임합니다.
- 3~5장과 부록 4편(`03-01`~`05-01`·`a0-01`~`a0-04`)은 2026-11-25에 Istio 1.32 소스와 대조해 보강했습니다.



## 학습 상태

> 세션을 열 때 현재 진행 위치만 빠르게 확인하는 요약입니다. 챕터별 복습 상태 정본은 복습 대기 큐에 있습니다.

| 항목 | 현재 값 |
|------|--------|
| 진행률 | 본편 14/14장 + 부록 A~E 완주 — 정독 노트 18편(본편 14 · 부록 4, 전부 draft) |
| 현재 상태 | 난이도 `기본`. Phase 4 자답 미실시(면접 질문 139개 · 복습 회차 0 · `last_verified` 비움) |
| 다음 작업 | 18편 면접 질문 자답 뒤 막힌 자리를 `blocked_count`에, 회차 날짜를 `last_verified`에 기록 |
| 복습 큐 | [복습 대기 큐](../../../_review/_queue.md) (`istio` ch01~ch14) |



## 관련 문서

> 같은 영역의 형제 정독본, Istio 공식문서 정독, 장애 사례와 상위 인덱스입니다.

- [Istio 공식문서 정독](../../docs/istio/README.md) — Istio 1.32 기준 Ambient·xDS·iptables·시동 순서 보강
- [Istio 학습 문서 읽기 순서](../../../99_ETC/2026-11-27_Istio%20%ED%95%99%EC%8A%B5%20%EB%AC%B8%EC%84%9C%20%EC%9D%BD%EA%B8%B0%20%EC%88%9C%EC%84%9C.md) — 선행 문서·정독본·공식문서 통합 읽기 경로
- [mesh 트러블슈팅](../../../troubleshooting/mesh/README.md) — 커넥션 풀·서킷 브레이커 503 장애 사례
- [Networking and Kubernetes 정독 인덱스](../networking-and-kubernetes/README.md) — 커널·CNI·Service·Ingress 아래층 짝
- [Kubernetes in Action 정독 인덱스](../kubernetes-in-action/README.md) — 오브젝트 중심 관점의 짝
- [Kubernetes: Up and Running 정독 인덱스](../kubernetes-up-and-running/README.md) — 서비스 디스커버리·RBAC 기초 위임 대상
- [Container Security 정독 인덱스](../container-security/README.md) — 컨테이너 이미지·X.509·TLS 기초 위임 대상
- [06_observability MOC](../../../06_observability/README.md) — Prometheus·Grafana·Tempo 관측 기초 위임 대상
- [99_ETC/security MOC](../../../99_ETC/security/README.md) — 인증·인가·JWT·OIDC 기초 위임 대상
- [08_cloud MOC](../../README.md) — 상위 카테고리 경계

> 아래 세 자리는 정독 노트에 링크가 없어서 여기에만 남깁니다. 메시와 무관한 기초로 넘기는 지점입니다.

- 13장 준비성·생존성 프로브와 `iptables` 리디렉션은 [『Networking and Kubernetes』 4장](../networking-and-kubernetes/04-01.Kubernetes%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EB%AA%A8%EB%8D%B8%20%E2%80%94%20Pod%20IP%C2%B7%EB%A0%88%EC%9D%B4%EC%95%84%EC%9B%83%C2%B7Probe.md)이 맡습니다.
- 13장에서 서비스 디스커버리가 DNS 로 풀리지 않는 지점은 [『Kubernetes: Up and Running』 7장](../kubernetes-up-and-running/07-01.Service%20Discovery%20%E2%80%94%20DNS%EA%B0%80%20%EB%AA%BB%20%ED%95%98%EB%8A%94%20%EC%9D%BC%EA%B3%BC%20%EB%B0%94%EA%B9%A5%EC%9D%84%20%EC%9E%87%EB%8A%94%20%EB%B2%95.md)이 맡습니다.
- 14장에서 OCI 이미지의 층과 식별자는 [『Container Security』 6장](../container-security/06-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%ED%95%B4%EB%B6%80%20%E2%80%94%20%EB%91%90%20%EB%B6%80%EB%B6%84%EA%B3%BC%20%EC%B8%B5%EA%B3%BC%20%EC%8B%9D%EB%B3%84%EC%9E%90.md)이 맡습니다.
