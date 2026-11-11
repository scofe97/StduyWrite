---
title: lsof 참조 시트
tags: [linux, cheatsheet, lsof, file-descriptor, socket, cli, reference]
status: draft
source:
  - lsof 4.95.0 lsof(8) (Debian 12 패키지, manpages.debian.org bookworm)
  - Linux man-pages proc(5), unlink(2), pid_namespaces(7), capabilities(7) (Debian 12 manpages)
  - coreutils df(1), du(1) (Debian 12 manpages)
related:
  - ../README.md
  - ../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md
updated: 2026-11-11
---

# lsof 참조 시트

---

> 프로세스가 열어 둔 파일과 소켓을 보는 `lsof` 의 옵션을 출력 열 읽기, 프로세스·파일·포트에서 출발하기, 지운 파일 찾기, 스크립트용 출력으로 나눠, 따라 치면 그대로 나오는 예제로 모았습니다.

## 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 프로세스와 파일이 모두 뜹니다.

macOS 의 `lsof` 는 Apple 이 따로 낸 판이라 열과 옵션 일부가 다릅니다. 이 시트는 Linux 용 lsof 4.95.0 을 씁니다. `docker run -it --rm --cap-add SYS_PTRACE debian:12` 로 연 Debian 12 컨테이너나 OrbStack 의 Linux VM 에서 root 로 실행합니다. `--cap-add SYS_PTRACE` 가 필요한 이유는 7절에서 봅니다. 출력은 터미널 폭과 무관합니다.

```bash
mkdir -p ~/cmd-lab/lsof && cd ~/cmd-lab/lsof
apt-get -qq update >/dev/null 2>&1; apt-get -qq install -y lsof procps netbase netcat-openbsd python3-minimal >/dev/null 2>&1
id appuser >/dev/null 2>&1 || useradd -m appuser
mkdir -p logs/old /dev/shm/lsof-lab
echo 'start' > logs/app.log
dd if=/dev/zero of=/dev/shm/lsof-lab/big.log bs=1M count=20 2>/dev/null
cat > holder.py << 'EOF2'
import time
log = open('logs/app.log', 'a')
conf = open('logs/app.conf', 'w')
old = open('logs/old/app.log.1', 'w')
time.sleep(700)
EOF2
cat > conn.py << 'EOF2'
import socket, time
s = socket.create_connection(('127.0.0.1', 8080))
time.sleep(701)
EOF2
cp /bin/sleep long-running-worker
python3 holder.py &
python3 -m http.server 8080 --bind 127.0.0.1 >/dev/null 2>&1 &
nc -4 -l 9000 &
nc -lU ~/cmd-lab/lsof/app.sock &
tail -f /dev/shm/lsof-lab/big.log >/dev/null 2>tail.err &
./long-running-worker 703 &
(cd /home/appuser && setpriv --reuid=appuser --regid=appuser --init-groups python3 -m http.server 8081 --bind 127.0.0.1 >/dev/null 2>&1) &
sleep 1
python3 conn.py &
sleep 1
```

이 블록은 열린 파일을 만드는 프로세스를 여럿 띄웁니다. `holder.py` 는 `logs/` 아래 파일 셋을 열고 700초 동안 쥐고 있습니다. `python3 -m http.server 8080` 은 127.0.0.1 의 8080 포트를 듣고, `conn.py` 가 거기에 붙어 연결 하나를 유지합니다. `appuser` 소유의 `http.server` 는 8081 포트를 듣습니다. `nc` 는 TCP 9000 포트와 유닉스 소켓 `app.sock` 을 각각 듣습니다.

`tail -f` 는 tmpfs 인 `/dev/shm` 의 20MB 파일을 열어 둡니다. 4절에서 이 파일을 지웁니다. `long-running-worker` 는 `sleep` 을 이름이 긴 파일로 복사한 것으로 1절에서 COMMAND 열이 이름을 자르는 모습에 씁니다. 대화형 셸에서는 `[1] 3153` 같은 잡 번호 줄이 더 나옵니다.

PID·장치 번호·inode·소켓 번호·임시 포트(`conn.py` 가 쓰는 포트)·`ls -l` 의 시각은 실행마다 다르므로 이 시트의 값과 같지 않아도 됩니다. 아래 예는 `holder.py` 의 PID 를 `$(pgrep -f holder.py)` 로 구해 씁니다.



## 1. 출력의 열 읽기

> `lsof` 는 프로세스마다 열린 파일을 한 줄씩 찍고, 한 줄은 아홉 열로 읽습니다. FD 와 TYPE 이 그 파일이 무엇인지 알려 줍니다.

프로세스가 무엇을 열어 두었는지 알려면 `-p` 에 PID 를 줍니다. 리눅스에서는 소켓도 파일 디스크립터라 일반 파일과 같은 목록에 나옵니다. `lsof` 라는 이름이 "list open files" 의 줄임말입니다.[^out]

```bash
# -p (PID): 그 프로세스가 연 파일 전부. 열은 COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME
lsof -p $(pgrep -f holder.py)
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3153 root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
python3 3153 root  rtd    DIR   0,61       42 4348902 /
python3 3153 root  txt    REG   0,61  6616880 4349624 /usr/bin/python3.11
python3 3153 root  mem    REG   0,61   353616 3986986 /usr/lib/locale/C.utf8/LC_CTYPE
python3 3153 root  mem    REG   0,61  1651408 3986083 /usr/lib/aarch64-linux-gnu/libc.so.6
python3 3153 root  mem    REG   0,61   198712 4349585 /usr/lib/aarch64-linux-gnu/libexpat.so.1.8.10
python3 3153 root  mem    REG   0,61   133520 3986181 /usr/lib/aarch64-linux-gnu/libz.so.1.2.13
python3 3153 root  mem    REG   0,61   591960 3986122 /usr/lib/aarch64-linux-gnu/libm.so.6
python3 3153 root  mem    REG   0,61   202912 3986065 /usr/lib/aarch64-linux-gnu/ld-linux-aarch64.so.1
python3 3153 root  mem    REG   0,61    27028 3986056 /usr/lib/aarch64-linux-gnu/gconv/gconv-modules.cache
python3 3153 root    0r   CHR    1,3      0t0       5 /dev/null
python3 3153 root    1w  FIFO   0,15      0t0  401170 pipe
python3 3153 root    2w  FIFO   0,15      0t0  401170 pipe
python3 3153 root    3w   REG   0,61        6 4353537 /root/cmd-lab/lsof/logs/app.log
python3 3153 root    4w   REG   0,61        0 4353543 /root/cmd-lab/lsof/logs/app.conf
python3 3153 root    5w   REG   0,61        0 4353544 /root/cmd-lab/lsof/logs/old/app.log.1
```

열마다 man 의 「OUTPUT」은 다음과 같이 풀이합니다.[^out]

- `COMMAND` 는 명령 이름의 앞 아홉 글자입니다. `PID` 는 프로세스 번호이고 `USER` 는 그 프로세스를 가진 사용자입니다.
- `FD` 는 파일 디스크립터 번호이거나 아래 표의 이름입니다. 번호 뒤에 열린 방식(`r` 읽기, `w` 쓰기, `u` 읽기와 쓰기)이 한 글자 붙고, 그 뒤에 잠금 글자가 올 수 있습니다.
- `TYPE` 은 파일의 종류입니다. 이 시트에서는 `REG`(일반 파일), `DIR`(디렉터리), `CHR`(문자 장치), `FIFO`(파이프), `IPv4`(IPv4 소켓), `unix`(유닉스 소켓)가 나옵니다.
- `DEVICE` 는 일반 파일·디렉터리·문자 장치에서는 쉼표로 나눈 장치 번호(`0,61`)입니다. 이 환경에서는 FIFO 도 `0,15` 처럼 장치 번호로 나옵니다. IPv4 소켓에서는 `/proc/PID/fd` 의 `socket:[번호]` 와 같은 번호가, 유닉스 소켓에서는 커널 주소가 찍힙니다.
- `SIZE/OFF` 는 파일 크기이거나 오프셋입니다. 크기가 없는 파일은 비고, 오프셋은 `0t` 가 앞에 붙습니다. `-s` 를 주면 크기만 보이고 열 이름이 `SIZE` 로 바뀝니다.
- `NODE` 는 로컬 파일의 inode 번호이고 네트워크 파일에서는 `TCP` 같은 프로토콜 이름입니다.
- `NAME` 은 파일 이름이나 네트워크 주소이고, TCP 면 끝의 괄호에 연결 상태가 붙습니다.

| FD 값 | 뜻 |
|------|-----|
| `cwd` | 현재 작업 디렉터리 |
| `rtd` | 루트 디렉터리 |
| `txt` | 프로그램 텍스트(실행 파일) |
| `mem` | 메모리에 매핑한 파일(공유 라이브러리 등) |
| `3w` | 파일 디스크립터 3번을 쓰기(`w`)로 열었다 |

`cwd`·`rtd`·`txt`·`mem` 은 프로세스가 `open` 으로 연 파일이 아니라 커널이 프로세스에 붙인 참조입니다. 위 출력에서 `holder.py` 가 직접 연 파일은 숫자로 시작하는 `3w`·`4w`·`5w` 세 줄입니다. 파이프 `1w`·`2w` 는 셸이 물려준 표준 출력과 오류입니다.

전체 출력에서 `TYPE` 열만 세면 이 환경에 어떤 종류의 파일이 열려 있는지 한눈에 보입니다. 옵션 없이 전부 볼 때는 스레드마다 줄이 더 나와 열 위치가 바뀌므로 `-K i` 로 스레드를 무시합니다.

```bash
# -K i: 스레드(task)를 무시한다. TYPE 은 5번째 열이라 awk 로 뽑아 종류별로 센다
lsof -K i | awk 'NR>1{print $5}' | sort | uniq -c
```

```bash
     16 CHR
     32 DIR
     29 FIFO
      5 IPv4
    114 REG
      1 a_inode
      1 unix
```

`a_inode` 는 man 의 TYPE 목록에 없는 값입니다. inotify 처럼 inode 가 없는 디스크립터입니다. `/proc/PID/fd` 에서는 `anon_inode:inotify` 로 보입니다.[^procfd]

```bash
# -c (command): 이름이 이 글자로 시작하는 프로세스. COMMAND 열은 아홉 글자에서 잘린다
lsof -c long-running -a -d cwd
```

```bash
COMMAND    PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
long-runn 3158 root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
```

```bash
# +c 0: COMMAND 열을 자르지 않는다. 0 대신 숫자 w 를 주면 w 글자까지
lsof +c 0 -c long-running -a -d cwd
```

```bash
COMMAND          PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
long-running-wo 3158 root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
```

`+c 0` 으로 봐도 이 환경에서는 15글자에서 끊깁니다. man 은 이 열이 UNIX 판이 lsof 에 넘기는 글자 수까지만 담는다고 적습니다.[^c]

```bash
# -R (PPID): 부모 프로세스 번호를 PPID 열로 붙인다
lsof -R -a -d cwd -p $(pgrep -f holder.py)
```

```bash
COMMAND  PID PPID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3153    1 root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
```

`http.server` 는 연결마다 스레드를 하나 만듭니다. `-K` 는 스레드도 한 줄씩 보이며 `TID` 와 `TASKCMD` 열이 생깁니다. `TID` 가 빈 줄이 프로세스 자신이고 값이 있는 줄이 스레드입니다.[^K]

```bash
# -K (task): 프로세스의 스레드까지 보인다. 열에 TID 와 TASKCMD 가 붙는다
lsof -K -a -d cwd -p $(pgrep -f 'http.server 8080')
```

```bash
COMMAND  PID  TID TASKCMD USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3154              root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
python3 3154 3164 python3 root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
```



## 2. 프로세스가 연 파일 보기

> 아는 것이 PID·명령 이름·사용자 중 하나일 때, 그것으로 출발해 열린 파일을 골라 냅니다. 조건을 둘 이상 주면 기본이 OR 라는 점이 가장 흔한 함정입니다.

아는 것이 PID 면 `-p`, 명령 이름이면 `-c`, 사용자면 `-u` 로 출발합니다.

```bash
# -p (PID): 번호로 고른다. 쉼표로 여러 개를 줄 수 있다(공백 없이)
lsof -p $(pgrep -f holder.py),$(pgrep -x tail) -a -d 3
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3153 root    3w   REG   0,61        6 4353537 /root/cmd-lab/lsof/logs/app.log
tail    3157 root    3r   REG   0,86 20971520       3 /dev/shm/lsof-lab/big.log
```

`-p` 에 `^` 를 붙이면 그 PID 를 뺍니다. 아래는 모든 프로세스의 작업 디렉터리 줄에서 PID 1 을 뺀 것이고 앞 세 줄만 봅니다.[^p]

```bash
# -p ^PID: 그 PID 를 제외한다
lsof -d cwd -p ^1 | head -3
```

```bash
COMMAND    PID    USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3   3153    root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
python3   3154    root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
```

```bash
# -c (command): 명령 이름이 이 글자로 시작하는 프로세스. nc 가 둘 떠 있어 둘 다 나온다
lsof -c nc -a -d cwd
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
nc      3155 root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
nc      3156 root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
```

```bash
# -c /정규식/: 앞뒤를 슬래시로 감싸면 정규식. 끝 슬래시 뒤에 i(대소문자 무시)·b(기본 정규식)를 붙인다
lsof -c '/^py/' -a -d cwd
```

```bash
COMMAND  PID    USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3153    root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
python3 3154    root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
python3 3161 appuser  cwd    DIR   0,61       54 4353531 /home/appuser
python3 3162    root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
```

```bash
# -u (user): 사용자 이름이나 UID. 이름이 appuser 인 프로세스의 줄을 명령별로 센다
lsof -u appuser | awk 'NR>1{print $1,$3}' | sort | uniq -c    #      21 python3 appuser
```

```bash
# -u ^사용자: 그 사용자를 뺀다. root 가 아닌 프로세스만 남는다
lsof -u ^root | awk 'NR>1{print $1,$3}' | sort | uniq -c    #      21 python3 appuser
```

```bash
# -l: USER 열에 이름 대신 UID 숫자를 찍는다 (이름 조회가 느릴 때도 쓴다)
lsof -l -a -u appuser -d cwd
```

```bash
COMMAND  PID     USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3161     1000  cwd    DIR   0,61       54 4353531 /home/appuser
```

### 여러 조건을 줄 때의 OR 와 AND

man 은 조건을 지정하면 기본으로 그 조건들을 OR 로 묶는다고 적습니다. 그래서 `-u appuser -i` 는 "appuser 의 파일 또는 모든 네트워크 파일"입니다. `-a` 를 붙여야 둘을 모두 만족하는 줄만 남습니다.[^sel]

```bash
# -u appuser -i: appuser 의 파일 OR 모든 네트워크 파일. root 의 nc 와 http.server 까지 섞여 나온다
lsof -u appuser -i | awk 'NR>1{print $1,$3}' | sort | uniq -c
```

```bash
      1 nc root
     21 python3 appuser
      3 python3 root
```

```bash
# -a (AND): 조건을 모두 만족하는 줄만. appuser 의 네트워크 파일 하나뿐이다
lsof -a -u appuser -i
```

```bash
COMMAND  PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3161 appuser    3u  IPv4 406324      0t0  TCP localhost:tproxy (LISTEN)
```

`-a` 는 위치와 상관없이 모든 조건에 걸립니다. 두 옵션 사이에 끼워 쌍으로 묶는 방식은 되지 않는다고 man 이 적습니다. 같은 종류의 값(`-u a,b`, `-c x -c y`)은 먼저 OR 로 묶인 뒤 `-a` 와 만납니다.[^sel]

`-p` 와 `-d` 도 같은 규칙입니다. `-a` 없이 쓰면 두 조건이 OR 가 되어 PID 와 무관한 프로세스의 파일 디스크립터까지 나옵니다.

```bash
# -p 와 -d 만 쓰면 OR: holder.py 의 모든 줄에 다른 프로세스의 0~2번까지 섞여 줄 수만 센다
lsof -p $(pgrep -f holder.py) -d 0-2 | wc -l    # 50
```

```bash
# -a 를 붙이면 holder.py 의 0~2번만
lsof -a -p $(pgrep -f holder.py) -d 0-2
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF   NODE NAME
python3 3153 root    0r   CHR    1,3      0t0      5 /dev/null
python3 3153 root    1w  FIFO   0,15      0t0 401170 pipe
python3 3153 root    2w  FIFO   0,15      0t0 401170 pipe
```

조건을 만족하는 줄이 하나도 없으면 출력이 비고 종료 코드가 1 입니다.

```bash
# appuser 가 연 nc 프로세스는 없다
lsof -a -u appuser -c nc; echo "exit $?"    # exit 1
```



## 3. 이 파일을 연 프로세스 찾기

> 파일이나 디렉터리 이름이 먼저일 때는 그 이름을 인자로 줍니다. `+d` 와 `+D` 는 디렉터리 아래를, `-d` 는 열린 파일의 FD 번호를 골라 냅니다.

```bash
# 파일 이름을 인자로: 그 파일을 열어 둔 프로세스. 3w 로 쓰기 모드로 열려 있다
lsof logs/app.log
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3153 root    3w   REG   0,61        6 4353537 logs/app.log
```

실행 파일을 주면 그 프로그램을 실행 중인 프로세스가 `txt` 로 나옵니다. 인자는 심볼릭 링크를 풀어 비교하므로 링크인 `/usr/bin/nc` 를 줘도 실제 파일 이름이 나옵니다.[^out]

```bash
# 실행 파일: txt 로 열린 줄이 그 프로그램을 돌리는 프로세스. /usr/bin/nc 는 nc.openbsd 를 가리키는 링크다
lsof /usr/bin/nc | awk '{print $1,$2,$4,$NF}'
```

```bash
COMMAND PID FD NAME
nc 3155 txt /usr/bin/nc.openbsd
nc 3156 txt /usr/bin/nc.openbsd
```

```bash
# +d (디렉터리): 그 디렉터리와 바로 아래 항목을 연 프로세스. 하위 디렉터리 안은 보지 않는다
lsof +d logs
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3153 root    3w   REG   0,61        6 4353537 logs/app.log
python3 3153 root    4w   REG   0,61        0 4353543 logs/app.conf
```

```bash
# +D (디렉터리): 끝까지 내려가며 찾는다. logs/old/app.log.1 까지 나온다
lsof +D logs
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3153 root    3w   REG   0,61        6 4353537 logs/app.log
python3 3153 root    4w   REG   0,61        0 4353543 logs/app.conf
python3 3153 root    5w   REG   0,61        0 4353544 logs/old/app.log.1
```

`+D` 는 디렉터리 트리를 훑으므로 큰 트리에서는 느립니다. 이 둘은 심볼릭 링크를 따라가지 않고 하위 마운트 지점도 건너뜁니다.[^dir]

```bash
# -d (FD 목록): 번호나 cwd·txt·mem 이름. 범위는 0-2 처럼. 3번 이상만 보려면 3-99
lsof -a -p $(pgrep -f holder.py) -d cwd,3-99
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3153 root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
python3 3153 root    3w   REG   0,61        6 4353537 /root/cmd-lab/lsof/logs/app.log
python3 3153 root    4w   REG   0,61        0 4353543 /root/cmd-lab/lsof/logs/app.conf
python3 3153 root    5w   REG   0,61        0 4353544 /root/cmd-lab/lsof/logs/old/app.log.1
```

```bash
# -d ^이름: 모두 ^ 로 시작하면 제외 목록. 라이브러리 줄(mem·txt)을 빼면 읽을 줄이 준다
lsof -a -p $(pgrep -f holder.py) -d '^mem,^txt'
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3153 root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
python3 3153 root  rtd    DIR   0,61       42 4348902 /
python3 3153 root    0r   CHR    1,3      0t0       5 /dev/null
python3 3153 root    1w  FIFO   0,15      0t0  401170 pipe
python3 3153 root    2w  FIFO   0,15      0t0  401170 pipe
python3 3153 root    3w   REG   0,61        6 4353537 /root/cmd-lab/lsof/logs/app.log
python3 3153 root    4w   REG   0,61        0 4353543 /root/cmd-lab/lsof/logs/app.conf
python3 3153 root    5w   REG   0,61        0 4353544 /root/cmd-lab/lsof/logs/old/app.log.1
```

`-d` 의 목록은 전부 포함이거나 전부 제외여야 하고 섞어 쓸 수 없습니다.[^fd]



## 4. 지운 파일이 붙든 공간 찾기

> 로그를 `rm` 했는데 디스크가 비지 않으면 어느 프로세스가 그 파일을 열어 둔 것입니다. `lsof +L1` 이 그런 파일을 찾고, `/proc/PID/fd` 로 비웁니다.

파일 이름(디렉터리 항목)을 지워도 어떤 프로세스가 그 파일을 열어 두었다면 파일 자체는 마지막 디스크립터가 닫힐 때까지 남습니다.[^unlink] 그래서 공간이 돌아오지 않습니다. `df` 는 파일시스템 단위의 사용량을 보고하고 `du` 는 디렉터리 아래 파일의 크기를 추정합니다. 두 값이 어긋나면 이 상황을 의심합니다.[^dfdu]

```bash
# 지우기 전: df 와 du 가 모두 20M 쪽이다(tmpfs 라 df 의 Used 가 파일 크기를 그대로 따른다)
df -h /dev/shm; du -sh /dev/shm/lsof-lab
```

```bash
Filesystem      Size  Used Avail Use% Mounted on
shm             4.0G   20M  3.9G   1% /dev/shm
20M	/dev/shm/lsof-lab
```

```bash
# +L1 은 지우기 전에는 아무것도 찾지 못한다(이 경우 종료 코드는 0)
lsof +L1; echo "exit $?"    # exit 0
```

```bash
# 파일을 지운다. tail -f 가 아직 열고 있다
rm /dev/shm/lsof-lab/big.log
```

```bash
# df 는 그대로 20M, du 는 파일이 사라진 만큼 줄었다
df -h /dev/shm; du -sh /dev/shm/lsof-lab
```

```bash
Filesystem      Size  Used Avail Use% Mounted on
shm             4.0G   20M  3.9G   1% /dev/shm
0	/dev/shm/lsof-lab
```

```bash
# +L1 (+L 에 숫자): 링크 수가 1 보다 작은 열린 파일, 곧 지워진 파일. NLINK 열이 붙는다
lsof +L1
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NLINK NODE NAME
tail    3157 root    3r   REG   0,86 20971520     0    3 /dev/shm/lsof-lab/big.log (deleted)
```

`+L` 은 숫자 없이도 쓰며, 그러면 링크 수를 모든 줄에 붙입니다. 지운 파일은 링크 수가 0 이므로 `+L1` 이 골라 냅니다. NAME 끝의 `(deleted)` 와 NLINK 의 0 이 표지입니다.[^l1]

같은 프로세스를 `/proc/PID/fd` 로도 봅니다. 그 디렉터리의 항목은 연 파일을 가리키는 심볼릭 링크이고 지워진 파일은 `(deleted)` 가 붙은 채 가리킵니다.[^procfd]

```bash
# /proc/PID/fd: 3번이 지워진 파일이다 (lsof 없이도 확인)
ls -l /proc/$(pgrep -x tail)/fd
```

```bash
total 0
lr-x------ 1 root root 64 Nov 11 13:12 0 -> /dev/null
l-wx------ 1 root root 64 Nov 11 13:12 1 -> /dev/null
l-wx------ 1 root root 64 Nov 11 13:12 2 -> /root/cmd-lab/lsof/tail.err
lr-x------ 1 root root 64 Nov 11 13:12 3 -> /dev/shm/lsof-lab/big.log (deleted)
lr-x------ 1 root root 64 Nov 11 13:12 4 -> anon_inode:inotify
```

공간을 돌려받으려면 그 프로세스를 재시작해 디스크립터를 닫는 것이 정석입니다. 재시작할 수 없는 프로세스는 `/proc/PID/fd/번호` 를 열어 내용만 비웁니다. 쓰기로 열면서 크기를 0 으로 만드는 리다이렉션 하나면 됩니다.

```bash
# 3번 디스크립터가 가리키는 파일을 0바이트로. 프로세스는 그대로 돈다
: > /proc/$(pgrep -x tail)/fd/3
```

```bash
# tail 이 파일이 줄어든 것을 알아차렸다 (tail 의 오류 출력을 prep 에서 tail.err 로 받아 두었다)
sleep 1; cat tail.err    # tail: /dev/shm/lsof-lab/big.log: file truncated
```

```bash
# 공간이 돌아왔다
df -h /dev/shm
```

```bash
Filesystem      Size  Used Avail Use% Mounted on
shm             4.0G     0  4.0G   0% /dev/shm
```

```bash
# 파일은 여전히 열려 있지만 SIZE 가 0 이다. 프로세스를 끝내면 이 줄도 사라진다
lsof +L1
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NLINK NODE NAME
tail    3157 root    3r   REG   0,86        0     0    3 /dev/shm/lsof-lab/big.log (deleted)
```



## 5. 포트와 연결 보기

> 포트에서 출발할 때는 `-i` 를 쓰고, 프로토콜·주소·상태로 좁힙니다. 소켓을 잡은 프로세스까지 한 번에 나옵니다.

`-i` 는 인터넷 주소와 맞는 파일을 고릅니다. 주소가 없으면 네트워크 파일 전부입니다. 형식은 `[46][프로토콜][@호스트][:포트]` 입니다. 호스트 앞의 `@` 와 포트 앞의 `:` 는 생략할 수 없습니다.[^net]

```bash
# -i: 네트워크 파일 전부. 이름 풀이가 켜져 있어 127.0.0.1 이 localhost 로, 8080 이 http-alt 로 보인다
lsof -i
```

```bash
COMMAND  PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3154    root    3u  IPv4 405452      0t0  TCP localhost:http-alt (LISTEN)
python3 3154    root    4u  IPv4 406330      0t0  TCP localhost:http-alt->localhost:48454 (ESTABLISHED)
nc      3155    root    3u  IPv4 408031      0t0  TCP *:9000 (LISTEN)
python3 3161 appuser    3u  IPv4 406324      0t0  TCP localhost:tproxy (LISTEN)
python3 3162    root    3u  IPv4 406329      0t0  TCP localhost:48454->localhost:http-alt (ESTABLISHED)
```

`localhost:http-alt` 처럼 읽기 쉬운 이름은 이름 조회를 거친 결과입니다. 조회가 느리면 `lsof` 자체가 느려지므로 `-n`(호스트 이름 풀이 끔)과 `-P`(포트 이름 풀이 끔)를 습관으로 씁니다.[^np]

```bash
# -n: 호스트 이름을 풀지 않는다 (127.0.0.1 로 나온다)
lsof -n -i :8080 | head -2
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3154 root    3u  IPv4 405452      0t0  TCP 127.0.0.1:http-alt (LISTEN)
```

```bash
# -P: 포트 이름을 풀지 않는다 (8080 으로 나온다)
lsof -P -i :8080 | head -2
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3154 root    3u  IPv4 405452      0t0  TCP localhost:8080 (LISTEN)
```

```bash
# -nP: 둘 다 끈다. 이 시트 이후의 예는 이 조합을 쓴다
lsof -nP -i :8080
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3154 root    3u  IPv4 405452      0t0  TCP 127.0.0.1:8080 (LISTEN)
python3 3154 root    4u  IPv4 406330      0t0  TCP 127.0.0.1:8080->127.0.0.1:48454 (ESTABLISHED)
python3 3162 root    3u  IPv4 406329      0t0  TCP 127.0.0.1:48454->127.0.0.1:8080 (ESTABLISHED)
```

`-i :8080` 은 그 포트를 듣는 소켓과 연결된 소켓을 모두 보입니다. 위 출력의 세 줄은 서버의 듣는 소켓(`LISTEN`)과 서버 쪽 연결, 클라이언트인 `conn.py` 의 연결입니다. `->` 의 왼쪽이 이 소켓의 로컬 주소이고 오른쪽이 상대입니다.

```bash
# -i TCP: 프로토콜로 좁힌다. UDP 도 같다
lsof -nP -i TCP
```

```bash
COMMAND  PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3154    root    3u  IPv4 405452      0t0  TCP 127.0.0.1:8080 (LISTEN)
python3 3154    root    4u  IPv4 406330      0t0  TCP 127.0.0.1:8080->127.0.0.1:48454 (ESTABLISHED)
nc      3155    root    3u  IPv4 408031      0t0  TCP *:9000 (LISTEN)
python3 3161 appuser    3u  IPv4 406324      0t0  TCP 127.0.0.1:8081 (LISTEN)
python3 3162    root    3u  IPv4 406329      0t0  TCP 127.0.0.1:48454->127.0.0.1:8080 (ESTABLISHED)
```

```bash
# -i UDP: 열린 UDP 소켓이 없으면 출력이 비고 종료 코드가 1 이다
lsof -nP -i UDP; echo "exit $?"    # exit 1
```

```bash
# -i 4TCP:8000-9000: IP 버전(4)·프로토콜(TCP)·포트 범위를 한 번에. 6 이면 IPv6 만 보며 이 환경에는 없다
lsof -nP -i 4TCP:8000-9000
```

```bash
COMMAND  PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3154    root    3u  IPv4 405452      0t0  TCP 127.0.0.1:8080 (LISTEN)
python3 3154    root    4u  IPv4 406330      0t0  TCP 127.0.0.1:8080->127.0.0.1:48454 (ESTABLISHED)
nc      3155    root    3u  IPv4 408031      0t0  TCP *:9000 (LISTEN)
python3 3161 appuser    3u  IPv4 406324      0t0  TCP 127.0.0.1:8081 (LISTEN)
python3 3162    root    3u  IPv4 406329      0t0  TCP 127.0.0.1:48454->127.0.0.1:8080 (ESTABLISHED)
```

```bash
# -i @주소: 그 주소에 묶인 소켓. 모든 주소에 묶인(*) nc 9000 은 빠진다
lsof -nP -i @127.0.0.1
```

```bash
COMMAND  PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3154    root    3u  IPv4 405452      0t0  TCP 127.0.0.1:8080 (LISTEN)
python3 3154    root    4u  IPv4 406330      0t0  TCP 127.0.0.1:8080->127.0.0.1:48454 (ESTABLISHED)
python3 3161 appuser    3u  IPv4 406324      0t0  TCP 127.0.0.1:8081 (LISTEN)
python3 3162    root    3u  IPv4 406329      0t0  TCP 127.0.0.1:48454->127.0.0.1:8080 (ESTABLISHED)
```

```bash
# -i TCP@주소:포트: 프로토콜·주소·포트를 한 번에
lsof -nP -i TCP@127.0.0.1:8081
```

```bash
COMMAND  PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3161 appuser    3u  IPv4 406324      0t0  TCP 127.0.0.1:8081 (LISTEN)
```

### 상태로 좁히기

`-s` 에 `프로토콜:상태` 를 주면 그 상태의 소켓만 남깁니다. 상태 앞에 `^` 를 붙이면 그 상태를 뺍니다.[^state]

```bash
# -s TCP:LISTEN: 듣는 소켓만. 어느 프로세스가 포트를 쥐고 있는지 볼 때
lsof -nP -i TCP -sTCP:LISTEN
```

```bash
COMMAND  PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3154    root    3u  IPv4 405452      0t0  TCP 127.0.0.1:8080 (LISTEN)
nc      3155    root    3u  IPv4 408031      0t0  TCP *:9000 (LISTEN)
python3 3161 appuser    3u  IPv4 406324      0t0  TCP 127.0.0.1:8081 (LISTEN)
```

```bash
# -s TCP:^LISTEN: LISTEN 이 아닌 것. 이미 맺은 연결만 남는다
lsof -nP -i TCP -sTCP:^LISTEN
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3154 root    4u  IPv4 406330      0t0  TCP 127.0.0.1:8080->127.0.0.1:48454 (ESTABLISHED)
python3 3162 root    3u  IPv4 406329      0t0  TCP 127.0.0.1:48454->127.0.0.1:8080 (ESTABLISHED)
```

### 유닉스 소켓

```bash
# -U: 유닉스 도메인 소켓. NAME 에 소켓 파일 경로와 종류가 나온다
lsof -U
```

```bash
COMMAND  PID USER   FD   TYPE             DEVICE SIZE/OFF   NODE NAME
nc      3156 root    3u  unix 0x0000000000000000      0t0 406316 /root/cmd-lab/lsof/app.sock type=STREAM (LISTEN)
```

`DEVICE` 의 `0x0000000000000000` 은 이 환경에서 커널 주소가 가려져 0 으로 찍힌 값입니다.



## 6. 스크립트에 넘길 출력 만들기

> `-t` 는 PID 만, `-F` 는 필드를 한 줄씩 찍어 파이프라인에 바로 연결합니다. `-r` 은 같은 조회를 되풀이합니다.

스크립트에는 헤더와 열 간격에 기대지 않는 출력이 필요합니다. 포트를 쥔 프로세스를 찾아 바로 다른 명령에 넘기는 일이 대표적입니다.

```bash
# -t (terse): 헤더 없이 PID 만. 같은 프로세스가 여러 줄이어도 한 번만 나온다
lsof -t -i :8081    # 3161
```

`-t` 는 `-w`(경고 억제)를 함께 켭니다. 아래처럼 PID 를 다른 명령에 바로 넘깁니다.[^t]

```bash
# 끝내기 전에 8081 을 쥔 줄이 있는지 센다. 2 는 헤더 한 줄과 소켓 한 줄이다
lsof -nP -i :8081 | wc -l    # 2
```

```bash
# kill $(lsof -t ...): 포트를 쥔 프로세스에 TERM. Terminated 는 8081 서버를 감싼 서브셸이 찍는다(대화형 셸은 잡 알림 줄이 더 나온다)
kill $(lsof -t -i :8081); sleep 0.5    # Terminated
```

```bash
# 끝났는지 다시 확인. 일치하는 줄이 없으면 종료 코드 1
lsof -nP -i :8081; echo "exit $?"    # exit 1
```

대상이 없을 때 `kill $(lsof -t …)` 는 인자 없이 `kill` 이 돌아 오류가 납니다. 스크립트에서는 `lsof -t … | xargs -r kill` 로 인자가 없으면 건너뜁니다. 이 시트의 `-t` 예는 man 의 예(`lsof -t /lib/*/libssl.so.* | xargs -r kill -HUP`)와 같은 꼴입니다.[^t]

```bash
# -F (필드 출력): 문자마다 필드 하나. p=PID c=명령 f=FD n=이름. 한 필드가 한 줄이다
lsof -F pcfn -i :8080
```

```bash
p3154
cpython3
f3
nlocalhost:http-alt
f4
nlocalhost:http-alt->localhost:48454
p3162
cpython3
f3
nlocalhost:48454->localhost:http-alt
```

`p` 로 시작하는 줄이 프로세스 하나의 시작이고 그 아래 `f`·`n` 줄이 그 프로세스가 연 파일입니다. 열 간격이 바뀌어도 깨지지 않으므로 `awk` 로 열 번호를 세는 것보다 안전합니다. `-F 0`(문자 `0` 만)은 모든 필드를 NUL 로 끝내 찍으며 공백이 든 파일 이름도 구분합니다.[^f]

```bash
# -r (초): 1초 간격으로 되풀이. c 뒤 숫자는 반복 횟수(여기서는 2번). 숫자가 없으면 Ctrl-C 까지 계속
lsof -nP -r 1c2 -i :9000
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
nc      3155 root    3u  IPv4 408031      0t0  TCP *:9000 (LISTEN)
=======
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
nc      3155 root    3u  IPv4 408031      0t0  TCP *:9000 (LISTEN)
=======
```

`-r` 은 목록 사이에 `=======` 줄을 찍습니다. `+r` 은 목록이 비는 순간 스스로 끝납니다. 포트를 쥔 프로세스가 사라질 때까지 기다리는 용도입니다.[^r]

```bash
# +r: 대상이 사라지면 끝낸다. 1.5초 뒤 9100 을 듣는 nc 를 죽여 본다
nc -4 -l 9100 & sleep 0.5; (sleep 1.5; kill $(lsof -t -i :9100)) & lsof -nP +r 1 -i :9100; echo "exit $?"
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
nc      3280 root    3u  IPv4 410918      0t0  TCP *:9100 (LISTEN)
=======
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
nc      3280 root    3u  IPv4 410918      0t0  TCP *:9100 (LISTEN)
=======
exit 0
```



## 7. 컨테이너 안에서 보이는 범위

> 컨테이너 안의 `lsof` 는 그 컨테이너의 PID 이름공간 안에서만 보입니다. 다른 사용자의 프로세스를 읽으려면 권한도 필요합니다.

PID 이름공간은 프로세스 번호 공간을 나눕니다. `lsof` 는 `/proc` 을 읽습니다. `/proc` 은 마운트한 프로세스의 이름공간에서 보이는 프로세스만 담습니다. 그래서 컨테이너 안에서는 호스트나 다른 컨테이너의 프로세스가 보이지 않습니다.[^pidns]

다른 사용자의 프로세스는 `/proc/PID/fd` 의 링크를 읽는 데 ptrace 접근 권한이 필요합니다.[^procfd] 컨테이너는 기본으로 `CAP_SYS_PTRACE` 가 없습니다.[^cap] 이 시트의 준비 블록이 `--cap-add SYS_PTRACE` 를 쓰는 이유입니다. 권한을 주지 않은 컨테이너에서 같은 조회를 하면 `appuser` 의 줄이 이렇게 나옵니다. 아래 출력은 `--cap-add` 없이 준비 블록을 실행한 컨테이너에서 받았습니다.

```bash
# --cap-add SYS_PTRACE 없이: 다른 사용자(appuser)의 프로세스는 이름 대신 오류가 NAME 에 찍힌다
lsof -a -u appuser -d cwd,3
```

```bash
COMMAND  PID    USER   FD      TYPE DEVICE SIZE/OFF NODE NAME
python3 3161 appuser  cwd   unknown                      /proc/3161/cwd (readlink: Permission denied)
python3 3161 appuser    3   unknown                      /proc/3161/fd/3 (readlink: Permission denied)
```



## 관련 문서

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [자원마다 창이 따로 나 있어 어느 창을 여느냐가 곧 진단이다](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md#lsof-의-두-방향) — `lsof` 로 포트에서 출발하는 법과 프로세스에서 출발하는 법의 원리
- [지워도 공간이 안 돌아오는 파일](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md#지워도-공간이-안-돌아오는-파일) — 지운 로그가 디스크를 붙드는 원리와 logrotate 와의 관계

소켓 쪽을 보는 다른 도구는 `ss` 입니다.



## 참고 자료

- lsof 4.95.0 의 `lsof -v`·`lsof -h` 출력 — Debian 12 컨테이너에서 2026-11-11 확인
- [lsof(8) — Debian bookworm](https://manpages.debian.org/bookworm/lsof/lsof.8.en.html)
- [proc(5) — Debian bookworm](https://manpages.debian.org/bookworm/manpages/proc.5.en.html)
- [unlink(2) — Debian bookworm](https://manpages.debian.org/bookworm/manpages-dev/unlink.2.en.html)
- [pid_namespaces(7) — Debian bookworm](https://manpages.debian.org/bookworm/manpages/pid_namespaces.7.en.html)
- [capabilities(7) — Debian bookworm](https://manpages.debian.org/bookworm/manpages/capabilities.7.en.html)
- [df(1) — Debian bookworm](https://manpages.debian.org/bookworm/coreutils/df.1.en.html), [du(1) — Debian bookworm](https://manpages.debian.org/bookworm/coreutils/du.1.en.html)

[^out]: `man lsof` (lsof 4.95.0) OUTPUT — "COMMAND contains the first nine characters of the name of the UNIX command associated with the process.", "FD is the File Descriptor number of the file or: cwd current working directory; ... mem memory-mapped file; ... rtd root directory; ... txt program text (code and data)", "r for read access; w for write access; u for read and write access", "TYPE is the type of the node associated with the file", "IPv4 for an IPv4 socket", "DIR for a directory", "FIFO for a FIFO special file", "REG for a regular file", "unix for a UNIX domain socket", "DEVICE contains the device numbers, separated by commas, for a character special, block special, regular, directory or NFS file; ... or a kernel reference address that identifies the file", "SIZE/OFF ... the offset is normally displayed in decimal with a leading 0t if it contains 8 digits or less", "If the -s option is specified, lsof always displays the file size ... and labels the column SIZE.", "NODE is the node number of a local file; ... or the Internet protocol type - e.g, TCP", "or the name of a file specified in the names option (after any symbolic links have been resolved)". https://manpages.debian.org/bookworm/lsof/lsof.8.en.html
[^procfd]: `man 5 proc` 의 /proc/pid/fd/ 항목 (Linux man-pages 6.03) — "For file descriptors that have no corresponding inode (e.g., file descriptors produced by bpf(2), epoll_create(2), eventfd(2), inotify_init(2), ...), the entry will be a symbolic link with contents of the form anon_inode:file-type", "Permission to dereference or read (readlink(2)) the symbolic links in this directory is governed by a ptrace access mode PTRACE_MODE_READ_FSCREDS check; see ptrace(2)." https://manpages.debian.org/bookworm/manpages/proc.5.en.html
[^K]: `man lsof` OPTIONS — `-K k` "selects the listing of tasks (threads) of processes, on dialects where task (thread) reporting is supported.", "If -K is followed by a value, k, it must be i. That causes lsof to ignore tasks, particularly in the default, list-everything case when no other options are specified."; OUTPUT "TID is the task (thread) IDentification number", "A blank TID column in Linux indicates a process - i.e., a non-task.", "TASKCMD is the task command name."
[^c]: `man lsof` OPTIONS — `-c c` "selects the listing of files for processes executing the command that begins with the characters of c.", `+c w` "defines the maximum number of initial characters of the name, supplied by the UNIX dialect, of the UNIX command associated with a process to be printed in the COMMAND column. (The lsof default is nine.)"; OUTPUT "If a non-zero w value is specified to the +c w option, the column contains the first w characters of the name of the UNIX command associated with the process up to the limit of characters supplied to lsof by the UNIX dialect.", "If a zero w value is specified to the +c w option, the column contains all the characters of the name of the UNIX command associated with the process." 15글자 한계는 이 환경에서 `+c 0` 출력으로 확인한 값입니다.
[^p]: `man lsof` OPTIONS — `-p s` "excludes or selects the listing of files for the processes whose optional process IDentification (PID) numbers are in the comma-separated set s - e.g., 123 or 123,^456. (There should be no spaces in the set.)", "PID numbers that begin with ^ (negation) represent exclusions."; `-u s` "selects the listing of files for the user whose login names or user ID numbers are in the comma-separated set s", `-l` "inhibits the conversion of user ID numbers to login names."
[^sel]: `man lsof` OPTIONS — "Normally, list options that are specifically stated are ORed - i.e., specifying the -i option without an address and the -ufoo option produces a listing of all network files OR files belonging to processes owned by user foo.", "The -a option may be used to AND the selections.", "Caution: the -a option causes all list selection options to be ANDed; it can't be used to cause ANDing of selected pairs of selection options by placing it between them, even though its placement there is acceptable. Wherever -a is placed, it causes the ANDing of all selection options.", "Items of the same selection set - command names, file descriptors, network addresses, process identifiers, user identifiers, zone names, security contexts - are joined in a single ORed set and applied before the result participates in ANDing."
[^dir]: `man lsof` OPTIONS — `+d s` "causes lsof to search for all open instances of directory s and the files and directories it contains at its top level. +d does NOT descend the directory tree, rooted at s.", `+D D` "causes lsof to search for all open instances of directory D and all the files and directories it contains to its complete depth.", "Processing of the +D option does not follow symbolic links within D unless the -x or -x l option is also specified. Nor does it search for open files on file system mount points on subdirectories of D unless the -x or -x f option is also specified.", "Further note: lsof may process this option slowly and require a large amount of dynamic memory to do it."
[^fd]: `man lsof` OPTIONS — `-d s` "specifies a list of file descriptors (FDs) to exclude from or include in the output listing. The file descriptors are specified in the comma-separated set s - e.g., cwd,1,3, ^6,^2.", "The list is an exclusion list if all entries of the set begin with ^. It is an inclusion list if no entry begins with ^. Mixed lists are not permitted.", "A file descriptor number range may be in the set as long as neither member is empty, both members are numbers, and the ending member is larger than the starting one - e.g., 0-7 or 3-10."
[^unlink]: `man 2 unlink` (Linux man-pages 6.03) — "If the name was the last link to a file but any processes still have the file open, the file will remain in existence until the last file descriptor referring to it is closed." https://manpages.debian.org/bookworm/manpages-dev/unlink.2.en.html
[^dfdu]: `man df` (coreutils 9.1) NAME — "df - report file system space usage"; `man du` NAME — "du - estimate file space usage". https://manpages.debian.org/bookworm/coreutils/df.1.en.html
[^l1]: `man lsof` OPTIONS — `+|-L [l]` "enables (+) or disables (-) the listing of file link counts, where they are available - e.g., they aren't available for sockets, or most FIFOs and pipes.", "When +L is followed by a number, only files having a link count less than that number will be listed. ... A specification of the form +L1 will select open files that have been unlinked."; OUTPUT "NLINK contains the file link count when +L has been specified".
[^net]: `man lsof` OPTIONS — `-i [i]` "selects the listing of files any of whose Internet address matches the address specified in i. If no address is specified, this option selects the listing of all Internet and x.25 (HP-UX) network files.", "[46][protocol][@hostname|hostaddr][:service|port]", "The @ character, leading the host specification, is always required; as is the :, leading the port specification.", "If -i4 or -i6 is specified with no following address, only files of the indicated IP version, IPv4 or IPv6, are displayed."; `-U` "selects the listing of UNIX domain socket files."
[^np]: `man lsof` OPTIONS — `-n` "inhibits the conversion of network numbers to host names for network files. Inhibiting conversion may make lsof run faster. It is also useful when host name lookup is not working properly.", `-P` "inhibits the conversion of port numbers to port names for network files. Inhibiting the conversion may make lsof run a little faster. It is also useful when port name lookup is not working properly."
[^state]: `man lsof` OPTIONS — `-s [p:s]` "the option causes open TCP and UDP files to be excluded if their state name(s) are in the list (s) preceded by a ^; or included if their name(s) are not preceded by a ^."
[^t]: `man lsof` OPTIONS — `-t` "produce terse output comprising only process identifiers (without a header), so that it is easy to use programmatically. e.g. # reload anything using old SSL lsof -t /lib/*/libssl.so.* | xargs -r kill -HUP", "The -t option implies the -w option."
[^f]: `man lsof` OPTIONS — `-F f` "specifies a character list, f, that selects the fields to be output for processing by another program, and the character that terminates each output field. ... The field terminator defaults to NL, but may be changed to NUL (000).", "When the field selection character list contains only a zero (0), all fields are selected (except the raw device field for compatibility reasons) and the NUL terminator character is used."; OUTPUT FOR OTHER PROGRAMS "A process set begins with a field whose identifier is p (for process IDentifier (PID))", field identifiers "c process command name", "f file descriptor", "n file name, comment, Internet address", "p process ID (always selected)".
[^r]: `man lsof` OPTIONS — `+|-r [t[c<N>][m<fmt>]]` "puts lsof in repeat mode. There lsof lists open files as selected by other options, delays t seconds (default fifteen), then repeats the listing", "If the prefix is a -, repeat mode is endless.", "`c<N>` is for specifying the limits of repeating; if the number of iterations reaches at <N>, Lsof stops itself.", "If the prefix is +, repeat mode will end the first cycle no open files are listed", "otherwise the default marker is ========". man 은 `=` 여덟 개로 적지만 이 환경의 4.95.0 이 실제로 찍는 줄은 일곱 개입니다.
[^pidns]: `man pid_namespaces` (Linux man-pages 6.03) — "PID namespaces isolate the process ID number space, meaning that processes in different PID namespaces can have the same PID.", "A /proc filesystem shows (in the /proc/pid directories) only processes visible in the PID namespace of the process that performed the mount, even if the /proc filesystem is viewed from processes in other namespaces." https://manpages.debian.org/bookworm/manpages/pid_namespaces.7.en.html
[^cap]: `man capabilities` (Linux man-pages 6.03) — `CAP_SYS_PTRACE` 항목 "Trace arbitrary processes using ptrace(2)". 컨테이너가 기본으로 이 capability 를 갖지 않는다는 것은 이 환경에서 `--cap-add` 없이 받은 출력으로 확인했습니다. https://manpages.debian.org/bookworm/manpages/capabilities.7.en.html
