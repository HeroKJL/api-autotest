"""购物车列表：GET /wx/cart/index（需要登录）

验证 session 级 token：本文件 2 条带 token 的用例，[token] 登录只会打印一次
"""
CART_INDEX = "/wx/cart/index"


def test_cart_index_with_token(auth_api):
    resp = auth_api.get(CART_INDEX)
    result = resp.json()
    assert resp.status_code == 200
    assert result["errno"] == 0
    assert "cartTotal" in result["data"]
    assert "cartList" in result["data"]


def test_cart_total_fields(auth_api):
    # 第二次用 token：不会重新登录
    cart_total = auth_api.get(CART_INDEX).json()["data"]["cartTotal"]
    for field in ["goodsCount", "checkedGoodsCount", "goodsAmount", "checkedGoodsAmount"]:
        assert field in cart_total, f"cartTotal 缺少字段 {field}"


def test_cart_index_without_token(api):
    # 不带 token：litemall 返回 errno 501（HTTP 仍是 200）
    result = api.get(CART_INDEX).json()
    assert result["errno"] == 501
