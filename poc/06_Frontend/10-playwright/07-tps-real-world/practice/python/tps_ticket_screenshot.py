#!/usr/bin/env python3
"""
TPS 티켓 페이지 스크린샷 자동 캡처 스크립트

기능:
- Playwright Sync API 사용
- 로그인 후 티켓 목록 페이지 스크린샷 캡처
- 전체 페이지 스크린샷 및 개별 티켓 캡처
- 에러 처리 및 로깅

사용법:
    python tps_ticket_screenshot.py

필수 패키지:
    pip install playwright
    playwright install chromium
"""

import os
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from pathlib import Path


class TPSScreenshotCapture:
    """TPS 스크린샷 캡처 클래스"""

    def __init__(self, base_url: str = "http://localhost:3002"):
        """
        Args:
            base_url: TPS 서버 URL (기본값: Mock 서버)
        """
        self.base_url = base_url
        self.screenshot_dir = Path(__file__).parent.parent.parent.parent / "screenshots"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 로그인 정보
        self.username = os.getenv("TPS_USERNAME", "admin")
        self.password = os.getenv("TPS_PASSWORD", "admin123")

    def setup_screenshot_dir(self):
        """스크린샷 디렉토리 생성"""
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 스크린샷 디렉토리: {self.screenshot_dir}")

    def login(self, page: Page) -> bool:
        """
        TPS 로그인 수행

        Args:
            page: Playwright Page 객체

        Returns:
            bool: 로그인 성공 여부
        """
        try:
            print(f"🔐 로그인 시도: {self.username}")

            # 로그인 페이지로 이동
            page.goto(f"{self.base_url}/login")
            page.wait_for_load_state("networkidle")

            # 로그인 폼 입력
            page.fill("#username", self.username)
            page.fill("#password", self.password)

            # 제출 버튼 클릭
            page.click('button[type="submit"]')

            # 대시보드 페이지 로드 대기
            page.wait_for_url("**/dashboard", timeout=10000)

            print("✅ 로그인 성공")
            return True

        except Exception as e:
            print(f"❌ 로그인 실패: {str(e)}")
            # 에러 스크린샷 저장
            error_path = self.screenshot_dir / f"login_error_{self.timestamp}.png"
            page.screenshot(path=str(error_path))
            print(f"   에러 스크린샷: {error_path}")
            return False

    def capture_ticket_list(self, page: Page):
        """
        티켓 목록 페이지 스크린샷 캡처

        Args:
            page: Playwright Page 객체
        """
        try:
            print("📋 티켓 목록 페이지로 이동...")

            # 티켓 목록 페이지로 이동
            page.goto(f"{self.base_url}/tickets")
            page.wait_for_load_state("networkidle")

            # 테이블이 로드될 때까지 대기
            page.wait_for_selector("table, tbody tr", timeout=10000)
            print("✅ 페이지 로드 완료")

            # 전체 페이지 스크린샷
            full_page_path = self.screenshot_dir / f"ticket_list_full_{self.timestamp}.png"
            page.screenshot(path=str(full_page_path), full_page=True)
            print(f"📸 전체 페이지 스크린샷: {full_page_path}")

            # 뷰포트 크기 스크린샷 (스크롤 없이)
            viewport_path = self.screenshot_dir / f"ticket_list_viewport_{self.timestamp}.png"
            page.screenshot(path=str(viewport_path))
            print(f"📸 뷰포트 스크린샷: {viewport_path}")

        except Exception as e:
            print(f"❌ 티켓 목록 캡처 실패: {str(e)}")
            error_path = self.screenshot_dir / f"ticket_list_error_{self.timestamp}.png"
            page.screenshot(path=str(error_path))
            raise

    def capture_individual_tickets(self, page: Page, max_tickets: int = 5):
        """
        개별 티켓 행 스크린샷 캡처

        Args:
            page: Playwright Page 객체
            max_tickets: 캡처할 최대 티켓 수
        """
        try:
            print(f"🎯 개별 티켓 캡처 (최대 {max_tickets}개)...")

            # 티켓 행 가져오기
            ticket_rows = page.locator("tbody tr")
            count = ticket_rows.count()

            if count == 0:
                print("⚠️  티켓이 없습니다")
                return

            print(f"   총 {count}개 티켓 발견")

            # 상위 N개 티켓 캡처
            for i in range(min(count, max_tickets)):
                try:
                    row = ticket_rows.nth(i)

                    # 티켓 ID 추출
                    ticket_id_element = row.locator(".ticket-id, [data-testid='ticket-id']")
                    ticket_id = ticket_id_element.text_content().strip()

                    # 티켓 행 스크린샷
                    ticket_path = self.screenshot_dir / f"ticket_{ticket_id}_{self.timestamp}.png"
                    row.screenshot(path=str(ticket_path))

                    print(f"   📸 티켓 {i+1}/{min(count, max_tickets)}: {ticket_id} → {ticket_path.name}")

                except Exception as e:
                    print(f"   ⚠️  티켓 {i+1} 캡처 실패: {str(e)}")
                    continue

        except Exception as e:
            print(f"❌ 개별 티켓 캡처 실패: {str(e)}")

    def capture_ticket_details(self, page: Page):
        """
        첫 번째 티켓의 상세 페이지 캡처

        Args:
            page: Playwright Page 객체
        """
        try:
            print("🔍 티켓 상세 페이지 캡처...")

            # 첫 번째 티켓 클릭
            first_ticket = page.locator("tbody tr").first()
            ticket_id = first_ticket.locator(".ticket-id, [data-testid='ticket-id']").text_content().strip()

            first_ticket.click()
            page.wait_for_load_state("networkidle")

            # 상세 페이지 스크린샷
            detail_path = self.screenshot_dir / f"ticket_detail_{ticket_id}_{self.timestamp}.png"
            page.screenshot(path=str(detail_path), full_page=True)
            print(f"📸 티켓 상세: {detail_path}")

            # 목록으로 돌아가기
            page.go_back()
            page.wait_for_load_state("networkidle")

        except Exception as e:
            print(f"⚠️  티켓 상세 캡처 실패: {str(e)}")

    def run(self):
        """메인 실행 함수"""
        print("=" * 60)
        print("🚀 TPS 티켓 스크린샷 자동 캡처 시작")
        print("=" * 60)
        print(f"🌐 대상 URL: {self.base_url}")
        print(f"👤 사용자: {self.username}")
        print()

        # 스크린샷 디렉토리 생성
        self.setup_screenshot_dir()

        with sync_playwright() as p:
            # 브라우저 시작 (headless 모드)
            print("🌐 브라우저 시작 (headless)...")
            browser: Browser = p.chromium.launch(headless=True)

            # 컨텍스트 및 페이지 생성
            context: BrowserContext = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (TPS Screenshot Bot)"
            )
            page: Page = context.new_page()

            try:
                # 1. 로그인
                if not self.login(page):
                    print("❌ 로그인 실패로 종료")
                    sys.exit(1)

                # 2. 티켓 목록 스크린샷
                self.capture_ticket_list(page)

                # 3. 개별 티켓 스크린샷
                self.capture_individual_tickets(page, max_tickets=5)

                # 4. 티켓 상세 페이지 스크린샷
                self.capture_ticket_details(page)

                print()
                print("=" * 60)
                print("✅ 모든 스크린샷 캡처 완료!")
                print("=" * 60)
                print(f"📁 저장 위치: {self.screenshot_dir}")
                print()

                # 저장된 파일 목록 출력
                screenshots = sorted(self.screenshot_dir.glob(f"*_{self.timestamp}.png"))
                print(f"📸 캡처된 스크린샷 ({len(screenshots)}개):")
                for screenshot in screenshots:
                    size_kb = screenshot.stat().st_size / 1024
                    print(f"   - {screenshot.name} ({size_kb:.1f} KB)")

            except Exception as e:
                print()
                print("=" * 60)
                print(f"❌ 오류 발생: {str(e)}")
                print("=" * 60)

                # 최종 에러 스크린샷
                final_error_path = self.screenshot_dir / f"final_error_{self.timestamp}.png"
                page.screenshot(path=str(final_error_path))
                print(f"📸 에러 스크린샷: {final_error_path}")

                sys.exit(1)

            finally:
                # 브라우저 종료
                browser.close()
                print()
                print("👋 브라우저 종료")


def main():
    """메인 진입점"""
    # 환경변수에서 URL 가져오기 (없으면 기본값)
    base_url = os.getenv("TPS_BASE_URL", "http://localhost:3002")

    # 스크린샷 캡처 실행
    capture = TPSScreenshotCapture(base_url=base_url)
    capture.run()


if __name__ == "__main__":
    main()
