import os
import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError

db = SQLAlchemy()

def create_app():
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')
    
    # PostgreSQL configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgres@db:5432/todos_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    # Add delay before first connection attempt
    time.sleep(5)
    
    with app.app_context():
        from . import routes
        routes.init_routes(app)
        
        # More robust connection handling
        max_retries = 10
        retry_delay = 5
        for attempt in range(max_retries):
            try:
                db.create_all()
                print("Database connection successful!")
                break
            except OperationalError as e:
                if attempt == max_retries - 1:
                    print(f"Failed to connect to database after {max_retries} attempts")
                    raise e
                print(f"Database connection failed (attempt {attempt + 1}), retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
    
    return app