# testcase-pages Specification

## Purpose
TBD - created by archiving change add-testcase-pages. Update Purpose after archive.
## Requirements
### Requirement: Test Cases List Page
The system SHALL provide a list page at `/testcases` that displays all test cases with search, filtering, and pagination capabilities.

#### Scenario: User views test cases list
- **WHEN** user navigates to `/testcases`
- **THEN** a paginated list of test cases is displayed
- **AND** each row shows title, status, priority, and tag count
- **AND** quick action buttons (view, edit, delete) are visible

#### Scenario: User searches test cases
- **WHEN** user enters a search term in the search box
- **THEN** the list filters to show test cases matching the search term in title or description

#### Scenario: User filters by status
- **WHEN** user selects a status filter (e.g., "Active", "Draft", "Archived")
- **THEN** only test cases with the selected status are displayed

#### Scenario: User filters by priority
- **WHEN** user selects a priority filter (e.g., "High", "Medium", "Low")
- **THEN** only test cases with the selected priority are displayed

#### Scenario: User filters by tag
- **WHEN** user selects a tag filter
- **THEN** only test cases with the selected tag are displayed

#### Scenario: User navigates pagination
- **WHEN** user clicks next/previous page or a page number
- **THEN** the corresponding page of results is displayed
- **AND** current page indicator is updated

### Requirement: Create Test Case Page
The system SHALL provide a create page at `/testcases/new` that allows users to create new test cases with an enhanced tag picker component.

#### Scenario: User searches for tags by typing
- **WHEN** user focuses on the tag picker input field
- **AND** user starts typing a search term
- **THEN** an autocomplete dropdown appears showing tags matching the search term
- **AND** matching tags are filtered from all available tags

#### Scenario: User selects tag from autocomplete
- **WHEN** user types in the tag picker
- **AND** autocomplete suggestions are displayed
- **AND** user presses Enter or clicks on a suggestion
- **THEN** the selected tag is added as a pill/token in the input field
- **AND** the autocomplete dropdown closes
- **AND** the input is cleared for additional typing

#### Scenario: User navigates autocomplete with keyboard
- **WHEN** autocomplete suggestions are visible
- **AND** user presses ArrowDown or ArrowUp keys
- **THEN** the highlighted suggestion changes accordingly
- **AND** pressing Enter selects the highlighted suggestion

#### Scenario: User removes a tag pill
- **WHEN** user has selected tags displayed as pills
- **AND** user clicks the × button on a tag pill
- **THEN** the tag is removed from the selection
- **AND** the pill is removed from the display

#### Scenario: User opens tag browser popover
- **WHEN** user clicks the search button in the tag picker
- **THEN** a popover dialog opens displaying all available tags grouped by category
- **AND** user can scroll through the list
- **AND** user can Ctrl+Click to select multiple tags

#### Scenario: User confirms tag selection from popover
- **WHEN** user has selected tags in the popover dialog
- **AND** user clicks the OK button
- **THEN** the popover dialog closes
- **AND** selected tags are added as pills in the tag picker input

#### Scenario: User closes popover by clicking outside
- **WHEN** the tag browser popover is open
- **AND** user clicks outside the popover area
- **THEN** the popover closes without adding any tags

#### Scenario: Form submission with tag picker
- **WHEN** user has selected tags using the enhanced tag picker
- **AND** user submits the create test case form
- **THEN** the test case is created with all selected tags associated

### Requirement: Edit Test Case Page
The system SHALL provide an edit page at `/testcases/{id}/edit` that allows users to modify existing test cases using the enhanced tag picker component.

#### Scenario: Edit page shows existing tags as pills
- **WHEN** user navigates to `/testcases/{id}/edit`
- **AND** the test case has associated tags
- **THEN** the tag picker displays existing tags as pills/tokens
- **AND** user can remove existing tags or add new ones

#### Scenario: User modifies tags on edit page
- **WHEN** user is on the edit page
- **AND** user adds or removes tags using the tag picker
- **AND** user saves the form
- **THEN** the test case tag associations are updated to match the final selection

### Requirement: View Test Case Details Page
The system SHALL provide a details page at `/testcases/{id}` that displays complete test case information in read-only format.

#### Scenario: User views test case details
- **WHEN** user navigates to `/testcases/{id}`
- **THEN** all test case fields are displayed (title, description, steps, expected_result, status, priority)
- **AND** associated tags are displayed with visual styling
- **AND** edit and delete buttons are visible

#### Scenario: User views projects using test case
- **WHEN** user views a test case that belongs to one or more projects
- **THEN** a list of projects using this test case is displayed

#### Scenario: User views audit information
- **WHEN** user views test case details
- **THEN** created_at and updated_at timestamps are displayed

#### Scenario: Non-existent test case
- **WHEN** user navigates to `/testcases/{id}` for a non-existent ID
- **THEN** a 404 error page is displayed

#### Scenario: User deletes test case
- **WHEN** user clicks the delete button
- **THEN** a confirmation dialog is shown
- **AND** if confirmed, the test case is deleted via the API
- **AND** user is redirected to the test cases list page

### Requirement: Responsive Design
All test case pages SHALL be responsive and work on mobile, tablet, and desktop screen sizes.

#### Scenario: Mobile view adaptation
- **WHEN** user views test case pages on a mobile device
- **THEN** the layout adapts to the smaller screen size
- **AND** all functionality remains accessible
- **AND** touch targets are appropriately sized

### Requirement: Loading States
All test case pages SHALL display appropriate loading indicators during data fetch operations.

#### Scenario: List page loading
- **WHEN** the test cases list is being fetched
- **THEN** a loading spinner or skeleton is displayed
- **AND** the spinner is replaced with data when loading completes

#### Scenario: Form submission loading
- **WHEN** a form is being submitted
- **THEN** the submit button shows a loading state
- **AND** the form is disabled to prevent duplicate submissions

### Requirement: Error Handling
All test case pages SHALL handle errors gracefully and display clear error messages.

#### Scenario: API error during list fetch
- **WHEN** an error occurs while fetching the test cases list
- **THEN** an error message is displayed to the user
- **AND** a retry option is provided

#### Scenario: Validation error display
- **WHEN** form validation fails
- **THEN** error messages are displayed next to the relevant fields
- **AND** the first invalid field receives focus

