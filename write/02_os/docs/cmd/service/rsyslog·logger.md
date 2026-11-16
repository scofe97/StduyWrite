---
title: "rsyslog·logger 참조 시트"
tags: ["linux", "command", "service", "rsyslog", "logger", "syslog", "log"]
status: draft
source:
  - "https://man7.org/linux/man-pages/man1/logger.1.html"
  - "https://man7.org/linux/man-pages/man5/rsyslog.conf.5.html"
  - "https://man7.org/linux/man-pages/man8/rsyslogd.8.html"
  - "https://www.rsyslog.com/doc/configuration/index.html"
  - "https://www.rsyslog.com/doc/configuration/conf_formats.html"
  - "https://man7.org/linux/man-pages/man1/systemd-analyze.1.html"
  - "https://man7.org/linux/man-pages/man5/journald.conf.5.html"
  - "OrbStack Debian 12 (rsyslog 8.2302.0, logger util-linux 2.38.1)·Rocky Linux 9.8 (rsyslog 8.2510.0, logger util-linux 2.37.4)·Ubuntu 24.04.5 (rsyslog 8.2312.0) 실측"
related:
  - "../../../book/learning-modern-linux/08-01.재는%20것은%20바깥이고%20알고%20싶은%20것은%20안이다.md"
  - "./journalctl.md"
  - "./logrotate.md"
updated: "2026-11-16"
---

# rsyslog·logger 참조 시트

---

> `logger` 로 로그 한 줄을 발생시키고 `rsyslog` 의 규칙으로 분배·저장하며 `rsyslogd` 로 설정을 검증하는 실측 예제를 모았습니다.

## 개요

> `logger` 는 시스템 로그 소켓에 메시지를 남기는 셸 명령이고, `rsyslog` 는 전달받은 로그를 규칙에 따라 파일로 나누어 쓰는 데몬입니다.

`logger` 는 util-linux 패키지의 외부 바이너리(`/usr/bin/logger`)입니다.[^pkg] `rsyslogd` 는 rsyslog 패키지의 시스템 데몬(`/usr/sbin/rsyslogd`)입니다. 이 시트의 출력은 Debian 12(rsyslog 8.2302.0, logger 2.38.1) 환경에서 실측했습니다.[^env] Rocky Linux 9.8(rsyslog 8.2510.0, logger 2.37.4)의 차이도 함께 적었습니다.

로그 한 줄이 수집되고 파일로 나뉘는 원리와 RFC 5424 구조는 [책 노트 8장 1절, 로그 한 줄은 저널과 파일로 갈라진다](../../../book/learning-modern-linux/08-01.재는%20것은%20바깥이고%20알고%20싶은%20것은%20안이다.md#2-로그-한-줄은-저널과-파일로-갈라진다)에서 다룹니다.



## 핵심 문법

> `logger` 로 메시지와 시설·심각도·전송 방식을 지정하고, `rsyslogd -N1` 로 분배 설정을 검증합니다.

```bash
# 호출 형태
# logger --help 및 rsyslogd -h 의 첫 줄
logger [options] [message]
rsyslogd [ -v ] [ -N level ]

# 기본 메시지를 파일과 저널에 남긴다 (한 줄 메시지 기록과 확인)
logger "plain test"

# 시설과 심각도 및 태그를 지정한다 (시설과 심각도 지정)
logger -p local3.info -t demo "routing test"

# RFC 프로토콜 형식을 지정해 표준 오류로 출력한다 (RFC 형식 지정과 원격 UDP 전송)
logger --rfc5424 -s -p local3.info -t demo "rfc test"

# 원격 syslog 서버로 UDP 패킷을 보낸다 (RFC 형식 지정과 원격 UDP 전송)
logger -n 127.0.0.1 -P 5514 -d -p local3.info -t demo "wire test"

# rsyslogd 설정 파일의 문법을 검증한다 (분배 규칙 추가와 설정 검증, 설정 문법 오류 검출)
rsyslogd -N1

# 기본 분배 규칙을 확인한다 (기본 분배 규칙 확인)
grep -vE "^\s*(#|$)" /etc/rsyslog.conf

# journald 연동 소켓 획득 기록을 확인한다 (저널 연동 소켓 경로 확인)
journalctl -u rsyslog -b --no-pager | grep -i imuxsock
```

### 시설과 심각도

> `-p` 는 `시설.심각도` 형식으로 우선순위를 지정하고, 저널에는 숫자 코드로 기록됩니다.[^facility]

```bash
# -p 에 쓰는 시설 이름과 저널 SYSLOG_FACILITY 실측값
# user     1    사용자 수준 메시지 (기본값)
# local3   19   로컬 사용 시설 3

# -p 에 쓰는 심각도 이름과 저널 PRIORITY 실측값 (숫자가 작을수록 심각함)
# emerg    0    시스템을 쓸 수 없다
# alert    1    즉시 조치해야 한다
# crit     2    위기 상태다
# err      3    오류다
# warning  4    경고다
# notice   5    정상이지만 눈여겨볼 상태다 (기본값)
# info     6    알림이다
# debug    7    디버그 메시지다
```

### 선택자와 PRI 읽는 법

> 규칙의 선택자는 `시설.심각도` 두 칸이고, 맨 앞 `PRI` 숫자는 시설 번호와 심각도 번호로 계산합니다.[^selector]

선택자에서 `*` 는 모든 시설 또는 모든 심각도를 뜻하고 `none` 은 그 시설을 뺍니다. 심각도를 적으면 그 심각도와 더 심각한 줄이 걸립니다. `PRI` 는 시설 번호 × 8 + 심각도 번호이므로 `local3`(19)과 `info`(6)는 19 × 8 + 6 = 158 입니다. 아래 「RFC 형식 지정과 원격 UDP 전송」 의 출력 `<158>1 …` 이 이 값입니다.

```bash
# 아래 셋은 Debian 12 기본 규칙 줄에서 그대로 가져온 선택자다 (기본 분배 규칙 확인)
# *.*;auth,authpriv.none   모든 시설의 모든 심각도에서 auth·authpriv 만 뺀다 → /var/log/syslog
# auth,authpriv.*          두 시설의 모든 심각도 → /var/log/auth.log
# kern.*                   커널 시설 → /var/log/kern.log
```

다른 기계로 보내는 규칙은 동작 자리에 `@호스트`(UDP, 포트 기본 514) 또는 `@@호스트`(TCP)를 씁니다. 예를 들면 `*.* @loghost.example` 입니다. UDP 는 전송 중 줄이 사라질 수 있습니다.[^forward]



## 종료 코드

> 성공이면 0, 실패면 1 을 돌려주며 매뉴얼은 0 이 아닌 실패 코드로 명시합니다.[^exit]

아래 값은 모두 실측값이며 정상 실행과 잘못된 시설 이름, 닫힌 포트 연결 실패로 확인했습니다.

```bash
# 0  성공
# 1  실패 (알 수 없는 시설 이름, 원격 서버 포트 연결 실패 등)

# 옵션 뜻
#   logger -p   메시지 시설과 심각도 지정 (--priority)
#   logger -n   원격 syslog 서버 주소 지정 (--server)
#   logger -P   원격 syslog 서버 포트 지정 (--port)
#   logger -T   TCP 스트림 소켓 사용 (--tcp)
logger "ok"; echo $?
# 0

logger -p foo.info "bad facility"; echo $?
# logger: unknown facility name: foo / 1

logger \
  -n 127.0.0.1 \
  -P 1 \
  -T "no listener"; echo $?
# logger: failed to connect to 127.0.0.1 port 1 / 1
```

`/` 앞은 오류 출력이고 뒤는 `echo $?` 가 읽은 종료 코드입니다. `rsyslogd -N1` 역시 설정이 올바르면 0, 문법 오류가 있으면 1 을 돌려줍니다.[^exit]



## 유스케이스

> 예제는 앞 예제가 만든 설정을 이어 쓰므로 위에서 아래로 차례대로 실행합니다.

### 실습 준비

> 실습을 시작하기 전에 rsyslog 서비스가 정상 동작 중인지 확인합니다.

```bash
# rsyslog 서비스 활성 상태 확인 (한 줄 메시지 기록과 확인부터 여러 곳)
systemctl is-active rsyslog
# active
```

### 한 줄 메시지 기록과 확인

> `logger` 로 일반 텍스트를 남기면 기본 로그 파일과 시스템 저널에 각각 기록됩니다.

```bash
# 기본 메시지를 보낸다
logger "plain test"
sleep 2

# 기본 로그 파일의 마지막 줄을 확인한다
grep 'plain test' /var/log/syslog | tail -1
# 2026-11-15T21:50:34.585151+09:00 lmlcmd-deb root: plain test

# 저널에 남은 최근 3줄을 ISO 형식으로 확인한다
#   journalctl -n          보일 줄 수 (--lines)
#   journalctl -o          출력 모드 (--output)
#   journalctl --no-pager  페이저를 쓰지 않고 출력
journalctl \
  -n 3 \
  -o short-iso \
  --no-pager
```

```bash
2026-11-15T21:50:08+0900 lmlcmd-deb systemd[1]: Started rsyslog.service - System Logging Service.
2026-11-15T21:50:10+0900 lmlcmd-deb systemd-rc-local-generator[431]: /etc/rc.d/rc.local is not marked executable, skipping.
2026-11-15T21:50:34+0900 lmlcmd-deb root[2494]: plain test
```

Rocky Linux 9 에서는 기본 로그가 `/var/log/messages` 에 남습니다. 시각은 UTC 기준 전통 BSD 형식(`Nov 15 12:50:46 lmlcmd-rocky root[544]: plain test`)으로 찍힙니다.

### 시설과 심각도 지정

> `-p` 로 시설과 심각도를 지정할 수 있고, 지정하지 않으면 기본값인 `user.notice` 가 들어갑니다.[^facility]

```bash
# -p 로 local3.info 를 지정해 보내고, 옵션 없이 기본값으로도 보낸다
#   logger -t   줄마다 붙일 태그 식별자 지정 (--tag)
logger -p local3.info -t demo "routing test"
logger -t demo "default test"
sleep 1

# 저널에서 demo 태그가 붙은 최근 2줄의 시설과 심각도 필드를 JSON 으로 확인한다
#   journalctl -t   syslog 식별자 지정 (--identifier)
#   grep -o         일치하는 부분만 출력 (--only-matching)
journalctl \
  -t demo \
  -n 2 \
  -o json \
  --no-pager \
  | grep -oE '"(SYSLOG_FACILITY|PRIORITY|SYSLOG_IDENTIFIER|MESSAGE)":"[^"]*"'
```

```bash
"SYSLOG_IDENTIFIER":"demo"
"SYSLOG_FACILITY":"19"
"PRIORITY":"6"
"MESSAGE":"routing test"
"SYSLOG_FACILITY":"1"
"SYSLOG_IDENTIFIER":"demo"
"PRIORITY":"5"
"MESSAGE":"default test"
```

Rocky Linux 9 에서도 `local3.info` 는 시설 19·심각도 6 이고 기본값은 시설 1·심각도 5 로 필드 값이 같습니다.

### RFC 형식 지정과 원격 UDP 전송

> `--rfc5424` 와 `--rfc3164` 로 프로토콜 형식을 선택하고 원격 UDP 소켓으로 전송합니다.[^rfc]

```bash
# RFC 5424 규격 헤더를 붙여 표준 오류로 함께 출력한다
#   logger --rfc5424   RFC 5424 syslog 프로토콜 형식 사용
#   logger -s          표준 오류에도 메시지 출력 (--stderr)
logger \
  --rfc5424 \
  -s \
  -p local3.info \
  -t demo \
  "rfc test"
# <158>1 2026-11-15T21:50:37.639576+09:00 lmlcmd-deb demo - - [timeQuality tzKnown="1" isSynced="0"] rfc test

# RFC 3164 BSD syslog 형식으로 표준 오류에 함께 출력한다
#   logger --rfc3164   RFC 3164 BSD syslog 프로토콜 형식 사용
logger \
  --rfc3164 \
  -s \
  -p local3.info \
  -t demo \
  "rfc3164 test"
# <158>Nov 15 21:50:37 lmlcmd-deb demo: rfc3164 test

# 백그라운드에서 5514번 포트 UDP 패킷을 대기하고 logger 로 전송해 확인한다
#   logger -d   UDP 데이터그램 소켓 사용 (--udp)
#   nc -u       UDP 모드
#   nc -l       포트 수신 대기
#   timeout     정해진 초 뒤 프로세스 종료
(timeout 4 nc -u -l 127.0.0.1 5514 > /tmp/wire5424.txt &)
sleep 1
logger \
  --rfc5424 \
  -n 127.0.0.1 \
  -P 5514 \
  -d \
  -p local3.info \
  -t demo \
  "wire test"
sleep 2
cat /tmp/wire5424.txt
# <158>1 2026-11-15T21:50:38.657848+09:00 lmlcmd-deb demo - - [timeQuality tzKnown="1" isSynced="0"] wire test

# RFC 3164 형식의 패킷도 동일하게 5514번 포트로 수신해 확인한다
(timeout 4 nc -u -l 127.0.0.1 5514 > /tmp/wire3164.txt &)
sleep 1
logger \
  --rfc3164 \
  -n 127.0.0.1 \
  -P 5514 \
  -d \
  -p local3.info \
  -t demo \
  "wire test"
sleep 2
cat /tmp/wire3164.txt
# <158>Nov 15 21:50:41 lmlcmd-deb demo: wire test
```

Rocky Linux 9 에서도 동일하게 `<158>1` 및 `<158>Nov 15` 접두사로 시작하는 패킷이 전달됩니다.

### 분배 규칙 추가와 설정 검증

> `/etc/rsyslog.d/` 에 분배 규칙을 작성하고 `rsyslogd -N1` 로 검증한 뒤 데몬을 재시작합니다.[^rsyslog-n]

```bash
# local3 의 모든 로그를 local3.log 로 보내는 분배 규칙을 작성한다
echo "local3.*    /var/log/local3.log" > /etc/rsyslog.d/50-local3.conf
cat /etc/rsyslog.d/50-local3.conf
# local3.*    /var/log/local3.log

# rsyslogd 설정 문법을 검증한다
#   rsyslogd -N1   설정 검증 모드 실행 (레벨 1은 검증만 수행)
rsyslogd -N1
```

```bash
rsyslogd: version 8.2302.0, config validation run (level 1), master config /etc/rsyslog.conf
rsyslogd: End of config validation run. Bye.
```

```bash
# rsyslog 서비스를 재시작해 새 규칙을 적용하고 상태를 확인한다
systemctl restart rsyslog
sleep 1
systemctl is-active rsyslog
# active

# local3.info 로 메시지를 보낸 뒤 local3.log 에 기록되었는지 확인한다
logger -p local3.info -t demo "routing test"
sleep 2
cat /var/log/local3.log
# 2026-11-15T21:50:44.736745+09:00 lmlcmd-deb demo: routing test
```

Rocky Linux 9 의 `local3.log` 는 전통 BSD 형식으로 기록됩니다. 출력 줄에 PID 가 포함됩니다(`Nov 15 21:50:57 lmlcmd-rocky demo[581]: routing test`).

같은 줄이 `syslog` 에도 남는지 이어서 확인합니다. 아래 출력은 `debian:12` 컨테이너(rsyslogd 를 systemd 없이 직접 띄운 환경)에서 받아 시각이 UTC 입니다.

```bash
# local3.info 한 줄을 보내고 local3.log 와 syslog 에서 각각 찾는다
logger -p local3.info -t lab0801 "routing test"
sleep 2
grep lab0801 /var/log/local3.log
grep lab0801 /var/log/syslog
```

```bash
2026-11-16T00:58:27.652364+00:00 lmlcmd-deb lab0801: routing test
2026-11-16T00:58:27.652364+00:00 lmlcmd-deb lab0801: routing test
```

같은 줄이 `local3.log` 와 `syslog` 둘 다에 남았습니다. 첫 규칙 `*.*;auth,authpriv.none` 이 `local3` 을 빼지 않기 때문입니다.

### 설정 문법 오류 검출

> 잘못된 액션 문법이 포함되면 `rsyslogd -N1` 이 오류 위치와 공식 안내 링크를 출력하고 종료 코드 1 을 냅니다.[^rsyslog-n]

```bash
# 지원하지 않는 omfoo 액션을 추가해 오류 규칙을 만든다
echo "local3.* :omfoo:" >> /etc/rsyslog.d/50-local3.conf
cat /etc/rsyslog.d/50-local3.conf
```

```bash
local3.*    /var/log/local3.log
local3.* :omfoo:
```

```bash
# 설정 검증으로 문법 오류를 감지한다
rsyslogd -N1
```

```bash
rsyslogd: version 8.2302.0, config validation run (level 1), master config /etc/rsyslog.conf
rsyslogd: error during parsing file /etc/rsyslog.d/50-local3.conf, on or before line 2: errors occurred in file '/etc/rsyslog.d/50-local3.conf' around line 2 [v8.2302.0 try https://www.rsyslog.com/e/2207 ]
```

```bash
# 정상 규칙으로 덮어쓰고 다시 검증해 오류가 사라졌는지 확인한다
echo "local3.*    /var/log/local3.log" > /etc/rsyslog.d/50-local3.conf
rsyslogd -N1
```

```bash
rsyslogd: version 8.2302.0, config validation run (level 1), master config /etc/rsyslog.conf
rsyslogd: End of config validation run. Bye.
```

Rocky Linux 9 에서도 동일하게 2행 오류 안내와 함께 오류 코드 URL 이 출력됩니다.

### 기본 분배 규칙 확인

> `/etc/rsyslog.conf` 에서 주석과 빈 줄을 제외하면 배포판의 기본 로그 수집 및 분배 설정을 읽을 수 있습니다.

```bash
# 주석과 빈 줄을 제외한 기본 설정을 출력한다
#   grep -v   일치하지 않는 줄 선택 (--invert-match)
#   grep -E   확장 정규식 사용 (--extended-regexp)
grep -vE "^\s*(#|$)" /etc/rsyslog.conf
```

```bash
module(load="imuxsock") # provides support for local system logging
module(load="imklog")   # provides kernel logging support
$FileOwner root
$FileGroup adm
$FileCreateMode 0640
$DirCreateMode 0755
$Umask 0022
$WorkDirectory /var/spool/rsyslog
$IncludeConfig /etc/rsyslog.d/*.conf
*.*;auth,authpriv.none		-/var/log/syslog
auth,authpriv.*			/var/log/auth.log
cron.*				-/var/log/cron.log
kern.*				-/var/log/kern.log
mail.*				-/var/log/mail.log
user.*				-/var/log/user.log
*.emerg				:omusrmsg:*
```

Rocky Linux 9 에서는 RainerScript 액션 블록(`action(...)`)을 씁니다. 기본 로그는 `/var/log/messages` 에 남깁니다.

```bash
# Rocky Linux 9 의 기본 설정을 같은 명령으로 확인한다
grep -vE "^\s*(#|$)" /etc/rsyslog.conf
```

```bash
global(workDirectory="/var/lib/rsyslog")
module(load="builtin:omfile" Template="RSYSLOG_TraditionalFileFormat")
module(load="imuxsock"    # provides support for local system logging (e.g. via logger command)
       SysSock.Use="off") # Turn off message reception via local log socket; 
module(load="imjournal"             # provides access to the systemd journal
       UsePid="system" # PID nummber is retrieved as the ID of the process the journal entry originates from
       FileCreateMode="0644" # Set the access permissions for the state file
       StateFile="imjournal.state") # File to store the position in the journal
include(file="/etc/rsyslog.d/*.conf" mode="optional")
*.info;mail.none;authpriv.none;cron.none action(type="omfile" file="/var/log/messages")
authpriv.* action(type="omfile" file="/var/log/secure")
mail.* action(type="omfile" file="/var/log/maillog" sync="on")
cron.* action(type="omfile" file="/var/log/cron")
*.emerg action(type="omusrmsg" users="*")
uucp,news.crit action(type="omfile" file="/var/log/spooler")
local7.* action(type="omfile" file="/var/log/boot.log")
```

이 출력은 `rockylinux:9` 컨테이너 이미지(`/etc/rocky-release` 는 9.3, rsyslog 8.2510.0)에서 다시 받았습니다. 첫 규칙은 `info` 이상 전부를 받되 `mail`·`authpriv`·`cron` 을 뺍니다. `kern` 을 따로 거르는 규칙은 이 출력에 없습니다. `imjournal` 모듈을 적재하고 `imuxsock` 은 `SysSock.Use="off"` 라서, Rocky 는 로컬 소켓이 아니라 저널을 직접 읽습니다.

### 저널 연동 소켓 경로 확인

> Debian 12 의 rsyslog 는 systemd 저널 소켓을 넘겨받아 로컬 시스템 로그를 수집합니다.[^journald-path]

```bash
# imuxsock 모듈이 journald 소켓을 획득한 로그를 확인한다
#   journalctl -u   유닛 이름으로 조회 (--unit)
#   journalctl -b   부팅 번호 지정 (--boot)
#   grep -i         대소문자 무시 (--ignore-case)
journalctl \
  -u rsyslog \
  -b \
  --no-pager \
  | grep -i imuxsock
```

```bash
Nov 15 21:50:08 lmlcmd-deb rsyslogd[2452]: imuxsock: Acquired UNIX socket '/run/systemd/journal/syslog' (fd 3) from systemd.  [v8.2302.0]
Nov 15 21:50:43 lmlcmd-deb rsyslogd[2525]: imuxsock: Acquired UNIX socket '/run/systemd/journal/syslog' (fd 3) from systemd.  [v8.2302.0]
```

Rocky Linux 9 에서는 소켓 전달 대신 `imjournal` 모듈로 저널 파일을 직접 읽으며 위치를 `imjournal.state` 에 기록합니다.

```bash
# Rocky Linux 9 의 imjournal 설정 위치 확인
#   grep -n   줄 번호 함께 출력 (--line-number)
grep -n imjournal /etc/rsyslog.conf
```

```bash
19:                          # local messages are retrieved through imjournal now.
20:module(load="imjournal"             # provides access to the systemd journal
23:       StateFile="imjournal.state") # File to store the position in the journal
```

### 지금 쓰는 명령과 옛 명령

> 같은 일을 하는 옛 명령과 지금 명령을 짝으로 놓고, 세 머신에서 읽기만 하는 명령으로 어느 쪽이 남아 있는지 확인합니다.[^now-old]

먼저 설정 문법입니다. 아래 명령은 `$` 로 시작하는 옛 문법 줄을 셉니다.

```bash
# rsyslog.conf 에서 $ 로 시작하는 옛 문법 줄의 수를 센다
#   grep -c   일치한 줄 수를 센다 (--count)
grep -cE '^\s*\$' /etc/rsyslog.conf
# Debian 12 는 7, Ubuntu 24.04 는 10, Rocky 9.8 은 0
```

공식 문서는 옛 형식을 `obsolete legacy` 라 부르고 새 설정에는 쓰지 말라고 합니다.[^legacy-syntax] `module()`·`action()` 이 속한 RainerScript 형식은 `advanced` 라 부릅니다. 아래 두 설정은 `debian:12` 컨테이너(rsyslog 8.2302.0)의 `rsyslogd -N1` 검증을 둘 다 통과했습니다.

```bash
# 옛 문법: 모듈 적재, 파일 소유자와 그룹을 $ 지시어 한 줄씩으로 적는다
$ModLoad imudp
$UDPServerRun 514
$FileOwner root
$FileGroup adm
local3.*    /var/log/local3.log

# 새 문법: 같은 설정을 module(), input(), action() 으로 적는다
module(load="imudp")
input(type="imudp" port="514")
module(load="builtin:omfile" fileOwner="root" fileGroup="adm")
local3.* action(type="omfile" file="/var/log/local3.log")
```

다음은 서비스를 다루는 명령입니다. 세 머신 모두 `/etc/init.d/rsyslog` 가 없어서 `service` 는 `systemctl` 을 대신 부릅니다.[^service-systemctl] `restart` 두 줄은 서비스를 다시 띄우므로 돌리지 않았고, 읽기만 하는 `status` 로 확인했습니다.

```bash
# 옛 init 스크립트 시절의 명령이다
service rsyslog restart

# 지금 쓰는 명령이다
systemctl restart rsyslog

# service 가 systemctl 로 넘기는지 status 첫 줄로 확인한다
service rsyslog status 2>&1 | head -1
# Rocky 9.8: Redirecting to /bin/systemctl status rsyslog.service
# Debian 12·Ubuntu 24.04: ● rsyslog.service - System Logging Service
```

로그를 따라 읽는 명령도 짝이 있습니다. 옛 방식은 텍스트 파일을, 지금 방식은 저널을 따라 읽으며, 아래 두 명령은 끝나지 않아서 같은 조회를 `-n 2` 로 바꿔 돌렸습니다.[^follow]

```bash
# 옛 방식: 텍스트 로그 파일 끝을 따라 읽는다 (Debian·Ubuntu 는 /var/log/syslog, Rocky 는 /var/log/messages)
#   tail -f   파일에 줄이 추가되면 이어서 보여 준다 (--follow)
tail -f /var/log/messages

# 지금 방식: 저널 전체를 따라 읽고, -u 로 유닛 하나만 좁힌다
#   journalctl -f   새 줄이 저널에 붙으면 이어서 보여 준다 (--follow)
journalctl -f
journalctl -f -u rsyslog

# 끝나는 꼴로 바꿔 rsyslog 유닛의 마지막 두 줄을 본다
journalctl \
  -u rsyslog \
  -n 2 \
  -o short-iso \
  --no-pager
```

```bash
2026-11-16T09:50:56+0900 lml-deb rsyslogd[2454]: [origin software="rsyslogd" swVersion="8.2302.0" x-pid="2454" x-info="https://www.rsyslog.com"] start
2026-11-16T09:50:56+0900 lml-deb systemd[1]: Started rsyslog.service - System Logging Service.
```

마지막은 설정을 읽는 방법입니다. 파일 하나만 `cat` 으로 보면 drop-in 이 덮은 값을 놓칩니다. 합친 결과는 `systemd-analyze cat-config` 로 봅니다.[^cat-config]

```bash
# 본 파일과 drop-in 을 합친 journald 설정에서 파일 머리와 ForwardToSyslog 줄만 본다
systemd-analyze cat-config systemd/journald.conf \
  | grep -nE 'ForwardToSyslog|^# /.*\.conf$'
```

```bash
# Debian 12 (본 파일 하나)
1:# /etc/systemd/journald.conf
36:#ForwardToSyslog=yes

# Rocky 9.8 (본 파일 하나)
1:# /etc/systemd/journald.conf
36:#ForwardToSyslog=no

# Ubuntu 24.04 (본 파일과 drop-in 하나)
1:# /etc/systemd/journald.conf
38:#ForwardToSyslog=no
52:# /usr/lib/systemd/journald.conf.d/syslog.conf
57:ForwardToSyslog=yes
```

Ubuntu 는 본 파일의 주석 처리된 `no` 를 drop-in 이 `yes` 로 덮어서 실제로는 rsyslog 로 넘깁니다. 본 파일만 읽었다면 반대로 판단했을 것입니다.

### 실습 정리

> 실습에서 생성한 분배 규칙과 로그 파일을 지우고 서비스를 원래 상태로 되돌립니다.

```bash
# 실습에서 추가한 파일들을 삭제하고 rsyslog 를 재시작한다
rm -f /etc/rsyslog.d/50-local3.conf /var/log/local3.log /tmp/wire*.txt
systemctl restart rsyslog
```

이 정리 명령의 실제 실행 결과는 실측 기록에 남기지 않았습니다.



## 관련 문서

> 이 시트와 이어지는 시트 및 책 노트입니다.

- [journalctl 참조 시트](./journalctl.md) — 저널 조회 옵션과 필드 필터링
- [logrotate 참조 시트](./logrotate.md) — 텍스트 로그 파일의 주기적 회전과 압축 관리
- [책 노트 8장 1절, 로그 한 줄은 저널과 파일로 갈라진다](../../../book/learning-modern-linux/08-01.재는%20것은%20바깥이고%20알고%20싶은%20것은%20안이다.md#2-로그-한-줄은-저널과-파일로-갈라진다) — journald 와 rsyslog 로 갈라지는 경로와 RFC 5424 구조



## 참고 자료

> 검증 환경과 공식 매뉴얼 및 각주 정의입니다.

- 검증 환경: Debian 12 (rsyslog 8.2302.0, logger 2.38.1), Rocky Linux 9.8 (rsyslog 8.2510.0, logger 2.37.4)
- 추가 환경: Ubuntu 24.04.5 (rsyslog 8.2312.0), 「지금 쓰는 명령과 옛 명령」 절에서만 씁니다
- 검증 일자: 2026-11-15 OrbStack VM 실측, 「지금 쓰는 명령과 옛 명령」 절은 2026-11-16 머신 lml-deb·lml-rocky·lml-ubuntu 에서 다시 받음
- [logger(1)](https://man7.org/linux/man-pages/man1/logger.1.html) — man7.org util-linux 최신 매뉴얼
- [rsyslog.conf(5)](https://man7.org/linux/man-pages/man5/rsyslog.conf.5.html) — man7.org rsyslog 설정 파일 매뉴얼
- [rsyslogd(8)](https://man7.org/linux/man-pages/man8/rsyslogd.8.html) — man7.org rsyslog 데몬 매뉴얼
- [rsyslog 공식 문서](https://www.rsyslog.com/doc/configuration/index.html) — rsyslog configuration documentation
- [rsyslog Configuration Formats](https://www.rsyslog.com/doc/configuration/conf_formats.html) — 설정 형식 이름과 권고
- [systemd-analyze(1)](https://man7.org/linux/man-pages/man1/systemd-analyze.1.html) — man7.org `cat-config`
- [journald.conf(5)](https://man7.org/linux/man-pages/man5/journald.conf.5.html) — man7.org drop-in 우선순위
- [journalctl(1)](https://man7.org/linux/man-pages/man1/journalctl.1.html) — man7.org `--follow`

[^pkg]: util-linux logger(1) DESCRIPTION — "logger is a shell command interface to the syslog(3) system log module." rsyslogd(8) DESCRIPTION — "rsyslogd is a system utility providing support for message logging."
[^env]: Debian 12(bookworm, rsyslog 8.2302.0, logger util-linux 2.38.1) 및 Rocky Linux 9.8(Blue Onyx, rsyslog 8.2510.0, logger util-linux 2.37.4) OrbStack VM 환경에서 실측했습니다.
[^facility]: logger(1) `-p, --priority priority` — "Enter the message into the log with the specified priority. The priority may be specified numerically or as a facility.level pair. The default is user.notice." syslog(3) — "LOG_USER random user-level messages", "LOG_LOCAL3 reserved for local use".
[^exit]: logger(1) EXIT STATUS — "The logger utility exits 0 on success, and >0 if an error occurs." rsyslogd(8) EXIT STATUS — "rsyslogd exits 0 on success and non-zero on error."
[^rfc]: logger(1) `--rfc5424` — "Use the RFC 5424 syslog protocol." `--rfc3164` — "Use the RFC 3164 BSD syslog protocol." RFC 5424 "The Syslog Protocol", RFC 3164 "The BSD Syslog Protocol".
[^selector]: rsyslog.conf(5) — "An asterisk ('*') stands for all facilities or all priorities, depending on where it is used (before or after the period). The keyword none stands for no priority of the given facility." 심각도는 "all messages of the specified priority and higher are logged according to the given action". https://man7.org/linux/man-pages/man5/rsyslog.conf.5.html
[^forward]: rsyslog.conf(5) — "To forward messages to another host via UDP, prepend the hostname with the at sign ("@"). To forward it via plain tcp, prepend two at signs ("@@")." "the destination port defaults to 514." "Due to the nature of UDP, you will probably lose some messages in transit." https://man7.org/linux/man-pages/man5/rsyslog.conf.5.html
[^rsyslog-n]: rsyslogd(8) `-N level` — "Do a config check. Do NOT run in normal mode, just verify the configuration file only. The level parameter modifies the behavior: 1 - verify only, 2 - verify and dump config, 3 - verify and print lots of debug info."
[^journald-path]: journald.conf(5) ForwardToSyslog — "ForwardToSyslog= controls whether log messages received by the journal daemon shall be forwarded to a traditional syslog daemon." Debian 은 `imuxsock` 이 `/run/systemd/journal/syslog` 소켓을 획득하고, Rocky Linux 는 `imjournal` 모듈이 저널 파일을 직접 읽습니다.
[^now-old]: 2026-11-16 머신 lml-deb(Debian 12, rsyslog 8.2302.0-1+deb12u2)·lml-rocky(Rocky 9.8, rsyslog 8.2510.0-2.el9_8.2)·lml-ubuntu(Ubuntu 24.04.5, rsyslog 8.2312.0-3ubuntu9.4)에서 읽기만 하는 명령으로 받았습니다. 설정 문법 두 블록의 `rsyslogd -N1` 검증은 머신이 아닌 `debian:12` 컨테이너에서 했습니다.
[^legacy-syntax]: rsyslog Configuration Formats — "basic - previously known as the sysklogd format." "advanced - previously known as the RainerScript format. The recommended format when you author rsyslog logic directly." "obsolete legacy - previously known as the legacy format. This format is obsolete and must not be used in new configurations." "Use advanced for new configurations, or the YAML format when rsyslog lives inside a YAML-centric workflow. The basic format is acceptable for simple, existing configurations. Never use obsolete legacy." 같은 문서의 「Legacy Configuration Directives」 목록에 `$ModLoad` 와 `$FileOwner` 가 있습니다. https://www.rsyslog.com/doc/configuration/conf_formats.html (이 주소는 docs.rsyslog.com 으로 넘어가며 최신판 문서입니다.)
[^service-systemctl]: 실측: 세 머신 모두 `ls /etc/init.d/rsyslog` 가 「No such file or directory」 입니다. Debian·Ubuntu 의 `/usr/sbin/service` 167줄은 `exec systemctl $sctl_args ${ACTION} ${UNIT}` 이고, Rocky 는 `service rsyslog status` 가 「Redirecting to /bin/systemctl status rsyslog.service」 를 찍습니다.
[^follow]: journalctl(1) `-f, --follow` — "Show only the most recent journal entries, and continuously print new entries as they are appended to the journal, until Ctrl-C is hit (or the tool is otherwise terminated)." https://man7.org/linux/man-pages/man1/journalctl.1.html
[^cat-config]: systemd-analyze(1) `cat-config` — "This command is similar to systemctl cat, but operates on config files. It will copy the contents of a config file and any drop-ins to standard output, using the usual systemd set of directories and rules for precedence." journald.conf(5) — "In addition to the main configuration file, drop-in configuration snippets are read from /usr/lib/systemd/*.conf.d/, /usr/local/lib/systemd/*.conf.d/, and /etc/systemd/*.conf.d/. Those drop-ins have higher precedence and override the main configuration file." 같은 문서는 "The vendor version of the file contains commented out entries showing the defaults as a guide to the administrator." 라고 적습니다. https://man7.org/linux/man-pages/man5/journald.conf.5.html
