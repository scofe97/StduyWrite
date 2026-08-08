---
title: Container Security — 정독 인덱스
tags: [moc, study-index, book, container-security, linux-kernel, namespace, cgroup, seccomp, supply-chain]
status: final
source:
  - 《Container Security: Fundamental Technology Concepts that Protect Containerized Applications》(Liz Rice, O'Reilly, 2020, ISBN 978-1492056706) — 1판
  - https://www.amazon.com/Container-Security-Fundamental-Containerized-Applications/dp/1492056707  # 1판 서지 확인 (2026-08-08 조회)
  - https://www.oreilly.com/library/view/container-security-2nd/9798341627697/  # 2판 존재 확인 — 이 노트는 1판 기준 (2026-08-08 조회)
related:
  - ../networking-and-kubernetes/README.md
  - ../kubernetes-in-action/README.md
  - ../kubernetes-patterns/README.md
  - ../../README.md
updated: 2026-08-09
---

# Container Security — 정독 인덱스
---
> 이 폴더는 『Container Security』(Liz Rice, O'Reilly, 2020)를 장 단위로 정독하며 정리하는 **책-종속 학습노트**입니다. 챕터 PDF를 하나씩 읽은 뒤 한 편씩 채워 넣습니다.

## 이 책을 여기 두는 이유

`08_cloud`는 "클러스터 내부에서 어떻게 돌아가는가"를 다루는 카테고리입니다. 이 책은 그 질문을 **격리 경계** 축으로 파고듭니다. 컨테이너를 만들어 내는 Linux 커널 기능(namespace·cgroup·capability·seccomp)이 실제로 어떤 보안 경계를 세우는지, 그 경계가 어디서 얼마나 쉽게 뚫리는지를 다룹니다. 저자는 1판 집필 당시 Aqua Security에서 오픈소스 엔지니어링을 이끌며 Trivy·kube-bench 같은 컨테이너 보안 도구를 만들던 사람이라, 관점이 "무엇을 설치하라"가 아니라 "이 격리가 정말 격리인가"입니다.[^author]

같은 폴더의 형제 책들과는 보는 층이 다릅니다. [『Kubernetes in Action』](../kubernetes-in-action/README.md)이 오브젝트 중심(무엇을 배포하는가), [『Networking and Kubernetes』](../networking-and-kubernetes/README.md)가 패킷 중심(트래픽이 어떻게 흐르는가)이라면, 이 책은 **경계 중심**(무엇이 무엇을 못 보게 막고 있는가)입니다. 그래서 namespace·cgroup처럼 이미 다른 노트에서 다룬 주제가 다시 나와도 질문이 다릅니다. 저쪽이 "컨테이너는 이렇게 격리된다"로 끝났다면, 여기는 "그 격리를 깨는 설정은 무엇인가"에서 시작합니다.

겹치는 개념의 기초 설명은 기존 노트로 링크를 걸어 위임하고, 이 폴더에는 **보안 관점에서 새로 얻는 것만** 남깁니다. 구체적으로 Linux namespace·cgroup의 일반 동작은 [`networking-and-kubernetes/03-01`](../networking-and-kubernetes/03-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%9D%98%20%ED%83%84%EC%83%9D%20%E2%80%94%20%EC%95%B1%20%EC%8B%A4%ED%96%89%EC%9D%98%20%EC%A7%84%ED%99%94%EC%99%80%20%EA%B2%A9%EB%A6%AC%20%ED%94%84%EB%A6%AC%EB%AF%B8%ED%8B%B0%EB%B8%8C.md)이, 네트워크 정책의 일반 동작은 [`networking-and-kubernetes/04-03`](../networking-and-kubernetes/04-03.NetworkPolicy%EC%99%80%20DNS%20%E2%80%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%95%88%EC%9D%98%20%EB%B0%A9%ED%99%94%EB%B2%BD%EA%B3%BC%20%EC%9D%B4%EB%A6%84.md)이 맡습니다.

## 장별 목표

> 각 장 PDF 앞머리의 저자 선언을 `pdftotext`로 추출해 근거로 삼았습니다. 원문에 없는 목표를 추측해 넣지 않습니다.

| 장 | 제목 | 저자가 선언한 목표 | 주요 토픽 |
|----|------|------------------|----------|
| 1 | Container Security Threats | 컨테이너 배포에 공통된 잠재 위협을 열거하고, 보안 도구·프로세스를 판단할 때 기준이 될 보안 원칙을 소개 | 리스크·위협·완화, 위협 모델, 보안 경계, 멀티테넌시, 보안 원칙 5가지 |
| 2 | Linux System Calls, Permissions, and Capabilities | 컨테이너 보안에 영향을 주는 Linux 기본 기능을 다룸 — 시스템 콜, 파일 권한, capability를 거쳐 권한 상승으로 마무리 | syscall, 파일 권한, capability, 권한 상승 |
| 3 | Control Groups | 컨테이너를 만드는 근본 building block 중 하나인 cgroup을 배움 — 자원 독점으로 다른 프로세스를 방해하지 못하게 하는 관점 | cgroup 계층, cgroup 생성, Docker의 cgroup 사용, cgroup v2 |
| 4 | Container Isolation | 컨테이너가 실제로 어떻게 동작하는지 밝혀, 컨테이너를 둘러싼 보안 경계의 강도를 스스로 평가할 수 있게 함 | namespace, chroot, cgroup 결합, 컨테이너 vs VM 대비 |
| 5 | Virtual Machines | VM의 동작 방식을 확실히 이해해 컨테이너와의 차이를 근거 있게 논할 수 있게 함 | BIOS·부팅, VMM(하이퍼바이저), 트랩앤에뮬레이트, 격리 강도 |
| 6 | Container Images | 이미지가 무엇을 담고 런타임이 어떻게 쓰는지 살핀 뒤, 빌드·저장·취득 단계의 보안 함의와 공격 벡터를 다룸 | 루트 파일시스템, 이미지 설정, 레지스트리, 빌드 보안 |
| 7 | Software Vulnerabilities in Images | 취약점이 무엇이고 어떻게 공표·추적되는지 다룬 뒤, 컨테이너 세계에서 완전히 재발명된 패치 프로세스를 설명 | CVE, 취약점 연구·공개, 이미지 스캐닝, 스캐닝 운영 |
| 8 | Strengthening Container Isolation | 같은 호스트 워크로드 간 격리를 강화하는 고급 도구·기법을 다룸 — 샌드박싱 관점 | seccomp, AppArmor, SELinux, gVisor, Kata Containers |
| 9 | Breaking Container Isolation | 컨테이너 격리가 사실상 깨지도록 설정하는 것이 얼마나 쉬운지 보임 — 의도적 사용과 심각한 위험을 함께 | 기본 root 실행, --privileged, 민감 디렉토리 마운트, Docker 소켓 |
| 10 | Container Network Security | 컨테이너 배포의 네트워크 보안을 사고할 수 있는 멘탈 모델을 제공 | 컨테이너 방화벽, 7계층 모델, 네트워크 정책 모범사례, 서비스 메시 |
| 11 | Securely Connecting Components with TLS | 컴포넌트가 서로를 식별하고 안전한 연결을 맺어 악의적 컴포넌트가 끼어들지 못하게 하는 방법을 다룸 | 보안 연결, 인증서, 키, CA, TLS 핸드셰이크 |
| 12 | Passing Secrets to Containers | 시크릿의 바람직한 속성을 따진 뒤 컨테이너에 시크릿을 전달하는 선택지를 탐색하고 Kubernetes 네이티브 지원으로 마무리 | 시크릿 속성, 전달 방식 비교, Kubernetes Secret |
| 13 | Container Runtime Protection | 이미지 단위로 기대 동작 프로파일을 정의해 그 이미지에서 뜬 모든 컨테이너의 트래픽·동작을 통제 | 이미지 프로파일, 네트워크·실행·파일 접근 프로파일, 드리프트 방지 |
| 14 | Containers and the OWASP Top 10 | OWASP Top 10 웹 애플리케이션 보안 리스크를 컨테이너 고유의 보안 접근법과 연결 | 인젝션, 인증 취약, 민감정보 노출 등 10대 리스크 |
| 부록 | Conclusions · Security Checklist | 책이 남기려 한 네 갈래를 되짚고, 배포 앞에서 스스로 물을 19개 질문으로 바꿈 | 계층별 점검 항목, 항목↔본문 절 대응 |

## 작성된 정독 노트

> 원문을 정독해 편을 작성하는 대로 채웁니다. 아직 작성하지 않은 장은 상태만 "작성 예정"으로 두고, 본문 내용은 원문 도착 전까지 채우지 않습니다.

| 편 | 제목 | 상태 |
|----|------|------|
| [01-01](./01-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%B3%B4%EC%95%88%20%EC%9C%84%ED%98%91%20%E2%80%94%20%EC%9C%84%ED%98%91%20%EB%AA%A8%EB%8D%B8%EB%B6%80%ED%84%B0%20%EB%B3%B4%EC%95%88%20%EC%9B%90%EC%B9%99%EA%B9%8C%EC%A7%80.md) | 컨테이너 보안 위협 — 위협 모델부터 보안 원칙까지 (Ch1 전체) | 완료 |
| [02-01](./02-01.Linux%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%BD%9C%C2%B7%EA%B6%8C%ED%95%9C%C2%B7capability%20%E2%80%94%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%B3%B4%EC%95%88%EC%9D%98%20%EB%B0%94%EB%8B%A5.md) | Linux 시스템 콜·권한·capability — 컨테이너 보안의 바닥 (Ch2 전체) | 완료 |
| [03-01](./03-01.Control%20Group%20%E2%80%94%20%EC%9E%90%EC%9B%90%EC%9D%84%20%EC%A0%9C%ED%95%9C%ED%95%B4%20%EA%B5%B6%EA%B8%B0%EA%B8%B0%EB%A5%BC%20%EB%A7%89%EB%8B%A4.md) | Control Group — 자원을 제한해 굶기기를 막다 (Ch3 전체) | 완료 |
| [04-01](./04-01.namespace%EC%99%80%20%EB%A3%A8%ED%8A%B8%20%EB%94%94%EB%A0%89%ED%86%A0%EB%A6%AC%20%E2%80%94%20%EA%B2%A9%EB%A6%AC%EB%A5%BC%20%EB%A7%8C%EB%93%9C%EB%8A%94%20%EB%91%90%20%EC%9E%A5%EC%B9%98.md) | namespace와 루트 디렉토리 — 격리를 만드는 두 장치 (Ch4 전반부) | 완료 |
| [04-02](./04-02.%EB%82%98%EB%A8%B8%EC%A7%80%20namespace%EC%99%80%20%ED%98%B8%EC%8A%A4%ED%8A%B8%EC%97%90%EC%84%9C%20%EB%B3%B8%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88.md) | 나머지 namespace와 호스트에서 본 컨테이너 (Ch4 후반부) | 완료 |
| [05-01](./05-01.%EA%B0%80%EC%83%81%EB%A8%B8%EC%8B%A0%20%E2%80%94%20%EC%99%9C%20VM%20%EA%B2%A9%EB%A6%AC%EA%B0%80%20%EB%8D%94%20%EA%B0%95%ED%95%98%EB%8B%A4%EA%B3%A0%20%ED%95%98%EB%8A%94%EA%B0%80.md) | 가상머신 — 왜 VM 격리가 더 강하다고 하는가 (Ch5 전체) | 완료 |
| [06-01](./06-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%ED%95%B4%EB%B6%80%20%E2%80%94%20%EB%91%90%20%EB%B6%80%EB%B6%84%EA%B3%BC%20%EC%B8%B5%EA%B3%BC%20%EC%8B%9D%EB%B3%84%EC%9E%90.md) | 컨테이너 이미지 해부 — 두 부분과 층과 식별자 (Ch6 전반부) | 완료 |
| [06-02](./06-02.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EA%B3%B5%EA%B8%89%EB%A7%9D%20%EB%B3%B4%EC%95%88%20%E2%80%94%20%EB%B9%8C%EB%93%9C%EB%B6%80%ED%84%B0%20%EB%B0%B0%ED%8F%AC%EA%B9%8C%EC%A7%80.md) | 이미지 공급망 보안 — 빌드부터 배포까지 (Ch6 후반부) | 완료 |
| [07-01](./07-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%86%8D%20%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4%20%EC%B7%A8%EC%95%BD%EC%A0%90%20%E2%80%94%20CVE%EB%B6%80%ED%84%B0%20%EC%8A%A4%EC%BA%94%20%EC%9A%B4%EC%98%81%EA%B9%8C%EC%A7%80.md) | 이미지 속 소프트웨어 취약점 — CVE부터 스캔 운영까지 (Ch7 전체) | 완료 |
| [08-01](./08-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC%20%EA%B0%95%ED%99%94%20%E2%80%94%20%EC%83%8C%EB%93%9C%EB%B0%95%EC%8B%B1%EC%9D%98%20%EC%84%B8%20%EA%B0%88%EB%9E%98.md) | 컨테이너 격리 강화 — 샌드박싱의 세 갈래 (Ch8 전체) | 완료 |
| [09-01](./09-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC%20%EA%B9%A8%EB%9C%A8%EB%A6%AC%EA%B8%B0%20%E2%80%94%20%EC%84%A4%EC%A0%95%20%ED%95%98%EB%82%98%EB%A1%9C%20%EB%AC%B4%EB%84%88%EC%A7%80%EB%8A%94%20%EA%B2%BD%EA%B3%84.md) | 컨테이너 격리 깨뜨리기 — 설정 하나로 무너지는 경계 (Ch9 전체) | 완료 |
| [10-01](./10-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EB%B3%B4%EC%95%88%20%E2%80%94%20%EA%B3%84%EC%B8%B5%EB%B3%84%EB%A1%9C%20%EB%82%98%EB%88%A0%20%EB%A7%89%EA%B8%B0.md) | 컨테이너 네트워크 보안 — 계층별로 나눠 막기 (Ch10 전체) | 완료 |
| [11-01](./11-01.TLS%EB%A1%9C%20%EC%BB%B4%ED%8F%AC%EB%84%8C%ED%8A%B8%20%EC%95%88%EC%A0%84%ED%95%98%EA%B2%8C%20%EC%97%B0%EA%B2%B0%ED%95%98%EA%B8%B0%20%E2%80%94%20%ED%82%A4%C2%B7%EC%9D%B8%EC%A6%9D%EC%84%9C%C2%B7CA%EC%9D%98%20%EC%97%AD%ED%95%A0.md) | TLS로 컴포넌트 안전하게 연결하기 — 키·인증서·CA의 역할 (Ch11 전체) | 완료 |
| [12-01](./12-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%97%90%20%EC%8B%9C%ED%81%AC%EB%A6%BF%20%EC%A0%84%EB%8B%AC%ED%95%98%EA%B8%B0%20%E2%80%94%20%EB%8B%A4%EC%84%AF%20%EA%B2%BD%EB%A1%9C%EC%99%80%20root%EB%9D%BC%EB%8A%94%20%EC%B2%9C%EC%9E%A5.md) | 컨테이너에 시크릿 전달하기 — 다섯 경로와 root라는 천장 (Ch12 전체) | 완료 |
| [13-01](./13-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%9F%B0%ED%83%80%EC%9E%84%20%EB%B3%B4%ED%98%B8%20%E2%80%94%20%EC%A0%95%EC%83%81%EC%9D%84%20%EC%A0%95%EC%9D%98%ED%95%B4%20%EC%9D%B4%EC%83%81%EC%9D%84%20%EC%9E%A1%EB%8B%A4.md) | 컨테이너 런타임 보호 — 정상을 정의해 이상을 잡다 (Ch13 전체) | 완료 |
| [14-01](./14-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%99%80%20OWASP%20Top%2010%20%E2%80%94%20%EC%9B%B9%20%EB%A6%AC%EC%8A%A4%ED%81%AC%EB%A5%BC%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%8C%80%EC%9D%91%EC%9C%BC%EB%A1%9C%20%EC%9E%87%EB%8B%A4.md) | 컨테이너와 OWASP Top 10 — 웹 리스크를 컨테이너 대응으로 잇다 (Ch14 전체) | 완료 |
| [15-01](./15-01.%EB%A7%BA%EC%9D%8C%EB%A7%90%EA%B3%BC%20%EB%B3%B4%EC%95%88%20%EC%B2%B4%ED%81%AC%EB%A6%AC%EC%8A%A4%ED%8A%B8%20%E2%80%94%20%EC%97%B4%EC%95%84%ED%99%89%20%EA%B0%9C%20%EC%A7%88%EB%AC%B8%EC%9C%BC%EB%A1%9C%20%EB%90%98%EC%A7%9A%EA%B8%B0.md) | 맺음말과 보안 체크리스트 — 열아홉 개 질문으로 되짚기 (부록 2편 통합) | 완료 |

## 학습 상태

> 세션을 새로 열 때 이 표부터 읽습니다. 정독본의 STATE.md 대용입니다.

| 항목 | 현재 값 |
|------|--------|
| 진행률 | **14/14 장 + 부록 — 완독**. 정독 노트 17편 |
| 난이도 레벨 | 부록은 새 개념이 없는 **점검 장치**입니다(Conclusions 363단어 + Checklist 549단어 = 912단어, 한 편으로 통합). 반드시 붙잡을 것 둘 — 체크리스트가 **명령문이 아니라 질문문**이라 여섯 해가 지나도 항목이 낡지 않았다는 점, 그리고 **답이 바뀐 항목은 전부 쿠버네티스 기능이고 그대로인 항목은 전부 커널 경계**라는 점. 후자가 이 책이 커널에서 시작해 위로 올라간 구성을 택한 것의 사후 정당화입니다 |
| 막힌 지점 | 없음 |
| 다음 레슨 후보 | 없음 — 완독. 복습으로 넘어갈 시점이며, 15-01 §4의 항목↔편 대응표가 복습 진입점 역할을 합니다 |
| 최근 검증 결과 | 15-01 §16 통과(한다체 0, AI 강조어 0, `##` 빈줄 위반 0, 시각화 3, 줄수 185, 마크다운 호환 exit 0), 벽 단락 0곳. §18 원문 대조 전 항목 일치("not absolutely comprehensive"·"off to a good start"·"unit not just of deployment but also of security"·"The more layers of defense"·"come what may"·피드백 창구) (2026-08-09) |
| 원문 정오 누적 | 5건 — 2장 `--no-new-privileges` → `--security-opt no-new-privileges` · 3장 "런타임이 v2 미지원(2020)" → 현재 역전(runc rc93+, K8s 1.25 GA, 1.35에서 v1 사용 중단) · 4장 "K8s는 user namespace 전혀 미지원(2020)" → **v1.36에서 stable·기본 활성**(`hostUsers: false`) · **8장 "K8s seccomp은 Alpha·PodSecurityPolicy 애노테이션"** → **v1.19 stable**, `securityContext.seccompProfile` 필드(PSP 자체가 제거됨) · **9장 읽기 전용 실행을 "PodSecurityPolicy의 `ReadOnlyRootFileSystem`"으로 설명** → PSP는 **v1.25에서 제거**, 지금은 `securityContext.readOnlyRootFilesystem: true`(정책 강제는 PSA·Gatekeeper·Kyverno) |
| 버전 차이 기록 | 19건 — 5장 "Linux 커널 2천만 줄 이상"(2020) → 2025년 1월 **4천만 줄 돌파**(논지는 오히려 강화, 숫자 인용만 주의) · 6장 "Notary v2 참여가 고무적" → **Notary Project/`notation`(CNCF Incubating)** 이 됐고 원문에 없던 **Sigstore/cosign**(2024-03 OpenSSF 졸업, 키리스 서명)이 별도 축으로 등장 · 6장 어드미션 컨트롤의 당시 대표 수단 **PodSecurityPolicy 제거** → **Pod Security Admission v1.25 stable**(이미지 기준 정책은 OPA Gatekeeper·Kyverno) · **7장 NVD가 전수 보강을 포기**(2026-04-15 NIST 발표) — KEV·연방·EO 14028 핵심 소프트웨어만 즉시 보강, 나머지는 "Lowest Priority". 원문의 "NVD만 보면 오탐"에 **"NVD만 보면 미탐"** 이 추가됨 · 7장 **Kritis 사실상 중단**(master 마지막 커밋 2022-10-20, 릴리스 0건), `anchore-engine`은 **아카이브**되고 후속은 `grype` · 7장 Alpine `secdb`는 **현재 정상 갱신 중**(집필 시점의 일시적 정지였음, 교훈 자체는 유효) · 8장 **AppArmor도 v1.31 stable**·기본 활성이며 애노테이션이 `securityContext.appArmorProfile`(v1.30+)로 대체됨. 단 seccomp 기본값은 여전히 `Unconfined`라 `seccompDefault` kubelet 설정이 필요 — 저자의 "K8s는 기본으로 안 건다"는 지적은 유효 · 8장 **Nabla(`runnc`) 아카이브**(마지막 커밋 2021-09)이고 원문이 권한 AppArmor 도구 `bane`도 2020-09 이후 정지 — Unikernel 축은 컨테이너 진영에서 주류가 못 됨(gVisor·Kata·Firecracker는 활발) · 8장 gVisor 공식 문서가 **syscall 개수로 호환성을 재지 말라고 명시** — 원문의 "97 vs 44" 대비는 그 시점 사실이나 지금은 과장으로 읽힘 · 9장 rootless "초기 단계" → **Docker는 v20.10에서 실험 딱지를 뗌**, 다만 **kubelet rootless는 v1.22 이후 여전히 alpha**(`KubeletInUserNamespace`) — "K8s에선 선택지가 아니다"는 절반만 갱신. Pod의 `hostUsers: false`(4장, v1.36 stable)와 혼동 주의 · 9장 **표준 Nginx 이미지는 6년이 지나도 여전히 root 기본**(공식 Dockerfile `USER` 0건), `nginx-unprivileged`는 조직이 `nginxinc/`→`nginx/`로 이동 · 10장 원문 NetworkPolicy 시연의 플러그인 **Weave 가 2024-08 아카이브**(Calico·Cilium 은 활발) — 개념은 유효하나 `WEAVE-NPC-*` 체인은 재현 불가. Cilium 의 **eBPF 경로는 "규칙은 netfilter 로 구현된다"는 장 전제 자체를 바꿈** · 10장 원문에 없던 **클러스터 범위 AdminNetworkPolicy**(sig-network, 현재 `v1alpha1`·ClusterNetworkPolicy 로 재편 중) — 저자가 다룬 NetworkPolicy 는 개발자용이고 관리자 계층이 추가되는 중 · 10장 "서비스 메시=사이드카 주입" 단정 → **Istio 앰비언트 모드가 v1.24 GA**(2024-11), 노드 단위 `ztunnel` 이 mTLS 처리. 저자가 든 한계 중 "사이드카 없으면 무력"은 성격이 달라졌고 "인프라는 못 지킨다"는 그대로 · 11장 "업계는 주로 TLS v1.3" → 그 뒤 **RFC 8996(2021-03, BCP 195)이 TLS 1.0·1.1 을 공식 폐기**("MUST NOT be used", Historic 이관). 브라우저 2020·AWS 2024·Azure 2025 지원 중단. 반면 **"K8s 는 인증서 폐기 미지원"은 6년 뒤에도 그대로**(공식 CSR 문서에 폐기·CRL 서술 없음, RBAC 차단이 여전히 표준 대응) · 12장 원문에 없던 **Secrets Store CSI Driver**(핵심 기능 Stable, K8s Secret 동기화·자동 순환은 Alpha) — 저자의 "파일 마운트가 선호" + "전용 솔루션이 낫다"를 하나로 이어 **etcd 를 우회**. External Secrets Operator 는 반대로 Secret 으로 동기화해 etcd 에 남김. 단 **"저장 시 암호화 기본 아님"은 그대로**(공식 문서 "By default … no at-rest encryption") · ★ **13장 "eBPF can detect but can't modify system calls" 가 뒤집힘** — 커널 문서상 **BPF LSM 프로그램은 `-EPERM` 반환으로 동작을 거부**(관찰 전용 아님). BPF LSM 은 **커널 5.7(2020-05)** 병합이라 원문 집필 시점엔 정확했고 바로 그 무렵 바뀜. 8장의 "LSM 프로파일 관리 부담"과 13장의 "eBPF 는 못 막는다"가 한 지점에서 함께 풀림 · 13장 **Falco 는 CNCF Graduated 로 승격**(원문은 "CNCF project"), 원문에 없던 **Tetragon** 이 `bpf_send_signal()` 로 커널 공간 kill — 단 이건 사후 완화라 BPF LSM 의 인라인 거부와 성격이 다름 · ★ **14장은 장 구조 자체가 갱신 대상** — 원문 기준은 **OWASP 2017년판**이고 이후 2021·2025 두 번 개정. 현재 **A03 Software Supply Chain Failures**(신규 3위)·**A10 Mishandling of Exceptional Conditions**(완전 신규), A02 Security Misconfiguration 은 5위→2위, A07·A09 는 개명. **원문 절 제목 중 XXE 는 별도 범주에서 빠졌고 안전하지 않은 역직렬화는 무결성 실패로 흡수**. 다만 공급망이 3위로 격상된 것은 저자의 "이미지 스캔이 최대 효율" 결론을 오히려 **강화** |
| 부록 메모 | 부록 자체에서 새로 발견한 원문 정오·버전 차이는 **없습니다**. 체크리스트 항목의 답이 바뀐 5건(어드미션 컨트롤·seccomp/AppArmor·읽기 전용·런타임 eBPF·시크릿 CSI)은 모두 본문 각 장에서 이미 기록한 것이고, 15-01 §3 이 그것을 항목 축으로 한자리에 모은 것입니다 |
| 복습 회차 | 0 |

## 번호 체계와 작성 규약

파일명은 `NN-MM.제목.md` 형식입니다. `NN`은 책의 장 번호, `MM`은 그 장을 여러 편으로 나눌 때의 편 순번입니다. 장 분량이 고르지 않아 장마다 PDF 분량을 보고 분할 여부를 정합니다. 1장은 4,245단어라 한 편으로 묶었습니다. 정밀 도식은 `_assets/`에 SVG로 두고, 흐름·관계 중 자동 배치가 나은 것은 Mermaid로 본문에 직접 그립니다.

작성 규약은 writing 스킬의 책 요약 템플릿(07-04)과 정독 노트 세션 규약(07-04b)을 따르되, 한 가지를 이 책에 맞게 조정했습니다. "Spring 앱 개발 관점" 섹션은 매 장 필수가 아니라 **Spring 접점이 자연스러운 장에만 선별 적용**합니다(합의 2026-08-08). 이 책은 Linux 커널과 컨테이너 런타임이 본체라, 순수 커널 장에 Spring을 붙이면 연결이 억지스러워지기 때문입니다. 7장(의존성 취약점 스캐닝)·11장(TLS — 키스토어·트러스트스토어 구분)·12장(시크릿 전달 — relaxed binding 과 `configtree`)에 적용했습니다. 후보 셋을 모두 소화해, 남은 13·14장은 런타임 탐지와 OWASP 대응이라 Spring 접점을 따로 두지 않습니다.

## 관련 문서

- [『Networking and Kubernetes』 정독본](../networking-and-kubernetes/README.md) — 같은 `book/` 영역, 패킷 중심 관점의 짝이자 namespace·cgroup 기초 설명의 위임 대상
- [『Kubernetes in Action, 2판』 정독본](../kubernetes-in-action/README.md) — 오브젝트 중심 관점, Secret·SecurityContext 사용법의 짝
- [『Kubernetes Patterns』 정독본](../kubernetes-patterns/README.md) — 23-01 Process Containment·25-01 Secure Configuration이 이 책의 실천 패턴에 해당
- [08_cloud MOC](../../README.md) — 상위 카테고리 경계

[^author]: O'Reilly 저자 소개 — Liz Rice. 1판 집필 시점 Aqua Security의 오픈소스 엔지니어링 VP였고, 이후 Isovalent(Cilium)의 Chief Open Source Officer로 옮겼습니다.
<https://www.oreilly.com/pub/au/7324>
