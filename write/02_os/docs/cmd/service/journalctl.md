---
title: journalctl 참조 시트
tags: [linux, cheatsheet, journalctl, systemd, journal, log, cli, reference]
status: draft
source:
  - systemd 259 journalctl(1)·journald.conf(5) (OrbStack Ubuntu 26.04 VM 의 `man journalctl`·`journalctl --help` 원문, freedesktop.org journalctl(1))
  - syslog(3)·timeout(1) (man7.org)
related:
  - ./journalctl%20저장%20공간과%20읽기%20권한.md
  - ./journalctl%20출력%20모양과%20jq.md
  - ../README.md
  - ./systemctl.md
  - ./systemctl%20유닛%20설정과%20타이머.md
  - ./systemctl%20함정과%20동작%20원리.md
  - ../../../book/learning-modern-linux/08-01.재는%20것은%20바깥이고%20알고%20싶은%20것은%20안이다.md
  - ../../../book/learning-modern-linux/06-01.먼저%20켜지는%20것%20하나가%20나머지%20전부를%20켠다.md
updated: 2026-11-14
---

# journalctl 참조 시트

---

> 유닛·시각·부팅·심각도·필드로 로그를 좁혀 읽고 저널의 크기와 저장 위치를 확인하는 `journalctl` 을 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `journalctl` 은 journald 가 모아 둔 로그를 조건으로 좁혀 읽는 명령입니다.

systemd 패키지의 외부 바이너리(`/usr/bin/journalctl`)이며 macOS 에는 없습니다.[^env] 이 시트의 출력은 OrbStack Ubuntu 26.04 VM(systemd 259.9)에서 root 셸로 받았고 시각은 KST, 호스트 이름은 `ubuntu` 입니다.

저널의 크기·저장 위치·정리와 읽기 권한은 [journalctl 저장 공간과 읽기 권한](./journalctl%20저장%20공간과%20읽기%20권한.md)으로 나눴습니다. 출력 모양을 바꾸고 `jq` 로 잇는 예는 [journalctl 출력 모양과 jq](./journalctl%20출력%20모양과%20jq.md)로 나눴습니다.



## 핵심 문법

> 대상은 `-u`·`-t`·`필드=값` 으로 고르고, 시각·부팅·심각도·`-g` 로 좁히고, `-o` 로 출력 모양을 정합니다.

```bash
# 호출 형태
# journalctl --help 의 첫 줄
journalctl [OPTIONS...] [MATCHES...]

# 유닛 하나의 로그를 본다 (유닛 하나의 로그 보기)
journalctl -u 유닛

# 끝 몇 줄만 보고 거꾸로 읽는다 (끝 몇 줄과 거꾸로 읽기)
journalctl -n 줄수 -r

# 새로 쌓이는 줄을 따라 읽는다 (새로 쌓이는 로그 따라 읽기)
journalctl -f -u 유닛

# 시각 범위로 좁힌다 (시각으로 좁히기)
journalctl --since 시각 --until 시각

# 부팅 하나로 좁힌다 (부팅으로 좁히기)
journalctl -b [부팅]

# 심각도로 좁힌다 (심각도로 좁히기)
journalctl -p 우선순위

# 커널 메시지만 본다 (커널 메시지 보기)
journalctl -k

# 필드로 좁힌다 (필드로 좁히기)
journalctl 필드=값

# 필드 값 목록과 필드 이름 목록을 뽑는다 (필드 값과 이름 찾기)
journalctl -F 필드
journalctl -N

# 메시지에서 문자열을 찾는다 (문자열로 찾기)
journalctl -g 정규식

# 출력 모양을 바꾼다 (journalctl 출력 모양과 jq 시트)
journalctl -o 출력모드

# 실패한 서비스의 원인을 본다 (실패한 서비스 원인 찾기)
journalctl -xeu 유닛
```

인자 없이 부르면 호출한 사용자가 볼 수 있는 저널을 가장 오래된 줄부터 모두 냅니다.[^syn]

### 우선순위 이름

> `-p` 는 이름이나 숫자로 심각도를 받고, 숫자가 작을수록 더 심각합니다.

이름과 숫자는 journalctl(1) `-p` 의 원문 순서이고 뜻은 syslog(3) 를 옮긴 것입니다.[^prio]

```bash
# -p 에 쓰는 이름과 숫자. 하나만 주면 그 값과 더 심각한 값을 모두 낸다
# 0  emerg     시스템을 쓸 수 없다
# 1  alert     바로 조치해야 한다
# 2  crit      치명적인 상태다
# 3  err       오류다
# 4  warning   경고다
# 5  notice    정상이지만 눈여겨볼 일이다
# 6  info      알림이다
# 7  debug     디버그 메시지다
```

### 출력 모드

> `-o` 는 한 줄 요약부터 JSON 까지 출력 모양을 고르고, 이 시트와 출력 모양 시트는 아래 일곱 가지를 씁니다.

매뉴얼의 `-o` 목록에서 본문에서 쓰는 항목만 옮겼습니다.[^outmode]

```bash
# -o 에 쓰는 이름 (여러 유닛 한꺼번에 보기, journalctl 출력 모양과 jq 시트)
# short           기본값. 날짜 시각 호스트 식별자[PID]: 메시지 한 줄
# short-iso       시각을 ISO 8601 꼴로 낸다
# short-precise   시각에 마이크로초를 붙인다
# cat             메시지만 낸다
# verbose         항목의 모든 필드를 한 줄씩 낸다
# json            항목 하나를 JSON 한 줄로 낸다
# json-pretty     JSON 을 여러 줄로 들여 써서 낸다
```



## 종료 코드

> 성공이면 0, 실패면 0 이 아닌 값이며 매뉴얼은 그 이상을 적지 않습니다.[^exit]

아래 값은 모두 실측이고 「실습 준비」 에서 만든 유닛으로 돌립니다. 줄이 하나도 없는 것은 오류가 아닙니다.

```bash
# 0  성공
#    -u 로 고른 유닛에 줄이 없어도 0 이다
# 1  실패
#    없는 옵션, -g 가 아무 줄도 못 찾은 경우,
#    기록에 없는 부팅을 고른 경우

# 옵션 뜻
#   -u           이 유닛의 로그만 본다 (--unit)
#   -g           메시지가 이 정규식에 맞는 줄만 본다 (--grep)
#   --no-pager   less 로 넘기지 않고 곧바로 낸다
journalctl --no-such-option; echo $?
# journalctl: unrecognized option '--no-such-option' / 1

journalctl -u lab-nothing --no-pager; echo $?
# -- No entries -- / 0

journalctl \
  -u lab-report \
  -g zzzz \
  --no-pager; echo $?
# -- No entries -- / 1
```

`/` 앞은 출력이고 뒤는 `echo $?` 가 읽은 종료 코드입니다. 기록에 없는 부팅의 1 은 「부팅으로 좁히기」 에서 봅니다.



## 유스케이스

> 예는 앞 예가 만든 상태를 이어 쓰므로 위에서 아래로 차례로 돌립니다.

### 실습 준비

> 아래 블록을 root 셸에 한 번 붙여 넣으면 이 시트의 예가 읽는 로그가 생깁니다.

PID·시각·저널 크기는 실행마다 다르므로 이 시트의 값과 같지 않아도 됩니다. 저널은 쌓이기만 하므로 블록을 두 번 돌리면 같은 줄이 두 벌 보입니다.

```bash
# 실습이 끝나면 「실습 정리」 블록으로 유닛 상태를 지운다
# 저널에 이미 남은 줄은 지우지 않는다

# 이 셸의 journalctl 이 less 로 넘기지 않게 한다
#   SYSTEMD_PAGER 가 빈 문자열이면 --no-pager 와 같다
export SYSTEMD_PAGER=

# lab-report: 로그 넷을 남기고 끝나는 서비스. 「유닛 하나의 로그 보기」 부터 여러 곳에서 쓴다
#   <4>·<3> 접두사는 그 줄의 심각도다. 4 는 warning, 3 은 err 이고 없으면 info 다
#   systemd-run 은 임시 서비스 유닛을 만들어 명령을 돌린다
#   systemd-run --unit=          유닛 이름
#   systemd-run --description=   status 와 로그에 보일 설명
#   systemd-run --quiet          "Running as unit" 안내를 끈다
#   systemd-run --wait           서비스가 끝날 때까지 기다린다
#   systemd-run --collect        끝나면 실패해도 유닛을 메모리에서 지운다
#   systemd-run -p               유닛 속성. Type=oneshot 은 한 번 돌고 끝나는
#                                서비스, SyslogIdentifier= 는 줄 앞의 이름이다
systemd-run \
  --unit=lab-report \
  --description="lab report job" \
  --quiet \
  --wait \
  --collect \
  -p Type=oneshot \
  -p SyslogIdentifier=lab-report \
  /bin/sh -c '
    echo "lab-report: starting"
    echo "<4>lab-report: disk almost full"
    echo "<3>lab-report: write failed"
    echo "lab-report: done"'

# lab-backup: 정상 로그만 남기고 끝나는 서비스. 같은 꼴이다
systemd-run \
  --unit=lab-backup \
  --description="lab backup job" \
  --quiet \
  --wait \
  --collect \
  -p Type=oneshot \
  -p SyslogIdentifier=lab-backup \
  /bin/sh -c '
    echo "lab-backup: copying 3 files"
    echo "lab-backup: done"'

# lab-crash: 종료 코드 3 으로 끝나는 서비스 (실패한 서비스 원인 찾기)
#   --collect 를 뺐으므로 failed 상태로 남는다
systemd-run \
  --unit=lab-crash \
  --description="lab crash job" \
  --quiet \
  --wait \
  -p Type=oneshot \
  -p SyslogIdentifier=lab-crash \
  /bin/sh -c '
    echo "lab-crash: starting"
    echo "lab-crash: giving up" >&2
    exit 3'

# lab-web: 데몬이 syslog 로 보낸 줄처럼 남긴다 (필드로 좁히기, 출력 모양과 jq 시트)
#   logger -t   줄마다 붙일 태그
#   logger -p   시설.심각도
logger -t lab-web -p user.warning "lab-web: cache miss rate high"
logger -t lab-web -p user.info "lab-web: request served"

# lab-batch: 표준 입력을 저널로 보낸다 (필드로 좁히기)
#   systemd-cat -t   syslog 식별자
#   systemd-cat -p   심각도 (0..7 이나 이름)
echo "lab-batch: from systemd-cat" | systemd-cat -t lab-batch -p err

```

### 유닛 하나의 로그 보기

> `-u` 는 유닛 자신이 남긴 줄과 그 유닛에 대해 systemd 가 남긴 시작·종료 줄을 함께 보여 줍니다.[^unit]

`--no-pager` 는 앞서 풀었고, 이 셸은 `SYSTEMD_PAGER` 로 페이저를 이미 껐으므로 이후 예에서는 붙이지 않습니다.[^pager]

```bash
# Starting·Finished 줄은 systemd[1] 이 남긴 것이고 lab-report[PID] 줄은 서비스가 남긴 것이다
journalctl -u lab-report --no-pager
```

```bash
Nov 14 07:50:09 ubuntu systemd[1]: Starting lab-report.service - lab report job...
Nov 14 07:50:09 ubuntu lab-report[56231]: lab-report: starting
Nov 14 07:50:09 ubuntu lab-report[56231]: lab-report: disk almost full
Nov 14 07:50:09 ubuntu lab-report[56231]: lab-report: write failed
Nov 14 07:50:09 ubuntu lab-report[56231]: lab-report: done
Nov 14 07:50:09 ubuntu systemd[1]: lab-report.service: Deactivated successfully.
Nov 14 07:50:09 ubuntu systemd[1]: Finished lab-report.service - lab report job.
```

### 끝 몇 줄과 거꾸로 읽기

> `-n` 은 끝에서 몇 줄만 남기고 `-r` 은 최근 줄이 먼저 나오게 뒤집습니다.[^lines]

`-n` 에 숫자를 주지 않으면 10줄이고, 숫자 앞에 `+` 를 붙이면 끝이 아니라 처음부터 셉니다.[^lines]

```bash
# 끝 3줄만 낸다
#   -n   보일 줄 수 (--lines)
journalctl -u lab-report -n 3
```

```bash
Nov 14 07:50:09 ubuntu lab-report[56231]: lab-report: done
Nov 14 07:50:09 ubuntu systemd[1]: lab-report.service: Deactivated successfully.
Nov 14 07:50:09 ubuntu systemd[1]: Finished lab-report.service - lab report job.
```

```bash
# 같은 3줄을 최근 줄이 먼저 나오게 뒤집는다
#   -r   순서를 뒤집는다 (--reverse)
journalctl \
  -u lab-report \
  -n 3 \
  -r
```

```bash
Nov 14 07:50:09 ubuntu systemd[1]: Finished lab-report.service - lab report job.
Nov 14 07:50:09 ubuntu systemd[1]: lab-report.service: Deactivated successfully.
Nov 14 07:50:09 ubuntu lab-report[56231]: lab-report: done
```

```bash
# + 를 붙이면 처음 2줄이다
journalctl -u lab-report -n +2
```

```bash
Nov 14 07:50:09 ubuntu systemd[1]: Starting lab-report.service - lab report job...
Nov 14 07:50:09 ubuntu lab-report[56231]: lab-report: starting
```

```bash
# 숫자 없이 -n 만 주면 10줄이다. 유닛으로 좁히지 않아 시스템 전체의 끝 10줄을 센다
journalctl -n | wc -l    # 10
```

### 여러 유닛 한꺼번에 보기

> `-u` 를 여러 번 주면 유닛마다 고른 줄을 시간순으로 합치고, 글자 패턴을 주면 이름이 맞는 유닛을 모두 고릅니다.[^unit]

```bash
# 두 유닛의 줄 수를 센다. lab-report 7줄에 lab-backup 5줄이다
#   -o   출력 모드 (--output). cat 은 메시지만 낸다 (「출력 모드」)
journalctl \
  -u lab-report \
  -u lab-backup \
  -o cat | wc -l
# 12

# 패턴은 셸이 풀지 않게 따옴표로 감싼다. [rb] 는 r 이나 b 한 글자다
journalctl -u 'lab-[rb]*' -o cat | wc -l    # 12
```

### 새로 쌓이는 로그 따라 읽기

> `-f` 는 끝의 몇 줄을 보이고 새로 쌓이는 줄을 기다리며 계속 냅니다.[^follow]

원래 `Ctrl-C` 로 끝내는 명령이라 이 시트는 `timeout` 으로 시간을 정해 끝냅니다. `timeout` 은 시간이 다 돼서 끝내면 124 를 돌려줍니다.[^timeout]

```bash
# 쌓인 5줄을 먼저 보이고 2초 기다린 뒤 끝난다
#   -f   새로 쌓이는 줄을 따라 읽는다 (--follow)
timeout 2 journalctl \
  -f \
  -u lab-backup \
  -o cat
echo "exit=$?"
```

```bash
Starting lab-backup.service - lab backup job...
lab-backup: copying 3 files
lab-backup: done
lab-backup.service: Deactivated successfully.
Finished lab-backup.service - lab backup job.
exit=124
```

```bash
# 쌓인 줄은 건너뛰고 새 줄만 받는다. 1초 뒤 새 유닛을 돌려 줄을 만든다
#   -n 0   처음에 보일 줄 수를 0 으로 둔다
( sleep 1
  systemd-run \
    --unit=lab-live \
    --description="lab live job" \
    --quiet \
    --wait \
    --collect \
    -p Type=oneshot \
    /bin/echo "lab-live: hello" ) &
timeout 4 journalctl \
  -f \
  -n 0 \
  -u lab-live \
  -o cat
echo "exit=$?"
wait
```

```bash
Starting lab-live.service - lab live job...
lab-live: hello
lab-live.service: Deactivated successfully.
Finished lab-live.service - lab live job.
exit=124
```

### 시각으로 좁히기

> `--since` 와 `--until` 은 시각 범위 안의 줄만 보이고, 날짜 자리에는 `today`·`-3h` 같은 말도 쓸 수 있습니다.[^since]

```bash
# 오늘 0시 이후의 줄만 낸다
#   --since   이 시각부터 (-S)
#   --until   이 시각까지 (-U)
journalctl \
  -u lab-report \
  --since today \
  -o cat
```

```bash
Starting lab-report.service - lab report job...
lab-report: starting
lab-report: disk almost full
lab-report: write failed
lab-report: done
lab-report.service: Deactivated successfully.
Finished lab-report.service - lab report job.
```

```bash
# 3시간 전부터의 줄 수를 센다
journalctl \
  -u lab-report \
  --since -3h \
  -o cat | wc -l
# 7

# 어제 0시까지만 보면 오늘 남은 줄이 없어 출력 없이 끝난다
journalctl \
  -u lab-report \
  --until yesterday \
  -o cat; echo $?
# 0
```

```bash
# 시각 두 개로 구간을 정한다. 시각은 실습 준비를 돌린 때로 바꿔 쓴다
# 이 시트의 줄은 07:50:09 에 남았다
journalctl \
  -u lab-report \
  --since "2026-11-14 07:50:00" \
  --until "2026-11-14 07:50:30" \
  -n 3
```

```bash
Nov 14 07:50:09 ubuntu lab-report[56231]: lab-report: done
Nov 14 07:50:09 ubuntu systemd[1]: lab-report.service: Deactivated successfully.
Nov 14 07:50:09 ubuntu systemd[1]: Finished lab-report.service - lab report job.
```

### 부팅으로 좁히기

> `-b` 는 부팅 하나의 줄만 고르고 `--list-boots` 는 저널에 기록된 부팅과 그 ID 를 보여 줍니다.[^boot]

```bash
# 기록된 부팅을 센다. IDX 0 이 지금 부팅이다
#   --list-boots   부팅 번호·ID·첫 줄과 끝 줄의 시각을 낸다
journalctl --list-boots
```

```bash
IDX BOOT ID                          FIRST ENTRY                 LAST ENTRY
  0 70f87065d40a408d88f0c9cfd9e3151d Tue 2026-11-10 16:53:51 KST Sat 2026-11-14 07:56:29 KST
```

```bash
# 지금 부팅의 줄만 고른다
#   -b   부팅 하나로 좁힌다. 인자가 없으면 지금 부팅이다 (--boot)
journalctl \
  -b \
  -u lab-backup \
  -o cat
```

```bash
Starting lab-backup.service - lab backup job...
lab-backup: copying 3 files
lab-backup: done
lab-backup.service: Deactivated successfully.
Finished lab-backup.service - lab backup job.
```

```bash
# -1 은 바로 전 부팅이다. 기록된 부팅이 하나뿐이라 오류로 끝난다
journalctl \
  -b -1 \
  -u lab-backup \
  -o cat; echo $?
# No journal boot entry found for the specified boot (-1). / 1
```

### 심각도로 좁히기

> `-p` 는 고른 심각도와 그보다 더 심각한 줄을 보이고 `A..B` 로 범위를 줄 수 있습니다.[^prio]

```bash
# err 와 더 심각한 줄만 낸다. lab-report 에는 <3> 줄 하나뿐이다
#   -p   심각도 (--priority). 이름이나 숫자를 쓴다
journalctl \
  -u lab-report \
  -p err \
  -o cat
# lab-report: write failed

# warning 이상이면 <4> 줄이 더해진다
journalctl \
  -u lab-report \
  -p warning \
  -o cat
```

```bash
lab-report: disk almost full
lab-report: write failed
```

```bash
# 범위를 주면 양 끝을 포함한 그 사이만 낸다. info 와 notice 만 남는다
journalctl \
  -u lab-report \
  -p info..notice \
  -o cat
```

```bash
Starting lab-report.service - lab report job...
lab-report: starting
lab-report: done
lab-report.service: Deactivated successfully.
Finished lab-report.service - lab report job.
```

### 커널 메시지 보기

> `-k` 는 커널이 남긴 메시지만 고르고 지금 부팅으로 한정합니다.[^dmesg]

```bash
# 커널 첫 줄의 버전만 본다
#   -k   커널 메시지만 본다 (--dmesg)
journalctl \
  -k \
  -g 'Linux version' \
  -o cat | cut -c1-50
# Linux version 7.2.12-orbstack-00394-gbecdd6130068
```

### 필드로 좁히기

> 저널 항목은 필드의 묶음이라 `필드=값` 을 그대로 조건으로 줄 수 있고, `-t` 는 `SYSLOG_IDENTIFIER=` 와 같은 줄을 고릅니다.[^match]

```bash
# lab-web 이 남긴 줄을 -t 로 고른다
#   -t   syslog 식별자 (--identifier). logger -t 와 systemd-cat -t 가 정한 이름이다
journalctl -t lab-web -o cat
```

```bash
lab-web: cache miss rate high
lab-web: request served
```

```bash
# 같은 줄을 필드 이름으로 고른다
journalctl SYSLOG_IDENTIFIER=lab-web -o cat
```

```bash
lab-web: cache miss rate high
lab-web: request served
```

```bash
# 프로세스 번호로 고른다. 먼저 lab-backup 의 PID 를 읽는다 (대괄호 안)
journalctl -t lab-backup -n 1
# Nov 14 07:50:09 ubuntu lab-backup[56234]: lab-backup: done

# 위 PID 로 그 프로세스가 남긴 줄만 낸다. 번호는 자기 출력의 것으로 바꾼다
journalctl _PID=56234 -o cat
```

```bash
lab-backup: copying 3 files
lab-backup: done
```

```bash
# 같은 필드를 두 번 주면 둘 중 하나인 줄이다 (OR)
journalctl SYSLOG_IDENTIFIER=lab-web SYSLOG_IDENTIFIER=lab-batch -o cat
```

```bash
lab-web: cache miss rate high
lab-web: request served
lab-batch: from systemd-cat
```

```bash
# 다른 필드를 같이 주면 둘 다 맞는 줄이다 (AND). PRIORITY=4 는 warning 이다
journalctl SYSLOG_IDENTIFIER=lab-web PRIORITY=4 -o cat    # lab-web: cache miss rate high

# 낱말 + 는 앞뒤 조건 묶음을 OR 로 잇는다
journalctl \
  SYSLOG_IDENTIFIER=lab-web PRIORITY=4 \
  + \
  SYSLOG_IDENTIFIER=lab-batch \
  -o cat
```

```bash
lab-web: cache miss rate high
lab-batch: from systemd-cat
```

### 필드 값과 이름 찾기

> `-F` 는 필드가 가진 값을, `-N` 은 저널에 쓰인 필드 이름을 중복 없이 보여 줍니다.[^fieldlist]

```bash
# 식별자 중 이 시트가 만든 것만 거른다
#   -F   이 필드가 가진 값의 목록 (--field)
journalctl -F SYSLOG_IDENTIFIER \
  | grep -E '^lab-(web|batch|report|backup|crash)$'
```

```bash
lab-batch
lab-web
lab-crash
lab-backup
lab-report
```

```bash
# 저널 전체에 쓰인 심각도 값. 3(err)부터 7(debug)까지 있다
journalctl -F PRIORITY | sort
```

```bash
3
4
5
6
7
```

```bash
# 자주 쓰는 필드 다섯이 모두 저널에 있는지 센다
#   -N   저널에 쓰인 필드 이름의 목록 (--fields)
journalctl -N \
  | grep -cE '^(PRIORITY|SYSLOG_IDENTIFIER|_PID|_SYSTEMD_UNIT|MESSAGE)$'
# 5
```

### 문자열로 찾기

> `-g` 는 메시지에서 정규식에 맞는 줄만 고르고, 정규식이 모두 소문자일 때만 대소문자를 가리지 않습니다.[^grep]

```bash
# | 로 두 낱말 중 하나가 든 줄을 찾는다
journalctl \
  -u lab-report \
  -g 'almost|failed' \
  -o cat
```

```bash
lab-report: disk almost full
lab-report: write failed
```

```bash
# 대문자가 섞이면 대소문자를 가려서 아무것도 못 찾는다
journalctl \
  -u lab-report \
  -g 'Write' \
  -o cat; echo "rc=$?"
# rc=1

# --case-sensitive=no 로 가리지 않게 되돌린다
#   --case-sensitive   대소문자를 가릴지 정한다
journalctl \
  -u lab-report \
  -g 'Write' \
  --case-sensitive=no \
  -o cat
# lab-report: write failed

# 소문자 정규식은 그대로도 가리지 않는다
journalctl \
  -u lab-report \
  -g 'write' \
  -o cat
# lab-report: write failed
```

### 실패한 서비스 원인 찾기

> 실패한 유닛은 `-p err` 로 실패 줄을 먼저 보고, `-xe` 로 줄마다 설명을 붙여 끝에서부터 읽습니다.

`systemctl status` 가 끝에 붙이는 로그와의 관계는 [systemctl 참조 시트](./systemctl.md)의 「실패한 서비스 추적」 에서 봅니다.

```bash
# 실패 줄만 낸다
journalctl \
  -u lab-crash \
  -p err \
  -o cat
# Failed to start lab-crash.service - lab crash job.
```

```bash
# systemd 가 권하는 꼴이다. 앞 아홉 줄만 본다
#   -x   메시지 카탈로그의 설명을 줄 아래에 붙인다 (--catalog)
#   -e   페이저에서 끝으로 바로 간다 (--pager-end). 줄 수를 1000 으로 둔다
journalctl -xeu lab-crash | head -9
```

```bash
Nov 14 07:50:09 ubuntu systemd[1]: Starting lab-crash.service - lab crash job...
░░ Subject: A start job for unit lab-crash.service has begun execution
░░ Defined-By: systemd
░░ Support: http://www.ubuntu.com/support
░░ 
░░ A start job for unit lab-crash.service has begun execution.
░░ 
░░ The job identifier is 25393.
Nov 14 07:50:09 ubuntu lab-crash[56237]: lab-crash: starting
```

`-x` 의 설명은 일부 메시지에만 있고, 이 줄들은 버그 보고에 붙일 때는 빼라고 매뉴얼이 적습니다.[^catalog] `-e` 는 less 를 쓸 때만 뜻이 있고 줄 수 1000 과 지금 부팅 한정도 함께 겁니다.[^pagerend]

```bash
# 유닛을 가장 최근에 돌린 한 번의 줄만 낸다
#   -I   그 유닛의 가장 최근 실행(invocation)의 줄만 본다
journalctl \
  -u lab-crash \
  -I \
  -o cat
```

```bash
Starting lab-crash.service - lab crash job...
lab-crash: starting
lab-crash: giving up
lab-crash.service: Main process exited, code=exited, status=3/NOTIMPLEMENTED
lab-crash.service: Failed with result 'exit-code'.
Failed to start lab-crash.service - lab crash job.
```

### 실습 정리

> 아래 블록으로 남은 failed 유닛 표시를 지웁니다.

저널에 남은 줄은 지우지 않습니다. 저널을 줄이는 일은 저장 공간 시트에서 복사본으로만 했습니다.

```bash
# lab-crash 의 failed 표시를 지운다
systemctl reset-failed lab-crash
```



## 주의사항과 동작 원리

### 없는 유닛 이름의 종료 코드 0

> `-u` 에 오타를 내도 오류 없이 `-- No entries --` 만 나오고 종료 코드는 0 이라, 스크립트가 빈 로그를 정상으로 읽습니다.

```bash
# 유닛 이름이 틀려도 종료 코드는 0 이다
journalctl -u lab-nothing; echo $?
# -- No entries -- / 0

# -q 를 주면 안내도 사라져 아무 출력이 없다
journalctl -q -u lab-nothing; echo $?    # 0
```

이름이 맞는지는 `systemctl status 유닛` 의 종료 코드 4 로 따로 확인합니다.[^unit]

### `-u` 와 `_SYSTEMD_UNIT=` 의 차이

> `-u` 는 유닛의 줄에 systemd 가 그 유닛에 대해 남긴 줄을 더하고, `_SYSTEMD_UNIT=` 는 유닛 프로세스의 줄만 고릅니다.

```bash
# 프로세스가 남긴 2줄
journalctl _SYSTEMD_UNIT=lab-backup.service -o cat | wc -l    # 2

# Starting·Deactivated·Finished 3줄이 더해진 5줄
journalctl -u lab-backup -o cat | wc -l    # 5
```

`-u` 의 정의는 `_SYSTEMD_UNIT=` 매치에 systemd 가 남긴 줄과 코어덤프 줄 매치를 더하는 것입니다.[^unit]

### `-F` 와 좁히기 옵션의 충돌

> `-F`·`-N` 에 `-u`·`-t`·`--since` 같은 좁히기 옵션을 붙이면 거부하므로, 유닛 안의 값 목록은 JSON 으로 뽑아 `sort -u` 로 줄입니다.

```bash
# 유닛을 좁혀 필드 값을 묻는다
journalctl -F PRIORITY -u lab-report; echo $?
```

```bash
-F/--field= and -N/--fields cannot be combined with options that limit the journal.
1
```

```bash
# 우회: JSON 에서 필드만 뽑아 중복을 없앤다
journalctl -u lab-report -o json | jq -r .PRIORITY | sort -u
```

```bash
3
4
6
```

`필드=값` 매치를 붙여도 `Extraneous arguments` 오류로 거부됩니다.[^fieldlist]

### `-g` 와 `-n` 의 역순 출력

> `-n` 에 `+` 를 붙이지 않고 `-g` 와 쓰면 `-r` 이 켜져서 최근 줄이 먼저 나옵니다.

```bash
# -r 을 주지 않았는데 최근 줄이 먼저 나온다
journalctl \
  -u lab-report \
  -g 'lab-report' \
  -n 2 \
  -o cat
```

```bash
Finished lab-report.service - lab report job.
lab-report.service: Deactivated successfully.
```

매뉴얼이 `-n` 에 "When not prefixed with "+" and used with --grep=, --reverse is implied." 라고 적습니다.[^lines]



## 관련 문서

> 이 시트의 예와 이어지는 시트와 책 노트입니다.

- [journalctl 저장 공간과 읽기 권한](./journalctl%20저장%20공간과%20읽기%20권한.md) — 저널 크기·저장 위치·정리와 읽기 권한
- [journalctl 출력 모양과 jq](./journalctl%20출력%20모양과%20jq.md) — 출력 모양 바꾸기, `jq` 와 잇기, `-T` 가 `-o cat` 에서 듣지 않는 함정
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [systemctl 참조 시트](./systemctl.md) — `status` 의 꼬리 로그와 실패한 서비스 추적
- [systemctl 유닛 설정과 타이머](./systemctl%20유닛%20설정과%20타이머.md) — 유닛을 만들고 주기 실행으로 로그를 쌓는 법
- [systemctl 함정과 동작 원리](./systemctl%20함정과%20동작%20원리.md) — 서비스 이름과 파일 자리가 만드는 함정
- [책 노트 8장 3절, 필요한 줄을 찾는다](../../../book/learning-modern-linux/08-01.재는%20것은%20바깥이고%20알고%20싶은%20것은%20안이다.md#journalctl-로-좁히기) — 저널이 필드의 묶음인 이유와 신뢰 필드
- [책 노트 6장 5절, 손으로 만지는 도구들](../../../book/learning-modern-linux/06-01.먼저%20켜지는%20것%20하나가%20나머지%20전부를%20켠다.md#5-손으로-만지는-도구들) — journald 가 systemd 의 구성요소인 배경



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- 검증 환경: OrbStack Ubuntu 26.04 VM, systemd 259.9 (`259.9-0ubuntu0.1`) — 2026-11-14 실측, `journalctl --help`·`man journalctl` 원문 대조
- [journalctl(1)](https://www.freedesktop.org/software/systemd/man/latest/journalctl.html) — freedesktop.org 최신판에서 각주 인용문의 존재를 확인
- [syslog(3)](https://man7.org/linux/man-pages/man3/syslog.3.html) · [timeout(1)](https://man7.org/linux/man-pages/man1/timeout.1.html)

[^env]: journalctl(1) DESCRIPTION — "journalctl is used to print the log entries stored in the journal by systemd-journald.service(8) and systemd-journal-remote.service(8)." macOS 호스트에서는 `command -v journalctl` 이 아무것도 내지 않고 종료 코드 1 이었습니다(2026-11-14 실측). https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
[^syn]: journalctl(1) DESCRIPTION — "If called without parameters, it will show the contents of the journal accessible to the calling user, starting with the oldest entry collected." https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
[^prio]: journalctl(1) `-p` — "If a single log level is specified, all messages with this log level or a lower (hence more important) log level are shown. If a range is specified, all messages within the range are shown, including both the start and the end value of the range." 뜻은 syslog(3) — "LOG_EMERG system is unusable", "LOG_ALERT action must be taken immediately", "LOG_CRIT critical conditions", "LOG_ERR error conditions", "LOG_WARNING warning conditions", "LOG_NOTICE normal, but significant, condition", "LOG_INFO informational message", "LOG_DEBUG debug-level message". https://man7.org/linux/man-pages/man3/syslog.3.html
[^outmode]: journalctl(1) `-o` — "short is the default and generates an output that is mostly identical to the formatting of classic syslog files, showing one line per journal entry." "short-iso is very similar, but shows timestamps in the RFC 3339 profile of ISO 8601." "short-precise is very similar, but shows classic syslog timestamps with full microsecond precision." "cat generates a very terse output, only showing the actual message of each journal entry with no metadata, not even a timestamp." "verbose shows the full-structured entry items with all fields." "json formats entries as JSON objects, separated by newline characters" "json-pretty formats entries as JSON data structures, but formats them in multiple lines in order to make them more readable by humans." https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
[^exit]: journalctl(1) EXIT STATUS — "On success, 0 is returned; otherwise, a non-zero failure code is returned." 이 절의 0 과 1 은 `명령; echo $?` 로 읽은 실측입니다. https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
[^unit]: journalctl(1) `-u` — "Show messages for the specified systemd unit UNIT (such as a service unit), or for any of the units matched by PATTERN." "For each unit name, a match is added for messages from the unit ("_SYSTEMD_UNIT=UNIT"), along with additional matches for messages from systemd and messages about coredumps for the specified unit." https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
[^pager]: journalctl(1) ENVIRONMENT — "Setting those environment variables to an empty string or the value "cat" is equivalent to passing --no-pager." https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
[^lines]: journalctl(1) `-n` — "The default value is 10 if no argument is given." "Additionally, if the number is prefixed with "+", the oldest journal events are used instead." "When not prefixed with "+" and used with --grep=, --reverse is implied." https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
[^follow]: journalctl(1) `-f` — "Show only the most recent journal entries, and continuously print new entries as they are appended to the journal, until Ctrl-C is hit (or the tool is otherwise terminated)." https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
[^timeout]: timeout(1) EXIT STATUS — "124 if COMMAND times out, and --preserve-status is not specified". https://man7.org/linux/man-pages/man1/timeout.1.html
[^since]: journalctl(1) `-S, --since=, -U, --until=` — "Start showing entries on or newer than the specified date, or on or older than the specified date, respectively." "Alternatively the strings "yesterday", "today", "tomorrow" are understood" "Finally, relative times may be specified, prefixed with "-" or "+", referring to times before or after the current time, respectively." https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
[^boot]: journalctl(1) `-b` — "Show messages from a specific boot. This will add a match for "_BOOT_ID="." `--list-boots` — "Show a tabular list of boot numbers (relative to the current boot), their IDs, and the timestamps of the first and last message pertaining to the boot." https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
[^dmesg]: journalctl(1) `-k` — "Show only kernel messages. This adds the match "_TRANSPORT=kernel". This implies --boot=0 unless explicitly specified otherwise." https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
[^match]: journalctl(1) DESCRIPTION — "If two matches apply to the same field, then they are automatically matched as alternatives" "Finally, the character "+" may appear as a separate word between other terms on the command line. This causes all matches before and after to be combined in a disjunction (i.e. logical OR)." `-t` — "Show messages for the specified syslog identifier SYSLOG_IDENTIFIER." https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
[^fieldlist]: journalctl(1) `-F` — "Print all possible data values the specified field can take in all entries of the journal." `-N` — "Print all field names currently used in all entries of the journal." 좁히기 옵션과 합칠 수 없다는 제한은 매뉴얼에 없고 실측한 오류 문구입니다. https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
[^grep]: journalctl(1) `-g` — "If the pattern is all lowercase, matching is case insensitive. Otherwise, matching is case sensitive. This can be overridden with the --case-sensitive option" https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
[^catalog]: journalctl(1) `-x` — "Augment log lines with explanation texts from the message catalog." "Note: when attaching journalctl output to bug reports, please do not use -x." https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
[^pagerend]: journalctl(1) `-e` — "This implies --lines=1000 and --boot=0 unless explicitly specified otherwise, to guarantee that the pager will not buffer logs of unbounded size. Note that this option is only supported for the less(1) pager." https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
