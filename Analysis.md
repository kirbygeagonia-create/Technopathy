TechnoPath SEAIT — Deep Codebase Audit
9
Critical bugs
18
Major issues
21
Code quality
12
Design issues
🔴 Critical — Core Features Broken
🔴
Pathfinding permanently broken — field name triple mismatch
Backend serializes edges as from_node / to_node; pathfinder.js reads from_node_id / to_node_id. Node coordinates are x/y in model but pathfinder reads x_position/y_position. Dijkstra gets undefined for every value — navigation is completely non-functional.
pathfinder.js / serializers.py
🔴
AdminNavGraph saves x/y as integers (0–20) but backend expects normalized floats (0.0–1.0)
AdminNavGraph.vue uses mock nodes with integer coordinates (x: 10, y: 0). The backend model stores them as FloatField (normalized 0–1). Any nodes created through the admin UI will have wildly incorrect positions on the map — they'll cluster at one corner.
AdminNavGraph.vue / NavigationNode model
🔴
QR scanner sends wrong query param — navigation never receives destination
QRScannerView routes with query: { destination: location }. NavigateView only listens for route.query.to and route.query.from. The destination param is silently ignored — QR scanning leads to a blank Navigate page.
QRScannerView.vue / NavigateView.vue
🔴
Feedback submission sends fields the backend model doesn't have
FeedbackView posts is_anonymous and location fields. The Feedback model has neither. These fields are silently dropped by DRF. Anonymous/location data is lost forever. Also: FeedbackView category values use title case ("Map Accuracy") but the model's CATEGORIES choices use snake_case ("map_accuracy") — all category values will fail validation.
FeedbackView.vue / feedback/models.py
🔴
InfoView calls /api/users/ for instructors/employees — unauthenticated public users get 403
The InfoView switches to /users/ endpoint for instructor and employee types. This endpoint requires admin authentication. Public users will always see a 403 error and fall back to fake hardcoded data. The route exists in the nav, the endpoint does not serve public data.
InfoView.vue / users endpoint
🔴
PWA icons missing from build directory — app will not install
Both vite.config.js and public/manifest.json reference /icons/icon-192.png. The frontend/public/ directory has no icons/ folder. The icon files (uppercase Icon-192.png) are in web/icons/ outside Vite's scope. PWA install prompt will fail on all devices.
vite.config.js / public/
🔴
Navigate locations list is hardcoded — never loads from database
locations in NavigateView is a static array of 18 names. loadData() fetches map markers for the visual display but never updates the dropdown. Adding/removing buildings in the admin panel has zero effect on navigation.
NavigateView.vue
🔴
super_admin role label says "Safety and Security Office" — wrong display name
In users/models.py, the super_admin role choice label is "Safety and Security Office" — the same as the safety_security department. The system administrator role shows the wrong title in audit logs, the admin panel, and all announcement attributions.
users/models.py ROLE_CHOICES
🔴
Favorites ID collision — MapView and HomeView use different ID schemes
MapView saves favorites with id: Date.now() (timestamp). HomeView saves with id: marker.id (database ID, typically 1–20). These can collide silently. Deleting a favorite by ID will delete the wrong one when both sources have written to localStorage.
MapView.vue / HomeView.vue
🟠 Major — Broken Functionality / Security
🟠
CORS open to all origins in Flask chatbot
CORS(app) with no configuration allows any origin to call the chatbot API. In production this means any website can send requests to the chatbot as if it were your app.
chatbot_flask/app.py
🟠
OpenAI API key exposed in client-side JavaScript bundle
VITE_OPENAI_API_KEY is bundled into the frontend JS and visible to anyone. API keys must only exist server-side. The Flask chatbot is already the correct place for AI calls.
aiChatbot.js
🟠
JWT tokens stored in localStorage — XSS accessible
Admin tokens (access + refresh) are stored in localStorage. Any XSS attack can steal them. HttpOnly cookies are the correct approach for admin authentication tokens.
api.js / authStore.js
🟠
AdminFeedback ignores canViewDeptFeedback — Deans locked out
AdminView shows the Feedback nav button to users with canViewDeptFeedback, but the panel itself only renders for canViewAllFeedback. Dean-level users see the button, click it, and get the "permission denied" screen.
AdminView.vue / AdminFeedback.vue
🟠
notifications: frontend mutates read status locally but backend tracks it separately
NotificationsView does notif.is_read = true and db.notifications.update() locally. But the backend uses a separate NotificationReadStatus table. If a user logs in on another device, all notifications show as unread again.
NotificationsView.vue / notifications serializer
🟠
HomeView polls notification count every 5 seconds — too aggressive
A full API call to /notifications/ every 5 seconds on every user device creates unnecessary server load. Existing 30s polling in sync.js already handles notification updates. This duplicates and overwhelms it.
HomeView.vue
🟠
authStore.logout() doesn't redirect — admin panel stays visible
After logout, tokens are cleared but there is no router.push(). The admin shell stays rendered until the user manually navigates away. Any subsequent API calls will return 401.
authStore.js
🟠
ProfileView computes isLoggedIn from localStorage directly, ignoring authStore
const isLoggedIn = computed(() => !!localStorage.getItem('tp_token')) — this bypasses the Pinia store entirely. If a token is invalidated or expires, the logout button won't appear until a page reload.
ProfileView.vue
🟠
Flask chatbot maintains its own separate SQLite database — data duplication
The Flask app has its own chatbot.db with a chat_history table, completely separate from Django's database. Chat history lives in two disconnected places. The Django aiChatbot service also saves logs to IndexedDB. Three separate chat history stores.
chatbot_flask/app.py
🟠
NavigationNode model missing is_active field — wrong IndexedDB schema
db.js indexes navigation_nodes on is_active but the Django model only has is_deleted. Queries filtering by is_active return incorrect results.
db.js / navigation/models.py
🟠
MapView floor count hardcoded — ignores total_floors from database
The floors computed uses a hardcoded JS object keyed by building name. The Facility model has total_floors. New buildings or floor changes require a code deploy.
MapView.vue
🟠
goToInstructorInfo / goToEmployees called in HomeView but buttons never shown in menu
Two functions are defined and would navigate to /instructor-info and /employees, but the slide-up menu only shows Building Info and Rooms Info. Dead functions, incomplete feature.
HomeView.vue
🟠
geolocation.js built but never used — "You Are Here" feature is missing
A complete GPS service with watchLocation() and gpsToMapCoords() exists but is never imported in MapView or NavigateView. The most essential feature for a campus navigation app is absent.
geolocation.js
🟠
PWA Workbox caches localhost:8000 only — offline API cache breaks in production
urlPattern: /^http:\/\/localhost:8000\/api\// is hardcoded. In production, API calls go to a different host, so Workbox never caches them and offline mode won't have API data backed by the service worker.
vite.config.js
🟠
81MB of Node.js installers committed to the repository
node-installer.msi (26MB), nodejs.msi (26MB), node-portable.zip (29MB) are tracked in git. This bloats every clone and CI pipeline. They should be deleted and added to .gitignore.
repo root
🟠
Acounts.txt (credential file) committed to repository
A file named Acounts.txt (typo) in the repo root appears to contain account information. Credentials must never be committed to version control — they should be rotated immediately and removed from git history.
Acounts.txt
🟠
lucide-vue-next installed as a dependency but never imported anywhere
package.json includes lucide-vue-next@^1.0.0. Not a single .vue or .js file imports from it. Dead dependency adds to bundle size.
package.json
🟠
Two duplicate AdminDashboard components — dead code
/components/AdminDashboard.vue (12KB) is the old version. /components/admin/AdminDashboard.vue (20KB) is the current one used by AdminView. The root-level file is orphaned.
components/
🟠
AdminReports.vue and AdminSettings.vue are completely unused
Both files exist in /components/ but are never imported anywhere in the application. 30KB+ of dead code.
components/
🔵 Code Quality — Logic, Organization, Duplication
🔵
Pan/zoom code copy-pasted identically across 3 views
HomeView, MapView, and NavigateView all contain identical pan/zoom logic (onPointerDown, onPointerMove, onTouchStart, onTouchMove, zoomIn, zoomOut, scale, tx, ty). Should be extracted to a useMapPanZoom() composable.
HomeView / MapView / NavigateView
🔵
SettingsView has its own local toast system — ignores the global AppToast
SettingsView defines a private toastMessage ref and custom showToast function. AppToast and toast.js already provide this globally. Inconsistent behavior — settings toasts look different from all other toasts.
SettingsView.vue
🔵
showSmartAlert() is functionally identical for mobile and desktop
The if/else branches differ only by 1 second toast duration. The "smart" conditional adds no real value.
toast.js
🔵
Mock fallback data is not gated to development mode
HomeView, MapView, and NavigateView all fall back to hardcoded mock data when API calls fail. In production, this silently hides real errors. All mock data should be wrapped in if (import.meta.env.DEV).
HomeView / MapView / NavigateView
🔵
syncStore.isSyncing never reflects the startup sync
main.js calls syncAllData() directly, bypassing syncStore.sync(). The syncing banner never shows during the initial app load — only during polling-triggered syncs.
main.js / syncStore.js
🔵
Dijkstra uses array.sort() instead of a min-heap priority queue
queue.sort((a, b) => a.dist - b.dist) runs on every loop iteration — O(n² log n) overall. A min-heap makes this O(n log n). For a large campus graph this matters.
pathfinder.js
🔵
HomeView has two identical search bars sharing one v-model
The desktop search bar and the mobile bottom search bar are separate DOM elements with the same v-model="searchText". One should be a component, or CSS alone should show/hide the single instance.
HomeView.vue
🔵
FeedbackView locations list is hardcoded — same problem as NavigateView
The optional location selector in FeedbackView uses the same 18 hardcoded location names as NavigateView. This list should come from the API.
FeedbackView.vue
🔵
Many unused IndexedDB tables defined in db.js
app_usage, connectivity_log, usage_analytics, device_preferences, feedback_flags, search_history, ratings — all defined in the schema but never read from or written to in frontend code.
db.js
🔵
FavoritesView uses browser confirm() dialog — terrible mobile UX
if (confirm('Remove this location from favorites?')) — native confirm dialogs are non-stylable, block the UI thread, and are disabled in some mobile WebViews. A custom inline confirmation is needed.
FavoritesView.vue
🔵
onOnboardingComplete / onOnboardingSkip are just console.log calls
Both callbacks do nothing useful — they only print to console. Onboarding completion state should be saved so the tutorial doesn't reappear.
HomeView.vue
🔵
ProfileView preferences (language, font scale, high contrast) have no backend sync
All marked with // TODO: Sync with backend if logged in. These are localhost-only preferences. Switching devices resets everything.
ProfileView.vue
🔵
AdminLoginView has debug console.log statements in production code
console.log('Login started...'), console.log('Login result:', result) — these leak information and should be removed before deployment.
AdminLoginView.vue
🔵
db.js version is v3 but has no migration from v1/v2 — existing users may get schema errors
Dexie schema versions without upgrade() callbacks can break on devices that have older IndexedDB versions cached. Upgrading requires explicit migration steps.
db.js
🔵
Flask chatbot knowledge base conflicts with Django/aiChatbot knowledge base
The Flask app has its own CAMPUS_KNOWLEDGE and CLASSROOM_BUILDINGS dictionaries that may differ from the CAMPUS_CONTEXT string in aiChatbot.js. Two sources of truth for the same campus information will give inconsistent answers.
chatbot_flask/app.py / aiChatbot.js
🔵
Splash screen comment references Flutter ("matching Flutter's 3s") — wrong framework
This is a Vue PWA. The comment is a stale copy from a Flutter codebase and is confusing to any developer reading the code.
SplashScreen.vue
⬜ Design & UX — Inconsistencies
⬜
23 hardcoded hex colors in view templates bypassing the CSS design system
Inline style="background: #E3F2FD; color: #2196F3" and similar appear 23 times in views. Dark mode will not apply to these elements — they'll show light-mode colors permanently.
ProfileView, HomeView, SettingsView
⬜
homeview.css is 1,353 lines — largest file by far, needs splitting
HomeView's CSS file is more than double the next largest (mapview.css at 581 lines). The home view handles too many responsibilities (map, search, dropdowns, dialogs, mobile/desktop layout) and should be decomposed.
homeview.css
⬜
ChatbotView mixes inline styles with external CSS file
ChatbotView.vue imports chatbot.css but also has a large <style> block with 60+ lines of component-specific styles. Styles are split across two locations.
ChatbotView.vue
⬜
NotificationsView mixes inline styles with external CSS file
Source-chip and chip-color styles are defined in an inline <style> block even though the view uses an external notifications.css. Same inconsistency as ChatbotView.
NotificationsView.vue
⬜
43 instances of hardcoded border-radius px values in homeview.css
Scattered uses of raw pixel values like border-radius: 12px, border-radius: 8px, border-radius: 50% ignore the design tokens (--radius-md, --radius-lg, --radius-full) defined in main.css.
homeview.css
⬜
AdminNavGraph has no visual canvas — cannot position nodes on the actual map
The navigation graph editor is a plain table with x/y text inputs. Admins have no way to visually place nodes on the SVG map. This makes the navigation graph essentially unmanageable in practice.
AdminNavGraph.vue
⬜
MapView legend is always visible by default — takes up map space
showLegend = ref(true) means the legend overlays the map on every load. On mobile, this blocks significant map area immediately. It should default to collapsed.
MapView.vue
⬜
SplashScreen uses fixed 2.5s timer regardless of data load state
The splash shows for exactly 2.5 seconds even if data loads in 0.3s or takes 5s on a slow connection. It should dismiss when syncAllData() resolves, with a minimum display time of ~1s for branding.
SplashScreen.vue
⬜
Bottom nav hides Notifications and Feedback — users can't find them
The mobile bottom nav shows only Home, Navigate, Chatbot, Settings. Notifications and Feedback are hidden routes. There is no badge count visible anywhere on mobile without already knowing where to look.
App.vue
⬜
"Check for Updates" button does nothing
The button calls showToast('You are using the latest version.') unconditionally. It doesn't check the PWA cache, service worker, or any version endpoint. Misleading to users.
SettingsView.vue
⬜
Profile page allows editing name/phone but these fields don't exist in the backend
Edits are saved to localStorage only. The backend AdminUser model has no phone field for public users. Profile data will be lost on browser storage clear. A proper user profile model for public/guest users is missing.
ProfileView.vue
⬜
Language switching UI exists but has no effect — app is English only
ProfileView lets users select English, Filipino, or Cebuano. No i18n library is installed and no translations exist. This is a placeholder with no implementation.
ProfileView.vue

Here's the complete second-pass audit. Here's a summary of what was uncovered beyond the first analysis:
New Critical Bugs Found:

AdminNavGraph saves coordinates as raw integers (0–20) but the backend expects normalized floats (0.0–1.0) — every node created through the UI will be misplaced on the map
QR Scanner sends ?destination= but NavigateView only reads ?to= — scanning a QR code never pre-fills the destination
FeedbackView posts is_anonymous and location fields that don't exist in the backend model, and uses "Map Accuracy" (title case) while the DB expects "map_accuracy" (snake_case) — all feedback category saves fail silently
InfoView calls the /api/users/ admin endpoint for instructors/employees — public users always get 403
Favorites saved with Date.now() from MapView and real database IDs from HomeView — both write to the same localStorage key and IDs collide

New Major Issues:

Flask CORS open to all origins
Dean-level users see Feedback in the nav but hit an access-denied screen — RBAC gap
Notifications read state is tracked locally but the backend tracks it separately per-user in a different table — read state doesn't sync across devices
The super_admin role label says "Safety and Security Office" instead of something like "System Administrator"
Flask chatbot maintains its own SQLite database completely separate from Django — three disconnected chat history stores (Flask SQLite + Django DB + IndexedDB)

New Code Quality / Design Issues:

1,353-line homeview.css — needs decomposing
23 hardcoded hex colors in templates bypass dark mode
Pan/zoom logic copy-pasted identically in 3 different views — needs a shared composable
AdminNavGraph has no visual canvas for placing nodes — completely unmanageable in practice
Language switcher UI exists but has zero implementation
"Check for Updates" always says you're up to date