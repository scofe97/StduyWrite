---
title: 02_os/troubleshooting — OS 트러블슈팅 사례집
tags: [moc, troubleshooting, linux, network, incident]
status: final
related:
  - ../README.md
  - ../networking/README.md
  - ../kernel/README.md
  - ../../08_cloud/troubleshooting/README.md
updated: 2026-09-05
---

# 02_os/troubleshooting
---
> 리눅스 호스트에서 마주치는 장애를 증상에서 원인으로 역추적하는 사례집입니다. `networking/`·`kernel/`이 메커니즘을 설명한다면 여기는 그 메커니즘이 깨졌을 때 무엇을 어떤 순서로 확인하는지를 다룹니다.

문서 하나가 하나의 주제를 맡고, 그 안의 `## 사례`가 개별 장애 하나에 해당합니다. 사례마다 증상과 주어진 출력, 원인, 조치, 재발 방지가 같은 순서로 들어 있습니다.

사례 41건은 [Infratice](https://github.com/kiku99/Infratice)의 `content/problems/` 에서 가져와 재구성했습니다. 원문은 정답을 가린 문제 형식이고 이 문서들은 해설을 이어 붙인 형태라, 먼저 사이트에서 풀어 본 뒤 여기서 대조하는 순서를 권합니다.



## 문서

> 장 번호가 자원의 종류를 나눕니다. 01 디스크, 02 프로세스와 자원, 03 서비스 가용성, 04 로그와 자동화, 05 네트워크입니다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 01-01 | [디스크 포화 — 용량·inode·마운트](01-01.%EB%94%94%EC%8A%A4%ED%81%AC%20%ED%8F%AC%ED%99%94%20%E2%80%94%20%EC%9A%A9%EB%9F%89%C2%B7inode%C2%B7%EB%A7%88%EC%9A%B4%ED%8A%B8.md) | 디스크가 찼다는 신호 하나에서 블록·inode·마운트 세 갈래를 어떻게 가르는가? |
| 01-02 | [로그가 디스크를 먹는 방식 — 급증 추적과 용량 산정](01-02.%EB%A1%9C%EA%B7%B8%EA%B0%80%20%EB%94%94%EC%8A%A4%ED%81%AC%EB%A5%BC%20%EB%A8%B9%EB%8A%94%20%EB%B0%A9%EC%8B%9D%20%E2%80%94%20%EA%B8%89%EC%A6%9D%20%EC%B6%94%EC%A0%81%EA%B3%BC%20%EC%9A%A9%EB%9F%89%20%EC%82%B0%EC%A0%95.md) | 로그가 파티션을 채우는 세 가지 실패 지점은 어디이고 무엇이 진짜 수정인가? |
| 01-03 | [파일 정리와 백업 — 빈 디렉터리·재귀 백업·크기 분할](01-03.%ED%8C%8C%EC%9D%BC%20%EC%A0%95%EB%A6%AC%EC%99%80%20%EB%B0%B1%EC%97%85%20%E2%80%94%20%EB%B9%88%20%EB%94%94%EB%A0%89%ED%84%B0%EB%A6%AC%C2%B7%EC%9E%AC%EA%B7%80%20%EB%B0%B1%EC%97%85%C2%B7%ED%81%AC%EA%B8%B0%20%EB%B6%84%ED%95%A0.md) | `find`로 대상을 고르고 처리할 때 무엇을 먼저 확인해야 사고가 안 나는가? |
| 02-01 | [프로세스 계보 추적 — 소유자·트리·서비스·좀비](02-01.%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%20%EA%B3%84%EB%B3%B4%20%EC%B6%94%EC%A0%81%20%E2%80%94%20%EC%86%8C%EC%9C%A0%EC%9E%90%C2%B7%ED%8A%B8%EB%A6%AC%C2%B7%EC%84%9C%EB%B9%84%EC%8A%A4%C2%B7%EC%A2%80%EB%B9%84.md) | 수백 개 프로세스에서 손봐야 할 하나를 어떤 집계 축으로 좁히는가? |
| 02-02 | [자원 병목 — CPU 우선순위와 메모리 누수](02-02.%EC%9E%90%EC%9B%90%20%EB%B3%91%EB%AA%A9%20%E2%80%94%20CPU%20%EC%9A%B0%EC%84%A0%EC%88%9C%EC%9C%84%EC%99%80%20%EB%A9%94%EB%AA%A8%EB%A6%AC%20%EB%88%84%EC%88%98.md) | 느리다는 신고를 총량 문제와 배분 문제로 어떻게 가르는가? |
| 03-01 | [서비스 기동 실패 — 포트 충돌과 502](03-01.%EC%84%9C%EB%B9%84%EC%8A%A4%20%EA%B8%B0%EB%8F%99%20%EC%8B%A4%ED%8C%A8%20%E2%80%94%20%ED%8F%AC%ED%8A%B8%20%EC%B6%A9%EB%8F%8C%EA%B3%BC%20502.md) | 502 와 기동 실패가 사실은 같은 원인인 이유는 무엇인가? |
| 03-02 | [접속과 서비스 복구 — SSH 잠금·실패한 유닛](03-02.%EC%A0%91%EC%86%8D%EA%B3%BC%20%EC%84%9C%EB%B9%84%EC%8A%A4%20%EB%B3%B5%EA%B5%AC%20%E2%80%94%20SSH%20%EC%9E%A0%EA%B8%88%C2%B7%EC%8B%A4%ED%8C%A8%ED%95%9C%20%EC%9C%A0%EB%8B%9B.md) | `MaxAuthTries` 와 `StartLimitBurst` 같은 상한값은 무엇을 기준으로 정하는가? |
| 03-03 | [디스크 I/O 포화와 우선순위 분리](03-03.%EB%94%94%EC%8A%A4%ED%81%AC%20I-O%20%ED%8F%AC%ED%99%94%EC%99%80%20%EC%9A%B0%EC%84%A0%EC%88%9C%EC%9C%84%20%EB%B6%84%EB%A6%AC.md) | 디스크가 포화일 때 늘리는 대신 순서를 정하면 무엇이 달라지는가? |
| 04-01 | [로그 텍스트 다루기 — 검색·분할·정렬·타임스탬프](04-01.%EB%A1%9C%EA%B7%B8%20%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EB%8B%A4%EB%A3%A8%EA%B8%B0%20%E2%80%94%20%EA%B2%80%EC%83%89%C2%B7%EB%B6%84%ED%95%A0%C2%B7%EC%A0%95%EB%A0%AC%C2%B7%ED%83%80%EC%9E%84%EC%8A%A4%ED%83%AC%ED%94%84.md) | 장애 조사에서 로그를 읽을 수 있는 상태로 만드는 준비는 무엇인가? |
| 04-02 | [반복 작업 자동화 — 설정 일괄 변경과 백업 스케줄](04-02.%EB%B0%98%EB%B3%B5%20%EC%9E%91%EC%97%85%20%EC%9E%90%EB%8F%99%ED%99%94%20%E2%80%94%20%EC%84%A4%EC%A0%95%20%EC%9D%BC%EA%B4%84%20%EB%B3%80%EA%B2%BD%EA%B3%BC%20%EB%B0%B1%EC%97%85%20%EC%8A%A4%EC%BC%80%EC%A4%84.md) | 자동화가 실수를 줄이면서 동시에 실수의 크기를 키우는 이유는 무엇인가? |
| 05-01 | [포트와 소켓 — 고갈·점유·포워딩·레이트 리밋](05-01.%ED%8F%AC%ED%8A%B8%EC%99%80%20%EC%86%8C%EC%BC%93%20%E2%80%94%20%EA%B3%A0%EA%B0%88%C2%B7%EC%A0%90%EC%9C%A0%C2%B7%ED%8F%AC%EC%9B%8C%EB%94%A9%C2%B7%EB%A0%88%EC%9D%B4%ED%8A%B8%20%EB%A6%AC%EB%B0%8B.md) | LISTEN·ESTABLISHED·TIME_WAIT 은 각각 어떤 종류의 문제를 가리키는가? |
| 05-02 | [라우팅과 DNS — 경로 추가·수정과 이름 해석](05-02.%EB%9D%BC%EC%9A%B0%ED%8C%85%EA%B3%BC%20DNS%20%E2%80%94%20%EA%B2%BD%EB%A1%9C%20%EC%B6%94%EA%B0%80%C2%B7%EC%88%98%EC%A0%95%EA%B3%BC%20%EC%9D%B4%EB%A6%84%20%ED%95%B4%EC%84%9D.md) | `unreachable` 과 `Could not resolve host` 는 어느 계층의 실패인가? |
| 05-03 | [패킷 캡처와 손실 진단](05-03.%ED%8C%A8%ED%82%B7%20%EC%BA%A1%EC%B2%98%EC%99%80%20%EC%86%90%EC%8B%A4%20%EC%A7%84%EB%8B%A8.md) | 네트워크 문제와 애플리케이션 문제를 패킷으로 어떻게 가르는가? |



## 어디부터 읽나

> 지금 장애를 겪고 있으면 증상에 맞는 장으로 바로 갑니다. 학습이 목적이면 01장부터 순서대로 읽는 편이 낫습니다.

장애 대응 중이라면 증상으로 찾습니다. 디스크가 찼으면 01장, 프로세스가 이상하면 02장, 서비스가 안 뜨면 03장, 연결이 안 되면 05장입니다.

학습이 목적이면 번호 순서가 곧 읽기 순서입니다. 01장과 02장이 자원의 상한을 다루고 03장이 그 상한이 서비스로 드러나는 지점을 다루며, 04장과 05장이 조사 도구와 네트워크로 넓어집니다.

전체를 관통하는 습관 셋은 어느 장에서나 반복됩니다. 죽이기 전에 기록을 남기는 것, 응급 조치와 재발 방지를 구분하는 것, 도구가 안 보여 준 것을 없다고 읽지 않는 것입니다.



## 트러블슈팅 연습 사이트

> 아래 목록은 각 사이트를 직접 열어 제목과 소개 문구를 확인한 것입니다(2026-09-05 기준). 유료 여부와 무료 범위는 자주 바뀌므로 링크에서 직접 확인합니다.

| 사이트 | 방식 | 다루는 범위 |
|--------|------|------------|
| [Infratice](https://infratice.co.kr/) | 정적 문제 — 로그·설정만 보고 원인을 추론하고 AI로 풀이를 검토 | Linux · Kubernetes · Network · CI/CD · Monitoring (한국어) |
| [SadServers](https://sadservers.com/scenarios) | 브라우저 안 실서버에 붙어 제한 시간 안에 복구 | Linux 트러블슈팅 랩, 면접·채용 평가 겸용 |
| [iximiuz Labs](https://labs.iximiuz.com/) | 브라우저나 SSH로 실서버 실습, 학습 경로 제공 | Linux · Docker · Kubernetes · Networking |
| [Killercoda](https://killercoda.com/) | 브라우저 터미널 시나리오, 직접 시나리오 작성 가능 | DevOps · Linux · Kubernetes · CKA/CKS/CKAD |
| [Killer Shell](https://killer.sh/) | 자격 시험 시뮬레이터 | CKA · CKS · CKAD · LFCS · CNPE |
| [KodeKloud](https://kodekloud.com/) | 핸즈온 랩과 가이드 영상 | DevOps · Cloud · AI 전반 |
| [Deadnodes](https://deadnodes.com/) | 실습·팀 챌린지·면접 워크플로를 묶은 플랫폼 | 시스템 엔지니어링 실습 |
| [DevOpsEngine Labs](https://devopsengine.cloud/labs/) | 핸즈온 랩 | Kubernetes · Linux · CI/CD · 트러블슈팅 |
| [Kubernetes Troubleshooting (LFWS313)](https://training.linuxfoundation.org/training/kubernetes-troubleshooting-lfws313/) | Linux Foundation 공식 과정, 랩과 실사례 중심 | Kubernetes |
| [DevOps-Learn-By-Doing](https://github.com/deepakkumar-platform/DevOps-Learn-By-Doing) | 무료 랩·챌린지 큐레이션 저장소 | Linux 부터 Kubernetes 까지 |

성격으로 나누면 셋입니다.

- 정적 문제: Infratice — 환경 없이 로그와 설정만 읽습니다
- 대화형 셸: SadServers · iximiuz Labs · Killercoda · Killer Shell — 실제 서버를 줍니다
- 학습 과정: LFWS313 · DevOps-Learn-By-Doing — 커리큘럼과 큐레이션입니다

환경 구축 비용 없이 판단력만 훈련하려면 첫째 갈래가 맞습니다. 손에 익히는 것이 목적이면 둘째 갈래로 갑니다.



## 상위·이웃

> 이 폴더가 어느 문서들 사이에 놓이는지를 정리합니다.

- 상위: [02_os MOC](../README.md)
- 이웃: [02_os/networking/](../networking/README.md) — 여기 사례들이 딛고 선 커널 네트워크 메커니즘
- 이웃: [02_os/kernel/](../kernel/README.md) — namespace·cgroup 같은 격리와 자원 제한 메커니즘
- 짝: [08_cloud/troubleshooting/](../../08_cloud/troubleshooting/README.md) — 같은 사례집의 쿠버네티스 편

> 사례 원문은 [Infratice](https://github.com/kiku99/Infratice)(MIT, `0aba7df`)의 `content/problems/` 에서 가져와 재구성했습니다.
