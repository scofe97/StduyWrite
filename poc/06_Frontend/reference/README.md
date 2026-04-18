# Frontend 학습 가이드

## 개요

프론트엔드 개발의 핵심 개념부터 실무 적용까지 체계적으로 정리한 학습 문서 모음이다.
면접 준비와 실무 참조를 위해 구조화된 형태로 작성되었다.

---

## 학습 로드맵

### 1단계: 기초 (01-fundamentals)
JavaScript와 TypeScript의 핵심 개념을 이해한다.

```
javascript-core.md → typescript-basics.md → browser-rendering.md
```

### 2단계: 디자인 패턴 (02-design-patterns)
소프트웨어 설계의 근본 원리를 학습한다.

```
00-introduction.md → 01-creational.md → 02-structural.md → 03-behavioral.md
                  → 04-async-patterns.md → 05-module-systems.md
```

### 3단계: 아키텍처 (03-architecture)
애플리케이션 구조 설계 패턴을 이해한다.

```
mvc-mvp-mvvm.md → component-architecture.md → state-management.md
```

### 4단계: React 핵심 (04-react)
React의 핵심 개념과 고급 패턴을 학습한다.

```
01-core-concepts.md → 02-hooks-deep-dive.md → 03-patterns.md
                   → 04-server-components.md → 05-performance.md → 06-testing.md
```

### 5단계: React 생태계 (05-ecosystem)
Next.js와 주요 라이브러리 활용법을 학습한다.

```
nextjs-fundamentals.md → data-fetching.md → forms.md
```

### 6단계: UI 개발 (06-ui-development)
스타일링과 UI 컴포넌트 라이브러리 활용법을 학습한다.

```
styling-approaches.md → shadcn-ui/
```

### 7단계: 개발 도구 (07-tooling)
개발 환경 설정과 문제 해결 방법을 익힌다.

```
vite-configuration.md → code-quality.md → yarn-troubleshooting.md
```

### 8단계: 실무 적용 (08-best-practices)
보안, 접근성, 성능 등 실무 필수 지식을 습득한다.

```
web-security.md → accessibility.md → performance-metrics.md
```

### 9단계: E2E 테스트 (09-testing)
Playwright를 활용한 E2E 테스트 전략을 학습한다.

```
01_Quick_Setup_Refresher.md → 02_Advanced_Selectors_Dynamic_Content.md
→ 03_Browser_Agnostic_Testing.md → 04_AI_Powered_Test_Generation.md
→ 05_Test_Parallelization_Performance.md
```

---

## 전체 목차

### 01-fundamentals/ (JavaScript/TypeScript 기초)
| 문서 | 핵심 내용 |
|------|----------|
| [javascript-core.md](./01-fundamentals/javascript-core.md) | 클로저, 프로토타입, this, 실행 컨텍스트, 이벤트 루프 |
| [typescript-basics.md](./01-fundamentals/typescript-basics.md) | 타입 시스템, 제네릭, 유틸리티 타입, 타입 가드 |
| [browser-rendering.md](./01-fundamentals/browser-rendering.md) | Critical Rendering Path, Reflow/Repaint, Compositing |

### 02-design-patterns/ (디자인 패턴)
| 문서 | 핵심 내용 |
|------|----------|
| [00-introduction.md](./02-design-patterns/00-introduction.md) | 디자인 패턴 개론, 안티패턴, 패턴 적용 원칙 |
| [01-creational.md](./02-design-patterns/01-creational.md) | Singleton, Factory, Abstract Factory, Builder, Prototype |
| [02-structural.md](./02-design-patterns/02-structural.md) | Adapter, Decorator, Facade, Proxy, Composite |
| [03-behavioral.md](./02-design-patterns/03-behavioral.md) | Observer, Mediator, Command, Strategy, State |
| [04-async-patterns.md](./02-design-patterns/04-async-patterns.md) | Promise 패턴, Async/Await 패턴, 에러 처리 |
| [05-module-systems.md](./02-design-patterns/05-module-systems.md) | AMD, CommonJS, UMD, ES Modules, 네임스페이싱 |

### 03-architecture/ (아키텍처 패턴)
| 문서 | 핵심 내용 |
|------|----------|
| [mvc-mvp-mvvm.md](./03-architecture/mvc-mvp-mvvm.md) | MVC, MVP, MVVM 패턴 비교 및 적용 |
| [component-architecture.md](./03-architecture/component-architecture.md) | 컴포넌트 설계 원칙, 재사용 가능한 구조 |
| [state-management.md](./03-architecture/state-management.md) | 상태 관리 전략, Context API, 외부 라이브러리 |

### 04-react/ (React 핵심)
| 문서 | 핵심 내용 |
|------|----------|
| [01-core-concepts.md](./04-react/01-core-concepts.md) | JSX, 컴포넌트, Props, 이벤트 처리 |
| [02-hooks-deep-dive.md](./04-react/02-hooks-deep-dive.md) | useState, useEffect, useRef, 커스텀 훅 |
| [03-patterns.md](./04-react/03-patterns.md) | HOC, Render Props, Compound Components |
| [04-server-components.md](./04-react/04-server-components.md) | RSC, Server Actions, 데이터 페칭 전략 |
| [05-performance.md](./04-react/05-performance.md) | 메모이제이션, 코드 스플리팅, 렌더링 최적화 |
| [06-testing.md](./04-react/06-testing.md) | Jest, React Testing Library, 테스트 전략 |

### 05-ecosystem/ (React 생태계)
| 문서 | 핵심 내용 |
|------|----------|
| [nextjs-fundamentals.md](./05-ecosystem/nextjs-fundamentals.md) | App Router, 라우팅, 레이아웃, 메타데이터 |
| [data-fetching.md](./05-ecosystem/data-fetching.md) | TanStack Query, SWR, 캐싱 전략 |
| [forms.md](./05-ecosystem/forms.md) | React Hook Form, Zod, 폼 유효성 검사 |

### 06-ui-development/ (UI 개발)
| 문서 | 핵심 내용 |
|------|----------|
| [styling-approaches.md](./06-ui-development/styling-approaches.md) | CSS Modules, Tailwind CSS, CSS-in-JS |
| [shadcn-ui/](./06-ui-development/shadcn-ui/) | shadcn/ui 컴포넌트 가이드 (9개 문서) |

### 07-tooling/ (개발 도구)
| 문서 | 핵심 내용 |
|------|----------|
| [vite-configuration.md](./07-tooling/vite-configuration.md) | Vite 설정, 플러그인, HMR, 빌드 최적화 |
| [code-quality.md](./07-tooling/code-quality.md) | ESLint, Prettier, Husky, lint-staged |
| [yarn-troubleshooting.md](./07-tooling/yarn-troubleshooting.md) | YN0018 체크섬 오류 등 문제 해결 |

### 08-best-practices/ (실무 적용)
| 문서 | 핵심 내용 |
|------|----------|
| [web-security.md](./08-best-practices/web-security.md) | XSS, CSRF, CORS, CSP, 인증/인가 |
| [accessibility.md](./08-best-practices/accessibility.md) | WCAG 2.1, ARIA, 키보드 내비게이션 |
| [performance-metrics.md](./08-best-practices/performance-metrics.md) | Core Web Vitals (LCP, FID, CLS) |

### 09-testing/ (E2E 테스트)
| 문서 | 핵심 내용 |
|------|----------|
| [01_Quick_Setup_Refresher.md](./09-testing/01_Quick_Setup_Refresher.md) | Playwright 설치, 기본 설정, 첫 테스트 |
| [02_Advanced_Selectors_Dynamic_Content.md](./09-testing/02_Advanced_Selectors_Dynamic_Content.md) | 고급 셀렉터, 동적 콘텐츠 테스트 |
| [03_Browser_Agnostic_Testing.md](./09-testing/03_Browser_Agnostic_Testing.md) | 크로스 브라우저 테스트 전략 |
| [04_AI_Powered_Test_Generation.md](./09-testing/04_AI_Powered_Test_Generation.md) | AI 기반 테스트 자동 생성 |
| [05_Test_Parallelization_Performance.md](./09-testing/05_Test_Parallelization_Performance.md) | 테스트 병렬화 및 성능 최적화 |

---

## 면접 준비 가이드

### 기초 필수 질문
1. **클로저란 무엇인가?** → [javascript-core.md](./01-fundamentals/javascript-core.md)
2. **이벤트 루프의 동작 원리는?** → [javascript-core.md](./01-fundamentals/javascript-core.md)
3. **TypeScript의 제네릭을 언제 사용하는가?** → [typescript-basics.md](./01-fundamentals/typescript-basics.md)

### React 필수 질문
1. **Virtual DOM의 동작 원리는?** → [01-core-concepts.md](./04-react/01-core-concepts.md)
2. **useEffect와 useLayoutEffect의 차이는?** → [02-hooks-deep-dive.md](./04-react/02-hooks-deep-dive.md)
3. **React Server Components란?** → [04-server-components.md](./04-react/04-server-components.md)

### 아키텍처 필수 질문
1. **MVC와 MVVM의 차이는?** → [mvc-mvp-mvvm.md](./03-architecture/mvc-mvp-mvvm.md)
2. **상태 관리 라이브러리 선택 기준은?** → [state-management.md](./03-architecture/state-management.md)
3. **컴포넌트 재사용성을 높이는 방법은?** → [component-architecture.md](./03-architecture/component-architecture.md)

### 성능/보안 필수 질문
1. **XSS 공격을 방어하는 방법은?** → [web-security.md](./08-best-practices/web-security.md)
2. **Core Web Vitals이란?** → [performance-metrics.md](./08-best-practices/performance-metrics.md)
3. **React 성능 최적화 기법은?** → [05-performance.md](./04-react/05-performance.md)

---

## 문서 작성 규칙

### 필수 섹션
모든 문서는 다음 구조를 따른다:

1. **개요**: 정의, 목적, 핵심 요약
2. **핵심 개념**: 기술적 정의, 동작 원리, 사용 시점
3. **구현 패턴**: 코드 예제와 설명
4. **트레이드오프**: 장단점 비교
5. **실무 적용**: 실제 시나리오와 해결 방법
6. **면접 포인트**: 예상 질문과 핵심 답변

### 어휘 기준
- 구어체 금지 (~하면 됩니다, ~해봅시다)
- 모호한 표현 금지 (보통, 일반적으로, 간단하게)
- 정의형 표현 사용: "X는 Y를 위한 Z이다"
- 비교형 표현 사용: "A와 달리 B는 ~한 특성을 가진다"

---

## 관련 실습

- [poc/06_Frontend](../): 프론트엔드 실습 코드
  - `01-react-hook-form/`: React Hook Form 실습
  - `02-tanstack-query/`: TanStack Query 실습
  - `03-zustand/`: Zustand 상태관리 실습
  - `04-shadcn-patterns/`: shadcn/ui 패턴 실습
  - `05-vitest/`: Vitest 테스트 실습
  - `06-typescript-patterns/`: TypeScript 패턴 실습
  - `07-demo/`: shadcn/ui 디자인 패턴 레퍼런스 앱
  - `08-websocket/`: WebSocket 실습
  - `09-sse/`: SSE 실습
  - `10-playwright/`: Playwright E2E 테스트 실습

---

## 참고 자료

- [React 공식 문서](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)
- [MDN Web Docs](https://developer.mozilla.org)
- [web.dev](https://web.dev)
- [Learning JavaScript Design Patterns](https://www.patterns.dev)
