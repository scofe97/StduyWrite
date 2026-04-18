# Ch08. 보안: 통신과 저장소

**핵심 질문**: "데이터를 전송하고 저장할 때 어떻게 보호하는가?"

---

## 🎯 학습 목표

1. 대칭·비대칭 암호화와 해시 함수가 각각 어떤 문제를 해결하는지 설명할 수 있다
2. TLS handshake 과정을 단계별로 서술하고, 인증서 체인의 신뢰 모델을 이해한다
3. OpenSSL로 키 생성·CSR 작성·자체 서명 인증서 발급·검증을 직접 수행할 수 있다
4. certbot으로 Let's Encrypt 인증서를 발급하고 자동 갱신 cron을 구성할 수 있다
5. AWS Secrets Manager와 HashiCorp Vault의 차이를 이해하고 기본 CLI를 사용할 수 있다
6. 저장소 암호화(EBS, S3 SSE, DB TDE)의 구조와 설정 방법을 파악한다

---

## 1. 암호화 기초

### 대칭 암호화: 속도를 위한 선택

대칭 암호화는 암호화와 복호화에 동일한 키를 사용하는 방식이다. 대표적인 알고리즘인 AES(Advanced Encryption Standard)는 초당 수 GB를 처리할 수 있어 대용량 데이터 암호화에 적합하다. 문제는 키 배분이다. 송신자와 수신자가 같은 키를 공유해야 하는데, 그 키를 안전하게 전달하는 과정 자체가 보안 위협이 된다. 실전에서는 대칭 암호화를 단독으로 쓰지 않고, 비대칭 암호화로 대칭 키를 교환한 뒤 본문 암호화에 대칭 암호화를 쓰는 방식(하이브리드)을 택한다. TLS가 바로 이 하이브리드 방식이다.

### 비대칭 암호화: 신뢰를 위한 선택

비대칭 암호화는 공개 키(public key)와 개인 키(private key)가 한 쌍을 이룬다. 공개 키로 암호화한 데이터는 대응하는 개인 키로만 복호화할 수 있다. RSA와 ECDSA가 대표적이다. ECDSA는 RSA와 동등한 보안 강도를 더 짧은 키 길이로 달성한다. 예를 들어 RSA 3072비트와 ECDSA 256비트는 보안 강도가 비슷하지만, ECDSA 키가 훨씬 작아 TLS handshake에서 전송 효율이 높다. 연산 비용이 대칭 암호화보다 수백 배 크므로 대량 데이터 암호화에는 적합하지 않다.

### 해시 함수: 무결성을 위한 단방향 변환

해시 함수는 임의 길이의 입력을 고정 길이 출력으로 변환하며, 역산이 불가능하다. SHA-256이 출력하는 256비트 다이제스트는 입력이 1비트만 바뀌어도 완전히 달라진다(눈사태 효과). 이 성질 덕분에 파일 무결성 검증, 디지털 서명, 패스워드 저장(bcrypt, Argon2) 등에 폭넓게 쓰인다. MD5와 SHA-1은 충돌 취약점이 발견되어 현재 보안 목적으로는 사용하지 않는다.

### 디지털 서명: 신원 증명과 무결성의 결합

디지털 서명은 개인 키로 서명하고 공개 키로 검증한다. 암호화 방향이 반대임에 주목하자. 송신자가 메시지 해시를 자신의 개인 키로 암호화(서명)하면, 수신자는 송신자의 공개 키로 복호화해 해시를 확인한다. 메시지가 변조되었다면 해시가 맞지 않고, 다른 사람이 서명했다면 공개 키로 검증이 실패한다. 인증서는 이 서명 메커니즘으로 CA(인증 기관)가 공개 키의 소유자를 보증하는 문서다.

---

## 2. TLS/SSL 통신 보안

### 인증서 체인의 신뢰 구조

브라우저가 `https://example.com`에 접속할 때 서버의 인증서를 어떻게 믿는가? 운영체제와 브라우저는 수십 개의 루트 CA 인증서를 미리 내장하고 있다. 서버 인증서는 루트 CA가 직접 서명하지 않고, 중간 CA(Intermediate CA)가 서명한다. 루트 CA → 중간 CA → 서버 인증서로 이어지는 체인이 형성되며, 각 단계에서 상위 기관의 서명을 검증한다. 중간 CA를 두는 이유는 루트 CA의 개인 키를 오프라인으로 보관해 보안을 강화하기 위해서다.

### TLS 1.3 Handshake 과정

TLS 1.3은 왕복 횟수를 TLS 1.2의 2-RTT에서 1-RTT로 줄였다. 최초 연결이 아닌 경우 0-RTT 재개도 지원한다.

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server

    Note over C,S: TLS 1.3 Handshake (1-RTT)

    C->>S: ClientHello<br/>(지원 cipher suites, key_share)
    Note over S: 키 교환 알고리즘 선택<br/>서버 측 key_share 생성
    S->>C: ServerHello<br/>(선택된 cipher, key_share)
    Note over C,S: 양측이 공유 비밀 도출<br/>(ECDHE → handshake 키)
    S->>C: {Certificate, CertificateVerify,<br/>Finished} [암호화됨]
    Note over C: 인증서 체인 검증<br/>서명 확인 → Finished MAC 검증
    C->>S: {Finished} [암호화됨]
    Note over C,S: Application 키로 전환<br/>데이터 전송 시작
    C->>S: 암호화된 HTTP 요청
    S->>C: 암호화된 HTTP 응답
```

---

## 3. OpenSSL 실습

OpenSSL은 TLS 구현과 인증서 관리에 쓰이는 오픈소스 라이브러리이자 CLI 도구다. 운영 환경에서 자체 서명 인증서가 필요하거나 내부 PKI를 구성할 때 직접 사용할 일이 많다.

```bash
# ── 1. RSA 개인 키 생성 (4096비트 권장, 최소 2048비트) ──
openssl genrsa -out server.key 4096
# AES-256으로 키 파일 자체를 암호화하려면 -aes256 옵션 추가
openssl genrsa -aes256 -out server.key 4096

# ── 2. ECDSA 키 생성 (RSA보다 짧고 빠름, 현대 서비스에 권장) ──
openssl ecparam -name prime256v1 -genkey -noout -out ec.key

# ── 3. 공개 키 추출 ──
openssl rsa -in server.key -pubout -out server.pub
# ECDSA 키에서
openssl ec -in ec.key -pubout -out ec.pub

# ── 4. CSR(Certificate Signing Request) 생성 ──
# CSR은 CA에 "이 공개 키를 인증해달라"고 요청하는 문서다
openssl req -new \
  -key server.key \
  -out server.csr \
  -subj "/C=KR/ST=Seoul/L=Gangnam/O=MyCompany/CN=example.com"

# SAN(Subject Alternative Name) 포함 — 현대 브라우저는 SAN 필수
openssl req -new \
  -key server.key \
  -out server.csr \
  -config <(cat <<EOF
[req]
distinguished_name = dn
req_extensions     = v3_req
prompt             = no

[dn]
C  = KR
ST = Seoul
O  = MyCompany
CN = example.com

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = example.com
DNS.2 = www.example.com
DNS.3 = api.example.com
EOF
)

# ── 5. CSR 내용 확인 ──
openssl req -text -noout -in server.csr

# ── 6. 자체 서명 인증서 발급 (개발/테스트 환경) ──
# -days 365: 1년 유효기간
openssl x509 -req \
  -in server.csr \
  -signkey server.key \
  -out server.crt \
  -days 365 \
  -extensions v3_req \
  -extfile <(printf "[v3_req]\nsubjectAltName=DNS:example.com,DNS:www.example.com")

# ── 7. 인증서 정보 확인 ──
openssl x509 -text -noout -in server.crt
# 만료일만 확인
openssl x509 -enddate -noout -in server.crt

# ── 8. 인증서 체인 검증 ──
openssl verify -CAfile ca.crt server.crt
# 원격 서버 인증서 검증
openssl s_client -connect example.com:443 -showcerts 2>/dev/null \
  | openssl x509 -text -noout

# ── 9. 해시 계산 ──
echo -n "hello" | openssl dgst -sha256
openssl dgst -sha256 -hex server.crt

# ── 10. 키-인증서 매칭 확인 ──
# 세 출력이 동일하면 쌍이 맞는 것
openssl rsa  -modulus -noout -in server.key | openssl md5
openssl req  -modulus -noout -in server.csr | openssl md5
openssl x509 -modulus -noout -in server.crt | openssl md5
```

---

## 4. Let's Encrypt 자동화

Let's Encrypt는 무료로 DV(Domain Validated) 인증서를 발급하며, 유효기간은 90일이다. 짧은 유효기간은 의도적인 설계다. 인증서가 탈취되더라도 피해 기간이 짧고, 자동 갱신을 강제함으로써 실수로 만료 상태가 지속되는 상황을 줄인다.

```bash
#!/bin/bash
# certbot-setup.sh — Let's Encrypt 인증서 발급 및 자동 갱신 설정

set -euo pipefail

DOMAIN="example.com"
EMAIL="admin@example.com"
WEBROOT="/var/www/html"

# ── 1. certbot 설치 (Ubuntu/Debian) ──
apt-get update
apt-get install -y certbot python3-certbot-nginx

# ── 2. 인증서 발급 (Nginx 플러그인 사용, 80→443 리다이렉트 자동 구성) ──
certbot --nginx \
  --non-interactive \
  --agree-tos \
  --email "$EMAIL" \
  --domains "$DOMAIN,www.$DOMAIN"

# ── 3. Webroot 방식 (Nginx 설정을 건드리지 않고 발급) ──
# 도메인 소유 증명을 위해 .well-known/acme-challenge/ 경로에 파일을 생성한다
certbot certonly \
  --webroot \
  --webroot-path "$WEBROOT" \
  --non-interactive \
  --agree-tos \
  --email "$EMAIL" \
  --domains "$DOMAIN"

# ── 4. 인증서 위치 확인 ──
# /etc/letsencrypt/live/$DOMAIN/
#   fullchain.pem  — 서버 인증서 + 중간 CA 체인
#   privkey.pem    — 개인 키
#   cert.pem       — 서버 인증서만
#   chain.pem      — 중간 CA 체인만
ls -la "/etc/letsencrypt/live/$DOMAIN/"

# ── 5. 수동 갱신 테스트 (실제로 갱신하지 않고 시뮬레이션) ──
certbot renew --dry-run

# ── 6. cron 자동 갱신 등록 ──
# certbot renew는 만료 30일 이내일 때만 실제 갱신을 수행한다
# 하루 두 번 실행해 실패 시 재시도 기회를 준다
(crontab -l 2>/dev/null; cat <<'CRON'
# Let's Encrypt 인증서 자동 갱신 (매일 03:00, 15:00)
0 3,15 * * * /usr/bin/certbot renew --quiet --post-hook "systemctl reload nginx" >> /var/log/certbot-renew.log 2>&1
CRON
) | crontab -

echo "Cron 등록 완료:"
crontab -l | grep certbot

# ── 7. systemd timer 방식 (cron 대신) ──
# certbot 패키지 설치 시 자동으로 등록되는 경우가 많다
systemctl status certbot.timer
systemctl list-timers certbot.timer

# ── 8. 인증서 만료 날짜 모니터링 ──
certbot certificates
openssl x509 -enddate -noout \
  -in "/etc/letsencrypt/live/$DOMAIN/cert.pem"
```

```nginx
# /etc/nginx/sites-available/example.com — 현대적 TLS 설정
server {
    listen 80;
    server_name example.com www.example.com;
    # ACME 챌린지는 HTTP로 허용, 나머지는 HTTPS로 리다이렉트
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    http2 on;
    server_name example.com www.example.com;

    # Let's Encrypt 인증서
    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # 현대적 TLS 설정 (TLS 1.2 이상, 구형 클라이언트 차단)
    ssl_protocols       TLSv1.2 TLSv1.3;
    # ECDHE 기반 PFS(Perfect Forward Secrecy) 암호 스위트 우선
    ssl_ciphers         ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;
    ssl_prefer_server_ciphers off; # TLS 1.3에서는 클라이언트 선택을 존중

    # OCSP Stapling — 브라우저가 CA에 직접 CRL 조회하지 않아도 됨
    ssl_stapling        on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;
    resolver            8.8.8.8 8.8.4.4 valid=300s;

    # HSTS — 일단 HTTPS로 방문한 브라우저는 2년간 HTTP 시도 차단
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

    ssl_session_cache   shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off; # PFS를 위해 세션 티켓 비활성화

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 5. 시크릿 관리

### 평문 시크릿의 문제

개발자들이 흔히 저지르는 실수는 `.env` 파일이나 코드에 시크릿을 직접 쓰는 것이다. `.env` 파일이 Git에 올라가거나, 로그에 환경변수가 출력되거나, 배포 파이프라인 변수가 노출되면 그 순간 시크릿은 의미를 잃는다.

```bash
# Bad: 코드에 하드코딩
DB_PASSWORD="super-secret-password-123"
API_KEY="sk-1234567890abcdef"

# Bad: .env 파일에 평문 저장 후 Git 커밋
# .gitignore에 .env를 추가했더라도 한 번이라도 커밋되면 히스토리에 남는다
echo "DB_PASSWORD=super-secret" >> .env
git add .env  # ← 절대 금지

# Good: 런타임에 시크릿 매니저에서 가져오기
# 코드에는 경로/ARN만, 실제 값은 코드 밖에 존재
DB_PASSWORD=$(aws secretsmanager get-secret-value \
  --secret-id prod/myapp/db \
  --query SecretString \
  --output text | jq -r '.password')
```

### AWS Secrets Manager 전체 워크플로

```bash
# ── 1. 시크릿 생성 ──
aws secretsmanager create-secret \
  --name "prod/myapp/db" \
  --description "Production DB credentials" \
  --secret-string '{"username":"dbadmin","password":"C0mpl3xP@ss!"}' \
  --region ap-northeast-2

# ── 2. KV 형식으로 생성 (개별 키 접근 가능) ──
aws secretsmanager create-secret \
  --name "prod/myapp/api-keys" \
  --secret-string '{
    "stripe_key": "sk_live_xxx",
    "sendgrid_key": "SG.xxx"
  }'

# ── 3. 시크릿 값 조회 ──
aws secretsmanager get-secret-value \
  --secret-id "prod/myapp/db" \
  --query SecretString \
  --output text

# jq로 특정 필드만 추출
aws secretsmanager get-secret-value \
  --secret-id "prod/myapp/db" \
  --query SecretString \
  --output text | jq -r '.password'

# ── 4. 시크릿 갱신 ──
aws secretsmanager put-secret-value \
  --secret-id "prod/myapp/db" \
  --secret-string '{"username":"dbadmin","password":"N3wP@ss!2025"}'

# ── 5. 자동 로테이션 설정 (Lambda 기반) ──
# RDS의 경우 AWS가 제공하는 로테이션 Lambda를 사용할 수 있다
aws secretsmanager rotate-secret \
  --secret-id "prod/myapp/db" \
  --rotation-lambda-arn "arn:aws:lambda:ap-northeast-2:123456789:function:SecretsManagerRDSRotation" \
  --rotation-rules AutomaticallyAfterDays=30

# ── 6. 로테이션 상태 확인 ──
aws secretsmanager describe-secret \
  --secret-id "prod/myapp/db" \
  --query '{RotationEnabled:RotationEnabled,LastRotatedDate:LastRotatedDate}'

# ── 7. 시크릿 목록 조회 ──
aws secretsmanager list-secrets \
  --filter Key=name,Values=prod/myapp \
  --query 'SecretList[*].{Name:Name,ARN:ARN}'

# ── 8. 리소스 기반 정책 설정 (다른 계정/서비스에서 접근 허용) ──
aws secretsmanager put-resource-policy \
  --secret-id "prod/myapp/db" \
  --resource-policy '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"AWS": "arn:aws:iam::123456789:role/ECSTaskRole"},
      "Action": ["secretsmanager:GetSecretValue"],
      "Resource": "*"
    }]
  }'

# ── 9. 버전 관리 — 로테이션 중 이전 버전도 유지된다 ──
aws secretsmanager list-secret-version-ids \
  --secret-id "prod/myapp/db"
```

### HashiCorp Vault 기초

Vault는 AWS Secrets Manager와 달리 클라우드 벤더에 종속되지 않는다. 온프레미스나 멀티 클라우드 환경에서 통합 시크릿 관리가 필요할 때 선택한다. 정적 시크릿(KV) 외에도 동적 시크릿이 핵심 기능이다. 동적 시크릿은 요청할 때마다 임시 자격증명을 생성하고, TTL이 지나면 자동 폐기한다. DB 계정이 고정되지 않으므로 유출되더라도 재사용이 불가능하다.

```bash
# ── Vault 기본 사용 ──
# KV v2 시크릿 엔진 활성화
vault secrets enable -path=secret kv-v2

# 시크릿 저장
vault kv put secret/myapp/db \
  username="dbadmin" \
  password="C0mpl3xP@ss!"

# 시크릿 조회
vault kv get secret/myapp/db
vault kv get -field=password secret/myapp/db

# 버전 히스토리 확인
vault kv metadata get secret/myapp/db

# ── 동적 시크릿: DB 엔진 예시 ──
vault secrets enable database

vault write database/config/my-postgres \
  plugin_name=postgresql-database-plugin \
  allowed_roles="readonly" \
  connection_url="postgresql://{{username}}:{{password}}@postgres:5432/mydb" \
  username="vault" \
  password="vault-password"

# 역할 정의: TTL 1시간, 최대 24시간
vault write database/roles/readonly \
  db_name=my-postgres \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"

# 임시 자격증명 발급 — 요청마다 새 계정이 생성된다
vault read database/creds/readonly
```

---

## 6. 저장소 암호화 (Encryption at Rest)

전송 중 암호화(TLS)로 네트워크를 보호했다면, 저장된 데이터는 별도로 보호해야 한다. 서버가 탈취되거나 스토리지 매체가 물리적으로 분실될 경우 암호화되지 않은 데이터는 곧바로 노출된다.

### EBS 볼륨 암호화

```bash
# ── EBS 볼륨 생성 시 암호화 활성화 ──
aws ec2 create-volume \
  --availability-zone ap-northeast-2a \
  --size 100 \
  --volume-type gp3 \
  --encrypted \
  --kms-key-id "arn:aws:kms:ap-northeast-2:123456789:key/mrk-xxx"

# 계정 기본값으로 EBS 암호화 활성화 (신규 볼륨 모두 암호화)
aws ec2 enable-ebs-encryption-by-default --region ap-northeast-2

# 기존 미암호화 볼륨 → 암호화 볼륨으로 마이그레이션
# 1. 스냅샷 생성
SNAPSHOT_ID=$(aws ec2 create-snapshot \
  --volume-id vol-xxx \
  --description "pre-encryption snapshot" \
  --query SnapshotId --output text)

# 2. 암호화된 스냅샷 복사
aws ec2 copy-snapshot \
  --source-snapshot-id "$SNAPSHOT_ID" \
  --source-region ap-northeast-2 \
  --encrypted \
  --kms-key-id alias/aws/ebs \
  --destination-region ap-northeast-2

# 3. 암호화된 스냅샷으로 새 볼륨 생성 후 교체
```

### S3 서버 측 암호화 (SSE)

S3는 세 가지 SSE 방식을 제공한다. SSE-S3는 AWS가 키를 완전히 관리한다. SSE-KMS는 AWS KMS를 통해 키 사용 감사 로그가 남아 규정 준수에 유리하다. SSE-C는 고객이 키를 직접 제공하므로 AWS에 키가 저장되지 않는다.

```bash
# ── 버킷 기본 암호화 설정 (SSE-KMS) ──
aws s3api put-bucket-encryption \
  --bucket my-secure-bucket \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "aws:kms",
        "KMSMasterKeyID": "arn:aws:kms:ap-northeast-2:123456789:key/mrk-xxx"
      },
      "BucketKeyEnabled": true
    }]
  }'

# 객체 업로드 시 암호화 명시 (버킷 기본값 재정의)
aws s3 cp secret.txt s3://my-secure-bucket/ \
  --sse aws:kms \
  --sse-kms-key-id alias/my-key

# 암호화 상태 확인
aws s3api head-object \
  --bucket my-secure-bucket \
  --key secret.txt \
  --query '{SSE:ServerSideEncryption,SSEKMSKeyId:SSEKMSKeyId}'

# ── 버킷 정책: 암호화되지 않은 객체 업로드 거부 ──
aws s3api put-bucket-policy \
  --bucket my-secure-bucket \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::my-secure-bucket/*",
      "Condition": {
        "StringNotEquals": {
          "s3:x-amz-server-side-encryption": "aws:kms"
        }
      }
    }]
  }'
```

### DB 투명 데이터 암호화 (TDE)

RDS는 인스턴스 생성 시 `--storage-encrypted` 플래그로 KMS 기반 TDE를 활성화한다. TDE는 DB 엔진이 디스크에 쓸 때 자동으로 암호화하고, 읽을 때 복호화한다. 애플리케이션 코드 변경 없이 저장소 수준에서 보호가 이루어지는 것이 장점이다.

```bash
aws rds create-db-instance \
  --db-instance-identifier prod-postgres \
  --db-instance-class db.t3.medium \
  --engine postgres \
  --engine-version 16.1 \
  --master-username dbadmin \
  --master-user-password "$(aws secretsmanager get-secret-value \
    --secret-id prod/rds/master-password --query SecretString --output text)" \
  --storage-encrypted \
  --kms-key-id "arn:aws:kms:ap-northeast-2:123456789:key/mrk-xxx" \
  --allocated-storage 100 \
  --backup-retention-period 7
```

---

## 7. Bad vs Good: 시크릿 관리 패턴

```python
# ── Bad: 환경변수에 평문 시크릿 ──
import os

DB_PASSWORD = os.environ.get("DB_PASSWORD")  # 컨테이너 환경변수로 주입
# 문제: 'docker inspect'로 환경변수 노출, CI/CD 로그에 출력될 수 있음
# 문제: 로테이션 시 앱 재시작 필요, 감사 로그 없음

# ── Good: 런타임에 Secrets Manager에서 조회 ──
import boto3
import json
from functools import lru_cache

@lru_cache(maxsize=None)
def get_db_credentials() -> dict:
    """
    시크릿은 프로세스 시작 시 한 번만 가져온다.
    로테이션 주기(30일)보다 배포 주기가 짧다면 이 패턴으로 충분하다.
    더 짧은 TTL이 필요하다면 캐시 만료 시간을 추가한다.
    """
    client = boto3.client("secretsmanager", region_name="ap-northeast-2")
    response = client.get_secret_value(SecretId="prod/myapp/db")
    return json.loads(response["SecretString"])

# 사용 측에서는 경로(키)만 알면 된다
creds = get_db_credentials()
conn = psycopg2.connect(
    host=os.environ["DB_HOST"],   # 비밀이 아닌 설정값은 환경변수로
    database="mydb",
    user=creds["username"],
    password=creds["password"],
)
```

---

## 8. 핵심 요약

보안은 통신과 저장소 두 영역에서 각각 다른 기법으로 접근한다. 통신 보안의 핵심은 TLS이며, TLS는 비대칭 암호화로 키를 교환하고 대칭 암호화로 본문을 보호하는 하이브리드 방식이다. 저장소 보안은 암호화 키 관리가 핵심이다. 애플리케이션이 키를 직접 보관하면 코드 유출과 키 유출이 동시에 발생하므로, KMS나 Vault 같은 전용 시스템에 키 관리를 위임하는 것이 원칙이다. 시크릿 관리는 이 두 영역을 연결하는 운영 레이어다. 코드에서 시크릿을 완전히 분리하고, 로테이션을 자동화하며, 접근 감사 로그를 남기는 체계가 갖춰졌을 때 비로소 방어 깊이(defense in depth)가 실현된다.

| 영역 | 기술 | 핵심 원칙 |
|---|---|---|
| 통신 암호화 | TLS 1.3, HSTS | PFS 암호 스위트 강제 |
| 인증서 관리 | Let's Encrypt + certbot | 90일 자동 갱신 |
| 시크릿 관리 | Secrets Manager, Vault | 코드에서 시크릿 완전 분리 |
| 저장소 암호화 | EBS/S3 SSE, RDS TDE | KMS로 키 관리 위임 |

---

## 9. 참고 자료

- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/) — Nginx/Apache/HAProxy 보안 TLS 설정 자동 생성
- [Let's Encrypt 문서](https://letsencrypt.org/docs/) — certbot 옵션 및 챌린지 방식 상세
- [AWS Secrets Manager 개발자 가이드](https://docs.aws.amazon.com/secretsmanager/)
- [HashiCorp Vault 공식 튜토리얼](https://developer.hashicorp.com/vault/tutorials)
- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)

---

**다음 챕터**: Ch09 — 모니터링과 관측성 (Prometheus, Grafana, 로그 집계)
