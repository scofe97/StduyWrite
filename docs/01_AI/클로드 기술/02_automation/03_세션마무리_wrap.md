# /wrap 명령어 - 세션 마무리 자동화

**출처**: [LinkedIn - 정구봉(Goobong Jeong)](https://www.linkedin.com/posts/gb-jeong_%EC%A0%80%EB%8A%94-claude-code-%EC%84%B8%EC%85%98%EC%9D%B4-%EB%81%9D%EB%82%A0-%EB%95%8C%EB%A7%88%EB%8B%A4-wrap-%EC%9D%B4-%EB%AA%85%EB%A0%B9%EC%96%B4%EB%A5%BC-activity-7415878861919379456-h0-g)

---

## 개념

Claude Code 세션 종료 시 `/wrap` 명령어를 입력하여 세션 정리 프로세스를 자동화

**처리 항목**:
- 문서 업데이트
- 미완성 작업 추적
- 자동화 기회 발굴

---

## 5가지 에이전트

| 에이전트 | 역할 |
|----------|------|
| **doc-updater** | CLAUDE.md와 context.md에 추가할 내용 제안 |
| **automation-scout** | 반복 패턴을 skill/command/agent로 자동화할 기회 탐지 |
| **learning-extractor** | 배운 것, 실수한 것, 새 발견사항 추출 |
| **followup-suggester** | 미완성 작업 및 다음 세션 우선순위 정리 |
| **duplicate-checker** | 제안 내용의 중복 검증 |

---

## 작동 방식

### Phase 1: 병렬 분석
4개 에이전트가 독립적으로 분석 수행

### Phase 2: 검증
duplicate-checker가 결과 검증 및 "이미 존재" 항목 필터링

### 사용자 선택
- 커밋
- 문서 업데이트
- 자동화 생성

---

## 주요 이점

1. **CLAUDE.md 자연 축적**: 세션 마무리 습관화
2. **자동화 아이디어 누락 방지**: 반복 패턴 자동 감지
3. **심리적 부담 감소**: "다음에 뭐 해야 하더라?" 고민 해소

---

## 설치

**GitHub**: `plugins-for-claude-natives` 저장소의 `session-wrap` 플러그인

---

## 핵심 포인트

세션을 그냥 끝내지 말고, `/wrap`으로 마무리하면:
- 오늘 배운 것이 문서로 남음
- 다음 세션 우선순위가 명확해짐
- 반복 작업이 자동화 후보로 등록됨
