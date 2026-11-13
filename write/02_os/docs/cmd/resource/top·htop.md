---
title: top·htop 참조 시트
tags: [linux, cheatsheet, top, htop, process, monitoring, cli, reference]
status: draft
source:
  - procps-ng 4.0.2 top(1) (Debian 12 `man top` 원문, manpages.debian.org bookworm)
  - procps-ng 4.0.2 ps(1) (Debian 12 `man ps` 원문)
related:
  - ../README.md
  - ./top·htop 대화형 키와 htop.md
updated: 2026-11-13
---

# top·htop 참조 시트

---

> 지금 이 순간의 부하와 프로세스를 갱신하며 보여 주는 `top` 을 배치 모드로 받아 읽는 법을 옵션별로 모았습니다.

## 개요

> `top` 은 지금 순간의 부하와 프로세스를 갱신하며 보이고, 배치 모드로 받으면 파이프와 파일로 읽을 수 있습니다.

`top` 은 procps 패키지의 외부 바이너리이고 이 시트는 Debian 12 컨테이너(procps-ng 4.0.2)로 실측했습니다. macOS 의 `top` 은 BSD 판이라 옵션이 다르고 이 시트의 출력과 열도 맞지 않습니다. 대화형 화면은 글로 옮길 수 없어서 출력은 모두 `top -b` 로 받았고, 스레드·명령줄 옵션과 대화형 키, `htop` 은 [top·htop 대화형 키와 htop 시트](./top·htop%20대화형%20키와%20htop.md)로 나눴습니다.



## 핵심 문법

> `top -b` 로 프레임을 찍고 `-p`·`-u`·`-o` 로 고르고 정렬합니다.

```bash
# 호출 형태. top --help 의 Usage 줄
top [options]

# 배치 모드로 프레임 하나를 찍는다 (배치 모드로 한 번 찍기)
top -b -n 1

# 프레임 수와 간격을 정하고 마지막 프레임만 남긴다 (배치 모드로 한 번 찍기)
top \
  -b \
  -d 초 \
  -n 횟수 \
  | awk "/^top -/{n++} n==횟수"

# 요약 영역과 프로세스 열의 메모리 단위를 바꾼다 (메모리 단위 바꾸기)
top \
  -b \
  -n 1 \
  -E 단위
top \
  -b \
  -n 1 \
  -e 단위

# 프로세스를 PID 나 사용자로 고른다 (특정 프로세스만 골라 보기)
top \
  -b \
  -n 1 \
  -p PID목록
top \
  -b \
  -n 1 \
  -u 사용자

# 정렬 열을 필드 이름으로 정한다 (정렬 열 정하기)
top \
  -b \
  -n 1 \
  -o 필드

# 프레임을 파일에 쌓는다 (프레임을 로그로 쌓기)
top \
  -b \
  -d 5 \
  -n 12 \
  > top.log
```

### 요약 영역 CPU 항목

> 요약 셋째 줄 `%Cpu(s)` 는 아래 여덟 항목의 비율이고 직전 갱신 이후의 값입니다.

뜻은 man 의 「SUMMARY Display」 를 옮긴 것입니다.[^sum]

```bash
#   us   niced 가 아닌 사용자 프로세스를 돌린 시간
#   sy   커널 프로세스를 돌린 시간
#   ni   niced 사용자 프로세스를 돌린 시간
#   id   커널 idle 핸들러에서 보낸 시간
#   wa   I/O 완료를 기다린 시간
#   hi   하드웨어 인터럽트를 처리한 시간
#   si   소프트웨어 인터럽트를 처리한 시간
#   st   하이퍼바이저에 빼앗긴 시간
```

### 프로세스 열

> 프로세스 목록의 기본 열 12개이고, 메모리 열 셋(`VIRT`·`RES`·`SHR`)은 서로 다른 것을 잽니다.

뜻은 man 의 「FIELDS / Columns」 를 옮긴 것입니다.[^fields]

```bash
#   PID    프로세스 고유 번호
#   USER   프로세스 소유자의 유효 사용자 이름
#   PR     스케줄링 우선순위. rt 이면 실시간 우선순위
#   NI     nice 값. 음수는 우선순위가 높고 양수는 낮다
#   VIRT   가상 메모리 크기(KiB). 코드·데이터·공유 라이브러리에 스왑 아웃된
#          페이지와 매핑만 하고 안 쓴 페이지를 더한 값
#   RES    상주 메모리 크기(KiB). VIRT 중 스왑되지 않고 지금 쓰는 물리 메모리
#   SHR    공유 메모리 크기(KiB). RES 중 다른 프로세스도 쓸 수 있는 부분
#   S      상태. D 대기 불가, I 유휴, R 실행, S 수면, T 정지, t 추적 정지, Z 좀비
#          R 은 man 의 말로 "실행할 준비가 된" 작업이라 CPU 에서 도는 작업과
#          실행 대기 큐에서 차례를 기다리는 작업이 모두 R 로 나온다
#   %CPU   마지막 화면 갱신 이후 경과한 CPU 시간 중 이 작업의 몫
#   %MEM   RES 를 물리 메모리로 나눈 비율
#   TIME+  이 작업이 시작 뒤 쓴 CPU 시간. 100분의 1초까지
#   COMMAND  명령 이름이나 명령줄
```



## 종료 코드

> `top` 은 인자 값이 틀리면 1 을 돌려주지만 모르는 옵션에는 메시지만 내고 0 으로 끝납니다.

`man top` 에는 종료 코드 절이 없어 뜻은 적지 않고 Debian 12 컨테이너에서 잰 값만 싣습니다.[^no-exit] `htop` 의 실측값은 [top·htop 대화형 키와 htop 시트](./top·htop%20대화형%20키와%20htop.md)의 「종료 코드」 에 있습니다.

```bash
# 0  프레임을 찍고 끝났을 때. 모르는 옵션을 줘도 0 이다
# 1  옵션에 잘못된 값을 줬을 때 (-n x, -d x)
# 매뉴얼에 종료 코드 절이 없어 값은 모두 실측이다

# 프레임 하나를 찍고 끝난다
#   -b   입력을 받지 않고 줄을 내보내는 배치 모드 (--batch-mode)
#   -n   프레임을 이 수만큼 찍고 끝낸다 (--iterations)
top -b -n 1 > /dev/null; echo $?    # 0

# top 은 모르는 옵션에 메시지를 내고도 0 으로 끝난다
# 2>&1 은 오류 메시지를 표준 출력에 합쳐 종료 코드와 함께 보인다
top --bad 2>&1; echo $?    # top: unrecognized option '--bad' / 0

# 옵션 인자가 잘못되면 메시지를 내고 1 로 끝난다
top -b -n x 2>&1; echo $?    # top: bad iterations argument 'x' / 1
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션과 만든 상태만 씁니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 프로세스가 모두 뜹니다.

`docker run -it --rm debian:12` 로 띄운 컨테이너나 OrbStack 의 Linux VM 에서 root 로 실행합니다. PID·시각·메모리·`%CPU`·`TIME+` 값은 실행마다 다르므로 이 시트의 값과 같지 않아도 됩니다.

```bash
# top·ps 는 procps, 화면은 htop, 아래 python 파일을 돌릴 python3 을 설치한다
apt-get update -qq >/dev/null 2>&1; \
apt-get install -y -qq procps htop python3-minimal >/dev/null 2>&1
mkdir -p ~/cmd-lab/top && cd ~/cmd-lab/top

# hog.py: 200MiB bytearray 를 만들어 실제로 쓴다
# 「프로세스 열 읽기」·「메모리 단위 바꾸기」·「VIRT 와 RES 가 갈리는 이유」 가 쓴다
cat > hog.py << 'EOF2'
import time
buf = bytearray(200 * 1024 * 1024)
time.sleep(700)
EOF2

# lazy.py: 같은 200MiB 를 mmap 으로 주소 공간에만 잡고 건드리지 않는다
# hog.py 와 같은 세 곳이 쓴다
cat > lazy.py << 'EOF2'
import mmap, time
m = mmap.mmap(-1, 200 * 1024 * 1024)
time.sleep(701)
EOF2

# threads.py: 스레드를 셋 더 만들어 모두 넷이다
# top·htop 대화형 키와 htop 시트의 「스레드와 명령줄까지 보기」 가 쓴다
cat > threads.py << 'EOF2'
import threading, time
for _ in range(3):
    threading.Thread(target=time.sleep, args=(702,)).start()
time.sleep(702)
EOF2

# python3 세 개를 백그라운드로 띄운다
# threads.py 의 긴 인자는 명령줄이 잘리는 예에 쓴다
python3 hog.py &
python3 lazy.py &
python3 threads.py \
  --name=payment-batch-worker \
  --queue=orders-2026-11-10 \
  --retry=3 \
  --timeout=30s &

# yes: CPU 를 계속 쓴다. 「프로세스 열 읽기」·「정렬 열 정하기」 가 쓴다
yes > /dev/null &

# sleep 703: nice 값이 5 다. 「프로세스 열 읽기」 가 쓴다
nice -n 5 sleep 703 &

# worker: sleep 을 복사해 이름만 바꾼 것이다. 예는 쓰지 않고 「실습 정리」 가 끈다
cp /bin/sleep worker
./worker 704 &

# sleep 705: appuser 소유다. 「특정 프로세스만 골라 보기」 가 쓴다
id appuser >/dev/null 2>&1 || useradd -m appuser
setpriv \
  --reuid=appuser \
  --regid=appuser \
  --init-groups \
  sleep 705 &

# 프로세스가 뜰 시간을 둔다
sleep 2
```

출력에서 PID 1 이 `bash` 로 보이는 것은 컨테이너의 첫 프로세스이기 때문입니다.

### 배치 모드로 한 번 찍기

> `top` 은 기본으로 화면을 계속 다시 그리지만 `-b` 를 주면 줄을 그대로 내보내서 파이프와 파일로 받을 수 있습니다.

`-n` 을 주지 않으면 `-b` 는 끝날 때까지 프레임을 계속 찍습니다.[^b]

```bash
# 프레임 1개를 찍고 끝낸다. 프레임은 한 번 갱신해 찍은 한 장이다
# 처음 다섯 줄이 요약 영역이고 빈 줄 뒤에 열 머리와 프로세스 목록이 이어진다
#   head -12   앞 12줄만 낸다
top -b -n 1 | head -12
```

```bash
top - 13:06:46 up 1 day,  5:14,  0 user,  load average: 0.33, 0.26, 0.16
Tasks:  10 total,   2 running,   8 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,100.0 sy,  0.0 ni,  0.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st 
MiB Mem :   8004.2 total,   6401.1 free,   1215.9 used,    609.5 buff/cache     
MiB Swap:   9028.2 total,   9028.2 free,      0.0 used.   6788.3 avail Mem 

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3131 root      20   0    2240    956    832 R 100.0   0.0   0:02.21 yes
      1 root      20   0    3784   2768   2460 S   0.0   0.0   0:00.01 bash
   3128 root      20   0  217980 212176   4480 S   0.0   2.6   0:00.04 python3
   3129 root      20   0  218208   7440   4504 S   0.0   0.1   0:00.00 python3
   3130 root      20   0  234796   8456   4728 S   0.0   0.1   0:00.00 python3
```

```bash
# 프레임 3개가 나온다. 0.5초 간격이면 1초 남짓 걸린다
#   -d         프레임 사이 간격(초). 소수도 된다 (--delay)
#   grep -c    일치한 줄 수를 센다
top \
  -b \
  -d 0.5 \
  -n 3 \
  | grep -c "^top -"
# 3
```

둘째 프레임부터 쓰려면 프레임 시작 줄을 세어 고릅니다. 마지막 프레임만 뽑는 `awk` 는 이 시트에서 계속 씁니다.

```bash
# 프레임 시작 줄(top -)을 세어 둘째 프레임만 남긴다
# 첫 프레임의 CPU 줄은 믿을 수 없다 (「첫 프레임의 CPU 줄」)
top \
  -b \
  -d 1 \
  -n 2 \
  | awk "/^top -/{n++} n==2" \
  | head -5
```

```bash
top - 13:06:50 up 1 day,  5:14,  0 user,  load average: 0.39, 0.27, 0.16
Tasks:  11 total,   2 running,   9 sleeping,   0 stopped,   0 zombie
%Cpu(s):  3.6 us,  9.3 sy,  0.0 ni, 87.1 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st 
MiB Mem :   8004.2 total,   6367.4 free,   1221.8 used,    637.2 buff/cache     
MiB Swap:   9028.2 total,   9028.2 free,      0.0 used.   6782.4 avail Mem 
```

```bash
# 판을 확인한다
#   -V   버전을 찍고 끝낸다 (--version)
top -V    # top from procps-ng 4.0.2
```

### 머리 다섯 줄 읽기

> 요약 영역은 `uptime`·`free`·`vmstat` 가 따로 알려 주던 값을 한 번에 보입니다.

각 줄의 뜻은 man 의 「SUMMARY Display」 를 옮긴 것이고 CPU 항목은 「요약 영역 CPU 항목」 에 있습니다.[^sum] 2행의 `-H` 는 [top·htop 대화형 키와 htop 시트](./top·htop%20대화형%20키와%20htop.md)의 「스레드와 명령줄까지 보기」 에서 다룹니다.

```bash
# 둘째 프레임의 머리 다섯 줄. 값은 실행마다 다르다
#   1행   현재 시각, 부팅 뒤 흐른 시간, 사용자 수, 최근 1·5·15분의 load average
#   2행   전체 작업 수와 running·sleeping·stopped·zombie 수. -H 면 Threads
#   3행   CPU 상태. 직전 갱신 이후의 비율
#   4행   물리 메모리 total·free·used·buff/cache
#   5행   스왑 total·free·used 와 avail Mem
top \
  -b \
  -d 1 \
  -n 2 \
  | awk "/^top -/{n++} n==2" \
  | head -5
```

```bash
top - 13:06:50 up 1 day,  5:14,  0 user,  load average: 0.39, 0.27, 0.16
Tasks:  11 total,   2 running,   9 sleeping,   0 stopped,   0 zombie
%Cpu(s):  3.6 us,  9.3 sy,  0.0 ni, 87.1 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st 
MiB Mem :   8004.2 total,   6367.4 free,   1221.8 used,    637.2 buff/cache     
MiB Swap:   9028.2 total,   9028.2 free,      0.0 used.   6782.4 avail Mem 
```

`avail Mem` 은 스왑 없이 새 프로그램을 띄울 수 있는 물리 메모리의 추정이고, `free` 와 달리 되돌릴 수 있는 페이지 캐시와 slab 을 계산에 넣습니다.[^mem] `free` 열의 원리는 [자원마다 창이 따로 나 있다 노트의 「`free` 여섯 열의 출처」](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md#free-여섯-열의-출처)에, 화면의 네 구역은 같은 노트의 [「5. `top` 화면 구역과 배치 모드」](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md#5-top-화면-구역과-배치-모드)에 있습니다.

### 프로세스 열 읽기

> 고른 프로세스 넷의 PR·NI·S 열을 실제 값으로 읽습니다.

열의 뜻은 「프로세스 열」 에 있습니다.

```bash
# NI 5 로 띄운 sleep 은 PR 이 25 다. 기본 20 에 nice 값을 더한 모양이다
# S 가 R 인 것은 CPU 를 쓰는 yes 다. 나머지 둘은 메모리 두 프로그램이다
#   -p         PID 로 고른다. 쉼표로 여러 개를 줄 수 있고 -p 를 여러 번 써도 된다 (--pid)
#   tail -n +7   7번째 줄부터 낸다. 요약 영역과 빈 줄을 빼고 열 머리부터 보인다
top \
  -b \
  -n 1 \
  -p $(pgrep -x yes),$(pgrep -f "sleep 703"),$(pgrep -f hog.py),$(pgrep -f lazy.py) \
  | tail -n +7
```

```bash
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3131 root      20   0    2240    956    832 R 100.0   0.0   0:07.49 yes
   3132 root      25   5    2240   1116   1020 S   0.0   0.0   0:00.00 sleep
   3128 root      20   0  217980 212176   4480 S   0.0   2.6   0:00.04 python3
   3129 root      20   0  218208   7440   4504 S   0.0   0.1   0:00.00 python3
```

### 메모리 단위 바꾸기

> 메모리 값이 너무 크거나 작아 읽기 어려울 때 표시 단위를 바꿉니다.

요약 영역 메모리 줄의 단위는 기본이 MiB 이고 `-E` 가 바꿉니다.[^scale]

```bash
# 요약 영역 메모리가 GiB 로 나온다
#   -E   요약 영역 메모리 단위. k m g t p e (--scale-summary-mem)
#   sed -n 1,5p   1~5번째 줄만 낸다
top \
  -b \
  -n 1 \
  -E g \
  | sed -n 1,5p
```

```bash
top - 13:06:51 up 1 day,  5:14,  0 user,  load average: 0.39, 0.27, 0.16
Tasks:  10 total,   2 running,   8 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st 
GiB Mem :      7.8 total,      6.5 free,      0.9 used,      0.6 buff/cache     
GiB Swap:      8.8 total,      8.8 free,      0.0 used.      6.9 avail Mem 
```

```bash
# 요약 영역 메모리가 KiB 로 나온다
top \
  -b \
  -n 1 \
  -E k \
  | sed -n 4,5p
```

```bash
KiB Mem :  8196284 total,  6781004 free,   990348 used,   652504 buff/cache     
KiB Swap:  9244852 total,  9244852 free,        0 used.  7205936 avail Mem 
```

```bash
# 프로세스 열 메모리를 KiB 로 낸다. 기본 표시와 같다
#   -e   프로세스 열 메모리 단위. k m g t p (--scale-task-mem)
top \
  -b \
  -n 1 \
  -p $(pgrep -f hog.py),$(pgrep -f lazy.py) \
  -e k
```

```bash
top - 13:06:51 up 1 day,  5:14,  0 user,  load average: 0.44, 0.28, 0.17
Tasks:   2 total,   0 running,   2 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st 
MiB Mem :   8004.2 total,   6618.5 free,    970.6 used,    637.3 buff/cache     
MiB Swap:   9028.2 total,   9028.2 free,      0.0 used.   7033.6 avail Mem 

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3128 root      20   0  217980 212176   4480 S   0.0   2.6   0:00.04 python3
   3129 root      20   0  218208   7440   4504 S   0.0   0.1   0:00.00 python3
```

```bash
# 프로세스 메모리 열이 GiB 로 나오고 작은 값은 0.0g 로 뭉개진다
top \
  -b \
  -n 1 \
  -p $(pgrep -f hog.py),$(pgrep -f lazy.py) \
  -e g
```

```bash
top - 13:06:51 up 1 day,  5:14,  0 user,  load average: 0.44, 0.28, 0.17
Tasks:   2 total,   0 running,   2 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st 
MiB Mem :   8004.2 total,   6617.8 free,    970.6 used,    638.2 buff/cache     
MiB Swap:   9028.2 total,   9028.2 free,      0.0 used.   7033.6 avail Mem 

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3128 root      20   0    0.2g   0.2g   0.0g S   0.0   2.6   0:00.04 python3
   3129 root      20   0    0.2g   0.0g   0.0g S   0.0   0.1   0:00.00 python3
```

단위를 너무 크게 올리면 값이 뭉개져 `lazy.py` 의 `RES` 가 `0.0g` 로 보입니다.[^scale]

### 특정 프로세스만 골라 보기

> PID 나 사용자로 바로 골라 목록에서 눈으로 찾지 않습니다.

`-p`·`-u`·`-U` 는 한 번에 하나만 줄 수 있습니다.[^p]

```bash
# yes 한 개만 남는다. -p 로 고르면 Tasks 줄도 고른 수(1)로 나온다
top \
  -b \
  -n 1 \
  -p $(pgrep -x yes)
```

```bash
top - 13:06:50 up 1 day,  5:14,  0 user,  load average: 0.39, 0.27, 0.16
Tasks:   1 total,   1 running,   0 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st 
MiB Mem :   8004.2 total,   6493.5 free,   1095.7 used,    637.2 buff/cache     
MiB Swap:   9028.2 total,   9028.2 free,      0.0 used.   6908.5 avail Mem 

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3131 root      20   0    2240    956    832 R 100.0   0.0   0:07.02 yes
```

`-p` 의 PID 0 은 `top` 자기 자신을 뜻합니다.[^p]

```bash
# top 자신의 한 줄만 남는다
#   tail -1   마지막 줄만 낸다
top \
  -b \
  -n 1 \
  -p 0 \
  | tail -1
```

```bash
   3186 root      20   0    8368   4536   2444 R   0.0   0.1   0:00.00 top
```

```bash
# appuser 가 유효 사용자인 프로세스만 남는다
# -p 와 달리 -u 는 Tasks 줄을 고른 수로 줄이지 않아 전체 작업 수가 그대로 나온다
#   -u   유효 사용자 이름이나 ID 가 맞는 프로세스만 (--filter-only-euser)
top \
  -b \
  -n 1 \
  -u appuser
```

```bash
top - 13:06:51 up 1 day,  5:14,  0 user,  load average: 0.44, 0.28, 0.17
Tasks:   9 total,   2 running,   7 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st 
MiB Mem :   8004.2 total,   6611.3 free,    972.2 used,    643.0 buff/cache     
MiB Swap:   9028.2 total,   9028.2 free,      0.0 used.   7032.0 avail Mem 

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3146 appuser   20   0    2240   1116   1020 S   0.0   0.0   0:00.00 sleep
```

```bash
# 같은 appuser 의 프로세스만 남는다
#   -U   실제·유효·저장·파일시스템 사용자 어느 것이든 맞으면 (--filter-any-user)
top \
  -b \
  -n 1 \
  -U appuser \
  | tail -n +7
```

```bash
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3146 appuser   20   0    2240   1116   1020 S   0.0   0.0   0:00.00 sleep
```

`-u` 는 유효 사용자만 보고 `-U` 는 네 종류 사용자 ID 를 모두 보며, 이 예에서는 `appuser` 가 모두 같아 결과가 같습니다.[^u]

```bash
# root 가 아닌 사용자의 프로세스만 남는다
#   -u !이름   그 사용자가 아닌 프로세스만 보인다
top \
  -b \
  -n 1 \
  -u "!root" \
  | tail -n +7
```

```bash
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3146 appuser   20   0    2240   1116   1020 S   0.0   0.0   0:00.00 sleep
```

```bash
# -u 와 -p 를 섞으면 오류 한 줄을 내고 끝난다
top \
  -b \
  -n 1 \
  -u appuser \
  -p 1
```

```bash
top: conflicting process selections (U/p/u)
```

```bash
# 마지막 프레임에서 CPU 를 쓴 yes 한 줄만 남기고 나머지를 감춘다
#   -i   마지막 갱신 뒤 CPU 를 쓰지 않은 프로세스를 감춘다 (--idle-toggle)
top \
  -b \
  -d 1 \
  -n 2 \
  -i \
  | awk "/^top -/{n++} n==2" \
  | tail -n +7
```

```bash
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3131 root      20   0    2240    956    832 R 100.0   0.0   0:11.37 yes
```

프로세스의 `%CPU` 는 요약의 `%Cpu(s)` 와 달리 첫 프레임에도 잡혀서 이 환경에서는 `-n 1` 로 찍어도 같은 한 줄이 남았습니다.[^i]

### 정렬 열 정하기

> 기본 정렬은 `%CPU` 이고, 배치 모드에서는 `-o` 로 열 이름을 정해 정렬합니다.

man 은 `-o` 가 "주로 자동화·스크립트 배치 모드를 위해" 있다고 적습니다.[^o]

```bash
# 필드 이름 앞 여덟 개가 한 줄에 하나씩 나온다
#   -O   필드 이름을 한 줄씩 보이고 끝낸다 (--list-fields)
top \
  -b \
  -n 1 \
  -O \
  | head -8
```

```bash
PID
PPID
UID
USER
RUID
RUSER
SUID
SUSER
```

```bash
# 메모리 비율 정렬. 이름만 쓰면 큰 값이 위에 온다
#   -o   정렬할 필드 이름. 앞에 + 를 붙이면 큰 값부터, - 를 붙이면 작은 값부터 (--sort-override)
top \
  -b \
  -n 1 \
  -o %MEM \
  | sed -n 7,10p
```

```bash
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3128 root      20   0  217980 212176   4480 S   0.0   2.6   0:00.04 python3
   3130 root      20   0  234796   8456   4728 S   0.0   0.1   0:00.00 python3
   3129 root      20   0  218208   7440   4504 S   0.0   0.1   0:00.00 python3
```

```bash
# %MEM 이 작은 프로세스가 위에 온다
top \
  -b \
  -n 1 \
  -o -%MEM \
  | sed -n 7,10p
```

```bash
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3131 root      20   0    2240    956    832 R 100.0   0.0   0:08.89 yes
   3132 root      25   5    2240   1116   1020 S   0.0   0.0   0:00.00 sleep
   3146 appuser   20   0    2240   1116   1020 S   0.0   0.0   0:00.00 sleep
```

```bash
# 이름만 쓴 것과 같이 %MEM 이 큰 프로세스가 위에 온다
top \
  -b \
  -n 1 \
  -o +%MEM \
  | sed -n 7,10p
```

```bash
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3128 root      20   0  217980 212176   4480 S   0.0   2.6   0:00.04 python3
   3130 root      20   0  234796   8456   4728 S   0.0   0.1   0:00.00 python3
   3129 root      20   0  218208   7440   4504 S   0.0   0.1   0:00.00 python3
```

```bash
# 둘째 프레임이 CPU 를 많이 쓰는 순서로 나온다
top \
  -b \
  -d 1 \
  -n 2 \
  -o %CPU \
  | awk "/^top -/{n++} n==2" \
  | sed -n 7,9p
```

```bash
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3131 root      20   0    2240    956    832 R 100.0   0.0   0:10.21 yes
      1 root      20   0    3784   2784   2460 S   0.0   0.0   0:00.02 bash
```

### 프레임을 로그로 쌓기

> 일정한 간격으로 프레임을 파일에 쌓아 두면 나중에 그 시간대의 부하를 되짚을 수 있습니다.

`top` 의 `%CPU` 는 "마지막 화면 갱신 이후"의 몫이라 지금 순간의 사용률에 가깝고, `ps` 의 `%CPU` 는 CPU 시간을 프로세스가 산 시간으로 나눈 평균입니다.[^pcpu] `top` 은 시간에 따른 프레임이고 `ps` 는 한 시점의 스냅숏입니다.

```bash
# 5초 간격으로 12프레임(1분)을 쌓는 관례. 여기서는 1초 간격 3프레임으로 같은 모양을 확인한다
# top -b -d 5 -n 12 > top.log
# 파일에는 프레임 3개가 이어져 있고 각 프레임은 top - 줄로 시작하므로 awk 로 쪼갤 수 있다
# 첫 프레임의 CPU 줄은 쓸모가 없으니 분석에서는 둘째부터 쓴다 (「첫 프레임의 CPU 줄」)
# 긴 수집은 nohup top -b -d 5 -n 12 > top.log & 처럼 백그라운드로 돌린다
#   grep -E   확장 정규식으로 찾는다
top \
  -b \
  -d 1 \
  -n 3 \
  > top.log; \
grep -c "^top -" top.log; \
grep -E "^(top -|%Cpu)" top.log
```

```bash
3
top - 13:06:56 up 1 day,  5:14,  0 user,  load average: 0.56, 0.31, 0.18
%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st 
top - 13:06:57 up 1 day,  5:14,  0 user,  load average: 0.56, 0.31, 0.18
%Cpu(s):  9.9 us, 13.8 sy,  0.0 ni, 73.3 id,  0.7 wa,  0.0 hi,  2.3 si,  0.0 st 
top - 13:06:58 up 1 day,  5:14,  0 user,  load average: 0.56, 0.31, 0.18
%Cpu(s):  5.2 us, 10.4 sy,  0.0 ni, 84.2 id,  0.0 wa,  0.0 hi,  0.3 si,  0.0 st 
```

```bash
# ps 의 %CPU 는 시작 이후의 평균. 열 선택과 정렬이 한 줄에 된다
# 열을 직접 고르고 정렬해 스크립트에 넘기려면 ps -eo 가 top 보다 단순하다
#   ps -e       모든 프로세스를 고른다
#   ps -o       출력할 열을 정한다
#   ps --sort   정렬 열. - 를 붙이면 큰 값부터
ps -eo pid,ni,pcpu,rss,comm --sort=-pcpu | head -3
```

```bash
    PID  NI %CPU   RSS COMMAND
   3131   0 99.9   956 yes
   3128   0  0.2 212176 python3
```

`ps` 옵션은 [ps 참조 시트](../process/ps.md)에 있습니다.

### 실습 정리

> 실습이 끝나면 아래 블록으로 띄운 프로세스를 정리합니다.

컨테이너를 나가면 모두 사라지므로 VM 에서 했을 때만 필요하고, 이어서 [top·htop 대화형 키와 htop 시트](./top·htop%20대화형%20키와%20htop.md)를 돌릴 때는 그 시트를 마친 뒤에 돌립니다. 출력은 `Killed` 알림뿐이라 싣지 않았습니다.

```bash
# 실습 준비가 띄운 프로세스를 이름으로 골라 끈다
#   pkill -9   SIGKILL 로 끈다
#   pkill -x   이름이 정확히 같은 것만 (--exact)
pkill -9 -x 'python3|yes|sleep|worker'
```



## 주의사항과 동작 원리

> 첫 프레임의 CPU 값은 기준이 없고, `VIRT` 는 쓰지 않은 매핑까지 셉니다.

### 첫 프레임의 CPU 줄

> 첫 프레임의 CPU 줄은 믿을 수 없습니다.

`%Cpu(s)` 는 직전 갱신 이후의 비율이라서 직전이 없는 첫 프레임은 기준이 없습니다.[^cpu] 첫 프레임 값은 실행마다 달라서 「배치 모드로 한 번 찍기」 의 첫 출력처럼 `100.0 sy` 로 나오기도 합니다.

```bash
# 1초 간격 두 프레임. 첫째는 기준 없는 값(여기서는 100.0 id), 둘째부터 실제 값이다
# yes 가 CPU 를 쓰는 중인데도 첫 프레임은 전부 놀고 있다고 나왔다
top \
  -b \
  -d 1 \
  -n 2 \
  | grep "^%Cpu"
```

```bash
%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st 
%Cpu(s):  3.7 us,  9.2 sy,  0.0 ni, 87.1 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st 
```

그래서 CPU 사용률이 필요하면 `-n 2` 이상으로 찍고 마지막 프레임을 씁니다.

### VIRT 와 RES 가 갈리는 이유

> 같은 200MiB 를 요청해도 `bytearray` 는 `RES` 로 올라오고 `mmap` 만 한 영역은 올라오지 않습니다.

아래는 `-e m` 으로 두 프로세스의 메모리 열을 MiB 로 본 것입니다.[^scale]

```bash
# 두 프로세스 모두 VIRT 가 약 213MiB 지만 RES 는 hog.py 가 207.2m, lazy.py 가 7.3m 다
# -p 를 두 번 준 꼴이다
top \
  -b \
  -n 1 \
  -p $(pgrep -f hog.py) \
  -p $(pgrep -f lazy.py) \
  -e m
```

```bash
top - 13:06:51 up 1 day,  5:14,  0 user,  load average: 0.44, 0.28, 0.17
Tasks:   2 total,   0 running,   2 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st 
MiB Mem :   8004.2 total,   6618.5 free,    970.6 used,    637.3 buff/cache     
MiB Swap:   9028.2 total,   9028.2 free,      0.0 used.   7033.6 avail Mem 

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3128 root      20   0  212.9m 207.2m   4.4m S   0.0   2.6   0:00.04 python3
   3129 root      20   0  213.1m   7.3m   4.4m S   0.0   0.1   0:00.00 python3
```

`bytearray` 는 만들 때 0 을 채워 모든 페이지를 쓰므로 물리 메모리에 올라옵니다. `mmap` 만 한 영역은 건드리기 전에는 물리 페이지가 붙지 않아서, `VIRT` 는 "매핑만 하고 안 쓴 페이지"까지 세고 `RES` 는 물리 메모리에 있는 것만 세므로 큰 `VIRT` 만으로는 메모리를 많이 쓴다고 말할 수 없습니다.[^fields]



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [top·htop 대화형 키와 htop 시트](./top·htop%20대화형%20키와%20htop.md) — 스레드·명령줄 옵션, 대화형 키, `htop`
- [ps 참조 시트](../process/ps.md) — 한 시점의 스냅숏으로 프로세스를 고르고 정렬하는 법
- [자원마다 창이 따로 나 있어 어느 창을 여느냐가 곧 진단이다](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md#5-top-화면-구역과-배치-모드) — `top` 화면 네 구역과 배치 모드
- [프로세스 메모리는 세그먼트와 페이지로 나뉜다](../../../book/tlpi_the-linux-programming-interface/06-02.%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EB%8A%94%20%EC%84%B8%EA%B7%B8%EB%A8%BC%ED%8A%B8%EC%99%80%20%ED%8E%98%EC%9D%B4%EC%A7%80%EB%A1%9C%20%EB%82%98%EB%89%9C%EB%8B%A4.md#참조의-지역성과-요구-페이징) — `VIRT` 와 `RES` 가 갈리는 원리



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- procps-ng 4.0.2 의 `man top` 원문 — Debian 12 컨테이너에서 2026-11-11 확인
- procps-ng 4.0.2 의 `top --help` 원문 — Debian 12 컨테이너에서 2026-11-13 확인
- [top(1) — Debian bookworm](https://manpages.debian.org/bookworm/procps/top.1.en.html)
- [ps(1) — Debian bookworm](https://manpages.debian.org/bookworm/procps/ps.1.en.html)

[^b]: `man top` (procps-ng 4.0.2) COMMAND-LINE Options — `-b, --batch` "Starts top in Batch mode, which could be useful for sending output from top to other programs or to a file. In this mode, top will not accept input and runs until the iterations limit you've set with the `-n' command-line option or until killed.", `-n, --iterations` "Specifies the maximum number of iterations, or frames, top should produce before ending." https://manpages.debian.org/bookworm/procps/top.1.en.html
[^cpu]: `man top` SUMMARY Display 2b — "Line 2 shows CPU state percentages based on the interval since the last refresh." 첫 프레임이 `100.0 id`·`100.0 sy`·`100.0 us` 처럼 실행마다 다르게 나오는 것은 이 환경에서 관찰한 값입니다. 직전 표본이 없어서라는 설명은 이 문장에서 추론한 것입니다.
[^sum]: `man top` SUMMARY Display — 2a "This portion consists of a single line containing:" 아래 줄마다 "program or window name, depending on display mode", "current time and length of time since last boot", "total number of users", "system load avg over the last 1, 5 and 15 minutes", 2b "Line 1 shows total tasks or threads, depending on the state of the Threads-mode toggle. That total is further classified as: running; sleeping; stopped; zombie", "us : time running un-niced user processes", "sy : time running kernel processes", "ni : time running niced user processes", "id : time spent in the kernel idle handler", "wa : time waiting for I/O completion", "hi : time spent servicing hardware interrupts", "si : time spent servicing software interrupts", "st : time stolen from this vm by the hypervisor".
[^mem]: `man top` SUMMARY Display 2c — "Line 1 reflects physical memory, classified as: total, free, used and buff/cache", "Line 2 reflects mostly virtual memory, classified as: total, free, used and avail (which is physical memory)", "The avail number on line 2 is an estimation of physical memory available for starting new applications, without swapping. Unlike the free field, it attempts to account for readily reclaimable page cache and memory slabs."
[^scale]: `man top` COMMAND-LINE Options — `-E, --scale-summary-mem = k | m | g | t | p | e` "Instructs top to force summary area memory to be scaled as: k - kibibytes m - mebibytes g - gibibytes t - tebibytes p - pebibytes e - exbibytes", `-e, --scale-task-mem = k | m | g | t | p` "Instructs top to force task area memory to be scaled as", 인터랙티브 `e` "Raising it too high, however, is likely to produce an all zero result".
[^fields]: `man top` FIELDS / Columns — VIRT -- Virtual Memory Size (KiB): "The total amount of virtual memory used by the task. It includes all code, data and shared libraries plus pages that have been swapped out and pages that have been mapped but not used.", RES -- Resident Memory Size (KiB): "A subset of the virtual address space (VIRT) representing the non-swapped physical memory a task is currently using.", SHR -- Shared Memory Size (KiB): "A subset of resident memory (RES) that may be used by other processes.", NI -- Nice Value: "A negative nice value means higher priority, whereas a positive nice value means lower priority.", PR -- Priority: "The scheduling priority of the task. If you see `rt' in this field, it means the task is running under real time scheduling priority.", %CPU -- CPU Usage: "The task's share of the elapsed CPU time since the last screen update, expressed as a percentage of total CPU time.", %MEM -- Memory Usage (RES): "A task's currently resident share of available physical memory.", S -- Process Status: 목록 D = uninterruptible sleep, I = idle, R = running, S = sleeping, T = stopped by job control signal, t = stopped by debugger during trace, Z = zombie(원문은 한 줄에 하나), "Tasks shown as running should be more properly thought of as ready to run -- their task_struct is simply represented on the Linux run-queue.", "Even without a true SMP machine, you may see numerous tasks in this state depending on top's delay interval and nice value.", TIME -- CPU Time: "Total CPU time the task has used since it started.", "TIME+ -- CPU Time, hundredths", USER -- User Name: "The effective user name of the task's owner."
[^p]: `man top` COMMAND-LINE Options — `-p, --pid = PIDLIST` "Monitor only processes with specified process IDs.", "This option can be given up to 20 times, or you can provide a comma delimited list with up to 20 pids. Co-mingling both approaches is permitted.", "A pid value of zero will be treated as the process id of the top program itself once it is running.", "The `p', `u' and `U' command-line options are mutually exclusive." 오류 문구 `top: conflicting process selections (U/p/u)` 와 `Tasks: 1 total` 은 이 환경에서 받은 출력입니다.
[^u]: `man top` COMMAND-LINE Options — `-U, --filter-any-user` "This option matches on any user (real, effective, saved, or filesystem).", `-u, --filter-only-euser` "This option matches on the effective user id only.", "Prepending an exclamation point (`!') to the user id or name instructs top to display only processes with users not matching the one provided."
[^i]: `man top` COMMAND-LINE Options — `-i, --idle-toggle` "Starts top with the last remembered `i' state reversed. When this toggle is Off, tasks that have not used any CPU since the last update will not be displayed." `top -b -n 1 -i` 도 `yes` 한 줄만 남기는 것은 이 환경에서 받은 출력입니다.
[^o]: `man top` COMMAND-LINE Options — `-O, --list-fields` "It will cause top to print each of the available field names on a separate line, then quit.", `-o, --sort-override = FIELDNAME` "You can prepend a `+' or `-' to the field name to also override the sort direction. A leading `+' will force sorting high to low, whereas a `-' will ensure a low to high ordering.", "This option exists primarily to support automated/scripted batch mode operation."
[^pcpu]: `man top` FIELDS %CPU -- CPU Usage: "The task's share of the elapsed CPU time since the last screen update"; `man ps` (procps-ng 4.0.2) STANDARD FORMAT SPECIFIERS `%cpu` "Currently, it is the CPU time used divided by the time the process has been running (cputime/realtime ratio), expressed as a percentage. It will not add up to 100% unless you are lucky." https://manpages.debian.org/bookworm/procps/ps.1.en.html
[^no-exit]: `man top` (procps-ng 4.0.2) 과 `man htop` (htop 3.2.2) 의 절 제목에는 종료 코드를 다루는 절이 없습니다. top 은 "NAME", "SYNOPSIS", "DESCRIPTION", "OVERVIEW" 와 "1. COMMAND-LINE Options" 부터 "9. BUGS", "10. SEE Also" 까지이고, htop 은 "NAME", "SYNOPSIS", "DESCRIPTION", "COMMAND-LINE OPTIONS", "INTERACTIVE COMMANDS", "COLUMNS", "EXTERNAL LIBRARIES", "CONFIG FILES", "MEMORY SIZES", "SEE ALSO", "SEE ALSO FOR PCP", "AUTHORS", "COPYRIGHT" 입니다. https://manpages.debian.org/bookworm/procps/top.1.en.html, https://manpages.debian.org/bookworm/htop/htop.1.en.html
