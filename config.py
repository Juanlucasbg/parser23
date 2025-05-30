"""
Mainframe Atlas Configuration
Centralized configuration for the holistic COBOL documentation platform
"""
import os
from typing import Dict, Any

class Config:
    """Main configuration class for Mainframe Atlas"""
    
    # Core Application Settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mainframe-atlas-dev-key-2024')
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # Database Configuration
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://localhost/mainframe_atlas')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Service Architecture Configuration
    MICROSERVICES_MODE = os.environ.get('MICROSERVICES_MODE', 'False').lower() == 'true'
    
    # Parser Service Configuration
    PARSER_SERVICE_URL = os.environ.get('PARSER_SERVICE_URL', 'http://localhost:8001')
    PARSER_TIMEOUT = int(os.environ.get('PARSER_TIMEOUT', '300'))  # 5 minutes
    
    # Graph Service Configuration (Neo4j)
    NEO4J_URI = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USERNAME = os.environ.get('NEO4J_USERNAME', 'neo4j')
    NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD', 'password')
    
    # Vector Service Configuration (Weaviate)
    WEAVIATE_URL = os.environ.get('WEAVIATE_URL', 'http://localhost:8080')
    WEAVIATE_API_KEY = os.environ.get('WEAVIATE_API_KEY', '')
    
    # LLM Orchestrator Configuration
    LLM_ORCHESTRATOR_URL = os.environ.get('LLM_ORCHESTRATOR_URL', 'http://localhost:8003')
    
    # External LLM Provider Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    PERPLEXITY_API_KEY = os.environ.get('PERPLEXITY_API_KEY', '')
    
    # SCM Integration Configuration
    ENDEVOR_BASE_URL = os.environ.get('ENDEVOR_BASE_URL', '')
    ENDEVOR_USERNAME = os.environ.get('ENDEVOR_USERNAME', '')
    ENDEVOR_PASSWORD = os.environ.get('ENDEVOR_PASSWORD', '')
    
    GIT_REPOS_BASE_PATH = os.environ.get('GIT_REPOS_BASE_PATH', './repositories')
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', '16777216'))  # 16MB
    ALLOWED_EXTENSIONS = {'cbl', 'cob', 'cobol', 'jcl', 'bms', 'sql', 'txt'}
    
    # Ingestion Configuration
    INGESTION_BATCH_SIZE = int(os.environ.get('INGESTION_BATCH_SIZE', '100'))
    INGESTION_PARALLEL_WORKERS = int(os.environ.get('INGESTION_PARALLEL_WORKERS', '4'))
    
    # Documentation Configuration
    DOCS_STORAGE_PATH = os.environ.get('DOCS_STORAGE_PATH', './documentation')
    DOCS_FORMAT = os.environ.get('DOCS_FORMAT', 'markdown')
    
    # Performance Configuration
    API_RESPONSE_TIMEOUT = int(os.environ.get('API_RESPONSE_TIMEOUT', '30'))
    VECTOR_SEARCH_TIMEOUT = int(os.environ.get('VECTOR_SEARCH_TIMEOUT', '5'))
    
    # Security Configuration
    ENABLE_MTLS = os.environ.get('ENABLE_MTLS', 'False').lower() == 'true'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', '3600'))  # 1 hour
    
    # Feature Flags
    ENABLE_AI_GENERATION = os.environ.get('ENABLE_AI_GENERATION', 'True').lower() == 'true'
    ENABLE_GRAPH_ANALYSIS = os.environ.get('ENABLE_GRAPH_ANALYSIS', 'True').lower() == 'true'
    ENABLE_VECTOR_SEARCH = os.environ.get('ENABLE_VECTOR_SEARCH', 'True').lower() == 'true'
    ENABLE_CICD_INTEGRATION = os.environ.get('ENABLE_CICD_INTEGRATION', 'False').lower() == 'true'
    
    @classmethod
    def get_service_config(cls) -> Dict[str, Any]:
        """Get configuration for service discovery and communication"""
        return {
            'parser_service': {
                'url': cls.PARSER_SERVICE_URL,
                'timeout': cls.PARSER_TIMEOUT,
                'enabled': True
            },
            'graph_service': {
                'neo4j_uri': cls.NEO4J_URI,
                'username': cls.NEO4J_USERNAME,
                'password': cls.NEO4J_PASSWORD,
                'enabled': cls.ENABLE_GRAPH_ANALYSIS
            },
            'vector_service': {
                'weaviate_url': cls.WEAVIATE_URL,
                'api_key': cls.WEAVIATE_API_KEY,
                'enabled': cls.ENABLE_VECTOR_SEARCH
            },
            'llm_orchestrator': {
                'url': cls.LLM_ORCHESTRATOR_URL,
                'enabled': cls.ENABLE_AI_GENERATION,
                'providers': {
                    'openai': bool(cls.OPENAI_API_KEY),
                    'groq': bool(cls.GROQ_API_KEY),
                    'perplexity': bool(cls.PERPLEXITY_API_KEY)
                }
            }
        }
    
    @classmethod
    def get_scm_config(cls) -> Dict[str, Any]:
        """Get SCM integration configuration"""
        return {
            'endevor': {
                'base_url': cls.ENDEVOR_BASE_URL,
                'username': cls.ENDEVOR_USERNAME,
                'password': cls.ENDEVOR_PASSWORD,
                'enabled': bool(cls.ENDEVOR_BASE_URL)
            },
            'git': {
                'repos_path': cls.GIT_REPOS_BASE_PATH,
                'enabled': True
            }
        }
    
    @classmethod
    def validate_config(cls) -> Dict[str, bool]:
        """Validate configuration and return service availability"""
        validation = {
            'database': bool(cls.DATABASE_URL),
            'neo4j': bool(cls.NEO4J_URI and cls.NEO4J_USERNAME),
            'weaviate': bool(cls.WEAVIATE_URL),
            'llm_providers': any([
                cls.OPENAI_API_KEY,
                cls.GROQ_API_KEY,
                cls.PERPLEXITY_API_KEY
            ]),
            'scm_integration': any([
                cls.ENDEVOR_BASE_URL,
                os.path.exists(cls.GIT_REPOS_BASE_PATH)
            ])
        }
        return validation

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False
    MICROSERVICES_MODE = False  # Monolithic for development

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False
    MICROSERVICES_MODE = True
    
    # Enhanced security for production
    ENABLE_MTLS = True
    
    # Performance optimizations
    INGESTION_PARALLEL_WORKERS = 8
    API_RESPONSE_TIMEOUT = 15

class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DEBUG = True
    DATABASE_URL = 'sqlite:///:memory:'
    MICROSERVICES_MODE = False

# Configuration selector
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}