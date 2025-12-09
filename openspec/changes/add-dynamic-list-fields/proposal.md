# Proposal: add-dynamic-list-fields

## Summary
Replace the single textarea fields for Preconditions, Steps, and Expected Results with dynamic list fields that allow users to add/remove individual items. This includes:
1. A new reusable `DynamicListField` UI component
2. Database schema migration to store items as structured arrays
3. Updated API schemas and form handling

## Motivation
Currently, Preconditions, Steps, and Expected Results are single textarea fields where users enter all items as free-form text. This has several limitations:
- No structure enforcement
- Difficult to reorder items
- No individual item management (edit/delete single items)
- Inconsistent formatting between users

A dynamic list field approach provides:
- Clear visual separation of items
- Easy add/remove individual items
- Structured data storage for better querying/reporting
- Improved UX with explicit item management

## Current Behavior
- `preconditions`: Single optional `Text` column, rendered as `TextAreaField`
- `steps`: Single required `Text` column, rendered as `TextAreaField`
- `expected_results`: Single required `Text` column, rendered as `TextAreaField`
- All stored as free-text strings in the database

## Proposed Solution

### 1. DynamicListField Component
A reusable FastHTML component that renders:
- Label with "+" (Add New) button on the right
- Clicking "+" adds a new input row below
- Each row has: input field + "×" remove button
- "+" button remains visible for adding more items
- Items are numbered for clarity (optional)

### 2. Database Schema Changes
Create new tables for structured storage:
- `testcase_preconditions`: (id, testcase_id, order_index, content)
- `testcase_steps`: (id, testcase_id, order_index, content)
- `testcase_expected_results`: (id, testcase_id, order_index, content)

Or alternatively, use a single polymorphic table:
- `testcase_items`: (id, testcase_id, item_type, order_index, content)

Data migration will convert existing text fields to individual items.

### 3. API Schema Updates
Update Pydantic schemas:
- `preconditions`: `list[str]` instead of `str | None`
- `steps`: `list[str]` instead of `str`
- `expected_results`: `list[str]` instead of `str`

### 4. Form Submission Handling
- Multiple inputs with same name (e.g., `steps[]`) submitted as array
- Backend parses array and creates associated items
- Order preserved based on form submission order

## Scope
- New component: `DynamicListField` in `src/tcm/pages/components/forms.py`
- Database migration for new item tables
- Model updates for relationships
- Schema updates for list fields
- Route handler updates for form processing
- View page updates to display items as lists
- CSS for list field styling
- JavaScript for add/remove functionality
- Integration tests

## Impact
- **Medium-High complexity**: Requires database migration and schema changes
- **Breaking change**: API response format changes for these fields
- **Data migration**: Existing data must be converted
- **Reusable**: Component can be used for any dynamic list input

## Migration Strategy
1. Create new tables/columns
2. Run data migration script to split existing text into items
3. Update API and UI to use new format
4. Keep old columns temporarily for rollback capability
5. Remove old columns after verification
