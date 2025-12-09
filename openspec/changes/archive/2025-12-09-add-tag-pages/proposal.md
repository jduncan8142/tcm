# Change: Add Tags Management Pages

## Why
The TCM application has a complete REST API for tag management but lacks a user interface. Tags are essential for categorizing and filtering test cases. Users need web pages to browse, create, and edit tags, particularly to manage the 40+ predefined tag categories and add custom tags as needed.

## What Changes
- Add Tags List Page (`/tags`) with category grouping and filtering
- Add Create Tag Page (`/tags/new`) with form validation
- Add Edit Tag Page (`/tags/{id}/edit`) with pre-populated form
- Reuse existing UI components (PageLayout, InputField, SubmitButton)
- Integrate with existing `/api/tags` endpoints

## Impact
- Affected specs: New `tag-pages` capability
- Affected code: `src/tcm/pages/` (new page modules), `src/tcm/routes/` (page routes), `src/tcm/static/css/` (styles)
- No breaking changes to existing API
