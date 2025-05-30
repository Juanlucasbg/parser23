"""
Autonomous COBOL Analysis Agent
Enhanced agent system combining advanced AI capabilities with comprehensive COBOL analysis
"""
import os
import json
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import requests

# Initialize logger
logger = logging.getLogger(__name__)

class AutonomousCOBOLAgent:
    """
    Advanced autonomous agent for comprehensive COBOL analysis and documentation
    Combines the best features from both applications
    """
    
    def __init__(self, session_id=None, user_id=None):
        self.session_id = session_id or str(uuid.uuid4())
        self.user_id = user_id
        self.memory = []
        self.user_preferences = {}
        self.max_memory_items = 20
        
        # Enhanced capabilities tracking
        self.analysis_capabilities = {
            'structure_analysis': True,
            'dependency_mapping': True,
            'complexity_calculation': True,
            'security_analysis': True,
            'modernization_assessment': True,
            'documentation_generation': True,
            'diagram_creation': True,
            'performance_analysis': True
        }
        
        # LLM provider preferences
        self.llm_provider = self.get_user_preference("llm_provider", "groq")
        self.llm_model = self.get_user_preference("llm_model", "llama-3.3-70b-versatile")
        
        logger.info(f"Initialized Autonomous COBOL Agent with session {self.session_id}")
    
    def set_user_preference(self, key: str, value: Any):
        """Set user preference for analysis customization"""
        self.user_preferences[key] = value
        logger.debug(f"Set user preference: {key} = {value}")
    
    def get_user_preference(self, key: str, default: Any = None):
        """Get user preference with fallback to default"""
        return self.user_preferences.get(key, default)
    
    def remember(self, item_type: str, content: Any):
        """Add item to agent memory for context awareness"""
        memory_item = {
            "type": item_type,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": self.session_id
        }
        
        self.memory.append(memory_item)
        
        # Maintain memory limit
        if len(self.memory) > self.max_memory_items:
            self.memory.pop(0)
            
        logger.debug(f"Added memory item: {item_type}")
        return memory_item
    
    def analyze_cobol_comprehensive(self, cobol_code: str, filename: str = None) -> Dict[str, Any]:
        """
        Perform comprehensive COBOL analysis using autonomous decision-making
        """
        analysis_start = datetime.utcnow()
        
        try:
            # Stage 1: Initial Structure Analysis
            logger.info("Starting comprehensive COBOL analysis...")
            structure_analysis = self._analyze_program_structure(cobol_code)
            
            # Stage 2: Advanced Complexity Analysis
            complexity_analysis = self._analyze_complexity_advanced(cobol_code, structure_analysis)
            
            # Stage 3: Security and Quality Assessment
            security_analysis = self._analyze_security_aspects(cobol_code)
            
            # Stage 4: Modernization Assessment
            modernization_analysis = self._assess_modernization_potential(cobol_code, structure_analysis)
            
            # Stage 5: Performance Analysis
            performance_analysis = self._analyze_performance_characteristics(cobol_code, structure_analysis)
            
            # Stage 6: Documentation Generation
            documentation = self._generate_comprehensive_documentation(
                cobol_code, structure_analysis, complexity_analysis, 
                security_analysis, modernization_analysis, performance_analysis
            )
            
            # Stage 7: Visual Diagrams
            diagrams = self._generate_visual_diagrams(structure_analysis)
            
            # Compile comprehensive results
            analysis_result = {
                'analysis_id': str(uuid.uuid4()),
                'filename': filename,
                'timestamp': analysis_start.isoformat(),
                'processing_time': (datetime.utcnow() - analysis_start).total_seconds(),
                'structure_analysis': structure_analysis,
                'complexity_analysis': complexity_analysis,
                'security_analysis': security_analysis,
                'modernization_analysis': modernization_analysis,
                'performance_analysis': performance_analysis,
                'documentation': documentation,
                'diagrams': diagrams,
                'recommendations': self._generate_actionable_recommendations(
                    complexity_analysis, security_analysis, modernization_analysis
                ),
                'overall_score': self._calculate_overall_quality_score(
                    complexity_analysis, security_analysis, performance_analysis
                )
            }
            
            # Remember this analysis
            self.remember("comprehensive_analysis", {
                'analysis_id': analysis_result['analysis_id'],
                'filename': filename,
                'overall_score': analysis_result['overall_score']
            })
            
            logger.info(f"Comprehensive analysis completed in {analysis_result['processing_time']:.2f} seconds")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Comprehensive analysis failed: {str(e)}")
            return {
                'error': str(e),
                'status': 'failed',
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def _analyze_program_structure(self, cobol_code: str) -> Dict[str, Any]:
        """Enhanced program structure analysis"""
        from cobol_parser import parse_cobol_to_ast
        
        # Get basic structure
        ast_result = parse_cobol_to_ast(cobol_code)
        
        # Enhanced structure analysis
        lines = cobol_code.split('\n')
        
        structure = {
            'program_id': ast_result.get('program_id', 'UNKNOWN'),
            'total_lines': len(lines),
            'code_lines': len([line for line in lines if line.strip() and not line.strip().startswith('*')]),
            'comment_lines': len([line for line in lines if line.strip().startswith('*')]),
            'blank_lines': len([line for line in lines if not line.strip()]),
            'divisions': ast_result.get('divisions', []),
            'procedures': ast_result.get('procedures', []),
            'working_storage': ast_result.get('working_storage', []),
            'file_section': ast_result.get('file_section', []),
            'dependencies': ast_result.get('dependencies', []),
            'copybooks': ast_result.get('copybooks', []),
            'program_flow': self._analyze_program_flow(cobol_code),
            'data_structures': self._analyze_data_structures(ast_result.get('working_storage', [])),
            'io_operations': self._identify_io_operations(cobol_code)
        }
        
        return structure
    
    def _analyze_complexity_advanced(self, cobol_code: str, structure: Dict) -> Dict[str, Any]:
        """Advanced complexity analysis with multiple metrics"""
        
        # Cyclomatic complexity calculation
        cyclomatic_complexity = self._calculate_cyclomatic_complexity(cobol_code)
        
        # Cognitive complexity
        cognitive_complexity = self._calculate_cognitive_complexity(cobol_code)
        
        # Maintainability index
        maintainability_index = self._calculate_maintainability_index(
            structure, cyclomatic_complexity
        )
        
        # Technical debt estimation
        technical_debt = self._estimate_technical_debt(structure, cyclomatic_complexity)
        
        return {
            'cyclomatic_complexity': cyclomatic_complexity,
            'cognitive_complexity': cognitive_complexity,
            'maintainability_index': maintainability_index,
            'technical_debt_hours': technical_debt,
            'complexity_rating': self._get_complexity_rating(cyclomatic_complexity),
            'refactoring_priority': self._assess_refactoring_priority(
                cyclomatic_complexity, maintainability_index, technical_debt
            ),
            'code_metrics': {
                'procedures_count': len(structure.get('procedures', [])),
                'data_items_count': len(structure.get('working_storage', [])),
                'dependency_count': len(structure.get('dependencies', [])),
                'comment_ratio': structure.get('comment_lines', 0) / max(1, structure.get('total_lines', 1))
            }
        }
    
    def _analyze_security_aspects(self, cobol_code: str) -> Dict[str, Any]:
        """Analyze security vulnerabilities and concerns"""
        
        security_issues = []
        risk_level = "LOW"
        
        # Check for common security patterns
        code_upper = cobol_code.upper()
        
        # SQL injection risks
        if 'EXEC SQL' in code_upper and any(word in code_upper for word in ['ACCEPT', 'INPUT']):
            security_issues.append({
                'type': 'SQL_INJECTION_RISK',
                'severity': 'HIGH',
                'description': 'Potential SQL injection vulnerability detected'
            })
            risk_level = "HIGH"
        
        # Hardcoded credentials
        if any(pattern in code_upper for pattern in ['PASSWORD', 'USERID', 'USER-ID']):
            security_issues.append({
                'type': 'HARDCODED_CREDENTIALS',
                'severity': 'MEDIUM',
                'description': 'Potential hardcoded credentials found'
            })
            if risk_level == "LOW":
                risk_level = "MEDIUM"
        
        # Buffer overflow risks
        if 'OCCURS' in code_upper:
            security_issues.append({
                'type': 'BUFFER_OVERFLOW_RISK',
                'severity': 'MEDIUM',
                'description': 'Array operations detected - review bounds checking'
            })
        
        # File handling security
        if any(op in code_upper for op in ['OPEN', 'READ', 'WRITE']):
            security_issues.append({
                'type': 'FILE_SECURITY',
                'severity': 'LOW',
                'description': 'File operations detected - ensure proper access controls'
            })
        
        return {
            'overall_risk_level': risk_level,
            'security_issues': security_issues,
            'security_score': max(0, 100 - len(security_issues) * 15),
            'recommendations': self._generate_security_recommendations(security_issues)
        }
    
    def _assess_modernization_potential(self, cobol_code: str, structure: Dict) -> Dict[str, Any]:
        """Assess potential for modernization"""
        
        modernization_score = 100
        modernization_opportunities = []
        
        # Check for modern COBOL features
        code_upper = cobol_code.upper()
        
        if 'OBJECT-COMPUTER' not in code_upper:
            modernization_opportunities.append('Add OBJECT-COMPUTER section for better hardware optimization')
            modernization_score -= 10
        
        if 'FUNCTION' not in code_upper:
            modernization_opportunities.append('Consider using intrinsic functions for better maintainability')
            modernization_score -= 5
        
        if len(structure.get('procedures', [])) > 20:
            modernization_opportunities.append('Break down large program into smaller, modular components')
            modernization_score -= 15
        
        if 'EXEC SQL' in code_upper:
            modernization_opportunities.append('Consider modernizing database access patterns')
            modernization_score -= 5
        
        # Calculate modernization effort
        effort_estimate = self._estimate_modernization_effort(structure, len(modernization_opportunities))
        
        return {
            'modernization_score': max(0, modernization_score),
            'modernization_priority': self._get_modernization_priority(modernization_score),
            'opportunities': modernization_opportunities,
            'effort_estimate_days': effort_estimate,
            'recommended_approach': self._recommend_modernization_approach(modernization_score, structure),
            'technology_suggestions': self._suggest_modern_technologies(structure)
        }
    
    def _analyze_performance_characteristics(self, cobol_code: str, structure: Dict) -> Dict[str, Any]:
        """Analyze performance characteristics and bottlenecks"""
        
        performance_score = 100
        performance_issues = []
        
        # Check for performance anti-patterns
        code_upper = cobol_code.upper()
        
        if 'SORT' in code_upper:
            performance_issues.append('Sorting operations detected - ensure optimal sort algorithms')
            performance_score -= 10
        
        if code_upper.count('PERFORM') > 50:
            performance_issues.append('High number of PERFORM statements - consider optimization')
            performance_score -= 15
        
        if 'SEARCH ALL' in code_upper:
            performance_issues.append('Binary search operations - verify table optimization')
            performance_score -= 5
        
        # Estimate execution complexity
        execution_complexity = len(structure.get('procedures', [])) * 2 + len(structure.get('dependencies', [])) * 3
        
        return {
            'performance_score': max(0, performance_score),
            'execution_complexity': execution_complexity,
            'performance_issues': performance_issues,
            'optimization_opportunities': self._identify_optimization_opportunities(structure),
            'resource_usage_estimate': self._estimate_resource_usage(structure)
        }
    
    def _generate_comprehensive_documentation(self, cobol_code: str, structure: Dict, 
                                           complexity: Dict, security: Dict, 
                                           modernization: Dict, performance: Dict) -> Dict[str, Any]:
        """Generate comprehensive documentation using AI analysis"""
        
        # Create structured documentation
        documentation = {
            'executive_summary': self._generate_executive_summary(structure, complexity, security),
            'technical_overview': self._generate_technical_overview(structure),
            'complexity_report': self._generate_complexity_report(complexity),
            'security_assessment': self._generate_security_report(security),
            'modernization_roadmap': self._generate_modernization_roadmap(modernization),
            'performance_analysis': self._generate_performance_report(performance),
            'maintenance_guide': self._generate_maintenance_guide(structure, complexity),
            'testing_recommendations': self._generate_testing_recommendations(structure, complexity)
        }
        
        return documentation
    
    def _generate_visual_diagrams(self, structure: Dict) -> Dict[str, Any]:
        """Generate Mermaid diagrams for visualization"""
        
        diagrams = {}
        
        # Program flow diagram
        if structure.get('procedures'):
            diagrams['program_flow'] = self._create_program_flow_diagram(structure['procedures'])
        
        # Data structure diagram
        if structure.get('working_storage'):
            diagrams['data_structure'] = self._create_data_structure_diagram(structure['working_storage'])
        
        # Dependency diagram
        if structure.get('dependencies'):
            diagrams['dependencies'] = self._create_dependency_diagram(structure['dependencies'])
        
        return diagrams
    
    def _generate_actionable_recommendations(self, complexity: Dict, security: Dict, modernization: Dict) -> List[Dict[str, Any]]:
        """Generate prioritized actionable recommendations"""
        
        recommendations = []
        
        # Complexity recommendations
        if complexity.get('cyclomatic_complexity', 0) > 15:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'COMPLEXITY',
                'title': 'Reduce Cyclomatic Complexity',
                'description': 'Break down complex procedures into smaller, more manageable functions',
                'effort': 'MEDIUM',
                'impact': 'HIGH'
            })
        
        # Security recommendations
        if security.get('overall_risk_level') == 'HIGH':
            recommendations.append({
                'priority': 'CRITICAL',
                'category': 'SECURITY',
                'title': 'Address Security Vulnerabilities',
                'description': 'Review and remediate identified security issues',
                'effort': 'HIGH',
                'impact': 'CRITICAL'
            })
        
        # Modernization recommendations
        if modernization.get('modernization_score', 100) < 70:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'MODERNIZATION',
                'title': 'Modernization Opportunities',
                'description': 'Consider modernizing legacy patterns and technologies',
                'effort': 'HIGH',
                'impact': 'MEDIUM'
            })
        
        return sorted(recommendations, key=lambda x: {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}[x['priority']])
    
    def _calculate_overall_quality_score(self, complexity: Dict, security: Dict, performance: Dict) -> float:
        """Calculate overall code quality score"""
        
        complexity_score = max(0, 100 - complexity.get('cyclomatic_complexity', 0) * 5)
        security_score = security.get('security_score', 0)
        performance_score = performance.get('performance_score', 0)
        maintainability_score = complexity.get('maintainability_index', 0)
        
        # Weighted average
        overall_score = (
            complexity_score * 0.3 +
            security_score * 0.25 +
            performance_score * 0.25 +
            maintainability_score * 0.2
        )
        
        return round(overall_score, 2)
    
    # Helper methods for specific calculations
    def _calculate_cyclomatic_complexity(self, cobol_code: str) -> int:
        """Calculate cyclomatic complexity"""
        decision_points = 0
        lines = cobol_code.upper().split('\n')
        
        for line in lines:
            line = line.strip()
            decision_keywords = ['IF', 'PERFORM', 'EVALUATE', 'WHEN', 'GO TO', 'CALL']
            for keyword in decision_keywords:
                if keyword in line:
                    decision_points += 1
                    break
        
        return decision_points + 1
    
    def _calculate_cognitive_complexity(self, cobol_code: str) -> int:
        """Calculate cognitive complexity (how hard it is to understand)"""
        cognitive_score = 0
        nesting_level = 0
        lines = cobol_code.upper().split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Increase nesting
            if any(keyword in line for keyword in ['IF', 'PERFORM', 'EVALUATE']):
                nesting_level += 1
                cognitive_score += nesting_level
            
            # Decrease nesting
            if any(keyword in line for keyword in ['END-IF', 'END-PERFORM', 'END-EVALUATE']):
                nesting_level = max(0, nesting_level - 1)
        
        return cognitive_score
    
    def _calculate_maintainability_index(self, structure: Dict, cyclomatic_complexity: int) -> float:
        """Calculate maintainability index"""
        lines_of_code = structure.get('code_lines', 1)
        comment_ratio = structure.get('comment_lines', 0) / max(1, structure.get('total_lines', 1))
        
        # Simplified maintainability index calculation
        maintainability = max(0, 100 - cyclomatic_complexity * 2 - lines_of_code * 0.1 + comment_ratio * 20)
        
        return round(maintainability, 2)
    
    def _estimate_technical_debt(self, structure: Dict, cyclomatic_complexity: int) -> float:
        """Estimate technical debt in hours"""
        base_debt = cyclomatic_complexity * 0.5
        complexity_debt = len(structure.get('procedures', [])) * 0.2
        dependency_debt = len(structure.get('dependencies', [])) * 0.3
        
        return round(base_debt + complexity_debt + dependency_debt, 1)
    
    def _analyze_program_flow(self, cobol_code: str) -> Dict[str, Any]:
        """Analyze program execution flow"""
        code_upper = cobol_code.upper()
        
        return {
            'has_main_logic': 'PROCEDURE DIVISION' in code_upper,
            'has_error_handling': any(pattern in code_upper for pattern in ['ERROR', 'EXCEPTION', 'INVALID']),
            'has_file_operations': any(pattern in code_upper for pattern in ['OPEN', 'READ', 'WRITE', 'CLOSE']),
            'has_database_operations': 'EXEC SQL' in code_upper,
            'has_calculations': any(pattern in code_upper for pattern in ['COMPUTE', 'ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE']),
            'flow_complexity': 'COMPLEX' if code_upper.count('IF') > 10 else 'MODERATE' if code_upper.count('IF') > 5 else 'SIMPLE'
        }
    
    def _analyze_data_structures(self, working_storage: List) -> Dict[str, Any]:
        """Analyze data structure complexity"""
        return {
            'total_variables': len(working_storage),
            'complex_structures': len([item for item in working_storage if item.get('level', 0) < 77]),
            'elementary_items': len([item for item in working_storage if item.get('level', 0) == 77]),
            'data_complexity': 'HIGH' if len(working_storage) > 50 else 'MEDIUM' if len(working_storage) > 20 else 'LOW'
        }
    
    def _identify_io_operations(self, cobol_code: str) -> Dict[str, Any]:
        """Identify input/output operations"""
        code_upper = cobol_code.upper()
        
        return {
            'file_operations': code_upper.count('OPEN') + code_upper.count('READ') + code_upper.count('WRITE'),
            'screen_operations': code_upper.count('DISPLAY') + code_upper.count('ACCEPT'),
            'database_operations': code_upper.count('EXEC SQL'),
            'io_complexity': 'HIGH' if (code_upper.count('OPEN') + code_upper.count('EXEC SQL')) > 10 else 'MEDIUM' if (code_upper.count('OPEN') + code_upper.count('EXEC SQL')) > 5 else 'LOW'
        }
    
    # Documentation generation helpers
    def _generate_executive_summary(self, structure: Dict, complexity: Dict, security: Dict) -> str:
        """Generate executive summary"""
        program_id = structure.get('program_id', 'Unknown')
        lines = structure.get('total_lines', 0)
        complexity_rating = complexity.get('complexity_rating', 'Unknown')
        security_level = security.get('overall_risk_level', 'Unknown')
        
        return f"""
Program {program_id} Analysis Summary:
- Total Lines: {lines}
- Complexity: {complexity_rating}
- Security Risk: {security_level}
- Maintainability Score: {complexity.get('maintainability_index', 'N/A')}

This program requires {'immediate attention' if security_level == 'HIGH' or complexity.get('cyclomatic_complexity', 0) > 20 else 'routine maintenance'}.
        """.strip()
    
    def _generate_technical_overview(self, structure: Dict) -> str:
        """Generate technical overview"""
        return f"""
Technical Structure:
- Program ID: {structure.get('program_id', 'Unknown')}
- Divisions: {len(structure.get('divisions', []))}
- Procedures: {len(structure.get('procedures', []))}
- Data Items: {len(structure.get('working_storage', []))}
- Dependencies: {len(structure.get('dependencies', []))}
- Copybooks: {len(structure.get('copybooks', []))}

Program Flow: {structure.get('program_flow', {}).get('flow_complexity', 'Unknown')}
Data Complexity: {structure.get('data_structures', {}).get('data_complexity', 'Unknown')}
        """.strip()
    
    def _generate_complexity_report(self, complexity: Dict) -> str:
        """Generate complexity analysis report"""
        return f"""
Complexity Analysis:
- Cyclomatic Complexity: {complexity.get('cyclomatic_complexity', 'N/A')}
- Cognitive Complexity: {complexity.get('cognitive_complexity', 'N/A')}
- Maintainability Index: {complexity.get('maintainability_index', 'N/A')}
- Technical Debt: {complexity.get('technical_debt_hours', 'N/A')} hours
- Refactoring Priority: {complexity.get('refactoring_priority', 'N/A')}
        """.strip()
    
    def _create_program_flow_diagram(self, procedures: List) -> str:
        """Create Mermaid diagram for program flow"""
        if not procedures:
            return ""
        
        diagram = "graph TD\n"
        diagram += "    START[Program Start]\n"
        
        for i, proc in enumerate(procedures[:10]):  # Limit to 10 procedures
            proc_name = proc.get('name', f'PROC_{i}').replace('-', '_')
            diagram += f"    {proc_name}[{proc.get('name', f'Procedure {i}')}]\n"
            if i == 0:
                diagram += f"    START --> {proc_name}\n"
            elif i < len(procedures) - 1:
                next_proc = procedures[i + 1].get('name', f'PROC_{i+1}').replace('-', '_')
                diagram += f"    {proc_name} --> {next_proc}\n"
        
        diagram += "    END[Program End]\n"
        if procedures:
            last_proc = procedures[-1].get('name', 'FINAL').replace('-', '_')
            diagram += f"    {last_proc} --> END\n"
        
        return diagram
    
    def _create_data_structure_diagram(self, working_storage: List) -> str:
        """Create Mermaid diagram for data structures"""
        if not working_storage:
            return ""
        
        diagram = "graph LR\n"
        diagram += "    WS[Working Storage]\n"
        
        for i, item in enumerate(working_storage[:10]):  # Limit to 10 items
            item_name = item.get('name', f'ITEM_{i}').replace('-', '_')
            item_type = item.get('type', 'X')
            diagram += f"    {item_name}[{item.get('name', f'Item {i}')} - {item_type}]\n"
            diagram += f"    WS --> {item_name}\n"
        
        return diagram
    
    def _create_dependency_diagram(self, dependencies: List) -> str:
        """Create Mermaid diagram for dependencies"""
        if not dependencies:
            return ""
        
        diagram = "graph LR\n"
        diagram += "    MAIN[Main Program]\n"
        
        for i, dep in enumerate(dependencies[:10]):  # Limit to 10 dependencies
            dep_name = str(dep).replace('-', '_').replace(' ', '_')
            diagram += f"    DEP_{i}[{dep}]\n"
            diagram += f"    MAIN --> DEP_{i}\n"
        
        return diagram
    
    # Additional helper methods
    def _get_complexity_rating(self, cyclomatic_complexity: int) -> str:
        """Get complexity rating based on cyclomatic complexity"""
        if cyclomatic_complexity <= 5:
            return "LOW"
        elif cyclomatic_complexity <= 15:
            return "MEDIUM"
        else:
            return "HIGH"
    
    def _assess_refactoring_priority(self, cyclomatic_complexity: int, maintainability_index: float, technical_debt: float) -> str:
        """Assess refactoring priority"""
        if cyclomatic_complexity > 20 or maintainability_index < 30 or technical_debt > 40:
            return "CRITICAL"
        elif cyclomatic_complexity > 15 or maintainability_index < 50 or technical_debt > 20:
            return "HIGH"
        elif cyclomatic_complexity > 10 or maintainability_index < 70 or technical_debt > 10:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_security_recommendations(self, security_issues: List) -> List[str]:
        """Generate security recommendations based on issues found"""
        recommendations = []
        
        issue_types = [issue['type'] for issue in security_issues]
        
        if 'SQL_INJECTION_RISK' in issue_types:
            recommendations.append("Implement parameterized queries to prevent SQL injection")
        
        if 'HARDCODED_CREDENTIALS' in issue_types:
            recommendations.append("Move credentials to secure configuration files")
        
        if 'BUFFER_OVERFLOW_RISK' in issue_types:
            recommendations.append("Add bounds checking for array operations")
        
        if 'FILE_SECURITY' in issue_types:
            recommendations.append("Implement proper file access controls and validation")
        
        return recommendations
    
    def _estimate_modernization_effort(self, structure: Dict, opportunity_count: int) -> int:
        """Estimate modernization effort in days"""
        base_effort = opportunity_count * 2
        complexity_factor = len(structure.get('procedures', [])) * 0.1
        dependency_factor = len(structure.get('dependencies', [])) * 0.2
        
        return max(1, int(base_effort + complexity_factor + dependency_factor))
    
    def _get_modernization_priority(self, modernization_score: int) -> str:
        """Get modernization priority based on score"""
        if modernization_score < 40:
            return "CRITICAL"
        elif modernization_score < 60:
            return "HIGH"
        elif modernization_score < 80:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _recommend_modernization_approach(self, modernization_score: int, structure: Dict) -> str:
        """Recommend modernization approach"""
        if modernization_score < 40:
            return "Complete rewrite recommended - consider modern languages"
        elif modernization_score < 60:
            return "Significant refactoring - modernize in phases"
        elif modernization_score < 80:
            return "Incremental improvements - focus on critical areas"
        else:
            return "Maintenance mode - minor enhancements only"
    
    def _suggest_modern_technologies(self, structure: Dict) -> List[str]:
        """Suggest modern technologies for replacement"""
        suggestions = []
        
        if structure.get('program_flow', {}).get('has_database_operations'):
            suggestions.append("Consider REST APIs for database access")
        
        if structure.get('program_flow', {}).get('has_file_operations'):
            suggestions.append("Consider cloud storage solutions")
        
        if len(structure.get('procedures', [])) > 20:
            suggestions.append("Consider microservices architecture")
        
        suggestions.append("Consider containerization with Docker")
        suggestions.append("Consider CI/CD pipeline implementation")
        
        return suggestions
    
    def _identify_optimization_opportunities(self, structure: Dict) -> List[str]:
        """Identify performance optimization opportunities"""
        opportunities = []
        
        if len(structure.get('procedures', [])) > 15:
            opportunities.append("Consider procedure consolidation")
        
        if len(structure.get('dependencies', [])) > 10:
            opportunities.append("Review dependency management")
        
        if structure.get('data_structures', {}).get('total_variables', 0) > 50:
            opportunities.append("Optimize data structure usage")
        
        return opportunities
    
    def _estimate_resource_usage(self, structure: Dict) -> Dict[str, str]:
        """Estimate resource usage characteristics"""
        procedures_count = len(structure.get('procedures', []))
        data_items_count = len(structure.get('working_storage', []))
        
        memory_usage = "LOW"
        if data_items_count > 100:
            memory_usage = "HIGH"
        elif data_items_count > 50:
            memory_usage = "MEDIUM"
        
        cpu_usage = "LOW"
        if procedures_count > 30:
            cpu_usage = "HIGH"
        elif procedures_count > 15:
            cpu_usage = "MEDIUM"
        
        return {
            'memory_usage': memory_usage,
            'cpu_usage': cpu_usage,
            'io_intensity': structure.get('io_operations', {}).get('io_complexity', 'LOW')
        }
    
    def _generate_security_report(self, security: Dict) -> str:
        """Generate security assessment report"""
        risk_level = security.get('overall_risk_level', 'UNKNOWN')
        security_score = security.get('security_score', 0)
        issues = security.get('security_issues', [])
        
        report = f"Security Assessment:\n"
        report += f"- Overall Risk Level: {risk_level}\n"
        report += f"- Security Score: {security_score}/100\n"
        report += f"- Issues Found: {len(issues)}\n\n"
        
        if issues:
            report += "Security Issues:\n"
            for issue in issues:
                report += f"- {issue['type']}: {issue['description']} (Severity: {issue['severity']})\n"
        
        return report
    
    def _generate_modernization_roadmap(self, modernization: Dict) -> str:
        """Generate modernization roadmap"""
        score = modernization.get('modernization_score', 0)
        priority = modernization.get('modernization_priority', 'UNKNOWN')
        effort = modernization.get('effort_estimate_days', 0)
        
        roadmap = f"Modernization Roadmap:\n"
        roadmap += f"- Modernization Score: {score}/100\n"
        roadmap += f"- Priority: {priority}\n"
        roadmap += f"- Estimated Effort: {effort} days\n"
        roadmap += f"- Recommended Approach: {modernization.get('recommended_approach', 'Not specified')}\n\n"
        
        opportunities = modernization.get('opportunities', [])
        if opportunities:
            roadmap += "Modernization Opportunities:\n"
            for opp in opportunities:
                roadmap += f"- {opp}\n"
        
        return roadmap
    
    def _generate_performance_report(self, performance: Dict) -> str:
        """Generate performance analysis report"""
        score = performance.get('performance_score', 0)
        complexity = performance.get('execution_complexity', 0)
        issues = performance.get('performance_issues', [])
        
        report = f"Performance Analysis:\n"
        report += f"- Performance Score: {score}/100\n"
        report += f"- Execution Complexity: {complexity}\n"
        report += f"- Performance Issues: {len(issues)}\n\n"
        
        if issues:
            report += "Performance Issues:\n"
            for issue in issues:
                report += f"- {issue}\n"
        
        return report
    
    def _generate_maintenance_guide(self, structure: Dict, complexity: Dict) -> str:
        """Generate maintenance guide"""
        guide = "Maintenance Guide:\n\n"
        
        # Based on complexity
        if complexity.get('cyclomatic_complexity', 0) > 15:
            guide += "High Complexity Areas:\n"
            guide += "- Focus on reducing cyclomatic complexity\n"
            guide += "- Break down large procedures\n"
            guide += "- Add comprehensive unit tests\n\n"
        
        # Based on structure
        if len(structure.get('dependencies', [])) > 10:
            guide += "Dependency Management:\n"
            guide += "- Document all external dependencies\n"
            guide += "- Create dependency maps\n"
            guide += "- Monitor for version changes\n\n"
        
        guide += "Regular Maintenance Tasks:\n"
        guide += "- Review and update documentation\n"
        guide += "- Perform code quality checks\n"
        guide += "- Monitor performance metrics\n"
        guide += "- Update security assessments\n"
        
        return guide
    
    def _generate_testing_recommendations(self, structure: Dict, complexity: Dict) -> str:
        """Generate testing recommendations"""
        recommendations = "Testing Recommendations:\n\n"
        
        # Unit testing
        recommendations += "Unit Testing:\n"
        procedures_count = len(structure.get('procedures', []))
        recommendations += f"- Create {procedures_count} unit tests (one per procedure)\n"
        recommendations += "- Focus on edge cases and error conditions\n"
        recommendations += "- Test data validation routines\n\n"
        
        # Integration testing
        if len(structure.get('dependencies', [])) > 0:
            recommendations += "Integration Testing:\n"
            recommendations += "- Test all external dependencies\n"
            recommendations += "- Verify data flow between modules\n"
            recommendations += "- Test error handling across module boundaries\n\n"
        
        # Performance testing
        if complexity.get('cyclomatic_complexity', 0) > 10:
            recommendations += "Performance Testing:\n"
            recommendations += "- Load test critical procedures\n"
            recommendations += "- Monitor memory usage\n"
            recommendations += "- Test with production-size data\n\n"
        
        recommendations += "Test Coverage Target: 90% or higher\n"
        recommendations += "Automated Testing: Implement CI/CD pipeline\n"
        
        return recommendations

# Global autonomous agent instance
autonomous_cobol_agent = AutonomousCOBOLAgent()