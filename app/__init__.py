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
    
    with app.app_context():
        from . import routes
        routes.init_routes(app)
        
        # Retry logic for database connection
        max_retries = 5
        retry_delay = 2
        for attempt in range(max_retries):
            try:
                db.create_all()
                break
            except OperationalError as e:
                if attempt == max_retries - 1:
                    raise e
                print(f"Database connection failed (attempt {attempt + 1}), retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
    
    return app