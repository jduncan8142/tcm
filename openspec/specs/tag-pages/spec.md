# tag-pages Specification

## Purpose
TBD - created by archiving change add-tag-pages. Update Purpose after archive.
## Requirements
### Requirement: Tags List Page
The system SHALL provide a list page at `/tags` that displays all tags grouped by category with filtering capabilities.

#### Scenario: User views tags list
- **WHEN** user navigates to `/tags`
- **THEN** all tags are displayed grouped by category
- **AND** each tag shows value, description, and predefined status
- **AND** quick action buttons (edit, delete) are visible

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

### Requirement: Create Tag Page
The system SHALL provide a create page at `/tags/new` that allows users to create new tags with full form validation.

#### Scenario: User creates a tag successfully
- **WHEN** user fills all required fields (category, value)
- **AND** user clicks the submit button
- **THEN** the tag is created via the API
- **AND** user is redirected to the tags list page
- **AND** a success message is displayed

#### Scenario: User submits invalid form
- **WHEN** user submits the form with missing required fields
- **THEN** validation errors are displayed next to the invalid fields
- **AND** the form is not submitted

#### Scenario: Category selection
- **WHEN** user selects a category from the dropdown
- **THEN** existing categories are shown as options
- **AND** user can also enter a new category name

#### Scenario: Duplicate tag detection
- **WHEN** user attempts to create a tag with a category+value combination that already exists
- **THEN** a validation error is displayed indicating the duplicate
- **AND** the form is not submitted

#### Scenario: User sets predefined flag
- **WHEN** user checks the "is_predefined" checkbox
- **AND** submits the form
- **THEN** the tag is created with is_predefined set to true

#### Scenario: User cancels creation
- **WHEN** user clicks the cancel button
- **THEN** user is redirected to the tags list page
- **AND** no tag is created

### Requirement: Edit Tag Page
The system SHALL provide an edit page at `/tags/{id}/edit` that allows users to modify existing tags.

#### Scenario: User edits a tag successfully
- **WHEN** user modifies tag fields
- **AND** user clicks the save button
- **THEN** the tag is updated via the API
- **AND** user is redirected to the tags list page
- **AND** a success message is displayed

#### Scenario: Form is pre-populated with existing data
- **WHEN** user navigates to `/tags/{id}/edit`
- **THEN** all form fields are pre-populated with the current tag data

#### Scenario: Non-existent tag
- **WHEN** user navigates to `/tags/{id}/edit` for a non-existent ID
- **THEN** a 404 error page is displayed

#### Scenario: Duplicate detection on update
- **WHEN** user changes category or value to a combination that already exists
- **THEN** a validation error is displayed indicating the duplicate
- **AND** the form is not submitted

#### Scenario: User cancels edit
- **WHEN** user clicks the cancel button
- **THEN** user is redirected to the tags list page
- **AND** no changes are saved

### Requirement: Tag Deletion
The system SHALL allow users to delete tags from the tags list page with confirmation.

#### Scenario: User deletes a tag
- **WHEN** user clicks the delete button on a tag
- **THEN** a confirmation dialog is shown
- **AND** if confirmed, the tag is deleted via the API
- **AND** the tags list is refreshed

#### Scenario: Delete tag with associations
- **WHEN** user attempts to delete a tag that is associated with test cases
- **THEN** a warning is displayed indicating the tag is in use
- **AND** user must confirm they want to proceed with deletion

### Requirement: Responsive Design
All tag pages SHALL be responsive and work on mobile, tablet, and desktop screen sizes.

#### Scenario: Mobile view adaptation
- **WHEN** user views tag pages on a mobile device
- **THEN** the layout adapts to the smaller screen size
- **AND** all functionality remains accessible
- **AND** touch targets are appropriately sized

### Requirement: Loading States
All tag pages SHALL display appropriate loading indicators during data fetch operations.

#### Scenario: List page loading
- **WHEN** the tags list is being fetched
- **THEN** a loading spinner or skeleton is displayed
- **AND** the spinner is replaced with data when loading completes

#### Scenario: Form submission loading
- **WHEN** a form is being submitted
- **THEN** the submit button shows a loading state
- **AND** the form is disabled to prevent duplicate submissions

### Requirement: Error Handling
All tag pages SHALL handle errors gracefully and display clear error messages.

#### Scenario: API error during list fetch
- **WHEN** an error occurs while fetching the tags list
- **THEN** an error message is displayed to the user
- **AND** a retry option is provided

#### Scenario: Validation error display
- **WHEN** form validation fails
- **THEN** error messages are displayed next to the relevant fields
- **AND** the first invalid field receives focus

