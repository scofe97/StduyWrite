---
title: Learning Modern Linux 정독 인덱스
tags: [moc, linux, kernel, shell, filesystem, networking, observability, container]
status: draft
source:
  - 《Learning Modern Linux》(Michael Hausenblas, O'Reilly, 2022)
related:
  - ../../README.md
  - ../systems-performance/README.md
  - ../linux-kernel-programming/README.md
  - ../../../network-roadmap.md
learning:
  topic: learning-modern-linux
  scope: durable
  level: 기본
  last_verified: 2026-09-05
  blocked_count: 0
  next_lesson: "08-01 Observability — 로그·메트릭·트레이스와 자원별 모니터링"
updated: 2026-09-05
---

# Learning Modern Linux 정독 인덱스

---

> 클라우드 네이티브 환경에서 리눅스를 쓰는 사람을 독자로 잡은 개론서입니다. 커널부터 셸·접근 제어·파일시스템·네트워크·관측까지를 한 권으로 훑고, 컨테이너를 특별한 주제가 아니라 리눅스 기능의 조합으로 다룹니다.

## 이 책을 여기 두는 이유

> `02_os` 는 언어가 아니라 실행 환경의 공통 기반을 모으는 자리입니다. 이 책은 그 기반을 한 바퀴 도는 개론이라 카테고리의 입구에 놓습니다.

같은 폴더의 다른 두 책과는 깊이와 시점이 다릅니다. [linux-kernel-programming](../linux-kernel-programming/README.md)은 커널 개발자의 시선으로 모듈을 짜고 커널을 빌드하는 책입니다. [systems-performance](../systems-performance/README.md)는 성능 분석가의 시선으로 방법론과 도구를 다룹니다. 이 책은 그 둘보다 얕은 대신 넓으며, 무엇보다 **컨테이너 환경을 전제로** 각 주제를 고릅니다.

읽는 이유는 하나 더 있습니다. [Kubernetes 네트워크 학습 로드맵](../../../network-roadmap.md)의 0단계가 이 책 7장 Networking 을 지정합니다. 그 7장을 읽으려면 네임스페이스와 커널의 어휘가 먼저 서 있어야 하고, 1장과 2장이 그 어휘를 만듭니다.



## 파트 구조

> 원서는 파트로 나뉘어 있지 않고 장 아홉과 부록 둘로 이어집니다. 성격이 갈리는 지점만 표시합니다.

| 구간 | 장 | 성격 |
|------|-----|------|
| 무대와 커널 | 1~2장 | 운영체제와 커널의 자리를 세우는 예비 구간 |
| 일상의 인터페이스 | 3~5장 | 셸·접근 제어·파일시스템. 손으로 매일 만지는 층 |
| 앱과 컨테이너 | 6장 | 부팅·패키지 관리·컨테이너. 이 책의 중심 |
| 네트워크와 관측 | 7~8장 | 로드맵 0단계가 지정한 7장이 여기 |
| 선택 구간 | 9장 · 부록 A·B | 저자가 선택 사항이라 밝힌 고급 주제와 레시피·도구 목록 |



## 장별 목표

> 각 장 앞머리에서 저자가 직접 적은 범위를 옮긴 것입니다. 추측으로 채운 칸은 없습니다.

| 장 | 제목 | 저자가 밝힌 범위 |
|:--:|------|------------------|
| 1 | Introduction to Linux | modern 의 뜻, 30년 약사, 운영체제의 역할, 배포판, 자원 가시성 |
| 2 | The Linux Kernel | 리눅스 아키텍처와 커널의 자리, CPU 계열, 커널 구성요소, 시스템 콜, 커널 확장 |
| 3 | Shells and Scripting | 셸 기본과 용어, Fish 같은 모던 셸, 설정과 일상 작업, 터미널 멀티플렉서, 안전하고 이식성 있는 스크립트와 린트·테스트 |
| 4 | Access Control | 사용자·프로세스·파일의 접근 관계, 샌드박싱과 접근 제어 유형, 사용자 정의와 관리, 권한, capability·seccomp·ACL 과 보안 관례 |
| 5 | Filesystems | 용어 정의, "모든 것은 파일" 추상의 구현, 커널이 정보를 드러내는 특수 목적 파일시스템, 일반 파일시스템 비교와 공통 연산 |
| 6 | Applications, Package Management, and Containers | 애플리케이션과 패키지의 정의, 부팅 과정과 systemd, 앱 공급망과 배포판별 패키지 관리, 컨테이너의 구성 요소와 도구, 모던 패키지 관리 |
| 7 | Networking | 하드웨어부터 HTTP·SSH 까지의 용어, 네트워크 스택과 프로토콜과 인터페이스, DNS, 애플리케이션 계층 프로토콜과 도구, 고급 주제 |
| 8 | Observability | 신호 유형(로그·메트릭·트레이스), 문제 해결과 성능 측정, 로그, 자원별 모니터링과 도구, 종단 간 구성 |
| 9 | Advanced Topics | IPC(시그널·네임드 파이프·유닉스 도메인 소켓), 가상 머신, 모던 배포판, Kerberos 와 PAM, 아직 주류가 아닌 쓰임새 |
| A | Helpful Recipes | 부록 |
| B | Modern Linux Tools | 부록 |



## 작성된 정독 노트

> 장 하나에 노트 하나가 원칙이고, 장이 길면 절로 나눕니다.

| 노트 | 장 | 한 줄 핵심 |
|------|:--:|-----------|
| [01-01. 하드웨어를 가리고 나면 무엇이 보일지를 정해야 한다](./01-01.%ED%95%98%EB%93%9C%EC%9B%A8%EC%96%B4%EB%A5%BC%20%EA%B0%80%EB%A6%AC%EA%B3%A0%20%EB%82%98%EB%A9%B4%20%EB%AC%B4%EC%97%87%EC%9D%B4%20%EB%B3%B4%EC%9D%BC%EC%A7%80%EB%A5%BC%20%EC%A0%95%ED%95%B4%EC%95%BC%20%ED%95%9C%EB%8B%A4.md) | 1 | 운영체제가 하드웨어를 가려 준 뒤에도 어느 자원이 어디까지 보이는지는 namespace 와 cgroups 가 따로 정합니다 |
| [02-01. 커널은 전부를 하지만 운영체제는 아니다](./02-01.%EC%BB%A4%EB%84%90%EC%9D%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%ED%95%98%EC%A7%80%EB%A7%8C%20%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EB%8A%94%20%EC%95%84%EB%8B%88%EB%8B%A4.md) | 2 | 셸도 `ps` 도 커널이 아니며, 커널이 기능을 드러내는 통로는 시스템 콜 하나입니다 |
| [03-01. 셸의 실체는 스트림과 변수와 종료 상태다](./03-01.%EC%85%B8%EC%9D%98%20%EC%8B%A4%EC%B2%B4%EB%8A%94%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%EA%B3%BC%20%EB%B3%80%EC%88%98%EC%99%80%20%EC%A2%85%EB%A3%8C%20%EC%83%81%ED%83%9C%EB%8B%A4.md) | 3 | 셸이 실제로 다루는 것은 스트림·변수·종료 상태 셋이고, 원서 실습 두 곳이 의도대로 동작하지 않습니다 |
| [03-02. 자주 치는 것일수록 짧아야 한다](./03-02.%EC%9E%90%EC%A3%BC%20%EC%B9%98%EB%8A%94%20%EA%B2%83%EC%9D%BC%EC%88%98%EB%A1%9D%20%EC%A7%A7%EC%95%84%EC%95%BC%20%ED%95%9C%EB%8B%A4.md) | 3 | 손이 덜 가게 만드는 법이 별칭·셸 교체·멀티플렉서 세 층으로 쌓입니다 |
| [03-03. bash 는 조용히 실패하므로 시끄럽게 만들어야 한다](./03-03.bash%20%EB%8A%94%20%EC%A1%B0%EC%9A%A9%ED%9E%88%20%EC%8B%A4%ED%8C%A8%ED%95%98%EB%AF%80%EB%A1%9C%20%EC%8B%9C%EB%81%84%EB%9F%BD%EA%B2%8C%20%EB%A7%8C%EB%93%A4%EC%96%B4%EC%95%BC%20%ED%95%9C%EB%8B%A4.md) | 3 | bash 가 기본으로 조용히 실패하므로 스켈레톤 세 줄이 그 침묵을 깹니다 |
| [04-01. 전부 아니면 전무에서 잘게 쪼개는 쪽으로](./04-01.%EC%A0%84%EB%B6%80%20%EC%95%84%EB%8B%88%EB%A9%B4%20%EC%A0%84%EB%AC%B4%EC%97%90%EC%84%9C%20%EC%9E%98%EA%B2%8C%20%EC%AA%BC%EA%B0%9C%EB%8A%94%20%EC%AA%BD%EC%9C%BC%EB%A1%9C.md) | 4 | root 냐 아니냐라는 이분법이 capability·seccomp·ACL 로 쪼개져 왔습니다 |
| [05-01. 모든 것이 파일이라는 말은 손잡이가 하나라는 뜻이다](./05-01.%EB%AA%A8%EB%93%A0%20%EA%B2%83%EC%9D%B4%20%ED%8C%8C%EC%9D%BC%EC%9D%B4%EB%9D%BC%EB%8A%94%20%EB%A7%90%EC%9D%80%20%EC%86%90%EC%9E%A1%EC%9D%B4%EA%B0%80%20%ED%95%98%EB%82%98%EB%9D%BC%EB%8A%94%20%EB%9C%BB%EC%9D%B4%EB%8B%A4.md) | 5 | 파일시스템이 주는 것은 저장 공간이 아니라 균일한 손잡이이고, VFS 가 그 손잡이를 블록 장치 밖으로 뻗습니다 |
| [06-01. 먼저 켜지는 것 하나가 나머지 전부를 켠다](./06-01.%EB%A8%BC%EC%A0%80%20%EC%BC%9C%EC%A7%80%EB%8A%94%20%EA%B2%83%20%ED%95%98%EB%82%98%EA%B0%80%20%EB%82%98%EB%A8%B8%EC%A7%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%EC%BC%A0%EB%8B%A4.md) | 6 | PID 1 이 나머지를 띄우고, 공급망의 세 자리가 그 앱을 날라 옵니다 |
| [06-02. 컨테이너의 새로움은 재료가 아니라 조합에 있다](./06-02.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%9D%98%20%EC%83%88%EB%A1%9C%EC%9B%80%EC%9D%80%20%EC%9E%AC%EB%A3%8C%EA%B0%80%20%EC%95%84%EB%8B%88%EB%9D%BC%20%EC%A1%B0%ED%95%A9%EC%97%90%20%EC%9E%88%EB%8B%A4.md) | 6 | 네임스페이스와 cgroups 와 CoW 는 Docker 이전에도 있었고, 새로운 것은 그것을 감싼 방식입니다 |
| [07-01. 결국은 선과 공기를 타고 다니는 비트다](./07-01.%EA%B2%B0%EA%B5%AD%EC%9D%80%20%EC%84%A0%EA%B3%BC%20%EA%B3%B5%EA%B8%B0%EB%A5%BC%20%ED%83%80%EA%B3%A0%20%EB%8B%A4%EB%8B%88%EB%8A%94%20%EB%B9%84%ED%8A%B8%EB%8B%A4.md) | 7 | 추상이 원격을 로컬처럼 보이게 하지만 아래에는 링크 계층과 인터넷 계층이 있습니다 |
| [07-02. 포트가 있어야 서비스를 가리킬 수 있고 이름이 있어야 사람이 기억한다](./07-02.%ED%8F%AC%ED%8A%B8%EA%B0%80%20%EC%9E%88%EC%96%B4%EC%95%BC%20%EC%84%9C%EB%B9%84%EC%8A%A4%EB%A5%BC%20%EA%B0%80%EB%A6%AC%ED%82%AC%20%EC%88%98%20%EC%9E%88%EA%B3%A0%20%EC%9D%B4%EB%A6%84%EC%9D%B4%20%EC%9E%88%EC%96%B4%EC%95%BC%20%EC%82%AC%EB%9E%8C%EC%9D%B4%20%EA%B8%B0%EC%96%B5%ED%95%9C%EB%8B%A4.md) | 7 | 주소는 기계까지만 데려다주므로 포트가 서비스를 가리키고 DNS 가 이름을 맡습니다 |
| [07-03. 주고받는 일은 결국 몇 개의 명령으로 줄어든다](./07-03.%EC%A3%BC%EA%B3%A0%EB%B0%9B%EB%8A%94%20%EC%9D%BC%EC%9D%80%20%EA%B2%B0%EA%B5%AD%20%EB%AA%87%20%EA%B0%9C%EC%9D%98%20%EB%AA%85%EB%A0%B9%EC%9C%BC%EB%A1%9C%20%EC%A4%84%EC%96%B4%EB%93%A0%EB%8B%A4.md) | 7 | 웹의 세 축 위에서 curl 과 ssh 와 rsync 가 일하고, tshark 한 줄에 네 층이 다 보입니다 |
| 미작성 | 8~9 · 부록 | |



## 학습 상태

> 다음 세션이 콜드 스타트로 시작하지 않도록 진입 조건을 적어 둡니다.

| 항목 | 값 |
|------|-----|
| 난이도 레벨 | 기본 |
| 진행률 | 7 / 11 (본문 9장 + 부록 2) · 3장과 7장은 길어 노트 셋으로, 6장은 둘로 나눔 |
| 최근 검증 | 2026-09-05 · 1~7장 형식 센서 전수(도식 66장 error 0) + 적대적 내용 검증 전수. 주장한 원문 정오는 모두 반박 실패로 성립, 노트 자체의 오류(도식 층 오배치·원서 절단분 채움)는 수정 완료 |
| 막힌 지점 | 없음 |
| 다음 레슨 후보 | 8장 Observability. 3장·5장·7장이 모두 문제 해결 도구를 이 장으로 미뤄 뒀습니다 |
| 발견한 원문 정오 | 25건 — 1장 1(CPU 모델명) · 2장 4(단위 목록 문구·eBPF 최소 버전·`mallocopt` 표기·시스템 콜 명령어) · 3장 4(`set` 으로 변수 만들기·`unset $VAR`·Ctrl+Z 서술·날짜 예제 입력값) · 4장 1(`/proc/$pid` 로 실제 UID 조회) · 5장 5(`mount -a`·`/proc/self/net/arp`·`devfs` 이름·`var` 행 복붙·AUFS 시제) · 6장 5(`initd`·Ruby 칸 Rails·`ENTRYPOINT` vs `CMD`·`prune -all`·`ARGS`) · 7장 5(멀티캐스트 `/24`·인프라 TLD 예·SRV 를 TTL 로 읽음·URI 순서·`rsync` 목적지 오타) |

원서 PDF 는 Google Drive 의 `내 드라이브/book/Learning Modern Linux/` 에 장별로 나뉘어 있습니다. 1장은 2026-09-05 에 추가됐고, 나머지는 2026-07-16 에 함께 받은 파일입니다.



## 출처와 톤

- 원서: 《Learning Modern Linux》 Michael Hausenblas, O'Reilly, 2022년
- 노트는 합니다체로 통일합니다. 같은 폴더의 기존 두 책 노트가 다른 톤이어도 따라가지 않습니다.
- 사실·수치·코드는 원서 PDF 에서 추출한 것만 씁니다. 책 밖 보강은 절을 나누고 공식 1차 자료 링크를 각주로 남깁니다.
- 원문의 오류는 조용히 고치지 않고 `원문 정오` 인용 블록으로 병기합니다. 원서를 다시 폈을 때 혼동하지 않게 하는 것이 목적입니다.



## 관련 문서

- [02_os — OS 공통 기반](../../README.md) — 이 카테고리의 MOC
- [systems-performance](../systems-performance/README.md) — 같은 주제를 성능 분석 관점에서 깊게
- [linux-kernel-programming](../linux-kernel-programming/README.md) — 같은 주제를 커널 개발자 관점에서 깊게
- [Kubernetes 네트워크 학습 로드맵](../../../network-roadmap.md) — 이 책 7장이 0단계로 지정된 자리
