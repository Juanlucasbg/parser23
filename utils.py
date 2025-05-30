"""
Utility functions for COBOL analysis application
"""

import re
import logging
from typing import Dict, Any, List, Optional
from collections import defaultdict
from models import CobolProgram, SystemStats, db
from database_setup import get_all_programs

def classify_query(query: str) -> str:
    """Classify user query type based on keywords"""
    query_lower = query.lower()
    
    if any(keyword in query_lower for keyword in ['depend', 'call', 'link', 'reference']):
        return 'dependencies'
    elif any(keyword in query_lower for keyword in ['similar', 'like', 'find', 'search']):
        return 'similar'
    elif any(keyword in query_lower for keyword in ['explain', 'what', 'how', 'purpose', 'function']):
        return 'explain'
    else:
        return 'general'

def get_relevant_context(query: str, max_programs: int = 3) -> str:
    """Get relevant context from COBOL programs for LLM queries"""
    try:
        # Extract program names or keywords from query
        keywords = extract_keywords_from_query(query)
        
        if keywords:
            # Search for programs matching keywords
            programs = CobolProgram.query.filter(
                db.or_(
                    *[CobolProgram.program_id.contains(keyword.upper()) for keyword in keywords]
                )
            ).limit(max_programs).all()
        else:
            # Get recent programs as context
            programs = CobolProgram.query.order_by(CobolProgram.created_at.desc()).limit(max_programs).all()
        
        context_parts = []
        for program in programs:
            context = f"Program: {program.program_id}\n"
            context += f"Complexity: {program.complexity}\n"
            context += f"Lines: {program.line_count}\n"
            
            if program.dependencies:
                context += f"Dependencies: {', '.join(program.dependencies[:5])}\n"
            
            if program.procedures:
                procedures = [p.get('name', str(p)) if isinstance(p, dict) else str(p) 
                            for p in program.procedures[:5]]
                context += f"Procedures: {', '.join(procedures)}\n"
            
            context_parts.append(context)
        
        return "\n---\n".join(context_parts)
        
    except Exception as e:
        logging.error(f"Error getting context: {str(e)}")
        return "No relevant context found."

def extract_keywords_from_query(query: str) -> List[str]:
    """Extract potential program names or keywords from query"""
    # Look for COBOL program name patterns
    patterns = [
        r'\b([A-Z][A-Z0-9\-]{2,})\b',  # Program name pattern
        r'program\s+([A-Za-z0-9\-]+)',  # "program NAME"
        r'called?\s+([A-Za-z0-9\-]+)',  # "call/called NAME"
    ]
    
    keywords = set()
    for pattern in patterns:
        matches = re.findall(pattern, query, re.IGNORECASE)
        keywords.update(match.upper() if isinstance(match, str) else match[0].upper() 
                       for match in matches)
    
    # Filter out common COBOL keywords
    cobol_keywords = {
        'PROGRAM', 'DIVISION', 'SECTION', 'PROCEDURE', 'DATA', 'WORKING', 
        'STORAGE', 'FILE', 'IDENTIFICATION', 'ENVIRONMENT', 'CALL', 'PERFORM'
    }
    
    return [kw for kw in keywords if kw not in cobol_keywords]

def get_system_statistics() -> Dict[str, Any]:
    """Get basic system statistics"""
    try:
        total_programs = CobolProgram.query.count()
        
        if total_programs == 0:
            return {
                'total_programs': 0,
                'total_lines': 0,
                'avg_complexity': 'N/A',
                'total_dependencies': 0
            }
        
        # Calculate total lines
        total_lines = db.session.query(db.func.sum(CobolProgram.line_count)).scalar() or 0
        
        # Get complexity breakdown
        complexity_counts = db.session.query(
            CobolProgram.complexity, 
            db.func.count(CobolProgram.id)
        ).group_by(CobolProgram.complexity).all()
        
        complexity_breakdown = {comp: count for comp, count in complexity_counts}
        
        # Count dependencies
        total_deps = 0
        programs = CobolProgram.query.all()
        for program in programs:
            if program.dependencies:
                total_deps += len(program.dependencies)
        
        return {
            'total_programs': total_programs,
            'total_lines': total_lines,
            'complexity_breakdown': complexity_breakdown,
            'total_dependencies': total_deps,
            'avg_lines_per_program': round(total_lines / total_programs, 1) if total_programs > 0 else 0
        }
        
    except Exception as e:
        logging.error(f"Error getting statistics: {str(e)}")
        return {'total_programs': 0, 'total_lines': 0, 'total_dependencies': 0}

def get_detailed_statistics() -> Dict[str, Any]:
    """Get detailed analytics for dashboard"""
    try:
        basic_stats = get_system_statistics()
        
        # Get programs by complexity
        programs = CobolProgram.query.all()
        
        # Analyze complexity distribution
        complexity_data = defaultdict(list)
        for program in programs:
            complexity_data[program.complexity or 'Unknown'].append({
                'program_id': program.program_id,
                'line_count': program.line_count or 0,
                'dependency_count': len(program.dependencies) if program.dependencies else 0
            })
        
        # Recent activity
        recent_programs = CobolProgram.query.order_by(
            CobolProgram.created_at.desc()
        ).limit(10).all()
        
        return {
            **basic_stats,
            'complexity_distribution': dict(complexity_data),
            'recent_programs': [p.to_dict() for p in recent_programs],
            'top_complex_programs': get_most_complex_programs(5),
            'most_dependencies': get_programs_with_most_dependencies(5)
        }
        
    except Exception as e:
        logging.error(f"Error getting detailed statistics: {str(e)}")
        return get_system_statistics()

def get_complexity_breakdown() -> Dict[str, Any]:
    """Get complexity breakdown for charts"""
    try:
        complexity_counts = db.session.query(
            CobolProgram.complexity,
            db.func.count(CobolProgram.id),
            db.func.avg(CobolProgram.line_count)
        ).group_by(CobolProgram.complexity).all()
        
        breakdown = {}
        for complexity, count, avg_lines in complexity_counts:
            breakdown[complexity or 'Unknown'] = {
                'count': count,
                'avg_lines': round(float(avg_lines or 0), 1)
            }
        
        return breakdown
        
    except Exception as e:
        logging.error(f"Error getting complexity breakdown: {str(e)}")
        return {}

def get_dependency_network() -> Dict[str, Any]:
    """Build dependency network for visualization"""
    try:
        programs = CobolProgram.query.all()
        
        nodes = []
        edges = []
        
        # Create nodes
        for program in programs:
            nodes.append({
                'id': program.program_id,
                'label': program.program_id,
                'complexity': program.complexity or 'Unknown',
                'lines': program.line_count or 0,
                'group': get_complexity_group(program.complexity)
            })
        
        # Create edges
        for program in programs:
            if program.dependencies:
                for dep in program.dependencies:
                    edges.append({
                        'from': program.program_id,
                        'to': dep,
                        'label': 'calls'
                    })
        
        return {
            'nodes': nodes,
            'edges': edges
        }
        
    except Exception as e:
        logging.error(f"Error building dependency network: {str(e)}")
        return {'nodes': [], 'edges': []}

def get_complexity_group(complexity: str) -> int:
    """Get numeric group for complexity visualization"""
    complexity_map = {
        'Low': 1,
        'Medium': 2,
        'High': 3,
        'Unknown': 0
    }
    return complexity_map.get(complexity, 0)

def get_most_complex_programs(limit: int = 5) -> List[Dict[str, Any]]:
    """Get programs with highest complexity"""
    try:
        # Order by complexity and line count
        programs = CobolProgram.query.filter(
            CobolProgram.complexity == 'High'
        ).order_by(
            CobolProgram.line_count.desc()
        ).limit(limit).all()
        
        if len(programs) < limit:
            # Add medium complexity programs
            medium_programs = CobolProgram.query.filter(
                CobolProgram.complexity == 'Medium'
            ).order_by(
                CobolProgram.line_count.desc()
            ).limit(limit - len(programs)).all()
            programs.extend(medium_programs)
        
        return [p.to_dict() for p in programs]
        
    except Exception as e:
        logging.error(f"Error getting complex programs: {str(e)}")
        return []

def get_programs_with_most_dependencies(limit: int = 5) -> List[Dict[str, Any]]:
    """Get programs with most dependencies"""
    try:
        programs = CobolProgram.query.all()
        
        # Sort by dependency count
        programs_with_deps = []
        for program in programs:
            dep_count = len(program.dependencies) if program.dependencies else 0
            if dep_count > 0:
                prog_dict = program.to_dict()
                prog_dict['dependency_count'] = dep_count
                programs_with_deps.append(prog_dict)
        
        # Sort by dependency count
        programs_with_deps.sort(key=lambda x: x['dependency_count'], reverse=True)
        
        return programs_with_deps[:limit]
        
    except Exception as e:
        logging.error(f"Error getting programs with dependencies: {str(e)}")
        return []

def build_dependency_graph(programs: List) -> Dict[str, Any]:
    """Build dependency graph structure"""
    try:
        graph = {
            'nodes': {},
            'edges': [],
            'stats': {
                'total_nodes': 0,
                'total_edges': 0,
                'cyclic_dependencies': 0
            }
        }
        
        # Build nodes
        for program in programs:
            program_dict = program.to_dict() if hasattr(program, 'to_dict') else program
            program_id = program_dict.get('program_id', 'Unknown')
            
            graph['nodes'][program_id] = {
                'id': program_id,
                'label': program_id,
                'complexity': program_dict.get('complexity', 'Unknown'),
                'lines': program_dict.get('line_count', 0),
                'dependencies': program_dict.get('dependencies', [])
            }
        
        # Build edges
        for program in programs:
            program_dict = program.to_dict() if hasattr(program, 'to_dict') else program
            source = program_dict.get('program_id', 'Unknown')
            dependencies = program_dict.get('dependencies', [])
            
            for dep in dependencies:
                graph['edges'].append({
                    'source': source,
                    'target': dep,
                    'type': 'dependency'
                })
        
        graph['stats']['total_nodes'] = len(graph['nodes'])
        graph['stats']['total_edges'] = len(graph['edges'])
        
        return graph
        
    except Exception as e:
        logging.error(f"Error building dependency graph: {str(e)}")
        return {'nodes': {}, 'edges': [], 'stats': {}}

def update_system_statistics():
    """Update system statistics in database"""
    try:
        stats = get_system_statistics()
        
        # Get or create system stats record
        sys_stats = SystemStats.query.first()
        if not sys_stats:
            sys_stats = SystemStats()
            db.session.add(sys_stats)
        
        # Update values
        sys_stats.total_programs = stats['total_programs']
        sys_stats.total_lines_of_code = stats['total_lines']
        sys_stats.complexity_breakdown = stats.get('complexity_breakdown', {})
        sys_stats.dependency_count = stats['total_dependencies']
        
        db.session.commit()
        logging.info("System statistics updated successfully")
        
    except Exception as e:
        logging.error(f"Error updating system statistics: {str(e)}")
        db.session.rollback()
