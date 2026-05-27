"""
01. Playwright Python (sync_api) 첫 테스트
TPS 로그인 페이지 스크린샷 자동화
"""
import os
from playwright.sync_api import sync_playwright, expect

def run_test():
    scenario_info = {
        "url": "http://localhost:3002/login",
        "scenario_name": "01-로그인_페이지_검증",
        "test_cases": [
            {"id": "TC-001", "name": "로그인 페이지 접근", "screenshot": "1. 로그인페이지접근.png"},
            {"id": "TC-002", "name": "에러 메시지 확인", "screenshot": "2. 에러메시지확인.png"},
            {"id": "TC-003", "name": "로그인 성공", "screenshot": "3. 로그인성공.png"},
        ]
    }

    screenshot_base = f"./screenshots/{scenario_info['scenario_name']}"
    os.makedirs(screenshot_base, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})

        # TC-001: 로그인 페이지 접근
        page.goto(scenario_info['url'])
        expect(page.get_by_role("button", name="로그인")).to_be_visible()
        page.screenshot(path=f"{screenshot_base}/{scenario_info['test_cases'][0]['screenshot']}")
        print(f"✅ {scenario_info['test_cases'][0]['name']} 완료")

        # TC-002: 잘못된 로그인 → 에러 메시지
        page.get_by_label("아이디").fill("wrong")
        page.get_by_label("비밀번호").fill("wrong")
        page.get_by_role("button", name="로그인").click()
        page.wait_for_timeout(1000)
        page.screenshot(path=f"{screenshot_base}/{scenario_info['test_cases'][1]['screenshot']}")
        print(f"✅ {scenario_info['test_cases'][1]['name']} 완료")

        # TC-003: 올바른 로그인 → 티켓 목록
        page.get_by_label("아이디").clear()
        page.get_by_label("아이디").fill("admin")
        page.get_by_label("비밀번호").clear()
        page.get_by_label("비밀번호").fill("admin123")
        page.get_by_role("button", name="로그인").click()
        page.wait_for_url("**/tickets")
        page.screenshot(path=f"{screenshot_base}/{scenario_info['test_cases'][2]['screenshot']}")
        print(f"✅ {scenario_info['test_cases'][2]['name']} 완료")

        browser.close()
        print(f"\n📸 스크린샷 저장: {screenshot_base}/")

if __name__ == "__main__":
    run_test()
