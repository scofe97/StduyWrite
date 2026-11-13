---
title: tr 참조 시트
tags: [linux, cheatsheet, tr, cli, reference]
status: draft
source:
  - GNU coreutils 매뉴얼
  - GNU coreutils tr (`--help` 원문, coreutils 9.1)
related:
  - ../README.md
updated: 2026-11-13
---

# tr 참조 시트

---

> `tr` 로 글자를 바꾸고 줄이고 지우는 법을 옵션마다 따라 치면 그대로 나오는 예제로 모은 조회용 시트입니다.

## 개요

> `tr` 은 글자 집합 둘을 짝지어 바꾸고 `-s` 로 연속을 줄이고 `-d` 로 지웁니다.

`tr` 은 파일 이름을 인자로 받지 않고 표준 입력을 읽어 표준 출력으로 냅니다.[^tr] coreutils 의 외부 바이너리이며 이 시트는 GNU 판(coreutils 9.1, Debian 12 컨테이너)으로 실측했습니다. macOS 기본 `tr` 은 BSD 판이라 문자 클래스와 `-c` 의 동작이 GNU 판과 조금 다릅니다.



## 핵심 문법

> 입력은 표준 입력으로만 받고 `STRING1`·`STRING2` 두 글자 집합이 동작을 정합니다.

```bash
# 호출 형태. 입력은 < 나 파이프로 준다
tr [OPTION]... STRING1 [STRING2]

# 글자 집합 둘을 짝지어 바꾼다 (글자를 짝지어 바꾸기)
tr SET1 SET2

# 짧은 SET2 를 채우지 않고 SET1 을 자른다 (글자를 짝지어 바꾸기)
tr -t SET1 SET2

# 글자 대신 문자 클래스로 집합을 적는다 (문자 클래스로 바꾸기)
tr '[:upper:]' '[:lower:]'

# SET1 에 든 글자를 지운다 (글자 지우기 -d)
tr -d SET1

# 연속한 글자를 하나로 줄인다 (연속을 한 글자로 줄이기 -s)
tr -s SET1

# SET1 이 아닌 글자를 대상으로 삼는다 (반대 집합 -c)
tr -c SET1 SET2
tr -cd SET1
tr -cs SET1 SET2

# 단어마다 줄을 나눠 다른 명령과 잇는다 (단어 빈도 세기)
tr -cs SET1 SET2 < 파일 | sort | uniq -c | sort -rn
```

### 문자 클래스

> `STRING1`·`STRING2` 자리에 글자 대신 쓰는 이름입니다. 본문에 나온 것만 실었습니다.

뜻은 `tr --help` 의 설명을 따랐습니다.[^tr-help]

```bash
# [:alnum:]   모든 글자와 숫자
# [:alpha:]   모든 글자
# [:blank:]   모든 가로 공백
# [:digit:]   모든 숫자
# [:lower:]   모든 소문자
# [:space:]   모든 가로·세로 공백
# [:upper:]   모든 대문자
```



## 종료 코드

> `tr` 은 성공하면 0, 실패하면 1 을 돌려줍니다.

매뉴얼은 `tr` 절에 성공은 0, 실패는 0 이 아닌 값이라고만 적고 실패 코드를 나누지 않습니다.[^tr-exit] 아래는 Debian 12 컨테이너에서 성공 하나와 실패 네 가지를 돌린 결과입니다.

```bash
# 0  성공. 입력을 읽어 바꾸고 끝났을 때
# 1  실패. 파일 이름 인자, 모르는 옵션, 빠진 피연산자, 없는 문자 클래스를 줬을 때
echo a | tr a b; echo $?    # b / 0

# tr 은 파일을 인자로 받지 않는다. 입력은 < 나 파이프로 준다
# 2>&1 은 오류 메시지를 표준 출력에 합쳐 종료 코드와 함께 보인다
tr a b app.log 2>&1; echo $?
```

```bash
tr: extra operand 'app.log'
Try 'tr --help' for more information.
1
```

```bash
# 모르는 옵션
tr --bad; echo $?    # tr: unrecognized option '--bad' / Try 'tr --help' for more information. / 1

# 피연산자가 없는 경우
tr; echo $?          # tr: missing operand / Try 'tr --help' for more information. / 1

# 없는 문자 클래스
echo a | tr '[:foo:]' x; echo $?    # tr: invalid character class 'foo' / 1
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션만 씁니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 파일이 모두 생깁니다.

OrbStack 의 Linux VM 이나 `docker run -it --rm debian:12` 안에서 실행합니다.

```bash
mkdir -p ~/cmd-lab/tr && cd ~/cmd-lab/tr
cat > app.log << 'EOF'
2026-11-10 09:01:15 INFO  order-api started
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:14:41 WARN  retrying orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
2026-11-10 10:06:01 error db connection reset
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
2026-11-10 11:30:00 INFO  heartbeat
EOF
printf 'name=app\r\nport=8080\r\n' > crlf.conf
printf 'Hello,   World!  Order 1001 \t done\n' > mixed.txt
```

`app.log` 는 일곱 줄짜리 애플리케이션 로그입니다. `crlf.conf` 는 줄 끝이 `\r\n` 인 두 줄짜리 설정 파일이고, `mixed.txt` 는 공백과 탭이 섞인 한 줄입니다. 나머지 예는 `echo` 와 `printf` 로 입력을 직접 만들므로 따로 준비할 파일이 없습니다.

### 글자를 짝지어 바꾸기

> `tr SET1 SET2` 는 SET1 의 n 번째 글자를 SET2 의 n 번째 글자로 바꿉니다.

SET1·SET2 는 단어나 문자열이 아니라 글자 목록이라 `tr 'lo' 'xy'` 는 `lo` 를 찾지 않고 글자 `l`·`o` 를 따로 바꿉니다.

```bash
# SET1→SET2: l 은 x 로, o 는 y 로
echo 'hello world' | tr 'lo' 'xy'  # hexxy wyrxd

# 범위 a-y→b-z: 알파벳을 한 글자씩 민다
echo 'hello' | tr 'a-y' 'b-z'  # ifmmp

# 범위 둘을 한 번에: _ 는 . 으로, 대문자는 소문자로
echo 'Com_Acme' | tr '_A-Z' '.a-z'  # com.acme
```

SET2 가 SET1 보다 짧을 때 GNU `tr` 은 기본으로 BSD `tr` 처럼 채우고, `-t` 를 주면 System V `tr` 처럼 자릅니다.[^tr-t]

```bash
# SET2 가 짧으면 마지막 글자를 되풀이해 채운다: b, c 모두 y 가 된다
echo 'abc' | tr 'abc' 'xy'  # xyy

# 남는 c 는 바뀌지 않고 그대로 남는다
#   -t   SET1 을 SET2 길이로 자른다 (--truncate-set1)
echo 'abc' | tr -t 'abc' 'xy'  # xyc
```

줄바꿈도 글자라서 `\n` 으로 넣고 뺄 수 있습니다.

```bash
# : 를 줄바꿈으로: 한 줄을 세 줄로 펼친다
echo 'a:b:c' | tr ':' '\n'
```

```bash
a
b
c
```

### 문자 클래스로 바꾸기

> 글자를 하나씩 나열하는 대신 `[:upper:]`·`[:lower:]`·`[:digit:]`·`[:space:]` 같은 클래스를 씁니다.

대문자·소문자 변환은 범위 `a-z` 로도 되지만 범위는 C 로캘 밖에서 이식성이 없습니다. `[:lower:]` 같은 클래스는 어느 로캘에서도 같은 뜻으로 읽힙니다.[^tr-class]

```bash
# [:upper:]→[:lower:]: 대문자를 소문자로
echo 'Hello World' | tr '[:upper:]' '[:lower:]'  # hello world

# [:lower:]→[:upper:]: 소문자를 대문자로
echo 'Hello World' | tr '[:lower:]' '[:upper:]'  # HELLO WORLD

# [:digit:]→#: 숫자를 모두 #
echo 'order 1001 and 1002' | tr '[:digit:]' '#'  # order #### and ####
```

```bash
# [:space:]→_: 공백, 탭, 줄바꿈이 모두 _ 가 된다. 끝의 줄바꿈도 바뀌어 echo 로 줄을 닫는다
printf 'a b\tc\nd\n' | tr '[:space:]' '_'; echo
```

```bash
a_b_c_d_
```

### 글자 지우기 -d

> `-d` 는 SET1 에 든 글자를 지우고 바꾸지는 않습니다.

지울 대상이 문자열이 아니라 글자 목록이라는 점은 바꾸기와 같습니다.[^tr]

```bash
# l 과 o 를 모두 지운다. 단어 lo 가 아니라 글자 l, o 가 대상이다
#   -d   SET1 에 든 글자를 지운다 (--delete)
echo 'hello world' | tr -d 'lo'  # he wrd

# -d 와 [:digit:]: 숫자를 모두 지운다
echo 'a1b2c3' | tr -d '[:digit:]'  # abc
```

윈도우에서 만든 파일은 줄 끝이 `\r\n` 이라 값 끝에 보이지 않는 `\r` 이 붙습니다. 파일은 `< 파일` 로 `tr` 의 표준 입력에 연결합니다.[^tr]

```bash
# 지우기 전: 줄마다 \r\n 이 붙어 있다. od -c 가 문자를 하나씩 보여 주므로 \r 이 남았는지 확인한다
#   -c   출력할 글자로 인쇄 가능한 문자나 역슬래시 이스케이프를 고른다 (od 의 옵션)
od -c crlf.conf | head -2
```

```bash
0000000   n   a   m   e   =   a   p   p  \r  \n   p   o   r   t   =   8
0000020   0   8   0  \r  \n
```

```bash
# -d '\r': \r 을 지우면 \n 만 남는다
tr -d '\r' < crlf.conf | od -c | head -2
```

```bash
0000000   n   a   m   e   =   a   p   p  \n   p   o   r   t   =   8   0
0000020   8   0  \n
```

```bash
# 짧은 입력으로 같은 일: \r 이 사라졌는지 od -c 로 본다
printf 'a\r\nb\r\n' | tr -d '\r' | od -c | head -1  # 0000000   a  \n   b  \n
```

### 연속을 한 글자로 줄이기 -s

> `-s` 는 연속해서 나오는 글자를 하나로 줄입니다.

집합 하나만 적으면 그 집합의 연속을 줄이고, 두 집합을 적으면 바꾼 뒤의 연속을 줄입니다.[^tr]

```bash
# 연속 공백을 하나로 축약
#   -s   마지막에 적은 집합에 든 글자의 연속을 한 글자로 줄인다 (--squeeze-repeats)
echo 'a    b   c' | tr -s ' '  # a b c

# -s 와 범위: a, b, c 의 연속을 각각 하나로
echo 'aaabbbccc' | tr -s 'a-c'  # abc

# -s 는 글자 하나를 지정해 구분자 정리에도 쓴다
echo 'a,,b,,,c' | tr -s ','  # a,b,c

# -s 와 SET2: 바꾼 뒤의 연속을 줄인다. 공백 연속이 _ 하나가 된다
echo 'hello  world' | tr -s ' ' '_'  # hello_world
```

```bash
# 공백과 탭이 섞인 줄을 한 번에 정리해 연속을 공백 하나로 줄인다
# [:blank:] 는 공백과 탭만 가리켜서 줄바꿈은 건드리지 않는다
tr -s '[:blank:]' ' ' < mixed.txt
```

```bash
Hello, World! Order 1001 done
```

### 반대 집합 -c

> `-c` 는 SET1 에 적은 글자가 아닌 모든 글자를 대상으로 삼습니다.

줄바꿈도 반대 집합에 들어가므로 `\n` 을 SET1 에 함께 적지 않으면 줄바꿈까지 바뀌거나 지워집니다.[^tr]

```bash
# 숫자가 아닌 글자를 모두 X 로. 입력 끝의 줄바꿈도 X 가 된다
#   -c   SET1 을 뒤집어 SET1 에 없는 글자를 대상으로 삼는다 (-C, --complement)
printf 'abc123def' | tr -c '0-9' 'X'; echo
```

```bash
XXX123XXX
```

```bash
# -cd: -c 와 -d 를 합쳐 SET1 에 든 글자만 남기고 나머지를 지운다. 숫자만 뽑을 때 쓴다
# 줄바꿈도 지워지므로 echo 로 닫는다
echo 'abc123def' | tr -cd '0-9'; echo  # 123

# -cd 에 \n 을 함께 적어 줄바꿈을 지키는 꼴
echo 'abc123def' | tr -cd '0-9\n'  # 123

# -cd 와 [:alnum:]: 영문자와 숫자만 남긴다
echo 'Hello, World! 123' | tr -cd '[:alnum:]\n'  # HelloWorld123
```

```bash
# -cs: -c 와 -s 를 합쳐 단어가 아닌 글자의 연속을 구분자 하나로 바꾼다. 단어 단위로 줄을 나눌 때 쓴다
# 알파벳이 아닌 글자의 연속을 줄바꿈 하나로. 단어마다 한 줄이 된다
echo 'a  b, c' | tr -cs '[:alpha:]' '\n'
```

```bash
a
b
c
```

### 단어 빈도 세기

> `tr` 로 단어마다 줄을 나눈 뒤 `sort`·`uniq` 로 세면 많이 나온 단어가 보입니다.

```bash
# 파이프라인: 단어마다 줄을 나눠 세면 많이 나온 단어가 보인다
tr -cs 'A-Za-z' '\n' < app.log | sort | uniq -c | sort -rn | head -3
```

```bash
      3 orderId
      3 ERROR
      2 timeout
```



## 주의사항과 동작 원리

> `tr -d` 의 인자는 문자열이 아니라 글자 목록이고, `-` 로 시작하는 글자는 `--` 뒤에 적어야 합니다.

### -d 는 문자열이 아니라 글자 목록

> `tr -d 'orderId='` 는 접두사를 떼지 않고 그 글자들을 값에서도 지웁니다.

`orderId=1001` 에서 앞부분을 떼려고 `tr -d 'orderId='` 를 쓰면 글자 `o r d e I =` 를 하나하나 지웁니다. 그래서 값이 숫자일 때만 우연히 맞아 보이고, 값에 같은 글자가 들면 함께 지워집니다. 접두사 문자열을 떼는 일은 [sed 참조 시트](./sed.md) 의 `s/^접두사//` 가 맞습니다.

```bash
# 글자 목록이라 값 속 글자도 지워진다: Order 의 O 는 대문자라 남고 소문자 r, d, e 는 지워진다
echo 'Order orderId=1001' | tr -d 'orderId='  # O 1001
```

### - 로 시작하는 글자와 --

> `-` 로 시작하는 글자는 `--` 로 옵션을 끝낸 뒤에 적습니다.

옵션은 인자 앞에 와야 합니다.[^tr] `-` 로 시작하는 글자를 지우려면 `--` 로 옵션이 끝났음을 알립니다.

```bash
# --: 옵션 끝을 알려 - 를 글자로 읽게 한다
echo 'a-b' | tr -d -- '-'  # ab
```



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [sed 참조 시트](./sed.md) — 글자 하나가 아니라 문자열을 바꿀 때
- [sort·uniq·wc 참조 시트](./sort%C2%B7uniq%C2%B7wc.md) — 바꾼 줄을 정렬하고 세기
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- GNU coreutils 9.1 의 `tr --help` 원문 — Debian 12 컨테이너에서 2026-11-13 출력
- [GNU coreutils 매뉴얼](https://www.gnu.org/software/coreutils/manual/coreutils.html) — 2026-11-11 조회

[^tr]: GNU coreutils 매뉴얼, "tr invocation" — "tr copies standard input to standard output", "-c: Instead of array1, use its complement (all characters not specified by string1)", "-d: Delete characters in array1; do not translate", "-s: Replace each sequence of a repeated character that is listed in the last specified array, with a single occurrence of that character", "-t: Truncate array1 to the length of array2", "Options must precede operands". <https://www.gnu.org/software/coreutils/manual/coreutils.html#tr-invocation>
[^tr-class]: GNU coreutils 매뉴얼, "Specifying arrays of characters" 의 `space` 는 "Horizontal or vertical whitespace", `blank` 는 "Horizontal whitespace" 이고, "Translating" 은 "ranges like a-z are not portable outside the C locale" 라고 적습니다. <https://www.gnu.org/software/coreutils/manual/coreutils.html#Character-arrays>
[^tr-t]: GNU coreutils 매뉴얼, "Translating" — "By default, GNU tr handles this case like BSD tr", "When the --truncate-set1 (-t) option is given, GNU tr handles this case like the System V tr instead". <https://www.gnu.org/software/coreutils/manual/coreutils.html#Translating>
[^tr-help]: `tr --help` (GNU coreutils 9.1) — `[:alnum:]` "all letters and digits", `[:alpha:]` "all letters", `[:blank:]` "all horizontal whitespace", `[:digit:]` "all digits", `[:lower:]` "all lower case letters", `[:space:]` "all horizontal or vertical whitespace", `[:upper:]` "all upper case letters".
[^tr-exit]: GNU coreutils 9.1 매뉴얼(Debian 12 의 `info coreutils`), "tr invocation" — "An exit status of zero indicates success, and a nonzero value indicates failure." 코드 1 은 이 시트의 실측입니다(Debian 12, coreutils 9.1). <https://www.gnu.org/software/coreutils/manual/html_node/tr-invocation.html>
