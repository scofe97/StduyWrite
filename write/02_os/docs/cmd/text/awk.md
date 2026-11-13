---
title: awk 참조 시트
tags: [linux, cheatsheet, awk, gawk, cli, reference]
status: draft
source:
  - GNU awk 매뉴얼
related:
  - ../README.md
updated: 2026-11-13
---

# awk 참조 시트

---

> `awk` 로 칸을 번호로 부르고 `패턴 { 동작 }` 으로 줄을 고르는 법을 옵션과 내장 변수별 예제로 모은 조회용 시트입니다.

## 개요

> `awk` 는 입력을 줄과 칸으로 나눠 `패턴 { 동작 }` 으로 줄을 골라 가공하는 패턴 스캔·처리 언어입니다.

Debian 12 의 기본 `awk` 는 mawk 패키지의 외부 바이너리이며 이 시트는 mawk 1.3.4 와 gawk 5.2.1 로 실측했습니다. 유스케이스의 예는 둘에서 같게 나오고 한글 글자 수를 세는 예만 다릅니다(「주의사항과 동작 원리」 의 「한글과 length」). macOS 기본 `awk` 는 GNU awk 가 아니어서 일부 동작과 출력이 다릅니다.



## 핵심 문법

> 프로그램 `패턴 { 동작 }` 을 줄마다 실행하고, 옵션으로 칸 구분자(`-F`)와 외부 변수(`-v`)를 정합니다.

```bash
# 호출 형태 (gawk --help 와 mawk -W usage 의 Usage 줄)
gawk [POSIX or GNU style options] -f progfile [--] file ...
gawk [POSIX or GNU style options] [--] 'program' file ...
mawk [Options] [Program] [file ...]

# 칸과 줄 번호를 부른다 (칸 번호와 줄 번호)
awk '{print $1, NR}' 파일

# 칸 구분자를 바꾼다 (구분자 -F)
awk -F구분자 '{print $2}' 파일

# 패턴이 참인 줄에서만 동작한다 (패턴과 동작)
awk '패턴 {동작}' 파일

# 칸이 정규식과 맞거나 맞지 않는 줄을 고른다 (칸에 정규식 걸기)
awk '$6 ~ /정규식/' 파일
awk '$6 !~ /정규식/' 파일

# 앞 패턴이 참인 줄부터 뒤 패턴이 참인 줄까지 고른다 (범위 패턴)
awk '/시작/,/끝/' 파일

# 칸 수와 마지막 칸을 부른다 (칸 수와 마지막 칸)
awk '{print NF, $NF}' 파일

# 셸의 값을 넘기고 합계를 낸다 (외부 변수 -v 와 합계)
awk -v 변수=값 '{sum += $3} END {print sum}' 파일

# 서식을 줘서 찍는다 (print 와 printf 서식)
awk '{printf "%-10s %5d\n", $1, $2}' 파일

# 출력의 칸 구분자와 줄 끝을 바꾼다 (출력 구분자 OFS 와 ORS)
awk 'BEGIN {OFS=","} {print $1, $2}' 파일

# 칸 값을 첨자로 세고 모은다 (연관 배열로 세기)
awk '{count[$1]++} END {for (k in count) print count[k], k}' 파일

# 칸 값을 함수로 가공한다 (문자열 함수)
awk '{print length($1), substr($1, 1, 3), toupper($1)}' 파일
awk '{gsub(/정규식/, "바꿀것"); print}' 파일

# 첫 파일로 표를 만들고 둘째 파일에 쓴다 (두 파일을 함께 읽기)
awk 'NR==FNR {표[$1] = $2; next} {print 표[$1]}' 파일1 파일2

# 다른 명령의 출력을 가공한다 (다른 명령 출력 가공)
명령 | awk '{print $2}'
```

### 내장 변수

> 프로그램 안에서 값을 읽거나 정하는 awk 의 내장 변수입니다. 본문에 나온 것만 실었습니다.

뜻은 gawk(1) 의 내장 변수 항목을 옮긴 것입니다.[^gawk-builtin]

```bash
# NR        지금까지 읽은 줄 번호. 입력 파일을 가리지 않고 이어서 센다
# FNR       지금 읽는 파일 안의 줄 번호. 파일마다 1 로 돌아온다
# NF        지금 줄의 칸 수
# FILENAME  지금 읽는 입력 파일 이름
# OFS       출력 칸 구분자. 기본은 공백 하나
# ORS       출력 줄 구분자. 기본은 줄바꿈
```



## 종료 코드

> `awk` 는 정상 종료하면 0, `exit` 에 값을 주면 그 값, 치명 오류가 나면 2 를 돌려줍니다.

매뉴얼은 `exit` 값, 정상 종료, 일반 오류, 치명 오류를 따로 적습니다.[^awk-exit] 아래 예는 「실습 준비」 에서 만든 `app.log` 로 돌립니다.

```bash
# 0  정상 종료. exit 에 값을 주지 않아도 0 이다
# N  exit N 으로 준 값. 프로그램이 정한다
# 1  gawk 가 구문 오류 같은 일반 오류에 돌려준다 (mawk 는 구문 오류에도 2)
# 2  치명 오류. 없는 파일을 읽으려 할 때가 그렇다

# 값 없는 exit 는 0, 값이 있으면 그 값이다
awk 'BEGIN {exit}'; echo $?              # 0
awk 'BEGIN {exit 3}'; echo $?            # 3

# END 에서 exit !found 로 찾았으면 0, 못 찾았으면 1 로 끝낸다
awk '/ERROR/ {found = 1} END {exit !found}' app.log; echo $?    # 0
awk '/panic/ {found = 1} END {exit !found}' app.log; echo $?    # 1

# 중괄호를 닫지 않으면 구문 오류다. mawk 는 2, gawk 는 1 로 끝난다
awk 'BEGIN {'; echo $?     # awk: line 2: missing } near end of file / 2

# 없는 파일을 읽으면 오류 메시지를 내고 2 로 끝난다
awk 'END {print NR}' nofile.log; echo $?     # awk: cannot open nofile.log (No such file or directory) / 2
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것이며, 오류 메시지는 mawk 의 것입니다. gawk 는 없는 파일에서 ``awk: fatal: cannot open file `nofile.log' for reading: No such file or directory`` 를 내고 같은 2 로 끝납니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션만 씁니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 파일이 모두 생깁니다.

OrbStack 의 Linux VM 이나 `docker run -it --rm debian:12` 안에서 실행합니다.

```bash
mkdir -p ~/cmd-lab/awk && cd ~/cmd-lab/awk
cat > df.txt << 'EOF'
Filesystem     1024-blocks      Used Available Capacity Mounted on
/dev/sda1         41152736  17283548  21755756      45% /
/dev/sdb1        103081248  97927188         0     100% /data
/dev/sdc1         51474912  46327424   2509728      95% /var/log
tmpfs              8139112         0   8139112       0% /dev/shm
EOF
cat > access.log << 'EOF'
10.0.0.7 - - [10/Nov/2026:09:01:15 +0900] "GET /index.html HTTP/1.1" 200 5120
10.0.0.9 - - [10/Nov/2026:09:02:03 +0900] "GET /api/orders HTTP/1.1" 200 812
10.0.0.7 - - [10/Nov/2026:09:03:44 +0900] "POST /api/pay HTTP/1.1" 500 120
10.0.0.3 - - [10/Nov/2026:09:04:10 +0900] "GET /favicon.ico HTTP/1.1" 404 0
10.0.0.7 - - [10/Nov/2026:09:05:31 +0900] "POST /api/pay HTTP/1.1" 500 120
10.0.0.9 - - [10/Nov/2026:09:06:02 +0900] "GET /api/orders HTTP/1.1" 500 95
10.0.0.7 - - [10/Nov/2026:09:07:19 +0900] "GET /index.html HTTP/1.1" 200 5120
EOF
cat > owners.txt << 'EOF'
10.0.0.7 alice
10.0.0.9 bob
10.0.0.3 carol
EOF
cat > passwd.txt << 'EOF'
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
dev:x:1000:1000::/home/dev:/bin/sh
svc:x:1001:1001::/home/svc:/usr/sbin/nologin
EOF
cat > app.log << 'EOF'
2026-11-10 09:01:15 INFO  order-api started
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:14:41 WARN  retrying orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
2026-11-10 10:06:01 error db connection reset
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
2026-11-10 11:30:00 INFO  heartbeat
EOF
cat > users.csv << 'EOF'
id,name,city,score
1,kim,seoul,90
2,lee,busan,85
3,park,daegu,70
EOF
cat > hangul.txt << 'EOF'
가나다abc
한글:테스트:끝
EOF
```

`df.txt` 는 `df -P` 의 출력 꼴입니다. `-P` 는 장치 이름이 길어도 파일시스템 하나를 한 줄에 찍으므로 다섯째 칸이 늘 사용률입니다.[^df] `access.log` 는 일곱 줄짜리 접근 로그로 첫 칸이 클라이언트 IP, 아홉째 칸이 상태 코드, 열째 칸이 응답 바이트입니다.

`owners.txt` 는 IP 와 사용자 이름을 짝지은 세 줄이고 `passwd.txt` 는 `/etc/passwd` 꼴 네 줄입니다. `app.log` 는 일곱 줄짜리 애플리케이션 로그이고 `users.csv` 는 쉼표로 나뉜 표입니다. `hangul.txt` 는 한글이 든 두 줄입니다.

### 칸 번호와 줄 번호

> `$번호` 로 칸을 부르고 `-F` 로 칸 구분자를 바꿉니다.

기본 구분자는 공백이며 `awk` 는 연속 공백을 구분자 하나로 묶습니다.[^gawk-fields]

```bash
# 첫째와 다섯째 칸만 찍는다. head -2 는 앞 두 줄만 남긴다
awk '{print $1, $5}' df.txt | head -2
```

```bash
Filesystem Capacity
/dev/sda1 45%
```

```bash
# $0 은 줄 전체이고 NR 은 읽은 줄 번호다
awk '{print NR, $0}' df.txt | head -1
# 1 Filesystem     1024-blocks      Used Available Capacity Mounted on
```

```bash
# 구분자를 콜론으로 바꿔 계정 이름인 첫째 칸만 찍는다
#   -F fs   칸 구분자 FS 를 fs 로 정한다 (gawk 만 --field-separator)
awk -F: '{print $1}' passwd.txt | head -2
```

```bash
root
daemon
```

### 구분자 -F

> `-F` 로 칸을 가르는 구분자를 바꿉니다.

한 글자면 그 글자로 끊고 두 글자 이상이면 정규식으로 읽습니다.[^gawk-regexfs] 기본은 연속 공백(공백과 탭)을 하나로 묶는 것입니다.

```bash
# 쉼표로 나눠 둘째와 넷째 칸을 찍는다. NR>1 은 머리글 줄을 건너뛴다
awk -F, 'NR>1 {print $2, $4}' users.csv
```

```bash
kim 90
lee 85
park 70
```

```bash
# 두 글자 이상은 정규식이다. orderId= 뒤쪽이 둘째 칸이라 주문 번호만 나온다
awk -F'orderId=' '/orderId/ {print $2}' app.log
```

```bash
1001
1001
1002
```

```bash
# 공백과 = 를 모두 구분자로 삼는다. 마지막 칸이 주문 번호다
awk -F'[ =]' '/orderId/ {print $NF}' app.log
```

```bash
1001
1001
1002
```

```bash
# 탭만 구분자로 삼으면 공백이 든 값(b c)이 한 칸으로 남는다
printf 'a\tb c\n' | awk -F'\t' '{print $2}'      # b c

# -F 없이: 공백도 구분자라서 둘째 칸이 b
printf 'a\tb c\n' | awk '{print $2}'             # b
```

### 패턴과 동작

> 프로그램은 `패턴 { 동작 }` 꼴이고 패턴이 참인 줄에서만 동작하며, 둘 중 하나를 뺄 수 있습니다.

```bash
# 패턴이 참인 줄에서만 동작한다
awk '/sdb/ {print $6}' df.txt          # /data

# 동작을 빼면 맞은 줄을 그대로 찍는다
awk '/sdb/' df.txt
# /dev/sdb1        103081248  97927188         0     100% /data

# 패턴을 빼면 모든 줄에서 동작한다
awk '{print $6}' df.txt | head -2
# Mounted
# /

# BEGIN 은 첫 줄 전, END 는 마지막 줄 뒤에 한 번 돈다
awk 'BEGIN {print "start"} END {print "lines:", NR}' df.txt
# start
# lines: 5
```

### 칸에 정규식 걸기

> `~` 는 칸이 정규식과 맞는지, `!~` 는 맞지 않는지를 묻습니다.

`/정규식/` 만 쓰면 줄 전체에, 앞에 `!` 를 붙이면 맞지 않는 줄에 걸립니다.

```bash
# 여섯째 칸이 /data 나 /var 로 시작하는 줄의 마운트 지점만 나온다
awk '$6 ~ /^\/(data|var)/ {print $6}' df.txt
```

```bash
/data
/var/log
```

```bash
# 맞지 않는 줄이 나온다. 머리글은 NR>1 로 뺀다
awk 'NR>1 && $6 !~ /^\/(data|var)/ {print $6}' df.txt
```

```bash
/
/dev/shm
```

```bash
# 줄 전체가 tmpfs 와 맞지 않는 줄이라 tmpfs 줄만 빠진다
awk '!/tmpfs/ {print $1}' df.txt
```

```bash
Filesystem
/dev/sda1
/dev/sdb1
/dev/sdc1
```

```bash
# ==: 문자열이 정확히 같을 때. NR==2 는 줄 번호가 같을 때
awk '$NF == "/data" {print $5}' df.txt      # 100%
awk 'NR==2' df.txt                          # /dev/sda1         41152736  17283548  21755756      45% /
```

### 범위 패턴

> 패턴을 쉼표로 이으면 앞 패턴이 참이 된 줄부터 뒤 패턴이 참이 되는 줄까지를 고릅니다.

끝 패턴이 참이 된 줄도 포함합니다.[^gawk-range]

```bash
# WARN 줄부터 그다음 ERROR 줄까지 두 줄이 나온다
awk '/WARN/,/ERROR/' app.log
```

```bash
2026-11-10 09:14:41 WARN  retrying orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
```

```bash
# 줄 번호로 범위를 준다. 둘째와 셋째 줄이 나온다
awk 'NR==2,NR==3 {print NR, $6}' df.txt
```

```bash
2 /
3 /data
```

```bash
# 정규식 두 개로 받은 범위: sdb 줄부터 sdc 줄까지
awk '/sdb/,/sdc/ {print $1}' df.txt
```

```bash
/dev/sdb1
/dev/sdc1
```

### 칸 수와 마지막 칸

> `NF` 는 칸 수, `$NF` 는 마지막 칸, `$(NF-1)` 은 끝에서 둘째 칸입니다.

```bash
# 칸 수 NF 와 마지막 칸 $NF 를 찍는다
# 머리글은 Mounted on 이 두 칸으로 갈려 NF 가 7 이다
awk '{print NR, NF, $NF}' df.txt | head -2
```

```bash
1 7 on
2 6 /
```

```bash
# 끝에서 둘째 칸 $(NF-1) 로 머리글을 건너뛰고 사용률과 마운트 지점을 찍는다
awk 'NR>1 {print $(NF-1), $NF}' df.txt | head -2
```

```bash
45% /
100% /data
```

```bash
# UID 1000 이상·로그인 셸 계정(!~ 부정)
# 조건 두 개를 && 로 묶은 패턴이다. svc(1001)는 셸이 nologin 이라 !~ 에 걸려 빠진다
awk \
  -F: \
  '$3 >= 1000 && $7 !~ /(nologin|false)$/ {print $1, $3, $7}' \
  passwd.txt
# dev 1000 /bin/sh
```

`/etc/passwd` 구조는 [《Learning Modern Linux》 4장 노트](../../../book/learning-modern-linux/04-01.%EC%A0%84%EB%B6%80%20%EC%95%84%EB%8B%88%EB%A9%B4%20%EC%A0%84%EB%AC%B4%EC%97%90%EC%84%9C%20%EC%9E%98%EA%B2%8C%20%EC%AA%BC%EA%B0%9C%EB%8A%94%20%EC%AA%BD%EC%9C%BC%EB%A1%9C.md)에 있습니다.

### 외부 변수 -v 와 합계

> `-v 변수=값` 으로 셸의 값을 `awk` 프로그램에 넘깁니다.

`BEGIN` 이 돌기 전에 변수를 정해 줍니다.[^gawk-v]

```bash
# 사용률이 limit(90) 이상인 마운트 지점 /data 와 /var/log 를 한 줄로 잇는다
# $5+0 은 칸을 숫자로 바꿔 비교한다 (「awk 비교가 문자열로 떨어질 때」)
#   -v var=val   프로그램 변수를 미리 정한다 (gawk 만 --assign)
awk -v limit=90 'NR>1 && $5+0 >= limit {print $6}' df.txt | tr '\n' ' '   # /data /var/log
```

```bash
# -v 는 여러 번 줄 수 있다. 사용률이 50 이상 99 이하
awk -v lo=50 -v hi=99 'NR>1 && $5+0>=lo && $5+0<=hi {print $6, $5}' df.txt
```

```bash
/var/log 95%
```

```bash
# 합계: 변수에 더해 두고 END 에서 찍는다
awk 'NR>1 {sum += $3} END {print sum}' df.txt                     # 161538160
awk 'NR>1 {sum += $3} END {print sum, sum/(NR-1)}' df.txt          # 161538160 40384540
awk '$9 == 500 {n++} END {print n}' access.log                    # 3
```

### print 와 printf 서식

> `print` 는 값을 그대로, `printf` 는 서식에 맞춰 폭과 소수 자리를 정해 찍습니다.

`print` 는 쉼표로 이은 값을 `OFS` 로 잇고 줄 끝에 `ORS` 를 붙입니다. `printf` 는 줄바꿈을 직접 넣어야 합니다.

```bash
# 쉼표 없이 이으면 두 칸이 붙는다
awk '{print $1 $5}' df.txt | head -2
```

```bash
FilesystemCapacity
/dev/sda145%
```

```bash
# "|" 를 끼우면 그 글자로 구분된다
awk '{print $1 "|" $5}' df.txt | head -2
```

```bash
Filesystem|Capacity
/dev/sda1|45%
```

```bash
# printf: %-10s 왼쪽 정렬 10칸, %5d 정수 5칸, %8.2f 소수 둘, \n 은 직접 넣는다
awk 'NR>1 {printf "%-10s|%5d|%8.2f|\n", $6, $3, $3/$2*100}' df.txt
```

```bash
/         |17283548|   42.00|
/data     |97927188|   95.00|
/var/log  |46327424|   90.00|
/dev/shm  |    0|    0.00|
```

```bash
# %% 는 % 글자, %c 는 숫자면 그 코드의 글자 문자열이면 첫 글자, %e 는 지수 꼴
awk 'BEGIN {printf "%s %d%%\n", "cpu", 42}'      # cpu 42%
awk 'BEGIN {printf "%c%c\n", 65, "BCD"}'          # AB
awk 'BEGIN {printf "%e\n", 12345.678}'            # 1.234568e+04
```

```bash
# %% 로 % 를 붙여 사용률을 소수 한 자리로 찍는다
awk 'NR>1 {printf "%-10s %5.1f%%\n", $6, $3/$2*100}' df.txt | head -2
```

```bash
/           42.0%
/data       95.0%
```

### 출력 구분자 OFS 와 ORS

> `OFS` 는 `print` 가 칸 사이에 넣는 구분자, `ORS` 는 줄 끝에 붙이는 문자열입니다.

입력 줄을 그대로 찍는 `print` 는 `OFS` 를 쓰지 않으므로, 칸을 새 구분자로 다시 조립하려면 `$1=$1` 처럼 필드를 재할당해야 합니다.[^gawk-rebuild]

```bash
# 그냥 print: 줄을 그대로 찍는다
echo 'a   b    c' | awk '{print}'                    # a   b    c

# $1=$1: 칸을 다시 조립해 연속 공백이 OFS(공백 하나)로 바뀐다
echo 'a   b    c' | awk '{$1=$1; print}'             # a b c
```

```bash
# OFS: 출력 구분자. print $1, $5 처럼 쉼표로 이은 값 사이에 들어간다
awk 'BEGIN{OFS=","} {print $1, $5}' df.txt | head -2
```

```bash
Filesystem,Capacity
/dev/sda1,45%
```

```bash
# $1=$1 로 모든 칸을 새 OFS 로 다시 조립한다
awk 'BEGIN {OFS=","} NR>1 {$1=$1; print}' df.txt | head -1        # /dev/sda1,41152736,17283548,21755756,45%,/
```

```bash
# 명령줄에서 구분자를 준다. 탭은 \t
awk -v OFS='\t' 'NR>1 {print $6, $5}' df.txt | head -2
```

```bash
/	45%
/data	100%
```

```bash
# ORS: 줄 끝 문자열. 모든 줄을 공백으로 이어 한 줄로 만든다
awk -v ORS=' ' '{print $1}' owners.txt; echo      # 10.0.0.7 10.0.0.9 10.0.0.3

# printf 는 줄바꿈이 없으니 END 에서 한 번 넣는다
awk '{printf "%s ", $1} END {print ""}' owners.txt  # 10.0.0.7 10.0.0.9 10.0.0.3
```

### 연관 배열로 세기

> `count[$1]++` 처럼 칸 값을 첨자로 쓰면 값마다 세는 표가 됩니다.

배열 첨자는 숫자가 아니라 아무 문자열이나 됩니다. `for (ip in count)` 는 도는 순서가 정해져 있지 않아 `sort -rn` 과 함께 씁니다.

```bash
# IP 별 요청 수를 센다. sort -rn 은 숫자 내림차순으로 많은 쪽을 위로 올린다
awk '{count[$1]++} END {for (ip in count) print count[ip], ip}' access.log \
  | sort -rn
```

```bash
4 10.0.0.7
2 10.0.0.9
1 10.0.0.3
```

```bash
# 값을 더하는 집계. IP 별 응답 바이트 합계
awk '{bytes[$1] += $10} END {for (ip in bytes) print ip, bytes[ip]}' \
  access.log \
  | sort
```

```bash
10.0.0.3 0
10.0.0.7 10480
10.0.0.9 907
```

```bash
# !seen[$1]++: 처음 나온 값만 통과시킨다(중복 제거, 입력 순서 유지)
awk '!seen[$1]++ {print $1}' access.log
```

```bash
10.0.0.7
10.0.0.9
10.0.0.3
```

```bash
# length(배열): 서로 다른 첨자의 수
awk '{c[$9]++} END {print length(c)}' access.log      # 3

# (값 in 배열): 그 첨자가 있는가. 있으면 1
awk '{c[$9]++} END {print ("404" in c), ("302" in c)}' access.log      # 1 0
```

### 문자열 함수

> 글자 수, 일부 떼기, 쪼개기, 대소문자, 바꾸기를 함수로 합니다.

`sub` 는 첫 번째 일치만, `gsub` 는 모두 바꾸고 바꾼 횟수를 돌려줍니다.[^gawk-str]

```bash
# length($7): 요청 경로의 글자 수
awk '{print length($7)}' access.log | head -3
```

```bash
11
11
8
```

```bash
# 인자를 빼면 줄 전체의 길이다
awk '{print length}' owners.txt
```

```bash
14
12
14
```

```bash
# substr(문자열, 시작, 길이): 시작은 1부터. 길이를 빼면 끝까지
awk '{print substr($4, 2, 11)}' access.log | head -1      # 10/Nov/2026
awk '{print substr($4, 14)}' access.log | head -1         # 09:01:15
```

```bash
# split(문자열, 배열, 구분자): 쪼개 배열에 넣고 조각 수를 돌려준다
awk '{split($4, t, ":"); print t[2] "h"}' access.log | head -1      # 09h
awk '{n = split($1, o, "."); print n, o[4]}' access.log | head -1   # 4 7
```

```bash
# tolower / toupper: 대소문자 바꾸기
awk '{print toupper($3), tolower("ABC")}' app.log | head -1         # INFO abc

# tolower 로 대소문자를 맞춰 센다. error·ERROR·[ERROR] 를 모두 센다
awk 'tolower($0) ~ /error/ {n++} END {print n}' app.log             # 4
```

```bash
# sub(정규식, 바꿀문자열): 줄에서 처음 맞은 곳 하나만 바꾼다
# sed -n 2,3p 는 둘째와 셋째 줄만 보여 준다
awk '{sub(/ERROR/, "E"); print}' app.log | sed -n 2,3p
```

```bash
2026-11-10 09:14:40 E payment timeout orderId=1001
2026-11-10 09:14:41 WARN  retrying orderId=1001
```

```bash
# gsub: 모두 바꾸고 바꾼 횟수를 돌려준다. 숫자 다섯 개가 # 로 바뀐다
awk '{n = gsub(/[0-9]/, "#"); print n, $0}' owners.txt | head -1      # 5 ##.#.#.# alice

# 대상을 칸으로 줄 수 있다. 날짜의 - 를 / 로
awk '{gsub(/-/, "/", $1); print $1}' app.log | head -1                 # 2026/11/10
```

### 두 파일을 함께 읽기

> 첫 파일을 읽는 동안에만 `NR==FNR` 이 참이라서, 첫 파일로 표를 만들고 둘째 파일을 그 표로 풀어 씁니다.

`NR` 은 파일을 가리지 않고 이어서 세고 `FNR` 은 파일마다 1 로 돌아옵니다.[^gawk-vars]

```bash
# FNR 은 파일마다 다시 센 줄 번호, FILENAME 은 지금 읽는 파일이다. NR 은 계속 센다
awk 'FNR==1 {print FILENAME, FNR, NR}' owners.txt access.log
```

```bash
owners.txt 1 1
access.log 1 4
```

```bash
# NR==FNR: 첫 파일 읽는 중. name 표를 만들고 next 로 다음 줄로 간다
awk 'NR==FNR {name[$1] = $2; next} {print name[$1], $7}' owners.txt access.log
```

```bash
alice /index.html
bob /api/orders
alice /api/pay
carol /favicon.ico
alice /api/pay
bob /api/orders
alice /index.html
```

```bash
# 파일마다 줄 수: 첫 파일이 3줄이고 NR 은 둘을 합친 10
awk 'NR==FNR {n++; next} END {print n, NR}' owners.txt access.log      # 3 10
```

### 다른 명령 출력 가공

> `free` 와 `/proc/loadavg` 의 출력에서 칸을 골라 비율과 부하를 계산합니다.

`free` 의 `Mem:` 행에서는 일곱째 칸 `available` 을 둘째 칸 `total` 로 나눕니다.[^free] `/proc/loadavg` 에서는 첫 칸인 1분 평균 부하를 코어 수와 견줍니다.[^loadavg]

```bash
# 두 값은 돌릴 때마다 달라진다
# free 는 procps 패키지에 있어 최소 컨테이너에는 없을 수 있다
free -m | awk '/^Mem:/ {printf "%.1f%%\n", $7/$2*100}'           # 76.4%
awk -v n="$(nproc)" '{print ($1 > n ? "over" : "ok"), $1, n}' /proc/loadavg   # ok 0.71 8
```

지표 원리는 [《Learning Modern Linux》 8장 둘째 노트](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md)에서 봅니다.



## 주의사항과 동작 원리

> 비교는 칸이 숫자 꼴인지에 따라 숫자나 문자열로 갈리고, 글자 수는 구현과 로캘에 따라 달라집니다.

### awk 비교가 문자열로 떨어질 때

> `95%` 처럼 숫자 꼴이 아닌 칸은 문자열로 비교되므로 임계 비교는 칸을 숫자로 바꿔서 합니다.

사용률 90% 이상을 고를 때 `$5 >= 90` 으로 쓰면 100% 를 놓칩니다.

```bash
# 95% 는 숫자 꼴이 아니라 문자열 비교다. 앞 글자부터 견주므로 1 로 시작하는 100% 가
# 9 로 시작하는 90 보다 작아 빠지고 /var/log 95% 만 나온다
# NR>1 을 빼고 awk '$5 > 9 {print $5}' df.txt 로 쓰면 머리글의 Capacity 까지 나온다
awk 'NR>1 && $5 >= 90 {print $6, $5}' df.txt      # /var/log 95%

# $5+0 은 칸을 숫자로 바꿔 /data 100% 와 /var/log 95% 가 모두 나온다
# grep '9[0-9]%' 처럼 패턴으로 임계를 흉내 내면 100% 를 놓친다
awk 'NR>1 && $5+0 >= 90 {print $6, $5}' df.txt
# /data 100%
# /var/log 95%
```

`awk` 는 칸 내용이 숫자 꼴일 때만 숫자로 비교합니다. `95%` 는 `%` 때문에 문자열이며 한쪽이 문자열이면 문자열 비교가 됩니다.[^gawk-cmp] `$5+0` 처럼 산술 연산을 걸면 앞머리의 숫자 부분만 수로 바뀝니다(100% 는 100).[^gawk-conv]

### 문자열 상수와 숫자 상수의 비교

> 따옴표로 쓴 값은 문자열이라 숫자와 견줘도 문자열 비교가 됩니다.

칸이 아니라 코드에 직접 쓴 값도 같은 규칙을 따릅니다.

```bash
# "5" 는 문자열이라 10 과도 문자열로 견준다. "5" < "10" 은 거짓(0)
awk 'BEGIN {x = "5"; y = 10; print (x < y), ("5" < "10")}'
```

```bash
0 0
```

```bash
# 따옴표 문자열 둘은 글자 순서로 견준다("10" < "9" 는 참). +0 을 걸면 수로 견준다
awk 'BEGIN {print ("10" < "9"), (10 < 9), ("10"+0 < "9"+0)}'      # 1 0 0
```

### 한글과 length

> `length` 와 `substr` 이 세는 단위는 구현마다 달라, mawk 는 늘 바이트를 세고 gawk 는 로캘이 UTF-8 이면 글자를 셉니다.

컨테이너 기본 로캘(POSIX)에서는 gawk 도 바이트를 셉니다.[^gawk-multibyte]

```bash
# 기본 로캘(POSIX): gawk·mawk 모두 바이트. 가나다abc 는 3×3+3 = 12
awk '{print length($0)}' hangul.txt
```

```bash
12
20
```

```bash
# LC_ALL=C.UTF-8 로 바꾸면 gawk 는 글자 수를 센다(6, 8). mawk 는 여전히 12, 20
LC_ALL=C.UTF-8 awk '{print length($0)}' hangul.txt
```

```bash
6
8
```

```bash
# substr 도 같다. gawk 는 C.UTF-8 에서 가나, 한글. mawk 는 바이트 둘이라 글자가 깨진다
LC_ALL=C.UTF-8 awk '{print substr($0, 1, 2)}' hangul.txt
```

```bash
가나
한글
```

위 출력은 gawk 5.2.1 입니다. 한글이 든 줄을 자르거나 길이를 잴 때는 `awk` 가 gawk 인지 로캘이 무엇인지에 따라 결과가 달라지므로 먼저 확인합니다.



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [cut 참조 시트](./cut.md) — 구분자 하나로 자르는 단순한 경우
- [sort·uniq·wc 참조 시트](./sort%C2%B7uniq%C2%B7wc.md) — 뽑은 칸을 정렬하고 세기
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- gawk 5.2.1 의 `gawk --help`·`man gawk` 와 mawk 1.3.4 의 `mawk -W usage` 원문 — Debian 12 컨테이너에서 2026-11-13 출력
- [GNU awk 매뉴얼](https://www.gnu.org/software/gawk/manual/gawk.html) — 2026-11-10 조회

[^df]: GNU coreutils 매뉴얼, "df invocation" 의 `-P` — "The information about each file system is always printed on exactly one line". <https://www.gnu.org/software/coreutils/manual/coreutils.html#df-invocation>
[^gawk-fields]: GNU awk 매뉴얼, "Specifying How Fields Are Separated" — "Fields are separated by runs of whitespace". <https://www.gnu.org/software/gawk/manual/gawk.html#Field-Separators>
[^gawk-cmp]: GNU awk 매뉴얼, "Variable Typing and Comparison Expressions" — 숫자 꼴인 칸만 strnum 속성을 갖고, 한쪽이 문자열이면 문자열로 비교합니다. <https://www.gnu.org/software/gawk/manual/gawk.html#Variable-Typing>
[^gawk-conv]: GNU awk 매뉴얼, "Conversion of Strings and Numbers" — "A string is converted to a number by interpreting any numeric prefix of the string as numerals". <https://www.gnu.org/software/gawk/manual/gawk.html#Strings-And-Numbers>
[^gawk-rebuild]: GNU awk 매뉴얼, "Changing the Contents of a Field". <https://www.gnu.org/software/gawk/manual/gawk.html#Changing-Fields>
[^free]: `free(1)` 의 `available` 항목. <https://man7.org/linux/man-pages/man1/free.1.html>
[^loadavg]: `proc_loadavg(5)` — 앞의 세 칸이 1분·5분·15분 평균 부하입니다. <https://man7.org/linux/man-pages/man5/proc_loadavg.5.html>
[^gawk-regexfs]: GNU awk 매뉴얼, "Using Regular Expressions to Separate Fields" — "the value of FS may be a string containing any regular expression. In this case, each match in the record for the regular expression separates fields". <https://www.gnu.org/software/gawk/manual/gawk.html#Regexp-Field-Splitting>
[^gawk-range]: GNU awk 매뉴얼, "Specifying Record Ranges with Patterns" — "The record that turns on the range pattern and the one that turns it off both match the range pattern". <https://www.gnu.org/software/gawk/manual/gawk.html#Ranges>
[^gawk-str]: gawk(1), 함수 항목 — "gsub(r, s [, t]) For each substring matching the regular expression r in the string t, substitute the string s, and return the number of substitutions", "substr(s, i [, n]) Return the at most n-character substring of s starting at i. If n is omitted, use the rest of s", "With an array argument, length() returns the number of elements in the array". <https://manpages.debian.org/bookworm/gawk/gawk.1.en.html>
[^gawk-multibyte]: gawk(1) — `length([s])` 는 "the length of the string s"(문자열 s 의 길이)이고, `-b` 는 "Treat all input data as single-byte characters". 컨테이너 로캘별 결과는 이 시트의 실측입니다. <https://manpages.debian.org/bookworm/gawk/gawk.1.en.html>
[^gawk-vars]: gawk(1), 내장 변수 — "FNR The input record number in the current input file", "NR The total number of input records seen so far", "FILENAME The name of the current input file". <https://manpages.debian.org/bookworm/gawk/gawk.1.en.html>
[^gawk-v]: GNU awk 매뉴얼, "Assigning Variables on the Command Line" — "the variable is set at the very beginning, even before the BEGIN rules execute". <https://www.gnu.org/software/gawk/manual/gawk.html#Assignment-Options>
[^gawk-builtin]: gawk(1), 내장 변수 — "FILENAME The name of the current input file.", "FNR The input record number in the current input file.", "NF The number of fields in the current input record.", "NR The total number of input records seen so far.", "OFS The output field separator, a space by default.", "ORS The output record separator, by default a newline." (gawk 5.2.1, Debian 12 의 `man gawk`) <https://manpages.debian.org/bookworm/gawk/gawk.1.en.html>
[^awk-exit]: `gawk(1)` 의 EXIT STATUS (gawk 5.2.1, Debian 12 의 `man gawk`) — "If the exit statement is used with a value, then gawk exits with the numeric value given to it. Otherwise, if there were no problems during execution, gawk exits with the value of the C constant EXIT_SUCCESS. This is usually zero. If an error occurs, gawk exits with the value of the C constant EXIT_FAILURE. This is usually one. If gawk exits because of a fatal error, the exit status is 2." <https://manpages.debian.org/bookworm/gawk/gawk.1.en.html>
