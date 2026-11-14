---
title: scp·sftp 참조 시트
tags: [linux, cheatsheet, ssh, scp, sftp, file-transfer, reference]
status: draft
source:
  - OpenSSH 9.2p1 scp(1)·sftp(1) (Debian 12 컨테이너의 `man` 원문, manpages.debian.org bookworm)
related:
  - ./ssh.md
  - ./ssh-keygen·ssh-copy-id·ssh-agent.md
  - ./sshd·sshd_config.md
  - ../README.md
updated: 2026-11-14
---

# scp·sftp 참조 시트

---

> ssh 연결로 파일과 디렉터리를 주고받는 `scp` 와, 명령을 파일로 적어 한꺼번에 돌리는 `sftp -b` 를 컨테이너에서 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `scp` 는 파일을 한 번 복사하고 끝나는 명령이고, `sftp` 는 원격 디렉터리를 보면서 여러 명령을 주고받는 파일 전송 클라이언트입니다.

두 명령은 Debian 12 의 `openssh-client` 1:9.2p1 패키지가 `/usr/bin/scp`·`/usr/bin/sftp` 로 설치하는 외부 바이너리입니다. 출력은 `ssh -V` 가 `OpenSSH_9.2p1 Debian-2+deb12u10, OpenSSL 3.0.22` 로 답하는 컨테이너에서 받았습니다. 이 판의 `scp` 는 SFTP 프로토콜로 전송하고, 옛 SCP 프로토콜은 `-O` 로 되살립니다.[^protocol]

이 시트는 `ssh` 시트의 「실습 준비」 를 이어받습니다. 컨테이너 셋(`srv`·`jump`·`cli`)과 `cli` 의 `appuser` 키가 이미 있어야 하므로 [ssh 접속·config·포트 포워딩 참조 시트](./ssh.md) 의 준비 블록을 먼저 돌려 둡니다. 키를 만들고 올리는 방법은 [ssh-keygen·ssh-copy-id·ssh-agent 참조 시트](./ssh-keygen·ssh-copy-id·ssh-agent.md) 가 맡습니다.



## 핵심 문법

> `scp` 는 원본과 대상 두 자리에 `[사용자@]호스트:경로` 꼴을 두고 어느 쪽이 원격인지로 방향을 정하며, `sftp` 는 접속한 뒤 `get`·`put` 같은 명령으로 방향을 정합니다.

```bash
# scp 호출 형태 (scp 인자 없이 부르면 나오는 사용법)
usage: scp [-346ABCOpqRrsTv] [-c cipher] [-D sftp_server_path] [-F ssh_config]
           [-i identity_file] [-J destination] [-l limit] [-o ssh_option]
           [-P port] [-S program] [-X sftp_option] source ... target

# sftp 호출 형태 (sftp 인자 없이 부르면 나오는 사용법)
usage: sftp [-46AaCfNpqrv] [-B buffer_size] [-b batchfile] [-c cipher]
          [-D sftp_server_command] [-F ssh_config] [-i identity_file]
          [-J destination] [-l limit] [-o ssh_option] [-P port]
          [-R num_requests] [-S program] [-s subsystem | sftp_server]
          [-X sftp_option] destination

# 로컬 파일을 서버로 올린다 (파일 하나 올리고 내려받기)
scp 파일 호스트:경로

# 서버 파일을 로컬로 내려받는다 (파일 하나 올리고 내려받기)
scp 호스트:경로 로컬경로

# 디렉터리째 복사한다 (디렉터리 복사하기)
scp -r 디렉터리 호스트:경로

# 포트·키·보존 옵션을 정한다 (포트·키·옵션 정하기)
scp \
  -P 포트 \
  -i 키파일 \
  -p \
  파일 호스트:경로

# 점프 호스트를 거치거나 서버 사이를 복사한다 (점프 호스트 거치기와 서버 사이 복사)
scp -J 점프호스트 파일 호스트:경로
scp 호스트1:경로 호스트2:경로

# sftp 로 원격 디렉터리를 보며 주고받는다 (sftp 배치 파일로 돌리기)
sftp 호스트
sftp -b 명령파일 호스트
```

### sftp 에서 쓰는 명령

> 명령은 `sftp>` 프롬프트나 `-b` 파일에 한 줄에 하나씩 적습니다. `l` 로 시작하는 명령은 로컬 쪽에서 돕니다.

```bash
# sftp 명령. help 가 찍는 목록에서 이 시트의 예가 쓰는 것만 옮겼다
#   pwd / lpwd         원격 / 로컬 작업 디렉터리를 찍는다
#   cd / lcd           원격 / 로컬 디렉터리를 옮긴다
#   ls [-l] [경로]     원격 목록
#   get 원격 [로컬]    내려받기
#   put 로컬 [원격]    올리기
#   mkdir / rmdir      원격 디렉터리 만들기 / 지우기
#   rename 이전 이후   원격 이름 바꾸기
#   chmod 모드 경로    원격 권한 바꾸기
#   rm 경로            원격 파일 지우기
#   bye                끝낸다. exit·quit 도 같다
```



## 종료 코드

> `scp` 는 성공이면 0 이고 실패면 0 보다 큰 값이며, `sftp` 는 man 에 종료 코드 절이 없어 실측한 값만 싣습니다.[^exit-scp][^no-exit]

```bash
# scp   0 성공
#       0 보다 큰 값  오류가 났다

# 실측한 scp 코드. 값마다 상황이 다르다
scp nosuch.txt srv:/tmp/; echo $?    # scp: stat local "nosuch.txt": No such file or directory / 255
scp; echo $?    # 사용법 / 1
```

원격 쪽에서 실패한 예는 「실습 준비」 를 마친 뒤 `~/xfer` 에서 돌립니다. 로컬 파일이 없으면 위처럼 255 가 먼저 나옵니다.

```bash
# 원격 대상 폴더가 없다
scp a.txt srv:/nonexistent/dir/; echo $?
```

```bash
scp: dest open "/nonexistent/dir/": No such file or directory
scp: failed to upload file a.txt to /nonexistent/dir/
1
```

```bash
# 실측한 sftp 코드
# sftp  0   배치 파일의 명령이 모두 성공함
#       1   배치 파일의 명령 하나가 실패해 sftp 가 멈춤. 인자 없이 불러도 1
#       255 접속하지 못함
```



## 유스케이스

> 예는 앞 예가 만든 상태를 이어 쓰므로 위에서 아래로 차례로 돌립니다. 모두 `cli` 의 `appuser` 셸에서 돌립니다.

### 실습 준비

> 이 시트는 `ssh` 시트의 준비 블록이 만든 컨테이너 셋을 쓰고, 복사할 파일과 디렉터리, 호스트 키 자동 수락 설정을 `cli` 에 더 만듭니다.

이 파일들은 「파일 하나 올리고 내려받기」·「디렉터리 복사하기」 부터 여러 곳이 씁니다.

```bash
# 새 호스트 키는 묻지 않고 받는 설정을 둔다
# ssh 시트의 config 예와 같은 줄이라 두 번 들어가도 같은 값이다
#   accept-new   처음 보는 호스트 키는 받고, 바뀐 키는 거부한다
mkdir -p ~/.ssh
printf 'Host *\n  StrictHostKeyChecking accept-new\n' >> ~/.ssh/config

# 권한이 넓으면 ssh 가 config 를 읽지 않는다
chmod 600 ~/.ssh/config

# 접속할 호스트의 키를 미리 받아 둔다
# 2222 번 sshd 는 22 번과 같은 호스트 키라 포트 없는 srv 줄로 확인된다
ssh srv true
ssh -p 2222 srv true
ssh jump true

# 복사할 파일 하나와 디렉터리(site) 하나를 만든다
mkdir -p ~/xfer/site/css
cd ~/xfer
echo 'hello from cli' > a.txt
echo 'body{}' > site/css/main.css
echo '<h1>hi</h1>' > site/index.html

#   ls -R   하위 디렉터리까지 목록을 찍는다
ls -R ~/xfer
```

```bash
/home/appuser/xfer:
a.txt  site

/home/appuser/xfer/site:
css  index.html

/home/appuser/xfer/site/css:
main.css
```

### 파일 하나 올리고 내려받기

> 원격 쪽에 `호스트:` 를 붙이면 그쪽이 원격이 되어, 올리기와 내려받기가 인자 순서만으로 갈립니다.

```bash
# 파일을 srv 의 /tmp 로 올린다
scp a.txt srv:/tmp/
```

```bash
a.txt                                           100%   15   211.3KB/s   00:00
```

진행 표시줄은 표준 출력이 터미널일 때만 나오고, 속도와 시간은 실행마다 다릅니다.

```bash
# 올라간 파일을 확인한다
ssh srv 'cat /tmp/a.txt'    # hello from cli

# 진행 표시줄 없이 올린다
#   -q   진행 표시줄과 경고를 끈다
scp -q a.txt srv:/tmp/b.txt

# 서버의 파일을 로컬 back.txt 로 내려받는다
scp srv:/tmp/a.txt ./back.txt
cat back.txt    # hello from cli
```

### 디렉터리 복사하기

> `-r` 이 없으면 디렉터리는 복사되지 않고 1 로 끝나며, `-r` 을 주면 하위 디렉터리까지 따라갑니다.

```bash
# -r 없이 디렉터리를 올린다
scp site srv:/tmp/; echo $?
```

```bash
scp: local "site" is not a regular file
scp: failed to upload file site to /tmp/
1
```

```bash
# 디렉터리를 하위 파일까지 올린다
#   -r   디렉터리를 재귀로 복사한다
scp -r site srv:/tmp/

# 서버에 생긴 파일을 확인한다
ssh srv 'find /tmp/site | sort'
```

```bash
/tmp/site
/tmp/site/css
/tmp/site/css/main.css
/tmp/site/index.html
```

### 포트·키·옵션 정하기

> `-P` 는 포트를, `-i` 는 키를, `-p` 는 시간과 모드 보존을, `-o` 는 ssh 옵션을 정합니다.

```bash
# 2222 번 sshd 로 접속해 올린다. 대문자 P 임에 주의한다
#   -P   서버 포트. ssh 의 -p 와 글자가 다르다
scp -P 2222 a.txt srv:/tmp/c.txt

# 키를 정해 올린다
#   -i   쓸 개인 키 파일
scp -i ~/.ssh/id_work a.txt srv:/tmp/d.txt

# 수정 시각을 보존해 올린다
#   -p   수정 시각·접근 시각·모드를 원본 그대로 둔다
scp -p a.txt srv:/tmp/p.txt
#   stat -c   정한 형식으로 찍는다. %y 는 수정 시각
ssh srv 'stat -c "%y" /tmp/p.txt'    # 2026-11-13 23:12:38.000000000 +0000
stat -c '%y' a.txt    # 2026-11-13 23:12:38.349773440 +0000
```

`-p` 로 올린 시각은 초 아래가 잘려 같은 초까지만 맞습니다.

```bash
# 서버에 등록하지 않은 키 하나만 쓰면 인증이 거절된다
#   -o   ssh 옵션. IdentitiesOnly=yes 면 -i 로 정한 키만 낸다
scp -o IdentitiesOnly=yes -i ~/.ssh/id_stray a.txt srv:/tmp/e.txt; echo $?
```

```bash
appuser@srv: Permission denied (publickey).
scp: Connection closed
255
```

### 점프 호스트 거치기와 서버 사이 복사

> `-J` 로 점프 호스트를 거치고, 원본과 대상이 모두 원격이면 서버 사이를 한 줄로 복사합니다.

```bash
# jump 를 거쳐 srv 로 올린다
#   -J   거쳐 갈 점프 호스트
scp -J jump a.txt srv:/tmp/j.txt

# srv 의 파일을 jump 로 복사한다. 원본과 대상이 모두 원격이다
scp -q srv:/tmp/a.txt jump:/tmp/from-srv.txt

# 데이터가 cli 를 거치게 명시한다
#   -3   두 원격 사이의 데이터를 로컬을 거쳐 전송한다
scp -q -3 srv:/tmp/a.txt jump:/tmp/from-srv3.txt
```

두 번째 줄은 `-3` 이 없는데도 에이전트나 `srv` 의 개인 키 없이 성공합니다. 이유는 「서버 사이 복사의 출발지」 에 있습니다.

### 원격 와일드카드 받기

> 원격 쪽의 `*` 는 홑따옴표로 감싸 서버가 펼치게 하며, 따옴표가 없으면 로컬 셸이 먼저 펼칩니다.

```bash
# srv 의 /tmp 에서 .txt 로 끝나는 파일을 모두 내려받는다
scp -q 'srv:/tmp/*.txt' ~/xfer/
ls ~/xfer
```

```bash
a.txt  b.txt  back.txt  c.txt  d.txt  in.txt  j.txt  p.txt  site
```

### sftp 배치 파일로 돌리기

> `sftp -b` 는 명령을 적은 파일을 위에서 아래로 실행하며, 명령 하나가 실패하면 거기서 멈춥니다.

```bash
# 배치 파일을 만든다. 원격에 디렉터리를 만들고 올리고 받고 이름과 권한을 바꾼 뒤 지운다
cat > batch.txt <<'X'
pwd
lpwd
mkdir /tmp/inbox
put a.txt /tmp/inbox/a.txt
ls -l /tmp/inbox
get /tmp/inbox/a.txt got.txt
rename /tmp/inbox/a.txt /tmp/inbox/a2.txt
chmod 600 /tmp/inbox/a2.txt
ls -l /tmp/inbox
rm /tmp/inbox/a2.txt
rmdir /tmp/inbox
bye
X

# 배치 파일로 돌린다
#   sftp -b   명령을 읽을 파일
sftp -b batch.txt srv; echo $?
```

```bash
sftp> pwd
Remote working directory: /home/appuser
sftp> lpwd
Local working directory: /home/appuser/xfer
sftp> mkdir /tmp/inbox
sftp> put a.txt /tmp/inbox/a.txt
sftp> ls -l /tmp/inbox
-rw-r--r--    ? appuser  appuser        15 Nov 13 23:13 /tmp/inbox/a.txt
sftp> get /tmp/inbox/a.txt got.txt
sftp> rename /tmp/inbox/a.txt /tmp/inbox/a2.txt
sftp> chmod 600 /tmp/inbox/a2.txt
sftp> ls -l /tmp/inbox
-rw-------    ? appuser  appuser        15 Nov 13 23:13 /tmp/inbox/a2.txt
sftp> rm /tmp/inbox/a2.txt
sftp> rmdir /tmp/inbox
sftp> bye
0
```

`ls -l` 의 링크 수 자리는 `?` 로 나오고, 시각은 실행마다 다릅니다.

```bash
# 파일 대신 표준 입력으로 명령을 준다. 포트도 정할 수 있다
#   sftp -P   서버 포트
sftp -P 2222 -b - srv <<'X'
pwd
X
```

```bash
sftp> pwd
Remote working directory: /home/appuser
```

```bash
# 명령이 실패하면 1 로 끝나고 뒤 명령은 돌지 않는다
printf 'ls /nonexistent\npwd\n' > bad.txt
sftp -b bad.txt srv; echo $?
```

```bash
sftp> ls /nonexistent
Can't ls: "/nonexistent" not found
1
```

```bash
# 명령 앞에 - 를 붙이면 실패해도 다음 명령으로 간다
printf -- '-ls /nonexistent\npwd\n' > bad2.txt
sftp -b bad2.txt srv; echo $?
```

```bash
sftp> -ls /nonexistent
Can't ls: "/nonexistent" not found
sftp> pwd
Remote working directory: /home/appuser
0
```

### 실습 정리

> 「주의사항과 동작 원리」 의 예도 `~/xfer` 와 서버의 `/tmp` 파일을 쓰므로 그 절까지 마친 뒤 지웁니다. 컨테이너와 네트워크는 `ssh` 시트의 「실습 정리」 가 지웁니다.

```bash
# 이 시트가 cli 와 srv·jump 의 /tmp 에 만든 파일을 지운다
rm -rf ~/xfer
ssh srv 'rm -rf /tmp/*.txt /tmp/site /tmp/newdir /tmp/dot'
ssh jump 'rm -f /tmp/*.txt'
```



## 주의사항과 동작 원리

### scp 가 쓰는 프로토콜

> 이 판의 `scp` 는 SFTP 프로토콜로 전송하고, SFTP 를 구현하지 않은 서버에는 `-O` 로 SCP 프로토콜을 강제합니다.

```bash
# 접속 과정을 보면 scp 가 서버에 sftp 서브시스템을 요청한다
#   -v   ssh 의 디버그 메시지를 함께 보여 준다
scp -v a.txt srv:/tmp/v.txt 2>&1 | grep -E 'Sending subsystem|Executing'
```

```bash
Executing: program /usr/bin/ssh host srv, user (unspecified), command sftp
debug1: Sending subsystem: sftp
```

명령 모양은 그대로인데 서버에 요청하는 것은 `sftp` 서브시스템입니다. `-O` 는 SFTP 를 구현하지 않은 서버에 쓰는 옵션입니다.[^protocol]

### 디렉터리를 복사할 때 대상이 이미 있는 경우

> `scp -r 디렉터리 호스트:대상` 은 대상이 없으면 대상 이름으로 복사하고, 이미 있으면 그 안에 디렉터리 이름으로 복사합니다.

```bash
# 대상(newdir)이 없을 때 한 번, 있을 때 한 번 올리고 구조를 본다
scp -q -r site srv:/tmp/newdir
ssh srv 'find /tmp/newdir | sort'
```

```bash
/tmp/newdir
/tmp/newdir/css
/tmp/newdir/css/main.css
/tmp/newdir/index.html
```

```bash
# 같은 명령을 한 번 더 돌린다
scp -q -r site srv:/tmp/newdir
ssh srv 'find /tmp/newdir | sort'
```

```bash
/tmp/newdir
/tmp/newdir/css
/tmp/newdir/css/main.css
/tmp/newdir/index.html
/tmp/newdir/site
/tmp/newdir/site/css
/tmp/newdir/site/css/main.css
/tmp/newdir/site/index.html
```

```bash
# 같은 이름의 중첩을 피하려면 디렉터리 안쪽 내용을 가리킨다
scp -q -r site/. srv:/tmp/dot
ssh srv 'find /tmp/dot | sort'
```

```bash
/tmp/dot
/tmp/dot/css
/tmp/dot/css/main.css
/tmp/dot/index.html
```

같은 명령을 두 번 돌리면 결과가 달라지므로, 스크립트에서는 대상을 먼저 만들거나 `site/.` 꼴을 씁니다.

### 서버 사이 복사의 출발지

> `-3` 없이 서버 둘을 복사해도 jump 의 sshd 가 본 접속은 srv 가 아니라 cli 의 주소에서 왔습니다.

```bash
# jump 의 로그에서 cli(192.0.2.20)에서 온 접속 수를 센다. 호스트 터미널에서 돌린다
# 숫자는 앞선 예에서 jump 에 접속한 횟수에 따라 다르고, 둘째 값이 하나 크다
#   grep -c   일치한 줄 수를 센다
docker exec jump \
  grep -c 'Accepted publickey for appuser from 192.0.2.20 ' /var/log/sshd.log    # 10

# -3 없이 서버 사이를 한 번 복사한 뒤 다시 센다
docker exec -u appuser cli scp -q srv:/tmp/a.txt jump:/tmp/r3.txt
docker exec jump \
  grep -c 'Accepted publickey for appuser from 192.0.2.20 ' /var/log/sshd.log    # 11
```

man 의 `-3` 항목은 `-3` 이 없으면 두 원격 호스트가 직접 주고받는다고 적은 뒤 이 방식(`-3`)이 기본이라고 덧붙입니다.[^third] 실측에서도 `-3` 유무와 상관없이 접속이 `cli` 쪽에서 늘었으므로 `srv` 에 `jump` 로 가는 키가 없어도 복사됩니다.

### 파일 이름의 콜론

> 로컬 파일 이름에 `:` 가 있으면 `scp` 가 앞부분을 호스트 이름으로 읽으므로 `./` 를 붙여 로컬 경로임을 밝힙니다.

```bash
# a:b.txt 를 호스트 a 의 b.txt 로 읽는다
echo x > 'a:b.txt'
scp a:b.txt srv:/tmp/; echo $?
```

```bash
ssh: Could not resolve hostname a: Name or service not known
scp: Connection closed
255
```

```bash
# ./ 를 붙이면 로컬 파일로 읽는다
scp -q ./a:b.txt srv:/tmp/; echo $?    # 0
```

`scp` 는 첫 `:` 앞을 호스트로 봅니다.[^colon]



## 관련 문서

> 이 시트의 전송이 쓰는 접속과 키, 서버 쪽 설정을 이어서 볼 수 있습니다.

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [ssh 접속·config·포트 포워딩 참조 시트](./ssh.md) — 이 시트가 이어받는 「실습 준비」 와 `-J`·`-o`·`~/.ssh/config`
- [ssh-keygen·ssh-copy-id·ssh-agent 참조 시트](./ssh-keygen·ssh-copy-id·ssh-agent.md) — 전송에 쓰는 키를 만들고 올리는 방법
- [sshd·sshd_config 참조 시트](./sshd·sshd_config.md) — 서버가 `sftp` 서브시스템을 여는 설정과 로그
- [주고받는 일은 결국 몇 개의 명령으로 줄어든다](../../../book/learning-modern-linux/07-03.주고받는%20일은%20결국%20몇%20개의%20명령으로%20줄어든다.md) — `scp` 가 속한 원격 작업 명령의 지도



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- OpenSSH 9.2p1(`openssh-client` 1:9.2p1-2+deb12u10)의 `scp`·`sftp` 사용법·`man scp`·`man sftp` 원문 — Debian 12 컨테이너 셋에서 2026-11-14 확인
- [scp(1)](https://manpages.debian.org/bookworm/openssh-client/scp.1.en.html) — 옵션 뜻과 종료 코드 원문
- [sftp(1)](https://manpages.debian.org/bookworm/openssh-client/sftp.1.en.html) — 옵션·배치 모드·명령 목록 원문

[^protocol]: scp(1) — "scp uses the SFTP protocol over a ssh(1) connection for data transfer, and uses the same authentication and provides the same security as a login session." "-O Use the legacy SCP protocol for file transfers instead of the SFTP protocol." <https://manpages.debian.org/bookworm/openssh-client/scp.1.en.html>
[^exit-scp]: scp(1) EXIT STATUS — "The scp utility exits 0 on success, and >0 if an error occurs." <https://manpages.debian.org/bookworm/openssh-client/scp.1.en.html>
[^no-exit]: sftp(1) 의 man 에는 종료 코드 절이 없습니다. 아래 값은 컨테이너에서 해당 호출을 돌려 `echo $?` 로 읽은 것입니다. 배치 모드의 중단 규칙은 sftp(1) 의 `-b` 항목에 있습니다.
[^third]: scp(1) — "-3 Copies between two remote hosts are transferred through the local host. Without this option the data is copied directly between the two remote hosts. … This mode is the default." 이 문장은 man 원문이고, 위 접속 수 비교는 컨테이너에서 측정한 값입니다. <https://manpages.debian.org/bookworm/openssh-client/scp.1.en.html>
[^colon]: scp(1) — "Local file names can be made explicit using absolute or relative pathnames to avoid scp treating file names containing ':' as host specifiers." <https://manpages.debian.org/bookworm/openssh-client/scp.1.en.html>
