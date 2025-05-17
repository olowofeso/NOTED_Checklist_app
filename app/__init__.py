import os
import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )
    
    # Get database URL from environment
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise ValueError("No DATABASE_URL environment variable set")


    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    # ── Simplified SSL forcing ──
    if '?' in db_url:
        db_url += '&sslmode=require'
    else:
        db_url += '?sslmode=require'
    
    # Apply to SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Remove custom connect_args entirely

    # Initialize extensions
    db.init_app(app)
    
    # Health check endpoint
    @app.route('/healthz')
    def health_check():
        try:
            db.session.execute(text('SELECT 1'))
            return 'OK', 200
        except Exception as e:
            app.logger.error(f"Health check failed: {str(e)}")
            return 'Database connection failed', 500

    # App-context setup & migrations
    with app.app_context():
        from . import routes
        routes.init_routes(app)
        
        # Initialize database with retries
        max_retries = 5
        for attempt in range(max_retries):
            try:
                db.create_all()
                app.logger.info("Database tables created successfully")
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    app.logger.error(
                        f"Failed to initialize database after {max_retries} attempts: {str(e)}"
                    )
                else:
                    app.logger.warning(
                        f"Database initialization attempt {attempt + 1} failed, retrying..."
                    )
                    time.sleep(5)
    
    return app


app = create_app()
