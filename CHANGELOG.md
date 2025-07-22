# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-21

### Added
- Initial release of Stacking PR Task API
- FastAPI-based REST API for task management
- SQLAlchemy ORM integration with PostgreSQL support
- Comprehensive test suite with 70%+ coverage
- Docker containerization with health checks
- GitHub Actions CI/CD pipeline
- Security middleware (CORS, TrustedHost)
- API versioning (`/api/v1/` prefix)
- Proper error handling and validation
- Interactive API documentation (Swagger/ReDoc)

### Features
- **Task Management**: Create and retrieve tasks with proper validation
- **Database Integration**: SQLAlchemy models with PostgreSQL backend
- **API Documentation**: Auto-generated OpenAPI/Swagger docs at `/docs`
- **Health Checks**: Dedicated endpoints for monitoring
- **Security**: Production-ready security configurations
- **Testing**: Unit, integration, and API endpoint tests
- **Containerization**: Docker support with non-root user and health checks

### Technical Details
- Python 3.8+ support
- FastAPI 0.115.12
- SQLAlchemy 2.0.40
- PostgreSQL database backend
- Pytest testing framework
- Black code formatting
- GitHub Actions CI/CD