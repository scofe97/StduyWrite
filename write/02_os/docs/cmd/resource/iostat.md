---
title: iostat 참조 시트
tags: [linux, cheatsheet, iostat, sysstat, io, monitoring, cli, reference]
status: draft
source:
  - sysstat 12.7.7 iostat(1) (Ubuntu 26.04 `man iostat`·`iostat --help` 원문, man7.org·manpages.debian.org 의 같은 계열 문서)
  - macOS 26.6 iostat(8) (`man iostat` 원문, 다르게 동작하는 환경)
related:
  - ../README.md
  - ../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md
  - ./top·htop.md
  - ./lsof.md
  - ./watch.md
updated: 2026-11-16
---

# iostat 참조 시트

---

> CPU 사용률과 블록 장치별 입출력 통계를 보고서로 찍어 주는 `iostat` 를 누계와 간격 보고, 확장 통계, 단위, 장치 고르기, 시각, JSON 으로 나눠 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `iostat` 는 CPU 보고와 장치 보고, 두 종류의 통계를 찍습니다.

`iostat` 는 sysstat 패키지의 외부 바이너리(`/usr/bin/iostat`)입니다. 이 시트는 sysstat 12.7.7(Ubuntu 26.04 VM)로 실측했습니다. 첫 보고는 부팅 뒤 누계이고 간격을 주면 둘째 보고부터 그 간격 동안의 값입니다.[^first] macOS 에도 `iostat` 가 있지만 BSD 계열이라 옵션(`-w`, `-c 횟수`)과 열이 다릅니다.[^macos]

장치 이름과 `%util` 은 VM 의 가상 디스크(virtio) 기준입니다. 물리 디스크나 클라우드 볼륨에서는 장치 이름(`sda`, `nvme0n1`)과 값이 다릅니다.



## 핵심 문법

> 옵션으로 보고 종류와 열과 단위를 고르고, 장치 이름으로 대상을 좁히고, 맨 뒤 간격과 횟수로 반복을 정합니다.

```bash
# 호출 형태 (iostat --help 의 Usage 줄)
iostat [ options ] [ <interval> [ <count> ] ]

# 부팅 뒤 누계를 한 번 찍는다 (부팅 뒤 누계 읽기)
iostat

# CPU 보고나 장치 보고만 찍는다 (CPU 보고와 장치 보고 고르기)
iostat -c
iostat -d

# 간격(초)과 횟수로 반복한다. -y 는 누계 보고를 뺀다 (간격 주고 지금 값 읽기)
iostat 간격 횟수
iostat -y 간격 횟수

# 확장 통계 열을 낸다 (확장 통계로 병목 읽기)
iostat -x

# 단위를 바꾼다 (단위 바꾸기)
iostat -m
iostat --human

# 장치를 고른다. -z 는 활동 없는 장치를 뺀다 (장치 고르기)
iostat 장치 [장치...]
iostat -p 장치
iostat -z
iostat -g 묶음이름 장치 [장치...]

# 표 폭과 소수 자리를 줄인다 (표 폭과 소수 자리 줄이기)
iostat -s
iostat --pretty [--compact]
iostat --dec=0

# 보고마다 시각을 붙인다 (보고마다 시각 붙이기)
iostat -t

# JSON 으로 낸다 (JSON 으로 내기)
iostat -o JSON
```

### CPU 보고 열

> CPU 보고(`avg-cpu`)의 열입니다. 값은 모든 CPU 의 평균 비율입니다.[^cols]

```bash
# %user     사용자 수준(애플리케이션)에서 실행한 비율
# %nice     nice 우선순위를 준 사용자 수준에서 실행한 비율
# %system   시스템 수준(커널)에서 실행한 비율
# %iowait   CPU 가 놀면서 처리 안 된 디스크 입출력을 기다린 비율
#           (읽는 법은 관련 문서의 08-02 노트)
# %steal    하이퍼바이저가 다른 가상 CPU 를 처리해서 가상 CPU 가 어쩔 수 없이 기다린 비율
# %idle     CPU 가 놀았고 처리 안 된 디스크 입출력도 없었던 비율
```

### 장치 보고 기본 열

> 인자 없이 부르거나 `-d` 를 주면 장치 행에 붙는 열입니다. 가운데는 「부팅 뒤 누계 읽기」 에서 받은 값이고, `/s` 가 붙은 열은 초당, 붙지 않은 열은 누계입니다.[^cols]

```bash
# 열            실측값      뜻
# tps            10.81     초당 장치에 보낸 전송 수. 전송은 장치로 가는 입출력 요청 하나이고
#                          논리 요청 여럿이 하나로 합쳐질 수 있어 크기는 정해져 있지 않다
# kB_read/s     286.51     초당 장치에서 읽은 양(kB)
# kB_wrtn/s     203.21     초당 장치에 쓴 양(kB)
# kB_dscd/s     278.90     초당 장치에서 버린(discard) 양(kB)
# kB_read    141189970     읽은 양의 합(kB)
# kB_wrtn    100141968     쓴 양의 합(kB)
# kB_dscd    137440928     버린 양의 합(kB)
```

### 확장 통계 열

> `-x` 를 주면 장치 행에 붙는 열입니다. 가운데는 「확장 통계로 병목 읽기」 의 쓰기 부하 행에서 받은 값입니다.[^cols]

```bash
# 열         실측값      뜻
# r/s          0.00     초당 완료한 읽기 요청 수(병합 뒤)
# rkB/s        0.00     초당 읽은 양(kB)
# rrqm/s       0.00     초당 병합된 읽기 요청 수
# %rrqm        0.00     장치로 보내기 전에 병합된 읽기 요청의 비율
# r_await      0.00     읽기 요청이 처리되기까지 평균 시간(ms). 큐 대기 포함
# rareq-sz     0.00     읽기 요청 하나의 평균 크기(kB)
# w/s       8917.00     초당 완료한 쓰기 요청 수(병합 뒤)
# wkB/s   570688.00     초당 쓴 양(kB)
# wrqm/s       0.00     초당 병합된 쓰기 요청 수
# %wrqm        0.00     장치로 보내기 전에 병합된 쓰기 요청의 비율
# w_await      0.09     쓰기 요청이 처리되기까지 평균 시간(ms). 큐 대기 포함
# wareq-sz    64.00     쓰기 요청 하나의 평균 크기(kB)
# d/s          0.00     초당 완료한 discard 요청 수(병합 뒤)
# dkB/s        0.00     초당 discard 한 양(kB)
# drqm/s       0.00     초당 병합된 discard 요청 수
# %drqm        0.00     장치로 보내기 전에 병합된 discard 요청의 비율
# d_await      0.00     discard 요청이 처리되기까지 평균 시간(ms)
# dareq-sz     0.00     discard 요청 하나의 평균 크기(kB)
# f/s          0.00     초당 완료한 flush 요청 수
# f_await      0.00     flush 요청이 처리되기까지 평균 시간(ms)
# aqu-sz       0.84     장치로 보낸 요청의 평균 큐 길이
# %util       89.70     경과 시간 중 장치에 요청이 있었던 비율(%)
```



## 종료 코드

> 보고를 내면 0 이고, 모르는 옵션이나 값을 주면 메시지를 찍고 1 로 끝납니다.[^no-exit]

```bash
# 0  보고를 냈다
# 1  모르는 옵션이나 값을 줬다. 사용법이나 오류 메시지를 찍고 끝난다
#    횟수 자리에 0 을 줘도 같다 (「횟수 자리의 잘못된 값」)

# 버전 첫 줄이 나오고 0 으로 끝난다
#   -V          버전을 찍고 끝낸다
#   sed -n 1p   첫 줄만 낸다
iostat -V | sed -n 1p; echo ${PIPESTATUS[0]}    # sysstat version 12.7.7 / 0

# 모르는 옵션. 첫 줄이 사용법이고 1 로 끝난다
iostat -Z 2>&1 | sed -n 1p; echo ${PIPESTATUS[0]}    # Usage: iostat [ options ] [ <interval> [ <count> ] ] / 1

# 영구 장치 이름 종류를 모르면 사용법 대신 이 메시지를 찍고 1 로 끝난다
#   -j   영구 장치 이름의 종류(ID, LABEL 등)를 고른다
iostat -j NOSUCH 2>&1 | sed -n 1p; echo ${PIPESTATUS[0]}    # Invalid type of persistent device name / 1
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션만 씁니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 부하 함수와 장치 이름이 준비됩니다.

실행 환경은 OrbStack 의 Ubuntu VM 의 root 셸입니다. `load` 는 「간격 주고 지금 값 읽기」 부터 여러 곳에서 씁니다.

```bash
# sysstat 이 없으면 넣는다
apt-get install -y -qq sysstat >/dev/null 2>&1
iostat -V | sed -n 1p    # sysstat version 12.7.7

# DEV: /var/tmp 가 놓인 디스크의 이름이다. 이 시트의 값은 vdb 다
# 직접 칠 때는 자기 환경의 이름이 나온다
DEV=$(lsblk -no PKNAME "$(findmnt -no SOURCE -T /var/tmp | sed 's/\[.*//')")
echo $DEV    # vdb

# 부하 파일을 쓸 디렉터리다
mkdir -p /var/tmp/lab-iostat && cd /var/tmp/lab-iostat

# load <초>: 쓰기 부하를 그 초 동안 백그라운드로 건다. 끝나면 파일을 지운다
#   dd if=/dev/zero   0 바이트를 끝없이 읽는다
#   dd of=...         부하 파일에 쓴다
#   dd bs=64k         요청 하나의 크기를 64 KiB 로 맞춘다
#   dd oflag=direct   페이지 캐시를 거치지 않고 장치에 바로 쓴다
#   timeout 초        dd 를 그 초 뒤에 끊는다
load() {
  ( timeout "${1:-4}" dd \
      if=/dev/zero \
      of=/var/tmp/lab-iostat/w.bin \
      bs=64k \
      oflag=direct 2>/dev/null
    rm -f /var/tmp/lab-iostat/w.bin ) &
  sleep 0.3
}
```

부하는 그 장치에 다른 프로세스가 쓰는 입출력과 섞이므로 값은 이 시트와 같지 않아도 됩니다. 열 이름과 보고 개수가 같으면 맞게 돈 것입니다.

### 부팅 뒤 누계 읽기

> 인자 없이 부르면 CPU 보고와 장치 보고를 한 번씩 찍고 값은 부팅 뒤 누계입니다.

```bash
# CPU 보고와 장치 보고가 한 번씩 나온다. 장치 이름을 인자로 주면 그 장치 행만 남는다
iostat $DEV
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           0.09    0.00    0.12    0.01    0.00   99.78

Device             tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd
vdb              10.81       286.51       203.21       278.90  141189970  100141968  137440928
```

열 뜻은 「CPU 보고 열」·「장치 보고 기본 열」 에 있습니다. 아래 블록은 누계를 부팅 뒤 경과 초(`/proc/uptime` 첫 칸)로 나누면 `kB_read/s` 가 되는지 맞춰 봅니다.

```bash
# kB_read/s 와 kB_read ÷ 경과 초를 나란히 찍는다. 둘이 같다
#   awk -v   셸 값을 awk 변수로 넘긴다
iostat -d $DEV \
  | awk \
      -v up="$(cut -d' ' -f1 /proc/uptime)" \
      -v dev="$DEV" \
      '$1 == dev {print $3, $6 / up}'
```

```bash
286.51 286.51
```

### CPU 보고와 장치 보고 고르기

> `-c` 는 CPU 보고만, `-d` 는 장치 보고만 남깁니다.

```bash
# CPU 보고만 나온다. 장치 보고와 그 앞 헤더는 없다
#   -c   CPU 보고만 낸다
iostat -c
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           0.09    0.00    0.12    0.01    0.00   99.78
```

```bash
# 장치 보고만 나온다. CPU 보고는 없다
#   -d   장치 보고만 낸다
iostat -d $DEV
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

Device             tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd
vdb              10.81       286.51       203.21       278.90  141192526  100141968  137440928
```

### 간격 주고 지금 값 읽기

> 간격과 횟수를 주면 첫 보고 뒤로 그 간격 동안의 값이 이어지고, `-y` 는 첫 누계 보고를 뺍니다.

```bash
# 1초 간격으로 2번 찍는다. 첫 보고는 누계(tps 10.82)이고 둘째가 1초 동안의 값(tps 10901)이다
# load 4 는 4초 동안 쓰기 부하를 걸고, wait 는 부하가 끝나기를 기다린다
#   <간격> <횟수>   명령 맨 뒤에 둔다. 횟수를 빼면 끝나지 않고 계속 찍는다
load 4
iostat -d $DEV 1 2
wait
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

Device             tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd
vdb              10.82       286.52       203.87       278.90  141192910  100463632  137440928


Device             tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd
vdb           10901.00      1492.00    692352.00         0.00       1492     692352          0
```

```bash
# 누계 보고 없이 간격 보고 2개만 나온다. 첫 줄 헤더 뒤에 곧바로 지금 값이다
#   -y   첫 누계 보고를 뺀다
load 4
iostat -d -y $DEV 1 2
wait
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

Device             tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd
vdb            5314.00         0.00    340096.00         0.00          0     340096          0


Device             tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd
vdb            5180.00        32.00    331392.00         0.00         32     331392          0
```

```bash
# -c 와 -d 를 함께 주면 CPU 보고와 장치 보고가 모두 나온다
# 쓰기 부하 동안 %system 이 14.32 로 오른다
load 4
iostat -c -d -y $DEV 1 1
wait
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           0.13    0.00   14.32    0.00    0.00   85.55

Device             tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd
vdb            9605.00         0.00    614720.00         0.00          0     614720          0
```

### 확장 통계로 병목 읽기

> `-x` 는 장치 행에 요청 수·평균 대기 시간·큐 길이·`%util` 열을 더합니다.

```bash
# 쓰기 부하 동안 w/s 8917, w_await 0.09ms, aqu-sz 0.84, %util 89.70 이 나온다
# 읽기 열(r/s, rkB/s 등)은 0.00 이다
#   -x   확장 통계 열을 더한다
load 4
iostat -x -d -y $DEV 1 1
wait
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

Device            r/s     rkB/s   rrqm/s  %rrqm r_await rareq-sz     w/s     wkB/s   wrqm/s  %wrqm w_await wareq-sz     d/s     dkB/s   drqm/s  %drqm d_await dareq-sz     f/s f_await  aqu-sz  %util
vdb              0.00      0.00     0.00   0.00    0.00     0.00 8917.00 570688.00     0.00   0.00    0.09    64.00    0.00      0.00     0.00   0.00    0.00     0.00    0.00    0.00    0.84  89.70
```

열이 많아 한 줄이 200자쯤 됩니다. 폭을 줄이는 방법은 「표 폭과 소수 자리 줄이기」 에 있습니다.

### 단위 바꾸기

> 기본 열은 `kB` 이고 `-m` 은 `MB` 로, `--human` 은 값마다 알맞은 단위로 바꿉니다.

```bash
# 열 이름과 단위가 기본과 같은 kB 다. -k 는 kB 로 찍는 옵션이다
#   -k   kB 단위로 찍는다
load 4
iostat -k -d -y $DEV 1 1
wait
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

Device             tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd
vdb           12664.00      2832.00    799168.00         0.00       2832     799168          0
```

```bash
# 열 이름이 MB_read/s·MB_wrtn/s 로 바뀌고 값이 MB 단위가 된다
#   -m   MB 단위로 찍는다
load 4
iostat -m -d -y $DEV 1 1
wait
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

Device             tps    MB_read/s    MB_wrtn/s    MB_dscd/s    MB_read    MB_wrtn    MB_dscd
vdb            4879.21         0.00       304.95         0.00          0        308          0
```

```bash
# 값 뒤에 k·M 이 붙는다. 열 이름은 그대로 kB_* 이므로 값의 글자가 단위다
#   --human   값마다 읽기 쉬운 단위(k, M, G)를 붙인다
load 4
iostat --human -d -y $DEV 1 1
wait
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

Device             tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd
vdb            7400.00         0.0k       462.5M         0.0k       0.0k     467.1M       0.0k
```

```bash
# --human 과 --pretty 를 한 번에 준 것과 같다. 장치 이름이 오른쪽 끝으로 간다
#   -h   --human --pretty 와 같다. --pretty 는 「표 폭과 소수 자리 줄이기」 에서 푼다
load 4
iostat -h -d -y $DEV 1 1
wait
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
  6340.00      1012.0k       395.6M         0.0k    1012.0k     395.6M       0.0k vdb
```

### 장치 고르기

> 장치 이름을 나열하거나, `-p` 로 파티션을 더하거나, `-z` 로 활동 없는 장치를 빼거나, `-g` 로 합계를 냅니다.

```bash
# 장치 이름 둘을 나열하면 그 두 장치 행만 나온다
iostat -d vda $DEV
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

Device             tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd
vda               1.36       158.07         0.00         0.00   77898916          0          0
vdb              11.27       286.52       232.36       305.18  141202402  114511996  150400080
```

```bash
# 장치 행 아래에 그 장치의 파티션 vdb1 행이 붙는다
#   -p   장치와 그 파티션을 모두 보인다
load 4
iostat -p $DEV -d -y 1 1
wait
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

Device             tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd
vdb           12824.00        16.00    820672.00         0.00         16     820672          0
vdb1          12816.00        16.00    820160.00         0.00         16     820160          0
```

```bash
# 장치를 안 골라도 1초 동안 활동한 vdb 한 줄만 남는다
#   -z   그 구간에 활동이 없었던 장치 행을 뺀다
load 4
iostat -z -d -y 1 1
wait
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

Device             tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd
vdb            2716.00         0.00    173824.00         0.00          0     173824          0
```

```bash
# 두 장치 행 아래에 묶음 이름 disks 의 합계 행이 붙는다
#   -g   장치 묶음의 합계 행을 더한다. 첫 인자가 묶음 이름이다
iostat -g disks -d vda $DEV
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

Device             tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd
vda               1.36       158.06         0.00         0.00   77898916          0          0
vdb              11.40       286.51       240.33       305.18  141202950  118440268  150400080
 disks           12.75       444.58       240.33       305.18  219101866  118440268  150400080
```

```bash
# 장치 행은 빠지고 합계 행 disks 만 남는다
#   -H   -g 와 함께 써서 합계 행만 보인다
iostat -g disks -H -d vda $DEV
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

Device             tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd
 disks           12.75       444.58       240.33       305.18  219101866  118440268  150400080
```

### 표 폭과 소수 자리 줄이기

> `-s` 는 열을 줄이고, `--pretty` 는 열을 여러 보고로 쪼개고, `--dec` 는 소수 자리를 줄입니다.

```bash
# 확장 통계가 7열로 줄어 80자 안에 들어온다. r_await·w_await 같은 읽기·쓰기 열은 합쳐진다
#   -s   80자 폭에 맞춘 짧은 보고를 낸다
load 4
iostat -x -s -d -y $DEV 1 1
wait
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

Device             tps      kB/s    rqm/s   await  areq-sz  aqu-sz  %util
vdb            6888.12 440839.60     0.00    0.15    64.00    1.04  90.40
```

```bash
# 열이 읽기·쓰기·discard·flush 네 보고로 나뉘고 장치 이름이 오른쪽 끝에 붙는다
#   --pretty   열이 많으면 보고를 쪼개고 장치 이름을 오른쪽에 둔다
load 4
iostat -x --pretty -d -y $DEV 1 1
wait
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

     r/s     rkB/s   rrqm/s  %rrqm r_await rareq-sz Device
   32.00   1392.00     0.00   0.00    0.47    43.50 vdb

     w/s     wkB/s   wrqm/s  %wrqm w_await wareq-sz Device
 7132.00 456448.00     0.00   0.00    0.13    64.00 vdb

     d/s     dkB/s   drqm/s  %drqm d_await dareq-sz Device
    0.00      0.00     0.00   0.00    0.00     0.00 vdb

     f/s f_await  aqu-sz  %util Device
    0.00    0.00    0.92  92.10 vdb
```

```bash
# 쪼개지 않고 한 줄에 모두 낸다. 장치 이름은 오른쪽 끝에 붙은 채다
#   --compact   --pretty 가 나누는 보고를 나누지 않는다
load 4
iostat -x --pretty --compact -d -y $DEV 1 1
wait
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

     r/s     rkB/s   rrqm/s  %rrqm r_await rareq-sz     w/s     wkB/s   wrqm/s  %wrqm w_await wareq-sz     d/s     dkB/s   drqm/s  %drqm d_await dareq-sz     f/s f_await  aqu-sz  %util Device
   40.59   4340.59     4.95  10.87    1.02   106.93 16758.42 1072538.61     0.00   0.00    0.04    64.00    0.00      0.00     0.00   0.00    0.00     0.00    0.00    0.00    0.72  68.12 vdb
```

```bash
# 소수 둘째 자리가 사라지고 정수만 남는다
#   --dec=0   소수 자리를 0자리로 한다(0~2, 기본 2)
load 4
iostat --dec=0 -d -y $DEV 1 1
wait
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

Device             tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd
vdb               7728            0       494592            0          0     494592          0
```

### 보고마다 시각 붙이기

> `-t` 는 보고마다 현재 시각 줄을 붙이고 `S_TIME_FORMAT=ISO` 는 그 형식을 ISO 8601 로 바꿉니다.[^isofmt]

```bash
# 장치 헤더 위에 시각 줄이 붙는다. 형식은 로캘을 따른다(월/일/연도 시:분:초 AM)
#   -t   보고마다 시각을 찍는다
load 4
iostat -t -d -y $DEV 1 1
wait
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

11/16/2026 09:46:38 AM
Device             tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd
vdb            2864.71         0.00    183341.18         0.00          0     187008          0
```

```bash
# 첫 줄의 날짜와 시각 줄이 모두 ISO 8601(연-월-일, T 로 이은 시각)로 바뀐다
load 4
S_TIME_FORMAT=ISO iostat -t -d -y $DEV 1 1
wait
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	2026-11-16 	_aarch64_	(8 CPU)

2026-11-16T09:46:42+0900
Device             tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd
vdb            1750.00         0.00    112000.00         0.00          0     112000          0
```

### JSON 으로 내기

> `-o JSON` 은 보고를 JSON 으로 내고, 필드 순서는 정해져 있지 않습니다.[^json]

```bash
# 보고가 JSON 객체 하나로 나온다. 장치 행은 disk 배열 안에 열 이름을 키로 들어간다
#   -o JSON   JSON 형식으로 낸다
load 4
iostat -o JSON -d -y $DEV 1 1
wait
```

```bash
{"sysstat": {
	"hosts": [
		{
			"nodename": "ubuntu",
			"sysname": "Linux",
			"release": "7.2.12-orbstack-00394-gbecdd6130068",
			"machine": "aarch64",
			"number-of-cpus": 8,
			"date": "11/16/2026",
			"statistics": [

				{
					"disk": [
						{"disk_device": "vdb", "tps": 1215.84, "kB_read/s": 4055.45, "kB_wrtn/s": 77750.50, "kB_dscd/s": 0.00, "kB_read": 4096, "kB_wrtn": 78528, "kB_dscd": 0}
					]
				}
			]
		}
	]
}}
```

### 간격 보고에서 값 뽑아 쓰기

> 간격 보고를 다른 명령에 넘기면 값 한 칸을 평균이나 비교에 쓸 수 있습니다.

```bash
# 1초 간격 보고 3개에서 kB_wrtn/s(넷째 칸)의 평균을 낸다. 결과는 197097 이다
#   $1 == dev   장치 이름이 맞는 행만 고른다
load 5
iostat -d -y $DEV 1 3 \
  | awk -v dev="$DEV" '$1 == dev {s += $4; n++} END {print s / n}'
wait
```

```bash
# JSON 에서 kB_wrtn/s 값 하나만 뽑는다. 결과는 356656.00 이다
#   jq   JSON 에서 지정한 필드를 꺼낸다
load 4
iostat -o JSON -d -y $DEV 1 1 \
  | jq '.sysstat.hosts[0].statistics[0].disk[0]."kB_wrtn/s"'
wait
```

### 실습 정리

```bash
# 「주의사항과 동작 원리」 의 예도 같은 준비를 쓰니 그 예까지 돌린 뒤에 지운다
# 부하 파일은 load 가 이미 지웠고 디렉터리와 함수와 변수가 남는다
cd / && rm -rf /var/tmp/lab-iostat
unset -f load
unset DEV
```



## 주의사항과 동작 원리

### 없는 장치 이름

> 없는 장치 이름을 줘도 오류 없이 헤더만 찍고 0 으로 끝납니다.

```bash
# 장치 행이 하나도 없는 보고가 나온다. 오타를 내도 알려 주지 않는다
iostat -d nosuch
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

Device             tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd
```

```bash
# 종료 코드도 0 이다
iostat -d nosuch >/dev/null; echo $?    # 0
```

이름이 맞는지는 `lsblk` 로 먼저 확인합니다.

### 횟수 자리의 잘못된 값

> 횟수 자리에 숫자가 아닌 글자를 주면 끝나지 않고, 0 을 주면 사용법을 찍고 1 로 끝납니다.

```bash
# abc 는 횟수로 읽히지 않아 계속 찍는다. timeout 3.5 가 끊을 때까지 Device 헤더가 4번 나왔다
#   grep -c   맞는 줄 수를 센다
timeout 3.5 iostat -d $DEV 1 abc | grep -c '^Device'    # 4
echo ${PIPESTATUS[0]}    # 124

# 0 은 사용법을 찍고 1 로 끝난다
iostat -d $DEV 1 0 2>&1 | sed -n 1p; echo ${PIPESTATUS[0]}    # Usage: iostat [ options ] [ <interval> [ <count> ] ] / 1
```

블록의 `/` 는 여러 줄 출력을 한 줄에 줄여 적은 것입니다. 스크립트에서 횟수를 변수로 넘길 때는 변수가 비거나 숫자가 아닌 경우를 막아야 합니다. 124 는 `iostat` 가 아니라 `timeout` 이 시간 초과로 끊은 값입니다.

### -z 와 누계 보고

> `-z` 는 그 보고 구간에 활동이 없던 장치를 빼므로 부팅 뒤 누계에서는 아무것도 빼지 못합니다.

```bash
# 첫 보고(누계)에는 세 장치 행이 모두 나오고 둘째 보고(1초)에는 행이 없다
iostat -z -d vda vdc zram0 1 2
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

Device             tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd
vda               1.37       158.65         0.00         0.00   78311504          0          0
vdc               0.00         0.04         0.00         2.12      21448          4    1048572
zram0             5.19        23.27        30.75         0.00   11485972   15177796          0


Device             tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd
```

부팅 뒤에 한 번이라도 입출력이 있었던 장치는 누계가 0 이 아니므로 첫 보고에 남습니다. 지금 활동 중인 장치만 보려면 `-y` 로 누계 보고를 빼고 간격 보고에 `-z` 를 줍니다.[^z]

### %util 과 포화

> `%util` 은 장치에 요청이 있었던 시간의 비율이라 처리량과 비례하지 않고, 병렬 장치에서는 한계를 가리키지 않습니다.[^util]

```bash
# 두 보고 사이에 %util 은 87.50 에서 91.90 으로 올랐는데 kB/s 는 422944 에서 338464 로 내렸다
load 4
iostat -x -s -d -y $DEV 1 2
wait
```

```bash
Linux 7.2.12-orbstack-00394-gbecdd6130068 (ubuntu) 	11/16/2026 	_aarch64_	(8 CPU)

Device             tps      kB/s    rqm/s   await  areq-sz  aqu-sz  %util
vdb            6610.00 422944.00     0.00    0.14    63.99    0.90  87.50


Device             tps      kB/s    rqm/s   await  areq-sz  aqu-sz  %util
vdb            5321.00 338464.00   290.00    0.21    63.61    1.10  91.90
```

매뉴얼은 요청을 직렬로 처리하는 장치에서는 `%util` 이 100% 에 가까우면 포화라고 적습니다. RAID 배열과 최신 SSD 처럼 요청을 병렬로 처리하는 장치에서는 이 수가 성능 한계를 반영하지 않는다고도 적습니다.

### kB 의 실제 단위

> 열 이름은 `kB` 인데 실제 단위는 1024 바이트(KiB)입니다.[^kib]

```bash
# 루프 장치에 정확히 32 MiB(33,554,432 바이트)를 쓰고 kB_wrtn 의 증가분을 본다
# 증가분이 32768 이다. 33,554,432 를 1024 로 나눈 값이고 1000 으로 나눈 33554 가 아니다
#   truncate -s   파일 크기를 정한다
#   losetup -f --show   빈 루프 장치에 파일을 잇고 장치 이름을 찍는다
truncate -s 64M lab-loop.img
LD=$(losetup -f --show lab-loop.img)
LN=${LD#/dev/}
before=$(iostat -d $LN | awk -v dev="$LN" '$1 == dev {print $7}')
dd if=/dev/zero of=$LD bs=1M count=32 oflag=direct 2>/dev/null
sleep 1    # 바로 읽으면 일부만 반영된 값이 나온 적이 있어 1초 기다린다
after=$(iostat -d $LN | awk -v dev="$LN" '$1 == dev {print $7}')
echo "$LD $before $after $((after - before))"    # /dev/loop0 568678 601446 32768

# 루프 장치와 파일을 되돌린다
losetup -d $LD; rm -f lab-loop.img
```

### 같은 패키지의 다른 명령

> sysstat 패키지는 `sar`·`pidstat`·`mpstat` 도 넣지만 이 시트는 `iostat` 만 다룹니다.



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [top·htop 참조 시트](./top·htop.md) — 프로세스별 CPU 사용과 한 화면 요약
- [awk 참조 시트](../text/awk.md) — 보고의 열 번호로 칸을 뽑아 평균을 내는 awk 문법
- [lsof 참조 시트](./lsof.md) — 프로세스가 연 파일과 장치
- [watch 참조 시트](./watch.md) — 다른 명령을 간격마다 다시 실행해 한 화면에 덮어 그리는 법
- [자원마다 창이 따로 나 있어 어느 창을 여느냐가 곧 진단이다](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md#iostat-의-장치별-행) — `tps`·`kB_*`·`%iowait` 를 읽는 법과 누계 보고를 읽는 원리



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- 검증 환경: Ubuntu 26.04.1 LTS VM(OrbStack, aarch64, CPU 8개, 커널 7.2.12-orbstack), sysstat 12.7.7-0ubuntu2, 가상 디스크 vda·vdb·vdc
- sysstat 12.7.7 의 `iostat --help`·`man iostat` 원문 — 2026-11-16 확인
- [iostat(1) — man7.org](https://man7.org/linux/man-pages/man1/iostat.1.html)
- [iostat(1) — Debian trixie](https://manpages.debian.org/trixie/sysstat/iostat.1.en.html)
- [iostat(8) — FreeBSD](https://man.freebsd.org/cgi/man.cgi?query=iostat&sektion=8)

[^first]: `man iostat` (sysstat 12.7.7) DESCRIPTION — "The first report generated by the iostat command provides statistics concerning the time since the system was booted, unless the -y option is used (in this case, this first report is omitted). Each subsequent report covers the time since the previous report." <https://man7.org/linux/man-pages/man1/iostat.1.html>
[^macos]: macOS 26.6 `man iostat` — "iostat [-CUdKIoT?] [-c count] [-n devs] [-w wait] [drives]", "The first statistics that are printed are averaged over the system uptime." 둘째 문장은 FreeBSD 문서에도 같은 글로 있고 옵션 줄은 판마다 다릅니다. <https://man.freebsd.org/cgi/man.cgi?query=iostat&sektion=8>
[^cols]: `man iostat` REPORTS — %user "the percentage of CPU utilization that occurred while executing at the user level (application)", %steal "the percentage of time spent in involuntary wait by the virtual CPU or CPUs while the hypervisor was servicing another virtual processor", aqu-sz "The average queue length of the requests that were issued to the device." 나머지 열의 뜻도 같은 절의 문장을 옮겼습니다. <https://man7.org/linux/man-pages/man1/iostat.1.html>
[^no-exit]: iostat(1) 의 man 에는 종료 코드 절이 없습니다. 아래 값은 VM 에서 해당 호출을 돌려 `echo $?` 로 읽은 것입니다.
[^isofmt]: `man iostat` ENVIRONMENT — "S_TIME_FORMAT If this variable exists and its value is ISO then the current locale will be ignored when printing the date in the report header. The iostat command will use the ISO 8601 format (YYYY-MM-DD) instead. The timestamp displayed with option -t will also be compliant with ISO 8601 format." <https://man7.org/linux/man-pages/man1/iostat.1.html>
[^json]: `man iostat` OPTIONS — "-o JSON Display the statistics in JSON (JavaScript Object Notation) format. JSON output field order is undefined, and new fields may be added in the future." <https://man7.org/linux/man-pages/man1/iostat.1.html>
[^z]: `man iostat` OPTIONS — "-z Tell iostat to omit output for any devices for which there was no activity during the sample period." <https://man7.org/linux/man-pages/man1/iostat.1.html>
[^util]: `man iostat` REPORTS — "%util Percentage of elapsed time during which I/O requests were issued to the device (bandwidth utilization for the device). Device saturation occurs when this value is close to 100% for devices serving requests serially. But for devices serving requests in parallel, such as RAID arrays and modern SSDs, this number does not reflect their performance limits." <https://man7.org/linux/man-pages/man1/iostat.1.html>
[^kib]: `man iostat` BUGS — "Although iostat displays units corresponding to kilobytes (kB), megabytes (MB)..., it actually uses kibibytes ... A kibibyte is equal to 1024 bytes". <https://man7.org/linux/man-pages/man1/iostat.1.html>
