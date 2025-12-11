# Tasks: Add Tag Modal Overlays

## Implementation Tasks

### Phase 1: Create Form Helper Functions

#### Task 1.1: Extract Create Form Logic
- **File**: `src/tcm/pages/tags/create.py`
- **Actions**:
  - Create new function `CreateTagForm(categories, error_message, form_data)` that returns just the Form element
  - Update `CreateTagPage()` to call `CreateTagForm()` and wrap it in PageLayout
  - Form helper should not include PageLayout wrapper
- **Dependencies**: None
- **Acceptance**: Form logic extracted into reusable function

#### Task 1.2: Extract Edit Form Logic
- **File**: `src/tcm/pages/tags/edit.py`
- **Actions**:
  - Create new function `EditTagForm(tag, categories, error_message)` that returns just the Form element
  - Update `EditTagPage()` to call `EditTagForm()` and wrap it in PageLayout
  - Form helper should not include PageLayout wrapper
- **Dependencies**: None
- **Acceptance**: Form logic extracted into reusable function

### Phase 2: Add Create Modal to List Page

#### Task 2.1: Embed Create Modal HTML
- **File**: `src/tcm/pages/tags/list.py`
- **Actions**:
  - Import `CreateTagForm` from create.py
  - Add modal div structure with id="create-tag-modal"
  - Embed `CreateTagForm()` inside modal-body
  - Add modal-header with title and close button
  - Modal initially hidden with `style="display: none;"`
  - Get categories list for form
- **Dependencies**: Task 1.1
- **Acceptance**: Create modal HTML present in tags list page

#### Task 2.2: Update Create Button
- **File**: `src/tcm/pages/tags/list.py`
- **Actions**:
  - Change "Create New Tag" from ActionButton to Button
  - Replace `href="/tags/new"` with `onclick="showCreateTagModal()"`
  - Add proper button styling classes
- **Dependencies**: Task 2.1
- **Acceptance**: Create button triggers JavaScript function

#### Task 2.3: Add Create Modal JavaScript
- **File**: `src/tcm/pages/tags/list.py`
- **Actions**:
  - Add Script element with modal JavaScript
  - Implement `showCreateTagModal()` function
  - Implement `hideCreateTagModal()` function
  - Add click-outside-to-close handler for create modal
- **Dependencies**: Task 2.1
- **Acceptance**: Modal opens, closes, and handles click-outside

### Phase 3: Add Edit Modal to List Page

#### Task 3.1: Embed Edit Modal HTML
- **File**: `src/tcm/pages/tags/list.py`
- **Actions**:
  - Import `EditTagForm` from edit.py
  - Add modal div structure with id="edit-tag-modal"
  - Create empty tag template for form
  - Embed `EditTagForm()` inside modal-body with empty/template tag
  - Add modal-header with title and close button
  - Modal initially hidden with `style="display: none;"`
  - Add hidden input for tag ID
- **Dependencies**: Task 1.2
- **Acceptance**: Edit modal HTML present in tags list page

#### Task 3.2: Update Edit Buttons
- **File**: `src/tcm/pages/tags/list.py`
- **Actions**:
  - Modify Edit button in TagRow (only shown for custom tags)
  - Replace `href` with `onclick` passing tag data as JSON
  - Use `json.dumps(tag)` for safe JavaScript embedding
  - Ensure button only shows for non-predefined tags
- **Dependencies**: Task 3.1
- **Acceptance**: Edit buttons trigger JavaScript with tag data

#### Task 3.3: Add Edit Modal JavaScript
- **File**: `src/tcm/pages/tags/list.py`
- **Actions**:
  - Implement `showEditTagModal(tagData)` function
  - Populate form fields (category, value, description) from tagData
  - Update form action URL with tag ID
  - Implement `hideEditTagModal()` function
  - Add click-outside-to-close handler for edit modal
- **Dependencies**: Task 3.1
- **Acceptance**: Modal opens with populated data, closes correctly

### Phase 4: Error Handling and Auto-Open

#### Task 4.1: Handle Create Form Errors
- **File**: `src/tcm/routes/tag_pages.py`
- **Actions**:
  - In `create_tag_submit`, on validation error:
  - Redirect to `/tags?error=<message>&modal=create` with form data in query params
  - Encode form data as URL-safe JSON
- **Dependencies**: Task 2.3
- **Acceptance**: Validation errors redirect with modal param

#### Task 4.2: Handle Edit Form Errors
- **File**: `src/tcm/routes/tag_pages.py`
- **Actions**:
  - In `edit_tag_submit`, on validation error:
  - Redirect to `/tags?error=<message>&modal=edit&tag_id=<id>` with form data in query params
  - Encode form data as URL-safe JSON
- **Dependencies**: Task 3.3
- **Acceptance**: Validation errors redirect with modal param

#### Task 4.3: Add Auto-Open JavaScript
- **File**: `src/tcm/pages/tags/list.py`
- **Actions**:
  - Add JavaScript to check URL parameters on page load
  - If `modal=create` param exists, call `showCreateTagModal()`
  - If `modal=edit` param exists, call `showEditTagModal()` with data from URL
  - Parse and populate form with `form_data` from URL params
  - Display error message from `error` param
- **Dependencies**: Task 4.1, Task 4.2
- **Acceptance**: Modals auto-open with errors after form submission failure

### Phase 5: Remove Old Routes

#### Task 5.1: Remove Create Page GET Route
- **File**: `src/tcm/routes/tag_pages.py`
- **Actions**:
  - Remove or comment out `@router.get("/new")` endpoint
  - Keep POST endpoint unchanged
  - Update any code comments referencing the GET route
- **Dependencies**: Tasks 2.1-2.3 complete
- **Acceptance**: GET /tags/new returns 404

#### Task 5.2: Remove Edit Page GET Route
- **File**: `src/tcm/routes/tag_pages.py`
- **Actions**:
  - Remove or comment out `@router.get("/{tag_id}/edit")` endpoint
  - Keep POST endpoint unchanged
  - Update any code comments referencing the GET route
- **Dependencies**: Tasks 3.1-3.3 complete
- **Acceptance**: GET /tags/1/edit returns 404

### Phase 6: Testing

#### Task 6.1: Update Create Tag Tests
- **File**: `tests/integration/test_tag_pages.py`
- **Actions**:
  - Remove or skip test for GET /tags/new if it exists
  - Add test verifying create modal is present in list page HTML
  - Add test for successful create via modal (POST still works)
  - Add test for error handling (redirect with modal param)
- **Dependencies**: Phase 2 complete
- **Acceptance**: All create tag tests pass with modal implementation

#### Task 6.2: Update Edit Tag Tests
- **File**: `tests/integration/test_tag_pages.py`
- **Actions**:
  - Remove or skip test for GET /tags/{id}/edit if it exists
  - Add test verifying edit modal is present in list page HTML
  - Add test for successful edit via modal (POST still works)
  - Add test for error handling (redirect with modal param)
- **Dependencies**: Phase 3 complete
- **Acceptance**: All edit tag tests pass with modal implementation

#### Task 6.3: Test Modal Behavior
- **File**: `tests/integration/test_tag_pages.py`
- **Actions**:
  - Test that modal HTML contains expected form fields
  - Test that JavaScript functions are included in page
  - Test that Edit buttons only show for custom tags (not predefined)
  - Verify modal structure matches expected pattern
- **Dependencies**: Phase 2-3 complete
- **Acceptance**: Modal structure tests pass

#### Task 6.4: Run Full Test Suite
- **Actions**:
  - Execute: `uv run pytest tests/`
  - Verify all tests pass
  - Fix any regressions in other test files
  - Verify no broken links to old routes
- **Dependencies**: All previous tasks
- **Acceptance**: All 185+ tests pass, no regressions

### Phase 7: Manual Testing

#### Task 7.1: Manual Functionality Testing
- **Actions**:
  - Start development server
  - Navigate to `/tags`
  - Test creating a tag via modal (success case)
  - Test creating a tag with validation errors
  - Test editing a custom tag via modal (success case)
  - Test editing with validation errors
  - Verify predefined tags don't show Edit buttons
  - Test Cancel buttons close modals
  - Test clicking outside modals closes them
- **Dependencies**: All previous tasks
- **Acceptance**: All manual tests pass

#### Task 7.2: Responsive Testing
- **Actions**:
  - Test modals on desktop (1920x1080)
  - Test modals on tablet (768px width)
  - Test modals on mobile (320px width)
  - Verify modals are centered and readable on all sizes
  - Verify click-outside works on mobile
  - Verify form fields are accessible on small screens
- **Dependencies**: Task 7.1
- **Acceptance**: Modals work correctly on all device sizes

## Task Summary

- **Total Tasks**: 18
- **Estimated Complexity**: Medium (UI transformation, JavaScript, error handling)
- **Critical Path**: Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6
- **Testing Coverage**: 5 test tasks covering modal structure, functionality, and regression

## Notes

- Phases 2 and 3 can be worked in parallel after Phase 1
- Phase 5 (removing routes) should only happen after modals are fully working
- Extensive testing required due to significant UX change
- Manual testing critical to verify modal interactions
