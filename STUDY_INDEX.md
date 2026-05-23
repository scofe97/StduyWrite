# runners-high 학습 인덱스
---
> 최종본은 [`write/`](write/)에 모인다. `poc/`는 실험 흔적이며 이관이 끝나는 대로 삭제될 예정이다.

## 카테고리 맵

하네스 §4.2의 v1 체계를 그대로 따른다. 주제 중심이며 언어별 분류는 하위 폴더로 내린다.

| # | 카테고리 | 범위 |
|---|----------|------|
| 01 | [`write/01_language/`](write/01_language/) | Java·Go·TS 등 언어별 문법·관용구·표준 API. JVM은 Java 하위 `09_jvm/` |
| 02 | [`write/02_os/`](write/02_os/) | OS·시스템 콜·프로세스·메모리·파일시스템 |
| 03 | [`write/03_architecture/`](write/03_architecture/) | DDD, Hexagonal, Clean, 설계 원칙·패턴 |
| 04 | [`write/04_messaging/`](write/04_messaging/) | Kafka, Redpanda, Avro, Schema Registry, EDA 구현 |
| 05 | [`write/05_data/`](write/05_data/) | DDIA 이론·분산 시스템·데이터 처리·DB 운영·드라이버 관측 (DB, CDC, Transaction, Indexing, Replication, Sharding, Consensus) |
| 06 | [`write/06_observability/`](write/06_observability/) | Logging, Tracing, Metrics, OpenTelemetry |
| 07 | [`write/07_devops/`](write/07_devops/) | CI/CD, Jenkins, Nexus, Sonarqube |
| 08 | [`write/08_cloud/`](write/08_cloud/) | Cloud Native, K8s, Service Mesh (미래) |
| 09 | [`write/09_tools/`](write/09_tools/) | tmux, vim, Claude Code, Git |
| 10 | [`write/10_security/`](write/10_security/) | OAuth/JWT, OWASP, 위협 모델링, Spring Security |
| 11 | [`write/11_spring/`](write/11_spring/) | Spring Framework, Spring Boot, Spring Cloud |
| 99 | [`write/99_ETC/`](write/99_ETC/) | 분류 보류 — 3개월 체류 후 재배치 또는 아카이브 |

## Spring 학습 진입점

Spring 문서는 주제별로 분산 배치된다. 전 카테고리 집계는 [`write/11_spring/README.md`](write/11_spring/README.md)에서 확인한다.

## 예약 폴더

- [`write/_meta/`](write/_meta/) — 저장소 컨벤션, 워크플로우 가이드
- `write/_company/` — 사내 전용 분석 (`.gitignore` 보호)
- [`write/_archive/`](write/_archive/) — 6개월 무갱신·무참조 문서 보관

## 최근 추가된 final 문서

현재는 Step D의 프론트매터 주입으로 대부분 `status: draft`다. 사용자가 리뷰를 거쳐 `final`로 승격하는 과정이 끝나면 이 섹션을 자동으로 채울 예정이다. 갱신 방식은 다음 grep 명령을 기반으로 한다.

```bash
grep -rl "status: final" write/ --include="*.md" \
  | xargs grep -H "^updated:" \
  | sort -k2 -r | head -5
```

## 아카이브 후보

`status: final`이면서 `updated` 기준 6개월 이상 경과하고, 다른 문서의 `related`로 참조되지 않는 파일이 후보다. 월간 리뷰(`journal/monthly/`)에서 점검한다.

## 하네스와 규칙

`write/` 작업 규약과 파일명·프론트매터 포맷은 하네스 문서에 있다.

- 하네스: `~/.claude/skills/writing/references/second-brain-harness.md`
- 작성 스타일: `~/.claude/skills/writing/SKILL.md`
- 이 저장소의 한 페이지 요약: [`write/_meta/conventions.md`](write/_meta/conventions.md)

## 이관 진척

`poc/` → `write/` 이관 상태를 추적한다. 카테고리 전체 이관이 완료되면 `poc/<카테고리>/README.md` 상단에 삭제 예정일이 기재된다.

| 카테고리 | 이관 대상 | 진척 |
|----------|----------|------|
| 04_messaging | poc/08_MessageQueue, poc/03_CloudNative/kafka 등 | 부분 이관 |
| 06_observability | poc/07_Observability | 일부 이관 (Grafana 시리즈 완료) |
| 03_architecture | poc/02_Architecture | 1차 이관 (분할 작업 남음) |
| 나머지 | — | 미착수 |
