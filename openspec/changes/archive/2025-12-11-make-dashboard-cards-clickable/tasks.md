# Implementation Tasks

## 1. Update StatisticsWidget Component
- [x] **File**: `src/tcm/pages/dashboard/__init__.py`
- [x] **Action**: Modify the `StatisticsWidget` function to accept an optional `href` parameter
- [x] **Details**:
  - Add `href: str = None` parameter to function signature
  - Wrap the entire widget content in an `A` tag when `href` is provided
  - Ensure the link is accessible and keyboard-navigable
  - Maintain existing styling and layout

## 2. Update DashboardPage to Pass Navigation Links
- [x] **File**: `src/tcm/pages/dashboard/__init__.py`
- [x] **Action**: Update the `StatisticsWidget` calls in `DashboardPage` to include href parameters
- [x] **Details**:
  - Test Cases widget: `href="/testcases"`
  - Projects widget: `href="/projects"`
  - Tags widget: `href="/tags"`

## 3. Add CSS Styles for Clickable Widgets
- [x] **File**: `src/tcm/static/css/styles.css`
- [x] **Action**: Add styles for clickable statistics widgets
- [x] **Details**:
  - Add hover effect (e.g., subtle background color change, slight scale transform)
  - Add cursor pointer on hover
  - Add focus styles for keyboard navigation
  - Ensure visited link colors don't interfere with widget appearance
  - Maintain smooth transitions for better UX

## 4. Update Dashboard Page Tests
- [x] **File**: `tests/integration/test_dashboard_pages.py`
- [x] **Action**: Add tests to verify navigation links are present and correct
- [x] **Details**:
  - Test that Test Cases widget has `href="/testcases"`
  - Test that Projects widget has `href="/projects"`
  - Test that Tags widget has `href="/tags"`
  - Verify the links are properly rendered in the HTML output

## 5. Manual Testing
- [ ] **Action**: Verify the feature works as expected in the browser
- [ ] **Details**:
  - Click each statistics widget and verify navigation to correct page
  - Test hover effects display correctly
  - Test keyboard navigation (Tab to widget, Enter to navigate)
  - Verify responsive behavior on mobile devices
  - Check that all existing dashboard functionality still works

## Dependencies
- Tasks 1 and 2 can be done in parallel or sequential order
- Task 3 (CSS) can be done in parallel with tasks 1-2
- Task 4 (tests) depends on tasks 1-2 being complete
- Task 5 (manual testing) depends on all previous tasks

## Validation
After implementation:
- Run test suite: `uv run pytest tests/integration/test_dashboard_pages.py`
- Verify all tests pass
- Run full test suite to ensure no regressions
- Manually test in browser for UX verification
