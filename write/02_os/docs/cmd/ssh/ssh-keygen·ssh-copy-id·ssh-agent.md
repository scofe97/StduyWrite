---
title: ssh-keygen·ssh-copy-id·ssh-agent 참조 시트
tags: [linux, cheatsheet, ssh, ssh-keygen, ssh-copy-id, ssh-agent, ssh-add, reference]
status: draft
source:
  - OpenSSH 9.2p1 ssh-keygen(1)·ssh-copy-id(1)·ssh-agent(1)·ssh-add(1) (Debian 12 컨테이너의 `man` 원문, manpages.debian.org bookworm)
related:
  - ./ssh.md
  - ./scp·sftp.md
  - ./sshd·sshd_config.md
  - ../README.md
updated: 2026-11-14
---

# ssh-keygen·ssh-copy-id·ssh-agent 참조 시트

---

> 키 쌍을 만들고, 공개 키를 서버의 `authorized_keys` 에 올리고, 에이전트에 개인 키를 맡기고, `known_hosts` 를 정리하는 방법을 컨테이너에서 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `ssh-keygen` 은 키 쌍을 만들고 지문을 읽고 `known_hosts` 를 고치며, `ssh-copy-id` 는 공개 키를 서버에 올리고, `ssh-agent` 와 `ssh-add` 는 개인 키를 메모리에 맡아 둡니다.

네 명령은 모두 Debian 12 의 `openssh-client` 1:9.2p1 패키지가 `/usr/bin` 에 설치하는 외부 바이너리입니다. `ssh-copy-id` 는 셸 스크립트입니다. 출력은 `ssh -V` 가 `OpenSSH_9.2p1 Debian-2+deb12u10, OpenSSL 3.0.22` 로 답하는 컨테이너에서 받았습니다. 이 판에서 `-t` 없이 `ssh-keygen` 을 부르면 RSA 3072 비트 키가 나오지만, 판이 바뀌면 기본 종류가 바뀔 수 있어 예에서는 `-t` 를 적습니다.[^default]

이 시트는 `ssh` 시트의 「실습 준비」 를 이어받습니다. 컨테이너 셋(`srv`·`jump`·`cli`)과 `cli` 의 `appuser` 키가 이미 있어야 하므로 [ssh 접속·config·포트 포워딩 참조 시트](./ssh.md) 의 준비 블록을 먼저 돌려 둡니다.

핵심은 이 흐름입니다. 키 쌍은 `cli` 에서 만들고, 공개 키 한 줄만 서버의 `~/.ssh/authorized_keys` 에 들어갑니다. 서버는 그 공개 키로 클라이언트가 개인 키를 가졌는지 확인합니다.



## 핵심 문법

> 키 파일은 `-f` 로, 키의 종류와 속성은 `-t`·`-b`·`-C` 로 정하고, `ssh-keygen` 은 `-l`·`-y`·`-F`·`-R` 같은 동작 옵션 하나로 하는 일이 정해집니다.

```bash
# ssh-keygen 호출 형태. --help 가 없어 잘못된 옵션을 주면 나오는 사용법의 앞부분이다
usage: ssh-keygen [-q] [-a rounds] [-b bits] [-C comment] [-f output_keyfile]
                  [-m format] [-N new_passphrase] [-O option]
                  [-t dsa | ecdsa | ecdsa-sk | ed25519 | ed25519-sk | rsa]
                  [-w provider] [-Z cipher]
       ssh-keygen -p [-a rounds] [-f keyfile] [-m format] [-N new_passphrase]
                   [-P old_passphrase] [-Z cipher]
       ssh-keygen -i [-f input_keyfile] [-m key_format]
       ssh-keygen -e [-f input_keyfile] [-m key_format]
       ssh-keygen -y [-f input_keyfile]
       ssh-keygen -c [-a rounds] [-C comment] [-f keyfile] [-P passphrase]
       ssh-keygen -l [-v] [-E fingerprint_hash] [-f input_keyfile]
       ssh-keygen -B [-f input_keyfile]
       ssh-keygen -D pkcs11
       ssh-keygen -F hostname [-lv] [-f known_hosts_file]
       ssh-keygen -H [-f known_hosts_file]
       ssh-keygen -K [-a rounds] [-w provider]
       ssh-keygen -R hostname [-f known_hosts_file]
       ...

# ssh-copy-id 호출 형태 (ssh-copy-id -h 의 Usage 줄)
Usage: /usr/bin/ssh-copy-id [-h|-?|-f|-n|-s] [-i [identity_file]] [-p port] [-F alternative ssh_config file] [[-o <ssh -o options>] ...] [user@]hostname

# ssh-agent 호출 형태. 잘못된 옵션을 주면 나오는 사용법이다
usage: ssh-agent [-c | -s] [-Dd] [-a bind_address] [-E fingerprint_hash]
                 [-O option] [-P allowed_providers] [-t life]
       ssh-agent [-a bind_address] [-E fingerprint_hash] [-O option]
                 [-P allowed_providers] [-t life] command [arg ...]
       ssh-agent [-c | -s] -k

# 키 쌍을 만든다 (키 만들기)
ssh-keygen \
  -t 종류 \
  -f 파일 \
  -N 암호문 \
  -C 주석

# 키 파일에서 지문이나 공개 키를 읽는다 (지문과 공개 키 읽기)
ssh-keygen -l -f 공개키파일
ssh-keygen -y -f 개인키파일

# 공개 키를 서버에 올린다 (공개 키를 서버에 올리기)
ssh-copy-id -i 공개키파일 호스트

# 에이전트를 띄우고 키를 맡긴다 (에이전트 쓰기)
eval "$(ssh-agent -s)"
ssh-add 개인키파일

# known_hosts 에서 호스트를 찾거나 지운다 (known_hosts 정리)
ssh-keygen -F 호스트
ssh-keygen -R 호스트
```

`ssh-add` 는 `-?` 로 사용법을 보여 줍니다. 에이전트가 떠 있을 때만 그렇습니다.

```bash
# ssh-add 호출 형태. 에이전트가 떠 있을 때 ssh-add -? 가 찍는 사용법이다
usage: ssh-add [-cDdKkLlqvXx] [-E fingerprint_hash] [-H hostkey_file]
               [-h destination_constraint] [-S provider] [-t life]
               [file ...]
       ssh-add -s pkcs11
       ssh-add -e pkcs11
       ssh-add -T pubkey ...
```



## 종료 코드

> `ssh-add` 는 0·1·2 의 뜻이 man 에 정해져 있고, 나머지 세 명령은 종료 코드 절이 없어 실측한 값만 싣습니다.[^exit-add][^no-exit]

```bash
# ssh-add   0 성공
#           1 지정한 동작이 실패함
#           2 에이전트에 연결하지 못함

# 에이전트가 없으면 2 로 끝난다
ssh-add -l; echo $?    # Could not open a connection to your authentication agent. / 2
```

```bash
# 실측한 코드. man 에 뜻이 없는 값이라 상황만 적는다
# ssh-keygen   이미 있는 파일에 덮어쓰기를 거절함 1
#              없는 파일을 -l 로 읽음 255
#              알 수 없는 -t 종류 255
#              -F 가 호스트를 못 찾음 1
# ssh-copy-id  이름을 풀지 못하거나 키 파일이 없음 1
# ssh-agent    -k 인데 SSH_AGENT_PID 가 없음 1
```



## 유스케이스

> 예는 앞 예가 만든 상태를 이어 쓰므로 위에서 아래로 차례로 돌립니다. 모두 `cli` 의 `appuser` 셸에서 돌립니다.

### 실습 준비

> 이 시트는 `ssh` 시트의 준비 블록이 만든 컨테이너 셋을 그대로 쓰고, 키를 담을 폴더와 호스트 키 자동 수락 설정만 더 만듭니다.

이 폴더에 만든 키는 「키 만들기」·「키 종류와 크기」 부터 여러 곳이 씁니다.

```bash
# 이 시트의 키를 모아 둘 폴더. 기본 키(~/.ssh/id_*)와 섞이지 않게 따로 둔다
mkdir -p ~/lab

# 새 호스트 키는 묻지 않고 받는 설정을 둔다
# ssh 시트의 config 예와 같은 줄이라 두 번 들어가도 같은 값이다
#   accept-new   처음 보는 호스트 키는 받고, 바뀐 키는 거부한다
mkdir -p ~/.ssh
printf 'Host *\n  StrictHostKeyChecking accept-new\n' >> ~/.ssh/config

# 권한이 넓으면 ssh 가 config 를 읽지 않는다
chmod 600 ~/.ssh/config

# srv 의 호스트 키를 미리 받아 둔다. 처음 접속이면 아래 경고 한 줄이 나온다
ssh srv true    # Warning: Permanently added 'srv' (ED25519) to the list of known hosts.
```

### 키 만들기

> `-t` 로 종류를, `-f` 로 파일을 정해 키 쌍을 만들면 개인 키와 `.pub` 공개 키가 생기고 지문과 무작위 그림이 출력됩니다.

```bash
# ed25519 키 쌍을 만든다
#   -t   키 종류
#   -f   개인 키 파일. 공개 키는 같은 이름에 .pub 이 붙는다
#   -N   새 암호문. 빈 문자열이면 암호문 없이 만든다
#   -C   공개 키 끝에 붙는 주석
ssh-keygen \
  -t ed25519 \
  -f ~/lab/k1 \
  -N '' \
  -C 'lab key'
```

```bash
Generating public/private ed25519 key pair.
Your identification has been saved in /home/appuser/lab/k1
Your public key has been saved in /home/appuser/lab/k1.pub
The key fingerprint is:
SHA256:vvF7wd0CJqUtN+RijqzX5V4ecP3BjPP3DuVkc/loCkY lab key
The key's randomart image is:
+--[ED25519 256]--+
|                 |
|            o    |
|           *     |
|          * B +..|
|       .S+EB.*.B*|
|       .o.. +o=*B|
|       .o.oo .*o=|
|      . .=..o= oo|
|       .. o+o ..o|
+----[SHA256]-----+
```

지문과 그림은 실행마다 다른 값입니다. 만들어진 파일과 공개 키의 앞 두 필드(종류·주석)를 봅니다.

```bash
# 만들어진 파일 목록
ls ~/lab    # k1  k1.pub

# 공개 키 한 줄에서 종류(1번째 필드)와 주석(3번째 필드)만 본다
#   cut -d   필드를 가르는 문자
#   cut -f   가져올 필드
cut -d' ' -f1,3 ~/lab/k1.pub    # ssh-ed25519 lab
```

공개 키 한 줄은 `종류 키본문 주석` 세 필드이고 주석은 `lab key` 에서 공백 앞까지만 `cut` 에 걸렸습니다.

### 키 종류와 크기

> `-t` 에 `rsa`·`ecdsa` 를 주고 `-b` 로 비트 수를 정하면 다른 종류의 키를 만들고, 지문 줄 끝에 종류가 찍힙니다.

```bash
# -t 없이 만들면 이 판에서는 RSA 3072 가 나온다
#   -q   만드는 과정의 출력을 끈다
ssh-keygen \
  -f ~/lab/kdef \
  -N '' \
  -q

# 만든 키의 지문과 종류를 본다
#   -l   지문을 보여 준다
ssh-keygen -lf ~/lab/kdef.pub
# 3072 SHA256:pgrwCvxmb9dtdKpzdMTrD+oq9ui6aOYzE/r+2INte6U appuser@cli (RSA)

# 종류와 비트 수를 정해 만든다
#   -b   비트 수. RSA 는 3072 가 기본이고, ECDSA 는 256·384·521 중에 고른다
ssh-keygen \
  -q \
  -t rsa \
  -b 3072 \
  -f ~/lab/k2 \
  -N '' \
  -C 'lab rsa'
ssh-keygen -lf ~/lab/k2.pub
# 3072 SHA256:Gm5y2kQbOfZL1lYVMB7suErmcIyCAFx9m7P+T4TxuOM lab rsa (RSA)

ssh-keygen \
  -q \
  -t ecdsa \
  -b 256 \
  -f ~/lab/k3 \
  -N '' \
  -C 'lab ecdsa'
ssh-keygen -lf ~/lab/k3.pub
# 256 SHA256:2ZT0Z420aCczznquMA8hOn0Xu1AC+J7NNFR8/W+64PA lab ecdsa (ECDSA)
```

`-C` 를 주지 않으면 주석이 `사용자@호스트` 로 채워졌습니다(`appuser@cli`).

### 지문과 공개 키 읽기

> 같은 키를 지문(`-l`), 무작위 그림(`-lv`), MD5 지문(`-E md5`), 공개 키 한 줄(`-y`), RFC4716 형식(`-e`)으로 읽을 수 있습니다.

```bash
# 공개 키 파일의 지문. 끝에 주석과 종류가 붙는다
ssh-keygen -lf ~/lab/k1.pub
# 256 SHA256:vvF7wd0CJqUtN+RijqzX5V4ecP3BjPP3DuVkc/loCkY lab key (ED25519)

# 지문과 함께 무작위 그림을 보여 준다
#   -v   -l 과 함께 쓰면 그림을 더한다
ssh-keygen -lv -f ~/lab/k1.pub

# MD5 지문으로 본다. 옛 문서와 대조할 때 쓴다
#   -E   지문 해시 알고리즘. md5 와 sha256 중에 고른다
ssh-keygen -lf ~/lab/k1.pub -E md5
# 256 MD5:36:e0:a6:d6:9b:46:61:17:e8:9d:99:11:1d:4c:60:dc lab key (ED25519)

# 개인 키에서 공개 키 한 줄을 다시 뽑는다. 첫 필드만 본다
#   -y   개인 키를 읽어 공개 키를 출력한다
ssh-keygen -y -f ~/lab/k1 | cut -d' ' -f1    # ssh-ed25519

# RFC4716 형식으로 내보낸다. 앞 60자만 본다
#   -e   공개 키를 다른 형식으로 출력한다
#   -m   출력 형식
#   cut -c   가져올 문자 위치
ssh-keygen \
  -e \
  -f ~/lab/k1.pub \
  -m RFC4716 \
  | cut -c1-60
```

```bash
---- BEGIN SSH2 PUBLIC KEY ----
Comment: "256-bit ED25519, converted by appuser@cli from Ope
AAAAC3NzaC1lZDI1NTE5AAAAIMs52fUO+7QoclSkgIIv5WnTc7dCAAwooqk5
---- END SSH2 PUBLIC KEY ----
```

`-lv` 의 그림은 「키 만들기」 의 출력에 나온 그림과 같고, 지문이 같으면 같은 키입니다. 서버 관리자에게 받은 지문을 이 출력과 맞대는 데 씁니다.

### 공개 키를 서버에 올리기

> `ssh-copy-id -i` 가 공개 키를 서버의 `authorized_keys` 에 붙이고, 이미 있는 키는 건너뜁니다.

```bash
# 올리기 전에 어떤 키가 올라갈지만 본다
#   ssh-copy-id -n   예행 연습. 서버에는 아무것도 쓰지 않는다
#   ssh-copy-id -i   올릴 공개 키 파일
ssh-copy-id -n -i ~/lab/k1.pub srv
```

```bash
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/appuser/lab/k1.pub"
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
=-=-=-=-=-=-=-=
Would have added the following key(s):

ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMs52fUO+7QoclSkgIIv5WnTc7dCAAwooqk5a+DpYnir lab key
=-=-=-=-=-=-=-=
```

```bash
# 실제로 올린다
ssh-copy-id -i ~/lab/k1.pub srv
```

```bash
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/appuser/lab/k1.pub"
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'srv'"
and check to make sure that only the key(s) you wanted were added.
```

`ssh-copy-id` 는 올리기 전에 접속을 한 번 시도합니다. 이 실습에서는 `cli` 의 기본 키가 서버에 이미 등록되어 있어 그 키로 로그인해 올렸습니다.

```bash
# 같은 키를 한 번 더 올린다. 이미 있으면 건너뛴다
ssh-copy-id -i ~/lab/k1.pub srv
```

```bash
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/appuser/lab/k1.pub"
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed

/usr/bin/ssh-copy-id: WARNING: All keys were skipped because they already exist on the remote system.
		(if you think this is a mistake, you may want to use -f option)
```

```bash
# 방금 올린 키로만 접속한다
#   ssh -i   쓸 개인 키 파일
#   ssh -o IdentitiesOnly=yes   -i 로 준 키만 쓴다
#                               에이전트의 다른 키와 기본 키는 내밀지 않는다
ssh -i ~/lab/k1 -o IdentitiesOnly=yes srv hostname    # srv

# 서버의 authorized_keys 에서 종류(1번째 필드)와 주석(3번째 필드)만 본다
ssh srv "awk '{print \$1, \$3}' ~/.ssh/authorized_keys"
```

```bash
ssh-ed25519 id_ed25519@cli
ssh-ed25519 id_work@cli
ssh-ed25519 lab
```

실습 준비가 넣은 키 둘 뒤에 방금 올린 `lab key` 가 한 줄 늘었고, 두 번째 실행은 줄을 늘리지 않았습니다. 확인 없이 붙이는 `-f` 는 같은 키를 둘 이상 복사할 수 있습니다.[^force]

### 에이전트 쓰기

> `ssh-agent` 가 환경 변수를 찍으면 셸에 적용하고, `ssh-add` 로 개인 키를 맡기면 이후 `ssh` 가 키 파일 없이도 에이전트의 키로 접속합니다.

```bash
# 에이전트가 없는 셸에서 ssh-add 를 부르면 2 로 끝난다
ssh-add -l; echo $?    # Could not open a connection to your authentication agent. / 2

# 에이전트를 띄우고 출력된 환경 변수 명령을 현재 셸에 적용한다
#   ssh-agent -s   Bourne 셸 명령을 출력한다
ssh-agent -s
```

```bash
SSH_AUTH_SOCK=/tmp/ssh-XXX/agent.4850; export SSH_AUTH_SOCK;
SSH_AGENT_PID=4852; export SSH_AGENT_PID;
echo Agent pid 4852;
```

`/tmp/ssh-XXX/` 는 임시 폴더 이름을 `XXX` 로 가려 적은 것이고, PID 는 실행마다 다릅니다. 위 출력은 확인용이라 에이전트가 하나 더 떠 있게 되므로, 실제로 쓸 에이전트는 아래처럼 `eval` 로 띄웁니다.

```bash
# 에이전트를 띄우면서 환경 변수를 현재 셸에 적용한다
eval "$(ssh-agent -s)"    # Agent pid 4854

# 맡은 키가 없으면 1 로 끝난다
ssh-add -l; echo $?    # The agent has no identities. / 1

# 키를 맡긴다
ssh-add ~/lab/k1    # Identity added: /home/appuser/lab/k1 (lab key)

# 맡길 때 수명을 정한다. 3600초 뒤에 에이전트가 키를 잊는다
#   ssh-add -t   수명(초)
ssh-add -t 3600 ~/.ssh/id_ed25519
# Identity added: /home/appuser/.ssh/id_ed25519 (id_ed25519@cli)
# Lifetime set to 3600 seconds

# 맡은 키의 지문과 공개 키를 본다
#   ssh-add -l   지문 목록
#   ssh-add -L   공개 키 목록
ssh-add -l
ssh-add -L | cut -d' ' -f1,3
```

```bash
256 SHA256:vvF7wd0CJqUtN+RijqzX5V4ecP3BjPP3DuVkc/loCkY lab key (ED25519)
256 SHA256:GV//FQkwXzjOl7NC6M5Kpc70rfWw6cOWytBddPHzzIk id_ed25519@cli (ED25519)
ssh-ed25519 lab
ssh-ed25519 id_ed25519@cli
```

에이전트가 키를 대신 내미는지는 개인 키 파일을 치워서 확인합니다.

```bash
# 개인 키 파일을 치우고, 공개 키 파일로 어떤 키를 쓸지만 고른다
mv ~/lab/k1 ~/lab/k1.off
#   ssh -v   디버그 메시지를 찍는다
ssh -i ~/lab/k1.pub -o IdentitiesOnly=yes -v srv hostname 2>&1 \
  | grep -E 'Offering|^srv'
```

```bash
debug1: Offering public key: /home/appuser/lab/k1.pub ED25519 SHA256:vvF7wd0CJqUtN+RijqzX5V4ecP3BjPP3DuVkc/loCkY explicit agent
srv
```

`Offering` 줄 끝의 `agent` 는 서명을 에이전트에 맡겼다는 뜻입니다. 개인 키 파일이 없는데도 접속이 되었습니다.

```bash
# 치운 개인 키 파일을 제자리로 돌려 놓는다
mv ~/lab/k1.off ~/lab/k1
```

```bash
# 맡은 키를 하나 뺀다. 개인 키가 아니라 공개 키 파일 경로를 준다
#   ssh-add -d   지정한 키를 에이전트에서 뺀다
ssh-add -d ~/lab/k1.pub    # Identity removed: /home/appuser/lab/k1.pub ED25519 (lab key)

# 전부 뺀다
#   ssh-add -D   모든 키를 뺀다
ssh-add -D; ssh-add -l; echo $?
```

```bash
All identities removed.
The agent has no identities.
1
```

```bash
# 에이전트를 끝낸다
#   ssh-agent -k   SSH_AGENT_PID 가 가리키는 에이전트를 죽인다
ssh-agent -k
```

```bash
unset SSH_AUTH_SOCK;
unset SSH_AGENT_PID;
echo Agent pid 4854 killed;
```

`-k` 의 출력도 `eval` 로 적용해야 환경 변수가 지워집니다. 위 예는 `-d` 에서 한 개를 빼고 `-D` 로 나머지를 빼는 순서라 `id_ed25519` 는 `-D` 가 뺐습니다.

### 에이전트 포워딩

> `ssh -A` 로 접속하면 서버에 키 파일을 두지 않고도 서버 안에서 로컬 에이전트의 키를 쓸 수 있습니다.

이 예는 에이전트가 떠 있고 키가 맡겨져 있어야 하므로 앞 예의 상태를 다시 만듭니다.

```bash
# 에이전트를 새로 띄우고 키 둘을 맡긴다
eval "$(ssh-agent -s)" > /dev/null
ssh-add ~/lab/k1 ~/.ssh/id_ed25519 2> /dev/null

# 포워딩 없이 서버에서 ssh-add 를 부르면 서버에는 에이전트가 없다
ssh srv 'ssh-add -l'; echo $?    # Could not open a connection to your authentication agent. / 2

# -A 를 주면 서버에서도 로컬 에이전트의 키가 보인다
#   ssh -A   인증 에이전트 연결을 서버로 포워딩한다
ssh -A srv 'ssh-add -l'
```

```bash
256 SHA256:vvF7wd0CJqUtN+RijqzX5V4ecP3BjPP3DuVkc/loCkY lab key (ED25519)
256 SHA256:GV//FQkwXzjOl7NC6M5Kpc70rfWw6cOWytBddPHzzIk id_ed25519@cli (ED25519)
```

```bash
# srv 에서 jump 로 한 번 더 접속한다. srv 에는 개인 키가 없고 에이전트 키로 로그인한다
ssh -A srv 'ssh -o StrictHostKeyChecking=accept-new jump hostname'

# 이 예의 에이전트를 끝낸다. 남겨 두면 뒤의 「권한이 넓은 개인 키」 에서 에이전트의 키가 대신 쓰인다
ssh-agent -k > /dev/null
```

```bash
Warning: Permanently added 'jump' (ED25519) to the list of known hosts.
jump
```

서버의 root 는 그 에이전트 소켓을 쓸 수 있으므로 믿는 서버에만 `-A` 를 씁니다.[^forward]

### known_hosts 정리

> `ssh-keygen -F` 로 `known_hosts` 에서 호스트를 찾고, `-R` 로 지우고, `-H` 로 이름을 해시로 바꿉니다.

```bash
# known_hosts 는 이름을 해시로 저장하므로 grep 으로는 호스트를 못 찾는다. -F 로 찾는다
#   -F   호스트 이름을 찾아 일치한 줄을 보여 준다
ssh-keygen -F srv | cut -c1-40
```

```bash
# Host srv found: line 4
|1|t6yaThVxP4QiC8jMjdg/ZlpY1OQ=|jPvpYKVI
# Host srv found: line 5
|1|LC+FbT/3HYK4L+gyMSc/PWsxFCg=|bRQ2JjNM
# Host srv found: line 6
|1|CSdDwzHD5h2+qUy0PjlYG39kon8=|/8CPgZ+u
```

```bash
# 해시를 지문으로 바꿔 본다. -F 와 -l 을 함께 준다
ssh-keygen -F srv -l
```

```bash
# Host srv found: line 4
srv ED25519 SHA256:GVRZp3T/T0XXPaMTr6FQC4qTsgf3LKtYp5luRGQ8ROc
# Host srv found: line 5
srv RSA SHA256:N/OPWXyK0bHejPThhheiclrEvMRxNc7IrdvpruZFq58
# Host srv found: line 6
srv ECDSA SHA256:XPVoyP3Ghd722cFXQIJMredbgTiH2FxucyqI6ZNeJeU
```

```bash
# 없는 호스트는 아무것도 찍지 않고 1 로 끝난다
ssh-keygen -F nosuch; echo $?    # 1
```

`srv` 가 세 줄인 것은 서버가 ED25519·RSA·ECDSA 호스트 키 셋을 모두 알려 주었기 때문입니다. 앞의 1~3번 줄은 `ssh` 시트의 `-J` 예에서 받은 `jump` 의 키입니다.

```bash
# jump 의 키를 known_hosts 에서 지운다
#   -R   호스트의 모든 키를 known_hosts 에서 지운다
ssh-keygen -R jump
```

```bash
# Host jump found: line 1
# Host jump found: line 2
# Host jump found: line 3
/home/appuser/.ssh/known_hosts updated.
Original contents retained as /home/appuser/.ssh/known_hosts.old
```

```bash
# 지운 호스트를 다시 찾으면 1 로 끝난다
ssh-keygen -F jump; echo $?    # 1

# 해시가 아닌 줄로 저장된 파일을 해시로 바꾼다
#   ssh -o HashKnownHosts=no     해시 없이 저장하게 한다
#   ssh -o UserKnownHostsFile=   이 접속이 쓸 known_hosts 파일
ssh \
  -o HashKnownHosts=no \
  -o UserKnownHostsFile=$HOME/lab/kh-plain \
  srv true    # Warning: Permanently added 'srv' (ED25519) to the list of known hosts.
cut -c1-40 ~/lab/kh-plain    # srv ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA

#   -H   파일의 이름을 모두 해시로 바꾼다
ssh-keygen -H -f ~/lab/kh-plain
```

```bash
/home/appuser/lab/kh-plain updated.
Original contents retained as /home/appuser/lab/kh-plain.old
WARNING: /home/appuser/lab/kh-plain.old contains unhashed entries
Delete this file to ensure privacy of hostnames
```

`-R` 과 `-H` 는 바꾸기 전 파일을 `.old` 로 남깁니다. 해시로 바꾼 뒤에는 `.old` 에 이름이 그대로 남아 있으므로 지웁니다.

### 실습 정리

> 「주의사항과 동작 원리」 의 예도 이 키 폴더를 쓰므로 그 절까지 마친 뒤 지웁니다. 컨테이너와 네트워크는 `ssh` 시트의 「실습 정리」 가 지웁니다.

```bash
# 이 시트가 만든 키 폴더를 지운다. 서버의 authorized_keys 에 올린 lab key 는 컨테이너와 함께 사라진다
rm -rf ~/lab
```



## 주의사항과 동작 원리

### 이미 있는 키 파일에 만들기

> `-f` 가 가리키는 파일이 이미 있으면 `ssh-keygen` 이 덮어쓸지 묻고, 입력이 없으면 거절하고 1 로 끝납니다.

```bash
# 표준 입력을 막고 같은 파일에 다시 만든다
ssh-keygen \
  -t ed25519 \
  -f ~/lab/k1 \
  -N '' \
  < /dev/null
echo rc=$?
```

```bash
Generating public/private ed25519 key pair.
/home/appuser/lab/k1 already exists.
Overwrite (y/n)? rc=1
```

스크립트에서 키를 만들 때는 파일이 없는지 먼저 확인하거나 `rm -f` 로 지운 뒤 만듭니다. 이 질문은 개인 키를 잃는 사고를 막는 장치입니다.

### 권한이 넓은 개인 키

> 개인 키 파일이 다른 사용자에게 읽히는 권한(0644)이면 `ssh` 와 `ssh-keygen` 이 그 키를 무시하고 255 로 끝납니다.

```bash
# 개인 키 권한을 0644 로 열고 읽어 본다
chmod 644 ~/lab/k1
ssh-keygen -y -f ~/lab/k1; echo rc=$?
```

```bash
...
Permissions 0644 for '/home/appuser/lab/k1' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "/home/appuser/lab/k1": bad permissions
rc=255
```

```bash
# 같은 키로 접속하면 키를 건너뛰고 인증이 거절된다
#   ssh -o BatchMode=yes   비밀번호 같은 입력을 묻지 않는다
ssh -i ~/lab/k1 -o BatchMode=yes srv hostname; echo rc=$?    # 위와 같은 경고 뒤에 appuser@srv: Permission denied (publickey). / 255

# 권한을 되돌린다
chmod 600 ~/lab/k1
```

개인 키는 0600 이어야 하고 이 검사는 클라이언트가 합니다. 출력의 `...` 는 `@` 로 둘러싼 경고 상자 3줄을 줄인 자리입니다.

### 서버의 .ssh 권한

> 서버 쪽 `~/.ssh` 폴더 권한이 넓으면 공개 키가 맞아도 클라이언트에는 `Permission denied (publickey)` 만 보이고, 이유는 서버 로그에만 남습니다.

```bash
# 서버의 ~/.ssh 를 누구나 쓸 수 있게 연다
ssh srv 'chmod 777 ~/.ssh'

# 같은 키로 접속하면 거절된다
ssh -o BatchMode=yes srv hostname; echo rc=$?    # appuser@srv: Permission denied (publickey). / 255
```

```bash
# 이유는 서버 쪽에서 본다. 호스트 터미널에서 돌린다
docker exec srv tail -3 /var/log/sshd.log
```

```bash
Disconnected from user appuser 192.0.2.20 port 44412
Authentication refused: bad ownership or modes for directory /home/appuser/.ssh
Connection closed by authenticating user appuser 192.0.2.20 port 44426 [preauth]
```

```bash
# 호스트 터미널에서 권한을 되돌리면 다시 접속된다
docker exec -u appuser srv chmod 700 /home/appuser/.ssh
ssh -o BatchMode=yes srv hostname; echo rc=$?    # srv / 0
```

서버의 `sshd` 는 `StrictModes` 가 켜져 있으면 사용자 폴더와 `~/.ssh` 의 권한과 소유자를 확인한 뒤에야 `authorized_keys` 를 읽습니다.[^strict] 로그 읽는 법은 [sshd·sshd_config 참조 시트](./sshd·sshd_config.md) 에 있습니다.



## 관련 문서

> 이 시트의 키와 에이전트를 쓰는 접속과 서버 쪽 설정을 이어서 볼 수 있습니다.

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [ssh 접속·config·포트 포워딩 참조 시트](./ssh.md) — 이 시트가 이어받는 「실습 준비」 와 `~/.ssh/config`, `known_hosts` 의 세 줄
- [scp·sftp 참조 시트](./scp·sftp.md) — 같은 키로 파일을 주고받는 방법
- [sshd·sshd_config 참조 시트](./sshd·sshd_config.md) — `PubkeyAuthentication`·`AuthorizedKeysFile` 과 로그 읽기
- [TLS 는 키를 어떻게 안전하게 나누는가 — 핸드셰이크·세션 인증·HTTPS·SSH](../../../book/ostep_operating-systems-three-easy-pieces/45-02.TLS%20는%20키를%20어떻게%20안전하게%20나누는가%20—%20핸드셰이크·세션%20인증·HTTPS·SSH.md) — 공개 키로 상대를 확인하는 원리



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- OpenSSH 9.2p1(`openssh-client` 1:9.2p1-2+deb12u10)의 `ssh-keygen`·`ssh-copy-id`·`ssh-agent`·`ssh-add` 사용법과 man 원문 — Debian 12 컨테이너 셋에서 2026-11-14 확인
- [ssh-keygen(1)](https://manpages.debian.org/bookworm/openssh-client/ssh-keygen.1.en.html) — 키 만들기·지문·`known_hosts` 옵션 원문
- [ssh-copy-id(1)](https://manpages.debian.org/bookworm/openssh-client/ssh-copy-id.1.en.html) — `-i`·`-f`·`-n` 원문
- [ssh-agent(1)](https://manpages.debian.org/bookworm/openssh-client/ssh-agent.1.en.html) — `-s`·`-k` 원문
- [ssh-add(1)](https://manpages.debian.org/bookworm/openssh-client/ssh-add.1.en.html) — 키 맡기기·종료 코드 원문

[^default]: ssh-keygen(1) — "If invoked without any arguments, ssh-keygen will generate an RSA key." "For RSA keys, the minimum size is 1024 bits and the default is 3072 bits." <https://manpages.debian.org/bookworm/openssh-client/ssh-keygen.1.en.html>
[^exit-add]: ssh-add(1) EXIT STATUS — "Exit status is 0 on success, 1 if the specified command fails, and 2 if ssh-add is unable to contact the authentication agent." <https://manpages.debian.org/bookworm/openssh-client/ssh-add.1.en.html>
[^no-exit]: ssh-keygen(1)·ssh-copy-id(1)·ssh-agent(1) 의 man 에는 종료 코드 절이 없습니다. 아래 값은 컨테이너에서 해당 호출을 돌려 `echo $?` 로 읽은 것입니다.
[^force]: ssh-copy-id(1) — "-f Forced mode: doesn't check if the keys are present on the remote server. This means that it does not need the private key. Of course, this can result in more than one copy of the key being installed on the remote system." <https://manpages.debian.org/bookworm/openssh-client/ssh-copy-id.1.en.html>
[^forward]: ssh(1) — "Agent forwarding should be enabled with caution. Users with the ability to bypass file permissions on the remote host (for the agent's UNIX-domain socket) can access the local agent through the forwarded connection." <https://manpages.debian.org/bookworm/openssh-client/ssh.1.en.html>
[^strict]: sshd_config(5) — "StrictModes Specifies whether sshd(8) should check file modes and ownership of the user's files and home directory before accepting login." <https://manpages.debian.org/bookworm/openssh-server/sshd_config.5.en.html>
