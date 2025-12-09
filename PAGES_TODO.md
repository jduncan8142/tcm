# TCM Pages - Specification TODO List

## Completed
- ✅ Login Page (`/login`)
- ✅ Dashboard Placeholder (`/dashboard`)

## High Priority - Core Functionality

### Test Cases Pages
- [ ] **Test Cases List Page** (`/testcases`)
  - Browse/search all test cases
  - Filter by status, priority, tags
  - Pagination
  - Quick actions (edit, delete, view)

- [ ] **Create Test Case Page** (`/testcases/new`)
  - Form with all test case fields
  - Tag selection/assignment
  - Validation

- [ ] **Edit Test Case Page** (`/testcases/{id}/edit`)
  - Pre-populated form
  - Tag management
  - Save/cancel actions

- [ ] **View Test Case Details** (`/testcases/{id}`)
  - Read-only view of test case
  - Associated tags display
  - Projects using this test case
  - Audit trail (created/updated timestamps)

### Projects Pages
- [ ] **Projects List Page** (`/projects`)
  - Browse all projects
  - Filter by status
  - Pagination
  - Quick actions

- [ ] **Create Project Page** (`/projects/new`)
  - Form with project details
  - Start/end dates
  - Status selection

- [ ] **Edit Project Page** (`/projects/{id}/edit`)
  - Pre-populated form
  - Update project details

- [ ] **View Project Details** (`/projects/{id}`)
  - Project information
  - List of test cases in project
  - Add/remove test cases
  - Project statistics

### Tags Management Pages
- [ ] **Tags List Page** (`/tags`)
  - Browse all tags
  - Group by category
  - Filter by category
  - Quick actions (edit, delete)

- [ ] **Create Tag Page** (`/tags/new`)
  - Form for category, value, description
  - Predefined flag

- [ ] **Edit Tag Page** (`/tags/{id}/edit`)
  - Update tag details

## Medium Priority - Enhanced Functionality

### Dashboard & Overview
- [ ] **Enhanced Dashboard** (`/dashboard`)
  - Replace placeholder with actual dashboard
  - Statistics widgets (total test cases, projects, tags)
  - Recent activity feed
  - Quick links to common actions

### Search & Filtering
- [ ] **Global Search Page** (`/search`)
  - Search across test cases, projects, tags
  - Advanced filters
  - Results grouping

- [ ] **Advanced Filter Page** (modal/sidebar)
  - Multi-criteria filtering
  - Save filter presets
  - Export filtered results

## Low Priority - Future Enhancements

### User Management (Post Azure AD Integration)
- [ ] **User Profile Page** (`/profile`)
  - View/edit user information
  - Preferences
  - Recent activity

- [ ] **User Settings Page** (`/settings`)
  - Application preferences
  - Notification settings
  - Display options

- [ ] **Admin User Management** (`/admin/users`)
  - User list
  - Role assignment
  - Permissions management

### Reporting & Analytics
- [ ] **Reports Dashboard** (`/reports`)
  - Available reports list
  - Generate reports

- [ ] **Test Execution Reports** (`/reports/execution`)
  - Test run results
  - Pass/fail statistics
  - Trends over time

- [ ] **Coverage Reports** (`/reports/coverage`)
  - Test coverage by module/system
  - Gap analysis

### Bulk Operations
- [ ] **Bulk Edit Page** (`/bulk/testcases` or `/bulk/tags`)
  - Multi-select test cases/tags
  - Bulk update fields
  - Bulk tag assignment
  - Bulk delete

### Import/Export
- [ ] **Import Page** (`/import`)
  - Upload CSV/Excel files
  - Map columns to fields
  - Preview and validate

- [ ] **Export Page** (`/export`)
  - Select data to export
  - Choose format (CSV, Excel, JSON)
  - Export options

## Navigation Components (Shared)
- [ ] **Main Navigation Bar**
  - Logo/branding
  - Main menu items
  - User menu (profile, logout)
  - Search bar

- [ ] **Sidebar Navigation** (optional)
  - Contextual navigation
  - Quick filters
  - Favorites

- [ ] **Breadcrumbs**
  - Page hierarchy
  - Quick navigation

## Recommended Implementation Order

1. **Phase 1 - Core CRUD** (Highest Priority)
   - Test Cases List, Create, Edit, View
   - Projects List, Create, Edit, View
   - Tags List, Create, Edit

2. **Phase 2 - Enhanced Dashboard & Navigation**
   - Enhanced Dashboard with statistics
   - Main Navigation Bar
   - Breadcrumbs

3. **Phase 3 - Search & Filtering**
   - Global Search
   - Advanced Filtering

4. **Phase 4 - Bulk Operations & Import/Export**
   - Bulk Edit
   - Import/Export functionality

5. **Phase 5 - Reporting** (Future)
   - Reports Dashboard
   - Test Execution Reports
   - Coverage Reports

6. **Phase 6 - User Management** (After Azure AD)
   - User Profile
   - User Settings
   - Admin User Management

## Design Considerations

- **Consistent Layout**: Reuse `PageLayout` component from login page
- **Form Components**: Extend existing `InputField`, `SubmitButton` components
- **Responsive**: All pages must work on mobile, tablet, desktop
- **Accessibility**: Keyboard navigation, screen reader support
- **Performance**: Pagination, lazy loading for large datasets
- **Error Handling**: Clear error messages, validation feedback
- **Loading States**: Spinners/skeletons during data fetch
