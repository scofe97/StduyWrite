---
title: notiflex-platform 분석 — GitAIOps 실습 저장소 해부
tags: [moc, gitaiops, gitops, kubernetes, argocd, ai-agent, book]
status: final
related:
  - ./01_git-history-flow.md
  - ./02_tech-architecture.md
  - ./03_gitaiops-method.md
  - ./04_ai-agent-comparison.md
  - ../../README.md
updated: 2026-06-26
---

# notiflex-platform 분석 — GitAIOps 실습 저장소 해부
---
> 책 「AI 시대에 개발자가 알아야 할 인프라 구성 배포 with 클로드 코드」(GitAIOps, sysnet4admin)의 실습 저장소 [`sysnet4admin/notiflex-platform`](https://github.com/sysnet4admin/notiflex-platform)를 git 이력·파일·브랜치까지 직접 클론해 해부한 노트입니다.



## 한 줄 결론

이 저장소를 처음 보면 "책 따라 만든 작은 쿠버네티스 프로젝트"로 보입니다. 그런데 708개 커밋과 `reset: run-NN` 커밋들을 따라가 보면 정체가 달라집니다. 같은 책 가드레일을 AI 에이전트(Claude·Codex·Gemini)가 **63회 처음부터 재실행한 실험 하네스**이고, 그 결과를 브랜치별로 박제해 둔 저장소입니다. 작은 결과물 뒤에 큰 반복 실험이 숨어 있다는 점이 이 저장소의 핵심입니다.

왜 이런 구조일까요? 책의 주제가 "AI에게 같은 지침을 줬을 때 인프라를 스스로 구성·배포하게 만들 수 있는가"이기 때문입니다. 한 번 성공한 결과만 보여주면 우연인지 실력인지 구분되지 않습니다. 그래서 저자는 같은 가드레일을 수십 번 돌려 재현성을 확인하고, 서로 다른 모델이 같은 지침에서 얼마나 비슷하거나 다른 결과를 내는지 비교했습니다.



## 무엇을 만든 저장소인가

Notiflex는 기업 고객별 알림 채널(이메일·SMS·Slack)을 관리하는 B2B 알림 SaaS를 가정한 데모 플랫폼입니다. 실제 알림 발송 로직은 핵심이 아니고, 그 앱을 GKE 위에 올리고 운영하는 **인프라 구성·배포 과정**이 학습 대상입니다. 앱 자체는 Go 표준 라이브러리로 작성한 154줄짜리 HTTP 서버이고, 그 주변을 ArgoCD·Argo Rollouts·Kafka·관측성 스택이 감쌉니다.

저장소가 책의 챕터(ch2~ch9)를 따라 한 겹씩 기능을 쌓아 올린다는 점이 중요합니다. ch2에서 맨몸 Go 앱과 첫 배포로 시작해, ch8에 가면 Kafka 이벤트와 분산 트레이싱까지 붙은 멀티테넌트 플랫폼이 됩니다. 이 누적 과정이 곧 "인프라를 단계적으로 구성하는 흐름"입니다.



## 분석 노트 인덱스

네 가지 축으로 나눠 정리했습니다. 각 축은 독립적으로 읽어도 되지만, 1번(이력)을 먼저 보면 나머지가 왜 그렇게 생겼는지 이해됩니다.

| 노트 | 축 | 핵심 질문 |
|------|-----|----------|
| [01_git-history-flow](./01_git-history-flow.md) | git 이력 흐름 해부 | 708개 커밋이 어떻게 63회 재실행·3개 AI 브랜치·챕터 마일스톤으로 쌓였는가 |
| [02_tech-architecture](./02_tech-architecture.md) | 기술 아키텍처 구성 | Go 앱과 GKE·ArgoCD·Kafka·관측성 스택이 ch2~ch9로 어떻게 누적 구축되는가 |
| [03_gitaiops-method](./03_gitaiops-method.md) | GitAIOps 방법론 | 3층 지식구조와 CI 자가커밋 루프로 "Git=진실 소스, AI=운영 표준 저자"를 어떻게 구현했는가 |
| [04_ai-agent-comparison](./04_ai-agent-comparison.md) | AI 에이전트별 결과 차이 | 같은 가드레일에서 세 모델의 결과가 어디서 수렴하고 어디서 발산하는가 |



## 분석 방법

저장소를 로컬에 클론한 뒤 파일 내용과 git 명령(`git log`, `git diff --stat`, `git rev-list` 등)으로 사실을 직접 확인했습니다. 노트의 수치(커밋 수, run 횟수, 브랜치 diff 등)는 추측이 아니라 클론에서 뽑은 실측값입니다. 책 본문은 보지 않고 저장소 산출물만 분석했으므로, 책이 의도한 설명과 저장소에 남은 결과 사이에 차이가 있을 수 있다는 점은 감안해 주십시오.
