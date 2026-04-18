# Java Fundamentals

> Java 언어 기본, 타입 시스템, 컬렉션 프레임워크를 다루는 토픽

## 챕터 목록

| # | 챕터 | 핵심 주제 |
|---|------|----------|
| 01 | 객체 생성과 파괴 | 정적 팩토리, 빌더, 싱글톤, DI |
| 02 | java.lang과 Object | equals/hashCode, 다형성, 래퍼 클래스 |
| 03 | 유틸리티 API | Math, Random, ThreadLocalRandom, Objects |
| 04 | 리플렉션 | Class, Method, Field, 모듈 시스템 |
| 05 | 날짜와 시간 | LocalDateTime, ZonedDateTime, Instant, DST |
| 06 | 클래스와 인터페이스 | 상속 vs 합성, default 메서드, 추상 클래스 |
| 07 | 불변 객체와 Record | final, 깊은 불변성, Java 16 Record |
| 08 | String | String Pool, StringBuilder, 컴파일러 최적화 |
| 09 | Sealed Class | Sealed 계층, Pattern Matching, Visitor 대체 |
| 10 | Enum | 상수별 구현, ordinal 함정, EnumMap/EnumSet |
| 11 | 예외 처리 | 체크/언체크, Spring 예외 전략, 도메인 예외 |
| 12 | 제네릭 | 타입 소거, 와일드카드, PECS |
| 13 | ArrayList | 내부 구조, ArrayList vs LinkedList, SequencedCollection |
| 14 | HashSet / HashMap | 버킷 구조, 트리화, hashCode 품질 |
| 15 | Set과 Map 심화 | ConcurrentHashMap, EnumSet 비트 벡터, TreeMap |
| 16 | 컬렉션 정렬 | TimSort, Comparable vs Comparator |

## 학습 순서

```
1~5  (Core)        → 언어 기본기: 객체 생성, Object 계약, 날짜, 리플렉션
6~12 (TypeSystem)  → 타입 설계: 상속/합성, 불변성, 제네릭, 예외
13~16 (Collections) → 컬렉션: 내부 구현, 성능, 정렬
```

각 챕터 디렉토리 구조:
```
learning/{챕터}/
├── README.md        # 학습 내용 정리 (있는 경우)
└── INVESTIGATE.md   # 심화 질문 2~3개 (면접/실무 관점)
```

## practice/

TODO: Java 21 기반 실습 프로젝트 (추후 구성)
