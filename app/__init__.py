from flask import Flask
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from app.extensions import db, migrate, login, mail, moment, csrf

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Proxy fix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    #initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)

    login.login_view = 'auth.login'

    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                        backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    from app.blog.routes import bp as blog_bp
    app.register_blueprint(blog_bp)

    from app.auth.routes import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.errors.routes import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.users.routes import bp as users_bp
    app.register_blueprint(users_bp)

    from app.main_routes import bp as main_bp
    app.register_blueprint(main_bp)
    return app
