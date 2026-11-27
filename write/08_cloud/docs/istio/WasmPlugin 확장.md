---
title: WasmPlugin 확장 — 선언적 필터 배치·모듈 배포·실패 정책
tags: [istio, wasm, wasmplugin, ecds, envoy, extensibility]
status: draft
source:
  - https://istio.io/v1.32/docs/concepts/wasm/
  - https://istio.io/v1.32/docs/reference/config/proxy_extensions/wasm-plugin/
  - https://istio.io/v1.32/docs/tasks/extensibility/wasm-modules/
  - https://istio.io/v1.32/docs/ops/configuration/extensibility/wasm-pull-policy/
  - https://istio.io/v1.32/docs/reference/config/proxy_extensions/traffic_extension/
  - https://istio.io/v1.32/docs/reference/commands/pilot-agent/
  - https://istio.io/v1.32/docs/reference/config/istio.mesh.v1alpha1/
  - https://istio.io/v1.32/docs/ops/integrations/prometheus/
  - https://github.com/istio/istio/blob/1.32.0/pkg/wasm/convert.go
related:
  - ./README.md
  - ../../book/istio-in-action/14-01.Envoy를 새로 빌드하지 않으려고 낸 네 개의 문.md
  - ./xDS 동기화 프로토콜.md
updated: 2026-11-27
---

# WasmPlugin 확장 — 선언적 필터 배치·모듈 배포·실패 정책

---

> `WasmPlugin` 은 Envoy 내부 좌표를 직접 패치하지 않고 `phase`·`priority` 와 모듈 `url` 선언만으로 프록시에 WebAssembly(Wasm) 필터를 싣는 Istio 리소스입니다. 이 문서는 주요 필드, `istio-agent` 의 ECDS 기반 모듈 배포와 캐시 흐름, 대안 확장 방식과의 선택 기준을 Istio 1.32 공식 문서 기준으로 정리합니다.

근거는 Istio 1.32 공식 개념·레퍼런스·태스크·운영 문서입니다. 규칙과 기본값은 주로 1.32 문서 문장에서 가져왔습니다. 모듈 가져오기 실패 처리와 루트 네임스페이스 기본값은 1.32.0 소스로 확인했습니다.

Istio 1.32 의 Wasm 모듈 태스크와 풀 정책 문서는 이 기능을 아직 **Alpha** 단계로 표시합니다.[^wasm-task][^pull-policy]

실제 클러스터에서 리소스를 적용해 확인하지는 않았습니다. YAML 예시는 1.32 레퍼런스 스키마에 맞춰 문법만 대조했습니다.

Envoy 필터 체인 구조와 Proxy-Wasm 이 커스텀 Envoy 빌드를 피하는 배경은 [14-01 노트](../../book/istio-in-action/14-01.Envoy%EB%A5%BC%20%EC%83%88%EB%A1%9C%20%EB%B9%8C%EB%93%9C%ED%95%98%EC%A7%80%20%EC%95%8A%EC%9C%BC%EB%A0%A4%EA%B3%A0%20%EB%82%B8%20%EB%84%A4%20%EA%B0%9C%EC%9D%98%20%EB%AC%B8.md)가 맡습니다.

## 1. EnvoyFilter 와의 차이와 등장 배경

> `EnvoyFilter` 로 Wasm 모듈을 올리면 Envoy 내부 필터 이름과 xDS 버전 변경에 직접 묶여 업그레이드 때마다 설정이 깨집니다. `WasmPlugin` 은 배치 위치·모듈 주소·실패 정책을 Istio 추상화로 분리합니다.

`EnvoyFilter` 로 커스텀 필터를 넣으면 리스너 포트와 `http_connection_manager` 를 직접 짚어야 합니다. `router` 서브필터 이름과 원격 클러스터 정의도 xDS 패치에 따로 적어야 합니다.

Istio 프록시 버전이 올라 내부 필터 구조가 바뀌면 이 패치가 어긋나거나 프록시 기동이 막힙니다. `EnvoyFilter` 의 하위 호환성 한계는 [14-01 노트 §3](../../book/istio-in-action/14-01.Envoy%EB%A5%BC%20%EC%83%88%EB%A1%9C%20%EB%B9%8C%EB%93%9C%ED%95%98%EC%A7%80%20%EC%95%8A%EC%9C%BC%EB%A0%A4%EA%B3%A0%20%EB%82%B8%20%EB%84%A4%20%EA%B0%9C%EC%9D%98%20%EB%AC%B8.md) 이 다룹니다.

**WasmPlugin** 은 WebAssembly 필터 배포와 배치를 전담하는 선언적 리소스입니다.[^wasm-ref] 사용자는 내부 필터 이름 대신 실행 단계(`phase`)와 우선순위(`priority`)만 고릅니다. 모듈 주소(`url`)를 적으면 에이전트가 내려받아 캐시하므로 원격 클러스터를 짤 필요가 없습니다.

실행 격리 방식도 다릅니다. Proxy-Wasm 모듈은 Envoy 안에 내장된 V8 **샌드박스(sandbox)** VM 에서 돕니다.[^wasm-concept] 플러그인 하나가 충돌하거나 예외를 내도 다른 플러그인이나 Envoy 워커 스레드는 멈추지 않습니다.

Istio 1.30 은 Wasm 과 인라인 Lua 를 묶은 `TrafficExtension` 을 도입했습니다.[^wasm-concept][^te-blog] API 그룹은 같은 `extensions.istio.io/v1alpha1` 입니다. 1.32 공식 문서도 `TrafficExtension` 을 기본 API 로 안내하며 `WasmPlugin` 도 내부 변환을 거쳐 그대로 지원합니다.[^te-blog]



## 2. WasmPlugin 필드와 적용 범위

> `WasmPlugin` 은 API 그룹 `extensions.istio.io/v1alpha1` 에 속합니다. 적용 대상, 모듈 위치, 체인 순서, 실패 정책을 각각 독립 필드로 선언합니다.

### 대상 선택: selector · targetRefs

적용 범위는 `selector` 나 `targetRefs` 중 하나로 정합니다. 한 리소스에 두 필드를 동시에 적을 수 없습니다.[^wasm-ref]

`selector` 는 레이블 셀렉터로 파드나 VM 워크로드를 고릅니다. `selector` 를 비우면 리소스가 놓인 네임스페이스의 모든 워크로드에 걸립니다.[^wasm-ref]

리소스를 설정 루트 네임스페이스에 두면 메시의 모든 네임스페이스 워크로드에 적용됩니다.[^wasm-ref] `meshConfig.rootNamespace` 의 기본값은 `istio-system` 입니다.[^mesh-root] `istio-config` 같은 다른 이름은 루트 네임스페이스 값이 그 이름일 때만 전역으로 동작합니다.

값은 `meshConfig.rootNamespace` 로 직접 지정할 수 있습니다. Helm 차트는 이 값이 비면 `global.istioNamespace` 를 채웁니다.[^mesh-root] 그래서 `global.istioNamespace` 를 `istio-config` 로 두고 설치하면 따로 지정하지 않아도 그 이름이 루트가 됩니다. 이 값의 기본은 `istio-system` 이며 `helm -n` 으로 준 설치 네임스페이스를 따라가지 않습니다.[^mesh-root]

`targetRefs` 는 레이블 셀렉터로 잡히지 않는 리소스에 붙입니다. Ambient 모드의 waypoint 프록시는 `selector` 를 무시하므로 `targetRefs` 가 필수입니다.[^wasm-ref]

Istio 1.32 에서 `targetRefs` 가 지원하는 대상은 넷입니다.[^wasm-ref]

- `Gateway`: `gateway.networking.k8s.io` 그룹, 같은 네임스페이스 대상
- `GatewayClass`: `gateway.networking.k8s.io` 그룹, 루트 네임스페이스 대상
- `Service`: 코어 그룹(`""` 또는 `"core"`), 같은 네임스페이스 대상이며 waypoint 전용
- `ServiceEntry`: `networking.istio.io` 그룹, 같은 네임스페이스 대상

### 모듈 경로와 imagePullPolicy

`url` 은 필수 문자열이며 Wasm 모듈이나 OCI(Open Container Initiative) 이미지 위치를 가리킵니다.[^wasm-ref] 스킴을 생략하면 OCI 이미지를 뜻하는 `oci://` 로 해석합니다.

- `oci://`: OCI 레지스트리에 올린 Wasm 이미지
- `http://` · `https://`: 원격 HTTP 서버에 호스팅된 `.wasm` 바이너리
- `file://`: 프록시 컨테이너 내부 로컬 파일 경로

비공개 레지스트리는 같은 네임스페이스의 Docker pull 시크릿 이름을 `imagePullSecret` 에 적습니다.[^wasm-ref] 무결성을 확인하려면 `sha256` 필드에 64자리 체크섬을 둡니다. `url` 에 `@sha256:` 다이제스트가 있으면 `sha256` 값과 같아야 합니다.

`imagePullPolicy` 는 Kubernetes 풀 정책과 같은 이름을 씁니다.[^pull-policy] 기본 정책은 `UNSPECIFIED_POLICY` 로 지정되며 보통 `IfNotPresent` 로 동작합니다. 예외로 OCI 이미지 태그가 `:latest` 이면 기본값이 `Always` 로 바뀝니다.[^wasm-ref][^pull-policy]

`sha256` 필드나 `@sha256:` 다이제스트가 있으면 풀 정책은 덮어쓰입니다. 이 경우 `imagePullPolicy` 값과 무관하게 `IfNotPresent` 가 적용됩니다.[^pull-policy]

`Always` 는 파드가 뜰 때만 다시 받는 Kubernetes 와 뜻이 다릅니다. `WasmPlugin` 에서는 리소스의 `spec` 이나 `metadata` 가 바뀔 때마다 모듈을 새로 받습니다.[^pull-policy]

### 실행 순서와 match 조건

`phase` 는 Envoy 필터 체인 안에서 플러그인이 들어갈 큰 구간을 고릅니다.[^wasm-ref]

| `phase` 값 | 필터 체인 삽입 위치 |
|---|---|
| `AUTHN` | Istio 인증 필터 앞 |
| `AUTHZ` | Istio 인증 필터 뒤이자 인가 필터 앞 |
| `STATS` | Istio 인가 필터 뒤이자 통계 필터 앞 |
| `UNSPECIFIED_PHASE` | 기본값. 컨트롤 플레인이 결정하며 보통 체인 끝 `router` 바로 앞 |

같은 `phase` 안에 여러 `WasmPlugin` 이 걸리면 `priority` 로 순서를 가릅니다. 32비트 정수이며 기본값은 `0` 입니다. 숫자가 큰 플러그인이 먼저 돌고, 값이 같으면 이름과 네임스페이스로 순서를 고정합니다.[^wasm-ref]

`match` 는 `TrafficSelector` 배열로 적용할 트래픽 방향과 포트를 좁힙니다.[^wasm-ref] `mode` 기본값은 `CLIENT_AND_SERVER` 입니다. `CLIENT`(아웃바운드) 나 `SERVER`(인바운드) 로 좁힐 수 있고, 게이트웨이에는 `CLIENT` 나 `CLIENT_AND_SERVER` 를 씁니다.

`ports` 를 비우면 모든 포트에 적용됩니다. `type` 은 L7 필터(`HTTP`)와 L4 필터(`NETWORK`) 중 하나를 고릅니다. 비우면 `UNSPECIFIED_PLUGIN_TYPE` 이 `HTTP` 로 동작합니다.[^wasm-ref]

### 설정 · 환경 · failStrategy

`pluginConfig` 에 적은 YAML 구조는 JSON 으로 직렬화되어 모듈 설정 콜백으로 넘어갑니다.[^wasm-ref][^wasm-alpha] 일부 `.wasm` 모듈은 `pluginName`(구 `rootID`) 으로 실행할 플러그인을 고르라고 요구합니다.

`vmConfig.env` 는 Wasm VM 안에 환경변수를 주입합니다.[^wasm-ref] 리터럴 값을 직접 주는 `INLINE`(`value`) 과 프록시 환경변수를 넘기는 `HOST`(`valueFrom: HOST`) 중 고릅니다.

`failStrategy` 는 바이너리 가져오기 실패나 실행 중 VM 중단(fatal error) 시 프록시 동작을 정합니다.[^wasm-ref]

| `failStrategy` 값 | 동작 | 주의점 |
|---|---|---|
| `FAIL_CLOSE` | 실행 오류 시 이후 요청을 5xx 로 실패 처리 | 인증·인가 플러그인의 안전한 기본 선택 |
| `FAIL_OPEN` | 복구할 수 없는 오류 시 플러그인을 건너뛰고 요청을 통과 | 인증·인가 플러그인에는 권장하지 않음 |
| `FAIL_RELOAD` | `proxy_wasm::FailState::RuntimeError` 발생 시 다음 요청에 새 인스턴스 생성 | 그 밖의 오류는 `FAIL_CLOSE` 로 폴백 |

레퍼런스는 `FAIL_CLOSE` 의 5xx 설명에 바이너리 가져오기 실패도 넣습니다.[^wasm-ref] 1.32.0 소스의 가져오기 실패 경로는 응답 코드가 다르며 3절에서 다룹니다.



## 3. ECDS 기반 모듈 배포와 캐시

> `istiod` 는 원격 모듈 주소를 담은 ECDS 설정만 내리고, 실제 다운로드·검증·로컬 캐시는 사이드카의 `istio-agent` 가 도맡습니다. 성공하면 Envoy 는 로컬 파일 경로를 넘겨받고, 가져오기나 검증이 실패하면 RBAC 대체 필터를 넘겨받습니다.

이 과정에는 `istiod`, `istio-agent`, `OCI 레지스트리`, `Envoy` 가 순서대로 관여합니다.

![istiod 가 ECDS 로 설정을 내리면 istio-agent 가 OCI 모듈을 받아 캐시하고 Envoy 가 AUTHN 자리에 로드한다](./_assets/WasmPlugin%20%ED%99%95%EC%9E%A5.ecds-pull-flow.svg)

위 흐름은 성공 경로와 실패 경로가 `ALT` 프레임에서 갈립니다. 아래쪽 실패 분기처럼 에이전트가 가져오기에 실패하면 Wasm 설정 대신 RBAC 대체 필터가 Envoy 로 내려갑니다.

### 단계별 전달과 ECDS 재작성

`istiod` 는 `WasmPlugin` 을 Envoy 의 **ECDS**(Extension Configuration Discovery Service) 설정으로 바꿉니다.[^wasm-alpha][^wasm-task] ECDS 는 리스너 전체를 다시 밀지 않고 필터 설정만 동적으로 주고받는 xDS API 입니다.

사이드카와 게이트웨이의 `istio-agent`(`pilot-agent`) 는 `istiod` 와 Envoy 사이의 xDS 프록시입니다.[^pilot-agent] `ISTIO_AGENT_ENABLE_WASM_REMOTE_LOAD_CONVERSION` 이 기본값 `true` 면 에이전트가 ECDS 응답을 가로챕니다.

에이전트는 ECDS 안의 원격 `url` 힌트를 읽고 OCI 레지스트리나 HTTP 서버에서 모듈을 내려받습니다. `sha256` 이 있으면 체크섬을 대조하고 통과한 바이너리를 로컬 디스크에 캐시합니다.[^wasm-alpha][^wasm-task]

다운로드와 검증이 끝나면 에이전트는 원격 주소를 로컬 `file://` 경로로 바꿔 Envoy 에 넘깁니다.[^pilot-agent][^wasm-task] Envoy 는 V8 VM 에 모듈을 올리고 `phase` 와 `priority` 자리에 필터를 붙입니다.

### 캐시 수명·실패 처리·관측 메트릭

캐시된 모듈의 수명은 파드 수명을 넘지 않습니다.[^pull-policy] 쓰이지 않는 모듈은 일정 시간 뒤 지워집니다. 지우는 주기와 다운로드 한도를 정하는 `pilot-agent` 환경변수는 다섯입니다.[^pilot-agent][^pull-policy]

- `WASM_MODULE_EXPIRY`: 캐시 만료 기간 (기본 `24h0m0s`)
- `WASM_PURGE_INTERVAL`: 만료 검사 주기 (기본 `1h0m0s`)
- `WASM_HTTP_REQUEST_TIMEOUT`: HTTP(S) 요청 타임아웃 (기본 `15s`)
- `WASM_HTTP_REQUEST_MAX_RETRIES`: HTTP(S) 최대 재시도 횟수 (기본 `5`)
- `ISTIO_WASM_MAX_BINARY_SIZE_BYTES`: 최대 Wasm 바이너리 크기 (기본 `268435456`, 256MB)

다운로드나 체크섬 검증이 실패해도 `istio-agent` 는 그 이유로 ECDS 를 NACK 하지 않습니다. 해당 리소스를 같은 이름의 RBAC 대체 필터로 바꿔 Envoy 에 넘깁니다.[^wasm-src] 어떤 필터가 내려갈지는 2절의 `failStrategy` 가 가릅니다.

- `FAIL_OPEN`: 규칙이 없는 allow-all RBAC 필터가 내려가 요청이 플러그인 없이 지나갑니다.[^wasm-src]
- `FAIL_CLOSE`(기본)·`FAIL_RELOAD`: 빈 규칙을 둔 deny-all RBAC 필터가 내려갑니다.[^wasm-src] HTTP 필터는 `403`(`RBAC: access denied`)을 돌려주고 `NETWORK` 필터는 연결을 닫습니다.[^rbac-deny]

NACK 은 에이전트가 ECDS 리소스를 해석하지 못하거나 대체 필터를 만들지 못할 때 나갑니다.[^wasm-src]

1.32 태스크 문서는 다운로드 실패 등으로 설정이 거부되면 `pilot_total_xds_rejects` 가 오른다고 적습니다.[^wasm-task] 1.32.0 소스의 다운로드 실패 경로는 거부하지 않으므로 이 메트릭만으로는 가져오기 실패를 찾을 수 없습니다.[^wasm-src] 대신 에이전트 로그 `error in converting the wasm config to local` 을 봅니다.[^wasm-src] 아래의 `istio_agent_wasm_remote_fetch_count` 결과 값도 함께 봅니다.

모듈을 가져온 뒤의 실행 오류는 에이전트가 아니라 Envoy 가 처리합니다. `istiod` 가 `failStrategy` 를 Envoy 의 `failure_policy` 로 옮겨 설정에 담기 때문입니다.[^wasm-src] 이때의 동작은 2절 표를 따릅니다.[^wasm-ref]

모듈 배포 상태는 `istio-agent` 가 여는 메트릭 다섯으로 확인합니다.[^wasm-task][^pilot-agent]

- `istio_agent_wasm_cache_lookup_count`: 원격 fetch 캐시 조회 횟수
- `istio_agent_wasm_cache_entries`: 원격 fetch 캐시에 담긴 항목 수를 나타내는 gauge[^wasm-metrics]
- `istio_agent_wasm_config_conversion_count`: Wasm 설정 변환 횟수와 결과(성공, 원격 로드 없음, 마샬·언마샬 실패, fetch 실패, 원격 힌트 누락)[^wasm-metrics]
- `istio_agent_wasm_config_conversion_duration_bucket`: 에이전트가 Wasm 설정을 변환하는 데 쓴 시간 분포(ms)
- `istio_agent_wasm_remote_fetch_count`: 원격 모듈 fetch 횟수와 결과(성공, 다운로드 실패, 체크섬 불일치)

사이드카와 게이트웨이에서 Envoy 자체 통계는 포트 `15090` 이 엽니다. 위 에이전트 메트릭과 Envoy 메트릭을 합친 Prometheus 엔드포인트는 포트 `15020` 의 `/stats/prometheus` 입니다.[^port-ref]



## 4. 다른 확장 방식과의 선택 기준

> 프록시 안 샌드박스에서 커스텀 로직을 돌릴 때는 `WasmPlugin`, 외부 서비스로 판정을 넘길 때는 `ext_authz` 나 `ext_proc`, 내장 Envoy 필터만 켤 때는 `EnvoyFilter` 를 고릅니다.

같은 "커스텀 Envoy 빌드 피하기" 문제라도 로직이 실행되는 위치와 Istio 1급 API 지원 여부가 다릅니다. 아래 표는 Istio 1.32 에서 자주 맞대는 네 방식을 네 축으로 비교합니다.

| 방식 | 실행 위치 · 구현 형태 | Istio API 지원 | 장애 격리 · 요청 홉 | 주로 쓰는 경우 |
|---|---|---|---|---|
| `WasmPlugin` | 프록시 내부 V8 샌드박스 VM(C++·Rust·Go·AssemblyScript) | 1급 CRD (`extensions.istio.io/v1alpha1`) | VM 격리 · 네트워크 홉 없음 · `failStrategy` 선택 | 커스텀 인증 토큰 파싱·헤더/본문 변환·재사용 모듈 |
| `EnvoyFilter` | 프록시 내부 내장 C++ 필터 패치 | 저수준 API (`networking.istio.io/v1alpha3`) | 프록시 설정 직접 변경 · 업그레이드 호환성 부담 | 상위 Istio API 가 노출하지 않는 기존 Envoy 필터 활성화 |
| `ext_authz` | 메시 안팎의 외부 HTTP/gRPC 인가 서버 | 1급 지원 (`MeshConfig` + `AuthorizationPolicy CUSTOM`) | 네트워크 홉 1개 추가 · 외부 서버 운영 필요 | OPA·`oauth2-proxy` 같은 외부 인가 시스템 연동 |
| `ext_proc` | 메시 안팎의 외부 양방향 gRPC 스트림 서버 | 1.32 `ExtensionProvider` 미지원(`EnvoyFilter` 필요) | 네트워크 홉 1개 추가 · 스트림 상태 관리 | 외부 서버에서 요청·응답 헤더·본문·트레일러를 동적 변조 |

`ext_authz` 는 `MeshConfig.extensionProviders` 에 `envoyExtAuthzHttp` 나 `envoyExtAuthzGrpc` 로 등록합니다. 호출 연결은 `AuthorizationPolicy` 의 `action: CUSTOM` 이 맡습니다.[^ext-authz-task]

반면 `ext_proc` 은 Istio 1.32 `ExtensionProvider` 목록에 아직 없습니다.[^mesh-ext] 그래서 `EnvoyFilter` 로 `envoy.filters.http.ext_proc` 필터를 직접 붙여야 합니다.[^ext-proc]

짧은 헤더 조작처럼 배포 파이프라인 없이 인라인 코드로 끝낼 일은 Lua 가 가볍습니다. 1.32 공식 벤치마크에서 Lua 는 동시성 1~16 구간에서 메모리를 약 20~26 MiB 씁니다. 같은 조건에서 Wasm 은 약 118~292 MiB 까지 늘어납니다.[^wasm-concept]

대신 Lua 는 Envoy 워커 스레드 안에서 돌아 fail-open 만 지원합니다. 1.32 에서는 `TrafficExtension` 의 `lua.inlineCode` 로 설정합니다.[^wasm-concept]



## 5. 공식 basic_auth 예시 YAML

> 공식 문서의 HTTP Basic 인증 예제를 `WasmPlugin` 리소스로 옮긴 구성입니다. `phase: AUTHN` 자리에 `basic_auth` 모듈을 꽂아 `/productpage` 경로를 보호합니다.

아래 YAML 은 단독 적용 가능한 예시입니다. Istio 1.32 `Executing WebAssembly Modules` 태스크는 같은 `basic_auth` 예제를 `TrafficExtension` (`spec.wasm.url`) 으로 적습니다.[^wasm-task] 여기서는 `WasmPlugin` 스키마에 맞춰 `url` 과 `pluginConfig` 를 `spec` 바로 아래에 두었습니다.[^wasm-ref]

```yaml
# 인그레스 게이트웨이의 AUTHN 단계에 HTTP Basic 인증 Wasm 필터를 붙입니다.
apiVersion: extensions.istio.io/v1alpha1
kind: WasmPlugin
metadata:
  name: basic-auth
  namespace: istio-system  # 기본 루트 네임스페이스이므로 전체 네임스페이스에 걸칩니다.
spec:
  selector:
    matchLabels:
      istio: ingressgateway  # 인그레스 게이트웨이 파드만 대상으로 삼습니다.
  phase: AUTHN  # Istio 기본 인증 필터보다 앞에서 실행합니다.
  url: oci://ghcr.io/istio-ecosystem/wasm-extensions/basic_auth:1.12.0
  imagePullPolicy: IfNotPresent  # 명시적 버전 태그이므로 로컬 캐시가 있으면 재사용합니다.
  pluginConfig:
    basic_auth_rules:
      - prefix: "/productpage"
        request_methods:
          - "GET"
          - "POST"
        credentials:
          - "ok:test"
          - "YWRtaW4zOmFkbWluMw=="  # Base64 로 인코딩한 자격 증명 예시입니다.
```

이 구성이 적용되면 인증 헤더 없는 `/productpage` 요청은 게이트웨이에서 `401` 응답으로 막힙니다.[^wasm-task] 반대로 유효한 `Authorization: Basic` 헤더(`YWRtaW4zOmFkbWluMw==`)를 실어 보내면 `200` 응답을 받습니다.[^wasm-task]

인증 필터이므로 `failStrategy` 는 `FAIL_OPEN` 을 피하고 기본 `FAIL_CLOSE` 를 유지해야 모듈 로드 실패 시 우회 통과를 막을 수 있습니다.[^wasm-ref][^wasm-concept]



## 관련 문서

> 이 문서가 딛고 서거나 이어지는 이웃입니다.

- [Istio 공식문서 정독 인덱스](./README.md) — 이 폴더의 문서 목록
- [Envoy를 새로 빌드하지 않으려고 낸 네 개의 문](../../book/istio-in-action/14-01.Envoy를%20새로%20빌드하지%20않으려고%20낸%20네%20개의%20문.md) — `EnvoyFilter`·Lua·전역 레이트 리미팅·Wasm 네 문을 나란히 비교한 정독 노트
- [xDS 동기화 프로토콜](./xDS%20동기화%20프로토콜.md) — `istiod` 와 Envoy 가 xDS 응답을 ACK·NACK 으로 주고받는 원리



## 참고 자료

> 본문에서 인용한 1차 자료입니다. Istio 문서 주소는 1.32 판으로 고정했습니다.

- [Istio 1.32 — Extensibility 개념](https://istio.io/v1.32/docs/concepts/wasm/) — Wasm 샌드박스 목표, Lua 와 메모리·격리 비교
- [Istio 1.32 — WasmPlugin 레퍼런스](https://istio.io/v1.32/docs/reference/config/proxy_extensions/wasm-plugin/) — `extensions.istio.io/v1alpha1` 전체 필드, `phase`, `priority`, `failStrategy`, `targetRefs`
- [Istio 1.32 — Executing WebAssembly Modules](https://istio.io/v1.32/docs/tasks/extensibility/wasm-modules/) — `basic_auth` 예제, `istio_agent_wasm_*`·`pilot_total_xds_rejects` 메트릭
- [Istio 1.32 — Pull Policy for WebAssembly Modules](https://istio.io/v1.32/docs/ops/configuration/extensibility/wasm-pull-policy/) — `imagePullPolicy` 예외 규칙, `Always` 동작, 캐시 만료
- [Istio 1.32 — Introducing the TrafficExtension API](https://istio.io/v1.32/blog/2026/traffic-extension-api/) — Istio 1.30+ 의 `TrafficExtension` 도입과 `WasmPlugin` 내부 변환
- [Istio 1.32 — pilot-agent 레퍼런스](https://istio.io/v1.32/docs/reference/commands/pilot-agent/) — Wasm 원격 로드 변환·캐시 만료·타임아웃 환경변수와 메트릭
- [Istio 1.32.0 소스 — `pkg/wasm/convert.go`](https://github.com/istio/istio/blob/1.32.0/pkg/wasm/convert.go) — 모듈 가져오기 실패 시 RBAC 대체 필터와 NACK 조건

[^wasm-ref]: Istio 1.32 — WasmPlugin 레퍼런스. `apiVersion: extensions.istio.io/v1alpha1`. `selector` 와 `targetRefs` 는 상호 배타적이며, 설정 루트 네임스페이스에 두면 모든 네임스페이스에 적용됩니다. `url` 은 스킴 생략 시 `oci://` 가 기본입니다. <https://istio.io/v1.32/docs/reference/config/proxy_extensions/wasm-plugin/> (2026-11-27 조회)
[^wasm-concept]: Istio 1.32 — Extensibility 개념. Proxy-Wasm 은 V8 샌드박스 VM 에서 돌아 플러그인 장애를 격리합니다. 동시성 1~16 벤치마크에서 Lua 는 약 20~26 MiB(19.79~25.66 MiB), Wasm 은 약 118~292 MiB(117.7~291.8 MiB) 를 사용합니다. <https://istio.io/v1.32/docs/concepts/wasm/> (2026-11-27 조회)
[^te-blog]: Istio 1.32 — Introducing the TrafficExtension API. Istio 1.30 이 `TrafficExtension` 을 도입해 `WasmPlugin` 을 대체하는 기본 API 가 됐으나, 기존 `WasmPlugin` 은 내부에서 `TrafficExtension` 으로 변환되어 그대로 동작합니다. <https://istio.io/v1.32/blog/2026/traffic-extension-api/> (2026-11-27 조회)
[^mesh-root]: Istio 1.32.0 소스, `pkg/config/mesh/mesh.go` 의 `DefaultMeshConfig`. `RootNamespace` 기본값은 `constants.IstioSystemNamespace`(`istio-system`)입니다. <https://github.com/istio/istio/blob/1.32.0/pkg/config/mesh/mesh.go#L91> Helm 차트는 `meshConfig.rootNamespace` 가 비면 `global.istioNamespace` 값을 채웁니다. <https://github.com/istio/istio/blob/1.32.0/manifests/charts/istio-control/istio-discovery/templates/configmap.yaml#L10> `global.istioNamespace` 의 차트 기본값은 `istio-system` 입니다. <https://github.com/istio/istio/blob/1.32.0/manifests/charts/istio-control/istio-discovery/values.yaml#L239> (2026-11-27 조회)
[^pull-policy]: Istio 1.32 — Pull Policy for WebAssembly Modules. `sha256` 또는 `@sha256:` 다이제스트 지정 시 `IfNotPresent` 로 덮어쓰이며, `:latest` 태그는 기본이 `Always` 입니다. `Always` 는 `spec` 과 `metadata` 변경 모두에 반응합니다. <https://istio.io/v1.32/docs/ops/configuration/extensibility/wasm-pull-policy/> (2026-11-27 조회)
[^wasm-alpha]: Istio 1.32 — Announcing the alpha availability of WebAssembly Plugins. `pluginConfig` 는 JSON 으로 인코딩되어 SDK 설정 콜백으로 넘어갑니다. `istio-agent` 는 ECDS 를 이용해 OCI 이미지를 내려받아 캐시합니다. 원격 fetch 가 실패해도 Envoy 가 깨진 설정에 묶일 걱정이 없다고 설명합니다. <https://istio.io/v1.32/blog/2021/wasm-api-alpha/> (2026-11-27 조회)
[^wasm-task]: Istio 1.32 — Executing WebAssembly Modules. `basic_auth` (`oci://ghcr.io/istio-ecosystem/wasm-extensions/basic_auth:1.12.0`) 예제와 `istio_agent_wasm_*`, `pilot_total_xds_rejects` 메트릭을 다룹니다. 이 기능은 Alpha 로 표시돼 있습니다. <https://istio.io/v1.32/docs/tasks/extensibility/wasm-modules/> (2026-11-27 조회)
[^pilot-agent]: Istio 1.32 — pilot-agent 레퍼런스. `ISTIO_AGENT_ENABLE_WASM_REMOTE_LOAD_CONVERSION`(기본 `true`), `WASM_MODULE_EXPIRY`(`24h0m0s`), `WASM_PURGE_INTERVAL`(`1h0m0s`), `WASM_HTTP_REQUEST_TIMEOUT`(`15s`), `WASM_HTTP_REQUEST_MAX_RETRIES`(`5`), `ISTIO_WASM_MAX_BINARY_SIZE_BYTES`(`268435456`) 정의가 있습니다. <https://istio.io/v1.32/docs/reference/commands/pilot-agent/> (2026-11-27 조회)
[^wasm-src]: Istio 1.32.0 소스. 변환 실패 시 RBAC 대체 필터를 만들고 해석 실패·대체 필터 생성 실패만 오류로 돌려줍니다(`pkg/wasm/convert.go` L70–200). <https://github.com/istio/istio/blob/1.32.0/pkg/wasm/convert.go#L100-L200> 에이전트는 이 오류가 있을 때만 NACK 합니다(`pkg/istio-agent/xds_proxy.go` L536–551, delta 는 `xds_proxy_delta.go` L269–293). <https://github.com/istio/istio/blob/1.32.0/pkg/istio-agent/xds_proxy.go#L536-L551> `failStrategy` 는 `pilot/pkg/model/extensions.go` L260–267 에서 `failure_policy` 로 옮깁니다. <https://github.com/istio/istio/blob/1.32.0/pilot/pkg/model/extensions.go#L260-L267> (2026-11-27 조회)
[^wasm-metrics]: Istio 1.32.0 소스, `pkg/wasm/monitoring.go`. `wasm_cache_entries` 는 `NewGauge` 로 만든 "number of Wasm remote fetch cache entries." 입니다(L40–43). 변환 횟수와 결과는 `NewSum` 인 `wasm_config_conversion_count` 가 셉니다(L55–58, 결과 값은 L28–33). <https://github.com/istio/istio/blob/1.32.0/pkg/wasm/monitoring.go#L28-L58> 접두사 `istio_agent_` 는 `pilot-agent` 가 붙입니다. <https://github.com/istio/istio/blob/1.32.0/pilot/cmd/pilot-agent/status/server.go#L181> 1.32 태스크 문서는 변환 결과 설명을 `istio_agent_wasm_cache_entries` 에 달아 놓아 소스와 다릅니다. (2026-11-27 조회)
[^rbac-deny]: Envoy 커밋 `56e0748`(Istio 1.32.0 이 고정한 istio/proxy 의 Envoy). `rules` 를 설정하고 비우면 모든 요청을 거부합니다. <https://github.com/envoyproxy/envoy/blob/56e0748e3deaeb8af7efcbf2f97329bb15539767/api/envoy/extensions/filters/http/rbac/v3/rbac.proto#L32> HTTP 필터는 `403` 을 보내고 <https://github.com/envoyproxy/envoy/blob/56e0748e3deaeb8af7efcbf2f97329bb15539767/source/extensions/filters/http/rbac/rbac_filter.cc#L234> 네트워크 필터는 연결을 닫습니다. <https://github.com/envoyproxy/envoy/blob/56e0748e3deaeb8af7efcbf2f97329bb15539767/source/extensions/filters/network/rbac/rbac_filter.cc#L157> (2026-11-27 조회)
[^port-ref]: Istio 1.32 — Prometheus 연동. Istio 메트릭을 앱 메트릭과 합쳐 `:15020/stats/prometheus` 에서 긁습니다. <https://istio.io/v1.32/docs/ops/integrations/prometheus/> (2026-11-27 조회). Envoy 메트릭 포트 `ENVOY_PROMETHEUS_PORT` 기본값 `15090` 은 pilot-agent 레퍼런스에 있습니다. 포트 지도는 [부록 포트 지도](../../book/istio-in-action/a0-04.부록%20—%20포트%20열넷과%20디버그%20엔드포인트%20지도.md)
[^ext-authz-task]: Istio 1.32 — External Authorization 태스크. `MeshConfig.extensionProviders` 에 `envoyExtAuthzGrpc` 나 `envoyExtAuthzHttp` 를 정의하고 `AuthorizationPolicy` 의 `action: CUSTOM` 으로 호출합니다. <https://istio.io/v1.32/docs/tasks/security/authorization/authz-custom/> (2026-11-27 조회)
[^mesh-ext]: Istio 1.32 — MeshConfig `ExtensionProvider` 레퍼런스. `envoyExtAuthzHttp` 와 `envoyExtAuthzGrpc` 는 있으나 `ext_proc` 전용 필드는 없습니다. <https://istio.io/v1.32/docs/reference/config/istio.mesh.v1alpha1/> (2026-11-27 조회)
[^ext-proc]: Envoy — External Processing 필터 문서. 양방향 gRPC 스트림으로 `ProcessingRequest` 와 `ProcessingResponse` 를 주고받으며 헤더·본문·트레일러를 검사·수정합니다. <https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/ext_proc_filter> (2026-11-27 조회)
