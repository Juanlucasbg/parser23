"""
Enhanced database models integrating advanced features from COBOL Documentation Generator
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
import time
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Enhanced User model with advanced features"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # User preferences for AI analysis
    preferred_llm_provider = db.Column(db.String(50), default='groq')
    preferred_llm_model = db.Column(db.String(100), default='llama-3.3-70b-versatile')
    documentation_style = db.Column(db.String(20), default='technical')  # technical, business, mixed
    detail_level = db.Column(db.String(10), default='medium')  # low, medium, high
    preferred_language = db.Column(db.String(10), default='en')
    
    # Relationships
    projects = db.relationship('Project', backref='owner', lazy=True)
    cobol_programs = db.relationship('CobolProgram', backref='user', lazy=True)
    analysis_sessions = db.relationship('AnalysisSession', backref='user', lazy=True)
    chat_messages = db.relationship('ChatMessage', backref='user', lazy=True)
    source_codes = db.relationship('SourceCodeQueue', backref='user', lazy=True)
    documents = db.relationship('DocGenerated', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Project(db.Model):
    """Enhanced Project model for organizing COBOL analysis work"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Project settings
    default_analysis_type = db.Column(db.String(20), default='comprehensive')
    auto_generate_docs = db.Column(db.Boolean, default=True)
    enable_diagrams = db.Column(db.Boolean, default=True)
    
    # Relationships
    cobol_files = db.relationship('CobolFile', backref='project', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Project {self.name}>'

class CobolFile(db.Model):
    """Enhanced COBOL file model with advanced metadata"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    program_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    
    # Enhanced metadata
    file_size = db.Column(db.Integer)
    encoding = db.Column(db.String(20), default='utf-8')
    dialect = db.Column(db.String(20), default='mainframe')
    last_analyzed = db.Column(db.DateTime)
    analysis_status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed
    
    # Relationships
    documentation = db.relationship('Documentation', backref='cobol_file', lazy=True, uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<CobolFile {self.filename}>'

class Documentation(db.Model):
    """Enhanced documentation model with advanced features"""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(10), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cobol_file_id = db.Column(db.Integer, db.ForeignKey('cobol_file.id'), nullable=False)
    
    # Enhanced documentation features
    documentation_type = db.Column(db.String(20), default='comprehensive')  # technical, business, comprehensive
    generation_method = db.Column(db.String(20), default='ai_generated')
    llm_provider = db.Column(db.String(50))
    llm_model = db.Column(db.String(100))
    quality_score = db.Column(db.Float)
    
    # Structured content
    summary = db.Column(db.Text)
    technical_details = db.Column(db.JSON)
    diagrams = db.Column(db.JSON)  # Mermaid diagrams and other visual elements
    recommendations = db.Column(db.JSON)
    
    def __repr__(self):
        return f'<Documentation for file {self.cobol_file_id}>'

# Original models enhanced with new features
class CobolProgram(db.Model):
    """Enhanced model for storing COBOL program metadata and analysis"""
    __tablename__ = 'cobol_programs'
    
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.String(100), nullable=False, index=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.Text)
    source_code = db.Column(db.Text)
    
    # Enhanced analysis data
    ast_structure = db.Column(db.JSON)
    procedures = db.Column(db.JSON)
    working_storage = db.Column(db.JSON)
    file_section = db.Column(db.JSON)
    dependencies = db.Column(db.JSON)
    copybooks = db.Column(db.JSON)
    business_rules = db.Column(db.Text)
    complexity = db.Column(db.String(20))
    line_count = db.Column(db.Integer)
    
    # New advanced features
    cyclomatic_complexity = db.Column(db.Integer)
    maintainability_score = db.Column(db.Float)
    security_issues = db.Column(db.JSON)
    performance_metrics = db.Column(db.JSON)
    modernization_suggestions = db.Column(db.JSON)
    
    # Metadata
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_analyzed = db.Column(db.DateTime)
    analysis_version = db.Column(db.String(20), default='1.0')
    
    def to_dict(self):
        """Convert model to dictionary with enhanced data"""
        return {
            'id': self.id,
            'program_id': self.program_id,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'complexity': self.complexity,
            'line_count': self.line_count,
            'cyclomatic_complexity': self.cyclomatic_complexity,
            'maintainability_score': self.maintainability_score,
            'procedures': self.procedures,
            'working_storage': self.working_storage,
            'dependencies': self.dependencies,
            'copybooks': self.copybooks,
            'business_rules': self.business_rules,
            'security_issues': self.security_issues,
            'performance_metrics': self.performance_metrics,
            'modernization_suggestions': self.modernization_suggestions,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_analyzed': self.last_analyzed.isoformat() if self.last_analyzed else None
        }

class AnalysisSession(db.Model):
    """Enhanced model for tracking comprehensive analysis sessions"""
    __tablename__ = 'analysis_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    programs_count = db.Column(db.Integer, default=0)
    processing_status = db.Column(db.String(50), default='pending')
    
    # Enhanced session tracking
    analysis_type = db.Column(db.String(50), default='comprehensive')  # basic, comprehensive, security, modernization
    llm_provider = db.Column(db.String(50))
    llm_model = db.Column(db.String(100))
    quality_threshold = db.Column(db.Float, default=0.8)
    
    # Progress tracking
    current_stage = db.Column(db.String(50))
    progress_percentage = db.Column(db.Integer, default=0)
    estimated_completion = db.Column(db.DateTime)
    
    # Results and metadata
    error_message = db.Column(db.Text)
    performance_metrics = db.Column(db.JSON)
    resource_usage = db.Column(db.JSON)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'programs_count': self.programs_count,
            'processing_status': self.processing_status,
            'analysis_type': self.analysis_type,
            'current_stage': self.current_stage,
            'progress_percentage': self.progress_percentage,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error_message': self.error_message
        }

class ChatMessage(db.Model):
    """Enhanced model for storing AI chat interactions"""
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message_type = db.Column(db.String(20), nullable=False)  # user, assistant, system
    content = db.Column(db.Text, nullable=False)
    
    # Enhanced chat features
    query_type = db.Column(db.String(50))  # dependencies, explain, similar, general, code_review
    context_data = db.Column(db.JSON)  # Referenced programs, files, etc.
    llm_provider = db.Column(db.String(50))
    llm_model = db.Column(db.String(100))
    response_time = db.Column(db.Float)  # Response time in seconds
    quality_rating = db.Column(db.Integer)  # 1-5 user rating
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'message_type': self.message_type,
            'content': self.content,
            'query_type': self.query_type,
            'context_data': self.context_data,
            'llm_provider': self.llm_provider,
            'response_time': self.response_time,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Ledger system models from advanced app
class SourceCodeQueue(db.Model):
    """Advanced source code queue system for processing large files"""
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(15), nullable=False, index=True)
    source_language = db.Column(db.String(20), nullable=False, index=True)
    input_source = db.Column(db.String(50), nullable=False)
    source_name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False, index=True)
    source_id = db.Column(db.String(300), nullable=False, unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    
    # Enhanced processing metadata
    file_size = db.Column(db.Integer)
    encoding = db.Column(db.String(20))
    processing_priority = db.Column(db.Integer, default=1)
    retry_count = db.Column(db.Integer, default=0)
    last_error = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    content = db.relationship('SourceCodeContent', backref='source_queue', lazy=True,
                             uselist=False, cascade='all, delete-orphan')
    documents = db.relationship('DocGenerated', backref='source_code', lazy=True)
    
    @staticmethod
    def generate_timestamp():
        """Generate timestamp in YYMMDD_HHMMSS format"""
        return time.strftime("%y%m%d_%H%M%S", time.gmtime())
    
    @staticmethod
    def generate_source_id(timestamp, language, source_name):
        """Generate composite source ID"""
        clean_name = source_name.replace(' ', '_').replace('/', '_').replace('\\', '_')
        return f"{timestamp}_{language}_{clean_name}"
    
    def __repr__(self):
        return f'<SourceCodeQueue {self.source_id}>'

class SourceCodeContent(db.Model):
    """Storage for large source code content"""
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.String(300), db.ForeignKey('source_code_queue.source_id'),
                         nullable=False, unique=True, index=True)
    content = db.Column(db.Text, nullable=False)
    
    # Content metadata
    original_encoding = db.Column(db.String(20))
    line_count = db.Column(db.Integer)
    character_count = db.Column(db.Integer)
    checksum = db.Column(db.String(64))  # For integrity verification
    
    def __repr__(self):
        return f'<SourceCodeContent for {self.source_id}>'

class DocGenerated(db.Model):
    """Advanced documentation generation tracking"""
    id = db.Column(db.Integer, primary_key=True)
    result_doc_id = db.Column(db.String(300), nullable=False, unique=True, index=True)
    result_doc_status = db.Column(db.String(50), nullable=False, index=True)
    doc_timestamp = db.Column(db.String(15), nullable=False, index=True)
    doc_source_code_id = db.Column(db.String(300), db.ForeignKey('source_code_queue.source_id'),
                                 nullable=False, index=True)
    status = db.Column(db.String(50), nullable=False, index=True)
    doc_content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    in_language = db.Column(db.String(20), nullable=False)
    
    # Enhanced documentation metadata
    generation_method = db.Column(db.String(50))  # ai_agent, direct_llm, template
    llm_provider = db.Column(db.String(50))
    llm_model = db.Column(db.String(100))
    quality_score = db.Column(db.Float)
    word_count = db.Column(db.Integer)
    diagram_count = db.Column(db.Integer)
    processing_time = db.Column(db.Float)  # Generation time in seconds
    
    # Structured content
    summary = db.Column(db.Text)
    technical_sections = db.Column(db.JSON)
    diagrams = db.Column(db.JSON)
    recommendations = db.Column(db.JSON)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def generate_result_doc_id(doc_timestamp, source_id):
        """Generate result document ID"""
        return f"RESULT_{doc_timestamp}_{source_id}"
    
    def __repr__(self):
        return f'<DocGenerated {self.result_doc_id}>'

# System monitoring and performance tracking
class SystemStats(db.Model):
    """Enhanced system statistics and monitoring"""
    __tablename__ = 'system_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    total_programs = db.Column(db.Integer, default=0)
    total_lines_of_code = db.Column(db.Integer, default=0)
    complexity_breakdown = db.Column(db.JSON)
    dependency_count = db.Column(db.Integer, default=0)
    
    # Enhanced analytics
    avg_maintainability_score = db.Column(db.Float)
    total_security_issues = db.Column(db.Integer, default=0)
    modernization_candidates = db.Column(db.Integer, default=0)
    total_documentation_generated = db.Column(db.Integer, default=0)
    avg_generation_time = db.Column(db.Float)
    
    # Performance metrics
    active_users = db.Column(db.Integer, default=0)
    total_api_calls = db.Column(db.Integer, default=0)
    avg_response_time = db.Column(db.Float)
    error_rate = db.Column(db.Float, default=0.0)
    
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'total_programs': self.total_programs,
            'total_lines_of_code': self.total_lines_of_code,
            'complexity_breakdown': self.complexity_breakdown,
            'dependency_count': self.dependency_count,
            'avg_maintainability_score': self.avg_maintainability_score,
            'total_security_issues': self.total_security_issues,
            'modernization_candidates': self.modernization_candidates,
            'total_documentation_generated': self.total_documentation_generated,
            'avg_generation_time': self.avg_generation_time,
            'active_users': self.active_users,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }