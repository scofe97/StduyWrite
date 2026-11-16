---
title: uptime·free 참조 시트
tags: [linux, cheatsheet, uptime, free, procps, load-average, memory, cli, reference]
status: draft
source:
  - procps-ng 4.0.4 uptime(1)·free(1) (Ubuntu 26.04 `--help`·`man` 원문, manpages.debian.org testing)
  - Linux man-pages 6.17 proc_loadavg(5)·proc_meminfo(5) (Ubuntu 26.04 `man` 원문)
  - 《Learning Modern Linux》 8장 "Observability and Monitoring"(Michael Hausenblas, O'Reilly, 2022)
related:
  - ../README.md
  - ../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md
  - ./vmstat.md
  - ./top%C2%B7htop.md
  - ./watch.md
  - ../sysinfo/lscpu%C2%B7nproc.md
updated: 2026-11-16
---

# uptime·free 참조 시트

---

> 부하 평균을 읽는 `uptime` 과 메모리 열을 읽는 `free` 의 옵션을, 이 VM 에서 실제로 받은 출력과 함께 모았습니다.

## 개요

> `uptime` 은 부하 평균을, `free` 는 `/proc/meminfo` 로 만든 메모리 열을 읽습니다.

`vmstat` 는 [vmstat 참조 시트](./vmstat.md)에서 이어 다룹니다. 이 시트는 그 시트의 「실습 준비」 없이 돌아갑니다.

둘 다 procps 패키지의 외부 바이너리(`/usr/bin/uptime`·`/usr/bin/free`)입니다. `uptime` 은 현재 시각·가동 시간·사용자 수·부하 평균을 한 줄로 보여 줍니다. `free` 는 물리·스왑 메모리와 커널의 버퍼·캐시를 `/proc/meminfo` 에서 읽어 보여 줍니다.[^desc] 이 시트는 Ubuntu 26.04.1 LTS(OrbStack VM, procps-ng 4.0.4)에서 root 로 실측했습니다.

macOS 에는 `free` 가 없고 `uptime` 은 `-p`·`-s` 를 받지 않습니다.[^macos] 이 VM 은 다른 작업과 함께 쓰는 환경이라 부하 값에 이웃 작업이 조금 섞입니다. 인자를 잘못 줄 때 나는 오류는 「종료 코드」 에 있습니다.



## 핵심 문법

> `uptime` 은 옵션 둘로 출력 모양만 고르고, `free` 는 옵션으로 단위와 열 모양을 고릅니다.

```bash
# 호출 형태 (uptime --help, free --help 의 Usage 줄)
uptime [options]
free [options]

# 가동 시간과 부하 평균을 한 줄로 읽는다 (가동 시간과 부하 평균 읽기)
uptime
uptime -p
uptime -s

# 부하 평균을 CPU 수로 나눈다 (부하 평균을 CPU 수와 견주기)
uptime; nproc

# 다른 명령으로 부하를 만들고 다시 읽는다 (부하가 오르고 내리는 모양 보기)
cat /proc/loadavg

# 메모리 열을 읽는다 (free 열을 meminfo 필드와 맞추기)
free

# 단위를 정한다 (메모리 단위 고르기)
free -m
free -h

# 버퍼와 캐시를 나누고 합계 줄을 더한다 (버퍼·캐시를 나누고 합계 더하기)
free -w
free -t

# 일정 간격으로 되풀이한다 (메모리를 일정 간격으로 반복해 찍기)
free -s 초 -c 횟수

# 다른 명령으로 파일을 쓰며 열을 본다 (파일을 쓸 때 달라지는 열 보기)
free -m
```

### free 열과 /proc/meminfo 필드

> `free` 의 열은 `/proc/meminfo` 의 필드를 옮기거나 더하고 빼서 만듭니다.

뜻은 `man free` 의 열 설명을 따랐습니다.[^free-cols]

```bash
# Mem 줄과 Swap 줄 모두에 같은 열 이름이 쓰인다
# total       MemTotal·SwapTotal   쓸 수 있는 전체. 예약분과 커널 코드는 뺀다
# used        total - available    사용 중이거나 내줄 수 없는 양
# free        MemFree·SwapFree     아무 데도 쓰지 않는 양
# shared      Shmem                대부분 tmpfs 가 쓰는 양
# buffers     Buffers              커널 버퍼가 쓰는 양 (-w 에서만 나뉜다)
# cache       Cached·SReclaimable  페이지 캐시와 slab (-w 에서만 나뉜다)
# buff/cache  buffers + cache      두 열의 합
# available   MemAvailable         스왑 없이 새 프로그램을 띄울 수 있는 양의 추정
```



## 종료 코드

> 두 매뉴얼에 종료 코드 절이 없어, 이 환경에서 잰 값은 성공 0 과 오류 1 입니다.[^no-exit]

```bash
# 0  성공
# 1  모르는 옵션이나 남는 인자처럼 호출이 잘못된 경우

# 인자 없이 호출하면 성공한다
free > /dev/null; echo $?    # 0

# 모르는 옵션. 오류 한 줄과 사용법이 표준 오류로 나가고 코드는 1 이다
uptime --bad > /dev/null 2>&1; echo $?    # 1

# 남는 인자도 같다
free x > /dev/null 2>&1; echo $?          # 1
```



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션만 씁니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 도구가 갖춰집니다.

이 시트는 시스템이 가진 값을 읽고, 「파일을 쓸 때 달라지는 열 보기」 만 `/var/tmp/lab-mem.bin` 을 만들었다가 지웁니다. 이 VM 의 `dd` 는 uutils coreutils 0.10.0 입니다.

```bash
# procps(uptime·free)와 부하를 만드는 stress-ng 를 설치한다
# stress-ng 는 「부하가 오르고 내리는 모양 보기」 에서 쓴다
sudo apt-get install -y procps stress-ng
```

### 가동 시간과 부하 평균 읽기

> 한 줄에 현재 시각, 가동 시간, 로그인한 사용자 수, 부하 평균 세 값이 나옵니다.

부하 평균은 1분·5분·15분 평균입니다. 값을 CPU 수와 견주는 법은 다음 예에 있습니다.

```bash
# 현재 시각, 가동 시간, 사용자 수, 부하 평균(1분·5분·15분)을 한 줄로 읽는다
uptime
# 09:44:22 up 5 days, 16:51,  0 users,  load average: 1.25, 1.06, 0.49

# 가동 시간만 풀어서 읽는다
#   uptime -p   가동 시간을 사람이 읽는 꼴로 찍는다 (--pretty)
uptime -p    # up 5 days, 16 hours, 51 minutes

# 켜진 시각을 읽는다
#   uptime -s   시스템이 켜진 시각을 yyyy-mm-dd HH:MM:SS 로 찍는다 (--since)
uptime -s    # 2026-11-10 16:52:30

# 같은 부하 평균 세 값이 /proc/loadavg 앞 세 칸에 있다
# 4째 칸은 지금 실행 가능한 스케줄링 단위 수와 전체 수, 5째 칸은 마지막으로 만든 PID
cat /proc/loadavg
# 1.25 1.06 0.49 2/328 61641
```

`uptime` 의 `users` 는 현재 로그인한 사용자 수이며 이 VM 의 셸에서는 0 으로 나왔습니다.[^uptime-man] 부하 평균을 센 대상은 실행 가능하거나 입출력을 기다리는 프로세스이고, 4째 칸의 단위에는 스레드도 들어갑니다.[^loadavg]

### 부하 평균을 CPU 수와 견주기

> 부하 평균은 CPU 수로 나뉘어 있지 않아서, 값을 읽기 전에 CPU 수부터 확인합니다.

원리와 판정 기준은 책 노트의 [`uptime` 과 CPU 수](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md#uptime-과-cpu-수)에 있습니다. 여기서는 값을 나누는 명령만 보입니다.

```bash
# 부하 평균과 프로세스가 쓸 수 있는 CPU 수를 함께 찍는다
uptime; nproc
# 09:44:22 up 5 days, 16:51,  0 users,  load average: 1.25, 1.06, 0.49
# 7

# 설치된 CPU 수를 센다. 이 VM 에서는 nproc 과 값이 다르다
#   nproc --all   설치된 프로세서 수를 센다
nproc --all    # 8

# 세 값을 CPU 8개로 나눈다. 1.25 / 8 = 0.16 이 CPU 하나에 걸린 몫이다
#   awk -v   프로그램 안에서 쓸 변수 n 에 CPU 수를 넣는다
awk -v n="$(nproc --all)" '{printf "%.2f %.2f %.2f\n", $1/n, $2/n, $3/n}' /proc/loadavg
# 0.16 0.13 0.06
```

`nproc` 이 7 이고 `--all` 이 8 인 이유는 이 VM 의 셸이 CPU 7개에만 묶여 있기 때문입니다. 두 값이 갈리는 원리는 [lscpu·nproc 참조 시트](../sysinfo/lscpu·nproc.md)의 「프로세스에 걸린 CPU 제한」 에 있습니다.

### 부하가 오르고 내리는 모양 보기

> 부하를 만들고 `/proc/loadavg` 를 몇 번 읽으면 1분·5분·15분 값이 서로 다른 속도로 움직입니다.

4개 CPU 를 45초 동안 채운 뒤 20초, 42초 시점과 부하를 끝내고 30초 뒤에 읽습니다.[^stress]

```bash
# 시작 전 값을 읽고, 4개 CPU 를 45초 동안 채우는 부하를 백그라운드로 띄운다
#   stress-ng --cpu 4         CPU 만 쓰는 워커 4개를 시작한다 (-c)
#   stress-ng --timeout 45s   45초 뒤 끝낸다 (-t)
#   stress-ng --quiet         진행 메시지를 찍지 않는다 (-q)
cat /proc/loadavg
stress-ng \
  --cpu 4 \
  --timeout 45s \
  --quiet &

# 20초 뒤와 42초 뒤, 부하가 끝나고 30초 뒤에 다시 읽는다
sleep 20; cat /proc/loadavg
sleep 22; cat /proc/loadavg
wait
sleep 30; cat /proc/loadavg
```

```bash
1.41 1.47 0.78 1/323 62262
2.15 1.63 0.85 5/331 62396
2.81 1.82 0.93 5/331 62420
1.84 1.69 0.92 2/351 62507
```

1분 값이 1.41 에서 2.15, 2.81 로 가장 빨리 오르고 15분 값은 0.78 에서 0.93 으로 천천히 따라옵니다. 부하를 끝내자 1분 값이 1.84 로 내려갔고 4째 칸의 분자도 5 에서 2 로 돌아왔습니다. 시작 값이 0 이 아닌 것은 이 VM 의 이웃 작업 때문입니다.

### free 열을 meminfo 필드와 맞추기

> `free` 가 찍은 숫자를 같은 순간의 `/proc/meminfo` 필드로 다시 계산하면 열마다 출처가 보입니다.

열의 출처 목록은 「free 열과 /proc/meminfo 필드」 에 있습니다. `used` 와 `available` 이 내려가는 이유는 책 노트의 [`free` 여섯 열의 출처](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md#free-여섯-열의-출처)에 있습니다.

```bash
# 메모리 열을 읽는다. 단위를 안 주면 kibibyte 다
free
```

```bash
               total        used        free      shared  buff/cache   available
Mem:         8196284      764236     7279784       23168      349772     7432048
Swap:        9244852           0     9244852
```

```bash
# 같은 열을 /proc/meminfo 에서 다시 만든다
#   used = MemTotal - MemAvailable, buff/cache = Buffers + Cached + SReclaimable
awk '
  /^MemTotal/ {t=$2} /^MemFree/ {f=$2} /^MemAvailable/ {a=$2}
  /^Shmem:/ {s=$2} /^Buffers/ {b=$2} /^Cached/ {c=$2} /^SReclaimable/ {r=$2}
  END {
    print "total", t; print "used", t-a; print "free", f
    print "shared", s; print "buff/cache", b+c+r; print "available", a
  }
' /proc/meminfo
```

```bash
total 8196284
used 764044
free 7279760
shared 23168
buff/cache 350204
available 7432240
```

`total`·`shared` 는 같고, 나머지는 두 명령 사이에 값이 조금 움직여 끝자리가 다릅니다. `used` 는 각자의 `total - available` 과 맞습니다(8196284 - 7432240 = 764044).

### 메모리 단위 고르기

> 같은 표를 바이트부터 사람이 읽는 단위까지 바꿔 찍습니다.

바이트·mebibyte·gibibyte 는 `-b`·`-m`·`-g` 로, 사람이 읽는 단위는 `-h` 로 고릅니다. `--si` 와 `--mega` 는 1024 가 아니라 1000 단위로 셉니다.[^free-man]

```bash
# 단위를 바꿔 위 두 줄(머리와 Mem 줄)만 본다
#   free -b          바이트 (--bytes)
#   free -m          mebibyte (--mebi)
#   free -g          gibibyte (--gibi)
#   sed -n 1,2p      1~2째 줄만 찍는다
free -b | sed -n 1,2p
#                total        used        free      shared  buff/cache   available
# Mem:      8392994816   783065088  7453773824    23724032   358645760  7609929728

free -m | sed -n 1,2p
#                total        used        free      shared  buff/cache   available
# Mem:            8004         747        7108          22         342        7257

free -g | sed -n 1,2p
#                total        used        free      shared  buff/cache   available
# Mem:               7           0           6           0           0           7
```

```bash
# 열마다 가장 짧은 세 자리 단위를 골라 단위 글자를 붙인다
#   free -h   사람이 읽는 단위로 찍는다 (--human). Ki·Mi·Gi 는 1024 단위다
free -h
```

```bash
               total        used        free      shared  buff/cache   available
Mem:           7.8Gi       747Mi       6.9Gi        22Mi       342Mi       7.1Gi
Swap:          8.8Gi          0B       8.8Gi
```

```bash
# 1000 단위로 센다. 같은 -h 인데 단위 글자에서 i 가 빠진다
#   free --si     1024 대신 1000 의 거듭제곱을 쓴다
free --si -h
```

```bash
               total        used        free      shared  buff/cache   available
Mem:            8.4G        783M        7.5G         23M        358M        7.6G
Swap:           9.5G          0B        9.5G
```

```bash
# --mega 는 --si 를 뜻한다. 총량이 8004 가 아니라 8392 로 나온다
#   free --mega   megabyte (1000 단위)로 찍는다
free --mega | sed -n 1,2p
#                total        used        free      shared  buff/cache   available
# Mem:            8392         783        7453          23         358        7609
```

### 버퍼·캐시를 나누고 합계 더하기

> 기본 표에서 합쳐진 `buff/cache` 를 둘로 가르고, 메모리와 스왑의 합계 줄이나 커밋 줄을 덧붙입니다.

```bash
# buffers 와 cache 를 두 열로 나눈다. -m 과 함께 쓴다
#   free -w   넓은 출력. buffers 와 cache 를 따로 낸다 (--wide)
free -m -w
```

```bash
               total        used        free      shared     buffers       cache   available
Mem:            8004         747        7107          22           0         342        7256
Swap:           9028           0        9028
```

`buffers` 가 0 인 것은 `Buffers` 가 24KiB 라서 mebibyte 로 반올림하면 사라지기 때문입니다.

```bash
# 메모리와 스왑을 더한 합계 줄을 덧붙인다. total·used·free 만 있다
#   free -t   합계 줄을 낸다 (--total)
free -m -t
```

```bash
               total        used        free      shared  buff/cache   available
Mem:            8004         747        7107          22         342        7256
Swap:           9028           0        9028
Total:         17032         747       16135
```

```bash
# 커밋 한도와 커밋된 양을 덧붙인다. Comm 줄의 total 이 커밋 한도다
#   free -v   커밋 줄을 낸다 (--committed)
free -m -v
```

```bash
               total        used        free      shared  buff/cache   available
Mem:            8004         747        7107          22         342        7256
Swap:           9028           0        9028
Comm:          13030        1529       11500
```

```bash
# Low·High 메모리를 나눠 보여 준다. 64비트 시스템에서는 High 가 0 이다
#   free -l   low 와 high 메모리 통계를 낸다 (--lohi)
free -m -l
```

```bash
               total        used        free      shared  buff/cache   available
Mem:            8004         747        7107          22         342        7256
Low:            8004         896        7107
High:              0           0           0
Swap:           9028           0        9028
```

```bash
# 한 줄에 다 찍는다. 값은 kibibyte 이고 -s 와 함께 쓰면 로그처럼 쌓인다
#   free -L   한 줄 출력 (--line)
free -L
# SwapUse           0 CachUse      350452  MemUse      765628 MemFree     7278048
```

### 메모리를 일정 간격으로 반복해 찍기

> `-s` 로 간격을 주고 `-c` 로 횟수를 정하면 같은 표를 되풀이합니다.

`-s` 는 소수도 받습니다. 매뉴얼은 `-c` 에 `-s` 가 필요하다고 적지만 `-c` 만으로도 도는 것은 「free -c 단독 호출」 에 있습니다. 반복을 화면에 덮어 그리려면 [watch 참조 시트](./watch.md)의 `watch -n 1 free -m` 을 씁니다.

```bash
# 1초 간격으로 3번 찍는다. 표 사이에 빈 줄이 하나씩 들어간다
#   free -s 1   1초마다 되풀이해 찍는다 (--seconds)
#   free -c 3   3번 찍고 끝낸다 (--count)
free \
  -m \
  -s 1 \
  -c 3
```

```bash
               total        used        free      shared  buff/cache   available
Mem:            8004         747        7107          22         342        7256
Swap:           9028           0        9028

               total        used        free      shared  buff/cache   available
Mem:            8004         747        7107          22         342        7256
Swap:           9028           0        9028

               total        used        free      shared  buff/cache   available
Mem:            8004         747        7107          22         342        7256
Swap:           9028           0        9028
```

### 파일을 쓸 때 달라지는 열 보기

> 디스크의 일반 파일을 쓰면 `buff/cache` 가 늘고 `free` 가 줄지만 `available` 은 거의 그대로입니다.

`tmpfs` 에 쓰면 `shared` 와 `available` 까지 움직이는 점은 책 노트의 [`used`·`shared` 에 섞이는 tmpfs](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md#usedshared-에-섞이는-tmpfs)에 있습니다.

```bash
# 쓰기 전 값을 찍는다
free -m | sed -n 1,2p
#                total        used        free      shared  buff/cache   available
# Mem:            8004         748        7106          22         342        7255

# 512MiB 를 디스크 파일에 쓰고 Mem 줄만 찍는다
#   dd if=       읽을 파일. /dev/zero 는 0 바이트를 끝없이 준다
#   dd of=       쓸 파일
#   dd bs=1M     한 번에 1MiB 씩 읽고 쓴다
#   dd count=512 입력을 512번 읽고 멈춘다
#   dd status=none  전송 통계를 찍지 않는다
dd \
  if=/dev/zero \
  of=/var/tmp/lab-mem.bin \
  bs=1M \
  count=512 \
  status=none
free -m | sed -n 2p
# Mem:            8004         784        6586          22         855        7219

# 파일을 지우면 캐시도 함께 내려간다
rm /var/tmp/lab-mem.bin
free -m | sed -n 2p
# Mem:            8004         756        7098          22         343        7247
```

`buff/cache` 가 342 에서 855 로 늘고 `free` 가 7106 에서 6586 으로 줄었습니다. `available` 은 7255 에서 7219 로 조금만 내려갔습니다. 파일을 지우자 `buff/cache` 가 343 으로 돌아왔습니다.[^dd]

### 실습 정리

```bash
# 예가 만든 파일은 예 안에서 지웠다. 중간에 멈췄다면 남은 파일을 지운다
rm -f /var/tmp/lab-mem.bin
```



## 주의사항과 동작 원리

> `free -c` 는 매뉴얼과 다르게 돌고, 컨테이너 안의 `free`·`uptime` 은 호스트 값을 읽습니다.

### free -c 단독 호출

> 매뉴얼은 `-c` 에 `-s` 가 필요하다고 적었지만 이 판에서는 `-c` 만 줘도 1초 간격으로 돕니다.

```bash
# -s 없이 -c 만 준다. 오류 없이 3번 찍고, 1초 간격이라 2초가 걸린다
#   time -p   걸린 시간을 POSIX 형식으로 찍는다
time -p free -m -c 3 > /dev/null
# real 2.00
```

매뉴얼은 `-c` 가 `-s` 를 요구한다고 적지만 이 판의 동작은 다릅니다.[^free-man] 간격을 정하려면 `-s` 를 같이 줍니다.

### 컨테이너 안의 값은 호스트 것

> 컨테이너 안의 `free` 는 메모리 상한이 아니라 호스트의 `/proc/meminfo` 를 읽어 보여 줍니다.

macOS 셸에서 OrbStack 의 Docker 로 돌린 결과입니다.

```bash
# 메모리를 256MiB 로 제한한 컨테이너에서 free·uptime 과 cgroup 상한을 읽는다
#   docker run --rm   컨테이너를 띄우고 끝나면 지운다
#   docker run -m     컨테이너의 메모리 상한을 정한다
docker run --rm -m 256m ubuntu:26.04 sh -c '
  apt-get -qq update >/dev/null 2>&1
  apt-get -qq install -y procps >/dev/null 2>&1
  free -m | sed -n 1,2p
  cat /sys/fs/cgroup/memory.max
  uptime -s
'
```

```bash
               total        used        free      shared  buff/cache   available
Mem:            8004        1418        5783          41        1043        6586
268435456
2026-11-10 07:52:30
```

`total` 이 256 이 아니라 호스트의 8004 로 나오고 컨테이너의 실제 상한은 `memory.max` 의 268435456(256MiB)에 있습니다. `uptime -s` 도 호스트가 켜진 시각이며 컨테이너의 시간대가 UTC 라 VM 의 16:52:30 보다 9시간 이른 07:52:30 으로 나옵니다.[^free-man]



## 관련 문서

> 이 시트의 예와 이어지는 시트와 책 노트입니다.

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [vmstat 참조 시트](./vmstat.md) — 같은 자원 창의 프로세스·메모리·스왑·입출력·CPU 표본
- [자원마다 창이 따로 나 있어 어느 창을 여느냐가 곧 진단이다](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md) — 부하 평균과 `free` 열을 읽는 원리와 판정 기준
- [top·htop 참조 시트](./top·htop.md) — 요약 영역이 `uptime`·`free` 값을 한 화면에 보여 주는 시트
- [watch 참조 시트](./watch.md) — `free` 를 화면에 덮어 그려 되풀이할 때
- [lscpu·nproc 참조 시트](../sysinfo/lscpu·nproc.md) — 부하 평균과 견줄 CPU 수를 세는 법
- [ps·pstree 트리·스레드·상태 읽기](../process/ps%20트리·스레드·상태%20읽기.md) — 부하 평균이 세는 실행 가능·입출력 대기 상태의 글자



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- 검증 환경: Ubuntu 26.04.1 LTS(OrbStack VM `ubuntu`, 커널 7.2.12, aarch64), 2026-11-16
- 패키지: procps 2:4.0.4-9ubuntu1(procps-ng 4.0.4), stress-ng 0.20.01, dd(uutils coreutils 0.10.0)
- [uptime(1)](https://manpages.debian.org/testing/procps/uptime.1.en.html)·[free(1)](https://manpages.debian.org/testing/procps/free.1.en.html)
- [proc_loadavg(5)](https://manpages.debian.org/testing/manpages/proc_loadavg.5.en.html)·[proc_meminfo(5)](https://manpages.debian.org/testing/manpages/proc_meminfo.5.en.html)
- 원서: 《Learning Modern Linux》 8장 Observability and Monitoring (Michael Hausenblas, O'Reilly, 2022년)

[^desc]: `man free` (procps-ng 4.0.4) — "free displays the total amount of free and used physical and swap memory in the system, as well as the buffers and caches used by the kernel. The information is gathered by parsing /proc/meminfo."; `man uptime` — "uptime gives a one line display of the following information. The current time, how long the system has been running, how many users are currently logged on, and the system load averages for the past 1, 5, and 15 minutes." <https://manpages.debian.org/testing/procps/free.1.en.html> <https://manpages.debian.org/testing/procps/uptime.1.en.html>
[^macos]: macOS 26.6 의 `man uptime` — 사용법 `uptime [--libxo]`. 이 기기에서 `which free` 는 명령을 찾지 못했습니다.
[^free-cols]: `man free` (procps-ng 4.0.4) — "used Used or unavailable memory (calculated as total - available)", "shared Memory used (mostly) by tmpfs (Shmem in /proc/meminfo)", "buff/cache Sum of buffers and cache", "available Estimation of how much memory is available for starting new applications, without swapping."; `man 5 proc_meminfo` (Linux man-pages 6.17) — "MemAvailable %lu (since Linux 3.14) An estimate of how much memory is available for starting new applications, without swapping." <https://manpages.debian.org/testing/procps/free.1.en.html> <https://manpages.debian.org/testing/manpages/proc_meminfo.5.en.html>
[^free-man]: `man free` (procps-ng 4.0.4) — "-c, --count count Display the result count times. Requires the -s option.", "--si Use kilo, mega, giga etc (power of 1000) instead of kibi, mebi, gibi (power of 1024).", "--mega Display the amount of memory in megabytes. Implies --si.", "-w, --wide ... In this mode buffers and cache are reported in two separate columns.", "-t, --total Display a line showing the column totals.", "-v, --committed Display a line showing the memory commit limit and amount of committed/uncommitted memory." 컨테이너 안의 값은 이 시트의 실측입니다(`/sys/fs/cgroup/memory.max` 268435456, `free` 의 total 8004). <https://manpages.debian.org/testing/procps/free.1.en.html>
[^uptime-man]: `man uptime` (procps-ng 4.0.4) — "Load averages are not normalized for the number of CPUs in a system, so a load average of 1 means a single CPU system is loaded all the time while on a 4 CPU system it means it was idle 75% of the time.", "-p, --pretty show uptime in pretty format", "-s, --since system up since, in yyyy-mm-dd HH:MM:SS format". <https://manpages.debian.org/testing/procps/uptime.1.en.html>
[^loadavg]: `man 5 proc_loadavg` (Linux man-pages 6.17) — "The fourth field consists of two numbers separated by a slash (/). The first of these is the number of currently runnable kernel scheduling entities (processes, threads). The value after the slash is the number of kernel scheduling entities that currently exist on the system. The fifth field is the PID of the process that was most recently created on the system." <https://manpages.debian.org/testing/manpages/proc_loadavg.5.en.html>
[^stress]: `stress-ng --help` (stress-ng 0.20.01) — "-c N, --cpu N start N workers that perform CPU only loading", "-t N, --timeout T timeout after T seconds", "-q, --quiet quiet output".
[^dd]: `dd --help` (uutils coreutils 0.10.0) — "direct : use direct I/O for data.", "status=LEVEL : controls whether volume and performance stats are written to stderr", "none : Do not print any stats."
[^no-exit]: `man uptime` 의 절은 "NAME", "SYNOPSIS", "DESCRIPTION", "OPTIONS", "FILES", "AUTHORS", "SEE ALSO", "REPORTING BUGS", `man free` 의 절은 "NAME", "SYNOPSIS", "DESCRIPTION", "OPTIONS", "FILES", "BUGS", "SEE ALSO" 라서 두 매뉴얼 모두 EXIT STATUS 절이 없습니다(procps-ng 4.0.4, Ubuntu 26.04 `man` 원문). 성공 0 과 오류 1 은 이 시트의 실측입니다.
