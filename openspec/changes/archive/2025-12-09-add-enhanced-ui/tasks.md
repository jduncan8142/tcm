## 1. Dashboard Page Implementation

### 1.1 Dashboard Page Components
- [x] 1.1.1 Create `src/tcm/pages/dashboard/__init__.py` module
- [x] 1.1.2 Create `StatisticsWidget` component for displaying entity counts
- [x] 1.1.3 Create `ActivityFeedItem` component for activity feed entries
- [x] 1.1.4 Create `ActivityFeed` component to list recent items
- [x] 1.1.5 Create `QuickActions` component with navigation links
- [x] 1.1.6 Create `DashboardPage` function composing all components

### 1.2 Dashboard Route
- [x] 1.2.1 Create `src/tcm/routes/dashboard_pages.py` with route handler
- [x] 1.2.2 Implement statistics fetching from API (testcases, projects, tags counts)
- [x] 1.2.3 Implement recent activity query across all entity types
- [x] 1.2.4 Update `src/tcm/main.py` to include dashboard router
- [x] 1.2.5 Update `src/tcm/routes/auth.py` to redirect to new dashboard or integrate

### 1.3 Dashboard Styling
- [x] 1.3.1 Add statistics widget styles to `styles.css`
- [x] 1.3.2 Add activity feed styles to `styles.css`
- [x] 1.3.3 Add quick actions card styles to `styles.css`
- [x] 1.3.4 Add responsive breakpoints for dashboard layout

## 2. Global Search Page Implementation

### 2.1 Search Page Components
- [x] 2.1.1 Create `src/tcm/pages/search/__init__.py` module
- [x] 2.1.2 Create `SearchForm` component with text input and entity type filter
- [x] 2.1.3 Create `SearchResultItem` component for individual results
- [x] 2.1.4 Create `SearchResultsSection` component for grouped results
- [x] 2.1.5 Create `SearchPage` function with form and results display

### 2.2 Search Route
- [x] 2.2.1 Create `src/tcm/routes/search_pages.py` with GET handler
- [x] 2.2.2 Implement search logic calling existing API endpoints
- [x] 2.2.3 Implement result aggregation and grouping by entity type
- [x] 2.2.4 Update `src/tcm/main.py` to include search router

### 2.3 Search Filters
- [x] 2.3.1 Add status filter for test cases in search form
- [x] 2.3.2 Add status filter for projects in search form
- [x] 2.3.3 Add category filter for tags in search form
- [x] 2.3.4 Implement filter application in search logic

### 2.4 Search Styling
- [x] 2.4.1 Add search form styles to `styles.css`
- [x] 2.4.2 Add search results section styles to `styles.css`
- [x] 2.4.3 Add result item styles (per entity type) to `styles.css`
- [x] 2.4.4 Add responsive breakpoints for search page

## 3. Navigation Integration

- [x] 3.1 Add search link to dashboard quick actions
- [x] 3.2 Add search icon/link to page header (optional, depends on header design)

## 4. Testing

### 4.1 Dashboard Tests
- [x] 4.1.1 Create `tests/integration/test_dashboard_pages.py`
- [x] 4.1.2 Test dashboard page renders with statistics
- [x] 4.1.3 Test activity feed displays recent items
- [x] 4.1.4 Test quick action links are present and correct

### 4.2 Search Tests
- [x] 4.2.1 Create `tests/integration/test_search_pages.py`
- [x] 4.2.2 Test search page renders with form
- [x] 4.2.3 Test search returns results grouped by entity type
- [x] 4.2.4 Test search with specific entity type filter
- [x] 4.2.5 Test search with status/category filters
- [x] 4.2.6 Test search with no results displays empty state
