"""登录接口测试：使用 Flask test_client 测试 POST /api/login。

需求: 2.4, 2.5, 2.7, 2.8
"""

import os
from datetime import timedelta

import pytest

from tests.utils.assertions import ResponseAssertions
from tests.utils.data_driver import DataDriver


class _FlaskResponseAdapter:
    """将 Flask TestResponse 适配为 ResponseAssertions 兼容的接口。

    ResponseAssertions 期望 requests.Response 风格的对象（.json() 可调用，.elapsed 属性），
    而 Flask TestResponse 的 .json 是 property，且没有 .elapsed。
    """

    def __init__(self, flask_response):
        self._resp = flask_response
        self.status_code = flask_response.status_code
        self.elapsed = timedelta(milliseconds=0)

    def json(self):
        return self._resp.get_json()


def _assert(flask_response):
    """快捷函数：将 Flask 响应包装后传入 ResponseAssertions。"""
    return ResponseAssertions(_FlaskResponseAdapter(flask_response))


@pytest.mark.api
class TestLogin:
    """POST /api/login 登录接口测试。"""

    def test_login_success(self, flask_client):
        """正确凭据登录：code=200 且包含 token 字段。"""
        resp = flask_client.post(
            "/api/login",
            json={"username": "admin", "password": "admin123"},
        )
        _assert(resp).status_code(200).json_field("code", 200).json_has_field(
            "data.token"
        )

    def test_login_wrong_password(self, flask_client):
        """错误密码：code=401。"""
        resp = flask_client.post(
            "/api/login",
            json={"username": "admin", "password": "wrong"},
        )
        _assert(resp).status_code(401).json_field("code", 401)

    def test_login_missing_params(self, flask_client):
        """缺少参数：code=400。"""
        resp = flask_client.post("/api/login", json={})
        _assert(resp).status_code(400).json_field("code", 400)


# 构建测试数据文件的绝对路径，确保无论 pytest 从哪里运行都能找到
_LOGIN_DATA_PATH = os.path.join(
    os.path.dirname(__file__), os.pardir, os.pardir, "testdata", "login_data.yaml"
)
_LOGIN_DATA = DataDriver.load(os.path.normpath(_LOGIN_DATA_PATH))


def _test_id(data):
    """为参数化测试用例生成可读的测试 ID。"""
    return data.get("name", "unknown")


@pytest.mark.api
class TestLoginDataDriven:
    """数据驱动登录测试：从 YAML 文件加载测试数据，验证各场景。"""

    @pytest.mark.parametrize("data", _LOGIN_DATA, ids=_test_id)
    def test_login_data_driven(self, flask_client, data):
        """使用数据驱动方式验证 POST /api/login 各场景。"""
        resp = flask_client.post("/api/login", json=data["input"])
        expected = data["expected"]

        # 断言 HTTP 状态码
        assert resp.status_code == expected["status_code"], (
            f"[{data['name']}] 状态码不匹配: "
            f"期望 {expected['status_code']}, 实际 {resp.status_code}"
        )

        # 断言响应体中的 code 字段
        body = resp.get_json()
        assert body["code"] == expected["code"], (
            f"[{data['name']}] code 不匹配: "
            f"期望 {expected['code']}, 实际 {body['code']}"
        )

        # 断言 msg 字段（如果 expected 中指定了）
        if "msg" in expected:
            assert body["msg"] == expected["msg"], (
                f"[{data['name']}] msg 不匹配: "
                f"期望 {expected['msg']}, 实际 {body['msg']}"
            )

        # 断言 token 存在性
        if expected.get("has_token"):
            assert "data" in body and "token" in body["data"], (
                f"[{data['name']}] 期望响应包含 data.token 字段"
            )
        else:
            has_token = "data" in body and isinstance(body["data"], dict) and "token" in body["data"]
            assert not has_token, (
                f"[{data['name']}] 期望响应不包含 token 字段"
            )
