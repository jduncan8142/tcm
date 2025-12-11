# Tasks: Convert Tag Forms to Modals and Protect Predefined Tags

## Implementation Tasks

### Phase 1: Remove Predefined Checkbox from Forms

#### Task 1.1: Remove Checkbox from Create Form
- **File**: `src/tcm/pages/tags/create.py`
- **Actions**:
  - Remove `CheckboxField` import if no longer used
  - Remove CheckboxField for `is_predefined` (lines 68-72)
  - Update function docstring if it mentions is_predefined
- **Dependencies**: None
- **Acceptance**: Create form no longer has predefined checkbox

#### Task 1.2: Remove Checkbox from Edit Form
- **File**: `src/tcm/pages/tags/edit.py`
- **Actions**:
  - Remove `CheckboxField` import if no longer used
  - Remove CheckboxField for `is_predefined` (lines 66-70)
  - Update function docstring if it mentions is_predefined
- **Dependencies**: None
- **Acceptance**: Edit form no longer has predefined checkbox

#### Task 1.3: Update Create Route to Set Predefined False
- **File**: `src/tcm/routes/tag_pages.py`
- **Actions**:
  - Remove `is_predefined` parameter from `create_tag_submit` function (line 117)
  - Update tag creation to always set `is_predefined=False` (line 179)
  - Remove is_predefined from form_data dictionaries (lines 145, 168)
- **Dependencies**: Task 1.1
- **Acceptance**: All new tags created with `is_predefined=False`

#### Task 1.4: Update Edit Route to Ignore Predefined Parameter
- **File**: `src/tcm/routes/tag_pages.py`
- **Actions**:
  - Remove `is_predefined` parameter from `edit_tag_submit` function (line 241)
  - Remove line that updates `tag.is_predefined` (line 319)
  - Remove is_predefined from tag_data dictionaries (lines 277, 303)
- **Dependencies**: Task 1.2
- **Acceptance**: Edit preserves existing `is_predefined` value

### Phase 2: Add Predefined Tag Protection

#### Task 2.1: Hide Edit/Delete Buttons for Predefined Tags
- **File**: `src/tcm/pages/tags/list.py`
- **Actions**:
  - Modify `TagRow` function (lines 17-49)
  - Conditionally render Edit button only if `not tag.get("is_predefined")`
  - Conditionally render Delete button only if `not tag.get("is_predefined")`
  - Add visual indicator for predefined tags (e.g., "System Tag" text)
- **Dependencies**: None
- **Acceptance**: Predefined tags do not show Edit/Delete buttons in UI

#### Task 2.2: Add Server-Side Protection for Edit
- **File**: `src/tcm/routes/tag_pages.py`
- **Actions**:
  - In `edit_tag_submit` function, after fetching tag (line 261)
  - Add check: if `tag.is_predefined`, return 403 error
  - Return appropriate error message
- **Dependencies**: None
- **Acceptance**: Editing predefined tags returns 403 error

#### Task 2.3: Add Server-Side Protection for Delete
- **File**: `src/tcm/routes/tags.py` (API routes)
- **Actions**:
  - Find delete tag endpoint
  - After fetching tag, add check: if `tag.is_predefined`, return 403 error
  - Return appropriate error message
- **Dependencies**: None
- **Acceptance**: Deleting predefined tags returns 403 error

### Phase 3: Create Tag Modal Implementation

#### Task 3.1: Add Create Modal to List Page
- **File**: `src/tcm/pages/tags/list.py`
- **Actions**:
  - Import create form components
  - Add modal structure with id="create-tag-modal"
  - Embed CreateTagPage form inside modal-body
  - Add modal-header with title and close button
  - Modal initially hidden with `style="display: none;"`
- **Dependencies**: Task 1.1, Task 1.3
- **Acceptance**: Create modal HTML present in tags list page

#### Task 3.2: Update Create Button to Open Modal
- **File**: `src/tcm/pages/tags/list.py`
- **Actions**:
  - Change "Create New Tag" ActionButton (line 157)
  - Replace `href="/tags/new"` with `onclick="showCreateTagModal()"`
  - Change to regular Button instead of ActionButton
- **Dependencies**: Task 3.1
- **Acceptance**: Create button triggers JavaScript function

#### Task 3.3: Add JavaScript for Create Modal
- **File**: `src/tcm/pages/tags/list.py`
- **Actions**:
  - Add Script element with modal functions
  - Implement `showCreateTagModal()` function
  - Implement `hideCreateTagModal()` function
  - Add click-outside-to-close functionality
- **Dependencies**: Task 3.1
- **Acceptance**: Modal opens, closes, and handles click-outside

#### Task 3.4: Update Create Form Action
- **File**: `src/tcm/pages/tags/create.py`
- **Actions**:
  - Add `form_id` parameter to CreateTagPage function
  - Set form id attribute for JavaScript targeting
  - Ensure Cancel button closes modal instead of navigating
- **Dependencies**: Task 3.1
- **Acceptance**: Form submission works from modal

### Phase 4: Edit Tag Modal Implementation

#### Task 4.1: Add Edit Modal to List Page
- **File**: `src/tcm/pages/tags/list.py`
- **Actions**:
  - Add modal structure with id="edit-tag-modal"
  - Embed EditTagPage form inside modal-body
  - Add modal-header with title and close button
  - Modal initially hidden with `style="display: none;"`
  - Add hidden input field for tag ID
- **Dependencies**: Task 1.2, Task 1.4
- **Acceptance**: Edit modal HTML present in tags list page

#### Task 4.2: Update Edit Buttons to Open Modal
- **File**: `src/tcm/pages/tags/list.py`
- **Actions**:
  - Modify Edit ActionButton in `TagRow` function (line 38)
  - Replace `href` with `onclick` containing tag data
  - Pass tag data as JSON to JavaScript function
  - Use proper escaping for JavaScript safety
- **Dependencies**: Task 4.1, Task 2.1
- **Acceptance**: Edit buttons trigger JavaScript with tag data

#### Task 4.3: Add JavaScript for Edit Modal
- **File**: `src/tcm/pages/tags/list.py`
- **Actions**:
  - Add `showEditTagModal(tagData)` function
  - Populate form fields with tag data
  - Update form action URL with tag ID
  - Implement `hideEditTagModal()` function
  - Add click-outside-to-close functionality
- **Dependencies**: Task 4.1
- **Acceptance**: Modal opens with populated data, closes correctly

#### Task 4.4: Update Edit Form for Modal Use
- **File**: `src/tcm/pages/tags/edit.py`
- **Actions**:
  - Add `form_id` parameter to EditTagPage function
  - Set form id attribute for JavaScript targeting
  - Ensure Cancel button closes modal instead of navigating
  - Make form work when embedded (not full page)
- **Dependencies**: Task 4.1
- **Acceptance**: Form submission works from modal

### Phase 5: Remove Old Routes

#### Task 5.1: Remove Create Page Route
- **File**: `src/tcm/routes/tag_pages.py`
- **Actions**:
  - Comment out or remove `@router.get("/new")` endpoint (line 88-108)
  - Keep POST endpoint for form submission
  - Update any documentation referencing the GET route
- **Dependencies**: Task 3.4
- **Acceptance**: GET /tags/new returns 404

#### Task 5.2: Remove Edit Page Route
- **File**: `src/tcm/routes/tag_pages.py`
- **Actions**:
  - Comment out or remove `@router.get("/{tag_id}/edit")` endpoint (line 190-231)
  - Keep POST endpoint for form submission
  - Update any documentation referencing the GET route
- **Dependencies**: Task 4.4
- **Acceptance**: GET /tags/1/edit returns 404

### Phase 6: Error Handling and Validation

#### Task 6.1: Handle Create Form Errors in Modal
- **File**: `src/tcm/routes/tag_pages.py`
- **Actions**:
  - In `create_tag_submit`, on validation error:
  - Redirect to `/tags?error=<message>&modal=create&form_data=<json>`
  - Add JavaScript to check URL params and reopen modal with error
  - Populate form with previous values from URL params
- **Dependencies**: Task 3.4
- **Acceptance**: Validation errors displayed in reopened modal

#### Task 6.2: Handle Edit Form Errors in Modal
- **File**: `src/tcm/routes/tag_pages.py`
- **Actions**:
  - In `edit_tag_submit`, on validation error:
  - Redirect to `/tags?error=<message>&modal=edit&tag_id=<id>&form_data=<json>`
  - Add JavaScript to check URL params and reopen modal with error
  - Populate form with previous values from URL params
- **Dependencies**: Task 4.4
- **Acceptance**: Validation errors displayed in reopened modal

#### Task 6.3: Add Modal Auto-Open on Error
- **File**: `src/tcm/pages/tags/list.py`
- **Actions**:
  - Add JavaScript to check for `modal` URL parameter on page load
  - If `modal=create`, call `showCreateTagModal()`
  - If `modal=edit`, call `showEditTagModal()` with data from URL
  - Populate form fields with data from `form_data` URL parameter
- **Dependencies**: Task 6.1, Task 6.2
- **Acceptance**: Modals reopen with errors after form submission failure

### Phase 7: Testing

#### Task 7.1: Update Create Tag Tests
- **File**: `tests/integration/test_tag_pages.py`
- **Actions**:
  - Remove test for GET /tags/new if it exists
  - Update test for POST /tags/new to verify `is_predefined=False`
  - Add test verifying create modal is present in list page HTML
  - Add test for modal JavaScript functions (if possible)
- **Dependencies**: Phase 3 complete
- **Acceptance**: All create tag tests pass

#### Task 7.2: Update Edit Tag Tests
- **File**: `tests/integration/test_tag_pages.py`
- **Actions**:
  - Remove test for GET /tags/{id}/edit if it exists
  - Update test for POST /tags/{id}/edit to verify is_predefined unchanged
  - Add test verifying edit modal is present in list page HTML
  - Add test for predefined tag edit returns 403
- **Dependencies**: Phase 4 complete
- **Acceptance**: All edit tag tests pass

#### Task 7.3: Add Predefined Tag Protection Tests
- **File**: `tests/integration/test_tag_pages.py`
- **Actions**:
  - Test that predefined tags do not show Edit button
  - Test that predefined tags do not show Delete button
  - Test that POST to edit predefined tag returns 403
  - Test that DELETE predefined tag returns 403
  - Test that custom tags can still be edited and deleted
- **Dependencies**: Phase 2 complete
- **Acceptance**: All protection tests pass

#### Task 7.4: Run Full Test Suite
- **Actions**:
  - Execute: `uv run pytest tests/`
  - Verify all tests pass
  - Fix any regressions in other areas
  - Verify no broken references to old routes
- **Dependencies**: All previous tasks
- **Acceptance**: All 185+ tests pass, no regressions

### Phase 8: Manual Testing and Cleanup

#### Task 8.1: Manual Testing
- **Actions**:
  - Start development server
  - Navigate to `/tags`
  - Test creating a tag via modal
  - Test editing a custom tag via modal
  - Test that predefined tags cannot be edited/deleted
  - Test modal close on click-outside
  - Test modal close on Cancel button
  - Test form validation errors display correctly
  - Test on mobile devices (responsive)
- **Dependencies**: All previous tasks
- **Acceptance**: All features work as expected in manual testing

#### Task 8.2: Code Cleanup
- **Actions**:
  - Remove unused imports (CheckboxField if not used elsewhere)
  - Remove commented-out code from old routes
  - Update docstrings to reflect new modal behavior
  - Verify no dead code remains
- **Dependencies**: Task 8.1
- **Acceptance**: Code is clean and well-documented

## Task Summary

- **Total Tasks**: 25
- **Estimated Complexity**: High (significant UI/UX change with business logic updates)
- **Critical Path**: Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → Phase 7
- **Testing Coverage**: 4 test tasks covering create, edit, protection, and full regression

## Notes

- Phases can be worked sequentially to minimize risk
- Phase 1-2 can be done in parallel with Phase 3-4 if needed
- Phase 5 (removing routes) should only happen after modals are fully working
- Phase 6 (error handling) is critical for good UX
- Extensive testing required due to significant UI changes
