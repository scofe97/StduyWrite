---
title: time 참조 시트
tags: [linux, cheatsheet, time, gnu-time, bash, performance, cli, reference]
status: draft
source:
  - GNU bash 5.3 매뉴얼 (Pipelines, Bash Variables 의 TIMEFORMAT)와 `help time`·`help type` 원문 (Ubuntu 26.04)
  - GNU time 1.9 time(1) (Ubuntu 26.04 `man time`·`/usr/bin/time --help` 원문, manpages.debian.org bookworm 같은 판)
  - Linux man-pages getrusage(2)
related:
  - ../README.md
  - ../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md
updated: 2026-11-16
---

# time 참조 시트

---

> 명령 앞에 `time` 을 붙여 걸린 시간을 `real`·`user`·`sys` 로 재는 방법을, bash 키워드와 GNU time 두 가지로 나눠 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `time` 은 명령을 실행하고 끝난 뒤 걸린 시간과 CPU 시간을 표준 오류로 알려 줍니다.

`time` 은 이름이 같은 두 가지입니다. 하나는 bash 의 예약어(키워드)이고 다른 하나는 `time` 패키지의 `/usr/bin/time`(GNU time 1.9)입니다. bash 에서 앞에 아무것도 붙이지 않고 치면 키워드가 먼저 잡힙니다.[^bash-pipeline]

이 시트는 Ubuntu 26.04 VM(bash 5.3.9, time 1.9-0.4)에서 실측했습니다. 이 VM 의 `sleep`·`sort`·`dd` 는 rust-coreutils(uutils 0.10.0)입니다. macOS 의 `/usr/bin/time` 은 BSD 판이라 `-v` 가 없고 `-l` 을 씁니다.[^bsd-time]

`/usr/bin/time` 은 옵션을 명령보다 앞에 써야 하고 명령 없이 부르면 오류와 코드 125 가 나옵니다. 코드 값은 「종료 코드」 에 있습니다.



## 핵심 문법

> bash 키워드는 `TIMEFORMAT` 변수로, GNU time 은 `-f`·`-v` 로 출력 모양을 정하고, 둘 다 잰 명령 뒤에 시간을 표준 오류로 찍습니다.

```bash
# 호출 형태. 첫 줄은 help time 의 첫 줄, 둘째 줄은 /usr/bin/time --help 의 Usage 줄
time: time [-p] pipeline
Usage: /usr/bin/time [OPTIONS] COMMAND [ARG]...

# 어느 time 이 실행되는지 본다 (키워드와 외부 명령 구분)
type -a time

# 명령 하나를 재고 real·user·sys 를 읽는다 (걸린 시간을 세 값으로 읽기)
time COMMAND

# 스레드 수를 바꿔 가며 읽는다 (CPU 여럿이 일할 때의 user)
time sort -n --parallel=N 파일

# 파이프라인 전체와 첫 명령만 잰다 (파이프라인 전체와 첫 명령)
time COMMAND1 | COMMAND2
/usr/bin/time COMMAND1 | COMMAND2

# 출력 모양을 바꾼다 (출력 모양 바꾸기)
TIMEFORMAT=형식; time COMMAND
/usr/bin/time -f 형식 COMMAND

# 결과를 변수나 파일로 받는다 (시간을 변수나 파일로 받기)
{ time COMMAND; } 2> 파일
/usr/bin/time -o 파일 COMMAND

# 메모리와 문맥 전환까지 본다 (최대 메모리와 문맥 전환)
/usr/bin/time -v COMMAND

# 잰 명령의 종료 코드를 함께 남긴다 (종료 코드를 함께 남기기)
/usr/bin/time -f '%x' COMMAND
```

### TIMEFORMAT 지정자

> bash 키워드 `time` 의 출력 모양을 정하는 `TIMEFORMAT` 에 쓰는 지정자입니다.

뜻은 bash 매뉴얼의 TIMEFORMAT 항목을 따랐습니다.[^timeformat]

```bash
# TIMEFORMAT 안에 쓴다. 가운데 열은 계산 스크립트(cpu.sh)를 잰 값이다
# %R    0.292       경과 시간(초)
# %U    0.291       user 모드 CPU 초
# %S    0.000       system 모드 CPU 초
# %P    99.00       CPU 사용률. (%U + %S) / %R
# %lR   0m0.292s    l 을 붙이면 분·초 꼴(MMmSS.FFs)
# %2R   0.29        앞의 숫자가 소수 자리 수. 기본은 3 자리
# %%    %           % 글자 그대로
```

### -f 형식 지정자

> GNU time 의 `-f` 에 쓰는 지정자입니다. 본문에 나온 것만 실었습니다.

뜻은 `man time` 의 FORMATTING THE OUTPUT 을 따랐습니다.[^gnu-format]

```bash
# -f 안에 쓴다. 가운데 열은 sort -n rand.txt 를 잰 값이라 실행마다 조금 다르다
# %C    sort -n rand.txt   명령과 인자
# %e    0.40               경과 시간(초)
# %E    0:00.40            경과 시간. [시:]분:초 꼴
# %U    0.77               user 모드 CPU 초
# %S    0.02               system 모드 CPU 초
# %P    196%               CPU 사용률. 코어 여럿이면 100% 를 넘는다
# %M    181548             최대 상주 메모리(KB)
# %R    1479               minor 페이지 폴트 수
# %F    0                  major 페이지 폴트 수(I/O 가 필요한 것)
# %w    42                 자발적 문맥 전환 수(I/O 를 기다리며)
# %c    771                비자발적 문맥 전환 수(타임 슬라이스 소진)
# %x    0                  잰 명령의 종료 코드
# %%    %                  % 글자 그대로
```



## 종료 코드

> `/usr/bin/time` 은 잰 명령의 종료 코드를 그대로 돌려주고, 키워드 `time` 은 파이프라인의 종료 상태를 돌려줍니다.[^time-exit]

```bash
# 0        잰 명령이 성공했을 때
# N        잰 명령이 N 으로 끝났을 때. time 이 그 값을 그대로 돌려준다
# 128+N    잰 명령이 N 번 신호로 끝났을 때 (man time 의 DIAGNOSTICS)
# 125      GNU time 에 명령이 없거나 모르는 옵션을 줬을 때. man 에 없는 실측값이다
# 127      GNU time 이 명령을 실행하지 못했을 때. man 에 없는 실측값이다

# 잰 명령의 코드를 그대로 돌려준다
#   -o FILE   통계를 표준 오류 대신 FILE 에 쓴다 (--output)
/usr/bin/time -o /dev/null sh -c 'exit 3'; echo $?    # 3

# 신호로 끝나면 128 + 신호 번호다
/usr/bin/time -o /dev/null sh -c 'kill -9 $$'; echo $?    # 137

# 없는 명령은 127 이다
/usr/bin/time -o /dev/null /nonexistent; echo $?
# /usr/bin/time: cannot run /nonexistent: No such file or directory / 127

# 명령 없이 부르면 125 다
/usr/bin/time; echo $?
# /usr/bin/time: missing program to run / Try '/usr/bin/time --help' for more information. / 125

# 키워드는 파이프라인의 상태를 돌려준다. TIMEFORMAT 를 비우면 시간 출력이 없다
( TIMEFORMAT=; time false; echo $? )    # 1
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다. GNU time 은 잰 명령이 실패하면 통계 앞에 `Command exited with non-zero status N` 줄을 더합니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션만 씁니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 파일이 모두 생깁니다.

OrbStack 의 Linux VM(Ubuntu 26.04)에서 실행합니다. `time` 패키지는 기본으로 깔려 있지 않아 첫 줄이 설치합니다.

```bash
# GNU time(/usr/bin/time). 「키워드와 외부 명령 구분」 부터 여러 곳에서 쓴다
sudo apt-get install -y time

# 작업 폴더
mkdir -p ~/cmd-lab/time && cd ~/cmd-lab/time

# cpu.sh: 반복문 30만 회를 도는 계산 작업.
# 「걸린 시간을 세 값으로 읽기」·「출력 모양 바꾸기」에서 쓴다
printf '%s\n' 'i=0' 'while ((i < 300000)); do ((i++)); done' > cpu.sh

# rand.txt: 1 부터 900만 사이 무작위 수 200만 줄.
# 「CPU 여럿이 일할 때의 user」·「최대 메모리와 문맥 전환」에서 쓴다
shuf -i 1-9000000 -n 2000000 > rand.txt
```

### 키워드와 외부 명령 구분

> 같은 `time` 이 bash 키워드일 수도 외부 명령일 수도 있고, 어느 쪽인지에 따라 출력 모양이 다릅니다.

```bash
# time 이 무엇으로 풀리는지 본다
#   type -a   같은 이름의 해석 결과를 모두 보인다
#   command -v   실행될 것 하나를 한 단어로 보인다
type -a time
command -v time    # time
```

```bash
time is a shell keyword
time is /usr/bin/time
time is /bin/time
```

`/bin` 은 `/usr/bin` 으로 이어지는 심볼릭 링크라 둘째·셋째 줄은 같은 파일입니다.

```bash
# 키워드 time. 앞에 빈 줄이 있는 세 줄이 나온다
time sleep 1
```

```bash

real	0m1.003s
user	0m0.001s
sys	0m0.001s
```

```bash
# 외부 time. 한 줄 요약과 한 줄 통계가 나온다
/usr/bin/time sleep 1
```

```bash
0.00user 0.00system 0:01.00elapsed 0%CPU (0avgtext+0avgdata 7680maxresident)k
0inputs+0outputs (0major+376minor)pagefaults 0swaps
```

### 걸린 시간을 세 값으로 읽기

> `real` 은 벽시계로 잰 시간이고 `user`·`sys` 는 CPU 를 쓴 시간이라, 세 값을 견주면 계산했는지 기다렸는지 가려집니다.

세 값의 정의와 읽는 기준은 책 노트 [자원마다 창이 따로 나 있어 어느 창을 여느냐가 곧 진단이다](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md#3-time-의-cpu-시간과-대기)에 있고, 이 시트는 명령을 치는 법만 다룹니다.

```bash
# 1초 잠. 기다리는 동안은 CPU 를 쓰지 않아 real 만 1초다
time sleep 1
```

```bash

real	0m1.006s
user	0m0.001s
sys	0m0.004s
```

```bash
# 반복문 계산. 거의 전부 user 다
time bash cpu.sh
```

```bash

real	0m0.230s
user	0m0.227s
sys	0m0.002s
```

```bash
# 1바이트씩 40만 번 읽고 쓴다. 시스템 콜이 많아 sys 가 user 보다 크다
#   if=FILE    읽을 파일. /dev/zero 는 0 바이트를 끝없이 준다
#   of=FILE    쓸 파일. /dev/null 은 받아서 버린다
#   bs=BYTES   한 번에 읽고 쓰는 크기
#   count=N    N 번 읽고 멈춘다
#   2>/dev/null   dd 의 통계 줄은 버린다. time 의 출력은 이것과 상관없이 나온다
time dd \
  if=/dev/zero \
  of=/dev/null \
  bs=1 \
  count=400000 \
  2>/dev/null
```

```bash

real	0m0.098s
user	0m0.036s
sys	0m0.062s
```

### CPU 여럿이 일할 때의 user

> 스레드가 여럿이면 CPU 시간이 동시에 쌓여 `user` 가 `real` 보다 커질 수 있습니다.

```bash
# 스레드 하나로 정렬한다. real 과 user 가 거의 같다
#   -n   숫자로 견준다 (--numeric-sort)
#   --parallel=N   동시에 도는 스레드 수
time sort \
  -n \
  --parallel=1 \
  rand.txt > /dev/null
```

```bash

real	0m0.748s
user	0m0.721s
sys	0m0.026s
```

```bash
# 스레드 넷으로 정렬한다. real 은 줄고 user 는 real 의 두 배 가까이 된다
time sort \
  -n \
  --parallel=4 \
  rand.txt > /dev/null
```

```bash

real	0m0.424s
user	0m0.769s
sys	0m0.012s
```

이 경우에는 `real` 에서 `user`+`sys` 를 빼도 기다린 시간이 나오지 않습니다. 두 값을 CPU 가 일한 총량과 걸린 시간이라는 별개의 축으로 읽어야 합니다.

### 파이프라인 전체와 첫 명령

> 키워드 `time` 은 파이프라인 전체를 재고, 외부 `time` 은 바로 뒤의 명령 하나만 잽니다.

```bash
# 키워드는 파이프라인 전체를 잰다. 뒤의 sleep 2 까지 real 이 2초다
time sleep 1 | sleep 2
```

```bash

real	0m2.005s
user	0m0.001s
sys	0m0.005s
```

```bash
# 외부 time 은 첫 명령 sleep 1 만 잰다. elapsed 가 1초다
/usr/bin/time sleep 1 | sleep 2
```

```bash
0.00user 0.00system 0:01.00elapsed 0%CPU (0avgtext+0avgdata 7688maxresident)k
0inputs+0outputs (0major+383minor)pagefaults 0swaps
```

```bash
# 파이프라인 전체를 외부 time 으로 재려면 sh -c 로 감싼다. elapsed 가 2초다
/usr/bin/time sh -c 'sleep 1 | sleep 2'
```

```bash
0.00user 0.00system 0:02.00elapsed 0%CPU (0avgtext+0avgdata 7596maxresident)k
0inputs+0outputs (0major+859minor)pagefaults 0swaps
```

### 출력 모양 바꾸기

> 키워드는 `TIMEFORMAT` 변수로, GNU time 은 `-p`·`-f` 로 출력 모양을 바꿉니다.

```bash
# 경과 시간만 초 단위로 찍는다
TIMEFORMAT='%R seconds'
time sleep 1    # 1.008 seconds

# 분·초 꼴(%l)로 세 값을 한 줄에 찍는다
TIMEFORMAT=$'real %lR / user %lU / sys %lS'
time sleep 1    # real 0m1.005s / user 0m0.000s / sys 0m0.003s

# 소수 3자리와 CPU 사용률을 찍는다
TIMEFORMAT='%3R %P'
time bash cpu.sh    # 0.298 100.00

# 변수를 지우면 기본 모양으로 돌아온다. -p 는 POSIX 모양으로 찍는다
#   -p   POSIX 모양. real·user·sys 를 소수 둘째 자리까지 찍는다
unset TIMEFORMAT
time -p sleep 1
```

```bash
real 1.01
user 0.00
sys 0.00
```

```bash
# GNU time 도 -p 로 같은 모양을 낸다
/usr/bin/time -p sleep 1
```

```bash
real 1.00
user 0.00
sys 0.00
```

```bash
# -f 로 지정자를 골라 한 줄로 찍는다
#   -f FORMAT   기본 모양 대신 FORMAT 으로 찍는다 (--format)
/usr/bin/time -f 'wall %e s / cpu %P / exit %x' sleep 1    # wall 1.01 s / cpu 0% / exit 0
/usr/bin/time -f '%E' sleep 1                              # 0:01.00
```

### 시간을 변수나 파일로 받기

> 시간은 잰 명령이 아니라 `time` 이 표준 오류로 찍으므로, 그 표준 오류를 따로 받아야 합니다.

```bash
# 키워드 time 은 중괄호로 묶어 그 바깥의 2> 로 받는다
{ time sleep 1; } 2> keyword.txt
cat keyword.txt
```

```bash

real	0m1.006s
user	0m0.001s
sys	0m0.003s
```

```bash
# 숫자 하나만 변수에 담는다. 잰 명령의 출력은 /dev/null 로 버린다
t=$( { TIMEFORMAT=%R; time sleep 1 >/dev/null; } 2>&1 )
echo "$t"    # 1.005
```

```bash
# GNU time 은 -o 로 파일에 쓰고 -a 로 이어 붙인다
#   -a   -o 로 준 파일 끝에 덧붙인다 (--append)
/usr/bin/time -o gnu.txt -f '%e s %C' sleep 1
/usr/bin/time -a -o gnu.txt -f '%e s %C' sleep 2
cat gnu.txt
```

```bash
1.00 s sleep 1
2.00 s sleep 2
```

```bash
# -a 가 없으면 파일을 덮어쓴다. 줄이 하나만 남는다
/usr/bin/time -o gnu.txt -f '%e s %C' sleep 1
wc -l < gnu.txt    # 1

rm keyword.txt gnu.txt
```

### 최대 메모리와 문맥 전환

> GNU time 의 `-v` 와 `-f` 는 최대 상주 메모리, 페이지 폴트, 문맥 전환까지 찍습니다.

```bash
# -v 는 모든 항목을 한 줄씩 영어 설명과 함께 찍는다
#   -v   기본 모양 대신 상세 모양으로 찍는다 (--verbose)
# 통계는 표준 오류로 나오므로 2>&1 으로 모으고 sort 의 출력은 버린다
/usr/bin/time -v sort -n rand.txt 2>&1 >/dev/null
```

```bash
	Command being timed: "sort -n rand.txt"
	User time (seconds): 0.71
	System time (seconds): 0.01
	Percent of CPU this job got: 189%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:00.38
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 184092
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 1511
	Voluntary context switches: 58
	Involuntary context switches: 1467
	Swaps: 0
	File system inputs: 0
	File system outputs: 0
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
```

```bash
# 필요한 항목만 -f 로 골라 한 줄로 찍는다. 정렬은 메모리를 쓰고 CPU 를 다툰다
/usr/bin/time \
  -f 'rss %M KB / minor %R / major %F / vol %w / invol %c' \
  sort -n rand.txt >/dev/null
# rss 183420 KB / minor 1363 / major 0 / vol 83 / invol 1330

# 잠만 자는 명령은 메모리가 작고 비자발적 전환이 없다
/usr/bin/time \
  -f 'rss %M KB / minor %R / major %F / vol %w / invol %c' \
  sleep 1
# rss 7436 KB / minor 379 / major 0 / vol 2 / invol 0
```

문맥 전환 수는 실행마다 크게 달라지므로 큰지 작은지만 봅니다.

### 종료 코드를 함께 남기기

> `%x` 로 잰 명령의 종료 코드를 통계 줄에 넣고, 실패 경고는 `-q` 로 끌 수 있습니다.

```bash
# 잰 명령이 3 으로 끝났다. time 이 경고 줄을 먼저 찍고 -f 모양이 이어진다
/usr/bin/time -f '%e s exit %x' sh -c 'sleep 1; exit 3'; echo $?
```

```bash
Command exited with non-zero status 3
1.00 s exit 3
3
```

```bash
# 경고 줄만 끈다. 종료 코드는 그대로 3 이다
#   -q   비정상 종료(0 이 아닌 코드·신호)의 경고를 찍지 않는다 (--quiet)
/usr/bin/time -q -f '%e s exit %x' sh -c 'sleep 1; exit 3'; echo $?
```

```bash
1.00 s exit 3
3
```

### 실습 정리

```bash
# 실습 폴더를 지운다
cd ~ && rm -rf ~/cmd-lab/time
```



## 주의사항과 동작 원리

### 키워드 time 뒤의 리다이렉션

> `time 명령 2>/dev/null` 은 시간 출력을 막지 못하고, 중괄호로 묶어야 막힙니다.

```bash
# 2> 는 잰 명령 sleep 에 걸리고 시간은 셸이 따로 찍는다
time sleep 1 2>/dev/null

# 묶으면 셸의 표준 오류까지 걸린다
{ time sleep 1; } 2>/dev/null
```

```bash

real	0m1.005s
user	0m0.000s
sys	0m0.002s
```

키워드는 파이프라인이 끝난 뒤 셸이 통계를 찍으므로 파이프라인 안의 리다이렉션이 닿지 않습니다.[^bash-pipeline] 첫 줄의 출력만 나오고 둘째 줄은 아무것도 나오지 않습니다.

### 셸 함수와 내장 재기

> 외부 `time` 은 프로그램 파일만 실행할 수 있어 셸 함수를 잴 수 없습니다.

```bash
# 함수를 키워드로 잰다
bash -c 'f() { sleep 1; }; time f'
```

```bash

real	0m1.004s
user	0m0.000s
sys	0m0.001s
```

```bash
# 같은 함수를 외부 time 으로 재면 파일을 찾다 실패한다
bash -c 'f() { sleep 1; }; /usr/bin/time -o /dev/null f; echo $?'
# /usr/bin/time: cannot run f: No such file or directory / 127
```

bash 매뉴얼은 예약어여서 셸 내장·함수·파이프라인을 잴 수 있고 외부 명령은 이를 잘 재지 못한다고 적습니다.[^bash-pipeline]

### sh 와 env 앞에서는 외부 time

> `sh` 가 dash 인 시스템에서는 `sh -c 'time …'` 이 키워드가 아니라 `/usr/bin/time` 을 실행하고, `env` 뒤에서도 같습니다.

```bash
# 이 VM 에서 /bin/sh 는 dash 다. 키워드가 없어 PATH 에서 time 을 찾는다
sh -c 'time sleep 1'
bash -c 'time sleep 1'
env time sleep 1
```

```bash
0.00user 0.00system 0:01.00elapsed 0%CPU (0avgtext+0avgdata 7640maxresident)k
0inputs+0outputs (0major+378minor)pagefaults 0swaps

real	0m1.007s
user	0m0.001s
sys	0m0.002s
0.00user 0.00system 0:01.00elapsed 0%CPU (0avgtext+0avgdata 9716maxresident)k
0inputs+0outputs (0major+374minor)pagefaults 0swaps
```

`#!/bin/sh` 로 시작하는 스크립트에서 `time` 의 출력 모양이 달라지면 이 때문입니다.

### GNU time 옵션은 명령 앞에만

> 명령 뒤에 쓴 옵션은 `time` 이 아니라 잰 명령에 넘어갑니다.

```bash
# -v 는 time 이 아니라 echo 의 인자다
/usr/bin/time echo hi -v
```

```bash
hi -v
0.00user 0.00system 0:00.00elapsed 33%CPU (0avgtext+0avgdata 7116maxresident)k
0inputs+0outputs (0major+372minor)pagefaults 0swaps
```

`man time` 은 "Options to time must appear on the command line before COMMAND." 라고 적습니다.[^gnu-format]

### 최대 메모리는 가장 큰 자식 하나

> `%M` 은 자식들의 합이 아니라 가장 큰 자식의 최대 상주 메모리입니다.

```bash
# sort 를 한 번, 두 번 잰다. 값이 두 배가 되지 않는다
/usr/bin/time -f '%M' sort -n rand.txt >/dev/null
# 181260
/usr/bin/time -f '%M' sh -c 'sort -n rand.txt >/dev/null; sort -n rand.txt >/dev/null'
# 183604
```

GNU time 은 `wait3(2)` 가 돌려주는 자원 사용량을 찍습니다. `getrusage(2)` 는 자식의 `ru_maxrss` 가 가장 큰 자식 하나의 값이지 프로세스 트리 전체의 최댓값이 아니라고 설명합니다.[^rss-max]



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [자원마다 창이 따로 나 있어 어느 창을 여느냐가 곧 진단이다](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md) — `real`·`user`·`sys` 의 정의와 CPU 시간에서 기다린 시간을 빼는 판정
- [top·htop 참조 시트](./top·htop.md) — 실행이 끝난 뒤 합계가 아니라 지금 도는 프로세스의 CPU 사용률을 볼 때
- [lsof 참조 시트](./lsof.md) — 시간이 CPU 밖에서 흘렀을 때 무엇을 열고 기다렸는지 찾는 법
- [watch 참조 시트](./watch.md) — 같은 측정을 간격을 두고 반복해 볼 때
- [ps 참조 시트](../process/ps.md) — 돌고 있는 프로세스의 `%CPU` 와 누적 CPU 시간 열
- [date 참조 시트](../time/date.md) — 시각을 에포크 초로 바꿔 두 시점의 차이를 계산하는 법
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- 검증 환경: Ubuntu 26.04.1 LTS(OrbStack VM, aarch64), GNU bash 5.3.9, time 1.9-0.4, rust-coreutils(uutils) 0.10.0 — 2026-11-16 실측
- [GNU time 매뉴얼](https://www.gnu.org/software/time/manual/time.html) — "Running the time Command"
- [time(1)](https://manpages.debian.org/bookworm/time/time.1.en.html) — Debian bookworm, 2026-11-16 조회
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html) — "Pipelines"·"Bash Variables"
- [getrusage(2)](https://man7.org/linux/man-pages/man2/getrusage.2.html) — `ru_maxrss`

[^bash-pipeline]: Bash Reference Manual, Pipelines — "If the reserved word time precedes the pipeline, Bash prints timing statistics for the pipeline once it finishes. The statistics currently consist of elapsed (wall-clock) time and user and system time consumed by the command's execution." 이어서 "Providing time as a reserved word permits the timing of shell builtins, shell functions, and pipelines. An external time command cannot time these easily." <https://www.gnu.org/software/bash/manual/bash.html#Pipelines>
[^bsd-time]: FreeBSD `time(1)` — "time [-al] [-h | -p] [-o file] utility [argument ...]", "-l The contents of the rusage structure are printed as well." macOS 26.6 에서 `/usr/bin/time -v true` 는 `illegal option -- v` 로 실패하고 usage 줄이 같은 꼴이었습니다(이 시트의 실측). <https://man.freebsd.org/cgi/man.cgi?query=time&sektion=1>
[^timeformat]: Bash Reference Manual, Bash Variables 의 TIMEFORMAT — "%[p][l]R The elapsed time in seconds. %[p][l]U The number of CPU seconds spent in user mode. %[p][l]S The number of CPU seconds spent in system mode. %P The CPU percentage, computed as (%U + %S) / %R.", "If the value is null, Bash does not display any timing information." `-p` 는 `help time` 의 "-p print the timing summary in the portable Posix format". <https://www.gnu.org/software/bash/manual/bash.html#index-TIMEFORMAT>
[^gnu-format]: `man time`(GNU time 1.9) FORMATTING THE OUTPUT — "M Maximum resident set size of the process during its lifetime, in Kilobytes.", "w Number of times that the program was context-switched voluntarily, for instance while waiting for an I/O operation to complete.", "c Number of times the process was context-switched involuntarily (because the time slice expired).", "x Exit status of the command." 옵션 위치는 DESCRIPTION 의 "Options to time must appear on the command line before COMMAND. Anything on the command line after COMMAND is passed as arguments to COMMAND." <https://manpages.debian.org/bookworm/time/time.1.en.html>
[^time-exit]: `man time`(GNU time 1.9) DIAGNOSTICS — "If the program exited normally, the return value of time is the return value of the program it executed and measured. Otherwise, the return value is 128 plus the number of the signal which caused the program to stop or terminate." 키워드는 `help time` 의 Exit Status — "The return status is the return status of PIPELINE." EXIT STATUS 절은 없고 125·127 은 이 시트의 실측입니다. <https://manpages.debian.org/bookworm/time/time.1.en.html>
[^rss-max]: getrusage(2) 의 ru_maxrss — "This is the maximum resident set size used (in KiB). For RUSAGE_CHILDREN, this is the resident set size of the largest child, not the maximum resident set size of the process tree." `man time` ACCURACY 는 "Most information shown by time is derived from the wait3(2) system call." <https://man7.org/linux/man-pages/man2/getrusage.2.html>
