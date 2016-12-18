from routes import *
from models.weibo import Comment
from models.user import User


main = Blueprint('comment', __name__)


@main.route('/comment/add', methods=['POST'])
def add():
    u = current_user()
    form = request.form
    c = Comment(form)
    c.username = u.username
    if c.valid():
        c.save()
    else:
        abort(400)
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 todo
    return redirect(url_for('weibo.public_index'))