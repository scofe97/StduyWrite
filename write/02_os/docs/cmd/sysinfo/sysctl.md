---
title: sysctl 참조 시트
tags: [linux, cheatsheet, sysctl, kernel, proc, systemd, sysinfo, cli, reference]
status: draft
source:
  - procps sysctl(8) (man7.org 최신판) 과 OrbStack VM 의 `sysctl --help` (Debian 12 procps 4.0.2, Rocky Linux 9 procps-ng 3.3.17)
  - sysctl.d(5)·systemd-sysctl.service(8) (freedesktop.org, 문서 머리 버전 262)
  - Documentation for /proc/sys, Linux kernel IP Sysctl (docs.kernel.org)
related:
  - ../README.md
  - ../service/systemctl.md
  - ../../../book/learning-modern-linux/05-01.모든%20것이%20파일이라는%20말은%20손잡이가%20하나라는%20뜻이다.md
  - ../../../book/learning-modern-linux/06-01.먼저%20켜지는%20것%20하나가%20나머지%20전부를%20켠다.md
  - ../../../book/learning-modern-linux/07-02.포트가%20있어야%20서비스를%20가리킬%20수%20있고%20이름이%20있어야%20사람이%20기억한다.md
updated: 2026-11-17
---

# sysctl 참조 시트

---

> 커널 매개변수를 `sysctl` 로 읽고, 지금 바꾸고, 파일에 적어 부팅 뒤에도 남기는 방법을 VM 에서 돌려 본 출력과 함께 모았습니다.

## 개요

> `sysctl` 은 `/proc/sys` 아래 커널 매개변수를 점으로 이은 이름으로 읽고 쓰고, 설정 파일에서 불러오는 명령입니다.[^sysctl8]

procps 패키지의 외부 바이너리(`/usr/sbin/sysctl`)입니다. 출력은 OrbStack Debian 12(procps 4.0.2)와 Rocky Linux 9(procps-ng 3.3.17)에서 받았습니다. 두 배포판의 `--help` 는 같았습니다. Debian 이미지에는 처음에 `sysctl` 이 없어서 `sudo apt-get install -y procps` 로 설치했습니다.

OrbStack 머신은 모두 `uname -r` 이 같아서 커널을 함께 씁니다. 이 시트는 머신마다 따로 갖는 키 `net.ipv4.ip_unprivileged_port_start` 하나만 바꿉니다. 그 값이 다른 머신에 새지 않음은 「네트워크 네임스페이스별 값」 에서 확인합니다.



## 핵심 문법

> 키 이름으로 읽을 대상을 고르고 `-w` 나 파일 옵션으로 쓸지 정하며, 이름이 없는 파일 옵션은 값을 파일에서 불러옵니다.

```bash
# 호출 형태 (sysctl --help 의 Usage 둘째 줄)
sysctl [options] [variable[=value] ...]

# 키 값을 읽는다 (키 읽기)
sysctl 키

# 모든 키를 읽는다 (전체 목록에서 키 찾기)
sysctl -a

# /proc/sys 파일과 같은 값을 본다 (/proc/sys 파일과 같은 값)
cat /proc/sys/경로

# 지금 값을 바꾼다. 재부팅하면 사라진다 (지금 값 바꾸기)
sudo sysctl -w 키=값

# 설정 파일을 읽어 적용한다 (설정 파일에 적어 두기)
sudo sysctl -p 파일
sudo sysctl --system

# 부팅 때 파일을 적용하는 서비스를 다시 돌린다 (부팅 때 적용하는 서비스)
sudo systemctl restart systemd-sysctl
```

### 키 이름과 설정 파일 한 줄

```bash
# 키 이름은 점이나 슬래시로 /proc/sys 아래 경로를 잇는다. 둘은 같은 키다
# kernel.domainname=foo     kernel/domainname=foo   /proc/sys/kernel/domainname 에 foo 를 쓴다
# 이름 안에 점이 들어 있는 인터페이스는 첫 구분자 쪽을 따른다
# net.ipv4.conf.enp3s0/200.forwarding   net/ipv4/conf/enp3s0.200/forwarding   같은 키다

# 설정 파일의 한 줄 (sysctl.d(5))
# 키 = 값        한 줄에 키 하나. 빈 줄과 # · ; 로 시작하는 줄은 무시한다
# -키 = 값       systemd-sysctl 에서 쓰는 꼴. 쓰기에 실패해도 서비스가 실패하지 않는다
# 키.*.패턴      systemd-sysctl 에서 쓰는 glob. 같은 값을 맞는 키 모두에 쓴다
```

설정 파일의 한 줄 꼴은 [sysctl.d(5)](https://www.freedesktop.org/software/systemd/man/latest/sysctl.d.html)가 정합니다.[^sysctld]



## 종료 코드

> 성공이면 0, 키를 못 찾거나 권한이 없거나 값이 거절되면 1 입니다.

sysctl(8) 에는 종료 코드 절이 없어서 아래는 모두 `명령; echo $?` 로 읽은 실측입니다. 「실습 준비」 를 돌린 뒤 실행합니다.

```bash
# 0  읽기·쓰기 성공. -e 를 붙이면 모르는 키도 0
# 1  모르는 키, 권한 없음, 값 거절, = 없이 -w 에 준 키

# 모르는 키는 1 로 끝난다
sysctl net.ipv4.no_such_key; echo $?
# sysctl: cannot stat /proc/sys/net/ipv4/no_such_key: No such file or directory
# 1

# 모르는 키 오류를 무시한다
#   -e   모르는 키 오류를 무시한다 (--ignore)
sysctl -e net.ipv4.no_such_key; echo $?    # 0

# 권한이 없으면 1 이다
sysctl -w net.ipv4.ip_unprivileged_port_start=80; echo $?
# sysctl: permission denied on key "net.ipv4.ip_unprivileged_port_start"
# 1

# 값을 커널이 거절해도 1 이다
sudo sysctl -w net.ipv4.ip_unprivileged_port_start=abc; echo $?
# sysctl: setting key "net.ipv4.ip_unprivileged_port_start": Invalid argument
# 1

# = 와 값 없이 -w 를 주면 문법 오류로 1 이다
sudo sysctl -w net.ipv4.ip_unprivileged_port_start; echo $?
# sysctl: command line(0): invalid syntax, continuing...
# 1
```



## 유스케이스

> 예는 앞 예가 만든 상태를 이어 쓰므로 위에서 아래로 차례로 돌립니다.

### 실습 준비

> 일반 사용자 셸에서 `sudo` 가 되는 VM 에 아래 두 줄을 붙여 넣으면 이 시트가 쓰는 PATH 와 바꿀 키 하나의 시작값을 확인합니다.

Debian 의 일반 사용자 PATH 에는 `/usr/sbin` 이 없어서 `sysctl` 이 `command not found` 로 끝납니다. Rocky 는 PATH 에 이미 있어 첫 줄이 필요 없고, 설정 파일은 각 예가 만들고 「실습 정리」 가 지웁니다.

```bash
# sysctl 이 있는 /usr/sbin 을 PATH 에 더한다 (Debian)
export PATH=$PATH:/usr/sbin

# 이 시트가 바꿀 키의 시작값. 다른 값이면 「실습 정리」 에서 이 값으로 돌린다
sysctl net.ipv4.ip_unprivileged_port_start    # net.ipv4.ip_unprivileged_port_start = 1024
```

### 키 읽기

> 키 이름을 주면 `키 = 값` 으로 읽고, 옵션으로 값만 또는 이름만 찍습니다.

```bash
# 키 둘을 한 번에 읽는다. 값이 여러 개인 키는 탭으로 이어서 찍는다
sysctl net.ipv4.ip_local_port_range net.ipv4.ip_unprivileged_port_start
```

```bash
net.ipv4.ip_local_port_range = 32768	60999
net.ipv4.ip_unprivileged_port_start = 1024
```

```bash
# 키 이름 없이 값만 찍는다. 스크립트에서 변수에 담을 때 쓴다
#   -n   키 이름 없이 값만 찍는다 (--values)
sysctl -n net.ipv4.ip_local_port_range    # 32768	60999

# 값 없이 이름만 찍는다
#   -N   이름만 찍는다 (--names)
sysctl -N net.ipv4.ip_unprivileged_port_start    # net.ipv4.ip_unprivileged_port_start
```

`ip_local_port_range` 는 클라이언트가 `connect()` 할 때 임시 포트를 고르는 범위입니다. 첫 값은 `ip_unprivileged_port_start` 이상이어야 합니다.[^ipsysctl]

### 전체 목록에서 키 찾기

> `-a` 는 읽을 수 있는 키를 모두 찍으므로 `grep` 으로 이름 일부를 찾고, 읽을 수 없는 키는 경고로 알려 줍니다.

일반 사용자는 읽을 수 없는 키가 있어서 stderr 에 경고가 나옵니다. 아래 첫 명령은 stderr 를 버리고 줄 수만 셉니다.

```bash
# 키가 몇 개인지 센다. 경고는 /dev/null 로 버린다
#   -a   읽을 수 있는 키를 모두 찍는다 (--all)
sysctl -a 2>/dev/null | wc -l    # 979

# 이름 일부로 찾는다
sysctl -a 2>/dev/null | grep ip_local_port
```

```bash
net.ipv4.ip_local_port_range = 32768	60999
net.ipv4.ip_local_port_step_width = 0
```

```bash
# 경고만 앞 세 줄 본다. stdout 은 버리고 stderr 만 파이프로 보낸다
sysctl -a 2>&1 >/dev/null | head -3
```

```bash
sysctl: permission denied on key 'kernel.cad_pid'
sysctl: permission denied on key 'kernel.usermodehelper.bset'
sysctl: permission denied on key 'kernel.usermodehelper.inheritable'
```

```bash
# 정규식으로 키를 고른다. grep 을 거치지 않아도 된다
#   -r   확장 정규식에 맞는 키만 고른다 (--pattern)
sysctl -a -r '^net.ipv4.ip_(local_port_range|unprivileged)'
```

```bash
net.ipv4.ip_local_port_range = 32768	60999
net.ipv4.ip_unprivileged_port_start = 1024
```

### /proc/sys 파일과 같은 값

> `sysctl` 키의 점은 `/proc/sys` 아래 경로의 슬래시이고, 파일을 `cat` 으로 읽어도 같은 값입니다.

```bash
# 파일을 직접 읽는다
cat /proc/sys/net/ipv4/ip_local_port_range    # 32768	60999

# 같은 키를 sysctl 로 읽는다
sysctl -n net.ipv4.ip_local_port_range    # 32768	60999

# 슬래시로 쓴 이름도 받는다. 출력은 점으로 바뀐다
sysctl net/ipv4/ip_local_port_range    # net.ipv4.ip_local_port_range = 32768	60999
```

`/proc/sys` 파일을 읽고 쓰면 `sysctl` 이 하는 일과 같습니다. `sysctl` 은 이름 규칙과 파일 읽기를 대신 해 주는 도구입니다.[^kdoc]

### 지금 값 바꾸기

> 일반 사용자는 값을 못 바꾸고 root 로 `-w` 를 주면 바뀌며, 재부팅하면 원래 값으로 돌아갑니다.

```bash
# 일반 사용자가 바꾸면 거절된다
sysctl -w net.ipv4.ip_unprivileged_port_start=80
# sysctl: permission denied on key "net.ipv4.ip_unprivileged_port_start"

# root 로 바꾼다. 바꾼 값을 그대로 찍는다
#   -w   뒤의 인자를 읽기가 아니라 쓰기로 읽는다 (--write)
sudo sysctl -w net.ipv4.ip_unprivileged_port_start=80    # net.ipv4.ip_unprivileged_port_start = 80

# /proc/sys 파일에도 같은 값이 들어갔다
cat /proc/sys/net/ipv4/ip_unprivileged_port_start    # 80

# 바꾼 값을 찍지 않는다
#   -q   쓴 값을 찍지 않는다 (--quiet)
sudo sysctl -q -w net.ipv4.ip_unprivileged_port_start=100
sysctl -n net.ipv4.ip_unprivileged_port_start    # 100

# 파일에 직접 써서 되돌린다. 같은 결과다
echo 1024 | sudo tee /proc/sys/net/ipv4/ip_unprivileged_port_start    # 1024
sysctl net.ipv4.ip_unprivileged_port_start    # net.ipv4.ip_unprivileged_port_start = 1024
```

### 설정 파일에 적어 두기

> 설정 파일은 적는 것만으로는 반영되지 않고, `-p` 가 파일을 읽을 때 적용됩니다.

```bash
# 설정 파일을 만든다. tee 가 찍는 내용은 /dev/null 로 버린다
echo 'net.ipv4.ip_unprivileged_port_start = 90' | sudo tee /etc/sysctl.d/90-cmdlab.conf > /dev/null

# 파일만 만들었으니 값은 그대로다
sysctl -n net.ipv4.ip_unprivileged_port_start    # 1024

# 파일을 읽어 적용한다
#   -p   인자로 준 설정 파일을 읽어 적용한다 (--load)
sudo sysctl -p /etc/sysctl.d/90-cmdlab.conf    # net.ipv4.ip_unprivileged_port_start = 90
sysctl -n net.ipv4.ip_unprivileged_port_start    # 90
```

`-p` 에 파일을 주지 않으면 `/etc/sysctl.conf` 를 읽고, 파일 이름에 `-` 를 주면 표준 입력을 읽습니다.[^sysctl8]

### 시스템 파일 전부 다시 읽기

> `--system` 은 설정 디렉터리의 파일을 정해진 순서로 모두 읽고, `--pattern` 을 함께 주면 맞는 키만 적용합니다.

```bash
# 값을 되돌려 놓고 설정 디렉터리 전부를 읽는다. 키 하나만 적용하게 고른다
#   --system    설정 디렉터리의 파일을 모두 읽어 적용한다
#   --pattern   맞는 키만 적용한다. -r 과 같다
sudo sysctl -w net.ipv4.ip_unprivileged_port_start=1024 > /dev/null
sudo sysctl --pattern '^net.ipv4.ip_unprivileged' --system
```

```bash
* Applying /usr/lib/sysctl.d/50-pid-max.conf ...
* Applying /etc/sysctl.d/90-cmdlab.conf ...
* Applying /usr/lib/sysctl.d/99-protect-links.conf ...
* Applying /etc/sysctl.d/99-sysctl.conf ...
* Applying /etc/sysctl.conf ...
net.ipv4.ip_unprivileged_port_start = 90
```

`Applying` 줄이 읽은 파일을 읽은 순서대로 보여 줍니다. 마지막 `/etc/sysctl.conf` 는 항상 맨 끝에 읽혀서 앞 파일들의 값을 덮을 수 있습니다.[^sysctl8]

### 파일 이름 순서와 충돌

> 같은 키를 여러 파일이 적으면 디렉터리와 상관없이 이름이 사전순으로 뒤인 파일의 값이 이기고, 같은 이름은 우선순위 높은 디렉터리의 파일 하나만 읽힙니다.

```bash
# 앞 예의 90 번 파일은 지우고, 이름이 다른 두 파일을 둔다. /etc 의 50 번과 /usr/lib 의 60 번이 같은 키를 적는다
sudo rm /etc/sysctl.d/90-cmdlab.conf
echo 'net.ipv4.ip_unprivileged_port_start = 50' | sudo tee /etc/sysctl.d/50-cmdlab.conf > /dev/null
echo 'net.ipv4.ip_unprivileged_port_start = 60' | sudo tee /usr/lib/sysctl.d/60-cmdlab.conf > /dev/null
sudo sysctl --pattern '^net.ipv4.ip_unprivileged' --system | grep -E 'cmdlab|^net'
```

```bash
* Applying /etc/sysctl.d/50-cmdlab.conf ...
* Applying /usr/lib/sysctl.d/60-cmdlab.conf ...
net.ipv4.ip_unprivileged_port_start = 50
net.ipv4.ip_unprivileged_port_start = 60
```

```bash
# 디렉터리가 /etc 와 /usr/lib 로 달라도 이름 순서로 읽혀 60 이 마지막에 쓰였다
sysctl -n net.ipv4.ip_unprivileged_port_start    # 60

# 같은 이름이면 /etc 의 파일 하나만 읽힌다. 앞의 두 파일은 지우고 같은 이름 둘을 둔다
sudo rm /etc/sysctl.d/50-cmdlab.conf /usr/lib/sysctl.d/60-cmdlab.conf
echo 'net.ipv4.ip_unprivileged_port_start = 70' | sudo tee /usr/lib/sysctl.d/90-cmdlab.conf > /dev/null
echo 'net.ipv4.ip_unprivileged_port_start = 90' | sudo tee /etc/sysctl.d/90-cmdlab.conf > /dev/null
sudo sysctl --pattern '^net.ipv4.ip_unprivileged' --system | grep -E 'cmdlab|^net'
```

```bash
* Applying /etc/sysctl.d/90-cmdlab.conf ...
net.ipv4.ip_unprivileged_port_start = 90
```

`/usr/lib/sysctl.d/90-cmdlab.conf`(70)는 읽히지 않고 `/etc/sysctl.d/90-cmdlab.conf`(90)만 적용됩니다.[^sysctld] 그래서 `/etc` 에서 벤더 파일을 이기려면 같은 이름으로 덮거나, 사전순으로 뒤인 이름의 파일을 둡니다.

```bash
# 이 예가 /usr/lib 에 둔 파일은 여기서 지운다. 벤더 디렉터리를 비교하는 뒤 예에 섞이지 않게 한다
sudo rm /usr/lib/sysctl.d/90-cmdlab.conf
```

### 부팅 때 적용하는 서비스

> 부팅 때 설정 파일을 적용하는 것은 `systemd-sysctl.service` 이고, 이 서비스를 다시 돌리면 파일 값이 런타임 값을 덮습니다.[^sdsysctl]

```bash
# 서비스의 종류와 유닛 파일 자리
systemctl show -p Type,FragmentPath systemd-sysctl
```

```bash
Type=oneshot
FragmentPath=/lib/systemd/system/systemd-sysctl.service
```

```bash
# 런타임 값을 되돌려 놓고 서비스를 다시 돌린다. 파일의 90 이 들어간다
sudo sysctl -w net.ipv4.ip_unprivileged_port_start=1024 > /dev/null
sudo systemctl restart systemd-sysctl
sysctl -n net.ipv4.ip_unprivileged_port_start    # 90

# 서비스가 읽을 파일을 읽는 순서대로 나열한다. 파일 이름은 주석으로 찍힌다
#   --cat-config   설정 파일 내용을 파일 이름 주석과 함께 찍는다
/usr/lib/systemd/systemd-sysctl --cat-config | grep -E '^# /.*\.conf$'
```

```bash
# /usr/lib/sysctl.d/50-pid-max.conf
# /etc/sysctl.d/90-cmdlab.conf
# /usr/lib/sysctl.d/99-protect-links.conf
# /etc/sysctl.d/99-sysctl.conf
```

`sysctl --system` 과 달리 목록에 `/etc/sysctl.conf` 가 따로 없습니다. 이 VM 에서는 `/etc/sysctl.d/99-sysctl.conf` 가 그 파일의 심볼릭 링크이고, 서비스는 링크 하나만 읽습니다.

재부팅해도 파일의 값이 들어오는지는 호스트에서 VM 을 다시 켜서 봤습니다. 켜기 전에 런타임 값을 1024 로 되돌려 두었습니다.

```bash
# macOS 호스트에서 VM 을 다시 켠다
orb restart lmlcmd-deb

# 다시 켠 VM 의 값. 부팅 때 서비스가 파일을 적용했다
orb -m lmlcmd-deb cat /proc/sys/net/ipv4/ip_unprivileged_port_start    # 90
```

### 네트워크 네임스페이스별 값

> `ip_unprivileged_port_start` 는 네트워크 네임스페이스마다 따로 있어서, 새 네임스페이스는 호스트 값을 물려받지 않고 기본값 1024 로 시작합니다.[^ipsysctl]

```bash
# 호스트의 지금 값. 앞 예에서 90 이 들어가 있다
sysctl -n net.ipv4.ip_unprivileged_port_start    # 90

# 새 네임스페이스를 만든다
sudo ip netns add cmdlab-ns

# 그 안에서 읽으면 기본값이다
sudo ip netns exec cmdlab-ns sysctl net.ipv4.ip_unprivileged_port_start
# net.ipv4.ip_unprivileged_port_start = 1024

# 네임스페이스 안에서 바꾼다
sudo ip netns exec cmdlab-ns sysctl -w net.ipv4.ip_unprivileged_port_start=500
# net.ipv4.ip_unprivileged_port_start = 500

# 호스트 값은 그대로이고, 네임스페이스 안만 500 이다
sysctl -n net.ipv4.ip_unprivileged_port_start    # 90
sudo ip netns exec cmdlab-ns sysctl -n net.ipv4.ip_unprivileged_port_start    # 500

# 네임스페이스를 지운다
sudo ip netns del cmdlab-ns
```

같은 이유로 OrbStack 의 다른 머신(`lml-deb`)에서 읽으면 이 VM 이 90 이어도 1024 였습니다. 컨테이너와 Pod 안의 `net.*` 값이 노드의 값과 다를 수 있는 것도 같은 원리입니다.

### Debian 과 Rocky 의 기본 파일

> 두 배포판 모두 `/etc/sysctl.conf` 는 주석뿐이고 `/etc/sysctl.d/99-sysctl.conf` 가 그 링크이며, 벤더 파일은 `/usr/lib/sysctl.d/` 에 놓입니다.

```bash
# 주석과 빈 줄을 뺀 /etc/sysctl.conf 의 줄 수. 두 배포판 모두 0 이다
grep -v '^#' /etc/sysctl.conf | grep -c .    # 0

# /etc/sysctl.d 의 99-sysctl.conf 는 /etc/sysctl.conf 로 가는 링크다 (Debian 과 Rocky 공통)
ls -l /etc/sysctl.d/99-sysctl.conf    # 99-sysctl.conf -> ../sysctl.conf

# 벤더 파일. 두 배포판 모두 /lib 가 usr/lib 로 가는 링크라 같은 자리다
ls /usr/lib/sysctl.d
```

```bash
# Debian 12
50-pid-max.conf
99-protect-links.conf

# Rocky Linux 9
10-default-yama-scope.conf
50-coredump.conf
50-default.conf
50-pid-max.conf
50-redhat.conf
```

Rocky 의 `50-default.conf` 에는 `net.ipv4.conf.*.rp_filter = 2` 와 `-net.ipv4.conf.all.rp_filter` 줄이 있습니다. 위 「키 이름과 설정 파일 한 줄」 의 glob 과 `-` 꼴을 실제로 볼 수 있습니다.

### 실습 정리

```bash
# 이 시트가 만든 설정 파일을 지운다
sudo rm -f /etc/sysctl.d/90-cmdlab.conf /usr/lib/sysctl.d/90-cmdlab.conf

# 값을 시작값으로 돌린다
sudo sysctl -w net.ipv4.ip_unprivileged_port_start=1024    # net.ipv4.ip_unprivileged_port_start = 1024
```



## 주의사항과 동작 원리

### sudo 뒤의 리다이렉트

> `sudo echo 값 > /proc/sys/경로` 는 `>` 를 일반 사용자 셸이 열어서 실패하므로 `sudo tee` 로 씁니다.

```bash
# 리다이렉트는 sudo 가 아니라 현재 셸이 연다
sudo echo 200 > /proc/sys/net/ipv4/ip_unprivileged_port_start
# bash: /proc/sys/net/ipv4/ip_unprivileged_port_start: Permission denied

# tee 가 root 로 파일을 열어 쓴다
echo 200 | sudo tee /proc/sys/net/ipv4/ip_unprivileged_port_start    # 200
```

`sudo` 는 `echo` 만 root 로 돌리고 `>` 는 명령을 부른 셸이 처리하기 때문입니다. 위 두 줄을 돌렸다면 「실습 정리」 의 `sysctl -w` 로 값을 되돌립니다.

### 같은 키에 다른 값을 적는 배포판

> `sysctl --system` 은 모든 파일의 키를 다시 쓰므로, 한 커널을 여러 머신이 쓰면 다른 머신의 값까지 건드릴 수 있습니다.

```bash
# 같은 키 fs.protected_regular 를 두 배포판의 벤더 파일이 다르게 적는다
grep -h protected_regular /usr/lib/sysctl.d/*.conf
# Debian 12:     fs.protected_regular = 2
# Rocky Linux 9: fs.protected_regular = 1
```

OrbStack 머신은 커널을 함께 쓰는데 `fs.protected_*` 는 네트워크 네임스페이스 키가 아닙니다. Debian VM 에서 `--system` 을 돌리자 `fs.protected_*`·`kernel.pid_max` 값도 함께 찍혔습니다. 공용 커널에서는 위 「시스템 파일 전부 다시 읽기」 처럼 `--pattern` 으로 키를 좁힙니다.

### 편집 뒤 적용 누락

> 설정 파일은 부팅 때나 `sysctl -p`·`--system`·`systemd-sysctl` 이 읽을 때만 적용되므로, 편집 뒤에 적용 명령을 직접 돌립니다.

「설정 파일에 적어 두기」 의 첫 예가 이 함정입니다. 파일을 만든 직후 `sysctl -n` 값은 그대로 1024 였습니다.

### /proc/sys 에는 키를 만들 수 없다

> `/proc/sys` 아래 파일은 커널이 만들므로 `mkdir`·`touch` 로 새 키를 만들 수 없고, 키가 없으면 그 기능의 커널 모듈이 적재되지 않았다는 뜻일 수 있습니다.

```bash
# 키 파일을 직접 만들어 본다 (Rocky Linux 9 컨테이너, root)
mkdir /proc/sys/net/foo; echo $?                  # mkdir: cannot create directory '/proc/sys/net/foo': No such file or directory → 1
touch /proc/sys/net/ipv4/newkey; echo $?          # touch: cannot touch '/proc/sys/net/ipv4/newkey': No such file or directory → 1
sysctl -w net.foo.bar=1; echo $?                  # sysctl: cannot stat /proc/sys/net/foo/bar: No such file or directory → 1
```

root 여도 같은 결과입니다. 설정 파일에 없는 키를 적었을 때 `sysctl` 이 실패하는 것도 이 때문입니다. 키 파일을 만드는 쪽은 커널(모듈을 적재할 때 그 모듈이 키를 등록하기도 합니다)입니다. `sysctl: cannot stat` 이 나오면 오타를 먼저 보고, 오타가 아니면 해당 기능의 모듈이 적재됐는지 `lsmod` 로 확인합니다.



## 관련 문서

> 이 시트와 이어지는 시트와 책 노트입니다.

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [systemctl 참조 시트](../service/systemctl.md) — `restart`·`show` 로 `systemd-sysctl.service` 를 다루는 법
- [책 노트 5장, 모든 것이 파일이라는 말](../../../book/learning-modern-linux/05-01.모든%20것이%20파일이라는%20말은%20손잡이가%20하나라는%20뜻이다.md) — `/proc/sys` 가 놓인 가짜 파일시스템
- [책 노트 6장, 먼저 켜지는 것 하나가](../../../book/learning-modern-linux/06-01.먼저%20켜지는%20것%20하나가%20나머지%20전부를%20켠다.md) — 부팅 때 서비스가 켜지는 순서
- [책 노트 7장, 포트와 이름](../../../book/learning-modern-linux/07-02.포트가%20있어야%20서비스를%20가리킬%20수%20있고%20이름이%20있어야%20사람이%20기억한다.md) — `ip_local_port_range`·`ip_unprivileged_port_start` 가 나오는 자리



## 참고 자료

> 검증 환경과 근거 문서입니다.

- 검증 환경: OrbStack 머신 `lmlcmd-deb`(Debian 12, procps 2:4.0.2-3)와 `lmlcmd-rocky`(Rocky Linux 9.9, procps-ng 3.3.17-15)
- 둘 다 systemd 252, 커널 7.2.12-orbstack, 2026-11-17 에 확인
- [sysctl(8)](https://man7.org/linux/man-pages/man8/sysctl.8.html) — procps 매뉴얼
- [sysctl.d(5)](https://www.freedesktop.org/software/systemd/man/latest/sysctl.d.html) · [systemd-sysctl.service(8)](https://www.freedesktop.org/software/systemd/man/latest/systemd-sysctl.service.html) — freedesktop.org 최신판
- [Documentation for /proc/sys](https://docs.kernel.org/admin-guide/sysctl/index.html) · [Linux kernel IP Sysctl](https://docs.kernel.org/networking/ip-sysctl.html)

[^sysctl8]: sysctl(8) DESCRIPTION — "sysctl is used to modify kernel parameters at runtime. The parameters available are those listed under /proc/sys/. Procfs is required for sysctl support in Linux." `-p` — "Load in sysctl settings from the file specified or /etc/sysctl.conf if none given. Specifying - as filename means reading data from standard input." NOTES 「System file precedence」 — "All configuration files are sorted in lexicographic order, regardless of the directory they reside in." "The file /etc/sysctl.conf is read last which means it can replace/override any parameters previously set in files in the listed directories." https://man7.org/linux/man-pages/man8/sysctl.8.html
[^sysctld]: sysctl.d(5) — "Note that either "/" or "." may be used as separators within sysctl variable names. If the first separator is a slash, remaining slashes and dots are left intact. If the first separator is a dot, dots and slashes are interchanged." "Files in /etc/ override files with the same name in /run/, /usr/local/lib/, and /usr/lib/." "If multiple files specify the same option, the entry in the file with the lexicographically latest name will take precedence." 접두사 `-` — "if a variable assignment is prefixed with a single "-" character, failure to set the variable for any reason will be logged at debug level and will not cause the service to fail." https://www.freedesktop.org/software/systemd/man/latest/sysctl.d.html
[^sdsysctl]: systemd-sysctl.service(8) — "systemd-sysctl.service is an early boot service that configures sysctl(8) kernel parameters by invoking /usr/lib/systemd/systemd-sysctl. When invoked with no arguments, /usr/lib/systemd/systemd-sysctl applies all directives from configuration files listed in sysctl.d(5)." `--cat-config` — "Copy the contents of config files to standard output. Before each file, the filename is printed as a comment." Examples — "Reset all sysctl settings" 예가 `systemctl restart systemd-sysctl` 입니다. 이 VM 의 `systemd-sysctl.service` 에는 OrbStack 이 `ExecStart=-` 로 실패를 무시하게 하는 drop-in 이 붙어 있습니다. https://www.freedesktop.org/software/systemd/man/latest/systemd-sysctl.service.html
[^kdoc]: Documentation for /proc/sys, Introduction — "Sysctl is a means of configuring certain aspects of the kernel at run-time, and the /proc/sys/ directory is there so that you don't even need special tools to do it!" https://docs.kernel.org/admin-guide/sysctl/index.html
[^ipsysctl]: Linux kernel IP Sysctl, `ip_unprivileged_port_start` — "This is a per-namespace sysctl. It defines the first unprivileged port in the network namespace. ... Default: 1024" `ip_local_port_range` — "Must be greater than or equal to ip_unprivileged_port_start. The default values are 32768 and 60999 respectively." https://docs.kernel.org/networking/ip-sysctl.html
