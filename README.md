# Document Summarizer

An intelligent document processing system built with Django that automatically extracts text from documents and generates comprehensive summaries using advanced AI models.

## What This Project Does

This application helps you process and understand documents quickly by:

- Extracting text content from PDF, DOCX, and TXT files
- Generating both brief summaries and detailed notes using AI
- Managing document uploads through a secure user system
- Processing large documents in the background for better performance
- Providing a complete REST API for integration with other applications

## Technology Stack

**Backend Framework:** Django 5.0 with Django REST Framework  
**Authentication:** JWT tokens via SimpleJWT  
**AI Engine:** HuggingFace Transformers with T5-small model  
**Database:** PostgreSQL with SQLite fallback  
**Background Processing:** Celery with Redis  
**Document Processing:** PyMuPDF for PDFs, python-docx for Word documents  

## Key Features

**User Management**
- Secure user registration and authentication
- JWT-based session management
- User-specific document access

**Document Processing**
- Support for PDF, DOCX, and TXT file formats
- Automatic text extraction with size limits
- File validation and error handling

**AI Summarization**
- Short summaries for quick overview
- Detailed bullet-point notes for comprehensive understanding
- Configurable summary lengths
- Multiple summarization modes

**Smart Processing**
- Small documents processed immediately
- Large documents handled asynchronously in background
- Real-time status tracking (pending, processing, complete, failed)
- Manual retry capability for failed processes

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Redis (for background processing)
- Git

### Installation

1. **Clone and setup the project:**
```bash
git clone <repository-url>
cd document-summarizer
python -m venv .venv
```

2. **Activate virtual environment:**
```bash
# Windows
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
```
Edit the `.env` file to customize settings if needed.

5. **Setup database:**
```bash
python manage.py migrate
python manage.py createsuperuser  # Optional: for admin access
```

6. **Start the development server:**
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

### Starting Background Processing (Optional)

For processing large documents asynchronously:

1. **Start Redis server:**
```bash
# Using Docker
docker run -d -p 6379:6379 redis:latest

# Or install Redis locally
```

2. **Start Celery worker:**
```bash
python -m celery -A summarizer_backend worker --loglevel=info
```

## Using the Application

### Getting Started - Step by Step

Once you have the server running (`python manage.py runserver`), follow these steps:

#### 1. Access the Application
Open your web browser and visit: `http://127.0.0.1:8000/api/`

#### 2. Create Your Account
- Go to: `http://127.0.0.1:8000/api/auth/register/`
- Fill in the registration form with:
  - Username: Choose any username
  - Email: Your email address
  - Password: At least 8 characters
- Click "POST" to create your account
- You should see: `HTTP 201 Created` with your user details

#### 3. Login to Get Access
- Go to: `http://127.0.0.1:8000/api/auth/login/`
- Enter your username and password
- Click "POST" to login
- You'll receive JWT tokens (save the "access" token for API calls)

#### 4. Access Protected Features
After logging in, you can access:

**Document Upload:**
- Visit: `http://127.0.0.1:8000/api/documents/`
- Look for "Log in" link in top-right corner and click it
- Login with your credentials
- Once logged in, you can upload PDF, DOCX, or TXT files
- Files are automatically processed and summarized

**Direct Text Summarization:**
- Visit: `http://127.0.0.1:8000/api/summarize-text/`
- Login using the web interface
- Paste any text and get instant AI summaries
- Choose summary mode: short, detailed, or both

### Web Interface Features

The Django REST Framework provides a user-friendly web interface where you can:

**Authentication:**
-  **Register**: Create new accounts via web form
-  **Login**: Authenticate via web interface
-  **Logout**: End your session securely

**Document Management:**
-  **Upload**: Drag-and-drop or browse for files
-  **View**: See all your uploaded documents
-  **Auto-Summary**: AI generates summaries automatically
-  **Delete**: Remove documents when no longer needed

**Text Processing:**
-  **Direct Input**: Paste text directly for summarization
-  **Instant Results**: Get summaries in seconds
-  **Multiple Modes**: Short overview or detailed notes

### Important Notes for Users

**File Formats Supported:**
- PDF documents (.pdf)
- Microsoft Word documents (.docx)
- Plain text files (.txt)

**Security:**
- Registration is open to everyone
- Document upload requires login (your files are protected)
- Only you can see your uploaded documents

**If You Don't See Login Options:**
- Refresh the browser page
- Make sure you're visiting the correct URLs
- The login link appears in the top-right corner of API pages

### API Endpoints

**Authentication:**
- `POST /api/auth/register/` - Create new user account
- `POST /api/auth/login/` - Get authentication tokens
- `POST /api/auth/refresh/` - Refresh access token

**Document Management:**
- `POST /api/documents/` - Upload document for processing
- `GET /api/documents/` - List your uploaded documents
- `GET /api/documents/{id}/summary/` - View document summary
- `DELETE /api/documents/{id}/` - Remove document

**Text Processing:**
- `POST /api/summarize-text/` - Summarize raw text directly

### Example User Workflow

1. **Start the server**: `python manage.py runserver`
2. **Register**: Visit registration page and create account
3. **Login**: Get your authentication tokens
4. **Upload**: Add a document via the web interface
5. **Review**: Check your automatically generated summaries
6. **Summarize**: Try direct text summarization for quick tasks

## Configuration

Key environment variables in `.env`:

```
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
SUMMARIZATION_MODEL_NAME=t5-small
REDIS_URL=redis://localhost:6379/0
MAX_DOCUMENT_SIZE_MB=25
AUTO_SUMMARY_MAX_CHAR=40000
```

## Development

### Running Tests

```bash
python manage.py test
```

### Code Structure

- `accounts/` - User authentication and management
- `documents/` - Document upload and text extraction
- `summarization/` - AI summarization engine and background tasks
- `summarizer_backend/` - Django project settings and configuration

## Deployment Considerations

**For Production:**
- Set `DJANGO_DEBUG=False`
- Use PostgreSQL database
- Configure proper Redis instance
- Set up proper static file serving
- Use environment variables for sensitive settings
- Consider using Gunicorn as WSGI server

**Security:**
- Change default secret key
- Configure CORS settings
- Set up proper authentication
- Use HTTPS in production

## Troubleshooting

**Common Issues:**

*Documents stuck in "pending" status:*
- Ensure Redis is running
- Start Celery worker for background processing

*Upload errors:*
- Check file size limits
- Verify supported file formats (PDF, DOCX, TXT)

*Authentication issues:*
- Verify JWT token is included in requests
- Check token expiration time

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For questions or issues, please check the troubleshooting section above or create an issue in the project repository.
