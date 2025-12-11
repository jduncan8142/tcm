# Tasks: Add Dark Theme Support

## Implementation Tasks

### Phase 1: Database and User Model (Foundation)

#### Task 1.1: Create User Model
- **File**: `src/tcm/db/models/user.py`
- **Actions**:
  - Create User SQLAlchemy model with fields: id, username, email, hashed_password, theme_preference, created_at, updated_at
  - Set theme_preference default to "light"
  - Add unique constraints on username and email
  - Add proper type hints using SQLAlchemy 2.0 style
- **Dependencies**: None
- **Acceptance**: Model defined and importable

#### Task 1.2: Export User Model
- **File**: `src/tcm/db/models/__init__.py`
- **Actions**:
  - Import User model
  - Add to __all__ list for public export
- **Dependencies**: Task 1.1
- **Acceptance**: `from src.tcm.db.models import User` works

#### Task 1.3: Create Database Migration
- **File**: `alembic/versions/XXXX_add_users_table.py`
- **Actions**:
  - Generate Alembic migration: `uv run alembic revision --autogenerate -m "Add users table with theme preference"`
  - Review and adjust generated migration
  - Ensure theme_preference has server_default='light'
  - Add data migration for placeholder users (admin, user)
- **Dependencies**: Task 1.1, Task 1.2
- **Acceptance**: Migration runs successfully with `uv run alembic upgrade head`

#### Task 1.4: Run Database Migration
- **Actions**:
  - Execute migration in development: `uv run alembic upgrade head`
  - Verify users table created with correct schema
  - Verify placeholder users migrated with default light theme
- **Dependencies**: Task 1.3
- **Acceptance**: Users table exists in database with expected structure

### Phase 2: Authentication Updates

#### Task 2.1: Update Authentication Routes
- **File**: `src/tcm/routes/auth.py`
- **Actions**:
  - Replace placeholder user logic with database User queries
  - Update login to fetch User from database
  - Store user.theme_preference in session: `request.session["theme"] = user.theme_preference`
  - Update password verification to use hashed_password
  - Maintain existing session structure for compatibility
- **Dependencies**: Task 1.4
- **Acceptance**: Login works, theme stored in session

#### Task 2.2: Add Theme API Endpoint
- **File**: `src/tcm/routes/auth.py` or new `src/tcm/routes/user.py`
- **Actions**:
  - Create POST endpoint `/api/user/theme`
  - Require authentication (check session)
  - Accept JSON body with `theme` field
  - Validate theme is "light" or "dark"
  - Update user.theme_preference in database
  - Update session theme value
  - Return success response or 400/401 errors
- **Dependencies**: Task 2.1
- **Acceptance**: API endpoint updates theme in database and session

### Phase 3: CSS Theme Implementation

#### Task 3.1: Add CSS Custom Properties for Light Theme
- **File**: `src/tcm/static/css/styles.css`
- **Actions**:
  - Define :root and [data-theme="light"] selectors with Flatly-inspired colors
  - Add variables: --bg-primary, --bg-secondary, --text-primary, --text-secondary, --primary-color, --accent-color, --border-color, --header-bg, --header-text
  - Map existing color values to new variables
- **Dependencies**: None
- **Acceptance**: Light theme colors defined as CSS variables

#### Task 3.2: Add CSS Custom Properties for Dark Theme
- **File**: `src/tcm/static/css/styles.css`
- **Actions**:
  - Define [data-theme="dark"] selector with Darkly-inspired colors
  - Use same variable names as light theme
  - Dark theme colors: backgrounds (#222, #303030), text (#fff, #adb5bd), primary (#375a7f), accent (#00bc8c)
- **Dependencies**: Task 3.1
- **Acceptance**: Dark theme colors defined as CSS variables

#### Task 3.3: Update Existing Styles to Use Variables
- **File**: `src/tcm/static/css/styles.css`
- **Actions**:
  - Replace hardcoded colors with var() references
  - Update body, headers, links, borders, backgrounds
  - Update component-specific styles (cards, forms, tables, buttons)
  - Test both themes render correctly
- **Dependencies**: Task 3.1, Task 3.2
- **Acceptance**: All UI elements respond to theme changes

#### Task 3.4: Style Theme Toggle Button
- **File**: `src/tcm/static/css/styles.css`
- **Actions**:
  - Add .theme-toggle-button styles
  - Position in header (right side)
  - Style as icon button with hover state
  - Ensure accessible (focus visible, cursor pointer)
  - Responsive on mobile
- **Dependencies**: None
- **Acceptance**: Theme toggle button styled and positioned correctly

### Phase 4: Layout Component Updates

#### Task 4.1: Update PageLayout to Apply Theme
- **File**: `src/tcm/pages/components/layout.py`
- **Actions**:
  - Read theme from request.session.get("theme", "light")
  - Apply data-theme attribute to Html element
  - Pass theme value to child components
- **Dependencies**: Task 2.1
- **Acceptance**: HTML element has correct data-theme attribute

#### Task 4.2: Add Theme Toggle Button to Header
- **File**: `src/tcm/pages/components/layout.py`
- **Actions**:
  - Add button to header (right side)
  - Show 🌙 (moon) icon for light theme
  - Show ☀️ (sun) icon for dark theme
  - Add onclick handler: `toggleTheme()`
  - Add aria-label for accessibility
  - Add id="theme-toggle" for JavaScript targeting
- **Dependencies**: Task 4.1, Task 3.4
- **Acceptance**: Toggle button renders with correct icon based on current theme

### Phase 5: JavaScript Implementation

#### Task 5.1: Create Theme Toggle JavaScript
- **File**: `src/tcm/static/js/theme.js`
- **Actions**:
  - Create toggleTheme() function
  - Read current theme from data-theme attribute
  - Toggle to opposite theme
  - Update HTML data-theme attribute
  - Call updateThemeIcon()
  - POST to /api/user/theme endpoint
  - Handle API errors (revert theme on failure)
- **Dependencies**: Task 2.2
- **Acceptance**: Theme toggles instantly when button clicked

#### Task 5.2: Create Icon Update Function
- **File**: `src/tcm/static/js/theme.js`
- **Actions**:
  - Create updateThemeIcon(theme) function
  - Find button by id="theme-toggle"
  - Update button innerHTML to show correct icon
  - Light theme → 🌙 moon
  - Dark theme → ☀️ sun
- **Dependencies**: Task 5.1
- **Acceptance**: Icon updates immediately after theme toggle

#### Task 5.3: Include Theme JavaScript in Layout
- **File**: `src/tcm/pages/components/layout.py`
- **Actions**:
  - Add Script tag to include theme.js
  - Place in page footer (before closing body tag)
  - Ensure loaded on all pages using PageLayout
- **Dependencies**: Task 5.1, Task 5.2
- **Acceptance**: theme.js loaded and functional on all pages

### Phase 6: Testing

#### Task 6.1: Create User Model Tests
- **File**: `tests/unit/test_user_model.py`
- **Actions**:
  - Test User model creation
  - Test default theme is "light"
  - Test unique constraints on username and email
  - Test created_at and updated_at timestamps
- **Dependencies**: Task 1.1
- **Acceptance**: All user model tests pass

#### Task 6.2: Create Authentication Tests
- **File**: `tests/integration/test_auth_with_themes.py`
- **Actions**:
  - Test login sets theme in session
  - Test theme defaults to "light" for new users
  - Test theme API endpoint requires authentication
  - Test theme API validates input ("light" or "dark" only)
  - Test theme API updates database and session
  - Test invalid theme value returns 400
- **Dependencies**: Task 2.1, Task 2.2
- **Acceptance**: All authentication + theme tests pass

#### Task 6.3: Create Theme Rendering Tests
- **File**: `tests/integration/test_theme_rendering.py`
- **Actions**:
  - Test HTML has data-theme attribute
  - Test data-theme matches session theme
  - Test toggle button shows correct icon for light theme
  - Test toggle button shows correct icon for dark theme
  - Test theme persists across page navigation
- **Dependencies**: Task 4.1, Task 4.2
- **Acceptance**: All theme rendering tests pass

#### Task 6.4: Create Theme API Tests
- **File**: `tests/integration/test_theme_api.py`
- **Actions**:
  - Test POST /api/user/theme updates database
  - Test POST /api/user/theme updates session
  - Test unauthenticated request returns 401
  - Test invalid theme value returns 400
  - Test successful update returns 200
- **Dependencies**: Task 2.2
- **Acceptance**: All theme API tests pass

#### Task 6.5: Run Full Test Suite
- **Actions**:
  - Execute: `uv run pytest tests/`
  - Verify all existing tests still pass
  - Verify all new theme tests pass
  - Check coverage for new code
- **Dependencies**: All previous tasks
- **Acceptance**: All tests pass, no regressions

### Phase 7: Documentation and Cleanup

#### Task 7.1: Update Project Documentation
- **File**: `openspec/project.md`
- **Actions**:
  - Document User model in database section
  - Document theme preference feature
  - Update authentication section to reflect database users
- **Dependencies**: All implementation complete
- **Acceptance**: Project docs accurately reflect new functionality

#### Task 7.2: Manual Testing
- **Actions**:
  - Start development server
  - Test login flow with theme
  - Toggle between light and dark themes
  - Verify theme persists after logout/login
  - Test on different pages (dashboard, test cases, projects)
  - Test keyboard navigation to toggle button
  - Test mobile responsive layout
- **Dependencies**: All implementation complete
- **Acceptance**: Theme functionality works as expected in manual testing

## Task Summary

- **Total Tasks**: 23
- **Estimated Complexity**: High (new User model, authentication changes, full-stack feature)
- **Critical Path**: Phase 1 → Phase 2 → Phase 4 → Phase 5
- **Testing Coverage**: 5 test tasks across unit and integration tests

## Notes

- Tasks are ordered by dependency
- Phase 1 must complete before Phase 2
- Phase 3 (CSS) can be done in parallel with Phase 1-2
- Phase 5 (JavaScript) depends on Phase 2 (API endpoint)
- Testing should be done incrementally, not saved for the end
- Each task should include running relevant tests to ensure no regressions
