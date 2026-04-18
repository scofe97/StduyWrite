import { Page, Locator } from '@playwright/test';

/**
 * BasePage - 모든 Page Object의 부모 클래스
 *
 * 역할:
 * - 모든 페이지에 공통으로 필요한 기능 제공
 * - page 인스턴스 관리
 * - 페이지 이동, 타이틀 조회, 로그인 상태 확인
 *
 * 원칙:
 * - 모든 페이지에 필요한 기능만 포함
 * - 특정 페이지 로직은 자식 클래스에서 구현
 */
export class BasePage {
  readonly page: Page;
  readonly header: Locator;

  constructor(page: Page) {
    this.page = page;
    this.header = page.locator('.header');
  }

  /**
   * 특정 경로로 페이지 이동
   * @param path - 이동할 경로 (예: /login, /tickets)
   */
  async goto(path: string) {
    const baseUrl = process.env.BASE_URL || 'http://localhost:3002';
    await this.page.goto(`${baseUrl}${path}`);
  }

  /**
   * 현재 페이지의 타이틀 조회
   */
  async getTitle() {
    return this.page.title();
  }

  /**
   * 로그인 상태 확인
   * localStorage에 token이 있으면 로그인 상태로 간주
   */
  async isLoggedIn(): Promise<boolean> {
    const token = await this.page.evaluate(() => localStorage.getItem('token'));
    return !!token;
  }

  /**
   * 헤더 표시 여부 확인
   */
  async isHeaderVisible(): Promise<boolean> {
    return this.header.isVisible();
  }

  /**
   * 페이지 로딩 완료 대기
   */
  async waitForPageLoad() {
    await this.page.waitForLoadState('networkidle');
  }

  /**
   * 스크린샷 캡처
   * @param name - 스크린샷 파일명
   */
  async screenshot(name: string) {
    await this.page.screenshot({ path: `screenshots/${name}.png`, fullPage: true });
  }
}
