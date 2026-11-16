---
title: vmstat 참조 시트
tags: [linux, cheatsheet, vmstat, procps, memory, swap, io, cpu, cli, reference]
status: draft
source:
  - procps-ng 4.0.4 vmstat(8) (Ubuntu 26.04 `--help`·`man` 원문, manpages.debian.org testing)
  - systemd-run(1)·systemd.resource-control(5) (스왑 실험의 메모리 상한)
  - 《Learning Modern Linux》 8장 "Observability and Monitoring"(Michael Hausenblas, O'Reilly, 2022)
related:
  - ../README.md
  - ../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md
  - ./uptime%C2%B7free.md
  - ./top%C2%B7htop.md
  - ./watch.md
  - ../sysinfo/lscpu%C2%B7nproc.md
updated: 2026-11-16
---

# vmstat 참조 시트

---

> 프로세스·메모리·스왑·입출력·시스템·CPU 를 한 표로 읽는 `vmstat` 의 옵션을, 이 VM 에서 실제로 받은 출력과 함께 모았습니다.

## 개요

> `vmstat` 는 여섯 자원 묶음의 표본을 한 줄씩 찍습니다.

`uptime`·`free` 는 [uptime·free 참조 시트](./uptime·free.md)에서 다룹니다. 이 시트는 그 시트의 「실습 준비」 없이 돌아가고 예가 쓰는 도구는 아래 「실습 준비」 가 설치합니다.

`vmstat` 는 procps 패키지의 외부 바이너리(`/usr/bin/vmstat`)입니다. 프로세스·메모리·페이징·블록 입출력·인터럽트·디스크·CPU 활동을 보고합니다.[^desc] 이 시트는 Ubuntu 26.04.1 LTS(OrbStack VM, procps-ng 4.0.4)에서 root 로 실측했습니다.

macOS 에는 `vmstat` 이 없고 메모리 통계는 `vm_stat` 이 맡습니다.[^macos] procps-ng 4.0.4 의 `vmstat` 은 CPU 묶음에 `gu` 열을 더 냅니다. 그래서 Debian 12(procps-ng 4.0.2)의 책 노트 출력보다 열이 하나 많습니다.[^vmstat-field] 이 VM 은 다른 작업과 함께 쓰는 환경이라 부하·입출력 값에 이웃 작업이 조금 섞입니다. 인자를 잘못 줄 때 나는 오류는 「종료 코드」 에 있습니다.



## 핵심 문법

> `vmstat` 는 옵션으로 표의 모양과 종류를 고르고, 간격과 횟수로 표본을 정합니다.

```bash
# 호출 형태 (vmstat --help 의 Usage 줄)
vmstat [options] [delay [count]]

# 표 한 줄과 간격·횟수 표본 (vmstat 첫 줄과 표본 간격 정하기)
vmstat
vmstat 초 횟수
vmstat -y 초 횟수
vmstat -n 초 횟수

# 부하를 걸고 표본을 읽는다 (CPU 를 채울 때 r 과 us 읽기 등)
vmstat 초 횟수

# 단위·폭·시각을 바꾼다 (단위·폭·시각 바꾸기)
vmstat -S M 초 횟수
vmstat -w 초 횟수
vmstat -t 초 횟수

# 메모리 구성과 누적 카운터를 본다 (메모리 구성과 누적 카운터 보기)
vmstat -a 초 횟수
vmstat -f
vmstat -s

# 디스크별 통계를 본다 (디스크별 통계 보기)
vmstat -d
vmstat -D
vmstat -p 파티션
```

### vmstat 열

> `vmstat` 의 열은 여섯 묶음이고, 앞 두 묶음은 순간 값이며 나머지는 표본 구간의 값입니다.

뜻은 `man vmstat` 의 FIELD DESCRIPTION 을 따랐습니다.[^vmstat-field]

```bash
# procs    r      실행 가능한 프로세스 수. 실행 중이거나 차례를 기다리는 것
# procs    b      입출력이 끝나기를 기다리며 막힌 프로세스 수
# memory   swpd   쓰는 중인 스왑 양
# memory   free   아무 데도 쓰지 않는 메모리 양
# memory   buff   버퍼로 쓰는 메모리 양
# memory   cache  캐시로 쓰는 메모리 양
# memory   inact  비활성 메모리 양 (-a 일 때 buff·cache 자리에 나온다)
# memory   active 활성 메모리 양 (-a 일 때)
# swap     si     디스크에서 스왑으로 들어온 양 (초당)
# swap     so     디스크 스왑으로 나간 양 (초당)
# io       bi     블록 장치에서 받은 양 (KiB/s)
# io       bo     블록 장치로 보낸 양 (KiB/s)
# system   in     초당 인터럽트 수. 시계 인터럽트를 포함한다
# system   cs     초당 컨텍스트 전환 수
# cpu      us     커널이 아닌 코드를 돈 시간 (nice 포함)
# cpu      sy     커널 코드를 돈 시간
# cpu      id     논 시간
# cpu      wa     입출력을 기다린 시간
# cpu      st     가상 머신에서 도둑맞은 시간
# cpu      gu     KVM 게스트 코드를 돈 시간 (procps-ng 4.0.4 의 열)
```



## 종료 코드

> 매뉴얼에 종료 코드 절이 없어, 이 환경에서 잰 값은 성공 0 과 오류 1 입니다.[^no-exit]

```bash
# 0  성공
# 1  잘못된 인자나 모르는 옵션으로 호출이 잘못된 경우

# 인자 없이 호출하면 성공한다
vmstat > /dev/null; echo $?    # 0

# 간격이 0 이면 거절한다
vmstat 0 2; echo $?
# vmstat: delay must be positive integer
# 1

# 숫자가 아닌 인자
vmstat x; echo $?
# vmstat: failed to parse argument: 'x'
# 1
```



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션만 씁니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 도구가 갖춰집니다.

이 시트는 시스템이 가진 값을 읽고, 「디스크 입출력의 bi·bo 읽기」 만 `/var/tmp/lab-mem.bin` 을 만들었다가 지웁니다. 이 VM 의 `dd` 는 uutils coreutils 0.10.0 입니다.

```bash
# procps(vmstat)와 부하를 만드는 stress-ng 를 설치한다
# stress-ng 는 「CPU 를 채울 때 r 과 us 읽기」 부터 쓴다
sudo apt-get install -y procps stress-ng
```

### vmstat 첫 줄과 표본 간격 정하기

> 간격을 주지 않으면 한 줄, 주면 그 간격마다 한 줄이며 첫 줄은 부팅 뒤 평균입니다.

첫 줄이 평균이라는 점과 간격·횟수의 뜻은 매뉴얼에 있습니다.[^vmstat-man] 책 노트는 열을 묶어 읽는 법을 [`vmstat` 한 줄의 여섯 축](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md#vmstat-한-줄의-여섯-축)에서 다룹니다.

```bash
# 표를 한 번만 찍는다. 이 한 줄은 부팅 뒤 평균이다
vmstat
```

```bash
procs -----------memory---------- ---swap-- -----io---- -system-- -------cpu-------
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st gu
 1  0      0 6309108     44 711868   23   30   481   708  425    0  0  0 100  0  0  0
```

```bash
# 1초 간격으로 3줄을 찍는다. 첫 줄은 위와 같은 부팅 뒤 평균이고 둘째 줄부터 직전 1초다
vmstat 1 3
```

```bash
procs -----------memory---------- ---swap-- -----io---- -system-- -------cpu-------
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st gu
 0  0      0 6308736     44 712012   23   30   481   708  425    0  0  0 100  0  0  0
 0  0      0 6308460     44 712236    0    0     0   292 1633 2738  1  1 98  0  0  0
 2  0      0 6306468     44 714980    0    0  2948     0 1708 2843  1  1 98  0  0  0
```

첫 줄의 `si` 23·`so` 30 은 이 VM 이 켜진 뒤 한 번이라도 스왑을 쓴 기록이 평균에 남은 값이고, 둘째 줄부터는 0 입니다.

```bash
# 첫 줄(부팅 뒤 평균)을 뺀다
#   vmstat -y   부팅 뒤 평균 줄을 빼고 찍는다 (--no-first)
vmstat -y 1 2
```

```bash
procs -----------memory---------- ---swap-- -----io---- -system-- -------cpu-------
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st gu
 0  0      0 6298632     44 720892    0    0  4944   176 1838 3012  2  1 97  0  0  0
 0  0      0 6290436     44 728048    0    0  7056   136 1786 2941  2  1 97  0  0  0
```

```bash
# 표 머리가 몇 번 나오는지 센다. 25줄을 찍으면 머리가 두 번 나온다
#   grep -c   맞는 줄 수를 센다
vmstat 1 25 | grep -c '^procs'    # 2

# 머리를 한 번만 찍는다
#   vmstat -n   머리를 한 번만 찍는다 (--one-header)
vmstat -n 1 25 | grep -c '^procs'    # 1
```

### CPU 를 채울 때 r 과 us 읽기

> CPU 워커를 4개 띄우면 `r` 이 4 가 되고 `us` 가 CPU 전체의 4/8 인 50 근처로 올라갑니다.

`r` 은 실행 가능한 프로세스 수이고 `us` 는 전체 CPU 시간 가운데 사용자 코드를 돈 비율입니다.

```bash
# 6초 동안 CPU 워커 4개를 돌리면서 표본을 5줄 찍는다
stress-ng \
  --cpu 4 \
  --timeout 6s \
  --quiet &
vmstat 1 5
wait
```

```bash
procs -----------memory---------- ---swap-- -----io---- -system-- -------cpu-------
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st gu
 2  0      0 6960460    116 581828   23   30   472   484  418    0  0  0 100  0  0  0
 4  0      0 6933656    116 598816    0    0 16444     0 4028  140 47  1 52  0  0  0
 4  0      0 6933656    116 598816    0    0     0     0 4215   78 50  0 50  0  0  0
 4  0      0 6933656    116 598816    0    0     0     0 4185   70 50  0 50  0  0  0
 4  0      0 6944372    116 598736    0    0     0     0 4114   88 50  0 50  0  0  0
```

첫 줄은 부팅 뒤 평균이라 `us` 가 0 이고, 둘째 줄부터 `r` 4·`us` 50 이 됩니다. 이 VM 에는 CPU 가 8개라 4개를 채우면 `us` 가 50 입니다.[^stress] 이때 `nproc` 은 7 을 찍는 이유는 「nproc 은 7 인데 vmstat 은 8개 기준」 에 있습니다.

### 디스크 입출력의 bi·bo 읽기

> 파일을 쓰면 `bo` 가, 읽으면 `bi` 가 KiB/s 로 올라갑니다.

`dd` 를 1초 뒤에 시작하는 백그라운드 부분 셸에 넣어 두면 `vmstat` 의 둘째 줄이 그 구간을 담습니다.[^dd]

```bash
# 1초 뒤 400MiB 를 디스크에 쓰는 동안 표본을 4줄 찍는다
#   dd oflag=direct   페이지 캐시를 거치지 않고 바로 쓴다
(sleep 1; dd if=/dev/zero of=/var/tmp/lab-mem.bin \
  bs=1M count=400 oflag=direct status=none) &
vmstat 1 4
wait
```

```bash
procs -----------memory---------- ---swap-- -----io---- -system-- -------cpu-------
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st gu
 1  0      0 6443944   3560 1109036   14   19   462   298  414    0  0  0 100  0  0  0
 1  0      0 6404176   3560 1109484    0    0     0     0 3300 5796  4  5 91  0  0  0
 1  0      0 6249916   3560 1188068    0    0    16 409600 4520 5928  8  7 84  0  0  0
 0  0      0 6255524   3560 1189472    0    0   128  1324 1183 1629  1  2 94  4  0  0
```

```bash
# 같은 파일을 읽는 동안 표본을 4줄 찍는다. 읽은 만큼 cache 도 늘어난다
(sleep 1; dd if=/var/tmp/lab-mem.bin of=/dev/null bs=1M status=none) &
vmstat 1 4
wait
rm /var/tmp/lab-mem.bin
```

```bash
procs -----------memory---------- ---swap-- -----io---- -system-- -------cpu-------
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st gu
 2  0      0 6255296   3560 1189472   14   19   462   299  414    0  0  0 100  0  0  0
 0  0      0 6277620   3560 1189576    0    0   100     0  382  393  0  1 99  0  0  0
 0  0      0 5869400   3560 1599176    0    0 409600     0  314  150  0  2 98  0  0  0
 0  0      0 5901444   3560 1599176    0    0     0     0   95   79  0  0 100  0  0  0
```

400MiB 는 409600KiB 이고, 쓸 때는 `bo` 가 읽을 때는 `bi` 가 그 값 근처로 뛰었습니다. 읽은 뒤 `cache` 는 1189576 에서 1599176 으로 409600 늘었습니다. 이 두 열은 KiB/s 라서 `-S` 로 단위가 바뀌지 않습니다.[^vmstat-man]

### 스왑이 일어날 때 si·so 읽기

> 메모리 상한을 걸어 둔 프로세스가 상한보다 많이 쓰면 `si`·`so` 와 `swpd` 가 0 에서 올라갑니다.

`si` 는 스왑에서 들어온 양, `so` 는 스왑으로 나간 양입니다. 이 VM 의 스왑은 zram 과 디스크 파티션이고, 상한은 실험용 `scope` 에만 걸립니다.[^systemd-run]

```bash
# 1초 뒤 메모리 상한 300MiB 의 scope 안에서 600MB 를 계속 쓰는 워커를 8초 돌린다
#   systemd-run --scope           서비스 대신 transient scope 유닛으로 시작한다
#   systemd-run -p MemoryMax=300M    이 유닛의 메모리 사용 상한을 300MiB 로 둔다
#   systemd-run -p MemorySwapMax=2G  이 유닛의 스왑 사용 상한을 2GiB 로 둔다
#   systemd-run --quiet           시작 메시지를 찍지 않는다
#   stress-ng --vm 1              익명 mmap 을 돌리는 워커 1개를 시작한다 (-m)
#   stress-ng --vm-bytes 600M     워커마다 600MB 를 할당한다
(sleep 1; sudo systemd-run --quiet --scope \
  -p MemoryMax=300M -p MemorySwapMax=2G \
  stress-ng --vm 1 --vm-bytes 600M --timeout 8s --quiet) &
vmstat 1 12
wait
```

```bash
procs -----------memory---------- ---swap-- -----io---- -system-- -------cpu-------
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st gu
 2  0      0 6319192   3560 1189576   14   19   463   299  414    0  0  0 100  0  0  0
 0  0      0 6319168   3560 1189576    0    0     0     0   72   68  0  0 100  0  0  0
 1  0 309080 5993948   3560 1190264 1208392 1517324 1209076 1517324 1781 2640  1 13 87  0  0  0
 2  0 309076 5995860   3560 1190264 1185052 1800588 1185308 1800588 1382 3379  4  9 87  0  0  0
 4  0 102068 5998168   3560 1190076 678848 779580 678848 779580 1666 1844  2  8 90  0  0  0
 1  0 308940 5874892   3560 1190076 31012 237856 31012 237856 1398  824  1 12 87  0  0  0
 1  0 308892 5873752   3560 1190076 198640 198604 198640 198604 1283  801  0 12 88  0  0  0
 1  0 308976 5871928   3560 1190076 216316 216380 216316 216380 1113  796  1 11 89  0  0  0
 1  0 308996 5869876   3560 1190076 307100 307136 307100 307136 1276 1005  1 12 87  0  0  0
 2  0 253148 5933704   3564 1190144 270140 270256 270208 270256 1961 2184  2 13 85  0  0  0
 0  0      0 6441664   3564 1190196  424    0   424 81556  185  205  0  1 99  0  0  0
 0  0      0 6441664   3564 1190196    0    0     0     0   84   82  0  0 100  0  0  0
```

워커가 시작하자 `swpd` 가 0 에서 약 309080KiB 로 오르고 `si`·`so` 가 수십만에서 백만 KiB/s 대로 뛰었습니다. 이 구간의 `bi`·`bo` 는 `si`·`so` 와 거의 같은 값입니다. 워커가 끝나자 `swpd` 가 0 으로 내려왔습니다.

### 단위·폭·시각 바꾸기

> 메모리 열의 단위를 바꾸고, 열 폭을 넓히고, 줄마다 시각을 붙입니다.

```bash
# 메모리 열을 M 단위로 찍는다. bi·bo 는 바뀌지 않는다
#   vmstat -S M   단위를 M(1048576 바이트)으로 바꾼다 (--unit)
#                  k 는 1000, K 는 1024, m 은 1000000 바이트다
vmstat -S M 1 2
```

```bash
procs -----------memory---------- ---swap-- -----io---- -system-- -------cpu-------
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st gu
 0  0      0   7094      0    405    0    0   461   292  413    0  0  0 100  0  0  0
 0  0      0   7092      0    405    0    0     8     0  115  102  0  0 100  0  0  0
```

```bash
# 메모리가 큰 시스템에서 열이 붙어 보이는 것을 막는다. 열이 넓어진다
#   vmstat -w   넓은 출력 (--wide)
vmstat -w 1 2
```

```bash
--procs-- -----------------------memory---------------------- ---swap-- -----io---- -system-- ----------cpu----------
   r    b         swpd         free         buff        cache   si   so    bi    bo   in   cs  us  sy  id  wa  st  gu
   0    0            0      7262136           32       414968   14   19   461   292  413    0   0   0 100   0   0   0
   0    0            0      7260864           32       414968    0    0     0     0   81   66   0   0 100   0   0   0
```

```bash
# 줄마다 오른쪽 끝에 시각을 붙인다. 머리의 KST 는 시간대다
#   vmstat -t   타임스탬프를 붙인다 (--timestamp)
vmstat -t 1 2
```

```bash
procs -----------memory---------- ---swap-- -----io---- -system-- -------cpu------- -----timestamp-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st gu                 KST
 1  0      0 7260864     32 414968   14   19   461   292  413    0  0  0 100  0  0  0 2026-11-16 09:47:08
 0  0      0 7260360     32 415416    0    0   424     0  295   72  3  0 97  0  0  0 2026-11-16 09:47:09
```

### 메모리 구성과 누적 카운터 보기

> 활성·비활성 메모리를 열로 바꾸고, 부팅 뒤 누적 카운터를 표로 봅니다.

```bash
# buff·cache 대신 비활성(inact)과 활성(active) 메모리를 찍는다
#   vmstat -a   활성·비활성 메모리를 찍는다 (--active)
vmstat -a 1 2
```

```bash
procs -----------memory---------- ---swap-- -----io---- -system-- -------cpu-------
 r  b   swpd   free  inact active   si   so    bi    bo   in   cs us sy id wa st gu
 0  0      0 7259904 192264 206168   14   19   461   292  413    0  0  0 100  0  0  0
 0  0      0 7259376 192312 206328    0    0     0     0 2166   74  0  0 100  0  0  0
```

```bash
# 부팅 뒤 만든 태스크 수를 찍는다. fork·vfork·clone 을 모두 센다
#   vmstat -f   부팅 뒤 fork 수를 찍는다 (--forks)
vmstat -f
# 692403 forks

# 이벤트 카운터와 메모리 통계를 표로 찍는다. 한 번만 찍고 끝난다
#   vmstat -s   카운터 표를 찍는다 (--stats)
vmstat -s
```

```bash
      8196284 K total memory
       753820 K used memory
       206260 K active memory
       192312 K inactive memory
      7254568 K free memory
           32 K buffer memory
       415416 K swap cache
      9244852 K total swap
            0 K used swap
      9244852 K free swap
       357560 non-nice user cpu ticks
           14 nice user cpu ticks
       383365 system cpu ticks
    392349750 idle cpu ticks
        29695 IO-wait cpu ticks
            0 IRQ cpu ticks
        87060 softirq cpu ticks
            0 stolen cpu ticks
            0 non-nice guest cpu ticks
            0 nice guest cpu ticks
    227334239 K paged in
    144028243 K paged out
      1846517 pages swapped in
      2462517 pages swapped out
    204051448 interrupts
     90234208 CPU context switches
   1794297150 boot time
       692404 forks
```

```bash
# boot time 은 부팅 시각의 에포크 초다. 날짜로 바꾸면 uptime -s 와 같다
date -d @"$(vmstat -s | awk '/boot time/ {print $1}')" '+%F %T'    # 2026-11-10 16:52:30
uptime -s                                                          # 2026-11-10 16:52:30
```

에포크 초를 날짜로 바꾸는 `date -d @초` 는 [date 참조 시트](../time/date.md)에 있습니다.

### 디스크별 통계 보기

> 디스크마다 읽기·쓰기 누적 횟수와 섹터를 보거나, 전체 합계나 파티션 하나만 봅니다.

열은 `man vmstat` 의 디스크 모드 설명을 따랐습니다.[^vmstat-man]

```bash
# 디스크별 누적 통계를 찍는다. 이 VM 에는 루프 장치가 많아 vd·zram 줄만 남긴다
# reads·writes 열   total 성공한 횟수, merged 묶인 횟수, sectors, ms 걸린 시간
# IO 열             cur 진행 중인 입출력 수, sec 입출력에 쓴 초(man 의 s)
#   vmstat -d    디스크 통계를 찍는다 (--disk)
#   awk 'NR <= 2 || /^(vd|zram)/'   머리 두 줄과 vd·zram 으로 시작하는 줄만 남긴다
vmstat -d | awk 'NR <= 2 || /^(vd|zram)/'
```

```bash
disk- ------------reads------------ ------------writes----------- -----IO------
       total merged sectors      ms  total merged sectors      ms    cur    sec
vda   669171   8238 155818680   45204      0      0       0       0      0   2279
vdb   2552378   7766 283483549  248254 2964575 835940 267631488 1177211      0   1512
vdc      267      0   39984       3      1      0       8       0      0      0
zram0 819966      0 14777424    2045 1011790      0 19700144    9045      0     11
```

```bash
# 모든 디스크를 합친 요약을 찍는다
#   vmstat -D   디스크 활동 요약을 찍는다 (--disk-sum)
vmstat -D
```

```bash
           21 disks
            1 partitions
      4050295 total reads
        16026 merged reads
    454674894 read sectors
       295917 milli reading
      3978351 writes
       838403 merged writes
    288754747 written sectors
      1190900 milli writing
            0 inprogress IO
         3803 milli spent IO
         2238 milli weighted IO
```

```bash
# 파티션 하나의 읽기·쓰기만 본다. 이름은 lsblk 로 확인한다
#   vmstat -p vdb1   파티션 vdb1 의 통계를 찍는다 (--partition)
vmstat -p vdb1
```

```bash
vdb1            reads      read sectors      writes  requested writes
              2552196         283480008     2964575         267631488
```

### 실습 정리

```bash
# 예가 만든 파일은 예 안에서 지웠다. 중간에 멈췄다면 남은 파일을 지운다
rm -f /var/tmp/lab-mem.bin
```



## 주의사항과 동작 원리

> `vmstat` 의 CPU 비율은 `nproc` 과 CPU 수 기준이 다르고, `-m` 은 이 VM 에서 실패합니다.

### nproc 은 7 인데 vmstat 은 8개 기준

> `vmstat` 의 `us`·`sy`·`id` 는 이 VM 의 CPU 8개 전체에 대한 비율이라, CPU 7개에 묶인 셸의 `nproc` 과 기준이 다릅니다.

```bash
# 이 셸이 쓸 수 있는 수와 설치된 수
nproc        # 7
nproc --all  # 8
```

워커 4개를 돌린 「CPU 를 채울 때 r 과 us 읽기」 에서 `us` 는 4/7 = 57 이 아니라 4/8 = 50 이었습니다.

### vmstat -m 이 슬랩 정보를 못 읽는 환경

> `-m` 은 `/proc/slabinfo` 를 읽는데, 이 VM 의 커널에는 그 파일이 없어 root 로 쳐도 실패합니다.

```bash
# 슬랩 통계를 찍으려 한다. root 로도 실패한다
#   vmstat -m   slabinfo 를 찍는다 (--slabs)
sudo vmstat -m    # vmstat: Unable to create slabinfo structure: No such file or directory
```

매뉴얼은 `-m` 이 `/proc/slabinfo` 읽기 권한을 요구하고 일반 사용자는 못 읽을 수 있다고 적습니다.[^vmstat-man] 이 VM 에서는 권한이 아니라 파일 자체가 없습니다.



## 관련 문서

> 이 시트의 예와 이어지는 시트와 책 노트입니다.

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [uptime·free 참조 시트](./uptime·free.md) — 같은 자원 창의 부하 평균과 메모리 열
- [자원마다 창이 따로 나 있어 어느 창을 여느냐가 곧 진단이다](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md) — `vmstat` 열을 읽는 원리와 판정 기준
- [top·htop 참조 시트](./top·htop.md) — 요약 영역의 CPU 줄이 `vmstat` 의 `us`·`sy`·`id` 와 같은 축인 시트
- [watch 참조 시트](./watch.md) — `vmstat` 을 화면에 덮어 그려 되풀이할 때
- [lsof 참조 시트](./lsof.md) — 같은 자원 창 가운데 열린 파일을 여는 시트
- [lscpu·nproc 참조 시트](../sysinfo/lscpu·nproc.md) — `r` 과 견줄 CPU 수를 세는 법
- [date 참조 시트](../time/date.md) — `vmstat -s` 의 에포크 초를 날짜로 바꾸는 법



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- 검증 환경: Ubuntu 26.04.1 LTS(OrbStack VM `ubuntu`, 커널 7.2.12, aarch64), 2026-11-16
- 패키지: procps 2:4.0.4-9ubuntu1(procps-ng 4.0.4), stress-ng 0.20.01, dd(uutils coreutils 0.10.0)
- [vmstat(8)](https://manpages.debian.org/testing/procps/vmstat.8.en.html)
- [systemd-run(1)](https://manpages.debian.org/testing/systemd/systemd-run.1.en.html)·[systemd.resource-control(5)](https://manpages.debian.org/testing/systemd/systemd.resource-control.5.en.html)
- 원서: 《Learning Modern Linux》 8장 Observability and Monitoring (Michael Hausenblas, O'Reilly, 2022년)

[^desc]: `man vmstat` (procps-ng 4.0.4) — "vmstat reports information about processes, memory, paging, block IO, traps, disks and cpu activity." <https://manpages.debian.org/testing/procps/vmstat.8.en.html>
[^macos]: macOS 26.6 의 `man vm_stat` — "vm_stat displays Mach virtual memory statistics." 이 기기에서 `which vmstat` 는 명령을 찾지 못했습니다.
[^vmstat-field]: `man vmstat` (procps-ng 4.0.4), FIELD DESCRIPTION FOR VM MODE — "r: The number of runnable processes (running or waiting for run time).", "b: The number of processes blocked waiting for I/O to complete.", "si: Amount of memory swapped in from disk (/s).", "bi: Kibibyte received from a block device (KiB/s).", "st: Time stolen from a virtual machine.", "gu: Time spent running KVM guest code (guest time, including guest nice)." <https://manpages.debian.org/testing/procps/vmstat.8.en.html>
[^vmstat-man]: `man vmstat` (procps-ng 4.0.4) — "The first report produced gives averages since the last reboot.", "delay The delay between updates in seconds. If no delay is specified, only one report is printed with the average values since boot.", "-y, --no-first Omits first report with statistics since system boot.", "-n, --one-header Display the header only once rather than periodically.", "-S, --unit character Switches outputs between 1000 (k), 1024 (K), 1000000 (m), or 1048576 (M) bytes.", "bi: Kibibyte received from a block device (KiB/s).", "vmstat requires read access to files under /proc. The -m requires read access to /proc/slabinfo which may not be available to standard users." <https://manpages.debian.org/testing/procps/vmstat.8.en.html>
[^systemd-run]: `man systemd-run` — "--scope Create a transient .scope unit instead of the default transient .service unit"; `man systemd.resource-control` — "MemoryMax=bytes ... Specify the absolute limit on memory usage of the executed processes in this unit.", "MemorySwapMax=bytes ... Specify the absolute limit on swap usage of the executed processes in this unit." <https://manpages.debian.org/testing/systemd/systemd-run.1.en.html> <https://manpages.debian.org/testing/systemd/systemd.resource-control.5.en.html>
[^stress]: `stress-ng --help` (stress-ng 0.20.01) — "-c N, --cpu N start N workers that perform CPU only loading", "-m N, --vm N start N workers spinning on anonymous mmap", "--vm-bytes N allocate N bytes per vm worker (default 256MB)", "-t N, --timeout T timeout after T seconds", "-q, --quiet quiet output".
[^dd]: `dd --help` (uutils coreutils 0.10.0) — "direct : use direct I/O for data.", "status=LEVEL : controls whether volume and performance stats are written to stderr", "none : Do not print any stats."
[^no-exit]: `man vmstat` 의 절은 "NAME", "SYNOPSIS", "DESCRIPTION", "OPTIONS", FIELD DESCRIPTION 넷, "NOTES", "SEE ALSO", "REPORTING BUGS" 라서 EXIT STATUS 절이 없습니다(procps-ng 4.0.4, Ubuntu 26.04 `man` 원문). 성공 0 과 오류 1 은 이 시트의 실측입니다.
