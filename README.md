# COBOL CodeSense - AI-Powered Legacy Code Analysis Platform

A comprehensive COBOL analysis platform with AI-powered code understanding, dependency mapping, and knowledge management capabilities.

## Features

- **File Upload & Processing**: Upload individual COBOL files or ZIP archives
- **Code Analysis**: Parse COBOL programs and extract structure, dependencies, and complexity metrics
- **AI Chat Interface**: Ask questions about your COBOL code using AI
- **Analytics Dashboard**: View complexity metrics, dependency graphs, and code statistics
- **Dependency Visualization**: Interactive network graphs showing program relationships
- **Search & Discovery**: Find programs by content, dependencies, or patterns

## Local Setup Instructions

### Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- Git

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd cobol-analysis-platform
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup

#### Option A: Local PostgreSQL
```bash
# Install PostgreSQL (varies by OS)
# Create database
createdb cobol_analysis

# Set environment variable
export DATABASE_URL="postgresql://username:password@localhost/cobol_analysis"
```

#### Option B: Docker PostgreSQL
```bash
docker run --name cobol-postgres -e POSTGRES_DB=cobol_analysis -e POSTGRES_USER=cobol -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:13

export DATABASE_URL="postgresql://cobol:password@localhost:5432/cobol_analysis"
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost/cobol_analysis

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SESSION_SECRET=your-secret-key-change-in-production

# Optional: AI Features (provide if you want AI chat functionality)
OPENAI_API_KEY=your-openai-api-key-here

# Optional: Advanced Features
WEAVIATE_URL=http://localhost:8080
COGNEE_API_KEY=your-cognee-api-key
CUSTOM_LLM_ENDPOINT=your-custom-llm-endpoint
CUSTOM_LLM_TOKEN=your-custom-llm-token
```

### 5. Initialize Database

```bash
# Run database migrations
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized')"
```

### 6. Start the Application

```bash
# Development server
python main.py

# Or using Gunicorn (production-like)
gunicorn --bind 0.0.0.0:5000 --reload main:app
```

The application will be available at: `http://localhost:5000`

## Project Structure

```
cobol-analysis-platform/
├── app.py                 # Flask application factory
├── main.py               # Application entry point
├── models.py             # Database models
├── routes.py             # URL routes and handlers
├── config.py             # Configuration settings
├── cobol_parser.py       # COBOL file parsing logic
├── utils.py              # Utility functions
├── analytics_service.py  # Analytics and reporting
├── database_setup.py     # Database configuration
├── knowledge.py          # Knowledge management
├── llm_integration.py    # AI/LLM integration
├── ingest.py            # Data ingestion pipeline
├── static/              # CSS, JavaScript, assets
├── templates/           # HTML templates
├── uploads/             # File upload directory
└── requirements.txt     # Python dependencies
```

## Usage Guide

### 1. Upload COBOL Files
- Navigate to the Upload page
- Drag and drop COBOL files (.cob, .cbl, .cobol, .cpy) or ZIP archives
- Files are automatically parsed and stored in the database

### 2. Analyze Code
- Visit the Analysis page to view parsed programs
- See program structure, complexity metrics, and dependencies
- Search for specific programs or patterns

### 3. Use AI Chat
- Go to the AI Chat page
- Ask questions about your COBOL code
- Try commands like:
  - "dependencies of PROGRAM-NAME"
  - "explain PROGRAM-NAME" 
  - "find similar to [code pattern]"
  - "what does [code] do?"

### 4. View Analytics
- Check the Analytics dashboard for:
  - Complexity distribution
  - Dependency graphs
  - Code statistics
  - Refactoring opportunities

### 5. Explore Dependencies
- Use the Dependencies page to visualize program relationships
- Interactive network graph shows how programs connect

## API Endpoints

- `POST /api/search` - Search programs
- `GET /api/program/<id>` - Get program details
- `POST /api/rebuild-knowledge-graph` - Rebuild knowledge graph
- `GET /api/analytics/overview` - Get analytics overview
- `GET /api/analytics/relationships` - Get relationship analysis

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
pg_isready

# Test connection
psql $DATABASE_URL -c "SELECT 1;"
```

### Missing Dependencies
```bash
# Reinstall packages
pip install --upgrade -r requirements.txt
```

### File Upload Issues
```bash
# Check uploads directory exists and is writable
mkdir -p uploads
chmod 755 uploads
```

### AI Features Not Working
- Ensure `OPENAI_API_KEY` is set in environment
- Check API key validity
- Review application logs for detailed error messages

## Development

### Adding New Features
1. Update models in `models.py`
2. Add routes in `routes.py`
3. Create templates in `templates/`
4. Add static assets in `static/`

### Database Migrations
```bash
# After model changes
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
pytest
```

## Production Deployment

### Environment Variables
```env
FLASK_ENV=production
FLASK_DEBUG=False
SESSION_SECRET=strong-random-secret-key
DATABASE_URL=postgresql://user:pass@host:port/db
```

### Using Docker
```bash
# Build image
docker build -t cobol-analysis .

# Run container
docker run -p 5000:5000 -e DATABASE_URL=$DATABASE_URL cobol-analysis
```

### Using Gunicorn
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

## Support

For issues and questions:
1. Check the application logs for error details
2. Verify all environment variables are set correctly
3. Ensure database connectivity
4. Check file permissions for uploads directory

## License

This project is licensed under the MIT License.