#!/usr/bin/env python3
"""
Playwright Python - TPS 티켓 목록 로케이터 데모

sync_api를 사용하여 로그인, 티켓 목록 탐색, 검색 기능을 테스트합니다.
"""

import os
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, expect

# 스크린샷 저장 디렉토리
SCREENSHOT_DIR = Path(__file__).parent.parent / "screenshots" / "02-locators"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

def login(page: Page) -> None:
    """TPS 로그인"""
    print("로그인 페이지로 이동...")
    page.goto("http://localhost:3002/login")

    # getByLabel 사용
    print("로그인 정보 입력...")
    page.get_by_label("아이디").fill("admin")
    page.get_by_label("비밀번호").fill("password123")

    # getByRole 사용
    page.get_by_role("button", name="로그인").click()

    # URL 변경 대기
    page.wait_for_url("**/tickets")
    print("✅ 로그인 완료")

def explore_ticket_list(page: Page) -> None:
    """티켓 목록 탐색"""
    print("\n=== 티켓 목록 탐색 ===")

    # getByTestId로 페이지 헤더 확인
    header = page.get_by_test_id("page-header")
    expect(header).to_be_visible()
    print(f"페이지 제목: {header.text_content()}")

    # getByRole로 버튼 찾기
    cicd_button = page.get_by_role("button", name="등록(CI/CD)")
    expect(cicd_button).to_be_visible()
    print("✅ 등록(CI/CD) 버튼 발견")

    pms_button = page.get_by_role("button", name="등록(PMS)")
    expect(pms_button).to_be_visible()
    print("✅ 등록(PMS) 버튼 발견")

    # getByTestId로 테이블 찾기
    table = page.get_by_test_id("ticket-table")
    expect(table).to_be_visible()

    # 티켓 행 카운트
    rows = table.locator("tbody tr")
    row_count = rows.count()
    print(f"✅ 총 {row_count}개의 티켓이 표시됨")

    # 첫 번째 티켓 정보 출력
    if row_count > 0:
        first_row = rows.first
        cells = first_row.locator("td")
        cell_count = cells.count()

        print(f"\n첫 번째 티켓 정보 ({cell_count}개 컬럼):")
        for i in range(min(cell_count, 3)):  # 처음 3개 컬럼만
            cell_text = cells.nth(i).text_content()
            print(f"  컬럼 {i+1}: {cell_text}")

    # 스크린샷
    screenshot_path = SCREENSHOT_DIR / "01-ticket-list.png"
    page.screenshot(path=str(screenshot_path))
    print(f"\n스크린샷 저장: {screenshot_path}")

def test_search_functionality(page: Page) -> None:
    """검색 기능 테스트"""
    print("\n=== 검색 기능 테스트 ===")

    # getByLabel로 검색 컬럼 선택
    column_select = page.get_by_label("검색 컬럼")
    expect(column_select).to_be_visible()
    column_select.select_option("tcktNm")  # 티켓명으로 검색
    print("✅ 검색 컬럼: 티켓명")

    # getByPlaceholder로 검색어 입력 필드 찾기
    search_input = page.get_by_placeholder("검색어를 입력하세요")
    expect(search_input).to_be_visible()
    search_input.fill("CICD")
    print("✅ 검색어 입력: CICD")

    # 검색 버튼 클릭 (getByRole)
    search_button = page.get_by_role("button", name="검색")
    if search_button.is_visible():
        search_button.click()
        page.wait_for_timeout(1000)  # 검색 결과 로드 대기
        print("✅ 검색 실행")

    # 검색 결과 확인
    table = page.get_by_test_id("ticket-table")
    result_rows = table.locator("tbody tr")
    result_count = result_rows.count()
    print(f"✅ 검색 결과: {result_count}개")

    # 검색 결과 스크린샷
    screenshot_path = SCREENSHOT_DIR / "02-search-results.png"
    page.screenshot(path=str(screenshot_path))
    print(f"스크린샷 저장: {screenshot_path}")

def test_status_badges(page: Page) -> None:
    """상태 뱃지 탐색"""
    print("\n=== 상태 뱃지 탐색 ===")

    # 검색 초기화
    search_input = page.get_by_placeholder("검색어를 입력하세요")
    search_input.clear()

    # getByText로 상태 뱃지 찾기
    status_texts = ["완료", "진행중", "임시저장", "실패"]

    for status in status_texts:
        elements = page.get_by_text(status, exact=True)
        count = elements.count()
        if count > 0:
            print(f"✅ '{status}' 상태: {count}개 발견")
        else:
            print(f"  '{status}' 상태: 없음")

    # CSS 클래스로 뱃지 카운트
    table = page.get_by_test_id("ticket-table")
    all_rows = table.locator("tbody tr")

    # filter로 특정 조건의 행 찾기
    draft_rows = all_rows.filter(has=page.locator(".badge-draft"))
    progress_rows = all_rows.filter(has=page.locator(".badge-progress"))
    complete_rows = all_rows.filter(has=page.locator(".badge-complete"))
    fail_rows = all_rows.filter(has=page.locator(".badge-fail"))

    print("\nCSS 클래스 기반 카운트:")
    print(f"  임시저장: {draft_rows.count()}개")
    print(f"  진행중: {progress_rows.count()}개")
    print(f"  완료: {complete_rows.count()}개")
    print(f"  실패: {fail_rows.count()}개")

def test_pagination(page: Page) -> None:
    """페이지네이션 테스트"""
    print("\n=== 페이지네이션 테스트 ===")

    # getByTestId로 페이지네이션 찾기
    pagination = page.get_by_test_id("pagination")

    if pagination.is_visible():
        print("✅ 페이지네이션 발견")

        # 페이지 번호 버튼들
        page_buttons = pagination.locator("button")
        button_count = page_buttons.count()
        print(f"  페이지 버튼: {button_count}개")

        # 현재 페이지 확인
        active_page = pagination.locator(".active, [aria-current='page']")
        if active_page.count() > 0:
            current_page = active_page.text_content()
            print(f"  현재 페이지: {current_page}")

        # 스크린샷
        screenshot_path = SCREENSHOT_DIR / "03-pagination.png"
        page.screenshot(path=str(screenshot_path))
        print(f"스크린샷 저장: {screenshot_path}")
    else:
        print("  페이지네이션 없음 (데이터가 적거나 단일 페이지)")

def test_locator_chaining(page: Page) -> None:
    """로케이터 체이닝 패턴"""
    print("\n=== 로케이터 체이닝 ===")

    # 체이닝: getByTestId → locator → first → locator
    first_ticket_no = (
        page.get_by_test_id("ticket-table")
        .locator("tbody")
        .locator("tr")
        .first
        .locator("td")
        .first
    )

    if first_ticket_no.is_visible():
        ticket_no = first_ticket_no.text_content()
        print(f"✅ 첫 번째 티켓 번호: {ticket_no}")

    # CICD 티켓 필터링
    cicd_rows = (
        page.get_by_test_id("ticket-table")
        .locator("tbody tr")
        .filter(has_text="CICD")
    )

    cicd_count = cicd_rows.count()
    print(f"✅ CICD 티켓: {cicd_count}개")

    if cicd_count > 0:
        # 첫 번째 CICD 티켓의 상태 확인
        first_cicd_status = cicd_rows.first.locator(".status-badge")
        if first_cicd_status.is_visible():
            status_text = first_cicd_status.text_content()
            print(f"  첫 번째 CICD 티켓 상태: {status_text}")

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("Playwright Python - TPS 로케이터 데모")
    print("=" * 60)

    with sync_playwright() as playwright:
        # 브라우저 실행
        browser = playwright.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        try:
            # 1. 로그인
            login(page)

            # 2. 티켓 목록 탐색
            explore_ticket_list(page)

            # 3. 검색 기능
            test_search_functionality(page)

            # 4. 상태 뱃지
            test_status_badges(page)

            # 5. 페이지네이션
            test_pagination(page)

            # 6. 로케이터 체이닝
            test_locator_chaining(page)

            print("\n" + "=" * 60)
            print("✅ 모든 테스트 완료!")
            print(f"스크린샷 저장 위치: {SCREENSHOT_DIR}")
            print("=" * 60)

            # 결과 확인을 위해 3초 대기
            page.wait_for_timeout(3000)

        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            # 오류 스크린샷
            error_screenshot = SCREENSHOT_DIR / "error.png"
            page.screenshot(path=str(error_screenshot))
            print(f"오류 스크린샷: {error_screenshot}")
            raise

        finally:
            # 브라우저 종료
            browser.close()

if __name__ == "__main__":
    main()
