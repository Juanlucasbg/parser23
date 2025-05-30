from datetime import datetime
from app import db
from sqlalchemy import text
import json

class CobolProgram(db.Model):
    """Model for storing COBOL program metadata"""
    __tablename__ = 'cobol_programs'
    
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.String(100), nullable=False, index=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.Text)
    source_code = db.Column(db.Text)
    ast_structure = db.Column(db.JSON)
    procedures = db.Column(db.JSON)
    working_storage = db.Column(db.JSON)
    file_section = db.Column(db.JSON)
    dependencies = db.Column(db.JSON)
    copybooks = db.Column(db.JSON)
    business_rules = db.Column(db.Text)
    complexity = db.Column(db.String(20))
    line_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'program_id': self.program_id,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'source_code': self.source_code,
            'ast_structure': self.ast_structure,
            'procedures': self.procedures or [],
            'working_storage': self.working_storage or [],
            'file_section': self.file_section or [],
            'dependencies': self.dependencies or [],
            'copybooks': self.copybooks or [],
            'business_rules': self.business_rules,
            'complexity': self.complexity,
            'line_count': self.line_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class AnalysisSession(db.Model):
    """Model for tracking analysis sessions"""
    __tablename__ = 'analysis_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    programs_count = db.Column(db.Integer, default=0)
    processing_status = db.Column(db.String(50), default='pending')  # pending, processing, completed, failed
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'programs_count': self.programs_count,
            'processing_status': self.processing_status,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class ChatMessage(db.Model):
    """Model for storing chat messages"""
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False, index=True)
    message_type = db.Column(db.String(20), nullable=False)  # user, assistant, system
    content = db.Column(db.Text, nullable=False)
    query_type = db.Column(db.String(50))  # dependencies, explain, similar, general
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'message_type': self.message_type,
            'content': self.content,
            'query_type': self.query_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ProgramDependency(db.Model):
    """Model for storing program dependencies"""
    __tablename__ = 'program_dependencies'
    
    id = db.Column(db.Integer, primary_key=True)
    source_program_id = db.Column(db.String(100), nullable=False, index=True)
    target_program_id = db.Column(db.String(100), nullable=False, index=True)
    dependency_type = db.Column(db.String(50), nullable=False)  # CALL, COPY, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'source_program_id': self.source_program_id,
            'target_program_id': self.target_program_id,
            'dependency_type': self.dependency_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class SystemStats(db.Model):
    """Model for storing system statistics"""
    __tablename__ = 'system_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    total_programs = db.Column(db.Integer, default=0)
    total_lines_of_code = db.Column(db.Integer, default=0)
    complexity_breakdown = db.Column(db.JSON)  # {"Low": 10, "Medium": 5, "High": 2}
    dependency_count = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'total_programs': self.total_programs,
            'total_lines_of_code': self.total_lines_of_code,
            'complexity_breakdown': self.complexity_breakdown or {},
            'dependency_count': self.dependency_count,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }
