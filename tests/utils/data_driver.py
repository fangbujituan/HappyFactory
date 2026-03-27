"""数据驱动模块，支持从 YAML、JSON、CSV 文件加载测试数据。"""

import csv
import json
import os

import yaml


class DataDriver:
    """测试数据加载器，支持 YAML、JSON、CSV 格式。"""

    @staticmethod
    def load_yaml(file_path: str) -> list[dict]:
        """从 YAML 文件加载测试数据。

        Args:
            file_path: YAML 文件路径。

        Returns:
            字典列表形式的测试数据。

        Raises:
            FileNotFoundError: 文件不存在时抛出。
            ValueError: 文件内容不是有效的 YAML 列表时抛出。
        """
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, list):
            raise ValueError(f"YAML 文件内容应为列表格式: {file_path}")
        return data

    @staticmethod
    def load_json(file_path: str) -> list[dict]:
        """从 JSON 文件加载测试数据。

        Args:
            file_path: JSON 文件路径。

        Returns:
            字典列表形式的测试数据。

        Raises:
            FileNotFoundError: 文件不存在时抛出。
            ValueError: 文件内容不是有效的 JSON 列表时抛出。
        """
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError(f"JSON 文件内容应为列表格式: {file_path}")
        return data

    @staticmethod
    def load_csv(file_path: str) -> list[dict]:
        """从 CSV 文件加载测试数据。

        Args:
            file_path: CSV 文件路径。

        Returns:
            字典列表形式的测试数据（每行为一个字典）。

        Raises:
            FileNotFoundError: 文件不存在时抛出。
        """
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    @staticmethod
    def load(file_path: str) -> list[dict]:
        """根据文件扩展名自动选择加载方式。

        支持的扩展名: .yaml, .yml, .json, .csv

        Args:
            file_path: 数据文件路径。

        Returns:
            字典列表形式的测试数据。

        Raises:
            ValueError: 不支持的文件格式时抛出。
        """
        ext = os.path.splitext(file_path)[1].lower()
        if ext in (".yaml", ".yml"):
            return DataDriver.load_yaml(file_path)
        elif ext == ".json":
            return DataDriver.load_json(file_path)
        elif ext == ".csv":
            return DataDriver.load_csv(file_path)
        else:
            raise ValueError(
                f"不支持的数据文件格式 '{ext}'，支持的格式: .yaml, .yml, .json, .csv"
            )
