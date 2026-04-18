# GC 알고리즘과 튜닝: Deep Investigation
> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. ZGC가 서브밀리초 일시정지를 달성하는 원리는 무엇인가?

### 왜 이 질문이 중요한가
ZGC는 Java 15에서 production-ready가 됐고, Java 21에서 Generational ZGC가 추가됐다. 레이턴시에 민감한 서비스(결제, 실시간 API, 게임 서버)에서 GC 일시정지를 서비스 SLA의 핵심 지표로 관리한다. "어떤 GC를 선택해야 하는가?"라는 질문에 원리 기반으로 답하려면 ZGC의 동작 방식을 알아야 한다.

### 답변

ZGC가 서브밀리초 일시정지(일반적으로 < 1ms, 힙 크기와 무관)를 달성하는 핵심은 **착색 포인터(Colored Pointers)**와 **로드 배리어(Load Barrier)** 두 가지다.

**착색 포인터**는 64비트 객체 참조의 상위 비트를 GC 메타데이터로 활용한다. 참조가 가리키는 객체의 상태(Marked0, Marked1, Remapped, Finalizable)를 포인터 자체에 인코딩한다. 이를 통해 GC 스레드와 애플리케이션 스레드가 동시에 동작하면서도 객체의 현재 상태를 포인터만 보고 즉시 파악할 수 있다.

```
ZGC 참조 비트 구조 (64비트 중 상위 4비트 활용):
bit 43: Finalizable
bit 42: Remapped
bit 41: Marked1
bit 40: Marked0
나머지 42비트: 실제 객체 주소 (최대 4TB 힙 지원)
```

**로드 배리어**는 객체 참조를 읽을 때마다(heap load) JIT가 삽입하는 코드다. 참조의 색상 비트를 검사해 이동된 객체라면 즉시 포인터를 수정한다. STW 없이 애플리케이션 스레드가 실행 중에 포인터 수정이 완료된다.

ZGC의 GC 사이클은 다음과 같이 대부분 동시(concurrent)로 실행된다.

```
STW: Initial Mark (< 1ms) → 루트만 마킹
Concurrent: Mark All
STW: Final Mark (< 1ms) → 마킹 완료
Concurrent: Relocate (객체 이동)  ← 이것이 동시 실행의 핵심
```

실무 적용 시 주의점은 ZGC가 처리량(throughput)을 약간 희생한다는 것이다. 로드 배리어 오버헤드로 인해 같은 힙 크기에서 G1GC 대비 처리량이 5~15% 낮을 수 있다. 레이턴시 SLA가 10ms 이하인 서비스는 ZGC, 배치 처리나 처리량 우선 서비스는 G1GC가 일반적으로 적합하다.

---

## Q2. G1GC에서 Mixed GC가 트리거되는 조건과 튜닝 방법은?

### 왜 이 질문이 중요한가
G1GC는 Java 9부터 기본 GC이므로 대부분의 Java 애플리케이션에 직접 관련된다. Mixed GC를 이해하지 못하면 Old Gen이 꽉 차서 Full GC가 발생하는 상황을 예측하거나 방지할 수 없다. GC 로그 분석 → 튜닝 파라미터 조정의 흐름을 실무에서 반복하려면 이 메커니즘이 필수다.

### 답변

G1GC는 힙을 동일 크기의 Region으로 나눈다(1MB~32MB, 힙 크기에 따라 자동 결정). Young GC는 Eden/Survivor Region만 회수하고, Mixed GC는 Young Region + Old Region 일부를 함께 회수한다.

**Mixed GC 트리거 조건**: Concurrent Marking Cycle이 완료된 후, Old Gen 점유율이 `InitiatingHeapOccupancyPercent`(기본 45%) 이상일 때 다음 Young GC에 Old Region 회수를 추가해 Mixed GC로 전환한다.

```bash
# G1GC 핵심 튜닝 파라미터
-XX:MaxGCPauseMillis=200          # 목표 일시정지 시간 (기본 200ms)
-XX:InitiatingHeapOccupancyPercent=45  # Mixed GC 시작 임계값
-XX:G1HeapRegionSize=16m          # Region 크기 (큰 객체가 많으면 증가)
-XX:G1MixedGCCountTarget=8        # Mixed GC 사이클 수 (기본 8)
-XX:G1MixedGCLiveThresholdPercent=85  # 이 비율 이상 살아있는 Region은 회수 대상 제외

# GC 로그 활성화 (Java 11+)
-Xlog:gc*:file=gc.log:time,uptime,level,tags:filecount=5,filesize=20m
```

실무 튜닝 시나리오: Old Gen이 계속 쌓여 Full GC가 발생한다면 두 가지를 먼저 확인한다. 첫째, `IHOP`를 낮춰(예: 35%) Concurrent Marking을 더 일찍 시작해 Mixed GC가 빠르게 트리거되도록 한다. 둘째, `G1MixedGCCountTarget`을 낮춰 각 Mixed GC 사이클에서 더 많은 Old Region을 회수하게 한다.

```bash
# GC 로그에서 Mixed GC 확인
grep "Pause Mixed" gc.log

# Humongous 객체(Region 크기의 50% 초과) 확인 - 바로 Old Gen으로 가서 문제 유발
grep "Humongous" gc.log
```

Humongous 객체가 많다면 `G1HeapRegionSize`를 늘려 Humongous 임계값을 높이거나, 해당 객체의 생성 자체를 줄이는 코드 개선이 우선이다.
