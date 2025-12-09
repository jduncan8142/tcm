# Pending TODOs

This file tracks tasks and enhancements that were identified but deferred during development. Review these items when time permits.

## Tag Picker Component Enhancements
**Related to**: `enhance-tag-picker-component` proposal
**Status**: ✅ Core implementation complete, enhancements deferred

### Accessibility Improvements
- Add ARIA labels, roles, and states to the tag picker component
- Implement proper focus management for modal dialogs
- Ensure screen reader compatibility

### Keyboard Navigation
- Add arrow key navigation for autocomplete dropdown
- Add Enter key to select highlighted suggestions
- Add Escape key to close dropdown/modal
- Test and verify full keyboard-only interaction flow

### Cross-Browser Testing
- Test tag picker on Chrome, Firefox, Safari, Edge
- Verify mobile/touch interaction on iOS and Android
- Test responsiveness on various screen sizes
- Verify all interactive elements work without mouse

## Dynamic List Fields Implementation
**Related to**: `add-dynamic-list-fields` proposal
**Status**: ⏸️ DEFERRED - Requires careful review and planning
**Complexity**: HIGH - Breaking changes, database migration required

### Why Deferred
This proposal requires significant changes that should be reviewed with you present:
1. **Breaking API Changes**: Fields change from `string` to `list[str]`
2. **Database Migration**: Need to create new tables and migrate existing data
3. **Data Loss Risk**: Improper migration could lose test case data
4. **Rollback Strategy**: Need plan for reverting if issues arise

### Proposed Implementation Approach (For Review)

#### Option 1: New Tables (Recommended)
Create separate tables for structured storage:
```
testcase_preconditions (id, testcase_id, order_index, content)
testcase_steps (id, testcase_id, order_index, content)
testcase_expected_results (id, testcase_id, order_index, content)
```

**Migration Steps:**
1. Create new tables with Alembic migration
2. Split existing text fields into individual items (split on newlines)
3. Keep old columns temporarily for rollback
4. Update API schemas to return `list[str]`
5. Update UI to use DynamicListField component
6. Test thoroughly with existing data
7. Remove old columns after verification period

#### Option 2: Polymorphic Table
Single table for all list items:
```
testcase_items (id, testcase_id, item_type, order_index, content)
```
Where `item_type` is enum: 'precondition', 'step', 'expected_result'

**Pros**: Single table, easier to manage
**Cons**: Less type safety, harder to query specific types

### Implementation Tasks Remaining
- [ ] Decide on database schema approach (Option 1 vs 2)
- [ ] Write Alembic migration script
- [ ] Write data migration script with safety checks
- [ ] Create DynamicListField UI component
- [ ] Add JavaScript for add/remove functionality
- [ ] Update Pydantic schemas for API
- [ ] Update form handlers to parse list inputs
- [ ] Update view pages to display as numbered lists
- [ ] Write comprehensive tests including migration tests
- [ ] Test with production-like data volume
- [ ] Create rollback procedure documentation

### Questions for Discussion
1. **Migration Strategy**: Should we migrate all at once or support both formats temporarily?
2. **Newline Handling**: How to split existing multi-line text? (by newline? by number?)
3. **Empty Items**: Should we allow empty list items or skip them?
4. **API Versioning**: Do we need to version the API for backward compatibility?
5. **UI Only**: Alternative - keep database as-is but only change UI to parse/format text as list?

### Risk Assessment
- **HIGH**: Data migration on production data
- **MEDIUM**: Breaking API changes affecting any API consumers
- **LOW**: UI changes (reversible)

### Recommendation
Schedule a dedicated session to:
1. Review and approve migration strategy
2. Test migration on copy of production database
3. Implement with ability to rollback
4. Monitor closely after deployment

## Notes
- Tag picker enhancements are nice-to-haves, not blockers
- Dynamic list fields is a major feature that needs careful planning
- All completed proposals have been tested and committed
- Enhanced UI proposal is being implemented by background agent

---
*Last Updated: 2025-12-09*
