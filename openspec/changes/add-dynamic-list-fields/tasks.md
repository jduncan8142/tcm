# Tasks: add-dynamic-list-fields

## Implementation Tasks

### Phase 1: Database Schema

- [ ] 1. Create SQLAlchemy models for item tables
  - File: `src/tcm/models/testcase_items.py` (new file)
  - Create `TestCasePrecondition`, `TestCaseStep`, `TestCaseExpectedResult` models
  - Include: id, testcase_id (FK), order_index, content, created_at

- [ ] 2. Update TestCase model with relationships
  - File: `src/tcm/models/testcase.py`
  - Add relationships: `precondition_items`, `step_items`, `expected_result_items`
  - Configure cascade delete and ordering

- [ ] 3. Update models __init__ to export new models
  - File: `src/tcm/models/__init__.py`
  - Export new item models

- [ ] 4. Create Alembic migration for new tables
  - Command: `uv run alembic revision --autogenerate -m "Add testcase item tables"`
  - Creates: testcase_preconditions, testcase_steps, testcase_expected_results
  - Add indexes for testcase_id + order_index

- [ ] 5. Run migration
  - Command: `uv run alembic upgrade head`
  - Verify tables created correctly

### Phase 2: Data Migration

- [ ] 6. Create data migration script
  - File: `scripts/migrate_testcase_items.py`
  - Split existing text fields into individual item records
  - Handle newline-separated content
  - Preserve ordering

- [ ] 7. Run data migration
  - Command: `uv run python scripts/migrate_testcase_items.py`
  - Verify existing test cases have migrated items

### Phase 3: API Schema Updates

- [ ] 8. Update Pydantic schemas
  - File: `src/tcm/schemas/testcase.py`
  - Change `preconditions` to `list[str]`
  - Change `steps` to `list[str]`
  - Change `expected_results` to `list[str]`
  - Add validators for non-empty required lists

- [ ] 9. Update API routes to handle list fields
  - File: `src/tcm/routes/testcases.py`
  - Create item records when creating/updating test cases
  - Return items as lists in responses
  - Handle item ordering

### Phase 4: UI Component

- [ ] 10. Create DynamicListField component
  - File: `src/tcm/pages/components/forms.py`
  - Render header with label and "+" button
  - Render items container with existing items
  - Include JavaScript for add/remove functionality

- [ ] 11. Add CSS styles for dynamic list fields
  - File: `src/tcm/static/css/styles.css`
  - Style `.dynamic-list-field`, `.dynamic-list-header`
  - Style `.dynamic-list-item`, `.btn-add-item`, `.btn-remove-item`
  - Handle responsive layout

### Phase 5: Form Integration

- [ ] 12. Update CreateTestCasePage
  - File: `src/tcm/pages/testcases/create.py`
  - Replace TextAreaField with DynamicListField for preconditions, steps, expected_results
  - Handle form_data as lists

- [ ] 13. Update EditTestCasePage
  - File: `src/tcm/pages/testcases/edit.py`
  - Replace TextAreaField with DynamicListField
  - Pre-populate with existing items

- [ ] 14. Update page route handlers for form submission
  - File: `src/tcm/routes/testcase_pages.py`
  - Parse list form fields
  - Create/update item records
  - Handle ordering

### Phase 6: View Page Updates

- [ ] 15. Update ViewTestCasePage
  - File: `src/tcm/pages/testcases/view.py`
  - Display preconditions as ordered list
  - Display steps as numbered list
  - Display expected results as numbered list

### Phase 7: Testing

- [ ] 16. Update API integration tests
  - File: `tests/integration/test_testcases_api.py`
  - Test creating test cases with list fields
  - Test updating list fields
  - Test response format

- [ ] 17. Update page integration tests
  - File: `tests/integration/test_testcase_pages.py`
  - Test form rendering with DynamicListField
  - Test form submission with multiple items
  - Test edit page pre-population

- [ ] 18. Run full test suite
  - Command: `uv run pytest tests/ -v`
  - Fix any regressions
  - All tests should pass

### Phase 8: Cleanup (Optional, after verification)

- [ ] 19. Create migration to remove old text columns
  - After sufficient testing/verification
  - Remove: preconditions, steps, expected_results text columns
  - This is optional and can be deferred

## Dependencies
- Phase 1-2 must complete before Phase 3
- Phase 3 must complete before Phase 4-6
- Phase 4-6 can be done in parallel
- Phase 7 requires Phases 4-6 to be complete
- Phase 8 is optional and can be done later

## Verification
- Manual: Create a test case with multiple steps, verify they save and display correctly
- Manual: Edit a test case, add/remove items, verify changes persist
- Automated: Run `uv run pytest tests/ -v`

## Rollback Plan
If issues arise:
1. Old text columns remain in database
2. Can revert code to use old columns
3. Data remains in both formats during transition
