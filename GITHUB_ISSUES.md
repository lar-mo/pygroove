# PyGroove - GitHub Issues Template

Copy/paste these into GitHub Issues at: https://github.com/lar-mo/pygroove/issues/new

---

## Issue 1: Add URL Slugs for SEO ✅

**Labels:** `enhancement`, `deployed`

### Description
Implement SEO-friendly URLs with slugs for albums and artists.

### Tasks
- [x] Add slug fields to Album and Artist models
- [x] Auto-generate slugs on save using slugify()
- [x] Update URL patterns to include slugs (album/<id>/<slug>/)
- [x] Add redirect views for backward compatibility
- [x] Update all templates to use slug-based URLs
- [x] Deploy to production

**Status:** Completed and deployed
**Commit:** f49c5aa

---

## Issue 2: Discogs Import with Rate Limiting ✅

**Labels:** `enhancement`, `deployed`

### Description
Import album tracks, artist bios, and metadata from Discogs API with proper rate limiting to avoid API throttling.

### Tasks
- [x] Add 1.5s delay between requests (~40 requests/min)
- [x] Fix query issues using Q objects for OR conditions
- [x] Import 271 albums with full track listings
- [x] Deploy to production and run import

**Results:** 3,709 tracks imported, 95% of albums complete
**Status:** Completed and deployed
**Commit:** d75f101

---

## Issue 3: Database Backup System ✅

**Labels:** `infrastructure`, `deployed`

### Description
Implement automated backups for SQLite database with local and off-site storage.

### Tasks
- [x] Create backup script with SQLite .backup command
- [x] Weekly automated backups (cron: Sundays at 2 AM)
- [x] 30-day retention with automatic cleanup
- [x] Off-site backup script for local downloads
- [x] Complete documentation in deployment/BACKUP.md

**Status:** Completed and deployed
**Files:** `/home/lar_mo/backup_pygroove.sh`, `deployment/download_backup.sh`
**Commit:** af75c8c

---

## Issue 4: Clean Discogs Markup in Bios ✅

**Labels:** `enhancement`, `data-quality`, `deployed`

### Description
Remove Discogs formatting markup from artist biographies for clean, readable text.

### Tasks
- [x] Remove [a=Artist] and [aXXXXX] tags
- [x] Remove [url=...]text[/url] tags
- [x] Remove [l=Label] and [r=Release] tags
- [x] Normalize Windows line endings (\r\n to \n)
- [x] Add explicit paragraph spacing in CSS
- [x] Create cleanup management command
- [x] Run cleanup on 162 artists
- [x] Deploy to production

**Results:** 127 artists cleaned up
**Status:** Completed and deployed
**Commit:** 38786fb, a17260e

---

## Issue 5: Import Artist Images from Discogs 🏃

**Labels:** `enhancement`, `in-progress`

### Description
Download and save artist images from Discogs to display on artist detail pages.

### Tasks
- [x] Create import_artist_images management command
- [x] Fix HTTP 403 errors with proper request headers
- [ ] Complete import for all 176 artists
- [ ] Verify images display correctly
- [ ] Deploy command to production
- [ ] Run import on production

**Status:** In Progress (currently running locally)
**Expected:** 170+ artist images

---

## Issue 6: Collection Sorting Options

**Labels:** `enhancement`, `backlog`

### Description
Add sorting options to the Collection page for better browsing experience.

### Tasks
- [ ] Add sort dropdown to collection page UI
- [ ] Implement sort by Artist Name (A-Z)
- [ ] Implement sort by Album Title (A-Z)
- [ ] Implement sort by Release Date (newest first)
- [ ] Implement sort by Genre
- [ ] Implement sort by Recently Added (current default)
- [ ] Store sort preference in session/URL param
- [ ] Update collection view queryset

**Priority:** Medium

---

## Issue 7: Artists List Page

**Labels:** `enhancement`, `backlog`

### Description
Create a dedicated Artists page to browse all artists with images and album counts.

### Tasks
- [ ] Create ArtistsListView (similar to CollectionView)
- [ ] Design grid layout with artist images
- [ ] Show album count per artist
- [ ] Add to main navigation
- [ ] Alphabetical sorting
- [ ] Create artist_list.html template

**Dependencies:** Issue #5 (Artist images)
**Priority:** Medium
**Reference:** https://www.aretemm.net/phpCDs/cdlistColumn.php?type=artist

---

## Issue 8: Custom Admin Panel with Tailwind

**Labels:** `enhancement`, `backlog`

### Description
Build a custom admin interface for managing albums, viewing checkout requests, and curating featured content.

### Tasks
- [ ] Create custom admin views (not Django admin)
- [ ] View checkout requests list
- [ ] Mark requests as fulfilled
- [ ] Toggle featured albums for homepage
- [ ] Bulk edit albums (genre, label, etc.)
- [ ] Analytics dashboard (most requested albums, popular genres)
- [ ] Style with Tailwind CSS

**Priority:** Low (Django admin works for now)

---

## Issue 9: Fix Album Name Typos

**Labels:** `bug`, `data-quality`, `backlog`

### Description
Manually correct album and artist name typos that prevent Discogs matching.

### Albums to Fix (14 total)
- [ ] "Permenant Waves" → "Permanent Waves" (Rush)
- [ ] "Ozzy Ozbourne - Tribute" → "Osbourne"
- [ ] "Laura Can Bite Me - Led Zeppelin III" → Fix artist name
- [ ] "Fila Brazilia - Anotherlatenight" → Check spelling
- [ ] "Jaco Pastorius - Live in New York City, Vol. 3" → Verify title
- [ ] "Various Artists - Qigong Massage Music" → Verify
- [ ] "Various Artists - Strung Out On OK Computer" → Verify
- [ ] "Ones And Zeros - Perception Is" → Verify
- [ ] "Earthride - Tree Of Life" → Verify spelling
- [ ] "Various Artists - Two Rooms: Celebrating..." → Verify
- [ ] "Various Artists - Hearts of Space: Universe Sampler 92" → Verify
- [ ] "Various Artists - Pure Moods, Vol. 2" → Verify
- [ ] "Warren Vache & Syncopatin' Seven - Warm Evenings" → Verify
- [ ] "Various Artists - Plastic Mutations - Electronic Tribute to Radiohead" → Verify

**After fixing:** Re-run `python manage.py import_discogs --missing-only`

**Priority:** Low

---

## Issue 10: Unit Tests

**Labels:** `testing`, `backlog`

### Description
Add comprehensive unit tests for models, views, and management commands.

### Tasks
- [ ] Test Album and Artist models (slugs, save methods)
- [ ] Test cart functionality
- [ ] Test checkout flow and email sending
- [ ] Test Discogs import command
- [ ] Test cleanup commands
- [ ] Set up pytest or Django TestCase
- [ ] Achieve >80% code coverage

**Priority:** Medium

---

## Issue 11: Cypress E2E Tests

**Labels:** `testing`, `backlog`

### Description
Add end-to-end tests for critical user workflows.

### Test Scenarios
- [ ] Browse collection and filter by genre
- [ ] View album detail page
- [ ] Add album to cart
- [ ] Complete checkout flow
- [ ] Search functionality
- [ ] Mobile responsiveness

**Priority:** Low

---

## Issue 12: CI/CD with GitHub Actions

**Labels:** `infrastructure`, `backlog`

### Description
Automate testing and deployment with GitHub Actions.

### Tasks
- [ ] Create workflow for running tests on PR
- [ ] Lint Python code (flake8/black)
- [ ] Run unit tests
- [ ] Auto-deploy to production on merge to main
- [ ] Set up environment secrets
- [ ] Add status badges to README

**Dependencies:** Issue #10 (Unit tests)
**Priority:** Low

---

## Issue 13: MySQL Migration (Optional)

**Labels:** `infrastructure`, `backlog`, `low-priority`

### Description
Evaluate and potentially migrate from SQLite to MySQL for production.

### Tasks
- [ ] Evaluate actual need (SQLite performing well)
- [ ] Create migration plan
- [ ] Test with MySQL locally
- [ ] Migrate data if needed
- [ ] Update deployment scripts

**Note:** SQLite is working fine for current scale (286 albums, 3,709 tracks)
**Priority:** Very Low (optional)

---

## Labels to Create

Create these labels in GitHub:
- `enhancement` - New features (green)
- `bug` - Something broken (red)
- `deployed` - Live in production (purple)
- `backlog` - Future work (gray)
- `in-progress` - Currently working (yellow)
- `infrastructure` - DevOps/deployment (blue)
- `data-quality` - Database cleanup (orange)
- `testing` - Tests and QA (light blue)
- `priority-high` - Urgent (red)
- `priority-medium` - Important (orange)
- `priority-low` - Nice to have (yellow)

---

## How to Use

1. Go to https://github.com/lar-mo/pygroove/issues
2. Click "New issue"
3. Copy/paste each issue above
4. Add appropriate labels
5. Create the issue

Then create a Project board to organize them!
