-- 최소 NeoVim 설정 (Ch09: 설정 파일)
-- 이 파일을 ~/.config/nvim/init.lua에 복사하여 사용

-- Leader 키 설정 (다른 설정보다 먼저)
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- ========================================
-- 기본 옵션
-- ========================================

-- 줄번호
vim.opt.number = true            -- 절대 줄번호
vim.opt.relativenumber = true    -- 상대 줄번호

-- 마우스 및 클립보드
vim.opt.mouse = "a"              -- 모든 모드에서 마우스 지원
vim.opt.clipboard = "unnamedplus" -- 시스템 클립보드 사용

-- 탭 및 들여쓰기
vim.opt.tabstop = 4              -- 탭 문자 너비
vim.opt.shiftwidth = 4           -- 들여쓰기 너비
vim.opt.expandtab = true         -- 탭을 스페이스로 변환
vim.opt.smartindent = true       -- 스마트 자동 들여쓰기

-- 검색
vim.opt.ignorecase = true        -- 대소문자 무시
vim.opt.smartcase = true         -- 대문자 포함 시 대소문자 구분
vim.opt.hlsearch = true          -- 검색 결과 하이라이트
vim.opt.incsearch = true         -- 입력 중 즉시 검색

-- UI
vim.opt.termguicolors = true     -- 24비트 색상 지원
vim.opt.scrolloff = 8            -- 스크롤 시 상하 여백
vim.opt.signcolumn = "yes"       -- 왼쪽 여백 항상 표시
vim.opt.cursorline = true        -- 현재 줄 강조
vim.opt.wrap = false             -- 줄바꿈 비활성화

-- 분할
vim.opt.splitright = true        -- 수직 분할 시 오른쪽에
vim.opt.splitbelow = true        -- 수평 분할 시 아래에

-- 기타
vim.opt.updatetime = 250         -- 빠른 반응 속도 (ms)
vim.opt.timeoutlen = 300         -- 키 매핑 대기 시간
vim.opt.undofile = true          -- 영구 undo 파일
vim.opt.backup = false           -- 백업 파일 비활성화
vim.opt.swapfile = false         -- swap 파일 비활성화

-- ========================================
-- 키 매핑
-- ========================================

local keymap = vim.keymap.set
local opts = { silent = true }

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

-- ========================================
-- 자동 명령
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

-- ========================================
-- 컬러스킴
-- ========================================

-- 기본 컬러스킴 설정 (플러그인 없이도 보기 좋게)
vim.cmd([[colorscheme habamax]])

-- 터미널 색상 설정
vim.g.terminal_color_0 = "#282828"
vim.g.terminal_color_8 = "#928374"
