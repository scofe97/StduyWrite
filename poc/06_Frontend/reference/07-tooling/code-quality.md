# 코드 품질 도구

## 개요

**정의**: 코드 품질 도구는 일관된 코드 스타일, 잠재적 버그 탐지, 자동 포맷팅을 통해 코드베이스 품질을 유지하는 자동화 도구이다.

**목적**: 코드 리뷰 부담 감소, 버그 사전 방지, 팀 코딩 컨벤션 통일, 개발자 경험 향상을 달성한다.

---

## 핵심 도구

| 도구 | 역할 | 설정 파일 |
|------|------|----------|
| **ESLint** | 코드 린팅 (버그/안티패턴 탐지) | `.eslintrc.js` |
| **Prettier** | 코드 포맷팅 | `.prettierrc` |
| **Husky** | Git hooks 관리 | `.husky/` |
| **lint-staged** | 스테이징된 파일만 린트 | `package.json` |

---

## 구현 패턴

### 1. ESLint 설정

```bash
npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
npm install -D eslint-plugin-react eslint-plugin-react-hooks
```

```javascript
// .eslintrc.js
module.exports = {
  root: true,
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 2022,
    sourceType: 'module',
    ecmaFeatures: { jsx: true },
  },
  env: {
    browser: true,
    es2022: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'prettier',  // Prettier와 충돌 방지 (마지막에)
  ],
  plugins: ['@typescript-eslint', 'react', 'react-hooks'],
  rules: {
    // TypeScript
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    '@typescript-eslint/explicit-function-return-type': 'off',

    // React
    'react/react-in-jsx-scope': 'off',  // React 17+
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',

    // 일반
    'no-console': ['warn', { allow: ['warn', 'error'] }],
    'prefer-const': 'error',
  },
  settings: {
    react: { version: 'detect' },
  },
};
```

### 2. Prettier 설정

```bash
npm install -D prettier eslint-config-prettier
```

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "bracketSpacing": true,
  "arrowParens": "avoid",
  "endOfLine": "lf"
}
```

```
// .prettierignore
node_modules
dist
build
coverage
*.min.js
```

### 3. Husky + lint-staged

```bash
npm install -D husky lint-staged
npx husky init
```

```json
// package.json
{
  "scripts": {
    "lint": "eslint src --ext .ts,.tsx",
    "format": "prettier --write src",
    "prepare": "husky"
  },
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,css}": ["prettier --write"]
  }
}
```

```bash
# .husky/pre-commit
npx lint-staged
```

### 4. VS Code 설정

```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

```json
// .vscode/extensions.json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode"
  ]
}
```

---

## 워크플로우

```
코드 작성
    │
    ▼
저장 시 자동 포맷 (Prettier)
    │
    ▼
커밋 시도
    │
    ▼
pre-commit hook (Husky)
    │
    ▼
lint-staged 실행
    ├─ ESLint --fix
    └─ Prettier --write
    │
    ▼
통과 시 커밋 완료
실패 시 커밋 중단 → 수정 필요
```

---

## 트레이드오프

| 설정 수준 | 장점 | 단점 |
|----------|------|------|
| 엄격함 | 일관성 최대화, 버그 방지 | 초기 설정 시간, 유연성 감소 |
| 느슨함 | 빠른 시작, 자유도 | 품질 불일치, 기술 부채 |

**권장**: 프로젝트 초기에 엄격하게 설정 후 필요 시 완화

---

## 면접 포인트

**Q**: ESLint와 Prettier의 차이는?

**A**: ESLint는 코드 품질과 잠재적 버그를 검사하는 린터이고, Prettier는 코드 스타일만 일관되게 포맷하는 포맷터이다. ESLint는 규칙 위반을 에러로 보고하고, Prettier는 의견 없이 자동 수정한다. 둘을 함께 사용할 때 eslint-config-prettier로 충돌을 방지한다.

**Q**: lint-staged를 사용하는 이유는?

**A**: 전체 프로젝트를 린팅하면 시간이 오래 걸린다. lint-staged는 git에 스테이징된 파일만 검사하여 커밋 속도를 빠르게 유지하면서도 새로 작성된 코드의 품질을 보장한다.

---

## 참고 자료

- [ESLint 공식 문서](https://eslint.org/)
- [Prettier 공식 문서](https://prettier.io/)
- [Husky 공식 문서](https://typicode.github.io/husky/)
