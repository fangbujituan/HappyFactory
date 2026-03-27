"""DataDriver 单元测试。"""

import json
import os
import tempfile

import pytest
import yaml

from tests.utils.data_driver import DataDriver


@pytest.fixture
def tmp_dir():
    """提供临时目录，测试结束后自动清理。"""
    with tempfile.TemporaryDirectory() as d:
        yield d


class TestLoadYaml:
    def test_load_yaml_list(self, tmp_dir):
        data = [{"name": "test1", "value": 1}, {"name": "test2", "value": 2}]
        path = os.path.join(tmp_dir, "data.yaml")
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True)
        result = DataDriver.load_yaml(path)
        assert result == data

    def test_load_yaml_not_list_raises(self, tmp_dir):
        path = os.path.join(tmp_dir, "bad.yaml")
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump({"key": "value"}, f)
        with pytest.raises(ValueError, match="列表格式"):
            DataDriver.load_yaml(path)

    def test_load_yaml_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            DataDriver.load_yaml("/nonexistent/path.yaml")


class TestLoadJson:
    def test_load_json_list(self, tmp_dir):
        data = [{"a": 1}, {"b": 2}]
        path = os.path.join(tmp_dir, "data.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        result = DataDriver.load_json(path)
        assert result == data

    def test_load_json_not_list_raises(self, tmp_dir):
        path = os.path.join(tmp_dir, "bad.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"key": "value"}, f)
        with pytest.raises(ValueError, match="列表格式"):
            DataDriver.load_json(path)

    def test_load_json_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            DataDriver.load_json("/nonexistent/path.json")


class TestLoadCsv:
    def test_load_csv(self, tmp_dir):
        path = os.path.join(tmp_dir, "data.csv")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("name,value\n")
            f.write("test1,1\n")
            f.write("test2,2\n")
        result = DataDriver.load_csv(path)
        assert result == [
            {"name": "test1", "value": "1"},
            {"name": "test2", "value": "2"},
        ]

    def test_load_csv_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            DataDriver.load_csv("/nonexistent/path.csv")


class TestLoadAutoDetect:
    def test_load_yaml_by_extension(self, tmp_dir):
        data = [{"x": 1}]
        path = os.path.join(tmp_dir, "data.yaml")
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f)
        assert DataDriver.load(path) == data

    def test_load_yml_by_extension(self, tmp_dir):
        data = [{"x": 1}]
        path = os.path.join(tmp_dir, "data.yml")
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f)
        assert DataDriver.load(path) == data

    def test_load_json_by_extension(self, tmp_dir):
        data = [{"x": 1}]
        path = os.path.join(tmp_dir, "data.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        assert DataDriver.load(path) == data

    def test_load_csv_by_extension(self, tmp_dir):
        path = os.path.join(tmp_dir, "data.csv")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("col\nval\n")
        assert DataDriver.load(path) == [{"col": "val"}]

    def test_load_unsupported_format_raises(self):
        with pytest.raises(ValueError, match="不支持的数据文件格式"):
            DataDriver.load("data.xml")
