"""登录页面 UI 测试模板：展示如何使用 POM + Playwright 编写 UI 测试。

本文件为模板示例，演示 UI 测试的基本结构和写法。
由于当前项目暂无前端页面，所有测试标记为 skip，待前端就绪后可取消跳过直接使用。

需求: 3.2
"""

import pytest

from tests.pages.base_page import BasePage


# ---------------------------------------------------------------------------
# 示例 Page Object —— 登录页面
# ---------------------------------------------------------------------------

class LoginPage(BasePage):
    """登录页面对象，继承 BasePage 封装登录页特有操作。

    选择器需根据实际前端页面调整。
    """

    # 页面元素选择器（示例，需根据实际页面修改）
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-btn"
    ERROR_MESSAGE = ".error-message"
    WELCOME_TEXT = ".welcome"

    def __init__(self, page, base_url: str = "http://localhost:5000"):
        super().__init__(page)
        self.base_url = base_url

    def open(self):
        """打开登录页面。"""
        self.navigate(f"{self.base_url}/login")

    def login(self, username: str, password: str):
        """执行登录操作：填写用户名、密码并点击登录按钮。"""
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        """获取页面上的错误提示文本。"""
        return self.get_text(self.ERROR_MESSAGE)

    def get_welcome_text(self) -> str:
        """获取登录成功后的欢迎文本。"""
        return self.get_text(self.WELCOME_TEXT)


# ---------------------------------------------------------------------------
# UI 测试用例
# ---------------------------------------------------------------------------

# 当前无前端页面，统一跳过；前端就绪后移除此标记即可
_SKIP_REASON = "前端登录页面尚未就绪，UI 测试模板仅作结构示例"
pytestmark = [pytest.mark.ui, pytest.mark.skip(reason=_SKIP_REASON)]


class TestLoginPage:
    """登录页面 UI 测试。"""

    @pytest.fixture(autouse=True)
    def setup_page(self, browser_page, config):
        """每个测试前初始化 LoginPage 对象。"""
        base_url = config.get("api.base_url", "http://localhost:5000")
        self.login_page = LoginPage(browser_page, base_url=base_url)

    def test_login_success(self):
        """正确凭据登录后应跳转到欢迎页面。"""
        self.login_page.open()
        self.login_page.login("admin", "admin123")
        assert "欢迎" in self.login_page.get_welcome_text()

    def test_login_wrong_password(self):
        """错误密码应显示错误提示。"""
        self.login_page.open()
        self.login_page.login("admin", "wrong_password")
        error = self.login_page.get_error_message()
        assert error, "应显示错误提示信息"

    def test_login_empty_fields(self):
        """空用户名和密码应显示错误提示。"""
        self.login_page.open()
        self.login_page.login("", "")
        error = self.login_page.get_error_message()
        assert error, "空字段应显示错误提示"

    def test_login_page_screenshot(self, browser_page):
        """验证截图功能可正常工作。"""
        self.login_page.open()
        self.login_page.screenshot("tests/reports/login_page.png")
