# HashSet / HashMap: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. HashMap 트리화 임계값이 8인 이유

### 왜 이 질문이 중요한가
HashMap은 Java 8에서 버킷 내 연결 리스트가 일정 길이를 초과하면 레드-블랙 트리로 변환하는 최적화가 추가됐다. 임계값이 왜 8인지 알면 HashMap의 충돌 확률 모델을 이해할 수 있다. 면접에서는 이를 통해 자료구조 설계의 수학적 근거를 이해하는지 확인한다.

### 답변

HashMap의 버킷당 원소 수는 이상적인 해시 함수에서 포아송 분포를 따른다. 부하율(load factor) 0.75 기준으로 버킷 길이가 k일 확률은 `e^(-0.5) * 0.5^k / k!`로 계산된다. 이를 계산하면 길이 8의 확률은 약 0.00000006(6천만분의 1)이다. 즉 정상적인 해시 함수에서는 버킷 길이가 8에 도달할 일이 거의 없다.

길이 8이 된다는 것은 해시 충돌이 비정상적으로 많이 발생하고 있다는 신호다. 이때 트리로 변환하면 최악의 경우 탐색이 O(n)에서 O(log n)으로 개선된다.

```
버킷 길이별 발생 확률 (부하율 0.75 기준, HashMap 소스 코드 주석 발췌):
길이 0: 0.60653066
길이 1: 0.30326533
길이 2: 0.07581633
길이 3: 0.01263606
길이 4: 0.00157952
길이 5: 0.00015795
길이 6: 0.00001316
길이 7: 0.00000094
길이 8: 0.00000006  ← 이 시점에 트리화
```

임계값을 더 낮게 설정하지 않은 이유는 트리 노드(`TreeNode`)가 일반 노드(`Node`)보다 메모리를 약 2배 더 사용하기 때문이다. 충돌이 적은 정상 상황에서는 트리 오버헤드가 손해이므로, 통계적으로 거의 발생하지 않는 수준인 8을 임계값으로 설정했다.

반대로 트리를 다시 연결 리스트로 되돌리는 언트리화(untreeify) 임계값은 6이다. 8과 2의 차이를 두어 원소가 8~6 사이를 계속 오가는 경우 트리/리스트 변환이 반복되는 것을 방지한다(히스테리시스).

```java
// HashMap 내부 상수 (JDK 소스)
static final int TREEIFY_THRESHOLD = 8;    // 트리화 임계값
static final int UNTREEIFY_THRESHOLD = 6;  // 언트리화 임계값
static final int MIN_TREEIFY_CAPACITY = 64; // 트리화 최소 전체 용량
// 전체 용량이 64 미만이면 트리화 대신 resize를 먼저 시도
```

---

## Q2. hashCode 충돌이 성능에 미치는 영향 측정법

### 왜 이 질문이 중요한가
hashCode 구현 품질이 HashMap 성능에 직접적인 영향을 미친다는 것을 알지만, 실제로 얼마나 차이가 나는지, 어떻게 측정하는지 모르면 문제를 사전에 발견하거나 원인을 진단하기 어렵다. "hashCode가 나쁘면 느리다"가 아니라 구체적으로 어떤 패턴이 문제인지 알아야 한다.

### 답변

hashCode 충돌의 영향은 크게 두 가지 패턴으로 나타난다. 첫째, 모든 객체가 같은 hashCode를 반환하는 최악의 경우다. `@Override public int hashCode() { return 42; }` 처럼 상수를 반환하면 HashMap이 단일 버킷에 모든 원소를 넣는다. Java 8 이후엔 트리화되어 O(log n)이지만 그래도 O(1)보다는 훨씬 느리다.

```java
// 나쁜 hashCode 예시와 영향
class BadKey {
    int value;
    @Override public int hashCode() { return 42; } // 모든 키가 같은 버킷
    @Override public boolean equals(Object o) { ... }
}

// 10만 개 삽입 성능 (개념적 비교)
// 좋은 hashCode: ~O(1) per op → 전체 ~ms
// 상수 hashCode: O(log n) per op (트리화 후) → 수십ms 이상 차이

// hashCode 분포 확인 방법
Map<Integer, Long> distribution = entries.stream()
    .collect(Collectors.groupingBy(
        e -> e.hashCode() & (capacity - 1), // 실제 버킷 인덱스
        Collectors.counting()
    ));
long maxBucketSize = distribution.values().stream().mapToLong(Long::longValue).max().orElse(0);
// maxBucketSize가 크면 충돌이 심한 것
```

실무에서 hashCode 품질을 측정하는 방법은 세 가지다. 첫째, JMH 벤치마크다. 실제 키 데이터로 `HashMap.get()`/`put()` 처리량을 측정하고 이론적 O(1) 성능과 비교한다. 둘째, 버킷 분포 분석이다. 위 코드처럼 각 버킷의 원소 수를 집계해서 최대 버킷 크기와 표준편차를 확인한다. 이상적인 분포는 원소 수/버킷 수에 가까워야 한다. 셋째, HashMap의 `treeifyBin()` 호출 횟수를 APM이나 커스텀 계측으로 추적한다. 트리화가 자주 일어난다면 hashCode 품질 문제다.

좋은 hashCode의 조건은 두 가지다. 두 객체가 논리적으로 다르면 되도록 다른 해시값을 반환해야 하고, 계산이 빠르고 결정론적이어야 한다. `Objects.hash(field1, field2, ...)`를 사용하거나, Lombok `@EqualsAndHashCode`, Record의 자동 생성을 활용하면 이 조건을 쉽게 충족할 수 있다.
