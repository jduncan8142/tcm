# dashboard-pages Specification Delta

## ADDED Requirements

### Requirement: Clickable Statistics Widgets
The dashboard statistics widgets SHALL be clickable and navigate to the corresponding entity list pages.

#### Scenario: Test Cases card navigation
- **GIVEN** the dashboard page is displayed
- **WHEN** a user clicks on the Test Cases statistics widget
- **THEN** the application SHALL navigate to the test cases list page at `/testcases`

#### Scenario: Projects card navigation
- **GIVEN** the dashboard page is displayed
- **WHEN** a user clicks on the Projects statistics widget
- **THEN** the application SHALL navigate to the projects list page at `/projects`

#### Scenario: Tags card navigation
- **GIVEN** the dashboard page is displayed
- **WHEN** a user clicks on the Tags statistics widget
- **THEN** the application SHALL navigate to the tags list page at `/tags`

#### Scenario: Visual feedback on hover
- **GIVEN** the dashboard page is displayed
- **WHEN** a user hovers over a statistics widget
- **THEN** the widget SHALL provide visual feedback (e.g., cursor change, color change)
- **AND** the feedback SHALL indicate the widget is clickable

#### Scenario: Keyboard accessibility
- **GIVEN** the dashboard page is displayed
- **WHEN** a user navigates using keyboard (Tab key)
- **THEN** the statistics widgets SHALL be focusable
- **AND** pressing Enter on a focused widget SHALL navigate to the corresponding list page
