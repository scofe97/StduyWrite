---
title: systemctl 유닛 설정과 타이머
tags: [linux, cheatsheet, systemctl, systemd, unit, drop-in, timer, reference]
status: draft
source:
  - systemd 259 systemctl(1) (OrbStack Ubuntu 26.04 VM 의 `man systemctl`·`systemctl --help` 원문, freedesktop.org systemctl(1))
  - systemd.service(5)·systemd.timer(5) (freedesktop.org)
related:
  - ./systemctl.md
  - ../README.md
updated: 2026-11-13
---

# systemctl 유닛 설정과 타이머

---

> 유닛 파일을 drop-in 으로 고쳐 반영하고, 서비스와 타이머 유닛을 만들어 주기 실행하는 `systemctl` 을 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> 이 시트는 `systemctl` 로 유닛 파일을 쓰고 고치는 일, 곧 drop-in 편집과 `daemon-reload`, 타이머로 서비스를 주기 실행하는 일을 다룹니다.

[systemctl 참조 시트](./systemctl.md)에서 유닛 파일을 쓰고 고치는 유스케이스를 떼어 낸 것입니다. 예는 그 시트의 「실습 준비」 블록을 돌린 상태에서 이어지고, 출력은 같은 OrbStack Ubuntu 26.04 VM(systemd 259)에서 `sudo bash` 로 받았습니다.



## 핵심 문법

> 서브커맨드는 drop-in 편집과 설정 반영, 타이머 조회 셋이고 옵션은 편집 방식과 drop-in 이름을 정합니다.

```bash
# 호출 형태
# systemctl --help 의 첫 줄
systemctl [OPTIONS...] COMMAND ...

# man systemctl 의 SYNOPSIS. COMMAND 는 서브커맨드, UNIT 은 유닛 이름이나 패턴
systemctl [OPTIONS...] COMMAND [UNIT...]

# 설정을 바꾸고 반영한다 (설정 바꾸기와 daemon-reload)
systemctl edit 유닛
systemctl daemon-reload

# 타이머를 본다 (타이머로 서비스를 주기 실행하기)
systemctl list-timers
```



## 종료 코드

> 종료 코드는 `systemctl` 한 벌이라 이 시트는 목록을 따로 싣지 않습니다.

목록은 [systemctl 참조 시트](./systemctl.md)의 「종료 코드」 에 있습니다.



## 유스케이스

> 예는 앞 예가 만든 상태를 이어 쓰므로 위에서 아래로 차례로 돌립니다.

### 실습 준비

> 아래 블록은 편집기 스크립트를 만들고 `cmd-lab-demo` 를 시작합니다.

먼저 [systemctl 참조 시트](./systemctl.md)의 「실습 준비」 블록을 돌립니다. PID·시각·`Invocation` 값은 실행마다 다르므로 이 시트의 값과 같지 않아도 됩니다.

```bash
# 실습이 끝나면 「실습 정리」 블록으로 모두 지운다

# systemctl 시트의 실습 폴더로 옮긴다. editor.sh 가 여기에 생긴다
cd ~/cmd-lab/systemctl

# 비대화형 edit 용 편집기 스크립트. 「설정 바꾸기와 daemon-reload」 에서 SYSTEMD_EDITOR 로 넘긴다
#   for f; do :; done   마지막 인자(편집할 파일)를 f 에 남긴다
#   sed -i '2a …'       둘째 줄 뒤에 [Service] 와 Environment 두 줄을 끼워 넣는다
cat > editor.sh << 'EOF'
#!/bin/sh
for f; do :; done
sed -i '2a [Service]\nEnvironment=GREETING=hello' "$f"
EOF
chmod +x editor.sh

# 「설정 바꾸기와 daemon-reload」 는 cmd-lab-demo 가 떠 있는 상태에서 시작한다
systemctl start cmd-lab-demo
```

### 설정 바꾸기와 daemon-reload

> 유닛을 고칠 때는 원본을 건드리지 않고 drop-in 조각에 쓰며, 조각 파일을 손으로 만들었다면 `daemon-reload` 를 해야 합니다.

`systemctl edit` 는 `<유닛>.d/override.conf` 라는 drop-in 을 편집기로 열고, 저장하면 `daemon-reload` 까지 알아서 합니다.[^edit] 비대화형 실습을 위해 `SYSTEMD_EDITOR` 환경 변수로 편집기를 `editor.sh` 로 바꿨습니다.[^editor]

```bash
# 편집기 창에는 템플릿이 뜬다. 첫 안내 주석 아래부터
# "Edits below this comment will be discarded" 주석 위까지만
# 파일 내용으로 저장된다
# editor.sh 는 템플릿의 둘째 줄 뒤에 두 줄을 끼워 넣는다
# tty 가 없으면 edit 가 거부하므로 script -qec 로 가상 터미널을 준다
#   -q   script 자신의 안내를 찍지 않는다 (--quiet)
#   -e   자식 프로세스의 종료 코드를 돌려준다 (--return)
#   -c   대화형 셸 대신 주어진 명령을 돌린다 (--command). 마지막 /dev/null 은 기록 파일 자리다
script -qec \
  "SYSTEMD_EDITOR=$PWD/editor.sh systemctl edit cmd-lab-demo" \
  /dev/null
```

```bash
Successfully installed edited file '/etc/systemd/system/cmd-lab-demo.service.d/override.conf'.
```

```bash
systemctl cat cmd-lab-demo --no-pager | head -15
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

# /etc/systemd/system/cmd-lab-demo.service.d/override.conf
[Service]
Environment=GREETING=hello
```

본 파일 아래에 `override.conf` 가 이어 붙어 보입니다.

```bash
# 설정은 daemon-reload 로 곧바로 유닛 정의에 반영됐지만, 이미 떠 있는 프로세스에는 restart 를 해야 닿는다
# 떠 있는 프로세스의 환경 변수. 아직 GREETING 이 없다 (grep 이 아무것도 못 찾아 종료 코드 1)
tr '\0' '\n' < /proc/$(systemctl show -p MainPID --value cmd-lab-demo)/environ \
  | grep GREETING
systemctl restart cmd-lab-demo
tr '\0' '\n' < /proc/$(systemctl show -p MainPID --value cmd-lab-demo)/environ \
  | grep GREETING
# GREETING=hello
```

```bash
# 내용을 파이프로 줘서 drop-in 을 만든다
#   --stdin      편집기 대신 표준 입력을 파일 내용으로 쓴다
#   --drop-in=   조각 파일 이름을 정한다. 기본은 override.conf
printf '[Service]\nNice=5\n' \
  | systemctl edit --stdin --drop-in=nice.conf cmd-lab-demo
```

```bash
Successfully installed edited file '/etc/systemd/system/cmd-lab-demo.service.d/nice.conf'.
```

`daemon-reload` 는 모든 유닛 파일을 다시 읽고 의존성 트리를 새로 만듭니다. 조각 파일을 손으로 만들었다면 이것을 해야 반영됩니다.[^reloadcmd]

```bash
# 편집기를 거치지 않고 조각 파일을 직접 만든다. daemon-reload 를 빠뜨리면 status 첫 줄에 경고가 뜬다
mkdir -p /etc/systemd/system/cmd-lab-demo.service.d
printf '[Service]\nEnvironment=LEVEL=2\n' \
  > /etc/systemd/system/cmd-lab-demo.service.d/manual.conf
systemctl status cmd-lab-demo --no-pager -n 0 | head -8
```

```bash
Warning: The unit file, source configuration file or drop-ins of cmd-lab-demo.service changed on disk. Run 'systemctl daemon-reload' to reload units.
● cmd-lab-demo.service - cmd-lab demo service
     Loaded: loaded (/usr/lib/systemd/system/cmd-lab-demo.service; disabled; preset: enabled)
    Drop-In: /etc/systemd/system/cmd-lab-demo.service.d
             └─nice.conf, override.conf
             /run/systemd/system/service.d
             └─zzz-lxc-service.conf
     Active: active (running) since Wed 2026-11-11 23:36:40 KST; 118ms ago
 Invocation: d234c22bc88e4455bbcaadef6c52aea4
```

경고 줄의 문구가 해결책까지 말해 줍니다. 새 파일이 `Drop-In:` 목록에 없는 것도 확인할 수 있습니다.

```bash
# daemon-reload 전후의 DropInPaths 를 비교한다
systemctl show -p DropInPaths cmd-lab-demo    # DropInPaths=/etc/systemd/system/cmd-lab-demo.service.d/nice.conf /etc/systemd/system/cmd-lab-demo.service.d/override.conf /run/systemd/system/service.d/zzz-lxc-service.conf
systemctl daemon-reload
systemctl show -p DropInPaths cmd-lab-demo    # DropInPaths=/etc/systemd/system/cmd-lab-demo.service.d/manual.conf /etc/systemd/system/cmd-lab-demo.service.d/nice.conf /etc/systemd/system/cmd-lab-demo.service.d/override.conf /run/systemd/system/service.d/zzz-lxc-service.conf
```

반영된 뒤의 `status` 는 경고가 없고 `Drop-In:` 에 `manual.conf` 가 들어 있습니다. 떠 있는 프로세스는 앞의 `GREETING` 처럼 `restart` 를 해야 새 설정으로 돕니다([systemctl 참조 시트](./systemctl.md)의 「지금 켜고 끄기」).

지금까지 만든 `override.conf`·`nice.conf`·`manual.conf` 를 `revert` 로 한 번에 정리합니다.[^revert]

```bash
# revert: drop-in 과 /etc 의 덮어쓰기 파일을 지워 유닛을 배포판 원본으로 되돌린다
systemctl revert cmd-lab-demo
```

```bash
Removed '/etc/systemd/system/cmd-lab-demo.service.d/override.conf'.
Removed '/etc/systemd/system/cmd-lab-demo.service.d/nice.conf'.
Removed '/etc/systemd/system/cmd-lab-demo.service.d/manual.conf'.
Removed '/etc/systemd/system/cmd-lab-demo.service.d'.
```

```bash
systemctl show -p DropInPaths cmd-lab-demo    # DropInPaths=/run/systemd/system/service.d/zzz-lxc-service.conf
```

### 타이머로 서비스를 주기 실행하기

> 서비스와 타이머 두 유닛을 만들고 타이머만 켜면, `list-timers` 는 다음·지난 실행 시각만 보여 주고 성공 여부는 서비스 쪽에서 읽어야 합니다.[^timer]

```bash
# 서비스: 일부러 종료 코드 3 으로 끝난다. Type=oneshot 은 메인 프로세스가 끝난 뒤에 유닛이 올라온 것으로 본다
cat > /etc/systemd/system/cmd-lab-tick.service << 'EOF'
[Service]
Type=oneshot
ExecStart=/bin/sh -c 'echo cmd-lab-tick: ran; exit 3'
EOF

# 타이머: 15초마다 같은 이름의 서비스를 깨운다. AccuracySec 은 깨우는 시각의 허용 오차이고 기본은 1분이다
cat > /etc/systemd/system/cmd-lab-tick.timer << 'EOF'
[Timer]
OnCalendar=*:*:0/15
AccuracySec=1s

[Install]
WantedBy=timers.target
EOF

systemctl daemon-reload
systemctl enable --now cmd-lab-tick.timer

# list-timers: 타이머를 다음에 울릴 때 순으로 보인다. 켜자마자 보면 LAST 와 PASSED 가 - 이다
sleep 20
systemctl list-timers 'cmd-lab*' --no-pager
```

```bash
NEXT                        LEFT LAST                         PASSED UNIT               ACTIVATES
Fri 2026-11-13 13:16:30 KST   3s Fri 2026-11-13 13:16:15 KST 11s ago cmd-lab-tick.timer cmd-lab-tick.service

1 timers listed.
Pass --all to see loaded but inactive timers, too.
```

NEXT 는 다음 실행, LEFT 는 남은 시간, LAST 는 지난 실행, PASSED 는 그 뒤 흐른 시간입니다. 성공 여부를 보이는 열은 없으므로 결과는 서비스 유닛에 묻습니다.

```bash
# 종료 코드 3 으로 끝난 실행이 서비스에 failed 로 남았다. 확인했으면 타이머를 멈추고 부팅 때의 시작도 끈다
systemctl is-failed cmd-lab-tick.service      # failed (종료 코드 0)
systemctl disable --now cmd-lab-tick.timer    # Removed '/etc/systemd/system/timers.target.wants/cmd-lab-tick.timer'.
```

### 실습 정리

> 실습이 끝나면 아래 블록으로 이 시트가 만든 타이머 유닛과 drop-in 을 지웁니다.

[systemctl 참조 시트](./systemctl.md)의 「실습 정리」 도 함께 돌려야 `cmd-lab-demo` 가 멈추고 나머지 유닛과 실습 폴더가 지워집니다.

```bash
systemctl disable --now cmd-lab-tick.timer
rm -rf /etc/systemd/system/cmd-lab-demo.service.d
rm -f /etc/systemd/system/cmd-lab-tick.service
rm -f /etc/systemd/system/cmd-lab-tick.timer
systemctl daemon-reload; systemctl reset-failed 'cmd-lab*'
```



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [systemctl 참조 시트](./systemctl.md) — 이 시트가 이어받는 실습 준비와 상태 조회·제어 예



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- systemd 259 의 `systemctl --help`·`man systemctl` 원문 — OrbStack Ubuntu 26.04 VM 에서 2026-11-11 확인
- [systemctl(1)](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html) — freedesktop.org 최신판(문서 머리 버전 262)에서 아래 각주의 인용문 존재를 확인
- [systemd.service(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html) — 「타이머로 서비스를 주기 실행하기」 의 `Type=oneshot`
- [systemd.timer(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html) — 「타이머로 서비스를 주기 실행하기」 의 `OnCalendar=`·`AccuracySec=`

[^edit]: systemctl(1) `edit` — "After the editing is finished, configuration is reloaded, equivalent to systemctl daemon-reload --system". "If --drop-in= is specified, the given drop-in file name will be used instead of the default override.conf." `--stdin` — "If --stdin is specified, the new contents will be read from standard input."
[^editor]: systemctl(1) ENVIRONMENT — "$SYSTEMD_EDITOR: Editor to use when editing units; overrides $EDITOR and $VISUAL."
[^reloadcmd]: systemctl(1) `daemon-reload` — "This will rerun all generators (see systemd.generator(7)), reload all unit files, and recreate the entire dependency tree." 경고 문구 "changed on disk. Run 'systemctl daemon-reload' to reload units." 는 실측 출력에서 확인했고 매뉴얼에는 없습니다.
[^revert]: systemctl(1) `revert` — "This command removes drop-in configuration files that modify the specified units, as well as any user-configured unit file that overrides a matching vendor supplied unit file."
[^timer]: systemctl(1) `list-timers` — "List timer units currently in memory, ordered by the time they elapse next." "NEXT shows the next time the timer will run. LEFT shows how long till the next time the timer runs. LAST shows the last time the timer ran. PASSED shows how long has passed since the timer last ran." systemd.timer(5) `OnCalendar=` — "Defines realtime (i.e. wallclock) timers with calendar event expressions." `AccuracySec=` — "Specify the accuracy the timer shall elapse with. Defaults to 1min." systemd.service(5) `Type=oneshot` — "the service manager will consider the unit up after the main process exits." https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html
