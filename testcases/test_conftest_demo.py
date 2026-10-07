"""第 2 关-③：conftest.py 练习

注意：本文件没有 import config / base_url，pytest 会自动去 conftest.py 里找。
"""
import requests


def test_read_config(config):
    print(f"\n  读到的配置：{config}")
    assert config["base_url"] == "http://localhost:8080"
    assert config["user"]["username"] == "user123"


def test_use_base_url(base_url, config):
    resp = requests.get(f"{base_url}/wx/home/index", timeout=config["timeout"])
    assert resp.status_code == 200
    assert resp.json()["errno"] == 0
