# Ch03. Oracle Cloud Free Tier 운영과 관리

> **핵심 요약**
> Oracle Cloud Free Tier VM의 일상 관리 포인트는 일반 VPS와 거의 동일하다. 다만 두 가지를 주의해야 한다. 첫째, OCI는 Security List(클라우드 방화벽)와 OS 내 방화벽(iptables/firewalld)이 **이중으로** 적용되므로 양쪽 모두 포트를 열어야 한다. 둘째, 7일간 유휴 상태(CPU 10% 미만 + 네트워크 미미)인 VM은 Oracle이 회수할 수 있으므로 최소한의 활동을 유지해야 한다.

---

## 학습 목표

1. OCI의 이중 방화벽 구조를 이해하고 포트를 올바르게 열 수 있다
2. 유휴 인스턴스 회수 정책을 이해하고 방지 대책을 설정할 수 있다
3. 부트 볼륨 백업을 설정할 수 있다
4. 알려진 이슈와 대응 방법을 파악한다

---

## 1. 이중 방화벽 관리

OCI에서 VM에 트래픽이 도달하려면 **두 단계**의 방화벽을 모두 통과해야 한다. GCP나 AWS에서는 클라우드 방화벽만 설정하면 되지만, OCI Ubuntu 이미지는 OS 내부에 iptables 규칙이 기본 활성화되어 있다.

```mermaid
graph LR
    A[인터넷] --> B[OCI Security List<br/>클라우드 방화벽]
    B --> C[OS iptables/firewalld<br/>OS 방화벽]
    C --> D[애플리케이션]

    style B fill:#e8f4fd,color:#333
    style C fill:#fff3cd,color:#333
```

### 1.1 OCI Security List (클라우드 레벨)

Terraform의 `oci_core_security_list`에서 또는 OCI Console > Networking > VCN > Security Lists에서 관리한다. Ch02에서 이미 SSH(22), HTTP(80), HTTPS(443)를 열었다.

추가 포트가 필요하면 ingress rule을 추가한다.

```hcl
# 예: 8080 포트 추가
ingress_security_rules {
  protocol = "6"
  source   = "0.0.0.0/0"
  tcp_options {
    min = 8080
    max = 8080
  }
}
```

### 1.2 OS 방화벽 (Ubuntu)

Ubuntu 이미지는 iptables 규칙이 기본으로 설정되어 있어 Security List를 열어도 트래픽이 차단될 수 있다. 두 가지 방법으로 해결한다.

**방법 1: iptables 규칙 추가 (권장)**

```bash
# 특정 포트 열기
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8080 -j ACCEPT

# 규칙 저장 (재부팅 후에도 유지)
sudo netfilter-persistent save
```

**방법 2: iptables 기본 정책 변경 (간편하지만 보안 약화)**

```bash
# 모든 INPUT 허용 — Security List에서만 제어
sudo iptables -P INPUT ACCEPT
sudo iptables -F  # 기존 규칙 초기화
sudo netfilter-persistent save
```

방법 2는 OCI Security List만으로 방화벽을 제어하겠다는 의미다. 관리가 단순해지지만, Security List 설정 실수 시 VM이 완전히 노출될 수 있으므로 주의해야 한다.

### 1.3 Oracle Linux의 경우

Oracle Linux는 firewalld를 사용한다.

```bash
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --reload
```

---

## 2. 유휴 인스턴스 회수 방지

### 2.1 회수 조건

Oracle은 Always Free VM이 **7일 연속** 아래 조건을 모두 충족하면 유휴로 판단하고 회수(중지)할 수 있다.

- CPU 사용률 10% 미만
- 네트워크 트래픽 미미
- 메모리 사용률 10% 미만 (블록 볼륨 연결 인스턴스 제외)

회수된 VM은 삭제되는 것이 아니라 **중지(stopped)** 상태가 된다. 콘솔에서 재시작하면 되지만, 타이밍에 따라 capacity 부족으로 재시작이 안 될 수도 있다.

### 2.2 방지 대책

실제 서비스를 운영 중이라면 자연스럽게 CPU/네트워크 사용이 발생하므로 문제 없다. 테스트 용도로 가끔만 사용하는 VM이라면 cron으로 최소한의 활동을 유지한다.

```bash
# crontab -e 로 추가
# 매 6시간마다 CPU 살짝 사용 (수 초 소요)
0 */6 * * * dd if=/dev/urandom bs=1M count=10 | md5sum > /dev/null 2>&1
```

Docker Compose로 서비스를 운영하거나 CI/CD 작업이 주기적으로 돌아가는 서버라면 별도 조치가 필요 없다.

---

## 3. 일상 관리

### 3.1 OS 업데이트

```bash
# Ubuntu
sudo apt update && sudo apt upgrade -y

# Oracle Linux
sudo dnf update -y
```

월 1회 정도 실행하면 충분하다. 커널 업데이트 후에는 재부팅이 필요할 수 있다.

### 3.2 부트 볼륨 백업

Always Free에서 부트 볼륨 백업을 5개까지 무료로 저장할 수 있다.

```
OCI Console > Block Storage > Boot Volume Backups > Create
```

중요한 설정 변경 전에 수동 백업을 생성해두면 복구가 가능하다. 자동 백업 정책도 설정할 수 있지만, Always Free 범위를 초과하지 않도록 보존 기간을 짧게 설정한다.

### 3.3 모니터링

OCI 콘솔에서 기본 메트릭을 제공한다.

```
OCI Console > Compute > Instance > Metrics
- CPU Utilization
- Memory Utilization
- Network Bytes In/Out
- Disk Read/Write Bytes
```

별도의 모니터링 도구 설치 없이도 기본적인 상태 확인이 가능하다. 더 상세한 모니터링이 필요하면 VM 내부에 node_exporter + Prometheus를 설치하거나, OCI의 Monitoring 서비스 알람을 설정한다.

### 3.4 SSH 키 분실 대응

SSH 키를 분실하면 콘솔 연결(Console Connection)로 복구할 수 있다.

```
OCI Console > Compute > Instance > Console Connection > Create
→ 직렬 콘솔 또는 VNC 연결로 접속
→ 새 SSH 키를 ~/.ssh/authorized_keys에 추가
```

---

## 4. 알려진 이슈 정리

| 이슈 | 심각도 | 발생 시점 | 대응 |
|------|--------|----------|------|
| **Out of Host Capacity** | 높음 | ARM VM 생성 시 | 시간대 변경 재시도, 자동 재시도 스크립트 |
| **유휴 인스턴스 회수** | 중간 | 7일 연속 유휴 시 | cron으로 최소 활동 유지 |
| **이중 방화벽** | 중간 | 포트 오픈 시 | Security List + OS iptables 양쪽 설정 |
| **계정 정지** | 낮음 | 약관 위반 시 | 채굴 등 금지, 정상 사용이면 문제 없음 |
| **체험 종료 후 리소스 삭제** | 낮음 | 30일 후 | Always Free 범위 내 리소스만 사용 |

### 4.1 계정 정지에 대하여

커뮤니티에서 간혹 "Oracle이 Free Tier 계정을 갑자기 정지시켰다"는 보고가 있다. 대부분은 약관 위반(암호화폐 채굴, 스팸 발송 등)이거나 결제 정보 문제다. 정상적인 개발/학습 용도로 사용하면 정지될 가능성은 매우 낮다. 그래도 중요한 데이터는 정기적으로 외부 백업해두는 것이 좋다.

---

## 5. 초기 서버 세팅 체크리스트

VM 생성 후 가장 먼저 실행할 작업 목록이다.

```bash
# 1. OS 업데이트
sudo apt update && sudo apt upgrade -y

# 2. 타임존 설정
sudo timedatectl set-timezone Asia/Seoul

# 3. swap 설정 (24GB RAM이지만 안전장치)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 4. 방화벽 포트 열기
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save

# 5. Docker 설치 (ARM Ubuntu)
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER

# 6. 유휴 방지 cron (선택)
(crontab -l 2>/dev/null; echo "0 */6 * * * dd if=/dev/urandom bs=1M count=10 | md5sum > /dev/null 2>&1") | crontab -
```

---

## 체크포인트

- [ ] OCI Security List에서 필요한 포트 확인
- [ ] OS 방화벽(iptables)에서 포트 열림 확인
- [ ] 유휴 방지 cron 등록 (필요 시)
- [ ] 부트 볼륨 백업 1회 생성
- [ ] Docker 설치 및 테스트 컨테이너 실행

---

## 참고 자료

- [유휴 인스턴스 이슈 (Hacker News)](https://news.ycombinator.com/item?id=36008957)
- [계정 정지 사례 (Oracle Forums)](https://forums.oracle.com/ords/apexds/post/always-free-tier-account-suspended-without-clear-reason-3380)
- [OCI Security List 문서](https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/securitylists.htm)
- [부트 볼륨 백업 문서](https://docs.oracle.com/en-us/iaas/Content/Block/Tasks/backingupabootvolume.htm)
