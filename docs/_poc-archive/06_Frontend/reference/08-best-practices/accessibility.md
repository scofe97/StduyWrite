# 웹 접근성 (Accessibility)

## 개요

**정의**: 웹 접근성(A11y)은 장애인, 고령자를 포함한 모든 사용자가 웹을 동등하게 이용할 수 있도록 하는 설계 원칙이다.

**목적**: 법적 준수, 사용자 기반 확대, SEO 개선, 전반적인 사용성 향상을 달성한다.

---

## WCAG 2.1 원칙 (POUR)

| 원칙 | 설명 | 핵심 요구사항 |
|------|------|--------------|
| **Perceivable** | 인지 가능 | 대체 텍스트, 자막, 색상 대비 |
| **Operable** | 운용 가능 | 키보드 접근, 충분한 시간 |
| **Understandable** | 이해 가능 | 가독성, 예측 가능성 |
| **Robust** | 견고함 | 보조 기술 호환성 |

---

## 구현 패턴

### 1. 시맨틱 HTML

```html
<!-- 좋은 예: 시맨틱 태그 사용 -->
<header>
  <nav aria-label="Main navigation">
    <a href="/">Home</a>
  </nav>
</header>
<main>
  <article>
    <h1>Article Title</h1>
  </article>
</main>
<footer>...</footer>
```

### 2. ARIA 속성

```html
<!-- 레이블과 설명 -->
<button aria-label="닫기">×</button>
<input aria-describedby="hint" />
<span id="hint">8자 이상 입력</span>

<!-- 상태 표시 -->
<button aria-expanded="false" aria-controls="menu">메뉴</button>
<div aria-live="polite">저장되었습니다.</div>
```

### 3. 키보드 접근성

```css
/* 포커스 스타일 */
:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

/* 스킵 링크 */
.skip-link {
  position: absolute;
  top: -40px;
}
.skip-link:focus {
  top: 0;
}
```

### 4. 색상 대비

```css
/* WCAG AA: 일반 텍스트 4.5:1, 큰 텍스트 3:1 */
.high-contrast {
  background: #ffffff;
  color: #333333;  /* 12.63:1 */
}

/* 색상만으로 정보 전달하지 않기 */
.error {
  color: #d32f2f;
  border-left: 4px solid #d32f2f;
}
.error::before { content: "⚠️ "; }
```

### 5. 폼 접근성

```html
<label for="email">이메일</label>
<input type="email" id="email"
       aria-describedby="email-error"
       aria-invalid="true" required />
<span id="email-error" role="alert">
  유효한 이메일을 입력하세요.
</span>
```

### 6. 스크린 리더 전용 텍스트

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}
```

```html
<button>
  <svg aria-hidden="true">...</svg>
  <span class="sr-only">메뉴 열기</span>
</button>
```

---

## 테스트 도구

```bash
# axe-core (자동화 테스트)
npm install @axe-core/react

# ESLint 플러그인
npm install eslint-plugin-jsx-a11y
```

---

## 면접 포인트

**Q**: aria-hidden과 display:none의 차이는?

**A**: aria-hidden="true"는 스크린 리더에서만 숨기고 시각적으로는 표시된다. display:none은 시각적으로도 스크린 리더에서도 완전히 숨긴다.

**Q**: 포커스 트랩이 필요한 이유는?

**A**: 모달에서 Tab 키가 컴포넌트 바깥으로 나가면 사용자가 뒤에 가려진 콘텐츠와 상호작용하게 된다. 포커스 트랩은 Tab이 컴포넌트 내부에서만 순환하도록 한다.

---

## 참고 자료

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [MDN - Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [A11y Project Checklist](https://www.a11yproject.com/checklist/)
