"""HTTP 响应断言工具模块，提供链式断言 API，支持状态码、JSON 字段、响应时间等断言。"""

import requests


class ResponseAssertions:
    """HTTP 响应断言工具，支持链式调用。

    每个断言方法返回 self，允许链式写法：
        ResponseAssertions(resp).status_code(200).json_field("data.name", "admin")

    Args:
        response: requests.Response 对象
    """

    def __init__(self, response: requests.Response):
        self._response = response

    def status_code(self, expected: int) -> "ResponseAssertions":
        """断言 HTTP 状态码。

        Args:
            expected: 期望的状态码

        Returns:
            self，支持链式调用

        Raises:
            AssertionError: 状态码不匹配时
        """
        actual = self._response.status_code
        assert actual == expected, (
            f"状态码断言失败: 期望 {expected}, 实际 {actual}"
        )
        return self

    def json_field(self, field_path: str, expected) -> "ResponseAssertions":
        """断言 JSON 响应中指定字段的值，支持点号路径。

        例如 field_path="data.user.name" 会依次访问 resp["data"]["user"]["name"]。

        Args:
            field_path: 点号分隔的字段路径
            expected: 期望的字段值

        Returns:
            self，支持链式调用

        Raises:
            AssertionError: 字段值不匹配或字段不存在时
        """
        actual = self._resolve_path(field_path)
        assert actual == expected, (
            f"JSON 字段断言失败: 路径 '{field_path}' 期望 {expected!r}, 实际 {actual!r}"
        )
        return self

    def json_has_field(self, field_path: str) -> "ResponseAssertions":
        """断言 JSON 响应中包含指定字段。

        Args:
            field_path: 点号分隔的字段路径

        Returns:
            self，支持链式调用

        Raises:
            AssertionError: 字段不存在时
        """
        self._resolve_path(field_path)
        return self

    def response_time_less_than(self, max_ms: float) -> "ResponseAssertions":
        """断言响应时间小于指定毫秒数。

        Args:
            max_ms: 最大允许响应时间（毫秒）

        Returns:
            self，支持链式调用

        Raises:
            AssertionError: 响应时间超过阈值时
        """
        actual_ms = self._response.elapsed.total_seconds() * 1000
        assert actual_ms < max_ms, (
            f"响应时间断言失败: 期望 < {max_ms}ms, 实际 {actual_ms:.2f}ms"
        )
        return self

    def _resolve_path(self, field_path: str):
        """沿点号路径解析 JSON 响应中的嵌套字段值。

        Args:
            field_path: 点号分隔的字段路径

        Returns:
            字段对应的值

        Raises:
            AssertionError: JSON 解析失败或路径中某个 key 不存在时
        """
        try:
            data = self._response.json()
        except Exception as exc:
            raise AssertionError(
                f"JSON 解析失败: 无法将响应体解析为 JSON ({exc})"
            ) from exc

        current = data
        for key in field_path.split("."):
            if not isinstance(current, dict) or key not in current:
                raise AssertionError(
                    f"JSON 字段不存在: 路径 '{field_path}' 在 key '{key}' 处不存在"
                )
            current = current[key]
        return current
