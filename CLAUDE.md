# runners-high — 개발 학습 세컨드 브레인
---
> Typora와 Markdown만으로 운용하는 개인 학습 저장소다. `write/`에 최종본을 모으고, `poc/`는 실험 흔적, `journal/`은 일지와 리뷰가 쌓인다.

## 저장소 정체성

저장소 목적은 두 가지다. 첫째, 공부한 내용을 "남에게 설명할 수 있는 수준의 문서"로 정착시키는 것이다. 둘째, 같은 개념을 시간이 지나 다시 만났을 때 빠르게 복습 가능한 MOC(Map of Content) 구조를 유지하는 것이다.

Obsidian·Zotero 같은 별도 도구는 쓰지 않는다. Typora가 지원하는 순수 Markdown + YAML 프론트매터만으로 연결·수명 관리가 가능한 구조를 선택했다. 이유는 단순하다. 도구가 죽어도 파일은 남기 때문이다.

## 디렉토리 역할

| 디렉토리 | 역할 | 특징 |
|----------|------|------|
| `write/` | **최종본** — 공유 가능한 완성 학습 문서 | 프론트매터·카테고리 규칙 강제 (하네스 적용). 실습 코드는 `write/{카테고리}/_code/` |
| `journal/` | 일지·주간·월간·분기·연간 리뷰 | daily/weekly/monthly/quarterly/yearly/goals |
| `issue/` | 장애·결함 보고서 | 날짜 폴더 + 한 줄 제목 `.md`. 양식은 기존 보고서 1건 따름. writing 스킬 1·2·4부 동일 적용 |
| `project/` | 실습 프로젝트 루트 | 독립 리포(submodule)이기도 함 |
| `docs/` | 과거 흔적 — write/로 이관 예정 | 신규 작성 금지. `docs/_poc-archive/`에 이관되지 못한 poc 자료 보관 |

## Claude / 에이전트 가드레일

`write/` 디렉토리 작업은 자동으로 두 가지 가드레일을 적용한다.

첫째, Markdown 스타일 규칙 1~4부 (`~/.claude/skills/writing/SKILL.md`) — 문단형 우선, 어미 다양화, AI 강조어 금지, "왜?" 포함.

둘째, 세컨드 브레인 하네스 (`~/.claude/skills/writing/references/second-brain-harness.md`) — 카테고리 맵, 파일명 규칙, 프론트매터 포맷, 이관 프로토콜.

신규 문서 작성·이관·리네이밍 전 하네스 §2 진입 체크리스트를 먼저 실행한다. 체크리스트를 통과하지 못하면 작업을 중단한다.

## 작성 분담 (사용자 vs Claude)

`runners-high/` 안의 자료는 *작성 주체* 가 분담된다.

| 영역 | 주체 | 비고 |
|---|---|---|
| `write/` (학습 자료 본문) | **사용자·Claude 협업** | 사용자가 요청하면 Claude 가 본문을 직접 수정하고 검증까지 수행 |
| `project/` (학습 프로젝트 코드) | **Claude 가 직접** | Edit/Write/Bash 로 직접 수정. 빌드·테스트 검증까지 책임 |
| `journal/` (일지·리뷰) | **사용자 주도** | 자기 메모라 톤이 더 자유롭다 |
| `issue/` (장애 보고서) | **사용자 주도** | 기존 보고서 1건의 형식을 SSOT 로 따름 |
| 저장소 메타 (`CLAUDE.md`·`STUDY_INDEX.md`·`README.md`·frontmatter 정합 등) | **사용자·Claude 협업** | 사용자가 요청하면 Claude 가 직접 수정 |

사용자가 문서 수정까지 요청하면 Claude 가 그 자리에서 본문을 직접 Edit/Write 한다.

## 금지 사항

- Obsidian wiki-link(`[[파일명]]`) 사용 — Typora 비호환
- 파일명 날짜 prefix(`2026-04-19-xxx.md`) — 날짜는 프론트매터 `updated` 필드 담당
- 사내 자료를 `_company/` 외 경로에 배치 — `.gitignore` 보호가 무력화된다
- 합니다체·한다체 혼용 — 한 문서 내에서 문체 하나만. **신규 문서 기본은 합니다체** (`~/.claude/skills/content/writing/SKILL.md` 의 어체 정책). 짧은 자기 메모(`journal/`, TIL)만 한다체 허용, 기존 한다체 문서는 일관성 유지 차원에서 그대로 둡니다
- `write/` 루트 고아 `.md` 배치 — 반드시 대분류에 귀속

## 시작점

| 질문 | 경로 |
|------|------|
| 어디서부터 읽지? | [STUDY_INDEX.md](STUDY_INDEX.md) |
| write/ 구조는? | [write/README.md](write/README.md) |
| 이번 달 목표는? | [journal/goals/current.md](journal/goals/) |
| 최근 학습 일지는? | [journal/daily/](journal/daily/) |

## 커밋 규칙

개인 저장소이므로 티켓 번호를 요구하지 않는다. 커밋 타입만 지킨다.

```
chore: 구조 변경, 파일 이동
refactor: 카테고리·파일명 리팩터
docs: 문서 추가·갱신
fix: 링크 수정, 프론트매터 오류 수정
```

히스토리가 얇아지지 않도록 카테고리·주제 단위로 쪼개 커밋한다. 한 번에 300개 파일을 묶어 "restructure"로 덮는 식의 커밋은 피한다.
