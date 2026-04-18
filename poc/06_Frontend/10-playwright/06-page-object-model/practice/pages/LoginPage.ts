import { Page, Locator } from '@playwright/test';
import { BasePage } from './BasePage';

/**
 * LoginPage - 로그인 페이지 Page Object
 *
 * 경로: /login
 *
 * 주요 기능:
 * - 사용자 인증
 * - 로그인 폼 입력
 * - 에러 메시지 처리
 *
 * 사용 예시:
 * ```typescript
 * const loginPage = new LoginPage(page);
 * await loginPage.goto();
 * await loginPage.login('admin', 'admin123');
 * // 또는
 * await loginPage.loginAsAdmin();
 * ```
 */
export class LoginPage extends BasePage {
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;
  readonly loginTitle: Locator;

  constructor(page: Page) {
    super(page);
    this.usernameInput = page.locator('#username');
    this.passwordInput = page.locator('#password');
    this.loginButton = page.locator('button[type="submit"]');
    this.errorMessage = page.locator('.error-message');
    this.loginTitle = page.locator('.login-title');
  }

  /**
   * 로그인 페이지로 이동
   */
  async goto() {
    await super.goto('/login');
  }

  /**
   * 사용자 로그인
   * @param username - 사용자 ID
   * @param password - 비밀번호
   *
   * 주의: 이 메서드는 로그인 액션만 수행하고 검증은 하지 않음
   * 검증은 테스트 코드에서 수행
   */
  async login(username: string, password: string) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }

  /**
   * 관리자 계정으로 로그인 (편의 메서드)
   *
   * TPS Mock 서버 기본 계정:
   * - username: admin
   * - password: admin123
   */
  async loginAsAdmin() {
    await this.login('admin', 'admin123');
  }

  /**
   * 일반 사용자 계정으로 로그인 (편의 메서드)
   *
   * TPS Mock 서버 기본 계정:
   * - username: user01
   * - password: password
   */
  async loginAsUser() {
    await this.login('user01', 'password');
  }

  /**
   * 에러 메시지 텍스트 가져오기
   * @returns 에러 메시지 텍스트 (없으면 null)
   */
  async getErrorMessage(): Promise<string | null> {
    const isVisible = await this.errorMessage.isVisible();
    if (!isVisible) {
      return null;
    }
    return this.errorMessage.textContent();
  }

  /**
   * 로그인 페이지인지 확인
   * @returns 로그인 페이지이면 true
   */
  async isLoginPage(): Promise<boolean> {
    const url = this.page.url();
    return url.includes('/login');
  }

  /**
   * 로그인 폼이 표시되는지 확인
   */
  async isLoginFormVisible(): Promise<boolean> {
    const usernameVisible = await this.usernameInput.isVisible();
    const passwordVisible = await this.passwordInput.isVisible();
    const buttonVisible = await this.loginButton.isVisible();
    return usernameVisible && passwordVisible && buttonVisible;
  }

  /**
   * 로그인 버튼 활성화 여부 확인
   */
  async isLoginButtonEnabled(): Promise<boolean> {
    return this.loginButton.isEnabled();
  }

  /**
   * 로그인 타이틀 텍스트 가져오기
   */
  async getLoginTitle(): Promise<string | null> {
    return this.loginTitle.textContent();
  }
}
