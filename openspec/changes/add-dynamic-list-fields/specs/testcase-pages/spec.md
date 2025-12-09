# testcase-pages Spec Delta

## MODIFIED Requirements

### Requirement: Create Test Case Page
The system SHALL provide a create page at `/testcases/new` that allows users to create new test cases with dynamic list input fields for preconditions, steps, and expected results.

#### Scenario: User sees empty list fields
- **WHEN** user navigates to `/testcases/new`
- **THEN** the Preconditions field shows only a label with "+ Add New" button
- **AND** the Steps field shows only a label with "+ Add New" button
- **AND** the Expected Results field shows only a label with "+ Add New" button
- **AND** no input fields are visible until the user clicks to add

#### Scenario: User adds items to a list field
- **WHEN** user clicks the "+ Add New" button on a list field
- **THEN** a new input row is added below the label
- **AND** the input row contains a text input field and a "×" remove button
- **AND** the "+ Add New" button remains visible for adding more items
- **AND** the new input field receives focus

#### Scenario: User adds multiple items
- **WHEN** user clicks "+ Add New" multiple times
- **THEN** multiple input rows are added
- **AND** each row is numbered sequentially (1, 2, 3, etc.)
- **AND** items are displayed in the order they were added

#### Scenario: User removes an item
- **WHEN** user clicks the "×" button on an item row
- **THEN** that item row is removed from the list
- **AND** remaining items are renumbered sequentially

#### Scenario: Form validation for required list fields
- **WHEN** user submits the form without any steps
- **THEN** a validation error is displayed indicating steps are required
- **AND** the form is not submitted

#### Scenario: Form validation for required expected results
- **WHEN** user submits the form without any expected results
- **THEN** a validation error is displayed indicating expected results are required
- **AND** the form is not submitted

#### Scenario: Form submission with list items
- **WHEN** user has added items to preconditions, steps, and expected results
- **AND** user submits the form
- **THEN** the test case is created with all items stored individually
- **AND** item order is preserved as entered

### Requirement: Edit Test Case Page
The system SHALL provide an edit page at `/testcases/{id}/edit` that allows users to modify existing test cases using dynamic list input fields.

#### Scenario: Edit page shows existing items
- **WHEN** user navigates to `/testcases/{id}/edit`
- **THEN** existing preconditions are displayed as individual input rows
- **AND** existing steps are displayed as individual input rows
- **AND** existing expected results are displayed as individual input rows
- **AND** each row shows its content in an editable input field

#### Scenario: User modifies existing items
- **WHEN** user edits the content of an existing item
- **AND** user saves the form
- **THEN** the item content is updated in the database

#### Scenario: User adds new items during edit
- **WHEN** user clicks "+ Add New" on the edit page
- **THEN** a new input row is added to the end of the list
- **AND** user can enter new content

#### Scenario: User removes items during edit
- **WHEN** user clicks "×" on an existing item
- **AND** user saves the form
- **THEN** the item is removed from the test case

#### Scenario: User reorders items during edit
- **WHEN** user adds or removes items
- **AND** user saves the form
- **THEN** the final order of items (top to bottom) is preserved

### Requirement: View Test Case Details Page
The system SHALL provide a details page at `/testcases/{id}` that displays test case items as formatted lists.

#### Scenario: User views preconditions list
- **WHEN** user views a test case with preconditions
- **THEN** preconditions are displayed as a bulleted or numbered list
- **AND** each precondition is shown as a separate list item

#### Scenario: User views steps list
- **WHEN** user views a test case with steps
- **THEN** steps are displayed as a numbered list
- **AND** each step is shown as a separate numbered item

#### Scenario: User views expected results list
- **WHEN** user views a test case with expected results
- **THEN** expected results are displayed as a numbered list
- **AND** each expected result is shown as a separate numbered item

#### Scenario: User views empty preconditions
- **WHEN** user views a test case with no preconditions
- **THEN** "None" or similar placeholder text is displayed

## ADDED Requirements

### Requirement: DynamicListField Component
The system SHALL provide a reusable DynamicListField component for forms that need multi-item input.

#### Scenario: Component renders with label and add button
- **WHEN** DynamicListField is rendered with no initial values
- **THEN** a label is displayed
- **AND** a "+ Add New" button is displayed next to the label
- **AND** no input rows are initially visible

#### Scenario: Component renders with initial values
- **WHEN** DynamicListField is rendered with initial values
- **THEN** each initial value is displayed in its own input row
- **AND** the "+ Add New" button is visible for adding more items

#### Scenario: Component handles required validation
- **WHEN** DynamicListField is marked as required
- **AND** no items have content
- **THEN** HTML5 validation prevents form submission
