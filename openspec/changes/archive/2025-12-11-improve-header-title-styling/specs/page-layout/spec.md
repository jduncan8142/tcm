# page-layout Specification Delta

## MODIFIED Requirements

### Requirement: Clickable Header Title Navigation
The application title in the page header SHALL be clickable and navigate to the dashboard page.

#### Scenario: Header title maintains visual appearance
- **GIVEN** any page using PageLayout is displayed
- **WHEN** the header title is displayed as a link
- **THEN** the title SHALL maintain its current visual appearance as a header
- **AND** the link SHALL not display default browser link styling (blue text, underline)
- **AND** the title SHALL provide visual feedback on hover using the theme's accent color
- **AND** the hover effect SHALL be subtle and not use opacity changes
