"""ApiClient 单元测试。"""

import pytest
import requests
from unittest.mock import patch, MagicMock

from tests.utils.api_client import ApiClient


@pytest.fixture
def client():
    """创建一个测试用 ApiClient 实例。"""
    return ApiClient(base_url="http://localhost:5000", timeout=5)


class TestApiClientInit:
    """测试 ApiClient 初始化。"""

    def test_base_url_stored(self, client):
        assert client.base_url == "http://localhost:5000"

    def test_base_url_trailing_slash_stripped(self):
        c = ApiClient(base_url="http://localhost:5000/")
        assert c.base_url == "http://localhost:5000"

    def test_timeout_default(self):
        c = ApiClient(base_url="http://example.com")
        assert c.timeout == 10

    def test_timeout_custom(self, client):
        assert client.timeout == 5

    def test_session_created(self, client):
        assert isinstance(client.session, requests.Session)

    def test_last_response_initially_none(self, client):
        assert client.get_last_response() is None


class TestApiClientRequest:
    """测试 request 方法的 URL 拼接和方法路由。"""

    @patch.object(requests.Session, "request")
    def test_url_prepends_base_url(self, mock_request, client):
        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.text = "{}"
        mock_request.return_value = mock_response

        client.get("/api/login")

        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert args == ("GET", "http://localhost:5000/api/login")

    @patch.object(requests.Session, "request")
    def test_path_without_leading_slash(self, mock_request, client):
        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.text = "{}"
        mock_request.return_value = mock_response

        client.get("api/login")

        args, _ = mock_request.call_args
        assert args == ("GET", "http://localhost:5000/api/login")

    @patch.object(requests.Session, "request")
    def test_timeout_passed(self, mock_request, client):
        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.text = "{}"
        mock_request.return_value = mock_response

        client.get("/test")

        _, kwargs = mock_request.call_args
        assert kwargs["timeout"] == 5

    @patch.object(requests.Session, "request")
    def test_last_response_stored(self, mock_request, client):
        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.text = "{}"
        mock_request.return_value = mock_response

        result = client.get("/test")

        assert client.get_last_response() is result
        assert client.get_last_response() is mock_response


class TestApiClientMethods:
    """测试 get/post/put/delete 便捷方法。"""

    @patch.object(requests.Session, "request")
    def test_get_uses_get_method(self, mock_request, client):
        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.text = "{}"
        mock_request.return_value = mock_response

        client.get("/test")
        args, _ = mock_request.call_args
        assert args[0] == "GET"

    @patch.object(requests.Session, "request")
    def test_post_uses_post_method(self, mock_request, client):
        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.text = "{}"
        mock_request.return_value = mock_response

        client.post("/test", json={"key": "value"})
        args, kwargs = mock_request.call_args
        assert args[0] == "POST"
        assert kwargs["json"] == {"key": "value"}

    @patch.object(requests.Session, "request")
    def test_put_uses_put_method(self, mock_request, client):
        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.text = "{}"
        mock_request.return_value = mock_response

        client.put("/test")
        args, _ = mock_request.call_args
        assert args[0] == "PUT"

    @patch.object(requests.Session, "request")
    def test_delete_uses_delete_method(self, mock_request, client):
        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.text = "{}"
        mock_request.return_value = mock_response

        client.delete("/test")
        args, _ = mock_request.call_args
        assert args[0] == "DELETE"


class TestApiClientToken:
    """测试 set_token 和 Authorization header 管理。"""

    def test_set_token_adds_auth_header(self, client):
        client.set_token("my-secret-token")
        assert client.session.headers["Authorization"] == "Bearer my-secret-token"

    @patch.object(requests.Session, "request")
    def test_token_sent_in_request(self, mock_request, client):
        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.text = "{}"
        mock_request.return_value = mock_response

        client.set_token("abc123")
        client.get("/protected")

        assert client.session.headers["Authorization"] == "Bearer abc123"

    def test_set_token_overwrites_previous(self, client):
        client.set_token("token1")
        client.set_token("token2")
        assert client.session.headers["Authorization"] == "Bearer token2"
