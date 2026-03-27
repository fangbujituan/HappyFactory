"""HTTP 客户端封装模块，基于 requests 库，提供统一的请求/响应日志和认证管理。"""

import requests
from typing import Optional

from tests.utils.logger import setup_logger

logger = setup_logger("api_client")


class ApiClient:
    """基于 requests 的 HTTP 客户端封装。

    自动拼接 base_url，记录请求/响应日志，支持 Authorization header 管理。

    Args:
        base_url: API 基础 URL，如 http://localhost:5000
        timeout: 请求超时时间（秒），默认 10
    """

    def __init__(self, base_url: str, timeout: int = 10):
        self.session = requests.Session()
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._last_response: Optional[requests.Response] = None

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        """发送 HTTP 请求，自动拼接 base_url，记录请求/响应日志。

        Args:
            method: HTTP 方法，如 GET、POST、PUT、DELETE
            path: 请求路径，如 /api/login
            **kwargs: 传递给 requests.Session.request 的额外参数

        Returns:
            requests.Response 响应对象
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        kwargs.setdefault("timeout", self.timeout)

        logger.debug("发送 %s %s | 参数: %s", method.upper(), url, _safe_log_kwargs(kwargs))

        response = self.session.request(method, url, **kwargs)
        self._last_response = response

        logger.debug(
            "响应 %s %s | 状态码: %s | 响应体: %s",
            method.upper(),
            url,
            response.status_code,
            _truncate(response.text),
        )

        return response

    def get(self, path: str, **kwargs) -> requests.Response:
        """发送 GET 请求。"""
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        """发送 POST 请求。"""
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        """发送 PUT 请求。"""
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        """发送 DELETE 请求。"""
        return self.request("DELETE", path, **kwargs)

    def set_token(self, token: str):
        """设置 Authorization header。

        Args:
            token: Bearer token 字符串
        """
        self.session.headers["Authorization"] = f"Bearer {token}"
        logger.debug("已设置 Authorization header")

    def get_last_response(self) -> Optional[requests.Response]:
        """获取最近一次响应，用于调试。

        Returns:
            最近一次 requests.Response，若尚未发送请求则返回 None
        """
        return self._last_response


def _truncate(text: str, max_len: int = 500) -> str:
    """截断过长的响应体文本用于日志输出。"""
    if len(text) <= max_len:
        return text
    return text[:max_len] + "...(truncated)"


def _safe_log_kwargs(kwargs: dict) -> dict:
    """过滤敏感信息，返回可安全记录的参数摘要。"""
    safe = {}
    for key, value in kwargs.items():
        if key in ("timeout",):
            safe[key] = value
        elif key == "json":
            safe[key] = value
        elif key == "data":
            safe[key] = "<data>"
        elif key == "headers":
            safe[key] = {k: ("***" if "auth" in k.lower() else v) for k, v in value.items()}
        else:
            safe[key] = value
    return safe
