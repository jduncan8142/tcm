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
- **Package Manager**: uv (fast Python package manager)
- **Deployment**: (To be determined)

## Project Conventions

### Code Style
- Follow flexible guidelines rather than strict enforcement
- Adhere to PEP 8 for Python code
- Use clear, descriptive variable and function names
- Prefer readability over cleverness
- Add docstrings for public functions and classes

### Dependency Management
- Use `uv` for all Python package management
- Maintain `pyproject.toml` for project dependencies
- Use `uv sync` to install dependencies
- Lock dependencies with `uv.lock` for reproducible builds

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

### Predefined Metadata Tags
The system provides 40 predefined tag categories organized into logical groups. Custom tags can also be added as needed.

**Organizational** (7 tags):
- organization, business_unit, customer, vendor, program, squad, owner

**System/Technical** (7 tags):
- system, process, module, server, cloud_provider, database, protocol

**Test-Specific** (8 tags):
- test_type, test_level, automation_status, priority, risk_level, test_phase, test_status, maintenance_status

**Platform/Technology** (4 tags):
- platform, browser, os, device_type

**Project Management** (4 tags):
- release, sprint, epic, feature

**Compliance/Security** (3 tags):
- data_classification, compliance_requirement, security_level

**Localization/Regional** (4 tags):
- region, language, locale, timezone

**Integration/Dependency** (3 tags):
- integration_point, api_version, dependency

## Current Implementation Status

### Database Schema (Completed)
**Models Implemented:**
- **Tag**: Metadata categorization (category, value, description, is_predefined)
- **TestCase**: Core test scenario entity with status tracking, priority, audit fields
- **Project**: Organizational unit for test execution with timeline tracking
- **Association Tables**: testcase_tags and project_testcases for many-to-many relationships

**Database Migrations:**
- Alembic configured for async SQLAlchemy migrations
- Initial migration: Tag model
- Second migration: TestCase, Project models with associations
- All tables include created_at/updated_at timestamps
- Proper indexes on frequently queried fields (status, priority, title, category)
- CASCADE delete for referential integrity

**Data Seeding:**
- Seed script for 182 predefined tags across 40 categories
- Example values provided for each tag category
- Clear and re-seed functionality available

### Project Structure
```
tcm/
├── src/tcm/              # Application code
│   ├── models/           # SQLAlchemy models (Tag, TestCase, Project, associations)
│   ├── routes/           # API routes (empty, ready for implementation)
│   ├── pages/            # FastHTML pages (empty, ready for implementation)
│   ├── schemas/          # Pydantic schemas (empty, ready for implementation)
│   ├── config.py         # Application configuration
│   ├── database.py       # Database connection setup
│   └── main.py           # FastAPI application entry point
├── alembic/              # Database migrations
│   ├── versions/         # Migration files
│   └── env.py            # Alembic async configuration
├── scripts/              # Utility scripts
│   └── seed_tags.py      # Tag seeding script
├── tests/                # Test suite (unit, integration, e2e)
├── docker-compose.yml    # Docker stack (app, postgres, pgadmin)
└── pyproject.toml        # Project dependencies
```

### API Implementation (Completed)

**Pydantic Schemas:**
- Tag, TestCase, and Project schemas for request/response validation
- Separate Create, Update, and Response schemas for each entity
- List response schemas with pagination support

**REST API Endpoints:**

All endpoints follow RESTful conventions and are prefixed with `/api`:

- **Tag Endpoints** (`/api/tags`):
  - Full CRUD operations
  - List with pagination and category filtering
  - Get unique tag categories
  - Duplicate detection on create/update

- **TestCase Endpoints** (`/api/testcases`):
  - Full CRUD operations
  - List with filtering by status, priority, and tag
  - Tag management (add/remove tags)
  - Eager loading of tag relationships

- **Project Endpoints** (`/api/projects`):
  - Full CRUD operations
  - List with status filtering
  - Test case management (add/remove test cases)
  - Get all test cases in a project

**Features:**
- Async SQLAlchemy with relationship loading
- Input validation with Pydantic
- Error handling (404, 400 status codes)
- Pagination support
- Auto-generated API documentation at `/docs`

### Testing Implementation (Completed)

**Test Infrastructure:**
- pytest with async support (pytest-asyncio)
- Test fixtures for database sessions and HTTP client
- File-based SQLite for test isolation
- Comprehensive test coverage for all API endpoints

**Integration Tests (52 tests):**

- **Tag API Tests** (13 tests):
  - CRUD operations
  - Duplicate detection
  - Pagination and filtering
  - Category listing

- **TestCase API Tests** (20 tests):
  - CRUD operations
  - Tag associations (add/remove)
  - Filtering by status, priority, and tags
  - Edge cases and error handling

- **Project API Tests** (20 tests):
  - CRUD operations
  - Test case associations (add/remove)
  - Status filtering
  - Relationship management

**Test Commands:**
- `uv run pytest` - Run all tests
- `uv run pytest tests/integration/` - Run integration tests
- `uv run pytest --cov=tcm` - Run with coverage report

### What's Next
- **FastHTML UI**: Build web interface for test case management
- **Authentication**: Add user authentication and authorization
- **Search & Filtering**: Implement advanced search and filtering UI
- **Unit Tests**: Add unit tests for models and business logic
- **E2E Tests**: Add end-to-end tests for critical user workflows
- **Bulk Operations**: Add endpoints for bulk create/update/delete

## Important Constraints
- Multi-tenant data access patterns must ensure proper isolation
- Search and filtering performance critical for large test case repositories
- Metadata taxonomy should be flexible and extensible

## External Dependencies
- **Package Manager**: uv (must be installed globally)
- **Database**: PostgreSQL database server
- **Python Packages** (managed via uv):
  - FastAPI (async web framework)
  - FastHTML (Python-based frontend framework)
  - SQLAlchemy (ORM)
  - Pydantic (data validation)
  - psycopg2 or asyncpg (PostgreSQL drivers)
  - pytest (testing framework)
- (Additional dependencies to be determined as project evolves)
