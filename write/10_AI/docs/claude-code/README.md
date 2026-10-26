---
title: docs/claude-code MOC
tags: [moc, ai, claude-code]
status: draft
source:
  - https://github.com/luongnv89/claude-howto/tree/188f468   # MIT, 커밋 188f468 (02-01~05-05 의 원문)
  - 실측 - Claude Code 2.1.295 (01-01), 사실 대조 2.1.310
related:
  - ../README.md
  - ../../README.md
updated: 2026-10-26
---

# docs/claude-code
---
> Claude Code 를 기능 단위로 정리한 노트입니다. 01-01 은 이 기기에서 직접 띄워 본 실측 노트이고, 02-01 부터는 공개 가이드 claude-howto 를 바탕으로 기능마다 무엇이고 왜 있고 어디서 막히는지를 다시 짰습니다.



## 무엇을 다루는가

> 맥락을 싣는 법, 기능을 덧붙이는 법, 자동으로 강제하는 법, 세션을 굴리는 법의 네 묶음입니다.

Claude Code 는 기능이 많지만 대부분 네 질문 가운데 하나에 답합니다. 모델이 무엇을 알고 시작하게 할지는 메모리와 스킬이 정하고, 무엇을 할 수 있게 할지는 서브에이전트와 MCP 가 정합니다.

모델에게 맡기지 않고 반드시 지키게 할 일은 훅과 권한이 맡습니다. 긴 일을 나누고 되돌리는 일은 세션과 체크포인트가 맡습니다. 그래서 장을 이 순서로 묶었습니다.

모델의 능력과 API 동작은 `10_AI/` 본문이 맡고, 여기는 그 모델을 감싼 제품의 명령과 설정을 봅니다.



## 근거와 기준 버전

> 02-01 부터의 근거는 원문 가이드이고, 그 위에 공식 문서·설치본 대조를 한 번 거쳤습니다.

02-01~05-05 의 원문은 [claude-howto](https://github.com/luongnv89/claude-howto/tree/188f468)(MIT) 의 커밋 188f468(2026-10-20 push) 입니다. 원문 10개 모듈 중 `09-advanced-features` 는 분량이 커서 05-02~05-05 네 편으로 나눴고, `10-cli` 는 01-01 과 겹쳐 따로 편을 만들지 않았습니다.

각 편은 쓴 뒤에 공식 문서(code.claude.com/docs)와 설치본 CLI 2.1.310 으로 옵션·설정 키·이벤트 이름을 대조했습니다. 공식 문서와 설치본에서 찾지 못한 사실은 지우지 않고 본문에 `확인 필요` 주석으로 남겨 두었습니다. 도식은 아직 그리지 않았고, 그릴 자리는 `도식 후보` 주석으로 표시했습니다.



## 본문 12편

> 1장은 실측, 2~5장은 원문 가이드 기반입니다.

### 1장 실행 옵션

| 편 | 다룰 내용 |
|----|----------|
| [01-01](01-01.CLI%20reference.md) | 다른 폴더에서 띄울 때의 `--add-dir`·`--settings`·신뢰 질문, 계정 분리, `--advisor`·`--effort`, 비대화 실행 (설치본 실측) |

### 2장 맥락과 명령

| 편 | 다룰 내용 |
|----|----------|
| [02-01](02-01.Slash%20Commands.md) | 내장·사용자·플러그인·MCP 네 출처, 사용자 명령이 스킬로 합쳐진 이유, 명령 파일의 frontmatter·인자·셸 주입 |
| [02-02](02-02.Memory.md) | CLAUDE.md 계층과 우선순위, 모듈 규칙·AGENTS.md·claudeMdExcludes, 설정 계층과의 차이, Auto Memory |

### 3장 기능 확장

| 편 | 다룰 내용 |
|----|----------|
| [03-01](03-01.Skills.md) | Progressive Disclosure 로 설명만 먼저 싣는 이유, 스킬 위치와 우선순위, 호출 제어, 다른 기능과의 경계 |
| [03-02](03-02.Subagents.md) | 별도 컨텍스트로 맡기는 이유, 정의 파일과 내장 에이전트, 재개·연결·백그라운드, worktree 격리와 영속 메모리 |
| [03-03](03-03.MCP.md) | 서버 추가와 범위, 도구가 컨텍스트에 실리는 방식(Tool Search·출력 한도), 프롬프트·리소스·Elicitation, 코드 실행으로 컨텍스트 줄이기 |

### 4장 자동화와 배포

| 편 | 다룰 내용 |
|----|----------|
| [04-01](04-01.Hooks.md) | 부탁과 강제의 차이, 이벤트·매처·종료 코드·JSON 결정, 프롬프트 기반 훅, 셸 명령을 그대로 실행하는 데서 오는 위험 |
| [04-02](04-02.Plugins.md) | 스킬·훅·에이전트·MCP 를 묶는 이유, plugin.json 과 로딩, 마켓플레이스와 설치 수명, 남의 플러그인을 들일 때 자동 실행되는 것 |

### 5장 세션과 고급 기능

| 편 | 다룰 내용 |
|----|----------|
| [05-01](05-01.Checkpoints.md) | 무엇을 저장하고 무엇은 저장하지 않는가, 되감기 선택지, git 을 대신하지 못하는 경우, 되감기·compact·새 세션 고르기 |
| [05-02](05-02.Planning%20Mode%C2%B7Extended%20Thinking%C2%B7Auto%20Mode%C2%B7Permission%20Modes%C2%B7Sandboxing.md) | 계획 모드, 생각 깊이, 자동 승인과 분류기, 권한 모드 비교, 커널 수준 샌드박스와 신뢰 범위 |
| [05-03](05-03.Background%20Tasks%C2%B7Monitor%C2%B7Scheduled%20Tasks%C2%B7Headless%20Mode.md) | 뒤로 보낸 작업과 완료 통지, 이벤트 스트림 감시, Dynamic Workflows, 예약 작업, CI 에 넣는 비대화 실행 |
| [05-04](05-04.Session%20Management%C2%B7Git%20Worktrees%C2%B7Agent%20Teams%C2%B7Remote%20Control.md) | 세션 이어 가기와 분기, 세션 간 메시지, 세션별 worktree, Agent Teams, 원격 조종과 웹 세션 |
| [05-05](05-05.Interactive%20Features%C2%B7Output%20Styles%C2%B7Status%20Line%C2%B7Settings.md) | 대화 중 기능, 출력 스타일, 상태줄과 TUI, 음성·채널·Chrome·데스크톱, settings 계층과 관리형 설정 |
