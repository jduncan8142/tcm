## 1. Dashboard Page Implementation

### 1.1 Dashboard Page Components
- [ ] 1.1.1 Create `src/tcm/pages/dashboard/__init__.py` module
- [ ] 1.1.2 Create `StatisticsWidget` component for displaying entity counts
- [ ] 1.1.3 Create `ActivityFeedItem` component for activity feed entries
- [ ] 1.1.4 Create `ActivityFeed` component to list recent items
- [ ] 1.1.5 Create `QuickActions` component with navigation links
- [ ] 1.1.6 Create `DashboardPage` function composing all components

### 1.2 Dashboard Route
- [ ] 1.2.1 Create `src/tcm/routes/dashboard_pages.py` with route handler
- [ ] 1.2.2 Implement statistics fetching from API (testcases, projects, tags counts)
- [ ] 1.2.3 Implement recent activity query across all entity types
- [ ] 1.2.4 Update `src/tcm/main.py` to include dashboard router
- [ ] 1.2.5 Update `src/tcm/routes/auth.py` to redirect to new dashboard or integrate

### 1.3 Dashboard Styling
- [ ] 1.3.1 Add statistics widget styles to `styles.css`
- [ ] 1.3.2 Add activity feed styles to `styles.css`
- [ ] 1.3.3 Add quick actions card styles to `styles.css`
- [ ] 1.3.4 Add responsive breakpoints for dashboard layout

## 2. Global Search Page Implementation

### 2.1 Search Page Components
- [ ] 2.1.1 Create `src/tcm/pages/search/__init__.py` module
- [ ] 2.1.2 Create `SearchForm` component with text input and entity type filter
- [ ] 2.1.3 Create `SearchResultItem` component for individual results
- [ ] 2.1.4 Create `SearchResultsSection` component for grouped results
- [ ] 2.1.5 Create `SearchPage` function with form and results display

### 2.2 Search Route
- [ ] 2.2.1 Create `src/tcm/routes/search_pages.py` with GET handler
- [ ] 2.2.2 Implement search logic calling existing API endpoints
- [ ] 2.2.3 Implement result aggregation and grouping by entity type
- [ ] 2.2.4 Update `src/tcm/main.py` to include search router

### 2.3 Search Filters
- [ ] 2.3.1 Add status filter for test cases in search form
- [ ] 2.3.2 Add status filter for projects in search form
- [ ] 2.3.3 Add category filter for tags in search form
- [ ] 2.3.4 Implement filter application in search logic

### 2.4 Search Styling
- [ ] 2.4.1 Add search form styles to `styles.css`
- [ ] 2.4.2 Add search results section styles to `styles.css`
- [ ] 2.4.3 Add result item styles (per entity type) to `styles.css`
- [ ] 2.4.4 Add responsive breakpoints for search page

## 3. Navigation Integration

- [ ] 3.1 Add search link to dashboard quick actions
- [ ] 3.2 Add search icon/link to page header (optional, depends on header design)

## 4. Testing

### 4.1 Dashboard Tests
- [ ] 4.1.1 Create `tests/integration/test_dashboard_pages.py`
- [ ] 4.1.2 Test dashboard page renders with statistics
- [ ] 4.1.3 Test activity feed displays recent items
- [ ] 4.1.4 Test quick action links are present and correct

### 4.2 Search Tests
- [ ] 4.2.1 Create `tests/integration/test_search_pages.py`
- [ ] 4.2.2 Test search page renders with form
- [ ] 4.2.3 Test search returns results grouped by entity type
- [ ] 4.2.4 Test search with specific entity type filter
- [ ] 4.2.5 Test search with status/category filters
- [ ] 4.2.6 Test search with no results displays empty state
