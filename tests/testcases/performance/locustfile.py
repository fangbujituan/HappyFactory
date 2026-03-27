"""Locust 性能测试脚本 - POST /api/login 接口压力测试。

可通过两种方式运行：
1. 独立 Locust 模式: locust -f tests/testcases/performance/locustfile.py
2. pytest 入口: pytest -m perf tests/testcases/performance/locustfile.py

注意: Locust 的 gevent monkey-patching 与 pytest 的 assertion rewriting 存在冲突，
因此 locust 相关类定义放在单独的模块中，由 locust CLI 直接加载；
pytest 入口通过 subprocess 调用 locust，不在当前进程中导入 locust。
"""

import logging
import subprocess
import sys
from pathlib import Path

import pytest

# 将项目根目录加入 sys.path，确保独立运行时也能导入配置
_project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

logger = logging.getLogger(__name__)


def _load_perf_config() -> dict:
    """从 ConfigManager 加载性能测试相关配置。

    Returns:
        包含 base_url、users、duration 等键的字典。
    """
    from tests.utils.config_manager import ConfigManager

    try:
        config = ConfigManager(env=ConfigManager.resolve_env())
    except FileNotFoundError:
        config = ConfigManager(env="dev")

    return {
        "base_url": config.get_base_url(),
        "users": config.get("performance.users", 10),
        "duration": config.get("performance.duration", 30),
    }


# ---------------------------------------------------------------------------
# pytest 入口
# ---------------------------------------------------------------------------

@pytest.mark.perf
def test_locust_performance():
    """通过 pytest 以编程方式调用 Locust 执行性能测试。

    从配置文件读取并发用户数和持续时间，以 headless 模式运行 Locust，
    测试完成后根据退出码判断是否通过。
    """
    perf_cfg = _load_perf_config()
    users = perf_cfg["users"]
    duration = perf_cfg["duration"]
    base_url = perf_cfg["base_url"]

    # 指向同目录下的 _locust_users.py（Locust User 定义）
    locust_users_file = str(
        Path(__file__).resolve().parent / "_locust_users.py"
    )

    cmd = [
        sys.executable, "-m", "locust",
        "-f", locust_users_file,
        "--headless",
        "--host", base_url,
        "-u", str(users),
        "-r", str(max(1, users // 2)),
        "-t", f"{duration}s",
        "--only-summary",
    ]

    logger.info(
        "启动 Locust 性能测试: users=%s, duration=%ss, host=%s",
        users, duration, base_url,
    )

    result = subprocess.run(
        cmd, capture_output=True, text=True,
        timeout=duration + 60, check=False,
    )

    if result.stdout:
        logger.info("Locust stdout:\n%s", result.stdout)
    if result.stderr:
        logger.debug("Locust stderr:\n%s", result.stderr)

    assert result.returncode == 0, (
        f"Locust 性能测试失败 (exit code {result.returncode}).\n"
        f"stdout: {result.stdout[-500:] if result.stdout else ''}\n"
        f"stderr: {result.stderr[-500:] if result.stderr else ''}"
    )
