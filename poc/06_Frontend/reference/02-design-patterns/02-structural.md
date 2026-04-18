# 구조 패턴 (Structural Patterns)

## 개요

**정의**: 구조 패턴은 객체 구성(Composition)에 관심을 두고, 서로 다른 객체 간의 관계를 실현하는 단순한 방법을 제공하는 패턴이다.

**목적**: 시스템 일부가 변경될 때 전체 구조가 변경되지 않도록 보장하고, 특정 목적에 맞지 않는 시스템 부분을 목적에 맞게 재구성한다.

---

## 핵심 개념

### 패턴 선택 가이드

```
객체 구성/관계 문제 발생
    │
    ├─ 복잡한 API를 단순화?
    │       └─ Yes → Facade 패턴
    │
    ├─ 여러 클래스에 기능 공유?
    │       └─ Yes → Mixin 패턴
    │
    ├─ 동적으로 기능 추가?
    │       └─ Yes → Decorator 패턴
    │
    └─ 메모리 최적화 필요?
            └─ Yes → Flyweight 패턴
```

### 패턴 비교

| 패턴 | 핵심 목적 | 주요 기법 | 결과 |
|------|----------|----------|------|
| Facade | 복잡성 숨김 | 단순 인터페이스 | 사용 용이 |
| Mixin | 기능 공유 | 클래스 확장 | 재사용성 |
| Decorator | 동적 기능 추가 | 래핑 | 유연성 |
| Flyweight | 메모리 최적화 | 공유 | 효율성 |

---

## 구현 패턴

### 1. Facade Pattern (파사드 패턴)

**목적**: 더 큰 코드 본체에 대한 편리한 고수준 인터페이스 제공

```javascript
// 크로스 브라우저 이벤트 Facade
const addMyEvent = (el, ev, fn) => {
    if (el.addEventListener) {
        el.addEventListener(ev, fn, false);
    } else if (el.attachEvent) {
        el.attachEvent(`on${ev}`, fn);
    } else {
        el[`on${ev}`] = fn;
    }
};
```

**Module 패턴과 통합**:

```javascript
// privateMethods.js
const _private = {
    i: 5,
    get() { console.log(`current value: ${this.i}`); },
    set(val) { this.i = val; },
    run() { console.log('running'); },
    jump() { console.log('jumping'); },
};

export default _private;

// module.js
import _private from './privateMethods.js';

const module = {
    facade({ val, run }) {
        _private.set(val);
        _private.get();
        if (run) {
            _private.run();
        }
    },
};

export default module;

// 사용
module.facade({ val: 10, run: true });
// current value: 10
// running
```

---

### 2. Mixin Pattern (믹스인 패턴)

**목적**: 여러 클래스에서 쉽게 공유할 수 있는 속성과 메서드를 가진 클래스

**서브클래싱 기본**:

```javascript
class Person {
    constructor(firstName, lastName) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.gender = "male";
    }
}

class Superhero extends Person {
    constructor(firstName, lastName, powers) {
        super(firstName, lastName);
        this.powers = powers;
    }
}

const SuperMan = new Superhero('Clark', 'Kent', ['flight', 'heat-vision']);
```

**Mixin 함수 구현**:

```javascript
const MyMixins = superclass =>
    class extends superclass {
        moveUp() { console.log('move up'); }
        moveDown() { console.log('move down'); }
        stop() { console.log('stop! in the name of love!'); }
    };

class CarAnimator {
    moveLeft() { console.log('move left'); }
}

// Mixin 적용
class MyAnimator extends MyMixins(CarAnimator) {}

const myAnimator = new MyAnimator();
myAnimator.moveLeft();  // move left
myAnimator.moveDown();  // move down
myAnimator.stop();      // stop! in the name of love!
```

**여러 Mixin 조합**:

```javascript
const Movable = superclass => class extends superclass {
    move() { console.log('moving'); }
};

const Jumpable = superclass => class extends superclass {
    jump() { console.log('jumping'); }
};

class Character {}

class Player extends Movable(Jumpable(Character)) {}

const player = new Player();
player.move();  // moving
player.jump();  // jumping
```

---

### 3. Decorator Pattern (데코레이터 패턴)

**목적**: 기존 클래스에 동적으로 행동 추가

**MacBook 가격 계산 예제**:

```javascript
class MacBook {
    constructor() {
        this.cost = 997;
        this.screenSize = 11.6;
    }
    getCost() { return this.cost; }
    getScreenSize() { return this.screenSize; }
}

// Decorator 1: 메모리 업그레이드
class Memory extends MacBook {
    constructor(macBook) {
        super();
        this.macBook = macBook;
    }
    getCost() { return this.macBook.getCost() + 75; }
}

// Decorator 2: 각인
class Engraving extends MacBook {
    constructor(macBook) {
        super();
        this.macBook = macBook;
    }
    getCost() { return this.macBook.getCost() + 200; }
}

// Decorator 3: 보험
class Insurance extends MacBook {
    constructor(macBook) {
        super();
        this.macBook = macBook;
    }
    getCost() { return this.macBook.getCost() + 250; }
}

// 사용: 데코레이터 체이닝
let mb = new MacBook();
mb = new Memory(mb);
mb = new Engraving(mb);
mb = new Insurance(mb);

console.log(mb.getCost());       // 1522 (997 + 75 + 200 + 250)
console.log(mb.getScreenSize()); // 11.6
```

**함수 기반 Decorator**:

```javascript
function withLogging(fn) {
    return function(...args) {
        console.log(`Calling ${fn.name} with`, args);
        const result = fn.apply(this, args);
        console.log(`Result:`, result);
        return result;
    };
}

function add(a, b) {
    return a + b;
}

const loggedAdd = withLogging(add);
loggedAdd(2, 3);
// Calling add with [2, 3]
// Result: 5
```

---

### 4. Flyweight Pattern (플라이웨이트 패턴)

**목적**: 많은 관련 객체와 데이터를 공유하여 메모리 사용 최소화

**핵심 개념**:

| 용어 | 설명 | 예시 |
|------|------|------|
| **Intrinsic** (내재적) | 객체 내부에 필요한 정보, 공유 가능 | 책 제목, 저자, ISBN |
| **Extrinsic** (외재적) | 외부에 저장 가능한 정보 | 대출일, 반납일, 회원 |

**도서관 시스템 예제**:

```javascript
// 최적화 전: 모든 데이터가 각 객체에 포함
class Book {
    constructor(id, title, author, genre, pageCount, publisherID, ISBN,
                checkoutDate, checkoutMember, dueReturnDate, availability) {
        this.id = id;
        this.title = title;
        this.author = author;
        // ... 모든 속성 포함
    }
}
```

```javascript
// 최적화 후: Flyweight (내재적 데이터만)
class Book {
    constructor({ title, author, genre, pageCount, publisherID, ISBN }) {
        this.title = title;
        this.author = author;
        this.genre = genre;
        this.pageCount = pageCount;
        this.publisherID = publisherID;
        this.ISBN = ISBN;
    }
}

// Factory: 동일한 책은 한 번만 생성
const existingBooks = {};

class BookFactory {
    createBook({ title, author, genre, pageCount, publisherID, ISBN }) {
        const existingBook = existingBooks[ISBN];
        if (existingBook) {
            return existingBook;
        }
        const book = new Book({ title, author, genre, pageCount, publisherID, ISBN });
        existingBooks[ISBN] = book;
        return book;
    }
}

// Manager: 외재적 상태 관리
const bookRecordDatabase = {};

class BookRecordManager {
    addBookRecord({ id, title, author, genre, pageCount, publisherID, ISBN,
                    checkoutMember, checkoutDate, dueReturnDate, availability }) {
        const bookFactory = new BookFactory();
        const book = bookFactory.createBook({ title, author, genre, pageCount, publisherID, ISBN });

        bookRecordDatabase[id] = {
            checkoutMember,
            checkoutDate,
            dueReturnDate,
            availability,
            book,  // Flyweight 참조
        };
    }

    updateCheckoutStatus({ bookID, newStatus, checkoutDate, checkoutMember, newReturnDate }) {
        const record = bookRecordDatabase[bookID];
        record.availability = newStatus;
        record.checkoutDate = checkoutDate;
        record.checkoutMember = checkoutMember;
        record.dueReturnDate = newReturnDate;
    }
}
```

**메모리 절약 효과**: 30권의 동일한 책 → 1개의 Book 객체만 저장

---

## 트레이드오프

### Facade Pattern

| 장점 | 단점 |
|------|------|
| 사용 용이성 | 내부 구현에 대한 접근 제한 |
| 작은 구현 풋프린트 | 추상화 레벨 추가 |
| 복잡성 숨김 | 성능 오버헤드 가능 |

### Mixin Pattern

| 장점 | 단점 |
|------|------|
| 기능 반복 감소 | 프로토타입 오염 가능 |
| 재사용 증가 | 함수 출처 불확실성 |
| 유연한 구성 | React에서 HOC/Hooks로 대체 권장 |

### Decorator Pattern

| 장점 | 단점 |
|------|------|
| 투명하게 사용 가능 | 아키텍처 복잡성 증가 |
| 유연성 | 작은 유사 객체 증가 |
| 서브클래스 대량 생성 방지 | 디버깅 어려움 |

### Flyweight Pattern

| 장점 | 단점 |
|------|------|
| 대폭적인 메모리 절약 | 구현 복잡도 증가 |
| 대규모 객체 처리 효율 | 외재적 상태 관리 필요 |
| 캐싱 효과 | 팩토리 패턴 필요 |

---

## 실무 적용

### React에서의 구조 패턴

| 패턴 | React 구현 |
|------|-----------|
| Facade | Custom Hooks (복잡한 로직 숨김) |
| Mixin | Hooks (기능 공유, Mixin 대체) |
| Decorator | HOC (Higher-Order Components) |
| Flyweight | React.memo, useMemo |

### 패턴 선택 체크리스트

```yaml
facade_pattern:
  use_when:
    - 복잡한 라이브러리 래핑
    - 레거시 시스템 통합
    - 서드파티 API 단순화
  avoid_when:
    - 모든 기능 노출 필요
    - 추상화 오버헤드 문제

mixin_pattern:
  use_when:
    - 다중 상속 필요
    - 횡단 관심사 공유
  avoid_when:
    - React 프로젝트 (Hooks 사용)
    - 명확한 상속 구조 필요

decorator_pattern:
  use_when:
    - 런타임 기능 추가
    - 조합 가능한 기능
  avoid_when:
    - 단순 상속으로 충분
    - 성능이 중요

flyweight_pattern:
  use_when:
    - 많은 유사 객체 생성
    - 메모리 제약 환경
  avoid_when:
    - 객체 수가 적음
    - 모든 상태가 고유
```

### 실제 사용 사례

```javascript
// Facade: API 클라이언트
class APIClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    async fetchUser(id) {
        const response = await fetch(`${this.baseURL}/users/${id}`);
        const data = await response.json();
        return this.transformUser(data);
    }

    transformUser(data) {
        return { id: data.id, name: `${data.firstName} ${data.lastName}` };
    }
}

// Decorator: 로깅 추가
function withLogging(apiClient) {
    const original = apiClient.fetchUser.bind(apiClient);
    apiClient.fetchUser = async function(id) {
        console.log(`Fetching user ${id}`);
        const result = await original(id);
        console.log(`Fetched:`, result);
        return result;
    };
    return apiClient;
}
```

---

## 면접 포인트

**Q**: Facade 패턴은 언제 사용하는가?

**A**: Facade 패턴은 복잡한 서브시스템에 단순한 인터페이스를 제공할 때 사용한다. 레거시 시스템 래핑, 서드파티 라이브러리 통합, 복잡한 API 단순화가 대표적인 사례다. React에서는 여러 상태와 효과를 관리하는 로직을 Custom Hook으로 추상화하는 것이 Facade 패턴의 예다.

**Q**: Decorator 패턴과 상속의 차이는?

**A**: 상속은 컴파일 타임에 정적으로 기능을 추가하는 반면, Decorator 패턴은 런타임에 동적으로 기능을 추가한다. Decorator는 객체를 래핑하여 기능을 조합하므로 서브클래스의 폭발적 증가를 방지한다. React의 HOC가 Decorator 패턴의 대표적 예다.

**Q**: Flyweight 패턴에서 Intrinsic과 Extrinsic 상태의 차이는?

**A**: Intrinsic 상태는 객체 내부에 저장되고 여러 인스턴스가 공유할 수 있는 불변 데이터다. Extrinsic 상태는 컨텍스트에 따라 달라지는 외부 데이터로, 별도로 관리된다. 도서관 시스템에서 책의 제목, 저자, ISBN은 Intrinsic이고, 대출일, 반납일은 Extrinsic이다.

---

## 참고 자료

- GoF, "Design Patterns: Elements of Reusable Object-Oriented Software"
- Dustin Diaz, Ross Harmes, "Pro JavaScript Design Patterns"
- [MDN: Mixins](https://developer.mozilla.org/en-US/docs/Glossary/Mixin)
- [React Higher-Order Components](https://reactjs.org/docs/higher-order-components.html)
