# 03_DesignPatterns — 디자인 패턴과 좋은 설계

Java/Spring 백엔드 맥락의 객체지향 설계 학습 카테고리다. 패턴 자체보다 "왜 그 자리에 그 패턴이 필요한가"와 "도입 신호가 어떻게 보이는가"에 무게를 둔다.



## 문서 지도

| 번호 | 제목 | 무엇을 다루는가 |
|------|------|----------------|
| [01-01](01-01.SOLID 원칙.md) | SOLID 원칙 | 클래스·모듈 단위 거시 원칙 5가지 (SRP/OCP/LSP/ISP/DIP) |
| [01-02](01-02.생성 패턴.md) | 생성 패턴 | Factory Method, Abstract Factory, Builder, Singleton, Prototype |
| [01-03](01-03.구조 패턴.md) | 구조 패턴 | Proxy, Decorator, Facade, Adapter + Spring AOP 프록시 |
| [01-04](01-04.행동 패턴.md) | 행동 패턴 | Strategy, Observer, Template Method, Command, State, Iterator, Chain of Responsibility |
| [02-01](02-01.일급객체 사상과 Java 코드 스타일.md) | 일급객체 사상과 Java 코드 스타일 | 일급함수·일급 컬렉션·VO·고차함수 |
| [02-02](02-02.클린 코드 원칙.md) | 클린 코드 원칙 | 코드 줄 단위 미시 규칙 12가지 |
| [02-03](02-03.함수형 패턴 도입의 함정과 경계 설계.md) | 함수형 패턴 도입의 함정과 경계 설계 | Spring 인프라 경계 함정·부수효과 경계·다른 카테고리와의 접점 |

Spring 컨테이너 차원의 디자인 패턴 흡수는 별도 카테고리에 있다.

- [11_spring/01_core/01-02.Spring과 디자인 패턴.md](../../../11_spring/01_core/01-02.Spring과 디자인 패턴.md) — Spring이 내부에 흡수한 GoF 패턴 9가지



## GoF 23 패턴 분류

GoF(Gang of Four) 분류 축은 세 가지다. *생성*은 객체를 어떻게 만드는가, *구조*는 객체를 어떻게 조합하는가, *행동*은 객체 사이에 책임과 통신을 어떻게 나누는가에 답한다. 본 카테고리가 다루는 패턴은 다음 표와 같다.

| 분류 | 본 카테고리 정리 패턴 | 문서 |
|------|----------------------|------|
| 생성(Creational) | Factory Method, Abstract Factory, Builder, Singleton, Prototype | [01-02](01-02.생성 패턴.md) |
| 구조(Structural) | Proxy, Decorator, Facade, Adapter | [01-03](01-03.구조 패턴.md) |
| 행동(Behavioral) | Strategy, Observer, Template Method, Command, State, Iterator, Chain of Responsibility | [01-04](01-04.행동 패턴.md) |



## 영상 7패턴 매핑 (시작 학습자용)

디자인 패턴 입문 영상에서 *반드시 알아야 할 7가지*로 소개되는 패턴들이 본 카테고리 어디에 들어 있는지 표로 정리한다. 패턴별 도입부 한 줄 정의를 본 카테고리에 그대로 반영했다.

| # | 영상 패턴 | 분류 | 위치 |
|---|----------|------|------|
| 1 | Singleton | 생성 | [01-02 §Singleton](01-02.생성 패턴.md#singleton--싱글톤) |
| 2 | Builder | 생성 | [01-02 §Builder](01-02.생성 패턴.md#builder--빌더) |
| 3 | Factory | 생성 | [01-02 §Factory Method](01-02.생성 패턴.md#factory-method--팩토리-메서드) |
| 4 | Facade | 구조 | [01-03 §Facade](01-03.구조 패턴.md#facade--퍼사드) |
| 5 | Adapter | 구조 | [01-03 §Adapter](01-03.구조 패턴.md#adapter--어댑터) |
| 6 | Strategy | 행동 | [01-04 §Strategy](01-04.행동 패턴.md#strategy--전략) |
| 7 | Observer | 행동 | [01-04 §Observer](01-04.행동 패턴.md#observer--옵저버) |



## 학습 순서 권장

처음 보는 사람은 SOLID → 생성 패턴 → 구조 패턴 → 행동 패턴 → 클린 코드 → 일급객체 사상 순서로 읽으면 인지 부담이 적다. 패턴 카탈로그를 먼저 익혀 *언어*를 확보한 다음, 클린 코드와 일급객체 사상으로 *문장*을 쓰는 흐름이다.

02-01·02-02 다음에 02-03을 읽어 패턴 도입의 *함정 지도*를 같이 잡으면 좋다. 함수형 패턴이 트랜잭션·프록시·자원 수명과 만났을 때 어디서 깨지는가를 다른 카테고리 문서와 연결해 보여준다.

설계 토론이나 면접 직전 점검이 목적이라면 역순도 가능하다. 02-01 §6 적용 우선순위 표와 02-02 §12 패턴 도입 신호만 훑어도 즉시 활용 가능한 판단 기준이 잡힌다.



## 관련 카테고리

- [01_language/java/02_CollectionAndStream/](../02_CollectionAndStream/) — Stream/Optional 기반 함수형 코드 스타일
- [03_architecture/](../../../03_architecture/) — DDD, Hexagonal, Clean Architecture 등 시스템 차원 설계
- [11_spring/01_core/](../../../11_spring/01_core/) — Spring DI/IoC와 디자인 패턴 흡수
