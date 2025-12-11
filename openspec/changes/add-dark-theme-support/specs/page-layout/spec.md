# page-layout Specification Delta

## ADDED Requirements

### Requirement: Theme Toggle Button in Header
The application SHALL provide a theme toggle button in the page header to allow users to switch between light and dark themes.

#### Scenario: Theme toggle button is displayed in header
- **GIVEN** any page using PageLayout is displayed
- **WHEN** the header is rendered
- **THEN** a theme toggle button SHALL be displayed in the header
- **AND** the button SHALL be positioned on the right side of the header

#### Scenario: Theme toggle button shows correct icon for light theme
- **GIVEN** the application is in light theme mode
- **WHEN** the header is rendered
- **THEN** the theme toggle button SHALL display a moon icon (🌙)
- **AND** the button SHALL have an accessible label indicating "Switch to dark theme"

#### Scenario: Theme toggle button shows correct icon for dark theme
- **GIVEN** the application is in dark theme mode
- **WHEN** the header is rendered
- **THEN** the theme toggle button SHALL display a sun icon (☀️)
- **AND** the button SHALL have an accessible label indicating "Switch to light theme"

#### Scenario: Theme toggle button is keyboard accessible
- **GIVEN** any page using PageLayout is displayed
- **WHEN** a user navigates to the theme toggle button using keyboard (Tab key)
- **THEN** the button SHALL be focusable
- **AND** the button SHALL have visible focus indication
- **AND** pressing Enter or Space SHALL trigger the theme toggle

#### Scenario: Theme toggle button is responsive
- **GIVEN** any page using PageLayout is displayed on a mobile device
- **WHEN** the viewport width is below 768px
- **THEN** the theme toggle button SHALL remain visible and functional
- **AND** the button SHALL be appropriately sized for touch interaction

### Requirement: Theme Application to Page Layout
The application SHALL apply the user's selected theme to the page layout based on their stored preference.

#### Scenario: User's theme preference is applied on page load
- **GIVEN** a user has a theme preference stored in their profile
- **WHEN** any page using PageLayout is loaded
- **THEN** the page SHALL apply the user's preferred theme (light or dark)
- **AND** the HTML element SHALL have a data-theme attribute matching the preference

#### Scenario: Default theme is light for new users
- **GIVEN** a user has no theme preference stored
- **WHEN** any page using PageLayout is loaded
- **THEN** the page SHALL apply the light theme by default
- **AND** the HTML element SHALL have data-theme="light" attribute

#### Scenario: Theme persists across page navigation
- **GIVEN** a user has selected a theme (light or dark)
- **WHEN** the user navigates to a different page
- **THEN** the selected theme SHALL remain applied
- **AND** the theme toggle button SHALL continue to show the correct icon

### Requirement: Dark Theme Visual Consistency
The application SHALL provide a consistent dark theme appearance based on Bootstrap's Darkly theme across all pages.

#### Scenario: Dark theme uses appropriate colors
- **GIVEN** the application is in dark theme mode
- **WHEN** any page using PageLayout is displayed
- **THEN** the background SHALL use dark colors (#222222 for primary, #303030 for secondary)
- **AND** the text SHALL use light colors (#ffffff for primary, #adb5bd for secondary)
- **AND** the primary accent color SHALL be #375a7f
- **AND** the success/accent color SHALL be #00bc8c

#### Scenario: Light theme uses appropriate colors
- **GIVEN** the application is in light theme mode
- **WHEN** any page using PageLayout is displayed
- **THEN** the background SHALL use light colors (#ffffff for primary, #ecf0f1 for secondary)
- **AND** the text SHALL use dark colors (#2c3e50 for primary, #7b8a8b for secondary)
- **AND** the primary accent color SHALL be #2c3e50
- **AND** the success/accent color SHALL be #18bc9c

#### Scenario: Theme transition is smooth
- **GIVEN** a user clicks the theme toggle button
- **WHEN** the theme changes from light to dark or dark to light
- **THEN** the theme SHALL change immediately without page reload
- **AND** all colors SHALL transition smoothly using CSS
- **AND** the theme toggle icon SHALL update to reflect the new theme
