# Java Concurrency

> 스레드 기초부터 Virtual Threads, Structured Concurrency까지 동시성 프로그래밍을 다루는 토픽

## 챕터 목록

| # | 챕터 | 핵심 주제 |
|---|------|----------|
| 01 | 스레드 생성과 생명주기 | Thread, Runnable, Callable, 상태 전이 |
| 02 | 메모리 가시성과 동기화 | volatile, synchronized, 데드락 |
| 03 | 생산자-소비자 패턴 | wait/notify, ReentrantLock, Condition, BlockingQueue |
| 04 | 원자 연산과 동시성 컬렉션 | CAS, Atomic, ConcurrentHashMap, LongAdder |
| 05 | Executor 프레임워크 | 스레드 풀, Future, CompletableFuture |
| 06 | ThreadLocal과 동시성 라이브러리 | ThreadLocal, ScopedValue, CountDownLatch, Semaphore |
| 07 | Java Memory Model 심화 | happens-before, 메모리 펜스, DCL |
| 08 | Virtual Threads 기초 | Carrier Thread, Mount/Unmount, 벤치마크 |
| 09 | Virtual Threads Pinning | Pinning 감지, synchronized→ReentrantLock |
| 10 | Structured Concurrency | StructuredTaskScope, ScopedValue (Preview) |

## 학습 순서

01~03 (스레드 기초) → 04~06 (고급 동시성) → 07 (JMM 심화) → 08~10 (Virtual Threads)

## practice/

TODO: 동시성 실습 프로젝트 (추후 구성)
