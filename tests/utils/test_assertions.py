"""ResponseAssertions 单元测试。"""

import json
from datetime import timedelta
from unittest.mock import MagicMock

import pytest

from tests.utils.assertions import ResponseAssertions


def _make_response(status_code=200, json_data=None, elapsed_ms=50.0):
    """构造一个模拟的 requests.Response 对象。"""
    resp = MagicMock()
    resp.status_code = status_code
    resp.elapsed = timedelta(milliseconds=elapsed_ms)
    if json_data is not None:
        resp.json.return_value = json_data
        resp.text = json.dumps(json_data)
    else:
        resp.json.side_effect = ValueError("No JSON")
        resp.text = ""
    return resp


class TestStatusCode:
    def test_matching_status_code_passes(self):
        resp = _make_response(status_code=200)
        result = ResponseAssertions(resp).status_code(200)
        assert isinstance(result, ResponseAssertions)

    def test_mismatched_status_code_raises(self):
        resp = _make_response(status_code=404)
        with pytest.raises(AssertionError, match="期望 200, 实际 404"):
            ResponseAssertions(resp).status_code(200)


class TestJsonField:
    def test_top_level_field(self):
        resp = _make_response(json_data={"code": 200, "msg": "ok"})
        ResponseAssertions(resp).json_field("code", 200)

    def test_nested_dot_path(self):
        resp = _make_response(json_data={"data": {"user": {"name": "admin"}}})
        ResponseAssertions(resp).json_field("data.user.name", "admin")

    def test_mismatched_value_raises(self):
        resp = _make_response(json_data={"code": 401})
        with pytest.raises(AssertionError, match="期望 200"):
            ResponseAssertions(resp).json_field("code", 200)

    def test_missing_field_raises(self):
        resp = _make_response(json_data={"code": 200})
        with pytest.raises(AssertionError, match="不存在"):
            ResponseAssertions(resp).json_field("data.name", "admin")

    def test_non_json_response_raises(self):
        resp = _make_response(json_data=None)
        with pytest.raises(AssertionError, match="JSON 解析失败"):
            ResponseAssertions(resp).json_field("code", 200)


class TestJsonHasField:
    def test_existing_field_passes(self):
        resp = _make_response(json_data={"token": "abc123"})
        result = ResponseAssertions(resp).json_has_field("token")
        assert isinstance(result, ResponseAssertions)

    def test_nested_existing_field_passes(self):
        resp = _make_response(json_data={"data": {"id": 1}})
        ResponseAssertions(resp).json_has_field("data.id")

    def test_missing_field_raises(self):
        resp = _make_response(json_data={"code": 200})
        with pytest.raises(AssertionError, match="不存在"):
            ResponseAssertions(resp).json_has_field("token")


class TestResponseTime:
    def test_fast_response_passes(self):
        resp = _make_response(elapsed_ms=50.0)
        result = ResponseAssertions(resp).response_time_less_than(100.0)
        assert isinstance(result, ResponseAssertions)

    def test_slow_response_raises(self):
        resp = _make_response(elapsed_ms=200.0)
        with pytest.raises(AssertionError, match="期望 < 100"):
            ResponseAssertions(resp).response_time_less_than(100.0)


class TestChaining:
    def test_multiple_assertions_chained(self):
        resp = _make_response(
            status_code=200,
            json_data={"code": 200, "data": {"token": "xyz"}},
            elapsed_ms=30.0,
        )
        result = (
            ResponseAssertions(resp)
            .status_code(200)
            .json_field("code", 200)
            .json_has_field("data.token")
            .json_field("data.token", "xyz")
            .response_time_less_than(1000.0)
        )
        assert isinstance(result, ResponseAssertions)
