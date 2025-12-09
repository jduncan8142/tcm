# Tasks: add-project-view-back-button

## Implementation Tasks

- [x] 1. Add "Back to Projects" button to project view page header
  - File: `src/tcm/pages/projects/view.py`
  - Add `ActionButton("Back to Projects", href="/projects", btn_type="secondary")` to the page actions div alongside Edit and Delete buttons
  - Match the pattern used in test case view page

- [x] 2. Add integration test for back button presence
  - File: `tests/integration/test_project_pages.py`
  - Add test case to verify the back button is rendered on the project details page
  - Verify the button links to `/projects`

- [x] 3. Update spec with back navigation requirement
  - File: `openspec/changes/add-project-view-back-button/specs/project-pages/spec.md`
  - Add scenario for back navigation to the "View Project Details Page" requirement

- [x] 4. Run tests to verify no regressions
  - Execute: `uv run pytest tests/integration/test_project_pages.py -v`
  - All existing tests should pass
  - New back button test should pass

## Dependencies
- Tasks 1-3 can be done in parallel
- Task 4 depends on tasks 1-2 completing

## Verification
- Manual: Navigate to any project details page and verify "Back to Projects" button is visible and works
- Automated: Run `uv run pytest tests/integration/test_project_pages.py -v`
