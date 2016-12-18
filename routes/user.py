# 调用__init__模块
from routes import *
# 调用User 数据模型
from models.user import User

# 用蓝图把user 变成一个模块
main = Blueprint('user', __name__)


# 把index()视图函数注册为user模块的路由'/'
@main.route('/')
def index():
    u = current_user()
    if u is not None:
        return redirect('/weibo')
    return render_template('user_login.html')
    # 如果用户存在（已登陆或注册），重定向到'/weibo'路由所在视图函数
    # 如果用户不存在，则打开注册登陆界面


# 把register()视图函数注册为user模块的路由'/user/register'
@main.route('/user/register', methods=['POST'])
def register():
    form = request.form
    u = User(form)
    if u.valid_register():
        u.save()
        print('注册成功')
        session['user_id'] = u.id
        return redirect('/weibo')
    else:
        return redirect(url_for('.index'))
    # 如果注册验证成功，把用户的id 存进session
    # 如果验证不成功，则重定向到注册登录界面


# 把switch()视图函数注册为user模块的路由'/user/switch'
@main.route('/user/switch')
def switch():
    return render_template('user_register.html')


# 把login()视图函数注册为user模块的路由'/user/login'
@main.route('/user/login', methods=['POST'])
def login():
    form = request.form
    u = User(form)
    user = User.query.filter_by(username=u.username).first()
    if user is not None and user.valid_login(u):
        print('登录成功')
        session['user_id'] = user.id
        return redirect('/weibo')
    else:
        print('登录失败')
        return redirect(url_for('.index'))
    # 如果用户输入的用户名和密码在数据库中存在且验证正确
    # 就把用户的id存进session中，切换到weibo页面
    # 否则重定向到注册登录页面


# 把update()视图函数注册为user模块的路由'/user/update'
@main.route('/user/update', methods=['POST'])
def update():
    u = current_user()
    password = request.form.get('password', '888')
    if u.change_password(password):
        print('修改成功')
    else:
        print('用户密码修改失败')
    return redirect('/user/profile')
    # 如果修改密码验证失败，重定向到用户个人界面


@main.route('/user/profile', methods=['GET'])
def profile():
    u = current_user()
    if u is not None:
        return render_template('profile.html', user=u)
    else:
        abort(400)


@main.route('/user/logout')
def logout():
    u = current_user()
    session.pop('user_id', None)
    return redirect(url_for('.index'))



