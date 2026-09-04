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
learning:
  topic: istio-in-action
  scope: durable
  level: 기본
  last_verified:            # Phase 4 자답·_review 회차 미실시 — 원문 대조일로 대신 채우지 않음
  blocked_count:
  next_lesson: "부록 A 완료. 다음은 B+E 한 편(사이드카 구성과 VM 설정 파일) — 둘 다 데이터 플레인이 설정을 받는 경로라 한 축으로 묶인다. 그다음 C(SPIFFE), D(포트·디버그 엔드포인트 지도)"
updated: 2026-09-02
---

# Istio in Action — 정독 인덱스

---

> 이 폴더는 『Istio in Action』(Christian E. Posta·Rinor Maloku, Manning)을 장 단위로 정독하며 정리하는 **책-종속 학습노트**입니다. 챕터 PDF를 하나씩 읽은 뒤 한 편씩 채워 넣습니다.

## 이 책을 여기 두는 이유

> 같은 주제를 다루던 폴더가 이미 있었고, 이 폴더를 따로 둔 이유는 주제가 아니라 자료의 성격이었습니다.

`08_cloud`는 클러스터 안에서 무엇이 어떻게 돌아가는지를 다루는 카테고리입니다. 이 폴더를 처음 열 때는 그 안의 `service-mesh/`가 서비스 메시를 맡고 있었고, 이 책을 따로 둔 이유도 주제가 새로워서가 아니라 자료의 성격이 달라서였습니다. 그쪽은 직접 띄운 클러스터의 실습 기록이었고 이 폴더는 저자가 왜 그렇게 설계했는지를 따라가는 정독 기록입니다.

같은 폴더의 [『Networking and Kubernetes』 정독본](../networking-and-kubernetes/README.md)이 패킷이 어떤 계층을 지나는지를 다룬다면, 이 책은 그 위에 프록시를 하나 더 얹었을 때 무엇을 얻고 무엇을 잃는지를 다룹니다. 저쪽이 커널과 CNI를 파고들고, 여기는 애플리케이션 계층 프록시의 설계 판단을 파고듭니다.



## 기존 `service-mesh/03_istio`와의 경계

> 넘기던 폴더가 지워졌으므로 위임 규칙을 다시 세웁니다. 판별 기준은 "Istio 를 쓸 줄 아는 사람에게도 새로운가" 하나입니다.

**그 폴더는 이제 없습니다.** `08_cloud/service-mesh/` 213편은 2026-08-17 커밋 `74b90d3`에서 사용자 확인을 거쳐 지워졌습니다. 그중 `03_istio/`가 Istio 문서 22편으로 이 책과 주제가 거의 1:1로 겹치던 쪽이었고, 1·2장이 CRD 필드와 실습 절차를 그쪽으로 넘기고 있었습니다.

그래서 위임 규칙을 다시 세웁니다.

- 이 폴더 안에서 해결합니다. `istiod`와 xDS는 3장, 게이트웨이는 4장, 트래픽 관리는 5장, 레질리언스는 6장, 메트릭은 7장, 시각화와 추적은 8장, 보안은 9장이 SSOT입니다.
- 이 폴더 밖으로 넘기는 것은 **책과 무관하게 존재하는 기초**뿐입니다. 관측 도구는 `06_observability`, 보안 기초는 `99_ETC/security`와 같은 폴더의 다른 정독본이 맡습니다.
- 지워진 노트로 넘기던 자리 중 대체가 없던 것은 원문에서 직접 채웠습니다. 2장 §1의 설치 절이 그 경우입니다.

판별 기준은 그대로입니다. **"이 문장이 Istio를 쓸 줄 아는 사람에게도 새로운가."** 새롭지 않으면 링크로 넘기고, 새로우면 여기 남깁니다.

관측성을 다루는 7·8장에는 경계가 하나 더 생깁니다. `write/06_observability/`에 마크다운 문서 86개가 있고 그중 `mastering_prometheus` 정독본 본편만 24편입니다. 그래서 다음은 그쪽이 SSOT 이고 정독본은 링크로 넘깁니다.

- 관측 가능성의 정의와 Prometheus 의 pull 방식
- Operator 와 `ServiceMonitor`·`PodMonitor` 리소스 자체
- `relabelings` 문법과 PromQL
- 골든 시그널

여기 남기는 것은 **메시가 있어야만 생기는 이야기**입니다. 프록시가 요청 경로에 앉아 있어서 셀 수 있는 것, 기본으로 감춰 둔 것, 그리고 애플리케이션 코드를 건드리지 않고 세는 축을 바꾸는 방법입니다.

8장에는 같은 경계가 한 겹 더 붙습니다. 넘기는 자리는 셋입니다.

- 스팬·트레이스의 정의와 전파 헤더 네 형식: `02_LGTMStack/02-04.Grafana Tempo.md` 와 `book/observability_with_grafana/06-01.Tempo 와 TraceQL`
- 대시보드 JSON 모델과 프로비저닝: `02_LGTMStack/02-01.Grafana Core.md`
- 트레이스를 뒤져 병목을 찾는 작업 순서: `03_Project/03-08.Tempo 분산 트레이싱 시각화.md`

그래서 8장 노트가 남긴 것은 사이드카가 코드 없이 붙여 주는 헤더, 그럼에도 애플리케이션이 해야 하는 전파, 그 몫을 조절하는 설정 자리, 그리고 메시의 리소스를 아는 화면입니다.

9장에도 경계가 하나 더 생깁니다. 인증과 인가, JWT 설계, OAuth2·OIDC 는 `write/99_ETC/security/01_concepts/` 가 SSOT 입니다. X.509 와 CA 는 같은 폴더의 [『Container Security』 11장](../container-security/11-01.TLS%EB%A1%9C%20%EC%BB%B4%ED%8F%AC%EB%84%8C%ED%8A%B8%20%EC%95%88%EC%A0%84%ED%95%98%EA%B2%8C%20%EC%97%B0%EA%B2%B0%ED%95%98%EA%B8%B0%20%E2%80%94%20%ED%82%A4%C2%B7%EC%9D%B8%EC%A6%9D%EC%84%9C%C2%B7CA%EC%9D%98%20%EC%97%AD%ED%95%A0.md)이, 쿠버네티스 자체의 인가는 [『Kubernetes Up and Running』 14장](../kubernetes-up-and-running/14-01.RBAC%20%E2%80%94%20%EC%9D%B8%EA%B0%80%EB%A5%BC%20%EC%84%A4%EA%B3%84%ED%95%98%EA%B3%A0%20%EC%9A%B4%EC%98%81%ED%95%98%EB%8A%94%20%EB%B2%95.md)이 갖습니다. 저자 자신이 9.1 을 "간단한 복습"이라 부르고 상세를 부록 C 로 넘기므로, 정독본도 같은 자리에서 넘기고 메시가 있어야만 생기는 이야기만 남깁니다.

10장은 도구를 여럿 부르지만 그 도구 자체는 다른 폴더가 갖고 있습니다. PromQL 질의 문법과 Grafana 대시보드 모델은 `06_observability` 가 SSOT 입니다. TCP 의 3방향 핸드셰이크와 `tcpdump`·Wireshark 실습은 같은 폴더의 [『Networking and Kubernetes』 정독본](../networking-and-kubernetes/README.md)이 갖습니다. 저자 스스로 ksniff 절을 연습이 목적이라 밝히므로 정독본도 그 무게로 둡니다. 여기 남기는 것은 프록시가 들고 있는 설정과 로그를 사람이 읽을 크기로 줄이는 방법입니다.

11장도 지표를 많이 부르지만 그 지표의 문법은 다른 폴더가 갖습니다. 골든 시그널 넷의 정의는 `06_observability/01_Foundations` 가 SSOT 이고, PromQL 과 Prometheus 스택 구성은 `mastering_prometheus` 정독본이 SSOT 입니다. 여기 남기는 것은 istiod 가 일을 덜 하게 만드는 손잡이와 그 순서입니다.

1. `Sidecar` 로 설정 크기를 깎는다
2. 발견 범위를 좁힌다
3. 이벤트를 묶는다
4. 마지막에 자원을 늘린다

12장은 여러 클러스터를 하나의 메시로 묶는 장이라 다른 폴더의 기초를 여럿 빌려 씁니다. 서비스 어카운트와 롤 같은 쿠버네티스 인가는 같은 폴더의 [『Kubernetes Up and Running』 14장](../kubernetes-up-and-running/14-01.RBAC%20%E2%80%94%20%EC%9D%B8%EA%B0%80%EB%A5%BC%20%EC%84%A4%EA%B3%84%ED%95%98%EA%B3%A0%20%EC%9A%B4%EC%98%81%ED%95%98%EB%8A%94%20%EB%B2%95.md)이 SSOT 이고, X.509 와 중간 CA 는 [『Container Security』 11장](../container-security/11-01.TLS%EB%A1%9C%20%EC%BB%B4%ED%8F%AC%EB%84%8C%ED%8A%B8%20%EC%95%88%EC%A0%84%ED%95%98%EA%B2%8C%20%EC%97%B0%EA%B2%B0%ED%95%98%EA%B8%B0%20%E2%80%94%20%ED%82%A4%C2%B7%EC%9D%B8%EC%A6%9D%EC%84%9C%C2%B7CA%EC%9D%98%20%EC%97%AD%ED%95%A0.md)이 갖습니다. 저자 자신이 RBAC 을 "이 책의 범위 밖"이라 적으므로 정독본도 같은 자리에서 넘깁니다. 여기 남기는 것은 클러스터 경계를 메시가 어떻게 덮는가, 그리고 어디서 덮지 못하는가입니다.

13장은 쿠버네티스 밖으로 나가는 장이라 플랫폼 기초를 여럿 빌려 씁니다. `Deployment` 와 `Pod` 의 관계, 준비성·생존성 프로브의 기본 동작은 같은 폴더의 [『Networking and Kubernetes』 4장](../networking-and-kubernetes/04-01.Kubernetes%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EB%AA%A8%EB%8D%B8%20%E2%80%94%20Pod%20IP%C2%B7%EB%A0%88%EC%9D%B4%EC%95%84%EC%9B%83%C2%B7Probe.md)가 SSOT 이고, `iptables` 리디렉션과 클러스터 안의 이름 해석도 그 정독본이 갖습니다. 서비스 디스커버리가 DNS 로 풀리지 않는 지점은 [『Kubernetes Up and Running』 7장](../kubernetes-up-and-running/07-01.Service%20Discovery%20%E2%80%94%20DNS%EA%B0%80%20%EB%AA%BB%20%ED%95%98%EB%8A%94%20%EC%9D%BC%EA%B3%BC%20%EB%B0%94%EA%B9%A5%EC%9D%84%20%EC%9E%87%EB%8A%94%20%EB%B2%95.md)이 맡습니다.

저자 자신이 생성된 설정 파일의 내부를 부록 E 로, 사이드카 주입 방식을 부록 B 로 넘기므로 정독본도 같은 자리에서 멈춥니다. 여기 남기는 것은 플랫폼이 대신해 주던 여섯 가지를 손으로 옮길 때 무엇이 드러나는가입니다.

14 장은 Envoy 안으로 한 겹 더 들어가지만 그 아래의 기초는 다른 정독본이 갖습니다. HTTP/1.1 과 HTTP/2, 그 아래 전송 계층은 같은 폴더의 [『Networking and Kubernetes』 정독본](../networking-and-kubernetes/README.md)이 SSOT 이고, OCI 이미지의 층과 식별자는 [『Container Security』 6장](../container-security/06-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%ED%95%B4%EB%B6%80%20%E2%80%94%20%EB%91%90%20%EB%B6%80%EB%B6%84%EA%B3%BC%20%EC%B8%B5%EA%B3%BC%20%EC%8B%9D%EB%B3%84%EC%9E%90.md)이 갖습니다. 저자 자신이 C++ 로 네이티브 필터를 쓰는 일을 "이 책의 범위 밖" 이라 적고 타임아웃과 재시도의 동작은 6 장과 Envoy 문서로 넘기므로, 정독본도 같은 자리에서 멈춥니다. 여기 남기는 것은 확장의 문 넷이 각각 무엇을 대신 요구하는가입니다.



## 파트 구조

> 파트 디바이더 PDF 3편의 저자 서술에서 옮겼습니다. 파트 1은 디바이더 PDF가 없어 빈칸입니다.

| 파트 | 제목 | 저자가 밝힌 범위 |
|------|------|-----------------|
| 1 | (디바이더 PDF 없음) | 1~3장 — 서비스 메시 개념, 설치 첫걸음, Envoy |
| 2 | Securing, observing, and controlling your service's network traffic | 4~9장 — ingress에서 콜 그래프 깊숙한 곳까지의 트래픽 처리 |
| 3 | Istio day-2 operations | 10~11장 — 데이터 플레인 문제 해결과 컨트롤 플레인 안정성·성능 유지 |
| 4 | Istio in your organization | 12~14장 — 규모 확장, 멀티 클러스터·VM, Wasm 등으로 메시 동작 커스터마이즈 |



## 장별 목표

> 각 장 PDF 앞머리의 저자 선언("This chapter covers")을 그대로 옮겼습니다. 원문에 없는 목표를 추측해 넣지 않습니다.

| 장 | 제목 | 저자가 선언한 목표 | 주요 토픽 |
|----|------|------------------|----------|
| 1 | Introducing the Istio service mesh | 서비스 메시로 SOA의 과제를 다루고, Istio가 마이크로서비스 문제를 어떻게 푸는지 소개하며, 서비스 메시를 앞선 기술들과 비교 | 서비스 메시 정의, 데이터·컨트롤 플레인, ESB·API 게이트웨이 비교 |
| 2 | First steps with Istio | Kubernetes에 Istio 설치, 컨트롤 플레인 컴포넌트 이해, Istio 프록시와 함께 앱 배포, VirtualService로 트래픽 제어, 추적·메트릭·시각화 보조 컴포넌트 탐색 | 설치, VirtualService 첫 사용 |
| 3 | Istio's data plane: The Envoy proxy | 독립 실행 Envoy와 그것이 Istio에 기여하는 바, Envoy 기능이 서비스 메시의 핵심인 이유, 정적 설정으로 Envoy 구성, Admin API로 들여다보고 디버깅 | Envoy 단독 사용, 정적 설정, Admin API |
| 4 | Istio gateways: Getting traffic into a cluster | 클러스터 진입점 정의, ingress 트래픽을 클러스터 내 배포로 라우팅, ingress 트래픽 보안, HTTP/S 아닌 트래픽 라우팅 | Gateway 리소스, TLS, TCP 트래픽 |
| 5 | Traffic control: Fine-grained traffic routing | 트래픽 라우팅 기초, 새 릴리스 중 트래픽 전환, 미러링으로 릴리스 위험 축소, 클러스터를 떠나는 트래픽 제어 | 가중치 라우팅, 미러링, egress 제어 |
| 6 | Resilience: Solving application networking challenges | 레질리언스의 중요성 이해, 클라이언트 사이드 로드밸런싱 활용, 요청 타임아웃·재시도 구현, 서킷 브레이킹과 커넥션 풀링, 레질리언스용 애플리케이션 라이브러리에서 이전 | 타임아웃·재시도, 서킷 브레이킹, 라이브러리 이전 |
| 7 | Observability: Understanding the behavior of your services | 기본 요청 수준 메트릭 수집, Istio 표준 서비스 간 메트릭 이해, Prometheus로 워크로드·컨트롤 플레인 메트릭 스크랩, Prometheus 추적용 신규 메트릭 추가 | 메트릭, Prometheus 연동 |
| 8 | Observability: Visualizing network behavior with Grafana, Jaeger, and Kiali | Grafana로 메트릭 시각 관찰, Jaeger로 분산 추적 계측, Kiali로 네트워크 콜 그래프 시각화 | Grafana, Jaeger, Kiali |
| 9 | Securing microservice communication | 서비스 메시에서 서비스 간 인증·인가 처리, 최종 사용자 인증·인가 처리 | mTLS, 인가 정책, 최종 사용자 인증 |
| 10 | Troubleshooting the data plane | 잘못 설정된 워크로드 문제 해결, istioctl·Kiali로 설정 오류 탐지·예방, istioctl로 서비스 프록시 설정 조사, Envoy 로그 해석, 텔레메트리로 앱 인사이트 확보 | istioctl 진단, Envoy 로그 |
| 11 | Performance-tuning the control plane | 컨트롤 플레인 성능 요인 이해, 성능 모니터링 방법, 핵심 성능 메트릭, 성능 최적화 방법 이해 | xDS 부하, 성능 메트릭, 최적화 |
| 12 | Scaling Istio in your organization | 다중 클러스터로 메시 확장, 두 클러스터 연결의 전제조건 해결, 서로 다른 클러스터 워크로드 간 공통 신뢰 수립, 클러스터 간 워크로드 디스커버리, east-west 트래픽용 ingress 게이트웨이 구성 | 멀티 클러스터, 공통 신뢰, east-west 게이트웨이 |
| 13 | Incorporating virtual machine workloads into the mesh | 레거시 워크로드를 메시에 편입, VM에 istio-agent 설치·구성, VM용 아이덴티티 프로비저닝, 클러스터 서비스를 VM에 노출하고 그 역방향도, 로컬 DNS 프록시로 클러스터 서비스 FQDN 해석 | VM 워크로드, istio-agent, DNS 프록시 |
| 14 | Extending Istio on the request path | Envoy 필터 이해, Istio EnvoyFilter 리소스로 Envoy 직접 설정, Lua로 요청 경로 커스터마이즈, WebAssembly로 요청 경로 커스터마이즈 | EnvoyFilter, Lua, Wasm |

부록 5편(A 설치 커스터마이징, B 사이드카 주입 옵션, C SPIFFE, D 컴포넌트 트러블슈팅, E VM 메시 조인 구성)도 PDF로 보유하고 있습니다. 본편 정독을 마친 뒤 필요한 것만 선별합니다.



## 작성된 정독 노트

> 장 하나에 노트 하나씩 채워 갑니다. 아래 표가 진도의 정본입니다.

| 장 | 노트 | 한 줄 핵심 | 상태 |
|----|------|-----------|------|
| 1 | [서비스 메시는 무엇을 인프라로 밀어냈는가](01-01.서비스%20메시는%20무엇을%20인프라로%20밀어냈는가.md) | 애플리케이션 네트워킹을 라이브러리에서 프록시로 옮긴 결정과 그 대가 | 작성 완료 |
| 2 | [배포와 릴리스를 가르는 첫 실습](02-01.배포와%20릴리스를%20가르는%20첫%20실습.md) | 코드를 올리는 일과 트래픽을 흘리는 일은 다른 사건이다 | 작성 완료 |
| 3 | [Envoy가 맡는 일과 Istio가 보태는 일](03-01.Envoy가%20맡는%20일과%20Istio가%20보태는%20일.md) | Istio 기능의 대부분은 Envoy가 하고, Istio는 그 Envoy 무리를 부양하는 인프라다 | 작성 완료 |
| 4 | [문을 여는 일과 길을 내는 일을 가른다](04-01.문을%20여는%20일과%20길을%20내는%20일을%20가른다.md) | 진입점에서 L4·L5(Gateway)와 L7(VirtualService)을 다른 리소스로 가른 이유 | 작성 완료 |
| 5 | [위험에 노출되는 트래픽을 줄여 가는 순서](05-01.위험에%20노출되는%20트래픽을%20줄여%20가는%20순서.md) | 다크 런치 → 가중치 → 미러링으로 새 코드가 해칠 수 있는 실사용자 트래픽의 몫을 줄인다 | 작성 완료 |
| 6 | [실패를 견디는 일을 프록시로 옮겼을 때](06-01.실패를%20견디는%20일을%20프록시로%20옮겼을%20때.md) | 레질리언스 설정은 실패의 비용을 옮길 뿐이라 옮긴 곳을 숫자로 봐야 한다 | 작성 완료 |
| 7 | [미리 정하지 않았던 것을 나중에 세려면](07-01.미리%20정하지%20않았던%20것을%20나중에%20세려면.md) | 무엇을 셀지가 배포 시점에 굳지 않게 남겨 두는 것이 관측 가능성의 요구다 | 작성 완료 |
| 8 | [메시가 절반까지만 해 주는 일](08-01.%EB%A9%94%EC%8B%9C%EA%B0%80%20%EC%A0%88%EB%B0%98%EA%B9%8C%EC%A7%80%EB%A7%8C%20%ED%95%B4%20%EC%A3%BC%EB%8A%94%20%EC%9D%BC.md) | 프록시는 스팬을 만들지만 트레이스를 잇는 헤더 전파는 애플리케이션의 몫으로 남는다 | 작성 완료 |
| 9 | [거의 안전한 기본값을 닫아 가는 순서](09-01.%EA%B1%B0%EC%9D%98%20%EC%95%88%EC%A0%84%ED%95%9C%20%EA%B8%B0%EB%B3%B8%EA%B0%92%EC%9D%84%20%EB%8B%AB%EC%95%84%20%EA%B0%80%EB%8A%94%20%EC%88%9C%EC%84%9C.md) | 신원을 문서로 옮기면 프록시가 판정할 수 있지만, 허용을 하나 적는 순간 기본값이 거부로 뒤집힌다 | 작성 완료 |
| 10 | [프록시는 다 알고 있고 사람은 못 읽는다](10-01.%ED%94%84%EB%A1%9D%EC%8B%9C%EB%8A%94%20%EB%8B%A4%20%EC%95%8C%EA%B3%A0%20%EC%9E%88%EA%B3%A0%20%EC%82%AC%EB%9E%8C%EC%9D%80%20%EB%AA%BB%20%EC%9D%BD%EB%8A%94%EB%8B%A4.md) | 진단 도구가 여럿인 것은 기능이 달라서가 아니라 의심 범위를 좁히는 단계가 달라서다 | 작성 완료 |
| 11 | [컨트롤 플레인의 성능은 낡은 설정의 수명이다](11-01.%EC%BB%A8%ED%8A%B8%EB%A1%A4%20%ED%94%8C%EB%A0%88%EC%9D%B8%EC%9D%98%20%EC%84%B1%EB%8A%A5%EC%9D%80%20%EB%82%A1%EC%9D%80%20%EC%84%A4%EC%A0%95%EC%9D%98%20%EC%88%98%EB%AA%85%EC%9D%B4%EB%8B%A4.md) | 성능 문제는 데이터 플레인이 옛 설정으로 도는 시간이고, 손잡이는 일을 줄이는 것부터 순서가 있다 | 작성 완료 |
| 12 | [경계를 지우는 전제 셋과 남는 한 자리](12-01.%EA%B2%BD%EA%B3%84%EB%A5%BC%20%EC%A7%80%EC%9A%B0%EB%8A%94%20%EC%A0%84%EC%A0%9C%20%EC%85%8B%EA%B3%BC%20%EB%82%A8%EB%8A%94%20%ED%95%9C%20%EC%9E%90%EB%A6%AC.md) | 발견·연결·공통 신뢰만 채우면 기능은 클러스터 경계를 모르고, 원격 안의 분산 하나만 예외로 남는다 | 작성 완료 |
| 13 | [자동으로 되던 일이 목록이 되어 나타난다](13-01.%EC%9E%90%EB%8F%99%EC%9C%BC%EB%A1%9C%20%EB%90%98%EB%8D%98%20%EC%9D%BC%EC%9D%B4%20%EB%AA%A9%EB%A1%9D%EC%9D%B4%20%EB%90%98%EC%96%B4%20%EB%82%98%ED%83%80%EB%82%9C%EB%8B%A4.md) | 쿠버네티스가 말없이 해 주던 여섯 가지가 VM 에서는 사람의 목록이 되고, 그중 이름 해석이 없으면 트래픽은 나가지도 못한다 | 작성 완료 |
| 14 | [Envoy를 새로 빌드하지 않으려고 낸 네 개의 문](14-01.Envoy%EB%A5%BC%20%EC%83%88%EB%A1%9C%20%EB%B9%8C%EB%93%9C%ED%95%98%EC%A7%80%20%EC%95%8A%EC%9C%BC%EB%A0%A4%EA%B3%A0%20%EB%82%B8%20%EB%84%A4%20%EA%B0%9C%EC%9D%98%20%EB%AC%B8.md) | 확장의 방법 넷은 기능이 아니라 커스텀 Envoy 빌드를 피한 대가로 갈린다 | 작성 완료 |
| A | [부록 — 설치를 고르는 API 와 프로파일 여덟](a0-01.%EB%B6%80%EB%A1%9D%20%E2%80%94%20%EC%84%A4%EC%B9%98%EB%A5%BC%20%EA%B3%A0%EB%A5%B4%EB%8A%94%20API%20%EC%99%80%20%ED%94%84%EB%A1%9C%ED%8C%8C%EC%9D%BC%20%EC%97%AC%EB%8D%9F.md) | 설치 도구 넷 중 셋은 같은 Helm 템플릿 위에 서고, 갈리는 것은 값을 넣기 전에 무엇이 검사하느냐다 | 작성 완료 |



## 학습 상태

> 난이도·막힌 지점·다음 후보·최근 검증을 한 표에 모읍니다. 편을 하나 마칠 때마다 갱신합니다.

| 항목 | 값 |
|------|-----|
| 난이도 레벨 | 기본. 3장 Envoy 단독 설정·Admin API, 4장 SNI 패스스루·게이트웨이 주입, 7장 stats·attribute-gen 플러그인과 CEL 표현식, 8장 `bootstrapOverride` 와 Kiali 오퍼레이터, 9장 SPIFFE·인가 규칙의 AND·OR 결합과 ExtAuthz, 10장 `proxy-config` 체인 질의와 Envoy 로거 스코프, 11장 디바운스·스로틀 환경변수와 `Sidecar` 스코프, 12장 SNI 클러스터와 `sni-dnat`·`AUTO_PASSTHROUGH`, 13장 `WorkloadGroup`·`WorkloadEntry` 와 로컬 DNS 프록시·NDS, 14장 `EnvoyFilter` 의 패치 좌표와 Wasm ABI·`WasmPlugin` 이 새 재료였고 Gateway·VirtualService·TLS 종료·Prometheus 스크랩·분산 추적·인증과 인가의 기초는 이미 익숙 |
| 막힌 지점 | 없음 |
| 다음 레슨 후보 | **본편 14장 + 부록 A 완주.** 부록은 넷이 남았다. 다음은 B+E 를 한 편으로 — 사이드카를 이루는 넷(B)과 VM 이 받는 다섯 파일(E)은 둘 다 데이터 플레인이 설정을 받는 경로라 한 축에 놓인다. 그다음이 C(SPIFFE), 마지막이 D(포트·디버그 엔드포인트 지도)다. A·D 를 2장·10장에 흡수하려던 앞의 계획은 원문을 읽고 접었다 — A 는 프로파일 여덟과 리소스 분리 절차를, D 는 포트 열일곱과 엔드포인트 목록을 담아 본문에 녹이면 둘 다 흐려진다 |
| 최근 검증 결과 | 부록 A §1 검사·벽 단락 0곳 통과, 도식 7장(타입 7종 — `dependency`·`layers`·`tree`·`flowchart`·`state`·`quadrant`·`process`) 본문 폭 800px 렌더로 전수 확인, 원문 식별자 33개 대조 일치 (2026-09-04). 눈 확인에서 넷을 고쳤다 — `profile-map` 의 버스가 계보 밖 루트 셋 밑을 지나 그 셋도 default 계열로 보이던 것, `operator-name` 의 전이 라벨 마스크가 상태 상자 변을 파먹던 것, `install-paths` 의 팬인 배지가 그려진 화살표 수와 어긋나던 것, `split-install` 의 산문이 끝 타원에 붙던 것. 14장 §1 검사·벽 단락 0곳 통과, 도식 9장(타입 9종 — `pyramid`·`uml-class` 첫 사용) 렌더 확인, 절 서사 골격 검출 0곳, 원문 식별자 108개 대조 일치 (2026-09-02). 자체 적대적 점검에서 셋을 고쳤다 — `WasmPlugin` 도식이 모듈을 당겨 오는 주체를 컨트롤 플레인으로 그린 것(원문은 프록시가 직접 내려받는다), `EnvoyFilter` 를 13장 리소스라 적은 것, 그리고 저자가 하지 않은 "라스트 마일은 대개 첫째·둘째 문에서 끝난다"는 분류. 13장도 같은 방식으로 셋을 고쳤고 10~12장은 서브에이전트 적대적 검증으로 각각 6·6·11건을 고쳤다. 1~9장까지 같은 게이트를 통과했다. Phase 4 자답은 아직 없어 `learning.last_verified` 비움 |
| 복습 회차 | 0 |

`03_istio` 22편과 겹치는 주제는 정독본에서 되풀이하지 않고 링크로 넘깁니다. 2장처럼 실습 비중이 큰 장은 `## 이 문서가 다루지 않는 것` 절에 위임 대상을 명시합니다.



## 출처와 톤 메모

원문 PDF가 1차 자료입니다. 사실·수치·인용은 `pdftotext`로 추출한 본문에서만 가져오고, 책 밖 보강은 `## 심화 학습`으로 분리해 공식 1차 링크를 답니다.

이 책은 저자가 Solo.io·Red Hat에서 Istio를 실제로 운영한 경험을 배경에 깔고 씁니다. 그래서 기능 나열보다 "왜 이 설계인가"와 "언제 쓰지 말아야 하는가"가 강한데, 정독본에서는 그 판단 부분을 우선 남깁니다.

톤은 합니다체로 통일합니다.
