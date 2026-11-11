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
  - ../../../book/learning-modern-linux/06-01.먼저%20켜지는%20것%20하나가%20나머지%20전부를%20켠다.md
  - ../sysinfo/uname%C2%B7os-release%C2%B7hostnamectl.md
updated: 2026-11-11
---

# systemctl 참조 시트

---

> 서비스의 상태를 읽고, 지금 켜고 끄고, 부팅 때 켜지게 하고, 설정을 바꾸는 `systemctl` 을 따라 치면 그대로 나오는 예제로 모았습니다.

## 실습 준비

> 아래 블록을 root 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 유닛 셋과 편집기 스크립트가 생깁니다.

`systemctl` 은 PID 1 이 `systemd` 인 시스템에서만 동작하므로 `docker run` 컨테이너로는 실습할 수 없습니다.

이 시트의 출력은 OrbStack 의 Ubuntu 26.04 VM(systemd 259)에서 `sudo bash` 로 받았습니다. 설치 파일을 풀어 보는 10절의 둘째 부분만 Debian 12 컨테이너에서 받았습니다.

이 VM 은 모든 service 에 OrbStack 이 만든 drop-in `zzz-lxc-service.conf` 를 붙입니다. 그래서 `status` 출력에 `Drop-In:` 줄이 항상 나옵니다. 다른 서버에서는 drop-in 이 하나도 없을 때만 이 줄이 빠집니다.

```bash
mkdir -p ~/cmd-lab/systemctl && cd ~/cmd-lab/systemctl
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
cat > /etc/systemd/system/cmd-lab-plain.service << 'EOF'
[Unit]
Description=cmd-lab service without ExecReload

[Service]
ExecStart=/bin/sleep infinity
EOF
cat > /etc/systemd/system/cmd-lab-fail.service << 'EOF'
[Unit]
Description=cmd-lab service that fails on purpose

[Service]
ExecStart=/bin/sh -c 'echo cmd-lab-fail: starting; echo cmd-lab-fail: giving up >&2; exit 3'
EOF
cat > editor.sh << 'EOF'
#!/bin/sh
for f; do :; done
sed -i '2a [Service]\nEnvironment=GREETING=hello' "$f"
EOF
chmod +x editor.sh
systemctl daemon-reload
```

`cmd-lab-demo` 는 `sleep infinity` 를 띄우는 서비스입니다. `ExecReload` 와 `[Install]` 이 있어 reload 와 enable 을 모두 받습니다.

이 유닛은 패키지가 설치한 유닛처럼 `/usr/lib/systemd/system` 에 두었습니다. 8절의 `mask` 가 그 자리의 유닛에만 먹기 때문입니다. `cmd-lab-plain` 은 `ExecReload` 와 `[Install]` 이 없는 서비스입니다. `cmd-lab-fail` 은 종료 코드 3 으로 곧바로 끝나는 서비스입니다. 실습이 끝나면 맨 아래 정리 블록으로 모두 지웁니다.

PID·시각·`Invocation` 값은 실행마다 다르므로 이 시트의 값과 같지 않아도 됩니다. 주석에 적은 종료 코드는 명령을 실행한 직후 `$?` 로 읽은 값입니다.



## 1. 서비스 상태 읽기

> `status` 한 번으로 이 서비스가 지금 떠 있는지, 부팅 때 켜지는지, 마지막 로그가 무엇인지를 함께 봅니다.

`status` 는 사람이 읽는 요약입니다. 스크립트가 값을 파싱할 용도라면 4절의 `show` 를 쓰라고 매뉴얼이 적어 둡니다.[^status] 터미널에서는 출력이 길면 pager 로 넘어가므로 아래 예는 `--no-pager` 를 붙였습니다.

```bash
# 켜기 전의 서비스. Active: inactive (dead), 종료 코드 3
systemctl status cmd-lab-demo --no-pager | head -5
```

```bash
○ cmd-lab-demo.service - cmd-lab demo service
     Loaded: loaded (/usr/lib/systemd/system/cmd-lab-demo.service; disabled; preset: enabled)
    Drop-In: /run/systemd/system/service.d
             └─zzz-lxc-service.conf
     Active: inactive (dead)
```

`Loaded:` 줄은 유닛 파일 경로와 부팅 때 켜지는지(`disabled`)를 보이고 `Active:` 줄은 지금 상태를 보입니다. 앞의 `○` 는 inactive, `●` 는 active, `×` 는 failed 를 뜻합니다.[^status]

```bash
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

`Main PID` 와 `CGroup` 은 이 서비스가 실제로 쥔 프로세스를 가리키고, 맨 아래 빈 줄 뒤의 줄들이 저널에서 가져온 최근 로그입니다. 로그만 빼고 싶으면 `-n 0` 을 줍니다.

```bash
# -n 0 (--lines=0): 저널 로그 줄을 0줄로. 기본은 10줄
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

없는 유닛이면 한 줄 메시지와 함께 종료 코드 4 로 끝납니다.

```bash
systemctl status cmd-lab-nothing --no-pager    # Unit cmd-lab-nothing.service could not be found. (종료 코드 4)
```



## 2. 스크립트에서 상태로 분기하기

> `is-active`·`is-enabled`·`is-failed` 는 상태 이름을 출력하고 종료 코드로도 답해서 `if` 에 그대로 넣을 수 있습니다.

`is-active` 는 하나라도 active 이면 종료 코드 0, 아니면 0 이 아닌 값을 돌려줍니다. `--quiet` 를 주지 않으면 상태 이름도 출력합니다.[^isactive] `is-failed` 는 반대로 failed 일 때 0 입니다.[^isactive]

```bash
systemctl is-active cmd-lab-demo    # active (종료 코드 0)
systemctl is-active cmd-lab-plain   # inactive (종료 코드 3)
systemctl is-active cmd-lab-nothing # inactive (종료 코드 4)
```

종료 코드 3 은 꺼진 유닛이고 4 는 없는 유닛이라 오타와 정지를 구분할 수 있습니다.

```bash
# -q (--quiet): 출력 없이 종료 코드만
systemctl is-active -q cmd-lab-demo    # 출력 없음 (종료 코드 0)

# 스크립트에서 쓰는 모양
if systemctl is-active --quiet cmd-lab-demo; then echo running; else echo not-running; fi    # running
```

`is-enabled` 는 부팅 때 켜지는지를 묻습니다. 켜지게 설정된 경우 0, 아니면 0 이 아닙니다. `[Install]` 이 없는 유닛은 `static` 이고 이것도 0 입니다.[^isenabled]

```bash
systemctl is-enabled cmd-lab-demo     # disabled (종료 코드 1)
systemctl is-enabled cmd-lab-plain    # static (종료 코드 0)
systemctl is-enabled cmd-lab-nothing  # not-found (종료 코드 4)
```

```bash
# 정상인 서비스에 is-failed 를 물으면 현재 상태를 출력하고 종료 코드 1
systemctl is-failed cmd-lab-demo    # active (종료 코드 1)
```

failed 일 때 0 이 되는 예는 11절에 있습니다.



## 3. 유닛 목록 뽑기

> 지금 메모리에 올라 있는 유닛은 `list-units`, 디스크에 설치된 유닛 파일은 `list-unit-files` 로 봅니다.

두 명령은 보는 대상이 다릅니다. `list-units` 는 메모리에 올라온 유닛만 보여서 꺼져 있고 실패하지도 않은 유닛은 목록에 없습니다.[^listunits] 이름 패턴을 따옴표로 감싸서 주면 `cmd-lab` 으로 시작하는 것만 고릅니다.

```bash
# --type=service --state=running: 서비스 유닛 중 running 상태만. 인자 없이 쓰면 모든 유닛이 나오고 패턴은 이름으로 좁힌다
systemctl list-units --type=service --state=running 'cmd-lab*' --no-pager
```

```bash
  UNIT                 LOAD   ACTIVE SUB     DESCRIPTION
  cmd-lab-demo.service loaded active running cmd-lab demo service

Legend: LOAD   → Reflects whether the unit definition was properly loaded.
        ACTIVE → The high-level unit activation state, i.e. generalization of SUB.
        SUB    → The low-level unit activation state, values depend on unit type.

1 loaded units listed.
```

`-t`(`--type`)는 `service`·`socket` 같은 유닛 종류를, `--state` 는 LOAD·SUB·ACTIVE 중 아무 상태나 받습니다. `--failed` 는 `--state=failed` 와 같습니다.[^state] 머리글과 범례는 사람에게는 도움이지만 `awk`·`wc` 로 넘길 때는 방해라서 `--no-legend` 로 뺍니다.

```bash
# --no-legend: 머리글·범례·합계 줄을 뺀다
systemctl list-units --type=service --state=running --no-legend 'cmd-lab*' --no-pager
```

```bash
  cmd-lab-demo.service loaded active running cmd-lab demo service
```

`list-unit-files` 는 설치된 유닛 파일과 그 enable 상태를 보여 줍니다. `PRESET` 열은 배포판의 preset 정책이 이 유닛을 어떻게 켜라고 하는지입니다.

```bash
systemctl list-unit-files 'cmd-lab*' --no-pager
```

```bash
UNIT FILE             STATE    PRESET
cmd-lab-demo.service  disabled enabled
cmd-lab-fail.service  static   -
cmd-lab-plain.service static   -

3 unit files listed.
```

`--state=disabled` 처럼 `list-unit-files` 도 `--state` 로 거를 수 있습니다. 실패한 유닛만 모으는 `--failed` 는 11절에서 씁니다.



## 4. 속성 하나만 뽑기

> 스크립트가 파싱할 값은 `status` 가 아니라 `show -p` 로 뽑습니다.

`show` 는 `이름=값` 줄을 냅니다. `-p`(`--property`)는 콤마로 나눈 속성 이름만 보이게 합니다.[^show]

```bash
# -p (--property): 보일 속성을 콤마로 나눠 고른다
systemctl show -p ActiveState,SubState cmd-lab-demo
```

```bash
ActiveState=active
SubState=running
```

```bash
# --value: 속성 이름 없이 값만. 변수에 담을 때 쓴다
systemctl show -p MainPID --value cmd-lab-demo    # 21256
```

`FragmentPath`·`UnitFileState` 처럼 유닛 파일 위치와 enable 상태도 `-p` 로 뽑을 수 있습니다. `-p` 없이 쓰면 모든 속성이 수백 줄 나오므로 `systemctl show 유닛 | head` 로 이름을 훑어 필요한 속성을 찾습니다. `ExecReload` 같은 구조 속성도 `-p` 로 한 줄씩 뽑을 수 있습니다.



## 5. 실제로 읽힌 유닛 파일 보기

> `cat` 은 유닛의 본 파일과 drop-in 을 한 번에 이어서 보여 줍니다.

`systemctl cat` 은 유닛의 fragment(본 파일)와 drop-in 파일을 각각 파일 이름 주석을 앞에 붙여 출력합니다. 디스크 내용이라서 `daemon-reload` 를 하지 않고 파일을 고쳤다면 systemd 가 아는 내용과 다를 수 있습니다.[^cat]

```bash
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

첫 줄 `# /usr/lib/systemd/system/cmd-lab-demo.service` 가 본 파일 경로입니다. drop-in 이 있으면 이 뒤에 파일마다 이어 붙는데 9절에서 봅니다. 어떤 서비스가 기대와 다르게 동작할 때 이 명령으로 실제 적용된 설정을 먼저 확인합니다.



## 6. 지금 켜고 끄기

> `start`·`stop`·`restart`·`reload` 는 지금 상태만 바꾸고, 부팅 때의 동작은 건드리지 않습니다.

PID 가 바뀌는지로 각 명령이 프로세스에 한 일을 구분할 수 있습니다. `restart` 는 멈췄다 다시 시작하고 안 떠 있어도 시작합니다.[^restart]

```bash
systemctl show -p MainPID --value cmd-lab-demo    # 21256
systemctl restart cmd-lab-demo
systemctl show -p MainPID --value cmd-lab-demo    # 21279
```

`reload` 는 서비스가 자기 설정 파일을 다시 읽게 하는 것이어서 프로세스를 바꾸지 않습니다. 매뉴얼은 이것이 서비스의 설정이지 systemd 의 유닛 파일이 아니라고 구분합니다.[^reload]

```bash
systemctl reload cmd-lab-demo
systemctl show -p MainPID --value cmd-lab-demo    # 21279
```

PID 가 그대로입니다. `try-restart` 는 떠 있을 때만 재시작하고 꺼져 있으면 아무것도 하지 않습니다. 배포 스크립트에서 "켜져 있던 것만 다시 띄운다" 를 표현할 때 씁니다.[^restart]

```bash
systemctl stop cmd-lab-demo
systemctl try-restart cmd-lab-demo       # 꺼져 있으므로 출력 없이 끝난다
systemctl is-active cmd-lab-demo         # inactive (종료 코드 3)

systemctl start cmd-lab-demo
systemctl show -p MainPID --value cmd-lab-demo    # 21291
systemctl try-restart cmd-lab-demo       # 떠 있으므로 재시작한다
systemctl show -p MainPID --value cmd-lab-demo    # 21295
```

`reload-or-restart` 는 `ExecReload` 가 있는 `cmd-lab-demo` 에서는 reload 만 하므로 PID 가 유지됩니다.

```bash
# reload-or-restart: reload 를 지원하면 reload, 아니면 stop 후 start
systemctl reload-or-restart cmd-lab-demo
systemctl show -p MainPID --value cmd-lab-demo    # 21295
```

`ExecReload` 가 없는 서비스에 `reload` 를 하면 종료 코드 3 으로 거절합니다.

```bash
systemctl start cmd-lab-plain
systemctl show -p MainPID --value cmd-lab-plain    # 21302
systemctl reload cmd-lab-plain
```

```bash
Failed to reload cmd-lab-plain.service: Job type reload is not applicable for unit cmd-lab-plain.service.
```

같은 서비스에 `reload-or-restart` 를 주면 재시작으로 바뀌어 PID 가 달라집니다.

```bash
systemctl reload-or-restart cmd-lab-plain
systemctl show -p MainPID --value cmd-lab-plain    # 21308
systemctl stop cmd-lab-plain
```

`stop` 은 서비스를 멈춥니다. 매뉴얼은 stop 에 설정된 `ExecStop=` 명령이 실패해도 매니저가 프로세스를 강제로 끝내므로 `stop` 자체는 실패하지 않는다고 적습니다.[^stop]



## 7. 부팅 때 켜고 끄기

> `enable` 은 유닛 파일 안의 `[Install]` 내용대로 심볼릭 링크를 만들 뿐 서비스를 지금 시작하지는 않습니다.

`start` 는 지금, `enable` 은 다음 부팅을 담당하는 서로 다른 일이라는 것을 상태 두 개로 확인합니다.[^enable] 지금 켜져 있는 `cmd-lab-demo` 는 아직 enable 하지 않았습니다.

```bash
systemctl is-active cmd-lab-demo     # active
systemctl is-enabled cmd-lab-demo    # disabled (종료 코드 1)
```

```bash
systemctl enable cmd-lab-demo
```

```bash
Created symlink '/etc/systemd/system/cmd-lab-nick.service' → '/usr/lib/systemd/system/cmd-lab-demo.service'.
Created symlink '/etc/systemd/system/multi-user.target.wants/cmd-lab-demo.service' → '/usr/lib/systemd/system/cmd-lab-demo.service'.
```

`enable` 은 링크 두 개를 만들었습니다. `multi-user.target.wants/` 안의 링크는 부팅 때 이 타깃이 이 유닛을 원한다는 뜻입니다. `[Install]` 의 `Alias=` 는 별칭 링크가 됩니다. 이제 서비스를 멈춰도 enable 상태는 그대로입니다.

```bash
systemctl is-enabled cmd-lab-demo     # enabled
systemctl stop cmd-lab-demo
systemctl is-active cmd-lab-demo      # inactive (종료 코드 3)
systemctl is-enabled cmd-lab-demo     # enabled
```

`--now` 는 enable·disable·mask 와 함께 쓰면 유닛 파일 처리 뒤에 시작·정지까지 한 번에 합니다.[^now]

```bash
# disable --now: 링크를 지우고 지금도 멈춘다
systemctl disable --now cmd-lab-demo
```

```bash
Removed '/etc/systemd/system/multi-user.target.wants/cmd-lab-demo.service'.
Removed '/etc/systemd/system/cmd-lab-nick.service'.
```

```bash
# enable --now: 링크를 만들고 지금도 시작한다
systemctl enable --now cmd-lab-demo
systemctl is-active cmd-lab-demo    # active
```

`list-unit-files --state=enabled` 로 enable 된 파일만 모아 볼 수 있습니다. 반대로 `--now` 없이 `disable` 만 하면 떠 있는 서비스는 그대로 떠 있습니다.

```bash
systemctl disable cmd-lab-demo
systemctl is-active cmd-lab-demo     # active
systemctl is-enabled cmd-lab-demo    # disabled (종료 코드 1)
```

`[Install]` 이 없는 유닛(`cmd-lab-plain`)에 `enable` 을 하면 설치 설정이 없다는 안내를 길게 출력합니다. 종료 코드는 0 입니다. 이런 유닛은 다른 유닛이나 소켓이 필요할 때 띄우는 용도입니다.



## 8. 유닛 막기와 풀기

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

`unmask` 가 링크를 지우면 다시 시작할 수 있습니다. 아래 출력은 `unmask` 의 것이고 `start` 는 출력 없이 끝납니다.

```bash
systemctl unmask cmd-lab-demo
systemctl start cmd-lab-demo
```

```bash
Removed '/etc/systemd/system/cmd-lab-demo.service'.
```

`mask` 는 같은 이름의 파일이 `/etc/systemd/system/` 에 이미 있으면 실패합니다. 직접 만든 유닛에는 보통 통하지 않고 패키지가 `/usr/lib/systemd/system/` 에 둔 유닛을 막는 용도라고 매뉴얼이 적습니다.[^mask] 실습 준비에서 `cmd-lab-demo` 를 `/usr/lib` 에 둔 이유가 이것입니다.

```bash
systemctl mask cmd-lab-plain    # Failed to mask unit: File '/etc/systemd/system/cmd-lab-plain.service' already exists (종료 코드 1)
```



## 9. 설정 바꾸기와 daemon-reload

> 유닛을 고칠 때는 원본을 건드리지 않고 drop-in 조각에 쓰며, 조각 파일을 손으로 만들었다면 `daemon-reload` 를 해야 합니다.

`systemctl edit` 는 `<유닛>.d/override.conf` 라는 drop-in 을 편집기로 엽니다. 저장하면 `daemon-reload` 까지 알아서 합니다.[^edit]

편집기 창에는 템플릿이 뜹니다. 첫 안내 주석 아래부터 "Edits below this comment will be discarded" 주석 위까지만 파일 내용으로 저장됩니다. 비대화형 실습을 위해 `SYSTEMD_EDITOR` 환경 변수로 편집기를 `editor.sh` 로 바꿨습니다.[^editor] 이 스크립트는 템플릿의 둘째 줄 뒤에 두 줄을 끼워 넣습니다. tty 가 없으면 `edit` 가 거부하므로 `script -qec` 로 가상 터미널을 줍니다.

```bash
# SYSTEMD_EDITOR: edit 가 열 편집기를 지정. 여기서는 내용을 자동으로 채우는 스크립트
script -qec "SYSTEMD_EDITOR=$PWD/editor.sh systemctl edit cmd-lab-demo" /dev/null
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

본 파일 아래에 `override.conf` 가 이어 붙어 보입니다. 설정은 `daemon-reload` 로 곧바로 유닛 정의에 반영됐지만, 이미 떠 있는 프로세스에는 `restart` 를 해야 닿습니다.

```bash
# 떠 있는 프로세스의 환경 변수. 아직 GREETING 이 없다 (grep 이 아무것도 못 찾아 종료 코드 1)
tr '\0' '\n' < /proc/$(systemctl show -p MainPID --value cmd-lab-demo)/environ | grep GREETING
systemctl restart cmd-lab-demo
tr '\0' '\n' < /proc/$(systemctl show -p MainPID --value cmd-lab-demo)/environ | grep GREETING    # GREETING=hello
```

내용을 파이프로 주려면 `--stdin` 을 쓰고, 파일 이름은 `--drop-in=` 으로 정합니다. 기본은 `override.conf` 입니다.[^edit]

```bash
# --stdin: 편집기 대신 표준 입력을 파일 내용으로. --drop-in=nice.conf: 조각 파일 이름
printf '[Service]\nNice=5\n' | systemctl edit --stdin --drop-in=nice.conf cmd-lab-demo
```

```bash
Successfully installed edited file '/etc/systemd/system/cmd-lab-demo.service.d/nice.conf'.
```

편집기를 거치지 않고 조각 파일을 직접 만들었다면 `daemon-reload` 가 필요합니다. 이 명령은 모든 유닛 파일을 다시 읽고 의존성 트리를 새로 만듭니다.[^reloadcmd] 빠뜨리면 `status` 첫 줄에 경고가 뜹니다.

```bash
mkdir -p /etc/systemd/system/cmd-lab-demo.service.d
printf '[Service]\nEnvironment=LEVEL=2\n' > /etc/systemd/system/cmd-lab-demo.service.d/manual.conf
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
systemctl show -p DropInPaths cmd-lab-demo    # DropInPaths=/etc/systemd/system/cmd-lab-demo.service.d/nice.conf /etc/systemd/system/cmd-lab-demo.service.d/override.conf /run/systemd/system/service.d/zzz-lxc-service.conf
systemctl daemon-reload
systemctl show -p DropInPaths cmd-lab-demo    # DropInPaths=/etc/systemd/system/cmd-lab-demo.service.d/manual.conf /etc/systemd/system/cmd-lab-demo.service.d/nice.conf /etc/systemd/system/cmd-lab-demo.service.d/override.conf /run/systemd/system/service.d/zzz-lxc-service.conf
```

반영된 뒤의 `status` 는 경고가 없고 `Drop-In:` 에 `manual.conf` 가 들어 있습니다. 이 서비스는 `restart` 하기 전까지 옛 설정으로 돌고 있으니 설정을 바꾼 뒤 필요하면 6절의 방법으로 재시작합니다.

`revert` 는 drop-in 과 `/etc` 의 덮어쓰기 파일을 지워 유닛을 배포판 원본으로 되돌립니다. 지금까지 만든 `override.conf`·`nice.conf`·`manual.conf` 를 한 번에 정리합니다.[^revert]

```bash
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



## 10. 서비스 이름 함정, ssh 와 별칭

> 같은 서비스가 이름 둘로 불리는 것은 `[Install]` 의 `Alias=` 때문이고, 어떤 이름의 유닛이 있는지는 패키지가 정합니다.

ssh 서버의 유닛 이름은 배포판 문서마다 `ssh` 와 `sshd` 로 갈립니다. 이 VM 에는 ssh 서버 패키지가 없어서 둘 다 없다고 나옵니다.

```bash
systemctl list-unit-files 'ssh*' --no-pager
```

```bash
UNIT FILE         STATE  PRESET
ssh-access.target static -

1 unit files listed.
```

```bash
systemctl status ssh --no-pager    # Unit ssh.service could not be found. (종료 코드 4)
systemctl cat ssh.socket --no-pager    # No files found for ssh.socket. (종료 코드 1)
```

`ssh-access.target` 은 OrbStack 이 만든 것이라 sshd 와 무관합니다. 서버가 설치된 경우의 유닛 파일은 패키지에서 직접 확인합니다. Debian 12 컨테이너에서 `openssh-server` 패키지를 설치하지 않고 받아 풀어 봅니다(이 부분은 Debian 12 에서 받은 출력입니다).

```bash
apt-get update -qq >/dev/null 2>&1
mkdir -p ~/cmd-lab/systemctl-pkg && cd ~/cmd-lab/systemctl-pkg
apt-get download openssh-server >/dev/null 2>&1
dpkg -x openssh-server_*.deb pkg
ls pkg/lib/systemd/system
```

```bash
rescue-ssh.target
ssh.service
ssh.socket
```

```bash
grep -n -E '^(Alias|WantedBy)' pkg/lib/systemd/system/ssh.service
```

```bash
21:WantedBy=multi-user.target
22:Alias=sshd.service
```

서비스 본 이름은 `ssh.service` 이고 `Alias=sshd.service` 로 `sshd` 라는 별칭을 겹쳐 답니다. 그래서 `systemctl status sshd` 도 같은 유닛을 가리킵니다. 같은 패키지에는 `ssh.socket` 도 들어 있어서 `ssh` 를 멈춰도 소켓 유닛이 포트를 계속 쥐고 있을 수 있습니다.

```bash
grep -n -E '^(ListenStream|WantedBy)' pkg/lib/systemd/system/ssh.socket
```

```bash
7:ListenStream=22
11:WantedBy=sockets.target
```

socket 유닛은 같은 이름의 service 유닛을 접속이 들어올 때 띄웁니다.[^socket] 이 소켓을 enable 한 시스템에서 `systemctl stop ssh` 만 하면 다음 접속에 서비스가 다시 뜰 수 있습니다. 그러니 `ssh.socket` 도 함께 봅니다. 설치한 쪽의 실제 상태는 `systemctl list-unit-files 'ssh*'` 로 확인하는 것이 확실합니다. Ubuntu 의 버전별 기본값은 이 환경에서 Ubuntu 공식 문서에 접근할 수 없어 확인하지 못했습니다.

별칭이 `enable` 에서 어떻게 만들어지는지는 실습 유닛으로 볼 수 있습니다. 7절에서 보았듯이 `enable` 은 `cmd-lab-nick.service` 링크를 만들었습니다.

```bash
systemctl enable --now cmd-lab-demo
systemctl is-active cmd-lab-nick    # active
systemctl status cmd-lab-nick --no-pager -n 0 | head -4
```

```bash
● cmd-lab-demo.service - cmd-lab demo service
     Loaded: loaded (/usr/lib/systemd/system/cmd-lab-demo.service; enabled; preset: enabled)
    Drop-In: /run/systemd/system/service.d
             └─zzz-lxc-service.conf
```

별칭 이름으로 물어도 첫 줄은 본 이름 `cmd-lab-demo.service` 입니다. `Id` 와 `Names` 로 둘의 관계를 확인합니다.

```bash
systemctl show -p Id,Names cmd-lab-nick
```

```bash
Id=cmd-lab-demo.service
Names=cmd-lab-demo.service cmd-lab-nick.service
```

```bash
systemctl disable --now cmd-lab-demo
```

```bash
Removed '/etc/systemd/system/multi-user.target.wants/cmd-lab-demo.service'.
Removed '/etc/systemd/system/cmd-lab-nick.service'.
```

별칭 링크는 enable 할 때만 생기고 disable 하면 함께 지워집니다.



## 11. 실패한 서비스 추적

> 실패하면 `status` 의 `Process:` 줄과 로그 줄이 종료 코드와 이유를 알려 주고, `journalctl -u` 가 같은 로그를 따로 보여 줍니다.

종료 코드 3 으로 끝나는 `cmd-lab-fail` 로 실패 상태를 만듭니다. `Type=` 을 적지 않은 서비스는 기본값 `simple` 로 돌아 `start` 자체는 성공하고 실행 직후 실패로 바뀌므로, 잠깐 기다린 뒤에 봅니다.[^simple]

```bash
systemctl start cmd-lab-fail
sleep 1
systemctl is-failed cmd-lab-fail    # failed (종료 코드 0)
systemctl is-active cmd-lab-fail    # failed (종료 코드 3)
```

`is-failed` 는 이번에는 0 으로 끝납니다. 이어서 `status` 를 봅니다.

```bash
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

읽는 순서는 세 단계입니다. `Active: failed (Result: exit-code)` 에서 실패 종류를 봅니다. `Process:` 줄에서 어느 명령이 어떤 코드(`status=3`)로 끝났는지 확인하고 맨 아래 로그에서 서비스가 남긴 메시지를 봅니다. 로그 줄 수는 `-n 숫자` 로 정합니다. 기본은 10줄이고 1절의 `-n 0` 은 로그를 모두 뺍니다.

로그만 더 보려면 `journalctl` 을 씁니다. `journalctl` 의 다른 옵션은 이 시트에서 다루지 않습니다.

```bash
# -u (--unit): 이 유닛의 로그만. -n 5: 최근 5줄
journalctl -u cmd-lab-fail -n 5 --no-pager
```

```bash
Nov 11 23:36:41 ubuntu systemd[1]: Started cmd-lab-fail.service - cmd-lab service that fails on purpose.
Nov 11 23:36:41 ubuntu sh[22807]: cmd-lab-fail: starting
Nov 11 23:36:41 ubuntu sh[22807]: cmd-lab-fail: giving up
Nov 11 23:36:41 ubuntu systemd[1]: cmd-lab-fail.service: Main process exited, code=exited, status=3/NOTIMPLEMENTED
Nov 11 23:36:41 ubuntu systemd[1]: cmd-lab-fail.service: Failed with result 'exit-code'.
```

시스템 전체에서 실패한 유닛은 `--failed` 로 모읍니다. `--state=failed` 와 같습니다.[^state]

```bash
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

원인을 고친 뒤에는 `reset-failed` 로 failed 표시를 지웁니다. 지우기 전에는 이 상태가 목록에 남습니다.[^reset]

```bash
systemctl reset-failed cmd-lab-fail
systemctl is-failed cmd-lab-fail    # inactive (종료 코드 1)
```

실습이 끝나면 다음으로 만든 것을 지웁니다.

```bash
systemctl disable --now cmd-lab-demo; systemctl stop cmd-lab-plain cmd-lab-fail
rm -rf /etc/systemd/system/cmd-lab-demo.service.d
rm -f /usr/lib/systemd/system/cmd-lab-demo.service /etc/systemd/system/cmd-lab-plain.service /etc/systemd/system/cmd-lab-fail.service
systemctl daemon-reload; systemctl reset-failed 'cmd-lab*'
```



## 관련 문서

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [책 노트 6장 4절, 단위로 말하기](../../../book/learning-modern-linux/06-01.먼저%20켜지는%20것%20하나가%20나머지%20전부를%20켠다.md#4-무엇을-언제-어떻게-돌릴지는-단위로-말한다) — 유닛 종류와 유닛 파일이 놓이는 세 자리
- [책 노트 6장 5절, 손으로 만지는 도구들](../../../book/learning-modern-linux/06-01.먼저%20켜지는%20것%20하나가%20나머지%20전부를%20켠다.md#5-손으로-만지는-도구들) — `enable`·`daemon-reload` 의 기본 흐름
- [uname·os-release·hostnamectl](../sysinfo/uname%C2%B7os-release%C2%B7hostnamectl.md) — 실습 VM 의 배포판과 커널 버전 확인



## 참고 자료

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
[^edit]: systemctl(1) `edit` — "After the editing is finished, configuration is reloaded, equivalent to systemctl daemon-reload --system". "If --drop-in= is specified, the given drop-in file name will be used instead of the default override.conf." `--stdin` — "If --stdin is specified, the new contents will be read from standard input."
[^editor]: systemctl(1) ENVIRONMENT — "$SYSTEMD_EDITOR: Editor to use when editing units; overrides $EDITOR and $VISUAL."
[^reloadcmd]: systemctl(1) `daemon-reload` — "This will rerun all generators (see systemd.generator(7)), reload all unit files, and recreate the entire dependency tree." 경고 문구 "changed on disk. Run 'systemctl daemon-reload' to reload units." 는 실측 출력에서 확인했고 매뉴얼에는 없습니다.
[^revert]: systemctl(1) `revert` — "This command removes drop-in configuration files that modify the specified units, as well as any user-configured unit file that overrides a matching vendor supplied unit file."
[^socket]: systemd.socket(5) — "For each socket unit, a matching service unit must exist, describing the service to start on incoming traffic on the socket". systemd.unit(5) `[Install]` — "Unit files may specify aliases through the Alias= directive in the [Install] section. When the unit is enabled, symlinks will be created for those names, and removed when the unit is disabled."
[^simple]: systemd.service(5) `Type=` — "If set to simple (the default if ExecStart= is specified but neither Type= nor BusName= are, and credentials are not used)". 같은 항목 — "systemctl start command lines for simple services will report success even if the service's binary cannot be invoked successfully". https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html
[^reset]: systemctl(1) `reset-failed` — "Reset the "failed" state of the specified units, or if no unit name is passed, reset the state of all units."
