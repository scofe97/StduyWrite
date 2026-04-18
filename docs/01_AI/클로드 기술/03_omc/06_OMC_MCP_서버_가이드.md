# OMC MCP 서버 가이드

## 개요

MCP(Model Context Protocol) 서버는 Claude Code에 외부 도구를 연결합니다. 웹 검색, 라이브러리 문서 조회, GitHub 연동 등의 기능을 추가할 수 있습니다.

## 왜 필요한가?

기본 Claude Code는 다음 한계가 있습니다:
- 최신 라이브러리 문서 접근 불가 (학습 데이터 기준)
- 웹 검색 기능 제한적
- 외부 서비스 연동 어려움

MCP 서버로 이 한계를 극복합니다.

## 설치된 MCP 서버

### 1. Context7 - 라이브러리 문서

**용도**: 최신 라이브러리/프레임워크 문서 실시간 조회

**설정** (`~/.mcp.json`):
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

**사용 예시**:
```
React 19의 새로운 훅 사용법 알려줘
```

Claude가 자동으로 Context7를 통해 최신 문서를 조회합니다.

**장점**:
- API 키 불필요
- 자동 라이브러리 감지
- 코드 예시 포함

### 2. Exa - 향상된 웹 검색

**용도**: 고품질 웹 검색 결과 제공

**설정** (`~/.mcp.json`):
```json
{
  "mcpServers": {
    "exa": {
      "command": "npx",
      "args": ["-y", "exa-mcp-server"],
      "env": {
        "EXA_API_KEY": "your-api-key"
      }
    }
  }
}
```

**API 키 발급**: https://exa.ai

**사용 예시**:
```
2024년 TypeScript 5.4 새 기능 검색해줘
```

**장점**:
- 기본 웹 검색보다 정확한 결과
- 개발 관련 콘텐츠 최적화
- 요약 기능 포함

## 설정 파일 위치

MCP 서버는 `~/.mcp.json`에 설정됩니다:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "exa": {
      "command": "npx",
      "args": ["-y", "exa-mcp-server"],
      "env": {
        "EXA_API_KEY": "your-key"
      }
    }
  }
}
```

## 추가 가능한 MCP 서버

### GitHub MCP
```json
{
  "github": {
    "command": "docker",
    "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "your-token"
    }
  }
}
```

**용도**: GitHub 이슈, PR, 리포지토리 관리
**요구사항**: Docker, GitHub Personal Access Token

### Filesystem MCP
```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allow"]
  }
}
```

**용도**: 지정된 디렉토리에 대한 확장된 파일 접근

## 활용 예시

### Context7 활용

```
# 라이브러리 문서 조회
Next.js 14 App Router에서 서버 액션 사용법 알려줘

# 특정 버전 문서
React 18의 Suspense 사용법 알려줘

# 설정 예시
Tailwind CSS 4.0 설정 방법 알려줘
```

### Exa 활용

```
# 최신 정보 검색
2024년 Node.js 성능 최적화 팁 검색해줘

# 비교 정보
Bun vs Deno 2024 비교 검색해줘

# 에러 해결
"Cannot read property of undefined" React 해결법 검색해줘
```

## 문제 해결

### MCP 서버가 동작하지 않을 때

1. **Claude Code 재시작**: 설정 후 반드시 재시작
2. **설정 파일 확인**:
```bash
cat ~/.mcp.json
```
3. **JSON 문법 검증**:
```bash
node -e "console.log(JSON.parse(require('fs').readFileSync('$HOME/.mcp.json')))"
```

### API 키 문제

- Exa: https://dashboard.exa.ai 에서 키 확인
- GitHub: https://github.com/settings/tokens 에서 발급

### npx 오류

Node.js 18 이상이 필요합니다:
```bash
node --version  # v18 이상 확인
```

## MCP 서버 추가/제거

### 추가
`~/.mcp.json`에 새 서버 설정 추가 후 Claude Code 재시작

### 제거
해당 서버 설정 삭제 후 Claude Code 재시작

### 설정 도구 사용
```
/oh-my-claudecode:mcp-setup
```

## 관련 문서

- [44_oh-my-claudecode_설치_및_개요.md](./44_oh-my-claudecode_설치_및_개요.md)
- [10_Cursor_MCP_서버_설치_가이드.md](./10_Cursor_MCP_서버_설치_가이드.md)
