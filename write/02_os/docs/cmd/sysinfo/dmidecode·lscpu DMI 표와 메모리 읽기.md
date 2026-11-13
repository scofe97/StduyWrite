---
title: dmidecode·lsmem·lshw DMI 표와 메모리 읽기
tags: [linux, cheatsheet, dmidecode, lsmem, lshw, smbios, memory, cli, reference]
status: draft
source:
  - dmidecode 3.4 dmidecode(8), lshw(1) (Debian 12 패키지 man 원문)
  - util-linux 2.38.1 lsmem(1) (Debian 12 패키지 man 원문, manpages.debian.org bookworm)
  - Linux man-pages proc(5), mem(4) (Debian 12 manpages)
  - Linux kernel documentation, The Unified Extensible Firmware Interface (UEFI)
related:
  - ./dmidecode%C2%B7lscpu.md
  - ../README.md
  - ../../../book/learning-modern-linux/02-01.%EC%BB%A4%EB%84%90%EC%9D%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%ED%95%98%EC%A7%80%EB%A7%8C%20%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EB%8A%94%20%EC%95%84%EB%8B%88%EB%8B%A4.md
  - ./uname%C2%B7os-release%C2%B7hostnamectl.md
updated: 2026-11-13
---

# dmidecode·lsmem·lshw DMI 표와 메모리 읽기

---

> 펌웨어가 적어 둔 제조사·모델·메모리 슬롯 정보를 읽는 `dmidecode` 와, 표가 없을 때 메모리를 읽는 `lsmem`·`lshw` 를 이 기기에서 실제로 받은 출력과 함께 모았습니다.

## 개요

> `dmidecode` 는 펌웨어가 적어 둔 DMI(SMBIOS) 표를 읽고, `lsmem`·`lshw` 는 표가 없을 때 메모리를 읽습니다.

[lscpu·nproc 참조 시트](./dmidecode·lscpu.md)에서 펌웨어의 DMI 표와 메모리를 읽는 유스케이스를 떼어 낸 것입니다. 예는 그 시트의 「실습 준비」 블록을 돌린 상태에서 이어지고, 출력은 같은 Debian 12 컨테이너(dmidecode 3.4, util-linux 2.38.1, lshw 02.19)의 root 에서 받았습니다.

세 도구는 각각 dmidecode·util-linux·lshw 패키지의 외부 바이너리입니다. 이 환경(Apple Silicon 위 컨테이너)에는 DMI 표가 없어 `dmidecode` 가 안내 메시지만 내고, 표가 있는 서버나 x86 가상 머신에서는 표의 내용이 나옵니다.



## 핵심 문법

> `dmidecode` 는 `-t` 로 종류를, `-s` 로 문자열 하나를 고르고, 표가 없을 때는 `lsmem`·`lshw` 와 `/proc/meminfo` 를 봅니다.

```bash
# 호출 형태 (dmidecode --help, lsmem --help, lshw --help 의 Usage 줄)
dmidecode [OPTIONS]
lsmem [options]
lshw [-format] [-options ...]

# 종류로 골라 표를 읽는다 (제조사·모델·BIOS 정보 읽기, 종류로 고르기 (-t))
dmidecode -t 종류

# 문자열 하나만 읽는다 (값 하나만 뽑기 (-s))
dmidecode -s 키워드

# 출력을 줄인다 (출력 모양 바꾸기 (-q))
dmidecode -q -t 종류

# 표를 파일로 뜨고 그 파일에서 읽는다 (표를 파일로 떠서 다른 곳에서 읽기)
dmidecode --dump-bin 파일
dmidecode --from-dump 파일

# 표가 없을 때 sysfs 의 DMI 파일을 직접 읽는다 (DMI 표가 없을 때 대신 볼 곳)
cat /sys/devices/virtual/dmi/id/product_name

# 메모리 범위와 온라인 상태를 읽는다 (lsmem)
lsmem

# 하드웨어 구성을 한 줄씩 읽는다 (lshw)
lshw -short

# 커널이 센 총 메모리를 읽는다 (커널이 직접 센 메모리 크기)
grep MemTotal /proc/meminfo
```

### DMI 종류 키워드

> `-t` 에 키워드를 주면 아래 종류 번호를 모두 고른 것과 같습니다.

키워드와 번호의 짝은 man 의 DMI TYPES 표를 옮긴 것이고, 키워드는 대소문자를 가리지 않습니다.[^dmi-opt]

```bash
# 키워드   종류 번호
#   bios        0, 13
#   system      1, 12, 15, 23, 32
#   baseboard   2, 10, 41
#   chassis     3
#   processor   4
#   memory      5, 6, 16, 17
#   cache       7
#   connector   8
#   slot        9
```



## 종료 코드

> 세 명령의 매뉴얼에 종료 코드 절이 없어, 이 환경에서 잰 값은 0·1·2 입니다.[^no-exit]

```bash
# dmidecode
# 0  성공. 표가 없어 안내만 내도 0 이고, 일반 사용자로 쳐도 0 이다
# 1  --from-dump 에 없는 파일을 줄 때 (「표를 파일로 떠서 다른 곳에서 읽기」)
# 2  모르는 옵션, 모르는 키워드, 값이 빠진 -s
#    (「종류로 고르기 (-t)」, 「값 하나만 뽑기 (-s)」)

# lsmem
# 1  sysfs 를 못 열 때 (「lsmem」), 모르는 옵션을 줄 때

# lshw
# 0  성공 (「lshw」)
# 1  모르는 옵션을 줄 때

# 표가 없으면 안내 두 줄을 내고도 0 으로 끝난다
dmidecode; echo $?
```

```bash
# dmidecode 3.4
# No SMBIOS nor DMI entry point found, sorry.
0
```

```bash
# 모르는 옵션. 2>&1 은 오류 메시지를 표준 출력에 합쳐 종료 코드와 함께 보인다
dmidecode --bad 2>&1; echo $?
```

```bash
dmidecode: unrecognized option '--bad'
2
```

```bash
# lsmem 은 같은 오류에 1 을 낸다
lsmem --bad 2>&1; echo $?
```

```bash
lsmem: unrecognized option '--bad'
Try 'lsmem --help' for more information.
1
```



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션만 씁니다.

### 실습 준비

> 이 시트는 따로 만드는 것이 없고 원래 시트가 설치한 도구와 일반 사용자를 그대로 씁니다.

먼저 [lscpu·nproc 참조 시트](./dmidecode·lscpu.md)의 「실습 준비」 블록을 돌립니다. 그 블록이 `dmidecode`·`lshw` 를 설치하고, 일반 사용자 `appuser` 는 「lshw」 와 「읽는 곳과 root 권한」 에서 씁니다.

### 제조사·모델·BIOS 정보 읽기

> `dmidecode` 는 펌웨어가 적어 둔 DMI(SMBIOS) 표를 읽어 서버 모델·시리얼·메모리 슬롯을 찍습니다.

표에는 하드웨어 구성, 시리얼 번호, BIOS 판 같은 정보가 있습니다. man 은 하드웨어를 직접 조사하지 않고 표에서 얻으므로 빠르고 안전하지만 정보가 틀릴 수 있다고 적고, 실행하면 sysfs 에서 표를 먼저 읽고 실패하면 메모리에서 직접 읽는다고 적습니다.[^dmi]

```bash
# 판을 확인한다
#   --version   판을 찍는다 (-V)
dmidecode --version    # 3.4
```

```bash
# 시스템 정보(type 1 등)를 읽는다. 표가 없으면 이 두 줄이 전부다
#   -t 종류   DMI 종류 번호나 키워드로 고른다
dmidecode -t system; echo "exit $?"
```

```bash
# dmidecode 3.4
# No SMBIOS nor DMI entry point found, sorry.
exit 0
```

메시지는 "SMBIOS 나 DMI 진입점을 찾지 못했다"는 뜻인데 종료 코드는 0 이라서, 스크립트가 종료 코드로 성공을 판단하면 표가 없는 것을 놓칩니다. 출력이 비었는지를 같이 봅니다.

### 종류로 고르기 (-t)

> 번호는 쉼표로 여러 개를 줄 수 있고, 키워드는 하나씩만 줄 수 있습니다.

`-t` 를 여러 번 주면 합집합이고,[^dmi-opt] 키워드 목록은 「핵심 문법」 의 「DMI 종류 키워드」 에 있습니다.

```bash
# 번호 목록. 4 는 Processor, 17 은 Memory Device. 표가 없으니 같은 메시지다
dmidecode -t 4,17; echo "exit $?"
```

```bash
# dmidecode 3.4
# No SMBIOS nor DMI entry point found, sorry.
exit 0
```

```bash
# 키워드 아홉 개를 하나씩 돌려 마지막 줄을 센다. 표가 없으니 전부 같은 줄이다
#   tail -1   마지막 한 줄만 남긴다
#   uniq -c   이어진 같은 줄을 하나로 묶고 앞에 개수를 붙인다
for t in bios system baseboard chassis processor memory cache connector slot; \
  do dmidecode -t $t | tail -1; \
done \
  | sort \
  | uniq -c
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

표가 있는 장비에서 `-t memory` 는 메모리 컨트롤러·모듈·물리 메모리 배열·메모리 장치(type 5, 6, 16, 17) 레코드를 찍습니다. 레코드는 `Handle 0x…, DMI type …, … bytes.` 로 시작하고 그 아래 항목이 `이름: 값` 줄로 이어지며,[^dmi] 슬롯 하나가 레코드 하나로 나오는지와 빈 슬롯이 어떻게 적히는지는 펌웨어마다 다릅니다.

### 값 하나만 뽑기 (-s)

> `-s` 로 받은 문자열은 변수에 바로 담을 수 있지만, 표가 없으면 빈 값이 됩니다.

키워드는 `system-product-name`, `system-serial-number`, `bios-version` 처럼 종류와 항목이 붙은 이름이고 모든 장비가 모든 문자열을 갖지는 않습니다. `-s` 는 한 번만 쓸 수 있고 `-t`·`--dump-bin`·`--oem-string` 과 함께 쓰지 못하며,[^dmi-opt] 키워드 전체 목록은 값 없이 `dmidecode -s` 를 치면 나옵니다.

```bash
# 모델 이름 한 줄. 표가 없으면 아무것도 찍지 않아 0바이트다
#   -s 키워드   키워드로 지정한 DMI 문자열 하나만 찍는다
#   wc -c       바이트 수를 센다
dmidecode -s system-product-name | wc -c    # 0
```

```bash
# 값을 안 주면 키워드 목록을 찍고 종료 코드 2. 종료 코드는 위처럼 따로 받는다
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

> `-q` 는 출력을 줄이고, `-u`·`-H`·`--oem-string` 은 해독 여부와 읽을 대상을 바꿉니다.

```bash
# 알 수 없거나 비활성이거나 OEM 전용인 항목, 메타데이터, 핸들 참조를 숨긴다
# 표가 없으면 안내 줄도 사라진다
#   -q   출력을 줄인다 (--quiet)
dmidecode -q -t memory | wc -l    # 0
```

```bash
# 그 밖의 출력 옵션. 이 기기에서는 -u·-H 도 -t system 과 같은 두 줄 메시지만 나왔다
#   -u               해독하지 않고 16진수로 찍는다. 디버깅에 쓴다
#   -H 핸들          핸들 번호 하나의 항목만 찍는다
#   --oem-string N   제조사가 넣은 OEM 문자열 N 번째 값을 찍는다
#                    count 를 주면 개수를 찍는다. 이 기기에서는 출력이 비어 있었다
```

이 옵션들의 뜻은 man 의 OPTIONS 절을 옮겼습니다.[^dmi-opt]

### 표를 파일로 떠서 다른 곳에서 읽기

> 표를 이진 파일로 떠 두면 다른 장비에서 뜬 표를 내 기기에서 읽을 수 있습니다.

`-d 파일` 은 `/dev/mem` 대신 읽을 장치 파일을, `--no-sysfs` 는 sysfs 를 건너뛰고 메모리에서 읽게 하는 옵션입니다.[^dmi-opt]

```bash
# 읽을 표가 없으면 파일도 만들어지지 않는다
#   --dump-bin 파일   표를 해독하지 않고 이진 파일로 저장한다
dmidecode --dump-bin dmi.bin; echo "exit $?"; ls dmi.bin 2>&1
```

```bash
# dmidecode 3.4
# No SMBIOS nor DMI entry point found, sorry.
exit 0
ls: cannot access 'dmi.bin': No such file or directory
```

```bash
# 파일을 못 열면 종료 코드 1
#   --from-dump 파일   --dump-bin 으로 만든 파일에서 읽는다
dmidecode --from-dump nofile.bin; echo "exit $?"
```

```bash
# dmidecode 3.4
Reading SMBIOS/DMI data from file nofile.bin.
nofile.bin: No such file or directory
exit 1
```

### DMI 표가 없을 때 대신 볼 곳

> DMI 표가 없는 이 기기에서 값이 나온 도구는 `lscpu`·`lshw -short`·`/proc/meminfo` 입니다.

이 시트를 만든 기기에서는 컨테이너와 OrbStack VM 모두 DMI 표가 없었고 `/sys/devices/virtual/dmi/id`·`/sys/firmware/dmi`·`/dev/mem` 이 없습니다. DMI 표는 펌웨어가 넘겨주는 것이라, 표를 받지 못한 환경에서는 `dmidecode` 가 읽을 것이 없습니다.

```bash
# 컨테이너: DMI sysfs 와 /dev/mem 이 모두 없다
ls /sys/devices/virtual/dmi/id /sys/firmware/dmi /dev/mem 2>&1
```

```bash
ls: cannot access '/sys/devices/virtual/dmi/id': No such file or directory
ls: cannot access '/sys/firmware/dmi': No such file or directory
ls: cannot access '/dev/mem': No such file or directory
```

```bash
# OrbStack VM(arm64, Ubuntu 26.04): DMI 는 없고 devicetree 가 있다 (fdt 도 함께)
# efi 디렉터리도 없다
# 이 VM 은 외부 이름 풀이가 막혀 dmidecode 를 설치하지 못해, dmidecode 출력 대신 sysfs 조회를 받았다
ls /sys/devices/virtual/dmi /sys/firmware/dmi 2>&1; ls /sys/firmware
```

```bash
ls: cannot access '/sys/devices/virtual/dmi': No such file or directory
ls: cannot access '/sys/firmware/dmi': No such file or directory
devicetree
fdt
```

```bash
# OrbStack VM: 장치 트리의 compatible 값은 orbstack,virt 다
# NUL 로 끝나는 문자열이라 tr 로 공백으로 바꾼다
tr '\0' ' ' < /sys/firmware/devicetree/base/compatible; echo
```

```bash
orbstack,virt 
```

Linux 커널 문서는 UEFI 규격을 따르는 펌웨어로 부팅하면 SMBIOS 같은 설정 정보를 UEFI 설정 표로 받을 수 있다고 적고,[^uefi] 그래서 같은 ARM 이라도 UEFI 로 부팅한 장비에서는 표가 나올 수 있습니다. man 은 `/sys/devices/virtual/dmi/id` 아래 파일 대부분을 일반 사용자도 읽는다고 적으므로(「읽는 곳과 root 권한」), 이 경로의 `product_name` 을 먼저 읽고 없으면 대체 메시지를 내는 식으로 짭니다.

```bash
# 파일이 없으면 대체 문구. 일반 사용자도 돌릴 수 있다
cat /sys/devices/virtual/dmi/id/product_name 2>/dev/null || echo "DMI 없음"
```

```bash
DMI 없음
```

### lsmem

> `lsmem` 은 메모리 범위와 온라인 상태를 sysfs 의 메모리 블록에서 읽습니다.

man 은 나열되는 메모리 블록이 sysfs 의 메모리 블록 표현과 대응한다고 적고,[^lsmem] 이 환경에는 그 sysfs 가 없어 실패합니다.

```bash
# /sys/devices/system/memory 를 읽는다. 이 환경에는 없다
lsmem; echo "exit $?"
```

```bash
lsmem: cannot open /sys/devices/system/memory: No such file or directory
exit 1
```

### lshw

> `lshw` 는 하드웨어 구성을 트리로 보여 주는 도구입니다.

man 은 lshw 의 DMI 지원을 x86·IA-64 전용으로 적고,[^lshw] 이 환경에서도 `-short` 는 CPU 개수와 메모리 크기를 찍지만 CPU 모델 이름은 비어 있습니다.

```bash
# 하드웨어 경로·종류·설명을 한 줄씩. 메모리 8004MiB 와 processor 8개가 보인다
#   -short     경로·종류·설명을 한 줄씩 찍는다
#   head -12   출력이 길어 앞 열두 줄만 남긴다
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
# 한 종류만 고른다
#   -class 종류   하드웨어 종류 하나만 고른다
lshw -class memory -short
```

```bash
H/W path  Device  Class      Description
========================================
/0/0              memory     8004MiB System memory
```

```bash
# 일반 사용자로 실행하면 root 로 실행하라는 경고가 먼저 나오고, 이 환경에서는 목록이 비어 있다
#   su appuser -c   appuser 로 따옴표 안의 명령을 실행한다
su appuser -c 'lshw -short 2>&1 | head -3'
```

```bash
WARNING: you should run this program as super-user.
H/W path  Device  Class      Description
========================================
```

### 커널이 직접 센 메모리 크기

> DMI 표가 없어도 커널이 센 총 메모리는 `/proc/meminfo` 에서 읽을 수 있습니다.

```bash
# 커널이 센 총 메모리. 단위는 kB. lshw 의 8004MiB 와 같은 메모리를 가리킨다
grep MemTotal /proc/meminfo
```

```bash
MemTotal:        8196284 kB
```

`MemTotal` 8196284 kB 는 약 8004MiB 입니다. `free` 도 이 파일에서 값을 읽습니다.[^cpuinfo]

### 서버 정보를 한 번에 확인하는 묶음

> 모델·메모리 슬롯 수·CPU 개수·메모리 크기를 한 번에 뽑고, DMI 표가 없는 환경은 앞 두 줄이 비는 것으로 드러납니다.

```bash
# 모델·슬롯 수(Memory Device 레코드 수)·CPU 개수와 계열·메모리 총량
# model·slots 는 DMI 표가 있는 장비에서 값이 들어온다
# slots 는 펌웨어가 빈 슬롯을 레코드로 적는지에 따라 실제 꽂힌 DIMM 수와 다를 수 있다 (「표를 믿는 데 쓰는 주의」)
# cpus 줄은 DMI 와 무관해서 어느 환경에서나 값이 나온다. nproc --all 은 설치된 전체다
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

`--cpuset-cpus` 제한을 반영하려면 [lscpu·nproc 참조 시트](./dmidecode·lscpu.md)의 「컨테이너 CPU 제한이 보이는 곳」 처럼 `nproc` 을, `--cpus` 제한은 `cpu.max` 를 봅니다.



## 주의사항과 동작 원리

> 예상과 다르게 동작하는 곳은 `dmidecode` 가 읽는 경로와 DMI 표의 정확도입니다.

### 읽는 곳과 root 권한

> 표 전체를 읽는 경로는 root 권한을 요구하고, 문자열 몇 개는 일반 사용자도 sysfs 에서 읽을 수 있습니다.

man 의 FILES 절은 Linux 가 sysfs 로 내보내는 `/sys/firmware/dmi/tables/` 아래 `smbios_entry_point`·`DMI` 와, sysfs 가 안 될 때 쓰는 물리 메모리 장치 `/dev/mem` 을 읽는 곳으로 적습니다.[^dmi][^devmem] `/dev/mem` 은 보통 `root:kmem` 소유라 표 전체를 보려면 root 로 실행하는 것이 보통입니다.[^devmem]

```bash
# appuser 로 실행해도 같다: 읽을 표 자체가 없어서 권한 단계까지 가지 않는다
su appuser -c 'dmidecode -t system; echo "exit $?"'
```

```bash
# dmidecode 3.4
# No SMBIOS nor DMI entry point found, sorry.
exit 0
```

이 기기에는 `/sys/firmware/dmi` 도 `/dev/mem` 도 없어서 권한 오류를 직접 재현하지 못했습니다. man 은 `-s` 로 읽는 문자열 대부분을 `/sys/devices/virtual/dmi/id` 의 파일에서도 읽을 수 있고 그 파일 대부분은 일반 사용자도 읽는다고 적지만, 표 전체를 읽는 경로에는 그런 말이 없습니다.[^dmi-opt]

### 표를 믿는 데 쓰는 주의

> 슬롯 수나 최대 용량처럼 구성 가능한 상한은 펌웨어가 적은 값이라, 실제 꽂힌 장치 수와 다를 수 있습니다.

man 은 DMI 표 정보가 "대개 부정확하거나 불완전하거나 그냥 틀렸다"고 적습니다.[^bugs] 그래서 표를 근거로 장비를 판단하기 전에 `lscpu`·`free` 같은 커널이 직접 센 값과 맞춰 봅니다.



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [lscpu·nproc 참조 시트](./dmidecode·lscpu.md) — 이 시트가 이어받는 실습 준비와 `lscpu`·`nproc` 예
- [무엇을 쓰고 있는지 확인하는 법](../../../book/learning-modern-linux/02-01.%EC%BB%A4%EB%84%90%EC%9D%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%ED%95%98%EC%A7%80%EB%A7%8C%20%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EB%8A%94%20%EC%95%84%EB%8B%88%EB%8B%A4.md#무엇을-쓰고-있는지-확인하는-법) — CPU 계열을 `lscpu` 로 읽는 이유와 x86 출력 예
- [BIOS 와 UEFI](../../../book/learning-modern-linux/02-01.%EC%BB%A4%EB%84%90%EC%9D%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%ED%95%98%EC%A7%80%EB%A7%8C%20%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EB%8A%94%20%EC%95%84%EB%8B%88%EB%8B%A4.md#bios-와-uefi) — `dmidecode` 가 읽는 펌웨어 표가 어디서 오는지의 배경
- [uname·os-release·lsb_release 참조 시트](./uname%C2%B7os-release%C2%B7hostnamectl.md) — 커널과 배포판 이름·버전을 읽는 시트



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- dmidecode 3.4 의 `dmidecode --help`·`man dmidecode` 원문 — Debian 12 컨테이너에서 2026-11-14 확인
- lshw 02.19 의 `lshw -help`·`man lshw` 원문 — Debian 12 컨테이너에서 2026-11-14 확인
- util-linux 2.38.1 의 `lsmem --help`·`man lsmem` 원문 — Debian 12 컨테이너에서 2026-11-14 확인
- [dmidecode(8) — Debian bookworm](https://manpages.debian.org/bookworm/dmidecode/dmidecode.8.en.html), [lshw(1)](https://manpages.debian.org/bookworm/lshw/lshw.1.en.html)
- [lsmem(1) — Debian bookworm](https://manpages.debian.org/bookworm/util-linux/lsmem.1.en.html)
- [proc(5) — Debian bookworm](https://manpages.debian.org/bookworm/manpages/proc.5.en.html), [mem(4)](https://manpages.debian.org/bookworm/manpages/mem.4.en.html)
- [The Unified Extensible Firmware Interface (UEFI) — The Linux Kernel documentation](https://docs.kernel.org/arch/arm/uefi.html)

[^no-exit]: `man dmidecode` (dmidecode 3.4) 의 절은 "NAME", "SYNOPSIS", "DESCRIPTION", "OPTIONS", "DMI TYPES", "BINARY DUMP FILE FORMAT", "UUID FORMAT", "FILES", "BUGS", "AUTHORS", "SEE ALSO", `man lsmem` (util-linux 2.38.1) 의 절은 "NAME", "SYNOPSIS", "DESCRIPTION", "OPTIONS", "AUTHORS", "SEE ALSO", "REPORTING BUGS", "AVAILABILITY", `man lshw` (lshw 02.19) 의 절은 "NAME", "SYNOPSIS", "DESCRIPTION", "BUGS", "NOTES", "FILES", "EXAMPLES", "SEE ALSO", "COPYING", "AUTHOR", "OTHER INFO" 라서 세 매뉴얼 모두 EXIT STATUS 절이 없습니다. https://manpages.debian.org/bookworm/dmidecode/dmidecode.8.en.html https://manpages.debian.org/bookworm/util-linux/lsmem.1.en.html https://manpages.debian.org/bookworm/lshw/lshw.1.en.html
[^cpuinfo]: `man 5 proc` (Linux man-pages 6.03) — /proc/cpuinfo "This is a collection of CPU and system architecture dependent items, for each supported architecture a different list.", "The lscpu(1) command gathers its information from this file."; /proc/meminfo "It is used by free(1) to report the amount of free and used memory (both physical and swap) on the system". https://manpages.debian.org/bookworm/manpages/proc.5.en.html
[^dmi]: `man dmidecode` (dmidecode 3.4) — "dmidecode is a tool for dumping a computer's DMI (some say SMBIOS) table contents in a human-readable format.", "you can retrieve this information without having to probe for the actual hardware. While this is a good point in terms of report speed and safeness, this also makes the presented information possibly unreliable.", "It will first try to read the DMI table from sysfs, and next try reading directly from memory if sysfs access failed.", "Each record has: A handle ... A type ... A size ... Decoded values."; FILES "/dev/mem", "/sys/firmware/dmi/tables/smbios_entry_point (Linux only)", "/sys/firmware/dmi/tables/DMI (Linux only)". https://manpages.debian.org/bookworm/dmidecode/dmidecode.8.en.html
[^dmi-opt]: `man dmidecode` OPTIONS — `-t` "It can be either a DMI type number, or a comma-separated list of type numbers, or a keyword from the following list: bios, system, baseboard, chassis, processor, memory, cache, connector, slot.", "If this option is used more than once, the set of displayed entries will be the union of all the given types.", "Keywords are matched case-insensitively."; `-s` "Only display the value of the DMI string identified by KEYWORD.", "Not all strings may be meaningful or even defined on all systems.", "This option cannot be used more than once.", "Note: on Linux, most of these strings can alternatively be read directly from sysfs, typically from files under /sys/devices/virtual/dmi/id. Most of these files are even readable by regular users."; "Options --string, --type, --dump-bin and --oem-string determine the output format and are mutually exclusive."; `-q` "Be less verbose. Unknown, inactive and OEM-specific entries are not displayed. Meta-data and handle references are hidden.", `-u` "Do not decode the entries, dump their contents as hexadecimal instead.", `-H` "Only display the entry whose handle matches HANDLE. HANDLE is a 16-bit integer.", `--dump-bin` "dump the DMI data to a file in binary form", `--from-dump` "Read the DMI data from a binary file previously generated using --dump-bin.", `-d` "Read memory from device FILE (default: /dev/mem)", `--no-sysfs` "Do not attempt to read DMI data from sysfs files.", `--oem-string` "With special value count, return the number of OEM strings instead."; DMI TYPES 표(`memory` = 5, 6, 16, 17 등). 이 환경에서 `-s` 가 `/sys/devices/virtual/dmi/id` 아래 파일을 읽는지는 확인하지 못했고, 시트는 man 의 문장만 옮깁니다.
[^devmem]: `man 4 mem` (Linux man-pages 6.03) — "/dev/mem is a character device file that is an image of the main memory of the computer.", "It is typically created by:" 다음 두 줄 "mknod -m 660 /dev/mem c 1 1", "chown root:kmem /dev/mem". 이 기기에는 `/dev/mem` 이 없어 권한은 직접 확인하지 못했습니다. https://manpages.debian.org/bookworm/manpages/mem.4.en.html
[^bugs]: `man dmidecode` BUGS — "More often than not, information contained in the DMI tables is inaccurate, incomplete or simply wrong."
[^lsmem]: `man lsmem` (util-linux 2.38.1) — "The lsmem command lists the ranges of available memory with their online status. The listed memory blocks correspond to the memory block representation in sysfs." https://manpages.debian.org/bookworm/util-linux/lsmem.1.en.html
[^lshw]: `man lshw` (lshw 02.19) — "lshw is a small tool to extract detailed information on the hardware configuration of the machine.", "It currently supports DMI (x86 and IA-64 only), OpenFirmware device tree (PowerPC only)". https://manpages.debian.org/bookworm/lshw/lshw.1.en.html
[^uefi]: Linux kernel documentation, The Unified Extensible Firmware Interface (UEFI) — "Booting on a platform with firmware compliant with the UEFI specification makes it possible for the kernel to support additional features:", "Retrieving various configuration information through the standardised interface of UEFI configuration tables. (ACPI, SMBIOS, ...)" https://docs.kernel.org/arch/arm/uefi.html
