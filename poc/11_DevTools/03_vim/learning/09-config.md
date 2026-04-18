# 09. 설정 파일 - .vimrc와 init.lua

Vim의 진정한 개인화는 설정 파일에서 시작됩니다. 기본 Vim은 .vimrc를 사용하지만, NeoVim은 Lua 기반의 init.lua를 사용합니다. Lua는 VimScript보다 읽기 쉽고, 성능이 뛰어나며, NeoVim의 모든 API에 직접 접근할 수 있습니다. 이 챕터에서는 직접 설정 파일을 작성하면서 자신만의 NeoVim 환경을 구축합니다.

---

## 목표

- [ ] init.lua의 기본 구조를 이해하고 작성할 수 있다
- [ ] vim.opt, vim.keymap.set, vim.g의 사용법을 알 수 있다
- [ ] leader 키 기반 단축키 체계를 설정할 수 있다

---

## 1. 설정 파일 위치

Vim과 NeoVim은 서로 다른 위치에 설정 파일을 저장합니다. NeoVim은 XDG Base Directory 규칙을 따르며, 설정을 모듈화할 수 있도록 디렉토리 구조를 지원합니다.

### 기본 경로

```bash
# Vim
~/.vimrc                    # 단일 파일

# NeoVim
~/.config/nvim/init.lua     # Lua 설정 (권장)
~/.config/nvim/init.vim     # VimScript 설정 (호환성)
```

### NeoVim 설정 디렉토리 구조

NeoVim은 여러 디렉토리에서 설정을 로드하여 모듈화를 지원합니다.

```
~/.config/nvim/
├── init.lua              # 진입점
├── lua/                  # Lua 모듈
│   ├── config/
│   │   ├── options.lua   # 옵션 설정
│   │   ├── keymaps.lua   # 키 매핑
│   │   └── autocmds.lua  # 자동 명령
│   └── plugins/
│       └── init.lua      # 플러그인 설정
├── plugin/               # 자동 로드 VimScript
└── after/
    └── plugin/           # 늦게 로드할 설정
```

### 설정 로드 순서 확인

```vim
" 현재 로드된 설정 파일 확인
:echo $MYVIMRC

" 런타임 경로 확인
:set runtimepath?

" 모든 로드된 스크립트 목록
:scriptnames
```

## 2. vim.opt - 옵션 설정

`vim.opt`는 Vim의 옵션을 Lua 문법으로 설정하는 인터페이스입니다. VimScript의 `set`과 동일하지만 타입 안전성과 자동완성이 더 뛰어납니다.

### 기본 옵션

```lua
-- ~/.config/nvim/init.lua

-- 줄번호 표시
vim.opt.number = true           -- 절대 줄번호
vim.opt.relativenumber = true   -- 상대 줄번호 (hjkl 이동에 유용)

-- 검색 설정
vim.opt.ignorecase = true       -- 대소문자 무시
vim.opt.smartcase = true        -- 대문자 입력 시 대소문자 구분
vim.opt.hlsearch = true         -- 검색 결과 하이라이트
vim.opt.incsearch = true        -- 입력하면서 검색

-- 들여쓰기
vim.opt.tabstop = 4             -- 탭 문자 너비
vim.opt.shiftwidth = 4          -- >> 들여쓰기 너비
vim.opt.expandtab = true        -- 탭을 스페이스로 변환
vim.opt.smartindent = true      -- 자동 들여쓰기

-- 클립보드
vim.opt.clipboard = "unnamedplus"  -- 시스템 클립보드 사용

-- UI
vim.opt.termguicolors = true    -- 24비트 컬러 지원
vim.opt.cursorline = true       -- 현재 줄 강조
vim.opt.signcolumn = "yes"      -- 왼쪽 사인 컬럼 항상 표시
vim.opt.scrolloff = 8           -- 스크롤 여백 (위아래 8줄)
vim.opt.sidescrolloff = 8       -- 가로 스크롤 여백

-- 윈도우 분할
vim.opt.splitbelow = true       -- 수평 분할 시 아래에
vim.opt.splitright = true       -- 수직 분할 시 오른쪽에

-- 파일
vim.opt.swapfile = false        -- 스왑 파일 비활성화
vim.opt.backup = false          -- 백업 파일 비활성화
vim.opt.undofile = true         -- 영구 undo 기록
vim.opt.updatetime = 300        -- CursorHold 이벤트 시간 (ms)

-- 기타
vim.opt.mouse = "a"             -- 모든 모드에서 마우스 지원
vim.opt.hidden = true           -- 저장 없이 버퍼 전환 허용
vim.opt.wrap = false            -- 줄 바꿈 비활성화
```

### vim.opt vs vim.o vs vim.opt_local

```lua
-- vim.opt: 권장 방식 (메타테이블로 자동 처리)
vim.opt.number = true

-- vim.o: 전역 옵션만 (VimScript의 set과 동일)
vim.o.number = true

-- vim.opt_local: 현재 버퍼/윈도우 한정
vim.opt_local.tabstop = 2

-- 리스트 옵션 추가 (+=, -=)
vim.opt.shortmess:append("c")   -- 완성 메시지 제거
vim.opt.iskeyword:append("-")   -- 단어에 하이픈 포함
```

## 3. vim.keymap.set - 키 매핑

키 매핑은 단축키를 정의하는 핵심 설정입니다. `vim.keymap.set`은 VimScript의 `map`, `nmap`, `imap` 등을 통합한 현대적인 API입니다.

### 기본 문법

```lua
-- vim.keymap.set(mode, lhs, rhs, opts)
-- mode: 모드 문자열
-- lhs: 입력할 키
-- rhs: 실행할 명령 (문자열 또는 함수)
-- opts: 옵션 테이블

vim.keymap.set("n", "<leader>w", ":w<CR>", { desc = "Save file" })
```

### 모드 종류

```lua
-- 모드 문자열
-- "n" : Normal
-- "i" : Insert
-- "v" : Visual + Select
-- "x" : Visual only
-- "s" : Select
-- "c" : Command-line
-- "t" : Terminal

-- 여러 모드에 동시 적용
vim.keymap.set({"n", "v"}, "<leader>y", '"+y', { desc = "Copy to clipboard" })
```

### 유용한 매핑 예시

```lua
-- ESC 대체 (Insert 모드 탈출)
vim.keymap.set("i", "jk", "<Esc>", { desc = "Exit insert mode" })
vim.keymap.set("i", "kj", "<Esc>", { desc = "Exit insert mode" })

-- 빠른 저장/종료
vim.keymap.set("n", "<leader>w", ":w<CR>", { desc = "Save file" })
vim.keymap.set("n", "<leader>q", ":q<CR>", { desc = "Quit" })
vim.keymap.set("n", "<leader>x", ":x<CR>", { desc = "Save and quit" })

-- 검색 하이라이트 제거
vim.keymap.set("n", "<Esc>", ":noh<CR>", { silent = true, desc = "Clear highlight" })

-- 윈도우 이동
vim.keymap.set("n", "<C-h>", "<C-w>h", { desc = "Move to left window" })
vim.keymap.set("n", "<C-j>", "<C-w>j", { desc = "Move to bottom window" })
vim.keymap.set("n", "<C-k>", "<C-w>k", { desc = "Move to top window" })
vim.keymap.set("n", "<C-l>", "<C-w>l", { desc = "Move to right window" })

-- 버퍼 전환
vim.keymap.set("n", "<S-l>", ":bnext<CR>", { desc = "Next buffer" })
vim.keymap.set("n", "<S-h>", ":bprevious<CR>", { desc = "Previous buffer" })

-- 윈도우 크기 조절
vim.keymap.set("n", "<C-Up>", ":resize +2<CR>", { desc = "Increase height" })
vim.keymap.set("n", "<C-Down>", ":resize -2<CR>", { desc = "Decrease height" })
vim.keymap.set("n", "<C-Left>", ":vertical resize -2<CR>", { desc = "Decrease width" })
vim.keymap.set("n", "<C-Right>", ":vertical resize +2<CR>", { desc = "Increase width" })

-- Visual 모드에서 들여쓰기 후 선택 유지
vim.keymap.set("v", "<", "<gv", { desc = "Indent left" })
vim.keymap.set("v", ">", ">gv", { desc = "Indent right" })

-- 줄 이동
vim.keymap.set("v", "J", ":m '>+1<CR>gv=gv", { desc = "Move line down" })
vim.keymap.set("v", "K", ":m '<-2<CR>gv=gv", { desc = "Move line up" })

-- 중앙 정렬 (스크롤 시)
vim.keymap.set("n", "<C-d>", "<C-d>zz", { desc = "Scroll down centered" })
vim.keymap.set("n", "<C-u>", "<C-u>zz", { desc = "Scroll up centered" })
vim.keymap.set("n", "n", "nzzzv", { desc = "Next search centered" })
vim.keymap.set("n", "N", "Nzzzv", { desc = "Previous search centered" })

-- 함수로 매핑
vim.keymap.set("n", "<leader>h", function()
  print("Hello from Lua!")
end, { desc = "Say hello" })
```

### 매핑 옵션

```lua
-- 옵션 테이블 키
{
  desc = "설명",           -- which-key 등에서 표시
  silent = true,          -- 명령 메시지 숨김
  noremap = true,         -- 재귀 매핑 방지 (기본값 true)
  expr = true,            -- 표현식으로 평가
  buffer = 0,             -- 버퍼 로컬 매핑 (0 = 현재 버퍼)
  nowait = true,          -- 다음 키 입력 대기하지 않음
}

-- 예시: 버퍼 로컬 매핑
vim.keymap.set("n", "<leader>r", ":!python %<CR>", {
  buffer = 0,
  desc = "Run current Python file",
})
```

## 4. leader 키

leader 키는 사용자 정의 단축키의 네임스페이스 역할을 합니다. Space를 leader로 설정하면 누르기 쉽고, 직관적인 단축키 체계를 만들 수 있습니다.

### leader 설정

```lua
-- Space를 leader로 설정 (가장 인기 있는 선택)
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- 주의: leader 설정은 키맵 정의보다 먼저 해야 함
-- init.lua 맨 위에 배치
```

### leader 기반 단축키 체계

```lua
-- 파일 (Find)
vim.keymap.set("n", "<leader>ff", "<cmd>Telescope find_files<CR>", { desc = "[F]ind [F]iles" })
vim.keymap.set("n", "<leader>fg", "<cmd>Telescope live_grep<CR>", { desc = "[F]ind by [G]rep" })
vim.keymap.set("n", "<leader>fb", "<cmd>Telescope buffers<CR>", { desc = "[F]ind [B]uffers" })
vim.keymap.set("n", "<leader>fr", "<cmd>Telescope oldfiles<CR>", { desc = "[F]ind [R]ecent" })

-- 버퍼 (Buffer)
vim.keymap.set("n", "<leader>bd", ":bd<CR>", { desc = "[B]uffer [D]elete" })
vim.keymap.set("n", "<leader>bn", ":bnext<CR>", { desc = "[B]uffer [N]ext" })
vim.keymap.set("n", "<leader>bp", ":bprevious<CR>", { desc = "[B]uffer [P]revious" })

-- 윈도우 (Window)
vim.keymap.set("n", "<leader>wv", "<C-w>v", { desc = "[W]indow split [V]ertical" })
vim.keymap.set("n", "<leader>wh", "<C-w>s", { desc = "[W]indow split [H]orizontal" })
vim.keymap.set("n", "<leader>wq", "<C-w>q", { desc = "[W]indow [Q]uit" })

-- 탭 (Tab)
vim.keymap.set("n", "<leader>tn", ":tabnew<CR>", { desc = "[T]ab [N]ew" })
vim.keymap.set("n", "<leader>tc", ":tabclose<CR>", { desc = "[T]ab [C]lose" })

-- LSP (Ch10에서 상세)
vim.keymap.set("n", "<leader>ca", vim.lsp.buf.code_action, { desc = "[C]ode [A]ction" })
vim.keymap.set("n", "<leader>rn", vim.lsp.buf.rename, { desc = "[R]e[n]ame" })

-- 파일 탐색기
vim.keymap.set("n", "<leader>e", ":NeoTreeToggle<CR>", { desc = "[E]xplorer" })
```

### which-key 플러그인과의 시너지

which-key 플러그인(Ch10 참고)을 사용하면 leader 키를 누르면 사용 가능한 단축키가 자동으로 표시됩니다.

```lua
-- which-key에서 그룹 설명 등록
require("which-key").register({
  ["<leader>f"] = { name = "[F]ind" },
  ["<leader>b"] = { name = "[B]uffer" },
  ["<leader>w"] = { name = "[W]indow" },
  ["<leader>t"] = { name = "[T]ab" },
  ["<leader>c"] = { name = "[C]ode" },
})

-- leader 누르면 팝업 표시:
-- <leader>f  [F]ind
--   ff  [F]ind [F]iles
--   fg  [F]ind by [G]rep
--   fb  [F]ind [B]uffers
```

## 5. 모듈화 구성

설정이 길어지면 파일을 분리하여 관리합니다. Lua의 `require` 시스템을 활용합니다.

### 디렉토리 구조

```
~/.config/nvim/
├── init.lua                      # 진입점
└── lua/
    └── config/
        ├── options.lua           # vim.opt 설정
        ├── keymaps.lua           # vim.keymap.set 설정
        └── autocmds.lua          # 자동 명령
```

### init.lua (진입점)

```lua
-- ~/.config/nvim/init.lua

-- leader 키는 맨 먼저 설정
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- 모듈 로드
require("config.options")
require("config.keymaps")
require("config.autocmds")

-- 플러그인 (Ch10에서 추가)
-- require("config.lazy")
```

### lua/config/options.lua

```lua
-- ~/.config/nvim/lua/config/options.lua

local opt = vim.opt

-- 줄번호
opt.number = true
opt.relativenumber = true

-- 검색
opt.ignorecase = true
opt.smartcase = true

-- 들여쓰기
opt.tabstop = 4
opt.shiftwidth = 4
opt.expandtab = true

-- UI
opt.termguicolors = true
opt.cursorline = true
opt.signcolumn = "yes"
opt.scrolloff = 8

-- 클립보드
opt.clipboard = "unnamedplus"

-- 파일
opt.swapfile = false
opt.backup = false
opt.undofile = true

-- 기타
opt.mouse = "a"
opt.hidden = true
opt.splitbelow = true
opt.splitright = true
```

### lua/config/keymaps.lua

```lua
-- ~/.config/nvim/lua/config/keymaps.lua

local keymap = vim.keymap

-- ESC 대체
keymap.set("i", "jk", "<Esc>")

-- 저장/종료
keymap.set("n", "<leader>w", ":w<CR>", { desc = "Save" })
keymap.set("n", "<leader>q", ":q<CR>", { desc = "Quit" })

-- 윈도우 이동
keymap.set("n", "<C-h>", "<C-w>h")
keymap.set("n", "<C-j>", "<C-w>j")
keymap.set("n", "<C-k>", "<C-w>k")
keymap.set("n", "<C-l>", "<C-w>l")

-- 버퍼 전환
keymap.set("n", "<S-l>", ":bnext<CR>")
keymap.set("n", "<S-h>", ":bprevious<CR>")

-- Visual 모드 들여쓰기
keymap.set("v", "<", "<gv")
keymap.set("v", ">", ">gv")
```

### lua/config/autocmds.lua

```lua
-- ~/.config/nvim/lua/config/autocmds.lua

-- 자동 명령 그룹 생성
local augroup = vim.api.nvim_create_augroup
local autocmd = vim.api.nvim_create_autocmd

-- 파일 저장 시 trailing whitespace 제거
autocmd("BufWritePre", {
  group = augroup("TrimWhitespace", { clear = true }),
  pattern = "*",
  command = [[%s/\s\+$//e]],
})

-- Markdown 파일은 wrap 활성화
autocmd("FileType", {
  group = augroup("MarkdownWrap", { clear = true }),
  pattern = "markdown",
  callback = function()
    vim.opt_local.wrap = true
    vim.opt_local.spell = true
  end,
})

-- 파일 열 때 마지막 커서 위치로
autocmd("BufReadPost", {
  group = augroup("LastPosition", { clear = true }),
  pattern = "*",
  callback = function()
    local mark = vim.api.nvim_buf_get_mark(0, '"')
    if mark[1] > 0 and mark[1] <= vim.api.nvim_buf_line_count(0) then
      vim.api.nvim_win_set_cursor(0, mark)
    end
  end,
})
```

## 실습

`practice/configs/minimal-init.lua`를 직접 수정하며 옵션과 키맵을 추가합니다.

### 연습 1: 옵션 설정

다음 옵션을 `minimal-init.lua`에 추가하세요.

```lua
-- TODO: 다음 옵션 추가
-- 1. 상대 줄번호 활성화
-- 2. 탭을 4칸 스페이스로
-- 3. 시스템 클립보드 사용
-- 4. 스크롤 여백 8줄
-- 5. 스왑 파일 비활성화
```

### 연습 2: 키맵 설정

```lua
-- TODO: 다음 키맵 추가
-- 1. jk로 Insert 모드 탈출
-- 2. <leader>w로 저장
-- 3. <S-h>/<S-l>로 버퍼 전환
-- 4. Visual 모드에서 </> 후 선택 유지
```

### 연습 3: 모듈화

`minimal-init.lua`를 다음과 같이 분리하세요.

```
practice/configs/
├── init.lua
└── lua/
    └── config/
        ├── options.lua
        └── keymaps.lua
```

## 명령어 요약

| 명령 | 설명 |
|------|------|
| `vim.opt.{option}` | 옵션 설정 |
| `vim.opt_local.{option}` | 버퍼/윈도우 로컬 옵션 |
| `vim.g.{var}` | 전역 변수 설정 |
| `vim.keymap.set(mode, lhs, rhs, opts)` | 키 매핑 |
| `vim.api.nvim_create_autocmd` | 자동 명령 생성 |
| `require("module")` | Lua 모듈 로드 |
| `:echo $MYVIMRC` | 설정 파일 경로 확인 |
| `:source $MYVIMRC` | 설정 다시 로드 |
| `:scriptnames` | 로드된 스크립트 목록 |

## 체크포인트

<details>
<summary>1. vim.opt.clipboard = "unnamedplus"는 어떤 효과가 있나요?</summary>

Vim의 레지스터와 시스템 클립보드를 연결합니다. 이 설정이 활성화되면 `y`로 복사한 텍스트를 다른 애플리케이션에 붙여넣을 수 있고, 반대로 외부에서 복사한 내용을 Vim에서 `p`로 붙여넣을 수 있습니다. `unnamedplus`는 X11의 `+` 레지스터를 사용합니다(Linux). macOS에서는 자동으로 pbcopy/pbpaste와 연결됩니다.

</details>

<details>
<summary>2. leader 키를 Space로 설정하는 이유는?</summary>

Space는 양손 엄지로 누를 수 있어 접근성이 뛰어나고, 기본 Vim에서 거의 사용하지 않는 키입니다(오른쪽 이동은 `l`로 대체 가능). 또한 `\`(기본 leader)보다 누르기 편하고, 시각적으로 단축키 체계를 기억하기 쉽습니다. 예: `<leader>f` = "Space + f" = "Find". 단, leader 설정은 반드시 키맵 정의보다 먼저 해야 합니다.

</details>

<details>
<summary>3. init.lua를 모듈화하는 것의 장점은?</summary>

옵션, 키맵, 자동 명령, 플러그인 설정을 각각의 파일로 분리하면 찾기 쉽고 유지보수가 편합니다. 특히 플러그인이 많아지면 하나의 파일이 수백 줄이 되어 관리가 어렵습니다. `require` 시스템을 사용하면 필요한 부분만 선택적으로 로드할 수도 있습니다. 또한 Git으로 버전 관리 시 변경사항을 파일별로 추적할 수 있어 협업에도 유리합니다.

</details>

---

다음: [10. NeoVim 플러그인](./10-plugins.md)
