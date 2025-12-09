# Proposal: enhance-tag-picker-component

## Summary
Replace the native multi-select dropdown for tag selection with an enhanced tag picker component featuring:
1. Type-ahead search with autocomplete suggestions
2. Token/pill display for selected tags with removal capability
3. Popover dialog for browsing all available tags

## Motivation
The current tag selection uses a native HTML `<select multiple>` element which has usability issues:
- Users must hold Ctrl/Cmd to select multiple items
- No type-ahead search capability
- Difficult to see which tags are selected
- Poor mobile experience
- All tags visible in a single scrolling list

An enhanced tag picker would significantly improve the user experience by:
- Allowing quick tag search via keyboard
- Displaying selected tags as visible pills/tokens
- Providing multiple interaction modes (typing vs browsing)
- Making tag selection more intuitive

## Current Behavior
- `MultiSelectTagField` component renders a `<select multiple>` element
- Tags are grouped by category using `<optgroup>` elements
- Users must hold Ctrl/Cmd to select multiple tags
- Selected tags are only visible within the select dropdown
- Used in both create (`/testcases/new`) and edit (`/testcases/{id}/edit`) pages

## Proposed Solution

### 1. Enhanced Tag Input Field
- Text input field where user can type to search/filter tags
- Autocomplete dropdown shows matching tags as user types
- Arrow keys to navigate suggestions, Enter to select
- Selected tag appears as a token/pill in the field
- User can continue typing to add more tags

### 2. Token/Pill Display
- Each selected tag displayed as a pill with:
  - Tag value text (and optionally category)
  - "×" button on right side to remove
- Pills wrap within the input field container
- Visual styling consistent with existing `TagBadge` component

### 3. Search Button & Popover Dialog
- Search/browse button (🔍 or similar) on right side of input
- Clicking opens a popover dialog containing:
  - Multi-select list with all tags grouped by category
  - Ctrl+Click for multiple selection
  - "OK" button at bottom center to confirm
- Dialog closes when clicking outside or pressing OK
- Selected tags from dialog populate as pills in the input

### 4. Form Submission
- Hidden input field(s) to submit selected tag IDs
- Compatible with existing form processing logic

## Scope
- New reusable component: `TagPickerField` in `src/tcm/pages/components/forms.py`
- CSS styles for pills, autocomplete dropdown, and popover dialog
- JavaScript for interactive behavior
- Update create and edit test case pages to use new component
- Update integration tests

## Impact
- **Medium complexity**: Requires JavaScript for interactive behavior
- **Reusable**: New component can be used across create/edit pages
- **Backwards compatible**: Form submission structure unchanged
- **Better UX**: Significant usability improvement for tag selection

## Scope Limitation
This proposal focuses on the test case create/edit pages. The same component can later be applied to other forms that need tag selection.
