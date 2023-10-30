from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


import config

db = SQLAlchemy()
migrate = Migrate()

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    #ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from .models import board_model

    #Mail
    mail.init_app(app)

    # views
    from .views import main_view, board_view, comment_view, notice_view, notice_comment_view,  auth_view
    app.register_blueprint(main_view.bp)
    app.register_blueprint(board_view.bp)
    app.register_blueprint(comment_view.bp)
    app.register_blueprint(notice_view.bp)
    app.register_blueprint(notice_comment_view.bp)
    app.register_blueprint(auth_view.bp)

    return app
