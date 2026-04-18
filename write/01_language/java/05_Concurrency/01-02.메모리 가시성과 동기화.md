# 메모리 가시성과 동기화
---
> 멀티스레드 환경에서 공유 변수의 변경이 다른 스레드에 즉시 보이지 않을 수 있다. `volatile`은 가시성을, `synchronized`는 원자성과 가시성을 함께 보장하며, 두 메커니즘을 올바르게 사용하는 것이 경합 조건과 데드락을 피하는 핵심이다.

## 1. CPU 캐시와 메모리 가시성 문제

현대 CPU는 성능을 위해 메인 메모리의 값을 코어별 캐시(L1/L2)에 복사해 사용한다. 스레드 A가 캐시에서 변수를 수정해도, 스레드 B가 바라보는 캐시에는 이전 값이 남아 있을 수 있다. 이처럼 한 스레드의 변경사항이 다른 스레드에 언제 보일지 보장되지 않는 상황을 *메모리 가시성(memory visibility) 문제*라고 한다.

```java
// 가시성 문제 발생 예
class MyTask implements Runnable {
    boolean flag = true; // 캐시에 저장될 수 있음

    @Override
    public void run() {
        while (flag) { // 메인 스레드의 flag=false 변경을 못 볼 수 있음
            // 작업 수행
        }
    }
}
```

메인 스레드에서 `task.flag = false`를 설정해도 work 스레드가 이를 인식하지 못해 무한 루프에 빠질 수 있다.

## 2. volatile 키워드

`volatile` 변수는 캐시를 거치지 않고 항상 메인 메모리에서 직접 읽고 쓴다. 이를 통해 한 스레드의 쓰기가 다른 스레드에 즉시 가시화된다.

```java
class MyTask implements Runnable {
    volatile boolean flag = true;  // 메인 메모리에서 직접 접근
    volatile long count = 0;

    @Override
    public void run() {
        while (flag) {
            count++;
            if (count % 100_000_000 == 0) {
                System.out.println("count = " + count);
            }
        }
        System.out.println("종료. count = " + count);
    }
}
```

`volatile`은 가시성만 보장하고 원자성(atomicity)은 보장하지 않는다. `count++`처럼 읽기-수정-쓰기가 하나의 연산처럼 보여도 실제로는 세 단계이므로, 두 스레드가 동시에 실행하면 증분 값이 유실될 수 있다. 단순한 플래그(boolean) 용도로는 충분하지만, 카운터나 복합 상태 변경에는 `synchronized` 또는 `Atomic` 클래스를 써야 한다.

## 3. 자바 메모리 모델과 happens-before

자바 메모리 모델(Java Memory Model, JMM)은 멀티스레드 환경에서 메모리 접근 순서를 정의한다. 핵심 개념은 *happens-before* 관계로, 특정 작업이 다른 작업보다 먼저 실행됨을 보장하는 규칙이다.

happens-before가 성립하는 주요 경우는 다음과 같다.

- 같은 스레드 안에서 앞선 코드는 뒤따르는 코드보다 happens-before다.
- `volatile` 변수에 대한 쓰기는 이후의 모든 읽기보다 happens-before다.
- `Thread.start()` 호출은 새 스레드의 모든 작업보다 happens-before다.
- `synchronized` 블록 종료는 이후 같은 락을 획득하는 스레드의 모든 작업보다 happens-before다.
- `Thread.join()` 이후 코드는 해당 스레드의 모든 작업보다 happens-after다.

`volatile`이나 `synchronized`를 올바르게 사용하면 happens-before 관계가 성립하여 메모리 가시성 문제가 해소된다.

## 4. synchronized — 메서드와 블록

`synchronized`는 임계 영역(critical section)에 한 번에 하나의 스레드만 진입하도록 보장한다. 원자성과 메모리 가시성을 동시에 제공한다.

```java
// 메서드 단위 동기화
public class BankAccount {
    private int balance;

    public synchronized boolean withdraw(int amount) {
        if (balance < amount) {
            return false;
        }
        balance -= amount;
        return true;
    }

    public synchronized int getBalance() {
        return balance;
    }
}

// 블록 단위 동기화 (임계 영역을 최소화할 때)
public void method() {
    // 동기화 불필요한 작업...
    synchronized (this) {
        // 임계 영역만 보호
        balance -= amount;
    }
    // 동기화 불필요한 작업...
}
```

임계 영역은 가능한 짧게 유지해야 한다. `synchronized` 메서드 전체를 잠그면 락 경합이 증가해 처리량이 줄어든다.

## 5. 모니터 락

자바의 모든 객체는 내부에 *모니터 락(monitor lock)*을 하나씩 가진다. `synchronized` 블록에 진입하려는 스레드는 해당 객체의 모니터 락을 획득해야 한다.

락 획득에 실패한 스레드는 BLOCKED 상태로 전환되어 락 대기 집합(entry set)에 들어간다. 락을 보유한 스레드가 블록을 벗어나면 락이 해제되고, 대기 중이던 스레드 중 하나가 경쟁을 통해 락을 획득한다. 어떤 스레드가 선택될지는 JVM이 보장하지 않으므로, 특정 순서를 가정한 코드를 작성하면 안 된다.

## 6. 경합 조건

*경합 조건(race condition)*은 두 스레드 이상이 공유 자원에 동시에 접근해 실행 순서에 따라 결과가 달라지는 버그다. 잔고 출금 예제가 대표적이다.

```java
// 경합 조건 발생 예 — synchronized 없음
public boolean withdraw(int amount) {
    if (balance < amount) { // t1과 t2 모두 잔고 충분하다고 판단
        return false;
    }
    // t1과 t2 둘 다 이 시점에 balance를 읽고 각자 차감
    balance -= amount;      // 두 번 차감 → 잔고 음수
    return true;
}
```

t1과 t2가 동시에 잔고 검사를 통과하면 두 번 출금이 발생해 잔고가 음수가 된다. `synchronized`를 추가하면 검사-수정 구간이 원자적으로 보호된다.

## 7. 데드락 발생 조건과 방지

*데드락(deadlock)*은 두 스레드가 서로 상대방이 보유한 락을 기다리며 영원히 진행하지 못하는 상태다. 데드락이 발생하려면 아래 네 조건이 동시에 성립해야 한다.

| 조건 | 설명 |
|------|------|
| 상호 배제 | 자원을 한 번에 하나의 스레드만 사용한다 |
| 점유와 대기 | 락을 보유한 채로 다른 락을 기다린다 |
| 비선점 | 다른 스레드의 락을 강제로 빼앗을 수 없다 |
| 순환 대기 | 스레드 간 락 획득 순서가 원형을 이룬다 |

```java
// 데드락 발생 예
Object lockA = new Object();
Object lockB = new Object();

// 스레드 1: lockA → lockB 순서로 획득
synchronized (lockA) {
    synchronized (lockB) { /* ... */ }
}

// 스레드 2: lockB → lockA 순서로 획득 → 데드락!
synchronized (lockB) {
    synchronized (lockA) { /* ... */ }
}
```

가장 실용적인 방지책은 **락 획득 순서를 전역적으로 통일**하는 것이다. 모든 스레드가 항상 lockA → lockB 순서로 획득하면 순환 대기 조건이 깨져 데드락이 발생하지 않는다. `tryLock(timeout)`으로 일정 시간 내에 락을 얻지 못하면 보유한 락을 놓고 재시도하는 방법도 유효하다.
