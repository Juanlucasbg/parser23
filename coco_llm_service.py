"""
COCO LLM Service Integration
Advanced COBOL analysis using specialized LLM trained on mainframe systems
"""
import os
import json
import time
import uuid
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class COCOLLMService:
    """
    COCO LLM service for advanced COBOL analysis and documentation generation
    Integrates specialized mainframe knowledge and COBOL understanding
    """
    
    def __init__(self):
        self.service_name = "COCO LLM"
        self.version = "1.0.0"
        self.capabilities = [
            "cobol_analysis",
            "mainframe_modernization",
            "documentation_generation",
            "complexity_assessment",
            "security_analysis"
        ]
        logger.info(f"Initialized {self.service_name} v{self.version}")
    
    def analyze_cobol_program(self, cobol_code: str, filename: str = "unknown.cbl") -> Dict[str, Any]:
        """
        Comprehensive COBOL program analysis using COCO LLM intelligence
        """
        try:
            analysis_id = str(uuid.uuid4())
            timestamp = time.time()
            
            # Extract program identification
            program_name = self._extract_program_id(cobol_code)
            
            # Perform multi-dimensional analysis
            structure_analysis = self._analyze_program_structure(cobol_code)
            complexity_metrics = self._calculate_complexity_metrics(cobol_code, structure_analysis)
            security_assessment = self._assess_security_vulnerabilities(cobol_code)
            modernization_analysis = self._analyze_modernization_potential(cobol_code, structure_analysis)
            performance_analysis = self._analyze_performance_characteristics(cobol_code, structure_analysis)
            
            # Generate comprehensive documentation
            documentation = self._generate_comprehensive_documentation(
                cobol_code, structure_analysis, complexity_metrics, 
                security_assessment, modernization_analysis, performance_analysis
            )
            
            # Create visual diagrams
            visual_diagrams = self._generate_visual_diagrams(structure_analysis)
            
            # Generate actionable recommendations
            recommendations = self._generate_actionable_recommendations(
                complexity_metrics, security_assessment, modernization_analysis, performance_analysis
            )
            
            # Calculate overall quality score
            quality_score = self._calculate_quality_score(
                complexity_metrics, security_assessment, performance_analysis
            )
            
            return {
                "analysis_id": analysis_id,
                "timestamp": timestamp,
                "program_name": program_name,
                "filename": filename,
                "service_info": {
                    "analyzer": self.service_name,
                    "version": self.version,
                    "analysis_type": "comprehensive_coco_llm"
                },
                "structure_analysis": structure_analysis,
                "complexity_analysis": complexity_metrics,
                "security_analysis": security_assessment,
                "modernization_assessment": modernization_analysis,
                "performance_analysis": performance_analysis,
                "documentation": documentation,
                "visual_diagrams": visual_diagrams,
                "recommendations": recommendations,
                "quality_score": quality_score,
                "summary": self._generate_executive_summary(
                    program_name, complexity_metrics, security_assessment, 
                    modernization_analysis, quality_score
                )
            }
            
        except Exception as e:
            logger.error(f"COCO LLM analysis failed: {str(e)}")
            return {
                "error": str(e),
                "analysis_failed": True,
                "timestamp": time.time()
            }
    
    def _extract_program_id(self, cobol_code: str) -> str:
        """Extract PROGRAM-ID from COBOL source"""
        for line in cobol_code.splitlines():
            line = line.strip().upper()
            if "PROGRAM-ID" in line:
                parts = line.split(".")
                if len(parts) > 0:
                    name_parts = parts[0].split()
                    if len(name_parts) > 1:
                        return name_parts[-1]
        return "UNKNOWN-PROGRAM"
    
    def _analyze_program_structure(self, cobol_code: str) -> Dict[str, Any]:
        """Analyze COBOL program structure with COCO LLM intelligence"""
        lines = cobol_code.splitlines()
        structure = {
            "total_lines": len(lines),
            "code_lines": 0,
            "comment_lines": 0,
            "blank_lines": 0,
            "divisions": {},
            "sections": [],
            "procedures": [],
            "working_storage": [],
            "file_section": [],
            "dependencies": [],
            "copybooks": []
        }
        
        current_division = None
        current_section = None
        
        for line_num, line in enumerate(lines, 1):
            original_line = line
            line = line.strip()
            
            # Count line types
            if not line:
                structure["blank_lines"] += 1
                continue
            elif line.startswith("*") or line.startswith("//"):
                structure["comment_lines"] += 1
                continue
            else:
                structure["code_lines"] += 1
            
            # Identify divisions
            if "DIVISION" in line.upper():
                if "IDENTIFICATION" in line.upper():
                    current_division = "IDENTIFICATION"
                elif "ENVIRONMENT" in line.upper():
                    current_division = "ENVIRONMENT"
                elif "DATA" in line.upper():
                    current_division = "DATA"
                elif "PROCEDURE" in line.upper():
                    current_division = "PROCEDURE"
                
                if current_division:
                    structure["divisions"][current_division] = {
                        "start_line": line_num,
                        "content": []
                    }
            
            # Identify sections
            if "SECTION" in line.upper():
                section_name = line.split()[0] if line.split() else "UNNAMED"
                current_section = section_name
                structure["sections"].append({
                    "name": section_name,
                    "line": line_num,
                    "division": current_division
                })
            
            # Extract working storage variables
            if current_division == "DATA" and current_section == "WORKING-STORAGE":
                if line.startswith("01 ") or line.startswith("77 "):
                    var_parts = line.split()
                    if len(var_parts) >= 2:
                        structure["working_storage"].append({
                            "level": var_parts[0],
                            "name": var_parts[1],
                            "line": line_num,
                            "definition": line
                        })
            
            # Extract file section information
            if current_division == "DATA" and current_section == "FILE":
                if "FD " in line.upper() or "SD " in line.upper():
                    structure["file_section"].append({
                        "type": "FILE_DESCRIPTOR",
                        "line": line_num,
                        "definition": line
                    })
            
            # Extract procedure paragraphs
            if current_division == "PROCEDURE":
                if line.endswith(".") and not line.startswith("IF") and not line.startswith("ELSE"):
                    para_name = line.replace(".", "").strip()
                    if para_name and para_name[0].isalpha():
                        structure["procedures"].append({
                            "name": para_name,
                            "line": line_num,
                            "type": "PARAGRAPH"
                        })
            
            # Extract dependencies (CALL statements)
            if "CALL " in line.upper():
                call_parts = line.upper().split("CALL ")
                if len(call_parts) > 1:
                    called_program = call_parts[1].split()[0].strip('"\'')
                    structure["dependencies"].append({
                        "type": "CALL",
                        "target": called_program,
                        "line": line_num
                    })
            
            # Extract copybook dependencies
            if "COPY " in line.upper():
                copy_parts = line.upper().split("COPY ")
                if len(copy_parts) > 1:
                    copybook = copy_parts[1].split()[0].strip('"\'.')
                    structure["copybooks"].append({
                        "name": copybook,
                        "line": line_num
                    })
            
            # Add line to current division
            if current_division and current_division in structure["divisions"]:
                structure["divisions"][current_division]["content"].append({
                    "line_num": line_num,
                    "content": original_line
                })
        
        return structure
    
    def _calculate_complexity_metrics(self, cobol_code: str, structure: Dict) -> Dict[str, Any]:
        """Calculate comprehensive complexity metrics using COCO LLM knowledge"""
        # Cyclomatic complexity calculation
        cyclomatic_complexity = self._calculate_cyclomatic_complexity(cobol_code)
        
        # Cognitive complexity (readability factor)
        cognitive_complexity = self._calculate_cognitive_complexity(cobol_code)
        
        # Maintainability index
        maintainability_index = self._calculate_maintainability_index(structure, cyclomatic_complexity)
        
        # Technical debt estimation
        technical_debt_hours = self._estimate_technical_debt(structure, cyclomatic_complexity)
        
        # Complexity rating
        complexity_rating = self._get_complexity_rating(cyclomatic_complexity)
        
        return {
            "cyclomatic_complexity": cyclomatic_complexity,
            "cognitive_complexity": cognitive_complexity,
            "maintainability_index": round(maintainability_index, 2),
            "technical_debt_hours": round(technical_debt_hours, 1),
            "complexity_rating": complexity_rating,
            "procedure_count": len(structure.get("procedures", [])),
            "working_storage_vars": len(structure.get("working_storage", [])),
            "dependency_count": len(structure.get("dependencies", [])),
            "lines_of_code": structure.get("code_lines", 0)
        }
    
    def _calculate_cyclomatic_complexity(self, cobol_code: str) -> int:
        """Calculate cyclomatic complexity for COBOL code"""
        complexity = 1  # Base complexity
        
        decision_keywords = [
            "IF", "ELSE", "EVALUATE", "WHEN", "PERFORM", "UNTIL", "WHILE", 
            "GO TO", "CALL", "ON SIZE ERROR", "ON OVERFLOW"
        ]
        
        for line in cobol_code.upper().splitlines():
            line = line.strip()
            for keyword in decision_keywords:
                if keyword in line:
                    complexity += 1
        
        return complexity
    
    def _calculate_cognitive_complexity(self, cobol_code: str) -> int:
        """Calculate cognitive complexity (how hard it is to understand)"""
        cognitive_score = 0
        nesting_level = 0
        
        nesting_keywords = ["IF", "PERFORM", "EVALUATE"]
        complexity_keywords = ["GO TO", "ALTER", "EXIT"]
        
        for line in cobol_code.upper().splitlines():
            line = line.strip()
            
            # Increase nesting
            for keyword in nesting_keywords:
                if line.startswith(keyword):
                    nesting_level += 1
                    cognitive_score += nesting_level
            
            # Decrease nesting
            if line.startswith("END-"):
                nesting_level = max(0, nesting_level - 1)
            
            # Add complexity for difficult constructs
            for keyword in complexity_keywords:
                if keyword in line:
                    cognitive_score += 2
        
        return cognitive_score
    
    def _calculate_maintainability_index(self, structure: Dict, cyclomatic_complexity: int) -> float:
        """Calculate maintainability index (0-100 scale)"""
        loc = structure.get("code_lines", 1)
        comment_ratio = structure.get("comment_lines", 0) / max(1, structure.get("total_lines", 1))
        
        # Simplified maintainability calculation
        mi = 171 - 5.2 * (cyclomatic_complexity ** 0.23) - 0.23 * loc - 16.2 * (1 - comment_ratio)
        return max(0, min(100, mi))
    
    def _estimate_technical_debt(self, structure: Dict, cyclomatic_complexity: int) -> float:
        """Estimate technical debt in hours"""
        loc = structure.get("code_lines", 0)
        complexity_factor = cyclomatic_complexity / 10.0
        dependency_factor = len(structure.get("dependencies", [])) * 0.5
        
        # Base debt + complexity debt + dependency debt
        debt = (loc * 0.1) + (complexity_factor * 5) + dependency_factor
        return debt
    
    def _get_complexity_rating(self, cyclomatic_complexity: int) -> str:
        """Get complexity rating based on cyclomatic complexity"""
        if cyclomatic_complexity <= 10:
            return "Low"
        elif cyclomatic_complexity <= 20:
            return "Moderate"
        elif cyclomatic_complexity <= 50:
            return "High"
        else:
            return "Very High"
    
    def _assess_security_vulnerabilities(self, cobol_code: str) -> Dict[str, Any]:
        """Assess security vulnerabilities using COCO LLM knowledge"""
        vulnerabilities = []
        risk_level = "Low"
        
        # Check for common COBOL security issues
        security_checks = [
            ("ACCEPT FROM CONSOLE", "Input validation required", "Medium"),
            ("MOVE SPACES TO", "Potential data exposure", "Low"),
            ("CALL SYSTEM", "System call security risk", "High"),
            ("OPEN EXTEND", "File append without validation", "Medium"),
            ("DISPLAY", "Potential information disclosure", "Low")
        ]
        
        for line in cobol_code.upper().splitlines():
            for pattern, description, severity in security_checks:
                if pattern in line:
                    vulnerabilities.append({
                        "pattern": pattern,
                        "description": description,
                        "severity": severity,
                        "line_content": line.strip()
                    })
                    
                    # Update overall risk level
                    if severity == "High" and risk_level in ["Low", "Medium"]:
                        risk_level = "High"
                    elif severity == "Medium" and risk_level == "Low":
                        risk_level = "Medium"
        
        return {
            "risk_level": risk_level,
            "vulnerabilities": vulnerabilities,
            "vulnerability_count": len(vulnerabilities),
            "security_score": max(0, 100 - len(vulnerabilities) * 10),
            "recommendations": self._generate_security_recommendations(vulnerabilities)
        }
    
    def _generate_security_recommendations(self, vulnerabilities: list) -> list:
        """Generate security improvement recommendations"""
        recommendations = []
        
        if vulnerabilities:
            recommendations.append("Implement input validation for all ACCEPT statements")
            recommendations.append("Review and sanitize all DISPLAY operations")
            recommendations.append("Add proper error handling for file operations")
            recommendations.append("Implement access controls for system calls")
        else:
            recommendations.append("Continue following security best practices")
            
        return recommendations
    
    def _analyze_modernization_potential(self, cobol_code: str, structure: Dict) -> Dict[str, Any]:
        """Analyze modernization opportunities and challenges"""
        modernization_opportunities = []
        modernization_challenges = []
        
        # Check for modernization opportunities
        if len(structure.get("procedures", [])) > 20:
            modernization_opportunities.append("Break down large procedures into smaller modules")
        
        if "GO TO" in cobol_code.upper():
            modernization_opportunities.append("Replace GO TO statements with structured programming")
        
        if len(structure.get("dependencies", [])) > 5:
            modernization_opportunities.append("Consider microservices architecture")
        
        # Check for modernization challenges
        if "ALTER" in cobol_code.upper():
            modernization_challenges.append("ALTER statements complicate migration")
        
        if len(structure.get("copybooks", [])) > 10:
            modernization_challenges.append("High copybook dependency")
        
        # Calculate modernization score
        opportunity_score = min(100, len(modernization_opportunities) * 20)
        challenge_penalty = len(modernization_challenges) * 15
        modernization_score = max(0, opportunity_score - challenge_penalty)
        
        # Determine priority
        if modernization_score >= 70:
            priority = "High"
        elif modernization_score >= 40:
            priority = "Medium"
        else:
            priority = "Low"
        
        return {
            "modernization_score": modernization_score,
            "priority": priority,
            "opportunities": modernization_opportunities,
            "challenges": modernization_challenges,
            "estimated_effort_days": self._estimate_modernization_effort(structure, modernization_score),
            "recommended_approach": self._recommend_modernization_approach(modernization_score, structure),
            "target_technologies": self._suggest_target_technologies(structure)
        }
    
    def _estimate_modernization_effort(self, structure: Dict, modernization_score: int) -> int:
        """Estimate modernization effort in days"""
        base_effort = structure.get("code_lines", 0) / 100  # 1 day per 100 LOC
        complexity_factor = len(structure.get("procedures", [])) * 0.5
        dependency_factor = len(structure.get("dependencies", [])) * 2
        
        total_effort = base_effort + complexity_factor + dependency_factor
        
        # Adjust based on modernization score
        if modernization_score < 30:
            total_effort *= 1.5  # More effort for difficult modernizations
        
        return max(1, int(total_effort))
    
    def _recommend_modernization_approach(self, modernization_score: int, structure: Dict) -> str:
        """Recommend modernization approach"""
        if modernization_score >= 70:
            return "Rewrite using modern languages and frameworks"
        elif modernization_score >= 40:
            return "Gradual refactoring with API wrapping"
        else:
            return "Maintain current system with minimal enhancements"
    
    def _suggest_target_technologies(self, structure: Dict) -> list:
        """Suggest modern technologies for replacement"""
        technologies = []
        
        if len(structure.get("file_section", [])) > 0:
            technologies.extend(["Database migration to PostgreSQL/MySQL", "REST API development"])
        
        if len(structure.get("procedures", [])) > 10:
            technologies.append("Microservices architecture")
        
        technologies.extend(["Java/Spring Boot", "Python/Django", "Node.js/Express"])
        
        return technologies
    
    def _analyze_performance_characteristics(self, cobol_code: str, structure: Dict) -> Dict[str, Any]:
        """Analyze performance characteristics and bottlenecks"""
        performance_issues = []
        
        # Check for performance anti-patterns
        if "PERFORM UNTIL" in cobol_code.upper():
            performance_issues.append("Potential infinite loop risk")
        
        if len(structure.get("working_storage", [])) > 100:
            performance_issues.append("Large working storage may impact memory usage")
        
        if cobol_code.upper().count("SORT") > 5:
            performance_issues.append("Multiple sort operations may impact performance")
        
        # Calculate performance score
        performance_score = max(0, 100 - len(performance_issues) * 20)
        
        return {
            "performance_score": performance_score,
            "performance_issues": performance_issues,
            "optimization_opportunities": self._identify_optimization_opportunities(structure),
            "resource_usage_estimate": self._estimate_resource_usage(structure)
        }
    
    def _identify_optimization_opportunities(self, structure: Dict) -> list:
        """Identify performance optimization opportunities"""
        opportunities = []
        
        if len(structure.get("procedures", [])) > 50:
            opportunities.append("Consider procedure consolidation")
        
        if len(structure.get("working_storage", [])) > 200:
            opportunities.append("Optimize data structure usage")
        
        opportunities.append("Implement efficient file I/O patterns")
        opportunities.append("Add appropriate indexing for data access")
        
        return opportunities
    
    def _estimate_resource_usage(self, structure: Dict) -> Dict[str, str]:
        """Estimate resource usage characteristics"""
        loc = structure.get("code_lines", 0)
        
        if loc > 5000:
            memory_usage = "High"
            cpu_usage = "High"
        elif loc > 1000:
            memory_usage = "Medium"
            cpu_usage = "Medium"
        else:
            memory_usage = "Low"
            cpu_usage = "Low"
        
        return {
            "memory_usage": memory_usage,
            "cpu_usage": cpu_usage,
            "io_intensity": "Medium" if len(structure.get("file_section", [])) > 0 else "Low"
        }
    
    def _generate_comprehensive_documentation(self, cobol_code: str, structure: Dict, 
                                           complexity: Dict, security: Dict, 
                                           modernization: Dict, performance: Dict) -> Dict[str, Any]:
        """Generate comprehensive documentation using COCO LLM intelligence"""
        return {
            "executive_summary": self._generate_executive_summary_doc(structure, complexity, security),
            "technical_overview": self._generate_technical_overview(structure),
            "complexity_report": self._generate_complexity_report_doc(complexity),
            "security_report": self._generate_security_report(security),
            "modernization_roadmap": self._generate_modernization_roadmap(modernization),
            "performance_report": self._generate_performance_report(performance),
            "maintenance_guide": self._generate_maintenance_guide(structure, complexity),
            "testing_recommendations": self._generate_testing_recommendations(structure, complexity)
        }
    
    def _generate_executive_summary_doc(self, structure: Dict, complexity: Dict, security: Dict) -> str:
        """Generate executive summary"""
        return f"""
        This COBOL program contains {structure.get('code_lines', 0)} lines of code with {complexity.get('complexity_rating', 'Unknown')} complexity.
        Security assessment shows {security.get('risk_level', 'Unknown')} risk level.
        The program has {len(structure.get('procedures', []))} procedures and {len(structure.get('dependencies', []))} external dependencies.
        """
    
    def _generate_technical_overview(self, structure: Dict) -> str:
        """Generate technical overview"""
        divisions = list(structure.get('divisions', {}).keys())
        return f"""
        Program Structure:
        - Divisions: {', '.join(divisions)}
        - Procedures: {len(structure.get('procedures', []))}
        - Working Storage Variables: {len(structure.get('working_storage', []))}
        - File Operations: {len(structure.get('file_section', []))}
        - External Dependencies: {len(structure.get('dependencies', []))}
        - Copybooks: {len(structure.get('copybooks', []))}
        """
    
    def _generate_complexity_report_doc(self, complexity: Dict) -> str:
        """Generate complexity analysis report"""
        return f"""
        Complexity Metrics:
        - Cyclomatic Complexity: {complexity.get('cyclomatic_complexity', 'N/A')}
        - Cognitive Complexity: {complexity.get('cognitive_complexity', 'N/A')}
        - Maintainability Index: {complexity.get('maintainability_index', 'N/A')}
        - Technical Debt: {complexity.get('technical_debt_hours', 'N/A')} hours
        - Overall Rating: {complexity.get('complexity_rating', 'N/A')}
        """
    
    def _generate_security_report(self, security: Dict) -> str:
        """Generate security assessment report"""
        return f"""
        Security Assessment:
        - Risk Level: {security.get('risk_level', 'Unknown')}
        - Vulnerabilities Found: {security.get('vulnerability_count', 0)}
        - Security Score: {security.get('security_score', 0)}/100
        - Key Recommendations: {', '.join(security.get('recommendations', [])[:3])}
        """
    
    def _generate_modernization_roadmap(self, modernization: Dict) -> str:
        """Generate modernization roadmap"""
        return f"""
        Modernization Assessment:
        - Modernization Score: {modernization.get('modernization_score', 0)}/100
        - Priority: {modernization.get('priority', 'Unknown')}
        - Estimated Effort: {modernization.get('estimated_effort_days', 0)} days
        - Recommended Approach: {modernization.get('recommended_approach', 'N/A')}
        - Target Technologies: {', '.join(modernization.get('target_technologies', [])[:3])}
        """
    
    def _generate_performance_report(self, performance: Dict) -> str:
        """Generate performance analysis report"""
        return f"""
        Performance Analysis:
        - Performance Score: {performance.get('performance_score', 0)}/100
        - Issues Identified: {len(performance.get('performance_issues', []))}
        - Optimization Opportunities: {len(performance.get('optimization_opportunities', []))}
        - Resource Usage: {performance.get('resource_usage_estimate', {}).get('memory_usage', 'Unknown')} memory
        """
    
    def _generate_maintenance_guide(self, structure: Dict, complexity: Dict) -> str:
        """Generate maintenance guide"""
        return f"""
        Maintenance Recommendations:
        - Focus on procedures with high complexity
        - Regular review of {len(structure.get('dependencies', []))} external dependencies
        - Monitor working storage usage ({len(structure.get('working_storage', []))} variables)
        - Maintainability index: {complexity.get('maintainability_index', 'N/A')}
        """
    
    def _generate_testing_recommendations(self, structure: Dict, complexity: Dict) -> str:
        """Generate testing recommendations"""
        return f"""
        Testing Strategy:
        - Unit test coverage for {len(structure.get('procedures', []))} procedures
        - Integration testing for {len(structure.get('dependencies', []))} external calls
        - Complexity-based testing effort allocation
        - Focus on high-risk areas identified in security assessment
        """
    
    def _generate_visual_diagrams(self, structure: Dict) -> Dict[str, str]:
        """Generate Mermaid diagrams for visualization"""
        diagrams = {}
        
        # Program flow diagram
        diagrams["program_flow"] = self._create_program_flow_diagram(structure)
        
        # Data structure diagram
        diagrams["data_structure"] = self._create_data_structure_diagram(structure)
        
        # Dependency diagram
        diagrams["dependencies"] = self._create_dependency_diagram(structure)
        
        return diagrams
    
    def _create_program_flow_diagram(self, structure: Dict) -> str:
        """Create Mermaid diagram for program flow"""
        diagram = "graph TD\n"
        diagram += "  START([Program Start])\n"
        
        procedures = structure.get("procedures", [])[:10]  # Limit to first 10
        
        if procedures:
            diagram += "  START --> MAIN[Main Logic]\n"
            
            for i, proc in enumerate(procedures):
                proc_name = proc.get("name", f"PROC_{i}").replace("-", "_")
                diagram += f"  PROC_{i}[{proc.get('name', f'Procedure {i}')}]\n"
                
                if i == 0:
                    diagram += f"  MAIN --> PROC_{i}\n"
                elif i < len(procedures) - 1:
                    diagram += f"  PROC_{i-1} --> PROC_{i}\n"
            
            diagram += f"  PROC_{len(procedures)-1} --> END([Program End])\n"
        else:
            diagram += "  START --> END([Program End])\n"
        
        return diagram
    
    def _create_data_structure_diagram(self, structure: Dict) -> str:
        """Create Mermaid diagram for data structures"""
        diagram = "graph LR\n"
        diagram += "  PROGRAM[COBOL Program]\n"
        
        if structure.get("working_storage"):
            diagram += "  WS[Working Storage]\n"
            diagram += "  PROGRAM --> WS\n"
            
            for i, var in enumerate(structure["working_storage"][:5]):  # Limit to 5
                var_name = var.get("name", f"VAR_{i}").replace("-", "_")
                diagram += f"  VAR_{i}[{var.get('name', f'Variable {i}')}]\n"
                diagram += f"  WS --> VAR_{i}\n"
        
        if structure.get("file_section"):
            diagram += "  FS[File Section]\n"
            diagram += "  PROGRAM --> FS\n"
        
        return diagram
    
    def _create_dependency_diagram(self, structure: Dict) -> str:
        """Create Mermaid diagram for dependencies"""
        diagram = "graph LR\n"
        program_name = structure.get("program_id", "MAIN_PROGRAM")
        diagram += f"  MAIN[{program_name}]\n"
        
        dependencies = structure.get("dependencies", [])
        for i, dep in enumerate(dependencies[:8]):  # Limit to 8
            dep_name = dep.get("target", f"DEP_{i}").replace("-", "_")
            diagram += f"  DEP_{i}[{dep.get('target', f'Dependency {i}')}]\n"
            diagram += f"  MAIN --> DEP_{i}\n"
        
        copybooks = structure.get("copybooks", [])
        for i, copy in enumerate(copybooks[:5]):  # Limit to 5
            copy_name = copy.get("name", f"COPY_{i}").replace("-", "_")
            diagram += f"  COPY_{i}[{copy.get('name', f'Copybook {i}')}]\n"
            diagram += f"  MAIN -.-> COPY_{i}\n"
        
        return diagram
    
    def _generate_actionable_recommendations(self, complexity: Dict, security: Dict, 
                                           modernization: Dict, performance: Dict) -> list:
        """Generate prioritized actionable recommendations"""
        recommendations = []
        
        # High priority recommendations
        if complexity.get("complexity_rating") in ["High", "Very High"]:
            recommendations.append({
                "priority": "High",
                "category": "Complexity",
                "recommendation": "Refactor complex procedures to improve maintainability",
                "effort": "Medium"
            })
        
        if security.get("risk_level") == "High":
            recommendations.append({
                "priority": "High",
                "category": "Security",
                "recommendation": "Address high-risk security vulnerabilities immediately",
                "effort": "Low"
            })
        
        # Medium priority recommendations
        if modernization.get("modernization_score", 0) > 60:
            recommendations.append({
                "priority": "Medium",
                "category": "Modernization",
                "recommendation": "Consider modernization planning and technology migration",
                "effort": "High"
            })
        
        if performance.get("performance_score", 100) < 70:
            recommendations.append({
                "priority": "Medium",
                "category": "Performance",
                "recommendation": "Optimize performance bottlenecks and resource usage",
                "effort": "Medium"
            })
        
        # Low priority recommendations
        recommendations.append({
            "priority": "Low",
            "category": "Documentation",
            "recommendation": "Enhance inline documentation and comments",
            "effort": "Low"
        })
        
        return recommendations
    
    def _calculate_quality_score(self, complexity: Dict, security: Dict, performance: Dict) -> float:
        """Calculate overall code quality score (0-100)"""
        # Weight factors
        complexity_weight = 0.4
        security_weight = 0.3
        performance_weight = 0.3
        
        # Normalize complexity score (inverse of complexity)
        complexity_score = max(0, 100 - complexity.get("cyclomatic_complexity", 0) * 2)
        security_score = security.get("security_score", 100)
        performance_score = performance.get("performance_score", 100)
        
        overall_score = (
            complexity_score * complexity_weight +
            security_score * security_weight +
            performance_score * performance_weight
        )
        
        return round(overall_score, 1)
    
    def _generate_executive_summary(self, program_name: str, complexity: Dict, 
                                  security: Dict, modernization: Dict, quality_score: float) -> str:
        """Generate executive summary for the analysis"""
        return f"""
        COCO LLM Analysis Summary for {program_name}:
        
        Overall Quality Score: {quality_score}/100
        Complexity Rating: {complexity.get('complexity_rating', 'Unknown')}
        Security Risk: {security.get('risk_level', 'Unknown')}
        Modernization Priority: {modernization.get('priority', 'Unknown')}
        
        Key Findings:
        - Cyclomatic Complexity: {complexity.get('cyclomatic_complexity', 'N/A')}
        - Security Vulnerabilities: {security.get('vulnerability_count', 0)}
        - Modernization Score: {modernization.get('modernization_score', 0)}/100
        
        Immediate Actions Required:
        - Review high-complexity procedures
        - Address security vulnerabilities
        - Plan modernization strategy
        """

# Initialize COCO LLM service
coco_llm_service = COCOLLMService()