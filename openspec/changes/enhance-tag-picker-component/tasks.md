# Tasks: enhance-tag-picker-component

## Implementation Tasks

### Phase 1: Core Component Structure

- [ ] 1. Create TagPickerField component shell
  - File: `src/tcm/pages/components/forms.py`
  - Create `TagPickerField` function that renders the basic HTML structure
  - Include container, label, input container, hidden inputs placeholder
  - Embed available tags as JSON data attribute for JavaScript

- [ ] 2. Add base CSS styles for tag picker
  - File: `src/tcm/static/css/styles.css`
  - Add styles for `.tag-picker`, `.tag-picker-input-container`
  - Add styles for input field and search button layout
  - Ensure responsive behavior

### Phase 2: Token/Pill Display

- [ ] 3. Create TagPill sub-component
  - File: `src/tcm/pages/components/forms.py`
  - Create `TagPill` function for individual pill rendering
  - Include tag text and × remove button

- [ ] 4. Add CSS for tag pills
  - File: `src/tcm/static/css/styles.css`
  - Style `.tag-pill`, `.tag-pill-text`, `.tag-pill-remove`
  - Handle wrapping and spacing for multiple pills

- [ ] 5. Add JavaScript for pill management
  - File: Inline Script or new JS file
  - Functions: `selectTag()`, `removeTag()`, `renderPills()`
  - Update hidden inputs when selection changes

### Phase 3: Autocomplete Search

- [ ] 6. Add autocomplete dropdown HTML structure
  - File: `src/tcm/pages/components/forms.py`
  - Add dropdown container in TagPickerField
  - Structure for suggestion items

- [ ] 7. Add CSS for autocomplete dropdown
  - File: `src/tcm/static/css/styles.css`
  - Style `.tag-autocomplete`, position below input
  - Style `.tag-autocomplete-item`, highlight state

- [ ] 8. Add JavaScript for autocomplete behavior
  - Functions: `filterTags()`, `showAutocomplete()`, `hideAutocomplete()`
  - Handle input typing events
  - Render filtered suggestions

- [ ] 9. Add keyboard navigation for autocomplete
  - Handle ArrowUp, ArrowDown for navigation
  - Handle Enter to select highlighted item
  - Handle Escape to close dropdown

### Phase 4: Popover Dialog

- [ ] 10. Add popover dialog HTML structure
  - File: `src/tcm/pages/components/forms.py`
  - Add popover container with category-grouped tag list
  - Add OK button in footer
  - Initially hidden

- [ ] 11. Add CSS for popover dialog
  - File: `src/tcm/static/css/styles.css`
  - Style `.tag-popover`, overlay, content area
  - Style tag list with category groups
  - Position and animation

- [ ] 12. Add JavaScript for popover functionality
  - Functions: `showPopover()`, `hidePopover()`
  - Handle search button click
  - Handle click outside to close
  - Handle OK button to confirm selection
  - Sync selected items back to pills

### Phase 5: Integration

- [ ] 13. Update CreateTestCasePage to use TagPickerField
  - File: `src/tcm/pages/testcases/create.py`
  - Replace `MultiSelectTagField` with `TagPickerField`
  - Ensure form submission still works

- [ ] 14. Update EditTestCasePage to use TagPickerField
  - File: `src/tcm/pages/testcases/edit.py`
  - Replace `MultiSelectTagField` with `TagPickerField`
  - Pass pre-selected tags for pill display

- [ ] 15. Update form processing to handle new input format
  - File: `src/tcm/routes/testcase_pages.py`
  - Verify tag_ids parsing works with new hidden inputs
  - Adjust if needed

### Phase 6: Testing

- [ ] 16. Add integration tests for TagPickerField
  - File: `tests/integration/test_testcase_pages.py`
  - Test that tag picker renders on create/edit pages
  - Test that selected tags are submitted correctly
  - Test that pre-selected tags show as pills on edit

- [ ] 17. Run full test suite and fix regressions
  - Execute: `uv run pytest tests/ -v`
  - All existing tests should pass
  - New tests should pass

### Phase 7: Refinement

- [ ] 18. Add accessibility attributes
  - ARIA labels, roles, and states
  - Focus management
  - Keyboard accessibility verification

- [ ] 19. Manual testing and polish
  - Test on different browsers
  - Test keyboard-only navigation
  - Test mobile/touch interaction
  - Refine styling as needed

## Dependencies
- Phase 1 must complete before phases 2-4
- Phases 2, 3, 4 can be done in parallel after phase 1
- Phase 5 requires phases 2-4 to be complete
- Phase 6-7 require phase 5 to be complete

## Verification
- Manual: Create a test case and verify tag picker works end-to-end
- Manual: Edit a test case and verify existing tags show as pills
- Automated: Run `uv run pytest tests/integration/test_testcase_pages.py -v`
