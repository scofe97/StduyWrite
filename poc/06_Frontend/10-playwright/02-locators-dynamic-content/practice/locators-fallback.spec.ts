import { test, expect } from '@playwright/test';

/**
 * 02-2. CSS/XPath 폴백 전략
 *
 * getBy* 로케이터로 찾기 어려운 경우 사용하는 폴백 전략:
 * - CSS 셀렉터: 클래스, ID, 속성 기반
 * - XPath: 복잡한 DOM 구조 탐색
 * - has/hasText 필터: 조건부 선택
 * - 로케이터 체이닝: 단계적 탐색
 */

test.describe('02-2. CSS/XPath 폴백', () => {
  test.beforeEach(async ({ page }) => {
    // 로그인 후 티켓 목록 페이지로 이동
    await page.goto('http://localhost:3002/login');
    await page.getByLabel('아이디').fill('admin');
    await page.getByLabel('비밀번호').fill('password123');
    await page.getByRole('button', { name: '로그인' }).click();
    await page.waitForURL('**/tickets');
  });

  test('CSS 셀렉터로 클래스 기반 접근', async ({ page }) => {
    // 클래스 셀렉터 (.class-name)
    const statusBadges = page.locator('.status-badge');
    const badgeCount = await statusBadges.count();
    expect(badgeCount).toBeGreaterThan(0);

    // 첫 번째 뱃지 확인
    const firstBadge = statusBadges.first();
    await expect(firstBadge).toBeVisible();

    // ID 셀렉터 (#id)
    const searchKeyword = page.locator('#searchKeyword');
    await expect(searchKeyword).toBeVisible();
    await searchKeyword.fill('테스트 키워드');
    await expect(searchKeyword).toHaveValue('테스트 키워드');

    // 복합 클래스 셀렉터
    const statusComplete = page.locator('.status-badge.badge-complete');
    if (await statusComplete.count() > 0) {
      await expect(statusComplete.first()).toBeVisible();
    }

    // 태그 + 클래스
    const tableElements = page.locator('table.ticket-table');
    await expect(tableElements.first()).toBeVisible();
  });

  test('CSS 속성 셀렉터', async ({ page }) => {
    // 속성 존재 여부 [attr]
    const elementsWithTestId = page.locator('[data-testid]');
    const testIdCount = await elementsWithTestId.count();
    expect(testIdCount).toBeGreaterThan(0);

    // 속성 값 정확히 일치 [attr="value"]
    const ticketTable = page.locator('[data-testid="ticket-table"]');
    await expect(ticketTable).toBeVisible();

    // 속성 값 포함 [attr*="value"]
    const statusElements = page.locator('[data-status*="COMPLETE"]');
    if (await statusElements.count() > 0) {
      await expect(statusElements.first()).toBeVisible();
    }

    // 속성 값 시작 [attr^="value"]
    const searchInputs = page.locator('[id^="search"]');
    expect(await searchInputs.count()).toBeGreaterThan(0);

    // 속성 값 끝 [attr$="value"]
    const idInputs = page.locator('[name$="Id"]');
    if (await idInputs.count() > 0) {
      await expect(idInputs.first()).toBeVisible();
    }

    // 여러 속성 조합
    const textInputs = page.locator('input[type="text"][placeholder]');
    expect(await textInputs.count()).toBeGreaterThan(0);
  });

  test('CSS 결합자', async ({ page }) => {
    // 자손 결합자 (공백): 모든 하위 요소
    const tableCells = page.locator('.ticket-table td');
    expect(await tableCells.count()).toBeGreaterThan(0);

    // 자식 결합자 (>): 직계 자식만
    const directChildren = page.locator('.ticket-table > tbody');
    await expect(directChildren).toBeVisible();

    // 인접 형제 결합자 (+): 바로 다음 형제
    // 예: label 다음의 input
    const adjacentInput = page.locator('label + input');
    if (await adjacentInput.count() > 0) {
      await expect(adjacentInput.first()).toBeVisible();
    }

    // 일반 형제 결합자 (~): 이후 모든 형제
    const siblingElements = page.locator('.search-area ~ .ticket-list');
    if (await siblingElements.count() > 0) {
      await expect(siblingElements.first()).toBeVisible();
    }

    // 가상 클래스 :first-child
    const firstRow = page.locator('.ticket-table tbody tr:first-child');
    await expect(firstRow).toBeVisible();

    // 가상 클래스 :last-child
    const lastRow = page.locator('.ticket-table tbody tr:last-child');
    await expect(lastRow).toBeVisible();

    // 가상 클래스 :nth-child(n)
    const secondRow = page.locator('.ticket-table tbody tr:nth-child(2)');
    if (await page.locator('.ticket-table tbody tr').count() >= 2) {
      await expect(secondRow).toBeVisible();
    }
  });

  test('XPath로 복잡한 구조 탐색', async ({ page }) => {
    // 절대 경로 (비권장: 구조 변경에 취약)
    // 상대 경로 권장

    // 텍스트 포함하는 요소 찾기
    const cicdRows = page.locator('//table//tr[contains(.,"CICD")]');
    if (await cicdRows.count() > 0) {
      await expect(cicdRows.first()).toBeVisible();
      await expect(cicdRows.first()).toContainText('CICD');
    }

    // 속성으로 찾기
    const testIdElements = page.locator('//*[@data-testid="ticket-table"]');
    await expect(testIdElements).toBeVisible();

    // 부모 요소 탐색 (..)
    const parentElement = page.locator('//table[@data-testid="ticket-table"]/..');
    await expect(parentElement).toBeVisible();

    // 형제 요소 탐색 (following-sibling)
    const nextSibling = page.locator('//div[@class="search-area"]/following-sibling::div');
    if (await nextSibling.count() > 0) {
      await expect(nextSibling.first()).toBeVisible();
    }

    // 조건부 선택
    const completedTickets = page.locator('//tr[.//td[contains(@class,"badge-complete")]]');
    if (await completedTickets.count() > 0) {
      console.log(`완료된 티켓: ${await completedTickets.count()}개`);
    }

    // 텍스트 정확히 일치
    const exactText = page.locator('//button[text()="등록(CI/CD)"]');
    await expect(exactText).toBeVisible();

    // AND 조건
    const complexXPath = page.locator('//input[@type="text" and @placeholder]');
    expect(await complexXPath.count()).toBeGreaterThan(0);
  });

  test('has/hasText 필터 조합', async ({ page }) => {
    // hasText: 특정 텍스트를 포함하는 요소
    const rowsWithCICD = page.locator('tr').filter({ hasText: 'CICD' });
    if (await rowsWithCICD.count() > 0) {
      await expect(rowsWithCICD.first()).toContainText('CICD');
    }

    // has: 특정 자식 요소를 포함하는 요소
    const rowsWithBadge = page.locator('tr').filter({
      has: page.locator('.status-badge')
    });
    const badgeRowCount = await rowsWithBadge.count();
    expect(badgeRowCount).toBeGreaterThan(0);

    // 복합 조건: has + hasText
    const completedRows = page.locator('tr').filter({
      has: page.locator('.badge-complete')
    }).filter({
      hasText: 'CICD'
    });

    if (await completedRows.count() > 0) {
      const firstCompleted = completedRows.first();
      await expect(firstCompleted).toContainText('CICD');
      await expect(firstCompleted).toContainText('완료');
    }

    // not() 필터: 특정 조건 제외
    const nonDraftRows = page.locator('tr').filter({
      hasNot: page.locator('.badge-draft')
    });
    expect(await nonDraftRows.count()).toBeGreaterThan(0);

    // 중첩 필터
    const specificRows = page
      .locator('.ticket-table tbody tr')
      .filter({ hasText: 'CICD' })
      .filter({ has: page.locator('.status-badge') })
      .first();

    if (await page.locator('.ticket-table tbody tr').filter({ hasText: 'CICD' }).count() > 0) {
      await expect(specificRows).toBeVisible();
    }
  });

  test('로케이터 체이닝 패턴', async ({ page }) => {
    // 1단계: 테이블 찾기
    const table = page.getByTestId('ticket-table');
    await expect(table).toBeVisible();

    // 2단계: tbody 찾기
    const tbody = table.locator('tbody');
    await expect(tbody).toBeVisible();

    // 3단계: tr 찾기
    const rows = tbody.locator('tr');
    const rowCount = await rows.count();
    expect(rowCount).toBeGreaterThan(0);

    // 4단계: 첫 번째 행 선택
    const firstRow = rows.first();
    await expect(firstRow).toBeVisible();

    // 5단계: 첫 번째 행의 셀들
    const cells = firstRow.locator('td');
    const cellCount = await cells.count();
    expect(cellCount).toBe(7); // 7개 컬럼

    // 한 번에 체이닝
    const firstTicketNo = page
      .getByTestId('ticket-table')
      .locator('tbody')
      .locator('tr')
      .first()
      .locator('td')
      .first();

    await expect(firstTicketNo).toBeVisible();

    // 특정 조건의 요소 체이닝
    const firstCICDTicketStatus = page
      .getByTestId('ticket-table')
      .locator('tbody tr')
      .filter({ hasText: 'CICD' })
      .first()
      .locator('.status-badge');

    if (await page.locator('tbody tr').filter({ hasText: 'CICD' }).count() > 0) {
      await expect(firstCICDTicketStatus).toBeVisible();
    }
  });

  test('성능 비교: CSS vs XPath', async ({ page }) => {
    // CSS 셀렉터 (일반적으로 더 빠름)
    const cssStart = Date.now();
    const cssElements = page.locator('.ticket-table tbody tr');
    const cssCount = await cssElements.count();
    const cssDuration = Date.now() - cssStart;

    // XPath (더 강력하지만 일반적으로 느림)
    const xpathStart = Date.now();
    const xpathElements = page.locator('//table[@data-testid="ticket-table"]//tbody//tr');
    const xpathCount = await xpathElements.count();
    const xpathDuration = Date.now() - xpathStart;

    // 결과 검증
    expect(cssCount).toBe(xpathCount);

    console.log(`CSS: ${cssCount}개 (${cssDuration}ms)`);
    console.log(`XPath: ${xpathCount}개 (${xpathDuration}ms)`);
    console.log(`권장: 간단한 구조는 CSS, 복잡한 조건은 XPath`);
  });

  test('실전 패턴: 상태별 티켓 카운트', async ({ page }) => {
    const table = page.getByTestId('ticket-table');
    const allRows = table.locator('tbody tr');
    const total = await allRows.count();

    // CSS 클래스로 상태별 카운트
    const draftCount = await allRows.filter({
      has: page.locator('.badge-draft')
    }).count();

    const progressCount = await allRows.filter({
      has: page.locator('.badge-progress')
    }).count();

    const completeCount = await allRows.filter({
      has: page.locator('.badge-complete')
    }).count();

    const failCount = await allRows.filter({
      has: page.locator('.badge-fail')
    }).count();

    console.log('=== 티켓 상태 통계 ===');
    console.log(`전체: ${total}개`);
    console.log(`임시저장: ${draftCount}개`);
    console.log(`진행중: ${progressCount}개`);
    console.log(`완료: ${completeCount}개`);
    console.log(`실패: ${failCount}개`);

    // 합계 검증 (모든 티켓이 하나의 상태를 가져야 함)
    const statusTotal = draftCount + progressCount + completeCount + failCount;
    expect(statusTotal).toBeLessThanOrEqual(total);
  });
});
