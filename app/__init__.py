import os
from flask import Flask
import time
from flask_sqlalchemy import SQLAlchemy
import urllib.parse

db = SQLAlchemy()

def create_app():
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')
    
    # Configure database with SSL 
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise ValueError("No DATABASE_URL environment variable set")
    
    # Fix common URL format issues
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    # Parse and rebuild URL to ensure proper encoding
    parsed = urllib.parse.urlparse(db_url)
    secure_url = urllib.parse.urlunparse(parsed._replace(
        query='sslmode=require'
    ))
    
    app.config['SQLALCHEMY_DATABASE_URI'] = secure_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300
    }
    
    db.init_app(app)
    
    # Add health check endpoint
    @app.route('/healthz')
    def health_check():
        try:
            db.session.execute('SELECT 1')
            return 'OK', 200
        except Exception:
            return 'Database connection failed', 500
    
    with app.app_context():
        from . import routes
        routes.init_routes(app)
        
        # Retry database initialization
        max_retries = 3
        for attempt in range(max_retries):
            try:
                db.create_all()
                print("Database tables created successfully")
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"Failed to initialize database after {max_retries} attempts: {str(e)}")
                else:
                    print(f"Database initialization attempt {attempt + 1} failed, retrying...")
                    time.sleep(5)
    
    return app