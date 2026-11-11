---
title: head·tail 참조 시트
tags: [linux, cheatsheet, head, tail, log-rotation, cli, reference]
status: draft
source:
  - GNU coreutils head·tail (`--help` 원문, coreutils 9.1)
related:
  - ../README.md
updated: 2026-11-11
---

# head·tail 참조 시트

---

> 긴 파일의 앞과 뒤만 잘라 보는 `head`·`tail` 과, 늘어나는 로그를 따라가는 `tail -f`·`-F` 를 따라 치면 그대로 나오는 예제로 모았습니다.

## 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 파일이 모두 생깁니다.

macOS 기본 `head`·`tail` 은 BSD 판이라 `head -n -3` 같은 음수 인자를 받지 않습니다. OrbStack 의 Linux VM 이나 `docker run -it --rm debian:12` 안에서 실행합니다.

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

`nums.txt` 는 1부터 100까지 한 줄에 하나씩 든 파일이라 몇째 줄이 나왔는지 바로 보입니다. `app.log` 는 일곱 줄짜리 애플리케이션 로그입니다. 2절의 로그 따라가기 예는 그 자리에서 `r.log` 를 따로 만듭니다.



## 1. 앞과 뒤만 잘라 보기

> 수만 줄짜리 파일을 열기 전에 첫 몇 줄로 형식을 확인하고, 마지막 몇 줄로 최근 기록을 봅니다.

### 줄 수로 자르기

`-n` 에 숫자만 주면 앞이나 뒤에서 그만큼을 자릅니다. 숫자 앞에 붙는 부호가 두 명령에서 뜻이 다릅니다.[^head][^tail]

```bash
# 앞 3줄. -3 은 -n 3 의 줄임
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
tail -3 nums.txt
```

```bash
98
99
100
```

```bash
# tail -n +98: 98째 줄부터 끝까지
tail -n +98 nums.txt
```

```bash
98
99
100
```

`head -n -N` 은 "뒤 N줄 빼고", `tail -n +N` 은 "N째 줄부터" 로 읽습니다. 헤더 한 줄을 건너뛸 때 `tail -n +2` 를 씁니다.

### 가운데 한 줄 꺼내기

앞 N줄을 자른 뒤 그 마지막 한 줄을 받으면 N째 줄이 됩니다. `sed -n 3p` 도 같은 줄을 냅니다([sed 참조 시트](./sed.md)).

```bash
head -n 3 app.log | tail -n 1    # 2026-11-10 09:14:41 WARN  retrying orderId=1001
sed -n 3p app.log                # 2026-11-10 09:14:41 WARN  retrying orderId=1001
```

`head` 는 필요한 줄을 다 찍으면 바로 끝납니다. 그래서 백만 줄을 내는 명령 뒤에 붙여도 기다리지 않습니다. 앞 명령은 `head` 가 끝난 뒤 더 쓰려 할 때 SIGPIPE 를 받고 멈춥니다.

```bash
seq 1 1000000 | head -2
```

```bash
1
2
```

### 바이트로 자르기

`-c` 는 줄이 아니라 바이트를 셉니다. 로그 앞머리의 타임스탬프 19바이트만 자르거나, 줄바꿈이 없는 바이너리 파일의 앞부분을 볼 때 씁니다.

```bash
# 앞 19바이트. 줄바꿈이 없어 echo 로 줄을 바꿔 준다
head -c 19 app.log; echo    # 2026-11-10 09:01:15

# 뒤 10바이트. 마지막 줄바꿈 1바이트를 포함한다
tail -c 10 app.log          # heartbeat
```

### 여러 파일을 한 번에

파일을 둘 이상 주면 파일마다 `==> 이름 <==` 머리줄이 붙습니다. `-q` 는 머리줄을 빼고 `-v` 는 파일이 하나여도 붙입니다.

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
head -q -n 1 app.log nums.txt
```

```bash
2026-11-10 09:01:15 INFO  order-api started
1
```



## 2. 늘어나는 로그 따라가기

> 서비스가 지금 쓰고 있는 로그는 끝을 한 번 보고 끝낼 수 없습니다. `tail -f` 는 끝을 찍은 뒤 멈추지 않고 새로 붙는 줄을 계속 찍습니다.

### -f 와 -F 가 따라가는 대상

`-f` 는 처음 연 파일 서술자를 따라갑니다. 로그 로테이션이 파일 이름을 `r.log.1` 로 바꾸고 새 `r.log` 를 만들면, `-f` 는 이름이 바뀐 옛 파일 끝에 머뭅니다. `-F` 는 `--follow=name --retry` 와 같아서 이름을 따라가고 파일이 사라졌다 다시 생기면 새 파일을 엽니다.[^tail]

아래 예는 로테이션 한 번을 손으로 흉내 냅니다. `tail` 을 뒤에서 돌려 둔 채 이름을 바꾸고 새 파일에 두 줄을 씁니다.

```bash
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

대화형 셸에서는 `tail` 을 뒤로 돌릴 때 `[1] 9` 같은 잡 번호 줄이 더 나옵니다. `kill` 뒤에는 `[1]   Terminated  tail -F r.log` 같은 알림 줄도 나옵니다. 위 출력은 그 줄을 뺀 것입니다.

알림 줄은 `tail` 이 이름 바뀜을 어떻게 알아챘는지에 따라 달라집니다. 파일 변화를 곧바로 알려 주는 inotify 로 알아채면 위 두 줄이 나옵니다. 파일을 주기적으로 다시 확인해 알아채면 `tail: 'r.log' has been replaced;  following new file` 한 줄이 나옵니다. 어느 쪽이든 `two`·`three` 가 따라 나오면 새 파일을 연 것입니다.

같은 순서를 `-f` 로 돌리면 `one` 에서 멈춥니다. 옛 파일에 줄을 덧붙이면 그 줄은 나옵니다. `-f` 가 이름이 아니라 처음 연 파일을 붙들고 있다는 뜻입니다.

```bash
rm -f r.log r.log.1; echo one > r.log
tail -f r.log &
sleep 1; mv r.log r.log.1; echo two > r.log; echo late >> r.log.1
sleep 2; kill %1
```

```bash
one
late
```

`docker run` 으로 띄운 컨테이너의 기본 파일시스템은 overlay 입니다. 여기서는 `-F` 가 이름 바뀜을 3~4초 뒤에야 알아채서, 위 예의 `sleep 2` 안에는 `one` 만 나왔습니다. 더 기다리면 `has been replaced` 한 줄과 `two`·`three` 가 나왔습니다(Debian 12 이미지, 2026-11-11). 이때 `tail` 은 파일 크기가 그대로인 채 정해진 횟수를 지나야 이름을 다시 확인하고 기본 횟수는 5입니다.[^tail] 이 예만은 `cd /dev/shm` 처럼 tmpfs 로 옮기거나 VM 에서 돌립니다.

### 새 줄만 보기와 끝낼 시점

`-n 0` 을 함께 주면 이미 있는 줄은 건너뛰고 지금부터 붙는 줄만 찍습니다. 배포 직후 새 로그만 지켜볼 때 씁니다.

```bash
rm -f r.log; echo old > r.log
tail -n 0 -F r.log &
sleep 1; echo new >> r.log
sleep 2; kill %1
```

```bash
new
```

`--pid` 를 주면 그 프로세스가 끝날 때 `tail` 도 끝납니다. 배치 작업이 쓰는 로그를 작업이 끝날 때까지만 따라갈 때 씁니다.

```bash
# 2초 뒤 끝나는 프로세스를 띄우고 그 PID 를 넘긴다
echo a > r.log
sleep 2 &
tail -f --pid=$! r.log; echo "exit $?"
```

```bash
a
exit 0
```



## 관련 문서

- [grep 참조 시트](./grep.md) — `tail -f` 로 따라가는 줄 가운데 맞는 줄만 고를 때. 출력이 파이프로 가면 `grep --line-buffered` 를 붙여 모아 찍지 않게 합니다
- [sed 참조 시트](./sed.md) — 줄 번호나 패턴으로 가운데 구간을 꺼낼 때
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

- GNU coreutils 9.1 의 `head --help`·`tail --help` 원문 — Debian 12 컨테이너에서 2026-11-11 출력
- [GNU coreutils 매뉴얼](https://www.gnu.org/software/coreutils/manual/coreutils.html) — "head invocation"·"tail invocation"

[^head]: `head --help` (GNU coreutils 9.1) — `-n, --lines=[-]NUM` "print the first NUM lines instead of the first 10; with the leading '-', print all but the last NUM lines of each file".
[^tail]: `tail --help` (GNU coreutils 9.1) — `-n, --lines=[+]NUM` "or use -n +NUM to output starting with line NUM", `-F` "same as --follow=name --retry", `--max-unchanged-stats=N` "with --follow=name, reopen a FILE which has not changed size after N (default 5) iterations to see if it has been unlinked or renamed", 그리고 "With --follow (-f), tail defaults to following the file descriptor, which means that even if a tail'ed file is renamed, tail will continue to track its end."
