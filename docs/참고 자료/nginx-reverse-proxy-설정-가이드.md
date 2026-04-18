# Nginx Reverse Proxy 설정 가이드

## 개요

Nginx를 Jenkins 앞단에 배치하여 SSL 종료(SSL Termination)를 처리하는 방법이다. 클라이언트 ↔ Nginx 구간은 HTTPS, Nginx ↔ Jenkins 구간은 HTTP로 통신한다. Jenkins가 직접 SSL을 처리하지 않으므로 JVM 부하가 줄고, 인증서 갱신도 Nginx 레벨에서 해결된다.

```
[클라이언트] ──HTTPS──▶ [Nginx :443] ──HTTP──▶ [Jenkins :8080]
```

---

## 사전 준비

### Nginx 설치

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y nginx

# CentOS/RHEL
sudo yum install -y epel-release
sudo yum install -y nginx

# 상태 확인
sudo systemctl status nginx
```

### 디렉토리 구조

```
/etc/nginx/
├── nginx.conf                  # 메인 설정
├── conf.d/
│   └── jenkins.conf            # Jenkins 전용 설정 (여기에 작성)
├── ssl/
│   ├── cert.pem                # SSL 인증서
│   └── key.pem                 # 개인 키
└── sites-enabled/              # 심볼릭 링크 (Ubuntu 기본)
```

---

## 인증서 준비

### 방법 1: Let's Encrypt (공인 인증서)

외부에서 접근 가능한 도메인이 있을 때 사용한다.

```bash
# certbot 설치
sudo apt install -y certbot

# 인증서 발급 (Nginx를 잠시 멈추고 standalone 모드)
sudo systemctl stop nginx
sudo certbot certonly --standalone -d jenkins.example.com
sudo systemctl start nginx
```

발급 경로:
- 인증서: `/etc/letsencrypt/live/jenkins.example.com/fullchain.pem`
- 개인 키: `/etc/letsencrypt/live/jenkins.example.com/privkey.pem`

자동 갱신 확인:
```bash
# certbot이 자동으로 cron/systemd timer 등록함
sudo certbot renew --dry-run
```

### 방법 2: 자체 서명 인증서 (내부망)

도메인이 없거나 내부망 전용일 때 사용한다. 브라우저에서 경고가 뜨지만 암호화 자체는 동작한다.

```bash
sudo mkdir -p /etc/nginx/ssl

# 인증서 + 키 한 번에 생성
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/key.pem \
  -out /etc/nginx/ssl/cert.pem \
  -subj "/CN=jenkins.internal"
```

### 방법 3: 사내 CA 발급 인증서

사내 PKI가 있다면 CSR을 생성하여 CA에 서명을 요청한다.

```bash
# 개인 키 생성
openssl genrsa -out /etc/nginx/ssl/key.pem 2048

# CSR 생성 (사내 CA에 제출)
openssl req -new -key /etc/nginx/ssl/key.pem \
  -out jenkins.csr \
  -subj "/CN=jenkins.example.com"

# CA에서 서명된 인증서를 받으면 /etc/nginx/ssl/cert.pem에 배치
```

---

## Nginx 설정

### 기본 설정

`/etc/nginx/conf.d/jenkins.conf`:

```nginx
# HTTP → HTTPS 리다이렉트
server {
    listen 80;
    server_name jenkins.example.com;
    return 301 https://$host$request_uri;
}

# HTTPS 서버
server {
    listen 443 ssl;
    server_name jenkins.example.com;

    # --- SSL 인증서 ---
    ssl_certificate     /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # --- SSL 보안 설정 ---
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # --- Proxy 설정 ---
    location / {
        proxy_pass http://localhost:8080;

        # Jenkins가 원본 클라이언트 정보를 알 수 있도록 헤더 전달
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;

        # WebSocket 지원 (Jenkins Agent WebSocket 모드, Blue Ocean 등)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # 타임아웃 (빌드 로그 스트리밍 등 장시간 연결)
        proxy_read_timeout 90s;
        proxy_connect_timeout 90s;
        proxy_send_timeout 90s;
    }
}
```

### 각 설정의 역할

| 설정 | 역할 |
|------|------|
| `ssl_protocols TLSv1.2 TLSv1.3` | TLS 1.0/1.1 비활성화 (보안 취약) |
| `ssl_ciphers HIGH:!aNULL:!MD5` | 약한 암호화 스위트 제외 |
| `X-Forwarded-Proto https` | Jenkins가 "나는 HTTPS 뒤에 있다"를 인지 |
| `proxy_http_version 1.1` + `Upgrade` | WebSocket 프록시 지원 |
| `proxy_read_timeout 90s` | 빌드 콘솔 로그 스트리밍 시 연결 유지 |

### 설정 검증 및 적용

```bash
# 문법 검사
sudo nginx -t

# 적용 (무중단 리로드)
sudo nginx -s reload
```

---

## Jenkins 측 설정

### Jenkins URL 변경

Nginx를 설정한 뒤 Jenkins에도 알려줘야 한다.

1. Jenkins 관리 → System → **Jenkins URL**: `https://jenkins.example.com/`
2. 저장

이걸 안 하면 빌드 알림 메일, Webhook 콜백 URL, Pipeline에서 `env.BUILD_URL` 등이 전부 `http://`로 나간다.

### Jenkins를 localhost만 리스닝하도록 제한

Nginx를 우회하여 Jenkins에 직접 접근하는 것을 막는다.

```bash
# /etc/default/jenkins (Ubuntu) 또는 /etc/sysconfig/jenkins (CentOS)
JENKINS_ARGS="--httpListenAddress=127.0.0.1"
```

이렇게 하면 `http://서버IP:8080`으로 직접 접근이 차단되고, 반드시 Nginx(443)를 통해서만 접근 가능하다.

```bash
sudo systemctl restart jenkins
```

---

## 방화벽 설정

```bash
# 80, 443만 외부 오픈
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

# 8080은 외부에서 접근 불필요 (Nginx가 localhost로 프록시)
# 이미 Jenkins가 127.0.0.1만 리스닝하므로 추가 차단 불필요
```

---

## 검증

```bash
# HTTPS 접속 확인
curl -I https://jenkins.example.com

# 인증서 정보 확인
openssl s_client -connect jenkins.example.com:443 </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -dates

# HTTP → HTTPS 리다이렉트 확인
curl -I http://jenkins.example.com
# 301 Moved Permanently → https://... 가 나와야 함

# Jenkins 직접 접근 차단 확인
curl -I http://서버IP:8080
# Connection refused 가 나와야 함
```

---

## 트러블슈팅

### "It appears that your reverse proxy setup is broken"

Jenkins 대시보드에 이 경고가 나오면 Nginx 헤더 설정이 빠진 것이다.

```nginx
# 이 4개가 모두 있는지 확인
proxy_set_header Host              $host;
proxy_set_header X-Real-IP         $remote_addr;
proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto https;
```

### 502 Bad Gateway

Jenkins가 아직 안 떴거나 포트가 다른 경우다.

```bash
# Jenkins 상태 확인
sudo systemctl status jenkins

# Jenkins가 실제로 리스닝하는 포트 확인
sudo ss -tlnp | grep java
```

### 빌드 콘솔 로그가 끊김

`proxy_read_timeout`이 너무 짧으면 장시간 빌드 중 연결이 끊긴다.

```nginx
proxy_read_timeout 300s;  # 5분으로 늘리기
```

---

## Let's Encrypt 자동 갱신 + Nginx 리로드

```bash
# /etc/letsencrypt/renewal-hooks/post/reload-nginx.sh
#!/bin/bash
nginx -s reload
```

```bash
sudo chmod +x /etc/letsencrypt/renewal-hooks/post/reload-nginx.sh
```

certbot이 갱신할 때마다 자동으로 Nginx가 새 인증서를 로드한다.
