---
title: 03_architecture/docs/system-design-course — 시니어처럼 시스템 설계하기 강의 지도
tags: [moc, system-design, interview, lecture]
status: draft
source:
  - "YouTube 강의 자막: Design Software Systems Like a Senior Engineer – Complete Course (3시간 16분, 영어 자동 생성 자막)"
related:
  - ../../book/system-design/README.md
  - ../../book/bytebytego-system-design/README.md
updated: 2026-10-20
---

# 03_architecture/docs/system-design-course — 시니어처럼 시스템 설계하기 강의 지도

---

> 3시간 16분짜리 시스템 설계 강의가 무엇을 다루는지, 그중 무엇이 이미 이 저장소에 있고 무엇이 비어 있는지를 정리한 지도입니다. 강의 개념의 대부분은 기존 정독 노트에 있고, 새로 쓸 만한 것은 Booking.com 사례의 예약 도메인과 WhatsApp 사례의 장애·운영 절입니다.

강의를 통째로 옮기면 기존 노트와 겹치는 분량이 커서, 먼저 겹침을 확인하고 빈 곳만 문서로 썼습니다. 대조는 강의 요약에서 뽑은 개념 120개를 `write/` 전체(아카이브 제외)에서 키워드로 찾은 뒤, 애매한 것은 해당 노트 본문을 열어 확인하는 방식으로 했습니다.



## 문서 목록

> 아래 「비어 있는 주제」 표의 1·2위와 3위를 한 편씩으로 묶어 썼습니다. 4·5위는 각 편의 마지막 절에 짧게 들어 있습니다.

| 번호 | 제목 | 한 줄 소개 |
|------|------|-----------|
| 01-01 | [호텔 예약은 방 타입의 날짜별 재고 행을 팔고 그 행을 잠가 이중 예약을 막는다](01-01.%ED%98%B8%ED%85%94%20%EC%98%88%EC%95%BD%EC%9D%80%20%EB%B0%A9%20%ED%83%80%EC%9E%85%EC%9D%98%20%EB%82%A0%EC%A7%9C%EB%B3%84%20%EC%9E%AC%EA%B3%A0%20%ED%96%89%EC%9D%84%20%ED%8C%94%EA%B3%A0%20%EA%B7%B8%20%ED%96%89%EC%9D%84%20%EC%9E%A0%EA%B0%80%20%EC%9D%B4%EC%A4%91%20%EC%98%88%EC%95%BD%EC%9D%84%20%EB%A7%89%EB%8A%94%EB%8B%A4.md) | 방 타입·날짜 단위 재고 모델에서 시작해, 마지막 한 방을 두고 두 예약이 겹칠 때 격리 수준·행 잠금·조건부 갱신이 각각 어떻게 막는지 비교합니다. |
| 02-01 | [메시징 서버는 Redis 가 멈추면 DB 수신함으로 Kafka 가 멈추면 로컬 로그로 버텨 메시지를 잃지 않는다](02-01.%EB%A9%94%EC%8B%9C%EC%A7%95%20%EC%84%9C%EB%B2%84%EB%8A%94%20Redis%20%EA%B0%80%20%EB%A9%88%EC%B6%94%EB%A9%B4%20DB%20%EC%88%98%EC%8B%A0%ED%95%A8%EC%9C%BC%EB%A1%9C%20Kafka%20%EA%B0%80%20%EB%A9%88%EC%B6%94%EB%A9%B4%20%EB%A1%9C%EC%BB%AC%20%EB%A1%9C%EA%B7%B8%EB%A1%9C%20%EB%B2%84%ED%85%A8%20%EB%A9%94%EC%8B%9C%EC%A7%80%EB%A5%BC%20%EC%9E%83%EC%A7%80%20%EC%95%8A%EB%8A%94%EB%8B%A4.md) | 메시지가 지나는 이음매마다 잃을 자리를 짚고, Redis 장애·브로커 장애·클러스터 전체 장애에 쓰는 장치와 그 비용을 따져 봅니다. |



## 강의 구성

> 강의는 면접 프레임워크 하나를 세우고 그 틀을 세 서비스 설계에 차례로 적용합니다. 뒤로 갈수록 길고 깊어서, WhatsApp 한 사례가 전체의 40% 가 넘습니다.

| 구간 | 시각 | 다루는 것 |
|------|------|-----------|
| 면접 프레임워크 | 00:00~00:23 | 면접 형태 네 가지, 평가 축 다섯 개, 5단계 시간 배분(요구사항 5~10분, 데이터·API와 고수준 설계 각 15~20분, 병목·확장 5~10분, 트레이드오프 정리), 해야 할 것과 피할 것 |
| Spotify | 00:23~00:51 | 음악 스트리밍 요구사항, 오디오 용량 계산(곡 2억 개에 600TB), Blob 저장소와 signed URL, CDN, 재생·업로드 흐름, 5천만 사용자까지의 확장 |
| Booking.com | 00:51~01:53 | 호텔 예약 요구사항, 방문·검색·예약 깔때기로 읽기 1,000 QPS 와 쓰기 17 TPS 어림, 서비스 분리, 방 타입과 일별 재고 테이블, 이중 예약 방지, 호텔 ID 샤딩, Redis 캐시, Elasticsearch 와 CDC, 리전 복제 |
| WhatsApp | 01:53~03:16 | 하루 100억 메시지 용량 계산, WebSocket 과 서비스 디스커버리, 1:1·그룹·오프라인 전달, 다중 기기의 전송·수신·읽음 상태, 미디어 업로드, Kafka 소비와 배치 쓰기, 종단 간 암호화, 처리율 제한, 샤딩, 정리 작업, Redis·Kafka 장애 대응, feature flag |



## 이미 있는 주제

> 강의가 설명하는 개념 대부분은 기존 정독 노트가 더 깊게 다룹니다. 이 표의 주제는 새로 쓰지 않고 링크로 넘깁니다.

강의가 덧붙이는 관점이 있으면 마지막 열에 적었습니다. 그 관점이 한두 문단 분량이라 별도 문서보다는 나중에 해당 노트를 보강할 때 넣을 후보로 둡니다. `04_messaging/` 은 문서 정리를 앞두고 있어 이 대조에서 뺐습니다. 그 폴더가 정리되면 Kafka 컨슈머 행을 다시 봅니다.

| 강의 주제 | 구간 | 기존 노트 | 강의가 덧붙이는 것 |
|-----------|------|-----------|-------------------|
| 면접 진행 단계와 시간 배분 | 프레임워크 | [가상 면접 3장 — 면접 네 단계](../../book/system-design/03-01.%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%84%A4%EA%B3%84%20%EB%A9%B4%EC%A0%91%EC%9D%80%20%EB%B2%94%EC%9C%84%20%ED%99%95%EC%A0%95%C2%B7%EA%B0%9C%EB%9E%B5%20%EC%84%A4%EA%B3%84%C2%B7%EC%83%81%EC%84%B8%20%EC%84%A4%EA%B3%84%C2%B7%EB%A7%88%EB%AC%B4%EB%A6%AC%20%EB%84%A4%20%EB%8B%A8%EA%B3%84%EB%A1%9C%20%EC%A7%84%ED%96%89%ED%95%9C%EB%8B%A4.md) | 단계가 넷이 아니라 다섯이고, 면접관이 보는 축(소통, 구조적 사고, 기술 판단, 실무 깊이, 시간 관리)을 따로 셉니다 |
| 개략적 규모 추정 | 세 사례 모두 | [가상 면접 2장 — 규모 추정](../../book/system-design/02-01.%EA%B0%9C%EB%9E%B5%EC%A0%81%20%EA%B7%9C%EB%AA%A8%20%EC%B6%94%EC%A0%95%EC%9D%80%202%EC%9D%98%20%EA%B1%B0%EB%93%AD%EC%A0%9C%EA%B3%B1%C2%B7%EC%A7%80%EC%97%B0%20%EC%8B%9C%EA%B0%84%C2%B7%EA%B0%80%EC%9A%A9%EC%84%B1%20%EC%88%98%EC%B9%98%EB%A1%9C%20QPS%20%EC%99%80%20%EC%A0%80%EC%9E%A5%20%EC%9A%A9%EB%9F%89%EC%9D%84%20%EC%96%B4%EB%A6%BC%ED%95%9C%EB%8B%A4.md) | 방문자 깔때기(전체의 10% 가 검색, 그중 10% 가 예약)로 읽기와 쓰기를 따로 어림합니다 |
| 로드밸런서·복제·무상태 서버·캐시·CDN 으로 규모 늘리기 | 프레임워크, Spotify | [가상 면접 1장 — 수백만 사용자까지](../../book/system-design/01-02.%EC%BA%90%EC%8B%9C%C2%B7CDN%C2%B7%EB%AC%B4%EC%83%81%ED%83%9C%20%EC%9B%B9%20%EA%B3%84%EC%B8%B5%C2%B7%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%84%BC%ED%84%B0%C2%B7%EB%A9%94%EC%8B%9C%EC%A7%80%20%ED%81%90%C2%B7%EC%83%A4%EB%94%A9%EC%9D%B4%20%EC%88%98%EB%B0%B1%EB%A7%8C%20%EC%82%AC%EC%9A%A9%EC%9E%90%EA%B9%8C%EC%A7%80%20%EA%B7%9C%EB%AA%A8%EB%A5%BC%20%EB%8A%98%EB%A6%B0%EB%8B%A4.md) | 없음 |
| 캐시 전략·TTL·무효화 | Booking.com | [ByteByteGo — 캐시 전략](../../book/bytebytego-system-design/02-01.%EC%BA%90%EC%8B%9C%20%EC%A0%84%EB%9E%B5%EC%9D%80%20%EC%9D%BD%EA%B8%B0%C2%B7%EC%93%B0%EA%B8%B0%20%EA%B2%BD%EB%A1%9C%EC%97%90%EC%84%9C%20%EC%BA%90%EC%8B%9C%20%EC%9E%90%EB%A6%AC%EB%A5%BC%20%EC%A0%95%ED%95%98%EA%B3%A0%20Redis%20%EB%8A%94%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EC%99%80%20%EB%8B%A8%EC%9D%BC%20%EC%8A%A4%EB%A0%88%EB%93%9C%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EB%A3%A8%ED%94%84%EB%A1%9C%20%EB%B9%A0%EB%A5%B4%EB%8B%A4.md), [캐싱 전략](../../../05_data/01_foundation/01-07.%EC%BA%90%EC%8B%B1%20%EC%A0%84%EB%9E%B5.md) | 예약이 성공하면 영향받는 캐시 키를 지우는 흐름을 예약 사례에 붙여 보여 줍니다 |
| 격리 수준·`SELECT … FOR UPDATE`·serializable | Booking.com | [ByteByteGo — 격리 수준과 낙관적 잠금](../../book/bytebytego-system-design/01-01.%EA%B2%A9%EB%A6%AC%20%EC%88%98%EC%A4%80%EA%B3%BC%20%EB%82%99%EA%B4%80%EC%A0%81%20%EC%9E%A0%EA%B8%88%EC%9D%B4%20%EB%8F%99%EC%8B%9C%20%EC%93%B0%EA%B8%B0%EC%9D%98%20%EC%9D%B4%EC%83%81%20%ED%98%84%EC%83%81%EC%9D%84%20%EB%A7%89%EA%B3%A0%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%AA%A8%EC%96%91%EC%9D%B4%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%20%EC%A2%85%EB%A5%98%EB%A5%BC%20%EA%B3%A0%EB%A5%B8%EB%8B%A4.md), [트랜잭션과 격리 수준](../../../05_data/01_foundation/01-04.%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%EA%B3%BC%20%EA%B2%A9%EB%A6%AC%20%EC%88%98%EC%A4%80.md) | 아래 「비어 있는 주제」의 이중 예약 항목에서 다룹니다 |
| 샤딩·읽기 복제본 | 세 사례 모두 | [ByteByteGo — 파티셔닝과 읽기 복제본](../../book/bytebytego-system-design/01-02.%ED%8C%8C%ED%8B%B0%EC%85%94%EB%8B%9D%EA%B3%BC%20%EC%9D%BD%EA%B8%B0%20%EB%B3%B5%EC%A0%9C%EB%B3%B8%EC%9D%80%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%EB%A5%BC%20%EB%84%93%ED%9E%88%EA%B3%A0%20%EC%A0%84%EC%97%AD%20%EC%9C%A0%EC%9D%BC%20ID%20%EB%8A%94%20%EB%82%98%EB%89%9C%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%97%90%20%EC%88%9C%EC%84%9C%EB%A5%BC%20%EC%A4%80%EB%8B%A4.md) | 샤드 키를 사례마다 다르게 고릅니다(곡은 아티스트 ID, 예약은 호텔 ID, 메시지는 사용자 ID) |
| 안정 해시 | Booking.com | [가상 면접 5장 — 안정 해시](../../book/system-design/05-01.%EC%95%88%EC%A0%95%20%ED%95%B4%EC%8B%9C%EB%8A%94%20%ED%95%B4%EC%8B%9C%20%EB%A7%81%EA%B3%BC%20%EA%B0%80%EC%83%81%20%EB%85%B8%EB%93%9C%EB%A1%9C%20%EC%84%9C%EB%B2%84%EA%B0%80%20%EB%8A%98%EA%B3%A0%20%EC%A4%84%20%EB%95%8C%20%EC%98%AE%EA%B8%B8%20%ED%82%A4%EB%A5%BC%20%EC%A4%84%EC%9D%B8%EB%8B%A4.md) | 없음 |
| CAP 과 키-값 저장소(Cassandra) | 프레임워크, WhatsApp | [가상 면접 6장 — 키-값 저장소](../../book/system-design/06-01.%ED%82%A4-%EA%B0%92%20%EC%A0%80%EC%9E%A5%EC%86%8C%EB%8A%94%20CAP%20%EC%84%A0%ED%83%9D%20%EC%95%84%EB%9E%98%20%EC%95%88%EC%A0%95%20%ED%95%B4%EC%8B%9C%EB%A1%9C%20%EB%82%98%EB%88%84%EA%B3%A0%20N%C2%B7W%C2%B7R%20%EC%A0%95%EC%A1%B1%EC%88%98%EB%A1%9C%20%EB%B3%B5%EC%A0%9C%20%EC%9D%BC%EA%B4%80%EC%84%B1%EC%9D%84%20%EA%B3%A0%EB%A5%B8%EB%8B%A4.md) | 없음 |
| 멱등 키 | Booking.com | [ByteByteGo — 결제 정확성](../../book/bytebytego-system-design/07-02.%EA%B2%B0%EC%A0%9C%20%EC%A0%95%ED%99%95%EC%84%B1%EC%9D%80%20%EB%A9%B1%EB%93%B1%20%ED%82%A4%EB%A1%9C%20%EC%9D%B4%EC%A4%91%20%EC%B2%AD%EA%B5%AC%EB%A5%BC%20%EB%A7%89%EA%B3%A0%20%EB%8C%80%EC%82%AC%EB%A1%9C%20%EC%9E%A5%EB%B6%80%20%EB%B6%88%EC%9D%BC%EC%B9%98%EB%A5%BC%20%EC%B0%BE%EA%B3%A0%20%ED%86%A0%ED%81%B0%ED%99%94%EB%A1%9C%20%EC%B9%B4%EB%93%9C%20%EC%A0%95%EB%B3%B4%EB%A5%BC%20%EC%A7%80%ED%82%A8%EB%8B%A4.md) | 클라이언트가 만든 예약 UUID 를 중복 키로 씁니다 |
| CDC 와 Debezium | Booking.com | [Data Liberation 과 CDC](../../05_edd/01-04.%EA%B8%B0%EC%A1%B4%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%ED%86%B5%ED%95%A9%20%E2%80%94%20Data%20Liberation%20%EA%B3%BC%20CDC.md), [DDIA 12장 — 데이터베이스와 스트림](../../../05_data/book/designing-data-intensive-applications/12-02.%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%EC%99%80%20%EC%8A%A4%ED%8A%B8%EB%A6%BC.md) | 아래 「비어 있는 주제」의 검색 색인 항목에서 다룹니다 |
| Elasticsearch 검색 | Booking.com | [OpenSearch 정독 노트](../../../06_observability/book/dgos_opensearch/README.md) | SQL `LIKE` 가 풀 스캔이 되는 이유로 검색 서비스를 따로 둡니다 |
| 모놀리스와 마이크로서비스 | Booking.com | [모놀리스에서 마이크로서비스로](../../04_ddd/03-04.%EB%AA%A8%EB%86%80%EB%A6%AC%EC%8A%A4%EC%97%90%EC%84%9C%20%EB%A7%88%EC%9D%B4%ED%81%AC%EB%A1%9C%EC%84%9C%EB%B9%84%EC%8A%A4%EB%A1%9C%20%E2%80%94%20%EC%96%B8%EC%A0%9C%2C%20%EC%99%9C.md) | 없음 |
| Blob 저장소·signed URL·CDN 스트리밍 | Spotify, WhatsApp | [가상 면접 14장 — YouTube 업로드](../../book/system-design/14-01.YouTube%20%EC%97%85%EB%A1%9C%EB%93%9C%EB%8A%94%20%EC%9B%90%EB%B3%B8%EC%9D%84%20BLOB%20%EC%A0%80%EC%9E%A5%EC%86%8C%EC%97%90%20%EB%91%90%EA%B3%A0%20DAG%20%EB%A1%9C%20%EC%AA%BC%EA%B0%A0%20%ED%8A%B8%EB%9E%9C%EC%8A%A4%EC%BD%94%EB%94%A9%EC%9D%84%20%EA%B1%B0%EC%B3%90%20CDN%20%EC%9C%BC%EB%A1%9C%20%EC%8A%A4%ED%8A%B8%EB%A6%AC%EB%B0%8D%ED%95%9C%EB%8B%A4.md), [ByteByteGo — 블록·파일·객체 저장소](../../book/bytebytego-system-design/04-01.%EB%B8%94%EB%A1%9D%C2%B7%ED%8C%8C%EC%9D%BC%C2%B7%EA%B0%9D%EC%B2%B4%20%EC%A0%80%EC%9E%A5%EC%86%8C%EB%8A%94%20%EC%A0%91%EA%B7%BC%20%EB%8B%A8%EC%9C%84%EA%B0%80%20%EB%8B%A4%EB%A5%B4%EA%B3%A0%20%EC%9D%B4%EB%A0%88%EC%9D%B4%EC%A0%80%20%EC%BD%94%EB%94%A9%EA%B3%BC%20%EB%B6%84%ED%95%A0%20%EC%97%85%EB%A1%9C%EB%93%9C%EA%B0%80%20%ED%81%B0%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%A5%BC%20%EC%8B%B8%EA%B3%A0%20%EC%95%88%EC%A0%84%ED%95%98%EA%B2%8C%20%EB%8B%B4%EB%8A%94%EB%8B%A4.md) | 영상 대신 오디오라서 비트레이트별 파일 크기와 egress 비용을 계산합니다 |
| 채팅 시스템 전반(WebSocket, 폴링 비교, 접속 상태, 서비스 디스커버리, 다중 기기 동기화, 그룹 수신함) | WhatsApp | [가상 면접 12장 — 채팅 시스템](../../book/system-design/12-01.%EC%B1%84%ED%8C%85%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%80%20%EC%9B%B9%EC%86%8C%EC%BC%93%20%EC%97%B0%EA%B2%B0%EC%9D%84%20%EC%83%81%ED%83%9C%20%EC%9C%A0%EC%A7%80%20%EC%84%9C%EB%B2%84%EC%97%90%20%EB%91%90%EA%B3%A0%20%ED%82%A4-%EA%B0%92%20%EC%A0%80%EC%9E%A5%EC%86%8C%EC%99%80%20%EB%A9%94%EC%8B%9C%EC%A7%80%20ID%20%EB%A1%9C%20%EB%8C%80%ED%99%94%EC%99%80%20%EC%A0%91%EC%86%8D%20%EC%83%81%ED%83%9C%EB%A5%BC%20%EB%8B%A4%EB%A3%AC%EB%8B%A4.md), [WebSocket 프로토콜과 핸드셰이크](../../../09_spring/03_network/realtime/03-01.WebSocket%20%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C%EA%B3%BC%20%ED%95%B8%EB%93%9C%EC%85%B0%EC%9D%B4%ED%81%AC.md) | 없음(구조가 거의 같습니다) |
| 푸시 알림(APNs·FCM) | WhatsApp | [가상 면접 10장 — 알림 시스템](../../book/system-design/10-01.%EC%95%8C%EB%A6%BC%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%80%20%EC%A0%9C3%EC%9E%90%20%ED%91%B8%EC%8B%9C%C2%B7SMS%C2%B7%EC%9D%B4%EB%A9%94%EC%9D%BC%20%EC%84%9C%EB%B9%84%EC%8A%A4%20%EC%95%9E%EC%97%90%20%EB%A9%94%EC%8B%9C%EC%A7%80%20%ED%81%90%EC%99%80%20%EC%9E%91%EC%97%85%20%EC%84%9C%EB%B2%84%EB%A5%BC%20%EB%91%90%EC%96%B4%20%EC%9E%AC%EC%8B%9C%EB%8F%84%EC%99%80%20%EC%A4%91%EB%B3%B5%EC%9D%84%20%EB%8B%A4%EB%A3%AC%EB%8B%A4.md) | 없음 |
| 처리율 제한(토큰 버킷, Redis 분산 카운터) | WhatsApp | [가상 면접 4장 — 처리율 제한 알고리즘](../../book/system-design/04-01.%EC%B2%98%EB%A6%AC%EC%9C%A8%20%EC%A0%9C%ED%95%9C%EA%B8%B0%EB%8A%94%20%ED%86%A0%ED%81%B0%20%EB%B2%84%ED%82%B7%C2%B7%EB%88%84%EC%B6%9C%20%EB%B2%84%ED%82%B7%C2%B7%EA%B3%A0%EC%A0%95%20%EC%9C%88%EB%8F%84%C2%B7%EC%9D%B4%EB%8F%99%20%EC%9C%88%EB%8F%84%20%EB%A1%9C%EA%B7%B8%C2%B7%EC%9D%B4%EB%8F%99%20%EC%9C%88%EB%8F%84%20%EC%B9%B4%EC%9A%B4%ED%84%B0%EB%A1%9C%20%EC%9A%94%EC%B2%AD%EC%9D%84%20%EC%84%BC%EB%8B%A4.md), [처리율 제한 미들웨어](../../book/system-design/04-02.%EC%B2%98%EB%A6%AC%EC%9C%A8%20%EC%A0%9C%ED%95%9C%20%EB%AF%B8%EB%93%A4%EC%9B%A8%EC%96%B4%EB%8A%94%20%EA%B7%9C%EC%B9%99%EA%B3%BC%20Redis%20%EC%B9%B4%EC%9A%B4%ED%84%B0%EB%A1%9C%20429%20%EB%A5%BC%20%EB%8F%8C%EB%A0%A4%EC%A3%BC%EA%B3%A0%20%EB%B6%84%EC%82%B0%20%ED%99%98%EA%B2%BD%EC%9D%98%20%EA%B2%BD%EC%9F%81%20%EC%A1%B0%EA%B1%B4%EA%B3%BC%20%EB%8F%99%EA%B8%B0%ED%99%94%EB%A5%BC%20%ED%91%BC%EB%8B%A4.md) | 경고에서 1시간·24시간 제한, 계정 정지로 올라가는 단계적 제재와 CAPTCHA |
| Kafka 컨슈머·리밸런스·DLQ | WhatsApp | [ByteByteGo — Kafka](../../book/bytebytego-system-design/05-01.Kafka%20%EB%8A%94%20%EC%88%9C%EC%B0%A8%20IO%20%EC%99%80%20%EC%A0%9C%EB%A1%9C%20%EC%B9%B4%ED%94%BC%EB%A1%9C%20%EB%B9%A0%EB%A5%B4%EA%B3%A0%20%EC%A0%84%EB%8B%AC%20%EB%B3%B4%EC%9E%A5%EC%9D%80%20%EC%B5%9C%EB%8C%80%20%ED%95%9C%20%EB%B2%88%C2%B7%EC%B5%9C%EC%86%8C%20%ED%95%9C%20%EB%B2%88%C2%B7%EC%A0%95%ED%99%95%ED%9E%88%20%ED%95%9C%20%EB%B2%88%EC%9C%BC%EB%A1%9C%20%EA%B0%88%EB%A6%B0%EB%8B%A4.md), [DDIA 12장 — 스트림 전송](../../../05_data/book/designing-data-intensive-applications/12-01.%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%EC%A0%84%EC%86%A1%20%E2%80%94%20%EB%A9%94%EC%8B%9C%EC%A7%80%20%EB%B8%8C%EB%A1%9C%EC%BB%A4%EC%99%80%20%EB%A1%9C%EA%B7%B8%20%EA%B8%B0%EB%B0%98%20%EB%B8%8C%EB%A1%9C%EC%BB%A4.md) | 이 표에서 유일하게 깊이가 부족한 행입니다. 두 노트 모두 컨슈머 그룹과 DLQ 를 짧게만 다루고, 배치 쓰기는 아래 「비어 있는 주제」에서 다룹니다 |
| 마지막 쓰기 우선(LWW)·자기 쓰기 읽기 | Booking.com, WhatsApp | [DDIA 6장 — 복제 지연](../../../05_data/book/designing-data-intensive-applications/06-03.%EB%B3%B5%EC%A0%9C%20%EC%A7%80%EC%97%B0%20%EB%AC%B8%EC%A0%9C%EC%99%80%20%EC%9D%BC%EA%B4%80%EC%84%B1%20%EB%B3%B4%EC%9E%A5.md), [DDIA 6장 — 쓰기 충돌](../../../05_data/book/designing-data-intensive-applications/06-05.%EC%93%B0%EA%B8%B0%20%EC%B6%A9%EB%8F%8C%20%ED%95%B4%EC%86%8C.md) | 없음 |
| 모니터링과 알림 임계값 | 프레임워크 | [SLO와 알림](../../../06_observability/01_Foundations/01-04.SLO%EC%99%80%20%EC%95%8C%EB%A6%BC%20%E2%80%94%20Error%20Budget%2C%20Burn%20Rate.md) | 없음 |



## 비어 있는 주제

> 아래 여덟 주제는 기존 노트에 없거나, 개념은 있어도 이 강의처럼 한 사례 안에서 이어 붙인 설명이 없습니다. 위에서부터 새로 쓸 가치가 큰 순서입니다.

"없음"은 `write/` 전체에서 관련 키워드가 0건이거나 본문과 무관한 곳에서만 나온 경우이고, "얕음"은 한두 문장 언급만 있는 경우입니다. "부분"은 개념 노트는 있지만 강의가 다루는 적용 방식이 빠진 경우입니다.

| 순위 | 주제 | 구간(시각) | 기존 노트 상태 | 쓸 이유 |
|------|------|------------|----------------|---------|
| 1 | 호텔 예약 도메인 모델 — 실제 방이 아니라 방 타입을 팔고, 호텔·방 타입·날짜마다 재고 행을 두고, 오버부킹 비율만큼 상한을 올리고, 결제 거래를 예약과 분리한다 | Booking.com (01:23~01:31) | 없음. "이중 예약"·"오버부킹"·"동적 가격" 0건. 가장 가까운 것은 [플래시 세일 재고 차감](../../book/bytebytego-system-design/07-03.%EA%B2%B0%EC%A0%9C%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%80%20%EA%B2%B0%EC%A0%9C%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%EB%A5%BC%20%EA%B2%B0%EC%A0%9C%20%EC%A3%BC%EB%AC%B8%EC%9C%BC%EB%A1%9C%20%EB%82%98%EB%88%A0%20PSP%20%EC%97%90%20%EB%A7%A1%EA%B8%B0%EA%B3%A0%20%ED%94%8C%EB%9E%98%EC%8B%9C%20%EC%84%B8%EC%9D%BC%EC%9D%80%20%EB%B9%84%EB%8F%99%EA%B8%B0%20%ED%81%90%EC%99%80%20%EC%9E%AC%EA%B3%A0%20%EC%B0%A8%EA%B0%90%20%EC%88%9C%EC%84%9C%EB%A1%9C%20%EA%B3%BC%ED%8C%90%EB%A7%A4%EB%A5%BC%20%EB%A7%89%EB%8A%94%EB%8B%A4.md) | 재고를 날짜 단위 행으로 쪼개는 모델링이 이 저장소에 한 번도 나오지 않습니다 |
| 2 | 이중 예약을 막는 세 방법의 비교 — 멱등 UUID, serializable, 재고 행 잠금 | Booking.com (01:34~01:37) | 부분. 격리 수준과 행 잠금은 위 표의 노트에 있으나 같은 시나리오 하나로 세 방법을 겨룬 설명은 없음 | 1번과 한 문서로 묶으면 모델과 동시성 제어가 같은 테이블 위에서 이어집니다 |
| 3 | 장애 대응 두 가지 — Redis 가 죽었을 때 오프라인 수신함을 DB 로 대신 읽고 복구 뒤 다시 맞추기, Kafka 브로커가 죽었을 때 채팅 서버가 로컬 append-only 버퍼에 쌓았다가 마지막 ID 이후부터 다시 내보내기 | WhatsApp (03:00~03:11) | 얕음. 캐시 폴백은 [캐싱 전략](../../../05_data/01_foundation/01-07.%EC%BA%90%EC%8B%B1%20%EC%A0%84%EB%9E%B5.md)에 한 문단, 로컬 버퍼와 재발행은 0건 | 강의 프레임워크 4단계(무엇이 깨지는가)를 실제로 보여 주는 절이라 시니어 신호에 해당합니다 |
| 4 | SQL 을 진실의 원천으로 두고 Elasticsearch 색인을 CDC 로 따라가게 하기 | Booking.com (01:43~01:49) | 부분. CDC 와 OpenSearch 는 따로 있으나 둘을 잇는 검색 색인 동기화는 1건 언급 | 두 노트를 잇는 다리 문서 하나로 충분합니다 |
| 5 | 메시지 저장 컨슈머의 배치 쓰기 — 1,000건을 한 건씩 넣으면 5초, 한 번에 넣으면 약 50ms | WhatsApp (02:34~02:41) | 없음. "배치 쓰기·batch insert" 는 JPA 노트에 1건뿐 | 처리량 차이를 숫자로 보여 주는 사례라 짧은 문서로 쓰기 좋습니다 |
| 6 | 다중 기기의 메시지 상태 전파 — 전송·수신·읽음 표시를 서버 사이로 넘기고, 충돌은 버전 번호와 LWW 로 정한다 | WhatsApp (02:15~02:20) | 부분. 가상 면접 12장은 기기별 최대 메시지 ID 로 새 메시지만 가져오는 동기화까지만 다룸 | 12장 노트 보강으로 처리할 수도 있습니다 |
| 7 | 종단 간 암호화(Signal 프로토콜의 identity key, prekey, 세션 키) | WhatsApp (02:41~02:45) | 얕음. 가상 면접 12장에 한 줄 | 강의 설명이 Signal 공식 설명과 어긋나 보이는 대목이 있어, 쓰려면 Signal 문서를 1차 자료로 삼아야 합니다 |
| 8 | 운영 작업 — 오래된 미디어·메시지를 지우는 정리 작업(스케줄러, 작업 큐, 워커 풀), 리전별 배치와 지연 기반 라우팅, feature flag 로 클라이언트 버전별 필드 걷어내기 | WhatsApp (02:58~03:00, 03:04~03:06, 03:11~03:13) | 얕음. 각각 다른 노트에 한두 줄 | 셋 다 강의에서도 짧게 지나가서 한 문서로 묶어야 분량이 됩니다 |

Spotify 사례는 이 목록에 넣지 않았습니다. 오디오 비트레이트와 egress 비용 계산을 빼면 가상 면접 14장(YouTube)과 구조가 같아서, 새 문서보다 14장 보강 후보로 보는 편이 맞습니다.



## 관련 문서

> 이 지도가 기대는 정독 노트입니다. 강의를 따라가다 막히면 여기서 개념을 찾습니다.

- [가상 면접 사례로 배우는 대규모 시스템 설계 기초](../../book/system-design/README.md) — 면접 진행법과 사례 15편
- [ByteByteGo 시스템 설계](../../book/bytebytego-system-design/README.md) — 데이터베이스·캐시·결제·저장소
- [데이터 중심 애플리케이션 설계](../../../05_data/book/designing-data-intensive-applications/README.md) — 복제·파티셔닝·트랜잭션의 원리
