---
title: Learning CoreDNS — 정독 인덱스
tags: [moc, study-index, book, coredns, dns, kubernetes, cncf, service-discovery]
status: draft
source:
  - 《Learning CoreDNS: Configuring DNS for Cloud Native Environments》(John Belamaric·Cricket Liu, O'Reilly, 2019, ISBN 978-1492047964)
  - 챕터 PDF 폴더 — GoogleDrive/내 드라이브/book/Learning CoreDNS/ (9개 장)
  - https://coredns.io/plugins/
related:
  - ../networking-and-kubernetes/README.md
  - ../kubernetes-in-action/README.md
  - ../../README.md
  - ../../kubernetes/04_networking/04-05.DNS와 CoreDNS.md
learning:
  topic: learning-coredns
  scope: durable
  level: 기본
  last_verified:            # Phase 4 자답·_review 회차 미실시 — 원문 대조일로 대신 채우지 않는다
  blocked_count:
  next_lesson: "05-01 Service Discovery — 1장이 던진 문제로 돌아가는 장. 여기서부터 CoreDNS 의 존재 이유가 본론이 된다"
updated: 2026-09-02
---

# Learning CoreDNS — 정독 인덱스

---

> 이 폴더는 《Learning CoreDNS》(John Belamaric·Cricket Liu, O'Reilly, 2019)를 장 단위로 정독하며 정리하는 책-종속 학습노트입니다. 챕터 PDF를 하나씩 읽은 뒤 한 편씩 채워 넣습니다.

## 이 책을 여기 두는 이유

`08_cloud`는 "클러스터 내부에서 어떻게 돌아가는가"를 다루는 카테고리입니다. 이 책은 그 질문을 **이름 해석의 서버 편**에서 파고듭니다. 컨테이너가 부하에 따라 뜨고 지는 환경에서 이름 하나가 흔들리는 IP 집합을 어떻게 가리키는지, 그 일을 맡은 서버가 무엇을 갖추고 무엇을 포기했는지를 다룹니다. 저자 둘은 각각 CoreDNS 메인테이너이자 쿠버네티스 기여자, 그리고 《DNS and BIND》를 쓴 DNS 아키텍트라 관점이 "무엇을 설치하라"가 아니라 "이 서버가 어떤 교환을 했는가"에 가깝습니다.

같은 폴더의 형제 책들과는 보는 층이 다릅니다. [『Kubernetes in Action』](../kubernetes-in-action/README.md)이 오브젝트 중심이고 [『Networking and Kubernetes』](../networking-and-kubernetes/README.md)가 패킷 중심이라면, 이 책은 **서비스 하나**를 끝까지 파고듭니다. 그 서비스가 클러스터의 모든 이름 해석을 떠받치기 때문에, 좁게 파도 닿는 범위가 넓습니다.

DNS를 다루는 기존 노트와는 편을 나눠 가집니다. 질의를 **보내는 쪽**, 곧 `resolv.conf`와 ndots와 search domain은 [02_os OS 네트워크 로드맵 §6](../../../02_os/networking/roadmap.md)이 SSOT입니다. 질의를 **받는 쪽**, 곧 Corefile과 플러그인과 존 데이터는 이 폴더가 맡습니다. 쿠버네티스 공식문서 기준의 운영 관점은 [DNS와 CoreDNS](../../kubernetes/04_networking/04-05.DNS%EC%99%80%20CoreDNS.md)가 이미 SSOT이므로, 겹치는 자리는 링크로 위임하고 여기에는 **책에서 새로 얻는 것만** 남깁니다.

## 장별 목표

> 각 장 PDF 앞머리의 저자 선언을 `pdftotext`로 추출해 근거로 삼았습니다. 원문에 없는 목표를 추측해 넣지 않습니다.

| 장 | 제목 | 저자가 선언한 목표 | 주요 토픽 |
|----|------|------------------|----------|
| 1 | Introduction | CoreDNS의 존재 이유와 다른 DNS 서버와의 차이를 한계까지 포함해 설명하고, CNCF와의 관계를 비롯한 내력을 짚음 | Caddy 포크, 플러그인 아키텍처, Go 메모리 안전성, 완전 재귀 미지원, BIND 대조표, CNCF |
| 2 | A DNS Refresher | 버텨 낼 만큼의 DNS 이론만 주고, 더 필요하면 《DNS and BIND》 쪽을 가리킴 | 전반부 — 이름공간과 도메인 이름, 도메인·위임·존, 리소스 레코드, 권한과 주·보조 서버, 리졸버, 해석과 재귀, 캐싱. 후반부 — 마스터 파일 형식과 NAME·TTL·CLASS, A·AAAA·CNAME·MX·NS·SRV·PTR·SOA, 주석 달린 존 파일 |
| 3 | Configuring CoreDNS | 2장의 이론 위에서 실제로 CoreDNS 서버를 설정함 | 전반부 — 실행 파일과 체크섬, 명령줄 옵션 여덟, Corefile 문법(엔트리·블록·지시어·서브지시어), 환경 변수·스니펫·import, 서버 블록 라벨, 최장 일치. 후반부 — 고정된 플러그인 순서, `root`·`file`·`secondary`·`forward`·`cache`·`errors`·`log`, `fallthrough`·`tls`·`transfer to`, 캐싱 전용·주·보조 서버 설정 |
| 4 | Managing Zone Data | CoreDNS가 지원하는 존 데이터 관리 방법을 모두 다룸 | `file` 상세(상대 경로·한 파일 여러 존·`transfer to`·`reload`), `auto` 의 디렉터리 스캔과 정규식 origin 추출, `git-sync` 조합, `hosts` 의 A·AAAA·PTR 생성과 별칭 함정, `route53` 의 Hosted Zone ID 와 자격증명 세 경로 |
| 5 | Service Discovery | 전통 DNS 지형에 없던 새 용례, 특히 모놀리스에서 마이크로서비스로 옮겨 가며 생긴 요구를 다룸 | 마이크로서비스 분해 예시, 서비스 디스커버리 개론 |
| 6 | Kubernetes | 쿠버네티스 기본 개념과 서비스 유형, 그것이 DNS 레코드로 어떻게 표현되는지, CoreDNS를 클러스터 안에서 어떻게 돌리고 확장하는지 | 쿠버네티스 내부 구조, DNS 명세, CoreDNS 배치·스케일, 표준 기능 너머의 최적화 |
| 7 | Manipulating Queries and Responses | 플러그인 체인을 지나는 요청과 그 응답을 환경에 맞게 다듬는 데 가장 흔히 쓰이는 플러그인들을 다룸 | `template` 플러그인, `rewrite` 플러그인 |
| 8 | Monitoring and Troubleshooting | DNS의 가용성과 성능을 관측하고 문제를 진단하는 플러그인을 다룸 | `prometheus` 플러그인, 질의·응답 로깅, 진단 |
| 9 | Building a Custom Server | 외부 플러그인을 넣어 CoreDNS를 다시 빌드하는 법과, CoreDNS를 라이브러리로 쓰는 법 둘을 다룸 | `plugin.cfg` 수정 후 재빌드, 자체 main 루틴 작성 |

## 작성된 정독 노트

> 원문을 정독해 편을 작성하는 대로 채웁니다. 아직 작성하지 않은 장은 상태만 두고 본문 내용은 원문 도착 전까지 채우지 않습니다.

| 편 | 제목 | 상태 |
|----|------|------|
| [01-01](./01-01.CoreDNS%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9D%84%20%ED%8F%AC%EA%B8%B0%ED%95%98%EA%B3%A0%20%EB%AC%B4%EC%97%87%EC%9D%84%20%EC%96%BB%EC%97%88%EB%8A%94%EA%B0%80.md) | CoreDNS는 무엇을 포기하고 무엇을 얻었는가 (Ch1 전체) | 완료 |
| [02-01](./02-01.%EC%9C%84%EC%9E%84%EC%9D%B4%20%EA%B7%B8%EC%9D%80%20%EA%B2%BD%EA%B3%84%EA%B0%80%20%EC%A7%88%EC%9D%98%20%EA%B2%BD%EB%A1%9C%EB%A5%BC%20%EC%A0%95%ED%95%9C%EB%8B%A4.md) | 위임이 그은 경계가 질의 경로를 정한다 (Ch2 전반부) | 완료 |
| [02-02](./02-02.%EB%A0%88%EC%BD%94%EB%93%9C%20%ED%95%9C%20%EC%A4%84%EC%9D%84%20%EC%9D%BD%EC%9C%BC%EB%A9%B4%20%EC%A1%B4%20%ED%8C%8C%EC%9D%BC%EC%9D%B4%20%EC%9D%BD%ED%9E%8C%EB%8B%A4.md) | 레코드 한 줄을 읽으면 존 파일이 읽힌다 (Ch2 후반부) | 완료 |
| [03-01](./03-01.Corefile%EC%9D%80%20%EB%9D%BC%EB%B2%A8%EB%A1%9C%20%EC%84%9C%EB%B2%84%EB%A5%BC%20%EA%B0%80%EB%A5%B8%EB%8B%A4.md) | Corefile은 라벨로 서버를 가른다 (Ch3 전반부) | 완료 |
| [03-02](./03-02.%ED%94%8C%EB%9F%AC%EA%B7%B8%EC%9D%B8%20%EC%9D%BC%EA%B3%B1%EC%9D%B4%EB%A9%B4%20%EC%84%9C%EB%B2%84%20%ED%95%98%EB%82%98%EA%B0%80%20%EC%84%A0%EB%8B%A4.md) | 플러그인 일곱이면 서버 하나가 선다 (Ch3 후반부) | 완료 |
| [04-01](./04-01.%EC%A1%B4%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%A5%BC%20%EC%96%B4%EB%94%94%EC%97%90%20%EB%91%98%EC%A7%80%EA%B0%80%20%EA%B4%80%EB%A6%AC%20%EB%B0%A9%EC%8B%9D%EC%9D%84%20%EC%A0%95%ED%95%9C%EB%8B%A4.md) | 존 데이터를 어디에 둘지가 관리 방식을 정한다 (Ch4 전체) | 완료 |
| 05-01 | Service Discovery | 작성 예정 |
| 06-01 | Kubernetes | 작성 예정 |
| 07-01 | Manipulating Queries and Responses | 작성 예정 |
| 08-01 | Monitoring and Troubleshooting | 작성 예정 |
| 09-01 | Building a Custom Server | 작성 예정 |

## 학습 상태

> 세션을 새로 열 때 이 표부터 읽습니다. 정독본의 STATE.md 대용입니다.

| 항목 | 현재 값 |
|------|--------|
| 진행률 | **4/9 장**. 정독 노트 6편 (2·3장은 분량이 커 각각 전·후반부로 나눔) |
| 난이도 레벨 | 기본. 3장부터 실물 설정이 나오지만 문법이 얇아 부담이 없었습니다. 붙잡을 것 셋 — **도메인과 존의 차이**, **레코드 한 줄의 다섯 칸**, 그리고 **플러그인 처리 순서가 빌드 때 고정된다**는 점입니다. 셋째가 특히 실무에서 헛짚기 쉬운 자리입니다 |
| 막힌 지점 | 없음 |
| 다음 레슨 후보 | 05-01 Service Discovery. 1장이 던진 "컨테이너가 뜨고 지는데 상대를 어떻게 찾나"로 돌아가는 장입니다. 4장까지가 전통 DNS 서버로서의 CoreDNS 였다면 5장부터가 이 책의 본론입니다 |
| 최근 검증 결과 | 6편 모두 §1 검사 12개 통과, 벽 단락 0곳, 링크 깨짐 0. 도식 누적 25장 overflow 0·dd-lint error 0·타입 12종(최다 24%). **§18 적대적 검증 6회 전부 완료** — 수치 8건·저자와 해석의 경계 13건·**노트가 놓친 원문 오류 8건**을 잡아 전부 1차 자료로 재확인 후 수정. 공개 저장소 대비 민감정보 센서를 돌려 원서 예제 IP·주소를 `allow:` 에 등록하고 AWS 자격증명 예제는 자리표시자로 치환 (2026-09-02) |
| 원문 정오 누적 | **16건 · 블록 14개** — 1장 1건(쿠버네티스 오픈소스화 2015 → 공식문서 2014) · 2장 4건(`precious`→`previous`, IPv6 역방향 `first`→`last`, `2001:db8:42:1:1` 은 유효한 IPv6 아님, Example 2-18 닫는 괄호 누락) · 3장 9건(`file` 산문의 `transfer from`→`transfer to`, Example 3-30 닫는 중괄호 누락, `{>do}` 의 `but`→`bit`, `errors and logs`→`log`, Example 3-39 의 `secondary` 누락, Example 3-38·3-39 의 `forward` 가 `FROM` 누락, 환경 변수 산문이 `{$VAR}` 의 `$` 를 빠뜨림, `along`→`alone` 오타, 인자 없는 `tls` 설명의 `server's client certificate`) · 4장 2건(Example 4-10 의 `--repo` 이하 세 줄에 줄바꿈 이스케이프 누락, Example 4-3 의 `2001:db8:42:1:1` 이 유효한 IPv6 아님). 각 편의 정오 블록에 병기 |
| 버전 차이 기록 | 9건 — **`auto` 플러그인도 `file` 과 같은 폭으로 갈림**(현재 문법은 `directory`·`reload` 둘뿐, `transfer to`·`upstream` 없음) · **`ZONES` 밖 존은 로드되되 질의되지 않음**(공식 문서가 원서보다 정확) · **`-cpu` 플래그가 사라지고 `-p` 별칭이 생김**(`coremain/run.go` 실측) · **`file` 플러그인에서 `upstream` 과 `transfer` 계열이 빠지고 `reload_by_mtime`·`fallthrough` 가 붙음**(공식 문서 실측, 존 전송은 별도 `transfer` 플러그인으로 이동한 것으로 읽힘) · **2장 루트 힌트 발췌의 B 서버 주소가 폐기됨**: 원서의 `199.9.14.201`·`2001:500:200::b` 는 그 뒤 다시 바뀌어, InterNIC `named.root`(2026-08-26 갱신)는 `170.247.170.2`·`2801:1b8:10::b` 를 싣는다 · 표 1-1의 **DoT 줄이 좁게 적힘**: 현재는 `https`(DoH)·`https3`(DoH3)·`quic` 플러그인이 함께 있음 · **CNCF 단계 날짜**를 원서는 양 끝(2017 제출, 2019-01 졸업)만 적었고 공식 발표는 생성 2016-03 · sandbox 합류 2017년(월 없음) · incubating 2018-02 · 졸업 2019-01-24 로 더 자세함 · **완전 재귀 미지원과 DNSSEC 제한은 여섯 해가 지나도 그대로**(공식 플러그인 목록에 재귀 해석기 없음, `dnssec`은 즉석 서명 전용) |
| 복습 회차 | 0 |

## 출처와 톤 메모

- 원문(챕터 PDF)이 1차 자료입니다. 사실·수치·API 이름은 추출한 원문에서만 가져오고, 책 밖 보강은 `## 심화 학습`에 분리해 공식 문서 링크를 각주로 답니다.
- 원문 자체의 오류를 발견하면 조용히 고치지 않고 `> **원문 정오**:` 인용 블록으로 병기합니다. 위 학습 상태 표의 "원문 정오 누적"이 그 집계입니다.
- 톤은 합니다체로 통일합니다. 도식은 흐름이 있는 절에만 두고 `>` 요약 바로 다음에 한 장씩 놓습니다.
- 도식 생성기는 `_assets/_gen/`에 있고 `_assets/`에서 실행합니다. `dd.py`는 `writing-method/assets/scripts/dd-primitives.py`의 사본입니다.
