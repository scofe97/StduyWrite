# Chapter 2. TypeScript 시작하기 (Getting Started with TypeScript)

---

### 📌 핵심 요약
> TypeScript는 JavaScript의 **슈퍼셋**으로, 풍부한 타입 시스템을 제공하여 개발 단계에서 타입 오류를 조기에 발견할 수 있다. 타입 추론(Type Inference)을 통해 모든 곳에 타입을 명시하지 않아도 되며, **타입 별칭(Type Alias)**과 **유니온 타입(Union Type)**으로 복잡한 타입을 정의할 수 있다. React 컴포넌트의 props와 state에 타입을 적용하면 컴파일 시점에 오류를 잡아 런타임 버그를 방지할 수 있다.

---

### 🎯 학습 목표
- TypeScript의 장점과 JavaScript와의 관계를 이해한다
- 기본 TypeScript 타입(number, string, Date, unknown, any)을 사용할 수 있다
- 타입 별칭과 유니온 타입으로 커스텀 타입을 생성할 수 있다
- TypeScript 컴파일러(tsc)와 tsconfig.json 설정을 이해한다
- React 컴포넌트에 Props와 State 타입을 적용할 수 있다

---

### 📖 본문 정리

#### 1. TypeScript의 장점

##### TypeScript란?
TypeScript는 JavaScript의 슈퍼셋으로, 브라우저에서 직접 실행되지 않고 JavaScript로 **트랜스파일**되어야 한다.

```
┌─────────────────────────────────────────────────────┐
│                    TypeScript                        │
│  ┌───────────────────────────────────────────────┐  │
│  │                 JavaScript                     │  │
│  │   (모든 JS 기능은 TS에서 사용 가능)            │  │
│  └───────────────────────────────────────────────┘  │
│  + 풍부한 타입 시스템                               │
│  + 컴파일 시점 타입 체크                            │
│  + IntelliSense 지원                               │
└─────────────────────────────────────────────────────┘
```

##### 주요 장점

| 장점 | 설명 |
|------|------|
| **조기 오류 발견** | 개발 중 타입 오류를 즉시 감지 |
| **IntelliSense** | 코드 자동완성, 속성 목록 제공 |
| **리팩토링 지원** | 안전한 이름 변경, 코드 탐색 |
| **가독성 향상** | 타입 정보가 문서 역할 |

##### 타입 오류 조기 발견 예시

```typescript
// JavaScript (버그 감지 불가)
function calculateTotalPrice(product, quantity, discount) {
  const priceWithoutDiscount = product.price * quantity;  // 버그: price가 아니라 unitPrice!
  return priceWithoutDiscount - (priceWithoutDiscount * discount);
}

// TypeScript (즉시 오류 감지)
function calculateTotalPrice(
  product: { name: string; unitPrice: number },
  quantity: number,
  discount: number
) {
  const priceWithoutDiscount = product.price * quantity;  // ❌ 오류: 'price' 속성이 없음
  return priceWithoutDiscount - (priceWithoutDiscount * discount);
}
```

---

#### 2. JavaScript 타입의 한계

JavaScript는 **느슨한 타입(Loosely Typed)** 언어:

```javascript
let score = 9;
console.log(typeof score);  // "number"

score = "ten";
console.log(typeof score);  // "string" - 타입이 변경됨!
```

**JavaScript 타입의 문제점**:
- 최소한의 타입만 제공 (string, number, boolean, object 등)
- 변수 타입이 런타임에 변경 가능
- `Date` 객체도 `typeof`로는 "object"로만 표시

---

#### 3. 기본 TypeScript 타입

##### 타입 어노테이션 (Type Annotation)

```typescript
// 변수에 타입 지정
let unitPrice: number;
unitPrice = 500;
unitPrice = "Table";  // ❌ 오류: string을 number에 할당 불가

// 함수 매개변수와 반환 타입
function getTotal(
  unitPrice: number,
  quantity: number,
  discount: number
): number {
  const priceWithoutDiscount = unitPrice * quantity;
  return priceWithoutDiscount - (priceWithoutDiscount * discount);
}
```

##### 타입 추론 (Type Inference)

TypeScript는 할당된 값으로부터 타입을 자동 추론:

```typescript
let flag = false;        // boolean으로 추론
let score = 100;         // number로 추론
let name = "TypeScript"; // string으로 추론

flag = "table";  // ❌ 오류: string을 boolean에 할당 불가
```

> 💡 **실무 팁**: 타입 추론이 가능한 경우 타입 어노테이션 생략. 추론이 불가능한 경우에만 명시적 타입 사용.

##### Date 타입

```typescript
let today: Date;
today = new Date();

// 타입 추론 사용
let tomorrow = new Date();  // Date로 추론

// IntelliSense 지원
today.getFullYear();  // ✅ 자동완성 가능
today.addMonths(2);   // ❌ 오류: addMonths 메서드 없음
```

##### any 타입 (사용 자제)

```typescript
let flag;  // any로 추론 (타입 어노테이션/값 없음)
flag = false;
flag = "table";  // 오류 없음 - 타입 체크 무시됨
```

> ⚠️ **주의**: `any`는 타입 체크를 우회하므로 가능한 사용 자제

##### unknown 타입 (any의 대안)

```typescript
// any 사용 - 문제 감지 불가
fetch("https://api.example.com/data")
  .then((response) => response.json())
  .then((data) => {
    console.log(data.firstName);  // 오류 없음 (하지만 런타임 오류 가능)
  });

// unknown 사용 - 안전한 타입 체크
fetch("https://api.example.com/data")
  .then((response) => response.json())
  .then((data: unknown) => {
    console.log(data.firstName);  // ❌ 오류: unknown 타입에 접근 불가
  });
```

##### unknown 타입 좁히기 (Type Narrowing)

```typescript
// 타입 가드 함수 (Type Predicate)
function isCharacter(
  character: any
): character is { name: string } {
  return "name" in character;
}

fetch("https://swapi.dev/api/people/1")
  .then((response) => response.json())
  .then((data: unknown) => {
    if (isCharacter(data)) {
      console.log("name", data.name);  // ✅ data는 { name: string }으로 좁혀짐
    }
  });
```

##### 배열 타입

```typescript
// 방법 1: 대괄호 표기법
const numbers: number[] = [];
numbers.push(1);      // ✅
numbers.push("two");  // ❌ 오류

// 방법 2: 제네릭 표기법
const names: Array<string> = [];

// 타입 추론
const scores = [1, 2, 3];  // number[]로 추론
```

---

#### 4. 커스텀 타입 생성

##### 객체 타입 (Object Types)

```typescript
// 인라인 객체 타입
function calculateTotalPrice(
  product: { name: string; unitPrice: number },
  quantity: number
): number {
  return product.unitPrice * quantity;
}

// 선택적 속성 (Optional Properties)
const table: { name: string; unitPrice?: number } = {
  name: "Table",
  // unitPrice 생략 가능
};
```

##### 타입 별칭 (Type Alias)

```typescript
// 타입 별칭 정의
type Product = {
  name: string;
  unitPrice?: number;
};

// 재사용
let table: Product = { name: "Table" };
let chair: Product = { name: "Chair", unitPrice: 40 };
```

##### 타입 확장 (Intersection Types)

```typescript
type Product = { name: string; unitPrice?: number };

// & 연산자로 타입 확장
type DiscountedProduct = Product & { discount: number };

let chairOnSale: DiscountedProduct = {
  name: "Chair on Sale",
  unitPrice: 30,
  discount: 5,
};
```

##### 함수 타입 별칭

```typescript
// 함수 타입 정의
type Purchase = (quantity: number) => void;

type Product = {
  name: string;
  unitPrice?: number;
  purchase: Purchase;
};

let table: Product = {
  name: "Table",
  purchase: (quantity) => console.log(`Purchased ${quantity} tables`),
};

table.purchase(4);  // "Purchased 4 tables"
```

##### 유니온 타입 (Union Types)

```typescript
// 특정 문자열 값만 허용
type Level = "H" | "M" | "L";
let priority: Level = "H";  // ✅
priority = "X";             // ❌ 오류

// 여러 타입 허용
type RGB = "red" | "green" | "blue" | null;
let color: RGB = "red";
color = null;  // ✅ null도 허용

// 숫자 리터럴 유니온
type OneToThree = 1 | 2 | 3;
let rating: OneToThree = 2;  // ✅
rating = 4;                   // ❌ 오류
```

---

#### 5. TypeScript 컴파일러 (tsc)

##### 프로젝트 설정

```json
// package.json
{
  "name": "tsc-play",
  "dependencies": {
    "typescript": "*"
  },
  "scripts": {
    "build": "tsc"
  }
}
```

##### tsconfig.json 핵심 설정

```json
{
  "compilerOptions": {
    "outDir": "dist",           // 출력 폴더
    "target": "esnext",         // JS 버전 (최신)
    "module": "esnext",         // 모듈 시스템
    "lib": ["DOM", "esnext"],   // 타입 라이브러리
    "strict": true,             // 엄격한 타입 체크
    "jsx": "react",             // JSX 트랜스파일
    "moduleResolution": "node", // 모듈 해석 방식
    "noEmitOnError": true       // 오류 시 JS 생성 안 함
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "build"]
}
```

| 옵션 | 설명 |
|------|------|
| `outDir` | 트랜스파일된 JS 출력 폴더 |
| `target` | 출력 JS 버전 (es5, es6, esnext 등) |
| `strict` | 가장 엄격한 타입 체크 활성화 |
| `noEmitOnError` | 타입 오류 시 JS 파일 생성 안 함 |

##### 트랜스파일 전/후 비교

```typescript
// welcome.ts (TypeScript)
function welcome(name: string | null) {
  if (name === null) {
    return `Welcome!`;
  }
  return `Welcome, ${name}!`;
}
```

```javascript
// welcome.js (트랜스파일된 JavaScript)
function welcome(name) {
  if (name === null) {
    return `Welcome!`;
  }
  return `Welcome, ${name}!`;
}
// 타입 어노테이션이 제거됨
```

---

#### 6. React + TypeScript 컴포넌트

##### 프로젝트 생성

```bash
npm create vite@latest alert -- --template react-ts
cd alert
npm i
npm run dev
```

> 📁 `.tsx` 확장자는 TypeScript React 컴포넌트를 의미

##### Props 타입 정의

```tsx
import { useState, type ReactNode } from 'react';

// Props 타입 별칭
type Props = {
  type?: string;              // 선택적
  heading: string;            // 필수
  children: ReactNode;        // JSX 요소 허용
  closable?: boolean;         // 선택적
  onClose?: () => void;       // 선택적 콜백
};

export function Alert({
  type = "information",
  heading,
  children,
  closable,
  onClose,
}: Props) {
  const [visible, setVisible] = useState(true);

  if (!visible) return null;

  return (
    <div className={`alert ${type}`}>
      <span>{heading}</span>
      <div>{children}</div>
      {closable && (
        <button onClick={() => {
          setVisible(false);
          onClose?.();
        }}>
          닫기
        </button>
      )}
    </div>
  );
}
```

##### Props 타입 오류 감지

```tsx
// App.tsx
import { Alert } from './Alert';

function App() {
  // ❌ 오류: heading과 children이 필수
  return <Alert />;

  // ✅ 올바른 사용
  return (
    <Alert heading="Success">
      Everything is really good!
    </Alert>
  );
}
```

##### State 타입 지정

```tsx
// 타입 추론 사용 (권장)
const [visible, setVisible] = useState(true);  // boolean으로 추론

// 명시적 타입 지정 (추론이 안 될 때)
const [visible, setVisible] = useState<boolean>();  // 초기값 없이 타입 지정

// 복잡한 타입의 경우
type User = { id: number; name: string };
const [user, setUser] = useState<User | null>(null);
```

---

### 🔍 심화 학습

#### Type Predicate (타입 술어) 패턴

```typescript
// 타입 가드 함수
function isError(response: unknown): response is { error: string } {
  return (
    typeof response === 'object' &&
    response !== null &&
    'error' in response
  );
}

// 사용
function handleResponse(response: unknown) {
  if (isError(response)) {
    console.error(response.error);  // response가 { error: string }으로 좁혀짐
  }
}
```

#### 선택적 속성 vs 유니온 with null

```typescript
// 선택적 속성: 속성 자체가 없을 수 있음
type Product1 = {
  name: string;
  lastSale?: Date;  // undefined 또는 Date
};

// 유니온 with null: 속성은 있지만 값이 null일 수 있음
type Product2 = {
  name: string;
  lastSale: Date | null;  // null 또는 Date (반드시 명시해야 함)
};

const p1: Product1 = { name: "Table" };           // ✅ lastSale 생략 가능
const p2: Product2 = { name: "Table" };           // ❌ lastSale 필수
const p2: Product2 = { name: "Table", lastSale: null };  // ✅
```

#### 제네릭 타입 미리보기

```typescript
// useState의 제네릭 인자
const [count, setCount] = useState<number>(0);
const [items, setItems] = useState<string[]>([]);

// 배열 제네릭
const numbers: Array<number> = [1, 2, 3];
```

---

### 💡 실무 적용 포인트

1. **타입 추론 우선**: 가능하면 타입 어노테이션 생략, 추론 불가 시만 명시
2. **any 사용 금지**: `unknown` + 타입 가드로 대체
3. **Props 타입 필수**: 모든 React 컴포넌트에 Props 타입 정의
4. **strict 모드 활성화**: tsconfig.json에서 `"strict": true` 설정
5. **noEmitOnError 활성화**: 타입 오류 시 빌드 실패하도록 설정
6. **ReactNode 활용**: children prop에는 `ReactNode` 타입 사용
7. **선택적 속성**: `?`로 optional props 명시, 기본값과 함께 사용

---

### ✅ 정리 체크리스트

- [ ] TypeScript가 JavaScript의 슈퍼셋이며 트랜스파일이 필요함을 안다
- [ ] 타입 어노테이션과 타입 추론의 차이를 설명할 수 있다
- [ ] `any`와 `unknown`의 차이를 안다
- [ ] Type Predicate로 `unknown` 타입을 좁힐 수 있다
- [ ] 타입 별칭(type alias)을 생성할 수 있다
- [ ] `&` 연산자로 타입을 확장할 수 있다
- [ ] 유니온 타입으로 여러 값을 허용하는 타입을 만들 수 있다
- [ ] `?`로 선택적 속성/매개변수를 정의할 수 있다
- [ ] tsconfig.json의 주요 옵션을 이해한다
- [ ] React 컴포넌트에 Props 타입을 적용할 수 있다
- [ ] useState에 제네릭으로 타입을 명시할 수 있다

---

### 🔗 참고 자료

- [TypeScript Playground](https://www.typescriptlang.org/play/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)
- [tsconfig.json 옵션](https://www.typescriptlang.org/tsconfig)
- [JavaScript Strict Mode](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode)
- [JavaScript 데이터 타입](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures)
- [책 코드 저장소](https://github.com/PacktPublishing/Learn-React-with-TypeScript-Third-Edition/tree/main/Chapter02)
