"""
Analytics service for COBOL analysis platform
"""
import logging
from typing import Dict, Any, List
from collections import Counter

def generate_codebase_overview():
    """Generate comprehensive codebase overview"""
    from models import CobolProgram
    from app import db
    
    try:
        programs = CobolProgram.query.all()
        
        if not programs:
            return {
                'total_programs': 0,
                'total_lines': 0,
                'complexity_breakdown': {'Low': 0, 'Medium': 0, 'High': 0},
                'most_common_dependencies': [],
                'status': 'empty'
            }
        
        total_lines = sum(p.line_count or 0 for p in programs)
        complexity_counts = Counter(p.complexity for p in programs if p.complexity)
        
        # Get most common dependencies
        all_deps = []
        for p in programs:
            if p.dependencies:
                if isinstance(p.dependencies, list):
                    all_deps.extend(p.dependencies)
                elif isinstance(p.dependencies, str):
                    all_deps.append(p.dependencies)
        
        common_deps = Counter(all_deps).most_common(5)
        
        return {
            'total_programs': len(programs),
            'total_lines': total_lines,
            'complexity_breakdown': {
                'Low': complexity_counts.get('Low', 0),
                'Medium': complexity_counts.get('Medium', 0),
                'High': complexity_counts.get('High', 0)
            },
            'most_common_dependencies': [{'name': dep, 'count': count} for dep, count in common_deps],
            'status': 'success'
        }
    except Exception as e:
        logging.error(f"Analytics error: {e}")
        return {
            'total_programs': 0,
            'total_lines': 0,
            'complexity_breakdown': {'Low': 0, 'Medium': 0, 'High': 0},
            'most_common_dependencies': [],
            'status': 'error',
            'error': str(e)
        }

def analyze_program_relationships():
    """Analyze relationships between programs"""
    from models import CobolProgram
    from app import db
    
    try:
        programs = CobolProgram.query.all()
        
        relationships = []
        for program in programs:
            if program.dependencies:
                deps = program.dependencies if isinstance(program.dependencies, list) else [program.dependencies]
                for dep in deps:
                    relationships.append({
                        'source': program.program_id,
                        'target': dep,
                        'type': 'CALL'
                    })
        
        return {
            'relationships': relationships,
            'total_relationships': len(relationships),
            'status': 'success'
        }
    except Exception as e:
        logging.error(f"Relationship analysis error: {e}")
        return {
            'relationships': [],
            'total_relationships': 0,
            'status': 'error',
            'error': str(e)
        }

def generate_analytics_report():
    """Generate comprehensive analytics report"""
    overview = generate_codebase_overview()
    relationships = analyze_program_relationships()
    
    return {
        'overview': overview,
        'relationships': relationships,
        'generated_at': 'now',
        'status': 'success' if overview['status'] == 'success' and relationships['status'] == 'success' else 'partial'
    }