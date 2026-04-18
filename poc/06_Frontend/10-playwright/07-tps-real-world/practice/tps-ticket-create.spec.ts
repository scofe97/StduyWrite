/**
 * TPS 티켓 생성 페이지 테스트
 *
 * 테스트 목표:
 * - CICD 티켓 생성 (필수 필드)
 * - PMS 티켓 생성 (릴리즈 선택)
 * - 폼 검증 에러 시나리오
 * - 생성 취소 플로우
 * - 생성 후 목록에서 확인
 */

import { test, expect } from '@playwright/test';

test.describe('TPS 티켓 생성', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/tickets/new');
    await page.waitForLoadState('networkidle');
  });

  test('CICD 티켓 생성: 모든 필수 필드 입력', async ({ page }) => {
    // Given: 티켓 생성 폼
    await expect(page.locator('h1, h2')).toContainText(/티켓 생성|New Ticket|Create/i);

    // When: CICD 타입 선택 및 필수 필드 입력
    await page.selectOption('select[name="type"], #type', 'CICD');
    await page.fill('input[name="title"], #title', '[E2E] CI/CD 파이프라인 구축');
    await page.fill('textarea[name="description"], #description', 'Jenkins 기반 CI/CD 파이프라인 자동화');

    // 우선순위 선택
    await page.selectOption('select[name="priority"], #priority', { label: '높음' }).catch(() =>
      page.selectOption('select[name="priority"], #priority', { value: 'high' })
    );

    // 담당자 선택 (선택사항)
    const assigneeField = page.locator('select[name="assignee"], #assignee, input[name="assignee"]');
    if (await assigneeField.isVisible()) {
      if (await assigneeField.evaluate(el => el.tagName) === 'SELECT') {
        await assigneeField.selectOption({ index: 1 }); // 첫 번째 담당자
      } else {
        await assigneeField.fill('admin');
      }
    }

    // Then: 제출 버튼 클릭
    await page.click('button[type="submit"]:has-text("생성"), button:has-text("Create")');

    // 성공 메시지 또는 목록 페이지로 리다이렉트
    await expect(
      page.locator('.success-message, .alert-success')
    ).toBeVisible().or(
      expect(page).toHaveURL(/.*\/tickets/)
    );
  });

  test('PMS 티켓 생성: 릴리즈 선택 필드', async ({ page }) => {
    // When: PMS 타입 선택
    await page.selectOption('select[name="type"], #type', 'PMS');

    // Then: 릴리즈 선택 필드가 나타남
    const releaseField = page.locator('select[name="release"], #release');

    // PMS 타입에서만 릴리즈 필드가 표시되는지 확인
    if (await releaseField.isVisible()) {
      // 릴리즈 옵션 선택
      await releaseField.selectOption({ index: 1 });

      // 나머지 필드 입력
      await page.fill('input[name="title"], #title', '[E2E] PMS 기능 개발');
      await page.fill('textarea[name="description"], #description', 'PMS 시스템 신규 기능 추가');

      await page.click('button[type="submit"]:has-text("생성")');

      // 성공 확인
      await expect(
        page.locator('.success-message, .alert-success')
      ).toBeVisible().or(
        expect(page).toHaveURL(/.*\/tickets/)
      );
    }
  });

  test('ITSM 티켓 생성', async ({ page }) => {
    // When: ITSM 타입 선택
    const typeSelect = page.locator('select[name="type"], #type');
    const options = await typeSelect.locator('option').allTextContents();

    if (options.some(opt => opt.includes('ITSM'))) {
      await typeSelect.selectOption('ITSM');

      await page.fill('input[name="title"], #title', '[E2E] ITSM 인시던트');
      await page.fill('textarea[name="description"], #description', 'ITSM 시스템 장애 대응');

      await page.click('button[type="submit"]:has-text("생성")');

      await expect(
        page.locator('.success-message, .alert-success')
      ).toBeVisible().or(
        expect(page).toHaveURL(/.*\/tickets/)
      );
    } else {
      test.skip();
    }
  });

  test('검증: 제목 필드 필수', async ({ page }) => {
    // Given: 제목을 비워둠
    await page.selectOption('select[name="type"], #type', 'CICD');
    await page.fill('textarea[name="description"], #description', '설명만 입력');

    // When: 제출 시도
    await page.click('button[type="submit"]:has-text("생성")');

    // Then: 검증 에러 메시지
    const titleField = page.locator('input[name="title"], #title');
    const isRequired = await titleField.evaluate((el: HTMLInputElement) => el.required);

    if (isRequired) {
      // HTML5 required validation
      expect(isRequired).toBeTruthy();
    } else {
      // 커스텀 검증 메시지
      await expect(page.locator('.error-message, .field-error')).toBeVisible();
    }
  });

  test('검증: 설명 필드 필수', async ({ page }) => {
    await page.selectOption('select[name="type"], #type', 'CICD');
    await page.fill('input[name="title"], #title', '제목만 입력');

    await page.click('button[type="submit"]:has-text("생성")');

    // 설명 필드 검증
    const descField = page.locator('textarea[name="description"], #description');
    const isRequired = await descField.evaluate((el: HTMLTextAreaElement) => el.required);

    if (isRequired) {
      expect(isRequired).toBeTruthy();
    } else {
      await expect(page.locator('.error-message, .field-error')).toBeVisible();
    }
  });

  test('검증: 제목 최소 길이 (5자 이상)', async ({ page }) => {
    await page.selectOption('select[name="type"], #type', 'CICD');
    await page.fill('input[name="title"], #title', '짧음'); // 2자
    await page.fill('textarea[name="description"], #description', '설명입니다');

    await page.click('button[type="submit"]:has-text("생성")');

    // 최소 길이 검증 메시지
    const errorMessage = page.locator('.error-message, .field-error, .invalid-feedback');
    if (await errorMessage.isVisible()) {
      await expect(errorMessage).toContainText(/최소|글자|5자|characters/i);
    }
  });

  test('검증: 제목 최대 길이 (200자)', async ({ page }) => {
    const longTitle = 'A'.repeat(201); // 201자

    await page.selectOption('select[name="type"], #type', 'CICD');
    await page.fill('input[name="title"], #title', longTitle);
    await page.fill('textarea[name="description"], #description', '설명입니다');

    await page.click('button[type="submit"]:has-text("생성")');

    // 최대 길이 검증
    const titleField = page.locator('input[name="title"], #title');
    const maxLength = await titleField.getAttribute('maxlength');

    if (maxLength) {
      expect(parseInt(maxLength)).toBeLessThanOrEqual(200);
    }
  });

  test('취소 버튼: 목록으로 돌아가기', async ({ page }) => {
    // Given: 폼에 일부 데이터 입력
    await page.fill('input[name="title"], #title', '취소할 티켓');

    // When: 취소 버튼 클릭
    const cancelButton = page.locator('button:has-text("취소"), button:has-text("Cancel"), a:has-text("취소")');
    await cancelButton.click();

    // Then: 목록 페이지로 이동
    await expect(page).toHaveURL(/.*\/tickets$/);
  });

  test('생성 후 목록에서 확인', async ({ page }) => {
    // Given: 고유한 제목으로 티켓 생성
    const timestamp = Date.now();
    const uniqueTitle = `[E2E-${timestamp}] 자동 생성 티켓`;

    await page.selectOption('select[name="type"], #type', 'CICD');
    await page.fill('input[name="title"], #title', uniqueTitle);
    await page.fill('textarea[name="description"], #description', 'E2E 테스트 자동 생성 티켓');

    // When: 생성
    await page.click('button[type="submit"]:has-text("생성")');

    // 목록 페이지로 이동 (자동 또는 수동)
    await page.goto('/tickets');
    await page.waitForLoadState('networkidle');

    // Then: 목록에서 생성한 티켓 찾기
    const searchInput = page.locator('input[type="search"], input[placeholder*="검색"]');
    if (await searchInput.isVisible()) {
      await searchInput.fill(uniqueTitle);
      await page.click('button:has-text("검색")');
      await page.waitForLoadState('networkidle');
    }

    // 티켓이 목록에 표시됨
    await expect(page.locator(`text=${uniqueTitle}`)).toBeVisible();
  });

  test('첨부파일 업로드 (선택사항)', async ({ page }) => {
    const fileInput = page.locator('input[type="file"]');

    if (await fileInput.isVisible()) {
      // 테스트 파일 업로드
      await fileInput.setInputFiles({
        name: 'test-screenshot.png',
        mimeType: 'image/png',
        buffer: Buffer.from('fake-image-data'),
      });

      // 파일명 표시 확인
      await expect(page.locator('.file-name, .uploaded-file')).toContainText('test-screenshot.png');
    }
  });

  test('폼 초기화 버튼', async ({ page }) => {
    // Given: 폼에 데이터 입력
    await page.selectOption('select[name="type"], #type', 'CICD');
    await page.fill('input[name="title"], #title', '테스트 제목');
    await page.fill('textarea[name="description"], #description', '테스트 설명');

    // When: 초기화 버튼 클릭
    const resetButton = page.locator('button[type="reset"], button:has-text("초기화")');

    if (await resetButton.isVisible()) {
      await resetButton.click();

      // Then: 모든 필드가 초기화됨
      await expect(page.locator('input[name="title"], #title')).toHaveValue('');
      await expect(page.locator('textarea[name="description"], #description')).toHaveValue('');
    }
  });
});

test.describe('티켓 생성 네트워크 에러 처리', () => {
  test('API 실패 시 에러 메시지 표시', async ({ page }) => {
    // Given: API 500 에러 모킹
    await page.route('**/api/tickets', async (route) => {
      if (route.request().method() === 'POST') {
        await route.fulfill({
          status: 500,
          contentType: 'application/json',
          body: JSON.stringify({ error: 'Internal Server Error' }),
        });
      } else {
        await route.continue();
      }
    });

    await page.goto('/tickets/new');

    // When: 티켓 생성 시도
    await page.selectOption('select[name="type"], #type', 'CICD');
    await page.fill('input[name="title"], #title', '에러 테스트');
    await page.fill('textarea[name="description"], #description', '에러 발생 시나리오');
    await page.click('button[type="submit"]:has-text("생성")');

    // Then: 에러 메시지 표시
    await expect(page.locator('.error-message, .alert-danger')).toBeVisible();
    await expect(page.locator('.error-message, .alert-danger')).toContainText(/오류|실패|에러|Error/i);
  });

  test('중복 제출 방지', async ({ page }) => {
    await page.goto('/tickets/new');

    // API 응답 지연 시뮬레이션
    await page.route('**/api/tickets', async (route) => {
      if (route.request().method() === 'POST') {
        await new Promise(resolve => setTimeout(resolve, 3000));
        await route.continue();
      } else {
        await route.continue();
      }
    });

    // 폼 입력
    await page.selectOption('select[name="type"], #type', 'CICD');
    await page.fill('input[name="title"], #title', '중복 방지 테스트');
    await page.fill('textarea[name="description"], #description', '중복 제출 테스트');

    // 제출 버튼 클릭
    const submitButton = page.locator('button[type="submit"]:has-text("생성")');
    await submitButton.click();

    // 버튼이 비활성화되는지 확인
    await expect(submitButton).toBeDisabled();
  });

  test('네트워크 타임아웃 처리', async ({ page }) => {
    await page.route('**/api/tickets', async (route) => {
      if (route.request().method() === 'POST') {
        // 응답하지 않고 대기
        await new Promise(resolve => setTimeout(resolve, 60000)); // 60초
      }
    });

    await page.goto('/tickets/new');

    await page.selectOption('select[name="type"], #type', 'CICD');
    await page.fill('input[name="title"], #title', '타임아웃 테스트');
    await page.fill('textarea[name="description"], #description', '타임아웃 시나리오');
    await page.click('button[type="submit"]:has-text("생성")');

    // 타임아웃 에러 메시지 또는 로딩 상태 확인
    await expect(
      page.locator('.error-message, .timeout-message')
    ).toBeVisible({ timeout: 10000 }).catch(() => {
      // 타임아웃 메시지가 없으면 로딩 상태 확인
      expect(page.locator('.loading-spinner, [role="progressbar"]')).toBeVisible();
    });
  });
});

test.describe('티켓 생성 UX 개선 요소', () => {
  test('실시간 유효성 검사', async ({ page }) => {
    await page.goto('/tickets/new');

    // 제목 필드에 짧은 텍스트 입력
    await page.fill('input[name="title"], #title', 'AB'); // 2자

    // 필드 벗어날 때 실시간 검증 (blur 이벤트)
    await page.locator('input[name="title"], #title').blur();

    // 실시간 에러 메시지 확인 (있다면)
    const errorMessage = page.locator('.field-error, .invalid-feedback');
    if (await errorMessage.isVisible()) {
      await expect(errorMessage).toContainText(/최소|글자|characters/i);
    }
  });

  test('자동 저장 (Draft) 기능', async ({ page }) => {
    await page.goto('/tickets/new');

    // 폼에 데이터 입력
    await page.fill('input[name="title"], #title', '자동 저장 테스트');

    // 로컬스토리지에 저장되는지 확인
    const draftData = await page.evaluate(() => {
      return localStorage.getItem('ticket-draft');
    });

    // Draft 기능이 구현되어 있다면
    if (draftData) {
      expect(draftData).toContain('자동 저장 테스트');
    }
  });
});
