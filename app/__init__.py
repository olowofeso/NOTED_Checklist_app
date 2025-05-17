import os
import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    with app.app_context():
        # Delay to ensure db is ready
        time.sleep(5)
        
        from . import routes
        routes.init_routes(app)
        
        try:
            db.create_all()
            print("Database tables created successfully")
        except Exception as e:
            print(f"Database initialization failed: {str(e)}")
            # Don't raise here - let the app start without tables
    
    return app