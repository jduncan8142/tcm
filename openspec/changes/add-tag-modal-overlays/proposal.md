# Change: Add Tag Modal Overlays

## Why
Tag creation and editing currently require navigating to separate pages (`/tags/new` and `/tags/{id}/edit`), breaking the user's context and making tag management slower. Converting these to modal overlays on the tags list page will provide a faster, more modern workflow where users stay on the list page and can quickly create or edit tags without losing their place.

## What Changes
- **Create Tag Modal**: Convert `/tags/new` from separate page to modal overlay on tags list page
  - Embed create form in tags list page (hidden by default)
  - Button triggers JavaScript to show modal
  - Tags list remains visible behind modal with backdrop
  - Click outside modal or Cancel closes it

- **Edit Tag Modal**: Convert `/tags/{id}/edit` from separate page to modal overlay on tags list page
  - Embed edit form template in tags list page (hidden by default)
  - Edit button triggers JavaScript to populate and show modal
  - Tags list remains visible behind modal with backdrop
  - Click outside modal or Cancel closes it

- **Remove Separate Page Routes**: Remove GET routes for `/tags/new` and `/tags/{id}/edit`
  - Keep POST routes for form submission
  - Forms submit to same endpoints but return to list page

## Impact
- **Affected specs**: tag-pages (MODIFIED create/edit requirements to use modals instead of separate pages)
- **Affected code**:
  - Modified: `src/tcm/pages/tags/list.py` (embed modals, add JavaScript)
  - Modified: `src/tcm/pages/tags/create.py` (adapt for modal rendering)
  - Modified: `src/tcm/pages/tags/edit.py` (adapt for modal rendering)
  - Modified: `src/tcm/routes/tag_pages.py` (remove GET routes, update error handling)
  - Tests: Update tests for modal behavior
- **User Experience**: Faster workflow, no context switching, modern UI pattern
- **Breaking Changes**: None - form submission endpoints remain the same
- **Dependencies**: Leverages existing modal CSS from project view page
