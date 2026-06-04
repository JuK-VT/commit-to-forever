import logging

from flask import Flask

from config import Config
from routes import register_blueprints


def create_app():
    logging.basicConfig(level=logging.INFO)
    app = Flask(__name__)
    app.config.from_object(Config)
    register_blueprints(app)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=app.config.get('DEBUG', True))
