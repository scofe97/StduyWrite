import { Page, Locator } from '@playwright/test';
import { BasePage } from './BasePage';

/**
 * TicketCreatePage - 티켓 생성 페이지 Page Object
 *
 * 경로:
 * - CICD: /tickets/create/cicd
 * - PMS: /tickets/create/pms
 *
 * 주요 기능:
 * - 티켓 기본 정보 입력
 * - Task, Workflow 선택
 * - Repository 추가
 * - 티켓 저장/취소
 * - 검증 에러 확인
 *
 * 사용 예시:
 * ```typescript
 * const createPage = new TicketCreatePage(page);
 * await createPage.goto('/tickets/create/cicd');
 * await createPage.fillTicketName('Jenkins 파이프라인');
 * await createPage.selectTask('BUILD');
 * await createPage.selectWorkflow('CICD_WORKFLOW_01');
 * await createPage.addRepository('https://git.okestro.com/tps/tps-api', 'main');
 * await createPage.save();
 * ```
 */
export class TicketCreatePage extends BasePage {
  // 기본 정보 필드
  readonly tcktNmInput: Locator;
  readonly taskCdSelect: Locator;
  readonly wrkflwCdSelect: Locator;
  readonly devlopPicIdSelect: Locator;

  // Repository 관련
  readonly repoUrlInput: Locator;
  readonly branchNmInput: Locator;
  readonly addRepoButton: Locator;
  readonly repoList: Locator;

  // 액션 버튼
  readonly saveButton: Locator;
  readonly cancelButton: Locator;

  // 검증 에러
  readonly validationErrors: Locator;

  constructor(page: Page) {
    super(page);

    // 기본 정보
    this.tcktNmInput = page.locator('#tcktNm');
    this.taskCdSelect = page.locator('#taskCd');
    this.wrkflwCdSelect = page.locator('#wrkflwCd');
    this.devlopPicIdSelect = page.locator('#devlopPicId');

    // Repository
    this.repoUrlInput = page.locator('#repoUrl');
    this.branchNmInput = page.locator('#branchNm');
    this.addRepoButton = page.locator('#addRepoBtn');
    this.repoList = page.locator('.repo-list');

    // 액션
    this.saveButton = page.locator('#saveBtn');
    this.cancelButton = page.locator('#cancelBtn');

    // 검증 에러
    this.validationErrors = page.locator('.validation-error');
  }

  /**
   * 티켓 생성 페이지로 이동
   * @param path - 경로 (/tickets/create/cicd 또는 /tickets/create/pms)
   */
  async goto(path: string = '/tickets/create/cicd') {
    await super.goto(path);
    await this.waitForPageLoad();
  }

  /**
   * CICD 티켓 생성 페이지로 이동
   */
  async gotoCicd() {
    await this.goto('/tickets/create/cicd');
  }

  /**
   * PMS 티켓 생성 페이지로 이동
   */
  async gotoPms() {
    await this.goto('/tickets/create/pms');
  }

  /**
   * 티켓명 입력
   * @param name - 티켓명
   */
  async fillTicketName(name: string) {
    await this.tcktNmInput.fill(name);
  }

  /**
   * Task 선택
   * @param taskCd - Task 코드 (BUILD, DEPLOY, TEST 등)
   */
  async selectTask(taskCd: string) {
    await this.taskCdSelect.selectOption(taskCd);
  }

  /**
   * Workflow 선택
   * @param wrkflwCd - Workflow 코드
   */
  async selectWorkflow(wrkflwCd: string) {
    await this.wrkflwCdSelect.selectOption(wrkflwCd);
  }

  /**
   * 개발 담당자 선택
   * @param devlopPicId - 개발 담당자 ID
   */
  async selectDeveloper(devlopPicId: string) {
    await this.devlopPicIdSelect.selectOption(devlopPicId);
  }

  /**
   * Repository 추가
   * @param repoUrl - Repository URL
   * @param branchNm - Branch 이름
   */
  async addRepository(repoUrl: string, branchNm: string) {
    await this.repoUrlInput.fill(repoUrl);
    await this.branchNmInput.fill(branchNm);
    await this.addRepoButton.click();
  }

  /**
   * 티켓 기본 정보 일괄 입력
   * @param data - 티켓 데이터
   */
  async fillBasicInfo(data: {
    tcktNm: string;
    taskCd: string;
    wrkflwCd: string;
    devlopPicId?: string;
  }) {
    await this.fillTicketName(data.tcktNm);
    await this.selectTask(data.taskCd);
    await this.selectWorkflow(data.wrkflwCd);

    if (data.devlopPicId) {
      await this.selectDeveloper(data.devlopPicId);
    }
  }

  /**
   * CICD 티켓 전체 폼 입력 (편의 메서드)
   * @param data - CICD 티켓 데이터
   */
  async fillCicdTicket(data: {
    tcktNm: string;
    taskCd: string;
    wrkflwCd: string;
    devlopPicId: string;
    repoUrl: string;
    branchNm: string;
  }) {
    await this.fillBasicInfo({
      tcktNm: data.tcktNm,
      taskCd: data.taskCd,
      wrkflwCd: data.wrkflwCd,
      devlopPicId: data.devlopPicId,
    });

    await this.addRepository(data.repoUrl, data.branchNm);
  }

  /**
   * PMS 티켓 전체 폼 입력 (편의 메서드)
   * @param data - PMS 티켓 데이터
   */
  async fillPmsTicket(data: {
    tcktNm: string;
    taskCd: string;
    wrkflwCd: string;
    devlopPicId: string;
  }) {
    await this.fillBasicInfo(data);
  }

  /**
   * 저장 버튼 클릭
   */
  async save() {
    await this.saveButton.click();
    // 저장 후 목록 페이지로 리디렉션 대기
    await this.page.waitForLoadState('networkidle');
  }

  /**
   * 취소 버튼 클릭
   */
  async cancel() {
    await this.cancelButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  /**
   * 검증 에러 메시지 가져오기
   * @returns 검증 에러 메시지 배열
   */
  async getValidationErrors(): Promise<string[]> {
    const count = await this.validationErrors.count();
    const errors: string[] = [];

    for (let i = 0; i < count; i++) {
      const error = await this.validationErrors.nth(i).textContent();
      if (error) {
        errors.push(error.trim());
      }
    }

    return errors;
  }

  /**
   * 검증 에러가 있는지 확인
   */
  async hasValidationErrors(): Promise<boolean> {
    const count = await this.validationErrors.count();
    return count > 0;
  }

  /**
   * 저장 버튼 활성화 여부 확인
   */
  async isSaveButtonEnabled(): Promise<boolean> {
    return this.saveButton.isEnabled();
  }

  /**
   * 필수 필드가 모두 입력되었는지 확인
   */
  async areRequiredFieldsFilled(): Promise<boolean> {
    const tcktNm = await this.tcktNmInput.inputValue();
    const taskCd = await this.taskCdSelect.inputValue();
    const wrkflwCd = await this.wrkflwCdSelect.inputValue();
    const devlopPicId = await this.devlopPicIdSelect.inputValue();

    return !!(tcktNm && taskCd && wrkflwCd && devlopPicId);
  }

  /**
   * 폼 초기화 여부 확인 (모든 필드가 비어있는지)
   */
  async isFormEmpty(): Promise<boolean> {
    const tcktNm = await this.tcktNmInput.inputValue();
    const taskCd = await this.taskCdSelect.inputValue();
    const wrkflwCd = await this.wrkflwCdSelect.inputValue();

    return !tcktNm && !taskCd && !wrkflwCd;
  }

  /**
   * Repository 개수 확인
   */
  async getRepositoryCount(): Promise<number> {
    return this.page.locator('.repo-item').count();
  }

  /**
   * 특정 인덱스의 Repository 정보 가져오기
   * @param index - Repository 인덱스 (0부터 시작)
   */
  async getRepositoryInfo(index: number): Promise<{ repoUrl: string; branchNm: string }> {
    const repoItem = this.page.locator('.repo-item').nth(index);
    const repoUrl = await repoItem.locator('.repo-url').textContent();
    const branchNm = await repoItem.locator('.branch-nm').textContent();

    return {
      repoUrl: repoUrl?.trim() || '',
      branchNm: branchNm?.trim() || '',
    };
  }

  /**
   * Repository 삭제
   * @param index - 삭제할 Repository 인덱스
   */
  async removeRepository(index: number) {
    const deleteButton = this.page.locator('.repo-item').nth(index).locator('.delete-repo-btn');
    await deleteButton.click();
  }
}
