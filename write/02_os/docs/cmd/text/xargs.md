---
title: xargs 참조 시트
tags: [linux, cheatsheet, xargs, cli, reference]
status: draft
source:
  - xargs(1)
related:
  - ../README.md
updated: 2026-11-11
---

# xargs 참조 시트

---

> `xargs` 로 표준 입력 항목을 명령 인자로 바꾸는 법을 코드와 주석으로 모은 조회용 시트입니다.

## 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 파일이 모두 생깁니다.

macOS 의 `xargs` 는 BSD 판이어서 `-d` 옵션이 없고 입력이 비어 있으면 명령을 실행하지 않는 것이 기본이라 GNU 판과 동작이 다릅니다. OrbStack 의 Linux VM 이나 `docker run -it --rm debian:12` 안에서 실행합니다.

```bash
mkdir -p ~/cmd-lab/xargs && cd ~/cmd-lab/xargs
mkdir -p conf spaced
echo 'timeout=30' > conf/a.conf
echo 'timeout=30' > conf/c.txt
echo 'timeout=60' > conf/b.conf
touch 'spaced/my file.txt' spaced/b.txt
printf 'alpha\nbeta\ngamma\ndelta\nepsilon\n' > list.txt
printf 'a b c\nd e\nf\n' > lines.txt
```

`conf/` 에는 `timeout=30` 인 `a.conf` 와 `c.txt`, `timeout=60` 인 `b.conf` 가 있습니다. `spaced/` 에는 이름에 공백이 든 빈 파일 `my file.txt` 와 `b.txt` 가 있습니다. `list.txt` 는 한 줄에 하나씩 다섯 줄이고, `lines.txt` 는 한 줄에 항목이 셋, 둘, 하나 든 세 줄입니다.



## 1. 입력을 인자로 바꾸기

> 대상을 표준 입력이 아니라 인자로 받는 명령에 입력 항목을 묶어 넘깁니다.

`rm`, `grep -l`, `ssh` 처럼 처리할 대상을 표준 입력이 아니라 인자로 받는 명령이 많습니다. `xargs` 는 표준 입력 항목을 인자로 바꿔 명령을 실행합니다(기본 명령 `echo`).[^xargs]

```bash
# 기본: 명령을 적지 않으면 echo. 입력 항목을 한 줄로 모아 인자로 넘긴다
printf 'a\nb\nc\nd\ne\n' | xargs echo                  # a b c d e
```

```bash
# -n (--max-args): 한 번에 넘길 인자 수. -t (--verbose): 실행할 명령을 표준 오류에 먼저 보인다
printf 'a\nb\nc\nd\ne\n' | xargs -t -n 2 echo
```

```bash
echo a b
a b
echo c d
c d
echo e
e
```

`-t` 는 실행 전에 명령 줄을 보여 주므로 인자가 어떻게 묶였는지 확인할 때 씁니다.[^xargs-p] `-p` (`--interactive`) 는 명령 줄을 보여 준 뒤 터미널에서 한 줄을 읽습니다. 그 줄이 `y` 나 `Y` 로 시작할 때만 실행하고 `-t` 를 함께 켭니다. 대화형이라 이 시트에는 출력을 적지 않습니다. `rm` 처럼 되돌리기 어려운 명령 앞에서 쓰기 좋습니다.

### 묶음 크기 정하기 (-n, -L, -a)

`-n` 은 인자 개수로, `-L` 은 입력 줄 수로 묶음을 끊습니다.[^xargs-n]

```bash
# -n 2: 인자를 둘씩 묶어 echo 를 세 번 실행한다. 마지막 묶음은 모자라도 실행한다
printf 'a\nb\nc\nd\ne\n' | xargs -n 2 echo
```

```bash
a b
c d
e
```

```bash
# -n 1: 인자 하나마다 명령을 한 번씩 실행한다
printf 'a\nb\nc\nd\ne\n' | xargs -n 1 echo
```

```bash
a
b
c
d
e
```

`lines.txt` 로 `-L` 과 `-n` 의 차이를 봅니다. `-L 1` 은 줄 하나가 명령 한 번이라 한 줄 안의 항목은 갈리지 않습니다.

```bash
# -L (--max-lines) 1: 입력 한 줄을 명령 한 번에 넘긴다
xargs -L 1 echo < lines.txt
```

```bash
a b c
d e
f
```

```bash
# -n 1: 줄과 상관없이 항목마다 한 번씩 실행한다
xargs -n 1 echo < lines.txt
```

```bash
a
b
c
d
e
f
```

```bash
# -a (--arg-file): 표준 입력 대신 파일에서 항목을 읽는다
xargs -a list.txt -n 2 echo
```

```bash
alpha beta
gamma delta
epsilon
```

### 인자 자리 정하기 (-I)

기본은 읽은 항목을 명령 맨 끝에 붙입니다. 인자를 명령 중간에 넣거나 한 항목을 여러 번 쓰려면 `-I` 로 바꿀 자리를 정합니다. `-I` 는 항목을 가르는 기준을 공백이 아니라 줄바꿈으로 바꾸고 줄마다 명령을 한 번씩 실행합니다.[^xargs-i]

```bash
# -I {} (--replace): 명령 안의 {} 를 입력 한 줄로 바꾼다. 공백이 든 줄도 한 항목이다
printf 'a b\nc d\n' | xargs -I{} echo '[{}]'
```

```bash
[a b]
[c d]
```

```bash
# -I @: 바꿀 문자열은 아무 문자열이나 된다. 명령에 {} 가 따로 쓰일 때 고른다
printf 'a\nb\n' | xargs -I @ echo cp @ @.bak
```

```bash
cp a a.bak
cp b b.bak
```

한 항목으로 명령 여러 개를 돌릴 때는 `sh -c` 로 감쌉니다. `sh -c '명령' _ 항목` 에서 `_` 가 `$0` 자리를 채우고 항목이 `$1` 이 됩니다.

```bash
# sh -c 로 감싸 항목을 $1 로 받는다. 따옴표 안의 $1 은 xargs 가 아니라 sh 가 푼다
printf 'a\nb\n' | xargs -n 1 sh -c 'echo "got $1"' _
```

```bash
got a
got b
```

### 빈 입력과 종료 상태 (-r)

입력이 비어도 GNU `xargs` 는 명령을 한 번 실행합니다. `-r` 은 입력에 공백이 아닌 글자가 없으면 실행하지 않게 합니다.[^xargs-r]

```bash
# 빈 입력인데도 echo 가 입력 항목 없이 한 번 실행된다
printf '' | xargs echo hello                     # hello

# -r (--no-run-if-empty): 입력이 비면 실행하지 않는다
printf '' | xargs -r echo hello                  # 출력 없음
```

`find ... | xargs rm` 처럼 찾은 것이 없을 때 인자 없는 `rm` 이 돌면 곤란한 파이프라인에서 `-r` 을 붙입니다. `xargs` 의 종료 상태는 실행한 명령이 모두 0 이면 0 이고, 한 번이라도 0 이 아닌 상태(255 제외)로 끝나면 123 입니다.

```bash
# false 는 항상 1 로 끝나므로 xargs 는 123 으로 끝난다
printf 'a\nb\n' | xargs -n 1 false; echo $?      # 123
```



## 2. 공백이 든 이름과 병렬 실행

> 기본 구분은 공백과 줄바꿈이라 공백이 든 이름은 널 문자로 넘깁니다. `-P` 는 여러 개를 함께 돌립니다.

```bash
printf 'my file.txt\nb.txt\n' | xargs -n 1 echo | tr '\n' ' '      # my file.txt b.txt
printf 'my file.txt\0b.txt\0' | xargs -0 -n 1 echo    # 널 문자(\0)로만 항목 구분
# my file.txt
# b.txt
find conf -name '*.conf' -print0 | xargs -0 grep -l 'timeout=30'    # conf/a.conf
printf 'a\nb\n' | xargs -I{} echo 'file: {} -> {}.bak'    # {} 자리에 항목 넣기(-I)
# file: a -> a.bak
# file: b -> b.bak
```

`xargs` 는 기본으로 공백에서도 항목을 끊습니다. 첫 줄의 `my file.txt b.txt` 는 `my`, `file.txt`, `b.txt` 세 줄로 갈린 출력을 한 줄로 이은 것입니다. 그래서 공백 파일명은 `find -print0` 과 `xargs -0` 조합으로 널 문자로 전달합니다. `-P N` 은 프로세스를 N개까지 병렬로 실행합니다. `sleep 1` 을 네 번 실행하는 데 `xargs -n 1` 은 4.014초, `xargs -n 1 -P 4` 는 1.009초가 걸렸습니다. `find` 조건식은 [find 참조 시트](../../../book/learning-modern-linux/00-02.find%20%EC%B0%B8%EC%A1%B0%20%EC%8B%9C%ED%8A%B8.md)에 있습니다.

### -0 과 -d 로 구분자 정하기

`spaced/` 의 `my file.txt` 로 차이를 봅니다. `find` 의 기본 출력은 줄바꿈으로 끝나는 이름이라 `xargs` 가 공백에서 다시 끊습니다. 아래 출력은 순서가 달라지지 않도록 `sort` 를 붙였습니다.

```bash
# find 의 기본 출력을 그대로 넘기면 my file.txt 가 my 와 file.txt 로 쪼개진다
find spaced -type f | xargs -n 1 echo | sort
```

```bash
file.txt
spaced/b.txt
spaced/my
```

```bash
# find -print0 | xargs -0: 널 문자로 끝나는 이름을 받아 공백이 든 이름이 한 항목으로 남는다
find spaced -type f -print0 | xargs -0 -n 1 echo | sort
```

```bash
spaced/b.txt
spaced/my file.txt
```

`-0` 은 널 문자 하나만 항목의 끝으로 보고 따옴표와 역슬래시도 글자 그대로 둡니다.[^xargs-d] `find` 처럼 널 문자로 끝내는 입력을 만들 수 없을 때는 `-d` 로 구분자를 줄바꿈 하나로 정합니다.

```bash
# -d (--delimiter) '\n': 줄바꿈만 항목의 끝으로 본다. 공백이 든 줄이 한 항목으로 남는다
printf 'my file.txt\nb.txt\n' | xargs -d '\n' -n 1 echo
```

```bash
my file.txt
b.txt
```

```bash
# -d 는 문자 하나라면 무엇이든 된다. 쉼표로 이은 항목을 나눈다
printf 'a,b,c' | xargs -d, -n 1 echo | tr '\n' ' '    # a b c
```

### 병렬로 돌리기 (-P)

`-P` 는 한 번에 돌릴 프로세스 수를 정하며 기본은 1이고 0 이면 가능한 만큼 돌립니다.[^xargs-pp] `-n` 이나 `-L` 로 묶음을 나눠야 여러 프로세스가 생기고, 같은 표준 출력에 쓰는 명령은 순서가 실행마다 달라질 수 있습니다. 아래는 순서가 같도록 `sort` 를 붙였습니다.

```bash
# -P 4: 항목마다 한 프로세스씩 최대 4개를 동시에 돌린다
printf '1\n2\n3\n4\n' | xargs -n 1 -P 4 echo | sort
```

```bash
1
2
3
4
```

앞의 `sleep` 측정처럼 기다리는 시간이 대부분인 명령 네 개를 `-n 1 -P 4` 로 돌리면 걸리는 시간이 4분의 1 가까이로 줄어듭니다.



## 관련 문서

- [find 참조 시트](../../../book/learning-modern-linux/00-02.find%20%EC%B0%B8%EC%A1%B0%20%EC%8B%9C%ED%8A%B8.md) — `find -print0` 과 이어 쓰는 조건식



## 참고 자료

- [xargs(1)](https://man7.org/linux/man-pages/man1/xargs.1.html) — 2026-11-10 조회

[^xargs]: `xargs(1)` — 기본 명령이 `echo` 이고 `-0`, `-n`, `-I`, `-P`, `-t` 의 뜻이 적혀 있습니다. <https://man7.org/linux/man-pages/man1/xargs.1.html>
[^xargs-p]: `xargs(1)` — `-t` 는 "Print the command line on the standard error output before executing it.", `-p` 는 "Prompt the user about whether to run each command line and read a line from the terminal. Only run the command line if the response starts with `y' or `Y'. Implies -t.". <https://man7.org/linux/man-pages/man1/xargs.1.html>
[^xargs-n]: `xargs(1)` — `-n` 은 "Use at most max-args arguments per command line.", `-L` 은 "Use at most max-lines nonblank input lines per command line.", `-a` 는 "Read items from file instead of standard input.". <https://man7.org/linux/man-pages/man1/xargs.1.html>
[^xargs-i]: `xargs(1)` — `-I` 는 "Replace occurrences of replace-str in the initial-arguments with names read from standard input. Also, unquoted blanks do not terminate input items; instead the separator is the newline character. Implies -x and "-L 1".". <https://man7.org/linux/man-pages/man1/xargs.1.html>
[^xargs-r]: `xargs(1)` — `-r` 은 "If the standard input does not contain any nonblanks, do not run the command. Normally, the command is run once even if there is no input.", 종료 상태는 "123 if any invocation of the command exited with status other than 0 or 255". <https://man7.org/linux/man-pages/man1/xargs.1.html>
[^xargs-d]: `xargs(1)` — `-0` 은 "Input items are terminated by a null character instead of by whitespace, and the quotes and backslash are not special (every character is taken literally).", `-d` 는 "Input items are terminated by the specified character.". <https://man7.org/linux/man-pages/man1/xargs.1.html>
[^xargs-pp]: `xargs(1)` — `-P` 는 "Run up to max-procs processes at a time; the default is 1. If max-procs is 0, xargs will run as many processes as possible at a time.", 같은 표준 출력에 쓰면 "the output will be produced in an indeterminate order". <https://man7.org/linux/man-pages/man1/xargs.1.html>
