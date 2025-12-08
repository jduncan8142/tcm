# Project Context

## Purpose
Test Case Management (TCM) is a web application for test case creation and tracking. The application uses projects as its primary organizational element. Test cases are created at a global level and tagged with metadata including:
- Business organization/unit
- System
- Process
- Module
- Customer/Vendor
- Program

The goal is to provide a centralized platform for managing test cases across multiple projects and organizational boundaries.

## Tech Stack
- **Backend**: Python with FastAPI
- **Frontend**: Python with FastHTML
- **Database**: PostgreSQL
- **Deployment**: (To be determined)

## Project Conventions

### Code Style
- Follow flexible guidelines rather than strict enforcement
- Adhere to PEP 8 for Python code
- Use clear, descriptive variable and function names
- Prefer readability over cleverness
- Add docstrings for public functions and classes

### Architecture Patterns
- RESTful API design with FastAPI for backend endpoints
- Separation of concerns between data models, business logic, and presentation
- Use SQLAlchemy ORM for database interactions
- FastHTML for server-side rendering and interactive frontend components
- Implement proper authentication and authorization for multi-tenant data access
- Async/await patterns for improved performance with FastAPI

### Testing Strategy
- **Unit Tests**: Required for all new features and business logic
  - Test individual functions and methods in isolation
  - Mock external dependencies
- **Integration Tests**: Test interactions between components
  - Database operations
  - API endpoints
  - Service layer interactions
- **End-to-End Tests**: Critical user workflows
  - Test case creation and editing
  - Project management
  - Search and filtering functionality

### Git Workflow
- **Main Branch**: `main` (protected)
- Create feature branches for new work
- Use descriptive commit messages
- Submit pull requests for code review before merging

## Domain Context

### Test Case Management Concepts
- **Test Case**: A single test scenario with steps, expected results, and metadata
- **Project**: Organizational unit that groups related test execution efforts
- **Metadata Tags**: Categorization system for test cases (org/unit, system, process, module, etc.)
- **Global Test Cases**: Test cases exist independently of projects and can be reused across multiple projects

### Data Model Considerations
- Test cases should be globally accessible but filterable by metadata
- Many-to-many relationships between test cases and projects
- Hierarchical organization of metadata (e.g., org → unit → system → process)
- Audit trail for test case modifications

## Important Constraints
- Multi-tenant data access patterns must ensure proper isolation
- Search and filtering performance critical for large test case repositories
- Metadata taxonomy should be flexible and extensible

## External Dependencies
- PostgreSQL database server
- Python package dependencies:
  - FastAPI (async web framework)
  - FastHTML (Python-based frontend framework)
  - SQLAlchemy (ORM)
  - Pydantic (data validation)
  - psycopg2 or asyncpg (PostgreSQL drivers)
  - pytest (testing framework)
- (Additional dependencies to be determined as project evolves)
