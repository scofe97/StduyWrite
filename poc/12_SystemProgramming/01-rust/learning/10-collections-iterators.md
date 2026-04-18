# 10. 컬렉션과 이터레이터

Rust의 컬렉션(Vec, HashMap, HashSet)과 Iterator 트레이트를 학습합니다. Iterator는 지연 평가(lazy evaluation)로 효율적인 데이터 변환을 제공하며, map/filter/fold 체이닝으로 선언적 코드를 작성할 수 있습니다. Java Stream과 유사하지만 소유권 시스템과 결합된 Rust의 독특한 패턴을 이해합니다.

## 목표

- [ ] Vec<T>, HashMap<K,V>, HashSet<T> 활용하기
- [ ] Iterator 트레이트와 지연 평가 이해하기
- [ ] iter()/into_iter()/iter_mut()의 차이 설명하기
- [ ] map/filter/fold 체이닝으로 데이터 변환하기
- [ ] collect()의 타입 추론 메커니즘 이해하기

---

## 1. Vec<T> 벡터

## 2. HashMap<K,V> 해시맵

## 3. HashSet<T> 해시셋

## 4. Iterator 트레이트

## 5. iter() vs into_iter() vs iter_mut()

## 6. map/filter/fold 체이닝

## 7. collect()와 타입 추론

## 8. 지연 평가(Lazy Evaluation)

---

## 명령어 요약

| 개념 | 설명 |
|------|------|
| `Vec<T>` | 동적 배열 (가변 크기) |
| `HashMap<K,V>` | 키-값 저장소 |
| `HashSet<T>` | 중복 없는 집합 |
| `iter()` | 불변 참조 이터레이터 |
| `into_iter()` | 소유권 이동 이터레이터 |
| `iter_mut()` | 가변 참조 이터레이터 |
| `map()/filter()/fold()` | 이터레이터 어댑터 |
| `collect()` | 이터레이터 → 컬렉션 변환 |

---

## 체크포인트

- [ ] Java Stream과 Rust Iterator의 차이는?
- [ ] iter() vs into_iter() vs iter_mut()의 선택 기준은?
- [ ] collect()가 다양한 컬렉션으로 변환 가능한 이유는?
- [ ] 지연 평가가 성능에 미치는 영향은?
- [ ] HashMap의 키가 Eq + Hash 트레이트를 구현해야 하는 이유는?
