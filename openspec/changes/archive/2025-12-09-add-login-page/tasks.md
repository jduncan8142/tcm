# Tasks: Add User Login Page

**Change ID:** `add-login-page`

## Implementation Checklist

### Phase 1: Foundation Setup
- [x] Create `src/tcm/pages/` directory structure
- [x] Create `src/tcm/pages/components/` for reusable components
- [x] Create `src/tcm/routes/auth.py` for authentication routes
- [x] Add basic CSS file for styling (or update existing styles)
- [x] Update `.env.example` with authentication configuration variables:
  - `SESSION_SECRET` (placeholder value)
  - `SESSION_TIMEOUT` (default: 3600)
  - `LOG_FAILED_LOGINS` (default: true)
- [x] Add logging configuration for authentication events

### Phase 2: Reusable Components
- [x] Create `PageLayout` component for consistent page structure
  - Header, main content area, footer
  - Responsive container
- [x] Create `InputField` component
  - Label, input field, error message slot
  - Support for different input types (text, password, email)
- [x] Create `SubmitButton` component
  - Primary button styling
  - Loading state support
- [x] Create `ErrorMessage` component
  - Alert/notification styling
  - Dismissible option

### Phase 3: Login Page Implementation
- [x] Create `src/tcm/pages/login.py` with login page component
  - Use PageLayout for structure
  - Login form with username and password fields
  - Client-side validation (HTML5 required attributes)
  - CSRF token integration
- [x] Add login page route in `src/tcm/routes/auth.py`
  - GET /login - Render login page
  - POST /api/auth/login - Handle login submission (placeholder)
- [x] Implement session management
  - Read `SESSION_TIMEOUT` from environment variables
  - Configure session expiration
  - Set secure session cookies
- [x] Implement failed login logging
  - Log timestamp, username (sanitized), IP address
  - Read `LOG_FAILED_LOGINS` from environment variables
  - Sanitize all logged data to prevent injection
- [x] Implement basic error handling and flash messages
- [x] Add redirect logic (if already logged in, redirect to dashboard)

### Phase 4: Styling and UX
- [x] Style login page components
  - Centered form on page
  - Professional, clean design
  - Proper spacing and typography
- [x] Make page responsive (mobile, tablet, desktop)
- [x] Add loading indicator for form submission
- [x] Test keyboard navigation and accessibility

### Phase 5: Integration
- [x] Register auth routes in `src/tcm/main.py`
- [x] Create placeholder `/dashboard` route for post-login redirect
- [x] Add navigation link to login page (if applicable)
- [x] Test full flow: visit login → submit form → see response

### Phase 6: Testing
- [x] Write unit tests for login page components
- [x] Write integration tests for auth routes
  - GET /login returns 200 with form
  - POST /api/auth/login with valid data (placeholder response)
  - POST /api/auth/login with invalid data returns error
- [x] Write E2E test for login flow
- [x] Test error scenarios (network failure, invalid input)

### Phase 7: Documentation
- [x] Update README.md with login page information
- [x] Document authentication flow in project.md
- [x] Add code comments for complex logic
- [x] Update API documentation if needed

## Validation Criteria

Each task must meet these criteria before being marked complete:
- Code follows project conventions (PEP 8, type hints)
- All new code has appropriate docstrings
- Tests pass for the implemented functionality
- No regressions in existing functionality
- Code reviewed (if applicable)

## Dependencies Between Tasks

- Phase 2 must complete before Phase 3 (components used in page)
- Phase 3 must complete before Phase 4 (can't style what doesn't exist)
- Phase 5 depends on Phase 3 (integration requires routes)
- Phase 6 can run in parallel with Phase 4-5 (testing as we go)

## Estimated Complexity

- **Small tasks**: Foundation setup, reusable components
- **Medium tasks**: Login page implementation, styling
- **Large tasks**: Full integration, comprehensive testing

Total estimated effort: 1-2 days for experienced FastHTML developer
