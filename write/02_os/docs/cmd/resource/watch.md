---
title: watch 참조 시트
tags: [linux, cheatsheet, watch, monitoring, cli, reference]
status: draft
source:
  - procps-ng 4.0.2 watch(1) (Debian 12 `man watch`·`watch --help` 원문, manpages.debian.org bookworm)
  - tmux 3.3a tmux(1) (Debian 12 `man tmux` 원문, 화면을 글자로 받는 도구)
  - GNU coreutils 9.1 timeout(1) (Debian 12 `timeout --help` 원문)
related:
  - ../README.md
updated: 2026-11-11
---

# watch 참조 시트

---

> 명령을 일정 간격으로 다시 실행해 결과를 한 화면에 덮어 그려 주는 `watch` 를 간격, 바뀐 곳 강조, 머리줄·줄바꿈·색, 끝내는 조건, 따옴표 처리로 나눠, 따라 치면 그대로 나오는 예제로 모았습니다.

## 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 프로세스와 파일과 도우미 함수가 모두 준비됩니다.

macOS 에는 `watch` 가 기본으로 들어 있지 않습니다. 이 시트는 procps-ng 4.0.2 의 `watch` 를 씁니다(`watch --version` 으로 확인). OrbStack 의 Linux VM 이나 `docker run -it --rm --hostname lab debian:12` 안에서 root 로 실행합니다. 출력의 `lab` 은 컨테이너를 `--hostname lab` 으로 띄운 결과이고 직접 칠 때는 자기 호스트 이름이 나옵니다.

```bash
apt-get update -qq >/dev/null 2>&1; apt-get install -y -qq procps tmux >/dev/null 2>&1
mkdir -p ~/cmd-lab/watch && cd ~/cmd-lab/watch
export TERM=${TERM:-xterm}
cp /bin/sleep worker
./worker 600 &
./worker 601 &
mkdir spool
echo 'a b' > 'my file.txt'
# shot <초> <명령...>: 80x8 tmux 창에서 명령을 돌리고, 그 초 뒤의 화면을 글자로 찍는다
shot() {
  local s=$1; shift
  tmux -L cmdlab kill-server 2>/dev/null
  tmux -L cmdlab new-session -d -x 80 -y 8 -- "$@"
  sleep "$s"
  tmux -L cmdlab capture-pane -p | awk 'NF{n=NR} {l[NR]=$0} END{for(i=1;i<=n;i++) print l[i]}'
  tmux -L cmdlab kill-server 2>/dev/null
}
# shote: shot 과 같되 반전·색 같은 속성 코드를 보이게 한다 (ESC 는 ^[ 로 찍힘)
shote() {
  local s=$1; shift
  tmux -L cmdlab kill-server 2>/dev/null
  tmux -L cmdlab new-session -d -x 80 -y 8 -- "$@"
  sleep "$s"
  tmux -L cmdlab capture-pane -pe | cat -v | awk 'NF{n=NR} {l[NR]=$0} END{for(i=1;i<=n;i++) print l[i]}'
  tmux -L cmdlab kill-server 2>/dev/null
}
# runw <명령...>: 터미널 없이 돌려 종료 코드와 걸린 시간만 찍는다. 5초 안에 안 끝나면 124
runw() {
  local s=$SECONDS
  timeout --foreground 5 "$@" > /dev/null
  echo "rc=$? 경과=$((SECONDS-s))초"
}
sleep 0.5
```

`worker` 두 개는 `sleep` 을 복사해 이름만 바꾼 것이라 `ps aux | grep worker` 로 골라 볼 수 있습니다. `spool` 은 빈 디렉터리이고 `my file.txt` 는 이름에 공백이 든 파일입니다.

`watch` 는 화면 전체를 다시 그리므로 출력을 파일로 받으면 제어 코드가 섞여 읽을 수 없습니다(1절). 그래서 이 시트의 화면은 `shot` 이 받은 것입니다. `shot` 은 80×8 크기의 tmux 창에서 명령을 돌리고 지정한 초 뒤의 화면을 `tmux capture-pane -p` 로 글자만 받아 옵니다.[^tmux] `shot` 과 `shote` 는 `tmux -L cmdlab` 로 따로 만든 tmux 서버만 씁니다. 이미 쓰는 tmux 세션과 섞이지 않습니다. 직접 칠 때는 `shot 1` 만 빼고 `watch` 부터 그대로 치면 같은 화면이 뜹니다. 끝낼 때는 Ctrl-C 를 누릅니다.

`shote` 는 `capture-pane -e` 로 반전·색 같은 속성 코드까지 받아 `cat -v` 로 보입니다. `runw` 는 `watch` 의 화면은 버리고 종료 코드와 걸린 시간만 찍습니다. `timeout --foreground` 는 `watch` 가 터미널 입력을 읽을 수 있는 상태로 시간 제한을 걸어 줍니다. 이 옵션 없이 `timeout` 으로 감싸면 이 환경에서는 `watch` 가 화면을 그리지 못하고 끝났습니다.[^timeout]

시각·PID·메모리 값은 실행마다 다르므로 이 시트의 값과 같지 않아도 됩니다. `runw` 의 경과 시간은 초 단위로 끊어 재서 1초쯤 어긋날 수 있습니다.



## 1. 같은 명령을 계속 다시 보기

> `watch` 는 명령을 반복 실행하며 화면을 덮어씁니다. 머리줄에 간격과 명령과 호스트와 시각이 나옵니다.

`watch` 는 명령을 반복해서 실행하고 그 출력과 오류를 보여 줍니다. 기본 간격은 2초이고 중단할 때까지 계속 돕니다.[^desc]

```bash
# 기본: 2초마다 date 를 다시 실행한다. 첫 줄이 머리줄(간격, 명령, 호스트: 시각)이고 빈 줄 한 줄 뒤에 명령 출력이 온다
shot 1 watch date
```

```bash
Every 2.0s: date                                   lab: Wed Nov 11 13:22:13 2026

Wed Nov 11 13:22:13 UTC 2026
```

머리줄 왼쪽의 `Every 2.0s: date` 는 간격과 실행하는 명령이고 오른쪽은 호스트 이름과 현재 시각입니다. 시각은 갱신마다 바뀌므로 눈으로 갱신을 확인할 수 있습니다.

`watch` 는 화면을 지우고 다시 그립니다. 그래서 출력을 파일이나 파이프로 받으면 글자 사이에 `^[` 로 시작하는 커서 이동·화면 지우기 코드가 섞입니다. 아래는 `hi` 를 찍는 명령을 2초 돌린 출력을 `cat -v` 로 보인 것이고 `hi` 는 코드들 사이에 끼어 있습니다.

아래 출력은 80×24 터미널에서 받았습니다. 코드 안의 `24` 같은 숫자는 터미널 크기에 따라 달라집니다.

```bash
# 파이프로 받으면: 출력 70자씩 접어 앞 4줄만. 화면 제어 코드가 섞여 있다
timeout --foreground 2 watch -n 1 echo hi | cat -v | fold -w 70 | head -4
```

```bash
^[(B^[)0^[[?1049h^[[1;24r^[[m^O^[[4l^[[H^[[JEvery 1.0s: echo hi^[[1;52
Hlab: Wed Nov 11 13:31:10 2026^[[3;1Hhi^[[24;80H^[[1;75H1^[[24;80H^[[2
4;1H^[[?1049l^M^[[?1l^[>
```



## 2. 갱신 간격 정하기

> 기본 2초 간격은 `-n` 으로 바꾸고 `-p` 로 시작 시각을 간격에 맞춥니다.

`-n` 은 초 단위이고 소수를 받습니다. 0.1초보다 짧은 값은 0.1초로 바뀌며 소수점은 `.` 와 `,` 모두 됩니다. 환경 변수 `WATCH_INTERVAL` 로 기본 간격을 정해 둘 수도 있습니다.[^n]

```bash
# -n (--interval): 갱신 간격(초). 0.5 면 머리줄이 Every 0.5s 로 바뀐다
shot 1 watch -n 0.5 date +%T.%N
```

```bash
Every 0.5s: date +%T.%N                            lab: Wed Nov 11 13:22:14 2026

13:22:14.593802989
```

```bash
# -n 0.01: 0.1초보다 짧은 값은 0.1초로 바뀐다
shot 1 watch -n 0.01 echo hi
```

```bash
Every 0.1s: echo hi                                lab: Wed Nov 11 13:22:16 2026

hi
```

```bash
# -n 0,5: 소수점은 쉼표도 된다
shot 1 watch -n 0,5 echo hi
```

```bash
Every 0.5s: echo hi                                lab: Wed Nov 11 13:22:16 2026

hi
```

```bash
# WATCH_INTERVAL: -n 없이 환경 변수로 간격을 정한다
WATCH_INTERVAL=0.5 shot 1 watch echo hi
```

```bash
Every 0.5s: echo hi                                lab: Wed Nov 11 13:22:18 2026

hi
```

기본 동작에서는 명령이 느리면 간격이 그만큼 밀립니다. 아래 명령은 0.3초 걸리는 일을 1초 간격으로 시키고 0.3초 일을 마친 시각의 초와 소수 셋째 자리(`date +%S.%N | cut -c1-6`)를 파일에 모읍니다. `paste -sd' '` 는 그 줄들을 한 줄로 이어 보입니다.

```bash
# (옵션 없음): 명령이 0.3초 걸리면 시작 시각이 갱신마다 1.3초씩 밀린다
rm -f normal
timeout --foreground 5.5 watch -t -n 1 'sleep 0.3; date +%S.%N | cut -c1-6 >> normal' > /dev/null
paste -sd' ' normal    # 18.493 19.806 21.121 22.436
```

`-p` 는 시작 시각을 간격에 맞춥니다. man 은 `ntptime` 으로 시험하면 소수부가 거의 그대로 남는다고 설명합니다.[^p] 아래 출력은 시작 시각이 1초씩 늘어납니다.

```bash
# -p (--precise): 명령이 0.3초 걸려도 시작 시각이 1초 간격으로 잡힌다
rm -f precise
timeout --foreground 5.5 watch -t -p -n 1 'sleep 0.3; date +%S.%N | cut -c1-6 >> precise' > /dev/null
paste -sd' ' precise    # 23.996 25.006 26.001 27.005 28.005 29.007
```

`-p` 는 명령이 간격보다 오래 걸리는 경우까지 보정하지는 못합니다. man 은 이때 따라잡으려고 연속해서 실행할 수 있다고 적습니다.[^pbug]



## 3. 바뀐 곳 강조하기

> `-d` 는 직전 갱신과 달라진 글자를 반전해 보이고, `-d=permanent` 는 한 번 바뀐 글자를 계속 반전해 둡니다.

`-d` 는 갱신과 갱신 사이에 달라진 곳을 강조합니다. `permanent` 를 붙이면 첫 갱신 이후 바뀐 모든 곳을 보입니다.[^d] 아래 예는 `state` 파일의 `x` 를 1.2초 뒤, `y` 를 그 1초 뒤 바꾸고 3.5초 시점의 화면을 찍습니다. 강조는 반전 속성이라 `shote` 로 받으며 `^[[7m` 이 반전을 켜는 코드입니다.

```bash
# -d (--differences): 직전 갱신에서 바뀐 글자만 반전. y 의 값만 반전되고 앞 갱신에서 바뀐 x 는 이미 평범하다
echo 'x=1 y=1' > state
( sleep 1.2; echo 'x=2 y=1' > state; sleep 1; echo 'x=2 y=2' > state ) &
shote 3.5 watch -t -d -n 1 cat state    # x=2 y=^[[7m2
```

```bash
# -d=permanent: 첫 갱신 이후 한 번이라도 바뀐 글자는 계속 반전. x 와 y 가 모두 반전된다
echo 'x=1 y=1' > state
( sleep 1.2; echo 'x=2 y=1' > state; sleep 1; echo 'x=2 y=2' > state ) &
shote 3.5 watch -t -d=permanent -n 1 cat state    # x=^[[7m2^[[0m^[[39m^[[49m y=^[[7m2
```

`x=` 뒤에 붙은 `^[[0m^[[39m^[[49m` 은 반전을 되돌리는 속성 코드입니다.

`=permanent` 는 옵션에 붙여 써야 합니다. `-d permanent` 처럼 띄우면 `permanent` 가 옵션의 값이 아니라 실행할 명령이 됩니다.

```bash
# -d permanent: 띄우면 permanent 라는 명령을 실행하려 한다
shot 1 watch -t -d permanent echo ok    # sh: 1: permanent: not found
```

긴 옵션은 `--differences=permanent` 로 씁니다.



## 4. 머리줄·줄바꿈·색 다루기

> `-t` 는 머리줄을, `-w` 는 줄바꿈을, `-c` 는 색 코드의 해석을 바꿉니다.

`-t` 는 머리줄과 그 아래 빈 줄을 없앱니다.[^t] 출력 줄만 남으므로 다른 곳에 옮겨 쓰기 좋습니다.

```bash
# -t (--no-title): 머리줄과 빈 줄이 없어지고 출력 줄만 남는다
shot 1 watch -t date    # Wed Nov 11 13:22:38 UTC 2026
```

`-w` 는 긴 줄을 다음 줄로 접지 않고 화면 폭에서 자릅니다.[^w] 아래 명령은 1부터 50까지 공백으로 이은 140자짜리 한 줄을 찍습니다.

```bash
# (옵션 없음): 화면 폭을 넘으면 다음 줄로 접어 그린다
shot 1 watch -t "seq -s' ' 1 50"
```

```bash
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50
```

```bash
# -w (--no-wrap): 화면 폭에서 자르고 접지 않는다
shot 1 watch -t -w "seq -s' ' 1 50"    # 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
```

`-c` 는 명령 출력 안의 ANSI 색·스타일 코드를 해석합니다.[^c] 옵션 없이 쓰면 색 코드가 해석되지 않고 `^[31m` 같은 글자로 화면에 남았습니다. 아래 `red` 는 빨간 글자 코드(`31m`)로 감싼 글자입니다.

```bash
# (옵션 없음): 색 코드가 글자로 찍힌다
shot 1 watch -t 'printf "\033[31mred\033[0m ok\n"'    # ^[31mred^[0m ok
```

```bash
# -c (--color): 색 코드가 사라지고 글자만 남는다
shot 1 watch -t -c 'printf "\033[31mred\033[0m ok\n"'    # red ok
```

```bash
# -c + shote: 속성 코드까지 받으면 빨간색(31m)이 적용된 것을 확인할 수 있다
shote 1 watch -t -c 'printf "\033[31mred\033[0m ok\n"'    # ^[[31mred^[[39m ok
```



## 5. 조건이 되면 끝내기

> `-g` 는 출력이 바뀔 때, `-q` 는 바뀌지 않을 때, `-e` 는 명령이 실패할 때 `watch` 를 끝냅니다.

### 출력이 바뀌면 끝내기

`-g` 는 명령의 출력이 바뀌면 `watch` 를 끝냅니다.[^g] 첫 실행의 출력이 비교 기준이 되므로 디렉터리에 파일이 생길 때까지 기다리는 데 씁니다. 아래 예는 2.5초 뒤 `spool/ready` 를 만들고 `watch` 가 그때 끝나는지 봅니다. `runw` 의 `rc` 는 종료 코드입니다.

```bash
# -g (--chgexit): 출력이 바뀌면 끝난다. ls 의 목록이 바뀌는 것이 곧 파일이 생긴 것이다
( sleep 2.5; touch spool/ready ) &
runw watch -g -n 1 ls spool    # rc=0 경과=3초
```

```bash
# 만들어진 파일
ls spool    # ready
```

출력이 바뀌지 않으면 끝나지 않습니다. 아래는 날짜만 찍는 명령이라 5초 뒤 `runw` 의 `timeout` 이 끊었고 종료 코드 124 는 `timeout` 이 시간 초과로 끊었다는 값입니다.

```bash
# (바뀌지 않는 출력): -g 로는 끝나지 않아 timeout 이 끊는다
runw watch -g -n 1 date +%F    # rc=124 경과=5초
```

### 출력이 안 바뀌면 끝내기

`-q` 는 출력이 지정한 횟수만큼 연속해서 바뀌지 않으면 끝냅니다.[^q]

```bash
# -q (--equexit) 2: 첫 실행 뒤 출력이 2번 연속 그대로면 끝난다(세 번째 실행, 2초 시점)
runw watch -q 2 -n 1 date +%F    # rc=0 경과=2초
```

### 명령이 실패하면 멈추기

`-e` 는 명령이 0 이 아닌 종료 코드로 끝나면 갱신을 멈추고 아무 키나 누를 때까지 화면을 붙들어 둡니다.[^e] 아래는 없는 파일을 `ls` 해 실패시킨 화면입니다. 맨 아래에 안내 문구가 나옵니다.

```bash
# -e (--errexit): 명령이 실패하면 갱신을 멈추고 안내를 띄운다
shot 2.5 watch -e -n 1 'ls nofile'
```

```bash
Every 1.0s: ls nofile                              lab: Wed Nov 11 13:22:54 2026

ls: cannot access 'nofile': No such file or directory




command exit with a non-zero status, press a key to exit
```

키를 누르면 `watch` 는 종료 코드 8 로 끝납니다.[^exit] 아래 예는 tmux 창에 `x` 키를 보내고 `watch` 뒤에 찍어 둔 `$?` 를 읽습니다.

```bash
# 키 입력 뒤 종료 코드: 2초 뒤 x 를 보내면 watch 가 끝나고 rc 에 8 이 남는다
tmux -L cmdlab kill-server 2>/dev/null
tmux -L cmdlab new-session -d -x 80 -y 8 -- bash -c 'watch -e -n 1 "ls nofile"; echo "rc=$?" > rc'
sleep 2; tmux -L cmdlab send-keys x; sleep 0.5; cat rc    # rc=8
```

### 실패하면 소리 내기

`-b` 는 명령이 0 이 아닌 종료 코드로 끝날 때 터미널 벨을 울립니다.[^b] 아래는 벨 문자(`\a`)가 출력에 몇 번 섞였는지 센 값입니다. `false` 는 3.5초 동안 0·1·2·3초에 네 번 실행됐습니다.

```bash
# -b (--beep): 실패한 실행마다 벨 문자가 하나씩 나온다
timeout --foreground 3.5 watch -b -n 1 false | tr -cd '\a' | wc -c    # 4
```

```bash
# 성공하면: 벨이 울리지 않는다
timeout --foreground 3.5 watch -b -n 1 true | tr -cd '\a' | wc -c    # 0
```



## 6. 파이프와 따옴표 넘기기

> `watch` 는 명령 인자를 `sh -c` 로 넘기므로 파이프와 변수는 따옴표로 묶어야 `watch` 가 돌리는 명령에 들어갑니다.

`watch` 는 인자를 공백으로 이어 `sh -c` 로 실행합니다.[^x] 그래서 인자에 든 공백은 셸이 다시 쪼개고 `$$` 같은 변수는 매번 새 셸이 풀어 줍니다. man 도 따옴표의 효과를 보려면 `watch echo $$` 와 `watch echo '$$'` 를 비교해 보라고 합니다.[^q2] 아래는 두 형태로 3.5초 동안 돌려 매번 찍힌 PID 를 모은 것입니다. `내 셸` 의 값은 이 시트를 돌린 컨테이너에서 1이었고 PID 값은 환경마다 다릅니다.

```bash
# 따옴표 안의 $$: watch 가 돌리는 sh 가 풀어서 실행마다 새 sh 의 PID 가 찍힌다
echo "내 셸: $$"
rm -f pids; shot 3.5 watch -t -n 1 'echo $$ >> pids' > /dev/null; cat pids
```

```bash
내 셸: 1
680
683
685
687
```

```bash
# 큰따옴표 안의 $$: 지금 셸이 먼저 풀어서 매번 같은 숫자(내 셸의 PID)가 간다
rm -f pids; shot 3.5 watch -t -n 1 "echo $$ >> pids" > /dev/null; cat pids
```

```bash
1
1
1
1
```

따옴표가 필요한 가장 흔한 경우가 파이프입니다. 따옴표로 묶으면 파이프까지 한 줄로 `sh -c` 에 넘어가 `ps` 의 결과를 `grep` 으로 거른 화면이 갱신됩니다. 마지막 줄은 `grep` 자신입니다.

```bash
# 따옴표로 묶음: 파이프 전체가 watch 가 돌리는 명령이 된다
shot 1 watch -t 'ps aux | grep worker'
```

```bash
root         236  0.0  0.0   2240  1108 ?        S    13:22   0:00 ./worker 600
root         237  0.0  0.0   2240  1108 ?        S    13:22   0:00 ./worker 601
root         724  0.0  0.0   3092  1324 pts/0    S+   13:23   0:00 grep worker
```

따옴표 없이 쓰면 지금 셸이 `|` 에서 명령을 가릅니다. `watch ps aux` 의 화면 출력이 `grep` 으로 가므로 터미널에는 거른 결과가 아니라 제어 코드 덩어리가 나옵니다.

```bash
# 따옴표 없이: 지금 셸이 | 에서 나눠 watch 의 화면 출력이 grep 으로 간다. cat -v 로 앞 60자만
timeout --foreground 3 watch -t -n 1 ps aux | grep worker | cat -v | cut -c1-60
```

```bash
^[(B^[)0^[[?1049h^[[1;24r^[[m^O^[[4l^[[H^[[JUSER^[[1;14HPID 
```

`-x` 는 `sh -c` 를 거치지 않고 `exec` 로 명령을 직접 실행합니다. 따옴표를 덜 써도 되는 대신 파이프·변수 같은 셸 기능은 쓸 수 없습니다.[^x] 먼저 `-x` 없이 공백이 든 파일 이름을 넘깁니다.

```bash
# (옵션 없음): 공백이 든 이름이 두 파일로 쪼개진다
shot 1 watch -t wc -l my file.txt
```

```bash
wc: my: No such file or directory
wc: file.txt: No such file or directory
0 total
```

```bash
# -x (--exec): 인자가 쪼개지지 않고 그대로 간다
shot 1 watch -t -x wc -l 'my file.txt'    # 1 my file.txt
```

```bash
# -x 와 $$: 셸이 풀지 않으므로 글자 그대로 찍힌다
shot 1 watch -t -x echo '$$'    # $$
```

```bash
# -x 와 파이프: 문자열 전체를 실행 파일 이름으로 보고 실행하지 못한다
shot 1 watch -t -x 'ps aux | grep worker'    # watch: unable to execute 'ps aux | grep worker': No such file or directory
```

`watch` 는 POSIX 방식으로 옵션을 읽어 명령이 시작되는 첫 인자부터는 옵션으로 해석하지 않습니다. 그래서 `watch -n 1 ls -l` 의 `-l` 은 `ls` 의 옵션입니다.[^notes]



## 7. 실무에서 자주 쓰는 형태

> 디스크와 메모리와 디렉터리를 일정 간격으로 보며 변화를 찾는 형태입니다.

디스크 사용량은 `df -h /` 를 1초 간격으로 봅니다. 큰 파일을 복사하는 동안 `Used` 가 늘어나는 것을 지켜보는 식으로 씁니다.

```bash
# 디스크 사용량을 1초마다
shot 1 watch -n 1 'df -h /'
```

```bash
Every 1.0s: df -h /                                lab: Wed Nov 11 13:23:21 2026

Filesystem      Size  Used Avail Use% Mounted on
overlay          93G   35G   59G  37% /
```

메모리는 `-d` 로 바뀐 숫자를 반전해 보입니다. 아래는 갱신 한 번의 화면이고 값이 달라지면 그 자리가 반전됩니다.

```bash
# 메모리 변화를 반전으로
shot 1 watch -d free -m
```

```bash
Every 2.0s: free -m                                lab: Wed Nov 11 13:22:37 2026

               total        used        free      shared  buff/cache   available
Mem:            8004         721        7065          22         439        7282
Swap:           9028           0        9028
```

디렉터리의 파일 개수는 `ls` 를 `wc -l` 로 세어 지켜봅니다. 5절의 `spool` 에 만든 `ready` 한 개가 보입니다. 파일이 생길 때까지 기다리고 싶으면 이 대신 5절의 `watch -g ls` 형태를 씁니다.

```bash
# 디렉터리의 파일 수
shot 1 watch -t -n 1 'ls spool | wc -l'    # 1
```



## 8. while sleep 반복문과의 차이

> 반복 실행만 필요하면 `while sleep 1` 로 되고, 화면을 덮어쓰고 바뀐 곳을 보이고 조건으로 끝내는 일은 `watch` 의 몫입니다.

`while sleep 1; do …; done` 은 출력이 위에서 아래로 쌓이는 반복문입니다. 화면을 지우지 않고 머리줄도 없습니다. 출력이 일반 텍스트라 파일에 남기거나 파이프로 잇기 쉽습니다.

```bash
# 반복문: 3.5초 동안 3번 돌고 출력이 줄줄이 쌓인다. 끝은 timeout 이 끊는다
timeout 3.5 bash -c 'while sleep 1; do date +%T; done'
```

```bash
13:23:24
13:23:25
13:23:26
```

`watch` 는 같은 자리에 다시 그리므로 변화가 눈에 띄고 `-d`·`-g`·`-q`·`-e` 로 강조하거나 끝낼 수 있습니다. 대신 화면 제어 코드를 쓰기 때문에 1절에서 본 것처럼 출력이 파일이나 파이프로 가는 곳에는 맞지 않습니다. 반복문은 명령이 실패해도 계속 돌고 끝내는 조건을 직접 써야 합니다.

`watch -g ls` 와 같은 일을 반복문으로 하면 기다릴 조건을 `ls` 의 출력 변화가 아니라 직접 씁니다. 아래는 2초 뒤 `spool/done` 을 만들고 반복문이 그때 끝나는지 봅니다.

```bash
# until 반복문: 기다리는 조건(파일 존재)을 직접 쓴다
( sleep 2; touch spool/done ) &
s=$SECONDS; until [ -e spool/done ]; do sleep 1; done; echo "경과=$((SECONDS-s))초"    # 경과=2초
```



## 관련 문서

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [ps 참조 시트](../process/ps.md) — `watch 'ps aux | grep …'` 로 프로세스 상태를 반복해 볼 때 고르는 열과 정렬 옵션
- [top·htop 참조 시트](./top·htop.md) — 간격을 `watch` 로 시키지 않고 스스로 화면을 갱신하는 도구



## 참고 자료

- procps-ng 4.0.2 의 `man watch`·`watch --help` 원문 — Debian 12 컨테이너에서 2026-11-11 확인
- [watch(1) — Debian bookworm](https://manpages.debian.org/bookworm/procps/watch.1.en.html)
- [tmux(1) — Debian bookworm](https://manpages.debian.org/bookworm/tmux/tmux.1.en.html)
- [timeout(1) — Debian bookworm](https://manpages.debian.org/bookworm/coreutils/timeout.1.en.html)

[^desc]: `man watch` (procps-ng 4.0.2) DESCRIPTION — "watch runs command repeatedly, displaying its output and errors (the first screenfull)." "By default, command is run every 2 seconds and watch will run until interrupted." https://manpages.debian.org/bookworm/procps/watch.1.en.html
[^tmux]: `man tmux` (tmux 3.3a) capture-pane — "If -p is given, the output goes to stdout", "If -e is given, the output includes escape sequences for text and background attributes." https://manpages.debian.org/bookworm/tmux/tmux.1.en.html
[^timeout]: `timeout --help` (GNU coreutils 9.1) — `--foreground` "when not running timeout directly from a shell prompt, allow COMMAND to read from the TTY and get TTY signals". https://manpages.debian.org/bookworm/coreutils/timeout.1.en.html
[^n]: `man watch` — `-n, --interval seconds` "The command will not allow quicker than 0.1 second interval, in which the smaller values are converted. Both '.' and ',' work for any locales. The WATCH_INTERVAL environment can be used to persistently set a non-default interval (following the same rules and formatting)."
[^p]: `man watch` — `-p, --precise` "Make watch attempt to run command every --interval seconds. Try it with ntptime (if present) and notice how the fractional seconds stays (nearly) the same, as opposed to normal mode where they continuously increase."
[^pbug]: `man watch` BUGS — "--precise mode doesn't yet have advanced temporal distortion technology to compensate for a command that takes more than --interval seconds to execute. watch also can get into a state where it rapid-fires as many executions of command as it can to catch up from a previous executions running longer than --interval".
[^d]: `man watch` — `-d, --differences[=permanent]` "Highlight the differences between successive updates. If the optional permanent argument is specified then watch will show all changes since the first iteration."
[^t]: `man watch` — `-t, --no-title` "Turn off the header showing the interval, command, and current time at the top of the display, as well as the following blank line."
[^w]: `man watch` — `-w, --no-wrap` "Turn off line wrapping. Long lines will be truncated instead of wrapped to the next line."
[^c]: `man watch` — `-c, --color` "Interpret ANSI color and style sequences."
[^g]: `man watch` — `-g, --chgexit` "Exit when the output of command changes."
[^q]: `man watch` — `-q, --equexit <cycles>` "Exit when output of command does not change for the given number of cycles."
[^e]: `man watch` — `-e, --errexit` "Freeze updates on command error, and exit after a key press." `watch --help` 는 같은 옵션을 "exit if command has a non-zero exit" 로 적는다.
[^exit]: `man watch` EXIT STATUS — "8 Getting child process return value with waitpid(2) failed, or command exited up on error."
[^b]: `man watch` — `-b, --beep` "Beep if command has a non-zero exit."
[^x]: `man watch` — `-x, --exec` "Pass command to exec(2) instead of sh -c which reduces the need to use extra quoting to get the desired effect."
[^q2]: `man watch` EXAMPLES — "To see the effects of quoting, try these out" `watch echo $$`, `watch echo '$$'`, `watch echo "'"'$$'"'"`.
[^notes]: `man watch` NOTES — "POSIX option processing is used (i.e., option processing stops at the first non-option argument). This means that flags after command don't get interpreted by watch itself."
