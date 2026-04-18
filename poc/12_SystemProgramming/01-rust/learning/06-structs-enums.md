# 06. 구조체와 열거형

Rust의 타입 시스템 핵심인 struct와 enum을 학습합니다. struct는 관련 데이터를 묶고 메서드를 정의하며, enum은 여러 가능한 값 중 하나를 표현합니다. Java의 class/enum과 다르게 Rust enum은 대수적 데이터 타입(ADT)으로 각 variant에 데이터를 담을 수 있어 매우 강력합니다.

## 목표

- [ ] struct 정의하고 impl 블록으로 메서드 구현하기
- [ ] enum으로 대수적 데이터 타입 구현하기
- [ ] Option<T>과 Result<T,E>의 활용 패턴 익히기
- [ ] match와 if let으로 패턴 매칭 수행하기
- [ ] match의 완전성 검사(exhaustiveness check) 이해하기

---

## 1. 구조체(Struct) 정의

## 2. impl 블록과 메서드

## 3. 연관 함수(Associated Functions)

## 4. 열거형(Enum) 정의

## 5. Enum에 데이터 담기

## 6. Option<T>으로 Null 안전성

## 7. Result<T,E>로 에러 표현

## 8. match 패턴 매칭

## 9. if let으로 간결한 매칭

---

## 명령어 요약

| 개념 | 설명 |
|------|------|
| `struct Name { field: Type }` | 구조체 정의 |
| `impl Name { fn method(&self) }` | 메서드 구현 |
| `impl Name { fn new() -> Self }` | 연관 함수 (생성자 패턴) |
| `enum Option<T> { Some(T), None }` | 값의 존재/부재 표현 |
| `enum Result<T,E> { Ok(T), Err(E) }` | 성공/실패 결과 표현 |
| `match value { pattern => expr }` | 패턴 매칭 (완전성 검사) |
| `if let Some(v) = opt { ... }` | 단일 패턴 매칭 |

---

## 체크포인트

- [ ] Java enum과 Rust enum의 근본적인 차이는 무엇인가?
- [ ] Option<T>이 null을 대체하는 방식은?
- [ ] match에서 모든 케이스를 처리해야 하는 이유는?
- [ ] impl 블록에서 &self, &mut self, self의 차이는?
- [ ] enum variant에 다른 타입의 데이터를 담을 수 있는가?
