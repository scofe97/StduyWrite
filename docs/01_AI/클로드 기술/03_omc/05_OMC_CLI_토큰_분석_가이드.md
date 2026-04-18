# OMC CLI 토큰 분석 가이드

## 개요

OMC CLI는 Claude Code 사용량을 분석하는 커맨드라인 도구입니다. 토큰 사용량, 비용, 에이전트별 분석을 제공합니다.

## 왜 필요한가?

Claude Code 사용 시 다음을 알기 어렵습니다:
- 얼마나 많은 토큰을 사용했는지
- 비용이 얼마나 발생했는지
- 어떤 에이전트가 가장 많이 사용했는지
- 세션별 사용 패턴

OMC CLI는 이 모든 정보를 명확하게 보여줍니다.

## 설치

```bash
# npm으로 설치
npm install -g oh-my-claude-sisyphus

# 또는 bun으로 설치 (더 빠름)
bun install -g oh-my-claude-sisyphus
```

## 주요 명령어

### omc - 종합 대시보드

```bash
omc
```

통계, 에이전트 분석, 비용을 한 번에 표시합니다.

### omc stats - 토큰 통계

```bash
omc stats
```

**출력 예시**:
```
📊 Token Usage Statistics
─────────────────────────
Total Input:  1,234,567 tokens
Total Output:   456,789 tokens
Total:       1,691,356 tokens

📅 By Date:
2024-02-03: 500,000 tokens
2024-02-02: 691,356 tokens
```

### omc agents - 에이전트별 분석

```bash
omc agents
```

**출력 예시**:
```
🤖 Agent Breakdown by Cost
──────────────────────────
1. architect    $2.34  (45%)  ████████░░
2. explorer     $1.23  (24%)  ████░░░░░░
3. executor     $0.89  (17%)  ███░░░░░░░
4. planner      $0.72  (14%)  ██░░░░░░░░
```

각 에이전트가 얼마나 비용을 사용했는지 확인할 수 있습니다.

### omc tui - 대화형 대시보드

```bash
omc tui
```

터미널에서 대화형 UI로 상세 분석을 확인합니다:
- 세션별 필터링
- 시간대별 그래프
- 상세 로그 조회

### omc backfill - 과거 데이터 채우기

```bash
omc backfill
```

이전 세션의 토큰 데이터를 분석합니다.

## 출력 옵션

### JSON 출력
```bash
omc stats --json
```

스크립트나 다른 도구와 연동할 때 유용합니다.

### 기간 필터
```bash
omc stats --days 7    # 최근 7일
omc stats --days 30   # 최근 30일
```

## 비용 계산 방식

OMC CLI는 다음 기준으로 비용을 계산합니다:

| 모델 | 입력 토큰 | 출력 토큰 |
|------|-----------|-----------|
| Claude Opus | $15/1M | $75/1M |
| Claude Sonnet | $3/1M | $15/1M |
| Claude Haiku | $0.25/1M | $1.25/1M |

## 데이터 저장 위치

토큰 사용 데이터는 Claude Code 세션 로그에서 추출됩니다:
- **위치**: `~/.claude/projects/`
- **형식**: JSON 로그 파일

## 활용 예시

### 1. 일일 비용 확인
```bash
omc stats --days 1
```

### 2. 비용이 높은 에이전트 확인
```bash
omc agents
```
비용이 높은 에이전트가 있다면 작업 방식을 조정할 수 있습니다.

### 3. 세션별 상세 분석
```bash
omc tui
```
특정 세션에서 무엇이 많은 토큰을 사용했는지 확인합니다.

## 비용 최적화 팁

1. **Haiku 우선 사용**: 간단한 작업은 Haiku 에이전트 활용
2. **컨텍스트 관리**: 불필요한 파일 포함 피하기
3. **작업 분할**: 큰 작업을 작은 단위로 나누기
4. **캐시 활용**: 반복 작업 시 캐시된 결과 사용

## 트러블슈팅

### 명령어를 찾을 수 없을 때
```bash
# npm 전역 바이너리 경로 확인
npm config get prefix

# PATH에 추가 (필요시)
export PATH="$PATH:$(npm config get prefix)/bin"
```

### 데이터가 표시되지 않을 때
```bash
# 과거 데이터 채우기
omc backfill
```

## 관련 문서

- [44_oh-my-claudecode_설치_및_개요.md](./44_oh-my-claudecode_설치_및_개요.md)
- [25_Claude_Code_사용량_모니터링_설치_가이드.md](./25_Claude_Code_사용량_모니터링_설치_가이드.md)
