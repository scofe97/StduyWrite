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
  next_lesson: "08-01 Monitoring and Troubleshooting — 7장 끝문단이 '그 서비스를 떠받치는 CoreDNS 인스턴스를 관측하는 플러그인'으로 넘긴 자리. prometheus 와 질의·응답 로깅, 진단"
updated: 2026-09-05
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
| 5 | Service Discovery | 전통 DNS 지형에 없던 새 용례, 특히 모놀리스에서 마이크로서비스로 옮겨 가며 생긴 요구를 다룸 | 마이크로서비스 분해 예시와 DNS-SD 와의 구분, 인자→hosts→DNS→`SRV`→전용 레지스트리 사다리, 전통 DNS 의 TTL·관리 방식 전제, DNS 에 푸시가 없다는 한계와 DNS-over-gRPC 실험, etcd 쿼럼과 무상태 CoreDNS, SkyDNS 메시지와 역순 키, `etcd` 문법 일곱, `pdsql`·`hosts`·오케스트레이터 |
| 6 | Kubernetes | 쿠버네티스 기본 개념과 서비스 유형, 그것이 DNS 레코드로 어떻게 표현되는지, CoreDNS를 클러스터 안에서 어떻게 돌리고 확장하는지 | 선언형 API·조정 루프·watch, ClusterIP 대 헤드리스와 kube-proxy, DNS 명세의 A·PTR·SRV 와 폐기된 파드 레코드, 되쓰지 않는 컨트롤러와 Endpoints watch 비용, 기본 Corefile 열두 줄과 스텁 도메인, RBAC·Service·Deployment 매니페스트와 오토스케일링, 더 나은 Corefile 두 단계, 플러그인 전체 문법, `pods` 세 모드의 메모리, 와일드카드 질의, `ndots:5` 와 `autopath`, AXFR, `k8s_external` |
| 7 | Manipulating Queries and Responses | 플러그인 체인을 지나는 요청과 그 응답을 환경에 맞게 다듬는 데 가장 흔히 쓰이는 플러그인들을 다룸 | `template` 이 요청만 보고 답을 짓는 방식과 매칭 실패의 행선지, 헤어핀을 피하는 `rewrite name` 과 정규식 규칙이 질문을 안 돌려주는 함정, `answer name`, `continue`·`stop` 과 `class` 재작성이 남기는 구멍, EDNS0 를 싣는 `rewrite edns0` 와 푸는 `metadata`, ZSK·KSK 를 나누는 이유와 정적 존 서명 절차, 합성 레코드의 즉석 서명과 서명 캐시, Infoblox BloxOne Threat Defense 사례 |
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
| [05-01](./05-01.%EC%83%81%ED%83%9C%EB%A5%BC%20%EB%B0%96%EC%97%90%20%EB%91%90%EC%96%B4%EC%95%BC%20%EC%9D%B4%EB%A6%84%EC%9D%B4%20%EC%B4%88%20%EB%8B%A8%EC%9C%84%EB%A1%9C%20%EB%B0%94%EB%80%90%EB%8B%A4.md) | 상태를 밖에 두어야 이름이 초 단위로 바뀐다 (Ch5 전체) | 완료 |
| [06-01](./06-01.%EB%AC%B4%EC%97%87%EC%9D%84%20%EC%84%A0%EC%96%B8%ED%96%88%EB%8A%90%EB%83%90%EA%B0%80%20%EB%A0%88%EC%BD%94%EB%93%9C%20%EB%AA%A8%EC%96%91%EC%9D%84%20%EC%A0%95%ED%95%9C%EB%8B%A4.md) | 무엇을 선언했느냐가 레코드 모양을 정한다 (Ch6 1/4) | 완료 |
| [06-02](./06-02.%EA%B8%B0%EB%B3%B8%20Corefile%EC%9D%98%20%EC%A4%84%EB%A7%88%EB%8B%A4%20%EC%9D%B4%EC%9C%A0%EA%B0%80%20%EC%9E%88%EB%8B%A4.md) | 기본 Corefile의 줄마다 이유가 있다 (Ch6 2/4) | 완료 |
| [06-03](./06-03.%EB%B3%B5%EC%A0%9C%EB%B3%B8%20%EB%91%98%EA%B3%BC%20170Mi%EB%8A%94%20%EC%96%B4%EB%94%94%EC%84%9C%20%EC%98%A8%20%EA%B0%92%EC%9D%B8%EA%B0%80.md) | 복제본 둘과 170Mi는 어디서 온 값인가 (Ch6 3/4) | 완료 |
| [06-04](./06-04.%EB%AA%85%EC%84%B8%20%EB%B0%96%EC%9C%BC%EB%A1%9C%20%EB%82%98%EA%B0%80%EB%A9%B4%20%EC%9D%B4%EC%8B%9D%EC%84%B1%EC%9D%84%20%EB%82%B4%EC%A4%80%EB%8B%A4.md) | 명세 밖으로 나가면 이식성을 내준다 (Ch6 4/4) | 완료 |
| [07-01](./07-01.%EC%A7%88%EB%AC%B8%EA%B3%BC%20%EB%8B%B5%EC%9D%B4%20%EC%96%B4%EA%B8%8B%EB%82%98%EB%A9%B4%20%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8%EA%B0%80%20%EB%B2%84%EB%A6%B0%EB%8B%A4.md) | 질문과 답이 어긋나면 클라이언트가 버린다 (Ch7 전체) | 완료 |
| 08-01 | Monitoring and Troubleshooting | 작성 예정 |
| 09-01 | Building a Custom Server | 작성 예정 |

## 학습 상태

> 세션을 새로 열 때 이 표부터 읽습니다. 정독본의 STATE.md 대용입니다.

| 항목 | 현재 값 |
|------|--------|
| 진행률 | **7/9 장**. 정독 노트 12편 (2·3장은 전·후반부로, 6장은 네 편으로 나눔) |
| 난이도 레벨 | 기본에서 심화 경계. 6장이 가장 두껍고 7장은 그 절반이 안 되지만 DNSSEC 이 새로 들어옵니다. 붙잡을 것 여섯 — **도메인과 존의 차이**, **레코드 한 줄의 다섯 칸**, **플러그인 처리 순서가 빌드 때 고정된다**는 점, **DNS 에는 푸시가 없어 조회는 TTL 을 기다린다**는 비대칭, **`ndots:5` 가 외부 이름 하나에 질의 여섯 번을 만든다**는 구조, 그리고 **정규식으로 이름을 바꾸면 질문이 저절로 돌아오지 않는다**는 것입니다. 뒤의 둘이 실무 비용과 장애로 곧장 이어집니다 |
| 막힌 지점 | 없음. 다만 원서가 출력만 보여 주고 설명하지 않는 숫자가 계속 나와 소스로 메워야 했습니다 — 5장의 TTL 300 과 `SRV` 가중치 100, 6장의 TTL 5, 7장의 `dns-version` TXT `"1.0.1"` 이 그렇습니다 |
| 다음 레슨 후보 | 08-01 Monitoring and Troubleshooting. 7장 끝문단이 "8장에서는 그 서비스를 떠받치는 CoreDNS 인스턴스를 관측하게 돕는 플러그인들을 본다"로 넘긴 자리입니다. `prometheus` 플러그인과 질의·응답 로깅, 진단이 주제이고 PDF 가 441KB 라 한 편으로 끝날 가능성이 높습니다 |
| 최근 검증 결과 | 12편 모두 §1 검사 12개 통과, 벽 단락 0곳, 링크 깨짐 0. 도식 누적 60장 overflow 0·dd-lint error 0·가독성 error 0(한글 하한 11px)·겹침 0·타입 18종(최다 21.7%, 상위 3종 41.7%). **§18 적대적 검증 12회 전부 완료.** 7장에서 잡힌 것은 **허위 정오 1건**(원서가 `answer name` 을 인라인으로 적고 예제는 블록으로 쓴 것을 모순으로 고발했으나 현재 공식 문서가 두 표기를 나란히 싣는다) · **놓친 정오 1건**(Example 7-24 캡션이 `dig` 출력에 `Hello World in Python` — 이 장에서 가장 명백한 것을 초고가 빠뜨렸다) · **정오 오분류 1건**(`upstream` 제거는 버전 차이인데 정오로 라벨) · **연수 오산 1건**(여섯 해 → 일곱 해, 도식에도 전파) · **인과 방향 뒤집힘 1건**(CSK 는 좁아진 게 아니라 catch-all 로 넓어졌다) · **인용 절반 누락 2건**(저자가 곧바로 붙인 OpenDNSSEC·BIND 대안 · NIST 표 9-1 이 ECDSA ZSK 에 주는 12~24개월) · **헤지 소실 2건**(`perhaps` · some→많은) · **예고 아닌 것을 예고로 1건**(`kubernetes` 공급자화는 원서 각주 3 이 이미 실현을 기록) · 근거 없는 직함 1건 · 지키지 않은 약속 1건 · 도식 라벨 2건 · 사정거리 과잉 1건. 전부 1차 자료로 재확인 후 수정. 도식 아홉은 렌더해 눈으로 확인했고, 기계 검사가 통과한 뒤에도 경로가 존 라벨을 관통하거나 화살표가 허공에서 끝나는 결함 셋이 눈에서만 잡혔다 |
| 원문 정오 누적 | **42건 · 블록 32개** — 1장 1건(쿠버네티스 오픈소스화 2015 → 공식문서 2014) · 2장 4건(`precious`→`previous`, IPv6 역방향 `first`→`last`, `2001:db8:42:1:1` 은 유효한 IPv6 아님, Example 2-18 닫는 괄호 누락) · 3장 9건(`file` 산문의 `transfer from`→`transfer to`, Example 3-30 닫는 중괄호 누락, `{>do}` 의 `but`→`bit`, `errors and logs`→`log`, Example 3-39 의 `secondary` 누락, Example 3-38·3-39 의 `forward` 가 `FROM` 누락, 환경 변수 산문이 `{$VAR}` 의 `$` 를 빠뜨림, `along`→`alone` 오타, 인자 없는 `tls` 설명의 `server's client certificate`) · 4장 2건(Example 4-10 의 `--repo` 이하 세 줄에 줄바꿈 이스케이프 누락, Example 4-3 의 `2001:db8:42:1:1` 이 유효한 IPv6 아님) · 5장 7건(Example 5-3 의 `put` 이 키를 `"port "` 로 적어 같은 예제의 `get` 출력과 어긋남, Docker 플래그를 `-link` 로 적음, 산문의 `Corefile-etcd-1` 과 Example 5-8 의 `Corefile-etcd` 불일치, 철자 `ectdv2`·`etdctl`·`overide`·`descibed`) · 6장 14건(dnstools 사이드바의 `--restart=Never` 와 Example 6-10 의 Deployment 형 파드 이름 불일치, Example 6-10 의 `kubectl get po` 출력 둘이 서로 어긋남, `even if though`, 산문의 `ipv6.arpa`·`ip6.arp` 가 같은 페이지 코드 블록의 `ip6.arpa` 와 어긋남, `is create`, `REVERSE_CIDR` 단수, **Example 6-17 이 캡션·산문으로는 서비스 이름이 `kube-dns` 라는데 YAML 은 `name: coredns`**, **Example 6-21 의 HPA 가 `namespace: default` 라 `kube-system` 의 Deployment 를 못 찾음**, 철자 `uses cases`·`presented to client`·`programatically`·`infastructure`, **옵션을 `nodendpoints` 로 적음**). 각 편의 정오 블록에 병기 · 7장 5건(**Example 7-24 의 캡션이 `Hello World in Python` 인데 블록 내용은 `dig soa +dnssec` 출력**, `Kcluster.local+013+47746` 이 `dnssec-keygen` 출력 형식과 달리 존 이름 뒤 점이 빠짐, `the their`, `(i.e,`, NIST 를 복수형 `National Institutes of Standards and Technology` 로 적음). 각 편의 정오 블록에 병기 |
| 버전 차이 기록 | 33건 — **`auto` 플러그인도 `file` 과 같은 폭으로 갈림**(현재 문법은 `directory`·`reload` 둘뿐, `transfer to`·`upstream` 없음) · **`ZONES` 밖 존은 로드되되 질의되지 않음**(공식 문서가 원서보다 정확) · **`-cpu` 플래그가 사라지고 `-p` 별칭이 생김**(`coremain/run.go` 실측) · **`file` 플러그인에서 `upstream` 과 `transfer` 계열이 빠지고 `reload_by_mtime`·`fallthrough` 가 붙음**(공식 문서 실측, 존 전송은 별도 `transfer` 플러그인으로 이동한 것으로 읽힘) · **2장 루트 힌트 발췌의 B 서버 주소가 폐기됨**: 원서의 `199.9.14.201`·`2001:500:200::b` 는 그 뒤 다시 바뀌어, InterNIC `named.root`(2026-08-26 갱신)는 `170.247.170.2`·`2801:1b8:10::b` 를 싣는다 · 표 1-1의 **DoT 줄이 좁게 적힘**: 현재는 `https`(DoH)·`https3`(DoH3)·`quic` 플러그인이 함께 있음 · **CNCF 단계 날짜**를 원서는 양 끝(2017 제출, 2019-01 졸업)만 적었고 공식 발표는 생성 2016-03 · sandbox 합류 2017년(월 없음) · incubating 2018-02 · 졸업 2019-01-24 로 더 자세함 · **완전 재귀 미지원과 DNSSEC 제한은 여섯 해가 지나도 그대로**(공식 플러그인 목록에 재귀 해석기 없음, `dnssec`은 즉석 서명 전용) · **`etcd` 문법에서 `stubzones`·`upstream` 이 사라짐**(원서가 각각 1.4.0·1.3.0 을 경계로 예고한 대로) · **`etcd` 에 `no_apex_fallback`·`min-lease-ttl`·`max-lease-ttl` 이 추가됨**(도입 버전은 미확인, master 문법에 존재만 확인) · **레코드 TTL 이 etcd 리스와 엮임**(리스가 있으면 남은 시간이 반영되고 두 옵션이 30초~24시간으로 가둔다 — 원서 시절에는 없던 축) · **`ETCDCTL_API=3` 이 etcd 3.4 부터 기본값**(원서가 기준한 3.3 에서는 필수였음) · **`kubernetes` 플러그인에서 `resyncperiod`·`upstream`·`transfer to` 가 사라짐**(저자들이 셋 다 예고했고 존 전송은 별도 `transfer` 플러그인으로 이동) · **`kubernetes` 플러그인에 `apiserver_qps` 계열·`namespace_labels`·`multicluster`·`zonal`·`startup_timeout` 이 추가** · **`k8s_external` 에 `headless`·`fallthrough` 가 추가** · **`kubernetes` 플러그인의 `ttl` 기본값이 5초**(원서 6장 예제 출력의 TTL 5 가 이 값인데 원서는 설명하지 않음) · **`template` 에서 `upstream` 이 빠지고 `ederror` 가 붙음** · **`template` 이 `.Meta` 로 metadata 소비자가 됨** · **매칭 실패의 행선지가 갈림**(원서 산문은 "그냥 넘어간다", 현재 문서는 `fallthrough` 없으면 `SERVFAIL`) · **`rewrite` 필드가 다섯에서 일곱으로**(`rcode`·`cname` 추가) · **`answer` 가 셋으로**(`auto`·`value` 추가) · **`edns0` 액션에 `unset` 추가**(셋 → 넷) · **`kubernetes` 가 metadata 공급자로**(키 아홉, 클라이언트 파드 라벨까지) · **`trace` 는 소비자로 문서화되지 않고 발행자로 등재**(`trace/traceid`) · **`dnstap` 이 metadata 소비자로** · **`dnssec` 에 `aws_secretsmanager` 키 소스 추가** · **CSK 판정이 SEP 비트 기준 catch-all 로 넓어짐** · **부재 증명이 NSEC black lies** · **`dns-version` TXT 가 1.0.1 → 1.1.0**(쿠버네티스 DNS 명세 자체가 올라감) · **NIST SP 800-81-2 가 2026-03-19 철회되고 SP 800-81r3 로 대체**(KSK·ZSK 를 나눈 주기를 버리고 서명 키 최대 수명 1~3년 하나로, RRSIG 유효 기간 5~7일 강조) · **RFC 4641 이 RFC 6781 로 폐기** · **`policy` 저장소가 CoreDNS 조직에서 `firewall` 을 제공**(Themis·OPA 엔진) |
| 복습 회차 | 0 |

## 출처와 톤 메모

- 원문(챕터 PDF)이 1차 자료입니다. 사실·수치·API 이름은 추출한 원문에서만 가져오고, 책 밖 보강은 `## 심화 학습`에 분리해 공식 문서 링크를 각주로 답니다.
- 원문 자체의 오류를 발견하면 조용히 고치지 않고 `> **원문 정오**:` 인용 블록으로 병기합니다. 위 학습 상태 표의 "원문 정오 누적"이 그 집계입니다.
- 톤은 합니다체로 통일합니다. 도식은 흐름이 있는 절에만 두고 `>` 요약 바로 다음에 한 장씩 놓습니다.
- 도식 생성기는 `_assets/_gen/`에 있고 `_assets/`에서 실행합니다. `dd.py`는 `writing-method/assets/scripts/dd-primitives.py`의 사본입니다.
