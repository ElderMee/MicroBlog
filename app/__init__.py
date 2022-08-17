from flask import Flask  # 从flask包中导入Flask类
from flask import request
from flask_babel import Babel, lazy_gettext as _l
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)  # 将Flask类的实例 赋值给名为 app 的变量。这个实例成为app包的成员。

# print('等会谁（哪个包或模块）在使用我：', __name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')

mail = Mail(app)

bootstrap = Bootstrap(app)

moment = Moment(app)

babel = Babel(app)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])


# 放在后面可以防止循环引用
from app import routes, models
