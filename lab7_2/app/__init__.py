from flask import Flask
from .extensions import db
from .blueprints.api.hosts import api_bp
from .blueprints.ui import ui

def create_app(conf="config.Config"):
    app=Flask(__name__)
    app.config.from_object(conf)
    db.init_app(app)
    app.register_blueprint(api_bp, url_prefix = "/api")
    app.register_blueprint(ui)
    with app.app_context():
        from .models import Host
        db.create_all()
    return app
