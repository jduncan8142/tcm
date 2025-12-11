# Proposal: Improve Header Title Styling

## Summary
Update the header title link styling to look more like a traditional title while maintaining clickability. Replace the opacity-based hover effect with a subtle highlight using the theme's accent color to provide better visual feedback that aligns with the application's design system.

## Motivation
The current header title link uses an opacity change (`opacity: 0.7`) on hover, which can make the title appear faded and less polished. The user wants:
- The title to look like a traditional header (not obviously a link)
- A subtle highlight effect on hover using the theme's accent color (`--primary-color`)
- Better integration with the application's overall design language

This change will:
- Improve visual polish and consistency
- Provide clearer hover feedback using the established color palette
- Maintain the clickable functionality while looking more like a title

## Scope
This change modifies the page-layout specification to:
- Update the hover effect styling for the header title link
- Replace opacity-based hover with a color-based highlight
- Use the theme's primary/accent color for consistency

## Impact
- **User Experience**: Better visual feedback that's consistent with the application's design
- **Code Changes**: Minimal - only affects CSS styling
- **Testing**: Existing tests remain valid; manual testing for visual verification

## Dependencies
None - this is a self-contained styling enhancement.

## Alternatives Considered
1. **Keep opacity-based hover**: Less polished, doesn't match design system
2. **Use background color change**: Could look too heavy for a header
3. **Use underline on hover**: More link-like, defeats the purpose of looking like a title

The chosen approach (color highlight) provides subtle feedback while maintaining the title appearance.
