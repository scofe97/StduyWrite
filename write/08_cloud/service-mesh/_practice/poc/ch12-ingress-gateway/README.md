# Ch12 - Ingress Gateway 실습
---
> 대응 학습 문서: `learning/ch12-ingress-gateway/LEARN.md`

Gateway와 VirtualService를 조합하여 외부 트래픽을 클러스터 내부 서비스로 라우팅한다. TLS 모드(SIMPLE/MUTUAL/PASSTHROUGH)를 단계별로 설정하고, HTTP에서 HTTPS로 강제 리다이렉트하는 방법까지 실습한다.

참조 파일: `../install/sidecar/istio-values.yaml`

## 사전 조건

`istio-system` 또는 `istio-ingress` 네임스페이스에 `istio-ingressgateway`가 Running 상태여야 한다. bookinfo 앱이 `bookinfo` 네임스페이스에 배포되어 있어야 한다.

```bash
kubectl get pods -n istio-ingress
kubectl get pods -n bookinfo
```

ingressgateway의 외부 접근 주소를 환경변수로 저장한다:

```bash
# LoadBalancer인 경우
export INGRESS_HOST=$(kubectl get svc istio-ingressgateway -n istio-ingress \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# NodePort인 경우
export INGRESS_HOST=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="ExternalIP")].address}')
export INGRESS_PORT=$(kubectl get svc istio-ingressgateway -n istio-ingress \
  -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
```

## 실습 항목

| # | 개념 | 실습 내용 | 검증 방법 |
|---|------|----------|----------|
| 1 | Gateway (HTTP) | 80 포트 Gateway 리소스 생성 | curl로 외부 접속 확인 |
| 2 | VirtualService | productpage로 라우팅 연결 | 브라우저에서 bookinfo 페이지 확인 |
| 3 | TLS SIMPLE | 인증서 생성 → Secret → Gateway HTTPS 설정 | curl --cacert로 443 접속 |
| 4 | HTTP→HTTPS 리다이렉트 | httpsRedirect: true 설정 | curl -L로 301 리다이렉트 확인 |
| 5 | mTLS Gateway | MUTUAL 모드 + 클라이언트 인증서 | 클라이언트 인증서 없이 접속 거부 확인 |
| 6 | TCP Gateway | echo 서비스 TCP 31400 포트 | TCP telnet/nc로 접속 확인 |
| 7 | SNI Passthrough | PASSTHROUGH 모드 + TLS 헤더 라우팅 | SNI 기반 라우팅 확인 |

## 실습 상세

### 1. Gateway 리소스 생성 (HTTP 80)

**목표**: 외부 트래픽을 받는 진입점(Gateway)을 설정한다. VirtualService 없이 Gateway만 있으면 라우팅 대상이 없어 404가 반환된다.

**단계**:

```bash
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: bookinfo-gateway
  namespace: bookinfo
spec:
  selector:
    istio: ingressgateway
  servers:
    - port:
        number: 80
        name: http
        protocol: HTTP
      hosts:
        - "*"
EOF

# Gateway 생성 확인
kubectl get gateway -n bookinfo
kubectl describe gateway bookinfo-gateway -n bookinfo
```

**검증**: Gateway가 생성되었지만 VirtualService가 없으므로 아직 접속하면 404가 반환된다.

```bash
curl -s -o /dev/null -w "%{http_code}" http://${INGRESS_HOST}:${INGRESS_PORT}/productpage
# 예상: 404
```

### 2. VirtualService로 bookinfo productpage 연결

**목표**: Gateway로 들어온 트래픽을 productpage 서비스로 전달한다.

**단계**:

```bash
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: bookinfo
  namespace: bookinfo
spec:
  hosts:
    - "*"
  gateways:
    - bookinfo-gateway
  http:
    - match:
        - uri:
            exact: /productpage
        - uri:
            prefix: /static
        - uri:
            exact: /login
        - uri:
            exact: /logout
        - uri:
            prefix: /api/v1/products
      route:
        - destination:
            host: productpage
            port:
              number: 9080
EOF

# 라우팅 확인
kubectl get virtualservice -n bookinfo
istioctl proxy-config route \
  $(kubectl get pod -n istio-ingress -l app=istio-ingressgateway -o jsonpath='{.items[0].metadata.name}') \
  -n istio-ingress
```

**검증**: `/productpage` 경로가 200 응답을 반환해야 한다.

```bash
curl -s -o /dev/null -w "%{http_code}" http://${INGRESS_HOST}:${INGRESS_PORT}/productpage
# 예상: 200
```

### 3. TLS SIMPLE 모드 (서버 인증서)

**목표**: HTTPS 접속을 위한 서버 인증서를 생성하고 Gateway에 적용한다. 클라이언트는 서버 인증서만 검증한다.

**단계**:

```bash
# 자체 서명 인증서 생성
mkdir -p /tmp/certs && cd /tmp/certs

# CA 키 및 인증서 생성
openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 \
  -subj '/O=test Inc./CN=example.com' \
  -keyout example.com.key -out example.com.crt

# 서버 인증서 생성
openssl req -out bookinfo.example.com.csr -newkey rsa:2048 -nodes \
  -keyout bookinfo.example.com.key \
  -subj "/CN=bookinfo.example.com/O=bookinfo"
openssl x509 -req -sha256 -days 365 \
  -CA example.com.crt -CAkey example.com.key -CAcreateserial \
  -in bookinfo.example.com.csr -out bookinfo.example.com.crt

# TLS Secret 생성
kubectl create -n istio-ingress secret tls bookinfo-tls \
  --key=bookinfo.example.com.key \
  --cert=bookinfo.example.com.crt

# Gateway 업데이트 (HTTPS 443 추가)
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: bookinfo-gateway
  namespace: bookinfo
spec:
  selector:
    istio: ingressgateway
  servers:
    - port:
        number: 443
        name: https
        protocol: HTTPS
      tls:
        mode: SIMPLE
        credentialName: bookinfo-tls
      hosts:
        - "bookinfo.example.com"
EOF

# HTTPS 접속 테스트
SECURE_PORT=$(kubectl get svc istio-ingressgateway -n istio-ingress \
  -o jsonpath='{.spec.ports[?(@.name=="https")].nodePort}')

curl -s -HHost:bookinfo.example.com \
  --cacert /tmp/certs/example.com.crt \
  -o /dev/null -w "%{http_code}" \
  https://${INGRESS_HOST}:${SECURE_PORT}/productpage
# 예상: 200
```

**검증**: 서버 인증서 없이 접속하면 실패해야 한다.

```bash
curl -k -s -HHost:bookinfo.example.com \
  -o /dev/null -w "%{http_code}" \
  https://${INGRESS_HOST}:${SECURE_PORT}/productpage
# -k 플래그로 인증서 검증 건너뜀 → 200 (서버 인증서는 있음)
```

### 4. HTTP → HTTPS 리다이렉트

**목표**: HTTP 80으로 들어오는 요청을 HTTPS 443으로 강제 리다이렉트한다. 보안 정책상 평문 HTTP를 허용하지 않을 때 사용한다.

**단계**:

```bash
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: bookinfo-gateway
  namespace: bookinfo
spec:
  selector:
    istio: ingressgateway
  servers:
    - port:
        number: 80
        name: http
        protocol: HTTP
      hosts:
        - "bookinfo.example.com"
      tls:
        httpsRedirect: true
    - port:
        number: 443
        name: https
        protocol: HTTPS
      tls:
        mode: SIMPLE
        credentialName: bookinfo-tls
      hosts:
        - "bookinfo.example.com"
EOF

# 리다이렉트 확인 (-L 옵션으로 자동 따라가기)
curl -v -HHost:bookinfo.example.com \
  http://${INGRESS_HOST}:${INGRESS_PORT}/productpage 2>&1 | grep -E "HTTP|Location"
# 예상: HTTP/1.1 301 Moved Permanently + Location: https://...
```

**검증**: 301 응답과 함께 `Location: https://bookinfo.example.com/productpage` 헤더가 응답에 포함되어야 한다.

### 5. mTLS Gateway (MUTUAL 모드)

**목표**: 서버가 클라이언트 인증서도 요구하는 상호 TLS를 설정한다. 클라이언트 인증서 없이 접속하면 거부된다.

**단계**:

```bash
cd /tmp/certs

# 클라이언트 인증서 생성
openssl req -out client.example.com.csr -newkey rsa:2048 -nodes \
  -keyout client.example.com.key \
  -subj "/CN=client.example.com/O=client"
openssl x509 -req -sha256 -days 365 \
  -CA example.com.crt -CAkey example.com.key -CAcreateserial \
  -in client.example.com.csr -out client.example.com.crt

# CA 인증서를 포함하는 Secret 생성 (MUTUAL 모드에서 CA 검증에 사용)
kubectl create -n istio-ingress secret generic bookinfo-mtls \
  --from-file=tls.key=bookinfo.example.com.key \
  --from-file=tls.crt=bookinfo.example.com.crt \
  --from-file=ca.crt=example.com.crt

# Gateway MUTUAL 모드로 업데이트
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: bookinfo-gateway-mtls
  namespace: bookinfo
spec:
  selector:
    istio: ingressgateway
  servers:
    - port:
        number: 443
        name: https-mtls
        protocol: HTTPS
      tls:
        mode: MUTUAL
        credentialName: bookinfo-mtls
      hosts:
        - "bookinfo-mtls.example.com"
EOF

# 클라이언트 인증서 없이 접속 (거부 확인)
curl -s -HHost:bookinfo-mtls.example.com \
  --cacert /tmp/certs/example.com.crt \
  -o /dev/null -w "%{http_code}" \
  https://${INGRESS_HOST}:${SECURE_PORT}/productpage
# 예상: 000 또는 연결 오류

# 클라이언트 인증서 포함하여 접속
curl -s -HHost:bookinfo-mtls.example.com \
  --cacert /tmp/certs/example.com.crt \
  --cert /tmp/certs/client.example.com.crt \
  --key /tmp/certs/client.example.com.key \
  -o /dev/null -w "%{http_code}" \
  https://${INGRESS_HOST}:${SECURE_PORT}/productpage
# 예상: 200
```

**검증**: 클라이언트 인증서 없이 접속 시 TLS handshake 오류가 발생해야 한다.

### 6. TCP Gateway (echo 서비스)

**목표**: HTTP가 아닌 TCP 프로토콜을 처리하는 Gateway를 설정한다.

**단계**:

```bash
# TCP echo 서버 배포
cat <<'EOF' | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: tcp-echo
  namespace: bookinfo
  labels:
    app: tcp-echo
spec:
  ports:
    - name: tcp
      port: 9000
  selector:
    app: tcp-echo
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tcp-echo
  namespace: bookinfo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: tcp-echo
  template:
    metadata:
      labels:
        app: tcp-echo
    spec:
      containers:
        - name: tcp-echo
          image: docker.io/istio/tcp-echo-server:1.2
          args: ["9000", "hello"]
          ports:
            - containerPort: 9000
EOF

# TCP Gateway 설정 (31400 포트 사용)
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: tcp-echo-gateway
  namespace: bookinfo
spec:
  selector:
    istio: ingressgateway
  servers:
    - port:
        number: 31400
        name: tcp
        protocol: TCP
      hosts:
        - "*"
---
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: tcp-echo
  namespace: bookinfo
spec:
  hosts:
    - "*"
  gateways:
    - tcp-echo-gateway
  tcp:
    - match:
        - port: 31400
      route:
        - destination:
            host: tcp-echo
            port:
              number: 9000
EOF

# TCP 포트 확인
TCP_PORT=$(kubectl get svc istio-ingressgateway -n istio-ingress \
  -o jsonpath='{.spec.ports[?(@.name=="tcp")].nodePort}')

# 접속 테스트
echo "world" | nc -w 3 ${INGRESS_HOST} ${TCP_PORT}
# 예상: hello world
```

**검증**: `echo "world" | nc` 명령 결과로 `hello world`가 출력되어야 한다.

### 7. SNI Passthrough 라우팅

**목표**: TLS를 Gateway에서 종료하지 않고, SNI 헤더를 기반으로 백엔드 서비스로 TLS 트래픽을 그대로 전달한다.

**단계**:

```bash
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: bookinfo-passthrough-gateway
  namespace: bookinfo
spec:
  selector:
    istio: ingressgateway
  servers:
    - port:
        number: 443
        name: tls-passthrough
        protocol: TLS
      tls:
        mode: PASSTHROUGH
      hosts:
        - "passthrough.example.com"
---
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: bookinfo-passthrough
  namespace: bookinfo
spec:
  hosts:
    - "passthrough.example.com"
  gateways:
    - bookinfo-passthrough-gateway
  tls:
    - match:
        - port: 443
          sniHosts:
            - passthrough.example.com
      route:
        - destination:
            host: productpage
            port:
              number: 9080
EOF

# SNI 라우팅 설정 확인
istioctl proxy-config listener \
  $(kubectl get pod -n istio-ingress -l app=istio-ingressgateway -o jsonpath='{.items[0].metadata.name}') \
  -n istio-ingress | grep -E "443|TLS|PASSTHROUGH"
```

**검증**: `istioctl proxy-config listener` 결과에서 443 포트가 `PASSTHROUGH` 모드로 설정되어야 한다.

## 정리 (Cleanup)

```bash
# 생성한 Gateway, VirtualService 제거
kubectl delete gateway bookinfo-gateway bookinfo-gateway-mtls tcp-echo-gateway bookinfo-passthrough-gateway -n bookinfo --ignore-not-found=true
kubectl delete virtualservice bookinfo tcp-echo bookinfo-passthrough -n bookinfo --ignore-not-found=true

# TLS Secret 제거
kubectl delete secret bookinfo-tls bookinfo-mtls -n istio-ingress --ignore-not-found=true

# TCP echo 서비스 제거
kubectl delete deployment tcp-echo -n bookinfo --ignore-not-found=true
kubectl delete service tcp-echo -n bookinfo --ignore-not-found=true

# 인증서 파일 제거
rm -rf /tmp/certs
```
