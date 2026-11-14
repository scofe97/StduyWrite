---
title: systemctl 참조 시트
tags: [linux, cheatsheet, systemctl, systemd, service, unit, cli, reference]
status: draft
source:
  - systemd 259 systemctl(1) (OrbStack Ubuntu 26.04 VM 의 `man systemctl`·`systemctl --help` 원문, freedesktop.org systemctl(1))
  - systemd.unit(5)·systemd.socket(5)·systemd.service(5) (freedesktop.org)
  - Debian 12 `openssh-server` 1:9.2p1-2+deb12u10 패키지 파일 (`apt-get download` 로 받아 푼 내용)
related:
  - ../README.md
  - ./systemctl%20함정과%20동작%20원리.md
  - ./systemctl%20유닛%20설정과%20타이머.md
  - ../../../book/learning-modern-linux/06-01.먼저%20켜지는%20것%20하나가%20나머지%20전부를%20켠다.md
  - ../sysinfo/uname%C2%B7os-release%C2%B7lsb_release.md
updated: 2026-11-13
---

# systemctl 참조 시트

---

> 서비스의 상태를 읽고, 지금 켜고 끄고, 부팅 때 켜지게 하고, 실패한 서비스를 추적하는 `systemctl` 을 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `systemctl` 은 systemd 가 관리하는 유닛의 상태를 읽고, 지금 켜고 끄고, 부팅 때의 동작을 바꾸는 명령입니다.

systemd 패키지의 외부 바이너리(`/usr/bin/systemctl`)이며 PID 1 이 systemd 인 시스템에서만 동작하므로 `docker run` 컨테이너와 macOS 에서는 쓸 수 없습니다. 이 시트의 출력은 OrbStack Ubuntu 26.04 VM(systemd 259)에서 `sudo bash` 로 받았습니다. 이 VM 이 모든 service 에 붙이는 drop-in `zzz-lxc-service.conf` 때문에 `status` 에 `Drop-In:` 줄이 항상 나옵니다.



## 핵심 문법

> 서브커맨드는 조회, 지금 상태 바꾸기, 유닛 파일 바꾸기 셋으로 나뉘고 옵션은 출력과 대상을 정하거나 서브커맨드에 동작을 덧붙입니다.

```bash
# 호출 형태
# systemctl --help 의 첫 줄
systemctl [OPTIONS...] COMMAND ...

# man systemctl 의 SYNOPSIS. COMMAND 는 서브커맨드, UNIT 은 유닛 이름이나 패턴
systemctl [OPTIONS...] COMMAND [UNIT...]

# 유닛 상태를 읽는다 (서비스 상태 읽기)
systemctl status 유닛

# 스크립트에서 상태로 가른다 (스크립트에서 상태로 분기하기)
systemctl is-active 유닛

# 유닛 목록을 뽑는다 (유닛 목록 뽑기)
systemctl list-units
systemctl list-unit-files

# 속성 하나만 뽑는다 (속성 하나만 뽑기)
systemctl show -p 속성 유닛

# 실제로 읽힌 유닛 파일을 본다 (실제로 읽힌 유닛 파일 보기)
systemctl cat 유닛

# 지금 켜고 끈다. 부팅 때 동작은 그대로다 (지금 켜고 끄기)
systemctl start 유닛
systemctl stop 유닛
systemctl restart 유닛

# 부팅 때 켜고 끈다. --now 를 붙이면 지금도 함께 바꾼다 (부팅 때 켜고 끄기)
systemctl enable --now 유닛
systemctl disable --now 유닛

# 수동 시작까지 막고 푼다 (유닛 막기와 풀기)
systemctl mask 유닛
systemctl unmask 유닛

# 실패한 유닛을 모으고 표시를 지운다 (실패한 서비스 추적)
systemctl list-units --failed
systemctl reset-failed 유닛
```

### 유닛 이름과 패턴

```bash
# UNIT 자리에 쓰는 표기
# cmd-lab-demo   유닛 이름. 종류 접미사를 생략하면 .service 로 읽는다
#                systemctl status ssh 는
#                "Unit ssh.service could not be found." 라고 답한다
# 'cmd-lab*'     이름 패턴. 셸과 같은 glob 규칙으로 유닛 이름에 맞춘다. 따옴표로 감싸서 준다 (유닛 목록 뽑기)
```



## 종료 코드

> 성공이면 0, 아니면 0 이 아닌 값입니다. 0~4 는 LSB 의 값을 빌려 쓰지만 대응이 완전하지 않아서 상태 이름을 직접 묻는 쪽이 안전합니다.[^exitstatus]

5 와 잘못된 서브커맨드의 1 은 매뉴얼에 값이 없는 실측입니다.[^exitother] 아래 값은 「실습 준비」 블록을 돌린 직후, 아무것도 시작하지 않은 상태에서 잰 것입니다.

```bash
# 0  LSB "program is running or service is OK"
#    systemd 에서는 "unit is active"
#    is-active 가 active 일 때, 그리고 대부분의 명령이 성공했을 때
#    is-enabled 는 enabled 와 static 에도 0
#    is-failed 는 failed 일 때 0
# 1  LSB "program is dead and /var/run pid file exists"
#    systemd 에서는 "unit not failed (used by is-failed)"
#    is-failed 가 failed 가 아닌 유닛에 낸다
#    is-enabled 의 disabled·masked, masked 유닛의 start, 잘못된 서브커맨드에도 1
# 2  LSB "program is dead and /var/lock lock file exists"
#    systemd 에서는 "unused"
#    쓰이지 않는 값이라 재현할 수 없다
# 3  LSB "program is not running"
#    systemd 에서는 "unit is not active"
#    is-active 가 inactive 나 failed 일 때, status 가 멈춘 유닛에 낸다
#    ExecReload 가 없는 서비스의 reload 거절도 3
# 4  LSB "program or service status is unknown"
#    systemd 에서는 "no such unit"
#    status·is-active·is-enabled·is-failed 가 없는 유닛에 낸다
#    오타와 정지를 가를 때 쓴다
# 5  매뉴얼 표에 없는 값. start·stop·restart 가 없는 유닛에 낸다
# is-active·is-enabled·is-failed 의 상태별 코드는 「스크립트에서 상태로 분기하기」 를 본다

# 출력은 /dev/null 로 버리고 echo $? 로 종료 코드만 읽는다
systemctl status cmd-lab-plain --no-pager > /dev/null 2>&1; echo $?     # 3
systemctl status cmd-lab-nothing --no-pager > /dev/null 2>&1; echo $?   # 4
systemctl is-failed cmd-lab-nothing > /dev/null; echo $?                # 4
systemctl start cmd-lab-nothing > /dev/null 2>&1; echo $?               # 5
systemctl no-such-command > /dev/null 2>&1; echo $?                     # 1
```



## 유스케이스

> 예는 앞 예가 만든 상태를 이어 쓰므로 위에서 아래로 차례로 돌립니다.

### 실습 준비

> 아래 블록을 root 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 유닛 셋이 생깁니다.

PID·시각·`Invocation` 값은 실행마다 다르므로 이 시트의 값과 같지 않아도 됩니다.

```bash
# 실습이 끝나면 「실습 정리」 블록으로 모두 지운다

# 실습 폴더를 만들고 그 안으로 옮긴다
# 유닛 설정과 타이머 시트가 editor.sh 를 이 폴더에 둔다
mkdir -p ~/cmd-lab/systemctl \
  && cd ~/cmd-lab/systemctl

# cmd-lab-demo: sleep infinity 를 띄운다
#   ExecReload 와 [Install] 이 있어 reload 와 enable 을 모두 받는다
#   Alias 는 enable 할 때 cmd-lab-nick.service 라는 별칭 링크를 만든다
#   패키지가 설치한 유닛처럼 /usr/lib/systemd/system 에 둔다
#   「유닛 막기와 풀기」 의 mask 가 그 자리의 유닛에만 먹기 때문이다
cat > /usr/lib/systemd/system/cmd-lab-demo.service << 'EOF'
[Unit]
Description=cmd-lab demo service

[Service]
ExecStart=/bin/sleep infinity
ExecReload=/bin/true

[Install]
WantedBy=multi-user.target
Alias=cmd-lab-nick.service
EOF

# cmd-lab-plain: ExecReload 와 [Install] 이 없는 서비스
#   reload 거절과 is-enabled 의 static 을 보는 데 쓴다
cat > /etc/systemd/system/cmd-lab-plain.service << 'EOF'
[Unit]
Description=cmd-lab service without ExecReload

[Service]
ExecStart=/bin/sleep infinity
EOF

# cmd-lab-fail: 종료 코드 3 으로 곧바로 끝나는 서비스
#   stdout 과 stderr 에 한 줄씩 남겨 failed 상태와 로그를 보는 데 쓴다
cat > /etc/systemd/system/cmd-lab-fail.service << 'EOF'
[Unit]
Description=cmd-lab service that fails on purpose

[Service]
ExecStart=/bin/sh -c 'echo cmd-lab-fail: starting; echo cmd-lab-fail: giving up >&2; exit 3'
EOF

# 새로 둔 유닛 파일 셋을 systemd 가 읽게 한다
systemctl daemon-reload
```

주석에 적은 종료 코드는 명령을 실행한 직후 `$?` 로 읽은 값입니다. 설치 파일을 풀어 보는 [함정 문서](./systemctl%20함정과%20동작%20원리.md)의 「ssh 서비스 이름과 ssh.socket」 둘째 부분만 Debian 12 컨테이너에서 받았습니다.

### 서비스 상태 읽기

> `status` 한 번으로 이 서비스가 지금 떠 있는지, 부팅 때 켜지는지, 마지막 로그가 무엇인지를 함께 봅니다.

`status` 는 사람이 읽는 요약이라 스크립트가 파싱할 값은 「속성 하나만 뽑기」 의 `show` 로 뽑으라고 매뉴얼이 적어 둡니다.[^status]

```bash
# 켜기 전의 서비스를 본다. Active: inactive (dead), 종료 코드 3
# Drop-In: 줄은 OrbStack 이 모든 service 에 붙이는 drop-in 때문에 나온다
# 다른 서버에서는 drop-in 이 하나도 없을 때만 빠진다
#   --no-pager   출력이 길어도 pager 로 넘기지 않는다. 이 시트의 예 대부분이 붙인다
systemctl status cmd-lab-demo --no-pager | head -5
```

```bash
○ cmd-lab-demo.service - cmd-lab demo service
     Loaded: loaded (/usr/lib/systemd/system/cmd-lab-demo.service; disabled; preset: enabled)
    Drop-In: /run/systemd/system/service.d
             └─zzz-lxc-service.conf
     Active: inactive (dead)
```

`Loaded:` 줄은 유닛 파일 경로와 부팅 때 켜지는지(`disabled`)를, `Active:` 줄은 지금 상태를 보입니다. 앞의 `○` 는 inactive, `●` 는 active, `×` 는 failed 를 뜻합니다.[^status]

```bash
# start: 서비스를 지금 시작한다 (「지금 켜고 끄기」 에서 이어 다룬다)
systemctl start cmd-lab-demo
systemctl status cmd-lab-demo --no-pager
```

```bash
● cmd-lab-demo.service - cmd-lab demo service
     Loaded: loaded (/usr/lib/systemd/system/cmd-lab-demo.service; disabled; preset: enabled)
    Drop-In: /run/systemd/system/service.d
             └─zzz-lxc-service.conf
     Active: active (running) since Wed 2026-11-11 23:36:39 KST; 5ms ago
 Invocation: 2aa3747ce5494a84ba43cebfcaf96a8a
   Main PID: 21256 (sleep)
      Tasks: 1 (limit: 9641)
     Memory: 1.5M (peak: 1.7M)
        CPU: 4ms
     CGroup: /system.slice/cmd-lab-demo.service
             └─21256 /bin/sleep infinity

Nov 11 23:36:39 ubuntu systemd[1]: Started cmd-lab-demo.service - cmd-lab demo service.
```

`Main PID` 와 `CGroup` 은 이 서비스가 실제로 쥔 프로세스를 가리킵니다. 맨 아래 빈 줄 뒤의 줄들은 저널에서 가져온 최근 로그입니다.

```bash
# 로그만 빼고 싶으면 저널 로그 줄을 0줄로 준다
#   -n   저널 로그 줄 수 (--lines=). status 는 기본 10줄이고 0 은 로그를 뺀다
systemctl status cmd-lab-demo --no-pager -n 0
```

```bash
● cmd-lab-demo.service - cmd-lab demo service
     Loaded: loaded (/usr/lib/systemd/system/cmd-lab-demo.service; disabled; preset: enabled)
    Drop-In: /run/systemd/system/service.d
             └─zzz-lxc-service.conf
     Active: active (running) since Wed 2026-11-11 23:36:39 KST; 8ms ago
 Invocation: 2aa3747ce5494a84ba43cebfcaf96a8a
   Main PID: 21256 (sleep)
      Tasks: 1 (limit: 9641)
     Memory: 1.4M (peak: 1.7M)
        CPU: 4ms
     CGroup: /system.slice/cmd-lab-demo.service
             └─21256 /bin/sleep infinity
```

```bash
# 없는 유닛이면 한 줄 메시지와 함께 종료 코드 4 로 끝난다
systemctl status cmd-lab-nothing --no-pager    # Unit cmd-lab-nothing.service could not be found. (종료 코드 4)
```

### 스크립트에서 상태로 분기하기

> `is-active`·`is-enabled`·`is-failed` 는 상태 이름을 출력하고 종료 코드로도 답해서 `if` 에 그대로 넣을 수 있습니다.

`is-active` 는 하나라도 active 이면 종료 코드 0, 아니면 0 이 아닌 값을 돌려주고 `--quiet` 를 주지 않으면 상태 이름도 출력합니다.[^isactive] `is-failed` 는 반대로 failed 일 때 0 입니다.[^isactive]

```bash
# 종료 코드 3 은 꺼진 유닛이고 4 는 없는 유닛이라 오타와 정지를 구분할 수 있다
systemctl is-active cmd-lab-demo    # active (종료 코드 0)
systemctl is-active cmd-lab-plain   # inactive (종료 코드 3)
systemctl is-active cmd-lab-nothing # inactive (종료 코드 4)
```

```bash
# 출력 없이 종료 코드만 낸다
#   -q   결과 출력을 끈다 (--quiet). 오류는 그대로 찍힌다
systemctl is-active -q cmd-lab-demo    # 출력 없음 (종료 코드 0)

# 스크립트에서 쓰는 모양
if systemctl is-active --quiet cmd-lab-demo; then echo running; \
  else echo not-running; fi
# running
```

`is-enabled` 는 부팅 때 켜지게 설정된 경우 0, 아니면 0 이 아닌 값을 돌려줍니다. `[Install]` 이 없는 유닛은 `static` 이고 이것도 0 입니다.[^isenabled]

```bash
systemctl is-enabled cmd-lab-demo     # disabled (종료 코드 1)
systemctl is-enabled cmd-lab-plain    # static (종료 코드 0)
systemctl is-enabled cmd-lab-nothing  # not-found (종료 코드 4)
```

```bash
# 정상인 서비스에 is-failed 를 물으면 현재 상태를 출력하고 종료 코드 1
# failed 일 때 0 이 되는 예는 「실패한 서비스 추적」 에 있다
systemctl is-failed cmd-lab-demo    # active (종료 코드 1)
```

### 유닛 목록 뽑기

> 지금 메모리에 올라 있는 유닛은 `list-units`, 디스크에 설치된 유닛 파일은 `list-unit-files` 로 봅니다.

`list-units` 는 메모리에 올라온 유닛만 보여서 꺼져 있고 실패하지도 않은 유닛은 목록에 없습니다.[^listunits]

```bash
# 메모리에 올라온 유닛 중 cmd-lab 으로 시작하는 서비스의 running 만 고른다
# 이름 패턴을 빼면 이름으로 좁히지 않아 조건에 맞는 유닛이 모두 나온다
#   --type=    service·socket 같은 유닛 종류로 거른다 (-t)
#   --state=   LOAD·SUB·ACTIVE 중 아무 상태로 거른다
systemctl list-units \
  --type=service \
  --state=running \
  'cmd-lab*' \
  --no-pager
```

```bash
  UNIT                 LOAD   ACTIVE SUB     DESCRIPTION
  cmd-lab-demo.service loaded active running cmd-lab demo service

Legend: LOAD   → Reflects whether the unit definition was properly loaded.
        ACTIVE → The high-level unit activation state, i.e. generalization of SUB.
        SUB    → The low-level unit activation state, values depend on unit type.

1 loaded units listed.
```

```bash
# 머리글·범례·합계 줄을 뺀다. 사람에게는 도움이지만 awk·wc 로 넘길 때는 방해라서 뺀다
#   --no-legend   man 의 정식 옵션은 열 머리글과 끝의 안내 줄을
#                 켜고 끄는 --legend=BOOL 이고, 이 시트는 --no-legend 로 쓴다
systemctl list-units \
  --type=service \
  --state=running \
  --no-legend \
  'cmd-lab*' \
  --no-pager
```

```bash
  cmd-lab-demo.service loaded active running cmd-lab demo service
```

```bash
# list-unit-files: 설치된 유닛 파일과 그 enable 상태를 보인다
# --state 로도 거를 수 있다 (예: --state=disabled)
# PRESET 열은 배포판의 preset 정책이 이 유닛을 어떻게 켜라고 하는지다
systemctl list-unit-files 'cmd-lab*' --no-pager
```

```bash
UNIT FILE             STATE    PRESET
cmd-lab-demo.service  disabled enabled
cmd-lab-fail.service  static   -
cmd-lab-plain.service static   -

3 unit files listed.
```

### 속성 하나만 뽑기

> 스크립트가 파싱할 값은 `status` 가 아니라 `show -p` 로 뽑습니다.

`-p` 는 콤마로 나눈 속성 이름만 보이게 합니다.[^show]

```bash
# show: 유닛의 속성을 이름=값 줄로 낸다
#   -p   보일 속성 (--property=)
# FragmentPath·UnitFileState 처럼 유닛 파일 위치와 enable 상태도 -p 로 뽑을 수 있다
# -p 없이 쓰면 모든 속성이 수백 줄 나오므로 systemctl show 유닛 | head 로 이름을 훑어 필요한 속성을 찾는다
# ExecReload 같은 구조 속성도 -p 로 한 줄씩 뽑을 수 있다
systemctl show -p ActiveState,SubState cmd-lab-demo
```

```bash
ActiveState=active
SubState=running
```

```bash
# 속성 이름 없이 값만 낸다. 변수에 담을 때 쓴다
#   --value   show -p 와 함께 쓴다
systemctl show -p MainPID --value cmd-lab-demo    # 21256
```

### 실제로 읽힌 유닛 파일 보기

> `cat` 은 유닛의 본 파일과 drop-in 을 한 번에 이어서 보여 줍니다.

`cat` 은 디스크 내용을 보이므로 `daemon-reload` 를 하지 않고 파일을 고쳤다면 systemd 가 아는 내용과 다를 수 있습니다.[^cat]

```bash
# cat: 유닛의 fragment(본 파일)와 drop-in 파일을 각각 파일 이름 주석을 앞에 붙여 출력한다
# 어떤 서비스가 기대와 다르게 동작할 때 이 명령으로 실제 적용된 설정을 먼저 확인한다
systemctl cat cmd-lab-demo --no-pager | head -13
```

```bash
# /usr/lib/systemd/system/cmd-lab-demo.service
[Unit]
Description=cmd-lab demo service

[Service]
ExecStart=/bin/sleep infinity
ExecReload=/bin/true

[Install]
WantedBy=multi-user.target
Alias=cmd-lab-nick.service

# /run/systemd/system/service.d/zzz-lxc-service.conf
```

첫 줄 `# /usr/lib/systemd/system/cmd-lab-demo.service` 가 본 파일 경로입니다. drop-in 이 있으면 이 뒤에 파일마다 이어 붙는데 [유닛 설정과 타이머 시트](./systemctl%20유닛%20설정과%20타이머.md)의 「설정 바꾸기와 daemon-reload」 에서 봅니다.

### 지금 켜고 끄기

> `start`·`stop`·`restart`·`reload` 는 지금 상태만 바꾸고, 부팅 때의 동작은 건드리지 않습니다.

`restart` 는 멈췄다 다시 시작하고 안 떠 있어도 시작하며, PID 가 바뀌는지로 각 명령이 프로세스에 한 일을 구분할 수 있습니다.[^restart]

```bash
# restart 앞뒤로 PID 를 읽는다. PID 가 바뀐다
systemctl show -p MainPID --value cmd-lab-demo    # 21256
systemctl restart cmd-lab-demo
systemctl show -p MainPID --value cmd-lab-demo    # 21279
```

매뉴얼은 `reload` 가 다시 읽는 것이 서비스의 설정이지 systemd 의 유닛 파일이 아니라고 구분합니다.[^reload]

```bash
# reload: 서비스가 자기 설정 파일을 다시 읽게 한다. 프로세스를 바꾸지 않으므로 PID 가 그대로다
systemctl reload cmd-lab-demo
systemctl show -p MainPID --value cmd-lab-demo    # 21279
```

매뉴얼은 `ExecStop=` 에 설정한 명령이 실패해도 매니저가 프로세스를 강제로 끝내므로 `stop` 자체는 실패하지 않는다고 적습니다.[^stop]

```bash
# stop: 서비스를 지금 멈춘다
# try-restart: 떠 있을 때만 재시작하고 꺼져 있으면 아무것도 하지 않는다
#   배포 스크립트에서 "켜져 있던 것만 다시 띄운다" 를 표현할 때 쓴다
systemctl stop cmd-lab-demo
systemctl try-restart cmd-lab-demo       # 꺼져 있으므로 출력 없이 끝난다
systemctl is-active cmd-lab-demo         # inactive (종료 코드 3)

systemctl start cmd-lab-demo
systemctl show -p MainPID --value cmd-lab-demo    # 21291
systemctl try-restart cmd-lab-demo       # 떠 있으므로 재시작한다
systemctl show -p MainPID --value cmd-lab-demo    # 21295
```

```bash
# reload-or-restart: reload 를 지원하면 reload, 아니면 stop 후 start
# ExecReload 가 있는 cmd-lab-demo 에서는 reload 만 하므로 PID 가 유지된다
systemctl reload-or-restart cmd-lab-demo
systemctl show -p MainPID --value cmd-lab-demo    # 21295
```

```bash
# ExecReload 가 없는 서비스에 reload 를 하면 종료 코드 3 으로 거절한다
systemctl start cmd-lab-plain
systemctl show -p MainPID --value cmd-lab-plain    # 21302
systemctl reload cmd-lab-plain
```

```bash
Failed to reload cmd-lab-plain.service: Job type reload is not applicable for unit cmd-lab-plain.service.
```

```bash
# 같은 서비스에 reload-or-restart 를 주면 재시작으로 바뀌어 PID 가 달라진다
systemctl reload-or-restart cmd-lab-plain
systemctl show -p MainPID --value cmd-lab-plain    # 21308
systemctl stop cmd-lab-plain
```

### 부팅 때 켜고 끄기

> `enable` 은 유닛 파일 안의 `[Install]` 내용대로 심볼릭 링크를 만들 뿐 서비스를 지금 시작하지는 않습니다.

`start` 는 지금, `enable` 은 다음 부팅을 담당하는 서로 다른 일이라는 것을 상태 두 개로 확인합니다.[^enable]

```bash
# 지금 켜져 있는 cmd-lab-demo 는 아직 enable 하지 않았다
systemctl is-active cmd-lab-demo     # active
systemctl is-enabled cmd-lab-demo    # disabled (종료 코드 1)
```

```bash
# enable: [Install] 내용대로 링크를 만들어 부팅 때 켜지게 한다. 서비스를 지금 시작하지는 않는다
systemctl enable cmd-lab-demo
```

```bash
Created symlink '/etc/systemd/system/cmd-lab-nick.service' → '/usr/lib/systemd/system/cmd-lab-demo.service'.
Created symlink '/etc/systemd/system/multi-user.target.wants/cmd-lab-demo.service' → '/usr/lib/systemd/system/cmd-lab-demo.service'.
```

링크가 두 개 생깁니다. `multi-user.target.wants/` 안의 링크는 부팅 때 이 타깃이 이 유닛을 원한다는 뜻이고 `[Install]` 의 `Alias=` 는 별칭 링크가 됩니다.

```bash
# 서비스를 멈춰도 enable 상태는 그대로다
systemctl is-enabled cmd-lab-demo     # enabled
systemctl stop cmd-lab-demo
systemctl is-active cmd-lab-demo      # inactive (종료 코드 3)
systemctl is-enabled cmd-lab-demo     # enabled
```

`--now` 는 `enable`·`disable`·`mask` 에 붙여 씁니다.[^now]

```bash
# disable --now: 링크를 지우고 지금도 멈춘다
#   --now   유닛 파일 처리 뒤에 시작·정지까지 한 번에 한다
systemctl disable --now cmd-lab-demo
```

```bash
Removed '/etc/systemd/system/multi-user.target.wants/cmd-lab-demo.service'.
Removed '/etc/systemd/system/cmd-lab-nick.service'.
```

```bash
# enable --now: 링크를 만들고 지금도 시작한다
# list-unit-files --state=enabled 로 enable 된 파일만 모아 볼 수 있다
systemctl enable --now cmd-lab-demo
systemctl is-active cmd-lab-demo    # active
```

```bash
# --now 없이 disable 만 하면 링크만 지우고 떠 있는 서비스는 그대로 떠 있다
systemctl disable cmd-lab-demo
systemctl is-active cmd-lab-demo     # active
systemctl is-enabled cmd-lab-demo    # disabled (종료 코드 1)
```

`[Install]` 이 없는 유닛(`cmd-lab-plain`)에 `enable` 을 하면 설치 설정이 없다는 안내를 길게 출력하고 종료 코드는 0 입니다. 이런 유닛은 다른 유닛이나 소켓이 필요할 때 띄우는 용도입니다.

### 유닛 막기와 풀기

> `mask` 는 유닛 파일을 `/dev/null` 로 링크해서 수동 시작까지 모두 막습니다.

`disable` 은 부팅 때만 빼는 것이고 `mask` 는 `start` 까지 거절하게 만드는 더 센 조치입니다.[^mask]

```bash
# mask --now: 막으면서 지금 떠 있는 것도 멈춘다
systemctl mask --now cmd-lab-demo
```

```bash
Created symlink '/etc/systemd/system/cmd-lab-demo.service' → '/dev/null'.
```

```bash
systemctl is-active cmd-lab-demo     # inactive (종료 코드 3)
systemctl is-enabled cmd-lab-demo    # masked (종료 코드 1)
systemctl start cmd-lab-demo         # Failed to start cmd-lab-demo.service: Unit cmd-lab-demo.service is masked. (종료 코드 1)
systemctl status cmd-lab-demo --no-pager -n 0
```

```bash
○ cmd-lab-demo.service
     Loaded: masked (Reason: Unit cmd-lab-demo.service is masked.)
     Active: inactive (dead)
```

```bash
# unmask: mask 가 만든 링크를 지운다. 지운 뒤에는 다시 시작할 수 있다
# 아래 출력은 unmask 의 것이고 start 는 출력 없이 끝난다
systemctl unmask cmd-lab-demo
systemctl start cmd-lab-demo
```

```bash
Removed '/etc/systemd/system/cmd-lab-demo.service'.
```

`/etc/systemd/system/` 에 같은 이름의 파일이 이미 있는 유닛에는 `mask` 가 실패합니다. 그 경우는 [함정 문서](./systemctl%20함정과%20동작%20원리.md)의 「mask 가 실패하는 경우」 에서 봅니다.

### 실패한 서비스 추적

> 실패하면 `status` 의 `Process:` 줄과 로그 줄이 종료 코드와 이유를 알려 주고, `journalctl -u` 가 같은 로그를 따로 보여 줍니다.

`Type=` 을 적지 않은 서비스는 기본값 `simple` 로 돌아 `start` 자체는 성공하고 실행 직후 실패로 바뀌므로, 잠깐 기다린 뒤에 봅니다.[^simple]

```bash
# 종료 코드 3 으로 끝나는 cmd-lab-fail 로 실패 상태를 만든다
systemctl start cmd-lab-fail
sleep 1
systemctl is-failed cmd-lab-fail    # failed (종료 코드 0)
systemctl is-active cmd-lab-fail    # failed (종료 코드 3)
```

```bash
# 읽는 순서는 세 단계다
#   Active: failed (Result: exit-code)   실패 종류를 본다
#   Process: 줄                           어느 명령이 어떤 코드(status=3)로 끝났는지 확인한다
#   맨 아래 로그                           서비스가 남긴 메시지를 본다
systemctl status cmd-lab-fail --no-pager
```

```bash
× cmd-lab-fail.service - cmd-lab service that fails on purpose
     Loaded: loaded (/etc/systemd/system/cmd-lab-fail.service; static)
    Drop-In: /run/systemd/system/service.d
             └─zzz-lxc-service.conf
     Active: failed (Result: exit-code) since Wed 2026-11-11 23:36:41 KST; 1s ago
   Duration: 2ms
 Invocation: 608345d5de9342a2918514708f846b27
    Process: 22807 ExecStart=/bin/sh -c echo cmd-lab-fail: starting; echo cmd-lab-fail: giving up >&2; exit 3 (code=exited, status=3)
   Main PID: 22807 (code=exited, status=3)
   Mem peak: 1.7M
        CPU: 2ms

Nov 11 23:36:41 ubuntu systemd[1]: Started cmd-lab-fail.service - cmd-lab service that fails on purpose.
Nov 11 23:36:41 ubuntu sh[22807]: cmd-lab-fail: starting
Nov 11 23:36:41 ubuntu sh[22807]: cmd-lab-fail: giving up
Nov 11 23:36:41 ubuntu systemd[1]: cmd-lab-fail.service: Main process exited, code=exited, status=3/NOTIMPLEMENTED
Nov 11 23:36:41 ubuntu systemd[1]: cmd-lab-fail.service: Failed with result 'exit-code'.
```

로그만 더 보려면 `journalctl` 을 씁니다. `journalctl` 의 다른 옵션은 [journalctl 참조 시트](./journalctl.md)에 있습니다.

```bash
# journalctl: 유닛이 남긴 저널 로그를 읽는다
#   systemd 패키지의 외부 바이너리(/usr/bin/journalctl)이고
#   systemctl 과 같은 VM 에서 실측했다
#   -u   이 유닛의 로그만 본다 (--unit)
#   -n   최근 몇 줄만 본다. status 의 -n 과 같은 뜻이다
journalctl \
  -u cmd-lab-fail \
  -n 5 \
  --no-pager
```

```bash
Nov 11 23:36:41 ubuntu systemd[1]: Started cmd-lab-fail.service - cmd-lab service that fails on purpose.
Nov 11 23:36:41 ubuntu sh[22807]: cmd-lab-fail: starting
Nov 11 23:36:41 ubuntu sh[22807]: cmd-lab-fail: giving up
Nov 11 23:36:41 ubuntu systemd[1]: cmd-lab-fail.service: Main process exited, code=exited, status=3/NOTIMPLEMENTED
Nov 11 23:36:41 ubuntu systemd[1]: cmd-lab-fail.service: Failed with result 'exit-code'.
```

`--failed` 는 `--state=failed` 와 같습니다.[^state]

```bash
# 시스템 전체에서 실패한 유닛을 모은다
systemctl list-units --failed 'cmd-lab*' --no-pager
```

```bash
  UNIT                 LOAD   ACTIVE SUB    DESCRIPTION
● cmd-lab-fail.service loaded failed failed cmd-lab service that fails on purpose

Legend: LOAD   → Reflects whether the unit definition was properly loaded.
        ACTIVE → The high-level unit activation state, i.e. generalization of SUB.
        SUB    → The low-level unit activation state, values depend on unit type.

1 loaded units listed.
```

원인을 고친 뒤에도 `reset-failed` 로 지우기 전에는 failed 상태가 목록에 남습니다.[^reset]

```bash
# reset-failed: failed 표시를 지운다
systemctl reset-failed cmd-lab-fail
systemctl is-failed cmd-lab-fail    # inactive (종료 코드 1)
```

### 실습 정리

> 실습이 끝나면 아래 블록으로 만든 유닛 셋과 실습 폴더를 지우고 systemd 를 원래대로 되돌립니다.

[유닛 설정과 타이머 시트](./systemctl%20유닛%20설정과%20타이머.md)의 예까지 돌렸다면 그 시트의 「실습 정리」 도 돌립니다.

```bash
systemctl disable --now cmd-lab-demo; systemctl stop cmd-lab-plain cmd-lab-fail
rm -f \
  /usr/lib/systemd/system/cmd-lab-demo.service \
  /etc/systemd/system/cmd-lab-plain.service \
  /etc/systemd/system/cmd-lab-fail.service
systemctl daemon-reload; systemctl reset-failed 'cmd-lab*'
cd ~ && rm -rf ~/cmd-lab/systemctl
```



## 주의사항과 동작 원리

> 이름과 파일 자리가 만드는 함정은 [systemctl 함정과 동작 원리](./systemctl%20함정과%20동작%20원리.md)에 따로 두었습니다.

- `/etc/systemd/system/` 에 같은 이름의 파일이 있으면 `mask` 가 실패합니다.
- ssh 서비스의 이름이 `ssh` 와 `sshd` 로 갈리고 `ssh.socket` 이 포트를 쥐는 방식이 따로 있습니다.
- `Alias=` 별칭 링크는 `enable` 이 만들고 `disable` 이 지웁니다.



## 관련 문서

> 이 시트와 이어지는 문서입니다.

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [systemctl 함정과 동작 원리](./systemctl%20함정과%20동작%20원리.md) — `mask` 실패, ssh 이름과 소켓, `Alias=` 별칭
- [책 노트 6장 4절, 단위로 말하기](../../../book/learning-modern-linux/06-01.먼저%20켜지는%20것%20하나가%20나머지%20전부를%20켠다.md#4-무엇을-언제-어떻게-돌릴지는-단위로-말한다) — 유닛 종류와 유닛 파일이 놓이는 세 자리
- [책 노트 6장 5절, 손으로 만지는 도구들](../../../book/learning-modern-linux/06-01.먼저%20켜지는%20것%20하나가%20나머지%20전부를%20켠다.md#5-손으로-만지는-도구들) — `enable`·`daemon-reload` 의 기본 흐름
- [유닛 설정과 타이머 시트](./systemctl%20유닛%20설정과%20타이머.md) — `edit`·`daemon-reload` 로 drop-in 쓰기, 타이머로 서비스 주기 실행
- [uname·os-release·lsb_release 참조 시트](../sysinfo/uname%C2%B7os-release%C2%B7lsb_release.md) — 실습 VM 의 배포판과 커널 버전 확인
- [journalctl 참조 시트](./journalctl.md) — `status` 꼬리 로그보다 길게, 시각·부팅·심각도로 좁혀 읽기



## 참고 자료

> 검증 환경, 공식 문서와 각주 정의입니다.

- systemd 259 의 `systemctl --help`·`man systemctl` 원문 — OrbStack Ubuntu 26.04 VM 에서 2026-11-11 확인
- [systemctl(1)](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html) — freedesktop.org 최신판(문서 머리 버전 262)에서 아래 각주의 인용문 존재를 확인
- [systemd.unit(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html) · [systemd.socket(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.socket.html) · [systemd.service(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html)
- Debian 12 `openssh-server` 1:9.2p1-2+deb12u10 패키지 파일 — 2026-11-11 `apt-get download` 후 `dpkg -x`

[^status]: systemctl(1) `status` — "This function is intended to generate human-readable output. If you are looking for computer-parsable output, use show instead." 그리고 "inactive" or "maintenance" is a white circle ("○"), "active" is a green dot ("●"), "deactivating" is a white dot, "failed" or "error" is a red cross ("×"). https://www.freedesktop.org/software/systemd/man/latest/systemctl.html
[^isactive]: systemctl(1) `is-active` — "Returns an exit code 0 if at least one is active, or non-zero otherwise. Unless --quiet is specified, this will also print the current unit state to standard output." `is-failed` — "Returns an exit code 0 if at least one has failed, non-zero otherwise."
[^isenabled]: systemctl(1) `is-enabled` — "Returns an exit code of 0 if at least one is enabled, non-zero otherwise. Prints the current enable status (see table)." 표에서 "static" 은 종료 코드 0, "masked" 는 0 보다 큽니다.
[^listunits]: systemctl(1) `list-units` — "By default, only units which are active, have pending jobs, or have failed are shown; this can be changed with option --all."
[^state]: systemctl(1) `--state=` — "The argument is a comma-separated list of unit LOAD, SUB, or ACTIVE states." `--failed` — "This is equivalent to --state=failed."
[^show]: systemctl(1) `-p, --property=` — "limit display to properties specified in the argument. The argument should be a comma-separated list of property names, such as "MainPID"."
[^cat]: systemctl(1) `cat` — "Show backing files of one or more units. Prints the "fragment" and "drop-ins" (source files) of units." 그리고 "...which might not match the system manager's understanding of these units if any unit files were updated on disk and the daemon-reload command was not issued since."
[^restart]: systemctl(1) `restart` — "Stop and then start one or more units specified on the command line. If the units are not running yet, they will be started." `try-restart` — "This does nothing if units are not running."
[^reload]: systemctl(1) `reload` — "Note that this will reload the service-specific configuration, not the unit configuration file of systemd." `reload-or-restart` — "Reload one or more units if they support it. If not, stop and then start them instead."
[^stop]: systemctl(1) `stop` — "It will not fail if any of the commands configured to stop the unit (ExecStop=, etc.) fail, because the manager will still forcibly terminate the unit."
[^enable]: systemctl(1) `is-enabled` 표 — "enabled" 는 "Enabled via .wants/, .requires/ or Alias= symlinks". 실측 출력의 `Created symlink` 두 줄이 그 링크입니다.
[^now]: systemctl(1) `--now` — "When used with enable, disable, mask, or reenable, also start/stop/try-restart the units after the specified unit file operations succeed."
[^mask]: systemctl(1) `mask` — "This will link these unit files to /dev/null, making it impossible to start them. This is a stronger version of disable". 같은 절 — "If a matching unit file already exists under these directories this operation will hence fail. This means that the operation is primarily useful to mask units shipped by the vendor".
[^simple]: systemd.service(5) `Type=` — "If set to simple (the default if ExecStart= is specified but neither Type= nor BusName= are, and credentials are not used)". 같은 항목 — "systemctl start command lines for simple services will report success even if the service's binary cannot be invoked successfully". https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html
[^reset]: systemctl(1) `reset-failed` — "Reset the "failed" state of the specified units, or if no unit name is passed, reset the state of all units."
[^exitstatus]: systemctl(1) EXIT STATUS — "On success, 0 is returned, a non-zero failure code otherwise." "systemctl uses the return codes defined by LSB" 그리고 LSB return codes 표의 0~4 행. "The mapping of LSB service states to systemd unit states is imperfect, so it is better to not rely on those return values but to look for specific unit states and substates instead." https://www.freedesktop.org/software/systemd/man/latest/systemctl.html
[^exitother]: OrbStack Ubuntu 26.04 VM(systemd 259.9)에서 `명령; echo $?` 로 읽은 실측입니다. systemctl(1) EXIT STATUS 는 0~4 만 표로 정의하고 그 밖의 값은 "a non-zero failure code otherwise." 라고만 적으므로, 없는 유닛에 `start`·`stop`·`restart` 를 준 5 와 잘못된 서브커맨드의 1 은 매뉴얼에 값이 적혀 있지 않습니다. https://www.freedesktop.org/software/systemd/man/latest/systemctl.html
