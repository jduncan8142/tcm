# Proposal: link-testcase-titles-in-project-view

## Summary
Make test case titles in the project details page clickable hyperlinks that navigate to the test case details page.

## Motivation
On the project details page (`/projects/{id}`), test cases are displayed in a table with Title, Status, Priority, and Actions columns. Currently, the test case title is plain text, requiring users to navigate away to find and view test case details. Making the title a hyperlink improves usability by providing direct navigation to test case details.

This follows the existing pattern where project names in the projects list page are already hyperlinks (see `list.py` line 67).

## Current Behavior
- **Project details page** (`/projects/{id}`): Test case titles displayed as plain text
- Users must manually navigate to `/testcases/{id}` to view test case details
- No direct link from project context to test case details

## Proposed Solution
Change the test case title cell in `TestCaseRow()` from:
```python
Td(testcase.get("title", ""))
```
To:
```python
Td(A(testcase.get("title", ""), href=f"/testcases/{testcase['id']}", cls="testcase-link"))
```

## Scope
- Single file modification: `src/tcm/pages/projects/view.py`
- One line change in the `TestCaseRow()` function
- Optional: CSS styling for `.testcase-link` class (may reuse existing link styles)

## Impact
- **Low risk**: Simple additive change with no breaking modifications
- **Improves UX**: Direct navigation from project to test case details
- **Minimal code change**: ~1 line of code
