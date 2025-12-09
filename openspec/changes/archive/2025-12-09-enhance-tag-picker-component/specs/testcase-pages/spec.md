# testcase-pages Spec Delta

## MODIFIED Requirements

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
