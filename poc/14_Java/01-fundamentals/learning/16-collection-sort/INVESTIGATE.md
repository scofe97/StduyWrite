# 컬렉션 정렬: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. TimSort 알고리즘의 핵심 아이디어

### 왜 이 질문이 중요한가
Java의 `Arrays.sort(Object[])`와 `Collections.sort()`는 TimSort를 사용한다. "안정 정렬이고 최선 O(n), 최악 O(n log n)"이라는 답변은 불완전하다. 실제 데이터에서 왜 빠른지, 어떤 입력에 최적화되어 있는지 이해하면 정렬 성능을 예측하고 활용할 수 있다.

### 답변

TimSort는 Tim Peters가 Python을 위해 2002년에 고안하고 Java 7에 도입된 알고리즘이다. 핵심 아이디어는 실제 데이터에는 이미 부분적으로 정렬된 구간(run)이 많다는 관찰에서 출발한다.

TimSort의 동작 원리는 두 단계다. 첫째, 입력 배열을 스캔하며 자연적으로 오름차순이나 내림차순으로 이어진 구간(run)을 찾는다. 내림차순 run은 뒤집어 오름차순으로 만든다. 각 run의 최소 길이(minrun, 보통 32~64)보다 짧으면 이진 삽입 정렬로 확장한다. 둘째, 스택에 쌓인 run들을 merge한다. 단, 인접한 run들의 길이 비율이 일정 조건을 만족할 때만 병합하여 균형 잡힌 merge 트리를 유지한다.

```
입력: [3,1,4,1,5, 9,2,6,5,3, 7,8,2,8,4]
       ← run1 →  ← run2 →  ← run3 →

실제 데이터 예시:
- 로그 파일: 대부분 타임스탬프 순 → 이미 정렬된 긴 run들
- DB 결과: 인덱스로 부분 정렬된 레코드들
- UI 목록 재정렬: 이전 정렬 상태가 부분 보존됨

이런 데이터에서 TimSort는 이미 정렬된 구간을 재정렬하지 않으므로
완전 무작위 데이터보다 훨씬 적은 비교 횟수로 정렬 완료
```

안정 정렬이라는 특성도 중요하다. 같은 키를 가진 원소들의 원래 순서가 보존된다. "이름으로 정렬된 목록을 다시 부서로 정렬하면 부서 내에서는 이름 순서가 유지된다"는 보장이 가능하다.

기본 타입 배열(`int[]`, `long[]` 등)에 대한 `Arrays.sort()`는 안정 정렬이 필요 없으므로 DualPivot QuickSort를 사용한다. 객체 배열에만 TimSort가 적용된다.

---

## Q2. Comparable vs Comparator, 어떤 것을 언제 구현해야 하는가?

### 왜 이 질문이 중요한가
`Comparable`과 `Comparator`의 문법적 차이는 쉽게 알 수 있지만, "이 클래스에 자연 순서가 있는가"라는 설계 질문에 답하지 못하면 잘못된 선택을 하게 된다. 특히 실무에서는 다양한 정렬 기준이 필요한 경우가 대부분이라 두 인터페이스의 역할 분리를 명확히 이해해야 한다.

### 답변

`Comparable<T>`은 클래스 자체에 "자연 순서(natural ordering)"가 있을 때 구현한다. `int compareTo(T other)`를 구현하며 "이 객체가 other보다 작으면 음수, 같으면 0, 크면 양수"를 반환한다. `Integer`, `String`, `LocalDate` 등 JDK 내장 타입들이 모두 `Comparable`을 구현한다.

자연 순서가 있다는 것은 "이 타입의 인스턴스들을 비교할 때 가장 자명하고 보편적인 기준이 하나 존재한다"는 의미다. 금액은 크기 순, 날짜는 시간 순, 문자열은 사전 순이 자연 순서다.

```java
// Comparable — 자연 순서가 명확한 경우
class Money implements Comparable<Money> {
    private final BigDecimal amount;
    private final Currency currency;

    @Override
    public int compareTo(Money other) {
        // 같은 통화 내에서만 비교 가능 — 다른 통화면 예외
        if (!currency.equals(other.currency))
            throw new IllegalArgumentException("Cannot compare different currencies");
        return amount.compareTo(other.amount);
    }
}

// 자연 순서 활용
List<Money> prices = ...;
Collections.sort(prices); // Comparable 사용
TreeSet<Money> priceSet = new TreeSet<>(prices); // TreeSet도 Comparable 사용
```

`Comparator<T>`는 두 가지 상황에서 쓴다. 첫째, 자연 순서 외의 다른 정렬 기준이 필요할 때다. `Employee`를 이름순, 연봉순, 입사일순으로 각각 정렬하려면 각 기준마다 `Comparator`가 필요하다. 둘째, `Comparable`을 구현하지 않은 외부 클래스를 정렬해야 할 때다.

```java
// Comparator — 다양한 정렬 기준
class Employee {
    String name;
    int salary;
    LocalDate hireDate;
}

// 명시적 Comparator 정의 (Java 8+ 메서드 참조 + 체이닝)
Comparator<Employee> bySalaryThenName = Comparator
    .comparingInt(Employee::getSalary).reversed()  // 연봉 내림차순
    .thenComparing(Employee::getName);              // 같은 연봉이면 이름순

List<Employee> employees = ...;
employees.sort(bySalaryThenName);

// 여러 기준 재사용
employees.sort(Comparator.comparing(Employee::getHireDate)); // 입사일순
employees.sort(Comparator.comparing(Employee::getName,
    Collator.getInstance(Locale.KOREA))); // 한국어 사전순
```

`compareTo`와 `equals`의 일관성도 중요하다. `a.compareTo(b) == 0`이면 `a.equals(b) == true`여야 한다는 계약이 있다. 이를 어기면 `TreeSet`에 원소를 넣을 때 `equals`로는 같다고 판단하지만 `compareTo`로는 다르게 판단해서 중복 원소가 삽입될 수 있다. `BigDecimal("1.0")`과 `BigDecimal("1.00")`이 `equals`는 false이지만 `compareTo`는 0인 것이 이 계약을 어기는 유명한 예다.
