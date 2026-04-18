# Claude Code LSP 통합 가이드

> **참고 영상**: [Claude Code Just Got The Ultimate Dev Shortcut (LSP Explained)](https://www.youtube.com/watch?v=lffYEu5MhSQ) - Zen van Riel

---

## 📌 개요

Claude Code에 **LSP(Language Server Protocol)** 지원이 추가되었습니다. 이 업데이트로 Claude Code가 코드베이스를 **더 빠르고 정확하게** 분석할 수 있게 되었습니다.

### LSP(Language Server Protocol)란?

LSP는 코드 편집기와 언어 서버 간의 통신을 표준화하여, 코드 편집기에서 다양한 프로그래밍 언어에 대한 기능(자동 완성, 정의로 이동, 참조 찾기 등)을 제공할 수 있게 해주는 프로토콜입니다.

> **핵심 포인트**: Claude가 단순히 텍스트로 코드를 읽는 것이 아니라, 언어 서버를 통해 코드의 **의미론적 구조**를 파악할 수 있게 되었습니다.

---

## 🚀 LSP가 제공하는 주요 기능

| 기능 | 설명 | 활용 예시 |
|------|------|----------|
| **정의로 이동 (Go to Definition)** | 함수나 변수의 정의 위치로 바로 점프 | `getUserById()` 함수가 어디서 정의되었는지 찾기 |
| **참조 찾기 (Find References)** | 여러 파일에 걸쳐 해당 코드가 사용된 모든 위치 추적 | `User` 인터페이스가 어디서 사용되는지 찾기 |
| **실시간 진단** | 코드 오류를 실시간으로 감지 | 타입 에러, 문법 오류 즉시 확인 |
| **코드베이스 탐색** | 전문 개발자처럼 프로젝트 구조를 이해하고 탐색 | 대규모 프로젝트에서 관련 코드 빠르게 찾기 |

---

## 🔧 설치 가이드

### 1. 시스템 요구사항

- **운영 체제**: 
  - macOS 10.15 이상
  - Ubuntu 20.04 이상, Debian 10 이상
  - Windows 10 이상 (WSL 필수)
- **하드웨어**: 4GB 이상의 RAM
- **소프트웨어**: Node.js 18 이상
- **네트워크**: 인터넷 연결 필수

### 2. Claude Code 설치

#### Windows (WSL 사용)

Windows에서는 WSL(Windows Subsystem for Linux)을 통해 실행해야 합니다.

```powershell
# 1. WSL 설치 (관리자 권한 PowerShell)
wsl --install

# 2. 시스템 재부팅 후, WSL 업데이트
wsl --update && wsl --shutdown
```

```bash
# 3. WSL 터미널에서 Node.js 설치
sudo apt update && sudo apt install nodejs npm

# 4. Claude Code 설치
npm install -g @anthropic-ai/claude-code
```

또는 PowerShell에서 직접 설치:

```powershell
irm https://claude.ai/install.ps1 | iex
```

#### macOS

```bash
# Homebrew를 통한 설치
brew install --cask claude-code

# 또는 스크립트 설치
curl -fsSL https://claude.ai/install.sh | bash

# 또는 npm 설치
npm install -g @anthropic-ai/claude-code
```

#### Linux

```bash
# 스크립트 설치
curl -fsSL https://claude.ai/install.sh | bash

# 또는 npm 설치
npm install -g @anthropic-ai/claude-code
```

### 3. 설치 확인

```bash
claude --version
```

### 4. 고급 LSP 기능 활성화 (cclsp)

기본 Claude Code도 코드 분석 기능이 있지만, **더 정확한 LSP 기능**을 위해 `cclsp` 도구를 설치할 수 있습니다:

```bash
# cclsp 설치
npm install -g cclsp

# 프로젝트 디렉토리에서 설정
cd your-project
cclsp setup
```

`cclsp setup` 실행 시:
- 프로젝트의 언어를 자동 감지
- 필요한 Language Server 설치 및 설정
- Claude Code와 LSP 연동 자동 구성

**지원되는 Language Server:**

| 언어 | Language Server |
|------|-----------------|
| TypeScript/JavaScript | typescript-language-server |
| Python | pyright, pylsp |
| Go | gopls |
| Rust | rust-analyzer |
| C/C++ | clangd |
| Java | Eclipse JDT |
| Ruby | solargraph |

---

## 🖥️ IDE 통합 설정

### Visual Studio Code

1. VS Code 실행
2. 통합 터미널 열기 (`Ctrl+`` ` 또는 `Cmd+`` `)
3. `claude` 명령어 실행
4. 확장 프로그램이 자동으로 설치됨

### JetBrains (IntelliJ, PyCharm 등)

1. JetBrains IDE 실행
2. **Settings/Preferences** → **Plugins** → **Marketplace**
3. "Claude Code" 검색 및 설치
4. **Settings** → **Tools** → **Claude Code [Beta]**에서 경로 설정

---

## 💡 사용법

### 기본 실행

```bash
# 프로젝트 디렉토리로 이동
cd /path/to/your/project

# Claude Code 실행
claude
```

최초 실행 시 브라우저가 열리며 Anthropic 계정으로 로그인합니다.

### 자주 사용하는 명령어

```bash
# 프로젝트 구조 분석
claude "이 프로젝트의 구조와 주요 기능을 설명해줘"

# 코드 작성 요청
claude "Python Flask API 엔드포인트를 만들어줘"

# 버그 수정 요청
claude "main.py 파일을 검토하고 버그를 찾아서 수정해줘"

# 테스트 실행 요청
claude "테스트를 실행하고 실패한 부분이 있으면 수정해줘"
```

### 대화 관리

```bash
# 이전 대화 이어가기
claude --continue

# 특정 대화 재개
claude --resume
```

### 고급 옵션

```bash
# 권한 확인 무시 (샌드박스 환경에서만 권장)
claude --dangerously-skip-permissions

# 특정 모델 사용
claude --model sonnet

# 디버그 모드 활성화
claude --debug

# 출력만 확인 (비대화형 모드)
claude --print "코드 리뷰해줘"
```

---

## 🎯 LSP를 활용한 개발 워크플로우

### 예시: 대규모 리팩토링

LSP 지원 전:
```
1. grep으로 함수명 검색
2. 각 파일 열어서 확인
3. 수동으로 참조 추적
4. 놓친 부분 발생 가능
```

LSP 지원 후:
```
1. "getUserById 함수의 모든 참조를 찾아줘"
2. Claude가 LSP를 통해 정확한 참조 목록 제공
3. 모든 사용처를 한 번에 파악
4. 안전한 리팩토링 가능
```

### 예시: 버그 추적

```bash
# Claude에게 요청
claude "이 에러가 발생하는 원인을 찾아줘. AuthService에서 시작해서 관련된 모든 코드를 추적해봐"
```

Claude는 LSP를 통해:
1. `AuthService`의 정의 위치 확인
2. 관련 메서드들의 참조 추적
3. 호출 계층 분석
4. 문제 원인 정확히 파악

---

## 🎉 개발자에게 주는 이점

### 1. 코드 정확도 향상
- LSP를 통해 Claude가 코드 구조를 더 정확히 파악
- 타입 정보, 인터페이스 관계 등을 정확히 이해

### 2. 팀 간 일관성 유지
- 코드베이스 전체를 일관되게 이해
- 프로젝트 컨벤션을 자동으로 파악

### 3. 효율적인 작업
- 여러 파일에 걸친 참조 추적이 빨라짐
- 대규모 코드베이스에서도 빠른 탐색

### 4. 전문 개발자 수준의 코드 탐색
- 단순 텍스트 검색이 아닌 의미론적 분석
- 정확한 정의/참조 추적

---

## 📚 참고 자료

- **공식 문서**: [docs.claude.com/ko/docs/claude-code/setup](https://docs.claude.com/ko/docs/claude-code/setup)
- **IDE 통합 가이드**: [docs.claude.com/ko/docs/claude-code/ide-integrations](https://docs.claude.com/ko/docs/claude-code/ide-integrations)
- **빠른 시작 가이드**: [docs.claude.com/ko/docs/claude-code/quickstart](https://docs.claude.com/ko/docs/claude-code/quickstart)
- **영상 원본**: [YouTube - Claude Code LSP Explained](https://www.youtube.com/watch?v=lffYEu5MhSQ)

---

## 🔑 핵심 요약

> LSP 지원은 Claude Code가 **"AI 코딩 어시스턴트"에서 "전문 개발자처럼 코드를 이해하는 도구"**로 진화하는 중요한 업데이트입니다. 
> 
> 특히 **대규모 코드베이스**에서 작업할 때 Claude Code의 정확도와 효율성을 크게 향상시킵니다.

