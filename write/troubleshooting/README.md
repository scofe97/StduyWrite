---
title: troubleshooting — 장애 사례와 진단 훈련
tags: [moc, troubleshooting, drill, rca]
status: draft
source:
  - experience
related:
  - ../README.md
  - ./_drill/README.md
  - ../02_os/troubleshooting/README.md
  - ../08_cloud/troubleshooting/README.md
updated: 2026-09-07
---

# troubleshooting

---

> 증상에서 원인으로 거슬러 올라간 기록입니다. 여기 있는 문항은 전부 제가 직접 풀어 정리한 것이고, 계층별 폴더에 날짜순으로 쌓입니다.

## 이 폴더가 하는 일

> 주제 카테고리(`01_language` ~ `11_career`)가 "무엇을 배웠나"라면 여기는 "그것이 깨졌을 때 무엇을 어떤 순서로 보나"입니다.

번호가 없는 이유가 그것입니다. 트러블슈팅은 열두 번째 주제가 아니라 모든 주제를 가로지르는 형식이라, 순서대로 읽는 게 아니라 증상으로 찾습니다. 정렬상 주제 카테고리를 다 지난 맨 뒤에 옵니다.

문항 하나가 파일 하나입니다. 푸는 동안은 증상과 세 칸이 있고, 다 풀면 같은 파일을 다섯 갈래(문제 소개·원인 분석·해결 방법·다른 방법 비교·나온 개념)로 채웁니다. 내 답과 점수는 [`_drill/log.md`](./_drill/log.md)로 빠져서, 남는 파일은 남이 읽어도 되는 사례입니다.



## 계층

> 문제가 사는 곳으로 나눕니다. 아래에서 위로 쌓이는 순서라 진단을 어디서 시작할지의 축이기도 합니다.

| 폴더 | 문자 | 문제가 사는 곳 | 문항 |
|------|------|--------------|------|
| [os/](./os/) | A | 리눅스 호스트 한 대 안 — 소켓·conntrack·MTU·라우팅·NIC | 1 |
| [kubernetes/](./kubernetes/) | B | 클러스터 안 — Pod 네트워크·Service·CoreDNS·CNI·NetworkPolicy | 1 |
| [mesh/](./mesh/) | C | 서비스 메시 — Envoy 사이드카·mTLS·xDS·서킷 브레이커 | 1 |
| [cloud/](./cloud/) | D | 클러스터 바깥 — VPC·보안 그룹·NAT·로드밸런서·리전 간 | 0 |
| [runtime/](./runtime/) | E | JVM 과 애플리케이션 — GC·OOM·스레드·커넥션 누수·트랜잭션 | 0 |

A 부터 D 까지가 "패킷이 어디서 사라지나"를 묻는 네트워크 축이고, E 는 "프로세스가 왜 멈추거나 느려지나"를 묻습니다.

문자와 폴더가 병존하는 것은 회차 로그와 커버리지 맵이 문자를 쓰기 때문입니다. 이 표가 대응표입니다.



## 계층은 늘어납니다

> 다섯은 시작점입니다. 후보가 이미 셋이고, 사례가 쌓이는 곳이면 더 열립니다.

| 후보 | 근거 노트 | 편수 |
|------|----------|------|
| `data/` F 데이터·메시징 | `05_data` + `04_messaging` | 256 |
| `pipeline/` G CI/CD | `07_devops` + Infratice cicd 13건 | 225 |
| `observability/` H 관측 | `06_observability` + Infratice monitoring | 86 |

계층을 열 때 하는 일은 넷입니다.

1. 폴더와 그 안의 `README.md` — 이 계층이 무엇을 다루고 어디서 끝나는지 한 문단
2. 위 계층 표에 한 줄
3. [`_drill/sources.md`](./_drill/sources.md) 커버리지 맵에 한 절 — 근거 폴더와 편수만
4. 문자를 다음 알파벳으로

여는 기준은 둘 중 하나입니다. 근거 노트 폴더가 이미 있거나, 드릴에서 그 계층 문항이 5건 쌓였거나. 둘 다 아니면 열지 않고 커버리지 맵에 "근거 없음"으로 둡니다.



## 어디부터 읽나

> 장애 중이면 계층 폴더에서 증상으로 찾고, 훈련이 목적이면 `_drill/` 로 갑니다.

장애 대응 중이라면 문제가 사는 계층의 폴더를 엽니다. 파일명이 증상이라 훑으면 됩니다.

직접 풀어 보려면 [`_drill/`](./_drill/README.md) 입니다. 하루 세 문항을 증상만 보고 진단하는 루틴과 채점 규약이 거기 있습니다. 문항은 [`_drill/sources.md`](./_drill/sources.md) 의 소스에서 그날 새로 뽑고, 기존 사례집 두 곳이 그 예비 풀입니다.

- [리눅스 사례집](../02_os/troubleshooting/README.md) — Infratice 41건. 디스크·프로세스·서비스·로그·네트워크
- [쿠버네티스 사례집](../08_cloud/troubleshooting/README.md) — Infratice 38건. 이미지·자원·설정·배치·볼륨·권한·관측

두 사례집은 남이 만든 해설이라 여기로 옮기지 않습니다. 풀어서 제 어휘로 정리한 것만 이 폴더에 들어옵니다.



## 관련 문서

- [write 루트](../README.md) — 전체 지도
- [드릴 진입점](./_drill/README.md) — 루틴, 채점, 스킵, 재출제 규약
- [회차 로그](./_drill/log.md) — 날짜별로 무엇을 풀었나
- [복습 시스템](../_review/README.md) — 학습 문서를 회상하는 다른 트랙. 점수 척도를 공유합니다
