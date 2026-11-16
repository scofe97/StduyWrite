---
title: dd 참조 시트
tags: [linux, cheatsheet, dd, block, signal, storage, cli, reference]
status: draft
source:
  - GNU coreutils 9.7 의 `dd --help` 원문과 `man dd`·`info coreutils` 의 "dd invocation" (Ubuntu 26.04 gnu-coreutils 9.7-3ubuntu2.1)
  - macOS 26.6 dd(1) (`man dd` 원문, 다르게 동작하는 환경)
related:
  - ../README.md
  - ./df·du.md
  - ../resource/iostat.md
  - ../process/kill·pgrep·killall.md
  - ../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md
  - ../../../book/learning-modern-linux/09-02.%EC%8B%9C%EA%B7%B8%EB%84%90%EC%9D%80%20%EB%B2%88%ED%98%B8%20%ED%95%98%EB%82%98%EB%A7%8C%20%EB%B3%B4%EB%82%B4%EA%B3%A0%20%EB%81%9D%EB%82%98%EB%8A%94%20%EB%AA%A8%EC%96%91%EC%9D%80%20%EC%B2%98%EB%A6%AC%20%EB%B0%A9%EC%8B%9D%EC%9D%B4%20%EC%A0%95%ED%95%9C%EB%8B%A4.md
updated: 2026-11-16
---

# dd 참조 시트

---

> 입력을 블록 단위로 읽어 출력에 쓰는 `dd` 를 블록 크기와 위치, 변환, 진행 통계와 `USR1`, 짧은 읽기, 쓰기 처리량으로 나눠 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `dd` 는 `이름=값` 꼴 피연산자로 입력과 출력, 블록 크기, 변환을 정해 파일이나 장치를 복사합니다.

`dd` 는 coreutils 의 외부 바이너리입니다. 이 시트는 Ubuntu 26.04 VM 에서 실측했습니다. 이 판의 `/usr/bin/dd` 는 uutils 0.10.0 입니다. 그래서 「실습 준비」 에서 GNU coreutils 9.7 의 `gnudd` 를 `dd` 이름으로 앞세웠습니다.

uutils 판은 `partial read` 경고를 내지 않습니다. 오류 문구와 `oflag=direct` 결과도 달라 「uutils 판 dd 와의 차이」 에서 따로 보입니다. macOS 의 BSD `dd` 는 `--help` 가 없고, 통계를 찍는 시그널이 `USR1` 이 아니라 `SIGINFO` 입니다.[^bsd]



## 핵심 문법

> `dd` 는 `--help`·`--version` 말고는 `이름=값` 피연산자만 받고, `if`·`of` 로 입출력을, `bs`·`count`·`skip`·`seek` 로 범위를 정합니다.

```bash
# 호출 형태 (dd --help 의 Usage 줄)
dd [OPERAND]...
dd OPTION

# 입력과 출력, 블록 크기, 개수를 정해 복사한다 (블록 크기와 개수로 파일 만들기)
dd \
  if=입력 \
  of=출력 \
  bs=크기 \
  count=개수

# 입력과 출력의 시작 위치를 옮긴다 (입력과 출력 위치 옮기기)
dd \
  if=입력 \
  of=출력 \
  bs=크기 \
  skip=블록수 \
  seek=블록수

# 변환과 출력 파일 처리를 정한다 (변환과 출력 파일 제어)
dd \
  if=입력 \
  of=출력 \
  conv=변환

# 통계를 줄이거나 진행을 본다 (통계와 진행 상황 보기)
dd \
  if=입력 \
  of=출력 \
  status=progress

# 파이프 입력의 짧은 읽기를 막는다 (짧은 읽기와 fullblock)
dd \
  bs=크기 \
  count=개수 \
  iflag=fullblock

# 디스크까지 쓰거나 캐시를 건너뛴다 (쓰기 처리량과 페이지 캐시)
dd \
  if=입력 \
  of=출력 \
  conv=fdatasync
dd \
  if=입력 \
  of=출력 \
  oflag=direct
```

### 크기 접미사

> `bs` 에 주는 수 뒤에 붙여 단위를 정하는 접미사 가운데 본문에서 쓰는 것입니다.[^dd-help]

```bash
# 접미사   뜻
# M        1024*1024 바이트. MiB 도 같다. bs=1M, bs=256M
# MB       1000*1000 바이트. bs=1MB
```



## 종료 코드

> `dd` 는 성공하면 0, 실패하면 0 이 아닌 값을 돌려주며 이 시트의 실패는 모두 1 이었습니다.[^exit]

```bash
# 0  성공. 복사를 끝냈을 때
# 1  실패. 없는 입력 파일, 모르는 피연산자, 잘못된 숫자를 줬을 때

# 없는 입력 파일
dd if=/nonexistent of=/dev/null; echo $?
# dd: failed to open '/nonexistent': No such file or directory / 1

# 0 인 블록 크기
dd bs=0 </dev/null; echo $?    # dd: invalid number: '0' / 1

# 모르는 피연산자
dd bogus=1; echo $?
```

```bash
dd: unrecognized operand 'bogus=1'
Try 'dd --help' for more information.
1
```

첫 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다. 이 출력은 「실습 준비」 의 첫 블록으로 GNU `dd` 를 앞세운 셸에서 받았습니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 피연산자와 만든 파일만 씁니다.

### 실습 준비

> 아래 블록을 root 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 폴더, 입력 파일, ext4 이미지가 생깁니다.

OrbStack 의 Ubuntu 26.04 VM 에서 `sudo -i` 로 root 가 된 뒤 실행합니다. 출력 대상은 아래에서 만든 폴더 안의 파일과 `/dev/null` 뿐이며, 디스크 장치에는 쓰지 않습니다.

```bash
# Ubuntu 26.04 의 dd 는 기본이 uutils 판이라 GNU 판 gnudd 를 dd 이름으로 앞세운다
# Debian·RHEL 처럼 GNU coreutils 를 쓰는 배포판에서는 이 세 줄이 필요 없다
mkdir -p /tmp/lab-dd/bin
ln -s /usr/bin/gnudd /tmp/lab-dd/bin/dd
export PATH=/tmp/lab-dd/bin:$PATH

# 예가 파일을 만들 작업 폴더. 이 셸은 이후 이 폴더에서 친다
#   work    「블록 크기와 개수로 파일 만들기」 부터 여러 곳이 쓴다
#   ext4    「쓰기 처리량과 페이지 캐시」 의 oflag=direct 예가 쓴다
#   /var/tmp/lab-dd   디스크 위 폴더. 「쓰기 처리량과 페이지 캐시」 가 쓴다
mkdir -p /tmp/lab-dd/work /tmp/lab-dd/ext4 /var/tmp/lab-dd
cd /tmp/lab-dd/work

# 바이트 위치를 세기 쉬운 10바이트 입력 파일. 「입력과 출력 위치 옮기기」 가 쓴다
printf 'ABCDEFGHIJ' > src.txt

# 64MiB 짜리 ext4 이미지를 루프 장치로 마운트한다
#   truncate -s N   파일 크기를 N 으로 맞춘다
#   mkfs.ext4 -q    메시지 없이 ext4 를 만든다
#   mount -o loop   파일을 장치처럼 마운트한다
truncate -s 64M /tmp/lab-dd/ext4.img
mkfs.ext4 -q /tmp/lab-dd/ext4.img
mount -o loop /tmp/lab-dd/ext4.img /tmp/lab-dd/ext4
```

### 블록 크기와 개수로 파일 만들기

> `if` 와 `of` 로 입출력을 정하고 `bs` 와 `count` 로 한 번에 옮기는 크기와 횟수를 정합니다.

```bash
# 0 으로 채운 10MiB 파일을 만든다. 통계 3줄은 표준 오류로 나온다
#   if=FILE    읽을 파일. 생략하면 표준 입력. /dev/zero 는 0 바이트를 끝없이 준다
#   of=FILE    쓸 파일. 생략하면 표준 출력
#   bs=BYTES   한 번에 최대 BYTES 바이트씩 읽고 쓴다. 기본 512
#   count=N    입력 블록 N개만 복사한다
dd \
  if=/dev/zero \
  of=zero.img \
  bs=1M \
  count=10
```

```bash
10+0 records in
10+0 records out
10485760 bytes (10 MB, 10 MiB) copied, 0.00406473 s, 2.6 GB/s
```

`10+0` 은 온전한 블록 10개와 짧은 블록 0개를 뜻합니다.[^status]

```bash
# 같은 1000000바이트를 1바이트씩, 그리고 한 번에 옮긴다. 시간이 크게 다르다
dd \
  if=/dev/zero \
  of=/dev/null \
  bs=1 \
  count=1000000

dd \
  if=/dev/zero \
  of=/dev/null \
  bs=1MB \
  count=1
```

```bash
1000000+0 records in
1000000+0 records out
1000000 bytes (1.0 MB, 977 KiB) copied, 0.187678 s, 5.3 MB/s
1+0 records in
1+0 records out
1000000 bytes (1.0 MB, 977 KiB) copied, 0.000267795 s, 3.7 GB/s
```

블록이 작으면 읽기와 쓰기 호출이 그만큼 늘어납니다. 시간과 속도는 실행마다 다릅니다.

### 입력과 출력 위치 옮기기

> `skip` 은 입력의 앞을 건너뛰고 `seek` 은 출력의 앞을 건너뛰며, 출력 파일을 자를지는 `conv=notrunc` 가 정합니다.

```bash
# 입력의 앞 3바이트를 건너뛰고 4바이트만 복사한다
#   skip=N   입력 앞의 N블록을 건너뛴다 (iseek=N). bs=1 이라 N바이트다
dd \
  if=src.txt \
  of=cut.txt \
  bs=1 \
  skip=3 \
  count=4
cat cut.txt; echo
```

```bash
4+0 records in
4+0 records out
4 bytes copied, 3.1256e-05 s, 128 kB/s
DEFG
```

```bash
# 출력 3바이트 뒤에 0 바이트 둘을 덮어쓴다. 뒤쪽 FGHIJ 는 남는다
#   seek=N         출력 앞의 N블록을 건너뛴다 (oseek=N)
#   conv=notrunc   출력 파일을 자르지 않는다
#   od -c          바이트를 문자로 찍는다. \0 은 0 바이트다
printf 'ABCDEFGHIJ' > dst.txt
dd \
  if=/dev/zero \
  of=dst.txt \
  bs=1 \
  seek=3 \
  count=2 \
  conv=notrunc
od -c dst.txt
```

```bash
2+0 records in
2+0 records out
2 bytes copied, 2.2545e-05 s, 88.7 kB/s
0000000   A   B   C  \0  \0   F   G   H   I   J
0000012
```

```bash
# notrunc 를 빼면 쓰기 전에 파일을 비워 앞 5바이트만 남는다
printf 'ABCDEFGHIJ' > dst2.txt
dd \
  if=/dev/zero \
  of=dst2.txt \
  bs=1 \
  seek=3 \
  count=2
od -c dst2.txt
```

```bash
2+0 records in
2+0 records out
2 bytes copied, 3.4881e-05 s, 57.3 kB/s
0000000   A   B   C  \0  \0
0000005
```

### 변환과 출력 파일 제어

> `conv` 는 데이터를 바꾸거나 출력 파일을 여는 방식을 정합니다.

```bash
# 표준 입력을 대문자로 바꿔 표준 출력으로 낸다. 통계는 표준 오류라 버린다
#   conv=ucase   소문자를 대문자로 바꾼다
echo hello | dd conv=ucase 2>/dev/null    # HELLO
```

```bash
# 0 블록을 쓰지 않고 건너뛰면 같은 10MiB 가 희소 파일이 된다
#   conv=sparse   0 으로만 찬 출력 블록은 쓰지 않고 seek 한다
#   stat -c       출력 형식을 정한다. %n 이름, %s 바이트 수, %b 512바이트 블록 수
dd \
  if=/dev/zero \
  of=sp.img \
  bs=1M \
  count=10 \
  conv=sparse 2>/dev/null
dd \
  if=/dev/zero \
  of=nosp.img \
  bs=1M \
  count=10 2>/dev/null
stat -c '%n %s %b' sp.img nosp.img
```

```bash
sp.img 10485760 0
nosp.img 10485760 20480
```

크기는 같고 `sp.img` 만 블록을 쓰지 않았습니다. `du` 로 보는 법은 [df·du 참조 시트](./df·du.md)에 있습니다.

```bash
# 이미 있는 파일에는 쓰지 않고, 없는 파일은 만들지 않는다
#   conv=excl      출력 파일이 이미 있으면 실패한다
#   conv=nocreat   출력 파일을 만들지 않는다. 없으면 실패한다
dd \
  if=src.txt \
  of=out.txt \
  conv=excl
dd \
  if=src.txt \
  of=out.txt \
  conv=excl
dd \
  if=src.txt \
  of=none.txt \
  conv=nocreat
```

```bash
0+1 records in
0+1 records out
10 bytes copied, 2.563e-05 s, 390 kB/s
dd: failed to open 'out.txt': File exists
dd: failed to open 'none.txt': No such file or directory
```

첫 줄 묶음은 `out.txt` 를 만든 첫 호출의 통계입니다. 둘째 호출은 이미 있는 파일이라, 셋째 호출은 없는 파일이라 실패했습니다.

### 통계와 진행 상황 보기

> `status` 로 통계를 줄이거나 진행을 찍고, 도는 `dd` 에 `USR1` 을 보내 그 시점의 통계를 받습니다.

```bash
# 통계를 줄인다
#   status=none     오류 말고는 아무것도 찍지 않는다
#   status=noxfer   마지막 전송량·속도 줄만 뺀다
dd \
  if=src.txt \
  of=/dev/null \
  status=none
dd \
  if=src.txt \
  of=/dev/null \
  status=noxfer
```

```bash
0+1 records in
0+1 records out
```

```bash
# 마지막 줄을 1초마다 갱신한다. 갱신이 \r 이라 tr 로 줄바꿈해서 본다
#   status=progress   전송량을 1초마다 표준 오류로 찍는다
dd \
  if=/dev/zero \
  of=/dev/null \
  bs=1M \
  count=100000 \
  status=progress 2>&1 | tr '\r' '\n'
```

```bash
27416068096 bytes (27 GB, 26 GiB) copied, 1 s, 27.4 GB/s
55406755840 bytes (55 GB, 52 GiB) copied, 2 s, 27.7 GB/s
83115376640 bytes (83 GB, 77 GiB) copied, 3 s, 27.7 GB/s
100000+0 records in
100000+0 records out
104857600000 bytes (105 GB, 98 GiB) copied, 3.80878 s, 27.5 GB/s
```

위 출력은 첫 빈 줄을 뺀 것입니다. 진행 줄은 한 줄을 덮어쓰며 갱신되고 끝날 때 마지막 통계 3줄이 이어집니다.

```bash
# 백그라운드로 돌리고 1초 뒤 USR1 을 보낸다. 통계만 찍고 복사는 이어진다
#   kill -USR1   프로세스에 USR1 시그널을 보낸다
dd \
  if=/dev/zero \
  of=/dev/null \
  bs=1M \
  count=200000 &
pid=$!
sleep 1
kill -USR1 $pid

# 통계를 확인한 뒤 TERM 으로 끝낸다
sleep 0.3
kill $pid
```

```bash
26993+0 records in
26993+0 records out
28304211968 bytes (28 GB, 26 GiB) copied, 1.01163 s, 28.0 GB/s
dd: warning: partial read (356352 bytes); suggest iflag=fullblock
```

`USR1` 은 `dd` 가 통계를 찍고 복사를 이어 가게 하는 시그널이며, 보내는 법은 [kill·pgrep·pkill·killall 참조 시트](../process/kill%C2%B7pgrep%C2%B7killall.md)에 있습니다.[^usr1] 마지막 경고는 매번 나지는 않으며 「짧은 읽기와 fullblock」 에서 풉니다.

### 짧은 읽기와 fullblock

> 입력이 블록을 다 채우지 못한 채 돌아오는 짧은 읽기가 `count` 의 뜻을 바꾸고, `iflag=fullblock` 이 이를 막습니다.

```bash
# 앞 3바이트, 0.5초 쉼, 뒤 3바이트를 파이프로 흘린다
# 4바이트 블록 둘을 바랐지만 읽기 두 번이 3바이트씩만 받는다
{ printf aaa; sleep 0.5; printf bbb; } | dd \
  bs=4 \
  count=2 \
  of=p1.out
```

```bash
dd: warning: partial read (3 bytes); suggest iflag=fullblock
0+2 records in
0+2 records out
6 bytes copied, 0.509634 s, 0.0 kB/s
```

`0+2` 는 온전한 블록 0개와 짧은 블록 2개이며, 짧은 읽기가 났다는 경고가 붙었습니다. 이 경고는 `count=` 가 있을 때 나옵니다.

```bash
# 뒤 입력을 늘려 count=2 가 몇 바이트를 옮기는지 본다. 4바이트씩 두 블록이면 8바이트다
{ printf aaa; sleep 0.5; printf bbbbbbbbbbbb; } | dd \
  bs=4 \
  count=2 \
  of=p2.out
```

```bash
dd: warning: partial read (3 bytes); suggest iflag=fullblock
1+1 records in
1+1 records out
7 bytes copied, 0.512852 s, 0.0 kB/s
```

```bash
# fullblock 을 주면 블록이 찰 때까지 읽어 8바이트를 옮긴다
#   iflag=fullblock   입력 한 블록이 찰 때까지 읽는다
{ printf aaa; sleep 0.5; printf bbbbbbbbbbbb; } | dd \
  bs=4 \
  count=2 \
  iflag=fullblock \
  of=p3.out
```

```bash
2+0 records in
2+0 records out
8 bytes copied, 0.505126 s, 0.0 kB/s
```

`fullblock` 이 없으면 `count=` 는 블록 수가 아니라 읽기 호출 수를 셉니다.[^fullblock] `USR1` 이 읽기를 끊어도 짧은 읽기가 생기며, 이 VM 에서는 블록이 클수록 자주 났습니다.[^signal-short]

```bash
# 256MiB 블록으로 USR1 을 보내면 읽는 도중에 시그널이 닿아 경고가 붙는다
dd \
  if=/dev/zero \
  of=/dev/null \
  bs=256M \
  count=1000 &
pid=$!
sleep 1
kill -USR1 $pid
sleep 0.3
kill $pid
```

```bash
86+0 records in
86+0 records out
23085449216 bytes (23 GB, 22 GiB) copied, 1.00762 s, 22.9 GB/s
dd: warning: partial read (182341632 bytes); suggest iflag=fullblock
```

```bash
# 같은 호출에 fullblock 을 주면 경고가 없다
dd \
  if=/dev/zero \
  of=/dev/null \
  bs=256M \
  count=1000 \
  iflag=fullblock &
pid=$!
sleep 1
kill -USR1 $pid
sleep 0.3
kill $pid
```

```bash
99+0 records in
99+0 records out
26575110144 bytes (27 GB, 25 GiB) copied, 1.00434 s, 26.5 GB/s
```

이 블록은 세 번 쳐서 세 번 모두 경고가 났고 `fullblock` 을 준 세 번에는 없었습니다. 위 출력은 그 가운데 한 번입니다.

### 쓰기 처리량과 페이지 캐시

> 기본 `dd` 는 페이지 캐시에 쓰고 끝나므로, 디스크까지 걸린 시간을 재려면 `conv=fdatasync` 나 `oflag=direct` 를 줍니다.

```bash
# 같은 512MiB 를 세 방식으로 디스크 위 폴더에 쓴다. 매번 sync 로 앞 쓰기를 비운 뒤 시작한다
#   conv=fdatasync   끝내기 전에 출력 데이터를 디스크에 쓴다
#   oflag=direct     페이지 캐시를 거치지 않고 직접 입출력으로 쓴다
#   2>&1 | tail -n 1   통계 3줄 중 속도 줄만 남긴다
sync
dd \
  if=/dev/zero \
  of=/var/tmp/lab-dd/w.img \
  bs=1M \
  count=512 2>&1 | tail -n 1

# 기본 쓰기 직후 아직 디스크에 쓰지 못한 양(Dirty)을 본다
grep -E '^Dirty' /proc/meminfo

sync
dd \
  if=/dev/zero \
  of=/var/tmp/lab-dd/w.img \
  bs=1M \
  count=512 \
  conv=fdatasync 2>&1 | tail -n 1

sync
dd \
  if=/dev/zero \
  of=/var/tmp/lab-dd/w.img \
  bs=1M \
  count=512 \
  oflag=direct 2>&1 | tail -n 1
```

```bash
536870912 bytes (537 MB, 512 MiB) copied, 0.127677 s, 4.2 GB/s
Dirty:            524336 kB
536870912 bytes (537 MB, 512 MiB) copied, 0.522511 s, 1.0 GB/s
536870912 bytes (537 MB, 512 MiB) copied, 0.106458 s, 5.0 GB/s
```

기본 쓰기 직후 `Dirty` 가 512MiB 가까이 남았으니 `dd` 는 데이터가 디스크에 닿기 전에 끝난 것입니다. 디스크 쪽 처리량과 대기 시간은 [iostat 참조 시트](../resource/iostat.md)의 `iostat -x` 로 봅니다.[^fdatasync]

### 실습 정리

```bash
# ext4 이미지를 떼고 실습 폴더 둘을 지운다. 루프 장치가 남지 않았는지도 본다
cd /
umount /tmp/lab-dd/ext4
losetup -a | grep lab-dd || echo "no loop"
rm -r /tmp/lab-dd /var/tmp/lab-dd
```



## 주의사항과 동작 원리

### uutils 판 dd 와의 차이

> Ubuntu 26.04 의 기본 `dd` 는 짧은 읽기에 경고를 내지 않고, 오류 문구가 다르며, 블록이 작은 `oflag=direct` 쓰기도 막지 않습니다.

uutils 의 `fullblock` 설명은 "wait for ibs bytes from each read" 입니다.[^uutils] 아래 예는 「실습 정리」 를 치기 전에 돌리며, 통계의 `0+2` 는 GNU 판과 같지만 경고 줄이 없습니다.

```bash
# 「짧은 읽기와 fullblock」 의 첫 예를 기본 /usr/bin/dd 로 돌린다
/usr/bin/dd --version | head -n 1
{ printf aaa; sleep 0.5; printf bbb; } | /usr/bin/dd \
  bs=4 \
  count=2 \
  of=p4.out
```

```bash
dd (uutils coreutils) 0.10.0
0+2 records in
0+2 records out
6 bytes copied, 0.503088 s, 11 B/s
```

경고 없는 같은 차이가 `USR1` 통계에서도 나서, 짧은 읽기는 `82+1 records in` 처럼 `+1` 로만 드러났습니다. 속도는 `28 GB/s`·`11 B/s` 처럼 정수에 단위를 붙여 찍고, 오류 문구와 `oflag=direct` 결과는 아래처럼 갈립니다.

```bash
# GNU 판과 문구가 다른 오류와 종료 코드. 「변환과 출력 파일 제어」 의 out.txt 가 있을 때 친다
/usr/bin/dd bogus=1; echo $?
/usr/bin/dd bs=0 </dev/null; echo $?
/usr/bin/dd \
  if=src.txt \
  of=out.txt \
  conv=excl; echo $?
```

```bash
dd: Unrecognized operand 'bogus=1'
1
dd: invalid number: ‘0’
1
dd: failed to open 'out.txt': Already exists
1
```

GNU 판은 같은 호출에 `unrecognized operand` 와 `Try 'dd --help'` 줄, `invalid number: '0'`, `File exists` 를 찍었습니다. 종료 코드는 모두 1 로 같았습니다.

### oflag=direct 와 블록 크기

> `oflag=direct` 에 512 의 배수가 아닌 블록을 주면 ext4 는 실패하고 이 VM 의 btrfs 는 성공했습니다.

info 는 ext4 대상에서 출력 버퍼 크기가 512 의 배수가 아니면 쓰기가 `EINVAL` 로 실패한다고 적습니다.[^direct] 아래 예도 「실습 정리」 를 치기 전에 돌리며, 같은 `bs=1` 호출이 ext4 이미지와 btrfs 루트에서 갈립니다.

```bash
# ext4 이미지에 bs=1, bs=512 로 쓰고 btrfs 위 폴더에 bs=1 로 쓴다
dd \
  if=/dev/zero \
  of=/tmp/lab-dd/ext4/w.img \
  bs=1 \
  count=100 \
  oflag=direct
dd \
  if=/dev/zero \
  of=/tmp/lab-dd/ext4/w.img \
  bs=512 \
  count=100 \
  oflag=direct
dd \
  if=/dev/zero \
  of=/var/tmp/lab-dd/w.img \
  bs=1 \
  count=100 \
  oflag=direct
```

```bash
dd: error writing '/tmp/lab-dd/ext4/w.img': Invalid argument
1+0 records in
0+0 records out
0 bytes copied, 0.000755253 s, 0.0 kB/s
100+0 records in
100+0 records out
51200 bytes (51 kB, 50 KiB) copied, 0.00542505 s, 9.4 MB/s
100+0 records in
100+0 records out
100 bytes copied, 0.00111752 s, 89.5 kB/s
```

uutils 판 `/usr/bin/dd` 로 같은 ext4 쓰기를 치면 100바이트를 쓰고 종료 코드 0 으로 끝났습니다.

### 처리량의 실행별 편차

> 같은 쓰기도 칠 때마다 값이 크게 흔들려 한 번 잰 값으로 기본·`fdatasync`·`direct` 의 우열을 정하지 않습니다.

「쓰기 처리량과 페이지 캐시」 의 한 번에서는 기본 쓰기가 `Dirty` 를 크게 남겼습니다. 같은 세 방식을 「실습 정리」 전에 세 번 돌려 보면 값이 이렇게 갈립니다.

```bash
# 방식마다 세 번 돌리고 기본 쓰기 직후의 Dirty 도 읽는다
for t in 1 2 3; do
  sync
  dd \
    if=/dev/zero \
    of=/var/tmp/lab-dd/w.img \
    bs=1M \
    count=512 2>&1 | tail -n 1
  grep -E '^Dirty' /proc/meminfo
  sync
  dd \
    if=/dev/zero \
    of=/var/tmp/lab-dd/w.img \
    bs=1M \
    count=512 \
    conv=fdatasync 2>&1 | tail -n 1
  sync
  dd \
    if=/dev/zero \
    of=/var/tmp/lab-dd/w.img \
    bs=1M \
    count=512 \
    oflag=direct 2>&1 | tail -n 1
done
```

```bash
536870912 bytes (537 MB, 512 MiB) copied, 0.208942 s, 2.6 GB/s
Dirty:                48 kB
536870912 bytes (537 MB, 512 MiB) copied, 0.201056 s, 2.7 GB/s
536870912 bytes (537 MB, 512 MiB) copied, 0.0766168 s, 7.0 GB/s
536870912 bytes (537 MB, 512 MiB) copied, 0.22864 s, 2.3 GB/s
Dirty:                48 kB
536870912 bytes (537 MB, 512 MiB) copied, 0.227245 s, 2.4 GB/s
536870912 bytes (537 MB, 512 MiB) copied, 0.0989566 s, 5.4 GB/s
536870912 bytes (537 MB, 512 MiB) copied, 0.183201 s, 2.9 GB/s
Dirty:                48 kB
536870912 bytes (537 MB, 512 MiB) copied, 0.233607 s, 2.3 GB/s
536870912 bytes (537 MB, 512 MiB) copied, 0.0905192 s, 5.9 GB/s
```

세 번 모두 `Dirty` 는 48kB 로 거의 비었고 기본 쓰기와 `fdatasync` 의 시간 차이도 작았습니다. 「쓰기 처리량과 페이지 캐시」 의 `fdatasync` 는 1.0 GB/s 였으니 방식은 여러 번 쳐서 범위로 견줍니다.



## 관련 문서

> 이 시트의 예와 이어지는 시트와 책 노트입니다.

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [df·du 참조 시트](./df·du.md) — `dd` 가 만든 희소 파일과 디스크 사용량을 재는 법
- [iostat 참조 시트](../resource/iostat.md) — 쓰기 처리량과 대기 시간을 장치 쪽에서 보는 법
- [kill·pgrep·pkill·killall 참조 시트](../process/kill%C2%B7pgrep%C2%B7killall.md) — `kill -USR1` 처럼 시그널을 이름으로 보내는 법
- [자원마다 창이 따로 나 있어 어느 창을 여느냐가 곧 진단이다](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md) — 장치의 입출력 창과 지워도 공간이 안 돌아오는 파일
- [시그널은 번호 하나만 보내고 끝나는 모양은 처리 방식이 정한다](../../../book/learning-modern-linux/09-02.%EC%8B%9C%EA%B7%B8%EB%84%90%EC%9D%80%20%EB%B2%88%ED%98%B8%20%ED%95%98%EB%82%98%EB%A7%8C%20%EB%B3%B4%EB%82%B4%EA%B3%A0%20%EB%81%9D%EB%82%98%EB%8A%94%20%EB%AA%A8%EC%96%91%EC%9D%80%20%EC%B2%98%EB%A6%AC%20%EB%B0%A9%EC%8B%9D%EC%9D%B4%20%EC%A0%95%ED%95%9C%EB%8B%A4.md) — `USR1` 을 쓰는 자리



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- 검증 환경: Ubuntu 26.04 VM(OrbStack, aarch64), `dd` 는 gnu-coreutils 9.7-3ubuntu2.1 의 `gnudd`, 기본 `dd` 는 rust-coreutils 0.10.0 — 2026-11-16 실측
- GNU coreutils 9.7 의 `dd --help`·`man dd`·`info coreutils` 원문 — 같은 VM 에서 2026-11-16 확인
- [gnudd(1) — Ubuntu 26.04](https://manpages.ubuntu.com/manpages/resolute/man1/gnudd.1.html)
- [GNU coreutils 매뉴얼 — dd invocation](https://www.gnu.org/software/coreutils/manual/html_node/dd-invocation.html)

[^bsd]: macOS 26.6 `dd --help` 는 "dd: unknown operand --help" 로 실패합니다. `man dd` — "If dd receives a SIGINFO (see the status argument for stty(1)) signal, the current input and output block counts will be written to the standard error output in the same format as the standard completion message." fullblock 도 같은 문서에 있습니다.
[^dd-help]: `dd --help` (GNU coreutils 9.7) — "N and BYTES may be followed by the following multiplicative suffixes: c=1, w=2, b=512, kB=1000, K=1024, MB=1000*1000, M=1024*1024, xM=M, GB=1000*1000*1000, G=1024*1024*1024, and so on for T, P, E, Z, Y, R, Q. Binary prefixes can be used, too: KiB=K, MiB=M, and so on." <https://manpages.ubuntu.com/manpages/resolute/man1/gnudd.1.html>
[^status]: GNU coreutils 9.7 `info coreutils`, "dd invocation" 의 `status=` — "The notation 'W+P' stands for W whole blocks and P partial blocks. A partial block occurs when a read or write operation succeeds but transfers less data than the block size.", "progress: Print the transfer rate and volume statistics on standard error, when processing each input block. Statistics are output on a single line at most once every second, but updates can be delayed when waiting on I/O." <https://www.gnu.org/software/coreutils/manual/html_node/dd-invocation.html>
[^usr1]: `man dd` (GNU coreutils 9.7) — "Sending a USR1 signal to a running 'dd' process makes it print I/O statistics to standard error and then resume copying." <https://manpages.ubuntu.com/manpages/resolute/man1/gnudd.1.html>
[^fullblock]: GNU coreutils 9.7 `info coreutils`, "dd invocation" 의 `iflag=fullblock` — "This flag is useful with pipes for example as they may return short reads. In that case, this flag is needed to ensure that a 'count=' argument is interpreted as a block count rather than a count of read operations." macOS `man dd` 도 "Without this flag, count limits the number of times read(2) is called on the input rather than the number of blocks copied in full." 라고 적습니다. <https://www.gnu.org/software/coreutils/manual/html_node/dd-invocation.html>
[^signal-short]: GNU coreutils 9.7 `info coreutils`, "dd invocation" 의 `USR1` 예 — "Run dd with the fullblock iflag to avoid short reads which can be triggered by reception of signals." 블록 크기에 따라 경고가 나는 빈도가 다른 것은 이 시트의 실측입니다. <https://www.gnu.org/software/coreutils/manual/html_node/dd-invocation.html>
[^fdatasync]: GNU coreutils 9.7 `info coreutils`, "dd invocation" 의 `conv=fdatasync` — "Synchronize output data just before finishing, even if there were write errors. This forces a physical write of output data, so that even if power is lost the output data will be preserved. If neither this nor 'fsync' are specified, output is treated as usual with file systems, i.e., output data and metadata may be cached in primary memory for some time before the operating system physically writes it". <https://www.gnu.org/software/coreutils/manual/html_node/dd-invocation.html>
[^direct]: GNU coreutils 9.7 `info coreutils`, "dd invocation" 의 `direct` — "Use direct I/O for data, avoiding the buffer cache. The kernel may impose restrictions on read or write buffer sizes. For example, with an ext4 destination file system and a Linux-based kernel, using 'oflag=direct' will cause writes to fail with 'EINVAL' if the output buffer size is not a multiple of 512." btrfs 에서 성공한 것은 이 시트의 실측입니다. <https://www.gnu.org/software/coreutils/manual/html_node/dd-invocation.html>
[^uutils]: `/usr/bin/dd --help` (uutils coreutils 0.10.0) — "fullblock : wait for ibs bytes from each read. zero-length reads are still considered EOF." 경고가 나지 않는 것은 이 시트의 실측입니다.
[^exit]: `man dd` 에는 종료 코드 절이 없습니다. GNU coreutils 9.7 `info coreutils`, "dd invocation" — "An exit status of zero indicates success, and a nonzero value indicates failure." 코드 1 은 이 시트의 실측입니다. <https://www.gnu.org/software/coreutils/manual/html_node/dd-invocation.html>
