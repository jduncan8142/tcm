# tag-pages Specification Delta

## MODIFIED Requirements

### Requirement: Tags List Page
The system SHALL provide a list page at `/tags` that displays all tags grouped by category with filtering capabilities and inline tag management via modal overlays.

#### Scenario: User views tags list
- **WHEN** user navigates to `/tags`
- **THEN** all tags are displayed grouped by category
- **AND** each tag shows value, description, and predefined status
- **AND** quick action buttons (edit, delete) are visible for custom tags only

#### Scenario: User filters by category
- **WHEN** user selects a category filter
- **THEN** only tags in the selected category are displayed

#### Scenario: Visual distinction for predefined tags
- **WHEN** user views the tags list
- **THEN** predefined tags are visually distinguished from custom tags
- **AND** predefined status is clearly indicated

#### Scenario: Category grouping
- **WHEN** user views the tags list with multiple categories
- **THEN** tags are organized into collapsible/expandable category groups
- **AND** each group shows the category name and tag count

#### Scenario: Predefined tags do not show edit/delete actions
- **WHEN** user views the tags list
- **THEN** predefined system tags SHALL NOT display Edit buttons
- **AND** predefined system tags SHALL NOT display Delete buttons
- **AND** a visual indicator SHALL show these are system-managed tags

### Requirement: Create Tag Modal
The system SHALL provide a modal overlay on `/tags` that allows users to create new custom tags without leaving the tags list page.

#### Scenario: User opens create tag modal
- **WHEN** user clicks the "Create New Tag" button on the tags list page
- **THEN** a modal overlay appears over the tags list
- **AND** the tags list remains visible in the background with a semi-transparent backdrop
- **AND** the modal displays a tag creation form

#### Scenario: User creates a tag successfully
- **WHEN** user fills all required fields (category, value) in the modal
- **AND** user clicks the submit button
- **THEN** the tag is created via the API with `is_predefined` set to false
- **AND** the modal closes
- **AND** the tags list refreshes showing the new tag
- **AND** a success message is displayed

#### Scenario: User closes modal by clicking outside
- **WHEN** the create tag modal is open
- **AND** user clicks on the backdrop area outside the modal
- **THEN** the modal SHALL close without creating a tag
- **AND** any form input SHALL be discarded

#### Scenario: User closes modal with close button
- **WHEN** the create tag modal is open
- **AND** user clicks the × close button or Cancel button
- **THEN** the modal SHALL close without creating a tag
- **AND** any form input SHALL be discarded

#### Scenario: User submits invalid form
- **WHEN** user submits the create form with missing required fields
- **THEN** validation errors are displayed within the modal
- **AND** the modal remains open with form data preserved
- **AND** the first invalid field receives focus

#### Scenario: Category selection
- **WHEN** user selects a category from the dropdown in the modal
- **THEN** existing categories are shown as options
- **AND** user can also enter a new category name

#### Scenario: Duplicate tag detection
- **WHEN** user attempts to create a tag with a category+value combination that already exists
- **THEN** a validation error is displayed within the modal indicating the duplicate
- **AND** the modal remains open with form data preserved

#### Scenario: Predefined flag cannot be set by users
- **WHEN** user creates a new tag via the modal
- **THEN** the form SHALL NOT include a checkbox or option to mark the tag as predefined
- **AND** the created tag SHALL automatically have `is_predefined` set to false
- **AND** only system-level operations can create predefined tags

### Requirement: Edit Tag Modal
The system SHALL provide a modal overlay on `/tags` that allows users to modify existing custom tags without leaving the tags list page.

#### Scenario: User opens edit tag modal
- **WHEN** user clicks the "Edit" button for a custom tag
- **THEN** a modal overlay appears over the tags list
- **AND** the tags list remains visible in the background with a semi-transparent backdrop
- **AND** the modal displays a tag edit form
- **AND** all form fields are pre-populated with the current tag data

#### Scenario: User edits a tag successfully
- **WHEN** user modifies tag fields in the modal
- **AND** user clicks the save button
- **THEN** the tag is updated via the API
- **AND** the modal closes
- **AND** the tags list refreshes showing the updated tag
- **AND** a success message is displayed

#### Scenario: User closes modal by clicking outside
- **WHEN** the edit tag modal is open
- **AND** user clicks on the backdrop area outside the modal
- **THEN** the modal SHALL close without saving changes
- **AND** any form modifications SHALL be discarded

#### Scenario: User closes modal with close button
- **WHEN** the edit tag modal is open
- **AND** user clicks the × close button or Cancel button
- **THEN** the modal SHALL close without saving changes
- **AND** any form modifications SHALL be discarded

#### Scenario: Duplicate detection on update
- **WHEN** user changes category or value to a combination that already exists
- **THEN** a validation error is displayed within the modal indicating the duplicate
- **AND** the modal remains open with form data preserved

#### Scenario: Predefined status cannot be changed
- **WHEN** user edits a tag via the modal
- **THEN** the form SHALL NOT include a checkbox or option to change the predefined status
- **AND** the tag's `is_predefined` value SHALL remain unchanged after edit
- **AND** only system-level operations can modify the predefined flag

### Requirement: Predefined Tag Protection
The system SHALL protect predefined system tags from user modification or deletion to maintain data integrity.

#### Scenario: Predefined tags cannot be edited via UI
- **WHEN** user views a predefined tag in the tags list
- **THEN** the Edit button SHALL NOT be displayed for that tag
- **AND** clicking on the tag SHALL NOT open the edit modal

#### Scenario: Predefined tags cannot be deleted via UI
- **WHEN** user views a predefined tag in the tags list
- **THEN** the Delete button SHALL NOT be displayed for that tag
- **AND** no deletion option SHALL be available for that tag

#### Scenario: Edit API rejects predefined tag modifications
- **WHEN** a request is made to edit a predefined tag via POST /tags/{id}/edit
- **THEN** the server SHALL return HTTP 403 Forbidden status
- **AND** an error message SHALL indicate that predefined tags cannot be modified
- **AND** no changes SHALL be saved to the tag

#### Scenario: Delete API rejects predefined tag deletion
- **WHEN** a request is made to delete a predefined tag via DELETE /api/tags/{id}
- **THEN** the server SHALL return HTTP 403 Forbidden status
- **AND** an error message SHALL indicate that predefined tags cannot be deleted
- **AND** the tag SHALL remain in the database

#### Scenario: Custom tags can still be edited
- **WHEN** user attempts to edit a custom tag (is_predefined=false)
- **THEN** the Edit button SHALL be visible and functional
- **AND** the edit modal SHALL open with the tag's data
- **AND** the tag can be successfully updated

#### Scenario: Custom tags can still be deleted
- **WHEN** user attempts to delete a custom tag (is_predefined=false)
- **THEN** the Delete button SHALL be visible and functional
- **AND** a confirmation dialog SHALL be shown
- **AND** the tag can be successfully deleted if confirmed

## REMOVED Requirements

### Requirement: Create Tag Page
**Reason**: Functionality moved to modal overlay on tags list page
**Migration**: Users now use the "Create New Tag" button on /tags which opens a modal overlay

### Requirement: Edit Tag Page
**Reason**: Functionality moved to modal overlay on tags list page
**Migration**: Users now use the "Edit" button on individual tags in /tags which opens a modal overlay

### Requirement: User sets predefined flag
**Reason**: Users should not be able to create or modify predefined tags
**Migration**: Only system-level operations (database seeds, migrations) can set is_predefined=true

### Requirement: User cancels creation
**Reason**: Covered by new create modal close scenarios

### Requirement: User cancels edit
**Reason**: Covered by new edit modal close scenarios

### Requirement: Form is pre-populated with existing data
**Reason**: Covered by edit modal open scenario

### Requirement: Non-existent tag
**Reason**: No longer relevant as edit is triggered from existing tag in list
