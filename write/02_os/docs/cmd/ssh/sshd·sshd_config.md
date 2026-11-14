---
title: sshd·sshd_config 참조 시트
tags: [linux, cheatsheet, ssh, sshd, sshd-config, server, reference]
status: draft
source:
  - OpenSSH 9.2p1 sshd(8)·sshd_config(5) (Debian 12 컨테이너의 `man` 원문, manpages.debian.org bookworm)
related:
  - ./ssh.md
  - ./ssh-keygen·ssh-copy-id·ssh-agent.md
  - ./scp·sftp.md
  - ../service/systemctl 함정과 동작 원리.md
  - ../README.md
updated: 2026-11-14
---

# sshd·sshd_config 참조 시트

---

> 서버 쪽 `sshd` 의 설정을 검사하고, 자주 바꾸는 설정을 적용하고, 디버그 실행과 로그로 접속이 왜 거절됐는지 읽는 방법을 컨테이너에서 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `sshd` 는 서버에서 ssh 접속을 받는 데몬이고, 동작은 `sshd_config` 설정 파일이 정합니다.

`sshd` 는 Debian 12 의 `openssh-server` 1:9.2p1 패키지가 `/usr/sbin/sshd` 로 설치하는 외부 바이너리입니다. 출력은 `OpenSSH_9.2, OpenSSL 3.0.22` 로 답하는 컨테이너 `srv` 에서 받았고, 클라이언트는 `cli` 입니다. 이 컨테이너에는 systemd 가 없어 `/usr/sbin/sshd -D -e` 로 직접 띄웠습니다. 서비스 이름과 `ssh.socket` 은 [systemctl 함정과 동작 원리](../service/systemctl%20함정과%20동작%20원리.md) 가 맡으므로 다루지 않습니다.[^sshd-D]

이 시트는 `ssh` 시트의 「실습 준비」 를 이어받습니다. 컨테이너 셋(`srv`·`jump`·`cli`)과 `srv` 의 sshd 가 이미 떠 있어야 하므로 [ssh 접속·config·포트 포워딩 참조 시트](./ssh.md) 의 준비 블록을 먼저 돌려 둡니다. 서버 쪽 인증 파일(`authorized_keys`)은 [ssh-keygen·ssh-copy-id·ssh-agent 참조 시트](./ssh-keygen·ssh-copy-id·ssh-agent.md) 가 다룹니다.



## 핵심 문법

> `sshd` 는 설정 파일을 `-t`·`-T` 로 검사하고, 바꾼 설정은 `SIGHUP` 으로 다시 읽히며, `-d` 로 한 접속을 디버그합니다.

```bash
# sshd 호출 형태 (잘못된 옵션을 주면 unknown option 줄과 판 줄 뒤에 나온다)
usage: sshd [-46DdeiqTtV] [-C connection_spec] [-c host_cert_file]
            [-E log_file] [-f config_file] [-g login_grace_time]
            [-h host_key_file] [-o option] [-p port] [-u len]

# 설정 파일의 문법을 검사한다 (설정 검사하기)
sshd -t

# 실제로 적용되는 설정을 전부 찍는다 (설정 검사하기)
sshd -T

# 접속 조건을 가정해 Match 가 적용된 설정을 찍는다 (조건별 설정 바꾸기)
sshd -T -C user=사용자,host=호스트,addr=주소

# 데몬에 설정을 다시 읽게 한다 (설정 적용하기)
kill -HUP $(cat /run/sshd.pid)

# 디버그 모드로 한 접속만 받는다 (디버그 실행하기)
sshd -d -p 포트
```

### sshd_config 에서 자주 바꾸는 키워드

> 설정 파일은 `키워드 값` 한 줄이 한 설정이고, 처음 읽힌 값이 이깁니다.

```bash
# sshd_config 의 키워드. 이 시트의 예가 쓰는 것만 옮겼다
#   PasswordAuthentication   비밀번호 인증을 허용할지. yes 또는 no
#   PermitRootLogin          root 로 로그인을 허용할지. yes·prohibit-password·no 등
#   PubkeyAuthentication     공개 키 인증을 허용할지
#   AllowUsers               이 목록에 있는 사용자만 로그인을 허용한다
#   Match                    조건(User·Address 등)이 맞는 접속에만 아래 줄들을 적용한다
#   LogLevel                 로그를 얼마나 자세히 남길지. 기본은 INFO
#   StrictModes              로그인 전에 사용자 파일의 권한과 소유자를 검사할지
```



## 종료 코드

> `sshd` 의 man 에는 종료 코드 절이 없어 실측한 값만 싣습니다.[^no-exit]

```bash
# sshd -t   0   설정에 문제가 없다
#           255 설정 파일에 틀린 줄이 있거나, 권한 분리 디렉터리(/run/sshd)가 없다
#           1   호스트 키가 없거나 읽을 수 없다

# 문제가 없으면 아무것도 찍지 않고 0 으로 끝난다
sshd -t; echo $?    # 0
```

틀린 설정이 255 로 끝나는 예는 「틀린 설정 읽기」 에 있습니다.



## 유스케이스

> 예는 앞 예가 만든 상태를 이어 쓰므로 위에서 아래로 차례로 돌립니다.

### 실습 준비

> 서버 쪽 명령은 `srv` 의 root 셸에서, 접속은 `cli` 의 `appuser` 셸에서 돌립니다. `cli` 에는 호스트 키 자동 수락 설정만 더합니다.

별도로 만드는 파일은 없고, 「틀린 설정 읽기」 부터 `/etc/ssh/sshd_config.d/` 에 설정 조각을 만들었다가 지웁니다.

```bash
# 호스트 터미널에서 서버(srv)의 root 셸과 클라이언트(cli)의 appuser 셸을 따로 연다
docker exec -it srv bash
docker exec -it -u appuser cli bash

# 새 호스트 키는 묻지 않고 받는 설정을 둔다
# ssh 시트의 config 예와 같은 줄이라 두 번 들어가도 같은 값이다
#   accept-new   처음 보는 호스트 키는 받고, 바뀐 키는 거부한다
mkdir -p ~/.ssh
printf 'Host *\n  StrictHostKeyChecking accept-new\n' >> ~/.ssh/config

# 권한이 넓으면 ssh 가 config 를 읽지 않는다
chmod 600 ~/.ssh/config

# srv 의 호스트 키를 미리 받아 둔다. 이후 접속은 cli 의 appuser 셸에서 돌린다
ssh srv true
```

### 설정 검사하기

> `sshd -t` 는 설정이 맞는지만 확인하고, `sshd -T` 는 파일 여러 개를 합친 결과를 한 줄씩 찍습니다.

```bash
# srv 에서 설정 문법을 검사한다
#   -t   설정과 호스트 키만 검사하고 끝낸다
sshd -t; echo $?    # 0

# 적용된 설정 중 이 시트가 다루는 것만 본다
#   -T   적용될 설정 전체를 찍는다
#   grep -E   확장 정규식으로 찾는다
sshd -T \
  | grep -E '^(port|passwordauthentication|permitrootlogin|pubkeyauthentication|strictmodes|authorizedkeysfile) '
```

```bash
port 22
permitrootlogin without-password
pubkeyauthentication yes
passwordauthentication no
strictmodes yes
authorizedkeysfile .ssh/authorized_keys .ssh/authorized_keys2
```

`sshd -T` 는 설정에 쓰지 않은 키워드의 기본값도 찍으므로 `PermitRootLogin` 이 없어도 `without-password` 가 나옵니다. man 은 이 값을 `prohibit-password` 의 옛 이름이라고 적습니다.[^root]

### 틀린 설정 읽기

> 설정 조각에 틀린 줄이 있으면 `sshd -t` 가 파일과 줄 번호를 알려 주고 255 로 끝납니다.

```bash
# 키워드 이름을 틀리게 쓴 조각을 만들고 검사한다
echo 'PasswordAuthentications no' > /etc/ssh/sshd_config.d/20-bad.conf
sshd -t; echo $?
```

```bash
/etc/ssh/sshd_config.d/20-bad.conf: line 1: Bad configuration option: PasswordAuthentications
/etc/ssh/sshd_config.d/20-bad.conf: terminating, 1 bad configuration options
255
```

```bash
# 값을 틀리게 쓴 조각도 같다
echo 'PermitRootLogin maybe' > /etc/ssh/sshd_config.d/20-bad.conf
sshd -t; echo $?

# 틀린 조각은 지운다
rm /etc/ssh/sshd_config.d/20-bad.conf
```

```bash
/etc/ssh/sshd_config.d/20-bad.conf line 1: unsupported option "maybe".
255
```

그래서 설정을 적용하기 전에 `sshd -t` 를 먼저 돌려 틀린 줄이 없는지 확인합니다.

### 설정 적용하기

> 설정 조각을 만들고 `SIGHUP` 을 보내면 데몬이 설정을 다시 읽고, 로그에 그 사실이 남습니다.

```bash
# 설정 조각을 만든다. /etc/ssh/sshd_config.d/ 의 *.conf 가 sshd_config 에 포함된다
echo 'MaxAuthTries 3' > /etc/ssh/sshd_config.d/20-tries.conf

# 문법을 검사한 뒤 데몬에 다시 읽게 한다
# /run/sshd.pid 는 데몬이 자기 PID 를 적어 둔 파일이다
sshd -t && kill -HUP $(cat /run/sshd.pid)

# 로그에서 다시 읽었는지, 값이 바뀌었는지 확인한다
grep 'Received SIGHUP' /var/log/sshd.log | tail -1    # Received SIGHUP; restarting.
#   grep -i   대소문자를 가리지 않는다
sshd -T | grep -i '^maxauthtries'    # maxauthtries 3

# 조각을 지우고 되돌린다
rm /etc/ssh/sshd_config.d/20-tries.conf
kill -HUP $(cat /run/sshd.pid)
```

systemd 서버에서는 `kill` 대신 `systemctl reload ssh` 를 씁니다. 이 컨테이너에는 systemd 가 없어 실측하지 않았습니다.

### 비밀번호 인증 거절 확인하기

> `PasswordAuthentication no` 이면 서버가 허용하는 인증 방법이 공개 키뿐이라, 공개 키를 내지 않는 접속은 `Permission denied (publickey)` 로 거절됩니다.

실습 준비가 `PasswordAuthentication no` 를 `/etc/ssh/sshd_config.d/10-lab.conf` 에 넣어 두었으므로 설정은 이미 적용되어 있습니다.

```bash
# cli 에서 공개 키 인증을 끄고 접속한다
#   ssh -o PubkeyAuthentication=no   공개 키 인증을 시도하지 않는다
#   ssh -o BatchMode=yes             비밀번호 등을 묻지 않고 실패한다
ssh -o PubkeyAuthentication=no -o BatchMode=yes srv true; echo $?
```

```bash
appuser@srv: Permission denied (publickey).
255
```

### root 로그인 막기

> `PermitRootLogin no` 를 적용하면 공개 키가 맞는 root 계정도 거절되고, 로그에 거절한 주소가 남습니다.

```bash
# srv 에서 root 의 authorized_keys 에 appuser 의 첫 키를 복사해 root 키 로그인을 가능하게 만든다
#   install -d   디렉터리를 만든다
#   install -m   권한을 정한다
install -d -m 700 /root/.ssh
head -1 /home/appuser/.ssh/authorized_keys > /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys

# cli 에서 root 로 접속한다. 기본값(prohibit-password)은 키 로그인을 허용한다
ssh -o BatchMode=yes root@srv id -un; echo $?    # root / 0
```

```bash
# srv 에서 root 로그인을 막고 적용한다
echo 'PermitRootLogin no' > /etc/ssh/sshd_config.d/20-root.conf
sshd -t && kill -HUP $(cat /run/sshd.pid)
sshd -T | grep -i '^permitrootlogin'    # permitrootlogin no

# cli 에서 같은 접속을 다시 시도한다
ssh -o BatchMode=yes root@srv id -un; echo $?    # root@srv: Permission denied (publickey). / 255
```

```bash
# srv 에서 거절 로그를 읽는다
tail -4 /var/log/sshd.log
```

```bash
Server listening on :: port 22.
ROOT LOGIN REFUSED FROM 192.0.2.20 port 54618
ROOT LOGIN REFUSED FROM 192.0.2.20 port 54618 [preauth]
Connection closed by authenticating user root 192.0.2.20 port 54618 [preauth]
```

```bash
# 원래대로 되돌린다
rm /etc/ssh/sshd_config.d/20-root.conf
kill -HUP $(cat /run/sshd.pid)
rm -rf /root/.ssh
```

클라이언트에는 이유가 없이 `Permission denied (publickey)` 만 보이고, 이유는 서버 로그에 있습니다.

### 접속 사용자 제한하기

> `AllowUsers` 에 이름이 없는 사용자는 공개 키가 맞아도 로그인되지 않습니다.

```bash
# srv 에서 appuser 가 아닌 사용자만 허용한다
echo 'AllowUsers nobody' > /etc/ssh/sshd_config.d/20-allow.conf
sshd -t && kill -HUP $(cat /run/sshd.pid)
sshd -T | grep -i '^allowusers'    # allowusers nobody

# cli 에서 접속한다
ssh -o BatchMode=yes srv hostname; echo $?    # appuser@srv: Permission denied (publickey). / 255
```

```bash
# srv 에서 거절 로그를 읽는다
tail -3 /var/log/sshd.log
```

```bash
Server listening on :: port 22.
User appuser from 192.0.2.20 not allowed because not listed in AllowUsers
Connection closed by invalid user appuser 192.0.2.20 port 59962 [preauth]
```

```bash
# appuser 를 허용하도록 바꾸면 다시 접속된다
echo 'AllowUsers appuser' > /etc/ssh/sshd_config.d/20-allow.conf
sshd -t && kill -HUP $(cat /run/sshd.pid)

# cli 에서 접속한다
ssh -o BatchMode=yes srv hostname; echo $?    # srv / 0

# 조각을 지우고 되돌린다
rm /etc/ssh/sshd_config.d/20-allow.conf
kill -HUP $(cat /run/sshd.pid)
```

### 조건별 설정 바꾸기

> `Match` 아래 줄은 조건이 맞는 접속에만 적용되고, `sshd -T -C` 로 접속 조건을 가정해 결과를 확인합니다.

```bash
# cli(192.0.2.20)에서 오는 접속에만 TCP 포워딩과 X11 포워딩을 끈다
printf '%s\n' \
  'Match Address 192.0.2.20' \
  '  AllowTcpForwarding no' \
  '  X11Forwarding no' \
  > /etc/ssh/sshd_config.d/30-match.conf
sshd -t; echo $?    # 0

# 조건 없이 설정을 찍으면 Match 는 적용되지 않는다
sshd -T | grep -E '^(allowtcpforwarding|x11forwarding)'
```

```bash
x11forwarding yes
allowtcpforwarding yes
```

```bash
# 접속 조건을 가정해 찍는다
#   -C   접속 조건. user·host·addr 를 쉼표로 이어 준다
sshd -T -C user=appuser,host=cli,addr=192.0.2.20 \
  | grep -E '^(allowtcpforwarding|x11forwarding)'
```

```bash
x11forwarding no
allowtcpforwarding no
```

```bash
# 다른 주소에서 오는 접속은 Match 에 걸리지 않는다
sshd -T -C user=appuser,host=jump,addr=192.0.2.30 \
  | grep -E '^(allowtcpforwarding|x11forwarding)'
```

```bash
x11forwarding yes
allowtcpforwarding yes
```

```bash
# 조각을 지우고 되돌린다
rm /etc/ssh/sshd_config.d/30-match.conf
kill -HUP $(cat /run/sshd.pid)
```

### 디버그 실행하기

> `sshd -d` 는 다른 포트에서 접속 하나만 받으며 그 과정을 표준 오류로 모두 찍고 끝납니다.

```bash
# srv 에서 2200 번 포트에 디버그 sshd 를 띄우고 로그를 파일로 모은다
#   -d   디버그 모드. 접속 하나만 처리하고 데몬이 되지 않는다
#   -p   받을 포트. 실제 sshd 와 겹치지 않게 다른 포트를 쓴다
/usr/sbin/sshd -d -p 2200 2> /tmp/dbg.log &

# cli 에서 그 포트로 접속한다
#   ssh -p   접속할 포트
ssh -p 2200 -o BatchMode=yes srv hostname; echo $?
```

```bash
Environment:
  USER=appuser
  LOGNAME=appuser
  HOME=/home/appuser
  PATH=/usr/local/bin:/usr/bin:/bin:/usr/games
  SHELL=/bin/bash
  MOTD_SHOWN=pam
  SSH_CLIENT=192.0.2.20 48688 2200
  SSH_CONNECTION=192.0.2.20 48688 192.0.2.10 2200
srv
0
```

디버그 모드의 서버는 세션 환경 변수 줄(`Environment:`)을 접속한 클라이언트의 화면에도 보냅니다. 포트 번호는 실행마다 다릅니다.

```bash
# 인증 흐름만 골라 읽는다
#   grep -n   줄 번호를 붙인다
#   cut -c    가져올 문자 위치
grep -nE 'Server listening|userauth-request|Accepted|Postponed' /tmp/dbg.log \
  | cut -c1-150
```

```bash
11:Server listening on 0.0.0.0 port 2200.
13:Server listening on :: port 2200.
44:debug1: userauth-request for user appuser service ssh-connection method none [preauth]
49:debug1: userauth-request for user appuser service ssh-connection method publickey [preauth]
57:Accepted key ED25519 SHA256:GV//FQkwXzjOl7NC6M5Kpc70rfWw6cOWytBddPHzzIk found at /home/appuser/.ssh/authorized_keys:1
59:Postponed publickey for appuser from 192.0.2.20 port 48688 ssh2 [preauth]
60:debug1: userauth-request for user appuser service ssh-connection method publickey-hostbound-v00@openssh.com [preauth]
67:Accepted key ED25519 SHA256:GV//FQkwXzjOl7NC6M5Kpc70rfWw6cOWytBddPHzzIk found at /home/appuser/.ssh/authorized_keys:1
71:Accepted publickey for appuser from 192.0.2.20 port 48688 ssh2: ED25519 SHA256:GV//FQkwXzjOl7NC6M5Kpc70rfWw6cOWytBddPHzzIk
```

줄 번호·포트·지문은 실행마다 다르고, 전체 로그는 이 접속에서 100줄이 넘어 위처럼 줄여 적었습니다. `Accepted key ... found at ...authorized_keys:1` 은 서버가 `authorized_keys` 몇째 줄의 키와 맞췄는지 알려 줍니다.

### 서버 로그 읽기

> 기본 로그 수준(`INFO`)은 성공한 접속과 거절한 접속의 줄만 남기고, 어느 키를 냈는지는 `VERBOSE` 에서 나옵니다.

```bash
# srv 에서 로그 수준을 올리고 적용한다
echo 'LogLevel VERBOSE' > /etc/ssh/sshd_config.d/20-log.conf
sshd -t && kill -HUP $(cat /run/sshd.pid)

# cli 에서 접속한 뒤 srv 에서 마지막 로그를 본다
ssh -o BatchMode=yes srv true
tail -6 /var/log/sshd.log | cut -c1-200
```

```bash
Accepted key ED25519 SHA256:GV//FQkwXzjOl7NC6M5Kpc70rfWw6cOWytBddPHzzIk found at /home/appuser/.ssh/authorized_keys:1
Accepted publickey for appuser from 192.0.2.20 port 50936 ssh2: ED25519 SHA256:GV//FQkwXzjOl7NC6M5Kpc70rfWw6cOWytBddPHzzIk
User child is on pid 5347
Starting session: command for appuser from 192.0.2.20 port 50936 id 0
Received disconnect from 192.0.2.20 port 50936:11: disconnected by user
Disconnected from user appuser 192.0.2.20 port 50936
```

```bash
# VERBOSE 조각을 지우고 기본 수준으로 되돌린다
rm /etc/ssh/sshd_config.d/20-log.conf
kill -HUP $(cat /run/sshd.pid)
```

```bash
# 서버에 등록하지 않은 키와 없는 사용자로 접속해 본다. cli 에서 돌린다
#   ssh -i                      쓸 개인 키 파일
#   ssh -o IdentitiesOnly=yes   -i 로 준 키만 쓴다
ssh \
  -i ~/.ssh/id_stray \
  -o IdentitiesOnly=yes \
  -o BatchMode=yes \
  srv true
ssh -o BatchMode=yes nouser@srv true

# srv 에서 거절 줄을 본다
tail -4 /var/log/sshd.log
```

```bash
Server listening on :: port 22.
Connection closed by authenticating user appuser 192.0.2.20 port 43658 [preauth]
Invalid user nouser from 192.0.2.20 port 43662
Connection closed by invalid user nouser 192.0.2.20 port 43662 [preauth]
```

등록하지 않은 키의 거절은 `Connection closed by authenticating user` 한 줄뿐이고 이유는 적히지 않습니다. 없는 사용자는 `Invalid user` 가 먼저 나옵니다.

### 실습 정리

> 「주의사항과 동작 원리」 의 예도 srv·jump 의 설정을 건드리므로 그 절까지 마친 뒤 돌립니다. 컨테이너와 네트워크는 `ssh` 시트의 「실습 정리」 가 지웁니다.

```bash
# srv 에서 이 시트가 만든 파일을 지운다
rm -f /tmp/dbg.log /etc/ssh/sshd_config.d/2*.conf /etc/ssh/sshd_config.d/3*.conf
kill -HUP $(cat /run/sshd.pid)
```



## 주의사항과 동작 원리

### 설정 조각의 우선순위

> `sshd_config` 맨 위가 `/etc/ssh/sshd_config.d/*.conf` 를 포함하므로, 같은 키워드를 파일 끝에 덧붙여도 조각의 값이 이깁니다.

```bash
# 조각이 no 로 정한 값을 sshd_config 끝에서 yes 로 덮으려 한다
echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config
sshd -T | grep -i '^passwordauthentication'    # passwordauthentication no

# 덧붙인 줄을 지운다
#   sed -i   파일을 제자리에서 고친다
sed -i '$d' /etc/ssh/sshd_config
```

```bash
# 포함 줄의 위치를 확인한다
grep -n '^Include' /etc/ssh/sshd_config    # 12:Include /etc/ssh/sshd_config.d/*.conf
```

처음 읽힌 값을 쓰는 규칙은 `ssh_config` 와 같습니다. 설정이 먹지 않으면 `sshd -T` 로 최종 값을 먼저 확인하고, 값을 정한 파일은 `/etc/ssh/sshd_config.d/` 를 먼저 봅니다.[^first]

### 권한 분리 디렉터리가 없을 때

> `/run/sshd` 가 없으면 `sshd -t` 가 설정은 멀쩡한데도 255 로 끝납니다.

```bash
# jump 에서 디렉터리를 지우고 검사한다. 호스트 터미널에서 돌린다
docker exec jump bash -c 'rmdir /run/sshd; sshd -t; echo $?'    # Missing privilege separation directory: /run/sshd / 255

# 다시 만들면 통과한다
docker exec jump bash -c '
  install -d -m 755 /run/sshd
  sshd -t; echo $?'    # 0
```

이 디렉터리가 없는 컨테이너에서는 직접 만들어야 하고, 이 실습의 준비 블록이 `install -d -m 755 /run/sshd` 를 하는 이유입니다.

### 거절 이유의 위치

> 거절의 모든 이유는 클라이언트에 `Permission denied (publickey)` 한 줄로 합쳐지고, 이유는 서버 로그에만 있습니다.

`PermitRootLogin`·`AllowUsers`·`StrictModes` 위반이 모두 같은 메시지였으므로, 서버 로그가 없으면 `ssh -v` 로 낸 키를 보고 설정을 하나씩 확인합니다. `StrictModes` 위반의 로그는 [ssh-keygen·ssh-copy-id·ssh-agent 참조 시트](./ssh-keygen·ssh-copy-id·ssh-agent.md) 의 「서버의 .ssh 권한」 에 있습니다.



## 관련 문서

> 서버 설정이 닿는 클라이언트 쪽 명령과 서비스 관리를 이어서 볼 수 있습니다.

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [ssh 접속·config·포트 포워딩 참조 시트](./ssh.md) — 이 시트가 이어받는 「실습 준비」 와 클라이언트 쪽 `ssh_config`
- [ssh-keygen·ssh-copy-id·ssh-agent 참조 시트](./ssh-keygen·ssh-copy-id·ssh-agent.md) — 서버가 읽는 `authorized_keys` 를 만드는 방법
- [scp·sftp 참조 시트](./scp·sftp.md) — 서버의 `Subsystem sftp` 를 쓰는 파일 전송
- [systemctl 함정과 동작 원리](../service/systemctl%20함정과%20동작%20원리.md) — ssh 서비스 이름과 `ssh.socket`
- [TLS 는 키를 어떻게 안전하게 나누는가 — 핸드셰이크·세션 인증·HTTPS·SSH](../../../book/ostep_operating-systems-three-easy-pieces/45-02.TLS%20는%20키를%20어떻게%20안전하게%20나누는가%20—%20핸드셰이크·세션%20인증·HTTPS·SSH.md) — 호스트 키와 사용자 인증이 하는 일



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- OpenSSH 9.2p1(`openssh-server` 1:9.2p1-2+deb12u10)의 `sshd` 사용법·`man sshd`·`man sshd_config` 원문 — Debian 12 컨테이너 셋에서 2026-11-14 확인
- [sshd(8)](https://manpages.debian.org/bookworm/openssh-server/sshd.8.en.html) — 옵션 뜻 원문
- [sshd_config(5)](https://manpages.debian.org/bookworm/openssh-server/sshd_config.5.en.html) — 키워드 뜻 원문

[^sshd-D]: sshd(8) — "-D When this option is specified, sshd will not detach and does not become a daemon. This allows easy monitoring of sshd." "-e Write debug logs to standard error instead of the system log." <https://manpages.debian.org/bookworm/openssh-server/sshd.8.en.html>
[^no-exit]: sshd(8) 의 man 에는 종료 코드 절이 없습니다. 아래 값은 컨테이너에서 해당 호출을 돌려 `echo $?` 로 읽은 것입니다.
[^root]: sshd_config(5) — "The default is prohibit-password." "If this option is set to prohibit-password (or its deprecated alias, without-password), password and keyboard-interactive authentication are disabled for root." 이 판의 `sshd -T` 는 이 값을 `without-password` 로 찍습니다. <https://manpages.debian.org/bookworm/openssh-server/sshd_config.5.en.html>
[^first]: sshd_config(5) — "For each keyword, the first obtained value will be used." "Include the specified configuration file(s)." <https://manpages.debian.org/bookworm/openssh-server/sshd_config.5.en.html>
