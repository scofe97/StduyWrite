import { test, expect } from '@playwright/test';

/**
 * 02-3 ~ 02-6. 다이얼로그, iframe, Shadow DOM, 동적 콘텐츠 테스트
 *
 * - 다이얼로그: alert, confirm, prompt 처리
 * - iframe: frameLocator로 iframe 내부 접근
 * - Shadow DOM: Shadow Root 내부 요소 접근
 * - 동적 콘텐츠: 지연 로드, 상태 변화 대기
 */

test.describe('02-3. 다이얼로그 처리', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3002/components');
  });

  test('alert 다이얼로그 처리', async ({ page }) => {
    // alert 다이얼로그 리스너 등록
    page.on('dialog', async dialog => {
      console.log(`Dialog type: ${dialog.type()}`);
      console.log(`Dialog message: ${dialog.message()}`);

      // alert 타입 확인
      expect(dialog.type()).toBe('alert');
      expect(dialog.message()).toContain('알림');

      // 다이얼로그 수락
      await dialog.accept();
    });

    // alert 트리거 버튼 클릭
    await page.getByRole('button', { name: 'Alert 열기' }).click();

    // 다이얼로그가 처리된 후 페이지 상태 확인
    await expect(page.getByText('Alert이 닫혔습니다')).toBeVisible({ timeout: 3000 });
  });

  test('confirm 다이얼로그 - 확인', async ({ page }) => {
    // confirm 다이얼로그 리스너 (확인)
    page.once('dialog', async dialog => {
      expect(dialog.type()).toBe('confirm');
      expect(dialog.message()).toContain('확인하시겠습니까?');

      // 확인 버튼 클릭
      await dialog.accept();
    });

    await page.getByRole('button', { name: 'Confirm 열기' }).click();

    // 확인 결과 검증
    await expect(page.getByText('사용자가 확인을 선택했습니다')).toBeVisible();
  });

  test('confirm 다이얼로그 - 취소', async ({ page }) => {
    // confirm 다이얼로그 리스너 (취소)
    page.once('dialog', async dialog => {
      expect(dialog.type()).toBe('confirm');

      // 취소 버튼 클릭
      await dialog.dismiss();
    });

    await page.getByRole('button', { name: 'Confirm 열기' }).click();

    // 취소 결과 검증
    await expect(page.getByText('사용자가 취소를 선택했습니다')).toBeVisible();
  });

  test('prompt 다이얼로그 처리', async ({ page }) => {
    const inputText = 'Playwright 테스트';

    // prompt 다이얼로그 리스너
    page.once('dialog', async dialog => {
      expect(dialog.type()).toBe('prompt');
      expect(dialog.message()).toContain('이름을 입력하세요');

      // 기본값 확인
      expect(dialog.defaultValue()).toBeTruthy();

      // 텍스트 입력 후 확인
      await dialog.accept(inputText);
    });

    await page.getByRole('button', { name: 'Prompt 열기' }).click();

    // 입력한 텍스트가 표시되는지 확인
    await expect(page.getByText(`입력값: ${inputText}`)).toBeVisible();
  });

  test('prompt 다이얼로그 - 취소', async ({ page }) => {
    page.once('dialog', async dialog => {
      expect(dialog.type()).toBe('prompt');

      // 취소
      await dialog.dismiss();
    });

    await page.getByRole('button', { name: 'Prompt 열기' }).click();

    // 취소 결과 검증
    await expect(page.getByText('입력이 취소되었습니다')).toBeVisible();
  });

  test('커스텀 모달 처리', async ({ page }) => {
    // 커스텀 모달 열기
    await page.getByRole('button', { name: '모달 열기' }).click();

    // 모달이 표시되는지 확인
    const modal = page.getByTestId('custom-modal');
    await expect(modal).toBeVisible();

    // 모달 제목 확인
    await expect(modal.getByRole('heading', { name: '알림' })).toBeVisible();

    // 모달 내용 확인
    await expect(modal.getByText('이것은 커스텀 모달입니다')).toBeVisible();

    // 모달 닫기 버튼 클릭
    await modal.getByRole('button', { name: '닫기' }).click();

    // 모달이 사라졌는지 확인
    await expect(modal).not.toBeVisible();
  });

  test('여러 다이얼로그 순차 처리', async ({ page }) => {
    let dialogCount = 0;

    page.on('dialog', async dialog => {
      dialogCount++;
      console.log(`Dialog ${dialogCount}: ${dialog.message()}`);
      await dialog.accept();
    });

    // 여러 다이얼로그 트리거
    await page.getByRole('button', { name: '연속 Alert' }).click();

    // 모든 다이얼로그가 처리될 때까지 대기
    await page.waitForTimeout(1000);

    expect(dialogCount).toBeGreaterThan(0);
  });
});

test.describe('02-4. iframe 접근', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3002/components');
  });

  test('iframe 내부 텍스트 읽기', async ({ page }) => {
    // frameLocator로 iframe 접근
    const frame = page.frameLocator('#embedded-frame');

    // iframe 내부 요소 찾기
    const heading = frame.getByRole('heading', { name: 'iframe 콘텐츠' });
    await expect(heading).toBeVisible();

    // iframe 내부 텍스트 확인
    const content = frame.getByText('이것은 iframe 안의 콘텐츠입니다');
    await expect(content).toBeVisible();
  });

  test('iframe 내부 버튼 클릭', async ({ page }) => {
    const frame = page.frameLocator('#embedded-frame');

    // iframe 내부 버튼 찾기
    const button = frame.getByRole('button', { name: 'iframe 버튼' });
    await expect(button).toBeVisible();

    // 클릭
    await button.click();

    // 클릭 후 상태 변화 확인
    const message = frame.getByText('버튼이 클릭되었습니다');
    await expect(message).toBeVisible();
  });

  test('iframe 내부 폼 입력', async ({ page }) => {
    const frame = page.frameLocator('#embedded-frame');

    // iframe 내부 입력 필드
    const nameInput = frame.getByLabel('이름');
    await expect(nameInput).toBeVisible();

    // 입력
    await nameInput.fill('홍길동');

    // 입력값 확인
    await expect(nameInput).toHaveValue('홍길동');

    // 이메일 입력
    const emailInput = frame.getByLabel('이메일');
    await emailInput.fill('test@example.com');
    await expect(emailInput).toHaveValue('test@example.com');

    // 제출 버튼
    const submitButton = frame.getByRole('button', { name: '제출' });
    await submitButton.click();

    // 제출 결과 확인
    const result = frame.getByText('제출 완료');
    await expect(result).toBeVisible();
  });

  test('중첩된 iframe 접근', async ({ page }) => {
    // 외부 iframe
    const outerFrame = page.frameLocator('#outer-frame');

    // 내부 iframe
    const innerFrame = outerFrame.frameLocator('#inner-frame');

    // 가장 내부의 요소 접근
    const deepContent = innerFrame.getByText('중첩된 iframe 콘텐츠');
    await expect(deepContent).toBeVisible();
  });
});

test.describe('02-5. Shadow DOM', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3002/components');
  });

  test('Shadow DOM 내부 요소 접근', async ({ page }) => {
    // Playwright는 자동으로 Shadow DOM을 관통합니다
    // piercing combinator (>>>) 필요 없음

    // Shadow DOM 내부 버튼 찾기
    const shadowButton = page.getByTestId('shadow-button');
    await expect(shadowButton).toBeVisible();

    // Shadow DOM 내부 텍스트
    const shadowText = page.getByText('Shadow DOM 안의 텍스트');
    await expect(shadowText).toBeVisible();
  });

  test('Shadow DOM 내부 입력 필드', async ({ page }) => {
    // Shadow DOM 내부 입력 필드 접근
    const shadowInput = page.locator('[data-testid="shadow-input"]');
    await expect(shadowInput).toBeVisible();

    // 입력
    await shadowInput.fill('Shadow DOM 테스트');
    await expect(shadowInput).toHaveValue('Shadow DOM 테스트');
  });

  test('중첩된 Shadow DOM', async ({ page }) => {
    // 여러 단계의 Shadow DOM도 자동으로 관통
    const nestedElement = page.getByTestId('nested-shadow-element');
    await expect(nestedElement).toBeVisible();
  });
});

test.describe('02-6. 동적 콘텐츠 대기', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3002/components');
  });

  test('지연 콘텐츠 로드 대기', async ({ page }) => {
    // 지연 로드 트리거
    await page.getByRole('button', { name: '지연 콘텐츠 로드' }).click();

    // 3초 후에 나타나는 콘텐츠 대기
    const delayedContent = page.getByText('3초 후에 나타난 콘텐츠');

    // Playwright는 자동으로 대기 (기본 30초 타임아웃)
    await expect(delayedContent).toBeVisible({ timeout: 5000 });

    // 로딩 인디케이터가 사라졌는지 확인
    const loader = page.getByTestId('loading-spinner');
    await expect(loader).not.toBeVisible();
  });

  test('카운터 값 변화 대기', async ({ page }) => {
    // 카운터 시작
    await page.getByRole('button', { name: '카운터 시작' }).click();

    const counter = page.getByTestId('counter-value');

    // 초기값 확인
    await expect(counter).toHaveText('0');

    // 값이 5가 될 때까지 대기
    await expect(counter).toHaveText('5', { timeout: 6000 });

    // 카운터 정지
    await page.getByRole('button', { name: '카운터 정지' }).click();
  });

  test('요소 토글 테스트', async ({ page }) => {
    const toggleButton = page.getByRole('button', { name: '토글' });
    const toggleTarget = page.getByTestId('toggle-target');

    // 초기 상태 확인 (숨김)
    await expect(toggleTarget).not.toBeVisible();

    // 토글 - 표시
    await toggleButton.click();
    await expect(toggleTarget).toBeVisible();

    // 토글 - 숨김
    await toggleButton.click();
    await expect(toggleTarget).not.toBeVisible();

    // 여러 번 토글
    for (let i = 0; i < 3; i++) {
      await toggleButton.click();
      await expect(toggleTarget).toBeVisible();
      await toggleButton.click();
      await expect(toggleTarget).not.toBeVisible();
    }
  });

  test('AJAX 요청 후 콘텐츠 업데이트', async ({ page }) => {
    // API 응답 대기
    const responsePromise = page.waitForResponse(
      response => response.url().includes('/api/data') && response.status() === 200
    );

    // AJAX 요청 트리거
    await page.getByRole('button', { name: '데이터 가져오기' }).click();

    // 응답 대기
    await responsePromise;

    // 데이터가 표시되는지 확인
    const dataList = page.getByTestId('data-list');
    await expect(dataList).toBeVisible();

    // 리스트 아이템 확인
    const items = dataList.locator('li');
    expect(await items.count()).toBeGreaterThan(0);
  });

  test('네트워크 유휴 상태 대기', async ({ page }) => {
    // 복잡한 페이지 로드
    await page.getByRole('button', { name: '복잡한 콘텐츠 로드' }).click();

    // 네트워크가 유휴 상태가 될 때까지 대기
    await page.waitForLoadState('networkidle');

    // 모든 콘텐츠가 로드되었는지 확인
    const sections = page.locator('[data-loaded="true"]');
    const count = await sections.count();
    expect(count).toBeGreaterThan(0);
  });

  test('요소 상태 변화 대기', async ({ page }) => {
    const submitButton = page.getByRole('button', { name: '처리 시작' });

    // 초기 상태: 활성화
    await expect(submitButton).toBeEnabled();

    // 버튼 클릭
    await submitButton.click();

    // 처리 중: 비활성화
    await expect(submitButton).toBeDisabled();

    // 처리 완료: 다시 활성화
    await expect(submitButton).toBeEnabled({ timeout: 5000 });

    // 완료 메시지 확인
    await expect(page.getByText('처리가 완료되었습니다')).toBeVisible();
  });

  test('특정 속성 값 변화 대기', async ({ page }) => {
    const progressBar = page.getByTestId('progress-bar');

    // 진행률 시작
    await page.getByRole('button', { name: '작업 시작' }).click();

    // 진행률이 0%에서 시작
    await expect(progressBar).toHaveAttribute('data-progress', '0');

    // 50%까지 대기
    await expect(progressBar).toHaveAttribute('data-progress', '50', { timeout: 3000 });

    // 100% 완료까지 대기
    await expect(progressBar).toHaveAttribute('data-progress', '100', { timeout: 6000 });

    // 완료 상태 확인
    await expect(progressBar).toHaveClass(/complete/);
  });

  test('DOM 변화 감지', async ({ page }) => {
    // 리스트 컨테이너
    const list = page.getByTestId('dynamic-list');

    // 초기 아이템 수
    const initialCount = await list.locator('li').count();

    // 아이템 추가 버튼
    await page.getByRole('button', { name: '아이템 추가' }).click();

    // 새 아이템이 추가될 때까지 대기
    await expect(list.locator('li')).toHaveCount(initialCount + 1);

    // 여러 아이템 추가
    for (let i = 0; i < 3; i++) {
      await page.getByRole('button', { name: '아이템 추가' }).click();
    }

    // 총 4개 추가되었는지 확인
    await expect(list.locator('li')).toHaveCount(initialCount + 4);
  });
});
