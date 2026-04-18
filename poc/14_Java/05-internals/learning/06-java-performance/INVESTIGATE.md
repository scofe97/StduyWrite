# Java 성능: Deep Investigation
> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. JMH 벤치마크에서 흔히 저지르는 실수는 무엇인가?

### 왜 이 질문이 중요한가
잘못 작성된 벤치마크는 실제 성능과 반대 결론을 낼 수 있다. "A가 B보다 10배 빠르다"는 측정이 JIT 최적화의 부산물이었다면 프로덕션에서는 오히려 역전될 수 있다. JMH는 이런 함정을 방지하기 위한 프레임워크이지만, JMH를 사용하더라도 잘못된 패턴을 쓰면 의미 없는 결과가 나온다.

### 답변

**실수 1: Dead Code Elimination(DCE).** JIT는 결과가 사용되지 않는 연산을 제거한다. 벤치마크 결과가 놀랍도록 빠르다면 DCE를 의심해야 한다.

```java
// 잘못된 벤치마크: 결과를 버림 → JIT가 연산 자체를 제거할 수 있음
@Benchmark
public void badBenchmark() {
    Math.sqrt(data);  // 결과 미사용 → 제거 대상
}

// 올바른 패턴 1: 반환값으로 사용
@Benchmark
public double goodBenchmark() {
    return Math.sqrt(data);  // JMH가 반환값을 블랙홀에 소비
}

// 올바른 패턴 2: Blackhole 명시적 사용
@Benchmark
public void goodBenchmark2(Blackhole bh) {
    bh.consume(Math.sqrt(data));
}
```

**실수 2: Constant Folding.** 벤치마크 입력값이 상수면 JIT가 계산 결과를 컴파일 타임에 치환한다.

```java
// 잘못된 예: x, y가 final 상수
private final double x = 1.0, y = 2.0;

@Benchmark
public double bad() { return x + y; }  // JIT가 3.0으로 치환

// 올바른 예: @State + 일반 필드
@State(Scope.Benchmark)
public class MyState {
    double x = 1.0, y = 2.0;  // non-final
}
```

**실수 3: 워밍업 부족.** `@Warmup(iterations = 0)`이거나 워밍업 반복 횟수가 너무 적으면 C2 컴파일 전의 인터프리터/C1 성능을 측정하게 된다.

**실수 4: 탈출 분석으로 인한 객체 제거.** 벤치마크 내에서 생성한 객체가 탈출하지 않으면 힙 할당이 제거돼 "할당 비용 없음"이라는 잘못된 결론이 나온다. `-XX:-DoEscapeAnalysis`로 비교 측정하거나 `Blackhole.consume(object)`로 탈출을 강제한다.

**실수 5: OS/JVM 환경 변동.** 벤치마크 중 GC가 발생하거나 CPU 주파수가 변동되면 결과에 노이즈가 생긴다. `@Fork(value = 3)`으로 JVM을 여러 번 재시작해 결과의 분산을 확인해야 한다.

---

## Q2. async-profiler로 CPU 핫스팟을 찾는 실전 워크플로우는 무엇인가?

### 왜 이 질문이 중요한가
프로파일링 없이 성능 최적화를 시도하는 것은 측정 없이 코드를 수정하는 것과 같다. async-profiler는 JVM의 SafePoint 편향 없이 실제 CPU 시간을 측정하는 현존 최고의 Java 프로파일러다. 프로덕션 트래픽을 받는 상태에서도 낮은 오버헤드로 동작하므로 실무 적용성이 높다.

### 답변

async-profiler는 리눅스의 `perf_events`와 AsyncGetCallTrace API를 조합해 SafePoint 밖의 코드도 정확하게 샘플링한다. 기존 JVMTI 기반 프로파일러(YourKit, VisualVM)는 SafePoint에서만 샘플링해 SafePoint 사이에서 실행되는 핫코드를 놓칠 수 있다.

**워크플로우 Step 1: 프로세스에 attach해 CPU 프로파일링 시작**

```bash
# 실행 중인 Java 프로세스에 attach (PID 확인: jps -l)
./asprof -e cpu -d 30 -f flamegraph.html <PID>

# 또는 시작부터 프로파일링
java -agentpath:/path/to/libasyncProfiler.so=start,event=cpu,file=flamegraph.html MyApp
```

**워크플로우 Step 2: 플레임 그래프 해석**

플레임 그래프에서 **넓은 플래토(plateau)**를 찾는다. 수평 너비가 CPU 시간 비율이므로, 넓고 평평한 구간이 핫스팟이다.

```
플레임 그래프 읽는 법:
- X축: 샘플 횟수 비율 (CPU 시간)
- Y축: 스택 깊이
- 색상: 의미 없음 (구분용)
- 넓은 사각형 = 그 메서드가 CPU를 많이 사용
```

**워크플로우 Step 3: 할당 프로파일링으로 GC 압박 원인 찾기**

```bash
# CPU 대신 heap allocation 프로파일링
./asprof -e alloc -d 30 -f alloc.html <PID>

# Lock contention 프로파일링
./asprof -e lock -d 30 -f lock.html <PID>
```

**워크플로우 Step 4: 핫스팟 확인 후 JMH로 검증**

프로파일러가 특정 메서드를 핫스팟으로 지목하면, 해당 메서드만 격리해 JMH 벤치마크를 작성하고 최적화 전후를 비교한다. 프로파일러 → 격리 → JMH 검증 → 최적화 → 재프로파일링의 사이클을 반복하는 것이 실무 표준 워크플로우다.
