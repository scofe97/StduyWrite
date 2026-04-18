# 07. 트레이트(Traits)

Rust의 트레이트는 타입이 가져야 할 동작을 정의하는 추상화 메커니즘입니다. Java interface와 유사하지만, 기본 구현, 연관 타입, orphan rule 등 독특한 특성을 가집니다. 트레이트 바운드를 통해 제네릭의 타입 제약을 표현하고, 정적/동적 디스패치를 선택할 수 있습니다.

## 목표

- [ ] trait 정의하고 타입에 구현하기
- [ ] 트레이트 바운드로 제네릭 함수 제약하기
- [ ] 정적 디스패치(impl Trait)와 동적 디스패치(dyn Trait) 차이 설명하기
- [ ] 표준 트레이트(Display, Debug, From, Into) 활용하기
- [ ] orphan rule이 코드 구조에 미치는 영향 이해하기

---

## 1. 트레이트 정의

## 2. impl Trait for Type

## 3. 기본 메서드 구현

## 4. 트레이트 바운드

## 5. impl Trait 문법

## 6. 동적 디스패치(dyn Trait)

## 7. 표준 트레이트 활용

---

## 명령어 요약

| 개념 | 설명 |
|------|------|
| `trait Name { fn method(&self); }` | 트레이트 정의 |
| `impl Name for Type { ... }` | 트레이트 구현 |
| `fn func<T: Trait>(x: T)` | 트레이트 바운드 |
| `fn func(x: impl Trait)` | impl Trait 문법 (정적 디스패치) |
| `fn func(x: &dyn Trait)` | 동적 디스패치 (trait object) |
| `#[derive(Debug, Clone)]` | 자동 트레이트 구현 |
| `Display`, `From`, `Into` | 주요 표준 트레이트 |

---

## 체크포인트

- [ ] Java interface와 Rust trait의 주요 차이는?
- [ ] orphan rule이란 무엇이며 왜 필요한가?
- [ ] impl Trait와 dyn Trait의 선택 기준은?
- [ ] 트레이트의 기본 메서드를 오버라이드할 수 있는가?
- [ ] Display와 Debug 트레이트의 용도 차이는?
