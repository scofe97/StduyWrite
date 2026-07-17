---
title: ddia2 — Designing Data-Intensive Applications 2판 정독
tags: [moc, ddia, data-intensive, second-edition, distributed-systems]
status: final
updated: 2026-06-09
---


# ddia2 — 《Designing Data-Intensive Applications, 2판》 정독
---
> Martin Kleppmann & Chris Riccomini 의 2판을 장별로 정독한 노트입니다. 장 번호가 바뀐 별개 판본이라 1판 요약([상위 theory](../README.md))과 분리해, 합니다체 + 핵심 요약 SVG + Mermaid 로 쌓습니다.



## 책 메타

| 항목 | 내용 |
|------|------|
| 제목 | Designing Data-Intensive Applications, Second Edition |
| 저자 | Martin Kleppmann · Chris Riccomini |
| 출판사 | O'Reilly |
| 1판 | 2017 |
| 2판 핵심 변화 | AI/ML 데이터 시스템(벡터 인덱스·DataFrame·배치) · 클라우드 네이티브(오브젝트 스토어) 전면 반영 |
| 2판 신규 | sync engine · durable execution · 형식 검증 · GraphQL · GDPR |
| 2판 제거 | MapReduce 폐기 → 배치 처리 장 재작성 |
| 구조 | 장 번호 변경 · 10장(일관성·합의) 거의 재작성 · 1판 대비 ~60쪽 증가 |
| 참조 모음 | https://github.com/ept/ddia2-references |



## 장별 정독

> 진척: ✅ = 완료 · ⏳ = 진행 중 · ◻ = 미착수. 서문·용어집과 1~14장 전 장 정독을 마쳤습니다.

| 장 | 문서 | 진척 |
|----|------|------|
| 서문 | [책의 철학과 2판 변경점](00-00.%EC%84%9C%EB%AC%B8%20%E2%80%94%20%EC%B1%85%EC%9D%98%20%EC%B2%A0%ED%95%99%EA%B3%BC%202%ED%8C%90%20%EB%B3%80%EA%B2%BD%EC%A0%90.md) | ✅ |
| 용어집 | [DDIA 2판 핵심 용어 50선](00-01.%EC%9A%A9%EC%96%B4%EC%A7%91%20%E2%80%94%20DDIA%202%ED%8C%90%20%ED%95%B5%EC%8B%AC%20%EC%9A%A9%EC%96%B4%2050%EC%84%A0.md) | ✅ |
| 1장 | [01-01 운영 시스템 vs 분석 시스템](01-01.%EC%9A%B4%EC%98%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20vs%20%EB%B6%84%EC%84%9D%20%EC%8B%9C%EC%8A%A4%ED%85%9C.md) | ✅ |
| 1장 | [01-02 기록 시스템 vs 파생 데이터](01-02.%EA%B8%B0%EB%A1%9D%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20vs%20%ED%8C%8C%EC%83%9D%20%EB%8D%B0%EC%9D%B4%ED%84%B0.md) | ✅ |
| 1장 | [01-03 클라우드 vs 셀프 호스팅](01-03.%ED%81%B4%EB%9D%BC%EC%9A%B0%EB%93%9C%20vs%20%EC%85%80%ED%94%84%20%ED%98%B8%EC%8A%A4%ED%8C%85.md) | ✅ |
| 1장 | [01-04 분산 vs 단일 노드](01-04.%EB%B6%84%EC%82%B0%20vs%20%EB%8B%A8%EC%9D%BC%20%EB%85%B8%EB%93%9C.md) | ✅ |
| 1장 | [01-05 데이터 시스템·법·사회](01-05.%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%C2%B7%EB%B2%95%C2%B7%EC%82%AC%ED%9A%8C.md) | ✅ |
| 2장 | [02-01 사례 연구 — 소셜 네트워크 홈 타임라인](02-01.%EC%82%AC%EB%A1%80%20%EC%97%B0%EA%B5%AC%20%E2%80%94%20%EC%86%8C%EC%85%9C%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%ED%99%88%20%ED%83%80%EC%9E%84%EB%9D%BC%EC%9D%B8.md) | ✅ |
| 2장 | [02-02 성능 — 응답 시간과 처리량](02-02.%EC%84%B1%EB%8A%A5%20%E2%80%94%20%EC%9D%91%EB%8B%B5%20%EC%8B%9C%EA%B0%84%EA%B3%BC%20%EC%B2%98%EB%A6%AC%EB%9F%89.md) | ✅ |
| 2장 | [02-03 신뢰성과 내결함성](02-03.%EC%8B%A0%EB%A2%B0%EC%84%B1%EA%B3%BC%20%EB%82%B4%EA%B2%B0%ED%95%A8%EC%84%B1.md) | ✅ |
| 2장 | [02-04 확장성](02-04.%ED%99%95%EC%9E%A5%EC%84%B1.md) | ✅ |
| 2장 | [02-05 유지보수성](02-05.%EC%9C%A0%EC%A7%80%EB%B3%B4%EC%88%98%EC%84%B1.md) | ✅ |
| 3장 | [03-01 관계형 vs 문서 모델](03-01.%EA%B4%80%EA%B3%84%ED%98%95%20vs%20%EB%AC%B8%EC%84%9C%20%EB%AA%A8%EB%8D%B8.md) | ✅ |
| 3장 | [03-02 정규화·비정규화·조인](03-02.%EC%A0%95%EA%B7%9C%ED%99%94%C2%B7%EB%B9%84%EC%A0%95%EA%B7%9C%ED%99%94%C2%B7%EC%A1%B0%EC%9D%B8.md) | ✅ |
| 3장 | [03-03 분석용 스키마 — 별·눈송이·OBT](03-03.%EB%B6%84%EC%84%9D%EC%9A%A9%20%EC%8A%A4%ED%82%A4%EB%A7%88%20%E2%80%94%20%EB%B3%84%C2%B7%EB%88%88%EC%86%A1%EC%9D%B4%C2%B7OBT.md) | ✅ |
| 3장 | [03-04 모델 선택과 스키마 유연성](03-04.%EB%AA%A8%EB%8D%B8%20%EC%84%A0%ED%83%9D%EA%B3%BC%20%EC%8A%A4%ED%82%A4%EB%A7%88%20%EC%9C%A0%EC%97%B0%EC%84%B1.md) | ✅ |
| 3장 | [03-05 그래프 데이터 모델](03-05.%EA%B7%B8%EB%9E%98%ED%94%84%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%AA%A8%EB%8D%B8.md) | ✅ |
| 3장 | [03-06 이벤트 소싱·CQRS·DataFrame](03-06.%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EC%86%8C%EC%8B%B1%C2%B7CQRS%C2%B7DataFrame.md) | ✅ |
| 4장 | [04-01 OLTP 저장과 인덱스 기초](04-01.OLTP%20%EC%A0%80%EC%9E%A5%EA%B3%BC%20%EC%9D%B8%EB%8D%B1%EC%8A%A4%20%EA%B8%B0%EC%B4%88.md) | ✅ |
| 4장 | [04-02 LSM 저장 엔진](04-02.LSM%20%EC%A0%80%EC%9E%A5%20%EC%97%94%EC%A7%84.md) | ✅ |
| 4장 | [04-03 B-tree와 LSM 비교](04-03.B-tree%EC%99%80%20LSM%20%EB%B9%84%EA%B5%90.md) | ✅ |
| 4장 | [04-04 보조 인덱스와 인메모리 저장](04-04.%EB%B3%B4%EC%A1%B0%20%EC%9D%B8%EB%8D%B1%EC%8A%A4%EC%99%80%20%EC%9D%B8%EB%A9%94%EB%AA%A8%EB%A6%AC%20%EC%A0%80%EC%9E%A5.md) | ✅ |
| 4장 | [04-05 분석용 컬럼 지향 저장](04-05.%EB%B6%84%EC%84%9D%EC%9A%A9%20%EC%BB%AC%EB%9F%BC%20%EC%A7%80%ED%96%A5%20%EC%A0%80%EC%9E%A5.md) | ✅ |
| 4장 | [04-06 다차원·전문·벡터 인덱스](04-06.%EB%8B%A4%EC%B0%A8%EC%9B%90%C2%B7%EC%A0%84%EB%AC%B8%C2%B7%EB%B2%A1%ED%84%B0%20%EC%9D%B8%EB%8D%B1%EC%8A%A4.md) | ✅ |
| 5장 | [05-01 인코딩과 호환성 기초](05-01.%EC%9D%B8%EC%BD%94%EB%94%A9%EA%B3%BC%20%ED%98%B8%ED%99%98%EC%84%B1%20%EA%B8%B0%EC%B4%88.md) | ✅ |
| 5장 | [05-02 JSON·XML·이진 변형](05-02.JSON%C2%B7XML%C2%B7%EC%9D%B4%EC%A7%84%20%EB%B3%80%ED%98%95.md) | ✅ |
| 5장 | [05-03 Protocol Buffers와 Avro](05-03.Protocol%20Buffers%EC%99%80%20Avro.md) | ✅ |
| 5장 | [05-04 데이터플로우 — DB·REST·RPC](05-04.%EB%8D%B0%EC%9D%B4%ED%84%B0%ED%94%8C%EB%A1%9C%EC%9A%B0%20%E2%80%94%20DB%C2%B7REST%C2%B7RPC.md) | ✅ |
| 5장 | [05-05 durable execution과 이벤트 기반 아키텍처](05-05.durable%20execution%EA%B3%BC%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EA%B8%B0%EB%B0%98%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.md) | ✅ |
| 6장 | [06-01 복제 개요와 단일 리더](06-01.%EB%B3%B5%EC%A0%9C%20%EA%B0%9C%EC%9A%94%EC%99%80%20%EB%8B%A8%EC%9D%BC%20%EB%A6%AC%EB%8D%94.md) | ✅ |
| 6장 | [06-02 노드 장애 처리와 복제 로그](06-02.%EB%85%B8%EB%93%9C%20%EC%9E%A5%EC%95%A0%20%EC%B2%98%EB%A6%AC%EC%99%80%20%EB%B3%B5%EC%A0%9C%20%EB%A1%9C%EA%B7%B8.md) | ✅ |
| 6장 | [06-03 복제 지연 문제와 일관성 보장](06-03.%EB%B3%B5%EC%A0%9C%20%EC%A7%80%EC%97%B0%20%EB%AC%B8%EC%A0%9C%EC%99%80%20%EC%9D%BC%EA%B4%80%EC%84%B1%20%EB%B3%B4%EC%9E%A5.md) | ✅ |
| 6장 | [06-04 다중 리더 복제](06-04.%EB%8B%A4%EC%A4%91%20%EB%A6%AC%EB%8D%94%20%EB%B3%B5%EC%A0%9C.md) | ✅ |
| 6장 | [06-05 쓰기 충돌 해소](06-05.%EC%93%B0%EA%B8%B0%20%EC%B6%A9%EB%8F%8C%20%ED%95%B4%EC%86%8C.md) | ✅ |
| 6장 | [06-06 리더리스 복제와 6장 종합](06-06.%EB%A6%AC%EB%8D%94%EB%A6%AC%EC%8A%A4%20%EB%B3%B5%EC%A0%9C%EC%99%80%206%EC%9E%A5%20%EC%A2%85%ED%95%A9.md) | ✅ |
| 7장 | [07-01 샤딩 개요와 키 범위 샤딩](07-01.%EC%83%A4%EB%94%A9%20%EA%B0%9C%EC%9A%94%EC%99%80%20%ED%82%A4%20%EB%B2%94%EC%9C%84%20%EC%83%A4%EB%94%A9.md) | ✅ |
| 7장 | [07-02 해시 샤딩과 일관 해싱](07-02.%ED%95%B4%EC%8B%9C%20%EC%83%A4%EB%94%A9%EA%B3%BC%20%EC%9D%BC%EA%B4%80%20%ED%95%B4%EC%8B%B1.md) | ✅ |
| 7장 | [07-03 요청 라우팅과 리밸런싱](07-03.%EC%9A%94%EC%B2%AD%20%EB%9D%BC%EC%9A%B0%ED%8C%85%EA%B3%BC%20%EB%A6%AC%EB%B0%B8%EB%9F%B0%EC%8B%B1.md) | ✅ |
| 7장 | [07-04 보조 인덱스와 7장 종합](07-04.%EB%B3%B4%EC%A1%B0%20%EC%9D%B8%EB%8D%B1%EC%8A%A4%EC%99%80%207%EC%9E%A5%20%EC%A2%85%ED%95%A9.md) | ✅ |
| 8장 | [08-01 ACID와 트랜잭션 개요](08-01.ACID%EC%99%80%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%20%EA%B0%9C%EC%9A%94.md) | ✅ |
| 8장 | [08-02 약한 격리 수준과 스냅샷 격리](08-02.%EC%95%BD%ED%95%9C%20%EA%B2%A9%EB%A6%AC%20%EC%88%98%EC%A4%80%EA%B3%BC%20%EC%8A%A4%EB%83%85%EC%83%B7%20%EA%B2%A9%EB%A6%AC.md) | ✅ |
| 8장 | [08-03 Write Skew와 직렬화 가능성](08-03.Write%20Skew%EC%99%80%20%EC%A7%81%EB%A0%AC%ED%99%94%20%EA%B0%80%EB%8A%A5%EC%84%B1.md) | ✅ |
| 8장 | [08-04 분산 트랜잭션과 2PC](08-04.%EB%B6%84%EC%82%B0%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%EA%B3%BC%202PC.md) | ✅ |
| 9장 | [09-01 부분 실패와 비신뢰 네트워크](09-01.%EB%B6%80%EB%B6%84%20%EC%8B%A4%ED%8C%A8%EC%99%80%20%EB%B9%84%EC%8B%A0%EB%A2%B0%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC.md) | ✅ |
| 9장 | [09-02 불신뢰 시계](09-02.%EB%B6%88%EC%8B%A0%EB%A2%B0%20%EC%8B%9C%EA%B3%84.md) | ✅ |
| 9장 | [09-03 진실·거짓·시스템 모델](09-03.%EC%A7%84%EC%8B%A4%C2%B7%EA%B1%B0%EC%A7%93%C2%B7%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EB%AA%A8%EB%8D%B8.md) | ✅ |
| 9장 | [09-04 분산 시스템 검증과 9장 종합](09-04.%EB%B6%84%EC%82%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B2%80%EC%A6%9D%EA%B3%BC%209%EC%9E%A5%20%EC%A2%85%ED%95%A9.md) | ✅ |
| 10장 | [10-01 선형성](10-01.%EC%84%A0%ED%98%95%EC%84%B1.md) | ✅ |
| 10장 | [10-02 선형성의 비용과 CAP](10-02.%EC%84%A0%ED%98%95%EC%84%B1%EC%9D%98%20%EB%B9%84%EC%9A%A9%EA%B3%BC%20CAP.md) | ✅ |
| 10장 | [10-03 ID 생성기와 논리 시계](10-03.ID%20%EC%83%9D%EC%84%B1%EA%B8%B0%EC%99%80%20%EB%85%BC%EB%A6%AC%20%EC%8B%9C%EA%B3%84.md) | ✅ |
| 10장 | [10-04 합의와 코디네이션 서비스](10-04.%ED%95%A9%EC%9D%98%EC%99%80%20%EC%BD%94%EB%94%94%EB%84%A4%EC%9D%B4%EC%85%98%20%EC%84%9C%EB%B9%84%EC%8A%A4.md) | ✅ |
| 11장 | [11-01 배치 처리 개요와 Unix 도구](11-01.%EB%B0%B0%EC%B9%98%20%EC%B2%98%EB%A6%AC%20%EA%B0%9C%EC%9A%94%EC%99%80%20Unix%20%EB%8F%84%EA%B5%AC.md) | ✅ |
| 11장 | [11-02 분산 파일시스템과 오브젝트 스토어](11-02.%EB%B6%84%EC%82%B0%20%ED%8C%8C%EC%9D%BC%EC%8B%9C%EC%8A%A4%ED%85%9C%EA%B3%BC%20%EC%98%A4%EB%B8%8C%EC%A0%9D%ED%8A%B8%20%EC%8A%A4%ED%86%A0%EC%96%B4.md) | ✅ |
| 11장 | [11-03 분산 잡 오케스트레이션과 MapReduce](11-03.%EB%B6%84%EC%82%B0%20%EC%9E%A1%20%EC%98%A4%EC%BC%80%EC%8A%A4%ED%8A%B8%EB%A0%88%EC%9D%B4%EC%85%98%EA%B3%BC%20MapReduce.md) | ✅ |
| 11장 | [11-04 데이터플로우 엔진과 배치 활용](11-04.%EB%8D%B0%EC%9D%B4%ED%84%B0%ED%94%8C%EB%A1%9C%EC%9A%B0%20%EC%97%94%EC%A7%84%EA%B3%BC%20%EB%B0%B0%EC%B9%98%20%ED%99%9C%EC%9A%A9.md) | ✅ |
| 12장 | [12-01 스트림 전송 — 메시지 브로커와 로그 기반 브로커](12-01.%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%EC%A0%84%EC%86%A1%20%E2%80%94%20%EB%A9%94%EC%8B%9C%EC%A7%80%20%EB%B8%8C%EB%A1%9C%EC%BB%A4%EC%99%80%20%EB%A1%9C%EA%B7%B8%20%EA%B8%B0%EB%B0%98%20%EB%B8%8C%EB%A1%9C%EC%BB%A4.md) | ✅ |
| 12장 | [12-02 데이터베이스와 스트림](12-02.%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%EC%99%80%20%EC%8A%A4%ED%8A%B8%EB%A6%BC.md) | ✅ |
| 12장 | [12-03 스트림 처리 — CEP·윈도우·조인](12-03.%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%EC%B2%98%EB%A6%AC%20%E2%80%94%20CEP%C2%B7%EC%9C%88%EB%8F%84%EC%9A%B0%C2%B7%EC%A1%B0%EC%9D%B8.md) | ✅ |
| 12장 | [12-04 시간 추론과 내결함성·12장 종합](12-04.%EC%8B%9C%EA%B0%84%20%EC%B6%94%EB%A1%A0%EA%B3%BC%20%EB%82%B4%EA%B2%B0%ED%95%A8%EC%84%B1%C2%B712%EC%9E%A5%20%EC%A2%85%ED%95%A9.md) | ✅ |
| 13장 | [13-01 데이터 통합 — 파생 데이터와 전순서의 한계](13-01.%EB%8D%B0%EC%9D%B4%ED%84%B0%20%ED%86%B5%ED%95%A9%20%E2%80%94%20%ED%8C%8C%EC%83%9D%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%99%80%20%EC%A0%84%EC%88%9C%EC%84%9C%EC%9D%98%20%ED%95%9C%EA%B3%84.md) | ✅ |
| 13장 | [13-02 배치·스트림 통합과 DB 언번들링](13-02.%EB%B0%B0%EC%B9%98%C2%B7%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%ED%86%B5%ED%95%A9%EA%B3%BC%20DB%20%EC%96%B8%EB%B2%88%EB%93%A4%EB%A7%81.md) | ✅ |
| 13장 | [13-03 데이터플로우 중심 애플리케이션 설계](13-03.%EB%8D%B0%EC%9D%B4%ED%84%B0%ED%94%8C%EB%A1%9C%EC%9A%B0%20%EC%A4%91%EC%8B%AC%20%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98%20%EC%84%A4%EA%B3%84.md) | ✅ |
| 13장 | [13-04 정확성과 신뢰·13장 종합](13-04.%EC%A0%95%ED%99%95%EC%84%B1%EA%B3%BC%20%EC%8B%A0%EB%A2%B0%C2%B713%EC%9E%A5%20%EC%A2%85%ED%95%A9.md) | ✅ |
| 14장 | [14-01 예측 분석의 윤리 — 편향·책임·피드백 루프](14-01.%EC%98%88%EC%B8%A1%20%EB%B6%84%EC%84%9D%EC%9D%98%20%EC%9C%A4%EB%A6%AC%20%E2%80%94%20%ED%8E%B8%ED%96%A5%C2%B7%EC%B1%85%EC%9E%84%C2%B7%ED%94%BC%EB%93%9C%EB%B0%B1%20%EB%A3%A8%ED%94%84.md) | ✅ |
| 14장 | [14-02 프라이버시와 감시·동의의 한계](14-02.%ED%94%84%EB%9D%BC%EC%9D%B4%EB%B2%84%EC%8B%9C%EC%99%80%20%EA%B0%90%EC%8B%9C%C2%B7%EB%8F%99%EC%9D%98%EC%9D%98%20%ED%95%9C%EA%B3%84.md) | ✅ |
| 14장 | [14-03 데이터의 권력·산업혁명의 교훈·책 종합](14-03.%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%9D%98%20%EA%B6%8C%EB%A0%A5%C2%B7%EC%82%B0%EC%97%85%ED%98%81%EB%AA%85%EC%9D%98%20%EA%B5%90%ED%9B%88%C2%B7%EC%B1%85%20%EC%A2%85%ED%95%A9.md) | ✅ |

> 1장 — Trade-Offs in Data Systems Architecture. 다섯 트레이드오프 축(운영/분석 · 기록/파생 · 클라우드/셀프 · 분산/단일 · 비즈니스/사용자 권리)을 절별로 나눠 정독했습니다. 종합은 [01-05 §4](01-05.%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%C2%B7%EB%B2%95%C2%B7%EC%82%AC%ED%9A%8C.md).
>
> 2장 — Defining Nonfunctional Requirements. 소셜 타임라인 사례로 시작해 네 비기능 요구사항(성능 · 신뢰성 · 확장성 · 유지보수성)을 절별로 정독했습니다. 종합은 [02-05 §4](02-05.%EC%9C%A0%EC%A7%80%EB%B3%B4%EC%88%98%EC%84%B1.md).
>
> 3장 — Data Models and Query Languages. 관계형·문서·그래프 모델과 분석용 스키마, 이벤트 소싱·CQRS·DataFrame을 여섯 절로 정독했습니다. 종합은 [03-06 §4](03-06.%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EC%86%8C%EC%8B%B1%C2%B7CQRS%C2%B7DataFrame.md).
>
> 4장 — Storage Engines and Indexing. OLTP·LSM·B-tree·보조 인덱스·컬럼 지향·다차원 인덱스를 여섯 절로 정독했습니다. 종합은 [04-06 §4](04-06.%EB%8B%A4%EC%B0%A8%EC%9B%90%C2%B7%EC%A0%84%EB%AC%B8%C2%B7%EB%B2%A1%ED%84%B0%20%EC%9D%B8%EB%8D%B1%EC%8A%A4.md).
>
> 5장 — Encoding and Evolution. 인코딩·호환성·Protocol Buffers·Avro·데이터플로우·durable execution을 다섯 절로 정독했습니다. 종합은 [05-05 §4](05-05.durable%20execution%EA%B3%BC%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EA%B8%B0%EB%B0%98%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.md).
>
> 6장 — Replication. 단일 리더·장애 처리·복제 지연·다중 리더·충돌 해소·리더리스를 여섯 절로 정독했습니다. 종합은 [06-06 §4](06-06.%EB%A6%AC%EB%8D%94%EB%A6%AC%EC%8A%A4%20%EB%B3%B5%EC%A0%9C%EC%99%80%206%EC%9E%A5%20%EC%A2%85%ED%95%A9.md).
>
> 7장 — Sharding. 키 범위·해시·일관 해싱·요청 라우팅·리밸런싱·보조 인덱스를 네 절로 정독했습니다. 종합은 [07-04 §4](07-04.%EB%B3%B4%EC%A1%B0%20%EC%9D%B8%EB%8D%B1%EC%8A%A4%EC%99%80%207%EC%9E%A5%20%EC%A2%85%ED%95%A9.md).
>
> 8장 — Transactions. ACID 속성·단일/다중 객체 트랜잭션·약한 격리(Read committed·스냅샷 격리·MVCC)·갱신 손실·쓰기 스큐·팬텀·직렬화(직렬 실행·2PL·SSI)·분산 원자 커밋·2PC·XA·exactly-once를 네 절로 정독했습니다. 종합은 [08-04 §6](08-04.%EB%B6%84%EC%82%B0%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%EA%B3%BC%202PC.md).
>
> 9장 — The Trouble with Distributed Systems. 부분 실패·비신뢰 네트워크·타임아웃·큐잉 지연(01)·불신뢰 시계 두 종류·NTP 한계·프로세스 포즈(02)·쿼럼 결정·펜싱 토큰·비잔틴 장애·시스템 모델·안전성/활동성(03)·모델 체커·결함 주입·DST·결정론(04)을 네 절로 정독했습니다. 종합은 [09-04 §5](09-04.%EB%B6%84%EC%82%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B2%80%EC%A6%9D%EA%B3%BC%209%EC%9E%A5%20%EC%A2%85%ED%95%A9.md).
>
> 10장 — Consistency and Consensus. 선형성 정의·CAS·직렬화와 차이·구현 방식(01)·파티션 시 CP/AP 선택·CAP 정리 한계·PACELC·성능 하한(02)·분산 ID 4방식·Lamport 클럭·HLC·벡터 클럭·선형화 가능 ID(03)·합의 4속성·FLP 불가능성·동치 문제(CAS/공유 로그/원자 커밋)·Raft/Paxos 에포크·ZooKeeper/etcd(04)를 네 절로 정독했습니다. 종합은 [10-04 §5](10-04.%ED%95%A9%EC%9D%98%EC%99%80%20%EC%BD%94%EB%94%94%EB%84%A4%EC%9D%B4%EC%85%98%20%EC%84%9C%EB%B9%84%EC%8A%A4.md).
>
> 11장 — Batch Processing. 온라인/배치/스트림 구분·Unix 파이프라인·정렬 vs 인메모리 집계·인간 결함 내성(01)·DFS 계층·블록 크기·복제/이레이저 코딩·오브젝트 스토어 특성·저장-연산 분리(02)·잡 오케스트레이터 3요소·스케줄링 NP-hard·MapReduce 4단계·셔플 알고리즘·Sort-Merge Join·워크플로우 스케줄러(03)·데이터플로우 엔진 장점·SQL/DataFrame·ETL·분석·ML·파생 데이터 서빙 패턴(04)을 네 절로 정독했습니다. 종합은 [11-04 §5](11-04.%EB%8D%B0%EC%9D%B4%ED%84%B0%ED%94%8C%EB%A1%9C%EC%9A%B0%20%EC%97%94%EC%A7%84%EA%B3%BC%20%EB%B0%B0%EC%B9%98%20%ED%99%9C%EC%9A%A9.md).
>
> 12장 — Stream Processing. 이벤트·프로듀서/컨슈머·AMQP vs 로그 기반·파티션·오프셋·DLQ·재처리(01)·듀얼 라이트 레이스 컨디션·CDC·아웃박스 패턴·이벤트 소싱 비교·불변성과 크립토 슈레딩(02)·CEP·스트림 분석·IVM·윈도우 4유형·스트림 조인 3종·시간 의존성(03)·이벤트/처리 시간·지각 이벤트 2전략·exactly-once 4전략(마이크로배치·체크포인트·원자적 커밋·멱등성)·배치는 스트림의 특수 케이스(04)를 네 절로 정독했습니다. 종합은 [12-04 §4](12-04.%EC%8B%9C%EA%B0%84%20%EC%B6%94%EB%A1%A0%EA%B3%BC%20%EB%82%B4%EA%B2%B0%ED%95%A8%EC%84%B1%C2%B712%EC%9E%A5%20%EC%A2%85%ED%95%A9.md).
>
> 13장 — A Philosophy of Streaming Systems. 단일 도구 한계·전문 시스템 조합·CDC 파생 데이터 흐름·분산 트랜잭션 vs 로그 기반·전순서 한계 4가지·인과성 포착(01)·재처리로 점진적 진화·람다→카파 아키텍처·DB 언번들링·연합 vs 언번들드 DB(02)·파생 함수로서의 앱 코드·쓰기/읽기 경로 경계·상태를 클라이언트까지 Push·SSE·읽기도 이벤트로(03)·end-to-end 인수·중복 억제·적시성 vs 무결성·exactly-once 4메커니즘·느슨한 제약과 사후 보정·코디네이션 회피·trust-but-verify·감사 가능성(04)를 네 절로 정독했습니다. 종합은 [13-04 §7](13-04.%EC%A0%95%ED%99%95%EC%84%B1%EA%B3%BC%20%EC%8B%A0%EB%A2%B0%C2%B713%EC%9E%A5%20%EC%A2%85%ED%95%A9.md).
>
> 14장 — Doing the Right Thing. 예측 분석의 윤리·알고리즘 감옥·편향 증폭(보호 특성 대리 변수)·책임과 설명 가능성(신용 점수 vs 예측 분석)·자기강화 피드백 루프·시스템 사고(01)·추적이 감시로 바뀌는 지점·"데이터→감시" 사고 실험·동의가 자유롭지 않은 3가지 이유·GDPR 동의 요건·프라이버시=결정권(02)·데이터=자산/권력/독성 자산(새 우라늄)·산업혁명의 교훈(데이터=정보화 시대의 공해)·데이터 최소화 vs 빅데이터 철학·자율 규제·책 전체 종합(03)을 세 절로 정독했습니다. 책 전체 종합은 [14-03 §4](14-03.%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%9D%98%20%EA%B6%8C%EB%A0%A5%C2%B7%EC%82%B0%EC%97%85%ED%98%81%EB%AA%85%EC%9D%98%20%EA%B5%90%ED%9B%88%C2%B7%EC%B1%85%20%EC%A2%85%ED%95%A9.md).
