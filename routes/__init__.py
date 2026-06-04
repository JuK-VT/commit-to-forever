from routes.auth import auth_bp
from routes.gifts import gifts_bp
from routes.main import main_bp
from routes.messages import messages_bp
from routes.rsvp import rsvp_bp


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(gifts_bp)
    app.register_blueprint(rsvp_bp)
    app.register_blueprint(messages_bp)
