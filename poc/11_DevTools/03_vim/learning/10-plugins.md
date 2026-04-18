# 10. NeoVim 플러그인 - lazy.nvim 기반 생태계

NeoVim의 플러그인 생태계는 2024~2026년 사이 급격히 성숙했습니다. lazy.nvim이라는 패키지 매니저가 사실상 표준으로 자리잡았고, telescope(퍼지 파인더), treesitter(구문 분석), neo-tree(파일 탐색기) 등 핵심 플러그인들이 IDE 수준의 경험을 제공합니다. 이 챕터에서는 가장 널리 사용되는 플러그인들을 하나씩 설치하고 설정합니다.

---

## 목표

- [ ] lazy.nvim으로 플러그인을 설치하고 관리할 수 있다
- [ ] telescope, treesitter, neo-tree를 설정할 수 있다
- [ ] which-key로 단축키를 체계적으로 관리할 수 있다

---

## 1. lazy.nvim 패키지 매니저

lazy.nvim은 현재 가장 인기 있는 NeoVim 플러그인 매니저입니다. 이전의 packer.nvim, vim-plug를 대체하며 지연 로딩과 빠른 시작 시간을 제공합니다.

### 왜 lazy.nvim인가?

기존 플러그인 매니저 대비 lazy.nvim이 제공하는 장점들입니다.

```lua
-- 장점 1: 지연 로딩 (Lazy Loading)
-- 필요할 때만 플러그인을 로드하여 시작 시간 단축

-- 장점 2: 록파일 (lockfile)
-- lazy-lock.json으로 플러그인 버전 고정 → 재현 가능한 환경

-- 장점 3: UI
-- :Lazy 명령으로 시각적 관리 인터페이스 제공

-- 장점 4: 자동 설치
-- missing 플러그인 자동 감지 및 설치

-- 장점 5: 프로파일링
-- 플러그인별 로딩 시간 측정
```

### 부트스트랩 설치

lazy.nvim은 NeoVim 시작 시 자동으로 설치되도록 부트스트랩 코드를 추가합니다.

```lua
-- ~/.config/nvim/lua/config/lazy.lua

local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"

-- lazy.nvim이 없으면 자동 설치
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable",
    lazypath,
  })
end

-- runtimepath에 추가
vim.opt.rtp:prepend(lazypath)

-- 플러그인 설정 로드
require("lazy").setup({
  -- 플러그인 스펙들이 여기에 들어감
  spec = {
    { import = "plugins" },  -- lua/plugins/ 디렉토리에서 자동 로드
  },
  -- 옵션
  defaults = {
    lazy = true,  -- 기본적으로 지연 로딩
  },
  install = {
    colorscheme = { "catppuccin" },  -- 설치 중 사용할 컬러스킴
  },
  checker = {
    enabled = true,  -- 업데이트 자동 확인
    notify = false,  -- 알림 비활성화
  },
  performance = {
    rtp = {
      disabled_plugins = {
        "gzip",
        "tarPlugin",
        "tohtml",
        "tutor",
        "zipPlugin",
      },
    },
  },
})
```

```lua
-- ~/.config/nvim/init.lua 에 추가
require("config.lazy")
```

### 플러그인 스펙 문법

플러그인은 Lua 테이블로 정의합니다.

```lua
-- 기본 형식
{
  "author/repo",              -- GitHub 저장소
  lazy = false,               -- false면 즉시 로드
  dependencies = { "dep" },   -- 의존성
  config = function()         -- 설정 함수
    require("plugin").setup({})
  end,
  keys = { "<leader>x" },     -- 특정 키 입력 시 로드
  ft = { "lua", "vim" },      -- 특정 파일 타입에서 로드
  cmd = { "Command" },        -- 특정 명령 실행 시 로드
  event = { "BufRead" },      -- 특정 이벤트 시 로드
  init = function() end,      -- 로드 전 실행
}

-- 예시: Telescope
{
  "nvim-telescope/telescope.nvim",
  dependencies = { "nvim-lua/plenary.nvim" },
  cmd = "Telescope",
  keys = {
    { "<leader>ff", "<cmd>Telescope find_files<CR>", desc = "Find Files" },
  },
  config = function()
    require("telescope").setup({
      -- 설정...
    })
  end,
}
```

### lazy.nvim 명령어

```vim
:Lazy           " UI 열기
:Lazy install   " 모든 플러그인 설치
:Lazy update    " 업데이트
:Lazy sync      " install + update + clean
:Lazy clean     " 사용하지 않는 플러그인 제거
:Lazy check     " 업데이트 확인
:Lazy profile   " 로딩 시간 프로파일
:Lazy log       " 변경 로그
:Lazy restore   " lockfile로 복원
```

## 2. telescope.nvim - 퍼지 파인더

telescope는 파일 찾기, 텍스트 검색, 버퍼 목록 등 모든 "선택" 작업을 통합하는 퍼지 파인더입니다. IDE의 "모든 것 검색" 기능과 동일합니다.

### 설치 및 설정

```lua
-- ~/.config/nvim/lua/plugins/telescope.lua

return {
  "nvim-telescope/telescope.nvim",
  branch = "0.1.x",
  dependencies = {
    "nvim-lua/plenary.nvim",
    { "nvim-telescope/telescope-fzf-native.nvim", build = "make" },
  },
  cmd = "Telescope",
  keys = {
    { "<leader>ff", "<cmd>Telescope find_files<CR>", desc = "Find Files" },
    { "<leader>fg", "<cmd>Telescope live_grep<CR>", desc = "Find by Grep" },
    { "<leader>fb", "<cmd>Telescope buffers<CR>", desc = "Find Buffers" },
    { "<leader>fh", "<cmd>Telescope help_tags<CR>", desc = "Find Help" },
    { "<leader>fr", "<cmd>Telescope oldfiles<CR>", desc = "Find Recent" },
    { "<leader>fw", "<cmd>Telescope grep_string<CR>", desc = "Find Word" },
  },
  config = function()
    local telescope = require("telescope")
    local actions = require("telescope.actions")

    telescope.setup({
      defaults = {
        -- 레이아웃
        layout_strategy = "horizontal",
        layout_config = {
          horizontal = {
            prompt_position = "top",
            preview_width = 0.55,
          },
          width = 0.87,
          height = 0.80,
        },
        -- 정렬
        sorting_strategy = "ascending",
        -- 키맵
        mappings = {
          i = {
            ["<C-j>"] = actions.move_selection_next,
            ["<C-k>"] = actions.move_selection_previous,
            ["<C-q>"] = actions.send_to_qflist + actions.open_qflist,
            ["<Esc>"] = actions.close,
          },
        },
        -- 파일 무시
        file_ignore_patterns = {
          "node_modules",
          ".git/",
          "dist/",
          "build/",
        },
      },
      pickers = {
        find_files = {
          hidden = true,  -- 숨김 파일 포함
        },
      },
    })

    -- fzf 네이티브 확장 로드 (더 빠른 검색)
    telescope.load_extension("fzf")
  end,
}
```

### 주요 기능

```vim
" 파일 찾기
:Telescope find_files         " 파일명으로 검색
<leader>ff

" 텍스트 검색 (ripgrep 필요)
:Telescope live_grep          " 파일 내용 실시간 검색
<leader>fg

" 커서 단어 검색
:Telescope grep_string        " 현재 커서 단어로 검색
<leader>fw

" 버퍼 목록
:Telescope buffers            " 열린 버퍼 목록
<leader>fb

" 최근 파일
:Telescope oldfiles           " 최근 연 파일
<leader>fr

" 도움말
:Telescope help_tags          " Vim 도움말 검색
<leader>fh

" Git
:Telescope git_files          " Git 추적 파일
:Telescope git_commits        " 커밋 히스토리
:Telescope git_branches       " 브랜치 목록
```

### 의존성 설치

telescope의 모든 기능을 사용하려면 외부 도구가 필요합니다.

```bash
# ripgrep (live_grep에 필요)
brew install ripgrep    # macOS
apt install ripgrep     # Ubuntu

# fd (find_files 성능 향상)
brew install fd         # macOS
apt install fd-find     # Ubuntu

# fzf-native (빠른 검색)
# lazy.nvim이 자동으로 빌드 (build = "make")
```

## 3. nvim-treesitter - 구문 분석

treesitter는 코드를 AST로 파싱하여 정확한 구문 하이라이팅, 코드 접기, 텍스트 객체 등을 제공합니다. 정규식 기반 구문 강조보다 훨씬 정확합니다.

### 정규식 vs AST 비교

```javascript
// 정규식 하이라이팅 문제점
const foo = "function bar() {}";  // 문자열 안의 'function'을 키워드로 인식할 수 있음

/* function test() {
  return true;
} */  // 주석 안의 코드를 실제 코드로 인식할 수 있음

// Treesitter는 AST 기반이라 정확히 구분
```

### 설치 및 설정

```lua
-- ~/.config/nvim/lua/plugins/treesitter.lua

return {
  "nvim-treesitter/nvim-treesitter",
  build = ":TSUpdate",
  event = { "BufReadPost", "BufNewFile" },
  dependencies = {
    "nvim-treesitter/nvim-treesitter-textobjects",
  },
  config = function()
    require("nvim-treesitter.configs").setup({
      -- 자동 설치할 언어
      ensure_installed = {
        "lua",
        "vim",
        "vimdoc",
        "javascript",
        "typescript",
        "tsx",
        "python",
        "rust",
        "go",
        "html",
        "css",
        "json",
        "markdown",
        "bash",
      },
      -- 파일 열 때 자동 설치
      auto_install = true,
      -- 구문 하이라이팅
      highlight = {
        enable = true,
        additional_vim_regex_highlighting = false,
      },
      -- 들여쓰기
      indent = {
        enable = true,
      },
      -- 증분 선택
      incremental_selection = {
        enable = true,
        keymaps = {
          init_selection = "<C-space>",
          node_incremental = "<C-space>",
          scope_incremental = false,
          node_decremental = "<bs>",
        },
      },
      -- 텍스트 객체
      textobjects = {
        select = {
          enable = true,
          lookahead = true,
          keymaps = {
            ["af"] = "@function.outer",
            ["if"] = "@function.inner",
            ["ac"] = "@class.outer",
            ["ic"] = "@class.inner",
            ["aa"] = "@parameter.outer",
            ["ia"] = "@parameter.inner",
          },
        },
        move = {
          enable = true,
          set_jumps = true,
          goto_next_start = {
            ["]m"] = "@function.outer",
            ["]]"] = "@class.outer",
          },
          goto_next_end = {
            ["]M"] = "@function.outer",
            ["]["] = "@class.outer",
          },
          goto_previous_start = {
            ["[m"] = "@function.outer",
            ["[["] = "@class.outer",
          },
          goto_previous_end = {
            ["[M"] = "@function.outer",
            ["[]"] = "@class.outer",
          },
        },
      },
    })
  end,
}
```

### Treesitter 명령어

```vim
:TSInstall {language}     " 언어 파서 설치
:TSInstall typescript tsx python

:TSUpdate                 " 모든 파서 업데이트
:TSUninstall {language}   " 파서 제거
:TSInstallInfo            " 설치된 파서 목록
:TSModuleInfo             " 모듈 상태 확인
```

### 텍스트 객체 활용

```vim
" 함수 단위 선택
vaf         " 함수 전체 (outer)
vif         " 함수 내부 (inner)
daf         " 함수 삭제
yif         " 함수 내부 복사

" 클래스 단위 선택
vac         " 클래스 전체
vic         " 클래스 내부

" 파라미터 단위 선택
via         " 파라미터 선택
daa         " 파라미터 삭제 (콤마 포함)

" 함수 간 이동
]m          " 다음 함수 시작
[m          " 이전 함수 시작
]]          " 다음 클래스 시작
[[          " 이전 클래스 시작
```

### 증분 선택 (Incremental Selection)

```vim
" 예시 코드:
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

" 커서가 'item' 위에 있을 때:
Ctrl+Space   " 1회: 'item' 선택
Ctrl+Space   " 2회: '(sum, item) => sum + item.price' 선택
Ctrl+Space   " 3회: 'items.reduce(...)' 전체 선택
Ctrl+Space   " 4회: 'return ...' 전체 선택
Backspace    " 이전 단계로
```

## 4. neo-tree.nvim - 파일 탐색기

neo-tree는 NeoVim의 현대적인 파일 탐색기입니다. NERDTree, nvim-tree를 대체합니다.

### 설치 및 설정

```lua
-- ~/.config/nvim/lua/plugins/neo-tree.lua

return {
  "nvim-neo-tree/neo-tree.nvim",
  branch = "v3.x",
  dependencies = {
    "nvim-lua/plenary.nvim",
    "nvim-tree/nvim-web-devicons",
    "MunifTanjim/nui.nvim",
  },
  keys = {
    { "<leader>e", "<cmd>Neotree toggle<CR>", desc = "Toggle Explorer" },
    { "<leader>o", "<cmd>Neotree focus<CR>", desc = "Focus Explorer" },
  },
  config = function()
    require("neo-tree").setup({
      close_if_last_window = true,  -- 마지막 윈도우면 닫기
      popup_border_style = "rounded",
      window = {
        position = "left",
        width = 30,
        mappings = {
          ["<space>"] = "none",  -- leader 키 충돌 방지
          ["o"] = "open",
          ["a"] = "add",
          ["d"] = "delete",
          ["r"] = "rename",
          ["y"] = "copy_to_clipboard",
          ["x"] = "cut_to_clipboard",
          ["p"] = "paste_from_clipboard",
          ["c"] = "copy",
          ["m"] = "move",
          ["/"] = "fuzzy_finder",
          ["f"] = "filter_on_submit",
          ["<C-x>"] = "clear_filter",
        },
      },
      filesystem = {
        filtered_items = {
          hide_dotfiles = false,
          hide_gitignored = false,
          hide_by_name = {
            "node_modules",
            ".git",
            ".DS_Store",
          },
        },
        follow_current_file = {
          enabled = true,  -- 현재 파일 자동 하이라이트
        },
        use_libuv_file_watcher = true,  -- 파일 변경 자동 감지
      },
    })
  end,
}
```

### 주요 기능

```vim
" 토글
<leader>e    " 열기/닫기
<leader>o    " 포커스

" 탐색
j/k          " 이동
Enter/o      " 파일 열기
h            " 디렉토리 닫기
l            " 디렉토리 열기

" 파일 조작
a            " 파일/디렉토리 추가
d            " 삭제
r            " 이름 변경
c            " 복사
m            " 이동
y            " 클립보드에 복사
p            " 붙여넣기

" 검색
/            " 퍼지 검색
f            " 필터
Ctrl+x       " 필터 해제

" 기타
R            " 새로고침
?            " 도움말
```

## 5. lualine.nvim - 상태표시줄

lualine은 하단 상태표시줄을 커스터마이징하는 플러그인입니다.

### 설치 및 설정

```lua
-- ~/.config/nvim/lua/plugins/lualine.lua

return {
  "nvim-lualine/lualine.nvim",
  dependencies = { "nvim-tree/nvim-web-devicons" },
  event = "VeryLazy",
  config = function()
    require("lualine").setup({
      options = {
        theme = "auto",  -- 컬러스킴과 자동 매칭
        component_separators = { left = "|", right = "|" },
        section_separators = { left = "", right = "" },
        globalstatus = true,  -- 윈도우마다 아닌 전역 상태줄
      },
      sections = {
        lualine_a = { "mode" },
        lualine_b = { "branch", "diff", "diagnostics" },
        lualine_c = { "filename" },
        lualine_x = { "encoding", "fileformat", "filetype" },
        lualine_y = { "progress" },
        lualine_z = { "location" },
      },
    })
  end,
}
```

## 6. which-key.nvim - 단축키 가이드

which-key는 키 입력 후 사용 가능한 다음 키를 팝업으로 표시합니다.

### 설치 및 설정

```lua
-- ~/.config/nvim/lua/plugins/which-key.lua

return {
  "folke/which-key.nvim",
  event = "VeryLazy",
  config = function()
    local wk = require("which-key")
    wk.setup({
      window = {
        border = "rounded",
        position = "bottom",
      },
    })

    -- 그룹 등록
    wk.register({
      ["<leader>f"] = { name = "[F]ind" },
      ["<leader>b"] = { name = "[B]uffer" },
      ["<leader>w"] = { name = "[W]indow" },
      ["<leader>t"] = { name = "[T]ab" },
      ["<leader>c"] = { name = "[C]ode" },
      ["<leader>g"] = { name = "[G]it" },
    })
  end,
}
```

## 7. 컬러스킴

NeoVim의 인기 컬러스킴들입니다.

### catppuccin

```lua
-- ~/.config/nvim/lua/plugins/colorscheme.lua

return {
  "catppuccin/nvim",
  name = "catppuccin",
  priority = 1000,  -- 다른 플러그인보다 먼저 로드
  config = function()
    require("catppuccin").setup({
      flavour = "mocha",  -- latte, frappe, macchiato, mocha
      transparent_background = false,
      integrations = {
        telescope = true,
        neo_tree = true,
        treesitter = true,
        which_key = true,
      },
    })
    vim.cmd.colorscheme("catppuccin")
  end,
}
```

### 다른 인기 테마

```lua
-- Tokyo Night
{ "folke/tokyonight.nvim" }

-- Gruvbox
{ "ellisonleao/gruvbox.nvim" }

-- Nord
{ "shaunsingh/nord.nvim" }

-- Dracula
{ "Mofiqul/dracula.nvim" }
```

## 8. LazyVim 배포판 - 대안적 접근

지금까지 플러그인을 하나씩 설치하는 방법을 배웠다. 하지만 2026년에는 이 모든 것이 사전 구성된 **Neovim 배포판**을 사용하는 것이 더 일반적이다.

### 배포판이란?

"Neovim + lazy.nvim + 사전 구성된 플러그인 세트"를 하나로 묶은 것이다. 설치 즉시 IDE급 환경이 구성된다.

### 주요 배포판 비교 (2026년 기준)

| 배포판 | 기동 시간 | 입문 난이도 | 철학 | 2026 상태 |
|--------|----------|------------|------|----------|
| **LazyVim** | 빠름 (~60%↑) | 쉬움 | "Less is more" | 매우 활발 (추천) |
| NvChad | 최고 (0.02-0.07s) | 쉬움 | 미학 + 성능 | 활발 |
| AstroNvim | 좋음 | 중간 | 완전한 OOTB | 활발 |
| kickstart.nvim | 빠름 | 학습용 | 교육 도구 | 안정 |
| LunarVim | - | - | - | **비추천** (유지보수자 없음) |

### LazyVim을 추천하는 이유

1. **즉시 생산적**: 설치 후 바로 LSP, Telescope, Treesitter, Git 통합이 동작
2. **점진적 커스터마이징**: 기본 설정을 쓰다가 필요할 때 오버라이드
3. **이 챕터의 모든 플러그인이 포함**: telescope, treesitter, neo-tree, lualine, which-key, gitsigns 등
4. **Claude Code 플러그인 추가 용이**: lazy.nvim 기반이라 claudecode.nvim 추가가 간단

### LazyVim + 직접 설정 병행 전략

```
추천 접근:
1. LazyVim을 주력으로 사용 (즉시 생산적)
2. 여유 시간에 kickstart.nvim 코드를 읽으며 내부 구조 학습
3. 이 챕터(Ch10)의 설정 코드로 "왜 이렇게 설정하는지" 이해
```

kickstart.nvim은 배포판이 아니라 "교육용 참조 설정"이다. 주석이 풍부하고 코드가 읽기 쉬워서 Neovim 설정의 원리를 이해하는 데 최적이다.

- [LazyVim 공식](https://www.lazyvim.org/)
- [kickstart.nvim GitHub](https://github.com/nvim-lua/kickstart.nvim)
- [LazyVim vs NvChad 비교](https://www.oreateai.com/blog/lazyvim-vs-nvchad-the-ultimate-neovim-showdown/)

---

## 9. 추천 플러그인 요약

| 플러그인 | 용도 | 우선순위 |
|---------|------|----------|
| **telescope.nvim** | 퍼지 파인더 | 필수 |
| **nvim-treesitter** | 구문 분석 | 필수 |
| **neo-tree.nvim** | 파일 탐색기 | 필수 |
| **lualine.nvim** | 상태표시줄 | 권장 |
| **which-key.nvim** | 단축키 가이드 | 권장 |
| **catppuccin** | 컬러스킴 | 권장 |
| **gitsigns.nvim** | Git 표시 | 권장 |
| **Comment.nvim** | 주석 토글 | 권장 |
| **nvim-autopairs** | 괄호 자동 완성 | 선택 |
| **indent-blankline** | 들여쓰기 가이드 | 선택 |

### 추가 유용한 플러그인

```lua
-- Git 통합
{
  "lewis6991/gitsigns.nvim",
  event = "BufReadPost",
  config = function()
    require("gitsigns").setup()
  end,
}

-- 주석 토글 (gcc, gc)
{
  "numToStr/Comment.nvim",
  keys = { "gc", "gb" },
  config = function()
    require("Comment").setup()
  end,
}

-- 괄호 자동 완성
{
  "windwp/nvim-autopairs",
  event = "InsertEnter",
  config = function()
    require("nvim-autopairs").setup()
  end,
}

-- 들여쓰기 가이드
{
  "lukas-reineke/indent-blankline.nvim",
  event = "BufReadPost",
  config = function()
    require("ibl").setup()
  end,
}
```

## 실습

`practice/configs/full-init.lua`와 `lua/plugins/` 디렉토리로 완전한 설정을 구축합니다.

### 연습 1: lazy.nvim 설치

```lua
-- TODO:
-- 1. lua/config/lazy.lua 생성
-- 2. 부트스트랩 코드 작성
-- 3. init.lua에서 require("config.lazy")
-- 4. NeoVim 재시작 → :Lazy 확인
```

### 연습 2: Telescope 설치

```lua
-- TODO:
-- 1. lua/plugins/telescope.lua 생성
-- 2. 플러그인 스펙 작성
-- 3. :Lazy sync로 설치
-- 4. <leader>ff로 파일 검색 테스트
```

### 연습 3: Treesitter 설치

```lua
-- TODO:
-- 1. lua/plugins/treesitter.lua 생성
-- 2. ensure_installed에 자주 사용하는 언어 추가
-- 3. :TSInstallInfo로 설치 확인
-- 4. 증분 선택 테스트 (Ctrl+Space)
```

### 연습 4: 전체 설정 통합

```
practice/configs/full/
├── init.lua
└── lua/
    ├── config/
    │   ├── options.lua
    │   ├── keymaps.lua
    │   └── lazy.lua
    └── plugins/
        ├── telescope.lua
        ├── treesitter.lua
        ├── neo-tree.lua
        ├── lualine.lua
        ├── which-key.lua
        └── colorscheme.lua
```

## 명령어 요약

| 명령 | 설명 |
|------|------|
| `:Lazy` | 플러그인 관리 UI |
| `:Lazy sync` | 설치 + 업데이트 + 정리 |
| `:Lazy profile` | 로딩 시간 프로파일 |
| `:Telescope find_files` | 파일 검색 |
| `:Telescope live_grep` | 텍스트 검색 |
| `:TSInstall {lang}` | Treesitter 파서 설치 |
| `:TSUpdate` | 파서 업데이트 |
| `:Neotree toggle` | 파일 탐색기 토글 |
| `<leader>ff` | Telescope 파일 검색 |
| `<leader>fg` | Telescope 텍스트 검색 |
| `<leader>e` | Neo-tree 토글 |

## 체크포인트

<details>
<summary>1. lazy.nvim의 지연 로딩(lazy loading)이란?</summary>

플러그인을 NeoVim 시작 시 모두 로드하지 않고, 필요한 시점(특정 키 입력, 명령 실행, 파일 타입 등)에 로드하는 기능입니다. 예를 들어 Telescope를 `keys = { "<leader>ff" }`로 설정하면 `<leader>ff`를 처음 누를 때만 로드됩니다. 이를 통해 시작 시간을 50~200ms로 단축할 수 있습니다. `:Lazy profile`로 각 플러그인의 로딩 시간을 측정할 수 있습니다.

</details>

<details>
<summary>2. treesitter가 기존 구문 하이라이팅보다 우수한 이유는?</summary>

정규식 기반 하이라이팅은 문자열이나 주석 안의 키워드를 잘못 인식하거나, 복잡한 중첩 구조를 처리하지 못합니다. Treesitter는 코드를 AST(Abstract Syntax Tree)로 파싱하여 문법적으로 정확한 하이라이팅을 제공합니다. 또한 텍스트 객체(함수, 클래스 단위 선택), 증분 선택, 정확한 코드 접기 등 추가 기능도 제공합니다. 단, 언어별 파서 설치가 필요합니다.

</details>

<details>
<summary>3. telescope의 live_grep과 find_files의 차이는?</summary>

`find_files`는 **파일명**으로 검색합니다(예: "config.lua"). `live_grep`은 **파일 내용**을 검색합니다(예: "function setup"). live_grep은 ripgrep이 설치되어 있어야 작동하며, 대규모 프로젝트에서도 빠른 전문 검색을 제공합니다. 키 매핑 예: `<leader>ff` = find files, `<leader>fg` = find by grep. 현재 커서 단어를 검색하려면 `grep_string`을 사용합니다.

</details>

---

다음: [11. LSP와 자동완성](./11-lsp-completion.md)
