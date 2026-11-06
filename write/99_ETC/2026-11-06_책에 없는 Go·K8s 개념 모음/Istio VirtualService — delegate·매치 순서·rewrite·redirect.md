---
title: "Istio VirtualService — delegate·매치 순서·rewrite·redirect"
tags: [istio, virtualservice, delegate, rewrite, redirect, routing]
status: draft
source:
  - https://istio.io/v1.27/docs/reference/config/networking/virtual-service/
updated: 2026-11-06
---

# Istio VirtualService — delegate·매치 순서·rewrite·redirect

---

> 임시 참고 문서 — 정본은 나중에 따로 만듭니다.

VirtualService 의 `http` 라우트를 쓸 때 헷갈리는 세 가지를 모았습니다. 한 VirtualService 의 라우트를 다른 VirtualService 에 넘기는 `delegate`, 어느 라우트가 이기는지를 정하는 매치 순서, 경로를 바꾸는 두 방법인 `rewrite` 와 `redirect` 입니다. 근거는 모두 Istio 공식 VirtualService 레퍼런스 한 페이지이고, 클러스터에서 적용해 본 것은 아닙니다. 한계는 문서 끝에 적었습니다.

## 1. delegate 로 라우트 나눠 맡기기

> root VirtualService 가 경로별로 라우트를 다른 VirtualService 에 넘기면, 팀마다 자기 경로의 라우팅만 따로 관리할 수 있습니다. 대신 제약이 몇 가지 있습니다.

### 어떤 문제가 생기나

하나의 호스트 뒤에 여러 팀의 서비스가 붙으면 VirtualService 한 개에 모든 경로 규칙이 쌓입니다. 한 팀이 규칙을 고치려면 다른 팀이 함께 쓰는 리소스를 편집해야 하고, 실수 하나가 전체 라우팅을 깨뜨립니다.

### 동작 원리

root VirtualService 는 `hosts` 와 `gateways` 를 갖고, `http` 라우트의 `route` 자리에 `delegate` 를 둡니다. `delegate` 는 대상 VirtualService 의 이름과 네임스페이스를 가리킵니다. 대상(delegate VirtualService)은 `hosts` 없이 자기 `http` 라우트만 정의합니다. 요청이 root 의 `match` 에 맞으면 대상의 라우트가 평가됩니다. 공식 문서는 이렇게 설명합니다.

> "Delegate is used to specify the particular VirtualService which can be used to define delegate HTTPRoute."

제약은 문서가 네 가지로 적습니다.

- `delegate` 는 같은 라우트의 `route`·`redirect` 가 비어 있을 때만 쓸 수 있습니다. 대상의 라우트는 현재 것과 병합됩니다.
- 위임은 한 단계만 지원합니다. delegate VirtualService 가 다시 delegate 를 가질 수 없습니다.
- 대상의 `match` 는 root 의 `match` 의 엄격한 부분집합이어야 합니다. 아니면 충돌이 나서 그 라우트는 적용되지 않습니다.
- 대상의 `hosts` 는 비어 있어야 합니다. 대상의 `namespace` 기본값은 root 와 같습니다.

세 번째가 가장 자주 걸립니다. root 가 `prefix: /productpage` 로 넘기면 대상은 그 아래 경로(`/productpage/v1/` 등)만 다룰 수 있습니다. 대상이 `/reviews` 를 매치하면 root 범위를 벗어납니다.

### 최소 예제

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: shop-root
spec:
  hosts:
  - "shop.example.com"
  gateways:
  - shop-gateway
  http:
  - match:
    - uri:
        prefix: "/cart"
    delegate:
      name: cart-routes
      namespace: team-cart
  - match:
    - uri:
        prefix: "/orders"
    delegate:
      name: order-routes
      namespace: team-orders
---
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: cart-routes
  namespace: team-cart
spec:
  http:
  - match:
    - uri:
        prefix: "/cart/v2/"
    route:
    - destination:
        host: cart-v2.team-cart.svc.cluster.local
  - route:
    - destination:
        host: cart.team-cart.svc.cluster.local
```

`cart-routes` 에 `hosts` 가 없고, `/cart/v2/` 는 root 의 `/cart` 안에 들어 있다는 점이 핵심입니다. 마지막 라우트는 `match` 가 없어서 root 가 넘긴 `/cart` 의 나머지를 받습니다.

### 흔한 함정

- delegate VirtualService 에 `hosts` 를 적으면 안 됩니다. 문서가 "It must be empty for a delegate VirtualService." 라고 못 박습니다.
- root 와 delegate 의 `match` 가 정규식이면 조심해야 합니다. 문서는 한쪽이 어떤 속성을 정규식으로 매치하면 다른 쪽은 같은 속성에 다른 매치를 두지 말라고 합니다.
- 두 단계 이상 위임하는 구조는 지원되지 않습니다. 팀 하위 팀까지 나누려면 경로 규칙을 root 쪽에 둬야 합니다.

### 공식 문서 근거

- HTTPRoute `delegate` 필드: 위 제약 네 가지와 예제(productpage·reviews 를 nsA·nsB 의 VirtualService 로 위임).
- HTTPRoute `delegate` 필드 설명의 NOTE: "Only one level delegation is supported."



## 2. http 라우트는 위에서부터 처음 맞는 것

> `http` 는 순서가 있는 목록이고, 요청에 맞는 첫 라우트 하나만 씁니다. 그래서 구체적인 규칙을 위에, 포괄적인 규칙을 아래에 둡니다.

### 어떤 문제가 생기나

`/api/admin` 만 다른 백엔드로 보내려고 규칙을 추가했는데, `/api` 규칙이 더 위에 있으면 admin 요청도 `/api` 규칙에 먼저 맞습니다. 새 규칙은 아무리 정확해도 한 번도 실행되지 않습니다. 에러도 나지 않아서 "추가했는데 왜 안 되지" 가 됩니다.

### 동작 원리

공식 문서의 `http` 필드 설명이 규칙의 전부입니다.

> "An ordered list of route rules for HTTP traffic."

> "The first rule matching an incoming request is used."

한 라우트 안의 `match` 는 두 층으로 읽습니다. 문서에 따르면 하나의 match 블록 안의 조건은 AND, match 블록 목록은 OR 입니다.

> "All conditions inside a single match block have AND semantics, while the list of match blocks have OR semantics."

`uri` 매치에는 `exact`·`prefix`·`regex` 세 종류가 있고 대소문자를 구분합니다. 대소문자를 무시하려면 `ignoreUriCase` 를 켭니다. `match` 가 없는 라우트는 문서가 "catch all" 이라고 부르지는 않지만, 모든 요청에 맞을 수밖에 없으므로 첫 매치 규칙에 따라 맨 아래에 둬야 합니다. 문서 예제도 `match` 없는 라우트를 마지막에 둡니다.

### 최소 예제

```yaml
http:
- match:                      # 1. 가장 구체적인 것
  - uri:
      exact: "/api/admin"
  route:
  - destination: { host: admin }
- match:                      # 2. 그다음으로 넓은 것
  - uri:
      prefix: "/api"
  route:
  - destination: { host: api }
- route:                      # 3. match 없음 = 나머지 전부
  - destination: { host: web }
```

순서를 1 과 2 로 뒤집으면 `/api/admin` 은 `prefix: /api` 에 맞아 `api` 로 갑니다.

### 흔한 함정

- `match` 없는 라우트를 위쪽에 두면 아래 라우트는 모두 죽은 규칙이 됩니다.
- 한 match 블록 안에 `uri` 와 `headers` 를 같이 쓰면 둘 다 맞아야 합니다. 둘 중 하나만 맞아도 되게 하려면 match 블록을 둘로 나눕니다.
- delegate 와 함께 쓸 때는 root 에서 먼저 어느 delegate 로 갈지 정해지고, 그 뒤 delegate 안에서 다시 위에서부터 평가됩니다. 병합 뒤의 정확한 평가 순서는 열어 본 문서에 적혀 있지 않았습니다.

### 공식 문서 근거

- HTTPRoute `match`: AND/OR 문장.
- VirtualService `http` 필드: 순서 목록과 첫 매치 문장. `tls`·`tcp` 필드에도 같은 문장이 있습니다.
- HTTPMatchRequest `uri`: `exact`·`prefix`·`regex`, `ignoreUriCase`.



## 3. rewrite 와 redirect 의 차이

> `rewrite` 는 백엔드로 보내기 전에 경로나 호스트 헤더를 바꿔서 서버 안에서만 처리하고, `redirect` 는 클라이언트에게 3xx 응답을 돌려줘서 클라이언트가 새 주소로 다시 요청하게 합니다.

### 어떤 문제가 생기나

옛 경로 `/v1/getProductRatings` 를 새 경로 `/v1/bookRatings` 로 옮기면 기존 클라이언트가 깨집니다. 어떤 경우에는 클라이언트가 새 주소를 알게 해야 하고(주소창이 바뀌어야 하는 경우), 어떤 경우에는 클라이언트는 그대로 두고 서버 쪽 경로만 맞춰야 합니다. 둘을 구분하지 않고 쓰면 무한 리다이렉트가 나거나 백엔드가 모르는 경로를 받습니다.

### 동작 원리

`rewrite` 는 라우트의 `route` 와 함께 쓰는 변환입니다. 문서는 "Rewrite will be performed before forwarding." 이라고 하고, `HTTPRouteDestination` 에서만 쓸 수 있다고 합니다. 필드는 셋입니다.

| 필드 | 동작 |
|------|------|
| `uri` | 경로(또는 prefix)를 이 값으로 바꿉니다. prefix 로 매치했으면 매치된 prefix 만 바뀝니다 |
| `uriRegexRewrite` | RE2 정규식으로 경로를 바꿉니다. 캡처 그룹을 새 경로에서 참조합니다 |
| `authority` | Authority/Host 헤더를 바꿉니다 |

`redirect` 는 응답을 만듭니다. 문서는 "send a 301 redirect response to the caller" 라고 합니다.

| 필드 | 동작 |
|------|------|
| `uri` | 경로 전체를 이 값으로 바꿉니다. exact 로 매치했든 prefix 로 매치했든 전체가 교체됩니다 |
| `authority` | Authority/Host 부분을 바꿉니다 |
| `redirectCode` | 응답 상태 코드. 기본값은 301(`MOVED_PERMANENTLY`) |
| `prefixRewrite` | 매치된 prefix 만 바꿉니다. prefix 매치에서만 쓰고 `uri` 와 함께 쓸 수 없습니다 |

둘은 같이 쓰지 못합니다. 문서가 rewrite 쪽에 "Rewrite cannot be used with Redirect primitive." 라고 적습니다. 하나의 라우트는 `route`, `redirect`, `directResponse` 가운데 하나로 응답합니다.

### 최소 예제

내부 경로만 바꾸는 rewrite 입니다. 클라이언트는 `/ratings/1` 을 부르고 백엔드는 `/v1/bookRatings/1` 을 받습니다.

```yaml
http:
- match:
  - uri:
      prefix: "/ratings"
  rewrite:
    uri: "/v1/bookRatings"
  route:
  - destination:
      host: ratings
      subset: v1
```

클라이언트에게 새 주소로 가라고 알리는 redirect 입니다. `example.com/foo/bar` 가 `foo.example.com/bar` 로 301 이동합니다.

```yaml
http:
- match:
  - uri:
      prefix: "/foo/"
  redirect:
    authority: foo.example.com
    prefixRewrite: "/"
```

### 흔한 함정

- redirect 의 `uri` 는 prefix 매치여도 경로 전체를 교체합니다. 하위 경로를 보존하려면 `prefixRewrite` 를 씁니다.
- redirect 의 기본 코드는 301 입니다. 브라우저가 301 을 오래 캐시하므로 임시 이동이면 `redirectCode` 로 302 를 지정합니다.
- rewrite 는 클라이언트에게 보이지 않습니다. 응답의 `Location` 이나 쿠키 경로가 옛 경로 기준이면 애플리케이션이 그것을 알아야 합니다.
- `rewrite` 와 `redirect` 는 한 라우트에 함께 쓸 수 없습니다.

### 공식 문서 근거

- HTTPRewrite: "Rewrite primitive can be used only with HTTPRouteDestination." 및 `uri`·`uriRegexRewrite`·`authority` 정의.
- HTTPRedirect: "The default response code is MOVED_PERMANENTLY (301)." 및 `prefixRewrite`·`uri` 상호 배타.
- HTTPRoute `rewrite`: "Rewrite cannot be used with Redirect primitive. Rewrite will be performed before forwarding."



## 확인하지 못한 것

- 클러스터에 적용해 보지 않았고 `istioctl analyze` 도 돌리지 않았습니다. YAML 은 문법만 확인했습니다.
- delegate VirtualService 가 `gateways` 필드를 가질 수 있는지, 대상에서 무시되는 필드가 무엇인지는 열어 본 문서에 없었습니다.
- delegate 병합 뒤 라우트 평가 순서는 문서에 적혀 있지 않았습니다.
- `match` 없는 라우트를 "나머지 전부"로 읽는 것은 첫 매치 규칙과 문서 예제의 배치에서 이끌어 낸 해석이고, 문서가 그렇게 명시한 문장은 없었습니다.
- redirect 의 실제 응답 `Location` 값은 확인하지 못했습니다. 필드 동작은 문서 문장 기준입니다.
- 301 캐시 기간과 `Location` 헤더 보정에 관한 함정 두 줄은 일반적인 HTTP 동작에서 적은 것이고 Istio 문서의 문장이 아닙니다.
- 문서 URL 은 `latest` 입니다. 열어 본 날짜(2026-11-06) 기준이고 버전을 고정한 주소가 아닙니다.
- 위임의 지원 범위는 문서 문장(한 단계, hosts 비움, match 부분집합)까지만 확인했습니다. Istio 버전별 차이는 확인하지 못했습니다.



## 관련 문서

- 같은 주제로 이미 있는 write/ 문서는 찾지 못했습니다. `08_cloud/book/istio-in-action/` 정독 노트 가운데 [서비스 메시는 무엇을 인프라로 밀어냈는가](../../08_cloud/book/istio-in-action/01-01.서비스%20메시는%20무엇을%20인프라로%20밀어냈는가.md) 가 메시 개요를 다룹니다.
