# Cursor MCP 서버 설치 가이드

> MCP(Model Context Protocol) 서버를 Cursor IDE에 설치하고 설정하는 방법

---

## 개요

MCP 서버는 AI 에이전트가 외부 도구와 통신할 수 있게 해주는 **표준화된 프로토콜**입니다. 이 가이드에서는 다음 3가지 MCP 서버를 설치합니다:

| MCP 서버 | 기능 | 설명 |
|----------|------|------|
| **context7** | 📚 문서 조회 | 라이브러리/프레임워크의 최신 API 문서를 실시간 조회 |
| **grep_app** | 🔍 코드 검색 | GitHub 오픈소스 저장소에서 코드 패턴 검색 |
| **websearch_exa** | 🌐 웹 검색 | AI 최적화 시맨틱 검색으로 최신 정보 검색 |

---

## 설치 방법

### 방법 1: 프로젝트별 설정 (권장)

프로젝트 루트에 `.cursor/mcp.json` 파일을 생성합니다.

#### 1단계: 디렉토리 생성

```bash
# Windows PowerShell
New-Item -ItemType Directory -Force -Path ".cursor"

# macOS / Linux
mkdir -p .cursor
```

#### 2단계: mcp.json 파일 생성

`.cursor/mcp.json` 파일을 생성하고 다음 내용을 추가합니다:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    },
    "grep_app": {
      "url": "https://mcp.grep.app"
    },
    "websearch_exa": {
      "url": "https://mcp.exa.ai"
    }
  }
}
```

#### 3단계: Cursor 재시작

설정을 적용하려면 Cursor IDE를 완전히 종료하고 다시 실행합니다.

---

### 방법 2: 전역 설정

모든 프로젝트에서 동일한 MCP 서버를 사용하려면 전역 설정 파일을 편집합니다.

#### 설정 파일 위치

| 운영체제 | 경로 |
|----------|------|
| **Windows** | `%APPDATA%\Cursor\User\settings.json` |
| **macOS** | `~/Library/Application Support/Cursor/User/settings.json` |
| **Linux** | `~/.config/Cursor/User/settings.json` |

#### 설정 추가

```json
{
  "mcp.servers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    },
    "grep_app": {
      "url": "https://mcp.grep.app"
    },
    "websearch_exa": {
      "url": "https://mcp.exa.ai"
    }
  }
}
```

---

### 방법 3: Cursor UI를 통한 설정

1. **설정 열기**: `Ctrl + ,` (Windows/Linux) 또는 `Cmd + ,` (macOS)
2. **MCP 검색**: 검색창에 `MCP` 또는 `Model Context Protocol` 입력
3. **서버 추가**: `Features → Model Context Protocol` 섹션에서 `Add MCP Server` 클릭
4. **정보 입력**: 서버 이름과 URL 또는 Command 입력
5. **저장**: `Save` 클릭

---

## 연결 확인

설정 완료 후 다음과 같이 확인합니다:

1. Cursor IDE 재시작
2. `Settings → Features → Model Context Protocol` 이동
3. 추가한 서버들이 **"Connected"** 상태인지 확인

```
▼ MCP
• context7 Connected ✅
• grep_app Connected ✅
• websearch_exa Connected ✅
```

---

## 각 MCP 서버 상세 설명

### 1. Context7 (`@upstash/context7-mcp`)

**기능**: 라이브러리 및 프레임워크의 최신 문서를 AI 컨텍스트에 제공

**사용 예시**:
- React 18 최신 API 문서 조회
- Next.js App Router 문서 확인
- TypeScript 최신 기능 문서 검색

**장점**:
- 학습 데이터 컷오프 이후의 최신 문서 접근 가능
- 버전별 정확한 API 정보 제공

---

### 2. Grep App (`https://mcp.grep.app`)

**기능**: GitHub 오픈소스 저장소에서 코드 패턴 검색

**사용 예시**:
- 특정 라이브러리 사용 패턴 검색
- 에러 메시지 관련 코드 찾기
- 베스트 프랙티스 예제 검색

**장점**:
- 수백만 개의 오픈소스 저장소 검색
- 실제 프로덕션 코드 참조 가능

---

### 3. Websearch Exa (`https://mcp.exa.ai`)

**기능**: AI 최적화 시맨틱 웹 검색

**사용 예시**:
- 최신 기술 트렌드 검색
- 버그 해결 방법 검색
- 새로운 라이브러리 정보 검색

**장점**:
- AI에 최적화된 검색 결과
- 실시간 최신 정보 접근

---

## 문제 해결

### MCP 서버가 연결되지 않는 경우

1. **Node.js 확인**: `node --version`으로 Node.js가 설치되어 있는지 확인
2. **npx 확인**: `npx --version`으로 npx가 사용 가능한지 확인
3. **네트워크 확인**: 인터넷 연결 상태 확인
4. **Cursor 버전**: 최신 버전의 Cursor 사용 권장
5. **JSON 형식**: `mcp.json` 파일의 JSON 형식이 올바른지 확인

### 로그 확인

Cursor의 개발자 도구(`Ctrl + Shift + I`)에서 Console 탭을 확인하여 오류 메시지를 확인할 수 있습니다.

---

## API 키가 필요한 경우

일부 MCP 서버는 API 키가 필요할 수 있습니다. 이 경우 `env` 필드를 사용합니다:

```json
{
  "mcpServers": {
    "websearch_exa": {
      "command": "npx",
      "args": ["-y", "exa-mcp-server@latest"],
      "env": {
        "EXA_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

---

## 참고 자료

- [Cursor MCP 공식 문서](https://docs.cursor.com/context/mcp)
- [MCP (Model Context Protocol) 공식 사이트](https://modelcontextprotocol.io/)
- [Context7 GitHub](https://github.com/upstash/context7)
- [Exa AI](https://exa.ai/)
- [Grep.app](https://grep.app/)

---

## 요약

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP 서버 설치 요약                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1️⃣ .cursor/mcp.json 파일 생성                              │
│  2️⃣ mcpServers 설정 추가                                    │
│  3️⃣ Cursor 재시작                                           │
│  4️⃣ Settings에서 Connected 상태 확인                        │
│                                                             │
│  ✅ context7    - 최신 문서 조회                            │
│  ✅ grep_app    - 오픈소스 코드 검색                        │
│  ✅ websearch_exa - 웹 검색                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

