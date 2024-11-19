from .extensions import app, db
from flask_session import Session

def create_app():
    app.config.from_object("config.Config")

    db.init_app(app)

    with app.app_context():
        from . import routes, models
        db.create_all()

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Manejo de sesiones
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    return app