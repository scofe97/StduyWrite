# 디자인 패턴 개론

## 개요

**정의**: 디자인 패턴은 소프트웨어 설계에서 반복되는 문제에 적용할 수 있는 재사용 가능한 솔루션 템플릿이다.

**목적**: 검증된 설계 지식을 공유하여 코드 품질과 유지보수성을 향상시킨다.

**역사**:
- 1977년: Christopher Alexander가 건축 패턴 개념 정립 ("A Pattern Language")
- 1995년: GoF(Gang of Four)가 23가지 핵심 OOP 패턴 정의

---

## 핵심 개념

### 패턴의 특성

| 특성 | 설명 |
|------|------|
| **처방적이지 않음** | 상황에 따라 적용 여부를 판단한다 |
| **언어 독립적** | JavaScript를 포함한 모든 언어에 적용 가능하다 |
| **프레임워크 내장** | React의 Provider 패턴처럼 이미 추상화되어 있을 수 있다 |

### 패턴의 이점

```
┌─────────────────────────────────────────────────────────────┐
│  핵심 이점                                                   │
├─────────────────────────────────────────────────────────────┤
│  검증된 솔루션: 시간 검증된 접근법 제공                        │
│  재사용성: 즉시 사용 가능한 솔루션                            │
│  표현력: 공유 어휘로 복잡한 문제를 명확히 표현                  │
├─────────────────────────────────────────────────────────────┤
│  추가 이점                                                   │
├─────────────────────────────────────────────────────────────┤
│  문제 예방: 구조적 실수 방지                                  │
│  일반화: 특정 언어/문제에 종속되지 않음                        │
│  DRY: 중복 제거로 코드 크기 축소                              │
│  커뮤니케이션: 팀 간 빠른 소통 가능                           │
└─────────────────────────────────────────────────────────────┘
```

### 패턴의 한계

패턴은 솔루션 스킴만 제공한다. 모든 설계 문제를 해결하지 않으며, 좋은 소프트웨어 설계자를 대체하지 않는다. 올바른 패턴 선택이 핵심이다.

---

## GoF 23가지 패턴 분류

### 생성 패턴 (Creational) - 5개
객체 생성 메커니즘을 다룬다.

| 패턴 | 목적 |
|------|------|
| Singleton | 클래스의 인스턴스를 하나로 제한 |
| Factory Method | 객체 생성을 서브클래스에 위임 |
| Abstract Factory | 관련 객체 군을 생성하는 인터페이스 제공 |
| Builder | 복잡한 객체를 단계별로 생성 |
| Prototype | 기존 객체를 복제하여 새 객체 생성 |

### 구조 패턴 (Structural) - 7개
객체와 클래스의 구성 방법을 다룬다.

| 패턴 | 목적 |
|------|------|
| Adapter | 호환되지 않는 인터페이스 연결 |
| Bridge | 추상화와 구현을 분리 |
| Composite | 객체를 트리 구조로 구성 |
| Decorator | 객체에 동적으로 책임 추가 |
| Facade | 복잡한 서브시스템에 단순한 인터페이스 제공 |
| Flyweight | 공유를 통해 많은 객체를 효율적으로 지원 |
| Proxy | 다른 객체에 대한 대리자 역할 |

### 행동 패턴 (Behavioral) - 11개
객체 간 책임 분배와 통신 방식을 다룬다.

| 패턴 | 목적 |
|------|------|
| Chain of Responsibility | 요청을 처리할 객체를 연결 |
| Command | 요청을 객체로 캡슐화 |
| Iterator | 컬렉션 요소에 순차 접근 |
| Mediator | 객체 간 상호작용을 캡슐화 |
| Memento | 객체 상태를 저장하고 복원 |
| Observer | 객체 상태 변화를 다른 객체에 통지 |
| State | 상태에 따라 객체 행동 변경 |
| Strategy | 알고리즘을 캡슐화하여 교체 가능 |
| Template Method | 알고리즘 골격 정의, 세부 단계는 서브클래스에서 구현 |
| Visitor | 객체 구조에 새로운 연산 추가 |
| Interpreter | 언어의 문법을 정의하고 해석 |

---

## 패턴 검증 프로세스

### Proto-Pattern과 Patlet

**Proto-Pattern**: 아직 충분한 검증을 거치지 않은 패턴 후보

**Patlet**: Proto-pattern의 간략한 설명 또는 코드 스니펫

모든 알고리즘, 모범 사례, 솔루션이 패턴이 되는 것은 아니다.

### Pattern-ity 테스트 (4가지 기준)

| 기준 | 설명 |
|------|------|
| **특정 문제 해결** | 원칙이 아닌 구체적 솔루션을 제공해야 한다 |
| **명백하지 않은 솔루션** | 잘 알려진 원칙에서 쉽게 도출되지 않아야 한다 |
| **검증된 개념** | 실제로 작동한다는 증거가 필요하다 |
| **관계 설명** | 시스템 구조와 메커니즘을 설명해야 한다 |

### Rule of Three

패턴이 유효하려면 반복되는 현상을 증명해야 한다.

| 요소 | 질문 |
|------|------|
| **Fitness of Purpose** | 패턴이 어떻게 성공적인가? |
| **Usefulness** | 패턴이 왜 성공적인가? |
| **Applicability** | 더 넓은 적용 가능성이 있는가? |

---

## 패턴 문서 구조

### 핵심 5가지 요소

| 요소 | 설명 | 예시 |
|------|------|------|
| **Pattern Name** | 패턴의 목적을 대표하는 고유한 이름 | "Observer", "Singleton" |
| **Description** | 패턴이 달성하는 것에 대한 간략한 설명 | "객체 간 1:N 의존성 정의" |
| **Context** | 패턴이 효과적으로 작동하는 상황 | "상태 변경 시 여러 객체 통지 필요" |
| **Problem** | 해결하려는 문제에 대한 진술 | "객체 상태 변경을 자동 통지" |
| **Solution** | 문제 해결 방법의 단계별 설명 | "Subject와 Observer 인터페이스 정의" |

### 추가 8가지 요소

Design, Implementation, Illustrations, Examples, Corequisites, Relations, Known Usage, Discussions

---

## 안티패턴

### 정의

**안티패턴**: 솔루션처럼 보이지만 실제로는 솔루션이 아닌 것

Andrew Koenig가 1995년에 용어를 창시했다. 패턴이 모범 사례라면, 안티패턴은 제안된 패턴이 잘못되었을 때 배운 교훈이다.

### 안티패턴의 두 가지 역할

1. **나쁜 솔루션 설명**: 특정 문제에 대한 나쁜 솔루션이 초래하는 불리한 상황
2. **탈출 방법 설명**: 해당 상황에서 벗어나 좋은 솔루션으로 전환하는 방법

### JavaScript 안티패턴

| 안티패턴 | 문제점 | 대안 |
|----------|--------|------|
| **전역 변수 남발** | 네임스페이스 충돌, 메모리 누수 | 모듈, 네임스페이스 패턴 |
| **setTimeout에 문자열 전달** | 내부적으로 eval() 실행, 보안 위험 | 함수 참조 전달 |
| **Object.prototype 수정** | 전역 영향, 다른 라이브러리와 충돌 | 유틸리티 함수 |
| **인라인 JavaScript** | 유연성 부족, CSP 위반 가능 | 이벤트 리스너 |
| **document.write 사용** | 페이지 로드 후 전체 덮어씀, XHTML 비호환 | DOM API |

### 코드 예시

```javascript
// 안티패턴: 전역 변수 남발
var name = "John";
var age = 30;

// 좋은 패턴: 모듈 사용
const MyApp = {
  name: "John",
  age: 30
};

// 안티패턴: setTimeout에 문자열 전달
setTimeout("doSomething()", 1000);

// 좋은 패턴: 함수 참조 전달
setTimeout(doSomething, 1000);

// 안티패턴: Object.prototype 수정
Object.prototype.myMethod = function() {};

// 좋은 패턴: 유틸리티 함수
function myMethod(obj) {}

// 안티패턴: document.write
document.write("<p>Hello</p>");

// 좋은 패턴: DOM API
document.body.insertAdjacentHTML('beforeend', '<p>Hello</p>');
```

---

## 실무 적용

### 패턴 적용 Decision Tree

```
문제 발생
    │
    ├─ 반복되는 문제인가?
    │       │
    │       ├─ Yes → 기존 패턴 존재?
    │       │           │
    │       │           ├─ Yes → 프레임워크에 구현됨?
    │       │           │           │
    │       │           │           ├─ Yes → 프레임워크 기능 사용
    │       │           │           └─ No → 패턴 적용
    │       │           │
    │       │           └─ No → 커스텀 솔루션
    │       │
    │       └─ No → 커스텀 솔루션
```

### 현대 JavaScript 프레임워크의 내장 패턴

| 프레임워크 | 내장 패턴 | 용도 |
|------------|-----------|------|
| React | Provider/Context | 전역 상태 공유 |
| React | Hooks | 상태 및 생명주기 로직 재사용 |
| React | HOC | 컴포넌트 로직 재사용 |
| Vue | Provide/Inject | 의존성 주입 |
| Angular | Dependency Injection | 서비스 주입 |

### 안티패턴 탐지 체크리스트

```yaml
code_review:
  global_scope:
    - 전역 변수가 최소화되어 있는가?
    - 네임스페이스/모듈 패턴을 사용하는가?

  timing_functions:
    - setTimeout/setInterval에 함수를 전달하는가?
    - 문자열을 전달하지 않는가?

  prototype:
    - 내장 객체의 prototype을 수정하지 않는가?

  dom_manipulation:
    - document.write를 사용하지 않는가?
    - DOM API를 적절히 사용하는가?

  html_js_separation:
    - 인라인 이벤트 핸들러가 없는가?
    - JavaScript가 별도 파일로 분리되어 있는가?
```

---

## 트레이드오프

| 장점 | 단점 |
|------|------|
| 검증된 솔루션 재사용 | 과도한 엔지니어링 위험 |
| 팀 커뮤니케이션 향상 | 모든 문제에 적합하지 않음 |
| 코드 품질 향상 | 학습 곡선 존재 |
| 유지보수성 개선 | 잘못된 컨텍스트에서 적용 시 역효과 |

---

## 면접 포인트

**Q**: 디자인 패턴이란 무엇인가?

**A**: 디자인 패턴은 소프트웨어 설계에서 반복되는 문제에 적용할 수 있는 재사용 가능한 솔루션 템플릿이다. GoF가 1995년에 23가지 핵심 패턴을 정의했으며, 생성, 구조, 행동 패턴으로 분류된다.

**Q**: 안티패턴이란 무엇인가?

**A**: 안티패턴은 솔루션처럼 보이지만 실제로는 문제를 야기하는 설계 방식이다. JavaScript에서는 전역 변수 남발, Object.prototype 수정, document.write 사용 등이 대표적이다. 안티패턴을 알면 흔한 실수를 사전에 회피할 수 있다.

**Q**: 패턴과 Proto-Pattern의 차이는?

**A**: 패턴은 Pattern-ity 테스트(특정 문제 해결, 명백하지 않은 솔루션, 검증된 개념, 관계 설명)와 Rule of Three(적합성, 유용성, 적용 가능성)를 충족한 검증된 솔루션이다. Proto-Pattern은 아직 이 검증을 거치지 않은 패턴 후보다.

---

## 참고 자료

- GoF, "Design Patterns: Elements of Reusable Object-Oriented Software" (1995)
- Christopher Alexander, "A Pattern Language" (1977)
- Andrew Koenig, "Journal of Object-Oriented Programming" (1995)
- [React Context API](https://react.dev/reference/react/useContext)
