---
title: 02_os/container-security — 컨테이너 보안의 리눅스 토대
tags: [moc, container, security, linux, namespace, cgroup, docker, kubernetes, runtime]
status: draft
related:
  - ../../README.md
  - ../../kernel/README.md
  - ../../../10_security/README.md
updated: 2026-06-03
---


# 02_os/container-security
---
> 『Container Security, 2판』(Liz Rice, O'Reilly)을 따라 컨테이너 보안을 리눅스 커널의 작동 원리에서부터 정리합니다. control groups·namespaces·root 디렉토리 변경이라는 세 기둥에서 출발해 이미지·공급망·런타임·통신까지 다룹니다. "이렇게 설정하라"가 아니라 "왜 그렇게 동작하는가"를 기준으로 위험을 스스로 판단하는 멘탈 모델을 목표로 합니다.

이웃한 `kernel/` 폴더가 K8s 운영자 관점에서 namespace·cgroup을 본다면, 본 폴더는 같은 메커니즘을 "보안 관점"에서 다시 봅니다. 컨테이너가 리눅스 커널 기능의 조합이라는 사실이 두 폴더를 잇는 공통 토대이므로, 같은 메커니즘이 양쪽에서 등장하면 서로 교차참조합니다.



## 문서

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 00-00 | [책 개요와 학습 로드맵](./00-00.책%20개요와%20학습%20로드맵.md) | 이 책은 무엇을 어떤 순서로 다루는가? 컨테이너를 떠받치는 리눅스 기초와 16챕터의 큰 줄기는? |
| 01-01 | [컨테이너 보안 위협 — 위협 모델·공격 벡터·보안 원칙](./01-01.컨테이너%20보안%20위협%20—%20위협%20모델·공격%20벡터·보안%20원칙.md) | 위험·위협·완화는 어떻게 다른가? 생애주기별 공격 벡터와 대응 장은? 컨테이너는 왜 약한 보안 경계이고 멀티테넌시·5대 보안 원칙은 무엇인가? (Ch 1) |
| 02-01 | [리눅스 시스템 콜·권한·Capabilities](./02-01.리눅스%20시스템%20콜·권한·Capabilities.md) | 앱은 왜 syscall 로 커널에 일을 청하는가? DAC·setuid/setgid·capabilities 3계층은? setuid 가 왜 권한 상승 통로이고 기본 root 컨테이너는 왜 위험한가? (Ch 2) |
| 03-01 | [제어 그룹(cgroups) — 자원 제한과 격리](./03-01.제어%20그룹(cgroups)%20—%20자원%20제한과%20격리.md) | cgroup 은 무엇을 제한하나? 컨트롤러·`memory.max`·`cgroup.procs`는? 런타임은 어떻게 자동화하고, 자원 고갈·fork bomb 공격을 어떻게 막나? (Ch 3) |
| 04-01 | [컨테이너 격리 (1) — namespace와 root 디렉토리 변경](./04-01.컨테이너%20격리%20(1)%20—%20namespace와%20root%20디렉토리%20변경.md) | namespace 8종은 각각 무엇을 격리하나? `unshare`·`--fork`·독립 `/proc`은 왜 필요한가? chroot/pivot_root 로 root 를 바꾼다는 게 무슨 뜻인가? (Ch 4 전반) |
| 04-02 | [컨테이너 격리 (2) — user namespace·Pod·호스트 관점](./04-02.컨테이너%20격리%20(2)%20—%20user%20namespace·Pod·호스트%20관점.md) | user namespace 는 왜 보안 핵심인가? `uid_map` 매핑은? Pod 는 어떤 namespace 를 공유하나? 왜 호스트 root 와 컨테이너 root 는 같은가? (Ch 4 후반) |
| 05-01 | [가상 머신 — VMM과 격리 비교](./05-01.가상%20머신%20—%20VMM과%20격리%20비교.md) | VM 과 컨테이너의 근본 차이는? Type 1/2·KVM·trap-and-emulate·권한 링은? 왜 VM 격리(Xen 5만 줄)가 컨테이너(커널 2000만 줄 공유)보다 강한가? (Ch 5) |
| 06-01 | [컨테이너 이미지 — 구조·빌드·저장](./06-01.컨테이너%20이미지%20—%20구조·빌드·저장.md) | 이미지의 두 부분(rootfs·설정)은? OCI 포맷·digest·runc bundle 은? 왜 빌드=root 위험이고, 삭제한 시크릿이 왜 레이어에 남으며, 태그 vs digest 는? (Ch 6) |
| 07-01 | [공급망 보안 (1) — SLSA·SBOM·Dockerfile·빌드 머신](./07-01.공급망%20보안%20(1)%20—%20SLSA·SBOM·Dockerfile·빌드%20머신.md) | SLSA 레벨·SBOM·provenance 는? 의존성 혼동·패키지 환각은? 최소 base image·Dockerfile 모범관행·임시 빌드 머신은? (Ch 7 전반) |
| 07-02 | [공급망 보안 (2) — 서명·attestation·배포 검증](./07-02.공급망%20보안%20(2)%20—%20서명·attestation·배포%20검증.md) | SBOM 생성·sigstore(cosign/fulcio/rekor) keyless 서명은? build attestation·in-toto 는? 배포 검증과 admission control 의 다섯 점검은? (Ch 7 후반) |
| 08-01 | [이미지 취약점 (1) — 취약점 연구·CVE·VEX](./08-01.이미지%20취약점%20(1)%20—%20취약점%20연구·CVE·VEX.md) | 취약점이란 무엇이고 누가 찾나? CVE·CNA·MITRE·NVD 는? 왜 NVD 만 보면 거짓 양성이 생기고 배포판 권고까지 봐야 하나? VEX 4상태는? (Ch 8 전반) |
| 08-02 | [이미지 취약점 (2) — 스캐닝·CI/CD·제로데이](./08-02.이미지%20취약점%20(2)%20—%20스캐닝·CI/CD·제로데이.md) | 왜 컨테이너가 아니라 이미지를 스캔하나? 불변성·drift·정기 스캔(Heartbleed)은? 스캐너 결과가 다른 이유·shift-left·admission·제로데이는? (Ch 8 후반) |
| 09-01 | [IaC 와 GitOps — 선언적 인프라·배포 보안](./09-01.IaC%20와%20GitOps%20—%20선언적%20인프라·배포%20보안.md) | IaC 와 GitOps 는 어떻게 다른가? 사람은 Git·controller 만 클러스터 모델은? 4원칙·배포 보안 함의 9가지는? 악성 manifest 주입·의존성 혼동과 모범 관행 10가지는? (Ch 9) |
| 10-01 | [격리 강화 (1) — seccomp·AppArmor·SELinux](./10-01.격리%20강화%20(1)%20—%20seccomp·AppArmor·SELinux.md) | sandboxing 이란? seccomp 가 막는 syscall 과 Moby 기본 프로파일은? AppArmor·SELinux 의 LSM·MAC vs DAC 는? 세 기법이 공통으로 못 막는 것(공유 커널·Dirty COW)은? (Ch 10 전반) |
| 10-02 | [격리 강화 (2) — gVisor·Kata·마이크로VM](./10-02.격리%20강화%20(2)%20—%20gVisor·Kata·마이크로VM.md) | gVisor 의 Sentry/Gofer·paravirt 는? Kata 는 컨테이너를 어떻게 VM 에 넣나? Firecracker 등 마이크로VM 이 빠른 비결은? unikernel·세 범주 비교·선택 기준은? (Ch 10 후반) |
| 11-01 | [격리 붕괴 (1) — root 문제와 회피](./11-01.격리%20붕괴%20(1)%20—%20root%20문제와%20회피.md) | 왜 기본 root 실행이 곧 호스트 root 인가? UID override·no-new-privileges(setuid)는? Nginx·SW 설치의 root 필요성과 대안은? eBPF 권한·rootless containers 는? (Ch 11 전반) |
| 11-02 | [격리 붕괴 (2) — 위험한 설정·정당한 공유](./11-02.격리%20붕괴%20(2)%20—%20위험한%20설정·정당한%20공유.md) | `--privileged` 가 푸는 capabilities 는? 민감 디렉토리 마운트·Docker socket·`--pid=host` 의 위험은? 같은 공유가 정당한 사이드카·debug container 패턴은? (Ch 11 후반) |
| 12-01 | [컨테이너 네트워크 (1) — 세그멘테이션·OSI·IP](./12-01.컨테이너%20네트워크%20(1)%20—%20세그멘테이션·OSI·IP.md) | 마이크로세그멘테이션·CNI 는? OSI 7계층은 어느 주소로 작동하나? IP 패킷이 DNS·라우팅·ARP·bridge 를 어떻게 거치나? K8s pod IP·service NAT 는? (Ch 12 전반) |
| 12-02 | [컨테이너 네트워크 (2) — 정책·eBPF·Service Mesh](./12-02.컨테이너%20네트워크%20(2)%20—%20정책·eBPF·Service%20Mesh.md) | iptables/kube-proxy 가 왜 규모에서 병목인가? eBPF/Cilium 의 map·identity 는? NetworkPolicy L3/4·L7·Service Mesh·default deny 는? (Ch 12 후반) |
| 13-01 | [안전한 연결 (1) — X.509·키·CA·TLS](./13-01.안전한%20연결%20(1)%20—%20X.509·키·CA·TLS.md) | 보안 연결의 두 축(인증·암호화)은? X.509·공개/개인 키(암호화·서명)는? CA·체인·self-signed 는? CSR·TLS/mTLS 핸드셰이크·skip-verify 는? (Ch 13 전반) |
| 13-02 | [안전한 연결 (2) — WireGuard·Mesh·SPIFFE](./13-02.안전한%20연결%20(2)%20—%20WireGuard·Mesh·SPIFFE.md) | WireGuard·IPSec 의 L3 터널은? zero-trust·인증서 폐기(K8s 미지원)는? Service Mesh mTLS·SPIFFE/SPIRE 신원 발급·ingress/egress 는? (Ch 13 후반) |
| 14-01 | [시크릿 전달 — 속성·전달방식·K8s Secrets](./14-01.시크릿%20전달%20—%20속성·전달방식·K8s%20Secrets.md) | 시크릿의 바람직한 속성(암호·폐기·회전·write-only)은? 컨테이너에 넣는 5가지 방법 중 왜 파일(tmpfs)이 최선인가? K8s Secrets·CSI Driver·External Secrets Operator 와 "root 는 다 본다"는? (Ch 14) |
| 15-01 | [런타임 보안 (1) — 정책·eBPF 기술](./15-01.런타임%20보안%20(1)%20—%20정책·eBPF%20기술.md) | 보안 관측성이란? 이미지 런타임 정책 4축(네트워크·실행파일·파일·UID)·drift 방지·fileless 는? LD_PRELOAD·ptrace·seccomp 한계와 eBPF 가 우수한 이유는? (Ch 15 전반) |
| 15-02 | [런타임 보안 (2) — 도구·차단·완화](./15-02.런타임%20보안%20(2)%20—%20도구·차단·완화.md) | Falco·Tetragon 의 비교 위치·차단 차이는? 동기적 SIGKILL·차단 vs 경고는? quarantine·eBPF 동적 로드로 패치 전 취약점(xz) 완화는? (Ch 15 후반) |
| 16-01 | [OWASP Top 10 — 컨테이너 관점 매핑](./16-01.OWASP%20Top%2010%20—%20컨테이너%20관점%20매핑.md) | OWASP Top 10 을 컨테이너 완화책에 어떻게 매핑하나? 왜 SSRF 가 컨테이너에서 순위가 올라가나? 컨테이너가 줄이는 폭발 반경 vs 앱 코드가 본령인 결함은? (Ch 16, 책 마무리·교차참조 허브) |



## 학습 로드맵 (완료)

책 구조를 따라 다섯 그룹 순서로 채웠습니다. **Preface + Chapter 1~16 전체(노트 24편)** 가 완성됐습니다. 각 그룹은 이전 그룹 위에 쌓이는 멘탈 모델이고, 마지막 16장(OWASP)이 전체를 공통 축으로 다시 묶습니다.

| 그룹 | 챕터 | 주제 | 상태 |
|------|------|------|------|
| ① 토대 | Ch 1~2 | 위협 모델·공격 벡터, 핵심 리눅스 메커니즘(시스템 콜·capability) | ✅ |
| ② 해부 | Ch 3~5 | 컨테이너의 구성 요소, 격리 수준과 한계, VM 격리와의 비교 | ✅ |
| ③ 이미지·공급망 | Ch 6~9 | 이미지 빌드 보안, 공급망 변조 방지, 취약점 탐지, 불변성·GitOps | ✅ |
| ④ 격리 강화 | Ch 10~11 | 선택적 리눅스 보안 강화(하드닝), 위험한 오설정과 격리 붕괴 | ✅ |
| ⑤ 통신·런타임 | Ch 12~16 | 컨테이너 간 통신, 키·인증서, 런타임 자격증명, 런타임 보안 도구, OWASP Top 10 | ✅ |



## 상위·이웃

- 상위: [02_os/ MOC](../../README.md)
- 이웃: [02_os/kernel/ MOC](../../kernel/README.md) — K8s 운영 관점의 커널 메커니즘(namespace·cgroup·user namespace·OverlayFS). 본서 Chapter 3·4와 주제가 겹칩니다
- 이웃: [10_security/ MOC](../../../10_security/README.md) — 인증·암호·OWASP·위협 모델링. 본서 Chapter 13·14(키·인증서)·16(OWASP)과 시선을 나눠 가집니다
