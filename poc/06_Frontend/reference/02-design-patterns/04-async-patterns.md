# 비동기 패턴 (Async Patterns)

## 개요

**정의**: 비동기 패턴은 메인 스레드를 차단하지 않고 장시간 작업을 백그라운드에서 실행하기 위한 설계 패턴이다.

**목적**: 콜백 지옥을 해결하고 비동기 코드를 동기 코드처럼 읽기 쉽게 작성하여 유지보수성을 향상시킨다.

---

## 핵심 개념

### 동기 vs 비동기

| 특성 | 동기 (Synchronous) | 비동기 (Asynchronous) |
|------|-------------------|----------------------|
| 실행 방식 | 블로킹 (순차 실행) | 논블로킹 (병렬 가능) |
| 제어 흐름 | 함수 완료 후 반환 | 즉시 반환, 백그라운드 실행 |
| 적합한 작업 | CPU 연산 | I/O, 네트워크, 타이머 |
| 메인 스레드 | 점유 | 자유 |

### 비동기 발전 역사

```
콜백 (Callback)
    │
    ├─ 문제: 콜백 지옥, 에러 처리 중복
    │
    ↓
Promise (ES2015)
    │
    ├─ 해결: 체이닝, 단일 에러 핸들링
    │
    ↓
async/await (ES2017)
    │
    └─ 해결: 동기 코드처럼 작성 가능
```

---

## Promise 패턴

### Promise 기본

Promise는 비동기 작업의 최종 완료 또는 실패를 나타내는 객체이다.

**세 가지 상태**:
- **Pending**: 초기 상태, 작업 진행 중
- **Fulfilled**: 작업 성공적으로 완료
- **Rejected**: 작업 실패

```javascript
function makeRequest(url) {
    return new Promise((resolve, reject) => {
        fetch(url)
            .then(response => response.json())
            .then(data => resolve(data))
            .catch(error => reject(error));
    });
}

makeRequest('http://example.com/')
    .then(data => console.log(data))
    .catch(error => console.error(error));
```

### 1. Promise Chaining (체이닝)

순차적 비동기 작업을 연결하여 콜백 지옥을 해결한다.

```javascript
makeRequest('http://example.com/')
    .then(data => processData(data))
    .then(processedData => saveData(processedData))
    .then(result => console.log(result))
    .catch(error => console.error(error));
```

**체이닝의 장점**:
- 콜백 지옥 해결
- 순차적 비동기 작업 명확히 표현
- 단일 catch로 에러 처리

### 2. Promise.all (병렬 실행)

모든 Promise가 성공해야 결과를 반환한다.

```javascript
Promise.all([
    makeRequest('http://example.com/1'),
    makeRequest('http://example.com/2'),
    makeRequest('http://example.com/3')
]).then(([data1, data2, data3]) => {
    console.log(data1, data2, data3);
}).catch(error => {
    console.error(error);
});
```

### 3. Promise.allSettled (부분 실패 허용)

모든 결과(성공/실패 모두)를 반환한다.

```javascript
Promise.allSettled([
    makeRequest('http://example.com/1'),
    makeRequest('http://example.com/2')
]).then(results => {
    results.forEach(result => {
        if (result.status === 'fulfilled') {
            console.log('Success:', result.value);
        } else {
            console.log('Failed:', result.reason);
        }
    });
});
```

### 4. Promise.race (경쟁)

가장 먼저 완료된 Promise 결과를 반환한다.

```javascript
// 타임아웃 구현에 활용
function withTimeout(promise, ms) {
    const timeout = new Promise((_, reject) => {
        setTimeout(() => reject(new Error('Timeout')), ms);
    });
    return Promise.race([promise, timeout]);
}

withTimeout(makeRequest('http://example.com/'), 5000)
    .then(data => console.log(data))
    .catch(error => console.error(error));
```

### 5. Promise Memoization (메모이제이션)

중복 요청을 방지하여 성능을 최적화한다.

```javascript
const cache = new Map();

function memoizedMakeRequest(url) {
    if (cache.has(url)) {
        return Promise.resolve(cache.get(url));
    }

    return new Promise((resolve, reject) => {
        fetch(url)
            .then(response => response.json())
            .then(data => {
                cache.set(url, data);
                resolve(data);
            })
            .catch(error => reject(error));
    });
}
```

### 6. Promise Retry (재시도)

실패 시 지수 백오프를 적용하여 재시도한다.

```javascript
function makeRequestWithBackoff(url, maxAttempts = 3) {
    let attempts = 0;

    const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

    const makeRequest = async () => {
        try {
            const response = await fetch(url);
            return await response.json();
        } catch (error) {
            attempts++;
            if (attempts >= maxAttempts) {
                throw new Error(`Request failed after ${maxAttempts} attempts.`);
            }
            await delay(Math.pow(2, attempts) * 1000);
            return makeRequest();
        }
    };

    return makeRequest();
}
```

### Promise 메서드 비교

| 메서드 | 동작 | 반환 시점 |
|--------|------|----------|
| `Promise.all` | 모든 Promise 병렬 실행 | 모두 fulfilled 또는 하나라도 rejected |
| `Promise.allSettled` | 모든 Promise 병렬 실행 | 모두 settled (성공/실패 모두 포함) |
| `Promise.race` | 모든 Promise 병렬 실행 | 가장 먼저 settled된 것 |
| `Promise.any` | 모든 Promise 병렬 실행 | 가장 먼저 fulfilled된 것 |

---

## async/await 패턴

### async/await 기본

async/await는 ES2017에서 도입된 문법으로, Promise 기반 비동기 코드를 동기 코드처럼 작성할 수 있게 한다.

```javascript
async function makeRequest(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error);
        throw error;
    }
}
```

**핵심 특징**:
- async 함수는 항상 Promise를 반환
- await는 Promise가 settle될 때까지 실행을 일시 중지
- try-catch로 동기 코드처럼 에러 처리

### 1. async Function Composition (함수 합성)

작은 async 함수를 합성하여 복잡한 로직을 구성한다.

```javascript
async function makeRequest(url) {
    const response = await fetch(url);
    return await response.json();
}

async function processData(data) {
    return { ...data, processed: true };
}

async function saveData(data) {
    return { ...data, saved: true };
}

// 파이프 유틸리티
const asyncPipe = (...fns) => async (input) => {
    let result = input;
    for (const fn of fns) {
        result = await fn(result);
    }
    return result;
};

const pipeline = asyncPipe(makeRequest, processData, saveData);
pipeline('http://example.com/').then(console.log);
```

### 2. async Parallelism (병렬 실행)

독립적인 작업은 Promise.all로 병렬 처리한다.

```javascript
async function fetchAllData() {
    const [users, products, orders] = await Promise.all([
        fetch('/api/users').then(r => r.json()),
        fetch('/api/products').then(r => r.json()),
        fetch('/api/orders').then(r => r.json())
    ]);

    return { users, products, orders };
}
```

### 3. async Sequential Execution (순차 실행)

의존성 있는 작업은 순차적으로 실행한다.

```javascript
async function fetchSequential() {
    const user = await fetchUser(userId);
    const profile = await fetchProfile(user.id);
    const posts = await fetchPosts(profile.id);

    return { user, profile, posts };
}
```

### 4. async Iteration (비동기 이터레이션)

for-await-of로 비동기 이터러블을 순회한다.

```javascript
async function* fetchPages(urls) {
    for (const url of urls) {
        const response = await fetch(url);
        const data = await response.json();
        yield data;
    }
}

async function processAllPages() {
    const urls = [
        'http://example.com/page/1',
        'http://example.com/page/2',
        'http://example.com/page/3'
    ];

    for await (const page of fetchPages(urls)) {
        console.log('Received page:', page);
    }
}
```

### 5. async Error Handling (에러 처리)

에러 래퍼 유틸리티로 일관된 에러 처리를 구현한다.

```javascript
async function safeAwait(promise) {
    try {
        const data = await promise;
        return [null, data];
    } catch (error) {
        return [error, null];
    }
}

async function main() {
    const [error, data] = await safeAwait(makeRequest('http://example.com/'));

    if (error) {
        console.error('Error:', error);
        return;
    }

    console.log('Data:', data);
}
```

### 6. async Memoization (메모이제이션)

TTL(Time-To-Live)을 적용한 캐싱을 구현한다.

```javascript
function createMemoizedFetch(ttl = 60000) {
    const cache = new Map();

    return async function(url) {
        const cached = cache.get(url);

        if (cached && Date.now() - cached.timestamp < ttl) {
            return cached.data;
        }

        const response = await fetch(url);
        const data = await response.json();

        cache.set(url, {
            data,
            timestamp: Date.now()
        });

        return data;
    };
}

const memoizedFetch = createMemoizedFetch(30000);
```

### 7. async Decorator (데코레이터)

로깅, 타임아웃, 재시도 등의 추가 동작을 래핑한다.

```javascript
// 로깅 데코레이터
function asyncLogger(fn) {
    return async function(...args) {
        console.log(`[${fn.name}] Starting...`);
        const startTime = Date.now();

        try {
            const result = await fn(...args);
            const duration = Date.now() - startTime;
            console.log(`[${fn.name}] Completed in ${duration}ms`);
            return result;
        } catch (error) {
            console.error(`[${fn.name}] Failed:`, error.message);
            throw error;
        }
    };
}

// 타임아웃 데코레이터
function withTimeout(fn, ms) {
    return async function(...args) {
        const timeoutPromise = new Promise((_, reject) => {
            setTimeout(() => reject(new Error('Timeout')), ms);
        });
        return Promise.race([fn(...args), timeoutPromise]);
    };
}

// 재시도 데코레이터
function withRetry(fn, maxRetries = 3) {
    return async function(...args) {
        for (let i = 0; i < maxRetries; i++) {
            try {
                return await fn(...args);
            } catch (error) {
                if (i === maxRetries - 1) throw error;
            }
        }
    };
}

// 데코레이터 조합
const fetchData = asyncLogger(
    withTimeout(
        withRetry(async (url) => {
            const response = await fetch(url);
            return response.json();
        }, 3),
        5000
    )
);
```

---

## 실행 전략 선택

### 병렬 vs 순차 실행

```
비동기 작업들
    │
    ├─ 작업 간 의존성 있음?
    │       └─ Yes → 순차 실행 (for...of + await)
    │
    └─ No → 실패 시 모두 중단?
            ├─ Yes → Promise.all
            └─ No → Promise.allSettled
```

### 흔한 실수

```javascript
// ❌ forEach 안에서 await (동작 안 함)
urls.forEach(async (url) => {
    const data = await fetch(url);
});

// ✅ for...of 사용 (순차 실행)
for (const url of urls) {
    const data = await fetch(url);
}

// ✅ Promise.all 사용 (병렬 실행)
const results = await Promise.all(
    urls.map(url => fetch(url))
);
```

---

## 트레이드오프

### Promise

| 장점 | 단점 |
|------|------|
| 콜백 지옥 해결 | 여전히 체이닝 문법 필요 |
| 단일 에러 핸들링 | 디버깅 시 스택 트레이스 복잡 |
| 병렬/순차 실행 제어 | 취소 기능 미지원 |

### async/await

| 장점 | 단점 |
|------|------|
| 동기 코드처럼 읽기 쉬움 | async 함수 내부에서만 사용 |
| 직관적인 에러 처리 | 무분별한 await로 성능 저하 가능 |
| 디버깅 용이 | ES2017+ 환경 필요 |

---

## 실무 적용

### 베스트 프랙티스

```yaml
코드_구조:
  - 작은 단위의 async 함수로 분리
  - 함수 합성으로 복잡한 로직 구성
  - 에러 처리는 호출부에서 중앙 관리

성능_최적화:
  - 독립적인 작업은 Promise.all로 병렬화
  - 불필요한 await 제거
  - 메모이제이션으로 중복 요청 방지

에러_처리:
  - try-catch로 명확한 에러 경계 설정
  - 재시도 로직에 최대 횟수와 백오프 적용
  - finally로 리소스 정리 보장
```

### 안티패턴 피하기

```javascript
// ❌ Promise 생성자 안티패턴
new Promise((resolve, reject) => {
    fetch(url)
        .then(response => resolve(response))
        .catch(error => reject(error));
});

// ✅ fetch는 이미 Promise 반환
fetch(url);

// ❌ .then() 안에서 .catch() 누락
makeRequest(url).then(data => {
    return anotherRequest(data);
});

// ✅ 체인 끝에 catch 추가
makeRequest(url)
    .then(data => anotherRequest(data))
    .catch(error => console.error(error));
```

---

## 면접 포인트

**Q**: Promise의 세 가지 상태는 무엇인가?

**A**: Promise는 pending(대기), fulfilled(이행), rejected(거부) 세 가지 상태를 가진다. pending은 초기 상태이며, 비동기 작업이 완료되면 fulfilled(성공) 또는 rejected(실패) 상태로 전환된다. 상태가 한번 변경되면 다시 변경되지 않는다(불변).

**Q**: Promise.all과 Promise.allSettled의 차이는?

**A**: Promise.all은 모든 Promise가 성공해야 결과를 반환하고, 하나라도 실패하면 전체가 실패한다. Promise.allSettled는 모든 Promise의 결과(성공/실패 모두)를 배열로 반환하며, 부분 실패를 허용해야 하는 상황에 적합하다.

**Q**: async/await에서 병렬 실행은 어떻게 하는가?

**A**: 독립적인 비동기 작업을 병렬로 실행하려면 await를 순차적으로 사용하는 대신 Promise.all과 함께 사용한다. `const [a, b, c] = await Promise.all([fetchA(), fetchB(), fetchC()])`처럼 작성하면 세 요청이 동시에 시작되어 총 소요 시간이 가장 긴 요청 시간과 같아진다.

---

## 참고 자료

- [MDN: Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)
- [MDN: async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)
- [JavaScript.info: Promises, async/await](https://javascript.info/async)
- [TC39: Top-level await](https://github.com/tc39/proposal-top-level-await)
