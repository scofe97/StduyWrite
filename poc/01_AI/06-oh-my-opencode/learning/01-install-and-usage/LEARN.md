# 01. OpenCode + OMO 설치와 기본 사용

## 목표

현재 Mac 환경에서 OpenCode와 OMO를 설치하고, `ultrawork` 중심 사용 흐름을 익힌다.

## 현재 환경 기준 결론

2026-03-11 KST 기준 이 환경은 아래 상태다.

- OS/아키텍처: `Darwin arm64`
- Node.js: `v20.18.1`
- npm/npx: `10.8.2`
- Homebrew: `5.0.16`
- `bun`: 없음
- `opencode`: 없음

따라서 이 환경에서는 아래 순서가 가장 자연스럽다.

1. `brew`로 OpenCode 설치
2. `npx`로 OMO 설치
3. `opencode auth login`으로 provider 인증
4. `opencode` 실행 후 `ultrawork` 또는 `ulw`로 작업 시작

## OMO는 무엇인가

인터뷰에서 개발자는 OMO를 "best agent harness for OpenCode"라고 설명한다. 여기서 harness는 말에 붙는 안장, 고삐, 채찍 같은 보조 장치에 가깝다. 즉 모델 자체를 바꾸는 것이 아니라 아래를 붙여서 OpenCode를 더 강하게 만드는 구조다.

- 실수 방지 장치
- 역할 분리된 서브에이전트
- 모델별 강점 활용
- 컨텍스트 절약 구조
- 반복 작업 강제 루프

## 왜 OpenCode 위에 올렸는가

인터뷰와 공식 저장소를 종합하면 이유는 아래와 같다.

- OpenCode는 플러그인/확장 구조가 열려 있다
- 특정 모델 제공자에 묶이지 않는다
- 다양한 모델을 역할별로 섞어 쓸 수 있다
- Claude Code에서 축적한 워크플로우를 옮기기 좋다

## 설치 순서

### 1. OpenCode 설치

이 환경에서는 Homebrew 설치가 가장 간단하다.

```bash
brew install anomalyco/tap/opencode
opencode --version
```

대안:

```bash
npm i -g opencode-ai@latest
opencode --version
```

### 2. OMO 설치

OMO 공식 설치 가이드는 `bunx oh-my-opencode install`을 권장하지만, 현재 환경에는 `bun`이 없으므로 `npx` 경로를 사용한다.

가장 안전한 방식:

```bash
npx oh-my-opencode install
```

구독 조합을 알고 있다면:

```bash
npx oh-my-opencode install --no-tui --claude=yes --openai=yes --gemini=no --copilot=no
```

주요 플래그:

- `--claude=yes|max20|no`
- `--openai=yes|no`
- `--gemini=yes|no`
- `--copilot=yes|no`
- `--opencode-zen=yes|no`
- `--zai-coding-plan=yes|no`

### 3. Provider 인증

```bash
opencode auth login
opencode auth list
```

Claude, OpenAI, Google, GitHub Copilot 등 실제로 사용할 provider만 로그인하면 된다.

### 4. 설치 확인

```bash
opencode --version
cat ~/.config/opencode/opencode.json
```

확인 포인트:

- `opencode` 명령이 동작한다
- `~/.config/opencode/opencode.json`이 생성된다
- plugin 배열에 `oh-my-opencode`가 들어간다

## 기본 사용법

### OpenCode 기본 명령

공식 문서 기준으로 우선 기억할 명령:

- `/help`
- `/init`
- `/share`
- `/undo`
- `/redo`

CLI에서 자주 쓰는 명령:

```bash
opencode auth login
opencode auth list
opencode mcp list
opencode agent list
opencode models
```

### OMO 핵심 사용 키워드

가장 중요한 키워드:

```text
ultrawork
```

짧게:

```text
ulw
```

예시:

```text
ultrawork
이 저장소의 인증 흐름을 분석하고 세션 만료 버그를 재현한 뒤 수정하고 테스트까지 끝내줘.
```

```text
ulw
README 설치 섹션을 최신 기준으로 정리해줘.
```

## 자주 언급되는 OMO 기능

| 기능 | 의미 | 언제 쓰는가 |
|------|------|-------------|
| `ultrawork` / `ulw` | 병렬 탐색, 설계, 구현, 검증을 강하게 켠다 | 중요한 작업 대부분 |
| `/ulw-loop` | 끝날 때까지 반복 수행한다 | 긴 수정, 대규모 정리 |
| `/init-deep` | 계층형 `AGENTS.md`를 자동 생성한다 | 큰 프로젝트 컨텍스트 정리 |

## 에이전트 역할 이해

| 에이전트 | 역할 | 요약 |
|---------|------|------|
| Sisyphus | 메인 오케스트레이터 | 사용자 요청을 받아 전체 작업을 끝까지 밀고 감 |
| Oracle | 고난도 판단/설계 자문 | 구현이 막혔을 때 논리/설계 판단 |
| Librarian | 라이브러리/문서 조사 | 외부 문서와 기술 선택 보조 |
| Explore | 코드베이스 탐색 | 어디를 수정해야 하는지 빠르게 찾음 |
| Prometheus | 계획 수립 | 실행 전 질문하고 계획을 세움 |

핵심은 Sisyphus가 모든 걸 직접 하지 않고, 필요한 전문 역할을 호출해서 중요한 정보만 받아오는 구조라는 점이다.

## 설정 파일 위치

### OpenCode 설정

- 글로벌: `~/.config/opencode/opencode.json`
- 프로젝트: 프로젝트 루트의 `opencode.json`
- 보조 디렉토리: 프로젝트의 `.opencode/`

OpenCode 설정은 교체가 아니라 병합된다.

### OMO 설정

우선순위:

1. `.opencode/oh-my-opencode.jsonc`
2. `.opencode/oh-my-opencode.json`
3. `~/.config/opencode/oh-my-opencode.jsonc`
4. `~/.config/opencode/oh-my-opencode.json`

실무적으로는 프로젝트별 튜닝을 `.opencode/oh-my-opencode.jsonc`에 두는 것이 가장 좋다.

## 최소 설정 예시

```jsonc
{
  "$schema": "https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/assets/oh-my-opencode.schema.json",
  "agents": {
    "sisyphus": {
      "model": "anthropic/claude-opus-4-6"
    },
    "oracle": {
      "model": "openai/gpt-5.4",
      "variant": "high"
    }
  }
}
```

## 인터뷰 자막에서 뽑은 핵심 인사이트

### 1. 설치만 해도 좋아져야 한다

개발자는 사용자가 내부 구조를 몰라도 설치만 하면 좋아져야 한다는 철학을 강하게 강조한다.

### 2. 멀티 모델 조합이 핵심이다

- Gemini는 프론트엔드/시각 작업에 강함
- GPT는 논리/추론에 강함
- Claude는 전반적으로 균형이 좋음

즉 하나의 최고 모델보다 역할별 최적 모델 조합이 더 중요하다는 철학이다.

### 3. 컨텍스트는 직접 다 들고 가지 않고 보고받는다

사람이 조직에서 일하듯:

- 각 담당자가 자기 맥락을 갖고 일함
- 메인 에이전트는 핵심만 보고받음
- 그래서 중요한 정보에 집중할 수 있음

### 4. `ultrawork`는 "생각 많이"보다 "끝까지 해"에 가깝다

- 구조 분석
- 코드베이스 탐색
- 외부 자료 조사
- 병렬 작업
- 완료될 때까지 계속 수행

을 강하게 켜는 키워드로 이해하면 된다.

### 5. Plan은 선택 사항이다

모호한 작업이면 계획 중심 접근이 좋고, 중요한 작업이면 그냥 `ultrawork`를 바로 넣어도 된다는 실전 감각이 인터뷰에서 드러난다.

## 주의사항

1. 현재 환경에는 `bun`이 없으므로 공식 문서의 `bunx` 예시를 그대로 복사하지 말고 `npx`로 바꾸는 것이 안전하다.
2. 2026-03-11 기준 공식 문서에서 바로 확인된 OpenCode 기본 슬래시 명령은 `/init`, `/help`, `/share`, `/undo`, `/redo`다.
3. Litmers 글에서 언급된 `/connect` 흐름은 이번 정리에서 공식 저장소 기준으로 바로 재검증하지 못했다.
4. OMO는 강력한 대신 토큰 사용량이 커질 수 있다. 인터뷰에서도 Ralph Loop, OMO 모두 토큰을 많이 먹는 성격이 있다고 직접 언급된다.
