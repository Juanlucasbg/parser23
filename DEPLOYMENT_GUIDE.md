# COBOL CodeSense - Complete Local Deployment Guide

A comprehensive step-by-step guide to deploy the COBOL analysis platform from ZIP file to a fully functional local system.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Pre-Installation Setup](#pre-installation-setup)
3. [Database Configuration](#database-configuration)
4. [Application Installation](#application-installation)
5. [Environment Configuration](#environment-configuration)
6. [Database Initialization](#database-initialization)
7. [Application Startup](#application-startup)
8. [Verification & Testing](#verification--testing)
9. [Troubleshooting](#troubleshooting)
10. [Optional AI Features](#optional-ai-features)

---

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.11 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **PostgreSQL**: Version 12 or higher

### Software Dependencies
- Git (optional, for version control)
- Text editor or IDE (VS Code, PyCharm, etc.)
- Web browser (Chrome, Firefox, Safari, Edge)

---

## Pre-Installation Setup

### Step 1: Download and Extract Files

1. **Download** the project ZIP file to your computer
2. **Extract** the ZIP file to your desired location:
   ```
   cobol-analysis-platform/
   ├── app.py
   ├── main.py
   ├── models.py
   ├── routes.py
   ├── config.py
   ├── cobol_parser.py
   ├── utils.py
   ├── analytics_service.py
   ├── database_setup.py
   ├── knowledge.py
   ├── llm_integration.py
   ├── ingest.py
   ├── static/
   ├── templates/
   ├── uploads/
   └── requirements.txt
   ```

### Step 2: Verify Python Installation

Open terminal/command prompt and check Python version:

```bash
python --version
# or
python3 --version
```

**Expected output**: `Python 3.11.x` or higher

If Python is not installed:
- **Windows**: Download from [python.org](https://python.org) and install
- **macOS**: Use Homebrew: `brew install python@3.11`
- **Linux**: Use package manager: `sudo apt install python3.11 python3.11-venv`

---

## Database Configuration

### Step 3: Install PostgreSQL

#### Windows Installation
1. Download PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run the installer with these settings:
   - Port: `5432`
   - Superuser password: Choose a strong password
   - Keep default locale
3. Add PostgreSQL to PATH during installation

#### macOS Installation
```bash
# Using Homebrew
brew install postgresql@15
brew services start postgresql@15

# Or download from postgresql.org
```

#### Linux Installation
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Step 4: Create Database User and Database

Open terminal and connect to PostgreSQL:

```bash
# Connect as postgres superuser
sudo -u postgres psql

# Or on Windows/macOS
psql -U postgres
```

Execute these SQL commands:

```sql
-- Create user with password
CREATE USER cobol_user WITH PASSWORD 'secure_password_123';

-- Create database
CREATE DATABASE cobol_analysis OWNER cobol_user;

-- Grant all privileges
GRANT ALL PRIVILEGES ON DATABASE cobol_analysis TO cobol_user;

-- Grant schema privileges
GRANT ALL PRIVILEGES ON SCHEMA public TO cobol_user;

-- Exit PostgreSQL
\q
```

### Step 5: Test Database Connection

```bash
# Test connection
psql -h localhost -U cobol_user -d cobol_analysis

# You should see a prompt like:
# cobol_analysis=>
```

If successful, type `\q` to exit.

---

## Application Installation

### Step 6: Create Python Virtual Environment

Navigate to your extracted project directory:

```bash
cd path/to/cobol-analysis-platform
```

Create and activate virtual environment:

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 7: Install Python Dependencies

Create a `requirements.txt` file with these contents:

```txt
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
psycopg2-binary==2.9.7
gunicorn==21.2.0
Werkzeug==2.3.7
email-validator==2.0.0
SQLAlchemy==2.0.20
```

Install dependencies:

```bash
pip install -r requirements.txt
```

**Expected output**: Successfully installed packages without errors.

### Step 8: Create Upload Directory

```bash
# Create uploads directory if it doesn't exist
mkdir -p uploads
chmod 755 uploads  # On Unix systems
```

---

## Environment Configuration

### Step 9: Create Environment Configuration

Create a `.env` file in the project root directory:

```env
# Database Configuration
DATABASE_URL=postgresql://cobol_user:secure_password_123@localhost:5432/cobol_analysis

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SESSION_SECRET=change-this-to-a-random-secret-key-in-production

# Application Settings
MAX_CONTENT_LENGTH=104857600
UPLOAD_FOLDER=uploads

# Optional: AI Features (uncomment and fill if you have API keys)
# OPENAI_API_KEY=your-openai-api-key-here
# CUSTOM_LLM_ENDPOINT=your-custom-llm-endpoint
# CUSTOM_LLM_TOKEN=your-custom-llm-token

# Optional: Advanced Analytics (uncomment if you have these services)
# WEAVIATE_URL=http://localhost:8080
# WEAVIATE_API_KEY=your-weaviate-api-key
# COGNEE_API_KEY=your-cognee-api-key
```

**Important**: Replace `secure_password_123` with your actual PostgreSQL password.

### Step 10: Load Environment Variables

**Windows (Command Prompt):**
```cmd
set DATABASE_URL=postgresql://cobol_user:secure_password_123@localhost:5432/cobol_analysis
set SESSION_SECRET=your-secret-key
set FLASK_DEBUG=True
```

**Windows (PowerShell):**
```powershell
$env:DATABASE_URL="postgresql://cobol_user:secure_password_123@localhost:5432/cobol_analysis"
$env:SESSION_SECRET="your-secret-key"
$env:FLASK_DEBUG="True"
```

**macOS/Linux:**
```bash
export DATABASE_URL="postgresql://cobol_user:secure_password_123@localhost:5432/cobol_analysis"
export SESSION_SECRET="your-secret-key"
export FLASK_DEBUG=True
```

---

## Database Initialization

### Step 11: Initialize Database Tables

Run the database initialization command:

```bash
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database tables created successfully')"
```

**Expected output**: `Database tables created successfully`

### Step 12: Verify Database Schema

Connect to database and check tables:

```bash
psql -h localhost -U cobol_user -d cobol_analysis
```

List tables:
```sql
\dt
```

**Expected output**: You should see tables like:
- `cobol_programs`
- `analysis_sessions`
- `chat_messages`
- `program_dependencies`
- `system_stats`

Exit with `\q`.

---

## Application Startup

### Step 13: Start the Application

Run the application:

```bash
python main.py
```

**Expected output**:
```
INFO:root:Database tables created successfully
INFO:root:Weaviate schema setup skipped - external service not configured
WARNING:root:Failed to initialize Weaviate schema - vector search may not work
INFO:root:Cognee.ai initialization skipped - external service not configured
WARNING:root:Failed to initialize Cognee.ai - knowledge graph features may not work
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://[your-ip]:5000
```

### Step 14: Alternative Startup Methods

**Using Gunicorn (Production-like):**
```bash
gunicorn --bind 0.0.0.0:5000 --reload main:app
```

**Using Flask Development Server:**
```bash
export FLASK_APP=main.py
flask run --host=0.0.0.0 --port=5000
```

---

## Verification & Testing

### Step 15: Access the Application

Open your web browser and navigate to:
- **Local access**: http://localhost:5000
- **Network access**: http://your-ip-address:5000

### Step 16: Test Core Features

1. **Homepage**: Should display the COBOL CodeSense dashboard
2. **Upload Page**: Navigate to `/upload` - should show file upload interface
3. **Analysis Page**: Navigate to `/analysis` - should show empty state initially
4. **Chat Page**: Navigate to `/chat` - should show AI chat interface
5. **Analytics Page**: Navigate to `/analytics` - should show analytics dashboard
6. **Dependencies Page**: Navigate to `/dependencies` - should show dependency visualization

### Step 17: Test File Upload

1. Create a simple test COBOL file (`test.cob`):
```cobol
       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLO-WORLD.
       
       PROCEDURE DIVISION.
           DISPLAY 'Hello, COBOL World!'.
           STOP RUN.
```

2. Upload the file through the web interface
3. Check if it appears in the Analysis page
4. Verify database contains the program:
```bash
psql -h localhost -U cobol_user -d cobol_analysis -c "SELECT program_id, file_name FROM cobol_programs;"
```

---

## Troubleshooting

### Common Issues and Solutions

#### Database Connection Errors

**Issue**: `psycopg2.OperationalError: could not connect to server`

**Solutions**:
1. Verify PostgreSQL is running:
   ```bash
   # Check service status
   sudo systemctl status postgresql  # Linux
   brew services list | grep postgresql  # macOS
   ```

2. Check connection parameters:
   ```bash
   psql -h localhost -U cobol_user -d cobol_analysis
   ```

3. Verify database URL format:
   ```
   postgresql://username:password@host:port/database
   ```

#### Port Already in Use

**Issue**: `Address already in use: Port 5000`

**Solutions**:
1. Kill existing process:
   ```bash
   # Find process using port 5000
   lsof -i :5000  # macOS/Linux
   netstat -ano | findstr :5000  # Windows
   
   # Kill the process
   kill -9 <PID>
   ```

2. Use different port:
   ```bash
   python main.py --port 5001
   ```

#### Python Module Errors

**Issue**: `ModuleNotFoundError: No module named 'flask'`

**Solutions**:
1. Ensure virtual environment is activated:
   ```bash
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### File Upload Issues

**Issue**: File uploads fail or directory errors

**Solutions**:
1. Create uploads directory:
   ```bash
   mkdir -p uploads
   chmod 755 uploads
   ```

2. Check disk space:
   ```bash
   df -h  # Unix systems
   dir    # Windows
   ```

#### Database Permission Errors

**Issue**: `permission denied for schema public`

**Solutions**:
```sql
-- Connect as postgres superuser
sudo -u postgres psql

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE cobol_analysis TO cobol_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO cobol_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO cobol_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO cobol_user;
```

---

## Optional AI Features

### Step 18: Enable AI Chat Features

To enable AI-powered code analysis and chat:

1. **Get OpenAI API Key**:
   - Visit [OpenAI API](https://platform.openai.com/api-keys)
   - Create account and generate API key

2. **Add API Key to Environment**:
   ```bash
   export OPENAI_API_KEY="your-actual-api-key-here"
   ```

3. **Update .env file**:
   ```env
   OPENAI_API_KEY=your-actual-api-key-here
   ```

4. **Restart Application**:
   ```bash
   # Stop current application (Ctrl+C)
   # Restart
   python main.py
   ```

### Step 19: Test AI Features

1. Navigate to the Chat page
2. Upload a COBOL file first
3. Try AI commands:
   - "explain HELLO-WORLD"
   - "what does this program do?"
   - "find dependencies of HELLO-WORLD"

---

## Production Deployment Notes

### Security Considerations

1. **Change Secret Key**:
   ```env
   SESSION_SECRET=generate-a-strong-random-secret-key
   ```

2. **Database Security**:
   - Use strong passwords
   - Limit database user permissions
   - Consider SSL connections

3. **Environment Variables**:
   ```env
   FLASK_ENV=production
   FLASK_DEBUG=False
   ```

### Performance Optimization

1. **Use Gunicorn with Multiple Workers**:
   ```bash
   gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
   ```

2. **Database Connection Pooling**:
   - Already configured in `app.py`
   - Adjust pool settings as needed

3. **Static File Serving**:
   - Consider using nginx for static files in production
   - Current setup serves static files through Flask

---

## Support and Maintenance

### Logs and Debugging

1. **Application Logs**: Check console output for errors
2. **Database Logs**: Check PostgreSQL logs in system logs
3. **Debug Mode**: Set `FLASK_DEBUG=True` for detailed errors

### Backup and Recovery

1. **Database Backup**:
   ```bash
   pg_dump -h localhost -U cobol_user cobol_analysis > backup.sql
   ```

2. **Database Restore**:
   ```bash
   psql -h localhost -U cobol_user cobol_analysis < backup.sql
   ```

3. **File Backup**: Backup the `uploads/` directory regularly

### Updates and Maintenance

1. **Update Dependencies**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Database Migrations**: 
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

---

## Conclusion

You now have a fully functional COBOL analysis platform running locally! The system provides:

- ✅ File upload and parsing
- ✅ Code structure analysis
- ✅ Dependency mapping
- ✅ Analytics dashboard
- ✅ Search capabilities
- ✅ AI chat features (with API key)

For additional support or advanced configuration, refer to the individual component documentation or check the application logs for specific error messages.

**Happy COBOL analyzing!** 🚀