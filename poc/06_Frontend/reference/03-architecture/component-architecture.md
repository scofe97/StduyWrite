# React 컴포넌트 아키텍처

## 개요

**정의**: React 애플리케이션 구조는 프로젝트 규모와 복잡도에 따라 폴더와 파일을 조직화하는 방식을 결정하는 아키텍처 패턴이다.

**목적**: 유지보수성, 확장성, 팀 협업 효율성을 높이고, 코드 탐색과 변경 영향 범위를 명확하게 한다.

---

## 핵심 개념

### 구조화 접근 방식 비교

| 접근 방식 | 설명 | 적합한 프로젝트 |
|----------|------|----------------|
| **기능별 그룹화** | 모듈/기능/라우트별 폴더 | 도메인 로직이 명확한 프로젝트 |
| **파일 유형별 그룹화** | CSS, 컴포넌트, 테스트별 폴더 | 작은 프로젝트, 표준화 중요 |
| **하이브리드 그룹화** | 위 두 방식의 조합 | 중대형 프로젝트 |

---

## 구현 패턴

### 1. 기능(Feature)별 그룹화

비즈니스 모델이나 애플리케이션 플로우를 반영한다.

```
src/
├── common/
│   ├── Avatar.js
│   ├── Avatar.css
│   └── ErrorUtils.js
├── product/
│   ├── index.js
│   ├── product.css
│   ├── price.js
│   └── product.test.js
└── checkout/
    ├── index.js
    ├── checkout.css
    └── checkout.test.js
```

| 장점 | 단점 |
|------|------|
| 관련 파일이 한 곳에 모임 | 공통 컴포넌트 중복 가능 |
| 변경 영향 범위가 명확 | 재사용 컴포넌트 식별 필요 |
| 기능 단위 개발에 용이 | 모듈 간 의존성 관리 필요 |

---

### 2. 파일 유형별 그룹화

파일 종류에 따라 폴더를 구성한다.

```
src/
├── css/
│   ├── global.css
│   ├── checkout.css
│   └── product.css
├── lib/
│   ├── date.js
│   ├── currency.js
│   └── gtm.js
└── pages/
    ├── product.js
    ├── productlist.js
    └── checkout.js
```

| 장점 | 단점 |
|------|------|
| 프로젝트 간 재사용 가능한 표준 구조 | 기능 변경 시 여러 폴더 수정 필요 |
| 새 팀원 온보딩 용이 | 파일 수 증가 시 탐색 어려움 |
| 공통 컴포넌트 한 곳에서 관리 | 논리적 연관성 파악 어려움 |

---

### 3. 하이브리드 그룹화 (권장)

두 접근 방식의 장점을 결합한다.

```
src/
├── css/
│   └── global.css
├── components/          # 공통 컴포넌트
│   ├── User/
│   │   ├── profile.js
│   │   ├── profile.test.js
│   │   └── avatar.js
│   ├── date.js
│   ├── currency.js
│   └── errorUtils.js
└── domain/              # 도메인/기능별
    ├── product/
    │   ├── product.js
    │   ├── product.css
    │   └── product.test.js
    └── checkout/
        ├── checkout.js
        ├── checkout.css
        └── checkout.test.js
```

**중첩 깊이 가이드라인**:

```
권장 (3-4 레벨):
domain/ → product/ → components/

피할 것 (5+ 레벨):
domain/ → product/ → type/ → features/ → size/
```

---

### 4. Redux 구조 (Ducks 패턴)

기능별 로직을 한 곳에 배치하는 "slice" 패턴이다.

```
src/
├── index.tsx
├── app/
│   ├── store.ts
│   ├── rootReducer.ts
│   └── App.tsx
├── common/
│   ├── hooks/
│   └── utils/
└── features/
    └── todos/
        ├── todosSlice.ts    # Redux 로직
        └── Todos.tsx        # React 컴포넌트
```

**Slice 파일 예시**:

```typescript
// features/todos/todosSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Todo {
  id: string;
  text: string;
  completed: boolean;
}

const todosSlice = createSlice({
  name: 'todos',
  initialState: [] as Todo[],
  reducers: {
    addTodo: (state, action: PayloadAction<string>) => {
      state.push({
        id: Date.now().toString(),
        text: action.payload,
        completed: false
      });
    },
    toggleTodo: (state, action: PayloadAction<string>) => {
      const todo = state.find(t => t.id === action.payload);
      if (todo) todo.completed = !todo.completed;
    }
  }
});

export const { addTodo, toggleTodo } = todosSlice.actions;
export default todosSlice.reducer;
```

---

### 5. Hooks 구조

```
src/
├── components/
│   └── ProductList/
│       ├── index.js
│       ├── test.js
│       ├── style.css
│       └── hooks.js         # 이 컴포넌트 전용 Hook
└── hooks/                   # 공통 Hooks
    ├── useClickOutside/
    │   └── index.js
    ├── useLocalStorage/
    │   └── index.js
    └── useDebounce/
        └── index.js
```

**공통 Hook 예시**:

```javascript
// hooks/useLocalStorage/index.js
import { useState, useEffect } from 'react';

export function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      return initialValue;
    }
  });

  useEffect(() => {
    window.localStorage.setItem(key, JSON.stringify(storedValue));
  }, [key, storedValue]);

  return [storedValue, setStoredValue];
}
```

---

### 6. Styled Components 구조

```
src/
├── components/
│   └── Button/
│       ├── index.js         # 컴포넌트 로직
│       └── style.js         # 스타일 정의
├── theme.js                  # 전역 테마 설정
└── globals.js                # 전역 스타일
```

```javascript
// components/Button/style.js
import styled from 'styled-components';

export const StyledButton = styled.button`
  background-color: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.text};
  padding: ${({ size }) => size === 'large' ? '12px 24px' : '8px 16px'};
  border: none;
  border-radius: 4px;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }
`;

// components/Button/index.js
import { StyledButton } from './style';

export function Button({ children, size = 'medium', ...props }) {
  return (
    <StyledButton size={size} {...props}>
      {children}
    </StyledButton>
  );
}
```

---

### 7. Next.js 구조

**Pages Router 구조**:

```
프로젝트/
├── public/
│   └── images/
├── common/
│   ├── components/
│   ├── hooks/
│   ├── utils/
│   └── styles/
├── modules/
│   ├── auth/
│   └── product/
└── pages/
    ├── _app.js
    ├── _document.js
    ├── index.js
    └── products/
        └── [id].js
```

**App Router 구조 (Next.js 13+)**:

```
src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── loading.tsx
│   ├── error.tsx
│   └── products/
│       ├── page.tsx
│       └── [id]/
│           └── page.tsx
├── components/
│   ├── ui/               # 기본 UI 컴포넌트
│   └── features/         # 기능별 컴포넌트
├── lib/                  # 유틸리티, API 클라이언트
└── hooks/
```

---

## 베스트 프랙티스

### Import Alias 설정

```javascript
// 피할 것
import { Button } from '../../../components/ui/Button';

// 권장
import { Button } from '@/components/ui/Button';
```

**설정 (tsconfig.json)**:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@hooks/*": ["src/hooks/*"],
      "@utils/*": ["src/utils/*"]
    }
  }
}
```

---

### Third-party 라이브러리 래핑

```javascript
// lib/analytics.js
import gtag from 'some-analytics-lib';

export const analytics = {
  pageView: (path) => {
    gtag.pageview(path);
  },
  event: (name, params) => {
    gtag.event(name, params);
  }
};

// 사용처
import { analytics } from '@/lib/analytics';
analytics.pageView('/home');
```

---

### PropTypes 사용

```javascript
import PropTypes from 'prop-types';

function UserCard({ name, email, role, onEdit }) {
  return (
    <div>
      <h3>{name}</h3>
      <p>{email}</p>
      <span>{role}</span>
      <button onClick={onEdit}>Edit</button>
    </div>
  );
}

UserCard.propTypes = {
  name: PropTypes.string.isRequired,
  email: PropTypes.string.isRequired,
  role: PropTypes.oneOf(['admin', 'user', 'guest']),
  onEdit: PropTypes.func
};

UserCard.defaultProps = {
  role: 'user',
  onEdit: () => {}
};
```

---

## 구조 선택 가이드

```
프로젝트 규모?
    │
    ├─ 소규모 (50개 미만 파일)
    │       └─ 파일 유형별 그룹화
    │
    ├─ 중규모 (50-200 파일)
    │       └─ 하이브리드 구조
    │           └─ Redux 사용? → Ducks 패턴
    │
    └─ 대규모 (200+ 파일)
            └─ 도메인 기반 + 모노레포
```

### 프로젝트 규모별 권장 구조

| 규모 | 파일 수 | 권장 구조 | 특징 |
|------|--------|----------|------|
| 소규모 | ~50 | 파일 유형별 | 단순, 빠른 시작 |
| 중규모 | 50-200 | 하이브리드 | 도메인 + 공통 분리 |
| 대규모 | 200+ | 도메인 기반 | 기능별 독립, 팀별 소유권 |

### 폴더 네이밍 컨벤션

| 유형 | 권장 네이밍 | 예시 |
|------|-----------|------|
| 컴포넌트 폴더 | PascalCase | `Button/`, `UserCard/` |
| 유틸리티 폴더 | camelCase | `utils/`, `hooks/` |
| 페이지/라우트 | kebab-case | `user-profile/` |
| 기능/도메인 | camelCase | `auth/`, `product/` |

---

## 트레이드오프

### DO (권장)

- 프로젝트 초기에 구조 결정 및 문서화
- Import alias 설정으로 경로 단순화
- 관련 파일(컴포넌트, 스타일, 테스트) 코로케이션
- Third-party 라이브러리 래핑
- 팀 컨벤션 문서화 및 공유

### DON'T (주의)

- 4레벨 이상의 깊은 중첩
- 구조 없이 시작하여 나중에 대규모 리팩토링
- 팀원마다 다른 구조 사용
- 불필요한 폴더 생성 (파일 1개에 폴더 1개)
- 순환 의존성 허용

---

## 마이그레이션 전략

기존 프로젝트 구조 개선 시:

1. **분석**: 현재 구조의 문제점 파악
2. **계획**: 목표 구조 설계 및 문서화
3. **점진적 적용**: 새 기능부터 새 구조 적용
4. **리팩토링**: 기존 코드 단계적 이동
5. **검증**: 빌드/테스트 확인

---

## 면접 포인트

**Q**: 기능별 그룹화와 파일 유형별 그룹화의 차이점은?

**A**: 기능별 그룹화는 관련 파일(컴포넌트, 스타일, 테스트)을 한 폴더에 모아 변경 영향 범위를 명확하게 한다. 파일 유형별 그룹화는 모든 CSS, 모든 컴포넌트를 각각 폴더에 모아 표준화된 구조를 제공한다. 기능별은 도메인 로직이 명확한 중대형 프로젝트에, 유형별은 작은 프로젝트나 팀 간 표준화가 중요할 때 적합하다.

**Q**: 컴포넌트 구조에서 코로케이션(Colocation)이란?

**A**: 코로케이션은 관련된 파일들을 같은 위치에 배치하는 원칙이다. 예를 들어 Button 컴포넌트의 로직, 스타일, 테스트 파일을 모두 Button/ 폴더에 배치한다. 이렇게 하면 컴포넌트 수정 시 관련 파일을 쉽게 찾고, 변경 영향 범위를 파악하기 쉬우며, 컴포넌트를 독립적으로 관리할 수 있다.

**Q**: Next.js App Router의 폴더 구조 특징은?

**A**: App Router는 파일 시스템 기반 라우팅을 사용하며, app/ 폴더 내에 page.tsx, layout.tsx, loading.tsx, error.tsx 등 규약된 파일명을 사용한다. [id]/ 같은 동적 라우트, (group)/ 같은 라우트 그룹을 지원하고, Server Components가 기본값이다. 컴포넌트와 유틸리티는 app/ 외부의 components/, lib/ 등에 배치하는 것이 일반적이다.

---

## 참고 자료

- [React 파일 구조 권장사항](https://reactjs.org/docs/faq-structure.html)
- [Redux Style Guide](https://redux.js.org/style-guide/)
- [Next.js 프로젝트 구조](https://nextjs.org/docs/getting-started/project-structure)
- [Bulletproof React](https://github.com/alan2207/bulletproof-react)
