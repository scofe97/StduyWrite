---
title: OS 개발 키워드
tags: [landscape, linux, os, kernel, container, performance, security]
status: final
source:
  - ../02_os/README.md
  - ../02_os/kernel/README.md
  - ../02_os/book/systems-performance/README.md
related:
  - README.md
  - network-keywords.md
  - k8s-keywords.md
  - ../02_os/README.md
updated: 2026-10-10
---

# OS 개발 키워드
---

> OS 개발 키워드 표. 문서를 쓸 때 참고합니다.



## 1단계 · Linux 사용

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 셸 — 스트림 · 변수 · 종료 상태 | 필수 | [셸의 실체](../02_os/book/learning-modern-linux/03-01.%EC%85%B8%EC%9D%98%20%EC%8B%A4%EC%B2%B4%EB%8A%94%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%EA%B3%BC%20%EB%B3%80%EC%88%98%EC%99%80%20%EC%A2%85%EB%A3%8C%20%EC%83%81%ED%83%9C%EB%8B%A4.md) | The Linux Command Line 1·5~8장 |
| 파일 · 권한 · 리다이렉션 | 필수 | [모든 것이 파일](../02_os/book/learning-modern-linux/05-01.%EB%AA%A8%EB%93%A0%20%EA%B2%83%EC%9D%B4%20%ED%8C%8C%EC%9D%BC%EC%9D%B4%EB%9D%BC%EB%8A%94%20%EB%A7%90%EC%9D%80%20%EC%86%90%EC%9E%A1%EC%9D%B4%EA%B0%80%20%ED%95%98%EB%82%98%EB%9D%BC%EB%8A%94%20%EB%9C%BB%EC%9D%B4%EB%8B%A4.md) | The Linux Command Line 4·6·9장 |
| 모든 것이 파일 — VFS · mount · 장치 | 필수 | [모든 것이 파일](../02_os/book/learning-modern-linux/05-01.%EB%AA%A8%EB%93%A0%20%EA%B2%83%EC%9D%B4%20%ED%8C%8C%EC%9D%BC%EC%9D%B4%EB%9D%BC%EB%8A%94%20%EB%A7%90%EC%9D%80%20%EC%86%90%EC%9E%A1%EC%9D%B4%EA%B0%80%20%ED%95%98%EB%82%98%EB%9D%BC%EB%8A%94%20%EB%9C%BB%EC%9D%B4%EB%8B%A4.md) | How Linux Works 3·4장 |
| inode · 저널링 파일시스템 | 선택 | | How Linux Works 4장 |
| 부팅 · initramfs · systemd | 필수 | [부팅과 systemd](../02_os/book/learning-modern-linux/06-01.%EB%A8%BC%EC%A0%80%20%EC%BC%9C%EC%A7%80%EB%8A%94%20%EA%B2%83%20%ED%95%98%EB%82%98%EA%B0%80%20%EB%82%98%EB%A8%B8%EC%A7%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%EC%BC%A0%EB%8B%A4.md) | How Linux Works 5·6장 |
| journal · 시스템 설정 · 서비스 의존 | 필수 | [부팅과 systemd](../02_os/book/learning-modern-linux/06-01.%EB%A8%BC%EC%A0%80%20%EC%BC%9C%EC%A7%80%EB%8A%94%20%EA%B2%83%20%ED%95%98%EB%82%98%EA%B0%80%20%EB%82%98%EB%A8%B8%EC%A7%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%EC%BC%A0%EB%8B%A4.md) | How Linux Works 7장 |
| 커널이 맡는 일과 맡지 않는 일 | 필수 | [커널과 운영체제](../02_os/book/learning-modern-linux/02-01.%EC%BB%A4%EB%84%90%EC%9D%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%ED%95%98%EC%A7%80%EB%A7%8C%20%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EB%8A%94%20%EC%95%84%EB%8B%88%EB%8B%A4.md) · [하드웨어 추상화](../02_os/book/learning-modern-linux/01-01.%ED%95%98%EB%93%9C%EC%9B%A8%EC%96%B4%EB%A5%BC%20%EA%B0%80%EB%A6%AC%EA%B3%A0%20%EB%82%98%EB%A9%B4%20%EB%AC%B4%EC%97%87%EC%9D%B4%20%EB%B3%B4%EC%9D%BC%EC%A7%80%EB%A5%BC%20%EC%A0%95%ED%95%B4%EC%95%BC%20%ED%95%9C%EB%8B%A4.md) | Operating System Concepts 1·2장 |
| 셸 스크립트가 조용히 실패하는 법 | 추천 | [조용한 실패](../02_os/book/learning-modern-linux/03-03.bash%20%EB%8A%94%20%EC%A1%B0%EC%9A%A9%ED%9E%88%20%EC%8B%A4%ED%8C%A8%ED%95%98%EB%AF%80%EB%A1%9C%20%EC%8B%9C%EB%81%84%EB%9F%BD%EA%B2%8C%20%EB%A7%8C%EB%93%A4%EC%96%B4%EC%95%BC%20%ED%95%9C%EB%8B%A4.md) | The Linux Command Line 7장 |
| 명령 조합 · 파이프라인 · 단축 | 추천 | [명령 줄이기](../02_os/book/learning-modern-linux/03-02.%EC%9E%90%EC%A3%BC%20%EC%B9%98%EB%8A%94%20%EA%B2%83%EC%9D%BC%EC%88%98%EB%A1%9D%20%EC%A7%A7%EC%95%84%EC%95%BC%20%ED%95%9C%EB%8B%A4.md) | Efficient Linux 1·3·5·7장 |
| `systemd-analyze` 로 부팅 쪼개기 | 선택 |  | [systemd-analyze(1)](https://man7.org/linux/man-pages/man1/systemd-analyze.1.html) |



## 2단계 · 실행 모델

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 유저 · 커널 스페이스 · 시스템 콜 | 필수 | [커널과 OS](../02_os/book/learning-modern-linux/02-01.%EC%BB%A4%EB%84%90%EC%9D%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%ED%95%98%EC%A7%80%EB%A7%8C%20%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EB%8A%94%20%EC%95%84%EB%8B%88%EB%8B%A4.md) · [커널·시스템 콜](../02_os/book/systems-performance/03-01.%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%20%E2%80%94%20%EC%BB%A4%EB%84%90%C2%B7%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%BD%9C%C2%B7%EC%9D%B8%ED%84%B0%EB%9F%BD%ED%8A%B8%C2%B7%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4.md) | Operating System Concepts 2장 |
| 인터럽트 · 트랩 · 시스템 콜 — 커널에 들어가는 세 길 | 추천 | | Operating System Concepts 1·2장 |
| `strace` 로 시스템 콜 세기 | 필수 | [namespace와 루트](../08_cloud/book/container-security/04-01.namespace%EC%99%80%20%EB%A3%A8%ED%8A%B8%20%EB%94%94%EB%A0%89%ED%86%A0%EB%A6%AC%20%E2%80%94%20%EA%B2%A9%EB%A6%AC%EB%A5%BC%20%EB%A7%8C%EB%93%9C%EB%8A%94%20%EB%91%90%20%EC%9E%A5%EC%B9%98.md) | |
| process · thread · task 구조 · VAS | 필수 | [컨텍스트·VAS·스택](../02_os/book/linux-kernel-programming/06-01.%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%EC%99%80%20%EC%8A%A4%EB%A0%88%EB%93%9C%20%281%29%20%E2%80%94%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%C2%B7VAS%C2%B7%EC%8A%A4%ED%83%9D.md) · [task 구조](../02_os/book/linux-kernel-programming/06-02.%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%EC%99%80%20%EC%8A%A4%EB%A0%88%EB%93%9C%20%282%29%20%E2%80%94%20task%20%EA%B5%AC%EC%A1%B0%EC%99%80%20current.md) | Operating System Concepts 3·4장 |
| `fork` · `exec` · copy-on-write 로 뜨는 새 프로세스 | 필수 | | Operating System Concepts 3장 |
| signal · 종료 코드 137 · 143 | 필수 | [셸의 실체](../02_os/book/learning-modern-linux/03-01.%EC%85%B8%EC%9D%98%20%EC%8B%A4%EC%B2%B4%EB%8A%94%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%EA%B3%BC%20%EB%B3%80%EC%88%98%EC%99%80%20%EC%A2%85%EB%A3%8C%20%EC%83%81%ED%83%9C%EB%8B%A4.md) | The Linux Command Line 10장 |
| zombie · PID 1 | 필수 | [부팅과 systemd](../02_os/book/learning-modern-linux/06-01.%EB%A8%BC%EC%A0%80%20%EC%BC%9C%EC%A7%80%EB%8A%94%20%EA%B2%83%20%ED%95%98%EB%82%98%EA%B0%80%20%EB%82%98%EB%A8%B8%EC%A7%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%EC%BC%A0%EB%8B%A4.md) | How Linux Works 8장 |
| core dump 저장 경로 | 선택 |  | [core(5)](https://man7.org/linux/man-pages/man5/core.5.html) |
| file descriptor · `ulimit` · 관측 창 | 필수 | [모든 것이 파일](../02_os/book/learning-modern-linux/05-01.%EB%AA%A8%EB%93%A0%20%EA%B2%83%EC%9D%B4%20%ED%8C%8C%EC%9D%BC%EC%9D%B4%EB%9D%BC%EB%8A%94%20%EB%A7%90%EC%9D%80%20%EC%86%90%EC%9E%A1%EC%9D%B4%EA%B0%80%20%ED%95%98%EB%82%98%EB%9D%BC%EB%8A%94%20%EB%9C%BB%EC%9D%B4%EB%8B%A4.md) · [자원별 관측 창](../02_os/book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md) | |
| 주소 공간 · heap · stack · 프로세스 메모리 배치 | 필수 |  | Operating System Concepts 3장 |
| `mmap` · 공유 메모리 · copy-on-write · zero-fill | 추천 | | Operating System Concepts 9장 |
| IPC — pipe · 공유 메모리 · 메시지 전달 | 추천 | [필요해지는 조건](../02_os/book/learning-modern-linux/09-01.%EC%9D%B4%20%EC%9E%A5%EC%9D%84%20%EB%AC%B6%EB%8A%94%20%EA%B2%83%EC%9D%80%20%EC%A3%BC%EC%A0%9C%EA%B0%80%20%EC%95%84%EB%8B%88%EB%9D%BC%20%ED%95%84%EC%9A%94%ED%95%B4%EC%A7%80%EB%8A%94%20%EC%A1%B0%EA%B1%B4%EC%9D%B4%EB%8B%A4.md) | Operating System Concepts 3장 |
| event loop · readiness 모델 · 배압 | 추천 |  | [epoll(7)](https://man7.org/linux/man-pages/man7/epoll.7.html) |
| `epoll` · 논블로킹 I/O | 추천 | [커널 구현·BPF](../02_os/book/systems-performance/03-03.%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%20%E2%80%94%20%EC%BB%A4%EB%84%90%20%EA%B5%AC%ED%98%84%C2%B7Linux%20%EB%B0%9C%EC%A0%84%EC%82%AC%C2%B7BPF.md) · [애플리케이션 성능](../02_os/book/systems-performance/05-01.%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98%20%E2%80%94%20%EA%B8%B0%EC%B4%88%EC%99%80%20%EC%84%B1%EB%8A%A5%20%EA%B8%B0%EB%B2%95.md) | Operating System Concepts 13장 |
| 동기화 · 교착 · 조건 변수 | 추천 | | Operating System Concepts 5·7장 |
| `prctl` · `PR_SET_PDEATHSIG` | 선택 |  | [prctl(2)](https://man7.org/linux/man-pages/man2/prctl.2.html) |
| `vfork` · `clone3` | 선택 |  | [vfork(2)](https://man7.org/linux/man-pages/man2/vfork.2.html) · [clone(2)](https://man7.org/linux/man-pages/man2/clone.2.html) |
| 이벤트 루프 · 비동기 I/O · 워커 스레드 | 선택 | [이벤트 루프](../02_os/book/ostep_operating-systems-three-easy-pieces/27-01.%EC%8A%A4%EB%A0%88%EB%93%9C%20%EC%97%86%EC%9D%B4%20%EB%8F%99%EC%8B%9C%20%EC%84%9C%EB%B2%84%EB%A5%BC%20%EB%A7%8C%EB%93%9C%EB%8A%94%20%EB%B2%95%20%E2%80%94%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EB%A3%A8%ED%94%84%EC%99%80%20select%C2%B7%EB%B9%84%EB%8F%99%EA%B8%B0%20%EC%9E%85%EC%B6%9C%EB%A0%A5.md) · [비동기 I/O](../02_os/book/ostep_operating-systems-three-easy-pieces/27-01.%EC%8A%A4%EB%A0%88%EB%93%9C%20%EC%97%86%EC%9D%B4%20%EB%8F%99%EC%8B%9C%20%EC%84%9C%EB%B2%84%EB%A5%BC%20%EB%A7%8C%EB%93%9C%EB%8A%94%20%EB%B2%95%20%E2%80%94%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EB%A3%A8%ED%94%84%EC%99%80%20select%C2%B7%EB%B9%84%EB%8F%99%EA%B8%B0%20%EC%9E%85%EC%B6%9C%EB%A0%A5.md) | |
| CPU 바운드 · I/O 바운드 | 선택 | [I/O 바운드](../01_language/book/Inside%20the%20Java%20Virtual%20Machine%20JVM%20Advanced%20Features%20and%20Best%20Practices/ch05_efficient-concurrency/01-05.Virtual%20Threads%20%EA%B8%B0%EC%B4%88.md) | |
| 원자적 연산 · 뮤텍스 컨텐션 | 선택 | [원자적 연산](../01_language/book/Inside%20the%20Java%20Virtual%20Machine%20JVM%20Advanced%20Features%20and%20Best%20Practices/ch05_efficient-concurrency/03-02.%EC%9B%90%EC%9E%90%20%EC%97%B0%EC%82%B0%EA%B3%BC%20%EB%8F%99%EC%8B%9C%EC%84%B1%20%EC%BB%AC%EB%A0%89%EC%85%98.md) | |



## 3단계 · 컨테이너 기반

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| namespace 여덟 가지 · `unshare` | 필수 | [나머지 namespace](../08_cloud/book/container-security/04-02.%EB%82%98%EB%A8%B8%EC%A7%80%20namespace%EC%99%80%20%ED%98%B8%EC%8A%A4%ED%8A%B8%EC%97%90%EC%84%9C%20%EB%B3%B8%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88.md) · [namespace와 루트](../08_cloud/book/container-security/04-01.namespace%EC%99%80%20%EB%A3%A8%ED%8A%B8%20%EB%94%94%EB%A0%89%ED%86%A0%EB%A6%AC%20%E2%80%94%20%EA%B2%A9%EB%A6%AC%EB%A5%BC%20%EB%A7%8C%EB%93%9C%EB%8A%94%20%EB%91%90%20%EC%9E%A5%EC%B9%98.md) | Container Security 4장 |
| cgroup v2 — controller · PSI | 필수 | [cgroup v2 깊이](../02_os/kernel/01-02.cgroup%20v2%20%EA%B9%8A%EC%9D%B4.md) · [Control Group](../08_cloud/book/container-security/03-01.Control%20Group%20%E2%80%94%20%EC%9E%90%EC%9B%90%EC%9D%84%20%EC%A0%9C%ED%95%9C%ED%95%B4%20%EA%B5%B6%EA%B8%B0%EA%B8%B0%EB%A5%BC%20%EB%A7%89%EB%8B%A4.md) | Container Security 3장 |
| cgroup 경로와 컨테이너 · Pod 신원의 연결 | 추천 | | Container Security 3장 |
| 한도의 출처 — 사람이 정한 값 · 기계가 유도한 값 · 상속된 값 | 필수 | [진단 개념](../troubleshooting/_concepts/common-%ED%95%9C%EB%8F%84%EB%8A%94-%EC%96%B4%EB%94%94%EC%84%9C-%EC%98%A4%EB%8A%94%EA%B0%80.md) | Linux Kernel Docs — cgroup v2 |
| `memory.max` · `memory.events` · OOM Killer | 필수 | [namespace와 cgroup으로 보는 격리](../08_cloud/book/kubernetes-in-action/02-03.%EB%84%A4%EC%9E%84%EC%8A%A4%ED%8E%98%EC%9D%B4%EC%8A%A4%EC%99%80%20cgroup%EC%9C%BC%EB%A1%9C%20%EB%B3%B4%EB%8A%94%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC.md) · [Endowus OOMKilled](../02_os/kernel/01-06.cgroup%20%EC%82%AC%EB%A1%80%20%E2%80%94%20Endowus%20OOMKilled.md) | |
| `cpu.max` · `cpu.stat` · throttling | 필수 | [cgroup v2 깊이](../02_os/kernel/01-02.cgroup%20v2%20%EA%B9%8A%EC%9D%B4.md) | |
| mount propagation 네 가지 | 필수 | [마운트 네임스페이스와 propagation](../02_os/kernel/01-03.%EB%A7%88%EC%9A%B4%ED%8A%B8%20%EB%84%A4%EC%9E%84%EC%8A%A4%ED%8E%98%EC%9D%B4%EC%8A%A4%EC%99%80%20propagation.md) | |
| OverlayFS · copy-on-write | 필수 | [OverlayFS와 user namespace](../02_os/kernel/01-07.OverlayFS%EC%99%80%20user%20namespace%20%E2%80%94%20Netflix%20UID%20%EA%B2%A9%EB%A6%AC.md) | |
| user namespace · rootless | 추천 | [OverlayFS와 user namespace](../02_os/kernel/01-07.OverlayFS%EC%99%80%20user%20namespace%20%E2%80%94%20Netflix%20UID%20%EA%B2%A9%EB%A6%AC.md) · [나머지 namespace](../08_cloud/book/container-security/04-02.%EB%82%98%EB%A8%B8%EC%A7%80%20namespace%EC%99%80%20%ED%98%B8%EC%8A%A4%ED%8A%B8%EC%97%90%EC%84%9C%20%EB%B3%B8%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88.md) | Container Security 4장 |
| VM 대 컨테이너 — 격리 강도의 차이 | 추천 | [가상머신 격리](../08_cloud/book/container-security/05-01.%EA%B0%80%EC%83%81%EB%A8%B8%EC%8B%A0%20%E2%80%94%20%EC%99%9C%20VM%20%EA%B2%A9%EB%A6%AC%EA%B0%80%20%EB%8D%94%20%EA%B0%95%ED%95%98%EB%8B%A4%EA%B3%A0%20%ED%95%98%EB%8A%94%EA%B0%80.md) | Container Security 5장 |
| 컨테이너 = namespace · cgroup · 파일시스템 — 재료가 아니라 조합 | 추천 | [컨테이너는 조합](../02_os/book/learning-modern-linux/06-02.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%9D%98%20%EC%83%88%EB%A1%9C%EC%9B%80%EC%9D%80%20%EC%9E%AC%EB%A3%8C%EA%B0%80%20%EC%95%84%EB%8B%88%EB%9D%BC%20%EC%A1%B0%ED%95%A9%EC%97%90%20%EC%9E%88%EB%8B%A4.md) |  |
| cgroup namespace | 선택 |  | [cgroup_namespaces(7)](https://man7.org/linux/man-pages/man7/cgroup_namespaces.7.html) |
| hugetlbfs | 선택 |  | [HugeTLB Pages](https://docs.kernel.org/admin-guide/mm/hugetlbpage.html) |



## 4단계 · 성능 분석

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| USE · RED · 드릴다운 · 지연 분석 | 필수 | [방법론 용어·모델](../02_os/book/systems-performance/02-01.%EB%B0%A9%EB%B2%95%EB%A1%A0%20%E2%80%94%20%EC%9A%A9%EC%96%B4%C2%B7%EB%AA%A8%EB%8D%B8%C2%B7%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md) · [방법론 분석 방법론 20종](../02_os/book/systems-performance/02-02.%EB%B0%A9%EB%B2%95%EB%A1%A0%20%E2%80%94%20%EB%B6%84%EC%84%9D%20%EB%B0%A9%EB%B2%95%EB%A1%A0%2020%EC%A2%85.md) · [관측·실험·60초 체크리스트](../02_os/book/systems-performance/01-02.%EC%84%9C%EB%A1%A0%20%E2%80%94%20%EA%B4%80%EC%B8%A1%C2%B7%EC%8B%A4%ED%97%98%C2%B7%EB%B0%A9%EB%B2%95%EB%A1%A0%C2%B7%EC%BC%80%EC%9D%B4%EC%8A%A4.md) |  |
| 활용률 대 압력 — PSI 가 답하는 질문 | 필수 |  | Linux Kernel Docs — psi |
| run queue · CFS · context switch | 필수 | [CPU 용어·모델](../02_os/book/systems-performance/06-01.CPU%20%E2%80%94%20%EC%9A%A9%EC%96%B4%C2%B7%EB%AA%A8%EB%8D%B8%C2%B7%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md) ~ [CPU 관측 도구](../02_os/book/systems-performance/06-04.CPU%20%E2%80%94%20%EA%B4%80%EC%B8%A1%20%EB%8F%84%EA%B5%AC%C2%B7%EC%8B%9C%EA%B0%81%ED%99%94.md) | Operating System Concepts 6장 |
| RSS · VSS · PSS · page cache | 필수 | [메모리 용어](../02_os/book/systems-performance/07-01.%EB%A9%94%EB%AA%A8%EB%A6%AC%20%E2%80%94%20%EC%9A%A9%EC%96%B4%C2%B7%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md) ~ [메모리 관측 도구](../02_os/book/systems-performance/07-04.%EB%A9%94%EB%AA%A8%EB%A6%AC%20%E2%80%94%20%EA%B4%80%EC%B8%A1%20%EB%8F%84%EA%B5%AC.md) | Operating System Concepts 8·9장 |
| block I/O · IOPS · queue depth · `fsync` | 필수 | [디스크 개념](../02_os/book/systems-performance/09-01.%EB%94%94%EC%8A%A4%ED%81%AC%20%E2%80%94%20%EB%B0%B0%EA%B2%BD%C2%B7%EB%AA%A8%EB%8D%B8%C2%B7%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md) ~ [디스크 관측 도구](../02_os/book/systems-performance/09-04.%EB%94%94%EC%8A%A4%ED%81%AC%20%E2%80%94%20%EA%B4%80%EC%B8%A1%20%EB%8F%84%EA%B5%AC.md) | Operating System Concepts 10장 |
| I/O 스케줄러 — mq-deadline · BFQ · kyber | 추천 | | Systems Performance 9장 |
| 파일 시스템 캐시 · 유형 · 튜닝 | 추천 | [파일 시스템 개념](../02_os/book/systems-performance/08-01.%ED%8C%8C%EC%9D%BC%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%E2%80%94%20%EB%B0%B0%EA%B2%BD%C2%B7%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md) ~ [파일 시스템 관측 도구](../02_os/book/systems-performance/08-04.%ED%8C%8C%EC%9D%BC%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%E2%80%94%20%EA%B4%80%EC%B8%A1%20%EB%8F%84%EA%B5%AC.md) | Operating System Concepts 11·12장 |
| load average · softirq | 추천 | [CPU 아키텍처·스케줄러](../02_os/book/systems-performance/06-02.CPU%20%E2%80%94%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98%C2%B7%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC.md) | |
| CPU 캐시 계층 · cache line · 캐시 일관성 — 연산보다 데이터 이동이 병목일 때 | 추천 | [CPU 아키텍처·스케줄러](../02_os/book/systems-performance/06-02.CPU%20%E2%80%94%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98%C2%B7%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC.md) | Systems Performance 6·7장 |
| swap · overcommit | 추천 | [메모리 방법론·튜닝](../02_os/book/systems-performance/07-03.%EB%A9%94%EB%AA%A8%EB%A6%AC%20%E2%80%94%20%EB%B0%A9%EB%B2%95%EB%A1%A0%C2%B7%ED%8A%9C%EB%8B%9D.md) | |
| THP — Transparent Huge Pages | 선택 | | [Transparent Hugepage](https://docs.kernel.org/admin-guide/mm/transhuge.html) |
| 관측 지점 — 재는 것은 바깥, 알고 싶은 것은 안 | 추천 | [바깥과 안](../02_os/book/learning-modern-linux/08-01.%EC%9E%AC%EB%8A%94%20%EA%B2%83%EC%9D%80%20%EB%B0%94%EA%B9%A5%EC%9D%B4%EA%B3%A0%20%EC%95%8C%EA%B3%A0%20%EC%8B%B6%EC%9D%80%20%EA%B2%83%EC%9D%80%20%EC%95%88%EC%9D%B4%EB%8B%A4.md) |  |
| 모델링 · 용량계획 · 통계 · 시각화 | 선택 | [모델링·용량계획](../02_os/book/systems-performance/02-03.%EB%B0%A9%EB%B2%95%EB%A1%A0%20%E2%80%94%20%EB%AA%A8%EB%8D%B8%EB%A7%81%C2%B7%EC%9A%A9%EB%9F%89%EA%B3%84%ED%9A%8D%C2%B7%ED%86%B5%EA%B3%84%C2%B7%EC%8B%9C%EA%B0%81%ED%99%94.md) | |
| throughput · tail latency · P99 · P99.9 | 필수 | [방법론 용어·모델](../02_os/book/systems-performance/02-01.%EB%B0%A9%EB%B2%95%EB%A1%A0%20%E2%80%94%20%EC%9A%A9%EC%96%B4%C2%B7%EB%AA%A8%EB%8D%B8%C2%B7%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md) | Systems Performance 2장 |
| coordinated omission — 측정이 놓치는 지연 | 필수 |  | [wrk2 README](https://github.com/giltene/wrk2) |
| flame graph · CPU·heap·block·mutex 프로파일 | 추천 | [CPU 관측 도구](../02_os/book/systems-performance/06-04.CPU%20%E2%80%94%20%EA%B4%80%EC%B8%A1%20%EB%8F%84%EA%B5%AC%C2%B7%EC%8B%9C%EA%B0%81%ED%99%94.md) | Systems Performance 6장 |
| 애플리케이션 프로파일링 — off-CPU · 스레드 상태 · 심볼·스택 누락 | 추천 | [언어·방법론](../02_os/book/systems-performance/05-02.%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98%20%E2%80%94%20%EC%96%B8%EC%96%B4%C2%B7%EB%B0%A9%EB%B2%95%EB%A1%A0.md) · [관측 도구·gotchas](../02_os/book/systems-performance/05-03.%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98%20%E2%80%94%20%EA%B4%80%EC%B8%A1%20%EB%8F%84%EA%B5%AC%C2%B7gotchas.md) | Systems Performance 5장 |
| 성능 사례 — 컨테이너가 3~4배 빨라진 이유 | 선택 | [케이스 스터디](../02_os/book/systems-performance/16-01.%EC%BC%80%EC%9D%B4%EC%8A%A4%20%EC%8A%A4%ED%84%B0%EB%94%94%20%E2%80%94%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EA%B0%80%203-4%EB%B0%B0%20%EB%B9%A0%EB%A5%B8%20%EC%9D%B4%EC%9C%A0.md) | Systems Performance 16장 |
| malloc · free list · arena · 단편화 · 대체 allocator | 추천 | [힙 밖에서 쌓이는 메모리](../troubleshooting/_concepts/runtime-%ED%9E%99-%EB%B0%96%EC%97%90%EC%84%9C-%EC%8C%93%EC%9D%B4%EB%8A%94-%EB%A9%94%EB%AA%A8%EB%A6%AC.md) |  |
| SIMD · 벡터화 — 한 명령이 여러 데이터를 | 추천 | | Real-World Cryptography 13장 |
| SSE · AVX · AVX2 · AVX-512 · ARM NEON | 선택 |  | [Intel Intrinsics Guide](https://www.intel.com/content/www/us/en/docs/intrinsics-guide/index.html) |
| CPUID · CPU feature detection · `lscpu` · `/proc/cpuinfo` | 추천 | | Systems Performance 6장 |
| AES-NI · PCLMULQDQ · SHA 확장 | 추천 | | Real-World Cryptography 13장 |
| 가상화·컨테이너에서 CPU feature 노출 | 선택 | | Systems Performance 11장 |
| steal time · noisy neighbor · CPU quota · 워밍업 | 추천 | [하드웨어 가상화](../02_os/book/systems-performance/11-02.%ED%81%B4%EB%9D%BC%EC%9A%B0%EB%93%9C%20%EC%BB%B4%ED%93%A8%ED%8C%85%20%E2%80%94%20%ED%95%98%EB%93%9C%EC%9B%A8%EC%96%B4%20%EA%B0%80%EC%83%81%ED%99%94.md) | Systems Performance 11장 |
| blk-cgroup · `io.max` | 선택 |  | [cgroup v2 — IO](https://docs.kernel.org/admin-guide/cgroup-v2.html) |
| IRQ affinity · `irqbalance` | 선택 |  | [SMP IRQ affinity](https://docs.kernel.org/core-api/irq/irq-affinity.html) |
| 사건 시점 스냅샷 — 상시 기록하고 경보 때 꺼내기 | 선택 | [당근 발표 정리](_digest/2026-10-10_당근_빌더_밋업_2026_인프라_발표_5편.md) | |



## 5단계 · 관측과 보안

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| procfs · sysfs · `sar` · 관측 소스 | 필수 | [관측 도구 커버리지](../02_os/book/systems-performance/04-01.%EA%B4%80%EC%B8%A1%20%EB%8F%84%EA%B5%AC%20%E2%80%94%20%EB%8F%84%EA%B5%AC%20%EC%BB%A4%EB%B2%84%EB%A6%AC%EC%A7%80%C2%B7%EC%9C%A0%ED%98%95.md) ~ [sar·트레이싱 도구](../02_os/book/systems-performance/04-03.%EA%B4%80%EC%B8%A1%20%EB%8F%84%EA%B5%AC%20%E2%80%94%20sar%C2%B7%ED%8A%B8%EB%A0%88%EC%9D%B4%EC%8B%B1%20%EB%8F%84%EA%B5%AC%C2%B7%EA%B4%80%EC%B8%A1%EC%9D%98%20%EA%B4%80%EC%B8%A1.md) | |
| `/proc/stat` · `/proc/meminfo` 읽기 | 필수 | | Linux Kernel Docs — proc |
| `/proc/PID/stat` · `status` · `statm` | 필수 | | Linux Kernel Docs — proc |
| `/proc/diskstats` · `/proc/net/snmp` | 추천 | | Linux Kernel Docs — proc |
| `/proc/net/tcp` 와 socket inode — 포트에서 프로세스로 거슬러 가기 | 추천 | | Linux Kernel Docs — proc |
| `/proc/pressure` — some 과 full · avg10 | 필수 | | Linux Kernel Docs — psi |
| perf — 샘플링과 이벤트 소스 | 필수 | [perf 개요](../02_os/book/systems-performance/13-01.perf%20%E2%80%94%20%EA%B0%9C%EC%9A%94%C2%B7%EC%84%9C%EB%B8%8C%EC%BB%A4%EB%A7%A8%EB%93%9C%C2%B7%EC%9B%90%EB%9D%BC%EC%9D%B4%EB%84%88.md) ~ [perf 명령](../02_os/book/systems-performance/13-03.perf%20%E2%80%94%20%EB%AA%85%EB%A0%B9.md) | |
| capability · seccomp | 필수 | [시스템 콜·capability](../08_cloud/book/container-security/02-01.Linux%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%BD%9C%C2%B7%EA%B6%8C%ED%95%9C%C2%B7capability%20%E2%80%94%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%B3%B4%EC%95%88%EC%9D%98%20%EB%B0%94%EB%8B%A5.md) · [잘게 쪼개는 접근 제어](../02_os/book/learning-modern-linux/04-01.%EC%A0%84%EB%B6%80%20%EC%95%84%EB%8B%88%EB%A9%B4%20%EC%A0%84%EB%AC%B4%EC%97%90%EC%84%9C%20%EC%9E%98%EA%B2%8C%20%EC%AA%BC%EA%B0%9C%EB%8A%94%20%EC%AA%BD%EC%9C%BC%EB%A1%9C.md) | Container Security 2장 |
| 비밀의 수명 — 생성·사용·파기 | 필수 | | Real-World Cryptography 8장 |
| zeroing · `explicit_bzero` · `OPENSSL_cleanse` | 필수 | | Real-World Cryptography 8장 |
| dead store elimination — `memset` 이 지워지는 이유 | 추천 | | [CWE-14](https://cwe.mitre.org/data/definitions/14.html) |
| `mlock` · swap · core dump 로 새는 비밀 | 추천 | | Systems Performance 7장 |
| 상수 시간 코드 · 사이드 채널 · 캐시 타이밍 | 선택 | | Real-World Cryptography 13·16장 |
| Ftrace — tracefs · 트레이서 | 추천 | [Ftrace 개요](../02_os/book/systems-performance/14-01.Ftrace%20%E2%80%94%20%EA%B0%9C%EC%9A%94%C2%B7tracefs%C2%B7%ED%94%84%EB%A1%9C%ED%8C%8C%EC%9D%BC%EB%9F%AC.md) ~ [Ftrace 프론트엔드](../02_os/book/systems-performance/14-03.Ftrace%20%E2%80%94%20%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%94%EB%93%9C.md) | |
| eBPF · BCC · bpftrace | 추천 | [BPF 개요](../02_os/book/systems-performance/15-01.BPF%20%E2%80%94%20%EA%B0%9C%EC%9A%94%C2%B7BCC%20vs%20bpftrace%C2%B7BCC.md) ~ [bpftrace](../02_os/book/systems-performance/15-03.BPF%20%E2%80%94%20bpftrace%20%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D%C2%B7%EB%A0%88%ED%8D%BC%EB%9F%B0%EC%8A%A4.md) · [BCC Hello World](../02_os/book/learning-ebpf/02-01.BCC%20Hello%20World%20%EB%8A%94%20execve%20%EC%97%90%20kprobe%20%EB%A5%BC%20%EA%B1%B8%EA%B3%A0%20%EA%B2%B0%EA%B3%BC%EB%A5%BC%20trace_pipe%20%EC%99%80%20%ED%95%B4%EC%8B%9C%20%EB%A7%B5%EC%9C%BC%EB%A1%9C%20%EA%BA%BC%EB%82%B8%EB%8B%A4.md) · [clang·bpftool 적재](../02_os/book/learning-ebpf/03-01.C%20%EC%86%8C%EC%8A%A4%EB%8A%94%20clang%20%EC%9C%BC%EB%A1%9C%20eBPF%20%EB%B0%94%EC%9D%B4%ED%8A%B8%EC%BD%94%EB%93%9C%EA%B0%80%20%EB%90%98%EA%B3%A0%20bpftool%20%EC%9D%B4%20%EC%A0%81%EC%9E%AC%ED%95%B4%20ID%20%EC%99%80%20%ED%83%9C%EA%B7%B8%EB%A5%BC%20%EB%B6%99%EC%9D%B8%EB%8B%A4.md) | Learning eBPF 3장 |
| verifier · CO-RE · BTF | 추천 | [BTF](../02_os/book/learning-ebpf/05-01.%EB%9F%B0%ED%83%80%EC%9E%84%20%EC%BB%B4%ED%8C%8C%EC%9D%BC%20%EB%8C%80%EC%8B%A0%20BTF%20%EA%B0%80%20%EA%B5%AC%EC%A1%B0%EC%B2%B4%20%EB%B0%B0%EC%B9%98%EB%A5%BC%20%EA%B8%B0%EB%A1%9D%ED%95%B4%20CO-RE%20%EC%9D%B4%EC%8B%9D%EC%9D%98%20%EA%B7%BC%EA%B1%B0%EA%B0%80%20%EB%90%9C%EB%8B%A4.md) · [vmlinux.h·CO-RE](../02_os/book/learning-ebpf/05-02.vmlinux.h%20%EC%99%80%20libbpf%20%EB%A7%A4%ED%81%AC%EB%A1%9C%EB%A1%9C%20%EC%93%B4%20eBPF%20%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%A8%EC%9D%80%20CO-RE%20%EC%9E%AC%EB%B0%B0%EC%B9%98%20%EC%A0%95%EB%B3%B4%EB%A5%BC%20%ED%92%88%EB%8A%94%EB%8B%A4.md) · [libbpf·스켈레톤](../02_os/book/learning-ebpf/05-03.libbpf%20%EB%8A%94%20%EC%A0%81%EC%9E%AC%20%EB%95%8C%20CO-RE%20%EC%9E%AC%EB%B0%B0%EC%B9%98%EB%A5%BC%20%EA%B3%A0%EC%B9%98%EA%B3%A0%20%EC%8A%A4%EC%BC%88%EB%A0%88%ED%86%A4%EC%9D%B4%20%EC%97%B4%EA%B8%B0%C2%B7%EC%A0%81%EC%9E%AC%C2%B7%EB%B6%80%EC%B0%A9%C2%B7%EC%A0%95%EB%A6%AC%EB%A5%BC%20%EB%AC%B6%EB%8A%94%EB%8B%A4.md) · [verifier 경로·로그](../02_os/book/learning-ebpf/06-01.verifier%20%EB%8A%94%20%EB%AA%A8%EB%93%A0%20%EA%B2%BD%EB%A1%9C%EB%A5%BC%20%EB%94%B0%EB%9D%BC%EA%B0%80%EB%A9%B0%20%EB%A0%88%EC%A7%80%EC%8A%A4%ED%84%B0%20%ED%83%80%EC%9E%85%EA%B3%BC%20%EA%B0%92%20%EB%B2%94%EC%9C%84%EB%A5%BC%20%EA%B8%B0%EB%A1%9D%ED%95%98%EA%B3%A0%20%EB%A1%9C%EA%B7%B8%EB%A1%9C%20%EB%B3%B4%EC%97%AC%20%EC%A4%80%EB%8B%A4.md) · [헬퍼·메모리·루프 검사](../02_os/book/learning-ebpf/06-02.%ED%97%AC%ED%8D%BC%C2%B7%EB%A9%94%EB%AA%A8%EB%A6%AC%20%EC%A0%91%EA%B7%BC%C2%B7%EB%A3%A8%ED%94%84%EB%8A%94%20%EC%A6%9D%EB%AA%85%EB%90%9C%20%EB%B2%94%EC%9C%84%20%EC%95%88%EC%97%90%EC%84%9C%EB%A7%8C%20verifier%20%EB%A5%BC%20%ED%86%B5%EA%B3%BC%ED%95%9C%EB%8B%A4.md) · [프로그램 유형](../02_os/book/learning-ebpf/07-01.%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%A8%20%EC%9C%A0%ED%98%95%EC%9D%B4%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%EC%99%80%20%ED%97%AC%ED%8D%BC%EB%A5%BC%20%EC%A0%95%ED%95%98%EA%B3%A0%20kprobe%C2%B7fentry%C2%B7tracepoint%20%EB%8A%94%20%EC%95%88%EC%A0%95%EC%84%B1%EA%B3%BC%20%EB%B9%84%EC%9A%A9%EC%9C%BC%EB%A1%9C%20%EA%B0%88%EB%A6%B0%EB%8B%A4.md) | Learning eBPF 5·6·7장 |
| 샌드박싱 세 갈래 | 추천 | [컨테이너 격리 강화](../08_cloud/book/container-security/08-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC%20%EA%B0%95%ED%99%94%20%E2%80%94%20%EC%83%8C%EB%93%9C%EB%B0%95%EC%8B%B1%EC%9D%98%20%EC%84%B8%20%EA%B0%88%EB%9E%98.md) | Container Security 8장 |
| 격리 우회 — 설정 하나로 무너지는 경계 | 추천 | [컨테이너 격리 깨뜨리기](../08_cloud/book/container-security/09-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC%20%EA%B9%A8%EB%9C%A8%EB%A6%AC%EA%B8%B0%20%E2%80%94%20%EC%84%A4%EC%A0%95%20%ED%95%98%EB%82%98%EB%A1%9C%20%EB%AC%B4%EB%84%88%EC%A7%80%EB%8A%94%20%EA%B2%BD%EA%B3%84.md) | Container Security 9장 |
| AppArmor · SELinux · 보호와 보안 | 선택 | [컨테이너 격리 강화](../08_cloud/book/container-security/08-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC%20%EA%B0%95%ED%99%94%20%E2%80%94%20%EC%83%8C%EB%93%9C%EB%B0%95%EC%8B%B1%EC%9D%98%20%EC%84%B8%20%EA%B0%88%EB%9E%98.md) | Operating System Concepts 14·15장 |
| eBPF 보안 활용 | 선택 | [LSM 훅·TOCTOU](../02_os/book/learning-ebpf/09-01.%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%BD%9C%20%EC%9E%85%EA%B5%AC%20%EA%B2%80%EC%82%AC%EB%8A%94%20TOCTOU%20%EC%97%90%20%EB%9A%AB%EB%A0%A4%20%EB%B3%B4%EC%95%88%20%EB%8F%84%EA%B5%AC%EB%8A%94%20LSM%20%ED%9B%85%EA%B3%BC%20%EC%BB%A4%EB%84%90%20%ED%95%A8%EC%88%98%EC%97%90%EC%84%9C%20%ED%8C%90%EC%A0%95%ED%95%98%EA%B3%A0%20SIGKILL%20%EB%A1%9C%20%EB%A7%89%EB%8A%94%EB%8B%A4.md) | Learning eBPF 9장 |
| Landlock | 선택 |  | [Landlock](https://docs.kernel.org/userspace-api/landlock.html) |
| BPF map 용량과 유형 — 가득 찰 때의 동작 · 용도별 맵 분리 | 추천 | [당근 발표 정리](_digest/2026-10-10_당근_빌더_밋업_2026_인프라_발표_5편.md) | [BPF maps](https://docs.kernel.org/bpf/maps.html) |
| 스택 심볼 해석 — `/proc/PID/maps` · ELF 심볼 · strip 된 바이너리 | 추천 | [당근 발표 정리](_digest/2026-10-10_당근_빌더_밋업_2026_인프라_발표_5편.md) | |
| eBPF 오버헤드 측정 — `kernel.bpf_stats_enabled` | 선택 | [당근 발표 정리](_digest/2026-10-10_당근_빌더_밋업_2026_인프라_발표_5편.md) | [kernel sysctl](https://docs.kernel.org/admin-guide/sysctl/kernel.html) |
| 제로 트러스트 · 권한 에스컬레이션 | 선택 | [권한 에스컬레이션](../08_cloud/book/container-security/02-01.Linux%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%BD%9C%C2%B7%EA%B6%8C%ED%95%9C%C2%B7capability%20%E2%80%94%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%B3%B4%EC%95%88%EC%9D%98%20%EB%B0%94%EB%8B%A5.md) | |
| 멀티 계정 전략 · 랜딩 존 · 계정 벤딩 · 조직 단위 · 서비스 컨트롤 정책 · 퍼미션 바운더리 | 선택 | [랜딩 존](../07_devops/book/cicd_cicd-patterns/10-01.Deployment%20Strategies%20Creational%20CICD%20with%20Cloud%20Providers.md) | |
| 특권 접근 관리 · 저스트 인 타임 접근 · 세션 레코딩 | 선택 | | |
| 불변 감사 로그 · 로그 무결성 · 로그 보존 정책 · 로그 아카이빙 | 선택 | [불변 감사 로그](../08_cloud/book/cks-study-guide/07-01.%EC%8B%A4%ED%96%89%20%EC%A4%91%EC%9D%B8%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%A7%80%EC%BC%9C%EB%B3%B4%EA%B8%B0%20%E2%80%94%20Falco%C2%B7%EB%B6%88%EB%B3%80%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%C2%B7%EA%B0%90%EC%82%AC%20%EB%A1%9C%EA%B7%B8.md) | |
| 위협 인텔리전스 · 위협 헌팅 · SIEM · SOAR · 포렌식 | 선택 | | |
| IAM 사용자 · IAM 역할 · 신뢰 정책 · 권한 정책 · 리소스 기반 정책 · STS AssumeRole | 선택 | | |
| 침해 지표(IOC) | 선택 | | |



## 6단계 · 커널 내부

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| VM split · 주소 변환 · KASLR · NUMA | 추천 | [VM split·주소 변환](../02_os/book/linux-kernel-programming/07-01.%EB%A9%94%EB%AA%A8%EB%A6%AC%20%EA%B4%80%EB%A6%AC%20%281%29%20%E2%80%94%20VM%20split%EA%B3%BC%20%EC%A3%BC%EC%86%8C%20%EB%B3%80%ED%99%98.md) ~ [물리 메모리·NUMA](../02_os/book/linux-kernel-programming/07-03.%EB%A9%94%EB%AA%A8%EB%A6%AC%20%EA%B4%80%EB%A6%AC%20%283%29%20%E2%80%94%20%EB%AC%BC%EB%A6%AC%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EC%99%80%20NUMA.md) | Operating System Concepts 8·9장 |
| TLB · TLB miss · shootdown | 추천 | | Operating System Concepts 8장 |
| page table · 가용 공간 관리 | 추천 | | Operating System Concepts 8·9장 |
| 페이지 할당자 · GFP 플래그 | 추천 | [페이지 할당자](../02_os/book/linux-kernel-programming/08-01.%EB%A9%94%EB%AA%A8%EB%A6%AC%20%ED%95%A0%EB%8B%B9%20%281%29%20%E2%80%94%20%ED%8E%98%EC%9D%B4%EC%A7%80%20%ED%95%A0%EB%8B%B9%EC%9E%90%EC%99%80%20GFP%20%ED%94%8C%EB%9E%98%EA%B7%B8.md) | |
| slab · `kmalloc` 낭비 · `vmalloc` | 추천 | [slab 할당자](../02_os/book/linux-kernel-programming/08-02.%EB%A9%94%EB%AA%A8%EB%A6%AC%20%ED%95%A0%EB%8B%B9%20%282%29%20%E2%80%94%20slab%20%ED%95%A0%EB%8B%B9%EC%9E%90%EC%99%80%20kmalloc%20%EB%82%AD%EB%B9%84.md) · [slab cache·vmalloc](../02_os/book/linux-kernel-programming/09-01.%EB%A9%94%EB%AA%A8%EB%A6%AC%20%ED%95%A0%EB%8B%B9%20%283%29%20%E2%80%94%20custom%20slab%20cache%EC%99%80%20vmalloc.md) | |
| 할당 API 선택 · memory reclaim · kswapd | 추천 | [API 선택과 reclaim](../02_os/book/linux-kernel-programming/09-02.%EB%A9%94%EB%AA%A8%EB%A6%AC%20%ED%95%A0%EB%8B%B9%20%284%29%20%E2%80%94%20API%20%EC%84%A0%ED%83%9D%EA%B3%BC%20memory%20reclaim.md) | Linux Kernel Programming 9장 |
| demand paging · OOM killer | 추천 | [demand paging·OOM](../02_os/book/linux-kernel-programming/09-03.%EB%A9%94%EB%AA%A8%EB%A6%AC%20%ED%95%A0%EB%8B%B9%20%285%29%20%E2%80%94%20demand%20paging%EA%B3%BC%20OOM%20killer.md) | Operating System Concepts 9장 |
| 스케줄링 클래스 · CFS 구현 · 선점 | 추천 | [스케줄링 기초](../02_os/book/linux-kernel-programming/10-01.CPU%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC%20%281%29%20%E2%80%94%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%A7%81%20%EA%B8%B0%EC%B4%88%EC%99%80%20%ED%9D%90%EB%A6%84%20%EC%8B%9C%EA%B0%81%ED%99%94.md) ~ [cgroups CPU 제약](../02_os/book/linux-kernel-programming/11-03.CPU%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC%20%286%29%20%E2%80%94%20cgroups%20CPU%20%EC%A0%9C%EC%95%BD%EA%B3%BC%20RTOS.md) | Operating System Concepts 6장 |
| 임계 구역 · mutex · spinlock | 추천 | [임계 구역](../02_os/book/linux-kernel-programming/12-01.%EC%BB%A4%EB%84%90%20%EB%8F%99%EA%B8%B0%ED%99%94%20%281%29%20%E2%80%94%20%EC%9E%84%EA%B3%84%20%EA%B5%AC%EC%97%AD%EA%B3%BC%20data%20race.md) ~ [spinlock](../02_os/book/linux-kernel-programming/12-03.%EC%BB%A4%EB%84%90%20%EB%8F%99%EA%B8%B0%ED%99%94%20%283%29%20%E2%80%94%20spinlock%EA%B3%BC%20%EC%9D%B8%ED%84%B0%EB%9F%BD%ED%8A%B8.md) | Operating System Concepts 5장 |
| atomic · lock-free · lockdep · memory barrier | 선택 | [atomic·refcount](../02_os/book/linux-kernel-programming/13-01.%EC%BB%A4%EB%84%90%20%EB%8F%99%EA%B8%B0%ED%99%94%20%284%29%20%E2%80%94%20atomic%C2%B7refcount%EC%99%80%20RMW%20%EC%97%B0%EC%82%B0%EC%9E%90.md) ~ [lock-free·barrier](../02_os/book/linux-kernel-programming/13-03.%EC%BB%A4%EB%84%90%20%EB%8F%99%EA%B8%B0%ED%99%94%20%286%29%20%E2%80%94%20lock-free%EC%99%80%20lockdep%C2%B7memory%20barrier.md) | |
| 하이퍼바이저 · VM · CPU·메모리 배분 | 선택 | | Virtualization Essentials 1~3 · 7·8장 · Operating System Concepts 16장 |
| KVM 구조 · 성능 튜닝 | 대체 | | Mastering KVM Virtualization 1·2 · 15장 |
| kdump · crash 분석 | 선택 |  | [kdump](https://docs.kernel.org/admin-guide/kdump/kdump.html) |
| io_uring · VFS 구현 · LSM 훅 | 선택 |  | [io_uring(7)](https://man7.org/linux/man-pages/man7/io_uring.7.html) |



## 넣지 않은 것

> 다른 문서가 정본이거나 이 로드맵의 축과 다른 것들입니다.

| 대상 | 이유 |
|---|---|
| 네트워크 패킷 경로 | [네트워크 로드맵](network-keywords.md)이 맡습니다 |
| Linux Kernel Programming 1~5장 | 커널 빌드와 모듈 개발 환경. 증상을 읽는 축이 아닙니다 |
| Systems Performance 11·12장 | 클라우드 가상화와 벤치마킹이라 읽기 흐름에 넣지 않았습니다. 11장은 4단계 보완 참조로, 12장은 실습 표에서만 겁니다 |
| Container Security 6·7장 | 이미지와 공급망. `07_devops` 소관입니다 |
| Operating System Concepts 17~20장 | 분산 시스템과 특정 OS 사례. 이 로드맵의 축이 아닙니다 |
| How Linux Works 9~17장 | 네트워크 · 데스크톱 · 컴파일. 다른 로드맵이거나 축 밖입니다 |
| JVM heap · G1GC · ZGC · native memory | [JVM 로드맵](jvm-keywords.md) 소관입니다. 3단계는 cgroup 이 재는 RSS 까지만 봅니다 |
| The Linux Programming Interface | 정독용이 아니라 사전입니다. 시스템 콜과 API 가 왜 그 모양인지 궁금할 때만 펴 봅니다 |
| BPF Performance Tools | 5단계 다음의 tracing 심화입니다. `/proc` · cgroup · PSI · perf 를 지난 뒤에 엽니다 |
| Below · OpenMetrics · exporter | Below 는 위 인터페이스를 프로그램이 어떻게 수집하는지 보는 코드입니다. 수집한 뒤 시각화는 [관측 가능성 로드맵](observability-keywords.md)이 맡습니다 |
| AVX-512 · ARM SVE 명령어 개별 규격 | 소장본에 장이 없습니다. 어떤 확장이 있는지까지만 알고, 개별 명령은 필요할 때 [Intel Intrinsics Guide](https://www.intel.com/content/www/us/en/docs/intrinsics-guide/index.html)에서 찾습니다 |
| dead store elimination 의 컴파일러 구현 | 소장본에 장이 없습니다. `memset` 이 지워진다는 사실과 `explicit_bzero` 로 막는다는 대응까지가 이 로드맵의 몫이고, 최적화 패스 자체는 컴파일러 축입니다 |
| HBM · CoWoS 같은 메모리 패키징 | 하드웨어 설계 축입니다. 연산보다 데이터 이동이 병목이라는 memory wall 개념까지가 4단계의 몫입니다 |
| 하드웨어 사이드 채널 — 캐시 타이밍 공격 · 전력 분석 | 백엔드 키워드 목록이 백엔드 밖 심화로 따로 뺀 키워드 |
| 하드웨어 신뢰 기반 — 신뢰 실행 환경·TEE · SGX · 시큐어 엔클레이브 · 원격 증명 · 어테스테이션 · 측정된 부트 · 시큐어 부트 · 체인 오브 트러스트 · 루트 오브 트러스트 | 백엔드 키워드 목록이 백엔드 밖 심화로 따로 뺀 키워드 |
| 어피니티·NUMA — 어피니티 · IRQ 어피니티 · CPU 어피니티 · NUMA · NUMA 어웨어 · 로컬·리모트 메모리 · 메모리 바인딩 · 인터리브 | 백엔드 키워드 목록이 백엔드 밖 심화로 따로 뺀 키워드 |
| 페이지 관리 — 휴즈 페이지 · 트랜스페어런트 휴즈 페이지 · 메모리 컴팩션 · 페이지 마이그레이션 · 스왑 프리 | 백엔드 키워드 목록이 백엔드 밖 심화로 따로 뺀 키워드 |
| 메모리 하드웨어 — 메모리 컨트롤러 · 채널 · 랭크 · 뱅크 · 로우 버퍼 · 컬럼 액세스 · CAS 레이턴시 · 메모리 대역폭 · 메모리 레이턴시 | 백엔드 키워드 목록이 백엔드 밖 심화로 따로 뺀 키워드 |
| 캐시 코히어런시 — 캐시 라인 · 캐시 코히어런시 · MESI · MOESI · 스누핑 · 디렉토리 기반 코히어런시 · 폴스·트루 쉐어링 · 캐시 라인 패딩 · 얼라인먼트 | 백엔드 키워드 목록이 백엔드 밖 심화로 따로 뺀 키워드 |
| 메모리 모델·배리어 — 메모리·로드·스토어·풀 배리어 · 릴랙스드 메모리 오더 · 시퀀셜 컨시스턴시 · 획득-해제 · 원자적 로드·스토어 | 백엔드 키워드 목록이 백엔드 밖 심화로 따로 뺀 키워드 |
| 원자 명령·락 프리 — 페치 앤 애드 · 테스트 앤 셋 · 스핀락 · 어댑티브 스핀락 · 락 프리 · 웨이트 프리 · 옵스트럭션 프리 · ABA 문제 · 해저드 포인터 · 에포크 기반 리클레임 · RCU · 리드 카피 업데이트 · 그레이스 피리어드 · 콰이센트 스테이트 · 지연 해제 · 메모리 리오더링 · 컴파일러·하드웨어 배리어 · 스토어·로드 버퍼 | 백엔드 키워드 목록이 백엔드 밖 심화로 따로 뺀 키워드 |
| CPU 마이크로아키텍처 — 아웃 오브 오더·스펙큘레이티브 실행 · 브랜치 프리딕션 · 파이프라인 해저드 · 슈퍼스칼라 · 리오더 버퍼 · 레지스터 리네이밍 · 프리페처 · L1~L3 미스 · TLB · 페이지 테이블 · PCID | 백엔드 키워드 목록이 백엔드 밖 심화로 따로 뺀 키워드 |
| 가상화 내부 — 메모리 가상화 · 게스트·호스트 물리 주소 · EPT · NPT · 중첩 페이지 테이블 · VM 엑시트·엔트리 · 파라·풀·하드웨어 어시스티드 버추얼라이제이션 · VT-x · AMD-V | 백엔드 키워드 목록이 백엔드 밖 심화로 따로 뺀 키워드 |
