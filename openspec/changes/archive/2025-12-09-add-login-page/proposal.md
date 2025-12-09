# Proposal: Add User Login Page

**Change ID:** `add-login-page`
**Status:** Proposed
**Created:** 2025-12-08

## Overview

Add a user login page to the TCM application using FastHTML, providing the foundation for user authentication and session management. This is the first step toward implementing authentication and authorization across the application.

## Motivation

Currently, the TCM application has a fully functional API backend but no user authentication mechanism. To secure the application and enable multi-user access with proper authorization, we need to implement a login system. This change introduces the login UI page as the entry point for authenticated users.

## Goals

1. Create a login page UI using FastHTML that matches the application's design
2. Implement basic form validation on the client side
3. Provide clear feedback for login attempts (success/error states)
4. Lay the groundwork for session management and authentication flow
5. Follow best practices for secure credential handling

## Non-Goals

- Implementing the full authentication backend (session storage, password hashing, JWT, etc.)
- User registration/signup functionality
- Password reset functionality (handled by Azure AD in production)
- Multi-factor authentication (MFA)
- "Remember Me" functionality (not needed with SSO)
- Full OAuth/SSO integration with Azure AD/Entra ID (separate future proposal)

These features will be addressed in separate proposals once the basic login page is established. The end goal is to implement SSO with Azure AD and Entra ID, so this login page serves as an interim solution and development foundation.

## Scope

This change introduces one new capability:
- **user-authentication**: User login page and form handling

## Dependencies

- FastHTML for server-side rendering
- FastAPI for backend routing
- Existing TCM application structure

## Success Criteria

- [ ] Login page is accessible at `/login`
- [ ] Form includes username and password fields
- [ ] Form validation prevents empty submissions
- [ ] Login page follows consistent styling with the application
- [ ] Error messages are displayed clearly to users
- [ ] Page is responsive and works on mobile devices

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Security vulnerabilities in login form | Follow OWASP guidelines, implement CSRF protection |
| Poor user experience | Use clear error messages, proper form validation |
| Inconsistent styling | Create reusable FastHTML components |

## Alternatives Considered

1. **Third-party authentication service (Auth0, Clerk)**: Decided against for now to maintain control and reduce external dependencies
2. **Single-page app with React/Vue**: Rejected in favor of FastHTML to maintain Python-only stack
3. **Basic HTTP authentication**: Too simplistic for a production application

## Open Questions - RESOLVED

1. **Should we implement "Remember Me" functionality in this initial version?**
   - **Answer:** No. The end goal is to implement SSO with Azure AD and Entra ID, so "Remember Me" is not needed.

2. **What should be the session timeout duration?**
   - **Answer:** Add session timeout as a configurable variable in the `.env` file with a default value of 3600 seconds (1 hour).

3. **Should we log failed login attempts for security monitoring?**
   - **Answer:** Yes. Implement logging for failed login attempts to monitor security and identify potential attacks.
