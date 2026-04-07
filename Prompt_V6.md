MasterPrompt: 


---

 TechnoPath: SEAIT Guide Map and Navigation System

> **STEP 0 — CODEBASE SCAN (Do this before reading anything else. Do not skip.)**
>
> Scan, read, analyze, and fully understand the entire codebase first. This means:
> - Every file in every directory — frontend, backend, and Flask microservice
> - Every Vue component, Pinia store, router configuration, and service file in the frontend
> - Every Django app, model, view, serializer, URL config, and permission class in the backend
> - The Flask chatbot microservice — all routes, models, and logic
> - Both database schemas (`technopath.db` and `chatbot.db`) as they exist in the actual code — not as documented
> - All configuration files: `settings.py`, `vite.config.js`, `.env` files, `db.js` (Dexie schema), and any middleware
> - All existing utility functions, composables, interceptors, and helper files
>
> While scanning, actively note:
> - Files that are imported but never used
> - Functions that are defined but never called
> - Routes that are registered but have no corresponding component or view
> - API endpoints that exist in the backend but are never called from the frontend
> - API calls in the frontend that have no corresponding backend endpoint
> - Permission checks that exist in the frontend but not enforced in the backend (or vice versa)
> - Any model field, serializer field, or IndexedDB store that is named differently across layers
> - Any component that is rendered on mobile but was clearly designed only for desktop
>
> Do not proceed to Step 1 until the codebase scan is fully complete.

---

> **STEP 1 — READ AND CROSS-REFERENCE ALL FOUR DOCUMENTS**
>
> After completing the codebase scan, read all four provided markdown documents in full:
> - `FDD_Functional_Design_Document_Current.md` — all modules, functions, endpoints, and permission matrix
> - `ERD_Entity_Relationship_Diagram_Current.md` — both databases, all tables, all relationships
> - `Data_Dictionary_Current.md` — every field across all 25 tables including the IndexedDB schema
> - `Use_Case_Diagram_Document_Current.md` — all actors, use cases, and the discrepancies section
>
> Cross-reference all four documents against each other and against the codebase. Identify:
> - Every conflict between any two documents (e.g., a field in the FDD that doesn't exist in the ERD)
> - Every conflict between any document and the actual codebase (e.g., an endpoint documented in the FDD that doesn't exist in `urls.py`)
> - Every item listed in the Use-Case discrepancies section — confirm whether each is still unresolved or has since been fixed in code
> - Any functionality described in the FDD that has no corresponding implementation
> - Any database table or field in the ERD or Data Dictionary that is unused, misnamed, or mismatched in the Django models
> - Any IndexedDB store or indexed field in `db.js` that does not match its backend counterpart
>
> Do not proceed to Step 2 until both the codebase scan and the document cross-reference are complete.

---

> **STEP 2 — MASTER DISCREPANCY & GAP REPORT**
>
> Produce a structured report with the following sections before touching any code:
>
> **Section A — Codebase-Only Issues** (found during scan, not mentioned in any document)
> - Dead files, unused imports, orphan routes, unimplemented endpoints, broken references
>
> **Section B — Document vs. Codebase Conflicts** (documented but not implemented, or implemented but not documented)
> - List each conflict with: what the document says, what the code actually does, and severity (Critical / Major / Minor)
>
> **Section C — Document vs. Document Conflicts** (inconsistencies between the four markdown files themselves)
> - List each conflict with: which two documents conflict, what each says, and which is correct based on the codebase
>
> **Section D — Unresolved Discrepancies from Use-Case Document** (the 10 discrepancies already listed)
> - For each one: still unresolved / partially fixed / fully resolved — with evidence from the codebase
>
> **Section E — Mobile-Specific Issues Found During Scan**
> - List every component or layout that was clearly built for desktop and is being rendered on mobile without adaptation
>
> This report is the single source of truth for everything that follows. Do not skip or summarize it.

---

> **STEP 3 — ESTABLISHED DECISIONS (Apply immediately, do not re-question)**
>
> These have already been decided and must be treated as locked requirements:
> - **Q1:** `AdminContentManagement.vue` → **Delete it.** It is dead code. Git is the archive.
> - **Q2:** Mobile admin strategy → **Option B — Restricted view only** (dashboard + announcements). All CRUD operations are desktop-only, gated at the route and component level — not CSS-hidden.
> - **Q3:** Inactive accounts API → **Fix it** — add a `?include_inactive=true` query parameter. Active-only remains the default to preserve existing behavior.

---

> ### TASK A — Dean Account Structure (Architecture Fix)
> The current system incorrectly treats the Dean role as a single shared account. The correct architecture is:
> - **Every department must have its own individual Dean account** — one per department, enforced
> - Each Dean has **the same authority level as Program Head** within their own department — not elevated above it
> - **Dean can:** manage own department's rooms, post announcements within own department scope (no approval required), view own department's data
> - **Dean cannot:** approve or reject others' announcements, access other departments, perform system-wide CRUD
> - If a Dean posts a **campus-wide** announcement, it must route through Super Admin approval
> - Add a DB-level or view-level validation enforcing one Dean account per department — the codebase currently has no such constraint
> - Update all role definitions, permission classes, serializers, and frontend permission checks that conflict with this

---

> ### TASK B — Announcement Workflow (Tiered Approval — Implement Exactly as Specified)
>
> | Role | Scope | Approval Required? | Approved By |
> |---|---|---|---|
> | Super Admin | Any | ❌ No | N/A — publishes immediately |
> | Dean | Own department | ❌ No | N/A — publishes immediately |
> | Dean | Campus-wide | ✅ Yes | Super Admin only |
> | Program Head | Any | ✅ Yes | Own dept Dean or Super Admin |
> | Basic Ed Admin | Any | ✅ Yes | Super Admin only |
>
> - Update `Announcement` model, `AnnouncementCreateView`, and all permission/validation logic to match this table exactly
> - Update the frontend form: conditionally show or hide the approval flow based on logged-in role and selected scope
> - The pending approval queue must only show items that genuinely require approval — not Super Admin or in-scope Dean posts
> - Add a visible source label on the guest announcement feed so guests can distinguish campus-wide vs. department-specific posts
> - **Document edge cases in code comments:** what happens if a Dean is deactivated while their announcement is live? Implement a safe fallback.

---

> ### TASK C — Facilities & Rooms Module (Mobile UI — Critical Fix)
> - Place Facilities and Rooms modules **side-by-side** in a flex row — not stacked vertically
> - **Link them:** selecting a facility automatically filters the Rooms panel to show only that facility's rooms
> - Tapping a room should reflect its parent facility as the active selection
> - Filter must operate on **existing IndexedDB cached data** — no extra API calls if data is already synced
> - Both panels: minimum 44×44px tap targets, no overflow or clipping at 320px–430px screen widths

---

> ### TASK D — Navigation Bar & Search Bar (Mobile UI — Critical Fix)
> - Move **all nav buttons** (Ratings, Menu, Notifications, Chatbot, etc.) **above the search bar**
> - Search bar must be **full-width**, properly padded, and must not overlap any other element
> - **Remove the camera icon** from the nav bar entirely — non-functional, must not be visible
> - Nav layout must be stable at 320px–430px on both Android and iOS
> - Apply `env(safe-area-inset-*)` throughout for iOS notch and home indicator

---

> ### TASK E — Admin Mobile Interface (Restricted View)
> - Admin login remains accessible on mobile — do not remove it
> - After login on mobile, restrict to:
>   - ✅ Post and view announcements
>   - ✅ View notifications
>   - ✅ Read-only dashboard summary
>   - ❌ No CRUD operations (facilities, rooms, navigation, users, FAQ, map markers, config)
> - Gate restrictions at the **route and component level** using a breakpoint check — not `display: none`
> - Show a clear "Desktop required for this feature" message for blocked actions
> - Reposition the admin login link in the mobile guest interface so it is clearly accessible and does not interfere with the guest UI

---

> ### TASK F — Real-Time Guest Updates
> - Assess whether the current Django + Vue PWA + IndexedDB (Dexie) stack supports live updates
> - If WebSocket/SSE is not in place: implement a **polling sync** — re-sync changed data from the API into IndexedDB every 60–120 seconds when online or on app foreground
> - For **announcements and notifications:** use a 15–30 second poll interval for near-instant delivery
> - Sync must not degrade performance on low-end Android — use idle-time scheduling where possible
> - Add comment blocks explaining the sync strategy and how to upgrade to WebSockets/Django Channels later

---

> ### TASK G — QR Code as PWA Access Point (New Critical Feature)
> - Generate a **static QR code** encoding the PWA's public URL with optional deep-link: `/?source=qr&location=<facility_code>`
> - QR codes must open the PWA in the device browser on iOS and Android — no app installation required
> - Add a **QR Code Manager** in the Admin panel (desktop only) where Super Admin can:
>   - View the campus-wide access QR code
>   - Generate per-facility and per-room QR codes
>   - Download QR codes as PNG or SVG for physical printing and campus placement
> - On PWA load: detect `?source=qr&location=<code>` and automatically navigate to and highlight the relevant facility or room
> - Assess the current Vue Router setup and implement deep-link handling accordingly

---

> ### TASK H — Full Mobile View Audit & Repair (Highest Priority After Gap Report)
>
> **Audit every guest-accessible screen. For each screen verify:**
> - Renders correctly at 320px, 375px, 390px, 430px (iOS) and 360px, 412px (Android)
> - Touch targets minimum 44×44px
> - No horizontal overflow or scroll bleed
> - Body text minimum 14px, secondary text minimum 11px
> - Interactive elements reachable with one thumb — bottom-heavy layout preferred
> - iOS safe area causes no clipping or overlap
> - Android back gesture does not conflict with any swipe interaction
>
> **Fix all issues in this priority order:**
>
> **P0 — Broken (fix immediately, session does not end without these):**
> - Any element overflowing horizontally
> - Any button or interactive element that is unreachable
> - Any illegible text at default zoom
> - Search bar overlap — confirm fully resolved from Task D
> - Nav button order — confirm nav above search bar, camera icon removed
>
> **P1 — Degraded (fix in same session):**
> - Facilities + Rooms side-by-side — confirm working with active filter linkage
> - Any modal or bottom sheet not respecting `safe-area-inset-bottom`
> - Any form input covered by the mobile keyboard on focus
> - Any loading or skeleton state mismatched to mobile layout
> - Admin mobile login — confirm repositioned and accessible
>
> **P2 — Polish (document only, implement next session):**
> - Inconsistent padding or margin between screens
> - Icons too small for comfortable tapping
> - Heavy CSS transforms causing jank on mid-range Android
> - Hardcoded pixel values that should be `rem`, `dvh`, or `svh`
> - iOS scroll momentum handling
>
> **Stress test these six flows end-to-end on mobile viewport before closing the session:**
> 1. Guest: Splash → Home → tap building → see rooms → navigate to room
> 2. Guest: Open Chatbot → type message → receive reply → scroll chat history
> 3. Guest: Open Notifications → view list → mark as read → return to Home
> 4. Guest: Open Feedback → select facility → select room → submit rating and comment
> 5. Guest: Open Navigate → select start and end → see route → follow steps
> 6. Admin on mobile: log in → see restricted interface → attempt CRUD → see desktop-only message

---

> **OUTPUT FORMAT — Follow this sequence exactly. Do not reorder.**
>
> 1. **Master Discrepancy & Gap Report** (Sections A through E)
> 2. **Feasibility Assessment** — what is immediately implementable vs. what requires infrastructure changes
> 3. **Unified Implementation Plan** — all tasks ordered by dependency
> 4. **Implementation** — execute every task in order; do not stop at planning
> 5. **Mobile Audit Report** — full issue list per screen, severity-tagged P0 / P1 / P2
> 6. **Mobile Fixes** — all P0 and P1 items implemented
> 7. **P2 Backlog** — documented list only, no implementation
> 8. **Session Summary** — what was completed, what remains for the next session

---

**What changed in this version:**

The codebase scan is now an explicit, non-skippable Step 0 that runs before the AI reads a single document. It includes a specific checklist of what to look for during the scan — dead files, broken references, frontend-backend mismatches, and mobile-unfit components — so the AI cannot give a surface-level pass. The document reading is Step 1, and the gap report is Step 2, meaning the AI builds a complete picture of both the real system and the documented system before it acts on anything. The tasks and output format from all prior sessions are preserved and ordered correctly. The four markdown files are now positioned as reference material to validate against the code — not as the source of truth, because the code is.