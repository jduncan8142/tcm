# Tasks: Add Tags Management Pages

## 1. Shared Components
- [x] 1.1 Create category dropdown/selector component
- [x] 1.2 Create tag badge/chip component for display
- [x] 1.3 Create category group accordion/collapsible component

## 2. Tags List Page
- [x] 2.1 Create `src/tcm/pages/tags/list.py` with FastHTML page
- [x] 2.2 Implement grouping by category
- [x] 2.3 Implement category filtering
- [x] 2.4 Display tag value, category, description, and predefined status
- [x] 2.5 Add quick action buttons (edit, delete)
- [x] 2.6 Add "Create New" button linking to create page
- [x] 2.7 Add loading states and error handling
- [x] 2.8 Visual distinction between predefined and custom tags

## 3. Create Tag Page
- [x] 3.1 Create `src/tcm/pages/tags/create.py` with FastHTML page
- [x] 3.2 Build form with fields: category, value, description, is_predefined
- [x] 3.3 Add category dropdown with existing categories and option to enter new
- [x] 3.4 Add client-side and server-side validation
- [x] 3.5 Handle duplicate tag detection (category + value combination)
- [x] 3.6 Handle form submission with success/error feedback
- [x] 3.7 Redirect to tags list on successful creation

## 4. Edit Tag Page
- [x] 4.1 Create `src/tcm/pages/tags/edit.py` with FastHTML page
- [x] 4.2 Fetch and pre-populate form with existing tag data
- [x] 4.3 Add save and cancel buttons
- [x] 4.4 Handle 404 for non-existent tags
- [x] 4.5 Handle duplicate detection on update
- [x] 4.6 Redirect to tags list on successful update

## 5. Page Routes
- [x] 5.1 Create `src/tcm/routes/tag_pages.py` with route handlers
- [x] 5.2 Register routes in main application
- [ ] 5.3 Add authentication/authorization checks

## 6. Styling
- [x] 6.1 Add CSS styles for tag pages
- [x] 6.2 Style tag badges with category-based colors
- [x] 6.3 Ensure responsive design for mobile/tablet/desktop
- [x] 6.4 Style category groups for visual organization

## 7. Testing
- [x] 7.1 Add integration tests for all page routes
- [x] 7.2 Test form validation scenarios
- [x] 7.3 Test duplicate detection
- [x] 7.4 Test category filtering
- [x] 7.5 Test error handling (404, validation errors)
