# 06. Page Object Model (POM) - 사전 질문

## 1. POM 패턴이란 무엇이고 왜 필요한가?

**질문 의도**: POM의 개념과 존재 이유를 이해하기

**힌트**:
- E2E 테스트에서 로케이터가 어디에 정의되는지?
- UI가 변경되었을 때 테스트 코드 수정 범위는?
- 중복 코드 문제를 어떻게 해결할까?

**생각해볼 점**:
- 로케이터를 테스트 코드에 직접 작성하면 어떤 문제가 발생하는가?
- 같은 로그인 로직을 10개 테스트에서 반복하면 유지보수가 어떻게 되는가?
- 페이지별로 클래스를 만들면 어떤 이점이 있는가?

---

## 2. Page Object에 assertion을 포함해야 하는가?

**질문 의도**: POM의 책임 범위를 명확히 이해하기

**힌트**:
- Page Object의 주 목적은 무엇인가? (페이지 구조 캡슐화 vs 검증)
- `expect()`를 Page Object 내부에 넣으면 재사용성이 어떻게 되는가?
- 테스트 시나리오별로 다른 검증이 필요한 경우는?

**생각해볼 점**:
```typescript
// 방법 A: Page Object에 assertion 포함
class LoginPage {
  async login(username: string, password: string) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
    await expect(this.page).toHaveURL(/.*tickets/); // ← 여기
  }
}

// 방법 B: Page Object는 액션만, assertion은 테스트에서
class LoginPage {
  async login(username: string, password: string) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }
}

test('로그인 성공', async () => {
  await loginPage.login('admin', 'admin123');
  await expect(page).toHaveURL(/.*tickets/); // ← 여기
});
```

**어떤 방식이 더 유연한가?**

---

## 3. BasePage에 공통 로직을 어디까지 넣어야 하는가?

**질문 의도**: 상속 구조와 공통 로직 분리의 균형점 찾기

**힌트**:
- 모든 페이지에 공통으로 필요한 기능은?
- 특정 페이지에만 필요한 기능을 BasePage에 넣으면?
- BasePage가 너무 비대해지면 어떤 문제가 생기는가?

**생각해볼 점**:
- `goto()`, `waitForPageLoad()` - BasePage에?
- `search()`, `filter()` - 특정 페이지에만 필요한 기능인데?
- Header, Footer 같은 공통 컴포넌트는?

**예시**:
```typescript
// BasePage에 넣을 것
- goto(path)
- waitForPageLoad()
- screenshot(name)
- getTitle()

// 각 Page에 넣을 것
- login(username, password) ← LoginPage
- searchByColumn(column, keyword) ← TicketListPage
- fillBasicInfo(data) ← TicketCreatePage
```

---

## 4. Page Object와 Component Object의 차이는?

**질문 의도**: 재사용 가능한 컴포넌트를 별도로 분리하는 이유 이해

**힌트**:
- Pagination이 여러 페이지에서 사용된다면?
- SearchComponent가 리스트 페이지마다 반복된다면?
- Header, Breadcrumb는 모든 페이지에 있다면?

**생각해볼 점**:
```typescript
// 방법 A: 각 Page에 Pagination 로직 중복
class TicketListPage {
  async goToNextPage() { /* 구현 */ }
  async goToPrevPage() { /* 구현 */ }
  async setPageSize(size) { /* 구현 */ }
}

class UserListPage {
  async goToNextPage() { /* 구현 - 중복! */ }
  async goToPrevPage() { /* 구현 - 중복! */ }
  async setPageSize(size) { /* 구현 - 중복! */ }
}

// 방법 B: Component Object로 분리
class PaginationComponent {
  async goToNextPage() { /* 구현 */ }
  async goToPrevPage() { /* 구현 */ }
  async setPageSize(size) { /* 구현 */ }
}

class TicketListPage {
  readonly pagination: PaginationComponent;

  constructor(page: Page) {
    this.pagination = new PaginationComponent(page);
  }
}
```

**어떤 방식이 더 유지보수하기 좋은가?**

---

## 5. POM이 과도하게 복잡해지는 안티패턴은?

**질문 의도**: POM의 함정을 미리 파악하여 과도한 추상화 방지

**힌트**:
- Page Object가 너무 많으면?
- 메서드가 너무 세분화되면?
- 상속 계층이 너무 깊으면?

**생각해볼 점**:

**안티패턴 1: 과도한 세분화**
```typescript
// ❌ 너무 세분화됨
class LoginPage {
  async fillUsername(username: string) { /* ... */ }
  async fillPassword(password: string) { /* ... */ }
  async clickLoginButton() { /* ... */ }
  async waitForRedirect() { /* ... */ }
}

// ✅ 적절한 추상화
class LoginPage {
  async login(username: string, password: string) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }
}
```

**안티패턴 2: 너무 많은 Page Object**
```typescript
// ❌ 모달/다이얼로그마다 Page Object 생성
- LoginPage.ts
- LoginModalPage.ts
- ConfirmDialogPage.ts
- ErrorDialogPage.ts
- ...

// ✅ 작은 UI는 Component로
- LoginPage.ts
- components/ModalComponent.ts
- components/DialogComponent.ts
```

**안티패턴 3: God Object**
```typescript
// ❌ BasePage에 모든 기능 넣기
class BasePage {
  async login() { /* ... */ }
  async search() { /* ... */ }
  async filter() { /* ... */ }
  async paginate() { /* ... */ }
  async export() { /* ... */ }
  // 100+ 메서드...
}
```

**질문**:
- 언제 Page Object를 분리하고 언제 합쳐야 하는가?
- 메서드를 어느 수준까지 추상화해야 하는가?
- 얼마나 많은 Page Object가 적당한가?

---

## 정답 확인 후 다음 단계

답을 생각해보셨나요?

다음 파일로 이동하세요:
→ `LEARN.md` (POM 패턴 학습 및 정답 확인)
