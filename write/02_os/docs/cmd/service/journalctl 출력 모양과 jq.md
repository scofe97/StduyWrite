---
title: journalctl 출력 모양과 jq
tags: [linux, cheatsheet, journalctl, systemd, journal, output, json, jq, reference]
status: draft
source:
  - systemd 259 journalctl(1) (OrbStack Ubuntu 26.04 VM 의 `man journalctl`·`journalctl --help` 원문, freedesktop.org journalctl(1))
related:
  - ./journalctl.md
  - ./journalctl%20저장%20공간과%20읽기%20권한.md
  - ../README.md
updated: 2026-11-14
---

# journalctl 출력 모양과 jq

---

> 같은 로그를 시각 표기·필드·JSON 으로 바꿔 보고 `jq` 로 필드를 뽑는 `journalctl` 을 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> 이 시트는 `journalctl` 의 출력 모양을 바꾸는 일과 JSON 출력을 `jq` 로 잇는 일을 다룹니다.

[journalctl 참조 시트](./journalctl.md)에서 출력 모양 바꾸기와 jq 와 잇기 유스케이스를 떼어 낸 것입니다. 예는 그 시트의 「실습 준비」 블록을 돌린 상태에서 이어지고, 출력은 같은 OrbStack Ubuntu 26.04 VM(systemd 259.9)에서 root 셸로 받았습니다.



## 핵심 문법

> `-o` 로 출력 모양을 고르고, `--output-fields` 로 낼 필드를 줄이고, `-o json` 을 `jq` 에 넘깁니다.

```bash
# 호출 형태
# journalctl --help 의 첫 줄
journalctl [OPTIONS...] [MATCHES...]

# 출력 모양을 바꾼다. 모드 이름은 원래 시트의 「출력 모드」 에 있다 (출력 모양 바꾸기)
journalctl -o 출력모드

# verbose·json 계열에서 낼 필드를 고른다 (출력 모양 바꾸기)
journalctl -o verbose --output-fields=필드,필드

# JSON 한 줄씩 내서 jq 로 필드를 뽑는다 (jq 와 잇기)
journalctl -o json | jq -r .필드
```

`-o` 의 모드 목록은 원래 시트와 이 시트가 함께 쓰므로 [journalctl 참조 시트](./journalctl.md)의 「출력 모드」 한 곳에 둡니다.



## 종료 코드

> 종료 코드는 `journalctl` 한 벌이라 이 시트는 목록을 따로 싣지 않습니다.

목록은 [journalctl 참조 시트](./journalctl.md)의 「종료 코드」 에 있습니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션과 만든 상태만 씁니다.

### 실습 준비

> 이 시트는 따로 만드는 것이 없고 원래 시트가 남긴 로그를 그대로 읽습니다.

먼저 [journalctl 참조 시트](./journalctl.md)의 「실습 준비」 블록을 같은 셸에서 돌립니다. PID·시각·커서는 실행마다 다르므로 이 시트의 값과 같지 않아도 됩니다.

### 출력 모양 바꾸기

> `-o` 는 같은 줄을 시각 표기가 다른 한 줄이나 필드 전체로 바꿔 보여 줍니다.[^outmode]

```bash
# 시각을 ISO 8601 로 낸다. 끝의 +09:00 이 KST 다
journalctl -t lab-web -o short-iso
```

```bash
2026-11-14T07:50:40+09:00 ubuntu lab-web[56324]: lab-web: cache miss rate high
2026-11-14T07:50:40+09:00 ubuntu lab-web[56325]: lab-web: request served
```

```bash
# 마이크로초까지 낸다
journalctl -t lab-web -o short-precise
```

```bash
Nov 14 07:50:40.684125 ubuntu lab-web[56324]: lab-web: cache miss rate high
Nov 14 07:50:40.685297 ubuntu lab-web[56325]: lab-web: request served
```

```bash
# 마지막 줄의 필드를 세 개만 고른다
#   --output-fields   verbose·json·cat 에서 낼 필드를 고른다
journalctl \
  -t lab-web \
  -n 1 \
  -o verbose \
  --output-fields=MESSAGE,PRIORITY,_PID
```

```bash
Sat 2026-11-14 07:50:40.685297 KST [s=ab714de21fe34e4c89cfc556ddd9b969;i=3497;b=70f87065d40a408d88f0c9cfd9e3151d;m=48e5a1dff5;t=6603041e8052a;x=c1e846592513707c]
    PRIORITY=6
    MESSAGE=lab-web: request served
    _PID=56325
```

`--output-fields` 로 고르지 않아도 `__CURSOR`·`__REALTIME_TIMESTAMP`·`__MONOTONIC_TIMESTAMP`·`_BOOT_ID` 는 verbose 와 json 계열에 항상 나옵니다.[^outfields]

```bash
# 같은 줄을 JSON 으로 들여 써서 낸다
journalctl \
  -t lab-web \
  -n 1 \
  -o json-pretty \
  --output-fields=MESSAGE,PRIORITY
```

```bash
{
	"_BOOT_ID" : "70f87065d40a408d88f0c9cfd9e3151d",
	"PRIORITY" : "6",
	"__REALTIME_TIMESTAMP" : "1794610240685354",
	"__SEQNUM" : "13463",
	"__MONOTONIC_TIMESTAMP" : "313090236405",
	"__SEQNUM_ID" : "ab714de21fe34e4c89cfc556ddd9b969",
	"__CURSOR" : "s=ab714de21fe34e4c89cfc556ddd9b969;i=3497;b=70f87065d40a408d88f0c9cfd9e3151d;m=48e5a1dff5;t=6603041e8052a;x=c1e846592513707c",
	"MESSAGE" : "lab-web: request served"
}
```

필드 순서는 실행마다 다를 수 있습니다.

```bash
# UTC 로 낸다. KST 보다 9시간 이르므로 07:50 이 전날 22:50 이 된다
#   --utc   시각을 UTC 로 표기한다
journalctl \
  -t lab-web \
  -n 1 \
  --utc
# Nov 13 22:50:40 ubuntu lab-web[56325]: lab-web: request served

# 호스트 이름 열을 뗀다
#   -W   호스트 이름을 내지 않는다 (--no-hostname)
journalctl \
  -t lab-web \
  -n 1 \
  -W
# Nov 14 07:50:40 lab-web[56325]: lab-web: request served
```

### jq 와 잇기

> `-o json` 은 항목마다 JSON 한 줄을 내서 `jq` 로 필드를 골라 다른 명령에 넘길 수 있습니다.

`jq` 는 JSON 을 다루는 별도 패키지의 명령입니다.

```bash
# 심각도와 메시지를 탭으로 이어 한 줄씩 뽑는다
journalctl -t lab-web -o json \
  | jq -r '[.PRIORITY, .MESSAGE] | @tsv'
```

```bash
4	lab-web: cache miss rate high
6	lab-web: request served
```

```bash
# lab-report 의 심각도별 줄 수를 센다
journalctl -u lab-report -o json \
  | jq -r .PRIORITY \
  | sort \
  | uniq -c
```

```bash
      1 3
      1 4
      5 6
```



## 주의사항과 동작 원리

### `-T` 가 `-o cat` 에서 듣지 않음

> 식별자를 빼는 `-T` 는 short 계열 출력에서만 줄을 줄이고 `cat`·`json` 에서는 그대로 모두 냅니다.

```bash
# -T systemd 로 systemd[1] 이 남긴 줄을 뺀다. short 에서는 7줄이 4줄이 된다
#   -T   이 syslog 식별자의 줄을 뺀다 (--exclude-identifier)
journalctl -u lab-report -T systemd | wc -l    # 4

# 같은 조건이 -o cat 에서는 7줄 그대로다
journalctl \
  -u lab-report \
  -T systemd \
  -o cat | wc -l
# 7
```

매뉴얼에는 이 구분이 적혀 있지 않은 실측이라 systemd 259.9 에서만 확인했습니다.[^ident]



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [journalctl 참조 시트](./journalctl.md) — 이 시트가 이어받는 실습 준비와 「출력 모드」 목록, 로그를 좁혀 읽는 예
- [journalctl 저장 공간과 읽기 권한](./journalctl%20저장%20공간과%20읽기%20권한.md) — 저널 크기·저장 위치·정리와 읽기 권한
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- 검증 환경: OrbStack Ubuntu 26.04 VM, systemd 259.9 (`259.9-0ubuntu0.1`) — 2026-11-14 실측, `journalctl --help`·`man journalctl` 원문 대조
- [journalctl(1)](https://www.freedesktop.org/software/systemd/man/latest/journalctl.html) — freedesktop.org 최신판에서 각주 인용문의 존재를 확인

[^outmode]: journalctl(1) `-o` — "short is the default and generates an output that is mostly identical to the formatting of classic syslog files, showing one line per journal entry." "short-iso is very similar, but shows timestamps in the RFC 3339 profile of ISO 8601." "short-precise is very similar, but shows classic syslog timestamps with full microsecond precision." "cat generates a very terse output, only showing the actual message of each journal entry with no metadata, not even a timestamp." "verbose shows the full-structured entry items with all fields." "json formats entries as JSON objects, separated by newline characters" "json-pretty formats entries as JSON data structures, but formats them in multiple lines in order to make them more readable by humans." https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
[^outfields]: journalctl(1) `--output-fields=` — "This has an effect only for the output modes which would normally show all fields (verbose, export, json, json-pretty, json-sse and json-seq), as well as on cat. For the former, the "__CURSOR", "__REALTIME_TIMESTAMP", "__MONOTONIC_TIMESTAMP", and "_BOOT_ID" fields are always printed." https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
[^ident]: journalctl(1) `-T` — "Exclude messages for the specified syslog identifier SYSLOG_IDENTIFIER." https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
