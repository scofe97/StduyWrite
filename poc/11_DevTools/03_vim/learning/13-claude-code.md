# 13. Claude Code + NeoVim 통합

Claude Code는 터미널 기반 AI 코딩 도구이고, NeoVim도 터미널 기반 에디터입니다. 이 두 도구를 tmux와 함께 조합하면, 마우스 없이 AI 지원 개발 환경을 구축할 수 있습니다. Claude Code가 코드를 생성하면 NeoVim에서 바로 확인하고 수정하는 워크플로우는 터미널 중심 개발의 완성형입니다.

---

## 목표

- [ ] Claude Code와 NeoVim을 tmux에서 함께 사용할 수 있다
- [ ] $EDITOR 설정으로 Claude Code의 에디터를 NeoVim으로 지정할 수 있다
- [ ] NeoVim 터미널 모드를 활용할 수 있다

---

## 1. tmux + NeoVim + Claude Code 레이아웃

터미널 멀티플렉서인 tmux를 사용하면 하나의 터미널 창을 여러 패널(pane)로 분할할 수 있습니다. NeoVim과 Claude Code를 나란히 배치하면, 코드 편집과 AI 상호작용을 동시에 진행할 수 있습니다.

### 권장 레이아웃

```
┌─────────────────────────────────┐
│        NeoVim (70%)             │
│  - 코드 편집                     │
│  - LSP 진단                      │
│  - 파일 탐색                     │
├─────────────────────────────────┤
│     Claude Code (30%)           │
│  - AI 질문                       │
│  - 코드 생성                     │
│  - 문서 검색                     │
└─────────────────────────────────┘
```

수평 분할(상하)이 수직 분할(좌우)보다 유리한 이유는 코드와 AI 출력 모두 세로로 긴 형태이기 때문입니다.

### tmux 레이아웃 구성

```bash
# 새 세션 생성
tmux new-session -s dev

# 상단 패널에서 NeoVim 실행
nvim

# 하단 패널 생성 (70%:30% 비율)
# Ctrl+b " (수평 분할)
# Ctrl+b :resize-pane -D 10 (하단 패널 축소)

# 하단 패널에서 Claude Code 실행
claude

# 패널 이동: Ctrl+b ↑↓
```

### tmux 스크립트로 자동화

```bash
#!/bin/bash
# ~/scripts/dev-session.sh

SESSION="dev"

# 세션이 이미 있으면 attach
tmux has-session -t $SESSION 2>/dev/null
if [ $? == 0 ]; then
  tmux attach -t $SESSION
  exit 0
fi

# 새 세션 생성 및 레이아웃 설정
tmux new-session -d -s $SESSION

# 첫 번째 윈도우 설정
tmux rename-window -t $SESSION:1 'code'
tmux send-keys -t $SESSION:1 'nvim' C-m

# 패널 분할 (30% 크기)
tmux split-window -v -p 30 -t $SESSION:1
tmux send-keys -t $SESSION:1.2 'claude' C-m

# 첫 번째 패널로 포커스
tmux select-pane -t $SESSION:1.1

# 세션 attach
tmux attach -t $SESSION
```

```bash
chmod +x ~/scripts/dev-session.sh
~/scripts/dev-session.sh
```

### 01_tmux 프로젝트 참조

더 고급 tmux 워크플로우는 `runners-high/poc/11_DevTools/01_tmux/` 프로젝트를 참고하세요. 해당 프로젝트에서는 다음을 다룹니다:

- 세션/윈도우/패널 관리
- 키 바인딩 커스터마이징
- 플러그인 (tmux-resurrect, tmux-continuum)
- 프로젝트별 레이아웃 자동화

---

## 2. $EDITOR 설정

`$EDITOR` 환경변수는 유닉스 시스템에서 "기본 텍스트 에디터"를 지정하는 표준 방법입니다. Claude Code, git, crontab 등 많은 도구가 이 변수를 참조하여 에디터를 실행합니다.

### 설정 방법

```bash
# ~/.zshrc 또는 ~/.bashrc에 추가
export EDITOR="nvim"

# 변경사항 적용
source ~/.zshrc
```

### Claude Code와의 통합

Claude Code는 파일 편집이 필요할 때 `$EDITOR`를 실행합니다. NeoVim으로 설정하면 다음과 같은 상황에서 자동으로 NeoVim이 열립니다:

- Claude가 생성한 코드를 수정하도록 요청할 때
- diff를 확인하고 수정할 때
- 긴 프롬프트를 작성할 때

### git commit도 NeoVim으로

```bash
# git commit 메시지 작성 시에도 NeoVim 사용
git commit
# → NeoVim이 열리고 커밋 메시지 작성
```

NeoVim에서 커밋 메시지를 작성할 때 유용한 설정:

```lua
-- practice/configs/nvim/init.lua에 추가
vim.api.nvim_create_autocmd("FileType", {
  pattern = "gitcommit",
  callback = function()
    -- 첫 줄에서 Insert 모드로 시작
    vim.cmd("startinsert")
    -- 72자 제한 표시
    vim.opt_local.colorcolumn = "72"
    -- 스펠 체크 활성화
    vim.opt_local.spell = true
  end,
})
```

---

## 3. claudecode.nvim - Neovim 네이티브 Claude Code 통합

2026년 현재, Neovim에서 Claude Code CLI를 네이티브로 연동하는 커뮤니티 플러그인이 여러 종 존재한다. Anthropic이 공식으로 VSCode와 JetBrains만 지원했기 때문에, 커뮤니티가 확장 프로토콜을 리버스 엔지니어링하여 만들었다.

### 주요 플러그인 3종 비교

| 플러그인 | 특징 | 의존성 | 프로토콜 호환 |
|---------|------|--------|-------------|
| **[coder/claudecode.nvim](https://github.com/coder/claudecode.nvim)** | 순수 Lua, 의존성 0 | 없음 (vim.loop만 사용) | VSCode 확장 100% 호환 |
| [greggh/claude-code.nvim](https://github.com/greggh/claude-code.nvim) | 분할 터미널 기반, 간편 설정 | 없음 | 터미널 통합 |
| [avifenesh/claucode.nvim](https://github.com/avifenesh/claucode.nvim) | 에디터 ↔ CLI 브릿지 | 없음 | 브릿지 방식 |

### coder/claudecode.nvim 설치 (추천)

```lua
-- lazy.nvim 플러그인 스펙 (LazyVim 사용자는 lua/plugins/claude.lua에 추가)
return {
  "coder/claudecode.nvim",
  config = true,
  keys = {
    { "<leader>ac", "<cmd>ClaudeCode<CR>", desc = "Claude Code 토글" },
    { "<leader>aa", "<cmd>ClaudeCodeAdd<CR>", desc = "파일을 Claude 컨텍스트에 추가" },
    { "<leader>aa", "<cmd>ClaudeCodeAdd<CR>", mode = "v", desc = "선택 영역을 Claude에 추가" },
  },
}
```

### 주요 명령어

```vim
:ClaudeCode           " Claude Code를 분할 터미널에서 열기/닫기
:ClaudeCodeAdd        " 현재 파일을 Claude 컨텍스트에 추가
                      " Visual 모드에서는 선택 영역만 추가
```

### 워크플로우: Neovim 안에서 Claude Code 사용

```
┌─────────────────────────────────┐
│  NeoVim: src/api/user.ts        │ ← 코드 편집 + LSP 진단
│                                 │
│  function getUser(id: string) { │
│    // Claude가 수정한 코드가     │
│    // 실시간으로 반영됨          │
│  }                              │
├─────────────────────────────────┤
│  Claude Code (claudecode.nvim)  │ ← :ClaudeCode로 토글
│  > "getUser 함수에 Zod 검증 추가│
│     해줘"                       │
│  Claude가 파일을 수정하면       │
│  상단 버퍼에 즉시 반영          │
└─────────────────────────────────┘
```

핵심 장점: Claude Code가 파일을 수정하면 Neovim 버퍼에 **즉시 반영**되어, 별도로 `:e`로 다시 열 필요가 없다.

### greggh/claude-code.nvim 설치 (대안)

```lua
return {
  "greggh/claude-code.nvim",
  dependencies = { "nvim-lua/plenary.nvim" },
  config = true,
  keys = {
    { "<leader>ac", "<cmd>ClaudeCode<CR>", desc = "Claude Code 토글" },
  },
}
```

### Ghostty 3-pane 워크플로우 (대안)

플러그인 대신 터미널 자체를 3-pane으로 구성하는 방법도 있다. Ghostty 터미널에서 Neovim, Claude Code, 일반 터미널을 나란히 배치한다.

```
┌──────────────┬──────────────┐
│              │ Claude Code  │
│   NeoVim     │              │
│              ├──────────────┤
│              │  Terminal    │
└──────────────┴──────────────┘
```

- [Neovim + Claude Code + Ghostty 통합 가이드](https://danielmiessler.com/blog/claude-code-neovim-ghostty-integration)
- [Replacing Cursor With Neovim and Claude Code](https://danielmiessler.com/blog/replacing-cursor-with-neovim-claude-code)
- [Configuring Neovim for Claude Code](https://xata.io/blog/configuring-neovim-coding-agents)

---

## 4. NeoVim 터미널 모드

NeoVim은 내장 터미널을 지원합니다. tmux 패널 대신 NeoVim 내부 분할 창에서 터미널을 실행할 수 있습니다.

### 터미널 열기

```vim
" 수평 분할로 터미널 열기
:terminal

" 또는 짧게
:term

" 수직 분할로 터미널 열기
:vsplit | terminal
```

### Terminal 모드

터미널을 열면 **Terminal 모드**에 진입합니다. 이 모드에서는 터미널 프로그램이 키 입력을 받으며, Vim 명령어는 동작하지 않습니다.

**Terminal 모드 탈출:**
```
Ctrl+\ Ctrl+N  (Normal 모드로 복귀)
```

Normal 모드로 돌아오면 터미널 출력을 Vim 모션으로 탐색하거나, 다른 윈도우로 이동할 수 있습니다.

### 터미널 단축키 설정

```lua
-- practice/configs/nvim/init.lua에 추가

-- 터미널 열기
vim.keymap.set("n", "<leader>tt", ":split | terminal<CR>", { desc = "Open terminal (horizontal)" })
vim.keymap.set("n", "<leader>tv", ":vsplit | terminal<CR>", { desc = "Open terminal (vertical)" })

-- Terminal 모드 탈출 (Esc 두 번)
vim.keymap.set("t", "<Esc><Esc>", "<C-\\><C-n>", { desc = "Exit terminal mode" })

-- Terminal 모드에서 윈도우 이동
vim.keymap.set("t", "<C-h>", "<C-\\><C-n><C-w>h", { desc = "Move to left window" })
vim.keymap.set("t", "<C-j>", "<C-\\><C-n><C-w>j", { desc = "Move to below window" })
vim.keymap.set("t", "<C-k>", "<C-\\><C-n><C-w>k", { desc = "Move to above window" })
vim.keymap.set("t", "<C-l>", "<C-\\><C-n><C-w>l", { desc = "Move to right window" })

-- 터미널 열 때 자동으로 Insert 모드
vim.api.nvim_create_autocmd("TermOpen", {
  pattern = "*",
  callback = function()
    vim.cmd("startinsert")
  end,
})
```

### NeoVim 터미널에서 Claude Code 실행

```vim
" 수평 분할로 터미널 열기
:split | terminal

" 터미널에서 Claude Code 실행
claude

" Esc Esc로 Normal 모드 → Ctrl+w k로 상단 코드 편집 창으로 이동
```

---

## 5. 실전 워크플로우

### 시나리오 1: Claude Code로 코드 생성 → NeoVim에서 리뷰/수정

```
┌──────────────────────────────────┐
│ NeoVim: src/api/user.ts          │ ← 여기서 코드 확인 및 수정
│                                  │
│ function getUser(id: string) {   │
│   // Claude가 생성한 코드        │
│ }                                │
├──────────────────────────────────┤
│ $ claude                         │
│ > "TypeScript로 사용자 조회      │
│    함수 만들어줘. Zod 검증 포함" │
└──────────────────────────────────┘

워크플로우:
1. Claude에게 요청
2. 생성된 코드 파일 경로 확인
3. NeoVim에서 :e src/api/user.ts 열기
4. 코드 리뷰 및 수정
5. :w 저장
```

### 시나리오 2: NeoVim에서 코드 작성 → Claude에게 질문

```
┌──────────────────────────────────┐
│ NeoVim: src/utils/parser.ts      │
│                                  │
│ function parseConfig(json: str) {│ ← 이 코드에 대해 질문
│   const data = JSON.parse(json); │
│   return data;                   │
│ }                                │
├──────────────────────────────────┤
│ $ claude                         │
│ > "parser.ts의 parseConfig 함수  │
│    에러 처리 어떻게 개선할까?"   │
└──────────────────────────────────┘

워크플로우:
1. NeoVim에서 코드 작성
2. Ctrl+b ↓ (tmux) 또는 Ctrl+w j (NeoVim terminal)로 Claude 패널 이동
3. 파일 경로와 질문 입력
4. Claude 응답 확인
5. NeoVim으로 돌아와 수정 적용
```

### 시나리오 3: Claude의 diff 출력을 NeoVim에서 확인

```bash
# Claude Code에서 diff 출력
$ claude "리팩토링해줘"
# Claude가 변경사항을 diff 형식으로 보여줌

# diff를 파일로 저장
$ claude "리팩토링해줘" > /tmp/changes.diff

# NeoVim에서 diff 확인
:e /tmp/changes.diff
:set filetype=diff  # 하이라이팅 적용
```

### 02_omc 프로젝트 참조

oh-my-claudecode(omc) 프로젝트는 Claude Code의 고급 워크플로우를 자동화하는 도구입니다. `runners-high/poc/02_omc/` 프로젝트에서 다루는 내용:

- 플래그 기반 작업 모드
- 에이전트 시스템 (Orchestrator, Executor)
- TODO 기반 작업 추적
- 계획(plan) 및 노트패드 시스템

NeoVim과 omc를 함께 사용하면 다음과 같은 고급 워크플로우가 가능합니다:

```bash
# NeoVim에서 TODO 작성
# TODO: API 엔드포인트에 인증 추가

# tmux 하단 패널에서 omc 실행
$ omc --plan=api-auth

# omc가 TODO를 읽고 작업 계획 수립
# NeoVim에서 실시간으로 생성된 코드 확인
```

---

## 6. 유용한 설정

### 터미널 모드 탈출 키맵

```lua
-- Esc 두 번으로 Terminal 모드 탈출
vim.keymap.set("t", "<Esc><Esc>", "<C-\\><C-n>")

-- jk로도 탈출 가능 (Insert 모드와 일관성)
vim.keymap.set("t", "jk", "<C-\\><C-n>")
```

### 터미널 자동 Insert 모드 진입

```lua
-- 터미널 열 때 자동으로 Insert 모드
vim.api.nvim_create_autocmd("TermOpen", {
  pattern = "*",
  callback = function()
    vim.cmd("startinsert")
    vim.opt_local.number = false         -- 라인 번호 숨기기
    vim.opt_local.relativenumber = false
    vim.opt_local.signcolumn = "no"      -- 사인 컬럼 숨기기
  end,
})

-- 터미널 윈도우로 돌아올 때도 Insert 모드
vim.api.nvim_create_autocmd("BufEnter", {
  pattern = "term://*",
  callback = function()
    vim.cmd("startinsert")
  end,
})
```

### 터미널 버퍼 자동 닫기

```lua
-- 터미널 프로세스 종료 시 버퍼 자동 닫기
vim.api.nvim_create_autocmd("TermClose", {
  pattern = "*",
  callback = function()
    vim.cmd("bdelete!")
  end,
})
```

### Claude Code 전용 터미널 토글

```lua
-- practice/configs/nvim/lua/config/claude-terminal.lua
local M = {}

local term_buf = nil
local term_win = nil

function M.toggle()
  -- 터미널이 이미 열려있으면 닫기
  if term_win and vim.api.nvim_win_is_valid(term_win) then
    vim.api.nvim_win_close(term_win, true)
    term_win = nil
    return
  end

  -- 터미널 버퍼가 없으면 생성
  if not term_buf or not vim.api.nvim_buf_is_valid(term_buf) then
    term_buf = vim.api.nvim_create_buf(false, true)
    vim.api.nvim_buf_call(term_buf, function()
      vim.fn.termopen("claude")
    end)
  end

  -- 하단에 30% 크기로 윈도우 생성
  local height = math.floor(vim.o.lines * 0.3)
  vim.cmd("botright " .. height .. "split")
  term_win = vim.api.nvim_get_current_win()
  vim.api.nvim_win_set_buf(term_win, term_buf)

  -- Insert 모드로 진입
  vim.cmd("startinsert")
end

return M
```

```lua
-- init.lua에 추가
vim.keymap.set("n", "<leader>tc", function()
  require("config.claude-terminal").toggle()
end, { desc = "Toggle Claude terminal" })
```

---

## 실습

1. **tmux 레이아웃 구성**
   - tmux 세션 생성
   - 상단 패널에서 NeoVim 실행
   - 하단 패널(30%)에서 Claude Code 실행
   - Ctrl+b ↑↓로 패널 전환 연습

2. **$EDITOR 설정**
   - `~/.zshrc`에 `export EDITOR="nvim"` 추가
   - `source ~/.zshrc`로 적용
   - `git commit`으로 NeoVim이 열리는지 확인

3. **NeoVim 터미널 모드 테스트**
   - `:split | terminal` 실행
   - `ls`, `pwd` 등 명령어 실행
   - `Esc Esc`로 Normal 모드 복귀
   - 터미널 출력을 Vim 모션으로 탐색

4. **통합 워크플로우 실습**
   - tmux 하단 패널에서 Claude Code 실행
   - "TypeScript 함수 하나 만들어줘" 요청
   - 생성된 파일을 상단 NeoVim에서 열기
   - 코드 수정 후 저장

---

## 명령어 요약

| 명령어/단축키 | 기능 |
|---------------|------|
| `export EDITOR="nvim"` | 기본 에디터를 NeoVim으로 설정 |
| `:terminal` | NeoVim 내장 터미널 열기 |
| `:split \| terminal` | 수평 분할로 터미널 열기 |
| `:vsplit \| terminal` | 수직 분할로 터미널 열기 |
| `Ctrl+\ Ctrl+N` | Terminal 모드 → Normal 모드 |
| `<Esc><Esc>` | Terminal 모드 탈출 (커스텀) |
| `Ctrl+b "` | tmux 수평 분할 |
| `Ctrl+b %` | tmux 수직 분할 |
| `Ctrl+b ↑↓←→` | tmux 패널 이동 |
| `<leader>tt` | 터미널 열기 (커스텀) |
| `<leader>tc` | Claude 터미널 토글 (커스텀) |

---

## 체크포인트

<details>
<summary><strong>1. tmux pane과 NeoVim :terminal 중 어느 것을 선호하나요? 각각의 장단점은?</strong></summary>

**tmux pane:**
- 장점: NeoVim과 독립적으로 동작, 세션 복구 가능(tmux-resurrect), 여러 프로그램을 동시에 실행, 네트워크 연결 끊어져도 세션 유지
- 단점: 추가 단축키 학습 필요, 설정 복잡도 증가

**NeoVim :terminal:**
- 장점: Vim 윈도우 관리와 통합(Ctrl+w), 설정이 단순, Terminal 출력을 Vim 버퍼로 조작 가능
- 단점: NeoVim을 닫으면 터미널도 종료, 세션 복구 불가

**권장:** 로컬 개발은 NeoVim :terminal로 시작하고, 원격 서버나 장시간 실행되는 작업은 tmux 사용. 많은 개발자들이 tmux(세션 관리) + NeoVim(에디터) + NeoVim :terminal(일시적 명령어)를 함께 사용합니다.
</details>

<details>
<summary><strong>2. $EDITOR 환경변수가 Claude Code에 미치는 영향은?</strong></summary>

Claude Code는 파일 편집이 필요한 상황에서 `$EDITOR` 환경변수를 참조하여 에디터를 실행합니다. `export EDITOR="nvim"`으로 설정하면 Claude가 코드 수정을 요청하거나 diff를 보여줄 때 NeoVim이 자동으로 열립니다. 이를 통해 마우스 없이 터미널 안에서 Claude의 제안을 받고 NeoVim으로 수정하는 통합 워크플로우가 가능해집니다. 또한 git commit, crontab 편집 등 다른 유닉스 도구들도 동일한 에디터를 사용하게 되어 개발 환경이 일관되게 유지됩니다.
</details>

<details>
<summary><strong>3. AI 도구와 Vim을 함께 쓸 때의 워크플로우 장점은?</strong></summary>

AI 도구(Claude Code)와 Vim을 함께 사용하면 **생성과 편집의 분리**가 명확해집니다. Claude는 초안 생성, 보일러플레이트 코드 작성, 리팩토링 제안 등 반복적인 작업을 빠르게 처리하고, Vim은 정밀한 편집, 코드 탐색, LSP 진단 등 세밀한 작업을 담당합니다. 또한 터미널 기반이므로 원격 서버, Docker 컨테이너, CI/CD 환경에서도 동일한 워크플로우를 사용할 수 있습니다. Vim의 모션과 연산자를 익히면 AI가 생성한 코드를 빠르게 수정하고 통합할 수 있어, 생산성이 크게 향상됩니다. 특히 tmux 세션 관리와 결합하면 프로젝트 컨텍스트를 유지하면서 AI와 대화하고 코드를 편집하는 매끄러운 흐름을 만들 수 있습니다.
</details>

---
다음: [14. 실전 워크플로우](./14-workflow.md)
