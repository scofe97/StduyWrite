# MVC, MVP, MVVM 패턴

## 개요

**정의**: MVC, MVP, MVVM은 애플리케이션의 데이터, 비즈니스 로직, UI를 분리하는 아키텍처 패턴이다.

**목적**: 관심사 분리(Separation of Concerns)를 통해 코드의 유지보수성, 테스트 용이성, 확장성을 향상시킨다.

---

## 핵심 개념

### 패턴 선택 가이드

```
아키텍처 패턴 선택
    │
    ├─ 단순한 웹 앱, 서버 사이드 렌더링?
    │       └─ Yes → MVC 패턴
    │
    ├─ 복잡한 프레젠테이션 로직, 단위 테스트 중요?
    │       └─ Yes → MVP 패턴 (Passive View)
    │
    └─ 양방향 데이터 바인딩, 선언적 UI?
            └─ Yes → MVVM 패턴
```

### 패턴 비교

| 패턴 | View-Model 관계 | 데이터 바인딩 | 테스트 용이성 | 대표 프레임워크 |
|------|----------------|--------------|--------------|----------------|
| MVC | View가 Model 참조 | 없음 | 중간 | Express, Rails |
| MVP | Presenter가 중재 | 없음 | 높음 | Android (전통) |
| MVVM | ViewModel 바인딩 | 양방향 | 높음 | Vue, Angular |

---

## 구현 패턴

### 1. MVC Pattern (Model-View-Controller)

**목적**: 사용자 인터페이스 로직을 비즈니스 로직과 분리

**역사**: 1970년대 Smalltalk-80에서 유래. Trygve Reenskaug이 최초 정의.

#### 구성 요소

```
┌──────────────────────────────────────────────────────────┐
│                       MVC 구조                            │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   ┌─────────┐     업데이트     ┌─────────┐              │
│   │  Model  │ ───────────────→ │  View   │              │
│   │         │ ←─────────────── │         │              │
│   │ (데이터) │     데이터 요청   │  (UI)   │              │
│   └────┬────┘                  └────┬────┘              │
│        │                            │                    │
│        │      ┌───────────┐        │                    │
│        └─────→│Controller │←───────┘                    │
│     업데이트   │ (중재자)   │   사용자 입력               │
│               └───────────┘                              │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 책임 |
|----------|------|------|
| **Model** | 데이터와 비즈니스 로직 | 상태 관리, 유효성 검사, 데이터 저장/검색 |
| **View** | 사용자 인터페이스 | Model 데이터의 시각적 표현 |
| **Controller** | 사용자 입력 처리 | View와 Model 사이 중재 |

#### Backbone.js Model 예제

```javascript
// Model 정의
const Todo = Backbone.Model.extend({
    defaults: {
        title: '',
        completed: false
    },

    toggle() {
        this.save({
            completed: !this.get('completed')
        });
    }
});

// Collection (Model 그룹)
const TodosCollection = Backbone.Collection.extend({
    model: Todo,

    completed() {
        return this.filter(todo => todo.get('completed'));
    },

    remaining() {
        return this.filter(todo => !todo.get('completed'));
    }
});
```

#### Backbone.js View 예제

```javascript
const TodoView = Backbone.View.extend({
    tagName: 'li',

    // View가 Model 변경 감시
    initialize() {
        this.listenTo(this.model, 'change', this.render);
        this.listenTo(this.model, 'destroy', this.remove);
    },

    events: {
        'click .toggle': 'toggleCompleted',
        'click .destroy': 'clear'
    },

    render() {
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    },

    toggleCompleted() {
        this.model.toggle();
    },

    clear() {
        this.model.destroy();
    }
});
```

#### MVC 장단점

| 장점 | 단점 |
|------|------|
| 관심사의 명확한 분리 | View-Model 직접 참조로 결합도 발생 |
| 동시 개발 가능 | 대규모 앱에서 Controller 비대화 |
| 수정이 전체에 영향 없음 | 양방향 데이터 흐름으로 복잡성 증가 |

---

### 2. MVP Pattern (Model-View-Presenter)

**목적**: View를 완전히 수동적(Passive)으로 만들어 테스트 용이성 극대화

**변형**:
- **Passive View**: Presenter가 View를 직접 업데이트 (가장 순수한 형태)
- **Supervising Controller**: View가 Model에 데이터 바인딩, Presenter는 복잡한 로직만 처리

#### MVP 구조

```
┌──────────────────────────────────────────────────────────┐
│                       MVP 구조                            │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   ┌─────────┐               ┌─────────────┐             │
│   │  Model  │ ←───────────→ │  Presenter  │             │
│   │ (데이터) │   데이터 요청/  │   (로직)    │             │
│   └─────────┘   업데이트     └──────┬──────┘             │
│                                    │                     │
│                              View 업데이트               │
│                                    │                     │
│                                    ▼                     │
│                              ┌─────────┐                │
│                              │  View   │                │
│                              │(Passive)│                │
│                              └─────────┘                │
│                                                          │
│   핵심: View는 Presenter의 지시만 수행                    │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

#### Passive View 특징

| 특징 | 설명 |
|------|------|
| **View의 역할** | 단순한 UI 렌더링만 담당, 로직 없음 |
| **Presenter의 역할** | 모든 프레젠테이션 로직 담당 |
| **테스트** | Presenter를 Mock View로 단위 테스트 |
| **의존성** | View는 Presenter에만 의존, Model 직접 접근 안 함 |

#### MVP 구현 예제

```javascript
// View Interface
class TodoView {
    setItems(items) { /* UI 렌더링 */ }
    setLoading(loading) { /* 로딩 표시 */ }
    showError(message) { /* 에러 표시 */ }
    onAddClick(handler) { /* 클릭 핸들러 등록 */ }
}

// Presenter
class TodoPresenter {
    constructor(view, model) {
        this.view = view;
        this.model = model;

        this.view.onAddClick(this.handleAdd.bind(this));
    }

    async loadTodos() {
        this.view.setLoading(true);
        try {
            const items = await this.model.fetchAll();
            this.view.setItems(items);
        } catch (error) {
            this.view.showError(error.message);
        } finally {
            this.view.setLoading(false);
        }
    }

    async handleAdd(title) {
        const newTodo = await this.model.create({ title });
        this.loadTodos(); // View 갱신
    }
}
```

#### MVC vs MVP 비교

| 측면 | MVC | MVP |
|------|-----|-----|
| View-Model 관계 | View가 Model 직접 참조 | Presenter가 중재 |
| View의 역할 | 능동적 (Observer) | 수동적 (Passive) |
| 테스트 용이성 | 중간 | 높음 |
| 코드량 | 적음 | 많음 (Interface 필요) |

---

### 3. MVVM Pattern (Model-View-ViewModel)

**목적**: 선언적 데이터 바인딩으로 View와 로직을 완전히 분리

**역사**: 2005년 Microsoft의 John Gossman이 WPF/Silverlight를 위해 제안

#### MVVM 구조

```
┌──────────────────────────────────────────────────────────┐
│                      MVVM 구조                            │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   ┌─────────┐               ┌─────────────┐             │
│   │  Model  │ ←───────────→ │  ViewModel  │             │
│   │ (데이터) │               │             │             │
│   └─────────┘               └──────┬──────┘             │
│                                    │                     │
│                              Data Binding               │
│                              (양방향)                    │
│                                    │                     │
│                                    ▼                     │
│                              ┌─────────┐                │
│                              │  View   │                │
│                              │         │                │
│                              └─────────┘                │
│                                                          │
│   핵심: View와 ViewModel 간 자동 동기화                   │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

#### 구성 요소

| 구성 요소 | 역할 | 특징 |
|----------|------|------|
| **Model** | 도메인 데이터와 로직 | 비즈니스 규칙, 데이터 검증 |
| **View** | UI 정의 (선언적) | 데이터 바인딩 표현식 포함 |
| **ViewModel** | View의 상태와 동작 | Model 데이터를 View에 맞게 변환 |

#### Vue.js MVVM 예제

```javascript
// Vue 3 Composition API
const app = createApp({
    setup() {
        // ViewModel (반응형 상태)
        const searchQuery = ref('');
        const todos = ref([]);
        const loading = ref(false);

        // 계산된 속성 (파생 상태)
        const filteredTodos = computed(() => {
            if (!searchQuery.value) return todos.value;
            return todos.value.filter(todo =>
                todo.title.includes(searchQuery.value)
            );
        });

        // 액션
        async function addTodo(title) {
            loading.value = true;
            const newTodo = await api.createTodo({ title });
            todos.value.push(newTodo);
            loading.value = false;
        }

        return {
            searchQuery,
            filteredTodos,
            loading,
            addTodo
        };
    }
});
```

```html
<!-- View (템플릿) - 양방향 바인딩 -->
<template>
    <div>
        <!-- v-model: 양방향 데이터 바인딩 -->
        <input v-model="searchQuery" placeholder="검색...">

        <!-- v-if: 조건부 렌더링 -->
        <div v-if="loading">로딩 중...</div>

        <!-- v-for: 리스트 렌더링 -->
        <ul v-else>
            <li v-for="todo in filteredTodos" :key="todo.id">
                {{ todo.title }}
            </li>
        </ul>
    </div>
</template>
```

#### 데이터 바인딩 유형

| 유형 | 방향 | 예시 | 설명 |
|------|------|------|------|
| **One-way** | Model → View | `{{ value }}` | 읽기 전용 표시 |
| **Two-way** | Model ↔ View | `v-model` | 입력과 상태 동기화 |
| **Event** | View → Model | `@click` | 사용자 액션 처리 |

#### MVVM 장단점

| 장점 | 단점 |
|------|------|
| View와 로직 완전 분리 | 간단한 UI에는 과도함 |
| 선언적 UI로 가독성 향상 | 양방향 바인딩 디버깅 어려움 |
| ViewModel 단위 테스트 용이 | 메모리 사용량 증가 가능 |
| UI 디자이너와 협업 용이 | 학습 곡선 존재 |

---

## 프레임워크별 적용

### React의 아키텍처

React는 순수 MVVM이 아닌 **단방향 데이터 흐름**을 따른다.

```
┌──────────────────────────────────────────────────────────┐
│                    React 데이터 흐름                      │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   State (상태)                                           │
│       │                                                  │
│       ▼                                                  │
│   Props (속성) ───→ Component (컴포넌트) ───→ UI         │
│       ▲                    │                             │
│       │                    │                             │
│       └────── Events ──────┘                             │
│                                                          │
│   특징: 단방향 데이터 흐름, 명시적 상태 업데이트           │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

```javascript
// React: 명시적인 상태 업데이트 필요
function TodoApp() {
    const [query, setQuery] = useState('');
    const [todos, setTodos] = useState([]);

    // 양방향 바인딩이 아님 - onChange로 명시적 업데이트
    const handleChange = (e) => setQuery(e.target.value);

    return (
        <input value={query} onChange={handleChange} />
    );
}
```

### 프레임워크별 비교

| 프레임워크 | 패턴 | 데이터 바인딩 | 상태 관리 |
|-----------|------|--------------|----------|
| **React** | 단방향 | One-way | useState, Redux |
| **Vue** | MVVM | Two-way (v-model) | Composition API, Pinia |
| **Angular** | MVVM | Two-way | Services, RxJS |
| **Svelte** | 반응형 | Two-way | 내장 반응성 |

---

## 트레이드오프

### 패턴별 선택 기준

```yaml
mvc_pattern:
  use_when:
    - 서버 사이드 렌더링 애플리케이션
    - 단순한 웹 페이지
    - 팀이 MVC에 익숙한 경우
  avoid_when:
    - 복잡한 UI 상호작용
    - 실시간 데이터 동기화 필요

mvp_pattern:
  use_when:
    - 높은 테스트 커버리지 요구
    - 복잡한 프레젠테이션 로직
    - View 로직 완전 분리 필요
  avoid_when:
    - 작은 프로젝트
    - 빠른 개발 속도 필요

mvvm_pattern:
  use_when:
    - 양방향 데이터 동기화 필요
    - 선언적 UI 선호
    - 디자이너-개발자 협업
  avoid_when:
    - 단순한 정적 UI
    - 메모리 제약 환경
    - 데이터 흐름 추적 중요
```

---

## 면접 포인트

**Q**: MVC, MVP, MVVM의 주요 차이점은?

**A**: MVC에서 View는 Model을 직접 참조하고 Observer 패턴으로 업데이트를 받는다. MVP에서 View는 완전히 수동적(Passive)이며 Presenter가 모든 로직을 담당하여 테스트가 용이하다. MVVM은 양방향 데이터 바인딩으로 View와 ViewModel이 자동 동기화되어 선언적 UI 작성이 가능하다.

**Q**: React는 어떤 아키텍처 패턴을 따르는가?

**A**: React는 순수 MVC나 MVVM이 아닌 단방향 데이터 흐름(Flux 아키텍처)을 따른다. 상태가 Props를 통해 컴포넌트로 전달되고, 이벤트로 상태 변경을 요청한다. MVVM의 양방향 바인딩과 달리 명시적인 setState 호출이 필요하여 데이터 흐름 추적이 용이하다.

**Q**: 양방향 데이터 바인딩의 장단점은?

**A**: 장점은 코드량 감소와 View-ViewModel 자동 동기화다. 단점은 복잡한 앱에서 데이터 변경 추적이 어렵고 의도치 않은 부작용이 발생할 수 있다. React가 단방향을 선택한 이유는 예측 가능성과 디버깅 용이성 때문이다.

---

## 참고 자료

- Trygve Reenskaug, "The original MVC reports" (1979)
- Martin Fowler, "GUI Architectures"
- Microsoft, "The MVVM Pattern"
- [Vue.js Reactivity Fundamentals](https://vuejs.org/guide/essentials/reactivity-fundamentals.html)
- [Angular Architecture](https://angular.io/guide/architecture)
