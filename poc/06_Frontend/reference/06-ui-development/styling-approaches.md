# Chapter 4. React 스타일링 접근법 (Approaches to Styling React Frontends)

---

### 📌 핵심 요약
> React는 표준 스타일링 메커니즘을 제공하지 않으며, 커뮤니티에서 다양한 접근법이 발전해왔다. **Plain CSS**는 간단하지만 클래스 충돌 문제가 있고, **CSS Modules**는 자동으로 클래스명을 스코핑하여 충돌을 방지한다. **Tailwind CSS**는 재사용 가능한 유틸리티 클래스를 제공하며, 사용된 클래스만 번들에 포함되어 작은 CSS 파일을 생성한다. SVG는 아이콘에 권장되며, Vite에서 쉽게 임포트하여 사용할 수 있다.

---

### 🎯 학습 목표
- Plain CSS의 장단점과 클래스 충돌 문제를 이해한다
- CSS Modules로 스타일을 컴포넌트에 스코핑할 수 있다
- Tailwind CSS를 설치, 설정하고 유틸리티 클래스를 사용할 수 있다
- React 앱에서 SVG를 사용하는 방법을 안다
- 프로젝트에 적합한 스타일링 접근법을 선택할 수 있다

---

### 📖 본문 정리

#### 1. Plain CSS

##### 사용 방법

```tsx
// CSS 파일 임포트
import './Alert.css';

// className 속성으로 클래스 적용
function Alert() {
  return (
    <div className="container">
      <span className="header-text">제목</span>
    </div>
  );
}
```

> 💡 React는 `class` 대신 `className`을 사용 (JavaScript에서 class는 예약어)

##### Alert.css 예시

```css
.container {
  display: inline-flex;
  flex-direction: column;
  text-align: left;
  padding: 1em;
  border-radius: 4px;
  border: 1px solid transparent;
}
.container.warning {
  color: #e7650f;
  background-color: #f3e8da;
}
.container.information {
  color: #118da0;
  background-color: #dcf1f3;
}
```

##### 조건부 클래스 적용

```tsx
<div className={`container ${type}`}>
  {/* type이 'warning'이면 container warning 클래스 적용 */}
</div>
```

##### Plain CSS의 문제: 클래스 충돌

```
┌─────────────────────────────────────────────────────┐
│              CSS 클래스 충돌 문제                    │
├─────────────────────────────────────────────────────┤
│                                                      │
│  App.css                    Alert.css               │
│  ┌─────────────────┐       ┌─────────────────┐     │
│  │ .container {    │       │ .container {    │     │
│  │   padding: 2em; │       │   padding: 1em; │     │
│  │ }               │       │ }               │     │
│  └────────┬────────┘       └────────┬────────┘     │
│           │                         │               │
│           └─────────┬───────────────┘               │
│                     ▼                               │
│           ⚠️ 같은 이름 = 스타일 충돌!               │
│                                                      │
└─────────────────────────────────────────────────────┘
```

##### Plain CSS 장단점

| 장점 | 단점 |
|------|------|
| 간단하고 익숙함 | 클래스 이름 충돌 가능 |
| 추가 설정 불필요 | 스코핑 없음 (전역 적용) |
| 빠른 개발 | 사용하지 않는 CSS도 번들에 포함 |

> 💡 **BEM 명명법**: 충돌 방지를 위해 `Alert__container`, `App__container` 같이 이름 지정

---

#### 2. CSS Modules

##### 개념

CSS Modules는 CSS 클래스명을 **자동으로 스코핑**하여 충돌을 방지하는 오픈소스 라이브러리.

```
┌─────────────────────────────────────────────────────┐
│               CSS Modules 동작 원리                  │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Alert.module.css           빌드 후                 │
│  ┌─────────────────┐       ┌─────────────────────┐  │
│  │ .container {    │  ──▶  │ ._container_16mbb_1 │  │
│  │   padding: 1em; │       │ {                   │  │
│  │ }               │       │   padding: 1em;     │  │
│  └─────────────────┘       │ }                   │  │
│                            └─────────────────────┘  │
│                                                      │
│  ✅ 고유한 클래스명으로 충돌 방지                   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

##### 사용 방법

**1. 파일명 변경**: `.css` → `.module.css`

```css
/* Alert.module.css */
.container {
  display: inline-flex;
  flex-direction: column;
  padding: 1em;
}
.headerIcon {
  width: 22px;
}
.headerText {
  font-weight: bold;
}
```

> 💡 camelCase 사용 권장: `header-text` → `headerText` (JS에서 접근 용이)

**2. 임포트 및 사용**

```tsx
import styles from './Alert.module.css';

function Alert({ type }: Props) {
  return (
    <div className={`${styles.container} ${styles[type]}`}>
      <span className={styles.headerIcon}>🔔</span>
      <span className={styles.headerText}>제목</span>
    </div>
  );
}
```

**3. 렌더링 결과**

```html
<!-- 스코핑된 클래스명 -->
<div class="_container_16mbb_1 _warning_16mbb_7">
  <span class="_headerIcon_16mbb_12">🔔</span>
  <span class="_headerText_16mbb_18">제목</span>
</div>
```

##### CSS Modules 장단점

| 장점 | 단점 |
|------|------|
| 자동 스코핑 (충돌 방지) | camelCase 변환 필요 |
| Plain CSS 문법 그대로 사용 | 사용하지 않는 CSS도 번들에 포함 |
| Vite에 기본 설정됨 | 동적 클래스명 사용 시 약간 복잡 |

---

#### 3. Tailwind CSS

##### 개념

Tailwind는 **유틸리티 우선(utility-first)** CSS 프레임워크로, 미리 정의된 클래스를 조합하여 스타일링.

```
┌─────────────────────────────────────────────────────┐
│              Tailwind CSS 철학                       │
├─────────────────────────────────────────────────────┤
│                                                      │
│  기존 CSS          Tailwind                         │
│  ┌─────────────┐   ┌────────────────────────────┐  │
│  │ .button {   │   │ className="bg-blue-500     │  │
│  │   bg: blue; │   │   text-white rounded-md    │  │
│  │   color:    │   │   px-4 py-2 cursor-pointer │  │
│  │     white;  │   │   hover:bg-blue-700"       │  │
│  │   ...       │   │                            │  │
│  │ }           │   └────────────────────────────┘  │
│  └─────────────┘                                    │
│                                                      │
│  새 CSS 작성 ❌  →  기존 클래스 조합 ✅             │
│                                                      │
└─────────────────────────────────────────────────────┘
```

##### 설치 및 설정

```bash
# 1. 패키지 설치
npm i -D tailwindcss @tailwindcss/vite

# 2. Prettier 플러그인 (선택)
npm i -D prettier-plugin-tailwindcss
```

```typescript
// vite.config.ts
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
});
```

```css
/* index.css */
@import 'tailwindcss';
```

##### 주요 유틸리티 클래스

| 카테고리 | 클래스 예시 | 설명 |
|----------|-------------|------|
| **레이아웃** | `flex`, `inline-flex`, `flex-col` | Flexbox |
| **간격** | `p-4`, `m-2`, `px-3`, `my-1` | Padding/Margin |
| **크기** | `w-6`, `h-6`, `w-full` | Width/Height |
| **색상** | `bg-blue-500`, `text-white` | Background/Text |
| **테두리** | `border`, `rounded-md`, `border-none` | Border |
| **텍스트** | `font-bold`, `text-left`, `text-sm` | Font 스타일 |
| **커서** | `cursor-pointer` | 마우스 커서 |

> 💡 **Spacing 단위**: 1 = 0.25rem ≈ 4px (p-4 = padding: 1rem)

##### 조건부 스타일 & Hover 상태

```tsx
// 조건부 스타일
<div className={`p-3 rounded-md ${
  type === 'warning'
    ? 'bg-amber-50 text-amber-900'
    : 'bg-teal-50 text-teal-900'
}`}>

// Hover 상태
<button className="bg-blue-500 hover:bg-blue-700">
  Click
</button>
```

##### Alert 컴포넌트 Tailwind 예시

```tsx
function Alert({ type, heading, children, closable }: Props) {
  return (
    <div className={`inline-flex flex-col rounded-md border-1
      border-transparent p-3 text-left ${
        type === 'warning'
          ? 'bg-amber-50 text-amber-900'
          : 'bg-teal-50 text-teal-900'
      }`}>

      <div className="mb-1 flex items-center">
        <img src={icon} className="mr-1 h-6 w-6" />
        <span className="font-bold">{heading}</span>
        {closable && (
          <button className="ml-auto flex h-6 w-6 cursor-pointer
            items-center justify-center border-none bg-transparent">
            ✕
          </button>
        )}
      </div>

      <div className="ml-7 pr-5 text-black">
        {children}
      </div>
    </div>
  );
}
```

##### Tailwind 장단점

| 장점 | 단점 |
|------|------|
| 사용된 클래스만 번들에 포함 | 클래스가 많아 JSX 가독성 저하 |
| 일관된 디자인 시스템 (색상, 간격) | 러닝 커브 존재 |
| 재사용성 높음 | 동적 클래스 생성 불가* |
| IntelliSense 지원 | |

> ⚠️ **동적 클래스 주의**: `bg-${color}-500`은 빌드 시점에 결정 불가 → 작동 안 함

---

#### 4. SVG 사용

##### SVG를 사용하는 이유

```
┌─────────────────────────────────────────────────────┐
│            PNG vs SVG 비교                           │
├─────────────────────────────────────────────────────┤
│                                                      │
│  PNG (래스터)              SVG (벡터)               │
│  ┌─────────────┐          ┌─────────────┐          │
│  │ ██████████  │          │ 수학적 공식  │          │
│  │ ██████████  │          │ 기반 도형    │          │
│  │ ██████████  │          │             │          │
│  └─────────────┘          └─────────────┘          │
│  확대 시 깨짐 ❌           확대해도 선명 ✅         │
│                                                      │
└─────────────────────────────────────────────────────┘
```

##### 방법 1: img 태그로 사용

```tsx
import warningIcon from './assets/warning.svg';
import infoIcon from './assets/info.svg';

function Alert({ type }: Props) {
  return (
    <img
      src={type === 'warning' ? warningIcon : infoIcon}
      alt={type === 'warning' ? 'Warning' : 'Information'}
      className="h-6 w-6"
    />
  );
}
```

##### 방법 2: JSX에 직접 삽입

```tsx
function UpArrow() {
  return (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
      <path d="M12 4L4 12H9V20H15V12H20L12 4Z" fill="white" />
    </svg>
  );
}
```

##### 방법 3: React 컴포넌트로 임포트 (vite-plugin-svgr)

```tsx
// ?react 쿼리 파라미터 사용
import UpArrow from './icons/uparrow.svg?react';

function Upload() {
  return (
    <button>
      <UpArrow />  {/* 컴포넌트처럼 사용 */}
    </button>
  );
}
```

##### public 폴더 vs src/assets

| 위치 | 용도 | 임포트 방식 |
|------|------|-------------|
| `public/` | 빌드 시 이름 유지 필요한 파일 | `/logo.svg` (절대 경로) |
| `src/assets/` | 일반 에셋 파일 | `import logo from './assets/logo.svg'` |

---

#### 5. 기타 스타일링 접근법

##### Inline Styles

```tsx
<div
  style={{
    display: "inline-flex",
    flexDirection: "column",
    padding: "1em",
    backgroundColor: type === "warning" ? "#f3e8da" : "#dcf1f3",
  }}
>
  ...
</div>
```

| 장점 | 단점 |
|------|------|
| 간단함, 스코핑 자동 | :hover, ::before 사용 불가 |
| 빌드 불필요 | 성능 저하 (캐시 불가) |

##### SCSS

```scss
// Alert.scss
.container {
  display: inline-flex;
  padding: 1em;

  // 중첩 문법
  &.warning {
    color: #e7650f;
    background-color: #f3e8da;
  }
  &.information {
    color: #118da0;
    background-color: #dcf1f3;
  }
}
```

```bash
# 설치 필요
npm i -D sass-embedded
```

> 💡 CSS 네이티브에서 변수와 중첩이 지원되면서 SCSS 인기 감소

##### CSS-in-JS (styled-components)

```tsx
import styled from 'styled-components';

const Container = styled.div<{ type: string }>`
  display: inline-flex;
  padding: 1em;
  ${(props) =>
    props.type === "warning" &&
    `
    color: #e7650f;
    background-color: #f3e8da;
  `}
`;

function Alert({ type }: Props) {
  return <Container type={type}>...</Container>;
}
```

| 장점 | 단점 |
|------|------|
| JS에서 동적 스타일 쉬움 | 런타임 성능 저하 |
| 스코핑 자동 | Server Component에서 사용 불가 |

> ⚠️ styled-components는 현재 유지보수 모드. 새 프로젝트에는 StyleX, Panda CSS 고려

---

### 🔍 심화 학습

#### 스타일링 접근법 비교표

| 접근법 | 스코핑 | 번들 최적화 | 러닝 커브 | Server Component |
|--------|--------|-------------|-----------|------------------|
| Plain CSS | ❌ | ❌ | 낮음 | ✅ |
| CSS Modules | ✅ | ❌ | 낮음 | ✅ |
| Tailwind | ✅* | ✅ | 중간 | ✅ |
| Inline Styles | ✅ | ❌ | 낮음 | ✅ |
| styled-components | ✅ | ❌ | 중간 | ❌ |

*Tailwind는 유틸리티 클래스라 스코핑 개념 자체가 불필요

#### Tailwind 동적 클래스 해결법

```tsx
// ❌ 작동 안 함 (빌드 시점에 클래스 결정 불가)
<div className={`bg-${color}-500`} />

// ✅ 해결법 1: 완전한 클래스명 사용
const colorClasses = {
  red: 'bg-red-500',
  blue: 'bg-blue-500',
  green: 'bg-green-500',
};
<div className={colorClasses[color]} />

// ✅ 해결법 2: tailwind.config.js에 safelist 추가
module.exports = {
  safelist: ['bg-red-500', 'bg-blue-500', 'bg-green-500'],
};
```

---

### 💡 실무 적용 포인트

1. **신규 프로젝트**: Tailwind CSS 권장 (작은 번들, 일관된 디자인)
2. **기존 프로젝트**: CSS Modules로 점진적 마이그레이션
3. **컴포넌트 라이브러리**: CSS Modules (의존성 최소화)
4. **아이콘**: 항상 SVG 사용 (PNG/JPG 대신)
5. **VSCode 확장**: Tailwind CSS IntelliSense 필수 설치
6. **Prettier 플러그인**: prettier-plugin-tailwindcss로 클래스 정렬
7. **동적 스타일**: Tailwind에서 완전한 클래스명 사용 또는 safelist

---

### ✅ 정리 체크리스트

- [ ] Plain CSS의 클래스 충돌 문제와 BEM 명명법을 안다
- [ ] CSS Modules의 파일명 규칙(.module.css)과 사용법을 안다
- [ ] Tailwind CSS 설치 및 설정을 할 수 있다
- [ ] Tailwind 유틸리티 클래스 (flex, p-4, bg-blue-500 등)를 사용할 수 있다
- [ ] Tailwind의 hover: 프리픽스 사용법을 안다
- [ ] Tailwind에서 동적 클래스명이 작동하지 않는 이유를 안다
- [ ] SVG를 img 태그와 React 컴포넌트로 사용할 수 있다
- [ ] Inline Styles의 한계(pseudo 클래스 불가)를 안다
- [ ] 프로젝트에 적합한 스타일링 접근법을 선택할 수 있다

---

### 🔗 참고 자료

- [Tailwind CSS 공식 문서](https://tailwindcss.com/)
- [CSS Modules GitHub](https://github.com/css-modules/css-modules)
- [BEM 명명법](https://css-tricks.com/bem-101/)
- [vite-plugin-svgr](https://github.com/pd4d10/vite-plugin-svgr)
- [styled-components](https://styled-components.com)
- [StyleX](https://stylexjs.com)
- [Panda CSS](https://panda-css.com)
- [SASS/SCSS](https://sass-lang.com)
- [책 코드 저장소](https://github.com/PacktPublishing/Learn-React-with-TypeScript-Third-Edition/tree/main/Chapter04)
