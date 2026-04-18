# Frontend 라이브러리 추가 계획

## 개요

GitHub 스타일 파일 구조, Diff, 코드 내용 출력을 위한 프론트엔드 라이브러리 추가 계획

---

## 현재 의존성 현황

```json
{
  "UI": ["@radix-ui/*", "lucide-react", "tailwindcss"],
  "상태관리": ["zustand", "@tanstack/react-query"],
  "폼": ["react-hook-form", "zod"],
  "유틸": ["date-fns", "lodash-es", "clsx", "tailwind-merge"]
}
```

---

## 추가 필요 라이브러리

### Phase 1: 코드 하이라이팅 (필수)

#### 옵션 A: react-syntax-highlighter (권장)
```bash
yarn add react-syntax-highlighter
yarn add -D @types/react-syntax-highlighter
```

| 장점 | 단점 |
|------|------|
| 200+ 언어 지원 | 번들 크기 큼 (Prism: ~60KB) |
| PrismJS/highlight.js 테마 내장 | |
| GitHub 스타일 테마 포함 | |

**사용 예시**:
```tsx
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

<SyntaxHighlighter language="typescript" style={oneDark}>
  {code}
</SyntaxHighlighter>
```

#### 옵션 B: prism-react-renderer (경량)
```bash
yarn add prism-react-renderer
```

| 장점 | 단점 |
|------|------|
| 번들 크기 작음 (~15KB) | 언어 추가 설정 필요 |
| Render props 패턴 | 기본 언어 제한적 |
| 커스터마이징 용이 | |

**권장**: `react-syntax-highlighter` (Prism 라이트 버전)

---

### Phase 2: Diff 뷰어 (필수)

#### 옵션 A: react-diff-viewer-continued (권장)
```bash
yarn add react-diff-viewer-continued
```

| 특징 | 설명 |
|------|------|
| Split/Unified 뷰 | GitHub 스타일 지원 |
| 라인 하이라이팅 | 추가/삭제/변경 표시 |
| 구문 강조 내장 | Prism 기반 |
| TypeScript 지원 | 타입 정의 포함 |

**사용 예시**:
```tsx
import ReactDiffViewer from 'react-diff-viewer-continued';

<ReactDiffViewer
  oldValue={oldCode}
  newValue={newCode}
  splitView={true}
  useDarkTheme={true}
/>
```

#### 옵션 B: diff + 직접 구현
```bash
yarn add diff
yarn add -D @types/diff
```

**권장**: `react-diff-viewer-continued` (완성도 높음)

---

### Phase 3: 마크다운 렌더링 (권장)

```bash
yarn add react-markdown remark-gfm rehype-highlight
```

| 라이브러리 | 역할 |
|-----------|------|
| `react-markdown` | 마크다운 → React 변환 |
| `remark-gfm` | GitHub Flavored Markdown |
| `rehype-highlight` | 코드블록 구문 강조 |

**사용 예시**:
```tsx
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';

<ReactMarkdown
  remarkPlugins={[remarkGfm]}
  rehypePlugins={[rehypeHighlight]}
>
  {markdown}
</ReactMarkdown>
```

---

### Phase 4: 가상화 (대용량 파일용)

```bash
yarn add @tanstack/react-virtual
```

| 용도 | 설명 |
|------|------|
| 대용량 파일 | 1000줄+ 코드 파일 |
| 파일 트리 | 수천 개 파일 트리 |
| 커밋 히스토리 | 무한 스크롤 |

**사용 예시**:
```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

const virtualizer = useVirtualizer({
  count: lines.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 20, // 라인 높이
});
```

---

### Phase 5: 파일 아이콘 (선택)

#### 옵션 A: vscode-icons (권장)
```bash
yarn add @vscode/codicons
```

#### 옵션 B: file-icons 직접 구현
- Lucide React로 기본 아이콘 사용
- 확장자별 매핑 함수 구현

**권장**: Lucide React 활용 + 커스텀 매핑

---

## 설치 명령어 (전체)

```bash
# 필수 라이브러리
yarn add react-syntax-highlighter react-diff-viewer-continued

# 타입 정의
yarn add -D @types/react-syntax-highlighter

# 권장 라이브러리
yarn add react-markdown remark-gfm rehype-highlight

# 성능 최적화
yarn add @tanstack/react-virtual
```

---

## 번들 크기 예상

| 라이브러리 | 크기 (gzipped) |
|-----------|----------------|
| react-syntax-highlighter (prism-light) | ~25KB |
| react-diff-viewer-continued | ~20KB |
| react-markdown + plugins | ~15KB |
| @tanstack/react-virtual | ~5KB |
| **합계** | **~65KB** |

---

## 컴포넌트 구조 계획

```
src/
├── components/
│   ├── code/
│   │   ├── CodeViewer.tsx          # 코드 뷰어 (하이라이팅)
│   │   ├── DiffViewer.tsx          # Diff 뷰어
│   │   └── LineNumbers.tsx         # 라인 번호
│   │
│   ├── file/
│   │   ├── FileTree.tsx            # 파일 트리
│   │   ├── FileTreeItem.tsx        # 트리 아이템
│   │   ├── FileIcon.tsx            # 파일 아이콘
│   │   └── FileBreadcrumb.tsx      # 경로 표시
│   │
│   └── markdown/
│       └── MarkdownViewer.tsx      # 마크다운 렌더러
│
├── hooks/
│   ├── useFileTree.ts              # 파일 트리 상태
│   └── useCodeHighlight.ts         # 코드 하이라이팅 설정
│
└── lib/
    ├── fileIcons.ts                # 파일 아이콘 매핑
    └── languageDetect.ts           # 언어 자동 감지
```

---

## 기능별 라이브러리 매핑

| 기능 | 라이브러리 | 우선순위 |
|------|-----------|---------|
| 코드 내용 출력 | react-syntax-highlighter | 필수 |
| 파일 Diff 표시 | react-diff-viewer-continued | 필수 |
| 파일 트리 | Radix UI Collapsible (기존) | 필수 |
| README 렌더링 | react-markdown + remark-gfm | 권장 |
| 대용량 파일 스크롤 | @tanstack/react-virtual | 권장 |
| 파일 아이콘 | Lucide React (기존) | 선택 |

---

## 구현 우선순위

### MVP (필수)
1. `react-syntax-highlighter` - 코드 뷰어
2. `react-diff-viewer-continued` - Diff 뷰어
3. 파일 트리 컴포넌트 (Radix UI 기반 직접 구현)

### v1.1 (권장)
4. `react-markdown` + 플러그인 - README 표시
5. `@tanstack/react-virtual` - 성능 최적화

### v1.2 (선택)
6. 파일 검색 (Go to file)
7. Blame 뷰어

---

## API 연동 계획

| 프론트엔드 컴포넌트 | git-provider API | 설명 |
|-------------------|------------------|------|
| FileTree | GetTree | 전체 파일 목록 |
| CodeViewer | GetContents | 파일 내용 |
| DiffViewer | Compare | 브랜치 비교 |
| CommitHistory | ListCommits | 커밋 히스토리 |

---

## 테마 설정

```tsx
// GitHub 스타일 테마
const codeTheme = {
  light: 'github',
  dark: 'oneDark'
};

const diffTheme = {
  light: {
    addedBackground: '#e6ffec',
    removedBackground: '#ffebe9',
  },
  dark: {
    addedBackground: '#1f3b2a',
    removedBackground: '#3b1f1f',
  }
};
```

---

## 참고 자료

- [react-syntax-highlighter](https://github.com/react-syntax-highlighter/react-syntax-highlighter)
- [react-diff-viewer-continued](https://github.com/aeolun/react-diff-viewer-continued)
- [react-markdown](https://github.com/remarkjs/react-markdown)
- [@tanstack/react-virtual](https://tanstack.com/virtual/latest)
