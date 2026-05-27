-- Treesitter 구문 분석 (Ch10)
return {
  "nvim-treesitter/nvim-treesitter",
  build = ":TSUpdate",
  event = { "BufReadPre", "BufNewFile" },
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
        "query",
        "javascript",
        "typescript",
        "tsx",
        "java",
        "kotlin",
        "go",
        "python",
        "rust",
        "c",
        "cpp",
        "json",
        "yaml",
        "toml",
        "html",
        "css",
        "scss",
        "bash",
        "markdown",
        "markdown_inline",
        "dockerfile",
        "sql",
        "regex",
      },

      -- 파일 열 때 자동 설치
      auto_install = true,

      -- 구문 강조
      highlight = {
        enable = true,
        additional_vim_regex_highlighting = false,
      },

      -- 자동 들여쓰기
      indent = {
        enable = true,
      },

      -- 점진적 선택
      incremental_selection = {
        enable = true,
        keymaps = {
          init_selection = "<C-space>",      -- 선택 시작
          node_incremental = "<C-space>",    -- 노드 확장
          scope_incremental = false,         -- 비활성화
          node_decremental = "<bs>",         -- 노드 축소
        },
      },

      -- 텍스트 객체
      textobjects = {
        select = {
          enable = true,
          lookahead = true, -- 다음 객체로 자동 이동

          keymaps = {
            -- 함수
            ["af"] = "@function.outer",       -- a function (전체)
            ["if"] = "@function.inner",       -- inner function (본문만)

            -- 클래스
            ["ac"] = "@class.outer",          -- a class (전체)
            ["ic"] = "@class.inner",          -- inner class (본문만)

            -- 파라미터/인자
            ["aa"] = "@parameter.outer",      -- a argument
            ["ia"] = "@parameter.inner",      -- inner argument

            -- 조건문
            ["ai"] = "@conditional.outer",    -- a conditional
            ["ii"] = "@conditional.inner",    -- inner conditional

            -- 반복문
            ["al"] = "@loop.outer",           -- a loop
            ["il"] = "@loop.inner",           -- inner loop

            -- 블록
            ["ab"] = "@block.outer",          -- a block
            ["ib"] = "@block.inner",          -- inner block

            -- 주석
            ["a/"] = "@comment.outer",        -- a comment
          },
        },

        -- 텍스트 객체 간 이동
        move = {
          enable = true,
          set_jumps = true, -- jumplist에 추가

          goto_next_start = {
            ["]f"] = "@function.outer",
            ["]c"] = "@class.outer",
            ["]a"] = "@parameter.outer",
          },

          goto_next_end = {
            ["]F"] = "@function.outer",
            ["]C"] = "@class.outer",
            ["]A"] = "@parameter.outer",
          },

          goto_previous_start = {
            ["[f"] = "@function.outer",
            ["[c"] = "@class.outer",
            ["[a"] = "@parameter.outer",
          },

          goto_previous_end = {
            ["[F"] = "@function.outer",
            ["[C"] = "@class.outer",
            ["[A"] = "@parameter.outer",
          },
        },

        -- 스왑 (파라미터 순서 변경)
        swap = {
          enable = true,
          swap_next = {
            ["<leader>sn"] = "@parameter.inner",  -- swap next
          },
          swap_previous = {
            ["<leader>sp"] = "@parameter.inner",  -- swap previous
          },
        },
      },

      -- 폴딩 (코드 접기)
      fold = {
        enable = true,
      },
    })

    -- Treesitter 기반 폴딩 활성화
    vim.opt.foldmethod = "expr"
    vim.opt.foldexpr = "nvim_treesitter#foldexpr()"
    vim.opt.foldenable = false  -- 파일 열 때 접기 비활성화 (수동 제어)
  end,
}
