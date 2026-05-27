---
title: "테스트와 멀티모듈 — 복습 회차 1"
tags: [review, querydsl, test, datajpatest, multi-module]
status: in_progress
source: "../../05_data/querydsl/03-01.테스트와 멀티모듈.md"
round: 1
round_date: 2026-05-28
prev_round_date: 2026-05-27
next_round_date: null
quality: null
metacog:
  interview: null
  speak_without_diagram: null
  apply_to_other_env: null
updated: 2026-05-28
---

# 테스트와 멀티모듈 — 복습 회차 1

> 원본: [테스트와 멀티모듈](../../05_data/querydsl/03-01.테스트와%20멀티모듈.md)
> 회차 1 · 2026-05-28 · 이전 학습: 2026-05-27 (첫 학습 세션 — Q&A 4문제 진행, 평균 ~2.9/5)
>
> **본 복습 규약 (Karpicke & Roediger 2006, testing effect):**
> 1. 각 질문에 *먼저 자기 답을 적어라* — 답을 보지 말 것
> 2. 자기 답 작성 후에만 `<details>` 의 정답을 열어라
> 3. 정답과 비교해 0~5 점 self-quality 점수를 매겨라
> 4. 회차 끝 종합 평가에서 다음 회차 날짜가 결정됨



## 학습 목표 (원본 §학습목표 인용)

> 이 문서를 읽고 나면, `@DataJpaTest` 환경에서 QueryDSL 리포지토리를 검증할 수 있고, `JPAQueryFactory` 빈을 테스트 슬라이스에 어떻게 주입하는지 적용할 수 있으며, 멀티 모듈 환경에서 다른 모듈의 Q클래스 가시성을 확보하는 두 패턴(생성 경로 공유 / 별 q-module 분리) 을 선택할 수 있다.

이 목표 한 줄이 본 복습의 *기준점*. 5개 질문 모두 이 목표의 한 축을 검증한다.

> **2026-05-27 1차 학습 시 약했던 자리** (본 복습이 *반드시* 짚고 가야 할 위치):
> 1. `@DataJpaTest` 가 자동 등록하는 빈의 정확한 카탈로그 (`EntityManager` / `JpaRepository` / `DataSource`) 와 *외부 라이브러리 빈은 자동 등록 안 됨*
> 2. annotationProcessor 가 *.java 새 파일을 생성* 한다는 메커니즘 — 본문 §annotationProcessor 가 Q클래스를 만드는 메커니즘 (line 260)
> 3. `api` vs `implementation` 의 *의존 노출 차이* — 멀티모듈 함정의 핵심
> 4. PostgreSQL `sum(int * int)` = `bigint` 함정 (H2 vs 운영 DB 방언 차이의 *구체* 예)
> 5. fragment *단위 테스트* 관점 (실패 원인 격리 + 기동 비용 감소) — *설계* 관점과 분리해 이해



## Q&A 5문제

> 5문제의 축: **정의 (Q1) · 동기 (Q2) · 메커니즘 (Q3) · 적용 (Q4) · 함정 (Q5)** 다섯 갈래로 챕터의 핵심을 잡는다. 1차 학습의 약점 ①~⑤ 와 각 문제가 1:1 대응.

### Q1. 정의 — `@DataJpaTest` 슬라이스가 자동 등록하는 빈은? (약점 ①)

**질문**: `@DataJpaTest` 어노테이션이 컨텍스트에 *자동으로* 올리는 빈을 3가지 이상 나열하고, *자동 등록되지 않는* 외부 라이브러리 빈의 예를 하나 들어라. 본 챕터에서 그 예가 어떤 함정을 일으키는지도 한 문장으로.

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

<details>
<summary>정답 보기 (먼저 자기 답 적은 뒤)</summary>

`@DataJpaTest` 는 JPA 슬라이스만 띄우므로 자동 등록 빈은 `EntityManager` / `JpaRepository`(스프링 데이터 리포지토리) / `DataSource` / `PlatformTransactionManager` 입니다. 슬라이스 안에서 트랜잭션은 자동 활성화되고 각 테스트 끝나면 롤백됩니다. 자동 등록되지 *않는* 대표 빈이 본 챕터의 함정인 `JPAQueryFactory` — QueryDSL 라이브러리가 제공하는 *애플리케이션 빈* 이라 슬라이스 후보에 없습니다. 따라서 `@Autowired JPAQueryFactory` 가 비어 NPE 가 떨어지고, `@TestConfiguration` + `@Import` 또는 운영 `QueryDslConfig` 직접 `@Import` 로 수동 등록해야 합니다. 원본 §`@DataJpaTest`에 JPAQueryFactory 붙이기 (line 85~144) 참조.
</details>

**자가 점수 (0~5)**: __
*점수 기준: 0=완전 못 답함, 1=틀린 답, 2=부분 답+큰 누락, 3=핵심 맞음+세부 누락, 4=정확하지만 머뭇, 5=막힘 없이 정확*

---

### Q2. 동기 — annotationProcessor 가 Q클래스를 만드는 메커니즘 (약점 ②)

**질문**: `@Entity Member` 가 있을 때 `QMember.java` 는 *언제·어디서·누구에 의해* 생성되는가? 같은 모듈 안에서는 자동 해결되는데 *왜* 다른 모듈에서는 함정이 생기는가?

**자기 답**:
```
(여기에 자기 답 작성)
```

<details>
<summary>정답</summary>

`@Entity` 가 붙은 클래스를 만나면 **컴파일 단계**에서 `annotationProcessor "querydsl-apt:...:jakarta"` 가 같은 패키지에 `QMember.java` 같은 새 .java 파일을 직접 생성합니다. 생성 위치 기본값은 `build/generated/sources/annotationProcessor/java/main/` 이고, 이 파일은 *같은 모듈의 `sourceSets.main.java` 에 자동 포함* 되어 원본 소스와 함께 컴파일됩니다. 최종 `domain.jar` 안에 `QMember.class` 형태로 들어갑니다. 같은 모듈 안에서는 sourceSet 통합으로 자동 해결되지만, 다른 모듈에서 보려면 *jar 안 .class* 가 의존 모듈의 컴파일 클래스패스에 들어와야 합니다 — 그래서 멀티모듈에서 *생성 후 노출* 단계가 추가로 필요합니다. 원본 §annotationProcessor 가 Q클래스를 만드는 메커니즘 (line 260~270) 참조. Lombok 과의 차이는 *기존 클래스에 메서드 주입 vs 완전히 새 클래스 파일 생성*.
</details>

**자가 점수 (0~5)**: __

---

### Q3. 메커니즘 — 멀티모듈 Q클래스 4단계 점검 순서 (약점 ③)

**질문**: 도메인 모듈을 분리했더니 `repository` 모듈에서 `QMember` 가 빨갛게 표시된다. *4단계 점검 순서* 를 한 문장씩 풀어 설명하라. 특히 `api` vs `implementation` 의 차이가 *왜* 중요한가?

**자기 답**:
```
(여기에 자기 답 작성)
```

<details>
<summary>정답</summary>

네 곳을 순서대로 점검합니다. ① **생성 측**: Q클래스를 만드는 모듈(`domain`)에 `annotationProcessor "querydsl-apt:...:jakarta"` 가 걸려 있는지. 없으면 Q클래스 자체가 생성 안 됩니다. ② **노출 측**: 해당 모듈이 `api 'querydsl-jpa'` 로 노출했는지. `implementation` 으로 닫으면 *의존 모듈* 의 컴파일 클래스패스에 querydsl 타입이 안 보이고, `QMember.member` 같은 정적 import 자체가 깨집니다. `api` 는 *전이 노출*, `implementation` 은 *자기 모듈만 사용* — querydsl 타입을 다운스트림에서 import 하려면 반드시 `api`. ③ **의존 그래프**: `repository/build.gradle` 에 `api project(':domain')` 이 있는지, Gradle 이 `domain` 을 `repository` 보다 *먼저* 빌드하는지. ④ **IDE 인식**: IntelliJ 가 `build/generated/sources/annotationProcessor/java/main/` 을 소스 폴더로 인식하지 못하면 빨간 줄만 보이므로 `./gradlew clean build` → IntelliJ Gradle 새로고침, 안 되면 `File > Invalidate Caches / Restart`. 원본 §멀티모듈 (line 272~370) 참조. annotationProcessor·api·implementation 키워드 카탈로그는 `01_language/java/06_Build/02-01.Gradle 의존성 키워드.md` §6~7 에 상세.
</details>

**자가 점수 (0~5)**: __

---

### Q4. 적용 — H2 vs 운영 DB 방언 차이 *구체* 예와 처방 (약점 ④)

**질문**: "H2 로 충분하지 않다" 의 *구체적* 예를 3가지 이상 들고, 각각에서 어떤 운영 사고가 가능한지 한 줄로. 그리고 본 챕터 `Ch08_TestSetupTest` 가 Testcontainers 대신 *어떤 더 가벼운 길* 을 택했는가?

**자기 답**:
```
(여기에 자기 답 작성)
```

<details>
<summary>정답</summary>

세 가지 구체 예가 있습니다. **(a) DB 함수 결과 타입**: PostgreSQL 에서 `sum(int * int)` 는 `bigint` 를 반환합니다. `Tuple.get(..., Long.class)` 로 받지 않으면 `ClassCastException` 이 운영에서 터지지만, H2 는 같은 식을 `int` 로 평탄화해 *테스트는 GREEN, 운영은 RED* 가 됩니다 (메모리 `feedback_pg_sum_returns_bigint`). **(b) 윈도우 함수**: H2 도 일부 지원하지만 `PARTITION BY` NULL 처리·정렬 안정성·중복 처리가 PostgreSQL/MySQL 과 갈립니다. **(c) 격리 수준 시나리오**: `Repeatable Read`·`Serializable` 동시성 테스트에서 H2 는 운영 DB 와 완전히 다른 lock·MVCC 를 가집니다. 본 챕터 `Ch08_TestSetupTest` 는 Testcontainers(도커 띄움) 대신 한 단계 가벼운 길로 `@AutoConfigureTestDatabase(replace = Replace.NONE)` + `@ActiveProfiles("test")` 조합을 써서 *이미 떠 있는* 외부 Supabase PostgreSQL 에 붙고, `databaseProductNameIsPostgreSQL` 테스트가 그 사실을 직접 단언합니다. 원본 §인메모리 DB vs Testcontainers + §`Replace.NONE` (line 146~205) 참조.
</details>

**자가 점수 (0~5)**: __

---

### Q5. 함정 — fragment *단위 테스트* 관점 vs *설계* 관점 (약점 ⑤)

**질문**: "fragment 단위 테스트가 좋다" 는 답을 *두 가지 관점* 으로 분리해서 설명하라 — fragment *설계* 가 좋은 것과 fragment *단위 테스트* 가 좋은 것은 *왜 다른가*? 본 챕터 `Ch08_TestSetupTest#customFragmentMethodAlone` 슬롯이 *어느 관점* 을 재현하는가?

**자기 답**:
```
(여기에 자기 답 작성)
```

<details>
<summary>정답</summary>

두 관점이 명확히 다릅니다. **설계 관점** (jpa/03-05 커스텀 리포지토리 패턴 영역): 한 리포지토리가 모든 쿼리를 들고 있지 않고 역할별 fragment 로 쪼개져 SRP·응집도가 올라갑니다. **단위 테스트 관점** (본 챕터): 그렇게 분리된 fragment 를 *검증할 때*, `@Import` 로 한 fragment 구현만 끌어오면 (1) **실패 원인 격리** — 다른 fragment·메인 리포지토리의 영향이 사라져 실패 시 원인을 해당 fragment 의 `BooleanExpression` 조립이나 `JPAQueryFactory` 주입으로 좁힐 수 있고, (2) **기동 비용 감소** — 슬라이스가 더 가벼워져 TDD 피드백이 빠릅니다. 특히 통계용 fragment 처럼 도메인 영속성과 분리된 메서드는 fragment 단독 검증이 의도와 코드를 일치시킵니다. 본 챕터 `Ch08_TestSetupTest#customFragmentMethodAlone` 슬롯은 *단위 테스트 관점* 을 재현 — `MemberRepositoryCustom#searchAsDto` 한 메서드만 호출해 DTO 프로젝션이 좁은 단위로 동작하는지 확인합니다. 본 프로젝트는 별도 fragment 인터페이스 대신 `MemberRepositoryCustom` + `MemberRepositoryImpl` 패턴이라 변형 형태. 원본 §fragment 단위 테스트 (line 238~256) 참조.
</details>

**자가 점수 (0~5)**: __



## 회차 종합 평가

### 1. SM-2 quality 점수 (0~5)

Q1~Q5 평균을 반올림, 또는 *가장 막힌 질문 기준* 으로 보수적으로.

**quality**: __

> Wozniak SM-2 알고리즘: 5=완벽, 4=정답+머뭇, 3=정답+힘듦, 2=오답+쉬워 보였음, 1=오답+정답 기억남, 0=완전 blackout.

### 2. 3축 메타인지 자가평가 (1~5)

| 축 | 점수 (1~5) | 메모 |
|----|----------|------|
| A. 면접 답변 가능성 (실제 면접관 앞에서 답할 수 있는가) | __ | |
| B. 그림 없이 말로 설명 (Mermaid 없이 흐름을 풀어낼 수 있는가) | __ | |
| C. 다른 환경 응용 (다른 DB·다른 도메인·다른 언어에 응용 가능한가) | __ | |

**평균**: __

> 1차 학습 시 측정: A=3, B=2, C=4. *B 가 가장 약함* — Mermaid·표 없이 메커니즘을 말로 풀어내는 자리. Q2·Q3 에서 특히 집중.

### 3. 다음 회차 결정 (SM-2 변형)

| 현재 회차 | quality 5 | quality 4 | quality 3 | quality 0~2 |
|----------|----------|----------|----------|------------|
| 1 (오늘) | +14일 | +7일 | +3일 | +1일 (즉시 재학습) |

**다음 회차 날짜**: __ (오늘 + 위 표의 간격)

### 4. 졸업 판정

다음 *세 조건 모두 충족* 시 원본 문서 `status: final` + 복습 졸업:

- [ ] 본 회차 quality ≥ 4
- [ ] 3축 메타인지 평균 ≥ 3.6
- [ ] _mistakes.md 에서 본 문서 관련 미해결 패턴 0개

### 5. 오답 박제 → `../05_data/querydsl/_mistakes.md`

본 회차에서 *quality ≤ 3 인 질문* 을 한 줄씩 정리해 `write/05_data/querydsl/_mistakes.md` 에 append (없으면 신규 생성).

```markdown
## 2026-05-28 — 테스트와 멀티모듈 Q{N}: {질문 요약}
- **자기 답**: {틀린 답 요약}
- **정답**: {정답 요약 + 원본 §N 링크}
- **원인 추정**: {왜 틀렸는가 — 개념 혼동 / 디테일 누락 / 적용 미숙}
- **재방문 트리거**: {다음 회차 날짜}
```

같은 패턴이 *3회 이상* 반복되면 해당 챕터 본문이 명확하지 않다는 신호 — 원본 챕터에 *3계열 구성* (시각+표+결론) 또는 *예시·수치* 추가 보강 트리거.



## 관련 자료

- 원본 챕터: [05_data/querydsl/03-01.테스트와 멀티모듈](../../05_data/querydsl/03-01.테스트와%20멀티모듈.md)
- 실습 코드: `~/Library/CloudStorage/GoogleDrive-tscofet@gmail.com/내 드라이브/study/runners-high/project/querydsl-practice/src/test/java/com/runnershigh/querydsl/repository/Ch08_TestSetupTest.java` (6 tests GREEN)
- 관련 챕터: [01_language/java/06_Build/02-01.Gradle 의존성 키워드](../../01_language/java/06_Build/02-01.Gradle%20의존성%20키워드.md) §6~7 (annotationProcessor·api·implementation 카탈로그)
- 1차 학습 세션 plan: `~/.claude-work/plans/dynamic-snacking-neumann.md`
