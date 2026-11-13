---
title: date 참조 시트
tags: [linux, cheatsheet, date, unix-epoch, y2038, openssl, cli, reference]
status: draft
source:
  - GNU coreutils date (`--help` 원문, coreutils 9.1) · date(1)
  - 《Learning Modern Linux》 3장 "Shells and Scripting"(Michael Hausenblas, O'Reilly, 2022)의 `date` 예
related:
  - ../README.md
updated: 2026-11-13
---

# date 참조 시트

---

> 날짜를 에포크 초라는 숫자로 바꾸고, 원하는 형식으로 찍고, 며칠 남았는지 계산하는 `date` 사용법을 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `date` 는 시각을 찍고, 날짜 문자열을 읽고, 날짜를 계산합니다.

지금 시각이나 `-d` 로 준 날짜를 `+형식` 으로 찍거나 에포크 초로 바꾸고, 상대 표현으로 날짜를 옮깁니다. coreutils 의 외부 바이너리이며 이 시트는 GNU 판(coreutils 9.1, Debian 12 컨테이너)으로 실측했습니다. macOS 기본 `date` 는 BSD 판이라 `-d` 가 없고 `-r` 에 숫자를 주면 에포크 초로 읽습니다.[^bsd-date]



## 핵심 문법

> 옵션으로 "어느 시각인가" 를 정하고 `+형식` 으로 "어떻게 찍는가" 를 정합니다.

```bash
# 호출 형태. 둘째 줄은 시계를 맞추는 형태라 이 시트는 쓰지 않는다
date [OPTION]... [+FORMAT]
date [-u|--utc|--universal] [MMDDhhmm[[CC]YY][.ss]]

# 지금 시각을 에포크 초로 찍는다 (지금 시각과 에포크 초)
date +%s

# 문자열로 준 날짜를 읽는다 (지금 시각과 에포크 초)
date -d "날짜 문자열" +형식

# 에포크 초를 날짜로 되돌린다 (지금 시각과 에포크 초)
date -d @초

# 지금 시각을 형식대로 찍는다 (원하는 형식으로 찍기, 파일 이름에 날짜 넣기)
date +형식

# 날짜를 앞뒤로 옮긴다 (상대 표현으로 날짜 옮기기)
date -d "날짜 +30 days" +형식

# 파일의 수정 시각을 읽는다 (두 날짜 사이의 날 수)
date -r 파일 +형식

# 다른 명령이 찍은 날짜를 에포크 초로 바꾼다 (인증서 만료까지 남은 날)
date -d "$(다른 명령)" +%s
```

### 형식 지정자

> `+` 뒤의 형식 문자열에 쓰는 지정자입니다. 본문에 나온 것만 실었습니다.

뜻은 `date --help` 의 설명을 따랐습니다.[^date-help]

```bash
# "+..." 안에 쓴다. 가운데 열은 2026-11-10 09:00:00 UTC 를 찍은 값이다
# %s   1794301200   에포크 초(1970-01-01 00:00 UTC 부터 흐른 초)
# %F   2026-11-10   전체 날짜. %+4Y-%m-%d 와 같다
# %T   09:00:00     시각. %H:%M:%S 와 같다
# %Y   2026         연
# %m   11           월 (01..12)
# %d   10           일 (예: 01)
# %H   09           시 (00..23)
# %M   00           분 (00..59)
# %S   00           초 (00..60)
# %j   314          그해의 몇째 날 (001..366)
# %A   Tuesday      요일 전체 이름
# %Z   UTC          시간대 약어. TZ=Asia/Seoul 이면 KST
# %z   +0000        +hhmm 꼴의 UTC 와의 차이. TZ=Asia/Seoul 이면 +0900
```

### -d 가 받는 입력

> `-d` 는 사람이 쓰는 날짜 표현을 읽습니다. 본문에 나온 꼴만 모았습니다.

`-d` 의 입력 규칙은 매뉴얼의 "DATE STRING" 에 있습니다.[^date-man]

```bash
# @초                      에포크 초를 날짜로 읽는다
# "YYYY-MM-DD HH:MM:SS"    날짜와 시각. 「상대 표현으로 날짜 옮기기」 처럼 날짜만 줄 수도 있다
# +N days                  날짜 뒤에 붙여 N일 뒤로 옮긴다
# -N day                   N일 전으로 옮긴다
# N weeks ago              N주 전으로 옮긴다
# yesterday                오늘 기준 하루 전
# tomorrow                 오늘 기준 하루 뒤
# UTC, +hhmm               시각 바로 뒤에 붙는 시간대 표기. 「시각 뒤 +30 과 월말 넘침」 참고
```



## 종료 코드

> `date` 는 성공하면 0, 실패하면 1 을 돌려줍니다.

매뉴얼은 `date` 절에 성공은 0, 실패는 0 이 아닌 값이라고만 적고 실패 코드를 나누지 않습니다.[^date-exit] 아래는 Debian 12 컨테이너에서 실패 세 가지를 돌린 결과입니다.

```bash
# 0  성공. 날짜를 읽어 찍었을 때. --help·--version 도 0 이다
# 1  실패. 무효한 날짜(date: invalid date), 모르는 옵션, 없는 -r 파일을 줬을 때
# openssl x509 -checkend 의 0 (만료 안 됨)·1 (만료됨) 은 date 가 아니라 openssl 의 코드다. 「인증서 만료까지 남은 날」 참고

# 무효한 날짜
date -d "2026-02-30"; echo $?    # date: invalid date '2026-02-30' / 1

# 모르는 옵션
date --badopt; echo $?           # date: unrecognized option '--badopt' / Try 'date --help' for more information. / 1

# 없는 파일을 -r 에 준 경우
date -r /nonexistent; echo $?    # date: /nonexistent: No such file or directory / 1
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다. 스크립트에서는 `if date -d "$s" >/dev/null 2>&1; then …` 처럼 종료 코드로 날짜 문자열이 맞는지 가립니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션만 씁니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 파일이 모두 생깁니다.

OrbStack 의 Linux VM 이나 `docker run -it --rm debian:12` 안에서 실행합니다. Debian 컨테이너에는 `openssl` 이 없어 마지막 줄이 설치합니다.

```bash
mkdir -p ~/cmd-lab/date && cd ~/cmd-lab/date
touch -d "2026-11-01 12:00:00" old.txt
# 「인증서 만료까지 남은 날」 에만 필요하다. 컨테이너는 root 라 sudo 없이 친다
apt-get update -qq && apt-get install -y -qq openssl
```

`old.txt` 는 수정 시각을 2026-11-01 12:00:00 으로 맞춘 빈 파일입니다. 컨테이너의 시간대는 UTC 이며, 시간대가 다른 VM 에서 `-u` 없이 치면 시각이 그만큼 달라집니다.

### 지금 시각과 에포크 초

> 날짜끼리 빼거나 견주려면 사람이 읽는 날짜를 숫자 하나로 바꿔야 합니다. 그 숫자가 에포크 초입니다.

`+%s` 는 1970-01-01 00:00:00 UTC 부터 흐른 초의 수를 찍고, `-d @숫자` 는 그 수를 날짜로 거꾸로 읽습니다.[^date-help] 첫 블록의 두 줄은 책에 실린 예입니다.

```bash
# 첫 줄의 값은 실행한 시각마다 다르며 아래 숫자는 책을 쓸 때 찍힌 값이다. 둘째 줄은 UTC 컨테이너에서 같은 값이 나온다
#   +형식       찍을 형식. +%s 는 에포크 초
#   -d STRING   now 대신 주어진 날짜를 쓴다 (--date)
date +%s                                    # 1629582883 (책을 쓸 때 찍힌 값)
date -d @1629582883 '+%m/%d/%Y:%H:%M:%S'    # 08/21/2021:21:54:43
```

```bash
# 지금 시각. 실행할 때마다 달라진다
date                                       # Wed Nov 11 07:17:57 UTC 2026

# 아래부터 2026-11-10 09:00:00 UTC 를 기준 시각으로 쓴다. 본문의 예는 대개 -u 와 함께 쓴다
#   -u   UTC 로 읽고 찍는다 (--utc, --universal). 빼면 실행한 곳의 시간대만큼 시각이 달라진다
date -u -d "2026-11-10 09:00:00" +%s       # 1794301200
date -u -d @1794301200                     # Tue Nov 10 09:00:00 UTC 2026

# 에포크 0
date -u -d @0                              # Thu Jan  1 00:00:00 UTC 1970

# TZ 환경 변수로 그 명령에만 시간대를 바꾼다
TZ=Asia/Seoul date -d @1794301200          # Tue Nov 10 18:00:00 KST 2026
```

같은 에포크 초가 UTC 로는 09시, 서울 시간으로는 18시입니다. 에포크 초는 시간대와 무관한 숫자이고 시간대는 찍을 때만 끼어듭니다.

### 원하는 형식으로 찍기

> 로그의 타임스탬프, 백업 파일 이름, 다른 도구가 받는 형식은 저마다 다릅니다. `+` 뒤에 형식 문자열을 주면 그 꼴로 찍습니다.

한 기준 시각을 지정자만 바꿔 여러 꼴로 찍습니다. 지정자의 뜻은 「형식 지정자」 에 있습니다.

```bash
date -u -d @1794301200 "+%Y-%m-%d %H:%M:%S"    # 2026-11-10 09:00:00

# %F 는 %Y-%m-%d, %T 는 %H:%M:%S 와 같다
date -u -d @1794301200 +%F                     # 2026-11-10
date -u -d @1794301200 +%T                     # 09:00:00

# %j 는 그해의 몇째 날, %A 는 요일 이름
date -u -d @1794301200 +%j                     # 314
date -u -d @1794301200 +%A                     # Tuesday

# 시간대가 붙은 표준 형식으로 찍는다. 먼저 ISO 8601 이다
#   -I[FMT]   ISO 8601 형식으로 찍는다 (--iso-8601[=FMT]). FMT 는 date(기본)·hours·minutes·seconds·ns. 본문은 seconds 를 쓴다
date \
  -u \
  -d @1794301200 \
  --iso-8601=seconds
# 2026-11-10T09:00:00+00:00

# 같은 시각을 다른 표준 형식으로 찍는다
#   -R        RFC 5322 형식으로 찍는다 (--rfc-email)
date \
  -u \
  -d @1794301200 \
  -R
# Tue, 10 Nov 2026 09:00:00 +0000

# %Z 는 시간대 이름, %z 는 UTC 와의 차이
TZ=Asia/Seoul date -d @1794301200 "+%F %T %Z %z"    # 2026-11-10 18:00:00 KST +0900
```

### 파일 이름에 날짜 넣기

> `$(date +%Y%m%d)` 처럼 형식 문자열을 이름 안에 넣어 백업 파일에 날짜를 붙입니다.

백업이나 덤프 파일 이름에 날짜를 넣으면 이름이 겹치지 않고 `ls` 로 정렬했을 때 시간순이 됩니다.

```bash
# 아래 두 줄은 실행한 날에 따라 값이 달라진다
echo backup-$(date +%Y%m%d).tar.gz    # backup-20261111.tar.gz

# 하루에 여러 번 만들면 시분초까지 넣는다
date +%F_%H%M%S                       # 2026-11-11_071758
```

### 상대 표현으로 날짜 옮기기

> 30일 뒤가 며칠인지, 두 날짜 사이가 며칠인지 셀 때 `-d` 가 받는 상대 표현과 에포크 초 뺄셈을 씁니다.

`-d` 는 "next Thursday" 같은 사람이 쓰는 표현도 읽습니다.[^date-man] 날짜 뒤에 `+30 days`·`2 weeks ago` 를 붙이면 그만큼 옮긴 날짜가 나옵니다.

```bash
# 날짜 뒤에 상대 표현을 붙여 옮긴다
date -u -d "2026-11-10 +30 days" +%F       # 2026-12-10
date -u -d "2026-11-10 -1 day" +%F         # 2026-11-09
date -u -d "2026-11-10 2 weeks ago" +%F    # 2026-10-27

# 기준 날짜를 빼면 오늘부터 센다. 실행한 날에 따라 달라진다
date -d yesterday +%F                      # 2026-11-10
date -d tomorrow +%F                       # 2026-11-12
```

시각 바로 뒤에 붙이는 `+30 days` 와 월말 넘침에는 함정이 있어 「시각 뒤 +30 과 월말 넘침」 에서 다룹니다.

### 두 날짜 사이의 날 수

> 날짜끼리의 뺄셈은 에포크 초에서 하고, 파일의 수정 시각은 `-r` 로 끌어옵니다.

두 날짜를 에포크 초로 바꿔 빼고 하루의 초 86,400 으로 나눕니다.

```bash
start=$(date -u -d "2026-11-10" +%s)
end=$(date -u -d "2026-12-25" +%s)
echo $(( (end - start) / 86400 ))    # 45
```

macOS BSD `date -r` 도 파일 이름을 받으면 같은 일을 하고, 숫자를 받을 때만 에포크 초로 읽습니다.[^bsd-date]

```bash
# 실습 준비에서 만든 old.txt 의 수정 시각을 찍는다
#   -r FILE   파일의 마지막 수정 시각을 쓴다 (--reference=FILE)
date -u -r old.txt "+%F %T"    # 2026-11-01 12:00:00
```

### 인증서 만료까지 남은 날

> 만료 시각을 에포크 초로 바꿔 남은 날을 세거나, `-checkend` 의 종료 상태로 기한 안에 만료되는지 확인합니다.

`openssl x509 -enddate` 로 뽑은 만료 시각을 `cut` 으로 떼어 에포크 초로 바꿉니다.[^x509] 그다음은 위 뺄셈처럼 현재 시각과의 차이를 86,400 으로 나눕니다.

```bash
# 실습용 자체 서명 인증서를 만든다. 유효 기간 30일
#   -x509      인증서 요청(CSR) 대신 X.509 인증서를 낸다
#   -newkey    새 개인 키를 함께 만든다. rsa:2048 은 2048비트 RSA 다
#   -nodes     개인 키를 암호로 감싸지 않는다. OpenSSL 3.0 에서는 -noenc 와 같고 deprecated 다
#   -keyout    개인 키를 저장할 파일
#   -out       인증서를 저장할 파일
#   -days      유효 기간(일)
#   -subj      인증서 주체(subject)를 정한다
openssl req \
  -x509 \
  -newkey rsa:2048 \
  -nodes \
  -keyout key.pem \
  -out cert.pem \
  -days 30 \
  -subj "/CN=lab.example" \
  2>/dev/null

# 인증서의 만료일만 읽는다. 만료 시각은 실행한 시각에 따라 달라진다
#   -enddate   만료일(notAfter 필드)을 찍는다
#   -noout     요청한 항목 말고는 찍지 않는다
#   -in        읽을 인증서 파일
openssl x509 \
  -enddate \
  -noout \
  -in cert.pem
# notAfter=Dec 11 07:18:10 2026 GMT

# 만료 시각을 에포크 초로 바꿔 지금과의 차이를 날로 센다
end=$(date -d "$(openssl x509 -enddate -noout -in cert.pem | cut -d= -f2)" +%s)
now=$(date +%s)
echo $(( (end - now) / 86400 ))              # 30
```

날 수가 아니라 "기한 안에 만료되는가" 만 알면 되면 `-checkend` 가 종료 상태로 답합니다. 아래 블록의 `/` 는 두 줄로 나온 출력을 한 줄에 줄여 적은 것입니다.

```bash
# 7일 안과 40일 안에 만료되는지 묻는다
#   -checkend 초   그 초 안에 만료되지 않으면 0, 만료되면 1 을 돌려준다
openssl x509 \
  -checkend $((7*86400)) \
  -noout \
  -in cert.pem; echo $?
# Certificate will not expire / 0

openssl x509 \
  -checkend $((40*86400)) \
  -noout \
  -in cert.pem; echo $?
# Certificate will expire / 1
```



## 주의사항과 동작 원리

> 시각 바로 뒤의 `+N` 과 월말 넘침은 오류나 엉뚱한 날짜를 내고, 32비트에 담은 에포크 초는 2038년에 넘칩니다.

### 시각 뒤 +30 과 월말 넘침

> 시각 바로 뒤의 `+N` 은 날 수가 아니라 시간대로 읽히고, 없는 날짜로 가는 달 더하기는 다음 달로 넘칩니다.

시각 바로 뒤의 `+30` 은 날 수가 아니라 UTC 와의 시간 차(30시간)로 읽힙니다.[^date-input] 그리고 1월 31일에 한 달을 더하면 없는 날짜인 2월 31일이 넘쳐 3월로 갑니다.

```bash
# 30시간 차이는 받지 않아 날짜 전체가 무효가 된다
date -u -d "2026-11-10 09:00:00 +30 days" "+%F %T"        # date: invalid date '2026-11-10 09:00:00 +30 days'

# +3 처럼 작은 수는 오류 없이 UTC+03 으로 읽히고, 남은 days 가 하루로 더해져 틀린 시각이 나온다
date -u -d "2026-11-10 09:00:00 +3 days" "+%F %T"         # 2026-11-11 06:00:00

# 시간대를 먼저 적으면 풀린다
date -u -d "2026-11-10 09:00:00 UTC +30 days" "+%F %T"    # 2026-12-10 09:00:00

# 없는 날짜로 가는 달 더하기는 다음 달로 넘친다. 없는 날짜 자체는 무효다
date -u -d "2026-01-31 +1 month" +%F    # 2026-03-03
date -u -d "2026-02-30"                 # date: invalid date '2026-02-30'
```

### 에포크 시간과 2038년

> 에포크 초를 부호 있는 32비트 정수에 담는 시스템은 2038년에 그 수가 넘칩니다.

에포크 시간은 모든 날을 정확히 86,400초로 칩니다. 부호 있는 32비트 `time_t` 는 최댓값 2³¹−1 의 1초 뒤를 담지 못해 음수로 넘어가며, 이것이 2038년 문제입니다.

```bash
# 부호 있는 32비트 정수의 최댓값 2³¹−1 = 2,147,483,647 을 날짜로 바꾸면 2038년 1월 19일 03:14:07 UTC 다
echo $(( 2**31 - 1 ))      # 2147483647
date -u -d @2147483647     # Tue Jan 19 03:14:07 UTC 2038

# 64비트 time_t 를 쓰는 지금의 리눅스는 그 다음 초도 찍는다
date -u -d @2147483648     # Tue Jan 19 03:14:08 UTC 2038
```

이 컨테이너의 `time_t` 가 64비트라서 마지막 줄이 정상으로 나왔습니다. 32비트 시스템이나 에포크 초를 32비트 칸에 저장하는 파일 형식·데이터베이스 칼럼은 여전히 이 경계를 넘지 못합니다.



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [cut 참조 시트](../text/cut.md) — 인증서 예에서 `notAfter=` 뒤를 자르는 법
- [head·tail 참조 시트](../text/head%C2%B7tail.md) — 날짜가 찍힌 로그의 앞뒤만 볼 때
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경, 공식 문서, 원서와 각주 정의입니다.

- GNU coreutils 9.1 의 `date --help` 원문 — Debian 12 컨테이너에서 2026-11-11 출력
- [date(1)](https://man7.org/linux/man-pages/man1/date.1.html) — 2026-11-11 조회
- [GNU coreutils 매뉴얼](https://www.gnu.org/software/coreutils/manual/coreutils.html) — "date invocation"·"Date input formats"
- 원서: 《Learning Modern Linux》 3장 Shells and Scripting (Michael Hausenblas, O'Reilly, 2022년) — 「지금 시각과 에포크 초」 의 `date +%s`·`date -d @…` 예

[^date-help]: `date --help` (GNU coreutils 9.1) — `%s` "seconds since the Epoch (1970-01-01 00:00 UTC)", `-d, --date=STRING` "display time described by STRING, not 'now'", `-r, --reference=FILE` "display the last modification time of FILE".
[^date-man]: `date(1)` 의 DATE STRING — "The --date=STRING is a mostly free format human readable date string such as … "next Thursday". A date string may contain items indicating calendar date, time of day, time zone, day of week, relative time, relative date, and numbers." <https://man7.org/linux/man-pages/man1/date.1.html>
[^date-input]: GNU coreutils 매뉴얼, "Time of day items" — "The time may alternatively be followed by a time zone correction, expressed as shhmm … The zone minutes term, mm, may be omitted, in which case the one- or two-digit correction is interpreted as a number of hours." `+24` 까지는 받고 `+25` 부터 무효가 되는 것과 `date --debug` 가 `+3` 을 `UTC+03` 으로 읽는 것은 이 시트의 실측입니다. <https://www.gnu.org/software/coreutils/manual/html_node/Time-of-day-items.html>
[^bsd-date]: FreeBSD `date(1)` — "-r seconds Print the date and time represented by seconds, where seconds is the number of seconds since the Unix Epoch", "-r filename Print the date and time of the last modification of filename." macOS 26.6 의 `man date` 도 같은 두 항목을 적습니다. <https://man.freebsd.org/cgi/man.cgi?query=date&sektion=1>
[^x509]: OpenSSL 3.0 `openssl-x509` 의 `-enddate`·`-checkend`. <https://docs.openssl.org/3.0/man1/openssl-x509/>
[^date-exit]: GNU coreutils 9.1 매뉴얼(Debian 12 의 `info coreutils`), "date invocation" — "An exit status of zero indicates success, and a nonzero value indicates failure." `date(1)` man 쪽에는 종료 상태 절이 없습니다. 이 기기에서 gnu.org 가 타임아웃이 나서 설치된 info 원문으로 대조했습니다. 코드 1 은 이 시트의 실측입니다(Debian 12, coreutils 9.1). <https://www.gnu.org/software/coreutils/manual/html_node/date-invocation.html>
