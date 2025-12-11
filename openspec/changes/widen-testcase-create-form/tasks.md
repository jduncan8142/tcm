# Tasks: Widen Test Case Create Form

## Implementation Tasks

### Task 1: Update Create Page Container Class
- **File**: `src/tcm/pages/testcases/create.py`
- **Actions**:
  - Change line 184 from `cls="container"` to `cls="container container-wide"`
  - Verify the form now uses the wider layout (1200px max-width)
- **Dependencies**: None
- **Acceptance**: Create page uses `container-wide` class like edit page

### Task 2: Update Test to Verify Container Class
- **File**: `tests/integration/test_testcase_pages.py`
- **Actions**:
  - Find test for create page rendering
  - Add assertion to verify `container-wide` class is present in the HTML
  - Verify the class appears in the rendered page output
- **Dependencies**: Task 1
- **Acceptance**: Test verifies container-wide class is used

### Task 3: Manual Testing
- **Actions**:
  - Start development server
  - Navigate to `/testcases/new`
  - Verify form is wider and more comfortable to use
  - Test on desktop (form should be max 1200px wide)
  - Test on tablet (form should be responsive)
  - Test on mobile (form should be 100% width)
  - Verify all form fields are properly aligned and usable
- **Dependencies**: Task 1
- **Acceptance**: Form displays correctly on all device sizes

### Task 4: Run Full Test Suite
- **Actions**:
  - Execute: `uv run pytest tests/`
  - Verify all tests pass
  - Verify no regressions in other test case pages
- **Dependencies**: Task 2
- **Acceptance**: All tests pass, no regressions

## Task Summary

- **Total Tasks**: 4
- **Estimated Complexity**: Low (single line code change + test update)
- **Critical Path**: Task 1 → Task 2 → Task 4
- **Testing**: Manual testing (Task 3) can be done in parallel with Task 2
