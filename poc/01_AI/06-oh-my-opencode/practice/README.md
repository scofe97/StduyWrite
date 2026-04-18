# OMO 실습 Quick Reference

## 설치

```bash
# OpenCode 설치
brew install anomalyco/tap/opencode

# 버전 확인
opencode --version

# OMO 설치
npx oh-my-opencode install
```

## 인증

```bash
# Provider 로그인
opencode auth login

# 로그인된 provider 확인
opencode auth list
```

## 기본 확인

```bash
# 모델 목록 확인
opencode models

# MCP 목록 확인
opencode mcp list

# 에이전트 목록 확인
opencode agent list
```

## 첫 실행

```bash
cd /path/to/project
opencode
```

첫 프롬프트 예시:

```text
ultrawork
이 저장소 구조를 분석하고 지금 가장 먼저 해야 할 작업을 제안해줘.
```

## 자주 쓰는 프롬프트

```text
ulw
README 설치 섹션을 최신 기준으로 정리해줘.
```

```text
ultrawork
로그인 흐름을 분석하고 세션 만료 버그가 있는지 확인해줘.
있으면 수정하고 테스트 결과까지 정리해줘.
```

```text
ultrawork
이 프로젝트에 필요한 AGENTS.md 구조를 만들어줘.
필요하면 /init-deep 흐름까지 포함해서 설계해줘.
```

## 설정 파일 위치

```bash
# OpenCode 글로벌 설정
~/.config/opencode/opencode.json

# OMO 글로벌 설정
~/.config/opencode/oh-my-opencode.jsonc

# OMO 프로젝트 설정
.opencode/oh-my-opencode.jsonc
```

## 최소 OMO 설정 예시

```jsonc
{
  "$schema": "https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/assets/oh-my-opencode.schema.json",
  "agents": {
    "sisyphus": {
      "model": "anthropic/claude-opus-4-6"
    }
  }
}
```

## 트러블슈팅

### Q1. `bunx` 예시가 공식 문서에 나오는데 왜 안 쓰는가?

```bash
# 현재 환경에는 bun이 없음
command -v bun

# 그래서 npx 사용
npx oh-my-opencode install
```

### Q2. `opencode` 설정 파일이 아직 없음

```bash
ls -la ~/.config/opencode

# 설치/인증 뒤 생성됨
```

### Q3. 어떤 키워드부터 써야 하는가?

```text
중요한 작업이면 일단 ultrawork
짧게 쓰고 싶으면 ulw
```
