---
title: 데이터 개발 키워드
tags: [landscape, data, database, storage, replication, consensus, stream]
status: final
source:
  - ../05_data/book/designing-data-intensive-applications/README.md
related:
  - README.md
  - spring-keywords.md
  - jvm-keywords.md
  - observability-keywords.md
  - ../05_data/README.md
updated: 2026-10-14
---

# 데이터 개발 키워드
---

> 데이터 개발 키워드 표. 문서를 쓸 때 참고합니다.



## 1단계 · 데이터 시스템의 축

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 운영 시스템과 분석 시스템 | 필수 | [운영 vs 분석](../05_data/book/designing-data-intensive-applications/01-01.%EC%9A%B4%EC%98%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20vs%20%EB%B6%84%EC%84%9D%20%EC%8B%9C%EC%8A%A4%ED%85%9C.md) | DDIA 1장 |
| 분산과 단일 노드 | 필수 | [분산 vs 단일 노드](../05_data/book/designing-data-intensive-applications/01-04.%EB%B6%84%EC%82%B0%20vs%20%EB%8B%A8%EC%9D%BC%20%EB%85%B8%EB%93%9C.md) | DDIA 1장 |
| 클라우드와 셀프 호스팅 | 추천 | [클라우드 vs 셀프 호스팅](../05_data/book/designing-data-intensive-applications/01-03.%ED%81%B4%EB%9D%BC%EC%9A%B0%EB%93%9C%20vs%20%EC%85%80%ED%94%84%20%ED%98%B8%EC%8A%A4%ED%8C%85.md) | DDIA 1장 |
| 응답 시간과 처리량 | 필수 | [응답 시간과 처리량](../05_data/book/designing-data-intensive-applications/02-02.%EC%84%B1%EB%8A%A5%20%E2%80%94%20%EC%9D%91%EB%8B%B5%20%EC%8B%9C%EA%B0%84%EA%B3%BC%20%EC%B2%98%EB%A6%AC%EB%9F%89.md) | DDIA 2장 |
| 신뢰성과 내결함성 | 필수 | [신뢰성과 내결함성](../05_data/book/designing-data-intensive-applications/02-03.%EC%8B%A0%EB%A2%B0%EC%84%B1%EA%B3%BC%20%EB%82%B4%EA%B2%B0%ED%95%A8%EC%84%B1.md) | DDIA 2장 |
| 확장성과 유지보수성 | 필수 | [확장성](../05_data/book/designing-data-intensive-applications/02-04.%ED%99%95%EC%9E%A5%EC%84%B1.md) · [유지보수성](../05_data/book/designing-data-intensive-applications/02-05.%EC%9C%A0%EC%A7%80%EB%B3%B4%EC%88%98%EC%84%B1.md) | DDIA 2장 |
| 사례로 보는 설계 선택 | 추천 | [홈 타임라인 사례](../05_data/book/designing-data-intensive-applications/02-01.%EC%82%AC%EB%A1%80%20%EC%97%B0%EA%B5%AC%20%E2%80%94%20%EC%86%8C%EC%85%9C%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%ED%99%88%20%ED%83%80%EC%9E%84%EB%9D%BC%EC%9D%B8.md) | DDIA 2장 |
| 데이터와 법 · 사회 | 선택 | [데이터·법·사회](../05_data/book/designing-data-intensive-applications/01-05.%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%C2%B7%EB%B2%95%C2%B7%EC%82%AC%ED%9A%8C.md) | DDIA 1·14장 |
| 저장 시 암호화 · DEK · KEK · envelope encryption | 추천 | | Real-World Cryptography 8장 |
| crypto-shredding — 데이터 대신 키를 파기한다 | 추천 | | |
| 삭제권과 보존 기간 — 백업까지 지워지는가 | 추천 | | DDIA 1·14장 |
| 용어를 먼저 고정하기 | 추천 | [DDIA 용어집](../05_data/book/designing-data-intensive-applications/00-01.%EC%9A%A9%EC%96%B4%EC%A7%91%20%E2%80%94%20DDIA%202%ED%8C%90%20%ED%95%B5%EC%8B%AC%20%EC%9A%A9%EC%96%B4%2050%EC%84%A0.md) | DDIA 서문 |
| 연결 풀링 · 커넥션 풀 관리 · 커넥션 리밋 · 아이들 타임아웃 · 맥스 라이프타임 · 커넥션 헬스 체크 | 선택 | [연결 풀링](../05_data/03_persistence/jdbc/01-01.%EC%BB%A4%EB%84%A5%EC%85%98%20%ED%92%80%EA%B3%BC%20DataSource.md) · [커넥션 풀 관리](../05_data/03_persistence/jdbc/01-01.%EC%BB%A4%EB%84%A5%EC%85%98%20%ED%92%80%EA%B3%BC%20DataSource.md) | |
| 핫 스토리지 · 웜 스토리지 · 콜드 스토리지 · 티어링 · 라이프사이클 정책 · 자동 티어링 | 선택 | [콜드 스토리지](../03_architecture/book/system-design/15-01.Google%20Drive%20%EB%8A%94%20%ED%8C%8C%EC%9D%BC%EC%9D%84%20%EB%B8%94%EB%A1%9D%EC%9C%BC%EB%A1%9C%20%EC%AA%BC%EA%B0%9C%20%EB%B3%80%EA%B2%BD%EB%B6%84%EB%A7%8C%20%EC%98%AC%EB%A6%AC%EA%B3%A0%20%EA%B0%95%ED%95%9C%20%EC%9D%BC%EA%B4%80%EC%84%B1%EC%9D%98%20%EB%A9%94%ED%83%80%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%99%80%20%EB%A1%B1%20%ED%8F%B4%EB%A7%81%EC%9C%BC%EB%A1%9C%20%EB%8F%99%EA%B8%B0%ED%99%94%ED%95%9C%EB%8B%A4.md) | |
| 데이터 만료 · TTL 기반 삭제 · 소프트 삭제 · 하드 삭제 | 선택 | | |
| 데이터 검증 · 엔드투엔드 체크섬 | 선택 | | |
| 쿼리 타임아웃 | 선택 | | |
| 소프트 삭제 유니크 제약 · 삭제 전파 | 선택 | | |
| 캐시 어사이드 · 라이트 스루 · 라이트 비하인드 · 리프레시 어헤드 · 스테일 와일 리밸리데이트 | 선택 | [캐시 어사이드](../05_data/01_foundation/01-07.%EC%BA%90%EC%8B%B1%20%EC%A0%84%EB%9E%B5.md) · [라이트 스루](../05_data/01_foundation/01-07.%EC%BA%90%EC%8B%B1%20%EC%A0%84%EB%9E%B5.md) · [라이트 비하인드](../05_data/01_foundation/01-07.%EC%BA%90%EC%8B%B1%20%EC%A0%84%EB%9E%B5.md) | |
| 캐시 무효화 · Redis 축출(eviction) · 캐시 스탬피드 · 락 기반 캐시 갱신 · 프로미스 기반 캐시 · 캐시 관통 · 캐시 붕괴 · 캐시 워밍 | 선택 | [캐시 스탬피드](../05_data/01_foundation/01-07.%EC%BA%90%EC%8B%B1%20%EC%A0%84%EB%9E%B5.md) · [캐시 관통](../05_data/01_foundation/01-07.%EC%BA%90%EC%8B%B1%20%EC%A0%84%EB%9E%B5.md) | |
| 분산 캐싱 · 멀티 레벨 캐시 · L1 캐시 · L2 캐시 · 로컬 캐시 · 리모트 캐시 | 선택 | [분산 캐싱](../03_architecture/book/bytebytego-system-design/02-01.%EC%BA%90%EC%8B%9C%20%EC%A0%84%EB%9E%B5%EC%9D%80%20%EC%9D%BD%EA%B8%B0%C2%B7%EC%93%B0%EA%B8%B0%20%EA%B2%BD%EB%A1%9C%EC%97%90%EC%84%9C%20%EC%BA%90%EC%8B%9C%20%EC%9E%90%EB%A6%AC%EB%A5%BC%20%EC%A0%95%ED%95%98%EA%B3%A0%20Redis%20%EB%8A%94%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EC%99%80%20%EB%8B%A8%EC%9D%BC%20%EC%8A%A4%EB%A0%88%EB%93%9C%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EB%A3%A8%ED%94%84%EB%A1%9C%20%EB%B9%A0%EB%A5%B4%EB%8B%A4.md) · [L1 캐시](../05_data/01_foundation/01-07.%EC%BA%90%EC%8B%B1%20%EC%A0%84%EB%9E%B5.md) · [L2 캐시](../05_data/01_foundation/01-07.%EC%BA%90%EC%8B%B1%20%EC%A0%84%EB%9E%B5.md) | |
| 캐시 컨트롤 · 이태그 · 라스트 모디파이드 · 304 응답 · 스테일 이프 에러 · 베리 헤더 · 캐시 키 · 캐시 변형 · 캐시 분할 · 콘텐츠 협상 캐시 · 동적 콘텐츠 캐싱 · 개인화 캐싱 | 선택 | | |
| 엣지 컴퓨팅 · CDN 엣지 · 엣지 함수 · 엣지 캐시 · 오리진 쉴드 · 오리진 요청 · 서러게이트 키 · 서러게이트 컨트롤 · 캐시 태그 · 퍼지 요청 · 소프트 퍼지 · 하드 퍼지 · 프리페치 · 예측 캐싱 · 엣지 사이드 인클루드·ESI · 프래그먼트 캐싱 · 홀 펀칭 · 캐시 어셈블리 | 선택 | [엣지 함수](../10_AI/project/flats/02-03.fetch%20handler%C2%B7env.DB%C2%B7env.FILES%C2%B7WebSocket.md) · [서러게이트 키](../05_data/03_persistence/jpa/01-03.%EC%8B%9D%EB%B3%84%EC%9E%90%20%EC%A0%84%EB%9E%B5.md) · [엣지 사이드 인클루드·ESI](../03_architecture/book/bmf_building-micro-frontends/03-09.%EB%AA%A8%EB%8D%98%20SSR%20%ED%94%84%EB%A0%88%EC%9E%84%EC%9B%8C%ED%81%AC%EC%99%80%20%EC%97%A3%EC%A7%80%20%E2%80%94%203%EC%9E%A5%EC%9D%84%20%EB%8B%AB%EC%9C%BC%EB%A9%B0.md) | |
| 썬더링 허드 · TTL 지터 | 선택 | | |
| 오리진 보호 · 오리진 접근 제어 · 핫링크 방지 | 선택 | | |



## 2단계 · 데이터 모델

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 관계형과 문서 모델 | 필수 | [관계형 vs 문서 모델](../05_data/book/designing-data-intensive-applications/03-01.%EA%B4%80%EA%B3%84%ED%98%95%20vs%20%EB%AC%B8%EC%84%9C%20%EB%AA%A8%EB%8D%B8.md) | DDIA 3장 |
| 정규화 · 비정규화 · 조인 | 필수 | [정규화·비정규화·조인](../05_data/book/designing-data-intensive-applications/03-02.%EC%A0%95%EA%B7%9C%ED%99%94%C2%B7%EB%B9%84%EC%A0%95%EA%B7%9C%ED%99%94%C2%B7%EC%A1%B0%EC%9D%B8.md) | DDIA 3장 |
| 스키마 유연성과 모델 선택 | 필수 | [모델 선택과 스키마 유연성](../05_data/book/designing-data-intensive-applications/03-04.%EB%AA%A8%EB%8D%B8%20%EC%84%A0%ED%83%9D%EA%B3%BC%20%EC%8A%A4%ED%82%A4%EB%A7%88%20%EC%9C%A0%EC%97%B0%EC%84%B1.md) | DDIA 3장 |
| 그래프 데이터 모델 | 추천 | [그래프 데이터 모델](../05_data/book/designing-data-intensive-applications/03-05.%EA%B7%B8%EB%9E%98%ED%94%84%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%AA%A8%EB%8D%B8.md) | DDIA 3장 |
| 분석용 스키마 — 별 · 눈송이 | 추천 | [분석용 스키마](../05_data/book/designing-data-intensive-applications/03-03.%EB%B6%84%EC%84%9D%EC%9A%A9%20%EC%8A%A4%ED%82%A4%EB%A7%88%20%E2%80%94%20%EB%B3%84%C2%B7%EB%88%88%EC%86%A1%EC%9D%B4%C2%B7OBT.md) | DDIA 3장 |
| 이벤트 소싱 · CQRS | 추천 | [이벤트 소싱·CQRS](../05_data/book/designing-data-intensive-applications/03-06.%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EC%86%8C%EC%8B%B1%C2%B7CQRS%C2%B7DataFrame.md) | DDIA 3장 |
| 데이터 정규화 · 역정규화 · 외래 키 제약 · 유니크 제약 · IDENTITY 키 | 선택 | [데이터 정규화](../05_data/book/designing-data-intensive-applications/03-02.%EC%A0%95%EA%B7%9C%ED%99%94%C2%B7%EB%B9%84%EC%A0%95%EA%B7%9C%ED%99%94%C2%B7%EC%A1%B0%EC%9D%B8.md) · [역정규화](../05_data/book/designing-data-intensive-applications/03-02.%EC%A0%95%EA%B7%9C%ED%99%94%C2%B7%EB%B9%84%EC%A0%95%EA%B7%9C%ED%99%94%C2%B7%EC%A1%B0%EC%9D%B8.md) | |
| 시간대와 날짜 저장 · 문자 인코딩 · 정렬 규칙 collation | 선택 | [시간대와 날짜 저장](../01_language/java/01_Core/01-05.%EB%82%A0%EC%A7%9C%EC%99%80%20%EC%8B%9C%EA%B0%84%20API.md) · [문자 인코딩](../01_language/java/01_Core/05-02.%EB%AC%B8%EC%9E%90%20%EC%9D%B8%EC%BD%94%EB%94%A9.md) | |
| 쿼리 빌더 | 선택 | [쿼리 빌더](../05_data/03_persistence/jpa/07-01.%EB%8F%84%EA%B5%AC%20%ED%98%BC%EC%9A%A9%20%ED%8C%A8%ED%84%B4.md) | |
| 데이터베이스 마이그레이션 · 제로 다운타임 마이그레이션 | 선택 | [제로 다운타임 마이그레이션](../03_architecture/04_ddd/03-03.%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%20%EB%A6%AC%ED%8C%A9%ED%86%A0%EB%A7%81.md) | |
| 머티리얼라이즈드 뷰 · 저장 프로시저 | 선택 | [머티리얼라이즈드 뷰](../05_data/01_foundation/01-07.%EC%BA%90%EC%8B%B1%20%EC%A0%84%EB%9E%B5.md) | |
| 타임시리즈 데이터베이스 · 그래프 데이터베이스 | 선택 | [타임시리즈 데이터베이스](../03_architecture/book/bytebytego-system-design/08-03.%EB%A9%94%ED%8A%B8%EB%A6%AD%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%EC%9D%80%20%EC%8B%9C%EA%B3%84%EC%97%B4%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%EC%97%90%20%EC%93%B0%EA%B8%B0%EB%A5%BC%20%EB%AA%B0%EC%95%84%20%EB%8B%B4%EA%B3%A0%20%EC%88%98%EC%A7%91%C2%B7%EC%A7%88%EC%9D%98%C2%B7%EA%B2%BD%EB%B3%B4%C2%B7%EC%8B%9C%EA%B0%81%ED%99%94%EB%A1%9C%20%EB%82%98%EB%89%9C%EB%8B%A4.md) · [그래프 데이터베이스](../05_data/01_foundation/01-06.NoSQL%20%EB%B9%84%EA%B5%90.md) | |
| 벡터 데이터베이스 | 선택 | | |
| 관계형 데이터베이스 · 문서형 데이터베이스 · 키-값 저장소 | 선택 | | |
| 시계열 데이터 모델 · 보존 정책 · 다운샘플링 · 쓰기 증폭 | 선택 | | |
| 리드 모델 · 라이트 모델 · 프로젝션 · 이벤트 스토어 · 스냅샷 스토어 · 이벤트 업캐스팅 | 선택 | [이벤트 스토어](../04_messaging/07_CQRS_EventSourcing/01-02.Event%20Sourcing.md) | |
| ORM | 선택 | [ORM](../05_data/03_persistence/jpa/01-01.ORM%20%EA%B0%9C%EB%85%90.md) | |
| DB 트리거 | 선택 | | |



## 3단계 · 저장 엔진과 인덱스

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| OLTP 저장과 인덱스 기초 | 필수 | [OLTP 저장과 인덱스 기초](../05_data/book/designing-data-intensive-applications/04-01.OLTP%20%EC%A0%80%EC%9E%A5%EA%B3%BC%20%EC%9D%B8%EB%8D%B1%EC%8A%A4%20%EA%B8%B0%EC%B4%88.md) | DDIA 4장 |
| B-tree 기초와 구현 | 필수 | | Database Internals 2·4장 |
| LSM 과 로그 구조 저장 | 필수 | [LSM 저장 엔진](../05_data/book/designing-data-intensive-applications/04-02.LSM%20%EC%A0%80%EC%9E%A5%20%EC%97%94%EC%A7%84.md) | Database Internals 7장 |
| B-tree 와 LSM 비교 | 필수 | [B-tree와 LSM 비교](../05_data/book/designing-data-intensive-applications/04-03.B-tree%EC%99%80%20LSM%20%EB%B9%84%EA%B5%90.md) | DDIA 4장 |
| 파일 포맷과 B-tree 변형 | 추천 | | Database Internals 3·6장 |
| WAL 과 세그먼트 로그 | 추천 | | PoDS 3·4장 |
| 보조 인덱스와 인메모리 | 필수 | [보조 인덱스·인메모리](../05_data/book/designing-data-intensive-applications/04-04.%EB%B3%B4%EC%A1%B0%20%EC%9D%B8%EB%8D%B1%EC%8A%A4%EC%99%80%20%EC%9D%B8%EB%A9%94%EB%AA%A8%EB%A6%AC%20%EC%A0%80%EC%9E%A5.md) | DDIA 4장 |
| 컬럼 지향 저장 | 추천 | [컬럼 지향 저장](../05_data/book/designing-data-intensive-applications/04-05.%EB%B6%84%EC%84%9D%EC%9A%A9%20%EC%BB%AC%EB%9F%BC%20%EC%A7%80%ED%96%A5%20%EC%A0%80%EC%9E%A5.md) | DDIA 4장 |
| 다차원 · 전문 · 벡터 인덱스 | 추천 | [다차원·전문·벡터 인덱스](../05_data/book/designing-data-intensive-applications/04-06.%EB%8B%A4%EC%B0%A8%EC%9B%90%C2%B7%EC%A0%84%EB%AC%B8%C2%B7%EB%B2%A1%ED%84%B0%20%EC%9D%B8%EB%8D%B1%EC%8A%A4.md) | DDIA 4장 |
| 전문 검색 엔진의 색인 | 선택 | | Elasticsearch 3·4 · 7장 |
| 검색 엔진 캐시와 cold start — 파일시스템 캐시 · 노드 쿼리 캐시 · 샤드 요청 캐시 | 추천 | [당근 발표 정리](_digest/2026-10-10_당근_빌더_밋업_2026_인프라_발표_5편.md) | [검색 속도 조정](https://www.elastic.co/docs/deploy-manage/production-guidance/optimize-performance/search-speed) |
| 데이터베이스 인덱스 · B-트리 · 해시 인덱스 · 비트맵 인덱스 · 클러스터드 인덱스 · 논클러스터드 인덱스 | 선택 | [데이터베이스 인덱스](../05_data/01_foundation/01-05.%EC%9D%B8%EB%8D%B1%EC%8A%A4%20%EC%9D%B4%EB%A1%A0.md) · [B-트리](../05_data/book/designing-data-intensive-applications/04-03.B-tree%EC%99%80%20LSM%20%EB%B9%84%EA%B5%90.md) · [해시 인덱스](../05_data/book/designing-data-intensive-applications/04-01.OLTP%20%EC%A0%80%EC%9E%A5%EA%B3%BC%20%EC%9D%B8%EB%8D%B1%EC%8A%A4%20%EA%B8%B0%EC%B4%88.md) · [비트맵 인덱스](../05_data/book/designing-data-intensive-applications/04-05.%EB%B6%84%EC%84%9D%EC%9A%A9%20%EC%BB%AC%EB%9F%BC%20%EC%A7%80%ED%96%A5%20%EC%A0%80%EC%9E%A5.md) · [논클러스터드 인덱스](../05_data/book/designing-data-intensive-applications/07-04.%EB%B3%B4%EC%A1%B0%20%EC%9D%B8%EB%8D%B1%EC%8A%A4%EC%99%80%207%EC%9E%A5%20%EC%A2%85%ED%95%A9.md) | |
| 커버링 인덱스 · 부분 인덱스 · 표현식 인덱스 · 컴포지트·멀티컬럼 인덱스 · 인덱스 인터섹션 | 선택 | [커버링 인덱스](../05_data/01_foundation/01-05.%EC%9D%B8%EB%8D%B1%EC%8A%A4%20%EC%9D%B4%EB%A1%A0.md) · [부분 인덱스](../05_data/01_foundation/01-05.%EC%9D%B8%EB%8D%B1%EC%8A%A4%20%EC%9D%B4%EB%A1%A0.md) · [표현식 인덱스](../05_data/01_foundation/01-05.%EC%9D%B8%EB%8D%B1%EC%8A%A4%20%EC%9D%B4%EB%A1%A0.md) · [컴포지트·멀티컬럼 인덱스](../05_data/01_foundation/01-05.%EC%9D%B8%EB%8D%B1%EC%8A%A4%20%EC%9D%B4%EB%A1%A0.md) | |
| EXPLAIN ANALYZE · 쿼리 플래너 · 코스트 기반 옵티마이저 · 규칙 기반 옵티마이저 · 통계 정보 · 히스토그램 · 카디널리티 추정 · 통계 갱신 | 선택 | [EXPLAIN ANALYZE](../05_data/01_foundation/01-05.%EC%9D%B8%EB%8D%B1%EC%8A%A4%20%EC%9D%B4%EB%A1%A0.md) | |
| 시퀀셜 스캔 · 인덱스 스캔 · 인덱스 온리 스캔 · 부분 스캔 | 선택 | [인덱스 온리 스캔](../05_data/01_foundation/01-05.%EC%9D%B8%EB%8D%B1%EC%8A%A4%20%EC%9D%B4%EB%A1%A0.md) | |
| 중첩 루프 조인 · 해시 조인 · 머지 조인 · 조인 순서 · 조인 알고리즘 선택 | 선택 | [머지 조인](../05_data/book/designing-data-intensive-applications/11-03.%EB%B6%84%EC%82%B0%20%EC%9E%A1%20%EC%98%A4%EC%BC%80%EC%8A%A4%ED%8A%B8%EB%A0%88%EC%9D%B4%EC%85%98%EA%B3%BC%20MapReduce.md) | |
| 쿼리 최적화 · N+1 쿼리 · 서브쿼리 최적화 · 공통 테이블 표현식 · 윈도우 함수 | 선택 | [쿼리 최적화](../07_devops/02_Jenkins/04_api/09-03.API%20%EC%BF%BC%EB%A6%AC%20%EC%B5%9C%EC%A0%81%ED%99%94%EC%99%80%20%EC%9A%B4%EC%98%81.md) · [N+1 쿼리](../05_data/03_persistence/jpa/03-03.%ED%94%84%EB%A1%9D%EC%8B%9C%EC%99%80%20N%2B1.md) · [공통 테이블 표현식](../05_data/book/designing-data-intensive-applications/03-05.%EA%B7%B8%EB%9E%98%ED%94%84%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%AA%A8%EB%8D%B8.md) | |
| 페이지 스플릿 · 인덱스 프래그먼테이션 · 리빌드 · 리오가나이즈 | 선택 | | |
| 트랜잭션 로그 · 체크포인트 · 버퍼 풀 · 오토 배큠 | 선택 | | |
| LSM-트리 · 톰스톤 · 가비지 컬렉션 지연 · 컴팩션 · 메이저 컴팩션 · 마이너 컴팩션 · 레벨드 컴팩션 · 사이즈 티어드 컴팩션 · 타임 윈도우 컴팩션 | 선택 | [LSM-트리](../05_data/book/designing-data-intensive-applications/04-02.LSM%20%EC%A0%80%EC%9E%A5%20%EC%97%94%EC%A7%84.md) · [톰스톤](../04_messaging/04_BrokerArchitecture/08-01.%EB%A9%94%EC%8B%9C%EC%A7%80%20%EC%A0%95%EB%A6%AC%20%E2%80%94%20Log%20Retention%C2%B7Compaction%C2%B7Tombstone.md) · [컴팩션](../06_observability/book/mastering_prometheus/03-03.TSDB%20%EC%A0%80%EC%9E%A5%20%EA%B5%AC%EC%A1%B0.md) | |
| 로우 스토리지 · 컬럼나 스토리지 · 하이브리드 스토리지 · 압축 알고리즘 · 델타 인코딩 · 딕셔너리 인코딩 · 런렝스 인코딩 · 페이지 압축 · 블록 압축 · 트랜잭션 로그 압축 | 선택 | [컬럼나 스토리지](../05_data/book/designing-data-intensive-applications/04-05.%EB%B6%84%EC%84%9D%EC%9A%A9%20%EC%BB%AC%EB%9F%BC%20%EC%A7%80%ED%96%A5%20%EC%A0%80%EC%9E%A5.md) | |
| B+트리 | 선택 | | |
| 풀텍스트 검색 · 역인덱스 · 관련성 스코어 | 선택 | [풀텍스트 검색](../05_data/book/designing-data-intensive-applications/04-06.%EB%8B%A4%EC%B0%A8%EC%9B%90%C2%B7%EC%A0%84%EB%AC%B8%C2%B7%EB%B2%A1%ED%84%B0%20%EC%9D%B8%EB%8D%B1%EC%8A%A4.md) · [역인덱스](../05_data/book/designing-data-intensive-applications/04-06.%EB%8B%A4%EC%B0%A8%EC%9B%90%C2%B7%EC%A0%84%EB%AC%B8%C2%B7%EB%B2%A1%ED%84%B0%20%EC%9D%B8%EB%8D%B1%EC%8A%A4.md) · [관련성 스코어](../06_observability/book/dgos_opensearch/05-01.%EA%B2%80%EC%83%89%20%ED%95%B5%EC%8B%AC%20API%20%E2%80%94%20%EC%BF%BC%EB%A6%AC%20%EC%B2%98%EB%A6%AC%EC%99%80%20leaf%20%EC%BF%BC%EB%A6%AC.md) | |
| 패싯 검색 · 퍼지 검색 · 오토컴플리트 | 선택 | [오토컴플리트](../03_architecture/book/system-design/13-01.%EA%B2%80%EC%83%89%EC%96%B4%20%EC%9E%90%EB%8F%99%EC%99%84%EC%84%B1%EC%9D%80%20%ED%8A%B8%EB%9D%BC%EC%9D%B4%20%EB%85%B8%EB%93%9C%EC%97%90%20%EC%83%81%EC%9C%84%20k%20%EA%B0%9C%EB%A5%BC%20%EC%BA%90%EC%8B%9C%ED%95%98%EA%B3%A0%20%EC%88%98%EC%A7%91%20%EA%B2%BD%EB%A1%9C%EA%B0%80%20%EC%A3%BC%EA%B8%B0%EC%A0%81%EC%9C%BC%EB%A1%9C%20%ED%8A%B8%EB%9D%BC%EC%9D%B4%EB%A5%BC%20%EB%8B%A4%EC%8B%9C%20%EB%A7%8C%EB%93%A0%EB%8B%A4.md) | |
| 벡터 유사도 · 코사인 유사도 · 근사 최근접 이웃(ANN) · HNSW · IVF | 선택 | | |



## 4단계 · 인코딩과 데이터플로우

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 인코딩과 호환성 기초 | 필수 | [인코딩과 호환성 기초](../05_data/book/designing-data-intensive-applications/05-01.%EC%9D%B8%EC%BD%94%EB%94%A9%EA%B3%BC%20%ED%98%B8%ED%99%98%EC%84%B1%20%EA%B8%B0%EC%B4%88.md) | DDIA 5장 |
| JSON · XML · 이진 변형 | 필수 | [JSON·XML·이진 변형](../05_data/book/designing-data-intensive-applications/05-02.JSON%C2%B7XML%C2%B7%EC%9D%B4%EC%A7%84%20%EB%B3%80%ED%98%95.md) | DDIA 5장 |
| Protocol Buffers 와 Avro | 필수 | [Protocol Buffers와 Avro](../05_data/book/designing-data-intensive-applications/05-03.Protocol%20Buffers%EC%99%80%20Avro.md) | DDIA 5장 |
| DB · REST · RPC 데이터플로우 | 필수 | [데이터플로우](../05_data/book/designing-data-intensive-applications/05-04.%EB%8D%B0%EC%9D%B4%ED%84%B0%ED%94%8C%EB%A1%9C%EC%9A%B0%20%E2%80%94%20DB%C2%B7REST%C2%B7RPC.md) | DDIA 5장 |
| durable execution | 추천 | [durable execution](../05_data/book/designing-data-intensive-applications/05-05.durable%20execution%EA%B3%BC%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EA%B8%B0%EB%B0%98%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.md) | DDIA 5장 |
| 이벤트 기반 아키텍처 | 추천 | [durable execution](../05_data/book/designing-data-intensive-applications/05-05.durable%20execution%EA%B3%BC%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EA%B8%B0%EB%B0%98%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.md) | DDIA 5장 |
| 스키마 레지스트리 · 스키마 진화 · 스키마 버저닝 · 이벤트 버저닝 · 메시지 스키마 진화 · 백워드 호환성 · 백워드 호환 스키마 · 포워드 호환 스키마 · 풀 호환 스키마 | 선택 | [스키마 레지스트리](../03_architecture/05_edd/04-01.%EC%A7%80%EC%9B%90%20%EB%8F%84%EA%B5%AC%20%E2%80%94%20%EC%8A%A4%ED%82%A4%EB%A7%88%20%EB%A0%88%EC%A7%80%EC%8A%A4%ED%8A%B8%EB%A6%AC%C2%B7%ED%95%A0%EB%8B%B9%EB%9F%89%C2%B7%EC%98%A4%ED%94%84%EC%85%8B%20%EA%B4%80%EB%A6%AC.md) · [스키마 진화](../04_messaging/02_MessageContract/02-02.Avro%20%EC%8A%A4%ED%82%A4%EB%A7%88%20%EC%A7%84%ED%99%94%20%ED%8C%A8%ED%84%B4.md) · [백워드 호환성](../03_architecture/05_edd/01-03.%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EA%B3%84%EC%95%BD%EA%B3%BC%20%EC%8A%A4%ED%82%A4%EB%A7%88%20%EC%84%A4%EA%B3%84%20%EC%9B%90%EC%B9%99.md) · [백워드 호환 스키마](../03_architecture/05_edd/01-03.%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EA%B3%84%EC%95%BD%EA%B3%BC%20%EC%8A%A4%ED%82%A4%EB%A7%88%20%EC%84%A4%EA%B3%84%20%EC%9B%90%EC%B9%99.md) · [포워드 호환 스키마](../03_architecture/05_edd/01-03.%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EA%B3%84%EC%95%BD%EA%B3%BC%20%EC%8A%A4%ED%82%A4%EB%A7%88%20%EC%84%A4%EA%B3%84%20%EC%9B%90%EC%B9%99.md) | |



## 5단계 · 복제와 샤딩

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 단일 리더 복제 | 필수 | [복제 개요와 단일 리더](../05_data/book/designing-data-intensive-applications/06-01.%EB%B3%B5%EC%A0%9C%20%EA%B0%9C%EC%9A%94%EC%99%80%20%EB%8B%A8%EC%9D%BC%20%EB%A6%AC%EB%8D%94.md) | DDIA 6장 |
| 복제 로그와 노드 장애 | 필수 | [노드 장애와 복제 로그](../05_data/book/designing-data-intensive-applications/06-02.%EB%85%B8%EB%93%9C%20%EC%9E%A5%EC%95%A0%20%EC%B2%98%EB%A6%AC%EC%99%80%20%EB%B3%B5%EC%A0%9C%20%EB%A1%9C%EA%B7%B8.md) | DDIA 6장 |
| 복제 지연과 일관성 보장 | 필수 | [복제 지연](../05_data/book/designing-data-intensive-applications/06-03.%EB%B3%B5%EC%A0%9C%20%EC%A7%80%EC%97%B0%20%EB%AC%B8%EC%A0%9C%EC%99%80%20%EC%9D%BC%EA%B4%80%EC%84%B1%20%EB%B3%B4%EC%9E%A5.md) | DDIA 6장 |
| 다중 리더와 쓰기 충돌 | 추천 | [다중 리더 복제](../05_data/book/designing-data-intensive-applications/06-04.%EB%8B%A4%EC%A4%91%20%EB%A6%AC%EB%8D%94%20%EB%B3%B5%EC%A0%9C.md) · [쓰기 충돌 해소](../05_data/book/designing-data-intensive-applications/06-05.%EC%93%B0%EA%B8%B0%20%EC%B6%A9%EB%8F%8C%20%ED%95%B4%EC%86%8C.md) | DDIA 6장 |
| 리더리스 복제와 정족수 | 필수 | [리더리스 복제](../05_data/book/designing-data-intensive-applications/06-06.%EB%A6%AC%EB%8D%94%EB%A6%AC%EC%8A%A4%20%EB%B3%B5%EC%A0%9C%EC%99%80%206%EC%9E%A5%20%EC%A2%85%ED%95%A9.md) | DDIA 6장 |
| 키 범위 샤딩 | 필수 | [샤딩 개요와 키 범위 샤딩](../05_data/book/designing-data-intensive-applications/07-01.%EC%83%A4%EB%94%A9%20%EA%B0%9C%EC%9A%94%EC%99%80%20%ED%82%A4%20%EB%B2%94%EC%9C%84%20%EC%83%A4%EB%94%A9.md) | DDIA 7장 · PoDS 20장 |
| 해시 샤딩과 일관 해싱 | 필수 | [해시 샤딩과 일관 해싱](../05_data/book/designing-data-intensive-applications/07-02.%ED%95%B4%EC%8B%9C%20%EC%83%A4%EB%94%A9%EA%B3%BC%20%EC%9D%BC%EA%B4%80%20%ED%95%B4%EC%8B%B1.md) | DDIA 7장 |
| rendezvous 해싱(HRW) · 가중치 — 건강한 후보를 먼저 거르고 해싱한다 | 추천 | | [Thaler·Ravishankar 1998](https://doi.org/10.1109/90.663936) |
| 요청 라우팅과 리밸런싱 | 필수 | [요청 라우팅과 리밸런싱](../05_data/book/designing-data-intensive-applications/07-03.%EC%9A%94%EC%B2%AD%20%EB%9D%BC%EC%9A%B0%ED%8C%85%EA%B3%BC%20%EB%A6%AC%EB%B0%B8%EB%9F%B0%EC%8B%B1.md) | DDIA 7장 · PoDS 19장 |
| 샤딩과 보조 인덱스 | 추천 | [샤딩과 보조 인덱스](../05_data/book/designing-data-intensive-applications/07-04.%EB%B3%B4%EC%A1%B0%20%EC%9D%B8%EB%8D%B1%EC%8A%A4%EC%99%80%207%EC%9E%A5%20%EC%A2%85%ED%95%A9.md) | DDIA 7장 |
| 복제 일관성의 구현 | 추천 | [N·W·R 정족수](../03_architecture/book/system-design/06-01.%ED%82%A4-%EA%B0%92%20%EC%A0%80%EC%9E%A5%EC%86%8C%EB%8A%94%20CAP%20%EC%84%A0%ED%83%9D%20%EC%95%84%EB%9E%98%20%EC%95%88%EC%A0%95%20%ED%95%B4%EC%8B%9C%EB%A1%9C%20%EB%82%98%EB%88%84%EA%B3%A0%20N%C2%B7W%C2%B7R%20%EC%A0%95%EC%A1%B1%EC%88%98%EB%A1%9C%20%EB%B3%B5%EC%A0%9C%20%EC%9D%BC%EA%B4%80%EC%84%B1%EC%9D%84%20%EA%B3%A0%EB%A5%B8%EB%8B%A4.md) · [벡터 시계·가십·머클 트리](../03_architecture/book/system-design/06-02.%EB%B2%A1%ED%84%B0%20%EC%8B%9C%EA%B3%84%C2%B7%EA%B0%80%EC%8B%AD%C2%B7%EC%9E%84%EC%8B%9C%20%EC%9C%84%ED%83%81%C2%B7%EB%A8%B8%ED%81%B4%20%ED%8A%B8%EB%A6%AC%EA%B0%80%20%EC%B6%A9%EB%8F%8C%EA%B3%BC%20%EC%9E%A5%EC%95%A0%EB%A5%BC%20%EB%8B%A4%EB%A3%A8%EA%B3%A0%20%EC%93%B0%EA%B8%B0%EC%99%80%20%EC%9D%BD%EA%B8%B0%EB%8A%94%20SSTable%20%EC%9D%84%20%EC%A7%80%EB%82%9C%EB%8B%A4.md) | Database Internals 11·12장 · System Design Interview 6장 |
| 무중단 클러스터 이전 — 쓰기 복제 · shadow read · 응답 전환 | 추천 | [당근 발표 정리](_digest/2026-10-10_당근_빌더_밋업_2026_인프라_발표_5편.md) | |
| 읽기 복제본 | 선택 | [읽기 복제본](../03_architecture/book/bytebytego-system-design/01-02.%ED%8C%8C%ED%8B%B0%EC%85%94%EB%8B%9D%EA%B3%BC%20%EC%9D%BD%EA%B8%B0%20%EB%B3%B5%EC%A0%9C%EB%B3%B8%EC%9D%80%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%EB%A5%BC%20%EB%84%93%ED%9E%88%EA%B3%A0%20%EC%A0%84%EC%97%AD%20%EC%9C%A0%EC%9D%BC%20ID%20%EB%8A%94%20%EB%82%98%EB%89%9C%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%97%90%20%EC%88%9C%EC%84%9C%EB%A5%BC%20%EC%A4%80%EB%8B%A4.md) | |
| 물리적 복제 · 논리적 복제 · 스트리밍 복제 · 비동기 복제 · 반동기 복제 · 동기 복제 · 멀티 소스 복제 · 그룹 복제 · 갈레라 | 선택 | [반동기 복제](../05_data/book/designing-data-intensive-applications/06-01.%EB%B3%B5%EC%A0%9C%20%EA%B0%9C%EC%9A%94%EC%99%80%20%EB%8B%A8%EC%9D%BC%20%EB%A6%AC%EB%8D%94.md) | |
| 아카이브 로그 · 바이너리 로그 · 릴레이 로그 · GTID · 포지션 기반 복제 | 선택 | | |
| 파티셔닝 · 레인지 파티셔닝 · 리스트 파티셔닝 · 해시 파티셔닝 · 컴포지트 파티셔닝 · 파티션 프루닝 · 파티션 와이즈 조인 · 글로벌 인덱스 · 로컬 인덱스 | 선택 | [파티셔닝](../03_architecture/book/bytebytego-system-design/01-02.%ED%8C%8C%ED%8B%B0%EC%85%94%EB%8B%9D%EA%B3%BC%20%EC%9D%BD%EA%B8%B0%20%EB%B3%B5%EC%A0%9C%EB%B3%B8%EC%9D%80%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%EB%A5%BC%20%EB%84%93%ED%9E%88%EA%B3%A0%20%EC%A0%84%EC%97%AD%20%EC%9C%A0%EC%9D%BC%20ID%20%EB%8A%94%20%EB%82%98%EB%89%9C%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%97%90%20%EC%88%9C%EC%84%9C%EB%A5%BC%20%EC%A4%80%EB%8B%A4.md) | |
| 데이터베이스 샤딩 · 샤드 키 · 핫 샤드 · 콜드 샤드 · 데이터 리샤딩 | 선택 | [데이터베이스 샤딩](../03_architecture/book/bytebytego-system-design/01-02.%ED%8C%8C%ED%8B%B0%EC%85%94%EB%8B%9D%EA%B3%BC%20%EC%9D%BD%EA%B8%B0%20%EB%B3%B5%EC%A0%9C%EB%B3%B8%EC%9D%80%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%EB%A5%BC%20%EB%84%93%ED%9E%88%EA%B3%A0%20%EC%A0%84%EC%97%AD%20%EC%9C%A0%EC%9D%BC%20ID%20%EB%8A%94%20%EB%82%98%EB%89%9C%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%97%90%20%EC%88%9C%EC%84%9C%EB%A5%BC%20%EC%A4%80%EB%8B%A4.md) · [샤드 키](../03_architecture/book/bytebytego-system-design/01-02.%ED%8C%8C%ED%8B%B0%EC%85%94%EB%8B%9D%EA%B3%BC%20%EC%9D%BD%EA%B8%B0%20%EB%B3%B5%EC%A0%9C%EB%B3%B8%EC%9D%80%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%EB%A5%BC%20%EB%84%93%ED%9E%88%EA%B3%A0%20%EC%A0%84%EC%97%AD%20%EC%9C%A0%EC%9D%BC%20ID%20%EB%8A%94%20%EB%82%98%EB%89%9C%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%97%90%20%EC%88%9C%EC%84%9C%EB%A5%BC%20%EC%A4%80%EB%8B%A4.md) | |
| 크로스 샤드 쿼리 · 분산 조인 · 팬아웃 쿼리 · 스캐터 개더 | 선택 | | |
| 쿼럼 · 쿼럼 기반 쓰기 · 다수결 읽기 · 리드 리페어 · 힌티드 핸드오프 · 안티 엔트로피 · 스플릿 브레인 · 스플릿 브레인 방지 | 선택 | [쿼럼](../05_data/book/designing-data-intensive-applications/10-04.%ED%95%A9%EC%9D%98%EC%99%80%20%EC%BD%94%EB%94%94%EB%84%A4%EC%9D%B4%EC%85%98%20%EC%84%9C%EB%B9%84%EC%8A%A4.md) · [쿼럼 기반 쓰기](../03_architecture/book/system-design/06-01.%ED%82%A4-%EA%B0%92%20%EC%A0%80%EC%9E%A5%EC%86%8C%EB%8A%94%20CAP%20%EC%84%A0%ED%83%9D%20%EC%95%84%EB%9E%98%20%EC%95%88%EC%A0%95%20%ED%95%B4%EC%8B%9C%EB%A1%9C%20%EB%82%98%EB%88%84%EA%B3%A0%20N%C2%B7W%C2%B7R%20%EC%A0%95%EC%A1%B1%EC%88%98%EB%A1%9C%20%EB%B3%B5%EC%A0%9C%20%EC%9D%BC%EA%B4%80%EC%84%B1%EC%9D%84%20%EA%B3%A0%EB%A5%B8%EB%8B%A4.md) · [힌티드 핸드오프](../03_architecture/book/system-design/06-02.%EB%B2%A1%ED%84%B0%20%EC%8B%9C%EA%B3%84%C2%B7%EA%B0%80%EC%8B%AD%C2%B7%EC%9E%84%EC%8B%9C%20%EC%9C%84%ED%83%81%C2%B7%EB%A8%B8%ED%81%B4%20%ED%8A%B8%EB%A6%AC%EA%B0%80%20%EC%B6%A9%EB%8F%8C%EA%B3%BC%20%EC%9E%A5%EC%95%A0%EB%A5%BC%20%EB%8B%A4%EB%A3%A8%EA%B3%A0%20%EC%93%B0%EA%B8%B0%EC%99%80%20%EC%9D%BD%EA%B8%B0%EB%8A%94%20SSTable%20%EC%9D%84%20%EC%A7%80%EB%82%9C%EB%8B%A4.md) | |



## 6단계 · 트랜잭션과 격리

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| ACID 와 트랜잭션 개요 | 필수 | [ACID와 트랜잭션 개요](../05_data/book/designing-data-intensive-applications/08-01.ACID%EC%99%80%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%20%EA%B0%9C%EC%9A%94.md) | DDIA 8장 |
| 약한 격리와 스냅샷 격리 | 필수 | [약한 격리·스냅샷](../05_data/book/designing-data-intensive-applications/08-02.%EC%95%BD%ED%95%9C%20%EA%B2%A9%EB%A6%AC%20%EC%88%98%EC%A4%80%EA%B3%BC%20%EC%8A%A4%EB%83%85%EC%83%B7%20%EA%B2%A9%EB%A6%AC.md) | DDIA 8장 |
| Write Skew 와 직렬화 | 필수 | [Write Skew](../05_data/book/designing-data-intensive-applications/08-03.Write%20Skew%EC%99%80%20%EC%A7%81%EB%A0%AC%ED%99%94%20%EA%B0%80%EB%8A%A5%EC%84%B1.md) | DDIA 8장 |
| 분산 트랜잭션과 2PC | 필수 | [분산 트랜잭션과 2PC](../05_data/book/designing-data-intensive-applications/08-04.%EB%B6%84%EC%82%B0%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%EA%B3%BC%202PC.md) | DDIA 8장 · PoDS 21장 |
| 트랜잭션 처리와 복구 | 추천 | | Database Internals 5장 |
| 분산 트랜잭션 구현 | 추천 | | Database Internals 13장 |
| 데이터베이스 트랜잭션 · ACID 속성 | 선택 | [데이터베이스 트랜잭션](../03_architecture/03_distributed/01-04.%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%20%EA%B2%BD%EA%B3%84%EC%99%80%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%9D%BC%EA%B4%80%EC%84%B1.md) · [ACID 속성](../05_data/book/designing-data-intensive-applications/08-01.ACID%EC%99%80%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%20%EA%B0%9C%EC%9A%94.md) | |
| 격리 수준 · 읽기 커밋됨 · 직렬화 격리 · 직렬화 가능성 · MVCC | 선택 | [격리 수준](../03_architecture/book/bytebytego-system-design/01-01.%EA%B2%A9%EB%A6%AC%20%EC%88%98%EC%A4%80%EA%B3%BC%20%EB%82%99%EA%B4%80%EC%A0%81%20%EC%9E%A0%EA%B8%88%EC%9D%B4%20%EB%8F%99%EC%8B%9C%20%EC%93%B0%EA%B8%B0%EC%9D%98%20%EC%9D%B4%EC%83%81%20%ED%98%84%EC%83%81%EC%9D%84%20%EB%A7%89%EA%B3%A0%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%AA%A8%EC%96%91%EC%9D%B4%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%20%EC%A2%85%EB%A5%98%EB%A5%BC%20%EA%B3%A0%EB%A5%B8%EB%8B%A4.md) · [읽기 커밋됨](../05_data/book/designing-data-intensive-applications/08-02.%EC%95%BD%ED%95%9C%20%EA%B2%A9%EB%A6%AC%20%EC%88%98%EC%A4%80%EA%B3%BC%20%EC%8A%A4%EB%83%85%EC%83%B7%20%EA%B2%A9%EB%A6%AC.md) · [직렬화 격리](../03_architecture/docs/system-design-course/01-01.%ED%98%B8%ED%85%94%20%EC%98%88%EC%95%BD%EC%9D%80%20%EB%B0%A9%20%ED%83%80%EC%9E%85%EC%9D%98%20%EB%82%A0%EC%A7%9C%EB%B3%84%20%EC%9E%AC%EA%B3%A0%20%ED%96%89%EC%9D%84%20%ED%8C%94%EA%B3%A0%20%EA%B7%B8%20%ED%96%89%EC%9D%84%20%EC%9E%A0%EA%B0%80%20%EC%9D%B4%EC%A4%91%20%EC%98%88%EC%95%BD%EC%9D%84%20%EB%A7%89%EB%8A%94%EB%8B%A4.md) · [직렬화 가능성](../05_data/book/designing-data-intensive-applications/08-03.Write%20Skew%EC%99%80%20%EC%A7%81%EB%A0%AC%ED%99%94%20%EA%B0%80%EB%8A%A5%EC%84%B1.md) · [MVCC](../03_architecture/book/bytebytego-system-design/01-01.%EA%B2%A9%EB%A6%AC%20%EC%88%98%EC%A4%80%EA%B3%BC%20%EB%82%99%EA%B4%80%EC%A0%81%20%EC%9E%A0%EA%B8%88%EC%9D%B4%20%EB%8F%99%EC%8B%9C%20%EC%93%B0%EA%B8%B0%EC%9D%98%20%EC%9D%B4%EC%83%81%20%ED%98%84%EC%83%81%EC%9D%84%20%EB%A7%89%EA%B3%A0%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%AA%A8%EC%96%91%EC%9D%B4%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%20%EC%A2%85%EB%A5%98%EB%A5%BC%20%EA%B3%A0%EB%A5%B8%EB%8B%A4.md) | |
| 낙관적 락 · CAS 조건부 갱신 | 선택 | [낙관적 락](../05_data/03_persistence/jpa/04-02.%EB%82%99%EA%B4%80%EC%A0%81%20%EB%B9%84%EA%B4%80%EC%A0%81%20%EB%9D%BD.md) · [CAS 조건부 갱신](../01_language/book/jpf_java-performance/09-03.%EB%8F%99%EA%B8%B0%ED%99%94%20%EB%B9%84%EC%9A%A9%20%E2%80%94%20Amdahl%C2%B7register%20flushing%C2%B7CAS.md) | |
| 데드락 탐지 | 선택 | | |
| 갱신 손실 | 선택 | | |
| 원장 패턴 · 재고 차감 | 선택 | | |
| 2단계 커밋 · 3단계 커밋 · 아웃박스 패턴 · 아웃박스 릴레이 · 사가 패턴 · 사가 오케스트레이션 · 사가 코레오그래피 · 컴펜세이팅 트랜잭션 · 트라이앤컴펜세이트 | 선택 | [2단계 커밋](../04_messaging/05_ConsistencyPattern/03-06.Kafka%20Transactions%20%EB%82%B4%EB%B6%80%20%E2%80%94%20Zombie%20Fencing%C2%B72PC.md) · [아웃박스 패턴](../03_architecture/05_edd/03-01.Saga%2C%20Outbox%2C%20Request-Response%20Bridge.md) · [아웃박스 릴레이](../03_architecture/05_edd/03-01.Saga%2C%20Outbox%2C%20Request-Response%20Bridge.md) · [사가 패턴](../03_architecture/05_edd/03-01.Saga%2C%20Outbox%2C%20Request-Response%20Bridge.md) · [사가 오케스트레이션](../03_architecture/05_edd/03-02.Choreography%20vs%20Orchestration.md) · [사가 코레오그래피](../03_architecture/05_edd/03-02.Choreography%20vs%20Orchestration.md) · [컴펜세이팅 트랜잭션](../09_spring/06_events/01-04.%EB%8F%99%EA%B8%B0%EC%99%80%20%EB%B9%84%EB%8F%99%EA%B8%B0%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%E2%80%94%20%40Async%EC%99%80%20%EB%B3%B4%EC%83%81%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98.md) | |



## 7단계 · 분산의 문제

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 부분 실패와 비신뢰 네트워크 | 필수 | [부분 실패](../05_data/book/designing-data-intensive-applications/09-01.%EB%B6%80%EB%B6%84%20%EC%8B%A4%ED%8C%A8%EC%99%80%20%EB%B9%84%EC%8B%A0%EB%A2%B0%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC.md) | DDIA 9장 |
| 불신뢰 시계 | 필수 | [불신뢰 시계](../05_data/book/designing-data-intensive-applications/09-02.%EB%B6%88%EC%8B%A0%EB%A2%B0%20%EC%8B%9C%EA%B3%84.md) | DDIA 9장 |
| 진실 · 거짓 · 시스템 모델 | 필수 | [진실·거짓·시스템 모델](../05_data/book/designing-data-intensive-applications/09-03.%EC%A7%84%EC%8B%A4%C2%B7%EA%B1%B0%EC%A7%93%C2%B7%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EB%AA%A8%EB%8D%B8.md) | DDIA 9장 |
| 분산 시스템 검증 | 추천 | [분산 시스템 검증](../05_data/book/designing-data-intensive-applications/09-04.%EB%B6%84%EC%82%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B2%80%EC%A6%9D%EA%B3%BC%209%EC%9E%A5%20%EC%A2%85%ED%95%A9.md) | DDIA 9장 |
| 장애 감지 | 필수 | | Database Internals 9장 · PoDS 7장 |
| 리더 선출 | 필수 | | Database Internals 10장 · PoDS 6장 |
| 임차와 상태 감시 | 추천 | | PoDS 26·27장 |
| 가십 전파와 창발 리더 | 선택 | | PoDS 28·29장 |
| 리더 리스 · 하트비트 · 리스 갱신 | 선택 | [하트비트](../02_os/book/npg_network-programming-with-go/03-03.%ED%83%80%EC%9E%84%EC%95%84%EC%9B%83%EC%9D%80%20Dialer%C2%B7context%20%EB%A1%9C%2C%20%EC%9C%A0%ED%9C%B4%20%EA%B0%90%EC%A7%80%EB%8A%94%20%EB%8D%B0%EB%93%9C%EB%9D%BC%EC%9D%B8%EA%B3%BC%20%ED%95%98%ED%8A%B8%EB%B9%84%ED%8A%B8%EB%A1%9C%20%EA%B1%B4%EB%8B%A4.md) | |
| 가십 프로토콜 · 클러스터 멤버십 · 멤버십 변경 · 조인 프로토콜 · 리브 프로토콜 · 실패 감지 · 의심 타임아웃 · 핑 프로토콜 · 가십 기반 실패 감지 | 선택 | [가십 프로토콜](../03_architecture/book/system-design/06-02.%EB%B2%A1%ED%84%B0%20%EC%8B%9C%EA%B3%84%C2%B7%EA%B0%80%EC%8B%AD%C2%B7%EC%9E%84%EC%8B%9C%20%EC%9C%84%ED%83%81%C2%B7%EB%A8%B8%ED%81%B4%20%ED%8A%B8%EB%A6%AC%EA%B0%80%20%EC%B6%A9%EB%8F%8C%EA%B3%BC%20%EC%9E%A5%EC%95%A0%EB%A5%BC%20%EB%8B%A4%EB%A3%A8%EA%B3%A0%20%EC%93%B0%EA%B8%B0%EC%99%80%20%EC%9D%BD%EA%B8%B0%EB%8A%94%20SSTable%20%EC%9D%84%20%EC%A7%80%EB%82%9C%EB%8B%A4.md) | |



## 8단계 · 일관성과 합의

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 선형성 | 필수 | [선형성](../05_data/book/designing-data-intensive-applications/10-01.%EC%84%A0%ED%98%95%EC%84%B1.md) | DDIA 10장 |
| 선형성의 비용과 CAP | 필수 | [선형성의 비용과 CAP](../05_data/book/designing-data-intensive-applications/10-02.%EC%84%A0%ED%98%95%EC%84%B1%EC%9D%98%20%EB%B9%84%EC%9A%A9%EA%B3%BC%20CAP.md) | DDIA 10장 |
| ID 생성기와 논리 시계 | 필수 | [ID 생성기와 논리 시계](../05_data/book/designing-data-intensive-applications/10-03.ID%20%EC%83%9D%EC%84%B1%EA%B8%B0%EC%99%80%20%EB%85%BC%EB%A6%AC%20%EC%8B%9C%EA%B3%84.md) | DDIA 10장 · PoDS 22·23장 |
| 합의와 코디네이션 서비스 | 필수 | [합의와 코디네이션 서비스](../05_data/book/designing-data-intensive-applications/10-04.%ED%95%A9%EC%9D%98%EC%99%80%20%EC%BD%94%EB%94%94%EB%84%A4%EC%9D%B4%EC%85%98%20%EC%84%9C%EB%B9%84%EC%8A%A4.md) | DDIA 10장 |
| 합의 알고리즘 | 필수 | | Database Internals 14장 |
| Paxos 와 Replicated Log | 추천 | | PoDS 11·12장 |
| 일관 코어 | 추천 | | PoDS 25장 |
| 버전 값과 버전 벡터 | 추천 | | PoDS 17·18장 |
| 시계 경계 대기 | 선택 | | PoDS 24장 |
| CAP 정리 · 최종 일관성 · 선형화 가능성 · 인과 일관성 · 읽기-자신의-쓰기 · 단조 읽기 · CRDT | 선택 | [CAP 정리](../05_data/book/designing-data-intensive-applications/10-02.%EC%84%A0%ED%98%95%EC%84%B1%EC%9D%98%20%EB%B9%84%EC%9A%A9%EA%B3%BC%20CAP.md) · [최종 일관성](../03_architecture/03_distributed/01-04.%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%20%EA%B2%BD%EA%B3%84%EC%99%80%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%9D%BC%EA%B4%80%EC%84%B1.md) · [선형화 가능성](../05_data/book/designing-data-intensive-applications/10-02.%EC%84%A0%ED%98%95%EC%84%B1%EC%9D%98%20%EB%B9%84%EC%9A%A9%EA%B3%BC%20CAP.md) · [인과 일관성](../05_data/book/designing-data-intensive-applications/13-01.%EB%8D%B0%EC%9D%B4%ED%84%B0%20%ED%86%B5%ED%95%A9%20%E2%80%94%20%ED%8C%8C%EC%83%9D%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%99%80%20%EC%A0%84%EC%88%9C%EC%84%9C%EC%9D%98%20%ED%95%9C%EA%B3%84.md) · [읽기-자신의-쓰기](../05_data/book/designing-data-intensive-applications/06-03.%EB%B3%B5%EC%A0%9C%20%EC%A7%80%EC%97%B0%20%EB%AC%B8%EC%A0%9C%EC%99%80%20%EC%9D%BC%EA%B4%80%EC%84%B1%20%EB%B3%B4%EC%9E%A5.md) · [CRDT](../05_data/book/designing-data-intensive-applications/06-05.%EC%93%B0%EA%B8%B0%20%EC%B6%A9%EB%8F%8C%20%ED%95%B4%EC%86%8C.md) | |
| 논리적 시계 · 물리적 시계 · 벡터 클록 · 시계 동기화 | 선택 | [논리적 시계](../05_data/book/designing-data-intensive-applications/10-03.ID%20%EC%83%9D%EC%84%B1%EA%B8%B0%EC%99%80%20%EB%85%BC%EB%A6%AC%20%EC%8B%9C%EA%B3%84.md) · [물리적 시계](../05_data/book/designing-data-intensive-applications/09-02.%EB%B6%88%EC%8B%A0%EB%A2%B0%20%EC%8B%9C%EA%B3%84.md) · [벡터 클록](../03_architecture/book/system-design/06-02.%EB%B2%A1%ED%84%B0%20%EC%8B%9C%EA%B3%84%C2%B7%EA%B0%80%EC%8B%AD%C2%B7%EC%9E%84%EC%8B%9C%20%EC%9C%84%ED%83%81%C2%B7%EB%A8%B8%ED%81%B4%20%ED%8A%B8%EB%A6%AC%EA%B0%80%20%EC%B6%A9%EB%8F%8C%EA%B3%BC%20%EC%9E%A5%EC%95%A0%EB%A5%BC%20%EB%8B%A4%EB%A3%A8%EA%B3%A0%20%EC%93%B0%EA%B8%B0%EC%99%80%20%EC%9D%BD%EA%B8%B0%EB%8A%94%20SSTable%20%EC%9D%84%20%EC%A7%80%EB%82%9C%EB%8B%A4.md) | |
| 분산 락 · 분산 락 서비스 · 리스 기반 락 · 펜싱 토큰 · 펜싱 · 레드락 · 주키퍼 락 · etcd 락 · 컨센서스 기반 락 | 선택 | [분산 락](../05_data/book/designing-data-intensive-applications/09-03.%EC%A7%84%EC%8B%A4%C2%B7%EA%B1%B0%EC%A7%93%C2%B7%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EB%AA%A8%EB%8D%B8.md) · [분산 락 서비스](../05_data/book/designing-data-intensive-applications/10-04.%ED%95%A9%EC%9D%98%EC%99%80%20%EC%BD%94%EB%94%94%EB%84%A4%EC%9D%B4%EC%85%98%20%EC%84%9C%EB%B9%84%EC%8A%A4.md) · [펜싱 토큰](../05_data/book/designing-data-intensive-applications/09-03.%EC%A7%84%EC%8B%A4%C2%B7%EA%B1%B0%EC%A7%93%C2%B7%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EB%AA%A8%EB%8D%B8.md) · [펜싱](../05_data/book/designing-data-intensive-applications/09-03.%EC%A7%84%EC%8B%A4%C2%B7%EA%B1%B0%EC%A7%93%C2%B7%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EB%AA%A8%EB%8D%B8.md) | |
| BASE · 머클 트리 | 선택 | [BASE](../05_data/01_foundation/01-06.NoSQL%20%EB%B9%84%EA%B5%90.md) · [머클 트리](../03_architecture/book/system-design/06-02.%EB%B2%A1%ED%84%B0%20%EC%8B%9C%EA%B3%84%C2%B7%EA%B0%80%EC%8B%AD%C2%B7%EC%9E%84%EC%8B%9C%20%EC%9C%84%ED%83%81%C2%B7%EB%A8%B8%ED%81%B4%20%ED%8A%B8%EB%A6%AC%EA%B0%80%20%EC%B6%A9%EB%8F%8C%EA%B3%BC%20%EC%9E%A5%EC%95%A0%EB%A5%BC%20%EB%8B%A4%EB%A3%A8%EA%B3%A0%20%EC%93%B0%EA%B8%B0%EC%99%80%20%EC%9D%BD%EA%B8%B0%EB%8A%94%20SSTable%20%EC%9D%84%20%EC%A7%80%EB%82%9C%EB%8B%A4.md) | |



## 9단계 · 배치와 스트림

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| Unix 도구와 배치 개요 | 필수 | [배치와 Unix 도구](../05_data/book/designing-data-intensive-applications/11-01.%EB%B0%B0%EC%B9%98%20%EC%B2%98%EB%A6%AC%20%EA%B0%9C%EC%9A%94%EC%99%80%20Unix%20%EB%8F%84%EA%B5%AC.md) | DDIA 11장 |
| 분산 FS 와 오브젝트 스토어 | 필수 | [분산 FS·오브젝트 스토어](../05_data/book/designing-data-intensive-applications/11-02.%EB%B6%84%EC%82%B0%20%ED%8C%8C%EC%9D%BC%EC%8B%9C%EC%8A%A4%ED%85%9C%EA%B3%BC%20%EC%98%A4%EB%B8%8C%EC%A0%9D%ED%8A%B8%20%EC%8A%A4%ED%86%A0%EC%96%B4.md) | DDIA 11장 |
| MapReduce 와 잡 오케스트레이션 | 추천 | [MapReduce](../05_data/book/designing-data-intensive-applications/11-03.%EB%B6%84%EC%82%B0%20%EC%9E%A1%20%EC%98%A4%EC%BC%80%EC%8A%A4%ED%8A%B8%EB%A0%88%EC%9D%B4%EC%85%98%EA%B3%BC%20MapReduce.md) | DDIA 11장 |
| 데이터플로우 엔진 | 추천 | [데이터플로우 엔진](../05_data/book/designing-data-intensive-applications/11-04.%EB%8D%B0%EC%9D%B4%ED%84%B0%ED%94%8C%EB%A1%9C%EC%9A%B0%20%EC%97%94%EC%A7%84%EA%B3%BC%20%EB%B0%B0%EC%B9%98%20%ED%99%9C%EC%9A%A9.md) | DDIA 11장 |
| 메시지 브로커와 로그 기반 | 필수 | [메시지 브로커](../05_data/book/designing-data-intensive-applications/12-01.%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%EC%A0%84%EC%86%A1%20%E2%80%94%20%EB%A9%94%EC%8B%9C%EC%A7%80%20%EB%B8%8C%EB%A1%9C%EC%BB%A4%EC%99%80%20%EB%A1%9C%EA%B7%B8%20%EA%B8%B0%EB%B0%98%20%EB%B8%8C%EB%A1%9C%EC%BB%A4.md) | DDIA 12장 |
| 작업 큐의 전달 보장 — 확인 응답과 재전달 · 재시도 · 멱등 키 · dead letter | 추천 | [메시지 브로커](../05_data/book/designing-data-intensive-applications/12-01.%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%EC%A0%84%EC%86%A1%20%E2%80%94%20%EB%A9%94%EC%8B%9C%EC%A7%80%20%EB%B8%8C%EB%A1%9C%EC%BB%A4%EC%99%80%20%EB%A1%9C%EA%B7%B8%20%EA%B8%B0%EB%B0%98%20%EB%B8%8C%EB%A1%9C%EC%BB%A4.md) · [정확성과 신뢰](../05_data/book/designing-data-intensive-applications/13-04.%EC%A0%95%ED%99%95%EC%84%B1%EA%B3%BC%20%EC%8B%A0%EB%A2%B0%C2%B713%EC%9E%A5%20%EC%A2%85%ED%95%A9.md) | DDIA 12·13장 · PoDS 15장 |
| 데이터베이스와 스트림 · CDC | 필수 | [DB와 스트림](../05_data/book/designing-data-intensive-applications/12-02.%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%EC%99%80%20%EC%8A%A4%ED%8A%B8%EB%A6%BC.md) | DDIA 12장 |
| CEP · 윈도우 · 조인 | 필수 | [스트림 처리](../05_data/book/designing-data-intensive-applications/12-03.%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%EC%B2%98%EB%A6%AC%20%E2%80%94%20CEP%C2%B7%EC%9C%88%EB%8F%84%EC%9A%B0%C2%B7%EC%A1%B0%EC%9D%B8.md) | DDIA 12장 |
| 시간 추론과 내결함성 | 추천 | [시간 추론](../05_data/book/designing-data-intensive-applications/12-04.%EC%8B%9C%EA%B0%84%20%EC%B6%94%EB%A1%A0%EA%B3%BC%20%EB%82%B4%EA%B2%B0%ED%95%A8%EC%84%B1%C2%B712%EC%9E%A5%20%EC%A2%85%ED%95%A9.md) | DDIA 12장 |
| 파생 데이터와 DB 언번들링 | 추천 | [DB 언번들링](../05_data/book/designing-data-intensive-applications/13-02.%EB%B0%B0%EC%B9%98%C2%B7%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%ED%86%B5%ED%95%A9%EA%B3%BC%20DB%20%EC%96%B8%EB%B2%88%EB%93%A4%EB%A7%81.md) | DDIA 13장 |
| 정확성과 신뢰 | 추천 | [정확성과 신뢰](../05_data/book/designing-data-intensive-applications/13-04.%EC%A0%95%ED%99%95%EC%84%B1%EA%B3%BC%20%EC%8B%A0%EB%A2%B0%C2%B713%EC%9E%A5%20%EC%A2%85%ED%95%A9.md) | DDIA 13장 |
| 블롭 스토리지 · 스토리지 일관성 모델 · 사전 서명 URL | 선택 | [블롭 스토리지](../03_architecture/book/system-design/14-01.YouTube%20%EC%97%85%EB%A1%9C%EB%93%9C%EB%8A%94%20%EC%9B%90%EB%B3%B8%EC%9D%84%20BLOB%20%EC%A0%80%EC%9E%A5%EC%86%8C%EC%97%90%20%EB%91%90%EA%B3%A0%20DAG%20%EB%A1%9C%20%EC%AA%BC%EA%B0%A0%20%ED%8A%B8%EB%9E%9C%EC%8A%A4%EC%BD%94%EB%94%A9%EC%9D%84%20%EA%B1%B0%EC%B3%90%20CDN%20%EC%9C%BC%EB%A1%9C%20%EC%8A%A4%ED%8A%B8%EB%A6%AC%EB%B0%8D%ED%95%9C%EB%8B%A4.md) · [사전 서명 URL](../03_architecture/book/system-design/14-02.%ED%8A%B8%EB%9E%9C%EC%8A%A4%EC%BD%94%EB%94%A9%EC%9D%80%20%EC%A0%84%EC%B2%98%EB%A6%AC%C2%B7DAG%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC%C2%B7%EC%9E%90%EC%9B%90%20%EA%B4%80%EB%A6%AC%EC%9E%90%C2%B7%EC%9E%91%EC%97%85%20%EC%84%9C%EB%B2%84%EB%A1%9C%20%EB%82%98%EB%89%98%EA%B3%A0%20%EC%82%AC%EC%A0%84%20%EC%84%9C%EB%AA%85%20URL%C2%B7CDN%20%EB%B9%84%EC%9A%A9%C2%B7%EC%98%A4%EB%A5%98%20%EC%B2%98%EB%A6%AC%EB%A1%9C%20%EB%8B%A4%EB%93%AC%EB%8A%94%EB%8B%A4.md) | |
| 메시지 큐 · Pub/Sub | 선택 | [메시지 큐](../03_architecture/book/system-design/10-01.%EC%95%8C%EB%A6%BC%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%80%20%EC%A0%9C3%EC%9E%90%20%ED%91%B8%EC%8B%9C%C2%B7SMS%C2%B7%EC%9D%B4%EB%A9%94%EC%9D%BC%20%EC%84%9C%EB%B9%84%EC%8A%A4%20%EC%95%9E%EC%97%90%20%EB%A9%94%EC%8B%9C%EC%A7%80%20%ED%81%90%EC%99%80%20%EC%9E%91%EC%97%85%20%EC%84%9C%EB%B2%84%EB%A5%BC%20%EB%91%90%EC%96%B4%20%EC%9E%AC%EC%8B%9C%EB%8F%84%EC%99%80%20%EC%A4%91%EB%B3%B5%EC%9D%84%20%EB%8B%A4%EB%A3%AC%EB%8B%A4.md) · [Pub/Sub](../01_language/java/03_DesignPatterns/01-04.%ED%96%89%EB%8F%99%20%ED%8C%A8%ED%84%B4.md) | |
| 백그라운드 워커 · 작업 스케줄링 · 우선순위 큐 · 지연 큐 · 재시도 큐 | 선택 | | |
| 이메일 발송 인프라 · 푸시·SMS 발송 | 선택 | [이메일 발송 인프라](../03_architecture/book/bytebytego-system-design/08-02.Gmail%20%EC%9D%80%20SMTP%20%EB%A1%9C%20%EB%B3%B4%EB%82%B4%EA%B3%A0%20IMAP%C2%B7POP%20%EC%9C%BC%EB%A1%9C%20%EB%B0%9B%EC%9C%BC%EB%A9%B0%20Google%20Maps%20%EB%8A%94%20%ED%83%80%EC%9D%BC%EC%9D%84%20%EC%A4%8C%20%EB%A0%88%EB%B2%A8%EB%B3%84%EB%A1%9C%20%EB%AF%B8%EB%A6%AC%20%EA%B7%B8%EB%A0%A4%20%EB%82%B4%EB%A0%A4%EC%A4%80%EB%8B%A4.md) · [푸시·SMS 발송](../03_architecture/book/system-design/10-01.%EC%95%8C%EB%A6%BC%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%80%20%EC%A0%9C3%EC%9E%90%20%ED%91%B8%EC%8B%9C%C2%B7SMS%C2%B7%EC%9D%B4%EB%A9%94%EC%9D%BC%20%EC%84%9C%EB%B9%84%EC%8A%A4%20%EC%95%9E%EC%97%90%20%EB%A9%94%EC%8B%9C%EC%A7%80%20%ED%81%90%EC%99%80%20%EC%9E%91%EC%97%85%20%EC%84%9C%EB%B2%84%EB%A5%BC%20%EB%91%90%EC%96%B4%20%EC%9E%AC%EC%8B%9C%EB%8F%84%EC%99%80%20%EC%A4%91%EB%B3%B5%EC%9D%84%20%EB%8B%A4%EB%A3%AC%EB%8B%A4.md) | |
| 데드 레터 큐 · 데드 레터 처리 · 포이즌 메시지 | 선택 | [데드 레터 큐](../04_messaging/05_ConsistencyPattern/06-01.Poison%20Message%20%EC%B2%98%EB%A6%AC%20%E2%80%94%20DLT%20%ED%9D%A1%EC%88%98%EC%9D%98%20%ED%95%9C%EA%B3%84%EC%99%80%20%EA%B2%A9%EB%A6%AC%20%ED%81%90.md) · [데드 레터 처리](../04_messaging/05_ConsistencyPattern/06-01.Poison%20Message%20%EC%B2%98%EB%A6%AC%20%E2%80%94%20DLT%20%ED%9D%A1%EC%88%98%EC%9D%98%20%ED%95%9C%EA%B3%84%EC%99%80%20%EA%B2%A9%EB%A6%AC%20%ED%81%90.md) · [포이즌 메시지](../04_messaging/05_ConsistencyPattern/06-01.Poison%20Message%20%EC%B2%98%EB%A6%AC%20%E2%80%94%20DLT%20%ED%9D%A1%EC%88%98%EC%9D%98%20%ED%95%9C%EA%B3%84%EC%99%80%20%EA%B2%A9%EB%A6%AC%20%ED%81%90.md) | |
| 최소한 한 번 전달 · 정확히 한 번 전달 · 메시지 중복 제거 · 인박스 패턴 · 멱등성 리시버 · 디듀플리케이션 테이블 | 선택 | [최소한 한 번 전달](../03_architecture/book/bytebytego-system-design/05-01.Kafka%20%EB%8A%94%20%EC%88%9C%EC%B0%A8%20IO%20%EC%99%80%20%EC%A0%9C%EB%A1%9C%20%EC%B9%B4%ED%94%BC%EB%A1%9C%20%EB%B9%A0%EB%A5%B4%EA%B3%A0%20%EC%A0%84%EB%8B%AC%20%EB%B3%B4%EC%9E%A5%EC%9D%80%20%EC%B5%9C%EB%8C%80%20%ED%95%9C%20%EB%B2%88%C2%B7%EC%B5%9C%EC%86%8C%20%ED%95%9C%20%EB%B2%88%C2%B7%EC%A0%95%ED%99%95%ED%9E%88%20%ED%95%9C%20%EB%B2%88%EC%9C%BC%EB%A1%9C%20%EA%B0%88%EB%A6%B0%EB%8B%A4.md) · [정확히 한 번 전달](../03_architecture/book/bytebytego-system-design/05-01.Kafka%20%EB%8A%94%20%EC%88%9C%EC%B0%A8%20IO%20%EC%99%80%20%EC%A0%9C%EB%A1%9C%20%EC%B9%B4%ED%94%BC%EB%A1%9C%20%EB%B9%A0%EB%A5%B4%EA%B3%A0%20%EC%A0%84%EB%8B%AC%20%EB%B3%B4%EC%9E%A5%EC%9D%80%20%EC%B5%9C%EB%8C%80%20%ED%95%9C%20%EB%B2%88%C2%B7%EC%B5%9C%EC%86%8C%20%ED%95%9C%20%EB%B2%88%C2%B7%EC%A0%95%ED%99%95%ED%9E%88%20%ED%95%9C%20%EB%B2%88%EC%9C%BC%EB%A1%9C%20%EA%B0%88%EB%A6%B0%EB%8B%A4.md) · [메시지 중복 제거](../03_architecture/book/bytebytego-system-design/08-01.%ED%8A%B8%EC%9C%84%ED%84%B0%20%ED%83%80%EC%9E%84%EB%9D%BC%EC%9D%B8%C2%B7%EA%B5%AC%EA%B8%80%20%EB%8F%85%EC%8A%A4%20%EB%8F%99%EC%8B%9C%20%ED%8E%B8%EC%A7%91%C2%B7%EC%8A%AC%EB%9E%99%20%EC%95%8C%EB%A6%BC%20%ED%8C%90%EC%A0%95%C2%B7%ED%81%AC%EB%A1%A4%EB%9F%AC%20%EC%A4%91%EB%B3%B5%20%EC%A0%9C%EA%B1%B0%EB%8A%94%20%ED%8C%AC%EC%95%84%EC%9B%83%C2%B7OT%C2%B7%ED%9D%90%EB%A6%84%EB%8F%84%C2%B7%EB%B8%94%EB%A3%B8%20%ED%95%84%ED%84%B0%EB%A1%9C%20%ED%91%BC%EB%8B%A4.md) · [인박스 패턴](../04_messaging/05_ConsistencyPattern/03-01.Inbox.md) · [멱등성 리시버](../04_messaging/05_ConsistencyPattern/03-01.Inbox.md) · [디듀플리케이션 테이블](../04_messaging/05_ConsistencyPattern/03-01.Inbox.md) | |
| 메시지 순서 보장 · 순서 보장 키 · 파티션 키 · 컨슈머 그룹 · 파티션 재조정 · 컨슈머 랙 · 오프셋 관리 | 선택 | [메시지 순서 보장](../04_messaging/05_ConsistencyPattern/02-01.Outbox.md) · [컨슈머 그룹](../04_messaging/04_BrokerArchitecture/06-02.AdminClient%20%EC%84%A4%EC%A0%95%C2%B7%EC%BB%A8%EC%8A%88%EB%A8%B8%EA%B7%B8%EB%A3%B9%C2%B7%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0.md) · [파티션 재조정](../04_messaging/04_BrokerArchitecture/01-04.%EB%A6%AC%EB%B0%B8%EB%9F%B0%EC%8A%A4%20%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C.md) · [컨슈머 랙](../04_messaging/04_BrokerArchitecture/06-02.AdminClient%20%EC%84%A4%EC%A0%95%C2%B7%EC%BB%A8%EC%8A%88%EB%A8%B8%EA%B7%B8%EB%A3%B9%C2%B7%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0.md) · [오프셋 관리](../03_architecture/05_edd/04-01.%EC%A7%80%EC%9B%90%20%EB%8F%84%EA%B5%AC%20%E2%80%94%20%EC%8A%A4%ED%82%A4%EB%A7%88%20%EB%A0%88%EC%A7%80%EC%8A%A4%ED%8A%B8%EB%A6%AC%C2%B7%ED%95%A0%EB%8B%B9%EB%9F%89%C2%B7%EC%98%A4%ED%94%84%EC%85%8B%20%EA%B4%80%EB%A6%AC.md) | |
| 데이터 웨어하우스 · 데이터 레이크 · 스키마 온 리드 · 스키마 온 라이트 · 데이터 리니지 | 선택 | [데이터 웨어하우스](../05_data/book/designing-data-intensive-applications/01-01.%EC%9A%B4%EC%98%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20vs%20%EB%B6%84%EC%84%9D%20%EC%8B%9C%EC%8A%A4%ED%85%9C.md) · [데이터 레이크](../05_data/book/designing-data-intensive-applications/01-01.%EC%9A%B4%EC%98%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20vs%20%EB%B6%84%EC%84%9D%20%EC%8B%9C%EC%8A%A4%ED%85%9C.md) · [스키마 온 리드](../05_data/book/designing-data-intensive-applications/03-04.%EB%AA%A8%EB%8D%B8%20%EC%84%A0%ED%83%9D%EA%B3%BC%20%EC%8A%A4%ED%82%A4%EB%A7%88%20%EC%9C%A0%EC%97%B0%EC%84%B1.md) | |
| 배치 처리 · 스트리밍 처리 · 람다 아키텍처 · 카파 아키텍처 · 스트리밍 알고리즘 · 레이트 리미티드 소스 | 선택 | [배치 처리](../05_data/book/designing-data-intensive-applications/11-01.%EB%B0%B0%EC%B9%98%20%EC%B2%98%EB%A6%AC%20%EA%B0%9C%EC%9A%94%EC%99%80%20Unix%20%EB%8F%84%EA%B5%AC.md) · [스트리밍 처리](../03_architecture/05_edd/02-03.%EA%B2%B0%EC%A0%95%EC%A0%81%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%EC%B2%98%EB%A6%AC%20%E2%80%94%20%EC%9B%8C%ED%84%B0%EB%A7%88%ED%81%AC%EC%99%80%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%ED%83%80%EC%9E%84.md) · [람다 아키텍처](../05_data/book/designing-data-intensive-applications/13-02.%EB%B0%B0%EC%B9%98%C2%B7%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%ED%86%B5%ED%95%A9%EA%B3%BC%20DB%20%EC%96%B8%EB%B2%88%EB%93%A4%EB%A7%81.md) · [카파 아키텍처](../05_data/book/designing-data-intensive-applications/13-02.%EB%B0%B0%EC%B9%98%C2%B7%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%ED%86%B5%ED%95%A9%EA%B3%BC%20DB%20%EC%96%B8%EB%B2%88%EB%93%A4%EB%A7%81.md) | |
| 윈도우 집계 · 텀블링 윈도우 · 세션 윈도우 · 워터마크 · 이벤트 타임 · 프로세싱 타임 · 인제스천 타임 | 선택 | [텀블링 윈도우](../04_messaging/06_StreamProcessing/01-01.Kafka%20Streams.md) · [세션 윈도우](../04_messaging/06_StreamProcessing/01-01.Kafka%20Streams.md) · [워터마크](../03_architecture/05_edd/02-03.%EA%B2%B0%EC%A0%95%EC%A0%81%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%EC%B2%98%EB%A6%AC%20%E2%80%94%20%EC%9B%8C%ED%84%B0%EB%A7%88%ED%81%AC%EC%99%80%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%ED%83%80%EC%9E%84.md) · [이벤트 타임](../03_architecture/05_edd/02-03.%EA%B2%B0%EC%A0%95%EC%A0%81%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%EC%B2%98%EB%A6%AC%20%E2%80%94%20%EC%9B%8C%ED%84%B0%EB%A7%88%ED%81%AC%EC%99%80%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%ED%83%80%EC%9E%84.md) · [프로세싱 타임](../03_architecture/05_edd/02-03.%EA%B2%B0%EC%A0%95%EC%A0%81%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%EC%B2%98%EB%A6%AC%20%E2%80%94%20%EC%9B%8C%ED%84%B0%EB%A7%88%ED%81%AC%EC%99%80%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%ED%83%80%EC%9E%84.md) | |
| 블룸 필터 · 카운팅 블룸 필터 · 쿠쿠 필터 · 하이퍼로그로그 · 카운트 민 스케치 · 탑K · 퀀타일 추정 | 선택 | [블룸 필터](../03_architecture/book/bytebytego-system-design/08-01.%ED%8A%B8%EC%9C%84%ED%84%B0%20%ED%83%80%EC%9E%84%EB%9D%BC%EC%9D%B8%C2%B7%EA%B5%AC%EA%B8%80%20%EB%8F%85%EC%8A%A4%20%EB%8F%99%EC%8B%9C%20%ED%8E%B8%EC%A7%91%C2%B7%EC%8A%AC%EB%9E%99%20%EC%95%8C%EB%A6%BC%20%ED%8C%90%EC%A0%95%C2%B7%ED%81%AC%EB%A1%A4%EB%9F%AC%20%EC%A4%91%EB%B3%B5%20%EC%A0%9C%EA%B1%B0%EB%8A%94%20%ED%8C%AC%EC%95%84%EC%9B%83%C2%B7OT%C2%B7%ED%9D%90%EB%A6%84%EB%8F%84%C2%B7%EB%B8%94%EB%A3%B8%20%ED%95%84%ED%84%B0%EB%A1%9C%20%ED%91%BC%EB%8B%A4.md) · [퀀타일 추정](../02_os/book/npg_network-programming-with-go/13-03.%EB%A9%94%ED%8A%B8%EB%A6%AD%EC%9D%80%20%EC%B9%B4%EC%9A%B4%ED%84%B0%C2%B7%EA%B2%8C%EC%9D%B4%EC%A7%80%C2%B7%ED%9E%88%EC%8A%A4%ED%86%A0%EA%B7%B8%EB%9E%A8%EC%9C%BC%EB%A1%9C%20%EC%84%9C%EB%B2%84%EB%A5%BC%20%EC%9E%AC%EA%B3%A0%20Prometheus%20%EA%B0%80%20%EA%B7%B8%20%EA%B0%92%EC%9D%84%20%EA%B8%81%EC%96%B4%20%EA%B0%84%EB%8B%A4.md) | |
| 랭킹 시스템 · 실시간 랭킹 | 선택 | | |
| ETL · ELT | 선택 | [ETL](../05_data/book/designing-data-intensive-applications/01-01.%EC%9A%B4%EC%98%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20vs%20%EB%B6%84%EC%84%9D%20%EC%8B%9C%EC%8A%A4%ED%85%9C.md) | |
| 오프셋 커밋 | 선택 | [오프셋 커밋](../04_messaging/04_BrokerArchitecture/01-05.%EC%98%A4%ED%94%84%EC%85%8B%20%EC%BB%A4%EB%B0%8B%20API.md) | |



## 넣지 않은 것

> 다른 문서가 정본이거나 이 로드맵의 축과 다른 것들입니다.

| 대상 | 이유 |
|---|---|
| SQL 문법 · MySQL 실행 계획 · 인덱스 튜닝 | 소장 책에 없고, 이 저장소에도 아직 노트가 없습니다 |
| JDBC · 커넥션 풀 · JPA · QueryDSL | 도구를 익히는 축입니다. `05_data/03_persistence` 와 [Spring 로드맵](spring-keywords.md) 4단계가 맡고, 커넥션 풀 고갈은 [JVM 로드맵](jvm-keywords.md) 7단계가 봅니다 |
| `@Transactional` 과 전파 · 롤백 규칙 | [Spring 로드맵](spring-keywords.md) 4단계가 맡습니다. 6단계는 격리 수준까지입니다 |
| DB 덤프 · 로컬 이관 · 마이그레이션 도구 | `05_data/06_operations` 가 맡습니다. 순서를 말할 대상이 아닙니다 |
| Kafka 브로커 설계와 운영 | `04_messaging` 이 정본입니다. 9단계는 로그 기반 브로커의 원리까지입니다 |
| 검색 애플리케이션 만들기 | Elasticsearch in Action 의 절반은 제품을 만드는 쪽입니다. 3단계는 색인 구조만 봅니다 |
