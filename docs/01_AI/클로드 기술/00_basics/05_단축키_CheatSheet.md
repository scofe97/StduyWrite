# Claude Code 단축키 & Cheat Sheet

**출처**:
- [LinkedIn - Edwin Kim](https://www.linkedin.com/posts/edwinjungwoo_claude-code-cheat-sheet%EB%A5%BC-%EA%B3%B5%EC%9C%A0%EB%93%9C%EB%A6%BD%EB%8B%88%EB%8B%A4-%ED%94%84%EB%A6%B0%ED%8A%B8%ED%95%B4%EC%84%9C-%EC%82%AC%EC%9A%A9%EC%A4%91%EC%9D%B8%EB%8D%B0-activity-7415961577650012160-AeoO)
- [awesomeclaude.ai/code-cheatsheet](https://awesomeclaude.ai/code-cheatsheet)

---

## 키보드 단축키

| 단축키 | 기능 |
|--------|------|
| `!` | Bash 모드 활성화 |
| `@` | 파일/폴더 참조 |
| `\\` | 줄 바꿈 |
| `Esc` | Claude 중단 |
| `Esc+Esc` | 되감기 메뉴 열기 |
| `Ctrl+R` | 전체 출력/컨텍스트 표시 |
| `Ctrl+V` | 이미지 붙여넣기 |
| `Shift+Tab` | 자동 수락 ("yolo 모드") |
| `Shift+Tab+Tab` | 계획 모드 |
| `Cmd+Esc / Ctrl+Esc` | IDE에서 빠른 실행 |

---

## 주요 슬래시 명령어

| 명령어 | 설명 |
|--------|------|
| `/help` | 도움말 |
| `/clear` | 대화 기록 초기화 |
| `/rewind` | 변경사항 되감기 |
| `/mcp` | MCP 서버 관리 |
| `/agents` | 커스텀 에이전트 관리 |
| `/config` | 설정 확인/수정 |
| `/terminal-setup` | 키 바인딩 설치 |
| `/review` | 코드 검토 요청 |
| `/model` | AI 모델 선택 |

---

## 입력 모드

| 접두사 | 모드 |
|--------|------|
| `!` | Bash 모드 - 직접 터미널 명령 실행 |
| `@` | 참조 모드 - 파일/폴더 경로 참조 |

---

## 설정 파일 우선순위

```
1. 엔터프라이즈: /etc/claude-code/managed-settings.json
2. 프로젝트 로컬: .claude/settings.local.json
3. 프로젝트 공유: .claude/settings.json
4. 사용자 전역: ~/.claude/settings.json
```

---

## 유용한 팁

1. **Yolo 모드** (`Shift+Tab`): 권한 요청 없이 자동 수락
2. **되감기** (`Esc+Esc`): 실수한 변경사항 롤백
3. **계획 모드** (`Shift+Tab+Tab`): 구현 전 계획 수립

---

## 참고 리소스

- [awesomeclaude.ai](https://awesomeclaude.ai) - 종합 리소스
- PDF/PNG 버전 다운로드 가능 (프린트용)
