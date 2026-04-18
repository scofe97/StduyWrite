# 컴파일과 최적화: Deep Investigation
> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. JIT C1/C2 계층 컴파일이 실무에 미치는 영향은 무엇인가?

### 왜 이 질문이 중요한가
"JVM은 처음에 느리다"는 현상, 즉 워밍업(warm-up) 문제는 실제 프로덕션에서 배포 직후 레이턴시 급등, 카나리 배포 중 트래픽 전환 실패, 서버리스 콜드스타트 성능 저하로 직결된다. C1/C2 계층 구조를 이해하면 이 문제를 예측하고 완화할 수 있다.

### 답변

HotSpot JVM은 Tiered Compilation(계층적 컴파일, Java 7u40+ 기본 활성화)을 사용해 5단계로 코드를 처리한다.

| 계층 | 실행 방식 | 특징 |
|------|----------|------|
| 0 | 인터프리터 | 프로파일링 수집 시작 |
| 1 | C1 (단순) | 빠른 컴파일, 최적화 최소 |
| 2 | C1 (제한 프로파일링) | |
| 3 | C1 (전체 프로파일링) | 호출 횟수, 타입 정보 수집 |
| 4 | C2 | 느리지만 최대 최적화 |

C1은 빠르게 컴파일해 인터프리터보다 빠른 코드를 즉시 제공하고, C2는 충분한 프로파일링 데이터(기본 임계값: 메서드 호출 10,000회 또는 루프 반복 10,000회)가 쌓이면 고도로 최적화된 네이티브 코드를 생성한다.

```bash
# JIT 컴파일 로그 확인
java -XX:+PrintCompilation -XX:+UnlockDiagnosticVMOptions MyApp

# 출력 예시:
#  854    3       3  java.lang.String::hashCode (55 bytes)  ← C1 계층 3
# 1203    4       4  java.lang.String::hashCode (55 bytes)  ← C2
# 1203    3       3  java.lang.String::hashCode (55 bytes) made not entrant ← C1 폐기
```

실무 영향은 세 가지다. 첫째, **배포 후 워밍업 기간** 동안 트래픽을 점진적으로 전환해야 한다. Spring Boot Actuator의 readiness probe를 배포 후 즉시 활성화하면 워밍업이 안 된 인스턴스가 프로덕션 트래픽을 받아 타임아웃이 발생한다. 둘째, **GraalVM AOT(Ahead-of-Time) 컴파일**은 JIT 워밍업을 제거하지만 프로파일링 기반 최적화를 포기한다. 서버리스나 CLI 도구에는 AOT가 유리하고, 장시간 실행 서버에는 JIT가 유리하다. 셋째, `-client` vs `-server` 플래그는 구버전 JVM에서 C1 전용 vs C2 포함 여부를 결정했으나, 현대 JVM에서는 Tiered Compilation이 둘을 자동으로 조합한다.

---

## Q2. 탈출 분석(Escape Analysis)이 메모리 할당을 줄이는 원리는 무엇인가?

### 왜 이 질문이 중요한가
GC 튜닝 전에 먼저 할당 자체를 줄이는 것이 더 근본적인 최적화다. 탈출 분석은 JVM이 자동으로 수행하는 할당 제거 최적화로, 이를 이해하면 GC 로그에서 보이는 Young GC 빈도를 줄이는 코드 패턴을 의도적으로 작성할 수 있다.

### 답변

탈출 분석은 C2 컴파일러가 객체의 참조가 메서드 경계 밖으로 "탈출"하는지 분석하는 기술이다. 탈출하지 않는 객체는 힙 대신 스택에 할당하거나(스택 할당), 아예 객체 자체를 제거하고 필드를 스칼라 변수로 대체(스칼라 교체)할 수 있다.

```java
// 이 메서드에서 Point 객체는 메서드 밖으로 탈출하지 않음
public double distanceFromOrigin(double x, double y) {
    Point p = new Point(x, y);  // 힙 할당 예상
    return Math.sqrt(p.x * p.x + p.y * p.y);
    // C2: p는 탈출하지 않음 → p.x, p.y를 지역 변수로 교체 → 힙 할당 없음
}

// 탈출하는 경우: 힙 할당 필수
public Point createPoint(double x, double y) {
    return new Point(x, y);  // 반환값이므로 탈출
}
```

탈출 분석이 활성화되면 **락 제거(lock elision)**도 가능해진다. `synchronized` 블록 내의 객체가 단일 스레드에서만 접근됨이 증명되면 락 획득/해제 비용 자체를 제거한다. `StringBuffer` 같은 thread-safe 클래스를 지역 변수로만 쓸 때 이 최적화가 적용된다.

```bash
# 탈출 분석 활성화 확인 (Java 8+에서 기본 활성화)
java -XX:+DoEscapeAnalysis -XX:+PrintEscapeAnalysis MyApp
# 비활성화하여 차이 측정
java -XX:-DoEscapeAnalysis MyApp
```

주의할 점은 탈출 분석이 항상 작동하지는 않는다는 것이다. 메서드가 너무 크거나, 인터페이스를 통해 호출되어 타입 정보가 불충분하거나, 배열이 포함된 경우 분석이 실패한다. JMH 벤치마크에서 의도치 않게 탈출 분석이 적용되어 "할당 없음"으로 최적화되면 현실과 동떨어진 측정 결과가 나올 수 있으므로, `-XX:-DoEscapeAnalysis`로 비교 측정하는 습관이 필요하다.
