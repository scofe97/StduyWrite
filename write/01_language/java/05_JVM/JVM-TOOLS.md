---
title: JVM 도구·명령어·플래그 레퍼런스
tags: [jvm, tooling, java, javac, javap, jcmd, jstack, jmap, jvm-options, hub]
status: draft
updated: 2026-06-24
---

# JVM 도구·명령어·플래그 레퍼런스

`java`·`javac`·`javap` 같은 JDK 도구와 그 플래그를 한 곳에서 찾는 허브입니다. 각 도구의 *깊은 설명*은 그 도구를 처음 만나는 챕터 노트(SSOT)에 있고, 이 문서는 **"어디서 무엇을 찾는지"** 와 **"자주 쓰는 명령 형태"** 를 카탈로그로 모읍니다. 실습마다 흩어지는 명령을 매번 다시 검색하지 않으려는 게 목적입니다.

> 실습 코드 모듈 쪽 실행 명령(Gradle task·래퍼 스크립트)은 `_practice/JVM-OPTIONS.md` 에 따로 둡니다. 이 문서는 *개념을 이해하는* 도구 레퍼런스, 그쪽은 *실습을 돌리는* 실행 레퍼런스로 역할이 갈립니다.




## 옵션 문법 — 형태로 성격을 읽는다

`java` 플래그는 형태만 봐도 부류를 짐작할 수 있습니다. 부류를 알면 처음 보는 옵션도 어느 성격인지 가늠됩니다.

| 형태 | 부류 | 뜻 | 예 |
|------|------|-----|-----|
| `-옵션` | 표준 | 모든 JVM이 보장, 잘 안 바뀜 | `-cp`, `-version`, `-server` |
| `-X옵션` | 비표준 | 벤더별, 다음 버전에 바뀔 수 있음 | `-Xmx`, `-Xint`, `-Xcomp` |
| `-XX:+옵션` / `-XX:-옵션` | 고급(스위치) | `+`는 켜기, `-`는 끄기 | `-XX:+PrintCompilation`, `-XX:-TieredCompilation` |
| `-XX:옵션=값` | 고급(값) | 수치·문자열 값 지정 | `-XX:MaxInlineSize=35` |

> `-XX:+/-` 의 부호를 헷갈리지 마세요. **`+`가 켜기, `-`가 끄기**입니다. `-XX:-TieredCompilation` 은 "끈다" 는 뜻입니다.




## 도구별 카탈로그

### java — 실행과 런타임 플래그

프로그램을 실행하고, JIT·GC·메모리 동작을 플래그로 제어합니다.

| 플래그 | 무엇을 하나 | 예 |
|--------|------------|-----|
| `-cp` / `-classpath` | 클래스·JAR 탐색 경로 | `java -cp out App` |
| `-XX:-TieredCompilation` | 계층형 컴파일 끄고 C2만 강제 | 가시성 버그 재현율 ↑ |
| `-Xint` | JIT 끄고 인터프리터만 | 바이트코드 그대로의 동작 관찰 |
| `-Xcomp` | 첫 호출부터 즉시 컴파일 | warm-up 없이 컴파일 코드 관찰 |
| `-XX:+PrintCompilation` | JIT 컴파일 시점 로그 | 핫스폿이 컴파일되는 순간 추적 |
| `-Xmx` / `-Xms` | 최대 / 초기 힙 크기 | `-Xmx512m` |
| `-Xlog:gc*` | GC 통합 로깅 (JDK 9+) | GC 동작 관찰 |

> JIT의 C1/C2·계층형 컴파일·핫스폿 탐지의 깊은 설명 → [ch04 02-01 JIT 컴파일러](./ch04_compilation-optimization/02-01.JIT%20컴파일러%20—%20인터프리터와%20계층형%20컴파일.md), [ch04 02-02 컴파일 대상과 핫스폿 탐지](./ch04_compilation-optimization/02-02.컴파일%20대상과%20핫스폿%20탐지.md)
> GC·메모리 플래그의 맥락 → [ch02 자동 메모리 관리](./ch02_automatic-memory-management/), 튜닝 플래그 전반 → [jpf 03-02 VM 정보·튜닝 플래그](./book/jpf_java-performance/03-02.JDK%20기본%20도구와%20VM%20정보·튜닝%20플래그.md)



### javac — 소스를 바이트코드로 (프론트엔드 컴파일)

| 플래그 | 무엇을 하나 | 예 |
|--------|------------|-----|
| `-d <dir>` | `.class` 출력 디렉토리 (패키지 경로대로 생성) | `javac -d out App.java` |
| `-cp` | 컴파일 시 의존 클래스 경로 | |
| `-processor` | 애너테이션 처리기 지정 | |
| `-Xlint` | 의심스러운 코드 경고 | `javac -Xlint:all App.java` |

> javac의 세 단계(파싱·애너테이션 처리·의미 분석)와 구문 설탕의 깊은 설명 → [ch04 01-01 javac 컴파일 과정](./ch04_compilation-optimization/01-01.javac%20컴파일러의%20컴파일%20과정.md), 애너테이션 처리기 실습 → [ch04 01-03](./ch04_compilation-optimization/01-03.실전%20—%20플러그인%20애너테이션%20처리기.md)



### javap — 클래스 파일 역어셈블

`.class` 안의 바이트코드·상수풀·메이저 버전을 들여다봅니다.

| 플래그 | 무엇을 하나 | 예 |
|--------|------------|-----|
| `-v` | verbose: 상수풀·메이저 버전·스택맵까지 | `javap -v App` |
| `-c` | 메서드 바이트코드 본문 출력 | `javap -c App` |
| `-p` | private 멤버 포함 | `javap -p -c App` |
| `-s` | 타입 시그니처(디스크립터) 출력 | |

> 메이저 버전으로 컴파일 JDK를 알 수 있습니다: **65 = Java 21**, 61 = Java 17, 52 = Java 8.
> 바이트코드로 디스패치(`invokevirtual`/`invokedynamic`)를 읽는 깊은 활용 → [ch03 03-02 메서드 호출 디스패치](./ch03_class-loading-mechanism/03-02.메서드%20호출%20—%20디스패치%20완전%20정복.md)

### jcmd · jstack · jmap — 가동 중 JVM 진단

실행 중인 JVM 프로세스(PID)에 붙어 상태를 들여다봅니다.

| 도구 | 무엇을 하나 | 예 |
|------|------------|-----|
| `jcmd <pid> <명령>` | 만능 진단 디스패처 (힙 덤프·스레드·플래그) | `jcmd <pid> GC.heap_dump /tmp/h.hprof` |
| `jstack <pid>` | 모든 스레드의 스택 덤프 (데드락 진단) | `jstack <pid>` |
| `jmap <pid>` | 힙 요약·히스토그램·덤프 | `jmap -histo <pid>` |
| `jstat <옵션> <pid>` | GC·클래스로딩 통계 주기 출력 | `jstat -gc <pid> 1s` |

> 명령줄 진단 도구의 깊은 설명 → [ch02 03-01 기본 문제 해결 도구 — 명령줄 도구](./ch02_automatic-memory-management/03-01.기본%20문제%20해결%20도구%20—%20명령줄%20도구.md)
> 시각화 도구(JConsole·VisualVM) → [ch02 03-02 시각화 문제 해결 도구](./ch02_automatic-memory-management/03-02.시각화%20문제%20해결%20도구.md)
> JVM 통합 로깅(`-Xlog`) → [ch02 03-03 통합 JVM 로깅](./ch02_automatic-memory-management/03-03.통합%20JVM%20로깅%20—%20Xlog와%20비동기%20로깅.md)




## 빠른 진단 레시피

자주 쓰는 조합을 명령 형태로 박아 둡니다. 상세 맥락은 위 카탈로그의 링크를 따라가세요.

```bash
# 클래스가 어느 JDK로 컴파일됐나 (major version 확인)
javap -v App.class | grep "major version"

# 실행 중 JVM 힙 덤프
jcmd <pid> GC.heap_dump /tmp/heap.hprof

# 데드락 의심 — 전체 스레드 스택
jstack <pid>

# JIT가 무엇을 언제 컴파일하나
java -XX:+PrintCompilation App

# 가시성 버그 재현 (C2 강제)
java -XX:-TieredCompilation VisibilityBug
```




## 관련 문서

- [ch04 02-01 JIT 컴파일러 — 인터프리터와 계층형 컴파일](./ch04_compilation-optimization/02-01.JIT%20컴파일러%20—%20인터프리터와%20계층형%20컴파일.md) — `-XX:-TieredCompilation`·C1/C2의 개념 SSOT입니다.
- [ch04 01-01 javac 컴파일러의 컴파일 과정](./ch04_compilation-optimization/01-01.javac%20컴파일러의%20컴파일%20과정.md) — `javac` 플래그가 작동하는 컴파일 파이프라인입니다.
- [ch03 03-02 메서드 호출 — 디스패치 완전 정복](./ch03_class-loading-mechanism/03-02.메서드%20호출%20—%20디스패치%20완전%20정복.md) — `javap` 로 바이트코드를 읽는 깊은 활용입니다.
- [ch02 03-01 기본 문제 해결 도구 — 명령줄 도구](./ch02_automatic-memory-management/03-01.기본%20문제%20해결%20도구%20—%20명령줄%20도구.md) — `jcmd`·`jstack`·`jmap` 의 진단 SSOT입니다.
- [ch05 01-02 volatile·happens-before·원자성](./ch05_efficient-concurrency/01-02.volatile·happens-before·원자성.md) — `-XX:-TieredCompilation` 로 재현하는 가시성 버그가 나온 곳입니다.
