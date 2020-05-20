from db import db_handler
from lib.common import get_logger

logger = get_logger("bank")


def withdraw_interface(user, money):
    user_dic = db_handler.select(user)
    if money <= user_dic["balance"]:
        money2 = 1.05 * money
        user_dic["balance"] -= money2
        user_dic["flow"].append("提现成功，提现金额为%s，现有金额为%s" % (money, user_dic["balance"]))
        logger.info("用户 %s ：提现成功，提现金额为%s，现有金额为%s" % (user, money, user_dic["balance"]))
        db_handler.save(user_dic)
        return True, "提现成功，提现金额为%s，现有金额为%s" % (money, user_dic["balance"])
    else:
        return False, "余额不足无法提现，请先还款"


def transfer_interface(src_user, dst_user, money):
    src_dic = db_handler.select(src_user)
    dst_dic = db_handler.select(dst_user)

    if money <= src_dic["balance"]:
        src_dic["balance"] -= money
        dst_dic["balance"] += money

        src_dic["flow"].append("转账成功，%s 转入目标账户 %s 金额 %s" % (src_user, dst_user, money))
        dst_dic["flow"].append("转账成功，由%s 转入 %s 金额 %s" % (src_user, dst_user, money))

        db_handler.save(src_dic)
        db_handler.save(dst_dic)
        logger.info("用户 %s ：转账成功，由%s 转入 %s 金额 %s" % (src_user, src_user, dst_user, money))
        return True, "转账成功，%s 转入 %s 金额 %s" % (src_user, dst_user, money)
    else:
        return False, "余额不足，转账失败"


def repay_interface(user, money):
    user_dic = db_handler.select(user)
    user_dic["balance"] += money
    user_dic["flow"].append("还款成功，还款金额为%s" % money)
    logger.info("用户 %s：还款成功，还款金额为%s" % (user, money))
    db_handler.save(user_dic)
    return "还款成功，还款金额为%s" % money


def check_flow_interface(user):
    user_dic = db_handler.select(user)
    logger.info("用户 %s 查询了流水" % user)
    return user_dic["flow"]
