# Implementation Tasks

## 1. Update Header Title Link CSS
- [x] **File**: `src/tcm/static/css/styles.css`
- [x] **Action**: Update the `.header-title-link:hover` style to use color-based highlight instead of opacity
- [x] **Details**:
  - Remove the current `opacity: 0.7` hover effect
  - Add a color change using `var(--primary-color)` for the hover state
  - Ensure the transition property is updated to transition color instead of opacity
  - Keep the subtle, professional appearance

## 2. Update Existing Tests (if needed)
- [x] **File**: `tests/integration/test_page_layout.py`
- [x] **Action**: Verify tests still pass with the updated styling
- [x] **Details**:
  - Run existing page layout tests
  - Verify no regressions
  - Tests should not be affected by CSS changes

## 3. Manual Testing
- [ ] **Action**: Verify the visual changes work as expected in the browser
- [ ] **Details**:
  - Navigate to various pages (dashboard, testcases, projects, tags)
  - Verify header title looks like a title (not a link)
  - Hover over the title and verify subtle color highlight appears
  - Verify the color used is the theme's accent/primary color
  - Check that the transition is smooth
  - Verify keyboard navigation still works (Tab to focus, Enter to navigate)

## Dependencies
- Task 1 is independent
- Task 2 depends on task 1 being complete
- Task 3 depends on task 1 being complete

## Validation
After implementation:
- Run test suite: `uv run pytest tests/integration/test_page_layout.py`
- Manually verify visual appearance in browser
- Check hover effect uses the correct color
