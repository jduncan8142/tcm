# Change: Add Enhanced UI Features (Dashboard & Search)

## Why
The current TCM application has a placeholder dashboard and lacks search/filtering capabilities beyond individual entity pages. Users need a functional dashboard with statistics and quick actions, plus a global search feature to find content across all entities (test cases, projects, tags). These are the "Medium Priority - Enhanced Functionality" items from the PAGES_TODO.md roadmap.

## What Changes
- **Enhanced Dashboard** (`/dashboard`):
  - Replace placeholder with statistics widgets (total test cases, projects, tags)
  - Add recent activity feed showing recently created/modified items
  - Provide quick links to common actions (create test case, create project, etc.)

- **Global Search Page** (`/search`):
  - Search across test cases, projects, and tags from a single interface
  - Display results grouped by entity type
  - Basic keyword search with filters for entity type

- **Advanced Filtering** (integrated into search):
  - Multi-criteria filtering by entity type, status, dates
  - Note: Save filter presets and export features deferred to future work

## Impact
- Affected specs: New `dashboard-pages` and `search-pages` capabilities
- Affected code:
  - `src/tcm/pages/dashboard/` (new dashboard page module)
  - `src/tcm/pages/search/` (new search page module)
  - `src/tcm/routes/auth.py` (modify existing dashboard route or create new)
  - `src/tcm/routes/dashboard_pages.py` (new route handler)
  - `src/tcm/routes/search_pages.py` (new route handler)
  - `src/tcm/main.py` (include new routers)
  - `src/tcm/static/css/styles.css` (dashboard and search styles)
- No breaking changes to existing API
- Reuses existing API endpoints for data retrieval

## Out of Scope (Future Work)
- Save filter presets (requires user preferences storage)
- Export filtered results (requires export functionality)
- Real-time activity updates (requires WebSocket or SSE)
