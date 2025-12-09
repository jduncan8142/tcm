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
│   ├── routes/           # API and page routes
│   │   ├── tags.py           # Tag API endpoints
│   │   ├── testcases.py      # TestCase API endpoints
│   │   ├── projects.py       # Project API endpoints
│   │   ├── auth.py           # Authentication routes
│   │   ├── tag_pages.py      # Tag management UI pages
│   │   ├── testcase_pages.py # TestCase management UI pages
│   │   └── project_pages.py  # Project management UI pages
│   ├── pages/            # FastHTML pages
│   │   ├── components/   # Reusable FastHTML components (layout, forms)
│   │   ├── tags/         # Tag pages (list, create, edit)
│   │   ├── testcases/    # TestCase pages (list, create, edit, view)
│   │   ├── projects/     # Project pages (list, create, edit, view)
│   │   └── login.py      # Login page
│   ├── schemas/          # Pydantic schemas (Tag, TestCase, Project)
│   ├── static/           # Static assets
│   │   └── css/          # Stylesheets
│   ├── config.py         # Application configuration
│   ├── database.py       # Database connection setup
│   └── main.py           # FastAPI application entry point
├── alembic/              # Database migrations
│   ├── versions/         # Migration files
│   └── env.py            # Alembic async configuration
├── scripts/              # Utility scripts
│   └── seed_tags.py      # Tag seeding script
├── tests/                # Test suite (unit, integration, e2e)
│   └── integration/      # Integration tests (auth, tags, testcases, projects, pages)
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

**Integration Tests (149 tests):**

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

- **Authentication Tests** (10 tests):
  - Login page rendering
  - Valid/invalid credentials
  - Session management
  - Logout functionality
  - Cookie security properties

- **Tag Pages Tests** (24 tests):
  - List, create, edit page functionality
  - Form validation and duplicate detection
  - Category filtering and grouping

- **TestCase Pages Tests** (33 tests):
  - List, create, edit, view page functionality
  - Search and filtering (status, priority, tags)
  - Pagination and tag management

- **Project Pages Tests** (30 tests):
  - List, create, edit, view page functionality
  - Test case assignment/removal
  - Date validation and status filtering

**Test Commands:**
- `uv run pytest` - Run all tests
- `uv run pytest tests/integration/` - Run integration tests
- `uv run pytest --cov=tcm` - Run with coverage report

### Authentication Implementation (Completed)

**Login Page & UI Components:**
- FastHTML-based login page with form validation
- Reusable UI components (PageLayout, InputField, SubmitButton, ErrorMessage)
- Responsive CSS styling with mobile-first design
- Dashboard placeholder page (post-login)

**Authentication Routes:**
- `GET /login` - Render login page
- `POST /api/auth/login` - Handle login submission with validation
- `GET /api/auth/logout` - Clear session and redirect
- `GET /dashboard` - Protected dashboard page

**Security Features:**
- Session-based authentication with HTTP-only cookies
- Failed login logging with timestamp, IP, username, and user agent
- Log injection prevention (username sanitization)
- Configurable session timeout via environment variables
- SameSite cookie protection
- Placeholder user database (admin/test users for development)

**Configuration:**
- `SESSION_SECRET` - Secret key for session signing
- `SESSION_TIMEOUT` - Session timeout in seconds (default: 3600)
- `LOG_FAILED_LOGINS` - Enable/disable failed login logging (default: true)

**Future Integration:**
- Azure AD / Entra ID SSO (planned)
- Current implementation serves as interim authentication solution

### FastHTML UI Implementation (Completed)

**Tag Management Pages** (`/tags`):
- List page with category grouping and filtering
- Create page with category dropdown (supports new categories)
- Edit page with pre-populated form
- Delete with JavaScript confirmation
- Visual distinction between predefined and custom tags

**Test Case Management Pages** (`/testcases`):
- List page with search, filtering (status, priority, tags), and pagination
- Create page with all fields and multi-select tag assignment
- Edit page with tag management
- View page showing tags, projects, and audit trail
- Delete with JavaScript confirmation

**Project Management Pages** (`/projects`):
- List page with status filtering
- Create page with date pickers and validation
- Edit page with pre-populated form
- View page with test case management (add/remove via modal)
- Delete with JavaScript confirmation

**Reusable UI Components** (`src/tcm/pages/components/`):
- PageLayout - Consistent page structure with header/footer
- InputField, TextAreaField, SelectField - Form inputs
- CheckboxField - Checkbox with label
- SubmitButton, ActionButton - Button components
- TagBadge - Visual tag display
- CategoryGroup - Collapsible category sections
- ErrorMessage, SuccessMessage - Alert components

### What's Next
- **Unit Tests**: Add unit tests for models and business logic
- **E2E Tests**: Add end-to-end tests for critical user workflows
- **Bulk Operations**: Add endpoints for bulk create/update/delete
- **Azure AD Integration**: Replace placeholder auth with SSO
- **Enhanced Dashboard**: Replace placeholder with statistics and activity feed
- **Global Search**: Search across test cases, projects, and tags

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
