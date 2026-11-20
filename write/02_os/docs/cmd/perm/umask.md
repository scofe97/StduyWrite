---
title: umask 참조 시트
tags: [linux, cheatsheet, umask, file-mode, permission, systemd, cli, reference]
status: draft
source:
  - GNU bash 5.2.15 `help umask` 원문 (Debian 12)
  - umask(2) (Linux man-pages 6.03, Debian bookworm)
  - systemd.exec(5) (systemd 252, Debian bookworm)
  - pam_umask(8) (Linux-PAM 1.5.2, Debian bookworm)
  - acl(5) (acl 2.3.1, Debian bookworm)
  - systemd.service(5) (systemd 252, Debian bookworm)
related:
  - ./getfacl·setfacl.md
  - ../file/ls.md
  - ../README.md
updated: 2026-11-17
---

# umask 참조 시트

---

> 새 파일과 디렉터리의 권한에서 `umask` 가 끄는 비트를 읽고 바꾸는 방법을 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `umask` 는 프로세스가 파일·디렉터리를 새로 만들 때 요청한 권한에서 끌 비트를 정하는 셸 내장 명령입니다.

`umask` 는 bash 내장이라 별도 패키지가 없고, 값은 `umask(2)` 시스템 콜이 프로세스에 저장합니다.[^umask-syscall]

출력은 Debian 12 컨테이너(GNU bash 5.2.15, coreutils 9.1, acl 2.3.1)에서 받았습니다. `docker exec` 로 들어간 셸의 시작 umask 는 `0000` 이었습니다. systemd `UMask=` 만 Debian 12 VM(OrbStack, systemd 252)에서 받았습니다.

예는 「실습 준비」 의 `alice` 계정으로 돌립니다. 실행 환경마다 시작 umask 가 다르므로 첫 예의 값은 달라질 수 있습니다.



## 핵심 문법

> 8진수나 기호로 끌 비트를 주고, 값을 주지 않으면 지금의 값을 읽습니다.

```bash
# 호출 형태. umask 는 bash 내장이라 help umask 의 첫 줄이다
umask: umask [-p] [-S] [mode]

# 지금 값을 8진수로 읽는다 (umask 읽고 바꾸기)
umask

# 8진수로 끌 비트를 정한다. 027 은 그룹의 쓰기와 그 밖의 모두의 읽기·쓰기·실행을 끈다 (umask 읽고 바꾸기)
umask 027

# 기호로 허용할 권한을 정한다. 8진수와 뜻이 반대로 읽힌다 (umask 읽고 바꾸기)
umask u=rwx,g=rx,o=

# 새 파일은 666, 새 디렉터리는 777 에서 umask 의 비트를 끈 값이 된다 (새 파일과 디렉터리의 권한 계산)
touch 파일; mkdir 디렉터리

# 서브셸 안에서만 바꾼다 (서브셸과 자식 프로세스의 umask)
( umask 077; 명령 )

# 로그인 셸에 영구로 둔다 (로그인 셸에 umask 영구 설정)
echo 'umask 027' >> ~/.profile

# 서비스에는 유닛에서 정한다 (systemd 서비스의 UMask=)
UMask=0077
```



## 종료 코드

> 잘못된 mode 는 1, 잘못된 옵션은 2 이고 나머지는 0 입니다.[^umask-exit]

```bash
# 0  값을 읽었거나 바꿨다
# 1  mode 가 잘못됐다
# 2  옵션이 잘못됐다
umask 022; echo $?    # 0
bash -c 'umask 999'; echo $?    # bash: line 1: umask: 999: octal number out of range / 1
bash -c 'umask -z'; echo $?    # bash: line 1: umask: -z: invalid option / umask: usage: umask [-p] [-S] [mode] / 2
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다. 앞의 두 줄은 `echo $?` 만 `1`·`2` 를 찍고, `umask 022` 는 아무것도 찍지 않아 `0` 만 나옵니다.



## 유스케이스

> 예는 앞 예가 만든 상태를 이어 쓰므로 위에서 아래로 차례로 돌립니다.

### 실습 준비

> 아래 블록을 한 번 붙여 넣으면 이 시트의 예가 쓰는 계정과 디렉터리가 생깁니다.

Debian 12 컨테이너의 root 셸에서 돌립니다. `docker exec` 로 들어간 셸의 시작 umask 는 `0000` 입니다. `docker run -it` 로 바로 띄운 셸은 `0022` 라서, 이 시트의 첫 값을 보려면 아래 방식으로 들어갑니다. `acl` 은 마지막 함정 절에서 씁니다.

```bash
# 컨테이너를 띄워 두고 docker exec 로 들어간다. 이 줄은 컨테이너 밖에서 돌린다
docker run --name permlab -d debian:12 sleep infinity
docker exec -it permlab bash

# 파일을 만들 alice, 읽으려는 www, 그룹 ops 와 작업 디렉터리를 만든다
apt-get update -qq && apt-get install -y -qq acl
useradd -m -s /bin/bash alice
useradd -m -s /bin/bash www
groupadd ops
mkdir -p /srv/lab
chown alice:alice /srv/lab
chmod 755 /srv/lab

# 이후 예는 아래 「로그인 셸에 umask 영구 설정」 까지 alice 셸에서 돌린다
su alice
```

### umask 읽고 바꾸기

> 인자 없이 부르면 지금의 값을 읽고, 인자를 주면 이 셸의 값을 바꿉니다.

`-S` 는 허용되는 권한을 기호로 보이고 `-p` 는 그대로 다시 입력할 수 있는 꼴로 보입니다.[^umask-exit]

```bash
# 지금 값을 8진수로 읽는다
umask    # 0000

# 허용되는 권한을 기호로 읽는다
#   -S   8진수 대신 기호로 출력한다
umask -S    # u=rwx,g=rwx,o=rwx

# 입력으로 다시 쓸 수 있는 꼴로 읽는다
#   -p   값을 읽을 때 umask 명령 꼴로 출력한다
umask -p    # umask 0000

# 8진수로 정하고 두 가지 꼴로 읽는다
umask 027
umask    # 0027
umask -S    # u=rwx,g=rx,o=
umask -p    # umask 0027

# 기호로 정하면 허용할 권한을 적는다. u=rwx,g=rx,o= 는 027 과 같다
umask u=rwx,g=rx,o=
umask    # 0027
```

8진수 `027` 은 끌 비트이고, 기호 `g=rx` 는 남길 권한이라 같은 값을 반대편에서 적은 것입니다.

### 새 파일과 디렉터리의 권한 계산

> 새 파일은 666, 새 디렉터리는 777 에서 umask 의 비트를 끈 권한으로 생깁니다.

`touch` 와 `mkdir` 는 666 과 777 을 요청하고, 커널은 요청한 권한에서 umask 에 든 비트를 끕니다.[^umask-syscall] 파일과 디렉터리 권한을 한 줄씩 찍어 비교합니다.

```bash
# stat -c 로 8진수(%a)와 글자(%A) 권한을 찍는다
#   stat -c   출력 형식을 직접 정한다
cd /srv/lab
for m in 022 027 077; do
  umask $m
  touch f$m
  mkdir d$m
  echo "$m  $(stat -c "%a %A" f$m)  $(stat -c "%a %A" d$m)"
done
```

```bash
022  644 -rw-r--r--  755 drwxr-xr-x
027  640 -rw-r-----  750 drwxr-x---
077  600 -rw-------  700 drwx------
```

앞 열이 umask, 다음 두 칸이 파일, 마지막 두 칸이 디렉터리입니다. `027` 은 파일 `640`, 디렉터리 `750` 입니다.

### 빼기가 아니라 비트 끄기

> umask 는 666·777 에서 값을 빼는 것이 아니라 비트를 꺼서, 파일에 실행 비트가 생기지 않습니다.

`033` 을 뺄셈으로 계산하면 파일이 `633` 이어야 하지만 실제로는 `644` 입니다. 이미 꺼진 비트를 또 끄려 해도 아무 일이 없기 때문입니다.

```bash
# 033 은 파일 666 에서 그룹·그 밖의 모두의 쓰기와 실행 비트를 끈다
umask 033
touch f033
mkdir d033
stat -c "%a %A" f033 d033
```

```bash
644 -rw-r--r--
744 drwxr--r--
```

umask 를 `000` 으로 풀어도 파일은 `777` 이 아니라 `666` 입니다. 끄는 일만 하므로 요청에 없던 실행 비트는 생기지 않습니다. `111` 은 파일에서 끌 비트가 이미 꺼져 있어 `666` 그대로이고 디렉터리에서는 실행 비트가 꺼집니다.

```bash
umask 000
touch f000
mkdir d000
stat -c "%a %A" f000 d000

umask 111
touch f111
mkdir d111
stat -c "%a %A" f111 d111
```

```bash
666 -rw-rw-rw-
777 drwxrwxrwx
666 -rw-rw-rw-
666 drw-rw-rw-
```

실행 비트가 없는 디렉터리 `d111` 은 안으로 들어갈 수 없습니다. 디렉터리에는 `x` 가 이동 권한이므로 umask 를 풀 때는 디렉터리 쪽을 먼저 봅니다.

### 서브셸과 자식 프로세스의 umask

> umask 는 프로세스마다 따로 있어서 서브셸이나 자식에서 바꿔도 부모 셸은 그대로입니다.

umask 는 자식 프로세스가 물려받기만 하고 되돌려 주지는 않습니다.

```bash
# 서브셸 안에서만 077 이다. 괄호 밖 umask 는 022 그대로다
umask 022
( umask 077; umask )    # 0077
umask    # 0022

# 자식 bash 가 바꿔도 이 셸은 그대로다
bash -c 'umask 077'
umask    # 0022
```

### 로그인 셸에 umask 영구 설정

> 셸에서 바꾼 umask 는 그 셸이 끝나면 사라지므로, 로그인 때 읽는 파일에 `umask` 줄을 넣어야 남습니다.

로그인 셸은 `~/.profile` 같은 시작 파일을 읽고, `su alice -c` 로 띄운 비로그인 셸은 읽지 않습니다. root 셸에서 `alice` 의 `~/.profile` 에 줄을 넣고 두 가지로 확인합니다.

```bash
# alice 셸을 나와 root 셸로 돌아간다. 이 아래는 「실습 정리」 까지 root 셸에서 돌린다
exit

# alice 의 로그인 시작 파일에 umask 를 넣는다
echo 'umask 027' >> /home/alice/.profile

# 로그인 셸이 아니면 시작 파일을 읽지 않아 부모의 값 0000 이 그대로다
su alice -c umask    # 0000

# 로그인 셸이면 ~/.profile 을 읽어 027 이 된다
#   -l   로그인 셸로 띄운다
su -l alice -c umask    # 0027
```

모든 사용자에게 적용할 자리는 `/etc/profile` 과 `/etc/profile.d/*.sh` 입니다. `/etc/login.defs` 의 `UMASK` 는 `pam_umask` 가 읽는 값입니다.[^pam-umask] 이 컨테이너의 `/etc/pam.d` 에는 `pam_umask` 줄이 없었습니다.

```bash
grep -n '^UMASK' /etc/login.defs    # 151:UMASK		022
grep -rn umask /etc/profile /etc/bash.bashrc /etc/profile.d /etc/pam.d; echo $?    # 1
```

### systemd 서비스의 UMask=

> 서비스는 셸을 거치지 않고 프로그램을 직접 실행하므로 시작 파일의 umask 줄이 닿지 않고, 유닛의 `UMask=` 로 정합니다.

`ExecStart=` 는 셸 명령줄을 직접 지원하지 않아 `~/.profile` 이나 `/etc/profile` 을 읽는 셸이 끼지 않습니다.[^systemd-service] system 유닛의 umask 기본값은 `0022` 이고 `UMask=` 로 바꿉니다.[^systemd-umask] 아래 예는 Debian 12 VM 에서 `systemd-run` 으로 일회성 유닛을 돌려 만든 파일의 권한을 봅니다.

```bash
# 유닛 안의 bash 가 umask 와 새 파일 권한을 찍고, 출력은 저널에서 읽는다
#   --wait       유닛이 끝날 때까지 기다린다
#   --collect    끝난 유닛을 정리한다
#   -p           유닛 속성을 준다
sudo systemd-run --quiet --wait --collect \
  -p Type=oneshot \
  --unit=umask-default \
  bash -c 'umask; touch /tmp/umask-default.f; stat -c %a /tmp/umask-default.f'
sudo journalctl -u umask-default -o cat --no-pager | grep -E '^[0-9]+$'
```

```bash
0022
644
```

`UMask=0077` 을 주면 같은 명령이 `0077` 과 `600` 을 찍습니다. 실행 중인 유닛의 값은 `systemctl show` 로 읽습니다.

```bash
sudo systemd-run --quiet --wait --collect \
  -p Type=oneshot \
  -p UMask=0077 \
  --unit=umask-0077 \
  bash -c 'umask; touch /tmp/umask-0077.f; stat -c %a /tmp/umask-0077.f'
sudo journalctl -u umask-0077 -o cat --no-pager | grep -E '^[0-9]+$'
```

```bash
0077
600
```

```bash
sudo systemd-run --quiet --unit=umask-show -p UMask=0077 sleep 60
systemctl show umask-show -p UMask    # UMask=0077
sudo systemctl stop umask-show
```

유닛 파일에는 `[Service]` 아래에 `UMask=0077` 한 줄을 씁니다. `systemctl edit` 로 만드는 drop-in 도 같은 자리입니다.

### 실습 정리

```bash
# 만든 계정·그룹·작업 디렉터리를 지운다. 「주의사항과 동작 원리」 의 예까지 돌린 뒤에 지운다
userdel -r alice
userdel -r www
groupdel ops
rm -rf /srv/lab

# Debian 12 VM 에서 쓴 임시 파일을 지운다
sudo rm -f /tmp/umask-default.f /tmp/umask-0077.f

# 컨테이너를 나와 지운다. 이 줄은 컨테이너 밖에서 돌린다
exit
docker rm -f permlab
```



## 주의사항과 동작 원리

> umask 를 조이면 다른 계정이 파일을 못 읽는 증상이 생기고, 그때는 umask 를 풀지 않고 그 계정에만 ACL 로 읽기를 줍니다.

### 조인 umask 와 읽지 못하는 다른 계정

> `umask 027` 로 만든 파일은 그 밖의 모두가 못 읽으므로 웹 서버 계정 같은 다른 계정이 거절됩니다.

`alice` 가 `umask 027` 로 파일을 만들면 `www` 는 그룹도 아니고 그 밖의 모두에 든 계정이라 읽을 수 없습니다. 디렉터리 `/srv/lab` 의 `755` 는 들어가는 데는 충분합니다.

```bash
# root 셸에서 alice 로 파일을 만든다
su alice -c "umask 027; echo '<h1>hi</h1>' > /srv/lab/index.html; ls -l /srv/lab/index.html"
```

```bash
-rw-r----- 1 alice alice 12 Nov 17 06:42 /srv/lab/index.html
```

```bash
# www 로 읽는다
su www -c 'cat /srv/lab/index.html'; echo rc=$?    # cat: /srv/lab/index.html: Permission denied / rc=1
```

umask 를 `022` 로 풀면 읽히지만 이후 모든 새 파일이 모두에게 읽힙니다. 대신 `www` 에만 읽기를 주면 `umask` 는 그대로입니다. `setfacl` 의 쓰는 법은 [getfacl·setfacl 참조 시트](./getfacl·setfacl.md)에 있습니다.

```bash
# alice 의 파일에 www 의 읽기 ACL 을 붙인다
su alice -c 'setfacl -m u:www:r-- /srv/lab/index.html'
su www -c 'cat /srv/lab/index.html'; echo rc=$?    # <h1>hi</h1> / rc=0
ls -l /srv/lab/index.html    # -rw-r-----+ 1 alice alice 12 Nov 17 06:42 /srv/lab/index.html
```

위 블록의 `/` 도 여러 줄 출력을 한 줄에 줄여 적은 것입니다. 권한 글자 끝의 `+` 는 ACL 항목이 더 있다는 표시입니다. `+` 의 뜻은 [ls 참조 시트](../file/ls.md#acl-표시-)에 있습니다.

### 디렉터리에 기본 ACL 이 있으면 umask 를 무시

> 부모 디렉터리에 기본 ACL 이 있으면 새 파일의 권한은 umask 가 아니라 그 ACL 로 정해집니다.

`umask(2)` 는 이 경우 umask 를 무시하고 기본 ACL 을 물려받는다고 적습니다.[^umask-syscall] 실측은 [getfacl·setfacl 참조 시트](./getfacl·setfacl.md)의 「기본 ACL 로 새 파일에 ACL 물려주기」 에 있습니다.



## 관련 문서

> 새 파일에 ACL 을 붙이는 시트와 권한 글자를 읽는 시트입니다.

- [getfacl·setfacl 참조 시트](./getfacl·setfacl.md) — umask 를 풀지 않고 특정 계정에만 읽기를 주는 ACL 과 mask
- [ls 참조 시트](../file/ls.md#종류권한acl-글자) — `-l` 의 권한 아홉 자리와 `+` 표시
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경과 각주의 근거 자료입니다.

- 검증 환경: Debian 12 컨테이너(GNU bash 5.2.15, coreutils 9.1, acl 2.3.1), systemd 부분은 Debian 12 VM(systemd 252)
- [umask(2) — Debian bookworm](https://manpages.debian.org/bookworm/manpages-dev/umask.2.en.html), [systemd.exec(5) — Debian bookworm](https://manpages.debian.org/bookworm/systemd/systemd.exec.5.en.html), [systemd.service(5) — Debian bookworm](https://manpages.debian.org/bookworm/systemd/systemd.service.5.en.html), [pam_umask(8) — Debian bookworm](https://manpages.debian.org/bookworm/libpam-modules/pam_umask.8.en.html)

[^umask-syscall]: umask(2) (Linux man-pages 6.03, Debian bookworm) — "The umask is used by open(2), mkdir(2), and other system calls that create files to modify the permissions placed on newly created files or directories. Specifically, permissions in the umask are turned off from the mode argument to open(2) and mkdir(2)", "if the parent directory has a default ACL (see acl(5)), the umask is ignored, the default ACL is inherited". https://manpages.debian.org/bookworm/manpages-dev/umask.2.en.html
[^umask-exit]: GNU bash 5.2.15 `help umask` (Debian 12) — "If MODE begins with a digit, it is interpreted as an octal number; otherwise it is a symbolic mode string like that accepted by chmod(1)", "-p if MODE is omitted, output in a form that may be reused as input", "-S makes the output symbolic; otherwise an octal number is output", "Returns success unless MODE is invalid or an invalid option is given." 모르는 옵션의 2 는 `bash.info` Exit Status 의 "All builtins return an exit status of 2 to indicate incorrect usage" 이고, 잘못된 mode 의 1 은 이 시트의 실측입니다. https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html
[^pam-umask]: pam_umask(8) (Linux-PAM 1.5.2, Debian bookworm) — "pam_umask is a PAM module to set the file mode creation mask of the current environment", "The PAM module tries to get the umask value from the following places in the following order: umask= entry in the user's GECOS field, umask= argument, UMASK entry from /etc/login.defs, UMASK= entry from /etc/default/login". 이 컨테이너에서 `/etc/pam.d` 에 `umask` 문자열이 없다는 것만 확인했고, `login.defs` 의 `UMASK` 가 로그인 umask 로 쓰이는지는 실측하지 않았습니다. https://manpages.debian.org/bookworm/libpam-modules/pam_umask.8.en.html
[^systemd-service]: systemd.service(5) (systemd 252, Debian bookworm), `ExecStart=` — "Note that shell command lines are not directly supported. If shell command lines are to be used, they need to be passed explicitly to a shell implementation of some kind." https://manpages.debian.org/bookworm/systemd/systemd.service.5.en.html
[^systemd-umask]: systemd.exec(5) (systemd 252, Debian bookworm), `UMask=` — "Controls the file mode creation mask. Takes an access mode in octal notation. See umask(2) for details. Defaults to 0022 for system units." https://manpages.debian.org/bookworm/systemd/systemd.exec.5.en.html
