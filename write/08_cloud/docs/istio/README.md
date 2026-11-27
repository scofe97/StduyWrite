---
title: 08_cloud/docs/istio — Istio 공식문서 정독
tags: [moc, istio, service-mesh, official-docs]
status: final
related:
  - ../README.md
  - ../../README.md
  - ../../book/istio-in-action/README.md
updated: 2026-11-25
---

# 08_cloud/docs/istio — Istio 공식문서 정독

---

> istio.io 공식문서를 1차 자료로 삼아 궁금한 주제만 한 편씩 파고드는 자리입니다. 전체 개념을 순서대로 훑는 일은 [book/istio-in-action/](../../book/istio-in-action/)의 정독 노트가 맡습니다.

## 폴더 규칙

> 문서는 폴더 바로 아래에 단독 편으로 두고, 파일명에는 번호를 붙이지 않습니다.

이 폴더의 문서는 처음부터 차례로 읽는 연재가 아닙니다. 궁금한 주제를 한 편씩 골라 읽으므로 파일명은 한글 문서 이름만으로 짓습니다. 다루는 대상이 둘 이상이면 `와/과` 대신 `·` 로 잇습니다. 제목에 ` — ` 로 붙은 부제는 파일명에서 뺍니다. 그래서 파일명과 H1 제목은 다를 수 있습니다.

아직 편 수가 적어 묶음 폴더 없이 폴더 바로 아래에 둡니다. 도식과 생성기는 문서 옆의 `_assets/` 에 두고, 생성기는 `_assets/_gen/` 에서 그 폴더의 `_assets/dd.py` 를 씁니다. 도식 센서(`dd-verify-all.sh`)가 문서 옆의 `_assets/` 만 보기 때문입니다.

공식 문서의 어느 페이지를 읽었는지는 프론트매터 `source` 가 맡습니다. 첫 줄에 1차 근거 페이지를 두어 공식 명세와의 연결을 유지합니다. istio.io 문서 주소에는 읽은 판을 `/v1.32/` 처럼 박습니다. 판 없는 `/latest/` 주소는 새 판이 나오면 내용이 바뀌거나 사라지기 때문입니다. 블로그 글은 주소에 날짜가 들어가 있어 판을 박지 않습니다.



## 문서 목록

> Istio 공식 문서 정독 편 목록입니다. 각 편이 다루는 핵심 주제를 요약합니다.

| 제목 | 한 줄 소개 |
|------|-----------|
| [Ambient 모드와 ztunnel·waypoint — 사이드카 없이 L4 와 L7 을 나눈 데이터 플레인](Ambient%20%EB%AA%A8%EB%93%9C%C2%B7ztunnel%C2%B7waypoint.md) | 사이드카 없이 L4 와 L7 을 두 층으로 나눈 데이터 플레인의 동작 원리와 ztunnel·waypoint 의 책임 경계를 봅니다. |
| [VirtualService 라우팅 — delegate·매치 순서·rewrite·redirect](VirtualService%20%EB%9D%BC%EC%9A%B0%ED%8C%85.md) | 라우트를 넘기는 `delegate`, 이기는 라우트를 정하는 매치 순서, 경로를 바꾸는 `rewrite` 와 `redirect` 를 봅니다. |
| [사이드카 시동·종료 순서 — holdApplicationUntilProxyStarts·네이티브 사이드카·terminationDrainDuration](%EC%82%AC%EC%9D%B4%EB%93%9C%EC%B9%B4%20%EC%8B%9C%EB%8F%99%C2%B7%EC%A2%85%EB%A3%8C%20%EC%88%9C%EC%84%9C.md) | 앱과 프록시의 시작 순서를 맞추는 두 방법과 종료 쪽 설정을 봅니다. |
| [사이드카 트래픽 가로채기와 iptables 체인](%EC%82%AC%EC%9D%B4%EB%93%9C%EC%B9%B4%20%ED%8A%B8%EB%9E%98%ED%94%BD%20%EA%B0%80%EB%A1%9C%EC%B1%84%EA%B8%B0%C2%B7iptables%20%EC%B2%B4%EC%9D%B8.md) | 파드를 드나드는 트래픽이 어느 iptables 체인을 지나 Envoy 15001·15006 에 닿는지, 무엇이 예외인지 봅니다. |
| [xDS 동기화 프로토콜](xDS%20%EB%8F%99%EA%B8%B0%ED%99%94%20%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C.md) | Istio 리소스가 xDS 로 바뀌어 Envoy 에 닿고, ACK·NACK 로 받아들여지는 과정을 봅니다. |
| [WasmPlugin 확장 — 선언적 Wasm 필터와 phase](WasmPlugin%20%ED%99%95%EC%9E%A5.md) | WasmPlugin 이 모듈을 받아 Envoy 필터 체인의 정해진 자리에 끼우는 과정과 필드를 봅니다. |



## 아직 안 쓴 주제

> 앞으로 다룰 공식 페이지입니다. 궁금한 주제부터 순서 없이 채워 갑니다.

- `Traffic Management — VirtualService and DestinationRule`
- `Security — AuthorizationPolicy and PeerAuthentication`
- `Gateways — Ingress Gateway and Gateway API integration`
- `Observability — Distributed Tracing and Telemetry API`



## 관련 문서

> 이 폴더가 딛고 서거나 이어지는 이웃입니다.

- [08_cloud MOC](../README.md) — 클라우드 인프라 대분류 지도
- [Istio in Action 정독 인덱스](../../book/istio-in-action/README.md) — 사이드카 기반 Istio 기초 이론과 동작 원리 정독 노트
- [쿠버네티스 공식문서 정독](../kubernetes/README.md) — 파드 네트워킹과 노드 런타임 아키텍처
