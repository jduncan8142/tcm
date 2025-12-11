# testcase-pages Specification Delta

## MODIFIED Requirements

### Requirement: Create Test Case Page
The system SHALL provide a create page at `/testcases/new` that allows users to create new test cases with an enhanced tag picker component and a wide, responsive form layout.

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

#### Scenario: Form layout uses wide container
- **WHEN** user navigates to `/testcases/new`
- **THEN** the form container SHALL use the wide layout (container-wide class)
- **AND** the form SHALL have a maximum width of 1200px on desktop screens
- **AND** the form SHALL fill 100% width on mobile devices (screens below 640px)
- **AND** the form layout SHALL be consistent with the edit form layout
