"""
COBOL Parser for extracting program structure and creating AST
"""

import os
import re
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

def extract_cobol_files(directory_path: str) -> List[Dict[str, Any]]:
    """
    Extract and parse all COBOL files from a directory.
    
    Args:
        directory_path: Path to directory containing COBOL files
        
    Returns:
        List of parsed COBOL program data
    """
    cobol_files = []
    
    try:
        # COBOL file extensions
        cobol_extensions = {'.cob', '.cbl', '.cobol', '.cpy', '.txt'}
        
        # Walk through directory
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = Path(file).suffix.lower()
                
                if file_ext in cobol_extensions:
                    try:
                        parsed_data = parse_cobol_file(file_path)
                        if parsed_data:
                            cobol_files.append(parsed_data)
                    except Exception as e:
                        logging.error(f"Error parsing {file_path}: {str(e)}")
                        continue
        
        logging.info(f"Successfully extracted {len(cobol_files)} COBOL files")
        return cobol_files
        
    except Exception as e:
        logging.error(f"Error extracting COBOL files: {str(e)}")
        return []

def parse_cobol_file(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Parse a single COBOL file and extract structure.
    
    Args:
        file_path: Path to COBOL file
        
    Returns:
        Dictionary containing parsed program data
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            source_code = f.read()
        
        # Parse the COBOL source
        ast_data = parse_cobol_to_ast(source_code, file_path)
        
        return ast_data
        
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {str(e)}")
        return None

def parse_cobol_to_ast(source_code: str, file_path: str = "") -> Dict[str, Any]:
    """
    Parse COBOL source code and create an Abstract Syntax Tree representation.
    
    Args:
        source_code: Raw COBOL source code
        file_path: Path to the source file
        
    Returns:
        Dictionary containing AST and metadata
    """
    try:
        # Clean and normalize source code
        lines = source_code.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove line numbers (columns 1-6) if present
            if len(line) > 6 and line[:6].isdigit():
                line = line[6:]
            # Remove sequence area (columns 73-80) if present
            if len(line) > 72:
                line = line[:72]
            cleaned_lines.append(line.rstrip())
        
        cleaned_source = '\n'.join(cleaned_lines)
        
        # Extract program structure
        program_id = extract_program_id(cleaned_source)
        divisions = extract_divisions(cleaned_source)
        procedures = extract_procedures(cleaned_source)
        working_storage = extract_working_storage(cleaned_source)
        file_section = extract_file_section(cleaned_source)
        dependencies = extract_dependencies(cleaned_source)
        copybooks = extract_copybooks(cleaned_source)
        
        # Calculate complexity
        complexity = estimate_complexity(cleaned_source, procedures)
        
        # Build AST structure
        ast_structure = {
            "program_id": program_id,
            "file_name": os.path.basename(file_path) if file_path else "unknown",
            "file_path": file_path,
            "divisions": divisions,
            "procedures": procedures,
            "working_storage": working_storage,
            "file_section": file_section,
            "dependencies": dependencies,
            "copybooks": copybooks,
            "line_count": len(lines),
            "metadata": {
                "has_file_section": bool(file_section),
                "has_working_storage": bool(working_storage),
                "procedure_count": len(procedures),
                "dependency_count": len(dependencies),
                "estimated_complexity": complexity
            }
        }
        
        return ast_structure
        
    except Exception as e:
        logging.error(f"Error parsing COBOL AST: {str(e)}")
        return {
            "program_id": "PARSE_ERROR",
            "file_name": os.path.basename(file_path) if file_path else "unknown",
            "file_path": file_path,
            "error": str(e),
            "line_count": len(source_code.split('\n')) if source_code else 0,
            "divisions": [],
            "procedures": [],
            "working_storage": [],
            "file_section": [],
            "dependencies": [],
            "copybooks": [],
            "metadata": {"estimated_complexity": "Unknown"}
        }

def extract_program_id(source: str) -> str:
    """Extract PROGRAM-ID from COBOL source"""
    try:
        # Look for PROGRAM-ID pattern
        pattern = r'PROGRAM-ID\.\s*([A-Za-z0-9\-]+)'
        match = re.search(pattern, source, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        # Alternative pattern
        pattern = r'PROGRAM-ID\s+([A-Za-z0-9\-]+)'
        match = re.search(pattern, source, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        return "UNKNOWN"
        
    except Exception as e:
        logging.error(f"Error extracting program ID: {str(e)}")
        return "UNKNOWN"

def extract_divisions(source: str) -> List[Dict[str, Any]]:
    """Extract division structure from COBOL source"""
    divisions = []
    
    try:
        # Common COBOL divisions
        division_patterns = [
            r'IDENTIFICATION\s+DIVISION',
            r'ENVIRONMENT\s+DIVISION',
            r'DATA\s+DIVISION',
            r'PROCEDURE\s+DIVISION'
        ]
        
        for pattern in division_patterns:
            matches = re.finditer(pattern, source, re.IGNORECASE)
            for match in matches:
                div_name = match.group(0).replace('DIVISION', '').strip()
                divisions.append({
                    "name": div_name,
                    "start_line": source[:match.start()].count('\n') + 1,
                    "content": match.group(0)
                })
        
        return divisions
        
    except Exception as e:
        logging.error(f"Error extracting divisions: {str(e)}")
        return []

def extract_procedures(source: str) -> List[Dict[str, Any]]:
    """Extract procedure/paragraph definitions"""
    procedures = []
    
    try:
        # Look for paragraph names (labels followed by period)
        lines = source.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('*'):
                continue
            
            # Look for paragraph labels (alphanumeric followed by period)
            if re.match(r'^[A-Za-z][A-Za-z0-9\-]*\.$', line):
                paragraph_name = line.rstrip('.')
                procedures.append({
                    "name": paragraph_name,
                    "type": "paragraph",
                    "line_number": i + 1,
                    "content": line
                })
            
            # Look for PERFORM statements
            elif 'PERFORM' in line.upper():
                perform_match = re.search(r'PERFORM\s+([A-Za-z][A-Za-z0-9\-]*)', line, re.IGNORECASE)
                if perform_match:
                    called_proc = perform_match.group(1)
                    procedures.append({
                        "name": called_proc,
                        "type": "called_procedure",
                        "line_number": i + 1,
                        "content": line.strip()
                    })
        
        return procedures
        
    except Exception as e:
        logging.error(f"Error extracting procedures: {str(e)}")
        return []

def extract_working_storage(source: str) -> List[Dict[str, Any]]:
    """Extract working storage section variables"""
    variables = []
    
    try:
        # Find WORKING-STORAGE SECTION
        ws_pattern = r'WORKING-STORAGE\s+SECTION\.(.*?)(?=\n\s*[A-Z\-]+\s+SECTION\.|\nPROCEDURE\s+DIVISION|$)'
        ws_match = re.search(ws_pattern, source, re.IGNORECASE | re.DOTALL)
        
        if ws_match:
            ws_content = ws_match.group(1)
            lines = ws_content.split('\n')
            
            for i, line in enumerate(lines):
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('*'):
                    continue
                
                # Look for variable definitions (level numbers)
                level_match = re.match(r'^(\d{2})\s+([A-Za-z][A-Za-z0-9\-]*)', line)
                if level_match:
                    level = level_match.group(1)
                    var_name = level_match.group(2)
                    
                    variables.append({
                        "level": int(level),
                        "name": var_name,
                        "definition": line,
                        "line_number": i + 1
                    })
        
        return variables
        
    except Exception as e:
        logging.error(f"Error extracting working storage: {str(e)}")
        return []

def extract_file_section(source: str) -> List[Dict[str, Any]]:
    """Extract file section definitions"""
    files = []
    
    try:
        # Find FILE SECTION
        fs_pattern = r'FILE\s+SECTION\.(.*?)(?=\n\s*[A-Z\-]+\s+SECTION\.|\nWORKING-STORAGE|$)'
        fs_match = re.search(fs_pattern, source, re.IGNORECASE | re.DOTALL)
        
        if fs_match:
            fs_content = fs_match.group(1)
            
            # Look for FD (File Description) entries
            fd_pattern = r'FD\s+([A-Za-z][A-Za-z0-9\-]*)'
            fd_matches = re.finditer(fd_pattern, fs_content, re.IGNORECASE)
            
            for match in fd_matches:
                file_name = match.group(1)
                files.append({
                    "name": file_name,
                    "type": "file_description",
                    "definition": match.group(0)
                })
        
        return files
        
    except Exception as e:
        logging.error(f"Error extracting file section: {str(e)}")
        return []

def extract_dependencies(source: str) -> List[str]:
    """Extract program dependencies (CALL statements)"""
    dependencies = set()
    
    try:
        # Look for CALL statements
        call_pattern = r'CALL\s+[\'"]([A-Za-z0-9\-]+)[\'"]'
        call_matches = re.finditer(call_pattern, source, re.IGNORECASE)
        
        for match in call_matches:
            called_program = match.group(1)
            dependencies.add(called_program)
        
        # Look for CALL with variables
        call_var_pattern = r'CALL\s+([A-Za-z][A-Za-z0-9\-]*)'
        call_var_matches = re.finditer(call_var_pattern, source, re.IGNORECASE)
        
        for match in call_var_matches:
            called_var = match.group(1)
            if not called_var.startswith('"') and not called_var.startswith("'"):
                dependencies.add(f"DYNAMIC:{called_var}")
        
        return list(dependencies)
        
    except Exception as e:
        logging.error(f"Error extracting dependencies: {str(e)}")
        return []

def extract_copybooks(source: str) -> List[str]:
    """Extract copybook dependencies (COPY statements)"""
    copybooks = set()
    
    try:
        # Look for COPY statements
        copy_pattern = r'COPY\s+([A-Za-z0-9\-]+)'
        copy_matches = re.finditer(copy_pattern, source, re.IGNORECASE)
        
        for match in copy_matches:
            copybook = match.group(1)
            copybooks.add(copybook)
        
        return list(copybooks)
        
    except Exception as e:
        logging.error(f"Error extracting copybooks: {str(e)}")
        return []

def estimate_complexity(source: str, procedures: List[Dict[str, Any]]) -> str:
    """Estimate program complexity based on various metrics"""
    try:
        lines = source.split('\n')
        non_empty_lines = [line for line in lines if line.strip() and not line.strip().startswith('*')]
        
        # Count various complexity indicators
        line_count = len(non_empty_lines)
        procedure_count = len(procedures)
        
        # Count conditional statements
        if_count = len(re.findall(r'\bIF\b', source, re.IGNORECASE))
        perform_count = len(re.findall(r'\bPERFORM\b', source, re.IGNORECASE))
        call_count = len(re.findall(r'\bCALL\b', source, re.IGNORECASE))
        
        # Calculate complexity score
        complexity_score = (
            line_count * 0.1 +
            procedure_count * 2 +
            if_count * 1.5 +
            perform_count * 1 +
            call_count * 2
        )
        
        # Classify complexity
        if complexity_score < 50:
            return "Low"
        elif complexity_score < 150:
            return "Medium"
        else:
            return "High"
            
    except Exception as e:
        logging.error(f"Error estimating complexity: {str(e)}")
        return "Unknown"
