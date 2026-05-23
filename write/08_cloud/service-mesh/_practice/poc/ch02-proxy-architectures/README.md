# Ch02 - 프록시 아키텍처 실습
---
> 대응 학습 문서: `learning/02-proxy-architectures/LEARN.md`

## 사전 조건

- Docker Desktop 실행 중
- curl 설치
- httpbin 이미지 접근 가능 (`docker pull kennethreitz/httpbin`)

## 실습 항목

| # | 개념 | 실습 내용 | 검증 방법 |
|---|------|----------|----------|
| 1 | Envoy 단독 실행 | Docker로 Envoy 컨테이너 기동 | `curl localhost:10000` |
| 2 | Static config 프록시 | httpbin을 upstream으로 설정 | 요청이 httpbin으로 전달됨 확인 |
| 3 | Admin API 탐색 | `/stats`, `/clusters`, `/config_dump` | JSON 응답 확인 |
| 4 | Retry 통계 확인 | retry 설정 후 `/stats`에서 카운터 확인 | `retry.upstream_rq_retry` 증가 |
| 5 | Dynamic config | filesystem watcher로 설정 핫 리로드 | 재시작 없이 변경 반영 |
| 6 | 용어 매핑 실습 | config에서 listener/route/cluster/endpoint 직접 찾기 | 각 블록 위치 식별 |

## 실습 상세

### 1. Envoy 단독 실행

**목표**: Envoy를 Docker 컨테이너로 기동하고 기본 동작을 확인한다.

**단계**:
1. 작업 디렉토리 생성
   ```bash
   mkdir -p /tmp/envoy-lab && cd /tmp/envoy-lab
   ```
2. 최소 static config 작성 (`envoy-static.yaml`)
   ```yaml
   static_resources:
     listeners:
       - name: listener_0
         address:
           socket_address: { address: 0.0.0.0, port_value: 10000 }
         filter_chains:
           - filters:
               - name: envoy.filters.network.http_connection_manager
                 typed_config:
                   "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
                   stat_prefix: ingress_http
                   route_config:
                     name: local_route
                     virtual_hosts:
                       - name: local_service
                         domains: ["*"]
                         routes:
                           - match: { prefix: "/" }
                             direct_response:
                               status: 200
                               body:
                                 inline_string: "Hello from Envoy!\n"
                   http_filters:
                     - name: envoy.filters.http.router
                       typed_config:
                         "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
     clusters: []

   admin:
     address:
       socket_address: { address: 0.0.0.0, port_value: 15000 }
   ```
3. Envoy 기동
   ```bash
   docker run --rm -d \
     --name envoy-lab \
     -p 10000:10000 \
     -p 15000:15000 \
     -v /tmp/envoy-lab/envoy-static.yaml:/etc/envoy/envoy.yaml \
     envoyproxy/envoy:v1.29-latest
   ```

**검증**:
```bash
curl localhost:10000
# Hello from Envoy!
```

### 2. httpbin upstream 프록시 설정

**목표**: Envoy가 요청을 httpbin 컨테이너로 포워딩하도록 static config를 수정한다.

**단계**:
1. httpbin 컨테이너 기동
   ```bash
   docker run --rm -d \
     --name httpbin \
     -p 8080:80 \
     kennethreitz/httpbin
   ```
2. `envoy-static.yaml`의 `direct_response` 부분을 cluster 라우팅으로 교체
   ```yaml
   # routes 섹션 변경
   routes:
     - match: { prefix: "/" }
       route: { cluster: httpbin_cluster }

   # clusters 섹션 추가
   clusters:
     - name: httpbin_cluster
       connect_timeout: 5s
       type: STATIC
       load_assignment:
         cluster_name: httpbin_cluster
         endpoints:
           - lb_endpoints:
               - endpoint:
                   address:
                     socket_address:
                       # host.docker.internal: Docker Desktop에서 호스트 접근
                       address: host.docker.internal
                       port_value: 8080
   ```
3. Envoy 재기동
   ```bash
   docker restart envoy-lab
   ```

**검증**:
```bash
curl localhost:10000/get
# httpbin의 JSON 응답이 출력된다
curl localhost:10000/headers
```

### 3. Admin API 탐색

**목표**: Envoy Admin API를 통해 런타임 상태, 클러스터 정보, 전체 설정을 조회한다.

**단계**:
1. 기본 통계 확인
   ```bash
   curl -s localhost:15000/stats | grep http
   ```
2. 클러스터 상태 확인
   ```bash
   curl -s localhost:15000/clusters | python3 -m json.tool 2>/dev/null || \
   curl -s localhost:15000/clusters
   ```
3. 전체 설정 덤프
   ```bash
   curl -s localhost:15000/config_dump | python3 -m json.tool | head -80
   ```
4. 런타임 정보
   ```bash
   curl -s localhost:15000/runtime
   ```

**검증**: `/clusters`에서 `httpbin_cluster`가 `HEALTHY` 상태로 표시된다.

### 4. Retry 설정 후 통계 확인

**목표**: route에 retry policy를 추가하고 실패 요청을 통해 retry 카운터가 올라가는지 확인한다.

**단계**:
1. route에 retry policy 추가
   ```yaml
   routes:
     - match: { prefix: "/" }
       route:
         cluster: httpbin_cluster
         retry_policy:
           retry_on: "5xx"
           num_retries: 3
           per_try_timeout: 2s
   ```
2. 500 응답을 유발하는 엔드포인트로 요청
   ```bash
   curl -s localhost:10000/status/500
   ```
3. retry 통계 확인
   ```bash
   curl -s localhost:15000/stats | grep retry
   ```

**검증**:
```
http.ingress_http.upstream_rq_retry: 3
```
retry 카운터가 0보다 크게 올라간다.

### 5. Dynamic config (filesystem 기반)

**목표**: xDS 파일 기반 dynamic config를 사용해 Envoy를 재시작하지 않고 설정을 변경한다.

**단계**:
1. 파일 기반 xDS 설정 디렉토리 생성
   ```bash
   mkdir -p /tmp/envoy-lab/xds
   ```
2. bootstrap에 dynamic resources 추가 (`envoy-dynamic.yaml`)
   ```yaml
   dynamic_resources:
     lds_config:
       path_config_source:
         path: /etc/envoy/xds/lds.yaml
         watched_directory:
           path: /etc/envoy/xds
     cds_config:
       path_config_source:
         path: /etc/envoy/xds/cds.yaml
         watched_directory:
           path: /etc/envoy/xds

   admin:
     address:
       socket_address: { address: 0.0.0.0, port_value: 15000 }
   ```
3. `xds/lds.yaml`, `xds/cds.yaml` 작성 후 Envoy 재기동
   ```bash
   docker stop envoy-lab
   docker run --rm -d \
     --name envoy-lab \
     -p 10000:10000 -p 15000:15000 \
     -v /tmp/envoy-lab/envoy-dynamic.yaml:/etc/envoy/envoy.yaml \
     -v /tmp/envoy-lab/xds:/etc/envoy/xds \
     envoyproxy/envoy:v1.29-latest
   ```
4. xds 파일 수정 후 핫 리로드 확인
   ```bash
   # lds.yaml에서 direct_response 메시지 변경
   # 저장하면 Envoy가 자동으로 감지
   curl localhost:10000
   ```

**검증**: Envoy 재시작 없이 응답 내용이 변경된다.

### 6. Envoy 용어 config 매핑 실습

**목표**: `config_dump` 출력에서 Envoy의 핵심 4개 개념이 어느 블록에 위치하는지 직접 찾는다.

**단계**:
1. config_dump를 파일로 저장
   ```bash
   curl -s localhost:15000/config_dump > /tmp/envoy-lab/config_dump.json
   ```
2. 각 개념 위치 검색
   ```bash
   # Listener (수신 포트 및 필터 체인 정의)
   cat /tmp/envoy-lab/config_dump.json | python3 -c \
     "import json,sys; d=json.load(sys.stdin); \
      [print(c['name']) for c in d['configs'] if 'ListenersConfigDump' in c.get('@type','')]"

   # Cluster (upstream 그룹 정의)
   curl -s localhost:15000/clusters | head -5

   # Route (요청을 cluster로 매핑하는 규칙)
   curl -s localhost:15000/config_dump | python3 -m json.tool | grep -A3 '"route"'

   # Endpoint (실제 서버 주소)
   curl -s localhost:15000/clusters | grep "::"
   ```

**검증**: 각 개념이 config의 어느 섹션에 속하는지 직접 확인하고 아래 표를 채운다.

| 개념 | 역할 | config_dump 위치 |
|------|------|-----------------|
| Listener | 수신 포트 + 필터 체인 | `ListenersConfigDump` |
| Route | URL → cluster 매핑 규칙 | `RoutesConfigDump` |
| Cluster | upstream 서버 그룹 | `ClustersConfigDump` |
| Endpoint | 실제 IP:Port | `EndpointsConfigDump` |

## 정리 (Cleanup)

```bash
docker stop envoy-lab httpbin
rm -rf /tmp/envoy-lab
```
