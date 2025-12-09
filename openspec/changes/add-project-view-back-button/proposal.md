# Proposal: add-project-view-back-button

## Summary
Add a "Back to Projects" button to the project details page (`/projects/{id}`) for consistent navigation back to the projects list, matching the navigation pattern already established in test case and tag pages.

## Motivation
Currently, the project details view page lacks a back button, while the test case view page and all edit pages include one. This creates an inconsistent user experience where users viewing project details must use the browser back button or manually navigate to the projects list.

## Current Behavior
- Test case view page (`/testcases/{id}`) has "Back to List" button in the page actions
- Test case edit page (`/testcases/{id}/edit`) has "Back to Test Cases" button in the 404 state
- Project edit page (`/projects/{id}/edit`) has "Back to Projects" button in the 404 state
- Tag edit page (`/tags/{id}/edit`) has "Back to Tags" button in the 404 state
- **Project view page (`/projects/{id}`) has NO back button**

## Proposed Solution
Add "Back to Projects" button to the project details page header alongside the existing Edit and Delete buttons.

## Scope
- Single file modification: `src/tcm/pages/projects/view.py`
- Add one `ActionButton` component call
- Update existing integration tests if needed

## Impact
- **Low risk**: Additive change with no breaking modifications
- **Improves UX**: Consistent navigation across all detail/view pages
- **Minimal code change**: ~1-2 lines of code

## Related Spec
Modifies existing spec: `project-pages`
