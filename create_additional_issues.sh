#!/bin/bash

# PyGroove - Additional GitHub Issues
# Phase 2 features and enhancements

REPO="lar-mo/pygroove"

echo "Creating additional GitHub Issues for PyGroove..."
echo ""

# Featured Albums on Homepage
gh issue create --repo $REPO \
  --title "Featured Albums on Homepage" \
  --label "enhancement,backlog,priority-medium" \
  --body "## Description
Add ability to feature select albums on the homepage for curation.

## Tasks
- [ ] Add \`featured\` BooleanField to Album model
- [ ] Create migration for new field
- [ ] Use Django admin to toggle featured flag
- [ ] Update homepage view to show featured albums when available
- [ ] Update homepage template to display featured section
- [ ] Add visual distinction for featured albums (e.g., \"Featured\" badge)

**Phase:** Homepage Curation
**Priority:** Medium" \
  --assignee "lar-mo"

echo "✓ Created: Featured Albums on Homepage"

# Full-text Search
gh issue create --repo $REPO \
  --title "Full-text Search Across Albums/Artists/Tracks" \
  --label "enhancement,backlog,priority-high" \
  --body "## Description
Implement comprehensive search functionality across the entire collection.

## Tasks
- [ ] Add full-text search across albums, artists, and tracks
- [ ] Search by genre, label, year range
- [ ] Implement autocomplete search box
- [ ] Add search filters/facets
- [ ] Update search UI with results highlighting
- [ ] Add \"No results found\" messaging
- [ ] Consider Django's PostgreSQL full-text search or simple icontains for SQLite

**Phase:** Search & Discovery
**Priority:** High" \
  --assignee "lar-mo"

echo "✓ Created: Full-text Search"

# Mobile Responsiveness
gh issue create --repo $REPO \
  --title "Mobile Responsiveness Improvements" \
  --label "enhancement,backlog,priority-medium" \
  --body "## Description
Audit and improve mobile experience across all pages.

## Tasks
- [ ] Test all pages on mobile devices (iPhone, Android)
- [ ] Fix layout issues on small screens
- [ ] Optimize touch targets (buttons, links)
- [ ] Test album grid layout on mobile
- [ ] Improve navigation menu for mobile
- [ ] Test checkout flow on mobile
- [ ] Add viewport meta tags if missing

**Phase:** User Experience
**Priority:** Medium" \
  --assignee "lar-mo"

echo "✓ Created: Mobile Responsiveness Improvements"

# Page Load Optimization
gh issue create --repo $REPO \
  --title "Page Load Optimization (Lazy Loading Images)" \
  --label "enhancement,backlog,priority-low" \
  --body "## Description
Improve page load performance with lazy loading and image optimization.

## Tasks
- [ ] Implement lazy loading for album cover images
- [ ] Implement lazy loading for artist images
- [ ] Add loading=\"lazy\" attribute to img tags
- [ ] Consider intersection observer for advanced lazy loading
- [ ] Test with Lighthouse performance score
- [ ] Optimize largest contentful paint (LCP)

**Phase:** User Experience
**Priority:** Low" \
  --assignee "lar-mo"

echo "✓ Created: Page Load Optimization"

# Album/Artist Detail Enhancements
gh issue create --repo $REPO \
  --title "Album/Artist Detail Page Enhancements" \
  --label "enhancement,backlog,priority-medium" \
  --body "## Description
Enhance detail pages with related content and better UX.

## Tasks
- [ ] Show related albums on album detail page (same artist)
- [ ] Show related albums on artist detail page (same genre)
- [ ] Add \"More by this artist\" section
- [ ] Add breadcrumb navigation
- [ ] Improve metadata display (year, label, genre)
- [ ] Add share buttons (optional)

**Phase:** User Experience
**Priority:** Medium" \
  --assignee "lar-mo"

echo "✓ Created: Album/Artist Detail Enhancements"

# Analytics Dashboard
gh issue create --repo $REPO \
  --title "Analytics Dashboard for Admin" \
  --label "enhancement,backlog,priority-low" \
  --body "## Description
Create analytics dashboard to track collection usage and checkout requests.

## Tasks
- [ ] Track most requested albums
- [ ] Track popular genres
- [ ] Track checkout request trends over time
- [ ] Display total albums, tracks, artists stats
- [ ] Add charts/graphs (Chart.js or similar)
- [ ] Create dedicated admin dashboard view
- [ ] Restrict access to authenticated admin users

**Phase:** Admin Features
**Priority:** Low
**Dependencies:** Custom admin panel (Issue #8)" \
  --assignee "lar-mo"

echo "✓ Created: Analytics Dashboard"

# Bulk Edit Albums
gh issue create --repo $REPO \
  --title "Bulk Edit Albums in Admin" \
  --label "enhancement,backlog,priority-low" \
  --body "## Description
Add ability to bulk edit album metadata in Django admin.

## Tasks
- [ ] Enable bulk edit in Django admin for albums
- [ ] Add bulk actions: update genre, update label, mark as featured
- [ ] Add bulk delete (with confirmation)
- [ ] Test with multiple albums selected
- [ ] Add success/error messaging

**Phase:** Admin Features
**Priority:** Low" \
  --assignee "lar-mo"

echo "✓ Created: Bulk Edit Albums"

# Email Templates
gh issue create --repo $REPO \
  --title "Email Templates for Checkout Responses" \
  --label "enhancement,backlog,priority-low" \
  --body "## Description
Create professional email templates for responding to checkout requests.

## Tasks
- [ ] Design email template for \"Request received\"
- [ ] Design email template for \"CDs ready for pickup\"
- [ ] Design email template for \"Request declined\" (out of stock)
- [ ] Use Django templates for email content
- [ ] Add HTML and plain-text versions
- [ ] Test email rendering in different clients
- [ ] Add unsubscribe link (if needed)

**Phase:** Admin Features
**Priority:** Low" \
  --assignee "lar-mo"

echo "✓ Created: Email Templates"

# Export Collection to CSV
gh issue create --repo $REPO \
  --title "Export Collection to CSV/Spreadsheet" \
  --label "enhancement,backlog,priority-low" \
  --body "## Description
Allow exporting entire collection to CSV for backup or external use.

## Tasks
- [ ] Create export view/management command
- [ ] Generate CSV with all album metadata
- [ ] Include tracks in export (optional separate file)
- [ ] Add download button in admin or collection page
- [ ] Test with large dataset (286+ albums)
- [ ] Consider Excel format (.xlsx) as alternative

**Phase:** Nice-to-Haves
**Priority:** Low" \
  --assignee "lar-mo"

echo "✓ Created: Export Collection to CSV"

# Social Meta Tags
gh issue create --repo $REPO \
  --title "Social Meta Tags for Album Sharing" \
  --label "enhancement,backlog,priority-low" \
  --body "## Description
Add Open Graph and Twitter Card meta tags for better social media sharing.

## Tasks
- [ ] Add Open Graph meta tags (og:title, og:image, og:description)
- [ ] Add Twitter Card meta tags
- [ ] Use album cover as og:image
- [ ] Test with Facebook sharing debugger
- [ ] Test with Twitter card validator
- [ ] Add dynamic meta tags per album/artist page

**Phase:** Nice-to-Haves
**Priority:** Low" \
  --assignee "lar-mo"

echo "✓ Created: Social Meta Tags"

# Rate Limiting on Checkout
gh issue create --repo $REPO \
  --title "Rate Limiting on Checkout Form (Prevent Spam)" \
  --label "enhancement,backlog,priority-medium" \
  --body "## Description
Implement rate limiting on checkout form to prevent spam and abuse.

## Tasks
- [ ] Add rate limiting middleware (django-ratelimit)
- [ ] Limit checkout requests per IP (e.g., 5 per hour)
- [ ] Add CAPTCHA (optional, if spam becomes an issue)
- [ ] Display friendly error message when rate limited
- [ ] Test rate limiting behavior
- [ ] Log rate limit violations

**Phase:** Security/Performance
**Priority:** Medium" \
  --assignee "lar-mo"

echo "✓ Created: Rate Limiting on Checkout"

# Image Optimization
gh issue create --repo $REPO \
  --title "Image Optimization and Compression" \
  --label "enhancement,backlog,priority-low" \
  --body "## Description
Optimize album covers and artist images for faster loading and reduced bandwidth.

## Tasks
- [ ] Install Pillow or similar for image processing
- [ ] Auto-resize images on upload (max width/height)
- [ ] Compress images without quality loss
- [ ] Convert to WebP format (modern browsers)
- [ ] Provide fallback for older browsers
- [ ] Test with existing 286 album covers + 166 artist images
- [ ] Measure bandwidth savings

**Phase:** Security/Performance
**Priority:** Low" \
  --assignee "lar-mo"

echo "✓ Created: Image Optimization"

echo ""
echo "✅ All 12 additional issues created successfully!"
echo ""
echo "View all issues: gh issue list --repo $REPO"
echo "Or visit: https://github.com/$REPO/issues"
