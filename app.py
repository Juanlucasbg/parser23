import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Database configuration
    database_url = os.environ.get("DATABASE_URL")
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url or "postgresql://localhost/cobol_analysis"
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # File upload configuration
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    
    # Create upload directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    
    # Add template filters
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        """Convert newlines to <br> tags"""
        if text is None:
            return ''
        return str(text).replace('\n', '<br>')
    
    with app.app_context():
        # Import models to ensure tables are created
        import models
        
        try:
            # Create all tables
            db.create_all()
            logging.info("Database tables created successfully")
            
            # Initialize database connections with error handling
            try:
                from database_setup import setup_weaviate_schema
                if setup_weaviate_schema():
                    logging.info("Weaviate schema initialized successfully")
                else:
                    logging.warning("Failed to initialize Weaviate schema - vector search may not work")
            except ImportError as e:
                logging.warning(f"Weaviate setup not available: {str(e)}")
            except Exception as e:
                logging.warning(f"Weaviate initialization failed: {str(e)}")
            
            # Initialize Cognee with error handling
            try:
                from knowledge import initialize_cognee
                if initialize_cognee():
                    logging.info("Cognee.ai initialized successfully")
                else:
                    logging.warning("Failed to initialize Cognee.ai - knowledge graph features may not work")
            except ImportError as e:
                logging.warning(f"Cognee setup not available: {str(e)}")
            except Exception as e:
                logging.warning(f"Cognee initialization failed: {str(e)}")
                
        except Exception as e:
            logging.error(f"Database initialization error: {str(e)}")
    
    # Register routes
    from routes import register_routes
    register_routes(app)
    
    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
