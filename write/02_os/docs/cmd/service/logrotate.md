---
title: logrotate 참조 시트
tags: [linux, cheatsheet, logrotate, log, sysadmin, cli, reference]
status: draft
source:
  - https://man7.org/linux/man-pages/man8/logrotate.8.html
  - https://man7.org/linux/man-pages/man3/sd_booted.3.html
  - OrbStack Debian 12 (logrotate 3.21.0)·Rocky Linux 9.8 (logrotate 3.18.0)·Ubuntu 24.04.5 실측
related:
  - ./journalctl.md
  - ./rsyslog·logger.md
  - ../text/grep.md
  - ../../../book/learning-modern-linux/08-01.%EC%9E%AC%EB%8A%94%20%EA%B2%83%EC%9D%80%20%EB%B0%94%EA%B9%A5%EC%9D%B4%EA%B3%A0%20%EC%95%8C%EA%B3%A0%20%EC%8B%B6%EC%9D%80%20%EA%B2%83%EC%9D%80%20%EC%95%88%EC%9D%B4%EB%8B%A4.md
updated: 2026-11-16
---

# logrotate 참조 시트

---

> 설정 파일에 선언한 주기와 용량 조건으로 로그 파일을 순환하고 압축해 디스크 고갈을 막는 `logrotate` 를 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `logrotate` 는 로그 파일의 순환, 압축, 제거와 메일 발송을 자동화하는 관리 도구입니다.

logrotate 패키지의 외부 바이너리(`/usr/sbin/logrotate`)이며 macOS 에는 없습니다.[^env] 이 시트의 출력은 OrbStack Debian 12 와 Rocky Linux 9.8 에서 root 셸로 받았고 시각은 KST 입니다.



## 핵심 문법

> 대상과 동작 조건은 설정 파일에 적고, 명령줄에서는 `-d` 로 점검하거나 `-f` 로 즉시 회전합니다.

```bash
# 호출 형태
# logrotate man 페이지의 SYNOPSIS
logrotate [--force] [--debug] [--state file] [--skip-state-lock] [--wait-for-state-lock] [--verbose] [--log file] [--mail command] config_file [config_file2 ...]

# 설정 파일의 판정 결과만 미리 본다 (모의 실행으로 회전 판정 확인)
logrotate -d 설정파일

# 조건을 무시하고 즉시 강제 회전한다 (강제 회전과 상태 파일 확인)
logrotate -f -v 설정파일

# 상태 파일 위치를 따로 정한다 (강제 회전과 상태 파일 확인)
logrotate -s 상태파일 설정파일

# 후처리 스크립트를 포함해 강제 회전한다 (후처리 스크립트 실행)
logrotate -f 설정파일

# 회전 주기를 관리하는 systemd 타이머 상태를 본다 (systemd 타이머로 주기 실행 확인)
systemctl list-timers logrotate.timer

# gzip 으로 압축된 회전 로그 안을 검색한다 (회전된 압축 파일 검색)
zgrep -c 문자열 로그패턴
```

### 주요 설정 지시어

> 회전 주기, 보관 개수, 압축, 새 파일 생성 방식을 설정 블록 안에서 선언합니다.

매뉴얼의 지시어 목록에서 본문 예제가 쓰는 항목을 추렸습니다.[^directives]

```bash
# 설정 블록에 적는 핵심 지시어와 기본 동작
# daily           로그를 매일 한 번 회전한다
# weekly          로그를 매주 한 번 회전한다 (Debian 12·Rocky 9 이미지의 기본 logrotate.conf 가 전역으로 둔 값)
# rotate 개수     오래된 로그를 지우기 전까지 보관할 세대 수를 정한다
# size 크기       로그가 지정한 용량을 넘었을 때만 회전한다
# compress        회전된 옛 로그를 gzip 으로 압축한다
# delaycompress   직전 세대(.1)의 압축을 다음 회전 주기로 미룬다
# missingok       로그 파일이 없어도 오류를 내지 않고 넘어간다
# notifempty      로그 파일이 비어 있으면 회전하지 않는다
# create 권한 소유자 그룹  회전 직후 새 빈 로그 파일을 지정 권한으로 만든다
# copytruncate    로그를 새 파일로 옮기지 않고 복사 후 원본을 0 바이트로 비운다
# sharedscripts   와일드카드로 여러 로그가 걸려도 스크립트를 한 번만 돌린다
# postrotate      회전 직후 실행할 셸 스크립트 블록을 시작한다
# endscript       postrotate 블록을 닫는다 (두 단어는 각각 줄을 따로 차지해야 한다)
```



## 종료 코드

> 성공하면 0, 회전 중 오류가 나면 1을 포함한 0이 아닌 값을 돌려줍니다.[^exit]

아래 값은 실측값이며 없는 설정 파일을 주거나 문법이 틀리면 1로 끝납니다.

```bash
# 0  성공 (정상 회전 또는 디버그 모드 정상 종료)
# 1  오류 (설정 파일 없음, 문법 오류, 디렉터리 보안 위반)
# 3  상태 파일 락 획득 실패 (동시 실행 방지 락 경합 시)

# 옵션 뜻
#   -d   실제 파일을 바꾸지 않고 디버그 메시지만 낸다 (--debug)
logrotate -d /etc/logrotate.d/demo >/dev/null 2>&1; echo status-of-d=$?
# status-of-d=0

logrotate -d /etc/logrotate.d/nothere; echo $?
```

```bash
warning: logrotate in debug mode does nothing except printing debug messages!  Consider using verbose mode (-v) instead if this is not what you want.

error: cannot stat /etc/logrotate.d/nothere: No such file or directory
Reading state from file: /var/lib/logrotate/status
Allocating hash table for state file, size 64 entries
Creating new state

Handling 0 logs
1
```

```bash
# 문법 오류가 있는 설정 파일
cat /etc/logrotate.d/bad
```

```bash
/srv/demo/app.log {
    rotate abc
}
```

```bash
logrotate -d /etc/logrotate.d/bad; echo $?
```

```bash
warning: logrotate in debug mode does nothing except printing debug messages!  Consider using verbose mode (-v) instead if this is not what you want.

reading config file /etc/logrotate.d/bad
error: /etc/logrotate.d/bad:2 bad rotation count 'abc'
error: found error in /srv/demo/app.log , skipping
removing last 1 log configs
Reading state from file: /var/lib/logrotate/status
Allocating hash table for state file, size 64 entries
Creating new state

Handling 0 logs
1
```



## 유스케이스

> 예제는 앞 예제가 만든 상태를 이어 쓰므로 위에서 아래로 차례로 돌립니다.

### 실습 준비

> 아래 블록을 root 셸에 붙여 넣으면 이 시트의 예제가 읽고 회전할 파일과 설정이 생깁니다.

실습 환경은 Debian 12 와 Rocky Linux 9 모두 `adm` 그룹이 있어야 합니다.

```bash
# 실습이 끝나면 「실습 정리」 블록으로 만든 파일과 디렉터리를 지운다
# demo: 실습용 디렉터리와 초기 로그 파일. 「모의 실행으로 회전 판정 확인」부터 여러 곳에서 쓴다
mkdir -p /srv/demo
cat << 'EOF' > /srv/demo/app.log
first line of app.log
second line of app.log
third line of app.log
EOF
chmod 644 /srv/demo/app.log

# /etc/logrotate.d/demo: 실습용 logrotate 설정 파일
cat << 'EOF' > /etc/logrotate.d/demo
/srv/demo/app.log {
    daily
    rotate 3
    size 1M
    create 0640 root adm
    missingok
    notifempty
}
EOF
chmod 644 /etc/logrotate.d/demo
```

실측 때 app.log 의 내용은 기록하지 않아, 이 세 줄로 만들면 아래 출력의 크기(112)와 다르게 나옵니다.

### 모의 실행으로 회전 판정 확인

> `-d` 는 실제 로그와 상태 파일을 건드리지 않고 회전 조건에 부합하는지만 판단해 보여 줍니다.[^debug]

`-d` 는 옵션 뜻을 앞서 풀었으므로 따로 주석을 달지 않습니다.

```bash
# 현재 설정 내용 확인
cat /etc/logrotate.d/demo
```

```bash
/srv/demo/app.log {
    daily
    rotate 3
    size 1M
    create 0640 root adm
    missingok
    notifempty
}
```

```bash
# 모의 실행으로 디버그 판정 출력
logrotate -d /etc/logrotate.d/demo
```

```bash
warning: logrotate in debug mode does nothing except printing debug messages!  Consider using verbose mode (-v) instead if this is not what you want.

reading config file /etc/logrotate.d/demo
note: 'size' overrides previously specified 'daily'
Reading state from file: /var/lib/logrotate/status
state file /var/lib/logrotate/status does not exist
Allocating hash table for state file, size 64 entries

Handling 1 logs

rotating pattern: /srv/demo/app.log  1048576 bytes (3 rotations)
empty log files are not rotated, old logs are removed
considering log /srv/demo/app.log
Creating new state
  Now: 2026-11-15 21:51
  Last rotated at 2026-11-15 21:00
  log does not need rotating (log size is below the 'size' threshold)
```

로그 용량이 1M(1048576 바이트)에 못 미치므로 회전하지 않는다고 판단합니다. Rocky 9 에서는 경고 접두사가 `WARNING:` 이고 상태 파일 없음을 알리지만 정상 종료합니다.

### 강제 회전과 상태 파일 확인

> `-f` 는 조건을 따지지 않고 회전하며 `-v` 는 처리 단계를 자세히 보여 줍니다.[^force]

```bash
# 회전 전 파일의 inode 번호와 크기 확인
#   ls -i   inode 번호를 함께 본다
ls -li /srv/demo/
```

```bash
total 4
15764 -rw-r--r-- 1 root root 112 Nov 15 21:51 app.log
```

```bash
# 강제 회전 실행과 과정 출력
#   -f   조건을 따지지 않고 강제 회전한다 (--force)
#   -v   회전 과정을 자세히 보여 준다 (--verbose)
logrotate -f -v /etc/logrotate.d/demo
```

```bash
reading config file /etc/logrotate.d/demo
note: 'size' overrides previously specified 'daily'
Creating stub state file: /var/lib/logrotate/status
acquired lock on state file /var/lib/logrotate/statusReading state from file: /var/lib/logrotate/status
Allocating hash table for state file, size 64 entries

Handling 1 logs

rotating pattern: /srv/demo/app.log  forced from command line (3 rotations)
empty log files are not rotated, old logs are removed
considering log /srv/demo/app.log
Creating new state
  Now: 2026-11-15 21:51
  Last rotated at 2026-11-15 21:00
  log needs rotating
rotating log /srv/demo/app.log, log->rotateCount is 3
dateext suffix '-20261115'
glob pattern '-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'
renaming /srv/demo/app.log.3 to /srv/demo/app.log.4 (rotatecount 3, logstart 1, i 3), 
old log /srv/demo/app.log.3 does not exist
renaming /srv/demo/app.log.2 to /srv/demo/app.log.3 (rotatecount 3, logstart 1, i 2), 
old log /srv/demo/app.log.2 does not exist
renaming /srv/demo/app.log.1 to /srv/demo/app.log.2 (rotatecount 3, logstart 1, i 1), 
old log /srv/demo/app.log.1 does not exist
log /srv/demo/app.log.4 doesn't exist -- won't try to dispose of it
renaming /srv/demo/app.log to /srv/demo/app.log.1
creating new /srv/demo/app.log mode = 0640 uid = 0 gid = 4
```

```bash
# 회전 후 새 파일과 회전된 백업 파일의 inode 확인
ls -li /srv/demo/
```

```bash
total 4
15766 -rw-r----- 1 root adm    0 Nov 15 21:51 app.log
15764 -rw-r--r-- 1 root root 112 Nov 15 21:51 app.log.1
```

기존 파일은 `app.log.1` 로 바뀌며 inode 15764 를 유지하고 새 파일은 inode 15766 으로 생겼습니다.

```bash
# 상태 파일에 기록된 마지막 회전 시각 확인
grep demo /var/lib/logrotate/status
# "/srv/demo/app.log" 2026-11-15-21:51:34

# 상태 파일 락 관련 도움말 확인
#   -s   기본 상태 파일 대신 지정한 상태 파일을 쓴다 (--state)
logrotate --help 2>&1 | grep -i state
```

```bash
  -s, --state=statefile         Path of state file
      --skip-state-lock         Do not lock the state file
      --wait-for-state-lock     Wait for lock on the state file
```

Rocky 9 에서는 상태 파일 경로가 `/var/lib/logrotate/logrotate.status` 입니다.

### 후처리 스크립트 실행

> `postrotate` 지시어로 선언한 셸 스크립트는 해당 로그의 회전이 끝난 직후 실행됩니다.[^postrotate]

```bash
# postrotate 블록이 추가된 설정 확인
cat /etc/logrotate.d/demo
```

```bash
/srv/demo/app.log {
    daily
    rotate 3
    size 1M
    create 0640 root adm
    missingok
    notifempty
    postrotate
        echo rotated-at $(date +%T) >> /tmp/post.log
    endscript
}
```

```bash
# 강제 회전 실행
logrotate -f /etc/logrotate.d/demo

# postrotate 스크립트가 남긴 로그 확인
cat /tmp/post.log    # rotated-at 21:51:38
```

실제 운영 환경에서는 이 스크립트 블록에서 프로세스에 HUP 시그널을 보냅니다.

### systemd 타이머로 주기 실행 확인

> 리눅스 배포판은 logrotate 를 데몬 상주 대신 systemd 타이머 유닛으로 매일 자정에 자동 실행합니다.[^timer]

```bash
# 등록된 logrotate 타이머 유닛의 다음 실행 시각 확인
systemctl list-timers logrotate.timer --no-pager
```

```bash
NEXT                        LEFT         LAST PASSED UNIT            ACTIVATES
Mon 2026-11-16 00:00:00 KST 2h 8min left -    -      logrotate.timer logrotate.service

1 timers listed.
Pass --all to see loaded but inactive timers, too.
```

```bash
# 타이머 유닛 설정 정의 확인
systemctl cat logrotate.timer --no-pager
```

```bash
# /lib/systemd/system/logrotate.timer
[Unit]
Description=Daily rotation of log files
Documentation=man:logrotate(8) man:logrotate.conf(5)

[Timer]
OnCalendar=daily
AccuracySec=1h
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
# 타이머가 구동하는 logrotate 서비스 유닛 확인
systemctl cat logrotate.service --no-pager | head -7
```

```bash
# /lib/systemd/system/logrotate.service
[Unit]
Description=Rotate log files
Documentation=man:logrotate(8) man:logrotate.conf(5)
RequiresMountsFor=/var/log
ConditionACPower=true

[Service]
Type=oneshot
ExecStart=/usr/sbin/logrotate /etc/logrotate.conf
```

`ExecStart` 줄이 `/usr/sbin/logrotate /etc/logrotate.conf` 를 호출하는 점이 확인됩니다. Rocky 9 에서는 유닛 파일 경로가 `/usr/lib/systemd/system/` 아래에 있습니다.

### 옛 cron.daily 와 지금 타이머

> 옛 방식은 `cron.daily` 스크립트가, 지금 방식은 `logrotate.timer` 가 logrotate 를 돌리며, 세 머신에서 어느 쪽이 켜져 있는지 읽기만 하는 명령으로 확인합니다.[^cron-timer]

```bash
# 지금 방식인 타이머가 부팅 때 켜지도록 등록돼 있는지 본다
#   systemctl is-enabled   유닛의 등록 상태를 한 단어로 출력한다
systemctl is-enabled logrotate.timer
# enabled (Debian 12, Rocky 9.8, Ubuntu 24.04 모두)

# 옛 방식인 cron.daily 스크립트가 있는지 본다
ls /etc/cron.daily/logrotate
# Debian 12, Ubuntu 24.04: /etc/cron.daily/logrotate
# Rocky 9.8: ls: cannot access '/etc/cron.daily/logrotate': No such file or directory
```

Debian 과 Ubuntu 에는 스크립트가 남아 있으므로 첫 몇 줄을 읽습니다. 이 줄들은 `/run/systemd/system` 디렉터리가 있으면, 곧 systemd 로 부팅했으면 바로 종료한다는 뜻입니다.[^sd-booted]

```bash
# 스크립트의 3~5줄을 읽는다
#   sed -n   자동 출력을 끄고 p 로 고른 줄만 출력한다
sed -n 3,5p /etc/cron.daily/logrotate
```

```bash
# skip in favour of systemd timer
if [ -d /run/systemd/system ]; then
    exit 0
```

Debian 과 Ubuntu 의 이 스크립트는 타이머에 일을 맡기고 물러납니다. Rocky 9.8 에는 스크립트 자체가 없습니다.

### 회전된 압축 파일 검색

> `compress` 와 `delaycompress` 로 압축된 과거 로그는 `zgrep` 으로 압축 해제 없이 바로 검색합니다.[^compress]

```bash
# 압축 설정이 들어간 설정 확인
cat /etc/logrotate.d/demo
```

```bash
/srv/demo/app.log {
    daily
    rotate 3
    size 1M
    compress
    delaycompress
    create 0640 root adm
    missingok
    notifempty
}
```

```bash
# 세대별 파일 목록과 압축 여부 확인
ls -l /srv/demo/
```

```bash
total 16
-rw-r----- 1 root adm  14 Nov 15 21:51 app.log
-rw-r----- 1 root adm  42 Nov 15 21:51 app.log.1
-rw-r----- 1 root adm  39 Nov 15 21:51 app.log.2.gz
-rw-r--r-- 1 root root 34 Nov 15 21:51 app.log.3.gz
```

직전 회전 파일인 `app.log.1` 은 압축되지 않고 그 이전 세대인 `.2.gz` 와 `.3.gz` 만 압축됩니다.

```bash
# 회전된 모든 로그에서 needle 문자열 개수 검색
#   zgrep -c   일치한 줄 수를 센다 (--count)
zgrep -c needle /srv/demo/app.log*
```

```bash
/srv/demo/app.log:1
/srv/demo/app.log.1:3
/srv/demo/app.log.2.gz:2
/srv/demo/app.log.3.gz:1
```

### 실습 정리

> 아래 블록으로 실습에서 만든 설정 파일과 로그 디렉터리를 정리합니다.

```bash
# 실습에서 만든 설정과 로그 파일, 디렉터리를 지운다
rm -f /etc/logrotate.d/demo /etc/logrotate.d/bad /tmp/post.log
rm -rf /srv/demo
```



## 주의사항과 동작 원리

> 회전 시 파일 기술자 참조 방식과 설정 파일 권한 제한을 이해해야 로그 유실과 중단을 예방할 수 있습니다.

### 열린 파일 기술자와 create·copytruncate

> 프로세스가 파일을 열고 있으면 이름이 바뀌어도 옛 inode 에 쓰므로, `create` 만 쓰면 새 로그가 0 바이트에 머뭅니다.

회전의 기본 동작은 파일 이름 변경이지만 파일 기술자는 inode 를 가리킵니다.[^inode]

```bash
# 1. create 방식: 루프 프로세스 PID 와 회전 전 파일 확인
echo "loop pid=$LP"; ls -li /srv/demo/
```

```bash
loop pid=2575
total 4
15768 -rw-r--r-- 1 root root 145 Nov 15 21:51 app.log
```

```bash
# 강제 회전 실행
logrotate -f /etc/logrotate.d/demo

# 회전 후 inode 확인
ls -li /srv/demo/
```

```bash
total 4
15769 -rw-r----- 1 root adm    0 Nov 15 21:51 app.log
15768 -rw-r--r-- 1 root root 145 Nov 15 21:51 app.log.1
```

```bash
# 프로세스의 열린 파일 기술자(fd 3)가 가리키는 대상 확인
ls -l /proc/$LP/fd/3
# l-wx------ 1 root root 64 Nov 15 21:51 /proc/2575/fd/3 -> /srv/demo/app.log.1

# 파일별 줄 수 확인
wc -l /srv/demo/app.log /srv/demo/app.log.1
```

```bash
  0 /srv/demo/app.log
 10 /srv/demo/app.log.1
 10 total
```

새 파일인 `app.log` 는 0줄이고 이전 파일인 `app.log.1` 에 계속 기록됩니다. 프로세스에 재오픈 시그널을 줄 수 없다면 `copytruncate` 지시어를 씁니다.

```bash
# 2. copytruncate 방식: 루프 프로세스 PID 와 회전 전 파일 확인
echo "loop pid=$LP"; ls -li /srv/demo/
```

```bash
loop pid=2605
total 4
15771 -rw-r--r-- 1 root root 145 Nov 15 21:51 app.log
```

```bash
# 강제 회전 실행
logrotate -f /etc/logrotate.d/demo

# 회전 후 inode 확인
ls -li /srv/demo/
```

```bash
total 8
15771 -rw-r--r-- 1 root root  29 Nov 15 21:51 app.log
15772 -rw-r--r-- 1 root root 145 Nov 15 21:51 app.log.1
```

```bash
# 프로세스의 파일 기술자(fd 3) 확인
ls -l /proc/$LP/fd/3
# l-wx------ 1 root root 64 Nov 15 21:51 /proc/2605/fd/3 -> /srv/demo/app.log

# 파일별 줄 수 확인
wc -l /srv/demo/app.log /srv/demo/app.log.1
```

```bash
  5 /srv/demo/app.log
  5 /srv/demo/app.log.1
 10 total
```

원본의 inode 15771 이 유지되므로 프로세스가 중단 없이 새 파일에 기록을 이어갑니다. 단, 파일 복사와 자르기 사이의 찰나에 쓰인 줄은 유실될 위험이 있습니다.[^copytruncate]

### 설정 파일과 디렉터리의 열린 권한 거부

> 설정 파일이나 상위 디렉터리에 타인의 쓰기 권한이 열려 있으면 보안 위험으로 판단해 회전을 거부합니다.[^insecure]

```bash
# 1. 설정 파일에 0666 권한 부여 시
chmod 666 /etc/logrotate.d/demo; ls -l /etc/logrotate.d/demo
# -rw-rw-rw- 1 root root 111 Nov 15 21:51 /etc/logrotate.d/demo

logrotate -d /etc/logrotate.d/demo
```

```bash
warning: logrotate in debug mode does nothing except printing debug messages!  Consider using verbose mode (-v) instead if this is not what you want.

warning: Potentially dangerous mode on /etc/logrotate.d/demo: 0666
error: Ignoring /etc/logrotate.d/demo because it is writable by group or others.
Reading state from file: /var/lib/logrotate/status
Allocating hash table for state file, size 64 entries
Creating new state

Handling 0 logs
```

설정 파일을 통째로 무시하여 `Handling 0 logs` 로 끝나며 이때 종료 코드는 0 입니다. 권한을 다시 644 로 복구합니다.

```bash
chmod 644 /etc/logrotate.d/demo; ls -l /etc/logrotate.d/demo
# -rw-r--r-- 1 root root 111 Nov 15 21:51 /etc/logrotate.d/demo

# 2. 로그 디렉터리에 0777 권한 부여 시
chmod 777 /srv/demo; ls -ld /srv/demo
# drwxrwxrwx 1 root root 14 Nov 15 21:51 /srv/demo

logrotate -d /etc/logrotate.d/demo
```

```bash
warning: logrotate in debug mode does nothing except printing debug messages!  Consider using verbose mode (-v) instead if this is not what you want.

reading config file /etc/logrotate.d/demo
note: 'size' overrides previously specified 'daily'
Reading state from file: /var/lib/logrotate/status
Allocating hash table for state file, size 64 entries
Creating new state

Handling 1 logs

rotating pattern: /srv/demo/app.log  1048576 bytes (3 rotations)
empty log files are not rotated, old logs are removed
considering log /srv/demo/app.log
error: skipping "/srv/demo/app.log" because parent directory has insecure permissions (It's world writable or writable by group which is not "root") Set "su" directive in config file to tell logrotate which user/group should be used for rotation.
```

상위 디렉터리 권한이 열려 있으면 해당 로그 회전을 건너뛰고 종료 코드 1 을 냅니다. 해결하려면 디렉터리 권한을 755 로 좁히거나 `su` 지시어로 실행 사용자와 그룹을 선언합니다.



## 관련 문서

> 이 시트의 예제와 이어지는 다른 서비스 시트와 책 노트입니다.

- [journalctl 참조 시트](./journalctl.md) — systemd 저널 조회와 저널 보존 용량 관리
- [rsyslog·logger 참조 시트](./rsyslog·logger.md) — 전통적인 syslog 메시지 전송과 파일 저장 규칙
- [grep 참조 시트](../text/grep.md) — 텍스트 로그 파일 검색과 정규식 필터링
- [책 노트 8장 4절, 로그가 디스크를 먹지 않게 한다](../../../book/learning-modern-linux/08-01.%EC%9E%AC%EB%8A%94%20%EA%B2%83%EC%9D%80%20%EB%B0%94%EA%B9%A5%EC%9D%B4%EA%B3%A0%20%EC%95%8C%EA%B3%A0%20%EC%8B%B6%EC%9D%80%20%EA%B2%83%EC%9D%80%20%EC%95%88%EC%9D%B4%EB%8B%A4.md#4-로그가-디스크를-먹지-않게-한다) — logrotate 회전 원리와 저널 보존 한도 이론



## 참고 자료

> 검증 환경, 공식 매뉴얼, 각주 정의입니다.

- 검증 환경: OrbStack Debian 12 (logrotate 3.21.0), Rocky Linux 9.8 (logrotate 3.18.0) — 2026-11-15 실측, `logrotate --help`·`man logrotate` 원문 대조
- 추가 환경: Ubuntu 24.04.5 — 「옛 cron.daily 와 지금 타이머」 절에서만 씁니다. 그 절은 2026-11-16 머신 lml-deb·lml-rocky·lml-ubuntu 에서 받았습니다
- [logrotate(8)](https://man7.org/linux/man-pages/man8/logrotate.8.html) — man7.org 최신 매뉴얼
- [zgrep(1)](https://manpages.debian.org/bookworm/gzip/zgrep.1.en.html)
- [sd_booted(3)](https://man7.org/linux/man-pages/man3/sd_booted.3.html) — man7.org

[^env]: logrotate(8) DESCRIPTION — "logrotate is designed to ease administration of systems that generate large numbers of log files. It allows automatic rotation, compression, removal, and mailing of log files." macOS 호스트에는 기본 설치되어 있지 않으며 `command -v logrotate` 가 아무것도 출력하지 않고 종료 코드 1 을 돌려줍니다. https://man7.org/linux/man-pages/man8/logrotate.8.html
[^directives]: logrotate(8) CONFIGURATION FILE DIRECTIVES — daily: "Log files are rotated every day.", rotate: "Log files are rotated count times before being removed", compress: "Old versions of log files are compressed with /bin/gzip(1) by default.", delaycompress: "Postpone compression of the previous log file to the next rotation cycle.", missingok: "If the log file is missing, go on to the next one without issuing an error message.", notifempty: "Do not rotate the log if it is empty", create: "Immediately after rotation (before the postrotate script is run) the log file is created", copytruncate: "Truncate the original log file to zero size in place after creating a copy", sharedscripts: "the scripts are only run once, no matter how many logs match the wildcarded pattern", weekly: "Log files are rotated once each weekday, or if the date is advanced by at least 7 days since the last rotation (while ignoring the exact time).", postrotate·endscript(SCRIPTS): "The lines between the starting keyword (e.g. prerotate) and endscript (both of which must appear on lines by themselves) are executed (using /bin/sh)." https://man7.org/linux/man-pages/man8/logrotate.8.html
[^exit]: logrotate(8) DESCRIPTION — "If any errors occur while rotating logs, logrotate will exit with non-zero status, although the state file will be updated." OPTIONS `-s` — "To prevent parallel execution logrotate by default acquires a lock on the state file, if it cannot be acquired logrotate will exit with value 3." https://man7.org/linux/man-pages/man8/logrotate.8.html
[^debug]: logrotate(8) OPTIONS `-d, --debug` — "Turn on debug mode, which means that no changes are made to the logs and the logrotate state file is not updated. Only debug messages are printed." https://man7.org/linux/man-pages/man8/logrotate.8.html
[^force]: logrotate(8) OPTIONS `-f, --force` — "Tells logrotate to force the rotation, even if it doesn't think this is necessary." `-v, --verbose` — "Turns on verbose mode, for example to display messages during rotation." https://man7.org/linux/man-pages/man8/logrotate.8.html
[^postrotate]: logrotate(8) SCRIPTS — "The lines between the starting keyword (e.g. prerotate) and endscript (both of which must appear on lines by themselves) are executed (using /bin/sh)." https://man7.org/linux/man-pages/man8/logrotate.8.html
[^timer]: logrotate.timer(8) · systemd.timer(5) — Debian 12 와 Rocky 9 에서는 cron 대신 systemd 타이머 유닛 `logrotate.timer` 로 매일 자정에 주기 실행됩니다. https://man7.org/linux/man-pages/man8/logrotate.8.html
[^compress]: logrotate(8) CONFIGURATION FILE DIRECTIVES `compress`, `delaycompress` — zgrep(1) DESCRIPTION: "The zgrep command invokes grep on compressed or gzipped files." https://manpages.debian.org/bookworm/gzip/zgrep.1.en.html
[^inode]: 책 노트 8장 4절 「옛 inode 에 남는 쓰기와 copytruncate」 — 열린 파일 기술자는 파일 이름이 아니라 inode 번호를 참조하므로 이름이 바뀌어도 기존 inode 에 쓰기가 지속됩니다. https://man7.org/linux/man-pages/man8/logrotate.8.html
[^copytruncate]: logrotate(8) CONFIGURATION FILE DIRECTIVES `copytruncate` — "Note that there is a very small time slice between copying the file and truncating it, so some logging data might be lost." https://man7.org/linux/man-pages/man8/logrotate.8.html
[^insecure]: logrotate(8) CONFIGURATION FILE — "For security reasons configuration files must not be group-writable nor world-writable." `su user group` — "Rotate log files set under this user and group instead of using default user/group (usually root)." https://man7.org/linux/man-pages/man8/logrotate.8.html
[^cron-timer]: 2026-11-16 머신 lml-deb(Debian 12, logrotate 3.21.0)·lml-rocky(Rocky 9.8, logrotate 3.18.0)·lml-ubuntu(Ubuntu 24.04.5)에서 읽기만 하는 명령으로 받았습니다. 세 머신 모두 `systemctl is-enabled logrotate.timer` 가 `enabled` 입니다.
[^sd-booted]: sd_booted(3) DESCRIPTION — "sd_booted() checks whether the system was booted up using the systemd init system." NOTES — "Internally, this function checks whether the directory /run/systemd/system/ exists." https://man7.org/linux/man-pages/man3/sd_booted.3.html
