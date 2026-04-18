# React 코드 구조화 패턴 3편 정리

## 개요

**배경**: AI가 코드 구현을 대신하는 시대에도, **코드를 어디에 배치하고 어떤 경계로 나눌지**는 여전히 사람이 판단해야 하는 영역이다. 이 문서는 서로 다른 관점에서 React 프로젝트 구조화를 다루는 3편의 글을 정리한다.

| 편 | 저자 | 핵심 주제 | 접근 |
|----|------|----------|------|
| 1 | @k-svelte-master | 횡단 관심사 분리 | 데코레이터 패턴 + OOP 상태관리 |
| 2 | @kennys | 기능별 응집화 | Features/Shared/App 3계층 |
| 3 | @teo | 코드 경계 찾기 | FSD(Feature-Sliced Design) 3축 |

---

## 패턴 1: 횡단 관심사 분리 (데코레이터 패턴)

### 문제 인식

에러 처리, 성공 알림, 권한 확인 같은 **보조 로직이 20곳에 반복**되면, 하나를 바꿀 때 20곳을 모두 수정해야 한다. 이것이 횡단 관심사(Cross-Cutting Concern) 문제다.

```tsx
// Before: try-catch가 모든 함수에 반복
const handleSubmit = async () => {
  try {
    await api.submit(data);
    toast.success("저장 완료");
  } catch (e) {
    toast.error("실패");
  }
};
```

### 해결: 데코레이터로 선언적 분리

`@` 문법으로 메서드 수준의 관심사를 분리한다. 코드가 **자기 서술적(self-describing)**이 된다.

```tsx
class TodoStore {
  @OnError((e) => toast.error(e.message))
  @OnSuccess(() => toast.success("저장 완료"))
  @Debounce(300)
  async submit(data: TodoForm) {
    return api.submit(data);  // 핵심 로직만 남음
  }
}
```

주요 데코레이터:
- `@OnError` - 에러 처리
- `@OnSuccess` - 성공 후처리
- `@Debounce` - 연속 호출 제어
- `@Authorized` - 권한 확인

### OOP 상태관리

상태와 액션을 클래스에 번들링하여 관련 코드를 한 곳에 모은다. MobX, valtio 같은 프록시 기반 라이브러리와 결합한다.

### Provider 스코프

모듈 레벨 상태의 SSR 위험을 구조적으로 차단한다. Provider 마운트 시 인스턴스 생성, 언마운트 시 파괴 — **사용자 간 데이터 오염이 구조적으로 불가능**하다.

### 핵심 메시지

> "설계는 사람이, 구현은 LLM이"

LLM은 "이렇게 짜라"를 잘 수행하지만, **"어떻게 짜야 하는지"를 결정하는 건 사람**의 몫이다. 구조적 판단과 횡단 관심사 분리 능력이 개발자의 차별점이다.

---

## 패턴 2: 기능별 응집화 (Features/Shared/App)

### 3계층 구조

FSD에서 영감을 받되 팀 특성에 맞게 커스터마이즈한 구조다.

```
src/
├── app/                    # Next.js App Router (라우팅)
│   └── render.tsx          # RSC → Client 중간 레이어
├── features/               # 기능별 응집
│   ├── landing-edit/
│   │   ├── ui/
│   │   ├── utils/
│   │   ├── store/
│   │   ├── types/
│   │   ├── constants/
│   │   ├── hooks/
│   │   └── context/
│   └── project-setting/
└── shared/                 # 공유 요소
    ├── @common/            # 전체 앱 공통 (Header, Provider)
    ├── landing/            # landing 도메인 공유 요소
    ├── project/            # project 도메인 공유 요소
    └── api/                # 중앙화된 API 관리
```

### 위계 규칙 (의존성 방향)

| 계층 | 접근 가능 대상 |
|------|--------------|
| app | features, shared |
| features | **shared만** |
| shared | 제한 없음 (하위 계층) |

**역방향 import는 금지**: features는 다른 features를 직접 import할 수 없다.

### API 중앙화 전략

API를 features 내부에 두면 "이 API가 이 기능에서만 쓰이는가?" 판단이 필요하고, 결국 다른 기능에서도 쓰게 되면서 중복이 생긴다. 따라서 **shared에서 queryKey, queries, mutations를 중앙 관리**한다.

### 폴더 네이밍 의사결정

세 가지 접근을 평가한 결과:
1. 도메인명 — 이름이 길어지고 가독성 저하
2. 카테고리+역할 — shared와 역할 모호
3. **순수 역할 기반** (채택) — 프로젝트 이해도가 있으면 명확

### 핵심 메시지

> "이것이 정답은 아니다"

도메인이 명확히 분리된 프로젝트에 적합하다. 팀원 간 **기능 분류 기준에 대한 합의**가 선행되어야 한다. 순수 함수와 비즈니스 로직 경계를 구분하는 규율이 필수다.

---

## 패턴 3: FSD (Feature-Sliced Design) 코드 경계

### 3축 구조

FSD는 코드를 **Layer(수직) x Slice(도메인) x Segment(기술)** 3축으로 조직화한다.

```
features/cart/ui/        ← Layer: features, Slice: cart, Segment: ui
entities/product/model/  ← Layer: entities, Slice: product, Segment: model
```

#### Layer (수직 관심사 분리)

| Layer | 목적 | 핵심 특성 |
|-------|------|----------|
| app | 프로젝트 전체 설정 | 진입점 |
| shared | 재사용 공통 요소 | 도메인 무관 |
| entities | 도메인 데이터 중심 | **읽기, 순수** |
| features | 사용자 행동/상호작용 | **쓰기, 상태, 부수효과** |
| widgets | 독립 UI 블록 | 탈부착 가능 |
| pages | 개별 페이지 조합 | 라우트 기반 |
| processes | 다중 페이지 비즈니스 프로세스 | (선택적) |

**핵심 원칙**: 상위 Layer는 하위 Layer를 사용 가능, **역방향 절대 금지**.

#### Slice (도메인 분리)

비즈니스 도메인 단위: user, product, cart, order 등.

#### Segment (기술 관심사 분리)

| Segment | 역할 |
|---------|------|
| ui | 컴포넌트 파일 |
| api | 서버 통신 |
| model | 비즈니스 로직, 상태 관리 |
| lib | 도메인 무관 유틸리티 |
| config | 상수, 설정값 |

### REST API 비유

REST가 **HTTP 메서드 + 리소스** 조합으로 엔드포인트를 예측 가능하게 만들듯, FSD는 **Layer + Slice + Segment** 조합으로 파일 위치를 직관적으로 예측 가능하게 만든다.

### entities vs features 구분

이것이 FSD의 가장 핵심적인 경계다.

| 구분 | entities | features |
|------|----------|----------|
| 성격 | 데이터, 읽기, 순수 | 액션, 쓰기, 상태변경 |
| 외부 의존성 | 없음 | 있음 (API 호출, 상태관리) |
| 예시 | 타입 정의, 데이터 변환, 유효성 검사 | 폼 제출, 장바구니 추가, 상태 hook |

```tsx
// entity: 순수 함수 — 외부 의존성 없음
const isValidProduct = (product: Product) =>
  product.price > 0 && product.stock >= 0;

// feature: 상태 관리 — 외부 의존성 있음
const useAddToCart = () => {
  const { mutate } = useAddToCartMutation();
  const handleAddToCart = (product: Product) => mutate(product.id);
  return { handleAddToCart };
};
```

### Props 가이드라인

| 대상 | handler props | styling props | config props |
|------|:---:|:---:|:---:|
| shared/ui (공통 컴포넌트) | O | O | O |
| **그 외 모든 컴포넌트** | **X** | **X** | **X** |

도메인 컴포넌트는 **도메인 데이터만** 받는다. handler나 style을 props로 내려주면 응집도가 저하된다.

```tsx
// Good: 도메인 데이터만 받음
const ProductCard = ({ product }: { product: Product }) => { ... };

// Bad: handler와 config를 props로 받음
const ProductCard = ({ product, onAdd, theme }: Props) => { ... };
```

### 점진적 도입 전략

| 단계 | 구성 | 시점 |
|------|------|------|
| 초기 | `app/config`, `shared/ui`, `shared/lib`, `pages/*` | 프로젝트 시작 |
| 성장 | entities(데이터), features(행동) 분리 | 도메인 패턴 인식 시 |
| 확장 | widgets 분리 | 코드 규모 증가 시 |
| 유연 | 프로젝트 유형에 따라 조정 | 어드민=entities 중심, 앱=features 중심 |

### 핵심 메시지: 무지개 비유

> 무지개에 원래 7가지 색이 있는 게 아니듯, FSD의 7 Layer도 절대 기준이 아니다. 하지만 **경계에 이름을 붙이고 정의하면 더 명확한 구조를 인식할 수 있다**. 중요한 것은 "이게 정답인가?"가 아니라 **"경계를 정의하고 일관되게 유지하는 감각"**이다.

---

## 3편의 교차점

세 글은 서로 다른 접근을 취하지만, 공통으로 강조하는 원칙이 있다.

### 1. 구조 설계는 사람의 몫

AI가 구현을 대신해도, **코드를 어디에 놓을지** 결정하는 건 사람이다. 기술별 폴더(`components/`, `hooks/`)는 규모가 커지면 한계에 부딪히고, 도메인/기능 기반 응집이 더 유지보수하기 좋다는 데 세 글 모두 동의한다.

### 2. 의존성 방향 규칙

세 글 모두 **상위 계층 → 하위 계층** 방향의 import만 허용하고, 역방향을 금지한다. 이 규칙이 없으면 순환 의존성이 발생하고, 변경 영향 범위를 예측할 수 없게 된다.

| 글 | 표현 |
|----|------|
| 패턴 1 | Provider 스코프로 의존성 격리 |
| 패턴 2 | app→features→shared 위계 규칙 |
| 패턴 3 | Layer 간 상위→하위만 허용, 역방향 절대 금지 |

### 3. 팀 합의가 프레임워크보다 중요

어떤 구조든 **팀원 모두가 "이 코드는 여기에 있어야 한다"를 예측할 수 있으면** 좋은 구조다. 완벽한 이론보다 일관된 합의가 실용적이다.

### 4. 읽기(데이터) vs 쓰기(행동) 분리

패턴 1은 상태+액션 번들링으로, 패턴 3은 entities vs features로 이 구분을 명확히 한다. 순수 데이터 표현과 부수효과가 있는 행동을 분리하면 테스트와 재사용이 쉬워진다.

---

## 출처

- [@k-svelte-master - React 데코레이터 패턴을 통한 클린코드 작성법](https://velog.io/@k-svelte-master/react-decorator-clean-over-llm)
- [@kennys - 리액트 프로젝트의 기능별 응집화를 통한 효율적인 코드 구조화](https://velog.io/@kennys/리액트-프로젝트의-응집화를-통한-효율적인-코드-구조화)
- [@teo - FSD 관점으로 바라보는 코드 경계 찾기](https://velog.io/@teo/fsd)
