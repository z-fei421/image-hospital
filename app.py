from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from config import config

db = SQLAlchemy()

def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from routes.upload import upload_bp
    from routes.diagnosis import diagnosis_bp
    from routes.treatment import treatment_bp
    from routes.report import report_bp
    from routes.history import history_bp
    from routes.main import main_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(diagnosis_bp)
    app.register_blueprint(treatment_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(history_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
