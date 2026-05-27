# JavaScript 핵심 개념

## 개요

**정의**: JavaScript의 핵심 개념은 언어의 동작 원리를 이해하기 위한 근본적인 메커니즘으로, 실행 컨텍스트, 클로저, 프로토타입, this 바인딩, 이벤트 루프를 포함한다.

**목적**: 예측 가능한 코드 작성, 메모리 관리 최적화, 비동기 처리 이해, 객체 지향 패턴 구현을 가능하게 한다.

---

## 핵심 개념

### 1. 실행 컨텍스트 (Execution Context)

**정의**: 코드가 실행되는 환경으로, 변수, 함수 선언, this 값, 스코프 체인 정보를 담고 있는 객체이다.

```
┌─────────────────────────────────────────────────────┐
│              Execution Context Stack                │
├─────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────┐  │
│  │ Function Execution Context (innerFunc)        │  │
│  │  - Variable Environment: { c: undefined }     │  │
│  │  - Lexical Environment: outer → outerFunc     │  │
│  │  - this: window (non-strict)                  │  │
│  └───────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────┐  │
│  │ Function Execution Context (outerFunc)        │  │
│  │  - Variable Environment: { b: 20 }            │  │
│  │  - Lexical Environment: outer → global        │  │
│  │  - this: window                               │  │
│  └───────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────┐  │
│  │ Global Execution Context                      │  │
│  │  - Variable Environment: { a: 10 }            │  │
│  │  - Lexical Environment: outer → null          │  │
│  │  - this: window                               │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

**실행 컨텍스트 구성 요소**:

| 구성 요소 | 설명 | 포함 내용 |
|-----------|------|-----------|
| Variable Environment | 변수 선언 저장 | var 변수, 함수 선언 |
| Lexical Environment | 스코프 체인 관리 | let/const 변수, 외부 환경 참조 |
| this Binding | this 값 결정 | 호출 방식에 따라 결정 |

**호이스팅 (Hoisting)**:

```javascript
console.log(a); // undefined (var 호이스팅)
console.log(b); // ReferenceError (TDZ)
console.log(c); // ReferenceError (TDZ)

var a = 1;
let b = 2;
const c = 3;

// 함수 선언문은 전체가 호이스팅
sayHello(); // "Hello" (정상 동작)
function sayHello() {
  console.log("Hello");
}

// 함수 표현식은 변수만 호이스팅
sayBye(); // TypeError: sayBye is not a function
var sayBye = function() {
  console.log("Bye");
};
```

---

### 2. 스코프와 스코프 체인

**스코프 유형**:

| 스코프 | 설명 | 키워드 |
|--------|------|--------|
| 전역 스코프 | 어디서든 접근 가능 | 최상위 선언 |
| 함수 스코프 | 함수 내부에서만 접근 | var |
| 블록 스코프 | 블록 {} 내부에서만 접근 | let, const |

```javascript
var globalVar = "global";  // 전역 스코프

function outer() {
  var outerVar = "outer";  // 함수 스코프

  if (true) {
    var varInBlock = "var";     // 함수 스코프 (블록 무시)
    let letInBlock = "let";     // 블록 스코프
    const constInBlock = "const"; // 블록 스코프
  }

  console.log(varInBlock);    // "var" (접근 가능)
  console.log(letInBlock);    // ReferenceError
}
```

**스코프 체인**:

```javascript
const global = "전역";

function outer() {
  const outerVar = "외부";

  function inner() {
    const innerVar = "내부";

    // 스코프 체인: inner → outer → global
    console.log(innerVar);  // "내부" (자신의 스코프)
    console.log(outerVar);  // "외부" (외부 스코프)
    console.log(global);    // "전역" (전역 스코프)
  }

  inner();
}
```

---

### 3. 클로저 (Closure)

**정의**: 함수와 그 함수가 선언된 렉시컬 환경의 조합이다. 내부 함수가 외부 함수의 변수에 접근할 수 있으며, 외부 함수 실행이 종료된 후에도 해당 변수를 참조할 수 있다.

```javascript
function createCounter() {
  let count = 0;  // 자유 변수 (free variable)

  return {
    increment: function() {
      count++;
      return count;
    },
    decrement: function() {
      count--;
      return count;
    },
    getCount: function() {
      return count;
    }
  };
}

const counter = createCounter();
console.log(counter.increment()); // 1
console.log(counter.increment()); // 2
console.log(counter.getCount());  // 2

// count 변수는 외부에서 직접 접근 불가 (캡슐화)
console.log(counter.count); // undefined
```

**클로저 활용 패턴**:

```javascript
// 1. 데이터 프라이버시 (모듈 패턴)
const bankAccount = (function() {
  let balance = 0;  // private

  return {
    deposit(amount) {
      balance += amount;
      return balance;
    },
    withdraw(amount) {
      if (amount <= balance) {
        balance -= amount;
        return balance;
      }
      return "잔액 부족";
    },
    getBalance() {
      return balance;
    }
  };
})();

// 2. 함수 팩토리
function multiplier(factor) {
  return function(number) {
    return number * factor;
  };
}

const double = multiplier(2);
const triple = multiplier(3);

console.log(double(5));  // 10
console.log(triple(5));  // 15

// 3. 이벤트 핸들러와 콜백
function setupButton(buttonId, message) {
  const button = document.getElementById(buttonId);
  button.addEventListener('click', function() {
    // message는 클로저를 통해 접근
    alert(message);
  });
}
```

**클로저 주의사항 - 루프 문제**:

```javascript
// 문제: 모든 버튼이 5를 출력
for (var i = 0; i < 5; i++) {
  setTimeout(function() {
    console.log(i);  // 5, 5, 5, 5, 5
  }, 100);
}

// 해결 1: let 사용 (블록 스코프)
for (let i = 0; i < 5; i++) {
  setTimeout(function() {
    console.log(i);  // 0, 1, 2, 3, 4
  }, 100);
}

// 해결 2: IIFE로 새 스코프 생성
for (var i = 0; i < 5; i++) {
  (function(j) {
    setTimeout(function() {
      console.log(j);  // 0, 1, 2, 3, 4
    }, 100);
  })(i);
}
```

---

### 4. this 바인딩

**정의**: this는 함수가 호출되는 방식에 따라 동적으로 결정되는 특수한 식별자이다.

**this 결정 규칙 (우선순위 순)**:

| 우선순위 | 호출 방식 | this 값 | 예시 |
|----------|-----------|---------|------|
| 1 | new 바인딩 | 새로 생성된 객체 | `new Func()` |
| 2 | 명시적 바인딩 | 지정된 객체 | `call/apply/bind` |
| 3 | 암시적 바인딩 | 호출 객체 | `obj.method()` |
| 4 | 기본 바인딩 | 전역/undefined | `func()` |

```javascript
const person = {
  name: "Kim",
  greet: function() {
    console.log(`Hello, ${this.name}`);
  }
};

// 1. 암시적 바인딩
person.greet();  // "Hello, Kim"

// 2. 기본 바인딩
const greet = person.greet;
greet();  // "Hello, undefined" (strict mode에서는 TypeError)

// 3. 명시적 바인딩
const anotherPerson = { name: "Lee" };
person.greet.call(anotherPerson);   // "Hello, Lee"
person.greet.apply(anotherPerson);  // "Hello, Lee"

const boundGreet = person.greet.bind(anotherPerson);
boundGreet();  // "Hello, Lee"

// 4. new 바인딩
function Person(name) {
  this.name = name;
}
const p = new Person("Park");
console.log(p.name);  // "Park"
```

**화살표 함수의 this**:

```javascript
const obj = {
  name: "Object",

  // 일반 함수: this는 호출 방식에 따라 결정
  regularMethod: function() {
    console.log(this.name);  // "Object"

    // 콜백의 this는 기본 바인딩
    setTimeout(function() {
      console.log(this.name);  // undefined
    }, 100);
  },

  // 화살표 함수: this는 렉시컬 스코프에서 상속
  arrowMethod: function() {
    console.log(this.name);  // "Object"

    // 화살표 함수는 외부 this를 상속
    setTimeout(() => {
      console.log(this.name);  // "Object"
    }, 100);
  }
};
```

---

### 5. 프로토타입 (Prototype)

**정의**: JavaScript의 객체 상속 메커니즘으로, 모든 객체는 다른 객체를 참조하는 내부 링크(프로토타입)를 가진다.

```
┌─────────────────────────────────────────────────────────┐
│                  프로토타입 체인                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   dog 인스턴스                                           │
│   { name: "Max" }                                        │
│        │                                                 │
│        │ __proto__                                       │
│        ▼                                                 │
│   Dog.prototype                                          │
│   { bark: function, constructor: Dog }                   │
│        │                                                 │
│        │ __proto__                                       │
│        ▼                                                 │
│   Animal.prototype                                       │
│   { eat: function, constructor: Animal }                 │
│        │                                                 │
│        │ __proto__                                       │
│        ▼                                                 │
│   Object.prototype                                       │
│   { toString, hasOwnProperty, ... }                      │
│        │                                                 │
│        │ __proto__                                       │
│        ▼                                                 │
│       null                                               │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**프로토타입 기반 상속**:

```javascript
// 생성자 함수
function Animal(name) {
  this.name = name;
}

Animal.prototype.eat = function() {
  console.log(`${this.name} is eating`);
};

function Dog(name, breed) {
  Animal.call(this, name);  // 부모 생성자 호출
  this.breed = breed;
}

// 프로토타입 체인 설정
Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog;

Dog.prototype.bark = function() {
  console.log(`${this.name} says woof!`);
};

const dog = new Dog("Max", "Labrador");
dog.eat();   // "Max is eating" (Animal에서 상속)
dog.bark();  // "Max says woof!" (Dog 고유)

// 프로토타입 체인 확인
console.log(dog instanceof Dog);     // true
console.log(dog instanceof Animal);  // true
console.log(dog instanceof Object);  // true
```

**ES6 클래스 (문법적 설탕)**:

```javascript
class Animal {
  constructor(name) {
    this.name = name;
  }

  eat() {
    console.log(`${this.name} is eating`);
  }
}

class Dog extends Animal {
  constructor(name, breed) {
    super(name);  // 부모 생성자 호출
    this.breed = breed;
  }

  bark() {
    console.log(`${this.name} says woof!`);
  }
}

// 내부적으로는 프로토타입 기반으로 동작
const dog = new Dog("Max", "Labrador");
console.log(Object.getPrototypeOf(dog) === Dog.prototype);  // true
```

---

### 6. 이벤트 루프 (Event Loop)

**정의**: JavaScript의 비동기 처리를 가능하게 하는 런타임 메커니즘으로, 콜 스택, 태스크 큐, 마이크로태스크 큐를 조율한다.

```
┌─────────────────────────────────────────────────────────────┐
│                    JavaScript Runtime                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────────┐        ┌─────────────────────────────┐   │
│   │  Call Stack  │        │        Web APIs             │   │
│   │              │        │  (setTimeout, fetch, DOM)   │   │
│   │   func3()    │ ────►  │                             │   │
│   │   func2()    │        │  타이머, HTTP 요청 등 처리    │   │
│   │   func1()    │ ◄────  │                             │   │
│   │   main()     │        └─────────────────────────────┘   │
│   └──────────────┘                     │                    │
│          ▲                             │                    │
│          │                             ▼                    │
│          │         ┌───────────────────────────────────┐   │
│          │         │      Microtask Queue              │   │
│          │ ◄────── │  (Promise.then, queueMicrotask)   │   │
│          │         │  높은 우선순위                      │   │
│          │         └───────────────────────────────────┘   │
│          │                             │                    │
│   ┌──────┴──────┐                      │                    │
│   │ Event Loop  │ ◄────────────────────┘                   │
│   │  (감시자)    │                                          │
│   └──────┬──────┘                                          │
│          │                                                  │
│          │         ┌───────────────────────────────────┐   │
│          └───────► │        Task Queue (Macrotask)     │   │
│                    │  (setTimeout, setInterval, I/O)   │   │
│                    │  낮은 우선순위                      │   │
│                    └───────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**실행 순서**:

```javascript
console.log('1: 동기');

setTimeout(() => {
  console.log('2: Macrotask (setTimeout)');
}, 0);

Promise.resolve().then(() => {
  console.log('3: Microtask (Promise)');
});

queueMicrotask(() => {
  console.log('4: Microtask (queueMicrotask)');
});

console.log('5: 동기');

// 출력 순서:
// 1: 동기
// 5: 동기
// 3: Microtask (Promise)
// 4: Microtask (queueMicrotask)
// 2: Macrotask (setTimeout)
```

**이벤트 루프 단계**:

| 단계 | 설명 | 예시 |
|------|------|------|
| 1. 콜 스택 실행 | 동기 코드 실행 | 함수 호출, 계산 |
| 2. 마이크로태스크 큐 | 콜 스택 비면 전부 실행 | Promise.then, async/await |
| 3. 렌더링 | 필요시 화면 업데이트 | DOM 변경 반영 |
| 4. 매크로태스크 큐 | 하나씩 실행 | setTimeout, setInterval |
| 5. 반복 | 1번으로 돌아감 | 계속 순환 |

**복잡한 예제**:

```javascript
async function async1() {
  console.log('async1 start');
  await async2();
  console.log('async1 end');
}

async function async2() {
  console.log('async2');
}

console.log('script start');

setTimeout(() => {
  console.log('setTimeout');
}, 0);

async1();

new Promise(resolve => {
  console.log('promise1');
  resolve();
}).then(() => {
  console.log('promise2');
});

console.log('script end');

// 출력 순서:
// script start      (동기)
// async1 start      (동기)
// async2            (동기)
// promise1          (동기 - Promise 생성자)
// script end        (동기)
// async1 end        (마이크로태스크)
// promise2          (마이크로태스크)
// setTimeout        (매크로태스크)
```

---

## 트레이드오프

### var vs let vs const

| 특성 | var | let | const |
|------|-----|-----|-------|
| 스코프 | 함수 | 블록 | 블록 |
| 재선언 | 가능 | 불가 | 불가 |
| 재할당 | 가능 | 가능 | 불가 |
| 호이스팅 | undefined | TDZ | TDZ |
| 권장도 | 사용 자제 | 재할당 필요 시 | **기본 선택** |

### 클래스 vs 프로토타입

| 특성 | 클래스 | 프로토타입 |
|------|--------|------------|
| 문법 | 직관적 | 복잡함 |
| 호이스팅 | TDZ | 함수 호이스팅 |
| 내부 동작 | 프로토타입 기반 | 직접 조작 |
| 사용 권장 | 일반적 상황 | 동적 상속 필요 시 |

---

## 실무 적용

### 메모리 누수 방지

```javascript
// 클로저로 인한 메모리 누수 방지
function setupHandler() {
  const largeData = new Array(1000000).fill('data');

  // 문제: largeData가 계속 참조됨
  element.addEventListener('click', function() {
    console.log(largeData.length);
  });

  // 해결: 필요한 값만 클로저에 포함
  const dataLength = largeData.length;
  element.addEventListener('click', function() {
    console.log(dataLength);
  });
}

// 이벤트 리스너 정리
function Component() {
  const handler = () => { /* ... */ };

  element.addEventListener('click', handler);

  // 정리 함수
  return () => {
    element.removeEventListener('click', handler);
  };
}
```

### 비동기 패턴 선택

```yaml
callback:
  use_when:
    - Node.js 레거시 API
    - 간단한 비동기 작업
  avoid_when:
    - 여러 비동기 작업 체이닝
    - 에러 처리가 복잡한 경우

promise:
  use_when:
    - 비동기 작업 체이닝
    - 여러 작업 병렬 실행 (Promise.all)
  avoid_when:
    - 매우 단순한 콜백

async_await:
  use_when:
    - 복잡한 비동기 흐름
    - 가독성 중요
    - 에러 처리 (try/catch)
  best_practice:
    - 기본 선택으로 권장
```

---

## 면접 포인트

**Q**: 클로저란 무엇이며 어디에 활용되는가?

**A**: 클로저는 함수와 그 함수가 선언된 렉시컬 환경의 조합이다. 외부 함수 실행이 종료된 후에도 내부 함수가 외부 변수에 접근할 수 있다. 데이터 프라이버시(모듈 패턴), 함수 팩토리, 콜백에서 상태 유지 등에 활용된다.

**Q**: this 바인딩 규칙을 설명하라.

**A**: this는 호출 방식에 따라 결정된다. 우선순위는 new 바인딩 > 명시적 바인딩(call/apply/bind) > 암시적 바인딩(객체 메서드) > 기본 바인딩(전역/undefined)이다. 화살표 함수는 자신만의 this가 없고 렉시컬 스코프의 this를 상속한다.

**Q**: 이벤트 루프와 태스크 큐의 차이는?

**A**: 이벤트 루프는 콜 스택이 비어있을 때 태스크 큐의 작업을 가져오는 메커니즘이다. 마이크로태스크 큐(Promise.then)는 매크로태스크 큐(setTimeout)보다 우선순위가 높아 콜 스택이 빌 때마다 전부 실행된다. 매크로태스크는 하나씩 실행된다.

**Q**: 프로토타입 체인이란?

**A**: 객체에서 속성을 찾을 때 자신에게 없으면 프로토타입 링크를 따라 상위 객체에서 찾는 메커니즘이다. 모든 체인은 최종적으로 Object.prototype을 거쳐 null에서 끝난다. ES6 클래스도 내부적으로 프로토타입 기반으로 동작한다.

---

## 참고 자료

- [MDN - Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures)
- [MDN - this](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this)
- [JavaScript.info - Event Loop](https://javascript.info/event-loop)
- [MDN - Inheritance and the prototype chain](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Inheritance_and_the_prototype_chain)
