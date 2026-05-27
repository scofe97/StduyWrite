# 행동 패턴 (Behavioral Patterns)

## 개요

**정의**: 행동 패턴은 시스템 내 서로 다른 객체 간의 통신을 개선하거나 간소화하는 패턴이다.

**목적**: 객체 간의 공통 통신 패턴을 식별하고, 통신 책임을 여러 객체에 분배하며, 행동을 그 행동을 수행하는 객체로부터 추상화한다.

---

## 핵심 개념

### 패턴 선택 가이드

```
객체 간 통신 문제 발생
    │
    ├─ 1:N 알림이 필요?
    │       └─ Yes → Observer 패턴
    │
    ├─ 중앙 집중식 조정 필요?
    │       └─ Yes → Mediator 패턴
    │
    └─ 요청을 객체로 캡슐화?
            └─ Yes → Command 패턴
```

### 패턴 비교

| 패턴 | 핵심 목적 | 통신 방식 | 결합도 |
|------|----------|----------|--------|
| Observer | 상태 변경 알림 | 1:N 직접 | 중간 |
| Pub/Sub | 이벤트 브로드캐스트 | 채널 통한 간접 | 낮음 |
| Mediator | 중앙 집중 조정 | 중재자 통한 간접 | 낮음 |
| Command | 요청 캡슐화 | 명령 객체 | 낮음 |

---

## 구현 패턴

### 1. Observer Pattern (옵저버 패턴)

**목적**: 한 객체가 변경될 때 다른 객체들에게 알림

**구성 요소**:

| 구성 요소 | 역할 |
|----------|------|
| **Subject** | observer 목록 유지, 추가/제거 관리 |
| **Observer** | Subject 상태 변경 시 호출되는 update 인터페이스 |
| **ConcreteSubject** | 상태 변경 시 observer에게 알림 |
| **ConcreteObserver** | ConcreteSubject 참조 저장, update 구현 |

**구현**:

```javascript
// ObserverList: Observer 관리
class ObserverList {
    constructor() {
        this.observerList = [];
    }

    add(obj) {
        return this.observerList.push(obj);
    }

    count() {
        return this.observerList.length;
    }

    get(index) {
        if (index > -1 && index < this.observerList.length) {
            return this.observerList[index];
        }
    }

    indexOf(obj, startIndex = 0) {
        let i = startIndex;
        while (i < this.observerList.length) {
            if (this.observerList[i] === obj) return i;
            i++;
        }
        return -1;
    }

    removeAt(index) {
        this.observerList.splice(index, 1);
    }
}

// Subject: 알림 발송자
class Subject {
    constructor() {
        this.observers = new ObserverList();
    }

    addObserver(observer) {
        this.observers.add(observer);
    }

    removeObserver(observer) {
        this.observers.removeAt(this.observers.indexOf(observer, 0));
    }

    notify(context) {
        const count = this.observers.count();
        for (let i = 0; i < count; i++) {
            this.observers.get(i).update(context);
        }
    }
}

// Observer: 알림 수신자
class Observer {
    constructor() {}
    update() {
        // 하위 클래스에서 구현
    }
}
```

**실제 사용 예제**:

```javascript
// ConcreteSubject
class NewsAgency extends Subject {
    constructor() {
        super();
        this.news = '';
    }

    setNews(news) {
        this.news = news;
        this.notify(news);
    }
}

// ConcreteObserver
class NewsChannel extends Observer {
    constructor(name) {
        super();
        this.name = name;
    }

    update(news) {
        console.log(`${this.name} received: ${news}`);
    }
}

// 사용
const agency = new NewsAgency();
const cnn = new NewsChannel('CNN');
const bbc = new NewsChannel('BBC');

agency.addObserver(cnn);
agency.addObserver(bbc);

agency.setNews('Breaking News!');
// CNN received: Breaking News!
// BBC received: Breaking News!
```

---

### Observer vs Publish/Subscribe

| 측면 | Observer | Publish/Subscribe |
|------|----------|-------------------|
| **결합도** | Subject와 Observer가 서로 인지 | Publisher와 Subscriber가 서로 모름 |
| **통신** | 직접 통신 | 이벤트 채널 통해 간접 통신 |
| **유연성** | 낮음 | 높음 |
| **사용 사례** | UI 컴포넌트 | 마이크로서비스, 이벤트 버스 |

**Publish/Subscribe 구현**:

```javascript
class PubSub {
    constructor() {
        this.topics = {};
        this.subUid = -1;
    }

    publish(topic, args) {
        if (!this.topics[topic]) return false;

        const subscribers = this.topics[topic];
        let len = subscribers ? subscribers.length : 0;

        while (len--) {
            subscribers[len].func(topic, args);
        }
        return this;
    }

    subscribe(topic, func) {
        if (!this.topics[topic]) {
            this.topics[topic] = [];
        }

        const token = (++this.subUid).toString();
        this.topics[topic].push({ token, func });
        return token;
    }

    unsubscribe(token) {
        for (const m in this.topics) {
            if (this.topics[m]) {
                for (let i = 0; i < this.topics[m].length; i++) {
                    if (this.topics[m][i].token === token) {
                        this.topics[m].splice(i, 1);
                        return token;
                    }
                }
            }
        }
        return this;
    }
}

// 사용
const pubsub = new PubSub();

// 구독
const token = pubsub.subscribe('news', (topic, data) => {
    console.log(`Topic: ${topic}, Data: ${data}`);
});

// 발행
pubsub.publish('news', 'Hello World!');
// Topic: news, Data: Hello World!

// 구독 해제
pubsub.unsubscribe(token);
```

---

### 2. Mediator Pattern (중재자 패턴)

**목적**: 한 객체가 이벤트 발생 시 다른 객체 집합에 알림 (중앙 집중식 통신)

**실세계 비유**:

| 비유 | 설명 |
|------|------|
| **공항 관제탑** | 비행기들이 서로 직접 통신하지 않고 관제탑을 통해 통신 |
| **DOM 이벤트 버블링** | document가 중재자 역할 |
| **채팅방** | 서버가 메시지를 중재 |

**구현**:

```javascript
class Mediator {
    constructor() {
        this.colleagues = {};
    }

    register(name, colleague) {
        this.colleagues[name] = colleague;
        colleague.setMediator(this);
    }

    send(message, from, to) {
        if (to) {
            // 특정 대상에게 전송
            this.colleagues[to].receive(message, from);
        } else {
            // 모든 참여자에게 브로드캐스트
            for (const name in this.colleagues) {
                if (name !== from) {
                    this.colleagues[name].receive(message, from);
                }
            }
        }
    }
}

class Colleague {
    constructor(name) {
        this.name = name;
        this.mediator = null;
    }

    setMediator(mediator) {
        this.mediator = mediator;
    }

    send(message, to) {
        this.mediator.send(message, this.name, to);
    }

    receive(message, from) {
        console.log(`${this.name} received from ${from}: ${message}`);
    }
}

// 사용
const mediator = new Mediator();
const user1 = new Colleague('Alice');
const user2 = new Colleague('Bob');
const user3 = new Colleague('Charlie');

mediator.register('Alice', user1);
mediator.register('Bob', user2);
mediator.register('Charlie', user3);

user1.send('Hello everyone!');
// Bob received from Alice: Hello everyone!
// Charlie received from Alice: Hello everyone!

user2.send('Hi Alice!', 'Alice');
// Alice received from Bob: Hi Alice!
```

---

### Mediator vs Event Aggregator

| 측면 | Event Aggregator | Mediator |
|------|------------------|----------|
| **로직 위치** | 이벤트 발생/처리 객체 | Mediator 자체 |
| **목적** | 이벤트 전달 | 워크플로우 조정 |
| **통신 모델** | Fire and Forget | 알려진 입력/출력 처리 |
| **결합도** | 매우 느슨 | 느슨 |
| **복잡도** | 낮음 | 높음 |

**사용 시기**:

- **Event Aggregator**: 너무 많은 객체를 직접 리스닝해야 할 때, 전혀 관련 없는 객체들이 있을 때
- **Mediator**: 간접적인 작업 관계가 있을 때, 비즈니스 로직/워크플로우가 상호작용을 지시해야 할 때

**Express.js Middleware (현대적 Mediator)**:

```javascript
const app = require("express")();

// Middleware 1: 헤더 추가
app.use("/", (req, res, next) => {
    req.headers["test-header"] = 1234;
    next();
});

// Middleware 2: 로깅
app.use("/", (req, res, next) => {
    console.log(`Request has test header: ${!!req.headers["test-header"]}`);
    next();
});

// Middleware 3: 응답
app.get("/", (req, res) => {
    res.send("Hello World!");
});

app.listen(3000);
```

---

### 3. Command Pattern (커맨드 패턴)

**목적**: 메서드 호출, 요청, 작업을 단일 객체로 캡슐화

**구성 요소**:

| 구성 요소 | 역할 |
|----------|------|
| **Command** | 실행 인터페이스 정의 |
| **ConcreteCommand** | 실제 실행 로직 |
| **Invoker** | Command 실행 요청 |
| **Receiver** | 실제 작업 수행 |

**기본 구현**:

```javascript
const CarManager = {
    requestInfo(model, id) {
        return `The information for ${model} with ID ${id} is foobar`;
    },
    buyVehicle(model, id) {
        return `You have successfully purchased Item ${id}, a ${model}`;
    },
    arrangeViewing(model, id) {
        return `You have booked a viewing of ${model} (${id})`;
    },
};

// Command 실행 메서드 추가
CarManager.execute = function(name, ...args) {
    return (
        CarManager[name] &&
        CarManager[name].apply(CarManager, args)
    );
};

// 사용
console.log(CarManager.execute('arrangeViewing', 'Ferrari', '14523'));
// You have booked a viewing of Ferrari (14523)
```

**클래스 기반 구현 (Undo 지원)**:

```javascript
// Command 인터페이스
class Command {
    execute() {}
    undo() {}
}

// Receiver
class Light {
    on() { console.log('Light is ON'); }
    off() { console.log('Light is OFF'); }
}

// ConcreteCommand
class LightOnCommand extends Command {
    constructor(light) {
        super();
        this.light = light;
    }
    execute() { this.light.on(); }
    undo() { this.light.off(); }
}

class LightOffCommand extends Command {
    constructor(light) {
        super();
        this.light = light;
    }
    execute() { this.light.off(); }
    undo() { this.light.on(); }
}

// Invoker
class RemoteControl {
    constructor() {
        this.history = [];
    }

    submit(command) {
        command.execute();
        this.history.push(command);
    }

    undo() {
        const command = this.history.pop();
        if (command) {
            command.undo();
        }
    }
}

// 사용
const light = new Light();
const lightOn = new LightOnCommand(light);
const lightOff = new LightOffCommand(light);

const remote = new RemoteControl();

remote.submit(lightOn);   // Light is ON
remote.submit(lightOff);  // Light is OFF
remote.undo();            // Light is ON
```

---

## 트레이드오프

### Observer/Pub-Sub

| 장점 | 단점 |
|------|------|
| 애플리케이션 부분 간 관계 재고 | 특정 부분이 기능하는지 보장 어려움 |
| 느슨한 결합 | 업데이트 의존성 추적 어려움 |
| 동적 관계 | 디버깅 복잡 |

### Command

| 장점 | 설명 |
|------|------|
| 명령 분리 | 실행과 구현 분리 |
| 유연성 | 구체 클래스 교체 용이 |
| 매개변수화 | 작업을 객체로 전달 가능 |
| 실행 취소 | undo 기능 구현 가능 |
| 큐잉 | 명령 저장 및 지연 실행 |

---

## 실무 적용

### React에서의 행동 패턴

| 패턴 | React 구현 |
|------|-----------|
| Observer | useEffect + dependencies |
| Pub/Sub | EventEmitter, RxJS |
| Mediator | Redux middleware, Context |
| Command | useReducer actions |

### 패턴 선택 체크리스트

```yaml
observer_pattern:
  use_when:
    - 상태 변경 시 여러 객체 업데이트
    - UI 컴포넌트 간 동기화
    - 이벤트 기반 시스템
  avoid_when:
    - 단순 함수 호출로 충분
    - 관계가 1:1

pubsub_pattern:
  use_when:
    - 완전히 분리된 모듈 간 통신
    - 마이크로서비스 아키텍처
  avoid_when:
    - 직접 참조가 더 명확

mediator_pattern:
  use_when:
    - 복잡한 객체 간 상호작용
    - 워크플로우 조정 필요
  avoid_when:
    - 단순 이벤트 전달

command_pattern:
  use_when:
    - 실행 취소/재실행 필요
    - 작업 큐잉/로깅 필요
  avoid_when:
    - 단순 메서드 호출
```

### 안티패턴 피하기

| 문제 | 해결책 |
|------|--------|
| Observer 메모리 누수 (구독 해제 안 함) | 컴포넌트 언마운트 시 unsubscribe |
| Mediator God Object (너무 많은 로직) | 책임 분리, 여러 Mediator 사용 |
| Command 과용 (모든 메서드 래핑) | 실행 취소가 필요한 경우만 적용 |

### 메모리 누수 방지

```javascript
// React에서 Observer 패턴 사용 시
useEffect(() => {
    const subscription = observable.subscribe(handler);

    // 클린업 함수에서 반드시 해제
    return () => {
        subscription.unsubscribe();
    };
}, [observable]);
```

---

## 면접 포인트

**Q**: Observer 패턴과 Publish/Subscribe 패턴의 차이는?

**A**: Observer 패턴은 Subject와 Observer가 서로를 직접 알고 있어 직접 통신한다. Publish/Subscribe 패턴은 Publisher와 Subscriber가 서로를 모르며, 이벤트 채널(Topic)을 통해 간접 통신한다. Pub/Sub이 더 느슨한 결합을 제공하므로 마이크로서비스나 분산 시스템에 적합하다.

**Q**: Mediator 패턴은 언제 사용하는가?

**A**: Mediator 패턴은 여러 객체 간의 복잡한 상호작용을 중앙에서 조정해야 할 때 사용한다. 공항 관제탑이 비행기들 간의 통신을 중재하는 것처럼, 객체들이 서로 직접 참조하지 않고 Mediator를 통해 통신하게 한다. Express.js의 미들웨어 체인이 현대적 Mediator 패턴의 예다.

**Q**: Command 패턴의 장점은 무엇인가?

**A**: Command 패턴은 요청을 객체로 캡슐화하여 실행과 구현을 분리한다. 주요 장점은 실행 취소/재실행 기능 구현, 명령 큐잉 및 로깅, 매크로 명령 조합이다. 텍스트 에디터의 Undo/Redo 기능이나 트랜잭션 처리에서 활용된다.

---

## 참고 자료

- GoF, "Design Patterns: Elements of Reusable Object-Oriented Software"
- Dustin Diaz, Ross Harmes, "Pro JavaScript Design Patterns"
- [RxJS Documentation](https://rxjs.dev/)
- [Express.js Middleware](https://expressjs.com/en/guide/using-middleware.html)
