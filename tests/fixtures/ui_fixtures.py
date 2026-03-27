"""UI 测试 fixture 模块，提供 Playwright 浏览器页面实例。

提供 browser_page fixture，支持 headless 模式配置、测试结束后自动关闭浏览器、
测试失败时自动截图。若 Playwright 未安装，自动跳过 UI 测试。

需求: 3.1, 3.4, 3.5, 3.6
"""

import logging
from datetime import datetime
from pathlib import Path

import pytest

logger = logging.getLogger(__name__)

# 报告目录（截图保存位置）
REPORTS_DIR = Path(__file__).parent.parent / "reports"


try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


@pytest.fixture
def browser_page(request, config):
    """Playwright 浏览器页面实例 fixture。

    从配置中读取 headless 模式设置，启动 Chromium 浏览器并创建新页面。
    测试结束后自动关闭浏览器；测试失败时自动截取页面截图保存到 reports/ 目录。

    Args:
        request: pytest request 对象，用于获取测试结果信息。
        config: 配置管理器 fixture（来自 conftest.py）。

    Yields:
        Page: Playwright Page 对象。
    """
    if not HAS_PLAYWRIGHT:
        pytest.skip("Playwright 未安装，跳过 UI 测试")

    headless = config.get("browser.headless", True)
    browser_type = config.get("browser.type", "chromium")

    logger.info("启动浏览器: type=%s, headless=%s", browser_type, headless)

    with sync_playwright() as pw:
        launcher = getattr(pw, browser_type, pw.chromium)
        browser = launcher.launch(headless=headless)
        page = browser.new_page()

        yield page

        # 测试失败时自动截图
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            _auto_screenshot(page, request.node.nodeid)

        browser.close()
        logger.info("浏览器已关闭")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):  # noqa: ARG001
    """pytest 钩子：将测试结果附加到 request.node 上，供 fixture 判断是否需要截图。"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def _auto_screenshot(page, node_id: str):
    """测试失败时自动截取页面截图。

    Args:
        page: Playwright Page 对象。
        node_id: pytest 测试节点 ID，用于生成截图文件名。
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # 将 node_id 中的特殊字符替换为下划线，生成安全的文件名
    safe_name = node_id.replace("/", "_").replace("::", "_").replace("[", "_").replace("]", "")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = REPORTS_DIR / f"failure_{safe_name}_{timestamp}.png"

    try:
        page.screenshot(path=str(screenshot_path))
        logger.info("测试失败截图已保存: %s", screenshot_path)
    except Exception:
        logger.warning("测试失败截图保存失败: %s", screenshot_path, exc_info=True)
