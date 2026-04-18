# 12. IdeaVim - IntelliJ에서 Vim 사용하기

IntelliJ IDEA는 Java/Kotlin 개발에서 가장 강력한 IDE이며, IdeaVim 플러그인을 통해 Vim의 모달 편집을 IntelliJ 안에서 사용할 수 있습니다. NeoVim에서 배운 모션과 연산자가 그대로 동작하면서, IntelliJ의 리팩토링, 디버거, 데이터베이스 도구 등 IDE 고유 기능도 함께 사용할 수 있습니다. 이 챕터는 Ch04(편집 필수기)까지 학습한 후 바로 시작할 수 있는 병렬 학습 경로입니다.

---

## 목표

- [ ] IdeaVim을 설치하고 .ideavimrc를 설정할 수 있다
- [ ] IntelliJ Action을 Vim 단축키에 매핑할 수 있다
- [ ] Vim 모션 + IntelliJ 리팩토링을 조합하여 사용할 수 있다

---

## 1. IdeaVim 설치 및 기본 설정

IdeaVim은 IntelliJ IDEA 플랫폼(IDEA, PyCharm, WebStorm, Android Studio 등) 전체에서 동작하는 Vim 에뮬레이션 플러그인입니다. NeoVim처럼 완벽한 Vim은 아니지만, 모달 편집의 핵심 기능은 모두 지원하며 IntelliJ의 강력한 기능과 결합할 수 있습니다.

### 설치 방법

1. IntelliJ IDEA 실행
2. **Preferences**(macOS) 또는 **Settings**(Windows/Linux) 열기 (`Cmd+,` / `Ctrl+Alt+S`)
3. **Plugins** 메뉴로 이동
4. **Marketplace** 탭에서 "IdeaVim" 검색
5. **Install** 클릭 후 IDE 재시작

재시작 후 모든 에디터가 Vim 모드로 전환됩니다. 기본 모드는 Normal 모드이며, 텍스트 입력을 위해서는 `i`, `a`, `o` 등으로 Insert 모드에 진입해야 합니다.

### .ideavimrc 파일 생성

NeoVim의 `init.lua` 또는 `.vimrc`처럼, IdeaVim은 `~/.ideavimrc` 파일에서 설정을 읽습니다. 이 파일은 Vimscript 문법을 사용합니다(Lua 아님).

```bash
# .ideavimrc 생성
touch ~/.ideavimrc
```

### 기본 설정

```vim
" practice/configs/.ideavimrc

" 기본 옵션
set number                " 라인 번호 표시
set relativenumber        " 상대 라인 번호
set ignorecase            " 검색 시 대소문자 무시
set smartcase             " 대문자 포함 시 대소문자 구분
set incsearch             " 점진적 검색
set hlsearch              " 검색 결과 하이라이트
set scrolloff=5           " 커서 위아래 5줄 여유
set clipboard+=unnamed    " 시스템 클립보드 연동
set clipboard+=ideaput    " IntelliJ 붙여넣기 사용

" Leader 키 설정
let mapleader = " "

" Esc 대체 (jk로 Normal 모드 복귀)
inoremap jk <Esc>

" 검색 하이라이트 제거
nnoremap <leader>h :nohlsearch<CR>
```

`.ideavimrc`를 수정한 후에는 **Tools → Vim → Reload .ideavimrc** 또는 `:source ~/.ideavimrc`로 재로드할 수 있습니다.

---

## 2. .ideavimrc 핵심 설정

IdeaVim은 일부 Vim 플러그인 기능을 내장 에뮬레이션으로 제공합니다. 또한 IntelliJ의 동작을 Vim 친화적으로 만드는 옵션들이 있습니다.

### IntelliJ 통합 옵션

```vim
" IntelliJ 스마트 줄 합치기 (J 명령어)
set ideajoin

" 리팩토링 후 모드 유지 (Normal 모드로 돌아감)
set idearefactormode=keep

" Visual 모드 선택 시 IntelliJ 선택과 동기화
set ideamarks
```

`set ideajoin`을 활성화하면 `J` 명령어가 단순히 줄을 합치는 것이 아니라, IntelliJ의 "Join Lines" 기능을 사용합니다. 예를 들어 Java에서 문자열을 합치거나 if 문의 중괄호를 제거하는 등 스마트한 합치기가 가능합니다.

### which-key 에뮬레이션

```vim
" which-key 플러그인 에뮬레이션
set which-key
set notimeout
```

이 설정을 활성화하면 `<leader>` 키를 누른 후 잠시 기다리면 사용 가능한 단축키 목록이 팝업으로 표시됩니다. 단축키를 외우지 않아도 탐색할 수 있습니다.

### 클립보드 통합

```vim
" 시스템 클립보드 연동
set clipboard+=unnamed      " macOS/Linux
set clipboard+=unnamedplus  " Windows

" IntelliJ 붙여넣기 로직 사용 (import 자동 추가 등)
set clipboard+=ideaput
```

`ideaput`을 설정하면 `p`로 붙여넣을 때 IntelliJ의 스마트 붙여넣기가 동작합니다. 예를 들어 클래스 이름을 붙여넣으면 자동으로 import 문이 추가됩니다.

---

## 3. IntelliJ Action 매핑

IdeaVim의 가장 강력한 기능은 IntelliJ의 모든 기능(Action)을 Vim 단축키에 매핑할 수 있다는 점입니다. IntelliJ는 수천 개의 Action을 제공하며, `:actionlist` 명령으로 목록을 볼 수 있습니다.

### Action 매핑 문법

```vim
" 문법: map {mode} {key} <Action>({ActionName})
nnoremap <leader>rn <Action>(RenameElement)
```

- `{mode}`: `nnoremap`, `vnoremap`, `inoremap` 등
- `{key}`: 매핑할 키 조합
- `<Action>(ActionName)`: IntelliJ Action 이름

### Action 찾기

`:actionlist` 명령으로 검색할 수 있습니다.

```vim
" 모든 Action 보기
:actionlist

" "refactor" 키워드로 검색
:actionlist refactor

" "goto" 키워드로 검색
:actionlist goto
```

또는 IntelliJ의 **Find Action** (`Cmd+Shift+A` / `Ctrl+Shift+A`)을 사용해서 기능을 실행한 후, 그 기능의 Action 이름을 `.ideavimrc`에 매핑할 수 있습니다.

### 필수 매핑

```vim
" ========== 네비게이션 ==========
" 정의로 이동
nnoremap gd <Action>(GotoDeclaration)

" 구현으로 이동
nnoremap gi <Action>(GotoImplementation)

" 타입 정의로 이동
nnoremap gy <Action>(GotoTypeDeclaration)

" 참조 찾기
nnoremap gr <Action>(FindUsages)

" 슈퍼클래스/인터페이스로 이동
nnoremap gs <Action>(GotoSuperMethod)

" 테스트로 이동/생성
nnoremap gt <Action>(GotoTest)

" 최근 파일
nnoremap <leader>e <Action>(RecentFiles)

" 파일 찾기
nnoremap <leader>ff <Action>(GotoFile)

" 텍스트 검색
nnoremap <leader>fg <Action>(FindInPath)

" 심볼 찾기 (함수, 클래스 등)
nnoremap <leader>fs <Action>(GotoSymbol)

" ========== 리팩토링 ==========
" 이름 변경
nnoremap <leader>rn <Action>(RenameElement)

" 리팩토링 메뉴
nnoremap <leader>rr <Action>(Refactorings.QuickListPopupAction)

" 메서드 추출
vnoremap <leader>rm <Action>(ExtractMethod)

" 변수 추출
vnoremap <leader>rv <Action>(IntroduceVariable)

" 인라인 (변수/메서드 인라인화)
nnoremap <leader>ri <Action>(Inline)

" ========== 코드 ==========
" 문서 보기
nnoremap K <Action>(QuickJavaDoc)

" 빠른 수정 (Quick Fix)
nnoremap <leader>ca <Action>(ShowIntentionActions)

" 코드 생성 (getter/setter, 생성자 등)
nnoremap <leader>cg <Action>(Generate)

" 코드 포맷
nnoremap <leader>cf <Action>(ReformatCode)
vnoremap <leader>cf <Action>(ReformatCode)

" Import 최적화
nnoremap <leader>co <Action>(OptimizeImports)

" ========== 진단 ==========
" 다음/이전 오류
nnoremap ]d <Action>(GotoNextError)
nnoremap [d <Action>(GotoPreviousError)

" 오류 설명
nnoremap <leader>e <Action>(ShowErrorDescription)

" ========== 윈도우/도구 ==========
" 프로젝트 도구창 토글
nnoremap <leader>1 <Action>(ActivateProjectToolWindow)

" 터미널 토글
nnoremap <leader>t <Action>(ActivateTerminalToolWindow)

" 실행 도구창
nnoremap <leader>4 <Action>(ActivateRunToolWindow)

" Git 도구창
nnoremap <leader>9 <Action>(ActivateVersionControlToolWindow)

" 모든 도구창 숨기기
nnoremap <leader>z <Action>(HideAllWindows)
```

---

## 4. 에뮬레이트 플러그인

IdeaVim은 인기 있는 Vim 플러그인의 기능을 내장으로 제공합니다. `set {plugin-name}` 형태로 활성화할 수 있습니다.

### 지원하는 플러그인

```vim
" vim-surround: ys, cs, ds 명령어
set surround

" vim-commentary: gc 명령어
set commentary

" NERDTree: 파일 탐색 (IntelliJ의 Project 도구창과 통합)
set NERDTree

" multiple-cursors: Ctrl+N으로 다중 커서
set multiple-cursors

" vim-highlightedyank: 복사한 영역 하이라이트
set highlightedyank

" argtextobj: 함수 인자를 텍스트 오브젝트로 (daa, cia)
set argtextobj

" vim-indent-object: 들여쓰기 블록을 텍스트 오브젝트로 (dii, dai)
set textobj-indent

" vim-sneak: 두 글자로 점프 (s{char}{char})
set sneak
```

### surround 사용 예시

```java
// 커서가 여기에 있을 때
String message = "Hello";

// ysiw" 실행 (surround inner word with ")
String message = ""Hello"";

// cs"' 실행 (change surrounding " to ')
String message = 'Hello';

// ds' 실행 (delete surrounding ')
String message = Hello;
```

### commentary 사용 예시

```java
// gcc로 현재 줄 주석 토글
int x = 10; // → // int x = 10;

// Visual 모드로 3줄 선택 후 gc
public void method() {
    doSomething();
    doAnother();
}

// 주석 처리 결과
// public void method() {
//     doSomething();
//     doAnother();
// }
```

---

## 5. 디버깅과 실행 매핑

IntelliJ의 디버거는 매우 강력하며, Vim 단축키로 제어할 수 있습니다.

```vim
" ========== 실행/디버그 ==========
" 현재 파일 실행
nnoremap <leader>rr <Action>(Run)

" 현재 파일 디버그
nnoremap <leader>rd <Action>(Debug)

" 중단점 토글
nnoremap <leader>db <Action>(ToggleLineBreakpoint)

" 조건부 중단점
nnoremap <leader>dB <Action>(ToggleBreakpointEnabled)

" 모든 중단점 보기
nnoremap <leader>dv <Action>(ViewBreakpoints)

" 디버깅 중 명령어
nnoremap <leader>dc <Action>(Resume)           " 계속 실행
nnoremap <leader>dn <Action>(StepOver)         " 다음 줄
nnoremap <leader>di <Action>(StepInto)         " 함수 안으로
nnoremap <leader>do <Action>(StepOut)          " 함수 밖으로
nnoremap <leader>de <Action>(EvaluateExpression) " 표현식 평가
```

### 디버깅 워크플로우

1. 중단하고 싶은 줄에서 `<leader>db` (중단점 토글)
2. `<leader>rd`로 디버그 모드 실행
3. 중단점에서 멈추면:
   - `<leader>dn`: 다음 줄로 (Step Over)
   - `<leader>di`: 함수 안으로 (Step Into)
   - `<leader>de`: 변수 값 확인
   - `<leader>dc`: 다음 중단점까지 실행

---

## 6. NeoVim vs IdeaVim 비교

두 도구는 서로 다른 장점을 가지고 있으며, 상황에 따라 선택하거나 함께 사용할 수 있습니다.

| 비교 항목 | NeoVim | IdeaVim |
|-----------|--------|---------|
| **Vim 완성도** | 완벽한 Vim | 80% 정도 (일부 기능 제한) |
| **플러그인 생태계** | 방대함 (Lua/Vimscript) | 제한적 (에뮬레이션만) |
| **속도** | 매우 빠름 | 무거움 (IDE 전체 로드) |
| **리팩토링** | 기본적 수준 (LSP) | 매우 강력 (언어별 최적화) |
| **디버거** | DAP 설정 필요 | 통합 디버거 (최고 수준) |
| **Java/Kotlin** | 기본 지원 | 최적화됨 (Spring, Gradle 등) |
| **터미널 통합** | 완벽 (tmux 등) | 제한적 |
| **설정 복잡도** | 높음 (직접 설정) | 낮음 (기본값 우수) |
| **기업 환경** | 팀 설득 필요할 수 있음 | 일반적으로 허용됨 |

### 선택 기준

**NeoVim을 선택하는 경우:**
- 터미널 중심 워크플로우
- 빠른 응답 속도가 중요
- 스크립트, 설정 파일 편집
- 원격 서버 작업
- 다양한 언어를 오가며 작업 (Go, TypeScript, Python 등)

**IdeaVim을 선택하는 경우:**
- Java/Kotlin 주력 개발
- 복잡한 리팩토링이 잦음 (Extract Interface, Change Signature 등)
- 디버깅이 중요함
- 데이터베이스 도구, HTTP 클라이언트 등 IDE 통합 도구 사용
- 팀이 IntelliJ를 표준으로 사용

### 결론: 양쪽 모두 사용

많은 개발자들이 다음과 같이 사용합니다.

- **Java/Kotlin 프로젝트**: IdeaVim (IntelliJ)
- **설정 파일, 스크립트**: NeoVim
- **빠른 편집**: NeoVim
- **복잡한 리팩토링**: IdeaVim

Vim 모션은 양쪽에서 모두 동일하게 동작하므로, 하나를 배우면 두 도구를 모두 효율적으로 사용할 수 있습니다.

---

## 실습

1. **IdeaVim 설치 및 기본 설정**
   - IntelliJ IDEA에서 IdeaVim 플러그인 설치
   - `~/.ideavimrc` 파일 생성 및 기본 설정 추가
   - `:source ~/.ideavimrc`로 설정 적용

2. **필수 매핑 추가**
   - `practice/configs/.ideavimrc` 참조
   - 네비게이션, 리팩토링, 디버깅 매핑 추가
   - `set surround`, `set commentary` 활성화

3. **Java 프로젝트에서 테스트**
   ```java
   public class Calculator {
       public int add(int a, int b) {
           return a + b;
       }
   }
   ```
   - `add` 메서드에서 `gr` → 사용처 찾기
   - `add` 메서드명에서 `<leader>rn` → 이름 변경
   - `a + b`를 Visual 선택 후 `<leader>rv` → 변수 추출
   - `gc`로 줄 주석 토글

4. **디버깅 테스트**
   - `return` 줄에서 `<leader>db` → 중단점 설정
   - `<leader>rd`로 디버그 실행
   - `<leader>dn`, `<leader>di`로 단계 실행

---

## 명령어 요약

| 명령어/단축키 | 기능 |
|---------------|------|
| `:source ~/.ideavimrc` | 설정 파일 재로드 |
| `:actionlist` | IntelliJ Action 목록 |
| `gd` | 정의로 이동 |
| `gr` | 참조 찾기 |
| `gi` | 구현으로 이동 |
| `K` | 문서 보기 |
| `<leader>rn` | 이름 변경 |
| `<leader>rr` | 리팩토링 메뉴 |
| `<leader>ca` | 빠른 수정 |
| `<leader>db` | 중단점 토글 |
| `<leader>rd` | 디버그 실행 |
| `<leader>ff` | 파일 찾기 |
| `<leader>fg` | 텍스트 검색 |
| `ys`, `cs`, `ds` | surround 명령어 (set surround 필요) |
| `gc` | 주석 토글 (set commentary 필요) |

---

## 체크포인트

<details>
<summary><strong>1. &lt;Action&gt;(ActionName) 문법은 무엇을 의미하나요?</strong></summary>

`<Action>(ActionName)`은 IdeaVim에서 IntelliJ IDEA의 기능을 호출하는 특수 문법입니다. IntelliJ는 모든 기능을 "Action"이라는 단위로 관리하며, 각 Action은 고유한 이름을 가지고 있습니다. 예를 들어 "이름 변경" 기능은 `RenameElement`라는 Action입니다. `:actionlist` 명령으로 사용 가능한 모든 Action을 볼 수 있으며, 이를 Vim 단축키에 매핑하면 마우스나 메뉴 없이 IntelliJ의 강력한 기능을 사용할 수 있습니다. 이는 IdeaVim이 단순한 Vim 에뮬레이터가 아니라 IntelliJ와 깊이 통합된 도구임을 보여줍니다.
</details>

<details>
<summary><strong>2. set surround를 활성화하면 어떤 기능을 쓸 수 있나요?</strong></summary>

`set surround`는 vim-surround 플러그인의 기능을 에뮬레이트합니다. 이를 통해 괄호, 따옴표, 태그 등으로 텍스트를 감싸거나(surround), 변경하거나(change), 제거하는(delete) 작업을 빠르게 할 수 있습니다. 주요 명령어는 `ys{motion}{char}`(추가), `cs{old}{new}`(변경), `ds{char}`(제거)입니다. 예를 들어 `ysiw"`는 커서 아래 단어를 큰따옴표로 감싸고, `cs"'`는 큰따옴표를 작은따옴표로 바꾸며, `ds"`는 큰따옴표를 제거합니다. HTML 태그에도 사용할 수 있어 `cst<div>`는 현재 태그를 div로 변경합니다.
</details>

<details>
<summary><strong>3. NeoVim과 IdeaVim 중 어느 것을 먼저 사용해야 하나요?</strong></summary>

**순서는 중요하지 않습니다.** 두 도구 모두 Vim의 모달 편집 개념을 공유하므로, 하나를 배우면 다른 하나도 쉽게 사용할 수 있습니다. 선택 기준은 현재 작업 환경입니다. Java/Kotlin 프로젝트를 주로 다루고 IntelliJ를 이미 사용 중이라면 IdeaVim부터 시작하는 것이 학습 곡선이 완만합니다. 반대로 터미널 작업이 많거나 다양한 언어를 다룬다면 NeoVim부터 시작하는 것이 좋습니다. 많은 개발자들은 결국 두 도구를 모두 사용하게 되며, 상황에 따라 전환합니다. 중요한 것은 Vim의 언어(motion + operator)를 익히는 것이며, 이는 어느 도구에서나 동일합니다.
</details>

---
다음: [13. Claude Code 통합](./13-claude-code.md)
