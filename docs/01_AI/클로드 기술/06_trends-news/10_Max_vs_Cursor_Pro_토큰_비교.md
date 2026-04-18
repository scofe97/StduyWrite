# Claude Code Max vs Cursor Pro 토큰 제한량 비교 (2026년 기준)

> 작성일: 2026-01-20

---

## 1. 요약

| 항목 | Claude Code Max ($100/월) | Cursor Pro ($20/월) |
|------|---------------------------|---------------------|
| **가격** | $100/월 | $20/월 |
| **토큰 제한 방식** | 5시간 롤링 윈도우 + 주간 제한 | 월간 $20 크레딧 풀 |
| **컨텍스트 윈도우** | 200K 토큰 | 모델별 상이 (최대 1M) |
| **Opus 접근성** | 주간 15-35시간 | 매우 제한적 (수십 회) |
| **Sonnet 접근성** | 주간 140-280시간 | 약 225회/월 |

---

## 2. Claude Code Max $100/월 (Max 5x) 상세

### 2.1 토큰 제한량

| 구분 | 제한량 |
|------|--------|
| **5시간 세션당 토큰** | 약 88,000 토큰 |
| **5시간당 프롬프트 수** | 약 50-200개 |
| **주간 Sonnet 4 사용량** | 140-280시간 (토큰 기반) |
| **주간 Opus 4 사용량** | 15-35시간 (토큰 기반) |
| **컨텍스트 윈도우** | 200K 토큰 (모든 플랜 동일) |

### 2.2 주요 특징

- **5시간 롤링 윈도우**: 첫 메시지 시점부터 5시간 단위로 리셋
- **주간 제한**: 2025년 8월부터 도입, 5시간 윈도우와 별개로 작동
- **모델별 차등 소비**: Opus 4.5는 Sonnet 대비 약 1.7배 빠르게 할당량 소진
- **플랫폼 통합 한도**: 웹 인터페이스 + CLI 사용량이 합산됨

### 2.3 주의사항

- 2026년 1월 기준, 일부 사용자들이 약 60% 제한량 감소 보고
- 코드베이스 크기, auto-accept 모드 등에 따라 사용량 변동
- 여러 Claude Code 인스턴스 병렬 실행 시 더 빠르게 한도 도달

---

## 3. Cursor Pro $20/월 상세

### 3.1 토큰 제한량

| 구분 | 제한량 |
|------|--------|
| **월간 크레딧** | $20 상당 (API 가격 기준) |
| **Sonnet 4 요청** | 약 225회/월 |
| **GPT-5 요청** | 약 500회/월 |
| **Gemini 요청** | 약 550회/월 |
| **Claude Opus 요청** | 수십 회 수준 (비용이 높아 제한적) |
| **Auto 모델** | 무제한 |

### 3.2 가격 기반 계산 (2026년 기준)

**Claude Opus 4.5 API 가격:**
- Input: $5/백만 토큰
- Output: $25/백만 토큰

**$20 크레딧으로 Opus 사용 시:**
- 평균 요청당 약 3,000 input + 1,500 output 토큰 가정
- 요청당 비용: ~$0.05
- 월 최대: **약 400회** (순수 Opus만 사용 시)
- 실제로는 컨텍스트 누적으로 **수십 회** 수준

### 3.3 2025년 6월 가격 변경

- **변경 전**: 500 fast requests + 무제한 slow requests
- **변경 후**: $20 크레딧 기반 (모든 요청이 동일 풀에서 차감)

---

## 4. Cursor 토큰 표시의 이해

### 4.1 1.8M 토큰 표시의 의미

Cursor에서 표시되는 큰 토큰 숫자(예: 1.8M)는 **실제 API 호출량이 아닌 UI 표시 숫자**입니다.

#### 왜 1.8M은 실제로 불가능한가?

| 모델 | 컨텍스트 윈도우 |
|------|----------------|
| Claude (Sonnet/Opus) | **200K 토큰** |
| GPT-4 Turbo | 128K 토큰 |
| Gemini 1.5 Pro | 1M 토큰 |

**1.8M 토큰은 어떤 모델의 컨텍스트 윈도우도 초과합니다.**

#### 실제로 일어나는 일

```
[Cursor UI 표시 vs 실제 API 호출]

UI 표시: 1.8M 토큰 (세션 누적 합계)
         ↓
실제 API 호출: ~150K 토큰 (컨텍스트 윈도우에 맞게 truncation)
```

- Cursor는 세션 전체의 **이론적 누적 합계**를 표시
- 실제 API 호출 시에는 모델 컨텍스트 윈도우에 맞게 **자동으로 잘림(truncation)**
- 오래된 대화 히스토리, 덜 중요한 컨텍스트가 제거됨

#### 토큰 누적 계산 (UI 표시 기준)

```
턴 1: 시스템 프롬프트(10k) + 질문(1k) + 응답(2k) = 13k
턴 2: 위 전체(13k) + 새 질문(1k) + 응답(2k) = 16k
턴 3: 위 전체(16k) + 새 질문(1k) + 응답(2k) = 19k
...
턴 N: UI 표시상 1.8M (실제 API 호출은 ~200K 이하)
```

**결론**: Cursor의 1.8M 표시는 "이만큼의 컨텍스트가 있었다"는 의미이지, "이만큼 API에 보냈다"는 의미가 아닙니다.

### 4.2 Cursor가 컨텍스트에 포함하는 것

- 전체 대화 히스토리
- 시스템 프롬프트 및 도구 스키마
- 현재 파일 내용
- 커서 위치 주변 코드
- @mentions로 참조한 파일들

### 4.3 알려진 버그/이슈

| 시기 | 문제 | 설명 |
|------|------|------|
| **2026.01** | 캐시 미작동 3M 토큰 | v2.3.34에서 Cache Read 0, 3백만 토큰 + $16 청구 |
| **2026.01** | Opus 이미지 분석 폭발 | 스크린샷 분석 시 토큰 사용량 급증 |
| **2025.12** | AWS Bedrock 예산 취약점 | 지출 한도 무제한 설정 가능, 기업 예산 고갈 위험 |
| **2025** | 10x 과대 표시 | 토큰 카운터가 실제의 10배 표시 |
| **2025** | MCP 서버 토큰 과다 | 모든 MCP 도구 설명이 매 요청마다 전송 |
| **2025** | 대시보드 vs IDE 불일치 | 대시보드가 실제 사용량의 30배 이상 과대 표시 |

### 4.4 토큰 수가 뒤죽박죽인 이유 (1.8M vs 12.9k)

Cursor에서 어떤 요청은 1.8M, 어떤 요청은 12.9k로 표시되는 이유:

#### 원인 1: 새 대화 vs 기존 대화

```
[새 대화 시작]
요청 1: 시스템 프롬프트(10k) + 현재 파일(2k) + 질문(1k) = 13k ← 작음

[기존 대화 이어가기]
요청 50: 전체 히스토리(1.7M) + 새 질문(1k) = 1.8M ← 큼
```

**핵심**: 새 대화를 시작하면 컨텍스트가 **리셋**되어 토큰이 작아짐

#### 원인 2: 참조 파일 크기 차이

```
[작은 파일 참조]
@small-file.ts (500줄) → 약 5k 토큰

[큰 파일 참조]
@large-codebase/** (수천 줄) → 수백k 토큰
```

#### 원인 3: 사용 모드별 차이

| 모드 | 기본 포함 컨텍스트 | 토큰 규모 |
|------|-------------------|----------|
| **Chat** | 현재 파일 + 대화 히스토리 | 중간 |
| **Composer** | 여러 파일 + 프로젝트 컨텍스트 | 큼 |
| **Agent** | 도구 스키마 + 탐색 결과 + 히스토리 | 매우 큼 |
| **Inline Edit (Cmd+K)** | 선택 영역만 | 작음 |

#### 원인 4: 표시 버그

| 버그 유형 | 내용 |
|----------|------|
| **10x 과대 표시** | 토큰 카운터가 실제의 10배 표시 |
| **30x 대시보드 불일치** | IDE vs 대시보드 간 30배 이상 차이 |
| **버전별 차이** | v2.2.44에서 인디케이터 제거됨 |

**참고 링크 (2026년 최신):**
- [3백만 토큰 + $16 청구 버그 | Cursor Forum](https://forum.cursor.com/t/millions-tokens-without-cache-read-and-extremely-high-cost/148575) - v2.3.34에서 캐시 미작동, 3M 토큰 청구 (2026.01)
- [Opus 스크린샷 분석 토큰 폭발 | Cursor Forum](https://forum.cursor.com/t/opus-consumes-a-lot-of-tokens-when-taking-analyzing-screenshots/149286) - 이미지 분석 시 토큰 급증 (2026.01)
- [MCP 서버 연결 시 토큰 과다 | Cursor Forum](https://forum.cursor.com/t/high-input-token-usage-when-many-mcp-servers-are-connected-mcp-connection-state-not-retained-on-restart/142547) - 모든 MCP 도구 설명이 매 요청마다 전송
- [토큰 인플레이션 이슈 | Cursor Forum](https://forum.cursor.com/t/why-is-my-token-count-so-inflated-i-dont-see-how-this-can-be-possible/132975) - 캐시 대신 Input 토큰 사용

**참고 링크 (2025년):**
- [10x 과대 표시 버그 | Cursor Forum](https://forum.cursor.com/t/cursor-token-counter-over-counting-by-x10/128362) - 토큰 카운터가 실제의 10배 표시
- [10x 버그 미수정 항의 | Cursor Forum](https://forum.cursor.com/t/wont-you-fix-the-token-bug/121676) - v1.3.0에서도 10x 버그 미수정
- [토큰 사용량 표시 불가 | Cursor Forum](https://forum.cursor.com/t/i-cant-see-token-usage-anymore/111309) - 대시보드에서 토큰 사용량 확인 불가
- [Extreme Token Usage | Cursor Forum](https://forum.cursor.com/t/extreme-token-usage/117870) - Ultra 플랜에서도 토큰 소진 과다
- [Auto Mode 과다 토큰 사용 | Cursor Forum](https://forum.cursor.com/t/cursor-auto-mode-excessive-token-usage/123899) - Auto 모드에서 300k 토큰 소비 보고
- [남은 토큰 % 오류 | Cursor Forum](https://forum.cursor.com/t/remaining-tokens-percentage-is-incorrect/147884) - 잔여 토큰 퍼센트 표시 오류

**보안 이슈 (2025.12):**
- [Cursor AWS Bedrock 예산 드레인 취약점 | CyberNews](https://cybernews.com/security/cursor-aws-bedrock-catastrophic-budget-drain-vulnerability/) - 무제한 지출 한도 취약점으로 기업 예산 고갈 가능

#### 정리: 왜 우상향하지 않나?

```
[시나리오 A: 연속 대화]
12k → 25k → 40k → 55k → ... → 1.8M  ✓ 우상향

[시나리오 B: 새 대화 시작]
1.8M → (새 대화) → 15k  ← 리셋!

[시나리오 C: 다른 모드 전환]
Chat 500k → Cmd+K → 8k  ← 모드별 독립
```

**결론**: 토큰 수는 **대화 세션 단위**로 누적됨. 새 대화, 다른 모드, 다른 파일을 열면 별개의 컨텍스트가 생성됨.

### 4.5 핵심 차이점

| 구분 | Cursor UI 표시 | 실제 API 호출 | Claude Code Max 제한 |
|------|---------------|---------------|---------------------|
| **표시 숫자** | 1.8M (이론적 누적) | ~200K 이하 (truncation) | 순수 API 사용량 |
| **계산 방식** | 세션 전체 누적 | 컨텍스트 윈도우 제한 | 실제 토큰 소비 |
| **비용 청구 기준** | ❌ UI 표시 아님 | ✅ 실제 호출량 | ✅ 실제 호출량 |

**중요**: Cursor에서 1.8M이 표시되어도 실제 비용은 truncation된 토큰(~200K 이하) 기준으로 청구됩니다.

---

## 5. 실제 토큰 사용량 측정 방법

### 5.1 Claude Code 측정 방법

#### 방법 1: `/context` 명령어 (가장 간편)

```bash
# Claude Code 세션에서 실행
/context
```

**제공 정보:**
- 현재 소비된 토큰 수
- 남은 가용 토큰
- 카테고리별 토큰 사용량 분석
- MCP 도구 사용 포함 상세 내역

#### 방법 2: ccusage CLI 도구 (추세 분석)

```bash
# 설치 없이 바로 실행
npx ccusage@latest daily    # 일별 사용량
npx ccusage@latest weekly   # 주별 사용량
npx ccusage@latest monthly  # 월별 사용량
```

**장점:** 시간대별 사용 패턴, 비용 추정 제공

#### 방법 3: Claude-Code-Usage-Monitor (실시간 모니터링)

```bash
# GitHub: Maciek-roboblog/Claude-Code-Usage-Monitor
# 실시간 터미널 모니터링 + ML 기반 예측
```

**제공 기능:**
- 실시간 토큰 소비량
- 번 레이트(burn rate) 분석
- 비용 분석
- 세션 한도 도달 예측

#### 방법 4: Anthropic Console (API 사용자)

API 직접 사용 시 Console에서 정확한 토큰 사용량 확인 가능:
- 모델별 토큰 사용량
- 시간대별 패턴
- 예상 비용

#### 방법 5: 로컬 JSONL 로그 파싱

Claude Code는 대화 데이터를 로컬 JSONL 파일로 저장:
- 위치: 프로젝트별 디렉토리 (워크스페이스 경로 기반)
- 파일명: UUID 기반 세션 파일
- 단점: 파싱이 복잡하고 파일 구조가 중첩됨

### 5.2 Cursor 측정 방법

#### 방법 1: 대시보드 (공식)

```
Settings > Dashboard > Usage
Settings > Dashboard > Billing (Usage Based Pricing 사용 시)
```

**주의:** 대시보드 표시가 실제와 다를 수 있음 (버그 보고됨)

#### 방법 2: Cursor Usage Widget (macOS)

- macOS 메뉴바에서 실시간 모니터링
- 토큰 추적 및 청구 내역 분석
- 월별 네비게이션

#### 방법 3: VS Code 확장 - Cursor Usage & Cost Tracker

```
Extension ID: cocodev.cursor-price-tracking
```

**제공 기능:**
- 실시간 사용량 모니터링
- 모델별 상세 분석
- 세션별 비용 추적

### 5.3 가장 정확한 측정 방법

| 플랫폼 | 권장 방법 | 정확도 |
|--------|----------|--------|
| **Claude Code** | `/context` + ccusage 조합 | ★★★★★ |
| **Claude API 직접** | Anthropic Console | ★★★★★ |
| **Cursor** | 대시보드 + VS Code 확장 조합 | ★★★ (버그 존재) |

#### Claude Code 권장 조합:

```bash
# 1. 현재 세션 상태 확인
/context

# 2. 추세 분석
npx ccusage@latest weekly

# 3. 실시간 모니터링 (필요 시)
# Claude-Code-Usage-Monitor 설치 후 실행
```

---

## 6. 비용 효율성 비교

### 6.1 월간 비용 대비 가치

| 사용 패턴 | Claude Code Max $100 | Cursor Pro $20 |
|-----------|---------------------|----------------|
| **가벼운 사용** | 과다 지출 가능 | 적합 |
| **중간 사용** | 적합 | 한도 도달 가능 |
| **헤비 사용** | 적합 | 크레딧 부족 |
| **Opus 집중 사용** | 권장 | 비권장 (비용 효율 낮음) |

### 6.2 Opus 모델 집중 사용 시

```
Claude Code Max $100:
- 주간 Opus 15-35시간 보장
- Sonnet 혼용으로 효율 극대화 가능

Cursor Pro $20:
- Opus 수십 회로 제한
- 실질적으로 Sonnet/Auto 위주 사용 필요
```

---

## 7. 결론 및 권장사항

### 7.1 선택 가이드

| 상황 | 권장 선택 |
|------|----------|
| **예산 제한적, 가벼운 사용** | Cursor Pro $20 |
| **Opus 모델 필수** | Claude Code Max $100 |
| **IDE 통합 중시** | Cursor |
| **CLI 기반 작업 선호** | Claude Code |
| **정확한 사용량 추적 필요** | Claude Code (더 나은 도구 지원) |

### 7.2 토큰 절약 팁

1. **긴 대화 피하기**: 컨텍스트 누적으로 토큰 소비 급증
2. **새 세션 자주 시작**: 불필요한 히스토리 제거
3. **적절한 모델 선택**: 단순 작업은 Sonnet/Auto, 복잡한 작업만 Opus
4. **@mentions 최소화**: 필요한 파일만 참조
5. **사용량 모니터링**: 주기적으로 `/context` 또는 대시보드 확인

---

## 8. 참고 자료

### Claude Code
- [Claude Code Token Limits Guide | Faros AI](https://www.faros.ai/blog/claude-code-token-limits)
- [About Claude's Max Plan Usage | Claude Help Center](https://support.claude.com/en/articles/11014257-about-claude-s-max-plan-usage)
- [How to track Claude Code usage | Shipyard](https://shipyard.build/blog/claude-code-track-usage/)
- [Claude-Code-Usage-Monitor | GitHub](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor)
- [How to monitor Claude code token usage | DEV Community](https://dev.to/saif_khan_67333bd574c6c8c/how-to-monitor-claude-code-token-usage-2en3)

### Cursor
- [Pricing | Cursor Docs](https://cursor.com/docs/account/pricing)
- [Tokens & Pricing | Cursor Learn](https://cursor.com/learn/tokens-pricing)
- [Understanding LLM Token Usage | Cursor Forum](https://forum.cursor.com/t/understanding-llm-token-usage/120673)
- [Context Window Guide | Cursor Forum](https://forum.cursor.com/t/context-window-must-know-if-you-dont-know/86786)
- [Cursor Usage & Cost Tracker | VS Marketplace](https://marketplace.visualstudio.com/items?itemName=cocodev.cursor-price-tracking)

### 비교 분석
- [Claude Code vs Cursor Comparison 2026 | Northflank](https://northflank.com/blog/claude-code-vs-cursor-comparison)
- [Claude Code vs Cursor Pricing 2026 | Zoer](https://zoer.ai/posts/zoer/claude-code-vs-cursor-pricing-2026)
- [Claude devs complain about usage limits | The Register](https://www.theregister.com/2026/01/05/claude_devs_usage_limits/)
