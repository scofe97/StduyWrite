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
  - ../../service-mesh/README.md
  - ../../service-mesh/03_istio/README.md
updated: 2026-08-11
---

# Istio in Action — 정독 인덱스

---

> 이 폴더는 『Istio in Action』(Christian E. Posta·Rinor Maloku, Manning)을 장 단위로 정독하며 정리하는 **책-종속 학습노트**입니다. 챕터 PDF를 하나씩 읽은 뒤 한 편씩 채워 넣습니다.

## 이 책을 여기 두는 이유

`08_cloud`는 클러스터 안에서 무엇이 어떻게 돌아가는지를 다루는 카테고리이고, 그 안에서 서비스 메시는 이미 [`service-mesh/`](../../service-mesh/README.md)가 맡고 있습니다. 이 책을 별도 폴더로 두는 이유는 주제가 새로워서가 아니라 **자료의 성격이 다르기 때문**입니다. 기존 `service-mesh/`는 직접 띄운 클러스터에서 얻은 실습 기록이고, 이 폴더는 저자가 왜 그렇게 설계했는지를 따라가는 정독 기록입니다.

같은 폴더의 [『Networking and Kubernetes』 정독본](../networking-and-kubernetes/README.md)이 패킷이 어떤 계층을 지나는지를 다룬다면, 이 책은 그 위에 프록시를 하나 더 얹었을 때 무엇을 얻고 무엇을 잃는지를 다룹니다. 저쪽이 커널과 CNI를 파고들고, 여기는 애플리케이션 계층 프록시의 설계 판단을 파고듭니다.

## 기존 `service-mesh/03_istio`와의 경계

이 폴더를 열기 전에 이미 [`service-mesh/03_istio/`](../../service-mesh/03_istio/README.md)에 Istio 문서 22편이 있습니다. 그쪽은 개인 GCP 클러스터 실습에서 나온 자체 기록이고, 주제 구성이 이 책과 거의 1:1로 겹칩니다. 4장은 Ingress Gateway, 5장은 트래픽 관리, 6장은 레질리언스, 9장은 보안, 10장은 트러블슈팅, 11장은 성능 튜닝, 14장은 EnvoyFilter로 대응합니다.

그래서 이 정독본은 **겹치는 개념을 다시 쓰지 않습니다.** 다음 규칙으로 가릅니다.

- `03_istio`가 SSOT인 것: CRD 필드, `istioctl` 명령, xDS 동작, 실습 절차. 정독본에서 필요하면 링크로 넘깁니다.
- 정독본이 SSOT인 것: 저자의 설계 논지, 대안 기술과의 비교, 그 기능이 없던 시절의 문제, 저자가 명시한 트레이드오프와 한계.

판별 기준은 하나입니다. **"이 문장이 Istio를 쓸 줄 아는 사람에게도 새로운가."** 새롭지 않으면 링크로 넘기고, 새로우면 여기 남깁니다.

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

| 장 | 노트 | 한 줄 핵심 | 상태 |
|----|------|-----------|------|
| 1 | [서비스 메시는 무엇을 인프라로 밀어냈는가](01-01.서비스%20메시는%20무엇을%20인프라로%20밀어냈는가.md) | 애플리케이션 네트워킹을 라이브러리에서 프록시로 옮긴 결정과 그 대가 | 작성 완료 |
| 2 | [배포와 릴리스를 가르는 첫 실습](02-01.배포와%20릴리스를%20가르는%20첫%20실습.md) | 코드를 올리는 일과 트래픽을 흘리는 일은 다른 사건이다 | 작성 완료 |
| 3~14 | | | 미작성 |

## 학습 상태

| 항목 | 값 |
|------|-----|
| 난이도 레벨 | 1~2장은 개론·실습이라 낮음. Istio 사용 경험이 이미 있어 개념 자체는 익숙 |
| 막힌 지점 | 없음 |
| 다음 레슨 후보 | 3장 Envoy — `03_istio`가 xDS를 다루지만 독립 실행 Envoy·정적 설정·Admin API는 다루지 않아 겹침이 가장 적음 |
| 최근 검증 결과 | 2장 센서 전수 통과, 원문 대조 완료 (2026-08-12). 1장은 해석 문장 2건 교정 후 재통과 |
| 복습 회차 | 0 |

`03_istio` 22편과 겹치는 주제는 정독본에서 되풀이하지 않고 링크로 넘깁니다. 2장처럼 실습 비중이 큰 장은 `## 이 문서가 다루지 않는 것` 절에 위임 대상을 명시합니다.

## 출처와 톤 메모

원문 PDF가 1차 자료입니다. 사실·수치·인용은 `pdftotext`로 추출한 본문에서만 가져오고, 책 밖 보강은 `## 심화 학습`으로 분리해 공식 1차 링크를 답니다.

이 책은 저자가 Solo.io·Red Hat에서 Istio를 실제로 운영한 경험을 배경에 깔고 씁니다. 그래서 기능 나열보다 "왜 이 설계인가"와 "언제 쓰지 말아야 하는가"가 강한데, 정독본에서는 그 판단 부분을 우선 남깁니다.

톤은 합니다체로 통일합니다.
