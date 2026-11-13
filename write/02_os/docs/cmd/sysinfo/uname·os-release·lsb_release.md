---
title: uname·os-release·lsb_release 참조 시트
tags: [linux, cheatsheet, uname, os-release, lsb_release, hostnamectl, hostname, sysinfo, cli, reference]
status: draft
source:
  - GNU coreutils 9.1 uname(1) (Debian 12 `uname --help` 원문, manpages.debian.org bookworm), uname(2)·gethostname(2)·proc(5) (bookworm)
  - systemd 252 os-release(5)·hostname(5)·machine-info(5)·hostnamectl(1) (bookworm), OrbStack VM 의 systemd 259.9 `man hostnamectl`
  - lsb-release 12.0 lsb_release(1), hostname 3.23 hostname(1) (bookworm)
related:
  - ./hostnamectl·hostname.md
  - ../README.md
updated: 2026-11-13
---

# uname·os-release·lsb_release 참조 시트

---

> 이 서버가 어떤 커널과 배포판인지를 `uname`·`/etc/os-release`·`lsb_release` 로 확인하는 방법을, 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `uname` 으로 커널을, `os-release` 파일과 `lsb_release` 로 배포판을 묻습니다.

`uname` 은 coreutils 의 외부 바이너리이고 `lsb_release` 는 lsb-release 패키지의 셸 스크립트입니다. `os-release` 는 명령이 아니라 배포판 패키지(Debian 은 base-files)가 설치하는 파일입니다.

이 시트는 Debian 12 컨테이너(coreutils 9.1, lsb-release 12.0)로 실측했습니다. 최소 이미지에는 `lsb_release` 가 없어 처음 부르면 `not found` 가 나옵니다. macOS 에는 `/etc/os-release`·`lsb_release`·`hostnamectl` 이 없고, BSD `uname` 은 `-i` 를 받지 않아 `uname: illegal option -- i` 를 냅니다.

호스트 이름을 읽고 바꾸는 `hostnamectl`·`hostname` 은 [hostnamectl·hostname 호스트 이름 다루기 시트](./hostnamectl·hostname.md)에서 이어 다룹니다.



## 핵심 문법

> `uname` 은 옵션으로 칸을 고르고, `os-release` 는 파일이라 셸로 읽고, `lsb_release` 는 옵션으로 항목을 고릅니다.

```bash
# 호출 형태. uname (uname --help 의 첫 줄)
uname [OPTION]...

# 호출 형태. lsb_release (lsb_release --help 의 첫 줄)
lsb_release [options]

# os-release 는 명령이 아니라 파일이다. 셸이 읽거나 cat 으로 본다
# (배포판 이름과 버전 확인, 스크립트에서 배포판 읽기와 분기)
. /etc/os-release
cat /etc/os-release

# 커널의 칸을 옵션으로 고른다 (커널 이름과 하드웨어 확인, uname)
uname -s
uname -r
uname -m
uname -a

# 파일에서 키 몇 개만 고른다 (배포판 이름과 버전 확인, os-release)
grep -E "^(ID|VERSION_ID)=" /etc/os-release

# 파일을 변수로 읽어 쓴다 (스크립트에서 배포판 읽기와 분기)
( . /etc/os-release; echo "$PRETTY_NAME" )

# 항목을 한꺼번에, 값만 꺼낸다 (lsb_release 로 한 항목씩 꺼내기)
lsb_release -a
lsb_release -s -d

# 배포판과 커널과 이름을 한 줄 묶음으로 본다 (이 서버의 배포판과 커널을 세 줄로)
( . /etc/os-release; echo "$PRETTY_NAME"; uname -srm; uname -n )
```



## 종료 코드

> `uname` 은 성공하면 0, 실패하면 1 을 돌려주고 `lsb_release` 는 모르는 옵션에 2 를 돌려줍니다.

`uname` 은 매뉴얼이 성공은 0, 실패는 0 이 아닌 값이라고만 적고, `lsb_release` 의 man 에는 종료 코드 절이 없어 실측한 값만 싣습니다.[^uname-exit][^lsb-exit] `lsb_release` 는 「실습 준비」 에서 설치한 뒤 돌립니다.

```bash
# uname
# 0  성공
# 1  모르는 옵션이나 남는 인자를 줬을 때

# 인자 없이 부르면 커널 이름을 찍고 0 으로 끝난다
uname; echo $?    # Linux / 0

# 모르는 긴 옵션과 짧은 옵션은 오류를 내고 1 로 끝난다
# 2>&1 은 오류 메시지를 표준 출력에 합쳐 종료 코드와 함께 보인다
uname --bad 2>&1; echo $?    # uname: unrecognized option '--bad' / Try 'uname --help' for more information. / 1
uname -z 2>&1; echo $?    # uname: invalid option -- 'z' / Try 'uname --help' for more information. / 1

# 남는 인자를 줘도 1 이다
uname extra 2>&1; echo $?    # uname: extra operand 'extra' / Try 'uname --help' for more information. / 1
```

```bash
# lsb_release
# 0  정상 종료
# 2  모르는 옵션

# 출력은 버리고 종료 코드만 본다. 정상이라 0 이다
#   -a   네 항목을 모두 찍는다 (--all)
lsb_release -a >/dev/null 2>&1; echo $?    # 0

# 모르는 옵션은 오류를 내고 2 로 끝난다
lsb_release --bad 2>&1; echo $?    # lsb_release: unrecognized option '--bad' / 2

# 최소 이미지에는 lsb_release 가 없다. 패키지 lsb-release 를 설치해야 한다 (호스트에서 실행)
docker run --rm debian:12 sh -c 'lsb_release -a'    # sh: 1: lsb_release: not found
docker run --rm rockylinux:9 sh -c 'lsb_release -a'    # sh: line 1: lsb_release: command not found
```

위 블록들의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션만 씁니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 `lsb_release` 가 설치되고 이 시트의 예가 쓰는 파일이 모두 만들어집니다.

예는 `docker run -it --rm debian:12` 안에서 root 로 실행했고, `lsb_release` 는 이 컨테이너에 처음부터 없어서 준비 블록이 설치합니다. `docker run --rm rockylinux:9` 나 `orb -m ubuntu` 처럼 `docker` 와 `orb` 를 부르는 예에는 "호스트에서 실행" 이라고 적었으니, 둘이 있는 호스트의 터미널에서 칩니다.

```bash
# lsb_release 를 설치한다. 최소 이미지에는 없다 (lsb_release 로 한 항목씩 꺼내기)
apt-get update -qq >/dev/null 2>&1; \
  apt-get install -y -qq lsb-release >/dev/null 2>&1

# 실습 폴더로 옮긴다. 아래 두 파일이 여기에 생긴다
mkdir -p ~/cmd-lab/uname && cd ~/cmd-lab/uname

# distro.sh: os-release 파일을 읽어 ID 와 ID_LIKE 로 계열을 나누는 짧은 스크립트다
# 인자가 없으면 /etc/os-release 를 읽는다 (스크립트에서 배포판 읽기와 분기)
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

# rocky.os-release: Rocky Linux 9 컨테이너의 /etc/os-release 를 그대로 옮긴 파일이다
# Rocky 컨테이너가 없어도 distro.sh 의 분기를 시험한다 (스크립트에서 배포판 읽기와 분기)
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

`uname -n`·`/proc/sys/kernel/hostname` 의 컨테이너 이름(12자리 16진수 값)은 컨테이너를 만들 때마다 달라지고, 커널 릴리스와 빌드 시각은 쓰는 OrbStack 의 커널을 따릅니다. Rocky 컨테이너의 판(`9.3`)도 이 기기에 내려받아 둔 이미지의 값이라 다를 수 있지만 형식은 같습니다.

### 커널 이름과 하드웨어 확인, uname

> `uname` 은 커널이 알고 있는 이름 다섯 칸(운영체제·호스트·릴리스·빌드 버전·하드웨어)을 옵션 하나에 한 칸씩 꺼냅니다.

`uname` 은 `uname(2)` 시스템 콜이 채워 주는 구조체의 칸을 찍습니다. 칸은 운영체제 이름 `sysname`, 네트워크 노드 이름 `nodename`, 릴리스 `release`, 버전 `version`, 하드웨어 종류 `machine` 입니다.[^uname2]

```bash
# 칸마다 옵션 하나로 꺼낸다. 이 컨테이너는 커널 Linux, 하드웨어 aarch64 다
#   (옵션 없음)  -s 와 같다
#   -s   커널 이름 (--kernel-name)
#   -n   네트워크에서 쓰는 호스트 이름. 컨테이너에서는 컨테이너 ID (--nodename)
#   -r   커널 릴리스. 버전 번호와 빌더가 붙인 꼬리표 (--kernel-release)
#   -v   커널 빌드 문자열. 빌드 번호·선점 모델·빌드 시각 (--kernel-version)
#   -m   하드웨어 이름. x86_64 나 aarch64 (--machine)
uname    # Linux
uname -s    # Linux
uname -n    # 37d0d842ab53
uname -r    # 7.2.12-orbstack-00394-gbecdd6130068
uname -v    # #1 SMP PREEMPT Thu Oct 22 22:17:17 UTC 2026
uname -m    # aarch64
```

이 Debian 컨테이너에서는 `-p`·`-i` 의 값을 알아내지 못해 `unknown` 을 찍고, man 은 둘을 "non-portable" 이라고 적습니다.[^uname]

```bash
# 값을 알아내지 못하면 unknown 이 나온다. -o 는 커널 이름이 아니라 GNU/Linux 다
#   -p   프로세서 종류 (--processor)
#   -i   하드웨어 플랫폼 (--hardware-platform)
#   -o   운영체제 이름 (--operating-system)
uname -p    # unknown
uname -i    # unknown
uname -o    # GNU/Linux
```

Debian 에서는 `-a` 에서 `-p`·`-i` 가 빠지고, 같은 하드웨어의 Rocky 컨테이너는 둘 다 알아내 `aarch64` 를 두 번 더 붙입니다.

```bash
# 이 컨테이너는 -p·-i 가 unknown 이라 두 칸이 빠진 채 한 줄로 나온다
#   -a   칸을 정해진 순서로 모두. -p·-i 가 unknown 이면 뺀다 (--all)
uname -a    # Linux 37d0d842ab53 7.2.12-orbstack-00394-gbecdd6130068 #1 SMP PREEMPT Thu Oct 22 22:17:17 UTC 2026 aarch64 GNU/Linux

# Rocky 컨테이너(호스트에서 실행): -p·-i 가 aarch64 로 나와 -a 에 두 칸이 더 붙는다
docker run --rm rockylinux:9 uname -a    # Linux 882b3d4940aa 7.2.12-orbstack-00394-gbecdd6130068 #1 SMP PREEMPT Thu Oct 22 22:17:17 UTC 2026 aarch64 aarch64 aarch64 GNU/Linux
docker run --rm rockylinux:9 uname -p -i    # aarch64 aarch64
```

배포판에 따라 `-p`·`-i` 값이 갈리므로 스크립트에서 하드웨어를 가릴 때는 `-m` 을 씁니다.

```bash
# -m -s 로 줘도 커널 이름(-s)이 앞에 온다
# 옵션을 여러 개 주면 인자 순서와 상관없이 -s -n -r -v -m 의 고정 순서로 찍는다
uname -m -s    # Linux aarch64

# 자주 쓰는 묶음: 커널 이름과 릴리스와 하드웨어를 한 줄로
uname -srm    # Linux 7.2.12-orbstack-00394-gbecdd6130068 aarch64
```

`uname -m` 의 이름은 패키지 관리자의 아키텍처 이름과 다를 수 있어, 파일을 내려받는 스크립트에서는 `aarch64` 와 `arm64` 를 맞바꿔야 합니다.

CPU 모델이나 코어 수는 `uname` 이 알려 주지 않으므로 `lscpu` 를 쓰고, 그 확인은 [커널은 전부를 하지만 운영체제는 아니다 노트의 「무엇을 쓰고 있는지 확인하는 법」](../../../book/learning-modern-linux/02-01.%EC%BB%A4%EB%84%90%EC%9D%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%ED%95%98%EC%A7%80%EB%A7%8C%20%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EB%8A%94%20%EC%95%84%EB%8B%88%EB%8B%A4.md#무엇을-쓰고-있는지-확인하는-법)에 있습니다.

```bash
# dpkg 의 아키텍처 이름: 같은 컨테이너에서 uname -m 의 aarch64 와 같은 하드웨어를 arm64 로 부른다
#   --print-architecture   dpkg 의 아키텍처 이름을 찍는다
dpkg --print-architecture    # arm64
```

### 배포판 이름과 버전 확인, os-release

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

자주 쓰는 키 다섯 개의 뜻은 man 을 따랐습니다.[^osrel]

```bash
# 다섯 키만 골라 본다 (Debian 12 컨테이너). ID_LIKE 는 이 컨테이너에 없다
#   ID                스크립트가 처리하기 좋은 소문자 식별자
#   ID_LIKE           이 배포판이 파생된 가까운 배포판의 ID 목록. 선택 키라 없는 배포판이 있다
#   VERSION_ID        코드명 없이 버전만 담은 값
#   VERSION_CODENAME  릴리스 코드명. 선택 키라 없는 배포판이 있다
#   PRETTY_NAME       사람에게 보여 주는 이름
grep \
  -E \
  "^(ID|ID_LIKE|VERSION_ID|VERSION_CODENAME|PRETTY_NAME)=" \
  /etc/os-release
```

```bash
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
VERSION_ID="12"
VERSION_CODENAME=bookworm
ID=debian
```

```bash
# Rocky Linux 9 컨테이너(호스트에서 실행): ID_LIKE 가 있고 VERSION_CODENAME 이 없다
docker run \
  --rm \
  rockylinux:9 \
  grep \
    -E \
    '^(ID|ID_LIKE|VERSION_ID|VERSION_CODENAME|PRETTY_NAME)=' \
    /etc/os-release
```

```bash
ID="rocky"
ID_LIKE="rhel centos fedora"
VERSION_ID="9.3"
PRETTY_NAME="Rocky Linux 9.3 (Blue Onyx)"
```

```bash
# Ubuntu 26.04 VM(호스트에서 실행): ID 는 ubuntu, ID_LIKE 는 debian
orb \
  -m ubuntu \
  grep \
    -E \
    '^(ID|ID_LIKE|VERSION_ID|VERSION_CODENAME|PRETTY_NAME)=' \
    /etc/os-release
```

```bash
PRETTY_NAME="Ubuntu 26.04.1 LTS"
VERSION_ID="26.04"
VERSION_CODENAME=resolute
ID=ubuntu
ID_LIKE=debian
```

Ubuntu 의 `ID_LIKE=debian` 은 "Debian 과 패키지와 프로그래밍 인터페이스가 가깝다" 는 선언입니다. 스크립트가 `ID` 를 모르는 배포판을 만났을 때 `ID_LIKE` 로 가까운 쪽을 따라가라고 만든 키입니다.[^osrel]

### 스크립트에서 배포판 읽기와 분기

> `os-release` 는 셸이 그대로 읽을 수 있는 형식이라, `grep` 으로 값을 자르지 않고 파일을 `.` 로 읽어 변수로 씁니다.

`os-release` 는 변수 대입만 담도록 정해져 있어 셸에서 `source` 해도 되고, 변수 확장 같은 셸 기능은 지원하지 않는다고 man 이 적습니다.[^osrel]

```bash
# grep+cut 으로 자르면 따옴표가 값에 그대로 붙는다
#   cut -d=   칸을 가르는 글자를 = 로 정한다 (--delimiter)
#   cut -f2   둘째 칸을 고른다 (--fields)
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

준비 블록의 `distro.sh` 는 `ID` 와 `ID_LIKE` 를 앞뒤에 공백을 붙인 한 문자열로 만들어 `case` 로 계열을 가립니다. 앞뒤 공백 덕에 낱말을 통째로만 맞추므로 `debian-like` 같은 부분 문자열에는 걸리지 않습니다.

`distro.sh` 는 `#!/bin/sh` 라서 Debian 에서는 dash 가 읽는데, dash 의 `.` 는 `/` 가 없는 이름을 `PATH` 에서만 찾으므로 현재 폴더의 파일에는 `./` 를 붙입니다. bash 는 보통 모드에서 `PATH` 에 없으면 현재 폴더도 찾지만 `--posix` 모드에서는 dash 처럼 실패합니다.[^dot]

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

### lsb_release 로 한 항목씩 꺼내기

> `lsb_release` 는 같은 정보를 `Distributor ID`·`Description`·`Release`·`Codename` 네 항목으로 나눠 찍는 옛 호환 명령입니다.

Debian 의 `lsb_release` 는 LSB 패키지 대신 `os-release` 를 읽는 짧은 POSIX 셸 스크립트이고, 옛 Python 판과 출력이 바이트까지 같다고 man 이 적습니다.[^lsb]

Debian 과 Rocky 의 최소 이미지에는 이 명령이 없고, 그 실패는 「종료 코드」 에 있습니다.

```bash
# 네 항목을 모두 찍는다. 항목 이름과 값 사이는 탭이다
lsb_release -a
```

```bash
Distributor ID:	Debian
Description:	Debian GNU/Linux 12 (bookworm)
Release:	12
Codename:	bookworm
```

```bash
# -a 를 뺀 네 옵션은 항목 하나씩 찍는다
#   -i   배포판 식별자 (--id)
#   -d   사람이 읽는 이름과 버전 (--description)
#   -r   릴리스 번호 (--release)
#   -c   릴리스 코드명 (--codename)
lsb_release -i    # Distributor ID:	Debian
lsb_release -d    # Description:	Debian GNU/Linux 12 (bookworm)
lsb_release -r    # Release:	12
lsb_release -c    # Codename:	bookworm
```

항목 이름이 붙으면 변수에 담기 전에 잘라야 하므로, 스크립트에서는 `-s` 로 값만 받습니다.[^lsb]

```bash
# 값만 찍는다
#   -s   항목 이름을 떼고 값만 찍는다 (--short)
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

이 최소 판은 지원하는 LSB 모듈이 없어 `-v` 는 아무것도 찍지 않고 정상 종료합니다.[^lsb]

```bash
# LSB 모듈 목록. 이 최소 판은 출력이 없다
#   -v   이 시스템이 지원하는 LSB 모듈을 보여 준다 (--version)
lsb_release -v
```

```bash
# 옵션 목록
#   -h   도움말과 옵션 목록 (--help)
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
( . /etc/os-release; \
  [ "$(lsb_release -sd)" = "$PRETTY_NAME" ] \
  && [ "$(lsb_release -sc)" = "$VERSION_CODENAME" ] \
  && [ "$(lsb_release -sr)" = "$VERSION_ID" ] \
  && echo "os-release 값과 같다" )
# os-release 값과 같다
```

새 스크립트는 `lsb_release` 를 부르지 말고 `/etc/os-release` 를 읽는 편이 낫습니다. `lsb_release` 는 패키지를 따로 설치해야 하고 Rocky 같은 이미지에는 처음부터 없기 때문입니다.

### 이 서버의 배포판과 커널을 세 줄로

> 배포판 이름, 커널과 하드웨어, 호스트 이름을 한 줄 묶음 하나로 확인합니다.

`os-release` 를 읽는 줄, `uname -srm` 줄, `uname -n` 줄을 세미콜론으로 이으면 배포판과 커널과 이름이 순서대로 나옵니다. 셋 다 최소 이미지에도 있어 `lsb_release` 나 `hostnamectl` 이 없어도 됩니다.

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
docker run \
  --rm \
  rockylinux:9 \
  sh -c '. /etc/os-release; echo "$PRETTY_NAME"; uname -srm; uname -n'
```

```bash
Rocky Linux 9.3 (Blue Onyx)
Linux 7.2.12-orbstack-00394-gbecdd6130068 aarch64
8668051c5e98
```

```bash
# Ubuntu VM(호스트에서 실행): 커널 줄은 같고 호스트 이름만 다르다
orb \
  -m ubuntu \
  sh -c '. /etc/os-release; echo "$PRETTY_NAME"; uname -srm; uname -n'
```

```bash
Ubuntu 26.04.1 LTS
Linux 7.2.12-orbstack-00394-gbecdd6130068 aarch64
ubuntu
```

systemd 가 도는 서버라면 `hostnamectl` 한 번이 같은 정보를 한 화면에 모읍니다. 그 줄만 고르는 예는 [호스트 이름 다루기 시트](./hostnamectl·hostname.md)의 「hostnamectl 로 배포판과 커널 줄 고르기」 에 있습니다.



## 주의사항과 동작 원리

> `uname -r` 과 `-v` 는 쓰임이 다르고, 컨테이너의 `uname` 은 호스트가 돌리는 커널을 보이며, `/etc/os-release` 는 링크입니다.

### 릴리스와 빌드 문자열 구분

> `uname -r` 은 커널 버전을 알리는 짧은 이름이고, `uname -v` 는 그 빌드가 언제 어떻게 만들어졌는지를 적은 문자열입니다.

`/proc/version` 은 지금 돌고 있는 커널을 설명하는 한 줄로, `/proc/sys/kernel/` 의 `ostype`·`osrelease`·`version` 을 이어 붙인 것입니다.[^proc]

컴파일러 정보까지 붙은 긴 한 줄이라 앞 세 단어와 `#` 로 시작하는 뒤쪽만 나눠 봅니다.

```bash
# 앞쪽: 커널 이름·"version"·릴리스. uname -r 과 같은 값이 들어 있다
cut -d" " -f1-3 /proc/version    # Linux version 7.2.12-orbstack-00394-gbecdd6130068

# # 로 시작하는 뒤쪽: 빌드 번호·선점 모델·빌드 시각
#   grep -o   줄 전체가 아니라 일치한 부분만 찍는다 (--only-matching)
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

# hostname: uname -n 과 같은 값
# (호스트 이름 다루기 시트의 「hostname 명령과 이름이 저장된 곳」 에서 hostnamectl 과 함께 다시 본다)
cat /proc/sys/kernel/hostname    # 37d0d842ab53

# 두 값이 정말 같은지 문자열로 비교한다
[ "$(uname -r)" = "$(cat /proc/sys/kernel/osrelease)" ] \
  && echo "uname -r 과 osrelease 가 같다"
# uname -r 과 osrelease 가 같다
[ "$(uname -v)" = "$(cat /proc/sys/kernel/version)" ] \
  && echo "uname -v 와 version 이 같다"
# uname -v 와 version 이 같다
```

커널 버전을 비교하는 스크립트는 `-r` 을 씁니다. `-v` 에는 빌드 번호와 시각이 들어 있어서 버전 순서를 비교하는 값이 아닙니다.

### 컨테이너와 VM 이 보는 같은 커널

> 컨테이너 안의 `uname -r` 은 이미지의 배포판이 아니라 그 컨테이너를 돌리는 Linux 커널(맥에서는 OrbStack 이 띄운 Linux VM 의 커널)의 값입니다.

`uname` 이 읽는 릴리스·버전·하드웨어는 커널에 들어 있는 값이고,[^uname2] 컨테이너는 이미지에서 배포판의 파일과 프로그램만 가져오므로 배포판이 달라도 커널 값은 같습니다. OrbStack 에서는 가벼운 Linux VM 하나가 커널을 쥐고 `ubuntu` 같은 머신이 그 커널을 나눠 씁니다.[^orb] `hostnamectl` 이 이 머신을 `Virtualization: lxc` 로 보이는 것도 그래서입니다([hostnamectl·hostname 호스트 이름 다루기 시트](./hostnamectl·hostname.md)의 「상태 읽기」).

```bash
# 호스트(macOS)의 커널은 Darwin 이고 나머지 셋은 같은 Linux 커널을 보인다
uname -sr    # Darwin 25.6.0

# Debian 컨테이너가 보는 커널
docker run --rm debian:12 uname -sr    # Linux 7.2.12-orbstack-00394-gbecdd6130068

# Rocky 컨테이너가 보는 커널. 배포판이 달라도 같은 값
docker run --rm rockylinux:9 uname -sr    # Linux 7.2.12-orbstack-00394-gbecdd6130068

# OrbStack VM 이 보는 커널
orb -m ubuntu uname -sr    # Linux 7.2.12-orbstack-00394-gbecdd6130068
```

그래서 컨테이너 안에서 `uname -r` 의 값을 배포판 이미지의 속성으로 읽으면 안 되고, 배포판은 「배포판 이름과 버전 확인, os-release」 의 `/etc/os-release` 로 확인합니다. 전역으로 보이는 값과 가려지는 값의 구분은 [노트의 「같은 자원인데 보는 자리에 따라 답이 갈린다」](../../../book/learning-modern-linux/01-01.%ED%95%98%EB%93%9C%EC%9B%A8%EC%96%B4%EB%A5%BC%20%EA%B0%80%EB%A6%AC%EA%B3%A0%20%EB%82%98%EB%A9%B4%20%EB%AC%B4%EC%97%87%EC%9D%B4%20%EB%B3%B4%EC%9D%BC%EC%A7%80%EB%A5%BC%20%EC%A0%95%ED%95%B4%EC%95%BC%20%ED%95%9C%EB%8B%A4.md#4-같은-자원인데-보는-자리에-따라-답이-갈린다)에서 다룹니다.

### /etc 와 /usr/lib 의 두 파일

> 읽는 쪽은 `/etc/os-release` 를 먼저 보고 없을 때만 `/usr/lib/os-release` 로 물러납니다.

`/usr/lib/os-release` 는 배포판이 설치하는 원본이고 `/etc/os-release` 는 여기를 가리키는 상대 심볼릭 링크로 두는 것이 권장이며, 둘을 동시에 읽어 합치면 안 됩니다.[^osrel]

```bash
# 링크 모양 확인: /etc 쪽이 ../usr/lib/os-release 를 가리킨다
#   ls -l   긴 형식으로 보인다
ls -l /etc/os-release /usr/lib/os-release
```

```bash
lrwxrwxrwx 1 root root  21 Jul  2 19:05 /etc/os-release -> ../usr/lib/os-release
-rw-r--r-- 1 root root 267 Jul  2 19:05 /usr/lib/os-release
```

```bash
# 링크를 끝까지 따라간 실제 파일
#   readlink -f   링크를 끝까지 따라간 경로를 찍는다 (--canonicalize)
readlink -f /etc/os-release    # /usr/lib/os-release

# 두 경로의 내용이 같은지
cmp /etc/os-release /usr/lib/os-release && echo 내용이 같다    # 내용이 같다
```



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [hostnamectl·hostname 호스트 이름 다루기 시트](./hostnamectl·hostname.md) — 호스트 이름을 읽고 바꾸는 `hostnamectl`·`hostname`
- [하드웨어를 가리고 나면 무엇이 보일지를 정해야 한다](../../../book/learning-modern-linux/01-01.%ED%95%98%EB%93%9C%EC%9B%A8%EC%96%B4%EB%A5%BC%20%EA%B0%80%EB%A6%AC%EA%B3%A0%20%EB%82%98%EB%A9%B4%20%EB%AC%B4%EC%97%87%EC%9D%B4%20%EB%B3%B4%EC%9D%BC%EC%A7%80%EB%A5%BC%20%EC%A0%95%ED%95%B4%EC%95%BC%20%ED%95%9C%EB%8B%A4.md#명령-한-줄로-확인하는-방법) — 명령 한 줄이 시스템 콜 하나를 감싸는 예 (`id --user` 와 `getuid`)
- [같은 자원인데 보는 자리에 따라 답이 갈린다](../../../book/learning-modern-linux/01-01.%ED%95%98%EB%93%9C%EC%9B%A8%EC%96%B4%EB%A5%BC%20%EA%B0%80%EB%A6%AC%EA%B3%A0%20%EB%82%98%EB%A9%B4%20%EB%AC%B4%EC%97%87%EC%9D%B4%20%EB%B3%B4%EC%9D%BC%EC%A7%80%EB%A5%BC%20%EC%A0%95%ED%95%B4%EC%95%BC%20%ED%95%9C%EB%8B%A4.md#4-같은-자원인데-보는-자리에-따라-답이-갈린다) — 전역으로 보이는 값과 컨테이너 안에서 갈리는 값의 구분
- [커널은 전부를 하지만 운영체제는 아니다](../../../book/learning-modern-linux/02-01.%EC%BB%A4%EB%84%90%EC%9D%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%ED%95%98%EC%A7%80%EB%A7%8C%20%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EB%8A%94%20%EC%95%84%EB%8B%88%EB%8B%A4.md#무엇을-쓰고-있는지-확인하는-법) — `lscpu` 와 `uname -m` 으로 아키텍처 확인
- [lscpu·nproc 참조 시트](./lscpu·nproc.md) — 하드웨어와 CPU 정보



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- GNU coreutils 9.1 의 `uname --help` 원문 — Debian 12 컨테이너에서 2026-11-13 확인
- GNU coreutils 9.1 의 `info coreutils 'uname invocation'` 원문 — Debian 12 컨테이너에서 2026-11-13 확인 (gnu.org 는 이 환경에서 열리지 않아 인용문 존재를 컨테이너 원문으로 확인)
- [uname(1) — Debian bookworm](https://manpages.debian.org/bookworm/coreutils/uname.1.en.html)
- [uname(2) — Debian bookworm](https://manpages.debian.org/bookworm/manpages-dev/uname.2.en.html)
- [proc(5) — Debian bookworm](https://manpages.debian.org/bookworm/manpages/proc.5.en.html)
- [os-release(5) — Debian bookworm](https://manpages.debian.org/bookworm/systemd/os-release.5.en.html)
- [lsb_release(1) — Debian bookworm](https://manpages.debian.org/bookworm/lsb-release/lsb_release.1.en.html)
- [bash(1) — Debian bookworm](https://manpages.debian.org/bookworm/bash/bash.1.en.html)
- [OrbStack Architecture](https://docs.orbstack.dev/architecture)

[^uname]: `man uname` (GNU coreutils 9.1) — "Print certain system information. With no OPTION, same as -s." "-a, --all print all information, in the following order, except omit -p and -i if unknown:" "-p, --processor print the processor type (non-portable)", "-i, --hardware-platform print the hardware platform (non-portable)", "-o, --operating-system print the operating system". https://manpages.debian.org/bookworm/coreutils/uname.1.en.html
[^uname2]: `man 2 uname` (Debian bookworm, manpages-dev) — "uname() returns system information in the structure pointed to by buf." 구조체 칸은 `sysname`("Operating system name (e.g., "Linux")"), `nodename`, `release`("Operating system release (e.g., "2.6.28")"), `version`("Operating system version"), `machine`("Hardware type identifier"). NOTES: "The kernel has the name, release, version, and supported machine type built in. Conversely, the nodename field is configured by the administrator to match the network (this is what the BSD historically calls the "hostname", and is set via sethostname(2))." https://manpages.debian.org/bookworm/manpages-dev/uname.2.en.html
[^proc]: `man 5 proc` (Debian bookworm) — "/proc/version This string identifies the kernel version that is currently running. It includes the contents of /proc/sys/kernel/ostype, /proc/sys/kernel/osrelease, and /proc/sys/kernel/version." "/proc/sys/kernel/ostype and /proc/sys/kernel/osrelease These files give substrings of /proc/version." "/proc/sys/kernel/hostname can be used to set the NIS/YP domainname and the hostname of your box in exactly the same way as the commands domainname(1) and hostname(1)". https://manpages.debian.org/bookworm/manpages/proc.5.en.html
[^osrel]: `man 5 os-release` (systemd 252, Debian bookworm) — "The format of os-release is a newline-separated list of environment-like shell-compatible variable assignments. It is possible to source the configuration from Bourne shell scripts, however, beyond mere variable assignments, no shell features are supported". "The file /etc/os-release takes precedence over /usr/lib/os-release. Applications should check for the former, and exclusively use its data if it exists, and only fall back to /usr/lib/os-release if it is missing. Applications should not read data from both files at the same time." "/etc/os-release should be a relative symlink to /usr/lib/os-release". ID= "A lower-case string ... identifying the operating system, excluding any version information and suitable for processing by scripts". ID_LIKE= "A space-separated list of operating system identifiers ... closely related to the local operating system in regards to packaging and programming interfaces". "Build scripts and similar should check this variable if they need to identify the local operating system and the value of ID= is not recognized." "For an operating system with "ID=ubuntu", an assignment of "ID_LIKE=debian" is appropriate." VERSION_ID= "excluding any OS name information or release code name, and suitable for processing by scripts", VERSION_CODENAME= "This field is optional and may not be implemented on all systems.", PRETTY_NAME= "A pretty operating system name in a format suitable for presentation to the user." https://manpages.debian.org/bookworm/systemd/os-release.5.en.html
[^lsb]: `man lsb_release` (lsb-release 12.0, Debian bookworm) — "This is a bare-bones version of the lsb_release command, implemented as a tiny POSIX shell script (less than 100 lines of commented code). Instead of using LSB packages, this version of lsb_release uses the information in /etc/os-release and /usr/lib/os-release. Nevertheless, the output of this version is byte-for-byte compatible with the Python-based version provided by Debian and its derivatives." "-v, --version Show LSB modules this system supports." "-i, --id Show distributor ID.", "-d, --description Show description of this distribution.", "-r, --release Show release number of this distribution.", "-c, --codename Show code name of this distribution.", "-a, --all Show all of the above information.", "-s, --short Show requested information in short format." https://manpages.debian.org/bookworm/lsb-release/lsb_release.1.en.html
[^dot]: `man bash` (bash 5.2.15, Debian bookworm) — "If filename does not contain a slash, filenames in PATH are used to find the directory containing filename, but filename does not need to be executable." "When bash is not in posix mode, it searches the current directory if no file is found in PATH." Debian 12 컨테이너에서 `sh -c ". rocky.os-release"`(dash)는 `.: rocky.os-release: not found`, `bash --posix -c ". rocky.os-release"` 는 `.: rocky.os-release: file not found` 로 실패하고, `bash -c ". rocky.os-release"` 는 현재 폴더의 파일을 읽어 성공하는 것을 확인했습니다. https://manpages.debian.org/bookworm/bash/bash.1.en.html
[^orb]: OrbStack 문서 Architecture — "OrbStack uses a lightweight Linux virtual machine with a shared kernel to minimize overhead and save resources" "OrbStack runs full-blown Linux machines that work almost exactly like traditional virtual machines, all while sharing the same kernel." https://docs.orbstack.dev/architecture
[^uname-exit]: GNU coreutils 9.1 매뉴얼(Debian 12 의 `info coreutils 'uname invocation'`), "uname invocation" — "An exit status of zero indicates success, and a nonzero value indicates failure." `man uname` 에는 종료 코드 절이 없고 코드 1 은 이 시트의 실측입니다(Debian 12, coreutils 9.1). <https://www.gnu.org/software/coreutils/manual/html_node/uname-invocation.html>
[^lsb-exit]: `man lsb_release` (lsb-release 12.0, Debian bookworm) — 절은 NAME, SYNOPSIS, DESCRIPTION, OPTIONS, FILES, SEE ALSO, AUTHOR, LICENSE 이고 종료 코드 절이 없습니다. 코드 0 과 2 는 이 시트의 실측입니다(Debian 12, lsb-release 12.0). <https://manpages.debian.org/bookworm/lsb-release/lsb_release.1.en.html>
