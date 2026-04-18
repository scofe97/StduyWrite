# CMUX 터미널 가이드

## CMUX란?

CMUX는 AI 코딩 에이전트 전용으로 설계된 오픈소스 터미널 에뮬레이터다. macOS 14.0 이상에서 동작하는 네이티브 Swift/AppKit 앱이며, manaflow-ai 팀이 개발한다. GitHub에서 약 5,200개의 스타를 받았고(2026년 3월 기준, v0.62.2), 라이선스는 AGPL-3.0이다.

기존 터미널은 사람이 직접 명령어를 입력하는 것을 전제로 설계되었다. CMUX는 이 전제를 뒤집는다. AI 에이전트가 터미널을 프로그래밍 방식으로 제어할 수 있도록 Unix 소켓 기반 JSON API를 제공하고, 에이전트의 작업 상태를 사람이 감시할 수 있는 UI를 결합했다. 터미널이 에이전트의 "손"이 되고, 사람은 "눈"이 되는 구조다.

기술적으로는 Ghostty의 렌더링 엔진(libghostty)을 라이브러리로 사용하는 별도의 네이티브 앱이다. Ghostty의 포크가 아니라, WebKit이 Safari에 내장되듯 libghostty를 렌더링 백엔드로 채택한 것이다. WebKit 기반 브라우저를 내장하고, tmux와 유사한 분할(pane split) 레이아웃을 GUI로 제공한다. Ghostty 사용자라면 기존 설정 파일(`~/.config/ghostty/config`)을 그대로 읽어 적용할 수 있어서 전환 비용이 낮다.

설치는 Homebrew로 간단하게 할 수 있다.

```bash
brew tap manaflow-ai/cmux && brew install --cask cmux
```


## 핵심 개념: 계층 구조

CMUX는 tmux의 세션-윈도우-페인 모델을 차용하되, 용어와 관리 방식을 단순화했다.

| CMUX | tmux 대응 | 설명 |
|------|-----------|------|
| Workspace | Session | 작업 단위의 최상위 컨테이너. 프로젝트별로 분리한다 |
| Surface (탭) | Window | 워크스페이스 안의 개별 화면. 브라우저의 탭과 동일한 UX |
| Pane | Pane | 탭 안에서 분할된 각각의 터미널 영역 |

tmux에서는 이 구조를 모두 CLI 명령어(`tmux new-session`, `tmux split-window`)로 관리해야 하지만, CMUX는 GUI에서 클릭과 단축키로 관리할 수 있다. tmux의 키바인딩을 외우지 않아도 되므로 진입장벽이 낮다.

워크스페이스는 `Cmd+N`으로 생성하고, 탭은 `Cmd+T`, 페인 분할은 `Cmd+D`(수직)로 수행한다. 에이전트 여러 개를 동시에 돌리면서 각각의 출력을 분할 화면으로 모니터링하는 것이 기본 사용 패턴이다.

CMUX는 터미널 세션마다 환경변수 3개(`CMUX_WORKSPACE_ID`, `CMUX_SURFACE_ID`, `CMUX_SOCKET_PATH`)를 자동 주입한다. 에이전트나 스크립트가 이 변수를 읽어 자신이 어느 워크스페이스/탭에서 실행 중인지 파악하고, 소켓을 통해 CMUX를 제어할 수 있다.


## 주요 기능

### CLI 제어

CMUX의 핵심 차별점은 거의 모든 터미널 조작을 CLI로 수행할 수 있다는 점이다. 내부적으로 Unix 소켓을 통해 JSON 메시지를 주고받으며, 이 덕분에 AI 에이전트가 터미널을 프로그래밍 방식으로 조종할 수 있다.

```bash
# 워크스페이스/탭/페인 계층 구조 확인
cmux tree --all

# 특정 서피스의 화면 내용 읽기 (스크롤백 포함)
cmux read-screen --surface surface:2 --lines 50 --scrollback

# 새 워크스페이스 생성 (명령어 지정 가능)
cmux new-workspace --command "cd ~/project && make"

# 페인 분할
cmux new-split right

# 특정 페인에 명령어 전송
cmux send "npm run dev"

# 알림 발송
cmux notify --title "Build Complete" --body "빌드가 완료되었습니다"

# 프로그레스 바 설정
cmux set-progress 0.5 --label "테스트 실행 중"
```

에이전트가 `cmux read-screen`으로 다른 탭의 터미널 출력을 읽을 수 있다는 점이 중요하다. 예를 들어, 탭 A에서 빌드 서버가 돌아가고 탭 B에서 에이전트가 코딩 중일 때, 에이전트는 탭 A의 로그를 CLI로 읽어 빌드 오류를 파악하고 코드를 수정할 수 있다. tmux의 `capture-pane`도 비슷한 역할을 하지만, CMUX는 JSON API로 구조화된 응답을 반환하므로 에이전트가 파싱하기 쉽고, 이를 에이전트 워크플로우의 핵심 기능으로 설계했다.

### 알림 시스템

에이전트가 장시간 작업을 수행할 때 사람이 계속 화면을 쳐다볼 수는 없다. CMUX는 작업 완료 시 시스템 알림을 보내고 해당 탭을 플래시(깜빡임)시킨다. 표준 터미널 이스케이프 시퀀스(OSC 9/99/777)를 지원하므로, 이 시퀀스를 출력하는 도구라면 자동으로 알림이 동작한다. Claude Code의 hooks와 연동하면 특정 이벤트(빌드 완료, 테스트 실패 등)에 `cmux notify`로 커스텀 알림을 트리거할 수도 있다.

이 기능이 없으면 에이전트 5개를 동시에 돌릴 때 어느 에이전트가 끝났는지 일일이 탭을 순회해야 한다. 알림 시스템은 멀티 에이전트 운영의 전제 조건이다.

### 내장 브라우저

WebKit 기반 브라우저를 내장하고 있어서, 터미널 앱 안에서 웹 페이지를 열 수 있다. 브라우저 CLI API는 Vercel의 agent-browser 프로젝트에서 설계를 차용했으며, 80개 이상의 브라우저 제어 명령어를 제공한다.

```bash
# 브라우저 탭에서 URL 열기
cmux browser open https://localhost:3000

# 접근성 트리 기반 스냅샷 (에이전트가 페이지 구조 파악)
cmux browser snapshot --interactive

# 요소 클릭, 폼 입력
cmux browser click "button[type='submit']"
cmux browser fill "input[name='email']" "test@example.com"
```

프론트엔드 개발에서 이 기능의 가치가 드러난다. 에이전트가 코드를 수정하고, 내장 브라우저에서 결과를 확인하고, 접근성 트리 스냅샷으로 에러를 감지해 다시 코드를 고치는 루프를 터미널 하나에서 완결할 수 있다. 별도 브라우저 창을 오가는 컨텍스트 스위칭이 사라진다.

단, WebKit 엔진 특성상 몇 가지 제약이 있다. Chromium DevTools는 사용할 수 없고, HTTP 연결이 차단되어 HTTPS만 허용될 수 있으며, 강제 다크 모드가 적용되는 경우가 있다. Chromium 기반 디버깅이 필요하다면 외부 브라우저를 병행해야 한다.

### 에이전트 호환성

특정 에이전트에 종속되지 않는다. Claude Code, OpenAI Codex, Open Code, Gemini CLI, Kiro, Aider, Goose, Amp, Cline, Cursor Agent 등 터미널에서 실행되는 모든 AI 코딩 에이전트와 함께 동작한다. CMUX는 에이전트가 아니라 에이전트가 동작하는 환경(하네스)이기 때문이다.

Claude Code와의 연동은 MCP 서버가 아니라 마크다운 스킬 파일 방식을 사용한다. CMUX CLI 명령어를 설명하는 문서를 세션 시작 시 Claude에게 제공하면, Claude가 필요할 때 `cmux` 명령어를 호출하는 식이다.

### 기타 편의 기능

- 워크스페이스별 커스텀 색상으로 프로젝트를 시각적으로 구분할 수 있다
- 탭 이름을 "frontend", "backend", "db" 같은 레이블로 변경하는 것도 가능하다
- VS Code처럼 `Cmd+Shift+P`로 커맨드 팔레트를 열어 명령어를 검색/실행할 수 있고
- `cmux set-progress`로 에이전트 작업 진행률을 프로그레스 바로 시각화하며
- 기존 Ghostty 설정 파일을 그대로 읽어 폰트, 테마 등을 유지해 준다


## 타 터미널 비교

| 항목 | CMUX | tmux | Warp | iTerm2 | Ghostty |
|------|------|------|------|--------|---------|
| AI 에이전트 통합 | 핵심 설계 목적 | 없음 | 부분적 (AI 자동완성) | 없음 | 없음 |
| 내장 브라우저 | WebKit 기반 | 없음 | 없음 | 없음 | 없음 |
| 세션 복원 | 레이아웃만 (프로세스 미복원) | 완전 복원 | 부분적 | 부분적 | 없음 |
| CLI/API 제어 | Unix 소켓 JSON (80+ 명령) | tmux CLI | 제한적 | AppleScript | 없음 |
| 학습 곡선 | 낮음 (GUI 기반) | 높음 (CLI 전용) | 낮음 | 낮음 | 낮음 |
| 플랫폼 | macOS 전용 | 거의 모든 OS | macOS, Linux | macOS 전용 | 멀티플랫폼 |
| 렌더링 성능 | 네이티브 (libghostty) | 경량 (TUI) | Rust 기반 | 보통 | 최고 수준 |
| 화면 분할 | GUI + CLI | CLI 전용 | 지원 | 지원 | 미지원 |

tmux 사용자에게 CMUX가 매력적인 이유는 tmux의 강력한 분할/세션 관리 기능을 GUI로 제공하면서, 에이전트 제어용 API를 추가했다는 점이다. 반면 tmux의 프로세스 복원(세션이 죽어도 프로세스 유지)은 CMUX에서 아직 지원하지 않으므로, 장시간 서버 세션 유지가 필요한 경우에는 tmux가 여전히 우위다.

같은 libghostty 기반 터미널로 Calyx도 존재한다. Calyx는 세션 영속성(크래시 복구, 원자적 저장)과 macOS 26 Liquid Glass UI에 강점이 있고, CMUX는 브라우저 CLI(80+ 명령)와 에이전트 워크플로우에 강점이 있다. 에이전트 중심이면 CMUX, 일상 드라이버가 필요하면 Calyx라는 평가가 있다.


## 장단점 분석

### 장점

다른 터미널은 사람이 사용하는 것을 전제로 만들어졌고, AI 에이전트 지원은 나중에 추가된 기능이다. CMUX는 처음부터 에이전트가 터미널을 제어하는 시나리오를 중심으로 설계했다. Unix 소켓 JSON API, 화면 읽기, 알림 시스템, 브라우저 자동화 모두 이 설계 철학의 산물이다.

내장 브라우저는 프론트엔드 개발에서 터미널-브라우저 간 컨텍스트 스위칭을 제거한다. 에이전트가 코드 수정, 브라우저 확인, 에러 수정 루프를 터미널 안에서 완결할 수 있기 때문이다.

CLI로 터미널 상태를 프로그래밍 방식으로 조회/조작할 수 있으므로, 스크립트나 에이전트 훅에서 터미널을 자동화하는 기반이 된다. tmux의 기능을 GUI로 제공하기 때문에 키바인딩을 외우지 않아도 분할 레이아웃을 관리할 수 있다는 점도 진입장벽을 낮춘다.

Swift/AppKit 네이티브 앱이므로 Electron 기반 터미널(예: Hyper)에 비해 메모리 사용량이 적고 렌더링이 빠르다.

### 단점

CMUX를 종료하면 레이아웃과 작업 디렉토리는 복원되지만, 실행 중이던 프로세스는 사라진다. tmux처럼 터미널을 닫아도 백그라운드에서 프로세스가 살아있는 기능이 없다. SSH 세션이나 장시간 빌드를 유지해야 하는 경우에는 tmux가 여전히 필요하다.

macOS 전용이라는 점도 제약이다. Linux는 공식 지원하지 않고(커뮤니티 포크만 존재), Windows는 별도 팀이 C#으로 재작성한 비공식 프로젝트(cmux-windows)가 있을 뿐이다.

출시 초기 프로젝트이므로 크래시, UI 버그, 기능 누락이 존재한다. HN에서는 "이틀 만에 18번 릴리스"라는 코멘트가 달릴 정도로 빠르게 반복하고 있지만, 프로덕션 워크플로우에 즉시 도입하기보다는 점진적으로 시도하는 것이 안전하다.

에이전트 연동을 위한 스킬/훅 설정도 아직 자동화되지 않았다. Claude Code hooks 설정, 브라우저 스킬 설치, 샌드박스 해제 등을 수동으로 진행해야 한다.


## 설정 팁

### Claude Code hooks 연동

CMUX의 알림 시스템은 Claude Code의 hooks와 연동할 때 진가를 발휘한다. hooks에서 에이전트 작업 완료, 빌드 실패 등의 이벤트를 감지하여 `cmux notify`로 알림을 트리거하도록 설정하면, 에이전트 여러 개를 동시에 돌리면서도 중요한 이벤트를 놓치지 않는다.

### 스킬 설치

CMUX가 제공하는 core 스킬과 browser 스킬을 설치하면 에이전트가 내장 브라우저를 제어하거나 터미널 자동화를 수행할 수 있다. 공식 문서에서 권장하는 스킬 목록을 확인하고 필요한 것만 선택적으로 설치한다.

### 샌드박스 해제

에이전트가 CLI를 통해 터미널을 제어하려면 CMUX의 샌드박스 모드를 해제해야 한다. 보안과 편의 사이의 트레이드오프이므로, 신뢰할 수 있는 에이전트만 사용하는 환경에서 해제하는 것이 적절하다.


## 누구에게 적합한가

에이전트 여러 개를 동시에 운영하면서 작업 상태를 모니터링하고 싶은 개발자에게 CMUX가 현재 가장 적합하다. tmux의 분할/세션 관리가 필요하지만 CLI 전용 인터페이스가 부담스럽다면, CMUX의 GUI가 대안이 될 수 있다. 프론트엔드 개발자라면 내장 브라우저로 코드-브라우저 간 왕복을 줄이는 이점도 있다.

반면, SSH 세션 유지가 필수이거나 macOS 외 플랫폼을 주력으로 사용하거나 안정적인 프로덕션 도구가 필요하다면 아직은 기다리는 것이 낫다.


## 참고 자료

- [manaflow-ai/cmux (GitHub)](https://github.com/manaflow-ai/cmux)
- [cmux.dev (공식 사이트)](https://www.cmux.dev/)
- [Teaching Claude Code to drive cmux (bounds.dev)](https://www.bounds.dev/posts/teaching-claude-code-to-drive-cmux/)
- [cmux Terminal: Practical Guide (BetterStack)](https://betterstack.com/community/guides/ai/cmux-terminal/)
- [Calyx vs cmux comparison (dev.to)](https://dev.to/yuu1ch13/calyx-vs-cmux-choosing-the-right-ghostty-based-terminal-for-macos-26-28e7)
