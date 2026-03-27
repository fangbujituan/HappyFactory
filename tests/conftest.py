"""全局 pytest fixture 和配置钩子。

提供 session 级别的配置管理器、Flask 应用实例、API 客户端，
以及函数级别的 Flask 测试客户端。
"""

import pytest

from tests.utils.config_manager import ConfigManager
from tests.utils.api_client import ApiClient


def pytest_addoption(parser):
    """注册 --env 命令行选项，用于指定测试环境。"""
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="指定测试环境: dev, staging, prod（默认通过 TEST_ENV 环境变量或 dev）",
    )


@pytest.fixture(scope="session")
def config():
    """会话级配置管理器，根据环境参数加载对应配置。"""
    return ConfigManager(env=ConfigManager.resolve_env())


@pytest.fixture(scope="session")
def flask_app():
    """会话级 Flask 应用实例，启用 TESTING 模式。"""
    from app import create_app

    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def flask_client(flask_app):
    """函数级 Flask 测试客户端。"""
    return flask_app.test_client()


@pytest.fixture(scope="session")
def api_client(config):
    """会话级 HTTP 客户端，base_url 从配置中读取。"""
    return ApiClient(base_url=config.get_base_url())
