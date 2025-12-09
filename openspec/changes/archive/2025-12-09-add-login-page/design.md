# Design: User Login Page

**Change ID:** `add-login-page`

## Architecture

### Component Structure

```
src/tcm/
├── pages/
│   ├── __init__.py
│   ├── login.py         # Login page component
│   └── components/      # Reusable UI components
│       ├── __init__.py
│       ├── forms.py     # Form components
│       └── layout.py    # Layout components
├── routes/
│   └── auth.py          # Authentication routes (new)
└── main.py              # Update to include auth routes
```

### Technology Choices

**FastHTML for UI:**
- Server-side rendering with Python
- Built-in HTMX support for dynamic interactions
- Simple, maintainable component structure
- Consistent with project tech stack

**Form Handling:**
- HTML5 form validation for basic client-side checks
- FastAPI endpoint for form submission
- Flash messages for user feedback

### Page Flow

```
User -> /login -> Login Page (FastHTML)
         |
         v
    [Submit Form]
         |
         v
    POST /api/auth/login
         |
         +---> Success: Redirect to /dashboard
         |
         +---> Failure: Reload /login with error message
```

### Security Considerations

1. **CSRF Protection**: Use FastAPI's CSRF middleware
2. **Password Handling**: Never log or display passwords
3. **Rate Limiting**: Implement basic rate limiting on login endpoint (future)
4. **HTTPS Only**: Ensure login only works over HTTPS in production
5. **Failed Login Logging**: Log all failed login attempts with timestamp, username (sanitized), and IP address for security monitoring
6. **Session Timeout**: Configurable via environment variable (default: 3600 seconds)

### Styling Approach

- Use minimal CSS with CSS Grid/Flexbox for layout
- Responsive design (mobile-first)
- Accessible form elements (ARIA labels, semantic HTML)
- Consistent color scheme with rest of application

### Component Reusability

Create reusable FastHTML components:
- `InputField`: Text input with label and validation
- `SubmitButton`: Primary action button
- `ErrorMessage`: Error alert component
- `PageLayout`: Consistent page wrapper

## Data Flow

1. User visits `/login`
2. FastHTML renders login page with form
3. User enters credentials and submits
4. Form data sent to `POST /api/auth/login`
5. Backend validates credentials (placeholder for now)
6. On success: Set session cookie, redirect to dashboard
7. On failure: Return to login page with error message

## Error Handling

- Empty fields: Client-side validation prevents submission
- Invalid credentials: "Invalid username or password" (generic message)
- Server errors: "An error occurred. Please try again"
- Network errors: "Unable to connect. Check your connection"

## Future Considerations

This design sets the foundation for:
- **SSO Integration with Azure AD/Entra ID** (primary future goal)
- Session management and expiration handling
- Authorization checks on protected routes
- Enhanced audit logging and security monitoring

**Note:** User registration and password reset are intentionally excluded as these will be handled by Azure AD in the production SSO implementation.

## Testing Strategy

- Unit tests for form validation logic
- Integration tests for login flow
- E2E tests for user journey
- Security testing for common vulnerabilities

## Implementation Notes

- Start with a simple, working login page
- Add styling after functionality is confirmed
- Keep authentication logic separate from UI for testability
- Use environment variables for configuration:
  - `SESSION_SECRET`: Secret key for session signing
  - `SESSION_TIMEOUT`: Session timeout in seconds (default: 3600)
  - `LOG_FAILED_LOGINS`: Enable/disable failed login logging (default: true)
- Failed login attempts should be logged with:
  - Timestamp
  - Username (sanitized to prevent log injection)
  - IP address
  - User agent (optional)
  - Reason for failure (invalid username, invalid password, account locked, etc.)
