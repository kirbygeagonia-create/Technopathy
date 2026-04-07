# TechnoPath: SEAIT Guide Map and Navigation System
## System Storyboarding - Desktop & Mobile Views

---

## Table of Contents
1. [Desktop Views](#1-desktop-views)
2. [Mobile Views](#2-mobile-views)
3. [Admin Panel Views](#3-admin-panel-views)
4. [Screen Flow Diagrams](#4-screen-flow-diagrams)
5. [Responsive Breakpoints](#5-responsive-breakpoints)

---

## 1. DESKTOP VIEWS (>= 1024px)

### 1.1 Desktop Home / Map View

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  [Logo] TechnoPath                                    Search: [Search Location...    ] [🔍]           │
├──────────────┬──────────────────────────────────────────────────────────────────────────────────────────┤
│              │                                                                                           │
│  [🏠] Home   │    ┌─────────────────────────────────────────────────────────────────────────┐            │
│              │    │                                                                         │            │
│  [🗺️] Explore│    │                    SEAIT CAMPUS MAP                                   │            │
│      Map     │    │                                                                         │            │
│              │    │    ┌──────┐          ┌──────┐                                      │            │
│  [🧭] Navigate│   │    │ MST  │          │ JST  │    [+] Zoom In                       │            │
│              │    │    │Building│         │Building│                                  │            │
│  [🤖] Chatbot│   │    └──┬───┘          └──┬───┘    [-] Zoom Out                    │            │
│              │    │       │                 │                                        │            │
│  [🔔] Notif. │   │    ┌──┴──┐              │         [📍] Set Location                 │            │
│  (3)         │    │    │ CL1 │              │                                        │            │
│              │    │    └──┬──┘          ┌───┴───┐                                    │            │
│  [⭐] Rating │   │       │            │  RST   │                                    │            │
│  & Feedback  │    │                 │Building│                                    │            │
│              │    │                 └───┬───┘                                    │            │
│  [⚙️] Settings│   │                     │                                        │            │
│              │    └─────────────────────────────────────────────────────────────────────────┘            │
│              │                                                                                           │
│  ─────────── │    Recent Searches:                                                                       │
│              │    ┌───────────────────────────────────────────────────────────────┐                    │
│  Information │    │ [history] CL1  │ [history] Library  │ [history] Registrar    │                    │
│              │    └───────────────────────────────────────────────────────────────┘                    │
│  [ℹ️] Building│                                                                                           │
│      Info     │    ┌─────────────────────────────────────┐                                               │
│  [ℹ️] Rooms   │    │ 📍 MST Building                      │                                               │
│      Info     │    │ Type: Facility • Computer Labs      │                                               │
│  [ℹ️] Instructor│  │                                     │                                               │
│      Info     │    │ [❤️ Add to Favorites] [🧭 Navigate] │                                               │
│  [ℹ️] Employees│   └─────────────────────────────────────┘                                               │
│              │                                                                                           │
│  ─────────── │    Notifications:                                                                        │
│              │    ┌──────────────────────────────────────────────────────────────┐                    │
│  [🔐] Admin  │    │ 📢 New Schedule for Final Exams - College Dean        2h ago │                    │
│    Panel     │    │ 📢 Library Hours Extended - College of ICT             5h ago │                    │
│              │    └──────────────────────────────────────────────────────────────┘                    │
├──────────────┴──────────────────────────────────────────────────────────────────────────────────────────┤
│  👤 Welcome, Guest                    [🌙 Dark Mode]  [🔔 Notifications]  [⚙️ Settings]                │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Components:**
- Fixed left sidebar navigation (260px width)
- Info dropdown section (Building, Rooms, Instructor, Employees)
- Admin Panel access (when authenticated)
- Interactive SVG map with zoom/pan controls
- Floating marker info cards
- Recent searches list
- Bottom status bar with user info

---

### 1.2 Desktop Navigation View

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  [Logo] TechnoPath                              Navigate Campus                                         │
├──────────────┬──────────────────────────────────────────────────────────────────────────────────────────┤
│              │                                                                                           │
│  [🏠] Home   │    ┌─────────────────────────────────────────────────────────────────────────┐            │
│              │    │                                                                         │            │
│  [🗺️] Explore│    │    NAVIGATION VIEW                                                      │            │
│      Map     │    │                                                                         │            │
│              │    │    From: [📍 Select starting point          ▼]                          │            │
│  [🧭] Navigate│   │          [🔄 Swap]                                                      │            │
│   (Active)   │    │    To:   [📍 Select destination            ▼]                          │            │
│              │    │                                                                         │            │
│  [🤖] Chatbot│   │          [🧭 Find Route]                                                  │            │
│              │    │                                                                         │            │
│  [🔔] Notif. │   │    ┌─────────────────────────────────────────────────────────────────┐   │            │
│              │    │    │                    MAP WITH ROUTE                                │   │            │
│  [⭐] Rating │   │    │                                                                 │   │            │
│  & Feedback  │    │    │     ●━━━━━━━━━━━━━━━━━━━━━━━●━━━━━━━━━━━━●                     │   │            │
│              │    │    │    Start                    Waypoint         End                │   │            │
│  [⚙️] Settings│   │    │    (Green)                   (Orange)      (Red)                │   │            │
│              │    │    │                                                                 │   │            │
│              │    │    └─────────────────────────────────────────────────────────────────┘   │            │
│              │    │                                                                         │            │
│              │    │    Route Information:                                                     │            │
│              │    │    ┌────────────────────────────────────────────────────────────────┐  │            │
│              │    │    │ 📍 MST Building → 📍 Library                                  │  │            │
│              │    │    │ 📏 Distance: 150m  ⏱️ Time: 2 min  👣 Steps: 180              │  │            │
│              │    │    │                                                                 │  │            │
│              │    │    │ [📋 Show Turn-by-Turn Directions]                             │  │            │
│              │    │    │ 1. Head north from MST Building entrance                        │  │            │
│              │    │    │ 2. Turn right at the main pathway                              │  │            │
│              │    │    │ 3. Continue straight past the fountain                         │  │            │
│              │    │    │ 4. Library entrance is on your left                            │  │            │
│              │    │    └────────────────────────────────────────────────────────────────┘  │            │
│              │    │                                                                         │            │
├──────────────┴──────────────────────────────────────────────────────────────────────────────────────────┤
│  👤 Welcome, Guest                                                                    [❓ Help]        │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 1.3 Desktop Chatbot View

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  [Logo] TechnoPath                              Campus Assistant 🤖                                       │
├──────────────┬──────────────────────────────────────────────────────────────────────────────────────────┤
│              │                                                                                           │
│  [🏠] Home   │    ┌─────────────────────────────────────────────────────────────────────────┐            │
│              │    │  🤖 Campus Assistant                              [🔄 AI Powered]       │            │
│  [🗺️] Explore│    │                                                                         │            │
│      Map     │    │  ┌─────────────────────────────────────────────────────────────────┐   │            │
│              │    │  │ 🤖 Hello! I'm your SEAIT Campus Assistant...                 │   │            │
│  [🧭] Navigate│   │  │                                                                 │   │            │
│              │    │  │ 👤 Where is CL1?                                               │   │            │
│  [🤖] Chatbot│   │  │                                                                 │   │            │
│   (Active)   │    │  │ 🤖 CL1 (Computer Lab 1) is located on the 2nd floor of the...  │   │            │
│              │    │  │     MST Building. Here's how to get there:                      │   │            │
│  [🔔] Notif. │   │  │     • Enter through the main entrance                          │   │            │
│              │    │  │     • Take the stairs or elevator to Floor 2                   │   │            │
│  [⭐] Rating │   │  │     • CL1 is the first room on your right                      │   │            │
│  & Feedback  │    │  │     [🗺️ Show on Map]  [🧭 Navigate There]                        │   │            │
│              │    │  │                                                                 │   │            │
│  [⚙️] Settings│   │  │ 👤 What are the library hours?                                 │   │            │
│              │    │  │                                                                 │   │            │
│              │    │  │ 🤖 The SEAIT Library is open:                                  │   │            │
│              │    │  │     Monday-Friday: 8:00 AM - 8:00 PM                          │   │            │
│              │    │  │     Saturday: 8:00 AM - 5:00 PM                                │   │            │
│              │    │  │     Sunday: Closed                                             │   │            │
│              │    │  │                                                                 │   │            │
│              │    │  └─────────────────────────────────────────────────────────────────┘   │            │
│              │    │                                                                         │            │
│              │    │  Quick Actions:                                                           │            │
│              │    │  [Where is CL1?] [MST Building info] [Library hours] [Get to Registrar]   │            │
│              │    │                                                                         │            │
│              │    │  ┌────────────────────────────────────────────────────────────────┐       │            │
│              │    │  [📎] [Ask me anything about SEAIT...                    ] [➤]       │            │
│              │    │  └────────────────────────────────────────────────────────────────┘       │            │
│              │    │                                                                         │            │
├──────────────┴──────────────────────────────────────────────────────────────────────────────────────────┤
│  👤 Welcome, Guest                                                           [❓ FAQ] [📧 Support]    │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 1.4 Desktop Notifications View

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  [Logo] TechnoPath                              Notifications                                             │
├──────────────┬──────────────────────────────────────────────────────────────────────────────────────────┤
│              │                                                                                           │
│  [🏠] Home   │    ┌─────────────────────────────────────────────────────────────────────────┐            │
│              │    │  Filters: [All ▼] [Department: All ▼] [Time: Recent ▼]    [🔔 Settings]   │            │
│  [🗺️] Explore│    │                                                                         │            │
│      Map     │    │  📢 Announcements                                                        │            │
│              │    │  ┌─────────────────────────────────────────────────────────────────────┐ │            │
│  [🧭] Navigate│   │  │ 🔴 Urgent                                                                 │            │
│              │    │  │ 📢 Campus-Wide • Safety and Security Office                            │            │
│  [🤖] Chatbot│   │  │ Emergency Drill Tomorrow                                                 │            │
│              │    │  │ There will be a fire drill scheduled for tomorrow at 9:00 AM...         │            │
│  [🔔] Notif. │   │  │                                                    [📖 Read More]  [✓]   │            │
│   (Active)   │    │  │                                                      2 hours ago        │            │
│  (5 unread)  │    │  └─────────────────────────────────────────────────────────────────────┘ │            │
│  [⭐] Rating │   │                                                                          │            │
│  & Feedback  │    │  ┌─────────────────────────────────────────────────────────────────────┐ │            │
│              │    │  │ 🟢 General                                                                │            │
│  [⚙️] Settings│   │  │ 🎓 College • College of ICT                                              │            │
│              │    │  │ New Lab Equipment                                                         │            │
│              │    │  │ The ICT department has new computers available in CL5 and CL6...        │            │
│              │    │  │                                                    [📖 Read More]  [✓]   │            │
│              │    │  │                                                      5 hours ago        │            │
│              │    │  └─────────────────────────────────────────────────────────────────────┘ │            │
│              │    │                                                                          │            │
│              │    │  🔔 System Notifications                                                   │            │
│              │    │  ┌─────────────────────────────────────────────────────────────────────┐ │            │
│              │    │  │ ⚙️ System Maintenance                                                     │            │
│              │    │  │ The campus map system will undergo maintenance on Sunday...             │            │
│              │    │  │                                                      1 day ago          │            │
│              │    │  └─────────────────────────────────────────────────────────────────────┘ │            │
│              │    │                                                                          │            │
├──────────────┴──────────────────────────────────────────────────────────────────────────────────────────┤
│  👤 Welcome, Guest                                    [✓ Mark All Read]  [🗑️ Clear All]               │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. MOBILE VIEWS (< 1024px)

### 2.1 Mobile Splash Screen

```
┌─────────────────────────┐
│                         │
│                         │
│      [SEAIT Logo]       │
│                         │
│       TechnoPath        │
│    Campus Navigation    │
│                         │
│   "Find your way        │
│    around SEAIT"        │
│                         │
│                         │
│                         │
│    [◌ ◌ ●]              │
│                         │
│                         │
│    [Get Started]        │
│                         │
│    [Skip Tutorial]      │
│                         │
└─────────────────────────┘
```

**Components:**
- SEAIT logo centered
- App name and tagline
- Feature carousel indicators
- Get Started CTA button
- Skip option

---

### 2.2 Mobile Home / Map View

```
┌─────────────────────────┐
│ [🏢] Select Facility ▼  │  ← Top facility selector
│ [🚪] Select Room ▼      │  ← Top room selector
├─────────────────────────┤
│                         │
│    ┌───────────────┐   │
│    │               │   │
│    │   SEAIT       │   │
│    │   CAMPUS      │   │
│    │    MAP        │   │
│    │               │   │
│    │  📍           │   │  ← Map markers
│    │     📍        │   │
│    │        📍     │   │
│    │               │   │
│    │     [+]       │   │  ← Zoom in
│    │     [-]       │   │  ← Zoom out
│    └───────────────┘   │
│                         │
│  ┌───────────────────┐  │
│  │ 🔍 Search...      │  │  ← Search bar
│  └───────────────────┘  │
├─────────────────────────┤
│[☰] [📍] [⭐] [🔔3] [🤖]│  ← Bottom action bar
│Menu Locate Rate Notif Bot│
└─────────────────────────┘
```

**Components:**
- Facility/Room dropdown selectors at top
- Full-screen interactive map
- Floating zoom controls
- Collapsible search bar
- Bottom action button row

---

### 2.3 Mobile Menu Sheet (Slide-up)

```
┌─────────────────────────┐
│         ───             │  ← Handle indicator
│         Menu            │
├─────────────────────────┤
│                         │
│  ┌───────────────────┐  │
│  │ 🏢 Building Info  │  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │ 🚪 Rooms Info     │  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │ 👨‍🏫 Instructor Info│  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │ 👥 Employees      │  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │ 🔬 Laboratory Info│  │
│  └───────────────────┘  │
│                         │
│  ┌───────────────────┐  │
│  │      Close        │  │
│  └───────────────────┘  │
│                         │
└─────────────────────────┘
```

---

### 2.4 Mobile Navigation View

```
┌─────────────────────────┐
│ [←]  Navigate           │
├─────────────────────────┤
│                         │
│  From:                  │
│  ┌───────────────────┐  │
│  │ 📍 Select start...│  │
│  └───────────────────┘  │
│          🔄             │  ← Swap button
│  To:                    │
│  ┌───────────────────┐  │
│  │ 📍 Select dest... │  │
│  └───────────────────┘  │
│                         │
│  [    Find Route    ]   │
│                         │
├─────────────────────────┤
│                         │
│      ┌───────────┐      │
│      │ MAP VIEW  │      │
│      │  with     │      │
│      │  ROUTE    │      │
│      │   LINE    │      │
│      └───────────┘      │
│                         │
│  [+] [-]                │
│                         │
├─────────────────────────┤
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │  ← Pull handle
│  Route: 150m • 2 min    │
│  MST → Library          │
│                         │
│  [Show Directions ▼]    │
│                         │
│  1. Head north...       │
│  2. Turn right...       │
│  3. Continue...         │
│                         │
├─────────────────────────┤
│[🏠] [🗺️] [🤖] [⚙️]     │
│Home  Map   Bot  Settings│
└─────────────────────────┘
```

---

### 2.5 Mobile Chatbot View

```
┌─────────────────────────┐
│ [←] Campus Assistant 🤖 │
│ 🤖 • Online/Offline     │
├─────────────────────────┤
│                         │
│ ┌─────────────────────┐ │
│ │ 🤖 Hello! I'm your  │ │
│ │ SEAIT Campus Guide  │ │
│ └─────────────────────┘ │
│                         │
│ ┌─────────────────────┐ │
│ │ 👤 Where is CL1?    │ │
│ └─────────────────────┘ │
│                         │
│ ┌─────────────────────┐ │
│ │ 🤖 CL1 is in the    │ │
│ │ MST Building, 2F... │ │
│ │ [🗺️ Map] [🧭 Nav]   │ │
│ └─────────────────────┘ │
│                         │
│ ...                     │
│                         │
│ • • • (typing)          │
│                         │
├─────────────────────────┤
│ [FAQ?]                  │
│ ┌───────────────────┐   │
│ │ ❓ Where is CL1?  │   │
│ │ ❓ Library hours? │   │
│ │ ❓ Registrar loc?│   │
│ └───────────────────┘   │
├─────────────────────────┤
│ [?] [Ask anything... ] [➤]│
└─────────────────────────┘
```

---

### 2.6 Mobile Notifications View

```
┌─────────────────────────┐
│ [←] Notifications    [✓]│
├─────────────────────────┤
│ 🔴 Urgent (1)           │
│ ┌─────────────────────┐ │
││ 🔴 Safety & Security  ││
││ Emergency Drill      ││
││ Tomorrow 9AM...    ✓ ││
││              2h ago   ││
│ └─────────────────────┘ │
│                         │
│ 🟢 General (2)          │
│ ┌─────────────────────┐ │
││ 🟢 College of ICT    ││
││ New Lab Equipment    ││
││ Computers in CL5...✓ ││
││              5h ago   ││
│ └─────────────────────┘ │
│ ┌─────────────────────┐ │
││ 🟢 College Dean      ││
││ Exam Schedule        ││
││ Final exams start...✓ ││
││              1d ago   ││
│ └─────────────────────┘ │
│                         │
│ ⚙️ System (1)           │
│ ┌─────────────────────┐ │
││ ⚙️ Maintenance       ││
││ Sunday update...    ✓ ││
││              2d ago   ││
│ └─────────────────────┘ │
│                         │
├─────────────────────────┤
│[🏠] [🗺️] [🤖] [⚙️]     │
└─────────────────────────┘
```

---

### 2.7 Mobile Settings View

```
┌─────────────────────────┐
│ [←] Settings            │
├─────────────────────────┤
│                         │
│ Appearance              │
│ ┌─────────────────────┐ │
││ 🌙 Dark Mode        [ ]││
││ 🔲 High Contrast    [ ]││
││ 📏 Large Text       [ ]││
││ ✨ Reduce Animations[ ]││
│ └─────────────────────┘ │
│                         │
│ Language                │
│ ┌─────────────────────┐ │
││ 🌐 English         ▶  ││
│ └─────────────────────┘ │
│                         │
│ Notifications           │
│ ┌─────────────────────┐ │
││ 🔔 Push Notifications[✓]││
││ 📢 Announcements    [✓]││
││ 🚨 Emergency Alerts [✓]││
│ └─────────────────────┘ │
│                         │
│ Account                 │
│ ┌─────────────────────┐ │
││ 👤 My Profile      ▶  ││
││ ⭐ My Favorites    ▶  ││
││ 📝 My Feedback     ▶  ││
│ └─────────────────────┘ │
│                         │
│ System                  │
│ ┌─────────────────────┐ │
││ 📶 Offline Mode: Ready││
││ 🔄 Last Sync: 2m ago  ││
││ ℹ️  Version 4.0.1     ││
││ [🔄 Check Updates]    ││
│ └─────────────────────┘ │
│                         │
│ [🗑️ Clear Cache]        │
│ [📤 Export Data]        │
│                         │
├─────────────────────────┤
│[🏠] [🗺️] [🤖] [⚙️]✓   │
└─────────────────────────┘
```

---

## 3. ADMIN PANEL VIEWS (Desktop Only)

### 3.1 Admin Dashboard

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  T TechnoPath Admin Panel                                    👤 Admin Name • Dean • ICT Dept  [🚪]       │
├────────────────┬────────────────────────────────────────────────────────────────────────────────────────┤
│                │                                                                                        │
│  [▣] Dashboard │  Dashboard Overview                                                    📱 Mobile        │
│  (Active)      │                                                                                        │
│                │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                     │
│  MAP MGMT      │  │   🏢 12    │  │   🚪 45    │  │   📍 120   │  │   ❓ 25    │                     │
│  [🏢] Facilities│  │ Facilities │  │   Rooms    │  │  Markers   │  │   FAQs     │                     │
│  [🚪] Rooms    │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘                     │
│  [🗺️] Nav Graph│                                                                                        │
│  [❓] FAQ      │  ┌────────────────────────────────────────┐  ┌─────────────────────────────┐           │
│  [🔳] QR Codes │  │ 📊 Quick Stats                         │  │ 🔔 Pending Actions        │           │
│                │  │                                        │  │                             │           │
│  COMMUNICATIONS│  │ Total Announcements: 156               │  │ • 3 Pending Approvals    🔴  │           │
│  [📢] Announce.│  │ This Month: 12                         │  │ • 2 Unread Feedback      🟡  │           │
│  [⏳] Pending  │  │ Pending Approval: 3                    │  │ • 5 System Notifications 🟢  │           │
│    (3)         │  │                                        │  │                             │           │
│  [🔔] Send Notif│  │ Popular Searches:                      │  │ [View All →]                │           │
│                │  │ 1. CL1 (45 searches)                   │  └─────────────────────────────┘           │
│  ADMINISTRATION│  │ 2. Library (38 searches)               │                                              │
│  [👤] Admin Acct│  │ 3. Registrar (32 searches)           │  ┌─────────────────────────────┐           │
│  [⭐] Feedback │  │                                        │  │ 📈 Recent Activity          │           │
│  [📋] Audit Log│  │ User Feedback:                         │  │ • Published announcement    │           │
│                │  │ • Average Rating: 4.2/5                │  │ • Approved 2 announcements  │           │
│  SYSTEM        │  │ • Total Feedback: 89                   │  │ • Added 3 new rooms        │           │
│  [🌐] View Site│  └────────────────────────────────────────┘  │ • System backup completed  │           │
│                │                                              └─────────────────────────────┘           │
└────────────────┴────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 3.2 Admin Facilities Management

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  T TechnoPath Admin Panel                                          👤 Admin • Super Admin    [🚪]       │
├────────────────┬────────────────────────────────────────────────────────────────────────────────────────┤
│                │                                                                                        │
│  [▣] Dashboard │  🏢 Facilities Management                                                [+ Add New]  │
│                │                                                                                        │
│  MAP MGMT      │  ┌────────────────────────────────────────────────────────────────────────────────┐   │
│  [🏢] Facilities│  │ Search: [                                  ]    Filter: [All Depts ▼] [🔍]     │   │
│   (Active)     │  └────────────────────────────────────────────────────────────────────────────────┘   │
│  [🚪] Rooms    │                                                                                        │
│  [🗺️] Nav Graph│  ┌────────────────────────────────────────────────────────────────────────────────┐   │
│  [❓] FAQ      │  │ Code  │ Name              │ Department    │ Floors │ Rooms │ Status    │ Actions    │   │
│  [🔳] QR Codes │  ├───────┼───────────────────┼───────────────┼────────┼───────┼───────────┼────────────┤   │
│                │  │ MST   │ MST Building      │ ICT           │   3    │  15   │ ✓ Active  │ [✏️] [🗑️] │   │
│  COMMUNICATIONS│  │ JST   │ JST Building      │ Basic Ed      │   2    │  12   │ ✓ Active  │ [✏️] [🗑️] │   │
│  [📢] Announce.│  │ RST   │ RST Building      │ Engineering   │   4    │  18   │ ✓ Active  │ [✏️] [🗑️] │   │
│  [⏳] Pending  │  │ LIB   │ Library         │ General Ed    │   2    │   8   │ ✓ Active  │ [✏️] [🗑️] │   │
│  [🔔] Send Notif│  │ GYM   │ Gymnasium       │ Athletics     │   1    │   5   │ ✓ Active  │ [✏️] [🗑️] │   │
│                │  └────────────────────────────────────────────────────────────────────────────────┘   │
│  ADMINISTRATION│                                                                                        │
│  [👤] Admin Acct│  Showing 5 of 5 facilities                                                              │
│  [⭐] Feedback │  [← Previous] [1] [2] [3] [Next →]                                                     │
│  [📋] Audit Log│                                                                                        │
│                │                                                                                        │
│  SYSTEM        │                                                                                        │
│  [🌐] View Site│                                                                                        │
│                │                                                                                        │
└────────────────┴────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 3.3 Admin Announcement Approval Workflow

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  T TechnoPath Admin Panel                                          👤 Admin • Super Admin    [🚪]       │
├────────────────┬────────────────────────────────────────────────────────────────────────────────────────┤
│                │                                                                                        │
│  [▣] Dashboard │  ⏳ Pending Approvals (3)                                                              │
│                │                                                                                        │
│  MAP MGMT      │  ┌──────────────────────────────────────────────────────────────────────────────────┐ │
│  [🏢] Facilities│  │ 🟡 Pending Approval                                                                 │ │
│  [🚪] Rooms    │  │                                                                                   │ │
│  [🗺️] Nav Graph│  │ From: 👤 Prof. Smith • College of ICT Dean                                       │ │
│  [❓] FAQ      │  │ Submitted: 2 hours ago                                                           │ │
│  [🔳] QR Codes │  │ Scope: 🎓 College (all college students)                                        │ │
│                │  │                                                                                   │ │
│  COMMUNICATIONS│  │ Title: Computer Laboratory Schedule Update                                       │ │
│  [📢] Announce.│  │                                                                                   │ │
│  [⏳] Pending  │  │ Please be informed that CL3 and CL4 will be temporarily closed for...           │ │
│   (Active)     │  │ maintenance starting next Monday, March 15. Alternative labs CL1 and CL2...       │ │
│    [3]         │  │ will be open for extended hours.                                                  │ │
│  [🔔] Send Notif│  │                                                                                   │ │
│                │  │ ┌─────────────────────────────────────────────────────────────────────────────┐ │ │
│  ADMINISTRATION│  │ │ Reviewer Notes (optional):                                                    │ │ │
│  [👤] Admin Acct│  │ │ [                                                                          ] │ │ │
│  [⭐] Feedback │  │ └─────────────────────────────────────────────────────────────────────────────┘ │ │
│  [📋] Audit Log│  │                                                                                   │ │
│                │  │              [❌ Reject]              [✅ Approve & Publish]                      │ │
│  SYSTEM        │  │                                                                                   │ │
│  [🌐] View Site│  └──────────────────────────────────────────────────────────────────────────────────┘ │
│                │                                                                                        │
│                │  ┌──────────────────────────────────────────────────────────────────────────────────┐ │
│                │  │ 🟡 Pending Approval #2                                                            │ │
│                │  │ From: 👤 Prof. Garcia • Basic Education Head                                     │ │
│                │  │ ...                                                                               │ │
│                │  └──────────────────────────────────────────────────────────────────────────────────┘ │
│                │                                                                                        │
└────────────────┴────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. SCREEN FLOW DIAGRAMS

### 4.1 Guest User Flow (Mobile)

```
                    ┌──────────────┐
                    │   Splash     │
                    │   Screen     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
    ┌───────────────│     Home     │───────────────┐
    │               │    (Map)     │               │
    │               └──────┬───────┘               │
    │                      │                        │
    ▼                      ▼                        ▼
┌─────────┐         ┌─────────┐              ┌─────────┐
│  Menu   │         │ Search  │              │Marker   │
│ Sheet   │         │ Results │              │Popup    │
└────┬────┘         └────┬────┘              └────┬────┘
     │                   │                        │
     ▼                   ▼                        ▼
┌─────────┐         ┌─────────┐              ┌─────────┐
│Building │         │Navigate │              │Navigate │
│  Info   │         │  View   │              │  View   │
└─────────┘         └─────────┘              └─────────┘
     │                   ▲                        ▲
     │                   │                        │
     └───────────────────┴────────────────────────┘
                         │
           ┌─────────────┼─────────────┐
           │             │             │
           ▼             ▼             ▼
      ┌─────────┐   ┌─────────┐   ┌─────────┐
      │Chatbot  │   │Settings │   │Feedback │
      │  View   │   │  View   │   │  View   │
      └─────────┘   └─────────┘   └─────────┘
```

### 4.2 Admin User Flow (Desktop)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                          ADMIN AUTHENTICATION                                           │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
                                   ┌──────────────┐
                                   │ Admin Login  │
                                   └──────┬───────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        ADMIN DASHBOARD (Hub)                                            │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
       │              │              │              │              │              │
       ▼              ▼              ▼              ▼              ▼              ▼
  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
  │  Map    │   │Communic-│   │  Admin  │   │ System  │   │ Reports │   │  Audit  │
  │Management│   │ications │   │ Accounts│   │Settings │   │& Analytics│   │  Log    │
  └────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘
       │              │              │              │              │              │
   ┌───┴───┐      ┌───┴───┐      ┌───┴───┐      ┌───┴───┐      ┌───┴───┐      ┌───┴───┐
   │       │      │       │      │       │      │       │      │       │      │       │
   ▼       ▼      ▼       ▼      ▼       ▼      ▼       ▼      ▼       ▼      ▼       ▼
┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
│Facil│ │Rooms│ │Annou│ │Pend.│ │Admin│ │Feedb│ │Config│ │QR   │ │Usage│ │Searc│ │Audit│
│ities│ │     │ │nce  │ │Apprv│ │Accts│ │ack  │ │      │ │Codes│ │Stats│ │hHist│ │Trail│
└─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘
   │       │       │       │       │       │       │       │       │       │       │
   └───────┴───────┴───────┴───────┴───────┴───────┴───────┴───────┴───────┴───────┘
                                          │
                                          ▼
                                   ┌──────────────┐
                                   │   Logout /   │
                                   │  Return to   │
                                   │  Public Site │
                                   └──────────────┘
```

---

## 5. RESPONSIVE BREAKPOINTS

| Breakpoint | Width | Layout | Navigation |
|------------|-------|--------|------------|
| Mobile | < 640px | Single column | Bottom nav bar |
| Tablet | 640px - 1023px | Adaptable | Collapsible sidebar or bottom nav |
| Desktop | >= 1024px | Two column (sidebar + main) | Fixed left sidebar |

### 5.1 Component Behavior by Breakpoint

| Component | Mobile | Tablet | Desktop |
|-----------|--------|--------|---------|
| Navigation | Bottom bar | Bottom bar or hamburger | Fixed sidebar |
| Map View | Full screen with overlays | Full screen | Sidebar + main content |
| Admin Panel | Limited access warning | Collapsible menu | Full sidebar |
| Search | Floating bar | Floating bar | Top header bar |
| Info Menu | Slide-up sheet | Dropdown | Sidebar section |
| Chatbot | Full screen | Modal or side panel | Modal or side panel |

---

## 6. KEY UI ELEMENTS REFERENCE

### Icons (Material Design)
| Icon | Code | Usage |
|------|------|-------|
| 🏠 | home | Home navigation |
| 🗺️ | map | Explore map |
| 🧭 | directions | Navigate |
| 🤖 | smart_toy | Chatbot |
| 🔔 | notifications | Notifications |
| ⭐ | star | Ratings |
| ⚙️ | settings | Settings |
| ☰ | menu | Menu/Drawer |
| 📍 | location_on | Location marker |
| 🔍 | search | Search action |
| ← | arrow_back | Back navigation |
| ✓ | check | Confirm/Success |
| ✕ | close | Close/Cancel |
| ℹ️ | info | Information |
| 🏢 | business | Building/Facility |
| 🚪 | meeting_room | Room |
| 👤 | person | User |

---

*Document Version: 1.0*
*Generated from TechnoPath V4 Codebase Analysis*
