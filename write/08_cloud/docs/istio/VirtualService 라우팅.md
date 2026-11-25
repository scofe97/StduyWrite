---
title: VirtualService 라우팅 — delegate·매치 순서·rewrite·redirect
tags: [istio, virtualservice, delegate, rewrite, redirect, routing]
status: draft
source:
  - https://istio.io/v1.32/docs/reference/config/networking/virtual-service/
  - https://www.rfc-editor.org/rfc/rfc9110#name-301-moved-permanently
related:
  - ./README.md
  - ./Ambient 모드·ztunnel·waypoint.md
  - ../../book/istio-in-action/04-01.문을 여는 일과 길을 내는 일을 가른다.md
  - ../../book/istio-in-action/05-01.위험에 노출되는 트래픽을 줄여 가는 순서.md
updated: 2026-11-25
---

# VirtualService 라우팅 — delegate·매치 순서·rewrite·redirect

---

> VirtualService 의 `http` 라우트에서 헷갈리는 세 가지를 다룹니다. 라우트를 넘기는 `delegate`, 이기는 라우트를 정하는 매치 순서, 경로를 바꾸는 `rewrite` 와 `redirect` 입니다.

근거는 Istio 1.32 의 VirtualService 레퍼런스 한 페이지입니다.

규칙은 모두 레퍼런스의 문장에서 가져왔고, 클러스터에 적용해 돌려 본 것은 아닙니다. 문서의 YAML 은 문법만 확인했습니다. 레퍼런스에 없어서 해석이거나 확인하지 못한 문장은 본문에서 그렇게 밝혔습니다.

`Gateway` 와 `VirtualService` 가 나뉜 이유, 가중치·미러링 같은 라우팅 속성은 이 문서가 다루지 않습니다. 앞의 것은 [04-01 노트](../../book/istio-in-action/04-01.문을%20여는%20일과%20길을%20내는%20일을%20가른다.md)가, 뒤의 것은 [05-01 노트](../../book/istio-in-action/05-01.위험에%20노출되는%20트래픽을%20줄여%20가는%20순서.md)가 맡습니다.



## 1. delegate 로 라우트 나눠 맡기기

> root VirtualService 가 경로별로 라우트를 다른 VirtualService 에 넘기면, 팀마다 자기 경로의 라우팅만 따로 관리할 수 있습니다. 대신 제약이 넷 붙습니다.

하나의 호스트 뒤에 여러 팀의 서비스가 붙으면 VirtualService 한 개에 모든 경로 규칙이 쌓입니다. 한 팀이 규칙을 고치려면 다른 팀이 함께 쓰는 리소스를 편집해야 하고, 실수 하나가 전체 라우팅을 깨뜨립니다.

`delegate` 는 이 리소스를 쪼개는 장치입니다. root VirtualService 는 `hosts` 와 `gateways` 를 갖습니다. 그리고 `http` 라우트의 `route` 자리에 `delegate` 를 둡니다.

`delegate.name` 은 대상 VirtualService 의 이름입니다. `namespace` 를 생략하면 root 와 같은 네임스페이스입니다.[^vs-delegate]

대상 VirtualService 는 `hosts` 없이 자기 `http` 라우트만 정의합니다. 요청이 root 의 `match` 에 맞으면 대상의 라우트가 평가됩니다.

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

`cart-routes` 에는 `hosts` 가 없습니다. `/cart/v2/` 는 root 의 `/cart` 안에 들어 있습니다. 마지막 라우트는 `match` 가 없어서 앞 라우트에 걸리지 않은 나머지 요청을 받습니다. `cart`·`team-cart` 같은 이름은 설명하려고 지은 값입니다.

제약은 레퍼런스가 네 가지로 적습니다.[^vs-delegate][^vs-hosts]

- `delegate` 는 같은 라우트의 `route` 와 `redirect` 가 비어 있을 때만 쓸 수 있습니다. 대상의 라우트 규칙은 현재 것과 병합됩니다.
- 위임은 한 단계만 지원합니다. 대상 VirtualService 가 다시 `delegate` 를 가질 수 없습니다.
- 대상의 `match` 는 root 의 `match` 의 엄격한 부분집합이어야 합니다. 아니면 충돌이 나서 그 라우트는 적용되지 않습니다.
- 대상의 `hosts` 는 비어 있어야 합니다.

세 번째가 가장 자주 걸립니다. root 가 `prefix: /cart` 로 넘기면 대상은 그 아래 경로(`/cart/v2/` 등)만 다룰 수 있습니다. 대상이 `/orders` 를 매치하면 root 범위를 벗어나 그 라우트는 적용되지 않습니다.

정규식 매치에는 따로 주의가 붙습니다. root 가 어떤 속성(경로, 헤더 등)을 정규식으로 매치했으면 대상은 같은 속성에 다른 매치를 두지 말아야 합니다. 반대로 대상이 정규식으로 매치했을 때 root 도 같은 속성에 다른 매치를 두지 말아야 합니다.[^vs-match]

두 단계 이상 나누는 구조는 지원되지 않습니다. 팀 안의 하위 팀까지 나누려면 그 경로 규칙을 root 나 대상 안에 직접 적어야 합니다.

위임의 지원 범위는 레퍼런스 문장(한 단계, `hosts` 비움, `match` 부분집합)까지만 확인했습니다. Istio 버전별 차이는 확인하지 못했습니다.

레퍼런스는 `gateways` 필드를 대상이 가질 수 있는지, 병합한 뒤 라우트를 어떤 순서로 평가하는지 적지 않습니다. 이 둘은 확인하지 못했습니다.



## 2. http 라우트는 위에서부터 처음 맞는 것

> `http` 는 순서가 있는 목록이고, 요청에 맞는 첫 라우트 하나만 씁니다. 그래서 구체적인 규칙을 위에, 포괄적인 규칙을 아래에 둡니다.

`/api/admin` 만 다른 백엔드로 보내려고 규칙을 추가했는데 `/api` 규칙이 더 위에 있으면, admin 요청도 `/api` 규칙에 먼저 맞습니다. 새 규칙은 아무리 정확해도 한 번도 실행되지 않습니다. 에러도 나지 않아서 "추가했는데 왜 안 되지" 가 됩니다.

레퍼런스의 `http` 필드 설명이 이 규칙의 전부입니다. `http` 는 HTTP 트래픽용 라우트 규칙의 순서 있는 목록이고, 들어온 요청에 맞는 첫 규칙을 씁니다.[^vs-http] `tls` 와 `tcp` 필드에도 같은 문장이 있습니다.

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

`match` 가 없는 라우트는 첫 매치 규칙에 따라 맨 아래에 둡니다. 레퍼런스가 이를 "나머지 전부" 라고 명시한 문장은 찾지 못했고, 첫 매치 규칙에서 이끌어 낸 해석입니다. 레퍼런스의 예제는 `match` 없는 라우트를 마지막에 둡니다.[^vs-example] 그러므로 위쪽에 두면 아래 라우트는 모두 죽은 규칙이 됩니다.

한 라우트 안의 `match` 는 두 층으로 읽습니다. 하나의 match 블록 안의 조건은 모두 맞아야 하고(AND), match 블록이 여럿이면 그중 하나만 맞아도 됩니다(OR).[^vs-route] `uri` 와 `headers` 를 한 블록에 쓰면 둘 다 맞아야 합니다. 둘 중 하나만 맞아도 되게 하려면 블록을 둘로 나눕니다. `match` 를 적을 때 그 항목은 비울 수 없습니다.[^vs-match]

`uri` 매치에는 세 종류가 있고 값은 대소문자를 구분합니다.[^vs-match]

| 종류 | 뜻 |
|------|-----|
| `exact` | 문자열이 같을 때 맞습니다 |
| `prefix` | 문자열로 시작할 때 맞습니다 |
| `regex` | RE2 정규식에 맞을 때 맞습니다 |

대소문자를 무시하려면 `ignoreUriCase` 를 켭니다. 이 플래그는 `exact` 와 `prefix` 매치에만 적용되고 `regex` 매치에는 적용되지 않습니다.[^vs-match]



## 3. rewrite 와 redirect 의 차이

> `rewrite` 는 백엔드로 보내기 전에 경로나 호스트 헤더를 바꿔서 서버 안에서만 처리합니다. `redirect` 는 클라이언트에게 3xx 응답을 돌려줘서 클라이언트가 새 주소로 다시 요청하게 합니다.

옛 경로 `/v1/getProductRatings` 를 새 경로 `/v1/bookRatings` 로 옮기면 기존 클라이언트가 깨집니다. 클라이언트가 새 주소를 알아야 하는 경우도 있고, 클라이언트는 그대로 두고 서버 쪽 경로만 맞추면 되는 경우도 있습니다. 앞의 것이 `redirect`, 뒤의 것이 `rewrite` 입니다. 둘은 한 라우트에 함께 쓸 수 없습니다.[^vs-route]

아래 도식은 같은 요청이 두 방식에서 어떤 길을 지나는지 보입니다.

![rewrite 와 redirect 의 요청 경로 비교](./_assets/VirtualService%20%EB%9D%BC%EC%9A%B0%ED%8C%85.rewrite-redirect.svg)

### rewrite

`rewrite` 는 라우트의 `route` 와 함께 쓰는 변환입니다. 레퍼런스는 `HTTPRouteDestination` 에서만 쓸 수 있고 전달하기 전에 수행된다고 적습니다.[^vs-rewrite] 필드는 셋입니다.

| 필드 | 동작 |
|------|------|
| `uri` | 경로(또는 prefix)를 이 값으로 바꿉니다. prefix 로 매치했으면 매치된 prefix 만 바뀝니다 |
| `uriRegexRewrite` | RE2 정규식(`match`)에 맞는 부분을 `rewrite` 문자열로 바꿉니다. 캡처 그룹을 새 경로에서 참조합니다 |
| `authority` | Authority/Host 헤더를 바꿉니다 |

내부 경로만 바꾸는 예입니다. 클라이언트는 `/ratings/1` 을 부르고 백엔드는 `/v1/bookRatings/1` 을 받습니다.

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

정규식 rewrite 로 대소문자를 무시하는 예입니다. `match` 는 `(?i)/xxx/`, `rewrite` 는 `/yyy/` 로 적습니다. 그러면 `/aaa/XxX/bbb` 는 `/aaa/yyy/bbb` 가 됩니다.[^vs-rewrite]

### redirect

`redirect` 는 라우트 대신 301 응답을 만들어 호출자에게 돌려줍니다.[^vs-redirect] 필드는 아래와 같습니다.

| 필드 | 동작 |
|------|------|
| `uri` | 경로 전체를 이 값으로 바꿉니다. exact 로 매치했든 prefix 로 매치했든 전체가 교체됩니다 |
| `authority` | Authority/Host 부분을 바꿉니다 |
| `port` | 포트를 이 값으로 바꿉니다 |
| `derivePort` | 포트를 동적으로 정합니다. `FROM_PROTOCOL_DEFAULT` 는 HTTP 80·HTTPS 443, `FROM_REQUEST_PORT` 는 요청의 포트입니다 |
| `scheme` | 스킴(`http`·`https`)을 바꿉니다. 생략하면 원래 스킴을 씁니다 |
| `redirectCode` | 응답 상태 코드입니다. 기본값은 301(`MOVED_PERMANENTLY`)입니다 |
| `prefixRewrite` | 매치된 prefix 만 바꿉니다. prefix 매치에서만 쓰고 `uri` 와 함께 쓸 수 없습니다 |

클라이언트에게 새 주소로 가라고 알리는 예입니다. `example.com/foo/bar` 가 `foo.example.com/bar` 로 301 이동합니다.

```yaml
http:
- match:
  - uri:
      prefix: "/foo/"
  redirect:
    authority: foo.example.com
    prefixRewrite: "/"
```

`prefixRewrite: /` 는 매치한 prefix 를 `/` 로 바꿉니다. 매치를 `/foo` 로 적으면 `/foo/baz` 는 `//baz` 가 됩니다. 슬래시까지 넣은 `/foo/` 로 매치해야 `/baz` 가 됩니다.[^vs-redirect]

### 흔한 함정

- redirect 의 `uri` 는 prefix 매치여도 경로 전체를 교체합니다. 하위 경로를 보존하려면 `prefixRewrite` 를 씁니다.
- redirect 의 기본 코드는 301 이고, 301 응답은 명시한 캐시 제어가 없어도 캐시될 수 있습니다.[^rfc-301] 임시 이동이면 `redirectCode` 로 302 를 지정합니다.
- rewrite 는 클라이언트에게 보이지 않습니다. 백엔드가 응답의 `Location` 이나 쿠키 경로를 옛 경로 기준으로 적으면 어긋날 수 있습니다. Istio 가 응답 쪽을 되돌려 주는지는 확인하지 못했습니다.
- 한 라우트는 `route`, `redirect`, `directResponse` 가운데 하나로 응답합니다.[^vs-route] `rewrite` 와 `redirect` 도 함께 쓸 수 없습니다.



## 관련 문서

> 이 문서가 딛고 서거나 이어지는 이웃입니다.

- [Istio 공식문서 정독 인덱스](./README.md) — 이 폴더의 문서 목록
- [Ambient 모드와 ztunnel·waypoint](./Ambient%20모드·ztunnel·waypoint.md) — waypoint 에서 HTTPRoute 로 L7 라우팅을 하는 Ambient 쪽 이야기
- [문을 여는 일과 길을 내는 일을 가른다](../../book/istio-in-action/04-01.문을%20여는%20일과%20길을%20내는%20일을%20가른다.md) — Gateway 와 VirtualService 의 분업
- [위험에 노출되는 트래픽을 줄여 가는 순서](../../book/istio-in-action/05-01.위험에%20노출되는%20트래픽을%20줄여%20가는%20순서.md) — 헤더 매치·가중치·미러링으로 쓰는 VirtualService



## 참고 자료

> 본문에서 인용한 1차 자료입니다. Istio 문서 주소는 1.32 판으로 고정했습니다.

- [Istio 1.32 — Virtual Service](https://istio.io/v1.32/docs/reference/config/networking/virtual-service/) — `http` 필드, `HTTPRoute`·`HTTPMatchRequest`·`Delegate`·`HTTPRewrite`·`HTTPRedirect` 정의와 예제
- [RFC 9110 — 301 Moved Permanently](https://www.rfc-editor.org/rfc/rfc9110#name-301-moved-permanently) — 301 응답의 캐시 가능성

[^vs-delegate]: Istio 1.32 — Virtual Service, HTTPRoute `delegate` 와 `Delegate`. "It can be set only when Route and Redirect are empty, and the route rules of the delegate VirtualService will be merged with that in the current one." "Only one level delegation is supported." "The delegate’s HTTPMatchRequest must be a strict subset of the root’s, otherwise there is a conflict and the HTTPRoute will not take effect." `Delegate.namespace` 는 "By default, it is same to the root’s." <https://istio.io/v1.32/docs/reference/config/networking/virtual-service/> (2026-11-25 조회)

[^vs-hosts]: Istio 1.32 — Virtual Service, `hosts` 필드. "Note: It must be empty for a delegate VirtualService." <https://istio.io/v1.32/docs/reference/config/networking/virtual-service/> (2026-11-25 조회)

[^vs-match]: Istio 1.32 — Virtual Service, `HTTPMatchRequest`. "HTTPMatchRequest CANNOT be empty." "If a root VirtualService have matched any property (path, header etc.) by regex, delegate VirtualServices should not have any other matches on the same property." `uri` 값은 "case-sensitive" 이고 `exact`·`prefix`·`regex`(RE2 스타일)이며, `ignoreUriCase` 는 "The case will be ignored only in the case of exact and prefix URI matches." <https://istio.io/v1.32/docs/reference/config/networking/virtual-service/> (2026-11-25 조회)

[^vs-http]: Istio 1.32 — Virtual Service, `http` 필드. "An ordered list of route rules for HTTP traffic." "The first rule matching an incoming request is used." <https://istio.io/v1.32/docs/reference/config/networking/virtual-service/> (2026-11-25 조회)

[^vs-example]: Istio 1.32 — Virtual Service 개요 예제. `reviews` 의 `http` 에서 `match` 가 있는 라우트(subset v2) 뒤에 `match` 없는 라우트(subset v1)를 둡니다. <https://istio.io/v1.32/docs/reference/config/networking/virtual-service/> (2026-11-25 조회)

[^vs-route]: Istio 1.32 — Virtual Service, `HTTPRoute`. "All conditions inside a single match block have AND semantics, while the list of match blocks have OR semantics." "A HTTP rule can either return a direct_response, redirect or forward (default) traffic." `rewrite` 는 "Rewrite cannot be used with Redirect primitive." <https://istio.io/v1.32/docs/reference/config/networking/virtual-service/> (2026-11-25 조회)

[^vs-rewrite]: Istio 1.32 — Virtual Service, `HTTPRewrite`. "Rewrite primitive can be used only with HTTPRouteDestination." `uri` 는 "If the original URI was matched based on prefix, the value provided in this field will replace the corresponding matched prefix." 정규식 예제는 `(?i)/xxx/` 와 `/yyy/` 입니다. <https://istio.io/v1.32/docs/reference/config/networking/virtual-service/> (2026-11-25 조회)

[^vs-redirect]: Istio 1.32 — Virtual Service, `HTTPRedirect`. "HTTPRedirect can be used to send a 301 redirect response to the caller." `redirectCode` 는 "The default response code is MOVED_PERMANENTLY (301)." `prefixRewrite` 는 "The route match must use a prefix match type." 이고 `uri` 와 상호 배타입니다. 예제 설명은 "prefix_rewrite: / → /foo/baz becomes //baz (use /foo/ match to get /baz)." <https://istio.io/v1.32/docs/reference/config/networking/virtual-service/> (2026-11-25 조회)

[^rfc-301]: RFC 9110 §15.4.2. "A 301 response is heuristically cacheable; i.e., unless otherwise indicated by the method definition or explicit cache controls (see Section 4.2.2 of [CACHING])." <https://www.rfc-editor.org/rfc/rfc9110#name-301-moved-permanently> (2026-11-25 조회)
