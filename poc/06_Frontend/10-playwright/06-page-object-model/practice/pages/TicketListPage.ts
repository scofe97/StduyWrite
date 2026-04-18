import { Page, Locator } from '@playwright/test';
import { BasePage } from './BasePage';

/**
 * TicketListPage - 티켓 목록 페이지 Page Object
 *
 * 경로: /tickets
 *
 * 주요 기능:
 * - 티켓 검색 (컬럼별)
 * - 티켓 상태별 필터링
 * - 페이징
 * - 티켓 목록 조회
 * - 티켓 생성 페이지 이동
 *
 * 사용 예시:
 * ```typescript
 * const listPage = new TicketListPage(page);
 * await listPage.goto();
 * await listPage.searchByColumn('tcktNm', 'CI/CD');
 * await listPage.filterByStatus('PROGRESS');
 * const count = await listPage.getTicketCount();
 * ```
 */
export class TicketListPage extends BasePage {
  // 검색 관련
  readonly searchInput: Locator;
  readonly searchButton: Locator;
  readonly columnSelect: Locator;

  // 테이블 관련
  readonly table: Locator;
  readonly tableRows: Locator;

  // 상태 탭
  readonly allTab: Locator;
  readonly draftTab: Locator;
  readonly progressTab: Locator;
  readonly completeTab: Locator;
  readonly failTab: Locator;

  // 페이징
  readonly prevPageButton: Locator;
  readonly nextPageButton: Locator;
  readonly pageSizeSelect: Locator;
  readonly pageInfo: Locator;

  // 액션 버튼
  readonly createCicdButton: Locator;
  readonly createPmsButton: Locator;

  constructor(page: Page) {
    super(page);

    // 검색
    this.searchInput = page.locator('#searchInput');
    this.searchButton = page.locator('#searchBtn');
    this.columnSelect = page.locator('#searchColumn');

    // 테이블
    this.table = page.locator('#ticketTable');
    this.tableRows = page.locator('.ticket-row');

    // 상태 탭 (data-status 속성으로 구분)
    this.allTab = page.locator('[data-status="all"]');
    this.draftTab = page.locator('[data-status="DRAFT"]');
    this.progressTab = page.locator('[data-status="PROGRESS"]');
    this.completeTab = page.locator('[data-status="COMPLETE"]');
    this.failTab = page.locator('[data-status="FAIL"]');

    // 페이징
    this.prevPageButton = page.locator('#prevPage');
    this.nextPageButton = page.locator('#nextPage');
    this.pageSizeSelect = page.locator('#pageSize');
    this.pageInfo = page.locator('.page-info');

    // 액션 버튼
    this.createCicdButton = page.locator('button:has-text("CICD 티켓 생성")');
    this.createPmsButton = page.locator('button:has-text("PMS 티켓 생성")');
  }

  /**
   * 티켓 목록 페이지로 이동
   */
  async goto() {
    await super.goto('/tickets');
    await this.waitForPageLoad();
  }

  /**
   * 컬럼별 검색
   * @param column - 검색할 컬럼 (tcktNm, tcktNo, devlopPicId 등)
   * @param keyword - 검색 키워드
   */
  async searchByColumn(column: string, keyword: string) {
    await this.columnSelect.selectOption(column);
    await this.searchInput.fill(keyword);
    await this.searchButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  /**
   * 상태별 필터링
   * @param status - 티켓 상태 (DRAFT, PROGRESS, COMPLETE, FAIL)
   */
  async filterByStatus(status: 'all' | 'DRAFT' | 'PROGRESS' | 'COMPLETE' | 'FAIL') {
    const tabMap = {
      all: this.allTab,
      DRAFT: this.draftTab,
      PROGRESS: this.progressTab,
      COMPLETE: this.completeTab,
      FAIL: this.failTab,
    };

    const tab = tabMap[status];
    if (!tab) {
      throw new Error(`Unknown status: ${status}`);
    }

    await tab.click();
    await this.page.waitForLoadState('networkidle');
  }

  /**
   * 티켓 개수 조회
   */
  async getTicketCount(): Promise<number> {
    return this.tableRows.count();
  }

  /**
   * 특정 티켓 클릭
   * @param tcktNo - 티켓 번호
   */
  async clickTicket(tcktNo: string) {
    await this.page.locator(`[data-tckt-no="${tcktNo}"]`).click();
    await this.page.waitForLoadState('networkidle');
  }

  /**
   * 특정 인덱스의 행 데이터 가져오기
   * @param index - 행 인덱스 (0부터 시작)
   * @returns 티켓 데이터 객체
   */
  async getRowData(index: number): Promise<{
    tcktNo: string;
    tcktNm: string;
    tcktStts: string;
  }> {
    const row = this.tableRows.nth(index);

    const tcktNo = await row.getAttribute('data-tckt-no');
    const tcktNm = await row.locator('.tckt-nm').textContent();
    const tcktStts = await row.locator('.tckt-stts').textContent();

    return {
      tcktNo: tcktNo || '',
      tcktNm: tcktNm || '',
      tcktStts: tcktStts || '',
    };
  }

  /**
   * 모든 행 데이터 가져오기
   */
  async getAllRowData(): Promise<Array<{ tcktNo: string; tcktNm: string; tcktStts: string }>> {
    const count = await this.getTicketCount();
    const rows = [];

    for (let i = 0; i < count; i++) {
      const rowData = await this.getRowData(i);
      rows.push(rowData);
    }

    return rows;
  }

  /**
   * 다음 페이지로 이동
   */
  async goToNextPage() {
    await this.nextPageButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  /**
   * 이전 페이지로 이동
   */
  async goToPrevPage() {
    await this.prevPageButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  /**
   * 페이지 크기 변경
   * @param size - 페이지당 표시할 항목 수 (10, 20, 50, 100)
   */
  async setPageSize(size: number) {
    await this.pageSizeSelect.selectOption(size.toString());
    await this.page.waitForLoadState('networkidle');
  }

  /**
   * 현재 페이지 정보 가져오기
   * @returns 페이지 정보 텍스트 (예: "1 / 5 페이지")
   */
  async getPageInfo(): Promise<string | null> {
    return this.pageInfo.textContent();
  }

  /**
   * CICD 티켓 생성 페이지로 이동
   */
  async navigateToCreateCicd() {
    await this.createCicdButton.click();
    await this.page.waitForURL(/.*tickets\/create\/cicd/);
  }

  /**
   * PMS 티켓 생성 페이지로 이동
   */
  async navigateToCreatePms() {
    await this.createPmsButton.click();
    await this.page.waitForURL(/.*tickets\/create\/pms/);
  }

  /**
   * 검색 입력란 초기화
   */
  async clearSearch() {
    await this.searchInput.clear();
  }

  /**
   * 티켓이 존재하는지 확인
   */
  async hasTickets(): Promise<boolean> {
    const count = await this.getTicketCount();
    return count > 0;
  }

  /**
   * 테이블이 표시되는지 확인
   */
  async isTableVisible(): Promise<boolean> {
    return this.table.isVisible();
  }

  /**
   * 티켓 행 로케이터 가져오기
   * 테스트에서 expect() 사용 시 필요
   */
  getTicketRows(): Locator {
    return this.tableRows;
  }
}
