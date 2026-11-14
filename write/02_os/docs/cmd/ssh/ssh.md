---
title: ssh 접속·config·포트 포워딩 참조 시트
tags: [linux, cheatsheet, ssh, openssh, ssh-config, port-forwarding, reference]
status: draft
source:
  - OpenSSH 9.2p1 ssh(1)·ssh_config(5) (Debian 12 컨테이너의 `man ssh`·`man ssh_config` 원문, manpages.debian.org bookworm)
related:
  - ./ssh-keygen·ssh-copy-id·ssh-agent.md
  - ./scp·sftp.md
  - ./sshd·sshd_config.md
  - ../README.md
updated: 2026-11-14
---

# ssh 접속·config·포트 포워딩 참조 시트

---

> 원격 접속과 원격 명령 실행, `~/.ssh/config` 설정, 점프 호스트, 포트 포워딩, 접속 재사용을 컨테이너 세 개로 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `ssh` 는 원격 호스트에 암호화된 연결을 열어 셸이나 명령을 실행하고, 같은 연결로 TCP 포트를 중계합니다.

`ssh` 는 Debian 12 의 `openssh-client` 1:9.2p1 패키지가 `/usr/bin/ssh` 로 설치하는 외부 바이너리입니다. 출력은 `ssh -V` 가 `OpenSSH_9.2p1 Debian-2+deb12u10, OpenSSL 3.0.22` 로 답하는 Debian 12 컨테이너 셋에서 받았습니다. 서버는 `srv`, 점프 호스트는 `jump`, 클라이언트는 `cli` 입니다. Debian 은 `/etc/ssh/ssh_config` 에 `HashKnownHosts yes` 같은 값을 미리 넣어 두어 upstream 기본값과 다르게 동작합니다.[^env]

키·에이전트·파일 전송·서버 쪽 설정은 같은 폴더의 다른 시트가 맡습니다. 그 시트들은 이 시트의 「실습 준비」 를 이어받으니 먼저 돌려 둡니다.



## 핵심 문법

> `ssh` 는 목적지(`[user@]host`)로 접속 대상을 고르고, 목적지 뒤의 명령으로 원격에서 할 일을 정하며, 옵션과 `~/.ssh/config` 가 접속 방식을 바꿉니다.

```bash
# 호출 형태. ssh 에는 --help 가 없고 인자 없이 부르면 나오는 사용법이다
usage: ssh [-46AaCfGgKkMNnqsTtVvXxYy] [-B bind_interface]
           [-b bind_address] [-c cipher_spec] [-D [bind_address:]port]
           [-E log_file] [-e escape_char] [-F configfile] [-I pkcs11]
           [-i identity_file] [-J [user@]host[:port]] [-L address]
           [-l login_name] [-m mac_spec] [-O ctl_cmd] [-o option] [-p port]
           [-Q query_option] [-R address] [-S ctl_path] [-W host:port]
           [-w local_tun[:remote_tun]] destination [command [argument ...]]

# 로그인 셸을 연다 (처음 접속과 호스트 키 확인)
ssh 호스트

# 원격에서 명령 하나만 실행하고 돌아온다 (원격 명령 실행하기)
ssh 호스트 명령

# 포트·사용자·키를 정해 접속한다 (접속 대상과 키 고르기)
ssh \
  -p 포트 \
  -l 사용자 \
  -i 키파일 \
  호스트

# 적용될 설정을 접속 없이 확인한다 (옵션 넘기기와 설정 확인)
ssh -G 호스트

# 점프 호스트를 거쳐 접속한다 (점프 호스트 거치기)
ssh -J 점프호스트 호스트

# 접속 하나를 여러 명령이 나눠 쓴다 (접속 재사용하기)
ssh -O check 호스트

# 포트를 중계한다 (포트 포워딩)
ssh -N -L 로컬포트:대상:대상포트 호스트
ssh -N -R 원격포트:대상:대상포트 호스트
ssh -N -D 포트 호스트
```

### config 에서 자주 쓰는 키워드

> 같은 이름의 명령줄 옵션이 있으면 명령줄이 이깁니다.

```bash
# ~/.ssh/config 의 키워드. Host 줄이 이후 줄들의 적용 범위를 정한다
#   Host           아래 줄들을 적용할 호스트 이름 패턴. 접속할 때 입력한 이름과 맞춘다
#   HostName       실제로 접속할 이름이나 주소
#   User           로그인할 사용자
#   Port           접속할 포트
#   IdentityFile   쓸 개인 키 파일. 여러 번 쓰면 시도할 키가 더해진다
#   IdentitiesOnly yes 면 에이전트가 더 많은 키를 내밀어도 설정한 키만 쓴다
#   ProxyJump      거쳐 갈 점프 호스트
#   ControlMaster  접속 재사용. auto 는 master 가 없으면 만들고 있으면 붙는다
#   ControlPath    제어 소켓 경로
#   ControlPersist 첫 접속이 끝난 뒤 master 를 백그라운드에 남겨 둔다
#                  시간(초)을 주면 붙은 접속 없이 그만큼 지나면 끝난다
```

여러 줄이 같은 키워드를 정하면 처음 읽힌 값이 쓰입니다.[^first]



## 종료 코드

> `ssh` 는 원격 명령의 종료 코드를 그대로 돌려주고, 접속·인증처럼 `ssh` 자체의 오류는 255 로 끝냅니다.[^exit]

아래 예는 호스트 키 확인 전에 실패하는 호출이라 「실습 준비」 만 마치면 바로 돌아갑니다. 원격 명령의 코드를 그대로 받는 예는 「원격 명령 실행하기」 에 있습니다.

```bash
# 원격 명령의 종료 코드   원격 명령을 실행했으면 그 코드가 그대로 나온다
# 255                    ssh 자체의 오류 (접속하지 못함, 인증 실패, 잘못된 사용)

# 인자 없이 부르면 사용법을 찍고 255 로 끝난다
ssh; echo $?
```

```bash
usage: ssh [-46AaCfGgKkMNnqsTtVvXxYy] [-B bind_interface]
           [-b bind_address] [-c cipher_spec] [-D [bind_address:]port]
           [-E log_file] [-e escape_char] [-F configfile] [-I pkcs11]
           [-i identity_file] [-J [user@]host[:port]] [-L address]
           [-l login_name] [-m mac_spec] [-O ctl_cmd] [-o option] [-p port]
           [-Q query_option] [-R address] [-S ctl_path] [-W host:port]
           [-w local_tun[:remote_tun]] destination [command [argument ...]]
255
```

```bash
# 이름을 풀지 못하면 접속 전에 255 로 끝난다
ssh nosuchhost true; echo $?    # ssh: Could not resolve hostname nosuchhost: Name or service not known / 255

# 서버가 그 포트에서 듣지 않으면 연결이 거절되어 255 로 끝난다
#   -p   접속할 원격 포트
ssh -p 2223 srv true; echo $?    # ssh: connect to host srv port 2223: Connection refused / 255
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다.



## 유스케이스

> 예는 앞 예가 만든 상태를 이어 쓰므로 위에서 아래로 차례로 돌립니다.

### 실습 준비

> 아래 블록은 컨테이너 셋과 키·sshd 를 한 번에 만들고, 예의 명령은 `cli` 컨테이너의 `appuser` 셸에서 돌립니다.

다른 세 시트도 이 블록을 이어받습니다. `docker exec` 로 시작하는 줄은 호스트 터미널에서, 나머지는 `docker exec -it -u appuser cli bash` 로 연 셸에서 돌립니다.

```bash
# 문서용 대역 네트워크에 컨테이너 셋을 띄운다. srv 가 서버, jump 가 점프 호스트, cli 가 클라이언트다
docker network create --subnet 192.0.2.0/24 sshlab
docker run -d --rm --name srv --hostname srv \
  --network sshlab --ip 192.0.2.10 debian:12 sleep infinity
docker run -d --rm --name jump --hostname jump \
  --network sshlab --ip 192.0.2.30 debian:12 sleep infinity
docker run -d --rm --name cli --hostname cli \
  --network sshlab --ip 192.0.2.20 debian:12 sleep infinity

# 셋 모두에 OpenSSH 와 일반 사용자 appuser 를 만든다. curl·python3·ss 는 포워딩 예에서 쓴다
for c in srv jump cli; do
  docker exec "$c" bash -c '
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -qq > /dev/null
    apt-get install -y -qq \
      openssh-client openssh-server curl python3 iproute2 \
      > /dev/null 2>&1
    useradd -m -s /bin/bash appuser'
done

# cli 의 appuser 에 키 셋을 만든다. id_stray 는 어느 서버에도 등록하지 않는다
for k in id_ed25519 id_work id_stray; do
  docker exec -u appuser cli \
    ssh-keygen \
      -q \
      -t ed25519 \
      -N '' \
      -C "$k@cli" \
      -f "/home/appuser/.ssh/$k"
done

# id_ed25519·id_work 의 공개 키를 srv·jump 의 authorized_keys 에 넣는다
for h in srv jump; do
  docker exec cli bash -c 'cat /home/appuser/.ssh/{id_ed25519,id_work}.pub' \
    | docker exec -i -u appuser "$h" bash -c '
        install -d -m 700 ~/.ssh
        cat > ~/.ssh/authorized_keys
        chmod 600 ~/.ssh/authorized_keys'
done

# srv·jump 에서 sshd 를 띄운다. 비밀번호 인증은 끄고, 로그는 /var/log/sshd.log 로 모은다
for h in srv jump; do
  docker exec "$h" bash -c '
    echo "PasswordAuthentication no" > /etc/ssh/sshd_config.d/10-lab.conf
    install -d -m 755 /run/sshd'
  docker exec -d "$h" bash -c '
    exec /usr/sbin/sshd -D -e 2> /var/log/sshd.log'
done

# srv 에는 -p 예를 위한 2222 번 sshd 와 포워딩 예를 위한 웹 서버(127.0.0.1:8080)를 더 띄운다
docker exec srv /usr/sbin/sshd -p 2222 -o PidFile=/run/sshd2.pid
docker exec srv bash -c '
  mkdir /srv/www
  echo "hello from srv" > /srv/www/index.html'
docker exec -d srv \
  python3 -m http.server 8080 \
    --bind 127.0.0.1 \
    --directory /srv/www

# cli 에는 -R 예를 위한 웹 서버(127.0.0.1:8081)를 띄운다
docker exec cli bash -c '
  mkdir /srv/www
  echo "hello from cli" > /srv/www/index.html'
docker exec -d cli \
  python3 -m http.server 8081 \
    --bind 127.0.0.1 \
    --directory /srv/www
```

### 처음 접속과 호스트 키 확인

> 처음 보는 서버에 접속하면 `ssh` 가 호스트 키 지문을 보여 주고, `yes` 로 받아들인 키는 `~/.ssh/known_hosts` 에 저장됩니다.

```bash
# srv 에서 hostname 을 실행한다. 처음이라 지문을 묻고, yes 를 입력하면 이어진다
ssh srv hostname
```

```bash
The authenticity of host 'srv (192.0.2.10)' can't be established.
ED25519 key fingerprint is SHA256:jWgI7oaTAa1ojMbc5HKzss5ORspZsYNszr8NKmHLEXk.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'srv' (ED25519) to the list of known hosts.
srv
```

```bash
# 서버가 가진 호스트 키의 지문과 대조한다 (호스트 터미널에서). 위 지문과 같으면 서버가 맞다
docker exec srv ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub    # 256 SHA256:jWgI7oaTAa1ojMbc5HKzss5ORspZsYNszr8NKmHLEXk root@srv (ED25519)

# 한 번 접속했는데 known_hosts 는 세 줄이고 이름은 해시로 적혀 있다
wc -l < ~/.ssh/known_hosts    # 3
awk '{print $2}' ~/.ssh/known_hosts
```

```bash
ssh-ed25519
ssh-rsa
ecdsa-sha2-nistp256
```

```bash
# 두 번째부터는 묻지 않는다
ssh srv hostname    # srv
```

한 줄이 아니라 세 줄이 생기는 이유는 「`known_hosts` 의 세 줄」 에 있습니다.

### 원격 명령 실행하기

> 목적지 뒤에 명령을 적으면 셸을 열지 않고 그 명령만 실행한 뒤 결과와 종료 코드를 돌려줍니다.

```bash
# 작은따옴표 안의 $HOSTNAME 과 pwd 는 원격에서 풀린다
ssh srv 'echo $HOSTNAME; pwd'

# 큰따옴표 안의 $HOSTNAME 은 로컬 셸이 먼저 풀어 버린다
ssh srv "echo local: $HOSTNAME"    # local: cli

# 원격 명령의 종료 코드가 ssh 의 종료 코드가 된다
ssh srv 'exit 3'; echo $?    # 3

# 로컬의 출력을 원격 명령의 입력으로 넘긴다
echo hello | ssh srv 'cat > /tmp/in.txt; wc -c /tmp/in.txt'    # 6 /tmp/in.txt
```

```bash
srv
/home/appuser
```

```bash
# 명령을 주면 터미널을 할당하지 않는다. tty 가 필요한 프로그램에는 -t 를 붙인다
#   -t   의사 터미널을 강제로 할당한다
ssh srv tty    # not a tty
ssh -t srv tty
```

```bash
/dev/pts/0
Connection to srv closed.
```

### 접속 대상과 키 고르기

> 포트는 `-p`, 사용자는 `-l` 이나 `user@`, 쓸 개인 키는 `-i` 로 정합니다.

```bash
# srv 의 2222 번 포트에 접속한다
ssh -p 2222 srv hostname    # srv

# 사용자는 -l 로도 user@host 로도 정한다
#   -l   로그인할 원격 사용자
ssh -l appuser srv whoami    # appuser
ssh appuser@srv whoami    # appuser
```

```bash
# 키를 -i 로 정하고, 어떤 키를 시도했는지 -v 로 본다
#   -i   공개 키 인증에 쓸 개인 키 파일
#   -v   디버그 메시지를 찍는다
#   grep -E   확장 정규식으로 찾는다
ssh -i ~/.ssh/id_work -v srv true 2>&1 | grep -E 'Will attempt|Offering'
```

```bash
debug1: Will attempt key: /home/appuser/.ssh/id_work ED25519 SHA256:d/RESSCWO9IsONjBbHZGElcufXWhkDZPwAkz8JnACyI explicit
debug1: Offering public key: /home/appuser/.ssh/id_work ED25519 SHA256:d/RESSCWO9IsONjBbHZGElcufXWhkDZPwAkz8JnACyI explicit
```

```bash
# 서버에 등록하지 않은 키를 주면 인증이 거절된다. 이때도 -i 키만 시도했다
ssh -i ~/.ssh/id_stray -v srv true 2>&1 \
  | grep -E 'Will attempt|Offering|Permission'
```

```bash
debug1: Will attempt key: /home/appuser/.ssh/id_stray ED25519 SHA256:9jUj+rZit21F0APxq0h9g1EHlb1ius6h6WuFKe15OsU explicit
debug1: Offering public key: /home/appuser/.ssh/id_stray ED25519 SHA256:9jUj+rZit21F0APxq0h9g1EHlb1ius6h6WuFKe15OsU explicit
appuser@srv: Permission denied (publickey).
```

없는 파일을 `-i` 로 주면 어떻게 되는지는 「`-i` 지정 키와 기본 키」 에 있습니다.

### 옵션 넘기기와 설정 확인

> `-o` 는 설정 파일 키워드를 명령줄로 넘기고, `-G` 는 접속하지 않고 적용될 설정을 보여 줍니다.

```bash
# 응답이 없는 주소는 2초 뒤 포기한다. BatchMode 는 묻는 일을 모두 끈다
#   -o   설정 파일 형식의 옵션을 명령줄로 넘긴다
ssh -o BatchMode=yes -o ConnectTimeout=2 192.0.2.99 hostname    # ssh: connect to host 192.0.2.99 port 22: Connection timed out
echo $?    # 255

# 접속하지 않고 이 호스트에 적용될 설정만 본다
#   -G   Host·Match 를 평가한 설정을 찍고 끝낸다
ssh -G srv | grep -E '^(user|hostname|port) '
```

```bash
user appuser
hostname srv
port 22
```

```bash
# -o 로 준 값이 -G 결과에 반영된다
ssh -o Port=2222 -G srv | grep '^port '    # port 2222

# 접속 과정에서 어떤 주소·사용자·키를 썼는지 -v 로 본다
ssh -v srv true 2>&1 \
  | grep -E 'Connecting|Authenticating|Offering|Authenticated'
```

```bash
debug1: Connecting to srv [192.0.2.10] port 22.
debug1: Authenticating to srv:22 as 'appuser'
debug1: Offering public key: /home/appuser/.ssh/id_ed25519 ED25519 SHA256:GV//FQkwXzjOl7NC6M5Kpc70rfWw6cOWytBddPHzzIk
Authenticated to srv ([192.0.2.10]:22) using "publickey".
```

### 접속 실패 메시지 읽기

> 접속 실패는 메시지 문구로 이름 풀이, 포트, 인증 중 어디서 막혔는지 가릅니다.

```bash
# 이름을 풀지 못한다 (DNS 나 hosts 에 없는 이름)
ssh nosuchhost hostname    # ssh: Could not resolve hostname nosuchhost: Name or service not known

# 포트에서 듣는 프로세스가 없다 (sshd 가 꺼졌거나 포트가 다르다)
ssh -p 2223 srv hostname    # ssh: connect to host srv port 2223: Connection refused

# 접속은 됐지만 서버가 키를 받아 주지 않는다. root 의 authorized_keys 에는 우리 키가 없다
ssh -o BatchMode=yes root@srv hostname    # root@srv: Permission denied (publickey).
```

```bash
# 인증 단계의 시도를 보면 서버가 받는 방식(publickey)과 내민 키를 알 수 있다
ssh -v -o BatchMode=yes root@srv hostname 2>&1 \
  | grep -E 'Offering|Authentications that|Permission'
```

```bash
debug1: Authentications that can continue: publickey
debug1: Offering public key: /home/appuser/.ssh/id_ed25519 ED25519 SHA256:GV//FQkwXzjOl7NC6M5Kpc70rfWw6cOWytBddPHzzIk
debug1: Authentications that can continue: publickey
root@srv: Permission denied (publickey).
```

### config 로 접속 이름 만들기

> `~/.ssh/config` 에 `Host` 별칭을 적어 두면 긴 옵션 없이 이름만으로 접속합니다.

```bash
# Host 블록마다 이후 줄들이 그 이름에만 적용된다. 마지막 Host * 는 모든 호스트의 기본값이다
cat > ~/.ssh/config << 'CFG'
Host web
    HostName srv
    User appuser
    IdentityFile ~/.ssh/id_work
    IdentitiesOnly yes

Host alt
    HostName srv
    Port 2222

Host inner
    HostName srv
    ProxyJump jump

Host fast
    HostName srv
    ControlMaster auto
    ControlPath ~/.ssh/cm-%r@%h:%p
    ControlPersist 60

Host *
    StrictHostKeyChecking accept-new
    ServerAliveInterval 30
CFG

# config 는 소유자만 쓸 수 있어야 한다
chmod 600 ~/.ssh/config
```

```bash
# web 은 srv 로, alt 는 srv 의 2222 번으로 간다
ssh web hostname    # srv
ssh alt hostname    # srv

# 별칭이 펼쳐진 결과를 본다. Host * 의 값도 함께 붙는다
ssh -G web \
  | grep -E '^(user|hostname|port|identityfile|identitiesonly|serveraliveinterval) '
```

```bash
user appuser
hostname srv
port 22
identitiesonly yes
serveraliveinterval 30
identityfile ~/.ssh/id_work
```

```bash
# 명령줄 옵션이 설정 파일을 이긴다
ssh -p 2222 -G web | grep '^port '    # port 2222
```

### 점프 호스트 거치기

> `-J` 나 `ProxyJump` 는 점프 호스트에 접속한 뒤 거기서 목적지로 연결을 이어 줍니다.

```bash
# jump 를 거쳐 srv 에 접속한다. 처음 보는 jump 의 호스트 키는 Host * 의 accept-new 가 받는다
#   -J   거쳐 갈 점프 호스트
ssh -J jump srv 'echo $SSH_CONNECTION'
```

```bash
Warning: Permanently added 'jump' (ED25519) to the list of known hosts.
192.0.2.30 47802 192.0.2.10 22
```

```bash
# config 의 inner 도 같은 길이다. srv 가 본 접속 주소가 jump(192.0.2.30)다
ssh inner 'echo $SSH_CONNECTION'    # 192.0.2.30 47808 192.0.2.10 22

# 직접 접속하면 cli(192.0.2.20)로 보인다
ssh srv 'echo $SSH_CONNECTION'    # 192.0.2.20 60628 192.0.2.10 22

# -v 로 보면 ssh 가 jump 에 -W 접속을 따로 열어 srv:22 로 잇는다
ssh -v inner true 2>&1 | grep -E 'Executing proxy|Authenticated to'
```

```bash
debug1: Executing proxy command: exec ssh -v -W '[srv]:22' jump
Authenticated to jump ([192.0.2.30]:22) using "publickey".
Authenticated to srv (via proxy) using "publickey".
```

### 접속 재사용하기

> `ControlMaster auto` 는 첫 접속이 소켓을 남기고, 이후 접속은 그 소켓으로 인증 없이 붙습니다.

```bash
# 첫 접속이 master 가 되어 제어 소켓을 만든다
ssh fast hostname    # srv
ls ~/.ssh | grep cm-    # cm-appuser@srv:22

# master 가 살아 있는지 묻는다
#   -O   master 프로세스에 명령(check, exit 등)을 보낸다
ssh -O check fast    # Master running (pid=4230)

# 두 번째 접속은 새로 인증하지 않고 master 에 붙는다
ssh -v fast true 2>&1 | grep -E 'auto-mux'    # debug1: auto-mux: Trying existing master

# master 를 내린다. 소켓이 사라지고 check 는 255 로 실패한다
ssh -O exit fast    # Exit request sent.
ls ~/.ssh | grep cm-; echo $?    # 1
ssh -O check fast; echo $?    # Control socket connect(/home/appuser/.ssh/cm-appuser@srv:22): No such file or directory / 255
```

### 포트 포워딩

> `-L` 은 로컬 포트를 원격 쪽 주소로, `-R` 은 원격 포트를 로컬 쪽 주소로, `-D` 는 로컬 SOCKS 프록시로 중계합니다.[^fwd]

```bash
# srv 의 127.0.0.1:8080 웹 서버를 cli 의 9000 번 포트로 끌어온다
#   -f   명령을 실행하기 직전에 백그라운드로 간다
#   -N   원격 명령을 실행하지 않는다 (중계만 한다)
#   -M   접속 재사용의 master 가 된다
#   -S   제어 소켓 경로를 정한다
#   -L   로컬 포트:srv 가 본 대상:대상 포트
ssh \
  -f \
  -N \
  -M \
  -S /tmp/ctl-srv \
  -L 9000:127.0.0.1:8080 \
  srv

# 9000 번이 열렸다. -L 은 루프백 IPv4 와 IPv6 에 모두 연다
#   ss -l   대기 중인 소켓만 보인다
#   ss -t   TCP 소켓만 보인다
#   ss -n   포트를 이름 대신 숫자로 보인다
ss -ltn | grep 9000
```

```bash
LISTEN 0      128        127.0.0.1:9000       0.0.0.0:*
LISTEN 0      128            [::1]:9000          [::]:*
```

```bash
# 터널 너머의 웹 서버가 응답한다
#   curl -s   진행 표시와 오류 메시지를 숨긴다
curl -s http://127.0.0.1:9000    # hello from srv

# srv 의 8080 은 루프백에만 묶여 있어 터널 없이는 닿지 않는다 (curl 의 종료 코드 7)
#   curl -m   응답을 기다리는 최대 시간(초)
curl -s -m 2 http://srv:8080; echo $?    # 7

# master 에 물어 상태를 보고, 끝나면 내린다. 포트도 닫힌다
ssh -S /tmp/ctl-srv -O check srv    # Master running (pid=4241)
ssh -S /tmp/ctl-srv -O exit srv    # Exit request sent.
ss -ltn | grep 9000; echo $?    # 1
```

```bash
# cli 의 127.0.0.1:8081 웹 서버를 srv 의 9100 번 포트로 내보낸다 (리버스 터널)
#   -R   원격 포트:cli 가 본 대상:대상 포트
ssh \
  -f \
  -N \
  -M \
  -S /tmp/ctl-srv \
  -R 9100:127.0.0.1:8081 \
  srv

# srv 쪽에서 9100 번으로 curl 하면 cli 의 서버가 응답한다
ssh srv 'curl -s http://127.0.0.1:9100'    # hello from cli
ssh srv 'ss -ltn | grep 9100'
ssh -S /tmp/ctl-srv -O exit srv    # Exit request sent.
```

```bash
LISTEN 0      128        127.0.0.1:9100       0.0.0.0:*
LISTEN 0      128            [::1]:9100          [::]:*
```

```bash
# cli 의 1080 번을 SOCKS 프록시로 연다. 목적지 이름은 srv 쪽에서 풀리므로 127.0.0.1 이 srv 의 루프백이다
#   -D   로컬 SOCKS 프록시 포트
ssh \
  -f \
  -N \
  -M \
  -S /tmp/ctl-srv \
  -D 1080 \
  srv

# SOCKS5 프록시로 보내고, 목적지 이름 풀이도 프록시 쪽에 맡긴다
#   curl --socks5-hostname   SOCKS5 프록시 주소
curl -s --socks5-hostname 127.0.0.1:1080 http://127.0.0.1:8080    # hello from srv
ssh -S /tmp/ctl-srv -O exit srv    # Exit request sent.
```

### 실습 정리

> 같은 실습 환경을 쓰는 다른 세 시트와 이 시트의 「주의사항과 동작 원리」 까지 마친 뒤 돌립니다.

```bash
# 컨테이너를 멈추면 --rm 으로 지워진다. 네트워크도 지운다 (호스트 터미널에서)
docker stop srv jump cli
docker network rm sshlab
```



## 주의사항과 동작 원리

### `-i` 지정 키와 기본 키

> `-i` 로 키를 주면 `ssh` 는 그 키만 시도하고 `~/.ssh/id_ed25519` 같은 기본 키는 시도하지 않습니다.

```bash
# -i 로 준 키가 서버에 없으면 기본 키가 있어도 인증이 거절된다. 위 「접속 대상과 키 고르기」 의 id_stray 가 그 경우다
ssh -i ~/.ssh/id_stray srv hostname    # appuser@srv: Permission denied (publickey).

# 없는 파일을 주면 경고만 하고 기본 키 목록으로 돌아가 접속에 성공한다
ssh -i /nonexistent -v srv true 2>&1 \
  | grep -E 'not accessible|Will attempt|Offering'
```

```bash
Warning: Identity file /nonexistent not accessible: No such file or directory.
debug1: Will attempt key: /home/appuser/.ssh/id_rsa 
debug1: Will attempt key: /home/appuser/.ssh/id_ecdsa 
debug1: Will attempt key: /home/appuser/.ssh/id_ecdsa_sk 
debug1: Will attempt key: /home/appuser/.ssh/id_ed25519 ED25519 SHA256:GV//FQkwXzjOl7NC6M5Kpc70rfWw6cOWytBddPHzzIk
debug1: Will attempt key: /home/appuser/.ssh/id_ed25519_sk 
debug1: Will attempt key: /home/appuser/.ssh/id_xmss 
debug1: Will attempt key: /home/appuser/.ssh/id_dsa 
debug1: Offering public key: /home/appuser/.ssh/id_ed25519 ED25519 SHA256:GV//FQkwXzjOl7NC6M5Kpc70rfWw6cOWytBddPHzzIk
```

경로를 잘못 적은 `-i` 는 오류가 아니라 경고 한 줄이라서 엉뚱한 키로 접속해도 눈에 띄지 않습니다.[^identity]

### `Host *` 의 위치와 우선순위

> 같은 키워드는 처음 읽힌 값이 쓰이므로 구체적인 `Host` 를 위에, `Host *` 를 아래에 둡니다.

```bash
# Host * 를 위에 둔 설정과 아래에 둔 설정을 만든다
printf '%s\n' 'Host *' '    User guest' '' \
  'Host web' '    User appuser' '    HostName srv' > ~/order1.conf
printf '%s\n' 'Host web' '    User appuser' '    HostName srv' '' \
  'Host *' '    User guest' > ~/order2.conf

# 위에 둔 쪽은 guest 가 이기고 아래에 둔 쪽은 appuser 가 이긴다
#   -F   설정 파일을 정한다
ssh -F ~/order1.conf -G web | grep '^user '    # user guest
ssh -F ~/order2.conf -G web | grep '^user '    # user appuser
```

`ssh_config(5)` 가 같은 이유로 호스트별 선언을 앞에, 일반 기본값을 뒤에 두라고 안내합니다.[^first]

### `~/.ssh/config` 권한

> 그룹이나 다른 사용자가 쓸 수 있는 config 는 읽지 않고 255 로 끝납니다.

```bash
# 모두가 쓸 수 있게 열면 접속이 거부된다
chmod 666 ~/.ssh/config
ssh web hostname; echo $?    # Bad owner or permissions on /home/appuser/.ssh/config / 255

# 되돌리면 다시 접속된다
chmod 600 ~/.ssh/config
ssh web hostname    # srv
```

매뉴얼은 남용 가능성 때문에 소유자만 읽고 쓰는 권한이어야 한다고 적습니다.[^perm]

### `known_hosts` 의 세 줄

> 서버가 접속 뒤에 가진 호스트 키 전부를 알려 주고 `ssh` 가 그것을 `known_hosts` 에 더하므로 한 번에 세 줄이 생깁니다.

「처음 접속과 호스트 키 확인」 은 `ED25519` 지문 하나만 보여 주었지만 `known_hosts` 에는 세 종류가 들어갔습니다. 기본으로 켜지는 `UpdateHostKeys` 가 이 일을 맡고, ED25519 키가 바뀌었을 때 경고가 `ECDSA` 줄을 가리키는 것도 이 때문입니다.[^update]

### 호스트 키 변경 경고

> 저장된 호스트 키와 서버가 내민 키가 다르면 `ssh` 는 경고를 찍고 접속을 거부하며, `StrictHostKeyChecking=no` 는 접속은 허용하되 비밀번호 인증을 끕니다.

```bash
# srv 의 ED25519 호스트 키를 새로 만들고 sshd 를 다시 읽게 한다 (호스트 터미널에서)
docker exec srv bash -c '
  rm -f /etc/ssh/ssh_host_ed25519_key /etc/ssh/ssh_host_ed25519_key.pub
  ssh-keygen \
    -q \
    -t ed25519 \
    -N "" \
    -f /etc/ssh/ssh_host_ed25519_key
  pkill -HUP -x sshd'

# 이제 접속하면 거부된다
ssh srv hostname; echo $?
```

```bash
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the ED25519 key sent by the remote host is
SHA256:GVRZp3T/T0XXPaMTr6FQC4qTsgf3LKtYp5luRGQ8ROc.
Please contact your system administrator.
Add correct host key in /home/appuser/.ssh/known_hosts to get rid of this message.
Offending ECDSA key in /home/appuser/.ssh/known_hosts:3
  remove with:
  ssh-keygen -f "/home/appuser/.ssh/known_hosts" -R "srv"
Host key for srv has changed and you have requested strict checking.
Host key verification failed.
255
```

```bash
# StrictHostKeyChecking=no 는 접속을 허용하지만 접속 중 비밀번호 인증을 쓰지 못하게 한다
ssh -o StrictHostKeyChecking=no srv hostname; echo $?
```

```bash
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
...
Password authentication is disabled to avoid man-in-the-middle attacks.
Keyboard-interactive authentication is disabled to avoid man-in-the-middle attacks.
UpdateHostkeys is disabled because the host key is not trusted.
srv
0
```

위 출력은 경고 본문 열 줄을 `...` 로 줄였습니다. 키가 정당하게 바뀐 것을 확인했다면 안내된 `ssh-keygen -R` 로 옛 줄을 지우고 다시 접속합니다.[^strict]

```bash
# 옛 호스트 키를 known_hosts 에서 지우고 다시 받는다
ssh-keygen -R srv
ssh srv hostname    # Warning: Permanently added 'srv' (ED25519) to the list of known hosts. / srv
```

```bash
# Host srv found: line 1
# Host srv found: line 2
# Host srv found: line 3
/home/appuser/.ssh/known_hosts updated.
Original contents retained as /home/appuser/.ssh/known_hosts.old
```

### 반복문 안의 `ssh` 와 표준 입력

> `while read` 로 목록을 읽으며 `ssh` 를 부르면 `ssh` 가 남은 목록을 표준 입력으로 읽어 가서 첫 호스트에서 끝납니다.

```bash
# 호스트 두 개가 적힌 목록. 첫 호스트에서 ssh 가 둘째 줄까지 읽어 가 srv 하나만 나온다
printf 'srv\njump\n' > ~/hosts.txt
while read -r h; do ssh "$h" hostname; done < ~/hosts.txt

# -n 은 ssh 의 표준 입력을 /dev/null 로 돌려 목록을 건드리지 않는다
#   -n   표준 입력을 읽지 않는다
while read -r h; do ssh -n "$h" hostname; done < ~/hosts.txt
```

```bash
srv
```

```bash
srv
jump
```

매뉴얼은 `-n` 이 `ssh` 를 백그라운드로 돌릴 때 필요하다고 적고, 표준 입력을 읽지 않게 막는 옵션이라는 것이 위 실측과 맞습니다.[^n]

### `-L` 이 이미 쓰는 포트를 만나면

> 같은 로컬 포트로 `-L` 을 다시 열면 경고만 찍고 접속은 계속되므로, 스크립트에서는 `ExitOnForwardFailure=yes` 로 실패를 오류로 바꿉니다.

```bash
# 먼저 9000 번을 쓰는 터널을 띄운다
ssh \
  -f \
  -N \
  -M \
  -S /tmp/ctl-srv \
  -L 127.0.0.1:9000:127.0.0.1:8080 \
  srv

# 같은 포트를 다시 연다

# ExitOnForwardFailure=yes 면 중계를 세우지 못할 때 ssh 가 255 로 끝난다
#   ControlPath=none   제어 소켓을 쓰지 않는다 (새 연결로 접속한다)
ssh \
  -o ControlPath=none \
  -o ExitOnForwardFailure=yes \
  -N \
  -L 127.0.0.1:9000:127.0.0.1:8080 \
  srv
echo $?

ssh -S /tmp/ctl-srv -O exit srv
```

```bash
bind [127.0.0.1]:9000: Address already in use
channel_setup_fwd_listener_tcpip: cannot listen to port: 9000
Could not request local forwarding.
255
Exit request sent.
```

이 옵션 없이는 `Could not request local forwarding.` 을 찍고도 접속이 이어질 수 있어 터널이 없는 줄 모르고 지나칩니다.[^exitfwd]



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [ssh-keygen·ssh-copy-id·ssh-agent 참조 시트](./ssh-keygen·ssh-copy-id·ssh-agent.md) — 키를 만들고 서버에 올리고 에이전트로 쓰는 방법
- [scp·sftp 참조 시트](./scp·sftp.md) — 같은 접속으로 파일을 주고받는 방법
- [sshd·sshd_config 참조 시트](./sshd·sshd_config.md) — 이 시트의 접속이 닿는 서버 쪽 설정과 로그
- [systemctl 함정과 동작 원리](../service/systemctl%20함정과%20동작%20원리.md) — ssh 서비스 이름과 `ssh.socket`
- [포트 포워딩 — local·remote·dynamic 과 리버스 터널의 최소 모형](../../../book/sshm_ssh-mastery/09-01.포트%20포워딩%20—%20local·remote·dynamic%20과%20리버스%20터널의%20최소%20모형.md) — 「포트 포워딩」 의 세 방향이 연결을 어떻게 중계하는지의 원리
- [TLS 는 키를 어떻게 안전하게 나누는가 — 핸드셰이크·세션 인증·HTTPS·SSH](../../../book/ostep_operating-systems-three-easy-pieces/45-02.TLS%20는%20키를%20어떻게%20안전하게%20나누는가%20—%20핸드셰이크·세션%20인증·HTTPS·SSH.md) — 호스트 키와 세션 키가 하는 일
- [주고받는 일은 결국 몇 개의 명령으로 줄어든다](../../../book/learning-modern-linux/07-03.주고받는%20일은%20결국%20몇%20개의%20명령으로%20줄어든다.md) — ssh·scp 가 속한 원격 작업 명령의 지도



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- OpenSSH 9.2p1(`openssh-client` 1:9.2p1-2+deb12u10)의 `ssh` 사용법·`man ssh`·`man ssh_config` 원문 — Debian 12 컨테이너 셋에서 2026-11-14 확인
- [ssh(1)](https://manpages.debian.org/bookworm/openssh-client/ssh.1.en.html) — 이 시트의 옵션 뜻과 종료 코드 원문
- [ssh_config(5)](https://manpages.debian.org/bookworm/openssh-client/ssh_config.5.en.html) — 키워드 뜻과 Debian 기본값 원문

[^env]: ssh_config(5) — "Note that the Debian openssh-client package sets several options as standard in /etc/ssh/ssh_config which are not the default in ssh(1): ... HashKnownHosts yes". 컨테이너의 `/etc/ssh/ssh_config` 에서 `HashKnownHosts yes` 를 확인했습니다. <https://manpages.debian.org/bookworm/openssh-client/ssh_config.5.en.html>
[^first]: ssh_config(5) — "For each parameter, the first obtained value will be used." "Since the first obtained value for each parameter is used, more host-specific declarations should be given near the beginning of the file, and general defaults at the end." <https://manpages.debian.org/bookworm/openssh-client/ssh_config.5.en.html>
[^exit]: ssh(1) EXIT STATUS — "ssh exits with the exit status of the remote command or with 255 if an error occurred." <https://manpages.debian.org/bookworm/openssh-client/ssh.1.en.html>
[^fwd]: ssh(1) — `-L` "Specifies that connections to the given TCP port or Unix socket on the local (client) host are to be forwarded to the given host and port, or Unix socket, on the remote side." `-R` "Specifies that connections to the given TCP port or Unix socket on the remote (server) host are to be forwarded to the local side." `-D` "Specifies a local "dynamic" application-level port forwarding." <https://manpages.debian.org/bookworm/openssh-client/ssh.1.en.html>
[^identity]: ssh_config(5) `IdentityFile` — "The default is ~/.ssh/id_rsa, ~/.ssh/id_ecdsa, ~/.ssh/id_ecdsa_sk, ~/.ssh/id_ed25519, ~/.ssh/id_ed25519_sk and ~/.ssh/id_dsa." 없는 `-i` 파일을 줄 때 경고만 찍고 기본 목록으로 돌아간다는 것은 위 `-v` 출력으로 확인했고 매뉴얼에는 그 문장이 없습니다. <https://manpages.debian.org/bookworm/openssh-client/ssh_config.5.en.html>
[^perm]: ssh_config(5) FILES — "Because of the potential for abuse, this file must have strict permissions: read/write for the user, and not writable by others." <https://manpages.debian.org/bookworm/openssh-client/ssh_config.5.en.html>
[^update]: ssh_config(5) `UpdateHostKeys` — "Specifies whether ssh(1) should accept notifications of additional hostkeys from the server sent after authentication has completed and add them to UserKnownHostsFile." "UpdateHostKeys is enabled by default if the user has not overridden the default UserKnownHostsFile setting and has not enabled VerifyHostKeyDNS". <https://manpages.debian.org/bookworm/openssh-client/ssh_config.5.en.html>
[^strict]: ssh_config(5) `StrictHostKeyChecking` — "If this flag is set to accept-new then ssh will automatically add new host keys to the user's known_hosts file, but will not permit connections to hosts with changed host keys. If this flag is set to no or off, ssh will automatically add new host keys to the user known hosts files and allow connections to hosts with changed hostkeys to proceed, subject to some restrictions." <https://manpages.debian.org/bookworm/openssh-client/ssh_config.5.en.html>
[^n]: ssh(1) `-n` — "Redirects stdin from /dev/null (actually, prevents reading from stdin). This must be used when ssh is run in the background." <https://manpages.debian.org/bookworm/openssh-client/ssh.1.en.html>
[^exitfwd]: ssh_config(5) `ExitOnForwardFailure` — "Specifies whether ssh(1) should terminate the connection if it cannot set up all requested dynamic, tunnel, local, and remote port forwardings, (e.g. if either end is unable to bind and listen on a specified port)." <https://manpages.debian.org/bookworm/openssh-client/ssh_config.5.en.html>
