---
title: sed 참조 시트
tags: [linux, cheatsheet, sed, cli, reference]
status: draft
source:
  - GNU sed 매뉴얼
related:
  - ../README.md
updated: 2026-11-11
---

# sed 참조 시트

---

> `sed` 로 줄을 고르고 바꾸고 설정 파일을 고치는 법을 옵션과 명령마다 따라 치면 그대로 나오는 예제로 모은 조회용 시트입니다.

## 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 파일이 모두 생깁니다.

macOS 기본 `sed` 는 GNU 판이 아니어서 `-i` 의 인자 규칙과 `\+`·`1~3` 같은 확장이 다르게 동작합니다. OrbStack 의 Linux VM 이나 `docker run -it --rm debian:12` 안에서 실행합니다.

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



## 1. 한 줄씩 읽고 찍기

> `sed` 는 한 줄을 읽어 명령을 적용하고 찍는 일을 줄마다 되풀이합니다. `-n` 과 `p` 를 함께 쓰면 원하는 줄만 고릅니다.

`sed` 는 입력을 한 줄씩 읽어 명령을 적용하고 그 줄을 찍은 뒤 다음 줄로 넘어갑니다. `-n` 은 이 자동 출력을 끄고 `p` 는 지금 줄을 찍습니다.[^sed-cycle] 아래 첫 예는 자동 출력만 켠 상태라 바꾼 줄도 안 바꾼 줄도 나옵니다.

```bash
# 자동 출력: 바꾼 줄도 안 바꾼 줄도 나온다
printf 'apple\nbanana\n' | sed 's/apple/APPLE/'
```

```bash
APPLE
banana
```

`-n` 을 붙이면 자동 출력이 꺼져서 `p` 가 없는 `s` 는 아무것도 찍지 않습니다.

```bash
# -n (--quiet, --silent): 자동 출력을 끈다. p 가 없으니 출력이 없다
printf 'apple\nbanana\n' | sed -n 's/apple/APPLE/'  # 출력 없음

# -n 과 s 의 p 플래그: 바꾼 줄만 나온다
printf 'apple\nbanana\n' | sed -n 's/apple/APPLE/p'  # APPLE
```

### 줄 번호와 패턴으로 고르기

명령 앞에 주소를 두면 그 줄에만 명령이 듭니다. 줄 번호 하나, `N,M` 범위, 마지막 줄 `$`, 정규식이 모두 주소가 됩니다. 줄을 고를 때는 `-n` 과 `p` 를 함께 씁니다.

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

패턴 둘을 쉼표로 이으면 첫 패턴이 나온 줄부터 둘째 패턴이 나온 줄까지 나옵니다. 둘째 자리에 `+N` 을 쓰면 첫 줄 뒤 N 줄까지, `first~step` 은 `first` 줄부터 `step` 줄 간격으로 고릅니다. 둘 다 GNU 확장입니다.[^sed-addr]

```bash
# /a/,/b/: WARN 이 나온 줄부터 reset 이 나온 줄까지
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

주소 뒤에 `!` 를 붙이면 맞지 않는 줄에 명령이 듭니다.

```bash
# !: INFO 가 아닌 줄만 찍는다
sed -n '/INFO/!p' app.log
```

```bash
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:14:41 WARN  retrying orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
2026-11-10 10:06:01 error db connection reset
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
```

맞은 줄에서 값만 뽑을 때는 앞부분을 지우고 남은 것을 찍습니다.

```bash
# s 로 앞부분을 지우고 p 로 찍는다
printf 'name=app\nversion=1.2.3\n' | sed -n 's/^version=//p'  # 1.2.3
```

### 줄 지우기

`d` 는 맞은 줄을 지우고 다음 줄로 넘어갑니다. 지운 줄은 자동 출력에도 나오지 않으므로 `-n` 이 필요 없습니다.

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

`q` 는 지금 줄을 찍고 끝냅니다. 큰 파일의 앞부분만 볼 때 `head` 처럼 씁니다. `=` 는 줄 번호를 찍는 명령이고 `{ }` 는 한 주소에 명령 여럿을 묶습니다.

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
# {p;q}: 3행만 찍고 곧바로 끝낸다
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



## 2. 바꾸고 넣기

> `s` 명령은 맞은 부분을 바꾸고 `i`, `a`, `c` 는 줄을 넣거나 바꿉니다.

### s 명령으로 바꾸기

바꾸기 `s/찾을 것/바꿀 것/` 은 줄마다 첫 일치만 바꾸고 끝에 `g` 를 붙이면 모든 일치를 바꿉니다. `gI` 의 `I` 는 대소문자를 가리지 않게 하는 GNU 확장입니다. `s` 뒤의 구분자는 `/` 가 아니어도 되므로 경로처럼 `/` 가 든 값을 바꿀 때는 다른 글자를 고릅니다.[^sed-s]

```bash
# 기본: 줄마다 첫 일치만 바꾼다
echo 'foo Foo foo' | sed 's/foo/bar/'  # bar Foo foo

# g 플래그: 줄 안 모든 일치를 바꾼다
echo 'foo Foo foo' | sed 's/foo/bar/g'  # bar Foo bar

# I 플래그: 대소문자를 가리지 않는다. g 와 함께 gI
echo 'foo Foo foo' | sed 's/foo/bar/gI'  # bar bar bar

# 구분자를 | 로 바꿔 / 를 이스케이프하지 않는다
echo '/usr/local/bin' | sed 's|/usr/local|/opt|'  # /opt/bin
```

숫자 플래그 `N` 은 줄 안에서 N 번째 일치만 바꿉니다. `g` 와 함께 쓰면 GNU sed 는 N 번째 이후 모든 일치를 바꿉니다.[^sed-s]

```bash
# N 플래그: 둘째 일치만 바꾼다
echo 'foo Foo foo' | sed 's/foo/bar/2'  # foo Foo bar

# Ng 플래그: 둘째 일치부터 끝까지 바꾼다
echo 'foo Foo foo foo' | sed 's/foo/bar/2g'  # foo Foo bar bar
```

`p` 플래그는 바꾼 줄을 찍습니다. `-n` 과 함께 써야 바꾼 줄만 한 번 나오고 `-n` 없이 쓰면 같은 줄이 두 번 찍힙니다.

```bash
# -n 과 p 플래그: 바꾼 줄만 한 번
echo 'foo Foo foo' | sed -n 's/foo/bar/gp'  # bar Foo bar

# -n 없이 p 플래그: 자동 출력과 겹쳐 두 번 찍힌다
echo 'foo Foo foo' | sed 's/foo/bar/gp'
```

```bash
bar Foo bar
bar Foo bar
```

바꿀 자리에서 `&` 는 맞은 부분 전체를, `\1`·`\2` 는 괄호로 묶은 부분을 가리킵니다. 기본 정규식(BRE)에서는 괄호를 `\( \)` 로 쓰고 `-E` 를 주면 `( )` 로 씁니다.[^sed-s]

```bash
# &: 맞은 부분 전체. 숫자 둘레에 [ ] 를 두른다. \+ 는 한 번 이상(GNU BRE)
echo 'orderId=1001' | sed 's/[0-9]\+/[&]/'  # orderId=[1001]

# \1 \2 되참조(BRE): 괄호를 \( \) 로 묶어 앞뒤를 맞바꾼다
echo 'name=app' | sed 's/\(.*\)=\(.*\)/\2=\1/'  # app=name
```

`-E` 는 확장 정규식(ERE)을 켜서 역슬래시를 줄여 줍니다. `-r` 과 `--regexp-extended` 는 같은 옵션이고 POSIX 에 들어간 이름은 `-E` 입니다.[^sed-opt] `-E` 없이 `+` 를 쓰면 문자 `+` 그대로로 읽혀 아무것도 바뀌지 않습니다.

```bash
# -E (-r, --regexp-extended): ( ) 로 묶고 \1 로 되참조한다
echo 'name=app' | sed -E 's/^([^=]+)=(.*)$/\2=\1/'  # app=name

# -E 없이 +: 글자 + 를 찾으므로 바뀌지 않는다
echo 'a1b22' | sed 's/[0-9]+/N/g'  # a1b22

# -E 와 +: 한 번 이상 반복으로 읽는다
echo 'a1b22' | sed -E 's/[0-9]+/N/g'  # aNbN
```

CSV 한 줄에서 칸을 골라 순서를 바꾸는 일도 같은 방식입니다.

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

한 줄에 명령 둘 이상이 필요하면 `-e` 를 여러 번 주거나 `;` 로 잇습니다. `;` 는 단순한 명령을 나누는 구분자입니다.[^sed-opt]

```bash
# -e (--expression): 스크립트를 여러 번 준다
echo 'hello world' | sed -e 's/hello/HI/' -e 's/world/ALL/'  # HI ALL

# ; 로 한 스크립트 안에서 잇기
echo 'hello world' | sed 's/hello/HI/; s/world/ALL/'  # HI ALL

# 긴 이름은 --expression=스크립트
echo 'hello world' | sed --expression='s/hello/HI/' --expression='s/world/ALL/'  # HI ALL

# -e p: 바꾼 뒤 p 를 더해 -n 과 함께 쓴다
echo 'hello world' | sed -n -e 's/hello/HI/' -e p  # HI world
```

### 줄 넣기와 줄 끝 다듬기

`i\` 는 그 줄 앞에, `a\` 는 그 줄 뒤에, `c\` 는 그 줄을 통째로 바꿔 넣습니다. 표준 꼴은 `a\` 뒤에서 줄을 바꿔 텍스트를 적고 GNU sed 는 `2a NEW` 처럼 한 줄에 적는 꼴도 받습니다.[^sed-a] 아래 예처럼 `\` 바로 뒤에 텍스트를 붙여도 GNU sed 는 같은 결과를 냅니다. `$a\` 는 파일 끝에 줄을 덧붙입니다. 아래 예는 결과를 한 줄에 모아 보이려고 `paste -sd' '` 로 줄을 공백으로 이어 붙입니다.

```bash
# 2행 앞에 넣기(i)
printf 'a\nb\nc\n' | sed '2i\NEW' | paste -sd' '  # a NEW b c

# 2행 뒤에 넣기(a)
printf 'a\nb\nc\n' | sed '2a\NEW' | paste -sd' '  # a b NEW c

# 2행을 NEW 로 바꾸기(c)
printf 'a\nb\nc\n' | sed '2c\NEW' | paste -sd' '  # a NEW c

# 1i: 맨 앞 줄에 헤더, $a: 맨 끝 줄에 푸터
printf 'a\nb\nc\n' | sed -e '1i\# header' -e '$a\# footer' | paste -sd' '  # # header a b c # footer
```

줄 끝 공백은 눈에 보이지 않으므로 `cat -A` 로 줄 끝을 `$` 로 드러내 확인합니다.

```bash
# 줄 끝 공백 지우기: cat -A 가 줄 끝을 $ 로 보인다
printf 'abc   \n' | sed 's/[[:space:]]*$//' | cat -A  # abc$
```

### 글자 하나씩 바꾸는 y

`y/원본/대상/` 은 `s` 와 달리 글자 하나하나를 같은 자리의 글자로 바꿉니다. 정규식이 아니라 글자 목록이고 두 목록의 길이가 같아야 합니다.[^sed-y]

```bash
# y: a-j 가 대문자로. 글자 목록이라 범위 a-j 를 쓸 수 없고 모두 적는다
echo 'hello' | sed 'y/abcdefghij/ABCDEFGHIJ/'  # HEllo

# y: - 와 _ 를 모두 공백으로
echo 'a-b_c' | sed 'y/-_/  /'  # a b c
```



## 3. 설정 파일을 제자리에서 고치기

> 결과를 먼저 확인하고 `-i.bak` 으로 원본을 남긴 채 고칩니다.

`sed` 는 결과를 `stdout` 으로 낼 뿐 파일은 그대로 둡니다. 제자리 수정은 되돌릴 길이 없으므로 먼저 `-i` 없이 결과를 확인하고 `-i.bak` 으로 원본을 남깁니다.[^sed-i]

```bash
# -i 없이: 파일은 그대로 두고 바뀔 결과만 본다
sed -E 's/^#?PermitRootLogin.*/PermitRootLogin no/' sshd_config | grep -n PermitRootLogin  # 4:PermitRootLogin no
```

`^#?` 는 줄 맨 앞에 `#` 가 있어도 없어도 맞으므로 주석 처리된 줄과 풀린 줄을 한 번에 맞춥니다. 결과가 맞으면 `-i.bak` 을 붙여 원본을 `sshd_config.bak` 으로 남기고 고칩니다.

```bash
# -i.bak (--in-place=.bak): 원본을 sshd_config.bak 으로 남기고 직접 수정한다
sed -i.bak -E 's/^#?PermitRootLogin.*/PermitRootLogin no/' sshd_config
ls sshd_config*
```

```bash
sshd_config
sshd_config.bak
```

백업과 고친 파일의 차이는 `diff` 로 확인합니다.

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

`-i` 뒤의 접미사 없이 쓰면 백업 없이 원본을 덮어씁니다. 접미사는 `-i` 에 바로 붙여 씁니다. `-Ei` 는 `-E -i` 이지만 `-iE` 는 접미사 `E` 로 읽혀 `sshd_configE` 라는 백업이 생깁니다.[^sed-i] 연습용 사본으로 `-i` 를 먼저 익힙니다.

```bash
# -i (백업 없음): 사본 f2.txt 를 직접 고친다
cp fruits.txt f2.txt; sed -i 's/apple/APPLE/' f2.txt; cat f2.txt
```

```bash
APPLE pie
banana split
APPLE tart
cherry cake
```

`-n` 과 `-i` 를 함께 쓰면서 `p` 를 빼면 자동 출력이 꺼진 채로 파일이 쓰여 내용이 모두 사라집니다.[^sed-i] 연습용 사본에서 확인합니다.

```bash
# -ni 와 p 없음: 자동 출력이 꺼져 출력이 빈 파일로 덮어 쓰인다
cp fruits.txt f3.txt; sed -ni 's/apple/APPLE/' f3.txt; wc -c f3.txt  # 0 f3.txt
```

`#` 로 시작하는 줄과 빈 줄은 `d` 로 지웁니다. 고치기 전 원본인 `sshd_config.bak` 에 돌리면 들여 쓴 주석이 남습니다. 그 줄은 `#` 가 아니라 공백으로 시작하기 때문이며 [grep 참조 시트](./grep.md)의 `-vE` 예가 이 줄까지 거릅니다.

```bash
sed '/^#/d; /^$/d' sshd_config.bak
```

```bash
Port 22
PasswordAuthentication yes
  # indented comment
X11Forwarding no
```

마지막으로 줄 전체를 바꾸는 한 줄짜리 `-i` 를 `&&` 로 이어 결과까지 확인하는 꼴입니다.

```bash
# 한 줄을 바꾸고 바뀐 줄을 곧바로 확인한다
sed -i 's/^X11Forwarding.*/X11Forwarding yes/' sshd_config && grep X11 sshd_config  # X11Forwarding yes
```

없는 파일을 주면 `sed` 는 오류 메시지를 stderr 로 내고 종료 상태 2 를 돌려줍니다.[^sed-exit]

```bash
# 없는 파일: 오류 메시지와 종료 상태 2
sed 's/a/A/' nofile.txt 2>&1; echo $?
```

```bash
sed: can't read nofile.txt: No such file or directory
2
```



## 관련 문서

- [grep 참조 시트](./grep.md) — 들여 쓴 주석까지 거르는 `grep -vE`
- [tr 참조 시트](./tr.md) — 글자 하나씩 바꾸고 지우는 짝 도구



## 참고 자료

- [GNU sed 매뉴얼](https://www.gnu.org/software/sed/manual/sed.html) — 2026-11-11 조회

[^sed-cycle]: GNU sed 매뉴얼, "How sed Works". <https://www.gnu.org/software/sed/manual/sed.html#Execution-Cycle>
[^sed-addr]: GNU sed 매뉴얼, "Addresses" — "addr1,+N: Matches addr1 and the N lines following addr1", "first~step: This GNU extension matches every stepth line starting with line first". <https://www.gnu.org/software/sed/manual/sed.html#Addresses-overview>
[^sed-s]: GNU sed 매뉴얼, "The s Command" — "The / characters may be uniformly replaced by any other single character within any given s command", "The I modifier to regular-expression matching is a GNU extension", "Only replace the numberth match of the regexp", "ignore matches before the numberth, and then match and replace all matches from the numberth on", "the replacement can contain unescaped & characters which reference the whole matched portion of the pattern space". <https://www.gnu.org/software/sed/manual/sed.html#The-_0022s_0022-Command>
[^sed-opt]: GNU sed 매뉴얼, "Command-Line Options" — "-n, --quiet, --silent: These options disable this automatic printing", "-E, -r, --regexp-extended: Use extended regular expressions rather than basic regular expressions", "the -E extension has since been added to the POSIX standard". <https://www.gnu.org/software/sed/manual/sed.html#Command_002dLine-Options> 같은 매뉴얼 "Multiple commands syntax" — "A semicolon (;) may be used to separate most simple commands". <https://www.gnu.org/software/sed/manual/sed.html#Multiple-commands-syntax>
[^sed-a]: GNU sed 매뉴얼, "Less Frequently-Used Commands" 의 `a text` — "This is a GNU extension to the standard a command". <https://www.gnu.org/software/sed/manual/sed.html#Other-Commands>
[^sed-y]: GNU sed 매뉴얼, "Less Frequently-Used Commands" 의 `y/source-chars/dest-chars/` — "Transliterate any characters in the pattern space which match any of the source-chars with the corresponding character in dest-chars". <https://www.gnu.org/software/sed/manual/sed.html#Other-Commands>
[^sed-i]: GNU sed 매뉴얼, "Command-Line Options" 의 `-i[SUFFIX]` — "If no extension is supplied, the original file is overwritten without making a backup", "sed -iE '...' FILE: This is equivalent to --in-place=E, creating FILEE as backup of FILE", "Be cautious of using -n with -i". <https://www.gnu.org/software/sed/manual/sed.html#Command_002dLine-Options>
[^sed-exit]: GNU sed 매뉴얼, "Exit status" — "An exit status of zero indicates success, and a nonzero value indicates failure", 2 는 입력 파일을 읽을 수 없을 때. <https://www.gnu.org/software/sed/manual/sed.html#Exit-status>
