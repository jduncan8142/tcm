# Tasks: Add Test Case Management Pages

## 1. Shared Components
- [x] 1.1 Create reusable table component for list views
- [x] 1.2 Create pagination component
- [x] 1.3 Create filter/search bar component
- [x] 1.4 Create tag selector component for test case forms
- [x] 1.5 Create confirmation dialog component for delete actions

## 2. Test Cases List Page
- [x] 2.1 Create `src/tcm/pages/testcases/list.py` with FastHTML page
- [x] 2.2 Implement search functionality (title, description)
- [x] 2.3 Implement filtering by status, priority, and tags
- [x] 2.4 Implement pagination with configurable page size
- [x] 2.5 Add quick action buttons (view, edit, delete)
- [x] 2.6 Add "Create New" button linking to create page
- [x] 2.7 Add loading states and error handling

## 3. Create Test Case Page
- [x] 3.1 Create `src/tcm/pages/testcases/create.py` with FastHTML page
- [x] 3.2 Build form with fields: title, description, steps, expected_result, status, priority
- [x] 3.3 Implement tag selection/assignment UI
- [x] 3.4 Add client-side and server-side validation
- [x] 3.5 Handle form submission with success/error feedback
- [x] 3.6 Redirect to view page on successful creation

## 4. Edit Test Case Page
- [x] 4.1 Create `src/tcm/pages/testcases/edit.py` with FastHTML page
- [x] 4.2 Fetch and pre-populate form with existing test case data
- [x] 4.3 Implement tag management (add/remove tags)
- [x] 4.4 Add save and cancel buttons
- [x] 4.5 Handle 404 for non-existent test cases
- [x] 4.6 Redirect to view page on successful update

## 5. View Test Case Details Page
- [x] 5.1 Create `src/tcm/pages/testcases/view.py` with FastHTML page
- [x] 5.2 Display all test case fields in read-only format
- [x] 5.3 Show associated tags with visual styling
- [x] 5.4 Display projects using this test case
- [x] 5.5 Show audit trail (created_at, updated_at timestamps)
- [x] 5.6 Add edit and delete action buttons
- [x] 5.7 Handle 404 for non-existent test cases

## 6. Page Routes
- [x] 6.1 Create `src/tcm/routes/testcase_pages.py` with route handlers
- [x] 6.2 Register routes in main application
- [ ] 6.3 Add authentication/authorization checks

## 7. Styling
- [x] 7.1 Add CSS styles for test case pages
- [x] 7.2 Ensure responsive design for mobile/tablet/desktop
- [ ] 7.3 Implement loading spinners and skeleton states

## 8. Testing
- [x] 8.1 Add integration tests for all page routes
- [x] 8.2 Test form validation scenarios
- [x] 8.3 Test filtering and pagination
- [x] 8.4 Test error handling (404, validation errors)
