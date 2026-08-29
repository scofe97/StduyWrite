# runners-high — 개발 학습 세컨드 브레인

공부한 내용을 "남에게 설명할 수 있는 수준"까지 정착시켜 두는 개인 학습 저장소다. 백엔드·JVM·인프라를 중심으로, 책과 실습에서 얻은 것을 시간이 지나도 다시 꺼내 읽을 수 있는 문서로 남긴다.

## 왜 이렇게 쓰나

도구가 아니라 파일이 오래 남는다. 그래서 Obsidian이나 Notion 같은 별도 앱에 묶이지 않고, Typora가 지원하는 순수 Markdown과 YAML 프론트매터만으로 운용한다. 링크도 문서 수명 관리도 전부 텍스트 파일 안에서 끝난다. 앱이 사라져도 저장소는 그대로 읽힌다.

목적은 두 가지다. 하나는 개념을 설명 가능한 글로 정착시키는 것이고, 다른 하나는 같은 주제를 다시 만났을 때 빠르게 복습할 수 있도록 MOC(Map of Content) 구조를 유지하는 것이다. 그래서 이 저장소의 글은 키워드 나열이 아니라 "왜 그런가"를 담은 문장으로 쓴다.

## 무엇이 들어 있나

학습 최종본은 모두 [`write/`](write/) 아래 주제별 카테고리로 모인다. 언어·프레임워크가 아니라 *주제*가 1차 분류 축이고, 언어별 구분은 그 하위 폴더로 내려간다. 예를 들어 JVM은 `01_language/java/05_JVM/`에 있다.

| # | 카테고리 | 범위 |
|---|----------|------|
| 01 | [`01_language/`](write/01_language/) | Java·Go·TS 등 언어 문법·관용구·표준 API. JVM 심화 포함 |
| 02 | [`02_os/`](write/02_os/) | OS·커널·프로세스·메모리·파일시스템 |
| 03 | [`03_architecture/`](write/03_architecture/) | DDD, Hexagonal, Clean, 설계 원칙·패턴 |
| 04 | [`04_messaging/`](write/04_messaging/) | Kafka, Redpanda, Avro, Schema Registry, EDA |
| 05 | [`05_data/`](write/05_data/) | 분산 시스템·트랜잭션·복제·합의·DB 운영 (DDIA 계열) |
| 06 | [`06_observability/`](write/06_observability/) | Logging, Tracing, Metrics, OpenTelemetry |
| 07 | [`07_devops/`](write/07_devops/) | CI/CD, Jenkins, Nexus, SonarQube |
| 08 | [`08_cloud/`](write/08_cloud/) | Cloud Native, Kubernetes, Service Mesh |
| — | [`tools/`](write/tools/) | tmux, vim, Git, Claude Code |
| 09 | [`09_spring/`](write/09_spring/) | Spring Framework·Boot·Cloud (전 카테고리 집계는 하위 README) |
| 10 | [`10_AI/`](write/10_AI/) | 생성형 AI·에이전트 활용 |
| 11 | [`11_career/`](write/11_career/) | 커리어·성장 기록 |
| 99 | [`99_ETC/`](write/99_ETC/) | 분류 보류 — 일정 기간 체류 후 재배치 |

`write/` 안에는 밑줄로 시작하는 예약 폴더도 있다. `_meta/`는 저장소 컨벤션과 작성 규약을, `_archive/`는 오래 갱신·참조되지 않은 문서를 보관한다.

실습 프로젝트는 [`project/`](project/)에 둔다. 프론트엔드 연습, 개인 도구, QueryDSL 실습 같은 코드가 여기 모인다.

## 문서 수명 관리

모든 문서는 프론트매터에 `status`를 갖는다. 처음 쓴 글은 `draft`로 시작하고, 직접 다시 읽어 검토를 마치면 `final`로 승격한다. `final` 상태로 오래 갱신되지 않고 다른 문서가 참조하지도 않는 글은 `_archive/`로 내려 보관한다. 문서를 지우기보다 상태로 관리하는 편이 나중에 맥락을 잃지 않는다.

## 어디서부터 읽나

- 전체 지도: [STUDY_INDEX.md](STUDY_INDEX.md) — 카테고리 맵과 이관 진척
- `write/` 구조 상세: [write/README.md](write/README.md)
- Spring 학습 진입점: [write/09_spring/README.md](write/09_spring/README.md)

## 작성 규약

파일명에 날짜 prefix를 붙이지 않는다. 날짜는 프론트매터 `updated` 필드가 담당한다. Typora 호환을 위해 Obsidian 위키링크(`[[...]]`)는 쓰지 않고, 신규 문서의 기본 문체는 합니다체로 통일한다. 자세한 규약은 [`write/_meta/`](write/_meta/)에 있다.
