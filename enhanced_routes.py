"""
Enhanced API endpoints for COBOL analysis platform
Clean integration of advanced features + COCO LLM integration
"""
import os
import json
import logging
import uuid
import time
from datetime import datetime
from flask import request, jsonify, render_template_string
from werkzeug.utils import secure_filename

from app import app, db
from models import CobolProgram

logger = logging.getLogger(__name__)

# Initialize enhanced services with error handling
autonomous_agent = None
data_converter = None
llm_service = None

try:
    from autonomous_cobol_agent import AutonomousCOBOLAgent
    autonomous_agent = AutonomousCOBOLAgent()
    logger.info("✅ Autonomous COBOL agent initialized")
except Exception as e:
    logger.warning(f"⚠️ Autonomous agent not available: {e}")

try:
    from cobol_data_converter import COBOLDataConverter
    data_converter = COBOLDataConverter()
    logger.info("✅ COBOL data converter initialized")
except Exception as e:
    logger.warning(f"⚠️ Data converter not available: {e}")

try:
    from advanced_llm_service import AdvancedLLMService
    llm_service = AdvancedLLMService()
    logger.info("✅ Advanced LLM service initialized")
except Exception as e:
    logger.warning(f"⚠️ LLM service not available: {e}")

@app.route('/api/enhanced-analysis', methods=['POST'])
def api_enhanced_analysis():
    """Enhanced COBOL analysis using autonomous agent"""
    if not autonomous_agent:
        return jsonify({
            'error': 'Enhanced analysis service not available',
            'message': 'Please check if API keys are configured properly'
        }), 503
    
    try:
        data = request.get_json()
        cobol_code = data.get('cobol_code')
        filename = data.get('filename', 'unknown.cbl')
        analysis_type = data.get('analysis_type', 'comprehensive')
        
        if not cobol_code:
            return jsonify({'error': 'COBOL code is required'}), 400
        
        # Set analysis preferences
        autonomous_agent.set_user_preference("analysis_type", analysis_type)
        
        # Perform comprehensive analysis
        results = autonomous_agent.analyze_cobol_comprehensive(cobol_code, filename)
        
        # Store results in existing database structure
        try:
            program_id = results.get('structure_analysis', {}).get('program_id', 'UNKNOWN')
            program = CobolProgram.query.filter_by(program_id=program_id).first()
            
            if not program:
                program = CobolProgram(
                    program_id=program_id,
                    file_name=filename,
                    source_code=cobol_code,
                    ast_structure=results.get('structure_analysis', {}),
                    procedures=results.get('structure_analysis', {}).get('procedures', []),
                    working_storage=results.get('structure_analysis', {}).get('working_storage', []),
                    dependencies=results.get('structure_analysis', {}).get('dependencies', []),
                    complexity=results.get('complexity_analysis', {}).get('complexity_rating', 'Unknown'),
                    line_count=results.get('structure_analysis', {}).get('total_lines', 0)
                )
                db.session.add(program)
            else:
                # Update existing program with enhanced analysis
                program.ast_structure = results.get('structure_analysis', {})
                program.procedures = results.get('structure_analysis', {}).get('procedures', [])
                program.working_storage = results.get('structure_analysis', {}).get('working_storage', [])
                program.dependencies = results.get('structure_analysis', {}).get('dependencies', [])
                program.complexity = results.get('complexity_analysis', {}).get('complexity_rating', 'Unknown')
            
            db.session.commit()
            results['database_id'] = program.id
            
        except Exception as db_error:
            logger.warning(f"Database storage failed: {db_error}")
            # Continue without database storage
        
        return jsonify({
            'success': True,
            'analysis_results': results
        })
        
    except Exception as e:
        logger.error(f"Enhanced analysis error: {str(e)}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/convert-data', methods=['POST'])
def api_convert_data():
    """COBOL data file conversion API"""
    if not data_converter:
        return jsonify({
            'error': 'Data conversion service not available',
            'message': 'COBOL data converter could not be initialized'
        }), 503
    
    try:
        data = request.get_json()
        conversion_type = data.get('conversion_type')
        
        if conversion_type == 'cobol_to_json':
            cobol_data_file = data.get('cobol_data_file')
            copybook_content = data.get('copybook_content')
            copybook_name = data.get('copybook_name', 'copybook.cbl')
            options = data.get('options', {})
            
            if not cobol_data_file or not copybook_content:
                return jsonify({'error': 'COBOL data file and copybook content are required'}), 400
            
            result = data_converter.convert_cobol_to_json(
                cobol_data_file,
                copybook_content,
                copybook_name,
                options=options
            )
            
        elif conversion_type == 'json_to_cobol':
            json_file = data.get('json_file')
            copybook_content = data.get('copybook_content')
            output_file = data.get('output_file', 'output.dat')
            options = data.get('options', {})
            
            if not json_file or not copybook_content:
                return jsonify({'error': 'JSON file and copybook content are required'}), 400
            
            result = data_converter.convert_json_to_cobol(
                json_file,
                copybook_content,
                output_file,
                options=options
            )
            
        else:
            return jsonify({'error': 'Invalid conversion type. Use "cobol_to_json" or "json_to_cobol"'}), 400
        
        return jsonify({
            'success': True,
            'conversion_result': result
        })
        
    except Exception as e:
        logger.error(f"Data conversion error: {str(e)}")
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500

@app.route('/api/llm-analysis', methods=['POST'])
def api_llm_analysis():
    """Advanced LLM-powered analysis"""
    if not llm_service:
        return jsonify({
            'error': 'LLM analysis service not available',
            'message': 'Please configure your API keys for Groq, Perplexity, or OpenAI'
        }), 503
    
    try:
        data = request.get_json()
        cobol_code = data.get('cobol_code')
        filename = data.get('filename', 'unknown.cbl')
        
        if not cobol_code:
            return jsonify({'error': 'COBOL code is required'}), 400
        
        # Create analysis job
        job_id = llm_service.create_analysis_job(cobol_code, filename)
        
        # Get job status (this will include results when completed)
        job_status = llm_service.get_job_status(job_id)
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'job_status': job_status
        })
        
    except Exception as e:
        logger.error(f"LLM analysis error: {str(e)}")
        return jsonify({'error': f'LLM analysis failed: {str(e)}'}), 500

@app.route('/api/services-status')
def api_services_status():
    """Check status of enhanced services"""
    status = {
        'enhanced_services': {
            'autonomous_agent': autonomous_agent is not None,
            'data_converter': data_converter is not None,
            'llm_service': llm_service is not None
        },
        'api_keys_available': {
            'groq': bool(os.environ.get('GROQ_API_KEY')),
            'perplexity': bool(os.environ.get('PERPLEXITY_API_KEY')),
            'openai': bool(os.environ.get('OPENAI_API_KEY'))
        },
        'capabilities': {
            'comprehensive_analysis': autonomous_agent is not None,
            'security_analysis': autonomous_agent is not None,
            'modernization_assessment': autonomous_agent is not None,
            'data_file_conversion': data_converter is not None,
            'visual_diagrams': autonomous_agent is not None,
            'ai_documentation': llm_service is not None
        }
    }
    
    return jsonify({
        'success': True,
        'status': status
    })

# COCO LLM Integration Routes
@app.route('/api/coco/upload', methods=['POST'])
def coco_upload_cobol():
    """Enhanced COBOL file upload with COCO LLM processing"""
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'cbl', 'cob', 'cobol', 'txt'}
    
    # Ensure upload directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if file and allowed_file(file.filename):
        job_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, f"{job_id}_{filename}")
        file.save(file_path)

        # Create a comprehensive job record
        job_data = {
            "job_id": job_id,
            "filename": filename,
            "file_path": file_path,
            "status": "queued",
            "created_at": time.time(),
            "analysis_type": "coco_enhanced"
        }

        # Store job info
        job_file = os.path.join(UPLOAD_FOLDER, f"{job_id}.json")
        with open(job_file, 'w') as f:
            json.dump(job_data, f)

        # Process with enhanced analysis
        try:
            with open(file_path, 'r') as f:
                cobol_code = f.read()

            # Try COCO LLM service first, then autonomous agent
            try:
                from coco_llm_service import coco_llm_service
                analysis_result = coco_llm_service.analyze_cobol_program(cobol_code, filename)
                analysis_type = "coco_llm"
            except Exception as coco_error:
                if autonomous_agent:
                    analysis_result = autonomous_agent.analyze_cobol_comprehensive(cobol_code, filename)
                    analysis_type = "autonomous_agent"
                else:
                    raise Exception("No analysis service available")
                
            # Store enhanced documentation
            enhanced_doc = {
                "job_id": job_id,
                "timestamp": time.time(),
                "program_name": analysis_result.get('program_name', analysis_result.get('structure_analysis', {}).get('program_id', 'Unknown')),
                "coco_analysis": analysis_result,
                "documentation_type": f"enhanced_{analysis_type}"
            }
            
            doc_path = os.path.join(UPLOAD_FOLDER, f"{job_id}_coco_documentation.json")
            with open(doc_path, 'w') as f:
                json.dump(enhanced_doc, f)
            
            # Update job status
            job_data['status'] = 'completed'
            job_data['completed_at'] = time.time()
            with open(job_file, 'w') as f:
                json.dump(job_data, f)

            return jsonify({
                "job_id": job_id, 
                "status": "completed",
                "analysis_type": analysis_type,
                "documentation_ready": True
            })

        except Exception as e:
            logger.error(f"COCO analysis error: {str(e)}")
            return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

    return jsonify({"error": "Invalid file type"}), 400

@app.route('/api/coco/job/<job_id>')
def coco_get_job_status(job_id):
    """Get COCO LLM job status and documentation"""
    try:
        job_file = os.path.join('uploads', f"{job_id}.json")
        with open(job_file, 'r') as f:
            job_data = json.load(f)
        
        # Check for enhanced documentation
        doc_file = os.path.join('uploads', f"{job_id}_coco_documentation.json")
        if os.path.exists(doc_file):
            with open(doc_file, 'r') as f:
                documentation = json.load(f)
            job_data['documentation'] = documentation
        
        return jsonify(job_data)
    except FileNotFoundError:
        return jsonify({"error": "Job not found"}), 404

@app.route('/api/coco/documentation/<job_id>')
def coco_view_documentation(job_id):
    """Display enhanced COBOL documentation with COCO LLM insights"""
    try:
        doc_file = os.path.join('uploads', f"{job_id}_coco_documentation.json")
        if os.path.exists(doc_file):
            with open(doc_file, 'r') as f:
                documentation = json.load(f)
            
            coco_analysis = documentation.get('coco_analysis', {})
            
            # Generate enhanced documentation HTML
            doc_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>COCO LLM Enhanced Documentation</title>
                <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
                <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            </head>
            <body>
                <div class="container mt-4">
                    <h1>🤖 COCO LLM Enhanced Documentation</h1>
                    <div class="alert alert-success">
                        <strong>Program:</strong> {documentation.get('program_name', 'Unknown')}<br>
                        <strong>Analysis Type:</strong> Enhanced COBOL Intelligence<br>
                        <strong>Generated:</strong> {time.ctime(documentation.get('timestamp', 0))}
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="card">
                                <div class="card-header">📊 Complexity Analysis</div>
                                <div class="card-body">
                                    <p><strong>Rating:</strong> {coco_analysis.get('complexity_analysis', {}).get('complexity_rating', 'N/A')}</p>
                                    <p><strong>Cyclomatic Complexity:</strong> {coco_analysis.get('complexity_analysis', {}).get('cyclomatic_complexity', 'N/A')}</p>
                                    <p><strong>Maintainability:</strong> {coco_analysis.get('complexity_analysis', {}).get('maintainability_index', 'N/A')}</p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-md-6">
                            <div class="card">
                                <div class="card-header">🔒 Security Assessment</div>
                                <div class="card-body">
                                    <p><strong>Risk Level:</strong> {coco_analysis.get('security_analysis', {}).get('risk_level', 'N/A')}</p>
                                    <p><strong>Issues Found:</strong> {len(coco_analysis.get('security_analysis', {}).get('vulnerabilities', []))}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mt-4">
                        <div class="card">
                            <div class="card-header">📈 Modernization Recommendations</div>
                            <div class="card-body">
                                <p><strong>Modernization Score:</strong> {coco_analysis.get('modernization_assessment', {}).get('modernization_score', 'N/A')}/100</p>
                                <p><strong>Priority:</strong> {coco_analysis.get('modernization_assessment', {}).get('priority', 'N/A')}</p>
                                <p><strong>Estimated Effort:</strong> {coco_analysis.get('modernization_assessment', {}).get('estimated_effort_days', 'N/A')} days</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mt-4">
                        <div class="card">
                            <div class="card-header">🎯 Program Flow Diagram</div>
                            <div class="card-body">
                                <div class="mermaid">
                                    {coco_analysis.get('documentation', {}).get('visual_diagrams', {}).get('program_flow', 'graph TD; A[No diagram available]')}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <script>
                    mermaid.initialize({{startOnLoad: true, theme: 'dark'}});
                </script>
            </body>
            </html>
            """
            
            return doc_html
        else:
            return jsonify({"error": "Documentation not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/coco-analyzer')
def coco_analyzer_interface():
    """Enhanced COBOL analyzer interface with COCO LLM"""
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>COCO LLM - COBOL Intelligence Platform</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <div class="text-center mb-5">
                <h1 class="display-4">🤖 COCO LLM</h1>
                <p class="lead">Advanced COBOL Intelligence & Documentation Platform</p>
            </div>
            
            <div class="row">
                <div class="col-md-8 mx-auto">
                    <div class="card">
                        <div class="card-header">
                            <h5>📁 Upload COBOL Program for Analysis</h5>
                        </div>
                        <div class="card-body">
                            <form id="cobolUploadForm" enctype="multipart/form-data">
                                <div class="mb-3">
                                    <label class="form-label">Select COBOL File (.cbl, .cob, .cobol, .txt)</label>
                                    <input type="file" class="form-control" id="cobolFile" accept=".cbl,.cob,.cobol,.txt" required>
                                </div>
                                <button type="submit" class="btn btn-primary">🚀 Analyze with COCO LLM</button>
                            </form>
                            
                            <div id="uploadStatus" class="mt-3"></div>
                            <div id="analysisResult" class="mt-3"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-4">
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body text-center">
                            <h6>🧠 AI-Powered Analysis</h6>
                            <p class="small">Advanced LLM specifically trained on COBOL and mainframe systems</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body text-center">
                            <h6>📊 Comprehensive Reports</h6>
                            <p class="small">Complexity analysis, security assessment, and modernization planning</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body text-center">
                            <h6>🎯 Visual Diagrams</h6>
                            <p class="small">Interactive flowcharts and dependency mapping</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
        document.getElementById('cobolUploadForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const fileInput = document.getElementById('cobolFile');
            const statusDiv = document.getElementById('uploadStatus');
            const resultDiv = document.getElementById('analysisResult');
            
            if (!fileInput.files[0]) {
                statusDiv.innerHTML = '<div class="alert alert-warning">Please select a file</div>';
                return;
            }
            
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            
            statusDiv.innerHTML = '<div class="alert alert-info">🔄 Uploading and analyzing...</div>';
            resultDiv.innerHTML = '';
            
            try {
                const response = await fetch('/api/coco/upload', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    statusDiv.innerHTML = '<div class="alert alert-success">✅ Analysis completed!</div>';
                    
                    if (result.documentation_ready) {
                        resultDiv.innerHTML = `
                            <div class="card">
                                <div class="card-body">
                                    <h6>📋 Analysis Complete</h6>
                                    <p><strong>Job ID:</strong> ${result.job_id}</p>
                                    <p><strong>Type:</strong> ${result.analysis_type}</p>
                                    <a href="/api/coco/documentation/${result.job_id}" class="btn btn-success" target="_blank">
                                        📖 View Enhanced Documentation
                                    </a>
                                </div>
                            </div>
                        `;
                    } else {
                        resultDiv.innerHTML = `
                            <div class="alert alert-info">
                                <strong>Job ID:</strong> ${result.job_id}<br>
                                Basic analysis completed. Enhanced features require configuration.
                            </div>
                        `;
                    }
                } else {
                    statusDiv.innerHTML = `<div class="alert alert-danger">❌ Error: ${result.error}</div>`;
                }
            } catch (error) {
                statusDiv.innerHTML = `<div class="alert alert-danger">❌ Upload failed: ${error.message}</div>`;
            }
        });
        </script>
    </body>
    </html>
    ''')

@app.route('/enhanced-features')
def enhanced_features():
    """Display available enhanced features including COCO LLM"""
    features = {
        'autonomous_analysis': autonomous_agent is not None,
        'data_conversion': data_converter is not None,
        'llm_analysis': llm_service is not None,
        'coco_llm_integration': True,
        'api_keys_available': {
            'groq': bool(os.environ.get('GROQ_API_KEY')),
            'perplexity': bool(os.environ.get('PERPLEXITY_API_KEY')),
            'openai': bool(os.environ.get('OPENAI_API_KEY')),
            'senso': bool(os.environ.get('SENSO_KEY'))
        }
    }
    return jsonify({
        'success': True,
        'enhanced_features': features,
        'message': 'Enhanced COBOL analysis features with COCO LLM integration available'
    })