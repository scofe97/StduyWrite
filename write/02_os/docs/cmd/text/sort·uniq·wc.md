---
title: sort·uniq·wc 참조 시트
tags: [linux, cheatsheet, sort, uniq, wc, cli, reference]
status: draft
source:
  - GNU coreutils 매뉴얼
related:
  - ../README.md
updated: 2026-11-11
---

# sort·uniq·wc 참조 시트

---

> `sort` 로 같은 줄을 붙이고 `uniq -c` 와 `wc` 로 세는 법을 코드와 주석으로 모은 조회용 시트입니다.

## 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 파일이 모두 생깁니다.

macOS 의 `sort`·`uniq`·`wc` 는 GNU coreutils 가 아니어서 옵션 지원과 출력 서식이 조금 다릅니다. OrbStack 의 Linux VM 이나 `docker run -it --rm debian:12` 안에서 실행합니다. 이 시트의 출력은 `LANG` 이 비어 있는(C locale) `debian:12` 컨테이너에서 받았습니다. 셸의 locale 이 `en_US.UTF-8` 이면 대소문자가 섞인 줄의 순서와 `wc -m` 결과가 달라집니다. 같은 출력을 보려면 `export LC_ALL=C` 를 먼저 실행합니다.

```bash
mkdir -p ~/cmd-lab/sort && cd ~/cmd-lab/sort
cat > access.log << 'EOT'
10.0.0.7 - - [10/Nov/2026:09:01:15] "GET /orders HTTP/1.1" 200 512
10.0.0.9 - - [10/Nov/2026:09:01:17] "GET /health HTTP/1.1" 200 15
10.0.0.7 - - [10/Nov/2026:09:02:03] "POST /orders HTTP/1.1" 201 87
10.0.0.3 - - [10/Nov/2026:09:03:44] "GET /orders/1001 HTTP/1.1" 404 0
10.0.0.7 - - [10/Nov/2026:09:04:10] "GET /orders HTTP/1.1" 200 512
10.0.0.9 - - [10/Nov/2026:09:05:01] "GET /health HTTP/1.1" 200 15
10.0.0.7 - - [10/Nov/2026:09:06:30] "GET /orders HTTP/1.1" 200 512
EOT
cat > app.log << 'EOT'
2026-11-10 09:01:15 INFO  order-api started
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:14:41 WARN  retrying orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
2026-11-10 10:06:01 error db connection reset
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
2026-11-10 11:30:00 INFO  heartbeat
EOT
cat > df.txt << 'EOT'
Filesystem     1024-blocks      Used Available Capacity Mounted on
/dev/sda1         41152736  17283548  21755756      45% /
/dev/sdb1        103081248  97927188         0     100% /data
/dev/sdc1         51474912  46327424   2509728      95% /var/log
tmpfs              8139112         0   8139112       0% /dev/shm
EOT
cat > members.csv << 'EOT'
kim,dev,31
lee,ops,25
park,dev,45
choi,ops,25
EOT
cat > pairs.txt << 'EOT'
a 1 z
b 1 y
c 0 x
EOT
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
cat > words.txt << 'EOT'
banana
Apple
cherry
apple
Banana
EOT
cat > tags.txt << 'EOT'
db
web
db
Web
db
cache
EOT
cat > ko.txt << 'EOT'
가나다
EOT
```

`access.log` 는 일곱 줄짜리 접근 로그로 첫 칸이 클라이언트 IP 입니다. `app.log` 는 일곱 줄짜리 애플리케이션 로그이고, `df.txt` 는 `df -P` 의 출력 꼴입니다. `-P` 는 장치 이름이 길어도 파일시스템 하나를 한 줄에 찍으므로 다섯째 칸이 늘 사용률입니다.[^df]

`members.csv` 는 이름과 부서와 나이를 쉼표로 나눈 네 줄입니다. 나이 25 가 두 줄이라 같은 키일 때의 순서를 보기 좋습니다. `pairs.txt` 는 둘째 칸 값이 겹치는 세 줄입니다. `sizes.txt` 와 `versions.txt` 에는 단위 접미사와 버전 번호가 들었습니다.

`words.txt` 에는 대소문자가 섞인 단어 다섯 개가 있습니다. `tags.txt` 는 `db` 가 세 번 나오고 `web` 과 `Web` 이 섞인 여섯 줄입니다. `ko.txt` 는 한글 세 글자 한 줄입니다.



## 1. sort 와 uniq -c 로 세기

> 세는 도구가 이웃한 줄끼리만 견주므로 같은 값을 먼저 붙여 놓아야 합니다.

### 정렬로 같은 줄을 붙여 세기

```bash
grep -oE '^[0-9.]+' access.log | sort | uniq -c | sort -rn
```

```bash
      4 10.0.0.7
      2 10.0.0.9
      1 10.0.0.3
```

`uniq` 는 이웃한 줄끼리만 비교하므로 `sort` 로 같은 값을 모은 뒤 `uniq -c` 로 세고 `sort -rn` 으로 내림차순 정렬합니다.[^uniq]

### uniq 의 옵션

`uniq` 는 앞줄과 같은 줄만 합치므로 같은 값이 떨어져 있으면 따로 셉니다. 아래 둘째 줄처럼 `sort` 를 앞에 두면 모두 이웃합니다.

```bash
# 정렬 없이: a 가 떨어져 있어 둘 다 남는다
printf 'a\nb\na\n' | uniq | tr '\n' ' '            # a b a

# 정렬 뒤에: 같은 줄이 이웃해 하나로 합쳐진다
printf 'a\nb\na\n' | sort | uniq | tr '\n' ' '     # a b
```

아래 옵션은 `tags.txt` 를 정렬한 뒤 줄 수를 세거나 거릅니다.

```bash
# -c (--count): 줄 앞에 연속으로 나온 횟수를 붙인다
sort tags.txt | uniq -c
```

```bash
      1 Web
      1 cache
      3 db
      1 web
```

```bash
# -d (--repeated): 두 번 이상 나온 줄을 하나씩만 보인다
sort tags.txt | uniq -d                          # db

# -u (--unique): 한 번만 나온 줄만 보인다
sort tags.txt | uniq -u | tr '\n' ' '            # Web cache web

# -D (--all-repeated): 두 번 이상 나온 줄을 나온 횟수만큼 모두 보인다
sort tags.txt | uniq -D | tr '\n' ' '            # db db db
```

`-d` 는 반복된 줄의 첫 줄 하나만, `-D` 는 반복된 줄 전부를 냅니다.[^uniq-d]

```bash
# -i (--ignore-case): 대소문자를 무시하고 같은 줄로 본다. 대소문자만 다른 web·Web 이 합쳐진다
sort -f tags.txt | uniq -ic
```

```bash
      1 cache
      3 db
      2 Web
```

`-i` 로 합친 그룹은 첫 줄 모양으로 나옵니다. `sort -f` 가 `Web` 을 `web` 앞에 뒀으므로 위에서는 `Web` 이 보입니다.

### 정렬 키와 순서

기본 정렬은 문자열 기준이라 `100` 이 `9` 앞에 옵니다. `-n` 은 앞머리의 숫자 부분만 읽어 숫자로 정렬하므로 `%` 가 붙은 칸도 숫자로 정렬됩니다.[^sort]

```bash
# 기본: 문자열 순서라 100 이 9 앞에 온다
printf '10\n9\n100\n' | sort | tr '\n' ' '                # 10 100 9

# -n (--numeric-sort): 앞머리 숫자 크기로 정렬한다
printf '10\n9\n100\n' | sort -n | tr '\n' ' '             # 9 10 100

# -r (--reverse): 비교 결과를 뒤집는다
printf 'b\na\nc\n' | sort -r | tr '\n' ' '                # c b a
```

`-n` 은 `K`·`M`·`G` 접미사를 숫자 크기로 읽지 못합니다. 크기 단위가 붙은 값은 `-h` 로 정렬합니다.[^sort-h]

```bash
# -n 으로 sizes.txt 를 정렬하면 접미사를 무시해 1.5G 가 맨 앞에 온다
sort -n sizes.txt | tr '\n' ' '                           # 1.5G 3K 12M 200M

# -h (--human-numeric-sort): K < M < G 접미사를 반영한다
sort -h sizes.txt | tr '\n' ' '                           # 3K 12M 200M 1.5G

# -h 와 -r: 큰 쪽부터
sort -hr sizes.txt | tr '\n' ' '                          # 1.5G 200M 12M 3K
```

버전 번호는 문자열로 정렬하면 `v1.10` 이 `v1.9` 앞에 옵니다. `-V` 는 숫자 덩어리를 숫자로 읽습니다.[^sort-v]

```bash
# 기본: 문자열 순서라 v1.10 이 v1.2 앞에 온다
sort versions.txt | tr '\n' ' '                           # v1.10 v1.2 v1.2.1 v1.9

# -V (--version-sort): 숫자 덩어리를 숫자로 읽는다
sort -V versions.txt | tr '\n' ' '                        # v1.2 v1.2.1 v1.9 v1.10
```

### 키와 구분자

`-k` 는 줄의 일부분을 정렬 기준으로 삼고 `-t` 는 칸을 나누는 문자를 정합니다.[^sort-k] `-t` 가 없으면 연속한 공백이 칸 구분입니다. 아래 `df.txt` 는 첫 줄이 머리글이라 `awk` 로 뺀 뒤 사용률 칸(다섯째)을 숫자 키로 삼아 큰 쪽부터 둘만 봅니다.

```bash
# -k 5 (--key=5): 다섯째 칸부터 줄 끝까지를 키로 삼는다. -n 은 숫자, -r 은 역순
awk 'NR>1' df.txt | sort -k5 -rn | head -2
```

```bash
/dev/sdb1        103081248  97927188         0     100% /data
/dev/sdc1         51474912  46327424   2509728      95% /var/log
```

```bash
# -t (--field-separator): 구분자를 : 로 정하고 셋째 칸(UID)부터를 숫자 키로 삼는다
sort -t: -k3 -n /etc/passwd | head -2 | cut -d: -f1,3
```

```bash
root:0
daemon:1
```

`-k3` 처럼 끝 칸을 적지 않으면 키가 줄 끝까지 이어집니다. 키를 한 칸으로 한정하려면 `-k3,3` 처럼 시작과 끝을 같이 적고, 옵션 글자(`n`·`r`)는 키 뒤에 붙여 그 키에만 적용합니다. 키가 같은 줄끼리는 마지막에 줄 전체를 견주므로 `choi` 가 `lee` 앞에 옵니다.

```bash
# -k3,3n: 쉼표로 나눈 셋째 칸 하나만 숫자 키로. 25 가 둘이라 줄 전체로 가려 choi 가 앞선다
sort -t, -k3,3n members.csv
```

```bash
choi,ops,25
lee,ops,25
kim,dev,31
park,dev,45
```

키를 여러 개 주면 앞 키가 같을 때 다음 키로 가립니다. 아래는 부서(둘째 칸)를 문자열로 먼저 정하고, 같은 부서 안에서 나이(셋째 칸)를 큰 쪽부터 놓습니다.

```bash
# -k2,2 -k3,3nr: 둘째 칸 문자열 순서, 같으면 셋째 칸 숫자 역순
sort -t, -k2,2 -k3,3nr members.csv
```

```bash
park,dev,45
kim,dev,31
choi,ops,25
lee,ops,25
```

`-k2` 와 `-k2,2` 는 다릅니다. `pairs.txt` 에서 둘째 칸 값이 1 인 두 줄을 보면 `-k2,2` 는 둘째 칸만 견주어 같다고 보고 줄 전체 비교로 가립니다. `-k2` 는 둘째 칸부터 줄 끝(`1 z` 와 `1 y`)까지 견주어 순서가 바뀝니다.

```bash
# -k2,2: 둘째 칸만 키. 1 인 a·b 는 같은 키라 줄 전체로 가려 a 가 앞선다
sort -k2,2 pairs.txt | tr '\n' '|'               # c 0 x|a 1 z|b 1 y|

# -k2: 둘째 칸부터 줄 끝까지가 키. 1 z 와 1 y 를 견주어 b 가 앞선다
sort -k2 pairs.txt | tr '\n' '|'                 # c 0 x|b 1 y|a 1 z|
```

### 대소문자와 locale

정렬 순서는 locale 의 `LC_COLLATE` 가 정합니다.[^sort-f] 이 컨테이너는 `LANG` 이 비어 있어 C 순서, 곧 바이트값 순서로 정렬하므로 대문자가 모두 소문자보다 앞섭니다. `LANG` 이 `en_US.UTF-8` 인 셸에서는 기본 결과가 아래 둘째 줄과 같습니다. Debian 컨테이너에는 locale 이 들어 있지 않아 `en_US.UTF-8` 을 먼저 만듭니다.

```bash
apt-get update -qq && apt-get install -y -qq locales
sed -i 's/# en_US.UTF-8/en_US.UTF-8/' /etc/locale.gen
locale-gen
```

같은 네 줄을 세 가지 설정으로 정렬해 순서를 비교합니다.

```bash
# 기본(C 순서): 대문자가 모두 소문자보다 앞선다
printf 'b\nA\na\nB\n' | sort | tr '\n' ' '                              # A B a b

# LC_ALL=en_US.UTF-8: 같은 글자의 대·소문자가 이웃한다
printf 'b\nA\na\nB\n' | LC_ALL=en_US.UTF-8 sort | tr '\n' ' '           # a A b B

# LC_ALL=C: 환경의 locale 과 무관하게 바이트값 순서로 고정한다
printf 'b\nA\na\nB\n' | LC_ALL=C sort | tr '\n' ' '                     # A B a b
```

스크립트에서 환경마다 결과가 달라지면 안 될 때는 `LC_ALL=C sort` 로 고정합니다.

```bash
# -f (--ignore-case): 비교할 때 소문자를 대문자로 접어 대소문자를 같게 본다
sort -f words.txt | tr '\n' ' '                  # Apple apple Banana banana cherry
```

### 중복 제거·검사·저장

```bash
# -u (--unique): 같은 줄은 하나만 남긴다. sort | uniq 와 같다
printf 'b\na\nb\n' | sort -u | tr '\n' ' '       # a b

# -f 와 -u: 대소문자가 다른 줄도 같은 줄로 보아 입력에서 먼저 나온 줄만 남긴다
sort -fu words.txt | tr '\n' ' '                 # Apple banana cherry
```

`-u` 가 없으면 `banana` 와 `Banana` 는 다른 줄로 남습니다.[^sort-u]

```bash
# -c (--check): 이미 정렬됐는지만 검사한다. 정렬돼 있으면 출력 없이 종료 상태 0
printf 'a\nb\nc\n' | sort -c; echo $?            # 0

# 어긋나면 처음 어긋난 줄을 알리고 종료 상태 1
sort -c words.txt; echo $?
```

```bash
sort: words.txt:2: disorder: Apple
1
```

```bash
# -o (--output): 결과를 파일에 쓴다. 입력과 같은 파일이어도 안전하다
cp tags.txt t1.txt; sort -o t1.txt t1.txt; wc -l t1.txt     # 6 t1.txt

# 리다이렉트로 같은 파일에 쓰면 셸이 먼저 비워 버려 내용이 사라진다
cp tags.txt t2.txt; sort t2.txt > t2.txt; wc -l t2.txt      # 0 t2.txt
```

`sort` 는 입력을 모두 읽은 뒤에 출력 파일을 열기 때문에 `-o` 는 같은 파일을 덮어써도 됩니다.[^sort-o] 리다이렉트는 `sort` 가 시작하기 전에 셸이 파일을 비웁니다.



## 2. 줄 수와 시간대 세기

> 맞은 줄을 시간대별로 세고, 파일의 줄 수와 단어 수와 바이트 수를 셉니다.

```bash
grep ERROR app.log | cut -d' ' -f2 | cut -c1-2 | sort | uniq -c
```

```bash
      2 09
      1 10
```

```bash
cut -d' ' -f1 access.log | sort -u | wc -l       # 3
```

`wc` 는 줄 수, 단어 수, 바이트 수를 차례로 내고 `wc -l` 은 줄 수만 냅니다. 위 둘째 파이프라인은 첫 칸의 IP 중 서로 다른 것의 수입니다. Unix 파이프라인을 배치 처리 원형으로 보는 관점은 [DDIA 11장 노트](../../../../05_data/book/designing-data-intensive-applications/11-01.%EB%B0%B0%EC%B9%98%20%EC%B2%98%EB%A6%AC%20%EA%B0%9C%EC%9A%94%EC%99%80%20Unix%20%EB%8F%84%EA%B5%AC.md) 2절에 있습니다.

### wc 의 옵션

옵션 없이 쓰면 줄 수, 단어 수, 바이트 수 순서로 세 숫자와 파일 이름을 냅니다.

```bash
wc app.log                                       #   7  38 337 app.log
```

옵션은 그중 하나만 고릅니다.

```bash
# -l (--lines): 줄바꿈 문자의 수
wc -l app.log                                    # 7 app.log

# -w (--words): 공백으로 나뉜 단어의 수
wc -w app.log                                    # 38 app.log

# -c (--bytes): 바이트 수
wc -c app.log                                    # 337 app.log

# -L (--max-line-length): 가장 긴 줄의 표시 너비
wc -L app.log                                    # 54 app.log
```

`-c` 는 바이트를 세고 `-m` 은 현재 locale 의 문자 수를 셉니다.[^wc-m] `ko.txt` 의 `가나다` 는 UTF-8 에서 글자당 3바이트라 줄바꿈까지 10 바이트이고 4 문자입니다. 이 컨테이너처럼 locale 이 C 이면 `-m` 도 바이트 단위로 세므로 UTF-8 locale 을 지정해야 문자 수가 나옵니다.

```bash
# -c: 바이트 수. 한글 세 글자 9바이트에 줄바꿈 1바이트
wc -c ko.txt                                     # 10 ko.txt

# -m (--chars): C locale 에서는 바이트와 같은 10
wc -m ko.txt                                     # 10 ko.txt

# LC_ALL=C.UTF-8 로 UTF-8 locale 을 주면 문자 수 4
LC_ALL=C.UTF-8 wc -m ko.txt                      # 4 ko.txt
```

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



## 관련 문서

- [awk 참조 시트](./awk.md) — 배열로 세는 다른 방법



## 참고 자료

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
