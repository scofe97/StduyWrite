---
title: uname·os-release·hostnamectl 참조 시트
tags: [linux, cheatsheet, uname, os-release, lsb_release, hostnamectl, hostname, sysinfo, cli, reference]
status: draft
source:
  - GNU coreutils 9.1 uname(1) (Debian 12 `uname --help` 원문, manpages.debian.org bookworm), uname(2)·gethostname(2)·proc(5) (bookworm)
  - systemd 252 os-release(5)·hostname(5)·machine-info(5)·hostnamectl(1) (bookworm), OrbStack VM 의 systemd 259.9 `man hostnamectl`
  - lsb-release 12.0 lsb_release(1), hostname 3.23 hostname(1) (bookworm)
related:
  - ../README.md
updated: 2026-11-11
---

# uname·os-release·hostnamectl 참조 시트

---

> 이 서버가 어떤 커널과 배포판이고 이름이 무엇인지를 `uname`·`/etc/os-release`·`lsb_release`·`hostnamectl` 로 확인하고 바꾸는 방법을, 따라 치면 그대로 나오는 예제로 모았습니다.

## 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 파일이 모두 만들어집니다.

macOS 에는 `/etc/os-release` 도 `lsb_release` 도 `hostnamectl` 도 없습니다. `uname` 도 BSD 판이라 `-i` 를 받지 않습니다(`uname: illegal option -- i`). 이 시트는 GNU coreutils 9.1 의 `uname` 과 lsb-release 12.0 의 `lsb_release` 를 씁니다.

1절부터 6절과 8절의 첫 예는 `docker run -it --rm debian:12` 안에서 root 로 실행했습니다. `lsb_release` 는 이 컨테이너에 처음부터 없어서 준비 블록이 설치합니다. 7절의 `hostnamectl` 은 systemd 가 돌아야 해서 OrbStack 의 Linux VM `ubuntu` 에서 `sudo` 가 되는 일반 사용자로 실행했습니다. 이 VM 은 Ubuntu 26.04.1 이고 systemd 259.9, hostname 3.25 가 깔려 있습니다.

`docker run --rm rockylinux:9` 나 `orb -m ubuntu` 처럼 `docker` 와 `orb` 를 부르는 예에는 "호스트에서 실행" 이라고 적었습니다. 둘이 있는 호스트의 터미널에서 칩니다.

```bash
apt-get update -qq >/dev/null 2>&1; apt-get install -y -qq lsb-release >/dev/null 2>&1
mkdir -p ~/cmd-lab/uname && cd ~/cmd-lab/uname
cat > distro.sh << 'EOF2'
#!/bin/sh
# 사용: ./distro.sh [os-release 파일]  (인자가 없으면 /etc/os-release)
. "${1:-/etc/os-release}"
case " $ID $ID_LIKE " in
  *" debian "*) echo "$ID: apt 계열 ($VERSION_ID)" ;;
  *" rhel "*|*" fedora "*) echo "$ID: dnf 계열 ($VERSION_ID)" ;;
  *) echo "$ID: 모르는 계열" ;;
esac
EOF2
chmod +x distro.sh
cat > rocky.os-release << 'EOF2'
NAME="Rocky Linux"
VERSION="9.3 (Blue Onyx)"
ID="rocky"
ID_LIKE="rhel centos fedora"
VERSION_ID="9.3"
PLATFORM_ID="platform:el9"
PRETTY_NAME="Rocky Linux 9.3 (Blue Onyx)"
ANSI_COLOR="0;32"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:rocky:rocky:9::baseos"
HOME_URL="https://rockylinux.org/"
BUG_REPORT_URL="https://bugs.rockylinux.org/"
SUPPORT_END="2032-05-31"
ROCKY_SUPPORT_PRODUCT="Rocky-Linux-9"
ROCKY_SUPPORT_PRODUCT_VERSION="9.3"
REDHAT_SUPPORT_PRODUCT="Rocky Linux"
REDHAT_SUPPORT_PRODUCT_VERSION="9.3"
EOF2
```

이 블록은 `distro.sh` 와 `rocky.os-release` 두 파일을 만듭니다. `distro.sh` 는 `os-release` 파일을 읽어 `ID` 와 `ID_LIKE` 로 계열을 나누는 짧은 스크립트입니다. `rocky.os-release` 는 Rocky Linux 9 컨테이너의 `/etc/os-release` 를 그대로 옮긴 파일이라, Rocky 컨테이너가 없어도 5절의 분기를 시험할 수 있습니다. 7절의 `hostnamectl` 은 파일이 필요 없어서 이 블록 없이도 됩니다.

`uname -n`·`/proc/sys/kernel/hostname` 의 컨테이너 이름(12자리 16진수 값)은 컨테이너를 만들 때마다 달라집니다. 커널 릴리스와 빌드 시각은 쓰는 OrbStack 의 커널에 따라 달라집니다. Rocky 컨테이너의 판(`9.3`)은 이 기기에 내려받아 둔 이미지의 값입니다. 값이 이 시트와 달라도 형식은 같습니다.



## 1. 커널 이름과 하드웨어 확인, uname

> `uname` 은 커널이 알고 있는 이름 다섯 칸(운영체제·호스트·릴리스·빌드 버전·하드웨어)을 옵션 하나에 한 칸씩 꺼냅니다.

`uname` 은 `uname(2)` 시스템 콜이 채워 주는 구조체의 칸을 찍습니다. 칸은 운영체제 이름(`sysname`), 네트워크 노드 이름(`nodename`), 릴리스(`release`), 버전(`version`), 하드웨어 종류(`machine`)입니다.[^uname2] 명령 한 줄이 시스템 콜 하나를 감싸는 구조는 `id --user` 가 `getuid` 를 감싸는 것과 같습니다. 그 설명은 [하드웨어를 가리고 나면 무엇이 보일지를 정해야 한다 노트의 「명령 한 줄로 확인하는 방법」](../../../book/learning-modern-linux/01-01.%ED%95%98%EB%93%9C%EC%9B%A8%EC%96%B4%EB%A5%BC%20%EA%B0%80%EB%A6%AC%EA%B3%A0%20%EB%82%98%EB%A9%B4%20%EB%AC%B4%EC%97%87%EC%9D%B4%20%EB%B3%B4%EC%9D%BC%EC%A7%80%EB%A5%BC%20%EC%A0%95%ED%95%B4%EC%95%BC%20%ED%95%9C%EB%8B%A4.md#명령-한-줄로-확인하는-방법)에 있습니다.

```bash
# (옵션 없음): -s 와 같다
uname    # Linux
# -s (--kernel-name): 커널 이름
uname -s    # Linux
# -n (--nodename): 네트워크에서 쓰는 호스트 이름. 컨테이너에서는 컨테이너 ID
uname -n    # 37d0d842ab53
# -r (--kernel-release): 커널 릴리스. 버전 번호와 빌더가 붙인 꼬리표
uname -r    # 7.2.12-orbstack-00394-gbecdd6130068
# -v (--kernel-version): 커널 빌드 문자열. 빌드 번호·선점 모델·빌드 시각
uname -v    # #1 SMP PREEMPT Thu Oct 22 22:17:17 UTC 2026
# -m (--machine): 하드웨어 이름. x86_64 나 aarch64
uname -m    # aarch64
```

`-p`(`--processor`)와 `-i`(`--hardware-platform`)는 man 이 "non-portable" 이라고 적은 옵션입니다. 이 Debian 컨테이너에서는 값을 알아내지 못해 `unknown` 을 찍습니다.[^uname]

```bash
# -p (--processor): 프로세서 종류. 이식성이 없다
uname -p    # unknown
# -i (--hardware-platform): 하드웨어 플랫폼. 이식성이 없다
uname -i    # unknown
# -o (--operating-system): 운영체제 이름. 커널 이름이 아니라 GNU/Linux
uname -o    # GNU/Linux
```

`-a`(`--all`)는 위 칸을 정해진 순서로 한 줄에 모두 찍되 `-p` 와 `-i` 가 `unknown` 이면 뺍니다.[^uname] Debian 에서는 그 둘이 빠지고 같은 하드웨어에서 Rocky 컨테이너의 `uname` 은 둘 다 알아내 `aarch64` 를 두 번 더 붙입니다.

```bash
# -a (--all): 칸을 순서대로 모두. unknown 인 -p·-i 는 뺀다
uname -a    # Linux 37d0d842ab53 7.2.12-orbstack-00394-gbecdd6130068 #1 SMP PREEMPT Thu Oct 22 22:17:17 UTC 2026 aarch64 GNU/Linux
# Rocky 컨테이너(호스트에서 실행): -p·-i 가 aarch64 로 나와 -a 에 두 칸이 더 붙는다
docker run --rm rockylinux:9 uname -a    # Linux 882b3d4940aa 7.2.12-orbstack-00394-gbecdd6130068 #1 SMP PREEMPT Thu Oct 22 22:17:17 UTC 2026 aarch64 aarch64 aarch64 GNU/Linux
docker run --rm rockylinux:9 uname -p -i    # aarch64 aarch64
```

배포판에 따라 `-p`·`-i` 값이 갈리므로 스크립트에서 하드웨어를 가릴 때는 `-m` 을 씁니다. 옵션을 여러 개 주면 `uname` 은 인자 순서와 상관없이 위 `-s -n -r -v -m` 의 고정 순서로 찍습니다.

```bash
# -m -s 로 줘도 커널 이름(-s)이 앞에 온다
uname -m -s    # Linux aarch64
# 자주 쓰는 묶음: 커널 이름과 릴리스와 하드웨어를 한 줄로
uname -srm    # Linux 7.2.12-orbstack-00394-gbecdd6130068 aarch64
```

`uname -m` 의 이름은 패키지 관리자가 쓰는 아키텍처 이름과 다를 수 있습니다. 같은 컨테이너에서 Debian 의 `dpkg` 는 `arm64` 라고 부릅니다. 파일을 내려받는 스크립트에서 `aarch64` 와 `arm64` 를 맞바꿔야 하는 일이 여기서 생깁니다. CPU 모델이나 코어 수는 `uname` 이 알려 주지 않으므로 `lscpu` 를 씁니다. 그 확인은 [커널은 전부를 하지만 운영체제는 아니다 노트의 「무엇을 쓰고 있는지 확인하는 법」](../../../book/learning-modern-linux/02-01.%EC%BB%A4%EB%84%90%EC%9D%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%ED%95%98%EC%A7%80%EB%A7%8C%20%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EB%8A%94%20%EC%95%84%EB%8B%88%EB%8B%A4.md#무엇을-쓰고-있는지-확인하는-법)에 있습니다.

```bash
# dpkg 의 아키텍처 이름: uname -m 의 aarch64 와 같은 하드웨어
dpkg --print-architecture    # arm64
```



## 2. 릴리스와 빌드 문자열 구분, /proc 대조

> `uname -r` 은 커널 버전을 알리는 짧은 이름이고, `uname -v` 는 그 빌드가 언제 어떻게 만들어졌는지를 적은 문자열입니다.

`/proc/version` 은 지금 돌고 있는 커널을 설명하는 한 줄이고 그 안에 `/proc/sys/kernel/ostype`·`osrelease`·`version` 의 내용이 들어 있습니다. `ostype` 과 `osrelease` 는 `/proc/version` 의 부분 문자열입니다.[^proc] 컴파일러 정보까지 붙은 긴 한 줄이라, 앞 세 단어와 `#` 로 시작하는 뒤쪽만 나눠 봅니다.

```bash
# /proc/version 의 앞쪽: 커널 이름·"version"·릴리스. uname -r 과 같은 값이 들어 있다
cut -d" " -f1-3 /proc/version    # Linux version 7.2.12-orbstack-00394-gbecdd6130068
# /proc/version 의 # 로 시작하는 뒤쪽: 빌드 번호·선점 모델·빌드 시각
grep -o '#.*' /proc/version    # #1 SMP PREEMPT Thu Oct 22 22:17:17 UTC 2026
# uname -v 가 찍는 값과 같은 문자열
uname -v    # #1 SMP PREEMPT Thu Oct 22 22:17:17 UTC 2026
```

`/proc/sys/kernel` 아래에는 같은 값이 칸마다 따로 파일로 있습니다. `uname` 이 시스템 콜로 읽는 값과 파일에서 읽는 값은 같은 커널 변수입니다.

```bash
# osrelease: uname -r 과 같은 값
cat /proc/sys/kernel/osrelease    # 7.2.12-orbstack-00394-gbecdd6130068
# version: uname -v 와 같은 값
cat /proc/sys/kernel/version    # #1 SMP PREEMPT Thu Oct 22 22:17:17 UTC 2026
# ostype: uname -s 와 같은 값
cat /proc/sys/kernel/ostype    # Linux
# hostname: uname -n 과 같은 값 (4절에서 hostnamectl 과 함께 다시 본다)
cat /proc/sys/kernel/hostname    # 37d0d842ab53
# 두 값이 정말 같은지 문자열로 비교한다
[ "$(uname -r)" = "$(cat /proc/sys/kernel/osrelease)" ] && echo "uname -r 과 osrelease 가 같다"    # uname -r 과 osrelease 가 같다
[ "$(uname -v)" = "$(cat /proc/sys/kernel/version)" ] && echo "uname -v 와 version 이 같다"    # uname -v 와 version 이 같다
```

커널 버전을 비교하는 스크립트는 `-r` 을 씁니다. `-v` 에는 빌드 번호와 시각이 들어 있어서 버전 순서를 비교하는 값이 아닙니다.



## 3. 컨테이너와 VM 이 보는 같은 커널

> 컨테이너 안의 `uname -r` 은 이미지의 배포판이 아니라 그 컨테이너를 돌리는 Linux 커널의 값입니다. 맥에서는 OrbStack 이 띄운 Linux VM 의 커널입니다.

`uname` 이 읽는 릴리스·버전·하드웨어는 커널에 들어 있는 값입니다.[^uname2] 컨테이너는 배포판의 파일과 프로그램만 이미지에서 가져오고 커널은 가져오지 않으므로, 배포판이 달라도 커널 값은 같습니다. 이 기기의 macOS 호스트는 `Darwin` 이고 컨테이너 둘과 OrbStack 의 VM 은 셋 다 같은 `Linux` 커널을 보입니다.

OrbStack 은 가벼운 Linux VM 하나가 커널을 쥐고 `ubuntu` 같은 머신은 그 커널을 나눠 쓰며 돕니다.[^orb] 7절의 `hostnamectl` 이 이 머신을 `Virtualization: lxc` 로 보이는 것도 그래서입니다.

전역으로 보이는 값과 가려지는 값의 구분은 [노트의 「같은 자원인데 보는 자리에 따라 답이 갈린다」](../../../book/learning-modern-linux/01-01.%ED%95%98%EB%93%9C%EC%9B%A8%EC%96%B4%EB%A5%BC%20%EA%B0%80%EB%A6%AC%EA%B3%A0%20%EB%82%98%EB%A9%B4%20%EB%AC%B4%EC%97%87%EC%9D%B4%20%EB%B3%B4%EC%9D%BC%EC%A7%80%EB%A5%BC%20%EC%A0%95%ED%95%B4%EC%95%BC%20%ED%95%9C%EB%8B%A4.md#4-같은-자원인데-보는-자리에-따라-답이-갈린다)에서 다룹니다.

```bash
# 호스트(macOS)의 커널
uname -sr    # Darwin 25.6.0
# Debian 컨테이너가 보는 커널
docker run --rm debian:12 uname -sr    # Linux 7.2.12-orbstack-00394-gbecdd6130068
# Rocky 컨테이너가 보는 커널. 배포판이 달라도 같은 값
docker run --rm rockylinux:9 uname -sr    # Linux 7.2.12-orbstack-00394-gbecdd6130068
# OrbStack VM 이 보는 커널
orb -m ubuntu uname -sr    # Linux 7.2.12-orbstack-00394-gbecdd6130068
```

그래서 컨테이너 안에서 `uname -r` 로 커널을 확인한 뒤 그 값을 배포판 이미지의 속성으로 읽으면 안 됩니다. 배포판을 확인하는 길은 `uname` 이 아니라 다음 절의 `/etc/os-release` 입니다.



## 4. 배포판 이름과 버전 확인, os-release

> `/etc/os-release` 는 배포판이 자기 이름과 버전을 `키=값` 으로 적어 둔 파일이라, 배포판 종류를 묻는 가장 표준적인 자리입니다.

`/etc/os-release` 와 `/usr/lib/os-release` 는 운영체제를 식별하는 데이터를 담습니다. 형식은 셸에서 읽을 수 있는 `키=값` 줄이고 공백이나 특수 문자가 든 값은 따옴표로 감쌉니다.[^osrel]

```bash
# Debian 12 컨테이너의 os-release
cat /etc/os-release
```

```bash
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
NAME="Debian GNU/Linux"
VERSION_ID="12"
VERSION="12 (bookworm)"
VERSION_CODENAME=bookworm
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"
```

자주 쓰는 키 다섯 개의 뜻은 man 에서 다음과 같이 읽힙니다.[^osrel] `ID` 는 스크립트가 처리하기 좋은 소문자 식별자이고 `ID_LIKE` 는 이 배포판이 파생된 가까운 배포판의 `ID` 목록입니다. `VERSION_ID` 는 코드명 없이 버전만 담은 값이고 `VERSION_CODENAME` 은 릴리스 코드명입니다. `PRETTY_NAME` 은 사람에게 보여 주는 이름입니다. `ID_LIKE` 와 `VERSION_CODENAME` 은 선택이라 배포판에 따라 없습니다. Debian 에는 `ID_LIKE` 가 없고 Rocky 에는 `VERSION_CODENAME` 이 없습니다.

```bash
# 다섯 키만 골라 본다 (Debian 12 컨테이너)
grep -E "^(ID|ID_LIKE|VERSION_ID|VERSION_CODENAME|PRETTY_NAME)=" /etc/os-release
```

```bash
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
VERSION_ID="12"
VERSION_CODENAME=bookworm
ID=debian
```

```bash
# Rocky Linux 9 컨테이너(호스트에서 실행): ID_LIKE 가 있고 VERSION_CODENAME 이 없다
docker run --rm rockylinux:9 grep -E '^(ID|ID_LIKE|VERSION_ID|VERSION_CODENAME|PRETTY_NAME)=' /etc/os-release
```

```bash
ID="rocky"
ID_LIKE="rhel centos fedora"
VERSION_ID="9.3"
PRETTY_NAME="Rocky Linux 9.3 (Blue Onyx)"
```

```bash
# Ubuntu 26.04 VM(호스트에서 실행): ID 는 ubuntu, ID_LIKE 는 debian
orb -m ubuntu grep -E '^(ID|ID_LIKE|VERSION_ID|VERSION_CODENAME|PRETTY_NAME)=' /etc/os-release
```

```bash
PRETTY_NAME="Ubuntu 26.04.1 LTS"
VERSION_ID="26.04"
VERSION_CODENAME=resolute
ID=ubuntu
ID_LIKE=debian
```

Ubuntu 의 `ID_LIKE=debian` 은 "Debian 과 패키지와 프로그래밍 인터페이스가 가깝다" 는 선언입니다. 스크립트가 `ID` 를 모르는 배포판을 만났을 때 `ID_LIKE` 로 가까운 쪽을 따라가라고 만든 키입니다.[^osrel]

### /etc 와 /usr/lib 의 두 파일

`/usr/lib/os-release` 는 배포판이 설치하는 원본이고 `/etc/os-release` 는 여기를 가리키는 상대 심볼릭 링크로 두는 것이 권장입니다. 읽는 쪽은 `/etc/os-release` 를 먼저 보고 없을 때만 `/usr/lib/os-release` 로 물러납니다. 둘을 동시에 읽어 합치면 안 됩니다.[^osrel]

```bash
# 링크 모양 확인: /etc 쪽이 ../usr/lib/os-release 를 가리킨다
ls -l /etc/os-release /usr/lib/os-release
```

```bash
lrwxrwxrwx 1 root root  21 Jul  2 19:05 /etc/os-release -> ../usr/lib/os-release
-rw-r--r-- 1 root root 267 Jul  2 19:05 /usr/lib/os-release
```

```bash
# 링크를 끝까지 따라간 실제 파일
readlink -f /etc/os-release    # /usr/lib/os-release
# 두 경로의 내용이 같은지
cmp /etc/os-release /usr/lib/os-release && echo 내용이 같다    # 내용이 같다
```



## 5. 스크립트에서 배포판 읽기와 분기

> `os-release` 는 셸이 그대로 읽을 수 있는 형식이라, `grep` 으로 값을 자르지 않고 파일을 `.` 로 읽어 변수로 씁니다.

`os-release` 는 변수 대입만 담도록 정해져 있어 셸에서 `source` 해도 됩니다. 변수 확장 같은 셸 기능은 지원하지 않는다고 man 이 적습니다.[^osrel] `grep` 과 `cut` 으로 자르면 따옴표가 값에 남습니다.

```bash
# grep+cut 으로 자르면 따옴표가 값에 그대로 붙는다
grep ^PRETTY_NAME= /etc/os-release | cut -d= -f2    # "Debian GNU/Linux 12 (bookworm)"
```

`.`(`source`)로 읽으면 셸이 따옴표를 풀어 주고 키 이름이 그대로 변수가 됩니다. 단, 읽는 순간 현재 셸에 `NAME`·`VERSION`·`ID` 같은 변수가 생겨 이미 있던 같은 이름의 변수를 덮어씁니다.

```bash
# 읽기 전: NAME 은 비어 있다
echo "NAME=[$NAME]"    # NAME=[]
# . 으로 읽어 ID 와 VERSION_ID 를 바로 쓴다
. /etc/os-release; echo "$ID $VERSION_ID"    # debian 12
# 읽은 뒤: NAME 이 현재 셸에 남았다
echo "읽은 뒤 NAME=[$NAME]"    # 읽은 뒤 NAME=[Debian GNU/Linux]
```

스크립트에서는 괄호로 서브셸을 만들어 그 안에서만 읽으면 변수가 밖으로 새지 않습니다.

```bash
# 서브셸 ( ) 안에서 읽는다. PRETTY_NAME 의 따옴표와 공백도 셸이 처리한다
( . /etc/os-release; echo "$PRETTY_NAME" )    # Debian GNU/Linux 12 (bookworm)
```

준비 블록의 `distro.sh` 는 `ID` 와 `ID_LIKE` 를 앞뒤에 공백을 붙인 한 문자열로 만들어 `case` 로 계열을 가립니다. 앞뒤 공백은 `ID` 와 `ID_LIKE` 안의 낱말을 통째로만 맞추려는 것입니다. 그래서 `debian-like` 같은 부분 문자열에는 걸리지 않습니다.

`distro.sh` 는 `#!/bin/sh` 라서 Debian 에서는 dash 가 읽습니다. dash 의 `.` 는 `/` 가 없는 이름을 `PATH` 의 폴더에서만 찾으므로, 현재 폴더의 파일은 `./` 를 붙여 넘겨야 합니다. bash 는 보통 모드에서 `PATH` 에 없으면 현재 폴더도 찾지만 `--posix` 모드에서는 dash 처럼 실패합니다.[^dot]

```bash
# ./ 없이 넘기면 PATH 에서 찾다가 실패한다
./distro.sh rocky.os-release    # ./distro.sh: 3: .: rocky.os-release: not found
# 인자 없이: 이 컨테이너의 /etc/os-release 를 읽는다
./distro.sh    # debian: apt 계열 (12)
# Rocky 의 os-release 를 넘긴다. ID_LIKE 의 rhel 에 걸린다
./distro.sh ./rocky.os-release    # rocky: dnf 계열 (9.3)
```

호스트에서 Rocky 컨테이너에 같은 한 줄을 시켜도 `rocky 9.3` 이 나옵니다. 배포판이 달라도 읽는 코드는 같습니다.

```bash
# Rocky 컨테이너(호스트에서 실행): 같은 . /etc/os-release 한 줄
docker run --rm rockylinux:9 sh -c '. /etc/os-release; echo "$ID $VERSION_ID"'    # rocky 9.3
```



## 6. lsb_release 로 한 항목씩 꺼내기

> `lsb_release` 는 같은 정보를 `Distributor ID`·`Description`·`Release`·`Codename` 네 항목으로 나눠 찍는 옛 호환 명령입니다.

`lsb_release` 는 LSB 패키지 시절에 배포판을 묻던 명령입니다. Debian 의 `lsb-release` 패키지가 주는 판은 `os-release` 를 읽는 짧은 POSIX 셸 스크립트입니다. Debian 이 예전에 주던 Python 판과 출력이 바이트까지 같다고 man 이 적습니다.[^lsb] 이 패키지가 없는 최소 이미지에는 명령 자체가 없습니다. Debian 과 Rocky 의 최소 이미지는 둘 다 `lsb_release` 를 찾지 못합니다(호스트에서 실행).

```bash
# 최소 이미지에는 lsb_release 가 없다. 패키지 lsb-release 를 설치해야 한다
docker run --rm debian:12 sh -c 'lsb_release -a'    # sh: 1: lsb_release: not found
docker run --rm rockylinux:9 sh -c 'lsb_release -a'    # sh: line 1: lsb_release: command not found
```

`-a` 는 네 항목을 모두 찍고 나머지 네 옵션은 한 항목씩 찍습니다. 항목 이름과 값 사이는 탭입니다.

```bash
# -a (--all): 네 항목을 모두
lsb_release -a
```

```bash
Distributor ID:	Debian
Description:	Debian GNU/Linux 12 (bookworm)
Release:	12
Codename:	bookworm
```

```bash
# -i (--id): 배포판 식별자
lsb_release -i    # Distributor ID:	Debian
# -d (--description): 사람이 읽는 이름과 버전
lsb_release -d    # Description:	Debian GNU/Linux 12 (bookworm)
# -r (--release): 릴리스 번호
lsb_release -r    # Release:	12
# -c (--codename): 릴리스 코드명
lsb_release -c    # Codename:	bookworm
```

`-s`(`--short`)는 항목 이름을 떼고 값만 찍습니다. 스크립트에서 값을 변수에 담을 때 씁니다.[^lsb]

```bash
# -s -d: 값만. 변수에 담기 좋다
lsb_release -s -d    # Debian GNU/Linux 12 (bookworm)
lsb_release -s -i    # Debian
lsb_release -s -r    # 12
lsb_release -s -c    # bookworm
```

```bash
# -s -a: 네 항목의 값만 한 줄씩
lsb_release -s -a
```

```bash
Debian
Debian GNU/Linux 12 (bookworm)
12
bookworm
```

옵션을 여러 개 주면 `uname` 처럼 인자 순서와 상관없이 고정 순서(`Distributor ID`, `Description`, `Release`, `Codename`)로 찍습니다.

```bash
# -c -i 로 줘도 Distributor ID 가 먼저 나온다
lsb_release -c -i
```

```bash
Distributor ID:	Debian
Codename:	bookworm
```

`-v`(`--version`)는 이 시스템이 지원하는 LSB 모듈을 보여 주는 옵션인데, 이 최소 판은 지원하는 모듈이 없어 아무것도 찍지 않고 정상 종료합니다. `-h` 는 옵션 목록입니다.[^lsb]

```bash
# -v (--version): LSB 모듈 목록. 이 최소 판은 출력이 없다
lsb_release -v
```

```bash
# -h (--help): 옵션 목록
lsb_release -h
```

```bash
Usage: lsb_release [options]

Options:
  -h, --help         show this help message and exit
  -v, --version      show LSB modules this system supports
  -i, --id           show distributor ID
  -d, --description  show description of this distribution
  -r, --release      show release number of this distribution
  -c, --codename     show code name of this distribution
  -a, --all          show all of the above information
  -s, --short        show requested information in short format
```

`lsb_release` 의 값은 `os-release` 에서 옵니다. 세 값이 서로 같다는 것을 직접 확인합니다.

```bash
# Description=PRETTY_NAME, Codename=VERSION_CODENAME, Release=VERSION_ID
( . /etc/os-release; [ "$(lsb_release -sd)" = "$PRETTY_NAME" ] && [ "$(lsb_release -sc)" = "$VERSION_CODENAME" ] && [ "$(lsb_release -sr)" = "$VERSION_ID" ] && echo "os-release 값과 같다" )    # os-release 값과 같다
```

새 스크립트는 `lsb_release` 를 부르지 말고 `/etc/os-release` 를 읽는 편이 낫습니다. `lsb_release` 는 패키지를 따로 설치해야 하고 Rocky 같은 이미지에는 처음부터 없기 때문입니다.



## 7. 호스트 이름 보기와 바꾸기, hostnamectl

> `hostnamectl` 은 호스트 이름 세 종류(static·transient·pretty)를 한 도구로 보고 바꿉니다. systemd 가 도는 서버에서 씁니다.

이 절의 출력은 OrbStack VM `ubuntu` 에서 받았습니다. 이름을 바꾸는 예는 VM 의 호스트 이름을 실제로 바꾸므로, 절의 끝에서 원래 이름 `ubuntu` 로 되돌립니다. 같은 일을 따라 할 때도 마지막 되돌리기까지 실행합니다.

`hostnamectl` 은 호스트 이름을 셋으로 나눕니다. pretty 는 특수 문자가 들어가도 되는 사람용 이름입니다. static 은 관리자가 정한 이름이고 transient 는 네트워크 설정에서 받는 대체값입니다.

static 이 유효하게 정해져 있으면 transient 는 쓰이지 않습니다. static 과 transient 는 DNS 이름 규칙(레이블 하나, 또는 점으로 이은 FQDN)을 따라야 하고 길이는 64자까지입니다.[^hctl]

### 상태 읽기

```bash
# (명령 없음) 또는 status: 호스트 이름과 시스템 정보를 한 화면에. Machine ID 와 Boot ID 두 줄은 식별값이라 뺐다
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

처음 두 줄은 이 VM 에서 제품 UUID 와 하드웨어 일련번호를 읽을 권한이 없어서 나오는 경고입니다. `hostnamectl` 은 이 줄을 stderr 로 찍고 계속 진행하므로, 상태 전체를 찍는 이후 예에서는 `2>/dev/null` 로 가립니다. `status` 는 명령을 생략했을 때의 기본값이라 붙이든 안 붙이든 출력이 같습니다.[^hctl]

```bash
# status: 명령을 생략한 것과 같다
diff <(hostnamectl 2>&1) <(hostnamectl status 2>&1) && echo "status 를 붙여도 같다"    # status 를 붙여도 같다
```

### 이름 하나만 꺼내기

```bash
# hostname: 시스템 호스트 이름 하나만 (이름을 안 주면 읽기)
hostnamectl hostname    # ubuntu
# --static: 관리자가 정한 static 이름만
hostnamectl --static    # ubuntu
# --transient: transient 이름. static 이 있으면 지금 쓰는 이름
hostnamectl --transient    # ubuntu
# --pretty: pretty 이름. 설정하지 않았으면 빈 줄이다 (대괄호로 빈 값을 보인다)
echo "[$(hostnamectl --pretty)]"    # []
```

### hostname 명령과 /etc/hostname, 커널의 이름

`hostname` 명령은 `gethostname(2)` 가 돌려주는 시스템 이름을 찍습니다.[^hname] 커널이 들고 있는 그 이름이 `/proc/sys/kernel/hostname` 이고 `uname -n` 의 `nodename` 칸과 같습니다.[^proc][^uname2] `/etc/hostname` 은 static 이름을 담은 파일입니다. systemd 가 부팅 때 이 값을 `sethostname(2)` 로 커널에 넣습니다.[^hostname5] 바꾸기 전에는 네 곳이 모두 같은 이름을 보입니다.

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

`hostname` 명령의 `-s`·`-f`·`-d` 도 이 이름에서 파생됩니다. `-s` 는 첫 점까지 자른 짧은 이름이고 `-f` 는 FQDN, `-d` 는 DNS 도메인 부분입니다. 점이 없는 이름이라 `-s` 와 `-f` 는 같고 `-d` 는 빈 줄입니다. man 은 `-f`·`-d`·`-i` 가 네트워크 설정에 따라 결과가 달라지니 피하라고 권합니다.[^hname]

```bash
# -s (--short): 첫 점 앞까지 짧은 이름
hostname -s    # ubuntu
# -f (--fqdn): FQDN. /etc/hosts 나 DNS 로 풀린 전체 이름
hostname -f    # ubuntu
# -d (--domain): DNS 도메인 부분. 점이 없는 이름이라 비어 있다
hostname -d
```

### 이름 바꾸기

`hostnamectl hostname NAME` 은 인자가 없으면 읽고 있으면 바꿉니다. 옵션이 없으면 pretty·static·transient 를 한꺼번에 바꿉니다. `--static`·`--transient`·`--pretty` 를 주면 고른 이름만 바꿉니다.[^hctl] 이름을 바꾸는 일은 권한이 필요합니다. `--no-ask-password` 는 권한이 없을 때 비밀번호를 묻지 않고 곧바로 실패하게 합니다.

```bash
# --no-ask-password: sudo 없이 시도하면 인증을 묻지 않고 실패한다
hostnamectl --no-ask-password hostname labhost    # Could not set static hostname: Access denied
# hostname NAME: static·transient(·pretty)를 모두 바꾼다
sudo hostnamectl hostname labhost
```

바꾼 이름이 `hostname`·`/etc/hostname`·static 이름 셋에 모두 반영됩니다. 부팅 때 읽는 `/etc/hostname` 까지 바뀌므로 재부팅 뒤에도 남습니다.

```bash
hostname    # labhost
cat /etc/hostname    # labhost
hostnamectl --static    # labhost
```

`--pretty` 는 pretty 이름만 바꿉니다. pretty 이름은 `/etc/machine-info` 의 `PRETTY_HOSTNAME` 에 저장되고 static 이름은 그대로입니다. 이 파일은 없어도 되는 파일이라 이름을 처음 정하는 순간 만들어집니다.[^minfo]

```bash
# --pretty: 공백과 괄호가 들어간 사람용 이름
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
# --transient: static 이 있으면 효과가 없다는 힌트
sudo hostnamectl --transient hostname tmp-name    # Hint: static hostname is already set, so the specified transient hostname will not be used.
hostnamectl --transient    # labhost
```

transient 이름을 바꾸는 효과는 커널의 호스트 이름을 직접 바꾸는 `hostname NAME` 으로 냅니다. 이 명령은 `sethostname(2)` 만 부르고 `/etc/hostname` 은 건드리지 않아 다음 재부팅 때까지만 유효합니다.[^hname] 그러면 transient 이름이 static 과 갈라져 `hostnamectl` 이 두 이름을 따로 보입니다.

```bash
# hostname NAME: 커널의 이름만 바꾼다 (재부팅까지)
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
# set-hostname: 옛 이름. 동작은 hostname NAME 과 같았다
sudo hostnamectl set-hostname labhost2
hostnamectl --static    # labhost2
```

### 그 밖의 항목과 JSON 출력

`hostnamectl` 은 이름 말고도 아이콘 이름·섀시 종류·배포 환경·위치를 읽고 씁니다. 같은 `명령 [값]` 모양이고 값을 주면 `/etc/machine-info` 에 저장됩니다.[^hctl] 이 VM 에서는 읽기만 했습니다.

```bash
# chassis: 섀시 종류. 가상 환경은 vm 이나 container
hostnamectl chassis    # container
# icon-name: 그래픽 도구가 이 호스트를 그릴 때 쓰는 아이콘 이름
hostnamectl icon-name    # computer-container
```

`--json=` 은 상태를 JSON 으로 찍습니다. 값은 `short`(한 줄)·`pretty`(들여쓰기)·`off` 입니다.[^hctl] 이 시트의 출력은 앞 몇 줄만 잘랐고 바로 앞에서 바꾼 이름 `labhost2` 가 그대로 보입니다.

```bash
# --json=pretty: 들여쓰기한 JSON. 앞 다섯 줄만
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
# --json=short: 공백 없는 한 줄 JSON. 앞 100자만
hostnamectl --json=short | cut -c1-100    # {"Hostname":"labhost2","StaticHostname":"labhost2","PrettyHostname":null,"DefaultHostname":"localhos
```

`-H`(`--host`)는 SSH 로 다른 호스트에, `-M`(`--machine`)은 로컬 컨테이너에 같은 명령을 보내는 옵션입니다.[^hctl] 이 시트에서는 실행하지 않았습니다.

### 원래 이름으로 되돌리기

위에서 바꾼 static 이름과 pretty 이름을 되돌립니다. pretty 이름을 빈 값으로 정하면 `/etc/machine-info` 의 그 줄이 사라지고 파일에 다른 줄이 없었으니 파일도 없어집니다.

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



## 8. 이 서버의 배포판과 커널을 세 줄로

> 처음 보는 서버에 들어가면 무슨 배포판에 어떤 커널이고 이름이 무엇인지부터 확인합니다. 한 줄 묶음 하나로 끝납니다.

서버에 처음 들어가면 배포판과 커널과 이름부터 묻습니다. `os-release` 를 읽는 줄, `uname -srm` 줄, `uname -n` 줄을 세미콜론으로 이으면 이 셋이 순서대로 나옵니다. 셋 다 최소 이미지에도 있는 도구라 `lsb_release` 나 `hostnamectl` 이 없어도 됩니다. 앞의 `( . /etc/os-release; … )` 서브셸은 변수가 밖으로 새지 않게 합니다.

```bash
# 배포판 이름·커널과 하드웨어·호스트 이름. Debian 12 컨테이너
( . /etc/os-release; echo "$PRETTY_NAME"; uname -srm; uname -n )
```

```bash
Debian GNU/Linux 12 (bookworm)
Linux 7.2.12-orbstack-00394-gbecdd6130068 aarch64
37d0d842ab53
```

```bash
# Rocky 컨테이너(호스트에서 실행): 같은 세 줄, 배포판 이름만 다르다
docker run --rm rockylinux:9 sh -c '. /etc/os-release; echo "$PRETTY_NAME"; uname -srm; uname -n'
```

```bash
Rocky Linux 9.3 (Blue Onyx)
Linux 7.2.12-orbstack-00394-gbecdd6130068 aarch64
8668051c5e98
```

```bash
# Ubuntu VM(호스트에서 실행): 커널 줄은 같고 호스트 이름만 다르다
orb -m ubuntu sh -c '. /etc/os-release; echo "$PRETTY_NAME"; uname -srm; uname -n'
```

```bash
Ubuntu 26.04.1 LTS
Linux 7.2.12-orbstack-00394-gbecdd6130068 aarch64
ubuntu
```

systemd 가 도는 서버라면 `hostnamectl` 한 번이 이 정보를 한 화면에 모읍니다. 필요한 줄만 `grep` 으로 고르면 됩니다.

```bash
# hostnamectl 의 Operating System 과 Kernel 줄 (처음 두 줄은 이 VM 의 읽기 권한 경고)
hostnamectl | grep -E "Operating System|Kernel"
```

```bash
Failed to query product UUID, ignoring: Access denied
Failed to query hardware serial, ignoring: Access denied
Operating System: Ubuntu 26.04.1 LTS
          Kernel: Linux 7.2.12-orbstack-00394-gbecdd6130068
```



## 관련 문서

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [하드웨어를 가리고 나면 무엇이 보일지를 정해야 한다](../../../book/learning-modern-linux/01-01.%ED%95%98%EB%93%9C%EC%9B%A8%EC%96%B4%EB%A5%BC%20%EA%B0%80%EB%A6%AC%EA%B3%A0%20%EB%82%98%EB%A9%B4%20%EB%AC%B4%EC%97%87%EC%9D%B4%20%EB%B3%B4%EC%9D%BC%EC%A7%80%EB%A5%BC%20%EC%A0%95%ED%95%B4%EC%95%BC%20%ED%95%9C%EB%8B%A4.md#명령-한-줄로-확인하는-방법) — 명령 한 줄이 시스템 콜 하나를 감싸는 예 (`id --user` 와 `getuid`)
- [같은 자원인데 보는 자리에 따라 답이 갈린다](../../../book/learning-modern-linux/01-01.%ED%95%98%EB%93%9C%EC%9B%A8%EC%96%B4%EB%A5%BC%20%EA%B0%80%EB%A6%AC%EA%B3%A0%20%EB%82%98%EB%A9%B4%20%EB%AC%B4%EC%97%87%EC%9D%B4%20%EB%B3%B4%EC%9D%BC%EC%A7%80%EB%A5%BC%20%EC%A0%95%ED%95%B4%EC%95%BC%20%ED%95%9C%EB%8B%A4.md#4-같은-자원인데-보는-자리에-따라-답이-갈린다) — 전역으로 보이는 값과 컨테이너 안에서 갈리는 값의 구분
- [커널은 전부를 하지만 운영체제는 아니다](../../../book/learning-modern-linux/02-01.%EC%BB%A4%EB%84%90%EC%9D%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%ED%95%98%EC%A7%80%EB%A7%8C%20%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EB%8A%94%20%EC%95%84%EB%8B%88%EB%8B%A4.md#무엇을-쓰고-있는지-확인하는-법) — `lscpu` 와 `uname -m` 으로 아키텍처 확인
- [dmidecode·lscpu 참조 시트](./dmidecode·lscpu.md) — 하드웨어와 CPU 정보
- [systemctl 참조 시트](../service/systemctl.md) — `hostnamectl` 이 속한 systemd 서비스 관리



## 참고 자료

- GNU coreutils 9.1 의 `uname --help` 원문 — Debian 12 컨테이너에서 2026-11-11 확인
- [uname(1) — Debian bookworm](https://manpages.debian.org/bookworm/coreutils/uname.1.en.html)
- [uname(2) — Debian bookworm](https://manpages.debian.org/bookworm/manpages-dev/uname.2.en.html)
- [proc(5) — Debian bookworm](https://manpages.debian.org/bookworm/manpages/proc.5.en.html)
- [os-release(5) — Debian bookworm](https://manpages.debian.org/bookworm/systemd/os-release.5.en.html)
- [lsb_release(1) — Debian bookworm](https://manpages.debian.org/bookworm/lsb-release/lsb_release.1.en.html)
- [hostnamectl(1) — Debian bookworm](https://manpages.debian.org/bookworm/systemd/hostnamectl.1.en.html)
- [hostname(1) — Debian bookworm](https://manpages.debian.org/bookworm/hostname/hostname.1.en.html)
- [hostname(5) — Debian bookworm](https://manpages.debian.org/bookworm/systemd/hostname.5.en.html)
- [machine-info(5) — Debian bookworm](https://manpages.debian.org/bookworm/systemd/machine-info.5.en.html)
- [bash(1) — Debian bookworm](https://manpages.debian.org/bookworm/bash/bash.1.en.html)
- [OrbStack Architecture](https://docs.orbstack.dev/architecture)

[^uname]: `man uname` (GNU coreutils 9.1) — "Print certain system information. With no OPTION, same as -s." "-a, --all print all information, in the following order, except omit -p and -i if unknown:" "-p, --processor print the processor type (non-portable)", "-i, --hardware-platform print the hardware platform (non-portable)", "-o, --operating-system print the operating system". https://manpages.debian.org/bookworm/coreutils/uname.1.en.html
[^uname2]: `man 2 uname` (Debian bookworm, manpages-dev) — "uname() returns system information in the structure pointed to by buf." 구조체 칸은 `sysname`("Operating system name (e.g., "Linux")"), `nodename`, `release`("Operating system release (e.g., "2.6.28")"), `version`("Operating system version"), `machine`("Hardware type identifier"). NOTES: "The kernel has the name, release, version, and supported machine type built in. Conversely, the nodename field is configured by the administrator to match the network (this is what the BSD historically calls the "hostname", and is set via sethostname(2))." https://manpages.debian.org/bookworm/manpages-dev/uname.2.en.html
[^proc]: `man 5 proc` (Debian bookworm) — "/proc/version This string identifies the kernel version that is currently running. It includes the contents of /proc/sys/kernel/ostype, /proc/sys/kernel/osrelease, and /proc/sys/kernel/version." "/proc/sys/kernel/ostype and /proc/sys/kernel/osrelease These files give substrings of /proc/version." "/proc/sys/kernel/hostname can be used to set the NIS/YP domainname and the hostname of your box in exactly the same way as the commands domainname(1) and hostname(1)". https://manpages.debian.org/bookworm/manpages/proc.5.en.html
[^osrel]: `man 5 os-release` (systemd 252, Debian bookworm) — "The format of os-release is a newline-separated list of environment-like shell-compatible variable assignments. It is possible to source the configuration from Bourne shell scripts, however, beyond mere variable assignments, no shell features are supported". "The file /etc/os-release takes precedence over /usr/lib/os-release. Applications should check for the former, and exclusively use its data if it exists, and only fall back to /usr/lib/os-release if it is missing. Applications should not read data from both files at the same time." "/etc/os-release should be a relative symlink to /usr/lib/os-release". ID= "A lower-case string ... identifying the operating system, excluding any version information and suitable for processing by scripts". ID_LIKE= "A space-separated list of operating system identifiers ... closely related to the local operating system in regards to packaging and programming interfaces". "Build scripts and similar should check this variable if they need to identify the local operating system and the value of ID= is not recognized." "For an operating system with "ID=ubuntu", an assignment of "ID_LIKE=debian" is appropriate." VERSION_ID= "excluding any OS name information or release code name, and suitable for processing by scripts", VERSION_CODENAME= "This field is optional and may not be implemented on all systems.", PRETTY_NAME= "A pretty operating system name in a format suitable for presentation to the user." https://manpages.debian.org/bookworm/systemd/os-release.5.en.html
[^lsb]: `man lsb_release` (lsb-release 12.0, Debian bookworm) — "This is a bare-bones version of the lsb_release command, implemented as a tiny POSIX shell script (less than 100 lines of commented code). Instead of using LSB packages, this version of lsb_release uses the information in /etc/os-release and /usr/lib/os-release. Nevertheless, the output of this version is byte-for-byte compatible with the Python-based version provided by Debian and its derivatives." "-v, --version Show LSB modules this system supports." "-i, --id Show distributor ID.", "-d, --description Show description of this distribution.", "-r, --release Show release number of this distribution.", "-c, --codename Show code name of this distribution.", "-a, --all Show all of the above information.", "-s, --short Show requested information in short format." https://manpages.debian.org/bookworm/lsb-release/lsb_release.1.en.html
[^hctl]: `man hostnamectl` (systemd 252 bookworm 원문과 VM 의 systemd 259.9 `man hostnamectl` 에서 같은 문장 확인) — "the high-level "pretty" hostname which might include all kinds of special characters (e.g. "Lennart's Laptop"), the "static" hostname which is the user-configured hostname (e.g. "lennarts-laptop"), and the transient hostname which is a fallback value received from network configuration (e.g. "node12345678"). If a static hostname is set to a valid value, then the transient hostname is not used." "status Show system hostname and related information. If no command is specified, this is the implied default." "hostname [NAME] If no argument is given, print the system hostname. If an optional argument NAME is provided then the command changes the system hostname to NAME. By default, this will alter the pretty, the static, and the transient hostname alike; however, if one or more of --static, --transient, --pretty are used, only the selected hostnames are changed." "The static and transient hostnames must each be either a single DNS label (a string composed of 7-bit ASCII lower-case characters and no spaces or dots, limited to the format allowed for DNS domain name labels), or a sequence of such labels separated by single dots that forms a valid DNS FQDN. The hostname must be at most 64 characters, which is a Linux limitation". 같은 문서의 COMMANDS 목록에 `set-hostname` 은 올라 있지 않습니다. icon-name·chassis·deployment·location 은 "If no argument is given, print ... If an optional argument ... is provided then the command changes ...". "--no-ask-password Do not query the user for authentication for privileged operations." "--static, --transient, --pretty If status is invoked (or no explicit command is given) and one of these switches is specified, hostnamectl will print out just this selected hostname." "-H, --host= Execute the operation remotely.", "-M, --machine= Execute operation on a local container.", "--json=MODE ... "short" ... "pretty" ... "off"". https://manpages.debian.org/bookworm/systemd/hostnamectl.1.en.html
[^hname]: `man hostname` (hostname 3.23, Debian bookworm) — "hostname will print the name of the system as returned by the gethostname(2) function." "Note, that this is effective only until the next reboot. Edit /etc/hostname for permanent change." "-s, --short Display the short host name. This is the host name cut at the first dot." "-f, --fqdn, --long Display the FQDN (Fully Qualified Domain Name)." "-d, --domain Display the name of the DNS domain." "Therefore avoid using hostname --fqdn, hostname --domain and dnsdomainname. hostname --ip-address is subject to the same limitations so it should be avoided as well." https://manpages.debian.org/bookworm/hostname/hostname.1.en.html
[^hostname5]: `man 5 hostname` (systemd 252, Debian bookworm) — "The /etc/hostname file configures the name of the local system. Unless overridden as described in the next section, systemd(1) will set this hostname during boot using the sethostname(2) system call." "Note that systemd-hostnamed.service(8) gives higher priority to the static hostname, so the transient hostname will only be used if the static hostname is not configured." https://manpages.debian.org/bookworm/systemd/hostname.5.en.html
[^minfo]: `man 5 machine-info` (systemd 252, Debian bookworm) — "PRETTY_HOSTNAME= A pretty human-readable UTF-8 machine identifier string." "It is thus completely fine for this file to not be present. You may use hostnamectl(1) to change the settings of this file from the command line." https://manpages.debian.org/bookworm/systemd/machine-info.5.en.html
[^dot]: `man bash` (bash 5.2.15, Debian bookworm) — "If filename does not contain a slash, filenames in PATH are used to find the directory containing filename, but filename does not need to be executable." "When bash is not in posix mode, it searches the current directory if no file is found in PATH." Debian 12 컨테이너에서 `sh -c ". rocky.os-release"`(dash)는 `.: rocky.os-release: not found`, `bash --posix -c ". rocky.os-release"` 는 `.: rocky.os-release: file not found` 로 실패하고, `bash -c ". rocky.os-release"` 는 현재 폴더의 파일을 읽어 성공하는 것을 확인했습니다. https://manpages.debian.org/bookworm/bash/bash.1.en.html
[^orb]: OrbStack 문서 Architecture — "OrbStack uses a lightweight Linux virtual machine with a shared kernel to minimize overhead and save resources" "OrbStack runs full-blown Linux machines that work almost exactly like traditional virtual machines, all while sharing the same kernel." https://docs.orbstack.dev/architecture
