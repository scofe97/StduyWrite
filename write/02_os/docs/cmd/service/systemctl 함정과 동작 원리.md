---
title: systemctl 함정과 동작 원리
tags: [linux, cheatsheet, systemctl, systemd, service, unit, mask, alias, socket]
status: draft
source:
  - systemd 259 systemctl(1) (OrbStack Ubuntu 26.04 VM 의 `man systemctl` 원문, freedesktop.org systemctl(1))
  - systemd.unit(5)·systemd.socket(5) (freedesktop.org)
  - Debian 12 `openssh-server` 1:9.2p1-2+deb12u10 패키지 파일 (`apt-get download` 로 받아 푼 내용)
related:
  - ./systemctl.md
  - ../README.md
updated: 2026-11-13
---

# systemctl 함정과 동작 원리

---

> `mask` 가 먹지 않는 경우, ssh 서비스의 이름과 소켓 활성화, `Alias=` 별칭 링크처럼 이름과 파일 자리가 만드는 함정을 모았습니다.

이 문서의 예는 [systemctl 참조 시트](./systemctl.md)의 「실습 준비」 블록을 돌린 뒤, 「실습 정리」 블록을 돌리기 전 상태에서 이어집니다. 「ssh 서비스 이름과 ssh.socket」 의 패키지 파일을 푸는 부분만 Debian 12 컨테이너에서 받았고, 나머지는 시트와 같은 OrbStack Ubuntu 26.04 VM(systemd 259)에서 받았습니다.



## mask 가 실패하는 경우

> `/etc/systemd/system/` 에 직접 둔 유닛 파일은 `mask` 로 막을 수 없습니다.

직접 만든 유닛에는 보통 통하지 않고 패키지가 `/usr/lib/systemd/system/` 에 둔 유닛을 막는 용도라고 매뉴얼이 적습니다.[^mask] 「실습 준비」 에서 `cmd-lab-demo` 를 `/usr/lib` 에 둔 이유가 이것입니다.

```bash
# mask 는 같은 이름의 파일이 /etc/systemd/system/ 에 이미 있으면 실패한다
systemctl mask cmd-lab-plain    # Failed to mask unit: File '/etc/systemd/system/cmd-lab-plain.service' already exists (종료 코드 1)
```



## ssh 서비스 이름과 ssh.socket

> 같은 서비스가 이름 둘로 불리는 것은 `[Install]` 의 `Alias=` 때문이고, 어떤 이름의 유닛이 있는지는 패키지가 정합니다.

ssh 서버의 유닛 이름은 배포판 문서마다 `ssh` 와 `sshd` 로 갈립니다. 이 VM 에는 ssh 서버 패키지가 없어서 둘 다 없다고 나옵니다.

```bash
systemctl list-unit-files 'ssh*' --no-pager
```

```bash
UNIT FILE         STATE  PRESET
ssh-access.target static -

1 unit files listed.
```

```bash
systemctl status ssh --no-pager    # Unit ssh.service could not be found. (종료 코드 4)
systemctl cat ssh.socket --no-pager    # No files found for ssh.socket. (종료 코드 1)
```

`ssh-access.target` 은 OrbStack 이 만든 것이라 sshd 와 무관합니다.

```bash
# 서버가 설치된 경우의 유닛 파일은 패키지에서 직접 확인한다
# Debian 12 컨테이너에서 openssh-server 패키지를 설치하지 않고 받아 푼다. 이 블록의 출력은 Debian 12 에서 받았다
apt-get update -qq >/dev/null 2>&1
mkdir -p ~/cmd-lab/systemctl-pkg && cd ~/cmd-lab/systemctl-pkg
apt-get download openssh-server >/dev/null 2>&1
dpkg -x openssh-server_*.deb pkg
ls pkg/lib/systemd/system
```

```bash
rescue-ssh.target
ssh.service
ssh.socket
```

```bash
grep -n -E '^(Alias|WantedBy)' pkg/lib/systemd/system/ssh.service
```

```bash
21:WantedBy=multi-user.target
22:Alias=sshd.service
```

서비스 본 이름은 `ssh.service` 이고 `Alias=sshd.service` 로 `sshd` 별칭을 달아서 `systemctl status sshd` 도 같은 유닛을 가리킵니다. 같은 패키지에는 `ssh.socket` 도 들어 있어서 `ssh` 를 멈춰도 소켓 유닛이 포트를 계속 쥐고 있을 수 있습니다.

```bash
grep -n -E '^(ListenStream|WantedBy)' pkg/lib/systemd/system/ssh.socket
```

```bash
7:ListenStream=22
11:WantedBy=sockets.target
```

socket 유닛은 같은 이름의 service 유닛을 접속이 들어올 때 띄우므로,[^socket] 이 소켓을 enable 한 시스템에서 `systemctl stop ssh` 만 하면 다음 접속에 서비스가 다시 뜰 수 있어 `ssh.socket` 도 함께 봅니다. 설치한 쪽의 실제 상태는 `systemctl list-unit-files 'ssh*'` 로 확인하는 것이 확실하고, Ubuntu 의 버전별 기본값은 이 환경에서 Ubuntu 공식 문서에 접근할 수 없어 확인하지 못했습니다.



## enable 이 만드는 별칭 링크

> `Alias=` 별칭은 `enable` 이 링크로 만들고 `disable` 이 지웁니다.

참조 시트의 「부팅 때 켜고 끄기」 에서 보았듯이 `enable` 은 `cmd-lab-nick.service` 링크를 만들었습니다. 별칭이 어떻게 만들어지는지는 실습 유닛으로 볼 수 있습니다.

```bash
# 시트의 유스케이스를 차례로 돌렸다면 cmd-lab-demo 는 떠 있고 enable 되지 않은 상태, 실습 준비만 돌렸다면 꺼져 있다. 어느 쪽이든 출력은 같다
systemctl enable --now cmd-lab-demo
systemctl is-active cmd-lab-nick    # active
systemctl status cmd-lab-nick --no-pager -n 0 | head -4
```

```bash
● cmd-lab-demo.service - cmd-lab demo service
     Loaded: loaded (/usr/lib/systemd/system/cmd-lab-demo.service; enabled; preset: enabled)
    Drop-In: /run/systemd/system/service.d
             └─zzz-lxc-service.conf
```

```bash
# 별칭 이름으로 물어도 첫 줄은 본 이름 cmd-lab-demo.service 다. Id 와 Names 로 둘의 관계를 확인한다
systemctl show -p Id,Names cmd-lab-nick
```

```bash
Id=cmd-lab-demo.service
Names=cmd-lab-demo.service cmd-lab-nick.service
```

```bash
# 별칭 링크는 enable 할 때만 생기고 disable 하면 함께 지워진다
systemctl disable --now cmd-lab-demo
```

```bash
Removed '/etc/systemd/system/multi-user.target.wants/cmd-lab-demo.service'.
Removed '/etc/systemd/system/cmd-lab-nick.service'.
```



## 관련 문서

> 이 문서와 이어지는 문서입니다.

- [systemctl 참조 시트](./systemctl.md) — 이 문서가 이어받는 실습 준비와 유스케이스의 예
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [sshd·sshd_config 참조 시트](../ssh/sshd%C2%B7sshd_config.md) — ssh 서버 데몬의 설정과 접속 거절 로그



## 참고 자료

> 공식 문서, 패키지 파일과 각주 정의입니다.

- [systemd.unit(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html) · [systemd.socket(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.socket.html)
- [systemctl(1)](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html) — `mask` 항목
- Debian 12 `openssh-server` 1:9.2p1-2+deb12u10 패키지 파일 — 2026-11-11 `apt-get download` 후 `dpkg -x`

[^mask]: systemctl(1) `mask` — "This will link these unit files to /dev/null, making it impossible to start them. This is a stronger version of disable". 같은 절 — "If a matching unit file already exists under these directories this operation will hence fail. This means that the operation is primarily useful to mask units shipped by the vendor".
[^socket]: systemd.socket(5) — "For each socket unit, a matching service unit must exist, describing the service to start on incoming traffic on the socket". systemd.unit(5) `[Install]` — "Unit files may specify aliases through the Alias= directive in the [Install] section. When the unit is enabled, symlinks will be created for those names, and removed when the unit is disabled."
