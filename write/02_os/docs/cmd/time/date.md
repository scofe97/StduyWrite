---
title: date 참조 시트
tags: [linux, cheatsheet, date, unix-epoch, y2038, openssl, cli, reference]
status: draft
source:
  - GNU coreutils date (`--help` 원문, coreutils 9.1) · date(1)
  - 《Learning Modern Linux》 3장 "Shells and Scripting"(Michael Hausenblas, O'Reilly, 2022)의 `date` 예
related:
  - ../README.md
updated: 2026-11-11
---

# date 참조 시트

---

> 날짜를 에포크 초라는 숫자로 바꾸고, 원하는 형식으로 찍고, 며칠 남았는지 계산하는 `date` 사용법을 따라 치면 그대로 나오는 예제로 모았습니다.

## 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 파일이 모두 생깁니다.

macOS 기본 `date` 는 BSD 판이라 `-d` 가 없고 `-r` 에 숫자를 주면 에포크 초로 읽습니다. OrbStack 의 Linux VM 이나 `docker run -it --rm debian:12` 안에서 실행합니다. Debian 컨테이너에는 `openssl` 이 없어서 3절의 인증서 예 전에 설치합니다.

```bash
mkdir -p ~/cmd-lab/date && cd ~/cmd-lab/date
touch -d "2026-11-01 12:00:00" old.txt
# 3절 인증서 예에만 필요하다. 컨테이너는 root 라 sudo 없이 친다
apt-get update -qq && apt-get install -y -qq openssl
```

`old.txt` 는 수정 시각을 2026-11-01 12:00:00 으로 맞춘 빈 파일입니다. 컨테이너의 시간대는 UTC 입니다. 시간대가 다른 VM 에서 `-u` 없이 치면 시각이 그만큼 달라집니다.



## 1. 지금 시각과 에포크 초

> 날짜끼리 빼거나 견주려면 사람이 읽는 날짜를 숫자 하나로 바꿔야 합니다. 그 숫자가 에포크 초입니다.

에포크 초는 1970-01-01 00:00:00 UTC 부터 흐른 초의 수입니다.[^date-help] `+%s` 로 지금 시각을 에포크 초로 찍고, `-d @숫자` 로 거꾸로 읽습니다. 아래 두 줄은 책에 실린 예입니다.

```bash
date +%s                                    # 1629582883 (책을 쓸 때 찍힌 값)
date -d @1629582883 '+%m/%d/%Y:%H:%M:%S'    # 08/21/2021:21:54:43
```

첫 줄은 실행한 시각마다 다른 값이 나오며 위 숫자는 책을 쓸 때 찍힌 값입니다. 둘째 줄은 UTC 컨테이너에서 같은 값이 나옵니다. 아래부터는 2026-11-10 09:00:00 UTC 를 기준 시각으로 씁니다.

```bash
# 지금 시각. 실행할 때마다 달라진다
date                                       # Wed Nov 11 07:17:57 UTC 2026

# -d (--date): 'now' 대신 주어진 날짜를 쓴다. -u (--utc): UTC 로 읽고 찍는다
date -u -d "2026-11-10 09:00:00" +%s       # 1794301200
date -u -d @1794301200                     # Tue Nov 10 09:00:00 UTC 2026

# 에포크 0
date -u -d @0                              # Thu Jan  1 00:00:00 UTC 1970

# TZ 환경 변수로 그 명령에만 시간대를 바꾼다
TZ=Asia/Seoul date -d @1794301200          # Tue Nov 10 18:00:00 KST 2026
```

같은 에포크 초가 UTC 로는 09시, 서울 시간으로는 18시입니다. 에포크 초는 시간대와 무관한 숫자이고 시간대는 찍을 때만 끼어듭니다.



## 2. 원하는 형식으로 찍기

> 로그의 타임스탬프, 백업 파일 이름, 다른 도구가 받는 형식은 저마다 다릅니다. `+` 뒤에 형식 문자열을 주면 그 꼴로 찍습니다.

```bash
date -u -d @1794301200 "+%Y-%m-%d %H:%M:%S"    # 2026-11-10 09:00:00

# %F 는 %Y-%m-%d, %T 는 %H:%M:%S 와 같다
date -u -d @1794301200 +%F                     # 2026-11-10
date -u -d @1794301200 +%T                     # 09:00:00

# %j 는 그해의 몇째 날, %A 는 요일 이름
date -u -d @1794301200 +%j                     # 314
date -u -d @1794301200 +%A                     # Tuesday

# 시간대가 붙은 표준 형식. -I (--iso-8601), -R (--rfc-email)
date -u -d @1794301200 --iso-8601=seconds      # 2026-11-10T09:00:00+00:00
date -u -d @1794301200 -R                      # Tue, 10 Nov 2026 09:00:00 +0000

# %Z 는 시간대 이름, %z 는 UTC 와의 차이
TZ=Asia/Seoul date -d @1794301200 "+%F %T %Z %z"    # 2026-11-10 18:00:00 KST +0900
```

### 파일 이름에 날짜 넣기

백업이나 덤프 파일 이름에 날짜를 넣으면 이름이 겹치지 않고 `ls` 로 정렬했을 때 시간순이 됩니다. 아래 두 줄은 실행한 날에 따라 값이 달라집니다.

```bash
echo backup-$(date +%Y%m%d).tar.gz    # backup-20261111.tar.gz

# 하루에 여러 번 만들면 시분초까지 넣는다
date +%F_%H%M%S                       # 2026-11-11_071758
```



## 3. 날짜 계산하기

> 30일 뒤가 며칠인지, 두 날짜 사이가 며칠인지 셀 때 `-d` 가 받는 상대 표현과 에포크 초 뺄셈을 씁니다.

### 상대 표현

`-d` 는 "next Thursday" 같은 사람이 쓰는 표현도 읽습니다.[^date-man] 날짜 뒤에 `+30 days`·`2 weeks ago` 를 붙이면 그만큼 옮긴 날짜가 나옵니다.

```bash
date -u -d "2026-11-10 +30 days" +%F       # 2026-12-10
date -u -d "2026-11-10 -1 day" +%F         # 2026-11-09
date -u -d "2026-11-10 2 weeks ago" +%F    # 2026-10-27

# 기준 날짜를 빼면 오늘부터 센다. 실행한 날에 따라 달라진다
date -d yesterday +%F                      # 2026-11-10
date -d tomorrow +%F                       # 2026-11-12
```

상대 표현에는 함정이 둘 있습니다. 시각 바로 뒤의 `+30` 은 날 수가 아니라 UTC 와의 시간 차(30시간)로 읽힙니다.[^date-input] 30시간 차이는 받지 않아 날짜 전체가 무효가 됩니다. `+3` 처럼 작은 수는 오류 없이 UTC+03 으로 읽히고 남은 `days` 가 하루로 더해져 틀린 시각이 나옵니다. 시간대를 먼저 적으면 풀립니다. 그리고 1월 31일에 한 달을 더하면 없는 날짜인 2월 31일이 넘쳐 3월로 갑니다.

```bash
date -u -d "2026-11-10 09:00:00 +30 days" "+%F %T"        # date: invalid date '2026-11-10 09:00:00 +30 days'
date -u -d "2026-11-10 09:00:00 +3 days" "+%F %T"         # 2026-11-11 06:00:00
date -u -d "2026-11-10 09:00:00 UTC +30 days" "+%F %T"    # 2026-12-10 09:00:00

date -u -d "2026-01-31 +1 month" +%F    # 2026-03-03
date -u -d "2026-02-30"                 # date: invalid date '2026-02-30'
```

### 두 날짜 사이의 날 수

두 날짜를 에포크 초로 바꿔 빼고 하루의 초 86,400 으로 나눕니다.

```bash
start=$(date -u -d "2026-11-10" +%s)
end=$(date -u -d "2026-12-25" +%s)
echo $(( (end - start) / 86400 ))    # 45
```

파일의 수정 시각은 `-r` 로 읽습니다. GNU `date -r 파일` 은 그 파일의 마지막 수정 시각을 찍습니다. macOS BSD `date -r` 도 파일 이름을 받지만 숫자를 주면 에포크 초로 읽어 그 날짜를 찍습니다.[^bsd-date]

```bash
date -u -r old.txt "+%F %T"    # 2026-11-01 12:00:00
```

### 인증서 만료까지 남은 날

인증서가 며칠 남았는지는 위 뺄셈을 그대로 씁니다. `openssl x509 -enddate` 로 뽑은 만료 시각을 `cut` 으로 떼어 에포크 초로 바꾼 뒤 현재 시각과의 차이를 86,400 으로 나눕니다.[^x509] 아래는 유효 기간 30일짜리 자체 서명 인증서를 만들어 돌린 결과입니다. 만료 시각은 실행한 시각에 따라 달라집니다.

```bash
# 실습용 자체 서명 인증서. 유효 기간 30일
openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 30 -subj "/CN=lab.example" 2>/dev/null

openssl x509 -enddate -noout -in cert.pem    # notAfter=Dec 11 07:18:10 2026 GMT
end=$(date -d "$(openssl x509 -enddate -noout -in cert.pem | cut -d= -f2)" +%s)
now=$(date +%s)
echo $(( (end - now) / 86400 ))              # 30
```

날 수가 아니라 "기한 안에 만료되는가" 만 알면 되면 `-checkend 초` 가 종료 상태로 답합니다. 만료되지 않으면 0, 만료되면 1입니다.

```bash
openssl x509 -checkend $((7*86400)) -noout -in cert.pem; echo $?     # Certificate will not expire / 0
openssl x509 -checkend $((40*86400)) -noout -in cert.pem; echo $?    # Certificate will expire / 1
```

위 블록의 `/` 는 두 줄로 나온 출력을 한 줄에 줄여 적은 것입니다.



## 4. 에포크 시간과 2038년

> 에포크 초를 부호 있는 32비트 정수에 담는 시스템은 2038년에 그 수가 넘칩니다.

에포크 시간은 모든 날을 정확히 86,400초로 칩니다. 부호 있는 32비트 정수의 최댓값은 2³¹−1 = 2,147,483,647 이고, 이 값을 날짜로 바꾸면 2038년 1월 19일 03:14:07 UTC 입니다. 그 1초 뒤를 32비트 `time_t` 로는 담을 수 없어 음수로 넘어갑니다. 이것이 2038년 문제입니다.

```bash
echo $(( 2**31 - 1 ))      # 2147483647
date -u -d @2147483647     # Tue Jan 19 03:14:07 UTC 2038

# 64비트 time_t 를 쓰는 지금의 리눅스는 그 다음 초도 찍는다
date -u -d @2147483648     # Tue Jan 19 03:14:08 UTC 2038
```

이 컨테이너의 `time_t` 가 64비트라서 마지막 줄이 정상으로 나왔습니다. 32비트 시스템이나 에포크 초를 32비트 칸에 저장하는 파일 형식·데이터베이스 칼럼은 여전히 이 경계를 넘지 못합니다.



## 관련 문서

- [cut 참조 시트](../text/cut.md) — 인증서 예에서 `notAfter=` 뒤를 자르는 법
- [head·tail 참조 시트](../text/head%C2%B7tail.md) — 날짜가 찍힌 로그의 앞뒤만 볼 때
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

- GNU coreutils 9.1 의 `date --help` 원문 — Debian 12 컨테이너에서 2026-11-11 출력
- [date(1)](https://man7.org/linux/man-pages/man1/date.1.html) — 2026-11-11 조회
- [GNU coreutils 매뉴얼](https://www.gnu.org/software/coreutils/manual/coreutils.html) — "date invocation"·"Date input formats"
- 원서: 《Learning Modern Linux》 3장 Shells and Scripting (Michael Hausenblas, O'Reilly, 2022년) — 1절의 `date +%s`·`date -d @…` 예

[^date-help]: `date --help` (GNU coreutils 9.1) — `%s` "seconds since the Epoch (1970-01-01 00:00 UTC)", `-d, --date=STRING` "display time described by STRING, not 'now'", `-r, --reference=FILE` "display the last modification time of FILE".
[^date-man]: `date(1)` 의 DATE STRING — "The --date=STRING is a mostly free format human readable date string such as … "next Thursday". A date string may contain items indicating calendar date, time of day, time zone, day of week, relative time, relative date, and numbers." <https://man7.org/linux/man-pages/man1/date.1.html>
[^date-input]: GNU coreutils 매뉴얼, "Time of day items" — "The time may alternatively be followed by a time zone correction, expressed as shhmm … The zone minutes term, mm, may be omitted, in which case the one- or two-digit correction is interpreted as a number of hours." `+24` 까지는 받고 `+25` 부터 무효가 되는 것과 `date --debug` 가 `+3` 을 `UTC+03` 으로 읽는 것은 이 시트의 실측입니다. <https://www.gnu.org/software/coreutils/manual/html_node/Time-of-day-items.html>
[^bsd-date]: FreeBSD `date(1)` — "-r seconds Print the date and time represented by seconds, where seconds is the number of seconds since the Unix Epoch", "-r filename Print the date and time of the last modification of filename." macOS 26.6 의 `man date` 도 같은 두 항목을 적습니다. <https://man.freebsd.org/cgi/man.cgi?query=date&sektion=1>
[^x509]: OpenSSL 3.0 `openssl-x509` 의 `-enddate`·`-checkend`. <https://docs.openssl.org/3.0/man1/openssl-x509/>
