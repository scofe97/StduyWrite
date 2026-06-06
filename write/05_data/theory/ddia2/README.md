---
title: ddia2 — Designing Data-Intensive Applications 2판 정독
tags: [moc, ddia, data-intensive, second-edition, distributed-systems]
status: draft
updated: 2026-06-06
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

> 진척: ✅ = 완료 · ⏳ = 진행 중 · ◻ = 미착수. 본문 장은 원문 수령 시 추가합니다.

| 장 | 문서 | 진척 |
|----|------|------|
| 서문 | [책의 철학과 2판 변경점](00-00.서문%20—%20책의%20철학과%202판%20변경점.md) | ✅ |
| 1장 | [01-01 운영 시스템 vs 분석 시스템](01-01.운영%20시스템%20vs%20분석%20시스템.md) | ✅ |
| 1장 | [01-02 기록 시스템 vs 파생 데이터](01-02.기록%20시스템%20vs%20파생%20데이터.md) | ✅ |
| 1장 | [01-03 클라우드 vs 셀프 호스팅](01-03.클라우드%20vs%20셀프%20호스팅.md) | ✅ |
| 1장 | [01-04 분산 vs 단일 노드](01-04.분산%20vs%20단일%20노드.md) | ✅ |
| 1장 | [01-05 데이터 시스템·법·사회](01-05.데이터%20시스템·법·사회.md) | ✅ |
| 2장 | [02-01 사례 연구 — 소셜 네트워크 홈 타임라인](02-01.사례%20연구%20—%20소셜%20네트워크%20홈%20타임라인.md) | ✅ |
| 2장 | [02-02 성능 — 응답 시간과 처리량](02-02.성능%20—%20응답%20시간과%20처리량.md) | ✅ |
| 2장 | [02-03 신뢰성과 내결함성](02-03.신뢰성과%20내결함성.md) | ✅ |
| 2장 | [02-04 확장성](02-04.확장성.md) | ✅ |
| 2장 | [02-05 유지보수성](02-05.유지보수성.md) | ✅ |
| 3장+ | (원문 수령 시 장별 추가) | ◻ |

> 1장 — Trade-Offs in Data Systems Architecture. 다섯 트레이드오프 축(운영/분석 · 기록/파생 · 클라우드/셀프 · 분산/단일 · 비즈니스/사용자 권리)을 절별로 나눠 정독했습니다. 종합은 [01-05 §4](01-05.데이터%20시스템·법·사회.md).
>
> 2장 — Defining Nonfunctional Requirements. 소셜 타임라인 사례로 시작해 네 비기능 요구사항(성능 · 신뢰성 · 확장성 · 유지보수성)을 절별로 정독했습니다. 종합은 [02-05 §4](02-05.유지보수성.md).
