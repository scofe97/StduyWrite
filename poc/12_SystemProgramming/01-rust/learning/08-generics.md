# 08. 제네릭과 타입 시스템

Rust의 제네릭은 단형화(Monomorphization)를 통해 컴파일 타임에 구체적인 타입으로 변환되어 런타임 오버헤드가 없습니다. where절로 복잡한 트레이트 바운드를 표현하고, 연관 타입으로 트레이트와 타입의 관계를 명확히 할 수 있습니다. Java의 타입 소거와 대비되는 Rust 제네릭의 강점을 이해합니다.

## 목표

- [ ] 제네릭 함수와 구조체 작성하기
- [ ] where절로 복잡한 트레이트 바운드 표현하기
- [ ] 연관 타입과 제네릭 파라미터의 차이 설명하기
- [ ] 단형화의 성능 장점과 트레이드오프 이해하기
- [ ] PhantomData와 타입 별칭 활용하기

---

## 1. 제네릭 함수

## 2. 제네릭 구조체와 열거형

## 3. where절 활용

## 4. 연관 타입(Associated Types)

## 5. PhantomData

## 6. 단형화(Monomorphization)

## 7. 타입 별칭(Type Aliases)

---

## 명령어 요약

| 개념 | 설명 |
|------|------|
| `fn func<T>(x: T)` | 제네릭 함수 |
| `struct Name<T> { field: T }` | 제네릭 구조체 |
| `where T: Trait + Other` | where절 트레이트 바운드 |
| `type Item = Type;` | 연관 타입 |
| `PhantomData<T>` | 컴파일 타임 타입 정보 보존 |
| `type Alias = ComplexType;` | 타입 별칭 |
| Monomorphization | 컴파일 타임 타입 특수화 |

---

## 체크포인트

- [ ] Java 제네릭(타입 소거)과 Rust 제네릭(단형화)의 차이는?
- [ ] 연관 타입은 언제 사용하고 제네릭 파라미터와 어떻게 다른가?
- [ ] PhantomData의 용도는 무엇인가?
- [ ] where절이 함수 시그니처의 가독성을 어떻게 개선하는가?
- [ ] 단형화가 컴파일 시간과 바이너리 크기에 미치는 영향은?
