"""配置管理器 - 多环境 YAML 配置加载与访问"""

import logging
import os
import sys
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

# 合法环境名称
VALID_ENVS = {"dev", "staging", "prod"}

# 配置文件目录（相对于 tests/ 目录）
CONFIG_DIR = Path(__file__).parent.parent / "config"


class ConfigManager:
    """多环境配置管理器，支持 YAML 配置文件加载"""

    def __init__(self, env: str = "dev"):
        """根据环境名加载对应配置文件。

        Args:
            env: 环境名称，支持 dev/staging/prod。无效名称回退到 dev。

        Raises:
            FileNotFoundError: 配置文件不存在时抛出。
        """
        if env not in VALID_ENVS:
            logger.warning(
                "无效的环境名称 '%s'，回退到默认环境 'dev'。有效值: %s",
                env,
                ", ".join(sorted(VALID_ENVS)),
            )
            env = "dev"

        self.env = env
        config_path = CONFIG_DIR / f"{env}.yaml"

        if not config_path.exists():
            raise FileNotFoundError(
                f"配置文件不存在: {config_path}"
            )

        with open(config_path, "r", encoding="utf-8") as f:
            self._data: dict = yaml.safe_load(f) or {}

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项，支持点号分隔的嵌套 key。

        Args:
            key: 配置键，如 'api.base_url'。
            default: 键不存在时的默认值。

        Returns:
            配置值，或 default。
        """
        keys = key.split(".")
        value: Any = self._data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value

    def get_base_url(self) -> str:
        """获取当前环境的 API base URL。"""
        return self.get("api.base_url", "http://localhost:5000")

    @staticmethod
    def resolve_env() -> str:
        """从命令行参数 --env 或环境变量 TEST_ENV 解析环境名。

        优先级: --env CLI 参数 > TEST_ENV 环境变量 > 默认 'dev'。
        """
        # 1. 从 sys.argv 中查找 --env 参数
        args = sys.argv
        for i, arg in enumerate(args):
            if arg == "--env" and i + 1 < len(args):
                return args[i + 1]
            if arg.startswith("--env="):
                return arg.split("=", 1)[1]

        # 2. 从环境变量 TEST_ENV 读取
        env_var = os.environ.get("TEST_ENV")
        if env_var:
            return env_var

        # 3. 默认 dev
        return "dev"
