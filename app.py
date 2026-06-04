import logging

from flask import Flask

from config import Config
from routes import register_blueprints
from services.wedding_service import WeddingService


def create_app():
    logging.basicConfig(level=logging.INFO)
    app = Flask(__name__)
    app.config.from_object(Config)
    register_blueprints(app)

    @app.context_processor
    def inject_wedding():
        try:
            return {'wedding': WeddingService.get()}
        except Exception:
            return {'wedding': {}}

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=app.config.get('DEBUG', True))
