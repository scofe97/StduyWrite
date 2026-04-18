-- 자동완성 설정 (Ch11)
return {
  "hrsh7th/nvim-cmp",
  event = "InsertEnter",
  dependencies = {
    "hrsh7th/cmp-nvim-lsp",    -- LSP 소스
    "hrsh7th/cmp-buffer",      -- 버퍼 단어
    "hrsh7th/cmp-path",        -- 파일 경로
    "hrsh7th/cmp-cmdline",     -- 명령줄
    "L3MON4D3/LuaSnip",        -- 스니펫 엔진
    "saadparwaiz1/cmp_luasnip", -- 스니펫 소스
    "rafamadriz/friendly-snippets", -- 스니펫 모음
  },
  config = function()
    local cmp = require("cmp")
    local luasnip = require("luasnip")

    -- VSCode 스타일 스니펫 로드
    require("luasnip.loaders.from_vscode").lazy_load()

    -- kind 아이콘 (자동완성 항목 타입)
    local kind_icons = {
      Text = "",
      Method = "󰆧",
      Function = "󰊕",
      Constructor = "",
      Field = "󰇽",
      Variable = "󰂓",
      Class = "󰠱",
      Interface = "",
      Module = "",
      Property = "󰜢",
      Unit = "",
      Value = "󰎠",
      Enum = "",
      Keyword = "󰌋",
      Snippet = "",
      Color = "󰏘",
      File = "󰈙",
      Reference = "",
      Folder = "󰉋",
      EnumMember = "",
      Constant = "󰏿",
      Struct = "",
      Event = "",
      Operator = "󰆕",
      TypeParameter = "󰅲",
    }

    cmp.setup({
      snippet = {
        expand = function(args)
          luasnip.lsp_expand(args.body)
        end,
      },

      -- 윈도우 스타일
      window = {
        completion = cmp.config.window.bordered(),
        documentation = cmp.config.window.bordered(),
      },

      -- 키 매핑
      mapping = cmp.mapping.preset.insert({
        -- 항목 이동
        ["<C-n>"] = cmp.mapping.select_next_item(),
        ["<C-p>"] = cmp.mapping.select_prev_item(),

        -- 문서 스크롤
        ["<C-b>"] = cmp.mapping.scroll_docs(-4),
        ["<C-f>"] = cmp.mapping.scroll_docs(4),

        -- 완성 트리거
        ["<C-Space>"] = cmp.mapping.complete(),

        -- 완성 취소
        ["<C-e>"] = cmp.mapping.abort(),

        -- 선택 확인
        ["<CR>"] = cmp.mapping.confirm({ select = true }),

        -- Tab으로 순환 및 스니펫 점프
        ["<Tab>"] = cmp.mapping(function(fallback)
          if cmp.visible() then
            cmp.select_next_item()
          elseif luasnip.expand_or_jumpable() then
            luasnip.expand_or_jump()
          else
            fallback()
          end
        end, { "i", "s" }),

        -- Shift+Tab으로 역방향
        ["<S-Tab>"] = cmp.mapping(function(fallback)
          if cmp.visible() then
            cmp.select_prev_item()
          elseif luasnip.jumpable(-1) then
            luasnip.jump(-1)
          else
            fallback()
          end
        end, { "i", "s" }),
      }),

      -- 완성 소스 (우선순위 순)
      sources = cmp.config.sources({
        { name = "nvim_lsp" },   -- LSP (최우선)
        { name = "luasnip" },    -- 스니펫
      }, {
        { name = "buffer", keyword_length = 3 },  -- 버퍼 단어 (3글자 이상)
        { name = "path" },       -- 파일 경로
      }),

      -- 완성 항목 포맷팅
      formatting = {
        format = function(entry, vim_item)
          -- Kind 아이콘 표시
          vim_item.kind = string.format("%s %s", kind_icons[vim_item.kind], vim_item.kind)

          -- 소스 표시
          vim_item.menu = ({
            nvim_lsp = "[LSP]",
            luasnip = "[Snippet]",
            buffer = "[Buffer]",
            path = "[Path]",
          })[entry.source.name]

          return vim_item
        end,
      },

      -- 실험적 기능
      experimental = {
        ghost_text = true, -- 미리보기 텍스트 표시
      },
    })

    -- 명령줄 완성 (/ 검색)
    cmp.setup.cmdline("/", {
      mapping = cmp.mapping.preset.cmdline(),
      sources = {
        { name = "buffer" },
      },
    })

    -- 명령줄 완성 (: 명령)
    cmp.setup.cmdline(":", {
      mapping = cmp.mapping.preset.cmdline(),
      sources = cmp.config.sources({
        { name = "path" },
      }, {
        { name = "cmdline" },
      }),
    })

    -- LuaSnip 설정
    luasnip.config.set_config({
      history = true,          -- 스니펫 히스토리
      updateevents = "TextChanged,TextChangedI", -- 동적 업데이트
      enable_autosnippets = true,
    })

    -- 커스텀 스니펫 (예시)
    local ls = luasnip
    local s = ls.snippet
    local t = ls.text_node
    local i = ls.insert_node

    ls.add_snippets("all", {
      s("todo", {
        t("TODO: "),
        i(1, "description"),
      }),
      s("fixme", {
        t("FIXME: "),
        i(1, "description"),
      }),
    })

    ls.add_snippets("lua", {
      s("req", {
        t('local '),
        i(1, "module"),
        t(' = require("'),
        i(2, "module"),
        t('")'),
      }),
    })

    ls.add_snippets("typescript", {
      s("log", {
        t("console.log("),
        i(1, "value"),
        t(");"),
      }),
    })
  end,
}
