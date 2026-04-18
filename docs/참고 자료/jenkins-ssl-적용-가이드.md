# Jenkins SSL 적용 가이드 (VM 환경)

## 개요

Jenkins VM에 SSL을 적용할 때는 **인바운드**(Jenkins로 들어오는 트래픽)와 **아웃바운드**(파이프라인에서 나가는 트래픽) 두 방향을 각각 처리해야 한다. 단일 솔루션으로 둘 다 해결되지 않는다.

```
[브라우저/Webhook]          [파이프라인 → 내부 서비스]
        │                           │
        ▼                           ▼
   ① 인바운드 SSL              ② 아웃바운드 SSL
   (Nginx Reverse Proxy)      (JVM Truststore)
        │                           │
        ▼                           ▼
     Jenkins ◄──────────────────────┘
```

---

## 접근법 선택

Jenkins에 SSL을 적용하는 방법은 2가지다.

| 기준 | Reverse Proxy (Nginx) | Jenkins 직접 SSL (JSSE) |
|------|----------------------|------------------------|
| 인증서 갱신 | certbot 자동 갱신 | keystore 수동 변환 필요 |
| SSL 처리 | Nginx가 offload | JVM이 직접 처리 |
| 복잡도 | Nginx 프로세스 추가 | 단일 프로세스 |
| 프로덕션 적합 | **권장** | 개발/테스트용 |

프로덕션 환경이라면 Reverse Proxy 방식을 쓰는 게 맞다. 인증서 갱신이 자동화되고, JVM에 SSL 부하를 주지 않기 때문이다.

---

## ① 인바운드 SSL (Nginx Reverse Proxy)

브라우저 접속, GitHub/GitLab Webhook, 외부 API 호출 등 Jenkins로 들어오는 모든 HTTP 트래픽을 HTTPS로 전환한다.

### 1단계: 인증서 준비

```bash
# Let's Encrypt (도메인이 있을 때)
sudo certbot certonly --standalone -d jenkins.example.com

# 자체 서명 (내부망/테스트)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/key.pem \
  -out /etc/nginx/ssl/cert.pem
```

### 2단계: Nginx 설정

```nginx
server {
    listen 443 ssl;
    server_name jenkins.example.com;

    ssl_certificate     /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}

# HTTP → HTTPS 리다이렉트
server {
    listen 80;
    return 301 https://$host$request_uri;
}
```

### 3단계: Jenkins URL 변경

Jenkins 관리 → System → **Jenkins URL**을 `https://jenkins.example.com/`으로 변경한다. 이걸 빠뜨리면 Jenkins가 생성하는 링크(빌드 알림, Webhook 콜백 등)가 여전히 HTTP로 나간다.

### 4단계: 재시작

```bash
sudo systemctl restart nginx
sudo systemctl restart jenkins
```

---

## ② 아웃바운드 SSL (파이프라인 → 외부 서비스)

파이프라인에서 `curl`, `git clone`, `docker push`, `httpRequest` 등으로 다른 서비스를 호출할 때의 SSL 처리다. 이건 Nginx와 무관하고, **대상 서비스의 인증서를 Jenkins가 신뢰하는지**가 핵심이다.

### 경우별 처리

| 대상 서비스 | 조치 |
|------------|------|
| 공인 인증서 (GitHub, DockerHub 등) | 아무것도 안 해도 됨 (JVM 기본 신뢰) |
| 사내 서비스 (자체 서명 인증서) | Jenkins JVM truststore에 인증서 등록 |
| HTTP만 지원하는 서비스 | 해당 서비스에 SSL을 적용해야 함 (Jenkins에서 할 수 있는 건 없음) |

### 사내 자체 서명 인증서 등록

```bash
# 1. 대상 서비스의 인증서 가져오기
openssl s_client -connect internal-service:443 </dev/null 2>/dev/null \
  | openssl x509 -out internal.crt

# 2. Jenkins JVM truststore에 추가
keytool -importcert -alias internal-service \
  -file internal.crt \
  -keystore $JAVA_HOME/lib/security/cacerts \
  -storepass changeit -noprompt

# 3. Jenkins 재시작
sudo systemctl restart jenkins
```

여러 사내 서비스가 있으면 각 서비스의 인증서를 반복해서 등록한다. alias만 다르게 지정하면 된다.

### 등록 확인

```bash
keytool -list -keystore $JAVA_HOME/lib/security/cacerts \
  -storepass changeit | grep internal-service
```

---

## Jenkins 직접 SSL (대안)

Reverse Proxy 없이 Jenkins 자체에서 SSL을 처리하는 방법이다. 테스트 환경이나 단일 서비스 구성에서 간편하다.

```bash
# keystore 생성 (자체 서명)
keytool -genkeypair -keystore jenkins.jks -alias jenkins \
  -keyalg RSA -keysize 2048 -validity 365 \
  -dname "CN=jenkins.example.com"

# Let's Encrypt 인증서를 JKS로 변환하는 경우
openssl pkcs12 -export -in cert.pem -inkey key.pem -out jenkins.p12
keytool -importkeystore -srckeystore jenkins.p12 \
  -srcstoretype PKCS12 -destkeystore jenkins.jks
```

```bash
# Jenkins 실행 옵션
java -jar jenkins.war \
  --httpsPort=8443 \
  --httpsKeyStore=/path/to/jenkins.jks \
  --httpsKeyStorePassword=changeit \
  --httpPort=-1   # HTTP 비활성화
```

systemd를 쓰는 경우 `/etc/default/jenkins`의 `JENKINS_ARGS`에 위 옵션을 추가한다.

---

## 적용 순서 요약

| 순서 | 대상 | 작업 | 비고 |
|------|------|------|------|
| 1 | Nginx | Reverse proxy + SSL 인증서 설정 | 인바운드 해결 |
| 2 | Jenkins | Jenkins URL을 `https://`로 변경 | 링크/콜백 URL 보정 |
| 3 | 대상 서비스 | 각 사내 서비스에 SSL 적용 | 서비스 담당자 작업 |
| 4 | Jenkins truststore | 자체 서명 인증서 등록 | 아웃바운드 해결 |

---

## 통신 방향별 영향 정리

| 통신 방향 | 예시 | SSL 처리 위치 |
|-----------|------|--------------|
| 외부 → Jenkins | 브라우저, Webhook | Nginx (Reverse Proxy) |
| Jenkins → 공인 서비스 | GitHub, DockerHub | 처리 불필요 (JVM 기본 신뢰) |
| Jenkins → 사내 서비스 | 내부 API, Registry | JVM Truststore에 인증서 등록 |
| Jenkins Agent → Controller | JNLP (TCP 50000) | WebSocket 모드 전환 시 443으로 통합 가능 |

파이프라인에서 외부로 나가는 통신(`sh 'curl ...'`, `git checkout` 등)은 Jenkins가 직접 발신하는 것이라 Nginx를 거치지 않는다. 따라서 인바운드와 아웃바운드는 각각 별도로 처리해야 한다.
