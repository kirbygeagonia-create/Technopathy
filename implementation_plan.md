# Technopath v4 — Full Codebase Audit Plan

## Background

Technopath is a Vue 3 PWA campus-guide app for SEAIT. Its **primary users are on mobile (Android & iOS)**. The app features an interactive map (HomeView), a route finder (NavigateView), a chatbot, QR scanner, notifications, settings, and an admin panel. All CSS is externalized from `.vue` files into `/src/assets/*.css`.

This audit covers: **Code Health**, **UI/UX**, and **Mobile Responsiveness (top priority)**.

---

## 1. Mobile Responsiveness — CRITICAL (Top Priority)

### 1.1 — HomeView: Search Bar Position Conflict
**Severity: Critical**

**What's wrong:**
The mobile search bar lives inside `.bottom-controls` which is `position: fixed; bottom: 76px`. The bottom nav (`.app-bottom-nav`) is `position: fixed; bottom: 0; height: 64px`. The `.app-content-area` parent uses `padding-bottom: 72px`. This creates a **stacking conflict**:

- On small Androids (360–375px wide), the 5 action buttons (`menu-btn` + 4 `action-btn`) in `.action-buttons` + the `menu-btn` row have a combined width of `36px * 5 + gaps ~30px ≈ 210px`. The row container is `display: flex; justify-content: space-between`, which works, but on **320px** screens the buttons will begin to crowd.
- The search bar sits at `bottom: 76px`. The bottom nav is 64px tall. This means the search bar bottom edge is at `76px` above the bottom of the viewport — but the nav occupies `0–64px`. This gives only `12px` visible gap: on iOS with a home indicator (safe-area-inset-bottom ≈ 34px), the search bar visually overlaps the bottom nav.
- `.app-bottom-nav` uses `padding-bottom: var(--safe-bottom)` but `.bottom-controls` uses a hardcoded `bottom: 76px` — it does **not** account for `--safe-bottom`. On iPhone 14/15 this means the search bar overlaps the home indicator bar.

**Fix strategy:**
Replace hardcoded `bottom: 76px` with `bottom: calc(64px + var(--safe-bottom, 0px) + 12px)` to dynamically account for iOS safe area. Same fix for the `@media (max-width: 768px)` override that also uses `bottom: 76px`.

---

### 1.2 — HomeView: Dropdown Selectors Absolute over Map
**Severity: Critical**

**What's wrong:**
`.top-selectors` is `position: absolute; top: 56px; left: 12px; right: 12px`. On screens narrower than 360px, two side-by-side dropdowns inside a flex row each take `flex: 1`. Their headers have `padding: 8px 10px; font-size: 12px`, which is workable — but:

- When either dropdown **expands**, its content (`max-height: 200px; overflow-y: auto`) overlaps the map surface entirely, pushing clickable map content under the dropdown — they share the same stacking context with `z-index: 100`.
- The `top: 56px` offset assumes the mobile top bar is exactly 56px. The `--top-bar-height` variable is defined as `56px`, but when used with `--safe-top` (e.g., iPhone notch adds 44–59px to safe area), the **entire selector region drops behind or over the notch area**.

**Fix strategy:**
Change `.top-selectors` `top` to use `calc(var(--top-bar-height) + var(--safe-top, 0px) + 8px)`. There is no top bar rendered on HomeView mobile — the top-selectors sit directly at the top of the screen, so the correct `top` should simply be `calc(var(--safe-top, 0px) + 8px)` (verified: HomeView has no `.top-bar` element). The 56px offset is **wrong and creates a layout gap**.

---

### 1.3 — HomeView: Search Suggestions / Recent Searches Overlap
**Severity: Critical**

**What's wrong:**
Both `.search-suggestions` and `.recent-searches` use:
```css
/* Desktop */
top: 80px; left: 16px; right: 16px;

/* Mobile override */
bottom: 140px; left: 12px; right: 12px;
```
The mobile bottom value of `140px` is hardcoded. At `bottom: 76px` (search bar) + `~50px` (search bar height) = ~126px, a 140px value gives only ~14px gap — this is fine on large phones but **collapses to overlap on 320–360px height screens** (e.g., short Androids). Also, when the keyboard opens on Android, the viewport shrinks and `bottom: 140px` can push the suggestions **completely off screen above the keyboard**.

**Fix strategy:**
Switch to a CSS-column approach — render suggestions **directly above the search input** using relative positioning within the bottom-controls stack, not absolute/fixed positioning anchored from the bottom. Alternatively, use a `position: absolute; bottom: 100%` on the search container itself. This avoids hardcoded pixel anchoring entirely.

---

### 1.4 — NavigateView: Map Image Fixed 800px Width
**Severity: Major**

**What's wrong:**
```css
/* navigate.css */
.navview-map-img { width: 800px; height: auto; }
.navview-route-svg { width: 800px; height: 600px; }
```
The map image is hardcoded to `800px` wide regardless of viewport. On a 360px mobile screen, only 45% of the map is visible initially. The route SVG overlay is also fixed at `800×600` with `preserveAspectRatio="none"` — meaning route lines are correctly drawn relative to the 800px coordinate space, but when the user pans/zooms there is no `max-width` constraint to prevent the image from becoming narrower than the SVG overlay.

The `transformOrigin: '0 0'` in NavigateView means zooming is anchored top-left — on small screens this feels unnatural (users expect pinch-zoom to be centered at the pinch point).

**Fix strategy:**
Set an initial scale on mount so the map fills the viewport width: `initialScale = containerWidth / 800`. Center the initial transform. Switch `transformOrigin` to `'50% 50%'` for centered zoom, adjusting pan logic accordingly. The SVG overlay should remain at `800×600` in its own coordinate space (it's correct), but the initial view should be scaled to fit.

---

### 1.5 — MapView (Explore): Same 800px Hardcoded Width
**Severity: Major**

**What's wrong:**
```css
/* mapview.css */
.mapview-svg { width: 800px; }
```
Same issue as NavigateView. Additionally, `.mapview-filters` (chip row) is positioned:
```css
top: calc(56px + var(--safe-top) + var(--space-3));
```
The header here IS rendered (`mapview-header` exists), so this calculation is correct — however on small screens (320–360px) the two filter chips (`Facilities`, `Rooms`) may overflow to the right. There is no `flex-wrap` or `max-width` guard. On 320px screens: `2 chips × ~90px each + gap = ~190px`, which fits, but just barely.

**Fix strategy:**
Same initial-scale strategy as NavigateView. Add `flex-wrap: wrap` to `.mapview-filters` as a safeguard.

---

### 1.6 — App.vue: `isDesktop` Uses Simple `window.innerWidth`, No Orientation Handling
**Severity: Major**

**What's wrong:**
```js
const isDesktop = computed(() => windowWidth.value >= 1024)
```
When a tablet is in **landscape orientation** (e.g., iPad 1024px wide), the app switches to desktop layout. But there is no debouncing on the resize listener — rapid resize events (or keyboard pop-up on Android causing viewport resize) will trigger re-renders. More critically, on **Android Chrome**, opening the software keyboard resizes `window.innerWidth` (in some configurations), which could briefly flip the layout.

**Fix strategy:**
Add a `debounce` (100–150ms) to `updateWindowWidth`. Consider also checking `window.innerHeight` > some threshold to better detect keyboard-caused viewport shrinkage. For the breakpoint, `1024px` is fine but worth documenting that this is the canonical mobile/desktop boundary.

---

### 1.7 — Bottom Nav: Only 3 Items on Mobile — Feature Discoverability Gap
**Severity: Major**

**What's wrong:**
```js
const mobileMenuItems = [
  { path: '/', label: 'Home', icon: 'home' },
  { path: '/navigate', label: 'Navigate', icon: 'explore' },
  { path: '/settings', label: 'Settings', icon: 'settings' },
]
```
Key features — Chatbot, QR Scanner, Notifications, Feedback, Favorites — are **hidden on mobile** and only accessible via the `menu-btn` slide-up sheet on HomeView, or not at all from other views (e.g., you cannot reach chatbot from NavigateView or SettingsView without going back to Home first). This is a significant discoverability concern.

**Fix strategy:**
Expand mobile nav to 4–5 items (Home, Navigate, Chatbot/QR, Settings, and a "More" overflow for others). Alternatively, ensure all views have a consistent header that exposes key actions.

---

### 1.8 — Notifications View: No `flex` on `.notifications-view`, Content Doesn't Fill Screen
**Severity: Major**

**What's wrong:**
```css
.notifications-view { height: 100%; width: 100%; }
```
This does not include `display: flex; flex-direction: column`. The inner `.notifications-main-content { flex: 1; overflow-y: auto }` has `flex: 1` but its parent is not a flex container, so `flex: 1` has **no effect**. The content area will not expand to fill the screen, causing the empty-state or short lists to not center properly below the header.

**Fix strategy:**
Add `display: flex; flex-direction: column;` to `.notifications-view`.

---

### 1.9 — `viewport` meta: `user-scalable=no` Blocks Accessibility Zoom
**Severity: Major**

**What's wrong:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
```
`user-scalable=no` prevents pinch-to-zoom at the browser level. This is an **accessibility violation** (WCAG 1.4.4 — Resize Text) and is ignored by iOS Safari 10+ anyway. Since the map has its own pinch-zoom handler this is doubly unnecessary.

**Fix strategy:**
Remove `maximum-scale=1.0, user-scalable=no`. Implement pinch-to-zoom prevention **only within the map container** using `touch-action: none` and the existing `onTouchMove` handler (already done in NavigateView and HomeView).

---

### 1.10 — `bottom-controls` Conflicts with `app-content-area` padding
**Severity: Major**

**What's wrong:**
`.app-content-area` has `padding-bottom: 72px` (for the bottom nav). But `.bottom-controls` is `position: fixed` — it sits on top of content, **not within the scroll flow**. On the HomeView the map (`map-wrapper`) takes `flex: 1` within `.home-view`, but `.home-view` also includes `.top-selectors` (absolute) and `.bottom-controls` (fixed). The `map-wrapper` correctly takes remaining height. However, when the `marker-info-popup` is shown at `bottom: 180px` (desktop: `bottom: 160px` mobile), this overlaps with `bottom-controls` at `bottom: 76px` — the popup sits at 180px and the controls extend ~180px total (76px base + ~100px for the action row + search bar), meaning **the popup and controls overlap**.

**Fix strategy:**
Increase `.marker-info-popup` bottom offset to `calc(164px + var(--safe-bottom, 0px))` where 164px = 76px (controls base) + 88px (action-row + search bar height). Or restructure into a stacking z-index hierarchy where popup is always fully above controls.

---

### 1.11 — Touch Target Sizes Below 44px Minimum
**Severity: Major**

Multiple components use touch targets smaller than the 44×44px minimum:

| Element | Actual Size |
|---|---|
| `.navview-back-btn` | 40×40px |
| `.navview-clear-btn` | 46×46px ✓ |
| `.navview-route-close` | 32×32px ❌ |
| `.mapview-legend-close` | 24×24px ❌ |
| `.feedback-top-bar-icon-btn` | 36×36px ❌ |
| `.notifications-back-btn` | 40×40px (borderline) |
| `.zoom-controls .zoom-btn` | 32×32px on mobile ❌ |
| `.action-btn` on mobile | 36×36px ❌ |
| `.menu-btn` on mobile | 36×36px ❌ |
| `.homeview-chevron` inline icon | no hit area |

**Fix strategy:**
Bring all interactive elements to minimum 44×44px tap targets. For icon-only buttons that can't be visually enlarged, use `padding` to extend the hit area while keeping the visual size.

---

### 1.12 — Android Chrome vs. iOS Safari Rendering Differences
**Severity: Major**

**Known divergences found:**

1. **`height: 100vh` on iOS Safari** — iOS Safari's `100vh` includes the browser chrome (address bar), causing the bottom nav area to be hidden behind the Safari UI bar. The app uses `100vh` in `.navview`, `.mapview`, and `#app-root.app-mobile`. **Fix:** Use `height: 100dvh` (dynamic viewport height) with a `100vh` fallback, or use `min-height: -webkit-fill-available` on the body/app root.

2. **`env(safe-area-inset-*)` in `--safe-bottom`** — This is correctly declared in `:root` in `main.css`. The issue is that some elements in `homeview.css`, `settings.css`, `feedback.css`, and `notifications.css` use **hardcoded pixel values** for bottom offsets instead of the CSS variable. These will not adapt to notched iPhones or Android devices with gesture bars.

3. **`-webkit-overflow-scrolling: touch`** — Used in several places (`app.css`, `navigate.css`, `mapview.css`). This is **deprecated** in modern iOS Safari but harmless. The correct replacement is `overscroll-behavior: contain`.

4. **Font scaling** — `html { font-size: 16px; -webkit-text-size-adjust: 100% }` is correctly set. However, `font-size` inside `@media (max-width: 389px)` reduces `--text-base` to `14px`, which on older small Androids may cause additional system font scaling on top of this, resulting in text that is either too small or unexpectedly large.

5. **`appearance: none` on selects** — Used on `.navview-select` and `.feedback-input-field`. This is correct for cross-browser consistency, but iOS Safari still renders a subtle system border — add `-webkit-appearance: none` (already present on navview-select).

---

### 1.13 — Onboarding Highlight Positions Are Viewport-Hardcoded
**Severity: Minor**

**What's wrong:**
```js
const styles = {
  search: { top: '20px', left: '50%', ..., width: '90%', height: '60px' },
  favorites: { bottom: '100px', right: '20px', width: '60px', height: '60px' },
  chatbot: { bottom: '20px', left: '50%', ..., width: '60px', height: '60px' },
  navigate: { bottom: '100px', left: '50%', ..., width: '60px', height: '60px' }
}
```
These are fixed pixel/percentage positions that don't correspond to where the actual UI elements are rendered. On 320px screens or tall phones the pulses will miss their targets. The "chatbot" highlight is at `bottom: 20px` but the chatbot action button on HomeView is at `bottom: ~120px` (inside fixed controls).

**Fix strategy:**
Use `element.getBoundingClientRect()` to dynamically compute highlight positions at runtime using `ref`s on the target elements, or simplify to icon-only highlights within the card (no absolute overlay).

---

## 2. Code Health Issues

### 2.1 — `showRecentSearches` ref is Declared but Never Used
**Severity: Minor**

```js
// HomeView.vue line 406
const showRecentSearches = ref(false)
```
This ref is declared and never read or written anywhere in the template or script. It's dead code.

**Fix strategy:** Remove the declaration.

---

### 2.2 — `isFavorite()` Function is Declared but Never Called in Template
**Severity: Minor**

```js
// HomeView.vue line 582
const isFavorite = (marker) => { ... }
```
The function checks localStorage for favorites but is **never called** from the template. The "Add to Favorites" button in `marker-info-popup` does not use this to show a toggle state (e.g., "Remove from Favorites" if already added) — it only calls `addToFavorites()`.

**Fix strategy:** Either wire `isFavorite` into the marker popup UI to show remove/add state, or remove it if toggling is not a planned feature.

---

### 2.3 — `alert()` Used for User Feedback
**Severity: Major**

Multiple places use `alert()`:
- `HomeView.vue` line 595: `alert('This location is already in your favorites!')`
- `HomeView.vue` line 609: `alert(${marker.name} added to favorites!)`
- `HomeView.vue` line 716: `alert('No locations found...')`

`alert()` is a blocking browser dialog that:
- Freezes the JavaScript thread
- Cannot be styled
- On Android Chrome shows as a modal with the web app origin URL
- Cannot be dismissed with back-swipe on iOS

The app already has a toast pattern in `SettingsView` — it should be unified app-wide.

**Fix strategy:** Replace all `alert()` calls with a shared toast/snackbar component or the existing `showToast` pattern from SettingsView. Add a lightweight global toast composable.

---

### 2.4 — `loadData()` in NavigateView Has an Unnecessary `Promise.all` with 1 Item
**Severity: Minor**

```js
// NavigateView.vue line 420
const [markerRes] = await Promise.all([
  api.get('/core/map-markers/'),
])
```
`Promise.all` with a single item is unnecessary overhead and makes the code harder to read.

**Fix strategy:** Replace with `const markerRes = await api.get('/core/map-markers/')`.

---

### 2.5 — `authStore.isAdmin` is Undefined — Getter Mismatch
**Severity: Critical (Bug)**

In `App.vue` line 63:
```html
<div v-if="authStore.isAdmin" class="app-admin-section">
```
But in `authStore.js`, the getters are: `isSuperAdmin`, `isDean`, `isProgramHead`, `isBasicEdHead` — **there is no `isAdmin` getter**. This means the Admin Panel button in the desktop sidebar will **never render**, even for authenticated admins.

**Fix strategy:** Add an `isAdmin` getter to `authStore`:
```js
isAdmin: (s) => !!s.token && (s.user?.role === 'super_admin' || s.user?.role === 'dean' || ...)
```
Or rename the template reference to use the correct getter (e.g., `authStore.isSuperAdmin`).

---

### 2.6 — `NotificationsView` Uses `db.notifications` — No Error Handling on DB Init
**Severity: Major**

```js
// NotificationsView.vue line 55
notifications.value = await db.notifications.orderBy('created_at').reverse().toArray()
```
If `db` (Dexie/IndexedDB) fails to initialize (e.g., private browsing mode on iOS Safari blocks IndexedDB), this will throw an unhandled rejection. There is no `try/catch` around this call, and the UI will be stuck in a loading state with an empty list and no error message.

**Fix strategy:** Wrap in `try/catch`, fall back to API fetch (`api.get('/notifications/')`), and display an error state if both fail.

---

### 2.7 — `markAllAsRead` in NotificationsView Does Not Persist to API
**Severity: Major**

```js
async function markAllAsRead() {
  for (const notif of notifications.value) {
    if (!notif.is_read) {
      notif.is_read = true
      await db.notifications.update(notif.id, { is_read: true }) // local only
    }
  }
}
```
This only updates the local IndexedDB, **not the backend**. If the user refreshes or the sync runs, the unread state may reset if the sync overwrites local data.

**Fix strategy:** Also call `api.patch('/notifications/${notif.id}/', { is_read: true })` for each — or use a batch endpoint if available.

---

### 2.8 — `SettingsView.vue`: Dark Mode Toggle Has Initialization Race
**Severity: Minor**

```js
// App.vue — initDarkMode() runs on mounted
// SettingsView.vue — also reads localStorage on mounted
```
Both `App.vue` and `SettingsView.vue` independently read and write `localStorage.tp_dark_mode`. They are not synchronized via a shared store. If the user navigates to Settings and the dark mode `keepAlive` restores the component, the `isDarkMode` ref will re-read from `localStorage` on `onMounted` — which is correct. However, if someone toggles dark mode in Settings and then another route triggers `initDarkMode()` via some lifecycle event, the state could briefly conflict.

**Fix strategy:** Move dark mode state into the `authStore` or a dedicated `themeStore` (Pinia). Both App.vue and SettingsView would then read/write from the same reactive source.

---

### 2.9 — Router `meta.requiresAuth` Check is Token-Existence Only
**Severity: Major**

```js
const token = localStorage.getItem('tp_token')
if (!token) { next('/admin/login') }
```
The guard only checks if a token string exists in localStorage — it does not validate it. An expired or invalid token will pass the guard and cause API calls to fail with 401 errors, resulting in a broken admin panel UI with no graceful redirect or error message.

**Fix strategy:** Implement a token validation step (check expiry from JWT decode, or catch 401 on first API call) and redirect to login on failure. Add a `router.beforeEach` that checks the authStore's `isLoggedIn` getter which is synced with the store, not raw localStorage.

---

### 2.10 — `onboarding.css` References `.reduce-animations` Class That Is Never Set
**Severity: Minor**

```css
.reduce-animations .onboarding-card { animation: none; }
.reduce-animations .highlight-pulse { animation: none; }
```
The `.reduce-animations` class is never toggled anywhere in the codebase. The proper implementation would check `prefers-reduced-motion` media query.

**Fix strategy:** Replace with:
```css
@media (prefers-reduced-motion: reduce) {
  .onboarding-card { animation: none; }
  .highlight-pulse { animation: none; }
}
```

---

### 2.11 — `homeview.css` Has Duplicate `.map-container` Rule
**Severity: Minor**

```css
/* Lines 151–159 */
.map-container { width: 100%; height: 100%; display: flex; ... }

/* Lines 263–268 */
.map-container { cursor: grab; }
.map-container:active { cursor: grabbing; }
```
Two separate `.map-container` blocks. Not a bug, but confusing and easy to miss when editing.

**Fix strategy:** Merge into a single rule block.

---

### 2.12 — `homeview.css` Has Duplicate `@keyframes slideUp`
**Severity: Minor**

Both `homeview.css` (line 642) and `main.css` (line 650) define a `@keyframes slideUp` animation. The values differ slightly:
- `main.css`: `from { opacity: 0; transform: translateY(20px) }`
- `homeview.css`: `from { transform: translateY(100%) }` (full-screen slide)

Since both are loaded in the same component, one will override the other depending on import order. Any component using the `.sheet` class from `main.css` alongside a HomeView element using the local `slideUp` will get an unexpected animation.

**Fix strategy:** Rename the HomeView version to `@keyframes slideUpSheet` or similar to avoid collision.

---

### 2.13 — Deprecate and Remove QR Scanner Feature
**Severity: Minor**

**What's wrong:**
The QR Scanner feature (`QRScannerView`) is no longer needed in the system. The codebase still contains its view component, CSS styling, routing, and navigational entry points, which adds unnecessary bloat.

**Fix strategy:**
Remove all traces of the QR Scanner:
1. **Delete Files:** `src/views/QRScannerView.vue` and `src/assets/qrscanner.css`.
2. **Remove Route:** Delete the `/qr-scanner` route from `src/router/index.js`.
3. **Clean App Nav:** Remove `{ path: '/qr-scanner', ... }` from `menuItems` and `'/qr-scanner'` from `hiddenRoutes` in `App.vue`.
4. **Clean HomeView:** Remove the `goToQRScanner` method and its associated `<button class="action-btn">` in `src/views/HomeView.vue`.
5. **Clean Admin Reports:** Remove the "QR Scans" stat element and icon in `src/components/AdminReports.vue`.

---

## 3. UI/UX Issues

### 3.1 — Settings: `min-height: 100vh` Causes Double Scrollbar on Desktop
**Severity: Minor**

```css
.settings-view { min-height: 100%; background: #f5f5f5; padding-bottom: 80px; }
```
And `favorites.css`:
```css
.favorites-view { min-height: 100vh; }
```
On desktop, the parent `.app-main-content` is `overflow-y: auto` with its own scrollbar. If the child has `min-height: 100vh`, the outer container's scroll area extends beyond the viewport, creating a double scroll situation on some desktop browsers.

**Fix strategy:** Replace `min-height: 100vh` on child views with `min-height: 100%`.

---

### 3.2 — Dark Mode Not Applied to Hardcoded Colors in Multiple CSS Files
**Severity: Major**

Many CSS files use hardcoded color values instead of CSS custom properties, breaking dark mode:

| File | Hardcoded Values |
|---|---|
| `homeview.css` | `background: #f5f5f5`, `color: #333`, `background: white`, `color: #666` |
| `settings.css` | `background: white`, color `#333`, `#666`, `#888` etc. |
| `notifications.css` | `background: #fff8f0` (unread card) hardcoded |
| `favorites.css` | `background: white`, `color: #333`, `background: #f5f5f5` |
| `feedback.css` | `background: #f5f5f5` (main content bg) |

When dark mode is enabled, cards and dialogs in Settings, Favorites, Notifications, and Feedback remain bright white with dark text — **these views don't respect dark mode at all**.

**Fix strategy:** Replace all hardcoded color values with CSS custom properties (`var(--color-bg)`, `var(--color-surface)`, `var(--color-text-primary)`, etc.) which are already fully defined for both light and dark themes in `main.css`.

---

### 3.3 — Notifications Top Bar Padding Missing `--safe-top`
**Severity: Major**

```css
.notifications-top-bar { padding: 16px; background: #FF9800; ... }
```
No `padding-top: calc(16px + var(--safe-top, 0px))` is applied, unlike `navview-header` and `mapview-header` which correctly handle this. On iOS devices with notches/Dynamic Island, the notification bar header will collide with the status bar.

**Fix strategy:** Add `padding-top: calc(16px + var(--safe-top, 0px))` to `.notifications-top-bar`. Same issue applies to `feedback-top-bar`.

---

### 3.4 — Feedback Top Bar Icon Button Below Minimum Size
**Severity: Minor**

```css
.feedback-top-bar-icon-btn { width: 36px; height: 36px; }
```
Already listed in touch targets (Issue 1.11). Additionally, the back button's `border-radius: 50%` combined with `width/height: 36px` means on Android the visual circle is noticeably smaller than expected for a primary navigation button.

---

### 3.5 — Onboarding Card `step-1` Gets `margin-top: 80px` on Mobile
**Severity: Minor**

```css
.onboarding-card.step-1 { margin-top: 80px; }
```
On 320px–375px height screens (shorter Androids), 80px top margin inside a flex-centered overlay with `padding: 20px` could push the card's bottom below the screen bottom edge, making the "Next" button unreachable without scrolling.

**Fix strategy:** Remove the margin-top adjustment or make it `max(20px, 5vh)` to cap it on small screens.

---

### 3.6 — `SettingsView` "Back to Home" Router Behavior Not Standard
**Severity: Minor**

The feedback success screen's "Back to Home" button calls `router.push('/')` rather than `router.back()`. If the user navigated as: Home → FeedbackView, pressing "Back to Home" pushes a new `/` entry onto the history stack rather than going back. On Android, pressing the hardware back button will then return to the feedback thank-you screen.

**Fix strategy:** Use `router.replace('/')` which replaces the current history entry, or `router.go(-1)` to go back naturally.

---

## 4. Prioritized Implementation Order

| Priority | Area | Issue # | Severity |
|---|---|---|---|
| 1 | Mobile | 1.1 — Search bar overlaps bottom nav on iOS | Critical |
| 2 | Mobile | 1.2 — Dropdown top offset wrong (no safe-top) | Critical |
| 3 | Mobile | 1.9 — `user-scalable=no` accessibility flaw | Critical |
| 4 | Code Health | 2.5 — `authStore.isAdmin` undefined (admin nav broken) | Critical |
| 5 | Mobile | 1.3 — Search suggestions fixed bottom overlap | Critical |
| 6 | Code Health | 3.3 — Missing `--safe-top` on Notifications/Feedback bars | Major |
| 7 | Mobile | 1.4 — NavigateView 800px hardcoded map width | Major |
| 8 | Mobile | 1.5 — MapView 800px hardcoded width | Major |
| 9 | Mobile | 1.8 — NotificationsView missing flex layout | Major |
| 10 | Mobile | 1.10 — Marker popup overlaps bottom controls | Major |
| 11 | Mobile | 1.11 — Touch targets below 44×44px | Major |
| 12 | Mobile | 1.12 — `100vh` iOS Safari viewport bug | Major |
| 13 | Code Health | 2.3 — `alert()` blocking dialogs | Major |
| 14 | Code Health | 2.6 — NotificationsView no error handling on DB | Major |
| 15 | Code Health | 2.7 — markAllAsRead doesn't persist to API | Major |
| 16 | Code Health | 2.9 — Router auth guard token-only check | Major |
| 17 | UI/UX | 3.2 — Dark mode broken in Settings/Favorites/Feedback/Notifications | Major |
| 18 | Mobile | 1.6 — No debounce on window resize | Major |
| 19 | Mobile | 1.7 — Only 3 mobile nav items (discoverability) | Major |
| 20 | Code Health | 2.8 — Dark mode state not in shared store | Minor |
| 21 | Code Health | 2.1 — Dead `showRecentSearches` ref | Minor |
| 22 | Code Health | 2.2 — Unused `isFavorite()` function | Minor |
| 23 | Code Health | 2.4 — Redundant `Promise.all` with 1 element | Minor |
| 24 | Code Health | 2.10 — `.reduce-animations` class never set | Minor |
| 25 | Code Health | 2.11 — Duplicate `.map-container` CSS rules | Minor |
| 26 | Code Health | 2.12 — Duplicate `@keyframes slideUp` names | Minor |
| 27 | UI/UX | 3.1 — `min-height: 100vh` double scrollbar (desktop) | Minor |
| 28 | UI/UX | 3.5 — Onboarding step-1 margin-top on short screens | Minor |
| 29 | UI/UX | 3.6 — Feedback back button pushes history | Minor |
| 30 | Mobile | 1.13 — Onboarding highlights hardcoded positions | Minor |
| 31 | Code Health | 2.13 — Deprecate and remove QR scanner feature | Minor |

---

## 5. Recommended Implementation Phases

### Phase 1 — Critical Fixes (Mobile-Breaking)
Issues: 1.1, 1.2, 1.3, 1.9, 2.5, 3.3

These block correct rendering on the majority of target devices (iPhone + Android). Fix before any other work.

### Phase 2 — Major Mobile Polish
Issues: 1.4, 1.5, 1.8, 1.10, 1.11, 1.12, 1.6, 1.7

Map rendering, touch targets, layout correctness across the 320–430px range.

### Phase 3 — Dark Mode & Code Health
Issues: 3.2, 2.3, 2.6, 2.7, 2.8, 2.9

Dark mode completeness, API consistency, error handling.

### Phase 4 — Cleanup & Polish
Issues: 2.1, 2.2, 2.4, 2.10–2.13, 3.1, 3.5, 3.6, 1.13

Dead code removal, minor CSS deduplication, UX edge cases, and removing deprecated features (QR Scanner).
