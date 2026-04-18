# 09. 에러 처리

Rust는 예외(exception)가 없고 Result<T,E> 타입으로 에러를 명시적으로 처리합니다. panic!은 복구 불가능한 에러에만 사용하며, ? 연산자로 에러를 간결하게 전파할 수 있습니다. From 트레이트를 활용한 에러 변환과 thiserror/anyhow 크레이트로 실전 에러 처리 패턴을 학습합니다.

## 목표

- [ ] panic!과 Result<T,E> 사용 시점 구분하기
- [ ] ? 연산자로 에러 전파하기
- [ ] 커스텀 에러 타입 정의하고 From 트레이트 구현하기
- [ ] thiserror로 라이브러리 에러, anyhow로 애플리케이션 에러 처리하기
- [ ] Java의 checked/unchecked exception과 비교하기

---

## 1. panic! vs Result

## 2. Result<T,E> 활용

## 3. ? 연산자로 에러 전파

## 4. 커스텀 에러 타입

## 5. From 트레이트로 에러 변환

## 6. thiserror 크레이트

## 7. anyhow 크레이트

---

## 명령어 요약

| 개념 | 설명 |
|------|------|
| `panic!("message")` | 복구 불가능한 에러 (스레드 종료) |
| `Result<T, E>` | 복구 가능한 에러 표현 |
| `?` 연산자 | 에러 조기 반환 (early return) |
| `impl From<SourceErr> for MyErr` | 에러 타입 자동 변환 |
| `unwrap()`, `expect()` | Result 강제 언래핑 (panic 가능) |
| `thiserror` | 라이브러리 에러 정의용 |
| `anyhow` | 애플리케이션 에러 처리용 |

---

## 체크포인트

- [ ] Java의 checked/unchecked exception과 Rust의 에러 처리 비교?
- [ ] unwrap()을 프로덕션 코드에서 쓰면 안 되는 이유는?
- [ ] thiserror와 anyhow의 선택 기준은?
- [ ] ? 연산자가 From 트레이트를 활용하는 방식은?
- [ ] panic!이 스레드에만 영향을 미치는 이유는?
