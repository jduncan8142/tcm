# Tasks: widen-testcase-edit-layout

## Implementation Tasks

- [x] 1. Update EditTestCasePage layout to full-width
  - File: `src/tcm/pages/testcases/edit.py`
  - Change outer container from `cls="container"` to `cls="container container-wide"`
  - Kept `form-card form-card-wide` wrapper for form styling consistency

- [x] 2. Add CSS for full-width form layout (if needed)
  - No CSS changes needed - existing styles work well with container-wide

- [x] 3. Run tests to verify no regressions
  - Execute: `uv run pytest tests/integration/test_testcase_pages.py -v`
  - All existing tests should pass
  - Verify edit page still renders correctly

- [x] 4. Manual verification
  - Layout now uses full width (1200px max) matching list and view pages
  - Form fields properly sized within the wider layout
  - Consistent with other full-width pages

## Dependencies
- Tasks 1-2 can be done together
- Task 3-4 depend on tasks 1-2 completing

## Verification
- Manual: Navigate to test case edit page and verify full-width layout
- Automated: Run `uv run pytest tests/integration/test_testcase_pages.py -v`
