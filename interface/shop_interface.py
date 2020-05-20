from db import db_handler
import pysnooper

@pysnooper.snoop()
def get_goods_interface():
    goods_list = [
        ['凤爪', 50],
        ['肠粉', 20],
        ['macbook pro', 10000],
        ['肥仔快乐水', 5]
    ]
    return goods_list

@pysnooper.snoop()
def get_shopping_cart(user):
    user_dic = db_handler.select(user)
    return user_dic["shopping_cart"]

@pysnooper.snoop()
def shopping_pay_interface(user, shopping_cart):
    user_dic = db_handler.select(user)
    goods_list = get_goods_interface()
    total = 0

    for k, num in shopping_cart.items():
        total += goods_list[k][1] * num

    if total <= user_dic["balance"]:
        user_dic["balance"] -= total
        user_dic["flow"].append("结算成功，此次花费金额%s" % total)
        db_handler.save(user_dic)
        return True, "结算成功，此次花费金额%s" % total
    else:
        return False, "余额不足，请先还款"


def add_shopping_cart_interface(user, shopping_cart):
    user_dic = db_handler.select(user)
    user_dic["shopping_cart"] = shopping_cart
    db_handler.save(user_dic)


def check_shopping_cart_interface(user):
    user_dic = db_handler.select(user)
    goods_list = get_goods_interface()
    return user_dic["shopping_cart"], goods_list
