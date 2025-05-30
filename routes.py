# Routes registration function for the holistic COBOL platform
from flask import render_template, render_template_string

def register_routes(app):
    """Register all routes for the holistic COBOL documentation platform"""
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/analyzer')
    def analyzer():
        return render_template('analyzer.html')
    
    @app.route('/coco-analyzer')
    def coco_analyzer():
        return render_template('analyzer.html')
    
    # Legacy route for compatibility
    @app.route('/legacy-index')
    def legacy_index():
        return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>🤖 COCO LLM - Holistic COBOL Documentation Platform</title>
            <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-5">
                <div class="row">
                    <div class="col-12 text-center">
                        <h1 class="display-3 mb-4">🤖 COCO LLM</h1>
                        <p class="lead">Holistic COBOL Documentation & Intelligence Platform</p>
                        <p class="text-muted">Advanced LLM specifically trained for mainframe modernization</p>
                    </div>
                </div>
                
                <div class="row mt-5">
                    <div class="col-md-6">
                        <div class="card h-100">
                            <div class="card-body">
                                <h5 class="card-title">📁 COCO Analyzer</h5>
                                <p class="card-text">Upload COBOL programs for comprehensive analysis using our specialized LLM trained on mainframe systems.</p>
                                <a href="/coco-analyzer" class="btn btn-primary btn-lg">🚀 Analyze COBOL Code</a>
                            </div>
                        </div>
                    </div>
                    
                    <div class="col-md-6">
                        <div class="card h-100">
                            <div class="card-body">
                                <h5 class="card-title">📊 Enhanced Analysis</h5>
                                <p class="card-text">Access advanced autonomous analysis with security assessment and modernization planning.</p>
                                <a href="/api/services-status" class="btn btn-success btn-lg">📈 View Capabilities</a>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row mt-4">
                    <div class="col-md-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <h6>🧠 AI Intelligence</h6>
                                <p class="small">Specialized LLM trained on COBOL and mainframe knowledge</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <h6>📋 Documentation</h6>
                                <p class="small">Comprehensive reports with visual diagrams and insights</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <h6>🔒 Security Analysis</h6>
                                <p class="small">Vulnerability detection and risk assessment</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <h6>📈 Modernization</h6>
                                <p class="small">Strategic planning for legacy system updates</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row mt-5">
                    <div class="col-12">
                        <div class="alert alert-success">
                            <h6 class="alert-heading">🎯 COCO LLM Features</h6>
                            <div class="row">
                                <div class="col-md-6">
                                    <ul class="list-unstyled mb-0">
                                        <li>✅ Complexity Analysis & Metrics</li>
                                        <li>✅ Security Vulnerability Assessment</li>
                                        <li>✅ Performance Optimization Recommendations</li>
                                    </ul>
                                </div>
                                <div class="col-md-6">
                                    <ul class="list-unstyled mb-0">
                                        <li>✅ Modernization Roadmap Planning</li>
                                        <li>✅ Interactive Visual Diagrams</li>
                                        <li>✅ Comprehensive Documentation Generation</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        ''')
    
    # Import and register enhanced routes including COCO LLM
    try:
        from enhanced_routes import app as enhanced_app
        print("✅ Enhanced API endpoints with COCO LLM loaded")
    except Exception as e:
        print(f"⚠️ Enhanced routes import warning: {e}")
    
    # Import COCO LLM service
    try:
        from coco_llm_service import coco_llm_service
        print("✅ COCO LLM service initialized")
    except Exception as e:
        print(f"⚠️ COCO LLM service warning: {e}")