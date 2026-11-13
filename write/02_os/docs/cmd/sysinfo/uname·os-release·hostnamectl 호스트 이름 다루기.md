---
title: hostnamectl·hostname 호스트 이름 다루기
tags: [linux, cheatsheet, hostnamectl, hostname, systemd, sysinfo, cli, reference]
status: draft
source:
  - systemd 252 hostnamectl(1)·hostname(5)·machine-info(5) (bookworm), OrbStack VM 의 systemd 259.9 `man hostnamectl`
  - hostname 3.23 hostname(1), gethostname(2)·proc(5) (bookworm)
related:
  - ./uname·os-release·hostnamectl.md
  - ../README.md
updated: 2026-11-13
---

# hostnamectl·hostname 호스트 이름 다루기

---

> 호스트 이름을 `hostnamectl`·`hostname` 으로 읽고 바꾸는 방법을, VM 에서 실제로 돌려 본 출력과 함께 모았습니다.

## 개요

> `hostnamectl` 은 호스트 이름 세 종류를 한 도구로 보고 바꾸고, `hostname` 은 커널의 이름 하나만 다룹니다.

이 시트는 [uname·os-release·lsb_release 참조 시트](./uname·os-release·hostnamectl.md)에서 호스트 이름을 읽고 바꾸는 유스케이스를 떼어 낸 것입니다. 원래 시트의 「실습 준비」 없이 돌아가고, 출력은 OrbStack VM `ubuntu`(systemd 259.9, hostname 3.25)에서 받았습니다.

`hostnamectl` 은 systemd 가 도는 서버에서 쓰고, `hostname` 은 hostname 패키지의 명령입니다. 이름을 바꾸는 예는 VM 의 호스트 이름을 실제로 바꾸므로, 따라 할 때도 「실습 정리」 까지 이어서 실행합니다.



## 핵심 문법

> `hostnamectl` 은 명령을 고르고 옵션으로 이름 종류를 고르며, `hostname` 은 인자가 있으면 바꾸고 없으면 읽습니다.

```bash
# 호출 형태. hostnamectl (hostnamectl --help 의 첫 줄)
hostnamectl [OPTIONS...] COMMAND ...

# 호출 형태. hostname (hostname --help 의 첫 세 줄)
hostname [-b] {hostname|-F file}
hostname [-a|-A|-d|-f|-i|-I|-s|-y]
hostname

# 호스트 이름 세 종류 (hostnamectl 의 이름 종류를 고르는 옵션이 같은 이름이다)
#   pretty      특수 문자가 들어가도 되는 사람용 이름. /etc/machine-info 에 저장된다
#   static      관리자가 정한 이름. /etc/hostname 에 저장된다
#   transient   네트워크 설정에서 받는 대체값. static 이 유효하면 쓰이지 않는다
# static 과 transient 는 DNS 이름 규칙(레이블 하나, 또는 점으로 이은 FQDN)을 따르고 64자까지다

# 상태를 읽는다 (상태 읽기)
hostnamectl
hostnamectl status

# 이름 하나만 꺼낸다 (이름 하나만 꺼내기)
hostnamectl hostname
hostnamectl --static
hostnamectl --transient
hostnamectl --pretty

# 커널의 이름을 읽는다 (hostname 명령과 이름이 저장된 곳)
hostname
hostname -s
hostname -f
hostname -d

# 이름을 바꾼다 (이름 바꾸기)
sudo hostnamectl hostname NAME
sudo hostnamectl --pretty hostname NAME
sudo hostnamectl --transient hostname NAME
sudo hostname NAME

# 이름 말고 다른 항목과 JSON 출력 (그 밖의 항목과 JSON 출력)
hostnamectl chassis
hostnamectl icon-name
hostnamectl --json=pretty

# 배포판과 커널 줄만 고른다 (hostnamectl 로 배포판과 커널 줄 고르기)
hostnamectl | grep -E "Operating System|Kernel"
```

`hostnamectl` 의 이름 종류는 위 주석의 세 가지이고 상세한 규칙은 man 에 있습니다.[^hctl]



## 종료 코드

> `hostnamectl` 이 이 VM 에서 낸 실패 코드는 모두 1 이었습니다.

man 은 성공하면 0 이고 실패하면 0 이 아닌 값이라고만 적고, 어떤 실패가 몇 번인지는 적지 않아 실측한 값만 싣습니다.[^hctl-exit]

```bash
# hostnamectl
# 0  성공
# 1  모르는 옵션, 모르는 명령, 권한이 없어 이름을 못 바꿀 때

# 이름을 읽으면 0 으로 끝난다
hostnamectl hostname; echo $?    # ubuntu / 0

# 모르는 옵션과 모르는 명령은 오류를 내고 1 로 끝난다
hostnamectl --bad 2>&1; echo $?    # hostnamectl: unrecognized option '--bad' / 1
hostnamectl nosuch 2>&1; echo $?    # Unknown command verb 'nosuch'. / 1
```

```bash
# 이름 바꾸기는 권한이 필요하다. sudo 없이 시도하면 실패한다
#   --no-ask-password   권한이 없을 때 인증을 묻지 않고 곧바로 실패한다
hostnamectl --no-ask-password hostname labhost    # Could not set static hostname: Access denied

# 오류 메시지를 버리고 종료 코드만 본다. 실패라 1 이다
hostnamectl --no-ask-password hostname labhost 2>/dev/null; echo $?    # 1
```

위 블록들의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 이름을 바꾸는 예는 「실습 정리」 에서 되돌립니다.

### 실습 준비

> 이 시트는 따로 만드는 것이 없고, 원래 시트의 컨테이너 대신 OrbStack VM 을 씁니다.

예는 OrbStack VM `ubuntu` 에서 `sudo` 가 되는 일반 사용자로 실행했고, macOS 호스트에서는 `orb -m ubuntu 명령` 으로 같은 일을 합니다. 다른 창이 같은 VM 을 읽을 수 있으므로 「이름 바꾸기」 부터 「실습 정리」 까지는 한 번에 이어서 실행합니다.

### 상태 읽기

> 명령 없이 부르면 호스트 이름과 시스템 정보를 한 화면에 보입니다.

`status` 는 명령을 생략했을 때의 기본값이라 붙이든 안 붙이든 출력이 같습니다.[^hctl] 처음 두 줄은 이 VM 에서 제품 UUID 와 하드웨어 일련번호를 읽을 권한이 없어서 나오는 경고입니다. `hostnamectl` 은 이 줄을 stderr 로 찍고 계속 진행하므로, 상태 전체를 찍는 이후 예에서는 `2>/dev/null` 로 가립니다.

```bash
# 호스트 이름과 시스템 정보를 한 화면에. Machine ID 와 Boot ID 두 줄은 식별값이라 뺐다
#   grep -v   패턴에 맞는 줄을 뺀다 (--invert-match)
#   grep -E   패턴을 확장 정규식으로 읽는다 (--extended-regexp)
hostnamectl 2>&1 | grep -vE '(Machine|Boot) ID'
```

```bash
Failed to query product UUID, ignoring: Access denied
Failed to query hardware serial, ignoring: Access denied
 Static hostname: ubuntu
       Icon name: computer-container
         Chassis: container ☐
  Virtualization: lxc
Operating System: Ubuntu 26.04.1 LTS
          Kernel: Linux 7.2.12-orbstack-00394-gbecdd6130068
    Architecture: arm64
```

```bash
# status 를 붙여도 출력이 같다. diff 는 두 출력이 같으면 0 으로 끝난다
diff <(hostnamectl 2>&1) <(hostnamectl status 2>&1) && echo "status 를 붙여도 같다"    # status 를 붙여도 같다
```

### 이름 하나만 꺼내기

> 이름 종류마다 옵션이나 명령으로 값 하나만 찍습니다.

```bash
# 시스템 호스트 이름 하나만. hostname 명령에 이름을 안 주면 읽는다
hostnamectl hostname    # ubuntu

# 관리자가 정한 이름
#   --static   static 이름만 고른다
hostnamectl --static    # ubuntu

# static 이 있으면 지금 쓰는 이름
#   --transient   transient 이름만 고른다
hostnamectl --transient    # ubuntu

# 설정하지 않았으면 빈 줄이라 대괄호로 빈 값을 보인다
#   --pretty   pretty 이름만 고른다
echo "[$(hostnamectl --pretty)]"    # []
```

### hostname 명령과 이름이 저장된 곳

> 시스템 호스트 이름은 `hostname`·`/etc/hostname`·`/proc/sys/kernel/hostname`·`uname -n` 네 곳에서 보입니다.

`hostname` 명령은 `gethostname(2)` 가 돌려주는 시스템 이름을 찍습니다.[^hname] 커널이 들고 있는 그 이름이 `/proc/sys/kernel/hostname` 이고 `uname -n` 의 `nodename` 칸과 같습니다.[^proc][^uname2] `/etc/hostname` 은 static 이름을 담은 파일이고, systemd 가 부팅 때 이 값을 `sethostname(2)` 로 커널에 넣습니다.[^hostname5]

```bash
# 시스템 호스트 이름
hostname    # ubuntu

# static 이름 파일: 부팅 때 커널에 들어가는 값
cat /etc/hostname    # ubuntu

# 커널의 호스트 이름
cat /proc/sys/kernel/hostname    # ubuntu

# uname 의 nodename 칸도 같은 이름
uname -n    # ubuntu
```

`hostname` 명령의 `-s`·`-f`·`-d` 도 이 이름에서 파생됩니다. 점이 없는 이름이라 `-s` 와 `-f` 는 같고 `-d` 는 빈 줄이며, man 은 `-f`·`-d`·`-i` 가 네트워크 설정에 따라 결과가 달라지니 피하라고 권합니다.[^hname]

```bash
# 짧은 이름, FQDN, 도메인 부분을 따로 묻는다
#   hostname -s   첫 점 앞까지 짧은 이름 (--short)
#   hostname -f   FQDN. /etc/hosts 나 DNS 로 풀린 전체 이름 (--fqdn)
#   hostname -d   DNS 도메인 부분 (--domain)
hostname -s    # ubuntu
hostname -f    # ubuntu
hostname -d
```

### 이름 바꾸기

> `hostnamectl hostname NAME` 은 이름을 한꺼번에 바꾸고, 옵션을 주면 고른 이름만 바꿉니다.

`hostnamectl hostname NAME` 은 인자가 없으면 읽고 있으면 바꿉니다. 옵션이 없으면 pretty·static·transient 를 한꺼번에 바꾸고, `--static`·`--transient`·`--pretty` 를 주면 고른 이름만 바꿉니다.[^hctl]

이름을 바꾸는 일은 권한이 필요해서 `sudo` 를 붙입니다. 권한이 없을 때의 실패는 「종료 코드」 에 있습니다.

```bash
# 옵션 없이 이름을 주면 static·transient(·pretty)를 모두 바꾼다
sudo hostnamectl hostname labhost
```

바꾼 이름이 `hostname`·`/etc/hostname`·static 이름 셋에 모두 반영됩니다. 부팅 때 읽는 `/etc/hostname` 까지 바뀌므로 재부팅 뒤에도 남습니다.

```bash
hostname    # labhost
cat /etc/hostname    # labhost
hostnamectl --static    # labhost
```

`--pretty` 는 pretty 이름만 바꾸고 static 이름은 그대로입니다. pretty 이름은 `/etc/machine-info` 의 `PRETTY_HOSTNAME` 에 저장되며, 이 파일은 없어도 되는 파일이라 이름을 처음 정하는 순간 만들어집니다.[^minfo]

```bash
# 공백과 괄호가 들어간 사람용 이름을 pretty 에만 넣는다
sudo hostnamectl --pretty hostname "Lab Host (test)"
hostnamectl --pretty    # Lab Host (test)

# static 은 그대로
hostnamectl --static    # labhost

# pretty 는 /etc/machine-info 에 들어간다
cat /etc/machine-info    # PRETTY_HOSTNAME="Lab Host (test)"
```

```bash
# status 에도 Pretty hostname 줄이 생긴다
hostnamectl 2>/dev/null | head -2
```

```bash
 Static hostname: labhost
 Pretty hostname: Lab Host (test)
```

`--transient` 는 transient 이름만 바꾸려는 옵션인데, static 이 이미 정해져 있으면 쓰이지 않는다는 힌트만 나오고 이름은 그대로입니다.[^hostname5]

```bash
# transient 만 바꾸면 static 이 있어 효과가 없다는 힌트가 나온다
sudo hostnamectl --transient hostname tmp-name    # Hint: static hostname is already set, so the specified transient hostname will not be used.
hostnamectl --transient    # labhost
```

transient 이름을 바꾸는 효과는 커널의 호스트 이름을 직접 바꾸는 `hostname NAME` 으로 냅니다. 이 명령은 `sethostname(2)` 만 부르고 `/etc/hostname` 은 건드리지 않아 다음 재부팅 때까지만 유효합니다.[^hname] 그러면 transient 이름이 static 과 갈라져 `hostnamectl` 이 두 이름을 따로 보입니다.

```bash
# hostname 명령에 이름을 주면 커널의 이름만 바꾼다 (재부팅까지)
sudo hostname kernel-name
hostname    # kernel-name

# /etc/hostname 은 그대로
cat /etc/hostname    # labhost

# static 은 그대로, transient 는 커널 이름을 따라간다
hostnamectl --static    # labhost
hostnamectl --transient    # kernel-name
```

```bash
# status 에 Transient hostname 줄이 생긴다
hostnamectl 2>/dev/null | head -2
```

```bash
Transient hostname: kernel-name
   Static hostname: labhost
```

옛 이름 `set-hostname` 도 이 VM(systemd 259)에서는 `hostname NAME` 과 같게 동작했습니다. 다만 이 버전의 man 에는 `hostname` 만 올라 있으므로 새로 쓰는 스크립트는 `hostname` 을 씁니다.[^hctl]

```bash
# 옛 이름 set-hostname 도 hostname NAME 과 같이 동작했다
sudo hostnamectl set-hostname labhost2
hostnamectl --static    # labhost2
```

### 그 밖의 항목과 JSON 출력

> `hostnamectl` 은 이름 말고도 섀시 종류와 아이콘 이름을 읽고, 상태를 JSON 으로 찍을 수 있습니다.

`hostnamectl` 은 이름 말고도 아이콘 이름·섀시 종류·배포 환경·위치를 읽고 씁니다. 같은 `명령 [값]` 모양이고 값을 주면 `/etc/machine-info` 에 저장되며, 이 VM 에서는 읽기만 했습니다.[^hctl]

```bash
# 섀시 종류. 가상 환경은 vm 이나 container
hostnamectl chassis    # container

# 그래픽 도구가 이 호스트를 그릴 때 쓰는 아이콘 이름
hostnamectl icon-name    # computer-container
```

`--json=` 은 상태를 JSON 으로 찍고 값은 `short`(한 줄)·`pretty`(들여쓰기)·`off` 입니다.[^hctl] 이 시트의 출력은 앞 몇 줄만 잘랐고 바로 앞에서 바꾼 이름 `labhost2` 가 그대로 보입니다.

```bash
# 들여쓰기한 JSON 의 앞 다섯 줄
#   --json=pretty   들여쓰기한 JSON 으로 찍는다
#   head -5   앞 다섯 줄만 남긴다 (--lines)
hostnamectl --json=pretty | head -5
```

```bash
{
	"Hostname" : "labhost2",
	"StaticHostname" : "labhost2",
	"PrettyHostname" : null,
	"DefaultHostname" : "localhost",
```

```bash
# 공백 없는 한 줄 JSON 의 앞 100자
#   --json=short   공백 없는 한 줄 JSON 으로 찍는다
#   cut -c1-100   글자 1번부터 100번까지만 남긴다 (--characters)
hostnamectl --json=short | cut -c1-100    # {"Hostname":"labhost2","StaticHostname":"labhost2","PrettyHostname":null,"DefaultHostname":"localhos
```

`-H`(`--host`)는 SSH 로 다른 호스트에, `-M`(`--machine`)은 로컬 컨테이너에 같은 명령을 보내는 옵션입니다.[^hctl] 이 시트에서는 실행하지 않았습니다.

### hostnamectl 로 배포판과 커널 줄 고르기

> `hostnamectl` 한 번이 배포판과 커널 정보를 한 화면에 모으므로, 필요한 줄만 `grep` 으로 고릅니다.

[uname·os-release·lsb_release 참조 시트](./uname·os-release·hostnamectl.md)의 「이 서버의 배포판과 커널을 세 줄로」 는 세 명령을 이었지만, systemd 가 도는 서버라면 이 한 번으로 됩니다. 처음 두 줄은 이 VM 의 읽기 권한 경고입니다.

```bash
# hostnamectl 의 Operating System 과 Kernel 줄
hostnamectl | grep -E "Operating System|Kernel"
```

```bash
Failed to query product UUID, ignoring: Access denied
Failed to query hardware serial, ignoring: Access denied
Operating System: Ubuntu 26.04.1 LTS
          Kernel: Linux 7.2.12-orbstack-00394-gbecdd6130068
```

### 실습 정리

> 위에서 바꾼 static 이름과 pretty 이름을 원래대로 되돌립니다.

pretty 이름을 빈 값으로 정하면 `/etc/machine-info` 의 그 줄이 사라지고, 파일에 다른 줄이 없었으니 파일도 없어집니다.

```bash
# static·transient 를 원래 이름으로
sudo hostnamectl hostname ubuntu

# pretty 를 비운다
sudo hostnamectl --pretty hostname ""
hostnamectl --static    # ubuntu
hostname    # ubuntu
echo "[$(hostnamectl --pretty)]"    # []

# pretty 를 비우면 파일도 없어진다
ls /etc/machine-info    # ls: cannot access '/etc/machine-info': No such file or directory
```



## 주의사항과 동작 원리

> `hostname NAME` 은 재부팅까지만 유효하고, `hostnamectl` 은 static 이름을 우선합니다.

### hostname 과 hostnamectl 의 차이

> `hostname NAME` 은 커널의 이름만 바꾸고, `hostnamectl hostname NAME` 은 파일까지 바꿉니다.

`hostname NAME` 은 `sethostname(2)` 만 불러 다음 재부팅 때까지만 유효하고, 영구히 바꾸려면 `/etc/hostname` 을 고쳐야 한다고 man 이 적습니다.[^hname] `hostnamectl` 은 static 이름이 유효하면 transient 이름을 쓰지 않으므로 `--transient` 로 바꾼 이름은 효과가 없습니다.[^hostname5] 두 이름이 갈라진 상태는 「이름 바꾸기」 의 `hostnamectl` 출력에서 보입니다.



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [uname·os-release·lsb_release 참조 시트](./uname·os-release·hostnamectl.md) — 이 시트를 떼어 낸 원래 시트, 커널과 배포판 확인
- [systemctl 참조 시트](../service/systemctl.md) — `hostnamectl` 이 속한 systemd 서비스 관리



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- systemd 259.9 의 `hostnamectl --help`·`man hostnamectl`, hostname 3.25 의 `hostname --help` 원문 — OrbStack VM `ubuntu` 에서 2026-11-14 확인
- [hostnamectl(1) — Debian bookworm](https://manpages.debian.org/bookworm/systemd/hostnamectl.1.en.html)
- [hostname(1) — Debian bookworm](https://manpages.debian.org/bookworm/hostname/hostname.1.en.html)
- [hostname(5) — Debian bookworm](https://manpages.debian.org/bookworm/systemd/hostname.5.en.html)
- [machine-info(5) — Debian bookworm](https://manpages.debian.org/bookworm/systemd/machine-info.5.en.html)
- [uname(2) — Debian bookworm](https://manpages.debian.org/bookworm/manpages-dev/uname.2.en.html)
- [proc(5) — Debian bookworm](https://manpages.debian.org/bookworm/manpages/proc.5.en.html)

[^uname2]: `man 2 uname` (Debian bookworm, manpages-dev) — "uname() returns system information in the structure pointed to by buf." 구조체 칸은 `sysname`("Operating system name (e.g., "Linux")"), `nodename`, `release`("Operating system release (e.g., "2.6.28")"), `version`("Operating system version"), `machine`("Hardware type identifier"). NOTES: "The kernel has the name, release, version, and supported machine type built in. Conversely, the nodename field is configured by the administrator to match the network (this is what the BSD historically calls the "hostname", and is set via sethostname(2))." https://manpages.debian.org/bookworm/manpages-dev/uname.2.en.html
[^proc]: `man 5 proc` (Debian bookworm) — "/proc/version This string identifies the kernel version that is currently running. It includes the contents of /proc/sys/kernel/ostype, /proc/sys/kernel/osrelease, and /proc/sys/kernel/version." "/proc/sys/kernel/ostype and /proc/sys/kernel/osrelease These files give substrings of /proc/version." "/proc/sys/kernel/hostname can be used to set the NIS/YP domainname and the hostname of your box in exactly the same way as the commands domainname(1) and hostname(1)". https://manpages.debian.org/bookworm/manpages/proc.5.en.html
[^hctl]: `man hostnamectl` (systemd 252 bookworm 원문과 VM 의 systemd 259.9 `man hostnamectl` 에서 같은 문장 확인) — "the high-level "pretty" hostname which might include all kinds of special characters (e.g. "Lennart's Laptop"), the "static" hostname which is the user-configured hostname (e.g. "lennarts-laptop"), and the transient hostname which is a fallback value received from network configuration (e.g. "node12345678"). If a static hostname is set to a valid value, then the transient hostname is not used." "status Show system hostname and related information. If no command is specified, this is the implied default." "hostname [NAME] If no argument is given, print the system hostname. If an optional argument NAME is provided then the command changes the system hostname to NAME. By default, this will alter the pretty, the static, and the transient hostname alike; however, if one or more of --static, --transient, --pretty are used, only the selected hostnames are changed." "The static and transient hostnames must each be either a single DNS label (a string composed of 7-bit ASCII lower-case characters and no spaces or dots, limited to the format allowed for DNS domain name labels), or a sequence of such labels separated by single dots that forms a valid DNS FQDN. The hostname must be at most 64 characters, which is a Linux limitation". 같은 문서의 COMMANDS 목록에 `set-hostname` 은 올라 있지 않습니다. icon-name·chassis·deployment·location 은 "If no argument is given, print ... If an optional argument ... is provided then the command changes ...". "--no-ask-password Do not query the user for authentication for privileged operations." "--static, --transient, --pretty If status is invoked (or no explicit command is given) and one of these switches is specified, hostnamectl will print out just this selected hostname." "-H, --host= Execute the operation remotely.", "-M, --machine= Execute operation on a local container.", "--json=MODE ... "short" ... "pretty" ... "off"". https://manpages.debian.org/bookworm/systemd/hostnamectl.1.en.html
[^hname]: `man hostname` (hostname 3.23, Debian bookworm) — "hostname will print the name of the system as returned by the gethostname(2) function." "Note, that this is effective only until the next reboot. Edit /etc/hostname for permanent change." "-s, --short Display the short host name. This is the host name cut at the first dot." "-f, --fqdn, --long Display the FQDN (Fully Qualified Domain Name)." "-d, --domain Display the name of the DNS domain." "Therefore avoid using hostname --fqdn, hostname --domain and dnsdomainname. hostname --ip-address is subject to the same limitations so it should be avoided as well." https://manpages.debian.org/bookworm/hostname/hostname.1.en.html
[^hostname5]: `man 5 hostname` (systemd 252, Debian bookworm) — "The /etc/hostname file configures the name of the local system. Unless overridden as described in the next section, systemd(1) will set this hostname during boot using the sethostname(2) system call." "Note that systemd-hostnamed.service(8) gives higher priority to the static hostname, so the transient hostname will only be used if the static hostname is not configured." https://manpages.debian.org/bookworm/systemd/hostname.5.en.html
[^minfo]: `man 5 machine-info` (systemd 252, Debian bookworm) — "PRETTY_HOSTNAME= A pretty human-readable UTF-8 machine identifier string." "It is thus completely fine for this file to not be present. You may use hostnamectl(1) to change the settings of this file from the command line." https://manpages.debian.org/bookworm/systemd/machine-info.5.en.html
[^hctl-exit]: `man hostnamectl` (systemd 252, Debian bookworm), EXIT STATUS — "On success, 0 is returned, a non-zero failure code otherwise." 코드 1 은 이 시트의 실측입니다(OrbStack VM `ubuntu`, systemd 259.9). https://manpages.debian.org/bookworm/systemd/hostnamectl.1.en.html
