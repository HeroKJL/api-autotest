"""统一请求封装：所有接口请求都从这里发出

解决的问题：
1. 每个用例都要写 base_url + 路径 → 这里统一拼接
2. 每个用例都要写 timeout、header → 这里统一设置
3. 登录后的 token 要带在每个请求里 → set_token 一次，后续请求自动带上
4. 请求和返回统一打印，排查问题时不用到处加 print
"""
import requests


class ApiClient:
    TOKEN_HEADER = "X-Litemall-Token"   # 用户端 token 的请求头名称

    def __init__(self, base_url, timeout=5):
        self.base_url = base_url
        self.timeout = timeout
        # Session 会复用 TCP 连接，并且自动保存设置好的 header
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def set_token(self, token):
        self.session.headers[self.TOKEN_HEADER] = token

    def request(self, method, path, **kwargs):
        url = self.base_url + path
        kwargs.setdefault("timeout", self.timeout)
        resp = self.session.request(method, url, **kwargs)
        print(f"\n  >>> {method} {path}  参数：{kwargs.get('params') or kwargs.get('json')}")
        print(f"  <<< HTTP {resp.status_code}  {resp.text[:200]}")
        return resp

    def get(self, path, params=None, **kwargs):
        return self.request("GET", path, params=params, **kwargs)

    def post(self, path, json=None, **kwargs):
        return self.request("POST", path, json=json, **kwargs)
