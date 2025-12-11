# Design: Add Tag Modal Overlays

## Overview
Convert tag create/edit forms from separate pages to modal overlays on the tags list page, using the existing modal pattern from the project view page.

## Architecture

### Existing Modal Pattern
The project uses an established modal pattern (from `src/tcm/pages/projects/view.py`):
- `.modal` - Full-screen backdrop (semi-transparent black overlay)
- `.modal-content` - Centered white container
- `.modal-header` - Title and × close button
- `.modal-body` - Form fields
- CSS already exists in `src/tcm/static/css/styles.css`

### Implementation Strategy

**Inline Forms (Chosen Approach):**
- Embed complete forms directly in tags list page HTML
- Forms hidden by default using `display: none`
- JavaScript toggles `display: flex` to show modal
- **Advantages**: Simple, no AJAX needed, forms always ready
- **Disadvantages**: Slightly larger initial page size (~2-3KB)

### Modal Structure

**Create Modal:**
```html
<div id="create-tag-modal" class="modal" style="display: none;">
  <div class="modal-content">
    <div class="modal-header">
      <h3>Create New Tag</h3>
      <button onclick="hideCreateTagModal()" class="modal-close">×</button>
    </div>
    <div class="modal-body">
      <!-- CreateTagPage form fields (without PageLayout wrapper) -->
    </div>
  </div>
</div>
```

**Edit Modal:**
```html
<div id="edit-tag-modal" class="modal" style="display: none;">
  <div class="modal-content">
    <div class="modal-header">
      <h3>Edit Tag</h3>
      <button onclick="hideEditTagModal()" class="modal-close">×</button>
    </div>
    <div class="modal-body">
      <!-- EditTagPage form fields (without PageLayout wrapper) -->
      <form id="edit-tag-form"><!-- populated by JavaScript --></form>
    </div>
  </div>
</div>
```

### Form Adaptations

**Current Form Functions:**
- `CreateTagPage()` returns full page with `PageLayout`
- `EditTagPage()` returns full page with `PageLayout`

**New Helper Functions Needed:**
- `CreateTagForm()` - Returns just the form element (no PageLayout)
- `EditTagForm()` - Returns just the form element (no PageLayout)

These extract the form logic from the page functions for reuse in modals.

### JavaScript Functions

```javascript
// Create Modal
function showCreateTagModal() {
    document.getElementById('create-tag-modal').style.display = 'flex';
}

function hideCreateTagModal() {
    document.getElementById('create-tag-modal').style.display = 'none';
}

// Edit Modal
function showEditTagModal(tagData) {
    // Populate form fields
    document.getElementById('edit-tag-id').value = tagData.id;
    document.getElementById('edit-category').value = tagData.category;
    document.getElementById('edit-value').value = tagData.value;
    document.getElementById('edit-description').value = tagData.description || '';

    // Update form action
    document.getElementById('edit-tag-form').action = `/tags/${tagData.id}/edit`;

    // Show modal
    document.getElementById('edit-tag-modal').style.display = 'flex';
}

function hideEditTagModal() {
    document.getElementById('edit-tag-modal').style.display = 'none';
}

// Click outside to close
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        hideCreateTagModal();
        hideEditTagModal();
    }
}
```

### Button Updates

**Create Button:**
```python
# Old
ActionButton("Create New Tag", href="/tags/new", btn_type="primary")

# New
Button(
    "Create New Tag",
    type="button",
    onclick="showCreateTagModal()",
    cls="btn btn-primary"
)
```

**Edit Button:**
```python
# Old
ActionButton("Edit", href=f"/tags/{tag['id']}/edit", size="small")

# New (if not predefined)
Button(
    "Edit",
    type="button",
    onclick=f"showEditTagModal({json.dumps(tag)})",
    size="small",
    cls="btn btn-small"
)
```

### Error Handling

**Challenge:** Traditional form submission redirects on error, but modal needs to stay open with error shown.

**Solution Options:**

**Option 1: Server-side redirect with query params (Chosen)**
- On validation error: Redirect to `/tags?error=message&modal=create&form_data=json`
- JavaScript on page load checks for `modal` param
- Auto-opens modal if param present
- Re-populates form with `form_data` from URL

**Option 2: AJAX submission**
- Would require converting to JSON responses
- More complex but smoother UX
- Deferred for future enhancement

### Route Changes

**GET Routes (Remove):**
- `GET /tags/new` → Remove (form embedded in list page)
- `GET /tags/{id}/edit` → Remove (form embedded in list page)

**POST Routes (Keep):**
- `POST /tags/new` → Keep, modify error redirect
- `POST /tags/{id}/edit` → Keep, modify error redirect

## Data Flow

### Create Tag Flow
1. User clicks "Create New Tag" button
2. JavaScript shows `#create-tag-modal` (display: flex)
3. User fills form and submits
4. POST to `/tags/new`
5. On success: Redirect to `/tags?success=Tag created`
6. On error: Redirect to `/tags?error=message&modal=create&form_data=json`
7. Page loads, JavaScript detects `modal=create` param
8. JavaScript auto-opens modal and populates form with previous data

### Edit Tag Flow
1. User clicks "Edit" button for a tag
2. JavaScript calls `showEditTagModal(tagData)`
3. Form fields populated with tag data
4. User modifies and submits
5. POST to `/tags/{id}/edit`
6. On success: Redirect to `/tags?success=Tag updated`
7. On error: Redirect to `/tags?error=message&modal=edit&tag_id=id&form_data=json`
8. Page loads, JavaScript detects `modal=edit` param
9. JavaScript auto-opens modal and populates form

## CSS Considerations

**No New CSS Needed:**
- All modal styles already exist in `src/tcm/static/css/styles.css`
- `.modal`, `.modal-content`, `.modal-header`, `.modal-body` classes work perfectly for forms
- Responsive behavior already handled (mobile adapts modal width)

## Testing Strategy

**Unit Tests:**
- Verify modal HTML is present in list page
- Verify modal contains form fields
- Verify JavaScript functions are included

**Integration Tests:**
- Test form submission success (redirects to list)
- Test form submission error (redirects with modal param)
- Test modal auto-open on error redirect

**Manual Tests:**
- Create tag via modal
- Edit tag via modal
- Validation errors display in modal
- Click outside closes modal
- Cancel button closes modal
- Mobile responsive behavior

## Performance

**Impact:**
- Initial page load: +2-3KB (embedded forms)
- Modal open: Instant (no HTTP request)
- Form submit: Same as before (POST request)

**Trade-off:** Slightly larger initial page vs. faster interaction (no page navigation).

## Alternatives Considered

**1. AJAX Form Submission**
- Pros: Smoother UX, no page reload
- Cons: Complex error handling, requires JSON responses
- Decision: Deferred - can add later if needed

**2. Separate Modal Routes**
- Pros: Smaller initial page
- Cons: Additional HTTP requests, loading delay
- Decision: Rejected - inline forms are simpler

**3. Keep Separate Pages**
- Pros: Traditional, simple routing
- Cons: Context switching, slower workflow
- Decision: Rejected - user requested modal overlays
