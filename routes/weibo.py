# 调用__init__模块
from routes import *
# 调用Weibo 数据模型和Comment 数据模型
from models.weibo import Weibo
from models.weibo import Comment


# 用蓝图把weibo 变成一个模块
main = Blueprint('weibo', __name__)


# 把square_index 视图函数注册为weibo 模块的路由'/weibo'
@main.route('/')
def public_index():
    u = current_user()
    if u is None:
        return redirect(url_for('user.index'))
    weibo_list = Weibo.query.order_by(Weibo.id.desc()).all()
    for w in weibo_list:
        w.comment = w.comments()
        w.commentNum = len(w.comment)
        w.avatar = w.get_avatar()
        for c in w.comment:
            c.avatar = c.get_avatar()
    return render_template('weibo_public.html', weibos=weibo_list)


# # 把personal_index 视图函数注册为weibo 模块的路由'/weibo/personal'
# @main.route('/personal')
# def personal_index():
#     u = current_user()
#     weibo_list = u.get_weibos
#     return render_template('weibo_personal.html', weibos=weibo_list)


# 把add 函数注册为weibo 模块的路由'/weibo/add'
@main.route('/add', methods=['POST'])
def add():
    u = current_user()
    form = request.form
    w = Weibo(form)
    w.username = u.username
    if w.valid():
        w.save()
    else:
        abort(400)
    return redirect(url_for('weibo.public_index'))


@main.route('/delete/<int:weibo_id>')
def delete(weibo_id):
    u = current_user()
    w = Weibo.query.get(weibo_id)
    user = User.query.filter_by(username=w.username).first()
    if u is user:
        w.delete()
    return redirect(url_for('weibo.public_index'))
