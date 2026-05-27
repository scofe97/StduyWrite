# Oh My ClaudeCode (OMC) 학습

Claude Code CLI의 기능을 확장하는 플러그인 시스템 oh-my-claudecode의 아키텍처, 실행 모드, 에이전트 시스템, 모니터링을 체계적으로 학습합니다.

---

## 학습 목표

1. OMC의 플러그인 아키텍처와 행동 주입(behavior injection) 원리를 설명할 수 있다
2. 8가지 실행 모드의 차이점과 적절한 사용 시점을 판단할 수 있다
3. 32개 에이전트와 3-Tier 모델 라우팅의 동작 원리를 이해한다
4. HUD/CLI를 활용한 실시간 모니터링과 비용 분석을 수행할 수 있다
5. Multi-AI 오케스트레이션과 2026년 생태계 도구를 파악한다
6. Claude Agent SDK의 확장점과 멀티 프로바이더 오케스트레이션 개념을 이해한다

---

## 커리큘럼

| 순서 | 파일 | 주제 | 예상 시간 |
|------|------|------|-----------|
| 00 | [00-setup](./learning/00-setup.md) | 설치 및 환경 설정 | 15분 |
| 01 | [01-architecture](./learning/01-architecture.md) | 핵심 아키텍처 | 30분 |
| 02 | [02-execution-modes](./learning/02-execution-modes.md) | 실행 모드 8가지 | 45분 |
| 03 | [03-agent-system](./learning/03-agent-system.md) | 에이전트 시스템 | 30분 |
| 04 | [04-hud-monitoring](./learning/04-hud-monitoring.md) | HUD 실시간 모니터링 | 20분 |
| 05 | [05-cli-analytics](./learning/05-cli-analytics.md) | CLI 토큰 분석 | 20분 |
| 06 | [06-mcp-tools](./learning/06-mcp-tools.md) | MCP 도구 통합 | 25분 |
| 07 | [07-multi-ai-orchestration](./learning/07-multi-ai-orchestration.md) | Multi-AI 오케스트레이션 | 30분 |
| 08 | [08-practical-workflows](./learning/08-practical-workflows.md) | 실전 워크플로우 | 35분 |
| 09 | [09-sdk-orchestration](./learning/09-sdk-orchestration.md) | SDK와 멀티 프로바이더 오케스트레이션 | 40분 |

**총 예상 시간: ~4시간 50분**

---

## 진행 상태

- [ ] 00-setup: 설치 및 환경 설정
- [ ] 01-architecture: 핵심 아키텍처
- [ ] 02-execution-modes: 실행 모드 8가지
- [ ] 03-agent-system: 에이전트 시스템
- [ ] 04-hud-monitoring: HUD 실시간 모니터링
- [ ] 05-cli-analytics: CLI 토큰 분석
- [ ] 06-mcp-tools: MCP 도구 통합
- [ ] 07-multi-ai-orchestration: Multi-AI 오케스트레이션
- [ ] 08-practical-workflows: 실전 워크플로우
- [ ] 09-sdk-orchestration: SDK와 멀티 프로바이더 오케스트레이션

---

## 학습 방식

각 learning 문서를 순서대로 따라가며:
1. **개념 학습**: 왜 필요한지, 어떤 문제를 해결하는지 이해
2. **구조 분석**: Mermaid 다이어그램과 테이블로 동작 원리 파악
3. **체크포인트**: 면접형 질문으로 이해도 확인

---

## 사전 요구사항

- Claude Code CLI 설치 완료
- Node.js 18+ / npm 또는 bun
- oh-my-claudecode 플러그인 설치 (00-setup에서 안내)

---

## 참조 문서

기존 이론 문서와 함께 학습하면 효과적입니다:

| 문서 | 내용 |
|------|------|
| [01_OMC_설치_및_개요](../../../docs/01_AI/클로드 기술/03_omc/01_OMC_설치_및_개요.md) | 설치 과정 및 구성 요소 |
| [02_OMC_자동화_모드_가이드](../../../docs/01_AI/클로드 기술/03_omc/02_OMC_자동화_모드_가이드.md) | 자동화 모드 상세 |
| [03_OMC_HUD_상태표시줄_가이드](../../../docs/01_AI/클로드 기술/03_omc/03_OMC_HUD_상태표시줄_가이드.md) | HUD 설정 및 해석 |
| [04_Claude_HUD_플러그인](../../../docs/01_AI/클로드 기술/03_omc/04_Claude_HUD_플러그인.md) | HUD 기술 구조 |
| [05_OMC_CLI_토큰_분석_가이드](../../../docs/01_AI/클로드 기술/03_omc/05_OMC_CLI_토큰_분석_가이드.md) | CLI 비용 분석 |
| [06_OMC_MCP_서버_가이드](../../../docs/01_AI/클로드 기술/03_omc/06_OMC_MCP_서버_가이드.md) | MCP 서버 연동 |

---

## 실습 참조

- [practice/README.md](./practice/README.md) - 명령어 Quick Reference
