from db import db_handler
from lib.common import get_logger
from conf.settings import db_path
import os
import sqlite3
import pysnooper


@pysnooper.snoop()
def register_interface(user, pwd):
    if db_handler.select(user):
        return False, "用户已存在"

    user_dic = {
        "name": user,
        "password": pwd,
        "balance": 15000,
        "flow": [],
        "shopping_cart": {}
    }

    db_handler.save(user_dic)

    # # 存放数据库
    # conn = sqlite3.connect('atm.db')  # 创建一个数据库链接
    # cmd = "INSERT INTO USERS (name,password,balance,flow) VALUES ('{}',\"{}\",\"{}\",\"{}\")".format(
    #     user_dic['name'], user_dic['password'], user_dic['balance'], user_dic['flow'])  # 将用户输入的信息写入数据库
    # print(cmd)
    # conn.execute(cmd)  # 写入数据到数据库
    # conn.commit()  # 提交
    # conn.close()  # 关闭数据库链接

    return True, "用户：%s 注册成功" % user


def login_interface(user, pwd):
    user_dic = db_handler.select(user)
    print(user_dic)

    # conn = sqlite3.connect('atm.db')  # 创建一个数据库链接
    # check = "SELECT password FROM USERS WHERE name = {}".format(user)  # 核对账户密码是否正确
    # conn.execute(check)  # 写入数据到数据库
    # conn.commit()  # 提交
    # conn.close()  # 关闭数据库链接

    if user == "admin":
        return False, "不能以管理员身份登录"

    if not user_dic:
        return False, "用户不存在，请重新登录"

    if pwd == user_dic["password"]:
        return True, "登录成功"
    else:
        return False, "密码错误"


def check_balance_interface(user):
    user_dic = db_handler.select(user)
    return user_dic["balance"]


def admin_login_interface(user, pwd):
    admin_dic = db_handler.select(user)
    logger = get_logger("admin_user")

    if pwd == admin_dic["password"]:
        logger.info("登录成功")
        return True, "登录成功"
    logger.info("登录失败")
    return False, "登录失败"


def admin_add_user_interface(user, pwd):
    flag, msg = register_interface(user, pwd)
    logger = get_logger("admin_user")
    logger.info("添加用户：%s 成功" % user)
    return flag, msg


def admin_change_user_interface(user, balance):
    user_dic = db_handler.select(user)
    user_dic["balance"] = int(balance)
    db_handler.save(user_dic)
    logger = get_logger("admin_user")
    logger.info("修改用户：%s 额度为 %s " % (user, balance))
    return True, "修改用户：%s 额度为 %s " % (user, balance)


def admin_close_user_interface(user):
    dbfile = os.path.join(db_path, "%s.json" % user)
    if not os.path.exists(dbfile):
        return False, "需要冻结的用户：%s 不存在" % user
    os.rename(dbfile, dbfile+".close")
    logger = get_logger("admin_user")
    logger.info("冻结用户：%s 成功" % user)
    return True, "冻结用户：%s 成功" % user








