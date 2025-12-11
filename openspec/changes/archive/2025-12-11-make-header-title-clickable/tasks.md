# Implementation Tasks

## 1. Update PageLayout Component
- [x] **File**: `src/tcm/pages/components/layout.py`
- [x] **Action**: Wrap the H1 header title in an anchor tag linking to `/dashboard`
- [x] **Details**:
  - Change line 38 from `H1("Test Case Management")` to wrap it in an `A` tag
  - Add `href="/dashboard"` to the anchor tag
  - Add a CSS class like "header-title-link" for styling
  - Maintain the H1 semantic structure

## 2. Add CSS Styles for Header Link
- [x] **File**: `src/tcm/static/css/styles.css`
- [x] **Action**: Add styles for the clickable header title link
- [x] **Details**:
  - Remove default link styling (color, underline)
  - Maintain current header title appearance
  - Add subtle hover effect (e.g., slight color change, opacity change)
  - Add focus styles for keyboard navigation
  - Ensure visited link colors don't change the appearance

## 3. Create Page Layout Tests
- [x] **File**: `tests/integration/test_page_layout.py` (new file)
- [x] **Action**: Create tests to verify header title link functionality
- [x] **Details**:
  - Test that header contains a link to `/dashboard`
  - Test that the link contains "Test Case Management" text
  - Test that the link is present on multiple pages (dashboard, testcases, projects, tags)
  - Verify the link has the correct CSS class

## 4. Run Existing Tests
- [x] **Action**: Verify no regressions in existing page tests
- [x] **Details**:
  - Run full test suite to ensure header change doesn't break anything
  - Pay special attention to page rendering tests
  - Verify all pages still display correctly

## 5. Manual Testing
- [ ] **Action**: Verify the feature works as expected in the browser
- [ ] **Details**:
  - Navigate to various pages and verify header title is clickable
  - Click header title and verify navigation to dashboard
  - Test hover effects display correctly
  - Test keyboard navigation (Tab to title, Enter to navigate)
  - Verify appearance matches original design
  - Check responsive behavior on mobile devices

## Dependencies
- Tasks 1 and 2 can be done in parallel or sequential order
- Task 3 (tests) depends on task 1 being complete
- Task 4 (existing tests) depends on tasks 1-2 being complete
- Task 5 (manual testing) depends on all previous tasks

## Validation
After implementation:
- Run test suite: `uv run pytest tests/integration/test_page_layout.py`
- Run full test suite: `uv run pytest tests/integration/`
- Verify all tests pass
- Manually test in browser for UX verification
