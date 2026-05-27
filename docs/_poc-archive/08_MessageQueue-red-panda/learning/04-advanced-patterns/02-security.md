# 02. Security

TLS 암호화, SASL 인증, ACL 권한 관리 — 환경별(Docker Compose / VM / K8s) 실전 적용 가이드

---

## 보안 계층

```
┌─────────────────────────────────────────┐
│           Application Layer              │
│  ┌─────────────────────────────────┐    │
│  │           ACL (권한)             │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │        SASL (인증)               │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │        TLS (암호화)              │    │
│  └─────────────────────────────────┘    │
│           Transport Layer               │
└─────────────────────────────────────────┘
```

---

## Redpanda 통신 경로와 TLS 적용 지점

Redpanda는 5개의 독립적인 리스너를 가지며, 각각에 TLS를 개별 설정할 수 있다. 어떤 경로에 TLS를 적용할지는 네트워크 경계와 데이터 민감도에 따라 결정한다.

| 리스너 | 기본 포트 | 용도 | TLS 필요성 |
|--------|----------|------|-----------|
| Kafka API | 9092 | 클라이언트 ↔ 브로커 (produce/consume) | **필수** — 비즈니스 데이터가 흐른다 |
| RPC (내부) | 33145 | 브로커 ↔ 브로커 (파티션 복제, Raft) | 프로덕션 필수, 로컬 선택 |
| Schema Registry | 8081 | 클라이언트 ↔ 스키마 레지스트리 | Kafka API와 동일 수준 권장 |
| Pandaproxy (REST) | 8082 | HTTP 클라이언트 ↔ 브로커 | 외부 노출 시 필수 |
| Admin API | 9644 | 관리 도구 ↔ 브로커 (설정, 모니터링) | 내부망이면 선택, 외부 노출 시 필수 |

### TLS 적용 판단 기준

1. **네트워크 경계를 넘는가?** — 컨테이너 내부 통신이면 TLS 없이도 괜찮다. 호스트 네트워크를 타거나 외부에 노출되면 TLS가 필요하다.
2. **민감 데이터가 흐르는가?** — PII, 결제 정보 등이 포함된 토픽이라면 로컬 개발에서도 TLS를 켜서 설정 검증을 하는 편이 안전하다.
3. **규제 요구사항이 있는가?** — PCI-DSS, HIPAA 등은 전송 암호화를 의무화한다.

로컬 개발에서는 Kafka API(9092)만 TLS를 켜도 충분하다. 프로덕션에서는 모든 리스너에 TLS를 적용하는 것이 표준이다.

---

## Docker Compose 환경 TLS 설정

### 자체 서명 인증서 생성

프로덕션에서는 사내 CA나 Let's Encrypt를 쓰지만, 로컬 개발에서는 자체 서명 인증서로 충분하다. 핵심은 CA → 서버 인증서 → 클라이언트 truststore 순서를 지키는 것이다.

```bash
#!/bin/bash
# generate-certs.sh — 로컬 개발용 자체 서명 인증서 생성

CERT_DIR="./certs"
PASSWORD="redpanda"  # 로컬 개발용, 프로덕션에서는 시크릿 관리 도구 사용

mkdir -p ${CERT_DIR}

# 1. CA 키 + 인증서 생성
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 \
  -keyout ${CERT_DIR}/ca.key \
  -out ${CERT_DIR}/ca.crt \
  -subj "/CN=Redpanda-CA/O=Local-Dev"

# 2. 서버 키 생성
openssl genrsa -out ${CERT_DIR}/broker.key 2048

# 3. CSR(인증서 서명 요청) 생성 — SAN 포함이 핵심
#    Docker 내부 DNS(redpanda, redpanda-0 등)와 localhost를 모두 포함해야 한다
cat > ${CERT_DIR}/broker.cnf <<EOF
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
CN = redpanda

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = redpanda
DNS.2 = redpanda-0
DNS.3 = localhost
IP.1 = 127.0.0.1
EOF

openssl req -new \
  -key ${CERT_DIR}/broker.key \
  -out ${CERT_DIR}/broker.csr \
  -config ${CERT_DIR}/broker.cnf

# 4. CA로 서버 인증서 서명
openssl x509 -req -days 365 \
  -in ${CERT_DIR}/broker.csr \
  -CA ${CERT_DIR}/ca.crt \
  -CAkey ${CERT_DIR}/ca.key \
  -CAcreateserial \
  -out ${CERT_DIR}/broker.crt \
  -extensions v3_req \
  -extfile ${CERT_DIR}/broker.cnf

echo "인증서 생성 완료: ${CERT_DIR}/"
echo "  ca.crt       — CA 인증서 (클라이언트 truststore에 추가)"
echo "  broker.key   — 서버 비공개 키"
echo "  broker.crt   — 서버 인증서"
```

**SAN(Subject Alternative Name)이 없으면 실패한다.** 최신 Go/Java TLS 클라이언트는 CN만으로는 호스트명 검증을 하지 않는다. `DNS.1`, `IP.1` 등으로 실제 접속 주소를 모두 포함해야 한다.

### docker-compose.yml TLS 설정

```yaml
# docker-compose-tls.yml — TLS 활성화 예시
version: "3.8"
services:
  redpanda:
    image: redpandadata/redpanda:v24.3.1
    command:
      - redpanda start
      - --smp 1
      - --memory 1G
      - --overprovisioned
      # Kafka API — TLS
      - --kafka-addr internal://0.0.0.0:9092,external://0.0.0.0:19092
      - --advertise-kafka-addr internal://redpanda:9092,external://localhost:19092
      # RPC — 로컬에서는 평문 유지
      - --rpc-addr redpanda:33145
      - --advertise-rpc-addr redpanda:33145
    volumes:
      - ./certs:/etc/redpanda/certs:ro
      - ./redpanda-tls.yaml:/etc/redpanda/.bootstrap.yaml:ro
    ports:
      - "19092:19092"  # external Kafka (TLS)
      - "18081:18081"  # external Schema Registry (TLS)
      - "18082:18082"  # external Pandaproxy (TLS)
      - "9644:9644"    # Admin API

  console:
    image: redpandadata/console:v2.7.2
    environment:
      KAFKA_BROKERS: redpanda:9092
      KAFKA_TLS_ENABLED: "true"
      KAFKA_TLS_CAFILEPATH: /etc/redpanda/certs/ca.crt
      # mTLS가 아니면 클라이언트 cert/key는 불필요
      SCHEMAREGISTRY_URLS: "https://redpanda:18081"
      SCHEMAREGISTRY_TLS_ENABLED: "true"
      SCHEMAREGISTRY_TLS_CAFILEPATH: /etc/redpanda/certs/ca.crt
    volumes:
      - ./certs:/etc/redpanda/certs:ro
    ports:
      - "8080:8080"
    depends_on:
      - redpanda
```

### Redpanda 노드 설정 (bootstrap.yaml)

```yaml
# redpanda-tls.yaml — Redpanda 노드 TLS 설정
redpanda:
  kafka_api_tls:
    - name: internal
      enabled: true
      cert_file: /etc/redpanda/certs/broker.crt
      key_file: /etc/redpanda/certs/broker.key
      truststore_file: /etc/redpanda/certs/ca.crt
    - name: external
      enabled: true
      cert_file: /etc/redpanda/certs/broker.crt
      key_file: /etc/redpanda/certs/broker.key
      truststore_file: /etc/redpanda/certs/ca.crt

schema_registry:
  schema_registry_api_tls:
    enabled: true
    cert_file: /etc/redpanda/certs/broker.crt
    key_file: /etc/redpanda/certs/broker.key
    truststore_file: /etc/redpanda/certs/ca.crt

pandaproxy:
  pandaproxy_api_tls:
    enabled: true
    cert_file: /etc/redpanda/certs/broker.crt
    key_file: /etc/redpanda/certs/broker.key
    truststore_file: /etc/redpanda/certs/ca.crt
```

### TLS on/off 프로파일 분리 전략

로컬 개발에서 TLS를 항상 켜면 인증서 갱신, 디버깅 등이 번거롭다. Docker Compose profiles로 분리하면 필요할 때만 TLS를 활성화할 수 있다.

```yaml
# docker-compose.yml (기본: 평문)
services:
  redpanda:
    profiles: ["default", "plain"]
    # ... 기존 평문 설정

  redpanda-tls:
    profiles: ["tls"]
    # ... TLS 설정 (위 예시)
```

```bash
# 평문 모드 (기본)
docker compose up -d

# TLS 모드
docker compose --profile tls up -d
```

실전에서는 `Makefile` 타겟으로 감싸면 더 편하다:

```makefile
up:           ## 평문 모드
	docker compose up -d

up-tls:       ## TLS 모드
	./generate-certs.sh
	docker compose --profile tls up -d
```

---

## TLS 설정 (K8s / Helm)

### Helm values.yaml

```yaml
tls:
  enabled: true
  certs:
    default:
      caEnabled: true
      # cert-manager 사용
      issuerRef:
        name: selfsigned-issuer
        kind: Issuer
      # 또는 기존 Secret 사용
      # secretRef:
      #   name: redpanda-tls

listeners:
  kafka:
    port: 9092
    tls:
      enabled: true
      cert: default
  admin:
    port: 9644
    tls:
      enabled: true
      cert: default
  schemaRegistry:
    port: 8081
    tls:
      enabled: true
      cert: default
```

### cert-manager Issuer

```yaml
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: selfsigned-issuer
  namespace: redpanda
spec:
  selfSigned: {}
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: redpanda-tls
  namespace: redpanda
spec:
  secretName: redpanda-tls
  issuerRef:
    name: selfsigned-issuer
    kind: Issuer
  commonName: redpanda
  dnsNames:
    - redpanda
    - redpanda.redpanda.svc
    - "*.redpanda.redpanda.svc.cluster.local"
```

cert-manager 기초 개념(Issuer/ClusterIssuer 차이, ACME 챌린지 등)은 TPS SSL 분석 문서를 참고한다.

> **교차 참조**: `specs/projects/tps/` — 02-support-tool-analysis.md 8.6 (cert-manager 개요)

---

## Spring Boot 클라이언트 SSL 연결

### truststore 생성

Java 클라이언트는 CA 인증서를 PEM 파일로 직접 읽지 못한다. JKS 또는 PKCS12 형식의 truststore로 변환해야 한다. PKCS12가 Java 9+ 기본 형식이므로 새 프로젝트에서는 `.p12`를 권장한다.

```bash
# CA 인증서 → truststore.p12 변환
keytool -import -trustcacerts \
  -alias redpanda-ca \
  -file certs/ca.crt \
  -keystore certs/truststore.p12 \
  -storetype PKCS12 \
  -storepass changeit \
  -noprompt

# 확인
keytool -list -keystore certs/truststore.p12 -storetype PKCS12 -storepass changeit
```

JKS가 필요한 경우(레거시 프로젝트):

```bash
keytool -import -trustcacerts \
  -alias redpanda-ca \
  -file certs/ca.crt \
  -keystore certs/truststore.jks \
  -storepass changeit \
  -noprompt
```

### application.yml 프로파일별 설정

```yaml
# application.yml — 공통
spring:
  kafka:
    bootstrap-servers: ${KAFKA_BOOTSTRAP_SERVERS:localhost:9092}

---
# application-local.yml — 평문 (기본)
spring:
  config:
    activate:
      on-profile: local
  kafka:
    bootstrap-servers: localhost:9092

---
# application-local-tls.yml — 로컬 TLS
spring:
  config:
    activate:
      on-profile: local-tls
  kafka:
    bootstrap-servers: localhost:19092
    properties:
      security.protocol: SSL
      ssl.truststore.location: ${SSL_TRUSTSTORE_LOCATION:classpath:certs/truststore.p12}
      ssl.truststore.password: ${SSL_TRUSTSTORE_PASSWORD:changeit}
      ssl.truststore.type: PKCS12
      # 자체 서명 인증서: 호스트명 검증 비활성화
      ssl.endpoint.identification.algorithm: ""

---
# application-k8s.yml — K8s 프로덕션
spring:
  config:
    activate:
      on-profile: k8s
  kafka:
    bootstrap-servers: redpanda.redpanda.svc.cluster.local:9092
    properties:
      security.protocol: SASL_SSL
      sasl.mechanism: SCRAM-SHA-512
      sasl.jaas.config: >
        org.apache.kafka.common.security.scram.ScramLoginModule required
        username="${KAFKA_USERNAME}"
        password="${KAFKA_PASSWORD}";
      ssl.truststore.location: /etc/ssl/certs/truststore.p12
      ssl.truststore.password: ${SSL_TRUSTSTORE_PASSWORD}
      ssl.truststore.type: PKCS12
```

### Schema Registry SSL 연결

Schema Registry도 TLS를 활성화했다면 클라이언트 측 SSL 설정이 필요하다. Spring Kafka의 `schema.registry.url`은 `https://`로 바꾸는 것만으로 끝나지 않는다.

```yaml
# application-local-tls.yml 추가
spring:
  kafka:
    properties:
      # Schema Registry SSL
      schema.registry.url: https://localhost:18081
      schema.registry.ssl.truststore.location: ${SSL_TRUSTSTORE_LOCATION}
      schema.registry.ssl.truststore.password: ${SSL_TRUSTSTORE_PASSWORD}
      schema.registry.ssl.truststore.type: PKCS12
```

**주의**: `spring.kafka.properties`의 `schema.registry.*` 프로퍼티는 Confluent의 `KafkaAvroSerializer`/`KafkaAvroDeserializer`가 읽는 것이다. Spring Boot의 auto-configuration이 자동으로 전달하지 않으므로, Serializer 설정에 명시적으로 포함해야 한다.

```java
// SchemaRegistryConfig.java — SSL 프로퍼티를 Serializer에 전달
@Bean
public Map<String, Object> avroSerializerConfig(KafkaProperties kafkaProperties) {
    Map<String, Object> props = new HashMap<>(kafkaProperties.buildProducerProperties(null));
    // spring.kafka.properties.schema.registry.* 가 이미 포함됨
    return props;
}
```

### Testcontainers에서 TLS 테스트

Testcontainers의 `RedpandaContainer`는 TLS를 기본 지원하지 않는다. 테스트에서 TLS를 검증하려면 두 가지 접근이 있다:

1. **통합 테스트에서 TLS 스킵** (권장) — TLS는 인프라 설정이지 비즈니스 로직이 아니다. 단위/통합 테스트는 평문으로 실행하고, TLS 검증은 스테이징 환경의 E2E 테스트에서 한다.

2. **Docker Compose 기반 테스트** — `@ActiveProfiles("local-tls")` + docker-compose-tls.yml을 띄워서 테스트. 기존 프로젝트의 `@ActiveProfiles("local")` 패턴과 동일한 방식이다.

```java
// 기존 패턴과 동일 — 프로파일만 변경
@SpringBootTest
@ActiveProfiles("local-tls")
class SslIntegrationTest {
    // docker-compose-tls.yml이 떠 있어야 함
}
```

---

## Go (franz-go) 클라이언트 SSL 연결

### tls.Config 기본 설정

franz-go는 Go 표준 `crypto/tls` 패키지를 그대로 사용한다. Java처럼 truststore 변환이 불필요하고, PEM 파일을 직접 로딩한다.

```go
package kafka

import (
	"crypto/tls"
	"crypto/x509"
	"fmt"
	"os"

	"github.com/twmb/franz-go/pkg/kgo"
)

// NewTLSClient는 TLS가 활성화된 Kafka 클라이언트를 생성한다.
// caPath는 CA 인증서(PEM) 경로다.
func NewTLSClient(brokers []string, caPath string) (*kgo.Client, error) {
	tlsCfg, err := newTLSConfig(caPath)
	if err != nil {
		return nil, fmt.Errorf("TLS 설정 실패: %w", err)
	}

	return kgo.NewClient(
		kgo.SeedBrokers(brokers...),
		kgo.DialTLSConfig(tlsCfg),
	)
}

func newTLSConfig(caPath string) (*tls.Config, error) {
	caCert, err := os.ReadFile(caPath)
	if err != nil {
		return nil, fmt.Errorf("CA 인증서 읽기 실패: %w", err)
	}

	caCertPool := x509.NewCertPool()
	if !caCertPool.AppendCertsFromPEM(caCert) {
		return nil, fmt.Errorf("CA 인증서 파싱 실패 — PEM 형식인지 확인")
	}

	return &tls.Config{
		RootCAs:    caCertPool,
		MinVersion: tls.VersionTLS12,
	}, nil
}
```

### 자체 서명 인증서 허용 (로컬 개발 전용)

프로덕션에서는 절대 사용하면 안 되지만, 로컬 개발에서 빠르게 테스트할 때는 인증서 검증을 건너뛸 수 있다.

```go
// 로컬 개발 전용 — 프로덕션 사용 금지
func newInsecureTLSConfig() *tls.Config {
	return &tls.Config{
		InsecureSkipVerify: true, //nolint:gosec // 로컬 개발 전용
		MinVersion:         tls.VersionTLS12,
	}
}
```

CA 인증서를 제대로 로딩하는 방식을 우선 사용하고, `InsecureSkipVerify`는 인증서 생성이 번거로울 때만 임시로 쓴다.

### mTLS (상호 인증) 설정

서버가 클라이언트 인증서도 요구하는 경우:

```go
func newMTLSConfig(caPath, certPath, keyPath string) (*tls.Config, error) {
	caCert, err := os.ReadFile(caPath)
	if err != nil {
		return nil, err
	}
	caCertPool := x509.NewCertPool()
	caCertPool.AppendCertsFromPEM(caCert)

	clientCert, err := tls.LoadX509KeyPair(certPath, keyPath)
	if err != nil {
		return nil, fmt.Errorf("클라이언트 인증서 로딩 실패: %w", err)
	}

	return &tls.Config{
		RootCAs:      caCertPool,
		Certificates: []tls.Certificate{clientCert},
		MinVersion:   tls.VersionTLS12,
	}, nil
}
```

### 환경변수 기반 설정 패턴

```go
type KafkaConfig struct {
	Brokers    []string
	TLSEnabled bool
	CAPath     string
	CertPath   string // mTLS용
	KeyPath    string // mTLS용
}

func NewClientFromConfig(cfg KafkaConfig) (*kgo.Client, error) {
	opts := []kgo.Opt{
		kgo.SeedBrokers(cfg.Brokers...),
	}

	if cfg.TLSEnabled {
		var tlsCfg *tls.Config
		var err error
		if cfg.CertPath != "" {
			tlsCfg, err = newMTLSConfig(cfg.CAPath, cfg.CertPath, cfg.KeyPath)
		} else {
			tlsCfg, err = newTLSConfig(cfg.CAPath)
		}
		if err != nil {
			return nil, err
		}
		opts = append(opts, kgo.DialTLSConfig(tlsCfg))
	}

	return kgo.NewClient(opts...)
}
```

---

## 환경별 TLS 전략 비교

| 항목 | Docker Compose (로컬) | VM (스테이징) | K8s (프로덕션) |
|------|----------------------|--------------|---------------|
| **CA** | 자체 서명 (openssl) | 사내 CA 또는 Let's Encrypt | cert-manager + ClusterIssuer |
| **인증서 배포** | 볼륨 마운트 | Ansible/Chef로 배포 | Secret (cert-manager 자동 갱신) |
| **갱신** | 수동 (스크립트 재실행) | cron + certbot | cert-manager 자동 |
| **TLS 범위** | Kafka API만 (선택적) | 모든 리스너 | 모든 리스너 |
| **mTLS** | 불필요 | 선택 | 권장 (Istio sidecar 또는 Redpanda 자체) |
| **서비스 메시** | N/A | N/A | Istio mTLS로 전송 계층 암호화 위임 가능 |
| **truststore** | 로컬 파일 | 시스템 CA store | Pod 마운트 Secret |

### Docker Compose (로컬 개발)

- 자체 서명 CA로 인증서를 생성하고, `volumes`로 마운트한다.
- TLS는 선택적이다. 평문 프로파일을 기본으로 두고, TLS 검증이 필요할 때만 `--profile tls`로 전환한다.
- 인증서 만료 시 스크립트를 다시 실행하면 된다 (365일이면 충분).

### VM (스테이징)

- 사내 CA가 있다면 해당 CA로 서명한 인증서를 사용한다. 없다면 Let's Encrypt + certbot.
- 인증서를 Ansible 같은 구성 관리 도구로 배포하고, `redpanda.yaml`에서 경로를 지정한다.
- certbot의 자동 갱신(`certbot renew`)과 Redpanda 재시작을 연동해야 한다. Redpanda는 인증서 파일 변경을 자동 감지하지 않으므로, 갱신 후 `rpk cluster config set` 또는 프로세스 재시작이 필요하다.

### K8s (프로덕션)

- cert-manager가 인증서 생성/갱신/Secret 관리를 자동화한다.
- Helm values.yaml의 `tls.certs.default.issuerRef`로 연결하면 Redpanda Operator가 나머지를 처리한다.
- `ClusterIssuer` + Let's Encrypt ACME를 쓸 수 있으나, 내부 서비스 간 통신에는 자체 서명 CA로 충분하다.

> **교차 참조**: cert-manager 설치, Issuer vs ClusterIssuer, ACME 챌린지 등 기초 개념은 TPS SSL 분석 문서를 참고한다. (`specs/projects/tps/` — 02-support-tool-analysis.md 8.6~8.8)

### K8s + Istio mTLS

Istio를 사용하는 클러스터에서는 서비스 메시가 제공하는 mTLS와 Redpanda 자체 TLS가 겹칠 수 있다. 두 레이어의 역할을 구분하는 것이 핵심이다.

**Istio mTLS가 해주는 것:**
- Pod 간 네트워크 트래픽을 sidecar(Envoy)가 자동 암호화한다. 애플리케이션 코드 변경 없이 전송 계층 보안을 확보할 수 있다.
- Istio CA(istiod)가 인증서를 자동 발급/갱신하므로 cert-manager 없이도 mTLS가 동작한다.
- `PeerAuthentication`으로 네임스페이스/워크로드 단위 mTLS 정책을 선언적으로 관리한다.

**Istio mTLS가 해주지 않는 것:**
- Kafka 프로토콜 수준의 인증(SASL)은 Istio 범위 밖이다. "누가 이 토픽에 접근할 수 있는가?"는 여전히 Redpanda ACL이 담당한다.
- Redpanda 브로커 간 RPC(33145)는 Raft 프로토콜을 사용하므로, Istio sidecar를 거치면 성능 이슈가 발생할 수 있다.

#### 구성 전략: Istio + Redpanda TLS 조합

| 전략 | Istio mTLS | Redpanda TLS | 적합한 상황 |
|------|-----------|-------------|------------|
| **A. Istio만** | STRICT | 비활성 | 단순한 구성, Kafka 클라이언트가 모두 같은 메시 안에 있을 때 |
| **B. Redpanda만** | DISABLE/PERMISSIVE | 활성 | Istio 없는 클러스터, 또는 메시 외부 클라이언트가 있을 때 |
| **C. 이중 적용** | STRICT | 활성 | 규제 요구(PCI-DSS 등)로 애플리케이션 레벨 암호화가 필수일 때 |

대부분의 경우 **전략 A**가 가장 단순하고 운영 부담이 적다. 메시 외부에서 Kafka에 접근하는 클라이언트가 있다면 외부 리스너에만 Redpanda TLS를 켜는 하이브리드 방식을 쓴다.

#### 전략 A 설정 예시: Istio mTLS + Redpanda 평문

```yaml
# PeerAuthentication — redpanda 네임스페이스에 STRICT mTLS 적용
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: redpanda-mtls
  namespace: redpanda
spec:
  mtls:
    mode: STRICT
```

```yaml
# Helm values.yaml — Redpanda 자체 TLS 비활성
tls:
  enabled: false

listeners:
  kafka:
    port: 9092
    # TLS 설정 없음 — Istio sidecar가 암호화 담당
    authenticationMethod: sasl  # 인증은 여전히 SASL로
```

이 구성에서 Spring Boot 클라이언트는 `security.protocol: SASL_PLAINTEXT`를 사용한다. 전송 암호화는 Istio sidecar가 투명하게 처리하므로 클라이언트 입장에서는 평문 연결처럼 보인다.

#### Redpanda StatefulSet에서 sidecar 제외 (브로커 간 RPC)

Redpanda 브로커 간 RPC 포트(33145)에 Istio sidecar가 끼면 Raft 복제 성능이 저하된다. 브로커 간 통신은 Redpanda 자체 TLS로 보호하고, sidecar는 클라이언트-facing 포트만 처리하도록 설정한다.

```yaml
# Redpanda StatefulSet Pod annotation
metadata:
  annotations:
    # RPC 포트를 sidecar에서 제외
    traffic.sidecar.istio.io/excludeInboundPorts: "33145"
    traffic.sidecar.istio.io/excludeOutboundPorts: "33145"
```

```yaml
# Helm values.yaml — RPC만 Redpanda 자체 TLS
redpanda:
  rpc_server_tls:
    enabled: true
    cert_file: /etc/redpanda/certs/broker.crt
    key_file: /etc/redpanda/certs/broker.key
    truststore_file: /etc/redpanda/certs/ca.crt
```

#### 메시 외부 클라이언트 접근 (Istio Gateway)

메시 밖의 클라이언트(외부 서비스, 모니터링 도구 등)가 Kafka에 접근해야 한다면, Istio Gateway로 TLS를 종단한다.

```yaml
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: kafka-gateway
  namespace: redpanda
spec:
  selector:
    istio: ingressgateway
  servers:
    - port:
        number: 9094
        name: kafka-tls
        protocol: TLS
      tls:
        mode: PASSTHROUGH  # Redpanda가 직접 TLS 처리
      hosts:
        - "kafka.example.com"
---
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: kafka-vs
  namespace: redpanda
spec:
  hosts:
    - "kafka.example.com"
  gateways:
    - kafka-gateway
  tls:
    - match:
        - port: 9094
          sniHosts:
            - "kafka.example.com"
      route:
        - destination:
            host: redpanda.redpanda.svc.cluster.local
            port:
              number: 9092
```

이 경우 Redpanda의 external 리스너에 TLS를 활성화하고, 클라이언트는 `kafka.example.com:9094`로 SSL 연결한다.

> **교차 참조**: Istio mTLS 아키텍처, PeerAuthentication/AuthorizationPolicy 상세 — `runners-high/poc/03_CloudNative/03-service-mesh/` Ch14(보안)

---

## SASL 인증

### 지원 메커니즘

| 메커니즘 | 설명 |
|---------|------|
| SCRAM-SHA-256 | 비밀번호 기반 (권장) |
| SCRAM-SHA-512 | 비밀번호 기반 (더 강력) |

### Helm values.yaml

```yaml
auth:
  sasl:
    enabled: true
    mechanism: SCRAM-SHA-512
    users:
      - name: admin
        password: ${ADMIN_PASSWORD}
        mechanism: SCRAM-SHA-512
      - name: producer
        password: ${PRODUCER_PASSWORD}
        mechanism: SCRAM-SHA-512
      - name: consumer
        password: ${CONSUMER_PASSWORD}
        mechanism: SCRAM-SHA-512
```

### Secret으로 비밀번호 관리

```yaml
# 외부 Secret 사용
auth:
  sasl:
    enabled: true
    secretRef: redpanda-users
```

```bash
# Secret 생성
kubectl create secret generic redpanda-users \
  --from-literal=admin=admin-password \
  --from-literal=producer=producer-password \
  --from-literal=consumer=consumer-password \
  -n redpanda
```

### 클라이언트 연결

```yaml
# application.yml
spring:
  kafka:
    properties:
      security.protocol: SASL_SSL
      sasl.mechanism: SCRAM-SHA-512
      sasl.jaas.config: >
        org.apache.kafka.common.security.scram.ScramLoginModule required
        username="${KAFKA_USERNAME}"
        password="${KAFKA_PASSWORD}";
```

---

## ACL (Access Control List)

### ACL 생성

```bash
# Producer 권한
rpk acl create \
  --allow-principal User:producer \
  --operation write \
  --topic orders

# Consumer 권한
rpk acl create \
  --allow-principal User:consumer \
  --operation read \
  --topic orders \
  --operation read \
  --group order-consumers

# 모든 토픽 읽기
rpk acl create \
  --allow-principal User:admin \
  --operation all \
  --topic '*' \
  --group '*'
```

### ACL 조회

```bash
# 전체 ACL 목록
rpk acl list

# 특정 Principal의 ACL
rpk acl list --principal User:producer

# 특정 토픽의 ACL
rpk acl list --topic orders
```

### ACL 삭제

```bash
rpk acl delete \
  --allow-principal User:producer \
  --operation write \
  --topic orders
```

### 주요 Operation

| Operation | 설명 |
|-----------|------|
| read | 읽기 (consume) |
| write | 쓰기 (produce) |
| create | 토픽 생성 |
| delete | 토픽 삭제 |
| alter | 설정 변경 |
| describe | 메타데이터 조회 |
| all | 모든 권한 |

---

## 보안 설정 예시 (프로덕션)

```yaml
# values-prod-secure.yaml
tls:
  enabled: true
  certs:
    default:
      issuerRef:
        name: letsencrypt-prod
        kind: ClusterIssuer

auth:
  sasl:
    enabled: true
    mechanism: SCRAM-SHA-512
    secretRef: redpanda-users

listeners:
  kafka:
    port: 9092
    tls:
      enabled: true
      cert: default
    authenticationMethod: sasl
  admin:
    port: 9644
    tls:
      enabled: true
      cert: default
    authenticationMethod: http_basic
  schemaRegistry:
    port: 8081
    tls:
      enabled: true
      cert: default
    authenticationMethod: http_basic
```

---

## Spring Boot 전체 설정

```yaml
spring:
  kafka:
    bootstrap-servers: redpanda:9092
    properties:
      security.protocol: SASL_SSL
      sasl.mechanism: SCRAM-SHA-512
      sasl.jaas.config: >
        org.apache.kafka.common.security.scram.ScramLoginModule required
        username="${KAFKA_USERNAME}"
        password="${KAFKA_PASSWORD}";
      ssl.truststore.location: ${SSL_TRUSTSTORE_LOCATION}
      ssl.truststore.password: ${SSL_TRUSTSTORE_PASSWORD}
      ssl.endpoint.identification.algorithm: ""  # 호스트명 검증 비활성화 (필요시)
```

---

## 트러블슈팅

### rpk 진단 명령어

TLS 문제 진단에서 `rpk`는 가장 빠른 도구다. 브로커 상태와 TLS 연결을 한 번에 확인할 수 있다.

```bash
# 1. 클러스터 헬스 체크 — TLS 미스매치가 있으면 브로커 unreachable로 표시
rpk cluster health

# 2. 브로커 설정 확인 — 현재 TLS 설정이 의도한 대로인지 검증
rpk cluster config get kafka_api_tls
rpk cluster config get schema_registry_api_tls

# 3. TLS 연결 테스트 (rpk 자체를 TLS 클라이언트로 사용)
rpk topic list \
  --tls-enabled \
  --tls-truststore certs/ca.crt \
  --brokers localhost:19092

# 4. 디버그 번들 — 로그, 설정, 메트릭을 한꺼번에 수집
rpk debug bundle --output /tmp/debug-bundle.zip
```

### 자주 발생하는 SSL 에러와 해결

| 에러 메시지 | 원인 | 해결 |
|------------|------|------|
| `SSL handshake failed` | 서버가 TLS를 기대하는데 평문으로 연결, 또는 반대 | `security.protocol`이 리스너 설정과 일치하는지 확인 |
| `certificate signed by unknown authority` | 클라이언트 truststore에 CA 인증서가 없다 | `ca.crt`를 truststore에 추가 |
| `x509: certificate is valid for X, not Y` | SAN에 접속 주소가 포함되지 않았다 | 인증서 재생성 시 `DNS.N`/`IP.N`에 실제 접속 주소 추가 |
| `PKIX path building failed` (Java) | truststore 경로가 잘못되었거나 비밀번호 불일치 | `ssl.truststore.location`, `ssl.truststore.password` 확인 |
| `tls: bad certificate` (Go) | mTLS에서 클라이언트 인증서를 제공하지 않았다 | `Certificates` 필드에 클라이언트 cert/key 추가 |
| `connection refused` on TLS port | Redpanda가 해당 리스너에 TLS를 바인딩하지 못했다 | `rpk redpanda admin config print`로 실제 리스너 확인 |

### 리스너별 TLS 미스매치 디버깅

Redpanda는 리스너마다 TLS를 독립적으로 설정한다. 가장 흔한 실수는 internal/external 리스너의 TLS 설정이 다른데, 클라이언트가 잘못된 리스너에 연결하는 경우다.

```bash
# 어떤 리스너가 어떤 포트에서 TLS를 쓰는지 확인
rpk redpanda admin config print | grep -A5 kafka_api_tls

# openssl로 TLS 핸드셰이크 직접 테스트
openssl s_client -connect localhost:19092 -CAfile certs/ca.crt < /dev/null 2>&1 | head -20

# 인증서 SAN 확인
openssl x509 -in certs/broker.crt -noout -text | grep -A5 "Subject Alternative Name"
```

### 인증서 만료 확인

```bash
# 서버 인증서 만료일 확인
openssl x509 -in certs/broker.crt -noout -dates

# 원격 서버 인증서 만료일 확인
echo | openssl s_client -connect localhost:19092 -CAfile certs/ca.crt 2>/dev/null \
  | openssl x509 -noout -dates
```

---

## 참고

- [Redpanda Security](https://docs.redpanda.com/current/manage/security/)
- [TLS Configuration](https://docs.redpanda.com/current/manage/security/encryption/)
- [SASL Authentication](https://docs.redpanda.com/current/manage/security/authentication/)
- [franz-go TLS Example](https://github.com/twmb/franz-go/tree/master/examples)
- **교차 참조**: `specs/projects/tps/` — 02-support-tool-analysis.md 8.6~8.10 (cert-manager, TLS 기초)
