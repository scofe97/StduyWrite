---
title: eval 참조 시트
tags: [linux, cheatsheet, eval, bash, shell, builtin, expansion, cli, reference]
status: draft
source:
  - GNU bash 5.3.9 의 `help eval` 원문 (OrbStack Ubuntu 26.04.1 VM)
  - GNU Bash Reference Manual — Bourne Shell Builtins 의 eval 항목
related:
  - ../README.md
  - ../ssh/ssh-keygen·ssh-copy-id·ssh-agent.md
  - ../../../book/learning-modern-linux/03-01.%EC%85%B8%EC%9D%98%20%EC%8B%A4%EC%B2%B4%EB%8A%94%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%EA%B3%BC%20%EB%B3%80%EC%88%98%EC%99%80%20%EC%A2%85%EB%A3%8C%20%EC%83%81%ED%83%9C%EB%8B%A4.md
  - ../../../book/learning-modern-linux/03-03.bash%20%EB%8A%94%20%EC%A1%B0%EC%9A%A9%ED%9E%88%20%EC%8B%A4%ED%8C%A8%ED%95%98%EB%AF%80%EB%A1%9C%20%EC%8B%9C%EB%81%84%EB%9F%BD%EA%B2%8C%20%EB%A7%8C%EB%93%A4%EC%96%B4%EC%95%BC%20%ED%95%9C%EB%8B%A4.md
updated: 2026-11-21
---

# eval 참조 시트

---

> 문자열을 셸이 한 번 더 읽어 명령으로 실행하게 하는 `eval` 의 쓰임과 함정을 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `eval` 은 인자들을 하나의 문자열로 이은 뒤, 그 문자열을 셸 입력으로 다시 읽어 실행합니다.

`eval` 은 외부 바이너리가 아니라 셸 내장 명령입니다(`type eval` → `eval is a shell builtin`). 셸은 한 줄을 실행하기 전에 따옴표를 풀고 `$` 를 확장하는데, 변수 값으로 들어온 문자열은 이 단계를 다시 거치지 않습니다. `eval` 은 그 문자열을 처음부터 다시 읽게 해 확장과 `;`·`|` 해석을 한 번 더 일으킵니다.[^help]

이 시트는 OrbStack 의 Ubuntu 26.04.1 VM 에서 GNU bash 5.3.9 로 실측했습니다. 홈 경로는 `/home/<user>` 로 가렸습니다.



## 핵심 문법

> 인자를 이어 붙인 문자열 하나가 새 명령 줄이 됩니다.

```bash
# 호출 형태 (help eval 의 usage)
eval: eval [arg ...]

# 변수에 담은 명령을 한 번 더 읽어 실행 (문자열에 담은 명령 실행)
eval "$cmd"

# 다른 명령이 출력한 셸 코드를 지금 셸에 적용 (출력된 셸 코드 적용)
eval "$(명령)"
```



## 종료 코드

> 다시 읽은 명령의 종료 코드를 그대로 내고, 인자가 비어 있으면 0, 문법 오류면 2 입니다.[^help]

```bash
# 0  실행한 명령이 성공했거나 인자가 비어 있을 때
# 2  문자열에 문법 오류가 있을 때
# -  그 밖에는 실행한 명령의 종료 코드

eval true; echo "exit=$?"     # exit=0

eval false; echo "exit=$?"    # exit=1

eval; echo "exit=$?"          # exit=0

# 끝나지 않은 if 문
eval 'if'; echo "exit=$?"
```

```bash
# 결과
bash: eval: line 2: syntax error: unexpected end of file from `if' command on line 1
exit=2
```



## 유스케이스

### 문자열에 담은 명령 실행

> 그냥 변수를 실행하면 안쪽 `$HOME` 이 글자로 남고, `eval` 을 거치면 확장됩니다.

```bash
# 명령을 작은따옴표로 담아 $HOME 을 확장하지 않은 채 둔다
cmd='echo $HOME'

# 변수를 그냥 실행 — 단어 분리만 일어나고 $HOME 은 다시 읽지 않는다
$cmd    # $HOME

# eval 로 실행 — 문자열을 다시 읽어 $HOME 을 확장한다
eval "$cmd"    # /home/<user>
```

### 출력된 셸 코드 적용

> `ssh-agent -s` 처럼 환경 변수 설정문을 출력만 하는 명령은 `eval` 로 받아야 지금 셸에 변수가 생깁니다.

```bash
# ssh-agent 가 출력하는 것 — 실행하지 않고 보기만 함
ssh-agent -s
```

```bash
# 결과 (PID·소켓 이름은 <N> 으로 가림)
SSH_AUTH_SOCK=/home/<user>/.ssh/agent/s.Y3BOlYzcSG.agent.6abTZC0Y<N>; export SSH_AUTH_SOCK;
SSH_AGENT_PID=<N>; export SSH_AGENT_PID;
echo Agent pid <N>;
```

```bash
# 출력된 세 문장을 지금 셸에서 실행 — 변수 두 개가 생긴다
eval "$(ssh-agent -s)"    # Agent pid 22841

echo "SOCK=${SSH_AUTH_SOCK:+set}"    # SOCK=set

# 끄는 쪽도 unset 문을 출력하므로 eval 로 적용한다
eval "$(ssh-agent -k)"    # Agent pid 22841 killed

echo "after=${SSH_AUTH_SOCK:-unset}"    # after=unset
```

`ssh-agent` 자체의 옵션은 [ssh-keygen·ssh-copy-id·ssh-agent 참조 시트](../ssh/ssh-keygen·ssh-copy-id·ssh-agent.md)에 있습니다.

### 조건에 따라 조립한 명령 실행

> 옵션을 조건에 따라 문자열에 이어 붙인 뒤 한 번에 실행합니다. 배포 스크립트가 `helmfile apply …` 를 이렇게 조립하는 경우가 많습니다.

```bash
# 조건이 맞으면 옵션을 붙여 명령 문자열을 만든다
LONG=yes
cmd="ls"
if [ -n "$LONG" ]; then cmd="$cmd -l"; fi
cmd="$cmd /etc/hostname"

# 조립한 문자열 확인
echo "$cmd"    # ls -l /etc/hostname

# 실행 — 권한과 경로 칸만 출력
eval "$cmd" | awk '{print $1, $NF}'    # -rw-r--r-- /etc/hostname
```

값에 공백·따옴표가 들어갈 수 있으면 「값 속 기호가 명령이 됨」 의 배열 방식으로 조립합니다.



## 주의사항과 동작 원리

### 값 속 기호가 명령이 됨

> 변수 값 안의 `;`·`$( )`·`|` 도 다시 읽히므로, 바깥에서 온 값을 `eval` 에 넣으면 그 값이 명령으로 실행됩니다.

```bash
# 값에 ; 와 둘째 명령이 들어 있다
x='a; echo INJECTED'

# eval 이 ; 를 명령 구분자로 읽어 둘째 명령까지 실행한다
eval "echo $x"
```

```bash
# 결과
a
INJECTED
```

```bash
# 피하는 방법 1 — printf %q 로 값을 셸이 다시 읽어도 글자로 남는 꼴로 바꾼다
eval "echo $(printf %q "$x")"    # a; echo INJECTED

# 피하는 방법 2 — eval 대신 배열에 명령과 인자를 담고 "${배열[@]}" 로 실행한다
args=(echo "$x")
"${args[@]}"    # a; echo INJECTED
```

배열은 원소 하나가 인자 하나로 그대로 넘어가므로 다시 읽는 단계가 없습니다. 명령을 조립하는 목적이면 배열이 먼저입니다.

### 따옴표 없는 인자의 공백이 줄어듦

> `eval` 은 인자를 공백 하나로 이은 뒤 다시 읽으므로, 바깥 따옴표만 둔 인자의 연속 공백이 하나로 줄고 `$` 가 두 번 확장됩니다.

```bash
# 바깥 셸이 따옴표를 먼저 풀어 eval 은 echo a   b 를 받고, 다시 읽으며 공백을 나눈다
eval echo "a   b"    # a b

# 문자열 전체를 작은따옴표로 넘기면 안쪽 따옴표가 다시 읽힐 때 살아 있다
eval 'echo "a   b"'    # a   b

# 값이 $HOME 이라는 글자여도 eval 이 한 번 더 확장한다
v='$HOME'
eval echo "$v"    # /home/<user>

# $ 를 \ 로 막아 넘기면 eval 이 $v 를 한 번만 확장한다
eval echo "\$v"    # $HOME
```

바깥 셸이 한 번, `eval` 이 한 번 읽으므로 확장과 단어 분리가 두 번 일어납니다. `eval` 에는 작은따옴표로 감싼 문자열 하나를 넘기는 것이 가장 예측하기 쉽습니다.[^manual]



## 관련 문서

> 셸이 실행 전에 하는 확장과 단어 분리는 책 노트에, `eval` 을 실제로 쓰는 명령은 다른 시트에 있습니다.

- [셸의 실체는 스트림과 변수와 종료 상태다](../../../book/learning-modern-linux/03-01.%EC%85%B8%EC%9D%98%20%EC%8B%A4%EC%B2%B4%EB%8A%94%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%EA%B3%BC%20%EB%B3%80%EC%88%98%EC%99%80%20%EC%A2%85%EB%A3%8C%20%EC%83%81%ED%83%9C%EB%8B%A4.md) — 「실행 전에 셸이 하는 `$` 확장」 절. `eval` 은 이 단계를 한 번 더 돌린다
- [bash 는 조용히 실패하므로 시끄럽게 만들어야 한다](../../../book/learning-modern-linux/03-03.bash%20%EB%8A%94%20%EC%A1%B0%EC%9A%A9%ED%9E%88%20%EC%8B%A4%ED%8C%A8%ED%95%98%EB%AF%80%EB%A1%9C%20%EC%8B%9C%EB%81%84%EB%9F%BD%EA%B2%8C%20%EB%A7%8C%EB%93%A4%EC%96%B4%EC%95%BC%20%ED%95%9C%EB%8B%A4.md) — 「변수 보호와 단어 분리」 절
- [ssh-keygen·ssh-copy-id·ssh-agent 참조 시트](../ssh/ssh-keygen·ssh-copy-id·ssh-agent.md) — `eval "$(ssh-agent -s)"` 로 에이전트 띄우기
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 실측 환경과 bash 매뉴얼입니다.

- 검증 환경: OrbStack Ubuntu 26.04.1 LTS VM, GNU bash 5.3.9(1)-release (aarch64)
- [GNU Bash Reference Manual — Bourne Shell Builtins](https://www.gnu.org/software/bash/manual/bash.html#Bourne-Shell-Builtins)

[^help]: `help eval` (bash 5.3.9) — "Combine ARGs into a single string, use the result as input to the shell, and execute the resulting commands. … Returns exit status of command or success if command is null."
[^manual]: GNU Bash Reference Manual, eval — "The arguments are concatenated together into a single command, separated by spaces. Bash then reads and executes this command and returns its exit status as the exit status of eval. If there are no arguments or only empty arguments, the return status is zero."
