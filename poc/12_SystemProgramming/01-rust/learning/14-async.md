# 14. 비동기(Async/Await)

Rust의 async/await는 Future 트레이트를 기반으로 zero-cost 추상화를 제공합니다. Java의 CompletableFuture와 달리 지연 평가(lazy evaluation)되며, tokio 같은 런타임이 실제 실행을 담당합니다. Pin 타입은 self-referential 구조체의 메모리 안전성을 보장하고, select! 매크로로 동시 태스크를 조율합니다.

## 목표
- [ ] Future 트레이트와 지연 평가 이해
- [ ] async fn과 .await 기본 사용
- [ ] tokio 런타임 구성과 설정
- [ ] tokio::spawn으로 동시 태스크 실행
- [ ] select! 매크로로 여러 Future 조합
- [ ] 비동기 스트림(Stream 트레이트) 처리
- [ ] Pin의 필요성과 동작 원리 이해

## 1. Future 트레이트

## 2. async fn

## 3. .await

## 4. tokio 런타임

## 5. spawn

## 6. select!

## 7. 비동기 스트림

## 8. Pin

## 명령어 요약
| 개념 | 설명 |
|------|------|
| `async fn` | 비동기 함수, Future 반환 |
| `.await` | Future 평가, 실행 양보 |
| `tokio::main` | 비동기 런타임 진입점 |
| `tokio::spawn` | 새 비동기 태스크 생성 |
| `tokio::select!` | 여러 Future 중 먼저 완료된 것 선택 |
| `Stream` | 비동기 이터레이터 |
| `Pin<T>` | 메모리 위치 고정 |

## 체크포인트
- Java CompletableFuture vs Rust Future의 근본적인 차이는?
- tokio::spawn vs std::thread::spawn의 차이는?
- Pin이 필요한 이유는 무엇인가?
- Future가 지연 평가되는 것의 장단점은?
- async 블록이 move를 요구하는 상황은?
- select! 매크로의 동작 원리는?
- async Rust가 zero-cost abstractions를 달성하는 방법은?
