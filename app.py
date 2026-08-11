import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from models import db
from routes.auth import auth_bp
from routes.analysis import analysis_bp
from routes.health import health_bp

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-me")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "change-me-too")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///agrishield.db"
    ).replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    CORS(app, resources={r"/api/*": {"origins": os.getenv("CORS_ORIGINS", "*")}})
    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(analysis_bp, url_prefix="/api")
    app.register_blueprint(health_bp, url_prefix="/api")

    # Serve the bundled frontend from the same Flask server.
    # This keeps frontend and backend on the same origin and avoids
    # opening index.html through a separate static server.
    frontend_dir = os.path.join(app.root_path, "frontend")

    @app.get("/")
    def home():
        return send_from_directory(frontend_dir, "index.html")

    @app.get("/frontend/<path:filename>")
    def frontend_static(filename):
        return send_from_directory(frontend_dir, filename)

    return app

app=create_app()

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
