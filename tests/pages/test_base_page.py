"""BasePage 单元测试，使用 mock 模拟 Playwright Page 对象。"""

from unittest.mock import MagicMock, patch
from tests.pages.base_page import BasePage


class TestBasePage:
    """BasePage 方法委托与行为验证。"""

    def setup_method(self):
        self.mock_page = MagicMock()
        self.base_page = BasePage(self.mock_page)

    def test_navigate_calls_goto(self):
        self.base_page.navigate("https://example.com")
        self.mock_page.goto.assert_called_once_with("https://example.com")

    def test_click_calls_page_click(self):
        self.base_page.click("#submit")
        self.mock_page.click.assert_called_once_with("#submit")

    def test_fill_calls_page_fill(self):
        self.base_page.fill("#username", "admin")
        self.mock_page.fill.assert_called_once_with("#username", "admin")

    def test_get_text_returns_text_content(self):
        self.mock_page.text_content.return_value = "Hello"
        result = self.base_page.get_text(".title")
        self.mock_page.text_content.assert_called_once_with(".title")
        assert result == "Hello"

    def test_get_text_returns_empty_string_when_none(self):
        self.mock_page.text_content.return_value = None
        result = self.base_page.get_text(".missing")
        assert result == ""

    def test_wait_for_uses_default_timeout(self):
        self.base_page.wait_for(".loader")
        self.mock_page.wait_for_selector.assert_called_once_with(
            ".loader", timeout=5000
        )

    def test_wait_for_uses_custom_timeout(self):
        self.base_page.wait_for(".loader", timeout=10000)
        self.mock_page.wait_for_selector.assert_called_once_with(
            ".loader", timeout=10000
        )

    def test_screenshot_calls_page_screenshot(self):
        self.base_page.screenshot("reports/shot.png")
        self.mock_page.screenshot.assert_called_once_with(path="reports/shot.png")

    def test_screenshot_logs_warning_on_failure(self):
        self.mock_page.screenshot.side_effect = RuntimeError("disk full")
        # Should not raise — just logs a warning
        self.base_page.screenshot("reports/shot.png")

    def test_page_attribute_stored(self):
        assert self.base_page.page is self.mock_page
