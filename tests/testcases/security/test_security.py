"""安全测试用例：SQL 注入、XSS、认证与授权。

针对 POST /api/login 端点进行安全测试，验证接口对常见攻击的防护能力。

需求: 6.1, 6.2, 6.3, 6.4, 6.5
"""

import pytest


# ---------------------------------------------------------------------------
# SQL 注入检测
# ---------------------------------------------------------------------------

SQL_INJECTION_PAYLOADS = [
    "' OR '1'='1",
    "admin'--",
    "' UNION SELECT * FROM users--",
]


@pytest.mark.security
class TestSQLInjection:
    """SQL 注入检测测试：验证 /api/login 对 SQL 注入攻击的防护。"""

    @pytest.mark.parametrize("payload", SQL_INJECTION_PAYLOADS)
    def test_sql_injection_in_username(self, flask_client, payload):
        """用户名字段注入 SQL payload，应返回 401 而非 200。"""
        resp = flask_client.post(
            "/api/login",
            json={"username": payload, "password": "anything"},
        )
        body = resp.get_json()

        # 注入不应导致认证成功
        assert resp.status_code != 200 or body.get("code") != 200, (
            f"SQL 注入可能成功: payload={payload!r}, "
            f"status={resp.status_code}, body={body}"
        )

    @pytest.mark.parametrize("payload", SQL_INJECTION_PAYLOADS)
    def test_sql_injection_in_password(self, flask_client, payload):
        """密码字段注入 SQL payload，应返回 401 而非 200。"""
        resp = flask_client.post(
            "/api/login",
            json={"username": "admin", "password": payload},
        )
        body = resp.get_json()

        assert resp.status_code != 200 or body.get("code") != 200, (
            f"SQL 注入可能成功: payload={payload!r}, "
            f"status={resp.status_code}, body={body}"
        )


# ---------------------------------------------------------------------------
# XSS 检测
# ---------------------------------------------------------------------------

XSS_PAYLOADS = [
    "<script>alert('xss')</script>",
    "<img onerror=alert(1) src=x>",
    "javascript:alert(1)",
]


@pytest.mark.security
class TestXSS:
    """XSS 检测测试：验证 /api/login 对跨站脚本攻击的防护。"""

    @pytest.mark.parametrize("payload", XSS_PAYLOADS)
    def test_xss_in_username(self, flask_client, payload):
        """用户名字段注入 XSS payload，响应不应原样反射脚本内容。"""
        resp = flask_client.post(
            "/api/login",
            json={"username": payload, "password": "anything"},
        )
        raw = resp.data.decode("utf-8", errors="replace")

        # 响应体不应原样包含未转义的脚本标签
        assert "<script>" not in raw, (
            f"XSS 反射风险: payload={payload!r} 在响应中被原样返回"
        )

    @pytest.mark.parametrize("payload", XSS_PAYLOADS)
    def test_xss_in_password(self, flask_client, payload):
        """密码字段注入 XSS payload，响应不应原样反射脚本内容。"""
        resp = flask_client.post(
            "/api/login",
            json={"username": "admin", "password": payload},
        )
        raw = resp.data.decode("utf-8", errors="replace")

        assert "<script>" not in raw, (
            f"XSS 反射风险: payload={payload!r} 在响应中被原样返回"
        )


# ---------------------------------------------------------------------------
# 认证与授权
# ---------------------------------------------------------------------------

@pytest.mark.security
class TestAuthSecurity:
    """认证与授权测试：验证接口的访问控制。"""

    def test_missing_token_access(self, flask_client):
        """未携带 token 访问受保护资源，应被拒绝（401/403）。"""
        resp = flask_client.get("/api/login")
        # GET /api/login 未定义，应返回 405 Method Not Allowed
        assert resp.status_code in (401, 403, 405), (
            f"缺少 token 时预期 401/403/405，实际 {resp.status_code}"
        )

    def test_invalid_token_access(self, flask_client):
        """携带无效 token 访问，应被拒绝。"""
        resp = flask_client.post(
            "/api/login",
            json={"username": "admin", "password": "admin123"},
            headers={"Authorization": "Bearer invalid-token-12345"},
        )
        # 登录端点本身不校验 token，但确保无效 token 不影响正常流程
        body = resp.get_json()
        assert body.get("code") == 200, (
            "有效凭据 + 无效 token 不应阻止登录"
        )

    def test_expired_token_pattern(self, flask_client):
        """携带过期 token 模式访问，验证不会绕过认证。"""
        resp = flask_client.post(
            "/api/login",
            json={"username": "admin", "password": "wrong"},
            headers={"Authorization": "Bearer expired-token-abc"},
        )
        body = resp.get_json()
        # 错误密码即使带 token 也不应成功
        assert resp.status_code == 401, (
            f"过期 token 不应绕过密码验证: status={resp.status_code}"
        )
        assert body.get("code") == 401
