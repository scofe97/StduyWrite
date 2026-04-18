# GC 알고리즘과 튜닝
---
> 가비지 컬렉션의 기초 알고리즘부터 현대 저지연 컬렉터까지의 발전 흐름을 이해하고, 실무에서 GC를 튜닝하는 방법을 익힌다. Mark-Sweep부터 ZGC까지 각 알고리즘의 트레이드오프와 JVM 옵션, GC 로그 분석을 다룬다.

## 1. GC 기본 알고리즘

가비지 컬렉션은 더 이상 참조되지 않는 객체를 식별하고 메모리를 회수하는 과정이다. 세 가지 기본 알고리즘이 현대 GC의 토대를 이룬다.

### 1-1. Mark-Sweep(표시-쓸기)

가장 기본적인 알고리즘이다. **Mark** 단계에서 GC 루트(스택 변수, 정적 변수, JNI 참조 등)로부터 참조 트리를 순회하며 도달 가능한 객체에 표시한다. **Sweep** 단계에서 표시되지 않은 객체의 메모리를 회수한다.

단점은 두 가지다. 우선 Mark와 Sweep 동안 모든 애플리케이션 스레드를 멈춰야 하는 **STW(Stop-The-World)**가 발생한다. 그리고 회수된 공간이 불연속적으로 흩어져 **메모리 단편화(Fragmentation)**가 생기며, 이후 대용량 객체 할당이 실패할 수 있다.

### 1-2. Mark-Compact(표시-압축)

Mark 단계 이후 살아있는 객체를 메모리 한쪽으로 밀어 모아 단편화 문제를 해결한다. 빈 공간이 연속적으로 확보되어 대용량 할당에 유리하지만, 객체를 이동시킬 때 참조를 업데이트해야 하므로 Sweep보다 비용이 크다.

### 1-3. Copying(복사)

메모리를 두 영역(From, To)으로 나누고, GC 시 살아있는 객체만 From에서 To로 복사한다. 복사 과정에서 자연스럽게 압축이 이루어지며, 단편화가 없다. 단점은 전체 메모리의 절반만 실제로 사용할 수 있다는 점이다. Young Generation의 Eden→Survivor 이동에 이 방식이 사용된다.

## 2. 세대별 수집

**약한 세대별 가설(Weak Generational Hypothesis)**에 기반한다. 대부분의 객체는 짧은 시간 안에 죽고, 오래 살아남은 객체는 계속 살아남는 경향이 있다. 이 관찰에 따라 힙을 세대로 나누면 GC 효율이 높아진다.

힙은 두 세대로 나뉜다:

- **Young Generation**: 새로 생성된 객체가 할당된다. Eden과 Survivor(S0, S1) 두 영역으로 세분화된다
- **Old Generation(Tenured)**: Young에서 여러 번의 GC를 생존한 장수 객체가 승격(Promotion)되는 영역이다

GC 종류는 세 가지다:

- **Minor GC**: Young Generation만 수집한다. 빈번하게 발생하지만 빠르다
- **Major GC**: Old Generation을 수집한다. Minor GC보다 훨씬 오래 걸린다
- **Full GC**: 전체 힙과 Metaspace를 수집한다. 가장 긴 STW가 발생한다

Minor GC 과정은 다음과 같다. Eden이 가득 차면 살아있는 객체를 현재 활성 Survivor 영역으로 복사하고, 일정 횟수(`-XX:MaxTenuringThreshold`, 기본 15) 이상 생존한 객체는 Old Generation으로 승격한다.

## 3. GC 알고리즘 비교

| 컬렉터 | 대상 힙 | 최대 STW | 처리량 | 기본/권장 버전 |
|---|---|---|---|---|
| Serial GC | 소형(<1GB) | 수백ms~수초 | 낮음 | 클라이언트, 단일 코어 |
| Parallel GC | 중형 | 수백ms | 높음 | Java 8 기본 |
| CMS | 중대형 | 짧음(수십ms) | 중간 | Java 9 deprecated, 14 제거 |
| G1 GC | 대형(6GB~) | 예측 가능(<200ms) | 중상 | Java 9+ 기본 |
| ZGC | 초대형(수TB) | <1ms | 높음 | Java 15 정식 |
| Shenandoah | 대형 | <10ms | 중간 | OpenJDK 12+ |

## 4. G1GC 상세

G1(Garbage-First) GC는 Java 9부터 기본 컬렉터다. 힙을 고정 크기(1~32MB, 2의 제곱수)의 **Region**으로 나누어 관리한다. 각 Region은 동적으로 Eden, Survivor, Old, Humongous 역할을 맡는다.

**Humongous Region**은 Region 크기의 50%를 초과하는 대형 객체를 위한 특수 영역이다. 연속된 Region을 점유하며, Old Generation처럼 취급된다.

G1의 GC 단계는 다음과 같다:

- **Young GC**: Eden Region이 가득 차면 발생한다. 살아있는 객체를 Survivor/Old Region으로 이동한다
- **Concurrent Marking**: 애플리케이션 스레드와 동시에 실행되며, Old Region의 살아있는 객체를 식별한다
- **Mixed GC**: Young Region과 수집 효율이 높은 일부 Old Region을 함께 수집한다. 이것이 G1이 "Garbage-First"로 불리는 이유다. 수집할 때 가비지 비율이 높은 Region부터 처리한다
- **Full GC**: 위 단계가 메모리 압박을 따라가지 못할 때 발생하며 단일 스레드로 수행되어 매우 느리다

`-XX:MaxGCPauseMillis=200`으로 목표 정지 시간을 설정하면 G1이 이를 달성하도록 Region 선택과 GC 빈도를 자동 조정한다. 보장은 아니지만 최선을 다해 맞추려 한다.

## 5. ZGC

ZGC는 Java 15부터 정식 지원하는 저지연 컬렉터로, **힙 크기와 무관하게 정지 시간을 1ms 미만**으로 유지하는 것을 목표로 한다.

ZGC의 핵심 기술은 두 가지다.

**컬러 포인터(Colored Pointers)**: 객체 참조 포인터의 상위 비트에 GC 메타데이터를 직접 인코딩한다. 별도의 Mark 비트맵 없이 포인터 자체에서 객체 상태(Marked, Remapped, Finalizable)를 읽을 수 있어 오버헤드가 작다.

**로드 배리어(Load Barrier)**: 애플리케이션 스레드가 힙에서 객체 참조를 읽을 때마다 JIT 컴파일러가 삽입한 소량의 코드가 실행된다. 이 코드가 포인터 상태를 확인하고 필요하면 재매핑(Remapping)하여 항상 유효한 참조를 반환한다. 이 방식으로 GC 작업의 대부분을 애플리케이션 스레드와 동시에 수행할 수 있다.

ZGC의 GC 단계 대부분은 애플리케이션과 동시에 실행된다. STW가 필요한 단계는 GC 루트 마킹과 재배치 집합 초기화처럼 매우 짧은 구간에만 한정된다.

## 6. Shenandoah GC

Red Hat이 개발한 저지연 컬렉터로 OpenJDK 12부터 포함되었다. ZGC와 목표가 비슷하지만 구현 방식이 다르다. **동시 압축(Concurrent Compaction)**이 핵심 기술로, 객체를 이동하면서 발생하는 참조 업데이트를 STW 없이 애플리케이션과 동시에 수행한다. 포워딩 포인터(Brooks Pointer)를 사용하여 이동 중에도 원본 참조가 유효하도록 유지한다.

## 7. GC 튜닝 JVM 옵션

기본적인 힙 크기 설정부터 컬렉터 선택까지의 주요 옵션이다:

```bash
# 힙 크기
-Xms2g                          # 초기 힙 크기 (Xmx와 같게 설정 권장)
-Xmx2g                          # 최대 힙 크기

# 컬렉터 선택
-XX:+UseSerialGC                # Serial GC
-XX:+UseParallelGC              # Parallel GC
-XX:+UseG1GC                    # G1 GC
-XX:+UseZGC                     # ZGC (Java 15+)
-XX:+UseShenandoahGC            # Shenandoah

# G1 튜닝
-XX:MaxGCPauseMillis=200        # 목표 최대 정지 시간
-XX:G1HeapRegionSize=8m         # Region 크기 (1~32MB)
-XX:InitiatingHeapOccupancyPercent=45  # 동시 마킹 시작 힙 사용률

# Young Generation
-Xmn256m                        # Young Generation 크기
-XX:MaxTenuringThreshold=15     # Old 승격 전 최대 생존 횟수

# 스레드
-XX:ParallelGCThreads=8         # STW GC 병렬 스레드 수
-XX:ConcGCThreads=4             # 동시 GC 스레드 수
```

프로덕션 권장 패턴은 `-Xms`와 `-Xmx`를 동일하게 설정하는 것이다. 힙 크기 동적 조정 오버헤드를 없애고 예측 가능한 메모리 사용을 보장한다.

## 8. GC 로그 분석

GC 로그를 활성화하면 STW 시간, GC 빈도, 힙 사용 패턴을 분석할 수 있다:

```bash
-Xlog:gc*:file=gc.log:time,uptime,level,tags
```

GC 로그의 주요 확인 항목은 다음과 같다:

- **Pause 시간**: STW가 목표 시간 내에 있는지 확인한다
- **GC 빈도**: Minor GC가 너무 잦으면 Young Generation 크기를 늘린다
- **Promotion Failure**: Old Generation이 가득 찬 상태에서 승격이 실패하면 Full GC가 발생한다
- **Humongous Allocation**: G1에서 대형 객체 할당이 잦으면 Region 크기를 늘린다

GC 로그 분석 도구로는 GCEasy, GCViewer, JDK 내장 `jstat`이 있다:

```bash
# jstat으로 GC 통계 실시간 확인 (1초 간격)
jstat -gcutil <pid> 1000
```

`jstat` 출력에서 `FGC`(Full GC 횟수)가 증가하거나 `O`(Old 사용률)가 지속적으로 높으면 메모리 누수 또는 힙 크기 부족을 의심한다.
