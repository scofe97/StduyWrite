---
title: 09_tools MOC
tags: [moc, tools]
status: final
related: []
updated: 2026-05-22
---

# 09_tools
---
> 개발 워크플로우를 구성하는 도구들. tmux, vim, Claude Code, Git 활용법을 모은다.

## 등록된 절

| 절 | 제목 | 다루는 범위 |
|----|------|-----------|
| 01-01 | [Neovim 입문 — 왜 쓰고 무엇을 모르면 시작도 못 하는가](./01-01.Neovim%20입문%20—%20왜%20쓰고%20무엇을%20모르면%20시작도%20못%20하는가.md) | 모달 편집, 연산자+모션, 텍스트 오브젝트, `:help` 사용법 |
| 01-02 | [LazyVim 설치와 디렉토리 구조 — 맥북 기준](./01-02.LazyVim%20설치와%20디렉토리%20구조%20—%20맥북%20기준.md) | brew 의존 도구, `~/.config/nvim` 백업, starter clone, `:checkhealth` 진단 |
| 01-03 | [IntelliJ 사용자를 위한 키맵·기능 매핑표](./01-03.IntelliJ%20사용자를%20위한%20키맵·기능%20매핑표.md) | IntelliJ 동작 → LazyVim 키 매핑, 멀티커서 대체 사고, 끝까지 안 되는 항목 |
| 01-04 | [Java·Spring 개발 환경 — jdtls·nvim-dap·gradle 연동](./01-04.Java·Spring%20개발%20환경%20—%20jdtls·nvim-dap·gradle%20연동.md) | `:LazyExtras` lang.java, jdtls 인덱싱, nvim-dap, IntelliJ 약점·하이브리드 전략 |
| 01-05 | [마크다운 글쓰기 환경 — 한글 IME·프론트매터·미리보기](./01-05.마크다운%20글쓰기%20환경%20—%20한글%20IME·프론트매터·미리보기.md) | `im-select` IME 강제, 프론트매터 LuaSnip, `markdown-preview.nvim`, Drive 동기화 폴더 주의 |

## 경계 기준

특정 언어나 프레임워크에 종속된 도구 설정(예: Spring Boot DevTools)은 해당 카테고리로 가고, 언어 독립적 CLI·터미널·에디터 설정만 여기에 둔다. 단, *에디터 자체를 그 언어 개발에 쓰는* 가이드(예: 10-04 Neovim의 Java 환경)는 에디터 도구로 분류해 본 디렉토리에 둔다.

## 향후 추가 후보

- 10-06: Go/Rust LSP 환경 (필요 시점에 작성)
- 10-07: tmux + nvim 조합 워크플로
- 10-08: lazygit 단독 사용법
