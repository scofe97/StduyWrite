# 00. 환경 설정

NeoVim은 2026년 기준으로 Vim보다 선호되는 에디터입니다. Lua 기반의 직관적인 설정, 내장 LSP 클라이언트, 비동기 플러그인 아키텍처, tree-sitter 기반 구문 분석 등 현대적인 개발 환경을 위한 기능을 기본 제공합니다. 이 장에서는 NeoVim을 설치하고, 최소한의 설정으로 학습을 시작할 준비를 합니다.

---

## 목표

- [ ] 2026년 Vim 생태계(Neovim, Helix 등)의 선택지를 설명할 수 있다
- [ ] NeoVim을 설치하고 실행할 수 있다
- [ ] vimtutor로 기본 조작을 체험할 수 있다
- [ ] LazyVim 배포판으로 즉시 사용 가능한 환경을 구축할 수 있다

---

## 1. 왜 Neovim인가? (2026년 Vim 생태계 개요)

2026년 기준 모달 에디터 선택지는 다양하지만, IntelliJ + Claude Code 사용자에게는 **Neovim**이 최적이다. 상세 조사는 [INVESTIGATE.md](../INVESTIGATE.md) 참조.

| 에디터 | 편집 모델 | IntelliJ 통합 | Claude Code 통합 | 입문 난이도 | 판정 |
|--------|----------|--------------|-----------------|------------|------|
| **Neovim** | Action → Target | IdeaVim (동일 키) | 네이티브 플러그인 3종+ | 중간 (배포판 사용시 쉬움) | **추천** |
| Helix | Selection → Action | 없음 | 없음 | 가장 쉬움 | 차선 |
| Vim (Classic) | Action → Target | IdeaVim | 터미널만 | 높음 | 레거시 |
| Kakoune | Selection → Action | 없음 | 없음 | 중간 | 니치 |
| Zed (Vim mode) | Vim 에뮬레이션 | JetBrains 키맵 지원 | 자체 AI | 쉬움 | 별도 에디터 |

**핵심 선택 근거**: Vim 키바인딩을 익히면 IntelliJ(IdeaVim)와 터미널(Neovim) 양쪽에서 동일하게 사용할 수 있다. Helix는 입문이 더 쉽지만 Selection→Action 모델이라 IdeaVim과 키바인딩이 근본적으로 다르다.

---

## 2. NeoVim 설치

NeoVim은 대부분의 패키지 매니저에서 제공됩니다. 최신 버전(0.10 이상)을 설치하는 것을 권장합니다.

### macOS (Homebrew)

```bash
brew install neovim
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install neovim
```

### 설치 확인

```bash
nvim --version
# 출력 예: NVIM v0.10.3
```

버전이 0.10 미만이라면 최신 버전으로 업그레이드하는 것을 권장합니다. LSP, tree-sitter 등 최신 기능을 활용하려면 최소 0.9 이상이 필요합니다.

---

## 3. 왜 NeoVim인가? (상세)

Vim은 여전히 강력한 에디터이지만, NeoVim은 다음과 같은 이유로 현대적인 개발 환경에 더 적합합니다.

### Lua 기반 설정 (init.lua)

Vim의 VimScript는 학습 곡선이 가파르고 가독성이 떨어집니다. NeoVim은 Lua를 공식 설정 언어로 채택하여 직관적이고 강력한 설정이 가능합니다.

```lua
-- init.lua 예시
vim.opt.number = true
vim.opt.relativenumber = true
```

VimScript보다 간결하고, Lua의 풍부한 생태계를 활용할 수 있습니다.

### 내장 LSP 클라이언트

NeoVim은 LSP(Language Server Protocol) 클라이언트를 기본 내장하여 외부 플러그인 없이도 자동완성, 정의 이동, 리팩토링 등 IDE급 기능을 사용할 수 있습니다. Vim은 CoC, ALE 같은 무거운 플러그인이 필요합니다.

### tree-sitter 기반 구문 분석

NeoVim은 tree-sitter를 통해 정확하고 빠른 구문 강조, 코드 접기, 텍스트 객체를 지원합니다. 정규 표현식 기반 하이라이팅보다 월등히 정확합니다.

### 비동기 플러그인 아키텍처

NeoVim은 처음부터 비동기 설계로 만들어져 플러그인이 에디터를 멈추지 않습니다. Vim은 버전 8부터 비동기를 지원하지만, NeoVim이 더 일관성 있고 안정적입니다.

### 활발한 커뮤니티

2026년 현재, 대부분의 최신 Vim 플러그인은 NeoVim을 주 타겟으로 개발됩니다. Telescope, nvim-cmp, lualine 등 현대적인 플러그인 생태계는 NeoVim 중심입니다.

---

## 4. 최소 설정 (바닐라 Neovim)

NeoVim 설정 파일은 `~/.config/nvim/init.lua`에 위치합니다. 학습을 위해 최소한의 설정만 추가합니다.

### 설정 디렉토리 생성

```bash
mkdir -p ~/.config/nvim
```

### init.lua 생성

다음 내용으로 `~/.config/nvim/init.lua` 파일을 생성합니다.

```bash
cat > ~/.config/nvim/init.lua << 'EOF'
-- 줄 번호 표시
vim.opt.number = true

-- 상대 줄 번호 (상대적 이동에 유용)
vim.opt.relativenumber = true

-- 시스템 클립보드와 통합
vim.opt.clipboard = "unnamedplus"

-- 마우스 지원 (학습 초기에는 유용)
vim.opt.mouse = "a"

-- 들여쓰기 설정
vim.opt.tabstop = 2
vim.opt.shiftwidth = 2
vim.opt.expandtab = true

-- 검색 설정
vim.opt.ignorecase = true  -- 대소문자 무시
vim.opt.smartcase = true   -- 대문자 포함 시 대소문자 구분

-- 하이라이트 검색 결과
vim.opt.hlsearch = true
vim.opt.incsearch = true

-- 상태바 항상 표시
vim.opt.laststatus = 2
EOF
```

### 설정 확인

```bash
# init.lua 파일 확인
cat ~/.config/nvim/init.lua

# NeoVim 실행
nvim
```

NeoVim을 실행하면 줄 번호가 표시되고 기본 설정이 적용된 상태로 시작됩니다.

---

## 5. LazyVim 배포판 (추천 빠른 시작)

바닐라 Neovim 설정이 복잡하다면 **LazyVim 배포판**으로 즉시 IDE급 환경을 구축할 수 있다. LazyVim은 lazy.nvim 패키지 매니저 위에 80+ 플러그인이 사전 구성된 배포판이다.

### LazyVim 설치

```bash
# 기존 설정 백업 (있을 경우)
mv ~/.config/nvim{,.bak}
mv ~/.local/share/nvim{,.bak}
mv ~/.local/state/nvim{,.bak}
mv ~/.cache/nvim{,.bak}

# LazyVim starter 클론
git clone https://github.com/LazyVim/starter ~/.config/nvim

# .git 제거 (자체 설정 관리를 위해)
rm -rf ~/.config/nvim/.git

# 실행 → 자동으로 플러그인 설치
nvim
```

### LazyVim이 제공하는 것

| 기능 | 포함 플러그인 | 수동 설정 필요 여부 |
|------|-------------|-------------------|
| 퍼지 파인더 | Telescope | 즉시 사용 |
| 파일 탐색기 | neo-tree | 즉시 사용 |
| LSP | nvim-lspconfig + mason | 즉시 사용 |
| 자동완성 | nvim-cmp | 즉시 사용 |
| 구문 분석 | Treesitter | 즉시 사용 |
| Git 통합 | gitsigns + lazygit | 즉시 사용 |
| 키바인딩 가이드 | which-key | 즉시 사용 |

### 바닐라 vs LazyVim 선택 기준

- **LazyVim**: "일단 쓰면서 배우겠다" → 이 커리큘럼의 Phase 3 (Ch10~11) 내용이 이미 구성됨
- **바닐라 + 직접 설정**: "내부를 이해하며 배우겠다" → Ch10에서 하나씩 플러그인을 추가

둘 다 Vim 모션 학습(Ch01~08)에는 영향 없으므로, 터미널 에디터 환경이 필요한 시점(Phase 3)에 선택하면 된다.

---

## 6. vimtutor 체험

vimtutor는 Vim의 기본 조작을 대화형으로 학습할 수 있는 내장 튜토리얼입니다. 30분 정도 소요되며, Vim의 핵심 개념을 빠르게 파악할 수 있습니다.

```bash
nvim +Tutor
```

위 명령을 실행하면 NeoVim이 튜토리얼 모드로 시작됩니다. 다음 내용을 다룹니다.

| 레슨 | 내용 |
|------|------|
| Lesson 1 | 이동(hjkl), 종료(`:q`), 삭제(`x`, `dd`) |
| Lesson 2 | 삭제 명령(`dw`, `d$`), 연산자와 모션 |
| Lesson 3 | Put(`p`), Replace(`r`), Change(`c`) |
| Lesson 4 | 검색(`/`), 치환(`:s`) |
| Lesson 5 | 외부 명령(`:!`), 파일 저장(`:w`) |
| Lesson 6 | Insert 모드(`i`, `a`, `o`), 복사(`y`) |
| Lesson 7 | 도움말(`:help`), 설정 |

vimtutor는 건너뛰지 말고 반드시 한 번 완료하는 것을 권장합니다. 이후 학습에서 다루는 개념의 기초를 다집니다.

---

## 7. Vim vs NeoVim 비교

| 항목 | Vim | NeoVim |
|------|-----|--------|
| 설정 언어 | VimScript (.vimrc) | Lua (init.lua) + VimScript 호환 |
| LSP 지원 | 외부 플러그인 필요 (CoC, ALE) | 내장 LSP 클라이언트 (`vim.lsp`) |
| 구문 분석 | 정규 표현식 기반 | tree-sitter 기반 (정확도↑) |
| 비동기 | v8부터 지원 (제한적) | 처음부터 비동기 설계 |
| 플러그인 생태계 | 전통적 (Vundle, Pathogen) | 현대적 (lazy.nvim, packer.nvim) |
| 커뮤니티 방향 | 보수적, 안정성 중시 | 진보적, 최신 기능 중시 |
| 사용 명령어 | `vim` | `nvim` |

두 에디터 모두 강력하지만, 2026년 기준으로 새로 시작한다면 NeoVim을 권장합니다. Vim의 모든 기능을 지원하면서 더 현대적인 개발 환경을 제공합니다.

---

## 체크포인트

다음 질문에 자신의 언어로 답변할 수 있는지 확인하세요.

### 1. NeoVim의 핵심 장점 3가지를 설명하세요

<details>
<summary>모범 답안 확인</summary>

NeoVim의 핵심 장점은 다음과 같습니다. 첫째, Lua 기반 설정으로 VimScript보다 직관적이고 강력한 설정이 가능합니다. 둘째, 내장 LSP 클라이언트로 외부 플러그인 없이 자동완성, 정의 이동 등 IDE급 기능을 사용할 수 있습니다. 셋째, tree-sitter를 통해 정규 표현식 기반보다 정확한 구문 분석과 하이라이팅을 제공합니다. 이 세 가지가 NeoVim을 현대적인 개발 환경에 적합하게 만드는 핵심 요소입니다.

</details>

### 2. init.lua와 .vimrc의 차이는?

<details>
<summary>모범 답안 확인</summary>

`.vimrc`는 Vim의 전통적인 설정 파일로 VimScript 언어를 사용합니다. 위치는 `~/.vimrc`입니다. 반면 `init.lua`는 NeoVim의 현대적 설정 파일로 Lua 언어를 사용하며 `~/.config/nvim/init.lua`에 위치합니다. Lua는 VimScript보다 가독성이 좋고 강력한 프로그래밍 기능을 제공합니다. NeoVim은 하위 호환성을 위해 `init.vim`(VimScript)도 지원하지만, 공식적으로는 `init.lua` 사용을 권장합니다.

</details>

### 3. vimtutor에서 가장 인상적이었던 기능은?

<details>
<summary>답변 예시</summary>

이 질문은 개인적인 경험을 묻는 것이므로 정답이 없습니다. 예를 들어, "연산자와 모션의 조합(예: `d2w` - 2개 단어 삭제)이 인상적이었습니다. 하나의 문법으로 무한한 조합을 만들 수 있다는 점에서 Vim의 철학을 이해할 수 있었습니다" 같은 답변이 가능합니다.

</details>

---

다음: [01. 모드 이해](./01-modes.md)
