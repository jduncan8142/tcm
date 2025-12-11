# Design: Convert Tag Forms to Modals and Protect Predefined Tags

## Overview
This document outlines the design approach for converting tag creation/editing from separate pages to modal overlays, and implementing protection for predefined system tags.

## Architecture

### Modal Implementation Pattern
We'll use the existing modal pattern from the project view page (used for "Add Test Cases to Project"):

**Existing Modal Components:**
- `.modal` - Full-screen backdrop (semi-transparent)
- `.modal-content` - Form container (centered, white background)
- `.modal-header` - Title and close button
- `.modal-body` - Form fields
- `.modal-footer` - Action buttons (Cancel, Submit)

**Modal Structure:**
```html
<div id="create-tag-modal" class="modal" style="display: none;">
  <div class="modal-content">
    <div class="modal-header">
      <h3>Create New Tag</h3>
      <button type="button" onclick="hideCreateTagModal()" class="modal-close">×</button>
    </div>
    <div class="modal-body">
      <form><!-- Tag form fields --></form>
    </div>
  </div>
</div>
```

### Component Strategy

**Option 1: Inline Forms (Chosen)**
- Embed complete forms directly in the tags list page
- Forms hidden by default using `display: none`
- JavaScript toggles visibility
- **Pros**: Simple, no additional HTTP requests, forms always ready
- **Cons**: Slightly larger initial page load

**Option 2: Dynamic Form Loading**
- Fetch form HTML via AJAX when modal opens
- **Pros**: Smaller initial page load
- **Cons**: Additional HTTP requests, loading delay, more complex

**Decision**: Use Option 1 (Inline Forms) for simplicity and consistency with existing project modal pattern.

### Form Modifications

**Remove Predefined Checkbox:**
Both create and edit forms currently include:
```python
CheckboxField(
    name="is_predefined",
    label="Mark as predefined tag",
    checked=form_data.get("is_predefined", False),
)
```

This will be removed from both forms. Server-side changes:
- Create: Always set `is_predefined=False` for new tags
- Edit: Do not accept `is_predefined` parameter (keep existing value)

### Predefined Tag Protection

**UI Layer Protection:**
In `TagRow` component (list.py:17-49), conditionally show Edit/Delete buttons:
```python
Td(
    Div(
        ActionButton("Edit", ...) if not tag.get("is_predefined") else None,
        ActionButton("Delete", ...) if not tag.get("is_predefined") else None,
        cls="action-buttons",
    ) if not tag.get("is_predefined") else Span("System Tag", cls="system-tag-indicator")
)
```

**Server-Side Protection:**
Add validation in routes:
```python
# Edit route
if tag.is_predefined:
    return JSONResponse(
        status_code=403,
        content={"detail": "Predefined tags cannot be modified"}
    )

# Delete route
if tag.is_predefined:
    return JSONResponse(
        status_code=403,
        content={"detail": "Predefined tags cannot be deleted"}
    )
```

### Route Changes

**Current Routes:**
- GET `/tags/new` → Renders CreateTagPage (full page)
- POST `/tags/new` → Processes form, redirects to `/tags`
- GET `/tags/{id}/edit` → Renders EditTagPage (full page)
- POST `/tags/{id}/edit` → Processes form, redirects to `/tags`

**New Routes:**
- GET `/tags/new` → **Remove route** (form embedded in list page)
- POST `/tags/new` → Keep, but set `is_predefined=False`, return redirect on success
- GET `/tags/{id}/edit` → **Remove route** (form embedded in list page, populated via JavaScript)
- POST `/tags/{id}/edit` → Keep, add predefined check, return redirect on success

**Edit Form Population:**
For edit modal, we need the tag data in JavaScript. Options:
1. **Embed in HTML data attributes** (Chosen)
2. Fetch via AJAX when edit clicked

**Decision**: Embed tag data in button data attributes:
```python
ActionButton(
    "Edit",
    onclick=f"showEditTagModal({tag['id']}, '{tag['category']}', '{tag['value']}', '{tag.get('description', '')}')",
    size="small"
)
```

### JavaScript Functions

```javascript
// Create modal
function showCreateTagModal() {
    document.getElementById('create-tag-modal').style.display = 'flex';
}

function hideCreateTagModal() {
    document.getElementById('create-tag-modal').style.display = 'none';
}

// Edit modal
function showEditTagModal(id, category, value, description) {
    // Populate form fields
    document.getElementById('edit-tag-id').value = id;
    document.getElementById('edit-category').value = category;
    document.getElementById('edit-value').value = value;
    document.getElementById('edit-description').value = description;

    // Update form action URL
    document.getElementById('edit-tag-form').action = `/tags/${id}/edit`;

    // Show modal
    document.getElementById('edit-tag-modal').style.display = 'flex';
}

function hideEditTagModal() {
    document.getElementById('edit-tag-modal').style.display = 'none';
}

// Click outside to close
window.onclick = function(event) {
    const createModal = document.getElementById('create-tag-modal');
    const editModal = document.getElementById('edit-tag-modal');

    if (event.target === createModal) {
        hideCreateTagModal();
    }
    if (event.target === editModal) {
        hideEditTagModal();
    }
}
```

### Form Submission Handling

**Create Form:**
- POST to `/tags/new`
- Server sets `is_predefined=False`
- On success: Redirect to `/tags?success=Tag created successfully`
- On error: Need to show error in modal (requires AJAX or page reload with modal open)

**Edit Form:**
- POST to `/tags/{id}/edit`
- Server validates tag is not predefined
- On success: Redirect to `/tags?success=Tag updated successfully`
- On error: Need to show error in modal

**Error Handling Strategy:**
Option 1: Traditional form submission (redirect on error, modal re-opens)
Option 2: AJAX submission (stay on page, show errors in modal)

**Decision**: Use Option 1 (traditional) for simplicity:
- On error, redirect back to `/tags` with error message
- Add JavaScript to check URL params and auto-open modal if error present
- Populate form with previous values from query params

### CSS Considerations

**Existing Modal Styles:**
- `.modal` and related classes already exist in styles.css
- Work well for form content
- Responsive (max-width adjusts on mobile)

**Additional Styles Needed:**
None - existing modal styles are sufficient for forms.

## Data Flow

### Create Tag Flow
1. User clicks "Create New Tag" button on `/tags`
2. JavaScript shows create modal (`#create-tag-modal`)
3. User fills form and submits
4. POST to `/tags/new` with `is_predefined` always False
5. Server validates, creates tag
6. Redirect to `/tags?success=Tag created successfully`
7. Success message displayed, modal closed

### Edit Tag Flow
1. User clicks "Edit" button for a custom tag
2. JavaScript populates edit modal with tag data
3. JavaScript shows edit modal (`#edit-tag-modal`)
4. User modifies form and submits
5. POST to `/tags/{id}/edit`
6. Server validates tag is not predefined
7. Server updates tag (keeps `is_predefined` unchanged)
8. Redirect to `/tags?success=Tag updated successfully`
9. Success message displayed, modal closed

### Predefined Tag Protection Flow
1. Tags list renders with predefined tags marked
2. Edit/Delete buttons hidden for predefined tags
3. If user attempts direct API call to edit/delete predefined tag:
   - Server returns 403 Forbidden
   - Error message displayed

## Migration Considerations

### Backward Compatibility
- Existing predefined tags remain unchanged
- Existing custom tags remain unchanged
- API endpoints remain the same (just different UI)
- No database migration needed

### Testing Strategy
1. **Modal Functionality**: Test modal open/close, click-outside
2. **Form Submission**: Test create/edit with valid/invalid data
3. **Predefined Protection**: Test that predefined tags cannot be edited/deleted
4. **Error Handling**: Test error display in modal context
5. **Responsive**: Test modals on mobile devices

## Security Considerations

### Server-Side Validation
Critical: Never trust client-side UI hiding. Always validate on server:
- Check `tag.is_predefined` before allowing edits
- Check `tag.is_predefined` before allowing deletes
- Return 403 Forbidden with clear error message

### XSS Prevention
When displaying tag data in JavaScript:
- Escape special characters in tag values
- Use proper JavaScript string escaping
- Consider using JSON encoding for data attributes

Example:
```python
import json

ActionButton(
    "Edit",
    onclick=f"showEditTagModal({json.dumps(tag)})",
    size="small"
)
```

## Performance Considerations

### Initial Page Load
- Modals embedded in HTML increase page size by ~2KB per form
- Negligible impact: forms are simple with few fields
- No additional HTTP requests needed

### Modal Interactions
- Show/hide is instant (CSS display toggle)
- No loading delay compared to page navigation
- Better perceived performance

## Alternatives Considered

### 1. Keep Separate Pages
**Pros**: Simpler routing, traditional pattern
**Cons**: Context switching, slower workflow, not requested
**Decision**: Rejected - user explicitly requested modal overlays

### 2. AJAX Form Submission
**Pros**: No page reload, smoother UX
**Cons**: More complex error handling, requires JSON responses
**Decision**: Deferred - can be added later if needed

### 3. Soft Delete Predefined Tags
**Pros**: Allows "deleting" while keeping data
**Cons**: Complicates UI (show hidden tags?), not requested
**Decision**: Rejected - hard protection is clearer

### 4. Allow Editing Predefined Tag Descriptions Only
**Pros**: Some flexibility while protecting structure
**Cons**: Adds complexity, partial edit is confusing
**Decision**: Rejected - complete protection is simpler and safer

## Future Enhancements

**Not in Scope:**
- Batch tag operations
- Tag templates
- Tag import/export
- Advanced tag permissions (role-based)
- Undo tag deletion
- Tag usage analytics

These can be considered in future proposals if needed.
