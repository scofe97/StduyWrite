# 06-oh-my-opencode: OMO 설치와 운영 이해

## 프로젝트 개요

OpenCode 위에서 동작하는 `Oh My OpenCode(OMO)`를 현재 Mac 개발 환경에 설치하고 활용하는 방법을 학습합니다. 단순히 설치 명령만 따라치는 것이 아니라, 왜 OMO가 강력한지, 어떤 에이전트 구조를 가지는지, 그리고 OpenCode에서 Claude Code 자격 증명을 섞어 쓸 때 어떤 운영 리스크가 있는지까지 함께 이해하는 것이 목표입니다.

## 학습 목표

이 프로젝트를 완료하면 다음을 설명할 수 있어야 합니다:

1. **Agent Harness 개념**: OMO가 단순 프롬프트 모음이 아니라 OpenCode 위의 실행 하네스라는 점을 설명할 수 있다
2. **현재 환경 설치 전략**: 왜 이 환경에서는 `brew + npx` 조합이 가장 자연스러운지 설명할 수 있다
3. **기본 사용 흐름**: `opencode`, `opencode auth login`, `ultrawork` 흐름을 스스로 재현할 수 있다
4. **멀티 모델 오케스트레이션**: Gemini, GPT, Claude를 역할별로 다르게 쓰는 이유를 설명할 수 있다
5. **컨텍스트 관리 전략**: 왜 여러 에이전트가 나눠 조사하고 핵심만 보고하는 구조가 유리한지 설명할 수 있다
6. **운영 리스크 판단**: OpenCode에서 Claude Code 자격 증명을 우회 사용하려 할 때 어떤 제약과 리스크가 있는지 설명할 수 있다

## 현재 환경

| 항목 | 값 | 비고 |
|------|----|------|
| OS/아키텍처 | `Darwin arm64` | Apple Silicon Mac |
| Node.js | `v20.18.1` | 설치됨 |
| npm / npx | `10.8.2` | 설치됨 |
| Homebrew | `5.0.16` | 설치됨 |
| bun | 없음 | `bunx` 대신 `npx` 사용 |
| opencode | 없음 | 새 설치 필요 |

## 커리큘럼

| Ch | 주제 | 핵심 질문 | 상태 |
|----|------|----------|------|
| 01 | [OpenCode + OMO 설치와 기본 사용](./learning/01-install-and-usage/LEARN.md) | 이 환경에서 OMO를 가장 짧고 안전하게 설치하는 방법은 무엇인가? | ⬜ |
| 02 | [Claude Code 자격 증명 제한 이슈](./learning/02-claude-code-credential-restriction/LEARN.md) | OpenCode에서 Claude Code 인증을 섞어 쓰면 왜 막힐 수 있는가? | ⬜ |

## Quick Start

```bash
# 1. OpenCode 설치
brew install anomalyco/tap/opencode

# 2. OMO 설치
npx oh-my-opencode install

# 3. Provider 인증
opencode auth login

# 4. 실행
opencode
```

첫 프롬프트 예시:

```text
ultrawork
이 프로젝트 구조를 파악하고 지금 내가 해야 할 첫 작업을 제안해줘.
```

## 디렉토리 구조

```
06-oh-my-opencode/
├── README.md
├── learning/
│   ├── 01-install-and-usage/
│   │   └── LEARN.md
│   └── 02-claude-code-credential-restriction/
│       └── LEARN.md
└── practice/
    └── README.md
```

## 참고 자료

- Litmers 블로그: https://litmers.com/blog/oh-my-opencode-%EC%98%A4-%EB%A7%88%EC%9D%B4-%EC%98%A4%ED%94%88%EC%BD%94%EB%93%9C-%EC%99%84%EB%B2%BD-%EA%B0%80%EC%9D%B4%EB%93%9C-%EC%9E%91%EB%8F%99%EC%9B%90%EB%A6%AC-%EC%84%A4%EC%B9%98-%ED%95%B5%EC%8B%AC-%EA%B8%B0%EB%8A%A5-json-%ED%8A%9C%EB%8B%9D%EA%B9%8C%EC%A7%80
- OpenCode 공식 문서: https://opencode.ai/docs/
- OMO 저장소(현 명칭): https://github.com/code-yeongyu/oh-my-openagent
- Claude Code 제한 이슈 글: https://ios-development.tistory.com/1839
- 인터뷰 자막 원문: `/Users/simbohyeon/Downloads/[English] Oh my open code.    .   . ! l   (AI  #78) [DownSub.com].txt`
