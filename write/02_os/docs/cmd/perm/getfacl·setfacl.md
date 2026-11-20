---
title: getfacl·setfacl 참조 시트
tags: [linux, cheatsheet, acl, getfacl, setfacl, mask, file-mode, permission, cli, reference]
status: draft
source:
  - getfacl(1)·setfacl(1)·acl(5) (acl 2.3.1, Debian bookworm)
  - umask(2) (Linux man-pages 6.03, Debian bookworm)
  - cp(1) (GNU coreutils 9.1), tar(1) (GNU tar 1.34), rsync(1) (rsync 3.5.0) 의 ACL 보존 옵션
related:
  - ./umask.md
  - ../file/ls.md
  - ../README.md
updated: 2026-11-17
---

# getfacl·setfacl 참조 시트

---

> 소유자·그룹·그 밖의 모두 세 칸으로 모자랄 때 특정 계정에만 권한을 더하는 `getfacl`·`setfacl` 과 그 상한인 mask 를 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `setfacl` 은 파일에 사용자·그룹별 권한 항목(ACL)을 더하고 `getfacl` 은 그 항목을 읽습니다.

`getfacl`·`setfacl` 은 Debian·Ubuntu 에서 `acl` 패키지의 외부 바이너리입니다. 출력은 Debian 12 컨테이너에서 받았고 `apt-get install -y acl` 로 `acl` 을 넣었습니다. 도구 버전은 acl 2.3.1, GNU coreutils 9.1, GNU tar 1.34, rsync 3.5.0 입니다.

파일 소유자는 root 이고, 읽는 계정 `www` 가 `su www -c` 로 파일을 열어 봅니다. umask 의 뜻은 [umask 참조 시트](./umask.md)에, `ls -l` 의 `+` 는 [ls 참조 시트](../file/ls.md#acl-표시-)에 있습니다.



## 핵심 문법

> `setfacl` 은 `-m` 으로 항목을 더하거나 바꾸고 `-x`·`-b` 로 지우며, `getfacl` 은 항목과 실효 권한을 읽습니다.

```bash
# 호출 형태. getfacl --help 와 setfacl --help 의 Usage 줄이다
getfacl [-aceEsRLPtpndvh] file ...
setfacl [-bkndRLP] { -m|-M|-x|-X ... } file ...

# 파일의 ACL 을 읽는다 (사용자에게 접근 권한 주기)
getfacl 파일

# 사용자·그룹 항목을 더한다 (사용자에게 접근 권한 주기, 그룹에 접근 권한 주기)
setfacl -m u:사용자:rw- 파일
setfacl -m g:그룹:r-x 파일

# mask 를 읽고 바꾼다 (mask 로 깎인 실효 권한 읽기, mask 를 다시 올리기)
setfacl -m m::rwx 파일
setfacl -n -m u:사용자:rwx 파일

# 항목을 지운다 (ACL 항목 지우기)
setfacl -x u:사용자 파일
setfacl -b 파일

# 디렉터리 아래까지 한꺼번에 준다 (하위 디렉터리까지 주기)
setfacl -R -m u:사용자:r-X 디렉터리

# 앞으로 생길 파일에 물려줄 기본 ACL 을 정한다 (기본 ACL 로 새 파일에 ACL 물려주기)
setfacl -d -m u:사용자:r-X 디렉터리
setfacl -k 디렉터리

# 복사하면서 ACL 을 남긴다 (ACL 을 남기며 복사하기)
cp -a 원본 사본
tar --acls -cf 묶음.tar 파일
rsync -aA 원본 사본
```

### getfacl 출력의 항목 읽기

```bash
# getfacl 이 한 줄에 항목 하나를 찍는다. 종류:이름:권한 꼴이고 이름이 비면 소유자·소유 그룹이다
# user::rw-        소유자 항목
# user:www:r--     이름 붙은 사용자 항목
# group::r--       소유 그룹 항목
# group:ops:r-x    이름 붙은 그룹 항목
# mask::r-x        이름 붙은 사용자·그룹과 소유 그룹 항목의 상한
# other::r--       그 밖의 모두 항목
# default:...      디렉터리가 새 파일에 물려줄 기본 ACL 항목
# #effective:r--   그 항목이 mask 에 깎인 뒤 실제로 통하는 권한
```



## 종료 코드

> `getfacl` 은 파일을 못 찾으면 1 이고, `setfacl` 은 항목 문법이 틀리면 2 입니다.

두 명령의 man 에는 종료 코드 절이 없어서 아래 값은 실측입니다.[^acl-exit] `m.txt` 는 「그룹에 접근 권한 주기」 에서 만드는 파일이라, 그 예까지 돌린 뒤에 이 블록을 돌립니다.

```bash
# 0  성공
# 1  getfacl 이 파일을 못 찾았다
# 2  setfacl 의 항목 문법이 틀렸다(없는 사용자 이름 포함)
getfacl /no/such; echo $?    # getfacl: /no/such: No such file or directory / 1
setfacl -m u:www:rwz m.txt; echo $?    # setfacl: Option -m: Invalid argument near character 9 / 2
setfacl -m u:nosuch:r-- m.txt; echo $?    # setfacl: Option -m: Invalid argument near character 3 / 2
setfacl -m u:www:r-- m.txt; echo $?    # 0
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다.



## 유스케이스

> 예는 앞 예가 만든 상태를 이어 쓰므로 위에서 아래로 차례로 돌립니다.

### 실습 준비

> 아래 블록을 한 번 붙여 넣으면 이 시트의 예가 쓰는 계정과 디렉터리가 생깁니다.

Debian 12 컨테이너의 root 셸에서 돌립니다. 파일은 root 소유로 만들고 `www` 로 열어 확인합니다. 출력은 `docker exec` 로 들어간 셸에서 받았습니다.

```bash
# 컨테이너를 띄워 두고 docker exec 로 들어간다. 이 줄은 컨테이너 밖에서 돌린다
docker run --name acllab -d debian:12 sleep infinity
docker exec -it acllab bash

# 읽는 계정 www·bob, 그룹 ops 와 작업 디렉터리를 만든다. rsync 는 마지막 복사 예에서 쓴다
apt-get update -qq && apt-get install -y -qq acl rsync
useradd -m -s /bin/bash www
useradd -m -s /bin/bash bob
groupadd ops
mkdir -p /srv/lab
cd /srv/lab
```

### 사용자에게 접근 권한 주기

> `setfacl -m u:사용자:권한` 은 그 사용자에게만 권한 항목을 더하고 `getfacl` 이 그 결과를 보입니다.

`umask 027` 로 만든 파일은 그 밖의 모두에게 권한이 없어 `www` 가 거절됩니다. `-m` 은 항목을 더하거나 바꿉니다.[^setfacl-entries]

```bash
# root 가 umask 027 로 파일을 만들고 www 로 읽어 본다
umask 027
echo hello > report.txt
ls -l report.txt    # -rw-r----- 1 root root 6 Nov 17 06:39 report.txt
su www -c 'cat report.txt'; echo rc=$?    # cat: report.txt: Permission denied / rc=1
```

```bash
# ACL 이 없으면 getfacl 은 ls -l 의 세 칸을 항목으로 풀어 보인다
getfacl report.txt
```

```bash
# file: report.txt
# owner: root
# group: root
user::rw-
group::r--
other::---
```

```bash
# www 에게만 읽기를 준다
#   -m   ACL 항목을 더하거나 바꾼다
setfacl -m u:www:r-- report.txt
ls -l report.txt    # -rw-r-----+ 1 root root 6 Nov 17 06:39 report.txt
su www -c 'cat report.txt'; echo rc=$?    # hello / rc=0
```

`ls -l` 의 `+` 가 ACL 항목이 있다는 표시입니다. `getfacl` 은 `user:www:r--` 과 함께 `mask::r--` 를 새로 보입니다.

```bash
# 위 세 줄 머리(file·owner·group)가 필요 없으면 -c 로 뺀다
#   -c   머리 주석을 찍지 않는다
getfacl -c report.txt
```

```bash
user::rw-
user:www:r--
group::r--
mask::r--
other::---
```

### 그룹에 접근 권한 주기

> `g:그룹:권한` 항목은 그 그룹에 든 계정에 같은 권한을 주고, 항목은 쉼표로 한 번에 여러 개 줍니다.

`-m` 에 쉼표로 이은 사용자·그룹 항목을 한꺼번에 줍니다. `ops` 는 읽기와 실행만, `www` 는 쓰기까지 줍니다.

```bash
umask 022
echo data > m.txt
setfacl -m u:www:rw-,g:ops:r-x m.txt
ls -l m.txt
getfacl m.txt
```

```bash
-rw-rwxr--+ 1 root root 5 Nov 17 06:39 m.txt
# file: m.txt
# owner: root
# group: root
user::rw-
user:www:rw-
group::r--
group:ops:r-x
mask::rwx
other::r--
```

`ls -l` 의 그룹 칸이 `r--` 이 아니라 `rwx` 로 찍힌 것에 주목합니다. 이 칸은 다음 절의 mask 를 보입니다.

### mask 로 깎인 실효 권한 읽기

> mask 는 이름 붙은 사용자·그룹과 소유 그룹 항목이 가질 수 있는 권한의 상한이고, `getfacl` 은 깎인 항목에 `#effective:` 를 붙입니다.

acl(5) 는 mask 가 소유자 항목과 other 항목을 뺀 모든 항목의 최대 접근이라고 정의합니다. ACL 에 mask 가 있으면 파일의 그룹 권한 칸이 mask 에 대응한다고도 적습니다.[^acl-mask] 그래서 `chmod g-w` 는 소유 그룹의 권한이 아니라 mask 의 쓰기 비트를 끕니다.

```bash
# 쓰기가 되는 상태에서 먼저 www 가 덧붙인다
su www -c 'echo x >> m.txt'; echo rc=$?    # rc=0

# 그룹 칸의 쓰기를 끈다
chmod g-w m.txt
ls -l m.txt
getfacl m.txt
```

```bash
-rw-r-xr--+ 1 root root 7 Nov 17 06:39 m.txt
# file: m.txt
# owner: root
# group: root
user::rw-
user:www:rw-	#effective:r--
group::r--
group:ops:r-x
mask::r-x
other::r--
```

`www` 항목은 여전히 `rw-` 로 적혀 있지만 `#effective:r--` 가 실제로 통하는 권한입니다. 쓰기를 시도하면 거절됩니다.

```bash
su www -c 'echo x >> m.txt'; echo rc=$?    # bash: line 1: m.txt: Permission denied / rc=1
```

### mask 를 다시 올리기

> `setfacl -m m::rwx` 는 mask 를 직접 정해 깎인 실효 권한을 되살립니다.

`m::rwx` 는 이름이 빈 mask 항목에 권한 `rwx` 를 주는 꼴입니다. mask 를 올리면 `#effective` 줄이 사라지고 `ls -l` 의 그룹 칸도 같이 바뀝니다.

```bash
setfacl -m m::rwx m.txt
ls -l m.txt
getfacl -c m.txt
su www -c 'echo x >> m.txt'; echo rc=$?    # rc=0
```

```bash
-rw-rwxr--+ 1 root root 7 Nov 17 06:39 m.txt
user::rw-
user:www:rw-
group::r--
group:ops:r-x
mask::rwx
other::r--
```

`setfacl` 은 항목을 바꿀 때 mask 를 따로 주지 않으면 mask 를 다시 계산해, 방금 깎은 상태를 되돌릴 수 있습니다. mask 를 계산하지 않게 하는 `-n` 과 비교합니다.[^setfacl-n]

```bash
# chmod g-w 로 mask 를 r-x 로 깎은 뒤 bob 에게 rwx 를 준다. -n 은 mask 를 다시 계산하지 않는다
#   -n   mask 를 다시 계산하지 않는다
chmod g-w m.txt
setfacl -n -m u:bob:rwx m.txt
getfacl -c m.txt
```

```bash
user::rw-
user:www:rw-	#effective:r--
user:bob:rwx	#effective:r-x
group::r--
group:ops:r-x
mask::r-x
other::r--
```

`bob` 은 `rwx` 를 받았지만 mask 가 `r-x` 로 남아 실효 권한은 `r-x` 입니다. 같은 명령에서 `-n` 을 빼면 mask 가 다시 계산됩니다.

```bash
setfacl -m u:bob:rwx m.txt
getfacl -c m.txt
```

```bash
user::rw-
user:www:rw-
user:bob:rwx
group::r--
group:ops:r-x
mask::rwx
other::r--
```

mask 가 `rwx` 로 되돌아가 앞서 깎은 `www` 의 쓰기도 함께 살아났습니다.

### ACL 항목 지우기

> `-x` 는 항목 하나를, `-b` 는 소유자·그룹·그 밖의 모두 말고 모든 확장 항목을 지웁니다.

`-x` 에는 권한 칸 없이 종류와 이름만 줍니다.[^setfacl-entries] 이때도 mask 는 `-n` 이 없으면 다시 계산됩니다.[^setfacl-n]

```bash
# bob 항목만 지운다
#   -x   지울 항목을 종류와 이름으로 준다
setfacl -x u:bob m.txt
getfacl -c m.txt
```

```bash
user::rw-
user:www:rw-
group::r--
group:ops:r-x
mask::rwx
other::r--
```

```bash
# 확장 항목을 모두 지우면 ls -l 의 + 도 사라진다
#   -b   모든 확장 항목을 지운다
setfacl -b m.txt
getfacl -c m.txt
ls -l m.txt
```

```bash
user::rw-
group::r--
other::r--

-rw-r--r-- 1 root root 9 Nov 17 06:39 m.txt
```

### 하위 디렉터리까지 주기

> `-R` 은 디렉터리 아래의 파일과 디렉터리에 같은 항목을 한꺼번에 줍니다.

권한 글자 `X` 는 대상이 디렉터리이거나 이미 누군가에게 실행 권한이 있을 때만 실행 권한이 됩니다.[^setfacl-d] 아래 파일에는 실행 비트가 없어 `r--` 이, 디렉터리에는 `r-x` 가 붙습니다.

```bash
# 이미 있는 디렉터리 site 아래의 모든 항목에 www 의 읽기를 준다
#   -R   하위 파일과 디렉터리까지 적용한다
umask 077
mkdir -p site/sub
echo a > site/a.txt
echo b > site/sub/b.txt
setfacl -R -m u:www:r-X site
ls -lR site
```

```bash
site:
total 4
-rw-r-----+ 1 root root  2 Nov 17 06:39 a.txt
drwxr-x---+ 1 root root 10 Nov 17 06:39 sub

site/sub:
total 4
-rw-r-----+ 1 root root 2 Nov 17 06:39 b.txt
```

```bash
getfacl -c site/sub/b.txt
```

```bash
user::rw-
user:www:r--
group::---
mask::r--
other::---
```

### 기본 ACL 로 새 파일에 ACL 물려주기

> `-d` 로 디렉터리에 기본 ACL 을 두면 그 안에 앞으로 생길 파일과 디렉터리가 같은 항목을 물려받습니다.

`-d` 는 모든 동작을 기본 ACL 에 적용합니다.[^setfacl-d] 아래 `site` 에는 `umask 077` 이 그대로지만 새 파일에는 `www` 항목이 생깁니다.

```bash
# site 에 기본 ACL 을 둔다
#   -d   동작을 기본 ACL 에 적용한다
setfacl -d -m u:www:r-X site
getfacl -c site
```

```bash
user::rwx
user:www:r-x
group::---
mask::r-x
other::---
default:user::rwx
default:user:www:r-x
default:group::---
default:mask::r-x
default:other::---
```

`default:` 로 시작하는 줄이 기본 ACL 입니다. 새 파일과 새 디렉터리를 만들어 물려받았는지 봅니다.

```bash
echo new > site/new.txt
mkdir site/newdir
ls -ld site/new.txt site/newdir
getfacl -c site/new.txt
su www -c 'cat site/new.txt'; echo rc=$?    # new / rc=0
```

```bash
-rw-r-----+ 1 root root 4 Nov 17 06:39 site/new.txt
drwxr-x---+ 1 root root 0 Nov 17 06:39 site/newdir
user::rw-
user:www:r-x	#effective:r--
group::---
mask::r--
other::---
```

새 파일은 `user:www:r-x` 를 물려받았지만 파일을 만들며 요청한 권한 `666` 에 실행 비트가 없어 `#effective:r--` 입니다.[^acl-default] 디렉터리에 기본 ACL 이 있으면 umask 는 무시되어 `umask 077` 인데도 `www` 가 읽습니다.[^umask-syscall]

기본 ACL 은 항목 하나만 지우거나 통째로 지울 수 있습니다. 앞은 종류 앞에 `d:` 를 붙이고, 뒤는 `-k` 입니다.

```bash
# 기본 ACL 의 www 항목만 지운다. 남은 default:mask 는 다시 계산되어 ---
setfacl -x d:u:www site
getfacl -c site
```

```bash
user::rwx
user:www:r-x
group::---
mask::r-x
other::---
default:user::rwx
default:group::---
default:mask::---
default:other::---
```

```bash
# 기본 ACL 을 통째로 지운다. 일반 ACL 은 그대로다
#   -k   기본 ACL 을 지운다
setfacl -k site
getfacl -c site
```

```bash
user::rwx
user:www:r-x
group::---
mask::r-x
other::---
```

### ACL 을 남기며 복사하기

> `cp` 와 `tar`·`rsync` 는 옵션을 주지 않으면 ACL 을 버리므로 `cp -a`·`tar --acls`·`rsync -A` 를 줍니다.

옵션 뜻은 각 명령의 man 에 있고, 여기서는 사본에 `www` 항목이 남았는지만 봅니다.[^keep-acl] 항목이 없으면 `none` 을 찍게 했습니다.

```bash
umask 022
echo v > src.txt
setfacl -m u:www:r-- src.txt

# cp 는 옵션 없이는 ACL 을 남기지 않고 -a 는 남긴다
cp src.txt c1.txt; getfacl -c c1.txt | grep www || echo none    # none
cp -a src.txt c2.txt; getfacl -c c2.txt | grep www || echo none    # user:www:r--

# tar 는 만들 때와 풀 때 모두 --acls 를 줘야 남는다
tar -cf p.tar src.txt; mkdir t1; tar -xf p.tar -C t1; getfacl -c t1/src.txt | grep www || echo none    # none
tar --acls -cf q.tar src.txt; mkdir t2; tar --acls -xf q.tar -C t2; getfacl -c t2/src.txt | grep www || echo none    # user:www:r--

# rsync 는 -a 만으로는 남기지 않고 -A 를 더한다
mkdir r1; rsync -a src.txt r1/; getfacl -c r1/src.txt | grep www || echo none    # none
mkdir r2; rsync -aA src.txt r2/; getfacl -c r2/src.txt | grep www || echo none    # user:www:r--
```

### 실습 정리

```bash
# 만든 파일·디렉터리·계정·그룹을 지운다
cd /
rm -rf /srv/lab
userdel -r www
userdel -r bob
groupdel ops

# 컨테이너를 나와 지운다. 이 줄은 컨테이너 밖에서 돌린다
exit
docker rm -f acllab
```



## 주의사항과 동작 원리

> `+` 가 붙은 파일의 `ls -l` 그룹 칸은 소유 그룹이 아니라 mask 이고, `chmod` 와 `setfacl` 이 서로의 결과를 바꿉니다.

### ACL 이 있는 파일의 chmod 와 그룹 칸

> ACL 이 있는 파일에 `chmod g±w` 를 하면 소유 그룹 항목이 아니라 mask 가 바뀌어 이름 붙은 항목의 실효 권한이 함께 바뀝니다.

「mask 로 깎인 실효 권한 읽기」 에서 `chmod g-w` 하나가 `www` 의 쓰기를 막았습니다. acl(5) 는 그룹 칸이 mask 가 있으면 `ACL_MASK` 에 대응하고, 파일 권한 비트를 바꾸면 대응하는 ACL 항목이 바뀐다고 적습니다.[^acl-mask] `ls -l` 만 보고 "그룹은 `r-x` 니까 쓰기가 안 된다"고 읽으면 틀립니다. 소유 그룹의 실제 권한은 `getfacl` 의 `group::` 줄이 보입니다.

### setfacl 이 mask 를 다시 계산하는 때

> 항목을 더하거나 지우면 `setfacl` 이 mask 를 다시 계산해 앞서 `chmod` 로 깎아 둔 mask 가 되돌아갈 수 있습니다.

`-n` 이나 `m::` 항목을 같이 주지 않으면 `setfacl` 은 mask 를 이름 붙은 항목과 소유 그룹 항목의 합집합으로 다시 정합니다.[^setfacl-n] 「mask 를 다시 올리기」 에서 `-n` 없이 `bob` 을 더하자 `r-x` 였던 mask 가 `rwx` 가 되었습니다. 깎아 둔 상한을 지키려면 `-n` 을 주거나 항목을 바꾼 뒤 `m::` 으로 mask 를 다시 정합니다.



## 관련 문서

> umask 와 ACL 이 어떻게 맞물리는지와 권한 글자를 읽는 시트입니다.

- [umask 참조 시트](./umask.md) — umask 를 조여 다른 계정이 못 읽을 때 ACL 로 푸는 흐름
- [ls 참조 시트](../file/ls.md#종류권한acl-글자) — `-l` 의 권한 아홉 자리와 `+`, 그룹 칸이 mask 인 점
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경과 각주의 근거 자료입니다.

- 검증 환경: Debian 12 컨테이너(acl 2.3.1-3, GNU coreutils 9.1, GNU tar 1.34, rsync 3.5.0+ds1)
- [getfacl(1)](https://manpages.debian.org/bookworm/acl/getfacl.1.en.html), [setfacl(1)](https://manpages.debian.org/bookworm/acl/setfacl.1.en.html), [acl(5)](https://manpages.debian.org/bookworm/acl/acl.5.en.html) — Debian bookworm, 2026-11-17 조회

[^acl-exit]: setfacl(1) (acl 2.3.1, Debian bookworm) 의 SYNOPSIS·DESCRIPTION·OPTIONS·EXAMPLES·CONFORMANCE·AUTHOR·SEE ALSO 절에는 EXIT STATUS 절이 없고, ACL 을 지원하지 않는 파일시스템에서 "returns with an exit status greater than 0" 라는 문장만 있습니다. 1·2 는 이 시트의 실측입니다(Debian 12 컨테이너). https://manpages.debian.org/bookworm/acl/setfacl.1.en.html
[^setfacl-entries]: setfacl(1) (acl 2.3.1, Debian bookworm), ACL ENTRIES — "The -m (--modify) and -M (--modify-file) options modify the ACL of a file or directory. ACL entries for this operation must include permissions.", "The -x (--remove) and -X (--remove-file) options remove ACL entries. It is not an error to remove an entry which does not exist. Only ACL entries without the perms field are accepted as parameters". https://manpages.debian.org/bookworm/acl/setfacl.1.en.html
[^acl-mask]: acl(5) (acl 2.3.1, Debian bookworm) — "A mask ACL entry specifies the maximum access which can be granted by any ACL entry except the user entry for the file owner and the other entry", "If the ACL has an ACL_MASK entry, the group permissions correspond to the permissions of the ACL_MASK entry. Otherwise, if the ACL has no ACL_MASK entry, the group permissions correspond to the permissions of the ACL_GROUP_OBJ entry", "Modification of the file permission bits results in the modification of the associated ACL entries". https://manpages.debian.org/bookworm/acl/acl.5.en.html
[^setfacl-n]: setfacl(1) (acl 2.3.1, Debian bookworm), -n — "Do not recalculate the effective rights mask. The default behavior of setfacl is to recalculate the ACL mask entry, unless a mask entry was explicitly given. The mask entry is set to the union of all permissions of the owning group, and all named user and group entries." getfacl(1) 의 출력 예에서 깎인 항목 뒤에 `#effective:r-x` 가 붙습니다. https://manpages.debian.org/bookworm/acl/setfacl.1.en.html
[^setfacl-d]: setfacl(1) (acl 2.3.1, Debian bookworm), -d — "All operations apply to the Default ACL. Regular ACL entries in the input set are promoted to Default ACL entries."; -b — "Remove all extended ACL entries. The base ACL entries of the owner, group and others are retained."; -k — "Remove the Default ACL."; -R — "Apply operations to all files and directories recursively." ACL ENTRIES — "The character X stands for the execute permission if the file is a directory or already has execute permission for some user." https://manpages.debian.org/bookworm/acl/setfacl.1.en.html
[^acl-default]: acl(5) (acl 2.3.1, Debian bookworm), OBJECT CREATION AND DEFAULT ACLs — "The new object inherits the default ACL of the containing directory as its access ACL. The access ACL entries corresponding to the file permission bits are modified so that they contain no permissions that are not contained in the permissions specified by the mode parameter." https://manpages.debian.org/bookworm/acl/acl.5.en.html
[^umask-syscall]: umask(2) (Linux man-pages 6.03, Debian bookworm) — "if the parent directory has a default ACL (see acl(5)), the umask is ignored, the default ACL is inherited, the permission bits are set based on the inherited ACL, and permission bits absent in the mode argument are turned off." https://manpages.debian.org/bookworm/manpages-dev/umask.2.en.html
[^keep-acl]: cp(1) (GNU coreutils 9.1) — "-a, --archive same as -dR --preserve=all"; tar(1) (GNU tar 1.34) — "--acls Enable POSIX ACLs support."; rsync(1) — "--acls, -A preserve ACLs (implies --perms)". 설치된 rsync 는 3.5.0 이고 man 은 Debian bookworm 판입니다. https://manpages.debian.org/bookworm/coreutils/cp.1.en.html, https://manpages.debian.org/bookworm/tar/tar.1.en.html, https://manpages.debian.org/bookworm/rsync/rsync.1.en.html
