# 효율적 동시성: Deep Investigation
> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. 편향 락 → 경량 락 → 중량 락 전이가 성능에 미치는 영향은 무엇인가?

### 왜 이 질문이 중요한가
`synchronized` 키워드의 성능 비용은 "항상 느리다"가 아니라 경합(contention) 상황에 따라 크게 달라진다. 락 상태 전이 메커니즘을 이해하지 못하면 불필요하게 `ReentrantLock`으로 교체하거나, 반대로 경합이 심한 상황에서 `synchronized`를 그대로 두는 실수를 저지른다. 면접에서 JVM 최적화를 물을 때 이 주제는 거의 빠지지 않는다.

### 답변

HotSpot JVM은 `synchronized`의 성능을 위해 객체 헤더의 Mark Word를 활용해 세 가지 락 상태를 관리한다.

**편향 락(Biased Locking)**: 특정 스레드가 락을 독점적으로 사용하는 경우, Mark Word에 해당 스레드 ID를 기록해 이후 락 획득 시 CAS 연산 없이 스레드 ID만 비교한다. 경합이 전혀 없는 단일 스레드 접근 패턴에서 비용이 거의 0에 가깝다. 단, 다른 스레드가 접근하면 Safe Point에서 편향 취소(revocation)가 발생하며, 이 과정이 STW(Stop-The-World)를 유발한다. Java 15에서 deprecated, Java 21에서 제거됐다.

**경량 락(Lightweight Lock)**: 두 스레드가 락을 번갈아 사용하는 저경합 상황. CAS로 Mark Word를 Lock Record 주소로 교체해 락을 획득한다. 실패하면 스핀(spin)을 수행한다.

**중량 락(Heavyweight Lock / Inflated Lock)**: 스핀 실패 또는 다수 스레드 경합 시 OS 뮤텍스로 전환. 스레드가 커널 모드로 전환되므로 컨텍스트 스위칭 비용이 발생한다.

```java
// 실무 패턴: 경합이 예상되는 경우 ReentrantLock의 tryLock으로 비차단 시도
ReentrantLock lock = new ReentrantLock();
if (lock.tryLock(100, TimeUnit.MILLISECONDS)) {
    try { /* 임계 구역 */ }
    finally { lock.unlock(); }
} else {
    // 락 획득 실패 처리 (중량 락 전이 회피)
}
```

Java 21에서 편향 락이 제거된 이유는 Virtual Thread 환경에서 편향 취소 STW가 오히려 독이 되기 때문이다. 현대 JVM에서는 경량 락과 중량 락만 존재하며, 경합이 적다면 경량 락의 CAS 비용은 무시할 수준이다.

---

## Q2. 락 제거(Lock Elimination)와 락 조대화(Lock Coarsening)가 실무에 미치는 영향은 무엇인가?

### 왜 이 질문이 중요한가
JIT 컴파일러가 자동으로 수행하는 락 최적화를 모르면, 성능 측정 시 예상과 다른 결과에 당황하거나, 반대로 JIT가 기대한 최적화를 수행하지 않는 상황에서 원인을 찾지 못한다. 특히 `StringBuffer`를 `StringBuilder`로 교체하라는 조언의 근거를 제대로 이해할 수 있다.

### 답변

**락 제거(Lock Elimination)**는 탈출 분석(Escape Analysis)의 결과로 적용된다. 동기화 객체가 단일 스레드에서만 접근됨이 증명되면, JIT가 `synchronized` 블록 전체를 제거한다.

```java
// StringBuffer는 모든 메서드가 synchronized이지만
public String buildMessage(String name) {
    StringBuffer sb = new StringBuffer();  // 지역 변수 → 탈출하지 않음
    sb.append("Hello, ");
    sb.append(name);
    return sb.toString();
    // JIT: sb는 이 메서드 밖으로 나가지 않으므로 모든 synchronized 제거
    // → 성능상 StringBuilder와 동일해짐
}
```

**락 조대화(Lock Coarsening)**는 루프나 연속된 코드에서 같은 객체에 대한 반복적인 락 획득/해제를 하나의 큰 락으로 통합하는 최적화다.

```java
// 최적화 전: 매 반복마다 락 획득/해제
for (int i = 0; i < 100; i++) {
    synchronized (list) { list.add(i); }
}

// JIT 최적화 후 (개념적 변환):
synchronized (list) {
    for (int i = 0; i < 100; i++) { list.add(i); }
}
```

실무 함정은 두 가지다. 첫째, 락 조대화가 루프를 통합하면 락 보유 시간이 길어져 다른 스레드의 대기 시간이 늘어날 수 있다. JIT가 이 최적화를 적용했는지 여부는 `-XX:+PrintOptimization`으로 확인해야 한다. 둘째, JMH 벤치마크에서 락 제거가 의도치 않게 적용되면 "synchronized가 비용 없음"이라는 잘못된 결론이 나온다. 반드시 객체를 필드로 두거나 `-XX:-DoEscapeAnalysis`로 탈출 분석을 비활성화해 측정해야 한다.
