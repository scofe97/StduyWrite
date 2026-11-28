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
updated: 2026-11-29
---

# Container Security — 정독 인덱스
---
> 이 폴더는 『Container Security』(Liz Rice, O'Reilly, 2020) 1판을 장 단위로 정독한 **책-종속 학습노트**입니다.[^author]

이 책은 컨테이너를 만드는 Linux 커널 기능이 어떤 격리 경계를 세우는지 다룹니다. 그 경계가 어디서 뚫리는지도 다룹니다.

형제 책과는 층이 다릅니다. [『Kubernetes in Action』](../kubernetes-in-action/README.md)은 오브젝트 중심이고, [『Networking and Kubernetes』](../networking-and-kubernetes/README.md)는 패킷 중심입니다. 이 책은 **경계 중심**입니다. "무엇이 무엇을 못 보게 막고 있는가"를 묻습니다.

겹치는 기초 개념은 기존 노트에 맡깁니다.

namespace·cgroup의 일반 동작은 [networking-and-kubernetes 03-01](../networking-and-kubernetes/03-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%9D%98%20%ED%83%84%EC%83%9D%20%E2%80%94%20%EC%95%B1%20%EC%8B%A4%ED%96%89%EC%9D%98%20%EC%A7%84%ED%99%94%EC%99%80%20%EA%B2%A9%EB%A6%AC%20%ED%94%84%EB%A6%AC%EB%AF%B8%ED%8B%B0%EB%B8%8C.md)에 있습니다. 네트워크 정책의 일반 동작은 [networking-and-kubernetes 04-03](../networking-and-kubernetes/04-03.NetworkPolicy%EC%99%80%20DNS%20%E2%80%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%95%88%EC%9D%98%20%EB%B0%A9%ED%99%94%EB%B2%BD%EA%B3%BC%20%EC%9D%B4%EB%A6%84.md)에 있습니다.

## 정독 노트

> 17편을 장 순서대로 나열하고, 편마다 다루는 것을 한 줄로 적었습니다.

17편 모두 완료했습니다.

| 장 | 편 | 다루는 것 |
|----|----|----------|
| 1 | [01-01](./01-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%B3%B4%EC%95%88%20%EC%9C%84%ED%98%91%20%E2%80%94%20%EC%9C%84%ED%98%91%20%EB%AA%A8%EB%8D%B8%EB%B6%80%ED%84%B0%20%EB%B3%B4%EC%95%88%20%EC%9B%90%EC%B9%99%EA%B9%8C%EC%A7%80.md) | 위협 모델, 보안 경계, 멀티테넌시, 보안 원칙 |
| 2 | [02-01](./02-01.Linux%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%BD%9C%C2%B7%EA%B6%8C%ED%95%9C%C2%B7capability%20%E2%80%94%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%B3%B4%EC%95%88%EC%9D%98%20%EB%B0%94%EB%8B%A5.md) | syscall, 파일 권한, capability, 권한 상승 |
| 3 | [03-01](./03-01.Control%20Group%20%E2%80%94%20%EC%9E%90%EC%9B%90%EC%9D%84%20%EC%A0%9C%ED%95%9C%ED%95%B4%20%EA%B5%B6%EA%B8%B0%EA%B8%B0%EB%A5%BC%20%EB%A7%89%EB%8B%A4.md) | cgroup 계층과 자원 제한 |
| 4 | [04-01](./04-01.namespace%EC%99%80%20%EB%A3%A8%ED%8A%B8%20%EB%94%94%EB%A0%89%ED%86%A0%EB%A6%AC%20%E2%80%94%20%EA%B2%A9%EB%A6%AC%EB%A5%BC%20%EB%A7%8C%EB%93%9C%EB%8A%94%20%EB%91%90%20%EC%9E%A5%EC%B9%98.md) | namespace와 루트 디렉토리 |
| 4 | [04-02](./04-02.%EB%82%98%EB%A8%B8%EC%A7%80%20namespace%EC%99%80%20%ED%98%B8%EC%8A%A4%ED%8A%B8%EC%97%90%EC%84%9C%20%EB%B3%B8%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88.md) | 나머지 namespace, 호스트에서 본 컨테이너 |
| 5 | [05-01](./05-01.%EA%B0%80%EC%83%81%EB%A8%B8%EC%8B%A0%20%E2%80%94%20%EC%99%9C%20VM%20%EA%B2%A9%EB%A6%AC%EA%B0%80%20%EB%8D%94%20%EA%B0%95%ED%95%98%EB%8B%A4%EA%B3%A0%20%ED%95%98%EB%8A%94%EA%B0%80.md) | VM 격리가 더 강하다고 보는 근거 |
| 6 | [06-01](./06-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%ED%95%B4%EB%B6%80%20%E2%80%94%20%EB%91%90%20%EB%B6%80%EB%B6%84%EA%B3%BC%20%EC%B8%B5%EA%B3%BC%20%EC%8B%9D%EB%B3%84%EC%9E%90.md) | 이미지의 두 부분, 층, 식별자 |
| 6 | [06-02](./06-02.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EA%B3%B5%EA%B8%89%EB%A7%9D%20%EB%B3%B4%EC%95%88%20%E2%80%94%20%EB%B9%8C%EB%93%9C%EB%B6%80%ED%84%B0%20%EB%B0%B0%ED%8F%AC%EA%B9%8C%EC%A7%80.md) | 빌드부터 배포까지 공급망 보안 |
| 7 | [07-01](./07-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%86%8D%20%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4%20%EC%B7%A8%EC%95%BD%EC%A0%90%20%E2%80%94%20CVE%EB%B6%80%ED%84%B0%20%EC%8A%A4%EC%BA%94%20%EC%9A%B4%EC%98%81%EA%B9%8C%EC%A7%80.md) | CVE, 이미지 스캔, 스캔 운영 |
| 8 | [08-01](./08-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC%20%EA%B0%95%ED%99%94%20%E2%80%94%20%EC%83%8C%EB%93%9C%EB%B0%95%EC%8B%B1%EC%9D%98%20%EC%84%B8%20%EA%B0%88%EB%9E%98.md) | seccomp·AppArmor·SELinux, gVisor, Kata 같은 샌드박싱 |
| 9 | [09-01](./09-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC%20%EA%B9%A8%EB%9C%A8%EB%A6%AC%EA%B8%B0%20%E2%80%94%20%EC%84%A4%EC%A0%95%20%ED%95%98%EB%82%98%EB%A1%9C%20%EB%AC%B4%EB%84%88%EC%A7%80%EB%8A%94%20%EA%B2%BD%EA%B3%84.md) | root 실행, --privileged, 민감 마운트로 깨지는 격리 |
| 10 | [10-01](./10-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EB%B3%B4%EC%95%88%20%E2%80%94%20%EA%B3%84%EC%B8%B5%EB%B3%84%EB%A1%9C%20%EB%82%98%EB%88%A0%20%EB%A7%89%EA%B8%B0.md) | 계층별 네트워크 방어, 서비스 메시 |
| 11 | [11-01](./11-01.TLS%EB%A1%9C%20%EC%BB%B4%ED%8F%AC%EB%84%8C%ED%8A%B8%20%EC%95%88%EC%A0%84%ED%95%98%EA%B2%8C%20%EC%97%B0%EA%B2%B0%ED%95%98%EA%B8%B0%20%E2%80%94%20%ED%82%A4%C2%B7%EC%9D%B8%EC%A6%9D%EC%84%9C%C2%B7CA%EC%9D%98%20%EC%97%AD%ED%95%A0.md) | 키·인증서·CA와 TLS 연결 |
| 12 | [12-01](./12-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%97%90%20%EC%8B%9C%ED%81%AC%EB%A6%BF%20%EC%A0%84%EB%8B%AC%ED%95%98%EA%B8%B0%20%E2%80%94%20%EB%8B%A4%EC%84%AF%20%EA%B2%BD%EB%A1%9C%EC%99%80%20root%EB%9D%BC%EB%8A%94%20%EC%B2%9C%EC%9E%A5.md) | 시크릿을 컨테이너에 전달하는 다섯 경로 |
| 13 | [13-01](./13-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%9F%B0%ED%83%80%EC%9E%84%20%EB%B3%B4%ED%98%B8%20%E2%80%94%20%EC%A0%95%EC%83%81%EC%9D%84%20%EC%A0%95%EC%9D%98%ED%95%B4%20%EC%9D%B4%EC%83%81%EC%9D%84%20%EC%9E%A1%EB%8B%A4.md) | 정상 프로파일로 런타임 이상 잡기 |
| 14 | [14-01](./14-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%99%80%20OWASP%20Top%2010%20%E2%80%94%20%EC%9B%B9%20%EB%A6%AC%EC%8A%A4%ED%81%AC%EB%A5%BC%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%8C%80%EC%9D%91%EC%9C%BC%EB%A1%9C%20%EC%9E%87%EB%8B%A4.md) | OWASP Top 10 리스크와 컨테이너 대응 |
| 부록 | [15-01](./15-01.%EB%A7%BA%EC%9D%8C%EB%A7%90%EA%B3%BC%20%EB%B3%B4%EC%95%88%20%EC%B2%B4%ED%81%AC%EB%A6%AC%EC%8A%A4%ED%8A%B8%20%E2%80%94%20%EC%97%B4%EC%95%84%ED%99%89%20%EA%B0%9C%20%EC%A7%88%EB%AC%B8%EC%9C%BC%EB%A1%9C%20%EB%90%98%EC%A7%9A%EA%B8%B0.md) | 네 갈래 되짚기와 19개 점검 질문 |



## 학습 상태

> 진행, 막힌 지점, 다음 할 일을 한 표에 모았습니다.

| 항목 | 값 |
|------|----|
| 진행 | 14장과 부록 완독. 복습 회차 0 |
| 막힌 지점 | 없음 |
| 다음 | 없음. 복습은 [15-01](./15-01.%EB%A7%BA%EC%9D%8C%EB%A7%90%EA%B3%BC%20%EB%B3%B4%EC%95%88%20%EC%B2%B4%ED%81%AC%EB%A6%AC%EC%8A%A4%ED%8A%B8%20%E2%80%94%20%EC%97%B4%EC%95%84%ED%99%89%20%EA%B0%9C%20%EC%A7%88%EB%AC%B8%EC%9C%BC%EB%A1%9C%20%EB%90%98%EC%A7%9A%EA%B8%B0.md)의 §4 항목↔편 대응표로 들어갑니다 |
| 부록 | 새 개념 없이 점검 질문 19개로 본문을 되짚습니다 |
| 원문 정오·버전 차이 | 각 편 본문에 적었습니다. [15-01](./15-01.%EB%A7%BA%EC%9D%8C%EB%A7%90%EA%B3%BC%20%EB%B3%B4%EC%95%88%20%EC%B2%B4%ED%81%AC%EB%A6%AC%EC%8A%A4%ED%8A%B8%20%E2%80%94%20%EC%97%B4%EC%95%84%ED%99%89%20%EA%B0%9C%20%EC%A7%88%EB%AC%B8%EC%9C%BC%EB%A1%9C%20%EB%90%98%EC%A7%9A%EA%B8%B0.md)의 §3이 답이 바뀐 항목을 모읍니다 |
| 검증 기록 | 2026-11-29 기본 게이트를 15-01에 돌려 실패 0을 확인했습니다. 옛 기록(2026-08-09)의 §16·§18과 185줄은 맞지 않습니다. 지금 15-01은 198줄이고 절은 §1~§4입니다 |



## 작성 규약

> 파일명, 편 나누기, 도식, Spring 절의 규칙입니다.

파일명은 `NN-MM.제목.md`입니다. `NN`은 장 번호이고, `MM`은 한 장을 나눈 편 순번입니다. 4장과 6장만 두 편으로 나눴고 나머지는 한 편입니다.

도식은 `_assets/`의 SVG 67장입니다. 각 그림을 만드는 생성기 67개는 `_assets/_gen/`에 있습니다.

책의 "Spring 앱 개발 관점" 절은 Spring 접점이 자연스러운 장에만 달았습니다. 7장, 11장, 12장이 그렇습니다. 커널 장에 억지로 붙이지 않기 위해서입니다.



## 관련 문서

- [『Networking and Kubernetes』 정독본](../networking-and-kubernetes/README.md): 같은 `book/` 영역의 패킷 중심 짝이며, namespace·cgroup 기초 설명을 위임하는 곳입니다.
- [『Kubernetes in Action, 2판』 정독본](../kubernetes-in-action/README.md): 오브젝트 중심 관점이며, Secret과 SecurityContext 사용법의 짝입니다.
- [『Kubernetes Patterns』 정독본](../kubernetes-patterns/README.md): 23-01 Process Containment와 25-01 Secure Configuration이 이 책의 실천 패턴에 해당합니다.
- [08_cloud MOC](../../README.md): 상위 카테고리 경계입니다.

[^author]: O'Reilly 저자 소개. Liz Rice는 1판 집필 시점 Aqua Security의 오픈소스 엔지니어링 VP였고, 이후 Isovalent(Cilium)의 Chief Open Source Officer로 옮겼습니다.
<https://www.oreilly.com/pub/au/7324>
