#!/bin/bash

# PyGroove - GitHub Issues Creation Script
# Creates all issues from GITHUB_ISSUES.md using GitHub CLI

REPO="lar-mo/pygroove"

echo "Creating GitHub Issues for PyGroove..."
echo "Repository: $REPO"
echo ""

# First, create the labels
echo "Creating labels..."
gh label create "enhancement" --color "0E8A16" --description "New features" --repo $REPO 2>/dev/null || echo "Label 'enhancement' already exists"
gh label create "bug" --color "D73A4A" --description "Something broken" --repo $REPO 2>/dev/null || echo "Label 'bug' already exists"
gh label create "deployed" --color "7057FF" --description "Live in production" --repo $REPO 2>/dev/null || echo "Label 'deployed' already exists"
gh label create "backlog" --color "D4C5F9" --description "Future work" --repo $REPO 2>/dev/null || echo "Label 'backlog' already exists"
gh label create "in-progress" --color "FBCA04" --description "Currently working" --repo $REPO 2>/dev/null || echo "Label 'in-progress' already exists"
gh label create "infrastructure" --color "0052CC" --description "DevOps/deployment" --repo $REPO 2>/dev/null || echo "Label 'infrastructure' already exists"
gh label create "data-quality" --color "FF9900" --description "Database cleanup" --repo $REPO 2>/dev/null || echo "Label 'data-quality' already exists"
gh label create "testing" --color "5EBEFF" --description "Tests and QA" --repo $REPO 2>/dev/null || echo "Label 'testing' already exists"
gh label create "priority-high" --color "D73A4A" --description "Urgent" --repo $REPO 2>/dev/null || echo "Label 'priority-high' already exists"
gh label create "priority-medium" --color "FF9900" --description "Important" --repo $REPO 2>/dev/null || echo "Label 'priority-medium' already exists"
gh label create "priority-low" --color "FBCA04" --description "Nice to have" --repo $REPO 2>/dev/null || echo "Label 'priority-low' already exists"

echo ""
echo "Creating issues..."
echo ""

# Issue 1: Add URL Slugs for SEO (COMPLETED)
gh issue create --repo $REPO \
  --title "Add URL Slugs for SEO" \
  --label "enhancement,deployed" \
  --body "## Description
Implement SEO-friendly URLs with slugs for albums and artists.

## Tasks
- [x] Add slug fields to Album and Artist models
- [x] Auto-generate slugs on save using slugify()
- [x] Update URL patterns to include slugs (album/<id>/<slug>/)
- [x] Add redirect views for backward compatibility
- [x] Update all templates to use slug-based URLs
- [x] Deploy to production

**Status:** ✅ Completed and deployed
**Commit:** f49c5aa" \
  --assignee "lar-mo"

echo "✓ Created Issue 1: Add URL Slugs for SEO"

# Issue 2: Discogs Import with Rate Limiting (COMPLETED)
gh issue create --repo $REPO \
  --title "Discogs Import with Rate Limiting" \
  --label "enhancement,deployed" \
  --body "## Description
Import album tracks, artist bios, and metadata from Discogs API with proper rate limiting to avoid API throttling.

## Tasks
- [x] Add 1.5s delay between requests (~40 requests/min)
- [x] Fix query issues using Q objects for OR conditions
- [x] Import 271 albums with full track listings
- [x] Deploy to production and run import

**Results:** 3,709 tracks imported, 95% of albums complete
**Status:** ✅ Completed and deployed
**Commit:** d75f101" \
  --assignee "lar-mo"

echo "✓ Created Issue 2: Discogs Import with Rate Limiting"

# Issue 3: Database Backup System (COMPLETED)
gh issue create --repo $REPO \
  --title "Database Backup System" \
  --label "infrastructure,deployed" \
  --body "## Description
Implement automated backups for SQLite database with local and off-site storage.

## Tasks
- [x] Create backup script with SQLite .backup command
- [x] Weekly automated backups (cron: Sundays at 2 AM)
- [x] 30-day retention with automatic cleanup
- [x] Off-site backup script for local downloads
- [x] Complete documentation in deployment/BACKUP.md

**Status:** ✅ Completed and deployed
**Files:** \`/home/lar_mo/backup_pygroove.sh\`, \`deployment/download_backup.sh\`
**Commit:** af75c8c" \
  --assignee "lar-mo"

echo "✓ Created Issue 3: Database Backup System"

# Issue 4: Clean Discogs Markup in Bios (COMPLETED)
gh issue create --repo $REPO \
  --title "Clean Discogs Markup in Artist Bios" \
  --label "enhancement,data-quality,deployed" \
  --body "## Description
Remove Discogs formatting markup from artist biographies for clean, readable text.

## Tasks
- [x] Remove [a=Artist] and [aXXXXX] tags
- [x] Remove [url=...]text[/url] tags
- [x] Remove [l=Label] and [r=Release] tags
- [x] Normalize Windows line endings (\r\n to \n)
- [x] Add explicit paragraph spacing in CSS
- [x] Create cleanup management command
- [x] Run cleanup on 162 artists
- [x] Deploy to production

**Results:** 127 artists cleaned up
**Status:** ✅ Completed and deployed
**Commits:** 38786fb, a17260e" \
  --assignee "lar-mo"

echo "✓ Created Issue 4: Clean Discogs Markup in Bios"

# Issue 5: Import Artist Images from Discogs (IN PROGRESS)
gh issue create --repo $REPO \
  --title "Import Artist Images from Discogs" \
  --label "enhancement,deployed" \
  --body "## Description
Download and save artist images from Discogs to display on artist detail pages.

## Tasks
- [x] Create import_artist_images management command
- [x] Fix HTTP 403 errors with proper request headers
- [x] Complete import for all 176 artists
- [x] Verify images display correctly
- [x] Deploy command to production
- [x] Run import on production

**Results:** 
- Local: 63 artist images imported
- Production: 166 artist images imported
**Status:** ✅ Completed and deployed
**Commit:** 761959c" \
  --assignee "lar-mo"

echo "✓ Created Issue 5: Import Artist Images from Discogs"

# Issue 6: Collection Sorting Options (BACKLOG)
gh issue create --repo $REPO \
  --title "Collection Sorting Options" \
  --label "enhancement,backlog,priority-medium" \
  --body "## Description
Add sorting options to the Collection page for better browsing experience.

## Tasks
- [ ] Add sort dropdown to collection page UI
- [ ] Implement sort by Artist Name (A-Z)
- [ ] Implement sort by Album Title (A-Z)
- [ ] Implement sort by Release Date (newest first)
- [ ] Implement sort by Genre
- [ ] Implement sort by Recently Added (current default)
- [ ] Store sort preference in session/URL param
- [ ] Update collection view queryset

**Priority:** Medium" \
  --assignee "lar-mo"

echo "✓ Created Issue 6: Collection Sorting Options"

# Issue 7: Artists List Page (BACKLOG)
gh issue create --repo $REPO \
  --title "Artists List Page" \
  --label "enhancement,backlog,priority-medium" \
  --body "## Description
Create a dedicated Artists page to browse all artists with images and album counts.

## Tasks
- [ ] Create ArtistsListView (similar to CollectionView)
- [ ] Design grid layout with artist images
- [ ] Show album count per artist
- [ ] Add to main navigation
- [ ] Alphabetical sorting
- [ ] Create artist_list.html template

**Dependencies:** Issue #5 (Artist images) ✅ Complete
**Priority:** Medium
**Reference:** https://www.aretemm.net/phpCDs/cdlistColumn.php?type=artist" \
  --assignee "lar-mo"

echo "✓ Created Issue 7: Artists List Page"

# Issue 8: Custom Admin Panel with Tailwind (BACKLOG)
gh issue create --repo $REPO \
  --title "Custom Admin Panel with Tailwind" \
  --label "enhancement,backlog,priority-low" \
  --body "## Description
Build a custom admin interface for managing albums, viewing checkout requests, and curating featured content.

## Tasks
- [ ] Create custom admin views (not Django admin)
- [ ] View checkout requests list
- [ ] Mark requests as fulfilled
- [ ] Toggle featured albums for homepage
- [ ] Bulk edit albums (genre, label, etc.)
- [ ] Analytics dashboard (most requested albums, popular genres)
- [ ] Style with Tailwind CSS

**Priority:** Low (Django admin works for now)" \
  --assignee "lar-mo"

echo "✓ Created Issue 8: Custom Admin Panel with Tailwind"

# Issue 9: Fix Album Name Typos (BACKLOG)
gh issue create --repo $REPO \
  --title "Fix Album Name Typos" \
  --label "bug,data-quality,backlog,priority-low" \
  --body "## Description
Manually correct album and artist name typos that prevent Discogs matching.

## Albums to Fix (14 total)
- [ ] \"Permenant Waves\" → \"Permanent Waves\" (Rush)
- [ ] \"Ozzy Ozbourne - Tribute\" → \"Osbourne\"
- [ ] \"Laura Can Bite Me - Led Zeppelin III\" → Fix artist name
- [ ] \"Fila Brazilia - Anotherlatenight\" → Check spelling
- [ ] \"Jaco Pastorius - Live in New York City, Vol. 3\" → Verify title
- [ ] \"Various Artists - Qigong Massage Music\" → Verify
- [ ] \"Various Artists - Strung Out On OK Computer\" → Verify
- [ ] \"Ones And Zeros - Perception Is\" → Verify
- [ ] \"Earthride - Tree Of Life\" → Verify spelling
- [ ] \"Various Artists - Two Rooms: Celebrating...\" → Verify
- [ ] \"Various Artists - Hearts of Space: Universe Sampler 92\" → Verify
- [ ] \"Various Artists - Pure Moods, Vol. 2\" → Verify
- [ ] \"Warren Vache & Syncopatin' Seven - Warm Evenings\" → Verify
- [ ] \"Various Artists - Plastic Mutations - Electronic Tribute to Radiohead\" → Verify

**After fixing:** Re-run \`python manage.py import_discogs --missing-only\`

**Priority:** Low" \
  --assignee "lar-mo"

echo "✓ Created Issue 9: Fix Album Name Typos"

# Issue 10: Unit Tests (BACKLOG)
gh issue create --repo $REPO \
  --title "Unit Tests" \
  --label "testing,backlog,priority-medium" \
  --body "## Description
Add comprehensive unit tests for models, views, and management commands.

## Tasks
- [ ] Test Album and Artist models (slugs, save methods)
- [ ] Test cart functionality
- [ ] Test checkout flow and email sending
- [ ] Test Discogs import command
- [ ] Test cleanup commands
- [ ] Set up pytest or Django TestCase
- [ ] Achieve >80% code coverage

**Priority:** Medium" \
  --assignee "lar-mo"

echo "✓ Created Issue 10: Unit Tests"

# Issue 11: Cypress E2E Tests (BACKLOG)
gh issue create --repo $REPO \
  --title "Cypress E2E Tests" \
  --label "testing,backlog,priority-low" \
  --body "## Description
Add end-to-end tests for critical user workflows.

## Test Scenarios
- [ ] Browse collection and filter by genre
- [ ] View album detail page
- [ ] Add album to cart
- [ ] Complete checkout flow
- [ ] Search functionality
- [ ] Mobile responsiveness

**Priority:** Low" \
  --assignee "lar-mo"

echo "✓ Created Issue 11: Cypress E2E Tests"

# Issue 12: CI/CD with GitHub Actions (BACKLOG)
gh issue create --repo $REPO \
  --title "CI/CD with GitHub Actions" \
  --label "infrastructure,backlog,priority-low" \
  --body "## Description
Automate testing and deployment with GitHub Actions.

## Tasks
- [ ] Create workflow for running tests on PR
- [ ] Lint Python code (flake8/black)
- [ ] Run unit tests
- [ ] Auto-deploy to production on merge to main
- [ ] Set up environment secrets
- [ ] Add status badges to README

**Dependencies:** Issue #10 (Unit tests)
**Priority:** Low" \
  --assignee "lar-mo"

echo "✓ Created Issue 12: CI/CD with GitHub Actions"

# Issue 13: MySQL Migration (Optional) (BACKLOG)
gh issue create --repo $REPO \
  --title "MySQL Migration (Optional)" \
  --label "infrastructure,backlog,priority-low" \
  --body "## Description
Evaluate and potentially migrate from SQLite to MySQL for production.

## Tasks
- [ ] Evaluate actual need (SQLite performing well)
- [ ] Create migration plan
- [ ] Test with MySQL locally
- [ ] Migrate data if needed
- [ ] Update deployment scripts

**Note:** SQLite is working fine for current scale (286 albums, 3,709 tracks)
**Priority:** Very Low (optional)" \
  --assignee "lar-mo"

echo "✓ Created Issue 13: MySQL Migration (Optional)"

echo ""
echo "✅ All issues created successfully!"
echo ""
echo "Next steps:"
echo "1. View issues: gh issue list --repo $REPO"
echo "2. Create a Project board to organize them"
echo "3. Visit: https://github.com/$REPO/issues"
