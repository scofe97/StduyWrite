# Claude HUD 플러그인 - 블랙박스 투명화

**출처**: [LinkedIn - Jeongmin Lee](https://www.linkedin.com/posts/jyoung105_claude-code%EC%9D%98-%EB%B8%94%EB%9E%99%EB%B0%95%EC%8A%A4%EB%A5%BC-%ED%88%AC%EB%AA%85%ED%95%98%EA%B2%8C-%EB%A7%8C%EB%93%A0-%ED%94%8C%EB%9F%AC%EA%B7%B8%EC%9D%B8-%EC%99%9C-%EA%B0%9C%EB%B0%9C%EC%9E%90%EB%93%A4%EC%9D%B4-ugcPost-7416490048826605568-8IVr)

---

## 문제점

> "Claude가 일하는 건지, 멍 때리는 건지 모르겠다"

- 장시간 작업 중 터미널이 조용함
- 컨텍스트 한계 도달 시기 파악 불가
- 무한 루프 발생 여부 확인 어려움

---

## Claude HUD란?

Claude Code의 작동 상태를 **실시간으로 모니터링**하는 오픈소스 플러그인

### 터미널 상태바 표시 항목

| 항목 | 설명 |
|------|------|
| 컨텍스트 사용량 | 시각적 바 + 퍼센티지 |
| 실행 중인 도구 | Read, Edit 등 현재 사용 중인 도구 |
| 서브에이전트 | 활성화된 서브에이전트 추적 |
| 작업 목록 완료도 | Todo 진행 상황 시각화 |

---

## 기술적 구조

### 토큰 계산

```
(input_tokens + cache_creation_input_tokens + cache_read_input_tokens)
÷ context_window_size
```

### 로그 파싱

- JSON 페이로드 스트림 처리
- `tool_use` 블록 감지 및 상태 추적

---

## 설치 방법

```bash
# 1. 마켓플레이스에서 추가
/plugin marketplace add jarrodwatts/claude-hud

# 2. 플러그인 설치
/plugin install claude-hud

# 3. 설정 실행
/claude-hud:setup
```

---

## GitHub

**jarrodwatts/claude-hud**

---

## 핵심 포인트

1. **투명성**: Claude의 현재 상태를 실시간 파악
2. **컨텍스트 관리**: 한계 도달 전 사전 인지
3. **디버깅**: 무한 루프나 멈춤 상태 빠른 감지
