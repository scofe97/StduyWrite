---
title: rsync 참조 시트
tags: [linux, cheatsheet, file, rsync, backup, ssh, cli, reference]
status: draft
source:
  - rsync(1) 3.5.0 (Debian 12 컨테이너의 `man rsync` 원문, https://download.samba.org/pub/rsync/rsync.1)
  - rsync 3.5.0 `--help` 원문 (Debian 12, rsync 3.5.0+ds1-0+deb12u1)
  - xattr(7) (Linux man-pages 6.03, Debian 12)
related:
  - ./ls.md
  - ../ssh/scp·sftp.md
  - ../README.md
  - ../../../book/learning-modern-linux/07-03.주고받는 일은 결국 몇 개의 명령으로 줄어든다.md
updated: 2026-11-17
---

# rsync 참조 시트

---

> 원본과 대상을 견주어 달라진 파일만 옮기는 `rsync` 를 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `rsync` 는 원본과 대상을 견주어 달라진 파일만 보내, 두 디렉터리를 같게 맞추는 복사 도구입니다.

`rsync` 는 Debian 패키지 `rsync` 3.5.0+ds1-0+deb12u1 의 외부 바이너리입니다(`dpkg -S` 로 확인). protocol 은 32 입니다. 출력은 Debian 12 컨테이너 `lab`(OpenSSH 9.2p1)에서 받았습니다. 원격 예의 `node1` 은 `lab` 자신이고 `srv` 는 `rsync` 가 없는 두 번째 컨테이너입니다.

macOS 에서 `rsync --version` 은 openrsync(protocol 29)를 가리키는 다른 구현입니다. 그래서 이 시트의 출력은 Linux 에서 받았습니다.[^macos]

`rsync` 가 보낼 파일을 고르는 기본 기준은 크기와 수정 시각입니다.[^quick]



## 핵심 문법

> 원본(SRC) 끝의 `/` 로 디렉터리째 옮길지 내용만 옮길지 정하고, 옵션으로 무엇을 맞출지 고릅니다.

```bash
# 호출 형태. --help 의 Usage 줄 그대로다
# 이 시트는 SSH 를 거치는 [USER@]HOST:DEST 꼴까지 다루고, ::·rsync:// 꼴(데몬 접속)은 다루지 않는다
rsync [OPTION]... SRC [SRC]... DEST
  or   rsync [OPTION]... SRC [SRC]... [USER@]HOST:DEST
  or   rsync [OPTION]... SRC [SRC]... [USER@]HOST::DEST
  or   rsync [OPTION]... SRC [SRC]... rsync://[USER@]HOST[:PORT]/DEST
  or   rsync [OPTION]... [USER@]HOST:SRC [DEST]
  or   rsync [OPTION]... [USER@]HOST::SRC [DEST]
  or   rsync [OPTION]... rsync://[USER@]HOST[:PORT]/SRC [DEST]

# 원본 디렉터리의 내용만 대상 안에 옮긴다 (원본 끝 슬래시로 복사 위치 정하기)
rsync -a src/ dst/

# 옮기지 않고 항목별 변화만 본다 (첫 전송과 -i 출력 읽기)
rsync -ain src/ dst/

# 크기·시각이 같아도 내용이 다른 파일을 찾는다 (바뀐 파일만 보내는 기준과 -c)
rsync -aic src/ dst/

# 대상에만 있는 파일을 지우기 전에 목록을 본다 (--delete 를 -n 으로 먼저 보기)
rsync -ain --delete src/ dst/

# 하드 링크·ACL·확장 속성까지 옮긴다 (-a 에 들지 않는 -H·-A·-X)
rsync -aH src/ dst/
rsync -aAX src/ dst/

# SSH 로 원격에 보내고 원격에서 받는다 (원격으로 보내고 받기)
rsync -a -e "ssh -p 2222" src/ user@host:dst/
rsync -a user@host:src/ dst/

# 회선이 느릴 때 압축하고 속도를 제한한다 (압축과 속도 제한)
rsync -az --bwlimit=RATE src/ user@host:dst/

# 끊겨도 이어 받도록 부분 파일을 남기고 진행률을 본다 (끊긴 전송 이어 보내기)
rsync -aP src/ user@host:dst/
```

### -i 출력 읽는 법

```bash
# -i 가 한 항목마다 찍는 11글자는 YXcstpoguax 꼴이다. 가운데 열은 이 시트에서 실제로 받은 값이다
# 첫 글자 Y 는 갱신 종류, 둘째 글자 X 는 파일 종류, 나머지는 바뀐 속성이다
#   >f+++++++++   받은 새 파일이다
#   <f+++++++++   보낸 새 파일이다
#   cd+++++++++   대상에 새로 만든 디렉터리다
#   cL+++++++++   대상에 새로 만든 심볼릭 링크다
#   >f..t......   내용 전송이 있었고 수정 시각 t 만 달랐다
#   >fc........   체크섬 c 가 달라 다시 받았다
#   *deleting     대상에서 지우는 항목이다 (뒤에 이름이 붙는다)
#   .f            갱신하지 않는 파일이다 (-ii 일 때만 나온다)
# Y: <(보냄) >(받음) c(로컬 생성·변경) h(하드 링크) .(갱신 없음) *(뒤가 메시지)
# X: f(파일) d(디렉터리) L(심볼릭 링크) D(장치) S(소켓·FIFO)
# 속성: c(체크섬) s(크기) t(수정 시각) p(권한) o(소유자) g(그룹) u·n·b(atime·crtime) a(ACL) x(확장 속성)
# 속성 자리: .(그대로) +(새로 만듦) 공백(전부 그대로)
```

위 목록은 `man rsync` 의 `--itemize-changes` 항목을 옮긴 것입니다.[^itemize]



## 종료 코드

> 0 은 성공이고, 23·24 는 일부만 옮기고 끝났다는 뜻이라 스크립트가 따로 읽어야 합니다.[^exit]

아래 예는 「실습 준비」 를 돌린 상태에서 이어집니다.

```bash
# 0   성공
# 1   문법·사용법 오류
# 2   프로토콜 비호환
# 3   입출력할 파일·디렉터리를 고르는 단계의 오류
# 5   클라이언트-서버 프로토콜 시작 오류
# 10  소켓 입출력 오류
# 11  파일 입출력 오류
# 12  rsync 프로토콜 데이터 스트림 오류 (「원격에 rsync 가 없을 때」 에서 재현한다)
# 20  SIGINT·SIGTERM·SIGHUP 을 받았다
# 23  오류로 일부만 전송했다
# 24  원본 파일이 전송 전에 사라져 일부만 전송했다
# 25  --max-delete 한도가 삭제를 멈췄다
# 30  데이터를 주고받는 중 시간 초과

# 성공하면 0 이다
rm -rf e1; mkdir e1
rsync -a src/ e1/; echo $?    # 0

# 모르는 옵션은 1 이다
rsync --nope src/ e1/ >/dev/null 2>&1; echo $?    # 1

# 없는 원본 디렉터리는 man 의 3 이 아니라 23 이 나왔다
rsync -a nosuch/ e1/; echo $?    # rsync: [sender] change_dir "/root/rsync-lab/nosuch" failed: No such file or directory (2) / rsync error: some files/attrs were not transferred (see previous errors) (code 23) at main.c(1394) [sender=3.5.0] / 23
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다.

```bash
# 읽을 수 없는 파일이 끼면 나머지는 옮기고 23 으로 끝난다
# root 소유의 600 파일 secret.txt 를 일반 계정 dev 로 복사한다
D=/home/dev/lab; rm -rf $D; mkdir -p $D/u1 $D/u2
echo a > $D/u1/ok.txt; echo b > $D/u1/secret.txt
chown -R dev:dev $D; chown root:root $D/u1/secret.txt; chmod 600 $D/u1/secret.txt
su dev -c "rsync -a $D/u1/ $D/u2/"; echo "rc=$?"
ls $D/u2
```

```bash
rsync: [sender] send_files failed to open "/home/dev/lab/u1/secret.txt": Permission denied (13)
rsync error: some files/attrs were not transferred (see previous errors) (code 23) at main.c(1394) [sender=3.5.0]
rc=23
ok.txt
```

```bash
# 원본이 전송 중에 사라지면 24 다. --bwlimit 으로 느리게 보내는 동안 c.dat 를 지운다
#   --bwlimit   초당 전송량 상한이다. 단위를 안 붙이면 KiB 다
rm -rf v1 v2; mkdir v1 v2
for n in a b c; do head -c 100000 /dev/zero | tr '\0' x > v1/$n.dat; done
rsync -a --bwlimit=50 v1/ v2/ & P=$!
sleep 1; rm v1/c.dat
wait $P; echo "rc=$?"
ls v2
```

```bash
file has vanished: "/root/rsync-lab/v1/c.dat"
rsync warning: some files vanished before they could be transferred (code 24) at main.c(1394) [sender=3.5.0]
rc=24
a.dat
b.dat
```



## 유스케이스

> 예는 앞 예가 만든 상태를 이어 쓰므로 위에서 아래로 차례로 돌립니다.

### 실습 준비

> 아래 블록을 한 번 붙여 넣으면 이 시트의 예가 쓰는 컨테이너와 파일이 모두 생깁니다. 호스트에는 Docker 가 있어야 합니다.

컨테이너 둘을 만들어 두 곳에 `sshd` 와 `dev` 계정을 둡니다. `rsync` 는 `lab` 에만 설치합니다.

```bash
# 호스트에서 실행용 lab 과 rsync 가 없는 원격 srv 를 띄운다
docker run -d --name lab debian:12 sleep infinity
docker run -d --name srv debian:12 sleep infinity

# 두 컨테이너에 sshd 와 일반 계정 dev 를 만든다
for c in lab srv; do
  docker exec $c bash -c 'umask 022; apt-get update -qq; apt-get install -y -qq openssh-server; mkdir -p /run/sshd; ssh-keygen -A; useradd -m dev; mkdir -p -m 700 /home/dev/.ssh; chown dev:dev /home/dev/.ssh'
done
docker exec lab apt-get install -y -qq rsync acl attr
```

```bash
# lab 의 root 키를 두 컨테이너의 dev 에 등록하고, 호스트 키 확인 질문을 끈다
docker exec lab bash -c 'umask 077; ssh-keygen -q -t ed25519 -N "" -f /root/.ssh/id_ed25519; printf "Host *\n  StrictHostKeyChecking no\n  UserKnownHostsFile /dev/null\n  LogLevel ERROR\n" > /root/.ssh/config'
for c in lab srv; do
  docker exec lab cat /root/.ssh/id_ed25519.pub | docker exec -i $c bash -c 'umask 077; cat > /home/dev/.ssh/authorized_keys; chown dev:dev /home/dev/.ssh/authorized_keys'
done

# lab 에서 node1 은 자기 자신, srv 는 두 번째 컨테이너를 가리키게 하고 sshd 를 켠다
SRV_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' srv)
docker exec lab bash -c "echo '127.0.0.1 node1' >> /etc/hosts; echo '$SRV_IP srv' >> /etc/hosts; /usr/sbin/sshd; /usr/sbin/sshd -p 2222"
docker exec srv /usr/sbin/sshd
docker exec lab bash -c 'mkdir -p -m 777 /srv/lab'
```

이제 `docker exec -it lab bash` 로 들어가 아래 블록으로 원본 트리를 만듭니다. 이후 예는 모두 이 셸의 `~/rsync-lab` 에서 돌립니다.

```bash
# src 는 「원본 끝 슬래시로 복사 위치 정하기」·「첫 전송과 -i 출력 읽기」부터 여러 곳에서 쓴다
# hard.txt 는 notes.txt 와 같은 파일의 하드 링크이고 link.txt 는 심볼릭 링크다
umask 022
cd ~
rm -rf rsync-lab && mkdir -p rsync-lab/src/conf rsync-lab/src/data && cd rsync-lab
echo 'port: 8080' > src/conf/app.yml
echo 'level: info' > src/conf/log.yml
seq 1 20000 > src/data/big.txt
echo v1 > src/notes.txt
ln src/notes.txt src/hard.txt
ln -s notes.txt src/link.txt
find src | sort
```

```bash
src
src/conf
src/conf/app.yml
src/conf/log.yml
src/data
src/data/big.txt
src/hard.txt
src/link.txt
src/notes.txt
```

### 원본 끝 슬래시로 복사 위치 정하기

> 원본 끝에 `/` 가 없으면 디렉터리 이름째 대상 안에 만들고, 있으면 내용만 대상에 넣습니다.

man 은 원본 끝의 `/` 를 "디렉터리 내용을 복사한다"로 읽으라고 설명합니다.[^slash] 아래는 같은 `src` 를 두 꼴로 보낸 결과입니다.

```bash
# -a(archive)는 -rlptgoD 를 묶은 옵션이라 하위 디렉터리까지 재귀하고
# 심볼릭 링크·권한·수정 시각·그룹·소유자·장치 파일을 지킨다
# 원본 끝에 / 가 없으면 src 라는 이름째 들어간다
rm -rf d1 d2; mkdir d1 d2
rsync -a src d1/; find d1 | sort
```

```bash
d1
d1/src
d1/src/conf
d1/src/conf/app.yml
d1/src/conf/log.yml
d1/src/data
d1/src/data/big.txt
d1/src/hard.txt
d1/src/link.txt
d1/src/notes.txt
```

```bash
# 원본 끝에 / 가 있으면 내용만 들어간다
rsync -a src/ d2/; find d2 | sort
```

```bash
d2
d2/conf
d2/conf/app.yml
d2/conf/log.yml
d2/data
d2/data/big.txt
d2/hard.txt
d2/link.txt
d2/notes.txt
```

대상 끝의 `/` 는 이 결과를 바꾸지 않습니다. 대상 `x2` 가 아직 없어도 `x1/` 로 보낸 결과와 같습니다.

```bash
# 두 결과의 파일 목록을 맞대어 본다. diff 가 비면 같다
rm -rf x1 x2; mkdir x1
rsync -a src x1/
rsync -a src x2
diff <(cd x1; find . | sort) <(cd x2; find . | sort) && echo same    # same
```

원본이 파일 하나이고 대상이 없을 때만 대상 끝 `/` 가 결과를 가릅니다. `/` 가 없으면 그 이름의 파일을 만듭니다. `/` 가 있으면 디렉터리를 만들어 그 안에 넣습니다.

```bash
rm -rf s1 s2
rsync -a src/notes.txt s1
rsync -a src/notes.txt s2/
ls -ld s1 s2
```

```bash
-rw-r--r-- 1 root root  3 Nov 17 06:35 s1
drwxr-xr-x 1 root root 18 Nov 17 06:38 s2
```

### 첫 전송과 -i 출력 읽기

> `-i` 는 항목마다 무엇이 바뀌는지 11글자로 보이고, 이미 같은 항목은 아무것도 찍지 않습니다.

```bash
# 대상이 없는 첫 전송이다. 앞의 -a 에 -i(--itemize-changes)를 더한다
rm -rf dst
rsync -ai src/ dst/
```

```bash
created directory dst
cd+++++++++ ./
>f+++++++++ hard.txt
cL+++++++++ link.txt -> notes.txt
>f+++++++++ notes.txt
cd+++++++++ conf/
>f+++++++++ conf/app.yml
>f+++++++++ conf/log.yml
cd+++++++++ data/
>f+++++++++ data/big.txt
```

```bash
# 같은 명령을 다시 돌리면 바뀐 것이 없어 아무것도 안 찍고 0 으로 끝난다
rsync -ai src/ dst/; echo "rc=$?"    # rc=0

# -i 를 두 번 주면 갱신하지 않은 항목도 .f 처럼 보인다
rsync -aii src/ dst/
```

```bash
.d          ./
.f          hard.txt
.L          link.txt -> notes.txt
.f          notes.txt
.d          conf/
.f          conf/app.yml
.f          conf/log.yml
.d          data/
.f          data/big.txt
```

첫 전송에서 `hard.txt` 와 `notes.txt` 를 각각 `>f+++++++++` 로 받았습니다. 하드 링크가 어떻게 옮겨지는지는 「-a 에 들지 않는 -H·-A·-X」 에서 봅니다.

### 바뀐 파일만 보내는 기준과 -c

> 기본 기준은 크기와 수정 시각이라, 둘이 같으면 내용이 달라도 건너뛰고 `-c` 를 주면 체크섬으로 가립니다.

`-c` 는 크기가 같은 파일마다 양쪽이 체크섬을 계산하려고 파일을 끝까지 읽으므로 디스크 입출력이 크게 늘어납니다.[^checksum]

```bash
# 내용은 달라지고 크기는 그대로인 경우다. 수정 시각이 바뀌어 t 만 찍힌다
echo 'port: 9090' > src/conf/app.yml
rsync -ai src/ dst/    # >f..t...... conf/app.yml

# 내용만 바뀌고 크기와 수정 시각이 같은 경우는 기본 기준으로 건너뛴다
# touch -r 은 dst 쪽 파일의 수정 시각을 그대로 복사한다
echo 'port: 7070' > src/conf/app.yml; touch -r dst/conf/app.yml src/conf/app.yml
rsync -ai src/ dst/

# -c 를 주면 체크섬이 달라 c 가 찍히고 다시 받는다
rsync -aic src/ dst/    # >fc........ conf/app.yml
cat dst/conf/app.yml    # port: 7070
```

바로 위 블록의 두 번째 `rsync` 는 아무것도 찍지 않았습니다.

### --delete 를 -n 으로 먼저 보기

> `--delete` 는 대상에만 있는 파일을 지우므로, 먼저 `-n` 으로 지울 목록을 보고 같은 명령에서 `-n` 만 뺍니다.

`-n`(`--dry-run`)은 아무것도 바꾸지 않고 실제 실행과 같은 `-i` 출력을 보여 줍니다.[^delete]

```bash
# 대상에 원본에 없는 old.log 를 두고 -n 으로 먼저 본다
#   --delete   원본에 없는 대상 파일을 지운다
#   -n         시험 실행이라 아무것도 바꾸지 않는다
echo junk > dst/old.log
rsync -ain --delete src/ dst/
ls dst
```

```bash
*deleting   old.log
.d..t...... ./
conf
data
hard.txt
link.txt
notes.txt
old.log
```

```bash
# -n 만 빼고 같은 명령을 돌린다
rsync -ai --delete src/ dst/
ls dst
```

```bash
*deleting   old.log
.d..t...... ./
conf
data
hard.txt
link.txt
notes.txt
```

### -a 에 들지 않는 -H·-A·-X

> `-a` 는 하드 링크·ACL·확장 속성을 옮기지 않아서 `-H`·`-A`·`-X` 를 따로 줘야 합니다.

man 은 `-a` 를 `-rlptgoD` 와 같다고 하면서 `-A`·`-X`·`-U`·`-N`·`-H` 는 빠진다고 적습니다.[^archive] 먼저 하드 링크입니다.[^hardlink]

```bash
# 원본의 notes.txt·hard.txt 는 inode 가 같다. -a 는 둘을 따로 복사한다
rm -rf h1 h2
ls -li src/notes.txt src/hard.txt
rsync -a src/ h1/; ls -li h1/notes.txt h1/hard.txt
```

```bash
5427048 -rw-r--r-- 2 root root 3 Nov 17 06:35 src/hard.txt
5427048 -rw-r--r-- 2 root root 3 Nov 17 06:35 src/notes.txt
5428474 -rw-r--r-- 1 root root 3 Nov 17 06:35 h1/hard.txt
5428475 -rw-r--r-- 1 root root 3 Nov 17 06:35 h1/notes.txt
```

```bash
# -H 를 더하면 대상에서도 같은 inode 를 가리키는 하드 링크가 된다
rsync -aH src/ h2/; ls -li h2/notes.txt h2/hard.txt
```

```bash
5428483 -rw-r--r-- 2 root root 3 Nov 17 06:35 h2/hard.txt
5428483 -rw-r--r-- 2 root root 3 Nov 17 06:35 h2/notes.txt
```

ACL 은 `-A`, 확장 속성은 `-X` 가 옮깁니다. root 가 `-X` 로 복사하면 `system.*` 을 뺀 모든 이름공간을 옮깁니다. 일반 사용자는 `user.*` 만 옮깁니다.[^xattr] SELinux 라벨은 `security.*` 이름공간에 저장되므로 root 의 `-X` 범위에 듭니다.[^secns]

```bash
# 원본 파일에 ACL(nobody 읽기)과 확장 속성 user.tag 를 단다
setfacl -m u:nobody:r src/conf/app.yml
setfattr -n user.tag -v prod src/conf/app.yml
getfacl -c src/conf/app.yml; getfattr -d src/conf/app.yml
```

```bash
user::rw-
user:nobody:r--
group::r--
mask::r--
other::r--

# file: src/conf/app.yml
user.tag="prod"

```

```bash
# -a 만 주면 둘 다 사라진다. getfattr 는 속성이 없으면 아무것도 찍지 않는다
rm -rf a1 a2 a3
rsync -a src/ a1/
getfacl -c a1/conf/app.yml; getfattr -d a1/conf/app.yml
```

```bash
user::rw-
group::r--
other::r--

```

```bash
# -A 는 ACL 만, -AX 는 ACL 과 확장 속성을 함께 옮긴다
rsync -aA src/ a2/; getfacl -c a2/conf/app.yml; getfattr -d a2/conf/app.yml
rsync -aAX src/ a3/; getfacl -c a3/conf/app.yml; getfattr -d a3/conf/app.yml
```

```bash
user::rw-
user:nobody:r--
group::r--
mask::r--
other::r--

user::rw-
user:nobody:r--
group::r--
mask::r--
other::r--

# file: a3/conf/app.yml
user.tag="prod"

```

`-A` 만 준 `a2` 는 ACL 만 있고 `user.tag` 가 없습니다. `-AX` 를 준 `a3` 는 둘 다 있습니다.

### 원격으로 보내고 받기

> `-e` 로 원격 셸을 정하고 `호스트:경로` 꼴로 쓰면 SSH 를 거쳐 보내고 받습니다.

`rsync` 는 기본으로 `ssh` 를 원격 셸로 씁니다.[^rsh] 아래 `-e "ssh -p 2222"` 는 `ssh` 에 포트를 넘기는 꼴입니다. `lab` 의 `sshd` 는 22 와 2222 에 띄워 두었습니다.

```bash
# 원격(node1)의 dev 홈 아래 remote-dst 로 보낸다. 보냈으니 Y 가 < 다
#   -e   원격 셸 명령을 정한다. 여기서는 포트 2222 의 ssh 다
rsync -ai -e "ssh -p 2222" src/ dev@node1:remote-dst/
```

```bash
created directory remote-dst
cd+++++++++ ./
<f+++++++++ hard.txt
cL+++++++++ link.txt -> notes.txt
<f+++++++++ notes.txt
cd+++++++++ conf/
<f+++++++++ conf/app.yml
<f+++++++++ conf/log.yml
cd+++++++++ data/
<f+++++++++ data/big.txt
```

```bash
# 같은 명령을 다시 돌리면 바뀐 것이 없어 아무것도 안 찍는다
rsync -ai -e "ssh -p 2222" src/ dev@node1:remote-dst/; echo "rc=$?"    # rc=0

# 호스트를 원본 쪽에 쓰면 원격에서 받아 온다
rsync -ai -e "ssh -p 2222" dev@node1:remote-dst/conf/ pulled/
```

```bash
created directory pulled
cd+++++++++ ./
>f+++++++++ app.yml
>f+++++++++ log.yml
```

### 압축과 속도 제한

> `-z` 는 전송 중에 데이터를 압축해 보내는 양을 줄이고, `--bwlimit` 는 초당 전송량에 상한을 둡니다.

`-z` 는 느린 회선에서 보내는 양을 줄입니다.[^compress] 같은 1.3MB 텍스트 파일을 `--stats` 로 보내면 보낸 바이트가 달라집니다.

```bash
# --stats 는 전송 뒤에 합계를 찍는다. grep 으로 두 줄만 남긴다
seq 1 200000 > /srv/lab/big2.txt
rsync -a --stats -e "ssh -p 2222" /srv/lab/big2.txt dev@node1:z1/ | grep -E 'Total file size|Total bytes sent'
rsync -az --stats -e "ssh -p 2222" /srv/lab/big2.txt dev@node1:z2/ | grep -E 'Total file size|Total bytes sent'
```

```bash
Total file size: 1,288,895 bytes
Total bytes sent: 1,289,307
Total file size: 1,288,895 bytes
Total bytes sent: 107,427
```

`--bwlimit` 의 값은 단위를 안 붙이면 1024 바이트 단위입니다.[^bwlimit] `-P` 는 `--partial --progress` 와 같습니다. 진행률 줄은 `\r` 로 덮어쓰므로 `tr` 로 줄을 나눠 봅니다.

```bash
# 1000 KiB/s 로 제한해 1.3MB 를 보내면 1초 남짓 걸린다
#   -P   --partial 과 --progress 를 함께 준다
mkdir -p /srv/lab/p1
time (rsync -aP --bwlimit=1000 /srv/lab/big2.txt /srv/lab/p1/ | tr '\r' '\n')
```

```bash
sending incremental file list
big2.txt

         32,768   2%    0.00kB/s    0:00:00  
      1,081,344  83%  996.11kB/s    0:00:00  
      1,288,895 100%    1.04MB/s    0:00:01 (xfr#1, to-chk=0/1)

real	0m1.314s
user	0m0.005s
sys	0m0.004s
```

### 끊긴 전송 이어 보내기

> `--partial` 을 주면 중단된 부분 파일이 남고, 다음 실행은 그 뒤쪽만 보냅니다.

기본은 중단되면 부분 파일을 지웁니다.[^partial] 2초 뒤 `SIGINT` 로 끊어 두 경우를 비교합니다.

```bash
# --partial 없이 끊으면 대상 디렉터리가 비어 있다
# 끊을 때 나오는 오류 메시지는 실행마다 달라서 버린다
#   timeout -s INT 2   2초 뒤 SIGINT 를 보내 끊는다
mkdir -p /srv/lab/p6
timeout -s INT 2 rsync -a --bwlimit=200 /srv/lab/big2.txt /srv/lab/p6/ 2>/dev/null
ls -la /srv/lab/p6
```

```bash
total 0
drwxr-xr-x 1 root root  0 Nov 17 06:43 .
drwxrwxrwx 1 root root 24 Nov 17 06:43 ..
```

```bash
# --partial 을 주고 원격으로 보내다 끊으면 받은 만큼의 파일이 남는다
#   --partial   중단돼도 부분 파일을 지우지 않는다
timeout -s INT 2 rsync -a --partial --bwlimit=200 -e "ssh -p 2222" /srv/lab/big2.txt dev@node1:p4/ 2>&1 | head -3
ssh dev@node1 'ls -la p4'
```

```bash
rsync error: unexplained error (code 255) at rsync.c(874) [sender=3.5.0]
total 352
drwxr-xr-x 1 dev dev     16 Nov 17 06:37 .
drwxr-xr-x 1 dev dev     92 Nov 17 06:37 ..
-rw-r--r-- 1 dev dev 360448 Jan  1  1970 big2.txt
```

부분 파일은 크기가 원본보다 작고 수정 시각도 달라서 기본 기준이 다름으로 읽습니다. 그래도 이미 받은 앞부분은 일치 데이터로 건너뜁니다.

```bash
# 같은 명령을 다시 돌려 이어 받는다. Matched 가 이미 있던 앞부분이다
rsync -ai --partial --stats -e "ssh -p 2222" /srv/lab/big2.txt dev@node1:p4/ | grep -E 'big2|Total file size|Literal|Matched|Total bytes sent'
```

```bash
<f.st...... big2.txt
Total file size: 1,288,895 bytes
Literal data: 929,095 bytes
Matched data: 359,800 bytes
Total bytes sent: 931,476
```

### 실습 정리

```bash
# lab 셸을 나온 뒤 호스트에서 두 컨테이너를 지운다
docker rm -f lab srv
```



## 주의사항과 동작 원리

> 슬래시 한 글자와 `--delete` 가 파일을 엉뚱한 곳에 두거나 지우고, 환경 조건이 빠지면 조용히 다르게 동작합니다.

### 끝 슬래시 한 글자가 바꾸는 대상

> 원본 끝 `/` 를 빼면 대상 안에 한 단계 더 들어가므로, 설정 디렉터리를 배포할 때 가장 먼저 의심합니다.

```bash
# 원본 끝에 / 가 없어 conf 가 app/conf 안에 한 번 더 생긴다
rm -rf app; mkdir -p app/conf
rsync -a src/conf app/conf/; find app | sort
```

```bash
app
app/conf
app/conf/conf
app/conf/conf/app.yml
app/conf/conf/log.yml
```

```bash
# 원본 끝에 /: conf 의 내용이 app/conf 에 바로 들어간다
rm -rf app; mkdir -p app/conf
rsync -a src/conf/ app/conf/; find app | sort
```

```bash
app
app/conf
app/conf/app.yml
app/conf/log.yml
```

위 첫 결과가 `conf/conf/app.yml` 입니다. 어느 쪽이 의도인지는 `-n` 과 `-i` 로 먼저 확인하면 알 수 있습니다.

### --delete 를 dry-run 없이 쓰면

> `--delete` 는 대상 디렉터리 전체를 원본에 맞추므로, 대상을 잘못 고르면 거기 있던 파일이 사라집니다.

대상 `etc-app` 에 원본과 무관한 파일이 있다고 합시다.

```bash
# 원본 끝에 / 가 있으면 etc-app 전체가 동기화 대상이라 무관한 파일이 지워질 목록에 오른다
rm -rf etc-app; mkdir etc-app; echo 'db: prod' > etc-app/db.yml; echo keep > etc-app/keep.txt
rsync -ain --delete src/conf/ etc-app/
```

```bash
*deleting   keep.txt
*deleting   db.yml
.d..t...... ./
>f+++++++++ app.yml
>f+++++++++ log.yml
```

```bash
# -n 을 빼고 돌리면 db.yml·keep.txt 가 실제로 지워진다
rsync -a --delete src/conf/ etc-app/; ls etc-app    # app.yml log.yml
```

원본 끝 `/` 를 빼면 동기화 대상이 `etc-app/conf` 로 좁아져 무관한 파일은 목록에 오르지 않습니다.[^delete]

```bash
# 원본 끝에 / 가 없으면 etc-app/conf 만 대상이다. 지울 항목이 없다
rm -rf etc-app; mkdir etc-app; echo keep > etc-app/keep.txt
rsync -ain --delete src/conf etc-app/
```

```bash
cd+++++++++ conf/
>f+++++++++ conf/app.yml
>f+++++++++ conf/log.yml
```

`-n` 은 `-i` 나 `-v` 를 함께 줘야 보여 줍니다. `rsync -an src/conf/ etc-app/` 처럼 출력 옵션이 없으면 아무것도 안 찍고 0 으로 끝납니다.

### 원격에 rsync 가 없을 때

> `rsync` 는 원격에서도 `rsync` 를 실행하므로, 원격에 없으면 연결은 되는데 종료 코드 12 로 끝납니다.

`srv` 에는 `sshd` 만 있고 `rsync` 가 없습니다.[^rsh]

```bash
# 원격 셸이 rsync 를 못 찾아 연결이 곧바로 닫힌다
rsync -a src/ dev@srv:dst/; echo "rc=$?"
```

```bash
sh: 1: rsync: not found
rsync: connection unexpectedly closed (0 bytes received so far) [sender]
rsync error: error in rsync protocol data stream (code 12) at io.c(285) [sender=3.5.0]
rc=12
```

```bash
# 경로가 틀린 --rsync-path 도 같은 12 다. rsync 가 있어도 PATH 밖이면 이 옵션으로 위치를 준다
#   --rsync-path   원격에서 실행할 rsync 프로그램을 정한다
rsync -a --rsync-path=/no/such/rsync src/ dev@node1:dst2/; echo "rc=$?"
```

```bash
sh: 1: /no/such/rsync: not found
rsync: connection unexpectedly closed (0 bytes received so far) [sender]
rsync error: error in rsync protocol data stream (code 12) at io.c(285) [sender=3.5.0]
rc=12
```

원격에 `rsync` 를 설치할 수 없으면 `scp` 로 같은 일을 합니다. 사용법은 [scp·sftp 참조 시트](../ssh/scp%C2%B7sftp.md)에 있습니다.

### 소유자 보존은 root 만

> `-a` 는 `-o` 를 포함하지만 `-o` 는 슈퍼유저만 효력이 있어서, 일반 사용자가 돌리면 소유자가 그 사용자로 바뀝니다.

usage 의 옵션 목록이 `--owner, -o` 를 "preserve owner (super-user only)" 로 적습니다. root 와 일반 사용자 `dev` 가 같은 원본을 복사해 비교합니다.

```bash
# 원본 log.yml 의 소유자를 nobody 로 바꿔 두고 root 와 dev 로 각각 복사한다
rm -rf /srv/lab/src /srv/lab/by-root /srv/lab/by-dev
cp -a src /srv/lab/src; chown nobody:nogroup /srv/lab/src/conf/log.yml
rsync -a /srv/lab/src/ /srv/lab/by-root/
su dev -c 'rsync -a /srv/lab/src/ /srv/lab/by-dev/'
ls -l /srv/lab/src/conf/log.yml /srv/lab/by-root/conf/log.yml /srv/lab/by-dev/conf/log.yml
```

```bash
-rw-r--r-- 1 dev    dev     12 Nov 17 06:35 /srv/lab/by-dev/conf/log.yml
-rw-r--r-- 1 nobody nogroup 12 Nov 17 06:35 /srv/lab/by-root/conf/log.yml
-rw-r--r-- 1 nobody nogroup 12 Nov 17 06:35 /srv/lab/src/conf/log.yml
```

`dev` 의 복사본은 오류 없이 끝났지만 소유자가 `nobody` 가 아니라 `dev` 입니다.

### 로컬 복사와 델타 전송

> 원본과 대상이 모두 로컬 경로이면 `rsync` 는 파일을 통째로 보내므로, 파일 안의 바뀐 부분만 보내는 효과는 원격에서 납니다.

`--whole-file` 은 델타 전송 알고리즘을 끄는 옵션입니다. 원본과 대상이 모두 로컬일 때는 이것이 기본입니다.[^wholefile] `--stats` 의 `Literal data` 는 새로 보낸 바이트입니다. `Matched data` 는 대상에 이미 있어 건너뛴 바이트입니다.

```bash
# 1.3MB 파일에 두 글자를 덧붙여 로컬로 다시 복사한다. 통째로 다시 보낸다
mkdir -p /srv/lab/p5; cp /srv/lab/big2.txt /srv/lab/p5/; echo x >> /srv/lab/big2.txt
rsync -ai --stats /srv/lab/big2.txt /srv/lab/p5/ | grep -E 'big2|Literal|Matched'
```

```bash
>f.s....... big2.txt
Literal data: 1,288,897 bytes
Matched data: 0 bytes
```

```bash
# --no-whole-file 로 델타를 켜면 바뀐 부분만 보낸다
echo y >> /srv/lab/big2.txt
rsync -ai --no-whole-file --stats /srv/lab/big2.txt /srv/lab/p5/ | grep -E 'big2|Literal|Matched'
```

```bash
>f.s....... big2.txt
Literal data: 723 bytes
Matched data: 1,288,176 bytes
```

### 호스트 뒤 콜론을 빼면

> 호스트 뒤 콜론이 없으면 `rsync` 는 그 인자를 로컬 경로로 읽어, 원격이 아니라 로컬에 디렉터리를 만듭니다.

```bash
# dev@node1 뒤에 : 가 없어 로컬의 dev@node1 디렉터리에 복사하고 0 으로 끝난다
rsync -a src/ dev@node1; echo "rc=$?"
ls dev@node1
```

```bash
rc=0
conf
data
hard.txt
link.txt
notes.txt
```

책 노트도 같은 경고를 적습니다.



## 관련 문서

> 같은 폴더의 `ls` 시트와 파일 전송 시트, 배경이 되는 책 노트입니다.

- [ls 참조 시트](./ls.md) — 대상에서 `-l` 열로 소유자·권한·링크 수를 확인할 때
- [scp·sftp 참조 시트](../ssh/scp%C2%B7sftp.md) — 원격에 `rsync` 가 없을 때 파일을 옮기는 방법
- [주고받는 일은 결국 몇 개의 명령으로 줄어든다](../../../book/learning-modern-linux/07-03.%EC%A3%BC%EA%B3%A0%EB%B0%9B%EB%8A%94%20%EC%9D%BC%EC%9D%80%20%EA%B2%B0%EA%B5%AD%20%EB%AA%87%20%EA%B0%9C%EC%9D%98%20%EB%AA%85%EB%A0%B9%EC%9C%BC%EB%A1%9C%20%EC%A4%84%EC%96%B4%EB%93%A0%EB%8B%A4.md#두-번째-전송에서-갈린다) — `scp` 와 `rsync` 가 두 번째 전송에서 갈리는 이유
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경과 각주가 가리키는 매뉴얼입니다.

- 검증 환경: Debian GNU/Linux 12 (bookworm) 컨테이너, rsync 3.5.0+ds1-0+deb12u1(protocol 32), OpenSSH 9.2p1, acl 2.3.1, attr 2.5.1. 2026-11-17 실행
- [rsync(1) 매뉴얼](https://download.samba.org/pub/rsync/rsync.1) — 인용은 Debian 12 컨테이너의 `man rsync` 원문. 2026-11-17 조회
- [xattr(7) — Debian bookworm](https://manpages.debian.org/bookworm/manpages/xattr.7.en.html)

[^macos]: 이 시트를 쓴 macOS 호스트에서 `rsync --version` 의 출력(2026-11-17) — "openrsync: protocol version 29", "rsync version 2.6.9 compatible". 컨테이너의 `rsync --version` 첫 줄은 "rsync  version 3.5.0  protocol version 32" 입니다.
[^quick]: rsync(1) 3.5.0 (Debian 12 컨테이너, 2026-11-17), DESCRIPTION — "Rsync finds files that need to be transferred using a "quick check" algorithm (by default) that looks for files that have changed in size or in last-modified time", "Any changes in the other preserved attributes (as requested by options) are made on the destination file directly when the quick check indicates that the file's data does not need to be updated". https://download.samba.org/pub/rsync/rsync.1
[^slash]: rsync(1) 3.5.0, USAGE — "A trailing slash on the source changes this behavior to avoid creating an additional directory level at the destination. You can think of a trailing / on a source as meaning "copy the contents of this directory" as opposed to "copy the directory by name"", 같은 결과를 내는 예로 "rsync -av /src/foo /dest" 와 "rsync -av /src/foo/ /dest/foo". 원본이 하나뿐일 때의 대상 끝 `/` 는 같은 절의 "To prevent such an accident, either make sure the destination directory exists or specify the destination path with a trailing slash" 와 이 시트의 실측입니다. https://download.samba.org/pub/rsync/rsync.1
[^itemize]: rsync(1) 3.5.0, `--itemize-changes, -i` — "The "%i" escape has a cryptic output that is 11 letters long. The general format is like the string YXcstpoguax, where Y is replaced by the type of update being done, X is replaced by the file-type, and the other letters represent attributes that may be output if they are being modified", "A < means that a file is being transferred to the remote host (sent)", "A > means that a file is being transferred to the local host (received)", "A c means either that a regular file has a different checksum (requires --checksum) or that a symlink, device, or special file has a changed value", "when deleting files, the "%i" will output the string "*deleting"", "If you repeat the option, unchanged files will also be output". https://download.samba.org/pub/rsync/rsync.1
[^exit]: rsync(1) 3.5.0, EXIT VALUES — "0 - Success", "1 - Syntax or usage error", "2 - Protocol incompatibility", "3 - Errors selecting input/output files, directories", "5 - Error starting client-server protocol", "10 - Error in socket I/O", "11 - Error in file I/O", "12 - Error in rsync protocol data stream", "20 - Received SIGINT, SIGTERM, or SIGHUP", "23 - Partial transfer due to error", "24 - Partial transfer due to vanished source files", "25 - The --max-delete limit stopped deletions", "30 - Timeout in data send/receive". 3 대신 23 이 나온 것은 이 시트의 실측입니다(Debian 12 컨테이너, rsync 3.5.0). https://download.samba.org/pub/rsync/rsync.1
[^checksum]: rsync(1) 3.5.0, `--checksum, -c` — "Without this option, rsync uses a "quick check" that (by default) checks if each file's size and time of last modification match between the sender and receiver. This option changes this to compare a checksum for each file that has a matching size. Generating the checksums means that both sides will expend a lot of disk I/O reading all the data in the files in the transfer". https://download.samba.org/pub/rsync/rsync.1
[^delete]: rsync(1) 3.5.0, `--delete` — "This tells rsync to delete extraneous files from the receiving side (those that don't exist on the sending side), but only for the directories that are being synchronized". `--dry-run, -n` — "This makes rsync perform a trial run that doesn't make any changes, and produces mostly the same output as a real run. It is most commonly used in combination with the --verbose (-v) and/or --itemize-changes (-i) options to see what an rsync command is going to do before one actually runs it". https://download.samba.org/pub/rsync/rsync.1
[^archive]: rsync(1) 3.5.0, `--archive, -a` — "This is equivalent to -rlptgoD. It is a quick way of saying you want recursion and want to preserve almost everything. Be aware that it does not include preserving ACLs (-A), xattrs (-X), atimes (-U), crtimes (-N), nor the finding and preserving of hardlinks (-H)". https://download.samba.org/pub/rsync/rsync.1
[^hardlink]: rsync(1) 3.5.0, `--hard-links, -H` — "This tells rsync to look for hard-linked files in the source and link together the corresponding files on the destination. Without this option, hard-linked files in the source are treated as though they were separate files". https://download.samba.org/pub/rsync/rsync.1
[^xattr]: rsync(1) 3.5.0, `--acls, -A` — "This option causes rsync to update the destination ACLs to be the same as the source ACLs. The option also implies --perms". `--xattrs, -X` — "For systems that support extended-attribute namespaces, a copy being done by a super-user copies all namespaces except system.*. A normal user only copies the user.* namespace". https://download.samba.org/pub/rsync/rsync.1
[^secns]: xattr(7) (Linux man-pages 6.03, Debian 12 `manpages` 6.03-2) — "The security attribute namespace is used by kernel security modules, such as Security Enhanced Linux, and also to implement file capabilities". Debian 12 컨테이너에는 SELinux 가 없고 `security.*` 속성은 쓰기 권한이 없어("Operation not permitted") 라벨 자체는 실측하지 못했고, 위 실측은 `user.*` 입니다. https://manpages.debian.org/bookworm/manpages/xattr.7.en.html
[^rsh]: rsync(1) 3.5.0, `--rsh=COMMAND, -e` — "This option allows you to choose an alternative remote shell program to use for communication between the local and remote copies of rsync. Typically, rsync is configured to use ssh by default". `--rsync-path=PROGRAM` — "Use this to specify what program is to be run on the remote machine to start-up rsync. Often used when rsync is not in the default remote-shell's path". https://download.samba.org/pub/rsync/rsync.1
[^compress]: rsync(1) 3.5.0, `--compress, -z` — "With this option, rsync compresses the file data as it is sent to the destination machine, which reduces the amount of data being transmitted -- something that is useful over a slow connection". https://download.samba.org/pub/rsync/rsync.1
[^bwlimit]: rsync(1) 3.5.0, `--bwlimit=RATE` — "This option allows you to specify the maximum transfer rate for the data sent over the socket, specified in units per second", "If no suffix is specified, the value will be assumed to be in units of 1024 bytes (as if "K" or "KiB" had been appended)". `-P` 는 `--help` 옵션 목록의 "-P same as --partial --progress" 입니다. https://download.samba.org/pub/rsync/rsync.1
[^partial]: rsync(1) 3.5.0, `--partial` — "By default, rsync will delete any partially transferred file if the transfer is interrupted. In some circumstances it is more desirable to keep partially transferred files. Using the --partial option tells rsync to keep the partial file which should make a subsequent transfer of the rest of the file much faster". https://download.samba.org/pub/rsync/rsync.1
[^wholefile]: rsync(1) 3.5.0, `--whole-file, -W` — "This option disables rsync's delta-transfer algorithm, causing the whole of all transferred files to be sent", "This is the default when both the source and destination are specified as local paths, but only if no batch-writing option is in effect". `--no-whole-file` 은 "Disable whole-file updating when it is enabled by default for a local transfer". https://download.samba.org/pub/rsync/rsync.1
