---
title: head·tail 참조 시트
tags: [linux, cheatsheet, head, tail, log-rotation, cli, reference]
status: draft
source:
  - GNU coreutils head·tail (`--help` 원문, coreutils 9.1)
related:
  - ../README.md
updated: 2026-11-13
---

# head·tail 참조 시트

---

> 긴 파일의 앞과 뒤만 잘라 보는 `head`·`tail` 과, 늘어나는 로그를 따라가는 `tail -f`·`-F` 를 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `head` 는 파일의 앞부분을, `tail` 은 뒷부분을 잘라 찍고, `tail -f` 는 늘어나는 파일의 끝을 따라갑니다.

둘 다 coreutils 의 외부 바이너리이며 이 시트는 GNU 판(coreutils 9.1, Debian 12 컨테이너)으로 실측했습니다. macOS 기본 `head`·`tail` 은 BSD 판이라 `head -n -3` 같은 음수 인자를 받지 않습니다.



## 핵심 문법

> `-n`·`-c` 로 자를 양을 정하고, `tail` 은 `-f`·`-F` 로 파일 끝에 붙는 줄을 따라갑니다.

```bash
# 호출 형태
head [OPTION]... [FILE]...
tail [OPTION]... [FILE]...

# 앞 N줄, 뒤 N줄을 자른다 (줄 수로 자르기)
head -n 줄수 파일
tail -n 줄수 파일

# 부호를 붙인다. head 는 뒤 N줄만 빼고, tail 은 N째 줄부터 찍는다 (줄 수로 자르기)
head -n -N 파일
tail -n +N 파일

# 줄이 아니라 바이트로 자른다 (바이트로 자르기)
head -c 바이트수 파일
tail -c 바이트수 파일

# 파일 여러 개의 앞부분을 머리줄 없이 찍는다 (여러 파일을 한 번에)
head -q -n 줄수 파일1 파일2

# 앞 N줄의 마지막 한 줄로 N째 줄을 꺼낸다 (가운데 한 줄 꺼내기)
head -n N 파일 | tail -n 1

# 늘어나는 파일의 끝을 따라간다. -F 는 이름을 따라간다 (-f 와 -F 가 따라가는 대상)
tail -f 파일
tail -F 파일

# 이미 있는 줄은 건너뛰고 새로 붙는 줄만 찍는다 (새 줄만 보기)
tail -n 0 -F 파일

# 프로세스가 끝나면 따라가기도 끝낸다 (종료 코드)
tail -f --pid=PID 파일
```



## 종료 코드

> `head`·`tail` 은 성공하면 0, 실패하면 1 을 돌려줍니다.

매뉴얼은 두 명령 절에 성공은 0, 실패는 0 이 아닌 값이라고만 적고 실패 코드를 나누지 않습니다.[^ht-exit] 아래는 Debian 12 컨테이너에서 실패 두 가지를 돌린 결과입니다.

```bash
# 0  성공. 파일을 읽어 찍었을 때. tail -f --pid 가 PID 의 종료로 끝났을 때도 0 이다
# 1  실패. 없는 파일, 모르는 옵션을 줬을 때
# tail -f 는 스스로 끝나지 않고 --pid 나 kill 로 끝낸다. 그래서 끝나는 꼴만 잰다

# 없는 파일
head /nonexistent; echo $?    # head: cannot open '/nonexistent' for reading: No such file or directory / 1
tail /nonexistent; echo $?    # tail: cannot open '/nonexistent' for reading: No such file or directory / 1

# 모르는 옵션
head --badopt; echo $?        # head: unrecognized option '--badopt' / Try 'head --help' for more information. / 1
tail --badopt; echo $?        # tail: unrecognized option '--badopt' / Try 'tail --help' for more information. / 1
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다. 아래 블록은 `--pid` 로 끝나는 `tail -f` 의 종료 코드를 잽니다.

```bash
# 2초 뒤 끝나는 프로세스를 띄우고 그 PID 를 넘긴다. 배치 작업이 쓰는 로그를 작업이 끝날 때까지만 따라갈 때 쓴다
#   -f          파일이 자라는 대로 덧붙은 데이터를 찍는다. 인자가 없으면 descriptor 다 (--follow[={name|descriptor}])
#   --pid=PID   -f 와 함께 쓴다. 프로세스 PID 가 끝나면 tail 도 끝난다
echo a > r.log
sleep 2 &
tail -f --pid=$! r.log; echo "exit $?"
```

```bash
a
exit 0
```



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션만 씁니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 파일이 모두 생깁니다.

OrbStack 의 Linux VM 이나 `docker run -it --rm debian:12` 안에서 실행합니다.

```bash
mkdir -p ~/cmd-lab/head-tail && cd ~/cmd-lab/head-tail
seq 1 100 > nums.txt
cat > app.log << 'EOF'
2026-11-10 09:01:15 INFO  order-api started
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:14:41 WARN  retrying orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
2026-11-10 10:06:01 error db connection reset
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
2026-11-10 11:30:00 INFO  heartbeat
EOF
```

`nums.txt` 는 1부터 100까지 한 줄에 하나씩 든 파일이라 몇째 줄이 나왔는지 바로 보입니다. `app.log` 는 일곱 줄짜리 애플리케이션 로그입니다. 로그를 따라가는 예의 `r.log` 는 「-f 와 -F 가 따라가는 대상」 에서 따로 만듭니다.

### 줄 수로 자르기

> 수만 줄짜리 파일을 열기 전에 첫 몇 줄로 형식을 확인하고, 마지막 몇 줄로 최근 기록을 봅니다.

숫자 앞에 붙는 부호가 두 명령에서 뜻이 다릅니다.[^head][^tail]

```bash
# 앞 3줄. -3 은 -n 3 의 줄임
#   -n NUM   앞 NUM줄을 찍는다. NUM 앞에 '-' 를 붙이면 뒤 NUM줄을 뺀 나머지 전부를 찍는다 (--lines)
head -3 nums.txt
```

```bash
1
2
3
```

```bash
# 줄 수를 주지 않으면 10줄
head nums.txt | wc -l    # 10

# head -n -97: 마지막 97줄을 뺀 나머지 전부
head -n -97 nums.txt
```

```bash
1
2
3
```

```bash
# 뒤 3줄
#   -n NUM   뒤 NUM줄을 찍는다. NUM 앞에 '+' 를 붙이면 NUM째 줄부터 끝까지 찍는다 (--lines)
tail -3 nums.txt
```

```bash
98
99
100
```

```bash
# tail -n +98: 98째 줄부터 끝까지. 헤더 한 줄을 건너뛸 때는 tail -n +2 를 쓴다
tail -n +98 nums.txt
```

```bash
98
99
100
```

### 바이트로 자르기

> `-c` 는 줄이 아니라 바이트를 셉니다.

로그 앞머리의 타임스탬프 19바이트만 자르거나, 줄바꿈이 없는 바이너리 파일의 앞부분을 볼 때 씁니다.

```bash
# 앞 19바이트. 줄바꿈이 없어 echo 로 줄을 바꿔 준다
#   -c NUM   앞 NUM바이트를 찍는다. NUM 앞에 '-' 를 붙이면 뒤 NUM바이트를 뺀 나머지 전부를 찍는다 (--bytes)
head -c 19 app.log; echo    # 2026-11-10 09:01:15

# 뒤 10바이트. 마지막 줄바꿈 1바이트를 포함한다
#   -c NUM   뒤 NUM바이트를 찍는다. NUM 앞에 '+' 를 붙이면 NUM째 바이트부터 끝까지 찍는다 (--bytes)
tail -c 10 app.log          # heartbeat
```

### 여러 파일을 한 번에

> 파일을 둘 이상 주면 파일마다 `==> 이름 <==` 머리줄이 붙습니다.

```bash
head -n 1 app.log nums.txt
```

```bash
==> app.log <==
2026-11-10 09:01:15 INFO  order-api started

==> nums.txt <==
1
```

```bash
# 머리줄을 뺀다. -v 를 주면 반대로 파일이 하나여도 머리줄을 붙인다
#   -q   파일 이름 머리줄을 찍지 않는다 (--quiet, --silent)
head -q -n 1 app.log nums.txt
```

```bash
2026-11-10 09:01:15 INFO  order-api started
1
```

### 가운데 한 줄 꺼내기

> 앞 N줄을 자른 뒤 그 마지막 한 줄을 받으면 N째 줄이 됩니다.

`sed -n 3p` 도 같은 줄을 냅니다([sed 참조 시트](./sed.md)).

```bash
head -n 3 app.log | tail -n 1    # 2026-11-10 09:14:41 WARN  retrying orderId=1001
sed -n 3p app.log                # 2026-11-10 09:14:41 WARN  retrying orderId=1001
```

```bash
# head 는 필요한 줄을 다 찍으면 바로 끝난다. 그래서 백만 줄을 내는 명령 뒤에 붙여도 기다리지 않는다
# 앞 명령은 head 가 끝난 뒤 더 쓰려 할 때 SIGPIPE 를 받고 멈춘다
seq 1 1000000 | head -2
```

```bash
1
2
```

### -f 와 -F 가 따라가는 대상

> 서비스가 지금 쓰고 있는 로그는 끝을 한 번 보고 끝낼 수 없습니다. `tail -f` 는 끝을 찍은 뒤 멈추지 않고 새로 붙는 줄을 계속 찍습니다.

로그 로테이션이 파일 이름을 `r.log.1` 로 바꾸고 새 `r.log` 를 만들면 `-f` 는 이름이 바뀐 옛 파일 끝에 머뭅니다.[^tail]

```bash
# 로테이션 한 번을 손으로 흉내 낸다. tail 을 뒤에서 돌려 둔 채 이름을 바꾸고 새 파일에 두 줄을 쓴다
# 대화형 셸에서는 tail 을 뒤로 돌릴 때 [1] 9 같은 잡 번호 줄이, kill 뒤에 [1]   Terminated  tail -F r.log 같은 알림 줄이 더 나온다
# 아래 출력은 그 줄을 뺀 것이다. docker 컨테이너의 overlay 파일시스템에서는 출력이 늦으니 cd /dev/shm 처럼 tmpfs 로 옮기거나 VM 에서 돌린다
# 늦는 까닭은 「overlay 에서 -F 가 늦게 알아챔」 참고
#   -F   --follow=name --retry 와 같다. 이름을 따라가고, 파일이 사라졌다 다시 생기면 새 파일을 연다
#        -f 의 기본인 descriptor 는 처음 연 파일 서술자를 따라간다
echo one > r.log
tail -F r.log &
sleep 1; mv r.log r.log.1; echo two > r.log; echo three >> r.log
sleep 2; kill %1
```

```bash
one
tail: 'r.log' has become inaccessible: No such file or directory
tail: 'r.log' has appeared;  following new file
two
three
```

`tail` 이 찍는 알림 줄은 이름 바뀜을 알아챈 방식에 따라 달라지며, 어느 쪽이든 `two`·`three` 가 따라 나오면 새 파일을 연 것입니다. 파일 변화를 곧바로 알려 주는 inotify 로 알아채면 위 두 줄이, 파일을 주기적으로 다시 확인해 알아채면 `tail: 'r.log' has been replaced;  following new file` 한 줄이 나옵니다.

```bash
# 같은 순서를 -f 로 돌린다. one 에서 멈추고 two 는 나오지 않는다. 옛 파일에 줄을 덧붙이면 그 줄은 나온다
# -f 가 이름이 아니라 처음 연 파일을 붙들고 있다는 뜻이다
rm -f r.log r.log.1; echo one > r.log
tail -f r.log &
sleep 1; mv r.log r.log.1; echo two > r.log; echo late >> r.log.1
sleep 2; kill %1
```

```bash
one
late
```

### 새 줄만 보기

> `-n 0` 을 함께 주면 이미 있는 줄은 건너뛰고 지금부터 붙는 줄만 찍습니다.

```bash
# 배포 직후 새 로그만 지켜볼 때 쓴다
rm -f r.log; echo old > r.log
tail -n 0 -F r.log &
sleep 1; echo new >> r.log
sleep 2; kill %1
```

```bash
new
```



## 주의사항과 동작 원리

> overlay 파일시스템에서는 `-F` 가 이름 바뀜을 늦게 알아챕니다.

### overlay 에서 -F 가 늦게 알아챔

> `-F` 가 이름 바뀜을 3~4초 뒤에야 알아채서 `sleep 2` 안에는 `one` 만 나옵니다.

`docker run` 으로 띄운 컨테이너의 기본 파일시스템은 overlay 입니다. 여기서 「-f 와 -F 가 따라가는 대상」 첫 예를 돌리면 `sleep 2` 안에는 `one` 만 나왔습니다. 더 기다리면 `has been replaced` 한 줄과 `two`·`three` 가 나왔습니다(Debian 12 이미지, 2026-11-11). 이때 `tail` 은 파일 크기가 그대로인 채 정해진 횟수를 지나야 이름을 다시 확인하며 기본 횟수는 5입니다.[^tail]



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [grep 참조 시트](./grep.md) — `tail -f` 로 따라가는 줄 가운데 맞는 줄만 고를 때. 출력이 파이프로 가면 `grep --line-buffered` 를 붙여 모아 찍지 않게 합니다
- [sed 참조 시트](./sed.md) — 줄 번호나 패턴으로 가운데 구간을 꺼낼 때
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- GNU coreutils 9.1 의 `head --help`·`tail --help` 원문 — Debian 12 컨테이너에서 2026-11-11 출력
- [GNU coreutils 매뉴얼](https://www.gnu.org/software/coreutils/manual/coreutils.html) — "head invocation"·"tail invocation"

[^head]: `head --help` (GNU coreutils 9.1) — `-n, --lines=[-]NUM` "print the first NUM lines instead of the first 10; with the leading '-', print all but the last NUM lines of each file".
[^tail]: `tail --help` (GNU coreutils 9.1) — `-n, --lines=[+]NUM` "or use -n +NUM to output starting with line NUM", `-F` "same as --follow=name --retry", `--max-unchanged-stats=N` "with --follow=name, reopen a FILE which has not changed size after N (default 5) iterations to see if it has been unlinked or renamed", 그리고 "With --follow (-f), tail defaults to following the file descriptor, which means that even if a tail'ed file is renamed, tail will continue to track its end."
[^ht-exit]: GNU coreutils 9.1 매뉴얼(Debian 12 의 `info coreutils`), "head invocation"·"tail invocation" — "An exit status of zero indicates success, and a nonzero value indicates failure." 코드 1 과 `--pid` 로 끝났을 때의 0 은 이 시트의 실측입니다(Debian 12, coreutils 9.1). <https://www.gnu.org/software/coreutils/manual/html_node/head-invocation.html>, <https://www.gnu.org/software/coreutils/manual/html_node/tail-invocation.html>
