---
title: semanage·restorecon·setsebool 참조 시트
tags: [linux, command, security, selinux]
status: draft
source:
  - https://github.com/SELinuxProject/selinux/tree/main/policycoreutils
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/using_selinux/index
related:
  - ../../kernel/01-03.SELinux.md
  - ./getenforce·setenforce·sestatus.md
  - ./ausearch·audit2why·audit2allow.md
updated: 2026-11-18
---

# semanage·restorecon·setsebool 참조 시트

---

> SELinux 정책의 파일 경로 규칙·포트 규칙·boolean·permissive 도메인을 읽고 바꾸는 `semanage`, 파일 라벨을 규칙에 맞게 되돌리는 `restorecon`, boolean 을 켜고 끄는 `setsebool` 입니다.

## 개요

> 규칙은 `semanage` 로 정책에 더하고, 파일에 적용하는 것은 `restorecon`, 기능 스위치는 `setsebool` 이 맡습니다.

`semanage` 는 `policycoreutils-python-utils`, `restorecon` 과 `setsebool` 은 `policycoreutils`·`libselinux-utils` 패키지의 명령입니다. 출력은 Rocky Linux 9.3 컨테이너에서 받았습니다. 이 컨테이너는 SELinux 가 꺼져 있습니다. 정책 저장소를 읽고 쓰는 `semanage` 와 `setsebool -P` 는 그대로 동작했지만, `restorecon` 은 아무 일도 하지 않고 종료 코드 0 으로 끝나서 실제 라벨 변경은 실측하지 못했습니다.[^env]



## 핵심 문법

> `semanage <대상> <동작>` 꼴이며 대상은 `fcontext`·`port`·`boolean`·`permissive` 등입니다. 동작은 `-a` 추가, `-m` 변경, `-d` 삭제, `-l` 목록입니다.

```bash
# 호출 형태
semanage {fcontext|port|boolean|permissive|login|user|module ...} [options]

# 경로 규칙을 더한다 (경로 규칙 추가)
semanage fcontext -a -t TYPE "경로 정규식"

# 포트를 타입에 묶는다 (포트 규칙 추가)
semanage port -a -t TYPE -p tcp|udp 포트

# 규칙대로 파일 라벨을 되돌린다 (라벨 복원)
restorecon -Rv 경로

# boolean 을 켠다. -P 가 있어야 재부팅 뒤에도 남는다 (boolean 영구 변경)
setsebool -P 이름 on|off
```

### semanage 의 공통 옵션

```bash
# -l   목록
# -C   로컬에서 바꾼 항목만 (-l 과 함께)
# -a   추가
# -m   변경
# -d   삭제
# -t   타입
# -p   프로토콜 (port 대상)
# -n   헤더 없이 출력
# -N   변경 뒤 정책을 다시 올리지 않음
```



## 종료 코드

> 성공은 0, 정책에 없는 이름이나 지울 수 없는 항목은 실패입니다.

```bash
# semanage      정책에 있는 포트 삭제 시도 → 1
# setsebool     정의 안 된 boolean → 255
# restorecon    SELinux 꺼짐일 때 → 0 (아무 일도 하지 않음)

semanage port -d -p tcp 80; echo $?    # ValueError: Port tcp/80 is defined in policy, cannot be deleted / 1
setsebool -P nosuchbool on; echo $?    # Boolean nosuchbool is not defined / 255
```



## 유스케이스

### 정책에 있는 규칙 조회

> 정책 파일만 읽는 목록 명령은 SELinux 를 켜지 않고도 동작합니다.

```bash
# 포트 타입
#   -l   목록
semanage port -l | grep -E "^http_port_t|^ssh_port_t"

# 경로가 가져야 할 라벨을 정책에서 찾는다
matchpathcon /var/www/html/index.html /etc/shadow
```

```bash
http_port_t                    tcp      80, 81, 443, 488, 8008, 8009, 8443, 9000
ssh_port_t                     tcp      22
/var/www/html/index.html	system_u:object_r:httpd_sys_content_t:s0
/etc/shadow	system_u:object_r:shadow_t:s0
```

### 경로 규칙을 더하고 파일에 적용

> 표준이 아닌 디렉터리를 웹 콘텐츠로 라벨링할 규칙을 더한 뒤 `restorecon` 으로 적용합니다.

```bash
# 규칙을 더한다
#   -a   추가
#   -t   타입
semanage fcontext -a -t httpd_sys_content_t "/srv/web(/.*)?"

# 로컬에서 더한 규칙만 본다
#   -l   목록
#   -C   로컬 변경만
semanage fcontext -l -C

# 규칙이 적용되는지 정책에서 확인한다
matchpathcon /srv/web/index.html
```

```bash
SELinux fcontext                                   type               Context

/srv/web(/.*)?                                     all files          system_u:object_r:httpd_sys_content_t:s0 
/srv/web/index.html	system_u:object_r:httpd_sys_content_t:s0
```

```bash
# 파일 라벨을 규칙대로 되돌린다
#   -R   하위까지
#   -v   바뀐 항목을 보인다
restorecon -Rv /srv/web
```

같은 경로에 규칙을 다시 `-a` 로 더하면 오류 없이 "already defined, modifying instead" 를 찍고 기존 규칙을 바꿉니다. `-m` 은 처음부터 변경용입니다.

### 규칙 수정과 삭제

> 잘못 더한 규칙은 `-m` 으로 고치거나 `-d` 로 지웁니다.

```bash
# 타입을 바꾼다
semanage fcontext -m -t httpd_sys_rw_content_t "/srv/web(/.*)?"
semanage fcontext -l -C

# 로컬 규칙을 지운다
semanage fcontext -d "/srv/web(/.*)?"
semanage fcontext -l -C
```

```bash
SELinux fcontext                                   type               Context

/srv/web(/.*)?                                     all files          system_u:object_r:httpd_sys_rw_content_t:s0 
```

삭제 뒤의 `-l -C` 는 아무것도 찍지 않습니다. 이미 파일에 붙은 라벨은 규칙을 지워도 그대로이므로 필요하면 `restorecon` 을 다시 돌립니다.

### 표준이 아닌 포트 허용

> 서비스가 쓰는 포트를 해당 서비스의 포트 타입에 묶습니다.

```bash
# 8888 번 TCP 를 http_port_t 에 묶는다
#   -a   추가
#   -t   타입
#   -p   프로토콜
semanage port -a -t http_port_t -p tcp 8888
semanage port -l -C
```

```bash
SELinux Port Type              Proto    Port Number

http_port_t                    tcp      8888
```

정책이 기본으로 가진 포트(`tcp/80` 등)는 삭제할 수 없고 로컬에서 더한 것만 `-d` 로 지웁니다.

### boolean 켜기

> 정책이 미리 만들어 둔 스위치를 켜서 기능 하나를 허용합니다.

```bash
# -P 를 빼면 재부팅 때 사라진다
setsebool -P httpd_can_network_connect on

# 로컬에서 바꾼 boolean 만 본다
semanage boolean -l -C
```

```bash
SELinux boolean                State  Default Description

httpd_can_network_connect      (on   ,   on)  Allow httpd to can network connect
```

목록의 두 값은 현재 상태와 기본 상태입니다. 이 컨테이너에서 `getsebool httpd_can_network_connect` 는 `SELinux is disabled` 로 실패했으므로 켜진 상태에서 `getsebool` 이 찍는 값은 실측하지 못했습니다.

### 도메인 하나만 permissive 로

> 새 서비스의 거절을 모을 때 전체를 끄지 않고 도메인 하나만 허락·감사 상태로 둡니다.

```bash
# 추가
semanage permissive -a httpd_t
semanage permissive -l

# 되돌린다
semanage permissive -d httpd_t
```

```bash
Customized Permissive Types

httpd_t
```

`-d` 는 `semanage permissive -l` 의 "Customized Permissive Types" 에 있는 도메인만 지웁니다. 없는 도메인은 `FileNotFoundError` 로 종료 코드 1 이 됩니다.[^perm]

### 실습 정리

```bash
# 이 시트에서 더한 로컬 변경을 되돌린다
semanage fcontext -d "/srv/web(/.*)?"
semanage port -d -t http_port_t -p tcp 8888
setsebool -P httpd_can_network_connect off
```



## 주의사항과 동작 원리

### restorecon 은 규칙이 있어야 되돌린다

> `restorecon` 은 정책의 경로 규칙대로 라벨을 맞추므로, 규칙을 먼저 더하지 않으면 원하는 타입이 되지 않습니다.

```bash
# restorecon 은 정책의 경로 규칙에 적힌 타입으로만 맞춘다
# 원하는 타입이 규칙에 없으면 semanage fcontext 로 먼저 더한다
```

restorecon(8) 은 라벨이 이미 있는 파일의 타입 칸만 고치고, 사용자·역할·레벨까지 맞추려면 `-F` 를 쓰라고 합니다.[^rc]

### 로컬 규칙이 정책 모듈 규칙보다 먼저

`semanage fcontext` 로 더한 규칙은 `file_contexts.local` 에 저장되고, 정책 모듈의 규칙보다 우선합니다. 로컬 규칙은 가장 최근 것부터 훑어 처음 맞는 것을 씁니다. 가장 구체적인 것이 아니라 처음 맞는 것이므로 정규식을 최대한 좁게 씁니다.[^fc]



## 관련 문서

> 이어서 볼 시트와 개념 문서입니다.

- [SELinux](../../kernel/01-03.SELinux.md) — 라벨이 저장되는 곳과 거절을 고치는 순서
- [getenforce·setenforce·sestatus](./getenforce%C2%B7setenforce%C2%B7sestatus.md) — 모드 확인과 전환
- [ausearch·audit2why·audit2allow](./ausearch%C2%B7audit2why%C2%B7audit2allow.md) — 거절을 읽는 명령



## 참고 자료

> 검증 환경과 근거 자료입니다.

- 검증 환경: macOS 의 OrbStack 위 `rockylinux:9`(Rocky Linux 9.3), `policycoreutils-python-utils-3.6-9.el9`, `selinux-policy-targeted-38.1.86-1.el9`
- [semanage-fcontext(8)·semanage-permissive(8)·restorecon(8)](https://github.com/SELinuxProject/selinux)

[^env]: 컨테이너에서 `restorecon -nv /tmp/f`, `restorecon -Rv /nonexistent`, `restorecon -v /tmp/f` 는 모두 출력 없이 종료 코드 0 이었습니다. `getsebool` 은 `getsebool:  SELinux is disabled` 와 종료 코드 1 이었습니다 (2026-11-18).
[^perm]: semanage-permissive(8): "this command can make any domain permissive, but can only remove the permissive property from domains where it was added by semanage permissive ("semanage permissive -d" can only be used on types listed as "Customized Permissive Types" by "semanage permissive -l")." Rocky Linux 9.3 컨테이너의 `man semanage-permissive` (2026-11-18)
[^rc]: restorecon(8): "If a file object has a context, restorecon will only modify the type portion of the security context. The -F option will force a replacement of the entire context." Rocky Linux 9.3 컨테이너의 `man restorecon` (2026-11-18)
[^fc]: semanage-fcontext(8): "file context definitions specified using 'semanage fcontext' (i.e. local file context modifications stored in file_contexts.local) have higher priority than those specified in policy modules. ... Entries in file_contexts.local are processed from most recent one to the oldest, with first match being used (as opposed to the most specific match, which is used when matching other file context definitions)." Rocky Linux 9.3 컨테이너의 `man semanage-fcontext` (2026-11-18)
