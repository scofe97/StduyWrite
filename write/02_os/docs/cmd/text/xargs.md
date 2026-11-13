---
title: xargs 참조 시트
tags: [linux, cheatsheet, xargs, cli, reference]
status: draft
source:
  - xargs(1)
related:
  - ../README.md
updated: 2026-11-13
---

# xargs 참조 시트

---

> `xargs` 로 표준 입력 항목을 명령 인자로 바꾸는 법을 코드와 주석으로 모은 조회용 시트입니다.

## 개요

> `xargs` 는 표준 입력 항목을 명령의 인자로 바꿔 실행합니다.

명령을 적지 않으면 `echo` 를 실행하고, 인자를 받는 명령에 입력을 묶어 넘기는 데 씁니다.[^xargs] findutils 패키지의 외부 바이너리이며 이 시트는 GNU 판(findutils 4.9.0, Debian 12 컨테이너)으로 실측했습니다. macOS 의 `xargs` 는 BSD 판이어서 `-d` 옵션이 없고 입력이 비어 있으면 명령을 실행하지 않는 것이 기본이라 GNU 판과 동작이 다릅니다.



## 핵심 문법

> 명령을 적고 옵션으로 묶음 크기, 인자 자리, 항목 구분자, 병렬 수를 정합니다.

```bash
# 호출 형태. 입력은 표준 입력이나 -a 파일로 준다
xargs [OPTION]... COMMAND [INITIAL-ARGS]...

# 입력 항목을 명령의 인자로 붙여 실행한다 (입력을 인자로 바꾸기)
xargs 명령
xargs -t 명령

# 한 번에 넘길 인자 수나 줄 수를 정하고 입력을 파일에서 읽는다 (묶음 크기 정하기 (-n, -L, -a))
xargs -n 개수 명령
xargs -L 줄수 명령
xargs -a 파일 명령

# 항목이 들어갈 자리를 정한다 (인자 자리 정하기 (-I))
xargs -I 문자열 명령 문자열

# 입력이 비면 실행하지 않는다 (빈 입력일 때 실행 막기 (-r))
xargs -r 명령

# 항목을 가르는 기준을 바꾼다 (-0 과 -d 로 구분자 정하기)
xargs -0 명령
xargs -d 문자 명령

# 프로세스 여러 개로 나눠 돌린다 (병렬로 돌리기 (-P))
xargs -n 개수 -P 개수 명령

# find 가 만든 이름을 받는다 (find 와 이어 쓰기 (-print0))
find 경로 -print0 | xargs -0 명령
```



## 종료 코드

> `xargs` 는 성공하면 0, 명령 호출이 실패하면 123, 명령을 실행하지 못하면 124~127, 그 밖의 오류는 1 을 돌려줍니다.

매뉴얼은 일곱 코드를 적습니다.[^xargs-exit]

```bash
# 0    성공
# 1    그 밖의 오류. 모르는 옵션이 그렇다
# 123  호출 하나라도 1~125 로 끝났다
# 124  명령이 255 로 끝났다
# 125  명령이 시그널로 죽었다
# 126  명령을 실행할 수 없다
# 127  명령을 찾을 수 없다

# 성공하면 0 이다
echo a | xargs echo; echo $?    # a / 0

# false 는 늘 1 로 끝나므로 xargs 는 123 으로 끝난다
#   -n N   한 번에 넘길 인자를 N 개까지로 한다 (--max-args)
printf 'a\nb\n' | xargs -n 1 false; echo $?      # 123

# 명령이 255 로 끝나면 xargs 는 중단하고 124 로 끝난다
echo a | xargs sh -c 'exit 255'; echo $?    # xargs: sh: exited with status 255; aborting / 124

# 명령이 시그널로 죽으면 125 다
echo a | xargs sh -c 'kill -9 $$'; echo $?    # xargs: sh: terminated by signal 9 / 125

# 디렉터리처럼 실행할 수 없는 대상은 126 이다
echo a | xargs /tmp; echo $?    # xargs: /tmp: Permission denied / 126

# 없는 명령은 127 이다
echo a | xargs nosuchcmd; echo $?    # xargs: nosuchcmd: No such file or directory / 127

# 모르는 옵션은 1 이다
xargs --bad; echo $?    # xargs: unrecognized option '--bad' / Try 'xargs --help' for more information. / 1
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션만 씁니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 파일이 모두 생깁니다.

OrbStack 의 Linux VM 이나 `docker run -it --rm debian:12` 안에서 실행합니다.

```bash
mkdir -p ~/cmd-lab/xargs && cd ~/cmd-lab/xargs
mkdir -p conf spaced

# conf/: timeout=30 인 a.conf·c.txt 와 timeout=60 인 b.conf
# (「find 와 이어 쓰기 (-print0)」)
echo 'timeout=30' > conf/a.conf
echo 'timeout=30' > conf/c.txt
echo 'timeout=60' > conf/b.conf

# spaced/: 이름에 공백이 든 빈 파일 my file.txt 와 b.txt
# (「find 와 이어 쓰기 (-print0)」, 「공백이 든 이름의 쪼개짐」)
touch 'spaced/my file.txt' spaced/b.txt

# list.txt: 한 줄에 하나씩 다섯 줄 (「묶음 크기 정하기 (-n, -L, -a)」)
printf 'alpha\nbeta\ngamma\ndelta\nepsilon\n' > list.txt

# lines.txt: 한 줄에 항목이 셋, 둘, 하나 든 세 줄 (「묶음 크기 정하기 (-n, -L, -a)」)
printf 'a b c\nd e\nf\n' > lines.txt
```

### 입력을 인자로 바꾸기

> 입력 항목을 모아 명령 한 번의 인자로 넘기고, 실제로 돈 명령 줄을 눈으로 봅니다.

`rm`, `grep -l`, `ssh` 처럼 처리할 대상을 표준 입력이 아니라 인자로 받는 명령이 많아서 `xargs` 가 필요합니다.

```bash
# 기본: 명령을 적지 않으면 echo. 입력 항목을 한 줄로 모아 인자로 넘긴다
printf 'a\nb\nc\nd\ne\n' | xargs echo                  # a b c d e
```

```bash
# 인자를 둘씩 묶어 echo 를 세 번 실행한다. echo a b 같은 명령 줄이 결과 앞에 찍힌다
#   -t   실행할 명령을 표준 오류에 먼저 보인다 (--verbose)
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

`-p` (`--interactive`) 는 명령 줄을 보여 준 뒤 터미널에서 한 줄을 읽어 `y` 나 `Y` 로 시작할 때만 실행하며 `-t` 를 함께 켭니다.[^xargs-p] 대화형이라 출력은 적지 않으며 `rm` 처럼 되돌리기 어려운 명령 앞에서 쓰기 좋습니다.

### 묶음 크기 정하기 (-n, -L, -a)

> 명령 한 번이 받을 양을 인자 수나 줄 수에 맞춰 끊습니다.

`-n` 과 `-L` 은 둘 다 한 번에 넘길 양의 상한이라 입력이 모자라면 마지막 묶음이 작아집니다.[^xargs-n]

```bash
# 인자를 둘씩 묶어 echo 를 세 번 실행한다. 마지막 묶음은 모자라도 실행한다
printf 'a\nb\nc\nd\ne\n' | xargs -n 2 echo
```

```bash
a b
c d
e
```

```bash
# 인자 하나마다 명령을 한 번씩 실행한다
printf 'a\nb\nc\nd\ne\n' | xargs -n 1 echo
```

```bash
a
b
c
d
e
```

`lines.txt` 로 `-L` 과 `-n` 의 차이를 봅니다.

```bash
# 줄 하나가 명령 한 번이라 한 줄 안의 항목은 갈리지 않는다. 세 줄이 세 번 실행된다
#   -L N   입력 줄 N 개를 명령 한 번에 넘긴다 (--max-lines)
xargs -L 1 echo < lines.txt
```

```bash
a b c
d e
f
```

```bash
# 줄과 상관없이 항목 여섯 개가 한 번씩 실행된다
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
# 표준 입력 대신 파일에서 항목을 읽어 둘씩 묶는다. 다섯 항목이 세 번에 나뉜다
#   -a FILE   표준 입력 대신 FILE 에서 항목을 읽는다 (--arg-file)
xargs -a list.txt -n 2 echo
```

```bash
alpha beta
gamma delta
epsilon
```

### 인자 자리 정하기 (-I)

> 읽은 항목을 명령 끝이 아니라 정한 자리에 넣고, 한 항목을 여러 번 쓸 수 있습니다.

기본은 읽은 항목을 명령 맨 끝에 붙이고, 매뉴얼은 `-I` 가 `-x` 와 `-L 1` 을 함께 뜻한다고 적습니다.[^xargs-i]

```bash
# 공백이 든 줄도 한 항목이라 두 줄이 두 번 실행된다
#   -I R   명령 안의 R 을 입력 한 줄로 바꾼다 (--replace)
#          항목을 공백이 아니라 줄바꿈으로 가르고 줄마다 한 번 실행한다
printf 'a b\nc d\n' | xargs -I{} echo '[{}]'
```

```bash
[a b]
[c d]
```

```bash
# {} 자리 두 곳에 같은 항목이 들어간다
# {} 자리에 항목 넣기(-I)
printf 'a\nb\n' | xargs -I{} echo 'file: {} -> {}.bak'
# file: a -> a.bak
# file: b -> b.bak
```

```bash
# 바꿀 문자열은 아무 문자열이나 된다. 명령에 {} 가 따로 쓰일 때 고른다
printf 'a\nb\n' | xargs -I @ echo cp @ @.bak
```

```bash
cp a a.bak
cp b b.bak
```

```bash
# 한 항목으로 명령 여러 개를 돌릴 때는 sh -c 로 감싼다. _ 가 $0 자리를 채우고 항목이 $1 이 된다
# 따옴표 안의 $1 은 xargs 가 아니라 sh 가 푼다. 항목마다 한 번씩 got 줄이 나온다
printf 'a\nb\n' | xargs -n 1 sh -c 'echo "got $1"' _
```

```bash
got a
got b
```

### 빈 입력일 때 실행 막기 (-r)

> 입력이 비면 명령을 실행하지 않게 합니다.

`find ... | xargs rm` 처럼 찾은 것이 없을 때 인자 없는 `rm` 이 돌면 곤란한 파이프라인에서 `-r` 을 붙입니다.[^xargs-r]

```bash
# 입력이 비면 실행하지 않아 출력이 없다. -r 이 없으면 한 번 실행된다 (「빈 입력에서의 한 번 실행」)
#   -r   입력에 공백이 아닌 글자가 없으면 명령을 실행하지 않는다 (--no-run-if-empty)
printf '' | xargs -r echo hello                  # 출력 없음
```

### -0 과 -d 로 구분자 정하기

> 기본 구분은 공백과 줄바꿈이라 공백이 든 이름은 널 문자로 넘깁니다.

`find -print0` 처럼 널 문자로 끝내는 입력을 만들 수 없을 때는 `-d` 로 구분자를 줄바꿈 하나로 정합니다.[^xargs-d]

```bash
# 공백이 든 my file.txt 가 한 항목으로 남는다
# 널 문자(\0)로만 항목 구분
#   -0   항목을 공백이 아니라 널 문자로 가른다 (--null)
#        따옴표와 역슬래시도 글자 그대로 둔다
printf 'my file.txt\0b.txt\0' | xargs -0 -n 1 echo
# my file.txt
# b.txt
```

```bash
# 줄바꿈만 항목의 끝으로 본다. 공백이 든 줄이 한 항목으로 남는다
#   -d C   항목의 끝을 문자 C 로 정한다 (--delimiter)
printf 'my file.txt\nb.txt\n' | xargs -d '\n' -n 1 echo
```

```bash
my file.txt
b.txt
```

```bash
# 쉼표로 이은 항목이 셋으로 갈린다. -d 는 문자 하나라면 무엇이든 된다
# tr 로 항목마다 한 줄인 출력을 한 줄에 잇는다
printf 'a,b,c' | xargs -d, -n 1 echo | tr '\n' ' '    # a b c
```

### 병렬로 돌리기 (-P)

> 기다리는 시간이 긴 명령을 동시에 돌려 전체 시간을 줄입니다.

`-n` 이나 `-L` 로 묶음을 나눠야 여러 프로세스가 생기고, 같은 표준 출력에 쓰는 명령은 순서가 실행마다 달라질 수 있습니다.[^xargs-pp]

```bash
# 항목마다 한 프로세스씩 최대 4개를 동시에 돌린다. 순서가 같도록 sort 를 붙였다
#   -P N   한 번에 돌릴 프로세스를 N 개까지로 한다 (--max-procs)
#          기본은 1 이고 0 이면 가능한 만큼 돌린다
printf '1\n2\n3\n4\n' | xargs -n 1 -P 4 echo | sort
```

```bash
1
2
3
4
```

`sleep 1` 을 네 번 실행하는 데 `xargs -n 1` 은 4.014초, `xargs -n 1 -P 4` 는 1.009초가 걸렸습니다. 기다리는 시간이 대부분인 명령은 걸리는 시간이 4분의 1 가까이로 줄어듭니다.

### find 와 이어 쓰기 (-print0)

> `find -print0` 이 널 문자로 끝낸 이름을 `xargs -0` 이 받습니다.

`find` 조건식은 [find 참조 시트](../../../book/learning-modern-linux/00-02.find%20%EC%B0%B8%EC%A1%B0%20%EC%8B%9C%ED%8A%B8.md)에 있습니다.

```bash
# 공백이 든 spaced/my file.txt 가 한 항목으로 남는다
# 순서가 달라지지 않도록 sort 를 붙였다
#   find -type f   일반 파일만 고른다
#   find -print0   이름을 줄바꿈이 아니라 널 문자로 끝낸다
find spaced -type f -print0 | xargs -0 -n 1 echo | sort
```

```bash
spaced/b.txt
spaced/my file.txt
```

```bash
# .conf 파일 가운데 timeout=30 이 든 것만 남는다. b.conf 는 값이 60 이라 빠진다
#   find -name GLOB   이름이 GLOB 에 맞는 파일만 고른다
#   grep -l           맞은 줄이 있는 파일 이름만 찍는다
find conf -name '*.conf' -print0 | xargs -0 grep -l 'timeout=30'    # conf/a.conf
```



## 주의사항과 동작 원리

> 기본 구분에서는 이름 안의 공백이 항목을 끊고, 입력이 비어도 명령이 한 번 실행됩니다.

### 공백이 든 이름의 쪼개짐

> `xargs` 는 기본으로 공백에서도 항목을 끊어 공백이 든 이름이 둘로 갈립니다.

해법은 「-0 과 -d 로 구분자 정하기」 와 「find 와 이어 쓰기 (-print0)」 에 있습니다.

```bash
# my file.txt 가 my 와 file.txt 로 갈려 echo 가 세 번 돈다
# 세 줄 my / file.txt / b.txt 를 tr 로 한 줄에 이어 보인다
printf 'my file.txt\nb.txt\n' | xargs -n 1 echo | tr '\n' ' '      # my file.txt b.txt
```

```bash
# spaced/my 와 file.txt 가 따로 나온다. 순서가 달라지지 않도록 sort 를 붙였다
# find 의 기본 출력은 줄바꿈으로 끝나는 이름이라 xargs 가 공백에서 다시 끊는다
find spaced -type f | xargs -n 1 echo | sort
```

```bash
file.txt
spaced/b.txt
spaced/my
```

### 빈 입력에서의 한 번 실행

> GNU `xargs` 는 입력이 비어도 명령을 한 번 실행하며 `-r` 로 막습니다.

```bash
# 빈 입력인데도 echo 가 입력 항목 없이 한 번 실행된다
printf '' | xargs echo hello                     # hello
```



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [find 참조 시트](../../../book/learning-modern-linux/00-02.find%20%EC%B0%B8%EC%A1%B0%20%EC%8B%9C%ED%8A%B8.md) — `find -print0` 과 이어 쓰는 조건식
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- findutils 4.9.0 의 `xargs --help`·`man xargs` 원문 — Debian 12 컨테이너에서 2026-11-13 출력
- [xargs(1)](https://man7.org/linux/man-pages/man1/xargs.1.html) — 2026-11-10 조회

[^xargs]: `xargs(1)` — 기본 명령이 `echo` 이고 `-0`, `-n`, `-I`, `-P`, `-t` 의 뜻이 적혀 있습니다. <https://man7.org/linux/man-pages/man1/xargs.1.html>
[^xargs-p]: `xargs(1)` — `-t` 는 "Print the command line on the standard error output before executing it.", `-p` 는 "Prompt the user about whether to run each command line and read a line from the terminal. Only run the command line if the response starts with `y' or `Y'. Implies -t.". <https://man7.org/linux/man-pages/man1/xargs.1.html>
[^xargs-n]: `xargs(1)` — `-n` 은 "Use at most max-args arguments per command line.", `-L` 은 "Use at most max-lines nonblank input lines per command line.", `-a` 는 "Read items from file instead of standard input.". <https://man7.org/linux/man-pages/man1/xargs.1.html>
[^xargs-i]: `xargs(1)` — `-I` 는 "Replace occurrences of replace-str in the initial-arguments with names read from standard input. Also, unquoted blanks do not terminate input items; instead the separator is the newline character. Implies -x and "-L 1".". <https://man7.org/linux/man-pages/man1/xargs.1.html>
[^xargs-r]: `xargs(1)` — `-r` 은 "If the standard input does not contain any nonblanks, do not run the command. Normally, the command is run once even if there is no input.", 종료 상태는 "123 if any invocation of the command exited with status other than 0 or 255". <https://man7.org/linux/man-pages/man1/xargs.1.html>
[^xargs-d]: `xargs(1)` — `-0` 은 "Input items are terminated by a null character instead of by whitespace, and the quotes and backslash are not special (every character is taken literally).", `-d` 는 "Input items are terminated by the specified character.". <https://man7.org/linux/man-pages/man1/xargs.1.html>
[^xargs-pp]: `xargs(1)` — `-P` 는 "Run up to max-procs processes at a time; the default is 1. If max-procs is 0, xargs will run as many processes as possible at a time.", 같은 표준 출력에 쓰면 "the output will be produced in an indeterminate order". <https://man7.org/linux/man-pages/man1/xargs.1.html>
[^xargs-exit]: `xargs(1)` 의 EXIT STATUS (findutils 4.9.0, Debian 12 의 `man xargs`) — "0 if it succeeds", "123 if any invocation of the command exited with status 1-125", "124 if the command exited with status 255", "125 if the command is killed by a signal", "126 if the command cannot be run", "127 if the command is not found", "1 if some other error occurred.". <https://manpages.debian.org/bookworm/findutils/xargs.1.en.html>
