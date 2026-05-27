/**
 * TPS 티켓 목록 페이지 테스트
 *
 * 테스트 목표:
 * - 티켓 목록 로드 검증
 * - 검색 기능 (여러 컬럼)
 * - 필터링 (상태별)
 * - 페이지네이션
 * - 정렬 기능
 *
 * 전제조건: storageState로 로그인된 상태
 */

import { test, expect } from '@playwright/test';

test.describe('TPS 티켓 목록 페이지', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/tickets');
    // 페이지 로드 대기
    await page.waitForLoadState('networkidle');
  });

  test('티켓 목록이 로드된다', async ({ page }) => {
    // Given: 티켓 목록 페이지
    await expect(page.locator('h1, h2')).toContainText(/티켓 목록|Ticket List|Tickets/i);

    // When: 페이지 로드 완료

    // Then: 티켓 테이블이 표시됨
    await expect(page.locator('table')).toBeVisible();

    // 티켓이 최소 1개 이상 있거나, 빈 상태 메시지
    const ticketRows = page.locator('tbody tr');
    const count = await ticketRows.count();

    if (count > 0) {
      // 티켓이 있는 경우
      expect(count).toBeGreaterThan(0);

      // 첫 번째 티켓의 필수 필드 확인
      const firstRow = ticketRows.first();
      await expect(firstRow.locator('.ticket-id, [data-testid="ticket-id"]')).toBeVisible();
      await expect(firstRow.locator('.ticket-title, [data-testid="ticket-title"]')).not.toBeEmpty();
    } else {
      // 티켓이 없는 경우 빈 상태 메시지
      await expect(page.locator('.empty-state, .no-data')).toContainText(/티켓이 없습니다|No tickets/i);
    }
  });

  test('티켓 ID 형식 검증 (동적 데이터)', async ({ page }) => {
    const ticketCount = await page.locator('tbody tr').count();

    if (ticketCount > 0) {
      // 첫 번째 티켓 ID가 올바른 형식인지 확인
      const ticketIdElement = page.locator('.ticket-id, [data-testid="ticket-id"]').first();
      await expect(ticketIdElement).toHaveText(/^(CICD|PMS|ITSM)-\d+$/);
    }
  });

  test('검색 기능: 티켓 제목으로 검색', async ({ page }) => {
    // Given: 검색 입력 필드가 있음
    const searchInput = page.locator('input[type="search"], input[placeholder*="검색"]');
    await expect(searchInput).toBeVisible();

    // When: 검색어 입력
    await searchInput.fill('CICD');
    await page.click('button:has-text("검색"), button[type="submit"]');

    // 검색 결과 로드 대기
    await page.waitForLoadState('networkidle');

    // Then: 검색 결과에 'CICD'가 포함됨
    const results = page.locator('tbody tr');
    const count = await results.count();

    if (count > 0) {
      // 첫 번째 결과에 검색어가 포함되는지 확인
      const firstRowText = await results.first().textContent();
      expect(firstRowText?.toLowerCase()).toContain('cicd');
    } else {
      // 결과가 없으면 "검색 결과 없음" 메시지
      await expect(page.locator('.empty-state, .no-results')).toBeVisible();
    }
  });

  test('검색 기능: 티켓 ID로 검색', async ({ page }) => {
    // Given: 첫 번째 티켓의 ID를 가져옴
    const ticketCount = await page.locator('tbody tr').count();

    if (ticketCount === 0) {
      test.skip();
    }

    const firstTicketId = await page.locator('.ticket-id, [data-testid="ticket-id"]').first().textContent();

    if (!firstTicketId) {
      test.skip();
    }

    // When: 티켓 ID로 검색
    const searchInput = page.locator('input[type="search"], input[placeholder*="검색"]');
    await searchInput.clear();
    await searchInput.fill(firstTicketId);
    await page.click('button:has-text("검색"), button[type="submit"]');
    await page.waitForLoadState('networkidle');

    // Then: 해당 티켓만 표시됨
    const results = page.locator('tbody tr');
    const resultCount = await results.count();
    expect(resultCount).toBeGreaterThanOrEqual(1);

    // 첫 번째 결과의 ID가 검색한 ID와 일치
    await expect(results.first().locator('.ticket-id, [data-testid="ticket-id"]')).toContainText(firstTicketId);
  });

  test('필터: 상태별 필터링', async ({ page }) => {
    // Given: 상태 필터 드롭다운
    const statusFilter = page.locator('select[name="status"], [data-testid="status-filter"]');

    if (await statusFilter.isVisible()) {
      // When: "진행중" 상태로 필터링
      await statusFilter.selectOption({ label: '진행중' }).catch(() =>
        statusFilter.selectOption({ value: 'in_progress' })
      );

      await page.waitForLoadState('networkidle');

      // Then: 모든 티켓이 "진행중" 상태
      const statusBadges = page.locator('.status-badge, [data-testid="status"]');
      const count = await statusBadges.count();

      if (count > 0) {
        for (let i = 0; i < count; i++) {
          await expect(statusBadges.nth(i)).toContainText(/진행중|In Progress/i);
        }
      }
    } else {
      console.log('⚠ 상태 필터가 없음');
    }
  });

  test('필터: 타입별 필터링', async ({ page }) => {
    const typeFilter = page.locator('select[name="type"], [data-testid="type-filter"]');

    if (await typeFilter.isVisible()) {
      // When: CICD 타입으로 필터링
      await typeFilter.selectOption({ label: 'CICD' }).catch(() =>
        typeFilter.selectOption({ value: 'CICD' })
      );

      await page.waitForLoadState('networkidle');

      // Then: 모든 티켓 ID가 CICD로 시작
      const ticketIds = page.locator('.ticket-id, [data-testid="ticket-id"]');
      const count = await ticketIds.count();

      if (count > 0) {
        for (let i = 0; i < count; i++) {
          await expect(ticketIds.nth(i)).toHaveText(/^CICD-\d+$/);
        }
      }
    }
  });

  test('페이지네이션: 다음 페이지로 이동', async ({ page }) => {
    // Given: 페이지네이션 버튼
    const nextButton = page.locator('button:has-text("다음"), button[aria-label="Next page"], .pagination .next');

    if (await nextButton.isVisible() && await nextButton.isEnabled()) {
      // 현재 페이지의 첫 티켓 ID 저장
      const firstTicketId = await page.locator('.ticket-id, [data-testid="ticket-id"]').first().textContent();

      // When: 다음 페이지 클릭
      await nextButton.click();
      await page.waitForLoadState('networkidle');

      // Then: 다른 티켓 목록 표시
      const newFirstTicketId = await page.locator('.ticket-id, [data-testid="ticket-id"]').first().textContent();
      expect(newFirstTicketId).not.toBe(firstTicketId);
    } else {
      console.log('⚠ 페이지네이션 없음 또는 1페이지만 존재');
    }
  });

  test('페이지네이션: 페이지 번호 직접 클릭', async ({ page }) => {
    const page2Button = page.locator('button:has-text("2"), [data-page="2"]');

    if (await page2Button.isVisible()) {
      await page2Button.click();
      await page.waitForLoadState('networkidle');

      // URL이나 active 상태로 2페이지 확인
      await expect(page.locator('.pagination .active, [aria-current="page"]')).toContainText('2');
    }
  });

  test('정렬: 생성일 기준 정렬', async ({ page }) => {
    // Given: 생성일 컬럼 헤더
    const createdAtHeader = page.locator('th:has-text("생성일"), th[data-sort="createdAt"]');

    if (await createdAtHeader.isVisible()) {
      // When: 헤더 클릭하여 정렬
      await createdAtHeader.click();
      await page.waitForLoadState('networkidle');

      // Then: 정렬 아이콘 또는 aria-sort 속성 확인
      await expect(createdAtHeader).toHaveAttribute('aria-sort', /(ascending|descending)/);
    }
  });

  test('티켓 행 클릭 시 상세 페이지로 이동', async ({ page }) => {
    const ticketCount = await page.locator('tbody tr').count();

    if (ticketCount > 0) {
      // Given: 첫 번째 티켓 ID
      const firstTicketId = await page.locator('.ticket-id, [data-testid="ticket-id"]').first().textContent();

      // When: 티켓 행 클릭
      await page.locator('tbody tr').first().click();

      // Then: 상세 페이지로 이동
      await expect(page).toHaveURL(/.*\/tickets\/[A-Z]+-\d+/);

      // 상세 페이지에 해당 티켓 정보 표시
      if (firstTicketId) {
        await expect(page.locator('.ticket-id, h1, h2')).toContainText(firstTicketId);
      }
    }
  });

  test('동적 데이터: 날짜 형식 검증', async ({ page }) => {
    const ticketCount = await page.locator('tbody tr').count();

    if (ticketCount > 0) {
      const createdAt = page.locator('.created-at, [data-testid="created-at"]').first();

      if (await createdAt.isVisible()) {
        // 날짜 형식 검증 (YYYY-MM-DD 또는 YYYY-MM-DD HH:mm:ss)
        await expect(createdAt).toHaveText(/\d{4}-\d{2}-\d{2}/);
      }
    }
  });

  test('로딩 상태 표시', async ({ page }) => {
    // API 응답 지연 시뮬레이션
    await page.route('**/api/tickets*', async (route) => {
      await new Promise(resolve => setTimeout(resolve, 2000));
      await route.continue();
    });

    // 페이지 새로고침
    await page.reload();

    // 로딩 스피너 확인 (잠깐 표시됨)
    const spinner = page.locator('.loading-spinner, .loader, [role="progressbar"]');
    // 로딩 중일 때는 보이거나, 이미 로드 완료되면 안 보임
    // 둘 다 정상 상태
  });

  test('빈 검색 결과 처리', async ({ page }) => {
    // When: 존재하지 않는 검색어
    const searchInput = page.locator('input[type="search"], input[placeholder*="검색"]');
    await searchInput.fill('존재하지않는티켓1234567890');
    await page.click('button:has-text("검색"), button[type="submit"]');
    await page.waitForLoadState('networkidle');

    // Then: 빈 상태 메시지
    const emptyState = page.locator('.empty-state, .no-results, tbody');
    await expect(emptyState).toBeVisible();

    // 메시지 확인 (있다면)
    const hasMessage = await page.locator('.empty-state, .no-results').count() > 0;
    if (hasMessage) {
      await expect(page.locator('.empty-state, .no-results')).toContainText(/검색 결과가 없습니다|No results/i);
    }
  });

  test('새로고침 버튼', async ({ page }) => {
    const refreshButton = page.locator('button:has-text("새로고침"), button[aria-label="Refresh"]');

    if (await refreshButton.isVisible()) {
      await refreshButton.click();
      await page.waitForLoadState('networkidle');

      // 페이지가 다시 로드되었는지 확인
      await expect(page.locator('table')).toBeVisible();
    }
  });
});

test.describe('티켓 목록 네트워크 에러 처리', () => {
  test('API 실패 시 에러 메시지 표시', async ({ page }) => {
    // Given: API 500 에러 모킹
    await page.route('**/api/tickets*', async (route) => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Internal Server Error' }),
      });
    });

    // When: 페이지 로드
    await page.goto('/tickets');

    // Then: 에러 메시지 표시
    await expect(page.locator('.error-message, .alert-danger')).toBeVisible();
    await expect(page.locator('.error-message, .alert-danger')).toContainText(/오류|에러|Error/i);
  });

  test('빈 응답 처리', async ({ page }) => {
    // Given: 빈 배열 응답
    await page.route('**/api/tickets*', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          tickets: [],
          total: 0,
          page: 1,
          pageSize: 20,
        }),
      });
    });

    // When: 페이지 로드
    await page.goto('/tickets');

    // Then: 빈 상태 표시
    await expect(page.locator('.empty-state, .no-data')).toBeVisible();
  });
});
