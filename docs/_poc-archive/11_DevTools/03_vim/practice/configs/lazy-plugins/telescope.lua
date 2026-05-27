-- Telescope 퍼지 파인더 (Ch10)
return {
  "nvim-telescope/telescope.nvim",
  branch = "0.1.x",
  dependencies = {
    "nvim-lua/plenary.nvim",
    { "nvim-telescope/telescope-fzf-native.nvim", build = "make" },
  },
  keys = {
    { "<leader>ff", "<cmd>Telescope find_files<cr>", desc = "파일 찾기" },
    { "<leader>fg", "<cmd>Telescope live_grep<cr>", desc = "텍스트 검색" },
    { "<leader>fb", "<cmd>Telescope buffers<cr>", desc = "버퍼 목록" },
    { "<leader>fr", "<cmd>Telescope oldfiles<cr>", desc = "최근 파일" },
    { "<leader>fh", "<cmd>Telescope help_tags<cr>", desc = "도움말 검색" },
    { "<leader>fd", "<cmd>Telescope diagnostics<cr>", desc = "진단 목록" },
    { "<leader>fs", "<cmd>Telescope lsp_document_symbols<cr>", desc = "심볼 검색" },
    { "<leader>fS", "<cmd>Telescope lsp_workspace_symbols<cr>", desc = "워크스페이스 심볼" },
    { "<leader>fc", "<cmd>Telescope commands<cr>", desc = "명령 검색" },
    { "<leader>fk", "<cmd>Telescope keymaps<cr>", desc = "키맵 검색" },
    { "<leader>f/", "<cmd>Telescope current_buffer_fuzzy_find<cr>", desc = "버퍼 내 검색" },
  },
  config = function()
    local telescope = require("telescope")
    local actions = require("telescope.actions")

    telescope.setup({
      defaults = {
        -- 무시할 파일 패턴
        file_ignore_patterns = {
          "node_modules",
          ".git/",
          "dist/",
          "build/",
          "target/",
          "*.class",
          "*.jar",
        },

        -- 레이아웃
        layout_strategy = "horizontal",
        layout_config = {
          prompt_position = "top",
          horizontal = {
            width = 0.9,
            height = 0.8,
            preview_width = 0.6,
          },
        },

        -- 정렬
        sorting_strategy = "ascending",

        -- 키맵
        mappings = {
          i = {
            ["<C-n>"] = actions.move_selection_next,
            ["<C-p>"] = actions.move_selection_previous,
            ["<C-j>"] = actions.move_selection_next,
            ["<C-k>"] = actions.move_selection_previous,
            ["<C-c>"] = actions.close,
            ["<Esc>"] = actions.close,
            ["<CR>"] = actions.select_default,
            ["<C-x>"] = actions.select_horizontal,
            ["<C-v>"] = actions.select_vertical,
            ["<C-t>"] = actions.select_tab,
            ["<C-u>"] = actions.preview_scrolling_up,
            ["<C-d>"] = actions.preview_scrolling_down,
          },
          n = {
            ["q"] = actions.close,
            ["<Esc>"] = actions.close,
            ["<CR>"] = actions.select_default,
            ["<C-x>"] = actions.select_horizontal,
            ["<C-v>"] = actions.select_vertical,
            ["<C-t>"] = actions.select_tab,
            ["j"] = actions.move_selection_next,
            ["k"] = actions.move_selection_previous,
            ["gg"] = actions.move_to_top,
            ["G"] = actions.move_to_bottom,
          },
        },
      },

      pickers = {
        find_files = {
          hidden = true, -- 숨김 파일 포함
        },
        live_grep = {
          additional_args = function()
            return { "--hidden" } -- 숨김 파일 포함
          end,
        },
        buffers = {
          sort_lastused = true,
          mappings = {
            i = {
              ["<C-d>"] = actions.delete_buffer,
            },
            n = {
              ["dd"] = actions.delete_buffer,
            },
          },
        },
      },
    })

    -- fzf 확장 로드 (성능 향상)
    telescope.load_extension("fzf")
  end,
}
