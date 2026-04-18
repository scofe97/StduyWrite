# 15. 제네릭 및 samber/lo

Go 1.18+의 제네릭과 함수형 프로그래밍 스타일 유틸리티를 학습합니다.

## 학습 목표

- 제네릭 함수 및 타입 정의
- 타입 제약 (Type Constraints)
- samber/lo를 활용한 함수형 유틸리티
- 컬렉션 처리 패턴

## 주요 라이브러리

### samber/lo
```bash
go get github.com/samber/lo
```

Lodash 스타일의 Go 유틸리티:
- Map, Filter, Reduce
- Find, GroupBy, Uniq
- Chunk, Flatten
- 제네릭 기반 타입 안전성

## 주요 개념

### 제네릭 기본
```go
// 제네릭 함수
func Max[T constraints.Ordered](a, b T) T {
    if a > b {
        return a
    }
    return b
}

// 제네릭 타입
type Stack[T any] struct {
    items []T
}
```

### 타입 제약
- `any`: 모든 타입
- `comparable`: 비교 가능한 타입 (==, !=)
- `constraints.Ordered`: 순서 비교 가능 (<, >, <=, >=)
- 커스텀 인터페이스 제약

## 프로젝트 구조

```
15-generics/
├── README.md
├── EXERCISES.md
├── HINTS.md
├── LEARNED.md
├── go.mod
├── main.go
├── collections/
│   ├── stack.go         # 제네릭 스택
│   ├── queue.go         # 제네릭 큐
│   └── set.go           # 제네릭 Set
└── examples/
    ├── lo_examples.go   # samber/lo 예제
    └── utils.go         # 커스텀 유틸리티
```

## 학습 순서

1. 제네릭 함수 정의 및 사용
2. 제네릭 데이터 구조 구현 (Stack, Queue, Set)
3. 타입 제약 활용
4. samber/lo의 Map, Filter, Reduce
5. 실전 예제: 데이터 변환 파이프라인

## 참조 자료

### 📚 Learning Go, 2nd Edition 참조
- **08_Generics.md**: ⭐ 핵심 참조 - 제네릭 함수, 타입, 타입 제약 조건
- **07_Types_Methods_and_Interfaces.md**: 인터페이스와 제네릭 제약 조건 관계
- **04_Composite_Types.md**: 슬라이스, 맵 → 제네릭 컬렉션 기반

## 다음 단계

다음 모듈 [16-context](../16-context/)에서 context 패키지를 학습합니다.
