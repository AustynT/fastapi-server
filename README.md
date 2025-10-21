# FastAPI Server

A robust, production-ready FastAPI server with authentication, authorization, and comprehensive logging.

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Run the automated setup script
python dev_setup.py
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your configuration
```

### Running the Server
```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Run the development server
python start_server.py

# Or with uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📋 Features

### ✅ Implemented Features
- **Authentication & Authorization**: JWT-based auth with refresh tokens
- **User Management**: Complete CRUD operations for users
- **Role-Based Access Control**: Permissions and roles system
- **Service Management**: Service catalog with pricing
- **Database Models**: Well-structured SQLAlchemy models
- **API Documentation**: Auto-generated OpenAPI/Swagger docs
- **Input Validation**: Pydantic schemas with comprehensive validation
- **Email Validation**: Proper email validation using email-validator
- **Structured Logging**: JSON logging in production, readable in development
- **Rate Limiting**: Protection against abuse on auth endpoints
- **Request/Response Logging**: Comprehensive HTTP request logging
- **Security Headers**: Security middleware for protection
- **CORS Configuration**: Configurable CORS settings
- **Environment Configuration**: Flexible environment-based configuration

### 🔧 Configuration

The application uses environment variables for configuration. Copy `.env.example` to `.env` and modify as needed:

```bash
# Application
APP_NAME=FastAPI Server
DEBUG=true
ENV=development

# Security (CHANGE IN PRODUCTION!)
SECRET_KEY=your_secret_key
JWT_SECRET=your_jwt_secret
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
DATABASE_URL=sqlite:///./fastapi_dev.db

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗️ Project Structure

```
fastapi-server/
├── app/
│   ├── api/
│   │   └── endpoints/          # API route handlers
│   ├── core/
│   │   └── config.py          # Configuration management
│   ├── db/
│   │   ├── database.py        # Database connection
│   │   └── dependency.py      # Database dependencies
│   ├── middleware/
│   │   └── logging_middleware.py  # Custom middleware
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic schemas
│   ├── services/              # Business logic layer
│   ├── utils/                 # Utility functions
│   └── main.py               # FastAPI application
├── tests/                    # Test files
├── alembic/                  # Database migrations
├── venv/                     # Virtual environment
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── dev_setup.py             # Development setup script
├── activate.sh              # Environment activation script
└── start_server.py          # Server startup script
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt password hashing
- **Rate Limiting**: Protection against brute force attacks
- **Security Headers**: XSS, CSRF, and clickjacking protection
- **Input Validation**: Comprehensive input sanitization
- **Token Blacklisting**: Ability to invalidate tokens

## 📊 Logging

The application includes structured logging with:
- **Request/Response Logging**: All HTTP requests are logged
- **Performance Metrics**: Request processing times
- **Security Events**: Authentication and authorization events
- **JSON Format**: Production-ready structured logs

## 🧪 Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_models.py
```

## 🚀 Production Deployment

1. **Environment Setup**:
   ```bash
   # Set production environment variables
   export ENV=production
   export DEBUG=false
   export DATABASE_URL=your_production_db_url
   ```

2. **Security**:
   - Change all secret keys in production
   - Use strong database passwords
   - Configure proper CORS origins
   - Set up SSL/TLS certificates

3. **Database**:
   ```bash
   # Run migrations
   alembic upgrade head
   ```

## 📝 Development

### Adding New Features
1. Create models in `app/models/`
2. Add schemas in `app/schemas/`
3. Implement services in `app/services/`
4. Create endpoints in `app/api/endpoints/`
5. Add tests in `tests/`

### Code Quality
- Follow PEP 8 style guidelines
- Add type hints
- Write comprehensive docstrings
- Include unit tests for new features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.


