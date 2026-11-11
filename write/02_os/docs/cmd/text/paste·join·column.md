---
title: paste·join·column 참조 시트
tags: [linux, cheatsheet, paste, join, column, cli, reference]
status: draft
source:
  - GNU coreutils 매뉴얼 · column(1)
related:
  - ../README.md
updated: 2026-11-11
---

# paste·join·column 참조 시트

---

> `paste`, `join`, `column` 으로 두 파일의 줄을 잇고 칸을 맞추는 법을 코드와 주석으로 모은 조회용 시트입니다.

## 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 파일이 모두 생깁니다.

macOS 의 `paste`·`join` 은 GNU 판이 아니어서 옵션과 출력이 조금 다릅니다. macOS 의 `column` 에는 `-o`·`-N`·`-R` 옵션이 없습니다. OrbStack 의 Linux VM 이나 `docker run -it --rm debian:12` 안에서 실행합니다. Debian 12 에서 `column` 은 `bsdextrautils` 패키지에 들어 있으므로 컨테이너에서는 `apt-get install -y bsdextrautils` 로 먼저 설치합니다.

```bash
mkdir -p ~/cmd-lab/paste-join-column && cd ~/cmd-lab/paste-join-column
printf '1 kim\n2 lee\n3 park\n' > names.txt
printf '1 dev\n3 ops\n' > teams.txt
printf '3 park\n1 kim\n2 lee\n' > unsorted.txt
printf 'o1 3 5000\no2 1 1200\no3 3 800\n' > orders.txt
printf 'kim,dev\nlee,ops\npark,dev\n' > m1.csv
printf 'kim,31\npark,45\nzed,50\n' > m2.csv
printf 'a\nb\nc\n' > letters.txt
printf '1\n2\n3\n' > digits.txt
printf 'x\ny\nz\n' > marks.txt
printf 'root:x:0:/root\ndaemon:x:1:/usr/sbin\nwww-data:x:33:/var/www\n' > accounts.txt
```

`names.txt` 에는 `1 kim`, `2 lee`, `3 park` 세 줄이 있고 `teams.txt` 에는 `1 dev`, `3 ops` 두 줄이 있습니다. `unsorted.txt` 는 `names.txt` 와 같은 내용을 첫 칸 기준으로 정렬하지 않은 파일입니다. `orders.txt` 는 주문 번호, 사용자 번호, 금액 순서의 세 줄이고 사용자 번호가 둘째 칸에 있습니다.

`m1.csv` 는 이름과 부서, `m2.csv` 는 이름과 나이를 쉼표로 나눈 파일입니다. 두 파일 모두 첫 칸이 이름이고 `lee` 는 `m2.csv` 에, `zed` 는 `m1.csv` 에 없습니다. `letters.txt`, `digits.txt`, `marks.txt` 는 각각 `a b c`, `1 2 3`, `x y z` 세 줄입니다. `accounts.txt` 는 `/etc/passwd` 처럼 콜론으로 나눈 세 줄입니다.



## 1. 두 파일의 줄을 잇기

> `paste` 는 줄 번호로, `join` 은 첫 칸 값으로 잇고 `column -t` 는 칸을 맞춥니다.

```bash
paste names.txt teams.txt
```

```bash
1 kim	1 dev
2 lee	3 ops
3 park
```

### paste 의 옵션

기본 구분자는 탭입니다. 짝이 없는 줄은 뒤가 빈 칸이 됩니다.[^paste-d] `-d` 로 구분자를 바꾸고 `-s` 로 줄을 세로에서 가로로 돌립니다.

```bash
# -d (--delimiters): 탭 대신 쓸 구분자
paste -d, names.txt teams.txt
```

```bash
1 kim,1 dev
2 lee,3 ops
3 park,
```

```bash
# -d 에 문자를 여러 개 주면 칸 사이마다 차례로 쓰고, 다 쓰면 처음부터 되풀이한다
paste -d ',:' letters.txt digits.txt marks.txt
```

```bash
a,1:x
b,2:y
c,3:z
```

```bash
# -d 의 \n 은 줄바꿈이라 두 파일의 줄이 번갈아 나온다
paste -d '\n' letters.txt marks.txt
```

```bash
a
x
b
y
c
z
```

`-s` 는 한 줄씩 가져오는 대신 파일 하나의 줄을 모두 이어 한 줄로 만듭니다.

```bash
# -s (--serial): 파일 하나의 모든 줄을 구분자로 이어 한 줄로 만든다. -d, 로 쉼표를 쓴다
paste -sd, letters.txt                           # a,b,c

# 숫자 줄을 더하기 식으로 이어 bc 같은 계산기에 넘길 수 있다
paste -sd+ digits.txt                            # 1+2+3
```

```bash
# 파일이 둘이면 파일마다 한 줄씩 만든다
paste -sd, letters.txt digits.txt
```

```bash
a,b,c
1,2,3
```

파일 이름 자리의 `-` 는 표준 입력입니다.[^paste-d] `-` 를 여러 번 쓰면 입력 줄을 번갈아 가져와 그 수만큼의 칸으로 끊습니다.

```bash
# 파일 이름 자리의 -: 표준 입력을 한 칸으로 쓴다
seq 1 3 | paste -d, names.txt -
```

```bash
1 kim,1
2 lee,2
3 park,3
```

```bash
# - 를 셋 쓰면 입력을 세 줄씩 끊어 한 줄로 만든다
seq 1 6 | paste -d, - - -
```

```bash
1,2,3
4,5,6
```

### 첫 칸으로 잇기와 표로 맞추기

```bash
join names.txt teams.txt | tr '\n' ' '    # 1 kim dev 3 park ops
printf 'svc enabled active\ncron disabled inactive\n' | column -t
```

```bash
svc   enabled   active
cron  disabled  inactive
```

```bash
for s in ssh cron nginx; do
  echo "$s $(systemctl is-enabled "$s") $(systemctl is-active "$s")"
done | column -t
```

`paste` 는 같은 줄 번호끼리 탭으로 붙일 뿐이라[^paste] `2 lee` 옆에 `3 ops` 가 옵니다. `join` 은 첫 칸이 같은 줄끼리 붙여 짝이 없는 `2 lee` 를 빼며 두 파일이 그 칸으로 정렬돼 있어야 합니다.[^join] `column -t` 는 공백 출력을 표 형태로 정렬합니다.[^column] `systemctl` 은 [《Learning Modern Linux》 6장 노트](../../../book/learning-modern-linux/06-01.%EB%A8%BC%EC%A0%80%20%EC%BC%9C%EC%A7%80%EB%8A%94%20%EA%B2%83%20%ED%95%98%EB%82%98%EA%B0%80%20%EB%82%98%EB%A8%B8%EC%A7%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%EC%BC%A0%EB%8B%A4.md) 5절에 나옵니다. 이 반복문은 systemd 가 없는 컨테이너라 돌려 보지 못했습니다. JSON 은 칸이 공백으로 나뉘지 않아 `jq` 가 맡으며 [《Learning Modern Linux》 3장 셋째 노트](../../../book/learning-modern-linux/03-03.bash%20%EB%8A%94%20%EC%A1%B0%EC%9A%A9%ED%9E%88%20%EC%8B%A4%ED%8C%A8%ED%95%98%EB%AF%80%EB%A1%9C%20%EC%8B%9C%EB%81%84%EB%9F%BD%EA%B2%8C%20%EB%A7%8C%EB%93%A4%EC%96%B4%EC%95%BC%20%ED%95%9C%EB%8B%A4.md)가 다룹니다.

### join 의 옵션

`join` 은 두 파일이 같은 칸을 기준으로 정렬돼 있어야 합니다. 정렬되지 않은 채 쓰면 짝이 없는 줄이 있을 때 순서가 어긋난 줄에서 오류를 냅니다. 모든 줄에 짝이 있으면 오류 없이 넘어가므로 늘 검사하려면 `--check-order` 를 줍니다.[^join-order] 오류 메시지는 표준 오류로 나오므로 아래는 `2>&1 >/dev/null` 로 메시지만 봅니다.

```bash
# 정렬되지 않은 unsorted.txt: 두 번째 줄에서 순서가 어긋났다고 알린다
join unsorted.txt teams.txt 2>&1 >/dev/null
```

```bash
join: unsorted.txt:2: is not sorted: 1 kim
join: input is not in sorted order
```

```bash
# --nocheck-order: 순서 검사를 끈다. 검사 없이 돌리면 1 kim dev 짝을 놓친다
join --nocheck-order unsorted.txt teams.txt      # 3 park ops
```

정렬한 결과를 `-` 로 넘기면 이 문제가 없어집니다. 로케일에 따라 정렬 순서가 달라지므로 `sort` 와 `join` 에 같은 `LC_ALL=C` 를 줍니다.[^join-c]

```bash
# 정렬해서 표준 입력(-)으로 넘긴다. 첫 칸이 같은 줄끼리 붙는다
LC_ALL=C sort unsorted.txt | LC_ALL=C join - teams.txt
```

```bash
1 kim dev
3 park ops
```

구분자는 기본이 공백입니다. `-t` 로 바꾸고 기준 칸이 첫 칸이 아니면 `-1`·`-2` 로 파일마다 정합니다.[^join-t]

```bash
# -t (쉼표): 입력과 출력의 칸 구분자. 출력은 기준 칸이 맨 앞에 온다
join -t, m1.csv m2.csv
```

```bash
kim,dev,31
park,dev,45
```

```bash
# -1 2 -2 1: 파일 1 은 둘째 칸, 파일 2 는 첫 칸을 기준으로 잇는다. 먼저 사용자 번호(둘째 칸)로 정렬한다
sort -k2,2 orders.txt > orders.by-user
join -1 2 -2 1 orders.by-user names.txt
```

```bash
1 o2 1200 kim
3 o1 5000 park
3 o3 800 park
```

짝이 없는 줄은 기본으로 버려집니다. `-a` 는 버려지는 줄도 내고 `-v` 는 버려지는 줄만 냅니다.

```bash
# -a 1: 파일 1 에서 짝이 없는 lee 도 낸다
join -t, -a1 m1.csv m2.csv
```

```bash
kim,dev,31
lee,ops
park,dev,45
```

```bash
# -a 1 -a 2: 양쪽에서 짝이 없는 줄을 모두 낸다
join -t, -a1 -a2 m1.csv m2.csv
```

```bash
kim,dev,31
lee,ops
park,dev,45
zed,50
```

```bash
# -v 1: 파일 1 에서 짝이 없는 줄만 낸다
join -t, -v1 m1.csv m2.csv                       # lee,ops

# -v 2: 파일 2 에서 짝이 없는 줄만 낸다
join -t, -v2 m1.csv m2.csv                       # zed,50
```

`-o` 는 출력할 칸을 직접 고르고 `-e` 는 짝이 없어 비는 칸을 채울 문자열을 정합니다.[^join-o] `0` 은 기준 칸이고 `1.2` 는 파일 1 의 둘째 칸입니다. `-e` 는 `-o` 로 칸을 골랐을 때만 빈 칸을 채웁니다. `-o` 없이 `-a1 -e NONE` 만 주면 `lee,ops` 가 그대로 나옵니다.

```bash
# -o 1.2,2.2: 파일 1 의 둘째 칸과 파일 2 의 둘째 칸만 낸다
join -t, -o 1.2,2.2 m1.csv m2.csv
```

```bash
dev,31
dev,45
```

```bash
# -a1 -e NONE -o 0,1.2,2.2: 기준 칸 + 두 파일의 둘째 칸을 내고 빈 칸은 NONE 으로 채운다
join -t, -a1 -e NONE -o 0,1.2,2.2 m1.csv m2.csv
```

```bash
kim,dev,31
lee,ops,NONE
park,dev,45
```

### column 의 옵션

`-t` 는 입력을 칸으로 나눠 너비를 맞추고 `-s` 는 입력 칸 구분자를, `-o` 는 출력 칸 구분자를 정합니다.[^column-opts] 기본은 공백으로 나누고 두 칸 띄워 출력합니다.

```bash
# -t (--table): 공백으로 나눠 칸 너비를 맞춘다
column -t names.txt
```

```bash
1  kim
2  lee
3  park
```

```bash
# -s (--separator): 입력 칸 구분자. 쉼표로 나눈 CSV 도 표가 된다
column -t -s, m1.csv
```

```bash
kim   dev
lee   ops
park  dev
```

```bash
# -o (--output-separator): 출력 칸 구분자. 기본 두 칸 대신 ' | ' 를 쓴다
column -t -s, -o ' | ' m1.csv
```

```bash
kim  | dev
lee  | ops
park | dev
```

머리글과 정렬은 표 모드에서 `-N`·`-R` 로 정합니다. `-N` 은 칸 이름을 쉼표로 이어 주면 그 이름으로 머리글 줄을 맨 위에 더하고 `-R` 은 이름이나 번호로 고른 칸을 오른쪽 정렬합니다.

```bash
# -N (--table-columns): 칸 이름을 주면 머리글 줄이 맨 위에 생긴다
column -t -s: -N NAME,PW,UID,HOME accounts.txt
```

```bash
NAME      PW  UID  HOME
root      x   0    /root
daemon    x   1    /usr/sbin
www-data  x   33   /var/www
```

```bash
# -R (--table-right): 이름(또는 번호)으로 고른 칸을 오른쪽 정렬한다
column -t -s: -N NAME,PW,UID,HOME -R UID accounts.txt
```

```bash
NAME      PW  UID  HOME
root      x     0  /root
daemon    x     1  /usr/sbin
www-data  x    33  /var/www
```



## 관련 문서

- [sort·uniq·wc 참조 시트](./sort%C2%B7uniq%C2%B7wc.md) — `join` 앞에 두 파일을 같은 칸으로 정렬하기
- [awk 참조 시트](./awk.md) — 칸을 골라 다시 조립하기



## 참고 자료

- [GNU coreutils 매뉴얼](https://www.gnu.org/software/coreutils/manual/coreutils.html) — 2026-11-10 조회

[^join]: GNU coreutils 매뉴얼, "join invocation" — "file1 and file2 should be sorted on the join fields". <https://www.gnu.org/software/coreutils/manual/coreutils.html#join-invocation>
[^column]: `column(1)` 의 `-t, --table`. <https://man7.org/linux/man-pages/man1/column.1.html>
[^paste]: GNU coreutils 매뉴얼, "paste invocation". <https://www.gnu.org/software/coreutils/manual/coreutils.html#paste-invocation>
[^paste-d]: GNU coreutils 매뉴얼, "paste invocation" — 기본 구분자는 "(default is the TAB character)", `-d` 는 "Consecutively use the characters in delim-list instead of TAB to separate merged lines. When delim-list is exhausted, start again at its beginning.", `-s` 는 "Paste the lines of one file at a time rather than one line from each file.", 표준 입력은 "Standard input is used for a file name of '-' or if no input files are given.". <https://www.gnu.org/software/coreutils/manual/coreutils.html#paste-invocation>
[^join-order]: GNU coreutils 매뉴얼, "join invocation" — `--check-order` 는 "Fail with an error message if either input file is wrongly ordered.", `--nocheck-order` 는 "Do not check that both input files are in sorted order.", 둘 다 주지 않으면 "wrongly sorted inputs are diagnosed only if an input file is found to contain unpairable lines". 이 시트의 오류 메시지는 Debian 12 의 coreutils 9.1 에서 실행해 받았다. <https://www.gnu.org/software/coreutils/manual/coreutils.html#join-invocation>
[^join-c]: GNU coreutils 매뉴얼, "join invocation" 의 "Pre-sorting" — "To avoid any locale-related issues, it is recommended to use the 'C' locale for both commands". <https://www.gnu.org/software/coreutils/manual/coreutils.html#join-invocation>
[^join-t]: GNU coreutils 매뉴얼, "join invocation" — `-t` 는 "Use character char as the input and output field separator.", `-1` 은 "Join on field field (a positive integer) of file 1.", `-a` 는 "Print a line for each unpairable line in file file-number (either '1' or '2'), in addition to the normal output.", `-v` 는 "… instead of the normal output.". <https://www.gnu.org/software/coreutils/manual/coreutils.html#join-invocation>
[^join-o]: GNU coreutils 매뉴얼, "join invocation" — `-e` 는 "Replace those output fields that are missing in the input with string.", `-o` 는 "A field specification of '0' denotes the join field.". <https://www.gnu.org/software/coreutils/manual/coreutils.html#join-invocation>
[^column-opts]: `column(1)` (Debian 12 bookworm, bsdextrautils) — `-t` "Determine the number of columns the input contains and create a table.", `-s` "Specify the possible input item delimiters (default is whitespace).", `-o` "Specify the columns delimiter for table output (default is two spaces).", `-N` "Specify the columns names by comma separated list of names. The names are used for the table header or to address column in option arguments.", `-R` "Right align text in the specified columns.". <https://manpages.debian.org/bookworm/bsdextrautils/column.1.en.html>
