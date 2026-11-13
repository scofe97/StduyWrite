---
title: sed 참조 시트
tags: [linux, cheatsheet, sed, cli, reference]
status: draft
source:
  - GNU sed 매뉴얼
  - GNU sed 4.9 (`--help` 원문)
related:
  - ../README.md
updated: 2026-11-13
---

# sed 참조 시트

---

> `sed` 로 줄을 고르고 바꾸고 설정 파일을 고치는 법을 옵션과 명령마다 따라 치면 그대로 나오는 예제로 모은 조회용 시트입니다.

## 개요

> `sed` 는 입력에서 줄을 고르고 바꾸고 넣고 지우는 스트림 편집기입니다.

sed 패키지의 외부 바이너리이며 이 시트는 GNU 판(sed 4.9, Debian 12 컨테이너)으로 실측했습니다. macOS 기본 `sed` 는 GNU 판이 아니어서 `-i` 의 인자 규칙과 `\+`·`1~3` 같은 확장이 다르게 동작합니다. 없는 파일을 주면 오류 메시지와 함께 종료 상태 2 를 돌려줍니다(「종료 코드」).



## 핵심 문법

> 스크립트가 줄에 하는 일을 정하고, 주소가 그 스크립트가 들 줄을 정합니다.

```bash
# 호출 형태
sed [OPTION]... {script-only-if-no-other-script} [input-file]...

# 스크립트를 줄마다 적용한다 (한 줄씩 읽고 찍기)
sed 스크립트 파일
sed -n 스크립트 파일

# 주소에 맞는 줄만 찍는다 (줄 번호와 패턴으로 고르기)
sed -n '주소p' 파일

# 주소에 맞는 줄을 지운다 (줄 지우기)
sed '주소d' 파일

# N 행을 찍고 끝낸다 (앞쪽만 읽고 멈추기)
sed Nq 파일

# 맞은 부분을 바꾼다 (s 명령으로 바꾸기)
sed 's/찾을 것/바꿀 것/플래그' 파일
sed -E 's/정규식/바꿀 것/' 파일

# 스크립트를 여럿 준다 (명령 여럿을 한 번에)
sed -e 스크립트 -e 스크립트 파일
sed '스크립트; 스크립트' 파일

# 줄을 넣거나 바꾼다 (줄 넣기와 줄 끝 다듬기)
sed '2i\텍스트' 파일
sed '2a\텍스트' 파일
sed '2c\텍스트' 파일

# 글자를 같은 자리의 글자로 바꾼다 (글자 하나씩 바꾸는 y)
sed 'y/원본/대상/' 파일

# 파일을 제자리에서 고친다 (설정 파일을 제자리에서 고치기)
sed -i.bak 스크립트 파일
```

### 주소

> 명령 앞에 두어 그 명령이 들 줄을 고르는 꼴입니다. 본문에 나온 것만 실었습니다.

뜻은 매뉴얼의 설명을 따랐습니다.[^sed-addr-list]

```bash
# N             그 줄 하나
# $             마지막 줄
# N,M           N 행부터 M 행까지
# /패턴/        패턴이 든 줄
# /패턴/I       대소문자를 가리지 않는 /패턴/ (GNU 확장)
# /a/,/b/       a 가 나온 줄부터 b 가 나온 줄까지
# 주소,+N       주소가 맞은 줄과 그 뒤 N 줄 (GNU 확장)
# first~step    first 줄부터 step 줄 간격으로 (GNU 확장)
# 주소!         주소에 맞지 않는 줄
```

### 명령 글자

> 주소 뒤에 두어 그 줄에 할 일을 정하는 글자입니다. 본문에 나온 것만 실었습니다.

뜻은 매뉴얼의 명령 요약을 따랐습니다.[^sed-cmds]

```bash
# p                  지금 줄을 찍는다
# d                  지금 줄을 지우고 다음 줄로 넘어간다
# q                  지금 줄을 찍고 끝낸다
# =                  현재 줄 번호를 찍는다
# { 명령 ; 명령 }    명령 여럿을 한 주소에 묶는다
# s/찾을 것/바꿀 것/플래그
#                    맞은 부분을 바꾼다
# i\ 텍스트          그 줄 앞에 텍스트를 넣는다
# a\ 텍스트          그 줄 뒤에 텍스트를 넣는다
# c\ 텍스트          그 줄을 텍스트로 바꾼다
# y/원본/대상/       원본의 글자를 같은 자리의 대상 글자로 바꾼다
```

### s 명령의 플래그

> `s/찾을 것/바꿀 것/` 끝에 붙여 바꾸는 방식을 정합니다. 본문에 나온 것만 실었습니다.

뜻은 매뉴얼의 「The s Command」 를 따랐습니다.[^sed-flags]

```bash
# g   줄 안의 모든 일치를 바꾼다
# N   줄 안에서 N 번째 일치만 바꾼다
# I   대소문자를 가리지 않는다 (GNU 확장)
# p   바꿨으면 그 줄을 찍는다
```



## 종료 코드

> `sed` 는 성공하면 0, 실패하면 원인에 따라 1·2·4 를 돌려줍니다.

매뉴얼은 코드마다 원인을 적고, `q`·`Q` 로 종료 코드를 직접 정하는 것을 GNU 확장이라고 적습니다.[^sed-exit-codes] 아래는 Debian 12 컨테이너에서 성공 하나, 실패 넷, 종료 코드 지정 하나를 돌린 결과입니다.

```bash
# 0  성공
# 1  잘못된 명령, 잘못된 구문, 잘못된 정규식
# 2  입력 파일을 열 수 없다. 나머지 파일은 계속 처리한다
# 4  입출력 오류나 실행 중 심각한 오류로 곧바로 중단했다
# q, Q 는 지정한 종료 코드로 끝낸다 (GNU 확장)

# a 를 b 로 바꿔 찍고 0 으로 끝난다
echo a | sed 's/a/b/'; echo $?    # b / 0
```

없는 파일을 주면 `sed` 는 오류 메시지를 stderr 로 내고 종료 상태 2 를 돌려줍니다.[^sed-exit]

```bash
# 없는 파일: 오류 메시지와 종료 상태 2
# 2>&1 은 오류 메시지를 표준 출력에 합쳐 종료 코드와 함께 보인다
sed 's/a/A/' nofile.txt 2>&1; echo $?
```

```bash
sed: can't read nofile.txt: No such file or directory
2
```

```bash
# 모르는 명령
echo a | sed k; echo $?    # sed: -e expression #1, char 1: unknown command: `k' / 1

# 닫히지 않은 s 명령
echo a | sed 's/a/b'; echo $?    # sed: -e expression #1, char 5: unterminated `s' command / 1

# 쓸 곳이 없으면 4. /dev/full 에 쓰면 항상 실패한다
echo a | sed p > /dev/full; echo $?    # sed: couldn't flush stdout: No space left on device / 4

# Q7: 지금 줄을 찍지 않고 종료 코드 7 로 끝낸다
echo a | sed Q7; echo $?    # 7
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션만 씁니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 파일이 모두 생깁니다.

OrbStack 의 Linux VM 이나 `docker run -it --rm debian:12` 안에서 실행합니다.

```bash
mkdir -p ~/cmd-lab/sed && cd ~/cmd-lab/sed
cat > app.log << 'EOF'
2026-11-10 09:01:15 INFO  order-api started
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:14:41 WARN  retrying orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
2026-11-10 10:06:01 error db connection reset
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
2026-11-10 11:30:00 INFO  heartbeat
EOF
cat > sshd_config << 'EOF'
# This is the sshd server system-wide configuration file.

Port 22
#PermitRootLogin prohibit-password
PasswordAuthentication yes
  # indented comment

X11Forwarding no
EOF
cat > fruits.txt << 'EOF'
apple pie
banana split
apple tart
cherry cake
EOF
cat > names.csv << 'EOF'
kim,minsu,30
lee,jiwon,25
park,hana,41
EOF
```

`app.log` 는 일곱 줄짜리 애플리케이션 로그이고 `ERROR`·`error`·`[ERROR]` 가 섞여 있습니다. `sshd_config` 에는 주석·빈 줄·들여 쓴 주석이 있고 `fruits.txt` 는 `apple` 이 두 줄에 든 네 줄짜리 목록입니다. `names.csv` 는 쉼표로 나눈 세 칸짜리 세 줄입니다. 이 시트의 `-i` 예제는 `sshd_config` 를 실제로 고치므로 순서대로 따라 칩니다. 중간에 어긋나면 위 블록을 다시 붙여 넣어 처음 상태로 돌립니다.

### 한 줄씩 읽고 찍기

> 자동 출력이 기본이고, `-n` 은 그것을 꺼서 `p` 로 찍은 줄만 남깁니다.

`sed` 는 입력을 한 줄씩 읽어 명령을 적용하고 그 줄을 찍은 뒤 다음 줄로 넘어갑니다.[^sed-cycle]

```bash
# 자동 출력: 바꾼 줄도 안 바꾼 줄도 나온다
# s/apple/APPLE/ 은 첫 일치를 바꾼다 (「s 명령으로 바꾸기」)
printf 'apple\nbanana\n' | sed 's/apple/APPLE/'
```

```bash
APPLE
banana
```

```bash
# -n 을 붙이면 자동 출력이 꺼져서 p 가 없는 s 는 아무것도 찍지 않는다
#   -n   자동 출력을 끈다 (--quiet, --silent)
printf 'apple\nbanana\n' | sed -n 's/apple/APPLE/'  # 출력 없음

# -n 과 s 의 p 플래그: 바꾼 줄만 나온다
printf 'apple\nbanana\n' | sed -n 's/apple/APPLE/p'  # APPLE
```

### 줄 번호와 패턴으로 고르기

> 명령 앞에 주소를 두면 그 줄에만 명령이 듭니다.

줄을 고를 때는 `-n` 과 `p` 를 함께 씁니다. `+N` 과 `first~step` 은 GNU 확장입니다.[^sed-addr]

```bash
# 2행 하나
sed -n '2p' app.log
```

```bash
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
```

```bash
# N,M: 2행부터 3행까지
sed -n '2,3p' app.log
```

```bash
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:14:41 WARN  retrying orderId=1001
```

```bash
# $: 마지막 줄
sed -n '$p' app.log  # 2026-11-10 11:30:00 INFO  heartbeat

# N,$: 5행부터 끝까지
sed -n '5,$p' app.log
```

```bash
2026-11-10 10:06:01 error db connection reset
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
2026-11-10 11:30:00 INFO  heartbeat
```

```bash
# /패턴/: 패턴이 든 줄
sed -n '/heartbeat/p' app.log  # 2026-11-10 11:30:00 INFO  heartbeat

# /패턴/I: 대소문자를 가리지 않는 GNU 확장. error 와 ERROR 가 모두 걸린다
sed -n '/error/Ip' app.log
```

```bash
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
2026-11-10 10:06:01 error db connection reset
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
```

```bash
# /a/,/b/: WARN 이 나온 줄부터 reset 이 나온 줄까지. 쉼표로 잇는다
sed -n '/WARN/,/reset/p' app.log
```

```bash
2026-11-10 09:14:41 WARN  retrying orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
2026-11-10 10:06:01 error db connection reset
```

```bash
# /a/,+N: WARN 줄과 그 뒤 한 줄
sed -n '/WARN/,+1p' app.log
```

```bash
2026-11-10 09:14:41 WARN  retrying orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
```

```bash
# first~step: 1행부터 3줄 간격(1, 4, 7행)
sed -n '1~3p' app.log
```

```bash
2026-11-10 09:01:15 INFO  order-api started
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
2026-11-10 11:30:00 INFO  heartbeat
```

```bash
# !: 주소에 맞지 않는 줄에 명령이 든다. INFO 가 아닌 줄만 찍는다
sed -n '/INFO/!p' app.log
```

```bash
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:14:41 WARN  retrying orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
2026-11-10 10:06:01 error db connection reset
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
```

```bash
# 맞은 줄에서 값만 뽑는다: s 로 앞부분을 지우고 p 로 찍는다
printf 'name=app\nversion=1.2.3\n' | sed -n 's/^version=//p'  # 1.2.3
```

### 줄 지우기

> `d` 는 맞은 줄을 지우고 다음 줄로 넘어갑니다.

지운 줄은 자동 출력에도 나오지 않으므로 `-n` 이 필요 없습니다.

```bash
# d: 2행부터 6행까지 지운다
sed '2,6d' app.log
```

```bash
2026-11-10 09:01:15 INFO  order-api started
2026-11-10 11:30:00 INFO  heartbeat
```

```bash
# $d: 마지막 줄만 지운다
sed '$d' app.log
```

```bash
2026-11-10 09:01:15 INFO  order-api started
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:14:41 WARN  retrying orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
2026-11-10 10:06:01 error db connection reset
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
```

```bash
# /패턴/!d: 패턴이 없는 줄을 지운다. 결국 패턴이 든 줄만 남는다
sed '/INFO/!d' app.log
```

```bash
2026-11-10 09:01:15 INFO  order-api started
2026-11-10 11:30:00 INFO  heartbeat
```

### 앞쪽만 읽고 멈추기

> `q` 는 지금 줄을 찍고 끝냅니다.

큰 파일의 앞부분만 볼 때 `head` 처럼 씁니다.

```bash
# q: 3행을 찍은 뒤 끝낸다
sed 3q app.log
```

```bash
2026-11-10 09:01:15 INFO  order-api started
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:14:41 WARN  retrying orderId=1001
```

```bash
# {p;q}: { } 로 명령 둘을 묶어 3행만 찍고 곧바로 끝낸다
sed -n '3{p;q}' app.log  # 2026-11-10 09:14:41 WARN  retrying orderId=1001
```

```bash
# =: 맞은 줄 앞에 줄 번호를 따로 한 줄로 찍는다
sed -n '/ERROR/{=;p}' app.log
```

```bash
2
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
4
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
6
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
```

### s 명령으로 바꾸기

> `s/찾을 것/바꿀 것/` 은 줄마다 첫 일치만 바꾸고 끝에 `g` 를 붙이면 모든 일치를 바꿉니다.

`I` 는 GNU 확장이고 `s` 뒤의 구분자는 `/` 가 아니어도 됩니다.[^sed-s]

```bash
# 기본: 줄마다 첫 일치만 바꾼다
echo 'foo Foo foo' | sed 's/foo/bar/'  # bar Foo foo

# g 플래그: 줄 안 모든 일치를 바꾼다
echo 'foo Foo foo' | sed 's/foo/bar/g'  # bar Foo bar

# I 플래그: 대소문자를 가리지 않는다. g 와 함께 gI
echo 'foo Foo foo' | sed 's/foo/bar/gI'  # bar bar bar

# 구분자를 | 로 바꿔 경로처럼 / 가 든 값에서 / 를 이스케이프하지 않는다
echo '/usr/local/bin' | sed 's|/usr/local|/opt|'  # /opt/bin
```

숫자 플래그 `N` 에 `g` 를 함께 쓰면 GNU sed 는 N 번째 이후 모든 일치를 바꿉니다.[^sed-s]

```bash
# N 플래그: 줄 안에서 둘째 일치만 바꾼다
echo 'foo Foo foo' | sed 's/foo/bar/2'  # foo Foo bar

# Ng 플래그: 둘째 일치부터 끝까지 바꾼다
echo 'foo Foo foo foo' | sed 's/foo/bar/2g'  # foo Foo bar bar
```

```bash
# -n 과 p 플래그: 바꾼 줄을 찍는다. 바꾼 줄만 한 번 나온다
echo 'foo Foo foo' | sed -n 's/foo/bar/gp'  # bar Foo bar

# -n 없이 p 플래그: 자동 출력과 겹쳐 두 번 찍힌다
echo 'foo Foo foo' | sed 's/foo/bar/gp'
```

```bash
bar Foo bar
bar Foo bar
```

바꿀 자리의 `&` 는 맞은 부분 전체를, `\1`·`\2` 는 괄호로 묶은 부분을 가리킵니다.[^sed-s]

```bash
# &: 맞은 부분 전체. 숫자 둘레에 [ ] 를 두른다. \+ 는 한 번 이상(GNU BRE)
echo 'orderId=1001' | sed 's/[0-9]\+/[&]/'  # orderId=[1001]

# \1 \2 되참조(BRE): 기본 정규식에서는 괄호를 \( \) 로 묶어 앞뒤를 맞바꾼다
echo 'name=app' | sed 's/\(.*\)=\(.*\)/\2=\1/'  # app=name
```

`-r` 은 `-E` 와 같은 옵션이고 POSIX 에 들어간 이름은 `-E` 입니다.[^sed-opt]

```bash
# -E 를 주면 ( ) 로 묶고 \1 로 되참조한다
#   -E   확장 정규식(ERE)을 켜서 역슬래시를 줄여 준다 (-r, --regexp-extended)
echo 'name=app' | sed -E 's/^([^=]+)=(.*)$/\2=\1/'  # app=name

# -E 없이 +: 글자 + 를 찾으므로 바뀌지 않는다
echo 'a1b22' | sed 's/[0-9]+/N/g'  # a1b22

# -E 와 +: 한 번 이상 반복으로 읽는다
echo 'a1b22' | sed -E 's/[0-9]+/N/g'  # aNbN
```

```bash
# 쉼표를 공백으로
sed 's/,/ /g' names.csv
```

```bash
kim minsu 30
lee jiwon 25
park hana 41
```

```bash
# 첫 두 칸을 되참조해 "이름 성" 순서로
sed -E 's/^([^,]+),([^,]+),.*/\2 \1/' names.csv
```

```bash
minsu kim
jiwon lee
hana park
```

### 명령 여럿을 한 번에

> 한 줄에 명령 둘 이상이 필요하면 `-e` 를 여러 번 주거나 `;` 로 잇습니다.

`;` 는 단순한 명령을 나누는 구분자입니다.[^sed-opt]

```bash
# 스크립트 둘이 차례로 적용돼 HI ALL 이 된다
#   -e   스크립트를 여러 번 준다 (--expression)
echo 'hello world' | sed -e 's/hello/HI/' -e 's/world/ALL/'  # HI ALL

# ; 로 한 스크립트 안에서 잇기
echo 'hello world' | sed 's/hello/HI/; s/world/ALL/'  # HI ALL

# 긴 이름은 --expression=스크립트
echo 'hello world' | sed --expression='s/hello/HI/' --expression='s/world/ALL/'  # HI ALL

# -e p: 바꾼 뒤 p 를 더해 -n 과 함께 쓴다
echo 'hello world' | sed \
  -n \
  -e 's/hello/HI/' \
  -e p
# HI world
```

### 줄 넣기와 줄 끝 다듬기

> `i\` 는 그 줄 앞에, `a\` 는 그 줄 뒤에, `c\` 는 그 줄을 통째로 바꿔 넣습니다.

표준 꼴은 `a\` 뒤에서 줄을 바꿔 텍스트를 적고 GNU sed 는 `2a NEW` 처럼 한 줄에 적는 꼴도 받습니다.[^sed-a] 아래 예처럼 `\` 바로 뒤에 텍스트를 붙여도 GNU sed 는 같은 결과를 냅니다.

```bash
# 결과를 한 줄에 모아 보이려고 줄을 공백으로 이어 붙인다
#   paste -s   파일 하나씩 이어 붙여 입력의 줄을 한 줄로 모은다 (--serial)
#   paste -d   TAB 대신 LIST 의 글자로 잇는다. -d' ' 은 공백이다 (--delimiters)

# 2행 앞에 넣기(i)
printf 'a\nb\nc\n' | sed '2i\NEW' | paste -sd' '  # a NEW b c

# 2행 뒤에 넣기(a)
printf 'a\nb\nc\n' | sed '2a\NEW' | paste -sd' '  # a b NEW c

# 2행을 NEW 로 바꾸기(c)
printf 'a\nb\nc\n' | sed '2c\NEW' | paste -sd' '  # a NEW c

# 1i: 맨 앞 줄에 헤더, $a: 파일 끝에 줄을 덧붙여 푸터
printf 'a\nb\nc\n' \
  | sed -e '1i\# header' -e '$a\# footer' \
  | paste -sd' '
# # header a b c # footer
```

```bash
# 줄 끝 공백 셋이 지워져 abc 바로 뒤에 줄 끝 $ 가 온다
#   cat -A   -vET 와 같다. 줄 끝을 $ 로 보인다 (--show-all)
printf 'abc   \n' | sed 's/[[:space:]]*$//' | cat -A  # abc$
```

### 글자 하나씩 바꾸는 y

> `y/원본/대상/` 은 `s` 와 달리 글자 하나하나를 같은 자리의 글자로 바꿉니다.

정규식이 아니라 글자 목록이고 두 목록의 길이가 같아야 합니다.[^sed-y]

```bash
# y: a-j 가 대문자로. 글자 목록이라 범위 a-j 를 쓸 수 없고 모두 적는다
echo 'hello' | sed 'y/abcdefghij/ABCDEFGHIJ/'  # HEllo

# y: - 와 _ 를 모두 공백으로
echo 'a-b_c' | sed 'y/-_/  /'  # a b c
```

### 설정 파일을 제자리에서 고치기

> 결과를 먼저 확인하고 `-i.bak` 으로 원본을 남긴 채 고칩니다.

`sed` 는 결과를 `stdout` 으로 낼 뿐 파일은 그대로 둡니다. `-i` 에 접미사를 주지 않으면 원본을 백업 없이 덮어써서 되돌릴 길이 없습니다.[^sed-i]

```bash
# -i 없이: 파일은 그대로 두고 바뀔 결과만 본다
# ^#? 는 줄 맨 앞에 # 가 있어도 없어도 맞아 주석 처리된 줄과 풀린 줄을 한 번에 맞춘다
#   grep -n   출력 줄 앞에 줄 번호를 붙인다 (--line-number)
sed -E 's/^#?PermitRootLogin.*/PermitRootLogin no/' sshd_config \
  | grep -n PermitRootLogin
# 4:PermitRootLogin no
```

```bash
# 결과가 맞으면 원본을 sshd_config.bak 으로 남기고 직접 수정한다
#   -i[SUFFIX]   파일을 제자리에서 고친다. SUFFIX 를 주면 원본을 남긴다 (--in-place[=SUFFIX])
sed -i.bak -E 's/^#?PermitRootLogin.*/PermitRootLogin no/' sshd_config
ls sshd_config*
```

```bash
sshd_config
sshd_config.bak
```

```bash
# 백업과 고친 파일의 차이
diff sshd_config.bak sshd_config
```

```bash
4c4
< #PermitRootLogin prohibit-password
---
> PermitRootLogin no
```

접미사는 `-i` 에 바로 붙여 씁니다. `-Ei` 는 `-E -i` 이지만 `-iE` 는 접미사 `E` 로 읽혀 `sshd_configE` 라는 백업이 생깁니다.[^sed-i]

```bash
# -i (백업 없음): 접미사 없이 쓰면 백업 없이 원본을 덮어쓴다. 연습용 사본 f2.txt 를 직접 고친다
cp fruits.txt f2.txt; sed -i 's/apple/APPLE/' f2.txt; cat f2.txt
```

```bash
APPLE pie
banana split
APPLE tart
cherry cake
```

고치기 전 원본인 `sshd_config.bak` 에 돌리면 들여 쓴 주석이 남습니다. 그 줄은 `#` 가 아니라 공백으로 시작하기 때문이며 [grep 참조 시트](./grep.md)의 `-vE` 예가 이 줄까지 거릅니다.

```bash
# # 로 시작하는 줄과 빈 줄을 d 로 지운다
sed '/^#/d; /^$/d' sshd_config.bak
```

```bash
Port 22
PasswordAuthentication yes
  # indented comment
X11Forwarding no
```

```bash
# 줄 전체를 바꾸고 && 로 이어 바뀐 줄을 곧바로 확인한다
sed -i 's/^X11Forwarding.*/X11Forwarding yes/' sshd_config \
  && grep X11 sshd_config
# X11Forwarding yes
```



## 주의사항과 동작 원리

> `-n` 과 `-i` 를 함께 쓰면서 `p` 를 빼면 자동 출력이 꺼진 채 파일이 쓰입니다.

### -n 과 -i 를 함께 쓸 때의 위험

> `p` 없이 `-ni` 를 쓰면 파일 내용이 모두 사라집니다.

매뉴얼도 `-n` 과 `-i` 를 함께 쓸 때 조심하라고 적습니다.[^sed-i] 연습용 사본에서 확인합니다.

```bash
# -ni 와 p 없음: 자동 출력이 꺼져 출력이 빈 파일로 덮어 쓰인다
#   wc -c   바이트 수를 센다 (--bytes)
cp fruits.txt f3.txt; sed -ni 's/apple/APPLE/' f3.txt; wc -c f3.txt  # 0 f3.txt
```



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [grep 참조 시트](./grep.md) — 들여 쓴 주석까지 거르는 `grep -vE`
- [tr 참조 시트](./tr.md) — 글자 하나씩 바꾸고 지우는 짝 도구
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- GNU sed 4.9 의 `sed --help` 원문 — Debian 12 컨테이너에서 2026-11-13 출력
- [GNU sed 매뉴얼](https://www.gnu.org/software/sed/manual/sed.html) — 2026-11-11 조회

[^sed-cycle]: GNU sed 매뉴얼, "How sed Works". <https://www.gnu.org/software/sed/manual/sed.html#Execution-Cycle>
[^sed-addr]: GNU sed 매뉴얼, "Addresses" — "addr1,+N: Matches addr1 and the N lines following addr1", "first~step: This GNU extension matches every stepth line starting with line first". <https://www.gnu.org/software/sed/manual/sed.html#Addresses-overview>
[^sed-s]: GNU sed 매뉴얼, "The s Command" — "The / characters may be uniformly replaced by any other single character within any given s command", "The I modifier to regular-expression matching is a GNU extension", "Only replace the numberth match of the regexp", "ignore matches before the numberth, and then match and replace all matches from the numberth on", "the replacement can contain unescaped & characters which reference the whole matched portion of the pattern space". <https://www.gnu.org/software/sed/manual/sed.html#The-_0022s_0022-Command>
[^sed-opt]: GNU sed 매뉴얼, "Command-Line Options" — "-n, --quiet, --silent: These options disable this automatic printing", "-E, -r, --regexp-extended: Use extended regular expressions rather than basic regular expressions", "the -E extension has since been added to the POSIX standard". <https://www.gnu.org/software/sed/manual/sed.html#Command_002dLine-Options> 같은 매뉴얼 "Multiple commands syntax" — "A semicolon (;) may be used to separate most simple commands". <https://www.gnu.org/software/sed/manual/sed.html#Multiple-commands-syntax>
[^sed-a]: GNU sed 매뉴얼, "Less Frequently-Used Commands" 의 `a text` — "This is a GNU extension to the standard a command". <https://www.gnu.org/software/sed/manual/sed.html#Other-Commands>
[^sed-y]: GNU sed 매뉴얼, "Less Frequently-Used Commands" 의 `y/source-chars/dest-chars/` — "Transliterate any characters in the pattern space which match any of the source-chars with the corresponding character in dest-chars". <https://www.gnu.org/software/sed/manual/sed.html#Other-Commands>
[^sed-i]: GNU sed 매뉴얼, "Command-Line Options" 의 `-i[SUFFIX]` — "If no extension is supplied, the original file is overwritten without making a backup", "sed -iE '...' FILE: This is equivalent to --in-place=E, creating FILEE as backup of FILE", "Be cautious of using -n with -i". <https://www.gnu.org/software/sed/manual/sed.html#Command_002dLine-Options>
[^sed-exit]: GNU sed 매뉴얼, "Exit status" — "An exit status of zero indicates success, and a nonzero value indicates failure", 2 는 입력 파일을 읽을 수 없을 때. <https://www.gnu.org/software/sed/manual/sed.html#Exit-status>
[^sed-addr-list]: GNU sed 4.9 매뉴얼(Debian 12 의 `info sed`), "sed addresses" — "Specifying a line number will match only that line in the input", "This address matches the last line of the last file of input", "This will select any line which matches the regular expression REGEXP", "The I modifier to regular-expression matching is a GNU extension which causes the REGEXP to be matched in a case-insensitive manner", "If the second address is a REGEXP, then checking for the ending match will start with the line following the line which matched the first address", "Appending the ! character to the end of an address specification (before the command letter) negates the sense of the match". `N,M` 은 같은 절 "Range Addresses" 의 `sed -n '4,6p'` 예가 4, 5, 6 행을 찍습니다. <https://www.gnu.org/software/sed/manual/sed.html#sed-addresses>
[^sed-cmds]: GNU sed 4.9 매뉴얼(Debian 12 의 `info sed`), "sed commands summary" — `p` "Print the pattern space", `d` "Delete the pattern space; immediately start next cycle", `q` "(quit) Exit sed without processing any more commands or input", `=` "Print the current input line number (with a trailing newline)", `{ CMD ; CMD ... }` "Group several commands together", `s` "(substitute) Match the regular-expression against the content of the pattern space. If found, replace matched string with REPLACEMENT", `i` "insert TEXT before a line", `a` "Append TEXT after a line", `c` "Replace (change) lines with TEXT". <https://www.gnu.org/software/sed/manual/sed.html#sed-commands-list>
[^sed-flags]: GNU sed 4.9 매뉴얼(Debian 12 의 `info sed`), "The s Command" — `g` "Apply the replacement to all matches to the REGEXP, not just the first", `NUMBER` "Only replace the NUMBERth match of the REGEXP", `p` "If the substitution was made, then print the new pattern space", `I` "The I modifier to regular-expression matching is a GNU extension". <https://www.gnu.org/software/sed/manual/sed.html#The-_0022s_0022-Command>
[^sed-exit-codes]: GNU sed 4.9 매뉴얼(Debian 12 의 `info sed`), "Exit status" — "An exit status of zero indicates success", 1 은 "Invalid command, invalid syntax, invalid regular expression or a GNU sed extension command used with --posix", 2 는 "One or more of the input file specified on the command line could not be opened", 4 는 "An I/O error, or a serious processing error during runtime, GNU sed aborted immediately", "the commands q and Q can be used to terminate sed with a custom exit code value (this is a GNU sed extension)". <https://www.gnu.org/software/sed/manual/sed.html#Exit-status>
