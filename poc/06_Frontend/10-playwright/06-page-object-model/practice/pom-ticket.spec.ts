import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';
import { TicketListPage } from './pages/TicketListPage';
import { TicketCreatePage } from './pages/TicketCreatePage';

/**
 * Page Object Model (POM) 패턴 적용 테스트
 *
 * 테스트 구성:
 * 1. 로그인 테스트 (LoginPage)
 * 2. 티켓 목록 네비게이션 및 검색 (TicketListPage)
 * 3. 티켓 생성 플로우 (TicketCreatePage)
 * 4. End-to-end 워크플로우 (모든 Page Object 조합)
 * 5. 검증 에러 테스트
 */

test.describe('Page Object Model - 로그인', () => {
  test('관리자 로그인 성공', async ({ page }) => {
    // Given: LoginPage 인스턴스 생성
    const loginPage = new LoginPage(page);
    await loginPage.goto();

    // When: 관리자 계정으로 로그인
    await loginPage.loginAsAdmin();

    // Then: 티켓 목록 페이지로 리디렉션
    await expect(page).toHaveURL(/.*tickets/);

    // And: 로그인 상태 확인
    const isLoggedIn = await loginPage.isLoggedIn();
    expect(isLoggedIn).toBe(true);
  });

  test('일반 사용자 로그인 성공', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();

    await loginPage.loginAsUser();

    await expect(page).toHaveURL(/.*tickets/);
  });

  test('잘못된 자격증명으로 로그인 실패', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();

    // When: 잘못된 계정 정보 입력
    await loginPage.login('wrong', 'wrong');

    // Then: 에러 메시지 표시
    const errorMessage = await loginPage.getErrorMessage();
    expect(errorMessage).toBeTruthy();
    expect(errorMessage).toContain('Invalid');

    // And: 여전히 로그인 페이지에 있음
    const isLoginPage = await loginPage.isLoginPage();
    expect(isLoginPage).toBe(true);
  });

  test('로그인 폼 표시 확인', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();

    // 로그인 폼 요소들이 모두 표시되는지 확인
    const isFormVisible = await loginPage.isLoginFormVisible();
    expect(isFormVisible).toBe(true);

    const isButtonEnabled = await loginPage.isLoginButtonEnabled();
    expect(isButtonEnabled).toBe(true);
  });
});

test.describe('Page Object Model - 티켓 목록', () => {
  test.beforeEach(async ({ page }) => {
    // 각 테스트 전에 로그인
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.loginAsAdmin();
  });

  test('티켓 목록 페이지 접근', async ({ page }) => {
    const listPage = new TicketListPage(page);
    await listPage.goto();

    // 테이블이 표시되는지 확인
    const isVisible = await listPage.isTableVisible();
    expect(isVisible).toBe(true);

    // 티켓이 존재하는지 확인
    const hasTickets = await listPage.hasTickets();
    expect(hasTickets).toBe(true);
  });

  test('티켓명으로 검색', async ({ page }) => {
    const listPage = new TicketListPage(page);
    await listPage.goto();

    // When: 티켓명으로 검색
    await listPage.searchByColumn('tcktNm', 'CI/CD');

    // Then: 검색 결과 확인
    const count = await listPage.getTicketCount();
    expect(count).toBeGreaterThan(0);

    // And: 첫 번째 행 데이터 확인
    const firstRow = await listPage.getRowData(0);
    expect(firstRow.tcktNm).toContain('CI/CD');
  });

  test('티켓 번호로 검색', async ({ page }) => {
    const listPage = new TicketListPage(page);
    await listPage.goto();

    // 먼저 첫 번째 티켓 번호 가져오기
    const firstRow = await listPage.getRowData(0);
    const tcktNo = firstRow.tcktNo;

    // 검색 실행
    await listPage.searchByColumn('tcktNo', tcktNo);

    // 결과 확인
    const count = await listPage.getTicketCount();
    expect(count).toBeGreaterThanOrEqual(1);

    const searchResult = await listPage.getRowData(0);
    expect(searchResult.tcktNo).toBe(tcktNo);
  });

  test('상태별 필터링', async ({ page }) => {
    const listPage = new TicketListPage(page);
    await listPage.goto();

    // When: PROGRESS 상태로 필터링
    await listPage.filterByStatus('PROGRESS');

    // Then: 모든 티켓이 PROGRESS 상태인지 확인
    const allRows = await listPage.getAllRowData();
    for (const row of allRows) {
      expect(row.tcktStts).toBe('PROGRESS');
    }
  });

  test('페이징 네비게이션', async ({ page }) => {
    const listPage = new TicketListPage(page);
    await listPage.goto();

    // 페이지 크기를 10으로 설정
    await listPage.setPageSize(10);

    // 현재 페이지 정보 확인
    const pageInfo = await listPage.getPageInfo();
    expect(pageInfo).toBeTruthy();

    // 다음 페이지로 이동 (티켓이 충분히 많다면)
    const initialCount = await listPage.getTicketCount();
    if (initialCount >= 10) {
      await listPage.goToNextPage();
      const newCount = await listPage.getTicketCount();
      expect(newCount).toBeGreaterThan(0);
    }
  });

  test('티켓 클릭하여 상세 페이지 이동', async ({ page }) => {
    const listPage = new TicketListPage(page);
    await listPage.goto();

    // Given: 첫 번째 티켓 정보
    const firstRow = await listPage.getRowData(0);

    // When: 티켓 클릭
    await listPage.clickTicket(firstRow.tcktNo);

    // Then: 진행 상태 페이지로 이동
    await expect(page).toHaveURL(/.*progress/);
  });
});

test.describe('Page Object Model - 티켓 생성', () => {
  test.beforeEach(async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.loginAsAdmin();
  });

  test('CICD 티켓 생성 페이지 접근', async ({ page }) => {
    const listPage = new TicketListPage(page);
    await listPage.goto();

    // When: CICD 티켓 생성 버튼 클릭
    await listPage.navigateToCreateCicd();

    // Then: CICD 티켓 생성 페이지로 이동
    await expect(page).toHaveURL(/.*tickets\/create\/cicd/);
  });

  test('CICD 티켓 생성 성공', async ({ page }) => {
    const createPage = new TicketCreatePage(page);
    await createPage.gotoCicd();

    // When: CICD 티켓 정보 입력
    await createPage.fillCicdTicket({
      tcktNm: 'Jenkins CI/CD 파이프라인 구축',
      taskCd: 'BUILD',
      wrkflwCd: 'CICD_WORKFLOW_01',
      devlopPicId: 'admin',
      repoUrl: 'https://git.okestro.com/tps/tps-api',
      branchNm: 'main',
    });

    // Then: 저장 버튼이 활성화됨
    const isEnabled = await createPage.isSaveButtonEnabled();
    expect(isEnabled).toBe(true);

    // When: 저장
    await createPage.save();

    // Then: 티켓 목록 페이지로 리디렉션
    await expect(page).toHaveURL(/.*tickets/);
  });

  test('PMS 티켓 생성 성공', async ({ page }) => {
    const createPage = new TicketCreatePage(page);
    await createPage.gotoPms();

    // When: PMS 티켓 정보 입력
    await createPage.fillPmsTicket({
      tcktNm: 'PMS 프로젝트 관리 기능 개발',
      taskCd: 'DEVELOP',
      wrkflwCd: 'PMS_WORKFLOW_01',
      devlopPicId: 'admin',
    });

    // When: 저장
    await createPage.save();

    // Then: 티켓 목록 페이지로 리디렉션
    await expect(page).toHaveURL(/.*tickets/);
  });

  test('필수 필드 미입력 시 검증 에러', async ({ page }) => {
    const createPage = new TicketCreatePage(page);
    await createPage.gotoCicd();

    // When: 필수 필드 없이 저장 시도
    await createPage.save();

    // Then: 검증 에러 표시
    const hasErrors = await createPage.hasValidationErrors();
    expect(hasErrors).toBe(true);

    const errors = await createPage.getValidationErrors();
    expect(errors.length).toBeGreaterThan(0);
  });

  test('Repository 추가 및 삭제', async ({ page }) => {
    const createPage = new TicketCreatePage(page);
    await createPage.gotoCicd();

    // When: Repository 추가
    await createPage.addRepository('https://git.okestro.com/tps/tps-api', 'main');
    await createPage.addRepository('https://git.okestro.com/tps/tps-web', 'develop');

    // Then: Repository 개수 확인
    let repoCount = await createPage.getRepositoryCount();
    expect(repoCount).toBe(2);

    // When: 첫 번째 Repository 정보 확인
    const firstRepo = await createPage.getRepositoryInfo(0);
    expect(firstRepo.repoUrl).toContain('tps-api');
    expect(firstRepo.branchNm).toBe('main');

    // When: 첫 번째 Repository 삭제
    await createPage.removeRepository(0);

    // Then: Repository 개수 감소
    repoCount = await createPage.getRepositoryCount();
    expect(repoCount).toBe(1);
  });

  test('취소 버튼 클릭 시 목록으로 돌아가기', async ({ page }) => {
    const createPage = new TicketCreatePage(page);
    await createPage.gotoCicd();

    // When: 취소 버튼 클릭
    await createPage.cancel();

    // Then: 티켓 목록 페이지로 리디렉션
    await expect(page).toHaveURL(/.*tickets/);
  });
});

test.describe('Page Object Model - End-to-end 워크플로우', () => {
  test('티켓 생성 → 검색 → 상세 페이지 이동', async ({ page }) => {
    // Given: 관리자로 로그인
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.loginAsAdmin();

    // When: CICD 티켓 생성
    const createPage = new TicketCreatePage(page);
    await createPage.gotoCicd();

    const ticketName = `E2E Test Ticket ${Date.now()}`;
    await createPage.fillCicdTicket({
      tcktNm: ticketName,
      taskCd: 'BUILD',
      wrkflwCd: 'CICD_WORKFLOW_01',
      devlopPicId: 'admin',
      repoUrl: 'https://git.okestro.com/tps/tps-api',
      branchNm: 'feature/e2e-test',
    });

    await createPage.save();

    // Then: 티켓 목록에서 검색
    const listPage = new TicketListPage(page);
    await listPage.searchByColumn('tcktNm', ticketName);

    const count = await listPage.getTicketCount();
    expect(count).toBeGreaterThan(0);

    // And: 생성된 티켓 클릭하여 상세 페이지로 이동
    const firstRow = await listPage.getRowData(0);
    expect(firstRow.tcktNm).toBe(ticketName);

    await listPage.clickTicket(firstRow.tcktNo);
    await expect(page).toHaveURL(/.*progress/);
  });

  test('여러 상태 필터 전환 후 티켓 생성', async ({ page }) => {
    // Given: 관리자로 로그인
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.loginAsAdmin();

    const listPage = new TicketListPage(page);
    await listPage.goto();

    // When: 여러 상태 필터 전환
    await listPage.filterByStatus('PROGRESS');
    let count = await listPage.getTicketCount();
    expect(count).toBeGreaterThanOrEqual(0);

    await listPage.filterByStatus('COMPLETE');
    count = await listPage.getTicketCount();
    expect(count).toBeGreaterThanOrEqual(0);

    await listPage.filterByStatus('all');
    count = await listPage.getTicketCount();
    expect(count).toBeGreaterThan(0);

    // Then: 티켓 생성 페이지로 이동
    await listPage.navigateToCreatePms();
    await expect(page).toHaveURL(/.*tickets\/create\/pms/);

    // And: 티켓 생성
    const createPage = new TicketCreatePage(page);
    await createPage.fillPmsTicket({
      tcktNm: 'Multi-filter Test Ticket',
      taskCd: 'TEST',
      wrkflwCd: 'PMS_WORKFLOW_01',
      devlopPicId: 'admin',
    });

    await createPage.save();
    await expect(page).toHaveURL(/.*tickets/);
  });

  test('로그인 상태 유지 확인', async ({ page }) => {
    // Given: 로그인
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.loginAsAdmin();

    // When: 여러 페이지 이동
    const listPage = new TicketListPage(page);
    await listPage.goto();
    let isLoggedIn = await listPage.isLoggedIn();
    expect(isLoggedIn).toBe(true);

    const createPage = new TicketCreatePage(page);
    await createPage.gotoCicd();
    isLoggedIn = await createPage.isLoggedIn();
    expect(isLoggedIn).toBe(true);

    await createPage.cancel();
    await listPage.goto();
    isLoggedIn = await listPage.isLoggedIn();
    expect(isLoggedIn).toBe(true);
  });
});

test.describe('Page Object Model - 검증 에러 처리', () => {
  test.beforeEach(async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.loginAsAdmin();
  });

  test('티켓명 미입력 시 검증 에러', async ({ page }) => {
    const createPage = new TicketCreatePage(page);
    await createPage.gotoCicd();

    // When: 티켓명 제외하고 입력
    await createPage.selectTask('BUILD');
    await createPage.selectWorkflow('CICD_WORKFLOW_01');
    await createPage.selectDeveloper('admin');
    await createPage.save();

    // Then: 검증 에러
    const hasErrors = await createPage.hasValidationErrors();
    expect(hasErrors).toBe(true);
  });

  test('필수 필드 모두 입력 시 검증 에러 없음', async ({ page }) => {
    const createPage = new TicketCreatePage(page);
    await createPage.gotoCicd();

    // When: 모든 필수 필드 입력
    await createPage.fillBasicInfo({
      tcktNm: 'Valid Ticket',
      taskCd: 'BUILD',
      wrkflwCd: 'CICD_WORKFLOW_01',
      devlopPicId: 'admin',
    });

    // Then: 필수 필드 입력 완료
    const isFilled = await createPage.areRequiredFieldsFilled();
    expect(isFilled).toBe(true);

    // And: 저장 버튼 활성화
    const isEnabled = await createPage.isSaveButtonEnabled();
    expect(isEnabled).toBe(true);
  });
});
