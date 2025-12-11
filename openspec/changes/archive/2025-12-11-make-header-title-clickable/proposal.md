# Proposal: Make Header Title Clickable

## Summary
Make the "Test Case Management" title in the site header clickable, linking to the dashboard page at `/dashboard`. This provides a consistent navigation pattern found in most web applications where clicking the site logo or title returns users to the home/dashboard page.

## Motivation
Currently, the site header displays "Test Case Management" as plain text. Users cannot click it to navigate anywhere. Web application conventions establish that the header title/logo should be a clickable link to the application's main page (dashboard). This enhancement improves:
- **Navigation consistency**: Follows standard web UX patterns
- **User efficiency**: Provides a quick way to return to dashboard from any page
- **Discoverability**: Makes navigation more intuitive

## Scope
This change:
- Creates a new `page-layout` specification for shared layout components
- Modifies the PageLayout component to wrap the header title in a link
- Adds CSS styling to maintain visual appearance while adding link functionality
- Updates tests to verify the header link is present

## Impact
- **User Experience**: Improved navigation with standard clickable header
- **Code Changes**: Minimal - only affects the PageLayout component
- **Testing**: Requires new tests for header link functionality
- **Specifications**: Creates new page-layout spec for future layout-related requirements

## Dependencies
None - this is a self-contained enhancement to the shared layout component.

## Alternatives Considered
1. **Add a separate "Home" navigation link**: More cluttered, duplicates functionality
2. **Use a logo image instead of text**: Would require design assets and more significant changes
3. **Keep current design**: Violates common UX patterns, less intuitive

The chosen approach (clickable header title) is the most common and expected pattern in web applications.
