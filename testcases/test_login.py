"""登录接口用例：POST /wx/auth/login

用 @pytest.mark.parametrize 参数化：一个测试函数 + 多组数据 = 多条用例
"""
import pytest

LOGIN_PATH = "/wx/auth/login"

# 每组数据：(请求体, 期望 errno, 期望 errmsg 里包含的文字)
# 期望值依据 litemall 源码 WxAuthController.login 整理，已运行验证
login_cases = [
    ({"username": "user123", "password": "user123"}, 0, "成功"),
    ({"username": "user123", "password": "wrong_pwd"}, 700, "账号密码不对"),
    ({"username": "", "password": "user123"}, 700, "账号不存在"),
    ({"password": "user123"}, 401, "参数不对"),
    ({"username": "no_such_user_9527", "password": "user123"}, 700, "账号不存在"),
]

case_ids = ["正常登录", "密码错误", "用户名为空串", "不传用户名", "用户名不存在"]


@pytest.mark.parametrize("body, expect_errno, expect_msg", login_cases, ids=case_ids)
def test_login(api, body, expect_errno, expect_msg):
    # 用封装好的 api：不用再写 base_url、timeout，请求和返回会自动打印
    resp = api.post(LOGIN_PATH, json=body)
    result = resp.json()

    # 第一层：HTTP 状态码
    assert resp.status_code == 200
    # 第二层：业务码 + 提示文案
    assert result["errno"] == expect_errno
    assert expect_msg in result["errmsg"]

    # 登录成功时，还要断言返回了 token 和用户信息
    if expect_errno == 0:
        assert result["data"]["token"], "登录成功但 token 为空"
        assert "nickName" in result["data"]["userInfo"]
