# Change: Add Project Management Pages

## Why
The TCM application has a complete REST API for project management but lacks a user interface. Users need web pages to browse, create, edit, and view projects, as well as manage which test cases belong to each project. Projects are the primary organizational unit in TCM, so this UI is critical for usability.

## What Changes
- Add Projects List Page (`/projects`) with filtering and pagination
- Add Create Project Page (`/projects/new`) with form validation
- Add Edit Project Page (`/projects/{id}/edit`) with pre-populated form
- Add View Project Details Page (`/projects/{id}`) with test case management
- Reuse existing UI components (PageLayout, InputField, SubmitButton)
- Integrate with existing `/api/projects` endpoints

## Impact
- Affected specs: New `project-pages` capability
- Affected code: `src/tcm/pages/` (new page modules), `src/tcm/routes/` (page routes), `src/tcm/static/css/` (styles)
- No breaking changes to existing API
