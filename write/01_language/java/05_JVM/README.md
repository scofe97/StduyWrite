---
title: JVM 학습 인덱스
tags: [jvm, hotspot, study-index, moc]
status: draft
related:
  - ./ch01_java-tech/01-01.JDK 구조와 바이트코드.md
  - ./ch01_java-tech/01-02.가상 머신 실행 서브시스템.md
  - ./ch01_java-tech/01-03.컴파일과 최적화.md
  - ./ch03_gc/01-01.GC 운영 — 로그와 튜닝.md
  - ./ch03_gc/01-02.Java 성능 — JMH와 측정 방법론.md
  - ./ch04_troubleshooting/02-01.기본 문제 해결 도구 — 명령줄 도구.md
  - ./ch04_troubleshooting/02-02.시각화 문제 해결 도구.md
  - ./ch05_optimization/02-01.최적화 사례 분석.md
  - ./ch05_optimization/02-02.실전 — Eclipse IDE 튜닝.md
  - ./ch06_class-file/02-01.클래스 파일 구조.md
  - ./ch06_class-file/02-02.바이트코드 명령어.md
  - ./_temp/01-04.효율적 동시성.md
  - ./03-01.스레드 생성과 생명주기.md
  - ./03-02.메모리 가시성과 동기화.md
  - ./03-03.생산자-소비자 패턴.md
  - ./04-01.원자 연산과 동시성 컬렉션.md
  - ./04-02.Executor 프레임워크.md
  - ./04-03.ThreadLocal과 동시성 라이브러리.md
  - ./05-01.Java Memory Model 심화.md
  - ./05-02.Virtual Threads 기초.md
  - ./05-03.Virtual Threads Pinning.md
  - ./05-04.Structured Concurrency.md
  - ./ch14_jpe-evolution/01-01.Java와 JVM의 성능 진화사.md
  - ./ch15_jpe-type-system/01-01.타입 시스템의 진화와 성능.md
updated: 2026-06-02
---

# JVM 학습 인덱스
---
> 이 폴더는 단행본 《JVM 밑바닥까지 파헤치기》의 **절 단위 정독 노트** 갈래(`chNN_*/02-NN`)와 **루트 직속의 동시성 학습 노트** 갈래(`03-xx` ~ `05-xx`)로 구성된다. 과거의 "부 단위 루트 요약" 레이어는 정독 폴더로 흡수했다 — 책 1·3·4부 요약은 [`ch01_java-tech/`](./ch01_java-tech/) 의 `01-NN` 파일(개관 갈래)로, 2부 요약은 [`ch03_gc/`](./ch03_gc/) 의 `01-NN` 파일로 이동했고, 5부 요약은 정독 폴더 신설 전까지 [`_temp/`](./_temp/) 에 보류 중이다. 각 폴더 안에서 `01-NN`은 *개관/운영 갈래*, `02-NN`은 *책의 절 정독 갈래*로 구분된다. 실습 코드는 `_practice/` 서브폴더에서 챕터별 Gradle 모듈로 모인다.
>
> 2026-06-02부터 두 번째 정독 대상 책 《JVM Performance Engineering》(Monica Beckwith) 갈래가 합류했다. 《밑바닥》이 `ch01`~`ch13` 번호대를 점유하므로, 새 책은 충돌을 피해 **`ch14`부터** 시작한다(예: [`ch14_jpe-evolution/`](./ch14_jpe-evolution/)). 새 책은 *한 폴더 = 책의 한 장*이고 파일 prefix는 장 안 소주제 순번을 뜻하는 `01-NN`이다 — 《밑바닥》의 `01-`(개관 흡수)/`02-`(절 정독) 의미와 다르니, 책마다 폴더가 갈려 출처가 섞이지 않는다. 책 구분은 각 노트의 `source` 필드가 1차 기준이다.

## 정독 대상 책

| 항목 | 내용 |
|------|------|
| 제목 | JVM 밑바닥까지 파헤치기 |
| 저자 | 저우즈밍 (周志明) |
| 원서 | 深入理解Java虚拟机 (3판) |
| 원서 출판사 | 机械工业出版社 |
| 한국어판 출판사 | 위키북스 |
| 교보 상품코드 | S000213057051 |
| 실습 JDK | OpenJDK 21 (Temurin 21.0.3) |

정확한 ISBN·페이지·역자 정보는 책 판권면 스크린샷 확보 시점에 보강한다.

### 두 번째 정독 대상 책 (2026-06-02 합류)

| 항목 | 내용 |
|------|------|
| 제목 | JVM Performance Engineering: Inside OpenJDK and the HotSpot VM |
| 저자 | Monica Beckwith (전 AMD Server Perf/Java Labs, Microsoft JDK 팀 리드) |
| 출판사 | Addison-Wesley (Pearson) |
| 폴더 갈래 | `ch14_*/` 이후 (《밑바닥》 ch01~13 번호대와 충돌 회피) |
| 파일 prefix | `01-NN` = 장 안 소주제 순번 (《밑바닥》 prefix 의미와 별개) |

정확한 ISBN·판차 정보는 책 판권면 확보 시점에 보강한다.

## 폴더 구조

```
05_JVM/
├── README.md                          # 이 문서
├── 03-xx ~ 05-xx (10편)               # 동시성 학습 노트 (직속 보존)
├── chNN_{topic}/                      # 단행본 절 단위 정독 노트
│   ├── 01-NN.{개관·운영 흡수본}.md       # 옛 루트 부 요약의 정독 폴더 이주본
│   └── 02-{절}.{제목}.md                  # 책의 절 정독 노트
├── _temp/                             # 정독 폴더 신설 대기 노트 (현재 5부 동시성 요약)
└── _practice/                             # 챕터별 Gradle 실습 코드
    ├── settings.gradle.kts
    ├── build.gradle.kts
    └── chNN/
        └── src/main/java/org/runners/jvm/chNN/...
```

폴더 안 노트 번호는 매 장마다 `01-NN`부터 시작한다. 각 장 폴더 안에서 `01-NN`은 *개관/운영 흡수본*(옛 루트 부 요약), `02-NN`은 *책의 절 정독 노트*로 구분된다.

## 부 요약 흡수 이력

옛 루트 부 요약(01-01~02-02) 6편은 다음 위치로 이주됐다. 이중 레이어를 폐기하고 정독 폴더 안으로 일원화한 결과다.

| 옛 위치 | 다루는 부 | 새 위치 |
|--------|----------|---------|
| 01-01.JDK 구조와 바이트코드 | 3부 6장 + 1부 일부 | [`ch01_java-tech/01-01.JDK 구조와 바이트코드.md`](./ch01_java-tech/01-01.JDK%20구조와%20바이트코드.md) |
| 01-02.가상 머신 실행 서브시스템 | 3부 7~8장 | [`ch01_java-tech/01-02.가상 머신 실행 서브시스템.md`](./ch01_java-tech/01-02.가상%20머신%20실행%20서브시스템.md) |
| 01-03.컴파일과 최적화 | 4부 10~11장 | [`ch01_java-tech/01-03.컴파일과 최적화.md`](./ch01_java-tech/01-03.컴파일과%20최적화.md) |
| 01-04.효율적 동시성 | 5부 12~13장 | [`_temp/01-04.효율적 동시성.md`](./_temp/01-04.효율적%20동시성.md) (정독 폴더 신설 대기) |
| 02-01.GC 알고리즘과 튜닝 | 2부 3장 | §6,§7만 [`ch03_gc/01-01.GC 운영 — 로그와 튜닝.md`](./ch03_gc/01-01.GC%20운영%20—%20로그와%20튜닝.md), §3 비교표는 [`ch03_gc/02-08.마치며.md`](./ch03_gc/02-08.마치며.md) 의 §3a로 흡수. §1,§2,§4,§5는 정독 노트와 중복으로 제거 |
| 02-02.Java 성능 | 2부 4~5장 | [`ch03_gc/01-02.Java 성능 — JMH와 측정 방법론.md`](./ch03_gc/01-02.Java%20성능%20—%20JMH와%20측정%20방법론.md) |

## 책 목차 ↔ 정독 노트 매핑

진척률 컬럼은 사이클마다 갱신한다. ⏳ = 진행 중, ✅ = 완료, ◻ = 미착수.

### 1부 자바와 친해지기

| 장 | 한국어 제목 | 폴더 | 진척 | 실습 |
|----|------------|------|------|------|
| 1장 | 자바 기술 시스템 소개 | [`ch01_java-tech/`](./ch01_java-tech/) | ⏳ §1.5~§1.7 정독 완료, 개관 흡수본 3편(01-01~01-03) 추가, §1.1~§1.4 보류 | [`_practice/ch01/`](./_practice/ch01/) |

### 2부 자동 메모리 관리

| 장 | 한국어 제목 | 폴더 | 진척 | 실습 |
|----|------------|------|------|------|
| 2장 | 자바 메모리 영역과 메모리 오버플로 | [`ch02_memory-area/`](./ch02_memory-area/) | ✅ §2.1~§2.5 | [`_practice/ch02-memory-area/`](./_practice/ch02-memory-area/) |
| 3장 | 가비지 컬렉터와 메모리 할당 전략 | [`ch03_gc/`](./ch03_gc/) | ✅ §3.1~§3.9 + 운영 흡수본 (01-01) | [`_practice/ch03-gc/`](./_practice/ch03-gc/) |
| 4장 | 가상 머신 성능 모니터링과 문제 해결 도구 | [`ch04_troubleshooting/`](./ch04_troubleshooting/) | ✅ §4.1~§4.4.1 정독(p.197~245, 02-01 명령줄 + 02-02 시각화), §4.5 마치며 ⏳ 스크린샷 미확보. GC 로그·jstat·튜닝은 [`ch03_gc/01-01`](./ch03_gc/01-01.GC%20운영%20—%20로그와%20튜닝.md) 운영 갈래에 별도 흡수 유지 | [`_practice/ch04-troubleshooting/`](./_practice/ch04-troubleshooting/) |
| 5장 | 최적화 사례 분석 및 실전 | [`ch05_optimization/`](./ch05_optimization/) | ✅ §5.1~§5.4 정독(p.253~283, 02-01 사례분석 + 02-02 실전). JMH·성능 측정 방법론은 [`ch03_gc/01-02`](./ch03_gc/01-02.Java%20성능%20—%20JMH와%20측정%20방법론.md) 흡수본에 별도 유지 | [`_practice/ch05-optimization/`](./_practice/ch05-optimization/) |

### 3부 가상 머신 실행 서브시스템

| 장 | 한국어 제목 | 폴더 | 진척 | 실습 |
|----|------------|------|------|------|
| 6장 | 클래스 파일 구조 | [`ch06_class-file/`](./ch06_class-file/) | ✅ §6.1~§6.5 정독(p.287~352, 02-01 클래스 파일 구조 + 02-02 바이트코드 명령어). 1장 부 요약 흡수본([`ch01_java-tech/01-01`](./ch01_java-tech/01-01.JDK%20구조와%20바이트코드.md))은 별도 유지 | [`_practice/ch06-class-file/`](./_practice/ch06-class-file/) |
| 7장 | 클래스 로딩 메커니즘 | [`ch01_java-tech/01-02`](./ch01_java-tech/01-02.가상%20머신%20실행%20서브시스템.md) (부 요약 흡수) | ⏳ 흡수만 | — |
| 8장 | 바이트코드 실행 엔진 | [`ch01_java-tech/01-02`](./ch01_java-tech/01-02.가상%20머신%20실행%20서브시스템.md) (부 요약 흡수) | ⏳ 스택 프레임·디스패치·invokedynamic 흡수, 본격 정독 미착수 | — |
| 9장 | 클래스 로딩과 실행 서브시스템, 사례와 실전 | _(미작성)_ | ◻ | — |

### 4부 컴파일과 최적화

| 장 | 한국어 제목 | 폴더 | 진척 | 실습 |
|----|------------|------|------|------|
| 10장 | 프런트엔드 컴파일과 최적화 | [`ch01_java-tech/01-03`](./ch01_java-tech/01-03.컴파일과%20최적화.md) (부 요약 흡수) | ⏳ javac·컴파일 단계 흡수 | — |
| 11장 | 백엔드 컴파일과 최적화 | [`ch01_java-tech/01-03`](./ch01_java-tech/01-03.컴파일과%20최적화.md) (부 요약 흡수) | ⏳ JIT·Graal·AOT 흡수, 본격 정독 미착수 | — |

### 5부 효율적인 동시성

| 장 | 한국어 제목 | 폴더 | 진척 | 실습 |
|----|------------|------|------|------|
| 12장 | 자바 메모리 모델과 스레드 | [`_temp/01-04`](./_temp/01-04.효율적%20동시성.md) (정독 폴더 신설 대기) | ⏳ 부 요약 _temp 보관, JMM 정독 미착수 | — |
| 13장 | 스레드 안전성과 락 최적화 | [`_temp/01-04`](./_temp/01-04.효율적%20동시성.md) (정독 폴더 신설 대기) | ⏳ 부 요약 _temp 보관, 락 최적화 정독 미착수 | — |

> 5부 정독 폴더(`chNN_concurrency/`)는 책 12장 스크린샷 확보 시점에 신설 예정. 현재 루트 직속 `03-xx` ~ `05-xx` 의 동시성 학습 노트 10편은 별도 갈래로 책 흐름과 무관하게 운영 중.

미작성 폴더는 해당 장 스크린샷이 들어올 때 비로소 생성한다. 빈 폴더 사전 생성은 하지 않는다.

## 두 번째 책 ↔ 정독 노트 매핑 (JVM Performance Engineering)

《JVM Performance Engineering》(Monica Beckwith) 갈래는 `ch14`부터 번호를 잇는다. 한 폴더가 책의 한 장에 대응하고, `01-NN`은 그 장 안 소주제 순번이다.

| 장 | 영어 제목 | 폴더 | 진척 | 실습 |
|----|----------|------|------|------|
| 1장 | The Performance Evolution of Java | [`ch14_jpe-evolution/`](./ch14_jpe-evolution/) | ✅ Java/JVM 성능 진화사 1편(01-01): HotSpot 실행엔진·tiered compilation·deopt·generational GC·Java 1.1~17 연대기 | — |
| 2장 | Performance and Type System | [`ch15_jpe-type-system/`](./ch15_jpe-type-system/) | ✅ 타입 시스템 진화와 성능 1편(01-01): 강한 정적 타입·generics·VarHandle·sealed/record·JOL object layout·Project Valhalla value class | — |

> 새 책의 나머지 장(3장 Monolithic to Modular 이후)은 해당 원문이 들어올 때 `ch16_*`/`ch17_*`처럼 번호를 이어 폴더를 신설한다.

## 작성 규칙

- 파일명 (《밑바닥》): `{장 폴더}/01-{NN}.{개관·운영 흡수본 제목}.md` 또는 `{장 폴더}/02-{절}.{책의 절 제목}.md`
- 파일명 (《JVM Performance Engineering》): `ch14_*/01-{NN}.{소주제 제목}.md` — 폴더가 장, `01-NN`은 장 안 소주제 순번
- 프론트매터 필수 필드: `title`, `tags`, `status`, `related`, `updated` (정독 노트는 `source`로 책 §범위+공식 스펙 URL 명시)
- 본문 톤: 한다체 통일, 문단형 우선, "왜?" 포함, AI 강조어("매우/굉장히/획기적/혁신적") 금지
- Mermaid 도식: pastel `fill` + `color:#000` 명시, sequenceDiagram에 `rect` 금지

상세 가드레일은 글로벌 하네스 `~/.claude/skills/content/writing/references/second-brain-harness.md` §4.5 (학습서 챕터별 실습 코드 예외) 참조.
