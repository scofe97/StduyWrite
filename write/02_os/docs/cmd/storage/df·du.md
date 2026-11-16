---
title: df·du 참조 시트
tags: [linux, cheatsheet, df, du, disk, inode, storage, cli, reference]
status: draft
source:
  - GNU coreutils 9.7 의 `df --help`·`du --help` 원문과 `info coreutils` 의 "df invocation"·"du invocation" (Ubuntu 26.04 gnu-coreutils 9.7-3ubuntu2.1)
  - macOS 26.6 df(1)·du(1) (`man` 원문, 다르게 동작하는 환경)
related:
  - ../README.md
  - ../resource/lsof.md
  - ../service/journalctl 저장 공간과 읽기 권한.md
  - ../text/sort·uniq·wc.md
  - ../../../book/learning-modern-linux/08-01.%EC%9E%AC%EB%8A%94%20%EA%B2%83%EC%9D%80%20%EB%B0%94%EA%B9%A5%EC%9D%B4%EA%B3%A0%20%EC%95%8C%EA%B3%A0%20%EC%8B%B6%EC%9D%80%20%EA%B2%83%EC%9D%80%20%EC%95%88%EC%9D%B4%EB%8B%A4.md
  - ../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md
updated: 2026-11-16
---

# df·du 참조 시트

---

> 파일시스템이 얼마나 찼는지 `df` 로, 디렉터리가 얼마를 쓰는지 `du` 로 재는 법을 inode 고갈, 큰 디렉터리 찾기, 둘의 값이 어긋나는 경우까지 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `df` 는 파일시스템 단위의 사용량을, `du` 는 경로 아래 파일이 쓰는 디스크를 찍습니다.

둘 다 coreutils 의 외부 바이너리입니다. 이 시트는 Ubuntu 26.04 VM 에서 실측했습니다. 이 판의 `/usr/bin/df` 는 GNU coreutils 9.7(`gnudf`)이지만 `/usr/bin/du` 는 uutils 0.10.0 입니다.

그래서 「실습 준비」 에서 GNU 판 `gnudu` 를 `du` 이름으로 앞세웠습니다. uutils 판도 이 시트의 `du` 예를 모두 같은 값과 오류 문구로 찍었습니다. macOS 의 BSD `df`·`du` 는 옵션이 다릅니다. `df -T` 는 종류 열을 더하는 옵션이 아니라 종류를 고르는 옵션이고, 겉보기 크기는 `du -A` 입니다.[^bsd]



## 핵심 문법

> `df` 는 인자로 준 경로가 놓인 파일시스템을, `du` 는 인자로 준 경로 아래를 걸어 얻은 크기를 찍습니다.

```bash
# 호출 형태 (df --help 의 Usage 줄)
df [OPTION]... [FILE]...

# 호출 형태 (du --help 의 Usage 줄)
du [OPTION]... [FILE]...
du [OPTION]... --files0-from=F

# 마운트된 파일시스템 전부의 사용량을 찍는다 (파일시스템 사용량 보기)
df -h

# 경로가 놓인 파일시스템만 찍고 종류 열을 더한다 (경로가 놓인 파일시스템 찾기)
df -hT 경로

# 블록 대신 inode 사용량을 찍는다 (inode 고갈 확인)
df -i 경로

# 디렉터리 합계 한 줄과 한 단계 아래 항목별 합계 (디렉터리 크기 재기)
du -sh 경로
du -h -d 1 경로

# 한 단계 아래를 크기순으로 정렬한다 (큰 디렉터리 찾기)
du -h -d 1 경로 | sort -h

# 크기 대신 inode 수를 세어 파일이 몰린 폴더를 찾는다 (큰 디렉터리 찾기)
du --inodes -s 경로/*

# 다른 파일시스템에 마운트된 하위 디렉터리를 뺀다 (다른 파일시스템 건너뛰기)
du -sh -x 경로

# 디스크 사용량 대신 겉보기 크기를 찍는다 (겉보기 크기와 실제 사용량)
du -h --apparent-size 경로
```

### df 출력 열

> `df` 의 기본 출력과 `-T`·`-i` 를 줄 때 붙는 열입니다. 이름은 `--output` 에 쓰는 필드 이름과 같습니다.[^df-fields]

```bash
# 열            --output 필드   뜻
# Filesystem    source          마운트의 원천. 보통 장치
# Type          fstype          파일시스템 종류. -T 를 줄 때만 붙는다
# Size          size            전체 블록 수
# Used          used            쓴 블록 수
# Avail         avail           남은 블록 수
# Use%          pcent           Used 를 Size 로 나눈 비율
# Mounted on    target          마운트 위치
# Inodes        itotal          전체 inode 수. -i 를 줄 때 Size 자리에 온다
# IUsed         iused           쓴 inode 수
# IFree         iavail          남은 inode 수
# IUse%         ipcent          IUsed 를 Inodes 로 나눈 비율
```



## 종료 코드

> `df` 와 `du` 는 성공하면 0, 실패하면 0 이 아닌 값을 돌려주며 이 시트의 실패는 모두 1 이었습니다.[^exit]

```bash
# 0  성공. 출력이 있었을 때
# 1  실패. 없는 경로, 모르는 옵션을 줬을 때
#    df 는 종류가 맞는 파일시스템이 없을 때도 1 이다

# 없는 경로
df /nonexistent; echo $?    # df: /nonexistent: No such file or directory / 1
du /nonexistent; echo $?
# du: cannot access '/nonexistent': No such file or directory / 1

# 모르는 옵션
df --badopt; echo $?
# df: unrecognized option '--badopt' / Try 'df --help' for more information. / 1
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다. 종류가 맞는 파일시스템이 없을 때의 실패는 「경로가 놓인 파일시스템 찾기」 에서 보입니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션과 만든 상태만 씁니다.

### 실습 준비

> 아래 블록을 root 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 디렉터리와 작은 tmpfs 셋이 생깁니다.

OrbStack 의 Ubuntu 26.04 VM 에서 `sudo -i` 로 root 가 된 뒤 실행합니다. 모든 파일은 `/tmp/lab-du/` 아래에만 만들고 끝에 「실습 정리」 로 지웁니다.

```bash
# Ubuntu 26.04 의 du 는 기본이 uutils 판이라 GNU 판 gnudu 를 du 이름으로 앞세운다
# Debian·RHEL 처럼 GNU coreutils 를 쓰는 배포판에서는 이 세 줄이 필요 없다
mkdir -p /tmp/lab-du/bin
ln -s /usr/bin/gnudu /tmp/lab-du/bin/du
export PATH=/tmp/lab-du/bin:$PATH

# 「디렉터리 크기 재기」 부터 여러 곳이 쓰는 디렉터리 트리
mkdir -p /tmp/lab-du/tree/{app,logs,data,mnt}

# tree/mnt 에는 별도 tmpfs 를 얹는다. 「다른 파일시스템 건너뛰기」 에서 쓴다
mount -t tmpfs -o size=20m tmpfs /tmp/lab-du/tree/mnt

# 「파일시스템 사용량 보기」 부터 여러 곳이 쓰는 20MiB 짜리 tmpfs
mkdir -p /tmp/lab-du/small
mount -t tmpfs -o size=20m tmpfs /tmp/lab-du/small

# 「inode 고갈 확인」 과 「큰 디렉터리 찾기」 가 쓰는 inode 100개짜리 tmpfs
mkdir -p /tmp/lab-du/inode
mount -t tmpfs -o size=20m,nr_inodes=100 tmpfs /tmp/lab-du/inode

# 크기가 정해진 파일을 만든다
#   head -c N   입력 앞에서 N바이트만 복사한다. 2M 은 2MiB 다
head -c 2M /dev/zero > /tmp/lab-du/tree/app/app.bin
head -c 5M /dev/zero > /tmp/lab-du/tree/logs/app.log
head -c 1M /dev/zero > /tmp/lab-du/tree/logs/old.log
head -c 8M /dev/zero > /tmp/lab-du/tree/mnt/other.bin

# 3바이트 파일과 100MiB 로 늘린 희소 파일. 「겉보기 크기와 실제 사용량」 에서 쓴다
#   truncate -s N   파일 크기를 N 으로 맞춘다. 늘린 구간은 빈 구멍이다
echo hi > /tmp/lab-du/tree/data/tiny.txt
truncate -s 100M /tmp/lab-du/tree/data/sparse.img
```

`tree` 아래에는 2MiB 짜리 `app`, 6MiB 짜리 `logs`, 희소 파일이 든 `data`, 별도 tmpfs 에 8MiB 가 든 `mnt` 가 있습니다.

### 파일시스템 사용량 보기

> `df -h` 는 파일시스템마다 크기·사용량·남은 양·사용률·마운트 위치를 한 줄씩 찍습니다.

인자 없이 친 `df -h` 의 전체 목록은 이 VM 의 마운트 이름이 드러나 싣지 않았습니다. 아래는 경로 둘로 좁힌 결과입니다.

```bash
# 루트 파일시스템과 작은 tmpfs 의 사용량을 사람이 읽는 단위로 찍는다
#   df -h   크기를 1024 의 거듭제곱 단위(K, M, G)로 찍는다
df -h / /tmp/lab-du/small
```

```bash
Filesystem      Size  Used Avail Use% Mounted on
/dev/vdb1        88G   33G   55G  38% /
tmpfs            20M     0   20M   0% /tmp/lab-du/small
```

첫 줄의 `Size`·`Used` 는 이 VM 의 디스크 값이라 환경마다 다릅니다.

```bash
# 옵션이 없으면 1024바이트 블록 수로 찍는다
df /tmp/lab-du/small

# 같은 파일시스템을 1000 의 거듭제곱 단위로 찍는다. 20MiB 가 21MB 로 보인다
#   df -H   크기를 1000 의 거듭제곱 단위(SI)로 찍는다
df -H /tmp/lab-du/small
```

```bash
Filesystem     1K-blocks  Used Available Use% Mounted on
tmpfs              20480     0     20480   0% /tmp/lab-du/small
Filesystem      Size  Used Avail Use% Mounted on
tmpfs            21M     0   21M   0% /tmp/lab-du/small
```

### 경로가 놓인 파일시스템 찾기

> 경로를 인자로 주면 그 경로가 든 파일시스템만 찍히고, `-T` 를 더하면 종류를 알 수 있습니다.

```bash
# 로그 폴더가 든 파일시스템의 종류와 마운트 위치를 본다
#   df -T   종류(Type) 열을 더한다
df -hT /var/log /tmp/lab-du/small
```

```bash
Filesystem     Type   Size  Used Avail Use% Mounted on
/dev/vdb1      btrfs   88G   33G   55G  38% /
tmpfs          tmpfs   20M     0   20M   0% /tmp/lab-du/small
```

`/var/log` 는 따로 마운트되지 않아 루트 파일시스템(`/`)의 한 줄로 나옵니다.

```bash
# 마운트 위치 한 줄만 뽑는다. 스크립트에서 경로의 파일시스템을 알아낼 때 쓴다
#   df --output=목록   찍을 열을 쉼표로 고른다. target 은 마운트 위치다
df --output=target /var/log/journal | tail -n 1    # /
```

```bash
# 종류로 거른다. 루트와 tmpfs 둘 가운데 tmpfs 만 남기거나 뺀다
#   df -t 종류   그 종류의 파일시스템만 남긴다 (--type)
#   df -x 종류   그 종류의 파일시스템을 뺀다 (--exclude-type)
df -h -t tmpfs / /tmp/lab-du/small
df -h -x tmpfs / /tmp/lab-du/small
```

```bash
Filesystem      Size  Used Avail Use% Mounted on
tmpfs            20M     0   20M   0% /tmp/lab-du/small
Filesystem      Size  Used Avail Use% Mounted on
/dev/vdb1        88G   33G   55G  38% /
```

```bash
# 종류가 맞는 파일시스템이 없으면 출력 없이 실패한다
df -t ext4 /; echo $?    # df: no file systems processed / 1
```

위 블록의 `/` 는 두 줄로 나온 출력을 한 줄에 줄여 적은 것입니다. 이 실패를 이용하면 `df -t ext4 경로` 의 종료 코드로 그 경로가 `ext4` 위에 있는지 가릴 수 있습니다.[^exit]

### inode 고갈 확인

> 파일 수가 inode 한도에 닿으면 용량이 남아 있어도 파일을 만들 수 없고, `df -i` 가 그 한도를 보여 줍니다.

```bash
# inode 가 100개뿐인 tmpfs 에 빈 파일을 만들다가 한도에서 멈춘다
for i in $(seq 1 120); do
  touch /tmp/lab-du/inode/f$i || break
done
```

```bash
touch: cannot touch '/tmp/lab-du/inode/f100': No space left on device
```

```bash
# 용량은 거의 비어 있는데 inode 는 100% 다
#   df -i   블록 대신 inode 사용량을 찍는다
df -h /tmp/lab-du/inode
df -i /tmp/lab-du/inode
```

```bash
Filesystem      Size  Used Avail Use% Mounted on
tmpfs            20M     0   20M   0% /tmp/lab-du/inode
Filesystem     Inodes IUsed IFree IUse% Mounted on
tmpfs             100   100     0  100% /tmp/lab-du/inode
```

파일은 99개가 만들어졌고 `IUsed` 는 100 입니다. 파일을 하나도 만들기 전에 `df -i` 를 치면 `IUsed` 가 1 이라 나머지 하나는 마운트 루트 디렉터리가 씁니다.

### 디렉터리 크기 재기

> `du -sh` 는 디렉터리 합계 한 줄을, `-d N` 은 N 단계 아래 항목마다 합계를 찍습니다.

```bash
# 디렉터리 합계 한 줄. mnt 의 8MiB 도 더해져 17M 다
#   du -s   인자마다 합계만 찍는다
#   du -h   크기를 사람이 읽는 단위로 찍는다
du -sh /tmp/lab-du/tree
```

```bash
17M	/tmp/lab-du/tree
```

```bash
# 한 단계 아래 항목마다 합계를 찍는다. 출력 순서는 크기순이 아니다
#   du -d N   N 단계 아래까지 항목마다 합계를 찍는다. 0 은 -s 와 같다
du -h -d 1 /tmp/lab-du/tree
```

```bash
8.0M	/tmp/lab-du/tree/mnt
4.0K	/tmp/lab-du/tree/data
6.0M	/tmp/lab-du/tree/logs
2.0M	/tmp/lab-du/tree/app
17M	/tmp/lab-du/tree
```

`data` 가 4.0K 인 것은 희소 파일이 디스크를 거의 쓰지 않기 때문이며 「겉보기 크기와 실제 사용량」 에서 다룹니다.

```bash
# 파일마다 한 줄씩 찍는다
#   du -a   디렉터리뿐 아니라 파일도 줄로 찍는다
du -ah /tmp/lab-du/tree/logs

# 인자 여럿의 합계를 마지막 줄에 더한다
#   du -c   마지막에 합계(total) 줄을 더한다
du -ch /tmp/lab-du/tree/app /tmp/lab-du/tree/logs
```

```bash
1.0M	/tmp/lab-du/tree/logs/old.log
5.0M	/tmp/lab-du/tree/logs/app.log
6.0M	/tmp/lab-du/tree/logs
2.0M	/tmp/lab-du/tree/app
6.0M	/tmp/lab-du/tree/logs
8.0M	total
```

### 큰 디렉터리 찾기

> `du` 출력을 `sort -h` 에 넘기면 어느 디렉터리가 큰지 정렬된 끝줄에서 읽습니다.

```bash
# 한 단계 아래를 작은 것부터 정렬한다. 큰 것이 맨 아래로 온다
#   sort -h   4.0K, 2.0M 같은 단위 접미사를 크기로 읽어 정렬한다
du -h -d 1 /tmp/lab-du/tree | sort -h
```

```bash
4.0K	/tmp/lab-du/tree/data
2.0M	/tmp/lab-du/tree/app
6.0M	/tmp/lab-du/tree/logs
8.0M	/tmp/lab-du/tree/mnt
17M	/tmp/lab-du/tree
```

```bash
# 파일까지 큰 순서로 위 4줄만 본다
#   sort -r     정렬을 뒤집는다. -h 와 함께 -rh 로 쓴다
#   head -n 4   앞 4줄만 남긴다
du -ah /tmp/lab-du/tree | sort -rh | head -n 4
```

```bash
17M	/tmp/lab-du/tree
8.0M	/tmp/lab-du/tree/mnt/other.bin
8.0M	/tmp/lab-du/tree/mnt
6.0M	/tmp/lab-du/tree/logs
```

```bash
# 파일 수가 많은 하위 폴더를 찾는다. inode 폴더에 파일 99개가 몰려 있다
#   du --inodes   크기 대신 inode 수를 센다
#   sort -n       맨 앞 숫자를 수로 읽어 정렬한다
du --inodes -s /tmp/lab-du/* | sort -n | tail -n 2
```

```bash
11	/tmp/lab-du/tree
100	/tmp/lab-du/inode
```

`sort` 의 옵션은 [sort·uniq·wc 참조 시트](../text/sort%C2%B7uniq%C2%B7wc.md)에 있습니다.

### 다른 파일시스템 건너뛰기

> `-x` 는 인자와 다른 파일시스템에 마운트된 하위 디렉터리를 세지 않습니다.

```bash
# tree 안의 mnt 는 별도 tmpfs 라 -x 를 주면 8MiB 가 빠진다
#   du -x   인자와 다른 파일시스템에 있는 디렉터리는 건너뛴다 (--one-file-system)
du -sh -x /tmp/lab-du/tree
du -sh /tmp/lab-du/tree
```

```bash
8.1M	/tmp/lab-du/tree
17M	/tmp/lab-du/tree
```

`/` 아래를 잴 때 `-x` 를 주면 `/proc`·`/run` 같은 다른 파일시스템이 합계에 섞이지 않습니다.

### 겉보기 크기와 실제 사용량

> `du` 의 기본값은 디스크를 쓴 양이라 3바이트 파일은 한 블록으로, 희소 파일은 거의 0 으로 나옵니다.

```bash
# 3바이트 파일이 디스크에서는 4.0K 를 쓴다. -b 로 겉보기 3바이트를 확인한다
#   du -b   바이트 단위 겉보기 크기로 찍는다 (--apparent-size --block-size=1)
du -h /tmp/lab-du/tree/data/tiny.txt
du -b /tmp/lab-du/tree/data/tiny.txt
```

```bash
4.0K	/tmp/lab-du/tree/data/tiny.txt
3	/tmp/lab-du/tree/data/tiny.txt
```

```bash
# 100MiB 로 늘린 희소 파일은 디스크 사용량이 0 이고 겉보기 크기가 100M 다
#   du --apparent-size   디스크 사용량 대신 겉보기 크기를 찍는다
du -h /tmp/lab-du/tree/data/sparse.img
du -h --apparent-size /tmp/lab-du/tree/data/sparse.img
```

```bash
0	/tmp/lab-du/tree/data/sparse.img
100M	/tmp/lab-du/tree/data/sparse.img
```

### 로그 디렉터리 크기 재기

> `/var/log` 는 `du -h -d 1` 에 `sort -h` 를 이어 큰 항목을 찾고, 저널은 `journalctl --disk-usage` 로 맞춰 봅니다.

```bash
# 로그 폴더 아래에서 큰 3줄을 본다. 값은 이 VM 의 저널 양이다
du -h -d 1 /var/log | sort -h | tail -n 3
```

```bash
64K	/var/log/apt
72M	/var/log/journal
76M	/var/log
```

```bash
# 저널 폴더만 재고 journalctl 이 센 값과 견준다
du -sh /var/log/journal
journalctl --disk-usage
```

```bash
72M	/var/log/journal
Archived and active journals take up 72M in the file system.
```

저널을 줄이는 `--vacuum-*` 는 [journalctl 저장 공간과 읽기 권한](../service/journalctl%20저장%20공간과%20읽기%20권한.md)에 있습니다.

### 지운 파일이 붙든 공간

> 지웠지만 프로세스가 열어 둔 파일은 `df` 에만 잡히고, 희소 파일의 구멍은 `du` 의 겉보기 크기에만 잡힙니다.

지운 파일을 찾는 `lsof +L1` 의 옵션은 [lsof 참조 시트](../resource/lsof.md)의 「지운 파일이 붙든 공간 찾기」 에 있습니다.

```bash
# 10MiB 로그를 만들고 sleep 이 읽기용으로 연 채 지운다
head -c 10M /dev/zero > /tmp/lab-du/small/app.log
sleep 300 < /tmp/lab-du/small/app.log &
pid=$!
rm /tmp/lab-du/small/app.log

# df 는 10MiB 를 쓴다고 하고 du 는 0 이다
#   df -BM   1MiB(1,048,576바이트) 단위로 찍는다 (--block-size=M)
df -BM /tmp/lab-du/small | tail -n 1
du -sh /tmp/lab-du/small
```

```bash
tmpfs                20M   10M       10M  50% /tmp/lab-du/small
0	/tmp/lab-du/small
```

```bash
# 링크 수(NLINK)가 0 인 열린 파일이 공간을 쥔 프로세스다
lsof +L1 /tmp/lab-du/small
```

```bash
COMMAND   PID USER FD   TYPE DEVICE SIZE/OFF NLINK NODE NAME
sleep   67652 root 0r   REG   0,96 10485760     0    2 /tmp/lab-du/small/app.log (deleted)
```

```bash
# 프로세스가 잡은 fd 로 파일을 비우면 공간이 돌아온다. 끝낼 수 없는 프로세스에 쓴다
: > /proc/$pid/fd/0
df -BM /tmp/lab-du/small | tail -n 1
kill $pid
```

```bash
tmpfs                20M    0M       20M   0% /tmp/lab-du/small
```

`: >` 로 비운 내용은 되살릴 수 없습니다. 이어서 희소 파일은 반대로 `df` 에 잡히지 않습니다.

```bash
# 20MiB 짜리 tmpfs 에 100MiB 희소 파일을 만든다. df 의 Used 는 그대로 0 이다
truncate -s 100M /tmp/lab-du/small/hole.img
du -h --apparent-size /tmp/lab-du/small/hole.img
df -BM /tmp/lab-du/small | tail -n 1
rm /tmp/lab-du/small/hole.img
```

```bash
100M	/tmp/lab-du/small/hole.img
tmpfs                20M    0M       20M   0% /tmp/lab-du/small
```

### 실습 정리

```bash
# tmpfs 를 떼고 실습 폴더를 지운다. 마운트가 남은 채 rm -r 을 치면 안 된다
umount /tmp/lab-du/tree/mnt /tmp/lab-du/small /tmp/lab-du/inode
rm -r /tmp/lab-du
```



## 주의사항과 동작 원리

### 인자 순서에 따른 합계 변화

> `du` 는 먼저 센 파일을 뒤 인자에서 다시 세지 않아 같은 경로를 순서만 바꿔 주면 값이 달라집니다.

`du` 는 한 번 센 파일을 다시 세지 않으며, 매뉴얼은 하드 링크에서 인자 순서가 어느 이름을 셀지 정한다고 적습니다.[^du-order] 아래는 저널 폴더가 든 `/var/log` 와 그 하위 `/var/log/journal` 을 두 순서로 준 결과입니다.

```bash
# 하위 폴더를 먼저 주면 /var/log 쪽에서는 저널 72M 가 빠진다
du -sh /var/log/journal /var/log
```

```bash
72M	/var/log/journal
3.5M	/var/log
```

```bash
# 상위를 먼저 주면 하위는 이미 센 것이라 줄이 나오지 않는다
du -sh /var/log /var/log/journal
```

```bash
76M	/var/log
```

폴더 여러 개의 합계를 비교할 때는 서로 겹치지 않는 경로만 한 번에 줍니다.

### -h 의 올림 표기

> `du -h` 는 반올림이 아니라 올림이라 8.0M 에 가까운 값도 8.1M 으로 찍습니다.

`-x` 로 잰 `tree` 는 8196KiB, 곧 8.004MiB 라 소수 첫째 자리에서 올려 8.1M 이 됩니다.[^round] 아래 예는 「실습 정리」 를 치기 전의 `tree` 로 돌립니다.

```bash
# 같은 값을 KiB 와 사람이 읽는 단위로 찍는다
#   du -k   1024바이트 단위(KiB)로 찍는다
du -sk -x /tmp/lab-du/tree
du -sh -x /tmp/lab-du/tree
```

```bash
8196	/tmp/lab-du/tree
8.1M	/tmp/lab-du/tree
```



## 관련 문서

> 이 시트의 예와 이어지는 시트와 책 노트입니다.

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [lsof 참조 시트](../resource/lsof.md) — 지운 파일을 연 프로세스를 `lsof +L1` 로 찾는 법
- [journalctl 저장 공간과 읽기 권한](../service/journalctl%20저장%20공간과%20읽기%20권한.md) — 저널이 디스크를 쓰는 양과 `--vacuum-*` 로 줄이는 법
- [sort·uniq·wc 참조 시트](../text/sort%C2%B7uniq%C2%B7wc.md) — `du` 출력을 크기순으로 정렬하는 `sort -h`
- [재는 것은 바깥이고 알고 싶은 것은 안이다](../../../book/learning-modern-linux/08-01.%EC%9E%AC%EB%8A%94%20%EA%B2%83%EC%9D%80%20%EB%B0%94%EA%B9%A5%EC%9D%B4%EA%B3%A0%20%EC%95%8C%EA%B3%A0%20%EC%8B%B6%EC%9D%80%20%EA%B2%83%EC%9D%80%20%EC%95%88%EC%9D%B4%EB%8B%A4.md) — `/var/log` 의 파일과 `du -sh` 로 크기를 확인하는 절
- [자원마다 창이 따로 나 있어 어느 창을 여느냐가 곧 진단이다](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md) — 지워도 공간이 안 돌아오는 파일



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- 검증 환경: Ubuntu 26.04 VM(OrbStack, aarch64), `df` 와 `du` 는 gnu-coreutils 9.7-3ubuntu2.1, 기본 `du` 는 rust-coreutils 0.10.0 — 2026-11-16 실측
- GNU coreutils 9.7 의 `df --help`·`du --help` 원문과 `info coreutils` — 같은 VM 에서 2026-11-16 확인
- [gnudf(1) — Ubuntu 26.04](https://manpages.ubuntu.com/manpages/resolute/man1/gnudf.1.html)
- [gnudu(1) — Ubuntu 26.04](https://manpages.ubuntu.com/manpages/resolute/man1/gnudu.1.html)
- [GNU coreutils 매뉴얼 — df invocation](https://www.gnu.org/software/coreutils/manual/html_node/df-invocation.html)
- [GNU coreutils 매뉴얼 — du invocation](https://www.gnu.org/software/coreutils/manual/html_node/du-invocation.html)

[^bsd]: macOS 26.6 `man du` — "-A Display the apparent size instead of the disk usage. This can be helpful when operating on compressed volumes or sparse files." 같은 문서의 `-d depth`·`-x` 는 이 시트와 같고, `man df` 는 "-T type Select file systems to display." 로 `-T` 를 종류 고르기로 적습니다.
[^df-fields]: GNU coreutils 9.7 `info coreutils`, "df invocation" 의 `--output` — "source: The source of the mount point, usually a device.", "fstype: File system type.", "itotal: Total number of inodes.", "iused: Number of used inodes.", "iavail: Number of available inodes.", "ipcent: Percentage of IUSED divided by ITOTAL.", "size: Total number of blocks.", "used: Number of used blocks.", "avail: Number of available blocks.", "pcent: Percentage of USED divided by SIZE.", "target: The mount point." <https://www.gnu.org/software/coreutils/manual/html_node/df-invocation.html>
[^exit]: `df(1)`·`du(1)` man 에는 종료 코드 절이 없습니다. GNU coreutils 9.7 `info coreutils` 의 "df invocation" 은 "An exit status of zero indicates success, and a nonzero value indicates failure. Failure includes the case where no output is generated, so you can inspect the exit status of a command like 'df -t ext3 -t reiserfs DIR' to test whether DIR is on a file system of type 'ext3' or 'reiserfs'." 라고, "du invocation" 은 앞 문장만 적습니다. 코드 1 은 이 시트의 실측입니다. <https://www.gnu.org/software/coreutils/manual/html_node/df-invocation.html>
[^du-order]: GNU coreutils 9.7 `info coreutils`, "du invocation" — "If two or more hard links point to the same file, only one of the hard links is counted. The FILE argument order affects which links are counted, and changing the argument order may change the numbers and entries that 'du' outputs." 같은 폴더 아래 파일을 두 경로로 준 경우도 먼저 센 쪽에 묶이는 것은 이 시트의 실측입니다. <https://www.gnu.org/software/coreutils/manual/html_node/du-invocation.html>
[^round]: GNU coreutils 9.7 `info coreutils`, "du invocation" — "Normally the space is printed in units of 1024 bytes, but this can be overridden (*note Block size::). Non-integer quantities are rounded up to the next higher unit." <https://www.gnu.org/software/coreutils/manual/html_node/du-invocation.html>
