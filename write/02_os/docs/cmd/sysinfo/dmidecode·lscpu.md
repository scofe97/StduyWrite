---
title: dmidecode·lscpu 참조 시트
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
  - ../../../book/learning-modern-linux/02-01.%EC%BB%A4%EB%84%90%EC%9D%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%ED%95%98%EC%A7%80%EB%A7%8C%20%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EB%8A%94%20%EC%95%84%EB%8B%88%EB%8B%A4.md
  - ./uname%C2%B7os-release%C2%B7hostnamectl.md
updated: 2026-11-11
---

# dmidecode·lscpu 참조 시트

---

> CPU 구성을 읽는 `lscpu` 와 `nproc`, 펌웨어가 적어 둔 제조사·모델·메모리 슬롯 정보를 읽는 `dmidecode` 의 옵션을, 이 기기에서 실제로 받은 출력과 함께 모았습니다.

## 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 도구와 일반 사용자가 갖춰집니다.

macOS 에는 `lscpu`·`dmidecode`·`nproc` 이 기본으로 없어서 Linux 에서 실행합니다. 이 시트의 출력은 `docker run -it --rm debian:12` 로 연 컨테이너에서 root 로 받았습니다. 도구 판은 util-linux 2.38.1, coreutils 9.1, dmidecode 3.4 입니다. 6절은 컨테이너를 띄우는 옵션을 다루므로 macOS 셸에서 `docker run` 을 직접 칩니다. 8절 일부는 OrbStack 의 `ubuntu` Linux VM(arm64)에서 받았고 그 자리에 적었습니다.

```bash
mkdir -p ~/cmd-lab/dmidecode-lscpu && cd ~/cmd-lab/dmidecode-lscpu
apt-get -qq update >/dev/null 2>&1; apt-get -qq install -y util-linux dmidecode lshw jq procps >/dev/null 2>&1
id appuser >/dev/null 2>&1 || useradd -m appuser
```

이 블록은 도구를 설치하고 권한 비교에 쓸 일반 사용자 `appuser` 를 만듭니다. 이 시트는 파일을 따로 만들지 않고 시스템이 가진 정보를 읽습니다.

출력은 Apple Silicon 맥 위의 가상 환경에서 받았습니다. 그래서 CPU 는 `aarch64` 이고 물리 서버나 x86 가상 머신에서는 값과 줄이 다릅니다. 이 기기에서 값이 없거나 다른 자리는 본문에서 짚습니다.



## 1. CPU 구성 한눈에 읽기

> 옵션 없는 `lscpu` 는 CPU 개수·구조·캐시를 `항목: 값` 으로 찍습니다. 읽을 줄은 CPU(s), 온라인 목록, 스레드·코어·소켓 수입니다.

`lscpu` 는 sysfs 와 `/proc/cpuinfo` 에서 정보를 모읍니다. 터미널에서는 보기 좋게 다듬어 찍을 수 있지만 파이프로 넘기면 항상 `항목: 값` 형식입니다.[^lscpu] 아래는 긴 `Flags` 줄과 `Vulnerability` 줄을 뺀 출력입니다.

```bash
# 옵션 없이: 요약. Flags·Vulnerability 줄은 길어서 뺀다
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

- `Architecture` 는 CPU 계열(`aarch64`, x86 이면 `x86_64`)입니다.
- `CPU(s)` 는 커널이 보는 논리 CPU 수이고 `On-line CPU(s) list` 는 그중 지금 쓰는 번호 범위입니다. 여기서는 0번부터 7번까지 여덟 개입니다.
- `Thread(s) per core` 가 1 이면 하이퍼스레딩 같은 코어 하나당 스레드 여러 개 구조가 아닙니다. 이 기기의 `CPU(s)` 8 은 스레드 1 에 클러스터 코어 8 을 곱한 값입니다.
- `Socket(s)` 와 `Model name` 이 `-` 인 것은 값이 없다는 뜻입니다. man 은 가상 환경에서는 게스트가 보는 구성이 그대로 나오고 가상 하드웨어에서는 소켓당 코어 수 등이 틀릴 수 있다고 적습니다.[^lscpu]
- 이 출력에는 NUMA 줄이 없습니다. x86 서버의 `Core(s) per socket`·`Socket(s)`·`NUMA node(s)` 가 값으로 채워진 예는 책 노트의 「무엇을 쓰고 있는지 확인하는 법」에 있습니다.



`Flags` 줄은 CPU 가 지원하는 기능 목록이고 `Vulnerability` 줄은 취약점별 영향 여부이며 둘 다 한 줄이 깁니다. 이 줄들의 개수와 내용은 CPU 와 커널 판마다 달라서 스크립트는 줄 번호가 아니라 항목 이름으로 고릅니다.



## 2. CPU 별로 한 줄씩 보기

> `-e` 는 논리 CPU 마다 한 줄을 표로 찍습니다. 열은 `=목록` 으로 고르고, 온라인·오프라인 필터와 물리 ID 옵션이 따라옵니다.

```bash
# -e (--extended): CPU 마다 한 줄. 기본 열은 CPU CLUSTER CORE 캐시 ONLINE MAXMHZ MINMHZ MHZ
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

`L1d:L1i:L2:L3` 열은 그 CPU 가 쓰는 캐시의 번호입니다. 번호가 같으면 같은 캐시를 공유합니다. 0~3번은 L2 번호가 0 이라 하나를 나눠 쓰고 4~7번은 1024 라 다른 L2 를 씁니다. 이 번호는 커널이 준 ID 를 따르므로 0부터 시작하지 않을 수 있고,[^lscpu] 위 표처럼 띄엄띄엄 매겨지기도 합니다.

```bash
# -e=열,열: 보고 싶은 열만, 적은 순서로. 열 이름은 대소문자를 가리지 않는다
lscpu -e=CPU,CORE,ONLINE,MAXMHZ | head -3
```

```bash
CPU CORE ONLINE    MAXMHZ
  0    0    yes 2000.0000
  1    1    yes 2000.0000
```



man 은 열이 모든 아키텍처에서 지원되지는 않으며 지원하지 않는 열을 적으면 열 이름만 찍고 값은 비워 둔다고 적습니다.[^lscpu] 존재하지 않는 열 이름은 `unknown column` 오류가 납니다.

그 밖의 옵션도 `-e` 와 함께 씁니다. `-e=+열` 은 기본 열 뒤에 열을 더하고 `--output-all` 은 쓸 수 있는 모든 열을 냅니다.

`-y` 는 논리 번호 대신 커널이 준 물리 ID 를 찍습니다. `-x` 는 CPU 집합을 `0-7` 같은 목록 대신 `ff` 같은 16진 마스크로 찍습니다.[^lscpu]

### 온라인과 오프라인 CPU 가르기

`-e` 는 기본으로 온라인과 오프라인 CPU 를 모두 보입니다(`-a`). `-b` 는 온라인만, `-c` 는 오프라인만 남깁니다. 세 옵션은 `-e` 나 `-p` 와 함께만 쓸 수 있습니다.[^lscpu] 이 환경에는 오프라인 CPU 가 없어서 `-a` 와 `-b` 의 줄 수가 같고(헤더 한 줄과 CPU 여덟 줄), `-c` 는 아무것도 찍지 않습니다.

```bash
# -a (--all): 온라인과 오프라인 모두 (-e 의 기본). 헤더 포함 줄 수
lscpu -a -e | wc -l    # 9
```

```bash
# -b (--online): 온라인만. 오프라인이 없으니 같다
lscpu -b -e | wc -l    # 9
```

```bash
# -c (--offline): 오프라인만. 없으면 출력이 비고 종료 코드는 0 이다
lscpu -c -e; echo "exit $?"    # exit 0
```

CPU 를 실제로 끄고 켜는 것은 `chcpu` 의 일입니다. 이 환경의 sysfs 에는 CPU 별 `online` 파일이 없어 `-c` 에 값이 나오는 모습은 받지 못했습니다.





## 3. 스크립트에 넘길 CPU 정보

> `-p` 는 쉼표로 나눈 줄을, `-J` 는 JSON 을 찍습니다. 열 간격에 기대지 않으므로 파이프라인에 바로 연결합니다.

```bash
# -p (--parse): 쉼표로 나눈 값. 앞의 # 줄은 설명과 열 이름이라 grep -v 로 거른다
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

`#` 로 시작하는 마지막 줄이 열 이름입니다. `Node` 열은 이 환경에 값이 없어 비어 있고 그 뒤의 이름 없는 빈 열이 캐시 열 앞의 구분입니다. 열 목록을 주지 않으면 옛 버전과 호환되는 형식이라 캐시 열 묶음 앞을 쉼표 두 개로 가릅니다.[^lscpu]


```bash
# -p=열,열: 열을 고른다. ONLINE 열은 Y 나 N 으로 나온다
lscpu -p=CPU,CORE,ONLINE | grep -v '^#' | head -3
```

```bash
0,0,Y
1,1,Y
2,2,Y
```

```bash
# -p=CPU,CACHE: CACHE 는 캐시 열 묶음(L1d·L1i·L2·L3)으로 풀려 나온다. 열 이름 줄과 앞 두 줄
lscpu -p=CPU,CACHE | sed -n '4,6p'
```

```bash
# CPU,,L1d,L1i,L2,L3
0,,0,0,0,0
1,,1,1,0,0
```

man 은 목록을 주면 캐시 열 사이를 콜론으로 나눈다고 적지만 이 환경의 2.38.1 은 쉼표로 나눴습니다. 열 이름 줄을 보고 칸을 세는 것이 안전합니다. CPU 개수는 헤더를 뺀 줄 수로 셉니다.

```bash
# 헤더 # 줄을 빼고 센 CPU 개수. -p 는 온라인 CPU 만 낸다
lscpu -p | grep -vc '^#'    # 8
```

`-J` 는 `{"lscpu": [{"field": "항목:", "data": "값"}, ...]}` 구조의 JSON 입니다. 항목 이름 끝에 콜론이 붙어 있는 점에 주의합니다.

```bash
# -J (--json): 요약을 JSON 으로. 앞 8줄만
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
lscpu -J | jq -r '.lscpu[] | select(.field=="CPU(s):") | .data'    # 8
```

```bash
# -J 를 -e 와 함께: CPU 별 배열은 cpus 키에 든다. 개수 세기
lscpu -J -e=CPU,ONLINE | jq '.cpus | length'    # 8
```

```bash
# 이름에 cache 가 든 항목만 뽑아 한 줄씩
lscpu -J | jq -r '.lscpu[] | select(.field|test("cache")) | "\(.field) \(.data)"'
```

```bash
L1d cache: 1 MiB (8 instances)
L1i cache: 1.5 MiB (8 instances)
L2 cache: 32 MiB (2 instances)
L3 cache: 64 MiB (1 instance)
```



## 4. 캐시 크기와 구조 보기

> `-C` 는 캐시 종류마다 한 줄을 찍습니다. 한 개의 크기와 전체 크기를 나눠 보여 줘서 코어가 나눠 쓰는 캐시를 구분합니다.

man 은 캐시 크기를 모든 CPU 의 합계로 보고하며 v2.34 앞 판은 코어당 크기를 보고해 혼란스러웠다고 적습니다.[^lscpu]

```bash
# -C (--caches): 캐시 한 줄에 하나. ONE-SIZE 는 한 개의 크기, ALL-SIZE 는 시스템 전체 합
lscpu -C
```

```bash
NAME ONE-SIZE ALL-SIZE WAYS TYPE        LEVEL SETS PHY-LINE COHERENCY-SIZE
L1d      128K       1M      Data            1                          128
L1i      192K     1.5M      Instruction     1                          128
L2        16M      32M      Unified         2                          128
L3        64M      64M      Unified         3                          128
```

L2 는 한 개가 16M 이고 전체가 32M 이므로 두 개입니다. 위 2절의 `-e` 표에서 L2 번호가 0 과 1024 로 갈린 것과 맞습니다. `WAYS`·`SETS` 칸이 빈 것은 이 환경이 값을 주지 않기 때문입니다.

```bash
# -C=열,열: 열을 고른다
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
# -B (--bytes): 사람이 읽는 K·M 대신 바이트 숫자. 계산에 넘길 때
lscpu -B -C=NAME,ONE-SIZE,ALL-SIZE
```

```bash
NAME ONE-SIZE ALL-SIZE
L1d    131072  1048576
L1i    196608  1572864
L2   16777216 33554432
L3   67108864 67108864
```




## 5. CPU 개수 세는 법 비교

> `nproc`·`lscpu`·`/proc/cpuinfo` 는 같은 8 을 내지만, 프로세스가 쓸 수 있는 개수를 묻는 것은 `nproc` 하나입니다.

세 도구는 묻는 것이 다릅니다. `nproc` 은 현재 프로세스가 쓸 수 있는 처리 장치 수를 냅니다. 이 값은 온라인 프로세서 수보다 적을 수 있고 `--all` 은 설치된 프로세서 수를 냅니다.[^nproc]

`/proc/cpuinfo` 는 아키텍처마다 다른 항목을 줄로 담습니다. `lscpu` 는 이 파일에서 정보를 모읍니다.[^cpuinfo]

```bash
# nproc: 이 프로세스가 쓸 수 있는 수. --all 은 설치된 전체. --ignore=N 은 N 개를 뺀 값
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

CPU 모델 이름을 `/proc/cpuinfo` 에서 읽을 때도 아키텍처 차이가 드러납니다. x86 은 `model name` 줄을 두지만 이 `aarch64` 기기에는 그 줄이 없고 `CPU implementer` 같은 줄이 나옵니다. 스크립트에서 `model name` 을 grep 하면 ARM 에서는 빈 값입니다.

```bash
# model name 이 없으면 CPU implementer 를 대신 잡는다. 0x61 은 Apple 의 제조사 코드
grep -m1 -E 'model name|CPU implementer' /proc/cpuinfo
```

```bash
CPU implementer	: 0x61
```

### 프로세스에 걸린 CPU 제한

`taskset` 으로 프로세스가 쓸 CPU 를 0번과 1번으로 묶으면 `nproc` 만 2 로 줍니다. `lscpu` 는 시스템이 가진 CPU 를 세므로 그대로 8 을 보입니다.

```bash
# taskset -c 0,1: 이 명령을 0·1번 CPU 에서만 돌게 묶는다. nproc 이 2 로 준다
taskset -c 0,1 nproc    # 2
```


```bash
# lscpu 는 제한을 반영하지 않는다 (CPU(s) 는 8, 온라인 목록은 0-7)
taskset -c 0,1 lscpu | grep -E '^(CPU\(s\):|On-line)'
```

```bash
CPU(s):                                  8
On-line CPU(s) list:                     0-7
```




## 6. 컨테이너 CPU 제한이 보이는 곳

> 컨테이너에 CPU 를 제한해도 `lscpu` 는 호스트 전체를 보입니다. 제한은 `--cpuset-cpus` 면 `nproc` 에, `--cpus` 면 cgroup 의 `cpu.max` 에만 보입니다.

이 절은 macOS 셸에서 `docker run` 을 직접 칩니다. 각 컨테이너 안에서 `nproc`·`lscpu`·cgroup 파일을 읽습니다. Docker 는 `--cpus` 를 "컨테이너가 쓸 수 있는 CPU 자원의 양", `--cpuset-cpus` 를 "컨테이너가 쓸 수 있는 특정 CPU 나 코어"로 설명합니다.[^docker]

```bash
# 제한 없이: nproc 8, lscpu 8. cpu.max 의 max 는 한도 없음
docker run --rm debian:12 bash -c 'nproc; lscpu | grep -E "^CPU\(s\):"; cat /sys/fs/cgroup/cpu.max'
```

```bash
8
CPU(s):                                  8
max 100000
```

```bash
# --cpus 2: CPU 시간 2개 분량으로 제한. nproc 과 lscpu 는 그대로 8, 제한은 cpu.max 에만 보인다
docker run --rm --cpus 2 debian:12 bash -c 'nproc; lscpu | grep -E "^CPU\(s\):"; cat /sys/fs/cgroup/cpu.max'
```

```bash
8
CPU(s):                                  8
200000 100000
```

`cpu.max` 는 `$MAX $PERIOD` 형식으로 "한 `$PERIOD` 동안 최대 `$MAX` 만큼 쓸 수 있다"는 뜻입니다.[^cgroup] `200000 100000` 은 100000 마이크로초마다 200000 마이크로초, 곧 CPU 2개 분량입니다. 이 제한은 CPU 번호를 막는 것이 아니라 시간을 자르는 것이라, 프로세스는 여덟 개를 모두 본 채 합쳐서 2개 분량만 쓰게 됩니다.

```bash
# --cpuset-cpus 0,1: 0·1번 CPU 에만 올린다. nproc 이 2 로 줄고 lscpu 는 여전히 8
docker run --rm --cpuset-cpus 0,1 debian:12 bash -c 'nproc; lscpu | grep -E "^CPU\(s\):"; cat /sys/fs/cgroup/cpuset.cpus.effective'
```

```bash
2
CPU(s):                                  8
0-1
```

`cpuset.cpus.effective` 는 이 cgroup 의 작업이 쓸 수 있는 활성 CPU 목록입니다.[^cgroup] `nproc` 은 프로세스의 CPU 친화도를 보므로 이 제한을 읽어 2 를 냅니다.

```bash
# 둘을 함께: cpuset 으로 4개를 열고 시간은 1.5개 분량. nproc 은 4, 시간 제한은 cpu.max
docker run --rm --cpus 1.5 --cpuset-cpus 0-3 debian:12 bash -c 'nproc; cat /sys/fs/cgroup/cpu.max /sys/fs/cgroup/cpuset.cpus.effective'
```

```bash
4
150000 100000
0-3
```

정리하면 컨테이너 안에서 "쓸 수 있는 CPU 수"는 `nproc` 으로, "쓸 수 있는 CPU 시간"은 `cpu.max` 로 읽습니다. `lscpu` 의 `CPU(s)` 는 어느 쪽도 반영하지 않으므로 스레드 풀 크기를 정하는 근거로 쓰면 호스트 전체 개수를 따라가게 됩니다. 위 출력은 cgroup v2 를 쓰는 환경 기준이고 cgroup v1 은 파일 이름이 다릅니다.



## 7. 제조사·모델·BIOS 정보 읽기 (dmidecode)

> `dmidecode` 는 펌웨어가 적어 둔 DMI(SMBIOS) 표를 읽어 서버 모델·시리얼·메모리 슬롯을 찍습니다. 표가 없는 환경에서는 같은 한 줄 메시지만 나옵니다.

`dmidecode` 는 컴퓨터의 DMI 표 내용을 사람이 읽는 형식으로 보여 주는 도구입니다. 표에는 하드웨어 구성, 시리얼 번호, BIOS 판 같은 정보가 있습니다.

하드웨어를 직접 조사하지 않고 얻으므로 빠르고 안전하지만 정보가 틀릴 수 있다고 man 은 적습니다.[^dmi] 실행하면 sysfs 에서 표를 먼저 읽고 실패하면 메모리에서 직접 읽으려 합니다.

이 시트의 실행 환경(Apple Silicon 위 컨테이너)에는 그 표가 없습니다. 아래 모든 출력은 그 환경에서 실제로 받은 것이고 서버나 x86 가상 머신에서는 표의 내용이 나옵니다.

```bash
# -V (--version): 판 확인
dmidecode --version    # 3.4
```

```bash
# -t system: 시스템 정보(type 1 등). 표가 없으면 이 두 줄이 전부다
dmidecode -t system; echo "exit $?"
```

```bash
# dmidecode 3.4
# No SMBIOS nor DMI entry point found, sorry.
exit 0
```

두 가지를 짚습니다. 메시지는 "SMBIOS 나 DMI 진입점을 찾지 못했다"입니다. 그런데 종료 코드는 0 이라서, 스크립트가 종료 코드로 성공을 판단하면 표가 없는 것을 놓칩니다. 출력이 비었는지를 같이 봅니다.

### 읽는 곳과 root 권한

man 의 FILES 절은 읽는 곳을 세 경로로 적습니다. `/sys/firmware/dmi/tables/` 아래 `smbios_entry_point` 와 `DMI` 는 Linux 가 sysfs 로 내보내는 표입니다. `/dev/mem` 은 sysfs 가 안 될 때 쓰는 물리 메모리 장치입니다.[^dmi][^devmem]

man 은 `-s` 로 읽는 문자열 대부분을 `/sys/devices/virtual/dmi/id` 의 파일에서도 읽을 수 있고 그 파일 대부분은 일반 사용자도 읽는다고 따로 적습니다. 표 전체를 읽는 경로에는 그런 말이 없습니다. `/dev/mem` 은 보통 `root:kmem` 소유로 만듭니다.[^devmem] 그래서 표 전체를 보려면 root 로 실행하는 것이 보통입니다.

이 기기에는 `/sys/firmware/dmi` 도 `/dev/mem` 도 없어서 권한 오류를 직접 재현하지 못했습니다. 일반 사용자 `appuser` 로 돌려도 root 와 같은 메시지가 나옵니다.

```bash
# appuser 로 실행해도 같다: 읽을 표 자체가 없어서 권한 단계까지 가지 않는다
su appuser -c 'dmidecode -t system; echo "exit $?"'
```

```bash
# dmidecode 3.4
# No SMBIOS nor DMI entry point found, sorry.
exit 0
```

### 종류로 고르기 (-t)

`-t` 는 DMI 종류(type) 번호나 키워드로 항목을 고릅니다. 번호는 쉼표로 여러 개를 줄 수 있지만 키워드는 쉼표로 묶을 수 없습니다. `-t` 를 여러 번 주면 합집합입니다.[^dmi-opt] 키워드는 대소문자를 가리지 않고 번호 목록의 별칭입니다.[^dmi-opt]

| 키워드 | 종류 번호 |
|--------|----------|
| `bios` | 0, 13 |
| `system` | 1, 12, 15, 23, 32 |
| `baseboard` | 2, 10, 41 |
| `chassis` | 3 |
| `processor` | 4 |
| `memory` | 5, 6, 16, 17 |
| `cache` | 7 |
| `connector` | 8 |
| `slot` | 9 |

```bash
# -t 4,17: 번호 목록. 4 는 Processor, 17 은 Memory Device. 표가 없으니 같은 메시지다
dmidecode -t 4,17; echo "exit $?"
```

```bash
# dmidecode 3.4
# No SMBIOS nor DMI entry point found, sorry.
exit 0
```

```bash
# 키워드 아홉 개를 하나씩 돌려 마지막 줄을 센다. 표가 없으니 전부 같은 줄이다
for t in bios system baseboard chassis processor memory cache connector slot; do dmidecode -t $t | tail -1; done | sort | uniq -c
```

```bash
      9 # No SMBIOS nor DMI entry point found, sorry.
```

```bash
# 키워드를 쉼표로 묶으면 오류와 종료 코드 2. 번호만 쉼표로 묶을 수 있다
# head 가 파이프를 먼저 닫으면 141(SIGPIPE)이 나올 수 있어 종료 코드는 따로 받는다
dmidecode -t memory,processor 2>&1 | head -3
dmidecode -t memory,processor >/dev/null 2>&1; echo "exit $?"
```

```bash
Invalid type keyword: memory,processor
Valid type keywords are:
  bios
exit 2
```


표가 있는 장비에서 `-t memory` 는 메모리 컨트롤러·모듈·물리 메모리 배열·메모리 장치(type 5, 6, 16, 17) 레코드를 찍습니다. 레코드는 `Handle 0x…, DMI type …, … bytes.` 로 시작하고 그 아래 항목이 `이름: 값` 줄로 이어집니다.[^dmi] 슬롯 하나가 레코드 하나로 나오는지, 빈 슬롯이 어떻게 적히는지는 펌웨어마다 다릅니다.

### 값 하나만 뽑기 (-s)

`-s` 는 키워드로 지정한 DMI 문자열 한 개만 찍어 스크립트에 편합니다. 키워드는 `system-product-name`, `system-serial-number`, `bios-version` 처럼 종류와 항목이 붙은 이름입니다. 모든 장비가 모든 문자열을 갖지는 않습니다.

`-s` 는 한 번만 쓸 수 있고 `-t`·`--dump-bin`·`--oem-string` 과 함께 쓰지 못합니다.[^dmi-opt] 키워드 전체 목록은 값 없이 `dmidecode -s` 를 치면 나옵니다.

```bash
# -s system-product-name: 모델 이름 한 줄. 표가 없으면 아무것도 찍지 않아 0바이트다
dmidecode -s system-product-name | wc -c    # 0
```

```bash
# -s 에 값을 안 주면 키워드 목록을 찍고 종료 코드 2. 종료 코드는 위처럼 따로 받는다
dmidecode -s 2>&1 | head -4
dmidecode -s >/dev/null 2>&1; echo "exit $?"
```

```bash
dmidecode: option requires an argument -- 's'
String keyword expected
Valid string keywords are:
  bios-vendor
exit 2
```

위 첫 예에서 `-s` 는 오류 없이 빈 출력과 종료 코드 0 으로 끝났습니다. 그래서 `model=$(dmidecode -s system-product-name)` 은 이런 환경에서 빈 문자열이 되고 스크립트는 빈 값을 따로 검사해야 합니다.

### 출력 모양 바꾸기 (-q)

```bash
# -q (--quiet): 알 수 없거나 비활성이거나 OEM 전용인 항목, 메타데이터, 핸들 참조를 숨긴다. 표가 없으면 안내 줄도 사라진다
dmidecode -q -t memory | wc -l    # 0
```

`-u` 는 해독하지 않고 16진수로 찍고 디버깅에 씁니다. `-H 핸들` 은 핸들 번호 하나의 항목만 찍습니다. 이 기기에서는 두 옵션도 `-t system` 과 같은 두 줄 메시지만 나왔습니다.[^dmi-opt]



`--oem-string N` 은 제조사가 넣은 OEM 문자열 N 번째 값을 찍고 `count` 를 주면 개수를 찍습니다. 이 기기에서는 출력이 비어 있었습니다.

### 표를 파일로 떠서 다른 곳에서 읽기

`--dump-bin 파일` 은 표를 해독하지 않고 이진 파일로 저장하고 `--from-dump 파일` 은 그 파일에서 읽습니다. 다른 장비에서 뜬 표를 내 기기에서 읽을 때 씁니다. `-d 파일` 은 `/dev/mem` 대신 읽을 장치 파일을, `--no-sysfs` 는 sysfs 를 건너뛰고 메모리에서 읽게 하는 옵션입니다.[^dmi-opt]

```bash
# --dump-bin: 읽을 표가 없으면 파일도 만들어지지 않는다
dmidecode --dump-bin dmi.bin; echo "exit $?"; ls dmi.bin 2>&1
```

```bash
# dmidecode 3.4
# No SMBIOS nor DMI entry point found, sorry.
exit 0
ls: cannot access 'dmi.bin': No such file or directory
```

```bash
# --from-dump: 파일을 못 열면 종료 코드 1
dmidecode --from-dump nofile.bin; echo "exit $?"
```

```bash
# dmidecode 3.4
Reading SMBIOS/DMI data from file nofile.bin.
nofile.bin: No such file or directory
exit 1
```

### 표를 믿는 데 쓰는 주의

man 은 DMI 표 정보가 "대개 부정확하거나 불완전하거나 그냥 틀렸다"고 적습니다.[^bugs] 슬롯 수나 최대 용량처럼 구성 가능한 상한은 펌웨어가 적은 값이라, 실제 꽂힌 장치 수와 다를 수 있습니다. 표를 근거로 장비를 판단하기 전에 `lscpu`·`free` 같은 커널이 직접 센 값과 맞춰 봅니다.



## 8. DMI 표가 없을 때 대신 볼 곳

> DMI 표는 펌웨어가 넘겨주는 것이라, 표를 받지 못한 환경에서는 `dmidecode` 가 읽을 것이 없습니다. 그때 이 기기에서 값이 나온 도구는 `lscpu`·`lshw -short`·`/proc/meminfo` 입니다.

이 시트를 만든 기기에서는 컨테이너와 OrbStack VM 모두 DMI 표가 없었습니다. `/sys/devices/virtual/dmi/id`·`/sys/firmware/dmi` 가 없고 `/dev/mem` 도 없습니다.

```bash
# 컨테이너: DMI sysfs 와 /dev/mem 이 모두 없다
ls /sys/devices/virtual/dmi/id /sys/firmware/dmi /dev/mem 2>&1
```

```bash
ls: cannot access '/sys/devices/virtual/dmi/id': No such file or directory
ls: cannot access '/sys/firmware/dmi': No such file or directory
ls: cannot access '/dev/mem': No such file or directory
```

OrbStack 의 `ubuntu` VM(arm64, Ubuntu 26.04)에서도 같았습니다. `/sys/firmware` 에는 DMI 대신 `devicetree` 가 있었고 `compatible` 값은 `orbstack,virt` 입니다. `efi` 디렉터리도 없었습니다. Linux 커널 문서는 UEFI 규격을 따르는 펌웨어로 부팅하면 SMBIOS 같은 설정 정보를 UEFI 설정 표로 받을 수 있다고 적습니다.[^uefi] 그래서 같은 ARM 이라도 UEFI 로 부팅한 장비에서는 표가 나올 수 있습니다.

이 VM 은 외부 이름 풀이가 막혀 `dmidecode` 를 설치하지 못했습니다. 그래서 VM 안의 `dmidecode` 출력은 받지 못했고 아래 두 블록은 VM 에서 받은 sysfs 조회입니다.

```bash
# OrbStack VM: DMI 는 없고 devicetree 가 있다 (fdt 도 함께)
ls /sys/devices/virtual/dmi /sys/firmware/dmi 2>&1; ls /sys/firmware
```

```bash
ls: cannot access '/sys/devices/virtual/dmi': No such file or directory
ls: cannot access '/sys/firmware/dmi': No such file or directory
devicetree
fdt
```

```bash
# OrbStack VM: 장치 트리의 compatible. NUL 로 끝나는 문자열이라 tr 로 공백으로 바꾼다
tr '\0' ' ' < /sys/firmware/devicetree/base/compatible; echo
```

```bash
orbstack,virt 
```

man 은 `/sys/devices/virtual/dmi/id` 아래 파일 대부분을 일반 사용자도 읽는다고 적습니다(7절). 이 경로의 `product_name` 을 먼저 읽고 없으면 대체 메시지를 내는 식으로 짭니다.

```bash
# 파일이 없으면 대체 문구. 일반 사용자도 돌릴 수 있다
cat /sys/devices/virtual/dmi/id/product_name 2>/dev/null || echo "DMI 없음"
```

```bash
DMI 없음
```

### lsmem

`lsmem` 은 메모리 범위와 온라인 상태를 sysfs 의 메모리 블록에서 읽습니다.[^lsmem] 이 환경에는 그 sysfs 가 없어 실패합니다.

```bash
# lsmem: /sys/devices/system/memory 를 읽는다. 이 환경에는 없다
lsmem; echo "exit $?"
```

```bash
lsmem: cannot open /sys/devices/system/memory: No such file or directory
exit 1
```

### lshw

`lshw` 는 하드웨어 구성을 트리로 보여 주는 도구입니다. man 은 lshw 의 DMI 지원을 x86·IA-64 전용으로 적습니다.[^lshw] 이 환경에서도 `-short` 는 CPU 개수와 메모리 크기를 찍지만 CPU 모델 이름은 비어 있습니다. 출력 줄 수가 긴 편이라 앞 12줄만 봅니다.

```bash
# -short: 하드웨어 경로·종류·설명을 한 줄씩. 메모리 8004MiB 와 processor 8개가 보인다
lshw -short | head -12
```

```bash
H/W path  Device  Class      Description
========================================
                  system     Computer
/0                bus        Motherboard
/0/0              memory     8004MiB System memory
/0/1              processor  
/0/2              processor  
/0/3              processor  
/0/4              processor  
/0/5              processor  
/0/6              processor  
/0/7              processor  
```

```bash
# -class memory: 한 종류만 고른다
lshw -class memory -short
```

```bash
H/W path  Device  Class      Description
========================================
/0/0              memory     8004MiB System memory
```

```bash
# 일반 사용자로 실행하면 root 로 실행하라는 경고가 먼저 나오고, 이 환경에서는 목록이 비어 있다
su appuser -c 'lshw -short 2>&1 | head -3'
```

```bash
WARNING: you should run this program as super-user.
H/W path  Device  Class      Description
========================================
```

### 커널이 직접 센 메모리 크기

```bash
# /proc/meminfo: 커널이 센 총 메모리. 단위는 kB. lshw 의 8004MiB 와 같은 메모리를 가리킨다
grep MemTotal /proc/meminfo
```

```bash
MemTotal:        8196284 kB
```

`MemTotal` 8196284 kB 는 약 8004MiB 입니다. `free` 도 이 파일에서 값을 읽습니다.[^cpuinfo]



## 9. 서버 정보를 한 번에 확인하는 묶음

> 모델·메모리 슬롯 수·CPU 개수·메모리 크기를 한 번에 뽑습니다. DMI 표가 없는 환경은 앞 두 줄이 비는 것으로 드러납니다.

```bash
# 모델·슬롯 수(Memory Device 레코드 수)·CPU 개수와 계열·메모리 총량
echo "model : $(dmidecode -s system-product-name)"
echo "slots : $(dmidecode -t memory | grep -c '^Memory Device')"
echo "cpus  : $(nproc --all) ($(lscpu | awk -F': *' '/^Architecture/{print $2}'))"
echo "memory: $(awk '/MemTotal/ {printf "%.1f GiB", $2/1024/1024}' /proc/meminfo)"
```

```bash
model : 
slots : 0
cpus  : 8 (aarch64)
memory: 7.8 GiB
```

이 기기에서는 `model` 이 비고 `slots` 가 0 입니다. DMI 표가 있는 장비에서는 위 두 줄에 값이 들어옵니다. 다만 `slots` 는 `Memory Device` 레코드 수이므로, 펌웨어가 빈 슬롯을 레코드로 적는지에 따라 실제 꽂힌 DIMM 수와 다를 수 있습니다. 이 한계는 7절 끝의 주의와 같습니다. `cpus` 줄은 DMI 와 무관해서 어느 환경에서나 값이 나옵니다. `nproc --all` 은 설치된 전체입니다. `--cpuset-cpus` 제한을 반영하려면 6절처럼 `nproc` 을, `--cpus` 제한은 `cpu.max` 를 봅니다.



## 관련 문서

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [무엇을 쓰고 있는지 확인하는 법](../../../book/learning-modern-linux/02-01.%EC%BB%A4%EB%84%90%EC%9D%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%ED%95%98%EC%A7%80%EB%A7%8C%20%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EB%8A%94%20%EC%95%84%EB%8B%88%EB%8B%A4.md#무엇을-쓰고-있는지-확인하는-법) — CPU 계열을 `lscpu` 로 읽는 이유와 x86 출력 예
- [BIOS 와 UEFI](../../../book/learning-modern-linux/02-01.%EC%BB%A4%EB%84%90%EC%9D%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%ED%95%98%EC%A7%80%EB%A7%8C%20%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EB%8A%94%20%EC%95%84%EB%8B%88%EB%8B%A4.md#bios-와-uefi) — `dmidecode` 가 읽는 펌웨어 표가 어디서 오는지의 배경
- [uname·os-release·hostnamectl](./uname%C2%B7os-release%C2%B7hostnamectl.md) — 커널과 배포판 이름·버전을 읽는 시트



## 참고 자료

- util-linux 2.38.1 의 `lscpu --help`·`man lscpu`·`man lsmem` — Debian 12 컨테이너에서 2026-11-11 확인
- dmidecode 3.4 의 `man dmidecode`·`man lshw`, coreutils 9.1 의 `nproc --help` — 같은 컨테이너에서 확인
- [lscpu(1) — Debian bookworm](https://manpages.debian.org/bookworm/util-linux/lscpu.1.en.html), [lsmem(1)](https://manpages.debian.org/bookworm/util-linux/lsmem.1.en.html)
- [dmidecode(8) — Debian bookworm](https://manpages.debian.org/bookworm/dmidecode/dmidecode.8.en.html), [lshw(1)](https://manpages.debian.org/bookworm/lshw/lshw.1.en.html)
- [nproc(1) — Debian bookworm](https://manpages.debian.org/bookworm/coreutils/nproc.1.en.html)
- [proc(5) — Debian bookworm](https://manpages.debian.org/bookworm/manpages/proc.5.en.html), [mem(4)](https://manpages.debian.org/bookworm/manpages/mem.4.en.html)
- [Resource constraints — Docker Docs](https://docs.docker.com/engine/containers/resource_constraints/)
- [Control Group v2 — The Linux Kernel documentation](https://docs.kernel.org/admin-guide/cgroup-v2.html)
- [The Unified Extensible Firmware Interface (UEFI) — The Linux Kernel documentation](https://docs.kernel.org/arch/arm/uefi.html)

[^lscpu]: `man lscpu` (util-linux 2.38.1) — "lscpu gathers CPU architecture information from sysfs, /proc/cpuinfo and any applicable architecture-specific libraries", "The default output formatting on terminal is subject to change and maybe optimized for better readability.", "The output for non-terminals (e.g., pipes) is never affected by this optimization and it is always in "Field: data\n" format.", "In virtualized environments, the CPU architecture information displayed reflects the configuration of the guest operating system which is typically different from the physical (host) system.", "On virtual hardware the number of cores per socket, etc. can be wrong.", "The column labels are not case sensitive.", "Not all columns are supported on all architectures. If an unsupported column is specified, lscpu prints the column but does not provide any data for it.", "The cache sizes are reported as summary from all CPUs. The versions before v2.34 reported per-core sizes", "Since version v2.37 lscpu follows cache IDs as provided by Linux kernel and it does not always start from zero."; OPTIONS `-a` "Include lines for online and offline CPUs in the output (default for -e).", `-b` "Limit the output to online CPUs (default for -p).", `-c` "Limit the output to offline CPUs.", "This option may only be specified together with option -e or -p.", `-e` "Display the CPU information in human-readable format.", `-J` "Use JSON output format for the default summary or extended output", `-p` "If the list argument is omitted, the command output is compatible with earlier versions of lscpu. In this compatible format, two commas are used to separate CPU cache columns.", `-B` "Print the sizes in bytes rather than in a human-readable format.", `-x` "Use hexadecimal masks for CPU sets (for example "ff").", `-y` "Display physical IDs for all columns with topology elements", `--output-all` "Output all available columns." https://manpages.debian.org/bookworm/util-linux/lscpu.1.en.html
[^nproc]: `nproc --help` (GNU coreutils 9.1) — "Print the number of processing units available to the current process, which may be less than the number of online processors", "--all      print the number of installed processors", "--ignore=N  if possible, exclude N processing units". https://manpages.debian.org/bookworm/coreutils/nproc.1.en.html
[^cpuinfo]: `man 5 proc` (Linux man-pages 6.03) — /proc/cpuinfo "This is a collection of CPU and system architecture dependent items, for each supported architecture a different list.", "The lscpu(1) command gathers its information from this file."; /proc/meminfo "It is used by free(1) to report the amount of free and used memory (both physical and swap) on the system". https://manpages.debian.org/bookworm/manpages/proc.5.en.html
[^docker]: Docker Docs, Resource constraints — `--cpus` "Specify how much of the available CPU resources a container can use.", `--cpuset-cpus` "Limit the specific CPUs or cores a container can use.", `--cpu-period` "Defaults to 100000 microseconds (100 milliseconds)." https://docs.docker.com/engine/containers/resource_constraints/
[^cgroup]: Linux kernel documentation, Control Group v2 — cpu.max "which indicates that the group may consume up to $MAX in each $PERIOD duration. "max" for $MAX indicates no limit.", cpuset.cpus.effective "It lists the active CPUs available to tasks in this cgroup." https://docs.kernel.org/admin-guide/cgroup-v2.html
[^dmi]: `man dmidecode` (dmidecode 3.4) — "dmidecode is a tool for dumping a computer's DMI (some say SMBIOS) table contents in a human-readable format.", "you can retrieve this information without having to probe for the actual hardware. While this is a good point in terms of report speed and safeness, this also makes the presented information possibly unreliable.", "It will first try to read the DMI table from sysfs, and next try reading directly from memory if sysfs access failed.", "Each record has: A handle ... A type ... A size ... Decoded values."; FILES "/dev/mem", "/sys/firmware/dmi/tables/smbios_entry_point (Linux only)", "/sys/firmware/dmi/tables/DMI (Linux only)". https://manpages.debian.org/bookworm/dmidecode/dmidecode.8.en.html
[^dmi-opt]: `man dmidecode` OPTIONS — `-t` "It can be either a DMI type number, or a comma-separated list of type numbers, or a keyword from the following list: bios, system, baseboard, chassis, processor, memory, cache, connector, slot.", "If this option is used more than once, the set of displayed entries will be the union of all the given types.", "Keywords are matched case-insensitively."; `-s` "Only display the value of the DMI string identified by KEYWORD.", "Not all strings may be meaningful or even defined on all systems.", "This option cannot be used more than once.", "Note: on Linux, most of these strings can alternatively be read directly from sysfs, typically from files under /sys/devices/virtual/dmi/id. Most of these files are even readable by regular users."; "Options --string, --type, --dump-bin and --oem-string determine the output format and are mutually exclusive."; `-q` "Be less verbose. Unknown, inactive and OEM-specific entries are not displayed. Meta-data and handle references are hidden.", `-u` "Do not decode the entries, dump their contents as hexadecimal instead.", `-H` "Only display the entry whose handle matches HANDLE. HANDLE is a 16-bit integer.", `--dump-bin` "dump the DMI data to a file in binary form", `--from-dump` "Read the DMI data from a binary file previously generated using --dump-bin.", `-d` "Read memory from device FILE (default: /dev/mem)", `--no-sysfs` "Do not attempt to read DMI data from sysfs files.", `--oem-string` "With special value count, return the number of OEM strings instead."; DMI TYPES 표(`memory` = 5, 6, 16, 17 등). 이 환경에서 `-s` 가 `/sys/devices/virtual/dmi/id` 아래 파일을 읽는지는 확인하지 못했고, 시트는 man 의 문장만 옮깁니다.
[^devmem]: `man 4 mem` (Linux man-pages 6.03) — "/dev/mem is a character device file that is an image of the main memory of the computer.", "It is typically created by:" 다음 두 줄 "mknod -m 660 /dev/mem c 1 1", "chown root:kmem /dev/mem". 이 기기에는 `/dev/mem` 이 없어 권한은 직접 확인하지 못했습니다. https://manpages.debian.org/bookworm/manpages/mem.4.en.html
[^bugs]: `man dmidecode` BUGS — "More often than not, information contained in the DMI tables is inaccurate, incomplete or simply wrong."
[^lsmem]: `man lsmem` (util-linux 2.38.1) — "The lsmem command lists the ranges of available memory with their online status. The listed memory blocks correspond to the memory block representation in sysfs." https://manpages.debian.org/bookworm/util-linux/lsmem.1.en.html
[^lshw]: `man lshw` (lshw 02.19) — "lshw is a small tool to extract detailed information on the hardware configuration of the machine.", "It currently supports DMI (x86 and IA-64 only), OpenFirmware device tree (PowerPC only)". https://manpages.debian.org/bookworm/lshw/lshw.1.en.html
[^uefi]: Linux kernel documentation, The Unified Extensible Firmware Interface (UEFI) — "Booting on a platform with firmware compliant with the UEFI specification makes it possible for the kernel to support additional features:", "Retrieving various configuration information through the standardised interface of UEFI configuration tables. (ACPI, SMBIOS, ...)" https://docs.kernel.org/arch/arm/uefi.html
