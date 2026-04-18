# Vim 생태계 학습

개발 생산성 향상을 위한 Vim 모션과 Neovim/IdeaVim/Claude Code 통합 워크플로우 학습

---

## 생태계 조사

2026년 Vim 생태계(Neovim, Helix, Kakoune, Zed 등)를 종합 조사하고, IntelliJ + Claude Code 사용자에게 최적인 조합을 선정했다.

**[INVESTIGATE.md](./INVESTIGATE.md)** - 전체 조사 결과 (에디터 비교, 배포판 비교, 추천 학습 경로)

**결론**: **IdeaVim + LazyVim(Neovim)** 조합이 최적
- Vim 키바인딩 통일 (IntelliJ ↔ 터미널)
- Claude Code 네이티브 플러그인 지원 (claudecode.nvim)
- LazyVim으로 즉시 IDE급 환경 구축

---

## 학습 목표

1. Vim 모션 문법 체계 완전 습득
2. IdeaVim으로 IntelliJ에서 Vim 모션 활용
3. LazyVim(Neovim) IDE급 터미널 환경 구축
4. Claude Code + Neovim 통합 워크플로우

---

## 커리큘럼

| 순서 | 파일 | 주제 | 예상 시간 |
|------|------|------|-----------|
| 00 | [00-setup](./learning/00-setup.md) | 환경 설정 | 10분 |
| 01 | [01-modes](./learning/01-modes.md) | 모드 이해 | 20분 |
| 02 | [02-navigation](./learning/02-navigation.md) | 내비게이션 | 30분 |
| 03 | [03-operators-motions](./learning/03-operators-motions.md) | 연산자와 모션 | 30분 |
| 04 | [04-editing-essentials](./learning/04-editing-essentials.md) | 편집 필수기 | 25분 |
| 05 | [05-registers-clipboard](./learning/05-registers-clipboard.md) | 레지스터와 클립보드 | 20분 |
| 06 | [06-search-replace](./learning/06-search-replace.md) | 검색과 치환 | 25분 |
| 07 | [07-visual-mode](./learning/07-visual-mode.md) | 비주얼 모드 | 20분 |
| 08 | [08-buffers-windows](./learning/08-buffers-windows.md) | 버퍼/윈도우/탭 | 25분 |
| 09 | [09-config](./learning/09-config.md) | 설정 파일 | 30분 |
| 10 | [10-plugins](./learning/10-plugins.md) | NeoVim 플러그인 | 40분 |
| 11 | [11-lsp-completion](./learning/11-lsp-completion.md) | LSP와 자동완성 | 30분 |
| 12 | [12-ideavim](./learning/12-ideavim.md) | IdeaVim | 30분 |
| 13 | [13-claude-code](./learning/13-claude-code.md) | Claude Code 통합 | 25분 |
| 14 | [14-workflow](./learning/14-workflow.md) | 실전 워크플로우 | 25분 |

---

## 진행 상태

- [ ] 00-setup: 환경 설정
- [ ] 01-modes: 모드 이해
- [ ] 02-navigation: 내비게이션
- [ ] 03-operators-motions: 연산자와 모션
- [ ] 04-editing-essentials: 편집 필수기
- [ ] 05-registers-clipboard: 레지스터와 클립보드
- [ ] 06-search-replace: 검색과 치환
- [ ] 07-visual-mode: 비주얼 모드
- [ ] 08-buffers-windows: 버퍼/윈도우/탭
- [ ] 09-config: 설정 파일
- [ ] 10-plugins: NeoVim 플러그인
- [ ] 11-lsp-completion: LSP와 자동완성
- [ ] 12-ideavim: IdeaVim
- [ ] 13-claude-code: Claude Code 통합
- [ ] 14-workflow: 실전 워크플로우

---

## 학습 방식

각 learning 파일을 순서대로 따라가며:
1. **개념 학습**: 왜 필요한지 이해
2. **명령어 실습**: 직접 에디터에서 실행
3. **체크포인트**: 이해도 확인

---

## 학습 경로

### Foundation (00-04)
Vim의 기본 철학과 핵심 모션을 익히는 단계입니다. 이 단계를 완료하면 Vim 모션의 문법 체계를 이해하고 기본적인 편집 작업을 할 수 있습니다.

### Intermediate (05-08)
레지스터, 검색/치환, 비주얼 모드, 버퍼/윈도우 관리 등 실무에서 필수적인 중급 기능을 다룹니다.

### Advanced (09-11)
NeoVim 설정, 플러그인 생태계, LSP 통합 등 IDE급 환경 구축을 위한 고급 주제를 학습합니다.

### Integration (12-14)
IdeaVim, Claude Code와의 통합, 실전 워크플로우를 통해 학습한 내용을 실무에 적용합니다. Ch12(IdeaVim)는 Ch04 이후부터 병행 학습 가능합니다.

---

## 사전 요구사항

- macOS 또는 Linux 환경
- Homebrew (macOS) 또는 apt (Linux)
- NeoVim 0.10+ (권장)
- IntelliJ IDEA + IdeaVim 플러그인
- Claude Code CLI
