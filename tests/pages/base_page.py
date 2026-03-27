"""
Page Object Model 基类，基于 Playwright 封装常用页面操作。

提供 navigate、click、fill、get_text、wait_for、screenshot 等方法，
所有页面对象应继承此基类。
"""

import logging

logger = logging.getLogger(__name__)


class BasePage:
    """页面对象基类，封装 Playwright Page 的常用操作。"""

    def __init__(self, page):
        """
        初始化页面对象。

        Args:
            page: Playwright Page 对象
        """
        self.page = page

    def navigate(self, url: str):
        """
        导航到指定 URL。

        Args:
            url: 目标页面地址
        """
        logger.info("导航到: %s", url)
        self.page.goto(url)

    def click(self, selector: str):
        """
        点击指定元素。

        Args:
            selector: CSS 或 Playwright 选择器
        """
        logger.debug("点击元素: %s", selector)
        self.page.click(selector)

    def fill(self, selector: str, value: str):
        """
        向输入框填入文本。

        Args:
            selector: CSS 或 Playwright 选择器
            value: 要填入的文本
        """
        logger.debug("填入 '%s' 到元素: %s", value, selector)
        self.page.fill(selector, value)

    def get_text(self, selector: str) -> str:
        """
        获取元素的文本内容。

        Args:
            selector: CSS 或 Playwright 选择器

        Returns:
            元素的文本内容
        """
        text = self.page.text_content(selector)
        logger.debug("获取元素 '%s' 文本: %s", selector, text)
        return text or ""

    def wait_for(self, selector: str, timeout: int = 5000):
        """
        等待元素出现在页面上。

        Args:
            selector: CSS 或 Playwright 选择器
            timeout: 超时时间（毫秒），默认 5000
        """
        logger.debug("等待元素: %s (超时: %dms)", selector, timeout)
        self.page.wait_for_selector(selector, timeout=timeout)

    def screenshot(self, path: str):
        """
        截取当前页面截图并保存。

        Args:
            path: 截图保存路径
        """
        try:
            self.page.screenshot(path=path)
            logger.info("截图已保存: %s", path)
        except Exception as e:
            logger.warning("截图保存失败: %s - %s", path, e)
