---
title: 클러스터에서 웹 서비스 주소 찾기 — Ingress·Route·Service·DNS 추적
tags: [kubernetes, openshift, ingress, route, service, dns, networking]
status: draft
source:
  - https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/ingress_and_load_balancing/routes#nw-ingress-creating-a-route-via-an-ingress_creating-basic-routes
  - https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/config_apis/ingress-config-openshift-io-v1
  - https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/config_apis/dns-config-openshift-io-v1
  - https://github.com/openshift/route-controller-manager/blob/release-4.18/pkg/route/ingress/ingress.go
  - https://github.com/openshift/router/blob/release-4.18/images/router/haproxy/conf/haproxy-config.template
  - https://github.com/kubernetes/kubectl/blob/release-1.33/pkg/cmd/set/set_env.go
  - https://kubernetes.io/docs/concepts/services-networking/ingress/
  - https://kubernetes.io/docs/concepts/services-networking/gateway/
  - https://kubernetes.io/docs/concepts/services-networking/service/
  - https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/
related:
  - ./README.md
  - ../08_cloud/book/kubernetes-in-action/12-01.Ingress로 여러 서비스를 한 IP에 노출하기.md
  - ../08_cloud/book/kubernetes-in-action/11-02.외부 노출 — NodePort·LoadBalancer·트래픽 정책.md
  - ../08_cloud/book/kubernetes-in-action/11-03.엔드포인트·DNS·토폴로지·readiness.md
updated: 2026-11-26
---

# 클러스터에서 웹 서비스 주소 찾기 — Ingress·Route·Service·DNS 추적

---

> 처음 보는 Kubernetes·OpenShift 클러스터에서 웹 서비스나 미들웨어 주소를 찾으려면 선언·노출·접속 세 층을 순서대로 조회해야 합니다.

## 1. 주소가 한 곳에 없는 이유

> 클러스터 서비스 주소는 하나의 설정 파일에 모이지 않고 선언·노출·접속 세 계층에 흩어져 있어, 어느 층의 주소가 필요한지에 따라 조회 대상이 달라집니다.

현장에서 "이 서비스 접속 주소가 무엇인가요?"라는 질문을 받으면 리소스 하나만 열어서는 답이 나오지 않습니다. 사용자가 브라우저에 치는 도메인, 클러스터가 받는 포트와 IP, 앱이 부르는 DB 주소가 모두 다른 오브젝트에 담기기 때문입니다.

주소와 경로가 갈라지는 계층은 세 층으로 나뉩니다.

- 선언 층: **Ingress** · **Gateway API** · **ConfigMap** · **Secret** · Helm values 가 호스트와 대상 주소를 선언합니다.
- 노출 층: **OpenShift Route** · **Service** · L7 프록시 VIP(가상 IP)가 요청을 받는 접점을 정합니다.
- 접속 층: DNS(`nslookup`·`dig`)와 로컬 `hosts` 파일이 도메인 이름을 IP 로 바꿉니다.

외부에서 웹 포털로 들어오는 주소는 Ingress·Route 와 DNS 를 먼저 봅니다. 반대로 앱이 내부 미들웨어나 외부 VM DB 를 부르는 주소는 ConfigMap 과 Deployment 환경변수를 확인합니다.



## 2. 주소가 정해지는 층 지도

> 브라우저에서 Pod 로 들어오는 인바운드 경로와, Pod 가 설정을 읽어 내부·외부 대상을 부르는 아웃바운드 경로가 서로 다른 계층을 탑니다.

외부 브라우저가 서비스를 찾는 길과 Pod 가 미들웨어를 찾는 길은 방향이 달라 한 표로 읽히지 않습니다. 아래 지도는 두 방향의 흐름을 `OUTSIDE CLUSTER` 와 `INSIDE CLUSTER` 두 구역으로 나눠 보여 줍니다.

![클러스터 인바운드·아웃바운드 주소 계층 지도](./_assets/2026-11-26_클러스터에서%20웹%20서비스%20주소%20찾기%20%E2%80%94%20Ingress%C2%B7Route%C2%B7Service%C2%B7DNS%20추적.address-layers.svg)

인바운드(1~5)는 브라우저가 `portal.apps.<cluster>.example.com` 을 DNS 로 조회해 VIP `10.0.0.46` 을 받는 것으로 시작합니다. 이어서 Router(L7 프록시)가 Ingress·Route 의 호스트·경로 규칙을 매칭해 Service 가 가리키는 Pod 로 요청을 넘깁니다.

도식의 4~5번은 대상을 찾아가는 객체 참조 순서입니다. OpenShift Router 의 HAProxy 설정에는 backend 서버로 Pod 쪽 endpoint IP 와 포트가 적힙니다.[^ocp-router] VIP 가 클러스터 밖 장비에 있으면 Service 목록에 안 보일 수 있으므로 DNS 응답으로 확인합니다.

아웃바운드(6~8)는 Pod 가 ConfigMap 의 키를 읽어 대상을 정하는 흐름입니다. `APP_MINIO_URL` 이 그런 키입니다.

대상이 내부면 `minio` 같은 Service 이름을 클러스터 DNS 로 풉니다. 도식에는 `minio.my-ns.svc` 로 적었습니다. 외부 VM 이면 `10.0.0.144:3306` 으로 직접 나갑니다.



## 3. 바깥에서 들어오는 주소

> 외부에서 클러스터 웹 UI 나 API 로 들어오는 URL 은 Ingress 를 먼저 훑고, OpenShift Route·Gateway API·Service·클러스터 기본 도메인 순으로 좁혀 갑니다.

처음 접속한 클러스터는 어떤 노출 방식이 켜져 있는지 몰라, Ingress 와 Route 를 따로 보지 않으면 자동 생성된 객체에 가려 실제 진입점을 놓칩니다.

| 노출 방식 | 주소가 담긴 필드 | 차이 및 확인 상황 |
|---|---|---|
| Ingress | `spec.rules[*].host` | 표준 L7 HTTP·HTTPS 진입점 파악 |
| OpenShift Route | `spec.host`, `ownerReferences` | OpenShift 도메인과 자동 생성 여부 구분 |
| Gateway API | `Gateway` 의 `spec.listeners[*].hostname`·`status.addresses`, `HTTPRoute` 의 `spec.hostnames` | Gateway API CRD 가 설치된 클러스터 |
| Service | `spec.type`, `spec.ports[*].nodePort`, `status.loadBalancer.ingress`, `spec.externalName` | L4 직접 노출 포트 확인. ExternalName 은 안에서 밖을 가리키는 별칭 |

표의 각 노출 방식은 아래 순서로 조회해 실제 도메인과 포트를 확정합니다.

### Ingress 목록과 호스트·클래스 조회

전체 네임스페이스의 Ingress 를 한 번에 훑으면 어떤 웹 도메인이 어느 네임스페이스에 묶여 있는지 바로 보입니다. `custom-columns` 로 네임스페이스, 이름, IngressClass, 호스트 열만 추리면 한눈에 들어옵니다.

```bash
# 모든 네임스페이스의 Ingress 와 호스트 목록을 요약해 조회합니다
#   -A                 전체 네임스페이스 대상
#   -o custom-columns  원하는 필드만 열로 추출
kubectl get ingress -A \
  -o 'custom-columns=NS:.metadata.namespace,NAME:.metadata.name,CLASS:.spec.ingressClassName,HOSTS:.spec.rules[*].host'
```

열 정의 전체를 작은따옴표로 감싼 것은 zsh 때문입니다. 따옴표가 없으면 zsh 가 `[*]` 를 파일 패턴으로 읽어 `no matches found` 로 멈춥니다.

아래는 실제 OpenShift 클러스터에서 위 명령을 실행해 얻은 출력을 익명화한 결과입니다. 같은 호스트 `portal.apps.<cluster>.example.com` 아래에 경로만 나뉜 Ingress 둘이 공존할 수 있습니다.

```bash
# 결과 (실측 익명화 출력)
NS       NAME              CLASS               HOSTS
my-ns    argocd-server     openshift-default   argocd.apps.<cluster>.example.com
my-ns    auth-ingress      openshift-default   portal.apps.<cluster>.example.com
my-ns    non-auth-ingress  openshift-default   portal.apps.<cluster>.example.com
my-ns    grafana           openshift-default   grafana.apps.<cluster>.example.com
```

TLS 인증서나 세부 경로(`path`)는 `kubectl get ingress <이름> -n <ns> -o yaml` 로 `spec.tls` 와 `paths` 를 확인합니다.[^k8s-ingress]

### OpenShift Route 와 자동 생성 구분

OpenShift 는 **Ingress** 가 생기면 대응하는 **Route** 를 자동으로 만듭니다. Ingress 를 지우면 그 Route 도 지워집니다.[^ocp-ingress-route] 이 일은 `route-controller-manager` 의 컨트롤러가 맡습니다. 자동 생성 Route 의 이름은 `<Ingress 이름>-` 뒤에 임의 문자 5자를 붙인 꼴입니다. `ownerReferences` 에는 부모 `Ingress/<이름>` 이 기록됩니다.[^ocp-ctrl]

모든 Ingress 가 Route 가 되지는 않습니다. IngressClass 를 지정했다면 그 클래스의 컨트롤러가 `openshift.io/ingress-to-route` 여야 합니다. `host` 가 없는 규칙, `pathType: Exact` 인 경로, 대상 Service 를 찾지 못하는 경로에서는 Route 가 만들어지지 않습니다. TLS 설정이 가리키는 Secret 이 없거나 잘못돼도 마찬가지입니다.[^ocp-ctrl]

컨트롤러는 규칙의 host 와 path 조합마다 Route 를 하나씩 만들기 때문에, path 가 많으면 Ingress 하나에서 Route 여러 개가 나옵니다. 실제 관측에서도 Ingress 9개에서 Route 29개가 생겼으며, `auth-ingress` 는 Route 6개, `non-auth-ingress` 는 16개로 불어났습니다.

반면 `console`, `oauth`, `monitoring` 같은 시스템 Route 는 Ingress 소유가 아닙니다. 아래 명령으로 Route 마다 `ownerReferences` 를 찍어 직접 만든 Route 와 구분합니다.

```bash
# 네임스페이스 내 Route 의 소유자(Ingress 여부)를 확인합니다
#   -n my-ns     조회할 네임스페이스 지정
#   -o jsonpath  이름과 첫 번째 ownerReference 만 출력
kubectl get route -n my-ns \
  -o jsonpath='{range .items[*]}{.metadata.name}{" <- "}{.metadata.ownerReferences[0].kind}/{.metadata.ownerReferences[0].name}{"\n"}{end}'
```

출력의 오른쪽이 `Ingress/<이름>` 이면 그 Ingress 에서 자동 생성된 Route 입니다. 왼쪽 이름의 5자 접미사는 보조 단서일 뿐이라 판정은 `ownerReferences` 로 합니다. 소유자가 없는 Route 는 오른쪽에 `/` 만 남고, 다른 종류가 적혀 있으면 Ingress 에서 나온 것이 아닙니다.

```bash
# 결과 (실측 익명화 출력)
argocd-server-pllxp <- Ingress/argocd-server
auth-ingress-7sgb6 <- Ingress/auth-ingress
auth-ingress-8qzb6 <- Ingress/auth-ingress
non-auth-ingress-6p7p8 <- Ingress/non-auth-ingress
grafana-6wknw <- Ingress/grafana
```

### Gateway API 확인과 미설치 클러스터

최근 클러스터는 Ingress 대신 **Gateway API**(`Gateway`, `HTTPRoute`)로 외부 트래픽을 받기도 합니다.[^k8s-gateway] 다만 CRD(사용자 정의 리소스)가 설치되지 않은 클러스터도 많으므로 리소스 유무부터 확인합니다.

```bash
# 클러스터에 Gateway 와 HTTPRoute 리소스가 있는지 조회합니다
kubectl get gateway,httproute -A
```

CRD 는 있는데 만든 리소스가 없으면 아래처럼 빈 결과가 나옵니다. CRD 자체가 없으면 이 출력 대신 리소스 종류를 알 수 없다는 오류가 납니다. Istio 처럼 `Gateway` 라는 이름의 CRD 를 따로 두는 제품도 있습니다. 헷갈리면 `gateways.gateway.networking.k8s.io` 처럼 전체 이름으로 조회합니다.

```bash
# 결과 (실측 출력)
No resources found
```

### Service 타입별 외부 접점

L7 프록시를 거치지 않는 L4 접점은 **Service** 타입으로 찾습니다. 내부 전용 `ClusterIP` 를 제외하고 `NodePort`, `LoadBalancer`, `ExternalName` 만 걸러 봅니다.[^k8s-service] 이 가운데 `ExternalName` 은 밖에서 들어오는 접점이 아닙니다. 포트를 열거나 트래픽을 중계하지 않지만, 앱이 밖의 어느 이름을 부르는지 알려 주므로 함께 봅니다.

- `NodePort`: 모든 클러스터 노드 IP 의 해당 `nodePort`(`30000`~`32767` 대역 기본)로 접속합니다.
- `LoadBalancer`: 클라우드나 MetalLB 등이 할당한 `EXTERNAL-IP` 로 접속합니다.
- `ExternalName`: 클러스터 DNS 가 Service 이름에 대해 `spec.externalName` 을 CNAME 으로 응답합니다.

```bash
# ClusterIP 를 제외한 Service 의 타입, ExternalName, NodePort 를 출력합니다
#   -A                 전체 네임스페이스 조회
#   -o custom-columns  타입과 포트 관련 열만 표시
kubectl get svc -A \
  -o 'custom-columns=NS:.metadata.namespace,NAME:.metadata.name,TYPE:.spec.type,EXT:.spec.externalName,NODEPORT:.spec.ports[*].nodePort' \
  | awk 'NR==1||$3!="ClusterIP"'
```

실제로 관측한 클러스터에는 `LoadBalancer` 가 없고 `NodePort` 와 `ExternalName` 만 있었습니다. 아래 출력 기준 `minio` 는 `<노드IP>:31900`, `grafana` 는 `<노드IP>:31269` 로 접근합니다.

```bash
# 결과 (실측 익명화 출력)
NS        NAME          TYPE           EXT                                    NODEPORT
default   openshift     ExternalName   kubernetes.default.svc.cluster.local   <none>
my-ns     minio         NodePort       <none>                                 31900
my-ns     grafana       NodePort       <none>                                 31269
```

### 클러스터 기본 도메인 확인

OpenShift 는 두 도메인을 전역 설정에 둡니다. 기본 Ingress 도메인은 `apps.<cluster>.example.com` 같은 값이고, 또 하나는 기반 도메인(base domain)입니다.[^ocp-config-ingress][^ocp-config-dns] 아래 두 명령으로 각각 앱 라우팅 도메인과 클러스터 기반 도메인을 조회합니다.

```bash
# OpenShift 기본 Ingress 도메인을 조회합니다
oc get ingresses.config.openshift.io cluster -o jsonpath='{.spec.domain}'

# OpenShift 클러스터 기반 도메인(baseDomain)을 조회합니다
oc get dns.config.openshift.io cluster -o jsonpath='{.spec.baseDomain}'
```

첫 번째 명령을 실행하면 `apps.<cluster>.example.com` 같은 기본 도메인 문자열이 출력됩니다.

```bash
# 첫 번째 명령의 결과 (실측 익명화 출력)
apps.<cluster>.example.com
```

일반 Kubernetes 에는 위 리소스가 없으므로 Ingress Controller Service 의 `EXTERNAL-IP` 를 먼저 봅니다. 이어서 앞에서 찾은 호스트의 상위 도메인에 와일드카드 DNS 가 있고 그 IP 를 가리키는지, 등록하지 않았을 임의의 하위 이름을 질의해 대조합니다.



## 4. 앱이 실제로 쓰는 주소

> 웹 진입점과 달리 앱이 DB·스토리지·내부 API 를 호출할 때 쓰는 주소는 ConfigMap, Secret 키 이름, Deployment 환경변수, Helm·ArgoCD 설정에 들어 있습니다.

Ingress 를 찾았는데도 앱이 어느 DB 나 객체 스토리지를 바라보는지 모를 때가 있습니다. 앱 Pod 가 실제로 읽는 설정 주입 경로 네 곳을 순서대로 확인해야 누락이 없습니다.

### ConfigMap 과 Secret 안전 조회

**ConfigMap** 에는 JDBC URL, 내부 API 엔드포인트, 외부 VM 주소가 키-값으로 들어 있습니다. 다만 비밀번호·토큰 성격의 키가 섞일 수 있으므로 민감 키는 마스킹해 출력합니다.

```bash
# ConfigMap 의 .data 를 읽되, 키 이름에 pass·secret·token·key 가 들면 값을 *** 로 가려 정렬 출력합니다
#   -o jsonpath='{.data}'  ConfigMap 본문 데이터만 JSON 으로 추출
#   python3 -I             사용자 사이트 패키지를 배제한 격리 파이썬으로 필터링
kubectl get cm backend-common-cm -n my-ns -o jsonpath='{.data}' \
  | python3 -I -c 'import json,sys,re; d=json.load(sys.stdin); [print(k,"=",("***" if re.search("pass|secret|token|key",k,re.I) else v)) for k,v in sorted(d.items())]'
```

아래 출력처럼 IP 로 적힌 외부 DB(`10.0.0.144:3306`), 같은 네임스페이스 서비스(`http://minio:9000`), 내부 API(`http://auth-api`)가 갈립니다.

```bash
# 결과 (실측 익명화 출력)
APP_DATASOURCE_JDBC_URL = jdbc:mariadb://10.0.0.144:3306/appdb
APP_DATASOURCE_PASSWORD = ***
APP_MINIO_URL = http://minio:9000
APP_SERVICES_AUTH_API_URL = http://auth-api
```

이 필터는 키 이름만 봅니다. `user:password@host` 꼴의 URL, 접속 문자열의 비밀번호 파라미터, `application.yml` 처럼 설정 파일을 통째로 담은 값은 그대로 출력됩니다. 화면을 공유하거나 로그를 남기는 중이라면 키 이름부터 확인합니다.

**Secret** 은 값 자체를 화면이나 터미널 로그에 찍지 않는 것이 원칙입니다. 어떤 키가 정의돼 있는지만 보려면 아래처럼 키 이름 목록만 뽑습니다.

```bash
# Secret 의 값을 디코딩하지 않고 키 이름만 정렬해 확인합니다
kubectl get secret my-app-secret -n my-ns -o jsonpath='{.data}' \
  | python3 -I -c 'import json,sys; print("\n".join(sorted(json.load(sys.stdin).keys())))'
```

### Deployment 환경변수 확인

ConfigMap 이나 Secret 에서 어느 키가 실제로 컨테이너에 들어가는지는 Deployment 의 `env` 와 `envFrom` 을 봅니다. `kubectl set env --list` 는 이 가운데 `env` 항목만 출력합니다. 참조 항목은 `# 이름 from ...` 꼴로 출처가 보입니다. 반면 `envFrom` 으로 통째로 주입한 ConfigMap·Secret 은 목록에 나오지 않습니다.[^kubectl-setenv]

```bash
# Deployment 의 env 항목을 목록으로 봅니다 (envFrom 은 나오지 않습니다)
#   deploy/<이름>  대상 Deployment 지정
#   --list         변경 없이 현재 환경변수 설정만 출력
kubectl set env deploy/myapp -n my-ns --list
```

`envFrom` 까지 확인하려면 `kubectl get deploy myapp -n my-ns -o yaml` 을 봅니다. `containers[*].env` 와 `containers[*].envFrom` 블록을 직접 찾습니다. 두 명령 모두 `env` 에 직접 적은 값은 평문으로 출력합니다. 거기에 비밀번호가 있으면 그대로 화면에 나옵니다.

### Helm 릴리스와 ArgoCD Application

**Helm** 차트로 배포된 앱이라면 릴리스에 넣은 오버라이드 값을 `helm get values` 로 조회합니다. 차트 기본값까지 합친 값을 보려면 `--all` 옵션을 붙입니다. 어느 쪽이든 values 에 비밀번호가 있으면 가려지지 않고 출력됩니다.

```bash
# Helm 릴리스의 설정값(host·endpoint 등)을 차트 기본값까지 합쳐 조회합니다
#   -n <ns>  릴리스가 배포된 네임스페이스
#   --all    차트 기본값(values.yaml)과 병합된 전체 값 출력
helm get values myapp-release -n my-ns --all
```

GitOps 도구인 **ArgoCD** 로 배포한 환경이라면 `Application` 리소스의 `spec.source` 를 봅니다. 저장소 URL 과 브랜치·경로가 여기에 있습니다. 도메인은 `spec.source.helm` 의 `values`·`valuesObject`·`parameters` 에 직접 적혀 있을 수 있습니다. `valueFiles` 가 가리키는 저장소 파일에 있을 수도 있습니다. 소스를 여러 개 쓰는 Application 은 `spec.sources` 를 봅니다.

```bash
# ArgoCD Application 의 배포 소스와 values 오버라이드를 확인합니다
kubectl get application myapp-app -n argocd -o yaml
```



## 5. 이름이 어디로 가는지 확인

> Ingress 나 Route 에서 도메인을 찾았더라도 실제 트래픽이 어느 IP 로 가는지 검증하려면 DNS 질의, 로컬 hosts 파일, curl 강제 매핑 세 단계를 대조해야 합니다.

설정에 도메인이 적혀 있어도 DNS 미등록이나 캐시 불일치 때문에 접속에 실패하는 일이 잦습니다. 브라우저에서 안 열린다고 곧바로 클러스터 장애로 단정하기 전에 이름 해석 경로를 끊어 확인합니다.

### nslookup 과 dig 로 DNS 응답 대조

먼저 현재 PC 또는 점프 호스트에서 DNS 가 해당 도메인에 어느 IP 로 응답하는지 확인합니다. `nslookup` 과 `dig` 는 DNS 서버에 직접 묻는 도구입니다. `hosts` 파일에 적어 둔 값은 반영되지 않아, 브라우저가 쓰는 주소와 다를 수 있습니다.

```bash
# 기본 DNS 서버로 도메인 해석 결과를 확인합니다
nslookup portal.apps.<cluster>.example.com

# 응답만 짧게(+short) 뽑아 VIP 일치 여부를 확인합니다 (CNAME 을 거치면 그 이름도 함께 나옵니다)
dig +short portal.apps.<cluster>.example.com

# 특정 DNS 서버의 응답과 대조합니다
dig @<DNS 서버 IP> +short portal.apps.<cluster>.example.com
nslookup portal.apps.<cluster>.example.com <DNS 서버 IP>
```

`nslookup` 에 `NXDOMAIN` 이 뜨거나 `dig +short` 결과가 비면 레코드가 없는지부터 봅니다. 원하는 VIP(`10.0.0.46`)와 다른 IP 가 나오면 레코드 값, DNS 캐시, 질의한 DNS 서버가 맞는지를 차례로 확인합니다.

### 로컬 hosts 파일과 curl 직결 테스트

DNS 등록 전이나 특정 VIP 강제 검증에는 로컬 `hosts` 파일이나 `curl --resolve` 를 씁니다. OS 별 `hosts` 파일 위치는 아래와 같습니다.

- Linux · macOS: `/etc/hosts`
- Windows: `C:\Windows\System32\drivers\etc\hosts`

`hosts` 파일을 건드리지 않고 특정 IP 의 TLS·HTTP 응답만 보려면 `curl -v --resolve` 가 안전합니다. SNI(Server Name Indication)와 `Host` 헤더를 도메인 그대로 둔 채 목적지 IP 만 바꿉니다.

```bash
# DNS 를 거치지 않고 지정 IP(10.0.0.46) 443 포트로 도메인 요청을 보냅니다
#   -v         TLS 핸드셰이크와 HTTP 응답 헤더 상세 출력
#   --resolve  <host>:<port>:<IP> 형식으로 이름 해석을 임시 고정
curl -v --resolve portal.apps.<cluster>.example.com:443:10.0.0.46 \
  https://portal.apps.<cluster>.example.com
```

같은 PC 에서 `--resolve` 요청은 성공하는데 브라우저만 실패한다면, 그 VIP 까지의 경로와 그 요청의 처리는 동작하는 것입니다. 이때는 브라우저가 받는 DNS 응답, 프록시 설정, 브라우저 캐시를 먼저 의심합니다.

### 클러스터 내부 DNS 의 경계

`minio` 나 `minio.my-ns.svc.cluster.local` 은 클러스터 DNS 가 푸는 내부용 이름입니다.[^k8s-dns] 같은 네임스페이스의 Pod 안에서는 `/etc/resolv.conf` 의 `search` 경로가 붙어 `http://minio:9000` 처럼 짧은 이름도 풀립니다. `cluster.local` 은 기본 클러스터 도메인이라 설치할 때 바꾼 환경에서는 다를 수 있습니다.

반면 클러스터 밖 노트북이나 외부 VM 에서 `minio.my-ns.svc.cluster.local` 을 `nslookup` 하면 풀리지 않습니다. 외부에서 그 서비스에 접근해야 한다면 3절에서 본 Ingress·Route·NodePort·LoadBalancer 접점을 거쳐야 합니다.



## 6. 조회 순서 체크리스트

> 처음 보는 클러스터에 들어가면 컨텍스트를 먼저 고정한 뒤 외부 진입점 → 앱 내부 설정 → DNS 검증 순으로 아래 명령을 위에서부터 실행합니다.

이 절의 명령은 3~5절에서 다룬 확인 과정을 현장 순서대로 한 블록에 모은 절차입니다. `--context <ctx>` 를 명시하면 여러 클러스터가 등록된 kubeconfig 에서도 잘못된 환경을 조회할 위험을 줄입니다.

```bash
# 0. 현재 작업 대상 컨텍스트와 네임스페이스를 먼저 확인합니다
kubectl config get-contexts
kubectl --context <ctx> get ns

# 1. 외부 진입점(Ingress · OpenShift Route · Gateway API · Service)을 훑습니다
kubectl --context <ctx> get ingress -A \
  -o 'custom-columns=NS:.metadata.namespace,NAME:.metadata.name,CLASS:.spec.ingressClassName,HOSTS:.spec.rules[*].host'
oc --context <ctx> get route -A \
  -o 'custom-columns=NS:.metadata.namespace,NAME:.metadata.name,HOST:.spec.host,OWNER:.metadata.ownerReferences[0].kind'
kubectl --context <ctx> get gateway,httproute -A
kubectl --context <ctx> get svc -A \
  -o 'custom-columns=NS:.metadata.namespace,NAME:.metadata.name,TYPE:.spec.type,EXT:.spec.externalName,NODEPORT:.spec.ports[*].nodePort' \
  | awk 'NR==1||$3!="ClusterIP"'

# 2. OpenShift 전역 도메인을 확인합니다 (일반 Kubernetes 에서는 생략)
oc --context <ctx> get ingresses.config.openshift.io cluster -o jsonpath='{.spec.domain}'
oc --context <ctx> get dns.config.openshift.io cluster -o jsonpath='{.spec.baseDomain}'

# 3. 앱이 쓰는 주소(ConfigMap · Secret 키 · Deployment env/envFrom · Helm/ArgoCD)를 확인합니다
kubectl --context <ctx> get cm <cm-name> -n <ns> -o jsonpath='{.data}' \
  | python3 -I -c 'import json,sys,re; d=json.load(sys.stdin); [print(k,"=",("***" if re.search("pass|secret|token|key",k,re.I) else v)) for k,v in sorted(d.items())]'
kubectl --context <ctx> get secret <secret-name> -n <ns> -o jsonpath='{.data}' \
  | python3 -I -c 'import json,sys; print("\n".join(sorted(json.load(sys.stdin).keys())))'
kubectl --context <ctx> set env deploy/<deploy-name> -n <ns> --list   # env 만 출력
kubectl --context <ctx> get deploy <deploy-name> -n <ns> -o yaml       # envFrom 확인
helm --kube-context <ctx> get values <release> -n <ns>
kubectl --context <ctx> get application <app-name> -n argocd -o yaml

# 4. 찾은 도메인이 실제 VIP 로 닿는지 DNS 와 curl 로 검증합니다
nslookup <host>
curl -v --resolve <host>:443:<VIP> https://<host>
```

컨텍스트 이름을 생략하고 싶다면 `kubectl config use-context <ctx>` 로 컨텍스트를 전환한 뒤 확인합니다. `oc project <ns>` 는 지금 접속한 클러스터 안에서 작업 네임스페이스(프로젝트)를 바꿀 때 씁니다. 다만 여러 터미널 창을 열어 두는 현장에서는 매 명령에 `--context <ctx>` 를 붙이는 편이 안전합니다.



## 7. 현장에서 자주 빠지는 함정

> 주소를 찾거나 고칠 때 흔히 겪는 사고 다섯 가지는 자동 생성 Route 직접 수정, Secret 실값 노출, 컨텍스트 착각, 내부 DNS 혼동, 그리고 Route 행 수 오해입니다.

조회 명령을 알더라도 리소스 간 소유 관계와 경계를 헷갈리면 원복되거나 보안 사고로 이어집니다. 현장 작업 전 아래 다섯 가지를 먼저 점검합니다.

### 자동 생성 Route 를 직접 수정

OpenShift 에서 `ownerReferences` 가 `Ingress/<이름>` 인 Route 는 컨트롤러가 부모 Ingress 에 맞춰 관리합니다. `oc edit` 로 대상 Service 나 어노테이션을 고치면 Ingress 기준 값으로 되돌립니다. host 나 path 를 고치면 그 Route 를 지우고 원래 조합의 Route 를 새로 만듭니다.[^ocp-ctrl] weight 처럼 보존되는 필드도 일부 있지만 거기에 기대지 않습니다. 설정은 부모 **Ingress** 에서 바꾸고, 그 Ingress 를 Helm·ArgoCD 가 배포했다면 배포 원본을 수정합니다.

### Secret 실값을 화면·로그에 출력

`kubectl get secret -o yaml` 이나 `jsonpath='{.data}'` 를 그대로 찍으면 Base64 로 인코딩된 비밀번호가 화면에 나옵니다. 터미널 스크롤백, 화면 공유, 세션 로그에 남은 값은 누구나 디코딩할 수 있습니다. 조회 시에는 4절처럼 키 이름만 뽑거나 민감 키 패턴을 `***` 로 마스킹합니다.

### 컨텍스트 혼동과 내부 DNS 오해

kubeconfig 에 개발·검증·운영 컨텍스트가 섞여 있으면 `kubectl get ingress` 가 다른 클러스터 주소를 돌려줍니다. 또한 `minio.my-ns.svc.cluster.local` 같은 내부 서비스 이름을 노트북 브라우저에 그대로 붙여 넣고 접속 불가를 의심하는 실수도 잦습니다.

### Ingress 수보다 많은 Route 목록

`kubectl get route` 를 쳤을 때 Ingress 개수보다 몇 배나 많은 Route 가 나와 당황하는 경우가 있습니다. Ingress 에 적은 host·path 조합이 여럿이면 조합마다 별도 Route 가 생기기 때문입니다. `ownerReferences` 로 묶어 보면 한 Ingress 에서 나온 목록임을 바로 알 수 있습니다.



## 8. 자가 점검 질문

> 답을 보기 전에 아래 다섯 질문에 스스로 설명해 본 뒤 파일 끝 정답 절과 대조합니다.

1. OpenShift 에서 `kubectl get route -n my-ns` 목록에 5자 임의 접미사가 붙은 Route 가 보일 때, Ingress 에서 자동 생성된 것인지 어떻게 확인하며 맞다면 왜 직접 고치면 안 됩니까?
2. `kubectl get ingress -A` 를 쳤더니 Ingress 는 9개인데 `get route -A` 는 29개가 나왔습니다. 이 개수 차이가 정상 동작인 이유는 무엇입니까?
3. ConfigMap 에서 `APP_MINIO_URL = http://minio:9000` 과 `APP_DATASOURCE_JDBC_URL = jdbc:mariadb://10.0.0.144:3306/appdb` 를 봤습니다. 클러스터 밖 노트북에서 어느 주소가 DNS 해석부터 막히며 이유는 무엇입니까?
4. DNS 에 미등록된 `portal.apps.<cluster>.example.com` 이 VIP `10.0.0.46` 에서 응답하는지 `/etc/hosts` 수정 없이 확인하려면 어떤 명령을 씁니까?
5. ConfigMap 이나 Secret 을 조회할 때 `kubectl get ... -o yaml` 을 그대로 실행하지 않고 키 필터링을 거치는 이유는 무엇입니까?



## 정답 (자답 후 펼치기)

> 위 질문 5개에 먼저 자답한 뒤 아래를 읽으세요.

### 정답 1 — 자동 생성 Route 구분과 수정 대상

`metadata.ownerReferences` 의 `kind` 와 `name` 을 조회해 `Ingress/<이름>` 이 찍혀 있으면 OpenShift 가 자동 생성한 Route 입니다. 비어 있거나 다른 종류면 Ingress 에서 나온 Route 가 아닙니다. 자동 생성 Route 를 직접 고치면 `route-controller-manager` 의 컨트롤러가 부모 Ingress 에 맞춰 되돌리거나 다시 만들므로, 수정은 부모 Ingress 나 배포 원본에서 해야 합니다.

### 정답 2 — Ingress 수와 Route 수의 차이

OpenShift 의 Ingress-to-Route 변환은 Ingress 규칙 안의 host·path 조합마다 별도 Route 오브젝트를 하나씩 생성하기 때문입니다. 따라서 path 가 많은 Ingress 가 여러 개 있으면 Ingress 9개에서 Route 29개처럼 Route 수가 몇 배로 늘어나는 것이 정상 동작입니다.

### 정답 3 — 내부 DNS 이름의 클러스터 경계

`http://minio:9000` 이 클러스터 밖 노트북에서 막힙니다. `minio` 는 Pod 의 `/etc/resolv.conf` 검색 경로를 거쳐 클러스터 DNS 가 `minio.<ns>.svc.cluster.local` 로 푸는 내부 전용 이름이기 때문입니다. 외부에서 닿으려면 Ingress·Route·NodePort·LoadBalancer 같은 외부 접점을 거쳐야 합니다.

### 정답 4 — hosts 수정 없는 VIP 직결 검증

`curl -v --resolve portal.apps.<cluster>.example.com:443:10.0.0.46 https://portal.apps.<cluster>.example.com` 을 실행합니다. `--resolve` 옵션이 로컬 DNS 나 `hosts` 파일을 수정하지 않고도 TLS SNI 와 HTTP `Host` 헤더를 도메인 그대로 보낸 채 지정한 VIP 로만 연결해 주기 때문입니다.

### 정답 5 — Secret·ConfigMap 마스킹 이유

Secret 의 `.data` 는 암호화가 아니라 Base64 인코딩만 되어 있어 실제 값을 화면이나 로그에 찍으면 자격증명이 그대로 노출되기 때문입니다. ConfigMap 에도 DB 비밀번호 같은 키가 섞여 있을 수 있습니다. 그래서 Secret 은 키 목록만 확인하고 ConfigMap 은 민감 키를 `***` 로 가려 출력합니다. 다만 키 이름 필터는 URL 이나 설정 파일 값 안에 든 비밀번호를 거르지 못합니다.



## 참고 자료

[^ocp-ingress-route]: Red Hat OpenShift Container Platform 4.18, "Ingress and load balancing — 1.1.4. Creating a route through an Ingress object". <https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/ingress_and_load_balancing/routes#nw-ingress-creating-a-route-via-an-ingress_creating-basic-routes>
[^ocp-ctrl]: openshift/route-controller-manager `release-4.18`, `pkg/route/ingress/ingress.go`. <https://github.com/openshift/route-controller-manager/blob/release-4.18/pkg/route/ingress/ingress.go>
[^ocp-router]: openshift/router `release-4.18`, `images/router/haproxy/conf/haproxy-config.template`. <https://github.com/openshift/router/blob/release-4.18/images/router/haproxy/conf/haproxy-config.template>
[^ocp-config-ingress]: Red Hat OpenShift Container Platform 4.18, "Config APIs — Ingress [config.openshift.io/v1]". <https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/config_apis/ingress-config-openshift-io-v1>
[^ocp-config-dns]: Red Hat OpenShift Container Platform 4.18, "Config APIs — DNS [config.openshift.io/v1]". <https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/config_apis/dns-config-openshift-io-v1>
[^kubectl-setenv]: kubernetes/kubectl `release-1.33`, `pkg/cmd/set/set_env.go`. <https://github.com/kubernetes/kubectl/blob/release-1.33/pkg/cmd/set/set_env.go>
[^k8s-ingress]: Kubernetes Documentation, "Ingress". <https://kubernetes.io/docs/concepts/services-networking/ingress/>
[^k8s-gateway]: Kubernetes Documentation, "Gateway API". <https://kubernetes.io/docs/concepts/services-networking/gateway/>
[^k8s-service]: Kubernetes Documentation, "Service". <https://kubernetes.io/docs/concepts/services-networking/service/>
[^k8s-dns]: Kubernetes Documentation, "DNS for Services and Pods". <https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/>

- [Ingress로 여러 서비스를 한 IP에 노출하기](../08_cloud/book/kubernetes-in-action/12-01.Ingress%EB%A1%9C%20%EC%97%AC%EB%9F%AC%20%EC%84%9C%EB%B9%84%EC%8A%A4%EB%A5%BC%20%ED%95%9C%20IP%EC%97%90%20%EB%85%B8%EC%B6%9C%ED%95%98%EA%B8%B0.md) — Ingress 오브젝트·컨트롤러·L7 프록시의 역할 분리 원리
- [외부 노출 — NodePort·LoadBalancer·트래픽 정책](../08_cloud/book/kubernetes-in-action/11-02.%EC%99%B8%EB%B6%80%20%EB%85%B8%EC%B6%9C%20%E2%80%94%20NodePort%C2%B7LoadBalancer%C2%B7%ED%8A%B8%EB%9E%98%ED%94%BD%20%EC%A0%95%EC%B1%85.md) — NodePort 와 LoadBalancer 가 외부 요청을 전달하는 구조와 포트 대역
- [엔드포인트·DNS·토폴로지·readiness](../08_cloud/book/kubernetes-in-action/11-03.%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8%C2%B7DNS%C2%B7%ED%86%A0%ED%8F%B4%EB%A1%9C%EC%A7%80%C2%B7readiness.md) — 클러스터 내부 CoreDNS 와 EndpointSlice 가 서비스 이름을 푸는 과정
- [Gateway API 개념과 Gateway 배포](../08_cloud/book/kubernetes-in-action/13-01.Gateway%20API%20%EA%B0%9C%EB%85%90%EA%B3%BC%20Gateway%20%EB%B0%B0%ED%8F%AC.md) — Ingress 에서 역할 분리된 Gateway·HTTPRoute 모델로의 전환 배경
- [ConfigMap으로 설정 분리하기](../08_cloud/book/kubernetes-in-action/08-02.ConfigMap%EC%9C%BC%EB%A1%9C%20%EC%84%A4%EC%A0%95%20%EB%B6%84%EB%A6%AC%ED%95%98%EA%B8%B0.md) — ConfigMap 을 환경변수·볼륨으로 Pod 에 주입하는 방법과 주의점
