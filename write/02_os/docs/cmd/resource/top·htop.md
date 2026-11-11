---
title: top·htop 참조 시트
tags: [linux, cheatsheet, top, htop, process, monitoring, cli, reference]
status: draft
source:
  - procps-ng 4.0.2 top(1) (Debian 12 `man top` 원문, manpages.debian.org bookworm)
  - procps-ng 4.0.2 ps(1) (Debian 12 `man ps` 원문)
  - htop 3.2.2 htop(1) (Debian 12 `man htop`·`htop --help` 원문)
related:
  - ../README.md
updated: 2026-11-11
---

# top·htop 참조 시트

---

> 지금 이 순간의 부하와 프로세스를 갱신하며 보여 주는 `top` 을 배치 모드로 받아 읽는 법을 옵션별로 모으고, 같은 일을 하는 `htop` 의 실행 옵션과 키를 덧붙입니다.

## 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 프로세스가 모두 뜹니다.

macOS 의 `top` 은 BSD 판이라 옵션이 다르고 이 시트의 출력과 열도 맞지 않습니다. 이 시트는 Debian 12 의 procps-ng 4.0.2 `top` 과 htop 3.2.2 를 씁니다. OrbStack 의 Linux VM 이나 `docker run -it --rm debian:12` 안에서 root 로 실행합니다. 대화형 화면은 글로 옮길 수 없어서 출력은 모두 `top -b` 로 받은 것입니다. `top -b` 는 입력을 받지 않고 화면 대신 줄을 내보내는 배치 모드입니다.

```bash
apt-get update -qq >/dev/null 2>&1; apt-get install -y -qq procps htop python3-minimal >/dev/null 2>&1
mkdir -p ~/cmd-lab/top && cd ~/cmd-lab/top
cat > hog.py << 'EOF2'
import time
buf = bytearray(200 * 1024 * 1024)
time.sleep(700)
EOF2
cat > lazy.py << 'EOF2'
import mmap, time
m = mmap.mmap(-1, 200 * 1024 * 1024)
time.sleep(701)
EOF2
cat > threads.py << 'EOF2'
import threading, time
for _ in range(3):
    threading.Thread(target=time.sleep, args=(702,)).start()
time.sleep(702)
EOF2
python3 hog.py &
python3 lazy.py &
python3 threads.py --name=payment-batch-worker --queue=orders-2026-11-10 --retry=3 --timeout=30s &
yes > /dev/null &
nice -n 5 sleep 703 &
cp /bin/sleep worker
./worker 704 &
id appuser >/dev/null 2>&1 || useradd -m appuser
setpriv --reuid=appuser --regid=appuser --init-groups sleep 705 &
sleep 2
```

이 블록은 메모리와 CPU 를 서로 다르게 쓰는 프로세스를 띄웁니다. `hog.py` 는 200MiB `bytearray` 를 만들어 실제로 씁니다. `lazy.py` 는 같은 200MiB 를 `mmap` 으로 주소 공간에만 잡고 건드리지 않습니다.

`threads.py` 는 스레드를 셋 더 만들어 모두 넷이고 `yes` 는 CPU 를 계속 씁니다. `sleep 703` 은 nice 값이 5이고 `sleep 705` 는 `appuser` 소유입니다. `worker` 는 `sleep` 을 복사해 이름만 바꾼 것입니다.

PID·시각·메모리·`%CPU`·`TIME+` 값은 실행마다 다르므로 이 시트의 값과 같지 않아도 됩니다. 출력에서 PID 1 이 `bash` 로 보이는 것은 컨테이너의 첫 프로세스이기 때문입니다.



## 1. 배치 모드로 한 번 찍기

> `top` 은 기본으로 화면을 계속 다시 그리지만, `-b` 를 주면 줄을 그대로 내보내서 파이프와 파일로 받을 수 있습니다.

`-b` 는 입력을 받지 않고 `-n` 으로 정한 횟수나 종료될 때까지 돕니다.[^b] 한 번 갱신해 찍은 한 장을 프레임이라 부릅니다.

```bash
# -b (--batch): 화면 대신 줄로 내보낸다. -n (--iterations): 프레임 수만큼 찍고 끝낸다
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

처음 다섯 줄이 요약 영역이고 빈 줄 뒤에 열 머리와 프로세스 목록이 이어집니다. 읽는 법은 다음 절에서 다룹니다.

```bash
# -d (--delay): 프레임 사이 간격(초). 소수도 된다
# -n 3 이면 프레임이 3개. 0.5초 간격이면 1초 남짓 걸린다
top -b -d 0.5 -n 3 | grep -c "^top -"    # 3
```

첫 프레임의 CPU 줄은 믿을 수 없습니다. `%Cpu(s)` 는 직전 갱신 이후의 비율이라서 직전이 없는 첫 프레임은 기준이 없습니다.[^cpu] 아래 실행에서는 `yes` 가 CPU 를 쓰는 중인데도 첫 프레임이 전부 놀고 있다고 나왔고 둘째 프레임부터 사용률이 잡혔습니다. 첫 프레임 값은 실행마다 달라서 맨 위 출력처럼 `100.0 sy` 로 나오기도 합니다.

```bash
# -n 2 -d 1: 1초 간격 두 프레임. 첫째는 기준 없는 값(여기서는 100.0 id), 둘째부터 실제 값
top -b -d 1 -n 2 | grep "^%Cpu"
```

```bash
%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st 
%Cpu(s):  3.7 us,  9.2 sy,  0.0 ni, 87.1 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st 
```

그래서 CPU 사용률이 필요하면 `-n 2` 이상으로 찍고 마지막 프레임을 씁니다. 마지막 프레임만 뽑는 `awk` 는 이 시트에서 계속 씁니다.

```bash
# 프레임 시작 줄(top -)을 세어 둘째 프레임만 남긴다
top -b -d 1 -n 2 | awk "/^top -/{n++} n==2" | head -5
```

```bash
top - 13:06:50 up 1 day,  5:14,  0 user,  load average: 0.39, 0.27, 0.16
Tasks:  11 total,   2 running,   9 sleeping,   0 stopped,   0 zombie
%Cpu(s):  3.6 us,  9.3 sy,  0.0 ni, 87.1 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st 
MiB Mem :   8004.2 total,   6367.4 free,   1221.8 used,    637.2 buff/cache     
MiB Swap:   9028.2 total,   9028.2 free,      0.0 used.   6782.4 avail Mem 
```

```bash
# -V (--version): 판 확인
top -V    # top from procps-ng 4.0.2
```



## 2. 머리 다섯 줄 읽기

> 요약 영역은 `uptime`·`free`·`vmstat` 가 따로 알려 주던 값을 한 번에 보입니다. 각 항목의 뜻은 man 의 「SUMMARY Display」 항목에 있습니다.

위 둘째 프레임을 다시 봅니다. 값은 실행마다 다릅니다.

```bash
# 둘째 프레임의 머리 다섯 줄
top -b -d 1 -n 2 | awk "/^top -/{n++} n==2" | head -5
```

```bash
top - 13:06:50 up 1 day,  5:14,  0 user,  load average: 0.39, 0.27, 0.16
Tasks:  11 total,   2 running,   9 sleeping,   0 stopped,   0 zombie
%Cpu(s):  3.6 us,  9.3 sy,  0.0 ni, 87.1 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st 
MiB Mem :   8004.2 total,   6367.4 free,   1221.8 used,    637.2 buff/cache     
MiB Swap:   9028.2 total,   9028.2 free,      0.0 used.   6782.4 avail Mem 
```

첫 줄은 현재 시각, 부팅 뒤 흐른 시간, 사용자 수, 최근 1·5·15분의 load average 입니다.[^sum] 둘째 줄은 전체 작업 수와 그 안의 running·sleeping·stopped·zombie 수입니다. `-H` 를 주면 `Tasks` 가 `Threads` 로 바뀌어 스레드 수를 셉니다.

셋째 줄은 CPU 상태이며 직전 갱신 이후의 비율입니다.[^sum]

| 항목 | man 의 뜻 |
|------|-----------|
| `us` | niced 가 아닌 사용자 프로세스를 돌린 시간 |
| `sy` | 커널 프로세스를 돌린 시간 |
| `ni` | niced 사용자 프로세스를 돌린 시간 |
| `id` | 커널 idle 핸들러에서 보낸 시간 |
| `wa` | I/O 완료를 기다린 시간 |
| `hi` | 하드웨어 인터럽트를 처리한 시간 |
| `si` | 소프트웨어 인터럽트를 처리한 시간 |
| `st` | 하이퍼바이저에 빼앗긴 시간 |

넷째·다섯째 줄은 메모리입니다. 첫째 줄이 물리 메모리(`total`·`free`·`used`·`buff/cache`)이고 둘째 줄이 스왑입니다. 끝의 `avail Mem` 은 스왑 없이 새 프로그램을 띄울 수 있는 물리 메모리의 추정입니다. `free` 와 달리 되돌릴 수 있는 페이지 캐시와 slab 을 계산에 넣습니다.[^mem] `free` 열의 원리는 [자원마다 창이 따로 나 있다 노트의 「`free` 여섯 열의 출처」](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md#free-여섯-열의-출처)에, 화면의 네 구역은 같은 노트의 [「5. `top` 화면 구역과 배치 모드」](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md#5-top-화면-구역과-배치-모드)에 있습니다.

메모리 줄의 단위는 기본이 MiB 입니다. `-E` 가 요약 영역 단위를 바꿉니다.[^scale]

```bash
# -E (--scale-summary-mem): 요약 영역 메모리 단위. k m g t p e
top -b -n 1 -E g | sed -n 1,5p
```

```bash
top - 13:06:51 up 1 day,  5:14,  0 user,  load average: 0.39, 0.27, 0.16
Tasks:  10 total,   2 running,   8 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st 
GiB Mem :      7.8 total,      6.5 free,      0.9 used,      0.6 buff/cache     
GiB Swap:      8.8 total,      8.8 free,      0.0 used.      6.9 avail Mem 
```

```bash
# -E k: 킬로바이트(KiB)로
top -b -n 1 -E k | sed -n 4,5p
```

```bash
KiB Mem :  8196284 total,  6781004 free,   990348 used,   652504 buff/cache     
KiB Swap:  9244852 total,  9244852 free,        0 used.  7205936 avail Mem 
```



## 3. 열 읽기와 VIRT·RES 가 갈리는 때

> 프로세스 열은 PID 부터 COMMAND 까지 기본 열 12개이고, 메모리 열 셋은 서로 다른 것을 잽니다.

```bash
# nice 5 로 띄운 sleep(NI 5, PR 25), CPU 를 쓰는 yes(S 가 R), 메모리 두 프로그램
top -b -n 1 -p $(pgrep -x yes),$(pgrep -f "sleep 703"),$(pgrep -f hog.py),$(pgrep -f lazy.py) | tail -n +7
```

```bash
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3131 root      20   0    2240    956    832 R 100.0   0.0   0:07.49 yes
   3132 root      25   5    2240   1116   1020 S   0.0   0.0   0:00.00 sleep
   3128 root      20   0  217980 212176   4480 S   0.0   2.6   0:00.04 python3
   3129 root      20   0  218208   7440   4504 S   0.0   0.1   0:00.00 python3
```

열의 뜻은 man 의 「FIELDS / Columns」 항목을 옮긴 것입니다.[^fields]

| 열 | man 의 뜻 |
|----|-----------|
| `PID` | 프로세스 고유 번호 |
| `USER` | 프로세스 소유자의 유효 사용자 이름 |
| `PR` | 스케줄링 우선순위. `rt` 이면 실시간 우선순위 |
| `NI` | nice 값. 음수는 우선순위가 높고 양수는 낮다 |
| `VIRT` | 가상 메모리 크기(KiB). 코드·데이터·공유 라이브러리에 스왑 아웃된 페이지와 매핑만 하고 안 쓴 페이지를 더한 값 |
| `RES` | 상주 메모리 크기(KiB). VIRT 중 스왑되지 않고 지금 쓰는 물리 메모리 |
| `SHR` | 공유 메모리 크기(KiB). RES 중 다른 프로세스도 쓸 수 있는 부분 |
| `S` | 상태. D 대기 불가, I 유휴, R 실행, S 수면, T 정지, t 추적 정지, Z 좀비 |
| `%CPU` | 마지막 화면 갱신 이후 경과한 CPU 시간 중 이 작업의 몫 |
| `%MEM` | RES 를 물리 메모리로 나눈 비율 |
| `TIME+` | 이 작업이 시작 뒤 쓴 CPU 시간. 100분의 1초까지 |
| `COMMAND` | 명령 이름이나 명령줄 |

`S` 가 `R` 인 작업은 man 의 말로 "실행할 준비가 된" 작업입니다. 지금 CPU 에서 도는 작업과 실행 대기 큐에서 차례를 기다리는 작업이 모두 `R` 로 나옵니다.[^fields] 위에서 nice 5 로 띄운 `sleep` 은 `NI` 가 5, `PR` 이 25 입니다. nice 값 5 에 `PR` 이 25 로 나온 것은 기본 20 에 nice 값을 더한 모양입니다.

`hog.py` 와 `lazy.py` 는 둘 다 200MiB 를 요청했는데 `RES` 가 갈립니다. 단위를 MiB 로 바꾸는 `-e` 로 보면 한눈에 읽힙니다.[^scale]

```bash
# -e (--scale-task-mem): 프로세스 열 메모리 단위. k m g t p
top -b -n 1 -p $(pgrep -f hog.py) -p $(pgrep -f lazy.py) -e m
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

두 프로세스 모두 `VIRT` 가 약 213MiB 지만 `hog.py` 의 `RES` 는 약 207MiB 이고 `lazy.py` 는 약 7MiB 입니다.

`bytearray` 는 만들 때 0 을 채워 모든 페이지를 쓰므로 물리 메모리에 올라옵니다. `mmap` 만 한 영역은 주소 공간으로 약속만 됐을 뿐 건드리기 전에는 물리 페이지가 붙지 않습니다. `VIRT` 는 "매핑만 하고 안 쓴 페이지"까지 세고 `RES` 는 물리 메모리에 있는 것만 세므로, 큰 `VIRT` 만으로는 메모리를 많이 쓴다고 말할 수 없습니다.[^fields] 요청한 크기와 올라온 크기가 갈리는 원리는 [프로세스 메모리 노트의 「참조의 지역성과 요구 페이징」](../../../book/tlpi_the-linux-programming-interface/06-02.%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EB%8A%94%20%EC%84%B8%EA%B7%B8%EB%A8%BC%ED%8A%B8%EC%99%80%20%ED%8E%98%EC%9D%B4%EC%A7%80%EB%A1%9C%20%EB%82%98%EB%89%9C%EB%8B%A4.md#참조의-지역성과-요구-페이징)에 있습니다.

```bash
# -e k: 킬로바이트(기본 표시). 위와 같은 값을 KiB 로
top -b -n 1 -p $(pgrep -f hog.py),$(pgrep -f lazy.py) -e k
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
# -e g: 기가바이트. 자릿수가 모자라 0.0g 로 뭉개질 수 있다
top -b -n 1 -p $(pgrep -f hog.py),$(pgrep -f lazy.py) -e g
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

단위를 너무 크게 올리면 값이 뭉개져 `lazy.py` 의 `RES` 가 `0.0g` 로 보입니다.[^scale] 위 `-p` 는 PID 를 쉼표로 이어 한 번에 줘도 되고 `-p` 를 여러 번 써도 같습니다.



## 4. 특정 프로세스만 골라 보기

> 목록 전체에서 눈으로 찾지 않고 PID 나 사용자로 바로 고릅니다. 이 세 옵션은 서로 섞어 쓰지 못합니다.

```bash
# -p (--pid): PID 로 고른다. 쉼표로 여러 개를 줄 수 있고 -p 를 여러 번 써도 된다
top -b -n 1 -p $(pgrep -x yes)
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

`-p` 로 고르면 위처럼 `Tasks` 줄도 고른 수(1)로 나옵니다. PID 0 은 `top` 자기 자신을 뜻합니다.[^p]

```bash
# -p 0: top 자신의 프로세스
top -b -n 1 -p 0 | tail -1
```

```bash
   3186 root      20   0    8368   4536   2444 R   0.0   0.1   0:00.00 top
```

```bash
# -u (--filter-only-euser): 유효 사용자 이름이나 ID 가 맞는 프로세스만
top -b -n 1 -u appuser
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
# -U (--filter-any-user): 실제·유효·저장·파일시스템 사용자 어느 것이든 맞으면
top -b -n 1 -U appuser | tail -n +7
```

```bash
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3146 appuser   20   0    2240   1116   1020 S   0.0   0.0   0:00.00 sleep
```

`-u` 는 유효 사용자만 보고 `-U` 는 네 종류 사용자 ID 를 모두 봅니다. 이 예에서는 `appuser` 가 모두 같아 결과가 같습니다.[^u] `-p` 와 달리 `-u` 는 `Tasks` 줄을 고른 수로 줄이지 않아서 위 출력에도 전체 작업 수가 그대로 나옵니다. 이름 앞에 `!` 를 붙이면 맞지 않는 사용자만 보입니다.

```bash
# -u "!root": root 가 아닌 사용자의 프로세스만
top -b -n 1 -u "!root" | tail -n +7
```

```bash
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3146 appuser   20   0    2240   1116   1020 S   0.0   0.0   0:00.00 sleep
```

`-p`·`-u`·`-U` 는 한 번에 하나만 줄 수 있습니다.[^p]

```bash
# 섞어 쓰면 거부된다
top -b -n 1 -u appuser -p 1
```

```bash
top: conflicting process selections (U/p/u)
```

```bash
# -i (--idle-toggle): 마지막 갱신 뒤 CPU 를 쓰지 않은 프로세스를 감춘다
top -b -d 1 -n 2 -i | awk "/^top -/{n++} n==2" | tail -n +7
```

```bash
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3131 root      20   0    2240    956    832 R 100.0   0.0   0:11.37 yes
```

`-i` 는 마지막 프레임에서 CPU 를 쓴 `yes` 한 줄만 남기고 나머지를 감춥니다. 요약의 `%Cpu(s)` 와 달리 프로세스의 `%CPU` 는 첫 프레임에도 잡혀서 이 환경에서는 `-n 1` 로 찍어도 같은 한 줄이 남았습니다.[^i]



## 5. 정렬 열 정하기

> 기본 정렬은 `%CPU` 이고, 배치 모드에서는 `-o` 로 열 이름을 정해 정렬합니다.

```bash
# -O (--list-fields): -o 에 쓸 수 있는 필드 이름을 한 줄씩 보이고 끝낸다
top -b -n 1 -O | head -8
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

`-o` 는 필드 이름으로 정렬 열을 정합니다. man 은 이 옵션이 "주로 자동화·스크립트 배치 모드를 위해" 있다고 적습니다.[^o] 앞에 `+` 를 붙이면 큰 값부터, `-` 를 붙이면 작은 값부터입니다.

```bash
# -o %MEM: 메모리 비율 정렬. 이름만 쓰면 큰 값이 위에 온다
top -b -n 1 -o %MEM | sed -n 7,10p
```

```bash
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3128 root      20   0  217980 212176   4480 S   0.0   2.6   0:00.04 python3
   3130 root      20   0  234796   8456   4728 S   0.0   0.1   0:00.00 python3
   3129 root      20   0  218208   7440   4504 S   0.0   0.1   0:00.00 python3
```

```bash
# -o -%MEM: 앞에 - 를 붙이면 작은 값이 위에 온다
top -b -n 1 -o -%MEM | sed -n 7,10p
```

```bash
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3131 root      20   0    2240    956    832 R 100.0   0.0   0:08.89 yes
   3132 root      25   5    2240   1116   1020 S   0.0   0.0   0:00.00 sleep
   3146 appuser   20   0    2240   1116   1020 S   0.0   0.0   0:00.00 sleep
```

```bash
# -o +%MEM: + 는 큰 값부터 (이름만 쓴 것과 같은 결과)
top -b -n 1 -o +%MEM | sed -n 7,10p
```

```bash
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3128 root      20   0  217980 212176   4480 S   0.0   2.6   0:00.04 python3
   3130 root      20   0  234796   8456   4728 S   0.0   0.1   0:00.00 python3
   3129 root      20   0  218208   7440   4504 S   0.0   0.1   0:00.00 python3
```

```bash
# -o %CPU: 둘째 프레임에서 CPU 를 쓰는 순서
top -b -d 1 -n 2 -o %CPU | awk "/^top -/{n++} n==2" | sed -n 7,9p
```

```bash
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3131 root      20   0    2240    956    832 R 100.0   0.0   0:10.21 yes
      1 root      20   0    3784   2784   2460 S   0.0   0.0   0:00.02 bash
```



## 6. 스레드와 명령줄까지 보기

> 기본 화면은 프로세스 하나에 한 줄이고, 스레드는 `-H`, 명령줄 전체는 `-c`·`-w` 로 펼칩니다.

`threads.py` 를 돌리는 `python3` 은 스레드가 넷입니다. 기본으로는 스레드를 합친 한 줄만 나옵니다.[^h]

```bash
# (옵션 없음): 스레드를 합산한 프로세스 한 줄
top -b -n 1 -p $(pgrep -f threads.py) | tail -1
```

```bash
   3130 root      20   0  234796   8456   4728 S   0.0   0.1   0:00.00 python3
```

```bash
# -H (--threads-show): 스레드마다 한 줄. 요약 줄도 Tasks 에서 Threads 로 바뀐다
top -b -n 1 -H -p $(pgrep -f threads.py)
```

```bash
top - 13:06:55 up 1 day,  5:14,  0 user,  load average: 0.44, 0.28, 0.17
Threads:   4 total,   0 running,   4 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st 
MiB Mem :   8004.2 total,   6516.0 free,   1006.4 used,    704.2 buff/cache     
MiB Swap:   9028.2 total,   9028.2 free,      0.0 used.   6997.8 avail Mem 

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3130 root      20   0  234796   8456   4728 S   0.0   0.1   0:00.00 python3
   3137 root      20   0  234796   8456   4728 S   0.0   0.1   0:00.00 python3
   3138 root      20   0  234796   8456   4728 S   0.0   0.1   0:00.00 python3
   3139 root      20   0  234796   8456   4728 S   0.0   0.1   0:00.00 python3
```

요약의 `Threads: 4 total` 이 스레드 수입니다. 목록 첫 줄은 PID 와 같은 ID 를 가진 그룹 리더이고 나머지 셋이 그 프로세스에 속한 스레드의 ID 입니다.

`COMMAND` 열은 기본으로 프로그램 이름만 보입니다. `-c` 는 마지막으로 기억한 `c` 상태를 뒤집어 이름 대신 명령줄을 보이게 합니다.[^c] `-w` 가 없으면 배치 모드에서도 폭은 `top` 을 띄운 터미널을 따릅니다.[^w] 이 예처럼 출력을 파이프로 넘기면 80열에서 잘리고 끝에 `+` 가 붙습니다.

```bash
# -c (--cmdline-toggle): COMMAND 를 명령줄로 바꾼다. 폭 제한이 있어 + 로 잘린다
top -b -n 1 -c -p $(pgrep -f threads.py) | tail -1
```

```bash
   3130 root      20   0  234796   8456   4728 S   0.0   0.1   0:00.00 python3+
```

`-w` 는 폭을 정합니다. 배치 모드에서 인자 없이 쓰면 최대 512열까지 쓰고 인자가 있으면 그 폭으로 정합니다.[^w]

```bash
# -w 100 (--width): 폭을 100열로. 아직 모자라면 + 로 잘린다
top -b -n 1 -c -w 100 -p $(pgrep -f threads.py) | tail -1
```

```bash
   3130 root      20   0  234796   8456   4728 S   0.0   0.1   0:00.00 python3 threads.py --name=p+
```

```bash
# -w 200: 명령줄이 다 들어가면 잘리지 않는다. 마지막 줄의 바이트 수(줄바꿈 포함)
top -b -n 1 -c -w 200 -p $(pgrep -f threads.py) | tail -1 | wc -c    # 168
# -w (인자 없음): 배치 모드에서 최대 512열. 같은 줄이므로 바이트 수가 같다
top -b -n 1 -c -w -p $(pgrep -f threads.py) | tail -1 | wc -c    # 168
```

`-w` 에 인자를 안 주면 `COLUMNS=` 와 `LINES=` 환경 변수가 있을 때 그 값을 따릅니다.[^w]

```bash
# COLUMNS 가 있으면 인자 없는 -w 가 그 폭을 쓴다
COLUMNS=60 top -b -n 1 -w -p $(pgrep -f threads.py) | sed -n 7,8p
```

```bash
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU
   3130 root      20   0  234796   8456   4728 S   0.0
```



## 7. 대화형 키 목록

> 아래 키는 화면에서 누르는 것이라 출력을 실을 수 없습니다. 뜻은 man 의 「INTERACTIVE Commands」 항목을 옮겼습니다.[^keys]

정렬 키는 `%CPU`·`%MEM`·PID·`TIME+` 를 고르는 네 개입니다. 같은 man 은 이 네 키가 옛 `top` 과의 호환용이라 도움말 화면에는 나오지 않는다고 적습니다.[^keys]

| 키 | 뜻 |
|----|----|
| `P` | `%CPU` 로 정렬 |
| `M` | `%MEM` 으로 정렬 |
| `N` | PID 로 정렬 |
| `T` | `TIME+` 로 정렬 |
| `R` | 정렬 방향을 뒤집음 |
| `1` | CPU 상태를 한 줄에 합쳐 보이거나 CPU 마다 한 줄씩 보임 |
| `k` | 프로세스에 신호 보내기. PID 를 묻고 기본 신호는 SIGTERM |
| `r` | renice. PID 를 묻고 nice 값을 정함 |
| `c` | COMMAND 를 프로그램 이름과 명령줄 사이에서 바꿈 |
| `H` | 스레드 보기 토글 |
| `f` | 열을 고르고 순서와 정렬 열을 정하는 화면을 엶 |
| `W` | 지금의 옵션과 표시 방식을 설정 파일에 저장 |
| `q` | 종료 |

`k` 의 기본 신호가 SIGTERM 이고 `r` 이 PID 를 먼저 묻는다는 점은 둘 다 man 에 적혀 있습니다. 둘은 대화형 입력이라 `-b` 에서는 쓸 수 없습니다. 설정 파일의 저장 위치는 man 의 「FILES」에 있습니다.[^keys]



## 8. 로그로 쌓기와 ps 와의 쓰임

> 일정한 간격으로 프레임을 파일에 쌓아 두면 나중에 그 시간대의 부하를 되짚을 수 있습니다.

```bash
# 5초 간격으로 12프레임(1분)을 쌓는 관례. 여기서는 1초 간격 3프레임으로 같은 모양을 확인한다
# top -b -d 5 -n 12 > top.log
top -b -d 1 -n 3 > top.log; grep -c "^top -" top.log; grep -E "^(top -|%Cpu)" top.log
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

파일에는 프레임 3개가 이어져 있고 각 프레임은 `top -` 줄로 시작하므로 `awk` 로 프레임을 쪼갤 수 있습니다. 첫 프레임의 CPU 줄은 쓸모가 없으니 분석에서는 둘째부터 씁니다. 긴 수집은 `nohup top -b -d 5 -n 12 > top.log &` 처럼 백그라운드로 돌립니다.

같은 일을 `ps` 로도 할 수 있어 둘의 쓰임이 갈립니다. `top` 은 시간에 따른 프레임이고 `%CPU` 는 "마지막 화면 갱신 이후"의 몫이라 지금 순간의 사용률에 가깝습니다. 반면 `ps` 는 한 시점의 스냅숏이고 `%CPU` 는 CPU 시간을 프로세스가 산 시간으로 나눈 평균입니다.[^pcpu] 열을 직접 고르고 정렬해 스크립트에 넘기려면 `ps -eo` 가 더 단순합니다.

```bash
# ps 의 %CPU 는 시작 이후의 평균. 열 선택과 정렬이 한 줄에 된다
ps -eo pid,ni,pcpu,rss,comm --sort=-pcpu | head -3
```

```bash
    PID  NI %CPU   RSS COMMAND
   3131   0 99.9   956 yes
   3128   0  0.2 212176 python3
```

`ps` 옵션은 [ps 참조 시트](../process/ps.md)에 있습니다.



## 9. htop 으로 옮겨 가기

> `htop` 은 `top` 에 가로·세로 스크롤과 마우스, 트리 보기, 여러 프로세스 선택을 더한 화면입니다. 화면은 대화형이라 이 시트에 싣지 않고 실행 옵션과 키만 적습니다.

```bash
# 설치 (Debian/Ubuntu). 이 시트의 실습 준비가 이미 설치했다
apt-get install -y htop
htop --version    # htop 3.2.2
```

`htop` 의 실행 옵션은 `top` 과 이름이 비슷한데 뜻이 다른 것이 있습니다. `-d` 는 초가 아니라 10분의 1초 단위입니다.[^htopd]

```bash
htop                       # 기본 화면
htop -u appuser            # -u (--user): 이 사용자의 프로세스만. 이름 없이 -u 만 주면 $USER
htop -p 3128,3129          # -p (--pid): 이 PID 만. 쉼표로 여러 개
htop -t                    # -t (--tree): 트리 보기
htop -d 20                 # -d (--delay): 갱신 간격. 10분의 1초 단위라 20 은 2초
htop -s PERCENT_MEM        # -s (--sort-key): 이 열로 정렬. --sort-key help 로 목록
htop -F python             # -F (--filter): 명령에 이 문자열이 든 프로세스만
htop --readonly            # 신호 보내기·renice 같은 변경 기능을 끈다
htop -C                    # -C (--no-color): 흑백
```

`-s` 의 열 이름은 `htop --sort-key help` 가 보입니다. 아래는 그 목록에서 CPU 와 메모리 열만 고른 것입니다.[^htops]

```bash
# --sort-key help: 정렬에 쓸 수 있는 열 이름과 뜻의 목록
htop --sort-key help | grep -E "PERCENT_(CPU|MEM)|M_RESIDENT"
```

```bash
         M_RESIDENT Resident set size, size of the text and data sections, plus stack usage
        PERCENT_CPU Percentage of the CPU time the process used in the last sampling
        PERCENT_MEM Percentage of the memory the process is using, based on resident memory size
  PERCENT_CPU_DELAY CPU delay %
              M_PSS proportional set size, same as M_RESIDENT but each page is divided by the number of processes sharing it
```

`-s` 를 `-t` 없이 주면 목록 보기로 강제되고 트리로 보려면 `-t` 를 함께 줍니다.[^htops] 화면 안에서 자주 쓰는 키는 다음과 같습니다.[^htopkeys]

| 키 | 뜻 |
|----|----|
| `F1`, `h`, `?` | 도움말 |
| `F2`, `S` | 설정 화면. 상단 미터와 표시 열을 정함 |
| `F3`, `/` | 명령줄 검색 |
| `F4`, `\` | 명령줄에 이 문자열이 든 프로세스만 거름 |
| `F5`, `t` | 트리 보기 토글 |
| `F6`, `<`, `>` | 정렬 열 고르기 |
| `F7`, `]` | nice 값을 낮춤(우선순위 올림). 슈퍼유저만 |
| `F8`, `[` | nice 값을 올림(우선순위 내림) |
| `F9`, `k` | 신호 메뉴를 열어 보냄. 태그한 프로세스가 있으면 모두에게 |
| `F10`, `q` | 종료 |
| `Space` | 프로세스에 태그를 켜고 끔 |
| `I` | 정렬 방향을 뒤집음 |
| `u` | 사용자를 골라 그 프로세스만 |
| `H` | 사용자 스레드 숨김 토글 |
| `K` | 커널 스레드 숨김 토글 |

`top` 의 정렬 키 `M`·`P`·`T`·`N` 도 `htop` 에서 같은 뜻으로 됩니다.[^htopkeys] `top` 의 `k` 와 `htop` 의 `F9` 는 같은 일을 합니다. 다만 `htop` 은 신호를 메뉴에서 고르고 태그한 여러 프로세스에 한꺼번에 보낼 수 있습니다.

실습이 끝나면 띄운 프로세스를 정리합니다. 컨테이너를 나가면 모두 사라지므로 VM 에서 했을 때만 필요합니다. 출력은 `Killed` 알림뿐이라 싣지 않았습니다.

```bash
pkill -9 -x 'python3|yes|sleep|worker'
```



## 관련 문서

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [ps 참조 시트](../process/ps.md) — 한 시점의 스냅숏으로 프로세스를 고르고 정렬하는 법
- [자원마다 창이 따로 나 있어 어느 창을 여느냐가 곧 진단이다](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md#5-top-화면-구역과-배치-모드) — `top` 화면 네 구역과 배치 모드
- [프로세스 메모리는 세그먼트와 페이지로 나뉜다](../../../book/tlpi_the-linux-programming-interface/06-02.%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EB%8A%94%20%EC%84%B8%EA%B7%B8%EB%A8%BC%ED%8A%B8%EC%99%80%20%ED%8E%98%EC%9D%B4%EC%A7%80%EB%A1%9C%20%EB%82%98%EB%89%9C%EB%8B%A4.md#참조의-지역성과-요구-페이징) — `VIRT` 와 `RES` 가 갈리는 원리



## 참고 자료

- procps-ng 4.0.2 의 `man top` 원문 — Debian 12 컨테이너에서 2026-11-11 확인
- [top(1) — Debian bookworm](https://manpages.debian.org/bookworm/procps/top.1.en.html)
- [ps(1) — Debian bookworm](https://manpages.debian.org/bookworm/procps/ps.1.en.html)
- [htop(1) — Debian bookworm](https://manpages.debian.org/bookworm/htop/htop.1.en.html)

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
[^h]: `man top` COMMAND-LINE Options — `-H, --threads-show` "Instructs top to display individual threads. Without this command-line option a summation of all threads in each process is shown."
[^c]: `man top` COMMAND-LINE Options — `-c, --cmdline-toggle` "Starts top with the last remembered `c' state reversed. Thus, if top was displaying command lines, now that field will show program names, and vice versa." 출력을 파이프로 넘겼을 때 80열에서 잘리는 것은 이 환경에서 관찰한 값입니다. 같은 명령을 120열 터미널에 바로 찍으면 120열 폭에서 잘렸습니다.
[^w]: `man top` COMMAND-LINE Options — `-w, --width [=COLUMNS]` "In Batch mode, when used without an argument top will format output using the COLUMNS= and LINES= environment variables, if set. Otherwise, width will be fixed at the maximum 512 columns. With an argument, output width can be decreased or increased (up to 512) but the number of rows is considered unlimited.", "Note: Without the use of this command-line option, output width is always based on the terminal at which top was invoked whether or not in Batch mode."
[^keys]: `man top` INTERACTIVE Commands — k :Kill-a-task: "You will be prompted for a PID and then the signal to send. ... The default signal, as reflected in the prompt, is SIGTERM.", r :Renice-a-Task: "You will be prompted for a PID and then the value to nice it to.", "c :Command-Line/Program-Name toggle", "H :Threads-mode toggle", f :Fields-Management: "This key displays a separate screen where you can change which fields are displayed, their order and also designate the sort field.", W :Write-the-Configuration-File: "This will save all of your options and toggles plus the current display mode and delay time.", "1 :Single/Separate-Cpu-States toggle", "q :Quit", "R :Reverse/Normal-Sort-Field toggle", 정렬 키 표(M 은 %MEM, N 은 PID, P 는 %CPU, T 는 TIME+), "For compatibility, this top supports most of the former top sort keys. Since this is primarily a service to former top users, these commands do not appear on any help screen.", FILES 6a "This file is created or updated via the 'W' interactive command."
[^pcpu]: `man top` FIELDS %CPU -- CPU Usage: "The task's share of the elapsed CPU time since the last screen update"; `man ps` (procps-ng 4.0.2) STANDARD FORMAT SPECIFIERS `%cpu` "Currently, it is the CPU time used divided by the time the process has been running (cputime/realtime ratio), expressed as a percentage. It will not add up to 100% unless you are lucky." https://manpages.debian.org/bookworm/procps/ps.1.en.html
[^htopd]: `htop --help` (htop 3.2.2) — "-d --delay=DELAY Set the delay between updates, in tenths of seconds", `man htop` COMMAND-LINE OPTIONS "-d --delay=DELAY Delay between updates, in tenths of a second.", "-u --user=USERNAME|UID Show only the processes of a given user", "-p --pid=PID,PID... Show only the given PIDs", "-t --tree Show processes in tree view.", "-F --filter=FILTER Filter processes by terms matching the commands.", "--readonly Disable all system and process changing features", "-C --no-color --no-colour Start htop in monochrome mode", `htop --help` "-u --user[=USERNAME] Show only processes for a given user (or $USER)". https://manpages.debian.org/bookworm/htop/htop.1.en.html
[^htops]: `man htop` COMMAND-LINE OPTIONS — "-s --sort-key COLUMN Sort by this column (use --sort-key help for a column list). This will force a list view unless you specify -t at the same time." `htop --sort-key help` 출력 (3.2.2): "PERCENT_CPU Percentage of the CPU time the process used in the last sampling", "PERCENT_MEM Percentage of the memory the process is using, based on resident memory size", "M_RESIDENT Resident set size, size of the text and data sections, plus stack usage".
[^htopkeys]: `man htop` INTERACTIVE COMMANDS — "F1, h, ? Go to the help screen", "F2, S Go to the setup screen", "F3, / Incrementally search the command lines of all the displayed processes", "F4, \ Incremental process filtering: type in part of a process command line and only processes whose names match will be shown", "F5, t Tree view: organize processes by parenthood", "F6, <, > Selects a field for sorting", "F7, ] Increase the selected process's priority (subtract from 'nice' value). This can only be done by the superuser.", "F8, [ Decrease the selected process's priority (add to 'nice' value)", "F9, k "Kill" process: sends a signal which is selected in a menu, to one or a group of processes. If processes were tagged, sends the signal to all tagged processes.", "F10, q Quit", "Space Tag or untag a process", "I Invert the sort order", "u Show only processes owned by a specified user", "K Hide kernel threads", "H Hide user threads", "N Sort by PID. M Sort by memory usage (top compatibility key). P Sort by processor usage (top compatibility key). T Sort by time (top compatibility key)."
