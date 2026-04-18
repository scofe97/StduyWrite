import { test, expect } from '@playwright/test';

/**
 * 02-1. getBy* 로케이터 실습
 *
 * TPS UI를 기반으로 getBy* 로케이터 사용법을 학습합니다.
 * - getByRole: 접근성 역할 기반 (권장)
 * - getByLabel: 레이블 텍스트 기반
 * - getByText: 텍스트 콘텐츠 기반
 * - getByTestId: 테스트 전용 속성
 * - getByPlaceholder: placeholder 속성 기반
 * - filter: 조건부 필터링
 * - nth/first/last: 인덱스 접근
 */

test.describe('02-1. getBy* 로케이터 실습', () => {
  test.beforeEach(async ({ page }) => {
    // 로그인 후 티켓 목록 페이지로 이동
    await page.goto('http://localhost:3002/login');
    await page.getByLabel('아이디').fill('admin');
    await page.getByLabel('비밀번호').fill('password123');
    await page.getByRole('button', { name: '로그인' }).click();

    // 티켓 목록 페이지 로드 대기
    await page.waitForURL('**/tickets');
    await expect(page.getByTestId('page-header')).toBeVisible();
  });

  test('getByRole로 버튼 찾기', async ({ page }) => {
    // 역할(role)과 접근 가능한 이름(accessible name)으로 요소 찾기
    // aria-label 또는 텍스트로 식별

    // 등록 버튼 찾기
    const cicdButton = page.getByRole('button', { name: '등록(CI/CD)' });
    await expect(cicdButton).toBeVisible();

    const pmsButton = page.getByRole('button', { name: '등록(PMS)' });
    await expect(pmsButton).toBeVisible();

    const deleteButton = page.getByRole('button', { name: '삭제' });
    await expect(deleteButton).toBeVisible();

    // 버튼 클릭 가능 여부 확인
    await expect(cicdButton).toBeEnabled();
  });

  test('getByLabel로 입력 필드 찾기', async ({ page }) => {
    // 레이블 텍스트로 연결된 입력 필드 찾기
    // <label for="id">와 <input id="id"> 연결 활용

    // 검색 컬럼 select
    const columnSelect = page.getByLabel('검색 컬럼');
    await expect(columnSelect).toBeVisible();
    await columnSelect.selectOption('tcktNm');

    // 검색어 입력 필드
    const searchInput = page.getByLabel('검색어');
    await expect(searchInput).toBeVisible();
    await searchInput.fill('테스트');

    // 입력 값 확인
    await expect(searchInput).toHaveValue('테스트');
  });

  test('getByText로 텍스트 기반 검색', async ({ page }) => {
    // 요소 내부의 텍스트 콘텐츠로 찾기
    // exact: false 옵션으로 부분 일치 가능

    // 상태 뱃지 텍스트 찾기
    const completeBadge = page.getByText('완료').first();
    await expect(completeBadge).toBeVisible();

    const progressBadge = page.getByText('진행중').first();
    await expect(progressBadge).toBeVisible();

    // 부분 일치 (exact: false)
    const statusText = page.getByText('상태', { exact: false });
    await expect(statusText).toBeVisible();

    // 정확한 일치 (기본값)
    const draftText = page.getByText('임시저장', { exact: true });
    await expect(draftText).toBeVisible();
  });

  test('getByTestId로 테스트 전용 속성 사용', async ({ page }) => {
    // data-testid 속성으로 요소 찾기
    // 프로덕션 코드에 영향 없는 테스트 전용 식별자

    // 티켓 테이블
    const ticketTable = page.getByTestId('ticket-table');
    await expect(ticketTable).toBeVisible();

    // 페이지네이션
    const pagination = page.getByTestId('pagination');
    await expect(pagination).toBeVisible();

    // 페이지 헤더
    const pageHeader = page.getByTestId('page-header');
    await expect(pageHeader).toBeVisible();
    await expect(pageHeader).toContainText('티켓 목록');

    // 검색 영역
    const searchArea = page.getByTestId('search-area');
    await expect(searchArea).toBeVisible();
  });

  test('getByPlaceholder로 placeholder 찾기', async ({ page }) => {
    // placeholder 속성으로 입력 필드 찾기
    // 레이블이 없는 경우 유용

    const searchInput = page.getByPlaceholder('검색어를 입력하세요');
    await expect(searchInput).toBeVisible();

    // 입력 및 확인
    await searchInput.fill('Playwright 테스트');
    await expect(searchInput).toHaveValue('Playwright 테스트');

    // clear 후 placeholder 다시 확인
    await searchInput.clear();
    await expect(searchInput).toHaveAttribute('placeholder', '검색어를 입력하세요');
  });

  test('filter로 조건부 로케이터', async ({ page }) => {
    // filter를 사용하여 특정 조건을 만족하는 요소만 선택

    const ticketTable = page.getByTestId('ticket-table');
    const allRows = ticketTable.locator('tbody tr');

    // 전체 행 개수 확인
    const totalCount = await allRows.count();
    expect(totalCount).toBeGreaterThan(0);

    // "CICD" 텍스트를 포함하는 행만 필터링
    const cicdRows = allRows.filter({ hasText: 'CICD' });
    const cicdCount = await cicdRows.count();

    console.log(`전체 티켓: ${totalCount}, CICD 티켓: ${cicdCount}`);

    // CICD 티켓이 하나 이상 있어야 함
    expect(cicdCount).toBeGreaterThan(0);

    // 첫 번째 CICD 티켓 확인
    const firstCicdRow = cicdRows.first();
    await expect(firstCicdRow).toContainText('CICD');

    // has 옵션으로 특정 요소를 포함하는 행 필터링
    const rowsWithBadge = allRows.filter({
      has: page.locator('.status-badge')
    });
    const badgeCount = await rowsWithBadge.count();
    expect(badgeCount).toBeGreaterThan(0);
  });

  test('nth, first, last로 인덱스 접근', async ({ page }) => {
    // 여러 요소 중 특정 인덱스의 요소 선택

    const ticketTable = page.getByTestId('ticket-table');
    const rows = ticketTable.locator('tbody tr');

    // 총 개수 확인
    const count = await rows.count();
    expect(count).toBeGreaterThan(0);

    // 첫 번째 티켓 행
    const firstRow = rows.first();
    await expect(firstRow).toBeVisible();

    // 마지막 티켓 행
    const lastRow = rows.last();
    await expect(lastRow).toBeVisible();

    // 두 번째 티켓 행 (인덱스 1)
    if (count >= 2) {
      const secondRow = rows.nth(1);
      await expect(secondRow).toBeVisible();

      // 첫 번째와 두 번째가 다른 티켓이어야 함
      const firstText = await firstRow.textContent();
      const secondText = await secondRow.textContent();
      expect(firstText).not.toBe(secondText);
    }

    // 각 행의 티켓 번호 컬럼 확인
    const firstTicketNo = firstRow.locator('td').first();
    await expect(firstTicketNo).toBeVisible();

    const lastTicketNo = lastRow.locator('td').first();
    await expect(lastTicketNo).toBeVisible();

    console.log(`총 ${count}개의 티켓이 표시되었습니다.`);
  });

  test('복합 로케이터 조합', async ({ page }) => {
    // 여러 로케이터를 조합하여 정확한 요소 찾기

    // getByTestId + locator 체이닝
    const tableBody = page.getByTestId('ticket-table').locator('tbody');
    await expect(tableBody).toBeVisible();

    // getByRole + filter
    const enabledButtons = page
      .getByRole('button')
      .filter({ hasText: '등록' });
    const buttonCount = await enabledButtons.count();
    expect(buttonCount).toBeGreaterThanOrEqual(2); // 등록(CI/CD), 등록(PMS)

    // getByLabel + nth
    const inputs = page.locator('input[type="text"]');
    if (await inputs.count() >= 2) {
      const secondInput = inputs.nth(1);
      await expect(secondInput).toBeVisible();
    }

    // filter + first
    const firstCompleteRow = page
      .getByTestId('ticket-table')
      .locator('tbody tr')
      .filter({ hasText: '완료' })
      .first();

    // 완료 상태 티켓이 있으면 확인
    if (await firstCompleteRow.count() > 0) {
      await expect(firstCompleteRow).toContainText('완료');
    }
  });
});
