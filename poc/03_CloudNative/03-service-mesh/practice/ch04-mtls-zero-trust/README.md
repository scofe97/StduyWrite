# Ch04 - mTLS와 Zero Trust 실습
---
> 대응 학습 문서: `learning/04-mtls-and-zero-trust/LEARN.md`

## 사전 조건

- openssl 설치 (`brew install openssl` 또는 시스템 기본 포함)
- curl 설치
- Kind 클러스터 실행 중, Istio 설치 완료 (항목 5~6)
- Python 3 또는 Node.js (간단한 HTTPS 서버용)

## 실습 항목

| # | 개념 | 실습 내용 | 검증 방법 |
|---|------|----------|----------|
| 1 | PKI 구조 | Root CA → Intermediate CA 인증서 체인 생성 | `openssl verify` |
| 2 | 서버/클라이언트 인증서 | 각 엔드포인트용 인증서 발급 | `openssl x509 -text` |
| 3 | 단방향 TLS | curl `--cacert`로 서버 인증서 검증 | HTTPS 응답 확인 |
| 4 | mTLS | curl `--cert` + `--key` + `--cacert` | 클라이언트 인증서 없으면 거부 |
| 5 | 인증서 없는 접근 차단 | 인증서 미제공 시 실패 확인 | `SSL handshake failed` |
| 6 | Istio 자동 mTLS 확인 | `istioctl authn tls-check` | STRICT/PERMISSIVE 모드 확인 |

## 실습 상세

### 1. Root CA → Intermediate CA 인증서 체인 생성

**목표**: 실제 PKI 구조처럼 Root CA가 Intermediate CA를 서명하는 2단계 체인을 만든다. 직접 Root CA로 서버 인증서를 발급하지 않는 이유는 Root CA를 오프라인으로 보호하기 위해서다.

**단계**:
1. 작업 디렉토리 생성
   ```bash
   mkdir -p /tmp/mtls-lab/{ca,certs}
   cd /tmp/mtls-lab
   ```
2. Root CA 키 및 자체 서명 인증서 생성
   ```bash
   # Root CA 개인키
   openssl genrsa -out ca/root-ca.key 4096

   # Root CA 인증서 (자체 서명, 유효기간 3650일)
   openssl req -x509 -new -nodes \
     -key ca/root-ca.key \
     -sha256 -days 3650 \
     -out ca/root-ca.crt \
     -subj "/CN=Root CA/O=Lab/C=KR"
   ```
3. Intermediate CA 키 및 CSR 생성
   ```bash
   openssl genrsa -out ca/intermediate-ca.key 4096

   openssl req -new \
     -key ca/intermediate-ca.key \
     -out ca/intermediate-ca.csr \
     -subj "/CN=Intermediate CA/O=Lab/C=KR"
   ```
4. Root CA가 Intermediate CA에 서명
   ```bash
   openssl x509 -req \
     -in ca/intermediate-ca.csr \
     -CA ca/root-ca.crt \
     -CAkey ca/root-ca.key \
     -CAcreateserial \
     -out ca/intermediate-ca.crt \
     -days 1825 \
     -sha256 \
     -extensions v3_ca \
     -extfile <(echo "[v3_ca]\nbasicConstraints=critical,CA:true\nkeyUsage=critical,keyCertSign,cRLSign")
   ```
5. 체인 파일 생성
   ```bash
   cat ca/intermediate-ca.crt ca/root-ca.crt > ca/ca-chain.crt
   ```

**검증**:
```bash
openssl verify -CAfile ca/root-ca.crt ca/intermediate-ca.crt
# ca/intermediate-ca.crt: OK
```

### 2. 서버 및 클라이언트 인증서 발급

**목표**: Intermediate CA를 통해 서버용과 클라이언트용 인증서를 각각 발급한다.

**단계**:
1. 서버 인증서 발급 (SAN 포함)
   ```bash
   openssl genrsa -out certs/server.key 2048

   openssl req -new \
     -key certs/server.key \
     -out certs/server.csr \
     -subj "/CN=localhost/O=Lab/C=KR"

   openssl x509 -req \
     -in certs/server.csr \
     -CA ca/intermediate-ca.crt \
     -CAkey ca/intermediate-ca.key \
     -CAcreateserial \
     -out certs/server.crt \
     -days 365 -sha256 \
     -extfile <(echo "subjectAltName=DNS:localhost,IP:127.0.0.1")
   ```
2. 클라이언트 인증서 발급
   ```bash
   openssl genrsa -out certs/client.key 2048

   openssl req -new \
     -key certs/client.key \
     -out certs/client.csr \
     -subj "/CN=client/O=Lab/C=KR"

   openssl x509 -req \
     -in certs/client.csr \
     -CA ca/intermediate-ca.crt \
     -CAkey ca/intermediate-ca.key \
     -CAcreateserial \
     -out certs/client.crt \
     -days 365 -sha256
   ```
3. 인증서 내용 확인
   ```bash
   openssl x509 -in certs/server.crt -text -noout | grep -E "Subject:|Issuer:|DNS:|IP:"
   ```

**검증**:
```
Subject: CN=localhost, O=Lab, C=KR
Issuer: CN=Intermediate CA, O=Lab, C=KR
DNS:localhost, IP Address:127.0.0.1
```

### 3. 단방향 TLS 테스트

**목표**: 클라이언트가 서버 인증서만 검증하는 일반적인 HTTPS 구조를 실습한다.

**단계**:
1. Python으로 간단한 TLS 서버 기동
   ```bash
   python3 - <<'PYEOF' &
   import ssl, http.server

   class Handler(http.server.BaseHTTPRequestHandler):
       def do_GET(self):
           self.send_response(200)
           self.end_headers()
           self.wfile.write(b"Hello TLS!\n")
       def log_message(self, *args): pass

   ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
   ctx.load_cert_chain('/tmp/mtls-lab/certs/server.crt',
                        '/tmp/mtls-lab/certs/server.key')
   ctx.load_verify_locations('/tmp/mtls-lab/ca/ca-chain.crt')

   httpd = http.server.HTTPServer(('localhost', 8443), Handler)
   httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
   print("TLS server listening on :8443")
   httpd.serve_forever()
   PYEOF
   sleep 1
   ```
2. CA 체인으로 서버 인증서 검증
   ```bash
   curl --cacert /tmp/mtls-lab/ca/ca-chain.crt https://localhost:8443
   ```

**검증**: `Hello TLS!` 가 출력된다.

### 4. mTLS 테스트

**목표**: 서버가 클라이언트 인증서까지 요구하도록 설정하고 mTLS 요청이 성공하는 것을 확인한다.

**단계**:
1. mTLS 서버로 재기동 (`verify_mode=CERT_REQUIRED` 추가)
   ```bash
   # 기존 서버 종료
   kill %1 2>/dev/null; sleep 1

   python3 - <<'PYEOF' &
   import ssl, http.server

   class Handler(http.server.BaseHTTPRequestHandler):
       def do_GET(self):
           cert = self.connection.getpeercert()
           cn = dict(x[0] for x in cert['subject']).get('commonName','unknown')
           self.send_response(200)
           self.end_headers()
           self.wfile.write(f"Hello {cn}! (mTLS OK)\n".encode())
       def log_message(self, *args): pass

   ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
   ctx.load_cert_chain('/tmp/mtls-lab/certs/server.crt',
                        '/tmp/mtls-lab/certs/server.key')
   ctx.load_verify_locations('/tmp/mtls-lab/ca/ca-chain.crt')
   ctx.verify_mode = ssl.CERT_REQUIRED

   httpd = http.server.HTTPServer(('localhost', 8443), Handler)
   httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
   print("mTLS server listening on :8443")
   httpd.serve_forever()
   PYEOF
   sleep 1
   ```
2. 클라이언트 인증서 포함하여 요청
   ```bash
   curl \
     --cacert /tmp/mtls-lab/ca/ca-chain.crt \
     --cert /tmp/mtls-lab/certs/client.crt \
     --key /tmp/mtls-lab/certs/client.key \
     https://localhost:8443
   ```

**검증**: `Hello client! (mTLS OK)` 가 출력된다.

### 5. 인증서 없이 접근 시도 → 실패 확인

**목표**: mTLS 서버에 클라이언트 인증서 없이 접근하면 TLS handshake에서 거부됨을 확인한다.

**단계**:
1. 클라이언트 인증서 없이 요청
   ```bash
   curl --cacert /tmp/mtls-lab/ca/ca-chain.crt https://localhost:8443
   ```
2. 오류 코드 확인
   ```bash
   curl -v --cacert /tmp/mtls-lab/ca/ca-chain.crt https://localhost:8443 2>&1 | \
     grep -E "SSL|alert|handshake|error"
   ```

**검증**:
```
curl: (35) OpenSSL SSL_connect: SSL_ERROR_SYSCALL
# 또는
alert handshake failure
```
클라이언트 인증서 없이는 연결이 거부된다.

### 6. Istio 자동 mTLS 확인

**목표**: Istio가 사이드카 간 통신에 자동으로 mTLS를 적용하고 있음을 `istioctl`로 확인한다.

**단계**:
1. 서비스 배포 (demo 네임스페이스에 istio-injection 활성화 가정)
   ```bash
   kubectl create namespace mtls-demo 2>/dev/null || true
   kubectl label namespace mtls-demo istio-injection=enabled --overwrite
   kubectl run httpbin --image=kennethreitz/httpbin \
     --port=80 -n mtls-demo
   kubectl expose pod httpbin --port=80 -n mtls-demo
   kubectl run client --image=curlimages/curl \
     --restart=Never -n mtls-demo -- sleep 3600
   ```
2. Pod가 뜰 때까지 대기
   ```bash
   kubectl wait --for=condition=Ready pod/httpbin -n mtls-demo --timeout=60s
   kubectl wait --for=condition=Ready pod/client -n mtls-demo --timeout=60s
   ```
3. mTLS 상태 확인
   ```bash
   istioctl authn tls-check client.mtls-demo
   ```
4. PeerAuthentication 명시적 STRICT 설정
   ```bash
   kubectl apply -f - <<EOF
   apiVersion: security.istio.io/v1beta1
   kind: PeerAuthentication
   metadata:
     name: default
     namespace: mtls-demo
   spec:
     mtls:
       mode: STRICT
   EOF

   istioctl authn tls-check client.mtls-demo
   ```

**검증**:
```
HOST:PORT                        STATUS     SERVER     CLIENT
httpbin.mtls-demo.svc.cluster.local:80   OK         mTLS       mTLS
```
`STATUS=OK`, `SERVER=mTLS`, `CLIENT=mTLS` 가 확인된다.

## 정리 (Cleanup)

```bash
kill %1 2>/dev/null; kill %2 2>/dev/null
rm -rf /tmp/mtls-lab
kubectl delete namespace mtls-demo
```
