---
title: 리눅스 명령어 시트
tags: [moc, linux, cli, cheatsheet, reference]
status: draft
related:
  - ../../README.md
  - ../../book/learning-modern-linux/README.md
updated: 2026-11-11
---

# 리눅스 명령어 시트

---

> 리눅스 명령의 사용법을 명령별로 모은 조회용 시트입니다. 책 노트는 원리를 설명하고, 명령 옵션과 실행 예는 여기에 둔 뒤 링크로 가져다 씁니다.

## 이 폴더를 쓰는 법

> 명령 하나를 한 시트에 두고, 늘 함께 쓰는 명령은 한 시트로 묶습니다.

시트는 하는 일에 따라 아래 분류의 하위 폴더에 둡니다. 시트가 아직 없는 분류도 표를 먼저 두었습니다.

- [text: 텍스트 처리](#text--텍스트-처리)
- [file: 파일과 디렉터리](#file--파일과-디렉터리)
- [perm: 사용자와 권한](#perm--사용자와-권한)
- [process: 프로세스와 잡](#process--프로세스와-잡)
- [resource: 자원과 성능 관측](#resource--자원과-성능-관측)
- [isolate: 격리와 자원 제한](#isolate--격리와-자원-제한)
- [net: 네트워크](#net--네트워크)
- [service: 서비스와 로그](#service--서비스와-로그)
- [ssh: 원격 접속과 전송](#ssh--원격-접속과-전송)
- [storage: 디스크와 파일시스템](#storage--디스크와-파일시스템)
- [kernel: 커널 설정과 부팅](#kernel--커널-설정과-부팅)
- [sysinfo: 시스템 정보](#sysinfo--시스템-정보)
- [security: SELinux·감사·인증서](#security--selinux감사인증서)
- [pkg: 패키지](#pkg--패키지)
- [shell: 세션과 스크립트](#shell--세션과-스크립트)
- [time: 날짜와 시간](#time--날짜와-시간)

시트는 모두 같은 절 순서로 씁니다. 하려는 일이 정해져 있으면 「핵심 문법」 에서 꼴을 찾고, 주석 끝 괄호에 적힌 유스케이스 제목으로 내려가면 됩니다.

- 개요: 명령이 하는 일 한 줄, 실측한 환경과 도구 버전
- 핵심 문법: 호출 형태와 자주 쓰는 꼴을 코드 블록 하나에 모은 것
- 종료 코드: 코드별 뜻과 그 코드가 나오는 예
- 유스케이스: 「실습 준비」 에서 입력 파일을 만든 뒤, 하려는 일마다 명령과 실제 출력을 둔 것
- 주의사항과 동작 원리: 헷갈리기 쉬운 동작과 그 이유
- 관련 문서와 참고 자료: 이어지는 시트·책 노트, man 원문 인용

유스케이스가 많아 한 시트가 900줄을 넘으면 유스케이스 묶음의 경계에서 두 시트로 나눕니다. 나눈 시트는 개요 첫 문장에서 원래 시트를 가리키고, 실습 준비를 이어받는지 적습니다.

코드 블록 안의 `#` 줄은 자리에 따라 뜻이 다릅니다.

- 명령 위의 `#` 줄은 풀이입니다. 그 아래 들여 쓴 `#   옵션   뜻` 줄은 그 자리에서 처음 쓰는 옵션의 뜻입니다
- 명령 옆이나 아래의 `#` 줄은 실제 출력입니다
- 명령 블록 바로 아래 따로 둔 블록도 실제 출력입니다

출력은 대부분 Debian 12 컨테이너에서 받았습니다. 도구 버전은 GNU sed 4.9, grep 3.8, coreutils 9.1, findutils 4.9.0, gawk 5.2.1, mawk 1.3.4, util-linux 2.38.1 입니다. `systemctl`·`hostnamectl` 처럼 systemd 가 있어야 하는 시트는 Ubuntu 26.04 VM 에서 받았습니다. 실측 환경은 시트마다 개요에 적혀 있습니다.

다른 리눅스 노트는 명령 사용법을 다시 쓰지 않고 이 시트로 링크합니다.



## text — 텍스트 처리

> 줄을 고르고, 칸을 자르고, 세고, 다음 명령의 인자로 넘기는 도구입니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|
| [sed](./text/sed.md) | `sed` | 줄 번호·패턴으로 줄을 고르거나, 문자열을 바꾸거나, 설정 파일을 제자리에서 고칠 때 |
| [head·tail](./text/head%C2%B7tail.md) | `head` · `tail` | 긴 파일의 앞뒤만 보거나, 로테이션되는 로그를 `tail -F` 로 따라갈 때 |
| [grep](./text/grep.md) | `grep` · `zgrep` | 패턴에 맞는 줄을 찾고 개수·파일 이름·앞뒤 문맥을 볼 때 |
| [cut](./text/cut.md) | `cut` | 구분자 하나나 글자 위치로 칸을 자를 때 |
| [awk](./text/awk.md) | `awk` | 공백으로 맞춘 출력에서 칸을 골라 비교하고 다시 조립할 때 |
| [sort·uniq·wc](./text/sort%C2%B7uniq%C2%B7wc.md) | `sort` · `uniq` · `wc` | 같은 값을 붙여 세거나 줄 수를 셀 때 |
| [tr](./text/tr.md) | `tr` | 글자를 바꾸거나 줄이거나 지울 때 |
| [paste·join·column](./text/paste%C2%B7join%C2%B7column.md) | `paste` · `join` · `column` | 두 파일의 줄을 잇거나 칸을 맞춰 표로 볼 때 |
| [xargs](./text/xargs.md) | `xargs` | 앞 명령의 출력을 다음 명령의 인자로 넘길 때 |



## file — 파일과 디렉터리

> 파일을 찾고, 속성을 보고, 복사하고 묶는 도구입니다. 후보는 `find`·`ls`·`stat`·`cp`·`rsync`·`tar` 입니다.

압축 후보는 `gzip`·`bzip2`·`xz`·`zstd`·`zip`·`unzip` 입니다. `tar` 는 여러 파일을 하나로 묶기만 하고 줄이지는 않습니다. 줄이는 일은 `gzip`·`xz`·`zstd` 같은 압축기가 맡고, `tar -z`·`-J`·`--zstd` 는 묶으면서 그 압축기를 부릅니다. `zip` 은 묶기와 압축을 한 번에 해서 Windows 와 주고받을 때 씁니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|



## perm — 사용자와 권한

> 누가 무엇을 할 수 있는지 보고 바꾸는 도구입니다. 후보는 `id`·`chmod`·`chown`·`chgrp`·`umask`·`getfacl`·`setfacl`·`sudo`·`visudo`·`su` 입니다.

계정을 만들고 바꾸는 `useradd`·`usermod`·`userdel`·`passwd`·`chage`, 로그인 기록을 보는 `last`·`lastb`·`lastlog`·`w`·`who`, 계정 정보를 묻는 `getent`·`faillock` 도 여기에 둡니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|



## process — 프로세스와 잡

> 실행 중인 프로세스를 보고, 신호를 보내고, 터미널에서 떼어 내는 도구입니다. 후보는 `kill`·`pgrep`·`killall`·`jobs`·`nohup`·`disown`·`setsid` 입니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|
| [ps](./process/ps.md) | `ps` | 프로세스 목록을 고르고 열을 골라 정렬하거나, %CPU·%MEM 을 읽을 때 |
| [ps 트리·스레드·상태 읽기](./process/ps%20트리·스레드·상태%20읽기.md) | `ps` · `pstree` | 부모·자식 트리, 스레드, VSZ/RSS, STAT 상태 코드와 좀비를 읽을 때 |
| [kill·pgrep·killall](./process/kill%C2%B7pgrep%C2%B7killall.md) | `kill` | 신호를 이름·번호로 보내고 종료와 강제 종료를 가를 때 |
| [kill·pgrep·killall 이름으로 찾아 신호 보내기](./process/kill%C2%B7pgrep%C2%B7killall%20이름으로%20찾아%20신호%20보내기.md) | `pgrep` · `pkill` · `killall` | 이름·사용자·명령줄로 프로세스를 찾아 신호를 보낼 때 |
| [jobs·bg·fg·wait](./process/jobs%C2%B7bg%C2%B7fg%C2%B7wait.md) | `jobs` · `bg` · `fg` · `wait` | 잡을 멈추고 앞뒤로 옮기거나 끝나기를 기다릴 때 |
| [nohup·disown·setsid 셸을 닫은 뒤에도 돌리기](./process/nohup%C2%B7disown%C2%B7setsid.md) | `nohup` · `disown` · `setsid` | 터미널이 끊기거나 셸을 닫아도 프로세스를 살려 둘 때 |



## resource — 자원과 성능 관측

> CPU·메모리·디스크가 얼마나 쓰이는지 재는 도구입니다. 후보는 `top`·`htop`·`watch`·`lsof`·`free`·`uptime`·`nproc`·`vmstat`·`iostat`·`mpstat`·`pidstat`·`sar`·`pmap`·`smem` 입니다.

우선순위와 한도를 바꾸는 `nice`·`renice`·`ionice`·`ulimit` 도 여기에 둡니다. 디스크 사용량을 재는 `df`·`du` 는 storage 에 둡니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|
| [top·htop](./resource/top%C2%B7htop.md) | `top` · `htop` | 머리줄의 부하·CPU·메모리와 VIRT·RES·SHR 열을 읽거나, `top -b` 로 기록을 남길 때 |
| [top·htop 대화형 키와 htop](./resource/top%C2%B7htop%20대화형%20키와%20htop.md) | `top` · `htop` | 스레드·명령줄을 펼치거나, 화면 키로 정렬·필터하거나, 같은 일을 `htop` 으로 할 때 |
| [lsof](./resource/lsof.md) | `lsof` | 파일을 쥔 프로세스를 찾거나, 지운 파일이 붙든 디스크 공간을 찾을 때 |
| [lsof 포트와 스크립트용 출력](./resource/lsof%20포트와%20스크립트용%20출력.md) | `lsof` | 포트를 듣는 프로세스와 연결 상태를 보거나, 스크립트에 넘길 PID·필드 출력을 만들 때 |
| [watch](./resource/watch.md) | `watch` | 명령을 몇 초마다 다시 돌려 바뀐 곳을 강조해 보거나, 출력이 바뀌면 멈출 때 |



## isolate — 격리와 자원 제한

> 프로세스가 볼 수 있는 것(namespace)과 쓸 수 있는 양(cgroup)을 정하는 도구입니다. 후보는 `systemd-cgls`·`systemd-cgtop`·`systemd-run -p`·`systemctl set-property`·`/sys/fs/cgroup`·`unshare`·`nsenter`·`lsns` 입니다.

resource 는 쓰이는 양을 재고, 여기는 쓸 수 있는 양에 한도를 겁니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|



## net — 네트워크

> 주소와 연결을 보고, 이름을 풀고, 요청을 보내는 도구입니다. 후보는 `ip`·`ss`·`ping`·`tracepath`·`traceroute`·`mtr`·`dig`·`resolvectl`·`curl`·`nc`·`nmcli`·`tcpdump` 입니다.

방화벽과 연결 추적을 다루는 `firewall-cmd`·`nft`·`iptables`·`conntrack`, NFS 를 다루는 `exportfs`·`showmount`·`nfsstat` 도 여기에 둡니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|



## service — 서비스와 로그

> 서비스를 켜고 끄고 로그를 읽는 도구입니다. 후보는 `systemctl`·`journalctl`·`systemd-run`·`logger`·`logrotate` 입니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|
| [systemctl](./service/systemctl.md) | `systemctl` | 서비스 상태를 읽고, 지금·부팅 때 켜고 끄고, 실패한 서비스를 추적할 때 |
| [systemctl 유닛 설정과 타이머](./service/systemctl%20유닛%20설정과%20타이머.md) | `systemctl` | drop-in 으로 유닛 설정을 바꾸고 반영하거나 타이머로 서비스를 주기 실행할 때 |
| [systemctl 함정과 동작 원리](./service/systemctl%20함정과%20동작%20원리.md) | `systemctl` | `mask` 가 실패하거나, ssh 서비스 이름과 소켓이 헷갈리거나, `Alias=` 별칭이 어떻게 생기는지 볼 때 |
| [journalctl](./service/journalctl.md) | `journalctl` | 유닛·시각·부팅·심각도·필드로 로그를 좁혀 읽을 때 |
| [journalctl 저장 공간과 읽기 권한](./service/journalctl%20저장%20공간과%20읽기%20권한.md) | `journalctl` | 저널 크기·저장 위치·복사본 정리와 일반 사용자의 읽기 권한을 볼 때 |
| [journalctl 출력 모양과 jq](./service/journalctl%20출력%20모양과%20jq.md) | `journalctl` · `jq` | 로그를 ISO 시각·필드·JSON 으로 바꿔 보거나, `-o json` 을 `jq` 로 넘겨 필드를 뽑을 때 |



## ssh — 원격 접속과 전송

> 다른 기계에 들어가고, 키를 만들어 나눠 주고, 파일을 주고받는 도구입니다. 후보는 `ssh`·`~/.ssh/config`·`ssh-keygen`·`ssh-copy-id`·`ssh-agent`·`scp`·`sftp`·`sshd`·`sshd_config` 입니다.

키 교환과 호스트 키 신뢰의 원리는 책 노트가 맡고, 여기는 명령과 설정 사용법만 둡니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|
| [ssh 접속·config·포트 포워딩](./ssh/ssh.md) | `ssh` · `~/.ssh/config` | 서버에 접속하거나 점프 호스트를 거치거나 터널을 열 때 |
| [ssh-keygen·ssh-copy-id·ssh-agent](./ssh/ssh-keygen%C2%B7ssh-copy-id%C2%B7ssh-agent.md) | `ssh-keygen` · `ssh-copy-id` · `ssh-agent` · `ssh-add` | 키를 만들어 올리고, 비밀번호 없이 접속하고, `known_hosts` 를 정리할 때 |
| [scp·sftp](./ssh/scp%C2%B7sftp.md) | `scp` · `sftp` | 서버와 파일을 주고받거나 서버 사이로 옮길 때 |
| [sshd·sshd_config](./ssh/sshd%C2%B7sshd_config.md) | `sshd` · `sshd_config` | 접속이 거절된 이유를 찾거나 서버 설정을 조일 때 |



## storage — 디스크와 파일시스템

> 디스크와 파티션을 보고, LVM 으로 묶고 늘리고, 파일시스템을 만들고 붙이는 도구입니다. 후보는 `lsblk`·`blkid`·`findmnt`·`mount`·`umount`·`parted`·`partprobe`·`growpart`·`pvs`·`vgs`·`lvs`·`lvextend`·`mkfs`·`tune2fs`·`e2fsck`·`resize2fs`·`xfs_info`·`xfs_growfs`·`swapon`·`mkswap`·`df`·`du`·`multipath` 입니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|



## kernel — 커널 설정과 부팅

> 커널 매개변수와 모듈, 커널 메시지, 부팅 설정과 부팅 시간을 다루는 도구입니다. 후보는 `sysctl`·`modprobe`·`lsmod`·`modinfo`·`dmesg`·`grubby`·`dracut`·`systemd-analyze` 입니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|



## sysinfo — 시스템 정보

> 어떤 배포판과 커널과 하드웨어 위에서 도는지 확인하는 도구입니다. 후보는 `uname`·`/etc/os-release`·`lsb_release`·`hostnamectl`·`dmidecode`·`lscpu` 입니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|
| [uname·os-release·lsb_release](./sysinfo/uname%C2%B7os-release%C2%B7lsb_release.md) | `uname` · `/etc/os-release` · `lsb_release` | 서버의 배포판·커널·하드웨어 종류를 확인할 때 |
| [hostnamectl·hostname](./sysinfo/hostnamectl%C2%B7hostname.md) | `hostnamectl` · `hostname` | 호스트 이름을 보거나 영구·임시로 바꿀 때 |
| [lscpu·nproc](./sysinfo/lscpu%C2%B7nproc.md) | `lscpu` · `nproc` | CPU 개수·구조·캐시를 읽거나, 컨테이너 CPU 제한이 어디에 보이는지 확인할 때 |
| [dmidecode·lsmem·lshw](./sysinfo/dmidecode%C2%B7lsmem%C2%B7lshw.md) | `dmidecode` · `lsmem` · `lshw` | 서버 모델·메모리 슬롯 정보를 보거나, DMI 표가 없을 때 대신 볼 곳을 찾을 때 |



## security — SELinux·감사·인증서

> 접근 제어 정책과 감사 기록을 보고, 인증서와 체크섬을 확인하는 도구입니다. 후보는 `getenforce`·`setenforce`·`sestatus`·`semanage`·`restorecon`·`setsebool`·`ausearch`·`aureport`·`audit2allow`·`openssl`·`sha256sum`·`update-ca-trust` 입니다.

SELinux 와 `update-ca-trust` 는 RHEL 계열 명령이라 이 분류의 출력은 Rocky Linux 9 에서 받습니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|



## pkg — 패키지

> 패키지를 찾고, 설치하고, 고정하고, 설치된 파일이 바뀌지 않았는지 확인하는 도구입니다. 후보는 RHEL 계열의 `dnf`·`rpm`·`createrepo`, Debian 계열의 `apt-get`·`apt-cache`·`apt-mark`·`dpkg`·`debsums` 입니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|



## shell — 세션과 스크립트

> 끊겨도 이어지는 세션을 두고, 명령을 시간 제한·잠금·예약과 함께 돌리는 도구입니다. 후보는 `tmux`·`screen`·`script`·`timeout`·`flock`·`tee`·`crontab`·`loginctl` 입니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|
| [flock](./shell/flock.md) | `flock` | 같은 작업이 겹쳐 돌지 않게 락을 걸거나, 락이 잡혀 있을 때 기다릴지 포기할지 옵션으로 고를 때 |
| [crontab](./shell/crontab.md) | `crontab` | 시각을 정해 명령을 돌리는 예약 표를 등록하거나, cron 이 작업에 주는 환경과 오류 출력을 확인할 때 |



## time — 날짜와 시간

> 시각을 읽고, 형식을 바꾸고, 날짜 사이를 계산하는 도구입니다. 다른 후보는 `timedatectl`·`chronyc`·`hwclock` 입니다.

| 시트 | 다루는 명령 | 이런 때 찾습니다 |
|------|------------|----------------|
| [date](./time/date.md) | `date` | 날짜를 에포크 초로 바꾸거나, 파일 이름에 날짜를 넣거나, 인증서 만료까지 남은 날을 셀 때 |



## 관련 문서

- [02_os](../../README.md) — OS 카테고리 지도
- [《Learning Modern Linux》 정독 노트](../../book/learning-modern-linux/README.md) — 셸과 명령의 원리. `find` 와 부록 레시피는 그 책의 00 시리즈 시트에 있습니다
