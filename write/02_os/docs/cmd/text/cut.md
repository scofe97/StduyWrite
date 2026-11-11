---
title: cut 참조 시트
tags: [linux, cheatsheet, cut, cli, reference]
status: draft
source:
  - GNU coreutils 매뉴얼
related:
  - ../README.md
updated: 2026-11-11
---

# cut 참조 시트

---

> `cut` 으로 구분자나 글자 위치로 칸을 자르는 법을 옵션별 예제로 모은 조회용 시트입니다.

## 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 파일이 모두 생깁니다.

macOS 기본 `cut` 은 GNU 판이 아니어서 `--complement`·`--output-delimiter` 가 없고 한글 처리도 다릅니다. OrbStack 의 Linux VM 이나 `docker run -it --rm debian:12` 안에서 실행합니다.

```bash
mkdir -p ~/cmd-lab/cut && cd ~/cmd-lab/cut
cat > app.log << 'EOF'
2026-11-10 09:01:15 INFO  order-api started
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:14:41 WARN  retrying orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
2026-11-10 10:06:01 error db connection reset
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
2026-11-10 11:30:00 INFO  heartbeat
EOF
cat > passwd.txt << 'EOF'
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
dev:x:1000:1000::/home/dev:/bin/sh
svc:x:1001:1001::/home/svc:/usr/sbin/nologin
EOF
cat > users.csv << 'EOF'
id,name,city,score
1,kim,seoul,90
2,lee,busan,85
3,park,daegu,70
EOF
cat > mixed.txt << 'EOF'
web1:80:up
no-colon-line
db1:5432:down
EOF
cat > hangul.txt << 'EOF'
가나다abc
한글:테스트:끝
EOF
cat > df.txt << 'EOF'
Filesystem     1024-blocks      Used Available Capacity Mounted on
/dev/sda1         41152736  17283548  21755756      45% /
/dev/sdb1        103081248  97927188         0     100% /data
/dev/sdc1         51474912  46327424   2509728      95% /var/log
tmpfs              8139112         0   8139112       0% /dev/shm
EOF
```

`app.log` 는 일곱 줄짜리 애플리케이션 로그입니다.

`passwd.txt` 는 `/etc/passwd` 꼴 네 줄로 일곱 칸이 `:` 로 나뉘고 `dev` 와 `svc` 는 다섯째 칸이 비어 있습니다.

`users.csv` 는 머리글과 세 줄짜리 쉼표 구분 표입니다. `mixed.txt` 는 `:` 가 없는 줄이 하나 섞인 세 줄입니다. `hangul.txt` 는 한글이 든 두 줄이고 `df.txt` 는 `df -P` 출력 꼴로 칸을 공백으로 맞춘 다섯 줄입니다.



## 1. 구분자와 글자 위치로 자르기

> `-d` 와 `-f` 로 구분자와 칸 번호를, `-c` 로 글자 위치를 줍니다. 공백 정렬 출력에서는 빈 칸이 생겨 `awk` 가 맞습니다.

단순 구분자 분리에는 `cut` 을 씁니다. 글자 위치로 자를 때는 `-c` 를 줍니다.[^cut]

```bash
cut -d: -f1,7 passwd.txt | head -2              # : 로 나눠 1·7번째 칸
```

```bash
root:/bin/bash
daemon:/usr/sbin/nologin
```

```bash
cut -c1-10 app.log | head -1                     # 2026-11-10
```

### 구분자와 칸 번호

`-f` 는 칸 번호를 받고 `-d` 는 칸 경계로 쓸 글자를 받습니다. `-d` 를 빼면 구분자는 탭입니다. 구분자는 글자 하나여야 합니다.

```bash
# -d (--delimiter): 칸을 가르는 글자. -f (--fields): 뽑을 칸 번호
cut -d: -f1 passwd.txt
```

```bash
root
daemon
dev
svc
```

```bash
# -d 는 쉼표 같은 다른 글자도 된다. 둘째·넷째 칸
cut -d, -f2,4 users.csv
```

```bash
name,score
kim,90
lee,85
park,70
```

```bash
# -d 를 빼면 구분자가 탭이다. 탭이 없는 줄은 통째로 나온다
cut -f1 passwd.txt | head -2
```

```bash
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
```

```bash
# 탭으로 나뉜 줄이면 -d 없이도 된다
printf 'a\tb\tc\n' | cut -f2      # b
# 구분자를 두 글자로 주면 오류다
cut -d'::' -f1 passwd.txt          # cut: the delimiter must be a single character
```

### 칸 번호를 고르는 꼴

번호는 하나, 쉼표로 이은 여럿, 범위, 열린 범위로 줍니다. 번호는 1부터 셉니다.

```bash
# -f N,M: 칸을 따로 고른다. 첫째와 일곱째
cut -d: -f1,7 passwd.txt | head -1      # root:/bin/bash

# -f N-M: 범위. 셋째에서 다섯째까지 (다섯째는 dev·svc 에서 빈 칸)
cut -d: -f3-5 passwd.txt
```

```bash
0:0:root
1:1:daemon
1000:1000:
1001:1001:
```

```bash
# -f N-: N번째부터 끝까지
cut -d: -f5- passwd.txt
```

```bash
root:/root:/bin/bash
daemon:/usr/sbin:/usr/sbin/nologin
:/home/dev:/bin/sh
:/home/svc:/usr/sbin/nologin
```

```bash
# -f -M: 처음부터 M번째까지 (1-M 과 같다)
cut -d: -f-2 passwd.txt | head -2
```

```bash
root:x
daemon:x
```

번호를 쓴 순서는 출력 순서가 아닙니다. 고른 칸은 입력에 나온 순서로 한 번씩만 나옵니다.

```bash
# -f3,1 은 3번 먼저가 아니라 1번 먼저 나온다
cut -d: -f3,1 passwd.txt | head -1      # root:0

# -f1,1 처럼 겹쳐도 한 번만 나온다
cut -d: -f1,1 passwd.txt | head -1      # root
```

### 구분자 없는 줄

`-f` 는 구분자가 없는 줄을 건드리지 않고 그대로 내보냅니다. 머리글이나 잡음 줄을 거르고 싶으면 `-s` 를 줍니다.[^cut]

```bash
# -f 만: 구분자 없는 줄(no-colon-line)이 그대로 섞여 나온다
cut -d: -f2 mixed.txt
```

```bash
80
no-colon-line
5432
```

```bash
# -s (--only-delimited): 구분자가 없는 줄은 버린다
cut -s -d: -f2 mixed.txt
```

```bash
80
5432
```

### 뺄 칸과 출력 구분자

`--complement` 는 고른 칸을 빼고 나머지를 냅니다. `--output-delimiter` 는 출력에서 칸 사이에 넣을 문자열을 바꿉니다. 둘 다 GNU 확장입니다.[^cut]

```bash
# --complement: 고른 칸의 나머지. 둘째에서 일곱째를 빼면 첫 칸만 남는다
cut -d: --complement -f2-7 passwd.txt
```

```bash
root
daemon
dev
svc
```

```bash
# --complement: 첫째와 일곱째를 뺀 가운데 칸들
cut -d: --complement -f1,7 passwd.txt | head -2
```

```bash
x:0:0:root:/root
x:1:1:daemon:/usr/sbin
```

```bash
# --output-delimiter: 출력 칸 사이 문자열. 두 글자 이상도 된다
cut -d: -f1,3 --output-delimiter=' => ' passwd.txt
```

```bash
root => 0
daemon => 1
dev => 1000
svc => 1001
```

```bash
# 입력은 쉼표, 출력은 탭으로 바꾼다. $'\t' 는 bash 의 탭 표기
cut -d, -f1,3 --output-delimiter=$'\t' users.csv
```

```bash
id	city
1	seoul
2	busan
3	daegu
```

### 글자 위치로 자르기

고정 폭 필드나 날짜처럼 위치가 일정한 줄은 `-c` 로 자릅니다. 칸 번호와 같은 꼴의 목록을 줍니다.

```bash
# -c (--characters): 글자 위치. 1~10번째 글자
cut -c1-10 app.log | head -2
```

```bash
2026-11-10
2026-11-10
```

```bash
# -c N-M: 시각만. 12~19번째
cut -c12-19 app.log | head -2
```

```bash
09:01:15
09:14:40
```

```bash
# -c N-: 21번째부터 끝까지
cut -c21- app.log | head -2
```

```bash
INFO  order-api started
ERROR payment timeout orderId=1001
```

```bash
# -c N,M: 위치를 따로 고른다. 1번째와 12번째 글자
cut -c1,12 app.log | head -1      # 20

# 목록을 여럿 주면 그 사이에 --output-delimiter 문자열이 들어간다
cut -c1-4,12-16 --output-delimiter=' | ' app.log | head -1      # 2026 | 09:01
```

### 한글과 -c 의 바이트 동작

이 시트의 환경인 coreutils 9.1 에서는 `-c` 가 글자가 아니라 바이트를 셉니다. 한글은 UTF-8 에서 한 글자가 3바이트라서 `-c1-3` 은 세 글자가 아니라 한 글자만 나옵니다. 로캘을 `C.UTF-8` 로 바꿔도 같았습니다. 9.1 매뉴얼도 `-c` 가 지금은 `-b` 와 같다고 적습니다. `-c` 가 글자를 세게 된 것은 coreutils 9.11 부터입니다.[^cut-c]

```bash
# -b (--bytes): 바이트 위치. 한글 한 글자는 3바이트라서 1~3바이트가 첫 글자 하나다
cut -b1-3 hangul.txt
```

```bash
가
한
```

```bash
# -c 도 같다. 세 글자(가나다)가 아니라 한 글자(가)만 나온다
cut -c1-3 hangul.txt
```

```bash
가
한
```

```bash
# 3의 배수가 아닌 끝을 주면 글자가 중간에서 잘려 깨진 바이트가 나온다. 16진수로 본다
cut -b1-2 hangul.txt | od -An -tx1
```

```bash
 ea b0 0a ed 95 0a
```

한글이 섞인 줄을 위치로 자를 때는 `cut` 대신 칸 구분자를 쓰거나 `awk` 의 `substr` 을 씁니다. `-d` 와 `-f` 는 구분자 글자를 찾는 방식이라 한글이 있어도 그대로 됩니다.

```bash
# 구분자 기준은 한글이 있어도 된다
cut -d: -f2 hangul.txt
```

```bash
가나다abc
테스트
```

첫 줄에는 `:` 가 없어서 통째로 나왔습니다. `-s` 를 주면 이 줄이 빠집니다.

### 연속 공백에서 생기는 빈 칸

`cut` 은 구분자 하나를 칸 경계 하나로 세지만 `awk` 는 연속 공백을 구분자 하나로 묶습니다.[^gawk-fields]

```bash
# cut: 공백 둘 사이에 빈 칸이 생겨 둘째 칸이 비었다
echo 'a  b' | cut -d' ' -f2         # 빈 줄

# awk: 연속 공백을 하나로 묶어 둘째 칸이 b
echo 'a  b' | awk '{print $2}'      # b
```

공백 둘 사이에 빈 칸이 하나 끼어 있으므로 `b` 는 셋째 칸입니다. `df.txt` 처럼 칸을 공백으로 맞춘 출력은 칸 수가 줄마다 달라 `-f` 번호를 믿을 수 없습니다.

```bash
# 공백이 둘인 줄에서는 셋째 칸이 b 다
echo 'a  b' | cut -d' ' -f3         # b

# df.txt 의 둘째 칸은 비어 있다. cat -A 는 줄 끝을 $ 로 보여 준다
cut -d' ' -f2 df.txt | head -2 | cat -A
```

```bash
$
$
```

`tr -s ' '` 로 연속 공백을 하나로 줄인 뒤 `cut` 에 넘기면 칸 번호가 맞습니다. 사용법은 [tr 참조 시트](./tr.md)에 있습니다.

```bash
# tr -s ' ': 연속 공백을 하나로 줄인 뒤 첫째·다섯째 칸
tr -s ' ' < df.txt | cut -d' ' -f1,5 | head -3
```

```bash
Filesystem Capacity
/dev/sda1 45%
/dev/sdb1 100%
```

그래서 공백으로 줄을 맞춘 출력에는 `awk` 가 맞습니다. 사용법은 [awk 참조 시트](./awk.md)에 있습니다.



## 관련 문서

- [awk 참조 시트](./awk.md) — 연속 공백을 하나로 묶는 칸 나누기
- [tr 참조 시트](./tr.md) — `-s` 로 연속 공백을 하나로 줄이기



## 참고 자료

- [GNU coreutils 매뉴얼, cut invocation](https://www.gnu.org/software/coreutils/manual/coreutils.html#cut-invocation) — 2026-11-11 조회

[^cut]: GNU coreutils 매뉴얼, "cut invocation" — "-f … Also print any line that contains no delimiter character, unless the --only-delimited (-s) option is specified", "the selected input is written in the same order that it is read, and is written exactly once", "--complement: This option is a GNU extension". 조회한 매뉴얼은 최신판(9.12)이고 `-c` 를 글자 위치로 설명하지만, 이 시트의 출력은 coreutils 9.1 이며 거기서는 `-c` 가 바이트처럼 동작했습니다. <https://www.gnu.org/software/coreutils/manual/html_node/cut-invocation.html>
[^cut-c]: coreutils 9.1 매뉴얼, "cut invocation" 의 `-c` — "The same as -b for now, but internationalization will change that". coreutils NEWS, 9.11 — "'cut' now supports multi-byte input and delimiters. Consequently the -c option is now honored, and no longer an alias for -b". <https://github.com/coreutils/coreutils/blob/v9.1/doc/coreutils.texi>, <https://github.com/coreutils/coreutils/blob/master/NEWS>
[^gawk-fields]: GNU awk 매뉴얼, "Specifying How Fields Are Separated" — "Fields are separated by runs of whitespace". <https://www.gnu.org/software/gawk/manual/gawk.html#Field-Separators>
