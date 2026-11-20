---
title: ausearch·audit2why·audit2allow 참조 시트
tags: [linux, command, security, selinux, audit]
status: draft
source:
  - https://github.com/SELinuxProject/selinux/tree/main/policycoreutils
  - https://github.com/linux-audit/audit-userspace
related:
  - ../../kernel/01-03.SELinux.md
  - ./semanage·restorecon·setsebool.md
  - ./getenforce·setenforce·sestatus.md
updated: 2026-11-18
---

# ausearch·audit2why·audit2allow 참조 시트

---

> 감사 로그에서 SELinux 거절(AVC)을 찾는 `ausearch` 와, 그 거절의 원인을 설명하는 `audit2why`, 허용 규칙과 정책 모듈을 만드는 `audit2allow` 입니다.

## 개요

> `ausearch` 로 거절 줄을 찾고, `audit2why` 로 원인을 가르고, 정책을 건드려야 할 때만 `audit2allow` 로 모듈을 만듭니다.

`ausearch` 는 `audit` 패키지, `audit2why`·`audit2allow` 는 `policycoreutils-python-utils` 패키지의 명령입니다. 출력은 Rocky Linux 9.3 컨테이너에서 받았습니다. 이 컨테이너에는 실제 거절 로그가 없어서, 아래 예에 쓴 AVC 줄은 설명을 위해 직접 만든 것입니다. 형식은 감사 로그와 같습니다.[^env]



## 핵심 문법

> 입력은 감사 로그(또는 `-i` 로 준 파일)이고, 정책 파일 경로를 `-p` 로 줘야 `audit2*` 가 동작합니다.

```bash
# 호출 형태
ausearch [options]
audit2why [-p policy] [-i file | -a | -b]
audit2allow [-p policy] [-i file | -a | -b] [-M name]

# 거절 줄만 찾는다 (거절 검색)
ausearch -m avc

# 거절의 원인을 설명한다 (원인 판정)
audit2why -p /etc/selinux/targeted/policy/policy.33 -i 로그파일

# 허용 규칙을 만든다 (규칙 초안)
audit2allow -p /etc/selinux/targeted/policy/policy.33 -i 로그파일
```

### 입력 옵션

```bash
# ausearch
#   -m avc          AVC 메시지만
#   -ts 시각        이 시각 이후
#   -c 이름         이 프로세스 이름(comm) 만
#   -i              숫자를 이름으로 풀어 읽기 쉽게
#   -if 파일        감사 로그 대신 이 파일을 읽는다
# audit2why·audit2allow
#   -i 파일         입력 파일
#   -a              감사 로그 전체
#   -b              마지막 부팅 이후
#   -p 정책파일     정책 파일 경로(필수)
#   -M 이름         정책 모듈 파일(.te·.pp)을 만든다
```



## 종료 코드

> `ausearch` 는 일치하는 줄이 없으면 1 입니다. `-p` 를 빼면 `audit2*` 는 ValueError 와 함께 1 로 끝납니다.

```bash
ausearch -m avc -c nginx -if /tmp/avc.log; echo $?    # <no matches> / 1
audit2allow -i /tmp/avc.log; echo $?                  # ValueError: You must specify the -p option ... / 1
```



## 유스케이스

### 실습 준비

> 아래 블록으로 AVC 줄 하나가 든 입력 파일을 만듭니다. 직접 만든 줄이며 실제 거절 로그가 아닙니다.

```bash
cat > /tmp/avc.log <<'LOG'
type=AVC msg=audit(1700000000.123:100): avc:  denied  { read } for  pid=1234 comm="httpd" name="index.html" dev="sda1" ino=5678 scontext=system_u:system_r:httpd_t:s0 tcontext=unconfined_u:object_r:user_home_t:s0 tclass=file permissive=0
LOG
```

### 거절 줄 찾기

> `ausearch -m avc` 로 거절만 모으고 `-i` 로 시각과 값을 읽기 쉽게 바꿉니다.

```bash
# 실제 서버에서는 -if 없이 감사 로그를 읽는다
#   -m   메시지 종류
#   -i   해석해서 출력
#   -if  입력 파일
ausearch -m avc -i -if /tmp/avc.log
```

```bash
----
type=AVC msg=audit(11/14/23 22:13:20.123:100) : avc:  denied  { read } for  pid=1234 comm=httpd name=index.html dev="sda1" ino=5678 scontext=system_u:system_r:httpd_t:s0 tcontext=unconfined_u:object_r:user_home_t:s0 tclass=file permissive=0 
```

읽는 칸은 동작(`{ read }`), 주체 도메인(`scontext` 의 `httpd_t`), 대상 타입(`tcontext` 의 `user_home_t`), 종류(`tclass=file`)입니다. `permissive=0` 은 enforcing 에서 실제로 거절된 줄이라는 뜻입니다. 이 값은 로그 형식에 대한 설명이고, 이 컨테이너에서 실제 거절을 재현한 것은 아닙니다.

### 시각과 프로세스로 좁히기

> `-ts` 와 `-c` 로 범위를 줄입니다. 일치가 없으면 `<no matches>` 와 종료 코드 1 입니다.

```bash
#   -ts recent   최근 10분
#   -c           프로세스 이름
ausearch -m avc -ts recent -if /tmp/avc.log
ausearch -m avc -c nginx -if /tmp/avc.log
```

```bash
<no matches>
```

### 거절 원인 판정

> `audit2why` 가 거절을 boolean 으로 풀 수 있는지 알려 줍니다.

```bash
audit2why -p /etc/selinux/targeted/policy/policy.33 -i /tmp/avc.log
```

```bash
type=AVC msg=audit(1700000000.123:100): avc:  denied  { read } for  pid=1234 comm="httpd" name="index.html" dev="sda1" ino=5678 scontext=system_u:system_r:httpd_t:s0 tcontext=unconfined_u:object_r:user_home_t:s0 tclass=file permissive=0

	Was caused by:
	The boolean httpd_read_user_content was set incorrectly. 
	Description:
	Allow httpd to read user content

	Allow access by executing:
	# setsebool -P httpd_read_user_content 1
```

이 판정은 정책 안에서 이 거절을 풀 수 있는 boolean 을 찾은 것입니다. 서비스의 의도에 맞는지는 사람이 가려야 합니다. 홈 디렉터리 파일을 웹 서버가 읽어야 하는 것이 맞는지부터 봅니다.

### 허용 규칙과 정책 모듈 만들기

> boolean·라벨·포트로 풀리지 않을 때만 `audit2allow -M` 으로 모듈을 만들고 설치합니다.

```bash
# 허용 규칙을 화면에 본다
audit2allow -p /etc/selinux/targeted/policy/policy.33 -i /tmp/avc.log

# 모듈 파일을 만든다
#   -M   모듈 이름 (webmod.te 와 webmod.pp 가 생긴다)
cd /tmp
audit2allow -p /etc/selinux/targeted/policy/policy.33 -i /tmp/avc.log -M webmod
cat webmod.te
```

```bash
module webmod 1.0;

require {
	type httpd_t;
	type user_home_t;
	class file read;
}

#============= httpd_t ==============
#!!!! This avc can be allowed using the boolean 'httpd_read_user_content'
allow httpd_t user_home_t:file read;
```

`#!!!!` 주석은 이 허용이 boolean 으로도 풀린다는 표시입니다. 이럴 때는 모듈을 설치하지 말고 boolean 을 씁니다. 모듈이 필요하다고 판단했다면 아래처럼 설치하고 지웁니다.

```bash
semodule -i /tmp/webmod.pp
semodule -l | grep webmod    # webmod
semodule -r webmod
```

### 실습 정리

```bash
rm -f /tmp/avc.log /tmp/webmod.te /tmp/webmod.pp
semodule -r webmod 2>/dev/null
```



## 주의사항과 동작 원리

### audit2allow 결과를 그대로 설치하지 않는다

> 만들어진 규칙은 거절을 없애는 가장 짧은 허용이어서, 의도보다 넓은 권한을 영구히 줄 수 있습니다.

```bash
# 설치 전에 .te 를 읽고 허용 대상 타입과 동작이 의도에 맞는지 본다
cat webmod.te
```

`audit2allow` 는 로그에 찍힌 거절만 보고 허용 규칙을 만듭니다. 서비스가 무엇을 해야 하는지는 알지 못합니다.

### 정책 파일 경로가 필요하다

> Rocky Linux 9 에서 `-p` 없이 `audit2why`·`audit2allow` 를 실행하면 ValueError 로 끝납니다.

```bash
audit2allow -i /tmp/avc.log    # ValueError: You must specify the -p option with the path to the policy file.
```

SELinux 가 켜진 시스템에서는 활성 정책을 자동으로 찾는 경우가 있습니다. 이 컨테이너는 SELinux 가 꺼져 있어 경로를 직접 줘야 했습니다. 켜진 시스템에서 `-p` 없이 동작하는지는 실측하지 못했습니다.



## 관련 문서

> 이어서 볼 시트와 개념 문서입니다.

- [SELinux](../../kernel/01-03.SELinux.md) — AVC 를 읽고 고치는 순서
- [semanage·restorecon·setsebool](./semanage%C2%B7restorecon%C2%B7setsebool.md) — boolean·라벨·포트를 고치는 명령
- [getenforce·setenforce·sestatus](./getenforce%C2%B7setenforce%C2%B7sestatus.md) — 모드 확인과 전환



## 참고 자료

> 검증 환경과 근거 자료입니다.

- 검증 환경: macOS 의 OrbStack 위 `rockylinux:9`(Rocky Linux 9.3)입니다.
- 패키지: `audit-3.1.5-9.el9`, `policycoreutils-python-utils-3.6-9.el9`, `selinux-policy-targeted-38.1.86-1.el9` 입니다.
- [audit2allow(1)·ausearch(8)](https://github.com/SELinuxProject/selinux)

[^env]: 컨테이너에서 `ausearch -m avc -i -if /tmp/avc.log` 는 시각을 `11/14/23 22:13:20.123` 로 해석해 찍었고, `-ts recent` 와 `-c nginx` 는 `<no matches>` 와 종료 코드 1 이었습니다. `audit2why` 와 `audit2allow` 의 출력은 위 AVC 줄에서 얻었습니다 (2026-11-18).
