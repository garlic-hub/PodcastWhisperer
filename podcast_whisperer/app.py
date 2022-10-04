import os.path
from flask import Flask

from . import database
from . import auth
from . import site


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'whisperer.db'),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    database.init_app(app)

    app.register_blueprint(auth.bp)

    app.register_blueprint(site.bp)
    app.add_url_rule('/', endpoint='index')

    return app
