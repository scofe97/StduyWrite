---
title: ls 참조 시트
tags: [linux, cheatsheet, ls, file-mode, acl, cli, reference]
status: draft
source:
  - GNU coreutils ls (`--help` 원문·`info coreutils` 의 "ls invocation", coreutils 9.7) · ls(1)
  - 《Learning Modern Linux》 4장 "Access Control"·8장 "Logs and Monitoring"(Michael Hausenblas, O'Reilly, 2022)의 `ls -al` 예
related:
  - ../README.md
  - ../../../book/learning-modern-linux/04-01.전부%20아니면%20전무에서%20잘게%20쪼개는%20쪽으로.md
  - ../../../book/learning-modern-linux/08-01.재는%20것은%20바깥이고%20알고%20싶은%20것은%20안이다.md
  - ../text/head%C2%B7tail.md
updated: 2026-11-16
---

# ls 참조 시트

---

> 디렉터리의 내용을 나열하고, 긴 목록(`-l`)의 열로 종류·권한·소유자·크기·시각을 읽는 `ls` 사용법을 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `ls` 는 파일 이름을 나열하고, `-l` 을 주면 파일마다 한 줄에 종류·권한·링크 수·소유자·그룹·크기·시각을 보입니다.

GNU coreutils 의 외부 바이너리입니다. 이 시트는 Ubuntu 26.04 VM(OrbStack)에서 GNU 판 9.7 로 실측했습니다. 이 VM 에서 GNU 판은 `gnu-coreutils` 패키지의 `/usr/bin/gnuls` 입니다. 이 VM 의 기본 `ls` 는 Rust 로 다시 쓴 uutils 0.10.0 이라 「실습 준비」 가 GNU 판을 `ls` 로 불러 쓰게 합니다.[^uutils] Debian·Rocky 의 `ls` 는 GNU 판이라 그 준비가 필요 없습니다. macOS 의 `ls` 는 BSD 판이라 `--time-style` 이 없고 `-T` 로 시각을 길게 찍습니다.[^bsd-ls]

값은 `LC_ALL=C.UTF-8`·`TZ=UTC` 로 고정해 받았습니다. 파일 종류·권한 글자의 뜻은 GNU 매뉴얼에 있습니다.[^ls-info]



## 핵심 문법

> 파일 인자로 무엇을 나열할지 정하고, 옵션으로 어떤 칸을 보일지와 어떤 순서로 둘지를 정합니다.

```bash
# 호출 형태
ls [OPTION]... [FILE]...

# 긴 목록으로 칸을 읽는다 (긴 목록의 열 읽기, 파일 종류 글자)
ls -l 파일...

# 디렉터리의 내용이 아니라 디렉터리 자체를 본다 (디렉터리 자체 보기)
ls -ld 디렉터리...

# 링크 수와 inode 번호를 본다 (링크 수와 inode)
ls -li 파일...

# 심볼릭 링크가 가리키는 파일의 정보를 본다 (심볼릭 링크가 가리키는 곳)
ls -lL 링크...

# 숨김 파일까지 나열한다 (숨김 파일 보기)
ls -1 -a [디렉터리]

# 이름 뒤에 종류 기호를 붙인다 (이름 뒤 종류 기호)
ls -1 -F [디렉터리]

# 크기를 K·M 단위로 찍는다 (사람이 읽는 크기)
ls -lh 파일...

# 시각이나 크기 순으로 놓는다 (정렬)
ls -lt [디렉터리]

# 시각 형식을 고른다 (시각 형식)
ls -l --time-style=형식 파일...

# 소유자·그룹을 숫자 ID 로 찍는다 (숫자 ID 로 보기)
ls -ln 파일...

# 하위 디렉터리까지 나열한다 (하위 디렉터리까지 나열)
ls -1 -R 디렉터리
```

### 종류·권한·ACL 글자

> `-l` 의 첫 열에서 본문에 나온 글자만 모았습니다.

뜻은 GNU 매뉴얼 "What information is listed" 를 따랐습니다.[^ls-info]

```bash
# -l 한 줄의 첫 열은 "종류 한 글자 + 권한 아홉 자리 + 대체 접근 표시 한 자리" 다
# -  일반 파일
# d  디렉터리
# l  심볼릭 링크
# s  소켓
# p  FIFO(이름 있는 파이프)
# b  블록 특수 파일
# c  문자 특수 파일
# 권한 아홉 자리는 소유자·그룹·그 밖의 모두 순서이고 자리마다 r w x - 중 하나다
# 실행 자리(셋째·여섯째·아홉째)에는 다음 글자가 올 수 있다
# s  setuid·setgid 비트와 실행 비트가 모두 켜짐
# S  setuid·setgid 비트만 켜지고 실행 비트는 꺼짐
# t  sticky 비트와 그 밖의 모두의 실행 비트가 모두 켜짐
# T  sticky 비트만 켜지고 그 밖의 모두의 실행 비트는 꺼짐
# 권한 뒤 한 자리는 대체 접근 방법(ACL 등)의 표시다
# +  ACL 같은 대체 접근 방법이 있다
# .  보안 컨텍스트(SELinux)만 있다
#    (공백)  없다
```



## 종료 코드

> `ls` 는 이상 없으면 0, 하위 디렉터리를 못 여는 것 같은 작은 문제면 1, 명령줄 인자에 접근하지 못하는 것 같은 심각한 문제면 2 를 돌려줍니다.[^ls-exit]

아래 예는 「실습 준비」 에서 만든 파일로 돌립니다. 옵션은 `--help` 의 설명을 따랐습니다.[^ls-help]

```bash
# 0  이상 없음
# 1  작은 문제. 예: 하위 디렉터리를 열 수 없음
# 2  심각한 문제. 예: 명령줄에 준 인자에 접근할 수 없음

# 0: 있는 파일
ls app.conf > /dev/null; echo $?    # 0

# 2: 없는 파일
ls missing.txt; echo $?    # ls: cannot access 'missing.txt': No such file or directory / 2

# 2: 모르는 옵션
ls --badopt; echo $?    # ls: unrecognized option '--badopt' / Try 'ls --help' for more information. / 2

# 1: 하위 디렉터리를 못 연 경우. appuser 는 tree/locked 를 열 수 없다
#   -R   하위 디렉터리까지 나열한다
#   runuser -u appuser --   뒤의 명령을 appuser 권한으로 실행한다
runuser -u appuser -- ls -R tree > /dev/null; echo $?    # ls: cannot open directory 'tree/locked': Permission denied / 1

# 2: 같은 디렉터리를 명령줄 인자로 준 경우
runuser -u appuser -- ls tree/locked; echo $?    # ls: cannot open directory 'tree/locked': Permission denied / 2
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다. 같은 `tree/locked` 를 `-R` 로 만나면 1, 인자로 주면 2 가 되어 인자 자체가 문제인지 아래 단계의 문제인지 코드로 갈립니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션만 씁니다.

### 실습 준비

> 아래 블록을 root 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 파일이 모두 `/tmp/lab-ls` 에 생깁니다.

Ubuntu 26.04 의 OrbStack VM 에서 `sudo -i` 로 연 root 셸에서 실행합니다. 새 셸을 열면 블록 앞쪽의 `export` 두 줄을 다시 치고 `/tmp/lab-ls` 로 옮겨 갑니다.

```bash
# 정렬 순서와 시각이 시트와 같도록 로케일과 시간대를 정한다
export LC_ALL=C.UTF-8 TZ=UTC

# 이 VM 의 기본 ls 는 uutils 라서 GNU 판(gnuls)을 ls 로 먼저 잡히게 한다
# ls 가 이미 GNU 판인 Debian·Rocky 에서는 이 두 줄이 필요 없다
mkdir -p /tmp/gnu-bin && ln -sf /usr/bin/gnuls /tmp/gnu-bin/ls
export PATH=/tmp/gnu-bin:$PATH

# 「ACL 표시 +」 의 getfacl 이 든 acl 패키지. 이미 있으면 그대로 둔다
apt-get -o DPkg::Lock::Timeout=300 install -y acl

# 소유자·그룹으로 쓸 appuser 와 devs. 번호를 고정해 「숫자 ID 로 보기」 값이 같게 한다
groupadd -g 2001 devs
useradd -u 2001 -g devs appuser

mkdir -p /tmp/lab-ls && cd /tmp/lab-ls

# 크기가 다른 일반 파일 여섯 개(「종료 코드」·「긴 목록의 열 읽기」부터 여러 곳)
head -c 1234    /dev/zero > app.conf
head -c 2048    /dev/zero > deploy.sh
head -c 512     /dev/zero > report.txt
head -c 3145728 /dev/zero > data.bin
head -c 800     /dev/zero > old.log
head -c 30      /dev/zero > .hidden-note
chmod 644 app.conf; chmod 755 deploy.sh; chmod 640 report.txt
chmod 664 data.bin; chmod 644 old.log; chmod 600 .hidden-note
chown appuser:devs app.conf deploy.sh data.bin old.log .hidden-note
chown appuser:root report.txt

# 하드 링크, 심볼릭 링크, 끊어진 링크(「링크 수와 inode」·「심볼릭 링크가 가리키는 곳」)
ln app.conf app.hard
ln -s app.conf app.lnk
ln -s missing.txt dangling.lnk

# FIFO 와 유닉스 소켓(「파일 종류 글자」)
mkfifo jobs.pipe
python3 -c "import socket; s=socket.socket(socket.AF_UNIX); s.bind('app.sock')"

# 디렉터리 다섯 개: logs(setgid), pub(sticky), shared(sticky, 그 밖의 모두 실행 없음),
# tools(setuid·setgid 실행 파일), tree(「하위 디렉터리까지 나열」)
mkdir logs pub shared tools
truncate -s 100 tools/suid-tool tools/nox-tool tools/sgid-tool
chmod 4755 tools/suid-tool
chmod 4644 tools/nox-tool
chmod 2755 tools/sgid-tool
chmod 2755 logs; chown root:devs logs
chmod 1777 pub
chmod 1770 shared; chown appuser:devs shared

# logs 에 ACL 항목 하나를 더한다(「ACL 표시 +」)
setfacl -m u:appuser:rwx logs

# tree 안의 locked 는 root 밖에는 열 수 없다(「종료 코드」)
mkdir -p tree/a tree/b/c tree/locked
truncate -s 10 tree/a/x.txt tree/b/y.txt tree/b/c/z.txt
chmod 000 tree/locked

# 시각을 고정한다. 디렉터리는 안에 파일이 생길 때 바뀌므로 맨 뒤에 맞춘다
touch -d "2026-11-10 09:30" app.conf app.hard
touch -d "2026-11-12 18:05" deploy.sh
touch -d "2026-11-14 08:00" report.txt
touch -d "2026-10-20 14:00" data.bin
touch -d "2021-01-24 12:00" old.log
touch -d "2026-11-01 00:00" .hidden-note
touch -h -d "2026-11-02 10:00" app.lnk dangling.lnk
touch -d "2026-11-03 11:00" jobs.pipe app.sock
touch -d "2026-11-05 07:00" tools/*
touch -d "2026-11-04 12:00" tree/a/x.txt tree/b/y.txt tree/b/c/z.txt
touch -d "2026-11-06 07:00" \
  tools logs pub shared \
  tree tree/a tree/b tree/b/c tree/locked
touch -d "2026-11-15 12:00" .
```

### 긴 목록의 열 읽기

> `-l` 한 줄은 종류와 권한, 링크 수, 소유자, 그룹, 크기, 수정 시각, 이름 순서입니다.

```bash
# 파일 셋의 긴 목록. 첫 줄 app.conf 를 앞에서부터 읽는다
#   -rw-r--r--   종류 `-` 와 권한 아홉 자리(소유자 rw-, 그룹 r--, 그 밖의 모두 r--)
#   2            하드 링크 수
#   appuser      소유자
#   devs         그룹
#   1234         크기(바이트)
#   Nov 10 09:30 마지막 수정 시각(mtime)
#   -l   긴 목록으로 찍는다
ls -l app.conf deploy.sh report.txt
```

```bash
-rw-r--r-- 2 appuser devs 1234 Nov 10 09:30 app.conf
-rwxr-xr-x 1 appuser devs 2048 Nov 12 18:05 deploy.sh
-rw-r----- 1 appuser root  512 Nov 14 08:00 report.txt
```

`deploy.sh` 는 실행 비트가 셋 모두 켜져 있습니다. `report.txt` 는 그룹이 `root` 라 소유자가 아닌 `devs` 구성원은 그 밖의 모두 자리(`---`)를 받아 읽을 수 없습니다.

### 파일 종류 글자

> 첫 글자가 파일 종류이고, 장치 파일은 크기 칸에 주 번호와 부 번호가 나옵니다.

```bash
# 실습 폴더 전체의 긴 목록
ls -l
```

```bash
total 3092
-rw-r--r--  2 appuser devs    1234 Nov 10 09:30 app.conf
-rw-r--r--  2 appuser devs    1234 Nov 10 09:30 app.hard
lrwxrwxrwx  1 root    root       8 Nov  2 10:00 app.lnk -> app.conf
srwxr-xr-x  1 root    root       0 Nov  3 11:00 app.sock
lrwxrwxrwx  1 root    root      11 Nov  2 10:00 dangling.lnk -> missing.txt
-rw-rw-r--  1 appuser devs 3145728 Oct 20 14:00 data.bin
-rwxr-xr-x  1 appuser devs    2048 Nov 12 18:05 deploy.sh
prw-r--r--  1 root    root       0 Nov  3 11:00 jobs.pipe
drwxrwsr-x+ 2 root    devs      40 Nov  6 07:00 logs
-rw-r--r--  1 appuser devs     800 Jan 24  2021 old.log
drwxrwxrwt  2 root    root      40 Nov  6 07:00 pub
-rw-r-----  1 appuser root     512 Nov 14 08:00 report.txt
drwxrwx--T  2 appuser devs      40 Nov  6 07:00 shared
drwxr-xr-x  2 root    root     100 Nov  6 07:00 tools
drwxr-xr-x  5 root    root     100 Nov  6 07:00 tree
```

`total 3092` 는 이 디렉터리 파일들이 차지한 할당 블록의 합(1024바이트 단위)이고 하드 링크도 따로 셉니다.[^ls-info] 링크 줄은 `->` 뒤에 가리키는 이름을 보이며, `dangling.lnk` 처럼 대상이 없어도 그대로 보입니다.

```bash
# 문자 특수 파일(c)과 블록 특수 파일(b). 크기 칸이 "주 번호, 부 번호" 로 바뀐다
ls -l /dev/null /dev/vdb1
```

```bash
crw-rw-rw- 1 root root   1,  3 Nov 16 01:05 /dev/null
brw-rw---- 1 root disk 254, 17 Nov 16 01:05 /dev/vdb1
```

위 두 줄은 이 VM 의 값이라 장치 이름·번호·시각은 환경마다 다릅니다.

### 디렉터리 자체 보기

> `-d` 를 주면 디렉터리의 내용이 아니라 디렉터리 자신의 줄이 나옵니다.

```bash
# 인자가 디렉터리면 ls 는 그 안을 나열한다. logs 는 비어 있어 total 줄만 나온다
ls -l logs    # total 0

# 디렉터리 자신의 소유자·권한·시각을 본다
#   -d   디렉터리의 내용 대신 디렉터리 자체를 나열한다
ls -ld logs    # drwxrwsr-x+ 2 root devs 40 Nov  6 07:00 logs

# 셸의 */ 가 디렉터리 이름만 골라 넘기고, -d 가 그 안 대신 디렉터리 자신을 보인다
ls -ld */
```

```bash
drwxrwsr-x+ 2 root    devs  40 Nov  6 07:00 logs/
drwxrwxrwt  2 root    root  40 Nov  6 07:00 pub/
drwxrwx--T  2 appuser devs  40 Nov  6 07:00 shared/
drwxr-xr-x  2 root    root 100 Nov  6 07:00 tools/
drwxr-xr-x  5 root    root 100 Nov  6 07:00 tree/
```

### 특수 비트 s·S·t·T

> 실행 자리의 `s`·`S`·`t`·`T` 는 setuid·setgid·sticky 비트를 보입니다.

```bash
# 실행 파일 셋과 디렉터리 둘의 특수 비트. 인자는 이름순으로 정렬되어 나온다
ls -ld \
  tools/suid-tool tools/nox-tool tools/sgid-tool \
  pub shared
```

```bash
drwxrwxrwt 2 root    root  40 Nov  6 07:00 pub
drwxrwx--T 2 appuser devs  40 Nov  6 07:00 shared
-rwSr--r-- 1 root    root 100 Nov  5 07:00 tools/nox-tool
-rwxr-sr-x 1 root    root 100 Nov  5 07:00 tools/sgid-tool
-rwsr-xr-x 1 root    root 100 Nov  5 07:00 tools/suid-tool
```

`suid-tool` 은 실행하면 소유자인 root 의 권한으로 돕니다. `nox-tool` 의 `S` 와 `shared` 의 `T` 는 특수 비트만 켜지고 그 자리의 실행 비트는 꺼진 모양입니다.

### ACL 표시 +

> 권한 뒤의 `+` 는 기본 세 항목 말고 ACL 항목이 더 있다는 표시이고, 그때 그룹 자리는 mask 를 보입니다.

```bash
# logs 는 chmod 2755 로 만들었다. 그룹 자리는 r-s 일 텐데 rws 로 찍힌다
ls -ld logs    # drwxrwsr-x+ 2 root devs 40 Nov  6 07:00 logs

# ACL 항목을 읽는다. getfacl 은 acl 패키지의 명령이다
getfacl logs
```

```bash
# file: logs
# owner: root
# group: devs
# flags: -s-
user::rwx
user:appuser:rwx
group::r-x
mask::rwx
other::r-x
```

`ls -l` 이 그룹 자리에 보이는 것은 소유 그룹의 권한(`group::r-x`)이 아니라 mask(`mask::rwx`)입니다.[^acl-mask] 그래서 `+` 가 붙은 줄의 그룹 자리는 실제 그룹 권한과 다를 수 있고, 정확한 값은 `getfacl` 로 읽습니다.

### 링크 수와 inode

> 하드 링크는 같은 inode 를 가리키는 두 번째 이름이라 링크 수가 2 가 되고, 심볼릭 링크는 따로 inode 를 가집니다.

```bash
# 이름 앞에 inode 번호를 붙인다
#   -i   각 파일의 inode 번호를 이름 왼쪽에 찍는다
ls -li app.conf app.hard app.lnk
```

```bash
1466 -rw-r--r-- 2 appuser devs 1234 Nov 10 09:30 app.conf
1466 -rw-r--r-- 2 appuser devs 1234 Nov 10 09:30 app.hard
1472 lrwxrwxrwx 1 root    root    8 Nov  2 10:00 app.lnk -> app.conf
```

`app.conf` 와 `app.hard` 는 inode 번호가 같고 링크 수가 둘 다 2 입니다. inode 번호는 실행할 때마다 달라지니 두 줄이 같은지만 봅니다.

### 심볼릭 링크가 가리키는 곳

> 기본은 링크 자체의 정보를 보이고, `-L` 을 주면 가리키는 파일의 정보를 보입니다.

```bash
# 링크 자체의 줄은 l 로 시작하고 크기는 대상 이름의 글자 수(app.conf 는 8글자)다
ls -l app.lnk    # lrwxrwxrwx 1 root root 8 Nov  2 10:00 app.lnk -> app.conf

# 가리키는 app.conf 의 종류·크기·시각이 나온다. 이름만 링크의 것이다
#   -L   링크를 따라가 대상의 정보를 보인다
ls -lL app.lnk    # -rw-r--r-- 2 appuser devs 1234 Nov 10 09:30 app.lnk

# 끊어진 링크는 -L 을 주면 대상이 없어 오류가 된다
ls -lL dangling.lnk; echo $?    # ls: cannot access 'dangling.lnk': No such file or directory / 2
```

### 숨김 파일 보기

> 이름이 점으로 시작하는 파일은 `-a` 를 줘야 나오고, `-A` 는 `.` 과 `..` 만 뺍니다.

```bash
# 이 시트의 출력이 터미널에서도 한 줄에 하나씩 나오도록 -1 을 준다
#   -1   한 줄에 이름 하나씩 찍는다
#   -a   점으로 시작하는 이름까지 모두 나열한다
ls -1 -a | head -4
```

```bash
.
..
.hidden-note
app.conf
```

```bash
# .(현재 디렉터리)과 ..(부모 디렉터리)만 뺀다
#   -A   . 과 .. 을 뺀 숨김 파일까지 나열한다
ls -1 -A | head -3
```

```bash
.hidden-note
app.conf
app.hard
```

`head -4`·`head -3` 은 점으로 시작하는 이름이 `C.UTF-8` 정렬에서 맨 앞에 오기 때문에 쓴 것입니다.

### 이름 뒤 종류 기호

> `-F` 는 이름 끝에 종류 기호를 붙여 `-l` 없이도 종류를 알 수 있게 합니다.

```bash
# 실행 파일은 *, 링크는 @, 소켓은 =, FIFO 는 |, 디렉터리는 / 가 붙는다
#   -F   이름 뒤에 종류 기호를 붙인다
ls -1 -F
```

```bash
app.conf
app.hard
app.lnk@
app.sock=
dangling.lnk@
data.bin
deploy.sh*
jobs.pipe|
logs/
old.log
pub/
report.txt
shared/
tools/
tree/
```

```bash
# -p 는 디렉터리에만 / 를 붙인다. 붙은 줄의 수를 센다
#   -p   디렉터리 이름 뒤에 / 만 붙인다
ls -1 -p | grep -c /    # 5
```

### 사람이 읽는 크기

> `-h` 는 크기를 1024 배수의 K·M 로, `--si` 는 1000 배수로 줄여 찍습니다.

```bash
# app.conf 는 1234 바이트, data.bin 은 3145728 바이트다. 1.2K 가 아니라 1.3K 로 올려 찍는다
#   -h   크기에 K·M·G 같은 글자를 붙인다(1024 배수)
ls -lh app.conf data.bin
```

```bash
-rw-r--r-- 2 appuser devs 1.3K Nov 10 09:30 app.conf
-rw-rw-r-- 1 appuser devs 3.0M Oct 20 14:00 data.bin
```

```bash
# 같은 data.bin 을 1000 배수로 찍으면 3.2M 이 된다
#   --si   -h 와 같지만 1000 배수를 쓴다
ls -l --si data.bin    # -rw-rw-r-- 1 appuser devs 3.2M Oct 20 14:00 data.bin
```

### 정렬

> 기본은 이름순이고 `-t` 는 수정 시각 최신순, `-S` 는 크기 큰 순이며 `-r` 은 순서를 뒤집습니다.

```bash
# 가장 최근에 바뀐 파일이 맨 위
#   -t   수정 시각이 최신인 것부터 놓는다
ls -lt report.txt deploy.sh app.conf old.log data.bin
```

```bash
-rw-r----- 1 appuser root     512 Nov 14 08:00 report.txt
-rwxr-xr-x 1 appuser devs    2048 Nov 12 18:05 deploy.sh
-rw-r--r-- 2 appuser devs    1234 Nov 10 09:30 app.conf
-rw-rw-r-- 1 appuser devs 3145728 Oct 20 14:00 data.bin
-rw-r--r-- 1 appuser devs     800 Jan 24  2021 old.log
```

```bash
# 가장 큰 파일이 맨 위
#   -S   크기가 큰 것부터 놓는다
ls -lS report.txt deploy.sh app.conf old.log data.bin
```

```bash
-rw-rw-r-- 1 appuser devs 3145728 Oct 20 14:00 data.bin
-rwxr-xr-x 1 appuser devs    2048 Nov 12 18:05 deploy.sh
-rw-r--r-- 2 appuser devs    1234 Nov 10 09:30 app.conf
-rw-r--r-- 1 appuser devs     800 Jan 24  2021 old.log
-rw-r----- 1 appuser root     512 Nov 14 08:00 report.txt
```

```bash
# 최신 파일이 맨 아래로 가서 긴 목록 끝에서 바로 보인다
#   -r   정렬 순서를 뒤집는다
ls -ltr report.txt deploy.sh app.conf old.log data.bin
```

```bash
-rw-r--r-- 1 appuser devs     800 Jan 24  2021 old.log
-rw-rw-r-- 1 appuser devs 3145728 Oct 20 14:00 data.bin
-rw-r--r-- 2 appuser devs    1234 Nov 10 09:30 app.conf
-rwxr-xr-x 1 appuser devs    2048 Nov 12 18:05 deploy.sh
-rw-r----- 1 appuser root     512 Nov 14 08:00 report.txt
```

```bash
# 가장 최근 파일 하나와 가장 큰 파일 하나의 이름
ls -t | head -1    # report.txt
ls -S | head -1    # data.bin

# 디렉터리를 앞으로 모은다. 그 안에서는 이름순이다
#   --group-directories-first   디렉터리를 파일보다 앞에 놓는다
ls -1 --group-directories-first | head -6
```

```bash
logs
pub
shared
tools
tree
app.conf
```

`head` 의 앞 줄만 자르는 쓰임은 [head·tail 참조 시트](../text/head%C2%B7tail.md)에 있습니다.

### 시각 형식

> `--time-style` 은 시각 칸의 형식을 고르고, 6개월보다 오래된 파일은 기본 형식에서 시각 대신 연도가 나옵니다.

```bash
# 기본 형식은 6개월 안이면 "월 일 시:분", 더 오래되면 "월 일  연도" 다
# old.log(2021년)만 연도로 찍히는 것이 위 「파일 종류 글자」 의 출력이다

# 초와 시간대까지 모두 찍는다
#   --time-style=full-iso   나노초와 UTC 오프셋까지 찍는다
ls -l --time-style=full-iso app.conf old.log
# -rw-r--r-- 2 appuser devs 1234 2026-11-10 09:30:00.000000000 +0000 app.conf
# -rw-r--r-- 1 appuser devs  800 2021-01-24 12:00:00.000000000 +0000 old.log

# 분까지만 찍는다. 최근이든 오래됐든 같은 형식이다
#   --time-style=long-iso   YYYY-MM-DD HH:MM 으로 찍는다
ls -l --time-style=long-iso app.conf old.log
# -rw-r--r-- 2 appuser devs 1234 2026-11-10 09:30 app.conf
# -rw-r--r-- 1 appuser devs  800 2021-01-24 12:00 old.log

# 최근 파일은 월-일 시:분, 오래된 파일은 연-월-일로 찍는다
#   --time-style=iso   최근과 오래됨을 나눠 ISO 꼴로 찍는다
ls -l --time-style=iso app.conf old.log
# -rw-r--r-- 2 appuser devs 1234 11-10 09:30 app.conf
# -rw-r--r-- 1 appuser devs  800 2021-01-24  old.log

# date 의 형식 지정자로 직접 정한다
#   --time-style=+형식   date 와 같은 형식 문자열로 찍는다
ls -l --time-style=+%Y-%m-%dT%H:%M app.conf old.log
# -rw-r--r-- 2 appuser devs 1234 2026-11-10T09:30 app.conf
# -rw-r--r-- 1 appuser devs  800 2021-01-24T12:00 old.log

# -l 과 full-iso 를 한 번에 준다
#   --full-time   -l --time-style=full-iso 와 같다
ls --full-time app.conf
# -rw-r--r-- 2 appuser devs 1234 2026-11-10 09:30:00.000000000 +0000 app.conf
```

기본 형식의 경계는 "6개월보다 오래됨" 이라 읽는 날짜가 지나면 같은 파일이 시각 대신 연도로 바뀝니다.[^ls-info]

### 숫자 ID 로 보기

> `-n` 은 소유자와 그룹을 이름 대신 숫자 ID 로 찍고, 이름을 알 수 없을 때도 숫자가 나옵니다.

```bash
# appuser 는 UID 2001, devs 는 GID 2001 이고 root 는 0 이다. 숫자는 오른쪽 맞춤이다
#   -n   소유자와 그룹을 숫자 ID 로 찍는다
ls -ln app.conf report.txt
```

```bash
-rw-r--r-- 2 2001 2001 1234 Nov 10 09:30 app.conf
-rw-r----- 1 2001    0  512 Nov 14 08:00 report.txt
```

```bash
# 이름이 없는 UID·GID 의 파일은 -n 없이도 숫자로 나온다
chown 3999:3999 report.txt
ls -l report.txt    # -rw-r----- 1 3999 3999 512 Nov 14 08:00 report.txt

# 되돌린다
chown appuser:root report.txt
```

### 하위 디렉터리까지 나열

> `-R` 은 하위 디렉터리를 `경로:` 머리말과 함께 아래로 내려가며 나열합니다.

`-R` 은 「종료 코드」 에서 풀었습니다.

```bash
# root 는 locked 도 열 수 있어 마지막에 빈 디렉터리로 나온다
ls -1 -R tree
```

```bash
tree:
a
b
locked

tree/a:
x.txt

tree/b:
c
y.txt

tree/b/c:
z.txt

tree/locked:
```

### 로그 디렉터리 읽기

> `/var/log` 의 파일은 소유 그룹과 권한으로 누가 읽는지가 갈리고, `journal/` 의 `s` 와 `+` 도 이 장면에서 읽습니다.

```bash
# 로그 디렉터리 자신과 자주 보는 파일 셋. 인자도 이름순으로 정렬되어 나온다
# -d 와 함께 준 -F 는 /var/log 자신에도 / 를 붙인다
# 크기와 시각은 이 VM 의 값이라 환경마다 다르다
ls -ldF \
  /var/log /var/log/auth.log /var/log/btmp \
  /var/log/wtmp /var/log/journal
```

```bash
drwxrwxr-x  1 root   syslog            274 Nov 16 00:37 /var/log/
-rw-r-----  1 syslog adm             77738 Nov 16 02:41 /var/log/auth.log
-rw-rw----  1 root   utmp                0 Nov  8 07:44 /var/log/btmp
drwxr-sr-x+ 1 root   systemd-journal    64 Nov 10 07:53 /var/log/journal/
-rw-rw-r--  1 root   utmp              400 Nov 10 07:53 /var/log/wtmp
```

`auth.log` 는 그룹 `adm` 만 읽고 `btmp` 는 그룹 `utmp` 만 읽고 씁니다. `journal/` 의 `s` 는 setgid 라 안에 생기는 파일이 그룹 `systemd-journal` 을 물려받습니다.

```bash
# journal 의 ACL 항목을 읽는다. 위치를 /var/log 로 옮겨 경로 앞 슬래시 경고를 피한다
cd /var/log && getfacl journal; cd /tmp/lab-ls
```

```bash
# file: journal
# owner: root
# group: systemd-journal
# flags: -s-
user::rwx
group::r-x
group:adm:r-x
mask::r-x
other::r-x
default:user::rwx
default:group::r-x
default:group:adm:r-x
default:mask::r-x
default:other::r-x
```

`+` 가 붙은 까닭은 `adm` 그룹에 읽기를 주는 `group:adm:r-x` 항목입니다. `default:` 항목은 그 안에 새로 생기는 파일이 이어받을 ACL 입니다.[^acl-default]

### 실습 정리

```bash
# 「실습 준비」 에서 만든 파일·디렉터리, GNU ls 링크, 사용자와 그룹을 지운다
cd /
rm -rf /tmp/lab-ls /tmp/gnu-bin
userdel appuser
groupdel devs

# 지워졌는지 확인한다
id appuser    # id: 'appuser': no such user
getent group devs    # (출력 없음)
```

acl 패키지는 다른 곳에서도 쓰므로 지우지 않았습니다.



## 주의사항과 동작 원리

### 스크립트에서 ls 출력을 파싱하는 것

> `ls` 출력은 줄바꿈이 든 이름을 한 파일로 세지 못하니, 파일 목록은 `find -printf` 나 `stat` 로 얻습니다.

```bash
# 공백과 줄바꿈이 든 이름 둘을 만든다
mkdir /tmp/lab-ls/odd && cd /tmp/lab-ls/odd
touch 'my report.txt' $'two\nlines.txt'

# 파일은 둘인데 ls 는 줄 셋을 찍는다
ls | wc -l    # 3

# 점 하나를 파일마다 찍고 센다. 이름 안의 줄바꿈과 관계없이 파일 수가 나온다
#   find -mindepth 1   시작 디렉터리 자신은 빼고 센다
#   find -printf .     파일마다 점 하나를 찍는다
find . -mindepth 1 -printf . | wc -c    # 2

# 이 디렉터리를 정리한다
cd /tmp/lab-ls && rm -rf odd
```

같은 `ls` 가 터미널에서는 이름을 따옴표로 감싸 `'my report.txt'  'two'$'\n''lines.txt'` 로 찍고 파이프에서는 따옴표 없이 줄바꿈 그대로 찍습니다. 이름을 안전하게 다루는 `find` 의 쓰임은 [find 참조 시트](../../../book/learning-modern-linux/00-02.find%20참조%20시트.md)에 있습니다.

### 디렉터리 링크 수와 크기의 차이

> 디렉터리 줄의 링크 수와 크기는 파일시스템이 정하는 값이라, 책의 `3 … 4096` 같은 숫자가 그대로 나오지 않습니다.

```bash
# tree 는 하위 디렉터리가 셋(a, b, locked)이라 링크 수가 5(2 + 3)이고 크기는 100 이다
# 실습 폴더가 있는 /tmp 는 tmpfs 다
ls -ld tree    # drwxr-xr-x 5 root root 100 Nov  6 07:00 tree

# 같은 VM 의 /var/log 는 btrfs 라서 하위 디렉터리가 있어도 링크 수가 1 이다
ls -ld /var/log    # drwxrwxr-x 1 root syslog 274 Nov 16 00:37 /var/log

# 파일시스템 종류는 stat 으로 읽는다
#   stat -f      파일 자체가 아니라 그 파일이 든 파일시스템을 본다
#   stat -c %T   파일시스템 종류 이름만 찍는다
stat -f -c '%T %n' /tmp/lab-ls /var/log
```

```bash
tmpfs /tmp/lab-ls
btrfs /var/log
```

링크 수가 `2 + 하위 디렉터리 수` 라는 계산은 이 시트의 tmpfs 에서 맞고 btrfs 에서는 맞지 않았습니다. 이 칸으로 하위 디렉터리 수를 세지 않고 `find -type d` 로 셉니다.

### 같은 시각 파일의 정렬 순서

> 목록에서 수정 시각이 같은 파일의 `-t` 정렬 순서는 GNU 판과 uutils 판이 다르게 정합니다.

```bash
# app.conf 와 app.hard 는 수정 시각이 같다. GNU 판은 시각이 같으면 이름순으로 둔다
/usr/bin/gnuls -1 -t | head -4
```

```bash
report.txt
deploy.sh
app.conf
app.hard
```

```bash
# 이 VM 의 기본 ls(uutils)는 시각이 같으면 디렉터리에서 읽은 순서대로 둔다
/usr/bin/ls -1 -t | head -4
```

```bash
report.txt
deploy.sh
app.hard
app.conf
```

```bash
# 디렉터리에서 읽은 순서로는 app.hard 가 app.conf 보다 앞이다
#   -U   정렬하지 않고 디렉터리에서 읽은 순서대로 찍는다
ls -1 -U | grep '^app\.[ch]'
# app.hard
# app.conf
```

두 구현은 `-ln` 의 숫자 칸 맞춤(GNU 오른쪽, uutils 왼쪽)과 오류 문구(`unrecognized option` 대 `unexpected argument`)도 달랐습니다. 이 시트는 GNU 판 기준이니, Ubuntu 26.04 에서 시트 값과 다르면 먼저 `ls --version` 으로 어느 구현인지 봅니다.



## 관련 문서

> 이 시트의 예와 이어지는 시트와 책 노트입니다.

- [전부 아니면 전무에서 잘게 쪼개는 쪽으로](../../../book/learning-modern-linux/04-01.전부%20아니면%20전무에서%20잘게%20쪼개는%20쪽으로.md) — 권한 아홉 자리와 `s`·`t` 비트, ACL 의 배경 이론
- [재는 것은 바깥이고 알고 싶은 것은 안이다](../../../book/learning-modern-linux/08-01.재는%20것은%20바깥이고%20알고%20싶은%20것은%20안이다.md) — `/var/log` 의 파일 이름과 `ls -al` 출력의 배경 이론
- [find 참조 시트](../../../book/learning-modern-linux/00-02.find%20참조%20시트.md) — `ls` 출력을 파싱하는 대신 파일을 안전하게 찾는 법
- [head·tail 참조 시트](../text/head%C2%B7tail.md) — `ls -t | head -1` 처럼 목록의 앞뒤만 볼 때
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경, 공식 문서, 원서와 각주 정의입니다.

- 검증 환경: Ubuntu 26.04.1 LTS(OrbStack VM) — 2026-11-16 출력
- 실측 구현: GNU coreutils 9.7(`gnu-coreutils` 패키지의 `/usr/bin/gnuls`), 비교한 기본 `ls` 는 uutils coreutils 0.10.0
- [ls(1)](https://man7.org/linux/man-pages/man1/ls.1.html) — 2026-11-16 조회
- [acl(5)](https://man7.org/linux/man-pages/man5/acl.5.html) — 2026-11-16 조회
- [GNU coreutils 매뉴얼](https://www.gnu.org/software/coreutils/manual/coreutils.html) — "ls invocation"
- 원서: 《Learning Modern Linux》 4장 Access Control·8장 Logs and Monitoring (Michael Hausenblas, O'Reilly, 2022년) — `ls -al` 으로 파일 모드를 읽는 예와 `/var/log` 목록

[^uutils]: uutils 프로젝트 — "uutils coreutils is a cross-platform reimplementation of the GNU coreutils in Rust." 이 VM 의 `/usr/bin/ls` 는 `../lib/cargo/bin/coreutils/ls` 로 가는 링크이고, `dpkg -S` 는 링크를 `coreutils-from-uutils` 패키지로, 링크 대상을 `rust-coreutils` 패키지로 보였습니다. `ls --version` 은 `ls (uutils coreutils) 0.10.0` 을 보였습니다. 이 시트의 실측입니다. <https://github.com/uutils/coreutils>
[^bsd-ls]: macOS 26.6.2 의 `man ls` — "-T When printing in the long (-l) format, display complete time information for the file, including month, day, hour, minute, second, and year." `ls -l --time-style=iso /usr` 는 `ls: unrecognized option` 으로 실패했습니다. 이 시트의 실측입니다.
[^ls-info]: GNU coreutils 9.7 의 `info coreutils` "ls invocation" — "The file type is one of the following characters", "‘s’ If the set-user-ID or set-group-ID bit and the corresponding executable bit are both set.", "‘S’ If the set-user-ID or set-group-ID bit is set but the corresponding executable bit is not set.", "‘T’ If the restricted deletion flag or sticky bit is set but the other-executable bit is not set.", "A file with any other combination of alternate access methods is marked with a ‘+’ character.", "The BLOCKS computed counts each hard link separately; this is arguably a deficiency.", "A timestamp is considered to be “recent” if it is less than six months old, and is not dated in the future." 이 기기에서 gnu.org 가 시간 초과로 열리지 않아 설치된 info 원문으로 대조했습니다. <https://www.gnu.org/software/coreutils/manual/html_node/What-information-is-listed.html>
[^ls-help]: `ls --help` (GNU coreutils 9.7) — "-d, --directory list directories themselves, not their contents", "-h, --human-readable with -l and -s, print sizes like 1K 234M 2G etc.", "--si likewise, but use powers of 1000 not 1024", "-p, --indicator-style=slash append / indicator to directories", "-r, --reverse reverse order while sorting", "-R, --recursive list subdirectories recursively", "-t sort by time, newest first; see --time", "-S sort by file size, largest first".
[^ls-exit]: ls(1) — "Exit status: 0 if OK, 1 if minor problems (e.g., cannot access subdirectory), 2 if serious trouble (e.g., cannot access command-line argument)." <https://man7.org/linux/man-pages/man1/ls.1.html>
[^acl-mask]: acl(5) — "If the ACL has an ACL_MASK entry, the group permissions correspond to the permissions of the ACL_MASK entry." <https://man7.org/linux/man-pages/man5/acl.5.html>
[^acl-default]: acl(5) — "a directory may have an associated ACL that governs the initial access ACL for objects created within that directory; this ACL is referred to as a default ACL." <https://man7.org/linux/man-pages/man5/acl.5.html>
