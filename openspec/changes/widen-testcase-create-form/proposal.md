# Change: Widen Test Case Create Form

## Why
The test case creation form at `/testcases/new` is currently constrained to a narrow 400px width, making it cramped and difficult to use with the multiple text areas and fields. The edit form already uses a wider 1200px layout, creating an inconsistency. Users need a comfortable form layout that fills the available screen width and adapts responsively to different device sizes.

## What Changes
- **Create Page Layout**: Change create page container from `container` (400px max-width) to `container container-wide` (1200px max-width)
- **Layout Consistency**: Align create form width with edit form width for consistent user experience
- **Responsive Behavior**: Form already adapts to 100% width on mobile devices (no CSS changes needed)

## Impact
- **Affected specs**: testcase-pages (MODIFIED "Create Test Case Page" requirement to add form layout scenario)
- **Affected code**:
  - Modified: `src/tcm/pages/testcases/create.py` (line 184: change container class)
  - Tests: Update test to verify container-wide class is present
- **User Experience**: Improved usability with more comfortable form layout, especially for multi-line text fields
- **Consistency**: Create and edit forms now have matching layouts
- **Responsive**: Form continues to work on all device sizes (existing responsive CSS already handles this)
