# Change: Add Test Case Management Pages

## Why
The TCM application has a complete REST API for test case management but lacks a user interface. Users need web pages to browse, create, edit, and view test cases without using the API directly. This is essential for non-technical users and efficient test case management.

## What Changes
- Add Test Cases List Page (`/testcases`) with search, filtering, and pagination
- Add Create Test Case Page (`/testcases/new`) with form validation
- Add Edit Test Case Page (`/testcases/{id}/edit`) with pre-populated form
- Add View Test Case Details Page (`/testcases/{id}`) with read-only display
- Reuse existing UI components (PageLayout, InputField, SubmitButton)
- Integrate with existing `/api/testcases` endpoints

## Impact
- Affected specs: New `testcase-pages` capability
- Affected code: `src/tcm/pages/` (new page modules), `src/tcm/routes/` (page routes), `src/tcm/static/css/` (styles)
- No breaking changes to existing API
