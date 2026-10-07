"""第 2 关-②：fixture 和 scope 练习

运行：pytest testcases\test_fixture_demo.py
看每个 fixture 的"准备""清理"各打印了几次，就能看出 scope 的区别。
"""
import pytest


# scope="session"：整个测试运行期间只执行 1 次（比如登录拿 token）
@pytest.fixture(scope="session")
def session_fx():
    print("\n  [session] 准备 —— 整轮测试只执行一次")
    yield "token-abc"          # yield 之前是准备，yield 的值会传给用例
    print("\n  [session] 清理 —— 全部用例结束后执行")


# scope="class"：每个测试类执行 1 次
@pytest.fixture(scope="class")
def class_fx():
    print("\n  [class] 准备 —— 每个类执行一次")
    yield
    print("\n  [class] 清理")


# scope="function"（默认）：每条用例都执行 1 次（比如每条用例前清空购物车）
@pytest.fixture
def function_fx():
    print("\n  [function] 准备 —— 每条用例都执行")
    yield
    print("\n  [function] 清理")


class TestA:
    def test_a1(self, session_fx, class_fx, function_fx):
        # 用例想用哪个 fixture，就把它的名字写进参数里
        print(f"  执行 test_a1，拿到 token = {session_fx}")

    def test_a2(self, session_fx, class_fx, function_fx):
        print(f"  执行 test_a2，拿到 token = {session_fx}")


class TestB:
    def test_b1(self, session_fx, class_fx, function_fx):
        print(f"  执行 test_b1，拿到 token = {session_fx}")
