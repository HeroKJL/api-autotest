"""第 2 关-①：assert 断言练习"""
import pytest
import requests


def test_equal():
    # 最基本的断言：条件为 True 就通过
    assert 1 + 1 == 2


def test_in():
    # 断言字段存在：接口返回里有没有 token
    resp_json = {"errno": 0, "data": {"token": "abc"}}
    assert "token" in resp_json["data"]


@pytest.mark.xfail(reason="故意失败的演示用例：用来看断言失败时的输出")
def test_fail():
    # 故意写错，看失败时 pytest 输出什么
    resp_json = {"errno": 0, "errmsg": "成功"}
    assert resp_json["errno"] == 1, f"errno 应为 1，实际为 {resp_json['errno']}"


def test_home_index():
    # 第一个真实接口断言：HTTP 状态码 + 业务码 errno 都要判断
    resp = requests.get("http://localhost:8080/wx/home/index", timeout=5)
    assert resp.status_code == 200
    assert resp.json()["errno"] == 0
