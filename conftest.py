"""公共 fixture：放在这里的 fixture，所有用例文件都能直接用，不需要 import"""
import pytest

from common.config import load_config
from common.request_util import ApiClient


@pytest.fixture(scope="session")
def config():
    """整轮测试只读一次配置文件"""
    return load_config()


@pytest.fixture(scope="session")
def base_url(config):
    """fixture 可以依赖另一个 fixture：这里直接拿 config 里的 base_url"""
    return config["base_url"]


@pytest.fixture(scope="session")
def api(base_url, config):
    """不带 token 的客户端：测登录接口、测"未登录"场景用"""
    return ApiClient(base_url, config["timeout"])


@pytest.fixture(scope="session")
def token(base_url, config):
    """session 级别：整轮测试只登录一次，拿到的 token 给所有用例复用"""
    print("\n  [token] 登录一次，获取 token")
    client = ApiClient(base_url, config["timeout"])
    user = config["user"]
    resp = client.post("/wx/auth/login",
                       json={"username": user["username"], "password": user["password"]})
    result = resp.json()
    # 登录失败直接报错，后面依赖登录的用例都不用跑了
    assert result["errno"] == 0, f"登录失败，无法获取 token：{result}"
    return result["data"]["token"]


@pytest.fixture(scope="session")
def auth_api(base_url, config, token):
    """带 token 的客户端：需要登录的接口都用它"""
    client = ApiClient(base_url, config["timeout"])
    client.set_token(token)
    return client
