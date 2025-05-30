"""
Data ingestion service for COBOL files
"""
import logging
import os
import zipfile
from typing import List, Dict, Any

def run_ingestion_pipeline(files_path: str) -> bool:
    """
    Run the ingestion pipeline to process COBOL files
    
    Args:
        files_path: Path to directory containing COBOL files
        
    Returns:
        True if successful, False otherwise
    """
    try:
        from cobol_parser import extract_cobol_files
        from models import CobolProgram
        from app import db
        
        # Extract and parse COBOL files
        programs = extract_cobol_files(files_path)
        
        if not programs:
            logging.warning(f"No COBOL programs found in {files_path}")
            return False
        
        # Store programs in database
        stored_count = 0
        for program_data in programs:
            try:
                # Check if program already exists
                existing = CobolProgram.query.filter_by(
                    program_id=program_data.get('program_id'),
                    file_name=program_data.get('file_name')
                ).first()
                
                if existing:
                    logging.info(f"Program {program_data.get('program_id')} already exists, skipping")
                    continue
                
                # Create new program record
                program = CobolProgram(
                    program_id=program_data.get('program_id', 'UNKNOWN'),
                    file_name=program_data.get('file_name', ''),
                    file_path=program_data.get('file_path', ''),
                    source_code=program_data.get('source_code', ''),
                    ast_structure=program_data.get('ast_structure'),
                    procedures=program_data.get('procedures'),
                    working_storage=program_data.get('working_storage'),
                    file_section=program_data.get('file_section'),
                    dependencies=program_data.get('dependencies'),
                    copybooks=program_data.get('copybooks'),
                    complexity=program_data.get('complexity', 'Unknown'),
                    line_count=program_data.get('line_count', 0)
                )
                
                db.session.add(program)
                stored_count += 1
                
            except Exception as e:
                logging.error(f"Error storing program {program_data.get('program_id', 'unknown')}: {e}")
                continue
        
        if stored_count > 0:
            db.session.commit()
            logging.info(f"Successfully stored {stored_count} COBOL programs")
            return True
        else:
            logging.warning("No new programs were stored")
            return False
            
    except Exception as e:
        logging.error(f"Ingestion pipeline error: {e}")
        return False

def get_pipeline_status() -> Dict[str, Any]:
    """Get status of the last pipeline run"""
    from models import CobolProgram
    from app import db
    
    try:
        total_programs = CobolProgram.query.count()
        return {
            'status': 'ready',
            'total_programs': total_programs,
            'last_run': 'Available',
            'message': f'Database contains {total_programs} COBOL programs'
        }
    except Exception as e:
        return {
            'status': 'error',
            'total_programs': 0,
            'last_run': 'Error',
            'message': str(e)
        }