# tcm

Test Case Management (TCM) is a web app for test case creation and tracking.

It uses projects as its primary organizational element and cases are created at a global level and tagged with meta data.

While custom meta data tags can be added as required, there are several predefined tags available

## Getting Started

### Prerequisites

- [Git](https://git-scm.com/downloads)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/jduncan8142/tcm.git
   cd tcm
   ```

2. **Configure environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env if you need to customize settings (optional for development)
   ```

3. **Start the Docker stack**
   ```bash
   docker-compose up -d
   ```

   This will start three services:
   - **TCM Application** - FastAPI + FastHTML web application
   - **PostgreSQL** - Database server
   - **pgAdmin** - Database management interface

4. **Verify services are running**
   ```bash
   docker-compose ps
   ```

   All services should show "Up" or "Up (healthy)" status.

### Accessing the Application

Once the Docker stack is running, you can access:

- **TCM Application**: http://localhost:8000
  - API Health Check: http://localhost:8000/health
  - API Documentation: http://localhost:8000/docs (FastAPI auto-generated)
  - API Base URL: http://localhost:8000/api

- **pgAdmin**: http://localhost:5050
  - Email: `admin@example.com`
  - Password: `admin`
  - To connect to PostgreSQL:
    - Host: `postgres`
    - Port: `5432`
    - Database: `tcm`
    - Username: `tcm`
    - Password: `tcm`

### API Endpoints

The API provides full CRUD operations for Tags, Test Cases, and Projects.

**Tags:**
- `GET /api/tags` - List all tags with pagination and filtering
- `GET /api/tags/categories` - Get unique tag categories
- `GET /api/tags/{id}` - Get specific tag
- `POST /api/tags` - Create new tag
- `PATCH /api/tags/{id}` - Update tag
- `DELETE /api/tags/{id}` - Delete tag

**Test Cases:**
- `GET /api/testcases` - List all test cases with filtering
- `GET /api/testcases/{id}` - Get specific test case
- `POST /api/testcases` - Create new test case
- `PATCH /api/testcases/{id}` - Update test case
- `DELETE /api/testcases/{id}` - Delete test case
- `POST /api/testcases/{id}/tags/{tag_id}` - Add tag to test case
- `DELETE /api/testcases/{id}/tags/{tag_id}` - Remove tag from test case

**Projects:**
- `GET /api/projects` - List all projects
- `GET /api/projects/{id}` - Get specific project
- `POST /api/projects` - Create new project
- `PATCH /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project
- `GET /api/projects/{id}/testcases` - Get test cases in project
- `POST /api/projects/{id}/testcases/{testcase_id}` - Add test case to project
- `DELETE /api/projects/{id}/testcases/{testcase_id}` - Remove test case from project

For detailed API documentation and interactive testing, visit http://localhost:8000/docs

### Development Workflow

```bash
# View application logs
docker-compose logs -f app

# View all service logs
docker-compose logs -f

# Restart services after code changes
docker-compose restart app

# Rebuild and restart (after dependency changes)
docker-compose up -d --build

# Stop all services
docker-compose down

# Stop and remove volumes (resets database)
docker-compose down -v
```

### Stopping the Application

```bash
# Stop services (keeps data)
docker-compose stop

# Stop and remove containers (keeps data volumes)
docker-compose down

# Stop and remove everything including data
docker-compose down -v
```

### Database Migrations

The project uses Alembic for database schema management. Migrations are configured to work with async SQLAlchemy.

```bash
# Check current migration version
uv run alembic current

# Apply all pending migrations
uv run alembic upgrade head

# Create a new migration (after modifying models)
uv run alembic revision --autogenerate -m "Description of changes"

# Rollback one migration
uv run alembic downgrade -1

# View migration history
uv run alembic history

# Rollback to specific version
uv run alembic downgrade <revision_id>
```

**Note:** Migrations are automatically applied when running inside Docker. For local development, you'll need to run migrations manually using `uv run alembic upgrade head`.

### Seeding Data

The project includes seed scripts to populate the database with predefined data.

**Seed Predefined Tags:**

```bash
# Seed all 40 predefined tag categories with example values
uv run python scripts/seed_tags.py

# Clear all tags and re-seed
uv run python scripts/seed_tags.py --clear
uv run python scripts/seed_tags.py
```

The seed script creates 182 predefined tags across 40 categories (organizational, system/technical, test-specific, platform/technology, project management, compliance/security, localization/regional, and integration/dependency).

### Running Tests

The project includes comprehensive integration tests for all API endpoints.

**Install Development Dependencies:**

```bash
# Install dev dependencies including pytest and testing libraries
uv sync --all-extras
```

**Run Tests:**

```bash
# Run all tests
uv run pytest

# Run only integration tests
uv run pytest tests/integration/

# Run tests with verbose output
uv run pytest -v

# Run tests with coverage report
uv run pytest --cov=tcm --cov-report=html

# Run specific test file
uv run pytest tests/integration/test_tags_api.py

# Run specific test
uv run pytest tests/integration/test_tags_api.py::TestTagsAPI::test_create_tag
```

**Test Coverage:**
- **52 integration tests** covering all CRUD operations
- Tag API (13 tests): Create, Read, Update, Delete, Categories, Filtering
- TestCase API (20 tests): CRUD, Tag management, Filtering
- Project API (20 tests): CRUD, Test case management, Filtering

## Default tags:

### Organizational
- organization
- business_unit
- customer
- vendor
- program
- squad
- owner

### System/Technical
- system
- process
- module
- server
- cloud_provider
- database
- protocol

### Test-Specific
- test_type
- test_level
- automation_status
- priority
- risk_level
- test_phase
- test_status
- maintenance_status

### Platform/Technology
- platform
- browser
- os
- device_type

### Project Management
- release
- sprint
- epic
- feature

### Compliance/Security
- data_classification
- compliance_requirement
- security_level

### Localization/Regional
- region
- language
- locale
- timezone

### Integration/Dependency
- integration_point
- api_version
- dependency
