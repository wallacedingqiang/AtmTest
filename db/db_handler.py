import os
import json
from conf import settings
import pysnooper

@pysnooper.snoop()
def save(user_dic):
    if not os.path.exists(settings.db_path):
        os.mkdir(settings.db_path)
    file_path = os.path.join(os.path.dirname(__file__), "%s.json" % (user_dic["name"],))
    with open(file_path, 'w', encoding="utf-8") as f:
        json.dump(user_dic, f)
        f.flush()

@pysnooper.snoop()
def select(user):
    userinfo_path = os.path.join(settings.db_path, "%s.json" % (user,))
    if os.path.exists(userinfo_path): #如果用户信息文件存在的话
        with open(userinfo_path, 'r', encoding="utf-8") as f:
            user_dic = json.load(f)
        return user_dic
