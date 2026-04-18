# ast-grep: Claude Code를 위한 구조적 코드 검색 가이드

> 작성일: 2026-01-06
> 버전: ast-grep 0.40.4

---

## 목차

1. [개요](#1-개요)
2. [설치](#2-설치)
3. [기본 사용법](#3-기본-사용법)
4. [패턴 문법](#4-패턴-문법)
5. [언어별 활용 예시](#5-언어별-활용-예시)
6. [Claude Code 통합](#6-claude-code-통합)
7. [고급 기능](#7-고급-기능)
8. [실전 활용 사례](#8-실전-활용-사례)
9. [grep vs ast-grep 비교](#9-grep-vs-ast-grep-비교)

---

## 1. 개요

### 1.1 ast-grep이란?

ast-grep(sg)은 **AST(Abstract Syntax Tree) 기반 코드 검색 도구**입니다.

일반적인 텍스트 검색 도구(grep, ripgrep)와 달리, 코드의 **구문 구조**를 이해하여 의미론적 검색이 가능합니다.

```
일반 grep:   "function" 문자열이 포함된 모든 라인
ast-grep:    실제 함수 선언 구문만 검색
```

### 1.2 왜 ast-grep인가?

| 상황 | grep | ast-grep |
|------|------|----------|
| `console.log` 찾기 | 주석 내 텍스트도 매칭 | 실제 함수 호출만 매칭 |
| 함수 정의 찾기 | `function` 텍스트 모두 매칭 | 함수 선언 구문만 매칭 |
| 변수 사용 찾기 | 같은 이름 모두 매칭 | 동일 스코프 변수만 매칭 |
| 특정 패턴 찾기 | 정규표현식 필요 | 코드 패턴으로 직관적 검색 |

### 1.3 핵심 특징

| 특징 | 설명 |
|------|------|
| **AST 기반** | 코드 구조를 이해하는 정확한 검색 |
| **고성능** | Rust로 작성, 멀티코어 활용 |
| **다국어** | 40+ 프로그래밍 언어 지원 |
| **직관적** | 코드 패턴으로 검색 (정규표현식 불필요) |
| **다기능** | 검색, 린팅, 리팩토링 |

---

## 2. 설치

### 2.1 macOS (Homebrew) - 권장

```bash
brew install ast-grep
```

### 2.2 기타 설치 방법

```bash
# npm
npm install --global @ast-grep/cli

# pip
pip install ast-grep-cli

# cargo (Rust)
cargo install ast-grep --locked

# Windows (scoop)
scoop install ast-grep
```

### 2.3 설치 확인

```bash
sg --version
# ast-grep 0.40.4

# 또는
ast-grep --version
```

### 2.4 쉘 자동완성 설정

```bash
# zsh
sg completions zsh > ~/.zfunc/_sg
```

---

## 3. 기본 사용법

### 3.1 기본 명령 구조

```bash
sg run --pattern '패턴' --lang 언어 [경로]
```

### 3.2 간단한 예시

```bash
# console.log 찾기
sg run --pattern 'console.log($MSG)' --lang js

# 특정 디렉토리에서 검색
sg run --pattern 'useState($INIT)' --lang tsx src/

# 여러 언어 지원
sg run --pattern '@Service' --lang java src/
```

### 3.3 주요 옵션

| 옵션 | 설명 | 예시 |
|------|------|------|
| `--pattern` | 검색 패턴 | `--pattern 'console.log($M)'` |
| `--lang` | 언어 지정 | `--lang tsx` |
| `--json` | JSON 출력 | `--json` |
| `--rewrite` | 코드 변환 | `--rewrite 'logger.log($M)'` |

---

## 4. 패턴 문법

### 4.1 와일드카드

| 패턴 | 의미 | 예시 |
|------|------|------|
| `$NAME` | 단일 AST 노드 | `console.log($MSG)` |
| `$$$` | 0개 이상의 노드 | `function($$$)` |
| `$$NAME` | 이름 있는 다중 노드 | `[$$$ITEMS]` |

### 4.2 패턴 예시

```bash
# 단일 와일드카드 ($NAME)
sg run --pattern 'console.log($MSG)' --lang js
# 매칭: console.log("hello"), console.log(variable)

# 다중 와일드카드 ($$$)
sg run --pattern 'function $NAME($$$) { $$$ }' --lang js
# 매칭: 모든 함수 선언

# 배열 요소
sg run --pattern '[$$$ITEMS]' --lang js
# 매칭: 모든 배열 리터럴
```

### 4.3 정확한 매칭 vs 와일드카드

```bash
# 정확한 매칭 (특정 값)
sg run --pattern 'console.log("debug")' --lang js

# 와일드카드 매칭 (모든 값)
sg run --pattern 'console.log($MSG)' --lang js

# 여러 인자
sg run --pattern 'console.log($$$ARGS)' --lang js
```

---

## 5. 언어별 활용 예시

### 5.1 JavaScript/TypeScript

```bash
# console.log 찾기
sg run --pattern 'console.log($$$)' --lang js

# 화살표 함수 찾기
sg run --pattern 'const $NAME = ($$$) => $BODY' --lang js

# async 함수 찾기
sg run --pattern 'async function $NAME($$$) { $$$ }' --lang js

# import 문 찾기
sg run --pattern 'import $NAME from $PATH' --lang js
```

### 5.2 React (TSX)

```bash
# useState 찾기
sg run --pattern 'useState($INIT)' --lang tsx

# useEffect 찾기
sg run --pattern 'useEffect($CALLBACK, [$$$])' --lang tsx

# 커스텀 훅 찾기
sg run --pattern 'const $NAME = use$HOOK($$$)' --lang tsx

# Props 타입 찾기
sg run --pattern 'interface $NAME { $$$PROPS }' --lang tsx

# 컴포넌트 찾기
sg run --pattern 'function $NAME($$$): JSX.Element { $$$ }' --lang tsx
```

### 5.3 Java

```bash
# 애노테이션 찾기
sg run --pattern '@Service' --lang java
sg run --pattern '@Transactional' --lang java
sg run --pattern '@Autowired' --lang java

# 클래스 찾기
sg run --pattern 'public class $NAME { $$$ }' --lang java

# 메서드 찾기
sg run --pattern 'public $TYPE $NAME($$$) { $$$ }' --lang java

# 인터페이스 구현 찾기
sg run --pattern 'class $NAME implements $INTERFACE { $$$ }' --lang java
```

### 5.4 Python

```bash
# 함수 정의 찾기
sg run --pattern 'def $NAME($$$): $$$' --lang python

# 클래스 정의 찾기
sg run --pattern 'class $NAME: $$$' --lang python

# 데코레이터 찾기
sg run --pattern '@$DECORATOR' --lang python

# import 찾기
sg run --pattern 'from $MODULE import $NAME' --lang python
```

---

## 6. Claude Code 통합

### 6.1 방법 1: CLI 직접 사용 (권장)

Claude Code에서 Bash 명령으로 직접 호출:

```bash
# Claude Code에서 실행
sg run --pattern 'useState($INIT)' --lang tsx src/
```

**프롬프트 예시**:
```
"이 프로젝트에서 useState를 사용하는 모든 위치를 ast-grep으로 찾아줘"

"sg run --pattern '@Service' --lang java src/ 로 Service 클래스들을 찾아줘"
```

### 6.2 방법 2: CLAUDE.md 설정

프로젝트 CLAUDE.md에 ast-grep 사용 지침 추가:

```markdown
## 코드 검색 도구 우선순위

구조적 코드 검색이 필요한 경우, ast-grep(sg)을 우선 사용합니다:

### 언제 ast-grep을 사용하는가?
- 특정 함수/메서드 패턴 검색
- 코드 구조 분석 (useState, useEffect 등)
- 애노테이션/@데코레이터 검색
- 리팩토링 대상 식별

### 기본 명령
```bash
sg run --pattern '패턴' --lang 언어 경로
```

### 자주 사용하는 패턴
- React: `useState($INIT)`, `useEffect($$$)`
- Java: `@Service`, `@Transactional`
- 함수: `function $NAME($$$) { $$$ }`
```

### 6.3 방법 3: MCP 서버 (고급)

ast-grep MCP 서버를 통한 AI 통합:

```bash
# MCP 서버 설치
git clone https://github.com/ast-grep/ast-grep-mcp.git
cd ast-grep-mcp
uv sync
```

**MCP 도구**:
| 도구 | 설명 |
|------|------|
| `dump_syntax_tree` | AST 구조 시각화 |
| `test_match_code_rule` | 규칙 테스트 |
| `find_code` | 패턴 검색 |
| `find_code_by_rule` | YAML 규칙 검색 |

---

## 7. 고급 기능

### 7.1 코드 변환 (Rewrite)

```bash
# console.log → logger.info 변환
sg run \
  --pattern 'console.log($MSG)' \
  --rewrite 'logger.info($MSG)' \
  --lang js

# var → const 변환
sg run \
  --pattern 'var $NAME = $VALUE' \
  --rewrite 'const $NAME = $VALUE' \
  --lang js
```

### 7.2 YAML 규칙 파일

```yaml
# no-console.yaml
id: no-console-log
language: javascript
rule:
  pattern: console.log($MSG)
message: "프로덕션 코드에서 console.log 사용 금지"
severity: warning
fix: "logger.info($MSG)"
```

```bash
# 규칙 적용
sg scan --rule no-console.yaml src/
```

### 7.3 여러 규칙 조합

```yaml
# security-rules.yaml
id: no-eval
language: javascript
rule:
  any:
    - pattern: eval($CODE)
    - pattern: new Function($CODE)
message: "eval/Function 생성자 사용 금지 (보안 위험)"
severity: error
```

### 7.4 메타변수 조건

```yaml
# async-without-await.yaml
id: async-without-await
language: javascript
rule:
  pattern: async function $NAME($$$) { $$$ }
  not:
    has:
      pattern: await $EXPR
message: "async 함수에 await가 없습니다"
```

---

## 8. 실전 활용 사례

### 8.1 코드 품질 검사

```bash
# console.log 찾기
sg run --pattern 'console.log($$$)' --lang tsx src/

# debugger 문 찾기
sg run --pattern 'debugger' --lang js src/

# TODO 주석 찾기
sg run --pattern '// TODO: $MSG' --lang tsx src/

# 빈 catch 블록 찾기
sg run --pattern 'catch ($E) { }' --lang js src/
```

### 8.2 보안 취약점 탐지

```bash
# SQL 인젝션 가능성
sg run --pattern '$QUERY + $VAR' --lang java src/

# XSS 가능성
sg run --pattern 'dangerouslySetInnerHTML={{__html: $VAR}}' --lang tsx src/

# eval 사용
sg run --pattern 'eval($CODE)' --lang js src/
```

### 8.3 리팩토링 대상 식별

```bash
# 클래스 컴포넌트 찾기 (함수형으로 변환 대상)
sg run --pattern 'class $NAME extends Component { $$$ }' --lang tsx src/

# 레거시 생명주기 메서드
sg run --pattern 'componentWillMount() { $$$ }' --lang tsx src/

# 구형 state 업데이트
sg run --pattern 'this.setState($STATE)' --lang tsx src/
```

### 8.4 의존성 분석

```bash
# 특정 모듈 import 찾기
sg run --pattern "import $NAME from 'lodash'" --lang js src/

# 상대 경로 import 찾기
sg run --pattern "import $NAME from './$PATH'" --lang js src/
```

---

## 9. grep vs ast-grep 비교

### 9.1 검색 결과 차이

```javascript
// 샘플 코드
function test() {
  console.log("hello");  // 실제 호출
  // console.log("주석");  // 주석 내 텍스트
  const str = "console.log in string";  // 문자열 내 텍스트
}
```

| 검색 도구 | 결과 |
|----------|------|
| `grep console.log` | 3개 모두 매칭 |
| `sg --pattern 'console.log($M)'` | 실제 호출 1개만 매칭 |

### 9.2 사용 시나리오별 권장

| 시나리오 | 권장 도구 | 이유 |
|----------|----------|------|
| 단순 텍스트 검색 | grep/ripgrep | 빠르고 간단 |
| 코드 구조 검색 | ast-grep | AST 기반 정확한 매칭 |
| 함수/클래스 찾기 | ast-grep | 구문 구조 이해 |
| 리팩토링 대상 | ast-grep | 패턴 기반 변환 가능 |
| 로그 파일 검색 | grep | 코드가 아닌 텍스트 |

### 9.3 조합 사용

```bash
# 1단계: grep으로 빠른 필터링
grep -r "useState" src/ | wc -l

# 2단계: ast-grep으로 정확한 분석
sg run --pattern 'useState($INIT)' --lang tsx src/
```

---

## 요약

| 항목 | 내용 |
|------|------|
| **설치** | `brew install ast-grep` |
| **기본 명령** | `sg run --pattern '패턴' --lang 언어 경로` |
| **와일드카드** | `$NAME` (단일), `$$$` (다중) |
| **장점** | AST 기반 정확한 구조적 검색 |
| **Claude Code 통합** | CLI 직접 사용 또는 CLAUDE.md 설정 |
| **적합한 상황** | 코드 패턴 검색, 리팩토링, 품질 검사 |

---

## 참고 자료

- [ast-grep 공식 문서](https://ast-grep.github.io/)
- [ast-grep GitHub](https://github.com/ast-grep/ast-grep)
- [ast-grep MCP 서버](https://github.com/ast-grep/ast-grep-mcp)
- [언어 지원 목록](https://ast-grep.github.io/reference/languages.html)
- [패턴 문법 레퍼런스](https://ast-grep.github.io/reference/pattern-syntax.html)

---

> **변경 이력**
> - 2026-01-06: 최초 작성 (ast-grep 0.40.4 기준)
