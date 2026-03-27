"""tests/fixtures/api_fixtures.py 的单元测试。"""

from tests.fixtures.api_fixtures import authenticated_api_client  # noqa: F401


class TestAuthenticatedApiClient:
    """authenticated_api_client fixture 的测试。"""

    def test_fixture_returns_api_client_with_token(
        self, authenticated_api_client  # noqa: F811
    ):
        """验证 fixture 返回的客户端已设置 Authorization header。"""
        auth_header = authenticated_api_client.session.headers.get("Authorization")
        assert auth_header is not None, "Authorization header 未设置"
        assert auth_header == "Bearer mock-token-admin"

    def test_fixture_login_uses_correct_credentials(self, flask_client):
        """验证登录端点使用正确凭据返回预期 token。"""
        response = flask_client.post(
            "/api/login",
            json={"username": "admin", "password": "admin123"},
        )
        data = response.get_json()
        assert data["code"] == 200
        assert data["data"]["token"] == "mock-token-admin"
