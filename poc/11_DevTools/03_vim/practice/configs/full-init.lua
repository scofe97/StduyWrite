-- 완전한 NeoVim 설정 (Ch10-11: 플러그인 + LSP)
-- 이 파일을 ~/.config/nvim/init.lua에 복사하여 사용
-- 플러그인 스펙은 lua/plugins/ 디렉토리 참조

-- ========================================
-- Leader 키 (최우선 설정)
-- ========================================
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- ========================================
-- 1. 기본 옵션
-- ========================================

-- 줄번호
vim.opt.number = true
vim.opt.relativenumber = true

-- 마우스 및 클립보드
vim.opt.mouse = "a"
vim.opt.clipboard = "unnamedplus"

-- 탭 및 들여쓰기
vim.opt.tabstop = 4
vim.opt.shiftwidth = 4
vim.opt.expandtab = true
vim.opt.smartindent = true

-- 검색
vim.opt.ignorecase = true
vim.opt.smartcase = true
vim.opt.hlsearch = true
vim.opt.incsearch = true

-- UI
vim.opt.termguicolors = true
vim.opt.scrolloff = 8
vim.opt.signcolumn = "yes"
vim.opt.cursorline = true
vim.opt.wrap = false
vim.opt.showmode = false          -- lualine이 표시하므로 비활성화

-- 분할
vim.opt.splitright = true
vim.opt.splitbelow = true

-- 기타
vim.opt.updatetime = 250
vim.opt.timeoutlen = 300
vim.opt.undofile = true
vim.opt.backup = false
vim.opt.swapfile = false
vim.opt.conceallevel = 0
vim.opt.fileencoding = "utf-8"

-- ========================================
-- 2. 키 매핑
-- ========================================

local keymap = vim.keymap.set

-- Insert 모드 탈출
keymap("i", "jk", "<Esc>", { desc = "Esc 대체" })

-- 빠른 저장/종료
keymap("n", "<leader>w", ":w<CR>", { desc = "저장" })
keymap("n", "<leader>q", ":q<CR>", { desc = "종료" })
keymap("n", "<leader>Q", ":qa!<CR>", { desc = "강제 전체 종료" })

-- 검색 하이라이트 끄기
keymap("n", "<leader>h", ":nohlsearch<CR>", { desc = "검색 하이라이트 끄기" })

-- 윈도우 이동
keymap("n", "<C-h>", "<C-w>h", { desc = "왼쪽 윈도우" })
keymap("n", "<C-j>", "<C-w>j", { desc = "아래 윈도우" })
keymap("n", "<C-k>", "<C-w>k", { desc = "위 윈도우" })
keymap("n", "<C-l>", "<C-w>l", { desc = "오른쪽 윈도우" })

-- 윈도우 크기 조절
keymap("n", "<C-Up>", ":resize +2<CR>", { desc = "높이 증가" })
keymap("n", "<C-Down>", ":resize -2<CR>", { desc = "높이 감소" })
keymap("n", "<C-Left>", ":vertical resize -2<CR>", { desc = "너비 감소" })
keymap("n", "<C-Right>", ":vertical resize +2<CR>", { desc = "너비 증가" })

-- 버퍼 이동
keymap("n", "<leader>bn", ":bnext<CR>", { desc = "다음 버퍼" })
keymap("n", "<leader>bp", ":bprevious<CR>", { desc = "이전 버퍼" })
keymap("n", "<leader>bd", ":bdelete<CR>", { desc = "버퍼 닫기" })
keymap("n", "<S-l>", ":bnext<CR>", { desc = "다음 버퍼" })
keymap("n", "<S-h>", ":bprevious<CR>", { desc = "이전 버퍼" })

-- 줄 이동 (Visual 모드)
keymap("v", "J", ":m '>+1<CR>gv=gv", { desc = "선택 줄 아래로" })
keymap("v", "K", ":m '<-2<CR>gv=gv", { desc = "선택 줄 위로" })

-- 화면 중앙 유지
keymap("n", "<C-d>", "<C-d>zz", { desc = "반 페이지 아래 + 중앙" })
keymap("n", "<C-u>", "<C-u>zz", { desc = "반 페이지 위 + 중앙" })
keymap("n", "n", "nzzzv", { desc = "다음 검색 + 중앙" })
keymap("n", "N", "Nzzzv", { desc = "이전 검색 + 중앙" })

-- 붙여넣기 시 레지스터 유지
keymap("x", "<leader>p", '"_dP', { desc = "레지스터 유지하며 붙여넣기" })

-- 시스템 클립보드
keymap("n", "<leader>y", '"+y', { desc = "시스템 클립보드로 복사" })
keymap("v", "<leader>y", '"+y', { desc = "시스템 클립보드로 복사" })
keymap("n", "<leader>Y", '"+Y', { desc = "줄 시스템 클립보드로 복사" })

-- 블랙홀 레지스터로 삭제
keymap("n", "<leader>d", '"_d', { desc = "블랙홀 삭제" })
keymap("v", "<leader>d", '"_d', { desc = "블랙홀 삭제" })

-- 빠른 명령 모드
keymap("n", ";", ":", { desc = "명령 모드" })

-- 터미널
keymap("t", "<Esc><Esc>", "<C-\\><C-n>", { desc = "터미널 Normal 모드" })
keymap("n", "<leader>tv", ":vsplit | terminal<CR>", { desc = "수직 터미널" })
keymap("n", "<leader>th", ":split | terminal<CR>", { desc = "수평 터미널" })

-- ========================================
-- 3. 자동 명령
-- ========================================

-- 파일 열 때 마지막 위치로 이동
vim.api.nvim_create_autocmd("BufReadPost", {
  pattern = "*",
  callback = function()
    local mark = vim.api.nvim_buf_get_mark(0, '"')
    local lcount = vim.api.nvim_buf_line_count(0)
    if mark[1] > 0 and mark[1] <= lcount then
      pcall(vim.api.nvim_win_set_cursor, 0, mark)
    end
  end,
})

-- 저장 시 trailing whitespace 제거
vim.api.nvim_create_autocmd("BufWritePre", {
  pattern = "*",
  callback = function()
    local save_cursor = vim.fn.getpos(".")
    vim.cmd([[%s/\s\+$//e]])
    vim.fn.setpos(".", save_cursor)
  end,
})

-- Yank 시 하이라이트
vim.api.nvim_create_autocmd("TextYankPost", {
  pattern = "*",
  callback = function()
    vim.highlight.on_yank({ higroup = "IncSearch", timeout = 200 })
  end,
})

-- 터미널 모드에서 줄번호 숨기기
vim.api.nvim_create_autocmd("TermOpen", {
  pattern = "*",
  callback = function()
    vim.opt_local.number = false
    vim.opt_local.relativenumber = false
    vim.opt_local.signcolumn = "no"
  end,
})

-- ========================================
-- 4. lazy.nvim 부트스트랩
-- ========================================

local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
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
vim.opt.rtp:prepend(lazypath)

-- ========================================
-- 5. 플러그인 로드
-- ========================================

require("lazy").setup({
  -- 플러그인 스펙은 lua/plugins/ 디렉토리에서 자동 로드
  { import = "plugins" },
}, {
  ui = {
    border = "rounded",
    icons = {
      cmd = "⌘",
      config = "🛠",
      event = "📅",
      ft = "📂",
      init = "⚙",
      keys = "🗝",
      plugin = "🔌",
      runtime = "💻",
      source = "📄",
      start = "🚀",
      task = "📌",
      lazy = "💤",
    },
  },
  checker = {
    enabled = true,
    notify = false,
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
