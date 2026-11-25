---
title: 02_os/docs/reverse-proxy — Nginx 와 HAProxy 리버스 프록시
tags: [moc, reverse-proxy, nginx, haproxy, official-docs]
status: draft
source:
  - https://nginx.org/en/docs/
  - https://docs.haproxy.org/2.8/configuration.html
related:
  - ../../README.md
  - ../../os-keywords.md
review:
  status: pending
updated: 2026-11-17
---

# 02_os/docs/reverse-proxy — Nginx 와 HAProxy 리버스 프록시
---
> 웹 서버이자 리버스 프록시인 Nginx 와 TCP·HTTP 프록시이자 로드밸런서인 HAProxy 는 인프라 앞단에서 같은 문제(헤더 전달, 타임아웃/버퍼링, 헬스체크, TLS 종료 및 인증서 체인)를 서로 다른 철학과 설정 모델로 해결합니다. 두 구현체를 나란히 놓고 비교할 때 설정 문법의 차이와 동작 메커니즘이 선명해집니다.

## 왜 주제 폴더로 묶는가

> docs 의 기본 규칙은 제품마다 폴더 하나지만 Nginx 와 HAProxy 는 인프라 경계에서 동일한 L7 리버스 프록시 역할을 분담하므로 나란히 비교할 때 원리가 가장 잘 드러납니다.

클라이언트와 백엔드 서버 사이에서 역방향 프록시가 수행하는 핵심 역할은 명확합니다. 클라이언트 식별 정보인 IP 와 프로토콜 및 호스트를 백엔드로 전달하는 일이 첫째입니다. 업스트림 연결 및 응답 기한을 관리하고 502·504 상태 코드를 생성하는 일이 둘째입니다. 여기에 백엔드 서버 건강 검사와 장애 격리, 그리고 TLS 핸드셰이크 종료와 인증서 체인 검증이 더해집니다.

Nginx 는 웹 서버의 설정 모델 위에서 프록시를 설정합니다. 지시어를 컨텍스트(http·server·location)에 적으며 하위 컨텍스트가 상위 정의를 물려받는 상속 규칙으로 동작합니다.

반면 HAProxy 는 프록시와 부하 분산 자체를 위한 설정 모델을 씁니다. 프런트엔드와 백엔드를 섹션으로 나누고 동작을 명시적인 규칙(`http-request`·`option`)으로 적습니다. 같은 네트워크 문제를 두 소프트웨어가 서로 다른 설정 어휘로 해결합니다. 그래서 제품별로 폴더를 쪼개기보다 주제 폴더 하나에서 나란히 다루는 편이 문제의 본질을 파악하기에 유리합니다.



## 문서 목록

> 01 번대는 Nginx 와 HAProxy 가 공통으로 다루는 프록시 핵심 메커니즘 연재입니다. 번호가 읽기 순서입니다.

| 번호 | 제목 | 핵심 내용 | 주 1차 자료 |
|---|---|---|---|
| 01-01 | [proxy_set_header·option forwardfor](./01-01.proxy_set_header·option%20forwardfor.md) | 클라이언트 원래 정보(IP, 프로토콜, 호스트)를 전달하는 설정, 상속 단절 주의점, 다중 프록시 신뢰 경계(`set_real_ip_from`) | Nginx `ngx_http_proxy_module`·`ngx_http_realip_module`, HAProxy `option forwardfor`, RFC 7239 |
| 01-02 | [proxy_read_timeout·client_max_body_size·timeout server](./01-02.proxy_read_timeout·client_max_body_size·timeout%20server.md) | 502 와 504 가 갈리는 지점, 업스트림 연결·응답 기한 초과가 504 를 만드는 과정(HAProxy `sH`·`sC`), 요청 본문 크기와 전송 시간 제한(413·408) | Nginx `ngx_http_proxy_module`·`ngx_http_core_module`·`ngx_http_upstream.c`, HAProxy `timeout`, RFC 9110 |
| 01-03 | [Health Checks·max_fails](./01-03.Health%20Checks·max_fails.md) | 프록시가 백엔드를 UP·DOWN 으로 판정하는 규칙, HAProxy 능동 검사(`check`·`inter`·`rise`·`fall`·`option httpchk`)와 Nginx 수동 판정(`max_fails`·`fail_timeout`), 장애 감지 시점 비교 | HAProxy `check`·`inter`·`fall`·`rise`·`option httpchk`, Nginx `ngx_http_upstream_module` server 매개변수·`ngx_http_upstream_round_robin.c` |
| 01-04 | [SSL certificate chains·crt](./01-04.SSL%20certificate%20chains·crt.md) | 서버 인증서와 중간 인증서를 한 파일에 잇는 순서와 순서가 틀렸을 때 생기는 일, TLS Certificate 목록 순서 규약, Nginx 결합 파일과 키 불일치 오류, HAProxy `crt` PEM 구성, `openssl s_client -showcerts` 확인 | Nginx Configuring HTTPS servers, HAProxy `crt`, RFC 8446 §4.4.2, OpenSSL `s_client` |



## 아직 안 쓴 주제

> 앞으로 쓸 후보입니다. 지금 연재는 Nginx 와 HAProxy 에 공통인 메커니즘만 다뤄서, HAProxy 설정 전체를 읽는 편이 없습니다.

- HAProxy 설정 구조 — `global`·`defaults`·`frontend`·`backend` 가 나눠 맡는 일
- HAProxy TCP 모드 — 쿠버네티스 API 서버(6443) 앞에 두는 L4 로드밸런싱



## 1차 자료

> 공식 문서와 표준 RFC 규격입니다. HAProxy 매뉴얼은 2.8 판으로 고정했고, nginx.org 문서는 판을 나눠 두지 않아 늘 최신 판을 가리킵니다.

### Nginx 공식 문서
- [Module ngx_http_proxy_module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html): `proxy_set_header`, `$proxy_add_x_forwarded_for`, `proxy_pass` 동작 규약
- [Module ngx_http_realip_module](https://nginx.org/en/docs/http/ngx_http_realip_module.html): `set_real_ip_from`, `real_ip_header`, `real_ip_recursive`
- [Module ngx_http_core_module](https://nginx.org/en/docs/http/ngx_http_core_module.html): `client_max_body_size`, 시간 제한
- [Configuring HTTPS servers](https://nginx.org/en/docs/http/configuring_https_servers.html): SSL 인증서 체인 구성

### HAProxy 공식 문서
- [HAProxy 2.8 Configuration Manual](https://docs.haproxy.org/2.8/configuration.html): `option forwardfor`, `http-request set-header`, `ssl_fc`, 건강 검사, 타임아웃 키워드

### 인터넷 표준 규약 (RFC)
- [RFC 7239: Forwarded HTTP Extension](https://www.rfc-editor.org/rfc/rfc7239): 프록시 경로 상의 전달 정보 표준 규격 및 신뢰 모델
- [RFC 8446: The Transport Layer Security (TLS) Protocol Version 1.3](https://www.rfc-editor.org/rfc/rfc8446): §4.4.2 Certificate 메시지 내 체인 순서 규약
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110): 게이트웨이 및 프록시 상태 코드(502 Bad Gateway, 504 Gateway Timeout 등)



## 관련 문서

> 프록시와 연계되는 네트워크 및 상위 문서입니다.

- [02_os/ MOC](../../README.md) — OS 공통 기반 및 네트워크
- [OS 학습 로드맵](../../os-keywords.md) — 네트워크 계층 및 소켓 통신
- [Ingress와 Service Mesh — L7의 두 층](../../../08_cloud/book/networking-and-kubernetes/05-03.Ingress와%20Service%20Mesh%20—%20L7의%20두%20층.md) — 인그레스 컨트롤러와 L7 프록시
