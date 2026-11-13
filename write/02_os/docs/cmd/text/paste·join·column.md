---
title: paste·join·column 참조 시트
tags: [linux, cheatsheet, paste, join, column, cli, reference]
status: draft
source:
  - GNU coreutils 매뉴얼 · column(1)
  - GNU coreutils paste·join `--help` 원문 (coreutils 9.1), util-linux column `--help` 원문 (2.38.1)
related:
  - ../README.md
updated: 2026-11-13
---

# paste·join·column 참조 시트

---

> `paste`, `join`, `column` 으로 두 파일의 줄을 잇고 칸을 맞추는 법을 코드와 주석으로 모은 조회용 시트입니다.

## 개요

> `paste` 는 줄 번호로, `join` 은 첫 칸 값으로 잇고 `column -t` 는 칸을 맞춥니다.

`paste`·`join` 은 coreutils 패키지, `column` 은 bsdextrautils 패키지의 외부 바이너리입니다. 이 시트는 Debian 12 컨테이너(coreutils 9.1, util-linux 2.38.1 의 `column`)로 실측했습니다. macOS 의 `paste`·`join` 은 GNU 판이 아니어서 옵션과 출력이 조금 다릅니다. macOS 의 `column` 에는 `-o`·`-N`·`-R` 옵션이 없습니다.



## 핵심 문법

> 세 명령의 호출 형태와 자주 쓰는 꼴을 유스케이스 순서로 보입니다.

```bash
# 호출 형태
paste [OPTION]... [FILE]...
join [OPTION]... FILE1 FILE2
column [options] [<file>...]

# 같은 줄 번호끼리 탭으로 붙인다 (줄 번호로 두 파일 잇기)
paste 파일1 파일2

# 탭 대신 다른 구분자로 붙인다 (구분자 바꾸기 -d)
paste -d 구분자 파일1 파일2

# 파일 하나의 줄을 모두 한 줄로 잇는다 (파일 하나를 한 줄로 잇기 -s)
paste -s 파일

# 표준 입력을 파일 자리에 쓴다 (표준 입력으로 잇기 -)
paste 파일 -

# 첫 칸이 같은 줄끼리 붙인다 (첫 칸으로 두 파일 잇기)
join 파일1 파일2

# 칸 구분자와 기준 칸을 정한다 (구분자와 기준 칸 정하기)
join \
  -t 구분자 \
  -1 칸 \
  -2 칸 \
  파일1 \
  파일2

# 짝이 없는 줄을 함께 내거나 그 줄만 낸다 (짝이 없는 줄 내기 -a -v)
join -a 1 파일1 파일2
join -v 1 파일1 파일2

# 출력할 칸을 고르고 빈 칸을 채운다 (출력 칸 고르기와 빈 칸 채우기)
join -o 0,1.2,2.2 -e 문자열 파일1 파일2

# 입력을 칸으로 나눠 표로 맞춘다 (표로 칸 너비 맞추기 -t)
column -t 파일

# 입력과 출력의 칸 구분자를 정한다 (입출력 칸 구분자 정하기 -s -o)
column \
  -t \
  -s 구분자 \
  -o 구분자 \
  파일

# 머리글을 더하고 칸을 오른쪽 정렬한다 (머리글과 오른쪽 정렬 -N -R)
column \
  -t \
  -N 이름,이름 \
  -R 이름 \
  파일

# 정렬한 결과를 표준 입력으로 받아 잇는다 (정렬한 입력으로 잇기)
다른 명령 | join - 파일2

# 다른 명령의 출력을 표로 맞춘다 (명령 출력을 표로 맞추기)
다른 명령 | column -t
```



## 종료 코드

> `paste`·`join`·`column` 은 성공하면 0, 실패하면 1 을 돌려줍니다.

`paste`·`join` 의 매뉴얼은 성공은 0, 실패는 0 이 아닌 값이라고만 적고[^coreutils-exit] `column(1)` 에는 종료 코드 절이 없습니다.[^column-exit] 아래 예는 「실습 준비」 에서 만든 파일로 돌립니다.

```bash
# 0  성공. 파일을 읽어 이어 붙이거나 잇거나 칸을 맞추고 끝났을 때
# 1  실패. 없는 파일, 모르는 옵션, 빠진 피연산자, 정렬되지 않은 join 입력을 줬을 때

# >/dev/null 은 정상 출력을 버려 종료 코드만 보이게 한다
paste names.txt teams.txt >/dev/null; echo $?    # 0
join names.txt teams.txt >/dev/null; echo $?     # 0
column names.txt >/dev/null; echo $?             # 0

# 없는 파일은 세 명령 모두 1 이다
paste nofile.txt; echo $?                # paste: nofile.txt: No such file or directory / 1
join names.txt nofile.txt; echo $?       # join: nofile.txt: No such file or directory / 1
column nofile.txt; echo $?               # column: nofile.txt: No such file or directory / 1

# 모르는 옵션
paste --bad; echo $?     # paste: unrecognized option '--bad' / Try 'paste --help' for more information. / 1
join --bad; echo $?      # join: unrecognized option '--bad' / Try 'join --help' for more information. / 1
column --bad; echo $?    # column: unrecognized option '--bad' / Try 'column --help' for more information. / 1

# join 은 파일 두 개가 필요하다. 하나만 주거나 없이 부르면 피연산자가 빠졌다고 알린다
join; echo $?               # join: missing operand / Try 'join --help' for more information. / 1
join names.txt; echo $?     # join: missing operand after 'names.txt' / Try 'join --help' for more information. / 1

# 정렬되지 않은 입력의 순서 오류도 1 이다. 메시지는 「정렬되지 않은 입력」 에 있다
join unsorted.txt teams.txt >/dev/null 2>&1; echo $?    # 1
```

`/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 표기입니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션만 씁니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 파일이 모두 생깁니다.

OrbStack 의 Linux VM 이나 `docker run -it --rm debian:12` 안에서 실행합니다. Debian 12 에서 `column` 은 `bsdextrautils` 패키지에 들어 있으므로 컨테이너에서는 `apt-get install -y bsdextrautils` 로 먼저 설치합니다.

```bash
mkdir -p ~/cmd-lab/paste-join-column && cd ~/cmd-lab/paste-join-column

# names.txt: 번호와 이름 세 줄, teams.txt: 번호와 팀 두 줄(2 가 없다)
# (「종료 코드」, 「줄 번호로 두 파일 잇기」, 「첫 칸으로 두 파일 잇기」)
printf '1 kim\n2 lee\n3 park\n' > names.txt
printf '1 dev\n3 ops\n' > teams.txt

# unsorted.txt: names.txt 를 첫 칸 기준으로 정렬하지 않은 것
# (「정렬한 입력으로 잇기」, 「정렬되지 않은 입력」)
printf '3 park\n1 kim\n2 lee\n' > unsorted.txt

# orders.txt: 주문 번호·사용자 번호·금액. 사용자 번호가 둘째 칸이다
# (「구분자와 기준 칸 정하기」)
printf 'o1 3 5000\no2 1 1200\no3 3 800\n' > orders.txt

# m1.csv: 이름과 부서, m2.csv: 이름과 나이. lee 는 m2 에, zed 는 m1 에 없다
# (「구분자와 기준 칸 정하기」, 「짝이 없는 줄 내기 -a -v」)
printf 'kim,dev\nlee,ops\npark,dev\n' > m1.csv
printf 'kim,31\npark,45\nzed,50\n' > m2.csv

# letters.txt·digits.txt·marks.txt: a b c, 1 2 3, x y z 세 줄씩
# (「구분자 바꾸기 -d」, 「파일 하나를 한 줄로 잇기 -s」)
printf 'a\nb\nc\n' > letters.txt
printf '1\n2\n3\n' > digits.txt
printf 'x\ny\nz\n' > marks.txt

# accounts.txt: /etc/passwd 처럼 콜론으로 나눈 세 줄
# (「머리글과 오른쪽 정렬 -N -R」)
printf 'root:x:0:/root\ndaemon:x:1:/usr/sbin\nwww-data:x:33:/var/www\n' > accounts.txt
```

### 줄 번호로 두 파일 잇기

> 두 파일의 내용은 보지 않고 줄 번호만 맞춰 옆으로 붙입니다.

```bash
# 두 파일을 줄 번호끼리 붙인다. 짝이 없는 3 park 줄은 뒤가 빈 칸이다
paste names.txt teams.txt
```

```bash
1 kim	1 dev
2 lee	3 ops
3 park
```

`paste` 는 칸 값을 견주지 않으므로[^paste] `2 lee` 옆에 `3 ops` 가 옵니다. 기본 구분자는 탭입니다.[^paste-d]

### 구분자 바꾸기 -d

> 구분자를 바꿔 CSV 를 만들거나 두 파일의 줄을 번갈아 냅니다.

```bash
# 탭 대신 쉼표로 붙인다. 짝이 없는 3 park 줄은 쉼표로 끝난다
#   paste -d   탭 대신 쓸 구분자를 정한다 (--delimiters)
paste -d, names.txt teams.txt
```

```bash
1 kim,1 dev
2 lee,3 ops
3 park,
```

```bash
# 세 파일 사이에 쉼표와 콜론이 차례로 들어간다
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

### 파일 하나를 한 줄로 잇기 -s

> 목록 파일을 쉼표로 이은 한 줄이나 더하기 식으로 바꿉니다.

```bash
# a, b, c 가 쉼표로 이어진 한 줄이 된다
#   paste -s   파일 하나의 모든 줄을 구분자로 이어 한 줄로 만든다 (--serial)
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

### 표준 입력으로 잇기 -

> 다른 명령의 출력을 한 칸으로 붙이거나 몇 줄씩 끊어 한 줄로 묶습니다.

파일을 주지 않아도 표준 입력을 읽습니다.[^paste-d]

```bash
# names.txt 의 줄마다 1, 2, 3 이 붙는다. 파일 이름 자리의 - 가 표준 입력이다
seq 1 3 | paste -d, names.txt -
```

```bash
1 kim,1
2 lee,2
3 park,3
```

```bash
# - 를 셋 쓰면 입력을 세 줄씩 끊어 한 줄로 만든다. 여섯 줄이 두 줄이 된다
seq 1 6 | paste -d, - - -
```

```bash
1,2,3
4,5,6
```

### 첫 칸으로 두 파일 잇기

> 줄 번호가 아니라 칸 값으로 짝을 찾아 붙입니다.

```bash
# 1 과 3 이 짝을 찾아 붙는다. tr 로 줄바꿈을 공백으로 바꿔 한 줄에 보인다
join names.txt teams.txt | tr '\n' ' '    # 1 kim dev 3 park ops
```

짝이 없는 `2 lee` 는 출력에서 빠지고 두 파일은 그 칸으로 정렬돼 있어야 합니다.[^join]

### 구분자와 기준 칸 정하기

> CSV 처럼 공백이 아닌 구분자를 쓰는 파일이나 기준 칸이 첫 칸이 아닌 파일을 잇습니다.

구분자는 기본이 공백이고, `-t` 로 정한 구분자는 입력과 출력에 함께 쓰입니다.[^join-t]

```bash
# 쉼표로 나뉜 두 파일을 첫 칸 이름으로 잇는다. 출력은 기준 칸이 맨 앞에 온다
# lee 와 zed 는 짝이 없어 빠진다
#   join -t,   칸 구분자를 쉼표로 정한다
join -t, m1.csv m2.csv
```

```bash
kim,dev,31
park,dev,45
```

```bash
# 주문의 사용자 번호(둘째 칸)로 먼저 정렬해 두고, 사용자 이름이 있는 names.txt 와 잇는다
#   sort -k2,2   정렬 기준을 둘째 칸 하나로 정한다
#   join -1 2    파일 1 에서 둘째 칸을 기준으로 잇는다
#   join -2 1    파일 2 에서 첫 칸을 기준으로 잇는다
sort -k2,2 orders.txt > orders.by-user
join -1 2 -2 1 orders.by-user names.txt
```

```bash
1 o2 1200 kim
3 o1 5000 park
3 o3 800 park
```

### 짝이 없는 줄 내기 -a -v

> 두 목록에서 한쪽에만 있는 항목을 찾을 때 씁니다.

```bash
# 파일 1 에서 짝이 없는 lee 도 낸다
#   join -a   그 파일의 짝이 없는 줄도 낸다. 파일 번호는 1 또는 2 다
join -t, -a1 m1.csv m2.csv
```

```bash
kim,dev,31
lee,ops
park,dev,45
```

```bash
# -a 를 두 번 주면 양쪽에서 짝이 없는 줄을 모두 낸다
join \
  -t, \
  -a1 \
  -a2 \
  m1.csv \
  m2.csv
```

```bash
kim,dev,31
lee,ops
park,dev,45
zed,50
```

```bash
# 파일 1 에서 짝이 없는 줄만 낸다
#   join -v   -a 와 같되 붙은 줄은 내지 않는다. 파일 번호는 1 또는 2 다
join -t, -v1 m1.csv m2.csv                       # lee,ops

# 파일 2 에서 짝이 없는 줄만 낸다
join -t, -v2 m1.csv m2.csv                       # zed,50
```

### 출력 칸 고르기와 빈 칸 채우기

> 줄마다 칸 수가 같은 결과를 만들 때 씁니다.

```bash
# 파일 1 의 둘째 칸과 파일 2 의 둘째 칸만 낸다. 기준 칸은 출력에서 빠진다
#   join -o   출력할 칸을 파일번호.칸번호로 고른다. 0 은 기준 칸이다
join -t, -o 1.2,2.2 m1.csv m2.csv
```

```bash
dev,31
dev,45
```

```bash
# 기준 칸 + 두 파일의 둘째 칸을 내고 빈 칸은 NONE 으로 채운다
#   join -e   짝이 없어 비는 입력 칸을 주어진 문자열로 채운다
join \
  -t, \
  -a1 \
  -e NONE \
  -o 0,1.2,2.2 \
  m1.csv \
  m2.csv
```

```bash
kim,dev,31
lee,ops,NONE
park,dev,45
```

`-e` 는 `-o` 로 칸을 골랐을 때만 빈 칸을 채우므로 `-o` 없이 `-a1 -e NONE` 만 주면 `lee,ops` 가 그대로 나옵니다.[^join-o]

### 표로 칸 너비 맞추기 -t

> 칸 너비가 들쭉날쭉한 출력을 눈으로 읽기 쉬운 표로 바꿉니다.

`column -t` 는 입력을 공백으로 나누고[^column] 출력 칸 사이는 두 칸을 띄웁니다.[^column-opts]

```bash
# 번호와 이름 사이가 두 칸이 된다
#   column -t   입력을 칸으로 나눠 너비를 맞춘 표로 만든다 (--table)
column -t names.txt
```

```bash
1  kim
2  lee
3  park
```

```bash
# 공백으로 나뉜 출력은 어느 것이든 표가 된다. 칸 너비는 가장 긴 줄에 맞춰진다
printf 'svc enabled active\ncron disabled inactive\n' | column -t
```

```bash
svc   enabled   active
cron  disabled  inactive
```

### 입출력 칸 구분자 정하기 -s -o

> CSV 를 표로 읽거나 표의 칸 사이를 원하는 문자로 나눕니다.

```bash
# 쉼표로 나눈 CSV 도 표가 된다
#   column -s   입력 칸 구분자를 정한다 (--separator)
column -t -s, m1.csv
```

```bash
kim   dev
lee   ops
park  dev
```

```bash
# 출력 칸 구분자를 기본 두 칸 대신 ' | ' 로 바꾼다
#   column -o   출력 칸 구분자를 정한다. 기본은 두 칸이다 (--output-separator)
column \
  -t \
  -s, \
  -o ' | ' \
  m1.csv
```

```bash
kim  | dev
lee  | ops
park | dev
```

### 머리글과 오른쪽 정렬 -N -R

> 머리글이 없는 파일에 칸 이름을 붙이고 숫자 칸을 오른쪽에 맞춥니다.

머리글과 정렬은 표 모드에서 정합니다.

```bash
# NAME PW UID HOME 머리글 줄이 맨 위에 생긴다
#   column -N   쉼표로 이은 칸 이름으로 머리글 줄을 더한다 (--table-columns)
column \
  -t \
  -s: \
  -N NAME,PW,UID,HOME \
  accounts.txt
```

```bash
NAME      PW  UID  HOME
root      x   0    /root
daemon    x   1    /usr/sbin
www-data  x   33   /var/www
```

```bash
# UID 칸의 0, 1, 33 이 칸 오른쪽 끝에 맞춰진다
#   column -R   이름이나 번호로 고른 칸을 오른쪽 정렬한다 (--table-right)
column \
  -t \
  -s: \
  -N NAME,PW,UID,HOME \
  -R UID \
  accounts.txt
```

```bash
NAME      PW  UID  HOME
root      x     0  /root
daemon    x     1  /usr/sbin
www-data  x    33  /var/www
```

### 정렬한 입력으로 잇기

> 정렬하지 않은 파일은 `sort` 로 정렬해 `-` 로 `join` 에 넘깁니다.

로케일에 따라 정렬 순서가 달라지므로 `sort` 와 `join` 에 같은 `LC_ALL=C` 를 줍니다.[^join-c]

```bash
# 정렬하지 않은 unsorted.txt 에서도 1 과 3 이 짝을 찾는다
LC_ALL=C sort unsorted.txt | LC_ALL=C join - teams.txt
```

```bash
1 kim dev
3 park ops
```

### 명령 출력을 표로 맞추기

> 반복문이 찍는 줄도 칸이 공백으로 나뉘면 표가 됩니다.

```bash
# 유닛마다 활성화 여부와 현재 상태를 한 줄로 모아 표로 맞춘다
# systemd 가 없는 컨테이너라 돌려 보지 못했다
for s in ssh cron nginx; do
  echo "$s $(systemctl is-enabled "$s") $(systemctl is-active "$s")"
done | column -t
```

`systemctl` 은 [《Learning Modern Linux》 6장 노트](../../../book/learning-modern-linux/06-01.%EB%A8%BC%EC%A0%80%20%EC%BC%9C%EC%A7%80%EB%8A%94%20%EA%B2%83%20%ED%95%98%EB%82%98%EA%B0%80%20%EB%82%98%EB%A8%B8%EC%A7%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%EC%BC%A0%EB%8B%A4.md) 「5. 손으로 만지는 도구들」 에 나옵니다. JSON 은 칸이 공백으로 나뉘지 않아 `jq` 가 맡으며 [《Learning Modern Linux》 3장 셋째 노트](../../../book/learning-modern-linux/03-03.bash%20%EB%8A%94%20%EC%A1%B0%EC%9A%A9%ED%9E%88%20%EC%8B%A4%ED%8C%A8%ED%95%98%EB%AF%80%EB%A1%9C%20%EC%8B%9C%EB%81%84%EB%9F%BD%EA%B2%8C%20%EB%A7%8C%EB%93%A4%EC%96%B4%EC%95%BC%20%ED%95%9C%EB%8B%A4.md)가 다룹니다.



## 주의사항과 동작 원리

> `join` 은 두 파일이 기준 칸으로 정렬돼 있어야 하고, 어긋나면 일부 짝을 놓칩니다.

### 정렬되지 않은 입력

> `join` 은 정렬되지 않은 입력에서 짝이 없는 줄이 있을 때만 순서 오류를 냅니다.

모든 줄에 짝이 있으면 오류 없이 넘어가므로 늘 검사하려면 `--check-order` 를 줍니다.[^join-order]

```bash
# 정렬되지 않은 unsorted.txt: 두 번째 줄에서 순서가 어긋났다고 알린다
# 오류 메시지는 표준 오류로 나오므로 2>&1 >/dev/null 로 메시지만 본다
join unsorted.txt teams.txt 2>&1 >/dev/null
```

```bash
join: unsorted.txt:2: is not sorted: 1 kim
join: input is not in sorted order
```

```bash
# 오류 없이 3 park ops 만 나오고 1 kim dev 짝을 놓친다
#   join --nocheck-order   입력이 정렬됐는지 검사하지 않는다
join --nocheck-order unsorted.txt teams.txt      # 3 park ops
```

정렬한 결과를 넘기는 법은 「정렬한 입력으로 잇기」 에 있습니다.



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [sort·uniq·wc 참조 시트](./sort%C2%B7uniq%C2%B7wc.md) — `join` 앞에 두 파일을 같은 칸으로 정렬하기
- [awk 참조 시트](./awk.md) — 칸을 골라 다시 조립하기
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- GNU coreutils 9.1 의 `paste --help`·`join --help` 원문과 util-linux 2.38.1 의 `column --help` 원문 — Debian 12 컨테이너에서 2026-11-13 출력
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
[^coreutils-exit]: GNU coreutils 9.1 매뉴얼(Debian 12 의 `info coreutils`), "paste invocation" 과 "join invocation" — "An exit status of zero indicates success, and a nonzero value indicates failure." 코드 1 은 이 시트의 실측입니다(Debian 12, coreutils 9.1). <https://www.gnu.org/software/coreutils/manual/html_node/paste-invocation.html>
[^column-exit]: `man column` (Debian 12 bookworm, bsdextrautils) 의 절은 NAME, SYNOPSIS, DESCRIPTION, OPTIONS, ENVIRONMENT, HISTORY, BUGS, EXAMPLES, SEE ALSO, REPORTING BUGS, AVAILABILITY 이고 종료 코드 절이 없습니다. 코드 0 과 1 은 이 시트의 실측입니다(Debian 12, util-linux 2.38.1). <https://manpages.debian.org/bookworm/bsdextrautils/column.1.en.html>
