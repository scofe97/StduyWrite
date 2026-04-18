# Claude Code 자율 코딩 - Superpowers

**출처**: [LinkedIn - HaYeJin Kang](https://www.linkedin.com/posts/h4y3j1n_claude-code%EB%A1%9C-2%EC%8B%9C%EA%B0%84-%EB%8F%99%EC%95%88-%EC%9E%90%EC%9C%A8-%EC%BD%94%EB%94%A9-%EC%8B%9C%EC%BC%9C%EB%B3%B8-%EC%A0%81-%EC%9E%88%EC%9C%BC%EC%84%B8%EC%9A%94%EB%B3%B4%ED%86%B5%EC%9D%80-activity-7419880228942004225-TsnO)

---

## 문제점

Claude Code로 2시간 동안 자율 코딩 시켜본 경험에서 발견한 일반적인 한계:

- 10분만 지나도 엉뚱한 방향으로 감
- 테스트 없이 코드만 쏟아냄
- 같은 버그를 반복

---

## 솔루션: Superpowers

AI 에이전트에게 **시니어 개발자 워크플로우**를 적용하는 스킬 라이브러리

### 핵심 개념: Subagent-Driven Development

- 각 태스크마다 **새로운 에이전트** 투입
- 완료 후 **2단계 코드 리뷰** 필수 후 진행

### 대상

- 비개발자로서 AI 코딩 결과가 부족했던 사람
- TDD(테스트 주도 개발) 없는 코드 생성에 불만 있는 사용자

### 설치 방법

Claude Code에서 2줄의 플러그인 임포트로 가능

---

## 핵심 포인트

1. **장시간 자율 실행의 문제**: AI가 방향을 잃거나 반복적인 실수
2. **해결책**: 구조화된 워크플로우와 서브에이전트 활용
3. **코드 리뷰 필수**: 자동화된 품질 검증 단계 포함
