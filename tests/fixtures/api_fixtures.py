"""API 测试 fixture 模块，提供已认证的 api_client fixture。

通过 Flask test_client 自动登录获取 token，并设置到 ApiClient 实例上，
供 API 测试用例直接使用已认证的客户端。
"""

import pytest

from tests.utils.api_client import ApiClient


@pytest.fixture
def authenticated_api_client(flask_client, config):
    """已认证的 API 客户端 fixture。

    使用 Flask test_client 调用 POST /api/login 自动登录，
    从响应中提取 token 并设置到 ApiClient 实例上。

    Args:
        flask_client: Flask 测试客户端 fixture（来自 conftest.py）
        config: 配置管理器 fixture（来自 conftest.py）

    Returns:
        ApiClient: 已设置 Authorization header 的 HTTP 客户端
    """
    response = flask_client.post(
        "/api/login",
        json={"username": "admin", "password": "admin123"},
    )
    data = response.get_json()
    assert data["code"] == 200, f"登录失败: {data}"

    token = data["data"]["token"]

    client = ApiClient(base_url=config.get_base_url())
    client.set_token(token)
    return client
