# Proposal: widen-testcase-edit-layout

## Summary
Change the test case edit page from a centered card layout to a full-width layout, providing more space for editing content.

## Motivation
The test case edit page currently uses a centered card style (`form-card form-card-wide` with `max-width: 600px`) which constrains the editing area. Given that test cases have multiple textarea fields (description, preconditions, steps, expected results), a wider layout would improve usability by:
- Providing more horizontal space for viewing and editing text
- Reducing vertical scrolling
- Better utilizing available screen real estate
- Aligning with the full-width pattern used by list and view pages

## Current Behavior
- Edit page uses `cls="container"` (centered, narrower)
- Form wrapped in `cls="form-card form-card-wide"` (max-width: 600px)
- Results in a narrow, centered card for editing

## Proposed Solution
Change the layout to use the same full-width pattern as list/view pages:
- Use `cls="container container-wide"` (max-width: 1200px)
- Remove the `form-card` wrapper or adjust styling for full-width form
- Keep form fields and functionality unchanged

## Scope
- Single file modification: `src/tcm/pages/testcases/edit.py`
- Possible CSS adjustments if needed for full-width form styling
- Layout change only, no functional changes

## Impact
- **Low risk**: Layout/styling change with no functional impact
- **Improves UX**: More space for editing test case content
- **Consistency**: Aligns with other full-width pages (list, view)
