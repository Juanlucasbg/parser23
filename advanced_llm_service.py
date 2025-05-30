"""
Advanced LLM Service with job processing and documentation generation
Integrated from COBOL Intelligence Agent features
"""
import os
import json
import uuid
import time
import requests
from typing import Dict, Any, Optional
from datetime import datetime
import logging

class AdvancedLLMService:
    """Enhanced LLM service with job processing and documentation generation"""
    
    def __init__(self):
        self.upload_folder = 'uploads'
        self.jobs = {}  # In production, this would be a database
        
    def create_analysis_job(self, cobol_code: str, filename: str, user_id: str = None) -> str:
        """Create a new analysis job for COBOL code"""
        job_id = str(uuid.uuid4())
        
        job_data = {
            "job_id": job_id,
            "filename": filename,
            "status": "queued",
            "created_at": time.time(),
            "user_id": user_id,
            "progress": 0,
            "stages": [
                "parsing",
                "structure_analysis", 
                "dependency_mapping",
                "complexity_analysis",
                "documentation_generation"
            ],
            "current_stage": "parsing",
            "results": {}
        }
        
        # Store job metadata
        self.jobs[job_id] = job_data
        job_file = os.path.join(self.upload_folder, f"{job_id}.json")
        with open(job_file, 'w') as f:
            json.dump(job_data, f, indent=2)
            
        # Start processing
        self._process_cobol_job(job_id, cobol_code)
        
        return job_id
    
    def _process_cobol_job(self, job_id: str, cobol_code: str):
        """Process COBOL code analysis job"""
        try:
            job_data = self.jobs[job_id]
            
            # Stage 1: Parsing
            job_data["current_stage"] = "parsing"
            job_data["progress"] = 20
            self._update_job(job_id, job_data)
            
            from cobol_parser import parse_cobol_to_ast
            ast_result = parse_cobol_to_ast(cobol_code)
            job_data["results"]["ast"] = ast_result
            
            # Stage 2: Structure Analysis
            job_data["current_stage"] = "structure_analysis"
            job_data["progress"] = 40
            self._update_job(job_id, job_data)
            
            structure_analysis = self._analyze_structure(ast_result)
            job_data["results"]["structure"] = structure_analysis
            
            # Stage 3: Dependency Mapping
            job_data["current_stage"] = "dependency_mapping"
            job_data["progress"] = 60
            self._update_job(job_id, job_data)
            
            dependencies = self._map_dependencies(ast_result)
            job_data["results"]["dependencies"] = dependencies
            
            # Stage 4: Complexity Analysis
            job_data["current_stage"] = "complexity_analysis"
            job_data["progress"] = 80
            self._update_job(job_id, job_data)
            
            complexity = self._analyze_complexity(ast_result, cobol_code)
            job_data["results"]["complexity"] = complexity
            
            # Stage 5: Documentation Generation
            job_data["current_stage"] = "documentation_generation"
            job_data["progress"] = 90
            self._update_job(job_id, job_data)
            
            documentation = self._generate_documentation(job_data["results"])
            job_data["results"]["documentation"] = documentation
            
            # Complete
            job_data["status"] = "completed"
            job_data["progress"] = 100
            job_data["completed_at"] = time.time()
            self._update_job(job_id, job_data)
            
        except Exception as e:
            logging.error(f"Job {job_id} failed: {str(e)}")
            job_data["status"] = "failed"
            job_data["error"] = str(e)
            self._update_job(job_id, job_data)
    
    def _analyze_structure(self, ast_result: Dict) -> Dict:
        """Analyze COBOL program structure"""
        return {
            "program_id": ast_result.get("program_id", "UNKNOWN"),
            "divisions": ast_result.get("divisions", []),
            "procedures": ast_result.get("procedures", []),
            "data_items": ast_result.get("working_storage", []),
            "file_definitions": ast_result.get("file_section", []),
            "paragraph_count": len(ast_result.get("procedures", [])),
            "data_item_count": len(ast_result.get("working_storage", [])),
        }
    
    def _map_dependencies(self, ast_result: Dict) -> Dict:
        """Map program dependencies"""
        return {
            "internal_calls": ast_result.get("dependencies", []),
            "copybooks": ast_result.get("copybooks", []),
            "external_programs": [],
            "database_access": [],
            "file_operations": []
        }
    
    def _analyze_complexity(self, ast_result: Dict, source_code: str) -> Dict:
        """Analyze code complexity"""
        lines = source_code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        return {
            "total_lines": len(lines),
            "code_lines": len(non_empty_lines),
            "comment_lines": len([line for line in lines if line.strip().startswith('*')]),
            "complexity_rating": ast_result.get("complexity", "Medium"),
            "cyclomatic_complexity": self._calculate_cyclomatic_complexity(source_code),
            "maintainability_score": self._calculate_maintainability_score(ast_result)
        }
    
    def _calculate_cyclomatic_complexity(self, source_code: str) -> int:
        """Calculate cyclomatic complexity"""
        decision_points = 0
        lines = source_code.upper().split('\n')
        
        for line in lines:
            line = line.strip()
            if any(keyword in line for keyword in ['IF', 'PERFORM', 'EVALUATE', 'WHEN']):
                decision_points += 1
        
        return decision_points + 1  # Base complexity
    
    def _calculate_maintainability_score(self, ast_result: Dict) -> int:
        """Calculate maintainability score (0-100)"""
        score = 100
        
        # Deduct points for complexity
        complexity = ast_result.get("complexity", "Medium")
        if complexity == "High":
            score -= 30
        elif complexity == "Medium":
            score -= 15
        
        # Deduct points for excessive procedures
        procedure_count = len(ast_result.get("procedures", []))
        if procedure_count > 20:
            score -= 20
        elif procedure_count > 10:
            score -= 10
        
        return max(0, score)
    
    def _generate_documentation(self, analysis_results: Dict) -> Dict:
        """Generate comprehensive documentation"""
        documentation = {
            "generated_at": datetime.now().isoformat(),
            "summary": self._generate_summary(analysis_results),
            "structure_overview": self._generate_structure_overview(analysis_results),
            "complexity_report": self._generate_complexity_report(analysis_results),
            "dependency_report": self._generate_dependency_report(analysis_results),
            "recommendations": self._generate_recommendations(analysis_results)
        }
        
        return documentation
    
    def _generate_summary(self, results: Dict) -> str:
        """Generate program summary"""
        structure = results.get("structure", {})
        complexity = results.get("complexity", {})
        
        return f"""
Program Overview:
- Program ID: {structure.get('program_id', 'Unknown')}
- Total Lines: {complexity.get('total_lines', 0)}
- Procedures: {structure.get('paragraph_count', 0)}
- Complexity: {complexity.get('complexity_rating', 'Unknown')}
- Maintainability Score: {complexity.get('maintainability_score', 0)}/100
        """.strip()
    
    def _generate_structure_overview(self, results: Dict) -> Dict:
        """Generate structure overview"""
        structure = results.get("structure", {})
        return {
            "divisions_found": len(structure.get("divisions", [])),
            "procedures_count": structure.get("paragraph_count", 0),
            "data_items_count": structure.get("data_item_count", 0),
            "file_definitions": len(structure.get("file_definitions", []))
        }
    
    def _generate_complexity_report(self, results: Dict) -> Dict:
        """Generate complexity analysis report"""
        complexity = results.get("complexity", {})
        return {
            "overall_rating": complexity.get("complexity_rating", "Unknown"),
            "cyclomatic_complexity": complexity.get("cyclomatic_complexity", 0),
            "maintainability_score": complexity.get("maintainability_score", 0),
            "code_coverage": {
                "total_lines": complexity.get("total_lines", 0),
                "code_lines": complexity.get("code_lines", 0),
                "comment_lines": complexity.get("comment_lines", 0)
            }
        }
    
    def _generate_dependency_report(self, results: Dict) -> Dict:
        """Generate dependency analysis report"""
        dependencies = results.get("dependencies", {})
        return {
            "internal_calls": dependencies.get("internal_calls", []),
            "copybooks": dependencies.get("copybooks", []),
            "external_dependencies": dependencies.get("external_programs", []),
            "total_dependencies": len(dependencies.get("internal_calls", []) + dependencies.get("copybooks", []))
        }
    
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        complexity = results.get("complexity", {})
        structure = results.get("structure", {})
        
        # Complexity recommendations
        if complexity.get("maintainability_score", 100) < 70:
            recommendations.append("Consider refactoring to improve maintainability score")
        
        if complexity.get("cyclomatic_complexity", 0) > 10:
            recommendations.append("High cyclomatic complexity detected - consider breaking down complex procedures")
        
        # Structure recommendations
        if structure.get("paragraph_count", 0) > 20:
            recommendations.append("Consider modularizing the program - large number of procedures detected")
        
        if len(structure.get("data_items", [])) > 50:
            recommendations.append("Consider reviewing data structure organization - large number of data items")
        
        if not recommendations:
            recommendations.append("Code structure looks good - no major issues detected")
        
        return recommendations
    
    def _update_job(self, job_id: str, job_data: Dict):
        """Update job data in storage"""
        self.jobs[job_id] = job_data
        job_file = os.path.join(self.upload_folder, f"{job_id}.json")
        with open(job_file, 'w') as f:
            json.dump(job_data, f, indent=2)
    
    def get_job_status(self, job_id: str) -> Optional[Dict]:
        """Get job status and results"""
        if job_id in self.jobs:
            return self.jobs[job_id]
        
        # Try loading from file
        job_file = os.path.join(self.upload_folder, f"{job_id}.json")
        if os.path.exists(job_file):
            with open(job_file, 'r') as f:
                job_data = json.load(f)
                self.jobs[job_id] = job_data
                return job_data
        
        return None
    
    def list_jobs(self, user_id: str = None) -> List[Dict]:
        """List all jobs for a user"""
        jobs = []
        for filename in os.listdir(self.upload_folder):
            if filename.endswith('.json') and not filename.startswith('_'):
                try:
                    with open(os.path.join(self.upload_folder, filename), 'r') as f:
                        job_data = json.load(f)
                        if user_id is None or job_data.get('user_id') == user_id:
                            jobs.append(job_data)
                except Exception as e:
                    logging.error(f"Error loading job file {filename}: {e}")
        
        return sorted(jobs, key=lambda x: x.get('created_at', 0), reverse=True)

# Global instance
advanced_llm_service = AdvancedLLMService()