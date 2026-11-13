---
title: lscpu·nproc 참조 시트
tags: [linux, cheatsheet, dmidecode, lscpu, nproc, smbios, cpu, cli, reference]
status: draft
source:
  - util-linux 2.38.1 lscpu(1), lsmem(1) (Debian 12 패키지 man 원문, manpages.debian.org bookworm)
  - dmidecode 3.4 dmidecode(8), lshw(1) (Debian 12 패키지 man 원문)
  - coreutils 9.1 nproc(1) (`nproc --help` 원문)
  - Linux man-pages proc(5), mem(4) (Debian 12 manpages)
  - Docker Docs, Resource constraints
  - Linux kernel documentation, Control Group v2, The Unified Extensible Firmware Interface (UEFI)
related:
  - ../README.md
  - ./dmidecode%C2%B7lscpu%20DMI%20표와%20메모리%20읽기.md
  - ../../../book/learning-modern-linux/02-01.%EC%BB%A4%EB%84%90%EC%9D%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%ED%95%98%EC%A7%80%EB%A7%8C%20%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EB%8A%94%20%EC%95%84%EB%8B%88%EB%8B%A4.md
  - ./uname%C2%B7os-release%C2%B7hostnamectl.md
updated: 2026-11-13
---

# lscpu·nproc 참조 시트

---

> CPU 구성을 읽는 `lscpu` 와 프로세스가 쓸 수 있는 CPU 수를 세는 `nproc` 의 옵션을, 이 기기에서 실제로 받은 출력과 함께 모았습니다.

## 개요

> `lscpu` 는 CPU 구성을, `nproc` 은 프로세스가 쓸 수 있는 CPU 수를 읽습니다.

`lscpu` 는 util-linux, `nproc` 은 coreutils 의 외부 바이너리입니다. macOS 에는 `lscpu`·`dmidecode`·`nproc` 이 기본으로 없어서 Linux 에서 실행합니다.

이 시트는 Debian 12 컨테이너(util-linux 2.38.1, coreutils 9.1, dmidecode 3.4)의 root 로 실측했습니다. 출력은 Apple Silicon 위의 가상 환경이라 CPU 가 `aarch64` 이고, 물리 서버나 x86 가상 머신에서는 값과 줄이 다릅니다.

펌웨어의 DMI 표를 읽는 `dmidecode` 와 메모리를 읽는 `lsmem`·`lshw` 는 [dmidecode·lsmem·lshw DMI 표와 메모리 읽기 시트](./dmidecode·lscpu%20DMI%20표와%20메모리%20읽기.md)에서 이어 다룹니다.



## 핵심 문법

> `lscpu` 는 옵션으로 출력 모양을 고르고, `nproc` 은 옵션 없이 호출해 프로세스가 쓸 수 있는 수를 냅니다.

```bash
# 호출 형태 (lscpu --help, nproc --help 의 Usage 줄)
lscpu [options]
nproc [OPTION]...

# CPU 구성 요약을 항목: 값 으로 읽는다 (CPU 구성 한눈에 읽기)
lscpu

# CPU 마다 한 줄씩 표로 읽는다 (CPU 별로 한 줄씩 보기)
lscpu -e=열,열

# 쉼표로 나눈 값이나 JSON 으로 스크립트에 넘긴다 (스크립트에 넘길 CPU 정보)
lscpu -p=열,열
lscpu -J

# 캐시를 종류마다 한 줄로 읽는다 (캐시 크기와 구조 보기)
lscpu -C=열,열

# 프로세스가 쓸 수 있는 CPU 수를 센다 (CPU 개수 세는 법 비교)
nproc
```



## 종료 코드

> 두 명령의 매뉴얼에 종료 코드 절이 없어, 이 환경에서 잰 값은 성공 0 과 오류 1 입니다.[^no-exit]

```bash
# 0  성공
# 1  모르는 옵션이나 남는 인자처럼 호출이 잘못된 경우

# 사용할 수 있는 CPU 수를 찍고 0 으로 끝난다
nproc    # 8
echo $?    # 0

# 모르는 옵션. 2>&1 은 오류 메시지를 표준 출력에 합쳐 종료 코드와 함께 보인다
lscpu --bad 2>&1; echo $?
```

```bash
lscpu: unrecognized option '--bad'
Try 'lscpu --help' for more information.
1
```

```bash
# 남는 인자
nproc x 2>&1; echo $?
```

```bash
nproc: extra operand 'x'
Try 'nproc --help' for more information.
1
```

`lscpu -c -e` 가 출력 없이 0 으로 끝나는 예는 「온라인과 오프라인 CPU 가르기」 에 있습니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션만 씁니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 도구와 일반 사용자가 갖춰집니다.

이 시트는 파일을 따로 만들지 않고 시스템이 가진 정보를 읽습니다. 출력은 `docker run -it --rm debian:12` 로 연 컨테이너의 root 에서 받았고, 「컨테이너 CPU 제한이 보이는 곳」 의 `docker run` 은 macOS 셸에서 직접 칩니다.

```bash
# 실습 폴더. 예는 파일을 만들지 않고 시스템 정보를 읽는다
mkdir -p ~/cmd-lab/dmidecode-lscpu && cd ~/cmd-lab/dmidecode-lscpu

# lscpu·lsmem(util-linux), dmidecode, lshw 를 설치한다
# jq 는 「스크립트에 넘길 CPU 정보」 에서 쓰고,
# dmidecode·lsmem·lshw 는 DMI 표와 메모리 읽기 시트에서 쓴다
apt-get -qq update >/dev/null 2>&1; \
apt-get -qq install -y util-linux dmidecode lshw jq procps >/dev/null 2>&1

# 권한 비교에 쓸 일반 사용자 appuser. DMI 표와 메모리 읽기 시트에서 쓴다
id appuser >/dev/null 2>&1 || useradd -m appuser
```

### CPU 구성 한눈에 읽기

> 옵션 없는 `lscpu` 는 CPU 개수·구조·캐시를 `항목: 값` 으로 찍습니다.

`lscpu` 는 sysfs 와 `/proc/cpuinfo` 에서 정보를 모읍니다. 터미널에서는 보기 좋게 다듬어 찍을 수 있지만 파이프로 넘기면 항상 `항목: 값` 형식입니다.[^lscpu]

```bash
# 옵션 없이: 요약. Flags·Vulnerability 줄은 길어서 뺀다
# 읽을 줄
#   Architecture         CPU 계열. aarch64, x86 이면 x86_64
#   CPU(s)               커널이 보는 논리 CPU 수
#   On-line CPU(s) list  그중 지금 쓰는 번호 범위. 0-7 은 0번부터 7번까지 여덟 개
#   Thread(s) per core   1 이면 하이퍼스레딩 같은 코어당 여러 스레드 구조가 아니다
#   Core(s) per cluster  CPU(s) 8 은 스레드 1 에 클러스터 코어 8 을 곱한 값이다
#   Socket(s)·Model name  - 는 값이 없다는 뜻이다
# NUMA 줄은 없다. x86 서버의 Core(s) per socket·Socket(s)·NUMA node(s) 가
# 채워진 예는 책 노트의 「무엇을 쓰고 있는지 확인하는 법」 에 있다
#   grep -v   패턴에 맞는 줄을 뺀다
#   grep -E   패턴을 확장 정규식으로 읽는다
lscpu | grep -v -E '^(Flags|Vulnerability)'
```

```bash
Architecture:                            aarch64
CPU op-mode(s):                          64-bit
Byte Order:                              Little Endian
CPU(s):                                  8
On-line CPU(s) list:                     0-7
Vendor ID:                               Apple
Model name:                              -
Model:                                   0
Thread(s) per core:                      1
Core(s) per cluster:                     8
Socket(s):                               -
Cluster(s):                              1
Stepping:                                0x0
CPU(s) scaling MHz:                      100%
CPU max MHz:                             2000.0000
CPU min MHz:                             2000.0000
BogoMIPS:                                48.00
L1d cache:                               1 MiB (8 instances)
L1i cache:                               1.5 MiB (8 instances)
L2 cache:                                32 MiB (2 instances)
L3 cache:                                64 MiB (1 instance)
```

man 은 가상 환경에서는 게스트가 보는 구성이 그대로 나오고 가상 하드웨어에서는 소켓당 코어 수 등이 틀릴 수 있다고 적습니다.[^lscpu] `Flags` 줄은 CPU 가 지원하는 기능 목록이고 `Vulnerability` 줄은 취약점별 영향 여부이며, 개수와 내용이 CPU 와 커널 판마다 달라서 스크립트는 줄 번호가 아니라 항목 이름으로 고릅니다.

### CPU 별로 한 줄씩 보기

> `-e` 는 논리 CPU 마다 한 줄을 표로 찍고, 열은 `=목록` 으로 고릅니다.

```bash
# CPU 마다 한 줄. 기본 열은 CPU CLUSTER CORE 캐시 ONLINE MAXMHZ MINMHZ MHZ
# L1d:L1i:L2:L3 열은 그 CPU 가 쓰는 캐시의 번호이고, 번호가 같으면 같은 캐시다
#   -e   논리 CPU 마다 한 줄을 표로 찍는다 (--extended)
lscpu -e
```

```bash
CPU CLUSTER CORE L1d:L1i:L2:L3 ONLINE    MAXMHZ    MINMHZ       MHZ
  0       0    0 0:0:0:0          yes 2000.0000 2000.0000 2000.0000
  1       0    1 1:1:0:0          yes 2000.0000 2000.0000 2000.0000
  2       0    2 2:2:0:0          yes 2000.0000 2000.0000 2000.0000
  3       0    3 3:3:0:0          yes 2000.0000 2000.0000 2000.0000
  4       0    4 4:4:1024:0       yes 2000.0000 2000.0000 2000.0000
  5       0    5 5:5:1024:0       yes 2000.0000 2000.0000 2000.0000
  6       0    6 6:6:1024:0       yes 2000.0000 2000.0000 2000.0000
  7       0    7 7:7:1024:0       yes 2000.0000 2000.0000 2000.0000
```

0~3번은 L2 번호가 0 이라 하나를 나눠 쓰고 4~7번은 1024 라 다른 L2 를 씁니다. 이 번호는 커널이 준 ID 를 따르므로 0부터 시작하지 않을 수 있고,[^lscpu] 위 표처럼 띄엄띄엄 매겨지기도 합니다.

```bash
# 보고 싶은 열만, 적은 순서로 찍는다. 열 이름은 대소문자를 가리지 않는다
#   -e=열,열   보고 싶은 열만 고른다
#   head -3    앞 세 줄만 남긴다
lscpu -e=CPU,CORE,ONLINE,MAXMHZ | head -3
```

```bash
CPU CORE ONLINE    MAXMHZ
  0    0    yes 2000.0000
  1    1    yes 2000.0000
```

man 은 열이 모든 아키텍처에서 지원되지는 않으며 지원하지 않는 열을 적으면 열 이름만 찍고 값은 비워 둔다고 적습니다.[^lscpu] 존재하지 않는 열 이름은 `unknown column` 오류가 납니다.

```bash
# -e 와 함께 쓰는 옵션
#   -e=+열        기본 열 뒤에 열을 더한다
#   --output-all  쓸 수 있는 모든 열을 낸다
#   -y            논리 번호 대신 커널이 준 물리 ID 를 찍는다
#   -x            CPU 집합을 0-7 같은 목록 대신 ff 같은 16진 마스크로 찍는다
```

이 옵션들의 뜻은 man 의 OPTIONS 절을 옮겼습니다.[^lscpu]

### 온라인과 오프라인 CPU 가르기

> `-e` 는 온라인과 오프라인 CPU 를 모두 보이고, `-b` 와 `-c` 는 그중 한쪽만 남깁니다.

세 옵션은 `-e` 나 `-p` 와 함께만 쓸 수 있습니다.[^lscpu]

```bash
# 이 환경에는 오프라인 CPU 가 없어 -a 와 -b 의 줄 수가 같다. 헤더 한 줄과 CPU 여덟 줄이다
#   -a      온라인과 오프라인 모두. -e 의 기본이다 (--all)
#   wc -l   줄 수를 센다
lscpu -a -e | wc -l    # 9
```

```bash
# 오프라인이 없으니 줄 수가 같다
#   -b   온라인 CPU 만 남긴다 (--online)
lscpu -b -e | wc -l    # 9
```

```bash
# 오프라인이 없으면 출력이 비고 종료 코드는 0 이다
#   -c   오프라인 CPU 만 남긴다 (--offline)
# CPU 를 실제로 끄고 켜는 것은 chcpu 의 일이다
# 이 환경의 sysfs 에는 CPU 별 online 파일이 없어 -c 에 값이 나오는 모습은 받지 못했다
lscpu -c -e; echo "exit $?"    # exit 0
```

### 스크립트에 넘길 CPU 정보

> `-p` 는 쉼표로 나눈 줄을, `-J` 는 JSON 을 찍어 열 간격에 기대지 않고 파이프라인에 바로 연결합니다.

```bash
# 쉼표로 나눈 값. 앞의 # 줄은 설명과 열 이름이라 grep -v 로 거른다
# # 로 시작하는 마지막 줄이 열 이름이다
# Node 열은 이 환경에 값이 없어 비어 있고, 그 뒤 이름 없는 빈 열이 캐시 열 앞의 구분이다
#   -p       쉼표로 나눈 값으로 찍는다 (--parse)
#   head -6  앞 여섯 줄만 남긴다
lscpu -p | head -6
```

```bash
# The following is the parsable format, which can be fed to other
# programs. Each different item in every column has an unique ID
# starting usually from zero.
# CPU,Core,Cluster,Node,,L1d,L1i,L2,L3
0,0,0,,,0,0,0,0
1,1,0,,,1,1,0,0
```

열 목록을 주지 않으면 옛 버전과 호환되는 형식이라 캐시 열 묶음 앞을 쉼표 두 개로 가릅니다.[^lscpu]

```bash
# 열을 고른다. ONLINE 열은 Y 나 N 으로 나온다
#   -p=열,열   열을 고른다
lscpu -p=CPU,CORE,ONLINE | grep -v '^#' | head -3
```

```bash
0,0,Y
1,1,Y
2,2,Y
```

```bash
# CACHE 는 캐시 열 묶음(L1d·L1i·L2·L3)으로 풀려 나온다. 열 이름 줄과 앞 두 줄
#   sed -n '4,6p'   4~6째 줄만 찍는다
lscpu -p=CPU,CACHE | sed -n '4,6p'
```

```bash
# CPU,,L1d,L1i,L2,L3
0,,0,0,0,0
1,,1,1,0,0
```

man 은 목록을 주면 캐시 열 사이를 콜론으로 나눈다고 적지만 이 환경의 2.38.1 은 쉼표로 나눴습니다. 열 이름 줄을 보고 칸을 세는 것이 안전합니다.

```bash
# 헤더 # 줄을 빼고 센 CPU 개수. -p 는 온라인 CPU 만 낸다
#   grep -c   맞는 줄 수를 센다
lscpu -p | grep -vc '^#'    # 8
```

```bash
# 요약을 JSON 으로 낸다. 구조는 {"lscpu": [{"field": "항목:", "data": "값"}, ...]} 이고
# 항목 이름 끝에 콜론이 붙는다. 앞 8줄만 본다
#   -J   JSON 으로 찍는다 (--json)
lscpu -J | head -8
```

```bash
{
   "lscpu": [
      {
         "field": "Architecture:",
         "data": "aarch64"
      },{
         "field": "CPU op-mode(s):",
         "data": "64-bit"
```

```bash
# jq 로 한 항목만: 필드 이름(콜론 포함)으로 고른다
#   jq -r   문자열을 따옴표 없이 찍는다
lscpu -J | jq -r '.lscpu[] | select(.field=="CPU(s):") | .data'    # 8
```

```bash
# -J 를 -e 와 함께: CPU 별 배열은 cpus 키에 든다. 개수 세기
lscpu -J -e=CPU,ONLINE | jq '.cpus | length'    # 8
```

```bash
# 이름에 cache 가 든 항목만 뽑아 한 줄씩
lscpu -J \
  | jq -r '.lscpu[] | select(.field|test("cache")) | "\(.field) \(.data)"'
```

```bash
L1d cache: 1 MiB (8 instances)
L1i cache: 1.5 MiB (8 instances)
L2 cache: 32 MiB (2 instances)
L3 cache: 64 MiB (1 instance)
```

### 캐시 크기와 구조 보기

> `-C` 는 캐시 종류마다 한 줄을 찍고, 한 개의 크기와 전체 크기를 나눠 보여 줍니다.

man 은 캐시 크기를 모든 CPU 의 합계로 보고하며 v2.34 앞 판은 코어당 크기를 보고해 혼란스러웠다고 적습니다.[^lscpu]

```bash
# 캐시 한 줄에 하나. ONE-SIZE 는 한 개의 크기, ALL-SIZE 는 시스템 전체 합
# WAYS·SETS 칸이 빈 것은 이 환경이 값을 주지 않기 때문이다
#   -C   캐시를 종류마다 한 줄로 찍는다 (--caches)
lscpu -C
```

```bash
NAME ONE-SIZE ALL-SIZE WAYS TYPE        LEVEL SETS PHY-LINE COHERENCY-SIZE
L1d      128K       1M      Data            1                          128
L1i      192K     1.5M      Instruction     1                          128
L2        16M      32M      Unified         2                          128
L3        64M      64M      Unified         3                          128
```

L2 는 한 개가 16M 이고 전체가 32M 이므로 두 개입니다. 「CPU 별로 한 줄씩 보기」 의 `-e` 표에서 L2 번호가 0 과 1024 로 갈린 것과 맞습니다.

```bash
# 열을 고른다
#   -C=열,열   열을 고른다
lscpu -C=NAME,ONE-SIZE,ALL-SIZE,TYPE
```

```bash
NAME ONE-SIZE ALL-SIZE TYPE
L1d      128K       1M Data
L1i      192K     1.5M Instruction
L2        16M      32M Unified
L3        64M      64M Unified
```

```bash
# 사람이 읽는 K·M 대신 바이트 숫자. 계산에 넘길 때
#   -B   크기를 바이트 숫자로 찍는다 (--bytes)
lscpu -B -C=NAME,ONE-SIZE,ALL-SIZE
```

```bash
NAME ONE-SIZE ALL-SIZE
L1d    131072  1048576
L1i    196608  1572864
L2   16777216 33554432
L3   67108864 67108864
```

### CPU 개수 세는 법 비교

> `nproc`·`lscpu`·`/proc/cpuinfo` 는 같은 8 을 내지만, 프로세스가 쓸 수 있는 개수를 묻는 것은 `nproc` 하나입니다.

`nproc` 은 현재 프로세스가 쓸 수 있는 처리 장치 수를 내며 이 값은 온라인 프로세서 수보다 적을 수 있습니다.[^nproc] `/proc/cpuinfo` 는 아키텍처마다 다른 항목을 줄로 담고, `lscpu` 는 이 파일에서 정보를 모읍니다.[^cpuinfo]

```bash
# 이 프로세스가 쓸 수 있는 수, 설치된 전체, 2개를 뺀 값이 차례로 나온다
#   --all        설치된 프로세서 수를 센다
#   --ignore=N   가능하면 N 개를 뺀다
nproc; nproc --all; nproc --ignore=2
```

```bash
8
8
6
```

```bash
# /proc/cpuinfo: processor 로 시작하는 줄이 CPU 마다 하나
grep -c ^processor /proc/cpuinfo    # 8
```

```bash
# lscpu -p: 헤더를 뺀 줄 수
lscpu -p | grep -vc '^#'    # 8
```

```bash
# sysfs: 커널이 켜 둔 CPU 번호 범위
cat /sys/devices/system/cpu/online    # 0-7
```

### 프로세스에 걸린 CPU 제한

> `taskset` 으로 프로세스가 쓸 CPU 를 묶으면 `nproc` 만 줄고, `lscpu` 는 시스템 전체를 그대로 보입니다.

```bash
# 이 명령을 0·1번 CPU 에서만 돌게 묶는다. nproc 이 2 로 준다
#   taskset -c 0,1   0번과 1번 CPU 에서만 명령을 실행한다
taskset -c 0,1 nproc    # 2
```

```bash
# lscpu 는 시스템이 가진 CPU 를 세므로 제한을 반영하지 않는다 (CPU(s) 는 8, 온라인 목록은 0-7)
taskset -c 0,1 lscpu | grep -E '^(CPU\(s\):|On-line)'
```

```bash
CPU(s):                                  8
On-line CPU(s) list:                     0-7
```



## 주의사항과 동작 원리

> 예상과 다르게 동작하는 곳은 ARM 의 `/proc/cpuinfo` 와 컨테이너의 CPU 제한입니다.

### ARM cpuinfo 의 model name 부재

> CPU 모델 이름을 `/proc/cpuinfo` 의 `model name` 줄로 읽는 스크립트는 ARM 에서 빈 값을 받습니다.

x86 은 `model name` 줄을 두지만 이 `aarch64` 기기에는 그 줄이 없고 `CPU implementer` 같은 줄이 나옵니다.[^cpuinfo]

```bash
# model name 이 없으면 CPU implementer 를 대신 잡는다. 0x61 은 Apple 의 제조사 코드
#   grep -m1   첫 일치에서 멈춘다
grep -m1 -E 'model name|CPU implementer' /proc/cpuinfo
```

```bash
CPU implementer	: 0x61
```

### 컨테이너 CPU 제한이 보이는 곳

> 컨테이너에 CPU 를 제한해도 `lscpu` 는 호스트 전체를 보이고, 제한은 `--cpuset-cpus` 면 `nproc` 에, `--cpus` 면 cgroup 의 `cpu.max` 에만 보입니다.

이 예는 macOS 셸에서 `docker run` 을 직접 치고, 각 컨테이너 안에서 `nproc`·`lscpu`·cgroup 파일을 읽습니다. 두 옵션의 뜻은 Docker 문서를 따랐습니다.[^docker]

```bash
# 제한 없이: nproc 8, lscpu 8. cpu.max 의 max 는 한도 없음
#   docker run --rm   컨테이너를 띄우고 끝나면 지운다
docker run \
  --rm \
  debian:12 \
  bash -c 'nproc; lscpu | grep -E "^CPU\(s\):"; cat /sys/fs/cgroup/cpu.max'
```

```bash
8
CPU(s):                                  8
max 100000
```

```bash
# CPU 시간 2개 분량으로 제한한다. nproc 과 lscpu 는 그대로 8, 제한은 cpu.max 에만 보인다
#   --cpus 2   컨테이너가 쓸 수 있는 CPU 자원의 양
docker run \
  --rm \
  --cpus 2 \
  debian:12 \
  bash -c 'nproc; lscpu | grep -E "^CPU\(s\):"; cat /sys/fs/cgroup/cpu.max'
```

```bash
8
CPU(s):                                  8
200000 100000
```

`cpu.max` 는 `$MAX $PERIOD` 형식으로 "한 `$PERIOD` 동안 최대 `$MAX` 만큼 쓸 수 있다"는 뜻입니다.[^cgroup] `200000 100000` 은 100000 마이크로초마다 200000 마이크로초, 곧 CPU 2개 분량이라 CPU 번호를 막는 것이 아니라 시간을 자르며, 프로세스는 여덟 개를 모두 본 채 합쳐서 2개 분량만 쓰게 됩니다.

```bash
# 0·1번 CPU 에만 올린다. nproc 이 2 로 줄고 lscpu 는 여전히 8
#   --cpuset-cpus 0,1   컨테이너가 쓸 수 있는 특정 CPU 나 코어
docker run \
  --rm \
  --cpuset-cpus 0,1 \
  debian:12 \
  bash -c 'nproc; lscpu | grep -E "^CPU\(s\):"; cat /sys/fs/cgroup/cpuset.cpus.effective'
```

```bash
2
CPU(s):                                  8
0-1
```

`cpuset.cpus.effective` 는 이 cgroup 의 작업이 쓸 수 있는 활성 CPU 목록입니다.[^cgroup] `nproc` 은 프로세스의 CPU 친화도를 보므로 이 제한을 읽어 2 를 냅니다.

```bash
# 둘을 함께: cpuset 으로 4개를 열고 시간은 1.5개 분량. nproc 은 4, 시간 제한은 cpu.max
docker run \
  --rm \
  --cpus 1.5 \
  --cpuset-cpus 0-3 \
  debian:12 \
  bash -c 'nproc; cat /sys/fs/cgroup/cpu.max /sys/fs/cgroup/cpuset.cpus.effective'
```

```bash
4
150000 100000
0-3
```

컨테이너 안에서 쓸 수 있는 CPU 수는 `nproc` 으로, 쓸 수 있는 CPU 시간은 `cpu.max` 로 읽고, `lscpu` 의 `CPU(s)` 는 어느 쪽도 반영하지 않아 스레드 풀 크기의 근거로 쓰면 호스트 전체 개수를 따라갑니다. 위 출력은 cgroup v2 를 쓰는 환경 기준이고 cgroup v1 은 파일 이름이 다릅니다.



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [dmidecode·lsmem·lshw DMI 표와 메모리 읽기 시트](./dmidecode·lscpu%20DMI%20표와%20메모리%20읽기.md) — 펌웨어 DMI 표를 읽는 `dmidecode` 와 메모리를 읽는 `lsmem`·`lshw`
- [무엇을 쓰고 있는지 확인하는 법](../../../book/learning-modern-linux/02-01.%EC%BB%A4%EB%84%90%EC%9D%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%ED%95%98%EC%A7%80%EB%A7%8C%20%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EB%8A%94%20%EC%95%84%EB%8B%88%EB%8B%A4.md#무엇을-쓰고-있는지-확인하는-법) — CPU 계열을 `lscpu` 로 읽는 이유와 x86 출력 예
- [uname·os-release·lsb_release 참조 시트](./uname%C2%B7os-release%C2%B7hostnamectl.md) — 커널과 배포판 이름·버전을 읽는 시트



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- util-linux 2.38.1 의 `lscpu --help`·`man lscpu` 원문 — Debian 12 컨테이너에서 2026-11-11 확인
- GNU coreutils 9.1 의 `nproc --help` 원문 — Debian 12 컨테이너에서 2026-11-11 확인
- [lscpu(1) — Debian bookworm](https://manpages.debian.org/bookworm/util-linux/lscpu.1.en.html), [nproc(1)](https://manpages.debian.org/bookworm/coreutils/nproc.1.en.html)
- [proc(5) — Debian bookworm](https://manpages.debian.org/bookworm/manpages/proc.5.en.html)
- [Resource constraints — Docker Docs](https://docs.docker.com/engine/containers/resource_constraints/)
- [Control Group v2 — The Linux Kernel documentation](https://docs.kernel.org/admin-guide/cgroup-v2.html)

[^no-exit]: `man lscpu` (util-linux 2.38.1) 의 절은 "NAME", "SYNOPSIS", "DESCRIPTION", "OPTIONS", "BUGS", "AUTHORS", "SEE ALSO", "REPORTING BUGS", "AVAILABILITY" 이고, `man nproc` (coreutils 9.1) 의 절은 "NAME", "SYNOPSIS", "DESCRIPTION", "AUTHOR", "REPORTING BUGS", "COPYRIGHT", "SEE ALSO" 라서 두 매뉴얼 모두 EXIT STATUS 절이 없습니다. https://manpages.debian.org/bookworm/util-linux/lscpu.1.en.html https://manpages.debian.org/bookworm/coreutils/nproc.1.en.html
[^lscpu]: `man lscpu` (util-linux 2.38.1) — "lscpu gathers CPU architecture information from sysfs, /proc/cpuinfo and any applicable architecture-specific libraries", "The default output formatting on terminal is subject to change and maybe optimized for better readability.", "The output for non-terminals (e.g., pipes) is never affected by this optimization and it is always in "Field: data\n" format.", "In virtualized environments, the CPU architecture information displayed reflects the configuration of the guest operating system which is typically different from the physical (host) system.", "On virtual hardware the number of cores per socket, etc. can be wrong.", "The column labels are not case sensitive.", "Not all columns are supported on all architectures. If an unsupported column is specified, lscpu prints the column but does not provide any data for it.", "The cache sizes are reported as summary from all CPUs. The versions before v2.34 reported per-core sizes", "Since version v2.37 lscpu follows cache IDs as provided by Linux kernel and it does not always start from zero."; OPTIONS `-a` "Include lines for online and offline CPUs in the output (default for -e).", `-b` "Limit the output to online CPUs (default for -p).", `-c` "Limit the output to offline CPUs.", "This option may only be specified together with option -e or -p.", `-e` "Display the CPU information in human-readable format.", `-J` "Use JSON output format for the default summary or extended output", `-p` "If the list argument is omitted, the command output is compatible with earlier versions of lscpu. In this compatible format, two commas are used to separate CPU cache columns.", `-B` "Print the sizes in bytes rather than in a human-readable format.", `-x` "Use hexadecimal masks for CPU sets (for example "ff").", `-y` "Display physical IDs for all columns with topology elements", `--output-all` "Output all available columns." https://manpages.debian.org/bookworm/util-linux/lscpu.1.en.html
[^nproc]: `nproc --help` (GNU coreutils 9.1) — "Print the number of processing units available to the current process, which may be less than the number of online processors", "--all      print the number of installed processors", "--ignore=N  if possible, exclude N processing units". https://manpages.debian.org/bookworm/coreutils/nproc.1.en.html
[^cpuinfo]: `man 5 proc` (Linux man-pages 6.03) — /proc/cpuinfo "This is a collection of CPU and system architecture dependent items, for each supported architecture a different list.", "The lscpu(1) command gathers its information from this file."; /proc/meminfo "It is used by free(1) to report the amount of free and used memory (both physical and swap) on the system". https://manpages.debian.org/bookworm/manpages/proc.5.en.html
[^docker]: Docker Docs, Resource constraints — `--cpus` "Specify how much of the available CPU resources a container can use.", `--cpuset-cpus` "Limit the specific CPUs or cores a container can use.", `--cpu-period` "Defaults to 100000 microseconds (100 milliseconds)." https://docs.docker.com/engine/containers/resource_constraints/
[^cgroup]: Linux kernel documentation, Control Group v2 — cpu.max "which indicates that the group may consume up to $MAX in each $PERIOD duration. "max" for $MAX indicates no limit.", cpuset.cpus.effective "It lists the active CPUs available to tasks in this cgroup." https://docs.kernel.org/admin-guide/cgroup-v2.html
