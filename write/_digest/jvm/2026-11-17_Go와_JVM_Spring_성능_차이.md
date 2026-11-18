> 출처: Claude 대화 · 2026-11-17 · Go 와 JVM Spring 의 성능 차이와 실행 방식(AOT·JIT) 비교 · 분야: jvm-keywords · 미검증(경고·수치만 2026-11-18 에 1차 자료·로컬 실측으로 확인)

## 요점

한 줄: Go 와 Java 는 둘 다 정적 타입이라 갈리는 축은 실행 방식(AOT 기계어 대 바이트코드+JIT)이고, 최소 HTTP 서버 실측에서 기동 시간·쉴 때 RSS·산출물 크기는 Go 가 작았으며 처리량은 프레임워크에 따라 순위가 갈렸습니다.

- 전제 바로잡기:
  - Go 는 인터프리터 언어가 아닙니다. `go build` 가 기계어를 미리(AOT) 만들고 GC·스케줄러 런타임을 실행 파일에 함께 넣습니다.
  - Java 도 동적 언어가 아닙니다. 타입 검사는 컴파일 때 끝납니다. `javac` 는 바이트코드까지만 만들고 JVM 이 해석하다가 자주 도는 메서드를 C1·C2 로 JIT 컴파일합니다.
  - 해석 단계·리플렉션·실행 중 클래스 로딩·`invokedynamic` 같은 동적 성격은 오히려 JVM 쪽에 있고 Spring 이 리플렉션·프록시를 많이 씁니다.
- 기동: Go 는 클래스 로딩이 없습니다. Spring Boot 는 JVM 기동·클래스 로딩·빈 생성·프록시 생성이 겹치고 뜬 뒤에도 웜업 전이라 느립니다. 쿠버네티스에서는 오토스케일 반응·readiness·롤링 배포 시간으로 이어집니다.
- JVM 기동 완화책: CDS/AppCDS, Spring AOT 처리, GraalVM Native Image, CRaC, Leyden 계열 AOT 캐시.
- 최고 처리량: C2 는 실행 중 프로파일로 추측 인라이닝·가상 호출 제거를 하고 틀리면 역최적화합니다. Go 컴파일러는 빠른 컴파일을 우선하고 PGO 로 프로파일 파일을 주면 최적화를 더 합니다. 짧게 사는 프로세스(CLI·배치·서버리스)는 기동 시간이 짧은 Go 가 유리합니다.
- 메모리: Spring Boot 는 쉴 때 RSS 가 Go 서비스보다 큽니다. 힙 밖에 메타스페이스·코드 캐시·JIT/GC 스레드·스레드 스택이 있습니다. Java 객체는 헤더를 달고 참조로 흩어지지만, Go struct 는 값 타입이라 헤더 없이 배열에 그대로 깔립니다.
- GC:
  - Go 는 동시·비이동·비세대 mark-sweep 하나에 손잡이가 `GOGC`·`GOMEMLIMIT` 둘뿐입니다. 할당이 몰리면 할당하는 고루틴이 GC 일을 나눠 맡는 GC assist 로 지연이 생깁니다. 탈출 분석으로 힙 할당 자체를 줄이는 쪽입니다.
  - JVM 은 G1·ZGC·Parallel 중에서 고르는 세대·이동 방식이라, 새 객체 할당이 포인터 밀기로 쌉니다.
- 동시성:
  - Go 는 2 KB 스택으로 시작하는 고루틴을 M:N 스케줄러가 OS 스레드에 얹고 네트워크 대기는 netpoller 가 고루틴만 재웁니다.
  - Spring MVC 는 요청당 플랫폼 스레드(Tomcat 기본 최대 200)입니다. Java 21 가상 스레드는 Spring Boot 3.2 의 `spring.threads.virtual.enabled` 로 켭니다. WebFlux 는 적은 스레드로 많은 연결을 받지만 코드 모양이 바뀝니다.
- 비교의 함정: 「Spring 대 Go」 는 대개 「무거운 프레임워크 대 `net/http`」 입니다. 기동·메모리 차이의 큰 몫이 빈 생성·리플렉션·AOP 프록시·Jackson 에서 옵니다. Go+Gin 대 Spring, 순수 Java(Javalin) 대 Go 처럼 나눠서 같은 조건으로 직접 잽니다.
- 컨테이너 한도: JVM 은 cgroup 메모리·CPU 한도를 읽어 힙·스레드 수를 정합니다. 힙 비율은 `MaxRAMPercentage`(기본 25%)로 정합니다. Go 는 1.25 부터 `GOMAXPROCS` 가 cgroup CPU 한도를 따릅니다. 그 전에는 노드 CPU 수를 써서 throttling 을 맞을 수 있었습니다(automaxprocs 로 막음).
- 고르는 기준: 잴 수 있는 지표로만 봅니다. 기동 시간·쉴 때 RSS·산출물 크기는 아래 실측에서 Go 가 작았습니다. 처리량과 CPU 과제 시간은 공개 수치에서 과제와 프레임워크에 따라 앞선 쪽이 바뀝니다. 그래서 한쪽이 유리하다고 정하지 않고 같은 조건에서 직접 잽니다.

### 실측과 수치

이 절의 수치는 2026-11-18 에 1차 자료와 로컬 실측으로 붙였습니다. 대화 요약이 아닙니다.

로컬 실측은 macOS 26.6.2(arm64, 8코어, 16 GB) 한 대에서 쟀습니다. 리눅스 컨테이너의 값이 아닙니다. 대상은 `/hello` 에 `hello` 를 돌려주는 최소 서버 둘입니다. 구성 다섯을 번갈아 7회씩 띄웠습니다. 칸에는 중앙값(최소~최대)을 적었습니다. 35회 모두 200 응답을 받았습니다.

| 구성 | 기동 시간 ms | 쉴 때 RSS MiB | OS 스레드 수 |
| :--- | :--- | :--- | :--- |
| Go 1.25.1 `net/http` 실행 파일 | 10.6 (7.6~19.0) | 10.4 (10.2~10.4) | 5~6 |
| Spring Boot 4.1.2 Web MVC, Oracle GraalVM 25, fat jar | 849.4 (841.1~1142.4) | 215.7 (179.2~217.0) | 44 |
| Spring Boot 4.1.2 Web MVC, OpenJDK 25, fat jar | 818.4 (796.2~888.9) | 164.4 (158.2~172.0) | 44 |
| 위 구성에서 jar 를 풀어 실행 | 691.6 (677.9~815.6) | 160.9 (158.5~169.3) | 43 |
| 위 구성에 AOT 캐시(`-XX:AOTCache`) 추가 | 414.9 (369.7~463.2) | 179.5 (178.7~179.8) | 43~44 |

- 기동 시간은 프로세스를 띄운 시점부터 첫 200 응답을 받은 시점까지입니다. RSS 와 스레드 수는 첫 응답 뒤 요청 없이 5초 둔 시점의 `ps` 값입니다.
- JVM 은 옵션을 주지 않은 기본값입니다. 이 기계에서 최대 힙은 4 GiB(16 GB 의 25%)로 잡혔습니다.
- 기동 시간은 OpenJDK 25 fat jar 가 Go 의 77배입니다. AOT 캐시를 써도 39배입니다. 쉴 때 RSS 는 16배입니다.
- AOT 캐시는 기동을 691.6 ms 에서 414.9 ms 로 40% 줄였습니다. RSS 는 18.6 MiB 늘었습니다.
- Spring Boot 로그는 OpenJDK 25 fat jar 에서 「Started in 0.567 seconds (process running for 0.765)」 를 찍었습니다(중앙값). 0.2초가 Spring 이 시작하기 전 JVM 몫입니다. 0.57초가 컨텍스트와 내장 Tomcat 몫입니다.
- 빈이 거의 없는 서버라 큰 앱의 기동 시간은 이보다 깁니다. 아래 표의 PetClinic 수치가 그 예입니다.

산출물 크기는 같은 빌드를 `ls -l` 과 `du` 로 쟀습니다.

| 산출물 | 크기 MiB | 조건 |
| :--- | :--- | :--- |
| Go 실행 파일 | 7.4 | `go build` 기본값. `-ldflags="-s -w"` 를 주면 5.1 |
| Spring Boot fat jar | 19.0 | `gradle bootJar`, 의존성은 `spring-boot-starter-webmvc` 하나 |
| JVM 런타임 | 81.8 | OpenJDK 25 `jlink`, `jdeps` 가 뽑은 모듈 13개. 이 런타임으로 200 응답 확인 |
| JDK 전체 | 369.2 | OpenJDK 25 설치 폴더 |
| AOT 캐시 파일 | 51.3 | 위 표 다섯째 구성이 쓰는 파일 |

Go 는 실행 파일 하나(7.4 MiB)로 돕니다. Spring Boot 는 fat jar 와 런타임을 합쳐 100.8 MiB 가 필요해 13.7배입니다.

아래는 1차 자료와 소스·플래그 출력에서 가져온 수치입니다.

| 지표 | Go | JVM·Spring | 조건과 출처 |
| :--- | :--- | :--- | :--- |
| 큰 앱의 기동 시간 | 수치 없음 | 4.486초, AOT 캐시를 쓰면 2.604초(42% 단축) | Spring PetClinic 3.2.0(클래스 약 21,000개), JDK 23 대 JDK 24. 기계 사양은 문서에 없습니다. [JEP 483](https://openjdk.org/jeps/483) |
| 처리량, JSON 응답 | `net/http` 388,485 req/s | Spring MVC 328,413 req/s, Spring WebFlux 1,286,696 req/s | TechEmpower 23라운드(2025-02-24 공개), 연결 16~512개 중 최고값, 한 번에 15초. Go 1.19, Spring Boot 3.3.5(MVC 는 Undertow)·JRE 23. 서버는 ProLiant DL360 Gen10 Plus, 40 GbE. [결과 파일](https://www.techempower.com/benchmarks/results/round23/ph.json)·[시험 코드](https://github.com/TechEmpower/FrameworkBenchmarks/tree/523534bb61450e3522d775a749ad060753e26e3a) |
| 처리량, plaintext | `net/http` 1,612,144 req/s | Spring MVC 832,510 req/s, Spring WebFlux 2,464,711 req/s | 같은 라운드·같은 버전. HTTP 파이프라이닝, 연결 256~16,384개 중 최고값 |
| CPU 과제 경과 시간 | 10개 중 6개에서 더 빠름(1.02~1.66배) | 10개 중 4개에서 더 빠름(1.06~5.42배) | [Benchmarks Game 25.03](https://benchmarksgame-team.pages.debian.net/benchmarksgame/fastest/javavm-go.html), Go 1.23.1 대 Java 23(HotSpot), 4코어 i5-3330·Ubuntu 24.04. 언어마다 가장 빠른 프로그램의 경과 시간을 골라 견줬습니다. 경과 시간은 프로세스 전체를 잰 값입니다. 3개 과제(binary-trees·pidigits·regex-redux)는 사이트가 접근법·라이브러리가 달라 논쟁적이라고 표시했습니다. pidigits 의 두 언어 프로그램과 regex-redux 의 Java 프로그램에는 손으로 쓴 벡터 명령·unsafe·ffi 가능 표시(`*`)가 붙어 있습니다 |
| GC 정지 목표 | STW 정지를 GC 주기당 500마이크로초(2018년 목표) | ZGC 1 ms 이하, G1 200 ms(`MaxGCPauseMillis` 기본값) | 모두 목표값이고 보장이 아닙니다. [Go 블로그](https://go.dev/blog/ismmkeynote), [JEP 439](https://openjdk.org/jeps/439), [G1 튜닝 문서](https://docs.oracle.com/en/java/javase/25/gctuning/garbage-first-g1-garbage-collector1.html) |
| 객체 헤더 | 0바이트. `struct{ X, Y int32 }` 가 8바이트, 1,000개 배열이 8,000바이트 | 12~16바이트. Compact Object Headers 를 켜면 8바이트 | Go 는 로컬 `unsafe.Sizeof`(Go 1.25.1). JVM 은 [JEP 450](https://openjdk.org/jeps/450) |
| 스택 | 고루틴 시작 크기 2,048바이트 | 플랫폼 스레드 `ThreadStackSize` 2,048 KB | [stack.go](https://github.com/golang/go/blob/go1.25.1/src/runtime/stack.go) 의 `stackMin`, 로컬 `PrintFlagsFinal`(OpenJDK 25, macOS arm64). 앞은 늘어나기 전 시작 크기이고 뒤는 스레드당 스택 크기라 뜻이 다릅니다. JVM 값은 플랫폼마다 다릅니다 |
| 인라이닝 예산 | `inlineMaxBudget` 80, PGO 로 뜨겁다고 판정된 함수는 2,000 | `MaxInlineSize` 35, `FreqInlineSize` 325 | Go 는 AST 노드 비용이고 JVM 은 바이트코드 바이트 수라 단위가 다릅니다. 두 값을 서로 견주지 않습니다. [inl.go](https://github.com/golang/go/blob/go1.25.1/src/cmd/compile/internal/inline/inl.go), 로컬 `PrintFlagsFinal`(OpenJDK 25) |
| 기본 스레드 수 | `GOMAXPROCS` 8(이 기계의 논리 CPU 수) | Tomcat 요청 스레드 최대 200 | 로컬 `runtime.GOMAXPROCS(0)`(Go 1.25.1), [공통 애플리케이션 속성](https://docs.spring.io/spring-boot/appendix/application-properties/index.html). 앞은 Go 코드를 동시에 돌리는 스레드 수이고 뒤는 요청 스레드 풀 상한입니다 |

- 처리량은 한쪽으로 정리되지 않습니다. JSON 시험에서 Go `net/http` 는 Spring MVC 의 1.18배였습니다. Spring WebFlux 는 Go `net/http` 의 3.31배였습니다.
- TechEmpower 의 Go 시험 코드는 Go 1.19 로 빌드했고 Java 쪽은 JRE 23 입니다. 두 쪽의 버전 나이가 다릅니다.
- 오래 돈 뒤(웜업 뒤)의 처리량을 Go 와 JVM 에서 같은 조건으로 잰 수치는 찾지 못했습니다. 그 비교는 직접 재야 합니다.



## 핵심 키워드

| 키워드 | 한 줄 | 이미 있음 |
| :--- | :--- | :--- |
| AOT 컴파일 대 JIT 컴파일 | Go 는 빌드 때 기계어를 만들고, JVM 은 바이트코드를 해석하다 자주 도는 메서드만 C1·C2 로 컴파일 | [JIT 컴파일러](../../01_language/book/Inside the Java Virtual Machine JVM Advanced Features and Best Practices/ch04_compilation-optimization/02-01.JIT 컴파일러 — 인터프리터와 계층형 컴파일.md) (일부: JVM 쪽만, Go AOT 와의 비교 없음) |
| 정적 타입 대 동적 언어 | 타입을 컴파일 때 검사하느냐 실행 중에 검사하느냐의 축으로, Go·Java 는 둘 다 정적 | |
| JVM 의 동적 기능 | 리플렉션·실행 중 클래스 로딩·`invokedynamic` 처럼 Spring 이 기대는 실행 중 기능 | [리플렉션과 동적 클래스 처리](../../01_language/book/Inside the Java Virtual Machine JVM Advanced Features and Best Practices/ch03_class-loading-mechanism/02-06.리플렉션과 동적 클래스 처리.md) |
| 추측 인라이닝·역최적화 | 실행 중 프로파일로 인라이닝·가상 호출 제거를 하고, 가정이 깨지면 해석 실행으로 되돌리는 C2 최적화 | [메서드 인라인과 탈출 분석](../../01_language/book/Inside the Java Virtual Machine JVM Advanced Features and Best Practices/ch04_compilation-optimization/02-03.컴파일러 최적화 — 메서드 인라인과 탈출 분석.md) |
| PGO (Go) | CPU 프로파일 파일을 빌드에 넣어 뜨거운 코드에 인라이닝 등을 더 하는 Go 의 프로파일 기반 최적화 | |
| JVM 기동 가속 | CDS·Spring AOT 처리·Native Image·CRaC·Leyden AOT 캐시로 기동과 웜업을 줄이는 기술 | [시동 가속](../../01_language/book/Inside the Java Virtual Machine JVM Advanced Features and Best Practices/ch04_compilation-optimization/03-01.시동 가속 — CDS·AOT·Leyden·GraalVM·CRaC.md) (일부: Spring AOT 처리 없음) |
| 힙 밖 상주 메모리 | 메타스페이스·코드 캐시·스레드 스택처럼 쉴 때도 JVM RSS 를 키우는 영역 | [힙 밖에서 쌓이는 메모리](../../troubleshooting/_concepts/runtime-힙-밖에서-쌓이는-메모리.md) |
| 객체 헤더·Compact Object Headers | Java 객체마다 붙는 헤더와, 이를 한 워드로 줄이는 HotSpot 기능 | [핫스팟의 객체 들여다보기](../../01_language/book/Inside the Java Virtual Machine JVM Advanced Features and Best Practices/ch02_automatic-memory-management/01-02.핫스팟의 객체 들여다보기.md) (일부: 헤더 없이 값으로 깔리는 Go struct 와의 비교 없음) |
| Go GC (`GOGC`·`GOMEMLIMIT`·GC assist) | 동시·비이동·비세대 mark-sweep 에 손잡이 둘, 할당이 몰리면 할당 고루틴이 GC 를 거드는 구조 | [GOGC 와 GOMEMLIMIT](../../01_language/book/lgo_learning-go/06-03.값을 스택에 두면 가비지가 줄고 GOGC 와 GOMEMLIMIT 가 힙을 조절합니다.md) (일부: 탈출 분석과 두 손잡이만, mark-sweep 구조·GC assist 없음) |
| JVM GC 선택 (G1·ZGC·Parallel) | 지연·처리량 목표에 따라 세대·이동 방식 컬렉터를 고르는 일 | [GC 선택하기](../../01_language/book/Inside the Java Virtual Machine JVM Advanced Features and Best Practices/ch02_automatic-memory-management/02-10.GC 선택하기.md) |
| 고루틴·M:N 스케줄러 | 2 KB 스택으로 시작하는 고루틴을 런타임이 적은 OS 스레드에 나눠 태우는 방식 | [고루틴](../../01_language/book/lgo_learning-go/12-01.고루틴은 런타임이 나눠 돌리는 가벼운 스레드이고 채널로 값을 주고받습니다.md) |
| netpoller | 블로킹처럼 보이는 네트워크 읽기에서 OS 스레드 대신 고루틴만 재우는 런타임 장치 | [netpoller](../../01_language/docs/go/net/01-02.netpoller.md) |
| 요청당 스레드 대 고루틴 | Tomcat 스레드 풀(기본 최대 200)과 연결당 고루틴의 처리 모델 차이 | [thread-per-request 랩](../../09_spring/project/thread-per-request/README.md) |
| 가상 스레드·pinning | JVM 이 M:N 으로 스케줄하는 스레드와, `synchronized` 안 블로킹이 캐리어를 붙잡는 문제 | [Virtual Threads 기초](../../01_language/book/Inside the Java Virtual Machine JVM Advanced Features and Best Practices/ch05_efficient-concurrency/01-05.Virtual Threads 기초.md) |
| JVM 컨테이너 인식 | JVM 이 cgroup 메모리·CPU 한도를 읽어 힙·스레드 수를 정하는 기능 | [힙 밖에서 쌓이는 메모리](../../troubleshooting/_concepts/runtime-힙-밖에서-쌓이는-메모리.md) (일부: JDK-8146115 출처 한 줄, `MaxRAMPercentage` 로 힙 비율 정하는 설명 없음) |
| 컨테이너 CPU 한도와 `GOMAXPROCS` | Go 1.25 부터 `GOMAXPROCS` 기본값이 cgroup CPU 한도를 따르는 변화 | [Go 키워드](../../01_language/go-keywords.md) (일부: 키워드 표 한 행만, 정리한 노트 없음) |
| 프레임워크 몫과 언어 몫 | 기동·메모리 차이 중 Spring 의 빈·리플렉션·프록시가 만드는 몫을 언어 차이와 나눠 보는 관점 | |



## 경고

- ⚠ 기동·메모리 수치: 정정합니다. 대화의 「Go 수십 ms·Spring 수 초」, 「Spring Boot 쉴 때 수백 MB·Go 수십 MB」 는 경험치였습니다. 로컬 실측(macOS arm64)의 최소 서버에서 Go 는 10.6 ms·10.4 MiB 였습니다. Spring Boot 4.1.2 는 818.4 ms·164.4 MiB 였습니다. 초 단위 기동은 큰 앱의 값입니다. [JEP 483](https://openjdk.org/jeps/483) 이 PetClinic 을 JDK 23 에서 4.486초로 적었습니다. 확인됨.
- ⚠ 처리량 우열: 정정합니다. 「오래 도는 CPU 작업에서 JVM 이 따라잡거나 앞선다」 는 과제마다 갈립니다. [Benchmarks Game 25.03](https://benchmarksgame-team.pages.debian.net/benchmarksgame/fastest/javavm-go.html) 의 CPU 과제 10개에서 Go 가 6개, Java 가 4개에서 더 빨랐습니다. 다만 이 과제들은 가장 빠른 프로그램 기준으로 0.8~14초 도는 프로그램입니다. 웜업 뒤 서버 처리량을 같은 조건으로 잰 수치는 찾지 못했습니다. 확인됨.
- ⚠ Go 인라이닝 예산: 기본 예산은 `inlineMaxBudget = 80` 입니다. PGO 로 뜨겁다고 판정된 함수는 `inlineHotMaxBudget = 2000` 입니다. [inl.go](https://github.com/golang/go/blob/go1.25.1/src/cmd/compile/internal/inline/inl.go) 확인됨. JVM 의 `MaxInlineSize`·`FreqInlineSize` 와는 단위가 다릅니다. 어느 쪽 예산이 작은지는 이 값으로 정할 수 없습니다.
- ⚠ Go PGO: Go 1.20 에 미리보기로 들어와 Go 1.21 에서 정식이 됐습니다. [Go 1.21 릴리스 노트](https://go.dev/doc/go1.21) 확인됨.
- ⚠ `GOMEMLIMIT`: Go 1.19 에 소프트 메모리 한도로 들어왔습니다. [Go 1.19 릴리스 노트](https://go.dev/doc/go1.19) 확인됨.
- ⚠ `GOMAXPROCS`: Go 1.25 부터 Linux 에서 cgroup CPU 대역폭 한도가 논리 CPU 수보다 작으면 그 값을 기본값으로 씁니다. [Go 1.25 릴리스 노트](https://go.dev/doc/go1.25) 확인됨.
- ⚠ 고루틴 시작 스택: 정정합니다. 「수 KB」 가 아니라 `runtime/stack.go` 의 `stackMin = 2048`, 즉 2 KB 입니다(Windows 등 일부 OS 는 여분을 더함). [stack.go](https://github.com/golang/go/blob/master/src/runtime/stack.go) 확인됨.
- ⚠ Go GC 방식: mark-sweep·비이동·애플리케이션과 동시 실행은 [GC 가이드](https://go.dev/doc/gc-guide) 확인됨.
- ⚠ Go GC 비세대: 런타임 소스 [mgc.go](https://github.com/golang/go/blob/go1.25.1/src/runtime/mgc.go) 머리 주석의 「non-generational and non-compacting」 으로 확인됨. Green Tea GC 가 기본이 된 [Go 1.26](https://go.dev/doc/go1.26) 의 [mgc.go](https://github.com/golang/go/blob/release-branch.go1.26/src/runtime/mgc.go) 에도 같은 구절이 있습니다.
- ⚠ 세대 구분 ZGC: JDK 21 에 들어왔습니다. [JEP 439](https://openjdk.org/jeps/439) 확인됨.
- ⚠ 가상 스레드와 pinning: 가상 스레드는 JDK 21([JEP 444](https://openjdk.org/jeps/444)), `synchronized` pinning 해소는 JDK 24([JEP 491](https://openjdk.org/jeps/491)) 확인됨. 정정합니다. JEP 491 은 pinning 을 「거의 모든 경우」 없앤다고 적었고 네이티브 코드 호출처럼 남는 경우가 있습니다.
- ⚠ Compact Object Headers: JDK 24 에 실험 기능([JEP 450](https://openjdk.org/jeps/450))으로 들어왔습니다. JDK 25 에서 정식 기능([JEP 519](https://openjdk.org/jeps/519))이 됐고 JDK 27 에서 기본값([JEP 534](https://openjdk.org/jeps/534))이 됐습니다. 확인됨. 로컬 OpenJDK 25 에서 `UseCompactObjectHeaders` 기본값은 false 였습니다.
- ⚠ 객체 헤더 크기: 64비트 HotSpot 에서 96~128비트(12~16바이트)입니다. [JEP 450](https://openjdk.org/jeps/450) 확인됨.
- ⚠ AOT 클래스 로딩·링킹: JDK 24 입니다. [JEP 483](https://openjdk.org/jeps/483) 확인됨.
- ⚠ JVM 컨테이너 인식: JDK 10 의 JDK-8146115 가 [8u191 릴리스 노트](https://www.oracle.com/java/technologies/javase/8u191-relnotes.html)에 들어 있습니다. 확인됨.
- ⚠ `MaxRAMPercentage`: JDK 10 에 [JDK-8186248](https://bugs.openjdk.org/browse/JDK-8186248) 로 들어왔고 8u191 에도 백포트됐습니다. [JDK 10 릴리스 노트](https://www.oracle.com/java/technologies/javase/10-relnote-issues.html)·[8u191 릴리스 노트](https://www.oracle.com/java/technologies/javase/8u191-relnotes.html) 확인됨. 기본값은 25.0 입니다(로컬 OpenJDK 25·Oracle GraalVM 25 의 `PrintFlagsFinal`).
- ⚠ Spring Boot 가상 스레드: 3.2 부터 Java 21 에서 `spring.threads.virtual.enabled=true` 로 켭니다. [Spring Boot 3.2 릴리스 노트](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.2-Release-Notes)·[공통 애플리케이션 속성](https://docs.spring.io/spring-boot/appendix/application-properties/index.html) 확인됨.
- ⚠ Tomcat 최대 스레드: `server.tomcat.threads.max` 기본값 200 입니다. 가상 스레드를 켜면 이 값은 효과가 없습니다. [공통 애플리케이션 속성](https://docs.spring.io/spring-boot/appendix/application-properties/index.html) 확인됨.
