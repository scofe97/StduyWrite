# 13. 동시성(Concurrency)

Rust는 소유권 시스템과 타입 시스템으로 데이터 레이스를 컴파일 타임에 방지합니다. Send와 Sync 마커 트레이트로 스레드 간 데이터 전송과 공유를 안전하게 제어하며, Mutex와 Arc 조합으로 공유 상태를, mpsc 채널로 메시지 패싱을 구현합니다. Java의 synchronized와 달리 타입 수준에서 안전성을 보장합니다.

## 목표
- [ ] std::thread로 스레드 생성 및 join
- [ ] move 클로저와 스레드 간 소유권 이동 이해
- [ ] Mutex<T>로 공유 상태 보호
- [ ] Arc<Mutex<T>>로 멀티 스레드 공유 데이터 구현
- [ ] mpsc 채널로 메시지 패싱
- [ ] Send/Sync 마커 트레이트의 역할 설명

## 1. std::thread

## 2. move 클로저와 스레드

## 3. Mutex<T>

## 4. Arc<Mutex<T>>

## 5. mpsc 채널

## 6. Send/Sync 트레이트

## 7. 데이터 레이스 컴파일 방지

## 명령어 요약
| 개념 | 설명 |
|------|------|
| `std::thread::spawn` | 새 스레드 생성 |
| `join()` | 스레드 종료 대기 |
| `Mutex<T>` | 상호 배제 잠금 |
| `Arc<T>` | 멀티 스레드 참조 카운팅 |
| `mpsc::channel()` | Multiple Producer Single Consumer 채널 |
| `Send` | 스레드 간 소유권 이동 가능 |
| `Sync` | 스레드 간 참조 공유 가능 |

## 체크포인트
- Rust가 데이터 레이스를 컴파일 타임에 방지하는 원리는?
- Java synchronized vs Rust Mutex의 차이는?
- mpsc에서 여러 producer가 가능한 이유는?
- Send와 Sync의 차이는 무엇인가?
- `Arc<Mutex<T>>` 대신 `Rc<RefCell<T>>`를 쓸 수 없는 이유는?
- 채널 방식(메시지 패싱)과 공유 메모리 방식의 트레이드오프는?
