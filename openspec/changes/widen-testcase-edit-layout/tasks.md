# Tasks: widen-testcase-edit-layout

## Implementation Tasks

- [ ] 1. Update EditTestCasePage layout to full-width
  - File: `src/tcm/pages/testcases/edit.py`
  - Change outer container from `cls="container"` to `cls="container container-wide"`
  - Remove or modify `form-card form-card-wide` wrapper to allow full-width form
  - Consider adding page header section for consistency with list/view pages

- [ ] 2. Add CSS for full-width form layout (if needed)
  - File: `src/tcm/static/css/styles.css`
  - Add styles for wide form layout if existing styles don't suffice
  - Ensure form fields expand appropriately in wider layout

- [ ] 3. Run tests to verify no regressions
  - Execute: `uv run pytest tests/integration/test_testcase_pages.py -v`
  - All existing tests should pass
  - Verify edit page still renders correctly

- [ ] 4. Manual verification
  - Verify edit page uses full screen width
  - Verify form fields are properly sized
  - Test responsive behavior on different screen sizes

## Dependencies
- Tasks 1-2 can be done together
- Task 3-4 depend on tasks 1-2 completing

## Verification
- Manual: Navigate to test case edit page and verify full-width layout
- Automated: Run `uv run pytest tests/integration/test_testcase_pages.py -v`
