# 从__init__模块调用ModelHelper,db,current_time
from . import ModelHelper
from . import db
from . import current_time


# 定义weibo数据类型
class Weibo(db.Model, ModelHelper):
    # 设置表名
    __tablename__ = 'weibos'
    # 定义weibos表的各个列（字段）
    id = db.Column(db.Integer, primary_key=True)
    # id，数据类型为整数，此字段设为主键
    content = db.Column(db.String())
    # 内容，数据类型位字符串，限定200个字符
    created_time = db.Column(db.Integer, default=0)
    # 创建时间，数据类型为整数，默认值为0
    username = db.Column(db.String())
    avatar = db.Column(db.String())

    # 初始化Weibo 类的属性
    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = current_time()
        self.username = ''
        self.comment = ''
        self.avatar = ''

    def comments(self):
        cs = Comment.query.filter_by(weibo_id=self.id).all()
        return cs

    # weibo内容不能为空
    def valid(self):
        return len(self.content) > 0

    def json(self):
        d = dict(
            id=self.id,
            content=self.content,
            created_time=self.created_time,
            username=self.username,
            avatar=self.avatar,
            comment=self.comment,
        )

    def get_avatar(self):
        from models.user import User
        u = User.query.filter_by(username=self.username).first()
        if u.gender == 'male':
            return 'http://upload-images.jianshu.io/upload_images/3425393-5d1a37667ddfd937.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240'
        else:
            return 'http://upload-images.jianshu.io/upload_images/3425393-86a758dfb0c0ac01.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240'


# 定义Comment数据类型
class Comment(db.Model, ModelHelper):
    # 设置表名
    __tablename__ = 'comments'
    # 定义comments 表的各个列（字段）
    id = db.Column(db.Integer, primary_key=True)
    # id, 数据类型为整数，主键
    content = db.Column(db.String())
    # 内容，数据类型为字符串
    username = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    # 创建时间，数据类型为整数，默认值为0
    weibo_id = db.Column(db.Integer)
    # weibo_id，数据类型为整数

    # 初始化Comment 类的属性
    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = current_time()
        self.username = ''
        self.weibo_id = form.get('weibo_id', '')

    def get_avatar(self):
        from models.user import User
        u = User.query.filter_by(username=self.username).first()
        if u.gender == 'male':
            return 'http://upload-images.jianshu.io/upload_images/3425393-5d1a37667ddfd937.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240'
        else:
            return 'http://upload-images.jianshu.io/upload_images/3425393-86a758dfb0c0ac01.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240'

    def json(self):
        d = dict(
            id=self.id,
            content=self.content,
            created_time=self.created_time,
            username=self.username,
            avatar=self.avatar,
            weibo_id=self.weibo_id,
        )

    def valid(self):
        return len(self.content) > 0

