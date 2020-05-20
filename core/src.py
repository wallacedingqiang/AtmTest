from interface import user_interface, bank_interface, shop_interface
from lib import common
import pysnooper


user_info = {}

@pysnooper.snoop()
# 1.注册
def register():
    while True:
        user = input("请输入需要注册的用户名：").strip()
        pwd = input("请输入密码：").strip()
        re_pwd = input("请再次输入密码：").strip()
        if pwd == re_pwd:
            flag, msg = user_interface.register_interface(user, pwd)
            if flag:
                print(msg)
                break
            else:
                print(msg)
        else:
            print("密码不一致，请重新输入")

@pysnooper.snoop()
# 2.登录
def login():
    while True:
        user = input("请输入用户名：").strip()
        pwd = input("请输入密码：").strip()
        flag, msg = user_interface.login_interface(user, pwd)
        if flag:
            print(msg)
            user_info["name"] = user
            break
        else:
            print(msg)


# 3.查看余额
@common.auth_register
def check_balance():
    res_balance = user_interface.check_balance_interface(user_info["name"])
    print("余额为%s" % (res_balance,))


# 4.提现
@common.auth_register
def withdraw():
    while True:
        money = input("需要提现的金额：").strip()
        if money.isdigit():
            money = int(money)
        flag, msg = bank_interface.withdraw_interface(user_info["name"], money)
        if flag:
            print(msg)
            break
        else:
            print(msg)


# 5.转账
@common.auth_register
def transfer():
    while True:
        dst_user = input("请输入转账目标用户：").strip()
        money = input("请输入转账金额：").strip()
        if money.isdigit():
            money = int(money)
        flag, msg = bank_interface.transfer_interface(user_info["name"], dst_user, money)
        if flag:
            print(msg)
            break
        else:
            print(msg)


# 6.还款
@common.auth_register
def repay():
    while True:
        money = input("请输入还款金额（输入q退出）：").strip()
        if money == 'q':
            break
        if money.isdigit():
            money = int(money)
            msg = bank_interface.repay_interface(user_info["name"], money)
            print(msg)
            break
        else:
            print("非法输入，请重新输入数字")
            continue


# 7.查看流水
@common.auth_register
def check_flow():
    flow_list = bank_interface.check_flow_interface(user_info["name"])
    for line in flow_list:
        print(line)


# 8.购物车功能
@common.auth_register
def shopping_cart():
    goods_list = shop_interface.get_goods_interface()
    shopping_car_dic = shop_interface.get_shopping_cart(user_info["name"])

    while True:
        for index, good_list in enumerate(goods_list):
            print('商品编号：' + str(index), good_list[0], good_list[1])
        choice = input("请选择需要的商品编号（按q退出）：").strip()
        if choice.isdigit() and len(goods_list) >= int(choice) >= 0:
            choice = int(choice)
            if choice in shopping_car_dic:
                shopping_car_dic[choice] += 1
            else:
                shopping_car_dic[choice] = 1
            option = input("是否需要继续购物（输入y结算，输入n加入购物车结束，其他输入继续）：")
            if option == "y":
                flag, msg = shop_interface.shopping_pay_interface(user_info["name"], shopping_car_dic)
                if flag:
                    print(msg)
                    break
                else:
                    print(msg)
            if option == "n":
                shop_interface.add_shopping_cart_interface(user_info["name"], shopping_car_dic)
                break
        else:
            print("商品编号不存在，请重新输入")


# 9.查看购物车
@common.auth_register
def check_shopping_cart():
    user_shopping_cart_dic, goods_list = shop_interface.check_shopping_cart_interface(user_info["name"])
    for k, num in user_shopping_cart_dic.items():
        print(goods_list[int(k)][0] + " 数量：" + str(num))


# 10.注销
@common.auth_register
def logout():
    user_info = {}
    print("用户已注销")


# 11.管理员登录
def admin_login():
    while True:
        user = "admin"
        pwd = input("请输入管理员密码：").strip()
        flag, msg = user_interface.admin_login_interface(user, pwd)
        if flag:
            print(msg)
            res = admin_func()
            if not res:
                logger = common.get_logger("admin_user")
                logger.info("管理员已退出")
                print("管理员已退出")
                break

        else:
            print(msg)


def admin_func():
    while True:
        option = input('''
        1. 添加账户
        2. 用户额度
        3. 冻结账户
        按q退出
        ''')
        if option == "q":
            break
        elif option in admin_func_map:
            flag, msg = admin_func_map[option]()
            if flag:
                print(msg)
                continue
            else:
                print(msg)
        else:
            print("错误输入请重新输入")


def _admin_add_user():
    user = input("需要添加的用户名：").strip()
    pwd = input("添加的用户密码：").strip()
    return user_interface.admin_add_user_interface(user, pwd)


def _admin_change_user_balance():
    user = input("需要修改额度的用户名：").strip()
    balance = input("请输入用户的具体额度：").strip()
    return user_interface.admin_change_user_interface(user, balance)


def _admin_close_user():
    user = input("需要冻结的用户名：").strip()
    return user_interface.admin_close_user_interface(user)


func_map = {
    "1": register,
    "2": login,
    "3": check_balance,
    "4": withdraw,
    "5": transfer,
    "6": repay,
    "7": check_flow,
    "8": shopping_cart,
    "9": check_shopping_cart,
    "10": logout,
    "11": admin_login
}

admin_func_map = {
    '1': _admin_add_user,
    '2': _admin_change_user_balance,
    '3': _admin_close_user
}



@pysnooper.snoop()
def run():
    while True:
        print('''
1.注册
2.登录
3.查看余额
4.提现
5.转账
6.还款
7.查看流水
8.购物车功能
9.查看购物车
10.注销
11.管理员功能
q.退出''')

        choice = input("请输入需要的功能（数字）：").strip()

        if choice == 'q':
            print("退出主程序")
            break
        if not choice in func_map:
            print("所选编号功能不存在,请重新输入")
            continue
        func_map[choice]()
