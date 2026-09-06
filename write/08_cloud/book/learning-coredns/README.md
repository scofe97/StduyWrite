---
title: Learning CoreDNS — 정독 인덱스
tags: [moc, study-index, book, coredns, dns, kubernetes, cncf, service-discovery]
status: draft
source:
  - 《Learning CoreDNS: Configuring DNS for Cloud Native Environments》(John Belamaric·Cricket Liu, O'Reilly, 2019, ISBN 978-1492047964)
  - 챕터 PDF 폴더 — GoogleDrive/내 드라이브/book/Learning CoreDNS/ (9개 장)
  - https://coredns.io/plugins/
related:
  - ./00-01.%EC%9A%A9%EC%96%B4%EC%A7%91.md
  - ./00-02.%EA%B2%B0%EC%A0%95%20%EC%B9%98%ED%8A%B8%EC%8B%9C%ED%8A%B8.md
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
  next_lesson: "Phase 4 자답 — 용어집과 결정 치트시트까지 섰으므로 남은 것은 문항 104개에 스스로 답하는 단계"
updated: 2026-09-06
---

# Learning CoreDNS — 정독 인덱스

---

> 이 폴더는 《Learning CoreDNS》(John Belamaric·Cricket Liu, O'Reilly, 2019)를 장 단위로 정독하며 정리하는 책-종속 학습노트입니다. 챕터 PDF를 하나씩 읽은 뒤 한 편씩 채워 넣습니다.

## 이 책을 여기 두는 이유

> 카테고리 선택의 근거와, 이미 있는 DNS 문서 셋과의 경계를 먼저 적습니다.

DNS 를 다루는 책을 어디에 둘지는 자명하지 않습니다. 이 저장소에는 이미 DNS 문서가 세 군데 흩어져 있어서, 자리를 잘못 잡으면 같은 주제가 네 갈래로 갈립니다. 그런데도 `08_cloud` 를 고른 것은 이 책이 던지는 질문이 "클러스터 내부에서 어떻게 돌아가는가"라서입니다. 이 책은 그 질문을 **이름 해석의 서버 편**에서 파고듭니다.

컨테이너가 부하에 따라 뜨고 지는 환경에서 이름 하나가 흔들리는 IP 집합을 어떻게 가리키는지, 그 일을 맡은 서버가 무엇을 갖추고 무엇을 포기했는지를 다룹니다. 저자 둘은 각각 CoreDNS 메인테이너이자 쿠버네티스 기여자, 그리고 《DNS and BIND》를 쓴 DNS 아키텍트라 관점이 "무엇을 설치하라"가 아니라 "이 서버가 어떤 교환을 했는가"에 가깝습니다.

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
| 8 | Monitoring and Troubleshooting | DNS의 가용성과 성능을 관측하고 문제를 진단하는 플러그인을 다룸 | `prometheus` 의 지표 이름과 라벨 축, `log` 한 줄의 칸과 좁히는 손잡이 셋(`NAMES`·`class`·형식 문자열), `dnstap` 의 이진 와이어 형식과 `full`, `errors` 의 `consolidate`, `trace` 의 표본율과 호스트 간 시계 오차, `debug` 와 운영 금지 |
| 9 | Building a Custom Server | 외부 플러그인을 넣어 CoreDNS를 다시 빌드하는 법과, CoreDNS를 라이브러리로 쓰는 법 둘을 다룸 | Docker 와 로컬 두 빌드 길, `plugin.cfg` 한 줄의 위치가 정하는 체인 순서와 `any` 로 그것을 확인하는 실험, `main` 을 갈아 끼워 CoreDNS 를 라이브러리로 쓰기, 플러그인의 네 함수(`init`·`setup`·`Name`·`ServeDNS`)와 호출 시점, Caddy 생명주기 훅 여섯, `nonwriter` 로 아래의 응답 가로채기, `plugin.ClientWrite` 규약, metrics·trace·metadata 통합 |



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
| [08-01](./08-01.%EB%AC%B4%EC%97%87%EC%9D%84%20%EB%B3%BC%EC%A7%80%20%EC%A2%81%ED%9E%88%EB%8A%94%20%EC%86%90%EC%9E%A1%EC%9D%B4%EA%B0%80%20%EB%8F%84%EA%B5%AC%EB%A7%88%EB%8B%A4%20%EB%8B%A4%EB%A5%B4%EB%8B%A4.md) | 무엇을 볼지 좁히는 손잡이가 도구마다 다르다 (Ch8 전체) | 완료 |
| [09-01](./09-01.%ED%95%9C%20%EC%A4%84%EC%9D%84%20%EC%98%AE%EA%B8%B0%EB%A9%B4%20%EA%B7%B8%20%ED%94%8C%EB%9F%AC%EA%B7%B8%EC%9D%B8%EC%9D%B4%20%EC%93%B8%EB%AA%A8%EC%97%86%EC%96%B4%EC%A7%84%EB%8B%A4.md) | 한 줄을 옮기면 그 플러그인이 쓸모없어진다 (Ch9 1/2) | 완료 |
| [09-02](./09-02.%EB%84%A4%20%ED%95%A8%EC%88%98%EB%A5%BC%20%EA%B5%AC%ED%98%84%ED%95%98%EB%A9%B4%20%EC%B2%B4%EC%9D%B8%EC%9D%98%20%ED%95%9C%20%EC%B9%B8%EC%9D%B4%20%EB%90%9C%EB%8B%A4.md) | 네 함수를 구현하면 체인의 한 칸이 된다 (Ch9 2/2) | 완료 |
| [00-01](./00-01.%EC%9A%A9%EC%96%B4%EC%A7%91.md) | 용어집 — 15편의 말을 장 순서로 모음 (용어 99개) | 완료 |
| [00-02](./00-02.%EA%B2%B0%EC%A0%95%20%EC%B9%98%ED%8A%B8%EC%8B%9C%ED%8A%B8.md) | 결정 치트시트 — 15편의 표를 결정 축 16개로 통합 (126행) | 완료 |



## 학습 상태

> 세션을 새로 열 때 이 표부터 읽습니다. 정독본의 STATE.md 대용입니다.

| 항목 | 현재 값 |
|------|--------|
| 진행률 | **9/9 장 완주 + 가로지르기 둘**. 정독 노트 15편과 용어집·결정 치트시트 (2·3·9장은 전·후반부로, 6장은 네 편으로 나눔) |
| 난이도 레벨 | 기본에서 심화 경계. 6장이 가장 두껍고(13,965 단어) 1장이 가장 얇습니다(1,389 단어). 8장은 3,353 단어로 셋째입니다. 붙잡을 것 일곱 — **도메인과 존의 차이**, **레코드 한 줄의 다섯 칸**, **플러그인 처리 순서가 빌드 때 고정된다**는 점, **DNS 에는 푸시가 없어 조회는 TTL 을 기다린다**는 비대칭, **`ndots:5` 가 외부 이름 하나에 질의 여섯 번을 만든다**는 구조, **정규식으로 이름을 바꾸면 질문이 저절로 돌아오지 않는다**는 것, 그리고 **관측 도구마다 값을 깎는 손잡이가 따로 있다**는 것입니다. 뒤의 셋이 실무 비용과 장애로 곧장 이어집니다 |
| 막힌 지점 | 없음. 다만 원서가 출력만 보여 주고 설명하지 않는 숫자가 계속 나와 소스로 메워야 했습니다 — 5장의 TTL 300 과 `SRV` 가중치 100, 6장의 TTL 5, 7장의 `dns-version` TXT `"1.0.1"` 이 그렇습니다 |
| 다음 레슨 후보 | Phase 4 자답. 면접 문항 104개와 정답 104개가 편마다 준비돼 있고, 자답은 학습자가 직접 하는 단계입니다. 그것을 마쳐야 `last_verified` 에 날짜를 적을 수 있습니다 |
| 최근 검증 결과 | **2026-09-05 전체 재점검(도식 포함).** 15편 모두 §1 검사 12개·절 도입부·요약 계층 통과, 벽 단락 0곳, 각주 63개 짝 일치, 링크 깨짐 0, 원문자 0. 도식 78장은 네 센서(overflow·lint·가독성·겹침) 전부 error 0 이고 78장 모두 렌더해 눈으로 대조했습니다. 이번 점검이 잡은 것 — **`dd.py` 가 정본과 어긋난 채 1~6장 도식 51장이 옛 글자 크기로 남아 가독성 error 52건**(재생성으로 해소), **`dd.state` 가 칩 폭을 ASCII 기준으로 잡아 한글 칩 10개가 상자를 넘치고 레인 점선이 글자 사이로 비친 것**(센서 넷이 모두 놓쳤고 눈으로만 잡혔습니다. 이 책은 국소 `chip()` 헬퍼로 대체), **7장에서 고친 "여섯 해"가 01-01·08-01·09-01·README 에 그대로 남은 것**, **README 가 8장을 가장 얇다고 적은 것**(실측 1장 1,389 · 4장 2,492 · 8장 3,353), **README 가 `resyncperiod`·`upstream`·`transfer to` 셋 다 저자가 제거를 예고했다고 적은 것**(원서 축자 확인 결과 예고는 `resyncperiod` 하나뿐), 정오 블록 수·버전 차이 건수 오기 2건, 사용처 없는 `allow:` 선언 3줄, 도식 표현 4건(연표의 경과 연수 단정 · 검색 경로 넷↔접미사 다섯 · 범례가 그림에 없는 "고리" 지칭 · 등급 둘이 렌더에서 구분 안 됨). 전부 1차 자료로 재확인 후 수정했습니다 |
| 적대적 검증 (§18) | **7·8·9장**은 별개 서브에이전트로 돌리고 보고서를 회수했습니다. **1~6장 11편은 2026-09-05 에 다시 걸었는데, 이 세션이 서브에이전트를 쓸 수 없어 직접 돌린 약한 변형입니다** — 정본 `07-verification.md` §5 는 "맥락을 공유하지 않는 서브에이전트가 반박을 기본값으로" 점검하라고 정합니다. 판정은 전부 1차 자료(원서 PDF 추출본 6개 · CoreDNS 공식 문서와 `.go` 소스 · etcd CHANGELOG)로 확정했습니다. 검사 규모 — 영문 인용 83개 축자 대조, Example 참조 전수, 원서 귀속 수치 37개, 기본값 15종(`-cpu` 100% · `max_fails` 2 · `health_check` 0.5초 · `expire` 10초 · cache CAPACITY 9,984/최소 1,024 · TTL 상한 3,600 · `hosts` ttl 3600·reload 5초 · etcd `defaultTTL` 300·`defaultPriority` 10 · `min/max-lease-ttl` 30초/24시간 · `kubernetes` ttl 5초 · health 8080 · 레이블 63자 · 루트 서버 13대), **원문 정오 27건 전수**, Binary 층 6항목. 결과는 **결함 2건 · 헛고발 0건** 입니다. 결함은 `grpc` 절의 "페이지 어디에도 push·stream·watch·service discovery 라는 말이 없다" (`stream` 이 `upstream` 의 일부로 14번 나와 grep 으로 반증됨)와 `max_fails` 를 "연속 실패 횟수"로 줄여 무엇을 세는지 지운 것 둘입니다. 가장 어려운 확인은 `forward` 헬스 체크였습니다 — 현재 README 가 "네트워크 오류가 아닌 응답은 전부 healthy" 라 적어 원서의 "빈 응답도 실패" 와 충돌하는 듯했으나, `plugin/pkg/proxy/health.go` 주석이 "Dial timeouts and empty replies are considered fails, basically anything else constitutes a healthy upstream" 이라 원서와 노트가 맞고 현재 문서 쪽이 느슨한 것이었습니다. **남은 일 — 1~6장을 정본이 정한 서브에이전트 형태로 다시 거는 것** |
| 원문 정오 누적 | **49건 · 블록 38개** — 1장 1건(쿠버네티스 오픈소스화 2015 → 공식문서 2014) · 2장 4건(`precious`→`previous`, IPv6 역방향 `first`→`last`, `2001:db8:42:1:1` 은 유효한 IPv6 아님, Example 2-18 닫는 괄호 누락) · 3장 9건(`file` 산문의 `transfer from`→`transfer to`, Example 3-30 닫는 중괄호 누락, `{>do}` 의 `but`→`bit`, `errors and logs`→`log`, Example 3-39 의 `secondary` 누락, Example 3-38·3-39 의 `forward` 가 `FROM` 누락, 환경 변수 산문이 `{$VAR}` 의 `$` 를 빠뜨림, `along`→`alone` 오타, 인자 없는 `tls` 설명의 `server's client certificate`) · 4장 2건(Example 4-10 의 `--repo` 이하 세 줄에 줄바꿈 이스케이프 누락, Example 4-3 의 `2001:db8:42:1:1` 이 유효한 IPv6 아님) · 5장 7건(Example 5-3 의 `put` 이 키를 `"port "` 로 적어 같은 예제의 `get` 출력과 어긋남, Docker 플래그를 `-link` 로 적음, 산문의 `Corefile-etcd-1` 과 Example 5-8 의 `Corefile-etcd` 불일치, 철자 `ectdv2`·`etdctl`·`overide`·`descibed`) · 6장 14건(dnstools 사이드바의 `--restart=Never` 와 Example 6-10 의 Deployment 형 파드 이름 불일치, Example 6-10 의 `kubectl get po` 출력 둘이 서로 어긋남, `even if though`, 산문의 `ipv6.arpa`·`ip6.arp` 가 같은 페이지 코드 블록의 `ip6.arpa` 와 어긋남, `is create`, `REVERSE_CIDR` 단수, **Example 6-17 이 캡션·산문으로는 서비스 이름이 `kube-dns` 라는데 YAML 은 `name: coredns`**, **Example 6-21 의 HPA 가 `namespace: default` 라 `kube-system` 의 Deployment 를 못 찾음**, 철자 `uses cases`·`presented to client`·`programatically`·`infastructure`, **옵션을 `nodendpoints` 로 적음**). 각 편의 정오 블록에 병기 · 7장 5건(**Example 7-24 의 캡션이 `Hello World in Python` 인데 블록 내용은 `dig soa +dnssec` 출력**, `Kcluster.local+013+47746` 이 `dnssec-keygen` 출력 형식과 달리 존 이름 뒤 점이 빠짐, `the their`, `(i.e,`, NIST 를 복수형 `National Institutes of Standards and Technology` 로 적음). 각 편의 정오 블록에 병기 · 8장 2건(Example 8-12 가 TCP 소켓을 `tcp://127.0.0.1/8053` 로 적는데 바로 앞 문장의 형식 설명과 같은 장의 Example 8-17 은 콜론을 씀, Example 8-21 의 정규식 `".* network is unreachable$"` 과 바로 뒤 접힌 출력 `'^.* network is unreachable$'` 이 어긋남 — 접힌 줄은 설정한 정규식을 소스가 그대로 되뇜). 각 편의 정오 블록에 병기 · 9장 5건(`plugin.ClientWrite` 가 `true` 를 돌려주면 응답이 **쓰이지 않은** 것이라고 적었으나 소스 주석과 호출부는 정반대 — `true` 가 이미 썼다는 뜻, 재시작 훅 셋을 열거한 뒤 "이것들은 전부 `OnShutdown` 앞에 불린다"고 적어 `OnShutdown` 이 자기보다 먼저 불릴 수 없게 됨, `Metadata` 가 `ServeDNS` 와 같은 인자를 받는다고 적었으나 실제는 `(ctx, request.Request)`, `nonwriter` 경로에서 저장소 이름 누락(`github.com/coredns/plugin/...`), 등록되는 곳을 `plug-in change` 로 적음). 각 편의 정오 블록에 병기 |
| 버전 차이 기록 | 47건 — **`auto` 플러그인도 `file` 과 같은 폭으로 갈림**(현재 문법은 `directory`·`reload` 둘뿐, `transfer to`·`upstream` 없음) · **`ZONES` 밖 존은 로드되되 질의되지 않음**(공식 문서가 원서보다 정확) · **`-cpu` 플래그가 사라지고 `-p` 별칭이 생김**(`coremain/run.go` 실측) · **`file` 플러그인에서 `upstream` 과 `transfer` 계열이 빠지고 `reload_by_mtime`·`fallthrough` 가 붙음**(공식 문서 실측, 존 전송은 별도 `transfer` 플러그인으로 이동한 것으로 읽힘) · **2장 루트 힌트 발췌의 B 서버 주소가 폐기됨**: 원서의 `199.9.14.201`·`2001:500:200::b` 는 그 뒤 다시 바뀌어, InterNIC `named.root`(2026-08-26 갱신)는 `170.247.170.2`·`2801:1b8:10::b` 를 싣는다 · 표 1-1의 **DoT 줄이 좁게 적힘**: 현재는 `https`(DoH)·`https3`(DoH3)·`quic` 플러그인이 함께 있음 · **CNCF 단계 날짜**를 원서는 양 끝(2017 제출, 2019-01 졸업)만 적었고 공식 발표는 생성 2016-03 · sandbox 합류 2017년(월 없음) · incubating 2018-02 · 졸업 2019-01-24 로 더 자세함 · **완전 재귀 미지원과 DNSSEC 제한은 일곱 해가 지나도 그대로**(공식 플러그인 목록에 재귀 해석기 없음, `dnssec`은 즉석 서명 전용) · **`etcd` 문법에서 `stubzones`·`upstream` 이 사라짐**(원서가 각각 1.4.0·1.3.0 을 경계로 예고한 대로) · **`etcd` 에 `no_apex_fallback`·`min-lease-ttl`·`max-lease-ttl` 이 추가됨**(도입 버전은 미확인, master 문법에 존재만 확인) · **레코드 TTL 이 etcd 리스와 엮임**(리스가 있으면 남은 시간이 반영되고 두 옵션이 30초~24시간으로 가둔다 — 원서 시절에는 없던 축) · **`ETCDCTL_API=3` 이 etcd 3.4 부터 기본값**(원서가 기준한 3.3 에서는 필수였음) · **`kubernetes` 플러그인에서 `resyncperiod`·`upstream`·`transfer to` 가 사라짐**(제거를 예고한 것은 `resyncperiod` 하나뿐 — "This option will be eliminated in later versions". `upstream` 은 1.3.0 이후 쓸모없다는 현재형 서술만, `transfer to` 는 아무 예고도 없습니다. 존 전송은 별도 `transfer` 플러그인으로 이동) · **`kubernetes` 플러그인에 `apiserver_qps` 계열·`namespace_labels`·`multicluster`·`zonal`·`startup_timeout` 이 추가** · **`k8s_external` 에 `headless`·`fallthrough` 가 추가** · **`kubernetes` 플러그인의 `ttl` 기본값이 5초**(원서 6장 예제 출력의 TTL 5 가 이 값인데 원서는 설명하지 않음) · **`template` 에서 `upstream` 이 빠지고 `ederror` 가 붙음** · **`template` 이 `.Meta` 로 metadata 소비자가 됨** · **매칭 실패의 행선지가 갈림**(원서 산문은 "그냥 넘어간다", 현재 문서는 `fallthrough` 없으면 `SERVFAIL`) · **`rewrite` 필드가 다섯에서 일곱으로**(`rcode`·`cname` 추가) · **`answer` 가 셋으로**(`auto`·`value` 추가) · **`edns0` 액션에 `unset` 추가**(셋 → 넷) · **`kubernetes` 가 metadata 공급자로**(키 아홉, 클라이언트 파드 라벨까지) · **`trace` 는 소비자로 문서화되지 않고 발행자로 등재**(`trace/traceid`) · **`dnstap` 이 metadata 소비자로** · **`dnssec` 에 `aws_secretsmanager` 키 소스 추가** · **CSK 판정이 SEP 비트 기준 catch-all 로 넓어짐** · **부재 증명이 NSEC black lies** · **`dns-version` TXT 가 1.0.1 → 1.1.0**(쿠버네티스 DNS 명세 자체가 올라감) · **NIST SP 800-81-2 가 2026-03-19 철회되고 SP 800-81r3 로 대체**(KSK·ZSK 를 나눈 주기를 버리고 서명 키 최대 수명 1~3년 하나로, RRSIG 유효 기간 5~7일 강조) · **RFC 4641 이 RFC 6781 로 폐기** · **`policy` 저장소가 CoreDNS 조직에서 `firewall` 을 제공**(Themis·OPA 엔진) · **표 8-1 의 CoreDNS 지표 열 중 다섯이 개명**(`coredns_dns_request_count_total`→`requests_total`, `response_rcode_count_total`→`responses_total`, `panic_count_total`→`panics_total`, `request_do_count_total`→`do_requests_total`, `request_type_count_total` 은 `type` 라벨로 흡수) · **살아남은 지표에 `view` 라벨 추가** · **`coredns_dns_https_responses_total`·`coredns_dns_quic_responses_total` 신설** · **`prometheus` 에 `runtime_metrics` 블록 추가** · **`log` 에 `{/LABEL}` metadata 칸 추가** · **`dnstap` 에 `identity`·`version`·`extra`·`skipverify`·`tls://`·`listen` 모드 추가** · **`errors` 의 `consolidate` 가 `[LEVEL] [show_first]` 를 받고 여러 개 허용, `stacktrace` 추가** · **`trace` 에 Zipkin 배치 옵션 셋과 `datadog_analytics_rate` 추가, 지원 유형은 zipkin·datadog 둘**(원서는 Stackdriver 도 듦) · **`debug` 문서가 소스와 어긋남**(`errors` 가 `recover` 를 건다는 서술이 현재 코드에 없음) · **CoreDNS 가 Caddy 를 자기 조직으로 포크**(`github.com/mholt/caddy` → `github.com/coredns/caddy`. 원서 각주는 `caddyserver/caddy` 를 가리켰으나 실제 행선지는 달랐다) · **Go 요구 버전이 1.12 에서 1.25.0 으로** · **`any` 가 인트리로 편입**(`plugin.cfg` 50번째 줄, 저자들이 각주에 v1.5.1 을 예고했고 그대로 됨) · **`plugin.cfg` 가 83줄 61엔트리로 늘고 마지막이 `nomad:nomad`** · **인트리 `init` 관용구가 `plugin.Register(name, setupFn)` 한 줄로** · **예제 저장소가 2022년에 포크 이후로 이관**(`coredns/caddy v1.1.1` · `coredns/coredns v1.9.2`) |
| 복습 회차 | 0 |



## 출처와 톤 메모

- 원문(챕터 PDF)이 1차 자료입니다. 사실·수치·API 이름은 추출한 원문에서만 가져오고, 책 밖 보강은 `## 심화 학습`에 분리해 공식 문서 링크를 각주로 답니다.
- 원문 자체의 오류를 발견하면 조용히 고치지 않고 `> **원문 정오**:` 인용 블록으로 병기합니다. 위 학습 상태 표의 "원문 정오 누적"이 그 집계입니다.
- 톤은 합니다체로 통일합니다. 도식은 흐름이 있는 절에만 두고 `>` 요약 바로 다음에 한 장씩 놓습니다.
- 도식 생성기는 `_assets/_gen/`에 있고 `_assets/`에서 실행합니다. `dd.py`는 `writing-method/assets/scripts/dd-primitives.py`의 사본입니다.
