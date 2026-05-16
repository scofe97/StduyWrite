<!-- migrated:
  - write/09_cloud/service-mesh/deepdive/19-01.Istio EnvoyFilter 실습.md
  - write/09_cloud/service-mesh/deepdive/19-02.Istio EnvoyFilter 점검.md
  (2026-04-19) -->

# Ch19. EnvoyFilter — 심화 탐구
---
> 📌 EnvoyFilter는 올바르게 사용하면 강력한 확장 수단이지만, 잘못된 선택과 관리 부재는 장기적인 운영 부채를 남긴다. 이 문서는 실제 운영에서 마주치는 판단 문제를 다룬다.

## Q1. EnvoyFilter와 WasmPlugin 중 어느 것을 선택해야 하는가? 마이그레이션 전략은?

두 리소스가 해결하는 문제의 교집합이 크기 때문에 선택 기준을 명확히 해야 한다. 핵심 차이는 추상화 수준에 있다. EnvoyFilter는 Envoy xDS 설정을 직접 패치하므로 모든 Envoy 기능에 접근할 수 있지만, Istio 버전 호환성을 직접 관리해야 한다. WasmPlugin은 Istio가 내부 xDS 배포를 담당하므로 설정이 단순하고 호환성 위험이 낮다. 단, WasmPlugin은 WASM 바이너리 형태의 플러그인에만 적용 가능하다.

선택 기준은 다음과 같이 정리된다:

- Lua 스크립트나 Envoy 내장 필터 설정 변경(재시도 코드, Cluster 설정 등)이 목적이라면 EnvoyFilter를 사용한다. WasmPlugin으로 대체할 방법이 없다.
- 커스텀 요청/응답 처리 로직(WAF, 커스텀 인증, 변환 로직 등)이 목적이라면 WasmPlugin을 먼저 검토한다. Lua로도 처리 가능하지만 로직이 100줄을 넘기면 WASM으로 전환하는 것이 유지보수에 유리하다.
- Istio 1.12 미만 환경이라면 WasmPlugin CRD가 없으므로 EnvoyFilter로 WASM을 배포해야 한다.

마이그레이션 전략은 점진적 교체를 원칙으로 한다. WASM 바이너리를 먼저 구현하고, 스테이징에서 WasmPlugin으로 배포해 기존 EnvoyFilter와 동일한 동작을 검증한다. 검증이 완료되면 EnvoyFilter를 삭제하고 WasmPlugin만 남긴다. 두 리소스가 동시에 활성화된 상태로 오래 두면 동작이 중복되거나 순서 충돌이 발생할 수 있다.

마이그레이션 시 주의할 점은 `phase` 필드다. WasmPlugin의 `phase`(AUTHN, AUTHZ, STATS)는 HTTP 필터 체인 내 삽입 위치를 추상화한 값이다. 기존 EnvoyFilter에서 `INSERT_BEFORE envoy.filters.http.router`로 삽입하던 위치가 WasmPlugin의 어떤 phase에 해당하는지 `config_dump`로 먼저 확인한다.

## Q2. EnvoyFilter의 우선순위 결정 규칙은? 충돌을 어떻게 예방하는가?

Istio는 여러 EnvoyFilter가 같은 xDS 객체를 수정할 때 적용 순서를 다음 규칙으로 결정한다.

첫 번째 규칙은 네임스페이스다. 루트 네임스페이스(기본값: `istio-system`)의 EnvoyFilter가 워크로드 네임스페이스보다 먼저 처리된다. 따라서 메시 전체에 적용해야 하는 공통 정책은 `istio-system`에 두고, 서비스별 커스텀은 해당 네임스페이스에 둔다.

두 번째 규칙은 생성 시각이다. 같은 네임스페이스 안에서는 생성 시각 기준으로 오래된 EnvoyFilter가 먼저 적용된다. 이 규칙은 예측하기 어렵고 실수를 유발하므로, Istio 1.10부터 도입된 `priority` 필드로 명시적 순서를 부여한다.

```yaml
spec:
  priority: 10   # 높을수록 나중에 적용 (기본값: 0, 음수도 허용)
```

충돌을 예방하는 실천 방법은 다음과 같다.

소유권 분리를 명확히 한다. 각 EnvoyFilter에 `annotations`로 담당 팀과 목적을 기록하고, 같은 `applyTo` 위치를 수정하는 EnvoyFilter는 한 팀에서 관리하도록 조직적으로 합의한다.

```yaml
metadata:
  annotations:
    team: platform-security
    purpose: "WAF via Coraza WASM plugin"
    last-verified-istio: "1.20"
```

`MERGE` operation 사용 시 특히 주의한다. 두 EnvoyFilter가 같은 필드를 `MERGE`로 수정하면 나중에 적용된 것이 이긴다. 배열 필드(예: `retriable_status_codes`)는 마지막에 적용된 EnvoyFilter의 값으로 완전히 교체되지 않고 병합된다. 이 동작을 `config_dump`로 반드시 확인해야 한다.

`INSERT_BEFORE`로 같은 위치에 두 필터를 삽입하면 적용 순서에 따라 필터 체인 순서가 달라진다. 순서가 중요한 경우(인증 → 인가 순서 등) `priority`를 명시적으로 지정한다.

## Q3. Istio 업그레이드 시 EnvoyFilter가 깨지는 흔한 패턴과 사전 검증 방법은?

EnvoyFilter 호환성 문제는 크게 세 가지 원인에서 발생한다.

첫 번째는 필터 이름 변경이다. Istio가 내부적으로 생성하는 Envoy 필터 이름이 버전 간에 바뀔 수 있다. `match.listener.filterChain.filter.name`에 하드코딩된 이름이 새 버전에서 달라지면 match 조건이 아무것도 매칭하지 못해 패치가 조용히 무시된다. 오류 메시지가 없어 탐지하기 어렵다.

두 번째는 typed_config의 @type 경로 변경이다. Envoy v2에서 v3 API로 전환되면서 많은 타입 경로가 변경됐다. 예를 들어 Lua 필터의 타입은 다음과 같이 바뀌었다:

```
# v2 (구버전)
@type: type.googleapis.com/envoy.config.filter.http.lua.v2.Lua

# v3 (현재)
@type: type.googleapis.com/envoy.extensions.filters.http.lua.v3.LuaPerRoute
```

구버전 @type을 사용하는 EnvoyFilter는 Istio 1.10 이후에서 파싱 경고를 발생시키거나 무시된다.

세 번째는 Istio가 생성하는 xDS 구조 자체의 변경이다. Istio 업그레이드 시 Listener나 Filter Chain 구조가 바뀌면 `match.listener.portNumber`나 `match.routeConfiguration.vhost.name` 같은 경로 조건이 더 이상 매칭되지 않을 수 있다.

사전 검증 방법은 단계적으로 수행한다.

1단계로 Istio 업그레이드 전 현재 `config_dump`를 저장한다:

```bash
kubectl exec -n production order-service-pod -c istio-proxy -- \
  curl -s localhost:15000/config_dump > /tmp/before_upgrade_config_dump.json
```

2단계로 업그레이드 후 동일한 Pod의 `config_dump`를 다시 저장하고 diff를 확인한다:

```bash
kubectl exec -n production order-service-pod -c istio-proxy -- \
  curl -s localhost:15000/config_dump > /tmp/after_upgrade_config_dump.json

diff /tmp/before_upgrade_config_dump.json /tmp/after_upgrade_config_dump.json | \
  grep -E "(filter\.name|typed_config|@type)"
```

3단계로 각 EnvoyFilter의 효과를 기능 테스트로 확인한다. config_dump에 필터가 보인다고 올바르게 동작하는 것은 아니다. Lua 헤더 삽입이라면 실제 요청을 보내 응답 헤더를 확인하고, Rate Limit이라면 임계치를 넘는 요청을 보내 `429` 응답을 확인한다.

Istio Changelog에서 `EnvoyFilter`, `xDS`, `Envoy upgrade` 관련 항목을 사전에 검토하는 것도 중요하다. Envoy 버전이 바뀔 때(Istio 릴리스마다 Envoy가 함께 업그레이드됨) 필터 이름이나 API 경로가 변경될 가능성이 높다.

## Q4. Lua 필터의 성능 오버헤드는 어느 수준인가? 어떤 경우에 WASM으로 전환해야 하는가?

Lua 필터는 LuaJIT으로 실행되어 인터프리터 언어 치고는 빠른 편이다. 단순한 헤더 추가나 값 읽기 수준의 Lua 코드는 일반적으로 P50에서 0.1ms 미만의 추가 지연을 발생시킨다. 이 수준은 대부분의 서비스에서 허용 가능하다.

그러나 다음 패턴에서는 성능 저하가 눈에 띄게 발생한다.

첫째, 요청 본문 읽기다. `request_handle:body()`로 전체 본문을 읽으면 스트리밍이 버퍼링으로 전환된다. 본문이 1MB라면 해당 데이터 전체가 메모리에 올라온 후 Lua 코드가 실행된다. 대용량 파일 업로드 경로에서 이 패턴을 사용하면 메모리 사용량이 급격히 증가하고 지연이 수십 ms 단위로 늘어난다.

둘째, 복잡한 문자열 처리와 정규표현식 반복 실행이다. 요청마다 복잡한 패턴 매칭을 수행하면 CPU 사용률이 올라간다.

셋째, Lua 내부에서 외부 서비스 호출이다. Envoy Lua API는 비동기 HTTP 호출을 지원하지만, 잘못 사용하면 코루틴이 블로킹되어 연결이 대기 상태에 빠질 수 있다.

WASM으로 전환을 고려해야 하는 시점은 다음과 같다:

- Lua 코드가 100줄을 초과하고 단위 테스트가 필요한 수준으로 복잡해질 때
- 요청 본문 검사(SQL Injection, XSS 탐지 등)가 필요해 본문 버퍼링이 불가피할 때
- 동일 로직을 여러 언어로 구현한 기존 라이브러리(예: Coraza WAF)를 재사용하려 할 때
- 팀이 Lua보다 Rust나 Go에 더 익숙할 때

성능 비교 시 주의할 점은 WASM이 항상 Lua보다 빠르지 않다는 것이다. WASM은 sandbox 격리를 위한 메모리 복사 오버헤드가 있어서 단순한 작업에서는 LuaJIT보다 느릴 수 있다. 구체적인 수치는 반드시 실 트래픽 패턴으로 벤치마킹해야 한다.

## Q5. Coraza WAF를 WASM 플러그인으로 배포할 때 고려해야 할 운영 사항은?

Coraza WAF는 OWASP CRS를 포함한 WASM 바이너리 크기가 약 10~20MB다. 이 크기는 운영에서 다음 문제를 일으킨다.

첫 번째는 Pod 시작 시간이다. WasmPlugin은 Pod 시작 시 사이드카 프록시가 OCI 레지스트리에서 WASM 바이너리를 다운로드한다. 10MB 이상의 바이너리는 느린 네트워크에서 10초 이상 걸릴 수 있다. 이는 Pod의 Readiness 확보를 지연시킨다. 해결책은 로컬 레지스트리(Harbor, Nexus 등 클러스터 내부)에 이미지를 미러링하는 것이다.

두 번째는 메모리 사용량이다. 각 사이드카 컨테이너가 WASM 바이너리를 독립적으로 로드하므로, 100개 Pod가 있으면 동일 바이너리가 100번 메모리에 올라온다. 노드당 메모리 여유를 확인하고 `resources.limits.memory`를 조정해야 한다.

세 번째는 규칙 업데이트다. OWASP CRS가 새 버전을 릴리스하면 WASM 바이너리를 다시 빌드하고 새 이미지 태그로 WasmPlugin을 업데이트해야 한다. 이 프로세스를 자동화하지 않으면 규칙이 오래된 채로 방치된다. CI 파이프라인에서 CRS 업데이트를 감지해 자동 빌드/배포하는 워크플로우를 구성한다.

네 번째는 false positive 관리다. CRS를 활성화하면 정상 트래픽이 차단될 수 있다. 특히 JSON API에서 SQL 쿼리 파라미터를 전달하는 경우(예: GraphQL 쿼리 문자열)나 Base64 인코딩된 바이너리 데이터가 포함된 요청이 오탐 대상이 된다. `SecRuleEngine DetectionOnly` 단계를 충분히 거친 후 차단 모드로 전환해야 한다.

다섯 번째는 로그 볼륨이다. CRS가 탐지한 공격 시도는 Envoy access log에 기록된다. 공격 트래픽이 많은 환경에서는 로그 볼륨이 급격히 증가해 스토리지 비용과 로그 파이프라인 부하를 높인다. Coraza의 로그 레벨 설정으로 탐지 이벤트만 선택적으로 기록하고, 로그 샘플링을 적용하는 것을 고려한다.

## Q6. EnvoyFilter로 ext_authz를 설정할 때 AuthorizationPolicy와의 관계는?

Istio의 AuthorizationPolicy는 내부적으로 Envoy의 `envoy.filters.http.rbac` 필터를 통해 구현된다. ext_authz는 별도의 `envoy.filters.http.ext_authz` 필터를 추가하는 것이므로, 두 메커니즘은 병렬로 동작한다.

두 필터의 실행 순서가 결과에 영향을 미친다. EnvoyFilter로 ext_authz를 `INSERT_BEFORE router`로 삽입하면 기본적으로 rbac 필터 다음에 위치한다. 즉, AuthorizationPolicy가 먼저 DENY하면 ext_authz 필터는 실행되지 않는다. ext_authz를 AuthorizationPolicy보다 먼저 실행하려면 `INSERT_FIRST` operation을 사용하거나 `priority`를 높게 설정해야 한다.

```
HTTP 필터 체인 실행 순서 (기본):
[jwt_authn] → [rbac(AuthorizationPolicy)] → [ext_authz] → [router]

INSERT_FIRST 사용 시:
[ext_authz] → [jwt_authn] → [rbac(AuthorizationPolicy)] → [router]
```

권장 패턴은 두 메커니즘을 용도에 따라 분리하는 것이다. AuthorizationPolicy는 메시 내부 서비스 간 접근 제어(SPIFFE ID 기반)에 사용하고, ext_authz는 외부 인가 서버에 위임이 필요한 복잡한 비즈니스 권한(사용자 역할, 데이터 소유권 등)에 사용한다.

Istio 1.9 이후부터는 `ExtensionProvider`와 AuthorizationPolicy의 `CUSTOM` action으로 ext_authz를 구성하는 공식 방법이 있다. 이 방식은 EnvoyFilter를 직접 작성하지 않고 Istio가 필터를 관리하므로 호환성 위험이 적다:

```yaml
# meshconfig에 ExtensionProvider 등록
extensionProviders:
  - name: my-ext-authz
    envoyExtAuthzGrpc:
      service: authz.production.svc.cluster.local
      port: 9000

---
# AuthorizationPolicy에서 CUSTOM action으로 사용
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: ext-authz
  namespace: production
spec:
  selector:
    matchLabels:
      app: order-service
  action: CUSTOM
  provider:
    name: my-ext-authz
  rules:
    - to:
        - operation:
            paths: ["/api/orders/*"]
```

신규 프로젝트라면 EnvoyFilter로 직접 ext_authz 필터를 삽입하는 대신 이 공식 방법을 우선 사용한다. 기존에 EnvoyFilter로 ext_authz를 설정한 경우에는 ExtensionProvider 방식으로 마이그레이션하는 것이 장기적으로 유지보수가 편하다.
