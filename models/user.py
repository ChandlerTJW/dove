# 从__init__模块调用ModelHelper和db
from . import ModelHelper
from . import db
from . import current_time
from models.weibo import Weibo


# 定义用户数据模型
class User(db.Model, ModelHelper):
    # 设置表名
    __tablename__ = 'users'
    # 定义users表的各个列（字段）
    id = db.Column(db.Integer, primary_key=True)
    # id,数据类型为整数，此字段为主键
    username = db.Column(db.String())
    # 用户名，数据类型为字符串
    password = db.Column(db.String())
    # 密码，数据类型为字符串
    created_time = db.Column(db.Integer, default=0)
    # 创建时间，数据类型为整数，默认值为0
    avatar = db.Column(db.String())
    # 头像，数据类型为字符串
    gender = db.Column(db.String())
    # 性别，数据类型为字符串

    # 初始化User 对象的属性
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.created_time = current_time()
        self.avatar = ''
        self.gender = form.get('gender', '')

    # 用户名要2位及以上
    # 密码要6位及以上
    def valid_register(self):
        return len(self.username) >= 2 and len(self.password) >= 6

    # 用户名和密码相等，登陆验证成功
    def valid_login(self, u):
        return u.username == self.username and u.password == self.password

    def get_weibos(self):
        weibos = Weibo.query.filter_by(username=self.username).all()
        return weibos

    # 如果密码在6位及以上，修改并保存
    def change_password(self, password):
        if len(password) >= 6:
            self.password = password
            self.save()
            return True
        else:
            return False

