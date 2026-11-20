---
title: firewall-cmd 참조 시트
tags: [linux, cheatsheet, firewall-cmd, firewalld, nftables, network, security, cli, reference]
status: draft
source:
  - firewall-cmd(1)·firewalld(1)·firewalld.zone(5)·firewalld.zones(5)·firewalld.conf(5) (firewalld 1.3.4, Rocky Linux 9 컨테이너의 man 원문)
  - https://firewalld.org/documentation/
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/configuring_firewalls_and_packet_filters/index
related:
  - ../README.md
  - ./ss.md
  - ../../../../08_cloud/book/networking-and-kubernetes/02-02.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%ED%8C%90%EC%A0%95%ED%95%98%EB%8A%94%20%EC%B8%B5%20%E2%80%94%20Netfilter%C2%B7Conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md
  - ../../../../08_cloud/book/networking-and-kubernetes/02-03.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md
updated: 2026-11-18
---

# firewall-cmd 참조 시트

---

> firewalld 데몬에 zone·service·port 규칙을 넣고 빼는 `firewall-cmd` 의 사용법을, runtime 과 permanent 의 차이까지 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `firewall-cmd` 는 실행 중인 firewalld 데몬에 D-Bus 로 명령을 보내 방화벽 규칙을 바꾸는 클라이언트입니다.

firewalld 패키지의 외부 바이너리입니다(`rpm -qf /usr/bin/firewall-cmd` 결과 `firewalld-1.3.4-20.el9_8`). 이 시트는 Rocky Linux 9 컨테이너에서 데몬을 직접 띄워 실측했습니다. 컨테이너에는 `--privileged` 가 필요하고, 호스트에서 켜 둔 firewalld 와는 다른 네트워크 네임스페이스라 호스트 규칙에는 영향이 없습니다.[^env]

`firewall-cmd` 자체는 규칙을 만들지 않습니다. 명령은 firewalld 데몬이 받아 nftables 규칙으로 바꿉니다.

그 규칙을 커널의 netfilter 훅에 올리는 것은 nftables 입니다. 그래서 데몬이 없으면 어떤 옵션도 통하지 않습니다(「데몬이 없을 때」). netfilter 와 nftables 의 구조는 책 노트 [커널이 패킷을 판정하는 층](../../../../08_cloud/book/networking-and-kubernetes/02-02.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%ED%8C%90%EC%A0%95%ED%95%98%EB%8A%94%20%EC%B8%B5%20%E2%80%94%20Netfilter%C2%B7Conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md)과 [iptables·IPVS·eBPF](../../../../08_cloud/book/networking-and-kubernetes/02-03.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md)에 있고, 이 시트는 그 위의 관리 계층만 다룹니다.



## 핵심 문법

> 규칙은 zone 에 담기고, `--zone` 으로 zone 을 고르고 `--add-*`·`--remove-*`·`--list-*`·`--query-*` 로 동작을 정하며, `--permanent` 가 없으면 runtime 에만 반영됩니다.

```bash
# 호출 형태 (firewall-cmd --help 의 Usage)
Usage: firewall-cmd [OPTIONS...]

# 지금 규칙을 zone 별로 본다 (zone 상태 보기)
firewall-cmd --list-all

# 서비스를 연다 (서비스와 포트 열기)
firewall-cmd --add-service=<서비스>

# 포트를 연다 (서비스와 포트 열기)
firewall-cmd --add-port=<포트>/<프로토콜>

# 지금 규칙을 디스크에 저장한다 (runtime 과 permanent)
firewall-cmd --runtime-to-permanent

# 디스크 설정을 지금 규칙으로 다시 읽는다 (runtime 과 permanent)
firewall-cmd --reload
```

### 옵션 뒤에 붙는 접미사

```bash
# 같은 이름의 옵션이 동작을 갈라 가진다. 접미사는 --add-service 를 예로 든다
#   --add-service      규칙을 넣는다
#   --remove-service   규칙을 뺀다
#   --query-service    들어 있는지 묻는다 (있으면 yes·종료 코드 0, 없으면 no·1)
#   --list-services    넣은 목록을 찍는다
```



## 종료 코드

> 성공은 0, 옵션 사용이 틀리면 2, 그 밖의 실패는 이름 붙은 코드이며, `--query-*` 의 `no` 는 1 입니다[^exit].

```bash
# 0    성공
# 1    --query-* 의 답이 no
# 2    옵션 사용이 틀림 (--get-zone-of-interface 가 "no zone" 일 때도 2)
# 252  firewalld 가 떠 있지 않음 (NOT_RUNNING)
# 101  INVALID_SERVICE
# 102  INVALID_PORT
firewall-cmd --add-service=nosuch; echo $?    # Error: INVALID_SERVICE: nosuch / 101
firewall-cmd --add-port=99999/tcp; echo $?    # Error: INVALID_PORT: 99999 / 102
firewall-cmd --query-service=ftp; echo $?     # no / 1
```



## 유스케이스

### 실습 준비

> 아래 블록을 한 번 실행하면 이 시트의 예가 모두 돌아가는 Rocky Linux 9 컨테이너와 firewalld 데몬이 생깁니다.

```bash
# 컨테이너를 띄우고 firewalld 를 설치한다 (--privileged 는 nftables 를 쓰기 위해 필요하다)
docker run -d --name fw9 --privileged rockylinux:9 sleep 3600
docker exec fw9 dnf -y install firewalld nftables dbus-daemon iproute

# D-Bus 와 firewalld 데몬을 띄운다 (컨테이너에는 systemd 가 없어 직접 띄운다)
docker exec fw9 bash -c 'mkdir -p /run/dbus; dbus-uuidgen --ensure; dbus-daemon --system --fork'
docker exec -d fw9 firewalld --nofork --nopid

# 이후 예는 컨테이너 안의 셸에서 친다
docker exec -it fw9 bash
```

### zone 상태 보기

> 기본 zone 과 활성 zone, 한 zone 의 전체 설정을 봅니다.

```bash
# 데몬 상태와 버전
firewall-cmd --state       # running
firewall-cmd --version     # 1.3.4

# 기본 zone 과 정의된 zone 목록
firewall-cmd --get-default-zone    # public
firewall-cmd --get-zones           # block dmz drop external home internal public trusted work

# 인터페이스나 출발지가 묶인 활성 zone (묶인 것이 없으면 빈 출력)
firewall-cmd --get-active-zones

# 기본 zone 의 전체 설정
firewall-cmd --list-all
```

```bash
public
  target: default
  icmp-block-inversion: no
  interfaces: 
  sources: 
  services: cockpit dhcpv6-client ssh
  ports: 
  protocols: 
  forward: yes
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules: 
```

`target: default` 는 어떤 규칙에도 맞지 않은 패킷을 거부한다는 뜻입니다[^target]. `trusted` 는 `ACCEPT`, `drop` 은 `DROP` 으로 정해져 있습니다.

### 서비스와 포트 열기

> 이름 붙은 서비스나 포트 번호를 zone 에 넣고, 들어 있는지 묻고, 뺍니다.

```bash
# 서비스 정의가 무엇을 여는지 본다
firewall-cmd --info-service=http    # ports: 80/tcp (그 밖의 항목은 빈 줄)

# 서비스를 넣고 확인하고 뺀다
firewall-cmd --add-service=https       # success
firewall-cmd --query-service=https     # yes
firewall-cmd --remove-service=https    # success

# 포트 하나, 여러 개, 범위를 넣는다
firewall-cmd --add-port=8080/tcp
firewall-cmd --add-port=80/tcp --add-port=443/tcp
firewall-cmd --add-port=8000-8010/tcp

# 넣은 포트를 찍는다
firewall-cmd --list-ports    # 80/tcp 443/tcp 8000-8010/tcp 처럼 넣은 포트가 공백으로 이어진다

# 시간이 지나면 저절로 빠지게 넣는다 (초 숫자나 s·m·h 접미사)
firewall-cmd --add-port=9090/tcp --timeout=30s    # success
```

같은 규칙을 두 번 넣거나 없는 규칙을 빼면 경고가 나오지만 종료 코드는 0 입니다.

```bash
firewall-cmd --add-service=ssh --zone=public
# Warning: ALREADY_ENABLED: 'ssh' already in 'public'
# success

firewall-cmd --remove-port=1234/tcp
# Warning: NOT_ENABLED: '1234:tcp' not in 'public'
# success
```

### runtime 과 permanent

> 옵션만 쓰면 지금 규칙(runtime)만 바뀌고 `--permanent` 를 붙여야 디스크 설정이 바뀌므로, 둘의 차이를 따라 쳐서 확인합니다[^perm].

```bash
# runtime 에만 넣는다
firewall-cmd --add-port=8080/tcp          # success
firewall-cmd --list-ports                 # 8080/tcp
firewall-cmd --permanent --list-ports     # (빈 줄)

# 디스크 설정을 다시 읽으면 runtime 에만 있던 규칙이 사라진다
firewall-cmd --reload          # success
firewall-cmd --list-ports      # (빈 줄)

# 지금 규칙을 통째로 디스크에 저장한다
firewall-cmd --add-port=8080/tcp          # success
firewall-cmd --runtime-to-permanent       # success
firewall-cmd --permanent --list-ports     # 8080/tcp

# permanent 에만 넣으면 지금은 열리지 않고 reload 뒤에 열린다
firewall-cmd --permanent --add-port=5432/tcp    # success
firewall-cmd --list-ports --zone=public         # (빈 줄)
firewall-cmd --permanent --list-ports           # 5432/tcp
```

`--timeout` 은 `--permanent` 와 함께 쓰지 못합니다. 설정을 확인하는 `--check-config` 는 디스크 설정에 오류가 없으면 `success` 를 냅니다.

### zone 에 인터페이스와 출발지 묶기

> 인터페이스나 출발지 주소를 zone 에 묶고, 묶인 zone 을 거꾸로 묻습니다.

```bash
# 인터페이스를 internal 에 묶는다
firewall-cmd --get-zone-of-interface=eth0    # no zone (종료 코드 2)
firewall-cmd --add-interface=eth0 --zone=internal
firewall-cmd --get-zone-of-interface=eth0    # internal

# 출발지 주소 대역을 trusted 에 묶는다
firewall-cmd --add-source=192.0.2.0/24 --zone=trusted
firewall-cmd --get-zone-of-source=192.0.2.0/24    # trusted

# 기본 zone 을 바꾼다 (runtime 과 permanent 가 함께 바뀐다)
firewall-cmd --set-default-zone=internal
```

```bash
firewall-cmd --get-active-zones
```

```bash
internal
  interfaces: eth0
trusted
  sources: 192.0.2.0/24
```

패킷이 인터페이스와 출발지 양쪽에 맞으면 출발지로 묶은 zone 이 먼저 고려됩니다(「zone 판정 순서」).

### rich rule 과 masquerade

> 서비스·포트 목록으로 못 쓰는 출발지 조건이나 거부 규칙은 rich rule 로, NAT 는 masquerade 로 넣습니다.

```bash
# 출발지 대역에만 22 번 포트를 허용한다
firewall-cmd --permanent --add-rich-rule='rule family=ipv4 source address=192.0.2.0/24 port port=22 protocol=tcp accept'
firewall-cmd --permanent --list-rich-rules
# rule family="ipv4" source address="192.0.2.0/24" port port="22" protocol="tcp" accept

# 특정 출발지의 ssh 만 버린다
firewall-cmd --add-rich-rule='rule family=ipv4 source address=198.51.100.7 service name=ssh drop' --zone=public

# 출발지 주소를 바꿔 내보내는 masquerade 를 켠다
firewall-cmd --add-masquerade     # success
firewall-cmd --query-masquerade   # yes
```

### nftables 규칙으로 확인

> `firewall-cmd` 가 넣은 규칙은 `inet firewalld` 테이블의 체인으로 보이므로, `nft` 로 실제 반영을 확인합니다.

```bash
# firewalld 가 만든 테이블
nft list tables    # table inet firewalld

# 입력 훅에서 zone 별 체인으로 넘기는 흐름
nft list chain inet firewalld filter_INPUT
```

```bash
table inet firewalld {
	chain filter_INPUT {
		type filter hook input priority filter + 10; policy accept;
		ct state { established, related } accept
		ct status dnat accept
		iifname "lo" accept
		ct state invalid drop
		jump filter_INPUT_ZONES
		reject with icmpx admin-prohibited
	}
}
```

```bash
# 포트를 넣기 전과 뒤의 internal zone 허용 체인을 맞대면 한 줄이 늘어난다
firewall-cmd --zone=internal --add-port=7000/tcp
nft list chain inet firewalld filter_IN_internal_allow    # 끝에 tcp dport 7000 accept 가 붙는다
```

### 설정 파일과 데몬 없이 고치기

> permanent 설정은 `/etc/firewalld/` 의 XML 파일이고, 데몬이 꺼져 있을 때는 `firewall-offline-cmd` 로 그 파일을 고칩니다.

```bash
# permanent 로 넣은 규칙은 zone XML 에 쌓인다
cat /etc/firewalld/zones/public.xml
```

```bash
<?xml version="1.0" encoding="utf-8"?>
<zone>
  <short>Public</short>
  <description>For use in public areas. You do not trust the other computers on networks to not harm your computer. Only selected incoming connections are accepted.</description>
  <service name="ssh"/>
  <service name="dhcpv6-client"/>
  <service name="cockpit"/>
  <port port="8080" protocol="tcp"/>
  <rule family="ipv4">
    <source address="192.0.2.0/24"/>
    <port port="22" protocol="tcp"/>
    <accept/>
  </rule>
  <forward/>
</zone>
```

```bash
# 데몬이 없어도 설정 파일을 고친다
firewall-offline-cmd --add-port=7777/tcp    # success
firewall-offline-cmd --list-ports           # 5432/tcp 7777/tcp
```

### 실습 정리

```bash
# 실습 컨테이너를 지운다
docker rm -f fw9
```



## 주의사항과 동작 원리

### runtime 과 permanent 분리

> `--permanent` 없이 넣은 규칙은 reload·재시작에 사라지고, `--permanent` 만 붙여 넣은 규칙은 reload 전까지 열리지 않으므로, 확인은 두 값을 모두 봅니다.

```bash
# runtime 에만 넣고 reload 한다
firewall-cmd --add-port=8080/tcp
firewall-cmd --reload
firewall-cmd --list-ports    # (빈 줄)

# permanent 로 만든 새 zone 은 reload 뒤에야 보인다
firewall-cmd --permanent --new-zone=web
firewall-cmd --get-zones     # block dmz drop external home internal public trusted work
firewall-cmd --reload
firewall-cmd --get-zones     # block dmz drop external home internal public trusted web work
```

`--reload` 는 permanent 설정을 새 runtime 으로 삼기 때문에, permanent 에 없던 runtime 규칙이 사라집니다.[^reload] 둘 다에 넣으려면 같은 명령을 `--permanent` 유무로 두 번 치거나, runtime 에서 시험한 뒤 `--runtime-to-permanent` 로 저장합니다.

인터페이스 묶음도 runtime 에만 있었으면 reload 뒤 사라집니다. 이번 실습에서도 reload 뒤 `filter_INPUT_ZONES` 가 `public` 하나로 돌아갔습니다.

### 기본 zone 이 아닌 zone 을 만지는 실수

> `--zone` 을 빼면 기본 zone 에만 적용되므로, 접속이 실제로 속한 zone 과 다르면 규칙이 엉뚱한 곳에 들어갑니다.

```bash
# 활성 zone 은 internal·trusted 인데 기본 zone 은 public 인 상태에서 --zone 없이 친다
firewall-cmd --list-ports
```

```bash
You're performing an operation over default zone ('public'),
but your connections/interfaces are in zone 'internal,trusted' (see --get-active-zones)
You most likely need to use --zone=internal option.
```

```bash
# 접속이 속한 zone 을 지정한다
firewall-cmd --zone=internal --add-port=7000/tcp
```

명령은 경고만 내고 그대로 실행되므로, 규칙을 넣은 뒤에도 연결이 안 되면 `--get-active-zones` 로 접속이 속한 zone 부터 확인합니다.

### zone 판정 순서

> 같은 패킷이 출발지 zone 과 인터페이스 zone 에 모두 맞으면 출발지 zone 이 먼저 걸리고, 어디에도 안 맞으면 기본 zone 으로 갑니다.

```bash
firewall-cmd --add-interface=eth0 --zone=internal
firewall-cmd --add-source=192.0.2.0/24 --zone=trusted
nft list chain inet firewalld filter_INPUT_ZONES
```

```bash
table inet firewalld {
	chain filter_INPUT_ZONES {
		ip saddr 192.0.2.0/24 goto filter_IN_trusted
		iifname "eth0" goto filter_IN_internal
		goto filter_IN_public
	}
}
```

nftables 체인이 위에서 아래로 평가되므로 출발지 줄이 인터페이스 줄보다 먼저 맞습니다. firewalld 가 이 순서를 문서로 못 박았는지는 이번에 열어 본 공식 문서에서 찾지 못했고, 위 순서는 1.3.4 가 만든 규칙에서 읽은 값입니다.

### 데몬이 없을 때

> firewalld 가 떠 있지 않으면 `firewall-cmd` 는 규칙을 못 넣고 종료 코드 252 로 끝나며, 이때는 `firewall-offline-cmd` 가 설정 파일만 고칩니다.

```bash
firewall-cmd --state                          # not running (종료 코드 252)
firewall-cmd --add-port=1/tcp                 # FirewallD is not running (종료 코드 252)
firewall-cmd --permanent --add-port=1/tcp     # FirewallD is not running (종료 코드 252)
```

`--permanent` 도 데몬을 거치므로 같은 오류입니다. 데몬이 꺼진 상태에서 설정 파일을 고쳐야 하면 `firewall-offline-cmd` 를 쓰고, 데몬은 다음 시작 때 그 파일을 읽습니다.

### iptables 와 혼용 금지

> firewalld 의 기본 backend 는 nftables 이고, 직접 `iptables` 나 `nft` 로 같은 훅에 규칙을 넣으면 firewalld 의 관리 밖이라 reload 에 어떻게 될지 알 수 없습니다.[^backend]

```bash
# firewalld 가 쓰는 backend 와 직접 규칙(direct rule) 확인
grep ^FirewallBackend /etc/firewalld/firewalld.conf    # FirewallBackend=nftables
firewall-cmd --direct --get-all-rules                  # (빈 출력)
```

`--direct` 인터페이스는 폐기 예정이고 항상 iptables 계열 backend 를 씁니다[^direct]. 새 규칙은 zone·service·rich rule 로 넣는 쪽이 낫고, 이 시트는 `iptables` 와 직접 규칙을 섞은 동작은 돌려 보지 않았습니다.

### 패닉 모드

> `--panic-on` 은 들어오고 나가는 모든 패킷을 버리고 runtime 에만 걸리므로, 원격 접속에서 켜면 그 접속도 끊깁니다.

```bash
firewall-cmd --panic-on      # success
firewall-cmd --query-panic   # yes
firewall-cmd --panic-off     # success
```

man 은 "serious problems with your network environment" 일 때만 켜라고 적습니다.[^panic] 이번 컨테이너는 외부 접속 없이 `docker exec` 로 쳤고, 패킷이 실제로 끊기는 것까지는 확인하지 않았습니다.

### 거부된 패킷 기록

> `--set-log-denied` 는 reject·drop 규칙 앞에 로그 규칙을 넣고 firewalld 를 reload 합니다.

```bash
firewall-cmd --get-log-denied          # off
firewall-cmd --set-log-denied=all
firewall-cmd --get-log-denied          # all
firewall-cmd --set-log-denied=off      # success
```

값은 `all`·`unicast`·`broadcast`·`multicast`·`off` 입니다[^log]. 이번 컨테이너에서는 `--set-log-denied=all` 이 한 번 `Error: dictionary changed size during iteration`(종료 코드 254)로 끝났는데도, 이어서 `--get-log-denied` 는 `all` 을 냈습니다.

원인은 확인하지 못했으니 값을 바꾼 뒤에는 `--get-log-denied` 로 확인합니다. 로그가 어디에 남는지는 이번에 보지 않았습니다.



## 관련 문서

> 규칙이 올라가는 커널 층과 포트 상태 확인은 아래 문서에서 이어서 봅니다.

- [ss 참조 시트](./ss.md) — 규칙을 연 뒤 포트가 실제로 듣고 있는지 확인합니다
- [커널이 패킷을 판정하는 층 — Netfilter·Conntrack·라우팅](../../../../08_cloud/book/networking-and-kubernetes/02-02.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%ED%8C%90%EC%A0%95%ED%95%98%EB%8A%94%20%EC%B8%B5%20%E2%80%94%20Netfilter%C2%B7Conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) — firewalld 규칙이 올라가는 netfilter 훅과 conntrack
- [iptables·IPVS·eBPF — kube-proxy를 이해하는 세 기술](../../../../08_cloud/book/networking-and-kubernetes/02-03.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md) — iptables 와 nftables 규칙 모델의 비교



## 참고 자료

> 검증은 Rocky Linux 9 컨테이너에서 했고, 옵션과 종료 코드 뜻은 같은 컨테이너의 man 원문과 대조했습니다.

- 검증 환경: Rocky Linux 9 컨테이너(`--privileged`), firewalld 1.3.4-20.el9_8, nftables 1.0.9-9.el9_8, 2026-11-18
- [firewalld 공식 문서](https://firewalld.org/documentation/)
- [RHEL 9 — Configuring firewalls and packet filters](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/configuring_firewalls_and_packet_filters/index)

[^env]: firewall-cmd(1) 1.3.4. 컨테이너에서 `dbus-daemon --system --fork` 와 `firewalld --nofork --nopid` 를 직접 띄운 뒤 `firewall-cmd --state` 가 `running` 을 냈습니다. 호스트에서 systemd 로 돌리는 구성과 같은 명령 집합이지만, 서비스 기동·NetworkManager 연동은 이 컨테이너에서 확인하지 않았습니다.
[^exit]: firewall-cmd(1) EXIT CODES. "On success 0 is returned. On failure the output is red colored and exit code is either 2 in case of wrong command-line option usage or one of the following error codes in other cases". 표에 `INVALID_SERVICE 101`, `INVALID_PORT 102`, `ALREADY_ENABLED 11`, `NOT_ENABLED 12` 가 있습니다. 252(NOT_RUNNING)와 `--query-*` 의 1 은 같은 컨테이너에서 `echo $?` 로 확인했습니다.
[^target]: firewalld.zone(5) `target`. "If the target is not specified, every packet not matching any rule will be rejected." `ACCEPT` 는 trusted, `%%REJECT%%` 는 block, `DROP` 은 drop zone 에서 씁니다.
[^perm]: firewall-cmd(1) `--permanent`. "These changes are not effective immediately, only after service restart/reload or system reboot. Without the --permanent option, a change will only be part of the runtime configuration." `--runtime-to-permanent` 는 "Save active runtime configuration and overwrite permanent configuration with it".
[^reload]: firewall-cmd(1) `--reload`. "Current permanent configuration will become new runtime configuration, i.e. all runtime only changes done until reload are lost with reload if they have not been also in permanent configuration." `FlushAllOnReload=no` 이면 direct 인터페이스로 넣은 규칙은 reload 에 남습니다.
[^backend]: firewalld.conf(5) `FirewallBackend`. "Selects the firewall backend implementation. Possible values are; nftables (default), or iptables." iptables backend 는 폐기 예정이라고 적혀 있습니다.
[^direct]: firewalld.conf(5) `FirewallBackend`. "The only exception is direct and passthrough rules which always use the traditional iptables, ip6tables, and ebtables backends." firewalld(1) 은 direct 인터페이스를 `DEPRECATED` 로 표시합니다.
[^panic]: firewall-cmd(1) `--panic-on`. "Enable panic mode. All incoming and outgoing packets are dropped, active connections will expire. Enable this only if there are serious problems with your network environment." 이 변경은 runtime 에만 적용됩니다.
[^log]: firewall-cmd(1) `--set-log-denied`. "The possible values are: all, unicast, broadcast, multicast and off. The default setting is off, which disables the logging. This is a runtime and permanent change and will also reload the firewall to be able to add the logging rules."
