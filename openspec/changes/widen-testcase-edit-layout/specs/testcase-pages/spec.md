# testcase-pages Spec Delta

## MODIFIED Requirements

### Requirement: Edit Test Case Page
The system SHALL provide an edit page at `/testcases/{id}/edit` that allows users to modify existing test cases using a full-width layout.

#### Scenario: Edit page displays in full-width layout
- **WHEN** user navigates to `/testcases/{id}/edit`
- **THEN** the edit form is displayed in a full-width layout (not centered card style)
- **AND** form fields utilize the available horizontal space
- **AND** the layout matches the width pattern of list and view pages
