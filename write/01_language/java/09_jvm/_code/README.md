# JVM 실습 코드

《JVM 밑바닥까지 파헤치기》(저우즈밍) 챕터별 실습 모듈을 모은다. 노트는 `09_jvm/chNN_*/` 폴더에, 실습 코드는 이 `_code/chNN/` 모듈에 있다. 두 자료를 같은 폴더 안에 두는 이유는 챕터 단위로 노트와 코드를 자주 오가기 때문이다. 자세한 배치 규약은 글로벌 하네스 `~/.claude/skills/content/writing/references/second-brain-harness.md` §4.5 를 따른다.

## 환경

| 항목 | 값 |
|------|------|
| JDK | OpenJDK 21 (Temurin 21.0.3 기준) |
| 빌드 도구 | Gradle 9.x (Kotlin DSL) |
| 모듈 추가 정책 | 책 진도에 맞춰 그때그때 추가, 미진행 챕터 사전 생성 금지 |

JDK 21 toolchain 은 `build.gradle.kts` 에서 강제하므로 로컬 `JAVA_HOME` 이 다른 버전이어도 Gradle 이 자동으로 21을 다운로드·사용한다.

## 실행

루트에서 챕터 모듈을 실행한다. 예시는 1챕터다.

```bash
./gradlew :ch01:run                    # 메인 실행
./gradlew :ch01:test                   # 테스트
./gradlew :ch01:dependencies           # 의존성 그래프
```

GC 로그를 활성화한 채 실행하려면 `tools/run-with-gc-log.sh` 래퍼를 쓴다.

```bash
./tools/run-with-gc-log.sh :ch01:run /tmp/gc.log
```

`javap` 역어셈블 결과는 `tools/decompile.sh` 로 챕터 빌드 후 한 번에 출력한다.

```bash
./gradlew :ch01:classes
./tools/decompile.sh ch01/build/classes/java/main/org/runners/jvm/ch01/SomeClass.class
```

## 챕터 모듈

각 챕터 실습이 만들어지면 이 표에 추가한다.

| 챕터 | 모듈 | 다루는 책의 절 | 상태 |
|------|------|---------------|------|
| 1장 | `:ch01` | 1.6 실전: JDK 빌드 (참고용 스크립트만) | ◻ |

미진행 챕터는 행을 추가하지 않는다.

## 패키지·코드 컨벤션

| 항목 | 규칙 |
|------|------|
| 패키지 | `org.runners.jvm.ch{NN}` |
| 출처 코멘트 | 책 예제 그대로 옮긴 클래스 상단에 `// 책 p.{쪽수}` 한 줄 |
| 실행 결과 | 노트 본문에 ```결과 코드블록으로 박제 |

## 의존성

공통 의존성은 루트 `build.gradle.kts` 의 `subprojects` 블록에서 관리한다.

| 라이브러리 | 용도 |
|------------|------|
| `org.openjdk.jol:jol-core` | 객체 메모리 레이아웃 측정 |
| `org.ow2.asm:asm`, `asm-tree`, `asm-util` | 바이트코드 조작 |
| `org.openjdk.jmh:jmh-core`, `jmh-generator-annprocess` | 마이크로벤치마크 |
| `org.junit.jupiter:junit-jupiter` | 단위 테스트 |
| `org.assertj:assertj-core` | 검증 표현 |
