-- LSP 설정 (Ch11)
return {
  {
    "williamboman/mason.nvim",
    cmd = "Mason",
    config = function()
      require("mason").setup({
        ui = {
          border = "rounded",
          icons = {
            package_installed = "✓",
            package_pending = "➜",
            package_uninstalled = "✗",
          },
        },
      })
    end,
  },

  {
    "williamboman/mason-lspconfig.nvim",
    dependencies = { "mason.nvim" },
    config = function()
      require("mason-lspconfig").setup({
        ensure_installed = {
          "lua_ls",       -- Lua
          "ts_ls",        -- TypeScript/JavaScript
          "gopls",        -- Go
          "pyright",      -- Python
          "jdtls",        -- Java
          "rust_analyzer", -- Rust
          "clangd",       -- C/C++
          "jsonls",       -- JSON
          "yamlls",       -- YAML
          "html",         -- HTML
          "cssls",        -- CSS
        },
        automatic_installation = true,
      })
    end,
  },

  {
    "neovim/nvim-lspconfig",
    event = { "BufReadPre", "BufNewFile" },
    dependencies = {
      "mason.nvim",
      "mason-lspconfig.nvim",
      "hrsh7th/cmp-nvim-lsp",
    },
    config = function()
      local lspconfig = require("lspconfig")
      local capabilities = require("cmp_nvim_lsp").default_capabilities()

      -- 진단 표시 설정
      vim.diagnostic.config({
        virtual_text = {
          prefix = "●",
          source = "if_many",
        },
        signs = true,
        underline = true,
        update_in_insert = false,
        severity_sort = true,
        float = {
          border = "rounded",
          source = "always",
        },
      })

      -- 진단 기호 설정
      local signs = {
        Error = " ",
        Warn = " ",
        Hint = " ",
        Info = " ",
      }
      for type, icon in pairs(signs) do
        local hl = "DiagnosticSign" .. type
        vim.fn.sign_define(hl, { text = icon, texthl = hl, numhl = hl })
      end

      -- LSP 서버 연결 시 키 매핑 설정
      vim.api.nvim_create_autocmd("LspAttach", {
        group = vim.api.nvim_create_augroup("UserLspConfig", {}),
        callback = function(ev)
          local map = function(keys, func, desc)
            vim.keymap.set("n", keys, func, { buffer = ev.buf, desc = "LSP: " .. desc })
          end

          -- 네비게이션
          map("gd", vim.lsp.buf.definition, "정의로 이동")
          map("gD", vim.lsp.buf.declaration, "선언으로 이동")
          map("gr", vim.lsp.buf.references, "참조 찾기")
          map("gI", vim.lsp.buf.implementation, "구현으로 이동")
          map("gy", vim.lsp.buf.type_definition, "타입 정의로 이동")

          -- 문서
          map("K", vim.lsp.buf.hover, "문서 보기")
          map("<C-k>", vim.lsp.buf.signature_help, "시그니처 도움말")

          -- 리팩토링
          map("<leader>rn", vim.lsp.buf.rename, "이름 변경")
          map("<leader>ca", vim.lsp.buf.code_action, "코드 액션")
          map("<leader>cf", function()
            vim.lsp.buf.format({ async = true })
          end, "포맷팅")

          -- 진단
          map("[d", vim.diagnostic.goto_prev, "이전 진단")
          map("]d", vim.diagnostic.goto_next, "다음 진단")
          map("<leader>e", vim.diagnostic.open_float, "진단 메시지")
          map("<leader>dl", vim.diagnostic.setloclist, "진단 목록")

          -- 워크스페이스
          map("<leader>wa", vim.lsp.buf.add_workspace_folder, "워크스페이스 폴더 추가")
          map("<leader>wr", vim.lsp.buf.remove_workspace_folder, "워크스페이스 폴더 제거")
          map("<leader>wl", function()
            print(vim.inspect(vim.lsp.buf.list_workspace_folders()))
          end, "워크스페이스 폴더 목록")

          -- 저장 시 자동 포맷팅 (옵션)
          -- local client = vim.lsp.get_client_by_id(ev.data.client_id)
          -- if client.server_capabilities.documentFormattingProvider then
          --   vim.api.nvim_create_autocmd("BufWritePre", {
          --     buffer = ev.buf,
          --     callback = function()
          --       vim.lsp.buf.format({ async = false })
          --     end,
          --   })
          -- end
        end,
      })

      -- 범용 언어 서버 설정
      local servers = {
        "ts_ls",
        "gopls",
        "pyright",
        "rust_analyzer",
        "clangd",
        "jsonls",
        "yamlls",
        "html",
        "cssls",
      }

      for _, server in ipairs(servers) do
        lspconfig[server].setup({
          capabilities = capabilities,
        })
      end

      -- Java는 별도 설정 필요 (jdtls 플러그인 권장)
      lspconfig.jdtls.setup({
        capabilities = capabilities,
      })

      -- Lua는 NeoVim 설정 파일 인식을 위해 별도 설정
      lspconfig.lua_ls.setup({
        capabilities = capabilities,
        settings = {
          Lua = {
            runtime = {
              version = "LuaJIT",
            },
            diagnostics = {
              globals = { "vim" }, -- vim 전역 변수 인식
            },
            workspace = {
              checkThirdParty = false,
              library = {
                vim.env.VIMRUNTIME,
                -- Lazy.nvim 플러그인 경로도 인식
                "${3rd}/luv/library",
              },
            },
            telemetry = {
              enable = false,
            },
            format = {
              enable = true,
              defaultConfig = {
                indent_style = "space",
                indent_size = "2",
              },
            },
          },
        },
      })
    end,
  },
}
