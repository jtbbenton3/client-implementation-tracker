from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from .db import db

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # set up database and cors
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app, 
         origins=["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174", "http://localhost:3000"],
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])
    
    # login stuff
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    # add all the routes
    from .routes.auth import auth_bp
    from .routes.projects import projects_bp
    from .routes.milestones import milestones_bp
    from .routes.tasks import tasks_bp
    from .routes.comments import comments_bp
    from .routes.status_updates import status_updates_bp
    from .routes.user import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(milestones_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(status_updates_bp)
    app.register_blueprint(user_bp)

    return app