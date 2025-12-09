# Tasks: link-testcase-titles-in-project-view

## Implementation Tasks

- [ ] 1. Update TestCaseRow to render title as hyperlink
  - File: `src/tcm/pages/projects/view.py`
  - Change `Td(testcase.get("title", ""))` to `Td(A(testcase.get("title", ""), href=f"/testcases/{testcase['id']}", cls="testcase-link"))`
  - Located in the `TestCaseRow()` function

- [ ] 2. Add integration test for test case title hyperlink
  - File: `tests/integration/test_project_pages.py`
  - Add test to verify test case titles are rendered as hyperlinks
  - Verify links point to correct `/testcases/{id}` URLs

- [ ] 3. Run tests to verify no regressions
  - Execute: `uv run pytest tests/integration/test_project_pages.py -v`
  - All existing tests should pass
  - New hyperlink test should pass

## Dependencies
- Tasks 1-2 can be done in parallel
- Task 3 depends on tasks 1-2 completing

## Verification
- Manual: Navigate to a project with test cases and verify titles are clickable links to test case details
- Automated: Run `uv run pytest tests/integration/test_project_pages.py -v`
