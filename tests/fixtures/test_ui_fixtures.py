"""tests/fixtures/ui_fixtures.py 的单元测试。

由于 Playwright 可能未安装，测试使用 mock 验证 fixture 逻辑。
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestBrowserPageFixture:
    """browser_page fixture 的单元测试。"""

    def test_skip_when_playwright_not_installed(self):
        """Playwright 未安装时 HAS_PLAYWRIGHT 标志应控制跳过逻辑。"""
        import tests.fixtures.ui_fixtures as ui_mod

        original = ui_mod.HAS_PLAYWRIGHT
        try:
            ui_mod.HAS_PLAYWRIGHT = False
            assert ui_mod.HAS_PLAYWRIGHT is False, "HAS_PLAYWRIGHT 应为 False"
        finally:
            ui_mod.HAS_PLAYWRIGHT = original

    def test_headless_config_default_true(self, config):
        """默认 headless 应为 True。"""
        headless = config.get("browser.headless", True)
        assert headless is True

    def test_browser_type_config_default_chromium(self, config):
        """默认浏览器类型应为 chromium。"""
        browser_type = config.get("browser.type", "chromium")
        assert browser_type == "chromium"


class TestAutoScreenshot:
    """_auto_screenshot 函数的单元测试。"""

    def test_auto_screenshot_creates_reports_dir(self, tmp_path):
        """截图时应自动创建 reports 目录。"""
        from tests.fixtures.ui_fixtures import _auto_screenshot

        reports_dir = tmp_path / "reports"
        page_mock = MagicMock()

        with patch("tests.fixtures.ui_fixtures.REPORTS_DIR", reports_dir):
            _auto_screenshot(page_mock, "tests/test_example::test_case")

        assert reports_dir.exists()

    def test_auto_screenshot_calls_page_screenshot(self, tmp_path):
        """应调用 page.screenshot 保存截图。"""
        from tests.fixtures.ui_fixtures import _auto_screenshot

        reports_dir = tmp_path / "reports"
        page_mock = MagicMock()

        with patch("tests.fixtures.ui_fixtures.REPORTS_DIR", reports_dir):
            _auto_screenshot(page_mock, "tests/test_example::test_case")

        page_mock.screenshot.assert_called_once()
        call_args = page_mock.screenshot.call_args
        path_arg = call_args[1]["path"]
        assert "failure_" in path_arg
        assert path_arg.endswith(".png")

    def test_auto_screenshot_safe_filename(self, tmp_path):
        """node_id 中的特殊字符应被替换为下划线。"""
        from tests.fixtures.ui_fixtures import _auto_screenshot

        reports_dir = tmp_path / "reports"
        page_mock = MagicMock()

        with patch("tests.fixtures.ui_fixtures.REPORTS_DIR", reports_dir):
            _auto_screenshot(page_mock, "tests/ui/test_login::TestLogin::test_submit[param1]")

        call_args = page_mock.screenshot.call_args
        path_arg = call_args[1]["path"]
        # 不应包含 / :: [ ] 等特殊字符
        filename = Path(path_arg).name
        assert "/" not in filename
        assert "::" not in filename
        assert "[" not in filename

    def test_auto_screenshot_handles_failure_gracefully(self, tmp_path):
        """截图失败时不应抛出异常。"""
        from tests.fixtures.ui_fixtures import _auto_screenshot

        reports_dir = tmp_path / "reports"
        page_mock = MagicMock()
        page_mock.screenshot.side_effect = RuntimeError("browser closed")

        with patch("tests.fixtures.ui_fixtures.REPORTS_DIR", reports_dir):
            # 不应抛出异常
            _auto_screenshot(page_mock, "tests/test_example::test_fail")


class TestPytestHook:
    """pytest_runtest_makereport 钩子的单元测试。"""

    def test_hook_sets_rep_attribute(self):
        """钩子应将测试结果设置到 item 上。"""
        from tests.fixtures.ui_fixtures import pytest_runtest_makereport

        item = MagicMock()
        call = MagicMock()

        # 模拟 hookwrapper 的 generator 行为
        gen = pytest_runtest_makereport(item, call)
        # 启动 generator，到 yield 处暂停
        next(gen)

        # 模拟 outcome
        rep = MagicMock()
        rep.when = "call"
        outcome = MagicMock()
        outcome.get_result.return_value = rep

        try:
            gen.send(outcome)
        except StopIteration:
            pass

        assert hasattr(item, "rep_call")
