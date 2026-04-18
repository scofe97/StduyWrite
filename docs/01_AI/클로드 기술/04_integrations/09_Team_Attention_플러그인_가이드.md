# Team Attention - Claude Code 플러그인 저장소 종합 가이드

> 출처: https://discuss.pytorch.kr/t/claude-code-200-team-attention/8782

---

## 프로젝트 개요

**plugins-for-claude-natives**는 Team Attention이 개발한 9개의 오픈소스 플러그인 모음입니다.

**핵심 철학**: "코딩 외적인 맥락과 워크플로우를 보강" - 단순 코드 생성을 넘어 개발자의 실무 환경 지원

---

## 핵심 플러그인 9개

| 플러그인 | 기능 | 활용 시나리오 |
|---------|------|--------------|
| **Agent Council** | 여러 AI 에이전트(Gemini, GPT 등)의 의견을 수집하여 종합된 결론 도출 | 복잡한 의사결정, 다양한 관점 필요 시 |
| **Clarify** | 모호한 요구사항을 구체적 명세서로 변환하는 "AI 프로덕트 매니저" | 요구사항 분석, 기획 단계 |
| **Dev** | Reddit, Hacker News 등 개발자 커뮤니티의 실제 여론 분석 | 기술 트렌드 파악, 라이브러리 선택 |
| **Interactive Review** | 웹 UI에서 계획서를 검토하고 승인/반려 가능 | 코드 리뷰, 계획 승인 프로세스 |
| **Say Summary** | 한국어/영어 음성으로 답변 핵심 요약 브리핑 | 멀티태스킹, 이동 중 확인 (macOS 전용) |
| **YouTube Digest** | 영상 자막 추출, 번역, 요약, 퀴즈 생성 | 기술 영상 학습, 컨텐츠 요약 |
| **Google Calendar** | 다중 계정 일정 관리 및 충돌 감지 | 스케줄 관리, 미팅 조율 |
| **KakaoTalk** | 카카오톡 메시지 읽기/전송 | 업무 커뮤니케이션 (macOS, Accessibility API) |
| **Session Wrap** | 작업 세션 히스토리 분석 및 회고 | 작업 리뷰, 생산성 분석 |

---

## 설치 방법

```bash
# 마켓플레이스에서 추가
/plugin marketplace add team-attention/plugins-for-claude-natives

# 개별 플러그인 설치
/plugin install <plugin-name>

# 예시
/plugin install agent-council
/plugin install clarify
/plugin install youtube-digest
```

---

## 주요 플러그인 상세

### 1. Agent Council - 다중 AI 의견 수집

여러 AI 에이전트의 의견을 종합하여 더 나은 결론을 도출합니다.

**활용 예시**:
- 아키텍처 결정 시 다양한 관점 확보
- 코드 리뷰에서 다양한 스타일 의견 수집
- 기술 선택 시 장단점 종합 분석

### 2. Clarify - AI 프로덕트 매니저

모호한 요구사항을 구체적 명세서로 변환합니다.

**변환 예시**:
```
입력: "로그인 기능 만들어줘"

출력:
- 인증 방식: JWT / OAuth / Session
- 비밀번호 정책: 최소 8자, 특수문자 포함
- 로그인 실패 처리: 5회 실패 시 10분 잠금
- 세션 유지 시간: 24시간
- 자동 로그인 기능: 체크박스 옵션
```

### 3. YouTube Digest - 영상 학습 도우미

```
기능:
- 자막 추출 및 번역
- 핵심 내용 요약
- 학습용 퀴즈 자동 생성
- 타임스탬프 기반 정리
```

---

## Team Attention 소개

### 핵심 철학

> **"Attention is all you need"**
> - 불필요한 노이즈 제거
> - 본질적 문제 해결에 집중

### 주요 활동

- **스탠포드 CS146S** (Modern Software Developer) 한국어 에디션 운영
- **AI 빌더 Meetup** 정기 개최
- **오픈소스 도구** 개발 및 배포

### 라이선스

**MIT License** - 자유로운 사용, 수정, 배포 가능

### 링크

- 공식 홈페이지: [team-attention.com](https://team-attention.com)
- GitHub: [plugins-for-claude-natives](https://github.com/team-attention/plugins-for-claude-natives)

---

## 실무 활용 팁

### 추천 조합

1. **기획 단계**: Clarify + Agent Council
   - 요구사항 구체화 → 다양한 관점 검토

2. **개발 단계**: Dev + Interactive Review
   - 커뮤니티 의견 참고 → 코드 리뷰 자동화

3. **학습 단계**: YouTube Digest + Session Wrap
   - 기술 영상 학습 → 세션 회고

### 주의사항

- macOS 전용 플러그인: Say Summary, KakaoTalk
- Accessibility API 권한 필요: KakaoTalk
- API 키 설정 필요: Google Calendar, YouTube Digest

---

## 핵심 요약

| 항목 | 내용 |
|------|------|
| **프로젝트명** | plugins-for-claude-natives |
| **개발팀** | Team Attention |
| **플러그인 수** | 9개 |
| **라이선스** | MIT |
| **핵심 가치** | 코딩 외 워크플로우 보강 |
