# How to Be a 30x AI Engineer with a Taste

- **원문**: https://pakodas.substack.com/p/how-to-be-a-30x-ai-engineer-with-a-taste
- **읽은 날**: 2026-06-11
- **한 줄 요지**: 코드 생성이 공짜가 되는 시대에 엔지니어의 차별점은 타이핑이 아니라 **taste — 내부 판단 함수의 품질**이다.

---

## 왜 이 글을 모아두는가

AI가 코드를 대신 쓰게 되면서 "그럼 엔지니어는 뭘 하는 사람인가"라는 질문에 이 글은 구체적으로 답합니다. 평가하고, 결정하고, 아키텍처를 고르는 일이 본업이 된다는 주장인데, 추상적 선언에 그치지 않고 taste를 세 형태로 쪼개고 90일 훈련 계획까지 내놓습니다. 제가 운영하는 engineering-harness 스킬(평가자 분리, 삭제 우선)과 같은 방향을 가리키고 있어서, 하네스 설계의 "왜"를 보강하는 원전으로 보관합니다.

## 핵심 주장

가치의 이동을 한 문장으로 압축하면 이렇습니다. "craft는 타이핑에 있었던 적이 없다. 항상 생각에 있었다(The craft was never in the typing. It was in the thinking)." AI는 taste를 새로 만든 게 아니라, 타이핑을 자동화해서 원래부터 본질이었던 판단력을 드러냈을 뿐이라는 진단입니다.

## Taste의 세 형태

| 형태 | 대상 | 설명 |
|------|------|------|
| **Recognition taste** | 완성된 산출물 | 어느 구현이 우월한지 이유를 언어화하기 전에 감지하는 능력. 셰프가 빠진 재료를 알아채는 것과 같음 |
| **Compass taste** | 실행 전 가능성 | 만들지 말아야 할 기능, 잘못된 접근을 실행 전에 감지하고 방향을 잡는 능력 |
| **Vision taste** | 궤적(2년 후) | 지금이 아니라 2년 뒤에 무엇이 중요해지는지 읽고 일을 재배치하는 능력 |

세 형태 모두 "내부 기준과의 비교 연산"이라는 같은 메커니즘으로 동작합니다. 대상이 완성물이냐, 가능성이냐, 궤적이냐만 다릅니다.

## Taste가 작동하는 다섯 가치 영역

1. **문제 선택** — 무엇을 풀지 고르기
2. **시스템 아키텍처** — 조각들이 어떻게 맞물리는지
3. **품질 판단** — 언제 출시 가능한 상태인지
4. **사용자 공감** — 실제 필요를 이해하기
5. **커뮤니케이션** — 프레이밍과 스토리텔링

## 실천 워크플로 — 인상 깊었던 세 가지

**리뷰 대상을 코드에서 프롬프트로 옮긴다.** 생성된 코드를 전수 감사하는 대신, 그 코드를 만든 프롬프트(의도)가 올바른지 먼저 봅니다. 의도를 이해하는 것이 출력물을 감사하는 것보다 중요하다는 전환입니다.

**모델 주변 코드를 최소화한다.** "We try to put as little code as possible around the model" (Boris Cherny, Claude Code). 새 기능마다 추가가 아니라 삭제를 먼저 고려하고, 올바른 결과가 우연히 가능한 구조가 아니라 구조적으로 일어날 법한 시스템을 만듭니다.

**복리 결정에 집중한다.** 뛰어난 아키텍처 결정 하나가 몇 달의 작업을 절약합니다. 노력은 선형으로 쌓이지만 결정의 가치는 복리로 쌓인다는 관점입니다.

## 90일 Taste 훈련 계획

- **1개월차 — Recognition (구조화된 노출)**: 존경하는 개발자 도구 10개의 설계 결정 관찰 기록, 논문 10편에서 우아한 방법론의 구조 원리 추출
- **2개월차 — Compass (능동적 변별)**: 주 1회 비슷한 두 사례를 500단어로 비교(side-by-side), 매일 한 문장씩 만든 이의 결정을 관찰 기록하고 30일 후 패턴 리뷰(noticing practice)
- **3개월차 — Vision (생성적 적용)**: 내 소유물 재설계, 모든 문단이 자리값을 하는 글 쓰기, 모든 결정을 1원칙에서 설명하는 시스템 설계, taste를 문서·시스템으로 인코딩해 공유

## Taste를 기르는 다섯 프로젝트

1. AI 생성 코드 평가 프레임워크 만들기 — 내부 기준을 명시화
2. 오픈소스 온보딩 재설계 — 사용자 공감 + 커뮤니케이션
3. 팀 "taste test" 문서 — 조직의 기준 불일치를 드러냄
4. 48시간 안에 제품 출시 — 시간 제약이 taste 결정을 강제
5. 관점을 뒤집는 기술 블로그 — 커뮤니케이션과 자기 관점

## 기억할 인용

> "Everybody can be a 10x engineer now, as long as you have people with good software taste." — Emma Tang (OpenAI)

> "The profession is being dramatically refactored." — Andrej Karpathy

> "Most code is boring data transformation. Focus energy on system design instead." — Peter Steinberger

> "The cost of software production is trending towards zero." — Malte Ubl (Vercel CTO)

## 내 시스템과의 연결점

이 글의 "평가가 곧 업무" 관점은 `.claude/skills/tools/engineering-harness/SKILL.md`의 원리 3(작성자/평가자 분리)과 직결됩니다. 기존 원리에는 없던 "리뷰 대상을 코드에서 프롬프트로 옮긴다"는 전환을 이번에 원리 3에 보강했고, 외부 참고 목록에 이 글을 추가했습니다. 90일 훈련 계획 중 noticing practice(매일 한 문장 관찰 기록)는 journal 루틴에 얹기 좋은 후보로 남겨둡니다.
