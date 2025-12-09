# Tasks: Add Project Management Pages

## 1. Shared Components
- [x] 1.1 Create date picker component for start/end dates (using HTML5 date inputs)
- [x] 1.2 Create status badge component
- [x] 1.3 Create test case selector component for project assignment (modal-based)

## 2. Projects List Page
- [x] 2.1 Create `src/tcm/pages/projects/list.py` with FastHTML page
- [x] 2.2 Implement status filtering (Active, Planning, Completed, On Hold)
- [ ] 2.3 Implement pagination with configurable page size (not implemented - basic list only)
- [x] 2.4 Display project name, status, date range, test case count
- [x] 2.5 Add quick action buttons (view, edit, delete)
- [x] 2.6 Add "Create New" button linking to create page
- [x] 2.7 Add loading states and error handling

## 3. Create Project Page
- [x] 3.1 Create `src/tcm/pages/projects/create.py` with FastHTML page
- [x] 3.2 Build form with fields: name, description, status, start_date, end_date
- [x] 3.3 Add date picker for start/end dates with validation
- [x] 3.4 Add client-side and server-side validation
- [x] 3.5 Handle form submission with success/error feedback
- [x] 3.6 Redirect to view page on successful creation

## 4. Edit Project Page
- [x] 4.1 Create `src/tcm/pages/projects/edit.py` with FastHTML page
- [x] 4.2 Fetch and pre-populate form with existing project data
- [x] 4.3 Add save and cancel buttons
- [x] 4.4 Handle 404 for non-existent projects
- [x] 4.5 Redirect to view page on successful update

## 5. View Project Details Page
- [x] 5.1 Create `src/tcm/pages/projects/view.py` with FastHTML page
- [x] 5.2 Display all project fields in read-only format
- [x] 5.3 Show project statistics (test case count, date range)
- [x] 5.4 Display list of test cases in the project
- [x] 5.5 Implement add/remove test cases functionality
- [x] 5.6 Add edit and delete action buttons
- [x] 5.7 Handle 404 for non-existent projects

## 6. Test Case Assignment
- [x] 6.1 Create test case picker modal/component
- [ ] 6.2 Implement search/filter for available test cases (not implemented - basic list only)
- [x] 6.3 Add "Add Test Case" functionality with API integration
- [x] 6.4 Add "Remove Test Case" functionality with confirmation
- [x] 6.5 Update test case list on project detail page after changes

## 7. Page Routes
- [x] 7.1 Create `src/tcm/routes/project_pages.py` with route handlers
- [x] 7.2 Register routes in main application
- [ ] 7.3 Add authentication/authorization checks (not implemented - no auth required yet)

## 8. Styling
- [x] 8.1 Add CSS styles for project pages
- [x] 8.2 Ensure responsive design for mobile/tablet/desktop
- [x] 8.3 Style date pickers and status badges

## 9. Testing
- [x] 9.1 Add integration tests for all page routes
- [x] 9.2 Test form validation scenarios
- [x] 9.3 Test test case assignment/removal
- [x] 9.4 Test error handling (404, validation errors)
