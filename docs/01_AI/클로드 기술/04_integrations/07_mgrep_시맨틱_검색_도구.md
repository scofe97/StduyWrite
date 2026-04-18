# mgrep - AI 시대의 시맨틱 검색 도구

> **출처**: [GitHub - mixedbread-ai/mgrep](https://github.com/mixedbread-ai/mgrep)
> **라이선스**: Apache-2.0

---

## 개요

**mgrep**은 기존 `grep`을 AI 시대에 맞게 현대화한 시맨틱 검색 CLI 도구.
자연어 쿼리로 코드, 이미지, PDF, 텍스트 파일을 검색.

> "Natural-language search that feels as immediate as grep"

---

## 주요 특징

| 특징 | 설명 |
|------|------|
| **시맨틱 검색** | 키워드 매칭이 아닌 의미 기반 검색 |
| **멀티모달 지원** | 코드, 텍스트, PDF, 이미지 (오디오/비디오 예정) |
| **웹 통합** | `--web` 플래그로 웹 검색 통합 |
| **백그라운드 인덱싱** | `mgrep watch`로 실시간 파일 동기화 |
| **에이전트 통합** | Claude Code, OpenCode, Codex, Factory Droid 지원 |
| **토큰 효율성** | grep 대비 **~2배** 토큰 사용량 절감 |

---

## 설치

```bash
npm install -g @mixedbread/mgrep
```

---

## 빠른 시작

### 1. 인증

```bash
mgrep login
# 또는 환경변수 설정
export MXBAI_API_KEY=your_api_key
```

### 2. 인덱싱

```bash
cd your-project
mgrep watch
```

### 3. 검색

```bash
# 자연어 검색
mgrep "where do we set up auth?"

# 결과 수 제한
mgrep -m 25 "store schema"

# 웹 검색 + 요약
mgrep --web --answer "latest React patterns"
```

---

## 핵심 명령어

| 명령어 | 설명 |
|--------|------|
| `mgrep search <pattern> [path]` | 시맨틱 검색 (grep 스타일 플래그 지원) |
| `mgrep watch` | 리포지토리 파일 인덱싱 및 동기화 |
| `mgrep install-claude-code` | Claude Code 통합 설치 |
| `mgrep --web --answer` | 웹 검색 + 요약 생성 |

---

## 설정

### 우선순위 (낮음 → 높음)

1. 기본값
2. `.mgreprc.yaml` 설정 파일
3. 환경변수 (`MGREP_MAX_COUNT`, `MXBAI_API_KEY`)
4. CLI 플래그

### 설정 예시 (`.mgreprc.yaml`)

```yaml
max_count: 25
web_search: false
answer: true
```

---

## Claude Code 통합

### 설치

```bash
mgrep install-claude-code
```

### 효과

- 코드베이스 컨텍스트 검색 효율화
- 토큰 사용량 ~2배 절감
- 자연어 질문으로 코드 탐색

### 사용 예시

```
"인증 로직이 어디에 있어?" → mgrep이 관련 파일 검색
"스키마 정의 찾아줘" → 의미 기반으로 관련 코드 반환
```

---

## grep vs mgrep 비교

| 항목 | grep | mgrep |
|------|------|-------|
| 검색 방식 | 정확한 패턴 매칭 | 시맨틱(의미) 매칭 |
| 쿼리 형태 | 정규식 | 자연어 |
| 파일 타입 | 텍스트만 | 텍스트, PDF, 이미지 |
| 컨텍스트 이해 | 없음 | 있음 |
| 토큰 효율성 | 기준 | ~2배 효율적 |

---

## 적용 포인트

### Claude Code 워크플로우 개선

1. **코드베이스 탐색**: `mgrep watch`로 인덱싱 후 자연어 검색
2. **문서 검색**: PDF, 마크다운 등 문서 통합 검색
3. **토큰 절약**: grep 대신 mgrep으로 컨텍스트 효율화

### 활용 시나리오

```bash
# 인증 관련 코드 찾기
mgrep "사용자 인증 처리하는 부분"

# API 엔드포인트 검색
mgrep "REST API 정의된 곳"

# 에러 핸들링 패턴
mgrep "예외 처리 패턴"
```

---

*작성일: 2025-01-18*
