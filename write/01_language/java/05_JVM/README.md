---
title: JVM 학습 인덱스
tags: [jvm, hotspot, study-index, moc]
status: draft
related:
  - ./ch01_java-tech/01-01.JDK 구조와 바이트코드.md
  - ./ch01_java-tech/01-02.가상 머신 실행 서브시스템.md
  - ./ch01_java-tech/01-03.컴파일과 최적화.md
  - ./ch02_automatic-memory-management/02-01.GC 운영 — 로그와 튜닝.md
  - ./ch02_automatic-memory-management/02-02.Java 성능 — JMH와 측정 방법론.md
  - ./ch02_automatic-memory-management/03-01.기본 문제 해결 도구 — 명령줄 도구.md
  - ./ch02_automatic-memory-management/03-02.시각화 문제 해결 도구.md
  - ./ch02_automatic-memory-management/04-01.최적화 사례 분석.md
  - ./ch02_automatic-memory-management/04-02.실전 — Eclipse IDE 튜닝.md
  - ./ch06_class-file/01-01.클래스 파일 구조.md
  - ./ch06_class-file/01-02.바이트코드 명령어.md
  - ./ch03_class-loading-mechanism/02-01.클래스 로딩 시점과 생명주기.md
  - ./ch03_class-loading-mechanism/02-02.로딩·검증·준비.md
  - ./ch03_class-loading-mechanism/02-03.해석과 초기화.md
  - ./ch03_class-loading-mechanism/02-04.클래스 로더와 부모 위임 모델.md
  - ./ch03_class-loading-mechanism/02-05.자바 모듈 시스템과 클래스 로더 변화.md
  - ./ch03_class-loading-mechanism/03-01.런타임 스택 프레임 구조.md
  - ./ch03_class-loading-mechanism/03-02.메서드 호출 — 디스패치 완전 정복.md
  - ./ch03_class-loading-mechanism/03-04.동적 타입 언어 지원과 invokedynamic.md
  - ./ch03_class-loading-mechanism/03-05.스택 기반 해석 실행 엔진.md
  - ./ch03_class-loading-mechanism/04-01.톰캣의 클래스 로더 아키텍처.md
  - ./ch03_class-loading-mechanism/04-02.OSGi의 유연한 클래스 로더와 바이트코드 생성.md
  - ./ch03_class-loading-mechanism/04-03.실전 — 원격 실행 기능 설계.md
  - ./ch03_class-loading-mechanism/04-04.실전 — 바이트코드 치환과 실행.md
  - ./ch04_compilation-optimization/01-01.javac 컴파일러의 컴파일 과정.md
  - ./ch04_compilation-optimization/01-02.자바 구문 설탕 — 제네릭과 타입 소거.md
  - ./ch04_compilation-optimization/01-03.자바 구문 설탕 — 박싱·향상된 for·조건 컴파일.md
  - ./ch04_compilation-optimization/01-04.실전 — 플러그인 애너테이션 처리기.md
  - ./ch04_compilation-optimization/02-01.JIT 컴파일러 — 인터프리터와 계층형 컴파일.md
  - ./ch04_compilation-optimization/02-02.컴파일 대상과 핫스폿 탐지.md
  - ./ch04_compilation-optimization/02-03.컴파일러 최적화 — 메서드 인라인과 탈출 분석.md
  - ./ch04_compilation-optimization/02-04.컴파일러 최적화 — 공통식 제거·경계 검사 제거와 Graal.md
  - ./ch05_efficient-concurrency/01-01.하드웨어 효율과 자바 메모리 모델.md
  - ./ch05_efficient-concurrency/01-02.volatile·happens-before·원자성.md
  - ./ch05_efficient-concurrency/01-03.자바와 스레드 — 구현·스케줄링·상태.md
  - ./ch05_efficient-concurrency/01-04.자바와 가상 스레드 — Virtual Threads.md
  - ./ch05_efficient-concurrency/02-01.스레드 안전성 — 다섯 등급.md
  - ./ch05_efficient-concurrency/02-02.스레드 안전성 구현 — 동기화와 락.md
  - ./ch05_efficient-concurrency/02-03.락 최적화 — 스핀·제거·굵게·경량·편향.md
  - ./ch05_efficient-concurrency/03-01.스레드 생성과 생명주기.md
  - ./ch05_efficient-concurrency/03-02.메모리 가시성과 동기화.md
  - ./ch05_efficient-concurrency/03-03.생산자-소비자 패턴.md
  - ./ch05_efficient-concurrency/04-01.원자 연산과 동시성 컬렉션.md
  - ./ch05_efficient-concurrency/04-02.Executor 프레임워크.md
  - ./ch05_efficient-concurrency/04-03.ThreadLocal과 동시성 라이브러리.md
  - ./ch05_efficient-concurrency/05-01.Java Memory Model 심화.md
  - ./ch05_efficient-concurrency/05-02.Virtual Threads 기초.md
  - ./ch05_efficient-concurrency/05-03.Virtual Threads Pinning.md
  - ./ch05_efficient-concurrency/05-04.Structured Concurrency.md
  - ./ch14_jpe-evolution/01-01.Java와 JVM의 성능 진화사.md
  - ./ch15_jpe-type-system/01-01.타입 시스템의 진화와 성능.md
  - ./ch16_jpe-modular/01-01.모놀리식에서 모듈러로 — JPMS와 모듈 시스템.md
  - ./ch17_jpe-logging/01-01.통합 JVM 로깅 — Xlog와 비동기 로깅.md
  - ./ch18_jpe-perf-eng/01-01.성능 엔지니어링과 하드웨어·메모리 모델.md
  - ./ch18_jpe-perf-eng/01-02.동기화와 NUMA, JMH 벤치마킹.md
  - ./ch19_jpe-gc/01-01.TLAB·PLAB·NUMA-aware GC와 G1 심화.md
  - ./ch19_jpe-gc/01-02.ZGC 심화와 워크로드별 GC 선택.md
  - ./ch20_jpe-runtime/01-01.문자열 런타임 최적화.md
  - ./ch20_jpe-runtime/01-02.락과 동시성 — 동기화부터 Virtual Threads까지.md
  - ./ch21_jpe-startup/01-01.시동 가속 — CDS·AOT·Leyden·GraalVM·CRaC.md
  - ./ch21_jpe-startup/01-02.HotSpot warm-up 최적화와 Metaspace.md
  - ./ch22_jpe-exotic-hw/01-01.Exotic Hardware와 JVM — 클라우드·툴체인.md
  - ./ch22_jpe-exotic-hw/01-02.케이스 스터디와 Project Panama.md
updated: 2026-06-03
---

# JVM 학습 인덱스
---
> 이 폴더는 단행본 《JVM 밑바닥까지 파헤치기》의 **절 단위 정독 노트** 갈래(`chNN_*` 폴더)로 구성된다. 책의 *부(部)* 단위로 폴더를 묶는다 — 2부 "자동 메모리 관리"(원서 2~5장)는 [`ch02_automatic-memory-management/`](./ch02_automatic-memory-management/) 한 폴더에 장번호로 통합돼 있어, `01-NN`이 메모리 영역(2장), `02-NN`이 가비지 컬렉션(3장, 운영·JMH는 `02-01~02-02` / GC 본문은 `02-03~02-10`), `03-NN`이 진단 도구(4장), `04-NN`이 최적화 실전(5장)이다. 과거의 "부 단위 루트 요약" 레이어는 정독 폴더로 흡수했다 — 책 1·3·4부 요약은 [`ch01_java-tech/`](./ch01_java-tech/) 의 `01-NN` 파일(개관 갈래)로 이동했고, 5부는 [`ch05_efficient-concurrency/`](./ch05_efficient-concurrency/) 정독 폴더로 풀어 썼다(12장=`01-NN` 4편, 13장=`02-NN` 3편). 옛 5부 부 요약 [`_temp/01-04`](./_temp/01-04.효율적%20동시성.md) 는 정독본으로 대체됐으나 요약 갈래로 보존한다. 실습 코드는 `_practice/` 서브폴더에서 챕터별 Gradle 모듈로 모인다.
>
> **동시성 갈래의 예외 — 출처 혼합 허용**: 책별로 폴더를 가르는 게 원칙이지만, [`ch05_efficient-concurrency/`](./ch05_efficient-concurrency/) 만은 *주제(동시성)* 를 우선해 두 책을 한 폴더에 둔다. `01-NN`·`02-NN`(《밑바닥》 12·13장 정독)에 더해, 출처가 《자바 동시성 프로그래밍》(또는 동등 도서)인 실무 학습 노트 10편을 `03-NN`~`05-NN`으로 합류시켰다(2026-06-17 루트 직속에서 이관). 폴더 안에서 책 구분은 각 노트의 `source` 필드가 1차 기준이다.
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
├── chNN_{topic}/                      # 단행본 절 단위 정독 노트
│   ├── 01-NN.{개관·운영 흡수본}.md       # 옛 루트 부 요약의 정독 폴더 이주본
│   └── 02-{절}.{제목}.md                  # 책의 절 정독 노트
│   └── (ch05만) 03~05-NN              # 《자바 동시성》 실무 노트 10편 (이관)
├── _temp/                             # 옛 5부 부 요약 보존 (정독본 ch05로 대체됨)
└── _practice/                             # 챕터별 Gradle 실습 코드
    ├── settings.gradle.kts
    ├── build.gradle.kts
    └── chNN/
        └── src/main/java/org/runners/jvm/chNN/...
```

폴더 안 노트 번호의 첫 숫자는 *그 폴더가 담은 책의 장(章) 순번*이다. 한 폴더에 여러 장이 들어가면(예: `ch04`는 10·11장) `01-NN`=앞 장, `02-NN`=뒤 장으로 갈린다. `ch02`·`ch03`처럼 `01-NN`이 개관/운영 흡수본(옛 루트 부 요약), `02-NN`이 절 정독인 곳도 있는데, 이는 그 폴더의 첫 묶음이 흡수본이었던 사정 때문이다. `ch05`는 12·13장을 담아 `01-NN`이 12장(메모리 모델·스레드), `02-NN`이 13장(스레드 안전성·락 최적화) 절 정독이다.

## 부 요약 흡수 이력

옛 루트 부 요약(01-01~02-02) 6편은 다음 위치로 이주됐다. 이중 레이어를 폐기하고 정독 폴더 안으로 일원화한 결과다.

| 옛 위치 | 다루는 부 | 새 위치 |
|--------|----------|---------|
| 01-01.JDK 구조와 바이트코드 | 3부 6장 + 1부 일부 | [`ch01_java-tech/01-01.JDK 구조와 바이트코드.md`](./ch01_java-tech/01-01.JDK%20구조와%20바이트코드.md) |
| 01-02.가상 머신 실행 서브시스템 | 3부 7~8장 | [`ch01_java-tech/01-02.가상 머신 실행 서브시스템.md`](./ch01_java-tech/01-02.가상%20머신%20실행%20서브시스템.md) |
| 01-03.컴파일과 최적화 | 4부 10~11장 | [`ch01_java-tech/01-03.컴파일과 최적화.md`](./ch01_java-tech/01-03.컴파일과%20최적화.md) |
| 01-04.효율적 동시성 | 5부 12장 | [`ch05_efficient-concurrency/`](./ch05_efficient-concurrency/) 정독 4편으로 풀어 씀 (01-01~01-04) |
| 01-04.효율적 동시성 | 5부 13장 | [`ch05_efficient-concurrency/`](./ch05_efficient-concurrency/) 정독 3편으로 풀어 씀 (02-01~02-03) |
| 02-01.GC 알고리즘과 튜닝 | 2부 3장 | §6,§7만 [`ch02_automatic-memory-management/02-01.GC 운영 — 로그와 튜닝.md`](./ch02_automatic-memory-management/02-01.GC%20운영%20—%20로그와%20튜닝.md), §3 비교표는 [`ch02_automatic-memory-management/02-10.마치며.md`](./ch02_automatic-memory-management/02-10.마치며.md) 의 §3a로 흡수. §1,§2,§4,§5는 정독 노트와 중복으로 제거 |
| 02-02.Java 성능 | 2부 4~5장 | [`ch02_automatic-memory-management/02-02.Java 성능 — JMH와 측정 방법론.md`](./ch02_automatic-memory-management/02-02.Java%20성능%20—%20JMH와%20측정%20방법론.md) |

## 책 목차 ↔ 정독 노트 매핑

진척률 컬럼은 사이클마다 갱신한다. ⏳ = 진행 중, ✅ = 완료, ◻ = 미착수.

### 1부 자바와 친해지기

| 장 | 한국어 제목 | 폴더 | 진척 | 실습 |
|----|------------|------|------|------|
| 1장 | 자바 기술 시스템 소개 | [`ch01_java-tech/`](./ch01_java-tech/) | ⏳ §1.5~§1.7 정독 완료, 개관 흡수본 3편(01-01~01-03) 추가, §1.1~§1.4 보류 | [`_practice/ch01/`](./_practice/ch01/) |

### 2부 자동 메모리 관리

| 장 | 한국어 제목 | 폴더 | 진척 | 실습 |
|----|------------|------|------|------|
| 2장 | 자바 메모리 영역과 메모리 오버플로 | [`ch02_automatic-memory-management/`](./ch02_automatic-memory-management/) `01-NN` | ✅ §2.1~§2.5 | [`_practice/ch02-memory-area/`](./_practice/ch02-memory-area/) |
| 3장 | 가비지 컬렉터와 메모리 할당 전략 | [`ch02_automatic-memory-management/`](./ch02_automatic-memory-management/) `02-NN` | ✅ §3.1~§3.9 + 운영 흡수본 (02-01) + GC 스레드 흡수본 (02-11, Beckwith Ch1에서) | [`_practice/ch03-gc/`](./_practice/ch03-gc/) |
| 4장 | 가상 머신 성능 모니터링과 문제 해결 도구 | [`ch02_automatic-memory-management/`](./ch02_automatic-memory-management/) `03-NN` | ✅ §4.1~§4.4.1 정독(p.197~245, 03-01 명령줄 + 03-02 시각화), §4.5 마치며 ⏳ 스크린샷 미확보. GC 로그·jstat·튜닝은 [`02-01`](./ch02_automatic-memory-management/02-01.GC%20운영%20—%20로그와%20튜닝.md) 운영 갈래에 별도 흡수 유지 | [`_practice/ch04-troubleshooting/`](./_practice/ch04-troubleshooting/) |
| 5장 | 최적화 사례 분석 및 실전 | [`ch02_automatic-memory-management/`](./ch02_automatic-memory-management/) `04-NN` | ✅ §5.1~§5.4 정독(p.253~283, 04-01 사례분석 + 04-02 실전). JMH·성능 측정 방법론은 [`02-02`](./ch02_automatic-memory-management/02-02.Java%20성능%20—%20JMH와%20측정%20방법론.md) 흡수본에 별도 유지 | [`_practice/ch05-optimization/`](./_practice/ch05-optimization/) |

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
| 12장 | 자바 메모리 모델과 스레드 | [`ch05_efficient-concurrency/`](./ch05_efficient-concurrency/) | ✅ §12.1~§12.5 정독 4편(01-01 하드웨어·JMM + 01-02 volatile·happens-before + 01-03 스레드 구현·상태 + 01-04 Virtual Threads) | — |
| 13장 | 스레드 안전성과 락 최적화 | [`ch05_efficient-concurrency/`](./ch05_efficient-concurrency/) | ✅ §13.1~§13.3 정독 3편(02-01 안전성 다섯 등급 + 02-02 동기화·락 구현 + 02-03 락 최적화 5기법) | — |

> 5부 정독 폴더 [`ch05_efficient-concurrency/`](./ch05_efficient-concurrency/) 는 12·13장 모두 신설 완료(2026-06-17). 12장 4편(`01-NN`) + 13장 3편(`02-NN`). 여기에 더해 《자바 동시성 프로그래밍》 출처 실무 노트 10편을 같은 폴더 `03-NN`~`05-NN`으로 이관 완료(2026-06-17, 옛 루트 직속). 《밑바닥》 정독(01·02)과 실무 노트(03~05)는 겹치는 주제를 각 노트의 §관련 문서에서 서로 교차참조한다.

미작성 폴더는 해당 장 스크린샷이 들어올 때 비로소 생성한다. 빈 폴더 사전 생성은 하지 않는다.

## 두 번째 책 ↔ 정독 노트 매핑 (JVM Performance Engineering)

《JVM Performance Engineering》(Monica Beckwith) 갈래는 `ch14`부터 번호를 잇는다. 한 폴더가 책의 한 장에 대응하고, `01-NN`은 그 장 안 소주제 순번이다.

| 장 | 영어 제목 | 폴더 | 진척 | 실습 |
|----|----------|------|------|------|
| 1장 | The Performance Evolution of Java | [`ch14_jpe-evolution/`](./ch14_jpe-evolution/) | ✅ Java/JVM 성능 진화사 1편(01-01): HotSpot 실행엔진·tiered compilation·deopt·generational GC·Java 1.1~17 연대기. §4 GC 알고리즘 상세는 ch02(02-04/06/07)로 위임 압축, GC 스레드 운영은 ch02 02-11로 흡수(2026-06-16) | — |
| 2장 | Performance and Type System | [`ch15_jpe-type-system/`](./ch15_jpe-type-system/) | ✅ 타입 시스템 진화와 성능 1편(01-01): 강한 정적 타입·generics·VarHandle·sealed/record·JOL object layout·Project Valhalla value class | — |
| 3장 | From Monolithic to Modular Java | [`ch16_jpe-modular/`](./ch16_jpe-modular/) | ✅ 모놀리식에서 모듈러로 1편(01-01): JPMS·module-info·ServiceLoader·ModuleLayer로 JAR hell versioning 우회·OSGi 비교·jdeps/jlink/jmod/jdeprscan | — |
| 4장 | Unified Logging System | [`ch17_jpe-logging/`](./ch17_jpe-logging/) | ✅ 통합 JVM 로깅 1편(01-01): JEP 158 -Xlog 네 축(tag·level·decorator·output)·계층적 레벨·jcmd 런타임 동적 조정·비동기 로깅(-Xlog:async) | — |
| 5장 | End-to-End Performance Optimization | [`ch18_jpe-perf-eng/`](./ch18_jpe-perf-eng/) | ✅ 2편: 01-01 성능 엔지니어링과 하드웨어·메모리 모델(footprint/responsiveness/throughput/availability·STW·SMT·store buffering), 01-02 동기화와 NUMA·JMH 벤치마킹(barrier/fence/volatile·happens-before·CAS/LSE·perfasm) | — |
| 6장 | Advanced Memory Management and GC | [`ch19_jpe-gc/`](./ch19_jpe-gc/) | ✅ 2편: 01-01 TLAB·PLAB·NUMA-aware GC와 G1 심화(region·IHOP·humongous·mixed collection 튜닝), 01-02 ZGC 심화와 워크로드별 GC 선택(colored pointer·load barrier·ZPage·6트리거·OLAP/OLTP/HTAP·LDS) | — |
| 7장 | Runtime Performance Optimizations | [`ch20_jpe-runtime/`](./ch20_jpe-runtime/) | ✅ 2편: 01-01 문자열 런타임 최적화(string pool·intern·G1 dedup·indy-fication·compact string), 01-02 락과 동시성(monitor lock·contended locking JEP 143·spin-wait·Executor/ForkJoinPool/CompletableFuture·virtual thread/continuation) | — |
| 8장 | Accelerating Time to Steady State | [`ch21_jpe-startup/`](./ch21_jpe-startup/) | ✅ 2편: 01-01 시동 가속(time-to-steady-state·CDS·AOT·Project Leyden training run·GraalVM native image·CRIU/CRaC), 01-02 HotSpot warm-up 최적화와 Metaspace(tiered C1/C2·Segmented CodeCache·speculative·PermGen→Metaspace·JEP 387) | — |
| 9장 | Harnessing Exotic Hardware | [`ch22_jpe-exotic-hw/`](./ch22_jpe-exotic-hw/) | ✅ 2편: 01-01 Exotic Hardware와 JVM(GPU/FPGA·OpenCL·AVX-512/SVE·클라우드 4도전·언어/툴체인), 01-02 케이스 스터디와 Project Panama(LWJGL/JNI·Aparapi·Sumatra/HSAIL·TornadoVM·Vector API·FFM API·Babylon/HAT) | — |

> **《JVM Performance Engineering》(Monica Beckwith) 전권 9장 완간** (2026-06-03). ch14~ch22, 총 14편. 9장이 책의 마지막 장이다.

## 작성 규칙

- 파일명 (《밑바닥》): `{장 폴더}/01-{NN}.{개관·운영 흡수본 제목}.md` 또는 `{장 폴더}/02-{절}.{책의 절 제목}.md`
- 파일명 (《JVM Performance Engineering》): `ch14_*/01-{NN}.{소주제 제목}.md` — 폴더가 장, `01-NN`은 장 안 소주제 순번
- 프론트매터 필수 필드: `title`, `tags`, `status`, `related`, `updated` (정독 노트는 `source`로 책 §범위+공식 스펙 URL 명시)
- 본문 톤: 한다체 통일, 문단형 우선, "왜?" 포함, AI 강조어("매우/굉장히/획기적/혁신적") 금지
- Mermaid 도식: pastel `fill` + `color:#000` 명시, sequenceDiagram에 `rect` 금지

상세 가드레일은 글로벌 하네스 `~/.claude/skills/content/writing/references/second-brain-harness.md` §4.5 (학습서 챕터별 실습 코드 예외) 참조.
