"""ConfigManager 单元测试"""

import os
import sys
from pathlib import Path

import pytest
import yaml

from tests.utils.config_manager import ConfigManager, CONFIG_DIR


class TestConfigManagerInit:
    """测试 ConfigManager 初始化"""

    def test_load_dev_config(self):
        cm = ConfigManager("dev")
        assert cm.env == "dev"
        assert cm._data is not None

    def test_load_staging_config(self):
        cm = ConfigManager("staging")
        assert cm.env == "staging"

    def test_load_prod_config(self):
        cm = ConfigManager("prod")
        assert cm.env == "prod"

    def test_default_env_is_dev(self):
        cm = ConfigManager()
        assert cm.env == "dev"

    def test_invalid_env_falls_back_to_dev(self, caplog):
        import logging

        with caplog.at_level(logging.WARNING):
            cm = ConfigManager("nonexistent")
        assert cm.env == "dev"
        assert "无效的环境名称" in caplog.text

    def test_missing_config_file_raises(self, tmp_path, monkeypatch):
        """当配置文件不存在时应抛出 FileNotFoundError"""
        import tests.utils.config_manager as mod

        monkeypatch.setattr(mod, "CONFIG_DIR", tmp_path)
        with pytest.raises(FileNotFoundError, match="配置文件不存在"):
            ConfigManager("dev")


class TestConfigManagerGet:
    """测试 get 方法（含点号嵌套 key）"""

    def setup_method(self):
        self.cm = ConfigManager("dev")

    def test_get_top_level_key(self):
        api = self.cm.get("api")
        assert isinstance(api, dict)
        assert "base_url" in api

    def test_get_nested_key(self):
        base_url = self.cm.get("api.base_url")
        assert base_url == "http://localhost:5000"

    def test_get_deeply_nested_key(self):
        timeout = self.cm.get("api.timeout")
        assert timeout == 10

    def test_get_missing_key_returns_default(self):
        assert self.cm.get("nonexistent") is None
        assert self.cm.get("nonexistent", "fallback") == "fallback"

    def test_get_missing_nested_key_returns_default(self):
        assert self.cm.get("api.nonexistent") is None
        assert self.cm.get("api.nonexistent", 42) == 42

    def test_get_partial_path_returns_default(self):
        # api.base_url.deep doesn't exist since base_url is a string
        assert self.cm.get("api.base_url.deep") is None


class TestGetBaseUrl:
    """测试 get_base_url 方法"""

    def test_dev_base_url(self):
        cm = ConfigManager("dev")
        assert cm.get_base_url() == "http://localhost:5000"

    def test_staging_base_url(self):
        cm = ConfigManager("staging")
        assert cm.get_base_url() == "http://staging.example.com"


class TestResolveEnv:
    """测试 resolve_env 静态方法"""

    def test_default_returns_dev(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["pytest"])
        monkeypatch.delenv("TEST_ENV", raising=False)
        assert ConfigManager.resolve_env() == "dev"

    def test_env_from_cli_arg(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["pytest", "--env", "staging"])
        monkeypatch.delenv("TEST_ENV", raising=False)
        assert ConfigManager.resolve_env() == "staging"

    def test_env_from_cli_arg_equals(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["pytest", "--env=prod"])
        monkeypatch.delenv("TEST_ENV", raising=False)
        assert ConfigManager.resolve_env() == "prod"

    def test_env_from_env_var(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["pytest"])
        monkeypatch.setenv("TEST_ENV", "staging")
        assert ConfigManager.resolve_env() == "staging"

    def test_cli_arg_takes_priority_over_env_var(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["pytest", "--env", "prod"])
        monkeypatch.setenv("TEST_ENV", "staging")
        assert ConfigManager.resolve_env() == "prod"
