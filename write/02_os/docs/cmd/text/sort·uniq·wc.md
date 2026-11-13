---
title: sort·uniq·wc 참조 시트
tags: [linux, cheatsheet, sort, uniq, wc, cli, reference]
status: draft
source:
  - GNU coreutils 매뉴얼
  - GNU coreutils sort·uniq·wc (`--help` 원문, coreutils 9.1)
related:
  - ../README.md
updated: 2026-11-13
---

# sort·uniq·wc 참조 시트

---

> `sort` 로 같은 줄을 붙이고 `uniq -c` 와 `wc` 로 세는 법을 코드와 주석으로 모은 조회용 시트입니다.

## 개요

> `sort` 는 줄을 정렬하고 `uniq` 는 이웃한 같은 줄을 합치며 `wc` 는 줄·단어·바이트 수를 셉니다.

세 명령은 모두 Debian 12 의 coreutils 패키지에 든 외부 바이너리입니다. 이 시트는 GNU 판(coreutils 9.1, Debian 12 컨테이너)으로 실측했습니다. macOS 의 `sort`·`uniq`·`wc` 는 GNU coreutils 가 아니어서 옵션 지원과 출력 서식이 조금 다릅니다. `sort` 의 정렬 순서와 `wc -m` 의 결과는 locale 에 따라 달라집니다.



## 핵심 문법

> 세 명령 모두 파일 이름을 받고, 파일 이름이 없으면 표준 입력을 읽습니다.

```bash
# 호출 형태
sort [OPTION]... [FILE]...
sort [OPTION]... --files0-from=F
uniq [OPTION]... [INPUT [OUTPUT]]
wc [OPTION]... [FILE]...
wc [OPTION]... --files0-from=F

# 정렬로 같은 줄을 이웃하게 붙인 뒤 합치거나 센다 (정렬로 같은 줄을 붙여 세기)
sort 파일 | uniq
sort 파일 | uniq -c

# 반복 여부로 거르거나 대소문자를 무시하고 센다 (반복된 줄 세고 거르기)
sort 파일 | uniq -d
sort 파일 | uniq -u
sort 파일 | uniq -D
sort -f 파일 | uniq -ic

# 정렬 기준을 숫자·크기·버전으로 바꾸고 순서를 뒤집는다 (정렬 키와 순서)
sort -n 파일
sort -r 파일
sort -h 파일
sort -V 파일

# 칸을 키로 삼아 정렬한다 (키와 구분자)
sort -t 구분자 -k 시작칸,끝칸 파일

# 같은 줄을 하나만 남기고 결과를 파일에 쓴다 (중복 제거와 제자리 저장)
sort -u 파일
sort -o 파일 파일

# 줄·단어·바이트 수를 센다 (줄·단어·바이트 수 세기)
wc 파일
wc -l 파일

# 바이트 수와 문자 수를 가른다 (바이트와 문자 수 구분하기)
wc -c 파일
wc -m 파일

# 여러 파일을 합계와 함께, 또는 표준 입력으로 센다 (여러 파일과 표준 입력)
wc 파일 파일
wc -l < 파일

# 다른 명령의 출력을 세어 많은 쪽부터 놓는다 (다른 명령과 이어 로그 세기)
다른 명령 | sort | uniq -c | sort -rn

# 정렬 순서를 환경과 무관하게 고정한다 (대소문자와 locale)
LC_ALL=C sort 파일
```



## 종료 코드

> `sort` 는 성공 0, `-c` 검사 실패 1, 오류 2 를 내고 `uniq` 와 `wc` 는 성공 0, 실패 1 을 냅니다.

매뉴얼은 `sort` 의 세 코드를 나누어 적고 `uniq`·`wc` 는 0 이 아닌 값이라고만 적습니다.[^sort-exit][^uniq-wc-exit] 아래 예는 「실습 준비」 에서 만든 파일로 돌립니다.

```bash
# sort
#   0  성공. -c 로 검사했다면 입력이 정렬돼 있다
#   1  -c 로 검사했는데 입력이 정렬돼 있지 않다
#   2  오류가 났다
# uniq, wc
#   0  성공
#   1  오류가 났다

# 정렬된 입력을 검사하면 출력 없이 0 이다
#   sort -c   이미 정렬됐는지만 검사한다 (--check)
printf 'a\nb\nc\n' | sort -c; echo $?            # 0

# 어긋나면 처음 어긋난 줄을 알리고 1 이다
sort -c words.txt; echo $?
```

```bash
sort: words.txt:2: disorder: Apple
1
```

```bash
# 없는 파일은 sort 에서 2, uniq 와 wc 에서 1 이다
sort nofile.txt; echo $?                # sort: cannot read: nofile.txt: No such file or directory / 2
uniq nofile.txt; echo $?                # uniq: nofile.txt: No such file or directory / 1
wc nofile.txt; echo $?                  # wc: nofile.txt: No such file or directory / 1

# 모르는 옵션
sort --bad; echo $?                     # sort: unrecognized option '--bad' / Try 'sort --help' for more information. / 2
wc --bad; echo $?                       # wc: unrecognized option '--bad' / Try 'wc --help' for more information. / 1
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션만 씁니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 파일이 모두 생깁니다.

OrbStack 의 Linux VM 이나 `docker run -it --rm debian:12` 안에서 실행합니다. 이 시트의 출력은 `LANG` 이 비어 있는(C locale) `debian:12` 컨테이너에서 받았습니다. 셸의 locale 이 `en_US.UTF-8` 이면 대소문자가 섞인 줄의 순서와 `wc -m` 결과가 달라집니다. 같은 출력을 보려면 `export LC_ALL=C` 를 먼저 실행합니다.

```bash
mkdir -p ~/cmd-lab/sort && cd ~/cmd-lab/sort

# access.log: 첫 칸이 클라이언트 IP 인 접근 로그 일곱 줄
# (「다른 명령과 이어 로그 세기」)
cat > access.log << 'EOT'
10.0.0.7 - - [10/Nov/2026:09:01:15] "GET /orders HTTP/1.1" 200 512
10.0.0.9 - - [10/Nov/2026:09:01:17] "GET /health HTTP/1.1" 200 15
10.0.0.7 - - [10/Nov/2026:09:02:03] "POST /orders HTTP/1.1" 201 87
10.0.0.3 - - [10/Nov/2026:09:03:44] "GET /orders/1001 HTTP/1.1" 404 0
10.0.0.7 - - [10/Nov/2026:09:04:10] "GET /orders HTTP/1.1" 200 512
10.0.0.9 - - [10/Nov/2026:09:05:01] "GET /health HTTP/1.1" 200 15
10.0.0.7 - - [10/Nov/2026:09:06:30] "GET /orders HTTP/1.1" 200 512
EOT

# app.log: 애플리케이션 로그 일곱 줄
# (「줄·단어·바이트 수 세기」, 「여러 파일과 표준 입력」, 「다른 명령과 이어 로그 세기」)
cat > app.log << 'EOT'
2026-11-10 09:01:15 INFO  order-api started
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:14:41 WARN  retrying orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
2026-11-10 10:06:01 error db connection reset
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
2026-11-10 11:30:00 INFO  heartbeat
EOT

# df.txt: df -P 출력 꼴. 다섯째 칸이 사용률이다 (「키와 구분자」)
cat > df.txt << 'EOT'
Filesystem     1024-blocks      Used Available Capacity Mounted on
/dev/sda1         41152736  17283548  21755756      45% /
/dev/sdb1        103081248  97927188         0     100% /data
/dev/sdc1         51474912  46327424   2509728      95% /var/log
tmpfs              8139112         0   8139112       0% /dev/shm
EOT

# members.csv: 이름·부서·나이를 쉼표로 나눈 네 줄. 나이 25 가 두 줄이다
# (「키와 구분자」)
cat > members.csv << 'EOT'
kim,dev,31
lee,ops,25
park,dev,45
choi,ops,25
EOT

# pairs.txt: 둘째 칸 값 1 이 겹치는 세 줄 (「키와 구분자」)
cat > pairs.txt << 'EOT'
a 1 z
b 1 y
c 0 x
EOT

# sizes.txt: 단위 접미사가 붙은 크기, versions.txt: 버전 번호
# (「정렬 키와 순서」)
cat > sizes.txt << 'EOT'
1.5G
200M
3K
12M
EOT
cat > versions.txt << 'EOT'
v1.10
v1.2
v1.9
v1.2.1
EOT

# words.txt: 대소문자가 섞인 단어 다섯 개
# (「종료 코드」, 「중복 제거와 제자리 저장」, 「대소문자와 locale」)
cat > words.txt << 'EOT'
banana
Apple
cherry
apple
Banana
EOT

# tags.txt: db 가 세 번, web 과 Web 이 섞인 여섯 줄
# (「정렬로 같은 줄을 붙여 세기」, 「반복된 줄 세고 거르기」)
cat > tags.txt << 'EOT'
db
web
db
Web
db
cache
EOT

# ko.txt: 한글 세 글자 한 줄 (「바이트와 문자 수 구분하기」)
cat > ko.txt << 'EOT'
가나다
EOT
```

`df -P` 는 장치 이름이 길어도 파일시스템 하나를 한 줄에 찍으므로 `df.txt` 의 다섯째 칸이 늘 사용률입니다.[^df] `members.csv` 는 나이 25 가 두 줄이라 같은 키일 때의 순서를 보기 좋습니다.

### 정렬로 같은 줄을 붙여 세기

> `sort` 로 같은 줄을 이웃하게 모은 뒤 `uniq` 로 합치거나 셉니다.

`uniq` 는 앞줄과 같은 줄만 합치므로 같은 값이 떨어져 있으면 따로 셉니다.[^uniq]

```bash
# tr '\n' ' ' 는 줄바꿈을 공백으로 바꿔 결과를 한 줄로 보인다
# 정렬 없이: a 가 떨어져 있어 둘 다 남는다
printf 'a\nb\na\n' | uniq | tr '\n' ' '            # a b a

# 정렬 뒤에: 같은 줄이 이웃해 하나로 합쳐진다
printf 'a\nb\na\n' | sort | uniq | tr '\n' ' '     # a b
```

```bash
# tags.txt 를 정렬해 센다. db 는 세 번이고 Web 과 web 은 따로 센다
#   uniq -c   줄 앞에 연속으로 나온 횟수를 붙인다 (--count)
sort tags.txt | uniq -c
```

```bash
      1 Web
      1 cache
      3 db
      1 web
```

### 반복된 줄 세고 거르기

> 반복된 줄이나 한 번만 나온 줄만 고르고, 대소문자만 다른 줄을 합쳐 셉니다.

아래 옵션은 `tags.txt` 를 정렬한 뒤 줄을 거르거나 셉니다.

```bash
# db 만 두 번 넘게 나와 db 하나가 보인다
#   uniq -d   두 번 이상 나온 줄을 하나씩만 보인다 (--repeated)
sort tags.txt | uniq -d                          # db

# 한 번씩 나온 세 줄이 보인다
#   uniq -u   한 번만 나온 줄만 보인다 (--unique)
sort tags.txt | uniq -u | tr '\n' ' '            # Web cache web

# db 세 줄이 모두 보인다
#   uniq -D   두 번 이상 나온 줄을 나온 횟수만큼 모두 보인다
sort tags.txt | uniq -D | tr '\n' ' '            # db db db
```

`-d` 는 반복된 줄의 첫 줄 하나만, `-D` 는 반복된 줄 전부를 냅니다.[^uniq-d]

```bash
# 대소문자만 다른 web·Web 이 한 줄로 합쳐진다
#   sort -f   비교할 때 소문자를 대문자로 접어 대소문자를 같게 본다 (--ignore-case)
#   uniq -i   대소문자를 무시하고 같은 줄로 본다 (--ignore-case)
sort -f tags.txt | uniq -ic
```

```bash
      1 cache
      3 db
      2 Web
```

`-i` 로 합친 그룹은 첫 줄 모양으로 나옵니다. `sort -f` 가 `Web` 을 `web` 앞에 뒀으므로 위에서는 `Web` 이 보입니다.

### 정렬 키와 순서

> 정렬 기준을 문자열에서 숫자·단위 크기·버전 번호로 바꾸고 순서를 뒤집습니다.

`-n` 은 앞머리의 숫자 부분만 읽으므로 `%` 가 붙은 칸도 숫자로 정렬됩니다.[^sort]

```bash
# 기본: 문자열 순서라 100 이 9 앞에 온다
printf '10\n9\n100\n' | sort | tr '\n' ' '                # 10 100 9

# 9 가 맨 앞에 온다
#   sort -n   앞머리 숫자 크기로 정렬한다 (--numeric-sort)
printf '10\n9\n100\n' | sort -n | tr '\n' ' '             # 9 10 100

# c 가 맨 앞에 온다
#   sort -r   비교 결과를 뒤집는다 (--reverse)
printf 'b\na\nc\n' | sort -r | tr '\n' ' '                # c b a
```

`-h` 는 부호, 단위 접미사, 숫자 값 순서로 견줍니다.[^sort-h]

```bash
# -n 으로 sizes.txt 를 정렬하면 접미사를 무시해 1.5G 가 맨 앞에 온다
sort -n sizes.txt | tr '\n' ' '                           # 1.5G 3K 12M 200M

# 3K 가 맨 앞이고 1.5G 가 맨 끝에 온다
#   sort -h   K < M < G 접미사를 반영해 숫자 크기로 정렬한다 (--human-numeric-sort)
sort -h sizes.txt | tr '\n' ' '                           # 3K 12M 200M 1.5G

# -h 와 -r 을 합치면 1.5G 부터 큰 쪽 순서다
sort -hr sizes.txt | tr '\n' ' '                          # 1.5G 200M 12M 3K
```

`-V` 는 숫자가 아닌 부분을 기본 정렬처럼 견줍니다.[^sort-v]

```bash
# 기본: 문자열 순서라 v1.10 이 v1.2 앞에 온다
sort versions.txt | tr '\n' ' '                           # v1.10 v1.2 v1.2.1 v1.9

# v1.9 가 v1.10 앞에 온다
#   sort -V   각 숫자 덩어리를 숫자로 읽는다 (--version-sort)
sort -V versions.txt | tr '\n' ' '                        # v1.2 v1.2.1 v1.9 v1.10
```

### 키와 구분자

> 정렬 기준을 줄 전체가 아니라 칸 하나나 여럿으로 좁힙니다.

`-t` 가 없으면 연속한 공백이 칸 구분입니다.

```bash
# df.txt 의 머리글을 awk 로 뺀 뒤 사용률(다섯째 칸)이 큰 두 줄만 본다
#   sort -k5   다섯째 칸부터 줄 끝까지를 키로 삼는다 (--key)
#   head -2    앞의 두 줄만 찍는다 (--lines)
awk 'NR>1' df.txt | sort -k5 -rn | head -2
```

```bash
/dev/sdb1        103081248  97927188         0     100% /data
/dev/sdc1         51474912  46327424   2509728      95% /var/log
```

```bash
# /etc/passwd 를 셋째 칸(UID) 숫자 순으로 정렬해 앞의 두 줄에서 이름과 UID 만 본다
#   sort -t:    칸을 나누는 문자를 : 로 정한다 (--field-separator)
#   cut -d:     칸 구분자를 : 로 정한다 (--delimiter)
#   cut -f1,3   첫째와 셋째 칸만 찍는다 (--fields)
sort \
  -t: \
  -k3 \
  -n \
  /etc/passwd \
  | head -2 \
  | cut -d: -f1,3
```

```bash
root:0
daemon:1
```

`-k3` 처럼 끝 칸을 적지 않으면 키가 줄 끝까지 이어지므로, 한 칸으로 한정하려면 `-k3,3` 처럼 시작과 끝을 같이 적습니다.[^sort-k]

```bash
# 쉼표로 나눈 셋째 칸 하나만 숫자 키로 삼는다. 25 가 둘이라 줄 전체로 가려 choi 가 앞선다
#   sort -k3,3n   키를 셋째 칸 하나로 한정한다. 키 뒤에 붙인 옵션 글자 n 은 그 키에만 적용된다
sort -t, -k3,3n members.csv
```

```bash
choi,ops,25
lee,ops,25
kim,dev,31
park,dev,45
```

키를 여러 개 주면 앞 키가 같을 때 다음 키로 가립니다.

```bash
# 부서(둘째 칸)를 문자열로 먼저 정하고, 같은 부서 안에서 나이(셋째 칸)를 큰 쪽부터 놓는다
#   sort -k2,2     둘째 칸 하나를 문자열 키로 삼는다
#   sort -k3,3nr   셋째 칸 하나를 숫자 역순 키로 삼는다
sort \
  -t, \
  -k2,2 \
  -k3,3nr \
  members.csv
```

```bash
park,dev,45
kim,dev,31
choi,ops,25
lee,ops,25
```

`-k2` 와 `-k2,2` 는 다릅니다. `pairs.txt` 에서 둘째 칸 값이 1 인 두 줄의 순서가 바뀝니다.

```bash
# -k2,2: 둘째 칸만 키. 1 인 a·b 는 같은 키라 줄 전체로 가려 a 가 앞선다
sort -k2,2 pairs.txt | tr '\n' '|'               # c 0 x|a 1 z|b 1 y|

# -k2: 둘째 칸부터 줄 끝까지가 키. 1 z 와 1 y 를 견주어 b 가 앞선다
sort -k2 pairs.txt | tr '\n' '|'                 # c 0 x|b 1 y|a 1 z|
```

### 중복 제거와 제자리 저장

> `sort | uniq` 를 한 명령으로 줄이고, 정렬 결과로 입력 파일을 덮어씁니다.

```bash
# b 가 하나만 남는다. sort | uniq 와 같다
#   sort -u   같은 줄이 이어지면 첫 줄만 남긴다 (--unique)
printf 'b\na\nb\n' | sort -u | tr '\n' ' '       # a b

# -f 와 -u: 대소문자가 다른 줄도 같은 줄로 보아 입력에서 먼저 나온 줄만 남긴다
sort -fu words.txt | tr '\n' ' '                 # Apple banana cherry
```

`-u` 가 없으면 `banana` 와 `Banana` 는 다른 줄로 남습니다.[^sort-u]

```bash
# -o 로 입력과 같은 파일에 쓰면 6줄이 그대로 남는다
#   sort -o   결과를 표준 출력 대신 파일에 쓴다 (--output)
#   wc -l     줄바꿈 문자의 수를 센다 (--lines)
cp tags.txt t1.txt; sort -o t1.txt t1.txt; wc -l t1.txt     # 6 t1.txt

# 리다이렉트로 같은 파일에 쓰면 셸이 먼저 비워 버려 내용이 사라진다
cp tags.txt t2.txt; sort t2.txt > t2.txt; wc -l t2.txt      # 0 t2.txt
```

`sort` 는 입력을 모두 읽은 뒤에 출력 파일을 열기 때문에 `-o` 는 같은 파일을 덮어써도 됩니다.[^sort-o]

### 줄·단어·바이트 수 세기

> 옵션 없이 쓰면 줄 수, 단어 수, 바이트 수 순서로 세 숫자와 파일 이름을 냅니다.

```bash
wc app.log                                       #   7  38 337 app.log
```

옵션은 그중 하나만 고릅니다.

```bash
# 줄 수 하나만 나온다
wc -l app.log                                    # 7 app.log

# 공백으로 나뉜 덩어리 38개를 단어로 센다
#   wc -w   단어 수만 센다 (--words)
wc -w app.log                                    # 38 app.log

# 337 은 줄바꿈 일곱 개까지 더한 바이트 수다
#   wc -c   바이트 수만 센다 (--bytes)
wc -c app.log                                    # 337 app.log

# ERROR 줄 두 개가 54칸으로 가장 길다
#   wc -L   가장 긴 줄의 표시 너비만 센다 (--max-line-length)
wc -L app.log                                    # 54 app.log
```

### 바이트와 문자 수 구분하기

> 한글처럼 여러 바이트로 적는 글자는 바이트 수와 문자 수가 갈립니다.

문자 수는 현재 locale 로 정해집니다.[^wc-m] `ko.txt` 의 `가나다` 는 UTF-8 에서 글자당 3바이트라 줄바꿈까지 10 바이트이고 4 문자입니다.

```bash
# -c: 바이트 수. 한글 세 글자 9바이트에 줄바꿈 1바이트
wc -c ko.txt                                     # 10 ko.txt

# C locale 에서는 -m 도 바이트와 같은 10 이다
#   wc -m   현재 locale 의 문자 수를 센다 (--chars)
wc -m ko.txt                                     # 10 ko.txt

# LC_ALL=C.UTF-8 로 UTF-8 locale 을 주어야 문자 수 4 가 나온다
LC_ALL=C.UTF-8 wc -m ko.txt                      # 4 ko.txt
```

### 여러 파일과 표준 입력

> 결과를 사람이 읽을지 스크립트가 받을지에 따라 입력 방식을 고릅니다.

파일을 여러 개 주면 파일마다 한 줄씩 낸 뒤 합계를 `total` 줄로 냅니다.[^wc-total]

```bash
wc -l app.log df.txt access.log
```

```bash
   7 app.log
   5 df.txt
   7 access.log
  19 total
```

파일 이름은 인자로 받은 경우에만 찍습니다. 표준 입력으로 받으면 숫자만 나와 변수에 담아 쓰기 좋습니다.

```bash
wc -l < app.log                                  # 7
cat app.log | wc -l                              # 7
```

### 다른 명령과 이어 로그 세기

> 다른 명령으로 칸을 뽑은 뒤 값별로 세거나 서로 다른 값의 수를 셉니다.

```bash
# 10.0.0.7 이 4번으로 맨 위다. 끝의 sort -rn 이 센 수를 큰 쪽부터 놓는다
#   grep -o   비어 있지 않은 맞은 부분만 찍는다 (--only-matching)
#   grep -E   패턴을 확장 정규식으로 읽는다 (--extended-regexp)
grep -oE '^[0-9.]+' access.log | sort | uniq -c | sort -rn
```

```bash
      4 10.0.0.7
      2 10.0.0.9
      1 10.0.0.3
```

```bash
# ERROR 줄을 골라 시각의 시(時)별로 센다. 09 시에 2건, 10 시에 1건이다
#   cut -c1-2   앞의 두 글자만 찍는다 (--characters)
grep ERROR app.log | cut -d' ' -f2 | cut -c1-2 | sort | uniq -c
```

```bash
      2 09
      1 10
```

```bash
# 첫 칸의 IP 중 서로 다른 것의 수를 센다
cut -d' ' -f1 access.log | sort -u | wc -l       # 3
```

Unix 파이프라인을 배치 처리 원형으로 보는 관점은 [DDIA 11장 노트](../../../../05_data/book/designing-data-intensive-applications/11-01.%EB%B0%B0%EC%B9%98%20%EC%B2%98%EB%A6%AC%20%EA%B0%9C%EC%9A%94%EC%99%80%20Unix%20%EB%8F%84%EA%B5%AC.md) 「2. Unix 파이프라인으로 배우는 배치 처리 원리」 에 있습니다.



## 주의사항과 동작 원리

> 정렬 순서는 locale 에 따라 달라집니다.

### 대소문자와 locale

> C 순서에서는 대문자가 소문자보다 앞서고 `en_US.UTF-8` 에서는 대·소문자가 이웃합니다.

정렬 순서는 locale 의 `LC_COLLATE` 가 정합니다.[^sort-f] 이 컨테이너는 `LANG` 이 비어 있어 C 순서, 곧 바이트값 순서로 정렬하므로 대문자가 모두 소문자보다 앞섭니다.

```bash
# Debian 컨테이너에는 locale 이 들어 있지 않아 en_US.UTF-8 을 먼저 만든다
apt-get update -qq && apt-get install -y -qq locales
sed -i 's/# en_US.UTF-8/en_US.UTF-8/' /etc/locale.gen
locale-gen
```

같은 네 줄을 세 가지 설정으로 정렬해 순서를 비교합니다.

```bash
# 기본(C 순서): 대문자가 모두 소문자보다 앞선다
printf 'b\nA\na\nB\n' | sort | tr '\n' ' '                              # A B a b

# LC_ALL=en_US.UTF-8: 같은 글자의 대·소문자가 이웃한다. LANG 이 en_US.UTF-8 인 셸의 기본 결과와 같다
printf 'b\nA\na\nB\n' | LC_ALL=en_US.UTF-8 sort | tr '\n' ' '           # a A b B

# LC_ALL=C: 환경의 locale 과 무관하게 바이트값 순서로 고정한다
printf 'b\nA\na\nB\n' | LC_ALL=C sort | tr '\n' ' '                     # A B a b
```

스크립트에서 환경마다 결과가 달라지면 안 될 때는 `LC_ALL=C sort` 로 고정합니다.

```bash
# 소문자를 대문자로 접어 비교하므로 Apple 과 apple, Banana 와 banana 가 이웃한다
sort -f words.txt | tr '\n' ' '                  # Apple apple Banana banana cherry
```



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [awk 참조 시트](./awk.md) — 배열로 세는 다른 방법
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- GNU coreutils 9.1 의 `sort --help`·`uniq --help`·`wc --help` 원문 — Debian 12 컨테이너에서 2026-11-13 출력
- [GNU coreutils 매뉴얼](https://www.gnu.org/software/coreutils/manual/coreutils.html) — 2026-11-10 조회

[^df]: GNU coreutils 매뉴얼, "df invocation" 의 `-P` — "The information about each file system is always printed on exactly one line". <https://www.gnu.org/software/coreutils/manual/coreutils.html#df-invocation>
[^uniq]: GNU coreutils 매뉴얼, "uniq invocation" — "repeated input lines are detected only if they are adjacent". <https://www.gnu.org/software/coreutils/manual/coreutils.html#uniq-invocation>
[^sort]: GNU coreutils 매뉴얼, "sort invocation" 의 `-n` — "The number begins each line and consists of optional blanks, an optional '-' sign, and zero or more digits …". <https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-invocation>
[^uniq-d]: GNU coreutils 매뉴얼, "uniq invocation" — `-d` 는 "When used by itself, this option causes uniq to print the first copy of each repeated line, and nothing else.", `-u` 는 "When used by itself, this option causes uniq to print unique lines, and nothing else.", `-D` 는 "Do not discard the second and subsequent repeated input lines, but discard lines that are not repeated.". <https://www.gnu.org/software/coreutils/manual/coreutils.html#uniq-invocation>
[^sort-h]: GNU coreutils 매뉴얼, "sort invocation" 의 `-h` — "Sort numerically, first by numeric sign (negative, zero, or positive); then by SI suffix (either empty, or 'k' or 'K', or one of 'MGTPEZYRQ', in that order …); and finally by numeric value.". <https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-invocation>
[^sort-v]: GNU coreutils 매뉴얼, "sort invocation" 의 `-V` — "Sort by version name and number. It behaves like a standard sort, except that each sequence of decimal digits is treated numerically as an index/version number.". <https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-invocation>
[^sort-k]: GNU coreutils 매뉴얼, "sort invocation" 의 `-k` — "Specify a sort field that consists of the part of the line between pos1 and pos2 (or the end of the line, if pos2 is omitted), inclusive.", `-t` 는 "Use character separator as the field separator when finding the sort keys in each line.". <https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-invocation>
[^sort-f]: GNU coreutils 매뉴얼, "sort invocation" — "Unless otherwise specified, all comparisons use the character collating sequence specified by the LC_COLLATE locale."(§ 앞머리), `-f` 는 "Fold lowercase characters into the equivalent uppercase characters when comparing so that, for example, 'b' and 'B' sort as equal.". <https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-invocation>
[^sort-u]: GNU coreutils 매뉴얼, "sort invocation" 의 `-u` — "Normally, output only the first of a sequence of lines that compare equal.", `-c` 는 "Check whether the given file is already sorted: if it is not all sorted, print a diagnostic containing the first out-of-order line and exit with a status of 1.". <https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-invocation>
[^sort-o]: GNU coreutils 매뉴얼, "sort invocation" 의 `-o` — "Normally, sort reads all input before opening output-file, so you can sort a file in place by using commands like sort -o F F and cat F | sort -o F.". <https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-invocation>
[^wc-m]: GNU coreutils 매뉴얼, "wc invocation" — `-c` 는 "Print only the byte counts.", `-m` 은 "Print only the character counts, as per the current locale.". <https://www.gnu.org/software/coreutils/manual/coreutils.html#wc-invocation>
[^wc-total]: GNU coreutils 매뉴얼, "wc invocation" — "By default if more than one file is given, wc prints a final line containing the cumulative counts, with the file name total.". <https://www.gnu.org/software/coreutils/manual/coreutils.html#wc-invocation>
[^sort-exit]: GNU coreutils 9.1 매뉴얼(Debian 12 의 `info coreutils`), "sort invocation" — "0 if no error occurred", "1 if invoked with '-c' or '-C' and the input is not sorted", "2 if an error occurred". <https://www.gnu.org/software/coreutils/manual/html_node/sort-invocation.html>
[^uniq-wc-exit]: GNU coreutils 9.1 매뉴얼(Debian 12 의 `info coreutils`), "uniq invocation"·"wc invocation" — "An exit status of zero indicates success, and a nonzero value indicates failure." 코드 1 은 이 시트의 실측입니다(Debian 12, coreutils 9.1). <https://www.gnu.org/software/coreutils/manual/html_node/uniq-invocation.html>, <https://www.gnu.org/software/coreutils/manual/html_node/wc-invocation.html>
