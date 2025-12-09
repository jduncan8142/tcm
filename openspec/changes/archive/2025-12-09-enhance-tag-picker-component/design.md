# Design: enhance-tag-picker-component

## Architecture Overview

This feature introduces a new interactive tag picker component that combines server-rendered FastHTML with client-side JavaScript for interactivity.

## Component Structure

```
TagPickerField
├── Container (wrapper div)
│   ├── Label
│   ├── Tag Input Container
│   │   ├── Pills Container (selected tags as pills)
│   │   │   └── TagPill × N (tag value + remove button)
│   │   ├── Text Input (for typing/search)
│   │   └── Search Button (opens popover)
│   ├── Autocomplete Dropdown (hidden until typing)
│   │   └── Suggestion items
│   └── Hidden Inputs (for form submission)
└── Popover Dialog (hidden until triggered)
    ├── Header
    ├── Tag List (grouped by category, multi-select)
    └── Footer (OK button)
```

## Data Flow

### Server → Client
1. FastHTML renders the component with all available tags as JSON data attribute
2. Selected tag IDs (if editing) passed as initial state
3. Tags embedded in the page for JavaScript to use

### Client-Side Interactions
1. **Typing**: Filter tags, show autocomplete dropdown
2. **Enter/Click suggestion**: Add tag as pill, clear input
3. **Click × on pill**: Remove tag from selection
4. **Click search button**: Open popover dialog
5. **Select in popover + OK**: Add selected tags as pills

### Client → Server (Form Submit)
1. Hidden `<input>` elements contain selected tag IDs
2. Form submission sends tag IDs array
3. Existing backend processing unchanged

## JavaScript Implementation

### State Management
```javascript
const tagPicker = {
    availableTags: [],      // All tags from server
    selectedTagIds: [],     // Currently selected tag IDs
    filteredTags: [],       // Tags matching current search
    highlightIndex: -1,     // Currently highlighted suggestion
};
```

### Key Functions
- `initTagPicker(containerId, tags, selectedIds)` - Initialize component
- `filterTags(searchTerm)` - Filter available tags by search term
- `selectTag(tagId)` - Add tag to selection, render pill
- `removeTag(tagId)` - Remove tag from selection
- `renderPills()` - Re-render all selected tag pills
- `showAutocomplete()` / `hideAutocomplete()` - Toggle dropdown
- `showPopover()` / `hidePopover()` - Toggle popover dialog
- `handleKeydown(event)` - Arrow keys, Enter, Escape handling
- `syncHiddenInputs()` - Update hidden form fields

## CSS Structure

```css
/* Container */
.tag-picker { }
.tag-picker-input-container { }

/* Pills */
.tag-pill { }
.tag-pill-text { }
.tag-pill-remove { }

/* Input */
.tag-picker-input { }
.tag-picker-search-btn { }

/* Autocomplete dropdown */
.tag-autocomplete { }
.tag-autocomplete-item { }
.tag-autocomplete-item.highlighted { }

/* Popover dialog */
.tag-popover { }
.tag-popover-content { }
.tag-popover-list { }
.tag-popover-footer { }
```

## Form Integration

### Hidden Input Strategy
For each selected tag, render a hidden input:
```html
<input type="hidden" name="tag_ids" value="1">
<input type="hidden" name="tag_ids" value="5">
<input type="hidden" name="tag_ids" value="12">
```

This maintains compatibility with existing form handling that expects `tag_ids` as a list.

## Accessibility Considerations

- ARIA labels for the input field
- ARIA roles for autocomplete listbox
- Keyboard navigation (arrows, enter, escape)
- Focus management when opening/closing popover
- Screen reader announcements for selection changes

## Trade-offs

### Chosen Approach: Client-Side Filtering
**Pros:**
- Instant filtering without server roundtrips
- Works with current FastHTML architecture
- Tags data already available from server

**Cons:**
- All tags loaded upfront (acceptable for ~200 predefined tags)
- More JavaScript code in the frontend

### Alternative Considered: Server-Side Search
**Pros:**
- Works with very large tag sets
- Less client-side JavaScript

**Cons:**
- Requires new API endpoint
- Slower UX due to network latency
- More complex implementation

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Uses standard DOM APIs
- No external dependencies required
