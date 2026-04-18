# Project Name

## Overview
[프로젝트의 목적과 핵심 기능을 1-2문장으로 설명]

## Tech Stack
- **Language**: [언어, 예: TypeScript 5.x]
- **Framework**: [프레임워크, 예: React 18, Node.js 20]
- **Database**: [데이터베이스, 예: PostgreSQL 15]
- **ORM**: [ORM, 예: Prisma]
- **Testing**: [테스트 도구, 예: Jest, Cypress]

## Project Structure
```
src/
├── components/     # UI 컴포넌트
├── services/       # 비즈니스 로직
├── hooks/          # 커스텀 훅
├── utils/          # 유틸리티 함수
├── types/          # 타입 정의
└── tests/          # 테스트 파일
```

## Code Style

### Naming Convention
- **파일명**: kebab-case (`user-service.ts`)
- **컴포넌트**: PascalCase (`UserProfile.tsx`)
- **함수/변수**: camelCase (`getUserById`)
- **상수**: UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`)

### General Rules
- 함수형 컴포넌트 선호
- 명확한 타입 정의
- 의미 있는 변수명

## Rules

### MUST (필수)
- 모든 함수에 타입 정의
- 커밋 전 린트/테스트 통과
- PR 전 코드 리뷰

### MUST NOT (금지)
- `any` 타입 사용 금지
- `console.log` 커밋 금지
- 하드코딩된 시크릿 금지

### SHOULD (권장)
- 작은 함수로 분리
- 주석보다 명확한 코드
- 재사용 가능한 컴포넌트

## Commit Convention
```
<type>: <subject>

Types:
- feat: 새 기능
- fix: 버그 수정
- refactor: 리팩토링
- docs: 문서
- test: 테스트
- chore: 빌드/설정
```

## Testing
- 단위 테스트: `npm test`
- E2E 테스트: `npm run e2e`
- 커버리지 목표: 80%

## Development
```bash
# 설치
npm install

# 개발 서버
npm run dev

# 빌드
npm run build

# 테스트
npm test
```
