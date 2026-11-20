---
title: getenforce·setenforce·sestatus 참조 시트
tags: [linux, command, security, selinux]
status: draft
source:
  - https://github.com/SELinuxProject/selinux/tree/main/policycoreutils
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/using_selinux/changing-selinux-states-and-modes_using-selinux
related:
  - ../../kernel/01-03.SELinux.md
  - ./semanage·restorecon·setsebool.md
  - ./ausearch·audit2why·audit2allow.md
updated: 2026-11-18
---

# getenforce·setenforce·sestatus 참조 시트

---

> SELinux 가 지금 켜져 있는지와 enforcing·permissive 어느 모드인지 읽고, 실행 중에 두 모드를 오가는 명령입니다.

## 개요

> `getenforce` 는 모드 한 단어를, `sestatus` 는 설정 파일과 현재 상태의 요약을, `setenforce` 는 모드 전환을 맡습니다.

세 명령은 RHEL 계열의 외부 바이너리입니다. `getenforce`·`setenforce` 는 `libselinux-utils`, `sestatus` 는 `policycoreutils` 패키지에 들어 있습니다. 출력은 Rocky Linux 9.3 컨테이너에서 받았습니다. 이 컨테이너에서는 SELinux 가 꺼져 있어서 `Disabled` 일 때의 출력만 실측했습니다. enforcing·permissive 일 때의 출력은 실측하지 못했습니다.[^env]



## 핵심 문법

> 읽기 명령은 인자가 없고, 전환 명령은 모드 하나를 인자로 받습니다.

```bash
# 현재 모드를 한 단어로 읽는다 (모드 확인)
getenforce

# 켜져 있는지만 종료 코드로 알려 준다. 출력은 없다 (스크립트 분기)
selinuxenabled

# 현재 상태와 설정 파일 값을 요약한다 (상태 확인)
sestatus

# 모드를 바꾼다. Enforcing·Permissive 또는 1·0 (모드 전환)
setenforce Enforcing|Permissive|1|0
```

### 모드 이름

```bash
# getenforce 가 찍는 값
# Enforcing    정책을 집행한다
# Permissive   집행하지 않고 거절했을 일을 감사 로그에 남긴다
# Disabled     SELinux 가 꺼져 있다
```



## 종료 코드

> `selinuxenabled` 는 켜져 있으면 0, 꺼져 있으면 1 입니다. `setenforce` 는 SELinux 가 꺼져 있으면 1 로 끝납니다.

```bash
# getenforce      → 0 (Disabled 일 때도 0)
# sestatus        → 0
# selinuxenabled  → 켜짐 0 / 꺼짐 1
# setenforce      → SELinux 꺼짐 1

getenforce; echo $?        # Disabled / 0
selinuxenabled; echo $?    # 1
setenforce 1; echo $?      # setenforce: SELinux is disabled / 1
```



## 유스케이스

### 지금 모드와 설정 파일 값 비교

> 재부팅 뒤에 적용될 값(설정 파일)과 지금 값을 한 번에 봅니다.

```bash
sestatus
cat /etc/selinux/config | grep -v "^#" | grep .
```

```bash
SELinux status:                 disabled
SELINUX=enforcing
SELINUXTYPE=targeted
```

설정 파일은 `enforcing` 인데 현재 상태가 `disabled` 이면 설정이 아직 적용되지 않았거나, 커널 인자 `selinux=0` 으로 부팅되었다는 뜻입니다.[^cfg]

### 문제를 가르려고 잠깐 permissive 로

> `setenforce 0` 으로 enforcing 을 permissive 로 내려서 거절이 SELinux 때문인지 가릅니다.

```bash
# 임시로 permissive (재부팅하면 설정 파일 값으로 돌아간다)
setenforce 0

# 다시 집행
setenforce 1
```

permissive 로 바꾸고 같은 동작이 되면 SELinux 거절이 원인입니다. 거절이 permissive 에서도 남으면 다른 원인입니다. 다만 permissive 는 enforcing 일 때와 거절 집합이 다를 수 있어서, 원인 확인용이지 해법이 아닙니다.



## 주의사항과 동작 원리

### disabled 는 setenforce 로 못 바꾼다

> `setenforce` 는 enforcing 과 permissive 만 바꾸고, 켜고 끄는 일은 설정 파일과 재부팅의 몫입니다.

```bash
setenforce 0    # setenforce: SELinux is disabled
```

setenforce(8) 은 SELinux 를 켜거나 끄려면 selinux(8) 을 보라고 안내합니다.[^set]

### 영구 변경은 설정 파일

```bash
# /etc/selinux/config 의 값을 바꾸고 재부팅해야 영구히 바뀐다
# SELINUX=enforcing | permissive | disabled
```

`SELINUX=disabled` 로 끄는 방식은 더는 권장하지 않고 부팅 인자 `selinux=0` 을 쓰라고 selinux(8) 은 적습니다.[^cfg]



## 관련 문서

> 이어서 볼 시트와 개념 문서입니다.

- [SELinux](../../kernel/01-03.SELinux.md) — 모드와 라벨, DAC 다음에 MAC 이 검사되는 순서
- [semanage·restorecon·setsebool](./semanage%C2%B7restorecon%C2%B7setsebool.md) — 라벨과 boolean 을 고치는 명령
- [ausearch·audit2why·audit2allow](./ausearch%C2%B7audit2why%C2%B7audit2allow.md) — 거절을 읽는 명령



## 참고 자료

> 검증 환경과 근거 자료입니다.

- 검증 환경: macOS 의 OrbStack 위 `rockylinux:9`(Rocky Linux 9.3), `libselinux-utils-3.6-4.el9`, `policycoreutils-3.6-9.el9`
- [selinux(8)·setenforce(8)·selinux_config(5)](https://github.com/SELinuxProject/selinux)

[^env]: 컨테이너의 `getenforce` 는 `Disabled`, `sestatus` 는 `SELinux status: disabled` 를 찍었고 `selinuxenabled` 는 종료 코드 1 이었습니다 (2026-11-18).
[^cfg]: selinux_config(5): "disabled — No SELinux policy is loaded. This option was used to disable SELinux completely, which is now deprecated. Use the selinux=0 kernel boot option instead (see selinux(8))." Rocky Linux 9.3 컨테이너의 `man selinux_config` (2026-11-18)
[^set]: setenforce(8): "Use Enforcing or 1 to put SELinux in enforcing mode. Use Permissive or 0 to put SELinux in permissive mode. If SELinux is disabled and you want to enable it, or SELinux is enabled and you want to disable it, please see selinux(8)." Rocky Linux 9.3 컨테이너의 `man setenforce` (2026-11-18)
