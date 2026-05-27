# 생성 패턴 (Creational Patterns)

## 개요

**정의**: 생성 패턴은 객체 생성 메커니즘을 다루어, 주어진 상황에 적합한 방식으로 객체를 생성하는 패턴이다.

**목적**: 기본적인 객체 생성 방식이 야기하는 복잡성을 해결하고, 생성 프로세스를 제어한다.

---

## 핵심 개념

### 패턴 선택 가이드

```
객체 생성 문제 발생
    │
    ├─ 초기화가 복잡한가?
    │       └─ Yes → Factory 패턴
    │
    ├─ 인스턴스가 하나만 필요?
    │       └─ Yes → Singleton 패턴
    │
    ├─ 기존 객체를 복제?
    │       └─ Yes → Prototype 패턴
    │
    └─ 캡슐화가 필요?
            ├─ Yes → Module 패턴
            └─ No → Constructor 패턴
```

### 패턴 비교

| 패턴 | 핵심 개념 | 사용 시기 | JavaScript 특징 |
|------|----------|----------|-----------------|
| Constructor | `new` + `class` | 기본 객체 초기화 | ES6 class 문법 |
| Module | 클로저, export | 캡슐화 필요 | ES Modules |
| Revealing Module | private → public 노출 | 일관된 API | 명확한 public 정의 |
| Singleton | 단일 인스턴스 | 전역 상태 | Context/Redux 대안 |
| Prototype | `Object.create()` | 복제 기반 생성 | 프로토타입 체인 |
| Factory | 생성 추상화 | 복잡한 생성 로직 | 다형성 |

---

## 구현 패턴

### 1. Constructor Pattern (생성자 패턴)

**목적**: 새로 생성된 객체를 초기화하는 특별한 메서드

```javascript
class Car {
    constructor(model, year, miles) {
        this.model = model;
        this.year = year;
        this.miles = miles;
    }

    toString() {
        return `${this.model} has done ${this.miles} miles`;
    }
}

const civic = new Car('Honda Civic', 2009, 20000);
console.log(civic.toString());
```

**프로토타입을 활용한 생성자**:

```javascript
class Car {
    constructor(model, year, miles) {
        this.model = model;
        this.year = year;
        this.miles = miles;
    }
}

// 프로토타입에 메서드 추가 - 모든 인스턴스가 공유
Car.prototype.toString = function() {
    return `${this.model} has done ${this.miles} miles`;
};
```

모든 Car 객체가 동일한 `toString()` 메서드를 공유하여 메모리 효율적이다.

---

### 2. Module Pattern (모듈 패턴)

**목적**: 클로저를 사용하여 "프라이버시" 상태와 조직을 캡슐화

```javascript
// privates
const basket = [];

const basketModule = {
    addItem(values) {
        basket.push(values);
    },
    getItemCount() {
        return basket.length;
    },
    getTotal() {
        return basket.reduce((sum, item) => item.price + sum, 0);
    },
};

export default basketModule;

// 사용
basketModule.addItem({ item: 'bread', price: 0.5 });
console.log(basketModule.getItemCount()); // 1
console.log(basketModule.basket);         // undefined (private)
```

**WeakMap을 활용한 현대적 모듈 패턴**:

```javascript
let _counter = new WeakMap();

class Module {
    constructor() {
        _counter.set(this, 0);
    }

    incrementCounter() {
        let counter = _counter.get(this);
        counter++;
        _counter.set(this, counter);
        return _counter.get(this);
    }

    resetCounter() {
        console.log(`counter value prior to reset: ${_counter.get(this)}`);
        _counter.set(this, 0);
    }
}
```

---

### 3. Revealing Module Pattern (노출식 모듈 패턴)

**목적**: 모든 함수와 변수를 private 스코프에 정의하고, public으로 노출할 것만 반환

```javascript
let privateVar = 'Rob Dodson';
const publicVar = 'Hey there!';

const privateFunction = () => {
    console.log(`Name: ${privateVar}`);
};

const publicSetName = strName => {
    privateVar = strName;
};

const publicGetName = () => {
    privateFunction();
};

// public 포인터를 private 함수/속성에 노출
const myRevealingModule = {
    setName: publicSetName,
    greeting: publicVar,
    getName: publicGetName,
};

export default myRevealingModule;
```

---

### 4. Singleton Pattern (싱글톤 패턴)

**목적**: 클래스의 인스턴스화를 단일 객체로 제한

```javascript
let instance;

const privateMethod = () => {
    console.log('I am private');
};
const randomNumber = Math.random();

class MySingleton {
    constructor() {
        if (!instance) {
            this.publicProperty = 'I am also public';
            instance = this;
        }
        return instance;
    }

    publicMethod() {
        console.log('The public can see me!');
    }

    getRandomNumber() {
        return randomNumber;
    }
}

export default MySingleton;

// 사용
const singleA = new MySingleton();
const singleB = new MySingleton();
console.log(singleA.getRandomNumber() === singleB.getRandomNumber()); // true
```

**적용 시기**:
- 정확히 하나의 인스턴스만 필요할 때
- 잘 알려진 접근점에서 접근 가능해야 할 때

**JavaScript에서의 주의사항**:

| 문제점 | 대안 |
|--------|------|
| 싱글톤 식별 어려움 | 명확한 네이밍 |
| 테스트 어려움 | Dependency Injection |
| 실행 순서 조율 필요 | Redux, React Context |

---

### 5. Prototype Pattern (프로토타입 패턴)

**목적**: 기존 객체를 복제하여 새 객체 생성 (프로토타입 상속 기반)

```javascript
const myCar = {
    name: 'Ford Escort',
    drive() {
        console.log("Weeee. I'm driving!");
    },
    panic() {
        console.log('Wait. How do you stop this thing?');
    },
};

// Object.create로 새 인스턴스 생성
const yourCar = Object.create(myCar);
console.log(yourCar.name); // "Ford Escort"
```

**차등 상속 (Differential Inheritance)**:

```javascript
const vehicle = {
    getModel() {
        console.log(`The model of this vehicle is...${this.model}`);
    },
};

const car = Object.create(vehicle, {
    id: {
        value: nextId(),
        enumerable: true,
    },
    model: {
        value: 'Ford',
        enumerable: true,
    },
});
```

---

### 6. Factory Pattern (팩토리 패턴)

**목적**: 생성자를 명시적으로 요구하지 않고 객체를 생성하는 일반적인 인터페이스 제공

```javascript
class Car {
    constructor({ doors = 4, state = 'brand new', color = 'silver' } = {}) {
        this.doors = doors;
        this.state = state;
        this.color = color;
    }
}

class Truck {
    constructor({ state = 'used', wheelSize = 'large', color = 'blue' } = {}) {
        this.state = state;
        this.wheelSize = wheelSize;
        this.color = color;
    }
}

class VehicleFactory {
    constructor() {
        this.vehicleClass = Car;
    }

    createVehicle(options) {
        const { vehicleType, ...rest } = options;

        switch (vehicleType) {
            case 'car':
                this.vehicleClass = Car;
                break;
            case 'truck':
                this.vehicleClass = Truck;
                break;
        }

        return new this.vehicleClass(rest);
    }
}

// 사용
const carFactory = new VehicleFactory();
const car = carFactory.createVehicle({
    vehicleType: 'car',
    color: 'yellow',
    doors: 6,
});

console.log(car instanceof Car); // true
```

**Abstract Factory**:

```javascript
class AbstractVehicleFactory {
    constructor() {
        this.types = {};
    }

    getVehicle(type, customizations) {
        const Vehicle = this.types[type];
        return Vehicle ? new Vehicle(customizations) : null;
    }

    registerVehicle(type, Vehicle) {
        const proto = Vehicle.prototype;
        // vehicle 계약을 충족하는 클래스만 등록
        if (proto.drive && proto.breakDown) {
            this.types[type] = Vehicle;
        }
        return this;
    }
}
```

---

## 트레이드오프

### Module Pattern

| 장점 | 단점 |
|------|------|
| private 데이터 지원 | public/private 접근 방식 차이 |
| 전역 스코프 오염 방지 | 나중에 추가한 메서드에서 private 접근 불가 |
| 네이밍 충돌 방지 | private 멤버 테스트 어려움 |

### Revealing Module Pattern

| 장점 | 단점 |
|------|------|
| 일관된 구문 | private → public 참조 시 패치 불가 |
| 모듈 끝에서 public 명확 | public 멤버도 no-patch 규칙 적용 |
| 가독성 향상 | |

---

## 실무 적용

### 패턴 선택 체크리스트

```yaml
constructor_pattern:
  use_when:
    - 간단한 객체 초기화
    - 프로토타입 메서드 공유 필요
  avoid_when:
    - 복잡한 생성 로직
    - 조건부 객체 타입

module_pattern:
  use_when:
    - private 상태 필요
    - 네임스페이스 충돌 방지
  avoid_when:
    - 여러 인스턴스 필요
    - 테스트 커버리지 중요

singleton_pattern:
  use_when:
    - 전역 상태 관리
    - 설정 객체
  avoid_when:
    - 테스트 용이성 중요
    - 다중 인스턴스 가능성

factory_pattern:
  use_when:
    - 런타임에 타입 결정
    - 복잡한 생성 로직
  avoid_when:
    - 단순 객체 생성
    - 타입이 고정
```

### 안티패턴 피하기

| 문제 | 해결책 |
|------|--------|
| Singleton 남용 (전역 상태 남용) | Dependency Injection 또는 Context 사용 |
| Module 테스트 어려움 (private 멤버) | 테스트 가능한 public API 설계 |

### ES2015+ 클래스 vs 전통적 패턴

```javascript
// ES5 Module Pattern
var Module = (function() {
    var private = 'private';
    return {
        public: function() { return private; }
    };
})();

// ES2015+ Class with Private Fields
class Module {
    #private = 'private';
    public() { return this.#private; }
}
```

---

## 면접 포인트

**Q**: Singleton 패턴은 언제 사용하는가?

**A**: Singleton은 클래스의 인스턴스를 단 하나로 제한해야 할 때 사용한다. 전역 설정 객체, 로깅 시스템, 데이터베이스 연결 풀 등이 대표적이다. 단, JavaScript에서는 테스트 어려움과 전역 상태 의존성 문제가 있어 React Context나 Redux 같은 상태 관리 라이브러리로 대체하는 것이 권장된다.

**Q**: Factory 패턴과 Constructor 패턴의 차이는?

**A**: Constructor 패턴은 `new` 키워드로 직접 객체를 생성하며 생성할 타입이 고정되어 있다. Factory 패턴은 생성 로직을 추상화하여 런타임에 타입을 결정할 수 있고, 생성 과정을 캡슐화한다. 복잡한 객체 생성이나 조건부 타입 생성이 필요할 때 Factory 패턴이 적합하다.

**Q**: Module 패턴에서 private 변수를 구현하는 방법은?

**A**: ES5에서는 클로저를 활용하여 IIFE 내부에 변수를 선언하고, 반환된 객체의 메서드를 통해서만 접근하게 한다. ES2015+에서는 WeakMap을 사용하거나, 클래스의 `#` 프라이빗 필드 문법을 사용할 수 있다.

---

## 참고 자료

- GoF, "Design Patterns: Elements of Reusable Object-Oriented Software"
- Dustin Diaz, Ross Harmes, "Pro JavaScript Design Patterns"
- [MDN: Object.create()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/create)
- [MDN: Classes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes)
