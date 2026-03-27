"""日志工具模块，支持控制台和文件双输出，按日期分类日志文件。"""

import logging
import os
from datetime import datetime


def setup_logger(
    name: str, log_file: str = None, level: str = "DEBUG"
) -> logging.Logger:
    """配置日志器，支持控制台和文件双输出，按日期分类。

    Args:
        name: 日志器名称，通常为模块或测试用例名称
        log_file: 日志文件路径。若提供，将按日期在同目录下创建子目录存放日志。
                  若为 None，则仅输出到控制台。
        level: 日志级别字符串，如 "DEBUG"、"INFO"、"WARNING"、"ERROR"

    Returns:
        配置好的 logging.Logger 实例
    """
    logger = logging.getLogger(name)

    log_level = getattr(logging, level.upper(), logging.DEBUG)
    logger.setLevel(log_level)

    # 避免重复添加 handler
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 控制台 handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件 handler（按日期分类）
    if log_file:
        log_dir = os.path.dirname(log_file) or "."
        date_dir = os.path.join(log_dir, datetime.now().strftime("%Y-%m-%d"))
        os.makedirs(date_dir, exist_ok=True)

        date_log_file = os.path.join(date_dir, os.path.basename(log_file))
        file_handler = logging.FileHandler(date_log_file, encoding="utf-8")
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
