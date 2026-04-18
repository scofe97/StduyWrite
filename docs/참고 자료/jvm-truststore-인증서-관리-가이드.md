# JVM Truststore 인증서 관리 가이드

## 개요

JVM은 HTTPS 통신 시 상대방 인증서를 **truststore**에서 검증한다. 공인 CA(DigiCert, Let's Encrypt 등)가 발급한 인증서는 JVM에 기본 포함되어 있어서 별도 작업이 필요 없다. 하지만 사내 자체 서명 인증서나 사설 CA 인증서는 truststore에 직접 등록해야 한다.

Jenkins 파이프라인에서 사내 서비스(GitLab, Nexus, Harbor, SonarQube 등)를 HTTPS로 호출할 때 `PKIX path building failed` 에러가 나면 이 작업이 필요하다.

---

## Truststore 기본 개념

### Truststore vs Keystore

| 구분 | Truststore | Keystore |
|------|-----------|----------|
| 용도 | **상대방**을 신뢰할지 판단 | **내 신원**을 증명 |
| 내용 | CA 인증서, 서버 공개 인증서 | 내 개인 키 + 인증서 |
| Jenkins에서 | 파이프라인이 호출하는 서비스의 인증서 | Jenkins 자체 SSL (직접 SSL 방식일 때) |

### 기본 truststore 위치

```bash
# 위치 확인
echo $JAVA_HOME/lib/security/cacerts

# 일반적인 경로들
/usr/lib/jvm/java-17-openjdk/lib/security/cacerts      # OpenJDK 17
/usr/lib/jvm/java-11-openjdk/lib/security/cacerts      # OpenJDK 11
/usr/java/latest/lib/security/cacerts                   # Oracle JDK

# Jenkins가 사용하는 Java 확인
ps aux | grep jenkins | grep -o 'java.home=[^ ]*'
# 또는
sudo cat /etc/default/jenkins | grep JAVA_HOME
```

기본 비밀번호는 `changeit`이다.

---

## 인증서 등록 절차

### 1단계: 대상 서비스의 인증서 가져오기

```bash
# 서비스에서 직접 추출
openssl s_client -connect gitlab.internal:443 </dev/null 2>/dev/null \
  | openssl x509 -out gitlab.crt

# 인증서 내용 확인 (발급자, 유효기간 등)
openssl x509 -in gitlab.crt -noout -subject -issuer -dates
```

체인 인증서(중간 CA 포함)가 필요한 경우:
```bash
# 전체 체인 추출
openssl s_client -showcerts -connect gitlab.internal:443 </dev/null 2>/dev/null \
  | awk '/BEGIN CERTIFICATE/,/END CERTIFICATE/{ print }' > gitlab-chain.crt
```

### 2단계: Truststore에 등록

```bash
# 등록 (alias는 서비스 식별용, 중복 불가)
sudo keytool -importcert \
  -alias gitlab-internal \
  -file gitlab.crt \
  -keystore $JAVA_HOME/lib/security/cacerts \
  -storepass changeit \
  -noprompt
```

여러 서비스가 있으면 alias만 바꿔서 반복한다:
```bash
sudo keytool -importcert -alias nexus-internal  -file nexus.crt  -keystore $JAVA_HOME/lib/security/cacerts -storepass changeit -noprompt
sudo keytool -importcert -alias harbor-internal -file harbor.crt -keystore $JAVA_HOME/lib/security/cacerts -storepass changeit -noprompt
sudo keytool -importcert -alias sonar-internal  -file sonar.crt  -keystore $JAVA_HOME/lib/security/cacerts -storepass changeit -noprompt
```

### 3단계: Jenkins 재시작

```bash
sudo systemctl restart jenkins
```

truststore는 JVM 시작 시 로드되므로 재시작이 필수다.

---

## 등록 확인 및 관리

### 등록된 인증서 조회

```bash
# 특정 alias 검색
keytool -list -keystore $JAVA_HOME/lib/security/cacerts \
  -storepass changeit | grep gitlab

# 특정 alias 상세 정보
keytool -list -v -keystore $JAVA_HOME/lib/security/cacerts \
  -storepass changeit -alias gitlab-internal
```

### 인증서 삭제

```bash
sudo keytool -delete -alias gitlab-internal \
  -keystore $JAVA_HOME/lib/security/cacerts \
  -storepass changeit
```

### 인증서 갱신 (만료 시)

기존 인증서를 삭제하고 새 인증서를 같은 alias로 등록한다:
```bash
# 삭제 → 재등록 → 재시작
sudo keytool -delete -alias gitlab-internal \
  -keystore $JAVA_HOME/lib/security/cacerts -storepass changeit

sudo keytool -importcert -alias gitlab-internal \
  -file gitlab-new.crt \
  -keystore $JAVA_HOME/lib/security/cacerts -storepass changeit -noprompt

sudo systemctl restart jenkins
```

---

## 별도 Truststore 사용 (기본 cacerts를 수정하고 싶지 않을 때)

Java 업그레이드 시 기본 `cacerts`가 덮어씌워질 수 있다. 이를 방지하려면 별도 truststore를 만들어 Jenkins에 지정한다.

### 별도 truststore 생성

```bash
# 기본 cacerts 복사
sudo cp $JAVA_HOME/lib/security/cacerts /opt/jenkins/truststore.jks

# 사내 인증서 추가
sudo keytool -importcert -alias gitlab-internal \
  -file gitlab.crt \
  -keystore /opt/jenkins/truststore.jks \
  -storepass changeit -noprompt
```

### Jenkins에 지정

```bash
# /etc/default/jenkins (Ubuntu) 또는 /etc/sysconfig/jenkins (CentOS)
JAVA_ARGS="-Djavax.net.ssl.trustStore=/opt/jenkins/truststore.jks -Djavax.net.ssl.trustStorePassword=changeit"
```

```bash
sudo systemctl restart jenkins
```

이 방식이면 Java 업그레이드와 무관하게 사내 인증서가 유지된다.

---

## 흔한 에러와 해결

### PKIX path building failed

```
sun.security.provider.certpath.SunCertPathBuilderException:
unable to find valid certification path to requested target
```

대상 서비스의 인증서가 truststore에 없다는 뜻이다. 위 등록 절차를 따르면 해결된다.

### Certificate already exists in keystore

```bash
# 같은 alias가 이미 있음 → 삭제 후 재등록
sudo keytool -delete -alias gitlab-internal \
  -keystore $JAVA_HOME/lib/security/cacerts -storepass changeit
# 그리고 다시 importcert
```

### Pipeline의 sh 단계에서 curl 인증서 에러

`sh 'curl https://internal-service/api'`는 **JVM truststore가 아니라 OS 인증서 저장소**를 사용한다. JVM과 별개로 OS에도 등록이 필요하다:

```bash
# Ubuntu/Debian
sudo cp gitlab.crt /usr/local/share/ca-certificates/gitlab-internal.crt
sudo update-ca-certificates

# CentOS/RHEL
sudo cp gitlab.crt /etc/pki/ca-trust/source/anchors/gitlab-internal.crt
sudo update-ca-trust
```

이 차이가 중요하다:

| 호출 방식 | 인증서 저장소 |
|-----------|-------------|
| Jenkins 플러그인 (`httpRequest`, `git` 등) | JVM Truststore |
| `sh 'curl ...'`, `sh 'git clone ...'` | OS 인증서 저장소 |

양쪽에서 사내 서비스를 호출한다면 **JVM truststore + OS 인증서 저장소 둘 다** 등록해야 한다.

---

## 만료 모니터링

인증서가 만료되면 파이프라인이 갑자기 실패한다. 주기적으로 확인하는 스크립트를 cron에 등록하면 좋다.

```bash
#!/bin/bash
# /opt/jenkins/check-certs.sh

TRUSTSTORE="$JAVA_HOME/lib/security/cacerts"
STOREPASS="changeit"
WARN_DAYS=30

keytool -list -v -keystore "$TRUSTSTORE" -storepass "$STOREPASS" 2>/dev/null \
  | grep -A2 "Alias name:" \
  | while read line; do
      if echo "$line" | grep -q "Valid from:"; then
        until_date=$(echo "$line" | grep -oP 'until: \K.*')
        expire=$(date -d "$until_date" +%s 2>/dev/null)
        now=$(date +%s)
        days_left=$(( (expire - now) / 86400 ))
        if [ "$days_left" -lt "$WARN_DAYS" ]; then
          echo "WARNING: Certificate expires in $days_left days ($until_date)"
        fi
      fi
    done
```

```bash
# 매주 월요일 확인
echo "0 9 * * 1 /opt/jenkins/check-certs.sh | mail -s 'Jenkins Cert Check' admin@example.com" \
  | sudo crontab -
```
