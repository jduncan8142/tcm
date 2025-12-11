# Change: Convert Tag Forms to Modals and Protect Predefined Tags

## Why
The current tag management system uses separate pages for creating and editing tags, requiring navigation away from the tags list. This breaks the user's context and makes tag management cumbersome. Additionally, users can currently edit and delete predefined system tags, which can break the application's taxonomy. Converting to modal overlays and protecting predefined tags will improve UX and data integrity.

## What Changes
- **Create Tag Modal**: Convert `/tags/new` from separate page to modal overlay on tags list page
  - Tags list remains visible behind modal (with backdrop)
  - Click outside modal closes it
  - Remove "predefined" checkbox (users cannot create predefined tags)

- **Edit Tag Modal**: Convert `/tags/{id}/edit` from separate page to modal overlay on tags list page
  - Tags list remains visible behind modal (with backdrop)
  - Click outside modal closes it
  - Remove "predefined" checkbox (users cannot modify predefined status)

- **Protect Predefined Tags**: Prevent users from editing or deleting predefined tags
  - Hide Edit/Delete buttons for predefined tags in list
  - Add server-side validation to reject edit/delete operations on predefined tags
  - All user-created tags default to `is_predefined=False`

## Impact
- **Affected specs**: tag-pages (MODIFIED create/edit requirements, ADDED predefined tag protection requirement)
- **Affected code**:
  - Modified: `src/tcm/pages/tags/list.py` (add modals, hide actions for predefined)
  - Modified: `src/tcm/pages/tags/create.py` (remove checkbox, adapt for modal rendering)
  - Modified: `src/tcm/pages/tags/edit.py` (remove checkbox, adapt for modal rendering)
  - Modified: `src/tcm/routes/tag_pages.py` (update routes for modal handling, add validation)
  - Modified: `src/tcm/static/css/styles.css` (modal form styling if needed)
  - Tests: Update tests for modal behavior and predefined tag protection
- **User Experience**: Faster tag management workflow, no context switching
- **Data Integrity**: Predefined tags protected from accidental modification
- **Breaking Changes**: None - existing tags and API remain compatible
