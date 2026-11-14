---
title: journalctl 저장 공간과 읽기 권한
tags: [linux, cheatsheet, journalctl, systemd, journal, storage, vacuum, permission, reference]
status: draft
source:
  - systemd 259 journalctl(1)·journald.conf(5) (OrbStack Ubuntu 26.04 VM 의 `man journalctl`·`journalctl --help` 원문, freedesktop.org journalctl(1))
related:
  - ./journalctl.md
  - ./journalctl%20출력%20모양과%20jq.md
  - ./systemctl.md
  - ../README.md
  - ../../../book/learning-modern-linux/08-01.재는%20것은%20바깥이고%20알고%20싶은%20것은%20안이다.md
updated: 2026-11-14
---

# journalctl 저장 공간과 읽기 권한

---

> 저널의 크기와 저장 위치를 확인하고 복사본에서 정리하며, 일반 사용자의 읽기 권한과 사용자 저널을 `journalctl` 로 확인하는 예제를 따라 치면 그대로 나오게 모았습니다.

## 개요

> 이 시트는 `journalctl` 중 저장 공간 확인, 복사본 정리, 읽기 권한을 다룹니다.

[journalctl 참조 시트](./journalctl.md)에서 저널을 읽는 유스케이스를 뺀 나머지입니다. 예는 그 시트의 「실습 준비」 블록을 돌린 상태에서 이어지고, 출력은 같은 OrbStack Ubuntu 26.04 VM(systemd 259.9)에서 root 셸로 받았습니다.



## 핵심 문법

> 크기는 `--disk-usage` 로 보고, 정리는 `-D` 로 고른 디렉터리에 `--vacuum-*` 로 하고, 읽기 범위는 `--user` 와 그룹이 정합니다.

```bash
# 호출 형태
# journalctl --help 의 첫 줄
journalctl [OPTIONS...] [MATCHES...]

# 저널의 크기를 본다 (저장 공간과 저장 위치)
journalctl --disk-usage

# 복사본의 저널을 줄인다 (저널 정리하기)
journalctl -D 디렉터리 --vacuum-size=크기

# 사용자 저널을 읽는다 (읽기 권한과 사용자 저널)
journalctl --user
```



## 종료 코드

> 성공이면 0, 실패면 0 이 아닌 값이며 매뉴얼은 그 이상을 적지 않습니다.[^exit]

아래 값은 실측이고 읽을 수 있는 저널 파일이 없을 때의 1 만 싣습니다.

```bash
# 0  성공
# 1  실패
#    열 수 있는 저널 파일이 없다 (권한 부족)
sudo -u appuser journalctl -u lab-backup -o cat; echo $?
# No journal files were opened due to insufficient permissions. / 1
```

위 예는 「실습 준비」 의 `appuser` 를 만든 뒤 「읽기 권한과 사용자 저널」 에서 돌립니다.



## 유스케이스

> 예는 앞 예가 만든 상태를 이어 쓰므로 위에서 아래로 차례로 돌립니다.

### 실습 준비

> 원래 시트의 「실습 준비」 를 돌린 상태에서 권한 시험용 사용자를 하나 더 만듭니다.

```bash
# appuser: 권한 시험용 일반 사용자 (읽기 권한과 사용자 저널)
#   저널이 사용자 저널 파일 이름에 UID 를 쓰므로 UID 를 정해 둔다
export SYSTEMD_PAGER=
useradd -m -u 2001 -s /bin/bash appuser
```

### 저장 공간과 저장 위치

> `--disk-usage` 는 저널 파일 전체의 크기를 보이고, 저장 위치는 journald.conf 의 `Storage=` 설정이 정합니다.[^storage]

```bash
# 보관된 파일과 쓰는 중인 파일을 합친 크기를 낸다. 값은 쌓인 저널만큼 다르다
#   --disk-usage   저널 파일 전체의 디스크 사용량
journalctl --disk-usage
# Archived and active journals take up 24M in the file system.
```

```bash
# Storage= 의 값 (journald.conf)
#   volatile    메모리(/run/log/journal)에만 둔다
#   persistent  디스크(/var/log/journal)에 두고 안 되면 /run 으로 물러난다
#   auto        /var/log/journal 디렉터리가 있으면 persistent, 없으면 volatile
#   none        저장하지 않는다
# 기본값은 persistent 다 (컴파일 때 정해지는 값)

# 두 디렉터리가 모두 있다
ls -d /var/log/journal /run/log/journal
```

```bash
/run/log/journal
/var/log/journal
```

```bash
# 적용 중인 설정에서 주석과 빈 줄을 뺀다. 첫 [Journal] 은 본 파일이고
# 둘째는 /usr/lib/systemd/journald.conf.d/syslog.conf drop-in 이다
systemd-analyze cat-config systemd/journald.conf \
  | grep -vE '^(#|$)'
```

```bash
[Journal]
[Journal]
ForwardToSyslog=yes
```

```bash
# 쓰는 중인 파일이 어디에 있는지 본다. 머신 ID 디렉터리 이름은 가렸다
find /var/log/journal /run/log/journal -name system.journal \
  | sed -E 's#/[0-9a-f]{32}/#/<machine-id>/#'
# /var/log/journal/<machine-id>/system.journal
```

`Storage=` 는 본 파일에서 주석이라 기본값 persistent 가 쓰입니다. 쓰는 중인 파일도 `/var/log/journal` 아래에 있어 이 VM 은 디스크에 남기는 영속 저널입니다.

### 저널 정리하기

> `--vacuum-*` 는 보관된 파일만 지우므로 실제 저널이 아니라 복사본에 `-D` 로 돌립니다.[^vacuum]

복사본에는 보관된 파일을 흉내 낸 사본 셋을 더합니다. 쓰는 중인 `system.journal` 하나만 있으면 지울 것이 없기 때문입니다.

```bash
# 복사본을 만드는 함수. 이후 예마다 다시 부른다
lab_jcopy() {
  rm -rf /tmp/lab-jcopy && mkdir /tmp/lab-jcopy
  src=$(find /var/log/journal -name system.journal)
  cp "$src" /tmp/lab-jcopy/system.journal
  # 보관 파일 이름을 흉내 낸다. %032d 는 32자리를 0 으로 채운 숫자다
  for n in 1 2 3; do
    printf -v f 'system@%032d-%016d-%016d.journal' "$n" "$n" "$n"
    cp "$src" "/tmp/lab-jcopy/$f"
  done
}

# 복사본을 만들고 크기를 잰다. 16M 짜리 파일 넷이다
#   -D   이 디렉터리의 저널 파일을 읽고 정리한다 (--directory)
lab_jcopy
ls /tmp/lab-jcopy
journalctl -D /tmp/lab-jcopy --disk-usage
```

```bash
system.journal
system@00000000000000000000000000000001-0000000000000001-0000000000000001.journal
system@00000000000000000000000000000002-0000000000000002-0000000000000002.journal
system@00000000000000000000000000000003-0000000000000003-0000000000000003.journal
Archived and active journals take up 64M in the file system.
```

```bash
# 40M 아래가 될 때까지 가장 오래된 보관 파일부터 지운다
#   --vacuum-size   저널 전체 크기를 이 값 아래로 줄인다
journalctl -D /tmp/lab-jcopy --vacuum-size=40M
ls /tmp/lab-jcopy
```

```bash
Deleted archived journal /tmp/lab-jcopy/system@00000000000000000000000000000001-0000000000000001-0000000000000001.journal (16M).
Deleted archived journal /tmp/lab-jcopy/system@00000000000000000000000000000002-0000000000000002-0000000000000002.journal (16M).
Vacuuming done, freed 32M of archived journals from /tmp/lab-jcopy.
system.journal
system@00000000000000000000000000000003-0000000000000003-0000000000000003.journal
```

```bash
# 파일 수를 2개로 줄인다. 쓰는 중인 파일도 센다
#   --vacuum-files   저널 파일 수를 이 값 이하로 줄인다
lab_jcopy
journalctl -D /tmp/lab-jcopy --vacuum-files=2
```

```bash
Deleted archived journal /tmp/lab-jcopy/system@00000000000000000000000000000001-0000000000000001-0000000000000001.journal (16M).
Deleted archived journal /tmp/lab-jcopy/system@00000000000000000000000000000002-0000000000000002-0000000000000002.journal (16M).
Vacuuming done, freed 32M of archived journals from /tmp/lab-jcopy.
```

```bash
# 1초보다 오래된 보관 파일을 모두 지운다. 사본 이름이 아주 옛 시각이라 셋 다 걸린다
#   --vacuum-time   이 기간보다 오래된 보관 파일을 지운다
lab_jcopy
journalctl -D /tmp/lab-jcopy --vacuum-time=1s
ls /tmp/lab-jcopy
```

```bash
Deleted archived journal /tmp/lab-jcopy/system@00000000000000000000000000000001-0000000000000001-0000000000000001.journal (16M).
Deleted archived journal /tmp/lab-jcopy/system@00000000000000000000000000000002-0000000000000002-0000000000000002.journal (16M).
Deleted archived journal /tmp/lab-jcopy/system@00000000000000000000000000000003-0000000000000003-0000000000000003.journal (16M).
Vacuuming done, freed 48M of archived journals from /tmp/lab-jcopy.
system.journal
```

```bash
# 쓰는 중인 파일만 남은 디렉터리에는 1M 으로 줄이라 해도 지울 것이 없다
journalctl -D /tmp/lab-jcopy --vacuum-size=1M
# Vacuuming done, freed 0B of archived journals from /tmp/lab-jcopy.

# 복사본도 일반 저널처럼 읽힌다
journalctl \
  -D /tmp/lab-jcopy \
  -t lab-web \
  -o cat
```

```bash
lab-web: cache miss rate high
lab-web: request served
```

아래 셋은 돌아가는 journald 에 요청을 보내 실제 저널을 바꾸므로 이 시트에서는 돌리지 않았습니다. 뜻은 `journalctl --help` 원문을 옮겼습니다.

```bash
# journald 에 요청을 보내는 명령
#   --rotate           저널 파일을 바로 교체(rotate)하라고 요청한다
#   --flush            /run 의 저널을 모두 /var 로 옮긴다
#   --relinquish-var   디스크 기록을 멈추고 임시 파일 시스템(/run)에 기록한다
journalctl --rotate
journalctl --flush
journalctl --relinquish-var
```

### 읽기 권한과 사용자 저널

> 일반 사용자는 자기 사용자 저널만 읽고 시스템 저널은 `adm`·`systemd-journal` 그룹 구성원이어야 읽습니다.[^groups]

```bash
# 그룹이 없는 일반 사용자로 시스템 저널을 읽는다. 열 수 있는 저널 파일이 없다
#   sudo -u   다른 사용자로 명령을 돌린다
sudo -u appuser journalctl -u lab-backup -o cat; echo $?
# No journal files were opened due to insufficient permissions. / 1
```

```bash
# -n 1 로 부르면 그룹 안내가 붙는다. -q 로 끌 수 있다
sudo -u appuser journalctl -n 1
```

```bash
Hint: You are currently not seeing messages from other users and the system.
      Users in groups 'adm', 'systemd-journal' can see all messages.
      Pass -q to turn off this notice.
No journal files were opened due to insufficient permissions.
```

```bash
# 사용자 매니저를 띄워 그 사용자의 유닛을 하나 돌린다
#   loginctl enable-linger   로그인하지 않아도 그 사용자의 매니저를 띄워 둔다
#   systemd-run --user -M    그 사용자 매니저(appuser@)에서 유닛을 돌린다
loginctl enable-linger appuser
sleep 3
systemd-run \
  --user \
  -M appuser@ \
  --unit=lab-ujob \
  --description="lab user job" \
  --quiet \
  --wait \
  --collect \
  -p Type=oneshot \
  /bin/echo "lab-ujob: hello from user manager"
```

```bash
# 사용자 저널은 그룹 없이도 읽힌다
#   --user   현재 사용자의 저널을 읽는다
sudo -u appuser journalctl \
  --user \
  -u lab-ujob \
  -o cat
```

```bash
Starting lab-ujob.service - lab user job...
lab-ujob: hello from user manager
Finished lab-ujob.service - lab user job.
```

```bash
# systemd-journal 그룹에 넣으면 시스템 저널이 읽힌다
usermod -aG systemd-journal appuser
sudo -u appuser journalctl -u lab-backup -o cat
```

```bash
Starting lab-backup.service - lab backup job...
lab-backup: copying 3 files
lab-backup: done
lab-backup.service: Deactivated successfully.
Finished lab-backup.service - lab backup job.
```

```bash
# 두 그룹의 이름과 GID 를 본다
getent group adm systemd-journal | cut -d: -f1,3
# adm:4
# systemd-journal:999
```

### 실습 정리

> 「주의사항과 동작 원리」 의 예까지 돌린 뒤 아래 블록으로 시험용 사용자와 복사본을 지웁니다.

저널에 남은 줄과 사용자 저널 파일(`user-2001.journal`)은 지우지 않습니다. 저널을 줄이는 일은 복사본에서만 했기 때문입니다.

```bash
# 사용자 매니저를 내리고 사용자를 지운다
loginctl disable-linger appuser
loginctl terminate-user appuser
sleep 2
userdel -r appuser
# userdel: appuser mail spool (/var/mail/appuser) not found

# 복사본을 지운다
rm -rf /tmp/lab-jcopy
```



## 주의사항과 동작 원리

### 사용자 저널만 열린 빈 결과

> 사용자 저널이 생긴 일반 사용자는 시스템 저널을 못 열어도 오류가 나지 않고 빈 결과를 받습니다.

```bash
# 「실습 정리」 전에 돌린다. 앞의 그룹을 빼고 다시 읽는다
# appuser 의 사용자 저널은 열리므로 오류가 없다
gpasswd -d appuser systemd-journal
# Removing user appuser from group systemd-journal
sudo -u appuser journalctl -u lab-backup -o cat; echo $?    # 0
```

그룹이 없는 사용자가 사용자 저널 없이 부르면 「읽기 권한과 사용자 저널」 처럼 오류가 나므로, 같은 명령이 사용자마다 다르게 끝납니다.[^groups]



## 관련 문서

> 이 시트의 예와 이어지는 시트와 책 노트입니다.

- [journalctl 참조 시트](./journalctl.md) — 저널을 읽는 유스케이스와 「실습 준비」
- [journalctl 출력 모양과 jq](./journalctl%20출력%20모양과%20jq.md) — 출력 모양 바꾸기와 `jq` 와 잇기
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [systemctl 참조 시트](./systemctl.md) — 유닛 상태와 `status` 의 꼬리 로그
- [책 노트 8장 4절, 로그가 디스크를 먹지 않게 한다](../../../book/learning-modern-linux/08-01.재는%20것은%20바깥이고%20알고%20싶은%20것은%20안이다.md#4-로그가-디스크를-먹지-않게-한다) — 저널 크기 한도와 정리의 배경



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- 검증 환경: OrbStack Ubuntu 26.04 VM, systemd 259.9 (`259.9-0ubuntu0.1`) — 2026-11-14 실측, `journalctl --help`·`man journalctl` 원문 대조
- [journalctl(1)](https://www.freedesktop.org/software/systemd/man/latest/journalctl.html) · [journald.conf(5)](https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html)

[^exit]: journalctl(1) EXIT STATUS — "On success, 0 is returned; otherwise, a non-zero failure code is returned." 이 절의 0 과 1 은 `명령; echo $?` 로 읽은 실측입니다. https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
[^storage]: journalctl(1) `--disk-usage` — "Shows the current disk usage of all journal files." journald.conf(5) `Storage=` — ""auto" behaves like "persistent" if the /var/log/journal directory exists, and "volatile" otherwise" "Defaults to "persistent" in the default journal namespace (this value is determined at compilation time)" https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html
[^vacuum]: journalctl(1) `--vacuum-size=` — "removes the oldest archived journal files until the disk space they use falls below the specified size." `--vacuum-time=` — "removes archived journal files older than the specified timespan." `-D` — "Takes a directory path as argument." https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
[^groups]: journalctl(1) DESCRIPTION — "All users are granted access to their private per-user journals. However, by default, only root and users who are members of a few special groups are granted access to the system journal and the journals of other users. Members of the groups "systemd-journal", "adm", and "wheel" can read all journal files." https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
