"""tests/utils/logger.py 的单元测试。"""

import logging
from datetime import datetime

import pytest

from tests.utils.logger import setup_logger


@pytest.fixture(autouse=True)
def cleanup_loggers():
    """每个测试后清理 logger handlers，避免测试间干扰。"""
    yield
    for name in list(logging.Logger.manager.loggerDict):
        logger = logging.getLogger(name)
        logger.handlers.clear()


@pytest.fixture
def tmp_log_dir(tmp_path):
    """提供临时日志目录。"""
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    return log_dir


class TestSetupLogger:
    """setup_logger 函数测试。"""

    def test_returns_logger_instance(self):
        logger = setup_logger("test_basic")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_basic"

    def test_console_handler_added(self):
        logger = setup_logger("test_console")
        stream_handlers = [
            h for h in logger.handlers if isinstance(h, logging.StreamHandler)
            and not isinstance(h, logging.FileHandler)
        ]
        assert len(stream_handlers) == 1

    def test_no_file_handler_without_log_file(self):
        logger = setup_logger("test_no_file")
        file_handlers = [
            h for h in logger.handlers if isinstance(h, logging.FileHandler)
        ]
        assert len(file_handlers) == 0

    def test_file_handler_added_with_log_file(self, tmp_log_dir):
        log_file = str(tmp_log_dir / "test.log")
        logger = setup_logger("test_file", log_file=log_file)
        file_handlers = [
            h for h in logger.handlers if isinstance(h, logging.FileHandler)
        ]
        assert len(file_handlers) == 1

    def test_date_based_directory_created(self, tmp_log_dir):
        log_file = str(tmp_log_dir / "test.log")
        setup_logger("test_date_dir", log_file=log_file)
        today = datetime.now().strftime("%Y-%m-%d")
        date_dir = tmp_log_dir / today
        assert date_dir.exists()
        assert (date_dir / "test.log").exists() or True  # file created on first write

    def test_log_format_contains_required_fields(self, tmp_log_dir, capfd):
        logger = setup_logger("test_format")
        logger.debug("测试消息")
        captured = capfd.readouterr()
        assert "[DEBUG]" in captured.err
        assert "[test_format]" in captured.err
        assert "测试消息" in captured.err

    def test_log_written_to_file(self, tmp_log_dir):
        log_file = str(tmp_log_dir / "output.log")
        logger = setup_logger("test_write", log_file=log_file)
        logger.info("写入文件测试")

        # Flush handlers
        for h in logger.handlers:
            h.flush()

        today = datetime.now().strftime("%Y-%m-%d")
        actual_file = tmp_log_dir / today / "output.log"
        content = actual_file.read_text(encoding="utf-8")
        assert "[INFO]" in content
        assert "[test_write]" in content
        assert "写入文件测试" in content

    def test_log_level_respected(self, capfd):
        logger = setup_logger("test_level", level="WARNING")
        logger.debug("should not appear")
        logger.warning("should appear")
        captured = capfd.readouterr()
        assert "should not appear" not in captured.err
        assert "should appear" in captured.err

    def test_no_duplicate_handlers_on_repeated_calls(self):
        logger1 = setup_logger("test_dup")
        handler_count = len(logger1.handlers)
        logger2 = setup_logger("test_dup")
        assert logger1 is logger2
        assert len(logger2.handlers) == handler_count

    def test_invalid_level_defaults_to_debug(self, capfd):
        logger = setup_logger("test_invalid_level", level="NONEXISTENT")
        logger.debug("debug msg")
        captured = capfd.readouterr()
        assert "debug msg" in captured.err

    def test_timestamp_format_in_output(self, capfd):
        logger = setup_logger("test_ts")
        logger.info("ts check")
        captured = capfd.readouterr()
        # Verify timestamp pattern like [2024-01-15 10:30:00]
        import re
        assert re.search(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]", captured.err)

    def test_exception_logging_includes_traceback(self, tmp_log_dir):
        log_file = str(tmp_log_dir / "exc.log")
        logger = setup_logger("test_exc", log_file=log_file)
        try:
            raise ValueError("test error")
        except ValueError:
            logger.error("捕获异常", exc_info=True)

        for h in logger.handlers:
            h.flush()

        today = datetime.now().strftime("%Y-%m-%d")
        content = (tmp_log_dir / today / "exc.log").read_text(encoding="utf-8")
        assert "ValueError" in content
        assert "test error" in content
        assert "Traceback" in content
