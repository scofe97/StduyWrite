---
title: write 디렉토리 컨벤션 한 페이지
tags: [meta, convention]
status: final
related:
  - ../README.md
updated: 2026-04-19
---

# write/ 컨벤션 한 페이지
---
> 하네스 전체는 `~/.claude/skills/writing/references/second-brain-harness.md`. 이 문서는 한 페이지 요약만 담는다.

## 파일명

`{장}-{절}.{제목}.md` 형식만 쓴다. 장·절은 두 자리 숫자로 고정하며, 번호 접미사(`-x`, `-rp`)는 금지다. 한 카테고리 내에서 파일명만으로 어떤 주제인지 짐작할 수 있어야 한다.

```
✅ 08-01.EDA 기초.md
✅ 05-03.Consumer Group.md
❌ 08-1.EDA 기초.md
❌ 07-x.Kafka Stream.md
❌ 정리.md
```

## 프론트매터

모든 `.md` 상단에 YAML 프론트매터를 둔다. 없이는 커밋하지 않는다.

```yaml
---
title: EDA 기초
tags: [kafka, event-driven]
status: draft       # draft | final | archived
related:
  - ../03_architecture/03_distributed/03-06.이벤트 기반 아키텍처.md
updated: 2026-04-19
---
```

- `status: draft`는 외부 공유 금지다.
- `related`는 상대경로로만 쓴다. Obsidian wiki-link(`[[...]]`)는 Typora가 지원하지 않아 깨진다.
- `updated`는 수동 갱신한다. Git 히스토리가 자동 대신한다.

## 카테고리 결정 원칙

주제 중심으로 고른다. 언어별 분류는 `01_language/` 하위로만 내린다. JVM은 언어가 아닌 런타임이므로 `02_runtime/jvm/`에 둔다. 메시징은 "패턴 이론"과 "구현 기술"이 나뉜다 — Saga·Outbox의 이론 측면은 `04_distributed/`, Kafka·Avro의 구현은 `05_messaging/`.

확신이 서지 않으면 `99_ETC/`에 먼저 넣고 월간 리뷰 때 재배치한다.

## 금지 사항

- 루트(`write/`) 바로 아래 고아 `.md` 배치 — 반드시 대분류에 귀속
- 사내 자료를 `_company/` 외 경로에 두기 — `.gitignore` 보호가 깨진다
- 파일명 날짜 prefix(`2026-04-19-xxx.md`) — 날짜는 프론트매터 `updated` 담당
- 합니다체·한다체 혼용 — 한 문서 내에서 하나만
