# Design: Add Dark Theme Support

## Overview
This document outlines the architectural decisions and design approach for implementing dark theme support in the Test Case Management application.

## Architecture

### User Model Design
Since no User model currently exists, we need to create one:

```python
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    theme_preference: Mapped[str] = mapped_column(String(10), default="light", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**Design Decisions:**
- `theme_preference` stored as string ("light" or "dark") for simplicity and extensibility
- Default value "light" at database level ensures consistent behavior
- Field is nullable=False to avoid null handling complexity
- Could be extended to Enum type in future if more themes are added

### Theme Storage Strategy

**Database-First Approach:**
1. User theme preference stored in PostgreSQL `users.theme_preference` field
2. Retrieved on login and stored in session
3. Session value used to determine theme on each page load
4. Updated via API endpoint when user toggles theme

**Flow:**
```
Login → Load user.theme_preference → Store in session
         ↓
Page Request → Read theme from session → Apply to HTML
         ↓
Theme Toggle → API call updates DB → Update session → Return success
         ↓
JavaScript → Toggle CSS classes → Instant visual update
```

**Advantages:**
- Persists across devices and browsers
- No client-side storage sync issues
- Single source of truth in database
- Works with server-side rendering

### CSS Architecture

**Custom Properties Strategy:**
We'll use CSS custom properties (variables) to enable instant theme switching:

```css
/* Light theme (Flatly-inspired) */
:root, [data-theme="light"] {
    --bg-primary: #ffffff;
    --bg-secondary: #ecf0f1;
    --text-primary: #2c3e50;
    --text-secondary: #7b8a8b;
    --primary-color: #2c3e50;
    --accent-color: #18bc9c;
    --border-color: #bdc3c7;
    --header-bg: #2c3e50;
    --header-text: #ffffff;
}

/* Dark theme (Darkly-inspired) */
[data-theme="dark"] {
    --bg-primary: #222222;
    --bg-secondary: #303030;
    --text-primary: #ffffff;
    --text-secondary: #adb5bd;
    --primary-color: #375a7f;
    --accent-color: #00bc8c;
    --border-color: #444444;
    --header-bg: #375a7f;
    --header-text: #ffffff;
}
```

**Color Mappings:**

**Flatly Theme (Light):**
- Background: #ffffff (white)
- Secondary: #ecf0f1 (light gray)
- Text: #2c3e50 (dark blue-gray)
- Primary: #2c3e50 (dark blue-gray)
- Success/Accent: #18bc9c (turquoise)

**Darkly Theme (Dark):**
- Background: #222222 (dark gray)
- Secondary: #303030 (darker gray)
- Text: #ffffff (white)
- Primary: #375a7f (muted blue)
- Success/Accent: #00bc8c (teal)

### Component Interactions

**Server-Side Flow:**
1. **Authentication Layer** (`src/tcm/routes/auth.py`):
   - Load user from database on login
   - Store theme_preference in session: `request.session["theme"] = user.theme_preference`
   - Default to "light" if no user or no preference

2. **Layout Component** (`src/tcm/pages/components/layout.py`):
   - Read theme from session: `theme = request.session.get("theme", "light")`
   - Apply to HTML element: `<html data-theme="{theme}">`
   - Render theme toggle button with correct icon

3. **Theme Toggle Button**:
   - Positioned in header, right-aligned
   - Icon based on current theme: 🌙 (moon) for light mode, ☀️ (sun) for dark mode
   - Click triggers JavaScript function

4. **API Endpoint** (`/api/user/theme`):
   - POST endpoint to update theme preference
   - Validates theme value ("light" or "dark")
   - Updates database and session
   - Returns success/error response

**Client-Side Flow:**
1. **JavaScript Theme Toggle**:
```javascript
async function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';

    // Update UI immediately
    html.setAttribute('data-theme', newTheme);
    updateThemeIcon(newTheme);

    // Persist to server
    try {
        await fetch('/api/user/theme', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ theme: newTheme })
        });
    } catch (error) {
        console.error('Failed to save theme preference:', error);
        // Revert on error
        html.setAttribute('data-theme', currentTheme);
        updateThemeIcon(currentTheme);
    }
}
```

### Rendering Decisions

**Server-Side Rendering (SSR):**
- Initial page load renders with correct theme from session
- No flash of unstyled content (FOUC)
- Works without JavaScript enabled (theme persists, toggle disabled)

**Client-Side Enhancement:**
- JavaScript toggles theme instantly without page reload
- Better user experience (no loading delay)
- Handles API errors gracefully

**Progressive Enhancement:**
- Base functionality works server-side only
- JavaScript enhances UX when available
- Graceful degradation if JavaScript fails

### Database Migration Strategy

**Migration Steps:**
1. Create User table with all authentication fields
2. Migrate existing placeholder users to database users
3. Set all existing users to "light" theme (default)
4. Update authentication flow to use database users
5. Add foreign keys from existing tables (testcases, projects, tags) if needed

**Migration Considerations:**
- Current auth uses hardcoded users ("admin", "user")
- Need to hash existing passwords and migrate to database
- Session structure may need updates to store user_id instead of username
- Backwards compatibility not critical (early development phase)

**Alembic Migration:**
```python
def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(100), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('theme_preference', sa.String(10), nullable=False, server_default='light'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )

    # Migrate placeholder users
    # ... (handled in separate data migration)

def downgrade():
    op.drop_table('users')
```

## Technical Considerations

### Performance
- CSS custom properties have negligible performance impact
- Theme toggle is instant (no re-render required)
- Single API call per theme change (not per page load)
- Database query on login only (cached in session)

### Accessibility
- Sun/moon icons are decorative (button has text alternative)
- Color contrast ratios verified for both themes
- Keyboard navigation supported (button is focusable)
- Screen readers announce theme change

### Security
- Theme preference is user-specific (no security implications)
- API endpoint requires authentication
- Input validation prevents invalid theme values
- SQL injection prevented by SQLAlchemy parameterization

### Browser Compatibility
- CSS custom properties supported in all modern browsers
- `data-theme` attribute universally supported
- Fetch API has broad support (fallback not needed for admin tool)
- Progressive enhancement ensures core functionality works everywhere

## File Changes

### New Files
- `src/tcm/db/models/user.py` - User model definition
- `src/tcm/static/js/theme.js` - Theme toggle JavaScript
- `alembic/versions/XXXX_add_users_table.py` - Database migration

### Modified Files
- `src/tcm/routes/auth.py` - Update authentication to use User model
- `src/tcm/pages/components/layout.py` - Add theme toggle button, apply theme
- `src/tcm/static/css/styles.css` - Add theme variables and dark theme styles
- `src/tcm/db/models/__init__.py` - Export User model

## Future Enhancements

**Not in Scope for This Change:**
- System theme detection (prefers-color-scheme media query)
- Multiple theme options beyond light/dark
- Per-page theme customization
- Theme preview before applying
- Scheduled theme switching (auto-dark at night)

These can be considered in future OpenSpec proposals if needed.

## Risks and Mitigations

**Risk 1: User Model Doesn't Exist**
- **Impact**: High - entire feature depends on it
- **Mitigation**: Create User model as first task, comprehensive testing
- **Fallback**: Use localStorage-only approach (doesn't meet requirements)

**Risk 2: Breaking Existing Authentication**
- **Impact**: High - users can't log in
- **Mitigation**: Thorough testing of auth flow, database migration validation
- **Fallback**: Keep placeholder auth temporarily, add theme to session only

**Risk 3: Theme Not Applying Consistently**
- **Impact**: Medium - poor UX
- **Mitigation**: Use data attribute on HTML element, test all pages
- **Fallback**: Force page reload on theme change (slower but reliable)

**Risk 4: Performance Impact on Page Load**
- **Impact**: Low - extra session read
- **Mitigation**: Session already accessed for auth, negligible overhead
- **Fallback**: Cache theme in memory (not needed based on performance testing)
