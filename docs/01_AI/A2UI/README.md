# A2UI 학습 가이드

> **A2UI (Agent to UI)**: AI 에이전트가 안전하게 풍부한 UI를 생성하는 프로토콜

---

## 📚 목차

| 순서 | 문서 | 내용 | 난이도 |
|------|------|------|--------|
| 1 | [소개](./01-introduction.md) | A2UI 개념, 필요성, 대상 사용자 | ⭐ |
| 2 | [핵심 개념](./02-core-concepts.md) | 데이터 흐름, 컴포넌트, 데이터 바인딩 | ⭐⭐ |
| 3 | [빠른 시작](./03-quickstart.md) | 5분 데모 실행, 환경 설정 | ⭐ |
| 4 | [스펙 정리](./04-specification.md) | v0.8 프로토콜 상세 | ⭐⭐⭐ |
| 5 | [컴포넌트 레퍼런스](./05-components.md) | 모든 컴포넌트 사용법 | ⭐⭐ |
| 6 | [실제 사용 시나리오](./06-practical-scenarios.md) | 프로덕션 적용 가이드 | ⭐⭐⭐ |

---

## 🎯 학습 목표

이 가이드를 완료하면 다음을 할 수 있습니다:

- ✅ A2UI 프로토콜의 목적과 장점 설명
- ✅ 핵심 개념 (스트리밍, 컴포넌트, 데이터 바인딩) 이해
- ✅ A2UI 데모 앱 실행 및 수정
- ✅ A2UI JSON 메시지 직접 작성
- ✅ 실제 프로젝트에 A2UI 적용

---

## 🚀 빠른 시작

### 1. 저장소 클론
```bash
git clone https://github.com/google/a2ui.git
cd a2ui
```

### 2. API 키 설정
```bash
export GEMINI_API_KEY="your_key"
```

### 3. 데모 실행
```bash
cd samples/client/lit
npm install
npm run demo:all
```

→ `http://localhost:5173` 에서 확인

---

## 📖 추천 학습 순서

### Week 1: 기초
- 📖 01-introduction.md 읽기
- 📖 02-core-concepts.md 읽기
- 🔧 03-quickstart.md 실습

### Week 2: 심화
- 📖 04-specification.md 읽기
- 📖 05-components.md 읽기
- 🔧 컴포넌트 갤러리 데모 실행

### Week 3: 실전
- 📖 06-practical-scenarios.md 읽기
- 🔧 To-Do 앱 구현
- 🔧 간단한 에이전트 개발

---

## 🔗 참고 자료

- [A2UI 공식 사이트](https://a2ui.org/)
- [GitHub 저장소](https://github.com/google/A2UI)
- [A2UI Composer](https://a2ui.org/composer/)
- [Google AI Studio](https://aistudio.google.com/apikey)

---

## 📝 학습 체크리스트

- [ ] A2UI 개념 이해
- [ ] 데모 앱 실행
- [ ] JSON 메시지 구조 파악
- [ ] 컴포넌트 사용법 숙지
- [ ] 실습 프로젝트 완성

---

**Made with 💙 for A2UI learners**
