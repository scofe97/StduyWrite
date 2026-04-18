# Ch07. Promtail to Alloy Migration - 점검 질문

## Q1. Promtail의 EOL 타임라인을 정확한 날짜와 함께 설명하라.

**핵심 포인트**:
- 2025-02-13 deprecated
- 2026-02-28 LTS 종료
- 2026-03-02 EOL

## Q2. Promtail -> Alloy migration이 단순 치환이 아닌 이유는 무엇인가?

**핵심 포인트**:
- 로그 전용 agent에서 통합 수집기로의 전환
- 운영 모델과 문서 기준이 함께 바뀜

## Q3. migration 전에 가장 먼저 해야 할 inventory는 무엇인가?

**핵심 포인트**:
- discovery 방식
- relabel 규칙
- drop/filter 정책
- tenant 분기

## Q4. 변환 도구를 돌린 뒤에도 수동 검토가 필요한 이유는 무엇인가?

**핵심 포인트**:
- 라벨 비용 문제
- 운영 검색 UX 문제
- 기존 정책 누락 가능성

## Q5. 단계적 cutover를 해야 하는 이유는 무엇인가?

**핵심 포인트**:
- 수집량 비교 가능
- 장애 범위 축소
- rollback 용이

## Q6. migration 완료를 어떤 기준으로 판단할 수 있는가?

**핵심 포인트**:
- 수집량 정상
- 라벨 폭발 없음
- 운영자 탐색 흐름 유지 또는 개선
- 보안/지원 리스크 제거
