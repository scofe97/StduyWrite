/**
 * TPS 전체 워크플로우 E2E 테스트
 *
 * 테스트 목표:
 * - 완전한 사용자 여정 검증
 * - 로그인 → 생성 → 조회 → 수정 → 검증
 * - 다중 페이지 네비게이션
 * - 상태 유지 확인
 */

import { test, expect } from '@playwright/test';

test.describe('TPS 티켓 관리 전체 워크플로우', () => {
  let createdTicketId: string | null = null;

  test('시나리오 1: 티켓 생성 → 목록 확인 → 상세 보기', async ({ page }) => {
    // Step 1: 티켓 생성 페이지로 이동
    await page.goto('/tickets/new');
    await expect(page.locator('h1, h2')).toContainText(/티켓 생성|New Ticket/i);

    // Step 2: CICD 티켓 생성
    const timestamp = Date.now();
    const ticketTitle = `[E2E-WF-${timestamp}] CI/CD 파이프라인 구축`;

    await page.selectOption('select[name="type"], #type', 'CICD');
    await page.fill('input[name="title"], #title', ticketTitle);
    await page.fill('textarea[name="description"], #description', '워크플로우 테스트용 티켓입니다.');

    await page.click('button[type="submit"]:has-text("생성")');

    // Step 3: 생성 성공 확인
    await expect(
      page.locator('.success-message, .alert-success')
    ).toBeVisible().or(
      expect(page).toHaveURL(/.*\/tickets/)
    );

    // Step 4: 티켓 목록 페이지로 이동
    await page.goto('/tickets');
    await page.waitForLoadState('networkidle');

    // Step 5: 생성한 티켓 검색
    const searchInput = page.locator('input[type="search"], input[placeholder*="검색"]');
    if (await searchInput.isVisible()) {
      await searchInput.fill(ticketTitle);
      await page.click('button:has-text("검색")');
      await page.waitForLoadState('networkidle');
    }

    // Step 6: 검색 결과에서 티켓 확인
    const ticketRow = page.locator(`tbody tr:has-text("${ticketTitle}")`).first();
    await expect(ticketRow).toBeVisible();

    // 티켓 ID 추출
    const ticketIdElement = ticketRow.locator('.ticket-id, [data-testid="ticket-id"]');
    createdTicketId = await ticketIdElement.textContent();

    // Step 7: 티켓 클릭하여 상세 페이지로 이동
    await ticketRow.click();

    // Step 8: 상세 페이지 검증
    await expect(page).toHaveURL(/.*\/tickets\/[A-Z]+-\d+/);
    await expect(page.locator('.ticket-detail, .ticket-info')).toBeVisible();
    await expect(page.locator('h1, h2, .ticket-title')).toContainText(ticketTitle);

    if (createdTicketId) {
      await expect(page.locator('.ticket-id, [data-testid="ticket-id"]')).toContainText(createdTicketId);
    }
  });

  test('시나리오 2: 티켓 수정 → 변경사항 검증', async ({ page }) => {
    // Step 1: 티켓 목록에서 첫 번째 티켓 선택
    await page.goto('/tickets');
    await page.waitForLoadState('networkidle');

    const ticketCount = await page.locator('tbody tr').count();
    if (ticketCount === 0) {
      test.skip();
    }

    // Step 2: 첫 번째 티켓의 ID 저장
    const firstTicketId = await page.locator('.ticket-id, [data-testid="ticket-id"]').first().textContent();
    await page.locator('tbody tr').first().click();

    // Step 3: 상세 페이지에서 수정 버튼 클릭
    await expect(page).toHaveURL(/.*\/tickets\/[A-Z]+-\d+/);

    const editButton = page.locator('button:has-text("수정"), button:has-text("Edit"), a:has-text("수정")');
    if (await editButton.isVisible()) {
      await editButton.click();

      // Step 4: 수정 폼에서 상태 변경
      const statusSelect = page.locator('select[name="status"], #status');
      if (await statusSelect.isVisible()) {
        await statusSelect.selectOption({ label: '진행중' }).catch(() =>
          statusSelect.selectOption({ value: 'in_progress' })
        );
      }

      // Step 5: 저장
      await page.click('button[type="submit"]:has-text("저장"), button:has-text("Save")');

      // Step 6: 변경사항 확인
      await expect(page.locator('.status-badge, [data-testid="status"]')).toContainText(/진행중|In Progress/i);
    }
  });

  test('시나리오 3: 필터링 → 상세 보기 → 뒤로가기', async ({ page }) => {
    // Step 1: 티켓 목록 페이지
    await page.goto('/tickets');
    await page.waitForLoadState('networkidle');

    // Step 2: CICD 타입으로 필터링
    const typeFilter = page.locator('select[name="type"], [data-testid="type-filter"]');
    if (await typeFilter.isVisible()) {
      await typeFilter.selectOption({ label: 'CICD' }).catch(() =>
        typeFilter.selectOption({ value: 'CICD' })
      );
      await page.waitForLoadState('networkidle');
    }

    // Step 3: 필터링된 결과 확인
    const ticketCount = await page.locator('tbody tr').count();
    if (ticketCount > 0) {
      // Step 4: 첫 번째 티켓 클릭
      await page.locator('tbody tr').first().click();
      await expect(page).toHaveURL(/.*\/tickets\/CICD-\d+/);

      // Step 5: 뒤로가기
      await page.goBack();

      // Step 6: 필터가 유지되는지 확인
      await expect(page).toHaveURL(/.*\/tickets/);
      // 필터 상태 확인 (구현에 따라 다를 수 있음)
    }
  });

  test('시나리오 4: 다중 페이지 네비게이션', async ({ page }) => {
    // Step 1: 대시보드에서 시작
    await page.goto('/dashboard');
    await expect(page.locator('h1, h2')).toContainText(/대시보드|Dashboard/i);

    // Step 2: 티켓 목록으로 이동 (네비게이션 메뉴)
    const ticketsNavLink = page.locator('a:has-text("티켓"), a:has-text("Tickets"), nav a[href*="tickets"]');
    if (await ticketsNavLink.first().isVisible()) {
      await ticketsNavLink.first().click();
      await expect(page).toHaveURL(/.*\/tickets/);
    }

    // Step 3: 티켓 생성 페이지로 이동
    const newTicketButton = page.locator('button:has-text("새 티켓"), a:has-text("티켓 생성"), [data-testid="new-ticket"]');
    if (await newTicketButton.isVisible()) {
      await newTicketButton.click();
      await expect(page).toHaveURL(/.*\/tickets\/new/);
    }

    // Step 4: 취소하고 목록으로 돌아가기
    const cancelButton = page.locator('button:has-text("취소"), a:has-text("취소")');
    if (await cancelButton.isVisible()) {
      await cancelButton.click();
      await expect(page).toHaveURL(/.*\/tickets$/);
    }
  });

  test('시나리오 5: 검색 → 페이지네이션 → 정렬', async ({ page }) => {
    await page.goto('/tickets');
    await page.waitForLoadState('networkidle');

    // Step 1: 검색
    const searchInput = page.locator('input[type="search"], input[placeholder*="검색"]');
    if (await searchInput.isVisible()) {
      await searchInput.fill('CICD');
      await page.click('button:has-text("검색")');
      await page.waitForLoadState('networkidle');

      // Step 2: 검색 결과 확인
      const resultCount = await page.locator('tbody tr').count();
      if (resultCount > 0) {
        // Step 3: 페이지네이션 (있다면)
        const nextButton = page.locator('button:has-text("다음"), .pagination .next');
        if (await nextButton.isVisible() && await nextButton.isEnabled()) {
          await nextButton.click();
          await page.waitForLoadState('networkidle');

          // 검색어가 유지되는지 확인
          await expect(searchInput).toHaveValue('CICD');
        }

        // Step 4: 정렬
        const createdAtHeader = page.locator('th:has-text("생성일"), th[data-sort="createdAt"]');
        if (await createdAtHeader.isVisible()) {
          await createdAtHeader.click();
          await page.waitForLoadState('networkidle');

          // 검색어가 여전히 유지되는지 확인
          await expect(searchInput).toHaveValue('CICD');
        }
      }
    }
  });

  test('시나리오 6: 상태 전환 워크플로우', async ({ page }) => {
    // 티켓의 생명주기: 접수 → 진행중 → 완료

    // Step 1: 새 티켓 생성 (기본 상태: 접수)
    await page.goto('/tickets/new');
    const timestamp = Date.now();
    const ticketTitle = `[E2E-State-${timestamp}] 상태 전환 테스트`;

    await page.selectOption('select[name="type"], #type', 'CICD');
    await page.fill('input[name="title"], #title', ticketTitle);
    await page.fill('textarea[name="description"], #description', '상태 전환 워크플로우 테스트');
    await page.click('button[type="submit"]:has-text("생성")');

    // Step 2: 목록에서 찾아서 상세 페이지로 이동
    await page.goto('/tickets');
    await page.waitForLoadState('networkidle');

    const searchInput = page.locator('input[type="search"], input[placeholder*="검색"]');
    if (await searchInput.isVisible()) {
      await searchInput.fill(ticketTitle);
      await page.click('button:has-text("검색")');
      await page.waitForLoadState('networkidle');
    }

    await page.locator(`tbody tr:has-text("${ticketTitle}")`).first().click();

    // Step 3: 초기 상태 확인 (접수)
    await expect(page.locator('.status-badge, [data-testid="status"]')).toContainText(/접수|Open|New/i);

    // Step 4: 진행중으로 변경
    const editButton = page.locator('button:has-text("수정"), button:has-text("Edit")');
    if (await editButton.isVisible()) {
      await editButton.click();

      const statusSelect = page.locator('select[name="status"], #status');
      await statusSelect.selectOption({ label: '진행중' }).catch(() =>
        statusSelect.selectOption({ value: 'in_progress' })
      );

      await page.click('button[type="submit"]:has-text("저장")');
      await expect(page.locator('.status-badge, [data-testid="status"]')).toContainText(/진행중|In Progress/i);
    }

    // Step 5: 완료로 변경
    if (await editButton.isVisible()) {
      await editButton.click();

      const statusSelect = page.locator('select[name="status"], #status');
      await statusSelect.selectOption({ label: '완료' }).catch(() =>
        statusSelect.selectOption({ value: 'completed' })
      );

      await page.click('button[type="submit"]:has-text("저장")');
      await expect(page.locator('.status-badge, [data-testid="status"]')).toContainText(/완료|Completed|Done/i);
    }
  });
});

test.describe('복잡한 사용자 시나리오', () => {
  test('시나리오 7: 댓글 추가 및 확인 (선택사항)', async ({ page }) => {
    await page.goto('/tickets');
    const ticketCount = await page.locator('tbody tr').count();

    if (ticketCount > 0) {
      await page.locator('tbody tr').first().click();
      await expect(page).toHaveURL(/.*\/tickets\/[A-Z]+-\d+/);

      // 댓글 입력 필드 확인
      const commentField = page.locator('textarea[name="comment"], textarea[placeholder*="댓글"]');

      if (await commentField.isVisible()) {
        // 댓글 작성
        await commentField.fill('E2E 테스트 댓글입니다.');
        await page.click('button:has-text("댓글 작성"), button:has-text("등록")');

        // 댓글 목록에서 확인
        await expect(page.locator('.comment-list, .comments')).toContainText('E2E 테스트 댓글입니다.');
      }
    }
  });

  test('시나리오 8: 티켓 삭제 워크플로우 (관리자 전용)', async ({ page }) => {
    // Admin으로 로그인된 경우에만 테스트
    const timestamp = Date.now();
    const ticketTitle = `[E2E-Delete-${timestamp}] 삭제 테스트`;

    // 임시 티켓 생성
    await page.goto('/tickets/new');
    await page.selectOption('select[name="type"], #type', 'CICD');
    await page.fill('input[name="title"], #title', ticketTitle);
    await page.fill('textarea[name="description"], #description', '삭제될 티켓입니다.');
    await page.click('button[type="submit"]:has-text("생성")');

    // 목록에서 찾기
    await page.goto('/tickets');
    const searchInput = page.locator('input[type="search"], input[placeholder*="검색"]');
    if (await searchInput.isVisible()) {
      await searchInput.fill(ticketTitle);
      await page.click('button:has-text("검색")');
      await page.waitForLoadState('networkidle');
    }

    await page.locator(`tbody tr:has-text("${ticketTitle}")`).first().click();

    // 삭제 버튼 확인
    const deleteButton = page.locator('button:has-text("삭제"), button[data-action="delete"]');

    if (await deleteButton.isVisible()) {
      await deleteButton.click();

      // 확인 다이얼로그
      const confirmDialog = page.locator('.modal, .dialog, [role="dialog"]');
      if (await confirmDialog.isVisible()) {
        await page.click('button:has-text("확인"), button:has-text("삭제")');
      }

      // 목록으로 리다이렉트
      await expect(page).toHaveURL(/.*\/tickets/);

      // 삭제된 티켓이 목록에 없는지 확인
      await searchInput.fill(ticketTitle);
      await page.click('button:has-text("검색")');
      await page.waitForLoadState('networkidle');

      const emptyState = page.locator('.empty-state, .no-results');
      await expect(emptyState).toBeVisible();
    }
  });

  test('시나리오 9: 여러 필터 조합', async ({ page }) => {
    await page.goto('/tickets');
    await page.waitForLoadState('networkidle');

    // 타입 필터
    const typeFilter = page.locator('select[name="type"], [data-testid="type-filter"]');
    if (await typeFilter.isVisible()) {
      await typeFilter.selectOption({ value: 'CICD' });
      await page.waitForLoadState('networkidle');
    }

    // 상태 필터
    const statusFilter = page.locator('select[name="status"], [data-testid="status-filter"]');
    if (await statusFilter.isVisible()) {
      await statusFilter.selectOption({ label: '진행중' }).catch(() =>
        statusFilter.selectOption({ value: 'in_progress' })
      );
      await page.waitForLoadState('networkidle');
    }

    // 검색어 추가
    const searchInput = page.locator('input[type="search"], input[placeholder*="검색"]');
    if (await searchInput.isVisible()) {
      await searchInput.fill('파이프라인');
      await page.click('button:has-text("검색")');
      await page.waitForLoadState('networkidle');
    }

    // 결과 확인
    const results = page.locator('tbody tr');
    const count = await results.count();

    if (count > 0) {
      // 모든 결과가 조건에 맞는지 확인
      for (let i = 0; i < Math.min(count, 5); i++) {
        const row = results.nth(i);
        await expect(row.locator('.ticket-id, [data-testid="ticket-id"]')).toHaveText(/^CICD-\d+$/);
        await expect(row.locator('.status-badge, [data-testid="status"]')).toContainText(/진행중|In Progress/i);
      }
    }
  });
});

test.describe('상태 유지 및 브라우저 동작', () => {
  test('페이지 새로고침 후 로그인 상태 유지', async ({ page }) => {
    await page.goto('/tickets');
    await expect(page.locator('table')).toBeVisible();

    // 새로고침
    await page.reload();

    // 로그인 페이지로 리다이렉트되지 않고 티켓 목록이 표시됨
    await expect(page.locator('table')).toBeVisible();
    await expect(page).not.toHaveURL(/.*login/);
  });

  test('브라우저 뒤로가기/앞으로가기', async ({ page }) => {
    // 티켓 목록 → 상세 → 목록 네비게이션
    await page.goto('/tickets');
    const ticketCount = await page.locator('tbody tr').count();

    if (ticketCount > 0) {
      await page.locator('tbody tr').first().click();
      await expect(page).toHaveURL(/.*\/tickets\/[A-Z]+-\d+/);

      // 뒤로가기
      await page.goBack();
      await expect(page).toHaveURL(/.*\/tickets/);

      // 앞으로가기
      await page.goForward();
      await expect(page).toHaveURL(/.*\/tickets\/[A-Z]+-\d+/);
    }
  });

  test('탭 간 세션 공유 (새 탭에서도 로그인 유지)', async ({ context, page }) => {
    await page.goto('/tickets');
    await expect(page.locator('table')).toBeVisible();

    // 새 탭 열기
    const newPage = await context.newPage();
    await newPage.goto('/tickets');

    // 새 탭에서도 로그인 상태 유지
    await expect(newPage.locator('table')).toBeVisible();
    await expect(newPage).not.toHaveURL(/.*login/);

    await newPage.close();
  });
});
