# Vim 생태계 조사 (2026년 기준)

> **목적**: IntelliJ + Claude Code CLI 사용자가 입문하기 좋은 Vim 에디터/배포판 선택
> **조사일**: 2026-02-13

---

## 1. 핵심 결론 (TL;DR)

### 추천 조합: **IdeaVim + LazyVim**

| 환경 | 도구 | 비중 | 이유 |
|------|------|------|------|
| IntelliJ (주력) | **IdeaVim** | 80% | IDE 기능 유지하면서 Vim 모션 학습 |
| 터미널 (Claude Code) | **LazyVim** (Neovim) | 20% | Claude Code 네이티브 플러그인, 동일 키바인딩 |

**핵심 근거**: Vim 키바인딩을 한 번 익히면 IntelliJ(IdeaVim)와 터미널(LazyVim) 양쪽에서 동일하게 사용할 수 있어 학습 투자 대비 효율이 가장 높다. Helix는 입문이 더 쉽지만 IntelliJ 플러그인이 없고 Claude Code 통합도 없어서 키바인딩을 이중으로 외워야 하는 문제가 있다.

---

## 2. 코어 에디터 비교

### 2.1 전체 비교표

| 항목 | Vim | **Neovim** | Helix | Kakoune | Vis |
|------|-----|-----------|-------|---------|-----|
| **편집 모델** | Action → Target | Action → Target | Selection → Action | Selection → Action | Action → Target |
| **입문 난이도** | 높음 | 중간 (배포판 사용시) | **낮음** | 중간 | 중간 |
| **IntelliJ 통합** | IdeaVim | IdeaVim (동일 키) | **없음** | 없음 | 없음 |
| **Claude Code 통합** | 터미널만 | **네이티브 플러그인** | 터미널만 | 터미널만 | 터미널만 |
| **플러그인 생태계** | 성숙 (VimScript) | **최대** (Lua) | 없음 (개발중) | 소규모 | 최소 |
| **설정 언어** | VimScript | **Lua** | TOML | Shell script | Lua |
| **성능** | 빠름 | 빠름 | 매우 빠름 (Rust) | 빠름 | 가벼움 |
| **커뮤니티** | 성숙/안정 | **가장 활발** | 성장중 | 소규모 | 니치 |
| **개발 활성도** | 유지보수 | **가장 활발** | 활발 | 안정 | 유지보수 |

### 2.2 편집 모델 차이 (가장 중요한 선택 기준)

```
Vim/Neovim (Action-first):     d  →  w     "단어를 삭제해"
                               동작   대상   (결과를 미리 볼 수 없음)

Helix/Kakoune (Selection-first): w  →  d    "단어를 선택하고 → 삭제"
                                 대상   동작  (선택 영역이 하이라이트되어 미리 보임)
```

Selection-first가 직관적이지만, IdeaVim은 Vim 키바인딩만 지원하므로 **Vim 스타일을 배우는 것이 IntelliJ 사용자에게는 필수**다.

### 2.3 에디터별 상세

#### Neovim - 추천
- **장점**: Lua 기반 설정, Tree-sitter/LSP 내장, 배포판으로 즉시 사용 가능, Claude Code 네이티브 연동
- **단점**: 바닐라 설정은 복잡, 배포판 선택이 필요
- **Claude Code 플러그인**: `coder/claudecode.nvim` (공식 VSCode 확장과 100% 프로토콜 호환)
- [Replacing Cursor With Neovim and Claude Code](https://danielmiessler.com/blog/replacing-cursor-with-neovim-claude-code)

#### Helix - 차선
- **장점**: 설정 없이 즉시 사용, LSP/Tree-sitter 내장, Selection-first로 학습 직관적
- **단점**: 플러그인 시스템 미완성 (Scheme 기반 개발중), IntelliJ 통합 없음, Claude Code 통합 없음
- **판단**: 단독 터미널 에디터로는 우수하지만, IntelliJ + Claude Code 조합에서는 키바인딩 불일치 문제가 크다
- [Helix vs Neovim Comparison](https://elsewebdevelopment.com/neovim-vs-helix-which-is-the-best-vi-vim-style-modal-editor/)
- [Helix Plugin System Discussion](https://github.com/helix-editor/helix/discussions/3806)

#### Vim (Classic)
- **장점**: 가장 안정적, 모든 서버에 설치됨, IdeaVim 호환
- **단점**: VimScript 기반으로 확장이 느림, 현대적 기능(LSP, Tree-sitter) 부족
- **판단**: 서버 관리용으로는 여전히 유용하지만, 2026년 개발 환경으로는 Neovim이 상위호환

#### Kakoune
- **장점**: Selection-first 모델의 원조, 깔끔한 설계
- **단점**: 작은 커뮤니티, IDE 통합 없음
- **판단**: Helix가 Kakoune의 철학을 더 발전시킨 후계자

#### Vis
- **장점**: Plan 9의 구조적 정규식 지원, 매우 가벼움
- **단점**: 니치한 커뮤니티, 실용성 제한적
- **판단**: 학술적 관심 외에는 추천하지 않음

---

## 3. Neovim 배포판 비교

배포판은 "Neovim + 사전 구성된 플러그인 세트"로, 바닐라 Neovim의 복잡한 초기 설정을 건너뛸 수 있게 해준다.

### 3.1 전체 비교표

| 항목 | **LazyVim** | NvChad | AstroNvim | kickstart.nvim | mini.nvim | LunarVim |
|------|-----------|--------|-----------|----------------|-----------|----------|
| **입문 난이도** | **쉬움** | 쉬움 | 중간 | 학습용 | 중간 | - |
| **기동 시간** | 빠름 (~60%↑) | **최고** (0.02-0.07s) | 좋음 | 빠름 | 빠름 | - |
| **기본 플러그인** | 34개 (lazy-load) | 최소 | 가장 많음 | ~15개 | 40+ 모듈 | - |
| **커스터마이징** | 점진적 확장 | 테마 강점 | 깊은 모듈성 | 직접 구성 | 모듈 선택 | - |
| **철학** | "Less is more" | 미학 + 성능 | 완전한 OOTB | 교육 도구 | Swiss Army knife | - |
| **2026 상태** | **매우 활발** | 활발 | 활발 | 안정 | 활발 | **비추천** |

### 3.2 배포판별 상세

#### LazyVim - 추천
- **왜 추천하는가**: 설치 즉시 생산적, 점진적 커스터마이징 가능, lazy.nvim 패키지 매니저 기반으로 기동 속도 우수
- **적합한 사람**: "일단 빠르게 쓰고, 점차 이해하겠다"는 접근
- **추천 학습 전략**: LazyVim으로 시작 → 병행하여 kickstart.nvim으로 내부 구조 학습
- [LazyVim vs NvChad Showdown](https://www.oreateai.com/blog/lazyvim-vs-nvchad-the-ultimate-neovim-showdown/)
- [How LazyVim Differs](https://lazynvim.com/how-is-lazyvim-different-from-other-neovim-distributions/)

#### NvChad
- **강점**: 기동 시간 최고 (93% lazy-load), 아름다운 UI/테마
- **약점**: 안정성을 위해 약간의 튜닝 필요
- **적합한 사람**: 에디터 외관에 가치를 두는 사용자
- [NvChad Official](https://nvchad.com/)

#### AstroNvim
- **강점**: OOTB 완성도 최고, 40+ 언어팩 (AstroCommunity), 활발한 Discord
- **약점**: 학습 곡선이 상대적으로 높음, 최적화에 추가 작업 필요
- **적합한 사람**: 풀 커스터마이징을 원하는 고급 사용자
- [AstroNvim Docs](https://docs.astronvim.com/)

#### kickstart.nvim - 학습 보조용 추천
- **목적**: 배포판이 아닌 "교육용 참조 설정"
- **강점**: 코드가 읽기 쉽고 주석이 풍부, Neovim 설정을 근본적으로 이해하는 데 최적
- **추천 사용법**: LazyVim을 주력으로 쓰면서, 여유 시간에 kickstart.nvim 코드를 읽으며 Lua 설정 학습
- [kickstart.nvim GitHub](https://github.com/nvim-lua/kickstart.nvim)

#### mini.nvim
- **컨셉**: 40+ 독립 Lua 모듈 라이브러리, 필요한 것만 골라 사용
- **강점**: 모듈 독립성 (의존성 없음), LazyVim과 함께 사용 가능 (mini.ai, mini.diff 등)
- **적합한 사람**: 직접 에디터를 조립하고 싶은 사용자
- [mini.nvim GitHub](https://github.com/nvim-mini/mini.nvim)

#### LunarVim - 비추천
- **상태**: 메인 개발자가 AstroNvim으로 이동, 활발한 유지보수자 없음
- **판단**: 신규 프로젝트에서 사용 금지
- [LunarVim Status Discussion](https://github.com/LunarVim/LunarVim/discussions/4627)

---

## 4. IDE Vim 플러그인 비교

| 항목 | **IdeaVim** | VSCodeVim | vscode-neovim | Zed Vim Mode |
|------|-----------|-----------|---------------|--------------|
| **IDE** | IntelliJ/JetBrains | VSCode | VSCode | Zed |
| **구현 방식** | 자체 엔진 | TypeScript 에뮬레이션 | **실제 Neovim 내장** | 자체 구현 |
| **모드 지원** | Normal/Insert/Visual/Ex | Normal/Insert/Visual | 전체 | Normal/Insert/Visual |
| **성능** | 좋음 | **느림** (장시간 사용 시 1key/sec 지연) | 빠름 | 빠름 (Rust) |
| **Vim 호환도** | 높음 | 중간 | **최고** | 중간 |
| **유지보수** | JetBrains 공식 | 커뮤니티 | 커뮤니티 (활발) | Zed 팀 |
| **특이 기능** | IDE 리팩토링 연동, 문법 인식 join, 자동 import | 편의 기능 | 실제 Neovim init.lua 사용 가능 | Tree-sitter 네비게이션 |

### IdeaVim 상세 (IntelliJ 사용자에게 가장 중요)

**지원 플러그인 에뮬레이션**:
- EasyMotion (빠른 커서 이동)
- Surround (괄호/따옴표 감싸기)
- NERDTree (파일 탐색)
- Which-Key (키바인딩 검색 - **입문자 필수**)
- Commentary (주석 토글)
- Multiple-cursors

**IDE 연동 장점**:
- `J` (join): 문법 인식 줄 합치기
- `p` (paste): 자동 import 추가 + 코드 포매팅
- `:action` 명령으로 모든 IntelliJ 액션 호출 가능

**참조**:
- [IdeaVim Official](https://lp.jetbrains.com/ideavim/)
- [IdeaVim GitHub](https://github.com/JetBrains/ideavim)
- [Practical IdeaVim Setup](https://medium.com/@dbilici/a-practical-ideavim-setup-for-intellij-idea-cf74222e7b45)

---

## 5. Claude Code 통합 비교

| 도구 | Claude Code 연동 | 방식 | 비고 |
|------|-----------------|------|------|
| **Neovim (LazyVim)** | **네이티브 플러그인** | `claudecode.nvim` - 공식 VSCode 확장과 100% 프로토콜 호환 | 분할 터미널에서 Claude 실행, 파일 컨텍스트 자동 전달 |
| IntelliJ | 공식 확장 | JetBrains Marketplace | Claude Code 공식 지원 |
| Helix | 없음 | 별도 터미널 | 파일 컨텍스트 수동 전달 |
| Zed | AI 내장 | Zed 자체 AI 통합 | Claude API 직접 연동 가능하나 Claude Code CLI와는 별개 |

### Neovim Claude Code 플러그인 주요 3종

1. **[coder/claudecode.nvim](https://github.com/coder/claudecode.nvim)** - 순수 Lua, 의존성 0, VSCode 확장 프로토콜 100% 호환
2. **[greggh/claude-code.nvim](https://github.com/greggh/claude-code.nvim)** - 분할 터미널 기반, 간편한 설정
3. **[avifenesh/claucode.nvim](https://github.com/avifenesh/claucode.nvim)** - 에디터 ↔ CLI 브릿지

**워크플로우 예시**: Ghostty 터미널 3-pane 구성 (Neovim | Claude Code | 터미널)
- [Neovim + Claude Code + Ghostty Integration](https://danielmiessler.com/blog/claude-code-neovim-ghostty-integration)

---

## 6. 터미널 멀티플렉서

| 항목 | tmux | Zellij |
|------|------|--------|
| **성숙도** | 업계 표준 | 신생 (2021~) |
| **Vim 연동** | vim-tmux-navigator 플러그인 | 자체 모달 편집 (Vim과 유사) |
| **학습 곡선** | 중간 | **쉬움** (TUI 가이드 표시) |
| **안정성** | 매우 높음 | 좋음 (빠른 pane 전환 시 간헐적 이슈) |
| **설정** | `.tmux.conf` | KDL 포맷 |

**추천**: tmux (안정성 + 자료 풍부). 이미 기존 01_tmux 학습 프로젝트가 있으므로 연계 가능.

---

## 7. 최종 추천 학습 경로

### Phase 1: IdeaVim 입문 (1~2주)

```
목표: Vim 모션의 기본 문법 체계 체득
환경: IntelliJ IDEA + IdeaVim 플러그인
```

1. `vimtutor` 매일 1회 실행 (목표: 5분 내 완주)
2. IdeaVim 설치 → Which-Key 플러그인 활성화
3. 핵심 모션 집중: `hjkl`, `w/b/e`, `d/c/y` + 텍스트 오브젝트 (`iw`, `i"`, `ip`)
4. [vim.rtorr.com](http://vim.rtorr.com) 치트시트 상시 오픈

### Phase 2: IdeaVim 심화 (3~4주)

```
목표: 일상 코딩에서 마우스 의존도 50% 감소
환경: IntelliJ IDEA + .ideavimrc 커스터마이징
```

1. 검색/치환: `/`, `*`, `:%s`
2. 마크와 점프: `m`, `'`, `Ctrl-o`, `Ctrl-i`
3. 비주얼 모드: `v`, `V`, `Ctrl-v`
4. `.ideavimrc`에 IDE 액션 매핑 추가

### Phase 3: LazyVim 터미널 환경 (5~6주)

```
목표: Claude Code CLI와 통합된 터미널 편집 환경 구축
환경: LazyVim + claudecode.nvim + tmux
```

1. LazyVim 설치 및 기본 사용
2. claudecode.nvim 플러그인 설정
3. Telescope (퍼지 파인더), LSP 네비게이션 학습
4. tmux 연동 (vim-tmux-navigator)

### Phase 4: 워크플로우 통합 (7~8주)

```
목표: IntelliJ ↔ 터미널 간 자연스러운 전환
환경: 전체 통합
```

1. 매크로 (`q` 레지스터)
2. 버퍼/윈도우 관리
3. 워크플로우 최적화: IntelliJ(코딩) → 터미널(Claude Code + LazyVim) → git
4. kickstart.nvim 코드 읽기로 Neovim 내부 구조 이해

---

## 8. Helix를 선택하지 않는 이유 (상세)

Helix는 단독 에디터로는 2026년 가장 입문하기 쉬운 모달 에디터다. 하지만 이 프로젝트의 맥락에서는 다음 이유로 차선:

| 문제 | 설명 |
|------|------|
| **키바인딩 불일치** | Helix(Selection→Action) vs IdeaVim(Action→Target)으로 근본적으로 다른 근육 기억을 요구 |
| **IntelliJ 통합 없음** | IdeaVim은 Vim 키만 지원. IntelliJ에서 Helix 키를 쓸 수 없음 |
| **Claude Code 플러그인 없음** | Neovim에는 네이티브 플러그인이 3종 이상 존재 |
| **플러그인 시스템 미완성** | 2026년 현재도 Scheme 기반 플러그인 시스템 개발 중 |
| **이중 학습 비용** | 터미널(Helix) + IDE(IdeaVim/Vim) 두 가지 체계를 배워야 함 |

**예외**: 만약 IntelliJ를 사용하지 않고 순수 터미널 개발만 한다면 Helix가 최적의 선택이 될 수 있다.

---

## 9. 기존 커리큘럼과의 관계

기존 `learning/` 15챕터 커리큘럼은 Neovim + IdeaVim 중심으로 이미 잘 구성되어 있다. 이 조사 결과는 그 선택이 2026년에도 여전히 최적임을 확인해준다.

**기존 커리큘럼 보완 제안**:
- `00-setup.md`에 LazyVim 설치 가이드 추가 (현재는 바닐라 Neovim만 다룰 수 있음)
- `13-claude-code.md`에 `claudecode.nvim` 플러그인 설정 추가
- `10-plugins.md`에서 LazyVim 배포판 소개 섹션 추가

---

## 참조 링크

### 에디터 비교
- [Neovim vs Helix](https://elsewebdevelopment.com/neovim-vs-helix-which-is-the-best-vi-vim-style-modal-editor/)
- [From Helix to Neovim](https://pawelgrzybek.com/from-helix-to-neovim/)
- [Notes on switching to Helix from Vim](https://jvns.ca/blog/2025/10/10/notes-on-switching-to-helix-from-vim/)
- [Should you learn Vim in 2026](https://app.daily.dev/posts/should-you-learn-vim-in-2026-e507s4eho)

### Neovim 배포판
- [What's the BEST Neovim Distro?](https://app.daily.dev/posts/4c5fbmmde)
- [LazyVim vs NvChad Showdown](https://www.oreateai.com/blog/lazyvim-vs-nvchad-the-ultimate-neovim-showdown/)
- [Neovim Configuration Distributions](https://lazyman.dev/posts/Configuration-Distributions/)
- [kickstart.nvim](https://github.com/nvim-lua/kickstart.nvim)
- [mini.nvim](https://github.com/nvim-mini/mini.nvim)

### IdeaVim
- [IdeaVim Official](https://lp.jetbrains.com/ideavim/)
- [Getting Started with IdeaVim](https://ikenox.info/blog/getting-started-ideavim/)
- [Vim Motions with IntelliJ IDEA](https://medium.com/wearewaes/vim-motions-with-intellij-idea-38a9d0bf3408)
- [Practical IdeaVim Setup](https://medium.com/@dbilici/a-practical-ideavim-setup-for-intellij-idea-cf74222e7b45)

### Claude Code + Neovim
- [claudecode.nvim](https://github.com/coder/claudecode.nvim)
- [claude-code.nvim](https://github.com/greggh/claude-code.nvim)
- [Replacing Cursor With Neovim and Claude Code](https://danielmiessler.com/blog/replacing-cursor-with-neovim-claude-code)
- [Neovim + Claude Code + Ghostty](https://danielmiessler.com/blog/claude-code-neovim-ghostty-integration)
- [Configuring Neovim for Claude Code](https://xata.io/blog/configuring-neovim-coding-agents)

### 학습 자료
- [Learn-Vim GitHub Guide](https://github.com/iggredible/Learn-Vim)
- [How To Learn Vim: Four Week Plan](https://peterxjang.com/blog/how-to-learn-vim-a-four-week-plan.html)
- [LearnVim Interactive](https://www.learnvim.com/)
- [8 Best Vim Courses for 2026](https://www.classcentral.com/report/best-vim-courses/)

### 기타
- [Zed Vim Mode](https://zed.dev/docs/vim)
- [Helix Plugin System Discussion](https://github.com/helix-editor/helix/discussions/3806)
- [tmux vs Zellij](https://tmuxai.dev/tmux-vs-zellij/)
