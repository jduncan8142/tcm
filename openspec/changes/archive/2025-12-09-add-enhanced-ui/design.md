## Context

The TCM application needs enhanced UI features for the dashboard and search functionality. The current dashboard is a placeholder showing a simple "Welcome" message. Users need:
1. A functional dashboard with statistics and quick actions
2. A global search feature to find content across test cases, projects, and tags

The application uses:
- FastAPI backend with REST API endpoints
- FastHTML for server-side rendered pages
- PostgreSQL database
- Existing reusable components (PageLayout, forms, etc.)

## Goals / Non-Goals

**Goals:**
- Create a functional dashboard with statistics from existing API endpoints
- Implement global search across all entities
- Maintain consistency with existing UI patterns and components
- Keep implementation simple and server-side rendered

**Non-Goals:**
- Real-time updates (would require WebSocket/SSE)
- Saved filter presets (requires user preferences)
- Export functionality (separate feature)
- Client-side JavaScript frameworks

## Decisions

### Dashboard Statistics
- **Decision:** Fetch counts from existing API endpoints on page load
- **Rationale:** Keeps implementation simple, no new API endpoints needed
- **Endpoints used:**
  - `GET /api/testcases` with limit=0 for count
  - `GET /api/projects` with limit=0 for count
  - `GET /api/tags` with limit=0 for count

### Recent Activity Feed
- **Decision:** Show recently modified entities based on `updated_at` timestamp
- **Rationale:** Simple to implement with existing data; no new tracking needed
- **Implementation:** Query each entity type sorted by updated_at, take top 5-10

### Global Search
- **Decision:** Client-side form submission to `/search` with server-side search
- **Rationale:** Simple implementation, no JavaScript required
- **Search strategy:** Use existing filtering capabilities on each API endpoint
  - TestCases: search by title (existing endpoint)
  - Projects: search by name (existing endpoint)
  - Tags: search by value/category (existing endpoint)

### Results Grouping
- **Decision:** Display results in tabs or sections by entity type
- **Rationale:** Clear organization, easy to scan results

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Dashboard may be slow with many entities | Use pagination/limits, cache counts if needed |
| Search across all entities requires multiple API calls | Execute in parallel, consider combined API later |
| No full-text search capability | Rely on LIKE queries via existing filtering |

## Migration Plan

No migration needed - these are new features that don't affect existing functionality.

1. Implement dashboard page and route
2. Update auth.py to use new dashboard page
3. Implement search page and route
4. Add navigation links to dashboard
5. Add tests for new pages

## Open Questions

- Should activity feed show all entity types or be configurable?
  - **Resolved:** Show all types, sorted by timestamp
- How many recent items to show in activity feed?
  - **Resolved:** 10 items maximum, configurable via constant
