"""Locust User 定义 - POST /api/login 接口并发测试。

此文件由 locust CLI 直接加载，或由 locustfile.py 中的 pytest 入口通过
subprocess 调用。不应被 pytest 直接导入（避免 gevent monkey-patching 冲突）。

独立运行:
    locust -f tests/testcases/performance/_locust_users.py --host http://localhost:5000
"""

from locust import HttpUser, between, task


class LoginUser(HttpUser):
    """模拟用户对 POST /api/login 接口发起并发请求。"""

    wait_time = between(0.5, 2.0)
    login_payload = {"username": "admin", "password": "admin123"}

    @task
    def login(self):
        """发送 POST /api/login 请求并校验响应。"""
        with self.client.post(
            "/api/login",
            json=self.login_payload,
            catch_response=True,
        ) as resp:
            if resp.status_code == 200:
                body = resp.json()
                if body.get("code") != 200:
                    resp.failure(f"业务码异常: {body.get('code')}")
            else:
                resp.failure(f"HTTP {resp.status_code}")
