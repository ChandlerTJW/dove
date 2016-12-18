from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from models import db

from models.user import User
from models.weibo import Weibo

app = Flask(__name__)
db_path = 'weibo.sqlite'
manager = Manager(app)


def register_routes(app):
    from routes.user import main as routes_user
    from routes.weibo import main as routes_weibo
    from routes.comment import main as routes_comment

    app.register_blueprint(routes_user)
    app.register_blueprint(routes_weibo, url_prefix='/weibo')
    app.register_blueprint(routes_comment)


def configure_app():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = 'secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    db.init_app(app)
    register_routes(app)


def configured_app():
    configure_app()
    return app


@manager.command
def server():
    print('server run')
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=3000,
    )
    app.run(**config)


def configure_manager():
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    configure_manager()
    configure_app()
    manager.run()
