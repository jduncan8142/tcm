# Change: Add Dark Theme Support

## Why
The application currently only supports a light theme. Users working in low-light environments or those with light sensitivity would benefit from a dark theme option. Modern web applications are expected to provide theme customization as a standard feature for improved user comfort and accessibility.

## What Changes
- **User Model**: Create new User database model with authentication fields (username, email, hashed_password) and theme_preference field (defaults to "light")
- **Database Migration**: Add users table with Alembic migration, migrate placeholder users to database
- **Authentication**: Update auth routes to use User model, store theme preference in session on login
- **Theme API**: New POST endpoint `/api/user/theme` to update user's theme preference
- **CSS Themes**: Add CSS custom properties for light theme (Flatly-inspired) and dark theme (Darkly-inspired)
- **Theme Toggle**: Add button in header (right-aligned) showing 🌙 for light mode, ☀️ for dark mode
- **JavaScript**: Client-side theme switching without page reload, with server-side persistence
- **Layout Updates**: Apply data-theme attribute to HTML element based on session value

## Impact
- **Affected specs**: page-layout (ADDED theme toggle and theme application requirements), user-authentication (NEW spec with 5 requirements)
- **Affected code**:
  - New: `src/tcm/db/models/user.py`, `src/tcm/static/js/theme.js`, `alembic/versions/XXXX_add_users_table.py`
  - Modified: `src/tcm/routes/auth.py`, `src/tcm/pages/components/layout.py`, `src/tcm/static/css/styles.css`, `src/tcm/db/models/__init__.py`
  - Tests: New test files for user model, theme API, and theme rendering
- **Dependencies**:
  - **BREAKING**: Requires User model creation (doesn't exist yet)
  - **BREAKING**: Changes authentication from placeholder users to database users
  - Database migration required before deployment
- **Migration**: Placeholder users (admin, user) will be migrated to database with default light theme
- **Default behavior**: New and existing users default to light theme for consistency
