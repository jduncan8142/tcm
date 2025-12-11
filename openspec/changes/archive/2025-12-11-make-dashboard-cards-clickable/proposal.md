# Proposal: Make Dashboard Cards Clickable

## Summary
Add clickable navigation to the dashboard statistics cards so users can quickly navigate to the list pages for test cases, projects, and tags by clicking on the corresponding statistics widget.

## Motivation
Currently, the dashboard displays statistics widgets showing counts for test cases, projects, and tags, but these widgets are static. Users must use the Quick Actions section or navigation menu to browse these entities. Making the statistics widgets clickable provides a more intuitive and efficient way to navigate to these commonly accessed pages.

## Scope
This change modifies the dashboard-pages specification to:
- Add a new requirement for clickable statistics widgets
- Update the `StatisticsWidget` component to support navigation links
- Wire up the statistics cards to navigate to the appropriate list pages

## Impact
- **User Experience**: Improved navigation efficiency and discoverability
- **Code Changes**: Minimal - only affects the dashboard page component
- **Testing**: Requires updates to dashboard page tests to verify navigation links

## Dependencies
None - this is a self-contained enhancement to existing dashboard functionality.

## Alternatives Considered
1. **Keep current design with Quick Actions only**: Less intuitive, requires extra clicks
2. **Add separate "View All" buttons below each widget**: More cluttered, less elegant

The chosen approach (clickable cards) is the most common pattern in dashboard interfaces and provides the best user experience.
